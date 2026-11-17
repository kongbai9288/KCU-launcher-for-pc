//! 软件完整性验证：签名、清单摘要、分级结果、安全模式诊断包。
//! 复用 updater::verify、ed25519_compact::sha512、robust、cache、envelope。
//! 信任根公钥与文件读取由调用方注入；本模块不内置密钥、不写路径、不发网络请求。

use crate::core::cache::Cache;
use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust::{self, OpBudget, MAX_TEXT_BYTES};
use crate::updater::verify::verify_detached;
use anyhow::{anyhow, Result};
use ed25519_compact::sha512;
use serde_json::{from_slice, Value};
use std::path::Path;
use std::time::Duration;

pub const MAX_MANIFEST_BYTES: usize = 1024 * 1024;
pub const MAX_MANIFEST_ENTRIES: usize = 4096;
pub const MAX_FILE_BYTES: usize = 64 * 1024 * 1024;
pub const SAFE_MODE_AFTER: u32 = 3;
pub const CACHE_CAPACITY: usize = 256;
pub const CACHE_TTL_SECS: u64 = 30;
pub const LOAD_TIMEOUT_SECS: u64 = 5;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ManifestEntry {
    pub path: String,
    pub sha512: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Manifest {
    pub entries: Vec<ManifestEntry>,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Level {
    Ok,
    Degraded,
    FeatureDisabled,
    Fatal,
}

impl Level {
    pub fn code(&self) -> &'static str {
        match self {
            Level::Ok => "ok",
            Level::Degraded => "degraded",
            Level::FeatureDisabled => "disabled",
            Level::Fatal => "fatal",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DiagnosticBundle {
    pub lines: Vec<String>,
    pub config_snapshot: String,
    pub runtime: String,
    pub modules: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct Outcome {
    pub level: Level,
    pub code: &'static str,
    pub envelope: Envelope,
    pub diagnostics: Vec<String>,
    pub checked: usize,
    pub mismatches: Vec<String>,
    pub safe_mode: bool,
    /// 原文第 12 行「失败则声明软件可能被修改，离线则不声明」。
    /// 离线时仍分级、仍记诊断、仍不给通过，只是不弹声明页。
    pub declaration: bool,
    pub bundle: Option<DiagnosticBundle>,
}

#[derive(Debug, Clone)]
pub struct VerifyInput<'a> {
    pub manifest_bytes: &'a [u8],
    pub public_key: &'a [u8],
    pub signature: &'a [u8],
    pub root: &'a Path,
    pub consecutive_failures: u32,
    pub offline: bool,
    pub config_snapshot: &'a str,
    pub runtime: &'a str,
    pub modules: &'a [String],
}

pub struct Verifier {
    digests: Cache<String, String>,
    budget: OpBudget,
}

impl Verifier {
    pub fn new() -> Self {
        Self {
            digests: Cache::new(CACHE_CAPACITY, Duration::from_secs(CACHE_TTL_SECS)),
            budget: OpBudget::new(robust::MAX_OPS_PER_WINDOW),
        }
    }

    /// 显式刷新：清空摘要缓存，下一次校验重新计算。签名与判定不走缓存。
    pub fn refresh(&self) {
        self.digests.clear();
    }

    pub fn cached(&self) -> usize {
        self.digests.len()
    }

    pub fn verify<F>(&self, input: &VerifyInput<'_>, read: F) -> Outcome
    where
        F: Fn(&Path) -> std::io::Result<Vec<u8>>,
    {
        if !self.budget.try_op() {
            return self.finish(
                Level::FeatureDisabled,
                "integrity.rate_limited",
                "DENY",
                input,
                0,
                Vec::new(),
                Vec::new(),
            );
        }

        if input.manifest_bytes.is_empty() || input.manifest_bytes.len() > MAX_MANIFEST_BYTES {
            return self.finish(
                Level::Fatal,
                "integrity.manifest_size",
                "DENY",
                input,
                0,
                Vec::new(),
                Vec::new(),
            );
        }

        // 签名在解析之前；不通过就不解析清单内容。
        if verify_detached(input.public_key, input.manifest_bytes, input.signature).is_err() {
            return self.finish(
                Level::FeatureDisabled,
                "integrity.signature",
                "DENY",
                input,
                0,
                Vec::new(),
                Vec::new(),
            );
        }

        let manifest = match parse_manifest(input.manifest_bytes) {
            Ok(m) => m,
            Err(_) => {
                return self.finish(
                    Level::Fatal,
                    "integrity.manifest_parse",
                    "DENY",
                    input,
                    0,
                    Vec::new(),
                    Vec::new(),
                )
            }
        };

        let mut mismatches = Vec::new();
        let mut missing = Vec::new();
        let mut checked = 0usize;
        let mut level = Level::Ok;
        let mut code: &'static str = "integrity.ok";

        for entry in &manifest.entries {
            let full = match robust::safe_join(input.root, &entry.path) {
                Ok(p) => p,
                Err(_) => {
                    level = Level::FeatureDisabled;
                    code = "integrity.path";
                    mismatches.push(entry.path.clone());
                    continue;
                }
            };
            let bytes = match read(&full) {
                Ok(b) => b,
                Err(_) => {
                    if level == Level::Ok {
                        level = Level::Degraded;
                        code = "integrity.missing_file";
                    }
                    missing.push(entry.path.clone());
                    continue;
                }
            };
            if bytes.len() > MAX_FILE_BYTES {
                level = Level::FeatureDisabled;
                code = "integrity.file_size";
                mismatches.push(entry.path.clone());
                continue;
            }
            let digest = match self.digest(&entry.path, bytes.len(), &bytes) {
                Ok(d) => d,
                Err(_) => {
                    return self.finish(
                        Level::Fatal,
                        "integrity.digest_cache",
                        "DENY",
                        input,
                        checked,
                        mismatches.clone(),
                        Vec::new(),
                    )
                }
            };
            checked += 1;
            if !digest.eq_ignore_ascii_case(entry.sha512.trim()) {
                level = Level::FeatureDisabled;
                code = "integrity.content_mismatch";
                mismatches.push(entry.path.clone());
            }
        }

        if level == Level::Ok && !missing.is_empty() {
            level = Level::Degraded;
            code = "integrity.missing_file";
        }

        let mut details = Vec::new();
        if !mismatches.is_empty() {
            details.push(format!("mismatches={}", mismatches.len()));
        }
        if !missing.is_empty() {
            details.push(format!("missing={}", missing.len()));
        }

        self.finish(
            level,
            code,
            if level == Level::Ok { "OK" } else { "DENY" },
            input,
            checked,
            mismatches,
            details,
        )
    }

    fn digest(&self, path: &str, len: usize, bytes: &[u8]) -> Result<String> {
        let key = format!("{}:{}", path, len);
        self.digests
            .get_or_load(key, Duration::from_secs(LOAD_TIMEOUT_SECS), || {
                let h = sha512::Hash::hash(bytes);
                Ok::<String, anyhow::Error>(hex::encode(h.as_ref()))
            })
            .map_err(|e| anyhow!("digest cache: {:?}", e))
    }

    #[allow(clippy::too_many_arguments)]
    fn finish(
        &self,
        level: Level,
        code: &'static str,
        result: &str,
        input: &VerifyInput<'_>,
        checked: usize,
        mismatches: Vec<String>,
        mut details: Vec<String>,
    ) -> Outcome {
        let safe_mode = level != Level::Ok && input.consecutive_failures >= SAFE_MODE_AFTER;
        let declaration = level != Level::Ok && !input.offline;
        details.push(format!("checked={}", checked));
        details.push(format!("level={}", level.code()));
        details.push(format!("declaration={}", if declaration { "1" } else { "0" }));
        if safe_mode {
            details.push("safe_mode=1".to_string());
        }

        let line = diag_line("core", "integrity", code, result, &details.join(" "));
        let mut diagnostics = vec![line];

        let mut envelope = Envelope::new(Kind::Response, "core.integrity")
            .with("code", code)
            .with("level", level.code())
            .with("checked", &checked.to_string())
            .with("declaration", if declaration { "1" } else { "0" })
            .with("offline", if input.offline { "1" } else { "0" })
            .with("safe_mode", if safe_mode { "1" } else { "0" });
        if level != Level::Ok {
            envelope = envelope.with_error(code);
        }

        let bundle = if safe_mode {
            let mut lines = diagnostics.clone();
            lines.push(diag_line(
                "core",
                "integrity",
                "safe_mode",
                "OK",
                &format!("failures={}", input.consecutive_failures),
            ));
            diagnostics = lines.clone();
            Some(DiagnosticBundle {
                lines,
                config_snapshot: input.config_snapshot.to_string(),
                runtime: input.runtime.to_string(),
                modules: input.modules.to_vec(),
            })
        } else {
            None
        };

        Outcome {
            level,
            code,
            envelope,
            diagnostics,
            checked,
            mismatches,
            safe_mode,
            declaration,
            bundle,
        }
    }
}

impl Default for Verifier {
    fn default() -> Self {
        Self::new()
    }
}

/// 清单只接受对象数组；缺字段、空集合、超量、非字符串都返回错误，不 panic。
fn parse_manifest(bytes: &[u8]) -> Result<Manifest> {
    let v: Value = from_slice(bytes)?;
    let arr = v
        .get("files")
        .and_then(Value::as_array)
        .ok_or_else(|| anyhow!("manifest files missing"))?;
    if arr.is_empty() || arr.len() > MAX_MANIFEST_ENTRIES {
        return Err(anyhow!("manifest files count invalid"));
    }
    let mut entries = Vec::with_capacity(arr.len());
    for item in arr {
        let path = item
            .get("path")
            .and_then(Value::as_str)
            .ok_or_else(|| anyhow!("manifest path missing"))?;
        let sum = item
            .get("sha512")
            .and_then(Value::as_str)
            .ok_or_else(|| anyhow!("manifest sha512 missing"))?;
        robust::check_text(path, MAX_TEXT_BYTES)?;
        if sum.len() != 128 || !sum.bytes().all(|b| b.is_ascii_hexdigit()) {
            return Err(anyhow!("manifest sha512 malformed"));
        }
        entries.push(ManifestEntry {
            path: path.to_string(),
            sha512: sum.to_string(),
        });
    }
    Ok(Manifest { entries })
}

#[cfg(test)]
mod tests {
    use super::*;
    use ed25519_compact::{KeyPair, Seed};
    use std::collections::BTreeMap;

    fn pair() -> KeyPair {
        KeyPair::from_seed(Seed::from_slice(&[11u8; 32]).unwrap())
    }

    fn digest_hex(bytes: &[u8]) -> String {
        hex::encode(sha512::Hash::hash(bytes).as_ref())
    }

    fn signed_manifest(files: &[(&str, &[u8])]) -> (Vec<u8>, Vec<u8>, Vec<u8>, BTreeMap<String, Vec<u8>>) {
        let mut rows = Vec::new();
        let mut disk: BTreeMap<String, Vec<u8>> = BTreeMap::new();
        for (p, b) in files {
            rows.push(format!(
                "{{\"path\":\"{}\",\"sha512\":\"{}\"}}",
                p,
                digest_hex(b)
            ));
            disk.insert((*p).to_string(), b.to_vec());
        }
        let body = format!("{{\"files\":[{}]}}", rows.join(","));
        let bytes = body.into_bytes();
        let kp = pair();
        let sig = kp.sk.sign(&bytes, None);
        (bytes, kp.pk.as_ref().to_vec(), sig.as_ref().to_vec(), disk)
    }

    fn input<'a>(
        manifest: &'a [u8],
        pk: &'a [u8],
        sig: &'a [u8],
        failures: u32,
    ) -> VerifyInput<'a> {
        VerifyInput {
            manifest_bytes: manifest,
            public_key: pk,
            signature: sig,
            root: Path::new("KCU"),
            consecutive_failures: failures,
            offline: false,
            config_snapshot: "{}",
            runtime: "test",
            modules: &[],
        }
    }

    fn reader(disk: &BTreeMap<String, Vec<u8>>) -> impl Fn(&Path) -> std::io::Result<Vec<u8>> + '_ {
        move |p: &Path| {
            let key = p.strip_prefix("KCU").unwrap_or(p).to_string_lossy().replace('\\', "/");
            disk.get(&key)
                .cloned()
                .ok_or_else(|| std::io::Error::new(std::io::ErrorKind::NotFound, "missing"))
        }
    }

    #[test]
    fn valid_manifest_passes() {
        let (m, pk, sig, disk) = signed_manifest(&[("config/launch.json", b"a"), ("core.bin", b"b")]);
        let v = Verifier::new();
        let o = v.verify(&input(&m, &pk, &sig, 0), reader(&disk));
        assert_eq!(o.level, Level::Ok);
        assert_eq!(o.checked, 2);
        assert!(!o.safe_mode);
        assert!(o.bundle.is_none());
        assert!(o.envelope.ok());
        assert_eq!(o.envelope.field("code"), Some("integrity.ok"));
    }

    #[test]
    fn signature_is_checked_before_manifest_parse() {
        let kp = pair();
        let m = b"not json at all".to_vec();
        let other = KeyPair::from_seed(Seed::from_slice(&[13u8; 32]).unwrap());
        let sig = other.sk.sign(&m, None);
        let v = Verifier::new();
        let o = v.verify(&input(&m, kp.pk.as_ref(), sig.as_ref(), 0), |_| Ok(vec![]));
        assert_eq!(o.code, "integrity.signature");
        assert_eq!(o.level, Level::FeatureDisabled);
        assert_eq!(o.checked, 0);
    }

    #[test]
    fn tampered_signed_manifest_is_rejected() {
        let (m, pk, sig, disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let mut altered = m.clone();
        altered.push(b' ');
        let v = Verifier::new();
        let o = v.verify(&input(&altered, &pk, &sig, 0), reader(&disk));
        assert_eq!(o.code, "integrity.signature");
    }

    #[test]
    fn content_mismatch_disables_custom_config() {
        let (m, pk, sig, _disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let mut changed = BTreeMap::new();
        changed.insert("config/launch.json".to_string(), b"tampered".to_vec());
        let v = Verifier::new();
        let o = v.verify(&input(&m, &pk, &sig, 0), reader(&changed));
        assert_eq!(o.code, "integrity.content_mismatch");
        assert_eq!(o.level, Level::FeatureDisabled);
        assert_eq!(o.mismatches, vec!["config/launch.json".to_string()]);
        assert!(!o.envelope.ok());
    }

    #[test]
    fn missing_file_degrades_instead_of_crashing() {
        let (m, pk, sig, disk) = signed_manifest(&[("config/launch.json", b"a"), ("core.bin", b"b")]);
        let mut partial = disk.clone();
        partial.remove("core.bin");
        let v = Verifier::new();
        let o = v.verify(&input(&m, &pk, &sig, 0), reader(&partial));
        assert_eq!(o.code, "integrity.missing_file");
        assert_eq!(o.level, Level::Degraded);
        assert_eq!(o.checked, 1);
    }

    #[test]
    fn empty_or_oversized_manifest_is_fatal() {
        let v = Verifier::new();
        let kp = pair();
        let empty = v.verify(&input(&[], kp.pk.as_ref(), &[0u8; 64], 0), |_| Ok(vec![]));
        assert_eq!(empty.code, "integrity.manifest_size");
        assert_eq!(empty.level, Level::Fatal);
        let big = vec![b'x'; MAX_MANIFEST_BYTES + 1];
        let o = v.verify(&input(&big, kp.pk.as_ref(), &[0u8; 64], 0), |_| Ok(vec![]));
        assert_eq!(o.code, "integrity.manifest_size");
    }

    #[test]
    fn manifest_shape_errors_are_fatal_not_panics() {
        let kp = pair();
        let v = Verifier::new();
        for body in [
            "{}".to_string(),
            "{\"files\":[]}".to_string(),
            "{\"files\":[{\"path\":\"a\"}]}".to_string(),
            "{\"files\":[{\"path\":\"a\",\"sha512\":\"zz\"}]}".to_string(),
        ] {
            let bytes = body.into_bytes();
            let sig = kp.sk.sign(&bytes, None);
            let o = v.verify(&input(&bytes, kp.pk.as_ref(), sig.as_ref(), 0), |_| Ok(vec![]));
            assert_eq!(o.level, Level::Fatal, "body={}", String::from_utf8_lossy(&bytes));
            assert_eq!(o.code, "integrity.manifest_parse");
        }
    }

    #[test]
    fn traversal_path_is_rejected() {
        let kp = pair();
        let body = format!(
            "{{\"files\":[{{\"path\":\"../outside\",\"sha512\":\"{}\"}}]}}",
            "0".repeat(128)
        );
        let bytes = body.into_bytes();
        let sig = kp.sk.sign(&bytes, None);
        let v = Verifier::new();
        let o = v.verify(&input(&bytes, kp.pk.as_ref(), sig.as_ref(), 0), |_| Ok(vec![]));
        assert_eq!(o.code, "integrity.path");
        assert_eq!(o.level, Level::FeatureDisabled);
    }

    #[test]
    fn three_consecutive_failures_enter_safe_mode_and_export_bundle() {
        let (m, pk, sig, _disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let mut changed = BTreeMap::new();
        changed.insert("config/launch.json".to_string(), b"bad".to_vec());
        let mods = vec!["core".to_string(), "plugins".to_string()];
        let mut inp = input(&m, &pk, &sig, 3);
        inp.config_snapshot = "{\"mode\":\"normal\"}";
        inp.runtime = "windows/x86_64";
        inp.modules = &mods;
        let v = Verifier::new();
        let o = v.verify(&inp, reader(&changed));
        assert!(o.safe_mode);
        let b = o.bundle.as_ref().expect("bundle");
        assert_eq!(b.config_snapshot, "{\"mode\":\"normal\"}");
        assert_eq!(b.runtime, "windows/x86_64");
        assert_eq!(b.modules, mods);
        assert!(b.lines.iter().any(|l| l.contains("safe_mode=1")));
        assert_eq!(o.envelope.field("safe_mode"), Some("1"));
    }

    #[test]
    fn safe_mode_is_not_triggered_below_threshold() {
        let (m, pk, sig, _disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let mut changed = BTreeMap::new();
        changed.insert("config/launch.json".to_string(), b"bad".to_vec());
        let v = Verifier::new();
        let o = v.verify(&input(&m, &pk, &sig, 2), reader(&changed));
        assert!(!o.safe_mode);
        assert!(o.bundle.is_none());
    }

    #[test]
    fn refresh_clears_digest_cache_without_skipping_signature() {
        let (m, pk, sig, disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let v = Verifier::new();
        let a = v.verify(&input(&m, &pk, &sig, 0), reader(&disk));
        assert_eq!(a.level, Level::Ok);
        assert_eq!(v.cached(), 1);
        v.refresh();
        assert_eq!(v.cached(), 0);
        let mut changed = BTreeMap::new();
        changed.insert("config/launch.json".to_string(), b"bad".to_vec());
        let b = v.verify(&input(&m, &pk, &sig, 0), reader(&changed));
        assert_eq!(b.code, "integrity.content_mismatch");
    }

    #[test]
    fn size_change_invalidates_cached_digest() {
        let (m, pk, sig, disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let v = Verifier::new();
        let a = v.verify(&input(&m, &pk, &sig, 0), reader(&disk));
        assert_eq!(a.level, Level::Ok);
        let mut changed = BTreeMap::new();
        changed.insert("config/launch.json".to_string(), b"longer-content".to_vec());
        let b = v.verify(&input(&m, &pk, &sig, 0), reader(&changed));
        assert_eq!(b.code, "integrity.content_mismatch");
    }

    #[test]
    fn rate_limit_never_returns_a_pass() {
        let (m, pk, sig, disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let v = Verifier::new();
        let mut last = Level::Ok;
        for _ in 0..(robust::MAX_OPS_PER_WINDOW + 4) {
            last = v.verify(&input(&m, &pk, &sig, 0), reader(&disk)).level;
        }
        assert_eq!(last, Level::FeatureDisabled);
        assert_eq!(v.verify(&input(&m, &pk, &sig, 0), reader(&disk)).code, "integrity.rate_limited");
    }

    #[test]
    fn diagnostics_are_single_line_prefixed() {
        let (m, pk, sig, disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let v = Verifier::new();
        let o = v.verify(&input(&m, &pk, &sig, 0), reader(&disk));
        for l in &o.diagnostics {
            assert!(l.starts_with("[KCU] "));
            assert!(!l.contains('\n'));
        }
    }

    #[test]
    fn offline_failure_suppresses_declaration_but_keeps_level() {
        let (m, pk, sig, _disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let mut changed = BTreeMap::new();
        changed.insert("config/launch.json".to_string(), b"bad".to_vec());
        let mut inp = input(&m, &pk, &sig, 0);
        inp.offline = true;
        let v = Verifier::new();
        let o = v.verify(&inp, reader(&changed));
        assert_eq!(o.code, "integrity.content_mismatch");
        assert_eq!(o.level, Level::FeatureDisabled);
        assert!(!o.declaration);
        assert_eq!(o.envelope.field("declaration"), Some("0"));
        assert_eq!(o.envelope.field("offline"), Some("1"));
        assert!(o.diagnostics[0].contains("declaration=0"));
    }

    #[test]
    fn online_failure_declares_software_may_be_modified() {
        let (m, pk, sig, _disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let mut changed = BTreeMap::new();
        changed.insert("config/launch.json".to_string(), b"bad".to_vec());
        let v = Verifier::new();
        let o = v.verify(&input(&m, &pk, &sig, 0), reader(&changed));
        assert!(o.declaration);
        assert_eq!(o.envelope.field("declaration"), Some("1"));
        assert_eq!(o.envelope.field("offline"), Some("0"));
        assert!(o.diagnostics[0].contains("declaration=1"));
    }

    #[test]
    fn passing_result_never_declares() {
        let (m, pk, sig, disk) = signed_manifest(&[("config/launch.json", b"a")]);
        let v = Verifier::new();
        let o = v.verify(&input(&m, &pk, &sig, 0), reader(&disk));
        assert_eq!(o.level, Level::Ok);
        assert!(!o.declaration);
        assert_eq!(o.envelope.field("declaration"), Some("0"));
    }

    #[test]
    fn level_codes_are_explicit_strings() {
        assert_eq!(Level::Ok.code(), "ok");
        assert_eq!(Level::Degraded.code(), "degraded");
        assert_eq!(Level::FeatureDisabled.code(), "disabled");
        assert_eq!(Level::Fatal.code(), "fatal");
    }
}

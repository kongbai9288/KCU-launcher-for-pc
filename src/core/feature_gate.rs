//! 自动关闭某功能：设备能力 + 平台下发策略的本地判定层。
//! 原文 `11-features-input.txt` 第 5 行：设备不支持时部分功能可能会被关闭；
//! 第 12 行：自动关闭某一功能，需有版本平台等信息。
//!
//! 平台策略字节、公钥、签名、设备能力、当前版本、日期全部由调用方注入；
//! 本模块不发网络请求、不内置密钥、不写绝对路径、不检测系统（能力由宿主 probe 注入）。
//! 判定全部复用已进构建的库：验签 036、版本 034、JSON 031、边界与限流 048、缓存 029、信封 031。

use crate::core::asynk::CancelToken;
use crate::core::cache::Cache;
use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust::{self, OpBudget, MAX_TEXT_BYTES};
use crate::updater::verify::verify_detached;
use anyhow::{anyhow, Result};
use serde_json::{from_slice, Value};
use std::cmp::Ordering;
use std::collections::BTreeMap;
use std::time::Duration;

pub const MAX_POLICY_BYTES: usize = 256 * 1024;
pub const MAX_POLICY_ENTRIES: usize = 512;
pub const MAX_REQUIRES: usize = 16;
pub const CACHE_CAPACITY: usize = 128;
pub const CACHE_TTL_SECS: u64 = 30;
pub const LOAD_TIMEOUT_SECS: u64 = 5;

/// 内置默认策略。原文第 12 行要求调度器送的 json「必须内置」；
/// 控制平面断开、签名不符、策略被删时一律回退到它，不擅自关闭用户功能。
pub const BUILTIN_POLICY: &str = r#"{"schema":1,"policy_version":"0.0.0","source":"builtin","entries":[]}"#;

/// 允许被关闭的功能白名单。未知 id 一律忽略，不让外部策略关掉任意入口。
pub const KNOWN_FEATURES: &[&str] = &[
    "feature.record",
    "feature.screenshot",
    "feature.skin_preview",
    "feature.projection_preview",
    "feature.music",
    "feature.phone_transfer",
    "feature.server_host",
    "feature.ai_interface",
    "feature.plugin_store",
    "feature.crash_upload",
    "feature.wiki_search",
    "feature.visitor_mode",
    "feature.multi_instance",
    "feature.backup_auto",
];

/// 020 锁定的核心槽位：设置与关于的位置、顺序、存在性都不可被策略或插件改写。
pub const CORE_LOCKED: &[&str] = &["core.locked.settings", "core.locked.about"];

const FORBIDDEN_ENTRY_KEYS: &[&str] = &[
    "url", "endpoint", "token", "key", "secret", "api", "password", "credential", "depends_on",
];

const ALLOWED_ENTRY_KEYS: &[&str] = &[
    "id", "owner", "expires", "reason_key", "requires", "min_app", "max_app", "default",
];

/// 宿主注入的设备能力；本模块不做任何系统检测。
#[derive(Debug, Clone, Default)]
pub struct DeviceCaps {
    pub app_version: String,
    pub today: String,
    pub context: BTreeMap<String, bool>,
}

impl DeviceCaps {
    pub fn context(&self, key: &str) -> bool {
        self.context.get(key).copied().unwrap_or(false)
    }
}

#[derive(Clone)]
pub struct GateInput<'a> {
    pub policy_bytes: &'a [u8],
    pub public_key: &'a [u8],
    pub signature: &'a [u8],
    /// None 表示控制平面断开（文件被删 / 离线 / 未取到），走内置默认策略。
    pub policy_present: bool,
    pub caps: &'a DeviceCaps,
    pub locale: &'a str,
    pub cancel: &'a CancelToken,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GateSource {
    Builtin,
    Platform,
}

impl GateSource {
    pub fn code(&self) -> &'static str {
        match self {
            GateSource::Builtin => "builtin",
            GateSource::Platform => "platform",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FeatureState {
    pub id: String,
    pub enabled: bool,
    pub reason_key: &'static str,
    pub source: GateSource,
}

/// 声明页条目：与 051 `DECLARATION` 三动作（用默认继续 / 重新获取 / 取消）对齐。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Notice {
    pub id: String,
    pub reason_key: &'static str,
    pub level: &'static str,
    pub closable: bool,
    pub actions: Vec<&'static str>,
    pub source: GateSource,
}

impl Notice {
    fn new(id: &str, reason_key: &'static str, source: GateSource) -> Self {
        Self {
            id: id.to_string(),
            reason_key,
            level: "info",
            closable: true,
            actions: vec!["gate.act.default", "gate.act.refresh", "gate.act.cancel"],
            source,
        }
    }
}

#[derive(Debug, Clone)]
pub struct GateOutcome {
    pub source: GateSource,
    pub code: &'static str,
    pub features: Vec<FeatureState>,
    pub notices: Vec<Notice>,
    pub diagnostics: Vec<String>,
    pub envelope: Envelope,
    pub cancelled: bool,
    pub policy_version: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Entry {
    id: String,
    owner: String,
    expires: String,
    reason_key: &'static str,
    requires: Vec<String>,
    min_app: Option<String>,
    max_app: Option<String>,
}

pub struct FeatureGate {
    decisions: Cache<String, bool>,
    budget: OpBudget,
}

impl FeatureGate {
    pub fn new() -> Self {
        Self {
            decisions: Cache::new(CACHE_CAPACITY, Duration::from_secs(CACHE_TTL_SECS)),
            budget: OpBudget::new(robust::MAX_OPS_PER_WINDOW),
        }
    }

    /// 显式刷新：清空判定缓存，下一次 `evaluate` 重跑签名与全部判定。
    pub fn refresh(&self) {
        self.decisions.clear();
    }

    pub fn cached(&self) -> usize {
        self.decisions.len()
    }

    pub fn evaluate(&self, input: &GateInput<'_>) -> GateOutcome {
        if input.cancel.is_cancelled() {
            return self.finish(
                GateSource::Builtin,
                "gate.cancelled",
                Vec::new(),
                Vec::new(),
                Vec::new(),
                input,
                true,
                "0.0.0".to_string(),
            );
        }

        if !self.budget.try_op() {
            return self.finish(
                GateSource::Builtin,
                "gate.rate_limited",
                Vec::new(),
                Vec::new(),
                Vec::new(),
                input,
                false,
                "0.0.0".to_string(),
            );
        }

        let (bytes, source, code, version) = match self.policy(input) {
            Ok(v) => v,
            Err(c) => {
                return self.finish(
                    GateSource::Builtin,
                    c,
                    Vec::new(),
                    Vec::new(),
                    Vec::new(),
                    input,
                    false,
                    "0.0.0".to_string(),
                )
            }
        };

        let entries = match parse_entries(&bytes) {
            Ok(e) => e,
            Err(_) => {
                return self.finish(
                    GateSource::Builtin,
                    "gate.policy_parse",
                    Vec::new(),
                    Vec::new(),
                    Vec::new(),
                    input,
                    false,
                    version,
                )
            }
        };

        let mut features = Vec::new();
        let mut notices = Vec::new();
        for entry in &entries {
            let enabled = self.decide(entry, input.caps);
            features.push(FeatureState {
                id: entry.id.clone(),
                enabled,
                reason_key: entry.reason_key,
                source,
            });
            if !enabled {
                notices.push(Notice::new(&entry.id, entry.reason_key, source));
            }
        }
        let code = if notices.is_empty() { code } else { "gate.disabled" };

        self.finish(source, code, features, notices, Vec::new(), input, false, version)
    }

    /// 顺序：存在性 → 大小 → 验签 → 解析。验签失败不解析内容，且不执行任何关闭。
    fn policy<'a>(
        &self,
        input: &'a GateInput<'_>,
    ) -> Result<(Vec<u8>, GateSource, &'static str, String), &'static str> {
        if !input.policy_present || input.policy_bytes.is_empty() {
            let v = parse_version(BUILTIN_POLICY.as_bytes()).unwrap_or_else(|_| "0.0.0".to_string());
            return Ok((BUILTIN_POLICY.as_bytes().to_vec(), GateSource::Builtin, "gate.builtin", v));
        }
        if input.policy_bytes.len() > MAX_POLICY_BYTES {
            return Err("gate.policy_size");
        }
        if verify_detached(input.public_key, input.policy_bytes, input.signature).is_err() {
            let v = parse_version(BUILTIN_POLICY.as_bytes()).unwrap_or_else(|_| "0.0.0".to_string());
            return Ok((BUILTIN_POLICY.as_bytes().to_vec(), GateSource::Builtin, "gate.signature", v));
        }
        let version = parse_version(input.policy_bytes).unwrap_or_else(|_| "0.0.0".to_string());
        Ok((
            input.policy_bytes.to_vec(),
            GateSource::Platform,
            "gate.policy_ok",
            version,
        ))
    }

    /// 单条独立判定，禁止嵌套依赖（组合数指数增长）。
    /// 任何判定输入异常一律取 enabled=true：误关用户功能比不关更糟。
    fn decide(&self, entry: &Entry, caps: &DeviceCaps) -> bool {
        if CORE_LOCKED.contains(&entry.id.as_str()) || !KNOWN_FEATURES.contains(&entry.id.as_str()) {
            return true;
        }
        if !entry.expires.is_empty() && !caps.today.is_empty() && entry.expires.as_str() < caps.today.as_str() {
            return true;
        }
        let key = format!("{}:{}:{}", entry.id, caps.app_version, caps.today);
        let decided = self.decisions.get_or_load(
            key,
            Duration::from_secs(LOAD_TIMEOUT_SECS),
            || -> Result<bool, anyhow::Error> {
                for req in &entry.requires {
                    if !caps.context(req) {
                        return Ok(false);
                    }
                }
                let cur = match semver::Version::parse(&caps.app_version) {
                    Ok(v) => v,
                    Err(_) => return Ok(true),
                };
                if let Some(min) = &entry.min_app {
                    let v = match semver::Version::parse(min) {
                        Ok(v) => v,
                        Err(_) => return Ok(true),
                    };
                    if cur.cmp_precedence(&v) == Ordering::Less {
                        return Ok(false);
                    }
                }
                if let Some(max) = &entry.max_app {
                    let v = match semver::Version::parse(max) {
                        Ok(v) => v,
                        Err(_) => return Ok(true),
                    };
                    if cur.cmp_precedence(&v) == Ordering::Greater {
                        return Ok(false);
                    }
                }
                Ok(true)
            },
        );
        decided.unwrap_or(true)
    }

    #[allow(clippy::too_many_arguments)]
    fn finish(
        &self,
        source: GateSource,
        code: &'static str,
        features: Vec<FeatureState>,
        notices: Vec<Notice>,
        mut extra: Vec<String>,
        input: &GateInput<'_>,
        cancelled: bool,
        policy_version: String,
    ) -> GateOutcome {
        let disabled = features.iter().filter(|f| !f.enabled).count();
        let mut details = vec![
            format!("source={}", source.code()),
            format!("features={}", features.len()),
            format!("disabled={}", disabled),
            format!("notices={}", notices.len()),
            format!("locale={}", input.locale),
        ];
        if cancelled {
            details.push("cancel=1".to_string());
        }
        details.append(&mut extra);

        let line = diag_line("core", "feature_gate", code, "OK", &details.join(" "));
        let mut diagnostics = vec![line];

        // 声明必须可见、可关、流程后 0 残留：每条关闭给一条可追溯诊断。
        for n in &notices {
            diagnostics.push(diag_line(
                "core",
                "feature_gate",
                "notice",
                "OK",
                &format!("id={} reason={} source={} closable=1", n.id, n.reason_key, n.source.code()),
            ));
        }

        let mut envelope = Envelope::new(Kind::Response, "core.feature_gate")
            .with("code", code)
            .with("source", source.code())
            .with("policy_version", &policy_version)
            .with("features", &features.len().to_string())
            .with("disabled", &disabled.to_string())
            .with("notices", &notices.len().to_string())
            .with("cancel", if cancelled { "1" } else { "0" });
        if matches!(code, "gate.signature" | "gate.policy_size" | "gate.policy_parse" | "gate.rate_limited") {
            envelope = envelope.with_error(code);
        }

        GateOutcome {
            source,
            code,
            features,
            notices,
            diagnostics,
            envelope,
            cancelled,
            policy_version,
        }
    }
}

impl Default for FeatureGate {
    fn default() -> Self {
        Self::new()
    }
}

fn parse_version(bytes: &[u8]) -> Result<String> {
    let v: Value = from_slice(bytes)?;
    let s = v
        .get("policy_version")
        .and_then(Value::as_str)
        .ok_or_else(|| anyhow!("policy_version missing"))?;
    robust::check_text(s, MAX_TEXT_BYTES)?;
    Ok(s.to_string())
}

/// 严格字段白名单：不放 API 地址、不放凭据、不放嵌套依赖。
/// 未知 id 忽略而不是报错；畸形条目整体拒绝，避免逐条静默吞掉。
fn parse_entries(bytes: &[u8]) -> Result<Vec<Entry>> {
    let v: Value = from_slice(bytes)?;
    let schema = v.get("schema").and_then(Value::as_u64).unwrap_or(0);
    if schema != 1 {
        return Err(anyhow!("unsupported schema"));
    }
    let arr = v
        .get("entries")
        .and_then(Value::as_array)
        .ok_or_else(|| anyhow!("entries missing"))?;
    if arr.len() > MAX_POLICY_ENTRIES {
        return Err(anyhow!("too many entries"));
    }
    let mut out = Vec::new();
    for item in arr {
        let obj = item.as_object().ok_or_else(|| anyhow!("entry not object"))?;
        for k in obj.keys() {
            if !ALLOWED_ENTRY_KEYS.contains(&k.as_str()) || FORBIDDEN_ENTRY_KEYS.contains(&k.as_str()) {
                return Err(anyhow!("forbidden entry key"));
            }
        }
        let id = get_str(obj, "id")?;
        robust::check_text(&id, MAX_TEXT_BYTES)?;
        if !KNOWN_FEATURES.contains(&id.as_str()) {
            continue;
        }
        let owner = get_str(obj, "owner")?;
        robust::check_text(&owner, MAX_TEXT_BYTES)?;
        let expires = obj.get("expires").and_then(Value::as_str).unwrap_or("").to_string();
        if !expires.is_empty() && !is_iso_date(&expires) {
            return Err(anyhow!("expires malformed"));
        }
        let reason_key = match obj.get("reason_key").and_then(Value::as_str).unwrap_or("") {
            "gate.reason.device" => "gate.reason.device",
            "gate.reason.version" => "gate.reason.version",
            "gate.reason.platform" => "gate.reason.platform",
            _ => "gate.reason.device",
        };
        let requires = match obj.get("requires") {
            Some(Value::Array(a)) => {
                if a.len() > MAX_REQUIRES {
                    return Err(anyhow!("too many requires"));
                }
                let mut r = Vec::with_capacity(a.len());
                for x in a {
                    let s = x.as_str().ok_or_else(|| anyhow!("requires not string"))?;
                    robust::check_text(s, MAX_TEXT_BYTES)?;
                    r.push(s.to_string());
                }
                r
            }
            Some(_) => return Err(anyhow!("requires not array")),
            None => Vec::new(),
        };
        let min_app = opt_str(obj, "min_app")?;
        let max_app = opt_str(obj, "max_app")?;
        if let Some(d) = obj.get("default").and_then(Value::as_str) {
            if d != "on" && d != "off" {
                return Err(anyhow!("default invalid"));
            }
        }
        out.push(Entry {
            id,
            owner,
            expires,
            reason_key,
            requires,
            min_app,
            max_app,
        });
    }
    Ok(out)
}

fn get_str(obj: &serde_json::Map<String, Value>, key: &str) -> Result<String> {
    obj.get(key)
        .and_then(Value::as_str)
        .map(|s| s.to_string())
        .ok_or_else(|| anyhow!("{} missing", key))
}

fn opt_str(obj: &serde_json::Map<String, Value>, key: &str) -> Result<Option<String>> {
    match obj.get(key) {
        None => Ok(None),
        Some(Value::String(s)) => {
            robust::check_text(s, MAX_TEXT_BYTES)?;
            Ok(Some(s.clone()))
        }
        Some(_) => Err(anyhow!("{} not string", key)),
    }
}

fn is_iso_date(s: &str) -> bool {
    let b = s.as_bytes();
    b.len() == 10
        && b[4] == b'-'
        && b[7] == b'-'
        && b.iter().enumerate().all(|(i, c)| {
            if i == 4 || i == 7 {
                true
            } else {
                c.is_ascii_digit()
            }
        })
}

#[cfg(test)]
mod tests {
    use super::*;
    use ed25519_compact::{KeyPair, Seed};

    fn pair() -> KeyPair {
        KeyPair::from_seed(Seed::from_slice(&[23u8; 32]).unwrap())
    }

    fn caps() -> DeviceCaps {
        let mut c = DeviceCaps {
            app_version: "0.4.0".to_string(),
            today: "2026-11-17".to_string(),
            context: BTreeMap::new(),
        };
        c.context.insert("webview2".to_string(), true);
        c.context.insert("gpu".to_string(), true);
        c
    }

    fn signed_policy(body: &str) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
        let bytes = body.as_bytes().to_vec();
        let kp = pair();
        let sig = kp.sk.sign(&bytes, None);
        (bytes, kp.pk.as_ref().to_vec(), sig.as_ref().to_vec())
    }

    fn platform(entries: &str) -> (Vec<u8>, Vec<u8>, Vec<u8>) {
        signed_policy(&format!(
            "{{\"schema\":1,\"policy_version\":\"1.2.0\",\"source\":\"platform\",\"entries\":[{}]}}",
            entries
        ))
    }

    fn input<'a>(
        bytes: &'a [u8],
        pk: &'a [u8],
        sig: &'a [u8],
        present: bool,
        caps: &'a DeviceCaps,
        cancel: &'a CancelToken,
    ) -> GateInput<'a> {
        GateInput {
            policy_bytes: bytes,
            public_key: pk,
            signature: sig,
            policy_present: present,
            caps,
            locale: "zh-CN",
            cancel,
        }
    }

    #[test]
    fn builtin_policy_is_used_when_control_plane_is_absent() {
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        let o = g.evaluate(&input(&[], &[], &[], false, &c, &t));
        assert_eq!(o.source, GateSource::Builtin);
        assert_eq!(o.code, "gate.builtin");
        assert!(o.features.is_empty());
        assert!(o.notices.is_empty());
        assert!(o.envelope.ok());
    }

    #[test]
    fn signature_failure_never_disables_anything() {
        let (m, _pk, _sig) = platform("{\"id\":\"feature.record\",\"owner\":\"core\",\"requires\":[\"webview2\"]}");
        let other = KeyPair::from_seed(Seed::from_slice(&[31u8; 32]).unwrap());
        let sig = other.sk.sign(&m, None);
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        let o = g.evaluate(&input(&m, pair().pk.as_ref(), sig.as_ref(), true, &c, &t));
        assert_eq!(o.code, "gate.signature");
        assert_eq!(o.source, GateSource::Builtin);
        assert!(o.features.iter().all(|f| f.enabled));
        assert!(!o.envelope.ok());
    }

    #[test]
    fn missing_device_capability_disables_only_that_feature_with_notice() {
        let (m, pk, sig) = platform(
            "{\"id\":\"feature.record\",\"owner\":\"core\",\"reason_key\":\"gate.reason.device\",\"requires\":[\"webview2\",\"gpu\"]}",
        );
        let mut c = caps();
        c.context.insert("gpu".to_string(), false);
        let g = FeatureGate::new();
        let t = CancelToken::new();
        let o = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
        assert_eq!(o.source, GateSource::Platform);
        assert_eq!(o.code, "gate.disabled");
        assert_eq!(o.features.len(), 1);
        assert!(!o.features[0].enabled);
        assert_eq!(o.features[0].reason_key, "gate.reason.device");
        assert_eq!(o.notices.len(), 1);
        assert!(o.notices[0].closable);
        assert_eq!(o.notices[0].actions.len(), 3);
        assert_eq!(o.envelope.field("disabled"), Some("1"));
    }

    #[test]
    fn version_range_uses_precedence_not_equality() {
        let (m, pk, sig) = platform(
            "{\"id\":\"feature.music\",\"owner\":\"core\",\"reason_key\":\"gate.reason.version\",\"min_app\":\"0.5.0\"}",
        );
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        let o = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
        assert!(!o.features[0].enabled);
        let mut c2 = caps();
        c2.app_version = "0.5.0+paper.1".to_string();
        let g2 = FeatureGate::new();
        let o2 = g2.evaluate(&input(&m, &pk, &sig, true, &c2, &t));
        assert!(o2.features[0].enabled);
    }

    #[test]
    fn core_locked_and_unknown_ids_are_never_disabled() {
        let body = format!(
            "{{\"schema\":1,\"policy_version\":\"1.0.0\",\"entries\":[{{\"id\":\"core.locked.settings\",\"owner\":\"x\",\"requires\":[\"nope\"]}},{{\"id\":\"feature.not_registered\",\"owner\":\"x\",\"requires\":[\"nope\"]}},{{\"id\":\"feature.record\",\"owner\":\"core\",\"requires\":[\"webview2\"]}}]}}"
        );
        let (m, pk, sig) = signed_policy(&body);
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        let o = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
        assert_eq!(o.features.len(), 1);
        assert_eq!(o.features[0].id, "feature.record");
        assert!(o.features[0].enabled);
        assert!(o.notices.is_empty());
    }

    #[test]
    fn forbidden_keys_are_rejected_before_any_decision() {
        for key in ["url", "token", "depends_on"] {
            let body = format!(
                "{{\"schema\":1,\"policy_version\":\"1.0.0\",\"entries\":[{{\"id\":\"feature.record\",\"owner\":\"core\",\"{}\":\"x\"}}]}}",
                key
            );
            let (m, pk, sig) = signed_policy(&body);
            let g = FeatureGate::new();
            let c = caps();
            let t = CancelToken::new();
            let o = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
            assert_eq!(o.code, "gate.policy_parse", "key={}", key);
            assert!(o.features.is_empty());
        }
    }

    #[test]
    fn oversized_and_malformed_policies_fall_back() {
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        let kp = pair();
        let big = vec![b'x'; MAX_POLICY_BYTES + 1];
        let o = g.evaluate(&input(&big, kp.pk.as_ref(), &[0u8; 64], true, &c, &t));
        assert_eq!(o.code, "gate.policy_size");
        assert_eq!(o.source, GateSource::Builtin);
        let weird = b"not json".to_vec();
        let sig = kp.sk.sign(&weird, None);
        let o2 = g.evaluate(&input(&weird, kp.pk.as_ref(), sig.as_ref(), true, &c, &t));
        assert_eq!(o2.code, "gate.policy_parse");
    }

    #[test]
    fn expired_entry_is_ignored() {
        let (m, pk, sig) = platform(
            "{\"id\":\"feature.music\",\"owner\":\"core\",\"expires\":\"2020-01-01\",\"requires\":[\"nope\"]}",
        );
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        let o = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
        assert_eq!(o.features.len(), 1);
        assert!(o.features[0].enabled);
        assert!(o.notices.is_empty());
    }

    #[test]
    fn refresh_clears_decisions_and_reruns_signature() {
        let (m, pk, sig) = platform(
            "{\"id\":\"feature.record\",\"owner\":\"core\",\"requires\":[\"webview2\"]}",
        );
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        let a = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
        assert!(a.features[0].enabled);
        assert_eq!(g.cached(), 1);
        g.refresh();
        assert_eq!(g.cached(), 0);
        let mut c2 = caps();
        c2.context.insert("webview2".to_string(), false);
        let b = g.evaluate(&input(&m, &pk, &sig, true, &c2, &t));
        assert!(!b.features[0].enabled);
    }

    #[test]
    fn cancel_has_no_side_effects() {
        let (m, pk, sig) = platform(
            "{\"id\":\"feature.record\",\"owner\":\"core\",\"requires\":[\"nope\"]}",
        );
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        t.cancel();
        let o = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
        assert!(o.cancelled);
        assert_eq!(o.code, "gate.cancelled");
        assert!(o.features.is_empty());
        assert!(o.notices.is_empty());
        assert_eq!(g.cached(), 0);
        assert_eq!(o.envelope.field("cancel"), Some("1"));
    }

    #[test]
    fn rate_limit_does_not_disable_features() {
        let (m, pk, sig) = platform("{\"id\":\"feature.music\",\"owner\":\"core\"}");
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        let mut last = String::new();
        for _ in 0..(robust::MAX_OPS_PER_WINDOW + 3) {
            last = g.evaluate(&input(&m, &pk, &sig, true, &c, &t)).code.to_string();
        }
        assert_eq!(last, "gate.rate_limited");
        let o = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
        assert!(o.notices.is_empty());
        assert_eq!(o.envelope.field("disabled"), Some("0"));
    }

    #[test]
    fn every_notice_is_closable_and_diagnostics_are_single_line() {
        let (m, pk, sig) = platform(
            "{\"id\":\"feature.record\",\"owner\":\"core\",\"requires\":[\"nope\"]},{\"id\":\"feature.music\",\"owner\":\"core\",\"requires\":[\"gpu\"]}",
        );
        let mut c = caps();
        c.context.insert("gpu".to_string(), false);
        let g = FeatureGate::new();
        let t = CancelToken::new();
        let o = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
        assert_eq!(o.notices.len(), 2);
        assert!(o.notices.iter().all(|n| n.closable && n.actions.len() == 3));
        for l in &o.diagnostics {
            assert!(l.starts_with("[KCU] "));
            assert!(!l.contains('\n'));
        }
        assert_eq!(o.diagnostics.len(), 3);
    }

    #[test]
    fn policy_version_is_recorded_in_envelope() {
        let (m, pk, sig) = platform("{\"id\":\"feature.music\",\"owner\":\"core\"}");
        let g = FeatureGate::new();
        let c = caps();
        let t = CancelToken::new();
        let o = g.evaluate(&input(&m, &pk, &sig, true, &c, &t));
        assert_eq!(o.policy_version, "1.2.0");
        assert_eq!(o.envelope.field("policy_version"), Some("1.2.0"));
        assert_eq!(o.envelope.field("source"), Some("platform"));
    }

    #[test]
    fn iso_date_validator_rejects_malformed() {
        assert!(is_iso_date("2027-12-31"));
        assert!(!is_iso_date("2027-1-1"));
        assert!(!is_iso_date("2027/12/31"));
        assert!(!is_iso_date("202a-12-31"));
    }

    #[test]
    fn source_codes_are_explicit_strings() {
        assert_eq!(GateSource::Builtin.code(), "builtin");
        assert_eq!(GateSource::Platform.code(), "platform");
    }
}

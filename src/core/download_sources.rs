use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const SOURCES_FILE: &str = "download-sources.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_SOURCES: &str = r#"{"schema":1,"tier":"auto_mirror","max_concurrent":3,"restricted_auto":false,"restricted":[],"key_present":false}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_RESTRICTED: usize = 64;
pub const MAX_CONCURRENT: u64 = 64;
pub const DEFAULT_CONCURRENT: u64 = 3;
pub const SOURCES_TARGET: &str = "download.sources";
pub const KNOWN_KEYS: &[&str] = &[
    "schema", "tier", "max_concurrent", "restricted_auto", "restricted", "key_present",
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SourceTier {
    AutoMirror,
    OfficialFirst,
    OriginalOnly,
}

impl SourceTier {
    pub fn code(&self) -> &'static str {
        match self {
            SourceTier::AutoMirror => "auto_mirror",
            SourceTier::OfficialFirst => "official_first",
            SourceTier::OriginalOnly => "original_only",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "auto_mirror" => Some(SourceTier::AutoMirror),
            "official_first" => Some(SourceTier::OfficialFirst),
            "original_only" => Some(SourceTier::OriginalOnly),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SourceKind {
    Mirror,
    Official,
    Original,
}

impl SourceKind {
    pub fn code(&self) -> &'static str {
        match self {
            SourceKind::Mirror => "mirror",
            SourceKind::Official => "official",
            SourceKind::Original => "original",
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RestrictedEntry {
    pub id: String,
    pub imported: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SourcePolicy {
    pub tier: SourceTier,
    pub max_concurrent: u64,
    pub restricted_auto: bool,
    pub restricted: Vec<RestrictedEntry>,
    pub key_present: bool,
}

impl Default for SourcePolicy {
    fn default() -> Self {
        SourcePolicy {
            tier: SourceTier::AutoMirror,
            max_concurrent: DEFAULT_CONCURRENT,
            restricted_auto: false,
            restricted: Vec::new(),
            key_present: false,
        }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("download", action, "sources", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("download", action, "sources", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_ID_BYTES && !has_control(s)
}

fn entry_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| k == "id" || k == "imported")
}

fn parse(raw: &str) -> (SourcePolicy, Vec<String>) {
    let mut lines = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (SourcePolicy::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (SourcePolicy::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (SourcePolicy::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (SourcePolicy::default(), lines);
    }
    let tier = match obj.get("tier").and_then(Value::as_str).and_then(SourceTier::parse) {
        Some(t) => t,
        None => {
            lines.push(degrade("load", "tier_invalid"));
            return (SourcePolicy::default(), lines);
        }
    };
    let max_concurrent = match obj.get("max_concurrent").and_then(Value::as_u64) {
        Some(n) if (1..=MAX_CONCURRENT).contains(&n) => n,
        _ => {
            lines.push(degrade("load", "concurrent_invalid"));
            return (SourcePolicy::default(), lines);
        }
    };
    let restricted_auto = match obj.get("restricted_auto").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "flag_invalid"));
            return (SourcePolicy::default(), lines);
        }
    };
    let key_present = match obj.get("key_present").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "flag_invalid"));
            return (SourcePolicy::default(), lines);
        }
    };
    let arr = match obj.get("restricted").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "restricted_not_array"));
            return (SourcePolicy::default(), lines);
        }
    };
    let mut restricted: Vec<RestrictedEntry> = Vec::new();
    for (i, item) in arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if entry_keys_ok(e) => e,
            _ => {
                lines.push(degrade("entry", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("entry", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let imported = match entry.get("imported") {
            None => false,
            Some(v) => match v.as_bool() {
                Some(b) => b,
                None => {
                    lines.push(degrade("entry", &format!("index={} bad_imported", i)));
                    continue;
                }
            },
        };
        if restricted.iter().any(|e| e.id == id) {
            lines.push(degrade("entry", &format!("index={} duplicate_id", i)));
            continue;
        }
        restricted.push(RestrictedEntry { id, imported });
    }
    if restricted.len() > MAX_RESTRICTED {
        let excess = restricted.len() - MAX_RESTRICTED;
        restricted.truncate(MAX_RESTRICTED);
        lines.push(degrade("entry", &format!("overflow={}", excess)));
    }
    (SourcePolicy { tier, max_concurrent, restricted_auto, restricted, key_present }, lines)
}

fn serialize(policy: &SourcePolicy) -> Result<String> {
    let entries: Vec<Value> = policy
        .restricted
        .iter()
        .map(|e| json!({"id": e.id, "imported": e.imported}))
        .collect();
    Ok(to_string(&json!({
        "schema": 1,
        "tier": policy.tier.code(),
        "max_concurrent": policy.max_concurrent,
        "restricted_auto": policy.restricted_auto,
        "restricted": entries,
        "key_present": policy.key_present,
    }))?)
}

fn write(root: &Path, policy: &SourcePolicy) -> Result<()> {
    let body = serialize(policy)?;
    let path = robust::safe_join(root, SOURCES_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", SOURCES_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl SourcePolicy {
    pub fn open(root: Option<&Path>) -> (SourcePolicy, Vec<String>) {
        let Some(dir) = root else {
            return (SourcePolicy::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, SOURCES_FILE) {
            Ok(p) => p,
            Err(_) => return (SourcePolicy::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_SOURCES);
        if missing {
            return (SourcePolicy::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (SourcePolicy::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn effective_plan(&self) -> (Vec<SourceKind>, Vec<String>) {
        let mut lines = Vec::new();
        let tier = if !self.key_present && self.tier != SourceTier::AutoMirror {
            lines.push(degrade("plan", "key_absent_downgrade_mirror"));
            SourceTier::AutoMirror
        } else {
            self.tier
        };
        let plan = match tier {
            SourceTier::AutoMirror => vec![SourceKind::Mirror, SourceKind::Official],
            SourceTier::OfficialFirst => vec![SourceKind::Official, SourceKind::Mirror],
            SourceTier::OriginalOnly => vec![SourceKind::Original],
        };
        (plan, lines)
    }

    pub fn can_auto_download(&self) -> bool {
        self.restricted_auto
    }

    pub fn add_restricted(&mut self, id: &str) -> bool {
        if !valid_id(id) || self.restricted.len() >= MAX_RESTRICTED {
            return false;
        }
        if self.restricted.iter().any(|e| e.id == id) {
            return false;
        }
        self.restricted.push(RestrictedEntry { id: id.to_string(), imported: false });
        true
    }

    pub fn mark_imported(&mut self, id: &str) -> bool {
        match self.restricted.iter_mut().find(|e| e.id == id) {
            Some(e) => {
                e.imported = true;
                true
            }
            None => false,
        }
    }

    pub fn pending(&self) -> Vec<&str> {
        self.restricted.iter().filter(|e| !e.imported).map(|e| e.id.as_str()).collect()
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        Envelope::new(Kind::Event, SOURCES_TARGET)
            .with("tier", self.tier.code())
            .with("restricted_auto", if self.restricted_auto { "true" } else { "false" })
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    SourcePolicy::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu069-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn tier_and_kind_codes_are_explicit() {
        assert_eq!(SourceTier::AutoMirror.code(), "auto_mirror");
        assert_eq!(SourceTier::OfficialFirst.code(), "official_first");
        assert_eq!(SourceTier::OriginalOnly.code(), "original_only");
        assert_eq!(SourceTier::parse("nope"), None);
        assert_eq!(SourceKind::Mirror.code(), "mirror");
        assert_eq!(KNOWN_KEYS.len(), 6);
    }

    #[test]
    fn default_is_auto_mirror_without_key_and_without_auto_download() {
        let (p, lines) = SourcePolicy::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p.tier, SourceTier::AutoMirror);
        assert_eq!(p.max_concurrent, DEFAULT_CONCURRENT);
        assert!(!p.restricted_auto);
        assert!(!p.key_present);
        assert!(p.restricted.is_empty());
        assert!(!p.can_auto_download());
        let (plan, dl) = p.effective_plan();
        assert!(dl.is_empty());
        assert_eq!(plan, vec![SourceKind::Mirror, SourceKind::Official]);
    }

    #[test]
    fn eight_bad_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(SOURCES_FILE);
        let cases = [
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            r#"{"schema":1,"tier":"auto_mirror","max_concurrent":3,"restricted_auto":false,"restricted":[],"key_present":false,"extra":1}"#.to_string(),
            r#"{"schema":1,"tier":"bad","max_concurrent":3,"restricted_auto":false,"restricted":[],"key_present":false}"#.to_string(),
            r#"{"schema":1,"tier":"auto_mirror","max_concurrent":0,"restricted_auto":false,"restricted":[],"key_present":false}"#.to_string(),
            r#"{"schema":1,"tier":"auto_mirror","max_concurrent":3,"restricted_auto":"no","restricted":[],"key_present":false}"#.to_string(),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (p, lines) = SourcePolicy::open(Some(&r));
            assert_eq!(p, SourcePolicy::default(), "case={}", &raw[..raw.len().min(24)]);
            assert!(lines.iter().any(|l| l.contains("DEGRADE")), "case={}", &raw[..raw.len().min(24)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_restricted_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"tier":"auto_mirror","max_concurrent":3,"restricted_auto":false,"restricted":[{"id":"a","imported":true},7,{"id":"","imported":false},{"id":"a","imported":false},{"id":"b","imported":"no"}],"key_present":false}"#;
        fs::write(r.join(SOURCES_FILE), raw).unwrap();
        let (p, lines) = SourcePolicy::open(Some(&r));
        assert_eq!(p.restricted.len(), 1);
        assert_eq!(p.restricted[0].id, "a");
        assert!(p.restricted[0].imported);
        assert!(lines.iter().any(|l| l.contains("bad_shape")));
        assert!(lines.iter().any(|l| l.contains("bad_id")));
        assert!(lines.iter().any(|l| l.contains("duplicate_id")));
        assert!(lines.iter().any(|l| l.contains("bad_imported")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn key_absence_downgrades_non_mirror_tiers() {
        let mut p = SourcePolicy::default();
        p.tier = SourceTier::OfficialFirst;
        let (plan, lines) = p.effective_plan();
        assert_eq!(plan, vec![SourceKind::Mirror, SourceKind::Official]);
        assert!(lines.iter().any(|x| x.contains("key_absent_downgrade_mirror")));
        p.tier = SourceTier::OriginalOnly;
        let (plan2, lines2) = p.effective_plan();
        assert_eq!(plan2, vec![SourceKind::Mirror, SourceKind::Official]);
        assert!(lines2.iter().any(|x| x.contains("key_absent_downgrade_mirror")));
        p.key_present = true;
        p.tier = SourceTier::OfficialFirst;
        assert_eq!(p.effective_plan().0, vec![SourceKind::Official, SourceKind::Mirror]);
        p.tier = SourceTier::OriginalOnly;
        assert_eq!(p.effective_plan().0, vec![SourceKind::Original]);
    }

    #[test]
    fn restricted_list_is_bounded_and_pending_tracks_import() {
        let mut p = SourcePolicy::default();
        assert!(p.add_restricted("mod-a"));
        assert!(p.add_restricted("mod-b"));
        assert!(!p.add_restricted("mod-a"));
        assert!(!p.add_restricted(""));
        assert_eq!(p.pending(), vec!["mod-a", "mod-b"]);
        assert!(p.mark_imported("mod-a"));
        assert!(!p.mark_imported("missing"));
        assert_eq!(p.pending(), vec!["mod-b"]);
        for i in 0..(MAX_RESTRICTED + 5) {
            p.add_restricted(&format!("f{}", i));
        }
        assert_eq!(p.restricted.len(), MAX_RESTRICTED);
    }

    #[test]
    fn persist_survives_reopen_and_reset_keeps_protected_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let mut p = SourcePolicy::default();
        p.tier = SourceTier::OfficialFirst;
        p.key_present = true;
        p.max_concurrent = 8;
        p.restricted_auto = true;
        p.add_restricted("mod-x");
        assert!(p.persist(Some(&r)).is_empty());
        let (back, lines) = SourcePolicy::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.tier, SourceTier::OfficialFirst);
        assert_eq!(back.max_concurrent, 8);
        assert!(back.key_present);
        assert!(back.restricted_auto);
        assert_eq!(back.restricted.len(), 1);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = SourcePolicy::open(Some(&r));
        assert_eq!(def, SourcePolicy::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut p = SourcePolicy::default();
        p.add_restricted("m");
        assert!(p.persist(None)[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn change_event_uses_unified_envelope() {
        let mut p = SourcePolicy::default();
        p.tier = SourceTier::OfficialFirst;
        p.restricted_auto = true;
        let e = p.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, SOURCES_TARGET);
        assert_eq!(e.field("tier"), Some("official_first"));
        assert_eq!(e.field("restricted_auto"), Some("true"));
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 2);
    }

    #[test]
    fn serialize_never_carries_key_value() {
        let mut p = SourcePolicy::default();
        p.key_present = true;
        let s = serialize(&p).unwrap();
        assert!(s.contains("\"key_present\":true"));
        assert!(!s.contains("CurseForge"));
        assert!(!s.contains("token"));
        let v: Value = from_str(&s).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 6);
    }

    #[test]
    fn concurrent_bounds_reject_zero_and_overflow() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for n in ["0", "65", "-1", "not_a_number"] {
            let raw = format!(r#"{{"schema":1,"tier":"auto_mirror","max_concurrent":{},"restricted_auto":false,"restricted":[],"key_present":false}}"#, if n.starts_with('"') { n.to_string() } else { format!("\"{}\"", n) });
            fs::write(r.join(SOURCES_FILE), &raw).unwrap();
            let (p, lines) = SourcePolicy::open(Some(&r));
            assert_eq!(p, SourcePolicy::default(), "n={}", n);
            assert!(lines.iter().any(|l| l.contains("concurrent_invalid")), "n={}", n);
        }
        let _ = fs::remove_dir_all(&r);
    }
}

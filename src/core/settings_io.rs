use crate::core::boot::{BUNDLE_FILE, STATE_FILE};
use crate::core::config::Config;
use crate::core::consent::CONSENT_FILE;
use crate::core::diagnostics::diag_line;
use crate::core::robust;
use crate::core::stats::STATS_FILE;
use anyhow::{anyhow, Result};
use serde_json::{from_str, to_string, Map, Value};
use std::fs;
use std::path::Path;

pub const SETTINGS_FILE: &str = "launch.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const MAX_IMPORT_BYTES: usize = 64 * 1024;
pub const MAX_ROOT_KEYS: usize = 64;
pub const MAX_ENDPOINTS: usize = 64;
pub const MAX_PORTS: usize = 64;
pub const MAX_VALUE_BYTES: usize = 4096;

pub const PROTECTED_FILES: &[&str] = &[CONSENT_FILE, STATE_FILE, BUNDLE_FILE, STATS_FILE];
pub const KNOWN_KEYS: &[&str] = &[
    "os_class",
    "language",
    "mirror_speedtest",
    "endpoints",
    "ports",
    "download_region",
];
pub const DERIVED_KEYS: &[&str] = &["os_class"];

pub struct ImportReport {
    pub config: Option<Config>,
    pub accepted: Vec<String>,
    pub rejected: Vec<String>,
    pub lines: Vec<String>,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CleanupReport {
    pub reset: bool,
    pub protected: Vec<String>,
    pub lines: Vec<String>,
}

pub fn is_protected(name: &str) -> bool {
    PROTECTED_FILES.contains(&name)
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("settings", action, "import", "DEGRADE", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn validate_key_value(key: &str, value: &Value) -> std::result::Result<(), String> {
    if !KNOWN_KEYS.contains(&key) {
        return Err("unknown_key".to_string());
    }
    match key {
        "os_class" | "language" | "download_region" => {
            let Some(s) = value.as_str() else { return Err("type_string".to_string()) };
            if s.len() > MAX_VALUE_BYTES { return Err("too_long".to_string()) }
            if has_control(s) { return Err("control_char".to_string()) }
        }
        "mirror_speedtest" => {
            if !value.is_boolean() { return Err("type_bool".to_string()) }
        }
        "endpoints" | "ports" => {
            let Some(m) = value.as_object() else { return Err("type_object".to_string()) };
            let cap = if key == "endpoints" { MAX_ENDPOINTS } else { MAX_PORTS };
            if m.len() > cap { return Err("too_many_entries".to_string()) }
            for (k, v) in m {
                if k.len() > MAX_VALUE_BYTES || has_control(k) {
                    return Err("bad_entry_key".to_string())
                }
                if key == "endpoints" {
                    let Some(s) = v.as_str() else { return Err("bad_endpoint_value".to_string()) };
                    if s.len() > MAX_VALUE_BYTES || has_control(s) {
                        return Err("bad_endpoint_value".to_string())
                    }
                } else if v.as_u64().and_then(|n| u16::try_from(n).ok()).is_none() {
                    return Err("bad_port_value".to_string())
                }
            }
        }
        _ => return Err("unknown_key".to_string()),
    }
    Ok(())
}

pub fn import(raw: &str) -> ImportReport {
    let mut report = ImportReport { config: None, accepted: Vec::new(), rejected: Vec::new(), lines: Vec::new() };
    if raw.is_empty() {
        report.lines.push(degrade("parse", "empty"));
        return report;
    }
    if raw.len() > MAX_IMPORT_BYTES {
        report.lines.push(degrade("parse", "too_large"));
        return report;
    }
    let Ok(v) = from_str::<Value>(raw) else {
        report.lines.push(degrade("parse", "not_json"));
        return report;
    };
    let Some(root) = v.as_object() else {
        report.lines.push(degrade("parse", "root_not_object"));
        return report;
    };
    if root.len() > MAX_ROOT_KEYS {
        report.lines.push(degrade("parse", "too_many_keys"));
        return report;
    }
    let mut clean = Map::new();
    for (key, value) in root {
        match validate_key_value(key, value) {
            Ok(()) => {
                clean.insert(key.clone(), value.clone());
                report.accepted.push(key.clone());
            }
            Err(reason) => {
                report.rejected.push(key.clone());
                report.lines.push(degrade("key", &format!("{}={}", key, reason)));
            }
        }
    }
    let Ok(text) = to_string(&Value::Object(clean)) else {
        report.lines.push(diag_line("settings", "serialize", "import", "ERROR", "json"));
        return report;
    };
    match Config::from_json_str(&text) {
        Ok(c) => report.config = Some(c),
        Err(e) => report.lines.push(diag_line("settings", "build", "import", "ERROR", &e.to_string())),
    }
    report
}

pub fn export_diff(config: &Config) -> Result<String> {
    let current: Map<String, Value> = from_str(&config.to_json_string()?)?;
    let base: Map<String, Value> = from_str(&Config::empty(&config.os_class).to_json_string()?)?;
    let mut diff = Map::new();
    for (key, value) in &current {
        if DERIVED_KEYS.contains(&key.as_str()) {
            continue;
        }
        if base.get(key) != Some(value) {
            diff.insert(key.clone(), value.clone());
        }
    }
    Ok(to_string(&Value::Object(diff))?)
}

pub fn atomic_write(root: &Path, body: &str) -> Result<()> {
    let path = robust::safe_join(root, SETTINGS_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", SETTINGS_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

pub fn cleanup(root: Option<&Path>, current: Option<&Config>) -> CleanupReport {
    let mut report = CleanupReport { reset: false, protected: Vec::new(), lines: Vec::new() };
    for name in PROTECTED_FILES {
        if is_protected(name) {
            report.protected.push((*name).to_string());
        }
    }
    let Some(dir) = root else {
        report.lines.push(diag_line("settings", "cleanup", "reset", "ERROR", "no_root"));
        return report;
    };
    let os_class = current.map(|c| c.os_class.as_str()).unwrap_or("");
    let body = match Config::empty(os_class).to_json_string() {
        Ok(s) => s,
        Err(e) => {
            report.lines.push(diag_line("settings", "cleanup", "default", "ERROR", &e.to_string()));
            return report;
        }
    };
    match atomic_write(dir, &body) {
        Ok(()) => {
            report.reset = true;
            report.lines.push(diag_line("settings", "cleanup", "reset", "OK", "protected_kept"));
        }
        Err(e) => report.lines.push(diag_line("settings", "cleanup", "reset", "ERROR", &e.to_string())),
    }
    report
}

pub fn reject_protected_removal(name: &str) -> Result<()> {
    if is_protected(name) {
        return Err(anyhow!("protected file"));
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu065-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn export_only_non_default_keys() {
        let mut c = Config::empty("windows");
        let d = export_diff(&c).unwrap();
        assert_eq!(d, "{}");
        c.language = "en-US".to_string();
        c.set_endpoint("download/java", "mirror-a");
        let v: Value = from_str(&export_diff(&c).unwrap()).unwrap();
        let m = v.as_object().unwrap();
        assert_eq!(m.get("language").unwrap(), "en-US");
        assert!(m.get("endpoints").is_some());
        assert!(m.get("os_class").is_none());
        assert!(m.get("mirror_speedtest").is_none());
    }

    #[test]
    fn os_class_is_derived_not_exported() {
        let c = Config::empty("linux");
        assert!(!export_diff(&c).unwrap().contains("os_class"));
    }

    #[test]
    fn eight_bad_inputs_are_visible_and_non_panicking() {
        let cases = [
            "",
            "not json",
            "[]",
            &"x".repeat(MAX_IMPORT_BYTES + 1),
            r#"{"language":7}"#,
            r#"{"mirror_speedtest":"yes"}"#,
            r#"{"endpoints":[]}"#,
            r#"{"ports":{"ai/local":"x"}}"#,
        ];
        for raw in cases {
            let r = import(raw);
            assert!(r.config.is_none() || !r.rejected.is_empty(), "case={}", &raw[..raw.len().min(20)]);
            assert!(r.lines.iter().any(|l| l.contains("DEGRADE")), "case={}", &raw[..raw.len().min(20)]);
        }
    }

    #[test]
    fn unknown_key_is_rejected_not_silently_dropped() {
        let r = import(r#"{"language":"en-US","evil_key":1}"#);
        assert!(r.accepted.contains(&"language".to_string()));
        assert!(r.rejected.contains(&"evil_key".to_string()));
        assert!(r.lines.iter().any(|l| l.contains("unknown_key")));
        assert!(r.config.is_some());
    }

    #[test]
    fn control_char_in_value_is_rejected() {
        let r = import("{\"language\":\"en\\u0000US\"}");
        assert!(r.rejected.contains(&"language".to_string()));
        assert!(r.lines.iter().any(|l| l.contains("control_char")));
    }

    #[test]
    fn endpoint_value_is_not_parsed_as_url() {
        let r = import(r#"{"endpoints":{"download/java":"java-source-a"}}"#);
        assert!(r.config.is_some());
        assert!(r.rejected.is_empty());
        assert_eq!(r.config.unwrap().endpoint("download/java"), Some("java-source-a"));
    }

    #[test]
    fn cleanup_never_removes_consent_or_state_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let c = Config::empty("windows");
        let report = cleanup(Some(&r), Some(&c));
        assert!(report.reset);
        assert_eq!(report.protected.len(), 4);
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        assert!(r.join(SETTINGS_FILE).is_file());
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn protected_removal_is_rejected() {
        assert!(reject_protected_removal(CONSENT_FILE).is_err());
        assert!(reject_protected_removal(STATE_FILE).is_err());
        assert!(reject_protected_removal(BUNDLE_FILE).is_err());
        assert!(reject_protected_removal(STATS_FILE).is_err());
        assert!(reject_protected_removal("other.json").is_ok());
    }

    #[test]
    fn settings_file_is_not_in_protected_set() {
        assert!(!is_protected(SETTINGS_FILE));
        assert!(!PROTECTED_FILES.contains(&SETTINGS_FILE));
    }

    #[test]
    fn atomic_write_leaves_no_tmp() {
        let r = tmp();
        atomic_write(&r, "{}").unwrap();
        assert!(r.join(SETTINGS_FILE).is_file());
        assert!(!r.join(format!("{}{}", SETTINGS_FILE, TMP_SUFFIX)).exists());
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn no_root_cleanup_is_error_not_panic() {
        let report = cleanup(None, None);
        assert!(!report.reset);
        assert_eq!(report.protected.len(), 4);
        assert!(report.lines[0].contains("ERROR"));
    }

    #[test]
    fn cleanup_preserves_os_class_without_hardcoded_default() {
        let r = tmp();
        let c = Config::empty("linux");
        cleanup(Some(&r), Some(&c)).reset.then_some(()).unwrap();
        let body = fs::read_to_string(r.join(SETTINGS_FILE)).unwrap();
        assert!(body.contains("linux"));
        let _ = fs::remove_dir_all(&r);
    }
}

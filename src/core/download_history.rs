use crate::core::diagnostics::diag_line;
use crate::core::robust;
use anyhow::{anyhow, Result};
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const HISTORY_FILE: &str = "download-history.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_ENTRIES: usize = 256;
pub const MAX_KEY_BYTES: usize = 256;
pub const MAX_VALUE_BYTES: usize = 4096;
pub const DEFAULT_HISTORY: &str = r#"{"schema":1,"entries":[]}"#;
pub const KINDS: &[&str] = &["game", "mod", "modpack", "resourcepack", "shaderpack", "datapack"];
pub const RESULTS: &[&str] = &["ok", "failed", "cancelled"];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DownloadRecord {
    pub key: String,
    pub kind: String,
    pub at: u64,
    pub result: String,
}

pub struct DownloadHistory {
    entries: Vec<DownloadRecord>,
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("download", action, "history", "DEGRADE", reason)
}

fn error(action: &str, reason: &str) -> String {
    diag_line("download", action, "history", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn parse_entry(v: &Value) -> Option<DownloadRecord> {
    let o = v.as_object()?;
    if o.len() != 4 {
        return None;
    }
    let key = o.get("key")?.as_str()?.to_string();
    let kind = o.get("kind")?.as_str()?.to_string();
    let at = o.get("at")?.as_u64()?;
    let result = o.get("result")?.as_str()?.to_string();
    if key.is_empty() || key.len() > MAX_KEY_BYTES || has_control(&key) {
        return None;
    }
    if !KINDS.contains(&kind.as_str()) || kind.len() > MAX_VALUE_BYTES || has_control(&kind) {
        return None;
    }
    if !RESULTS.contains(&result.as_str()) || result.len() > MAX_VALUE_BYTES || has_control(&result) {
        return None;
    }
    Some(DownloadRecord { key, kind, at, result })
}

fn write_default(root: &Path) -> Result<()> {
    let path = robust::safe_join(root, HISTORY_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", HISTORY_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, DEFAULT_HISTORY)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

fn write_all(root: &Path, entries: &[DownloadRecord]) -> Result<()> {
    let list: Vec<Value> = entries
        .iter()
        .map(|e| json!({"key": e.key, "kind": e.kind, "at": e.at, "result": e.result}))
        .collect();
    let body = to_string(&json!({"schema": 1, "entries": list}))?;
    let path = robust::safe_join(root, HISTORY_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", HISTORY_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl DownloadHistory {
    pub fn open(root: Option<&Path>) -> (DownloadHistory, Vec<String>) {
        let mut history = DownloadHistory { entries: Vec::new() };
        let Some(dir) = root else {
            return (history, vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, HISTORY_FILE) {
            Ok(p) => p,
            Err(_) => return (history, vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_HISTORY);
        if missing {
            return (history, vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (history, vec![degrade("load", "too_large")]);
        }
        let value: Value = match from_str(&raw) {
            Ok(v) => v,
            Err(_) => return (history, vec![degrade("load", "not_json")]),
        };
        let root_obj = match value.as_object() {
            Some(o) => o,
            None => return (history, vec![degrade("load", "root_not_object")]),
        };
        if root_obj.get("schema").and_then(Value::as_u64) != Some(1) {
            return (history, vec![degrade("load", "schema_invalid")]);
        }
        let arr = match root_obj.get("entries").and_then(Value::as_array) {
            Some(a) => a,
            None => return (history, vec![degrade("load", "entries_not_array")]),
        };
        let mut lines = Vec::new();
        for (i, entry) in arr.iter().enumerate() {
            match parse_entry(entry) {
                Some(r) => history.entries.push(r),
                None => lines.push(degrade("entry", &format!("index={} rejected", i))),
            }
        }
        if history.entries.len() > MAX_ENTRIES {
            let excess = history.entries.len() - MAX_ENTRIES;
            history.entries.truncate(MAX_ENTRIES);
            lines.push(degrade("entry", &format!("overflow={}", excess)));
        }
        (history, lines)
    }

    pub fn record(&mut self, root: Option<&Path>, key: &str, kind: &str, at: u64, result: &str) -> Vec<String> {
        if key.is_empty() || key.len() > MAX_KEY_BYTES || has_control(key) {
            return vec![degrade("record", "bad_key")];
        }
        if !KINDS.contains(&kind) || kind.len() > MAX_VALUE_BYTES || has_control(kind) {
            return vec![degrade("record", "bad_kind")];
        }
        if !RESULTS.contains(&result) || result.len() > MAX_VALUE_BYTES || has_control(result) {
            return vec![degrade("record", "bad_result")];
        }
        let mut found = false;
        for e in &mut self.entries {
            if e.key == key && e.kind == kind {
                e.at = at;
                e.result = result.to_string();
                found = true;
                break;
            }
        }
        if !found {
            self.entries.push(DownloadRecord {
                key: key.to_string(),
                kind: kind.to_string(),
                at,
                result: result.to_string(),
            });
        }
        if self.entries.len() > MAX_ENTRIES {
            let excess = self.entries.len() - MAX_ENTRIES;
            self.entries.drain(0..excess);
        }
        match self.save(root) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error("record", &e.to_string())],
        }
    }

    fn save(&self, root: Option<&Path>) -> Result<()> {
        let dir = root.ok_or_else(|| anyhow!("no_root"))?;
        write_all(dir, &self.entries)
    }

    pub fn query(&self, kind: Option<&str>, limit: usize) -> Vec<&DownloadRecord> {
        if limit == 0 {
            return Vec::new();
        }
        let mut rows: Vec<&DownloadRecord> = self
            .entries
            .iter()
            .filter(|e| match kind {
                Some(k) => e.kind == k,
                None => true,
            })
            .collect();
        rows.sort_by(|a, b| b.at.cmp(&a.at));
        rows.truncate(limit);
        rows
    }

    pub fn len(&self) -> usize {
        self.entries.len()
    }

    pub fn is_empty(&self) -> bool {
        self.entries.is_empty()
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    let Some(dir) = root else {
        return vec![error("reset", "no_root")];
    };
    match write_default(dir) {
        Ok(()) => Vec::new(),
        Err(e) => vec![error("reset", &e.to_string())],
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu066-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn constants_are_bounded_and_closed() {
        assert_eq!(KINDS.len(), 6);
        assert_eq!(RESULTS.len(), 3);
        assert!(KINDS.contains(&"mod"));
        assert!(RESULTS.contains(&"ok"));
        assert_eq!(MAX_ENTRIES, 256);
        assert_eq!(HISTORY_FILE, "download-history.json");
    }

    #[test]
    fn missing_file_uses_default_with_visible_line() {
        let r = tmp();
        let (h, lines) = DownloadHistory::open(Some(&r));
        assert!(h.is_empty());
        assert!(lines[0].contains("DEGRADE"));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn eight_bad_inputs_degrade_without_panic() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(HISTORY_FILE);
        let cases = [
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            r#"{"schema":2,"entries":[]}"#.to_string(),
            r#"{"schema":1,"entries":"oops"}"#.to_string(),
            r#"{"schema":1,"entries":[{"key":"a","kind":"mod","at":1,"result":"ok","extra":1}]}"#.to_string(),
            r#"{"schema":1,"entries":[{"key":"a","kind":"mod","at":"x","result":"ok"}]}"#.to_string(),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (h, lines) = DownloadHistory::open(Some(&r));
            assert!(h.is_empty(), "case={}", &raw[..raw.len().min(20)]);
            assert!(lines.iter().any(|l| l.contains("DEGRADE")), "case={}", &raw[..raw.len().min(20)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn invalid_kind_and_result_entries_are_rejected() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        fs::write(
            r.join(HISTORY_FILE),
            r#"{"schema":1,"entries":[{"key":"a","kind":"evil","at":1,"result":"ok"},{"key":"b","kind":"mod","at":1,"result":"maybe"}]}"#,
        ).unwrap();
        let (h, lines) = DownloadHistory::open(Some(&r));
        assert!(h.is_empty());
        assert_eq!(lines.len(), 2);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn control_char_in_key_is_rejected() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        fs::write(r.join(HISTORY_FILE), "{\"schema\":1,\"entries\":[{\"key\":\"a\\u0000b\",\"kind\":\"mod\",\"at\":1,\"result\":\"ok\"}]}").unwrap();
        let (h, lines) = DownloadHistory::open(Some(&r));
        assert!(h.is_empty());
        assert!(lines.iter().any(|l| l.contains("DEGRADE")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn record_deduplicates_same_key_and_kind() {
        let r = tmp();
        let (mut h, _) = DownloadHistory::open(Some(&r));
        h.record(Some(&r), "sodium", "mod", 100, "ok");
        h.record(Some(&r), "sodium", "mod", 200, "failed");
        assert_eq!(h.len(), 1);
        let (back, lines) = DownloadHistory::open(Some(&r));
        assert_eq!(back.len(), 1);
        assert!(lines.is_empty());
        assert_eq!(back.query(None, 1)[0].result, "failed");
        assert_eq!(back.query(None, 1)[0].at, 200);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn different_kind_keeps_two_rows() {
        let r = tmp();
        let (mut h, _) = DownloadHistory::open(Some(&r));
        h.record(Some(&r), "pack", "modpack", 1, "ok");
        h.record(Some(&r), "pack", "resourcepack", 2, "ok");
        assert_eq!(h.len(), 2);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_record_arguments_do_not_write() {
        let r = tmp();
        let (mut h, _) = DownloadHistory::open(Some(&r));
        assert!(h.record(Some(&r), "", "mod", 1, "ok")[0].contains("DEGRADE"));
        assert!(h.record(Some(&r), "a", "evil", 1, "ok")[0].contains("DEGRADE"));
        assert!(h.record(Some(&r), "a", "mod", 1, "maybe")[0].contains("DEGRADE"));
        assert!(h.is_empty());
        assert!(!r.join(HISTORY_FILE).exists());
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn overflow_evicts_oldest_and_stays_bounded() {
        let r = tmp();
        let (mut h, _) = DownloadHistory::open(Some(&r));
        for i in 0..(MAX_ENTRIES + 10) {
            h.record(Some(&r), &format!("k{}", i), "mod", i as u64, "ok");
        }
        assert_eq!(h.len(), MAX_ENTRIES);
        let (back, _) = DownloadHistory::open(Some(&r));
        assert_eq!(back.len(), MAX_ENTRIES);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn query_filters_orders_and_limits() {
        let r = tmp();
        let (mut h, _) = DownloadHistory::open(Some(&r));
        h.record(Some(&r), "a", "mod", 10, "ok");
        h.record(Some(&r), "b", "shaderpack", 30, "ok");
        h.record(Some(&r), "c", "mod", 20, "failed");
        assert_eq!(h.query(Some("mod"), 10).len(), 2);
        assert_eq!(h.query(Some("mod"), 10)[0].key, "c");
        assert_eq!(h.query(None, 0).len(), 0);
        assert_eq!(h.query(None, 2)[0].key, "b");
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn reset_keeps_protected_files_and_clears_history() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let (mut h, _) = DownloadHistory::open(Some(&r));
        h.record(Some(&r), "a", "mod", 1, "ok");
        assert_eq!(h.len(), 1);
        let lines = reset(Some(&r));
        assert!(lines.is_empty());
        let (back, _) = DownloadHistory::open(Some(&r));
        assert!(back.is_empty());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn no_root_is_error_not_panic() {
        let (mut h, lines) = DownloadHistory::open(None);
        assert!(h.is_empty());
        assert!(lines[0].contains("DEGRADE"));
        let out = h.record(None, "a", "mod", 1, "ok");
        assert!(out[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn atomic_write_leaves_no_tmp() {
        let r = tmp();
        let (mut h, _) = DownloadHistory::open(Some(&r));
        h.record(Some(&r), "a", "mod", 1, "ok");
        assert!(r.join(HISTORY_FILE).is_file());
        assert!(!r.join(format!("{}{}", HISTORY_FILE, TMP_SUFFIX)).exists());
        let _ = fs::remove_dir_all(&r);
    }
}

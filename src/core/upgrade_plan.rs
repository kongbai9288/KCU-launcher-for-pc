use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const UPGRADE_PLAN_FILE: &str = "upgrade-plan.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"page_size":5,"choices":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_CHOICES: usize = 24;
pub const MAX_PAGE_SIZE: usize = 10;
pub const MIN_PAGE_SIZE: usize = 1;
pub const DEFAULT_PAGE_SIZE: usize = 5;
pub const UPGRADE_TARGET: &str = "upgrade.plan";
pub const KNOWN_KEYS: &[&str] = &["schema", "page_size", "choices"];
pub const CHOICE_KEYS: &[&str] = &["id", "current", "candidate", "compat", "mode", "confirmed"];
pub const COMPATS: &[&str] = &["compatible", "conflict", "unknown"];
pub const MODES: &[&str] = &["defer", "direct", "clone"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Compat {
    Compatible,
    Conflict,
    Unknown,
}

impl Compat {
    pub fn code(&self) -> &'static str {
        match self {
            Compat::Compatible => "compatible",
            Compat::Conflict => "conflict",
            Compat::Unknown => "unknown",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "compatible" => Some(Compat::Compatible),
            "conflict" => Some(Compat::Conflict),
            "unknown" => Some(Compat::Unknown),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UpgradeMode {
    Defer,
    Direct,
    Clone,
}

impl UpgradeMode {
    pub fn code(&self) -> &'static str {
        match self {
            UpgradeMode::Defer => "defer",
            UpgradeMode::Direct => "direct",
            UpgradeMode::Clone => "clone",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "defer" => Some(UpgradeMode::Defer),
            "direct" => Some(UpgradeMode::Direct),
            "clone" => Some(UpgradeMode::Clone),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UpgradeChoice {
    pub id: String,
    pub current: String,
    pub candidate: String,
    pub compat: Compat,
    pub mode: UpgradeMode,
    pub confirmed: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UpgradePlan {
    pub page_size: usize,
    pub choices: Vec<UpgradeChoice>,
}

impl Default for UpgradePlan {
    fn default() -> Self {
        UpgradePlan { page_size: DEFAULT_PAGE_SIZE, choices: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("upgrade", action, "plan", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("upgrade", action, "plan", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_text(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_ID_BYTES && !has_control(s)
}

fn choice_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| CHOICE_KEYS.contains(&k.as_str()))
}

fn parse(raw: &str) -> (UpgradePlan, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (UpgradePlan::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (UpgradePlan::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (UpgradePlan::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (UpgradePlan::default(), lines);
    }
    let page_size = match obj.get("page_size").and_then(Value::as_u64) {
        Some(v) if v >= MIN_PAGE_SIZE as u64 && v <= MAX_PAGE_SIZE as u64 => v as usize,
        _ => {
            lines.push(degrade("load", "page_size_invalid"));
            return (UpgradePlan::default(), lines);
        }
    };
    let arr = match obj.get("choices").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "choices_not_array"));
            return (UpgradePlan::default(), lines);
        }
    };
    let mut choices: Vec<UpgradeChoice> = Vec::new();
    for (i, item) in arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if choice_keys_ok(e) => e,
            _ => {
                lines.push(degrade("choice", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("choice", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let current = match entry.get("current").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("choice", &format!("index={} bad_current", i)));
                continue;
            }
        };
        let candidate = match entry.get("candidate").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("choice", &format!("index={} bad_candidate", i)));
                continue;
            }
        };
        let compat = match entry.get("compat").and_then(Value::as_str).and_then(Compat::parse) {
            Some(c) => c,
            None => {
                lines.push(degrade("choice", &format!("index={} bad_compat", i)));
                continue;
            }
        };
        let mode = match entry.get("mode").and_then(Value::as_str).and_then(UpgradeMode::parse) {
            Some(m) => m,
            None => {
                lines.push(degrade("choice", &format!("index={} bad_mode", i)));
                continue;
            }
        };
        let confirmed = match entry.get("confirmed").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("choice", &format!("index={} bad_confirmed", i)));
                continue;
            }
        };
        if (confirmed && mode == UpgradeMode::Defer) || (confirmed && compat == Compat::Conflict) {
            lines.push(degrade("choice", &format!("index={} bad_state_pair", i)));
            continue;
        }
        if choices.iter().any(|c| c.id == id) {
            lines.push(degrade("choice", &format!("index={} duplicate_id", i)));
            continue;
        }
        choices.push(UpgradeChoice { id, current, candidate, compat, mode, confirmed });
    }
    if choices.len() > MAX_CHOICES {
        let excess = choices.len() - MAX_CHOICES;
        choices.truncate(MAX_CHOICES);
        lines.push(degrade("choice", &format!("overflow={}", excess)));
    }
    (UpgradePlan { page_size, choices }, lines)
}

fn serialize(p: &UpgradePlan) -> Result<String> {
    let choices: Vec<Value> = p
        .choices
        .iter()
        .map(|c| json!({"id": c.id, "current": c.current, "candidate": c.candidate,
                        "compat": c.compat.code(), "mode": c.mode.code(), "confirmed": c.confirmed}))
        .collect();
    Ok(to_string(&json!({
        "schema": 1,
        "page_size": p.page_size,
        "choices": choices,
    }))?)
}

fn write(root: &Path, p: &UpgradePlan) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, UPGRADE_PLAN_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", UPGRADE_PLAN_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl UpgradePlan {
    pub fn open(root: Option<&Path>) -> (UpgradePlan, Vec<String>) {
        let Some(dir) = root else {
            return (UpgradePlan::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, UPGRADE_PLAN_FILE) {
            Ok(p) => p,
            Err(_) => return (UpgradePlan::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (UpgradePlan::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (UpgradePlan::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn add_choice(&mut self, id: &str, current: &str, candidate: &str, compat: Compat) -> bool {
        if !valid_text(id) || !valid_text(current) || !valid_text(candidate) {
            return false;
        }
        if self.choices.len() >= MAX_CHOICES || self.choices.iter().any(|c| c.id == id) {
            return false;
        }
        self.choices.push(UpgradeChoice {
            id: id.to_string(),
            current: current.to_string(),
            candidate: candidate.to_string(),
            compat,
            mode: UpgradeMode::Defer,
            confirmed: false,
        });
        true
    }

    pub fn remove_choice(&mut self, id: &str) -> bool {
        let before = self.choices.len();
        self.choices.retain(|c| c.id != id);
        self.choices.len() != before
    }

    pub fn set_compat(&mut self, id: &str, compat: Compat) -> bool {
        let Some(c) = self.choices.iter_mut().find(|c| c.id == id) else {
            return false;
        };
        c.compat = compat;
        if c.compat == Compat::Conflict {
            c.mode = UpgradeMode::Defer;
            c.confirmed = false;
        }
        true
    }

    pub fn set_mode(&mut self, id: &str, mode: UpgradeMode) -> bool {
        let Some(c) = self.choices.iter_mut().find(|c| c.id == id) else {
            return false;
        };
        c.mode = mode;
        if c.mode == UpgradeMode::Defer {
            c.confirmed = false;
        }
        true
    }

    pub fn confirm(&mut self, id: &str) -> bool {
        let Some(c) = self.choices.iter_mut().find(|c| c.id == id) else {
            return false;
        };
        if c.mode == UpgradeMode::Defer {
            return false;
        }
        c.confirmed = true;
        true
    }

    pub fn revoke(&mut self, id: &str) -> bool {
        let Some(c) = self.choices.iter_mut().find(|c| c.id == id) else {
            return false;
        };
        c.confirmed = false;
        true
    }

    pub fn set_page_size(&mut self, size: usize) -> bool {
        if size < MIN_PAGE_SIZE || size > MAX_PAGE_SIZE {
            return false;
        }
        self.page_size = size;
        true
    }

    pub fn page_count(&self) -> usize {
        if self.choices.is_empty() {
            return 0;
        }
        (self.choices.len() + self.page_size - 1) / self.page_size
    }

    pub fn page_items(&self, page: usize) -> &[UpgradeChoice] {
        if page >= self.page_count() || self.choices.is_empty() {
            return &[];
        }
        let start = page * self.page_size;
        let end = (start + self.page_size).min(self.choices.len());
        &self.choices[start..end]
    }

    pub fn pending_count(&self) -> usize {
        self.choices.iter().filter(|c| !c.confirmed).count()
    }

    pub fn ready_count(&self) -> usize {
        self.choices
            .iter()
            .filter(|c| c.confirmed && c.mode != UpgradeMode::Defer && c.compat != Compat::Conflict)
            .count()
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        Envelope::new(Kind::Event, UPGRADE_TARGET)
            .with("choices", &self.choices.len().to_string())
            .with("pending", &self.pending_count().to_string())
            .with("ready", &self.ready_count().to_string())
            .with("pages", &self.page_count().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    UpgradePlan::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu076-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"page_size":5,"choices":[]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 3);
    }

    #[test]
    fn enum_codes_and_tables_are_explicit() {
        assert_eq!(Compat::Compatible.code(), "compatible");
        assert_eq!(Compat::Conflict.code(), "conflict");
        assert_eq!(Compat::Unknown.code(), "unknown");
        assert_eq!(Compat::parse("nope"), None);
        assert_eq!(UpgradeMode::Defer.code(), "defer");
        assert_eq!(UpgradeMode::Direct.code(), "direct");
        assert_eq!(UpgradeMode::Clone.code(), "clone");
        assert_eq!(UpgradeMode::parse("nope"), None);
        assert_eq!(KNOWN_KEYS.len(), 3);
        assert_eq!(CHOICE_KEYS.len(), 6);
        assert_eq!(COMPATS.len(), 3);
        assert_eq!(MODES.len(), 3);
        assert_eq!(MAX_CHOICES, 24);
        assert_eq!(MAX_PAGE_SIZE, 10);
        assert_eq!(DEFAULT_PAGE_SIZE, 5);
    }

    #[test]
    fn default_is_empty_with_page_size() {
        let (p, lines) = UpgradePlan::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, UpgradePlan::default());
        assert_eq!(p.page_size, DEFAULT_PAGE_SIZE);
        assert!(p.choices.is_empty());
        assert_eq!(p.page_count(), 0);
        assert_eq!(p.page_items(0).len(), 0);
        assert_eq!(p.pending_count(), 0);
        assert_eq!(p.ready_count(), 0);
    }

    #[test]
    fn bad_root_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(UPGRADE_PLAN_FILE);
        let base = r#"{"schema":1,"page_size":5,"choices":[]}"#;
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            base.replace("\"choices\":[]", "\"choices\":[],\"extra\":1"),
            base.replace("\"schema\":1", "\"schema\":2"),
            base.replace("\"page_size\":5", "\"page_size\":0"),
            base.replace("\"page_size\":5", "\"page_size\":99"),
            base.replace("\"page_size\":5", "\"page_size\":\"no\""),
            base.replace("\"choices\":[]", "\"choices\":\"no\""),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (p, lines) = UpgradePlan::open(Some(&r));
            assert_eq!(p, UpgradePlan::default(), "case={}", &raw[..raw.len().min(28)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(28)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_choice_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"page_size":3,"choices":[{"id":"a","current":"1.0","candidate":"2.0","compat":"compatible","mode":"direct","confirmed":true},7,{"id":"","current":"1","candidate":"2","compat":"compatible","mode":"defer","confirmed":false},{"id":"b","current":"1","candidate":"","compat":"compatible","mode":"defer","confirmed":false},{"id":"c","current":"1","candidate":"2","compat":"nope","mode":"defer","confirmed":false},{"id":"d","current":"1","candidate":"2","compat":"compatible","mode":"nope","confirmed":false},{"id":"e","current":"1","candidate":"2","compat":"compatible","mode":"defer","confirmed":"no"},{"id":"f","current":"1","candidate":"2","compat":"compatible","mode":"defer","confirmed":false,"z":1},{"id":"a","current":"1","candidate":"2","compat":"unknown","mode":"clone","confirmed":false}]}"#;
        fs::write(r.join(UPGRADE_PLAN_FILE), raw).unwrap();
        let (p, lines) = UpgradePlan::open(Some(&r));
        assert_eq!(p.page_size, 3);
        assert_eq!(p.choices.len(), 1);
        assert_eq!(p.choices[0].id, "a");
        assert_eq!(p.choices[0].compat, Compat::Compatible);
        assert_eq!(p.choices[0].mode, UpgradeMode::Direct);
        assert!(p.choices[0].confirmed);
        assert!(lines.iter().any(|x| x.contains("bad_shape")));
        assert!(lines.iter().any(|x| x.contains("bad_id")));
        assert!(lines.iter().any(|x| x.contains("bad_candidate")));
        assert!(lines.iter().any(|x| x.contains("bad_compat")));
        assert!(lines.iter().any(|x| x.contains("bad_mode")));
        assert!(lines.iter().any(|x| x.contains("bad_confirmed")));
        assert!(lines.iter().any(|x| x.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn conflict_and_defer_pairs_are_rejected() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"page_size":5,"choices":[{"id":"a","current":"1","candidate":"2","compat":"compatible","mode":"defer","confirmed":true},{"id":"b","current":"1","candidate":"2","compat":"conflict","mode":"direct","confirmed":true}]}"#;
        fs::write(r.join(UPGRADE_PLAN_FILE), raw).unwrap();
        let (p, lines) = UpgradePlan::open(Some(&r));
        assert!(p.choices.is_empty());
        assert_eq!(lines.iter().filter(|x| x.contains("bad_state_pair")).count(), 2);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn add_remove_and_bound() {
        let mut p = UpgradePlan::default();
        assert!(p.add_choice("m1", "1.0", "2.0", Compat::Compatible));
        assert!(p.add_choice("m2", "1.0", "2.0", Compat::Unknown));
        assert!(!p.add_choice("m1", "1.0", "2.0", Compat::Compatible));
        assert!(!p.add_choice("", "1", "2", Compat::Compatible));
        assert!(!p.add_choice("bad\nid", "1", "2", Compat::Compatible));
        assert!(!p.add_choice("x", "", "2", Compat::Compatible));
        assert!(!p.add_choice("y", "1", "", Compat::Compatible));
        assert!(p.remove_choice("m1"));
        assert!(!p.remove_choice("missing"));
        assert_eq!(p.choices.len(), 1);
        for i in 0..(MAX_CHOICES + 5) {
            p.add_choice(&format!("w{}", i), "1", "2", Compat::Unknown);
        }
        assert_eq!(p.choices.len(), MAX_CHOICES);
    }

    #[test]
    fn single_choice_confirm_and_revoke() {
        let mut p = UpgradePlan::default();
        p.add_choice("a", "1", "2", Compat::Compatible);
        p.add_choice("b", "1", "2", Compat::Compatible);
        assert!(!p.confirm("a"));
        assert!(!p.confirm("missing"));
        assert!(p.set_mode("a", UpgradeMode::Direct));
        assert!(p.confirm("a"));
        assert_eq!(p.ready_count(), 1);
        assert_eq!(p.pending_count(), 1);
        assert!(p.set_mode("b", UpgradeMode::Clone));
        assert_eq!(p.pending_count(), 1);
        assert!(p.choices[0].confirmed);
        assert!(!p.choices[1].confirmed);
        assert!(p.confirm("b"));
        assert_eq!(p.ready_count(), 2);
        assert!(p.revoke("a"));
        assert_eq!(p.ready_count(), 1);
        assert!(!p.revoke("missing"));
        assert!(p.set_mode("a", UpgradeMode::Defer));
        assert!(!p.choices[0].confirmed);
    }

    #[test]
    fn defer_confirm_is_refused() {
        let mut p = UpgradePlan::default();
        p.add_choice("a", "1", "2", Compat::Compatible);
        assert_eq!(p.choices[0].mode, UpgradeMode::Defer);
        assert!(!p.confirm("a"));
        assert_eq!(p.ready_count(), 0);
    }

    #[test]
    fn set_compat_conflict_resets_decision() {
        let mut p = UpgradePlan::default();
        p.add_choice("a", "1", "2", Compat::Compatible);
        assert!(p.set_mode("a", UpgradeMode::Direct));
        assert!(p.confirm("a"));
        assert_eq!(p.ready_count(), 1);
        assert!(p.set_compat("a", Compat::Conflict));
        assert_eq!(p.choices[0].mode, UpgradeMode::Defer);
        assert!(!p.choices[0].confirmed);
        assert_eq!(p.ready_count(), 0);
        assert!(!p.confirm("a"));
        assert!(!p.set_compat("missing", Compat::Conflict));
    }

    #[test]
    fn page_count_and_page_items_are_derived() {
        let mut p = UpgradePlan::default();
        for i in 0..7 {
            p.add_choice(&format!("m{}", i), "1", "2", Compat::Unknown);
        }
        assert_eq!(p.page_size, 5);
        assert_eq!(p.page_count(), 2);
        assert_eq!(p.page_items(0).len(), 5);
        assert_eq!(p.page_items(1).len(), 2);
        assert_eq!(p.page_items(2).len(), 0);
        assert!(p.set_page_size(3));
        assert_eq!(p.page_count(), 3);
        assert_eq!(p.page_items(2).len(), 1);
        assert!(!p.set_page_size(0));
        assert!(!p.set_page_size(MAX_PAGE_SIZE + 1));
        assert_eq!(p.page_size, 3);
        let mut empty = UpgradePlan::default();
        empty.set_page_size(2);
        assert_eq!(empty.page_count(), 0);
        assert_eq!(empty.page_items(0).len(), 0);
    }

    #[test]
    fn bounded_overflow_from_disk() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let mut body = String::from(r#"{"schema":1,"page_size":5,"choices":["#);
        for i in 0..(MAX_CHOICES + 3) {
            if i > 0 { body.push(','); }
            body.push_str(&format!(r#"{{"id":"q{}","current":"1","candidate":"2","compat":"unknown","mode":"defer","confirmed":false}}"#, i));
        }
        body.push_str("]}");
        fs::write(r.join(UPGRADE_PLAN_FILE), body).unwrap();
        let (p, lines) = UpgradePlan::open(Some(&r));
        assert_eq!(p.choices.len(), MAX_CHOICES);
        assert!(lines.iter().any(|x| x.contains("overflow=3")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut p = UpgradePlan::default();
        p.add_choice("a", "1", "2", Compat::Compatible);
        assert!(p.persist(None)[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn persist_reopen_reset_keep_protected_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let mut p = UpgradePlan::default();
        p.add_choice("a", "1", "2", Compat::Compatible);
        p.add_choice("b", "1", "2", Compat::Unknown);
        assert!(p.set_page_size(4));
        assert!(p.set_mode("a", UpgradeMode::Clone));
        assert!(p.confirm("a"));
        assert!(p.set_compat("b", Compat::Conflict));
        assert!(p.persist(Some(&r)).is_empty());
        let (back, lines) = UpgradePlan::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.page_size, 4);
        assert_eq!(back.choices.len(), 2);
        assert_eq!(back.choices[0].mode, UpgradeMode::Clone);
        assert!(back.choices[0].confirmed);
        assert_eq!(back.choices[1].compat, Compat::Conflict);
        assert_eq!(back.ready_count(), 1);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = UpgradePlan::open(Some(&r));
        assert_eq!(def, UpgradePlan::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope_without_ids() {
        let mut p = UpgradePlan::default();
        p.add_choice("a", "1", "2", Compat::Compatible);
        p.add_choice("b", "1", "2", Compat::Unknown);
        p.add_choice("c", "1", "2", Compat::Unknown);
        assert!(p.set_mode("a", UpgradeMode::Direct));
        assert!(p.confirm("a"));
        let e = p.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, UPGRADE_TARGET);
        assert_eq!(e.field("choices"), Some("3"));
        assert_eq!(e.field("pending"), Some("2"));
        assert_eq!(e.field("ready"), Some("1"));
        assert_eq!(e.field("pages"), Some("1"));
        assert_eq!(e.field("ids"), None);
        assert_eq!(e.field("versions"), None);
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 4);
    }

    #[test]
    fn serialize_carries_no_choice_table() {
        let mut p = UpgradePlan::default();
        p.add_choice("a", "1", "2", Compat::Compatible);
        let raw = serialize(&p).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 3);
        assert!(!raw.contains("CHOICE_TABLE"));
        assert!(!raw.contains("VERSION_TABLE"));
        assert!(!raw.contains("cmp_precedence"));
        assert!(!raw.contains("semver"));
    }
}

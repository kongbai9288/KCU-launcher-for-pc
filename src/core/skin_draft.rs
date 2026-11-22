use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const SKIN_DRAFT_FILE: &str = "skin-draft.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"active":null,"leave_warn":true,"drafts":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_DRAFTS: usize = 12;
pub const MAX_INTERVAL: u64 = 3600;
pub const SKIN_TARGET: &str = "skin.draft";
pub const KNOWN_KEYS: &[&str] = &["schema", "active", "leave_warn", "drafts"];
pub const DRAFT_KEYS: &[&str] = &["id", "kind", "state", "interval"];
pub const KINDS: &[&str] = &["saved", "original"];
pub const DRAFT_STATES: &[&str] = &["clean", "dirty"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SkinKind {
    Saved,
    Original,
}

impl SkinKind {
    pub fn code(&self) -> &'static str {
        match self {
            SkinKind::Saved => "saved",
            SkinKind::Original => "original",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "saved" => Some(SkinKind::Saved),
            "original" => Some(SkinKind::Original),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DraftState {
    Clean,
    Dirty,
}

impl DraftState {
    pub fn code(&self) -> &'static str {
        match self {
            DraftState::Clean => "clean",
            DraftState::Dirty => "dirty",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "clean" => Some(DraftState::Clean),
            "dirty" => Some(DraftState::Dirty),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SkinDraft {
    pub id: String,
    pub kind: SkinKind,
    pub state: DraftState,
    pub interval: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SkinWorkspace {
    pub active: Option<String>,
    pub leave_warn: bool,
    pub drafts: Vec<SkinDraft>,
}

impl Default for SkinWorkspace {
    fn default() -> Self {
        SkinWorkspace { active: None, leave_warn: true, drafts: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("skin", action, "draft", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("skin", action, "draft", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_ID_BYTES && !has_control(s)
}

fn draft_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| DRAFT_KEYS.contains(&k.as_str()))
}

fn parse(raw: &str) -> (SkinWorkspace, Vec<String>) {
    let mut lines = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (SkinWorkspace::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (SkinWorkspace::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (SkinWorkspace::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (SkinWorkspace::default(), lines);
    }
    let active: Option<String> = match obj.get("active") {
        Some(Value::Null) => None,
        Some(Value::String(s)) if valid_id(s) => Some(s.clone()),
        _ => {
            lines.push(degrade("load", "active_invalid"));
            return (SkinWorkspace::default(), lines);
        }
    };
    let leave_warn = match obj.get("leave_warn").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "leave_warn_not_bool"));
            return (SkinWorkspace::default(), lines);
        }
    };
    let arr = match obj.get("drafts").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "drafts_not_array"));
            return (SkinWorkspace::default(), lines);
        }
    };
    let mut drafts: Vec<SkinDraft> = Vec::new();
    for (i, item) in arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if draft_keys_ok(e) => e,
            _ => {
                lines.push(degrade("draft", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("draft", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let kind = match entry.get("kind").and_then(Value::as_str).and_then(SkinKind::parse) {
            Some(k) => k,
            None => {
                lines.push(degrade("draft", &format!("index={} bad_kind", i)));
                continue;
            }
        };
        let state = match entry.get("state").and_then(Value::as_str).and_then(DraftState::parse) {
            Some(s) => s,
            None => {
                lines.push(degrade("draft", &format!("index={} bad_state", i)));
                continue;
            }
        };
        let interval = match entry.get("interval").and_then(Value::as_u64) {
            Some(v) if v <= MAX_INTERVAL => v,
            _ => {
                lines.push(degrade("draft", &format!("index={} bad_interval", i)));
                continue;
            }
        };
        if drafts.iter().any(|d| d.id == id) {
            lines.push(degrade("draft", &format!("index={} duplicate_id", i)));
            continue;
        }
        drafts.push(SkinDraft { id, kind, state, interval });
    }
    if drafts.len() > MAX_DRAFTS {
        let excess = drafts.len() - MAX_DRAFTS;
        drafts.truncate(MAX_DRAFTS);
        lines.push(degrade("draft", &format!("overflow={}", excess)));
    }
    if let Some(id) = &active {
        if !drafts.iter().any(|d| &d.id == id) {
            lines.push(degrade("load", "active_dangling"));
            return (SkinWorkspace::default(), lines);
        }
    }
    (SkinWorkspace { active, leave_warn, drafts }, lines)
}

fn serialize(w: &SkinWorkspace) -> Result<String> {
    let drafts: Vec<Value> = w
        .drafts
        .iter()
        .map(|d| json!({"id": d.id, "kind": d.kind.code(), "state": d.state.code(), "interval": d.interval}))
        .collect();
    let active = match &w.active {
        Some(s) => Value::String(s.clone()),
        None => Value::Null,
    };
    Ok(to_string(&json!({
        "schema": 1,
        "active": active,
        "leave_warn": w.leave_warn,
        "drafts": drafts,
    }))?)
}

fn write(root: &Path, w: &SkinWorkspace) -> Result<()> {
    let body = serialize(w)?;
    let path = robust::safe_join(root, SKIN_DRAFT_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", SKIN_DRAFT_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl SkinWorkspace {
    pub fn open(root: Option<&Path>) -> (SkinWorkspace, Vec<String>) {
        let Some(dir) = root else {
            return (SkinWorkspace::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, SKIN_DRAFT_FILE) {
            Ok(p) => p,
            Err(_) => return (SkinWorkspace::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (SkinWorkspace::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (SkinWorkspace::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn add_draft(&mut self, id: &str, kind: SkinKind) -> bool {
        if !valid_id(id) || self.drafts.len() >= MAX_DRAFTS || self.drafts.iter().any(|d| d.id == id) {
            return false;
        }
        self.drafts.push(SkinDraft { id: id.to_string(), kind, state: DraftState::Clean, interval: 0 });
        true
    }

    pub fn remove_draft(&mut self, id: &str) -> bool {
        let before = self.drafts.len();
        self.drafts.retain(|d| d.id != id);
        if self.drafts.len() == before {
            return false;
        }
        if self.active.as_deref() == Some(id) {
            self.active = None;
        }
        true
    }

    pub fn set_active(&mut self, id: &str) -> bool {
        if !self.drafts.iter().any(|d| d.id == id) {
            return false;
        }
        self.active = Some(id.to_string());
        true
    }

    pub fn clear_active(&mut self) {
        self.active = None;
    }

    pub fn mark_dirty(&mut self, id: &str) -> bool {
        let Some(d) = self.drafts.iter_mut().find(|d| d.id == id) else {
            return false;
        };
        d.state = DraftState::Dirty;
        true
    }

    pub fn mark_clean(&mut self, id: &str) -> bool {
        let Some(d) = self.drafts.iter_mut().find(|d| d.id == id) else {
            return false;
        };
        d.state = DraftState::Clean;
        true
    }

    pub fn set_kind(&mut self, id: &str, kind: SkinKind) -> bool {
        let Some(d) = self.drafts.iter_mut().find(|d| d.id == id) else {
            return false;
        };
        d.kind = kind;
        true
    }

    pub fn set_interval(&mut self, id: &str, secs: u64) -> bool {
        if secs > MAX_INTERVAL {
            return false;
        }
        let Some(d) = self.drafts.iter_mut().find(|d| d.id == id) else {
            return false;
        };
        d.interval = secs;
        true
    }

    pub fn set_leave_warn(&mut self, on: bool) {
        self.leave_warn = on;
    }

    pub fn drafts_by_kind(&self, kind: SkinKind) -> usize {
        self.drafts.iter().filter(|d| d.kind == kind).count()
    }

    pub fn dirty_count(&self) -> usize {
        self.drafts.iter().filter(|d| d.state == DraftState::Dirty).count()
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        Envelope::new(Kind::Event, SKIN_TARGET)
            .with("active", if self.active.is_some() { "1" } else { "0" })
            .with("drafts", &self.drafts.len().to_string())
            .with("dirty", &self.dirty_count().to_string())
            .with("leave_warn", &self.leave_warn.to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    SkinWorkspace::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu075-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"active":null,"leave_warn":true,"drafts":[]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 4);
    }

    #[test]
    fn enum_codes_and_tables_are_explicit() {
        assert_eq!(SkinKind::Saved.code(), "saved");
        assert_eq!(SkinKind::Original.code(), "original");
        assert_eq!(SkinKind::parse("nope"), None);
        assert_eq!(DraftState::Clean.code(), "clean");
        assert_eq!(DraftState::Dirty.code(), "dirty");
        assert_eq!(DraftState::parse("nope"), None);
        assert_eq!(KNOWN_KEYS.len(), 4);
        assert_eq!(DRAFT_KEYS.len(), 4);
        assert_eq!(KINDS.len(), 2);
        assert_eq!(DRAFT_STATES.len(), 2);
        assert_eq!(MAX_DRAFTS, 12);
        assert_eq!(MAX_INTERVAL, 3600);
    }

    #[test]
    fn default_is_empty_with_warn_on() {
        let (w, lines) = SkinWorkspace::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(w, SkinWorkspace::default());
        assert_eq!(w.active, None);
        assert!(w.leave_warn);
        assert!(w.drafts.is_empty());
        assert_eq!(w.dirty_count(), 0);
    }

    #[test]
    fn nine_bad_root_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(SKIN_DRAFT_FILE);
        let base = r#"{"schema":1,"active":null,"leave_warn":true,"drafts":[]}"#;
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            base.replace("\"drafts\":[]", "\"drafts\":[],\"extra\":1"),
            base.replace("\"schema\":1", "\"schema\":2"),
            base.replace("\"active\":null", "\"active\":7"),
            base.replace("\"leave_warn\":true", "\"leave_warn\":\"no\""),
            base.replace("\"drafts\":[]", "\"drafts\":\"no\""),
            r#"{"schema":1,"active":"ghost","leave_warn":true,"drafts":[]}"#.to_string(),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (w, lines) = SkinWorkspace::open(Some(&r));
            assert_eq!(w, SkinWorkspace::default(), "case={}", &raw[..raw.len().min(28)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(28)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_draft_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"active":"a","leave_warn":false,"drafts":[{"id":"a","kind":"saved","state":"clean","interval":0},7,{"id":"","kind":"saved","state":"clean","interval":0},{"id":"b","kind":"nope","state":"clean","interval":0},{"id":"c","kind":"saved","state":"nope","interval":0},{"id":"d","kind":"saved","state":"clean","interval":99999},{"id":"e","kind":"saved","state":"clean","interval":0,"z":1},{"id":"a","kind":"original","state":"dirty","interval":5}]}"#;
        fs::write(r.join(SKIN_DRAFT_FILE), raw).unwrap();
        let (w, lines) = SkinWorkspace::open(Some(&r));
        assert!(!w.leave_warn);
        assert_eq!(w.active, Some("a".to_string()));
        assert_eq!(w.drafts.len(), 1);
        assert_eq!(w.drafts[0].id, "a");
        assert_eq!(w.drafts[0].kind, SkinKind::Saved);
        assert_eq!(w.drafts[0].state, DraftState::Clean);
        assert!(lines.iter().any(|x| x.contains("bad_shape")));
        assert!(lines.iter().any(|x| x.contains("bad_id")));
        assert!(lines.iter().any(|x| x.contains("bad_kind")));
        assert!(lines.iter().any(|x| x.contains("bad_state")));
        assert!(lines.iter().any(|x| x.contains("bad_interval")));
        assert!(lines.iter().any(|x| x.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn dangling_active_is_rejected() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"active":"ghost","leave_warn":true,"drafts":[{"id":"a","kind":"saved","state":"clean","interval":0}]}"#;
        fs::write(r.join(SKIN_DRAFT_FILE), raw).unwrap();
        let (w, lines) = SkinWorkspace::open(Some(&r));
        assert_eq!(w, SkinWorkspace::default());
        assert!(lines.iter().any(|x| x.contains("active_dangling")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn add_remove_and_bound() {
        let mut w = SkinWorkspace::default();
        assert!(w.add_draft("s1", SkinKind::Saved));
        assert!(w.add_draft("s2", SkinKind::Original));
        assert!(!w.add_draft("s1", SkinKind::Saved));
        assert!(!w.add_draft("", SkinKind::Saved));
        assert!(!w.add_draft("bad\nid", SkinKind::Saved));
        assert!(w.remove_draft("s1"));
        assert!(!w.remove_draft("missing"));
        assert_eq!(w.drafts.len(), 1);
        for i in 0..(MAX_DRAFTS + 5) {
            w.add_draft(&format!("w{}", i), SkinKind::Saved);
        }
        assert_eq!(w.drafts.len(), MAX_DRAFTS);
    }

    #[test]
    fn active_dirty_kind_and_interval() {
        let mut w = SkinWorkspace::default();
        w.add_draft("a", SkinKind::Saved);
        w.add_draft("b", SkinKind::Original);
        assert!(!w.set_active("missing"));
        assert!(w.set_active("b"));
        assert_eq!(w.active, Some("b".to_string()));
        assert!(w.mark_dirty("a"));
        assert!(!w.mark_dirty("missing"));
        assert_eq!(w.dirty_count(), 1);
        assert!(w.mark_clean("a"));
        assert_eq!(w.dirty_count(), 0);
        assert!(w.set_kind("a", SkinKind::Original));
        assert_eq!(w.drafts_by_kind(SkinKind::Original), 2);
        assert_eq!(w.drafts_by_kind(SkinKind::Saved), 0);
        assert!(w.set_interval("a", MAX_INTERVAL));
        assert_eq!(w.drafts[0].interval, MAX_INTERVAL);
        assert!(!w.set_interval("a", MAX_INTERVAL + 1));
        assert_eq!(w.drafts[0].interval, MAX_INTERVAL);
        assert!(!w.set_interval("missing", 5));
        w.clear_active();
        assert_eq!(w.active, None);
    }

    #[test]
    fn removing_active_clears_it() {
        let mut w = SkinWorkspace::default();
        w.add_draft("a", SkinKind::Saved);
        w.add_draft("b", SkinKind::Original);
        assert!(w.set_active("a"));
        assert!(w.remove_draft("a"));
        assert_eq!(w.active, None);
        assert_eq!(w.drafts.len(), 1);
        w.set_leave_warn(false);
        assert!(!w.leave_warn);
    }

    #[test]
    fn bounded_overflow_from_disk() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let mut body = String::from(r#"{"schema":1,"active":null,"leave_warn":true,"drafts":["#);
        for i in 0..(MAX_DRAFTS + 3) {
            if i > 0 { body.push(','); }
            body.push_str(&format!(r#"{{"id":"q{}","kind":"saved","state":"clean","interval":0}}"#, i));
        }
        body.push_str("]}");
        fs::write(r.join(SKIN_DRAFT_FILE), body).unwrap();
        let (w, lines) = SkinWorkspace::open(Some(&r));
        assert_eq!(w.drafts.len(), MAX_DRAFTS);
        assert!(lines.iter().any(|x| x.contains("overflow=3")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut w = SkinWorkspace::default();
        w.add_draft("a", SkinKind::Saved);
        assert!(w.persist(None)[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn persist_reopen_reset_keep_protected_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let mut w = SkinWorkspace::default();
        w.add_draft("a", SkinKind::Saved);
        w.add_draft("b", SkinKind::Original);
        assert!(w.set_active("b"));
        assert!(w.mark_dirty("a"));
        assert!(w.set_interval("a", 120));
        w.set_leave_warn(false);
        assert!(w.persist(Some(&r)).is_empty());
        let (back, lines) = SkinWorkspace::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.active, Some("b".to_string()));
        assert!(!back.leave_warn);
        assert_eq!(back.drafts.len(), 2);
        assert_eq!(back.drafts[0].state, DraftState::Dirty);
        assert_eq!(back.drafts[0].interval, 120);
        assert_eq!(back.drafts[1].kind, SkinKind::Original);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = SkinWorkspace::open(Some(&r));
        assert_eq!(def, SkinWorkspace::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn active_null_roundtrip() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"active":null,"leave_warn":true,"drafts":[]}"#;
        fs::write(r.join(SKIN_DRAFT_FILE), raw).unwrap();
        let (w, lines) = SkinWorkspace::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(w.active, None);
        assert!(w.persist(Some(&r)).is_empty());
        let text = fs::read_to_string(r.join(SKIN_DRAFT_FILE)).unwrap();
        assert!(text.contains("\"active\":null"));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope_without_ids() {
        let mut w = SkinWorkspace::default();
        w.add_draft("a", SkinKind::Saved);
        w.add_draft("b", SkinKind::Original);
        assert!(w.set_active("b"));
        assert!(w.mark_dirty("a"));
        let e = w.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, SKIN_TARGET);
        assert_eq!(e.field("active"), Some("1"));
        assert_eq!(e.field("drafts"), Some("2"));
        assert_eq!(e.field("dirty"), Some("1"));
        assert_eq!(e.field("leave_warn"), Some("true"));
        assert_eq!(e.field("ids"), None);
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 4);
    }

    #[test]
    fn serialize_carries_no_skin_table() {
        let mut w = SkinWorkspace::default();
        w.add_draft("a", SkinKind::Saved);
        let raw = serialize(&w).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 4);
        assert!(!raw.contains("SKIN_TABLE"));
        assert!(!raw.contains("texture"));
        assert!(!raw.contains("png"));
        assert!(!raw.contains("uuid"));
    }
}

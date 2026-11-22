use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const NOTICE_CENTER_FILE: &str = "notice-center.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"entries":[{"id":"declaration","category":"declaration","read":"unread","action":"later","closable":true,"detail":true,"builtin":true}]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_ENTRIES: usize = 24;
pub const EVENT_TARGET: &str = "notice.center";
pub const BUILTIN_ID: &str = "declaration";
pub const KNOWN_KEYS: &[&str] = &["schema", "entries"];
pub const ENTRY_KEYS: &[&str] = &["id", "category", "read", "action", "closable", "detail", "builtin"];
pub const CATEGORIES: &[&str] = &["update", "maintenance", "activity", "declaration"];
pub const READ_STATES: &[&str] = &["unread", "read"];
pub const ACTIONS: &[&str] = &["never", "later", "ack"];
pub const CLOSE_PATHS: &[&str] = &["button", "escape", "cancel"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum NoticeCategory {
    Update,
    Maintenance,
    Activity,
    Declaration,
}

impl NoticeCategory {
    pub fn code(&self) -> &'static str {
        match self {
            NoticeCategory::Update => "update",
            NoticeCategory::Maintenance => "maintenance",
            NoticeCategory::Activity => "activity",
            NoticeCategory::Declaration => "declaration",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "update" => Some(NoticeCategory::Update),
            "maintenance" => Some(NoticeCategory::Maintenance),
            "activity" => Some(NoticeCategory::Activity),
            "declaration" => Some(NoticeCategory::Declaration),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ReadState {
    Unread,
    Read,
}

impl ReadState {
    pub fn code(&self) -> &'static str {
        match self {
            ReadState::Unread => "unread",
            ReadState::Read => "read",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "unread" => Some(ReadState::Unread),
            "read" => Some(ReadState::Read),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum NoticeAction {
    Never,
    Later,
    Ack,
}

impl NoticeAction {
    pub fn code(&self) -> &'static str {
        match self {
            NoticeAction::Never => "never",
            NoticeAction::Later => "later",
            NoticeAction::Ack => "ack",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "never" => Some(NoticeAction::Never),
            "later" => Some(NoticeAction::Later),
            "ack" => Some(NoticeAction::Ack),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClosePath {
    Button,
    Escape,
    Cancel,
}

impl ClosePath {
    pub fn code(&self) -> &'static str {
        match self {
            ClosePath::Button => "button",
            ClosePath::Escape => "escape",
            ClosePath::Cancel => "cancel",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "button" => Some(ClosePath::Button),
            "escape" => Some(ClosePath::Escape),
            "cancel" => Some(ClosePath::Cancel),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NoticeEntry {
    pub id: String,
    pub category: NoticeCategory,
    pub read: ReadState,
    pub action: NoticeAction,
    pub closable: bool,
    pub detail: bool,
    pub builtin: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct NoticeCenter {
    pub entries: Vec<NoticeEntry>,
}

impl Default for NoticeCenter {
    fn default() -> Self {
        NoticeCenter {
            entries: vec![NoticeEntry {
                id: BUILTIN_ID.to_string(),
                category: NoticeCategory::Declaration,
                read: ReadState::Unread,
                action: NoticeAction::Later,
                closable: true,
                detail: true,
                builtin: true,
            }],
        }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("notice", action, "center", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("notice", action, "center", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_TEXT_BYTES && !has_control(s)
}

fn entry_consistent(e: &NoticeEntry) -> bool {
    if e.action == NoticeAction::Never && e.read == ReadState::Unread {
        return false;
    }
    if !e.closable && e.action == NoticeAction::Later {
        return false;
    }
    if e.builtin && e.id != BUILTIN_ID {
        return false;
    }
    true
}

fn parse(raw: &str) -> (NoticeCenter, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (NoticeCenter::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (NoticeCenter::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (NoticeCenter::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (NoticeCenter::default(), lines);
    }
    let arr = match obj.get("entries").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "entries_not_array"));
            return (NoticeCenter::default(), lines);
        }
    };
    if arr.len() > MAX_ENTRIES {
        lines.push(degrade("load", "entries_too_many"));
        return (NoticeCenter::default(), lines);
    }
    let mut entries: Vec<NoticeEntry> = Vec::new();
    for item in arr {
        let eo = match item.as_object() {
            Some(o) => o,
            None => {
                lines.push(degrade("load", "entry_not_object"));
                return (NoticeCenter::default(), lines);
            }
        };
        if eo.keys().any(|k| !ENTRY_KEYS.contains(&k.as_str())) {
            lines.push(degrade("load", "entry_unknown_key"));
            return (NoticeCenter::default(), lines);
        }
        let id = match eo.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "id_too_large"));
                return (NoticeCenter::default(), lines);
            }
            _ => {
                lines.push(degrade("load", "bad_id"));
                return (NoticeCenter::default(), lines);
            }
        };
        if entries.iter().any(|e| e.id == id) {
            lines.push(degrade("load", "duplicate_id"));
            return (NoticeCenter::default(), lines);
        }
        let category = match eo.get("category").and_then(Value::as_str).and_then(NoticeCategory::parse) {
            Some(c) => c,
            None => {
                lines.push(degrade("load", "bad_category"));
                return (NoticeCenter::default(), lines);
            }
        };
        let read = match eo.get("read").and_then(Value::as_str).and_then(ReadState::parse) {
            Some(r) => r,
            None => {
                lines.push(degrade("load", "bad_read"));
                return (NoticeCenter::default(), lines);
            }
        };
        let action = match eo.get("action").and_then(Value::as_str).and_then(NoticeAction::parse) {
            Some(a) => a,
            None => {
                lines.push(degrade("load", "bad_action"));
                return (NoticeCenter::default(), lines);
            }
        };
        let closable = match eo.get("closable").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("load", "bad_closable"));
                return (NoticeCenter::default(), lines);
            }
        };
        let detail = match eo.get("detail").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("load", "bad_detail"));
                return (NoticeCenter::default(), lines);
            }
        };
        let builtin = match eo.get("builtin").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("load", "bad_builtin"));
                return (NoticeCenter::default(), lines);
            }
        };
        let e = NoticeEntry { id, category, read, action, closable, detail, builtin };
        if !entry_consistent(&e) {
            lines.push(degrade("load", "bad_entry_state"));
            return (NoticeCenter::default(), lines);
        }
        entries.push(e);
    }
    if !entries.iter().any(|e| e.builtin && e.id == BUILTIN_ID) {
        lines.push(degrade("load", "missing_builtin"));
        return (NoticeCenter::default(), lines);
    }
    if entries.iter().filter(|e| e.builtin).count() != 1 {
        lines.push(degrade("load", "duplicate_builtin"));
        return (NoticeCenter::default(), lines);
    }
    (NoticeCenter { entries }, lines)
}

fn serialize(p: &NoticeCenter) -> Result<String> {
    let items: Vec<Value> = p.entries.iter().map(|e| json!({
        "id": e.id,
        "category": e.category.code(),
        "read": e.read.code(),
        "action": e.action.code(),
        "closable": e.closable,
        "detail": e.detail,
        "builtin": e.builtin,
    })).collect();
    Ok(to_string(&json!({ "schema": 1, "entries": items }))?)
}

fn write(root: &Path, p: &NoticeCenter) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, NOTICE_CENTER_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", NOTICE_CENTER_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl NoticeCenter {
    pub fn open(root: Option<&Path>) -> (NoticeCenter, Vec<String>) {
        let Some(dir) = root else {
            return (NoticeCenter::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, NOTICE_CENTER_FILE) {
            Ok(p) => p,
            Err(_) => return (NoticeCenter::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (NoticeCenter::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (NoticeCenter::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn can_close(&self, id: &str, path: ClosePath) -> bool {
        if !CLOSE_PATHS.contains(&path.code()) {
            return false;
        }
        match self.entries.iter().find(|e| e.id == id) {
            Some(e) => e.closable,
            None => false,
        }
    }

    pub fn visible_count(&self) -> usize {
        self.entries.iter().filter(|e| e.read == ReadState::Unread && e.action != NoticeAction::Never).count()
    }

    pub fn unread_count(&self) -> usize {
        self.entries.iter().filter(|e| e.read == ReadState::Unread).count()
    }

    pub fn by_category(&self, cat: NoticeCategory) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for e in &self.entries {
            if e.category == cat {
                out.push(e.id.as_str());
            }
        }
        out
    }

    pub fn action_for(&self, id: &str) -> Option<NoticeAction> {
        self.entries.iter().find(|e| e.id == id).map(|e| e.action)
    }

    pub fn is_builtin(&self, id: &str) -> bool {
        self.entries.iter().any(|e| e.id == id && e.builtin)
    }

    pub fn detail_available(&self, id: &str) -> bool {
        self.entries.iter().any(|e| e.id == id && e.detail)
    }

    pub fn summary(&self) -> [usize; 4] {
        let mut out: [usize; 4] = [0, 0, 0, 0];
        for e in &self.entries {
            let idx = match e.category {
                NoticeCategory::Update => 0,
                NoticeCategory::Maintenance => 1,
                NoticeCategory::Activity => 2,
                NoticeCategory::Declaration => 3,
            };
            out[idx] += 1;
        }
        out
    }

    pub fn add_entry(&mut self, id: &str, category: NoticeCategory, read: ReadState, action: NoticeAction, closable: bool, detail: bool) -> bool {
        if self.entries.len() >= MAX_ENTRIES || !valid_id(id) || self.entries.iter().any(|e| e.id == id) {
            return false;
        }
        if !CATEGORIES.contains(&category.code()) || !READ_STATES.contains(&read.code()) || !ACTIONS.contains(&action.code()) {
            return false;
        }
        let e = NoticeEntry {
            id: id.to_string(),
            category,
            read,
            action,
            closable,
            detail,
            builtin: false,
        };
        if !entry_consistent(&e) {
            return false;
        }
        self.entries.push(e);
        true
    }

    pub fn set_read(&mut self, id: &str, read: ReadState) -> bool {
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.read = read;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].read = read;
        true
    }

    pub fn set_action(&mut self, id: &str, action: NoticeAction) -> bool {
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.action = action;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].action = action;
        true
    }

    pub fn set_closable(&mut self, id: &str, closable: bool) -> bool {
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.closable = closable;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].closable = closable;
        true
    }

    pub fn remove_entry(&mut self, id: &str) -> bool {
        if self.is_builtin(id) {
            return false;
        }
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        self.entries.remove(pos);
        true
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        Envelope::new(Kind::Event, EVENT_TARGET)
            .with("total", &self.entries.len().to_string())
            .with("visible", &self.visible_count().to_string())
            .with("unread", &self.unread_count().to_string())
            .with("builtin", &(self.entries.iter().filter(|e| e.builtin).count()).to_string())
            .with("categories", &CATEGORIES.len().to_string())
            .with("reads", &READ_STATES.len().to_string())
            .with("actions", &ACTIONS.len().to_string())
            .with("closes", &CLOSE_PATHS.len().to_string())
            .with("max_entries", &MAX_ENTRIES.to_string())
            .with("schema", "1")
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    NoticeCenter::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu081-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    fn load(dir: &std::path::Path, raw: &str) -> (NoticeCenter, Vec<String>) {
        fs::create_dir_all(dir).unwrap();
        fs::write(dir.join(NOTICE_CENTER_FILE), raw).unwrap();
        NoticeCenter::open(Some(dir))
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"entries":[{"id":"declaration","category":"declaration","read":"unread","action":"later","closable":true,"detail":true,"builtin":true}]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 2);
        assert_eq!(v["entries"].as_array().unwrap().len(), 1);
        assert_eq!(v["entries"][0].as_object().unwrap().len(), 7);
    }

    #[test]
    fn four_enum_codes_and_six_tables_are_explicit() {
        assert_eq!(NoticeCategory::Update.code(), "update");
        assert_eq!(NoticeCategory::Maintenance.code(), "maintenance");
        assert_eq!(NoticeCategory::Activity.code(), "activity");
        assert_eq!(NoticeCategory::Declaration.code(), "declaration");
        assert_eq!(NoticeCategory::parse("nope"), None);
        assert_eq!(ReadState::Unread.code(), "unread");
        assert_eq!(ReadState::Read.code(), "read");
        assert_eq!(ReadState::parse("nope"), None);
        assert_eq!(NoticeAction::Never.code(), "never");
        assert_eq!(NoticeAction::Later.code(), "later");
        assert_eq!(NoticeAction::Ack.code(), "ack");
        assert_eq!(NoticeAction::parse("nope"), None);
        assert_eq!(ClosePath::Button.code(), "button");
        assert_eq!(ClosePath::Escape.code(), "escape");
        assert_eq!(ClosePath::Cancel.code(), "cancel");
        assert_eq!(ClosePath::parse("nope"), None);
        assert_eq!(KNOWN_KEYS.len(), 2);
        assert_eq!(ENTRY_KEYS.len(), 7);
        assert_eq!(CATEGORIES.len(), 4);
        assert_eq!(READ_STATES.len(), 2);
        assert_eq!(ACTIONS.len(), 3);
        assert_eq!(CLOSE_PATHS.len(), 3);
        assert_eq!(BUILTIN_ID, "declaration");
    }

    #[test]
    fn default_has_one_builtin_unread_declaration() {
        let (p, lines) = NoticeCenter::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, NoticeCenter::default());
        assert_eq!(p.entries.len(), 1);
        assert!(p.is_builtin(BUILTIN_ID));
        assert_eq!(p.unread_count(), 1);
        assert_eq!(p.visible_count(), 1);
        assert_eq!(p.summary(), [0, 0, 0, 1]);
        assert!(p.can_close(BUILTIN_ID, ClosePath::Escape));
        assert!(!p.can_close("missing", ClosePath::Button));
    }

    #[test]
    fn bad_root_inputs_return_to_default() {
        let r = tmp();
        let base = DEFAULT_STATE;
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            base.replace("\"schema\":1", "\"schema\":1,\"extra\":1"),
            base.replace("\"schema\":1", "\"schema\":2"),
            base.replace("\"entries\":[{", "\"entries\":7,"),
            base.replace("\"id\":\"declaration\"", "\"id\":\"declaration\",\"extra\":1"),
            base.replace("\"id\":\"declaration\"", "\"id\":\"other\""),
            base.replace("\"category\":\"declaration\"", "\"category\":\"nope\""),
            base.replace("\"read\":\"unread\"", "\"read\":\"nope\""),
            base.replace("\"action\":\"later\"", "\"action\":\"nope\""),
            base.replace("\"closable\":true", "\"closable\":\"no\""),
            base.replace("\"detail\":true", "\"detail\":7"),
            base.replace("\"builtin\":true", "\"builtin\":\"no\""),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, NoticeCenter::default(), "case={}", &raw[..raw.len().min(48)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(48)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_entry_texts_and_capacity_are_rejected() {
        let r = tmp();
        let base = DEFAULT_STATE;
        let cases = vec![
            base.replace("\"id\":\"declaration\"", "\"id\":\"a\\nb\""),
            base.replace("\"id\":\"declaration\"", "\"id\":\"\""),
            base.replace("\"id\":\"declaration\"", &format!("\"id\":\"{}\"", "x".repeat(robust::MAX_TEXT_BYTES + 1))),
            base.replace("\"read\":\"unread\"", "\"read\":null"),
            base.replace("\"category\":\"declaration\"", "\"category\":7"),
            base.replace("\"entries\":[", &format!("\"entries\":[{}", "null,")),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, NoticeCenter::default(), "case={}", &raw[..raw.len().min(48)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(48)]);
        }
        let many = format!("{{\"schema\":1,\"entries\":[{}]}}",
            (0..MAX_ENTRIES + 1).map(|i| format!("{{\"id\":\"n{}\",\"category\":\"update\",\"read\":\"unread\",\"action\":\"later\",\"closable\":true,\"detail\":false,\"builtin\":false}}", i)).collect::<Vec<_>>().join(","));
        let (p, lines) = load(&r, &many);
        assert_eq!(p, NoticeCenter::default());
        assert!(lines.iter().any(|x| x.contains("entries_too_many")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn contradiction_states_are_rejected_on_load() {
        let r = tmp();
        let cases = vec![
            (DEFAULT_STATE.replace("\"action\":\"later\"", "\"action\":\"never\""), "never_with_unread"),
            (DEFAULT_STATE.replace("\"closable\":true", "\"closable\":false"), "unclosable_with_later"),
            (DEFAULT_STATE.replace("\"builtin\":true", "\"builtin\":false"), "missing_builtin"),
        ];
        for (raw, tag) in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, NoticeCenter::default(), "tag={}", tag);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "tag={}", tag);
        }
        let dup = format!("{{\"schema\":1,\"entries\":[{},{}]}}",
            r#"{"id":"declaration","category":"declaration","read":"unread","action":"later","closable":true,"detail":true,"builtin":true}"#,
            r#"{"id":"declaration","category":"update","read":"unread","action":"later","closable":true,"detail":false,"builtin":false}"#);
        let (p, lines) = load(&r, &dup);
        assert_eq!(p, NoticeCenter::default());
        assert!(lines.iter().any(|x| x.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn pure_queries_do_not_read_files() {
        let mut p = NoticeCenter::default();
        assert!(p.add_entry("n1", NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, true, false));
        assert!(p.add_entry("n2", NoticeCategory::Maintenance, ReadState::Read, NoticeAction::Never, true, true));
        assert_eq!(p.entries.len(), 3);
        assert_eq!(p.visible_count(), 2);
        assert_eq!(p.unread_count(), 2);
        assert_eq!(p.by_category(NoticeCategory::Update), vec!["n1"]);
        assert_eq!(p.by_category(NoticeCategory::Maintenance), vec!["n2"]);
        assert_eq!(p.by_category(NoticeCategory::Activity), Vec::<&str>::new());
        assert_eq!(p.action_for("n1"), Some(NoticeAction::Later));
        assert_eq!(p.action_for("missing"), None);
        assert!(p.is_builtin(BUILTIN_ID));
        assert!(!p.is_builtin("n1"));
        assert!(p.detail_available(BUILTIN_ID));
        assert!(!p.detail_available("n1"));
        assert_eq!(p.summary(), [1, 1, 0, 1]);
        assert!(p.can_close("n1", ClosePath::Button));
        assert!(p.can_close("n1", ClosePath::Cancel));
    }

    #[test]
    fn single_item_mutations_do_not_touch_other_fields() {
        let mut p = NoticeCenter::default();
        assert!(p.set_read(BUILTIN_ID, ReadState::Read));
        assert_eq!(p.unread_count(), 0);
        assert_eq!(p.action_for(BUILTIN_ID), Some(NoticeAction::Later));
        assert!(p.set_action(BUILTIN_ID, NoticeAction::Never));
        assert_eq!(p.visible_count(), 0);
        assert!(!p.set_read(BUILTIN_ID, ReadState::Unread));
        assert_eq!(p.action_for(BUILTIN_ID), Some(NoticeAction::Never));
        assert!(p.set_action("missing", NoticeAction::Ack) == false);
        assert_eq!(p.entries.len(), 1);
    }

    #[test]
    fn set_closable_three_way_contradiction() {
        let mut p = NoticeCenter::default();
        assert!(!p.set_closable(BUILTIN_ID, false));
        assert!(p.can_close(BUILTIN_ID, ClosePath::Escape));
        assert!(p.set_action(BUILTIN_ID, NoticeAction::Ack));
        assert!(p.set_closable(BUILTIN_ID, false));
        assert!(!p.can_close(BUILTIN_ID, ClosePath::Escape));
        assert!(!p.set_action(BUILTIN_ID, NoticeAction::Later));
        assert_eq!(p.action_for(BUILTIN_ID), Some(NoticeAction::Ack));
        assert!(p.set_closable(BUILTIN_ID, true));
        assert!(p.set_action(BUILTIN_ID, NoticeAction::Later));
    }

    #[test]
    fn add_entry_rejects_bad_inputs_and_never_unread() {
        let mut p = NoticeCenter::default();
        assert!(!p.add_entry("", NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, true, false));
        assert!(!p.add_entry("bad\nid", NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, true, false));
        assert!(!p.add_entry(BUILTIN_ID, NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, true, false));
        assert!(!p.add_entry("n1", NoticeCategory::Update, ReadState::Unread, NoticeAction::Never, true, false));
        assert!(!p.add_entry("n1", NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, false, false));
        assert!(p.add_entry("n1", NoticeCategory::Activity, ReadState::Read, NoticeAction::Ack, true, true));
        assert_eq!(p.entries.len(), 2);
        assert!(p.detail_available("n1"));
        assert_eq!(p.summary(), [0, 0, 1, 1]);
    }

    #[test]
    fn builtin_cannot_be_removed_and_reset_keeps_it() {
        let mut p = NoticeCenter::default();
        assert!(!p.remove_entry(BUILTIN_ID));
        assert!(p.add_entry("n1", NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, true, false));
        assert!(p.remove_entry("n1"));
        assert_eq!(p.entries.len(), 1);
        assert!(!p.remove_entry("missing"));
        let r = tmp();
        assert!(reset(Some(&r)).is_empty());
        let (back, lines) = NoticeCenter::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back, NoticeCenter::default());
        assert!(back.is_builtin(BUILTIN_ID));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let p = NoticeCenter::default();
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
        let mut p = NoticeCenter::default();
        assert!(p.add_entry("n1", NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, true, false));
        assert!(p.add_entry("n2", NoticeCategory::Activity, ReadState::Read, NoticeAction::Never, true, true));
        assert!(p.set_read(BUILTIN_ID, ReadState::Read));
        assert_eq!(p.summary(), [1, 0, 1, 1]);
        assert_eq!(p.visible_count(), 1);
        assert_eq!(p.unread_count(), 1);
        assert!(p.persist(Some(&r)).is_empty());
        let (back, lines) = NoticeCenter::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.entries.len(), 3);
        assert_eq!(back.action_for("n2"), Some(NoticeAction::Never));
        assert!(back.detail_available("n2"));
        assert!(back.is_builtin(BUILTIN_ID));
        assert_eq!(back.summary(), [1, 0, 1, 1]);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = NoticeCenter::open(Some(&r));
        assert_eq!(def, NoticeCenter::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope_without_user_text() {
        let mut p = NoticeCenter::default();
        p.add_entry("secret-id", NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, true, false);
        let e = p.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, EVENT_TARGET);
        assert_eq!(e.field("total"), Some("2"));
        assert_eq!(e.field("visible"), Some("2"));
        assert_eq!(e.field("unread"), Some("2"));
        assert_eq!(e.field("builtin"), Some("1"));
        assert_eq!(e.field("categories"), Some("4"));
        assert_eq!(e.field("reads"), Some("2"));
        assert_eq!(e.field("actions"), Some("3"));
        assert_eq!(e.field("closes"), Some("3"));
        assert_eq!(e.field("max_entries"), Some("24"));
        assert_eq!(e.field("schema"), Some("1"));
        assert_eq!(e.field("id"), None);
        assert_eq!(e.field("title"), None);
        assert_eq!(e.field("body"), None);
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 10);
    }

    #[test]
    fn serialize_carries_no_notice_table() {
        let mut p = NoticeCenter::default();
        p.add_entry("n1", NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, true, false);
        let raw = serialize(&p).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 2);
        assert_eq!(v["entries"][0].as_object().unwrap().len(), 7);
        assert!(!raw.contains("NOTICE_TABLE"));
        assert!(!raw.contains("CATEGORY_TABLE"));
        assert!(!raw.contains("ACTION_TABLE"));
    }

    #[test]
    fn four_tables_are_round_trip_stable() {
        for cat in CATEGORIES {
            assert_eq!(NoticeCategory::parse(cat).unwrap().code(), *cat);
        }
        for read in READ_STATES {
            assert_eq!(ReadState::parse(read).unwrap().code(), *read);
        }
        for action in ACTIONS {
            assert_eq!(NoticeAction::parse(action).unwrap().code(), *action);
        }
        for path in CLOSE_PATHS {
            assert_eq!(ClosePath::parse(path).unwrap().code(), *path);
        }
    }

    #[test]
    fn capacity_is_bounded() {
        let mut p = NoticeCenter::default();
        for i in 0..MAX_ENTRIES + 4 {
            let id = format!("n{}", i);
            p.add_entry(&id, NoticeCategory::Update, ReadState::Unread, NoticeAction::Later, true, false);
        }
        assert_eq!(p.entries.len(), MAX_ENTRIES);
        assert!(p.is_builtin(BUILTIN_ID));
    }
}

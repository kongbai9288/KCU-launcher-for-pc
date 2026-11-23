use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::{Component, Path};

pub const INSTANCE_IMPORT_FILE: &str = "instance-import.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"format":"mrpack","current":0,"entries":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_ENTRIES: usize = 24;
pub const MAX_ENTRY_BYTES: u64 = 64 * 1024 * 1024;
pub const EVENT_TARGET: &str = "instance.import";
pub const ROOT_KEYS: &[&str] = &["schema", "format", "current", "entries"];
pub const ENTRY_KEYS: &[&str] = &["id", "path", "kind", "action", "state", "bytes"];
pub const FORMATS: &[&str] = &["mrpack", "curseforge_zip", "portable_instance", "instance_template"];
pub const KINDS: &[&str] = &["mod", "plugin", "config", "world", "other"];
pub const ACTIONS: &[&str] = &["create", "clone", "overwrite_confirm", "skip", "auto_rename"];
pub const STATES: &[&str] = &["pending", "accepted", "rejected"];
pub const PATH_KINDS: &[(&str, &str)] = &[
    ("mods", "mod"),
    ("plugins", "plugin"),
    ("config", "config"),
    ("saves", "world"),
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ImportFormat {
    Mrpack,
    CurseForgeZip,
    PortableInstance,
    InstanceTemplate,
}

impl ImportFormat {
    pub fn code(&self) -> &'static str {
        match self {
            ImportFormat::Mrpack => "mrpack",
            ImportFormat::CurseForgeZip => "curseforge_zip",
            ImportFormat::PortableInstance => "portable_instance",
            ImportFormat::InstanceTemplate => "instance_template",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "mrpack" => Some(ImportFormat::Mrpack),
            "curseforge_zip" => Some(ImportFormat::CurseForgeZip),
            "portable_instance" => Some(ImportFormat::PortableInstance),
            "instance_template" => Some(ImportFormat::InstanceTemplate),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EntryKind {
    Mod,
    Plugin,
    Config,
    World,
    Other,
}

impl EntryKind {
    pub fn code(&self) -> &'static str {
        match self {
            EntryKind::Mod => "mod",
            EntryKind::Plugin => "plugin",
            EntryKind::Config => "config",
            EntryKind::World => "world",
            EntryKind::Other => "other",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "mod" => Some(EntryKind::Mod),
            "plugin" => Some(EntryKind::Plugin),
            "config" => Some(EntryKind::Config),
            "world" => Some(EntryKind::World),
            "other" => Some(EntryKind::Other),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ImportAction {
    Create,
    Clone,
    OverwriteConfirm,
    Skip,
    AutoRename,
}

impl ImportAction {
    pub fn code(&self) -> &'static str {
        match self {
            ImportAction::Create => "create",
            ImportAction::Clone => "clone",
            ImportAction::OverwriteConfirm => "overwrite_confirm",
            ImportAction::Skip => "skip",
            ImportAction::AutoRename => "auto_rename",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "create" => Some(ImportAction::Create),
            "clone" => Some(ImportAction::Clone),
            "overwrite_confirm" => Some(ImportAction::OverwriteConfirm),
            "skip" => Some(ImportAction::Skip),
            "auto_rename" => Some(ImportAction::AutoRename),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EntryState {
    Pending,
    Accepted,
    Rejected,
}

impl EntryState {
    pub fn code(&self) -> &'static str {
        match self {
            EntryState::Pending => "pending",
            EntryState::Accepted => "accepted",
            EntryState::Rejected => "rejected",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "pending" => Some(EntryState::Pending),
            "accepted" => Some(EntryState::Accepted),
            "rejected" => Some(EntryState::Rejected),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ImportEntry {
    pub id: String,
    pub path: String,
    pub kind: EntryKind,
    pub action: ImportAction,
    pub state: EntryState,
    pub bytes: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InstanceImport {
    pub format: ImportFormat,
    pub current: usize,
    pub entries: Vec<ImportEntry>,
}

impl Default for InstanceImport {
    fn default() -> Self {
        InstanceImport { format: ImportFormat::Mrpack, current: 0, entries: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("instance", action, "import", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("instance", action, "import", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_TEXT_BYTES && !has_control(s)
}

fn validate_entry_path(s: &str) -> Option<String> {
    if s.is_empty() || s.len() > robust::MAX_PATH_BYTES || has_control(s) {
        return None;
    }
    let mut parts: Vec<String> = Vec::new();
    for c in Path::new(s).components() {
        match c {
            Component::Normal(part) => {
                let text = part.to_string_lossy();
                if text.is_empty() || text.len() > robust::MAX_ID_BYTES {
                    return None;
                }
                if text.bytes().any(|b| {
                    b < 0x20
                        || matches!(b, b'<' | b'>' | b':' | b'"' | b'|' | b'?' | b'*' | b'\\')
                }) {
                    return None;
                }
                parts.push(text.into_owned());
            }
            Component::CurDir | Component::ParentDir | Component::RootDir | Component::Prefix(_) => {
                return None;
            }
        }
        if parts.len() > robust::MAX_REL_DEPTH {
            return None;
        }
    }
    if parts.is_empty() {
        return None;
    }
    Some(parts.join("/"))
}

fn classify_path(path: &str) -> EntryKind {
    let first = match path.split('/').next() {
        Some(v) => v,
        None => return EntryKind::Other,
    };
    for (prefix, code) in PATH_KINDS {
        if *prefix == first {
            if let Some(k) = EntryKind::parse(code) {
                return k;
            }
            return EntryKind::Other;
        }
    }
    EntryKind::Other
}

fn entry_consistent(i: &ImportEntry) -> bool {
    if i.state == EntryState::Accepted && i.action == ImportAction::Skip {
        return false;
    }
    if i.state == EntryState::Pending && i.action == ImportAction::Skip {
        return false;
    }
    if i.kind != classify_path(&i.path) {
        return false;
    }
    if i.bytes > MAX_ENTRY_BYTES {
        return false;
    }
    if i.action == ImportAction::Clone && i.kind == EntryKind::World {
        return false;
    }
    true
}

fn parse(raw: &str) -> (InstanceImport, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (InstanceImport::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (InstanceImport::default(), lines);
        }
    };
    if obj.keys().any(|k| !ROOT_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (InstanceImport::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (InstanceImport::default(), lines);
    }
    let format = match obj.get("format").and_then(Value::as_str).and_then(ImportFormat::parse) {
        Some(f) => f,
        None => {
            lines.push(degrade("load", "bad_format"));
            return (InstanceImport::default(), lines);
        }
    };
    let arr = match obj.get("entries").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "entries_not_array"));
            return (InstanceImport::default(), lines);
        }
    };
    if arr.len() > MAX_ENTRIES {
        lines.push(degrade("load", "entries_too_many"));
        return (InstanceImport::default(), lines);
    }
    let current = match obj.get("current").and_then(Value::as_u64) {
        Some(n) => match usize::try_from(n) {
            Ok(v) => v,
            Err(_) => {
                lines.push(degrade("load", "bad_current"));
                return (InstanceImport::default(), lines);
            }
        },
        None => {
            lines.push(degrade("load", "bad_current"));
            return (InstanceImport::default(), lines);
        }
    };
    if current > arr.len() {
        lines.push(degrade("load", "current_out_of_range"));
        return (InstanceImport::default(), lines);
    }
    let mut items: Vec<ImportEntry> = Vec::new();
    for item in arr {
        let io = match item.as_object() {
            Some(o) => o,
            None => {
                lines.push(degrade("load", "entry_not_object"));
                return (InstanceImport::default(), lines);
            }
        };
        if io.keys().any(|k| !ENTRY_KEYS.contains(&k.as_str())) {
            lines.push(degrade("load", "entry_unknown_key"));
            return (InstanceImport::default(), lines);
        }
        let id = match io.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "id_too_large"));
                return (InstanceImport::default(), lines);
            }
            Some(_) => {
                lines.push(degrade("load", "bad_id"));
                return (InstanceImport::default(), lines);
            }
            None => {
                lines.push(degrade("load", "bad_id"));
                return (InstanceImport::default(), lines);
            }
        };
        if items.iter().any(|e| e.id == id) {
            lines.push(degrade("load", "duplicate_id"));
            return (InstanceImport::default(), lines);
        }
        let path = match io.get("path").and_then(Value::as_str).and_then(validate_entry_path) {
            Some(p) => p,
            None => {
                lines.push(degrade("load", "path_escapes_root"));
                return (InstanceImport::default(), lines);
            }
        };
        let kind = match io.get("kind").and_then(Value::as_str).and_then(EntryKind::parse) {
            Some(k) => k,
            None => {
                lines.push(degrade("load", "bad_kind"));
                return (InstanceImport::default(), lines);
            }
        };
        let action = match io.get("action").and_then(Value::as_str).and_then(ImportAction::parse) {
            Some(a) => a,
            None => {
                lines.push(degrade("load", "bad_action"));
                return (InstanceImport::default(), lines);
            }
        };
        let state = match io.get("state").and_then(Value::as_str).and_then(EntryState::parse) {
            Some(s) => s,
            None => {
                lines.push(degrade("load", "bad_state"));
                return (InstanceImport::default(), lines);
            }
        };
        let bytes = match io.get("bytes").and_then(Value::as_u64) {
            Some(n) if n <= MAX_ENTRY_BYTES => n,
            _ => {
                lines.push(degrade("load", "bad_bytes"));
                return (InstanceImport::default(), lines);
            }
        };
        let next = ImportEntry { id, path, kind, action, state, bytes };
        if kind != classify_path(&next.path) {
            lines.push(degrade("load", "kind_path_mismatch"));
            return (InstanceImport::default(), lines);
        }
        if !entry_consistent(&next) {
            lines.push(degrade("load", "bad_entry_state"));
            return (InstanceImport::default(), lines);
        }
        items.push(next);
    }
    (InstanceImport { format, current, entries: items }, lines)
}

fn serialize(p: &InstanceImport) -> Result<String> {
    let entries: Vec<Value> = p.entries.iter().map(|i| json!({
        "id": i.id,
        "path": i.path,
        "kind": i.kind.code(),
        "action": i.action.code(),
        "state": i.state.code(),
        "bytes": i.bytes,
    })).collect();
    Ok(to_string(&json!({
        "schema": 1,
        "format": p.format.code(),
        "current": p.current,
        "entries": entries
    }))?)
}

fn write(root: &Path, p: &InstanceImport) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, INSTANCE_IMPORT_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", INSTANCE_IMPORT_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl InstanceImport {
    pub fn open(root: Option<&Path>) -> (InstanceImport, Vec<String>) {
        let Some(dir) = root else {
            return (InstanceImport::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, INSTANCE_IMPORT_FILE) {
            Ok(p) => p,
            Err(_) => return (InstanceImport::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (InstanceImport::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (InstanceImport::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn page_count(&self) -> usize {
        self.entries.len()
    }

    pub fn pending_count(&self) -> usize {
        self.entries.iter().filter(|e| e.state == EntryState::Pending).count()
    }

    pub fn accepted_count(&self) -> usize {
        self.entries.iter().filter(|e| e.state == EntryState::Accepted).count()
    }

    pub fn rejected_count(&self) -> usize {
        self.entries.iter().filter(|e| e.state == EntryState::Rejected).count()
    }

    pub fn current_entry(&self) -> Option<&ImportEntry> {
        self.entries.get(self.current)
    }

    pub fn by_kind(&self, kind: EntryKind) -> Vec<&ImportEntry> {
        self.entries.iter().filter(|e| e.kind == kind).collect()
    }

    pub fn by_action(&self, action: ImportAction) -> Vec<&ImportEntry> {
        self.entries.iter().filter(|e| e.action == action).collect()
    }

    pub fn summary(&self) -> String {
        diag_line("instance", "summary", "import", "OK",
            &format!("pages={} pending={} accepted={} rejected={} formats={} kinds={}",
                self.page_count(), self.pending_count(), self.accepted_count(),
                self.rejected_count(), FORMATS.len(), KINDS.len()))
    }

    pub fn add_entry(&mut self, id: &str, path: &str, bytes: u64) -> bool {
        if !valid_id(id) || self.entries.len() >= MAX_ENTRIES {
            return false;
        }
        if self.entries.iter().any(|e| e.id == id) {
            return false;
        }
        let normalized = match validate_entry_path(path) {
            Some(p) => p,
            None => return false,
        };
        let kind = classify_path(&normalized);
        let candidate = ImportEntry {
            id: id.to_string(),
            path: normalized,
            kind,
            action: ImportAction::Create,
            state: EntryState::Pending,
            bytes,
        };
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries.push(candidate);
        true
    }

    pub fn append_entry(&mut self, id: &str, path: &str, bytes: u64) -> bool {
        if self.pending_count() == 0 {
            return false;
        }
        self.add_entry(id, path, bytes)
    }

    pub fn resolve_current(&mut self, state: EntryState) -> bool {
        if state == EntryState::Pending || self.current >= self.entries.len() {
            return false;
        }
        let mut next: ImportEntry = match self.entries.get(self.current) {
            Some(e) => e.clone(),
            None => return false,
        };
        next.state = state;
        if !entry_consistent(&next) {
            return false;
        }
        self.entries[self.current] = next;
        self.current += 1;
        true
    }

    pub fn set_action(&mut self, id: &str, action: ImportAction) -> bool {
        let mut next: ImportEntry = match self.entries.iter().find(|e| e.id == id) {
            Some(e) => e.clone(),
            None => return false,
        };
        next.action = action;
        if !entry_consistent(&next) {
            return false;
        }
        if let Some(slot) = self.entries.iter_mut().find(|e| e.id == id) {
            *slot = next;
            return true;
        }
        false
    }

    pub fn set_state(&mut self, id: &str, state: EntryState) -> bool {
        let mut next: ImportEntry = match self.entries.iter().find(|e| e.id == id) {
            Some(e) => e.clone(),
            None => return false,
        };
        next.state = state;
        if !entry_consistent(&next) {
            return false;
        }
        if let Some(slot) = self.entries.iter_mut().find(|e| e.id == id) {
            *slot = next;
            return true;
        }
        false
    }

    pub fn set_path(&mut self, id: &str, path: &str) -> bool {
        let normalized = match validate_entry_path(path) {
            Some(p) => p,
            None => return false,
        };
        let mut next: ImportEntry = match self.entries.iter().find(|e| e.id == id) {
            Some(e) => e.clone(),
            None => return false,
        };
        next.path = normalized;
        next.kind = classify_path(&next.path);
        if !entry_consistent(&next) {
            return false;
        }
        if let Some(slot) = self.entries.iter_mut().find(|e| e.id == id) {
            *slot = next;
            return true;
        }
        false
    }

    pub fn set_format(&mut self, format: ImportFormat) {
        self.format = format;
    }

    pub fn remove_entry(&mut self, id: &str) -> bool {
        let before = self.entries.len();
        self.entries.retain(|e| e.id != id);
        if self.entries.len() == before {
            return false;
        }
        if self.current > self.entries.len() {
            self.current = self.entries.len();
        }
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
            .with("pages", &self.page_count().to_string())
            .with("current", &self.current.to_string())
            .with("pending", &self.pending_count().to_string())
            .with("accepted", &self.accepted_count().to_string())
            .with("rejected", &self.rejected_count().to_string())
            .with("create", &self.by_action(ImportAction::Create).len().to_string())
            .with("clone", &self.by_action(ImportAction::Clone).len().to_string())
            .with("skip", &self.by_action(ImportAction::Skip).len().to_string())
            .with("formats", &FORMATS.len().to_string())
            .with("kinds", &KINDS.len().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    InstanceImport::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use serde_json::from_str;

    fn sample() -> InstanceImport {
        InstanceImport::default()
    }

    #[test]
    fn default_state_is_empty() {
        let p = sample();
        assert_eq!(p.page_count(), 0);
        assert_eq!(p.pending_count(), 0);
        assert_eq!(p.format, ImportFormat::Mrpack);
    }

    #[test]
    fn path_rejects_parent_dir() {
        assert_eq!(validate_entry_path("mods/../config/a.toml"), None);
    }

    #[test]
    fn path_rejects_root_dir() {
        assert_eq!(validate_entry_path("/etc/config"), None);
    }

    #[test]
    fn path_rejects_cur_dir() {
        assert_eq!(validate_entry_path("./mods/a"), None);
    }

    #[test]
    fn path_rejects_windows_prefix_form() {
        assert_eq!(validate_entry_path("C:/mods/a"), None);
    }

    #[test]
    fn path_rejects_control_and_empty() {
        assert_eq!(validate_entry_path(""), None);
        assert_eq!(validate_entry_path("mods/a\n"), None);
    }

    #[test]
    fn path_rejects_too_deep() {
        let deep = vec!["d"; robust::MAX_REL_DEPTH + 2].join("/");
        assert_eq!(validate_entry_path(&deep), None);
    }

    #[test]
    fn path_accepts_normal_relative() {
        assert_eq!(validate_entry_path("mods/a.toml"), Some("mods/a.toml".to_string()));
    }

    #[test]
    fn classify_maps_known_prefixes() {
        assert_eq!(classify_path("mods/a"), EntryKind::Mod);
        assert_eq!(classify_path("plugins/a"), EntryKind::Plugin);
        assert_eq!(classify_path("config/a"), EntryKind::Config);
        assert_eq!(classify_path("saves/a"), EntryKind::World);
    }

    #[test]
    fn classify_unknown_is_other() {
        assert_eq!(classify_path("assets/a"), EntryKind::Other);
    }

    #[test]
    fn parse_rejects_unknown_root_key() {
        let (p, lines) = parse(r#"{"schema":1,"format":"mrpack","current":0,"entries":[],"extra":1}"#);
        assert_eq!(p.page_count(), 0);
        assert!(lines.iter().any(|l| l.contains("unknown_key")));
    }

    #[test]
    fn parse_rejects_unknown_entry_key() {
        let raw = r#"{"schema":1,"format":"mrpack","current":0,"entries":[{"id":"a","path":"mods/a","kind":"mod","action":"create","state":"pending","bytes":1,"extra":1}]}"#;
        let (_, lines) = parse(raw);
        assert!(lines.iter().any(|l| l.contains("entry_unknown_key")));
    }

    #[test]
    fn parse_rejects_path_escape() {
        let raw = r#"{"schema":1,"format":"mrpack","current":0,"entries":[{"id":"a","path":"../mods/a","kind":"mod","action":"create","state":"pending","bytes":1}]}"#;
        let (_, lines) = parse(raw);
        assert!(lines.iter().any(|l| l.contains("path_escapes_root")));
    }

    #[test]
    fn parse_rejects_duplicate_id() {
        let raw = r#"{"schema":1,"format":"mrpack","current":0,"entries":[{"id":"a","path":"mods/a","kind":"mod","action":"create","state":"pending","bytes":1},{"id":"a","path":"mods/b","kind":"mod","action":"create","state":"pending","bytes":1}]}"#;
        let (_, lines) = parse(raw);
        assert!(lines.iter().any(|l| l.contains("duplicate_id")));
    }

    #[test]
    fn parse_rejects_current_out_of_range() {
        let (_, lines) = parse(r#"{"schema":1,"format":"mrpack","current":2,"entries":[]}"#);
        assert!(lines.iter().any(|l| l.contains("current_out_of_range")));
    }

    #[test]
    fn parse_rejects_schema_invalid() {
        let (_, lines) = parse(r#"{"schema":2,"format":"mrpack","current":0,"entries":[]}"#);
        assert!(lines.iter().any(|l| l.contains("schema_invalid")));
    }

    #[test]
    fn parse_rejects_kind_path_mismatch() {
        let raw = r#"{"schema":1,"format":"mrpack","current":0,"entries":[{"id":"a","path":"mods/a","kind":"world","action":"create","state":"pending","bytes":1}]}"#;
        let (_, lines) = parse(raw);
        assert!(lines.iter().any(|l| l.contains("kind_path_mismatch")));
    }

    #[test]
    fn parse_accepts_well_formed_entry() {
        let raw = r#"{"schema":1,"format":"mrpack","current":0,"entries":[{"id":"a","path":"mods/a","kind":"mod","action":"create","state":"pending","bytes":1}]}"#;
        let (p, lines) = parse(raw);
        assert_eq!(p.page_count(), 1);
        assert!(lines.is_empty());
    }

    #[test]
    fn add_entry_single_and_resolve_advances_one() {
        let mut p = sample();
        assert!(p.add_entry("a", "mods/a", 1));
        assert!(p.add_entry("b", "config/b", 1));
        assert_eq!(p.pending_count(), 2);
        assert!(p.resolve_current(EntryState::Accepted));
        assert_eq!(p.current, 1);
        assert_eq!(p.pending_count(), 1);
    }

    #[test]
    fn append_entry_requires_pending() {
        let mut p = sample();
        assert!(!p.append_entry("a", "mods/a", 1));
        assert!(p.add_entry("a", "mods/a", 1));
        assert!(p.append_entry("b", "config/b", 1));
    }

    #[test]
    fn set_action_updates_one_entry() {
        let mut p = sample();
        assert!(p.add_entry("a", "mods/a", 1));
        assert!(p.set_action("a", ImportAction::AutoRename));
        assert_eq!(p.by_action(ImportAction::AutoRename).len(), 1);
        assert!(!p.set_action("missing", ImportAction::Skip));
    }

    #[test]
    fn skip_requires_decided_state() {
        let mut p = sample();
        assert!(p.add_entry("a", "mods/a", 1));
        assert!(!p.set_action("a", ImportAction::Skip));
        assert!(p.set_state("a", EntryState::Rejected));
        assert!(p.set_action("a", ImportAction::Skip));
    }

    #[test]
    fn clone_rejects_world_entry() {
        let mut p = sample();
        assert!(p.add_entry("a", "saves/w", 1));
        assert!(!p.set_action("a", ImportAction::Clone));
    }

    #[test]
    fn serialize_roundtrip_is_byte_stable() {
        let mut p = sample();
        p.set_format(ImportFormat::PortableInstance);
        assert!(p.add_entry("a", "mods/a", 12));
        let body = serialize(&p).unwrap();
        let (q, lines) = parse(&body);
        assert!(lines.is_empty());
        assert_eq!(q, p);
        let v: Value = from_str(&body).unwrap();
        assert_eq!(v["format"].as_str(), Some("portable_instance"));
    }

    #[test]
    fn change_event_payload_has_no_user_text() {
        let mut p = sample();
        p.add_entry("secret-id", "mods/secret-name", 7);
        let e = p.change_event();
        let body = e.to_json_string().unwrap();
        assert!(!body.contains("secret-id"));
        assert!(!body.contains("secret-name"));
        assert_eq!(e.field("pages"), Some("1"));
        assert_eq!(e.field("formats"), Some("4"));
    }

    #[test]
    fn persist_without_root_reports_no_root() {
        let p = sample();
        let lines = p.persist(None);
        assert_eq!(lines.len(), 1);
        assert!(lines[0].contains("no_root"));
    }

    #[test]
    fn open_without_root_is_in_memory() {
        let (p, lines) = InstanceImport::open(None);
        assert_eq!(p.page_count(), 0);
        assert!(lines.iter().any(|l| l.contains("in_memory")));
    }

    #[test]
    fn remove_entry_clamps_current() {
        let mut p = sample();
        assert!(p.add_entry("a", "mods/a", 1));
        assert!(p.add_entry("b", "mods/b", 1));
        assert!(p.resolve_current(EntryState::Accepted));
        assert!(p.remove_entry("b"));
        assert_eq!(p.current, 1);
        assert_eq!(p.page_count(), 1);
    }
}

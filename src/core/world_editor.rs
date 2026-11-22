use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const WORLD_EDITOR_FILE: &str = "world-editor.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"session":"draft","entries":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_ENTRIES: usize = 24;
pub const EVENT_TARGET: &str = "world.editor";
pub const VERIFIED_LICENSE: &str = "MIT";
pub const KNOWN_KEYS: &[&str] = &["schema", "session", "entries"];
pub const ENTRY_KEYS: &[&str] = &["id", "field", "format", "source", "license", "link_mode", "verified", "diff_checked", "state"];
pub const FIELDS: &[&str] = &["seed", "world_type", "chunks", "dimension"];
pub const FORMATS: &[&str] = &["int", "bool", "opaque"];
pub const SOURCES: &[&str] = &["builtin", "open_source"];
pub const LINK_MODES: &[&str] = &["same_license", "dynamic_link", "separate_process"];
pub const STATES: &[&str] = &["draft", "verified", "applied"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EditField {
    Seed,
    WorldType,
    Chunks,
    Dimension,
}

impl EditField {
    pub fn code(&self) -> &'static str {
        match self {
            EditField::Seed => "seed",
            EditField::WorldType => "world_type",
            EditField::Chunks => "chunks",
            EditField::Dimension => "dimension",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "seed" => Some(EditField::Seed),
            "world_type" => Some(EditField::WorldType),
            "chunks" => Some(EditField::Chunks),
            "dimension" => Some(EditField::Dimension),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ValueFormat {
    Int,
    Bool,
    Opaque,
}

impl ValueFormat {
    pub fn code(&self) -> &'static str {
        match self {
            ValueFormat::Int => "int",
            ValueFormat::Bool => "bool",
            ValueFormat::Opaque => "opaque",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "int" => Some(ValueFormat::Int),
            "bool" => Some(ValueFormat::Bool),
            "opaque" => Some(ValueFormat::Opaque),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OssSource {
    Builtin,
    OpenSource,
}

impl OssSource {
    pub fn code(&self) -> &'static str {
        match self {
            OssSource::Builtin => "builtin",
            OssSource::OpenSource => "open_source",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "builtin" => Some(OssSource::Builtin),
            "open_source" => Some(OssSource::OpenSource),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LinkMode {
    SameLicense,
    DynamicLink,
    SeparateProcess,
}

impl LinkMode {
    pub fn code(&self) -> &'static str {
        match self {
            LinkMode::SameLicense => "same_license",
            LinkMode::DynamicLink => "dynamic_link",
            LinkMode::SeparateProcess => "separate_process",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "same_license" => Some(LinkMode::SameLicense),
            "dynamic_link" => Some(LinkMode::DynamicLink),
            "separate_process" => Some(LinkMode::SeparateProcess),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EditorState {
    Draft,
    Verified,
    Applied,
}

impl EditorState {
    pub fn code(&self) -> &'static str {
        match self {
            EditorState::Draft => "draft",
            EditorState::Verified => "verified",
            EditorState::Applied => "applied",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "draft" => Some(EditorState::Draft),
            "verified" => Some(EditorState::Verified),
            "applied" => Some(EditorState::Applied),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EditorEntry {
    pub id: String,
    pub field: EditField,
    pub format: ValueFormat,
    pub source: OssSource,
    pub license: String,
    pub link_mode: LinkMode,
    pub verified: bool,
    pub diff_checked: bool,
    pub state: EditorState,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorldEditor {
    pub session: EditorState,
    pub entries: Vec<EditorEntry>,
}

impl Default for WorldEditor {
    fn default() -> Self {
        WorldEditor { session: EditorState::Draft, entries: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("world", action, "editor", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("world", action, "editor", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_TEXT_BYTES && !has_control(s)
}

fn valid_license(s: &str) -> bool {
    s.len() <= robust::MAX_TEXT_BYTES && !has_control(s)
}

fn entry_consistent(e: &EditorEntry) -> bool {
    if e.source == OssSource::OpenSource && e.license.is_empty() {
        return false;
    }
    if e.state == EditorState::Applied && !e.verified {
        return false;
    }
    if e.state == EditorState::Applied && !e.diff_checked {
        return false;
    }
    if e.link_mode == LinkMode::SeparateProcess && e.source == OssSource::Builtin {
        return false;
    }
    if !e.license.is_empty() && e.source == OssSource::Builtin {
        return false;
    }
    true
}

fn parse(raw: &str) -> (WorldEditor, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (WorldEditor::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (WorldEditor::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (WorldEditor::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (WorldEditor::default(), lines);
    }
    let session = match obj.get("session").and_then(Value::as_str).and_then(EditorState::parse) {
        Some(s) => s,
        None => {
            lines.push(degrade("load", "bad_session"));
            return (WorldEditor::default(), lines);
        }
    };
    let arr = match obj.get("entries").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "entries_not_array"));
            return (WorldEditor::default(), lines);
        }
    };
    if arr.len() > MAX_ENTRIES {
        lines.push(degrade("load", "entries_too_many"));
        return (WorldEditor::default(), lines);
    }
    let mut entries: Vec<EditorEntry> = Vec::new();
    for item in arr {
        let eo = match item.as_object() {
            Some(o) => o,
            None => {
                lines.push(degrade("load", "entry_not_object"));
                return (WorldEditor::default(), lines);
            }
        };
        if eo.keys().any(|k| !ENTRY_KEYS.contains(&k.as_str())) {
            lines.push(degrade("load", "entry_unknown_key"));
            return (WorldEditor::default(), lines);
        }
        let id = match eo.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "id_too_large"));
                return (WorldEditor::default(), lines);
            }
            _ => {
                lines.push(degrade("load", "bad_id"));
                return (WorldEditor::default(), lines);
            }
        };
        if entries.iter().any(|e| e.id == id) {
            lines.push(degrade("load", "duplicate_id"));
            return (WorldEditor::default(), lines);
        }
        let field = match eo.get("field").and_then(Value::as_str).and_then(EditField::parse) {
            Some(f) => f,
            None => {
                lines.push(degrade("load", "bad_field"));
                return (WorldEditor::default(), lines);
            }
        };
        let format = match eo.get("format").and_then(Value::as_str).and_then(ValueFormat::parse) {
            Some(f) => f,
            None => {
                lines.push(degrade("load", "bad_format"));
                return (WorldEditor::default(), lines);
            }
        };
        let source = match eo.get("source").and_then(Value::as_str).and_then(OssSource::parse) {
            Some(s) => s,
            None => {
                lines.push(degrade("load", "bad_source"));
                return (WorldEditor::default(), lines);
            }
        };
        let license = match eo.get("license").and_then(Value::as_str) {
            Some(s) if valid_license(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "license_too_large"));
                return (WorldEditor::default(), lines);
            }
            _ => {
                lines.push(degrade("load", "bad_license"));
                return (WorldEditor::default(), lines);
            }
        };
        let link_mode = match eo.get("link_mode").and_then(Value::as_str).and_then(LinkMode::parse) {
            Some(m) => m,
            None => {
                lines.push(degrade("load", "bad_link_mode"));
                return (WorldEditor::default(), lines);
            }
        };
        let verified = match eo.get("verified").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("load", "bad_verified"));
                return (WorldEditor::default(), lines);
            }
        };
        let diff_checked = match eo.get("diff_checked").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("load", "bad_diff_checked"));
                return (WorldEditor::default(), lines);
            }
        };
        let state = match eo.get("state").and_then(Value::as_str).and_then(EditorState::parse) {
            Some(s) => s,
            None => {
                lines.push(degrade("load", "bad_state"));
                return (WorldEditor::default(), lines);
            }
        };
        let e = EditorEntry { id, field, format, source, license, link_mode, verified, diff_checked, state };
        if !entry_consistent(&e) {
            lines.push(degrade("load", "bad_entry_state"));
            return (WorldEditor::default(), lines);
        }
        entries.push(e);
    }
    (WorldEditor { session, entries }, lines)
}

fn serialize(p: &WorldEditor) -> Result<String> {
    let items: Vec<Value> = p.entries.iter().map(|e| json!({
        "id": e.id,
        "field": e.field.code(),
        "format": e.format.code(),
        "source": e.source.code(),
        "license": e.license,
        "link_mode": e.link_mode.code(),
        "verified": e.verified,
        "diff_checked": e.diff_checked,
        "state": e.state.code(),
    })).collect();
    Ok(to_string(&json!({ "schema": 1, "session": p.session.code(), "entries": items }))?)
}

fn write(root: &Path, p: &WorldEditor) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, WORLD_EDITOR_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", WORLD_EDITOR_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl WorldEditor {
    pub fn open(root: Option<&Path>) -> (WorldEditor, Vec<String>) {
        let Some(dir) = root else {
            return (WorldEditor::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, WORLD_EDITOR_FILE) {
            Ok(p) => p,
            Err(_) => return (WorldEditor::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (WorldEditor::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (WorldEditor::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn editable_count(&self) -> usize {
        self.entries.iter().filter(|e| e.state != EditorState::Applied).count()
    }

    pub fn verified_count(&self) -> usize {
        self.entries.iter().filter(|e| e.verified).count()
    }

    pub fn by_field(&self, field: EditField) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for e in &self.entries {
            if e.field == field {
                out.push(e.id.as_str());
            }
        }
        out
    }

    pub fn by_source(&self, source: OssSource) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for e in &self.entries {
            if e.source == source {
                out.push(e.id.as_str());
            }
        }
        out
    }

    pub fn by_link_mode(&self, mode: LinkMode) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for e in &self.entries {
            if e.link_mode == mode {
                out.push(e.id.as_str());
            }
        }
        out
    }

    pub fn license_for(&self, id: &str) -> Option<&str> {
        self.entries.iter().find(|e| e.id == id).map(|e| e.license.as_str())
    }

    pub fn applied_count(&self) -> usize {
        self.entries.iter().filter(|e| e.state == EditorState::Applied).count()
    }

    pub fn summary(&self) -> [usize; 4] {
        let mut out: [usize; 4] = [0, 0, 0, 0];
        for e in &self.entries {
            let idx = match e.field {
                EditField::Seed => 0,
                EditField::WorldType => 1,
                EditField::Chunks => 2,
                EditField::Dimension => 3,
            };
            out[idx] += 1;
        }
        out
    }

    pub fn add_entry(&mut self, id: &str, field: EditField, format: ValueFormat, source: OssSource, license: &str, link_mode: LinkMode, verified: bool, diff_checked: bool, state: EditorState) -> bool {
        if self.entries.len() >= MAX_ENTRIES || !valid_id(id) || !valid_license(license) || self.entries.iter().any(|e| e.id == id) {
            return false;
        }
        if !FIELDS.contains(&field.code()) || !FORMATS.contains(&format.code()) || !SOURCES.contains(&source.code()) || !LINK_MODES.contains(&link_mode.code()) || !STATES.contains(&state.code()) {
            return false;
        }
        let e = EditorEntry {
            id: id.to_string(),
            field,
            format,
            source,
            license: license.to_string(),
            link_mode,
            verified,
            diff_checked,
            state,
        };
        if !entry_consistent(&e) {
            return false;
        }
        self.entries.push(e);
        true
    }

    pub fn set_field(&mut self, id: &str, field: EditField) -> bool {
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.field = field;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].field = field;
        true
    }

    pub fn set_source(&mut self, id: &str, source: OssSource) -> bool {
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.source = source;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].source = source;
        true
    }

    pub fn set_link_mode(&mut self, id: &str, link_mode: LinkMode) -> bool {
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.link_mode = link_mode;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].link_mode = link_mode;
        true
    }

    pub fn set_state(&mut self, id: &str, state: EditorState) -> bool {
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.state = state;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].state = state;
        true
    }

    pub fn set_verified(&mut self, id: &str, verified: bool) -> bool {
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.verified = verified;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].verified = verified;
        true
    }

    pub fn set_diff_checked(&mut self, id: &str, diff_checked: bool) -> bool {
        let Some(pos) = self.entries.iter().position(|e| e.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.diff_checked = diff_checked;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].diff_checked = diff_checked;
        true
    }

    pub fn remove_entry(&mut self, id: &str) -> bool {
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
            .with("session", self.session.code())
            .with("editable", &self.editable_count().to_string())
            .with("verified", &self.verified_count().to_string())
            .with("applied", &self.applied_count().to_string())
            .with("open_source", &self.by_source(OssSource::OpenSource).len().to_string())
            .with("separate_process", &self.by_link_mode(LinkMode::SeparateProcess).len().to_string())
            .with("fields", &FIELDS.len().to_string())
            .with("formats", &FORMATS.len().to_string())
            .with("links", &LINK_MODES.len().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    WorldEditor::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu082-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    fn load(dir: &std::path::Path, raw: &str) -> (WorldEditor, Vec<String>) {
        fs::create_dir_all(dir).unwrap();
        fs::write(dir.join(WORLD_EDITOR_FILE), raw).unwrap();
        WorldEditor::open(Some(dir))
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"session":"draft","entries":[]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 3);
        assert_eq!(v["entries"].as_array().unwrap().len(), 0);
        assert_eq!(v["session"], "draft");
    }

    #[test]
    fn five_enum_codes_and_seven_tables_are_explicit() {
        assert_eq!(EditField::Seed.code(), "seed");
        assert_eq!(EditField::WorldType.code(), "world_type");
        assert_eq!(EditField::Chunks.code(), "chunks");
        assert_eq!(EditField::Dimension.code(), "dimension");
        assert_eq!(EditField::parse("nope"), None);
        assert_eq!(ValueFormat::Int.code(), "int");
        assert_eq!(ValueFormat::Bool.code(), "bool");
        assert_eq!(ValueFormat::Opaque.code(), "opaque");
        assert_eq!(ValueFormat::parse("nope"), None);
        assert_eq!(OssSource::Builtin.code(), "builtin");
        assert_eq!(OssSource::OpenSource.code(), "open_source");
        assert_eq!(OssSource::parse("nope"), None);
        assert_eq!(LinkMode::SameLicense.code(), "same_license");
        assert_eq!(LinkMode::DynamicLink.code(), "dynamic_link");
        assert_eq!(LinkMode::SeparateProcess.code(), "separate_process");
        assert_eq!(LinkMode::parse("nope"), None);
        assert_eq!(EditorState::Draft.code(), "draft");
        assert_eq!(EditorState::Verified.code(), "verified");
        assert_eq!(EditorState::Applied.code(), "applied");
        assert_eq!(EditorState::parse("nope"), None);
        assert_eq!(KNOWN_KEYS.len(), 3);
        assert_eq!(ENTRY_KEYS.len(), 9);
        assert_eq!(FIELDS.len(), 4);
        assert_eq!(FORMATS.len(), 3);
        assert_eq!(SOURCES.len(), 2);
        assert_eq!(LINK_MODES.len(), 3);
        assert_eq!(STATES.len(), 3);
        assert_eq!(VERIFIED_LICENSE, "MIT");
    }

    #[test]
    fn default_is_empty_draft_session() {
        let (p, lines) = WorldEditor::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, WorldEditor::default());
        assert_eq!(p.session, EditorState::Draft);
        assert_eq!(p.entries.len(), 0);
        assert_eq!(p.editable_count(), 0);
        assert_eq!(p.verified_count(), 0);
        assert_eq!(p.applied_count(), 0);
        assert_eq!(p.summary(), [0, 0, 0, 0]);
        assert_eq!(p.by_field(EditField::Seed), Vec::<&str>::new());
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
            base.replace("\"session\":\"draft\"", "\"session\":\"nope\""),
            base.replace("\"entries\":[]", "\"entries\":7"),
            base.replace("\"entries\":[", "\"entries\":[null,"),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, WorldEditor::default(), "case={}", &raw[..raw.len().min(48)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(48)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_entry_texts_and_capacity_are_rejected() {
        let r = tmp();
        let e = r#"{"id":"n1","field":"seed","format":"int","source":"open_source","license":"MIT","link_mode":"dynamic_link","verified":true,"diff_checked":true,"state":"draft"}"#;
        let one = format!("{{\"schema\":1,\"session\":\"draft\",\"entries\":[{}]}}", e);
        let cases = vec![
            one.replace("\"entries\":[{", "\"entries\":[{\"extra\":1,"),
            one.replace("\"id\":\"n1\"", "\"id\":\"a\\nb\""),
            one.replace("\"id\":\"n1\"", "\"id\":\"\""),
            one.replace("\"id\":\"n1\"", &format!("\"id\":\"{}\"", "x".repeat(robust::MAX_TEXT_BYTES + 1))),
            one.replace("\"field\":\"seed\"", "\"field\":\"nope\""),
            one.replace("\"format\":\"int\"", "\"format\":\"nope\""),
            one.replace("\"source\":\"open_source\"", "\"source\":\"nope\""),
            one.replace("\"license\":\"MIT\"", "\"license\":\"a\\nb\""),
            one.replace("\"license\":\"MIT\"", &format!("\"license\":\"{}\"", "x".repeat(robust::MAX_TEXT_BYTES + 1))),
            one.replace("\"link_mode\":\"dynamic_link\"", "\"link_mode\":\"nope\""),
            one.replace("\"verified\":true", "\"verified\":\"no\""),
            one.replace("\"diff_checked\":true", "\"diff_checked\":7"),
            one.replace("\"state\":\"draft\"", "\"state\":\"nope\""),
            format!("{{\"schema\":1,\"session\":\"draft\",\"entries\":[{},{}]}}", e, e),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, WorldEditor::default(), "case={}", &raw[..raw.len().min(48)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(48)]);
        }
        let many = format!("{{\"schema\":1,\"session\":\"draft\",\"entries\":[{}]}}",
            (0..MAX_ENTRIES + 1).map(|i| format!("{{\"id\":\"n{}\",\"field\":\"seed\",\"format\":\"int\",\"source\":\"builtin\",\"license\":\"\",\"link_mode\":\"same_license\",\"verified\":false,\"diff_checked\":false,\"state\":\"draft\"}}", i)).collect::<Vec<_>>().join(","));
        let (p, lines) = load(&r, &many);
        assert_eq!(p, WorldEditor::default());
        assert!(lines.iter().any(|x| x.contains("entries_too_many")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn contradiction_states_are_rejected_on_load() {
        let r = tmp();
        let e = r#"{"id":"n1","field":"seed","format":"int","source":"open_source","license":"MIT","link_mode":"dynamic_link","verified":true,"diff_checked":true,"state":"draft"}"#;
        let one = format!("{{\"schema\":1,\"session\":\"draft\",\"entries\":[{}]}}", e);
        let cases = vec![
            (one.replace("\"license\":\"MIT\"", "\"license\":\"\""), "open_source_without_license"),
            (one.replace("\"state\":\"draft\"", "\"state\":\"applied\"").replace("\"verified\":true", "\"verified\":false"), "applied_without_verified"),
            (one.replace("\"state\":\"draft\"", "\"state\":\"applied\"").replace("\"diff_checked\":true", "\"diff_checked\":false"), "applied_without_diff_checked"),
            (one.replace("\"source\":\"open_source\"", "\"source\":\"builtin\"").replace("\"link_mode\":\"dynamic_link\"", "\"link_mode\":\"separate_process\""), "separate_process_with_builtin"),
            (one.replace("\"source\":\"open_source\"", "\"source\":\"builtin\""), "builtin_with_license"),
        ];
        for (raw, tag) in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, WorldEditor::default(), "tag={}", tag);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "tag={}", tag);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn pure_queries_do_not_read_files() {
        let mut p = WorldEditor::default();
        assert!(p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::OpenSource, VERIFIED_LICENSE, LinkMode::DynamicLink, true, true, EditorState::Applied));
        assert!(p.add_entry("b", EditField::Chunks, ValueFormat::Bool, OssSource::Builtin, "", LinkMode::SameLicense, false, false, EditorState::Draft));
        assert_eq!(p.entries.len(), 2);
        assert_eq!(p.editable_count(), 1);
        assert_eq!(p.verified_count(), 1);
        assert_eq!(p.applied_count(), 1);
        assert_eq!(p.by_field(EditField::Seed), vec!["a"]);
        assert_eq!(p.by_field(EditField::WorldType), Vec::<&str>::new());
        assert_eq!(p.by_source(OssSource::OpenSource), vec!["a"]);
        assert_eq!(p.by_source(OssSource::Builtin), vec!["b"]);
        assert_eq!(p.by_link_mode(LinkMode::DynamicLink), vec!["a"]);
        assert_eq!(p.by_link_mode(LinkMode::SeparateProcess), Vec::<&str>::new());
        assert_eq!(p.license_for("a"), Some(VERIFIED_LICENSE));
        assert_eq!(p.license_for("b"), Some(""));
        assert_eq!(p.license_for("missing"), None);
        assert_eq!(p.summary(), [1, 0, 1, 0]);
    }

    #[test]
    fn single_item_mutations_do_not_touch_other_fields() {
        let mut p = WorldEditor::default();
        assert!(p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::OpenSource, VERIFIED_LICENSE, LinkMode::DynamicLink, true, true, EditorState::Verified));
        assert!(p.set_field("a", EditField::Dimension));
        assert_eq!(p.by_field(EditField::Dimension), vec!["a"]);
        assert_eq!(p.license_for("a"), Some(VERIFIED_LICENSE));
        assert_eq!(p.applied_count(), 0);
        assert!(p.set_state("a", EditorState::Applied));
        assert_eq!(p.applied_count(), 1);
        assert_eq!(p.verified_count(), 1);
        assert_eq!(p.entries.len(), 1);
        assert!(!p.set_field("missing", EditField::Seed));
    }

    #[test]
    fn set_state_and_evidence_three_way_contradiction() {
        let mut p = WorldEditor::default();
        assert!(p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::OpenSource, VERIFIED_LICENSE, LinkMode::DynamicLink, false, false, EditorState::Draft));
        assert!(!p.set_state("a", EditorState::Applied));
        assert_eq!(p.applied_count(), 0);
        assert!(p.set_verified("a", true));
        assert!(!p.set_state("a", EditorState::Applied));
        assert!(p.set_diff_checked("a", true));
        assert!(p.set_state("a", EditorState::Applied));
        assert_eq!(p.applied_count(), 1);
        assert!(!p.set_verified("a", false));
        assert!(!p.set_diff_checked("a", false));
        assert_eq!(p.applied_count(), 1);
    }

    #[test]
    fn set_source_and_link_mode_contradiction() {
        let mut p = WorldEditor::default();
        assert!(p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::OpenSource, VERIFIED_LICENSE, LinkMode::DynamicLink, true, true, EditorState::Draft));
        assert!(!p.set_source("a", OssSource::Builtin));
        assert_eq!(p.license_for("a"), Some(VERIFIED_LICENSE));
        assert!(p.set_link_mode("a", LinkMode::SeparateProcess));
        assert_eq!(p.by_link_mode(LinkMode::SeparateProcess), vec!["a"]);
        assert!(!p.set_source("missing", OssSource::Builtin));
        assert!(!p.set_link_mode("missing", LinkMode::SameLicense));
        assert!(!p.set_state("missing", EditorState::Applied));
        assert!(!p.set_verified("missing", false));
        assert!(!p.set_diff_checked("missing", false));
    }

    #[test]
    fn add_entry_rejects_bad_inputs() {
        let mut p = WorldEditor::default();
        assert!(!p.add_entry("", EditField::Seed, ValueFormat::Int, OssSource::Builtin, "", LinkMode::SameLicense, false, false, EditorState::Draft));
        assert!(!p.add_entry("bad\nid", EditField::Seed, ValueFormat::Int, OssSource::Builtin, "", LinkMode::SameLicense, false, false, EditorState::Draft));
        assert!(!p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::OpenSource, "", LinkMode::DynamicLink, false, false, EditorState::Draft));
        assert!(!p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::Builtin, VERIFIED_LICENSE, LinkMode::SameLicense, false, false, EditorState::Draft));
        assert!(!p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::Builtin, "", LinkMode::SeparateProcess, false, false, EditorState::Draft));
        assert!(!p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::OpenSource, VERIFIED_LICENSE, LinkMode::DynamicLink, false, false, EditorState::Applied));
        assert!(p.add_entry("a", EditField::Dimension, ValueFormat::Opaque, OssSource::OpenSource, VERIFIED_LICENSE, LinkMode::DynamicLink, true, true, EditorState::Verified));
        assert!(!p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::Builtin, "", LinkMode::SameLicense, false, false, EditorState::Draft));
        assert_eq!(p.entries.len(), 1);
    }

    #[test]
    fn remove_entry_is_single_item() {
        let mut p = WorldEditor::default();
        assert!(p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::Builtin, "", LinkMode::SameLicense, false, false, EditorState::Draft));
        assert!(p.add_entry("b", EditField::Chunks, ValueFormat::Bool, OssSource::Builtin, "", LinkMode::SameLicense, false, false, EditorState::Draft));
        assert!(p.remove_entry("a"));
        assert_eq!(p.entries.len(), 1);
        assert_eq!(p.by_field(EditField::Chunks), vec!["b"]);
        assert!(!p.remove_entry("missing"));
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let p = WorldEditor::default();
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
        let mut p = WorldEditor::default();
        assert!(p.add_entry("a", EditField::Seed, ValueFormat::Int, OssSource::OpenSource, VERIFIED_LICENSE, LinkMode::DynamicLink, true, true, EditorState::Applied));
        assert!(p.add_entry("b", EditField::WorldType, ValueFormat::Bool, OssSource::Builtin, "", LinkMode::SameLicense, false, false, EditorState::Draft));
        assert!(p.set_diff_checked("b", true));
        assert_eq!(p.summary(), [1, 1, 0, 0]);
        assert_eq!(p.applied_count(), 1);
        assert!(p.persist(Some(&r)).is_empty());
        let (back, lines) = WorldEditor::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.entries.len(), 2);
        assert_eq!(back.session, EditorState::Draft);
        assert_eq!(back.license_for("a"), Some(VERIFIED_LICENSE));
        assert_eq!(back.applied_count(), 1);
        assert_eq!(back.summary(), [1, 1, 0, 0]);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = WorldEditor::open(Some(&r));
        assert_eq!(def, WorldEditor::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope_without_user_text() {
        let mut p = WorldEditor::default();
        p.add_entry("secret-id", EditField::Seed, ValueFormat::Int, OssSource::OpenSource, VERIFIED_LICENSE, LinkMode::DynamicLink, true, true, EditorState::Applied);
        let e = p.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, EVENT_TARGET);
        assert_eq!(e.field("total"), Some("1"));
        assert_eq!(e.field("session"), Some("draft"));
        assert_eq!(e.field("editable"), Some("0"));
        assert_eq!(e.field("verified"), Some("1"));
        assert_eq!(e.field("applied"), Some("1"));
        assert_eq!(e.field("open_source"), Some("1"));
        assert_eq!(e.field("separate_process"), Some("0"));
        assert_eq!(e.field("fields"), Some("4"));
        assert_eq!(e.field("formats"), Some("3"));
        assert_eq!(e.field("links"), Some("3"));
        assert_eq!(e.field("id"), None);
        assert_eq!(e.field("license"), None);
        assert_eq!(e.field("title"), None);
        assert_eq!(e.field("body"), None);
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 10);
    }

    #[test]
    fn serialize_carries_no_editor_table() {
        let mut p = WorldEditor::default();
        p.add_entry("n1", EditField::Seed, ValueFormat::Int, OssSource::OpenSource, VERIFIED_LICENSE, LinkMode::DynamicLink, true, true, EditorState::Verified);
        let raw = serialize(&p).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 3);
        assert_eq!(v["entries"][0].as_object().unwrap().len(), 9);
        assert!(!raw.contains("EDITOR_TABLE"));
        assert!(!raw.contains("FIELD_TABLE"));
        assert!(!raw.contains("LICENSE_TABLE"));
    }

    #[test]
    fn seven_tables_are_round_trip_stable() {
        for f in FIELDS {
            assert_eq!(EditField::parse(f).unwrap().code(), *f);
        }
        for f in FORMATS {
            assert_eq!(ValueFormat::parse(f).unwrap().code(), *f);
        }
        for s in SOURCES {
            assert_eq!(OssSource::parse(s).unwrap().code(), *s);
        }
        for m in LINK_MODES {
            assert_eq!(LinkMode::parse(m).unwrap().code(), *m);
        }
        for s in STATES {
            assert_eq!(EditorState::parse(s).unwrap().code(), *s);
        }
    }

    #[test]
    fn capacity_is_bounded() {
        let mut p = WorldEditor::default();
        for i in 0..MAX_ENTRIES + 4 {
            let id = format!("n{}", i);
            p.add_entry(&id, EditField::Seed, ValueFormat::Int, OssSource::Builtin, "", LinkMode::SameLicense, false, false, EditorState::Draft);
        }
        assert_eq!(p.entries.len(), MAX_ENTRIES);
    }
}

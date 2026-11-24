use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::{Component, Path};

pub const PROJECTION_FILE: &str = "projection-preview.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"current":0,"entries":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_ENTRIES: usize = 24;
pub const MIN_SCALE: u32 = 25;
pub const MAX_SCALE: u32 = 400;
pub const DEFAULT_SCALE: u32 = 100;
pub const EVENT_TARGET: &str = "projection.preview";
pub const ROOT_KEYS: &[&str] = &["schema", "current", "entries"];
pub const ENTRY_KEYS: &[&str] = &["id", "format", "path", "view", "scale", "state", "decided"];
pub const FORMATS: &[&str] = &["primary", "secondary"];
pub const VIEWS: &[&str] = &["fit", "original", "scaled"];
pub const STATES: &[&str] = &["pending", "previewed", "closed"];
pub const PATH_KINDS: &[(&str, &str)] = &[
    ("primary", "primary"),
    ("secondary", "secondary"),
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProjectionFormat {
    Primary,
    Secondary,
}

impl ProjectionFormat {
    pub fn code(&self) -> &'static str {
        match self {
            ProjectionFormat::Primary => "primary",
            ProjectionFormat::Secondary => "secondary",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "primary" => Some(ProjectionFormat::Primary),
            "secondary" => Some(ProjectionFormat::Secondary),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ViewMode {
    Fit,
    Original,
    Scaled,
}

impl ViewMode {
    pub fn code(&self) -> &'static str {
        match self {
            ViewMode::Fit => "fit",
            ViewMode::Original => "original",
            ViewMode::Scaled => "scaled",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "fit" => Some(ViewMode::Fit),
            "original" => Some(ViewMode::Original),
            "scaled" => Some(ViewMode::Scaled),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PreviewState {
    Pending,
    Previewed,
    Closed,
}

impl PreviewState {
    pub fn code(&self) -> &'static str {
        match self {
            PreviewState::Pending => "pending",
            PreviewState::Previewed => "previewed",
            PreviewState::Closed => "closed",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "pending" => Some(PreviewState::Pending),
            "previewed" => Some(PreviewState::Previewed),
            "closed" => Some(PreviewState::Closed),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PreviewEntry {
    pub id: String,
    pub format: ProjectionFormat,
    pub path: String,
    pub view: ViewMode,
    pub scale: u32,
    pub state: PreviewState,
    pub decided: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ProjectionSession {
    pub current: usize,
    pub entries: Vec<PreviewEntry>,
}

impl Default for ProjectionSession {
    fn default() -> Self {
        ProjectionSession { current: 0, entries: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("projection", action, "preview", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("projection", action, "preview", "ERROR", reason)
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
                let v = part.to_string_lossy();
                if v.is_empty() || v.len() > robust::MAX_ID_BYTES {
                    return None;
                }
                parts.push(v.to_string());
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
    if !PATH_KINDS.iter().any(|(prefix, _)| *prefix == parts[0]) {
        return None;
    }
    Some(parts.join("/"))
}

fn classify_path(path: &str) -> ProjectionFormat {
    let first = match path.split('/').next() {
        Some(v) => v,
        None => return ProjectionFormat::Primary,
    };
    for (prefix, code) in PATH_KINDS {
        if *prefix == first {
            if let Some(f) = ProjectionFormat::parse(code) {
                return f;
            }
            return ProjectionFormat::Primary;
        }
    }
    ProjectionFormat::Primary
}

fn entry_consistent(i: &PreviewEntry) -> bool {
    if i.state == PreviewState::Closed && !i.decided {
        return false;
    }
    if i.decided && i.state == PreviewState::Pending {
        return false;
    }
    if i.view == ViewMode::Scaled && (i.scale < MIN_SCALE || i.scale > MAX_SCALE) {
        return false;
    }
    if i.view != ViewMode::Scaled && i.scale != DEFAULT_SCALE {
        return false;
    }
    if i.format != classify_path(&i.path) {
        return false;
    }
    true
}

fn parse(raw: &str) -> (ProjectionSession, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (ProjectionSession::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (ProjectionSession::default(), lines);
        }
    };
    if obj.keys().any(|k| !ROOT_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (ProjectionSession::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (ProjectionSession::default(), lines);
    }
    let current = match obj.get("current").and_then(Value::as_u64) {
        Some(v) if v <= usize::MAX as u64 => v as usize,
        _ => {
            lines.push(degrade("load", "bad_current"));
            return (ProjectionSession::default(), lines);
        }
    };
    let arr = match obj.get("entries").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "entries_not_array"));
            return (ProjectionSession::default(), lines);
        }
    };
    if arr.len() > MAX_ENTRIES {
        lines.push(degrade("load", "entries_too_many"));
        return (ProjectionSession::default(), lines);
    }
    if current > arr.len() {
        lines.push(degrade("load", "current_out_of_range"));
        return (ProjectionSession::default(), lines);
    }
    let mut items: Vec<PreviewEntry> = Vec::new();
    for item in arr {
        let io = match item.as_object() {
            Some(o) => o,
            None => {
                lines.push(degrade("load", "entry_not_object"));
                return (ProjectionSession::default(), lines);
            }
        };
        if io.keys().any(|k| !ENTRY_KEYS.contains(&k.as_str())) {
            lines.push(degrade("load", "entry_unknown_key"));
            return (ProjectionSession::default(), lines);
        }
        let id = match io.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "id_too_large"));
                return (ProjectionSession::default(), lines);
            }
            _ => {
                lines.push(degrade("load", "bad_id"));
                return (ProjectionSession::default(), lines);
            }
        };
        if items.iter().any(|e| e.id == id) {
            lines.push(degrade("load", "duplicate_id"));
            return (ProjectionSession::default(), lines);
        }
        let format = match io.get("format").and_then(Value::as_str).and_then(ProjectionFormat::parse) {
            Some(f) => f,
            None => {
                lines.push(degrade("load", "bad_format"));
                return (ProjectionSession::default(), lines);
            }
        };
        let path = match io.get("path").and_then(Value::as_str).and_then(validate_entry_path) {
            Some(p) => p,
            None => {
                lines.push(degrade("load", "path_escapes_root"));
                return (ProjectionSession::default(), lines);
            }
        };
        let view = match io.get("view").and_then(Value::as_str).and_then(ViewMode::parse) {
            Some(v) => v,
            None => {
                lines.push(degrade("load", "bad_view"));
                return (ProjectionSession::default(), lines);
            }
        };
        let scale = match io.get("scale").and_then(Value::as_u64) {
            Some(v) if v <= u32::MAX as u64 => v as u32,
            _ => {
                lines.push(degrade("load", "bad_scale"));
                return (ProjectionSession::default(), lines);
            }
        };
        let state = match io.get("state").and_then(Value::as_str).and_then(PreviewState::parse) {
            Some(s) => s,
            None => {
                lines.push(degrade("load", "bad_state"));
                return (ProjectionSession::default(), lines);
            }
        };
        let decided = match io.get("decided").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("load", "bad_decided"));
                return (ProjectionSession::default(), lines);
            }
        };
        let e = PreviewEntry { id, format, path, view, scale, state, decided };
        if !entry_consistent(&e) {
            lines.push(degrade("load", "bad_entry_state"));
            return (ProjectionSession::default(), lines);
        }
        items.push(e);
    }
    (ProjectionSession { current, entries: items }, lines)
}

fn serialize(p: &ProjectionSession) -> Result<String> {
    let entries: Vec<Value> = p.entries.iter().map(|i| json!({
        "id": i.id,
        "format": i.format.code(),
        "path": i.path,
        "view": i.view.code(),
        "scale": i.scale,
        "state": i.state.code(),
        "decided": i.decided,
    })).collect();
    Ok(to_string(&json!({
        "schema": 1,
        "current": p.current,
        "entries": entries,
    }))?)
}

fn write(root: &Path, p: &ProjectionSession) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, PROJECTION_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", PROJECTION_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl ProjectionSession {
    pub fn open(root: Option<&Path>) -> (ProjectionSession, Vec<String>) {
        let Some(dir) = root else {
            return (ProjectionSession::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, PROJECTION_FILE) {
            Ok(p) => p,
            Err(_) => return (ProjectionSession::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (ProjectionSession::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (ProjectionSession::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn page_count(&self) -> usize {
        self.entries.len()
    }

    pub fn pending_count(&self) -> usize {
        self.entries.iter().filter(|i| i.state == PreviewState::Pending).count()
    }

    pub fn previewed_count(&self) -> usize {
        self.entries.iter().filter(|i| i.state == PreviewState::Previewed).count()
    }

    pub fn closed_count(&self) -> usize {
        self.entries.iter().filter(|i| i.state == PreviewState::Closed).count()
    }

    pub fn current_entry(&self) -> Option<&PreviewEntry> {
        self.entries.get(self.current)
    }

    pub fn by_format(&self, format: ProjectionFormat) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for i in &self.entries {
            if i.format == format {
                out.push(i.id.as_str());
            }
        }
        out
    }

    pub fn by_view(&self, view: ViewMode) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for i in &self.entries {
            if i.view == view {
                out.push(i.id.as_str());
            }
        }
        out
    }

    pub fn summary(&self) -> [usize; 3] {
        let mut out: [usize; 3] = [0, 0, 0];
        for i in &self.entries {
            let idx = match i.format {
                ProjectionFormat::Primary => 0,
                ProjectionFormat::Secondary => 1,
            };
            out[idx] += 1;
            out[2] += 1;
        }
        out
    }

    pub fn add_entry(&mut self, id: &str, format: ProjectionFormat, path: &str, view: ViewMode, scale: u32, state: PreviewState, decided: bool) -> bool {
        if self.entries.len() >= MAX_ENTRIES || !valid_id(id) || self.entries.iter().any(|i| i.id == id) {
            return false;
        }
        if !FORMATS.contains(&format.code()) || !VIEWS.contains(&view.code()) || !STATES.contains(&state.code()) {
            return false;
        }
        let Some(p) = validate_entry_path(path) else { return false };
        let e = PreviewEntry {
            id: id.to_string(),
            format,
            path: p,
            view,
            scale,
            state,
            decided,
        };
        if !entry_consistent(&e) {
            return false;
        }
        self.entries.push(e);
        true
    }

    pub fn append_entry(&mut self, id: &str, format: ProjectionFormat, path: &str, view: ViewMode, scale: u32, state: PreviewState, decided: bool) -> bool {
        if self.pending_count() == 0 {
            return false;
        }
        self.add_entry(id, format, path, view, scale, state, decided)
    }

    pub fn resolve_current(&mut self, state: PreviewState, decided: bool) -> bool {
        if state == PreviewState::Pending || self.current >= self.entries.len() {
            return false;
        }
        let mut candidate = match self.entries.get(self.current) {
            Some(i) => i.clone(),
            None => return false,
        };
        candidate.state = state;
        candidate.decided = decided;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[self.current] = candidate;
        self.current += 1;
        true
    }

    pub fn set_format(&mut self, id: &str, format: ProjectionFormat) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.format = format;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].format = format;
        true
    }

    pub fn set_view(&mut self, id: &str, view: ViewMode) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.view = view;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].view = view;
        true
    }

    pub fn set_scale(&mut self, id: &str, scale: u32) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.scale = scale;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].scale = scale;
        true
    }

    pub fn set_state(&mut self, id: &str, state: PreviewState) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.state = state;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].state = state;
        true
    }

    pub fn set_decided(&mut self, id: &str, decided: bool) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.decided = decided;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].decided = decided;
        true
    }

    pub fn set_path(&mut self, id: &str, path: &str) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        let Some(p) = validate_entry_path(path) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.path = p.clone();
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].path = p;
        true
    }

    pub fn remove_entry(&mut self, id: &str) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        self.entries.remove(pos);
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
            .with("previewed", &self.previewed_count().to_string())
            .with("closed", &self.closed_count().to_string())
            .with("primary", &self.by_format(ProjectionFormat::Primary).len().to_string())
            .with("secondary", &self.by_format(ProjectionFormat::Secondary).len().to_string())
            .with("formats", &FORMATS.len().to_string())
            .with("views", &VIEWS.len().to_string())
            .with("states", &STATES.len().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    ProjectionSession::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use serde_json::from_str;
    use std::path::PathBuf;
    use std::sync::atomic::{AtomicUsize, Ordering};

    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu090-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    fn load(dir: &Path, raw: &str) -> (ProjectionSession, Vec<String>) {
        fs::create_dir_all(dir).unwrap();
        fs::write(dir.join(PROJECTION_FILE), raw).unwrap();
        ProjectionSession::open(Some(dir))
    }

    fn entry() -> &'static str {
        r#"{"id":"p1","format":"primary","path":"primary/a","view":"fit","scale":100,"state":"pending","decided":false}"#
    }

    fn one() -> String {
        format!("{{\"schema\":1,\"current\":0,\"entries\":[{}]}}", entry())
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"current":0,"entries":[]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 3);
        assert_eq!(v["entries"].as_array().unwrap().len(), 0);
        assert_eq!(v["current"], 0);
    }

    #[test]
    fn tables_and_enum_codes_are_explicit() {
        assert_eq!(ProjectionFormat::Primary.code(), "primary");
        assert_eq!(ProjectionFormat::Secondary.code(), "secondary");
        assert_eq!(ProjectionFormat::parse("nope"), None);
        assert_eq!(ViewMode::Fit.code(), "fit");
        assert_eq!(ViewMode::Original.code(), "original");
        assert_eq!(ViewMode::Scaled.code(), "scaled");
        assert_eq!(ViewMode::parse("nope"), None);
        assert_eq!(PreviewState::Pending.code(), "pending");
        assert_eq!(PreviewState::Previewed.code(), "previewed");
        assert_eq!(PreviewState::Closed.code(), "closed");
        assert_eq!(PreviewState::parse("nope"), None);
        assert_eq!(ROOT_KEYS.len(), 3);
        assert_eq!(ENTRY_KEYS.len(), 7);
        assert_eq!(FORMATS.len(), 2);
        assert_eq!(VIEWS.len(), 3);
        assert_eq!(STATES.len(), 3);
        assert_eq!(PATH_KINDS.len(), 2);
        assert_eq!(MIN_SCALE, 25);
        assert_eq!(MAX_SCALE, 400);
        assert_eq!(DEFAULT_SCALE, 100);
    }

    #[test]
    fn both_format_slots_are_registered() {
        assert!(FORMATS.contains(&"primary"));
        assert!(FORMATS.contains(&"secondary"));
        assert_eq!(classify_path("primary/a"), ProjectionFormat::Primary);
        assert_eq!(classify_path("secondary/b"), ProjectionFormat::Secondary);
    }

    #[test]
    fn default_is_empty_session() {
        let (p, lines) = ProjectionSession::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, ProjectionSession::default());
        assert_eq!(p.current, 0);
        assert_eq!(p.page_count(), 0);
        assert_eq!(p.pending_count(), 0);
        assert_eq!(p.previewed_count(), 0);
        assert_eq!(p.closed_count(), 0);
        assert_eq!(p.summary(), [0, 0, 0]);
        assert!(p.current_entry().is_none());
    }

    #[test]
    fn path_rejects_parent_dir() {
        assert_eq!(validate_entry_path("primary/../secondary/a"), None);
    }

    #[test]
    fn path_rejects_root_dir() {
        assert_eq!(validate_entry_path("/primary/a"), None);
    }

    #[test]
    fn path_rejects_cur_dir() {
        assert_eq!(validate_entry_path("./primary/a"), None);
    }

    #[test]
    fn path_rejects_windows_prefix_form() {
        assert_eq!(validate_entry_path("C:/primary/a"), None);
    }

    #[test]
    fn path_rejects_control_and_empty() {
        assert_eq!(validate_entry_path(""), None);
        assert_eq!(validate_entry_path("primary/a\nb"), None);
        assert_eq!(validate_entry_path("other/a"), None);
    }

    #[test]
    fn path_rejects_too_deep() {
        let deep = "primary/".to_string() + &"d/".repeat(robust::MAX_REL_DEPTH + 1);
        assert_eq!(validate_entry_path(&deep), None);
    }

    #[test]
    fn path_accepts_normal_relative() {
        assert_eq!(validate_entry_path("primary/a"), Some("primary/a".to_string()));
        assert_eq!(validate_entry_path("secondary/x/y"), Some("secondary/x/y".to_string()));
    }

    #[test]
    fn classify_maps_known_prefixes() {
        assert_eq!(classify_path("primary/a/b"), ProjectionFormat::Primary);
        assert_eq!(classify_path("secondary/a"), ProjectionFormat::Secondary);
    }

    #[test]
    fn parse_rejects_unknown_root_key() {
        let r = tmp();
        let raw = one().replace("\"schema\":1", "\"schema\":1,\"extra\":1");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, ProjectionSession::default());
        assert!(lines.iter().any(|l| l.contains("unknown_key")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_unknown_entry_key() {
        let r = tmp();
        let raw = one().replace("\"entries\":[{", "\"entries\":[{\"extra\":1,");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, ProjectionSession::default());
        assert!(lines.iter().any(|l| l.contains("entry_unknown_key")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_path_escape() {
        let r = tmp();
        let raw = one().replace("\"path\":\"primary/a\"", "\"path\":\"primary/../b\"");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, ProjectionSession::default());
        assert!(lines.iter().any(|l| l.contains("path_escapes_root")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_duplicate_id() {
        let r = tmp();
        let raw = format!("{{\"schema\":1,\"current\":0,\"entries\":[{},{}]}}", entry(), entry());
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, ProjectionSession::default());
        assert!(lines.iter().any(|l| l.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_current_out_of_range() {
        let r = tmp();
        let raw = one().replace("\"current\":0", "\"current\":5");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, ProjectionSession::default());
        assert!(lines.iter().any(|l| l.contains("current_out_of_range")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_schema_invalid() {
        let r = tmp();
        let raw = one().replace("\"schema\":1", "\"schema\":2");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, ProjectionSession::default());
        assert!(lines.iter().any(|l| l.contains("schema_invalid")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_format_path_mismatch() {
        let r = tmp();
        let raw = one().replace("\"format\":\"primary\"", "\"format\":\"secondary\"");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, ProjectionSession::default());
        assert!(lines.iter().any(|l| l.contains("bad_entry_state")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_accepts_well_formed_entry() {
        let r = tmp();
        let (p, lines) = load(&r, &one());
        assert_eq!(p.entries.len(), 1);
        assert_eq!(p.entries[0].format, ProjectionFormat::Primary);
        assert_eq!(p.entries[0].view, ViewMode::Fit);
        assert_eq!(p.entries[0].scale, DEFAULT_SCALE);
        assert!(lines.is_empty());
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_root_inputs_return_to_default() {
        let r = tmp();
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            one().replace("\"current\":0", "\"current\":-1"),
            one().replace("\"entries\":[", "\"entries\":[null,"),
            one().replace("\"entries\":[", "\"entries\":7,\"x\":["),
            one().replace("\"scale\":100", "\"scale\":\"no\""),
            one().replace("\"decided\":false", "\"decided\":7"),
            one().replace("\"view\":\"fit\"", "\"view\":\"nope\""),
            one().replace("\"state\":\"pending\"", "\"state\":\"nope\""),
            one().replace("\"format\":\"primary\"", "\"format\":\"nope\""),
            one().replace("\"id\":\"p1\"", "\"id\":\"\""),
            one().replace("\"id\":\"p1\"", "\"id\":\"a\\nb\""),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, ProjectionSession::default(), "case={}", &raw[..raw.len().min(48)]);
            assert!(lines.iter().any(|l| l.contains("DEGRADE")), "case={}", &raw[..raw.len().min(48)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn contradiction_states_are_rejected_on_load() {
        let r = tmp();
        let cases = vec![
            one().replace("\"state\":\"pending\"", "\"state\":\"closed\""),
            one().replace("\"decided\":false", "\"decided\":true"),
            one().replace("\"view\":\"fit\"", "\"view\":\"scaled\"").replace("\"scale\":100", "\"scale\":9"),
            one().replace("\"scale\":100", "\"scale\":150"),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, ProjectionSession::default());
            assert!(lines.iter().any(|l| l.contains("DEGRADE")));
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn add_entry_single_and_resolve_advances_one() {
        let mut p = ProjectionSession::default();
        assert!(p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert_eq!(p.page_count(), 1);
        assert!(p.resolve_current(PreviewState::Previewed, true));
        assert_eq!(p.current, 1);
        assert_eq!(p.previewed_count(), 1);
        assert!(!p.resolve_current(PreviewState::Previewed, true));
    }

    #[test]
    fn append_entry_requires_pending() {
        let mut p = ProjectionSession::default();
        assert!(!p.append_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert!(p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert!(p.append_entry("p2", ProjectionFormat::Secondary, "secondary/b", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert_eq!(p.page_count(), 2);
    }

    #[test]
    fn set_view_updates_one_entry() {
        let mut p = ProjectionSession::default();
        assert!(p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert!(p.set_view("p1", ViewMode::Scaled));
        assert!(p.set_scale("p1", 200));
        assert_eq!(p.entries[0].scale, 200);
        assert!(!p.set_scale("p1", 9));
        assert!(!p.set_view("p1", ViewMode::Fit));
    }

    #[test]
    fn scaled_view_requires_in_range_scale() {
        let mut p = ProjectionSession::default();
        assert!(!p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Scaled, 9, PreviewState::Pending, false));
        assert!(!p.add_entry("p2", ProjectionFormat::Primary, "primary/b", ViewMode::Scaled, 401, PreviewState::Pending, false));
        assert!(p.add_entry("p3", ProjectionFormat::Primary, "primary/c", ViewMode::Scaled, 200, PreviewState::Pending, false));
    }

    #[test]
    fn closed_requires_decided() {
        let mut p = ProjectionSession::default();
        assert!(!p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Closed, false));
        assert!(p.add_entry("p2", ProjectionFormat::Primary, "primary/b", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Closed, true));
        assert!(!p.set_decided("p2", false));
    }

    #[test]
    fn format_change_must_match_path() {
        let mut p = ProjectionSession::default();
        assert!(p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert!(!p.set_format("p1", ProjectionFormat::Secondary));
        assert!(!p.set_path("p1", "secondary/b"));
        assert!(p.add_entry("p2", ProjectionFormat::Secondary, "secondary/b", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert_eq!(p.by_format(ProjectionFormat::Secondary), vec!["p2"]);
        assert_eq!(p.by_format(ProjectionFormat::Primary), vec!["p1"]);
        assert_eq!(p.summary(), [1, 1, 2]);
    }

    #[test]
    fn serialize_roundtrip_is_byte_stable() {
        let mut p = ProjectionSession::default();
        assert!(p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert!(p.add_entry("p2", ProjectionFormat::Secondary, "secondary/b", ViewMode::Original, DEFAULT_SCALE, PreviewState::Previewed, true));
        let body = serialize(&p).unwrap();
        let (q, lines) = parse(&body);
        assert!(lines.is_empty());
        assert_eq!(p, q);
        assert_eq!(serialize(&q).unwrap(), body);
    }

    #[test]
    fn change_event_payload_has_no_user_text() {
        let mut p = ProjectionSession::default();
        assert!(p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        let e = p.change_event();
        assert_eq!(e.payload.len(), 10);
        for key in ["id", "path", "title", "body"] {
            assert_eq!(e.field(key), None);
        }
        assert_eq!(e.field("formats"), Some("2"));
        assert_eq!(e.field("states"), Some("3"));
    }

    #[test]
    fn persist_without_root_reports_no_root() {
        let p = ProjectionSession::default();
        let lines = p.persist(None);
        assert_eq!(lines.len(), 1);
        assert!(lines[0].contains("no_root"));
    }

    #[test]
    fn persist_and_reload_preserves_two_slots() {
        let r = tmp();
        let mut p = ProjectionSession::default();
        assert!(p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert!(p.add_entry("p2", ProjectionFormat::Secondary, "secondary/b", ViewMode::Original, DEFAULT_SCALE, PreviewState::Previewed, true));
        assert!(p.persist(Some(&r)).is_empty());
        let (q, lines) = ProjectionSession::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(p, q);
        assert_eq!(q.summary(), [1, 1, 2]);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn open_without_root_is_in_memory() {
        let (p, lines) = ProjectionSession::open(None);
        assert_eq!(p, ProjectionSession::default());
        assert!(lines.iter().any(|l| l.contains("in_memory")));
    }

    #[test]
    fn remove_entry_clamps_current() {
        let mut p = ProjectionSession::default();
        assert!(p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert!(p.add_entry("p2", ProjectionFormat::Secondary, "secondary/b", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert!(p.resolve_current(PreviewState::Previewed, true));
        assert!(p.resolve_current(PreviewState::Previewed, true));
        assert_eq!(p.current, 2);
        assert!(p.remove_entry("p1"));
        assert!(p.remove_entry("p2"));
        assert_eq!(p.current, 0);
        assert_eq!(p.page_count(), 0);
    }

    #[test]
    fn protected_state_files_are_not_projection_files() {
        assert!(!PROTECTED_FILES.iter().any(|f| *f == PROJECTION_FILE));
        let r = tmp();
        let mut p = ProjectionSession::default();
        assert!(p.add_entry("p1", ProjectionFormat::Primary, "primary/a", ViewMode::Fit, DEFAULT_SCALE, PreviewState::Pending, false));
        assert!(p.persist(Some(&r)).is_empty());
        for name in PROTECTED_FILES {
            assert!(!r.join(name).exists());
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn too_many_entries_are_rejected() {
        let r = tmp();
        let many = format!("{{\"schema\":1,\"current\":0,\"entries\":[{}]}}",
            (0..MAX_ENTRIES + 1).map(|i| format!("{{\"id\":\"p{}\",\"format\":\"primary\",\"path\":\"primary/a{}\",\"view\":\"fit\",\"scale\":100,\"state\":\"pending\",\"decided\":false}}", i, i)).collect::<Vec<_>>().join(","));
        let (p, lines) = load(&r, &many);
        assert_eq!(p, ProjectionSession::default());
        assert!(lines.iter().any(|l| l.contains("entries_too_many")));
        let _ = fs::remove_dir_all(&r);
    }
}

use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::{Component, Path};

pub const STUDIO_IMAGE_FILE: &str = "studio-image.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"session":"draft","entries":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_ENTRIES: usize = 24;
pub const MIN_PIXEL: u32 = 16;
pub const MAX_PIXEL: u32 = 1024;
pub const DEFAULT_PIXEL: u32 = 64;
pub const EVENT_TARGET: &str = "studio.image";
pub const ROOT_KEYS: &[&str] = &["schema", "session", "entries"];
pub const ENTRY_KEYS: &[&str] = &["id", "format", "path", "target_px", "fit", "state", "decided"];
pub const IMAGE_FORMATS: &[&str] = &["png", "gif", "svg", "opaque"];
pub const STATES: &[&str] = &["draft", "adjusted", "closed"];
pub const PATH_KINDS: &[(&str, &str)] = &[
    ("logo", "logo"),
    ("icon", "icon"),
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ImageFormat {
    Png,
    Gif,
    Svg,
    Opaque,
}

impl ImageFormat {
    pub fn code(&self) -> &'static str {
        match self {
            ImageFormat::Png => "png",
            ImageFormat::Gif => "gif",
            ImageFormat::Svg => "svg",
            ImageFormat::Opaque => "opaque",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "png" => Some(ImageFormat::Png),
            "gif" => Some(ImageFormat::Gif),
            "svg" => Some(ImageFormat::Svg),
            "opaque" => Some(ImageFormat::Opaque),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EditState {
    Draft,
    Adjusted,
    Closed,
}

impl EditState {
    pub fn code(&self) -> &'static str {
        match self {
            EditState::Draft => "draft",
            EditState::Adjusted => "adjusted",
            EditState::Closed => "closed",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "draft" => Some(EditState::Draft),
            "adjusted" => Some(EditState::Adjusted),
            "closed" => Some(EditState::Closed),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ImageEntry {
    pub id: String,
    pub format: ImageFormat,
    pub path: String,
    pub target_px: u32,
    pub fit: bool,
    pub state: EditState,
    pub decided: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StudioImage {
    pub session: EditState,
    pub entries: Vec<ImageEntry>,
}

impl Default for StudioImage {
    fn default() -> Self {
        StudioImage { session: EditState::Draft, entries: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("studio", action, "image", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("studio", action, "image", "ERROR", reason)
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

fn classify_target(path: &str) -> &'static str {
    let first = match path.split('/').next() {
        Some(v) => v,
        None => return "logo",
    };
    for (prefix, code) in PATH_KINDS {
        if *prefix == first {
            return *code;
        }
    }
    "logo"
}

fn entry_consistent(i: &ImageEntry) -> bool {
    if i.state == EditState::Closed && !i.decided {
        return false;
    }
    if i.decided && i.state == EditState::Draft {
        return false;
    }
    if i.state == EditState::Adjusted && !i.fit {
        return false;
    }
    if i.format == ImageFormat::Opaque && i.fit {
        return false;
    }
    if i.target_px < MIN_PIXEL || i.target_px > MAX_PIXEL {
        return false;
    }
    true
}

fn parse(raw: &str) -> (StudioImage, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (StudioImage::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (StudioImage::default(), lines);
        }
    };
    if obj.keys().any(|k| !ROOT_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (StudioImage::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (StudioImage::default(), lines);
    }
    let session = match obj.get("session").and_then(Value::as_str).and_then(EditState::parse) {
        Some(s) => s,
        None => {
            lines.push(degrade("load", "bad_session"));
            return (StudioImage::default(), lines);
        }
    };
    let arr = match obj.get("entries").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "entries_not_array"));
            return (StudioImage::default(), lines);
        }
    };
    if arr.len() > MAX_ENTRIES {
        lines.push(degrade("load", "entries_too_many"));
        return (StudioImage::default(), lines);
    }
    let mut items: Vec<ImageEntry> = Vec::new();
    for item in arr {
        let io = match item.as_object() {
            Some(o) => o,
            None => {
                lines.push(degrade("load", "entry_not_object"));
                return (StudioImage::default(), lines);
            }
        };
        if io.keys().any(|k| !ENTRY_KEYS.contains(&k.as_str())) {
            lines.push(degrade("load", "entry_unknown_key"));
            return (StudioImage::default(), lines);
        }
        let id = match io.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "id_too_large"));
                return (StudioImage::default(), lines);
            }
            _ => {
                lines.push(degrade("load", "bad_id"));
                return (StudioImage::default(), lines);
            }
        };
        if items.iter().any(|e| e.id == id) {
            lines.push(degrade("load", "duplicate_id"));
            return (StudioImage::default(), lines);
        }
        let format = match io.get("format").and_then(Value::as_str).and_then(ImageFormat::parse) {
            Some(f) => f,
            None => {
                lines.push(degrade("load", "bad_format"));
                return (StudioImage::default(), lines);
            }
        };
        let path = match io.get("path").and_then(Value::as_str).and_then(validate_entry_path) {
            Some(p) => p,
            None => {
                lines.push(degrade("load", "path_escapes_root"));
                return (StudioImage::default(), lines);
            }
        };
        let target_px = match io.get("target_px").and_then(Value::as_u64) {
            Some(v) if v <= u32::MAX as u64 => v as u32,
            _ => {
                lines.push(degrade("load", "bad_target_px"));
                return (StudioImage::default(), lines);
            }
        };
        let fit = match io.get("fit").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("load", "bad_fit"));
                return (StudioImage::default(), lines);
            }
        };
        let state = match io.get("state").and_then(Value::as_str).and_then(EditState::parse) {
            Some(s) => s,
            None => {
                lines.push(degrade("load", "bad_state"));
                return (StudioImage::default(), lines);
            }
        };
        let decided = match io.get("decided").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("load", "bad_decided"));
                return (StudioImage::default(), lines);
            }
        };
        let e = ImageEntry { id, format, path, target_px, fit, state, decided };
        if !entry_consistent(&e) {
            lines.push(degrade("load", "bad_entry_state"));
            return (StudioImage::default(), lines);
        }
        items.push(e);
    }
    (StudioImage { session, entries: items }, lines)
}

fn serialize(p: &StudioImage) -> Result<String> {
    let entries: Vec<Value> = p.entries.iter().map(|i| json!({
        "id": i.id,
        "format": i.format.code(),
        "path": i.path,
        "target_px": i.target_px,
        "fit": i.fit,
        "state": i.state.code(),
        "decided": i.decided,
    })).collect();
    Ok(to_string(&json!({
        "schema": 1,
        "session": p.session.code(),
        "entries": entries,
    }))?)
}

fn write(root: &Path, p: &StudioImage) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, STUDIO_IMAGE_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", STUDIO_IMAGE_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl StudioImage {
    pub fn open(root: Option<&Path>) -> (StudioImage, Vec<String>) {
        let Some(dir) = root else {
            return (StudioImage::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, STUDIO_IMAGE_FILE) {
            Ok(p) => p,
            Err(_) => return (StudioImage::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (StudioImage::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (StudioImage::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn entry_count(&self) -> usize {
        self.entries.len()
    }

    pub fn draft_count(&self) -> usize {
        self.entries.iter().filter(|i| i.state == EditState::Draft).count()
    }

    pub fn adjusted_count(&self) -> usize {
        self.entries.iter().filter(|i| i.state == EditState::Adjusted).count()
    }

    pub fn closed_count(&self) -> usize {
        self.entries.iter().filter(|i| i.state == EditState::Closed).count()
    }

    pub fn by_format(&self, format: ImageFormat) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for i in &self.entries {
            if i.format == format {
                out.push(i.id.as_str());
            }
        }
        out
    }

    pub fn by_target(&self, target: &str) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for i in &self.entries {
            if classify_target(&i.path) == target {
                out.push(i.id.as_str());
            }
        }
        out
    }

    pub fn format_for(&self, id: &str) -> Option<&str> {
        self.entries.iter().find(|i| i.id == id).map(|i| i.format.code())
    }

    pub fn summary(&self) -> [usize; 3] {
        let mut out: [usize; 3] = [0, 0, 0];
        for i in &self.entries {
            if classify_target(&i.path) == "logo" {
                out[0] += 1;
            } else {
                out[1] += 1;
            }
            out[2] += 1;
        }
        out
    }

    pub fn add_entry(&mut self, id: &str, format: ImageFormat, path: &str, target_px: u32, fit: bool, state: EditState, decided: bool) -> bool {
        if self.entries.len() >= MAX_ENTRIES || !valid_id(id) || self.entries.iter().any(|i| i.id == id) {
            return false;
        }
        if !IMAGE_FORMATS.contains(&format.code()) || !STATES.contains(&state.code()) {
            return false;
        }
        let Some(p) = validate_entry_path(path) else { return false };
        let e = ImageEntry {
            id: id.to_string(),
            format,
            path: p,
            target_px,
            fit,
            state,
            decided,
        };
        if !entry_consistent(&e) {
            return false;
        }
        self.entries.push(e);
        true
    }

    pub fn set_format(&mut self, id: &str, format: ImageFormat) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.format = format;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].format = format;
        true
    }

    pub fn set_target_px(&mut self, id: &str, target_px: u32) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.target_px = target_px;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].target_px = target_px;
        true
    }

    pub fn set_fit(&mut self, id: &str, fit: bool) -> bool {
        let Some(pos) = self.entries.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.entries[pos].clone();
        candidate.fit = fit;
        if !entry_consistent(&candidate) {
            return false;
        }
        self.entries[pos].fit = fit;
        true
    }

    pub fn set_state(&mut self, id: &str, state: EditState) -> bool {
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
            .with("entries", &self.entry_count().to_string())
            .with("session", self.session.code())
            .with("draft", &self.draft_count().to_string())
            .with("adjusted", &self.adjusted_count().to_string())
            .with("closed", &self.closed_count().to_string())
            .with("logo", &self.by_target("logo").len().to_string())
            .with("icon", &self.by_target("icon").len().to_string())
            .with("formats", &IMAGE_FORMATS.len().to_string())
            .with("targets", &PATH_KINDS.len().to_string())
            .with("pixel_bounds", &format!("{}-{}", MIN_PIXEL, MAX_PIXEL))
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    StudioImage::default().persist(root)
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
        let p = std::env::temp_dir().join(format!("kcu091-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    fn load(dir: &Path, raw: &str) -> (StudioImage, Vec<String>) {
        fs::create_dir_all(dir).unwrap();
        fs::write(dir.join(STUDIO_IMAGE_FILE), raw).unwrap();
        StudioImage::open(Some(dir))
    }

    fn entry() -> &'static str {
        r#"{"id":"i1","format":"png","path":"logo/a","target_px":64,"fit":true,"state":"draft","decided":false}"#
    }

    fn one() -> String {
        format!("{{\"schema\":1,\"session\":\"draft\",\"entries\":[{}]}}", entry())
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
    fn tables_and_enum_codes_are_explicit() {
        assert_eq!(ImageFormat::Png.code(), "png");
        assert_eq!(ImageFormat::Gif.code(), "gif");
        assert_eq!(ImageFormat::Svg.code(), "svg");
        assert_eq!(ImageFormat::Opaque.code(), "opaque");
        assert_eq!(ImageFormat::parse("nope"), None);
        assert_eq!(EditState::Draft.code(), "draft");
        assert_eq!(EditState::Adjusted.code(), "adjusted");
        assert_eq!(EditState::Closed.code(), "closed");
        assert_eq!(EditState::parse("nope"), None);
        assert_eq!(ROOT_KEYS.len(), 3);
        assert_eq!(ENTRY_KEYS.len(), 7);
        assert_eq!(IMAGE_FORMATS.len(), 4);
        assert_eq!(STATES.len(), 3);
        assert_eq!(PATH_KINDS.len(), 2);
        assert_eq!(MIN_PIXEL, 16);
        assert_eq!(MAX_PIXEL, 1024);
        assert_eq!(DEFAULT_PIXEL, 64);
    }

    #[test]
    fn two_target_slots_are_registered() {
        assert_eq!(classify_target("logo/a"), "logo");
        assert_eq!(classify_target("icon/b"), "icon");
        assert!(IMAGE_FORMATS.contains(&"png"));
        assert!(IMAGE_FORMATS.contains(&"gif"));
        assert!(IMAGE_FORMATS.contains(&"svg"));
        assert!(IMAGE_FORMATS.contains(&"opaque"));
    }

    #[test]
    fn default_is_empty_session() {
        let (p, lines) = StudioImage::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, StudioImage::default());
        assert_eq!(p.session, EditState::Draft);
        assert_eq!(p.entry_count(), 0);
        assert_eq!(p.draft_count(), 0);
        assert_eq!(p.adjusted_count(), 0);
        assert_eq!(p.closed_count(), 0);
        assert_eq!(p.summary(), [0, 0, 0]);
        assert_eq!(p.by_format(ImageFormat::Png), Vec::<&str>::new());
    }

    #[test]
    fn path_rejects_parent_dir() {
        assert_eq!(validate_entry_path("logo/../icon/a"), None);
    }

    #[test]
    fn path_rejects_root_dir() {
        assert_eq!(validate_entry_path("/logo/a"), None);
    }

    #[test]
    fn path_rejects_cur_dir() {
        assert_eq!(validate_entry_path("./logo/a"), None);
    }

    #[test]
    fn path_rejects_windows_prefix_form() {
        assert_eq!(validate_entry_path("C:/logo/a"), None);
    }

    #[test]
    fn path_rejects_control_and_empty() {
        assert_eq!(validate_entry_path(""), None);
        assert_eq!(validate_entry_path("logo/a\nb"), None);
        assert_eq!(validate_entry_path("other/a"), None);
    }

    #[test]
    fn path_rejects_too_deep() {
        let deep = "logo/".to_string() + &"d/".repeat(robust::MAX_REL_DEPTH + 1);
        assert_eq!(validate_entry_path(&deep), None);
    }

    #[test]
    fn path_accepts_normal_relative() {
        assert_eq!(validate_entry_path("logo/a"), Some("logo/a".to_string()));
        assert_eq!(validate_entry_path("icon/x/y"), Some("icon/x/y".to_string()));
    }

    #[test]
    fn parse_rejects_unknown_root_key() {
        let r = tmp();
        let raw = one().replace("\"schema\":1", "\"schema\":1,\"extra\":1");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, StudioImage::default());
        assert!(lines.iter().any(|l| l.contains("unknown_key")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_unknown_entry_key() {
        let r = tmp();
        let raw = one().replace("\"entries\":[{", "\"entries\":[{\"extra\":1,");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, StudioImage::default());
        assert!(lines.iter().any(|l| l.contains("entry_unknown_key")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_path_escape() {
        let r = tmp();
        let raw = one().replace("\"path\":\"logo/a\"", "\"path\":\"logo/../b\"");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, StudioImage::default());
        assert!(lines.iter().any(|l| l.contains("path_escapes_root")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_duplicate_id() {
        let r = tmp();
        let raw = format!("{{\"schema\":1,\"session\":\"draft\",\"entries\":[{},{}]}}", entry(), entry());
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, StudioImage::default());
        assert!(lines.iter().any(|l| l.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_rejects_schema_invalid() {
        let r = tmp();
        let raw = one().replace("\"schema\":1", "\"schema\":2");
        let (p, lines) = load(&r, &raw);
        assert_eq!(p, StudioImage::default());
        assert!(lines.iter().any(|l| l.contains("schema_invalid")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_accepts_well_formed_entry() {
        let r = tmp();
        let (p, lines) = load(&r, &one());
        assert_eq!(p.entries.len(), 1);
        assert_eq!(p.entries[0].format, ImageFormat::Png);
        assert_eq!(p.entries[0].target_px, DEFAULT_PIXEL);
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
            one().replace("\"session\":\"draft\"", "\"session\":\"nope\""),
            one().replace("\"entries\":[", "\"entries\":[null,"),
            one().replace("\"target_px\":64", "\"target_px\":\"no\""),
            one().replace("\"fit\":true", "\"fit\":7"),
            one().replace("\"decided\":false", "\"decided\":7"),
            one().replace("\"format\":\"png\"", "\"format\":\"nope\""),
            one().replace("\"state\":\"draft\"", "\"state\":\"nope\""),
            one().replace("\"id\":\"i1\"", "\"id\":\"\""),
            one().replace("\"id\":\"i1\"", "\"id\":\"a\\nb\""),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, StudioImage::default(), "case={}", &raw[..raw.len().min(48)]);
            assert!(lines.iter().any(|l| l.contains("DEGRADE")), "case={}", &raw[..raw.len().min(48)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn contradiction_states_are_rejected_on_load() {
        let r = tmp();
        let cases = vec![
            one().replace("\"state\":\"draft\"", "\"state\":\"closed\""),
            one().replace("\"decided\":false", "\"decided\":true"),
            one().replace("\"format\":\"png\"", "\"format\":\"opaque\""),
            one().replace("\"fit\":true", "\"fit\":false").replace("\"state\":\"draft\"", "\"state\":\"adjusted\""),
            one().replace("\"target_px\":64", "\"target_px\":9"),
            one().replace("\"target_px\":64", "\"target_px\":2048"),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, StudioImage::default());
            assert!(lines.iter().any(|l| l.contains("DEGRADE")));
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn add_entry_single_and_setters_are_bounded() {
        let mut p = StudioImage::default();
        assert!(p.add_entry("i1", ImageFormat::Png, "logo/a", DEFAULT_PIXEL, true, EditState::Draft, false));
        assert_eq!(p.entry_count(), 1);
        assert!(p.set_target_px("i1", 128));
        assert_eq!(p.entries[0].target_px, 128);
        assert!(!p.set_target_px("i1", 9));
        assert!(!p.set_target_px("i1", 2048));
        assert!(p.set_fit("i1", false));
        assert!(!p.set_state("i1", EditState::Adjusted));
        assert!(p.set_fit("i1", true));
        assert!(p.set_state("i1", EditState::Adjusted));
        assert!(!p.set_fit("i1", false));
        assert!(p.set_format("i1", ImageFormat::Gif));
        assert_eq!(p.format_for("i1"), Some("gif"));
        assert!(!p.add_entry("i1", ImageFormat::Png, "icon/b", DEFAULT_PIXEL, true, EditState::Draft, false));
    }

    #[test]
    fn target_migration_and_close_are_separate() {
        let mut p = StudioImage::default();
        assert!(p.add_entry("i1", ImageFormat::Png, "logo/a", DEFAULT_PIXEL, true, EditState::Draft, false));
        assert!(p.set_path("i1", "icon/b"));
        assert_eq!(p.by_target("icon"), vec!["i1"]);
        assert!(p.set_state("i1", EditState::Adjusted));
        assert!(p.set_decided("i1", true));
        assert!(p.set_state("i1", EditState::Closed));
        assert_eq!(p.closed_count(), 1);
        assert!(!p.set_decided("i1", false));
        assert!(p.remove_entry("i1"));
        assert_eq!(p.entry_count(), 0);
    }

    #[test]
    fn serialize_roundtrip_is_byte_stable() {
        let mut p = StudioImage::default();
        assert!(p.add_entry("i1", ImageFormat::Png, "logo/a", DEFAULT_PIXEL, true, EditState::Draft, false));
        assert!(p.add_entry("i2", ImageFormat::Svg, "icon/b", 128, true, EditState::Adjusted, true));
        let body = serialize(&p).unwrap();
        let (q, lines) = parse(&body);
        assert!(lines.is_empty());
        assert_eq!(p, q);
        assert_eq!(serialize(&q).unwrap(), body);
    }

    #[test]
    fn change_event_payload_has_no_user_text() {
        let mut p = StudioImage::default();
        assert!(p.add_entry("i1", ImageFormat::Png, "logo/a", DEFAULT_PIXEL, true, EditState::Draft, false));
        let e = p.change_event();
        assert_eq!(e.payload.len(), 10);
        for key in ["id", "path", "title", "body"] {
            assert_eq!(e.field(key), None);
        }
        assert_eq!(e.field("formats"), Some("4"));
        assert_eq!(e.field("targets"), Some("2"));
    }

    #[test]
    fn persist_without_root_reports_no_root() {
        let p = StudioImage::default();
        let lines = p.persist(None);
        assert_eq!(lines.len(), 1);
        assert!(lines[0].contains("no_root"));
    }

    #[test]
    fn persist_and_reload_preserves_two_slots() {
        let r = tmp();
        let mut p = StudioImage::default();
        assert!(p.add_entry("i1", ImageFormat::Png, "logo/a", DEFAULT_PIXEL, true, EditState::Draft, false));
        assert!(p.add_entry("i2", ImageFormat::Gif, "icon/b", 128, true, EditState::Adjusted, true));
        assert!(p.persist(Some(&r)).is_empty());
        let (q, lines) = StudioImage::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(p, q);
        assert_eq!(q.summary(), [1, 1, 2]);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn open_without_root_is_in_memory() {
        let (p, lines) = StudioImage::open(None);
        assert_eq!(p, StudioImage::default());
        assert!(lines.iter().any(|l| l.contains("in_memory")));
    }

    #[test]
    fn protected_state_files_are_not_studio_files() {
        assert!(!PROTECTED_FILES.iter().any(|f| *f == STUDIO_IMAGE_FILE));
        let r = tmp();
        let mut p = StudioImage::default();
        assert!(p.add_entry("i1", ImageFormat::Png, "logo/a", DEFAULT_PIXEL, true, EditState::Draft, false));
        assert!(p.persist(Some(&r)).is_empty());
        for name in PROTECTED_FILES {
            assert!(!r.join(name).exists());
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn opaque_format_rejects_automatic_pixel_fit() {
        let mut p = StudioImage::default();
        assert!(!p.add_entry("i1", ImageFormat::Opaque, "logo/a", DEFAULT_PIXEL, true, EditState::Draft, false));
        assert!(p.add_entry("i2", ImageFormat::Opaque, "logo/b", DEFAULT_PIXEL, false, EditState::Draft, false));
        assert!(!p.set_fit("i2", true));
        assert_eq!(p.by_format(ImageFormat::Opaque), vec!["i2"]);
    }

    #[test]
    fn too_many_entries_are_rejected() {
        let r = tmp();
        let many = format!("{{\"schema\":1,\"session\":\"draft\",\"entries\":[{}]}}",
            (0..MAX_ENTRIES + 1).map(|i| format!("{{\"id\":\"i{}\",\"format\":\"png\",\"path\":\"logo/a{}\",\"target_px\":64,\"fit\":true,\"state\":\"draft\",\"decided\":false}}", i, i)).collect::<Vec<_>>().join(","));
        let (p, lines) = load(&r, &many);
        assert_eq!(p, StudioImage::default());
        assert!(lines.iter().any(|l| l.contains("entries_too_many")));
        let _ = fs::remove_dir_all(&r);
    }
}

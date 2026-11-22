use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const GENERATOR_SESSION_FILE: &str = "generator-session.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"format":"legacy","sessions":[],"translations":[],"history":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_SESSIONS: usize = 24;
pub const MAX_TRANSLATIONS: usize = 64;
pub const MAX_HISTORY: usize = 32;
pub const EVENT_TARGET: &str = "lab.generators";
pub const KNOWN_KEYS: &[&str] = &["schema", "format", "sessions", "translations", "history"];
pub const SESSION_KEYS: &[&str] = &["id", "kind", "format", "input", "result", "state"];
pub const TRANSLATION_KEYS: &[&str] = &["id", "key", "value", "enabled"];
pub const KINDS: &[&str] = &["recipe", "gradient", "mod_translation"];
pub const FORMATS: &[&str] = &["legacy", "json"];
pub const STATES: &[&str] = &["draft", "ready", "archived"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GeneratorKind {
    Recipe,
    Gradient,
    ModTranslation,
}

impl GeneratorKind {
    pub fn code(&self) -> &'static str {
        match self {
            GeneratorKind::Recipe => "recipe",
            GeneratorKind::Gradient => "gradient",
            GeneratorKind::ModTranslation => "mod_translation",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "recipe" => Some(GeneratorKind::Recipe),
            "gradient" => Some(GeneratorKind::Gradient),
            "mod_translation" => Some(GeneratorKind::ModTranslation),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OutputFormat {
    Legacy,
    Json,
}

impl OutputFormat {
    pub fn code(&self) -> &'static str {
        match self {
            OutputFormat::Legacy => "legacy",
            OutputFormat::Json => "json",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "legacy" => Some(OutputFormat::Legacy),
            "json" => Some(OutputFormat::Json),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SessionState {
    Draft,
    Ready,
    Archived,
}

impl SessionState {
    pub fn code(&self) -> &'static str {
        match self {
            SessionState::Draft => "draft",
            SessionState::Ready => "ready",
            SessionState::Archived => "archived",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "draft" => Some(SessionState::Draft),
            "ready" => Some(SessionState::Ready),
            "archived" => Some(SessionState::Archived),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GeneratorSession {
    pub id: String,
    pub kind: GeneratorKind,
    pub format: OutputFormat,
    pub input: String,
    pub result: String,
    pub state: SessionState,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct TranslationEntry {
    pub id: String,
    pub key: String,
    pub value: String,
    pub enabled: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GeneratorWorkspace {
    pub format: OutputFormat,
    pub sessions: Vec<GeneratorSession>,
    pub translations: Vec<TranslationEntry>,
    pub history: Vec<String>,
}

impl Default for GeneratorWorkspace {
    fn default() -> Self {
        GeneratorWorkspace {
            format: OutputFormat::Legacy,
            sessions: Vec::new(),
            translations: Vec::new(),
            history: Vec::new(),
        }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("lab", action, "generators", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("lab", action, "generators", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_text(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_TEXT_BYTES && !has_control(s)
}

fn valid_optional_text(s: &str) -> bool {
    s.len() <= robust::MAX_TEXT_BYTES && !has_control(s)
}

fn session_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| SESSION_KEYS.contains(&k.as_str()))
}

fn translation_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| TRANSLATION_KEYS.contains(&k.as_str()))
}

fn parse_strings(arr: &[Value], label: &str, lines: &mut Vec<String>) -> Vec<String> {
    let mut out: Vec<String> = Vec::new();
    for (i, v) in arr.iter().enumerate() {
        let Some(s) = v.as_str() else {
            lines.push(degrade(label, &format!("index={} bad_shape", i)));
            continue;
        };
        if !valid_text(s) {
            lines.push(degrade(label, &format!("index={} bad_text", i)));
            continue;
        }
        if out.iter().any(|x| x == s) {
            lines.push(degrade(label, &format!("index={} duplicate", i)));
            continue;
        }
        out.push(s.to_string());
    }
    out
}

fn parse(raw: &str) -> (GeneratorWorkspace, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (GeneratorWorkspace::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (GeneratorWorkspace::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (GeneratorWorkspace::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (GeneratorWorkspace::default(), lines);
    }
    let format = match obj.get("format").and_then(Value::as_str).and_then(OutputFormat::parse) {
        Some(f) => f,
        None => {
            lines.push(degrade("load", "format_invalid"));
            return (GeneratorWorkspace::default(), lines);
        }
    };
    let sess_arr = match obj.get("sessions").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "sessions_not_array"));
            return (GeneratorWorkspace::default(), lines);
        }
    };
    let mut sessions: Vec<GeneratorSession> = Vec::new();
    for (i, item) in sess_arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if session_keys_ok(e) => e,
            _ => {
                lines.push(degrade("session", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("session", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let kind = match entry.get("kind").and_then(Value::as_str).and_then(GeneratorKind::parse) {
            Some(k) => k,
            None => {
                lines.push(degrade("session", &format!("index={} bad_kind", i)));
                continue;
            }
        };
        let fmt = match entry.get("format").and_then(Value::as_str).and_then(OutputFormat::parse) {
            Some(f) => f,
            None => {
                lines.push(degrade("session", &format!("index={} bad_format", i)));
                continue;
            }
        };
        let input = match entry.get("input").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("session", &format!("index={} bad_input", i)));
                continue;
            }
        };
        let result = match entry.get("result").and_then(Value::as_str) {
            Some(s) if valid_optional_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("session", &format!("index={} bad_result", i)));
                continue;
            }
        };
        let state = match entry.get("state").and_then(Value::as_str).and_then(SessionState::parse) {
            Some(s) => s,
            None => {
                lines.push(degrade("session", &format!("index={} bad_state", i)));
                continue;
            }
        };
        if state == SessionState::Ready && result.is_empty() {
            lines.push(degrade("session", &format!("index={} bad_state_pair", i)));
            continue;
        }
        if sessions.iter().any(|x| x.id == id) {
            lines.push(degrade("session", &format!("index={} duplicate_id", i)));
            continue;
        }
        sessions.push(GeneratorSession { id, kind, format: fmt, input, result, state });
    }
    if sessions.len() > MAX_SESSIONS {
        let excess = sessions.len() - MAX_SESSIONS;
        sessions.truncate(MAX_SESSIONS);
        lines.push(degrade("session", &format!("overflow={}", excess)));
    }
    let tr_arr = match obj.get("translations").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "translations_not_array"));
            return (GeneratorWorkspace::default(), lines);
        }
    };
    let mut translations: Vec<TranslationEntry> = Vec::new();
    for (i, item) in tr_arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if translation_keys_ok(e) => e,
            _ => {
                lines.push(degrade("translation", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("translation", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let key = match entry.get("key").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("translation", &format!("index={} bad_key", i)));
                continue;
            }
        };
        let val = match entry.get("value").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("translation", &format!("index={} bad_value", i)));
                continue;
            }
        };
        let enabled = match entry.get("enabled").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("translation", &format!("index={} bad_enabled", i)));
                continue;
            }
        };
        if translations.iter().any(|x| x.key == key) {
            lines.push(degrade("translation", &format!("index={} duplicate_key", i)));
            continue;
        }
        translations.push(TranslationEntry { id, key, value: val, enabled });
    }
    if translations.len() > MAX_TRANSLATIONS {
        let excess = translations.len() - MAX_TRANSLATIONS;
        translations.truncate(MAX_TRANSLATIONS);
        lines.push(degrade("translation", &format!("overflow={}", excess)));
    }
    let hi_arr = match obj.get("history").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "history_not_array"));
            return (GeneratorWorkspace::default(), lines);
        }
    };
    let mut history: Vec<String> = parse_strings(hi_arr, "history", &mut lines);
    if history.len() > MAX_HISTORY {
        history.truncate(MAX_HISTORY);
        lines.push(degrade("history", "overflow"));
    }
    (GeneratorWorkspace { format, sessions, translations, history }, lines)
}

fn serialize(p: &GeneratorWorkspace) -> Result<String> {
    let sessions: Vec<Value> = p.sessions.iter().map(|s| json!({
        "id": s.id, "kind": s.kind.code(), "format": s.format.code(),
        "input": s.input, "result": s.result, "state": s.state.code(),
    })).collect();
    let translations: Vec<Value> = p.translations.iter().map(|t| json!({
        "id": t.id, "key": t.key, "value": t.value, "enabled": t.enabled,
    })).collect();
    Ok(to_string(&json!({
        "schema": 1,
        "format": p.format.code(),
        "sessions": sessions,
        "translations": translations,
        "history": p.history,
    }))?)
}

fn write(root: &Path, p: &GeneratorWorkspace) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, GENERATOR_SESSION_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", GENERATOR_SESSION_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl GeneratorWorkspace {
    pub fn open(root: Option<&Path>) -> (GeneratorWorkspace, Vec<String>) {
        let Some(dir) = root else {
            return (GeneratorWorkspace::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, GENERATOR_SESSION_FILE) {
            Ok(p) => p,
            Err(_) => return (GeneratorWorkspace::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (GeneratorWorkspace::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (GeneratorWorkspace::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn add_session(&mut self, id: &str, kind: GeneratorKind, format: OutputFormat, input: &str) -> bool {
        if !valid_text(id) || !valid_text(input) {
            return false;
        }
        if self.sessions.len() >= MAX_SESSIONS || self.sessions.iter().any(|s| s.id == id) {
            return false;
        }
        self.sessions.push(GeneratorSession {
            id: id.to_string(), kind, format, input: input.to_string(),
            result: String::new(), state: SessionState::Draft,
        });
        true
    }

    pub fn remove_session(&mut self, id: &str) -> bool {
        let before = self.sessions.len();
        self.sessions.retain(|s| s.id != id);
        self.sessions.len() != before
    }

    pub fn set_session_input(&mut self, id: &str, text: &str) -> bool {
        if !valid_text(text) { return false; }
        let Some(s) = self.sessions.iter_mut().find(|s| s.id == id) else { return false; };
        s.input = text.to_string();
        true
    }

    pub fn set_session_result(&mut self, id: &str, text: &str) -> bool {
        if !valid_optional_text(text) { return false; }
        let Some(s) = self.sessions.iter_mut().find(|s| s.id == id) else { return false; };
        s.result = text.to_string();
        true
    }

    pub fn set_session_state(&mut self, id: &str, state: SessionState) -> bool {
        let Some(s) = self.sessions.iter_mut().find(|s| s.id == id) else { return false; };
        if state == SessionState::Ready && s.result.is_empty() { return false; }
        s.state = state;
        true
    }

    pub fn set_session_format(&mut self, id: &str, format: OutputFormat) -> bool {
        let Some(s) = self.sessions.iter_mut().find(|s| s.id == id) else { return false; };
        s.format = format;
        true
    }

    pub fn set_session_kind(&mut self, id: &str, kind: GeneratorKind) -> bool {
        let Some(s) = self.sessions.iter_mut().find(|s| s.id == id) else { return false; };
        s.kind = kind;
        true
    }

    pub fn add_translation(&mut self, id: &str, key: &str, value: &str) -> bool {
        if !valid_text(id) || !valid_text(key) || !valid_text(value) {
            return false;
        }
        if self.translations.len() >= MAX_TRANSLATIONS || self.translations.iter().any(|t| t.key == key) {
            return false;
        }
        self.translations.push(TranslationEntry {
            id: id.to_string(), key: key.to_string(), value: value.to_string(), enabled: true,
        });
        true
    }

    pub fn remove_translation(&mut self, id: &str) -> bool {
        let before = self.translations.len();
        self.translations.retain(|t| t.id != id);
        self.translations.len() != before
    }

    pub fn set_translation_enabled(&mut self, id: &str, enabled: bool) -> bool {
        let Some(t) = self.translations.iter_mut().find(|t| t.id == id) else { return false; };
        t.enabled = enabled;
        true
    }

    pub fn set_translation_value(&mut self, id: &str, value: &str) -> bool {
        if !valid_text(value) { return false; }
        let Some(t) = self.translations.iter_mut().find(|t| t.id == id) else { return false; };
        t.value = value.to_string();
        true
    }

    pub fn set_format(&mut self, format: OutputFormat) -> bool {
        if !FORMATS.contains(&format.code()) { return false; }
        self.format = format;
        true
    }

    pub fn add_history(&mut self, s: &str) -> bool {
        if !valid_text(s) || self.history.len() >= MAX_HISTORY || self.history.iter().any(|x| x == s) {
            return false;
        }
        self.history.push(s.to_string());
        true
    }

    pub fn remove_history(&mut self, s: &str) -> bool {
        let before = self.history.len();
        self.history.retain(|x| x != s);
        self.history.len() != before
    }

    pub fn renderable(&self) -> Vec<&str> {
        self.sessions.iter()
            .filter(|s| s.state == SessionState::Ready && !s.result.is_empty())
            .map(|s| s.id.as_str()).collect()
    }

    pub fn active_translations(&self) -> Vec<&str> {
        self.translations.iter().filter(|t| t.enabled).map(|t| t.key.as_str()).collect()
    }

    pub fn by_kind(&self) -> [usize; 3] {
        let mut out = [0usize; 3];
        for s in &self.sessions {
            match s.kind {
                GeneratorKind::Recipe => out[0] += 1,
                GeneratorKind::Gradient => out[1] += 1,
                GeneratorKind::ModTranslation => out[2] += 1,
            }
        }
        out
    }

    pub fn clipboard_candidates(&self, format: OutputFormat) -> Vec<&str> {
        self.sessions.iter()
            .filter(|s| s.state == SessionState::Ready && !s.result.is_empty() && s.format == format)
            .map(|s| s.id.as_str()).collect()
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        let kinds = self.by_kind();
        Envelope::new(Kind::Event, EVENT_TARGET)
            .with("sessions", &self.sessions.len().to_string())
            .with("ready", &self.renderable().len().to_string())
            .with("translations", &self.translations.len().to_string())
            .with("active", &self.active_translations().len().to_string())
            .with("history", &self.history.len().to_string())
            .with("format", self.format.code())
            .with("recipe", &kinds[0].to_string())
            .with("gradient", &kinds[1].to_string())
            .with("mod_translation", &kinds[2].to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    GeneratorWorkspace::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu078-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"format":"legacy","sessions":[],"translations":[],"history":[]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 5);
    }

    #[test]
    fn three_enum_codes_and_six_tables_are_explicit() {
        assert_eq!(GeneratorKind::Recipe.code(), "recipe");
        assert_eq!(GeneratorKind::Gradient.code(), "gradient");
        assert_eq!(GeneratorKind::ModTranslation.code(), "mod_translation");
        assert_eq!(GeneratorKind::parse("nope"), None);
        assert_eq!(OutputFormat::Legacy.code(), "legacy");
        assert_eq!(OutputFormat::Json.code(), "json");
        assert_eq!(OutputFormat::parse("nope"), None);
        assert_eq!(SessionState::Draft.code(), "draft");
        assert_eq!(SessionState::Ready.code(), "ready");
        assert_eq!(SessionState::Archived.code(), "archived");
        assert_eq!(SessionState::parse("nope"), None);
        assert_eq!(KNOWN_KEYS.len(), 5);
        assert_eq!(SESSION_KEYS.len(), 6);
        assert_eq!(TRANSLATION_KEYS.len(), 4);
        assert_eq!(KINDS.len(), 3);
        assert_eq!(FORMATS.len(), 2);
        assert_eq!(STATES.len(), 3);
        assert_eq!(MAX_SESSIONS, 24);
        assert_eq!(MAX_TRANSLATIONS, 64);
        assert_eq!(MAX_HISTORY, 32);
    }

    #[test]
    fn default_is_empty_with_legacy_format() {
        let (p, lines) = GeneratorWorkspace::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, GeneratorWorkspace::default());
        assert_eq!(p.format, OutputFormat::Legacy);
        assert!(p.sessions.is_empty());
        assert!(p.translations.is_empty());
        assert!(p.history.is_empty());
        assert!(p.renderable().is_empty());
        assert!(p.active_translations().is_empty());
        assert_eq!(p.by_kind(), [0, 0, 0]);
        assert!(p.clipboard_candidates(OutputFormat::Legacy).is_empty());
        assert!(p.clipboard_candidates(OutputFormat::Json).is_empty());
    }

    #[test]
    fn bad_root_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(GENERATOR_SESSION_FILE);
        let base = DEFAULT_STATE;
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            base.replace("\"history\":[]", "\"history\":[],\"extra\":1"),
            base.replace("\"schema\":1", "\"schema\":2"),
            base.replace("\"format\":\"legacy\"", "\"format\":\"bad\""),
            base.replace("\"sessions\":[]", "\"sessions\":\"no\""),
            base.replace("\"translations\":[]", "\"translations\":\"no\""),
            base.replace("\"history\":[]", "\"history\":\"no\""),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (p, lines) = GeneratorWorkspace::open(Some(&r));
            assert_eq!(p, GeneratorWorkspace::default(), "case={}", &raw[..raw.len().min(40)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(40)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_session_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"format":"json","sessions":[{"id":"a","kind":"recipe","format":"legacy","input":"x","result":"y","state":"ready"},7,{"id":"","kind":"recipe","format":"legacy","input":"x","result":"y","state":"draft"},{"id":"b","kind":"bad","format":"legacy","input":"x","result":"y","state":"draft"},{"id":"c","kind":"recipe","format":"bad","input":"x","result":"y","state":"draft"},{"id":"d","kind":"recipe","format":"legacy","input":"","result":"y","state":"draft"},{"id":"e","kind":"recipe","format":"legacy","input":"x","result":"y\nz","state":"draft"},{"id":"f","kind":"recipe","format":"legacy","input":"x","result":"y","state":"bad"},{"id":"g","kind":"recipe","format":"legacy","input":"x","result":"","state":"ready"},{"id":"h","kind":"recipe","format":"legacy","input":"x","result":"y","state":"no"},{"id":"i","kind":"recipe","format":"legacy","input":"x","result":"y","state":"draft","z":1},{"id":"a","kind":"gradient","format":"json","input":"q","result":"","state":"draft"}],"translations":[],"history":[]}"#;
        fs::write(r.join(GENERATOR_SESSION_FILE), raw).unwrap();
        let (p, lines) = GeneratorWorkspace::open(Some(&r));
        assert_eq!(p.format, OutputFormat::Json);
        assert_eq!(p.sessions.len(), 1);
        assert_eq!(p.sessions[0].id, "a");
        assert_eq!(p.sessions[0].kind, GeneratorKind::Recipe);
        assert_eq!(p.sessions[0].state, SessionState::Ready);
        for tag in ["bad_shape", "bad_id", "bad_kind", "bad_format", "bad_input", "bad_result", "bad_state", "bad_state_pair", "duplicate_id"] {
            assert!(lines.iter().any(|x| x.contains(tag)), "missing={}", tag);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_translation_entries_and_history_are_skipped() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"format":"legacy","sessions":[],"translations":[{"id":"t1","key":"menu.title","value":"hello","enabled":true},false,{"id":"","key":"k","value":"v","enabled":true},{"id":"t2","key":"","value":"v","enabled":true},{"id":"t3","key":"k","value":"","enabled":true},{"id":"t4","key":"k","value":"v","enabled":"no"},{"id":"t5","key":"k","value":"v","enabled":true,"z":1},{"id":"t6","key":"k","value":"v","enabled":false},{"id":"t7","key":"k","value":"w","enabled":true}],"history":[7,"","a\nb","ok","ok"]}"#;
        fs::write(r.join(GENERATOR_SESSION_FILE), raw).unwrap();
        let (p, lines) = GeneratorWorkspace::open(Some(&r));
        assert_eq!(p.translations.len(), 2);
        assert_eq!(p.translations[0].id, "t1");
        assert_eq!(p.translations[1].id, "t6");
        assert!(!p.translations[1].enabled);
        assert_eq!(p.active_translations(), vec!["menu.title"]);
        assert_eq!(p.history, vec!["ok".to_string()]);
        for tag in ["bad_shape", "bad_id", "bad_key", "bad_value", "bad_enabled", "duplicate_key", "bad_text", "duplicate"] {
            assert!(lines.iter().any(|x| x.contains(tag)), "missing={}", tag);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_truncates_overflow_from_disk() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let mut sess = String::from("[");
        for i in 0..(MAX_SESSIONS + 3) {
            if i > 0 { sess.push(','); }
            sess.push_str(&format!(r#"{{"id":"s{}","kind":"recipe","format":"legacy","input":"i","result":"r","state":"ready"}}"#, i));
        }
        sess.push(']');
        let mut tr = String::from("[");
        for i in 0..(MAX_TRANSLATIONS + 2) {
            if i > 0 { tr.push(','); }
            tr.push_str(&format!(r#"{{"id":"t{}","key":"k{}","value":"v","enabled":true}}"#, i, i));
        }
        tr.push(']');
        let raw = format!(r#"{{"schema":1,"format":"legacy","sessions":{},"translations":{},"history":[]}}"#, sess, tr);
        fs::write(r.join(GENERATOR_SESSION_FILE), raw).unwrap();
        let (p, lines) = GeneratorWorkspace::open(Some(&r));
        assert_eq!(p.sessions.len(), MAX_SESSIONS);
        assert_eq!(p.translations.len(), MAX_TRANSLATIONS);
        assert!(lines.iter().any(|x| x.contains("overflow=3")));
        assert!(lines.iter().any(|x| x.contains("overflow=2")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn add_remove_and_session_bounds() {
        let mut p = GeneratorWorkspace::default();
        assert!(p.add_session("s1", GeneratorKind::Recipe, OutputFormat::Legacy, "in"));
        assert!(p.add_session("s2", GeneratorKind::Gradient, OutputFormat::Json, "in2"));
        assert_eq!(p.by_kind(), [1, 1, 0]);
        assert!(!p.add_session("s1", GeneratorKind::Recipe, OutputFormat::Legacy, "in"));
        assert!(!p.add_session("", GeneratorKind::Recipe, OutputFormat::Legacy, "in"));
        assert!(!p.add_session("bad\nid", GeneratorKind::Recipe, OutputFormat::Legacy, "in"));
        assert!(!p.add_session("s3", GeneratorKind::Recipe, OutputFormat::Legacy, ""));
        assert!(p.remove_session("s1"));
        assert!(!p.remove_session("missing"));
        assert_eq!(p.sessions.len(), 1);
        for i in 0..(MAX_SESSIONS + 5) {
            p.add_session(&format!("w{}", i), GeneratorKind::ModTranslation, OutputFormat::Legacy, "v");
        }
        assert_eq!(p.sessions.len(), MAX_SESSIONS);
    }

    #[test]
    fn single_session_mutations_only_touch_one_item() {
        let mut p = GeneratorWorkspace::default();
        p.add_session("a", GeneratorKind::Recipe, OutputFormat::Legacy, "x");
        p.add_session("b", GeneratorKind::Gradient, OutputFormat::Json, "y");
        assert!(p.set_session_input("a", "x2"));
        assert_eq!(p.sessions[0].input, "x2");
        assert_eq!(p.sessions[1].input, "y");
        assert!(p.set_session_result("a", "r1"));
        assert_eq!(p.sessions[0].result, "r1");
        assert_eq!(p.sessions[1].result, "");
        assert!(!p.set_session_state("b", SessionState::Ready));
        assert_eq!(p.sessions[1].state, SessionState::Draft);
        assert!(p.set_session_state("a", SessionState::Ready));
        assert_eq!(p.sessions[0].state, SessionState::Ready);
        assert!(p.set_session_format("a", OutputFormat::Json));
        assert_eq!(p.sessions[0].format, OutputFormat::Json);
        assert_eq!(p.sessions[1].format, OutputFormat::Json);
        assert!(p.set_session_kind("b", GeneratorKind::ModTranslation));
        assert_eq!(p.sessions[0].kind, GeneratorKind::Recipe);
        assert_eq!(p.sessions[1].kind, GeneratorKind::ModTranslation);
        assert!(!p.set_session_input("missing", "q"));
        assert!(!p.set_session_result("missing", "q"));
        assert!(!p.set_session_state("missing", SessionState::Archived));
        assert!(!p.set_session_format("missing", OutputFormat::Json));
        assert!(!p.set_session_kind("missing", GeneratorKind::Recipe));
        assert!(!p.set_session_input("a", ""));
        assert!(!p.set_session_result("a", "a\nb"));
    }

    #[test]
    fn state_pair_and_format_validation() {
        let mut p = GeneratorWorkspace::default();
        p.add_session("a", GeneratorKind::Recipe, OutputFormat::Legacy, "x");
        assert!(!p.set_session_state("a", SessionState::Ready));
        assert!(p.set_session_result("a", "r"));
        assert!(p.set_session_state("a", SessionState::Ready));
        assert!(p.set_session_state("a", SessionState::Archived));
        assert_eq!(p.renderable(), Vec::<&str>::new());
        assert!(p.set_session_result("a", ""));
        assert!(!p.set_session_state("a", SessionState::Ready));
        assert!(p.set_format(OutputFormat::Json));
        assert_eq!(p.format, OutputFormat::Json);
        assert!(p.set_format(OutputFormat::Legacy));
        assert_eq!(p.format, OutputFormat::Legacy);
    }

    #[test]
    fn translation_add_remove_and_bounds() {
        let mut p = GeneratorWorkspace::default();
        assert!(p.add_translation("t1", "menu.title", "hello"));
        assert!(!p.add_translation("t2", "menu.title", "other"));
        assert!(!p.add_translation("", "k", "v"));
        assert!(!p.add_translation("t3", "", "v"));
        assert!(!p.add_translation("t4", "k", ""));
        assert!(!p.add_translation("t5", "a\nb", "v"));
        assert_eq!(p.active_translations(), vec!["menu.title"]);
        assert!(p.set_translation_enabled("t1", false));
        assert!(p.active_translations().is_empty());
        assert!(p.set_translation_value("t1", "world"));
        assert_eq!(p.translations[0].value, "world");
        assert!(!p.set_translation_value("t1", ""));
        assert!(!p.set_translation_enabled("missing", false));
        assert!(!p.set_translation_value("missing", "v"));
        assert!(p.remove_translation("t1"));
        assert!(!p.remove_translation("t1"));
        for i in 0..(MAX_TRANSLATIONS + 3) {
            p.add_translation(&format!("t{}", i), &format!("k{}", i), "v");
        }
        assert_eq!(p.translations.len(), MAX_TRANSLATIONS);
    }

    #[test]
    fn history_add_remove_and_bound() {
        let mut p = GeneratorWorkspace::default();
        assert!(p.add_history("h1"));
        assert!(!p.add_history("h1"));
        assert!(!p.add_history(""));
        assert!(!p.add_history("a\nb"));
        assert!(p.remove_history("h1"));
        assert!(!p.remove_history("h1"));
        for i in 0..(MAX_HISTORY + 3) { p.add_history(&format!("h{}", i)); }
        assert_eq!(p.history.len(), MAX_HISTORY);
    }

    #[test]
    fn derived_queries_are_pure_and_state_aware() {
        let mut p = GeneratorWorkspace::default();
        p.add_session("a", GeneratorKind::Recipe, OutputFormat::Legacy, "i");
        p.add_session("b", GeneratorKind::Gradient, OutputFormat::Json, "i");
        p.add_session("c", GeneratorKind::ModTranslation, OutputFormat::Legacy, "i");
        p.set_session_result("a", "ra");
        p.set_session_result("b", "rb");
        p.set_session_result("c", "rc");
        p.set_session_state("a", SessionState::Ready);
        p.set_session_state("b", SessionState::Ready);
        p.set_session_state("c", SessionState::Archived);
        assert_eq!(p.renderable(), vec!["a", "b"]);
        assert_eq!(p.clipboard_candidates(OutputFormat::Legacy), vec!["a"]);
        assert_eq!(p.clipboard_candidates(OutputFormat::Json), vec!["b"]);
        assert_eq!(p.by_kind(), [1, 1, 1]);
        p.add_translation("t1", "k1", "v1");
        p.add_translation("t2", "k2", "v2");
        p.set_translation_enabled("t2", false);
        assert_eq!(p.active_translations(), vec!["k1"]);
        p.set_session_result("a", "");
        assert_eq!(p.renderable(), vec!["b"]);
        assert!(p.clipboard_candidates(OutputFormat::Legacy).is_empty());
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut p = GeneratorWorkspace::default();
        p.add_session("a", GeneratorKind::Recipe, OutputFormat::Legacy, "x");
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
        let mut p = GeneratorWorkspace::default();
        assert!(p.set_format(OutputFormat::Json));
        assert!(p.add_session("a", GeneratorKind::Recipe, OutputFormat::Legacy, "in-a"));
        assert!(p.set_session_result("a", "out-a"));
        assert!(p.set_session_state("a", SessionState::Ready));
        assert!(p.add_session("b", GeneratorKind::Gradient, OutputFormat::Json, "in-b"));
        assert!(p.add_translation("t1", "menu.title", "hello"));
        assert!(p.set_translation_enabled("t1", false));
        assert!(p.add_history("h1"));
        assert!(p.persist(Some(&r)).is_empty());
        let (back, lines) = GeneratorWorkspace::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.format, OutputFormat::Json);
        assert_eq!(back.sessions.len(), 2);
        assert_eq!(back.sessions[0].state, SessionState::Ready);
        assert_eq!(back.sessions[0].result, "out-a");
        assert_eq!(back.sessions[1].state, SessionState::Draft);
        assert_eq!(back.sessions[1].result, "");
        assert_eq!(back.translations.len(), 1);
        assert!(!back.translations[0].enabled);
        assert_eq!(back.history, vec!["h1".to_string()]);
        assert_eq!(back.renderable(), vec!["a"]);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = GeneratorWorkspace::open(Some(&r));
        assert_eq!(def, GeneratorWorkspace::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope_without_user_text() {
        let mut p = GeneratorWorkspace::default();
        p.add_session("secret-id", GeneratorKind::Recipe, OutputFormat::Legacy, "secret-input");
        p.set_session_result("secret-id", "secret-result");
        p.set_session_state("secret-id", SessionState::Ready);
        p.add_session("s2", GeneratorKind::Gradient, OutputFormat::Json, "i");
        p.add_session("s3", GeneratorKind::ModTranslation, OutputFormat::Legacy, "i");
        p.add_translation("t1", "menu.secret", "secret-value");
        p.add_history("secret-history");
        let e = p.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, EVENT_TARGET);
        assert_eq!(e.field("sessions"), Some("3"));
        assert_eq!(e.field("ready"), Some("1"));
        assert_eq!(e.field("translations"), Some("1"));
        assert_eq!(e.field("active"), Some("1"));
        assert_eq!(e.field("history"), Some("1"));
        assert_eq!(e.field("format"), Some("legacy"));
        assert_eq!(e.field("recipe"), Some("1"));
        assert_eq!(e.field("gradient"), Some("1"));
        assert_eq!(e.field("mod_translation"), Some("1"));
        assert_eq!(e.field("ids"), None);
        assert_eq!(e.field("values"), None);
        assert_eq!(e.field("text"), None);
        assert_eq!(e.field("input"), None);
        assert_eq!(e.field("result"), None);
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 9);
    }

    #[test]
    fn serialize_carries_no_session_table() {
        let mut p = GeneratorWorkspace::default();
        p.add_session("a", GeneratorKind::Recipe, OutputFormat::Legacy, "x");
        let raw = serialize(&p).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 5);
        assert!(!raw.contains("SESSION_TABLE"));
        assert!(!raw.contains("GRADIENT_TABLE"));
        assert!(!raw.contains("cmp_precedence"));
        assert!(!raw.contains("semver"));
    }
}

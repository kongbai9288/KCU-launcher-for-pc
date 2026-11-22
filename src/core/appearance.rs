use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const APPEARANCE_FILE: &str = "appearance.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"mode":"light","accent":null,"background":false,"transparency":false,"presets":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_PRESETS: usize = 16;
pub const APPEARANCE_TARGET: &str = "appearance.modes";
pub const KNOWN_KEYS: &[&str] = &["schema", "mode", "accent", "background", "transparency", "presets"];
pub const PRESET_KEYS: &[&str] = &["id", "accent"];
pub const MODES: &[&str] = &["light", "dark", "oled", "system"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AppearanceMode {
    Light,
    Dark,
    Oled,
    System,
}

impl AppearanceMode {
    pub fn code(&self) -> &'static str {
        match self {
            AppearanceMode::Light => "light",
            AppearanceMode::Dark => "dark",
            AppearanceMode::Oled => "oled",
            AppearanceMode::System => "system",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "light" => Some(AppearanceMode::Light),
            "dark" => Some(AppearanceMode::Dark),
            "oled" => Some(AppearanceMode::Oled),
            "system" => Some(AppearanceMode::System),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Preset {
    pub id: String,
    pub accent: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Appearance {
    pub mode: AppearanceMode,
    pub accent: Option<String>,
    pub background: bool,
    pub transparency: bool,
    pub presets: Vec<Preset>,
}

impl Default for Appearance {
    fn default() -> Self {
        Appearance {
            mode: AppearanceMode::Light,
            accent: None,
            background: false,
            transparency: false,
            presets: Vec::new(),
        }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("appearance", action, "modes", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("appearance", action, "modes", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_ID_BYTES && !has_control(s)
}

fn preset_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| PRESET_KEYS.contains(&k.as_str()))
}

fn parse(raw: &str) -> (Appearance, Vec<String>) {
    let mut lines = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (Appearance::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (Appearance::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (Appearance::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (Appearance::default(), lines);
    }
    let mode = match obj.get("mode").and_then(Value::as_str).and_then(AppearanceMode::parse) {
        Some(m) => m,
        None => {
            lines.push(degrade("load", "mode_invalid"));
            return (Appearance::default(), lines);
        }
    };
    let accent: Option<String> = match obj.get("accent") {
        Some(Value::Null) => None,
        Some(Value::String(s)) if valid_id(s) => Some(s.clone()),
        _ => {
            lines.push(degrade("load", "accent_invalid"));
            return (Appearance::default(), lines);
        }
    };
    let background = match obj.get("background").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "background_not_bool"));
            return (Appearance::default(), lines);
        }
    };
    let transparency = match obj.get("transparency").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "transparency_not_bool"));
            return (Appearance::default(), lines);
        }
    };
    let arr = match obj.get("presets").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "presets_not_array"));
            return (Appearance::default(), lines);
        }
    };
    let mut presets: Vec<Preset> = Vec::new();
    for (i, item) in arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if preset_keys_ok(e) => e,
            _ => {
                lines.push(degrade("preset", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("preset", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let accent_value = match entry.get("accent").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("preset", &format!("index={} bad_accent", i)));
                continue;
            }
        };
        if presets.iter().any(|p| p.id == id) {
            lines.push(degrade("preset", &format!("index={} duplicate_id", i)));
            continue;
        }
        presets.push(Preset { id, accent: accent_value });
    }
    if presets.len() > MAX_PRESETS {
        let excess = presets.len() - MAX_PRESETS;
        presets.truncate(MAX_PRESETS);
        lines.push(degrade("preset", &format!("overflow={}", excess)));
    }
    (Appearance { mode, accent, background, transparency, presets }, lines)
}

fn serialize(a: &Appearance) -> Result<String> {
    let presets: Vec<Value> = a
        .presets
        .iter()
        .map(|p| json!({"id": p.id, "accent": p.accent}))
        .collect();
    let accent = match &a.accent {
        Some(s) => Value::String(s.clone()),
        None => Value::Null,
    };
    Ok(to_string(&json!({
        "schema": 1,
        "mode": a.mode.code(),
        "accent": accent,
        "background": a.background,
        "transparency": a.transparency,
        "presets": presets,
    }))?)
}

fn write(root: &Path, a: &Appearance) -> Result<()> {
    let body = serialize(a)?;
    let path = robust::safe_join(root, APPEARANCE_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", APPEARANCE_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl Appearance {
    pub fn open(root: Option<&Path>) -> (Appearance, Vec<String>) {
        let Some(dir) = root else {
            return (Appearance::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, APPEARANCE_FILE) {
            Ok(p) => p,
            Err(_) => return (Appearance::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (Appearance::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (Appearance::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn set_mode(&mut self, mode: AppearanceMode) {
        self.mode = mode;
    }

    pub fn set_accent(&mut self, accent: &str) -> bool {
        if !valid_id(accent) {
            return false;
        }
        self.accent = Some(accent.to_string());
        true
    }

    pub fn clear_accent(&mut self) {
        self.accent = None;
    }

    pub fn set_background(&mut self, on: bool) {
        self.background = on;
    }

    pub fn set_transparency(&mut self, on: bool) {
        self.transparency = on;
    }

    pub fn add_preset(&mut self, id: &str, accent: &str) -> bool {
        if !valid_id(id) || !valid_id(accent)
            || self.presets.len() >= MAX_PRESETS
            || self.presets.iter().any(|p| p.id == id)
        {
            return false;
        }
        self.presets.push(Preset { id: id.to_string(), accent: accent.to_string() });
        true
    }

    pub fn remove_preset(&mut self, id: &str) -> bool {
        let before = self.presets.len();
        self.presets.retain(|p| p.id != id);
        self.presets.len() != before
    }

    pub fn apply_preset(&mut self, id: &str) -> bool {
        let Some(p) = self.presets.iter().find(|p| p.id == id) else {
            return false;
        };
        self.accent = Some(p.accent.clone());
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
        Envelope::new(Kind::Event, APPEARANCE_TARGET)
            .with("mode", self.mode.code())
            .with("presets", &self.presets.len().to_string())
            .with("background", &self.background.to_string())
            .with("transparency", &self.transparency.to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    Appearance::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu073-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn mode_codes_and_keys_are_explicit() {
        assert_eq!(AppearanceMode::Light.code(), "light");
        assert_eq!(AppearanceMode::Dark.code(), "dark");
        assert_eq!(AppearanceMode::Oled.code(), "oled");
        assert_eq!(AppearanceMode::System.code(), "system");
        assert_eq!(AppearanceMode::parse("nope"), None);
        assert_eq!(MODES.len(), 4);
        assert_eq!(KNOWN_KEYS.len(), 6);
        assert_eq!(PRESET_KEYS.len(), 2);
        assert_eq!(MAX_PRESETS, 16);
    }

    #[test]
    fn default_is_light_empty() {
        let (a, lines) = Appearance::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(a, Appearance::default());
        assert_eq!(a.mode, AppearanceMode::Light);
        assert_eq!(a.accent, None);
        assert!(!a.background);
        assert!(!a.transparency);
        assert!(a.presets.is_empty());
    }

    #[test]
    fn ten_bad_root_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(APPEARANCE_FILE);
        let base = r#"{"schema":1,"mode":"light","accent":null,"background":false,"transparency":false,"presets":[]}"#;
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            base.replace("\"presets\":[]", "\"presets\":[],\"extra\":1"),
            base.replace("\"schema\":1", "\"schema\":2"),
            base.replace("\"mode\":\"light\"", "\"mode\":\"nope\""),
            base.replace("\"accent\":null", "\"accent\":7"),
            base.replace("\"background\":false", "\"background\":\"no\""),
            base.replace("\"transparency\":false", "\"transparency\":\"no\""),
            base.replace("\"presets\":[]", "\"presets\":\"no\""),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (a, lines) = Appearance::open(Some(&r));
            assert_eq!(a, Appearance::default(), "case={}", &raw[..raw.len().min(28)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(28)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_preset_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"mode":"dark","accent":"a1","background":true,"transparency":false,"presets":[{"id":"p1","accent":"c1"},7,{"id":"","accent":"c2"},{"id":"p2","accent":""},{"id":"p3","accent":"c3","z":1},{"id":"p1","accent":"c4"}]}"#;
        fs::write(r.join(APPEARANCE_FILE), raw).unwrap();
        let (a, lines) = Appearance::open(Some(&r));
        assert_eq!(a.mode, AppearanceMode::Dark);
        assert_eq!(a.accent, Some("a1".to_string()));
        assert!(a.background);
        assert_eq!(a.presets.len(), 1);
        assert_eq!(a.presets[0].id, "p1");
        assert!(lines.iter().any(|x| x.contains("bad_shape")));
        assert!(lines.iter().any(|x| x.contains("bad_id")));
        assert!(lines.iter().any(|x| x.contains("bad_accent")));
        assert!(lines.iter().any(|x| x.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn set_mode_and_accent() {
        let mut a = Appearance::default();
        a.set_mode(AppearanceMode::Oled);
        assert_eq!(a.mode, AppearanceMode::Oled);
        assert!(a.set_accent("c-01"));
        assert_eq!(a.accent, Some("c-01".to_string()));
        assert!(!a.set_accent(""));
        assert!(!a.set_accent("bad\nid"));
        assert_eq!(a.accent, Some("c-01".to_string()));
        a.clear_accent();
        assert_eq!(a.accent, None);
    }

    #[test]
    fn booleans_and_preset_crud() {
        let mut a = Appearance::default();
        a.set_background(true);
        a.set_transparency(true);
        assert!(a.background && a.transparency);
        assert!(a.add_preset("p1", "c1"));
        assert!(a.add_preset("p2", "c2"));
        assert!(!a.add_preset("p1", "c3"));
        assert!(!a.add_preset("", "c3"));
        assert!(!a.add_preset("p3", ""));
        assert!(a.apply_preset("p2"));
        assert_eq!(a.accent, Some("c2".to_string()));
        assert!(!a.apply_preset("missing"));
        assert!(a.remove_preset("p1"));
        assert!(!a.remove_preset("p1"));
        assert_eq!(a.presets.len(), 1);
    }

    #[test]
    fn presets_bounded_and_dedup() {
        let mut a = Appearance::default();
        for i in 0..(MAX_PRESETS + 5) {
            a.add_preset(&format!("p{}", i), "c");
        }
        assert_eq!(a.presets.len(), MAX_PRESETS);
        assert!(!a.add_preset("overflow", "c"));
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let mut body = String::from(r#"{"schema":1,"mode":"system","accent":null,"background":false,"transparency":true,"presets":["#);
        for i in 0..(MAX_PRESETS + 3) {
            if i > 0 { body.push(','); }
            body.push_str(&format!(r#"{{"id":"q{}","accent":"c"}}"#, i));
        }
        body.push_str("]}");
        fs::write(r.join(APPEARANCE_FILE), body).unwrap();
        let (back, lines) = Appearance::open(Some(&r));
        assert_eq!(back.presets.len(), MAX_PRESETS);
        assert!(lines.iter().any(|x| x.contains("overflow=3")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut a = Appearance::default();
        a.set_mode(AppearanceMode::Dark);
        assert!(a.persist(None)[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn persist_reopen_reset_keep_protected_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let mut a = Appearance::default();
        a.set_mode(AppearanceMode::System);
        a.set_accent("c-9");
        a.set_background(true);
        a.add_preset("p1", "c1");
        assert!(a.persist(Some(&r)).is_empty());
        let (back, lines) = Appearance::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.mode, AppearanceMode::System);
        assert_eq!(back.accent, Some("c-9".to_string()));
        assert!(back.background);
        assert!(!back.transparency);
        assert_eq!(back.presets.len(), 1);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = Appearance::open(Some(&r));
        assert_eq!(def, Appearance::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn accent_null_roundtrip() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"mode":"light","accent":null,"background":false,"transparency":false,"presets":[]}"#;
        fs::write(r.join(APPEARANCE_FILE), raw).unwrap();
        let (a, lines) = Appearance::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(a.accent, None);
        assert!(a.persist(Some(&r)).is_empty());
        let text = fs::read_to_string(r.join(APPEARANCE_FILE)).unwrap();
        assert!(text.contains("\"accent\":null"));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope() {
        let mut a = Appearance::default();
        a.set_mode(AppearanceMode::Oled);
        a.set_accent("c-1");
        a.set_background(true);
        a.add_preset("p1", "c1");
        let e = a.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, APPEARANCE_TARGET);
        assert_eq!(e.field("mode"), Some("oled"));
        assert_eq!(e.field("presets"), Some("1"));
        assert_eq!(e.field("background"), Some("true"));
        assert_eq!(e.field("transparency"), Some("false"));
        assert_eq!(e.field("accent"), None);
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 4);
    }

    #[test]
    fn serialize_carries_no_color_table() {
        let mut a = Appearance::default();
        a.add_preset("p1", "c1");
        let raw = serialize(&a).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 6);
        assert!(!raw.contains("PRESET_COLORS"));
        assert!(!raw.contains("minecraft"));
        assert!(!raw.contains("#ffffff"));
    }
}

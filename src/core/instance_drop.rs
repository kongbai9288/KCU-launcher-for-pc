use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::{Path, PathBuf};

pub const DROP_FILE: &str = "instance-drop.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"collapsed":false,"ungrouped":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_UNGROUPED: usize = 64;
pub const DROP_TARGET: &str = "instance.drop";
pub const KNOWN_KEYS: &[&str] = &["schema", "collapsed", "ungrouped"];
pub const CATEGORY_DIRS: &[(&str, &str)] = &[
    ("resource_pack", "resourcepacks"),
    ("mod", "mods"),
    ("shader_pack", "shaderpacks"),
];
pub const ALLOWED_EXTENSIONS: &[&str] = &[".zip", ".jar"];
pub const REJECTED_EXTENSIONS: &[&str] = &[".exe", ".bat", ".dll", ".cmd", ".scr", ".ps1", ".sh", ".lnk"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DropCategory {
    ResourcePack,
    Mod,
    ShaderPack,
}

impl DropCategory {
    pub fn code(&self) -> &'static str {
        match self {
            DropCategory::ResourcePack => "resource_pack",
            DropCategory::Mod => "mod",
            DropCategory::ShaderPack => "shader_pack",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "resource_pack" => Some(DropCategory::ResourcePack),
            "mod" => Some(DropCategory::Mod),
            "shader_pack" => Some(DropCategory::ShaderPack),
            _ => None,
        }
    }
}

fn category_dir(cat: DropCategory) -> Option<&'static str> {
    CATEGORY_DIRS
        .iter()
        .find(|(c, _)| *c == cat.code())
        .map(|(_, d)| *d)
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct UngroupedState {
    pub collapsed: bool,
    pub ungrouped: Vec<String>,
}

impl Default for UngroupedState {
    fn default() -> Self {
        UngroupedState { collapsed: false, ungrouped: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("instance", action, "drop", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("instance", action, "drop", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_ID_BYTES && !has_control(s)
}

fn parse(raw: &str) -> (UngroupedState, Vec<String>) {
    let mut lines = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (UngroupedState::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (UngroupedState::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (UngroupedState::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (UngroupedState::default(), lines);
    }
    let collapsed = match obj.get("collapsed").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "collapsed_invalid"));
            return (UngroupedState::default(), lines);
        }
    };
    let arr = match obj.get("ungrouped").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "ungrouped_not_array"));
            return (UngroupedState::default(), lines);
        }
    };
    let mut ungrouped: Vec<String> = Vec::new();
    for (i, item) in arr.iter().enumerate() {
        let id = match item.as_str() {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("entry", &format!("index={} bad_id", i)));
                continue;
            }
        };
        if ungrouped.contains(&id) {
            lines.push(degrade("entry", &format!("index={} duplicate_id", i)));
            continue;
        }
        ungrouped.push(id);
    }
    if ungrouped.len() > MAX_UNGROUPED {
        let excess = ungrouped.len() - MAX_UNGROUPED;
        ungrouped.truncate(MAX_UNGROUPED);
        lines.push(degrade("entry", &format!("overflow={}", excess)));
    }
    (UngroupedState { collapsed, ungrouped }, lines)
}

fn serialize(state: &UngroupedState) -> Result<String> {
    Ok(to_string(&json!({
        "schema": 1,
        "collapsed": state.collapsed,
        "ungrouped": state.ungrouped,
    }))?)
}

fn write(root: &Path, state: &UngroupedState) -> Result<()> {
    let body = serialize(state)?;
    let path = robust::safe_join(root, DROP_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", DROP_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl UngroupedState {
    pub fn open(root: Option<&Path>) -> (UngroupedState, Vec<String>) {
        let Some(dir) = root else {
            return (UngroupedState::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, DROP_FILE) {
            Ok(p) => p,
            Err(_) => return (UngroupedState::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (UngroupedState::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (UngroupedState::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn add(&mut self, id: &str) -> bool {
        if !valid_id(id) || self.ungrouped.len() >= MAX_UNGROUPED || self.ungrouped.iter().any(|e| e == id) {
            return false;
        }
        self.ungrouped.push(id.to_string());
        true
    }

    pub fn remove(&mut self, id: &str) -> bool {
        let before = self.ungrouped.len();
        self.ungrouped.retain(|e| e != id);
        self.ungrouped.len() != before
    }

    pub fn toggle(&mut self) {
        self.collapsed = !self.collapsed;
    }

    pub fn plan(&self, root: Option<&Path>, category: DropCategory, file_name: &str) -> (Option<PathBuf>, Vec<String>) {
        let Some(dir) = root else {
            return (None, vec![error_line("plan", "no_root")]);
        };
        if file_name.is_empty()
            || file_name.len() > robust::MAX_ID_BYTES
            || has_control(file_name)
            || file_name.contains('/')
            || file_name.contains('\\')
        {
            return (None, vec![degrade("plan", "bad_file_name")]);
        }
        let ext = match Path::new(file_name).extension().and_then(|e| e.to_str()) {
            Some(e) => format!(".{}", e.to_ascii_lowercase()),
            None => return (None, vec![degrade("plan", "extension_missing")]),
        };
        if !ALLOWED_EXTENSIONS.contains(&ext.as_str()) || REJECTED_EXTENSIONS.contains(&ext.as_str()) {
            return (None, vec![degrade("plan", "extension_rejected")]);
        }
        let Some(dir_rel) = category_dir(category) else {
            return (None, vec![error_line("plan", "category_dir_missing")]);
        };
        let base = match robust::safe_join(dir, dir_rel) {
            Ok(p) => p,
            Err(e) => return (None, vec![error_line("plan", &e.to_string())]),
        };
        let target = match robust::safe_join(&base, file_name) {
            Ok(p) => p,
            Err(e) => return (None, vec![error_line("plan", &e.to_string())]),
        };
        (Some(target), Vec::new())
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        Envelope::new(Kind::Event, DROP_TARGET)
            .with("collapsed", if self.collapsed { "true" } else { "false" })
            .with("count", &self.ungrouped.len().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    UngroupedState::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu070-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn category_codes_and_dirs_are_explicit() {
        assert_eq!(DropCategory::ResourcePack.code(), "resource_pack");
        assert_eq!(DropCategory::Mod.code(), "mod");
        assert_eq!(DropCategory::ShaderPack.code(), "shader_pack");
        assert_eq!(DropCategory::parse("nope"), None);
        assert_eq!(CATEGORY_DIRS.len(), 3);
        for cat in [DropCategory::ResourcePack, DropCategory::Mod, DropCategory::ShaderPack] {
            assert!(category_dir(cat).is_some());
        }
        assert_eq!(category_dir(DropCategory::Mod), Some("mods"));
        assert_eq!(KNOWN_KEYS.len(), 3);
    }

    #[test]
    fn default_is_expanded_empty() {
        let (s, lines) = UngroupedState::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert!(!s.collapsed);
        assert!(s.ungrouped.is_empty());
    }

    #[test]
    fn eight_bad_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(DROP_FILE);
        let cases = [
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            r#"{"schema":1,"collapsed":false,"ungrouped":[],"extra":1}"#.to_string(),
            r#"{"schema":2,"collapsed":false,"ungrouped":[]}"#.to_string(),
            r#"{"schema":1,"collapsed":"no","ungrouped":[]}"#.to_string(),
            r#"{"schema":1,"collapsed":false,"ungrouped":"no"}"#.to_string(),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (s, lines) = UngroupedState::open(Some(&r));
            assert_eq!(s, UngroupedState::default(), "case={}", &raw[..raw.len().min(24)]);
            assert!(lines.iter().any(|l| l.contains("DEGRADE")), "case={}", &raw[..raw.len().min(24)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_ungrouped_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"collapsed":true,"ungrouped":["a",7,"","a","b"]}"#;
        fs::write(r.join(DROP_FILE), raw).unwrap();
        let (s, lines) = UngroupedState::open(Some(&r));
        assert!(s.collapsed);
        assert_eq!(s.ungrouped, vec!["a".to_string(), "b".to_string()]);
        assert!(lines.iter().any(|l| l.contains("bad_id")));
        assert!(lines.iter().any(|l| l.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn add_remove_toggle_and_bounds() {
        let mut s = UngroupedState::default();
        assert!(s.add("inst-a"));
        assert!(s.add("inst-b"));
        assert!(!s.add("inst-a"));
        assert!(!s.add(""));
        assert!(!s.add("bad\nid"));
        assert!(s.remove("inst-a"));
        assert!(!s.remove("missing"));
        assert_eq!(s.ungrouped, vec!["inst-b".to_string()]);
        s.toggle();
        assert!(s.collapsed);
        s.toggle();
        assert!(!s.collapsed);
        for i in 0..(MAX_UNGROUPED + 5) {
            s.add(&format!("f{}", i));
        }
        assert_eq!(s.ungrouped.len(), MAX_UNGROUPED);
    }

    #[test]
    fn plan_rejects_bad_file_names() {
        let r = tmp();
        let s = UngroupedState::default();
        for name in ["", "..", "../escape.zip", "a/b.jar", "a\\b.jar", "bad\nname.zip"] {
            let (out, lines) = s.plan(Some(&r), DropCategory::Mod, name);
            assert!(out.is_none(), "name={:?}", name);
            assert!(!lines.is_empty(), "name={:?}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn plan_rejects_executable_and_missing_extension() {
        let r = tmp();
        let s = UngroupedState::default();
        for name in ["tool.exe", "script.bat", "noext", "a.ZIP.bad"] {
            let (out, lines) = s.plan(Some(&r), DropCategory::Mod, name);
            assert!(out.is_none(), "name={}", name);
            assert!(lines.iter().any(|l| l.contains("DEGRADE")), "name={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn plan_accepts_three_categories_with_distinct_dirs() {
        let r = tmp();
        let s = UngroupedState::default();
        let mut seen = Vec::new();
        for (cat, expected) in [
            (DropCategory::ResourcePack, "resourcepacks"),
            (DropCategory::Mod, "mods"),
            (DropCategory::ShaderPack, "shaderpacks"),
        ] {
            let (out, lines) = s.plan(Some(&r), cat, "pack.zip");
            assert!(lines.is_empty());
            let p = out.expect("plan target");
            assert_eq!(p.parent().unwrap().file_name().unwrap(), expected);
            assert_eq!(p.file_name().unwrap(), "pack.zip");
            seen.push(expected.to_string());
        }
        assert_eq!(seen.len(), 3);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut s = UngroupedState::default();
        s.add("m");
        assert!(s.plan(None, DropCategory::Mod, "pack.zip").0.is_none());
        assert!(s.persist(None)[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn persist_reopen_and_reset_keep_protected_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let mut s = UngroupedState::default();
        s.collapsed = true;
        s.add("inst-x");
        assert!(s.persist(Some(&r)).is_empty());
        let (back, lines) = UngroupedState::open(Some(&r));
        assert!(lines.is_empty());
        assert!(back.collapsed);
        assert_eq!(back.ungrouped, vec!["inst-x".to_string()]);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = UngroupedState::open(Some(&r));
        assert_eq!(def, UngroupedState::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope() {
        let mut s = UngroupedState::default();
        s.toggle();
        s.add("inst-a");
        s.add("inst-b");
        let e = s.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, DROP_TARGET);
        assert_eq!(e.field("collapsed"), Some("true"));
        assert_eq!(e.field("count"), Some("2"));
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 2);
    }

    #[test]
    fn serialize_never_carries_file_content() {
        let mut s = UngroupedState::default();
        s.add("inst-a");
        let raw = serialize(&s).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 3);
        assert!(raw.contains("instance-drop") == false);
        assert!(!raw.contains("resourcepacks"));
    }
}

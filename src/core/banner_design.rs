use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const BANNER_FILE: &str = "banner-design.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"layers":[],"recent":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_LAYERS: usize = 32;
pub const MAX_HISTORY: usize = 64;
pub const MAX_RECENT: usize = 32;
pub const BANNER_TARGET: &str = "banner.design";
pub const KNOWN_KEYS: &[&str] = &["schema", "layers", "recent"];
pub const LAYER_KEYS: &[&str] = &["pattern", "dye"];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Layer {
    pub pattern: String,
    pub dye: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BannerDoc {
    pub layers: Vec<Layer>,
    pub recent: Vec<String>,
    undo: Vec<Vec<Layer>>,
    redo: Vec<Vec<Layer>>,
}

impl Default for BannerDoc {
    fn default() -> Self {
        BannerDoc {
            layers: Vec::new(),
            recent: Vec::new(),
            undo: Vec::new(),
            redo: Vec::new(),
        }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("banner", action, "design", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("banner", action, "design", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_ID_BYTES && !has_control(s)
}

fn layer_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| LAYER_KEYS.contains(&k.as_str()))
}

fn parse(raw: &str) -> (BannerDoc, Vec<String>) {
    let mut lines = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (BannerDoc::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (BannerDoc::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (BannerDoc::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (BannerDoc::default(), lines);
    }
    let arr = match obj.get("layers").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "layers_not_array"));
            return (BannerDoc::default(), lines);
        }
    };
    let recent_raw = match obj.get("recent").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "recent_not_array"));
            return (BannerDoc::default(), lines);
        }
    };

    let mut layers: Vec<Layer> = Vec::new();
    for (i, item) in arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if layer_keys_ok(e) => e,
            _ => {
                lines.push(degrade("layer", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let pattern = match entry.get("pattern").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("layer", &format!("index={} bad_pattern", i)));
                continue;
            }
        };
        let dye = match entry.get("dye").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("layer", &format!("index={} bad_dye", i)));
                continue;
            }
        };
        layers.push(Layer { pattern, dye });
    }
    if layers.len() > MAX_LAYERS {
        let excess = layers.len() - MAX_LAYERS;
        layers.truncate(MAX_LAYERS);
        lines.push(degrade("layer", &format!("overflow={}", excess)));
    }

    let mut recent: Vec<String> = Vec::new();
    for (i, item) in recent_raw.iter().enumerate() {
        let id = match item.as_str() {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("recent", &format!("index={} bad_id", i)));
                continue;
            }
        };
        if recent.contains(&id) {
            lines.push(degrade("recent", &format!("index={} duplicate_id", i)));
            continue;
        }
        recent.push(id);
    }
    if recent.len() > MAX_RECENT {
        let excess = recent.len() - MAX_RECENT;
        recent.truncate(MAX_RECENT);
        lines.push(degrade("recent", &format!("overflow={}", excess)));
    }

    (
        BannerDoc { layers, recent, undo: Vec::new(), redo: Vec::new() },
        lines,
    )
}

fn serialize(doc: &BannerDoc) -> Result<String> {
    let layers: Vec<Value> = doc
        .layers
        .iter()
        .map(|l| json!({"pattern": l.pattern, "dye": l.dye}))
        .collect();
    Ok(to_string(&json!({
        "schema": 1,
        "layers": layers,
        "recent": doc.recent,
    }))?)
}

fn write(root: &Path, doc: &BannerDoc) -> Result<()> {
    let body = serialize(doc)?;
    let path = robust::safe_join(root, BANNER_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", BANNER_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl BannerDoc {
    pub fn open(root: Option<&Path>) -> (BannerDoc, Vec<String>) {
        let Some(dir) = root else {
            return (BannerDoc::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, BANNER_FILE) {
            Ok(p) => p,
            Err(_) => return (BannerDoc::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (BannerDoc::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (BannerDoc::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    fn snapshot(&mut self) {
        if self.undo.len() >= MAX_HISTORY {
            self.undo.remove(0);
        }
        self.undo.push(self.layers.clone());
        self.redo.clear();
    }

    pub fn push_layer(&mut self, pattern: &str, dye: &str) -> bool {
        if !valid_id(pattern) || !valid_id(dye) || self.layers.len() >= MAX_LAYERS {
            return false;
        }
        self.snapshot();
        self.layers.push(Layer { pattern: pattern.to_string(), dye: dye.to_string() });
        true
    }

    pub fn replace_dye(&mut self, index: usize, dye: &str) -> bool {
        if !valid_id(dye) || index >= self.layers.len() {
            return false;
        }
        self.snapshot();
        self.layers[index].dye = dye.to_string();
        true
    }

    pub fn remove_layer(&mut self, index: usize) -> bool {
        if index >= self.layers.len() {
            return false;
        }
        self.snapshot();
        self.layers.remove(index);
        true
    }

    pub fn undo(&mut self) -> bool {
        let Some(prev) = self.undo.pop() else {
            return false;
        };
        let current = std::mem::replace(&mut self.layers, prev);
        if self.redo.len() >= MAX_HISTORY {
            self.redo.remove(0);
        }
        self.redo.push(current);
        true
    }

    pub fn redo(&mut self) -> bool {
        let Some(next) = self.redo.pop() else {
            return false;
        };
        let current = std::mem::replace(&mut self.layers, next);
        if self.undo.len() >= MAX_HISTORY {
            self.undo.remove(0);
        }
        self.undo.push(current);
        true
    }

    pub fn mark_edited(&mut self, id: &str) -> bool {
        if !valid_id(id) {
            return false;
        }
        self.recent.retain(|e| e != id);
        if self.recent.len() >= MAX_RECENT {
            self.recent.remove(0);
        }
        self.recent.push(id.to_string());
        true
    }

    pub fn undo_depth(&self) -> usize {
        self.undo.len()
    }

    pub fn redo_depth(&self) -> usize {
        self.redo.len()
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        Envelope::new(Kind::Event, BANNER_TARGET)
            .with("layers", &self.layers.len().to_string())
            .with("undo", &self.undo.len().to_string())
            .with("recent", &self.recent.len().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    BannerDoc::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu071-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn keys_and_bounds_are_explicit() {
        assert_eq!(KNOWN_KEYS.len(), 3);
        assert_eq!(LAYER_KEYS.len(), 2);
        assert_eq!(MAX_LAYERS, 32);
        assert_eq!(MAX_HISTORY, 64);
        assert_eq!(MAX_RECENT, 32);
        assert!(KNOWN_KEYS.contains(&"schema"));
        assert!(LAYER_KEYS.contains(&"dye"));
    }

    #[test]
    fn default_is_empty_with_empty_stacks() {
        let (d, lines) = BannerDoc::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(d, BannerDoc::default());
        assert!(d.layers.is_empty());
        assert!(d.recent.is_empty());
        assert_eq!(d.undo_depth(), 0);
        assert_eq!(d.redo_depth(), 0);
    }

    #[test]
    fn eight_bad_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(BANNER_FILE);
        let cases = [
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            r#"{"schema":1,"layers":[],"recent":[],"extra":1}"#.to_string(),
            r#"{"schema":2,"layers":[],"recent":[]}"#.to_string(),
            r#"{"schema":1,"layers":"no","recent":[]}"#.to_string(),
            r#"{"schema":1,"layers":[],"recent":"no"}"#.to_string(),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (d, lines) = BannerDoc::open(Some(&r));
            assert_eq!(d, BannerDoc::default(), "case={}", &raw[..raw.len().min(24)]);
            assert!(lines.iter().any(|l| l.contains("DEGRADE")), "case={}", &raw[..raw.len().min(24)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_layer_and_recent_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"layers":[{"pattern":"p1","dye":"d1"},7,{"pattern":"","dye":"d2"},{"pattern":"p2","dye":""},{"pattern":"p3","dye":"d3"},{"pattern":"p4","dye":"d4","z":1}],"recent":["a",7,"","a","b"]}"#;
        fs::write(r.join(BANNER_FILE), raw).unwrap();
        let (d, lines) = BannerDoc::open(Some(&r));
        assert_eq!(d.layers.len(), 2);
        assert_eq!(d.layers[0].pattern, "p1");
        assert_eq!(d.layers[1].pattern, "p3");
        assert_eq!(d.recent, vec!["a".to_string(), "b".to_string()]);
        assert!(lines.iter().any(|l| l.contains("bad_shape")));
        assert!(lines.iter().any(|l| l.contains("bad_pattern")));
        assert!(lines.iter().any(|l| l.contains("bad_dye")));
        assert!(lines.iter().any(|l| l.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn push_replace_remove_and_bounds() {
        let mut d = BannerDoc::default();
        assert!(d.push_layer("p1", "d1"));
        assert!(d.push_layer("p2", "d2"));
        assert!(!d.push_layer("", "d3"));
        assert!(!d.push_layer("p3", "bad\nid"));
        assert_eq!(d.layers.len(), 2);
        assert!(d.replace_dye(0, "d9"));
        assert!(!d.replace_dye(99, "d9"));
        assert!(!d.replace_dye(0, ""));
        assert_eq!(d.layers[0].dye, "d9");
        assert!(d.remove_layer(1));
        assert!(!d.remove_layer(50));
        assert_eq!(d.layers.len(), 1);
        for i in 0..(MAX_LAYERS + 5) {
            d.push_layer(&format!("p{}", i), "d");
        }
        assert_eq!(d.layers.len(), MAX_LAYERS);
    }

    #[test]
    fn undo_redo_and_branch_invalidation() {
        let mut d = BannerDoc::default();
        assert!(!d.undo());
        assert!(!d.redo());
        assert!(d.push_layer("p1", "d1"));
        assert!(d.push_layer("p2", "d2"));
        assert_eq!(d.undo_depth(), 2);
        assert!(d.undo());
        assert_eq!(d.layers.len(), 1);
        assert_eq!(d.redo_depth(), 1);
        assert!(d.redo());
        assert_eq!(d.layers.len(), 2);
        assert!(d.undo());
        assert!(d.push_layer("p3", "d3"));
        assert_eq!(d.redo_depth(), 0);
        assert!(!d.redo());
        assert_eq!(d.layers.len(), 2);
        assert_eq!(d.layers[1].pattern, "p3");
    }

    #[test]
    fn history_stacks_stay_bounded() {
        let mut d = BannerDoc::default();
        assert!(d.push_layer("p0", "d0"));
        for i in 0..(MAX_HISTORY + 20) {
            assert!(d.replace_dye(0, &format!("d{}", i)));
        }
        assert_eq!(d.undo_depth(), MAX_HISTORY);
        for _ in 0..MAX_HISTORY {
            assert!(d.undo());
        }
        assert_eq!(d.redo_depth(), MAX_HISTORY);
        assert!(!d.undo());
        for _ in 0..MAX_HISTORY {
            assert!(d.redo());
        }
        assert_eq!(d.undo_depth(), MAX_HISTORY);
        assert_eq!(d.redo_depth(), 0);
    }

    #[test]
    fn mark_edited_dedups_and_bounds() {
        let mut d = BannerDoc::default();
        assert!(d.mark_edited("a"));
        assert!(d.mark_edited("b"));
        assert!(d.mark_edited("a"));
        assert_eq!(d.recent, vec!["b".to_string(), "a".to_string()]);
        assert!(!d.mark_edited(""));
        for i in 0..(MAX_RECENT + 5) {
            assert!(d.mark_edited(&format!("id{}", i)));
        }
        assert_eq!(d.recent.len(), MAX_RECENT);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut d = BannerDoc::default();
        d.push_layer("p", "d");
        assert!(d.persist(None)[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn persist_reopen_reset_keep_protected_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let mut d = BannerDoc::default();
        d.push_layer("p1", "d1");
        d.push_layer("p2", "d2");
        d.mark_edited("design-a");
        assert!(d.persist(Some(&r)).is_empty());
        let (back, lines) = BannerDoc::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.layers.len(), 2);
        assert_eq!(back.layers[1].dye, "d2");
        assert_eq!(back.recent, vec!["design-a".to_string()]);
        assert_eq!(back.undo_depth(), 0);
        assert_eq!(back.redo_depth(), 0);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = BannerDoc::open(Some(&r));
        assert_eq!(def, BannerDoc::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope() {
        let mut d = BannerDoc::default();
        d.push_layer("p1", "d1");
        d.push_layer("p2", "d2");
        d.mark_edited("design-a");
        let e = d.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, BANNER_TARGET);
        assert_eq!(e.field("layers"), Some("2"));
        assert_eq!(e.field("undo"), Some("2"));
        assert_eq!(e.field("recent"), Some("1"));
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 3);
    }

    #[test]
    fn serialize_carries_no_external_format_values() {
        let mut d = BannerDoc::default();
        d.push_layer("p1", "d1");
        d.mark_edited("design-a");
        let raw = serialize(&d).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 3);
        assert!(!raw.contains("give"));
        assert!(!raw.contains("minecraft"));
        assert!(!raw.contains("undo"));
        assert!(!raw.contains("redo"));
    }
}

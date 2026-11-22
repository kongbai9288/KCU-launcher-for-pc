use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const WIDGET_FILE: &str = "widget-layout.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"mode":"compact","slots":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_SLOTS: usize = 32;
pub const WIDGET_TARGET: &str = "widget.layout";
pub const KNOWN_KEYS: &[&str] = &["schema", "mode", "slots"];
pub const SLOT_KEYS: &[&str] = &["id", "pinned"];
pub const MODES: &[&str] = &["compact", "custom"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LayoutMode {
    Compact,
    Custom,
}

impl LayoutMode {
    pub fn code(&self) -> &'static str {
        match self {
            LayoutMode::Compact => "compact",
            LayoutMode::Custom => "custom",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "compact" => Some(LayoutMode::Compact),
            "custom" => Some(LayoutMode::Custom),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Slot {
    pub id: String,
    pub pinned: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WidgetLayout {
    pub mode: LayoutMode,
    pub slots: Vec<Slot>,
}

impl Default for WidgetLayout {
    fn default() -> Self {
        WidgetLayout { mode: LayoutMode::Compact, slots: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("widget", action, "layout", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("widget", action, "layout", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_ID_BYTES && !has_control(s)
}

fn slot_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| SLOT_KEYS.contains(&k.as_str()))
}

fn parse(raw: &str) -> (WidgetLayout, Vec<String>) {
    let mut lines = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (WidgetLayout::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (WidgetLayout::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (WidgetLayout::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (WidgetLayout::default(), lines);
    }
    let mode = match obj.get("mode").and_then(Value::as_str).and_then(LayoutMode::parse) {
        Some(m) => m,
        None => {
            lines.push(degrade("load", "mode_invalid"));
            return (WidgetLayout::default(), lines);
        }
    };
    let arr = match obj.get("slots").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "slots_not_array"));
            return (WidgetLayout::default(), lines);
        }
    };
    let mut slots: Vec<Slot> = Vec::new();
    for (i, item) in arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if slot_keys_ok(e) => e,
            _ => {
                lines.push(degrade("slot", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("slot", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let pinned = match entry.get("pinned").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("slot", &format!("index={} bad_pinned", i)));
                continue;
            }
        };
        if slots.iter().any(|s| s.id == id) {
            lines.push(degrade("slot", &format!("index={} duplicate_id", i)));
            continue;
        }
        slots.push(Slot { id, pinned });
    }
    if slots.len() > MAX_SLOTS {
        let excess = slots.len() - MAX_SLOTS;
        slots.truncate(MAX_SLOTS);
        lines.push(degrade("slot", &format!("overflow={}", excess)));
    }
    (WidgetLayout { mode, slots }, lines)
}

fn serialize(layout: &WidgetLayout) -> Result<String> {
    let slots: Vec<Value> = layout
        .slots
        .iter()
        .map(|s| json!({"id": s.id, "pinned": s.pinned}))
        .collect();
    Ok(to_string(&json!({
        "schema": 1,
        "mode": layout.mode.code(),
        "slots": slots,
    }))?)
}

fn write(root: &Path, layout: &WidgetLayout) -> Result<()> {
    let body = serialize(layout)?;
    let path = robust::safe_join(root, WIDGET_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", WIDGET_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl WidgetLayout {
    pub fn open(root: Option<&Path>) -> (WidgetLayout, Vec<String>) {
        let Some(dir) = root else {
            return (WidgetLayout::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, WIDGET_FILE) {
            Ok(p) => p,
            Err(_) => return (WidgetLayout::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (WidgetLayout::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (WidgetLayout::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn add(&mut self, id: &str, pinned: bool) -> bool {
        if !valid_id(id) || self.slots.len() >= MAX_SLOTS || self.slots.iter().any(|s| s.id == id) {
            return false;
        }
        self.slots.push(Slot { id: id.to_string(), pinned });
        true
    }

    pub fn remove(&mut self, id: &str) -> bool {
        let before = self.slots.len();
        self.slots.retain(|s| s.id != id);
        self.slots.len() != before
    }

    pub fn move_to(&mut self, id: &str, index: usize) -> bool {
        if index >= self.slots.len() {
            return false;
        }
        let Some(pos) = self.slots.iter().position(|s| s.id == id) else {
            return false;
        };
        let slot = self.slots.remove(pos);
        self.slots.insert(index, slot);
        true
    }

    pub fn toggle_pin(&mut self, id: &str) -> bool {
        let Some(slot) = self.slots.iter_mut().find(|s| s.id == id) else {
            return false;
        };
        slot.pinned = !slot.pinned;
        true
    }

    pub fn set_mode(&mut self, mode: LayoutMode) {
        self.mode = mode;
    }

    pub fn pinned_count(&self) -> usize {
        self.slots.iter().filter(|s| s.pinned).count()
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        Envelope::new(Kind::Event, WIDGET_TARGET)
            .with("mode", self.mode.code())
            .with("slots", &self.slots.len().to_string())
            .with("pinned", &self.pinned_count().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    WidgetLayout::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu072-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn mode_codes_and_keys_are_explicit() {
        assert_eq!(LayoutMode::Compact.code(), "compact");
        assert_eq!(LayoutMode::Custom.code(), "custom");
        assert_eq!(LayoutMode::parse("nope"), None);
        assert_eq!(MODES.len(), 2);
        assert_eq!(KNOWN_KEYS.len(), 3);
        assert_eq!(SLOT_KEYS.len(), 2);
        assert_eq!(MAX_SLOTS, 32);
    }

    #[test]
    fn default_is_compact_empty() {
        let (l, lines) = WidgetLayout::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(l, WidgetLayout::default());
        assert_eq!(l.mode, LayoutMode::Compact);
        assert!(l.slots.is_empty());
    }

    #[test]
    fn eight_bad_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(WIDGET_FILE);
        let cases = [
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            r#"{"schema":1,"mode":"compact","slots":[],"extra":1}"#.to_string(),
            r#"{"schema":2,"mode":"compact","slots":[]}"#.to_string(),
            r#"{"schema":1,"mode":"nope","slots":[]}"#.to_string(),
            r#"{"schema":1,"mode":"compact","slots":"no"}"#.to_string(),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (l, lines) = WidgetLayout::open(Some(&r));
            assert_eq!(l, WidgetLayout::default(), "case={}", &raw[..raw.len().min(24)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(24)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_slot_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"mode":"custom","slots":[{"id":"a","pinned":true},7,{"id":"","pinned":false},{"id":"b","pinned":"no"},{"id":"c","pinned":false},{"id":"a","pinned":false}]}"#;
        fs::write(r.join(WIDGET_FILE), raw).unwrap();
        let (l, lines) = WidgetLayout::open(Some(&r));
        assert_eq!(l.mode, LayoutMode::Custom);
        assert_eq!(l.slots.len(), 2);
        assert_eq!(l.slots[0].id, "a");
        assert!(l.slots[0].pinned);
        assert_eq!(l.slots[1].id, "c");
        assert!(lines.iter().any(|x| x.contains("bad_shape")));
        assert!(lines.iter().any(|x| x.contains("bad_id")));
        assert!(lines.iter().any(|x| x.contains("bad_pinned")));
        assert!(lines.iter().any(|x| x.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn add_remove_and_bound() {
        let mut l = WidgetLayout::default();
        assert!(l.add("w1", true));
        assert!(l.add("w2", false));
        assert!(!l.add("w1", false));
        assert!(!l.add("", false));
        assert!(!l.add("bad\nid", false));
        assert!(l.remove("w1"));
        assert!(!l.remove("missing"));
        assert_eq!(l.slots.len(), 1);
        for i in 0..(MAX_SLOTS + 5) {
            l.add(&format!("w{}", i), false);
        }
        assert_eq!(l.slots.len(), MAX_SLOTS);
    }

    #[test]
    fn move_to_reorders_and_rejects_out_of_range() {
        let mut l = WidgetLayout::default();
        l.add("a", false);
        l.add("b", false);
        l.add("c", false);
        assert!(l.move_to("c", 0));
        assert_eq!(l.slots.iter().map(|s| s.id.as_str()).collect::<Vec<_>>(), vec!["c", "a", "b"]);
        assert!(!l.move_to("missing", 0));
        assert!(!l.move_to("a", 99));
        assert_eq!(l.slots.iter().map(|s| s.id.as_str()).collect::<Vec<_>>(), vec!["c", "a", "b"]);
    }

    #[test]
    fn toggle_pin_and_set_mode() {
        let mut l = WidgetLayout::default();
        l.add("a", false);
        assert!(l.toggle_pin("a"));
        assert_eq!(l.pinned_count(), 1);
        assert!(l.toggle_pin("a"));
        assert_eq!(l.pinned_count(), 0);
        assert!(!l.toggle_pin("missing"));
        l.set_mode(LayoutMode::Custom);
        assert_eq!(l.mode, LayoutMode::Custom);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut l = WidgetLayout::default();
        l.add("a", true);
        assert!(l.persist(None)[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn persist_reopen_reset_keep_protected_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let mut l = WidgetLayout::default();
        l.set_mode(LayoutMode::Custom);
        l.add("a", true);
        l.add("b", false);
        assert!(l.move_to("b", 0));
        assert!(l.persist(Some(&r)).is_empty());
        let (back, lines) = WidgetLayout::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.mode, LayoutMode::Custom);
        assert_eq!(back.slots.len(), 2);
        assert_eq!(back.slots[0].id, "b");
        assert!(back.slots[1].pinned);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = WidgetLayout::open(Some(&r));
        assert_eq!(def, WidgetLayout::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope() {
        let mut l = WidgetLayout::default();
        l.set_mode(LayoutMode::Custom);
        l.add("a", true);
        l.add("b", false);
        let e = l.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, WIDGET_TARGET);
        assert_eq!(e.field("mode"), Some("custom"));
        assert_eq!(e.field("slots"), Some("2"));
        assert_eq!(e.field("pinned"), Some("1"));
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 3);
    }

    #[test]
    fn serialize_carries_no_widget_type_table() {
        let mut l = WidgetLayout::default();
        l.add("a", true);
        let raw = serialize(&l).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 3);
        assert!(!raw.contains("calendar"));
        assert!(!raw.contains("greeting"));
        assert!(!raw.contains("recent_world"));
        assert!(!raw.contains("minecraft"));
    }
}

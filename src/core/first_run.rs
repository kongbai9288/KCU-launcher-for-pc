use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const FIRST_RUN_FILE: &str = "first-run.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"cursor":0,"finished":false,"steps":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_STEPS: usize = 12;
pub const FIRST_RUN_TARGET: &str = "first_run.wizard";
pub const KNOWN_KEYS: &[&str] = &["schema", "cursor", "finished", "steps"];
pub const STEP_KEYS: &[&str] = &["id", "required", "state"];
pub const STATES: &[&str] = &["pending", "done", "skipped"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum StepState {
    Pending,
    Done,
    Skipped,
}

impl StepState {
    pub fn code(&self) -> &'static str {
        match self {
            StepState::Pending => "pending",
            StepState::Done => "done",
            StepState::Skipped => "skipped",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "pending" => Some(StepState::Pending),
            "done" => Some(StepState::Done),
            "skipped" => Some(StepState::Skipped),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Step {
    pub id: String,
    pub required: bool,
    pub state: StepState,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Wizard {
    pub cursor: usize,
    pub finished: bool,
    pub steps: Vec<Step>,
}

impl Default for Wizard {
    fn default() -> Self {
        Wizard { cursor: 0, finished: false, steps: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("first_run", action, "wizard", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("first_run", action, "wizard", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_ID_BYTES && !has_control(s)
}

fn step_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| STEP_KEYS.contains(&k.as_str()))
}

fn parse(raw: &str) -> (Wizard, Vec<String>) {
    let mut lines = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (Wizard::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (Wizard::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (Wizard::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (Wizard::default(), lines);
    }
    let cursor = match obj.get("cursor").and_then(Value::as_u64) {
        Some(v) => usize::try_from(v).unwrap_or(usize::MAX),
        None => {
            lines.push(degrade("load", "cursor_not_u64"));
            return (Wizard::default(), lines);
        }
    };
    let finished = match obj.get("finished").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "finished_not_bool"));
            return (Wizard::default(), lines);
        }
    };
    let arr = match obj.get("steps").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "steps_not_array"));
            return (Wizard::default(), lines);
        }
    };
    let mut steps: Vec<Step> = Vec::new();
    for (i, item) in arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if step_keys_ok(e) => e,
            _ => {
                lines.push(degrade("step", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            _ => {
                lines.push(degrade("step", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let required = match entry.get("required").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("step", &format!("index={} bad_required", i)));
                continue;
            }
        };
        let state = match entry.get("state").and_then(Value::as_str).and_then(StepState::parse) {
            Some(s) => s,
            None => {
                lines.push(degrade("step", &format!("index={} bad_state", i)));
                continue;
            }
        };
        if steps.iter().any(|s| s.id == id) {
            lines.push(degrade("step", &format!("index={} duplicate_id", i)));
            continue;
        }
        steps.push(Step { id, required, state });
    }
    if steps.len() > MAX_STEPS {
        let excess = steps.len() - MAX_STEPS;
        steps.truncate(MAX_STEPS);
        lines.push(degrade("step", &format!("overflow={}", excess)));
    }
    if cursor > steps.len() {
        lines.push(degrade("load", "cursor_out_of_range"));
        return (Wizard::default(), lines);
    }
    (Wizard { cursor, finished, steps }, lines)
}

fn serialize(w: &Wizard) -> Result<String> {
    let steps: Vec<Value> = w
        .steps
        .iter()
        .map(|s| json!({"id": s.id, "required": s.required, "state": s.state.code()}))
        .collect();
    Ok(to_string(&json!({
        "schema": 1,
        "cursor": w.cursor,
        "finished": w.finished,
        "steps": steps,
    }))?)
}

fn write(root: &Path, w: &Wizard) -> Result<()> {
    let body = serialize(w)?;
    let path = robust::safe_join(root, FIRST_RUN_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", FIRST_RUN_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl Wizard {
    pub fn open(root: Option<&Path>) -> (Wizard, Vec<String>) {
        let Some(dir) = root else {
            return (Wizard::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, FIRST_RUN_FILE) {
            Ok(p) => p,
            Err(_) => return (Wizard::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (Wizard::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (Wizard::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn add_step(&mut self, id: &str, required: bool) -> bool {
        if !valid_id(id) || self.steps.len() >= MAX_STEPS || self.steps.iter().any(|s| s.id == id) {
            return false;
        }
        self.steps.push(Step { id: id.to_string(), required, state: StepState::Pending });
        true
    }

    pub fn remove_step(&mut self, id: &str) -> bool {
        let before = self.steps.len();
        self.steps.retain(|s| s.id != id);
        if self.steps.len() == before {
            return false;
        }
        if self.cursor > self.steps.len() {
            self.cursor = self.steps.len();
        }
        true
    }

    pub fn advance(&mut self) -> bool {
        if self.cursor >= self.steps.len() {
            return false;
        }
        if self.steps[self.cursor].state != StepState::Skipped {
            self.steps[self.cursor].state = StepState::Done;
        }
        self.cursor += 1;
        true
    }

    pub fn back(&mut self) -> bool {
        if self.cursor == 0 {
            return false;
        }
        self.cursor -= 1;
        true
    }

    pub fn skip(&mut self, id: &str) -> bool {
        let Some(s) = self.steps.iter_mut().find(|s| s.id == id) else {
            return false;
        };
        if s.required {
            return false;
        }
        s.state = StepState::Skipped;
        true
    }

    pub fn set_state(&mut self, id: &str, state: StepState) -> bool {
        let Some(s) = self.steps.iter_mut().find(|s| s.id == id) else {
            return false;
        };
        s.state = state;
        true
    }

    pub fn set_finished(&mut self, on: bool) {
        self.finished = on;
    }

    pub fn pending_required(&self) -> usize {
        self.steps[self.cursor.min(self.steps.len())..]
            .iter()
            .filter(|s| s.required && s.state != StepState::Done)
            .count()
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        Envelope::new(Kind::Event, FIRST_RUN_TARGET)
            .with("cursor", &self.cursor.to_string())
            .with("steps", &self.steps.len().to_string())
            .with("finished", &self.finished.to_string())
            .with("pending", &self.pending_required().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    Wizard::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu074-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"cursor":0,"finished":false,"steps":[]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 4);
    }

    #[test]
    fn enum_codes_and_keys_are_explicit() {
        assert_eq!(StepState::Pending.code(), "pending");
        assert_eq!(StepState::Done.code(), "done");
        assert_eq!(StepState::Skipped.code(), "skipped");
        assert_eq!(StepState::parse("nope"), None);
        assert_eq!(STATES.len(), 3);
        assert_eq!(KNOWN_KEYS.len(), 4);
        assert_eq!(STEP_KEYS.len(), 3);
        assert_eq!(MAX_STEPS, 12);
    }

    #[test]
    fn default_is_zero_pending() {
        let (w, lines) = Wizard::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(w, Wizard::default());
        assert_eq!(w.cursor, 0);
        assert!(!w.finished);
        assert!(w.steps.is_empty());
        assert_eq!(w.pending_required(), 0);
    }

    #[test]
    fn nine_bad_root_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(FIRST_RUN_FILE);
        let base = r#"{"schema":1,"cursor":0,"finished":false,"steps":[]}"#;
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            base.replace("\"steps\":[]", "\"steps\":[],\"extra\":1"),
            base.replace("\"schema\":1", "\"schema\":2"),
            base.replace("\"cursor\":0", "\"cursor\":-1"),
            base.replace("\"finished\":false", "\"finished\":\"no\""),
            base.replace("\"steps\":[]", "\"steps\":\"no\""),
            r#"{"schema":1,"cursor":9,"finished":false,"steps":[]}"#.to_string(),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (w, lines) = Wizard::open(Some(&r));
            assert_eq!(w, Wizard::default(), "case={}", &raw[..raw.len().min(28)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(28)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_step_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"cursor":1,"finished":false,"steps":[{"id":"a","required":true,"state":"pending"},7,{"id":"","required":false,"state":"done"},{"id":"b","required":"no","state":"done"},{"id":"c","required":false,"state":"nope"},{"id":"d","required":false,"state":"done","z":1},{"id":"a","required":false,"state":"done"}]}"#;
        fs::write(r.join(FIRST_RUN_FILE), raw).unwrap();
        let (w, lines) = Wizard::open(Some(&r));
        assert_eq!(w.cursor, 1);
        assert_eq!(w.steps.len(), 1);
        assert_eq!(w.steps[0].id, "a");
        assert_eq!(w.steps[0].state, StepState::Pending);
        assert!(lines.iter().any(|x| x.contains("bad_shape")));
        assert!(lines.iter().any(|x| x.contains("bad_id")));
        assert!(lines.iter().any(|x| x.contains("bad_required")));
        assert!(lines.iter().any(|x| x.contains("bad_state")));
        assert!(lines.iter().any(|x| x.contains("duplicate_id")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn add_remove_and_bound() {
        let mut w = Wizard::default();
        assert!(w.add_step("s1", true));
        assert!(w.add_step("s2", false));
        assert!(!w.add_step("s1", false));
        assert!(!w.add_step("", false));
        assert!(!w.add_step("bad\nid", false));
        assert!(w.remove_step("s1"));
        assert!(!w.remove_step("missing"));
        assert_eq!(w.steps.len(), 1);
        for i in 0..(MAX_STEPS + 5) {
            w.add_step(&format!("w{}", i), false);
        }
        assert_eq!(w.steps.len(), MAX_STEPS);
    }

    #[test]
    fn advance_back_and_state_transitions() {
        let mut w = Wizard::default();
        w.add_step("a", true);
        w.add_step("b", false);
        w.add_step("c", false);
        assert_eq!(w.pending_required(), 1);
        assert!(w.advance());
        assert_eq!(w.cursor, 1);
        assert_eq!(w.steps[0].state, StepState::Done);
        assert_eq!(w.pending_required(), 0);
        assert!(w.back());
        assert_eq!(w.cursor, 0);
        assert!(!w.back());
        assert!(w.advance());
        assert!(w.skip("b"));
        assert_eq!(w.steps[1].state, StepState::Skipped);
        assert!(w.advance());
        assert_eq!(w.steps[1].state, StepState::Skipped);
        assert_eq!(w.cursor, 2);
        assert!(w.advance());
        assert_eq!(w.cursor, 3);
        assert!(!w.advance());
        assert_eq!(w.steps[2].state, StepState::Done);
    }

    #[test]
    fn required_step_cannot_be_skipped() {
        let mut w = Wizard::default();
        w.add_step("a", true);
        w.add_step("b", false);
        assert!(!w.skip("a"));
        assert_eq!(w.steps[0].state, StepState::Pending);
        assert!(w.skip("b"));
        assert_eq!(w.steps[1].state, StepState::Skipped);
        assert!(!w.skip("missing"));
        assert!(w.set_state("a", StepState::Done));
        assert!(!w.set_state("missing", StepState::Done));
    }

    #[test]
    fn remove_step_clamps_cursor() {
        let mut w = Wizard::default();
        w.add_step("a", false);
        w.add_step("b", false);
        w.add_step("c", false);
        assert!(w.advance());
        assert!(w.advance());
        assert_eq!(w.cursor, 2);
        assert!(w.remove_step("c"));
        assert_eq!(w.cursor, 2);
        assert!(w.remove_step("b"));
        assert_eq!(w.cursor, 1);
    }

    #[test]
    fn bounded_overflow_from_disk() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let mut body = String::from(r#"{"schema":1,"cursor":0,"finished":true,"steps":["#);
        for i in 0..(MAX_STEPS + 3) {
            if i > 0 { body.push(','); }
            body.push_str(&format!(r#"{{"id":"q{}","required":false,"state":"pending"}}"#, i));
        }
        body.push_str("]}");
        fs::write(r.join(FIRST_RUN_FILE), body).unwrap();
        let (w, lines) = Wizard::open(Some(&r));
        assert_eq!(w.steps.len(), MAX_STEPS);
        assert!(w.finished);
        assert!(lines.iter().any(|x| x.contains("overflow=3")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut w = Wizard::default();
        w.add_step("a", true);
        assert!(w.persist(None)[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn persist_reopen_reset_keep_protected_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let mut w = Wizard::default();
        w.add_step("a", true);
        w.add_step("b", false);
        assert!(w.advance());
        assert!(w.skip("b"));
        w.set_finished(true);
        assert!(w.persist(Some(&r)).is_empty());
        let (back, lines) = Wizard::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.cursor, 1);
        assert!(back.finished);
        assert_eq!(back.steps.len(), 2);
        assert_eq!(back.steps[0].state, StepState::Done);
        assert_eq!(back.steps[1].state, StepState::Skipped);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = Wizard::open(Some(&r));
        assert_eq!(def, Wizard::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope_without_ids() {
        let mut w = Wizard::default();
        w.add_step("a", true);
        w.add_step("b", false);
        assert!(w.advance());
        w.set_finished(true);
        let e = w.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, FIRST_RUN_TARGET);
        assert_eq!(e.field("cursor"), Some("1"));
        assert_eq!(e.field("steps"), Some("2"));
        assert_eq!(e.field("finished"), Some("true"));
        assert_eq!(e.field("pending"), Some("0"));
        assert_eq!(e.field("ids"), None);
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 4);
    }

    #[test]
    fn serialize_carries_no_step_table() {
        let mut w = Wizard::default();
        w.add_step("a", true);
        let raw = serialize(&w).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 4);
        assert!(!raw.contains("language"));
        assert!(!raw.contains("account"));
        assert!(!raw.contains("java"));
        assert!(!raw.contains("minecraft"));
    }
}

use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const SEED_ACCESS_FILE: &str = "seed-access.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"guest_mode":false,"password_required":false,"records":[],"audit":[],"locked_features":[],"command_deny":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_RECORDS: usize = 24;
pub const MAX_AUDIT: usize = 64;
pub const MAX_LOCKED: usize = 32;
pub const MAX_DENY: usize = 32;
pub const EVENT_TARGET: &str = "instance.seed_access";
pub const KNOWN_KEYS: &[&str] = &["schema", "guest_mode", "password_required", "records", "audit", "locked_features", "command_deny"];
pub const SEED_KEYS: &[&str] = &["instance_id", "value", "policy", "note"];
pub const AUDIT_KEYS: &[&str] = &["id", "action", "target", "scope"];
pub const POLICIES: &[&str] = &["visible", "hint", "hidden"];
pub const ACTIONS: &[&str] = &["view", "policy_change", "guest_toggle", "hidden"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SeedPolicy {
    Visible,
    Hint,
    Hidden,
}

impl SeedPolicy {
    pub fn code(&self) -> &'static str {
        match self {
            SeedPolicy::Visible => "visible",
            SeedPolicy::Hint => "hint",
            SeedPolicy::Hidden => "hidden",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "visible" => Some(SeedPolicy::Visible),
            "hint" => Some(SeedPolicy::Hint),
            "hidden" => Some(SeedPolicy::Hidden),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AuditAction {
    View,
    PolicyChange,
    GuestToggle,
    Hidden,
}

impl AuditAction {
    pub fn code(&self) -> &'static str {
        match self {
            AuditAction::View => "view",
            AuditAction::PolicyChange => "policy_change",
            AuditAction::GuestToggle => "guest_toggle",
            AuditAction::Hidden => "hidden",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "view" => Some(AuditAction::View),
            "policy_change" => Some(AuditAction::PolicyChange),
            "guest_toggle" => Some(AuditAction::GuestToggle),
            "hidden" => Some(AuditAction::Hidden),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SeedRecord {
    pub instance_id: String,
    pub value: String,
    pub policy: SeedPolicy,
    pub note: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AuditEntry {
    pub id: String,
    pub action: AuditAction,
    pub target: String,
    pub scope: String,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SeedWorkspace {
    pub guest_mode: bool,
    pub password_required: bool,
    pub records: Vec<SeedRecord>,
    pub audit: Vec<AuditEntry>,
    pub locked_features: Vec<String>,
    pub command_deny: Vec<String>,
}

impl Default for SeedWorkspace {
    fn default() -> Self {
        SeedWorkspace {
            guest_mode: false,
            password_required: false,
            records: Vec::new(),
            audit: Vec::new(),
            locked_features: Vec::new(),
            command_deny: Vec::new(),
        }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("instance", action, "seed_access", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("instance", action, "seed_access", "ERROR", reason)
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

fn seed_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| SEED_KEYS.contains(&k.as_str()))
}

fn audit_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| AUDIT_KEYS.contains(&k.as_str()))
}

fn policy_note_pair_ok(policy: SeedPolicy, note: &str) -> bool {
    if policy == SeedPolicy::Hint {
        !note.is_empty()
    } else {
        note.is_empty()
    }
}

fn parse_strings(arr: &[Value], label: &str, cap: usize, lines: &mut Vec<String>) -> Vec<String> {
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
    if out.len() > cap {
        let excess = out.len() - cap;
        out.truncate(cap);
        lines.push(degrade(label, &format!("overflow={}", excess)));
    }
    out
}

fn parse(raw: &str) -> (SeedWorkspace, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (SeedWorkspace::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (SeedWorkspace::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (SeedWorkspace::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (SeedWorkspace::default(), lines);
    }
    let guest_mode = match obj.get("guest_mode").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "guest_not_bool"));
            return (SeedWorkspace::default(), lines);
        }
    };
    let password_required = match obj.get("password_required").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "password_not_bool"));
            return (SeedWorkspace::default(), lines);
        }
    };
    let rec_arr = match obj.get("records").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "records_not_array"));
            return (SeedWorkspace::default(), lines);
        }
    };
    let mut records: Vec<SeedRecord> = Vec::new();
    for (i, item) in rec_arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if seed_keys_ok(e) => e,
            _ => {
                lines.push(degrade("record", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let instance_id = match entry.get("instance_id").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("record", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let val = match entry.get("value").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("record", &format!("index={} bad_value", i)));
                continue;
            }
        };
        let policy = match entry.get("policy").and_then(Value::as_str).and_then(SeedPolicy::parse) {
            Some(p) => p,
            None => {
                lines.push(degrade("record", &format!("index={} bad_policy", i)));
                continue;
            }
        };
        let note = match entry.get("note").and_then(Value::as_str) {
            Some(s) if valid_optional_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("record", &format!("index={} bad_note", i)));
                continue;
            }
        };
        if !policy_note_pair_ok(policy, &note) {
            lines.push(degrade("record", &format!("index={} bad_policy_note_pair", i)));
            continue;
        }
        if records.iter().any(|r| r.instance_id == instance_id) {
            lines.push(degrade("record", &format!("index={} duplicate_id", i)));
            continue;
        }
        records.push(SeedRecord { instance_id, value: val, policy, note });
    }
    if records.len() > MAX_RECORDS {
        let excess = records.len() - MAX_RECORDS;
        records.truncate(MAX_RECORDS);
        lines.push(degrade("record", &format!("overflow={}", excess)));
    }
    let au_arr = match obj.get("audit").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "audit_not_array"));
            return (SeedWorkspace::default(), lines);
        }
    };
    let mut audit: Vec<AuditEntry> = Vec::new();
    for (i, item) in au_arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if audit_keys_ok(e) => e,
            _ => {
                lines.push(degrade("audit", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("audit", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let action = match entry.get("action").and_then(Value::as_str).and_then(AuditAction::parse) {
            Some(a) => a,
            None => {
                lines.push(degrade("audit", &format!("index={} bad_action", i)));
                continue;
            }
        };
        let target = match entry.get("target").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("audit", &format!("index={} bad_target", i)));
                continue;
            }
        };
        let scope = match entry.get("scope").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("audit", &format!("index={} bad_scope", i)));
                continue;
            }
        };
        if audit.iter().any(|a| a.id == id) {
            lines.push(degrade("audit", &format!("index={} duplicate_id", i)));
            continue;
        }
        audit.push(AuditEntry { id, action, target, scope });
    }
    if audit.len() > MAX_AUDIT {
        let excess = audit.len() - MAX_AUDIT;
        audit.truncate(MAX_AUDIT);
        lines.push(degrade("audit", &format!("overflow={}", excess)));
    }
    let locked_arr = match obj.get("locked_features").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "locked_not_array"));
            return (SeedWorkspace::default(), lines);
        }
    };
    let locked_features: Vec<String> = parse_strings(locked_arr, "locked", MAX_LOCKED, &mut lines);
    let deny_arr = match obj.get("command_deny").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "deny_not_array"));
            return (SeedWorkspace::default(), lines);
        }
    };
    let command_deny: Vec<String> = parse_strings(deny_arr, "deny", MAX_DENY, &mut lines);
    (SeedWorkspace { guest_mode, password_required, records, audit, locked_features, command_deny }, lines)
}

fn serialize(p: &SeedWorkspace) -> Result<String> {
    let records: Vec<Value> = p.records.iter().map(|r| json!({
        "instance_id": r.instance_id, "value": r.value,
        "policy": r.policy.code(), "note": r.note,
    })).collect();
    let audit: Vec<Value> = p.audit.iter().map(|a| json!({
        "id": a.id, "action": a.action.code(),
        "target": a.target, "scope": a.scope,
    })).collect();
    Ok(to_string(&json!({
        "schema": 1,
        "guest_mode": p.guest_mode,
        "password_required": p.password_required,
        "records": records,
        "audit": audit,
        "locked_features": p.locked_features,
        "command_deny": p.command_deny,
    }))?)
}

fn write(root: &Path, p: &SeedWorkspace) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, SEED_ACCESS_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", SEED_ACCESS_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

pub fn classify(policy: SeedPolicy, guest_mode: bool) -> SeedPolicy {
    match (policy, guest_mode) {
        (SeedPolicy::Visible, false) => SeedPolicy::Visible,
        (SeedPolicy::Visible, true) => SeedPolicy::Hidden,
        (SeedPolicy::Hint, false) => SeedPolicy::Hint,
        (SeedPolicy::Hint, true) => SeedPolicy::Hidden,
        (SeedPolicy::Hidden, false) => SeedPolicy::Hidden,
        (SeedPolicy::Hidden, true) => SeedPolicy::Hidden,
    }
}

impl SeedWorkspace {
    pub fn open(root: Option<&Path>) -> (SeedWorkspace, Vec<String>) {
        let Some(dir) = root else {
            return (SeedWorkspace::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, SEED_ACCESS_FILE) {
            Ok(p) => p,
            Err(_) => return (SeedWorkspace::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (SeedWorkspace::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (SeedWorkspace::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn add_record(&mut self, instance_id: &str, val: &str, policy: SeedPolicy, note: &str) -> bool {
        if !valid_text(instance_id) || !valid_text(val) || !valid_optional_text(note) {
            return false;
        }
        if !POLICIES.contains(&policy.code()) || !policy_note_pair_ok(policy, note) {
            return false;
        }
        if self.records.len() >= MAX_RECORDS || self.records.iter().any(|r| r.instance_id == instance_id) {
            return false;
        }
        self.records.push(SeedRecord {
            instance_id: instance_id.to_string(), value: val.to_string(), policy, note: note.to_string(),
        });
        true
    }

    pub fn remove_record(&mut self, instance_id: &str) -> bool {
        let before = self.records.len();
        self.records.retain(|r| r.instance_id != instance_id);
        self.records.len() != before
    }

    pub fn set_policy(&mut self, instance_id: &str, policy: SeedPolicy) -> bool {
        if !POLICIES.contains(&policy.code()) { return false; }
        let Some(r) = self.records.iter_mut().find(|r| r.instance_id == instance_id) else { return false; };
        if !policy_note_pair_ok(policy, &r.note) { return false; }
        r.policy = policy;
        true
    }

    pub fn set_note(&mut self, instance_id: &str, note: &str) -> bool {
        if !valid_optional_text(note) { return false; }
        let Some(r) = self.records.iter_mut().find(|r| r.instance_id == instance_id) else { return false; };
        if !policy_note_pair_ok(r.policy, note) { return false; }
        r.note = note.to_string();
        true
    }

    pub fn set_value(&mut self, instance_id: &str, val: &str) -> bool {
        if !valid_text(val) { return false; }
        let Some(r) = self.records.iter_mut().find(|r| r.instance_id == instance_id) else { return false; };
        r.value = val.to_string();
        true
    }

    pub fn add_audit(&mut self, id: &str, action: AuditAction, target: &str, scope: &str) -> bool {
        if !valid_text(id) || !valid_text(target) || !valid_text(scope) {
            return false;
        }
        if !ACTIONS.contains(&action.code()) {
            return false;
        }
        if self.audit.len() >= MAX_AUDIT || self.audit.iter().any(|a| a.id == id) {
            return false;
        }
        self.audit.push(AuditEntry {
            id: id.to_string(), action, target: target.to_string(), scope: scope.to_string(),
        });
        true
    }

    pub fn remove_audit(&mut self, id: &str) -> bool {
        let before = self.audit.len();
        self.audit.retain(|a| a.id != id);
        self.audit.len() != before
    }

    pub fn set_audit_action(&mut self, id: &str, action: AuditAction) -> bool {
        if !ACTIONS.contains(&action.code()) { return false; }
        let Some(a) = self.audit.iter_mut().find(|a| a.id == id) else { return false; };
        a.action = action;
        true
    }

    pub fn set_guest_mode(&mut self, on: bool) {
        self.guest_mode = on;
    }

    pub fn set_password_required(&mut self, on: bool) {
        self.password_required = on;
    }

    pub fn add_locked(&mut self, id: &str) -> bool {
        if !valid_text(id) || self.locked_features.len() >= MAX_LOCKED || self.locked_features.iter().any(|x| x == id) {
            return false;
        }
        self.locked_features.push(id.to_string());
        true
    }

    pub fn remove_locked(&mut self, id: &str) -> bool {
        let before = self.locked_features.len();
        self.locked_features.retain(|x| x != id);
        self.locked_features.len() != before
    }

    pub fn add_deny(&mut self, cmd: &str) -> bool {
        if !valid_text(cmd) || self.command_deny.len() >= MAX_DENY || self.command_deny.iter().any(|x| x == cmd) {
            return false;
        }
        self.command_deny.push(cmd.to_string());
        true
    }

    pub fn remove_deny(&mut self, cmd: &str) -> bool {
        let before = self.command_deny.len();
        self.command_deny.retain(|x| x != cmd);
        self.command_deny.len() != before
    }

    pub fn visible_records(&self) -> Vec<&str> {
        self.records.iter()
            .filter(|r| classify(r.policy, self.guest_mode) == SeedPolicy::Visible)
            .map(|r| r.instance_id.as_str()).collect()
    }

    pub fn hint_records(&self) -> Vec<&str> {
        self.records.iter()
            .filter(|r| classify(r.policy, self.guest_mode) == SeedPolicy::Hint)
            .map(|r| r.instance_id.as_str()).collect()
    }

    pub fn hidden_records(&self) -> Vec<&str> {
        self.records.iter()
            .filter(|r| classify(r.policy, self.guest_mode) == SeedPolicy::Hidden)
            .map(|r| r.instance_id.as_str()).collect()
    }

    pub fn policy_counts(&self) -> [usize; 3] {
        let mut out = [0usize; 3];
        for r in &self.records {
            match r.policy {
                SeedPolicy::Visible => out[0] += 1,
                SeedPolicy::Hint => out[1] += 1,
                SeedPolicy::Hidden => out[2] += 1,
            }
        }
        out
    }

    pub fn audit_by_action(&self) -> [usize; 4] {
        let mut out = [0usize; 4];
        for a in &self.audit {
            match a.action {
                AuditAction::View => out[0] += 1,
                AuditAction::PolicyChange => out[1] += 1,
                AuditAction::GuestToggle => out[2] += 1,
                AuditAction::Hidden => out[3] += 1,
            }
        }
        out
    }

    pub fn guest_locked(&self, id: &str) -> bool {
        self.guest_mode && self.locked_features.iter().any(|x| x == id)
    }

    pub fn command_allowed(&self, cmd: &str) -> bool {
        !self.command_deny.iter().any(|x| x == cmd)
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        let counts = self.policy_counts();
        Envelope::new(Kind::Event, EVENT_TARGET)
            .with("records", &self.records.len().to_string())
            .with("classified_visible", &self.visible_records().len().to_string())
            .with("classified_hint", &self.hint_records().len().to_string())
            .with("classified_hidden", &self.hidden_records().len().to_string())
            .with("audit", &self.audit.len().to_string())
            .with("locked", &self.locked_features.len().to_string())
            .with("deny", &self.command_deny.len().to_string())
            .with("guest", &(self.guest_mode as u8).to_string())
            .with("password", &(self.password_required as u8).to_string())
            .with("policy_visible", &counts[0].to_string())
            .with("policy_hint", &counts[1].to_string())
            .with("policy_hidden", &counts[2].to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    SeedWorkspace::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu079-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"guest_mode":false,"password_required":false,"records":[],"audit":[],"locked_features":[],"command_deny":[]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 7);
    }

    #[test]
    fn two_enum_codes_and_five_tables_are_explicit() {
        assert_eq!(SeedPolicy::Visible.code(), "visible");
        assert_eq!(SeedPolicy::Hint.code(), "hint");
        assert_eq!(SeedPolicy::Hidden.code(), "hidden");
        assert_eq!(SeedPolicy::parse("nope"), None);
        assert_eq!(AuditAction::View.code(), "view");
        assert_eq!(AuditAction::PolicyChange.code(), "policy_change");
        assert_eq!(AuditAction::GuestToggle.code(), "guest_toggle");
        assert_eq!(AuditAction::Hidden.code(), "hidden");
        assert_eq!(AuditAction::parse("nope"), None);
        assert_eq!(KNOWN_KEYS.len(), 7);
        assert_eq!(SEED_KEYS.len(), 4);
        assert_eq!(AUDIT_KEYS.len(), 4);
        assert_eq!(POLICIES.len(), 3);
        assert_eq!(ACTIONS.len(), 4);
        assert_eq!(MAX_RECORDS, 24);
        assert_eq!(MAX_AUDIT, 64);
        assert_eq!(MAX_LOCKED, 32);
        assert_eq!(MAX_DENY, 32);
    }

    #[test]
    fn default_is_empty_and_all_lists_empty() {
        let (p, lines) = SeedWorkspace::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, SeedWorkspace::default());
        assert!(!p.guest_mode);
        assert!(!p.password_required);
        assert!(p.visible_records().is_empty());
        assert!(p.hint_records().is_empty());
        assert!(p.hidden_records().is_empty());
        assert_eq!(p.policy_counts(), [0, 0, 0]);
        assert_eq!(p.audit_by_action(), [0, 0, 0, 0]);
        assert!(!p.guest_locked("x"));
        assert!(p.command_allowed("x"));
    }

    #[test]
    fn bad_root_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(SEED_ACCESS_FILE);
        let base = DEFAULT_STATE;
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            base.replace("\"command_deny\":[]", "\"command_deny\":[],\"extra\":1"),
            base.replace("\"schema\":1", "\"schema\":2"),
            base.replace("\"guest_mode\":false", "\"guest_mode\":\"no\""),
            base.replace("\"password_required\":false", "\"password_required\":\"no\""),
            base.replace("\"records\":[]", "\"records\":\"no\""),
            base.replace("\"audit\":[]", "\"audit\":\"no\""),
            base.replace("\"locked_features\":[]", "\"locked_features\":\"no\""),
            base.replace("\"command_deny\":[]", "\"command_deny\":\"no\""),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (p, lines) = SeedWorkspace::open(Some(&r));
            assert_eq!(p, SeedWorkspace::default(), "case={}", &raw[..raw.len().min(40)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(40)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_record_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"guest_mode":false,"password_required":false,"records":[{"instance_id":"a","value":"s1","policy":"visible","note":""},7,{"instance_id":"","value":"s","policy":"visible","note":""},{"instance_id":"b","value":"","policy":"visible","note":""},{"instance_id":"c","value":"s","policy":"bad","note":""},{"instance_id":"d","value":"s","policy":"visible","note":"a\nb"},{"instance_id":"e","value":"s","policy":"hint","note":""},{"instance_id":"f","value":"s","policy":"visible","note":"leak"},{"instance_id":"g","value":"s","policy":"visible","note":"","z":1},{"instance_id":"a","value":"s2","policy":"hidden","note":""},{"instance_id":"h","value":"s","policy":"hint","note":"ask"},{"instance_id":"i","value":"s","policy":"hidden","note":"x"}],"audit":[],"locked_features":[],"command_deny":[]}"#;
        fs::write(r.join(SEED_ACCESS_FILE), raw).unwrap();
        let (p, lines) = SeedWorkspace::open(Some(&r));
        assert_eq!(p.records.len(), 2);
        assert_eq!(p.records[0].instance_id, "a");
        assert_eq!(p.records[0].policy, SeedPolicy::Visible);
        assert_eq!(p.records[1].instance_id, "h");
        assert_eq!(p.records[1].policy, SeedPolicy::Hint);
        assert_eq!(p.records[1].note, "ask");
        assert!(lines.iter().any(|x| x.contains("index=11 bad_policy_note_pair")), "i rejected");
        assert!(!p.records.iter().any(|r| r.instance_id == "i"));
        for tag in ["bad_shape", "bad_id", "bad_value", "bad_policy", "bad_note", "bad_policy_note_pair", "duplicate_id"] {
            assert!(lines.iter().any(|x| x.contains(tag)), "missing={}", tag);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_audit_entries_and_collections_are_skipped() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"guest_mode":false,"password_required":false,"records":[],"audit":[{"id":"a1","action":"view","target":"t","scope":"s"},false,{"id":"","action":"view","target":"t","scope":"s"},{"id":"a2","action":"bad","target":"t","scope":"s"},{"id":"a3","action":"view","target":"","scope":"s"},{"id":"a4","action":"view","target":"t","scope":""},{"id":"a5","action":"view","target":"t","scope":"s","z":1},{"id":"a1","action":"hidden","target":"t","scope":"s"},{"id":"a6","action":"guest_toggle","target":"t","scope":"s"}],"locked_features":[7,"","a\nb","ok","ok"],"command_deny":[false,"","dup","dup"]}"#;
        fs::write(r.join(SEED_ACCESS_FILE), raw).unwrap();
        let (p, lines) = SeedWorkspace::open(Some(&r));
        assert_eq!(p.audit.len(), 2);
        assert_eq!(p.audit[0].id, "a1");
        assert_eq!(p.audit[0].action, AuditAction::View);
        assert_eq!(p.audit[1].id, "a6");
        assert_eq!(p.audit[1].action, AuditAction::GuestToggle);
        assert_eq!(p.locked_features, vec!["ok".to_string()]);
        assert_eq!(p.command_deny, vec!["dup".to_string()]);
        for tag in ["bad_shape", "bad_id", "bad_action", "bad_target", "bad_scope", "duplicate_id", "bad_text", "duplicate"] {
            assert!(lines.iter().any(|x| x.contains(tag)), "missing={}", tag);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_truncates_overflow_from_disk() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let mut rec = String::from("[");
        for i in 0..(MAX_RECORDS + 3) {
            if i > 0 { rec.push(','); }
            rec.push_str(&format!(r#"{{"instance_id":"r{}","value":"v","policy":"visible","note":""}}"#, i));
        }
        rec.push(']');
        let mut au = String::from("[");
        for i in 0..(MAX_AUDIT + 2) {
            if i > 0 { au.push(','); }
            au.push_str(&format!(r#"{{"id":"a{}","action":"view","target":"t","scope":"s"}}"#, i));
        }
        au.push(']');
        let raw = format!(r#"{{"schema":1,"guest_mode":false,"password_required":false,"records":{},"audit":{},"locked_features":[],"command_deny":[]}}"#, rec, au);
        fs::write(r.join(SEED_ACCESS_FILE), raw).unwrap();
        let (p, lines) = SeedWorkspace::open(Some(&r));
        assert_eq!(p.records.len(), MAX_RECORDS);
        assert_eq!(p.audit.len(), MAX_AUDIT);
        assert!(lines.iter().any(|x| x.contains("overflow=3")));
        assert!(lines.iter().any(|x| x.contains("overflow=2")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn classify_matrix_has_six_branches() {
        assert_eq!(classify(SeedPolicy::Visible, false), SeedPolicy::Visible);
        assert_eq!(classify(SeedPolicy::Visible, true), SeedPolicy::Hidden);
        assert_eq!(classify(SeedPolicy::Hint, false), SeedPolicy::Hint);
        assert_eq!(classify(SeedPolicy::Hint, true), SeedPolicy::Hidden);
        assert_eq!(classify(SeedPolicy::Hidden, false), SeedPolicy::Hidden);
        assert_eq!(classify(SeedPolicy::Hidden, true), SeedPolicy::Hidden);
    }

    #[test]
    fn add_remove_and_record_bounds() {
        let mut p = SeedWorkspace::default();
        assert!(p.add_record("a", "s1", SeedPolicy::Visible, ""));
        assert!(p.add_record("b", "s2", SeedPolicy::Hint, "ask"));
        assert!(p.add_record("c", "s3", SeedPolicy::Hidden, ""));
        assert!(!p.add_record("a", "s1", SeedPolicy::Visible, ""));
        assert!(!p.add_record("", "s", SeedPolicy::Visible, ""));
        assert!(!p.add_record("bad\nid", "s", SeedPolicy::Visible, ""));
        assert!(!p.add_record("d", "", SeedPolicy::Visible, ""));
        assert!(!p.add_record("e", "s", SeedPolicy::Hint, ""));
        assert!(!p.add_record("f", "s", SeedPolicy::Visible, "leak"));
        assert_eq!(p.policy_counts(), [1, 1, 1]);
        assert!(p.remove_record("a"));
        assert!(!p.remove_record("missing"));
        assert_eq!(p.records.len(), 2);
        for i in 0..(MAX_RECORDS + 5) {
            p.add_record(&format!("w{}", i), "v", SeedPolicy::Visible, "");
        }
        assert_eq!(p.records.len(), MAX_RECORDS);
    }

    #[test]
    fn single_record_mutations_only_touch_one_item() {
        let mut p = SeedWorkspace::default();
        p.add_record("a", "s1", SeedPolicy::Hint, "ask");
        p.add_record("b", "s2", SeedPolicy::Visible, "");
        assert!(p.set_value("a", "s1b"));
        assert_eq!(p.records[0].value, "s1b");
        assert_eq!(p.records[1].value, "s2");
        assert!(!p.set_policy("a", SeedPolicy::Visible));
        assert_eq!(p.records[0].policy, SeedPolicy::Hint);
        assert!(p.set_note("a", "ask2"));
        assert_eq!(p.records[0].note, "ask2");
        assert!(!p.set_note("a", ""));
        assert_eq!(p.records[0].note, "ask2");
        assert!(!p.set_policy("a", SeedPolicy::Hidden));
        assert!(p.set_policy("a", SeedPolicy::Hint));
        assert_eq!(p.records[0].policy, SeedPolicy::Hint);
        assert_eq!(p.records[1].policy, SeedPolicy::Visible);
        assert_eq!(p.records[1].note, "");
        assert_eq!(p.records[1].value, "s2");
        assert!(!p.set_value("missing", "q"));
        assert!(!p.set_policy("missing", SeedPolicy::Hidden));
        assert!(!p.set_note("missing", "q"));
        assert!(!p.set_value("a", ""));
        assert!(!p.set_note("a", "a\nb"));
    }

    #[test]
    fn audit_add_remove_and_bounds() {
        let mut p = SeedWorkspace::default();
        assert!(p.add_audit("a1", AuditAction::View, "t", "s"));
        assert!(!p.add_audit("a1", AuditAction::Hidden, "t", "s"));
        assert!(!p.add_audit("", AuditAction::View, "t", "s"));
        assert!(!p.add_audit("a2", AuditAction::View, "", "s"));
        assert!(!p.add_audit("a3", AuditAction::View, "t", ""));
        assert!(p.add_audit("a4", AuditAction::GuestToggle, "t", "s"));
        assert_eq!(p.audit_by_action(), [1, 0, 1, 0]);
        assert!(p.set_audit_action("a1", AuditAction::PolicyChange));
        assert_eq!(p.audit_by_action(), [0, 1, 1, 0]);
        assert!(!p.set_audit_action("missing", AuditAction::Hidden));
        assert!(p.remove_audit("a1"));
        assert!(!p.remove_audit("a1"));
        for i in 0..(MAX_AUDIT + 3) {
            p.add_audit(&format!("x{}", i), AuditAction::View, "t", "s");
        }
        assert_eq!(p.audit.len(), MAX_AUDIT);
    }

    #[test]
    fn policy_sets_and_deny_bound() {
        let mut p = SeedWorkspace::default();
        assert!(p.add_locked("f1"));
        assert!(!p.add_locked("f1"));
        assert!(!p.add_locked(""));
        assert!(!p.add_locked("a\nb"));
        assert!(p.remove_locked("f1"));
        assert!(!p.remove_locked("f1"));
        assert!(p.add_deny("c1"));
        assert!(!p.add_deny("c1"));
        assert!(!p.add_deny(""));
        assert!(p.remove_deny("c1"));
        assert!(!p.remove_deny("c1"));
        for i in 0..(MAX_LOCKED + 3) { p.add_locked(&format!("f{}", i)); }
        assert_eq!(p.locked_features.len(), MAX_LOCKED);
        for i in 0..(MAX_DENY + 3) { p.add_deny(&format!("c{}", i)); }
        assert_eq!(p.command_deny.len(), MAX_DENY);
    }

    #[test]
    fn guest_mode_changes_all_three_derived_sets() {
        let mut p = SeedWorkspace::default();
        p.add_record("a", "s1", SeedPolicy::Visible, "");
        p.add_record("b", "s2", SeedPolicy::Hint, "ask");
        p.add_record("c", "s3", SeedPolicy::Hidden, "");
        assert_eq!(p.visible_records(), vec!["a"]);
        assert_eq!(p.hint_records(), vec!["b"]);
        assert_eq!(p.hidden_records(), vec!["c"]);
        assert_eq!(p.policy_counts(), [1, 1, 1]);
        p.set_guest_mode(true);
        assert!(p.visible_records().is_empty());
        assert!(p.hint_records().is_empty());
        assert_eq!(p.hidden_records(), vec!["a", "b", "c"]);
        assert_eq!(p.policy_counts(), [1, 1, 1]);
        p.set_guest_mode(false);
        assert_eq!(p.visible_records(), vec!["a"]);
        assert_eq!(p.hint_records(), vec!["b"]);
    }

    #[test]
    fn guest_locked_and_command_allowed_are_pure() {
        let mut p = SeedWorkspace::default();
        p.add_locked("accounts");
        p.add_deny("op");
        assert!(!p.guest_locked("accounts"));
        assert!(!p.guest_locked("instances"));
        p.set_guest_mode(true);
        assert!(p.guest_locked("accounts"));
        assert!(!p.guest_locked("instances"));
        assert!(!p.command_allowed("op"));
        assert!(p.command_allowed("list"));
        p.set_guest_mode(false);
        assert!(!p.guest_locked("accounts"));
    }

    #[test]
    fn password_flag_has_two_actions() {
        let mut p = SeedWorkspace::default();
        assert!(!p.password_required);
        p.set_password_required(true);
        assert!(p.password_required);
        p.set_password_required(false);
        assert!(!p.password_required);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut p = SeedWorkspace::default();
        p.add_record("a", "s1", SeedPolicy::Visible, "");
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
        let mut p = SeedWorkspace::default();
        p.set_guest_mode(true);
        p.set_password_required(true);
        assert!(p.add_record("a", "s1", SeedPolicy::Visible, ""));
        assert!(p.add_record("b", "s2", SeedPolicy::Hint, "ask"));
        assert!(p.add_audit("a1", AuditAction::GuestToggle, "t", "s"));
        assert!(p.add_locked("accounts"));
        assert!(p.add_deny("op"));
        assert!(p.persist(Some(&r)).is_empty());
        let (back, lines) = SeedWorkspace::open(Some(&r));
        assert!(lines.is_empty());
        assert!(back.guest_mode);
        assert!(back.password_required);
        assert_eq!(back.records.len(), 2);
        assert_eq!(back.records[1].policy, SeedPolicy::Hint);
        assert_eq!(back.records[1].note, "ask");
        assert_eq!(back.audit.len(), 1);
        assert_eq!(back.audit[0].action, AuditAction::GuestToggle);
        assert_eq!(back.locked_features, vec!["accounts".to_string()]);
        assert_eq!(back.command_deny, vec!["op".to_string()]);
        assert_eq!(back.hidden_records(), vec!["a", "b"]);
        assert!(back.guest_locked("accounts"));
        assert!(!back.command_allowed("op"));
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = SeedWorkspace::open(Some(&r));
        assert_eq!(def, SeedWorkspace::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope_without_user_text() {
        let mut p = SeedWorkspace::default();
        p.set_guest_mode(true);
        p.set_password_required(true);
        p.add_record("secret-id", "secret-value", SeedPolicy::Visible, "");
        p.add_record("b", "s2", SeedPolicy::Hint, "secret-note");
        p.add_record("c", "s3", SeedPolicy::Hidden, "");
        p.add_audit("secret-au", AuditAction::View, "secret-target", "secret-scope");
        p.add_locked("secret-locked");
        p.add_deny("secret-deny");
        let e = p.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, EVENT_TARGET);
        assert_eq!(e.field("records"), Some("3"));
        assert_eq!(e.field("classified_visible"), Some("0"));
        assert_eq!(e.field("classified_hint"), Some("0"));
        assert_eq!(e.field("classified_hidden"), Some("3"));
        assert_eq!(e.field("audit"), Some("1"));
        assert_eq!(e.field("locked"), Some("1"));
        assert_eq!(e.field("deny"), Some("1"));
        assert_eq!(e.field("guest"), Some("1"));
        assert_eq!(e.field("password"), Some("1"));
        assert_eq!(e.field("policy_visible"), Some("1"));
        assert_eq!(e.field("policy_hint"), Some("1"));
        assert_eq!(e.field("policy_hidden"), Some("1"));
        for key in ["value", "note", "instance_id", "target", "scope"] {
            assert_eq!(e.field(key), None);
        }
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 12);
    }

    #[test]
    fn serialize_carries_no_seed_table() {
        let mut p = SeedWorkspace::default();
        p.add_record("a", "s1", SeedPolicy::Visible, "");
        let raw = serialize(&p).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 7);
        assert!(!raw.contains("SEED_TABLE"));
        assert!(!raw.contains("POLICY_TABLE"));
        assert!(!raw.contains("cmp_precedence"));
        assert!(!raw.contains("semver"));
    }
}

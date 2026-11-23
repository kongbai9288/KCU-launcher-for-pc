use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use semver::Version;
use serde_json::{from_str, json, to_string, Value};
use std::cmp::Ordering;
use std::fs;
use std::path::Path;

pub const MOD_ROLLBACK_FILE: &str = "mod-rollback.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"scope":"instance","current":0,"items":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_ITEMS: usize = 24;
pub const EVENT_TARGET: &str = "mod.rollback";
pub const ROOT_KEYS: &[&str] = &["schema", "scope", "current", "items"];
pub const ITEM_KEYS: &[&str] = &["id", "mod_id", "installed", "candidate", "kind", "disable_lower", "choice", "snapshot"];
pub const SCOPES: &[&str] = &["instance"];
pub const KINDS: &[&str] = &["same_version", "higher_version", "lower_version", "other_issue"];
pub const CHOICES: &[&str] = &["pending", "keep", "replace", "rollback"];
pub const SNAPSHOTS: &[&str] = &["server_properties", "ops_json", "mod_config", "loader_version"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RollbackScope {
    Instance,
}

impl RollbackScope {
    pub fn code(&self) -> &'static str {
        match self {
            RollbackScope::Instance => "instance",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "instance" => Some(RollbackScope::Instance),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DecisionKind {
    SameVersion,
    HigherVersion,
    LowerVersion,
    OtherIssue,
}

impl DecisionKind {
    pub fn code(&self) -> &'static str {
        match self {
            DecisionKind::SameVersion => "same_version",
            DecisionKind::HigherVersion => "higher_version",
            DecisionKind::LowerVersion => "lower_version",
            DecisionKind::OtherIssue => "other_issue",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "same_version" => Some(DecisionKind::SameVersion),
            "higher_version" => Some(DecisionKind::HigherVersion),
            "lower_version" => Some(DecisionKind::LowerVersion),
            "other_issue" => Some(DecisionKind::OtherIssue),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UserChoice {
    Pending,
    Keep,
    Replace,
    Rollback,
}

impl UserChoice {
    pub fn code(&self) -> &'static str {
        match self {
            UserChoice::Pending => "pending",
            UserChoice::Keep => "keep",
            UserChoice::Replace => "replace",
            UserChoice::Rollback => "rollback",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "pending" => Some(UserChoice::Pending),
            "keep" => Some(UserChoice::Keep),
            "replace" => Some(UserChoice::Replace),
            "rollback" => Some(UserChoice::Rollback),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SnapshotTarget {
    ServerProperties,
    OpsJson,
    ModConfig,
    LoaderVersion,
}

impl SnapshotTarget {
    pub fn code(&self) -> &'static str {
        match self {
            SnapshotTarget::ServerProperties => "server_properties",
            SnapshotTarget::OpsJson => "ops_json",
            SnapshotTarget::ModConfig => "mod_config",
            SnapshotTarget::LoaderVersion => "loader_version",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "server_properties" => Some(SnapshotTarget::ServerProperties),
            "ops_json" => Some(SnapshotTarget::OpsJson),
            "mod_config" => Some(SnapshotTarget::ModConfig),
            "loader_version" => Some(SnapshotTarget::LoaderVersion),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RollbackItem {
    pub id: String,
    pub mod_id: String,
    pub installed: String,
    pub candidate: String,
    pub kind: DecisionKind,
    pub disable_lower: bool,
    pub choice: UserChoice,
    pub snapshot: SnapshotTarget,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ModRollback {
    pub scope: RollbackScope,
    pub current: usize,
    pub items: Vec<RollbackItem>,
}

impl Default for ModRollback {
    fn default() -> Self {
        ModRollback { scope: RollbackScope::Instance, current: 0, items: Vec::new() }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("mod", action, "rollback", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("mod", action, "rollback", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_TEXT_BYTES && !has_control(s)
}

fn valid_version(s: &str) -> bool {
    s.len() <= robust::MAX_TEXT_BYTES && !has_control(s)
}

fn version_order(installed: &str, candidate: &str) -> Option<Ordering> {
    match (Version::parse(installed), Version::parse(candidate)) {
        (Ok(a), Ok(b)) => Some(b.cmp_precedence(&a)),
        _ => None,
    }
}

fn classify(installed: &str, candidate: &str) -> DecisionKind {
    match version_order(installed, candidate) {
        Some(Ordering::Greater) => DecisionKind::HigherVersion,
        Some(Ordering::Equal) => DecisionKind::SameVersion,
        Some(Ordering::Less) => DecisionKind::LowerVersion,
        None => DecisionKind::OtherIssue,
    }
}

fn item_consistent(i: &RollbackItem) -> bool {
    if i.kind == DecisionKind::HigherVersion && !i.disable_lower {
        return false;
    }
    if i.kind == DecisionKind::SameVersion && i.disable_lower {
        return false;
    }
    if i.choice == UserChoice::Rollback
        && i.kind != DecisionKind::LowerVersion
        && i.kind != DecisionKind::OtherIssue
    {
        return false;
    }
    if i.choice != UserChoice::Pending
        && i.kind != DecisionKind::OtherIssue
        && (i.installed.is_empty() || i.candidate.is_empty())
    {
        return false;
    }
    if i.snapshot == SnapshotTarget::LoaderVersion && i.choice == UserChoice::Keep {
        return false;
    }
    true
}

fn parse(raw: &str) -> (ModRollback, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (ModRollback::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (ModRollback::default(), lines);
        }
    };
    if obj.keys().any(|k| !ROOT_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (ModRollback::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (ModRollback::default(), lines);
    }
    let scope = match obj.get("scope").and_then(Value::as_str).and_then(RollbackScope::parse) {
        Some(s) => s,
        None => {
            lines.push(degrade("load", "bad_scope"));
            return (ModRollback::default(), lines);
        }
    };
    let arr = match obj.get("items").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "items_not_array"));
            return (ModRollback::default(), lines);
        }
    };
    if arr.len() > MAX_ITEMS {
        lines.push(degrade("load", "items_too_many"));
        return (ModRollback::default(), lines);
    }
    let current = match obj.get("current").and_then(Value::as_u64) {
        Some(n) => match usize::try_from(n) {
            Ok(v) => v,
            Err(_) => {
                lines.push(degrade("load", "bad_current"));
                return (ModRollback::default(), lines);
            }
        },
        None => {
            lines.push(degrade("load", "bad_current"));
            return (ModRollback::default(), lines);
        }
    };
    if current > arr.len() {
        lines.push(degrade("load", "current_out_of_range"));
        return (ModRollback::default(), lines);
    }
    let mut items: Vec<RollbackItem> = Vec::new();
    for item in arr {
        let io = match item.as_object() {
            Some(o) => o,
            None => {
                lines.push(degrade("load", "item_not_object"));
                return (ModRollback::default(), lines);
            }
        };
        if io.keys().any(|k| !ITEM_KEYS.contains(&k.as_str())) {
            lines.push(degrade("load", "item_unknown_key"));
            return (ModRollback::default(), lines);
        }
        let id = match io.get("id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "id_too_large"));
                return (ModRollback::default(), lines);
            }
            _ => {
                lines.push(degrade("load", "bad_id"));
                return (ModRollback::default(), lines);
            }
        };
        if items.iter().any(|i| i.id == id) {
            lines.push(degrade("load", "duplicate_id"));
            return (ModRollback::default(), lines);
        }
        let mod_id = match io.get("mod_id").and_then(Value::as_str) {
            Some(s) if valid_id(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "mod_id_too_large"));
                return (ModRollback::default(), lines);
            }
            _ => {
                lines.push(degrade("load", "bad_mod_id"));
                return (ModRollback::default(), lines);
            }
        };
        let installed = match io.get("installed").and_then(Value::as_str) {
            Some(s) if valid_version(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "installed_too_large"));
                return (ModRollback::default(), lines);
            }
            _ => {
                lines.push(degrade("load", "bad_installed"));
                return (ModRollback::default(), lines);
            }
        };
        let candidate = match io.get("candidate").and_then(Value::as_str) {
            Some(s) if valid_version(s) => s.to_string(),
            Some(s) if s.len() > robust::MAX_TEXT_BYTES => {
                lines.push(degrade("load", "candidate_too_large"));
                return (ModRollback::default(), lines);
            }
            _ => {
                lines.push(degrade("load", "bad_candidate"));
                return (ModRollback::default(), lines);
            }
        };
        let kind = match io.get("kind").and_then(Value::as_str).and_then(DecisionKind::parse) {
            Some(k) => k,
            None => {
                lines.push(degrade("load", "bad_kind"));
                return (ModRollback::default(), lines);
            }
        };
        let disable_lower = match io.get("disable_lower").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("load", "bad_disable_lower"));
                return (ModRollback::default(), lines);
            }
        };
        let choice = match io.get("choice").and_then(Value::as_str).and_then(UserChoice::parse) {
            Some(c) => c,
            None => {
                lines.push(degrade("load", "bad_choice"));
                return (ModRollback::default(), lines);
            }
        };
        let snapshot = match io.get("snapshot").and_then(Value::as_str).and_then(SnapshotTarget::parse) {
            Some(s) => s,
            None => {
                lines.push(degrade("load", "bad_snapshot"));
                return (ModRollback::default(), lines);
            }
        };
        let i = RollbackItem {
            id,
            mod_id,
            installed,
            candidate,
            kind,
            disable_lower,
            choice,
            snapshot,
        };
        if !item_consistent(&i) {
            lines.push(degrade("load", "bad_item_state"));
            return (ModRollback::default(), lines);
        }
        items.push(i);
    }
    (ModRollback { scope, current, items }, lines)
}

fn serialize(p: &ModRollback) -> Result<String> {
    let items: Vec<Value> = p.items.iter().map(|i| json!({
        "id": i.id,
        "mod_id": i.mod_id,
        "installed": i.installed,
        "candidate": i.candidate,
        "kind": i.kind.code(),
        "disable_lower": i.disable_lower,
        "choice": i.choice.code(),
        "snapshot": i.snapshot.code(),
    })).collect();
    Ok(to_string(&json!({
        "schema": 1,
        "scope": p.scope.code(),
        "current": p.current,
        "items": items
    }))?)
}

fn write(root: &Path, p: &ModRollback) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, MOD_ROLLBACK_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", MOD_ROLLBACK_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl ModRollback {
    pub fn open(root: Option<&Path>) -> (ModRollback, Vec<String>) {
        let Some(dir) = root else {
            return (ModRollback::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, MOD_ROLLBACK_FILE) {
            Ok(p) => p,
            Err(_) => return (ModRollback::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (ModRollback::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (ModRollback::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn page_count(&self) -> usize {
        self.items.len()
    }

    pub fn pending_count(&self) -> usize {
        self.items.iter().filter(|i| i.choice == UserChoice::Pending).count()
    }

    pub fn resolved_count(&self) -> usize {
        self.items.iter().filter(|i| i.choice != UserChoice::Pending).count()
    }

    pub fn current_item(&self) -> Option<&RollbackItem> {
        self.items.get(self.current)
    }

    pub fn disable_lower_count(&self) -> usize {
        self.items.iter().filter(|i| i.disable_lower).count()
    }

    pub fn by_kind(&self, kind: DecisionKind) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for i in &self.items {
            if i.kind == kind {
                out.push(i.id.as_str());
            }
        }
        out
    }

    pub fn by_snapshot(&self, target: SnapshotTarget) -> Vec<&str> {
        let mut out: Vec<&str> = Vec::new();
        for i in &self.items {
            if i.snapshot == target {
                out.push(i.id.as_str());
            }
        }
        out
    }

    pub fn summary(&self) -> [usize; 4] {
        let mut out: [usize; 4] = [0, 0, 0, 0];
        for i in &self.items {
            let idx = match i.kind {
                DecisionKind::SameVersion => 0,
                DecisionKind::HigherVersion => 1,
                DecisionKind::LowerVersion => 2,
                DecisionKind::OtherIssue => 3,
            };
            out[idx] += 1;
        }
        out
    }

    pub fn add_item(&mut self, id: &str, mod_id: &str, installed: &str, candidate: &str, snapshot: SnapshotTarget) -> bool {
        if self.items.len() >= MAX_ITEMS
            || !valid_id(id)
            || !valid_id(mod_id)
            || !valid_version(installed)
            || !valid_version(candidate)
            || self.items.iter().any(|i| i.id == id)
        {
            return false;
        }
        if !SCOPES.contains(&self.scope.code())
            || !SNAPSHOTS.contains(&snapshot.code())
        {
            return false;
        }
        let kind = classify(installed, candidate);
        let disable_lower = kind == DecisionKind::HigherVersion;
        let i = RollbackItem {
            id: id.to_string(),
            mod_id: mod_id.to_string(),
            installed: installed.to_string(),
            candidate: candidate.to_string(),
            kind,
            disable_lower,
            choice: UserChoice::Pending,
            snapshot,
        };
        if !item_consistent(&i) {
            return false;
        }
        self.items.push(i);
        true
    }

    pub fn append_issue(&mut self, id: &str, mod_id: &str, snapshot: SnapshotTarget) -> bool {
        if self.pending_count() == 0 {
            return false;
        }
        if self.items.len() >= MAX_ITEMS
            || !valid_id(id)
            || !valid_id(mod_id)
            || self.items.iter().any(|i| i.id == id)
            || !SNAPSHOTS.contains(&snapshot.code())
        {
            return false;
        }
        let i = RollbackItem {
            id: id.to_string(),
            mod_id: mod_id.to_string(),
            installed: String::new(),
            candidate: String::new(),
            kind: DecisionKind::OtherIssue,
            disable_lower: false,
            choice: UserChoice::Pending,
            snapshot,
        };
        if !item_consistent(&i) {
            return false;
        }
        self.items.push(i);
        true
    }

    pub fn resolve_current(&mut self, choice: UserChoice) -> bool {
        if choice == UserChoice::Pending || self.current >= self.items.len() {
            return false;
        }
        let pos = self.current;
        let mut candidate = self.items[pos].clone();
        candidate.choice = choice;
        if !item_consistent(&candidate) {
            return false;
        }
        self.items[pos].choice = choice;
        self.current += 1;
        true
    }

    pub fn set_kind(&mut self, id: &str, kind: DecisionKind) -> bool {
        let Some(pos) = self.items.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.items[pos].clone();
        candidate.kind = kind;
        if !KINDS.contains(&kind.code()) || !item_consistent(&candidate) {
            return false;
        }
        self.items[pos].kind = kind;
        true
    }

    pub fn set_choice(&mut self, id: &str, choice: UserChoice) -> bool {
        let Some(pos) = self.items.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.items[pos].clone();
        candidate.choice = choice;
        if !CHOICES.contains(&choice.code()) || !item_consistent(&candidate) {
            return false;
        }
        self.items[pos].choice = choice;
        true
    }

    pub fn set_disable_lower(&mut self, id: &str, disable_lower: bool) -> bool {
        let Some(pos) = self.items.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.items[pos].clone();
        candidate.disable_lower = disable_lower;
        if !item_consistent(&candidate) {
            return false;
        }
        self.items[pos].disable_lower = disable_lower;
        true
    }

    pub fn set_snapshot(&mut self, id: &str, snapshot: SnapshotTarget) -> bool {
        let Some(pos) = self.items.iter().position(|i| i.id == id) else { return false };
        let mut candidate = self.items[pos].clone();
        candidate.snapshot = snapshot;
        if !SNAPSHOTS.contains(&snapshot.code()) || !item_consistent(&candidate) {
            return false;
        }
        self.items[pos].snapshot = snapshot;
        true
    }

    pub fn set_versions(&mut self, id: &str, installed: &str, candidate: &str) -> bool {
        let Some(pos) = self.items.iter().position(|i| i.id == id) else { return false };
        if !valid_version(installed) || !valid_version(candidate) {
            return false;
        }
        let mut next = self.items[pos].clone();
        next.installed = installed.to_string();
        next.candidate = candidate.to_string();
        if !item_consistent(&next) {
            return false;
        }
        self.items[pos].installed = installed.to_string();
        self.items[pos].candidate = candidate.to_string();
        true
    }

    pub fn remove_item(&mut self, id: &str) -> bool {
        let Some(pos) = self.items.iter().position(|i| i.id == id) else { return false };
        self.items.remove(pos);
        if self.current > self.items.len() {
            self.current = self.items.len();
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
            .with("resolved", &self.resolved_count().to_string())
            .with("disable_lower", &self.disable_lower_count().to_string())
            .with("higher", &self.by_kind(DecisionKind::HigherVersion).len().to_string())
            .with("same", &self.by_kind(DecisionKind::SameVersion).len().to_string())
            .with("rollback", &self.by_kind(DecisionKind::LowerVersion).len().to_string())
            .with("kinds", &KINDS.len().to_string())
            .with("snapshots", &SNAPSHOTS.len().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    ModRollback::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering as AtomicOrdering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, AtomicOrdering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu085-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    fn load(dir: &std::path::Path, raw: &str) -> (ModRollback, Vec<String>) {
        fs::create_dir_all(dir).unwrap();
        fs::write(dir.join(MOD_ROLLBACK_FILE), raw).unwrap();
        ModRollback::open(Some(dir))
    }

    fn sample() -> ModRollback {
        let mut p = ModRollback::default();
        assert!(p.add_item("r1", "sodium", "1.2.0", "1.3.0", SnapshotTarget::ModConfig));
        p
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"scope":"instance","current":0,"items":[]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 4);
        assert_eq!(v["scope"], "instance");
        assert_eq!(v["current"], 0);
        assert_eq!(v["items"].as_array().unwrap().len(), 0);
    }

    #[test]
    fn four_enum_codes_and_six_tables_are_explicit() {
        assert_eq!(RollbackScope::Instance.code(), "instance");
        assert_eq!(RollbackScope::parse("nope"), None);
        assert_eq!(DecisionKind::SameVersion.code(), "same_version");
        assert_eq!(DecisionKind::HigherVersion.code(), "higher_version");
        assert_eq!(DecisionKind::LowerVersion.code(), "lower_version");
        assert_eq!(DecisionKind::OtherIssue.code(), "other_issue");
        assert_eq!(DecisionKind::parse("nope"), None);
        assert_eq!(UserChoice::Pending.code(), "pending");
        assert_eq!(UserChoice::Keep.code(), "keep");
        assert_eq!(UserChoice::Replace.code(), "replace");
        assert_eq!(UserChoice::Rollback.code(), "rollback");
        assert_eq!(UserChoice::parse("nope"), None);
        assert_eq!(SnapshotTarget::ServerProperties.code(), "server_properties");
        assert_eq!(SnapshotTarget::OpsJson.code(), "ops_json");
        assert_eq!(SnapshotTarget::ModConfig.code(), "mod_config");
        assert_eq!(SnapshotTarget::LoaderVersion.code(), "loader_version");
        assert_eq!(SnapshotTarget::parse("nope"), None);
        assert_eq!(ROOT_KEYS.len(), 4);
        assert_eq!(ITEM_KEYS.len(), 8);
        assert_eq!(SCOPES.len(), 1);
        assert_eq!(KINDS.len(), 4);
        assert_eq!(CHOICES.len(), 4);
        assert_eq!(SNAPSHOTS.len(), 4);
    }

    #[test]
    fn version_order_uses_precedence_not_equality() {
        assert_eq!(version_order("1.2.0", "1.3.0"), Some(Ordering::Greater));
        assert_eq!(version_order("1.2.0", "1.2.0"), Some(Ordering::Equal));
        assert_eq!(version_order("1.2.0", "1.1.0"), Some(Ordering::Less));
        assert_eq!(version_order("1.2.0+alpha", "1.2.0+beta"), Some(Ordering::Equal));
        assert_eq!(version_order("nope", "1.2.0"), None);
        assert_eq!(classify("1.2.0", "1.3.0"), DecisionKind::HigherVersion);
        assert_eq!(classify("1.2.0", "1.2.0"), DecisionKind::SameVersion);
        assert_eq!(classify("1.2.0", "1.1.0"), DecisionKind::LowerVersion);
        assert_eq!(classify("bad", "1.2.0"), DecisionKind::OtherIssue);
    }

    #[test]
    fn default_is_empty_instance_scope() {
        let (p, lines) = ModRollback::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, ModRollback::default());
        assert_eq!(p.scope, RollbackScope::Instance);
        assert_eq!(p.current, 0);
        assert_eq!(p.page_count(), 0);
        assert_eq!(p.pending_count(), 0);
        assert_eq!(p.resolved_count(), 0);
        assert_eq!(p.current_item(), None);
        assert_eq!(p.summary(), [0, 0, 0, 0]);
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
            base.replace("\"scope\":\"instance\"", "\"scope\":\"global\""),
            base.replace("\"current\":0", "\"current\":-1"),
            base.replace("\"current\":0", "\"current\":1"),
            base.replace("\"items\":[]", "\"items\":7"),
            base.replace("\"items\":[", "\"items\":[null,"),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, ModRollback::default(), "case={}", &raw[..raw.len().min(48)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(48)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_item_texts_and_capacity_are_rejected() {
        let r = tmp();
        let e = r#"{"id":"r1","mod_id":"sodium","installed":"1.2.0","candidate":"1.3.0","kind":"higher_version","disable_lower":true,"choice":"pending","snapshot":"mod_config"}"#;
        let one = format!("{{\"schema\":1,\"scope\":\"instance\",\"current\":0,\"items\":[{}]}}", e);
        let cases = vec![
            one.replace("\"items\":[{", "\"items\":[{\"extra\":1,"),
            one.replace("\"id\":\"r1\"", "\"id\":\"a\\nb\""),
            one.replace("\"id\":\"r1\"", "\"id\":\"\""),
            one.replace("\"id\":\"r1\"", &format!("\"id\":\"{}\"", "x".repeat(robust::MAX_TEXT_BYTES + 1))),
            one.replace("\"mod_id\":\"sodium\"", "\"mod_id\":\"\""),
            one.replace("\"mod_id\":\"sodium\"", &format!("\"mod_id\":\"{}\"", "x".repeat(robust::MAX_TEXT_BYTES + 1))),
            one.replace("\"installed\":\"1.2.0\"", "\"installed\":\"a\\nb\""),
            one.replace("\"installed\":\"1.2.0\"", &format!("\"installed\":\"{}\"", "x".repeat(robust::MAX_TEXT_BYTES + 1))),
            one.replace("\"candidate\":\"1.3.0\"", "\"candidate\":\"a\\nb\""),
            one.replace("\"candidate\":\"1.3.0\"", &format!("\"candidate\":\"{}\"", "x".repeat(robust::MAX_TEXT_BYTES + 1))),
            one.replace("\"kind\":\"higher_version\"", "\"kind\":\"nope\""),
            one.replace("\"disable_lower\":true", "\"disable_lower\":\"no\""),
            one.replace("\"choice\":\"pending\"", "\"choice\":\"nope\""),
            one.replace("\"snapshot\":\"mod_config\"", "\"snapshot\":\"nope\""),
            format!("{{\"schema\":1,\"scope\":\"instance\",\"current\":0,\"items\":[{},{}]}}", e, e),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, ModRollback::default(), "case={}", &raw[..raw.len().min(48)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(48)]);
        }
        let many = format!("{{\"schema\":1,\"scope\":\"instance\",\"current\":0,\"items\":[{}]}}",
            (0..MAX_ITEMS + 1).map(|i| format!("{{\"id\":\"r{}\",\"mod_id\":\"m\",\"installed\":\"1.0.0\",\"candidate\":\"1.0.0\",\"kind\":\"same_version\",\"disable_lower\":false,\"choice\":\"pending\",\"snapshot\":\"mod_config\"}}", i)).collect::<Vec<_>>().join(","));
        let (p, lines) = load(&r, &many);
        assert_eq!(p, ModRollback::default());
        assert!(lines.iter().any(|x| x.contains("items_too_many")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn contradiction_states_are_rejected_on_load() {
        let r = tmp();
        let e = r#"{"id":"r1","mod_id":"sodium","installed":"1.2.0","candidate":"1.3.0","kind":"higher_version","disable_lower":true,"choice":"pending","snapshot":"mod_config"}"#;
        let one = format!("{{\"schema\":1,\"scope\":\"instance\",\"current\":0,\"items\":[{}]}}", e);
        let cases = vec![
            one.replace("\"disable_lower\":true", "\"disable_lower\":false"),
            one.replace("\"kind\":\"higher_version\"", "\"kind\":\"same_version\"").replace("\"disable_lower\":true", "\"disable_lower\":true"),
            one.replace("\"choice\":\"pending\"", "\"choice\":\"rollback\""),
            one.replace("\"installed\":\"1.2.0\"", "\"installed\":\"\"").replace("\"choice\":\"pending\"", "\"choice\":\"keep\""),
            one.replace("\"snapshot\":\"mod_config\"", "\"snapshot\":\"loader_version\"").replace("\"choice\":\"pending\"", "\"choice\":\"keep\""),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, ModRollback::default(), "case={}", &raw[..raw.len().min(48)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(48)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn higher_version_disables_lower_same_version_does_not() {
        let mut p = sample();
        assert_eq!(p.items[0].kind, DecisionKind::HigherVersion);
        assert!(p.items[0].disable_lower);
        assert_eq!(p.disable_lower_count(), 1);
        assert!(!p.set_disable_lower("r1", false));
        assert!(p.add_item("r2", "iris", "1.0.0", "1.0.0", SnapshotTarget::ModConfig));
        assert_eq!(p.items[1].kind, DecisionKind::SameVersion);
        assert!(!p.items[1].disable_lower);
        assert!(p.set_disable_lower("r2", true) == false);
    }

    #[test]
    fn resolve_current_advances_one_page_at_a_time() {
        let mut p = sample();
        assert!(p.add_item("r2", "iris", "2.0.0", "1.9.0", SnapshotTarget::LoaderVersion));
        assert_eq!(p.page_count(), 2);
        assert_eq!(p.current, 0);
        assert_eq!(p.current_item().unwrap().id, "r1");
        assert!(!p.resolve_current(UserChoice::Pending));
        assert!(p.resolve_current(UserChoice::Replace));
        assert_eq!(p.current, 1);
        assert_eq!(p.current_item().unwrap().id, "r2");
        assert_eq!(p.pending_count(), 1);
        assert_eq!(p.resolved_count(), 1);
        assert!(p.resolve_current(UserChoice::Rollback));
        assert_eq!(p.current, 2);
        assert_eq!(p.current_item(), None);
        assert_eq!(p.pending_count(), 0);
        assert!(!p.resolve_current(UserChoice::Keep));
    }

    #[test]
    fn append_issue_only_while_user_choice_pending() {
        let mut p = sample();
        assert!(p.append_issue("r2", "extra", SnapshotTarget::OpsJson));
        assert_eq!(p.page_count(), 2);
        assert_eq!(p.items[1].kind, DecisionKind::OtherIssue);
        assert!(p.resolve_current(UserChoice::Replace));
        assert!(p.resolve_current(UserChoice::Keep));
        assert_eq!(p.pending_count(), 0);
        assert!(!p.append_issue("r3", "late", SnapshotTarget::OpsJson));
        assert_eq!(p.page_count(), 2);
    }

    #[test]
    fn loader_snapshot_keep_is_rejected() {
        let mut p = sample();
        assert!(p.set_choice("r1", UserChoice::Keep));
        assert!(!p.set_snapshot("r1", SnapshotTarget::LoaderVersion));
        assert!(p.set_snapshot("r1", SnapshotTarget::ServerProperties));
        assert_eq!(p.by_snapshot(SnapshotTarget::ServerProperties), vec!["r1"]);
        assert!(!p.set_choice("r1", UserChoice::Rollback));
        assert!(p.set_kind("r1", DecisionKind::LowerVersion));
        assert!(p.set_choice("r1", UserChoice::Rollback));
    }

    #[test]
    fn versions_are_bounded_and_reclassifiable() {
        let mut p = sample();
        assert!(!p.set_versions("r1", "bad\n", "1.0.0"));
        assert!(!p.set_versions("r1", &"x".repeat(robust::MAX_TEXT_BYTES + 1), "1.0.0"));
        assert!(p.set_versions("r1", "1.3.0", "1.2.0"));
        assert_eq!(p.items[0].installed, "1.3.0");
        assert_eq!(p.items[0].candidate, "1.2.0");
    }

    #[test]
    fn remove_keeps_current_in_range() {
        let mut p = sample();
        assert!(p.add_item("r2", "iris", "1.0.0", "1.0.0", SnapshotTarget::ModConfig));
        assert!(p.resolve_current(UserChoice::Keep));
        assert_eq!(p.current, 1);
        assert!(p.remove_item("r2"));
        assert_eq!(p.page_count(), 1);
        assert_eq!(p.current, 1);
        assert_eq!(p.current_item(), None);
        assert!(!p.remove_item("missing"));
    }

    #[test]
    fn summary_and_queries_match_items() {
        let mut p = sample();
        assert!(p.add_item("r2", "iris", "1.0.0", "1.0.0", SnapshotTarget::OpsJson));
        assert!(p.add_item("r3", "sodium-extra", "2.0.0", "1.0.0", SnapshotTarget::LoaderVersion));
        assert!(p.append_issue("r4", "conflict", SnapshotTarget::ModConfig));
        assert_eq!(p.summary(), [1, 1, 1, 1]);
        assert_eq!(p.by_kind(DecisionKind::HigherVersion), vec!["r1"]);
        assert_eq!(p.by_kind(DecisionKind::SameVersion), vec!["r2"]);
        assert_eq!(p.by_kind(DecisionKind::LowerVersion), vec!["r3"]);
        assert_eq!(p.by_kind(DecisionKind::OtherIssue), vec!["r4"]);
        assert_eq!(p.by_snapshot(SnapshotTarget::LoaderVersion), vec!["r3"]);
    }

    #[test]
    fn persist_and_open_roundtrip() {
        let r = tmp();
        let mut p = sample();
        assert!(p.add_item("r2", "iris", "2.0.0", "1.0.0", SnapshotTarget::ServerProperties));
        assert!(p.resolve_current(UserChoice::Replace));
        assert!(p.persist(Some(&r)).is_empty());
        let (back, lines) = ModRollback::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back, p);
        assert_eq!(back.current, 1);
        assert_eq!(back.items[0].choice, UserChoice::Replace);
        let body = fs::read_to_string(r.join(MOD_ROLLBACK_FILE)).unwrap();
        assert!(body.contains("\"kind\":\"higher_version\""));
        assert!(!body.contains(TMP_SUFFIX));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn persist_without_root_is_visible_error() {
        let p = sample();
        let lines = p.persist(None);
        assert_eq!(lines.len(), 1);
        assert!(lines[0].contains("ERROR"));
    }

    #[test]
    fn protected_files_are_not_touched() {
        for name in PROTECTED_FILES {
            assert_ne!(*name, MOD_ROLLBACK_FILE);
        }
        let r = tmp();
        assert!(reset(Some(&r)).is_empty());
        assert_eq!(ModRollback::open(Some(&r)).0, ModRollback::default());
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn event_payload_has_no_user_text() {
        let mut p = sample();
        assert!(p.add_item("r2", "iris", "1.0.0", "1.0.0", SnapshotTarget::OpsJson));
        let e = p.change_event();
        assert_eq!(e.payload.len(), 10);
        assert_eq!(e.field("id"), None);
        assert_eq!(e.field("mod_id"), None);
        assert_eq!(e.field("installed"), None);
        assert_eq!(e.field("candidate"), None);
        assert_eq!(e.field("title"), None);
        assert_eq!(e.field("body"), None);
        assert_eq!(e.field("pages"), Some("2"));
        assert_eq!(e.field("kinds"), Some("4"));
        assert_eq!(e.field("snapshots"), Some("4"));
    }

    #[test]
    fn capacity_bound_holds_after_many_adds() {
        let mut p = ModRollback::default();
        for i in 0..MAX_ITEMS + 8 {
            let _ = p.add_item(&format!("r{}", i), "m", "1.0.0", "1.0.0", SnapshotTarget::ModConfig);
        }
        assert_eq!(p.page_count(), MAX_ITEMS);
        assert_eq!(p.pending_count(), MAX_ITEMS);
    }
}

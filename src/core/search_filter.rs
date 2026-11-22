use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const SEARCH_FILTER_FILE: &str = "search-filter.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"scope":"current","sort":{"key":"name","desc":false},"conditions":[],"excludes":[],"saved":[],"history":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_CONDITIONS: usize = 24;
pub const MAX_EXCLUDES: usize = 32;
pub const MAX_SAVED: usize = 24;
pub const MAX_HISTORY: usize = 32;
pub const FILTER_TARGET: &str = "search.filter";
pub const KNOWN_KEYS: &[&str] = &["schema", "scope", "sort", "conditions", "excludes", "saved", "history"];
pub const CONDITION_KEYS: &[&str] = &["id", "dimension", "op", "value", "enabled"];
pub const SORT_KEYS: &[&str] = &["key", "desc"];
pub const SCOPES: &[&str] = &["current", "recursive"];
pub const DIMENSIONS: &[&str] = &["name", "type", "size", "modified", "path"];
pub const SORT_DIMENSIONS: &[&str] = DIMENSIONS;
pub const OPS: &[&str] = &["contains", "equals", "prefix", "suffix"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SearchDimension {
    Name,
    Type,
    Size,
    Modified,
    Path,
}

impl SearchDimension {
    pub fn code(&self) -> &'static str {
        match self {
            SearchDimension::Name => "name",
            SearchDimension::Type => "type",
            SearchDimension::Size => "size",
            SearchDimension::Modified => "modified",
            SearchDimension::Path => "path",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "name" => Some(SearchDimension::Name),
            "type" => Some(SearchDimension::Type),
            "size" => Some(SearchDimension::Size),
            "modified" => Some(SearchDimension::Modified),
            "path" => Some(SearchDimension::Path),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SearchOp {
    Contains,
    Equals,
    Prefix,
    Suffix,
}

impl SearchOp {
    pub fn code(&self) -> &'static str {
        match self {
            SearchOp::Contains => "contains",
            SearchOp::Equals => "equals",
            SearchOp::Prefix => "prefix",
            SearchOp::Suffix => "suffix",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "contains" => Some(SearchOp::Contains),
            "equals" => Some(SearchOp::Equals),
            "prefix" => Some(SearchOp::Prefix),
            "suffix" => Some(SearchOp::Suffix),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SearchCondition {
    pub id: String,
    pub dimension: SearchDimension,
    pub op: SearchOp,
    pub value: String,
    pub enabled: bool,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SortSpec {
    pub key: SearchDimension,
    pub desc: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Candidate {
    pub name: String,
    pub kind: String,
    pub size: String,
    pub modified: String,
    pub path: String,
}

impl Candidate {
    pub fn field(&self, dim: SearchDimension) -> &str {
        match dim {
            SearchDimension::Name => self.name.as_str(),
            SearchDimension::Type => self.kind.as_str(),
            SearchDimension::Size => self.size.as_str(),
            SearchDimension::Modified => self.modified.as_str(),
            SearchDimension::Path => self.path.as_str(),
        }
    }

    pub fn fields(&self) -> [&str; 5] {
        [self.name.as_str(), self.kind.as_str(), self.size.as_str(),
         self.modified.as_str(), self.path.as_str()]
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SearchFilter {
    pub scope: String,
    pub sort: SortSpec,
    pub conditions: Vec<SearchCondition>,
    pub excludes: Vec<String>,
    pub saved: Vec<String>,
    pub history: Vec<String>,
}

impl Default for SearchFilter {
    fn default() -> Self {
        SearchFilter {
            scope: "current".to_string(),
            sort: SortSpec { key: SearchDimension::Name, desc: false },
            conditions: Vec::new(),
            excludes: Vec::new(),
            saved: Vec::new(),
            history: Vec::new(),
        }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("search", action, "filter", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("search", action, "filter", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_text(s: &str) -> bool {
    !s.is_empty() && s.len() <= robust::MAX_ID_BYTES && !has_control(s)
}

fn condition_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| CONDITION_KEYS.contains(&k.as_str()))
}

fn sort_keys_ok(obj: &serde_json::Map<String, Value>) -> bool {
    obj.keys().all(|k| SORT_KEYS.contains(&k.as_str()))
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

fn parse(raw: &str) -> (SearchFilter, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (SearchFilter::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (SearchFilter::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (SearchFilter::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (SearchFilter::default(), lines);
    }
    let scope = match obj.get("scope").and_then(Value::as_str) {
        Some(s) if SCOPES.contains(&s) => s.to_string(),
        _ => {
            lines.push(degrade("load", "scope_invalid"));
            return (SearchFilter::default(), lines);
        }
    };
    let sort_obj = match obj.get("sort").and_then(Value::as_object) {
        Some(o) if sort_keys_ok(o) => o,
        _ => {
            lines.push(degrade("load", "sort_invalid"));
            return (SearchFilter::default(), lines);
        }
    };
    let desc = match sort_obj.get("desc").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "sort_invalid"));
            return (SearchFilter::default(), lines);
        }
    };
    let sort = match sort_obj.get("key").and_then(Value::as_str) {
        Some(s) if SORT_DIMENSIONS.contains(&s) => match SearchDimension::parse(s) {
            Some(d) => SortSpec { key: d, desc },
            None => {
                lines.push(degrade("load", "sort_invalid"));
                return (SearchFilter::default(), lines);
            }
        },
        _ => {
            lines.push(degrade("load", "sort_invalid"));
            return (SearchFilter::default(), lines);
        }
    };
    let cond_arr = match obj.get("conditions").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "conditions_not_array"));
            return (SearchFilter::default(), lines);
        }
    };
    let mut conditions: Vec<SearchCondition> = Vec::new();
    for (i, item) in cond_arr.iter().enumerate() {
        let entry = match item.as_object() {
            Some(e) if condition_keys_ok(e) => e,
            _ => {
                lines.push(degrade("condition", &format!("index={} bad_shape", i)));
                continue;
            }
        };
        let id = match entry.get("id").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("condition", &format!("index={} bad_id", i)));
                continue;
            }
        };
        let dimension = match entry.get("dimension").and_then(Value::as_str).and_then(SearchDimension::parse) {
            Some(d) => d,
            None => {
                lines.push(degrade("condition", &format!("index={} bad_dimension", i)));
                continue;
            }
        };
        let op = match entry.get("op").and_then(Value::as_str).and_then(SearchOp::parse) {
            Some(o) => o,
            None => {
                lines.push(degrade("condition", &format!("index={} bad_op", i)));
                continue;
            }
        };
        let val = match entry.get("value").and_then(Value::as_str) {
            Some(s) if valid_text(s) => s.to_string(),
            _ => {
                lines.push(degrade("condition", &format!("index={} bad_value", i)));
                continue;
            }
        };
        let enabled = match entry.get("enabled").and_then(Value::as_bool) {
            Some(b) => b,
            None => {
                lines.push(degrade("condition", &format!("index={} bad_enabled", i)));
                continue;
            }
        };
        if conditions.iter().any(|c| c.id == id) {
            lines.push(degrade("condition", &format!("index={} duplicate_id", i)));
            continue;
        }
        conditions.push(SearchCondition { id, dimension, op, value: val, enabled });
    }
    if conditions.len() > MAX_CONDITIONS {
        let excess = conditions.len() - MAX_CONDITIONS;
        conditions.truncate(MAX_CONDITIONS);
        lines.push(degrade("condition", &format!("overflow={}", excess)));
    }
    let ex_arr = match obj.get("excludes").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "excludes_not_array"));
            return (SearchFilter::default(), lines);
        }
    };
    let mut excludes: Vec<String> = parse_strings(ex_arr, "exclude", &mut lines);
    if excludes.len() > MAX_EXCLUDES {
        excludes.truncate(MAX_EXCLUDES);
        lines.push(degrade("exclude", "overflow"));
    }
    let sv_arr = match obj.get("saved").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "saved_not_array"));
            return (SearchFilter::default(), lines);
        }
    };
    let mut saved: Vec<String> = parse_strings(sv_arr, "saved", &mut lines);
    if saved.len() > MAX_SAVED {
        saved.truncate(MAX_SAVED);
        lines.push(degrade("saved", "overflow"));
    }
    let hi_arr = match obj.get("history").and_then(Value::as_array) {
        Some(a) => a,
        None => {
            lines.push(degrade("load", "history_not_array"));
            return (SearchFilter::default(), lines);
        }
    };
    let mut history: Vec<String> = parse_strings(hi_arr, "history", &mut lines);
    if history.len() > MAX_HISTORY {
        history.truncate(MAX_HISTORY);
        lines.push(degrade("history", "overflow"));
    }
    (SearchFilter { scope, sort, conditions, excludes, saved, history }, lines)
}

fn serialize(p: &SearchFilter) -> Result<String> {
    let conditions: Vec<Value> = p.conditions.iter().map(|c| json!({
        "id": c.id, "dimension": c.dimension.code(), "op": c.op.code(),
        "value": c.value, "enabled": c.enabled,
    })).collect();
    Ok(to_string(&json!({
        "schema": 1,
        "scope": p.scope,
        "sort": {"key": p.sort.key.code(), "desc": p.sort.desc},
        "conditions": conditions,
        "excludes": p.excludes,
        "saved": p.saved,
        "history": p.history,
    }))?)
}

fn write(root: &Path, p: &SearchFilter) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, SEARCH_FILTER_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", SEARCH_FILTER_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl SearchFilter {
    pub fn open(root: Option<&Path>) -> (SearchFilter, Vec<String>) {
        let Some(dir) = root else {
            return (SearchFilter::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, SEARCH_FILTER_FILE) {
            Ok(p) => p,
            Err(_) => return (SearchFilter::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (SearchFilter::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (SearchFilter::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn add_condition(&mut self, id: &str, dim: SearchDimension, op: SearchOp, value: &str) -> bool {
        if !valid_text(id) || !valid_text(value) {
            return false;
        }
        if self.conditions.len() >= MAX_CONDITIONS || self.conditions.iter().any(|c| c.id == id) {
            return false;
        }
        self.conditions.push(SearchCondition {
            id: id.to_string(), dimension: dim, op, value: value.to_string(), enabled: true,
        });
        true
    }

    pub fn remove_condition(&mut self, id: &str) -> bool {
        let before = self.conditions.len();
        self.conditions.retain(|c| c.id != id);
        self.conditions.len() != before
    }

    pub fn set_condition_enabled(&mut self, id: &str, enabled: bool) -> bool {
        let Some(c) = self.conditions.iter_mut().find(|c| c.id == id) else { return false; };
        c.enabled = enabled;
        true
    }

    pub fn set_condition_op(&mut self, id: &str, op: SearchOp) -> bool {
        let Some(c) = self.conditions.iter_mut().find(|c| c.id == id) else { return false; };
        c.op = op;
        true
    }

    pub fn set_condition_value(&mut self, id: &str, value: &str) -> bool {
        if !valid_text(value) { return false; }
        let Some(c) = self.conditions.iter_mut().find(|c| c.id == id) else { return false; };
        c.value = value.to_string();
        true
    }

    pub fn add_exclude(&mut self, s: &str) -> bool {
        if !valid_text(s) || self.excludes.len() >= MAX_EXCLUDES || self.excludes.iter().any(|x| x == s) {
            return false;
        }
        self.excludes.push(s.to_string());
        true
    }

    pub fn remove_exclude(&mut self, s: &str) -> bool {
        let before = self.excludes.len();
        self.excludes.retain(|x| x != s);
        self.excludes.len() != before
    }

    pub fn add_saved(&mut self, s: &str) -> bool {
        if !valid_text(s) || self.saved.len() >= MAX_SAVED || self.saved.iter().any(|x| x == s) {
            return false;
        }
        self.saved.push(s.to_string());
        true
    }

    pub fn remove_saved(&mut self, s: &str) -> bool {
        let before = self.saved.len();
        self.saved.retain(|x| x != s);
        self.saved.len() != before
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

    pub fn set_scope(&mut self, scope: &str) -> bool {
        if !SCOPES.contains(&scope) { return false; }
        self.scope = scope.to_string();
        true
    }

    pub fn set_sort(&mut self, key: SearchDimension, desc: bool) -> bool {
        if !SORT_DIMENSIONS.contains(&key.code()) { return false; }
        self.sort = SortSpec { key, desc };
        true
    }

    pub fn active_count(&self) -> usize {
        self.conditions.iter().filter(|c| c.enabled).count()
    }

    pub fn matches(&self, c: &Candidate) -> bool {
        let fields = c.fields();
        for ex in &self.excludes {
            if fields.iter().any(|f| f.contains(ex.as_str())) {
                return false;
            }
        }
        for cond in self.conditions.iter().filter(|x| x.enabled) {
            let v = c.field(cond.dimension);
            let hit = match cond.op {
                SearchOp::Contains => v.contains(cond.value.as_str()),
                SearchOp::Equals => v == cond.value.as_str(),
                SearchOp::Prefix => v.starts_with(cond.value.as_str()),
                SearchOp::Suffix => v.ends_with(cond.value.as_str()),
            };
            if !hit { return false; }
        }
        true
    }

    pub fn apply(&self, items: &[Candidate]) -> Vec<usize> {
        let mut idx: Vec<usize> = (0..items.len()).filter(|&i| self.matches(&items[i])).collect();
        idx.sort_by(|&a, &b| {
            let ord = items[a].field(self.sort.key).cmp(items[b].field(self.sort.key));
            if self.sort.desc { ord.reverse() } else { ord }
        });
        idx
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        Envelope::new(Kind::Event, FILTER_TARGET)
            .with("conditions", &self.conditions.len().to_string())
            .with("active", &self.active_count().to_string())
            .with("excludes", &self.excludes.len().to_string())
            .with("saved", &self.saved.len().to_string())
            .with("history", &self.history.len().to_string())
            .with("scope", self.scope.as_str())
            .with("sort", self.sort.key.code())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    SearchFilter::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu077-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    fn cand(name: &str, kind: &str, size: &str, modified: &str, path: &str) -> Candidate {
        Candidate { name: name.to_string(), kind: kind.to_string(), size: size.to_string(),
                    modified: modified.to_string(), path: path.to_string() }
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"scope":"current","sort":{"key":"name","desc":false},"conditions":[],"excludes":[],"saved":[],"history":[]}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 7);
    }

    #[test]
    fn enum_codes_and_tables_are_explicit() {
        assert_eq!(SearchDimension::Name.code(), "name");
        assert_eq!(SearchDimension::Type.code(), "type");
        assert_eq!(SearchDimension::Size.code(), "size");
        assert_eq!(SearchDimension::Modified.code(), "modified");
        assert_eq!(SearchDimension::Path.code(), "path");
        assert_eq!(SearchDimension::parse("nope"), None);
        assert_eq!(SearchOp::Contains.code(), "contains");
        assert_eq!(SearchOp::Equals.code(), "equals");
        assert_eq!(SearchOp::Prefix.code(), "prefix");
        assert_eq!(SearchOp::Suffix.code(), "suffix");
        assert_eq!(SearchOp::parse("nope"), None);
        assert_eq!(KNOWN_KEYS.len(), 7);
        assert_eq!(CONDITION_KEYS.len(), 5);
        assert_eq!(SORT_KEYS.len(), 2);
        assert_eq!(SCOPES.len(), 2);
        assert_eq!(DIMENSIONS.len(), 5);
        assert_eq!(OPS.len(), 4);
        assert_eq!(SORT_DIMENSIONS, DIMENSIONS);
        assert_eq!(MAX_CONDITIONS, 24);
        assert_eq!(MAX_EXCLUDES, 32);
        assert_eq!(MAX_SAVED, 24);
        assert_eq!(MAX_HISTORY, 32);
    }

    #[test]
    fn default_is_empty_with_scope_and_sort() {
        let (p, lines) = SearchFilter::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, SearchFilter::default());
        assert_eq!(p.scope, "current");
        assert_eq!(p.sort, SortSpec { key: SearchDimension::Name, desc: false });
        assert!(p.conditions.is_empty());
        assert!(p.excludes.is_empty());
        assert!(p.saved.is_empty());
        assert!(p.history.is_empty());
        assert_eq!(p.active_count(), 0);
        let c = cand("a", "jar", "1", "2026-01", "/a");
        assert!(p.matches(&c));
        assert_eq!(p.apply(&[c]), vec![0]);
        assert_eq!(p.apply(&[]), Vec::<usize>::new());
    }

    #[test]
    fn bad_root_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(SEARCH_FILTER_FILE);
        let base = DEFAULT_STATE;
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            base.replace("\"history\":[]", "\"history\":[],\"extra\":1"),
            base.replace("\"schema\":1", "\"schema\":2"),
            base.replace("\"scope\":\"current\"", "\"scope\":\"bad\""),
            base.replace("\"sort\":{\"key\":\"name\",\"desc\":false}", "\"sort\":\"no\""),
            base.replace("\"sort\":{\"key\":\"name\",\"desc\":false}", "\"sort\":{\"key\":\"name\",\"desc\":false,\"z\":1}"),
            base.replace("\"sort\":{\"key\":\"name\",\"desc\":false}", "\"sort\":{\"key\":\"bad\",\"desc\":false}"),
            base.replace("\"conditions\":[]", "\"conditions\":\"no\""),
            base.replace("\"excludes\":[]", "\"excludes\":\"no\""),
            base.replace("\"saved\":[]", "\"saved\":\"no\""),
            base.replace("\"history\":[]", "\"history\":\"no\""),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (p, lines) = SearchFilter::open(Some(&r));
            assert_eq!(p, SearchFilter::default(), "case={}", &raw[..raw.len().min(40)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(40)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_condition_entries_are_skipped_not_fatal() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"scope":"recursive","sort":{"key":"path","desc":true},"conditions":[{"id":"a","dimension":"name","op":"contains","value":"x","enabled":true},7,{"id":"","dimension":"name","op":"contains","value":"x","enabled":true},{"id":"b","dimension":"bad","op":"contains","value":"x","enabled":true},{"id":"c","dimension":"name","op":"bad","value":"x","enabled":true},{"id":"d","dimension":"name","op":"contains","value":"","enabled":true},{"id":"e","dimension":"name","op":"contains","value":"x","enabled":"no"},{"id":"f","dimension":"name","op":"contains","value":"x","enabled":true,"z":1},{"id":"a","dimension":"name","op":"equals","value":"y","enabled":false}],"excludes":[],"saved":[],"history":[]}"#;
        fs::write(r.join(SEARCH_FILTER_FILE), raw).unwrap();
        let (p, lines) = SearchFilter::open(Some(&r));
        assert_eq!(p.scope, "recursive");
        assert_eq!(p.sort, SortSpec { key: SearchDimension::Path, desc: true });
        assert_eq!(p.conditions.len(), 1);
        assert_eq!(p.conditions[0].id, "a");
        assert_eq!(p.conditions[0].op, SearchOp::Contains);
        assert!(p.conditions[0].enabled);
        assert_eq!(p.active_count(), 1);
        for tag in ["bad_shape", "bad_id", "bad_dimension", "bad_op", "bad_value", "bad_enabled", "duplicate_id"] {
            assert!(lines.iter().any(|x| x.contains(tag)), "missing={}", tag);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_string_collections_from_disk_are_skipped() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let raw = r#"{"schema":1,"scope":"current","sort":{"key":"name","desc":false},"conditions":[],"excludes":[7,"","a\nb","ok","ok"],"saved":[false,"ok2"],"history":[null,"ok3"]}"#;
        fs::write(r.join(SEARCH_FILTER_FILE), raw).unwrap();
        let (p, lines) = SearchFilter::open(Some(&r));
        assert_eq!(p.excludes, vec!["ok".to_string()]);
        assert_eq!(p.saved, vec!["ok2".to_string()]);
        assert_eq!(p.history, vec!["ok3".to_string()]);
        assert!(lines.iter().any(|x| x.contains("bad_shape")));
        assert!(lines.iter().any(|x| x.contains("bad_text")));
        assert!(lines.iter().any(|x| x.contains("duplicate")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn parse_truncates_overflow_from_disk() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let mut cond = String::from("[");
        for i in 0..(MAX_CONDITIONS + 3) {
            if i > 0 { cond.push(','); }
            cond.push_str(&format!(r#"{{"id":"q{}","dimension":"name","op":"equals","value":"v","enabled":true}}"#, i));
        }
        cond.push(']');
        let mut exc = String::from("[");
        for i in 0..(MAX_EXCLUDES + 2) {
            if i > 0 { exc.push(','); }
            exc.push_str(&format!("\"x{}\"", i));
        }
        exc.push(']');
        let raw = format!(r#"{{"schema":1,"scope":"current","sort":{{"key":"name","desc":false}},"conditions":{},"excludes":{},"saved":[],"history":[]}}"#, cond, exc);
        fs::write(r.join(SEARCH_FILTER_FILE), raw).unwrap();
        let (p, lines) = SearchFilter::open(Some(&r));
        assert_eq!(p.conditions.len(), MAX_CONDITIONS);
        assert_eq!(p.excludes.len(), MAX_EXCLUDES);
        assert!(lines.iter().any(|x| x.contains("overflow=3")));
        assert!(lines.iter().any(|x| x.contains("overflow")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn add_remove_and_bound() {
        let mut p = SearchFilter::default();
        assert!(p.add_condition("m1", SearchDimension::Name, SearchOp::Contains, "x"));
        assert!(p.add_condition("m2", SearchDimension::Path, SearchOp::Suffix, ".jar"));
        assert_eq!(p.active_count(), 2);
        assert!(!p.add_condition("m1", SearchDimension::Name, SearchOp::Contains, "x"));
        assert!(!p.add_condition("", SearchDimension::Name, SearchOp::Contains, "x"));
        assert!(!p.add_condition("bad\nid", SearchDimension::Name, SearchOp::Contains, "x"));
        assert!(!p.add_condition("y", SearchDimension::Name, SearchOp::Contains, ""));
        assert!(p.remove_condition("m1"));
        assert!(!p.remove_condition("missing"));
        assert_eq!(p.conditions.len(), 1);
        for i in 0..(MAX_CONDITIONS + 5) {
            p.add_condition(&format!("w{}", i), SearchDimension::Name, SearchOp::Equals, "v");
        }
        assert_eq!(p.conditions.len(), MAX_CONDITIONS);
    }

    #[test]
    fn single_condition_mutations_only_touch_one_item() {
        let mut p = SearchFilter::default();
        p.add_condition("a", SearchDimension::Name, SearchOp::Contains, "x");
        p.add_condition("b", SearchDimension::Name, SearchOp::Equals, "y");
        assert_eq!(p.active_count(), 2);
        assert!(p.set_condition_enabled("a", false));
        assert_eq!(p.active_count(), 1);
        assert!(!p.conditions[0].enabled);
        assert!(p.conditions[1].enabled);
        assert!(p.set_condition_op("a", SearchOp::Prefix));
        assert_eq!(p.conditions[0].op, SearchOp::Prefix);
        assert_eq!(p.conditions[1].op, SearchOp::Equals);
        assert!(p.set_condition_value("b", "z"));
        assert_eq!(p.conditions[0].value, "x");
        assert_eq!(p.conditions[1].value, "z");
        assert!(!p.set_condition_value("b", ""));
        assert!(!p.set_condition_value("missing", "q"));
        assert!(!p.set_condition_enabled("missing", false));
        assert!(!p.set_condition_op("missing", SearchOp::Suffix));
    }

    #[test]
    fn scope_and_sort_validation() {
        let mut p = SearchFilter::default();
        assert!(p.set_scope("recursive"));
        assert_eq!(p.scope, "recursive");
        assert!(p.set_scope("current"));
        assert_eq!(p.scope, "current");
        assert!(!p.set_scope("bad"));
        assert_eq!(p.scope, "current");
        assert!(p.set_sort(SearchDimension::Modified, true));
        assert_eq!(p.sort, SortSpec { key: SearchDimension::Modified, desc: true });
        assert!(p.set_sort(SearchDimension::Size, false));
        assert_eq!(p.sort, SortSpec { key: SearchDimension::Size, desc: false });
    }

    #[test]
    fn collection_add_remove_and_bounds() {
        let mut p = SearchFilter::default();
        assert!(p.add_exclude("x"));
        assert!(!p.add_exclude("x"));
        assert!(!p.add_exclude(""));
        assert!(!p.add_exclude("a\nb"));
        assert!(p.remove_exclude("x"));
        assert!(!p.remove_exclude("x"));
        assert!(p.add_saved("q1"));
        assert!(!p.add_saved("q1"));
        assert!(p.remove_saved("q1"));
        assert!(p.add_history("h1"));
        assert!(!p.add_history("h1"));
        assert!(p.remove_history("h1"));
        assert!(!p.remove_history("h1"));
        for i in 0..(MAX_EXCLUDES + 3) { p.add_exclude(&format!("e{}", i)); }
        assert_eq!(p.excludes.len(), MAX_EXCLUDES);
        for i in 0..(MAX_SAVED + 3) { p.add_saved(&format!("s{}", i)); }
        assert_eq!(p.saved.len(), MAX_SAVED);
        for i in 0..(MAX_HISTORY + 3) { p.add_history(&format!("t{}", i)); }
        assert_eq!(p.history.len(), MAX_HISTORY);
    }

    #[test]
    fn matches_empty_and_single_condition() {
        let items = vec![
            cand("mod_a", "jar", "10", "2026-01", "/m/mod_a.jar"),
            cand("mod_b", "zip", "20", "2026-03", "/m/mod_b.zip"),
            cand("tool", "jar", "30", "2026-02", "/m/tool.jar"),
        ];
        let mut p = SearchFilter::default();
        assert_eq!(p.apply(&items), vec![0, 1, 2]);
        assert!(p.add_condition("c1", SearchDimension::Name, SearchOp::Contains, "mod"));
        assert_eq!(p.apply(&items), vec![0, 1]);
        assert!(p.set_condition_enabled("c1", false));
        assert_eq!(p.apply(&items), vec![0, 1, 2]);
        assert!(p.set_condition_enabled("c1", true));
        assert!(p.set_condition_op("c1", SearchOp::Prefix));
        assert_eq!(p.apply(&items), vec![0, 1]);
        assert!(p.set_condition_op("c1", SearchOp::Equals));
        assert_eq!(p.apply(&items), Vec::<usize>::new());
    }

    #[test]
    fn matches_and_exclude_and_sort_are_derived() {
        let items = vec![
            cand("mod_a", "jar", "10", "2026-01", "/m/mod_a.jar"),
            cand("mod_b", "zip", "20", "2026-03", "/m/mod_b.zip"),
            cand("tool", "jar", "30", "2026-02", "/m/tool.jar"),
            cand("mod_c", "jar", "40", "2026-04", "/skip/mod_c.jar"),
            cand("mod_d", "jar", "50", "2026-05", "/m/mod_d.jar"),
        ];
        let mut p = SearchFilter::default();
        assert_eq!(p.apply(&items), vec![0, 1, 3, 4, 2]);
        assert!(p.add_condition("c1", SearchDimension::Name, SearchOp::Contains, "mod"));
        assert_eq!(p.apply(&items), vec![0, 1, 3, 4]);
        assert!(p.add_condition("c2", SearchDimension::Type, SearchOp::Equals, "jar"));
        assert_eq!(p.apply(&items), vec![0, 3, 4]);
        assert!(p.set_condition_enabled("c2", false));
        assert_eq!(p.apply(&items), vec![0, 1, 3, 4]);
        assert!(p.add_exclude("skip"));
        assert_eq!(p.apply(&items), vec![0, 1, 4]);
        assert!(p.set_sort(SearchDimension::Modified, true));
        assert_eq!(p.apply(&items), vec![4, 1, 0]);
        assert!(p.set_sort(SearchDimension::Size, false));
        assert_eq!(p.apply(&items), vec![0, 1, 4]);
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut p = SearchFilter::default();
        p.add_condition("a", SearchDimension::Name, SearchOp::Contains, "x");
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
        let mut p = SearchFilter::default();
        assert!(p.set_scope("recursive"));
        assert!(p.set_sort(SearchDimension::Modified, true));
        assert!(p.add_condition("a", SearchDimension::Name, SearchOp::Prefix, "mod"));
        assert!(p.add_condition("b", SearchDimension::Path, SearchOp::Suffix, ".jar"));
        assert!(p.set_condition_enabled("b", false));
        assert!(p.add_exclude("skip"));
        assert!(p.add_saved("q1"));
        assert!(p.add_history("h1"));
        assert!(p.persist(Some(&r)).is_empty());
        let (back, lines) = SearchFilter::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.scope, "recursive");
        assert_eq!(back.sort, SortSpec { key: SearchDimension::Modified, desc: true });
        assert_eq!(back.conditions.len(), 2);
        assert_eq!(back.conditions[0].op, SearchOp::Prefix);
        assert_eq!(back.conditions[1].op, SearchOp::Suffix);
        assert!(!back.conditions[1].enabled);
        assert_eq!(back.active_count(), 1);
        assert_eq!(back.excludes, vec!["skip".to_string()]);
        assert_eq!(back.saved, vec!["q1".to_string()]);
        assert_eq!(back.history, vec!["h1".to_string()]);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = SearchFilter::open(Some(&r));
        assert_eq!(def, SearchFilter::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope_without_user_text() {
        let mut p = SearchFilter::default();
        p.add_condition("a", SearchDimension::Name, SearchOp::Contains, "secret-value");
        p.add_condition("b", SearchDimension::Path, SearchOp::Equals, "another-value");
        p.set_condition_enabled("b", false);
        p.add_exclude("excluded-text");
        p.add_saved("saved-text");
        p.add_history("history-text");
        let e = p.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, FILTER_TARGET);
        assert_eq!(e.field("conditions"), Some("2"));
        assert_eq!(e.field("active"), Some("1"));
        assert_eq!(e.field("excludes"), Some("1"));
        assert_eq!(e.field("saved"), Some("1"));
        assert_eq!(e.field("history"), Some("1"));
        assert_eq!(e.field("scope"), Some("current"));
        assert_eq!(e.field("sort"), Some("name"));
        assert_eq!(e.field("ids"), None);
        assert_eq!(e.field("values"), None);
        assert_eq!(e.field("text"), None);
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 7);
    }

    #[test]
    fn serialize_carries_no_condition_table() {
        let mut p = SearchFilter::default();
        p.add_condition("a", SearchDimension::Name, SearchOp::Contains, "x");
        let raw = serialize(&p).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 7);
        assert!(!raw.contains("CONDITION_TABLE"));
        assert!(!raw.contains("VALUE_TABLE"));
        assert!(!raw.contains("cmp_precedence"));
        assert!(!raw.contains("semver"));
    }
}

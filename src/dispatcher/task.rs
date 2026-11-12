use crate::core::args::LaunchArgs;
use crate::dispatcher::json::Json;
use std::collections::BTreeMap;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum TaskKind {
    Launch,
    Join,
    Server,
    Unknown(String),
}

impl TaskKind {
    pub fn parse(s: &str) -> Self {
        match s {
            "launch" => TaskKind::Launch,
            "join" => TaskKind::Join,
            "server" => TaskKind::Server,
            "" => TaskKind::Launch,
            other => TaskKind::Unknown(other.to_string()),
        }
    }

    pub fn code(&self) -> &str {
        match self {
            TaskKind::Launch => "launch",
            TaskKind::Join => "join",
            TaskKind::Server => "server",
            TaskKind::Unknown(s) => s,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct LaunchTask {
    pub id: String,
    pub kind: TaskKind,
    pub server: Option<String>,
    pub instance: Option<String>,
    pub mode: Option<String>,
    pub kculf: Option<String>,
    pub kculh: Option<String>,
    pub version: Option<String>,
    pub lang: Option<String>,
    pub extras: BTreeMap<String, String>,
}

impl Default for LaunchTask {
    fn default() -> Self {
        Self {
            id: "default".to_string(),
            kind: TaskKind::Launch,
            server: None,
            instance: None,
            mode: None,
            kculf: None,
            kculh: None,
            version: None,
            lang: None,
            extras: BTreeMap::new(),
        }
    }
}

impl LaunchTask {
    pub fn from_json(value: &Json) -> Result<Self, String> {
        let obj = match value {
            Json::Obj(_) => value,
            _ => return Err("task root must be an object".to_string()),
        };
        let mut t = Self::default();
        if let Some(v) = obj.string_field("id") {
            if !v.trim().is_empty() {
                t.id = v;
            }
        }
        if let Some(v) = obj.string_field("kind") {
            t.kind = TaskKind::parse(&v);
        }
        for (field, slot) in [
            ("server", 0),
            ("instance", 1),
            ("mode", 2),
            ("kculf", 3),
            ("kculh", 4),
            ("version", 5),
            ("lang", 6),
        ] {
            if let Some(v) = obj.string_field(field) {
                if v.trim().is_empty() {
                    continue;
                }
                match slot {
                    0 => t.server = Some(v),
                    1 => t.instance = Some(v),
                    2 => t.mode = Some(v),
                    3 => t.kculf = Some(v),
                    4 => t.kculh = Some(v),
                    5 => t.version = Some(v),
                    _ => t.lang = Some(v),
                }
            }
        }
        if let Some(Json::Bool(b)) = obj.get("headless") {
            if *b && t.kculh.is_none() {
                t.kculh = Some(t.id.clone());
            }
        }
        if let Some(Json::Obj(m)) = obj.get("extras") {
            for (k, v) in m {
                if let Some(s) = v.as_str() {
                    t.extras.insert(k.clone(), s.to_string());
                }
            }
        }
        Ok(t)
    }

    pub fn from_str(input: &str) -> Result<Self, String> {
        let value = super::json::parse(input)?;
        Self::from_json(&value)
    }

    pub fn from_args(args: &LaunchArgs) -> Self {
        let mut t = Self::default();
        t.id = "cmd".to_string();
        if args.joins_server() {
            t.kind = TaskKind::Join;
            t.server = args.server.clone();
        }
        t.instance = args.instance.clone();
        t.mode = args.mode.clone();
        t.kculf = args.kculf.clone();
        t.kculh = args.kculh.clone();
        t.lang = args.lang.clone();
        for (i, x) in args.extras.iter().enumerate() {
            t.extras.insert(format!("arg{}", i), x.clone());
        }
        t
    }

    pub fn headless(&self) -> bool {
        self.kculh.is_some()
            || self.mode.as_deref() == Some("headless")
            || self.kind == TaskKind::Unknown("headless".to_string())
    }

    pub fn joins_server(&self) -> bool {
        self.server.is_some() || self.kind == TaskKind::Join
    }
}

#[derive(Debug, Clone, Default)]
pub struct TaskSet {
    pub tasks: Vec<LaunchTask>,
}

impl TaskSet {
    pub fn from_values(values: &[Json]) -> Result<Self, String> {
        let mut tasks = Vec::with_capacity(values.len());
        for v in values {
            tasks.push(LaunchTask::from_json(v)?);
        }
        tasks.sort_by(|a, b| a.id.cmp(&b.id));
        tasks.dedup_by(|a, b| a.id == b.id);
        Ok(Self { tasks })
    }

    pub fn from_texts(texts: &[&str]) -> Result<Self, String> {
        let mut values = Vec::with_capacity(texts.len());
        for t in texts {
            values.push(super::json::parse(t)?);
        }
        Self::from_values(&values)
    }

    pub fn len(&self) -> usize {
        self.tasks.len()
    }

    pub fn is_empty(&self) -> bool {
        self.tasks.is_empty()
    }

    pub fn pick(&self, args: &LaunchArgs) -> LaunchTask {
        if args.joins_server() {
            return LaunchTask::from_args(args);
        }
        if let Some(t) = self.tasks.iter().find(|t| t.headless()) {
            return t.clone();
        }
        self.tasks.first().cloned().unwrap_or_default()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn parses_full_task() {
        let t = LaunchTask::from_str(r#"{"id":"a","kind":"join","server":"s:25565","instance":"i1","mode":"normal","version":"1.20.4","lang":"zh-CN","extras":{"x":"1"}}"#).unwrap();
        assert_eq!(t.id, "a");
        assert_eq!(t.kind, TaskKind::Join);
        assert_eq!(t.server.as_deref(), Some("s:25565"));
        assert_eq!(t.instance.as_deref(), Some("i1"));
        assert_eq!(t.extras.get("x").map(String::as_str), Some("1"));
        assert!(t.joins_server());
    }

    #[test]
    fn empty_fields_fall_back_to_defaults() {
        let t = LaunchTask::from_str("{}").unwrap();
        assert_eq!(t.id, "default");
        assert_eq!(t.kind, TaskKind::Launch);
        assert!(!t.joins_server());
        assert!(!t.headless());
    }

    #[test]
    fn root_must_be_object() {
        assert!(LaunchTask::from_str("[1,2]").is_err());
        assert!(LaunchTask::from_str("{bad").is_err());
    }

    #[test]
    fn headless_flag_and_kculh_set_headless() {
        let t = LaunchTask::from_str(r#"{"id":"h","headless":true}"#).unwrap();
        assert!(t.headless());
        assert_eq!(t.kculh.as_deref(), Some("h"));
        assert!(LaunchTask::from_str(r#"{"mode":"headless"}"#).unwrap().headless());
    }

    #[test]
    fn single_arg_generates_join_task() {
        let a = LaunchArgs::parse(["--server", "mc.example.net:25565"]).unwrap();
        let t = LaunchTask::from_args(&a);
        assert_eq!(t.kind, TaskKind::Join);
        assert_eq!(t.id, "cmd");
        assert!(t.joins_server());
    }

    #[test]
    fn task_set_is_sorted_deduped_and_picks_headless_first() {
        let s = TaskSet::from_texts(&[
            r#"{"id":"z","kind":"launch"}"#,
            r#"{"id":"a","kind":"launch"}"#,
            r#"{"id":"h","kculh":"x.kculh"}"#,
            r#"{"id":"z","kind":"server"}"#,
        ])
        .unwrap();
        assert_eq!(s.len(), 3);
        assert_eq!(s.tasks[0].id, "a");
        assert_eq!(s.pick(&LaunchArgs::default()).id, "h");
    }

    #[test]
    fn empty_task_set_yields_default_task() {
        let s = TaskSet::default();
        assert!(s.is_empty());
        assert_eq!(s.pick(&LaunchArgs::default()), LaunchTask::default());
    }

    #[test]
    fn cmd_arg_overrides_task_files() {
        let s = TaskSet::from_texts(&[r#"{"id":"a","mode":"normal"}"#]).unwrap();
        let a = LaunchArgs::parse(["--server", "x:1", "--mode", "lightweight"]).unwrap();
        let t = s.pick(&a);
        assert_eq!(t.id, "cmd");
        assert_eq!(t.mode.as_deref(), Some("lightweight"));
        assert!(t.joins_server());
    }
}

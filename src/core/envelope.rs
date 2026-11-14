use serde_json::{from_str, to_string, Map, Value};
use std::sync::atomic::{AtomicU64, Ordering};

static SEQ: AtomicU64 = AtomicU64::new(0);

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Kind {
    Request,
    Response,
    Event,
}

#[derive(Debug, Clone)]
pub struct Envelope {
    pub request_id: String,
    pub kind: Kind,
    pub target: String,
    pub payload: Map<String, Value>,
    pub error: Option<String>,
}

impl Envelope {
    pub fn new(kind: Kind, target: &str) -> Self {
        let n = SEQ.fetch_add(1, Ordering::Relaxed) + 1;
        Self {
            request_id: format!("kcu-{:08x}", n),
            kind,
            target: target.to_string(),
            payload: Map::new(),
            error: None,
        }
    }

    pub fn with(mut self, key: &str, value: &str) -> Self {
        self.payload
            .insert(key.to_string(), Value::String(value.to_string()));
        self
    }

    pub fn with_error(mut self, message: &str) -> Self {
        self.error = Some(message.to_string());
        self
    }

    pub fn ok(&self) -> bool {
        self.error.is_none()
    }

    pub fn field(&self, key: &str) -> Option<&str> {
        self.payload.get(key).and_then(Value::as_str)
    }

    pub fn to_json_string(&self) -> anyhow::Result<String> {
        let mut m = self.payload.clone();
        m.insert(
            "request_id".to_string(),
            Value::String(self.request_id.clone()),
        );
        m.insert(
            "kind".to_string(),
            Value::String(format!("{:?}", self.kind)),
        );
        m.insert("target".to_string(), Value::String(self.target.clone()));
        if let Some(e) = &self.error {
            m.insert("error".to_string(), Value::String(e.clone()));
        }
        Ok(to_string(&Value::Object(m))?)
    }

    pub fn from_json_str(s: &str) -> anyhow::Result<Value> {
        Ok(from_str(s)?)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn ids_are_unique() {
        let a = Envelope::new(Kind::Request, "core.paths");
        let b = Envelope::new(Kind::Request, "core.paths");
        assert_ne!(a.request_id, b.request_id);
        assert!(a.ok());
    }

    #[test]
    fn error_clears_ok() {
        let e = Envelope::new(Kind::Response, "core.args").with_error("E01");
        assert!(!e.ok());
        assert_eq!(e.error.as_deref(), Some("E01"));
    }

    #[test]
    fn payload_order_is_stable() {
        let e = Envelope::new(Kind::Event, "core.log")
            .with("b", "2")
            .with("a", "1");
        let keys: Vec<String> = e.payload.keys().cloned().collect();
        assert_eq!(keys, vec!["a".to_string(), "b".to_string()]);
        assert_eq!(e.field("a"), Some("1"));
    }

    #[test]
    fn json_output_is_parseable_and_keeps_fields() {
        let e = Envelope::new(Kind::Event, "core.log").with("line", "hello");
        let s = e.to_json_string().unwrap();
        let v = Envelope::from_json_str(&s).unwrap();
        assert_eq!(v["target"], "core.log");
        assert_eq!(v["line"], "hello");
        assert_eq!(v["kind"], "Event");
        assert!(v.get("error").is_none());
    }

    #[test]
    fn json_output_keeps_error() {
        let e = Envelope::new(Kind::Response, "core.args").with_error("E02");
        let v = Envelope::from_json_str(&e.to_json_string().unwrap()).unwrap();
        assert_eq!(v["error"], "E02");
    }
}

use serde_json::{from_str, to_string, Map, Value};
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::OnceLock;
use std::time::{SystemTime, UNIX_EPOCH};
use uuid::Uuid;

static SEQ: AtomicU64 = AtomicU64::new(0);

/// 进程启动时取一次纳秒时间戳，参与 name，避免 pid 复用 + 计数归零时跨启动撞 ID。
fn session_seed() -> u128 {
    static SEED: OnceLock<u128> = OnceLock::new();
    *SEED.get_or_init(|| {
        SystemTime::now()
            .duration_since(UNIX_EPOCH)
            .map(|d| d.as_nanos())
            .unwrap_or(0)
    })
}

/// 由库实现 RFC 9562 的版本 5 命名空间 UUID：SHA-1(namespace || name)，
/// 再设置 version=5 与 RFC 4122 variant 位。项目侧不手写摘要与位操作。
pub fn derive_id(name: &str) -> String {
    Uuid::new_v5(&Uuid::NAMESPACE_OID, name.as_bytes()).to_string()
}

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
        let name = format!(
            "kcu/{}/{}/{}/{:?}/{}",
            std::process::id(),
            session_seed(),
            n,
            kind,
            target
        );
        Self {
            request_id: derive_id(&name),
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
    use uuid::{Variant, Version};

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

    // 期望值由 Python 标准库 uuid.uuid5(uuid.NAMESPACE_OID, name) 独立算出，
    // 不依赖本仓库的 uuid / sha1_smol 实现，用于换库前后行为对齐。
    #[test]
    fn matches_independent_uuid_v5_reference() {
        assert_eq!(
            derive_id("kcu-fixture-0001"),
            "d4bf11e5-29b6-5b3f-a553-5701cc26efd5"
        );
        assert_eq!(
            derive_id("kcu-fixture-0002"),
            "04f2fd33-d7a7-540a-9552-31d9ec50d344"
        );
        assert_eq!(
            derive_id("core.start/1"),
            "fb682a9c-378d-5faf-919a-502fb45585db"
        );
        assert_eq!(
            derive_id(""),
            "0a68eb57-c88a-5f34-9e9d-27f85e68af4f"
        );
    }

    #[test]
    fn request_id_is_a_parseable_rfc4122_v5_uuid() {
        let e = Envelope::new(Kind::Request, "core.window");
        let u = Uuid::parse_str(&e.request_id).unwrap();
        assert_eq!(u.get_version(), Some(Version::Sha1));
        assert_eq!(u.get_variant(), Variant::RFC4122);
        assert_eq!(e.request_id.len(), 36);
        assert_eq!(e.request_id.chars().filter(|c| *c == '-').count(), 4);
    }

    #[test]
    fn derive_id_is_deterministic_and_name_sensitive() {
        assert_eq!(derive_id("same"), derive_id("same"));
        assert_ne!(derive_id("same"), derive_id("other"));
    }

    #[test]
    fn json_output_carries_the_uuid_request_id() {
        let e = Envelope::new(Kind::Event, "core.diag");
        let v = Envelope::from_json_str(&e.to_json_string().unwrap()).unwrap();
        assert_eq!(v["request_id"], e.request_id);
        assert!(Uuid::parse_str(v["request_id"].as_str().unwrap()).is_ok());
    }

    #[test]
    fn different_kinds_and_targets_do_not_share_ids() {
        let a = Envelope::new(Kind::Request, "core.paths");
        let b = Envelope::new(Kind::Response, "core.paths");
        let c = Envelope::new(Kind::Request, "core.log");
        assert_ne!(a.request_id, b.request_id);
        assert_ne!(a.request_id, c.request_id);
        assert_ne!(b.request_id, c.request_id);
    }
}

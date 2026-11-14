use serde_json::{from_str, to_string, Map, Value};

pub struct Config {
    pub os_class: String,
    pub language: String,
    pub mirror_speedtest: bool,
    data: Map<String, Value>,
    region_override: Option<String>,
}

impl Config {
    pub fn empty(os_class: &str) -> Self {
        let mut data = Map::new();
        Self::ensure_object(&mut data, "endpoints");
        Self::ensure_object(&mut data, "ports");
        Self {
            os_class: os_class.to_string(),
            language: "zh-CN".to_string(),
            mirror_speedtest: true,
            data,
            region_override: None,
        }
    }

    pub fn from_json_str(s: &str) -> anyhow::Result<Self> {
        let v: Value = from_str(s)?;
        let root = v
            .as_object()
            .ok_or_else(|| anyhow::anyhow!("config root is not an object"))?
            .clone();
        let mut data = root;
        Self::ensure_object(&mut data, "endpoints");
        Self::ensure_object(&mut data, "ports");
        let os_class = data
            .get("os_class")
            .and_then(Value::as_str)
            .unwrap_or("windows")
            .to_string();
        let language = data
            .get("language")
            .and_then(Value::as_str)
            .unwrap_or("zh-CN")
            .to_string();
        let mirror_speedtest = data
            .get("mirror_speedtest")
            .and_then(Value::as_bool)
            .unwrap_or(true);
        let region_override = data
            .get("download_region")
            .and_then(Value::as_str)
            .map(str::to_string);
        Ok(Self {
            os_class,
            language,
            mirror_speedtest,
            data,
            region_override,
        })
    }

    pub fn to_json_string(&self) -> anyhow::Result<String> {
        let mut root = self.data.clone();
        root.insert("os_class".to_string(), Value::String(self.os_class.clone()));
        root.insert("language".to_string(), Value::String(self.language.clone()));
        root.insert(
            "mirror_speedtest".to_string(),
            Value::Bool(self.mirror_speedtest),
        );
        if let Some(r) = &self.region_override {
            root.insert("download_region".to_string(), Value::String(r.clone()));
        }
        Ok(to_string(&Value::Object(root))?)
    }

    fn ensure_object(data: &mut Map<String, Value>, key: &str) {
        let slot = data
            .entry(key.to_string())
            .or_insert_with(|| Value::Object(Map::new()));
        if !slot.is_object() {
            *slot = Value::Object(Map::new());
        }
    }

    fn endpoints(&self) -> Option<&Map<String, Value>> {
        self.data.get("endpoints").and_then(Value::as_object)
    }

    fn ports(&self) -> Option<&Map<String, Value>> {
        self.data.get("ports").and_then(Value::as_object)
    }

    pub fn set_endpoint(&mut self, key: &str, url: &str) {
        Self::ensure_object(&mut self.data, "endpoints");
        if let Some(m) = self
            .data
            .get_mut("endpoints")
            .and_then(Value::as_object_mut)
        {
            m.insert(key.to_string(), Value::String(url.to_string()));
        }
    }

    pub fn endpoint(&self, key: &str) -> Option<&str> {
        self.endpoints()
            .and_then(|m| m.get(key))
            .and_then(Value::as_str)
    }

    pub fn set_port(&mut self, key: &str, port: u16) {
        Self::ensure_object(&mut self.data, "ports");
        if let Some(m) = self.data.get_mut("ports").and_then(Value::as_object_mut) {
            m.insert(key.to_string(), Value::from(port as u64));
        }
    }

    pub fn port(&self, key: &str) -> Option<u16> {
        self.ports()
            .and_then(|m| m.get(key))
            .and_then(Value::as_u64)
            .and_then(|n| u16::try_from(n).ok())
    }

    pub fn endpoint_keys(&self) -> Vec<String> {
        self.endpoints()
            .map(|m| m.keys().cloned().collect())
            .unwrap_or_default()
    }

    pub fn set_download_region(&mut self, region: &str) {
        self.region_override = Some(region.to_string());
    }

    pub fn download_region(&self) -> Option<&str> {
        self.region_override.as_deref()
    }

    pub fn has_policy_endpoint(&self) -> bool {
        self.endpoints()
            .map(|m| m.keys().any(|k| k.starts_with("policy/")))
            .unwrap_or(false)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn endpoints_are_injected() {
        let mut c = Config::empty("windows");
        assert_eq!(c.endpoint("download/java"), None);
        c.set_endpoint("download/java", "java-source-a");
        assert_eq!(c.endpoint("download/java"), Some("java-source-a"));
    }

    #[test]
    fn ports_are_injected() {
        let mut c = Config::empty("windows");
        c.set_port("ai/local", 0);
        assert_eq!(c.port("ai/local"), Some(0));
    }

    #[test]
    fn region_override_only_exposed_for_download_selection() {
        let mut c = Config::empty("windows");
        c.set_download_region("overseas");
        assert_eq!(c.download_region(), Some("overseas"));
        assert!(!c.has_policy_endpoint());
    }

    #[test]
    fn language_pack_is_configurable() {
        let mut c = Config::empty("windows");
        c.language = "en-US".to_string();
        assert_eq!(c.language, "en-US");
    }

    #[test]
    fn malformed_endpoints_is_normalised_not_panicking() {
        let c = Config::from_json_str(r#"{"endpoints":"oops","ports":[1,2]}"#).unwrap();
        assert_eq!(c.endpoint("a"), None);
        assert_eq!(c.port("b"), None);
        assert!(c.endpoint_keys().is_empty());
        assert!(!c.has_policy_endpoint());
    }

    #[test]
    fn writes_recover_after_malformed_input() {
        let mut c = Config::from_json_str(r#"{"endpoints":null,"ports":false}"#).unwrap();
        c.set_endpoint("download/java", "mirror-a");
        c.set_port("ai/local", 8787);
        assert_eq!(c.endpoint("download/java"), Some("mirror-a"));
        assert_eq!(c.port("ai/local"), Some(8787));
    }

    #[test]
    fn roundtrip_still_normalises_nested_objects() {
        let mut c = Config::empty("windows");
        c.set_endpoint("policy/mirror", "off");
        let s = c.to_json_string().unwrap();
        let back = Config::from_json_str(&s).unwrap();
        assert_eq!(back.endpoint("policy/mirror"), Some("off"));
        assert!(back.has_policy_endpoint());
    }

    #[test]
    fn json_roundtrip_keeps_every_value() {
        let mut c = Config::empty("windows");
        c.language = "en-US".to_string();
        c.mirror_speedtest = false;
        c.set_endpoint("download/java", "java-source-a");
        c.set_port("ai/local", 8080);
        c.set_download_region("overseas");
        let s = c.to_json_string().unwrap();
        let d = Config::from_json_str(&s).unwrap();
        assert_eq!(d.language, "en-US");
        assert!(!d.mirror_speedtest);
        assert_eq!(d.endpoint("download/java"), Some("java-source-a"));
        assert_eq!(d.port("ai/local"), Some(8080));
        assert_eq!(d.download_region(), Some("overseas"));
    }

    #[test]
    fn malformed_json_is_rejected() {
        assert!(Config::from_json_str("not json").is_err());
        assert!(Config::from_json_str("[]").is_err());
    }

    #[test]
    fn missing_sections_are_defaulted() {
        let c = Config::from_json_str(r#"{"os_class":"linux"}"#).unwrap();
        assert_eq!(c.os_class, "linux");
        assert_eq!(c.endpoint_keys().len(), 0);
        assert_eq!(c.port("ai/local"), None);
    }
}

use std::collections::BTreeMap;

pub struct Config {
    pub os_class: String,
    pub language: String,
    pub mirror_speedtest: bool,
    endpoints: BTreeMap<String, String>,
    ports: BTreeMap<String, u16>,
    region_override: Option<String>,
}

impl Config {
    pub fn empty(os_class: &str) -> Self {
        Self {
            os_class: os_class.to_string(),
            language: "zh-CN".to_string(),
            mirror_speedtest: true,
            endpoints: BTreeMap::new(),
            ports: BTreeMap::new(),
            region_override: None,
        }
    }

    pub fn set_endpoint(&mut self, key: &str, url: &str) {
        self.endpoints.insert(key.to_string(), url.to_string());
    }

    pub fn endpoint(&self, key: &str) -> Option<&str> {
        self.endpoints.get(key).map(String::as_str)
    }

    pub fn set_port(&mut self, key: &str, port: u16) {
        self.ports.insert(key.to_string(), port);
    }

    pub fn port(&self, key: &str) -> Option<u16> {
        self.ports.get(key).copied()
    }

    pub fn endpoint_keys(&self) -> Vec<String> {
        self.endpoints.keys().cloned().collect()
    }

    pub fn set_download_region(&mut self, region: &str) {
        self.region_override = Some(region.to_string());
    }

    pub fn download_region(&self) -> Option<&str> {
        self.region_override.as_deref()
    }

    pub fn has_policy_endpoint(&self) -> bool {
        self.endpoints.keys().any(|k| k.starts_with("policy/"))
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
}

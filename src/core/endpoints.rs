//! 联网端点集中解析层。
//!
//! 048 合规核对 B03 / EQ-15 选项①：scheme、authority、path 从
//! `Config::endpoint("download/batch")` 读取，缺省才回内置常量。
//! 解析交给 `http::Uri`，不自己写主机名与 URL 规则。

use crate::core::config::Config;
use crate::core::http;
use ::http::Uri;

pub const DOWNLOAD_BATCH_KEY: &str = "download/batch";
pub const DEFAULT_SCHEME: &str = "https";
pub const DEFAULT_PATH: &str = "/v1/batch";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Origin {
    /// 没配端点，用内置缺省。
    Default,
    /// 配置解析通过并生效。
    Config,
    /// 配了但不可用，回退到内置缺省，不 panic、不静默吞。
    Fallback,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Endpoint {
    pub scheme: String,
    pub authority: String,
    pub path: String,
    pub origin: Origin,
    pub reason: &'static str,
}

/// 从 `Config` 拷出的纯数据，避免让 `ProviderConfig` 持有 `Config` 本体。
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct EndpointConfig {
    pub raw: String,
}

impl EndpointConfig {
    pub fn new(raw: &str) -> Self {
        Self { raw: raw.to_string() }
    }
}

pub fn from_app_config(cfg: &Config) -> Option<EndpointConfig> {
    cfg.endpoint(DOWNLOAD_BATCH_KEY).map(EndpointConfig::new)
}

fn fallback(base: &str, reason: &'static str) -> Endpoint {
    Endpoint {
        scheme: DEFAULT_SCHEME.to_string(),
        authority: base.to_string(),
        path: DEFAULT_PATH.to_string(),
        origin: Origin::Fallback,
        reason,
    }
}

fn default(base: &str) -> Endpoint {
    Endpoint {
        scheme: DEFAULT_SCHEME.to_string(),
        authority: base.to_string(),
        path: DEFAULT_PATH.to_string(),
        origin: Origin::Default,
        reason: "not_configured",
    }
}

/// 配置值支持两种写法：
/// - 完整 URL：scheme、authority（可带端口）、path 三段齐全
/// - 仅 authority：`mirror-b:8080`（scheme 与 path 保留缺省）
///
/// 不可用的配置一律回退，并带 `reason`；查询串、片段、`§` 模板、非 http/https
/// scheme、解析失败都不接受，因为 `http::plan` 会追加自己的 `?page=&ids=`。
pub fn resolve(base: &str, configured: Option<&EndpointConfig>) -> Endpoint {
    let Some(cfg) = configured else {
        return default(base);
    };
    let raw = cfg.raw.trim();
    if raw.is_empty() {
        return fallback(base, "empty_endpoint");
    }
    if raw.contains('\u{00a7}') {
        return fallback(base, "template_not_supported");
    }
    if !raw.contains("://") {
        return match http::validate_authority(raw) {
            Ok(()) => Endpoint {
                scheme: DEFAULT_SCHEME.to_string(),
                authority: raw.to_string(),
                path: DEFAULT_PATH.to_string(),
                origin: Origin::Config,
                reason: "authority_only",
            },
            Err(_) => fallback(base, "invalid_authority"),
        };
    }

    let uri: Uri = match raw.parse() {
        Ok(u) => u,
        Err(_) => return fallback(base, "uri_parse_failed"),
    };
    let scheme = match uri.scheme_str() {
        Some(s @ ("http" | "https")) => s.to_string(),
        _ => return fallback(base, "unsupported_scheme"),
    };
    let authority = match uri.authority() {
        Some(a) => a.as_str().to_string(),
        None => return fallback(base, "missing_authority"),
    };
    if uri.host().is_none() {
        return fallback(base, "missing_host");
    }
    if uri.query().is_some() {
        return fallback(base, "query_not_allowed");
    }
    // http::plan 用 spec.path 拼 "?page=N&ids=..."，配置里带 query 会冲突。
    let path = match uri.path() {
        "" | "/" => DEFAULT_PATH.to_string(),
        p if p.starts_with('/') && !p.contains('?') && !p.contains('#') => p.to_string(),
        _ => return fallback(base, "invalid_path"),
    };
    if http::validate_authority(&authority).is_err() {
        return fallback(base, "invalid_authority");
    }
    Endpoint {
        scheme,
        authority,
        path,
        origin: Origin::Config,
        reason: "full_url",
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn url(scheme: &str, host: &str, path: &str) -> String {
        [scheme, "://", host, path].concat()
    }

    #[test]
    fn no_config_keeps_builtin_defaults_verbatim() {
        let e = resolve("mirror-a", None);
        assert_eq!(e.scheme, "https");
        assert_eq!(e.authority, "mirror-a");
        assert_eq!(e.path, "/v1/batch");
        assert_eq!(e.origin, Origin::Default);
    }

    #[test]
    fn full_url_overrides_scheme_authority_and_path() {
        let c = EndpointConfig::new(&url("http", "mirror-b:8080", "/v2/batch"));
        let e = resolve("mirror-a", Some(&c));
        assert_eq!(e.scheme, "http");
        assert_eq!(e.authority, "mirror-b:8080");
        assert_eq!(e.path, "/v2/batch");
        assert_eq!(e.origin, Origin::Config);
        assert_eq!(e.reason, "full_url");
    }

    #[test]
    fn authority_only_keeps_default_scheme_and_path() {
        let c = EndpointConfig::new("mirror-b:9000");
        let e = resolve("mirror-a", Some(&c));
        assert_eq!(e.scheme, "https");
        assert_eq!(e.authority, "mirror-b:9000");
        assert_eq!(e.path, "/v1/batch");
        assert_eq!(e.origin, Origin::Config);
        assert_eq!(e.reason, "authority_only");
    }

    #[test]
    fn host_only_url_keeps_default_path() {
        let c = EndpointConfig::new(&url("http", "mirror-b", ""));
        let e = resolve("mirror-a", Some(&c));
        assert_eq!(e.scheme, "http");
        assert_eq!(e.authority, "mirror-b");
        assert_eq!(e.path, "/v1/batch");
        assert_eq!(e.origin, Origin::Config);
    }

    #[test]
    fn empty_and_whitespace_fall_back() {
        for raw in ["", "   "] {
            let e = resolve("mirror-a", Some(&EndpointConfig::new(raw)));
            assert_eq!(e.origin, Origin::Fallback);
            assert_eq!(e.reason, "empty_endpoint");
            assert_eq!(e.authority, "mirror-a");
        }
    }

    #[test]
    fn unsupported_scheme_falls_back() {
        let c = EndpointConfig::new(&url("ftp", "mirror-b", "/v1/batch"));
        let e = resolve("mirror-a", Some(&c));
        assert_eq!(e.origin, Origin::Fallback);
        assert_eq!(e.reason, "unsupported_scheme");
        assert_eq!(e.scheme, "https");
        assert_eq!(e.path, "/v1/batch");
    }

    #[test]
    fn query_in_config_falls_back() {
        let c = EndpointConfig::new(&url("https", "mirror-b", "/v1/batch?x=1"));
        let e = resolve("mirror-a", Some(&c));
        assert_eq!(e.origin, Origin::Fallback);
        assert_eq!(e.reason, "query_not_allowed");
    }

    #[test]
    fn malformed_url_falls_back_not_panics() {
        let candidates = [
            ["https", "://"].concat(),
            ["http", "://", "bad host/x"].concat(),
            ["http", "://", "/x"].concat(),
            ["://", "mirror-b"].concat(),
        ];
        for raw in &candidates {
            let e = resolve("mirror-a", Some(&EndpointConfig::new(raw)));
            assert_eq!(e.origin, Origin::Fallback, "raw={}", raw);
            assert_eq!(e.authority, "mirror-a");
        }
    }

    #[test]
    fn template_marker_falls_back_explicitly() {
        let raw = ["https", "://", "mirror-b", "/v1/download/", "\u{00a7}"].concat();
        let c = EndpointConfig::new(&raw);
        let e = resolve("mirror-a", Some(&c));
        assert_eq!(e.origin, Origin::Fallback);
        assert_eq!(e.reason, "template_not_supported");
    }

    #[test]
    fn from_app_config_reads_the_existing_table() {
        let mut cfg = Config::empty("windows");
        assert!(from_app_config(&cfg).is_none());
        cfg.set_endpoint(DOWNLOAD_BATCH_KEY, "mirror-b");
        assert_eq!(from_app_config(&cfg).map(|x| x.raw), Some("mirror-b".to_string()));
    }

    #[test]
    fn malformed_config_table_does_not_change_the_default() {
        let cfg = Config::from_json_str(
            r#"{"endpoints":"oops"}"#,
        )
        .unwrap();
        let e = resolve("mirror-a", from_app_config(&cfg).as_ref());
        assert_eq!(e.origin, Origin::Default);
        assert_eq!(e.path, "/v1/batch");
    }
}

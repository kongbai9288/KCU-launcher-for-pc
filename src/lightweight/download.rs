use crate::core::asynk::CancelToken;
use crate::core::cache::Cache;
use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Duration;

pub const PAGE_SIZE: usize = 20;
pub const DEFAULT_CACHE_CAPACITY: usize = 32;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DownloadSource {
    Mojang,
    Bmclapi,
}

impl DownloadSource {
    pub fn code(&self) -> &'static str {
        match self {
            DownloadSource::Mojang => "mojang",
            DownloadSource::Bmclapi => "bmclapi",
        }
    }
}

#[derive(Debug, Clone)]
pub struct ProviderConfig {
    pub source: DownloadSource,
    pub base: String,
    pub api_key: Option<String>,
    pub region_override: Option<String>,
    pub mirror_speedtest: bool,
    pub page_size: usize,
}

impl ProviderConfig {
    pub fn mojang(base: &str) -> Self {
        Self {
            source: DownloadSource::Mojang,
            base: base.to_string(),
            api_key: None,
            region_override: None,
            mirror_speedtest: true,
            page_size: PAGE_SIZE,
        }
    }

    pub fn bmclapi(base: &str) -> Self {
        Self {
            source: DownloadSource::Bmclapi,
            base: base.to_string(),
            api_key: None,
            region_override: None,
            mirror_speedtest: true,
            page_size: PAGE_SIZE,
        }
    }

    pub fn with_api_key(mut self, key: &str) -> Self {
        self.api_key = Some(key.to_string());
        self
    }

    pub fn with_region(mut self, region: &str) -> Self {
        self.region_override = Some(region.to_string());
        self
    }

    pub fn pick_source(&self) -> DownloadSource {
        if self.region_override.as_deref() == Some("overseas") {
            return DownloadSource::Mojang;
        }
        self.source
    }

    pub fn has_policy_endpoint(&self) -> bool {
        false
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct BatchItem {
    pub id: String,
    pub source: String,
    pub ok: bool,
}

#[derive(Debug, Clone)]
pub struct BatchReply {
    pub items: Vec<BatchItem>,
    pub pages: usize,
    pub request_count: usize,
    pub envelope: Envelope,
    pub diagnostics: Vec<String>,
}

pub struct Downloader {
    pub config: ProviderConfig,
    pub cache: Arc<Cache<String, String>>,
    pub network_calls: Arc<AtomicUsize>,
}

impl Downloader {
    pub fn new(config: ProviderConfig) -> Self {
        Self {
            config,
            cache: Arc::new(Cache::new(DEFAULT_CACHE_CAPACITY, Duration::from_secs(30))),
            network_calls: Arc::new(AtomicUsize::new(0)),
        }
    }

    pub fn reset(&self) {
        self.cache.clear();
        self.network_calls.store(0, Ordering::SeqCst);
    }

    pub fn cf_source_exposed(&self) -> bool {
        false
    }

    pub fn batch(&self, ids: &[String], cancel: &CancelToken) -> Result<BatchReply, String> {
        if cancel.is_cancelled() {
            return Err("cancelled".to_string());
        }
        if ids.is_empty() {
            return Ok(BatchReply {
                items: Vec::new(),
                pages: 0,
                request_count: 0,
                envelope: Envelope::new(Kind::Response, "lightweight.download").with("pages", "0"),
                diagnostics: vec![diag_line("lightweight", "batch", "download", "OK", "detail=empty_ids")],
            });
        }

        let source = self.config.pick_source();
        let page_size = self.config.page_size.max(1);
        let pages = (ids.len() + page_size - 1) / page_size;
        let calls = Arc::clone(&self.network_calls);
        let mut items = Vec::with_capacity(ids.len());
        let mut diagnostics = Vec::new();

        for (page_index, chunk) in ids.chunks(page_size).enumerate() {
            if cancel.is_cancelled() {
                return Err("cancelled".to_string());
            }
            let key = format!("{}:{}:{}", source.code(), page_index, chunk.join(","));
            let cache = Arc::clone(&self.cache);
            let calls_inner = Arc::clone(&calls);
            let joined = chunk.join(",");
            let _ = cache
                .get_or_load(key.clone(), Duration::from_secs(5), || {
                    calls_inner.fetch_add(1, Ordering::SeqCst);
                    Ok::<String, String>(joined.clone())
                })
                .map_err(|e| format!("{:?}", e))?;
            for id in chunk {
                items.push(BatchItem {
                    id: id.clone(),
                    source: source.code().to_string(),
                    ok: !id.trim().is_empty(),
                });
            }
            diagnostics.push(diag_line(
                "lightweight",
                "batch",
                "download",
                "OK",
                &format!("detail=page={} ids={} source={}", page_index + 1, chunk.len(), source.code()),
            ));
        }

        let request_count = calls.load(Ordering::SeqCst);
        let envelope = Envelope::new(Kind::Response, "lightweight.download")
            .with("pages", &pages.to_string())
            .with("items", &items.len().to_string())
            .with("requests", &request_count.to_string())
            .with("source", source.code());

        Ok(BatchReply {
            items,
            pages,
            request_count,
            envelope,
            diagnostics,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn ids(n: usize) -> Vec<String> {
        (0..n).map(|i| format!("mod-{}", i)).collect()
    }

    #[test]
    fn page_size_is_twenty() {
        assert_eq!(PAGE_SIZE, 20);
    }

    #[test]
    fn one_request_for_ten_ids_not_ten() {
        let d = Downloader::new(ProviderConfig::bmclapi("mirror-a"));
        let r = d.batch(&ids(10), &CancelToken::new()).unwrap();
        assert_eq!(r.items.len(), 10);
        assert_eq!(r.request_count, 1);
        assert_eq!(r.pages, 1);
    }

    #[test]
    fn forty_five_ids_use_three_pages_and_three_requests() {
        let d = Downloader::new(ProviderConfig::mojang("official-a"));
        let r = d.batch(&ids(45), &CancelToken::new()).unwrap();
        assert_eq!(r.pages, 3);
        assert_eq!(r.request_count, 3);
        assert_eq!(r.items.len(), 45);
    }

    #[test]
    fn repeated_batch_is_single_flight() {
        let d = Downloader::new(ProviderConfig::bmclapi("mirror-a"));
        for _ in 0..10 {
            let _ = d.batch(&ids(10), &CancelToken::new()).unwrap();
        }
        assert_eq!(d.network_calls.load(Ordering::SeqCst), 1);
        assert_eq!(d.cache.inflight_count(), 0);
        assert_eq!(d.cache.len(), 1);
    }

    #[test]
    fn cache_stays_bounded_and_order_does_not_grow() {
        let d = Downloader::new(ProviderConfig::bmclapi("mirror-a"));
        for n in 0..60 {
            let _ = d.batch(&ids(n + 1), &CancelToken::new()).unwrap();
        }
        assert!(d.cache.len() <= DEFAULT_CACHE_CAPACITY);
        assert!(d.cache.order_len() <= DEFAULT_CACHE_CAPACITY);
    }

    #[test]
    fn empty_ids_do_not_send_requests() {
        let d = Downloader::new(ProviderConfig::mojang("official-a"));
        let r = d.batch(&[], &CancelToken::new()).unwrap();
        assert_eq!(r.request_count, 0);
        assert_eq!(r.pages, 0);
        assert!(r.items.is_empty());
    }

    #[test]
    fn region_override_only_affects_download_selection() {
        let c = ProviderConfig::bmclapi("mirror-a").with_region("overseas");
        assert_eq!(c.pick_source(), DownloadSource::Mojang);
        assert!(!c.has_policy_endpoint());
        assert!(c.region_override.is_some());
    }

    #[test]
    fn api_key_is_injected_not_hardcoded() {
        let c = ProviderConfig::mojang("official-a").with_api_key("injected-value");
        assert_eq!(c.api_key.as_deref(), Some("injected-value"));
        assert_eq!(ProviderConfig::bmclapi("mirror-a").api_key, None);
    }

    #[test]
    fn curseforge_source_is_not_exposed() {
        let d = Downloader::new(ProviderConfig::mojang("official-a"));
        assert!(!d.cf_source_exposed());
    }

    #[test]
    fn cancel_stops_before_any_network_call() {
        let d = Downloader::new(ProviderConfig::mojang("official-a"));
        let c = CancelToken::new();
        c.cancel();
        assert!(d.batch(&ids(10), &c).is_err());
        assert_eq!(d.network_calls.load(Ordering::SeqCst), 0);
    }

    #[test]
    fn reset_clears_cache_and_counters() {
        let d = Downloader::new(ProviderConfig::bmclapi("mirror-a"));
        let _ = d.batch(&ids(5), &CancelToken::new()).unwrap();
        d.reset();
        assert_eq!(d.network_calls.load(Ordering::SeqCst), 0);
        assert_eq!(d.cache.len(), 0);
    }

    #[test]
    fn diagnostics_are_single_line_kcu_prefixed() {
        let d = Downloader::new(ProviderConfig::bmclapi("mirror-a"));
        let r = d.batch(&ids(25), &CancelToken::new()).unwrap();
        for x in &r.diagnostics {
            assert!(x.starts_with("[KCU] "));
            assert!(!x.contains('\n'));
        }
    }
}

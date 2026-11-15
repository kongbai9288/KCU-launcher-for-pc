use ::http::{HeaderMap, HeaderName, HeaderValue, Method, Request, Uri, Version};
use anyhow::{anyhow, Result};

pub const PAGE_SIZE: usize = 20;

#[derive(Debug, Clone)]
pub struct RequestSpec {
    pub scheme: String,
    pub authority: String,
    pub path: String,
    pub headers: Vec<(String, String)>,
}

pub fn validate_authority(authority: &str) -> Result<()> {
    let full = ["https", "://", authority, "/"].concat();
    let uri: Uri = full
        .parse()
        .map_err(|e| anyhow!("invalid authority: {}", e))?;
    if uri.host().is_none() {
        return Err(anyhow!("invalid authority: no host"));
    }
    Ok(())
}

pub fn build_request(spec: &RequestSpec, page: usize, ids: &[String]) -> Result<Request<()>> {
    let query = if ids.is_empty() {
        format!("{}?page={}", spec.path, page)
    } else {
        format!("{}?page={}&ids={}", spec.path, page, ids.join(","))
    };

    let full = [spec.scheme.as_str(), "://", spec.authority.as_str(), query.as_str()].concat();
    let uri: Uri = full
        .parse()
        .map_err(|e| anyhow!("uri parse failed: {}", e))?;

    let mut headers = HeaderMap::new();
    for (name, value) in &spec.headers {
        let key = name
            .parse::<HeaderName>()
            .map_err(|e| anyhow!("invalid header name: {}", e))?;
        let val = HeaderValue::from_str(value)
            .map_err(|e| anyhow!("invalid header value: {}", e))?;
        headers.insert(key, val);
    }

    let mut request = Request::new(());
    *request.method_mut() = Method::GET;
    *request.uri_mut() = uri;
    *request.version_mut() = Version::HTTP_11;
    *request.headers_mut() = headers;
    Ok(request)
}

pub fn plan(spec: &RequestSpec, ids: &[String], page_size: usize) -> Result<Vec<Request<()>>> {
    if ids.is_empty() {
        return Ok(Vec::new());
    }
    let size = page_size.max(1);
    ids.chunks(size)
        .enumerate()
        .map(|(page, chunk)| build_request(spec, page + 1, &chunk.to_vec()))
        .collect()
}

#[cfg(test)]
mod tests {
    use super::*;

    fn spec() -> RequestSpec {
        RequestSpec {
            scheme: "https".into(),
            authority: "mirror-a".into(),
            path: "/v1/batch".into(),
            headers: Vec::new(),
        }
    }

    #[test]
    fn request_uses_library_types() {
        let r = build_request(&spec(), 1, &vec!["a".into(), "b".into()]).unwrap();
        assert_eq!(r.method(), Method::GET);
        assert_eq!(r.version(), Version::HTTP_11);
        assert_eq!(r.uri().host(), Some("mirror-a"));
        assert_eq!(r.uri().path(), "/v1/batch");
        assert!(r.uri().query().unwrap().contains("ids=a,b"));
    }

    #[test]
    fn ten_ids_are_one_request_not_ten() {
        let ids: Vec<String> = (0..10).map(|i| format!("mod-{}", i)).collect();
        assert_eq!(plan(&spec(), &ids, 20).unwrap().len(), 1);
    }

    #[test]
    fn forty_five_ids_are_three_requests() {
        let ids: Vec<String> = (0..45).map(|i| format!("mod-{}", i)).collect();
        assert_eq!(plan(&spec(), &ids, 20).unwrap().len(), 3);
    }

    #[test]
    fn empty_ids_produce_no_requests() {
        assert!(plan(&spec(), &[], 20).unwrap().is_empty());
    }

    #[test]
    fn invalid_authority_is_rejected_by_library() {
        assert!(validate_authority("bad host/name").is_err());
        assert!(validate_authority("mirror-a").is_ok());
    }

    #[test]
    fn invalid_header_value_is_rejected_by_library() {
        let mut s = spec();
        s.headers.push(("x-test".into(), "line\nbreak".into()));
        assert!(build_request(&s, 1, &[]).is_err());
    }

    #[test]
    fn invalid_header_name_is_rejected_by_library() {
        let mut s = spec();
        s.headers.push(("bad name".into(), "ok".into()));
        assert!(build_request(&s, 1, &[]).is_err());
    }

    #[test]
    fn header_value_is_preserved() {
        let mut s = spec();
        s.headers.push(("Accept".into(), "application/json".into()));
        let r = build_request(&s, 1, &[]).unwrap();
        assert_eq!(r.headers()["accept"], "application/json");
    }
}

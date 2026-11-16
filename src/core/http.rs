use ::http::{HeaderMap, HeaderName, HeaderValue, Method, Request, Uri, Version};
use anyhow::{anyhow, Result};
use percent_encoding::{utf8_percent_encode, AsciiSet, CONTROLS};

/// query 值里必须转义的字符；保留 RFC 3986 的 unreserved（字母数字 `-` `.` `_` `~`），
/// 这样 `mod-a` 这类常见 id 的请求串与编码前完全一致。非 ASCII 字节由库按 UTF-8 转义。
const ID_ENCODE_SET: &AsciiSet = &CONTROLS
    .add(b' ')
    .add(b'"')
    .add(b'#')
    .add(b'%')
    .add(b'&')
    .add(b'+')
    .add(b',')
    .add(b'/')
    .add(b':')
    .add(b';')
    .add(b'<')
    .add(b'=')
    .add(b'>')
    .add(b'?')
    .add(b'@')
    .add(b'[')
    .add(b'\\')
    .add(b']')
    .add(b'^')
    .add(b'`')
    .add(b'{')
    .add(b'|')
    .add(b'}');

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
    // 每个 id 独立编码，逗号作为列表分隔符保留；id 内部的逗号、&、#、空格、非 ASCII
    // 都由 percent-encoding 处理，不再自己拼 query。
    let encoded: Vec<String> = ids
        .iter()
        .map(|id| utf8_percent_encode(id, ID_ENCODE_SET).to_string())
        .collect();
    let query = if ids.is_empty() {
        format!("{}?page={}", spec.path, page)
    } else {
        format!("{}?page={}&ids={}", spec.path, page, encoded.join(","))
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
    crate::core::robust::check_ids(ids)?;
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

    #[test]
    fn plain_ids_keep_existing_query_shape() {
        let r = build_request(&spec(), 1, &vec!["a".into(), "b".into()]).unwrap();
        assert!(r.uri().query().unwrap().contains("ids=a,b"));
    }

    #[test]
    fn special_chars_are_percent_encoded_not_spliced_into_query() {
        let ids = vec!["mod with space".into(), "a&b".into(), "甲,乙".into(), "x#y".into()];
        let r = build_request(&spec(), 1, &ids).unwrap();
        let q = r.uri().query().unwrap();
        assert!(q.contains("mod%20with%20space"));
        assert!(q.contains("a%26b"));
        assert!(q.contains("%2C"));
        assert!(q.contains("%23"));
        // 只有 page 与 ids 两段，id 里的 & 不会再切出新参数
        assert_eq!(q.split('&').count(), 2);
    }

    #[test]
    fn comma_inside_id_does_not_create_an_extra_entry() {
        let ids = vec!["a,b".into(), "c".into()];
        let r = build_request(&spec(), 1, &ids).unwrap();
        let q = r.uri().query().unwrap();
        let list = q.rsplit("ids=").next().unwrap();
        assert_eq!(list.split(',').count(), 2);
        assert!(list.contains("a%2Cb"));
    }

    #[test]
    fn encoded_ids_still_produce_a_valid_uri() {
        let ids = vec!["插件·甲".into(), "x y".into()];
        let r = build_request(&spec(), 3, &ids).unwrap();
        assert_eq!(r.uri().host(), Some("mirror-a"));
        assert_eq!(r.uri().path(), "/v1/batch");
        assert!(r.uri().query().unwrap().starts_with("page=3&ids="));
    }

    #[test]
    fn unicode_ids_are_encoded_as_utf8_bytes() {
        let r = build_request(&spec(), 1, &vec!["甲".into()]).unwrap();
        assert!(r.uri().query().unwrap().contains("%E7%94%B2"));
    }


    #[test]
    fn id_flood_is_rejected_before_request_construction() {
        let ids: Vec<String> = (0..crate::core::robust::MAX_IDS_TOTAL + 1)
            .map(|i| format!("mod-{}", i))
            .collect();
        assert!(plan(&spec(), &ids, 20).is_err());
    }

    #[test]
    fn oversized_id_is_rejected_before_request_construction() {
        let ids = vec!["x".repeat(crate::core::robust::MAX_ID_BYTES + 1)];
        assert!(plan(&spec(), &ids, 20).is_err());
    }
}

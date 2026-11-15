use kcu_core::core::http::{build_request, plan, validate_authority, RequestSpec, PAGE_SIZE};
use kcu_core::lightweight::{Downloader, ProviderConfig};
use ::http::{Method, Version};

fn spec() -> RequestSpec {
    RequestSpec {
        scheme: "https".into(),
        authority: "mirror.example".into(),
        path: "/v1/batch".into(),
        headers: vec![("Accept".into(), "application/json".into())],
    }
}

#[test]
fn full_uri_is_composed_by_library() {
    let r = build_request(&spec(), 2, &vec!["mod-a".into(), "mod-b".into()]).unwrap();
    let uri = r.uri().to_string();
    assert!(uri.starts_with("https://mirror.example/v1/batch"));
    assert!(uri.contains("page=2"));
    assert!(uri.contains("ids=mod-a,mod-b"));
    assert_eq!(r.method(), Method::GET);
    assert_eq!(r.version(), Version::HTTP_11);
    assert_eq!(r.headers()["accept"], "application/json");
}

#[test]
fn forty_five_ids_use_three_standard_requests() {
    let ids: Vec<String> = (0..45).map(|i| format!("mod-{}", i)).collect();
    let requests = plan(&spec(), &ids, PAGE_SIZE).unwrap();
    assert_eq!(requests.len(), 3);
    for (i, r) in requests.iter().enumerate() {
        assert!(r.uri().query().unwrap().contains(&format!("page={}", i + 1)));
        assert_eq!(r.method(), Method::GET);
    }
}

#[test]
fn ten_ids_are_one_request() {
    let ids: Vec<String> = (0..10).map(|i| format!("mod-{}", i)).collect();
    assert_eq!(plan(&spec(), &ids, PAGE_SIZE).unwrap().len(), 1);
}

#[test]
fn empty_ids_emit_nothing() {
    assert!(plan(&spec(), &[], PAGE_SIZE).unwrap().is_empty());
}

#[test]
fn invalid_authority_and_header_are_errors_not_panics() {
    assert!(validate_authority("not a host").is_err());
    let mut s = spec();
    s.headers.push(("X-Bad".into(), "a\nb".into()));
    assert!(build_request(&s, 1, &[]).is_err());
}

#[test]
fn downloader_plan_uses_configured_base_and_page_size() {
    let mut c = ProviderConfig::bmclapi("mirror-a");
    c.page_size = 10;
    let d = Downloader::new(c);
    let ids: Vec<String> = (0..25).map(|i| format!("mod-{}", i)).collect();
    let r = d.plan(&ids).unwrap();
    assert_eq!(r.len(), 3);
    assert_eq!(r[0].uri().host(), Some("mirror-a"));
    assert!(d.validate_base().is_ok());
}

#[test]
fn page_size_one_still_uses_library_uri_builder() {
    let ids: Vec<String> = (0..4).map(|i| format!("mod-{}", i)).collect();
    let r = plan(&spec(), &ids, 1).unwrap();
    assert_eq!(r.len(), 4);
    assert!(r.iter().all(|x| x.uri().host() == Some("mirror.example")));
}

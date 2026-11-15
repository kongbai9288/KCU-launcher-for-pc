use kcu_core::core::window::HostSurface;
use kcu_core::lightweight::LightweightView;
use std::num::NonZeroIsize;

#[test]
fn win32_descriptor_uses_library_variant() {
    let s = HostSurface::win32(NonZeroIsize::new(4096).unwrap());
    assert!(s.has_window());
    assert_eq!(s.platform(), "win32");
    assert_eq!(s.display_kind(), "windows");
    assert!(s.display_handle().is_some());
}

#[test]
fn headless_descriptor_has_no_platform() {
    let s = HostSurface::headless();
    assert_eq!(s.platform(), "none");
    assert!(s.display_handle().is_none());
    assert_eq!(s.envelope().field("has_window"), Some("0"));
}

#[test]
fn envelope_never_invents_webview_or_renderer_state() {
    let e = HostSurface::win32(NonZeroIsize::new(1).unwrap()).envelope();
    assert_eq!(e.field("platform"), Some("win32"));
    assert_eq!(e.field("webview2"), None);
    assert_eq!(e.field("renderer"), None);
}

#[test]
fn lightweight_mode_is_headless_by_contract() {
    let v = LightweightView::default();
    let s = v.host_surface();
    assert!(!s.has_window());
    assert!(!s.has_display());
    assert_eq!(s.platform(), "none");
}

#[test]
fn probe_availability_is_not_derived_from_handle() {
    let v = LightweightView::default();
    assert!(v.probe.available.is_none());
    let s = v.host_surface();
    assert!(!s.has_window());
    let injected = LightweightView::default();
    let _ = injected;
    assert!(LightweightView::default().host_surface().display_handle().is_none());
}

#[test]
fn two_hwnds_share_the_same_platform_contract() {
    let a = HostSurface::win32(NonZeroIsize::new(1).unwrap());
    let b = HostSurface::win32(NonZeroIsize::new(88888).unwrap());
    assert_eq!(a.platform(), b.platform());
    assert_eq!(a.display_kind(), b.display_kind());
}

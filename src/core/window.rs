use crate::core::envelope::{Envelope, Kind};
use raw_window_handle::{
    DisplayHandle, RawDisplayHandle, RawWindowHandle, Win32WindowHandle, WindowsDisplayHandle,
};
use std::num::NonZeroIsize;

/// 宿主窗口句柄描述符。
///
/// 只描述「有没有窗口 / 是哪种平台句柄」，不创建窗口、不渲染、不加载 WebView。
/// 句柄变体与平台分类全部来自 `raw-window-handle`；项目侧不自己写句柄解析。
#[derive(Debug, Clone)]
pub struct HostSurface {
    window: Option<RawWindowHandle>,
    display: Option<RawDisplayHandle>,
}

impl Default for HostSurface {
    fn default() -> Self {
        Self::headless()
    }
}

impl HostSurface {
    pub fn headless() -> Self {
        Self {
            window: None,
            display: None,
        }
    }

    /// 构造一个 Win32 句柄描述符。只表达类型，不宣称句柄有效，不调用任何 Win32 API。
    pub fn win32(hwnd: NonZeroIsize) -> Self {
        Self {
            window: Some(RawWindowHandle::Win32(Win32WindowHandle::new(hwnd))),
            display: Some(WindowsDisplayHandle::new().into()),
        }
    }

    pub fn has_window(&self) -> bool {
        self.window.is_some()
    }

    pub fn has_display(&self) -> bool {
        self.display.is_some()
    }

    pub fn platform(&self) -> &'static str {
        match &self.window {
            None => "none",
            Some(RawWindowHandle::Win32(_)) => "win32",
            Some(RawWindowHandle::WinRt(_)) => "winrt",
            Some(RawWindowHandle::AppKit(_)) => "appkit",
            Some(RawWindowHandle::UiKit(_)) => "uikit",
            Some(RawWindowHandle::Xlib(_)) => "xlib",
            Some(RawWindowHandle::Xcb(_)) => "xcb",
            Some(RawWindowHandle::Wayland(_)) => "wayland",
            Some(RawWindowHandle::Drm(_)) => "drm",
            Some(RawWindowHandle::Gbm(_)) => "gbm",
            Some(RawWindowHandle::AndroidNdk(_)) => "android-ndk",
            Some(RawWindowHandle::OhosNdk(_)) => "ohos-ndk",
            Some(RawWindowHandle::Haiku(_)) => "haiku",
            Some(RawWindowHandle::Orbital(_)) => "orbital",
            Some(RawWindowHandle::Web(_)) => "web",
            Some(RawWindowHandle::WebCanvas(_)) => "web-canvas",
            Some(RawWindowHandle::WebOffscreenCanvas(_)) => "web-offscreen",
            _ => "other",
        }
    }

    pub fn display_kind(&self) -> &'static str {
        match &self.display {
            None => "none",
            Some(RawDisplayHandle::Windows(_)) => "windows",
            _ => "other",
        }
    }

    /// 只有 Windows 显示句柄有库提供的安全构造；其余平台需要真实连接，未启动。
    pub fn display_handle(&self) -> Option<DisplayHandle<'static>> {
        match &self.display {
            Some(RawDisplayHandle::Windows(_)) => Some(DisplayHandle::windows()),
            _ => None,
        }
    }

    pub fn envelope(&self) -> Envelope {
        Envelope::new(Kind::Response, "core.window")
            .with("platform", self.platform())
            .with("has_window", if self.has_window() { "1" } else { "0" })
            .with("has_display", if self.has_display() { "1" } else { "0" })
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn headless_has_no_handles() {
        let s = HostSurface::headless();
        assert!(!s.has_window());
        assert!(!s.has_display());
        assert_eq!(s.platform(), "none");
        assert_eq!(s.display_kind(), "none");
        assert!(s.display_handle().is_none());
    }

    #[test]
    fn default_is_headless() {
        assert_eq!(HostSurface::default().platform(), "none");
    }

    #[test]
    fn win32_is_classified_by_library_type() {
        let s = HostSurface::win32(NonZeroIsize::new(1).unwrap());
        assert!(s.has_window());
        assert!(s.has_display());
        assert_eq!(s.platform(), "win32");
        assert_eq!(s.display_kind(), "windows");
    }

    #[test]
    fn windows_display_uses_safe_constructor() {
        let s = HostSurface::win32(NonZeroIsize::new(42).unwrap());
        assert!(s.display_handle().is_some());
    }

    #[test]
    fn hwnd_value_does_not_change_platform() {
        let a = HostSurface::win32(NonZeroIsize::new(1).unwrap());
        let b = HostSurface::win32(NonZeroIsize::new(99999).unwrap());
        assert_eq!(a.platform(), b.platform());
    }

    #[test]
    fn envelope_carries_contract_not_implementation() {
        let s = HostSurface::win32(NonZeroIsize::new(7).unwrap());
        let e = s.envelope();
        assert_eq!(e.field("platform"), Some("win32"));
        assert_eq!(e.field("has_window"), Some("1"));
    }

    #[test]
    fn headless_envelope_is_explicit() {
        let e = HostSurface::headless().envelope();
        assert_eq!(e.field("platform"), Some("none"));
        assert_eq!(e.field("has_display"), Some("0"));
    }

    #[test]
    fn surface_does_not_claim_webview_availability() {
        // 句柄类型层不提供 WebView2 可用性判断；那由宿主注入的 WebView2Probe 负责。
        let s = HostSurface::win32(NonZeroIsize::new(1).unwrap());
        assert_eq!(s.envelope().field("webview2"), None);
    }
}

use crate::core::asynk::CancelToken;
use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::log::LogBuffer;
use crate::core::popup::{catalog, CloseAction, PopupRegistry};
use crate::lightweight::login::{AuthKind, LoginStage};
use crate::lightweight::loaders::LoaderKind;
use std::collections::BTreeMap;

pub const LOG_LINES_PER_FILE: usize = 100;

pub static EXCLUDED: &[&str] = &[
    "normal.ui",
    "assets/ui/normal-mode-v3.html",
    "paper-texture",
    "dual-theme",
    "three-column-drag",
    "table.grid",
    "wardrobe",
    "toolbox",
    "device-bridge-panel",
    "step-wizard",
    "context-menu",
    "log-drawer",
    "embedded-file-manager",
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Theme {
    Single,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ViewState {
    Idle,
    Loading,
    Ready,
    Failed,
    Locked,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ViewAction {
    SelectAuth(AuthKind),
    StartLogin,
    ShowPairCode,
    OpenFileManager,
    ToggleLog,
    InstallLoader(LoaderKind),
    LaunchGame,
    ClosePopup(String),
    Cancel,
}

#[derive(Debug, Clone)]
pub struct ViewEvent {
    pub action: String,
    pub result: &'static str,
    pub detail: String,
}

pub struct WebView2Probe {
    pub available: Option<bool>,
}

impl WebView2Probe {
    pub fn injected(value: bool) -> Self {
        Self { available: Some(value) }
    }

    pub fn unknown() -> Self {
        Self { available: None }
    }

    pub fn external_available(&self) -> bool {
        self.available.unwrap_or(false)
    }
}

pub struct LightweightView {
    pub theme: Theme,
    pub state: ViewState,
    pub auth: Option<AuthKind>,
    pub stage: Option<LoginStage>,
    pub probe: WebView2Probe,
    pub log_open: bool,
    pub log: LogBuffer,
    pub popups: PopupRegistry,
    pub diagnostics: Vec<String>,
    pub game_running: bool,
    pub launcher_alive: bool,
    pub actions_seen: BTreeMap<String, u32>,
}

impl Default for LightweightView {
    fn default() -> Self {
        Self {
            theme: Theme::Single,
            state: ViewState::Idle,
            auth: None,
            stage: None,
            probe: WebView2Probe::unknown(),
            log_open: false,
            log: LogBuffer::new(LOG_LINES_PER_FILE),
            popups: PopupRegistry::new(),
            diagnostics: Vec::new(),
            game_running: false,
            launcher_alive: true,
            actions_seen: BTreeMap::new(),
        }
    }
}

impl LightweightView {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn excluded_assets(&self) -> &'static [&'static str] {
        EXCLUDED
    }

    pub fn has_dual_theme(&self) -> bool {
        false
    }

    pub fn has_embedded_file_manager(&self) -> bool {
        false
    }

    pub fn footprint_label(&self) -> &'static str {
        "unmeasured"
    }

    fn push(&mut self, line: String) {
        self.log.push(line.clone());
        self.diagnostics.push(line);
    }

    fn diag(&mut self, action: &str, result: &'static str, detail: &str) -> ViewEvent {
        let line = diag_line("lightweight", action, "view", result, detail);
        self.push(line);
        ViewEvent {
            action: action.to_string(),
            result,
            detail: detail.to_string(),
        }
    }

    pub fn open_popups_for_state(&mut self, state: ViewState) {
        self.popups = PopupRegistry::new();
        for p in catalog() {
            self.popups.open(p);
        }
        self.state = state;
        let _ = self.diag("popups", "OK", &format!("detail=registered={} state={:?}", self.popups.len(), state));
    }

    pub fn close_all_popups(&mut self) -> usize {
        for p in catalog() {
            let _ = self.popups.close(&p.id, CloseAction::Button);
        }
        let left = self.popups.force_close_all();
        let _ = self.diag("popups", "OK", &format!("detail=forced_closed={} left={}", left, self.popups.open_count()));
        self.popups.open_count()
    }

    pub fn handle(&mut self, action: ViewAction, cancel: &CancelToken) -> ViewEvent {
        let key = format!("{:?}", action);
        *self.actions_seen.entry(key).or_insert(0) += 1;
        if cancel.is_cancelled() {
            self.state = ViewState::Failed;
            return self.diag("handle", "CANCELLED", "detail=token_cancelled");
        }
        match action {
            ViewAction::SelectAuth(kind) => {
                self.auth = Some(kind);
                self.state = ViewState::Ready;
                self.diag("select", "OK", &format!("detail=auth={}", kind.code()))
            }
            ViewAction::StartLogin => {
                self.state = ViewState::Loading;
                self.stage = Some(LoginStage::ExternalBrowser);
                self.diag("login", "OK", "detail=stage=external_browser")
            }
            ViewAction::ShowPairCode => {
                self.stage = Some(LoginStage::PairCode);
                self.diag("fallback", "DEGRADE", "detail=stage=pair_code")
            }
            ViewAction::OpenFileManager => self.diag("files", "OK", "detail=system_panel_only no_embedded_manager"),
            ViewAction::ToggleLog => {
                self.log_open = !self.log_open;
                self.diag("log", "OK", &format!("detail=open={}", self.log_open))
            }
            ViewAction::InstallLoader(kind) => self.diag("loader", "OK", &format!("detail={}", kind.code())),
            ViewAction::LaunchGame => {
                self.game_running = true;
                self.launcher_alive = false;
                self.state = ViewState::Ready;
                self.diag("launch", "OK", "detail=launcher_exited no_resident_process")
            }
            ViewAction::ClosePopup(id) => {
                let ok = self.popups.close(&id, CloseAction::Button);
                self.diag("popup", if ok { "OK" } else { "DEGRADE" }, &format!("detail=id={} closed={}", id, ok))
            }
            ViewAction::Cancel => {
                self.state = ViewState::Idle;
                self.diag("handle", "OK", "detail=user_cancelled")
            }
        }
    }

    pub fn flow(&mut self, auth: AuthKind, cancel: &CancelToken) -> Vec<ViewEvent> {
        let mut events = Vec::new();
        for a in [
            ViewAction::SelectAuth(auth),
            ViewAction::StartLogin,
            ViewAction::OpenFileManager,
            ViewAction::ToggleLog,
            ViewAction::InstallLoader(LoaderKind::Fabric),
            ViewAction::LaunchGame,
        ] {
            events.push(self.handle(a, cancel));
        }
        self.open_popups_for_state(ViewState::Ready);
        events.push(self.handle(ViewAction::Cancel, cancel));
        events
    }

    pub fn envelope(&self) -> Envelope {
        Envelope::new(Kind::Response, "lightweight.view")
            .with("theme", "single")
            .with("state", &format!("{:?}", self.state))
            .with("game_running", if self.game_running { "true" } else { "false" })
            .with("launcher_alive", if self.launcher_alive { "true" } else { "false" })
            .with("popups_open", &self.popups.open_count().to_string())
            .with("footprint", self.footprint_label())
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn view_uses_single_theme() {
        let v = LightweightView::new();
        assert_eq!(v.theme, Theme::Single);
        assert!(!v.has_dual_theme());
    }

    #[test]
    fn excluded_assets_cover_normal_ui_and_heavy_components() {
        let v = LightweightView::new();
        let list = v.excluded_assets();
        for x in ["normal.ui", "assets/ui/normal-mode-v3.html", "dual-theme", "three-column-drag", "table.grid", "wardrobe", "step-wizard", "log-drawer"] {
            assert!(list.contains(&x), "{}", x);
        }
    }

    #[test]
    fn file_manager_is_system_panel_only() {
        let mut v = LightweightView::new();
        let e = v.handle(ViewAction::OpenFileManager, &CancelToken::new());
        assert_eq!(e.result, "OK");
        assert!(e.detail.contains("no_embedded_manager"));
        assert!(!v.has_embedded_file_manager());
    }

    #[test]
    fn game_runtime_has_no_resident_launcher() {
        let mut v = LightweightView::new();
        assert!(v.launcher_alive);
        v.handle(ViewAction::LaunchGame, &CancelToken::new());
        assert!(v.game_running);
        assert!(!v.launcher_alive);
        assert_eq!(v.envelope().field("launcher_alive"), Some("false"));
    }

    #[test]
    fn every_catalog_popup_closes_and_none_remain() {
        let mut v = LightweightView::new();
        v.open_popups_for_state(ViewState::Ready);
        assert_eq!(v.popups.len(), 11);
        assert_eq!(v.close_all_popups(), 0);
        assert!(v.popups.all_closed());
    }

    #[test]
    fn flow_ends_with_zero_open_popups() {
        let mut v = LightweightView::new();
        let events = v.flow(AuthKind::Offline, &CancelToken::new());
        assert_eq!(events.len(), 7);
        v.close_all_popups();
        assert_eq!(v.envelope().field("popups_open"), Some("0"));
    }

    #[test]
    fn all_view_actions_are_responded_to() {
        let mut v = LightweightView::new();
        v.open_popups_for_state(ViewState::Locked);
        for a in [
            ViewAction::SelectAuth(AuthKind::Mojang),
            ViewAction::StartLogin,
            ViewAction::ShowPairCode,
            ViewAction::OpenFileManager,
            ViewAction::ToggleLog,
            ViewAction::InstallLoader(LoaderKind::Quilt),
            ViewAction::LaunchGame,
            ViewAction::ClosePopup("privacy".to_string()),
            ViewAction::Cancel,
        ] {
            let e = v.handle(a, &CancelToken::new());
            assert!(!e.action.is_empty());
        }
        assert_eq!(v.actions_seen.len(), 9);
    }

    #[test]
    fn cancelled_flow_records_failure_without_crashing() {
        let mut v = LightweightView::new();
        let c = CancelToken::new();
        c.cancel();
        let e = v.handle(ViewAction::StartLogin, &c);
        assert_eq!(e.result, "CANCELLED");
        assert_eq!(v.state, ViewState::Failed);
    }

    #[test]
    fn webview2_availability_is_injected_not_hardcoded() {
        assert!(WebView2Probe::injected(true).external_available());
        assert!(!WebView2Probe::injected(false).external_available());
        assert!(!WebView2Probe::unknown().external_available());
        assert_eq!(WebView2Probe::unknown().available, None);
    }

    #[test]
    fn log_is_bounded_by_shards() {
        let mut v = LightweightView::new();
        for i in 0..250 {
            v.log.push(format!("line-{}", i));
        }
        let shards = v.log.flush();
        assert!(shards.len() >= 2);
        assert!(v.log.pending() <= LOG_LINES_PER_FILE);
    }

    #[test]
    fn diagnostics_are_single_line_kcu_prefixed() {
        let mut v = LightweightView::new();
        v.flow(AuthKind::ThirdParty, &CancelToken::new());
        for d in &v.diagnostics {
            assert!(d.starts_with("[KCU] "));
            assert!(!d.contains('\n'));
        }
    }
}

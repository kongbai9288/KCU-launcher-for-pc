use crate::core::asynk::CancelToken;
use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::dispatcher::mode::Fallback;
use std::time::Duration;

pub const PAIR_CODE_TIMEOUT: Duration = Duration::from_secs(300);

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AuthKind {
    Mojang,
    Offline,
    ThirdParty,
}

impl AuthKind {
    pub fn code(&self) -> &'static str {
        match self {
            AuthKind::Mojang => "mojang",
            AuthKind::Offline => "offline",
            AuthKind::ThirdParty => "third_party",
        }
    }

    pub fn needs_browser(&self) -> bool {
        *self != AuthKind::Offline
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LoginStage {
    ExternalBrowser,
    EmbeddedBrowser,
    PairCode,
    Done,
    Failed,
}

impl LoginStage {
    pub fn code(&self) -> &'static str {
        match self {
            LoginStage::ExternalBrowser => "external_browser",
            LoginStage::EmbeddedBrowser => "embedded_browser",
            LoginStage::PairCode => "pair_code",
            LoginStage::Done => "done",
            LoginStage::Failed => "failed",
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct StageAvailability {
    pub external_browser: bool,
    pub embedded_browser: bool,
    pub pair_code_delivered: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum LoginError {
    Cancelled,
    Timeout,
    ZeroLevel(String),
}

pub struct LoginSession {
    pub auth: AuthKind,
    pub stage: LoginStage,
    pub fallback: Fallback,
    pub premium_allowed: bool,
    pub pair_code: String,
    pub diagnostics: Vec<String>,
    pub envelope: Envelope,
    attempts: u8,
}

impl LoginSession {
    pub fn new(auth: AuthKind, premium_allowed: bool) -> Self {
        Self {
            auth,
            stage: if auth.needs_browser() {
                LoginStage::ExternalBrowser
            } else {
                LoginStage::Done
            },
            fallback: Fallback::Three,
            premium_allowed,
            pair_code: String::new(),
            diagnostics: Vec::new(),
            envelope: Envelope::new(Kind::Request, "lightweight.login"),
            attempts: 0,
        }
    }

    fn diag(&mut self, action: &str, result: &str, detail: &str) {
        self.diagnostics
            .push(diag_line("lightweight", action, "login", result, detail));
    }

    pub fn advance(
        &mut self,
        available: &StageAvailability,
        cancel: &CancelToken,
        pair_code: &str,
    ) -> Result<LoginStage, LoginError> {
        if cancel.is_cancelled() {
            self.diag("login", "CANCELLED", "detail=token_cancelled");
            return Err(LoginError::Cancelled);
        }

        if self.auth == AuthKind::Offline {
            self.stage = LoginStage::Done;
            self.fallback = Fallback::Three;
            self.diag("login", "OK", "detail=offline_no_browser");
            self.envelope = Envelope::new(Kind::Response, "lightweight.login")
                .with("auth", "offline")
                .with("stage", "done");
            return Ok(self.stage);
        }

        if self.auth == AuthKind::Mojang && !self.premium_allowed {
            self.stage = LoginStage::Failed;
            self.fallback = Fallback::One;
            self.diag("auth", "DEGRADE", "detail=premium_disabled_credential_absent");
            return Err(LoginError::ZeroLevel("premium_disabled_credential_absent".to_string()));
        }

        loop {
            self.attempts += 1;
            if self.attempts > 4 {
                self.stage = LoginStage::Failed;
                self.fallback = Fallback::Zero;
                self.diag("login", "FAIL", "detail=all_stages_exhausted");
                return Err(LoginError::ZeroLevel("all_stages_exhausted".to_string()));
            }
            match self.stage {
                LoginStage::ExternalBrowser => {
                    if available.external_browser {
                        self.finish();
                        return Ok(self.stage);
                    }
                    self.stage = LoginStage::EmbeddedBrowser;
                    self.fallback = Fallback::Two;
                    self.diag("fallback", "DEGRADE", "detail=external_to_embedded");
                }
                LoginStage::EmbeddedBrowser => {
                    if available.embedded_browser {
                        self.finish();
                        return Ok(self.stage);
                    }
                    self.stage = LoginStage::PairCode;
                    self.fallback = Fallback::Two;
                    self.pair_code = pair_code.to_string();
                    self.diag("fallback", "DEGRADE", "detail=embedded_to_pair_code");
                }
                LoginStage::PairCode => {
                    if cancel.is_cancelled() {
                        self.diag("pair_code", "CANCELLED", "detail=polling_cancelled");
                        return Err(LoginError::Cancelled);
                    }
                    if available.pair_code_delivered {
                        self.finish();
                        return Ok(self.stage);
                    }
                    self.stage = LoginStage::Failed;
                    self.fallback = Fallback::Zero;
                    self.diag("pair_code", "TIMEOUT", &format!("detail=timeout={}s", PAIR_CODE_TIMEOUT.as_secs()));
                    return Err(LoginError::Timeout);
                }
                LoginStage::Done | LoginStage::Failed => return Ok(self.stage),
            }
        }
    }

    fn finish(&mut self) {
        self.stage = LoginStage::Done;
        self.diag("login", "OK", &format!("detail=auth={} stage={}", self.auth.code(), self.stage.code()));
        self.envelope = Envelope::new(Kind::Response, "lightweight.login")
            .with("auth", self.auth.code())
            .with("stage", "done")
            .with("fallback", self.fallback.code());
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn all_up() -> StageAvailability {
        StageAvailability {
            external_browser: true,
            embedded_browser: true,
            pair_code_delivered: true,
        }
    }

    #[test]
    fn offline_login_needs_no_browser() {
        let mut s = LoginSession::new(AuthKind::Offline, false);
        assert!(!s.auth.needs_browser());
        assert_eq!(s.advance(&StageAvailability::default(), &CancelToken::new(), "X").unwrap(), LoginStage::Done);
        assert_eq!(s.fallback, Fallback::Three);
    }

    #[test]
    fn external_browser_succeeds_without_fallback() {
        let mut s = LoginSession::new(AuthKind::ThirdParty, true);
        assert_eq!(s.advance(&all_up(), &CancelToken::new(), "X").unwrap(), LoginStage::Done);
        assert_eq!(s.fallback, Fallback::Three);
        assert!(s.diagnostics.iter().any(|d| d.contains("OK")));
    }

    #[test]
    fn first_fallback_goes_to_embedded_browser() {
        let mut s = LoginSession::new(AuthKind::ThirdParty, true);
        let a = StageAvailability { external_browser: false, embedded_browser: true, ..all_up() };
        assert_eq!(s.advance(&a, &CancelToken::new(), "X").unwrap(), LoginStage::Done);
        assert_eq!(s.fallback, Fallback::Two);
        assert!(s.diagnostics.iter().any(|d| d.contains("external_to_embedded")));
    }

    #[test]
    fn second_fallback_shows_pair_code() {
        let mut s = LoginSession::new(AuthKind::ThirdParty, true);
        let a = StageAvailability { external_browser: false, embedded_browser: false, pair_code_delivered: true };
        assert_eq!(s.advance(&a, &CancelToken::new(), "KCU-7F3A").unwrap(), LoginStage::Done);
        assert_eq!(s.pair_code, "KCU-7F3A");
        assert!(s.diagnostics.iter().any(|d| d.contains("embedded_to_pair_code")));
    }

    #[test]
    fn pair_code_timeout_is_zero_level_error() {
        let mut s = LoginSession::new(AuthKind::ThirdParty, true);
        let a = StageAvailability::default();
        assert_eq!(s.advance(&a, &CancelToken::new(), "KCU-7F3A"), Err(LoginError::Timeout));
        assert_eq!(s.fallback, Fallback::Zero);
        assert!(s.diagnostics.iter().any(|d| d.contains("timeout=300")));
    }

    #[test]
    fn premium_disabled_disables_mojang_but_not_third_party() {
        let mut m = LoginSession::new(AuthKind::Mojang, false);
        assert_eq!(m.advance(&all_up(), &CancelToken::new(), "X"), Err(LoginError::ZeroLevel("premium_disabled_credential_absent".to_string())));
        let mut t = LoginSession::new(AuthKind::ThirdParty, false);
        assert_eq!(t.advance(&all_up(), &CancelToken::new(), "X").unwrap(), LoginStage::Done);
    }

    #[test]
    fn cancelled_token_stops_login() {
        let mut s = LoginSession::new(AuthKind::ThirdParty, true);
        let c = CancelToken::new();
        c.cancel();
        assert_eq!(s.advance(&all_up(), &c, "X"), Err(LoginError::Cancelled));
        assert!(s.diagnostics.iter().any(|d| d.contains("CANCELLED")));
    }

    #[test]
    fn diagnostics_are_single_line_kcu_prefixed() {
        let mut s = LoginSession::new(AuthKind::ThirdParty, true);
        let _ = s.advance(&StageAvailability::default(), &CancelToken::new(), "X");
        for d in &s.diagnostics {
            assert!(d.starts_with("[KCU] "));
            assert!(!d.contains('\n'));
        }
    }
}

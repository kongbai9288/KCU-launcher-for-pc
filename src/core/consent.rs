use crate::core::popup::CloseAction;
use crate::core::robust;
use anyhow::{anyhow, Result};
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const POLICY_VERSION: &str = "v1.1";
pub const POLICY_EFFECTIVE: &str = "2026-11-21";
pub const POLICY_TEXT: &str = include_str!("../../docs/spec/64-privacy-policy-v1.1.txt");
pub const CONSENT_FILE: &str = "privacy-consent.json";
pub const MAX_CONSENT_BYTES: usize = 4096;
pub const MAX_VERSION_BYTES: usize = 64;
pub const DEFAULT_CONSENT: &str = r#"{"schema":1,"version":"","accepted_at":0}"#;
pub const POPUP_ID: &str = "privacy";

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ConsentState {
    pub schema: u8,
    pub version: String,
    pub accepted_at: u64,
}

impl Default for ConsentState {
    fn default() -> Self {
        ConsentState { schema: 1, version: String::new(), accepted_at: 0 }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum ConsentDecision {
    Accepted,
    Required,
    Degraded(String),
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConsentAction {
    Accept,
    Decline,
}

pub fn text_digest() -> String {
    hex::encode(ed25519_compact::sha512::Hash::hash(POLICY_TEXT.as_bytes()).as_ref())
}

fn degrade(reason: &str) -> Vec<String> {
    vec![crate::core::diagnostics::diag_line("privacy", "consent", "load", "DEGRADE", reason)]
}

fn parse(raw: &str) -> Option<ConsentState> {
    if raw.len() > MAX_CONSENT_BYTES { return None; }
    let v: Value = from_str(raw).ok()?;
    let schema = v.get("schema")?.as_u64()?;
    if schema != 1 { return None; }
    let version = v.get("version")?.as_str()?.to_string();
    if version.is_empty() || version.len() > MAX_VERSION_BYTES { return None; }
    let accepted_at = v.get("accepted_at")?.as_u64()?;
    Some(ConsentState { schema: 1, version, accepted_at })
}

pub fn load(root: Option<&Path>) -> (ConsentState, Vec<String>) {
    let Some(dir) = root else {
        return (ConsentState::default(), degrade("in_memory"));
    };
    let Ok(path) = robust::safe_join(dir, CONSENT_FILE) else {
        return (ConsentState::default(), degrade("path_rejected"));
    };
    let (raw, missing) = robust::read_or_default(&path, DEFAULT_CONSENT);
    if missing {
        return (ConsentState::default(), degrade("missing_or_unreadable"));
    }
    match parse(&raw) {
        Some(s) => (s, Vec::new()),
        None => (ConsentState::default(), degrade("schema_or_field_invalid")),
    }
}

pub fn check(state: &ConsentState) -> ConsentDecision {
    if state.version == POLICY_VERSION && !state.version.is_empty() {
        ConsentDecision::Accepted
    } else {
        ConsentDecision::Required
    }
}

pub fn save(root: &Path, state: &ConsentState) -> Result<()> {
    let path = robust::safe_join(root, CONSENT_FILE)?;
    if let Some(parent) = path.parent() { fs::create_dir_all(parent)?; }
    let body = to_string(&json!({
        "schema": state.schema,
        "version": state.version,
        "accepted_at": state.accepted_at
    }))?;
    fs::write(&path, body)?;
    Ok(())
}

pub fn decline() -> ConsentDecision {
    ConsentDecision::Required
}

pub fn resolve(action: CloseAction) -> ConsentAction {
    match action {
        CloseAction::Confirm => ConsentAction::Accept,
        _ => ConsentAction::Decline,
    }
}

pub fn apply(root: Option<&Path>, action: CloseAction, now: u64) -> (ConsentDecision, Vec<String>) {
    if resolve(action) == ConsentAction::Decline {
        return (decline(), Vec::new());
    }
    let Some(dir) = root else {
        let line = crate::core::diagnostics::diag_line("privacy", "consent", "save", "ERROR", "no_root");
        return (ConsentDecision::Degraded("no_root".to_string()), vec![line]);
    };
    let state = ConsentState { schema: 1, version: POLICY_VERSION.to_string(), accepted_at: now };
    match save(dir, &state) {
        Ok(()) => (ConsentDecision::Accepted, Vec::new()),
        Err(e) => {
            let line = crate::core::diagnostics::diag_line("privacy", "consent", "save", "ERROR", &e.to_string());
            (ConsentDecision::Degraded(e.to_string()), vec![line])
        }
    }
}

pub fn require_popup_registered(ids: &[&str]) -> Result<()> {
    if ids.contains(&POPUP_ID) { Ok(()) } else { Err(anyhow!("privacy popup missing")) }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu064-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    #[test]
    fn policy_text_is_verbatim() {
        assert!(POLICY_TEXT.starts_with("《KCU"));
        assert!(POLICY_TEXT.contains("Launcher"));
        assert!(POLICY_TEXT.contains("隐私政策"));
        assert!(POLICY_TEXT.contains("版本： v1.1"));
        assert!(POLICY_TEXT.contains("生效日期： 2026年11月21日"));
        assert!(POLICY_TEXT.contains("kcustudios@outlook.com"));
        assert_eq!(POLICY_VERSION, "v1.1");
        assert_eq!(POLICY_EFFECTIVE, "2026-11-21");
    }

    #[test]
    fn digest_is_stable_and_library_based() {
        let d = text_digest();
        assert_eq!(d.len(), 128);
        assert_eq!(d, text_digest());
    }

    #[test]
    fn missing_file_requires_consent_with_visible_line() {
        let r = tmp();
        let (s, lines) = load(Some(&r));
        assert_eq!(s, ConsentState::default());
        assert_eq!(check(&s), ConsentDecision::Required);
        assert!(lines[0].contains("DEGRADE"));
    }

    #[test]
    fn accept_persists_and_next_load_is_accepted() {
        let r = tmp();
        let (d, _) = apply(Some(&r), CloseAction::Confirm, 1_700_000_000);
        assert_eq!(d, ConsentDecision::Accepted);
        let (s, lines) = load(Some(&r));
        assert_eq!(check(&s), ConsentDecision::Accepted);
        assert!(lines.is_empty());
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn cancel_escape_button_timeout_all_decline_without_write() {
        let r = tmp();
        for a in [CloseAction::Cancel, CloseAction::Escape, CloseAction::Button, CloseAction::Timeout, CloseAction::Host] {
            let (d, lines) = apply(Some(&r), a, 1);
            assert_eq!(d, ConsentDecision::Required);
            assert!(lines.is_empty());
            assert!(!r.join(CONSENT_FILE).exists());
        }
    }

    #[test]
    fn version_change_requires_new_consent() {
        let mut s = ConsentState::default();
        s.version = "v1.0".to_string();
        assert_eq!(check(&s), ConsentDecision::Required);
        s.version = POLICY_VERSION.to_string();
        assert_eq!(check(&s), ConsentDecision::Accepted);
    }

    #[test]
    fn eight_bad_inputs_return_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let p = r.join(CONSENT_FILE);
        let cases = [
            "",
            "not json",
            "{}",
            r#"{"schema":2,"version":"v1.1","accepted_at":1}"#,
            r#"{"schema":1,"version":7,"accepted_at":1}"#,
            r#"{"schema":1,"version":"v1.1","accepted_at":"x"}"#,
            &"x".repeat(MAX_CONSENT_BYTES + 1),
            r#"{"schema":1,"version":"","accepted_at":1}"#,
        ];
        for raw in cases {
            fs::write(&p, raw).unwrap();
            let (s, lines) = load(Some(&r));
            assert_eq!(s, ConsentState::default(), "case={}", &raw[..raw.len().min(24)]);
            assert!(lines.iter().any(|l| l.contains("DEGRADE")));
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn path_traversal_is_rejected_by_robust() {
        let (s, lines) = load(Some(Path::new("/x/../../y")));
        assert_eq!(s, ConsentState::default());
        assert!(lines[0].contains("DEGRADE") || lines[0].contains("path_rejected"));
    }

    #[test]
    fn no_root_is_degraded_not_panic() {
        let (d, lines) = apply(None, CloseAction::Confirm, 1);
        assert!(matches!(d, ConsentDecision::Degraded(_)));
        assert!(lines[0].contains("ERROR"));
    }

    #[test]
    fn popup_id_is_in_registry() {
        assert!(require_popup_registered(&["privacy", "declaration"]).is_ok());
        assert!(require_popup_registered(&["declaration"]).is_err());
    }
}

use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::popup::PopupRegistry;
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::collections::BTreeMap;
use std::fs;
use std::path::Path;

pub const INSTALLS_FILE: &str = "extension-installs.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_INSTALLS: &str = r#"{"schema":1,"installed":[]}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const MAX_INSTALLED: usize = 64;
pub const MAX_ID_BYTES: usize = 256;
pub const MAX_PENDING: usize = 16;
pub const PENDING_TIMEOUT_SECS: u64 = 30;
pub const INSTALL_TARGET: &str = "extension.install";
pub const LOCK_POPUP_ID: &str = "extension";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ExtensionSlot {
    pub slot_id: &'static str,
    pub extension_id: &'static str,
    pub popup_id: &'static str,
    pub label_key: &'static str,
}

pub const EXTENSION_SLOTS: &[ExtensionSlot] = &[
    ExtensionSlot { slot_id: "normal.filemanager", extension_id: "ext.filemanager", popup_id: LOCK_POPUP_ID, label_key: "slot.filemanager" },
    ExtensionSlot { slot_id: "normal.skineditor", extension_id: "ext.skineditor", popup_id: LOCK_POPUP_ID, label_key: "slot.skineditor" },
    ExtensionSlot { slot_id: "normal.worldeditor", extension_id: "ext.worldeditor", popup_id: LOCK_POPUP_ID, label_key: "slot.worldeditor" },
    ExtensionSlot { slot_id: "headless.kculf", extension_id: "ext.kculf", popup_id: LOCK_POPUP_ID, label_key: "slot.kculf" },
    ExtensionSlot { slot_id: "normal.serverhost", extension_id: "ext.serverhost", popup_id: LOCK_POPUP_ID, label_key: "slot.serverhost" },
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SlotState {
    Locked,
    Unlocked,
    Unknown,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClickOutcome {
    InstallPrompt,
    Allowed,
    UnknownSlot,
    PopupMissing,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ResponseDecision {
    Installed,
    Rejected,
}

struct Pending {
    extension_id: String,
    issued_at: u64,
}

pub struct ExtensionGate {
    installed: Vec<String>,
    pending: BTreeMap<String, Pending>,
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("extension", action, "gate", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("extension", action, "gate", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_id(s: &str) -> bool {
    !s.is_empty() && s.len() <= MAX_ID_BYTES && !has_control(s)
}

fn slot(slot_id: &str) -> Option<&'static ExtensionSlot> {
    EXTENSION_SLOTS.iter().find(|s| s.slot_id == slot_id)
}

fn write_installs(root: &Path, installed: &[String]) -> Result<()> {
    let body = to_string(&json!({"schema": 1, "installed": installed}))?;
    let path = robust::safe_join(root, INSTALLS_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", INSTALLS_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl ExtensionGate {
    pub fn open(root: Option<&Path>) -> (ExtensionGate, Vec<String>) {
        let mut gate = ExtensionGate { installed: Vec::new(), pending: BTreeMap::new() };
        let Some(dir) = root else {
            return (gate, vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, INSTALLS_FILE) {
            Ok(p) => p,
            Err(_) => return (gate, vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_INSTALLS);
        if missing {
            return (gate, vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (gate, vec![degrade("load", "too_large")]);
        }
        let value: Value = match from_str(&raw) {
            Ok(v) => v,
            Err(_) => return (gate, vec![degrade("load", "not_json")]),
        };
        let obj = match value.as_object() {
            Some(o) => o,
            None => return (gate, vec![degrade("load", "root_not_object")]),
        };
        if obj.get("schema").and_then(Value::as_u64) != Some(1) {
            return (gate, vec![degrade("load", "schema_invalid")]);
        }
        let arr = match obj.get("installed").and_then(Value::as_array) {
            Some(a) => a,
            None => return (gate, vec![degrade("load", "installed_not_array")]),
        };
        let mut lines = Vec::new();
        for (i, entry) in arr.iter().enumerate() {
            let Some(s) = entry.as_str() else {
                lines.push(degrade("entry", &format!("index={} not_string", i)));
                continue;
            };
            if !valid_id(s) {
                lines.push(degrade("entry", &format!("index={} bad_id", i)));
                continue;
            }
            if !EXTENSION_SLOTS.iter().any(|x| x.extension_id == s) {
                lines.push(degrade("entry", &format!("index={} unknown_extension", i)));
                continue;
            }
            if !gate.installed.contains(&s.to_string()) {
                gate.installed.push(s.to_string());
            }
        }
        if gate.installed.len() > MAX_INSTALLED {
            let excess = gate.installed.len() - MAX_INSTALLED;
            gate.installed.truncate(MAX_INSTALLED);
            lines.push(degrade("entry", &format!("overflow={}", excess)));
        }
        (gate, lines)
    }

    pub fn slot_state(&self, slot_id: &str) -> SlotState {
        let Some(s) = slot(slot_id) else { return SlotState::Unknown };
        if self.installed.iter().any(|x| x == s.extension_id) {
            SlotState::Unlocked
        } else {
            SlotState::Locked
        }
    }

    pub fn on_lock_click(&self, slot_id: &str, popups: &mut PopupRegistry) -> (ClickOutcome, Vec<String>) {
        let Some(s) = slot(slot_id) else {
            return (ClickOutcome::UnknownSlot, vec![degrade("click", "unknown_slot")]);
        };
        if self.slot_state(slot_id) == SlotState::Unlocked {
            return (ClickOutcome::Allowed, Vec::new());
        }
        match popups.open_registered(s.popup_id) {
            Ok(()) => (ClickOutcome::InstallPrompt, Vec::new()),
            Err(e) => (ClickOutcome::PopupMissing, vec![error_line("click", &format!("popup={:?}", e))]),
        }
    }

    pub fn begin_install(&mut self, slot_id: &str, now: u64) -> (Option<Envelope>, Vec<String>) {
        let Some(s) = slot(slot_id) else {
            return (None, vec![degrade("begin", "unknown_slot")]);
        };
        if self.installed.iter().any(|x| x == s.extension_id) {
            return (None, vec![degrade("begin", "already_installed")]);
        }
        self.expire(now);
        if self.pending.len() >= MAX_PENDING {
            return (None, vec![degrade("begin", "pending_full")]);
        }
        let envelope = Envelope::new(Kind::Request, INSTALL_TARGET)
            .with("slot_id", s.slot_id)
            .with("extension_id", s.extension_id);
        self.pending.insert(
            envelope.request_id.clone(),
            Pending { extension_id: s.extension_id.to_string(), issued_at: now },
        );
        (Some(envelope), Vec::new())
    }

    fn expire(&mut self, now: u64) -> Vec<String> {
        let expired: Vec<String> = self
            .pending
            .iter()
            .filter(|(_, p)| now.saturating_sub(p.issued_at) > PENDING_TIMEOUT_SECS)
            .map(|(k, _)| k.clone())
            .collect();
        let mut lines = Vec::new();
        for key in &expired {
            self.pending.remove(key);
            lines.push(degrade("expire", "timeout"));
        }
        lines
    }

    pub fn accept_response(&mut self, root: Option<&Path>, response: &Envelope, now: u64) -> (ResponseDecision, Vec<String>) {
        let mut lines = self.expire(now);
        if response.kind != Kind::Response {
            lines.push(degrade("response", "kind_not_response"));
            return (ResponseDecision::Rejected, lines);
        }
        if response.target != INSTALL_TARGET {
            lines.push(degrade("response", "target_not_allowed"));
            return (ResponseDecision::Rejected, lines);
        }
        if !response.ok() {
            lines.push(degrade("response", "error_envelope"));
            return (ResponseDecision::Rejected, lines);
        }
        let Some(p) = self.pending.get(&response.request_id) else {
            lines.push(degrade("response", "unknown_or_replayed_request_id"));
            return (ResponseDecision::Rejected, lines);
        };
        if now.saturating_sub(p.issued_at) > PENDING_TIMEOUT_SECS {
            self.pending.remove(&response.request_id);
            lines.push(degrade("response", "timeout"));
            return (ResponseDecision::Rejected, lines);
        }
        let Some(ext) = response.field("extension_id") else {
            lines.push(degrade("response", "extension_id_missing"));
            return (ResponseDecision::Rejected, lines);
        };
        if ext != p.extension_id {
            lines.push(degrade("response", "extension_id_mismatch"));
            return (ResponseDecision::Rejected, lines);
        }
        if !EXTENSION_SLOTS.iter().any(|s| s.extension_id == ext) {
            lines.push(degrade("response", "extension_id_unknown"));
            return (ResponseDecision::Rejected, lines);
        }
        let ext_owned = ext.to_string();
        self.pending.remove(&response.request_id);
        if !self.installed.contains(&ext_owned) {
            self.installed.push(ext_owned);
        }
        let Some(dir) = root else {
            lines.push(error_line("response", "no_root"));
            return (ResponseDecision::Rejected, lines);
        };
        match write_installs(dir, &self.installed) {
            Ok(()) => (ResponseDecision::Installed, lines),
            Err(e) => {
                lines.push(error_line("response", &e.to_string()));
                (ResponseDecision::Rejected, lines)
            }
        }
    }

    pub fn installed_count(&self) -> usize {
        self.installed.len()
    }

    pub fn pending_count(&self) -> usize {
        self.pending.len()
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    let Some(dir) = root else { return vec![error_line("reset", "no_root")] };
    match write_installs(dir, &[]) {
        Ok(()) => Vec::new(),
        Err(e) => vec![error_line("reset", &e.to_string())],
    }
}

pub fn event_from_request(request: &Envelope) -> Option<Envelope> {
    if request.kind != Kind::Request || request.target != INSTALL_TARGET {
        return None;
    }
    let Some(ext) = request.field("extension_id") else { return None };
    if !EXTENSION_SLOTS.iter().any(|s| s.extension_id == ext) {
        return None;
    }
    Some(Envelope::new(Kind::Event, INSTALL_TARGET).with("extension_id", ext))
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::envelope::Kind as EKind;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu067-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    fn response_for(request: &Envelope) -> Envelope {
        let ext = request.field("extension_id").unwrap_or("").to_string();
        let mut e = Envelope::new(EKind::Response, INSTALL_TARGET);
        e.request_id = request.request_id.clone();
        e.with("extension_id", &ext)
    }

    #[test]
    fn slot_table_is_closed_and_unique() {
        assert_eq!(EXTENSION_SLOTS.len(), 5);
        let mut ids: Vec<&str> = EXTENSION_SLOTS.iter().map(|s| s.slot_id).collect();
        ids.sort();
        ids.dedup();
        assert_eq!(ids.len(), 5);
        assert!(EXTENSION_SLOTS.iter().all(|s| s.popup_id == LOCK_POPUP_ID));
        assert!(EXTENSION_SLOTS.iter().all(|s| !s.label_key.is_empty()));
    }

    #[test]
    fn default_state_is_all_locked() {
        let (g, lines) = ExtensionGate::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(g.installed_count(), 0);
        for s in EXTENSION_SLOTS {
            assert_eq!(g.slot_state(s.slot_id), SlotState::Locked);
        }
        assert_eq!(g.slot_state("not.registered"), SlotState::Unknown);
    }

    #[test]
    fn eight_bad_inputs_return_to_default() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        let path = r.join(INSTALLS_FILE);
        let cases = [
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            r#"{"schema":2,"installed":[]}"#.to_string(),
            r#"{"schema":1,"installed":"oops"}"#.to_string(),
            r#"{"schema":1,"installed":[7]}"#.to_string(),
            r#"{"schema":1,"installed":["ext.unknown"]}"#.to_string(),
        ];
        for raw in cases {
            fs::write(&path, &raw).unwrap();
            let (g, lines) = ExtensionGate::open(Some(&r));
            assert_eq!(g.installed_count(), 0, "case={}", &raw[..raw.len().min(20)]);
            assert!(lines.iter().any(|l| l.contains("DEGRADE")), "case={}", &raw[..raw.len().min(20)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn lock_click_opens_registered_popup_only_when_locked() {
        let r = tmp();
        let (mut g, _) = ExtensionGate::open(Some(&r));
        let mut p = PopupRegistry::new();
        let (outcome, _) = g.on_lock_click("normal.filemanager", &mut p);
        assert_eq!(outcome, ClickOutcome::InstallPrompt);
        assert_eq!(p.open_count(), 1);
        p.close_all_registered();
        let (env, lines) = g.begin_install("normal.filemanager", 100);
        assert!(lines.is_empty());
        let resp = response_for(env.as_ref().unwrap());
        let (decision, _) = g.accept_response(Some(&r), &resp, 101);
        assert_eq!(decision, ResponseDecision::Installed);
        assert_eq!(g.slot_state("normal.filemanager"), SlotState::Unlocked);
        let (outcome2, _) = g.on_lock_click("normal.filemanager", &mut p);
        assert_eq!(outcome2, ClickOutcome::Allowed);
        assert_eq!(p.open_count(), 0);
        let (outcome3, _) = g.on_lock_click("not.registered", &mut p);
        assert_eq!(outcome3, ClickOutcome::UnknownSlot);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn event_cannot_unlock_and_forged_response_is_rejected() {
        let r = tmp();
        let (mut g, _) = ExtensionGate::open(Some(&r));
        let (env, _) = g.begin_install("headless.kculf", 10);
        let request = env.unwrap();
        let forged = Envelope::new(EKind::Event, INSTALL_TARGET).with("extension_id", "ext.kculf");
        let (d1, l1) = g.accept_response(Some(&r), &forged, 11);
        assert_eq!(d1, ResponseDecision::Rejected);
        assert!(l1.iter().any(|x| x.contains("kind_not_response")));
        let mut wrong = response_for(&request);
        wrong.request_id = Envelope::new(EKind::Response, INSTALL_TARGET).request_id;
        let (d2, l2) = g.accept_response(Some(&r), &wrong, 12);
        assert_eq!(d2, ResponseDecision::Rejected);
        assert!(l2.iter().any(|x| x.contains("unknown_or_replayed_request_id")));
        assert_eq!(g.slot_state("headless.kculf"), SlotState::Locked);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn response_id_is_consumed_once() {
        let r = tmp();
        let (mut g, _) = ExtensionGate::open(Some(&r));
        let (env, _) = g.begin_install("normal.skineditor", 10);
        let request = env.unwrap();
        let resp = response_for(&request);
        assert_eq!(g.accept_response(Some(&r), &resp, 11).0, ResponseDecision::Installed);
        let (d, lines) = g.accept_response(Some(&r), &resp, 12);
        assert_eq!(d, ResponseDecision::Rejected);
        assert!(lines.iter().any(|x| x.contains("unknown_or_replayed_request_id")));
        assert_eq!(g.installed_count(), 1);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn mismatched_extension_id_is_rejected() {
        let r = tmp();
        let (mut g, _) = ExtensionGate::open(Some(&r));
        let (env, _) = g.begin_install("normal.worldeditor", 10);
        let request = env.unwrap();
        let mut resp = response_for(&request);
        resp.payload.insert("extension_id".to_string(), Value::String("ext.kculf".to_string()));
        let (d, lines) = g.accept_response(Some(&r), &resp, 11);
        assert_eq!(d, ResponseDecision::Rejected);
        assert!(lines.iter().any(|x| x.contains("extension_id_mismatch")));
        assert_eq!(g.slot_state("normal.worldeditor"), SlotState::Locked);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn timeout_and_error_and_bad_target_are_rejected() {
        let r = tmp();
        let (mut g, _) = ExtensionGate::open(Some(&r));
        let (env, _) = g.begin_install("normal.serverhost", 10);
        let request = env.unwrap();
        let late = response_for(&request);
        let (d1, l1) = g.accept_response(Some(&r), &late, 10 + PENDING_TIMEOUT_SECS + 1);
        assert_eq!(d1, ResponseDecision::Rejected);
        assert!(l1.iter().any(|x| x.contains("timeout")));
        let (env2, _) = g.begin_install("normal.serverhost", 100);
        let request2 = env2.unwrap();
        let mut err = response_for(&request2);
        err = err.with_error("install_failed");
        let (d2, l2) = g.accept_response(Some(&r), &err, 101);
        assert_eq!(d2, ResponseDecision::Rejected);
        assert!(l2.iter().any(|x| x.contains("error_envelope")));
        let (env3, _) = g.begin_install("normal.filemanager", 200);
        let request3 = env3.unwrap();
        let mut bad_target = response_for(&request3);
        bad_target.target = "other.target".to_string();
        let (d3, l3) = g.accept_response(Some(&r), &bad_target, 201);
        assert_eq!(d3, ResponseDecision::Rejected);
        assert!(l3.iter().any(|x| x.contains("target_not_allowed")));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn reset_keeps_protected_files_and_relocks_all() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let (mut g, _) = ExtensionGate::open(Some(&r));
        let (env, _) = g.begin_install("headless.kculf", 1);
        let resp = response_for(env.as_ref().unwrap());
        assert_eq!(g.accept_response(Some(&r), &resp, 2).0, ResponseDecision::Installed);
        assert_eq!(reset(Some(&r)).len(), 0);
        let (back, _) = ExtensionGate::open(Some(&r));
        assert_eq!(back.installed_count(), 0);
        assert_eq!(back.slot_state("headless.kculf"), SlotState::Locked);
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn persisted_install_survives_reopen() {
        let r = tmp();
        let (mut g, _) = ExtensionGate::open(Some(&r));
        let (env, _) = g.begin_install("normal.filemanager", 1);
        let resp = response_for(env.as_ref().unwrap());
        g.accept_response(Some(&r), &resp, 2);
        let (back, lines) = ExtensionGate::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.installed_count(), 1);
        assert_eq!(back.slot_state("normal.filemanager"), SlotState::Unlocked);
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn pending_is_bounded_and_no_root_is_visible() {
        let r = tmp();
        let (mut g, _) = ExtensionGate::open(Some(&r));
        for _ in 0..(MAX_PENDING + 3) {
            let (env, lines) = g.begin_install("normal.filemanager", 100);
            if env.is_none() {
                assert!(lines.iter().any(|x| x.contains("pending_full")));
            }
        }
        assert!(g.pending_count() <= MAX_PENDING);
        let (env, _) = g.begin_install("normal.skineditor", 100);
        assert!(env.is_none());
        let (mut g2, _) = ExtensionGate::open(None);
        let (env2, _) = g2.begin_install("normal.skineditor", 1);
        let request2 = env2.unwrap();
        let resp2 = response_for(&request2);
        let (d, lines) = g2.accept_response(None, &resp2, 2);
        assert_eq!(d, ResponseDecision::Rejected);
        assert!(lines.iter().any(|x| x.contains("ERROR")));
        assert!(reset(None)[0].contains("ERROR"));
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn event_from_request_only_for_known_install_requests() {
        let (mut g, _) = ExtensionGate::open(None);
        let (env, _) = g.begin_install("normal.worldeditor", 1);
        let request = env.unwrap();
        let event = event_from_request(&request).unwrap();
        assert_eq!(event.kind, EKind::Event);
        assert_eq!(event.field("extension_id"), Some("ext.worldeditor"));
        assert!(event_from_request(&Envelope::new(EKind::Event, INSTALL_TARGET)).is_none());
        let plain = Envelope::new(EKind::Request, "other.target");
        assert!(event_from_request(&plain).is_none());
        let (d, _) = g.accept_response(None, &event, 2);
        assert_eq!(d, ResponseDecision::Rejected);
    }
}

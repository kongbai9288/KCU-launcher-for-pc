use std::collections::BTreeMap;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CloseAction {
    Button,
    Escape,
    Cancel,
    Confirm,
    Timeout,
    Host,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PopupKind {
    PrivacyPolicy,
    Declaration,
    Eula,
    DuplicateMod,
    FileLockWarning,
    GuestPassword,
    OnlineNotice,
    Duration,
    Error,
    AiConfirm,
    ExtensionInstall,
}

#[derive(Debug, Clone)]
pub struct Popup {
    pub id: String,
    pub kind: PopupKind,
    pub title: String,
    pub closable: bool,
    pub has_close_button: bool,
    pub has_escape: bool,
    pub has_cancel: bool,
    pub closed: bool,
    pub close_reason: Option<CloseAction>,
    special_reason: Option<CloseAction>,
}

impl Popup {
    pub fn new(id: &str, kind: PopupKind, title: &str) -> Self {
        Self {
            id: id.to_string(),
            kind,
            title: title.to_string(),
            closable: true,
            has_close_button: true,
            has_escape: true,
            has_cancel: true,
            closed: false,
            close_reason: None,
            special_reason: None,
        }
    }

    pub fn with_special(mut self, reason: CloseAction) -> Self {
        self.special_reason = Some(reason);
        self
    }

    pub fn allow(mut self, button: bool, escape: bool, cancel: bool) -> Self {
        self.has_close_button = button;
        self.has_escape = escape;
        self.has_cancel = cancel;
        self.closable = button || escape || cancel || self.special_reason.is_some();
        self
    }

    pub fn close(&mut self, action: CloseAction) -> bool {
        if self.closed {
            return true;
        }
        let permitted = match action {
            CloseAction::Button => self.has_close_button,
            CloseAction::Escape => self.has_escape,
            CloseAction::Cancel => self.has_cancel,
            CloseAction::Confirm | CloseAction::Timeout | CloseAction::Host => true,
        };
        if self.special_reason == Some(action) {
            self.closed = true;
            self.close_reason = Some(action);
            return true;
        }
        if !permitted || !self.closable {
            return false;
        }
        self.closed = true;
        self.close_reason = Some(action);
        true
    }

    pub fn is_closed(&self) -> bool {
        self.closed
    }

    pub fn has_close_path(&self) -> bool {
        self.has_close_button
            || self.has_escape
            || self.has_cancel
            || self.special_reason.is_some()
    }
}

#[derive(Debug, Default)]
pub struct PopupRegistry {
    items: BTreeMap<String, Popup>,
}

impl PopupRegistry {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn open(&mut self, popup: Popup) {
        self.items.insert(popup.id.clone(), popup);
    }

    pub fn close(&mut self, id: &str, action: CloseAction) -> bool {
        match self.items.get_mut(id) {
            Some(p) => p.close(action),
            None => false,
        }
    }

    pub fn open_count(&self) -> usize {
        self.items.values().filter(|p| !p.is_closed()).count()
    }

    pub fn all_closed(&self) -> bool {
        self.open_count() == 0
    }

    pub fn missing_close_path(&self) -> Vec<String> {
        self.items
            .iter()
            .filter(|(_, p)| !p.has_close_path())
            .map(|(id, _)| id.clone())
            .collect()
    }

    pub fn force_close_all(&mut self) -> usize {
        let mut n = 0;
        for p in self.items.values_mut() {
            if !p.is_closed() {
                p.closed = true;
                p.close_reason = Some(CloseAction::Host);
                n += 1;
            }
        }
        n
    }

    pub fn len(&self) -> usize {
        self.items.len()
    }
}

pub fn catalog() -> Vec<Popup> {
    vec![
        Popup::new("privacy", PopupKind::PrivacyPolicy, "privacy"),
        Popup::new("declaration", PopupKind::Declaration, "declaration"),
        Popup::new("eula", PopupKind::Eula, "eula"),
        Popup::new("dup-mod", PopupKind::DuplicateMod, "duplicate_mod"),
        Popup::new("file-lock", PopupKind::FileLockWarning, "file_lock"),
        Popup::new("guest", PopupKind::GuestPassword, "guest_password"),
        Popup::new("notice", PopupKind::OnlineNotice, "kcu_recorder"),
        Popup::new("duration", PopupKind::Duration, "play_duration"),
        Popup::new("error", PopupKind::Error, "error"),
        Popup::new("ai-confirm", PopupKind::AiConfirm, "ai_request"),
        Popup::new("extension", PopupKind::ExtensionInstall, "extension_install"),
    ]
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn every_catalog_popup_has_close_path() {
        let mut r = PopupRegistry::new();
        for p in catalog() {
            r.open(p);
        }
        assert_eq!(r.len(), 11);
        assert!(r.missing_close_path().is_empty());
    }

    #[test]
    fn every_catalog_popup_can_be_closed_by_button() {
        let mut r = PopupRegistry::new();
        for p in catalog() {
            r.open(p);
        }
        for p in catalog() {
            assert!(r.close(&p.id, CloseAction::Button), "{}", p.id);
        }
        assert!(r.all_closed());
        assert_eq!(r.open_count(), 0);
    }

    #[test]
    fn escape_and_cancel_also_close() {
        let mut p = Popup::new("x", PopupKind::Error, "error");
        assert!(p.has_close_path());
        assert!(p.close(CloseAction::Escape));
        let mut q = Popup::new("y", PopupKind::Error, "error");
        assert!(q.close(CloseAction::Cancel));
    }

    #[test]
    fn special_requirement_overrides_default() {
        let mut p = Popup::new("x", PopupKind::Declaration, "declaration")
            .with_special(CloseAction::Host)
            .allow(false, false, false);
        assert!(!p.close(CloseAction::Button));
        assert!(p.close(CloseAction::Host));
        assert!(p.is_closed());
    }

    #[test]
    fn closing_twice_is_idempotent() {
        let mut p = Popup::new("x", PopupKind::Duration, "duration");
        assert!(p.close(CloseAction::Button));
        assert!(p.close(CloseAction::Button));
        assert_eq!(p.close_reason, Some(CloseAction::Button));
    }

    #[test]
    fn force_close_all_leaves_no_open_popup() {
        let mut r = PopupRegistry::new();
        for p in catalog() {
            r.open(p);
        }
        assert_eq!(r.force_close_all(), 11);
        assert!(r.all_closed());
    }
}

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

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum PopupKind {
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
    PluginUpgradeConfirm,
    PluginFault,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct PopupSpec {
    pub id: &'static str,
    pub kind: PopupKind,
    pub title_key: &'static str,
    pub button: bool,
    pub escape: bool,
    pub cancel: bool,
    pub special: Option<CloseAction>,
}

/// 弹窗唯一声明源。新增弹窗只改这张表，行为由注册表统一给出。
pub(crate) const POPUP_SPECS: &[PopupSpec] = &[
    PopupSpec { id: "privacy", kind: PopupKind::PrivacyPolicy, title_key: "privacy", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "declaration", kind: PopupKind::Declaration, title_key: "declaration", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "eula", kind: PopupKind::Eula, title_key: "eula", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "dup-mod", kind: PopupKind::DuplicateMod, title_key: "duplicate_mod", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "file-lock", kind: PopupKind::FileLockWarning, title_key: "file_lock", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "guest", kind: PopupKind::GuestPassword, title_key: "guest_password", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "notice", kind: PopupKind::OnlineNotice, title_key: "kcu_recorder", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "duration", kind: PopupKind::Duration, title_key: "play_duration", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "error", kind: PopupKind::Error, title_key: "error", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "ai-confirm", kind: PopupKind::AiConfirm, title_key: "ai_request", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "extension", kind: PopupKind::ExtensionInstall, title_key: "extension_install", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "plugin-upgrade", kind: PopupKind::PluginUpgradeConfirm, title_key: "plugin_upgrade", button: true, escape: true, cancel: true, special: None },
    PopupSpec { id: "plugin-fault", kind: PopupKind::PluginFault, title_key: "plugin_fault", button: true, escape: true, cancel: true, special: None },
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PopupOpenError {
    UnknownId,
}

#[derive(Debug, Clone)]
pub(crate) struct Popup {
    pub id: String,
    // 注册表元数据：非测试构建不读取，保留供后续查询；显式标注而非删除。
    #[allow(dead_code)]
    pub kind: PopupKind,
    #[allow(dead_code)]
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
    pub(crate) fn new(id: &str, kind: PopupKind, title: &str) -> Self {
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

    pub(crate) fn from_spec(spec: &PopupSpec) -> Self {
        let mut p = Self::new(spec.id, spec.kind, spec.title_key);
        if let Some(reason) = spec.special {
            p = p.with_special(reason);
        }
        p.allow(spec.button, spec.escape, spec.cancel)
    }

    fn with_special(mut self, reason: CloseAction) -> Self {
        self.special_reason = Some(reason);
        self
    }

    fn allow(mut self, button: bool, escape: bool, cancel: bool) -> Self {
        self.has_close_button = button;
        self.has_escape = escape;
        self.has_cancel = cancel;
        self.closable = button || escape || cancel || self.special_reason.is_some();
        self
    }

    fn close(&mut self, action: CloseAction) -> bool {
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

    fn is_closed(&self) -> bool {
        self.closed
    }

    fn has_close_path(&self) -> bool {
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

    pub(crate) fn open(&mut self, popup: Popup) {
        self.items.insert(popup.id.clone(), popup);
    }

    /// 按注册表 id 打开。未知 id 拒绝，不构造、不落表。
    pub fn open_registered(&mut self, id: &str) -> Result<(), PopupOpenError> {
        let spec = POPUP_SPECS
            .iter()
            .find(|s| s.id == id)
            .ok_or(PopupOpenError::UnknownId)?;
        self.open(Popup::from_spec(spec));
        Ok(())
    }

    /// 全表统一打开，返回注册表条数。
    pub fn open_all_registered(&mut self) -> usize {
        for spec in POPUP_SPECS {
            self.open(Popup::from_spec(spec));
        }
        POPUP_SPECS.len()
    }

    /// 全表统一关闭，返回已关闭条数。
    pub fn close_all_registered(&mut self) -> usize {
        let mut n = 0;
        for spec in POPUP_SPECS {
            if self.close(spec.id, CloseAction::Button)
                || self.close(spec.id, CloseAction::Escape)
            {
                n += 1;
            }
        }
        n
    }

    pub fn registered_ids(&self) -> Vec<&'static str> {
        POPUP_SPECS.iter().map(|s| s.id).collect()
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

#[cfg(test)]
pub(crate) fn catalog() -> Vec<Popup> {
    POPUP_SPECS.iter().map(Popup::from_spec).collect()
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
        assert_eq!(r.len(), 13);
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
        assert_eq!(r.force_close_all(), 13);
        assert!(r.all_closed());
    }

    #[test]
    fn spec_table_is_single_source() {
        assert_eq!(POPUP_SPECS.len(), 13);
        assert_eq!(catalog().len(), POPUP_SPECS.len());
        let ids: std::collections::BTreeSet<_> = POPUP_SPECS.iter().map(|s| s.id).collect();
        assert_eq!(ids.len(), POPUP_SPECS.len());
        assert_eq!(PopupRegistry::new().registered_ids().len(), 13);
    }

    #[test]
    fn unknown_id_is_rejected_and_does_not_enter_registry() {
        let mut r = PopupRegistry::new();
        assert_eq!(r.open_registered("nope"), Err(PopupOpenError::UnknownId));
        assert_eq!(r.len(), 0);
    }

    #[test]
    fn registered_open_matches_catalog_behavior() {
        for spec in POPUP_SPECS {
            let mut a = PopupRegistry::new();
            let mut b = PopupRegistry::new();
            assert!(a.open_registered(spec.id).is_ok());
            b.open(Popup::from_spec(spec));
            assert_eq!(a.len(), b.len());
            assert_eq!(a.missing_close_path(), b.missing_close_path());
            assert_eq!(a.open_count(), b.open_count());
        }
    }

    #[test]
    fn duplicate_open_does_not_grow_registry() {
        let mut r = PopupRegistry::new();
        assert!(r.open_registered("error").is_ok());
        assert!(r.open_registered("error").is_ok());
        assert_eq!(r.len(), 1);
    }

    #[test]
    fn open_all_and_close_all_are_uniform() {
        let mut r = PopupRegistry::new();
        assert_eq!(r.open_all_registered(), 13);
        assert_eq!(r.len(), 13);
        assert!(r.missing_close_path().is_empty());
        assert_eq!(r.close_all_registered(), 13);
        assert!(r.all_closed());
        assert_eq!(r.open_count(), 0);
    }

    #[test]
    fn every_spec_has_a_close_path() {
        for spec in POPUP_SPECS {
            assert!(
                spec.button || spec.escape || spec.cancel || spec.special.is_some(),
                "{}",
                spec.id
            );
        }
    }
}

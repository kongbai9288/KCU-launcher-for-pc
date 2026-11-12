use crate::core::asynk::CancelToken;
use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use std::collections::BTreeSet;

#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum LoaderKind {
    Fabric,
    Forge,
    NeoForge,
    Quilt,
    LiteLoader,
    OptiFine,
}

impl LoaderKind {
    pub fn code(&self) -> &'static str {
        match self {
            LoaderKind::Fabric => "fabric",
            LoaderKind::Forge => "forge",
            LoaderKind::NeoForge => "neoforge",
            LoaderKind::Quilt => "quilt",
            LoaderKind::LiteLoader => "liteloader",
            LoaderKind::OptiFine => "optifine",
        }
    }

    pub fn all() -> [LoaderKind; 6] {
        [
            LoaderKind::Fabric,
            LoaderKind::Forge,
            LoaderKind::NeoForge,
            LoaderKind::Quilt,
            LoaderKind::LiteLoader,
            LoaderKind::OptiFine,
        ]
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum InstallOutcome {
    Installed(String),
    Skipped(String),
    Failed(String),
}

impl InstallOutcome {
    pub fn code(&self) -> &'static str {
        match self {
            InstallOutcome::Installed(_) => "installed",
            InstallOutcome::Skipped(_) => "skipped",
            InstallOutcome::Failed(_) => "failed",
        }
    }
}

pub struct LoaderRegistry {
    registered: BTreeSet<LoaderKind>,
    pub diagnostics: Vec<String>,
}

impl Default for LoaderRegistry {
    fn default() -> Self {
        Self {
            registered: BTreeSet::new(),
            diagnostics: Vec::new(),
        }
    }
}

impl LoaderRegistry {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn register(&mut self, kind: LoaderKind) -> bool {
        let inserted = self.registered.insert(kind);
        self.diagnostics.push(diag_line(
            "lightweight",
            "register",
            "loader",
            if inserted { "OK" } else { "DEGRADE" },
            &format!("detail={} duplicate={}", kind.code(), !inserted),
        ));
        inserted
    }

    pub fn register_all(&mut self) {
        for k in LoaderKind::all() {
            self.register(k);
        }
    }

    pub fn contains(&self, kind: LoaderKind) -> bool {
        self.registered.contains(&kind)
    }

    pub fn len(&self) -> usize {
        self.registered.len()
    }

    pub fn is_empty(&self) -> bool {
        self.registered.is_empty()
    }

    pub fn codes(&self) -> Vec<&'static str> {
        self.registered.iter().map(LoaderKind::code).collect()
    }

    pub fn version_json_fields(&self) -> Vec<String> {
        Vec::new()
    }

    pub fn schema_patch(&self) -> Option<String> {
        None
    }

    pub fn install(&mut self, kind: LoaderKind, cancel: &CancelToken) -> InstallOutcome {
        let outcome = if cancel.is_cancelled() {
            InstallOutcome::Skipped("cancelled".to_string())
        } else if !self.registered.contains(&kind) {
            InstallOutcome::Skipped("not_registered".to_string())
        } else {
            InstallOutcome::Installed(kind.code().to_string())
        };
        let result = match &outcome {
            InstallOutcome::Installed(_) => "OK",
            InstallOutcome::Skipped(_) => "DEGRADE",
            InstallOutcome::Failed(_) => "FAIL",
        };
        self.diagnostics.push(diag_line(
            "lightweight",
            "install",
            "loader",
            result,
            &format!("detail={} outcome={}", kind.code(), outcome.code()),
        ));
        outcome
    }

    pub fn envelope(&self) -> Envelope {
        Envelope::new(Kind::Response, "lightweight.loaders")
            .with("registered", &self.len().to_string())
            .with("schema_patch", "none")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn six_loaders_are_registered_once() {
        let mut r = LoaderRegistry::new();
        r.register_all();
        r.register_all();
        assert_eq!(r.len(), 6);
        assert_eq!(r.codes().len(), 6);
        assert!(r.contains(LoaderKind::Fabric));
        assert!(r.contains(LoaderKind::OptiFine));
    }

    #[test]
    fn duplicate_register_is_visible_and_not_fatal() {
        let mut r = LoaderRegistry::new();
        assert!(r.register(LoaderKind::Quilt));
        assert!(!r.register(LoaderKind::Quilt));
        assert_eq!(r.len(), 1);
        assert!(r.diagnostics.iter().any(|d| d.contains("duplicate=true")));
    }

    #[test]
    fn uninstalled_loader_install_is_skipped_not_crash() {
        let mut r = LoaderRegistry::new();
        assert_eq!(r.install(LoaderKind::Forge, &CancelToken::new()), InstallOutcome::Skipped("not_registered".to_string()));
    }

    #[test]
    fn installed_loader_returns_record_without_schema_fields() {
        let mut r = LoaderRegistry::new();
        r.register(LoaderKind::NeoForge);
        assert_eq!(r.install(LoaderKind::NeoForge, &CancelToken::new()), InstallOutcome::Installed("neoforge".to_string()));
        assert!(r.version_json_fields().is_empty());
        assert_eq!(r.schema_patch(), None);
    }

    #[test]
    fn cancelled_install_skips() {
        let mut r = LoaderRegistry::new();
        r.register(LoaderKind::Forge);
        let c = CancelToken::new();
        c.cancel();
        assert_eq!(r.install(LoaderKind::Forge, &c), InstallOutcome::Skipped("cancelled".to_string()));
    }

    #[test]
    fn envelope_declares_no_schema_patch() {
        let mut r = LoaderRegistry::new();
        r.register_all();
        let e = r.envelope();
        assert_eq!(e.field("registered"), Some("6"));
        assert_eq!(e.field("schema_patch"), Some("none"));
    }

    #[test]
    fn diagnostics_are_single_line_kcu_prefixed() {
        let mut r = LoaderRegistry::new();
        r.register_all();
        for d in &r.diagnostics {
            assert!(d.starts_with("[KCU] "));
            assert!(!d.contains('\n'));
        }
    }
}

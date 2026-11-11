use std::path::{Path, PathBuf};

pub struct PathResolver {
    root: PathBuf,
}

const LOGICAL: &[(&str, &str)] = &[
    ("config", "config"),
    ("logs", "logs"),
    ("icons", "assets/icons"),
    ("lang", "lang"),
    ("instances", "instances"),
    ("backups", "backups"),
    ("dialogs_state", "state/dialogs"),
    ("diag", "diagnostics"),
];

impl PathResolver {
    pub fn new(root: impl Into<PathBuf>) -> Self {
        Self { root: root.into() }
    }

    pub fn from_env(key: &str) -> Result<Self, String> {
        let value = std::env::var(key).map_err(|_| format!("{} unset", key))?;
        Ok(Self::new(value))
    }

    pub fn root(&self) -> &Path {
        &self.root
    }

    pub fn resolve(&self, logical: &str) -> Result<PathBuf, String> {
        for (name, segment) in LOGICAL {
            if *name == logical {
                return Ok(self.root.join(segment));
            }
        }
        Err(format!("unknown logical name: {}", logical))
    }

    pub fn logical_names(&self) -> Vec<&'static str> {
        LOGICAL.iter().map(|(name, _)| *name).collect()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn resolves_every_logical_name() {
        let r = PathResolver::new("KCU");
        for name in r.logical_names() {
            assert!(r.resolve(name).is_ok(), "{}", name);
        }
    }

    #[test]
    fn unknown_name_is_rejected() {
        assert!(PathResolver::new("KCU").resolve("nope").is_err());
    }

    #[test]
    fn root_is_injected_not_hardcoded() {
        let a = PathResolver::new("KCU");
        let b = PathResolver::new("OTHER");
        assert_ne!(a.root(), b.root());
        assert_eq!(a.resolve("config").unwrap(), PathBuf::from("KCU/config"));
    }

    #[test]
    fn save_path_is_selectable() {
        let r = PathResolver::from_env("KCU_TEST_ROOT").unwrap_or_else(|_| PathResolver::new("KCU"));
        assert!(r.resolve("backups").unwrap().ends_with("backups"));
    }
}

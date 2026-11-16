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

    pub fn from_env(key: &str) -> anyhow::Result<Self> {
        let value = std::env::var(key).map_err(|_| anyhow::anyhow!("{} unset", key))?;
        Ok(Self::new(value))
    }

    pub fn root(&self) -> &Path {
        &self.root
    }

    pub fn resolve(&self, logical: &str) -> anyhow::Result<PathBuf> {
        for (name, segment) in LOGICAL {
            if *name == logical {
                return Ok(self.root.join(segment));
            }
        }
        Err(anyhow::anyhow!("unknown logical name: {}", logical))
    }

    pub fn logical_names(&self) -> Vec<&'static str> {
        LOGICAL.iter().map(|(name, _)| *name).collect()
    }

    /// 用户给出的相对路径必须落在已登记的逻辑目录内。
    pub fn resolve_relative(&self, logical: &str, rel: &str) -> anyhow::Result<PathBuf> {
        let base = self.resolve(logical)?;
        crate::core::robust::safe_join(&base, rel)
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


    #[test]
    fn user_relative_path_cannot_escape_logical_dir() {
        let r = PathResolver::new("KCU");
        assert_eq!(
            r.resolve_relative("instances", "alpha/mods").unwrap(),
            PathBuf::from("KCU/instances/alpha/mods")
        );
        assert!(r.resolve_relative("instances", "../../Windows").is_err());
        assert!(r.resolve_relative("instances", "/abs").is_err());
        assert!(r.resolve_relative("instances", "CON").is_err());
        assert!(r.resolve_relative("unknown", "x").is_err());
    }
}

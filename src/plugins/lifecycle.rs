use anyhow::{anyhow, Result};
use crossbeam_utils::sync::WaitGroup;
use crossbeam_utils::thread;
use libloading::Library;
use std::path::{Path, PathBuf};

use crate::plugins::abi::{compatible, open, read_abi, AbiVerdict, ABI_MAJOR};

#[derive(Debug)]
struct Loaded {
    id: String,
    library: Library,
}

#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct UnloadReport {
    pub unloaded: Vec<String>,
    pub errors: Vec<(String, String)>,
}

#[derive(Debug, Default)]
pub struct PluginSet {
    loaded: Vec<Loaded>,
}

impl PluginSet {
    pub fn new() -> Self {
        Self::default()
    }

    pub fn len(&self) -> usize {
        self.loaded.len()
    }

    pub fn is_empty(&self) -> bool {
        self.loaded.is_empty()
    }

    pub fn active_ids(&self) -> Vec<String> {
        self.loaded.iter().map(|x| x.id.clone()).collect()
    }

    pub fn push(&mut self, id: &str, path: &Path) -> Result<()> {
        if self.loaded.iter().any(|x| x.id == id) {
            return Err(anyhow!("duplicate plugin id: {}", id));
        }
        let library = open(path)?;
        let verdict = compatible(read_abi(&library)?);
        match verdict {
            AbiVerdict::Compatible(_) => {
                self.loaded.push(Loaded { id: id.to_string(), library });
                Ok(())
            }
            other => Err(anyhow!("ABI rejected: {:?}", other)),
        }
    }

    pub fn load_many(&mut self, entries: &[(String, PathBuf)]) -> Result<usize> {
        let base = self.loaded.len();
        let mut added = 0usize;
        for (id, path) in entries {
            if let Err(e) = self.push(id, path) {
                self.rollback_to(base);
                return Err(anyhow!("load_many aborted at {}: {}", id, e));
            }
            added += 1;
        }
        Ok(added)
    }

    fn rollback_to(&mut self, base: usize) {
        while self.loaded.len() > base {
            if let Some(item) = self.loaded.pop() {
                let _ = item.library.close();
            }
        }
    }

    pub fn probe_scoped(&self) -> usize {
        let wg = WaitGroup::new();
        let ok = thread::scope(|s| {
            let mut handles = Vec::new();
            for item in &self.loaded {
                let w = wg.clone();
                let lib = &item.library;
                handles.push(s.spawn(move |_| {
                    let _w = w;
                    matches!(read_abi(lib), Ok(a) if a.major == ABI_MAJOR)
                }));
            }
            handles
                .into_iter()
                .filter_map(|h| h.join().ok())
                .filter(|ok| *ok)
                .count()
        });
        wg.wait();
        ok.unwrap_or(0)
    }

    pub fn unload_all(&mut self) -> UnloadReport {
        let mut report = UnloadReport::default();
        while let Some(item) = self.loaded.pop() {
            match item.library.close() {
                Ok(()) => report.unloaded.push(item.id),
                Err(e) => {
                    report.errors.push((item.id.clone(), e.to_string()));
                    report.unloaded.push(item.id);
                }
            }
        }
        report
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn empty_set_reports_zero() {
        let mut s = PluginSet::new();
        assert!(s.is_empty());
        assert_eq!(s.len(), 0);
        assert_eq!(s.probe_scoped(), 0);
        assert_eq!(s.unload_all(), UnloadReport::default());
    }

    #[test]
    fn missing_path_returns_error_without_panic() {
        let mut s = PluginSet::new();
        let e = s.push("x", Path::new("/definitely/not/here/plugin.so")).unwrap_err();
        assert!(e.to_string().contains("plugin library load failed"));
        assert!(s.is_empty());
    }

    #[test]
    fn load_many_empty_input_is_noop() {
        let mut s = PluginSet::new();
        assert_eq!(s.load_many(&[]).unwrap(), 0);
        assert!(s.is_empty());
    }

    #[test]
    fn unload_report_default_has_no_errors() {
        let r = UnloadReport::default();
        assert!(r.unloaded.is_empty());
        assert!(r.errors.is_empty());
    }
}

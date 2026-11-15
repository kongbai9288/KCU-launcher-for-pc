use anyhow::{anyhow, Result};
use libloading::{Library, Symbol};
use std::path::Path;

pub const ABI_MAJOR: u32 = 1;
pub const ABI_MINOR: u32 = 0;

pub const SYM_ABI_MAJOR: &[u8] = b"kcu_plugin_abi_major\0";
pub const SYM_ABI_MINOR: &[u8] = b"kcu_plugin_abi_minor\0";
pub const SYM_INIT: &[u8] = b"kcu_plugin_init\0";

type AbiFn = unsafe extern "C" fn() -> u32;
type InitFn = unsafe extern "C" fn() -> i32;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct PluginAbi {
    pub major: u32,
    pub minor: u32,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AbiVerdict {
    Compatible(PluginAbi),
    RejectMajor { found: u32, host: u32 },
    RejectMinor { found: u32, host: u32 },
}

pub fn compatible(abi: PluginAbi) -> AbiVerdict {
    if abi.major != ABI_MAJOR {
        return AbiVerdict::RejectMajor { found: abi.major, host: ABI_MAJOR };
    }
    if abi.minor > ABI_MINOR {
        return AbiVerdict::RejectMinor { found: abi.minor, host: ABI_MINOR };
    }
    AbiVerdict::Compatible(abi)
}

pub fn open(path: &Path) -> Result<Library> {
    unsafe { Library::new(path) }.map_err(|e| anyhow!("plugin library load failed: {}", e))
}

pub fn read_abi(lib: &Library) -> Result<PluginAbi> {
    unsafe {
        let major: Symbol<AbiFn> = lib
            .get(SYM_ABI_MAJOR)
            .map_err(|e| anyhow!("missing kcu_plugin_abi_major: {}", e))?;
        let minor: Symbol<AbiFn> = lib
            .get(SYM_ABI_MINOR)
            .map_err(|e| anyhow!("missing kcu_plugin_abi_minor: {}", e))?;
        Ok(PluginAbi { major: major(), minor: minor() })
    }
}

pub fn read_init(lib: &Library) -> Option<i32> {
    unsafe { lib.get::<InitFn>(SYM_INIT).ok().map(|f| f()) }
}

pub fn check(path: &Path) -> Result<AbiVerdict> {
    let lib = open(path)?;
    let abi = read_abi(&lib)?;
    Ok(compatible(abi))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn exact_host_version_is_compatible() {
        assert_eq!(compatible(PluginAbi { major: 1, minor: 0 }),
                   AbiVerdict::Compatible(PluginAbi { major: 1, minor: 0 }));
    }

    #[test]
    fn host_constants_and_symbol_names_are_nul_terminated() {
        assert_eq!(ABI_MAJOR, 1);
        assert_eq!(ABI_MINOR, 0);
        for s in [SYM_ABI_MAJOR, SYM_ABI_MINOR, SYM_INIT] {
            assert_eq!(s.last(), Some(&0));
        }
    }

    #[test]
    fn newer_minor_is_rejected() {
        assert_eq!(compatible(PluginAbi { major: 1, minor: 1 }),
                   AbiVerdict::RejectMinor { found: 1, host: 0 });
    }

    #[test]
    fn different_major_is_rejected_before_minor() {
        assert_eq!(compatible(PluginAbi { major: 2, minor: 99 }),
                   AbiVerdict::RejectMajor { found: 2, host: 1 });
        assert_eq!(compatible(PluginAbi { major: 0, minor: 0 }),
                   AbiVerdict::RejectMajor { found: 0, host: 1 });
    }

    #[test]
    fn missing_library_returns_error_not_panic() {
        assert!(check(Path::new("/definitely/not/here/kcu-plugin.so")).is_err());
    }
}

use kcu_core::plugins::abi::{
    check, compatible, open, read_abi, read_init, AbiVerdict, PluginAbi, ABI_MINOR,
};
use std::path::PathBuf;
use std::process::Command;

fn fixture(name: &str, major: u32, minor: u32, with_init: bool) -> PathBuf {
    let dir = std::env::temp_dir().join(format!("kcu-abi-{}-{}", std::process::id(), name));
    std::fs::create_dir_all(&dir).unwrap();
    let src = dir.join("fixture.rs");
    let body = format!(
        "#[no_mangle] pub extern \"C\" fn kcu_plugin_abi_major() -> u32 {{ {m} }}\n\
         #[no_mangle] pub extern \"C\" fn kcu_plugin_abi_minor() -> u32 {{ {n} }}\n{init}",
        m = major,
        n = minor,
        init = if with_init {
            "#[no_mangle] pub extern \"C\" fn kcu_plugin_init() -> i32 { 0 }\n"
        } else {
            ""
        }
    );
    std::fs::write(&src, body).unwrap();
    let out = dir.join(format!(
        "{}kcu_fixture_{}{}",
        std::env::consts::DLL_PREFIX,
        name,
        std::env::consts::DLL_SUFFIX
    ));
    let rustc = std::env::var("RUSTC").unwrap_or_else(|_| "rustc".to_string());
    let status = Command::new(rustc)
        .args(["--edition", "2021", "--crate-type", "cdylib", "-O", "-o"])
        .arg(&out)
        .arg(&src)
        .status()
        .unwrap();
    assert!(status.success(), "fixture compile failed: {}", name);
    out
}

#[test]
fn library_loads_and_abi_is_compatible() {
    let path = fixture("ok", 1, 0, true);
    let lib = open(&path).unwrap();
    assert_eq!(read_abi(&lib).unwrap(), PluginAbi { major: 1, minor: 0 });
    assert_eq!(read_init(&lib), Some(0));
    assert_eq!(check(&path).unwrap(), AbiVerdict::Compatible(PluginAbi { major: 1, minor: 0 }));
}

#[test]
fn newer_major_is_rejected() {
    let path = fixture("major2", 2, 0, false);
    assert_eq!(check(&path).unwrap(), AbiVerdict::RejectMajor { found: 2, host: 1 });
}

#[test]
fn newer_minor_is_rejected_with_host_bound() {
    let path = fixture("minor99", 1, ABI_MINOR + 1, false);
    assert_eq!(check(&path).unwrap(),
               AbiVerdict::RejectMinor { found: ABI_MINOR + 1, host: ABI_MINOR });
}

#[test]
fn missing_init_symbol_is_optional() {
    let path = fixture("noinit", 1, 0, false);
    let lib = open(&path).unwrap();
    assert_eq!(read_init(&lib), None);
}

#[test]
fn missing_abi_symbol_returns_error() {
    let dir = std::env::temp_dir().join(format!("kcu-abi-{}-bare", std::process::id()));
    std::fs::create_dir_all(&dir).unwrap();
    let src = dir.join("fixture.rs");
    std::fs::write(&src, "#[no_mangle] pub extern \"C\" fn kcu_plugin_abi_major() -> u32 { 1 }\n").unwrap();
    let out = dir.join(format!("{}kcu_bare{}", std::env::consts::DLL_PREFIX, std::env::consts::DLL_SUFFIX));
    let rustc = std::env::var("RUSTC").unwrap_or_else(|_| "rustc".to_string());
    let status = Command::new(rustc)
        .args(["--edition", "2021", "--crate-type", "cdylib", "-O", "-o"])
        .arg(&out).arg(&src).status().unwrap();
    assert!(status.success());
    assert!(open(&out).is_ok());
    assert!(check(&out).is_err());
}

#[test]
fn verdict_helper_matches_check_on_loaded_abi() {
    let path = fixture("match", 1, 0, true);
    let lib = open(&path).unwrap();
    let abi = read_abi(&lib).unwrap();
    assert_eq!(compatible(abi), check(&path).unwrap());
}

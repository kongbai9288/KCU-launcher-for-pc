use kcu_core::plugins::lifecycle::PluginSet;
use std::path::PathBuf;
use std::process::Command;
use std::sync::OnceLock;

static FIXTURES: OnceLock<(PathBuf, PathBuf)> = OnceLock::new();

fn fixture(name: &str, major: u32) -> PathBuf {
    let dir = std::env::temp_dir().join(format!("kcu-lifecycle-{}-{}", std::process::id(), name));
    std::fs::create_dir_all(&dir).unwrap();
    let src = dir.join("fixture.rs");
    std::fs::write(
        &src,
        format!(
            "#[no_mangle] pub extern \"C\" fn kcu_plugin_abi_major() -> u32 {{ {m} }}\n\
             #[no_mangle] pub extern \"C\" fn kcu_plugin_abi_minor() -> u32 {{ 0 }}\n\
             #[no_mangle] pub extern \"C\" fn kcu_plugin_init() -> i32 {{ 0 }}\n",
            m = major
        ),
    )
    .unwrap();
    let out = dir.join(format!(
        "{}kcu_lifecycle_{}{}",
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

fn libs() -> &'static (PathBuf, PathBuf) {
    FIXTURES.get_or_init(|| (fixture("ok", 1), fixture("bad", 2)))
}

fn ok() -> &'static PathBuf {
    &libs().0
}

fn bad() -> &'static PathBuf {
    &libs().1
}

fn entries(ids: &[&str]) -> Vec<(String, PathBuf)> {
    ids.iter().map(|id| (id.to_string(), ok().clone())).collect()
}

#[test]
fn three_libraries_unload_in_reverse_order() {
    let mut s = PluginSet::new();
    assert_eq!(s.load_many(&entries(&["a", "b", "c"])).unwrap(), 3);
    assert_eq!(s.active_ids(), vec!["a", "b", "c"]);
    let r = s.unload_all();
    assert_eq!(r.unloaded, vec!["c", "b", "a"]);
    assert!(r.errors.is_empty());
    assert!(s.is_empty());
}

#[test]
fn probe_scoped_reads_real_symbols_and_joins() {
    let mut s = PluginSet::new();
    s.load_many(&entries(&["x", "y", "z"])).unwrap();
    assert_eq!(s.probe_scoped(), 3);
    assert_eq!(s.active_ids().len(), 3);
    s.unload_all();
}

#[test]
fn duplicate_id_is_rejected_without_extra_handle() {
    let mut s = PluginSet::new();
    s.push("only", ok()).unwrap();
    let e = s.push("only", ok()).unwrap_err();
    assert!(e.to_string().contains("duplicate plugin id"));
    assert_eq!(s.len(), 1);
    assert_eq!(s.unload_all().unloaded, vec!["only"]);
}

#[test]
fn abi_mismatch_rolls_back_only_new_entries() {
    let mut s = PluginSet::new();
    s.push("preexisting", ok()).unwrap();

    let mut batch = entries(&["new1", "new2"]);
    batch.push(("broken".into(), bad().clone()));
    let e = s.load_many(&batch).unwrap_err();
    assert!(e.to_string().contains("load_many aborted at broken"));

    assert_eq!(s.len(), 1);
    assert_eq!(s.active_ids(), vec!["preexisting"]);
    assert_eq!(s.probe_scoped(), 1);
}

#[test]
fn unload_twice_is_idempotent() {
    let mut s = PluginSet::new();
    s.load_many(&entries(&["p", "q"])).unwrap();
    let first = s.unload_all();
    let second = s.unload_all();
    assert_eq!(first.unloaded, vec!["q", "p"]);
    assert_eq!(second, Default::default());
}

#[test]
fn after_unload_probe_is_zero_and_ids_empty() {
    let mut s = PluginSet::new();
    s.load_many(&entries(&["m", "n"])).unwrap();
    s.unload_all();
    assert_eq!(s.probe_scoped(), 0);
    assert!(s.active_ids().is_empty());
    assert!(s.is_empty());
}

#[test]
fn missing_path_in_batch_rolls_back_without_panic() {
    let mut s = PluginSet::new();
    s.push("keep", ok()).unwrap();
    let mut batch = entries(&["temp1", "temp2"]);
    batch.push(("gone".into(), PathBuf::from("/definitely/not/here.so")));
    assert!(s.load_many(&batch).is_err());
    assert_eq!(s.active_ids(), vec!["keep"]);
}

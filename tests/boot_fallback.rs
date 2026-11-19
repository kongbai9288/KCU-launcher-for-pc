use kcu_core::core::boot::{BootState, BUNDLE_FILE, STATE_FILE};
use kcu_core::dispatcher::{DispatchInput, Dispatcher, FAILURE_THRESHOLD};
use kcu_core::CancelToken;
use serde_json::{from_str, Value};
use std::fs;
use std::path::Path;
use std::sync::atomic::{AtomicUsize, Ordering};

static SEQ: AtomicUsize = AtomicUsize::new(0);

fn tmp() -> String {
    let n = SEQ.fetch_add(1, Ordering::SeqCst);
    std::env::temp_dir()
        .join(format!("kcu057-it-{}-{}", std::process::id(), n))
        .to_string_lossy()
        .into_owned()
}

fn failing_input(dir: Option<String>) -> DispatchInput {
    DispatchInput {
        config_text: Some("not-json{".to_string()),
        task_texts: Vec::new(),
        mem_bytes: 8 * 1024 * 1024 * 1024,
        export_dir: dir,
        ..DispatchInput::default()
    }
}

fn run_until_bundle(d: &mut Dispatcher, input: &DispatchInput) -> Option<String> {
    let cancel = CancelToken::new();
    let mut last = None;
    for _ in 0..=(FAILURE_THRESHOLD + 1) {
        let o = d.dispatch(input, &cancel);
        last = o.bundle_path;
    }
    last
}

#[test]
fn safe_mode_failure_exports_real_four_sections() {
    let dir = tmp();
    let mut d = Dispatcher::default();
    let input = failing_input(Some(dir.clone()));
    let path = run_until_bundle(&mut d, &input);
    assert!(path.is_some(), "bundle_path must be set after safe-mode failure");
    let p = path.unwrap();
    let text = fs::read_to_string(&p).expect("bundle readable");
    let v: Value = from_str(&text).expect("bundle json");
    assert_eq!(v["schema"], 1);
    assert!(v["lines"].as_array().expect("lines array").len() >= 4);
    assert_eq!(v["config_snapshot"], "not-json{");
    assert!(v["runtime"].as_str().expect("runtime").contains("mem="));
    assert!(v["modules"].as_array().expect("modules").len() >= 20);
    assert_eq!(Path::new(&p).file_name().unwrap().to_string_lossy(), BUNDLE_FILE);
    fs::remove_dir_all(&dir).ok();
}

#[test]
fn no_export_dir_is_visible_not_silent() {
    let mut d = Dispatcher::default();
    let input = failing_input(None);
    let cancel = CancelToken::new();
    let mut last = None;
    let mut seen_skip = false;
    for _ in 0..=(FAILURE_THRESHOLD + 1) {
        let o = d.dispatch(&input, &cancel);
        last = o.bundle_path;
        if o.diagnostics.iter().any(|x| x.contains("no_export_dir")) {
            seen_skip = true;
        }
    }
    assert!(last.is_none());
    assert!(seen_skip, "missing dir must produce a visible diagnostic line");
}

#[test]
fn deleted_state_file_recovers() {
    let dir = tmp();
    let (a, _) = BootState::open(Some(&dir));
    a.record(true);
    assert_eq!(a.consecutive_failures(), 1);
    fs::remove_file(Path::new(&dir).join(STATE_FILE)).ok();
    let (b, diagnostics) = BootState::open(Some(&dir));
    assert_eq!(b.consecutive_failures(), 0);
    assert!(diagnostics.iter().any(|x| x.contains("fallback_default")));
    fs::remove_dir_all(&dir).ok();
}

#[test]
fn deleted_bundle_is_reexported() {
    let dir = tmp();
    let mut d = Dispatcher::default();
    let input = failing_input(Some(dir.clone()));
    let first = run_until_bundle(&mut d, &input).expect("first export");
    fs::remove_file(&first).ok();
    let cancel = CancelToken::new();
    let o = d.dispatch(&input, &cancel);
    assert!(o.bundle_path.is_some());
    assert!(Path::new(&first).is_file());
    fs::remove_dir_all(&dir).ok();
}

#[test]
fn malformed_state_recovers_and_persists_again() {
    let dir = tmp();
    fs::create_dir_all(&dir).ok();
    fs::write(Path::new(&dir).join(STATE_FILE), "{\"schema\":9}").ok();
    let (a, diagnostics) = BootState::open(Some(&dir));
    assert_eq!(a.consecutive_failures(), 0);
    assert!(diagnostics.iter().any(|x| x.contains("state schema")));
    a.record(true);
    let (b, _) = BootState::open(Some(&dir));
    assert_eq!(b.consecutive_failures(), 1);
    fs::remove_dir_all(&dir).ok();
}

#[test]
fn concurrent_records_do_not_panic_and_do_not_overflow() {
    let dir = tmp();
    let (s, _) = BootState::open(Some(&dir));
    let shared = &s;
    crossbeam_utils::thread::scope(|scope| {
        for _ in 0..8 {
            scope.spawn(move |_| {
                for _ in 0..8 {
                    shared.record(true);
                }
            });
        }
    })
    .expect("scope join");
    let n = s.consecutive_failures();
    assert!(n <= 64, "unexpected count {}", n);
    fs::remove_dir_all(&dir).ok();
}

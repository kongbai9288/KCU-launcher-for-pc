use kcu_core::core::stats::{PlayStats, MAX_CONCURRENT_SESSIONS, MAX_SESSION_SECONDS, STATS_FILE};
use kcu_core::dispatcher::Dispatcher;
use serde_json::{from_str, Value};
use std::fs;
use std::path::PathBuf;
use std::sync::atomic::{AtomicUsize, Ordering};

static SEQ: AtomicUsize = AtomicUsize::new(0);

fn tmp() -> String {
    let n = SEQ.fetch_add(1, Ordering::SeqCst);
    std::env::temp_dir()
        .join(format!("kcu061-it-{}-{}", std::process::id(), n))
        .to_string_lossy()
        .into_owned()
}

fn file(dir: &str) -> PathBuf {
    PathBuf::from(dir).join(STATS_FILE)
}

fn read_json(dir: &str) -> Value {
    from_str(&fs::read_to_string(file(dir)).unwrap()).unwrap()
}

#[test]
fn persists_real_json_and_survives_reopen() {
    let dir = tmp();
    let _ = fs::remove_dir_all(&dir);
    let (s, _) = PlayStats::open(Some(&dir));
    assert!(s.record("alpha", 0, 120, false).accepted);
    assert!(s.record("beta", 0, 30, true).accepted);

    let v = read_json(&dir);
    assert_eq!(v["schema"].as_u64(), Some(1));
    assert_eq!(v["total_seconds"].as_u64(), Some(150));
    assert_eq!(v["instances"]["alpha"].as_u64(), Some(120));
    assert_eq!(v["instances"]["beta"].as_u64(), Some(30));

    let (s2, _) = PlayStats::open(Some(&dir));
    let (total, map) = s2.totals();
    assert_eq!(total, 150);
    assert_eq!(map.get("alpha"), Some(&120));
    assert_eq!(map.get("beta"), Some(&30));
    let _ = fs::remove_dir_all(&dir);
}

#[test]
fn deleted_file_falls_back_and_next_record_restores() {
    let dir = tmp();
    let _ = fs::remove_dir_all(&dir);
    let (s, _) = PlayStats::open(Some(&dir));
    s.record("alpha", 0, 42, false);
    assert!(file(&dir).is_file());

    fs::remove_file(file(&dir)).unwrap();
    let (s2, d2) = PlayStats::open(Some(&dir));
    assert_eq!(s2.totals().0, 0);
    assert!(d2.iter().any(|x| x.contains("fallback_default")));

    assert!(s2.record("beta", 0, 8, false).accepted);
    assert!(file(&dir).is_file());
    assert_eq!(read_json(&dir)["total_seconds"].as_u64(), Some(8));
    let _ = fs::remove_dir_all(&dir);
}

#[test]
fn malformed_wrong_schema_and_oversized_files_all_fall_back() {
    let dir = tmp();
    let _ = fs::remove_dir_all(&dir);
    fs::create_dir_all(&dir).unwrap();

    let cases = [
        "{bad".to_string(),
        r#"{"schema":9,"total_seconds":7,"instances":{}}"#.to_string(),
        "x".repeat(64 * 1024 + 1),
    ];
    for body in &cases {
        fs::write(file(&dir), body).unwrap();
        let (s, d) = PlayStats::open(Some(&dir));
        assert_eq!(s.totals().0, 0);
        assert!(d.iter().any(|x| x.contains("ERROR")), "{}", body.len());
    }

    let (s, _) = PlayStats::open(Some(&dir));
    assert!(s.record("alpha", 0, 5, false).accepted);
    assert_eq!(read_json(&dir)["total_seconds"].as_u64(), Some(5));
    let _ = fs::remove_dir_all(&dir);
}

#[test]
fn dispatcher_finish_session_records_and_emits_diagnostics() {
    let mut d = Dispatcher::default();
    let (s, _) = PlayStats::open(None);

    let o = d.finish_session(&s, "alpha", 0, 45, false);
    assert!(o.accepted);
    assert_eq!(o.played_seconds, 45);
    assert_eq!(o.total_seconds, 45);
    assert!(o.show_popup);

    let silent = d.finish_session(&s, "alpha", 100, 155, true);
    assert!(silent.accepted);
    assert!(silent.silent);
    assert!(!silent.show_popup);
    assert_eq!(silent.total_seconds, 100);
    assert_eq!(s.totals().0, 100);

    let shards = d.flush_diagnostics();
    let flat: Vec<&String> = shards.iter().flatten().collect();
    assert!(flat.iter().any(|x| x.contains("core stats session OK")));
    assert!(flat.iter().all(|x| x.starts_with("[KCU] ")));
}

#[test]
fn concurrent_sessions_are_capped_and_concurrent_records_are_exact() {
    let (s, _) = PlayStats::open(None);
    let ids: Vec<u64> = (0..MAX_CONCURRENT_SESSIONS)
        .map(|i| s.start(&format!("i{}", i), 0).0.unwrap())
        .collect();
    assert_eq!(s.active_count(), MAX_CONCURRENT_SESSIONS);
    let (extra, diag) = s.start("overflow", 0);
    assert!(extra.is_none());
    assert!(diag.iter().any(|x| x.contains("concurrent_limit")));
    for id in ids {
        assert!(s.end(id, 60, false).accepted);
    }
    assert_eq!(s.active_count(), 0);
    assert_eq!(s.totals().0, 180);

    let accepted = AtomicUsize::new(0);
    let (s2, _) = PlayStats::open(None);
    std::thread::scope(|scope| {
        for _ in 0..8 {
            scope.spawn(|| {
                for _ in 0..8 {
                    if s2.record("shared", 0, 10, false).accepted {
                        accepted.fetch_add(1, Ordering::SeqCst);
                    }
                }
            });
        }
    });
    assert_eq!(s2.totals().1.get("shared").copied(), Some(accepted.load(Ordering::SeqCst) as u64 * 10));
    assert_eq!(s2.totals().0, s2.totals().1.get("shared").copied().unwrap());
}

#[test]
fn silent_quick_launch_writes_data_without_popup() {
    let dir = tmp();
    let _ = fs::remove_dir_all(&dir);
    let (s, _) = PlayStats::open(Some(&dir));
    let o = s.record("quick", 0, 75, true);
    assert!(o.accepted);
    assert!(!o.show_popup);
    assert_eq!(read_json(&dir)["instances"]["quick"].as_u64(), Some(75));
    let _ = fs::remove_dir_all(&dir);
}

#[test]
fn clock_rollback_and_oversized_session_are_bounded_end_to_end() {
    let dir = tmp();
    let _ = fs::remove_dir_all(&dir);
    let (s, _) = PlayStats::open(Some(&dir));
    let back = s.record("alpha", 900, 100, false);
    assert_eq!(back.played_seconds, 0);
    assert!(back.diagnostics.iter().any(|x| x.contains("clock_rollback")));
    let big = s.record("alpha", 0, MAX_SESSION_SECONDS + 5000, false);
    assert_eq!(big.played_seconds, MAX_SESSION_SECONDS);
    assert!(big.diagnostics.iter().any(|x| x.contains("session_clamped")));
    assert_eq!(read_json(&dir)["total_seconds"].as_u64(), Some(MAX_SESSION_SECONDS));
    let _ = fs::remove_dir_all(&dir);
}

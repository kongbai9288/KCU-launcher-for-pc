use crate::core::diagnostics::diag_line;
use crate::core::robust::{self, OpBudget};
use anyhow::{anyhow, Result};
use serde_json::{from_str, json, to_string, Value};
use std::collections::BTreeMap;
use std::fs;
use std::path::PathBuf;
use std::sync::atomic::{AtomicU64, Ordering};
use std::sync::{Mutex, MutexGuard, PoisonError};

pub const STATS_FILE: &str = "play-stats.json";
pub const DEFAULT_STATS: &str = r#"{"schema":1,"total_seconds":0,"instances":{}}"#;
pub const MAX_STATS_BYTES: usize = 64 * 1024;
pub const MAX_DIR_BYTES: usize = 1024;
pub const MAX_SESSION_SECONDS: u64 = 30 * 24 * 3600;
pub const MAX_INSTANCES: usize = 4096;
pub const MAX_CONCURRENT_SESSIONS: usize = 3;

/// Per-session result. `show_popup` is false for silent (quick-launch) records.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SessionOutcome {
    pub played_seconds: u64,
    pub total_seconds: u64,
    pub instance_seconds: u64,
    pub silent: bool,
    pub show_popup: bool,
    pub accepted: bool,
    pub diagnostics: Vec<String>,
}

struct ActiveSession {
    instance: String,
    started: u64,
}

pub struct PlayStats {
    root: Option<PathBuf>,
    total: Mutex<u64>,
    instances: Mutex<BTreeMap<String, u64>>,
    active: Mutex<BTreeMap<u64, ActiveSession>>,
    next_id: AtomicU64,
    budget: OpBudget,
}

impl PlayStats {
    pub fn open(dir: Option<&str>) -> (Self, Vec<String>) {
        let mut diagnostics = Vec::new();
        let root = match dir {
            Some(d) if !d.is_empty() => match validate_dir(d) {
                Ok(p) => Some(p),
                Err(e) => {
                    diagnostics.push(diag_line("core", "stats", "state_dir", "ERROR", &format!("detail={}", e)));
                    None
                }
            },
            Some(_) => {
                diagnostics.push(diag_line("core", "stats", "state_dir", "SKIP", "detail=empty_dir"));
                None
            }
            None => None,
        };

        let mut total = 0u64;
        let mut instances = BTreeMap::new();
        if let Some(ref r) = root {
            let path = match robust::safe_join(r, STATS_FILE) {
                Ok(p) => p,
                Err(e) => {
                    diagnostics.push(diag_line("core", "stats", "state_file", "ERROR", &format!("detail={}", e)));
                    r.join(STATS_FILE)
                }
            };
            let (text, used_fallback) = robust::read_or_default(&path, DEFAULT_STATS);
            if used_fallback {
                diagnostics.push(diag_line("core", "stats", "state_file", "OK", "detail=fallback_default"));
            }
            match parse_stats(&text) {
                Ok((t, m)) => {
                    total = t;
                    instances = m;
                }
                Err(e) => {
                    diagnostics.push(diag_line("core", "stats", "state_file", "ERROR", &format!("detail={}", e)));
                }
            }
        } else {
            diagnostics.push(diag_line("core", "stats", "state_file", "SKIP", "detail=in_memory"));
        }

        (
            Self {
                root,
                total: Mutex::new(total),
                instances: Mutex::new(instances),
                active: Mutex::new(BTreeMap::new()),
                next_id: AtomicU64::new(1),
                budget: OpBudget::new(robust::MAX_OPS_PER_WINDOW),
            },
            diagnostics,
        )
    }

    pub fn totals(&self) -> (u64, BTreeMap<String, u64>) {
        (*self.lock_total(), (*self.lock_instances()).clone())
    }

    pub fn active_count(&self) -> usize {
        self.lock_active().len()
    }

    /// Register a running game. Returns None when the concurrent limit is reached.
    pub fn start(&self, instance: &str, at: u64) -> (Option<u64>, Vec<String>) {
        let mut diagnostics = Vec::new();
        if let Err(e) = robust::check_text(instance, robust::MAX_ID_BYTES) {
            diagnostics.push(diag_line("core", "stats", "start", "ERROR", &format!("detail={}", e)));
            return (None, diagnostics);
        }
        let mut active = self.lock_active();
        if active.len() >= MAX_CONCURRENT_SESSIONS {
            diagnostics.push(diag_line("core", "stats", "start", "DENY", "detail=concurrent_limit"));
            return (None, diagnostics);
        }
        let id = self.next_id.fetch_add(1, Ordering::SeqCst);
        active.insert(id, ActiveSession { instance: instance.to_string(), started: at });
        diagnostics.push(diag_line("core", "stats", "start", "OK", &format!("detail=id={} active={}", id, active.len())));
        (Some(id), diagnostics)
    }

    /// Close a registered session and accumulate its duration.
    pub fn end(&self, session_id: u64, ended: u64, silent: bool) -> SessionOutcome {
        if !self.budget.try_op() {
            return denied(self.snapshot(), silent, "rate_limited");
        }
        let removed = self.lock_active().remove(&session_id);
        let Some(s) = removed else {
            return denied(self.snapshot(), silent, "unknown_session");
        };
        self.record_inner(&s.instance, s.started, ended, silent)
    }

    /// Accumulate a duration without a start/end pair.
    pub fn record(&self, instance: &str, started: u64, ended: u64, silent: bool) -> SessionOutcome {
        if !self.budget.try_op() {
            return denied(self.snapshot(), silent, "rate_limited");
        }
        self.record_inner(instance, started, ended, silent)
    }

    fn record_inner(&self, instance: &str, started: u64, ended: u64, silent: bool) -> SessionOutcome {
        let mut diagnostics = Vec::new();
        if let Err(e) = robust::check_text(instance, robust::MAX_ID_BYTES) {
            diagnostics.push(diag_line("core", "stats", "session", "ERROR", &format!("detail={}", e)));
            return denied_with(self.snapshot(), silent, diagnostics);
        }

        let mut played = ended.saturating_sub(started);
        if ended < started {
            diagnostics.push(diag_line("core", "stats", "session", "DEGRADE", "detail=clock_rollback"));
        }
        if played > MAX_SESSION_SECONDS {
            played = MAX_SESSION_SECONDS;
            diagnostics.push(diag_line("core", "stats", "session", "DEGRADE", "detail=session_clamped"));
        }

        let mut total = self.lock_total();
        let mut instances = self.lock_instances();
        if !instances.contains_key(instance) && instances.len() >= MAX_INSTANCES {
            diagnostics.push(diag_line("core", "stats", "session", "DENY", "detail=instance_limit"));
            return denied_with(self.snapshot_unlocked(&total, &instances), silent, diagnostics);
        }

        let next_total = total.saturating_add(played);
        let next_instance = instances.get(instance).copied().unwrap_or(0).saturating_add(played);
        *total = next_total;
        instances.insert(instance.to_string(), next_instance);
        diagnostics.extend(self.persist(next_total, &instances));
        diagnostics.push(diag_line(
            "core",
            "stats",
            "session",
            "OK",
            &format!("detail=played={} total={} instance={} silent={}", played, next_total, next_instance, if silent { 1 } else { 0 }),
        ));

        SessionOutcome {
            played_seconds: played,
            total_seconds: next_total,
            instance_seconds: next_instance,
            silent,
            show_popup: !silent,
            accepted: true,
            diagnostics,
        }
    }

    fn snapshot(&self) -> (u64, BTreeMap<String, u64>) {
        self.totals()
    }

    fn snapshot_unlocked(&self, total: &u64, instances: &BTreeMap<String, u64>) -> (u64, BTreeMap<String, u64>) {
        (*total, instances.clone())
    }

    fn persist(&self, total: u64, instances: &BTreeMap<String, u64>) -> Vec<String> {
        let mut diagnostics = Vec::new();
        let Some(ref root) = self.root else {
            diagnostics.push(diag_line("core", "stats", "state_write", "SKIP", "detail=in_memory"));
            return diagnostics;
        };

        let mut im = serde_json::Map::new();
        for (k, v) in instances {
            im.insert(k.clone(), json!(*v));
        }
        let mut obj = serde_json::Map::new();
        obj.insert("schema".to_string(), json!(1));
        obj.insert("total_seconds".to_string(), json!(total));
        obj.insert("instances".to_string(), Value::Object(im));
        let body = match to_string(&Value::Object(obj)) {
            Ok(s) => s,
            Err(e) => {
                diagnostics.push(diag_line("core", "stats", "state_write", "ERROR", &format!("detail={}", e)));
                return diagnostics;
            }
        };

        let path = match robust::safe_join(root, STATS_FILE) {
            Ok(p) => p,
            Err(e) => {
                diagnostics.push(diag_line("core", "stats", "state_write", "ERROR", &format!("detail={}", e)));
                return diagnostics;
            }
        };
        match fs::create_dir_all(root).and_then(|_| fs::write(&path, body.as_bytes())) {
            Ok(()) => diagnostics.push(diag_line("core", "stats", "state_write", "OK", &format!("detail=bytes={}", body.len()))),
            Err(e) => diagnostics.push(diag_line("core", "stats", "state_write", "ERROR", &format!("detail={:?}", e.kind()))),
        }
        diagnostics
    }

    fn lock_total(&self) -> MutexGuard<'_, u64> {
        self.total.lock().unwrap_or_else(PoisonError::into_inner)
    }

    fn lock_instances(&self) -> MutexGuard<'_, BTreeMap<String, u64>> {
        self.instances.lock().unwrap_or_else(PoisonError::into_inner)
    }

    fn lock_active(&self) -> MutexGuard<'_, BTreeMap<u64, ActiveSession>> {
        self.active.lock().unwrap_or_else(PoisonError::into_inner)
    }
}

fn denied(snap: (u64, BTreeMap<String, u64>), silent: bool, reason: &str) -> SessionOutcome {
    denied_with(snap, silent, vec![diag_line("core", "stats", "session", "DENY", &format!("detail={}", reason))])
}

fn denied_with(snap: (u64, BTreeMap<String, u64>), silent: bool, mut diagnostics: Vec<String>) -> SessionOutcome {
    let (total, _) = snap;
    diagnostics.push(diag_line("core", "stats", "session", "DENY", "detail=not_recorded"));
    SessionOutcome {
        played_seconds: 0,
        total_seconds: total,
        instance_seconds: 0,
        silent,
        show_popup: false,
        accepted: false,
        diagnostics,
    }
}

fn validate_dir(dir: &str) -> Result<PathBuf> {
    robust::check_text(dir, MAX_DIR_BYTES)?;
    if dir.bytes().any(|b| b == 0) {
        return Err(anyhow!("nul byte in dir"));
    }
    let p = PathBuf::from(dir);
    if p.as_os_str().is_empty() {
        return Err(anyhow!("empty dir"));
    }
    Ok(p)
}

fn parse_stats(text: &str) -> Result<(u64, BTreeMap<String, u64>)> {
    if text.len() > MAX_STATS_BYTES {
        return Err(anyhow!("stats oversized"));
    }
    let v: Value = from_str(text).map_err(|_| anyhow!("stats malformed"))?;
    if v.get("schema").and_then(Value::as_u64) != Some(1) {
        return Err(anyhow!("stats schema"));
    }
    let total = v
        .get("total_seconds")
        .and_then(Value::as_u64)
        .ok_or_else(|| anyhow!("total_seconds missing"))?;
    let obj = v
        .get("instances")
        .and_then(Value::as_object)
        .ok_or_else(|| anyhow!("instances missing"))?;
    if obj.len() > MAX_INSTANCES {
        return Err(anyhow!("too many instances"));
    }
    let mut out = BTreeMap::new();
    for (k, val) in obj {
        robust::check_text(k, robust::MAX_ID_BYTES)?;
        let n = val.as_u64().ok_or_else(|| anyhow!("instance value out of range"))?;
        out.insert(k.clone(), n);
    }
    Ok((total, out))
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::atomic::AtomicUsize;

    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> String {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        std::env::temp_dir()
            .join(format!("kcu061-{}-{}", std::process::id(), n))
            .to_string_lossy()
            .into_owned()
    }

    #[test]
    fn open_without_dir_uses_in_memory_defaults() {
        let (s, d) = PlayStats::open(None);
        assert_eq!(s.totals().0, 0);
        assert!(s.totals().1.is_empty());
        assert!(d.iter().any(|x| x.contains("in_memory")));
    }

    #[test]
    fn record_accumulates_single_total_and_per_instance() {
        let (s, _) = PlayStats::open(None);
        let a = s.record("alpha", 100, 160, false);
        assert_eq!(a.played_seconds, 60);
        assert_eq!(a.total_seconds, 60);
        assert_eq!(a.instance_seconds, 60);
        assert!(a.show_popup);
        let b = s.record("alpha", 200, 230, false);
        assert_eq!(b.total_seconds, 90);
        assert_eq!(b.instance_seconds, 90);
        let c = s.record("beta", 300, 310, false);
        assert_eq!(c.total_seconds, 100);
        assert_eq!(c.instance_seconds, 10);
        assert_eq!(s.totals().1.get("alpha"), Some(&90));
        assert_eq!(s.totals().1.get("beta"), Some(&10));
    }

    #[test]
    fn silent_record_keeps_data_but_suppresses_popup() {
        let (s, _) = PlayStats::open(None);
        let o = s.record("alpha", 10, 70, true);
        assert!(o.accepted);
        assert!(o.silent);
        assert!(!o.show_popup);
        assert_eq!(s.totals().0, 60);
    }

    #[test]
    fn clock_rollback_and_oversized_session_are_bounded() {
        let (s, _) = PlayStats::open(None);
        let back = s.record("alpha", 900, 100, false);
        assert_eq!(back.played_seconds, 0);
        assert!(back.diagnostics.iter().any(|x| x.contains("clock_rollback")));
        let big = s.record("alpha", 0, MAX_SESSION_SECONDS + 5000, false);
        assert_eq!(big.played_seconds, MAX_SESSION_SECONDS);
        assert!(big.diagnostics.iter().any(|x| x.contains("session_clamped")));
    }

    #[test]
    fn empty_or_control_character_instance_is_rejected() {
        let (s, _) = PlayStats::open(None);
        let a = s.record("", 0, 10, false);
        assert!(!a.accepted);
        let b = s.record("a\nb", 0, 10, false);
        assert!(!b.accepted);
        assert_eq!(s.totals().0, 0);
    }

    #[test]
    fn concurrent_sessions_are_capped_at_three() {
        let (s, _) = PlayStats::open(None);
        let ids: Vec<_> = (0..3).map(|i| s.start(&format!("i{}", i), 0).0.unwrap()).collect();
        assert_eq!(s.active_count(), 3);
        let (fourth, d) = s.start("i3", 0);
        assert!(fourth.is_none());
        assert!(d.iter().any(|x| x.contains("concurrent_limit")));
        for id in ids {
            let o = s.end(id, 30, false);
            assert!(o.accepted);
        }
        assert_eq!(s.active_count(), 0);
        assert_eq!(s.totals().0, 90);
    }

    #[test]
    fn unknown_session_is_not_recorded() {
        let (s, _) = PlayStats::open(None);
        let o = s.end(9999, 100, false);
        assert!(!o.accepted);
        assert!(o.diagnostics.iter().any(|x| x.contains("unknown_session")));
        assert_eq!(s.totals().0, 0);
    }

    #[test]
    fn rate_limit_does_not_drop_a_started_session() {
        let (s, _) = PlayStats::open(None);
        let id = s.start("alpha", 0).0.unwrap();
        let mut count = 0;
        for _ in 0..robust::MAX_OPS_PER_WINDOW + 5 {
            if s.record("flood", 0, 1, false).accepted {
                count += 1;
            }
        }
        assert!(count <= robust::MAX_OPS_PER_WINDOW);
        let o = s.end(id, 10, false);
        assert!(!o.accepted);
        assert!(o.diagnostics.iter().any(|x| x.contains("rate_limited")));
        assert_eq!(s.active_count(), 1);
    }

    #[test]
    fn deleted_file_falls_back_and_next_write_restores() {
        let dir = tmp();
        let _ = fs::remove_dir_all(&dir);
        let (s, _) = PlayStats::open(Some(&dir));
        let o = s.record("alpha", 0, 42, false);
        assert!(o.accepted);
        assert!(PathBuf::from(&dir).join(STATS_FILE).is_file());
        fs::remove_file(PathBuf::from(&dir).join(STATS_FILE)).unwrap();
        let (s2, d2) = PlayStats::open(Some(&dir));
        assert_eq!(s2.totals().0, 0);
        assert!(d2.iter().any(|x| x.contains("fallback_default")));
        let o2 = s2.record("beta", 0, 8, true);
        assert!(o2.accepted);
        assert!(PathBuf::from(&dir).join(STATS_FILE).is_file());
        let _ = fs::remove_dir_all(&dir);
    }

    #[test]
    fn malformed_and_wrong_schema_files_fall_back() {
        let dir = tmp();
        let _ = fs::remove_dir_all(&dir);
        fs::create_dir_all(&dir).unwrap();
        let path = PathBuf::from(&dir).join(STATS_FILE);
        fs::write(&path, "{bad").unwrap();
        let (s1, d1) = PlayStats::open(Some(&dir));
        assert_eq!(s1.totals().0, 0);
        assert!(d1.iter().any(|x| x.contains("malformed")));
        fs::write(&path, r#"{"schema":9,"total_seconds":7,"instances":{}}"#).unwrap();
        let (s2, d2) = PlayStats::open(Some(&dir));
        assert_eq!(s2.totals().0, 0);
        assert!(d2.iter().any(|x| x.contains("schema")));
        let _ = fs::remove_dir_all(&dir);
    }

    #[test]
    fn persisted_totals_survive_reopen() {
        let dir = tmp();
        let _ = fs::remove_dir_all(&dir);
        let (s, _) = PlayStats::open(Some(&dir));
        s.record("alpha", 0, 100, false);
        s.record("beta", 0, 50, true);
        let (s2, _) = PlayStats::open(Some(&dir));
        let (total, map) = s2.totals();
        assert_eq!(total, 150);
        assert_eq!(map.get("alpha"), Some(&100));
        assert_eq!(map.get("beta"), Some(&50));
        let _ = fs::remove_dir_all(&dir);
    }

    #[test]
    fn oversized_file_is_rejected() {
        let dir = tmp();
        let _ = fs::remove_dir_all(&dir);
        fs::create_dir_all(&dir).unwrap();
        let path = PathBuf::from(&dir).join(STATS_FILE);
        fs::write(&path, "x".repeat(MAX_STATS_BYTES + 1)).unwrap();
        let (s, d) = PlayStats::open(Some(&dir));
        assert_eq!(s.totals().0, 0);
        assert!(d.iter().any(|x| x.contains("oversized")));
        let _ = fs::remove_dir_all(&dir);
    }

    #[test]
    fn poisoned_locks_still_serve() {
        let (s, _) = PlayStats::open(None);
        let t = std::thread::scope(|scope| {
            let r = scope.spawn(|| {
                let _g = s.total.lock().unwrap();
                panic!("poison total");
            });
            assert!(r.join().is_err());
        });
        let _ = t;
        let o = s.record("alpha", 0, 5, false);
        assert!(o.accepted);
        assert_eq!(s.totals().0, 5);
    }

    #[test]
    fn diagnostics_are_single_line_kcu_prefixed() {
        let (s, _) = PlayStats::open(None);
        let o = s.record("alpha", 0, 10, false);
        for x in &o.diagnostics {
            assert!(x.starts_with("[KCU] "));
            assert!(!x.contains('\n'));
        }
    }
}

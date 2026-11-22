use crate::core::config::Config;
use crate::core::diagnostics::diag_line;
use crate::core::integrity::{DiagnosticBundle, Level, SAFE_MODE_AFTER};
use crate::core::robust::{self, OpBudget};
use anyhow::{anyhow, Result};
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::PathBuf;
use std::sync::atomic::{AtomicU32, Ordering};

pub const STATE_FILE: &str = "boot-state.json";
pub const BUNDLE_FILE: &str = "diagnostic-bundle.json";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"failures":0}"#;
pub const MAX_STATE_BYTES: usize = 4096;
pub const MAX_DIR_BYTES: usize = 1024;
pub const MAX_SNAPSHOT_BYTES: usize = 256 * 1024;
pub const MAX_RUNTIME_BYTES: usize = 16 * 1024;
pub const MAX_LINES: usize = 4096;
pub const MAX_MODULES: usize = 512;
pub const MAX_LINE_BYTES: usize = 4096;

pub const LOADED_MODULES: &[&str] = &[
    "core.envelope",
    "core.diagnostics",
    "core.paths",
    "core.config",
    "core.log",
    "core.http",
    "core.window",
    "core.args",
    "core.instance",
    "core.popup",
    "core.userflow",
    "core.cache",
    "core.asynk",
    "core.leak",
    "core.robust",
    "core.endpoints",
    "core.integrity",
    "core.feature_gate",
    "core.region",
    "core.boot",
    "core.stats",
    "core.consent",
    "core.client_ai",
    "core.storage",
    "core.ax",
    "core.settings_io",
    "core.download_history",
    "core.extension_gate",
    "core.launch_progress",
    "core.download_sources",
    "core.instance_drop",
    "core.banner_design",
    "core.widget_layout",
    "core.appearance",
    "core.first_run",
    "core.skin_draft",
    "core.upgrade_plan",
    "core.search_filter",
    "core.generator_session",
    "core.seed_access",
    "core.lan_channel",
    "core.notice_center",
    "dispatcher.launcher",
];

/// 零级致命 / 一级功能失效 / 二级降级 / 三级忽略。
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Tier {
    Fatal,
    FeatureDisabled,
    Degraded,
    Ignored,
}

impl Tier {
    pub fn code(&self) -> &'static str {
        match self {
            Tier::Fatal => "fatal",
            Tier::FeatureDisabled => "disabled",
            Tier::Degraded => "degraded",
            Tier::Ignored => "ignored",
        }
    }

    pub fn action(&self) -> &'static str {
        match self {
            Tier::Fatal => "report_and_stop",
            Tier::FeatureDisabled => "disable_and_notice",
            Tier::Degraded => "switch_and_notice",
            Tier::Ignored => "log_only",
        }
    }

    pub fn line(&self, target: &str) -> String {
        diag_line("core", "boot", target, self.code(), &format!("action={}", self.action()))
    }
}

pub fn classify(level: Option<Level>) -> Tier {
    match level {
        Some(Level::Fatal) => Tier::Fatal,
        Some(Level::FeatureDisabled) => Tier::FeatureDisabled,
        Some(Level::Degraded) => Tier::Degraded,
        Some(Level::Ok) | None => Tier::Ignored,
    }
}

pub fn safe_mode_reached(failures: u32) -> bool {
    failures >= SAFE_MODE_AFTER
}

pub struct BootState {
    failures: AtomicU32,
    root: Option<PathBuf>,
    budget: OpBudget,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ExportOutcome {
    pub path: Option<String>,
    pub bytes: usize,
    pub diagnostics: Vec<String>,
}

impl BootState {
    pub fn open(dir: Option<&str>) -> (Self, Vec<String>) {
        let mut diagnostics = Vec::new();
        let root = match dir {
            Some(d) if !d.is_empty() => match validate_dir(d) {
                Ok(p) => Some(p),
                Err(e) => {
                    diagnostics.push(diag_line("core", "boot", "state_dir", "ERROR", &format!("detail={}", e)));
                    None
                }
            },
            Some(_) => {
                diagnostics.push(diag_line("core", "boot", "state_dir", "SKIP", "detail=empty_dir"));
                None
            }
            None => None,
        };

        let mut failures = 0u32;
        if let Some(ref r) = root {
            let path = r.join(STATE_FILE);
            let (text, used_fallback) = robust::read_or_default(&path, DEFAULT_STATE);
            if used_fallback {
                diagnostics.push(diag_line("core", "boot", "state_file", "OK", "detail=fallback_default"));
            }
            match parse_state(&text) {
                Ok(n) => failures = n,
                Err(e) => {
                    diagnostics.push(diag_line("core", "boot", "state_file", "ERROR", &format!("detail={}", e)));
                }
            }
        } else {
            diagnostics.push(diag_line("core", "boot", "state_file", "SKIP", "detail=in_memory"));
        }

        (
            Self {
                failures: AtomicU32::new(failures),
                root,
                budget: OpBudget::new(robust::MAX_OPS_PER_WINDOW),
            },
            diagnostics,
        )
    }

    pub fn consecutive_failures(&self) -> u32 {
        self.failures.load(Ordering::SeqCst)
    }

    pub fn safe_mode(&self) -> bool {
        safe_mode_reached(self.consecutive_failures())
    }

    pub fn record(&self, failed: bool) -> Vec<String> {
        if !self.budget.try_op() {
            return vec![diag_line("core", "boot", "record", "DENY", "detail=rate_limited")];
        }
        let next = if failed {
            let prev = match self
                .failures
                .try_update(Ordering::SeqCst, Ordering::SeqCst, |v| Some(v.saturating_add(1)))
            {
                Ok(v) | Err(v) => v,
            };
            prev.saturating_add(1)
        } else {
            self.failures.store(0, Ordering::SeqCst);
            0
        };
        let mut diagnostics = vec![diag_line(
            "core",
            "boot",
            "record",
            "OK",
            &format!("failed={} failures={}", if failed { 1 } else { 0 }, next),
        )];
        if let Some(ref r) = self.root {
            let text = json!({"schema": 1, "failures": next}).to_string();
            match fs::create_dir_all(r).and_then(|_| fs::write(r.join(STATE_FILE), text)) {
                Ok(()) => {}
                Err(e) => diagnostics.push(diag_line(
                    "core",
                    "boot",
                    "state_write",
                    "ERROR",
                    &format!("detail={:?}", e.kind()),
                )),
            }
        }
        diagnostics
    }

    /// 安全模式忽略自定义配置；内置默认取 Config::empty 与 feature_gate 内置策略。
    pub fn builtin_defaults(&self) -> (String, String, Vec<String>) {
        let mut diagnostics = Vec::new();
        let config = match Config::empty("windows").to_json_string() {
            Ok(s) => s,
            Err(e) => {
                diagnostics.push(diag_line("core", "boot", "builtin_config", "ERROR", &format!("detail={}", e)));
                DEFAULT_STATE.to_string()
            }
        };
        let policy = crate::core::feature_gate::BUILTIN_POLICY.to_string();
        diagnostics.push(diag_line("core", "boot", "builtin_config", "OK", "detail=custom_ignored"));
        (config, policy, diagnostics)
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

fn parse_state(text: &str) -> Result<u32> {
    if text.len() > MAX_STATE_BYTES {
        return Err(anyhow!("state oversized"));
    }
    let v: Value = from_str(text).map_err(|_| anyhow!("state malformed"))?;
    if v.get("schema").and_then(Value::as_u64) != Some(1) {
        return Err(anyhow!("state schema"));
    }
    let n = v
        .get("failures")
        .and_then(Value::as_u64)
        .ok_or_else(|| anyhow!("state failures missing"))?;
    if n > u32::MAX as u64 {
        return Err(anyhow!("state failures out of range"));
    }
    Ok(n as u32)
}

pub fn export(dir: Option<&str>, bundle: &DiagnosticBundle) -> ExportOutcome {
    let mut diagnostics = Vec::new();
    let dir = match dir {
        Some(d) if !d.is_empty() => d,
        Some(_) => {
            diagnostics.push(diag_line("core", "boot", "bundle", "SKIP", "detail=empty_dir"));
            return ExportOutcome { path: None, bytes: 0, diagnostics };
        }
        None => {
            diagnostics.push(diag_line("core", "boot", "bundle", "SKIP", "detail=no_export_dir"));
            return ExportOutcome { path: None, bytes: 0, diagnostics };
        }
    };

    let root = match validate_dir(dir) {
        Ok(p) => p,
        Err(e) => {
            diagnostics.push(diag_line("core", "boot", "bundle", "ERROR", &format!("detail={}", e)));
            return ExportOutcome { path: None, bytes: 0, diagnostics };
        }
    };

    if let Err(e) = validate_bundle(bundle) {
        diagnostics.push(diag_line("core", "boot", "bundle", "ERROR", &format!("detail={}", e)));
        return ExportOutcome { path: None, bytes: 0, diagnostics };
    }

    let body = match to_string(&json!({
        "schema": 1,
        "lines": bundle.lines,
        "config_snapshot": bundle.config_snapshot,
        "runtime": bundle.runtime,
        "modules": bundle.modules,
    })) {
        Ok(s) => s,
        Err(e) => {
            diagnostics.push(diag_line("core", "boot", "bundle", "ERROR", &format!("detail={}", e)));
            return ExportOutcome { path: None, bytes: 0, diagnostics };
        }
    };

    let path = match robust::safe_join(&root, BUNDLE_FILE) {
        Ok(p) => p,
        Err(e) => {
            diagnostics.push(diag_line("core", "boot", "bundle", "ERROR", &format!("detail={}", e)));
            return ExportOutcome { path: None, bytes: 0, diagnostics };
        }
    };

    match fs::create_dir_all(&root) {
        Ok(()) => {}
        Err(e) => {
            diagnostics.push(diag_line("core", "boot", "bundle_dir", "ERROR", &format!("detail={:?}", e.kind())));
            return ExportOutcome { path: None, bytes: 0, diagnostics };
        }
    }
    match fs::write(&path, body.as_bytes()) {
        Ok(()) => {
            diagnostics.push(diag_line("core", "boot", "bundle", "OK", &format!("bytes={}", body.len())));
            ExportOutcome {
                path: Some(path.to_string_lossy().into_owned()),
                bytes: body.len(),
                diagnostics,
            }
        }
        Err(e) => {
            diagnostics.push(diag_line("core", "boot", "bundle", "ERROR", &format!("detail={:?}", e.kind())));
            ExportOutcome { path: None, bytes: 0, diagnostics }
        }
    }
}

fn validate_bundle(b: &DiagnosticBundle) -> Result<()> {
    if b.lines.len() > MAX_LINES {
        return Err(anyhow!("too many lines"));
    }
    if b.modules.len() > MAX_MODULES {
        return Err(anyhow!("too many modules"));
    }
    if b.config_snapshot.len() > MAX_SNAPSHOT_BYTES {
        return Err(anyhow!("snapshot oversized"));
    }
    if b.runtime.len() > MAX_RUNTIME_BYTES {
        return Err(anyhow!("runtime oversized"));
    }
    for line in &b.lines {
        if line.len() > MAX_LINE_BYTES {
            return Err(anyhow!("line oversized"));
        }
    }
    for m in &b.modules {
        robust::check_text(m, robust::MAX_ID_BYTES)?;
    }
    Ok(())
}

pub fn loaded_modules() -> Vec<String> {
    LOADED_MODULES.iter().map(|s| (*s).to_string()).collect()
}

pub fn ax_pool_line() -> String {
    use crate::core::ax::{self, AxState};
    let conflicts = ax::AX_SPECS.iter().filter(|s| !s.conflict.is_empty()).count();
    let no_ui = ax::AX_SPECS.iter().filter(|s| !s.ui).count();
    let named = ax::AX_SPECS.iter().filter(|s| !s.name.is_empty() && !s.id.is_empty()).count();
    let planned = ax::AX_SPECS.iter().filter(|s| s.state == AxState::Planned).count();
    let _ = ax::by_id("AX23");
    let _ = ax::count_by_state(AxState::GateOnly);
    format!(
        "[KCU] core ax pool OK specs={} planned={} conflicts={} no_ui={} named={}",
        ax::AX_SPECS.len(), planned, conflicts, no_ui, named
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::path::Path;
    use std::sync::atomic::AtomicUsize;

    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> String {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        std::env::temp_dir()
            .join(format!("kcu057-{}-{}", std::process::id(), n))
            .to_string_lossy()
            .into_owned()
    }

    fn bundle() -> DiagnosticBundle {
        DiagnosticBundle {
            lines: vec!["[KCU] core boot record OK failed=1 failures=1".to_string()],
            config_snapshot: r#"{"schema":1}"#.to_string(),
            runtime: "mem=8589934592 first=0".to_string(),
            modules: loaded_modules(),
        }
    }

    #[test]
    fn default_state_is_zero() {
        let (s, d) = BootState::open(None);
        assert_eq!(s.consecutive_failures(), 0);
        assert!(!s.safe_mode());
        assert!(d.iter().any(|x| x.contains("in_memory")));
    }

    #[test]
    fn consecutive_failures_reach_safe_mode() {
        let (s, _) = BootState::open(None);
        for _ in 0..SAFE_MODE_AFTER {
            s.record(true);
        }
        assert!(s.safe_mode());
        assert_eq!(s.consecutive_failures(), SAFE_MODE_AFTER);
    }

    #[test]
    fn success_resets_counter() {
        let (s, _) = BootState::open(None);
        s.record(true);
        s.record(true);
        s.record(false);
        assert_eq!(s.consecutive_failures(), 0);
        assert!(!s.safe_mode());
    }

    #[test]
    fn counter_saturates() {
        let (s, _) = BootState::open(None);
        s.failures.store(u32::MAX, Ordering::SeqCst);
        s.record(true);
        assert_eq!(s.consecutive_failures(), u32::MAX);
    }

    #[test]
    fn deleted_state_falls_back() {
        let dir = tmp();
        let (s, d) = BootState::open(Some(&dir));
        assert_eq!(s.consecutive_failures(), 0);
        assert!(d.iter().any(|x| x.contains("fallback_default")));
    }

    #[test]
    fn malformed_state_falls_back() {
        let dir = tmp();
        fs::create_dir_all(&dir).ok();
        fs::write(Path::new(&dir).join(STATE_FILE), "not json").ok();
        let (s, d) = BootState::open(Some(&dir));
        assert_eq!(s.consecutive_failures(), 0);
        assert!(d.iter().any(|x| x.contains("state malformed")));
    }

    #[test]
    fn oversized_state_falls_back() {
        let dir = tmp();
        fs::create_dir_all(&dir).ok();
        fs::write(Path::new(&dir).join(STATE_FILE), "x".repeat(MAX_STATE_BYTES + 1)).ok();
        let (s, d) = BootState::open(Some(&dir));
        assert_eq!(s.consecutive_failures(), 0);
        assert!(d.iter().any(|x| x.contains("state oversized")));
    }

    #[test]
    fn negative_failures_falls_back() {
        let dir = tmp();
        fs::create_dir_all(&dir).ok();
        fs::write(Path::new(&dir).join(STATE_FILE), r#"{"schema":1,"failures":-1}"#).ok();
        let (s, d) = BootState::open(Some(&dir));
        assert_eq!(s.consecutive_failures(), 0);
        assert!(d.iter().any(|x| x.contains("state failures missing")));
    }

    #[test]
    fn persisted_counter_survives_reopen() {
        let dir = tmp();
        let (a, _) = BootState::open(Some(&dir));
        a.record(true);
        a.record(true);
        let (b, _) = BootState::open(Some(&dir));
        assert_eq!(b.consecutive_failures(), 2);
        b.record(true);
        assert!(b.safe_mode());
    }

    #[test]
    fn builtin_defaults_are_serializable() {
        let (s, _) = BootState::open(None);
        let (config, policy, d) = s.builtin_defaults();
        let _: Value = from_str(&config).unwrap();
        let _: Value = from_str(&policy).unwrap();
        assert!(d.iter().any(|x| x.contains("custom_ignored")));
    }

    #[test]
    fn four_tiers() {
        assert_eq!(classify(Some(Level::Fatal)), Tier::Fatal);
        assert_eq!(classify(Some(Level::FeatureDisabled)), Tier::FeatureDisabled);
        assert_eq!(classify(Some(Level::Degraded)), Tier::Degraded);
        assert_eq!(classify(None), Tier::Ignored);
        assert!(Tier::Fatal.line("start").contains("report_and_stop"));
    }

    #[test]
    fn export_writes_all_four_sections() {
        let dir = tmp();
        let r = export(Some(&dir), &bundle());
        assert!(r.path.is_some());
        let p = r.path.unwrap();
        let text = fs::read_to_string(&p).unwrap();
        let v: Value = from_str(&text).unwrap();
        assert_eq!(v["schema"], 1);
        assert_eq!(v["lines"].as_array().unwrap().len(), 1);
        assert_eq!(v["config_snapshot"], r#"{"schema":1}"#);
        assert_eq!(v["runtime"], "mem=8589934592 first=0");
        assert_eq!(v["modules"].as_array().unwrap().len(), LOADED_MODULES.len());
        fs::remove_dir_all(&dir).ok();
    }

    #[test]
    fn export_without_dir_is_visible() {
        let r = export(None, &bundle());
        assert!(r.path.is_none());
        assert!(r.diagnostics.iter().any(|x| x.contains("no_export_dir")));
    }

    #[test]
    fn export_rejects_oversized_bundle() {
        let dir = tmp();
        let mut b = bundle();
        b.lines = vec!["x".to_string(); MAX_LINES + 1];
        let r = export(Some(&dir), &b);
        assert!(r.path.is_none());
        assert!(r.diagnostics.iter().any(|x| x.contains("too many lines")));
    }

    #[test]
    fn export_rejects_control_chars_in_module() {
        let dir = tmp();
        let mut b = bundle();
        b.modules = vec!["core\u{0000}bad".to_string()];
        let r = export(Some(&dir), &b);
        assert!(r.path.is_none());
        assert!(r.diagnostics.iter().any(|x| x.contains("ERROR")));
    }

    #[test]
    fn rate_limit_does_not_panic() {
        let (s, _) = BootState::open(None);
        for _ in 0..(robust::MAX_OPS_PER_WINDOW + 8) {
            let d = s.record(true);
            assert!(!d.is_empty());
        }
    }
}

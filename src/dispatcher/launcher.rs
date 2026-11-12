use crate::core::args::LaunchArgs;
use crate::core::asynk::CancelToken;
use crate::core::cache::Cache;
use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::instance::{select_instance, Instance, ServerEntry, VersionWeight};
use crate::core::log::LogBuffer;
use crate::core::popup::{catalog, CloseAction, PopupRegistry};
use crate::dispatcher::json;
use crate::dispatcher::mode::{Fallback, Mode, ModeInput, ModeSelection, ModeSelector};
use crate::dispatcher::task::{LaunchTask, TaskSet};
use std::sync::atomic::{AtomicUsize, Ordering};
use std::sync::Arc;
use std::time::Duration;

pub const FAILURE_THRESHOLD: u32 = 3;
pub const DEFAULT_CACHE_CAPACITY: usize = 16;
pub const DEFAULT_CACHE_TTL: Duration = Duration::from_secs(30);

#[derive(Debug, Clone, Default)]
pub struct DispatchInput {
    pub task_texts: Vec<String>,
    pub config_text: Option<String>,
    pub args: LaunchArgs,
    pub mem_bytes: u64,
    pub memory_unknown: bool,
    pub first_run: bool,
    pub kcul_present: bool,
    pub credential_present: bool,
    pub server: Option<ServerEntry>,
    pub instances: Vec<Instance>,
    pub habit: Vec<VersionWeight>,
    pub user_choice: Option<String>,
}

#[derive(Debug, Clone)]
pub struct LaunchOutcome {
    pub envelope: Envelope,
    pub mode: Mode,
    pub fallback: Fallback,
    pub task: LaunchTask,
    pub instance: Option<String>,
    pub diagnostics: Vec<String>,
    pub premium_allowed: bool,
    pub ui_loaded: bool,
    pub popups_open: usize,
    pub safe_mode: bool,
    pub diagnostic_bundle: Vec<String>,
    pub cancelled: bool,
}

pub struct Dispatcher {
    pub cache: Arc<Cache<String, String>>,
    pub parse_calls: Arc<AtomicUsize>,
    pub log: LogBuffer,
    pub failures: u32,
    pub safe_mode: bool,
    pub diagnostic_ready: bool,
}

impl Default for Dispatcher {
    fn default() -> Self {
        Self::new(DEFAULT_CACHE_CAPACITY)
    }
}

impl Dispatcher {
    pub fn new(capacity: usize) -> Self {
        Self {
            cache: Arc::new(Cache::new(capacity, DEFAULT_CACHE_TTL)),
            parse_calls: Arc::new(AtomicUsize::new(0)),
            log: LogBuffer::new(100),
            failures: 0,
            safe_mode: false,
            diagnostic_ready: false,
        }
    }

    pub fn reset(&mut self) {
        self.cache.clear();
        self.parse_calls.store(0, Ordering::SeqCst);
        let _ = self.log.flush();
        self.failures = 0;
        self.safe_mode = false;
        self.diagnostic_ready = false;
    }

    pub fn flush_diagnostics(&mut self) -> Vec<Vec<String>> {
        self.log.flush()
    }

    pub fn dispatch(&mut self, input: &DispatchInput, cancel: &CancelToken) -> LaunchOutcome {
        let mut envelope = Envelope::new(Kind::Request, "dispatcher");
        let mut diagnostics = Vec::new();
        let mut failed = false;

        if cancel.is_cancelled() {
            diagnostics.push(diag_line("dispatcher", "dispatch", "launch", "CANCELLED", "detail=token_cancelled"));
            self.log.push(diagnostics[0].clone());
            return LaunchOutcome {
                envelope: envelope.with_error("CANCELLED"),
                mode: Mode::Safe,
                fallback: Fallback::Zero,
                task: LaunchTask::default(),
                instance: None,
                diagnostics,
                premium_allowed: false,
                ui_loaded: false,
                popups_open: 0,
                safe_mode: self.safe_mode,
                diagnostic_bundle: Vec::new(),
                cancelled: true,
            };
        }

        let mut config_mode = None;
        if let Some(text) = input.config_text.as_deref() {
            match json::parse(text) {
                Ok(v) => config_mode = v.string_field("mode"),
                Err(e) => {
                    failed = true;
                    diagnostics.push(diag_line("dispatcher", "parse", "config/launch.json", "ERROR", &format!("detail={}", e)));
                }
            }
        }

        let cache = Arc::clone(&self.cache);
        let calls = Arc::clone(&self.parse_calls);
        let mut values = Vec::new();
        for text in &input.task_texts {
            match cache.get_or_load(text.clone(), Duration::from_secs(2), || {
                calls.fetch_add(1, Ordering::SeqCst);
                let id = LaunchTask::from_str(text).map(|t| t.id).map_err(|e| e.to_string())?;
                Ok::<String, String>(id)
            }) {
                Ok(_) => match json::parse(text) {
                    Ok(v) => values.push(v),
                    Err(e) => {
                        failed = true;
                        diagnostics.push(diag_line("dispatcher", "parse", "task", "ERROR", &format!("detail={}", e)));
                    }
                },
                Err(_) => {
                    failed = true;
                    diagnostics.push(diag_line("dispatcher", "parse", "task", "DEGRADE", "detail=task_disabled"));
                }
            }
        }

        let set = TaskSet::from_values(&values).unwrap_or_default();
        let task = set.pick(&input.args);
        let mut instance = None;
        if task.joins_server() {
            if let Some(server) = input.server.as_ref() {
                let choice = input
                    .args
                    .instance
                    .as_deref()
                    .or(task.instance.as_deref())
                    .or(input.user_choice.as_deref());
                match select_instance(server, &input.instances, &input.habit, choice) {
                    Ok(i) => {
                        instance = Some(i.id.clone());
                        diagnostics.push(diag_line("dispatcher", "select", "instance", "OK", &format!("detail={}", i.id)));
                    }
                    Err(e) => {
                        diagnostics.push(diag_line("dispatcher", "select", "instance", "DEGRADE", &format!("detail={:?}", e)));
                    }
                }
            } else {
                diagnostics.push(diag_line("dispatcher", "join", "server", "OK", "detail=direct_join"));
            }
        }

        let mode_input = ModeInput {
            mem_bytes: input.mem_bytes,
            memory_unknown: input.memory_unknown,
            first_run: input.first_run,
            config_mode: if self.safe_mode { None } else { config_mode.clone() },
            args_mode: if self.safe_mode { None } else { input.args.mode.clone() },
            task_mode: if self.safe_mode { None } else { task.mode.clone() },
            force_headless: input.args.headless() || task.headless() || input.kcul_present,
            credential_present: input.credential_present,
        };

        let mut selection: ModeSelection = if self.safe_mode {
            ModeSelector::safe(&mode_input)
        } else {
            match ModeSelector::select(&mode_input) {
                Ok(s) => s,
                Err(e) => {
                    failed = true;
                    diagnostics.push(diag_line("dispatcher", "mode", "selector", "ERROR", &format!("detail={}", e)));
                    let clean = ModeInput {
                        config_mode: None,
                        args_mode: None,
                        task_mode: None,
                        ..mode_input.clone()
                    };
                    ModeSelector::select(&clean).unwrap_or_else(|_| ModeSelector::safe(&clean))
                }
            }
        };

        if selection.memory_degraded {
            diagnostics.push(diag_line("dispatcher", "memory", "detect", "DEGRADE", "detail=default_normal"));
        }
        if !selection.premium_allowed {
            diagnostics.push(diag_line("dispatcher", "auth", "premium", "DEGRADE", "detail=credential_absent"));
        }
        if !selection.ui_loaded {
            diagnostics.push(diag_line("dispatcher", "ui", "frame", "OK", &format!("detail=skipped mode={}", selection.mode.code())));
        }

        let popups_open = if selection.ui_loaded {
            let mut reg = PopupRegistry::new();
            for p in catalog() {
                reg.open(p);
            }
            let missing = reg.missing_close_path();
            if !missing.is_empty() {
                diagnostics.push(diag_line("dispatcher", "popup", "registry", "ERROR", &format!("detail={:?}", missing)));
            }
            for p in catalog() {
                let _ = reg.close(&p.id, CloseAction::Button);
            }
            let _ = reg.force_close_all();
            reg.open_count()
        } else {
            0
        };

        if failed {
            self.failures += 1;
        } else {
            self.failures = 0;
        }
        if self.failures >= FAILURE_THRESHOLD {
            self.safe_mode = true;
            selection = ModeSelector::safe(&mode_input);
            diagnostics.push(diag_line("dispatcher", "safety", "enter", "OK", "detail=builtin_defaults"));
        }
        if self.safe_mode && failed {
            self.diagnostic_ready = true;
        }

        let mut diagnostic_bundle = Vec::new();
        if self.diagnostic_ready {
            diagnostic_bundle.push(diag_line("dispatcher", "bundle", "logs", "OK", &format!("detail={}", diagnostics.len())));
            diagnostic_bundle.push(diag_line("dispatcher", "bundle", "config", "OK", &format!("detail={:?}", config_mode)));
            diagnostic_bundle.push(diag_line("dispatcher", "bundle", "runtime", "OK", &format!("detail=mem={} first={}", input.mem_bytes, input.first_run)));
            diagnostic_bundle.push(diag_line("dispatcher", "bundle", "modules", "OK", "detail=core,dispatcher"));
        }

        diagnostics.push(diag_line("dispatcher", "dispatch", "launch", "OK", &format!("detail=mode={} task={} fallback={}", selection.mode.code(), task.id, selection.fallback.code())));
        for d in &diagnostics {
            self.log.push(d.clone());
        }

        envelope = envelope
            .with("mode", selection.mode.code())
            .with("task", &task.id)
            .with("fallback", selection.fallback.code())
            .with("instance", instance.as_deref().unwrap_or("none"))
            .with("ui_loaded", if selection.ui_loaded { "true" } else { "false" });
        if failed {
            envelope = envelope.with_error("partial_failure");
        }

        LaunchOutcome {
            envelope,
            mode: selection.mode,
            fallback: selection.fallback,
            task,
            instance,
            diagnostics,
            premium_allowed: selection.premium_allowed,
            ui_loaded: selection.ui_loaded,
            popups_open,
            safe_mode: self.safe_mode,
            diagnostic_bundle,
            cancelled: false,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::leak::Tracker;

    fn input() -> DispatchInput {
        DispatchInput {
            mem_bytes: 8 * 1024 * 1024 * 1024,
            ..DispatchInput::default()
        }
    }

    fn server() -> ServerEntry {
        ServerEntry {
            name: "S".to_string(),
            address: "s.example.net".to_string(),
            supported_versions: vec!["1.20.4".to_string(), "1.21.1".to_string()],
        }
    }

    fn instances() -> Vec<Instance> {
        vec![
            Instance { id: "a".into(), mc_version: "1.20.4".into() },
            Instance { id: "b".into(), mc_version: "1.21.1".into() },
        ]
    }

    #[test]
    fn low_memory_first_run_dispatches_lightweight_without_ui() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.mem_bytes = 2147483648;
        i.first_run = true;
        let o = d.dispatch(&i, &CancelToken::new());
        assert_eq!(o.mode, Mode::Lightweight);
        assert!(!o.ui_loaded);
        assert_eq!(o.popups_open, 0);
        assert_eq!(o.task.id, "default");
    }

    #[test]
    fn normal_mode_registers_and_closes_every_popup() {
        let mut d = Dispatcher::default();
        let o = d.dispatch(&input(), &CancelToken::new());
        assert_eq!(o.mode, Mode::Normal);
        assert!(o.ui_loaded);
        assert_eq!(o.popups_open, 0);
        assert!(o.envelope.ok());
    }

    #[test]
    fn config_launch_json_overrides_automatic_mode() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.mem_bytes = 2147483648;
        i.first_run = true;
        i.config_text = Some(r#"{"mode":"normal"}"#.to_string());
        assert_eq!(d.dispatch(&i, &CancelToken::new()).mode, Mode::Normal);
    }

    #[test]
    fn kcul_entry_forces_headless_and_disables_premium() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.kcul_present = true;
        let o = d.dispatch(&i, &CancelToken::new());
        assert_eq!(o.mode, Mode::Headless);
        assert!(!o.ui_loaded);
        assert!(!o.premium_allowed);
        assert_eq!(o.fallback, Fallback::One);
        assert!(o.diagnostics.iter().any(|x| x.contains("credential_absent")));
    }

    #[test]
    fn headless_with_saved_credential_allows_premium() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.kcul_present = true;
        i.credential_present = true;
        assert!(d.dispatch(&i, &CancelToken::new()).premium_allowed);
    }

    #[test]
    fn invalid_mode_reports_and_falls_back_without_crashing() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.config_text = Some(r#"{"mode":"turbo"}"#.to_string());
        let o = d.dispatch(&i, &CancelToken::new());
        assert!(!o.envelope.ok());
        assert_eq!(o.mode, Mode::Normal);
        assert!(o.diagnostics.iter().any(|x| x.contains("invalid mode")));
    }

    #[test]
    fn single_arg_joins_server_directly() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.args = LaunchArgs::parse(["--server", "mc.example.net:25565"]).unwrap();
        let o = d.dispatch(&i, &CancelToken::new());
        assert!(o.task.joins_server());
        assert_eq!(o.task.id, "cmd");
    }

    #[test]
    fn double_click_picks_compatible_instance_by_weight() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.args = LaunchArgs::parse(["--server", "s.example.net"]).unwrap();
        i.server = Some(server());
        i.instances = instances();
        i.habit = vec![VersionWeight { version: "1.21.1".into(), weight: 9 }];
        let o = d.dispatch(&i, &CancelToken::new());
        assert_eq!(o.instance.as_deref(), Some("b"));
    }

    #[test]
    fn user_choice_ranks_first_over_habit_weight() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.args = LaunchArgs::parse(["--server", "s.example.net"]).unwrap();
        i.server = Some(server());
        i.instances = instances();
        i.habit = vec![VersionWeight { version: "1.21.1".into(), weight: 9 }];
        i.user_choice = Some("1.20.4".to_string());
        assert_eq!(d.dispatch(&i, &CancelToken::new()).instance.as_deref(), Some("a"));
    }

    #[test]
    fn incompatible_user_choice_is_visible_and_non_fatal() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.args = LaunchArgs::parse(["--server", "s.example.net"]).unwrap();
        i.server = Some(server());
        i.instances = instances();
        i.user_choice = Some("1.16.5".to_string());
        let o = d.dispatch(&i, &CancelToken::new());
        assert!(o.envelope.ok());
        assert!(o.diagnostics.iter().any(|x| x.contains("UserChoiceNotCompatible")));
    }

    #[test]
    fn repeated_task_text_is_parsed_once() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.task_texts = vec![r#"{"id":"a","kind":"launch"}"#.to_string()];
        for _ in 0..10 {
            let _ = d.dispatch(&i, &CancelToken::new());
        }
        assert_eq!(d.parse_calls.load(Ordering::SeqCst), 1);
        assert_eq!(d.cache.len(), 1);
        assert_eq!(d.cache.inflight_count(), 0);
    }

    #[test]
    fn cache_stays_bounded_over_many_tasks() {
        let mut d = Dispatcher::new(4);
        for n in 0..40 {
            let mut i = input();
            i.task_texts = vec![format!(r#"{{"id":"t{}","kind":"launch"}}"#, n)];
            let _ = d.dispatch(&i, &CancelToken::new());
        }
        assert!(d.cache.len() <= 4);
        assert!(d.cache.order_len() <= 4);
        assert_eq!(d.cache.inflight_count(), 0);
    }

    #[test]
    fn cancelled_token_stops_before_any_work() {
        let mut d = Dispatcher::default();
        let c = CancelToken::new();
        c.cancel();
        let o = d.dispatch(&input(), &c);
        assert!(o.cancelled);
        assert!(!o.envelope.ok());
        assert_eq!(d.parse_calls.load(Ordering::SeqCst), 0);
    }

    #[test]
    fn consecutive_failures_enter_safe_mode_then_export_bundle() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.config_text = Some("{bad".to_string());
        for n in 0..3 {
            let o = d.dispatch(&i, &CancelToken::new());
            assert_eq!(o.safe_mode, n == 2);
        }
        assert_eq!(d.failures, 3);
        let o = d.dispatch(&i, &CancelToken::new());
        assert!(o.safe_mode);
        assert_eq!(o.mode, Mode::Safe);
        assert!(!o.ui_loaded);
        assert_eq!(o.diagnostic_bundle.len(), 4);
    }

    #[test]
    fn successful_dispatch_clears_failure_counter() {
        let mut d = Dispatcher::default();
        let mut bad = input();
        bad.config_text = Some("{bad".to_string());
        let _ = d.dispatch(&bad, &CancelToken::new());
        assert_eq!(d.failures, 1);
        let _ = d.dispatch(&input(), &CancelToken::new());
        assert_eq!(d.failures, 0);
        assert!(!d.safe_mode);
    }

    #[test]
    fn unknown_memory_is_level_two_degradation() {
        let mut d = Dispatcher::default();
        let mut i = input();
        i.memory_unknown = true;
        let o = d.dispatch(&i, &CancelToken::new());
        assert_eq!(o.fallback, Fallback::Two);
        assert!(o.diagnostics.iter().any(|x| x.contains("default_normal")));
    }

    #[test]
    fn diagnostics_are_single_line_kcu_prefixed() {
        let mut d = Dispatcher::default();
        let o = d.dispatch(&input(), &CancelToken::new());
        for x in &o.diagnostics {
            assert!(x.starts_with("[KCU] "));
            assert!(!x.contains('\n'));
        }
        assert!(d.flush_diagnostics().len() >= 1);
    }

    #[test]
    fn outcomes_do_not_leave_live_tracked_objects() {
        let t = Tracker::new();
        let mut d = Dispatcher::default();
        {
            let a = t.track(d.dispatch(&input(), &CancelToken::new()));
            let b = a.clone();
            assert_eq!(t.live(), 2);
            drop(b);
        }
        assert_eq!(t.live(), 0);
    }

    #[test]
    fn reset_clears_cache_log_and_safety_state() {
        let mut d = Dispatcher::default();
        d.failures = 2;
        let mut i = input();
        i.task_texts = vec![r#"{"id":"a"}"#.to_string()];
        let _ = d.dispatch(&i, &CancelToken::new());
        d.reset();
        assert_eq!(d.cache.len(), 0);
        assert_eq!(d.parse_calls.load(Ordering::SeqCst), 0);
        assert_eq!(d.failures, 0);
        assert!(!d.safe_mode);
        assert!(d.flush_diagnostics().is_empty());
    }
}

use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};

pub const PROGRESS_TARGET: &str = "launcher.progress";
pub const MAX_WAIT_SECS: u64 = 120;
pub const PHASES: &[(&str, u8)] = &[
    ("dispatcher_start", 0),
    ("mode_resolved", 20),
    ("assets_loaded", 50),
    ("modules_loaded", 80),
    ("ui_ready", 100),
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ProgressState {
    Running,
    Ready,
    Failed,
    Cancelled,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AdvanceDecision {
    Advanced,
    Rejected,
}

pub struct LaunchProgress {
    index: usize,
    percent: u8,
    state: ProgressState,
    started_at: u64,
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("launcher", action, "progress", "DEGRADE", reason)
}

impl LaunchProgress {
    pub fn new(now: u64) -> Self {
        LaunchProgress { index: 0, percent: 0, state: ProgressState::Running, started_at: now }
    }

    pub fn state(&self) -> ProgressState {
        self.state
    }

    pub fn percent(&self) -> u8 {
        self.percent
    }

    pub fn phase(&self) -> &'static str {
        PHASES[self.index].0
    }

    fn frozen(&self) -> bool {
        self.state != ProgressState::Running
    }

    pub fn advance(&mut self, phase: &str, now: u64) -> (AdvanceDecision, Vec<String>) {
        if self.frozen() {
            return (AdvanceDecision::Rejected, vec![degrade("advance", "frozen")]);
        }
        if now.saturating_sub(self.started_at) > MAX_WAIT_SECS {
            self.state = ProgressState::Failed;
            return (AdvanceDecision::Rejected, vec![degrade("advance", "timeout")]);
        }
        let Some(next) = PHASES.iter().position(|(name, _)| *name == phase) else {
            return (AdvanceDecision::Rejected, vec![degrade("advance", "unknown_phase")]);
        };
        if next <= self.index {
            return (AdvanceDecision::Rejected, vec![degrade("advance", "non_monotonic")]);
        }
        self.index = next;
        self.percent = PHASES[next].1;
        if next + 1 == PHASES.len() {
            self.state = ProgressState::Ready;
        }
        (AdvanceDecision::Advanced, Vec::new())
    }

    pub fn event(&self) -> Envelope {
        Envelope::new(Kind::Event, PROGRESS_TARGET)
            .with("phase", self.phase())
            .with("percent", &self.percent.to_string())
    }

    pub fn cancel(&mut self) -> Vec<String> {
        if self.frozen() {
            return vec![degrade("cancel", "frozen")];
        }
        self.state = ProgressState::Cancelled;
        Vec::new()
    }

    pub fn fail(&mut self, reason: &str) -> Vec<String> {
        if self.frozen() {
            return vec![degrade("fail", "frozen")];
        }
        self.state = ProgressState::Failed;
        vec![diag_line("launcher", "fail", "progress", "ERROR", reason)]
    }
}

pub fn full_sequence(now: u64) -> (LaunchProgress, Vec<Envelope>, Vec<String>) {
    let mut progress = LaunchProgress::new(now);
    let mut events = vec![Envelope::new(Kind::Event, PROGRESS_TARGET)
        .with("phase", PHASES[0].0)
        .with("percent", &PHASES[0].1.to_string())];
    let mut lines = Vec::new();
    for (name, _) in PHASES.iter().skip(1) {
        let (decision, more) = progress.advance(name, now);
        if decision == AdvanceDecision::Rejected {
            lines.extend(more);
        }
        events.push(progress.event());
    }
    (progress, events, lines)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn phase_table_is_ordered_and_ends_at_hundred() {
        assert_eq!(PHASES.len(), 5);
        assert_eq!(PHASES[0].1, 0);
        assert_eq!(PHASES[PHASES.len() - 1].1, 100);
        let mut last = 0;
        for (_, p) in PHASES {
            assert!(*p >= last);
            last = *p;
        }
    }

    #[test]
    fn full_sequence_reaches_ready_with_five_events() {
        let (p, events, lines) = full_sequence(10);
        assert_eq!(p.state(), ProgressState::Ready);
        assert_eq!(p.percent(), 100);
        assert_eq!(p.phase(), "ui_ready");
        assert_eq!(events.len(), 5);
        assert!(lines.is_empty());
        assert!(events.iter().all(|e| e.kind == Kind::Event && e.target == PROGRESS_TARGET));
    }

    #[test]
    fn non_monotonic_and_unknown_phase_are_rejected_without_state_change() {
        let mut p = LaunchProgress::new(1);
        assert_eq!(p.advance("assets_loaded", 2).0, AdvanceDecision::Advanced);
        assert_eq!(p.percent(), 50);
        let (d1, l1) = p.advance("mode_resolved", 3);
        assert_eq!(d1, AdvanceDecision::Rejected);
        assert!(l1.iter().any(|x| x.contains("non_monotonic")));
        let (d2, l2) = p.advance("not_a_phase", 4);
        assert_eq!(d2, AdvanceDecision::Rejected);
        assert!(l2.iter().any(|x| x.contains("unknown_phase")));
        let (d3, l3) = p.advance("assets_loaded", 5);
        assert_eq!(d3, AdvanceDecision::Rejected);
        assert!(l3.iter().any(|x| x.contains("non_monotonic")));
        assert_eq!(p.percent(), 50);
        assert_eq!(p.state(), ProgressState::Running);
    }

    #[test]
    fn cancel_freezes_and_has_no_side_effects() {
        let mut p = LaunchProgress::new(1);
        p.advance("mode_resolved", 2);
        assert!(p.cancel().is_empty());
        assert_eq!(p.state(), ProgressState::Cancelled);
        let before = p.percent();
        let (d, lines) = p.advance("ui_ready", 3);
        assert_eq!(d, AdvanceDecision::Rejected);
        assert!(lines.iter().any(|x| x.contains("frozen")));
        assert_eq!(p.percent(), before);
        assert_eq!(p.state(), ProgressState::Cancelled);
        assert!(!p.fail("late").is_empty());
    }

    #[test]
    fn timeout_is_visible_and_freezes() {
        let mut p = LaunchProgress::new(1);
        let (d, lines) = p.advance("mode_resolved", 1 + MAX_WAIT_SECS + 1);
        assert_eq!(d, AdvanceDecision::Rejected);
        assert!(lines.iter().any(|x| x.contains("timeout")));
        assert_eq!(p.state(), ProgressState::Failed);
        assert_eq!(p.percent(), 0);
    }

    #[test]
    fn event_carries_only_phase_percent_and_request_id() {
        let (_, events, _) = full_sequence(1);
        let last = events.last().unwrap();
        assert_eq!(last.field("phase"), Some("ui_ready"));
        assert_eq!(last.field("percent"), Some("100"));
        assert_eq!(last.payload.len(), 2);
        assert!(!last.request_id.is_empty());
        assert!(last.ok());
    }

    #[test]
    fn fail_is_visible_and_blocks_further_advance() {
        let mut p = LaunchProgress::new(1);
        let lines = p.fail("asset_missing");
        assert!(lines[0].contains("ERROR"));
        assert_eq!(p.state(), ProgressState::Failed);
        assert_eq!(p.advance("ui_ready", 2).0, AdvanceDecision::Rejected);
        assert!(!p.cancel().is_empty());
    }

    #[test]
    fn skipped_phase_still_moves_forward_monotonically() {
        let mut p = LaunchProgress::new(1);
        assert_eq!(p.advance("modules_loaded", 2).0, AdvanceDecision::Advanced);
        assert_eq!(p.percent(), 80);
        assert_eq!(p.advance("ui_ready", 3).0, AdvanceDecision::Advanced);
        assert_eq!(p.state(), ProgressState::Ready);
        assert_eq!(p.advance("ui_ready", 4).0, AdvanceDecision::Rejected);
    }
}

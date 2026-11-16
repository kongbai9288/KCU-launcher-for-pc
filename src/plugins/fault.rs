use std::collections::BTreeSet;

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct PluginFault {
    pub plugin_id: String,
    pub reason: String,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum FaultAction {
    DisableAndContinue,
    Cancel,
}

#[derive(Debug, Clone, Default)]
pub struct StartupPlan {
    pub plugins: Vec<String>,
    pub disabled: BTreeSet<String>,
    pub cancelled: bool,
    pub retry_count: usize,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FaultReport {
    pub title_key: String,
    pub body_key: String,
    pub body_args: Vec<String>,
    pub primary_key: String,
    pub secondary_key: String,
    pub closable: bool,
}

pub fn fault_report(fault: &PluginFault) -> FaultReport {
    FaultReport {
        title_key: "fault.title".to_string(),
        body_key: "fault.body".to_string(),
        body_args: vec![fault.plugin_id.clone(), fault.reason.clone()],
        primary_key: "fault.action.disable".to_string(),
        secondary_key: "fault.action.cancel".to_string(),
        closable: true,
    }
}

pub fn handle_fault(plan: &mut StartupPlan, fault: &PluginFault, action: FaultAction) {
    match action {
        FaultAction::DisableAndContinue => {
            plan.disabled.insert(fault.plugin_id.clone());
            plan.retry_count += 1;
            plan.cancelled = false;
        }
        FaultAction::Cancel => {
            plan.cancelled = true;
        }
    }
}

impl StartupPlan {
    pub fn active_plugins(&self) -> Vec<&String> {
        self.plugins
            .iter()
            .filter(|p| !self.disabled.contains(*p))
            .collect()
    }

    pub fn should_continue(&self) -> bool {
        !self.cancelled && !self.active_plugins().is_empty()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn plan() -> StartupPlan {
        StartupPlan {
            plugins: vec!["a".into(), "b".into(), "c".into()],
            ..Default::default()
        }
    }

    fn fault() -> PluginFault {
        PluginFault { plugin_id: "b".into(), reason: "入口符号缺失".into() }
    }

    #[test]
    fn report_has_the_two_actions_and_is_closable() {
        let r = fault_report(&fault());
        assert_eq!(r.title_key, "fault.title");
        assert_eq!(r.body_key, "fault.body");
        assert_eq!(r.body_args[0], "b");
        assert_eq!(r.primary_key, "fault.action.disable");
        assert_eq!(r.secondary_key, "fault.action.cancel");
        assert!(r.closable);
    }

    #[test]
    fn disable_removes_only_the_faulty_plugin() {
        let mut p = plan();
        handle_fault(&mut p, &fault(), FaultAction::DisableAndContinue);
        assert_eq!(p.active_plugins(), vec!["a", "c"]);
        assert_eq!(p.retry_count, 1);
        assert!(p.should_continue());
    }

    #[test]
    fn cancel_stops_startup_without_disabling() {
        let mut p = plan();
        handle_fault(&mut p, &fault(), FaultAction::Cancel);
        assert!(p.cancelled);
        assert!(!p.should_continue());
        assert!(p.disabled.is_empty());
    }

    #[test]
    fn disabling_all_plugins_stops_startup() {
        let mut p = plan();
        for id in ["a", "b", "c"] {
            handle_fault(&mut p, &PluginFault { plugin_id: id.into(), reason: "x".into() }, FaultAction::DisableAndContinue);
        }
        assert!(!p.cancelled);
        assert!(p.active_plugins().is_empty());
        assert!(!p.should_continue());
        assert_eq!(p.retry_count, 3);
    }

    #[test]
    fn close_button_and_escape_map_to_cancel() {
        let mut p = plan();
        for a in [FaultAction::Cancel, FaultAction::Cancel] {
            handle_fault(&mut p, &fault(), a);
        }
        assert!(p.cancelled);
    }

    #[test]
    fn reason_is_carried_into_report() {
        let r = fault_report(&PluginFault { plugin_id: "x".into(), reason: "签名校验失败".into() });
        assert_eq!(r.body_args[1], "签名校验失败");
    }
}

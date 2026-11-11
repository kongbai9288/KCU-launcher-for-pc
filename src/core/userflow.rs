use crate::core::args::LaunchArgs;
use crate::core::envelope::{Envelope, Kind};
use crate::core::instance::{select_instance, Instance, ServerEntry, VersionWeight};
use crate::core::popup::{catalog, CloseAction, PopupRegistry};

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum Step {
    Boot,
    PrivacyPolicyShown,
    PrivacyPolicyAccepted,
    DeclarationPage,
    PopupsRegistered,
    PopupsAllClosed,
    ServerDoubleClicked(String),
    InstanceSelected(String),
    DirectJoinByArg(String),
    DialogsStatePersisted,
    FlowDone,
}

#[derive(Debug, Clone)]
pub struct FlowReport {
    pub steps: Vec<Step>,
    pub popup_open_count: usize,
    pub all_popups_closed: bool,
    pub joined_server_directly: bool,
    pub user_choice_honored: bool,
    pub errors: Vec<String>,
    pub envelope_count: usize,
}

impl FlowReport {
    pub fn ok(&self) -> bool {
        self.errors.is_empty()
            && self.all_popups_closed
            && self.popup_open_count == 0
            && self.steps.last() == Some(&Step::FlowDone)
    }
}

pub fn simulate(
    server: &ServerEntry,
    instances: &[Instance],
    habit: &[VersionWeight],
    args: &LaunchArgs,
    user_choice: Option<&str>,
) -> FlowReport {
    let mut steps = Vec::new();
    let mut errors = Vec::new();
    let mut envelopes = Vec::new();
    let mut reg = PopupRegistry::new();

    steps.push(Step::Boot);
    envelopes.push(Envelope::new(Kind::Request, "core.boot"));

    reg.open(crate::core::popup::Popup::new(
        "privacy",
        crate::core::popup::PopupKind::PrivacyPolicy,
        "privacy",
    ));
    steps.push(Step::PrivacyPolicyShown);
    if !reg.close("privacy", CloseAction::Confirm) {
        errors.push("privacy popup did not close".to_string());
    }
    steps.push(Step::PrivacyPolicyAccepted);
    envelopes.push(Envelope::new(Kind::Response, "core.privacy").with("accepted", "true"));

    steps.push(Step::DeclarationPage);
    for p in catalog() {
        if p.id != "privacy" {
            reg.open(p);
        }
    }
    steps.push(Step::PopupsRegistered);

    let missing = reg.missing_close_path();
    if !missing.is_empty() {
        errors.push(format!("popups without close path: {:?}", missing));
    }
    for p in catalog() {
        if !reg.close(&p.id, CloseAction::Button) && !reg.close(&p.id, CloseAction::Escape) {
            errors.push(format!("popup {} could not be closed", p.id));
        }
    }
    if !reg.all_closed() {
        errors.push(format!("{} popups left open", reg.open_count()));
    }
    steps.push(Step::PopupsAllClosed);

    let mut joined_directly = false;
    let mut honored = false;

    if args.joins_server() {
        let addr = args.server.clone().unwrap_or_default();
        joined_directly = true;
        steps.push(Step::DirectJoinByArg(addr.clone()));
        envelopes.push(Envelope::new(Kind::Event, "core.join").with("server", &addr));
    } else {
        steps.push(Step::ServerDoubleClicked(server.address.clone()));
        if user_choice.is_some() {
            honored = true;
        }
        match select_instance(server, instances, habit, user_choice) {
            Ok(i) => steps.push(Step::InstanceSelected(i.id)),
            Err(e) => errors.push(format!("instance selection failed: {:?}", e)),
        }
        envelopes.push(Envelope::new(Kind::Request, "core.instance").with("server", &server.address));
    }

    steps.push(Step::DialogsStatePersisted);
    envelopes.push(Envelope::new(Kind::Event, "core.state").with("path", "dialogs_state"));
    steps.push(Step::FlowDone);

    FlowReport {
        steps,
        popup_open_count: reg.open_count(),
        all_popups_closed: reg.all_closed(),
        joined_server_directly: joined_directly,
        user_choice_honored: honored,
        errors,
        envelope_count: envelopes.len(),
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn server() -> ServerEntry {
        ServerEntry {
            name: "S".into(),
            address: "s.example.net".into(),
            supported_versions: vec!["1.20.4".into(), "1.21.1".into()],
        }
    }

    fn instances() -> Vec<Instance> {
        vec![
            Instance { id: "a".into(), mc_version: "1.20.4".into() },
            Instance { id: "b".into(), mc_version: "1.21.1".into() },
        ]
    }

    fn habit() -> Vec<VersionWeight> {
        vec![VersionWeight { version: "1.21.1".into(), weight: 9 }]
    }

    #[test]
    fn normal_double_click_flow_is_clean() {
        let args = LaunchArgs::default();
        let r = simulate(&server(), &instances(), &habit(), &args, None);
        assert!(r.ok(), "{:?}", r.errors);
        assert!(r.all_popups_closed);
        assert_eq!(r.popup_open_count, 0);
        assert!(r.steps.contains(&Step::InstanceSelected("b".into())));
        assert!(!r.joined_server_directly);
    }

    #[test]
    fn user_choice_ranks_first_in_flow() {
        let args = LaunchArgs::default();
        let r = simulate(&server(), &instances(), &habit(), &args, Some("1.20.4"));
        assert!(r.ok(), "{:?}", r.errors);
        assert!(r.user_choice_honored);
        assert!(r.steps.contains(&Step::InstanceSelected("a".into())));
    }

    #[test]
    fn single_arg_bypasses_selection_and_joins_server() {
        let args = LaunchArgs::parse(["--server", "mc.example.net:25565"]).unwrap();
        let r = simulate(&server(), &instances(), &habit(), &args, None);
        assert!(r.ok(), "{:?}", r.errors);
        assert!(r.joined_server_directly);
        assert!(r.steps.iter().any(|s| matches!(s, Step::DirectJoinByArg(_))));
    }

    #[test]
    fn no_popup_is_left_open_after_any_path() {
        for (args, choice) in [
            (LaunchArgs::default(), None),
            (LaunchArgs::default(), Some("1.20.4")),
            (LaunchArgs::parse(["--server", "x"]).unwrap(), None),
        ] {
            let r = simulate(&server(), &instances(), &habit(), &args, choice);
            assert_eq!(r.popup_open_count, 0);
            assert!(r.all_popups_closed);
        }
    }

    #[test]
    fn flow_trace_contains_close_step() {
        let r = simulate(&server(), &instances(), &habit(), &LaunchArgs::default(), None);
        assert!(r.steps.contains(&Step::PopupsAllClosed));
        assert!(r.steps.contains(&Step::FlowDone));
    }
}

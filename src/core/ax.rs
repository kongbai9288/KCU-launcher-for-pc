#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum AxState {
    Planned,
    DataLayer,
    GateOnly,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct AxSpec {
    pub id: &'static str,
    pub name: &'static str,
    pub state: AxState,
    pub conflict: &'static str,
    pub ui: bool,
}

pub(crate) const AX_SPECS: &[AxSpec] = &[
    AxSpec { id: "AX01", name: "home_widgets", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX02", name: "game_news", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX03", name: "world_editor", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX04", name: "mod_rollback", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX05", name: "storage_analysis", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX06", name: "download_history", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX07", name: "doh_support", state: AxState::Planned, conflict: "network_io_not_started", ui: false },
    AxSpec { id: "AX08", name: "instance_import", state: AxState::Planned, conflict: "", ui: true },
    AxSpec { id: "AX09", name: "upgrade_compat", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX10", name: "first_run_wizard", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX11", name: "settings_export", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX12", name: "download_sources", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX13", name: "appearance_modes", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX14", name: "skin_editor", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX15", name: "studio_image_editor", state: AxState::Planned, conflict: "", ui: true },
    AxSpec { id: "AX16", name: "cn_search_filter", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX17", name: "banner_designer", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX18", name: "lab_generators", state: AxState::DataLayer, conflict: "ai_provider_ui_excluded", ui: true },
    AxSpec { id: "AX19", name: "seed_map", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX20", name: "projection_workshop", state: AxState::Planned, conflict: "", ui: true },
    AxSpec { id: "AX21", name: "redstone_multiplayer", state: AxState::DataLayer, conflict: "", ui: true },
    AxSpec { id: "AX22", name: "shimu_account", state: AxState::Planned, conflict: "", ui: true },
    AxSpec { id: "AX23", name: "client_ai_gate", state: AxState::GateOnly, conflict: "11:18 gate_only_no_ui", ui: false },
    AxSpec { id: "AX24", name: "ungrouped_drop", state: AxState::DataLayer, conflict: "", ui: true },
];

pub(crate) fn by_id(id: &str) -> Option<&'static AxSpec> {
    AX_SPECS.iter().find(|s| s.id == id)
}

pub(crate) fn count_by_state(state: AxState) -> usize {
    AX_SPECS.iter().filter(|s| s.state == state).count()
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::BTreeSet;

    #[test]
    fn twenty_four_unique_specs() {
        assert_eq!(AX_SPECS.len(), 24);
        let ids: BTreeSet<_> = AX_SPECS.iter().map(|s| s.id).collect();
        assert_eq!(ids.len(), 24);
        for i in 1..=24 {
            assert!(by_id(&format!("AX{:02}", i)).is_some());
        }
    }

    #[test]
    fn ax23_is_gate_only_without_ui() {
        let s = by_id("AX23").unwrap();
        assert_eq!(s.state, AxState::GateOnly);
        assert!(!s.ui);
        assert!(s.conflict.contains("no_ui"));
    }

    #[test]
    fn ax05_is_data_layer_this_round() {
        for id in ["AX05", "AX06", "AX11", "AX12", "AX17", "AX24", "AX01", "AX13", "AX10", "AX14", "AX09", "AX16", "AX18", "AX19", "AX21", "AX02", "AX03", "AX04"] {
            assert_eq!(by_id(id).unwrap().state, AxState::DataLayer);
        }
        assert_eq!(count_by_state(AxState::DataLayer), 18);
        assert_eq!(count_by_state(AxState::GateOnly), 1);
        assert_eq!(count_by_state(AxState::Planned), 5);
    }

    #[test]
    fn excluded_subitem_is_recorded_not_silently_dropped() {
        assert!(by_id("AX18").unwrap().conflict.contains("ai_provider_ui_excluded"));
    }

    #[test]
    fn network_io_dependency_is_recorded() {
        assert!(by_id("AX07").unwrap().conflict.contains("network_io_not_started"));
    }

    #[test]
    fn unknown_id_is_rejected() {
        assert!(by_id("AX25").is_none());
        assert!(by_id("").is_none());
    }
}

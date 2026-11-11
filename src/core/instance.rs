#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Instance {
    pub id: String,
    pub mc_version: String,
}

#[derive(Debug, Clone)]
pub struct ServerEntry {
    pub name: String,
    pub address: String,
    pub supported_versions: Vec<String>,
}

#[derive(Debug, Clone)]
pub struct VersionWeight {
    pub version: String,
    pub weight: u32,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SelectError {
    NoCompatibleInstance,
    UserChoiceNotCompatible(String),
}

pub fn select_instance(
    server: &ServerEntry,
    instances: &[Instance],
    habit: &[VersionWeight],
    user_choice: Option<&str>,
) -> Result<Instance, SelectError> {
    if let Some(choice) = user_choice {
        if !server.supported_versions.iter().any(|v| v == choice) {
            return Err(SelectError::UserChoiceNotCompatible(choice.to_string()));
        }
        if let Some(i) = instances.iter().find(|i| i.mc_version == choice) {
            return Ok(i.clone());
        }
    }

    let mut scored: Vec<(u32, u32, &Instance)> = Vec::new();
    for (rank, i) in instances.iter().enumerate() {
        if !server.supported_versions.contains(&i.mc_version) {
            continue;
        }
        let w = habit
            .iter()
            .find(|h| h.version == i.mc_version)
            .map(|h| h.weight)
            .unwrap_or(0);
        scored.push((w, rank as u32, i));
    }

    scored.sort_by(|a, b| b.0.cmp(&a.0).then_with(|| a.1.cmp(&b.1)));
    scored
        .first()
        .map(|(_, _, i)| (*i).clone())
        .ok_or(SelectError::NoCompatibleInstance)
}

#[cfg(test)]
mod tests {
    use super::*;

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
            Instance { id: "c".into(), mc_version: "1.16.5".into() },
        ]
    }

    #[test]
    fn user_choice_ranks_first() {
        let habit = vec![VersionWeight { version: "1.21.1".into(), weight: 999 }];
        let got = select_instance(&server(), &instances(), &habit, Some("1.20.4")).unwrap();
        assert_eq!(got.id, "a");
    }

    #[test]
    fn habit_weight_picks_compatible_instance() {
        let habit = vec![
            VersionWeight { version: "1.20.4".into(), weight: 3 },
            VersionWeight { version: "1.21.1".into(), weight: 9 },
        ];
        let got = select_instance(&server(), &instances(), &habit, None).unwrap();
        assert_eq!(got.id, "b");
    }

    #[test]
    fn unsupported_version_is_never_selected() {
        let habit = vec![VersionWeight { version: "1.16.5".into(), weight: 1000 }];
        let got = select_instance(&server(), &instances(), &habit, None).unwrap();
        assert_ne!(got.mc_version, "1.16.5");
    }

    #[test]
    fn no_compatible_instance_reports_error() {
        let s = ServerEntry {
            name: "S".into(),
            address: "x".into(),
            supported_versions: vec!["1.7.10".into()],
        };
        assert_eq!(
            select_instance(&s, &instances(), &[], None),
            Err(SelectError::NoCompatibleInstance)
        );
    }

    #[test]
    fn incompatible_user_choice_reports_error() {
        assert_eq!(
            select_instance(&server(), &instances(), &[], Some("1.7.10")),
            Err(SelectError::UserChoiceNotCompatible("1.7.10".into()))
        );
    }
}

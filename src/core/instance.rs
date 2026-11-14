use semver::{Version, VersionReq};
use std::cmp::Ordering;

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

fn is_range_expr(s: &str) -> bool {
    s.chars()
        .any(|c| matches!(c, '^' | '~' | '>' | '<' | '=' | '*' | ',' | '|' | 'x' | 'X' | ' ' | '\t'))
}

fn versions_match(supported: &str, candidate: &str) -> bool {
    if supported == candidate {
        return true;
    }
    if is_range_expr(supported) {
        return match (VersionReq::parse(supported), Version::parse(candidate)) {
            (Ok(req), Ok(v)) => req.matches(&v),
            _ => false,
        };
    }
    match (Version::parse(supported), Version::parse(candidate)) {
        (Ok(a), Ok(b)) => a.cmp_precedence(&b) == Ordering::Equal,
        _ => false,
    }
}

pub fn select_instance(
    server: &ServerEntry,
    instances: &[Instance],
    habit: &[VersionWeight],
    user_choice: Option<&str>,
) -> Result<Instance, SelectError> {
    if let Some(choice) = user_choice {
        if !server
            .supported_versions
            .iter()
            .any(|v| versions_match(v, choice) || versions_match(choice, v))
        {
            return Err(SelectError::UserChoiceNotCompatible(choice.to_string()));
        }
        if let Some(i) = instances
            .iter()
            .find(|i| i.mc_version == choice)
            .or_else(|| instances.iter().find(|i| versions_match(choice, &i.mc_version)))
        {
            return Ok(i.clone());
        }
    }

    let mut scored: Vec<(u32, u32, &Instance)> = Vec::new();
    for (rank, i) in instances.iter().enumerate() {
        if !server
            .supported_versions
            .iter()
            .any(|v| versions_match(v, &i.mc_version))
        {
            continue;
        }
        let w = habit
            .iter()
            .find(|h| versions_match(&h.version, &i.mc_version))
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

    fn inst(id: &str, v: &str) -> Instance {
        Instance { id: id.into(), mc_version: v.into() }
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

    #[test]
    fn build_metadata_is_ignored_by_the_library() {
        let s = ServerEntry {
            name: "S".into(),
            address: "paper.example.net".into(),
            supported_versions: vec!["1.20.4+paper.381".into()],
        };
        let got = select_instance(&s, &[inst("p", "1.20.4")], &[], None).unwrap();
        assert_eq!(got.id, "p");
        assert!(versions_match("1.20.4+paper.381", "1.20.4"));
    }

    #[test]
    fn prerelease_is_not_treated_as_release() {
        assert!(!versions_match("1.20.4", "1.20.4-pre1"));
        assert!(!versions_match("1.20.4-pre1", "1.20.4"));
    }

    #[test]
    fn range_expression_matches_within_bounds() {
        let s = ServerEntry {
            name: "S".into(),
            address: "x".into(),
            supported_versions: vec![">=1.20.0, <1.21.0".into()],
        };
        let list = [inst("a", "1.20.4"), inst("b", "1.21.1")];
        let got = select_instance(&s, &list, &[], None).unwrap();
        assert_eq!(got.id, "a");
    }

    #[test]
    fn wildcard_range_is_supported() {
        assert!(versions_match("1.20.x", "1.20.4"));
        assert!(!versions_match("1.20.x", "1.21.1"));
    }

    #[test]
    fn snapshot_version_falls_back_to_exact_string() {
        assert!(versions_match("23w31a", "23w31a"));
        assert!(!versions_match("23w31a", "23w32a"));
        let s = ServerEntry {
            name: "S".into(),
            address: "x".into(),
            supported_versions: vec!["23w31a".into()],
        };
        let got = select_instance(&s, &[inst("snap", "23w31a")], &[], None).unwrap();
        assert_eq!(got.id, "snap");
    }

    #[test]
    fn malformed_range_never_crashes() {
        assert!(!versions_match(">=not-a-version", "1.20.4"));
        assert!(!versions_match("^1.20", "not-a-version"));
        assert!(!versions_match("", "1.20.4"));
    }

    #[test]
    fn plain_version_stays_exact_not_caret() {
        assert!(versions_match("1.20.4", "1.20.4"));
        assert!(!versions_match("1.20.4", "1.20.5"));
        assert!(!versions_match("1.20.4", "1.21.1"));
    }

    #[test]
    fn habit_key_can_use_range() {
        let s = ServerEntry {
            name: "S".into(),
            address: "x".into(),
            supported_versions: vec!["1.20.x".into()],
        };
        let habit = vec![VersionWeight { version: "1.20.x".into(), weight: 7 }];
        let got = select_instance(&s, &[inst("a", "1.20.1"), inst("b", "1.20.4")], &habit, None).unwrap();
        assert_eq!(got.id, "a");
    }
}

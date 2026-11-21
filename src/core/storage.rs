pub const BUCKETS: &[&str] = &[
    "instances",
    "backups",
    "shared_resources",
    "caches",
    "external_game_dirs",
];
pub const CLEANABLE: &[&str] = &["downloaded_caches", "unused_metadata"];
pub const PROTECTED: &[&str] = &[
    "installed_games",
    "saves",
    "backups",
    "offline_or_recovery_files",
];

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StorageBucket {
    pub name: String,
    pub bytes: u64,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct StorageReport {
    pub buckets: Vec<StorageBucket>,
    pub total_bytes: u64,
    pub cleanable: Vec<String>,
    pub protected: Vec<String>,
    pub degraded: bool,
}

pub fn analyze(input: &[(&str, u64)]) -> StorageReport {
    let mut buckets = Vec::new();
    let mut total: u64 = 0;
    let mut degraded = input.is_empty();
    for (name, bytes) in input {
        if !BUCKETS.contains(name) {
            degraded = true;
            continue;
        }
        buckets.push(StorageBucket { name: (*name).to_string(), bytes: *bytes });
        total = total.saturating_add(*bytes);
    }
    StorageReport {
        buckets,
        total_bytes: total,
        cleanable: CLEANABLE.iter().map(|s| (*s).to_string()).collect(),
        protected: PROTECTED.iter().map(|s| (*s).to_string()).collect(),
        degraded,
    }
}

pub fn cleanup_scope(report: &StorageReport) -> Vec<String> {
    report.cleanable.clone()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn five_buckets_are_known() {
        assert_eq!(BUCKETS.len(), 5);
        let r = analyze(&[("instances", 10), ("backups", 20), ("shared_resources", 30), ("caches", 40), ("external_game_dirs", 50)]);
        assert_eq!(r.buckets.len(), 5);
        assert_eq!(r.total_bytes, 150);
        assert!(!r.degraded);
    }

    #[test]
    fn unknown_bucket_is_degraded_and_skipped() {
        let r = analyze(&[("instances", 10), ("../evil", 999)]);
        assert_eq!(r.buckets.len(), 1);
        assert_eq!(r.total_bytes, 10);
        assert!(r.degraded);
    }

    #[test]
    fn empty_input_is_degraded() {
        let r = analyze(&[]);
        assert!(r.degraded);
        assert_eq!(r.total_bytes, 0);
    }

    #[test]
    fn saturating_sum_does_not_wrap() {
        let r = analyze(&[("caches", u64::MAX), ("backups", 1)]);
        assert_eq!(r.total_bytes, u64::MAX);
    }

    #[test]
    fn cleanup_never_touches_protected() {
        let r = analyze(&[("caches", 1)]);
        let scope = cleanup_scope(&r);
        assert_eq!(scope, vec!["downloaded_caches".to_string(), "unused_metadata".to_string()]);
        for p in PROTECTED {
            assert!(!scope.contains(&p.to_string()), "protected={}", p);
        }
    }

    #[test]
    fn protected_list_matches_policy() {
        assert_eq!(PROTECTED.len(), 4);
        assert!(PROTECTED.contains(&"saves"));
        assert!(PROTECTED.contains(&"backups"));
    }
}

use anyhow::{anyhow, Result};
use semver::Version;
use std::cmp::Ordering;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Decision {
    Install,
    Keep,
    Reject,
}

#[derive(Debug, Clone, Default)]
pub struct UpdatePolicy {
    pub explicit_target: Option<String>,
    pub rollback_confirmed: bool,
}

pub fn decide(current: &str, candidate: &str, policy: &UpdatePolicy) -> Result<Decision> {
    let a = Version::parse(current).map_err(|e| anyhow!("current version: {:?}", e))?;
    let b = Version::parse(candidate).map_err(|e| anyhow!("candidate version: {:?}", e))?;

    match b.cmp_precedence(&a) {
        Ordering::Greater => return Ok(Decision::Install),
        Ordering::Equal => return Ok(Decision::Keep),
        Ordering::Less => {}
    }
    let target_matches = policy
        .explicit_target
        .as_deref()
        .map(|t| Version::parse(t).map(|v| v == b).unwrap_or(false))
        .unwrap_or(false);
    if target_matches && policy.rollback_confirmed {
        return Ok(Decision::Install);
    }
    Ok(Decision::Reject)
}

pub fn verify_then_decide(
    public_key: &[u8],
    payload: &[u8],
    signature: &[u8],
    current: &str,
    candidate: &str,
    policy: &UpdatePolicy,
) -> Decision {
    if super::verify::verify_detached(public_key, payload, signature).is_err() {
        return Decision::Keep;
    }
    decide(current, candidate, policy).unwrap_or(Decision::Keep)
}

#[cfg(test)]
mod tests {
    use super::*;
    use ed25519_compact::{KeyPair, Seed};

    fn signed(payload: &[u8]) -> (Vec<u8>, Vec<u8>) {
        let kp = KeyPair::from_seed(Seed::from_slice(&[3u8; 32]).unwrap());
        let sig = kp.sk.sign(payload, None);
        (kp.pk.as_ref().to_vec(), sig.as_ref().to_vec())
    }

    #[test]
    fn newer_version_installs() {
        assert_eq!(decide("1.2.3", "1.2.4", &UpdatePolicy::default()).unwrap(), Decision::Install);
    }

    #[test]
    fn same_version_keeps() {
        assert_eq!(decide("1.2.3", "1.2.3", &UpdatePolicy::default()).unwrap(), Decision::Keep);
    }

    #[test]
    fn downgrade_is_rejected_by_default() {
        assert_eq!(decide("1.2.3", "1.2.2", &UpdatePolicy::default()).unwrap(), Decision::Reject);
    }

    #[test]
    fn downgrade_needs_both_explicit_target_and_confirmation() {
        let only_target = UpdatePolicy { explicit_target: Some("1.2.2".into()), rollback_confirmed: false };
        let only_confirm = UpdatePolicy { explicit_target: None, rollback_confirmed: true };
        let both = UpdatePolicy { explicit_target: Some("1.2.2".into()), rollback_confirmed: true };
        assert_eq!(decide("1.2.3", "1.2.2", &only_target).unwrap(), Decision::Reject);
        assert_eq!(decide("1.2.3", "1.2.2", &only_confirm).unwrap(), Decision::Reject);
        assert_eq!(decide("1.2.3", "1.2.2", &both).unwrap(), Decision::Install);
    }

    #[test]
    fn malformed_version_returns_error() {
        assert!(decide("not-a-version", "1.2.3", &UpdatePolicy::default()).is_err());
        assert!(decide("1.2.3", "", &UpdatePolicy::default()).is_err());
    }

    #[test]
    fn build_metadata_does_not_force_reinstall() {
        assert_eq!(decide("1.2.3+old", "1.2.3+new", &UpdatePolicy::default()).unwrap(), Decision::Keep);
    }

    #[test]
    fn signature_failure_keeps_old_plugin() {
        let (pk, sig) = signed(b"plugin-1.2.4");
        assert_eq!(
            verify_then_decide(&pk, b"plugin-1.2.4-TAMPERED", &sig, "1.2.3", "1.2.4", &UpdatePolicy::default()),
            Decision::Keep
        );
    }

    #[test]
    fn valid_signature_and_newer_version_installs() {
        let (pk, sig) = signed(b"plugin-1.2.4");
        assert_eq!(
            verify_then_decide(&pk, b"plugin-1.2.4", &sig, "1.2.3", "1.2.4", &UpdatePolicy::default()),
            Decision::Install
        );
    }

    #[test]
    fn malformed_version_after_valid_signature_keeps_old_plugin() {
        let (pk, sig) = signed(b"plugin");
        assert_eq!(
            verify_then_decide(&pk, b"plugin", &sig, "bad", "1.2.4", &UpdatePolicy::default()),
            Decision::Keep
        );
    }
}

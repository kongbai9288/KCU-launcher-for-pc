use anyhow::{anyhow, Result};
use semver::Version;
use std::cmp::Ordering;

use crate::plugins::identity::Identity;
use crate::updater::verify::verify_detached;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum UpgradeDecision {
    Install,
    Keep,
    Reject,
}

#[derive(Debug, Clone, Default)]
pub struct UpgradeRequest {
    pub installed_identity: Option<Identity>,
    pub installed_version: Option<String>,
    pub candidate_identity: Identity,
    pub candidate_version: String,
    pub public_key: Vec<u8>,
    pub payload: Vec<u8>,
    pub signature: Vec<u8>,
    pub user_confirmed_upgrade: bool,
    pub explicit_target: Option<String>,
    pub rollback_confirmed: bool,
}

pub fn decide_upgrade(req: &UpgradeRequest) -> Result<UpgradeDecision> {
    if verify_detached(&req.public_key, &req.payload, &req.signature).is_err() {
        return Ok(UpgradeDecision::Keep);
    }
    let installed = match (&req.installed_identity, &req.installed_version) {
        (Some(id), Some(v)) if *id == req.candidate_identity => {
            Version::parse(v).map_err(|e| anyhow!("installed version: {:?}", e))?
        }
        _ => return Ok(UpgradeDecision::Install),
    };
    let candidate = Version::parse(&req.candidate_version)
        .map_err(|e| anyhow!("candidate version: {:?}", e))?;

    match candidate.cmp_precedence(&installed) {
        Ordering::Greater => {
            if req.user_confirmed_upgrade {
                Ok(UpgradeDecision::Install)
            } else {
                Ok(UpgradeDecision::Keep)
            }
        }
        Ordering::Equal => Ok(UpgradeDecision::Keep),
        Ordering::Less => {
            let target_matches = req
                .explicit_target
                .as_deref()
                .map(|t| Version::parse(t).map(|v| v.cmp_precedence(&candidate) == Ordering::Equal).unwrap_or(false))
                .unwrap_or(false);
            if target_matches && req.rollback_confirmed && req.user_confirmed_upgrade {
                Ok(UpgradeDecision::Install)
            } else {
                Ok(UpgradeDecision::Reject)
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::plugins::identity::identity_hash;
    use ed25519_compact::{KeyPair, Seed};

    fn key() -> Vec<u8> {
        KeyPair::from_seed(Seed::from_slice(&[5u8; 32]).unwrap())
            .pk
            .as_ref()
            .to_vec()
    }

    fn signed(payload: &[u8]) -> Vec<u8> {
        let kp = KeyPair::from_seed(Seed::from_slice(&[5u8; 32]).unwrap());
        kp.sk.sign(payload, None).as_ref().to_vec()
    }

    fn base(identity: &str, installed: Option<&str>, candidate: &str) -> UpgradeRequest {
        UpgradeRequest {
            installed_identity: installed.map(|_| identity_hash(identity)),
            installed_version: installed.map(str::to_string),
            candidate_identity: identity_hash(identity),
            candidate_version: candidate.to_string(),
            public_key: key(),
            payload: b"plugin-package".to_vec(),
            signature: signed(b"plugin-package"),
            ..Default::default()
        }
    }

    #[test]
    fn same_identity_newer_version_needs_manual_confirmation() {
        let req = base("kcu.plugin.a", Some("1.2.3"), "1.3.0");
        assert_eq!(decide_upgrade(&req).unwrap(), UpgradeDecision::Keep);
        let mut ok = req.clone();
        ok.user_confirmed_upgrade = true;
        assert_eq!(decide_upgrade(&ok).unwrap(), UpgradeDecision::Install);
    }

    #[test]
    fn different_identity_is_new_install_not_upgrade() {
        let mut req = base("kcu.plugin.a", Some("1.2.3"), "1.3.0");
        req.installed_identity = Some(identity_hash("kcu.plugin.b"));
        assert_eq!(decide_upgrade(&req).unwrap(), UpgradeDecision::Install);
    }

    #[test]
    fn no_installed_plugin_is_new_install() {
        let req = base("kcu.plugin.a", None, "1.0.0");
        assert_eq!(decide_upgrade(&req).unwrap(), UpgradeDecision::Install);
    }

    #[test]
    fn same_version_keeps() {
        let mut req = base("kcu.plugin.a", Some("1.2.3"), "1.2.3");
        req.user_confirmed_upgrade = true;
        assert_eq!(decide_upgrade(&req).unwrap(), UpgradeDecision::Keep);
    }

    #[test]
    fn build_metadata_difference_keeps() {
        let mut req = base("kcu.plugin.a", Some("1.2.3+old"), "1.2.3+new");
        req.user_confirmed_upgrade = true;
        assert_eq!(decide_upgrade(&req).unwrap(), UpgradeDecision::Keep);
    }

    #[test]
    fn downgrade_still_needs_all_three_conditions() {
        let mut req = base("kcu.plugin.a", Some("1.3.0"), "1.2.3");
        req.explicit_target = Some("1.2.3".into());
        req.rollback_confirmed = true;
        assert_eq!(decide_upgrade(&req).unwrap(), UpgradeDecision::Reject);
        req.user_confirmed_upgrade = true;
        assert_eq!(decide_upgrade(&req).unwrap(), UpgradeDecision::Install);
    }

    #[test]
    fn signature_failure_keeps_old_plugin_even_if_confirmed() {
        let mut req = base("kcu.plugin.a", Some("1.2.3"), "1.3.0");
        req.user_confirmed_upgrade = true;
        req.payload = b"plugin-package-TAMPERED".to_vec();
        assert_eq!(decide_upgrade(&req).unwrap(), UpgradeDecision::Keep);
    }

    #[test]
    fn malformed_version_returns_error_not_panic() {
        let req = base("kcu.plugin.a", Some("not-a-version"), "1.3.0");
        assert!(decide_upgrade(&req).is_err());
        let req2 = base("kcu.plugin.a", Some("1.2.3"), "");
        assert!(decide_upgrade(&req2).is_err());
    }

    #[test]
    fn truncated_key_does_not_panic() {
        let mut req = base("kcu.plugin.a", Some("1.2.3"), "1.3.0");
        req.public_key.truncate(8);
        assert_eq!(decide_upgrade(&req).unwrap(), UpgradeDecision::Keep);
    }
}

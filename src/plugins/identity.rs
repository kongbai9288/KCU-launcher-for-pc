use ed25519_compact::sha512;

pub const IDENTITY_HEX_LEN: usize = 32;

#[derive(Debug, Clone, Default, PartialEq, Eq, Hash)]
pub struct Identity(pub String);

pub fn identity_hash(plugin_id: &str) -> Identity {
    let digest = sha512::Hash::hash(plugin_id.as_bytes());
    let bytes: Vec<u8> = digest
        .iter()
        .take(IDENTITY_HEX_LEN / 2)
        .copied()
        .collect();
    Identity(hex::encode(bytes))
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn same_id_same_identity() {
        assert_eq!(identity_hash("kcu.plugin.recommend"), identity_hash("kcu.plugin.recommend"));
    }

    #[test]
    fn different_id_different_identity() {
        assert_ne!(identity_hash("kcu.plugin.recommend"), identity_hash("kcu.plugin.status"));
    }

    #[test]
    fn empty_id_is_stable_and_nonempty() {
        let a = identity_hash("");
        assert_eq!(a.0.len(), IDENTITY_HEX_LEN);
        assert_eq!(a, identity_hash(""));
    }

    #[test]
    fn digest_is_hex_lowercase() {
        let a = identity_hash("anything");
        assert!(a.0.bytes().all(|c| c.is_ascii_digit() || (b'a'..=b'f').contains(&c)));
    }

    #[test]
    fn unicode_id_is_hashed_by_utf8_bytes() {
        assert_eq!(identity_hash("插件·甲"), identity_hash("插件·甲"));
        assert_ne!(identity_hash("插件·甲"), identity_hash("插件·乙"));
    }

    // 期望值由 Python hashlib.sha512(...).digest()[:16].hex() 独立算出，
    // 不依赖本仓库的 hex / ed25519-compact 实现，用于换库前后行为对齐。
    #[test]
    fn matches_independent_sha512_reference() {
        assert_eq!(identity_hash("kcu.plugin.recommend").0, "d8122f42167ad862c28ae17de745ca5d");
        assert_eq!(identity_hash("kcu.plugin.status").0, "4938c84aee3a3cf091b356266ec1d6a0");
        assert_eq!(identity_hash("").0, "cf83e1357eefb8bdf1542850d66d8007");
        assert_eq!(identity_hash("插件·甲").0, "12bbb4336c14437ae11065c7f1eea84d");
    }

    #[test]
    fn output_is_exactly_32_lowercase_hex_chars() {
        let s = identity_hash("anything").0;
        assert_eq!(s.len(), IDENTITY_HEX_LEN);
        assert!(s.bytes().all(|c| c.is_ascii_digit() || (b'a'..=b'f').contains(&c)));
    }
}

use ed25519_compact::sha512;

pub const IDENTITY_HEX_LEN: usize = 32;

#[derive(Debug, Clone, Default, PartialEq, Eq, Hash)]
pub struct Identity(pub String);

pub fn identity_hash(plugin_id: &str) -> Identity {
    let digest = sha512::Hash::hash(plugin_id.as_bytes());
    let mut s = String::with_capacity(IDENTITY_HEX_LEN);
    for b in digest.iter().take(IDENTITY_HEX_LEN / 2) {
        s.push_str(&format!("{:02x}", b));
    }
    Identity(s)
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
}

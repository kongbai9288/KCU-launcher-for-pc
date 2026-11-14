use anyhow::{anyhow, Result};
use ed25519_compact::{PublicKey, Signature};

pub const PUBLIC_KEY_BYTES: usize = PublicKey::BYTES;
pub const SIGNATURE_BYTES: usize = Signature::BYTES;

pub fn verify_detached(public_key: &[u8], payload: &[u8], signature: &[u8]) -> Result<()> {
    let pk = PublicKey::from_slice(public_key)
        .map_err(|e| anyhow!("invalid public key: {:?}", e))?;
    let sig = Signature::from_slice(signature)
        .map_err(|e| anyhow!("invalid signature encoding: {:?}", e))?;
    pk.verify(payload, &sig)
        .map_err(|e| anyhow!("signature verification failed: {:?}", e))
}

#[cfg(test)]
mod tests {
    use super::*;
    use ed25519_compact::{KeyPair, Seed};

    fn pair() -> KeyPair {
        KeyPair::from_seed(Seed::from_slice(&[7u8; 32]).unwrap())
    }

    fn signed(payload: &[u8]) -> (Vec<u8>, Vec<u8>) {
        let kp = pair();
        let sig = kp.sk.sign(payload, None);
        (kp.pk.as_ref().to_vec(), sig.as_ref().to_vec())
    }

    #[test]
    fn valid_signature_passes() {
        let (pk, sig) = signed(b"kcu-plugin-1.2.3");
        assert!(verify_detached(&pk, b"kcu-plugin-1.2.3", &sig).is_ok());
    }

    #[test]
    fn modified_payload_is_rejected() {
        let (pk, sig) = signed(b"kcu-plugin-1.2.3");
        assert!(verify_detached(&pk, b"kcu-plugin-1.2.4", &sig).is_err());
    }

    #[test]
    fn wrong_public_key_is_rejected() {
        let (_, sig) = signed(b"payload");
        let other = KeyPair::from_seed(Seed::from_slice(&[9u8; 32]).unwrap());
        assert!(verify_detached(other.pk.as_ref(), b"payload", &sig).is_err());
    }

    #[test]
    fn truncated_inputs_return_error_not_panic() {
        assert!(verify_detached(&[0u8; 31], b"payload", &[0u8; 64]).is_err());
        assert!(verify_detached(&[0u8; 32], b"payload", &[0u8; 63]).is_err());
        assert!(verify_detached(&[], b"payload", &[]).is_err());
    }

    #[test]
    fn empty_payload_can_still_be_verified() {
        let (pk, sig) = signed(b"");
        assert!(verify_detached(&pk, b"", &sig).is_ok());
    }

    #[test]
    fn signature_bytes_are_not_swapped() {
        let (pk, mut sig) = signed(b"payload");
        sig.swap(0, 63);
        assert!(verify_detached(&pk, b"payload", &sig).is_err());
    }
}

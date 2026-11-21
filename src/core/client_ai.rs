#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ClientAiGate;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ClientAiError {
    NotEnabled,
    NoSurface,
}

impl ClientAiGate {
    pub fn new() -> Self {
        ClientAiGate
    }

    pub fn enabled(&self) -> bool {
        false
    }

    pub fn surface_count(&self) -> usize {
        0
    }

    pub fn submit(&self, _payload: &str) -> std::result::Result<String, ClientAiError> {
        Err(ClientAiError::NotEnabled)
    }
}

impl Default for ClientAiGate {
    fn default() -> Self {
        Self::new()
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn one_gate_denies_by_default() {
        let g = ClientAiGate::new();
        assert!(!g.enabled());
        assert_eq!(g.surface_count(), 0);
    }

    #[test]
    fn submit_never_runs() {
        let g = ClientAiGate::default();
        assert_eq!(g.submit("query"), Err(ClientAiError::NotEnabled));
        assert_eq!(g.submit(""), Err(ClientAiError::NotEnabled));
    }

    #[test]
    fn gate_has_no_state() {
        assert_eq!(std::mem::size_of::<ClientAiGate>(), 0);
    }

    #[test]
    fn error_variants_are_distinct() {
        assert_ne!(ClientAiError::NotEnabled, ClientAiError::NoSurface);
    }
}

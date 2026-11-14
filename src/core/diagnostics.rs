use crate::core::log::LogBuffer;
use log::Level;

pub fn diag_line(domain: &str, action: &str, target: &str, result: &str, detail: &str) -> String {
    format!("[KCU] {} {} {} {} {}", domain, action, target, result, detail)
}

pub fn emit(buf: &LogBuffer, domain: &str, action: &str, target: &str, result: &str, detail: &str) {
    buf.record(
        format_args!("[KCU] {} {} {} {} {}", domain, action, target, result, detail),
        Level::Info,
        "kcu.diag",
    );
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn shape_is_fixed() {
        assert_eq!(
            diag_line("core", "start", "paths", "OK", "root=KCU"),
            "[KCU] core start paths OK root=KCU"
        );
    }

    #[test]
    fn single_line() {
        let s = diag_line("ui", "close", "popup", "OK", "id=eula");
        assert!(!s.contains('\n'));
    }

    #[test]
    fn emit_uses_logging_facade() {
        let b = LogBuffer::new(10);
        emit(&b, "core", "start", "paths", "OK", "root=KCU");
        let parts = b.take_shards();
        assert_eq!(parts[0][0], "[KCU] core start paths OK root=KCU");
    }
}

pub fn diag_line(domain: &str, action: &str, target: &str, result: &str, detail: &str) -> String {
    format!("[KCU] {} {} {} {} {}", domain, action, target, result, detail)
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
}

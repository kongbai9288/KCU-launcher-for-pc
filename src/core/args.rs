#[derive(Debug, Clone, Default, PartialEq, Eq)]
pub struct LaunchArgs {
    pub server: Option<String>,
    pub instance: Option<String>,
    pub mode: Option<String>,
    pub kculf: Option<String>,
    pub kculh: Option<String>,
    pub lang: Option<String>,
    pub extras: Vec<String>,
}

impl LaunchArgs {
    pub fn parse<I, S>(xs: I) -> Result<Self, String>
    where
        I: IntoIterator<Item = S>,
        S: Into<String>,
    {
        let mut a = Self::default();
        let mut it = xs.into_iter().map(Into::into).peekable();
        while let Some(tok) = it.next() {
            match tok.as_str() {
                "--server" | "--join-server" => {
                    a.server = Some(it.next().ok_or_else(|| "--server requires a value".to_string())?);
                }
                "--instance" => {
                    a.instance = Some(it.next().ok_or_else(|| "--instance requires a value".to_string())?);
                }
                "--mode" => {
                    a.mode = Some(it.next().ok_or_else(|| "--mode requires a value".to_string())?);
                }
                "--kculf" => {
                    a.kculf = Some(it.next().ok_or_else(|| "--kculf requires a value".to_string())?);
                }
                "--kculh" => {
                    a.kculh = Some(it.next().ok_or_else(|| "--kculh requires a value".to_string())?);
                }
                "--lang" => {
                    a.lang = Some(it.next().ok_or_else(|| "--lang requires a value".to_string())?);
                }
                other if other.starts_with('-') => {
                    return Err(format!("unknown flag: {}", other));
                }
                other => a.extras.push(other.to_string()),
            }
        }
        Ok(a)
    }

    pub fn joins_server(&self) -> bool {
        self.server.is_some()
    }

    pub fn headless(&self) -> bool {
        self.kculh.is_some() || self.mode.as_deref() == Some("headless")
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn single_arg_joins_server() {
        let a = LaunchArgs::parse(["--server", "mc.example.net:25565"]).unwrap();
        assert!(a.joins_server());
        assert_eq!(a.server.as_deref(), Some("mc.example.net:25565"));
    }

    #[test]
    fn alias_joins_server() {
        assert!(LaunchArgs::parse(["--join-server", "a"]).unwrap().joins_server());
    }

    #[test]
    fn missing_value_is_rejected() {
        assert!(LaunchArgs::parse(["--server"]).is_err());
    }

    #[test]
    fn unknown_flag_is_rejected() {
        assert!(LaunchArgs::parse(["--nope"]).is_err());
    }

    #[test]
    fn kculf_and_kculh_are_separate() {
        let a = LaunchArgs::parse(["--kculf", "x.kculf", "--kculh", "y.kculh"]).unwrap();
        assert_eq!(a.kculf.as_deref(), Some("x.kculf"));
        assert_eq!(a.kculh.as_deref(), Some("y.kculh"));
        assert!(a.headless());
    }
}

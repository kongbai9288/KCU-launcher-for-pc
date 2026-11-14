use lexopt::prelude::*;

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
        let raw: Vec<String> = xs.into_iter().map(Into::into).collect();
        let mut parser = lexopt::Parser::from_args(raw);
        let mut a = Self::default();
        while let Some(arg) = parser.next().map_err(|e| e.to_string())? {
            match arg {
                Long("server") | Long("join-server") => {
                    a.server = Some(value(&mut parser)?);
                }
                Long("instance") => {
                    a.instance = Some(value(&mut parser)?);
                }
                Long("mode") => {
                    a.mode = Some(value(&mut parser)?);
                }
                Long("kculf") => {
                    a.kculf = Some(value(&mut parser)?);
                }
                Long("kculh") => {
                    a.kculh = Some(value(&mut parser)?);
                }
                Long("lang") => {
                    a.lang = Some(value(&mut parser)?);
                }
                Value(v) => a.extras.push(
                    v.into_string()
                        .map_err(|_| "positional value is not valid unicode".to_string())?,
                ),
                other => return Err(other.unexpected().to_string()),
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

fn value(parser: &mut lexopt::Parser) -> Result<String, String> {
    let v = parser.value().map_err(|e| e.to_string())?;
    v.into_string().map_err(|_| "value is not valid unicode".to_string())
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

    #[test]
    fn equals_syntax_is_accepted() {
        let a = LaunchArgs::parse(["--instance=alpha"]).unwrap();
        assert_eq!(a.instance.as_deref(), Some("alpha"));
    }

    #[test]
    fn double_dash_marks_remaining_as_positional() {
        let a = LaunchArgs::parse(["--", "--server", "literal"]).unwrap();
        assert_eq!(a.extras, vec!["--server".to_string(), "literal".to_string()]);
        assert!(!a.joins_server());
    }

    #[test]
    fn positional_extras_are_kept() {
        let a = LaunchArgs::parse(["pack.mrpack", "--lang", "en-US"]).unwrap();
        assert_eq!(a.extras, vec!["pack.mrpack".to_string()]);
        assert_eq!(a.lang.as_deref(), Some("en-US"));
    }
}

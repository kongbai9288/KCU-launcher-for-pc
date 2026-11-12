pub const LOW_MEMORY_BYTES: u64 = 2 * 1024 * 1024 * 1024;

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Mode {
    Lightweight,
    Normal,
    Headless,
    Safe,
}

impl Mode {
    pub fn code(&self) -> &'static str {
        match self {
            Mode::Lightweight => "lightweight",
            Mode::Normal => "normal",
            Mode::Headless => "headless",
            Mode::Safe => "safe",
        }
    }

    pub fn parse(s: &str) -> Option<Mode> {
        match s {
            "lightweight" => Some(Mode::Lightweight),
            "normal" => Some(Mode::Normal),
            "headless" => Some(Mode::Headless),
            "safe" => Some(Mode::Safe),
            _ => None,
        }
    }

    pub fn loads_ui(&self) -> bool {
        *self == Mode::Normal
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Fallback {
    Zero,
    One,
    Two,
    Three,
}

impl Fallback {
    pub fn code(&self) -> &'static str {
        match self {
            Fallback::Zero => "0",
            Fallback::One => "1",
            Fallback::Two => "2",
            Fallback::Three => "3",
        }
    }
}

#[derive(Debug, Clone, Default)]
pub struct ModeInput {
    pub mem_bytes: u64,
    pub memory_unknown: bool,
    pub first_run: bool,
    pub config_mode: Option<String>,
    pub args_mode: Option<String>,
    pub task_mode: Option<String>,
    pub force_headless: bool,
    pub credential_present: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ModeSelection {
    pub mode: Mode,
    pub reason: &'static str,
    pub fallback: Fallback,
    pub premium_allowed: bool,
    pub ui_loaded: bool,
    pub memory_degraded: bool,
}

impl ModeSelection {
    fn build(mode: Mode, reason: &'static str, input: &ModeInput) -> Self {
        let premium_allowed = match mode {
            Mode::Headless => input.credential_present,
            Mode::Safe => false,
            _ => true,
        };
        let fallback = match mode {
            Mode::Headless if !input.credential_present => Fallback::One,
            Mode::Safe => Fallback::Two,
            _ if input.memory_unknown => Fallback::Two,
            _ => Fallback::Three,
        };
        Self {
            ui_loaded: mode.loads_ui(),
            memory_degraded: input.memory_unknown && mode == Mode::Normal,
            mode,
            reason,
            fallback,
            premium_allowed,
        }
    }
}

pub struct ModeSelector;

impl ModeSelector {
    pub fn select(input: &ModeInput) -> Result<ModeSelection, String> {
        if input.force_headless {
            return Ok(ModeSelection::build(Mode::Headless, "forced_headless", input));
        }
        for (source, value) in [
            ("args", input.args_mode.as_deref()),
            ("config", input.config_mode.as_deref()),
            ("task", input.task_mode.as_deref()),
        ] {
            if let Some(v) = value {
                if v.trim().is_empty() {
                    continue;
                }
                let mode = Mode::parse(v).ok_or_else(|| format!("invalid mode from {}: {}", source, v))?;
                return Ok(ModeSelection::build(mode, "explicit_override", input));
            }
        }
        if input.memory_unknown {
            return Ok(ModeSelection::build(Mode::Normal, "memory_unknown_degrade", input));
        }
        if input.mem_bytes <= LOW_MEMORY_BYTES && input.first_run {
            return Ok(ModeSelection::build(Mode::Lightweight, "low_memory_first_run", input));
        }
        Ok(ModeSelection::build(Mode::Normal, "automatic", input))
    }

    pub fn safe(input: &ModeInput) -> ModeSelection {
        ModeSelection::build(Mode::Safe, "consecutive_failures", input)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    fn base() -> ModeInput {
        ModeInput {
            mem_bytes: 8 * 1024 * 1024 * 1024,
            first_run: false,
            ..ModeInput::default()
        }
    }

    #[test]
    fn threshold_is_two_gib() {
        assert_eq!(LOW_MEMORY_BYTES, 2147483648);
    }

    #[test]
    fn low_memory_first_run_selects_lightweight() {
        let mut i = base();
        i.mem_bytes = LOW_MEMORY_BYTES;
        i.first_run = true;
        let s = ModeSelector::select(&i).unwrap();
        assert_eq!(s.mode, Mode::Lightweight);
        assert!(!s.ui_loaded);
        assert_eq!(s.reason, "low_memory_first_run");
    }

    #[test]
    fn above_threshold_selects_normal() {
        let mut i = base();
        i.first_run = true;
        let s = ModeSelector::select(&i).unwrap();
        assert_eq!(s.mode, Mode::Normal);
        assert!(s.ui_loaded);
    }

    #[test]
    fn low_memory_without_first_run_selects_normal() {
        let mut i = base();
        i.mem_bytes = LOW_MEMORY_BYTES - 1;
        assert_eq!(ModeSelector::select(&i).unwrap().mode, Mode::Normal);
    }

    #[test]
    fn config_override_beats_automatic() {
        let mut i = base();
        i.first_run = true;
        i.mem_bytes = LOW_MEMORY_BYTES;
        i.config_mode = Some("normal".to_string());
        assert_eq!(ModeSelector::select(&i).unwrap().mode, Mode::Normal);
    }

    #[test]
    fn args_override_beats_config() {
        let mut i = base();
        i.config_mode = Some("normal".to_string());
        i.args_mode = Some("lightweight".to_string());
        assert_eq!(ModeSelector::select(&i).unwrap().mode, Mode::Lightweight);
    }

    #[test]
    fn invalid_mode_is_zero_level_error() {
        let mut i = base();
        i.config_mode = Some("turbo".to_string());
        assert!(ModeSelector::select(&i).unwrap_err().contains("invalid mode from config"));
    }

    #[test]
    fn forced_headless_is_unconditional() {
        let mut i = base();
        i.config_mode = Some("normal".to_string());
        i.force_headless = true;
        let s = ModeSelector::select(&i).unwrap();
        assert_eq!(s.mode, Mode::Headless);
        assert!(!s.ui_loaded);
        assert_eq!(s.reason, "forced_headless");
    }

    #[test]
    fn headless_without_credential_disables_premium() {
        let mut i = base();
        i.force_headless = true;
        let s = ModeSelector::select(&i).unwrap();
        assert!(!s.premium_allowed);
        assert_eq!(s.fallback, Fallback::One);
    }

    #[test]
    fn headless_with_existing_credential_allows_premium() {
        let mut i = base();
        i.force_headless = true;
        i.credential_present = true;
        assert!(ModeSelector::select(&i).unwrap().premium_allowed);
    }

    #[test]
    fn unknown_memory_degrades_to_normal_with_level_two() {
        let mut i = base();
        i.memory_unknown = true;
        i.first_run = true;
        i.mem_bytes = LOW_MEMORY_BYTES;
        let s = ModeSelector::select(&i).unwrap();
        assert_eq!(s.mode, Mode::Normal);
        assert_eq!(s.fallback, Fallback::Two);
        assert!(s.memory_degraded);
    }

    #[test]
    fn safe_mode_ignores_custom_and_ui() {
        let mut i = base();
        i.config_mode = Some("normal".to_string());
        i.credential_present = true;
        let s = ModeSelector::safe(&i);
        assert_eq!(s.mode, Mode::Safe);
        assert!(!s.ui_loaded);
        assert!(!s.premium_allowed);
        assert_eq!(s.fallback, Fallback::Two);
    }

    #[test]
    fn only_normal_loads_ui() {
        assert!(Mode::Normal.loads_ui());
        for m in [Mode::Lightweight, Mode::Headless, Mode::Safe] {
            assert!(!m.loads_ui());
        }
    }
}

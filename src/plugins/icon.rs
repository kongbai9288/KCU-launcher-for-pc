pub const FALLBACK_GLYPH: &str = "?";
pub const MAX_SVG_BYTES: usize = 16 * 1024;

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PluginIcon {
    Svg(String),
    Fallback,
}

impl PluginIcon {
    pub fn from_svg(raw: Option<&str>) -> Self {
        let s = match raw {
            Some(v) => v.trim(),
            None => return Self::Fallback,
        };
        if s.is_empty() || s.len() > MAX_SVG_BYTES || !s.starts_with("<svg") {
            return Self::Fallback;
        }
        let low = s.to_ascii_lowercase();
        for bad in ["<script", "foreignobject", "<iframe", "<image", "onload=", "onerror=", "onclick="] {
            if low.contains(bad) {
                return Self::Fallback;
            }
        }
        let mut rest = low.as_str();
        while let Some(pos) = rest.find("href=\"") {
            let after = &rest[pos + 6..];
            let Some(end) = after.find('"') else {
                return Self::Fallback;
            };
            let value = after[..end].trim();
            if !value.starts_with('#') {
                return Self::Fallback;
            }
            rest = &after[end + 1..];
        }
        Self::Svg(s.to_string())
    }

    pub fn glyph(&self) -> &str {
        match self {
            Self::Svg(_) => "",
            Self::Fallback => FALLBACK_GLYPH,
        }
    }

    pub fn is_fallback(&self) -> bool {
        matches!(self, Self::Fallback)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    const GOOD: &str = r#"<svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="2"/></svg>"#;

    #[test]
    fn missing_svg_uses_question_mark() {
        let i = PluginIcon::from_svg(None);
        assert_eq!(i, PluginIcon::Fallback);
        assert_eq!(i.glyph(), "?");
        assert!(i.is_fallback());
    }

    #[test]
    fn empty_or_whitespace_uses_fallback() {
        assert!(PluginIcon::from_svg(Some("")).is_fallback());
        assert!(PluginIcon::from_svg(Some("   ")).is_fallback());
    }

    #[test]
    fn valid_svg_is_kept() {
        let i = PluginIcon::from_svg(Some(GOOD));
        assert_eq!(i, PluginIcon::Svg(GOOD.to_string()));
        assert!(!i.is_fallback());
    }

    #[test]
    fn non_svg_markup_uses_fallback() {
        assert!(PluginIcon::from_svg(Some("<div>hi</div>")).is_fallback());
        assert!(PluginIcon::from_svg(Some("<html></html>")).is_fallback());
    }

    #[test]
    fn script_and_event_handlers_use_fallback() {
        assert!(PluginIcon::from_svg(Some(r#"<svg onload="alert(1)"></svg>"#)).is_fallback());
        assert!(PluginIcon::from_svg(Some(r#"<svg><script>alert(1)</script></svg>"#)).is_fallback());
        assert!(PluginIcon::from_svg(Some(r#"<svg><foreignObject></foreignObject></svg>"#)).is_fallback());
    }

    #[test]
    fn external_references_use_fallback() {
        assert!(PluginIcon::from_svg(Some(r#"<svg><use href="https://x/y.svg"/></svg>"#)).is_fallback());
        assert!(PluginIcon::from_svg(Some(r#"<svg xlink:href="https://x/y.svg"></svg>"#)).is_fallback());
        assert!(PluginIcon::from_svg(Some(r#"<svg><image href="a.png"/></svg>"#)).is_fallback());
    }

    #[test]
    fn oversized_svg_uses_fallback() {
        let big = format!("<svg>{}</svg>", "a".repeat(MAX_SVG_BYTES + 1));
        assert!(PluginIcon::from_svg(Some(&big)).is_fallback());
    }

    #[test]
    fn internal_fragment_reference_stays_customisable() {
        let i = PluginIcon::from_svg(Some(r##"<svg><use href="#i-puzzle"/></svg>"##));
        assert!(!i.is_fallback());
    }
}

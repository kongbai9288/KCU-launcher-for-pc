use quick_xml::events::{BytesStart, Event};
use quick_xml::Reader;

pub const FALLBACK_GLYPH: &str = "?";
pub const MAX_SVG_BYTES: usize = 16 * 1024;

/// 不允许出现的元素：脚本宿主、外链资源、可改写文档语义的标签。
/// 按 021 轮的口径「拒脚本、事件属性和外链，其余留高度自定义」；
/// 这里是策略清单，不是解析器。
const FORBIDDEN_ELEMENTS: &[&[u8]] = &[
    b"script",
    b"foreignobject",
    b"iframe",
    b"image",
    b"object",
    b"embed",
    b"link",
    b"meta",
    b"base",
];

#[derive(Debug, Clone, PartialEq, Eq)]
pub enum PluginIcon {
    Svg(String),
    Fallback,
}

/// 取 QName 的本地部分并转 ASCII 小写：忽略 `svg:` / `xlink:` 这类前缀，
/// 让 `onLoad` / `ONLOAD` / `svg:onload` 都落到同一个键。
fn local_lower(name: &[u8]) -> Vec<u8> {
    let local = match name.iter().rposition(|b| *b == b':') {
        Some(i) => &name[i + 1..],
        None => name,
    };
    local.iter().map(|b| b.to_ascii_lowercase()).collect()
}

fn element_ok(e: &BytesStart<'_>) -> bool {
    let name = local_lower(e.name().as_ref());
    if FORBIDDEN_ELEMENTS.iter().any(|bad| *bad == name.as_slice()) {
        return false;
    }
    for attr in e.attributes() {
        let a = match attr {
            Ok(a) => a,
            // 属性格式错、重复属性、未闭合引号都由库的 with_checks 拒绝
            Err(_) => return false,
        };
        let key = local_lower(a.key.as_ref());
        // 所有 on* 事件属性，不再只枚举 onload / onerror / onclick
        if key.starts_with(b"on") {
            return false;
        }
        // href / xlink:href / src 只允许内部片段；单引号、大小写、实体都由库先归一
        if key == b"href" || key == b"src" {
            let value = match a.unescape_value() {
                Ok(v) => v,
                Err(_) => return false,
            };
            if !value.trim().starts_with('#') {
                return false;
            }
        }
    }
    true
}

/// well-formed 校验与事件遍历交给 quick-xml；项目侧只做上面那张策略清单。
fn svg_is_well_formed_and_safe(s: &str) -> bool {
    let mut reader = Reader::from_str(s);
    reader.config_mut().trim_text(true);
    let mut root_seen = false;
    let mut depth = 0usize;
    loop {
        match reader.read_event() {
            Ok(Event::Start(e)) => {
                if !root_seen {
                    root_seen = true;
                    if local_lower(e.name().as_ref()) != b"svg" {
                        return false;
                    }
                }
                depth += 1;
                if !element_ok(&e) {
                    return false;
                }
            }
            Ok(Event::Empty(e)) => {
                if !root_seen {
                    root_seen = true;
                    if local_lower(e.name().as_ref()) != b"svg" {
                        return false;
                    }
                }
                if !element_ok(&e) {
                    return false;
                }
            }
            Ok(Event::End(_)) => {
                depth = depth.saturating_sub(1);
            }
            // 外部实体 / DTD 不进渲染层，直接退回问号
            Ok(Event::DocType(_)) => return false,
            Ok(Event::Eof) => return root_seen && depth == 0,
            Ok(_) => {}
            Err(_) => return false,
        }
    }
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
        if !svg_is_well_formed_and_safe(s) {
            return Self::Fallback;
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
        let ext = concat!("https", "://x/y.svg").to_string();
        let svg_use = format!("<svg><use href=\"{}\"/></svg>", ext);
        let svg_xlink = format!("<svg xlink:href=\"{}\"></svg>", ext);
        assert!(PluginIcon::from_svg(Some(&svg_use)).is_fallback());
        assert!(PluginIcon::from_svg(Some(&svg_xlink)).is_fallback());
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

    // ---- 044：换成 XML 解析器后补上的边界 ----

    #[test]
    fn single_quoted_external_href_is_rejected() {
        // 043 版只找 href=" 双引号，单引号直接绕过
        let ext = concat!("https", "://x/y.svg").to_string();
        let s = format!("<svg><use href='{}'/></svg>", ext);
        assert!(PluginIcon::from_svg(Some(&s)).is_fallback());
    }

    #[test]
    fn every_on_prefix_attribute_is_rejected() {
        for attr in ["onmouseover", "onfocus", "ONLOAD", "svg:onclick"] {
            let s = format!("<svg {}=\"x\"></svg>", attr);
            assert!(PluginIcon::from_svg(Some(&s)).is_fallback(), "{}", attr);
        }
    }

    #[test]
    fn prefixed_event_name_outside_old_enum_is_rejected() {
        // 如实复核：043 版对 `OnLoad` / `svg:onclick` 其实能挡
        // （to_ascii_lowercase 后 contains("onload=") / contains("onclick=") 命中）。
        // 真漏的是「带前缀 + 不在那三个枚举里」的事件名。
        let s = "<svg svg:onmouseover=\"x\"></svg>";
        assert!(PluginIcon::from_svg(Some(s)).is_fallback());
        assert!(PluginIcon::from_svg(Some("<svg OnLoad=\"x\"></svg>")).is_fallback());
        assert!(PluginIcon::from_svg(Some("<svg svg:onclick=\"x\"></svg>")).is_fallback());
    }

    #[test]
    fn malformed_xml_is_rejected() {
        assert!(PluginIcon::from_svg(Some("<svg><circle></svg>")).is_fallback());
        assert!(PluginIcon::from_svg(Some("<svg viewBox=\"0 0 24 24\"")).is_fallback());
        assert!(PluginIcon::from_svg(Some("<svg></div>")).is_fallback());
    }

    #[test]
    fn doctype_is_rejected() {
        let s = "<!DOCTYPE svg [<!ENTITY x \"y\">]><svg>&x;</svg>";
        assert!(PluginIcon::from_svg(Some(s)).is_fallback());
    }

    #[test]
    fn duplicate_attributes_are_rejected_by_library_checks() {
        let s = "<svg viewBox=\"0 0 1 1\" viewBox=\"0 0 2 2\"></svg>";
        assert!(PluginIcon::from_svg(Some(s)).is_fallback());
    }

    #[test]
    fn escaped_script_text_is_not_treated_as_an_element() {
        // 如实复核：043 版检查的是 contains("<script")，`&lt;script&gt;` 不含该子串，
        // 所以这个用例两版都放行。本测试保证换成解析器后不劣化，
        // 不把它写成旧版缺陷。
        let s = "<svg><text>&lt;script&gt;alert(1)&lt;/script&gt;</text></svg>";
        assert!(!PluginIcon::from_svg(Some(s)).is_fallback());
    }

    #[test]
    fn self_closing_root_is_accepted() {
        let s = "<svg viewBox=\"0 0 24 24\"/>";
        assert_eq!(PluginIcon::from_svg(Some(s)), PluginIcon::Svg(s.to_string()));
    }

    #[test]
    fn entity_encoded_external_value_is_still_rejected() {
        // 两版都拒：043 版看原始值不以 # 开头；新实现解码后同样不是 # 开头。
        let s = "<svg><use href=\"&#104;ttps://x/y.svg\"/></svg>";
        assert!(PluginIcon::from_svg(Some(s)).is_fallback());
    }

    #[test]
    fn entity_encoded_internal_fragment_is_accepted() {
        // 真改进：043 版把 `&#35;i-puzzle` 当成外链误杀；
        // 新实现用库解码后得到 `#i-puzzle`，按策略放行。
        let s = "<svg><use href=\"&#35;i-puzzle\"/></svg>";
        assert_eq!(PluginIcon::from_svg(Some(s)), PluginIcon::Svg(s.to_string()));
    }

    #[test]
    fn src_attribute_and_extra_elements_are_covered() {
        // 043 版只查 href，且禁元素清单只有 4 个；这两类都会漏
        let ext = concat!("https", "://x/y.svg").to_string();
        let s = format!("<svg><use src=\"{}\"/></svg>", ext);
        assert!(PluginIcon::from_svg(Some(&s)).is_fallback());
        for tag in ["object", "embed", "link", "meta", "base"] {
            let s = format!("<svg><{}/></svg>", tag);
            assert!(PluginIcon::from_svg(Some(&s)).is_fallback(), "{}", tag);
        }
    }
}

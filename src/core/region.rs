//! 境外离线账户登录/注册限制：只用宿主注入的本地信号做判定。
//! 原文 `11-features-input.txt` 第 7 行：特殊版本除外；物理位置处于国外时，
//! 离线账户的登录与注册不可使用；正版后正常；位于中国大陆地区功能恢复正常；
//! 明确禁止用网络连接打法，避免误伤加速器与 VPN。
//!
//! 本模块不发网络请求、不读 IP、不做 GeoIP、不检测系统、不内置密钥。
//! 区域信号、用户覆盖、特殊版本标记、账户类型、正版权状态全部由调用方注入。
//! 判定复用已进构建的库：边界与限流 048、缓存 029、信封 031、取消 027、诊断 032。

use crate::core::asynk::CancelToken;
use crate::core::cache::Cache;
use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust::{self, OpBudget};
use serde_json::json;
use std::collections::BTreeMap;
use std::time::Duration;

pub const MAX_SIGNAL_BYTES: usize = 128;
pub const MAX_SIGNAL_KEYS: usize = 16;
pub const CACHE_CAPACITY: usize = 128;
pub const CACHE_TTL_SECS: u64 = 30;
pub const LOAD_TIMEOUT_SECS: u64 = 5;

/// 允许注入的本地信号键。未知键直接拒，不让调用方顺手把网络探测结果塞进来。
pub const ALLOWED_SIGNAL_KEYS: &[&str] = &[
    "locale",
    "timezone",
    "user_override",
    "special_build",
    "account",
    "authenticated",
    "action",
    "offline",
];

/// 原文禁止「网络连接打法」：这些键出现即整份信号作废，回退到不限制。
pub const FORBIDDEN_SIGNAL_KEYS: &[&str] = &[
    "ip",
    "geoip",
    "vpn",
    "proxy",
    "asn",
    "isp",
    "network_probe",
    "latitude",
    "longitude",
    "country_by_ip",
    "url",
    "endpoint",
    "token",
    "key",
    "secret",
    "api",
];

/// 中国大陆 IANA 时区。时区只是本地偏好信号，不是地理测量。
pub const MAINLAND_TIMEZONES: &[&str] = &["Asia/Shanghai", "Asia/Urumqi"];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Region {
    Mainland,
    Outside,
    Unknown,
}

impl Region {
    pub fn code(&self) -> &'static str {
        match self {
            Region::Mainland => "mainland",
            Region::Outside => "outside",
            Region::Unknown => "unknown",
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum AccountKind {
    Offline,
    ThirdParty,
    Mojang,
    Unknown,
}

impl AccountKind {
    pub fn code(&self) -> &'static str {
        match self {
            AccountKind::Offline => "offline",
            AccountKind::ThirdParty => "third_party",
            AccountKind::Mojang => "mojang",
            AccountKind::Unknown => "unknown",
        }
    }

    fn parse(s: &str) -> Self {
        match s {
            "offline" => AccountKind::Offline,
            "third_party" => AccountKind::ThirdParty,
            "mojang" => AccountKind::Mojang,
            _ => AccountKind::Unknown,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Action {
    Login,
    Register,
    Unknown,
}

impl Action {
    pub fn code(&self) -> &'static str {
        match self {
            Action::Login => "login",
            Action::Register => "register",
            Action::Unknown => "unknown",
        }
    }

    fn parse(s: &str) -> Self {
        match s {
            "login" => Action::Login,
            "register" => Action::Register,
            _ => Action::Unknown,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DecisionSource {
    SpecialBuild,
    UserOverride,
    LocalSignals,
    Unknown,
}

impl DecisionSource {
    pub fn code(&self) -> &'static str {
        match self {
            DecisionSource::SpecialBuild => "special_build",
            DecisionSource::UserOverride => "user_override",
            DecisionSource::LocalSignals => "local_signals",
            DecisionSource::Unknown => "unknown",
        }
    }
}

#[derive(Clone)]
pub struct RegionInput<'a> {
    /// 宿主注入的本地信号，键必须在 `ALLOWED_SIGNAL_KEYS` 内。
    pub signals: &'a BTreeMap<String, String>,
    /// 语言包 tag，只进诊断行，不参与判定（049 口径）。
    pub locale_tag: &'a str,
    pub cancel: &'a CancelToken,
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct RegionNotice {
    pub id: String,
    pub reason_key: &'static str,
    pub level: &'static str,
    pub closable: bool,
    pub actions: Vec<&'static str>,
    pub source: DecisionSource,
}

#[derive(Debug, Clone)]
pub struct RegionOutcome {
    pub code: &'static str,
    pub region: Region,
    pub source: DecisionSource,
    pub account: AccountKind,
    pub action: Action,
    pub allowed: bool,
    pub reason_key: &'static str,
    pub notices: Vec<RegionNotice>,
    pub diagnostics: Vec<String>,
    pub envelope: Envelope,
    pub cancelled: bool,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct Signals {
    locale: String,
    timezone: String,
    user_override: Option<Region>,
    special_build: bool,
    account: AccountKind,
    authenticated: bool,
    action: Action,
}

pub struct RegionGate {
    decisions: Cache<String, bool>,
    budget: OpBudget,
}

impl RegionGate {
    pub fn new() -> Self {
        Self {
            decisions: Cache::new(CACHE_CAPACITY, Duration::from_secs(CACHE_TTL_SECS)),
            budget: OpBudget::new(robust::MAX_OPS_PER_WINDOW),
        }
    }

    /// 用户改了地区覆盖、换了账号或网络状态变化后调用；下一次判定全部重跑。
    pub fn refresh(&self) {
        self.decisions.clear();
    }

    pub fn cached(&self) -> usize {
        self.decisions.len()
    }

    pub fn evaluate(&self, input: &RegionInput<'_>) -> RegionOutcome {
        if input.cancel.is_cancelled() {
            return self.finish(
                "region.cancelled",
                Region::Unknown,
                DecisionSource::Unknown,
                AccountKind::Unknown,
                Action::Unknown,
                true,
                "region.reason.none",
                Vec::new(),
                input,
                true,
            );
        }
        if !self.budget.try_op() {
            return self.finish(
                "region.rate_limited",
                Region::Unknown,
                DecisionSource::Unknown,
                AccountKind::Unknown,
                Action::Unknown,
                true,
                "region.reason.none",
                Vec::new(),
                input,
                false,
            );
        }

        let s = match parse_signals(input.signals) {
            Ok(v) => v,
            Err(_) => {
                return self.finish(
                    "region.signal_invalid",
                    Region::Unknown,
                    DecisionSource::Unknown,
                    AccountKind::Unknown,
                    Action::Unknown,
                    true,
                    "region.reason.none",
                    Vec::new(),
                    input,
                    false,
                )
            }
        };

        let (region, source) = resolve_region(&s);
        let allowed = self.decide(&s, region, source);
        let reason_key = if allowed {
            "region.reason.none"
        } else {
            "region.reason.outside_offline"
        };
        let code = if allowed {
            "region.allowed"
        } else {
            "region.blocked_offline"
        };

        let notices = if allowed {
            Vec::new()
        } else {
            vec![RegionNotice {
                id: format!("region.offline_{}", s.action.code()),
                reason_key: "region.reason.outside_offline",
                level: "info",
                closable: true,
                actions: vec!["region.act.premium", "region.act.override", "region.act.cancel"],
                source,
            }]
        };

        self.finish(
            code,
            region,
            source,
            s.account,
            s.action,
            allowed,
            reason_key,
            notices,
            input,
            false,
        )
    }

    fn decide(&self, s: &Signals, region: Region, source: DecisionSource) -> bool {
        // 原文：除了特殊版本以外。全局豁免排在最前。
        if s.special_build {
            return true;
        }
        // 原文：这个功能在这个场景下只有在正版后才能正常使用。
        if s.authenticated {
            return true;
        }
        // 原文只点名离线账户；第三方与正版不扩大限制范围。
        if s.account != AccountKind::Offline {
            return true;
        }
        if s.action == Action::Unknown {
            return true;
        }
        // 未知信号一律不限制：单一信号、冲突信号都不足以做硬拒绝（防误伤）。
        if region != Region::Outside {
            return true;
        }

        let key = format!(
            "{}:{}:{}:{}:{}:{}:{}",
            region.code(),
            source.code(),
            s.account.code(),
            s.action.code(),
            s.special_build,
            s.authenticated,
            s.locale
        );
        let decided = self.decisions.get_or_load(
            key,
            Duration::from_secs(LOAD_TIMEOUT_SECS),
            || -> Result<bool, anyhow::Error> { Ok(false) },
        );
        decided.unwrap_or(true)
    }

    #[allow(clippy::too_many_arguments)]
    fn finish(
        &self,
        code: &'static str,
        region: Region,
        source: DecisionSource,
        account: AccountKind,
        action: Action,
        allowed: bool,
        reason_key: &'static str,
        notices: Vec<RegionNotice>,
        input: &RegionInput<'_>,
        cancelled: bool,
    ) -> RegionOutcome {
        let mut details = vec![
            format!("code={}", code),
            format!("region={}", region.code()),
            format!("source={}", source.code()),
            format!("account={}", account.code()),
            format!("action={}", action.code()),
            format!("allowed={}", if allowed { "1" } else { "0" }),
            format!("locale_tag={}", input.locale_tag),
            "network_probe=0".to_string(),
        ];
        if cancelled {
            details.push("cancel=1".to_string());
        }

        let line = diag_line("core", "region", code, "OK", &details.join(" "));
        let mut diagnostics = vec![line];
        for n in &notices {
            diagnostics.push(diag_line(
                "core",
                "region",
                "notice",
                "OK",
                &format!(
                    "id={} reason={} source={} closable=1 actions=3",
                    n.id,
                    n.reason_key,
                    n.source.code()
                ),
            ));
        }

        let mut envelope = Envelope::new(Kind::Response, "core.region")
            .with("code", code)
            .with("region", region.code())
            .with("source", source.code())
            .with("account", account.code())
            .with("action", action.code())
            .with("allowed", if allowed { "1" } else { "0" })
            .with("reason_key", reason_key)
            .with("notices", &notices.len().to_string())
            .with("cancel", if cancelled { "1" } else { "0" })
            .with("network_probe", "0");
        if matches!(code, "region.signal_invalid" | "region.rate_limited" | "region.cancelled") {
            envelope = envelope.with_error(code);
        }

        RegionOutcome {
            code,
            region,
            source,
            account,
            action,
            allowed,
            reason_key,
            notices,
            diagnostics,
            envelope,
            cancelled,
        }
    }
}

impl Default for RegionGate {
    fn default() -> Self {
        Self::new()
    }
}

/// 严格解析：禁用键、未知键、超长、控制字符任一出现即整份作废。
fn parse_signals(map: &BTreeMap<String, String>) -> Result<Signals, ()> {
    if map.len() > MAX_SIGNAL_KEYS {
        return Err(());
    }
    for (k, v) in map {
        if !ALLOWED_SIGNAL_KEYS.contains(&k.as_str()) || FORBIDDEN_SIGNAL_KEYS.contains(&k.as_str()) {
            return Err(());
        }
        robust::check_text(k, MAX_SIGNAL_BYTES).map_err(|_| ())?;
        robust::check_text(v, MAX_SIGNAL_BYTES).map_err(|_| ())?;
    }
    let get = |k: &str| map.get(k).map(|s| s.as_str()).unwrap_or("");

    let locale = get("locale").to_string();
    let timezone = get("timezone").to_string();
    if !locale.is_empty() && !is_bcp47_shape(&locale) {
        return Err(());
    }
    if !timezone.is_empty() && !is_timezone_shape(&timezone) {
        return Err(());
    }

    let user_override = match get("user_override") {
        "mainland" => Some(Region::Mainland),
        "outside" => Some(Region::Outside),
        "" => None,
        // 畸形覆盖按未设置处理，不 panic、不擅自当境外。
        _ => None,
    };
    let special_build = match get("special_build") {
        "1" => true,
        "0" | "" => false,
        _ => false,
    };
    let authenticated = match get("authenticated") {
        "1" => true,
        "0" | "" => false,
        _ => false,
    };
    // `offline` 键允许宿主注入且已过边界校验，但显式不参与判定：
    // 原文禁止用网络连接打法，网络可达与否不能改变账户限制结论。
    Ok(Signals {
        locale,
        timezone,
        user_override,
        special_build,
        account: AccountKind::parse(get("account")),
        authenticated,
        action: Action::parse(get("action")),
    })
}

/// 只做形状校验，不实现完整 BCP-47 解析器：子标签为 ASCII 字母数字与连字符。
fn is_bcp47_shape(s: &str) -> bool {
    !s.is_empty()
        && s.bytes().all(|b| b.is_ascii_alphanumeric() || b == b'-')
        && s.split('-').all(|p| !p.is_empty() && p.len() <= 8)
}

/// IANA 时区形状：`Area/Location`，允许一个下划线或连字符，不含路径分隔符。
fn is_timezone_shape(s: &str) -> bool {
    let parts: Vec<&str> = s.split('/').collect();
    parts.len() == 2
        && parts.iter().all(|p| {
            !p.is_empty()
                && p.bytes()
                    .all(|b| b.is_ascii_alphanumeric() || b == b'_' || b == b'-' || b == b'+')
        })
}

/// 取 BCP-47 的第一个 region 子标签（2 个大写字母或 3 位数字）。
/// 跳过主语言、3 字母 extlang、4 字母 script、单字母 extension 与小写变体。
fn region_subtag(locale: &str) -> Option<String> {
    for part in locale.split('-').skip(1) {
        let b = part.as_bytes();
        let is_region = (b.len() == 2 && b.iter().all(|c| c.is_ascii_uppercase()))
            || (b.len() == 3 && b.iter().all(|c| c.is_ascii_digit()));
        if is_region {
            return Some(part.to_ascii_uppercase());
        }
        if b.len() == 1 || b.first().is_some_and(|c| *c == b'x' || *c == b'u' || *c == b't') {
            break;
        }
    }
    None
}

/// 双信号一致才敢判境外；单一信号、冲突信号、缺信号一律 Unknown（fail-open）。
fn resolve_region(s: &Signals) -> (Region, DecisionSource) {
    if let Some(r) = s.user_override {
        return (r, DecisionSource::UserOverride);
    }
    if s.special_build {
        return (Region::Unknown, DecisionSource::SpecialBuild);
    }
    let locale_region = region_subtag(&s.locale);
    let tz_mainland = MAINLAND_TIMEZONES.contains(&s.timezone.as_str());
    let tz_present = !s.timezone.is_empty();

    match locale_region.as_deref() {
        Some("CN") => {
            if tz_present && !tz_mainland {
                // 冲突：zh-CN 配 America/New_York，不硬判，交给用户覆盖。
                (Region::Unknown, DecisionSource::Unknown)
            } else {
                (Region::Mainland, DecisionSource::LocalSignals)
            }
        }
        Some(_) => {
            if tz_present && !tz_mainland {
                (Region::Outside, DecisionSource::LocalSignals)
            } else {
                // 只有 locale 一个信号，或时区仍指向大陆：不足以拒绝。
                (Region::Unknown, DecisionSource::Unknown)
            }
        }
        None => (Region::Unknown, DecisionSource::Unknown),
    }
}

/// 供调用方构造诊断包载荷；不进产品界面。
pub fn diagnostic_payload(outcome: &RegionOutcome) -> serde_json::Value {
    json!({
        "code": outcome.code,
        "region": outcome.region.code(),
        "source": outcome.source.code(),
        "account": outcome.account.code(),
        "action": outcome.action.code(),
        "allowed": outcome.allowed,
        "notices": outcome.notices.len(),
    })
}

#[cfg(test)]
mod tests {
    use super::*;

    fn sig(pairs: &[(&str, &str)]) -> BTreeMap<String, String> {
        pairs.iter().map(|(k, v)| (k.to_string(), v.to_string())).collect()
    }

    fn base() -> BTreeMap<String, String> {
        sig(&[
            ("locale", "en-US"),
            ("timezone", "America/New_York"),
            ("account", "offline"),
            ("action", "login"),
        ])
    }

    fn input<'a>(s: &'a BTreeMap<String, String>, cancel: &'a CancelToken) -> RegionInput<'a> {
        RegionInput {
            signals: s,
            locale_tag: "zh-CN",
            cancel,
        }
    }

    #[test]
    fn outside_offline_login_is_blocked_with_closable_notice() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let s = base();
        let o = g.evaluate(&input(&s, &t));
        assert_eq!(o.region, Region::Outside);
        assert_eq!(o.source, DecisionSource::LocalSignals);
        assert_eq!(o.code, "region.blocked_offline");
        assert!(!o.allowed);
        assert_eq!(o.reason_key, "region.reason.outside_offline");
        assert_eq!(o.notices.len(), 1);
        assert!(o.notices[0].closable);
        assert_eq!(o.notices[0].actions.len(), 3);
        assert_eq!(o.envelope.field("allowed"), Some("0"));
        assert_eq!(o.envelope.field("network_probe"), Some("0"));
        assert_eq!(o.diagnostics.len(), 2);
        assert!(o.diagnostics.iter().all(|l| l.starts_with("[KCU] ") && !l.contains('\n')));
    }

    #[test]
    fn outside_offline_register_is_also_blocked() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let s = sig(&[
            ("locale", "ja-JP"),
            ("timezone", "Asia/Tokyo"),
            ("account", "offline"),
            ("action", "register"),
        ]);
        let o = g.evaluate(&input(&s, &t));
        assert!(!o.allowed);
        assert_eq!(o.action, Action::Register);
        assert_eq!(o.notices[0].id, "region.offline_register");
    }

    #[test]
    fn mainland_restores_offline_login() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let s = sig(&[
            ("locale", "zh-Hans-CN"),
            ("timezone", "Asia/Shanghai"),
            ("account", "offline"),
            ("action", "login"),
        ]);
        let o = g.evaluate(&input(&s, &t));
        assert_eq!(o.region, Region::Mainland);
        assert!(o.allowed);
        assert!(o.notices.is_empty());
    }

    #[test]
    fn special_build_is_exempt_even_outside() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let mut s = base();
        s.insert("special_build".to_string(), "1".to_string());
        let o = g.evaluate(&input(&s, &t));
        assert!(o.allowed);
        assert_eq!(o.source, DecisionSource::SpecialBuild);
        assert!(o.notices.is_empty());
    }

    #[test]
    fn authenticated_premium_is_allowed_outside() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let mut s = base();
        s.insert("authenticated".to_string(), "1".to_string());
        s.insert("account".to_string(), "mojang".to_string());
        let o = g.evaluate(&input(&s, &t));
        assert!(o.allowed);
        assert_eq!(o.account, AccountKind::Mojang);
        assert!(o.notices.is_empty());
    }

    #[test]
    fn third_party_login_is_not_expanded_into_the_restriction() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let mut s = base();
        s.insert("account".to_string(), "third_party".to_string());
        let o = g.evaluate(&input(&s, &t));
        assert!(o.allowed);
        assert_eq!(o.account, AccountKind::ThirdParty);
    }

    #[test]
    fn user_override_ranks_first() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let mut s = base();
        s.insert("user_override".to_string(), "mainland".to_string());
        let o = g.evaluate(&input(&s, &t));
        assert_eq!(o.region, Region::Mainland);
        assert_eq!(o.source, DecisionSource::UserOverride);
        assert!(o.allowed);

        let mut s2 = sig(&[
            ("locale", "zh-Hans-CN"),
            ("timezone", "Asia/Shanghai"),
            ("account", "offline"),
            ("action", "login"),
            ("user_override", "outside"),
        ]);
        s2.insert("user_override".to_string(), "outside".to_string());
        let o2 = RegionGate::new().evaluate(&input(&s2, &t));
        assert_eq!(o2.region, Region::Outside);
        assert!(!o2.allowed);
    }

    #[test]
    fn single_signal_never_triggers_a_hard_block() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let only_locale = sig(&[
            ("locale", "en-US"),
            ("account", "offline"),
            ("action", "login"),
        ]);
        assert!(g.evaluate(&input(&only_locale, &t)).allowed);
        let only_tz = sig(&[
            ("timezone", "America/New_York"),
            ("account", "offline"),
            ("action", "login"),
        ]);
        assert!(g.evaluate(&input(&only_tz, &t)).allowed);
    }

    #[test]
    fn conflicting_signals_fall_back_to_unknown() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let s = sig(&[
            ("locale", "zh-CN"),
            ("timezone", "America/New_York"),
            ("account", "offline"),
            ("action", "login"),
        ]);
        let o = g.evaluate(&input(&s, &t));
        assert_eq!(o.region, Region::Unknown);
        assert!(o.allowed);
    }

    #[test]
    fn network_probe_keys_invalidate_the_whole_signal_set() {
        for k in ["ip", "geoip", "vpn", "proxy", "asn", "network_probe", "country_by_ip"] {
            let mut s = base();
            s.insert(k.to_string(), "203.0.113.1".to_string());
            let o = RegionGate::new().evaluate(&input(&s, &CancelToken::new()));
            assert_eq!(o.code, "region.signal_invalid", "key={}", k);
            assert!(o.allowed);
            assert!(!o.envelope.ok());
        }
    }

    #[test]
    fn credential_like_keys_are_rejected_too() {
        for k in ["url", "endpoint", "token", "key", "secret", "api"] {
            let mut s = base();
            s.insert(k.to_string(), "x".to_string());
            let o = RegionGate::new().evaluate(&input(&s, &CancelToken::new()));
            assert_eq!(o.code, "region.signal_invalid", "key={}", k);
        }
    }

    #[test]
    fn malformed_locale_and_timezone_do_not_panic() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let s = sig(&[
            ("locale", "../etc/passwd"),
            ("timezone", "Asia/../../etc"),
            ("account", "offline"),
            ("action", "login"),
        ]);
        let o = g.evaluate(&input(&s, &t));
        assert_eq!(o.code, "region.signal_invalid");
        assert!(o.allowed);
    }

    #[test]
    fn oversized_signal_value_is_rejected() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let mut s = base();
        s.insert("locale".to_string(), "a".repeat(MAX_SIGNAL_BYTES + 1));
        let o = g.evaluate(&input(&s, &t));
        assert_eq!(o.code, "region.signal_invalid");
        assert!(o.allowed);
    }

    #[test]
    fn offline_flag_never_changes_the_decision() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let mut a = base();
        a.insert("offline".to_string(), "0".to_string());
        let mut b = base();
        b.insert("offline".to_string(), "1".to_string());
        let oa = g.evaluate(&input(&a, &t));
        let ob = RegionGate::new().evaluate(&input(&b, &t));
        assert_eq!(oa.allowed, ob.allowed);
        assert_eq!(oa.code, ob.code);
        assert!(oa.diagnostics[0].contains("network_probe=0"));
    }

    #[test]
    fn refresh_clears_decisions_and_reruns() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let s = base();
        let a = g.evaluate(&input(&s, &t));
        assert!(!a.allowed);
        assert_eq!(g.cached(), 1);
        g.refresh();
        assert_eq!(g.cached(), 0);
        let mut s2 = s.clone();
        s2.insert("user_override".to_string(), "mainland".to_string());
        let b = g.evaluate(&input(&s2, &t));
        assert!(b.allowed);
    }

    #[test]
    fn cancel_has_no_side_effects() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        t.cancel();
        let s = base();
        let o = g.evaluate(&input(&s, &t));
        assert!(o.cancelled);
        assert_eq!(o.code, "region.cancelled");
        assert!(o.allowed);
        assert!(o.notices.is_empty());
        assert_eq!(g.cached(), 0);
        assert_eq!(o.envelope.field("cancel"), Some("1"));
    }

    #[test]
    fn rate_limit_never_denies_a_login() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let s = base();
        let mut last = String::new();
        for _ in 0..(robust::MAX_OPS_PER_WINDOW + 3) {
            last = g.evaluate(&input(&s, &t)).code.to_string();
        }
        assert_eq!(last, "region.rate_limited");
        let o = g.evaluate(&input(&s, &t));
        assert!(o.allowed);
        assert!(o.notices.is_empty());
    }

    #[test]
    fn region_subtag_handles_script_extlang_and_extensions() {
        assert_eq!(region_subtag("zh-Hans-CN").as_deref(), Some("CN"));
        assert_eq!(region_subtag("zh-yue-HK").as_deref(), Some("HK"));
        assert_eq!(region_subtag("de-DE-u-co-phonebk").as_deref(), Some("DE"));
        assert_eq!(region_subtag("en-US").as_deref(), Some("US"));
        assert_eq!(region_subtag("zh").as_deref(), None);
        assert_eq!(region_subtag("sr-Latn-001").as_deref(), Some("001"));
    }

    #[test]
    fn codes_are_explicit_strings() {
        assert_eq!(Region::Mainland.code(), "mainland");
        assert_eq!(Region::Outside.code(), "outside");
        assert_eq!(AccountKind::Offline.code(), "offline");
        assert_eq!(Action::Register.code(), "register");
        assert_eq!(DecisionSource::UserOverride.code(), "user_override");
    }

    #[test]
    fn diagnostic_payload_carries_no_raw_signals() {
        let g = RegionGate::new();
        let t = CancelToken::new();
        let s = base();
        let o = g.evaluate(&input(&s, &t));
        let p = diagnostic_payload(&o);
        assert_eq!(p["allowed"], false);
        assert_eq!(p["region"], "outside");
        assert!(p.get("locale").is_none());
        assert!(p.get("ip").is_none());
    }
}

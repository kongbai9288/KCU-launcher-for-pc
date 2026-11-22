use crate::core::diagnostics::diag_line;
use crate::core::envelope::{Envelope, Kind};
use crate::core::robust;
use anyhow::Result;
use serde_json::{from_str, json, to_string, Value};
use std::fs;
use std::path::Path;

pub const LAN_CHANNEL_FILE: &str = "lan-channel.json";
pub const TMP_SUFFIX: &str = ".tmp";
pub const DEFAULT_STATE: &str = r#"{"schema":1,"stage":"discover","method":"qr","direction":"","room_id":"","pair_code":"","channel_open":false}"#;
pub const MAX_FILE_BYTES: usize = 64 * 1024;
pub const EVENT_TARGET: &str = "lan.channel";
pub const KNOWN_KEYS: &[&str] = &["schema", "stage", "method", "direction", "room_id", "pair_code", "channel_open"];
pub const MESSAGE_KINDS: &[&str] = &["request", "response", "event"];
pub const STAGES: &[&str] = &["discover", "pair", "transfer", "close"];
pub const METHODS: &[&str] = &["qr", "link_code"];
pub const DIRECTIONS: &[&str] = &["pc_to_phone", "phone_to_pc"];
pub const TRANSITIONS: &[(&str, &str)] = &[
    ("discover", "pair"),
    ("pair", "transfer"),
    ("transfer", "close"),
    ("pair", "discover"),
    ("transfer", "pair"),
    ("close", "discover"),
];
pub const STAGE_FIELDS: &[(&str, &[&str])] = &[
    ("discover", &["stage", "method"]),
    ("pair", &["stage", "method", "pair_code", "room_id"]),
    ("transfer", &["stage", "direction", "channel_open", "pair_code"]),
    ("close", &["stage", "channel_open"]),
];

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum MessageKind {
    Request,
    Response,
    Event,
}

impl MessageKind {
    pub fn code(&self) -> &'static str {
        match self {
            MessageKind::Request => "request",
            MessageKind::Response => "response",
            MessageKind::Event => "event",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "request" => Some(MessageKind::Request),
            "response" => Some(MessageKind::Response),
            "event" => Some(MessageKind::Event),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LinkStage {
    Discover,
    Pair,
    Transfer,
    Close,
}

impl LinkStage {
    pub fn code(&self) -> &'static str {
        match self {
            LinkStage::Discover => "discover",
            LinkStage::Pair => "pair",
            LinkStage::Transfer => "transfer",
            LinkStage::Close => "close",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "discover" => Some(LinkStage::Discover),
            "pair" => Some(LinkStage::Pair),
            "transfer" => Some(LinkStage::Transfer),
            "close" => Some(LinkStage::Close),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PairMethod {
    Qr,
    LinkCode,
}

impl PairMethod {
    pub fn code(&self) -> &'static str {
        match self {
            PairMethod::Qr => "qr",
            PairMethod::LinkCode => "link_code",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "qr" => Some(PairMethod::Qr),
            "link_code" => Some(PairMethod::LinkCode),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransferDirection {
    PcToPhone,
    PhoneToPc,
}

impl TransferDirection {
    pub fn code(&self) -> &'static str {
        match self {
            TransferDirection::PcToPhone => "pc_to_phone",
            TransferDirection::PhoneToPc => "phone_to_pc",
        }
    }

    pub fn parse(s: &str) -> Option<Self> {
        match s {
            "pc_to_phone" => Some(TransferDirection::PcToPhone),
            "phone_to_pc" => Some(TransferDirection::PhoneToPc),
            _ => None,
        }
    }
}

#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ChannelState {
    pub stage: LinkStage,
    pub method: PairMethod,
    pub direction: Option<TransferDirection>,
    pub room_id: String,
    pub pair_code: String,
    pub channel_open: bool,
}

impl Default for ChannelState {
    fn default() -> Self {
        ChannelState {
            stage: LinkStage::Discover,
            method: PairMethod::Qr,
            direction: None,
            room_id: String::new(),
            pair_code: String::new(),
            channel_open: false,
        }
    }
}

fn degrade(action: &str, reason: &str) -> String {
    diag_line("lan", action, "channel", "DEGRADE", reason)
}

fn error_line(action: &str, reason: &str) -> String {
    diag_line("lan", action, "channel", "ERROR", reason)
}

fn has_control(s: &str) -> bool {
    s.chars().any(|c| c.is_control())
}

fn valid_optional_text(s: &str) -> bool {
    s.len() <= robust::MAX_TEXT_BYTES && !has_control(s)
}

fn state_consistent(stage: LinkStage, direction: Option<TransferDirection>, pair_code: &str, channel_open: bool) -> bool {
    if (stage == LinkStage::Pair || stage == LinkStage::Transfer) && pair_code.is_empty() {
        return false;
    }
    if stage == LinkStage::Transfer && (direction.is_none() || !channel_open) {
        return false;
    }
    if (stage == LinkStage::Close || stage == LinkStage::Discover) && channel_open {
        return false;
    }
    true
}

pub fn can_transition(from: LinkStage, to: LinkStage) -> bool {
    TRANSITIONS.iter().any(|(a, b)| *a == from.code() && *b == to.code())
}

pub fn stage_fields(stage: LinkStage) -> &'static [&'static str] {
    for entry in STAGE_FIELDS {
        if entry.0 == stage.code() {
            return entry.1;
        }
    }
    &[]
}

pub fn next_stages(stage: LinkStage) -> Vec<&'static str> {
    let mut out: Vec<&'static str> = Vec::new();
    for (a, b) in TRANSITIONS {
        if *a == stage.code() && !out.contains(b) {
            out.push(b);
        }
    }
    out
}

pub fn message_kind_for(stage: LinkStage) -> MessageKind {
    match stage {
        LinkStage::Discover => MessageKind::Request,
        LinkStage::Pair => MessageKind::Request,
        LinkStage::Transfer => MessageKind::Event,
        LinkStage::Close => MessageKind::Response,
    }
}

pub fn field_allowed(stage: LinkStage, field: &str) -> bool {
    stage_fields(stage).contains(&field)
}

fn parse(raw: &str) -> (ChannelState, Vec<String>) {
    let mut lines: Vec<String> = Vec::new();
    let value: Value = match from_str(raw) {
        Ok(v) => v,
        Err(_) => {
            lines.push(degrade("load", "not_json"));
            return (ChannelState::default(), lines);
        }
    };
    let obj = match value.as_object() {
        Some(o) => o,
        None => {
            lines.push(degrade("load", "root_not_object"));
            return (ChannelState::default(), lines);
        }
    };
    if obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str())) {
        lines.push(degrade("load", "unknown_key"));
        return (ChannelState::default(), lines);
    }
    if obj.get("schema").and_then(Value::as_u64) != Some(1) {
        lines.push(degrade("load", "schema_invalid"));
        return (ChannelState::default(), lines);
    }
    let stage = match obj.get("stage").and_then(Value::as_str).and_then(LinkStage::parse) {
        Some(s) => s,
        None => {
            lines.push(degrade("load", "bad_stage"));
            return (ChannelState::default(), lines);
        }
    };
    let method = match obj.get("method").and_then(Value::as_str).and_then(PairMethod::parse) {
        Some(m) => m,
        None => {
            lines.push(degrade("load", "bad_method"));
            return (ChannelState::default(), lines);
        }
    };
    let direction_raw = match obj.get("direction").and_then(Value::as_str) {
        Some(s) => s,
        None => {
            lines.push(degrade("load", "direction_not_text"));
            return (ChannelState::default(), lines);
        }
    };
    if direction_raw.len() > robust::MAX_TEXT_BYTES {
        lines.push(degrade("load", "direction_too_large"));
        return (ChannelState::default(), lines);
    }
    let direction = if direction_raw.is_empty() {
        None
    } else {
        match TransferDirection::parse(direction_raw) {
            Some(d) => Some(d),
            None => {
                lines.push(degrade("load", "bad_direction"));
                return (ChannelState::default(), lines);
            }
        }
    };
    let room_id = match obj.get("room_id").and_then(Value::as_str) {
        Some(s) if valid_optional_text(s) => s.to_string(),
        _ => {
            lines.push(degrade("load", "bad_room_id"));
            return (ChannelState::default(), lines);
        }
    };
    let pair_code = match obj.get("pair_code").and_then(Value::as_str) {
        Some(s) if valid_optional_text(s) => s.to_string(),
        _ => {
            lines.push(degrade("load", "bad_pair_code"));
            return (ChannelState::default(), lines);
        }
    };
    let channel_open = match obj.get("channel_open").and_then(Value::as_bool) {
        Some(b) => b,
        None => {
            lines.push(degrade("load", "channel_not_bool"));
            return (ChannelState::default(), lines);
        }
    };
    if !state_consistent(stage, direction, &pair_code, channel_open) {
        lines.push(degrade("load", "bad_stage_state_pair"));
        return (ChannelState::default(), lines);
    }
    (ChannelState { stage, method, direction, room_id, pair_code, channel_open }, lines)
}

fn serialize(p: &ChannelState) -> Result<String> {
    let direction = match p.direction {
        Some(d) => d.code(),
        None => "",
    };
    Ok(to_string(&json!({
        "schema": 1,
        "stage": p.stage.code(),
        "method": p.method.code(),
        "direction": direction,
        "room_id": p.room_id,
        "pair_code": p.pair_code,
        "channel_open": p.channel_open,
    }))?)
}

fn write(root: &Path, p: &ChannelState) -> Result<()> {
    let body = serialize(p)?;
    let path = robust::safe_join(root, LAN_CHANNEL_FILE)?;
    if let Some(parent) = path.parent() {
        fs::create_dir_all(parent)?;
    }
    let tmp = robust::safe_join(root, &format!("{}{}", LAN_CHANNEL_FILE, TMP_SUFFIX))?;
    fs::write(&tmp, body)?;
    fs::rename(&tmp, &path)?;
    Ok(())
}

impl ChannelState {
    pub fn open(root: Option<&Path>) -> (ChannelState, Vec<String>) {
        let Some(dir) = root else {
            return (ChannelState::default(), vec![degrade("load", "in_memory")]);
        };
        let path = match robust::safe_join(dir, LAN_CHANNEL_FILE) {
            Ok(p) => p,
            Err(_) => return (ChannelState::default(), vec![degrade("load", "path_rejected")]),
        };
        let (raw, missing) = robust::read_or_default(&path, DEFAULT_STATE);
        if missing {
            return (ChannelState::default(), vec![degrade("load", "missing_or_unreadable")]);
        }
        if raw.len() > MAX_FILE_BYTES {
            return (ChannelState::default(), vec![degrade("load", "too_large")]);
        }
        parse(&raw)
    }

    pub fn pair_ready(&self) -> bool {
        !self.pair_code.is_empty()
    }

    pub fn channel_usable(&self) -> bool {
        self.stage == LinkStage::Transfer
            && self.channel_open
            && self.direction.is_some()
            && !self.pair_code.is_empty()
    }

    pub fn summary(&self) -> [usize; 4] {
        [MESSAGE_KINDS.len(), STAGES.len(), TRANSITIONS.len(), stage_fields(self.stage).len()]
    }

    pub fn set_stage(&mut self, to: LinkStage) -> bool {
        if !can_transition(self.stage, to) {
            return false;
        }
        if (to == LinkStage::Pair || to == LinkStage::Transfer) && !self.pair_ready() {
            return false;
        }
        if to == LinkStage::Transfer && (self.direction.is_none() || !self.channel_open) {
            return false;
        }
        if (to == LinkStage::Close || to == LinkStage::Discover) && self.channel_open {
            return false;
        }
        self.stage = to;
        true
    }

    pub fn set_method(&mut self, method: PairMethod) -> bool {
        if !METHODS.contains(&method.code()) {
            return false;
        }
        self.method = method;
        true
    }

    pub fn set_direction(&mut self, direction: TransferDirection) -> bool {
        if !DIRECTIONS.contains(&direction.code()) {
            return false;
        }
        self.direction = Some(direction);
        true
    }

    pub fn clear_direction(&mut self) -> bool {
        if self.stage == LinkStage::Transfer {
            return false;
        }
        self.direction = None;
        true
    }

    pub fn set_room_id(&mut self, id: &str) -> bool {
        if !valid_optional_text(id) {
            return false;
        }
        self.room_id = id.to_string();
        true
    }

    pub fn set_pair_code(&mut self, code: &str) -> bool {
        if !valid_optional_text(code) {
            return false;
        }
        if code.is_empty() && (self.stage == LinkStage::Pair || self.stage == LinkStage::Transfer) {
            return false;
        }
        self.pair_code = code.to_string();
        true
    }

    pub fn set_channel_open(&mut self, on: bool) -> bool {
        if on {
            if self.stage != LinkStage::Pair && self.stage != LinkStage::Transfer {
                return false;
            }
            if self.direction.is_none() || !self.pair_ready() {
                return false;
            }
        }
        self.channel_open = on;
        true
    }

    pub fn persist(&self, root: Option<&Path>) -> Vec<String> {
        let Some(dir) = root else { return vec![error_line("persist", "no_root")] };
        match write(dir, self) {
            Ok(()) => Vec::new(),
            Err(e) => vec![error_line("persist", &e.to_string())],
        }
    }

    pub fn change_event(&self) -> Envelope {
        let direction = match self.direction {
            Some(d) => d.code(),
            None => "",
        };
        Envelope::new(Kind::Event, EVENT_TARGET)
            .with("stage", self.stage.code())
            .with("method", self.method.code())
            .with("direction", direction)
            .with("channel_open", &(self.channel_open as u8).to_string())
            .with("pair_ready", &(self.pair_ready() as u8).to_string())
            .with("channel_usable", &(self.channel_usable() as u8).to_string())
            .with("kinds", &MESSAGE_KINDS.len().to_string())
            .with("stages", &STAGES.len().to_string())
            .with("transitions", &TRANSITIONS.len().to_string())
            .with("fields", &stage_fields(self.stage).len().to_string())
    }
}

pub fn reset(root: Option<&Path>) -> Vec<String> {
    ChannelState::default().persist(root)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::core::settings_io::PROTECTED_FILES;
    use std::sync::atomic::{AtomicUsize, Ordering};
    static SEQ: AtomicUsize = AtomicUsize::new(0);

    fn tmp() -> std::path::PathBuf {
        let n = SEQ.fetch_add(1, Ordering::SeqCst);
        let p = std::env::temp_dir().join(format!("kcu080-{}-{}", std::process::id(), n));
        let _ = fs::remove_dir_all(&p);
        p
    }

    fn load(dir: &std::path::Path, raw: &str) -> (ChannelState, Vec<String>) {
        fs::create_dir_all(dir).unwrap();
        fs::write(dir.join(LAN_CHANNEL_FILE), raw).unwrap();
        ChannelState::open(Some(dir))
    }

    #[test]
    fn default_state_literal_is_unchanged() {
        assert_eq!(DEFAULT_STATE, r#"{"schema":1,"stage":"discover","method":"qr","direction":"","room_id":"","pair_code":"","channel_open":false}"#);
        let v: Value = from_str(DEFAULT_STATE).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 7);
    }

    #[test]
    fn four_enum_codes_and_five_tables_are_explicit() {
        assert_eq!(MessageKind::Request.code(), "request");
        assert_eq!(MessageKind::Response.code(), "response");
        assert_eq!(MessageKind::Event.code(), "event");
        assert_eq!(MessageKind::parse("nope"), None);
        assert_eq!(LinkStage::Discover.code(), "discover");
        assert_eq!(LinkStage::Pair.code(), "pair");
        assert_eq!(LinkStage::Transfer.code(), "transfer");
        assert_eq!(LinkStage::Close.code(), "close");
        assert_eq!(LinkStage::parse("nope"), None);
        assert_eq!(PairMethod::Qr.code(), "qr");
        assert_eq!(PairMethod::LinkCode.code(), "link_code");
        assert_eq!(PairMethod::parse("nope"), None);
        assert_eq!(TransferDirection::PcToPhone.code(), "pc_to_phone");
        assert_eq!(TransferDirection::PhoneToPc.code(), "phone_to_pc");
        assert_eq!(TransferDirection::parse("nope"), None);
        assert_eq!(KNOWN_KEYS.len(), 7);
        assert_eq!(MESSAGE_KINDS.len(), 3);
        assert_eq!(STAGES.len(), 4);
        assert_eq!(METHODS.len(), 2);
        assert_eq!(DIRECTIONS.len(), 2);
        assert_eq!(TRANSITIONS.len(), 6);
        assert_eq!(STAGE_FIELDS.len(), 4);
    }

    #[test]
    fn default_is_discover_and_closed() {
        let (p, lines) = ChannelState::open(None);
        assert!(lines[0].contains("DEGRADE"));
        assert_eq!(p, ChannelState::default());
        assert_eq!(p.stage, LinkStage::Discover);
        assert_eq!(p.method, PairMethod::Qr);
        assert!(p.direction.is_none());
        assert!(!p.channel_open);
        assert!(!p.pair_ready());
        assert!(!p.channel_usable());
        assert_eq!(p.summary(), [3, 4, 6, 2]);
    }

    #[test]
    fn bad_root_inputs_return_to_default() {
        let r = tmp();
        let base = DEFAULT_STATE;
        let cases = vec![
            "".to_string(),
            "not json".to_string(),
            "[]".to_string(),
            "x".repeat(MAX_FILE_BYTES + 1),
            base.replace("\"channel_open\":false", "\"channel_open\":false,\"extra\":1"),
            base.replace("\"schema\":1", "\"schema\":2"),
            base.replace("\"stage\":\"discover\"", "\"stage\":\"nope\""),
            base.replace("\"method\":\"qr\"", "\"method\":\"nope\""),
            base.replace("\"direction\":\"\"", "\"direction\":\"nope\""),
            base.replace("\"room_id\":\"\"", "\"room_id\":7"),
            base.replace("\"pair_code\":\"\"", "\"pair_code\":false"),
            base.replace("\"channel_open\":false", "\"channel_open\":\"no\""),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, ChannelState::default(), "case={}", &raw[..raw.len().min(40)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(40)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn bad_field_texts_are_rejected() {
        let r = tmp();
        let base = DEFAULT_STATE;
        let cases = vec![
            base.replace("\"room_id\":\"\"", "\"room_id\":\"a\\nb\""),
            base.replace("\"pair_code\":\"\"", "\"pair_code\":\"a\\tb\""),
            base.replace("\"room_id\":\"\"", &format!("\"room_id\":\"{}\"", "x".repeat(robust::MAX_TEXT_BYTES + 1))),
            base.replace("\"pair_code\":\"\"", &format!("\"pair_code\":\"{}\"", "x".repeat(robust::MAX_TEXT_BYTES + 1))),
            base.replace("\"direction\":\"\"", "\"direction\":null"),
            base.replace("\"stage\":\"discover\"", "\"stage\":7"),
        ];
        for raw in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, ChannelState::default(), "case={}", &raw[..raw.len().min(40)]);
            assert!(lines.iter().any(|x| x.contains("DEGRADE")), "case={}", &raw[..raw.len().min(40)]);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn contradiction_states_are_rejected_on_load() {
        let r = tmp();
        let cases = vec![
            (r#"{"schema":1,"stage":"pair","method":"qr","direction":"","room_id":"","pair_code":"","channel_open":false}"#.to_string(), "bad_pair_without_code"),
            (r#"{"schema":1,"stage":"transfer","method":"qr","direction":"","room_id":"","pair_code":"c","channel_open":true}"#.to_string(), "bad_transfer_without_direction"),
            (r#"{"schema":1,"stage":"transfer","method":"qr","direction":"pc_to_phone","room_id":"","pair_code":"c","channel_open":false}"#.to_string(), "bad_transfer_without_open_channel"),
            (r#"{"schema":1,"stage":"close","method":"qr","direction":"","room_id":"","pair_code":"","channel_open":true}"#.to_string(), "bad_close_with_open_channel"),
            (r#"{"schema":1,"stage":"discover","method":"qr","direction":"","room_id":"","pair_code":"","channel_open":true}"#.to_string(), "bad_discover_with_open_channel"),
        ];
        for (raw, tag) in cases {
            let (p, lines) = load(&r, &raw);
            assert_eq!(p, ChannelState::default(), "tag={}", tag);
            assert!(lines.iter().any(|x| x.contains("bad_stage_state_pair")), "tag={}", tag);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn transitions_table_has_six_pairs() {
        assert!(can_transition(LinkStage::Discover, LinkStage::Pair));
        assert!(can_transition(LinkStage::Pair, LinkStage::Transfer));
        assert!(can_transition(LinkStage::Transfer, LinkStage::Close));
        assert!(can_transition(LinkStage::Pair, LinkStage::Discover));
        assert!(can_transition(LinkStage::Transfer, LinkStage::Pair));
        assert!(can_transition(LinkStage::Close, LinkStage::Discover));
        assert!(!can_transition(LinkStage::Discover, LinkStage::Transfer));
        assert!(!can_transition(LinkStage::Discover, LinkStage::Close));
        assert!(!can_transition(LinkStage::Pair, LinkStage::Close));
        assert!(!can_transition(LinkStage::Close, LinkStage::Pair));
        assert_eq!(next_stages(LinkStage::Discover), vec!["pair"]);
        assert_eq!(next_stages(LinkStage::Pair), vec!["transfer", "discover"]);
        assert_eq!(next_stages(LinkStage::Transfer), vec!["close", "pair"]);
        assert_eq!(next_stages(LinkStage::Close), vec!["discover"]);
    }

    #[test]
    fn stage_fields_table_has_four_segments() {
        assert_eq!(stage_fields(LinkStage::Discover), &["stage", "method"]);
        assert_eq!(stage_fields(LinkStage::Pair), &["stage", "method", "pair_code", "room_id"]);
        assert_eq!(stage_fields(LinkStage::Transfer), &["stage", "direction", "channel_open", "pair_code"]);
        assert_eq!(stage_fields(LinkStage::Close), &["stage", "channel_open"]);
        assert!(field_allowed(LinkStage::Pair, "pair_code"));
        assert!(!field_allowed(LinkStage::Pair, "channel_open"));
        assert!(field_allowed(LinkStage::Transfer, "channel_open"));
        assert!(!field_allowed(LinkStage::Close, "pair_code"));
        assert_eq!(message_kind_for(LinkStage::Discover), MessageKind::Request);
        assert_eq!(message_kind_for(LinkStage::Pair), MessageKind::Request);
        assert_eq!(message_kind_for(LinkStage::Transfer), MessageKind::Event);
        assert_eq!(message_kind_for(LinkStage::Close), MessageKind::Response);
    }

    #[test]
    fn pure_queries_do_not_read_files() {
        let p = ChannelState::default();
        assert_eq!(p.summary(), [3, 4, 6, 2]);
        assert!(!p.pair_ready());
        assert!(!p.channel_usable());
        assert_eq!(MESSAGE_KINDS, &["request", "response", "event"]);
        assert_eq!(STAGES, &["discover", "pair", "transfer", "close"]);
        assert_eq!(METHODS, &["qr", "link_code"]);
        assert_eq!(DIRECTIONS, &["pc_to_phone", "phone_to_pc"]);
    }

    #[test]
    fn set_stage_rejects_illegal_jumps() {
        let mut p = ChannelState::default();
        assert!(!p.set_stage(LinkStage::Transfer));
        assert!(!p.set_stage(LinkStage::Close));
        assert!(!p.set_stage(LinkStage::Pair));
        assert_eq!(p.stage, LinkStage::Discover);
        assert!(p.set_pair_code("c1"));
        assert!(p.set_stage(LinkStage::Pair));
        assert!(!p.set_stage(LinkStage::Transfer));
        assert!(p.set_direction(TransferDirection::PcToPhone));
        assert!(p.set_channel_open(true));
        assert!(p.set_stage(LinkStage::Transfer));
        assert!(p.channel_usable());
        assert!(!p.set_stage(LinkStage::Close));
        assert!(p.set_channel_open(false));
        assert!(p.set_stage(LinkStage::Close));
        assert_eq!(p.stage, LinkStage::Close);
    }

    #[test]
    fn set_channel_open_three_way_contradiction() {
        let mut p = ChannelState::default();
        assert!(!p.set_channel_open(true));
        assert!(p.set_pair_code("c1"));
        assert!(!p.set_channel_open(true));
        assert!(p.set_direction(TransferDirection::PhoneToPc));
        assert!(!p.set_channel_open(true));
        assert!(p.set_stage(LinkStage::Pair));
        assert!(p.set_channel_open(true));
        assert!(p.channel_open);
        assert!(p.clear_direction());
        assert!(p.direction.is_none());
        assert!(!p.set_channel_open(true));
        assert!(p.set_direction(TransferDirection::PcToPhone));
        assert!(p.set_channel_open(true));
        assert!(p.set_stage(LinkStage::Transfer));
        assert!(!p.clear_direction());
        assert_eq!(p.direction, Some(TransferDirection::PcToPhone));
        assert!(p.set_channel_open(false));
        assert!(!p.channel_open);
        assert!(!p.channel_usable());
        assert!(!p.clear_direction());
        assert_eq!(p.direction, Some(TransferDirection::PcToPhone));
        assert!(p.set_stage(LinkStage::Pair));
        assert!(p.clear_direction());
        assert!(p.direction.is_none());
    }

    #[test]
    fn single_item_mutations_do_not_touch_other_fields() {
        let mut p = ChannelState::default();
        assert!(p.set_room_id("room-1"));
        assert_eq!(p.room_id, "room-1");
        assert_eq!(p.method, PairMethod::Qr);
        assert!(p.set_method(PairMethod::LinkCode));
        assert_eq!(p.method, PairMethod::LinkCode);
        assert_eq!(p.room_id, "room-1");
        assert_eq!(p.stage, LinkStage::Discover);
        assert!(p.set_direction(TransferDirection::PcToPhone));
        assert_eq!(p.direction, Some(TransferDirection::PcToPhone));
        assert!(p.clear_direction());
        assert!(p.direction.is_none());
        assert!(!p.set_room_id("bad\nid"));
        assert_eq!(p.room_id, "room-1");
    }

    #[test]
    fn set_pair_code_cannot_break_pair_state() {
        let mut p = ChannelState::default();
        assert!(p.set_pair_code("c1"));
        assert!(p.set_stage(LinkStage::Pair));
        assert!(!p.set_pair_code(""));
        assert_eq!(p.pair_code, "c1");
        assert!(p.set_pair_code("c2"));
        assert_eq!(p.pair_code, "c2");
        assert!(!p.set_pair_code("bad\ncode"));
        assert_eq!(p.pair_code, "c2");
        assert!(p.set_channel_open(false));
        assert!(p.set_stage(LinkStage::Discover));
        assert!(p.set_pair_code(""));
        assert!(!p.pair_ready());
    }

    #[test]
    fn no_root_is_visible_and_not_silent() {
        let mut p = ChannelState::default();
        p.set_pair_code("c1");
        assert!(p.persist(None)[0].contains("ERROR"));
        assert!(reset(None)[0].contains("ERROR"));
    }

    #[test]
    fn persist_reopen_reset_keep_protected_files() {
        let r = tmp();
        fs::create_dir_all(&r).unwrap();
        for name in PROTECTED_FILES {
            fs::write(r.join(name), "keep").unwrap();
        }
        let mut p = ChannelState::default();
        assert!(p.set_room_id("room-1"));
        assert!(p.set_pair_code("code-1"));
        assert!(p.set_method(PairMethod::LinkCode));
        assert!(p.set_direction(TransferDirection::PhoneToPc));
        assert!(p.set_stage(LinkStage::Pair));
        assert!(p.set_channel_open(true));
        assert!(p.set_stage(LinkStage::Transfer));
        assert!(p.channel_usable());
        assert!(p.persist(Some(&r)).is_empty());
        let (back, lines) = ChannelState::open(Some(&r));
        assert!(lines.is_empty());
        assert_eq!(back.stage, LinkStage::Transfer);
        assert_eq!(back.method, PairMethod::LinkCode);
        assert_eq!(back.direction, Some(TransferDirection::PhoneToPc));
        assert_eq!(back.room_id, "room-1");
        assert_eq!(back.pair_code, "code-1");
        assert!(back.channel_open);
        assert!(back.channel_usable());
        assert_eq!(back.summary(), [3, 4, 6, 4]);
        assert!(reset(Some(&r)).is_empty());
        let (def, _) = ChannelState::open(Some(&r));
        assert_eq!(def, ChannelState::default());
        for name in PROTECTED_FILES {
            assert_eq!(fs::read_to_string(r.join(name)).unwrap(), "keep", "lost={}", name);
        }
        let _ = fs::remove_dir_all(&r);
    }

    #[test]
    fn change_event_uses_unified_envelope_without_user_text() {
        let mut p = ChannelState::default();
        p.set_room_id("secret-room");
        p.set_pair_code("secret-code");
        p.set_direction(TransferDirection::PcToPhone);
        p.set_stage(LinkStage::Pair);
        p.set_channel_open(true);
        p.set_stage(LinkStage::Transfer);
        let e = p.change_event();
        assert_eq!(e.kind, Kind::Event);
        assert_eq!(e.target, EVENT_TARGET);
        assert_eq!(e.field("stage"), Some("transfer"));
        assert_eq!(e.field("method"), Some("qr"));
        assert_eq!(e.field("direction"), Some("pc_to_phone"));
        assert_eq!(e.field("channel_open"), Some("1"));
        assert_eq!(e.field("pair_ready"), Some("1"));
        assert_eq!(e.field("channel_usable"), Some("1"));
        assert_eq!(e.field("kinds"), Some("3"));
        assert_eq!(e.field("stages"), Some("4"));
        assert_eq!(e.field("transitions"), Some("6"));
        assert_eq!(e.field("fields"), Some("4"));
        for key in ["room_id", "pair_code"] {
            assert_eq!(e.field(key), None);
        }
        assert!(!e.request_id.is_empty());
        assert!(e.ok());
        assert_eq!(e.payload.len(), 10);
    }

    #[test]
    fn serialize_carries_no_channel_table() {
        let mut p = ChannelState::default();
        p.set_room_id("room-1");
        p.set_pair_code("code-1");
        let raw = serialize(&p).unwrap();
        let v: Value = from_str(&raw).unwrap();
        assert_eq!(v.as_object().unwrap().len(), 7);
        assert!(!raw.contains("CHANNEL_TABLE"));
        assert!(!raw.contains("TRANSITION_TABLE"));
        assert!(!raw.contains("FIELD_TABLE"));
    }

    #[test]
    fn both_pair_methods_are_reachable() {
        let mut p = ChannelState::default();
        assert!(p.set_method(PairMethod::Qr));
        assert_eq!(p.method.code(), "qr");
        assert!(p.set_method(PairMethod::LinkCode));
        assert_eq!(p.method.code(), "link_code");
        assert!(METHODS.contains(&PairMethod::Qr.code()));
        assert!(METHODS.contains(&PairMethod::LinkCode.code()));
    }

    #[test]
    fn message_kinds_cover_request_response_event() {
        for kind in MESSAGE_KINDS {
            assert!(MessageKind::parse(kind).is_some());
            assert_eq!(MessageKind::parse(kind).unwrap().code(), *kind);
        }
        assert_eq!(MessageKind::parse("unknown"), None);
    }
}

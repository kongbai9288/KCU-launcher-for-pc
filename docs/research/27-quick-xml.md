# quick-xml 0.38.4 一手资料（044）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/tafia/quick-xml/blob/v0.38.4/Cargo.toml | MIT / edition 2021 / MSRV 1.56；`default = []`；`[dependencies]` 只有 `memchr = "2.1"` 非 optional，`encoding_rs 0.8` / `serde >=1.0.139` / `tokio 1.10` 均 optional；features 含 serialize / serde-types / encoding / async-tokio / overlapped-lists；dev 含 criterion / regex / serde_derive / tokio-test | 已证实（api.github.com 同 tag 内容） |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/reader/slice_reader.rs | `Reader<&[u8]>::from_str(&str)` 由 Rust 字符串 UTF-8 保证锁定编码；`read_event() -> Result<Event>` 调 `read_event_impl(())` | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/reader/mod.rs | `config_mut() -> &mut Config`；`Config::trim_text` | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/events/attributes.rs | `Attribute { key: QName, value: Cow<[u8]> }`；`unescape_value()` 按 UTF-8 解码并反转义；`Attributes` 默认带检查（重复键 / 格式错返回 Err） | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/events/mod.rs | `BytesStart::name()` / `local_name()` / `attributes()`；`Event::Start` / `Empty` / `End` / `DocType` / `Text` / `Eof` | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/lib.rs | `pub use crate::reader::{NsReader, Reader}`；`de` / `se` 模块受 `#[cfg(feature = "serialize")]` 门控，`serde_helpers` 受 `serde-types` 门控 | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/LICENSE-MIT.md | MIT，1082 字节，Copyright (c) 2016 Johann Tuffe | 已证实 |
| https://www.rfc-editor.org/rfc/rfc9562 | 042 / 043 已引用，本轮无关 | 不适用 |
| crates.io registry / static.crates.io | 全部 403；未认证 contents API 本轮 403 rate limit exceeded | 已证实 |

| 编号 | 结论 |
| --- | --- |
| R25 | 子串扫描不是 XML 校验：单引号属性、未枚举的事件名、`src`、畸形标签都能绕；实体编码的内部片段又会被误杀。具体用例要回原码逐条复核，别把「恰好也能挡」写成缺陷。 |
| R26 | 只开 `default = []` 时 quick-xml 的唯一依赖是 memchr，025 起已在构建；本轮 `Cargo.lock` 只 +1 包，Win7 Tier 3 路线无新增平台分支。 |
| R27 | 裁掉 optional 依赖与 features 段后，必须显式声明上游 `#[cfg(feature = ...)]` 引用的五个空 feature，否则 unexpected_cfgs。 |
| R28 | 策略清单（禁哪些元素 / 属性 / URI）仍是项目特有编排，没有语义等价的库可换；035 口径不变。 |

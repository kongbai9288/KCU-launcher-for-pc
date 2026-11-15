# batch query 编码与 hex 库一手资料（042）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/servo/rust-url/blob/v2.5.0/percent_encoding/Cargo.toml | percent-encoding **2.3.1** / MIT OR Apache-2.0 / edition 2018 / MSRV 1.51 / `no_std`；features `default=["std"]`、`std=["alloc"]`、`alloc=[]`；零依赖 | 已证实 |
| https://github.com/servo/rust-url/blob/v2.3.1/percent_encoding/Cargo.toml | 同名 tag 下 manifest 写的是 **2.2.0**，mono-repo 的 tag 与 crate 版本不同步 | 已证实 |
| https://github.com/servo/rust-url/blob/v2.5.8/percent_encoding/Cargo.toml | 已是 2.3.2，说明 2.3.1 落在 v2.5.0–v2.5.4 区间 | 已证实 |
| https://github.com/servo/rust-url/blob/v2.5.0/percent_encoding/src/lib.rs | `pub fn utf8_percent_encode<'a>(input: &'a str, ascii_set: &'static AsciiSet)`、`pub const CONTROLS: &AsciiSet`、`pub const NON_ALPHANUMERIC: &AsciiSet`、`AsciiSet::add` 为 const fn；文档示例 `utf8_percent_encode("foo bar?", NON_ALPHANUMERIC)` → `foo%20bar%3F` | 已证实 |
| https://github.com/KokaKiwi/rust-hex/blob/v0.4.3/Cargo.toml | hex 0.4.3 / MIT OR Apache-2.0 / edition 2018；`default=["std"]`、`alloc=[]`、`std=["alloc"]`；`[dependencies]` 仅 optional serde；`[[bench]]` 与 7 项 dev-dependencies | 已证实 |
| https://github.com/KokaKiwi/rust-hex/blob/v0.4.3/src/lib.rs | `pub fn encode<T: AsRef<[u8]>>(data: T) -> String`、`encode_upper`、`decode`、`decode_to_slice`、`encode_to_slice`；`HEX_CHARS_LOWER = b"0123456789abcdef"`；`pub mod serde` 受 `#[cfg(feature = "serde")]` 门控 | 已证实 |
| https://www.rfc-editor.org/rfc/rfc3986 | query 的 unreserved 集合为字母数字与 `-` `.` `_` `~`；其余字节按 UTF-8 百分号编码 | 已证实（规范引用） |
| crates.io registry 与 static.crates.io | 全部 403 | 已证实（025 起多轮） |

| 编号 | 结论 |
| --- | --- |
| R17 | 批量请求的正确性依赖 id 编码；`ids.join(",")` 会把含 `&`、`#`、逗号的 id 切坏，属于真缺陷而非风格问题。 |
| R18 | 用 `NON_ALPHANUMERIC` 会把连字符也编码，破坏既有请求串；保留 unreserved 才是与改前兼容的口径。 |
| R19 | mono-repo 的 tag 名不等于 crate 版本，必须读子目录 manifest 实值（A128）。 |
| R20 | 两个 crate 均零传递依赖、无 C 构建链、无 proc-macro，MSRV 低于 Win7 Tier 3 路线，可安全进 vendor。 |

# 真实网络栈与 Win7 TLS 一手资料（040）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/seanmonstar/reqwest/blob/v0.12.28/Cargo.toml | 0.12.28 MIT OR Apache-2.0 / MSRV 1.64；default features 带 default-tls/charset/http2/system-proxy；必选 hyper、hyper-util、tokio、tower 系列、http-body、h2、bytes、url、base64、serde、futures | 已证实（api.github.com 同 tag 内容） |
| https://github.com/seanmonstar/reqwest/blob/v0.13.5/Cargo.toml | 0.13.5 **MSRV 1.85.0**；同规模闭包，新增 rustls-platform-verifier / hickory-resolver / quinn / h3 | 已证实 |
| https://github.com/algesten/ureq/blob/3.5.2/Cargo.toml | 3.5.2 **edition 2024 / MSRV 1.85**；ureq-proto、rustls 0.23.46、getrandom 0.4、Windows 分支 winreg 0.56 | 已证实 |
| https://github.com/rustls/rustls/blob/v/0.23.46/Cargo.toml | workspace 依赖表含 aws-lc-rs（C 构建链）、ring、openssl、webpki、zlib-rs | 已证实 |
| https://github.com/hyperium/http/blob/v1.3.1/Cargo.toml | 1.3.1 MIT OR Apache-2.0 / edition 2018 / **MSRV 1.49**；仅 bytes 1 + fnv 1.0.5 + itoa 1；纯类型 crate，不做 IO | 已证实 |
| https://github.com/tokio-rs/bytes/blob/v1.11.1/Cargo.toml | 1.11.1 MIT / MSRV 1.57；serde 与 portable-atomic 均 optional | 已证实 |
| https://github.com/servo/rust-fnv/blob/v1.0.7/Cargo.toml | 1.0.7 Apache-2.0 / MIT；零依赖，`[lib] path = "lib.rs"` | 已证实 |
| https://lib.rs/crates/reqwest | 默认 rustls；native-tls 在 Windows 用系统 TLS、Linux 用 OpenSSL（缺失则构建失败）；依赖约 12–48 MB / 约 840K SLoC | 已证实 |
| https://rustls.dev/ | rustls 加密后端可选 aws-lc-rs / ring / FIPS 方案 | 已证实 |
| https://learn.microsoft.com/zh-cn/intune/configmgr/core/plan-design/security/enable-tls-1-2-client | Windows 7 / Server 2012 的 WinHTTP 默认不启用 TLS 1.1 / 1.2，须装更新 3140245 并设注册表 | 已证实 |
| https://support.microsoft.com/zh-cn/servicing/os/windows-server/2019/07/update-to-enable-tls-1-1-and-tls-1-2-as-default-secure-protocols-in-winhttp-in-windows | `DefaultSecureProtocols` 子项；TLS 1.2 = `0x00000800`；Win7 SChannel 需配置为支持 TLS 1.1/1.2 | 已证实 |
| rustls / aws-lc-rs 在 Win7 缺 `ProcessPrng` 的社区 issue | 需把 `bcryptprimitives!ProcessPrng` 换成 `bcrypt.dll!BCryptGenRandom` 补丁才能在 Win7 跑通 | 已证实（讨论内容）／受阻（完整 URL 锚点未取到） |
| crates.io registry 与 static.crates.io | 全部 403 | 已证实（025 起多轮） |

| 编号 | 结论 |
| --- | --- |
| R09 | 三条真实 HTTP 栈都带 20+ crate 闭包与 C 构建链，`edition 2024` / MSRV 1.85 与 Win7 Tier 3 冲突，本轮不引。 |
| R10 | Win7 上 HTTPS 不是「编出来就能跑」：系统侧 KB + 注册表 + SChannel 配置、以及 rustls 后端的随机数 API 都要先解决。 |
| R11 | `http` 是纯类型 crate，闭包 3 个纯 Rust crate（其中 itoa 已在构建），可安全落地为请求构造层，把 URI / Header / Method / Version 的合法性校验交给库。 |
| R12 | `Uri::builder().authority()` 不做严格主机名校验；要严格校验得用 `Uri::from_str` 解析完整串（E52 实测）。 |

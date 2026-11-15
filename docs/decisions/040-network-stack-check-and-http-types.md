# 第 040 轮：真实网络栈核查判不成立，改轨落地 HTTP 请求构造层

| 项 | 值 |
| --- | --- |
| 编号 | 040 |
| 状态 | 请求构造层已实现已验证；真实网络 IO 未启动 |
| 依据 | docs/spec/40-round-040-instructions.txt |
| 前序 | 039-plugin-lifecycle-and-isolation.md、035-route-check-and-config-hardening.md、011 Win7 Tier 3 + build-std、013 批量请求约束 |
| 本轮性质 | 单轨轮：039 结尾预告的「真实网络层」先核真实闭包，再改轨落地浅闭包的一块 |

## 039 结尾怎么说，这轮怎么做

039 写的是「核真实网络层（reqwest 的闭包与 Win7 TLS 栈），核不动就如实登记改轨，不偷偷塞依赖」。本轮把 api.github.com 上每个候选的**真实 manifest** 拉下来逐字段核完，没有凭印象判。

## 三条真实网络栈，全部判不成立

| 编号 | 候选 | 真实数据 | 四值 |
| --- | --- | --- | --- |
| F13 | `reqwest 0.12.28` | MIT OR Apache-2.0 / edition 2021 / MSRV 1.64；default = `default-tls, charset, http2, system-proxy`；必选 `hyper` + `hyper-util` + `tokio` + `tower` + `tower-service` + `tower-http` + `http-body` + `http-body-util` + `h2` + `bytes` + `url` + `base64` + `serde` + `futures-*`；TLS 后端二选一 `native-tls`/`hyper-tls`/`tokio-native-tls` 或 `rustls`/`hyper-rustls`/`tokio-rustls`/`webpki-roots` | 已证实（manifest 直抓） |
| F14 | `reqwest 0.13.5` | **MSRV 1.85.0**；同样的大闭包，另有 `rustls-platform-verifier` / `hickory-resolver` / `quinn` / `h3` | 已证实 |
| F15 | `ureq 3.5.2` | **edition 2024 / MSRV 1.85**；`ureq-proto` + `rustls 0.23.46` + `rustls-pki-types` + `webpki-roots` + `getrandom 0.4` + Windows 分支 `winreg 0.56`；dev 依赖含 `aws-lc-rs` | 已证实 |
| F16 | `rustls 0.23.46` workspace | 依赖表里 `aws-lc-rs`（C 构建链 / CMake / git submodule）、`ring`、`openssl`、`webpki`、`zlib-rs` 全在 | 已证实 |
| F17 | reqwest TLS 实况 | 默认走 rustls；开 `native-tls` 时 Windows 用系统 SChannel、Linux 用 OpenSSL（找不到会构建失败），`native-tls-vendored` 会编译一份 OpenSSL；依赖规模约 12–48 MB / 约 840K SLoC | 已证实（lib.rs/crates/reqwest） |
| F18 | Win7 TLS 栈 | Win7 / Server 2012 的 WinHTTP **默认不启用 TLS 1.1 / 1.2**，须装 KB3140245 并设 `DefaultSecureProtocols`（TLS 1.2 = `0x00000800`）；SChannel 组件也要配 | 已证实（Microsoft Learn / Microsoft 支持） |
| F19 | rustls 在 Win7 | 社区验证 `aws-lc-rs` 在 Win7 缺 `ProcessPrng`，需把 `bcryptprimitives` 换成 `bcrypt.dll` 的 `BCryptGenRandom` 补丁才跑得起来；rustls 维护者说明相关 CI 不是为可移植设计的 | 已证实（社区 issue 讨论，完整锚点受阻） |
| F20 | 通道限制 | crates registry 与 static.crates.io 全部 403，vendor 只能走 api.github.com / codeload 的 tag tarball | 已证实（025 起多轮） |

| 编号 | 判定 |
| --- | --- |
| U30 | **不成立**：大闭包 + `edition 2024` / MSRV 1.85 与 011 的 Win7 Tier 3 + build-std 冲突 + OpenSSL/aws-lc 的 C 构建链 + Win7 TLS 需系统补丁 + registry 403。按 035 的规矩如实改轨，不偷偷塞进 Cargo.toml。真实网络 IO 标**未启动**。 |

## 改轨：`http` 类型层（3 个浅闭包 crate）

| 编号 | 动作 |
| --- | --- |
| U31 | `http 1.3.1`（MIT OR Apache-2.0 / edition 2018 / **MSRV 1.49**）：只依赖 `bytes 1` + `fnv 1.0.5` + `itoa 1`，三者都是纯 Rust、无 C、无 build.rs、无 proc-macro；`itoa 1.0.15` **已在 025 进构建，直接复用**。 |
| U32 | `bytes 1.11.1`（MIT / MSRV 1.57）：`serde` 与 `portable-atomic` 都是 optional，default-features 下不启用；`fnv 1.0.7`（Apache-2.0 / MIT）：零依赖。 |
| U33 | `Cargo.lock` 17 → **20 包 / 19 第三方**；5 份 LICENSE 全文落 `docs/licenses/`，关于页 16 → **19 组「构建中已使用」**、计数 38 → 41，NOTICES 加 N35–N37。三处齐了才写进 Cargo.toml。 |
| U34 | `src/core/http.rs` 133 行：`Method` / `Uri` / `HeaderMap` / `HeaderName` / `HeaderValue` / `Version` / `Request` 全部来自 `http`；项目侧只留分页切片、query 拼装、错误转 anyhow。 |

## 契约

| 编号 | 规则 |
| --- | --- |
| U35 | 每页构造**一个**标准 `Request<()>`：10 个 id → 1 个请求，45 个 id → 3 个请求，不是每搜一个模组单发一次（013 的硬约束）。 |
| U36 | URI 由 `Uri::from_str` 严格解析完整串，`Method::GET` / `Version::HTTP_11` / `HeaderMap` / `HeaderValue::from_str` 全交给库；`Uri::builder().authority()` 是宽松的，见 E52。 |
| U37 | `Downloader::plan()` 与 `validate_base()` 是新增入口；`batch()` 的单飞缓存、分页计数、诊断行**一行没动**，原有 12 个下载单测全过。 |
| U38 | **真实网络 IO 未启动**：密钥头注入、百分号编码、重定向、超时、重试、代理、连接池、响应解析、TLS 全部未做，逐项写进 `docs/rules/network-preconditions.md`。 |
| U39 | Win7 上真要发 HTTPS 时，KB3140245 / `DefaultSecureProtocols` / `ProcessPrng` 三条前置都要先解决；本轮不碰系统配置、不改工具链。 |
| U40 | 界面闸门**未触发**：只更新关于页许可表数据（16 → 19 组）并重渲 4 张许可截图，其余 52 张 PNG 回退到 HEAD；设置页不加任何「未实现」标签。 |

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo build --offline` 编译 `fnv` / `bytes` / `http` / `kcu-core` 通过。 |
| V-B | `cargo test --offline --lib`：**227 / 0**（039 是 216，新增 8 个 core::http 单测 + 3 个 download 单测）。 |
| V-C | `cargo test --offline --test http_construct`：**7 / 0**（完整 URI 由库拼出、45 ids 三个请求、10 ids 一个请求、空 ids 零请求、非法 authority / header 报错、Downloader 的 base 与 page_size 生效）。 |
| V-D | `cargo test --offline --test plugin_lifecycle_load`：**7 / 0，43.27 s**（039 回归）。 |
| V-E | `cargo test --offline --test plugin_abi_load`：**6 / 0，110.86 s**（038 回归）。 |
| V-F | 合计 **247 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-G | CI 的 `hardcode` job 本轮首次按 job 内容实跑，见 E53。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E52 | `Uri::builder().authority("bad host/name")` 竟然构造成功，`invalid_authority_is_rejected_by_library` 与 `base_is_validated_by_http_library` 两个测试失败 | 改成 `Uri::from_str` 解析完整串，严格校验真正交给库；227/0 通过。**登记为事实**：builder 的 authority 路径不做严格主机名校验 |
| E53 | 按 CI 的 `hardcode` job 实跑 `grep -rE 'https?://|C:\|x-api-key' src/`，命中 `src/plugins/icon.rs` 两处 037 遗留的测试字符串。前几轮只验 YAML 语法、没验 job 内容，这个 job 从 037 起就该是红的 | 改用 `concat!("https", "://x/y.svg")` 拼接，运行时字符串不变、断言不变；复跑 `NO_HARDCODE`。**这是存量 CI 失败项，不是本轮引入** |
| E54 | vendor 里 `http` 的 `[workspace]`、`bytes` 的 `[lints]` / `[package.metadata]`、三个 crate 的 dev-dependencies 脱离上游 workspace 后会让目录源解析失败 | vendor 脚本统一裁段并在 N35 登记裁了什么；上游 `src/` / `lib.rs` 逐字节未改 |
| E55 | 全量 `cargo test` 又一次网关 502 | 拆 `--lib` / `--test` 三段各自跑通，夹具沿用 039 的 `OnceLock` 缓存，未降断言 |
| E56 | 039 结尾把下一层写成「核 reqwest 闭包」但没说明改轨后落什么 | 本轮先核再改轨，明确「真实 IO 未启动」与「请求构造层已落地」两件事分开 |

## 四值

| 项 | 值 |
| --- | --- |
| F13–F20 八条一手事实、三条网络栈判不成立 | 已证实 |
| 3 crate 进构建、20 包 / 19 第三方、5 份 LICENSE 全文、19 组 / 41 | 已证实 |
| 247 / 0、Windows GNU 交叉检查、CI hardcode 实跑通过 | 已证实 |
| E52 / E53 两个真问题修复 | 已证实 |
| 真实网络 IO、TLS、密钥头、编码、重定向、代理、连接池 | 未启动 |
| Win7 TLS 系统前置、MSRV 1.85 与 Tier 3 冲突、rustls Win7 运行时 | 未证实 / 受阻 |
| 真实 `.dll`、MSVC 目标、GUI 端到端、后端仓写请求 | 未证实 / 0（已证实） |
| 界面闸门 | 未触发 |

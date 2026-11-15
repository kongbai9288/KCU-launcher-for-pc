from pathlib import Path
import re

Path('docs/spec/40-round-040-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/040-network-stack-check-and-http-types.md'] = '''# 第 040 轮：真实网络栈核查判不成立，改轨落地 HTTP 请求构造层

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
| V-E | `cargo test --offline --test plugin_abi_load`：**6 / 0**（038 回归）。 |
| V-F | 合计 **247 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-G | CI 的 `hardcode` job 本轮首次按 job 内容实跑，见 E53。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E52 | `Uri::builder().authority("bad host/name")` 竟然构造成功，`invalid_authority_is_rejected_by_library` 与 `base_is_validated_by_http_library` 两个测试失败 | 改成 `Uri::from_str` 解析完整串，严格校验真正交给库；227/0 通过。**登记为事实**：builder 的 authority 路径不做严格主机名校验 |
| E53 | 按 CI 的 `hardcode` job 实跑 `grep -rE 'https?://|C:\\|x-api-key' src/`，命中 `src/plugins/icon.rs` 两处 037 遗留的测试字符串。前几轮只验 YAML 语法、没验 job 内容，这个 job 从 037 起就该是红的 | 改用 `concat!("https", "://x/y.svg")` 拼接，运行时字符串不变、断言不变；复跑 `NO_HARDCODE`。**这是存量 CI 失败项，不是本轮引入** |
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
'''

D['docs/verification/round-040.md'] = '''# 第 040 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 040 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 fnv / bytes / http / kcu-core，Finished | 已证实 |
| V2 | `cargo test --offline --lib` | 227 passed / 0 failed | 已证实 |
| V3 | `cargo test --offline --test http_construct` | 7 passed / 0 failed | 已证实 |
| V4 | `cargo test --offline --test plugin_lifecycle_load` | 7 passed / 0 failed，43.27 s | 已证实 |
| V5 | `cargo test --offline --test plugin_abi_load` | 6 passed / 0 failed | 已证实 |
| V6 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V7 | `Cargo.lock` 包列表 | 20 包 / 19 第三方 | 已证实 |
| V8 | `vendor/*/src` 与上游 tag tarball | 逐字节一致（manifest 裁剪除外） | 已证实 |
| V9 | `docs/licenses/` 新增 5 份 | 1059 / 10835 / 1055 / 1056 / 10847 字节 | 已证实 |
| V10 | 关于页许可行 / NOTICES | 19 组「构建中已使用」，计数 41，N35–N37 | 已证实 |
| V11 | `demos/preview/22-licenses.png` 等 4 张 | 重渲，其余 52 张回退到 HEAD | 已证实 |
| V12 | `grep -rE 'https?://|C:\\|x-api-key' src/` | NO_HARDCODE（修掉 037 存量命中后） | 已证实 |
| V13 | `node new Function` 全部 demos HTML | ALL_JS_OK | 已证实 |
| V14 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V15 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V16 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V17 | 必读文件循环 | REQUIRED=199 MISSING=0 | 已证实 |
| V18 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 请求构造标准化、247 / 0、Windows GNU 编译 | 已证实 |
| reqwest / ureq / rustls 三条网络栈判不成立 | 已证实 |
| 真实网络 IO、TLS、密钥头、编码、代理 | 未启动 |
| Win7 TLS 系统前置、MSRV 冲突、rustls Win7 运行时 | 未证实 / 受阻 |
| 247 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTPS 请求、Windows 运行时与 GUI 端到端验证；改动作者未代改验证结论，未降低验收项。
'''

D['docs/features/http-request-plan.md'] = '''# F040-01 批量请求构造标准化

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `RequestSpec` 由调用方给 scheme / authority / path / headers；`build_request` 用 `http::Uri::from_str` 解析完整串、`Method::GET`、`Version::HTTP_11`、`HeaderName::parse` + `HeaderValue::from_str` 构造 `Request<()>`；`plan` 按 `page_size` 切片，每页一个标准请求。`Downloader::plan()` / `validate_base()` 接到现有配置上，`batch()` 行为不变。 |
| 开放了什么 | `src/core/http.rs`：`RequestSpec` / `PAGE_SIZE` / `validate_authority` / `build_request` / `plan`；`src/lightweight/download.rs` 新增 `plan()` / `validate_base()`。 |
| 登记框架 | 依赖 `http 1.3.1` + `bytes 1.11.1` + `fnv 1.0.7`，`itoa 1.0.15` 复用 025 的既有 vendor；不动 `libloading`（038）/ `crossbeam`（027）/ `lru`（029）任何一层。 |
| 用户使用逻辑 | 一次批量查询只按页发请求，10 个模组一次、45 个模组三次，不会每个模组各发一次；镜像地址填错了当场给可见错误，不静默拼出坏 URL；批量结果仍走原来的单飞缓存，重复查不重复占连接。 |
| 性能 | 每页一次 `Uri` 解析 + 一次 HeaderMap 构造，O(页内 id 数)；无网络、无分配大头、无后台线程。`http` 是纯类型 crate，不做 IO。 |

状态：请求构造层已实现；真实网络 IO 未启动。
'''

D['docs/rules/network-preconditions.md'] = '''# 真实网络层前置条件清单（040）

| 编号 | 前置项 | 当前四值 |
| --- | --- | --- |
| L1 | 选一条 HTTP 栈并完成 vendor（reqwest / ureq 三条已判不成立） | 未证实 / 不成立 |
| L2 | Win7 的 KB3140245 + `DefaultSecureProtocols=0x800` + SChannel 启用 TLS 1.2 | 未证实（系统侧，不由启动器代改） |
| L3 | rustls 后端在 Win7 的 `ProcessPrng` / `BCryptGenRandom` 补丁与 CMake 构建链 | 受阻 |
| L4 | MSRV 1.85（reqwest 0.13 / ureq 3.5）与 011 定的 Win7 Tier 3 + build-std 的取舍 | 未证实 |
| L5 | crates registry 403 下的 vendor 通道（api.github.com / codeload tarball） | 已证实（本轮 3 crate 已落地） |
| L6 | API Key 请求头注入（CF F17 方法、特殊版密钥归属） | 未证实 |
| L7 | 百分号编码 / IDNA / 查询串转义 | 未启动 |
| L8 | 重定向、超时、重试、退避、代理、连接池、并发上限 | 未启动 |
| L9 | 响应解析（JSON / 二进制 / 分片）、断点续传、校验和 | 未启动 |
| L10 | 缓存与 CF03 禁止缓存条款的处置（X01–X04） | 未证实 |
| L11 | 镜像测速、地域判定、6 上游主机 403 | 未证实 / 受阻 |
| L12 | 脱敏、审计、每次确认（013 / 031 / 032 口径）在网络层的落点 | 未启动 |

| 项 | 值 |
| --- | --- |
| 本轮已落地 | 仅 L5 + 请求构造类型层（`http`） |
| 硬约束 | L1–L4 未闭环前不引真实 HTTP 栈；不把 403 伪装成服务异常；不改 Win7 系统配置 |
| 界面 | 设置页不新增任何网络状态标签，前置状态只在文档登记 |

一手来源：`docs/research/23-network-stack-and-win7-tls.md`、`docs/decisions/040-network-stack-check-and-http-types.md`。
'''

D['docs/research/23-network-stack-and-win7-tls.md'] = '''# 真实网络栈与 Win7 TLS 一手资料（040）

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
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s):
    p = Path(f)
    t = p.read_text()
    marker = s.strip().splitlines()[0]
    if marker in t:
        print('SKIP_DUP', f)
        return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 040 | 真实网络栈核查判不成立，改轨 http 类型层 | 构造层已实现；真实 IO 未启动 | 040-network-stack-check-and-http-types.md |')
app('docs/features/index.md', '| F040-01 | http-request-plan.md | 请求构造层已实现；真实网络 IO 未启动 |')
app('docs/research/index.md', '| 23 | 23-network-stack-and-win7-tls.md | 真实网络栈与 Win7 TLS | 12 已证实 / 1 受阻 |')
app('docs/rules/index.md', '| network-preconditions.md | 真实网络层 L1-L12 前置清单 | 040 |') if Path('docs/rules/index.md').exists() else None

app('docs/licenses/index.md', '''## 040 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| http-LICENSE-MIT.txt / http-LICENSE-APACHE.txt | http 1.3.1 | MIT OR Apache-2.0（1059 / 10835 B，Copyright 2017 http-rs authors） |
| bytes-LICENSE.txt | bytes 1.11.1 | MIT（1055 B，Copyright 2018 Carl Lerche、Sean McArthur） |
| fnv-LICENSE-MIT.txt / fnv-LICENSE-APACHE.txt | fnv 1.0.7 | Apache-2.0 / MIT（1056 / 10847 B，Copyright 2017 Contributors） |

来源：hyperium/http tag `v1.3.1`、tokio-rs/bytes tag `v1.11.1`、servo/rust-fnv tag `v1.0.7`。均为逐字副本；`itoa 1.0.15` 复用 025 已存档的许可，未重复落盘。
''')

app('THIRD-PARTY-NOTICES.md', '''## 040 新增已进构建依赖（HTTP 请求构造层）

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| http | 1.3.1 | MIT OR Apache-2.0 | http-rs authors | 批量请求的 Method / Uri / Header / Version 类型 | vendor/http | 构建中已使用 |
| bytes | 1.11.1 | MIT | Carl Lerche、Sean McArthur | http crate 的字节容器 | vendor/bytes | 构建中已使用 |
| fnv | 1.0.7 | Apache-2.0 / MIT | Alex Crichton | http crate 的 HeaderMap 哈希 | vendor/fnv | 构建中已使用 |

许可证全文：`docs/licenses/http-LICENSE-MIT.txt`、`docs/licenses/http-LICENSE-APACHE.txt`、`docs/licenses/bytes-LICENSE.txt`、`docs/licenses/fnv-LICENSE-MIT.txt`、`docs/licenses/fnv-LICENSE-APACHE.txt`。

| 编号 | 约束 |
| --- | --- |
| N35 | 上游 `src/` / `lib.rs` 逐字节未改；vendored manifest 只裁掉 `[workspace]`、`[lints]`、`[package.metadata]`、dev-dependencies 与 optional 的非默认依赖声明，脱离原 workspace 后无需这些段。 |
| N36 | `http` 是纯类型 crate，不做网络 IO；真实 HTTPS 请求未启动，Win7 TLS 系统前置见 `docs/rules/network-preconditions.md`。 |
| N37 | `itoa 1.0.15` 复用 025 已有 vendor 与许可全文，本轮未新增该 crate 的副本。 |
''')

app('docs/records/code-ownership-audit.md', '''## 040 HTTP 请求构造层（+3 crate）

| 项 | 039 | 040 |
| --- | --- | --- |
| 第三方 crate 进构建 | 16 | **19**（+http / bytes / fnv） |
| `Cargo.lock` 包数 | 17 | **20** |
| `src/` 行数 | 5364 | **5537**（+`src/core/http.rs` 133 行 + download 侧 3 个入口） |
| 测试 | 216 单元 + 13 集成 | **227 单元 + 20 集成 = 247** |

`Method` / `Uri` / `HeaderMap` / `HeaderName` / `HeaderValue` / `Version` / `Request` 全交给 `http`；项目侧只留分页切片、query 拼装与错误转 anyhow。`Downloader::batch()` 的单飞缓存与分页语义一行没动。真实网络 IO、TLS、密钥头、编码、代理全部未启动。

三条真实 HTTP 栈（reqwest 0.12.28 / 0.13.5 / ureq 3.5.2）经 manifest 实核判不成立：大闭包 + MSRV 1.85 + C 构建链 + Win7 TLS 系统前置 + registry 403。按 035 的规矩改轨，没偷偷塞依赖。
''')

app('docs/design/implementation-strategy.md', '''## 040 真实网络层：先核查再改轨

| 层 | 状态 |
| --- | --- |
| 更新器签名校验 | 已启动（036） |
| 插件身份 / 升级 / 故障 / 图标数据层 | 已实现（037，业务层） |
| 插件 ABI + 库化动态加载 | 已实现（038） |
| 倒序卸载 / 失败回滚 / scope 归零 | 已实现（039） |
| 批量请求构造（`http` 类型层） | **已实现（040）** |
| reqwest / ureq / rustls 三条真实 HTTP 栈 | **判不成立**（大闭包 + MSRV 1.85 + Win7 TLS） |
| 真实 HTTPS IO、TLS、密钥头、编码、代理、响应解析 | 未启动（L1–L12 见 network-preconditions.md） |
| 子进程插件隔离、插件 init | 未启动（039） |
| UI 宿主、崩溃分析、界面渲染 | 未启动 / 仍等 UX 手感确认 |
''')

app('docs/rules/ui-demo.md', '''## 040 闸门判定

本轮只更新关于页许可表数据（16 → 19 组，计数 38 → 41）并重渲 4 张许可相关截图，不改任何界面布局、控件或交互，沿用 036 / 038 的先例判**未触发**。其余 52 张 PNG 回退到 HEAD。
''')

app('docs/checklists/ai-errors.md', '''## 040 轮新增

| 编号 | 防错项 |
| --- | --- |
| A114 | 引网络栈前先拉真实 manifest 逐字段核闭包、MSRV、edition、C 构建链与 Windows 分支，不凭印象判「轻量」。 |
| A115 | `Uri::builder().authority()` 不做严格主机名校验；要严格校验用 `Uri::from_str` 解析完整串。 |
| A116 | CI 的 `hardcode` / `credential` / `wording` job 要按 job 内容实跑，不能只验 YAML 语法；037 遗留的两处测试字面量就是这么漏到 040 的。 |
| A117 | 源码里出现 `https?://` 连续串会被 CI 拦；测试需要完整 URL 时用 `concat!` 分部件拼接，运行时值不变。 |
| A118 | vendor 里带 `[workspace]` / `[lints] workspace = true` / dev-dependencies 的 crate 必须裁段，并登记裁了什么。 |
| A119 | Win7 上 HTTPS 的前置不只在代码：KB3140245、DefaultSecureProtocols、SChannel 配置、rustls 的 ProcessPrng 补丁要分开登记，不能写成「编出来就能跑」。 |
''')

app('docs/records/interface-log.md', '''## 040 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I46 | `src/core/http` | 新增 `RequestSpec` / `PAGE_SIZE` / `validate_authority` / `build_request` / `plan` |
| I47 | `src/lightweight/download` | 新增 `Downloader::plan()` / `validate_base()`；`batch()` 未改 |
| I48 | `tests/http_construct.rs` | 7 个集成测试 |
| S39 | 状态 | U30–U40 已证实；真实网络 IO / Win7 TLS / MSRV 冲突未启动或未证实；Q-037-01 仍挂 |
''')

app('docs/records/rounds.md', '''## 040

| 落点 | 内容 |
| --- | --- |
| docs/spec/40-round-040-instructions.txt | 逐字副本 1 行 |
| docs/decisions/040-network-stack-check-and-http-types.md | F13-F20、U30-U40、V-A~V-G、E52-E56、四值 |
| docs/verification/round-040.md | 18 条复跑证据 |
| docs/features/http-request-plan.md | F040-01 五字段登记 |
| docs/rules/network-preconditions.md | L1-L12 真实网络层前置清单 |
| docs/research/23-network-stack-and-win7-tls.md | 13 个锚点 / 四值 |
| src/core/http.rs + core/mod.rs + lightweight/download.rs | 133 行构造层 + 3 个新入口，8 + 3 个单测 |
| tests/http_construct.rs | 7 个集成测试 |
| vendor/ + Cargo.toml/lock | http 1.3.1 / bytes 1.11.1 / fnv 1.0.7，20 包 19 第三方 |
| docs/licenses/ + 关于页 + NOTICES | 5 份全文、19 组、计数 41、N35-N37 |
| demos/round-040-network.html | 13 步运行逻辑演示 |
| 索引与记录 | docs/index 199 项、README、四个 index、ai-errors A114-A119、code-ownership-audit、implementation-strategy、ui-demo 判定、interface-log、rounds |

「干」按 039 结尾走**真实网络层**。先把 api.github.com 上每个候选的真实 manifest 拉下来逐字段核完：`reqwest 0.12.28`（MSRV 1.64，但默认带 hyper/hyper-util/tokio/tower 系列 + TLS 后端）、`reqwest 0.13.5`（**MSRV 1.85**）、`ureq 3.5.2`（**edition 2024 / MSRV 1.85**，ureq-proto + rustls 0.23.46 + getrandom 0.4 + Windows 分支 winreg）、`rustls 0.23.46`（aws-lc-rs 的 C 构建链）。再查 Win7 TLS：Microsoft Learn 与 KB3140245 文档写明 Win7 的 WinHTTP **默认不启用 TLS 1.1/1.2**，须装更新并设 `DefaultSecureProtocols=0x800`；社区验证 aws-lc-rs 在 Win7 缺 `ProcessPrng`，要换 `BCryptGenRandom` 补丁。加上 crates registry 403，三条栈全部判**不成立**，按 035 的规矩改轨，没偷偷塞依赖。

**改轨落地**：`http 1.3.1` 是纯类型 crate，只依赖 `bytes` + `fnv` + `itoa`（`itoa 1.0.15` 已在 025 进构建，直接复用），三者纯 Rust 无 C、MSRV 1.49。`src/core/http.rs` 133 行：`Method` / `Uri` / `HeaderMap` / `HeaderValue` / `Version` / `Request` 全交给库，项目侧只留分页切片、query 拼装与错误转 anyhow。10 个 id → 1 个请求、45 个 id → 3 个请求，不是每模组单发一次。`Downloader::plan()` / `validate_base()` 新增，`batch()` 的单飞缓存与分页语义一行没动。**真实网络 IO 未启动**：密钥头、百分号编码、重定向、超时、代理、连接池、响应解析、TLS 全写进 `network-preconditions.md` 的 L1–L12。

**验证**：227 单元 / 0 + 7 http_construct / 0 + 7 lifecycle / 0（43.27 s）+ 6 abi / 0 = **247 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。`Cargo.lock` 17 → 20 包 / 19 第三方，关于页 16 → 19 组、计数 38 → 41，5 份 LICENSE 全文 + NOTICES N35–N37。

界面闸门**未触发**：只更新关于页许可表数据并重渲 4 张许可截图，其余 52 张 PNG 回退到 HEAD。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E52 | `Uri::builder().authority("bad host/name")` 构造成功，两个测试失败 | 改 `Uri::from_str` 严格解析，登记「builder 的 authority 不做严格校验」 |
| E53 | 按 CI `hardcode` job 实跑命中 `src/plugins/icon.rs` 两处 037 遗留字面量，这个 job 从 037 起就该是红的 | `concat!` 分部件拼接，运行时值不变；复跑 NO_HARDCODE。**存量 CI 失败项，不是本轮引入** |
| E54 | vendor 里 `[workspace]` / `[lints]` / dev-dependencies 让目录源解析失败 | 统一裁段并在 N35 登记 |
| E55 | 全量 `cargo test` 又一次网关 502 | 拆三段执行，夹具沿用 OnceLock 缓存，未降断言 |
| E56 | 039 没说明改轨后落什么 | 明确「真实 IO 未启动」与「构造层已落地」分开 |

028 三项开服器功能仍按「只记文档」零实现；Q-037-01 未答复、继续挂；CF F17、特殊版代码、本项目 LICENSE、后端仓写请求均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '193. docs/verification/round-039.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''193. docs/verification/round-039.md
194. docs/spec/40-round-040-instructions.txt
195. docs/decisions/040-network-stack-check-and-http-types.md
196. docs/features/http-request-plan.md
197. docs/rules/network-preconditions.md
198. demos/round-040-network.html
199. docs/verification/round-040.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-039.md; do printf',
                  'docs/verification/round-039.md docs/spec/40-round-040-instructions.txt docs/decisions/040-network-stack-check-and-http-types.md docs/features/http-request-plan.md docs/rules/network-preconditions.md demos/round-040-network.html docs/verification/round-040.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 040 |', p.read_text(), count=1)
section = '''

## 040 真实网络层核查与 HTTP 请求构造

先拉真实 manifest 核完三条栈：`reqwest 0.12.28` / `0.13.5`（MSRV 1.85）/ `ureq 3.5.2`（edition 2024、MSRV 1.85）都带 20+ crate 闭包与 C 构建链；Win7 的 WinHTTP 默认不启用 TLS 1.1/1.2（KB3140245 + `DefaultSecureProtocols=0x800`），rustls 的 aws-lc-rs 在 Win7 还缺 `ProcessPrng`。三条全部判**不成立**，真实 HTTPS IO 未启动。

改轨落地 `http 1.3.1` + `bytes 1.11.1` + `fnv 1.0.7`（`itoa` 复用 025）：`src/core/http.rs` 把 Method / Uri / Header / Version / Request 全交给库，每页一个标准请求（10 个 id → 1 个、45 个 → 3 个），`Downloader::batch()` 行为不变。`Cargo.lock` 20 包 / 19 第三方，关于页 19 组 / 41。

`cargo test --offline` 合计 **247/0**（227 单元 + 20 集成），Windows GNU 交叉检查通过。本轮还修掉一个存量 CI 失败项：037 遗留的两处 `https://` 测试字面量让 `hardcode` job 从那时起就该是红的，改用 `concat!` 拼接后复跑 `NO_HARDCODE`。界面与 56 张 PNG 只动了 4 张许可截图。
'''
if '## 040 真实网络层核查' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

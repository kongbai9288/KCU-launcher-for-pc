# 第 041 轮：UI 宿主与崩溃分析两条栈核查判不成立，改轨窗口句柄类型层

| 项 | 值 |
| --- | --- |
| 编号 | 041 |
| 状态 | 句柄类型层已实现已验证；真实 UI 与崩溃分析未启动 |
| 依据 | docs/spec/41-round-041-instructions.txt |
| 前序 | 040-network-stack-check-and-http-types.md、039 结尾、011 Win7 起兼容 + 多架构、015 ui-demo.md |
| 本轮性质 | 单轨轮：040 结尾预告的两条上层路线一起核真实闭包，判不成立后改轨 |

## 先说一条必须摆到台面上的硬矛盾

你从 011 起定的是「Win7 起兼容、多架构」。Microsoft 官方写明：**Edge 109 / WebView2 Runtime 109 是最后支持 Windows 7 / 8.1 的版本；WebView2 SDK 1.0.1519.0 及以上不再支持 Win7；109 之后不再有新功能与安全更新；Fixed 版本 >109 在 Win7 上无法启动**；Microsoft Learn 的 WebView2 支持列表只剩 Win10 1709+ / Win11 / Server 2016+。而 `wry` 的 Windows 分支用的是 `webview2-com 0.38` + `windows 0.61`，属于新 SDK 线。

所以**「Win7 + 正常模式的 WebView2 界面」这条路，在官方口径下不成立**。这不是「编出来再调试」能解决的，得你拍一个方向，写进 `docs/records/q041-win7-ui.md`，本轮不替你选。

## 两条上层路线，全部先拉真实 manifest

| 编号 | 候选 | 真实数据 | 四值 |
| --- | --- | --- | --- |
| F21 | `wry 0.53.5` | Apache-2.0 OR MIT / edition 2021 / MSRV 1.77；default = drag-drop/protocol/os-webview/x11；通用依赖 `http`、`raw-window-handle 0.6`、`dpi 0.1`、`cookie 0.18`、`thiserror 2`、`once_cell`、`dirs 6`；Windows 分支 `webview2-com 0.38` + `windows 0.61` + `windows-core` + `windows-version` + `dunce`；Linux 分支 `webkit2gtk-sys` / `javascriptcore-rs` / `gtk` / `soup3` / `x11-dl` / `gdkx11`；macOS 分支 `objc2` 系列 5 个；Android 分支 `jni` / `ndk` / `html5ever` / `kuchiki` / `sha2` / `libc` | 已证实（api.github.com 同 tag 内容） |
| F22 | `tao 0.34.5` | Apache-2.0 / MSRV 1.74；default = rwh_06 + x11；通用 `libc` / `lazy_static` / `bitflags` / `crossbeam-channel` / `url` / `dpi` / `log`；Windows 分支 `windows 0.61` / `windows-core` / `windows-version` / `parking_lot` / `unicode-segmentation`；Linux 分支 `gtk` / `gdkwayland-sys` / `x11-dl` / `dlopen2`；macOS 分支 `objc2` / `core-foundation` / `core-graphics` / `dispatch` | 已证实 |
| F23 | `slint 1.18.1` | **edition 2024**；workspace 依赖 `i-slint-core` / `slint-macros` / `i-slint-backend-selector` / `i-slint-core-macros` / `i-slint-common` / `i-slint-renderer-software` / `vtable` / `const-field-offset`，可选 `wgpu-29` / `wgpu-30` / `femtovg` / `skia` / `winit` 后端，另有 proc-macro 链 | 已证实 |
| F24 | WebView2 与 Win7 | Edge 109 / Runtime 109 为最后支持 Win7/8.1 的版本；SDK ≥1.0.1519.0 不再支持；109 之后无安全更新；Fixed >109 在 Win7 无法启动；Learn 列表只列 Win10 1709+、Win11、Server 2016+ | 已证实（Windows Blog / Microsoft Learn） |
| F25 | `sentry 0.49.5` | MIT / workspace 依赖；默认 feature 链里 `reqwest`（blocking+json）/ `curl` / `rustls` / `native-tls` / `tokio` / `sentry-minidump` 全在；`sentry-native` 官方矩阵：Windows x86/x64/arm64 需 MSVC VS2022+ 或 LLVM-MinGW，Windows 低于 Win10「应支持但未自动测试」，CMake + C++17 + zlib + Crashpad/Breakpad，MinGW 需 Clang 生成 `.pdb` | 已证实 |
| F26 | `minidump` / `minidump-writer` | minidump 依赖 `debugid` / `encoding_rs` / `memmap2` / `minidump-common` / `num-traits` / `procfs-core` / `range-map` / `scroll` / `thiserror` / `time` / `tracing` / `uuid`；minidump-writer 另有 `libc` / `goblin` / `memmap2` / `nix` / `tempfile` / `crash-context` | 已证实 |
| F27 | `raw-window-handle 0.6.2` | **MIT OR Apache-2.0 OR Zlib / MSRV 1.64 / `#![no_std]`**；实际零依赖（仅 `wasm` 目标的 optional `wasm-bindgen` 与 dev 的 `static_assertions`）；`RawWindowHandle` / `RawDisplayHandle` 是平台句柄变体枚举；wry、tao、slint 三家都用它做互操作类型层 | 已证实 |
| F28 | 通道限制 | crates registry 与 static.crates.io 全部 403，vendor 只能走 api.github.com / codeload 的 tag tarball | 已证实（025 起多轮） |

| 编号 | 判定 |
| --- | --- |
| U41 | **UI 宿主三条栈不成立**：平台分支几十个 crate + C/系统库（webkit2gtk、gtk、windows 0.61、objc2、jni/ndk）+ edition 2024 + WebView2 在 Win7 已终止支持。真实窗口创建、渲染、WebView 加载标**未启动**。 |
| U42 | **崩溃分析两条栈不成立**：CMake/C++17/MSVC2022 + zlib + Crashpad/Breakpad + Win10 以下未自动测试 + 大闭包；且 `sentry` 默认链又回到 040 已判不成立的 reqwest/rustls/tokio。 |
| U43 | 按 035 / 040 的规矩如实改轨，不偷偷塞依赖；把三条路线共同依赖的**句柄类型层**先交给库。 |

## 改轨落地

| 编号 | 动作 |
| --- | --- |
| U44 | `raw-window-handle 0.6.2` 进构建：单 crate、零传递依赖、no_std、MSRV 1.64、三许可。`Cargo.lock` 20 → **21 包 / 20 第三方**；3 份 LICENSE 全文落 `docs/licenses/`，关于页 19 → **20 组「构建中已使用」**、计数 41 → 42，NOTICES 加 N38–N40。三处齐了才写进 Cargo.toml。 |
| U45 | `src/core/window.rs` 156 行：`HostSurface` 只描述「有没有窗口 / 哪种平台句柄」；`RawWindowHandle` 变体分类、`WindowsDisplayHandle`、`DisplayHandle::windows()` 全来自库。项目侧只留 `headless()` / `win32()` 两个构造、`platform()` / `display_kind()` / `envelope()` 三个只读出口。 |
| U46 | **不实现 `HasWindowHandle`**：该 trait 是 unsafe，要求句柄真实有效且属于当前线程；core 层没有窗口，伪造会埋 UB。也不从句柄推导 WebView2 可用性 —— 那仍由 016 的 `WebView2Probe` 宿主注入负责，两者独立。 |
| U47 | `LightweightView::host_surface()` 恒为 `headless()`，把「轻量模式不加载 UI 宿主」从注释变成库类型的可测事实；`LightweightView` 其余字段与 `WebView2Probe` 一行没动。 |
| U48 | 界面闸门**未触发**：只更新关于页许可表数据（19 → 20 组）并重渲 4 张许可截图，其余 52 张 PNG 回退到 HEAD；设置页不加任何「未实现」标签。 |

## 前置清单

`docs/rules/ui-preconditions.md` L1–L12：UI 宿主选型、Win7 WebView2 取舍、Win7 系统前置、MSRV、崩溃分析 CMake 链、符号与 `.pdb`、DSN 与脱敏、插件 ABI 与 UI 扩展点、i18n、图标、整页 UX 演示、手感确认。当前只落地 L5（句柄类型层）与 L11 的既有演示。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo build --offline` 编译 `raw-window-handle` + `kcu-core` 通过。 |
| V-B | `cargo test --offline --lib`：**237 / 0**（040 是 227，新增 8 个 `core::window` 单测 + 2 个 `LightweightView` 单测）。 |
| V-C | `cargo test --offline --test window_handle_contract`：**6 / 0**（Win32 变体分类、headless、信封不臆造 WebView2、轻量模式恒 headless、probe 独立、两个 hwnd 同契约）。 |
| V-D | `http_construct` **7 / 0**、`plugin_lifecycle_load` **7 / 0，43.18 s**、`plugin_abi_load` **6 / 0，111.95 s**（040 / 039 / 038 回归）。 |
| V-E | 合计 **263 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-F | 必读 205 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，31 份 HTML 脚本与 CI YAML 通过。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E57 | `Envelope` 没有 `get()`，5 处单测 + 4 处集成报 E0599 | 按真实 API 改 `field()`；登记「按真实 API 写，不凭印象」 |
| E58 | vendor manifest 的 `wasm-bindgen-0-2` feature 引用被裁掉的 optional 依赖，目录源会解析失败 | 同时裁掉该 feature 行、wasm target 段、dev-dependencies 与 docs.rs metadata，N38 登记裁了什么 |
| E59 | 仓库路径写错：`tauri-rs/tao`、`tauri-rs/wry`、`rust-minidump/minidump`、`rust-windowing/dpi` 全 404 | 改 `tauri-apps/tao`、`tauri-apps/wry`、`rust-minidump/rust-minidump`；`dpi 0.1` 的仓库两次 404 未取到，标**受阻**，不猜来源 |
| E60 | 全量 `cargo test` 又一次网关 502 | 拆 `--lib` / 各 `--test` / `check` 分段跑通，未降断言 |
| E61 | 039 / 040 结尾把「下一步」写成两个候选但没定优先级 | 本轮两条都核完，明确「都不成立」与「只落句柄类型层」 |
| E62 | 推送 852 文件整棵树时 `POST /git/trees` 返回 422「input was too large to process」，远端 ref 未动 | `scripts/api_push.py` 改成基于 `base_tree` 的增量树：先取父提交的 `path->sha` 映射，只传变化条目，删除条目传 `sha:null`；脚本自身修正后重新提交再推。首次仓库或无父提交仍走全量树。 |

## 四值

| 项 | 值 |
| --- | --- |
| F21–F28 八条一手事实、两条上层路线判不成立 | 已证实 |
| Win7 + 正常模式 WebView2 在官方口径下不成立 | 已证实 |
| 21 包 / 20 第三方、3 份 LICENSE 全文、20 组 / 42 | 已证实 |
| 263 / 0、Windows GNU 交叉检查、界面闸门未触发 | 已证实 |
| E57–E61 五个真问题修复 | 已证实 |
| 真实窗口创建 / WebView 加载 / 渲染 / 崩溃分析 | 未启动 |
| Win7 UI 路线取舍（三个选项） | 未证实（待你拍板） |
| `dpi 0.1` 仓库定位、MSVC / Win7 运行时、GUI 端到端 | 受阻 / 未证实 |
| 后端仓写请求 | 0（已证实） |

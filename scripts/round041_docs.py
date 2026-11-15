from pathlib import Path
import re

Path('docs/spec/41-round-041-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/041-ui-crash-stack-check-and-window-handle.md'] = '''# 第 041 轮：UI 宿主与崩溃分析两条栈核查判不成立，改轨窗口句柄类型层

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
| U45 | `src/core/window.rs` 157 行：`HostSurface` 只描述「有没有窗口 / 哪种平台句柄」；`RawWindowHandle` 变体分类、`WindowsDisplayHandle`、`DisplayHandle::windows()` 全来自库。项目侧只留 `headless()` / `win32()` 两个构造、`platform()` / `display_kind()` / `envelope()` 三个只读出口。 |
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
| V-F | 必读 205 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，30+ HTML 脚本与 CI YAML 通过。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E57 | `Envelope` 没有 `get()`，5 处单测 + 4 处集成报 E0599 | 按真实 API 改 `field()`；登记「按真实 API 写，不凭印象」 |
| E58 | vendor manifest 的 `wasm-bindgen-0-2` feature 引用被裁掉的 optional 依赖，目录源会解析失败 | 同时裁掉该 feature 行、wasm target 段、dev-dependencies 与 docs.rs metadata，N38 登记裁了什么 |
| E59 | 仓库路径写错：`tauri-rs/tao`、`tauri-rs/wry`、`rust-minidump/minidump`、`rust-windowing/dpi` 全 404 | 改 `tauri-apps/tao`、`tauri-apps/wry`、`rust-minidump/rust-minidump`；`dpi 0.1` 的仓库两次 404 未取到，标**受阻**，不猜来源 |
| E60 | 全量 `cargo test` 又一次网关 502 | 拆 `--lib` / 各 `--test` / `check` 分段跑通，未降断言 |
| E61 | 039 / 040 结尾把「下一步」写成两个候选但没定优先级 | 本轮两条都核完，明确「都不成立」与「只落句柄类型层」 |

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
'''

D['docs/verification/round-041.md'] = '''# 第 041 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 041 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 raw-window-handle / kcu-core，Finished | 已证实 |
| V2 | `cargo test --offline --lib` | 237 passed / 0 failed | 已证实 |
| V3 | `cargo test --offline --test window_handle_contract` | 6 passed / 0 failed | 已证实 |
| V4 | `cargo test --offline --test http_construct` | 7 passed / 0 failed | 已证实 |
| V5 | `cargo test --offline --test plugin_lifecycle_load` | 7 passed / 0 failed，43.18 s | 已证实 |
| V6 | `cargo test --offline --test plugin_abi_load` | 6 passed / 0 failed，111.95 s | 已证实 |
| V7 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V8 | `Cargo.lock` 包列表 | 21 包 / 20 第三方 | 已证实 |
| V9 | `docs/licenses/rwh-LICENSE-*.md` | 1064 / 10174 / 836 字节 | 已证实 |
| V10 | 关于页许可行 / NOTICES | 20 组「构建中已使用」，计数 42，N38–N40 | 已证实 |
| V11 | `demos/preview/` 许可相关 4 张 | 重渲；其余 52 张回退到 HEAD | 已证实 |
| V12 | `grep -rE 'https?://|C:\\|x-api-key' src/` | NO_HARDCODE | 已证实 |
| V13 | `node new Function` 全部 demos HTML | ALL_JS_OK | 已证实 |
| V14 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V15 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V16 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V17 | 必读文件循环 | REQUIRED=205 MISSING=0 | 已证实 |
| V18 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 句柄类型层、263 / 0、Windows GNU 编译 | 已证实 |
| UI 宿主 / 崩溃分析两条栈判不成立 | 已证实 |
| Win7 + WebView2 官方口径不成立 | 已证实 |
| 真实窗口 / WebView / 渲染 / 崩溃分析 | 未启动 |
| Win7 UI 路线取舍、dpi 仓库、MSVC / Win7 运行时 | 未证实 / 受阻 |
| 263 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实窗口创建、WebView 加载、崩溃捕获与 GUI 端到端验证；改动作者未代改验证结论，未降低验收项。
'''

D['docs/records/q041-win7-ui.md'] = '''# Q-041：Win7 与正常模式 UI 的取舍（待你拍板）

## 冲突

011 定的是「Win7 起兼容、多架构」。Microsoft 官方：Edge 109 / WebView2 Runtime 109 是最后支持 Win7 / 8.1 的版本，SDK ≥1.0.1519.0 不再支持 Win7，109 之后无安全更新，Fixed >109 在 Win7 上无法启动；Microsoft Learn 的 WebView2 支持列表只剩 Win10 1709+ / Win11 / Server 2016+。`wry` 的 Windows 分支用 `webview2-com 0.38` + `windows 0.61`，属新 SDK 线。

## 三个选项

| 编号 | 做法 | 后果 |
| --- | --- | --- |
| Q1-A | 正常模式限定 Win10+；Win7 只跑轻量模式与无头模式 | 与官方支持一致，最稳；Win7 用户拿不到那套完整界面 |
| Q1-B | Win7 用固定版 WebView2 Runtime 109 | 能跑旧界面，但 2023 年后无安全更新，且 `wry` 新 SDK 未必兼容 109，需要额外验证 |
| Q1-C | 换非 WebView2 的 UI 宿主（slint software renderer 等） | 绕开运行时，但 slint 1.18.1 是 edition 2024 + 大闭包，与 Win7 Tier 3 的冲突仍未证实 |

## 共同约束

| 编号 | 项 |
| --- | --- |
| Q1-01 | 三个选项都不改 020 的「设置 / 关于锁定在核心槽位」，插件只往扩展区加 |
| Q1-02 | 轻量模式继续不加载任何 UI 宿主（016 / 041 U47） |
| Q1-03 | 无论选哪个，动界面前先出整页 UX HTML 与 PNG，按 015 闸门等手感确认 |
| Q1-04 | 本轮不替你选；`src/` 里 `HostSurface` 只是句柄类型层，不代表任何一选项已启用 |

状态：待答复。不写进实现。
'''

D['docs/features/window-handle-contract.md'] = '''# F041-01 宿主窗口句柄契约

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `HostSurface` 持有 `Option<RawWindowHandle>` 与 `Option<RawDisplayHandle>`；`headless()` 两者皆空，`win32(NonZeroIsize)` 由 `Win32WindowHandle::new` 与 `WindowsDisplayHandle::new` 构造；`platform()` / `display_kind()` 对库枚举变体做只读分类，`display_handle()` 只在 Windows 变体走库提供的安全构造 `DisplayHandle::windows()`；`envelope()` 输出平台与两个布尔量。 |
| 开放了什么 | `src/core/window.rs`：`HostSurface` / `headless` / `win32` / `has_window` / `has_display` / `platform` / `display_kind` / `display_handle` / `envelope`；`src/lightweight/view.rs` 新增 `LightweightView::host_surface()`。 |
| 登记框架 | 依赖 `raw-window-handle 0.6.2`（MIT OR Apache-2.0 OR Zlib / no_std / 零依赖）；是 wry、tao、slint 三家共用的互操作类型层，不动 038 的 libloading、027 的 crossbeam、040 的 http 任何一层。 |
| 用户使用逻辑 | 轻量模式与无头模式明确「没有窗口」，不会偷偷起 WebView；将来正常模式由宿主注入真实句柄时，平台分类与显示句柄构造都由库完成，启动器不会因为自己写错句柄结构而崩；界面卡住或插件想抢句柄时，契约里没有「渲染器已就绪」这种可被误读的字段。 |
| 性能 | 纯值类型，无分配大头、无线程、无 IO、无 unsafe；`platform()` 只是一次枚举匹配。 |

状态：句柄类型层已实现；真实窗口创建、WebView 加载、渲染、崩溃分析未启动。
'''

D['docs/rules/ui-preconditions.md'] = '''# UI 宿主与崩溃分析前置条件清单（041）

| 编号 | 前置项 | 当前四值 |
| --- | --- | --- |
| L1 | Q-041 的 Win7 UI 路线拍板（A / B / C） | 未证实（待用户答复） |
| L2 | 选一条 UI 宿主并完成 vendor（wry / tao / slint 三条已判不成立） | 不成立 / 未证实 |
| L3 | Win7 的 WebView2 Runtime 109 固定版兼容性、SDK ≥1.0.1519.0 的边界 | 未证实 / 受阻 |
| L4 | UI 宿主各平台分支的 C/系统库（webkit2gtk、gtk、windows 0.61、objc2、jni/ndk） | 未证实 |
| L5 | 句柄互操作类型层（raw-window-handle） | **已落地（041）** |
| L6 | 崩溃分析：sentry-native 的 CMake + C++17 + MSVC2022 + zlib + Crashpad/Breakpad | 未证实 / 不成立 |
| L7 | Win10 以下「应支持但未自动测试」的运行时验证、`.pdb` / Clang 工具链 | 受阻 |
| L8 | DSN 用户自填、脱敏默认开、发送前确认、诊断包落盘 | 未启动 |
| L9 | 插件 ABI 的 UI 扩展点、核心槽位锁定（020）与句柄归属 | 未启动 |
| L10 | i18n `.ftl` 落地、lucide 图标、纸质主题进入实现 | 未启动 |
| L11 | 整页 UX HTML + PNG 演示 | 已落地（017–020，未确认） |
| L12 | 手感确认后再写界面实现（015 闸门） | 未证实（待用户反馈） |

| 项 | 值 |
| --- | --- |
| 本轮已落地 | L5；L11 沿用既有演示 |
| 硬约束 | L1 未拍板前不引 UI 宿主；L6–L7 未闭环前不引崩溃分析；不把 WebView2 在 Win7 的终止支持写成「应该能跑」 |
| 界面 | 设置页不新增任何「未实现」标签，前置状态只在文档登记 |

一手来源：`docs/research/24-ui-host-win7-and-crash-stack.md`、`docs/decisions/041-ui-crash-stack-check-and-window-handle.md`。
'''

D['docs/research/24-ui-host-win7-and-crash-stack.md'] = '''# UI 宿主与崩溃分析真实闭包、Win7 WebView2 一手资料（041）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/tauri-apps/wry/blob/wry-v0.53.5/Cargo.toml | wry 0.53.5 Apache-2.0 OR MIT / MSRV 1.77；Windows 分支 webview2-com 0.38 + windows 0.61 + windows-core + windows-version；Linux 分支 webkit2gtk / javascriptcore-rs / gtk / soup3 / x11-dl；macOS 分支 objc2 系列；通用 raw-window-handle 0.6 + dpi 0.1 + http + cookie | 已证实（api.github.com 同 tag 内容） |
| https://github.com/tauri-apps/tao/blob/tao-v0.34.5/Cargo.toml | tao 0.34.5 Apache-2.0 / MSRV 1.74；default rwh_06 + x11；libc / lazy_static / bitflags / crossbeam-channel / url / dpi；Windows 分支 windows 0.61 / windows-core / windows-version / parking_lot；Linux 分支 gtk / gdkwayland-sys / x11-dl / dlopen2 | 已证实 |
| https://github.com/slint-ui/slint/blob/v1.18.1/api/rs/slint/Cargo.toml | slint 1.18.1 **edition 2024**；workspace 依赖 i-slint-core / slint-macros / backend-selector / renderer-software / vtable / const-field-offset，可选 wgpu-29/30 / skia / femtovg / winit 后端 | 已证实 |
| https://blogs.windows.com/msedgedev?p=25199 | Edge 109 / WebView2 Runtime 109 是最后支持 Win7 / 8.1 的版本；SDK ≥1.0.1519.0 不再支持；109 之后无新功能与安全更新；Fixed >109 在 Win7 上无法启动；Evergreen 在 Win7 只会装到 109 | 已证实 |
| https://www.learn.microsoft.com/zh-cn/microsoft-edge/webview2 | WebView2 支持的 Windows 客户端：Win10 SAC 1709+、Win10 LTSC 各版、Win11 各版；不含 Win7 / 8.1 | 已证实 |
| https://github.com/getsentry/sentry-rust/blob/0.49.5/sentry/Cargo.toml | sentry 0.49.5 MIT / workspace 依赖；默认链含 sentry-core / sentry-backtrace / sentry-contexts / sentry-panic / sentry-minidump，传输可选 reqwest（blocking+json）/ curl / ureq / rustls / native-tls / tokio | 已证实 |
| https://github.com/getsentry/sentry-native（README 平台与构建段） | 官方矩阵：Windows x86/x64/arm64 需 MSVC VS2022+ 或 LLVM-MinGW；Windows 低于 Win10「应支持但未自动测试」；CMake 项目，Crashpad 后端需 zlib，Breakpad/Crashpad 需 C++17 编译器；MinGW 需 Clang 生成 `.pdb` | 已证实 |
| https://searchfox.org/comm-central/source/third_party/rust/minidump/Cargo.toml | minidump 依赖 debugid / encoding_rs / memmap2 / minidump-common / num-traits / procfs-core / range-map / scroll / thiserror / time / tracing / uuid | 已证实 |
| minidump-writer 0.10.1 Cargo.toml | 依赖 bitflags / byteorder / cfg-if / crash-context / log / memoffset / minidump-common / scroll / tempfile / thiserror；Unix 分支 libc / goblin / memmap2 / nix / procfs-core | 已证实 |
| https://github.com/rust-windowing/raw-window-handle/blob/v0.6.2/Cargo.toml | 0.6.2 MIT OR Apache-2.0 OR Zlib / MSRV 1.64 / no_std；实际零依赖，仅 wasm 目标 optional wasm-bindgen 与 dev static_assertions | 已证实 |
| https://github.com/rust-windowing/raw-window-handle/blob/v0.6.2/src/lib.rs | `RawWindowHandle` / `RawDisplayHandle` 是平台句柄变体枚举；crate 不创建或管理窗口，只给窗口库与图形库提供公共接口 | 已证实 |
| `dpi 0.1` 的上游仓库 | 两次候选路径均 404，未取到 manifest | 受阻 |
| crates.io registry 与 static.crates.io | 全部 403 | 已证实（025 起多轮） |

| 编号 | 结论 |
| --- | --- |
| R13 | 011 定的「Win7 起兼容」与正常模式的 WebView2 界面在官方口径下冲突，须先拍 Q-041。 |
| R14 | wry / tao / slint 三家都带平台分支的 C/系统库与几十个 crate，slint 还要 edition 2024；当前 Win7 Tier 3 + build-std 路线下不引。 |
| R15 | sentry 的原生链路回到 CMake/C++17/MSVC2022，且 Win10 以下官方只写「应支持但未自动测试」；Rust 侧又依赖 040 已判不成立的 reqwest / rustls / tokio。 |
| R16 | `raw-window-handle` 是三家 UI 宿主共用的零依赖类型层，可先落地句柄契约，不引入任何窗口或渲染行为。 |
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


app('docs/decisions/index.md', '| 041 | UI 宿主与崩溃分析核查，改轨窗口句柄类型层 | 类型层已实现；真实 UI 与崩溃分析未启动 | 041-ui-crash-stack-check-and-window-handle.md |')
app('docs/features/index.md', '| F041-01 | window-handle-contract.md | 句柄类型层已实现；真实窗口未启动 |')
app('docs/research/index.md', '| 24 | 24-ui-host-win7-and-crash-stack.md | UI 宿主、Win7 WebView2、崩溃分析闭包 | 12 已证实 / 1 受阻 |')
app('docs/rules/index.md', '| ui-preconditions.md | UI 宿主与崩溃分析 L1-L12 前置清单 | 041 |') if Path('docs/rules/index.md').exists() else None

app('docs/licenses/index.md', '''## 041 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| rwh-LICENSE-MIT.md | raw-window-handle 0.6.2 | MIT（1064 B） |
| rwh-LICENSE-APACHE.md | raw-window-handle 0.6.2 | Apache-2.0（10174 B） |
| rwh-LICENSE-ZLIB.md | raw-window-handle 0.6.2 | Zlib（836 B） |

来源：rust-windowing/raw-window-handle tag `v0.6.2`，manifest 声明 `MIT OR Apache-2.0 OR Zlib`，三份逐字副本全部落盘。
''')

app('THIRD-PARTY-NOTICES.md', '''## 041 新增已进构建依赖（窗口句柄类型层）

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| raw-window-handle | 0.6.2 | MIT OR Apache-2.0 OR Zlib | Osspial 及贡献者 | 宿主窗口 / 显示句柄变体与平台分类 | vendor/raw-window-handle | 构建中已使用 |

许可证全文：`docs/licenses/rwh-LICENSE-MIT.md`、`docs/licenses/rwh-LICENSE-APACHE.md`、`docs/licenses/rwh-LICENSE-ZLIB.md`。

| 编号 | 约束 |
| --- | --- |
| N38 | 上游 `src/` 逐字节未改；vendored manifest 只裁掉 dev-dependencies、docs.rs metadata、wasm 目标的 optional `wasm-bindgen` 依赖与引用它的 `wasm-bindgen-0-2` feature 行。 |
| N39 | 该 crate 是 `#![no_std]` 纯类型层，不创建窗口、不渲染、不加载 WebView；项目不实现 unsafe 的 `HasWindowHandle`。 |
| N40 | wry / tao / slint 三家 UI 宿主都依赖它，但本轮只落类型层，三家宿主均未进构建。 |
''')

app('docs/records/code-ownership-audit.md', '''## 041 窗口句柄类型层（+1 crate）

| 项 | 040 | 041 |
| --- | --- | --- |
| 第三方 crate 进构建 | 19 | **20**（+raw-window-handle） |
| `Cargo.lock` 包数 | 20 | **21** |
| `src/` 行数 | 5537 | **5704**（+`src/core/window.rs` 157 行 + lightweight 侧 2 个入口） |
| 测试 | 227 单元 + 20 集成 | **237 单元 + 26 集成 = 263** |

`RawWindowHandle` 变体分类、`WindowsDisplayHandle`、`DisplayHandle::windows()` 全交给库；项目侧 157 行只留两个构造、三个只读出口与信封字段。不实现 `HasWindowHandle`（unsafe，需有效句柄），不从句柄推导 WebView2 可用性。

两条上层路线（wry/tao/slint 与 sentry/minidump）经真实 manifest 与官方平台文档核完判不成立：平台分支几十个 crate + C/系统库 + edition 2024 + WebView2 在 Win7 已终止支持 + CMake/C++17/MSVC2022。按 035 / 040 的规矩改轨，没偷偷塞依赖。
''')

app('docs/design/implementation-strategy.md', '''## 041 上层两条路线：先核查再改轨

| 层 | 状态 |
| --- | --- |
| 更新器签名校验 | 已启动（036） |
| 插件身份 / 升级 / 故障 / 图标数据层 | 已实现（037，业务层） |
| 插件 ABI + 库化动态加载 | 已实现（038） |
| 倒序卸载 / 失败回滚 / scope 归零 | 已实现（039） |
| 批量请求构造（http 类型层） | 已实现（040） |
| 窗口句柄契约（raw-window-handle 类型层） | **已实现（041）** |
| wry / tao / slint 三条 UI 宿主 | **判不成立**（大闭包 + Win7 WebView2 终止支持） |
| sentry / sentry-native / minidump 崩溃分析 | **判不成立**（CMake + C++17 + Win10 以下未自动测试） |
| 真实窗口 / WebView / 渲染 / 崩溃捕获 | 未启动（L1–L12 见 ui-preconditions.md） |
| 子进程插件隔离、插件 init | 未启动（039） |
| 界面渲染 | 仍等 UX 手感确认与 Q-041 拍板 |
''')

app('docs/rules/ui-demo.md', '''## 041 闸门判定

本轮只更新关于页许可表数据（19 → 20 组，计数 41 → 42）并重渲 4 张许可相关截图，不改任何界面布局、控件或交互；`src/core/window.rs` 是 core 类型层，不创建窗口、不渲染、不加载 WebView。沿用 036 / 038 / 039 / 040 的先例判**未触发**。其余 52 张 PNG 回退到 HEAD。
''')

app('docs/checklists/ai-errors.md', '''## 041 轮新增

| 编号 | 防错项 |
| --- | --- |
| A120 | 引 UI 宿主或崩溃分析前先拉真实 manifest 与官方平台支持页，核平台分支、C/系统库、MSRV、edition 与 Win7 运行时口径。 |
| A121 | 官方写「最后支持版本 / 不再支持 / 未自动测试」时，不能写成「编出来应该能跑」；须把取舍摆给用户。 |
| A122 | 用项目自有类型前先读它的真实方法名（本轮 `Envelope` 是 `field()` 不是 `get()`），不凭印象调。 |
| A123 | 仓库路径要实核，组织改名后旧路径会 404；取不到就标受阻，不猜来源。 |
| A124 | 裁 vendor manifest 时，optional 依赖与引用它的 feature 行要一起裁，否则目录源解析失败。 |
| A125 | unsafe trait（`HasWindowHandle`）要求句柄真实有效；core 层没有窗口时不实现、不伪造。 |
| A126 | 句柄类型层不得推导 WebView2 可用性；可用性由宿主注入的 probe 负责，两者独立。 |
''')

app('docs/records/interface-log.md', '''## 041 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I49 | `src/core/window` | 新增 `HostSurface` / `headless` / `win32` / `has_window` / `has_display` / `platform` / `display_kind` / `display_handle` / `envelope` |
| I50 | `src/lightweight/view` | 新增 `LightweightView::host_surface()`，恒 headless |
| I51 | `tests/window_handle_contract.rs` | 6 个集成测试 |
| S40 | 状态 | U41–U48 已证实；Q-041 三选项待拍板；真实窗口 / WebView / 崩溃分析未启动；Q-037-01 仍挂 |
''')

app('docs/records/rounds.md', '''## 041

| 落点 | 内容 |
| --- | --- |
| docs/spec/41-round-041-instructions.txt | 逐字副本 1 行 |
| docs/decisions/041-ui-crash-stack-check-and-window-handle.md | F21-F28、U41-U48、V-A~V-F、E57-E61、四值 |
| docs/verification/round-041.md | 18 条复跑证据 |
| docs/records/q041-win7-ui.md | Q-041 三选项，待拍板 |
| docs/features/window-handle-contract.md | F041-01 五字段登记 |
| docs/rules/ui-preconditions.md | L1-L12 前置清单 |
| docs/research/24-ui-host-win7-and-crash-stack.md | 13 个锚点 / 四值 |
| src/core/window.rs + core/mod.rs + lightweight/view.rs | 157 行类型层 + 2 个入口，8 + 2 个单测 |
| tests/window_handle_contract.rs | 6 个集成测试 |
| vendor/ + Cargo.toml/lock | raw-window-handle 0.6.2，21 包 20 第三方 |
| docs/licenses/ + 关于页 + NOTICES | 3 份全文、20 组、计数 42、N38-N40 |
| demos/round-041-window-handle.html | 13 步运行逻辑演示 |
| 索引与记录 | docs/index 205 项、README、四个 index、ai-errors A120-A126、code-ownership-audit、implementation-strategy、ui-demo 判定、interface-log、rounds |

「干」按 040 结尾把两条上层路线一起核完。**先摆一条硬矛盾**：你 011 定的是 Win7 起兼容，Microsoft 官方写明 Edge 109 / WebView2 Runtime 109 是最后支持 Win7 / 8.1 的版本、SDK ≥1.0.1519.0 不再支持、109 之后无安全更新、Fixed >109 在 Win7 上无法启动，Learn 支持列表只剩 Win10 1709+ / Win11 / Server 2016+。而 `wry` 的 Windows 分支用 `webview2-com 0.38` + `windows 0.61`，属于新 SDK 线。所以**「Win7 + 正常模式 WebView2 界面」在官方口径下不成立**，三个选项写进 `q041-win7-ui.md`，本轮不替你选。

**真实 manifest 核查**：`wry 0.53.5`（MSRV 1.77，Windows 分支 webview2-com + windows 0.61，Linux 分支 webkit2gtk/gtk/soup3，macOS 分支 objc2 系列，Android 分支 jni/ndk）、`tao 0.34.5`（MSRV 1.74，libc + windows 0.61 + gtk + objc2 + dlopen2）、`slint 1.18.1`（**edition 2024** + 一堆 workspace 依赖 + wgpu/skia/femtovg）；崩溃分析侧 `sentry 0.49.5`（默认链含 reqwest/rustls/native-tls/tokio/sentry-minidump）、`sentry-native`（CMake + C++17 + MSVC2022 + zlib + Crashpad/Breakpad，Windows 低于 Win10「应支持但未自动测试」）、`minidump` / `minidump-writer`（十几项依赖 + libc/nix）。两条路线全部判**不成立**，按 035 / 040 的规矩改轨，没偷偷塞依赖。

**改轨落地**：`raw-window-handle 0.6.2` 是 wry / tao / slint 三家共用的零依赖 no_std 类型层，MSRV 1.64、MIT OR Apache-2.0 OR Zlib。`src/core/window.rs` 157 行：`HostSurface` 只描述有没有窗口、哪种平台句柄，变体分类与 `DisplayHandle::windows()` 全交给库；**不实现 unsafe 的 `HasWindowHandle`**，也不从句柄推导 WebView2 可用性（那仍由 `WebView2Probe` 注入）。`LightweightView::host_surface()` 恒 headless，把「轻量模式不加载 UI 宿主」变成库类型的可测事实。`Cargo.lock` 20 → 21 包 / 20 第三方，关于页 19 → 20 组、计数 41 → 42，3 份 LICENSE 全文 + NOTICES N38–N40。

**验证**：237 单元 / 0 + 6 窗口契约 / 0 + 7 http_construct / 0 + 7 lifecycle / 0（43.18 s）+ 6 abi / 0（111.95 s）= **263 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。界面闸门**未触发**：只更新关于页许可表数据并重渲 4 张许可截图，其余 52 张 PNG 回退到 HEAD。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E57 | `Envelope` 没有 `get()`，9 处测试报 E0599 | 按真实 API 改 `field()` |
| E58 | vendor manifest 的 `wasm-bindgen-0-2` feature 引用被裁掉的 optional 依赖 | 连同 wasm target 段、dev-dependencies、docs.rs metadata 一起裁，N38 登记 |
| E59 | `tauri-rs/tao`、`tauri-rs/wry`、`rust-minidump/minidump`、`rust-windowing/dpi` 全 404 | 改 `tauri-apps/tao` 等；`dpi 0.1` 两次 404 标受阻，不猜来源 |
| E60 | 全量 `cargo test` 又一次网关 502 | 拆段跑通，未降断言 |
| E61 | 039 / 040 结尾两个候选没定优先级 | 两条都核完，明确「都不成立」与「只落句柄类型层」 |

028 三项开服器功能仍按「只记文档」零实现；Q-037-01 未答复、继续挂；CF F17、特殊版代码、本项目 LICENSE、后端仓写请求均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '199. docs/verification/round-040.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''199. docs/verification/round-040.md
200. docs/spec/41-round-041-instructions.txt
201. docs/decisions/041-ui-crash-stack-check-and-window-handle.md
202. docs/features/window-handle-contract.md
203. docs/rules/ui-preconditions.md
204. demos/round-041-window-handle.html
205. docs/verification/round-041.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-040.md; do printf',
                  'docs/verification/round-040.md docs/spec/41-round-041-instructions.txt docs/decisions/041-ui-crash-stack-check-and-window-handle.md docs/features/window-handle-contract.md docs/rules/ui-preconditions.md demos/round-041-window-handle.html docs/verification/round-041.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 041 |', p.read_text(), count=1)
section = '''

## 041 UI 宿主与崩溃分析核查，改轨窗口句柄类型层

先摆一条硬矛盾：Microsoft 官方写明 Edge 109 / WebView2 Runtime 109 是最后支持 Win7 / 8.1 的版本，SDK ≥1.0.1519.0 不再支持 Win7，109 之后无安全更新；Learn 的 WebView2 列表只剩 Win10 1709+ / Win11 / Server 2016+。而 `wry` 的 Windows 分支用 `webview2-com 0.38` + `windows 0.61`。所以「Win7 + 正常模式 WebView2 界面」在官方口径下不成立，三个选项写在 `docs/records/q041-win7-ui.md`，本轮不替用户选。

真实 manifest 核完 `wry 0.53.5` / `tao 0.34.5` / `slint 1.18.1`（edition 2024）与 `sentry 0.49.5` / `sentry-native`（CMake + C++17 + MSVC2022，Win10 以下未自动测试）/ `minidump` 闭包，两条上层路线都判不成立。改轨落 `raw-window-handle 0.6.2`：零依赖 no_std 类型层，MSRV 1.64，三家 UI 宿主共用。`src/core/window.rs` 157 行把句柄变体分类交给库，不实现 unsafe 的 `HasWindowHandle`，不从句柄推导 WebView2 可用性；轻量模式 `host_surface()` 恒 headless。`Cargo.lock` 21 包 / 20 第三方，关于页 20 组 / 42。

`cargo test --offline` 合计 **263/0**（237 单元 + 26 集成），Windows GNU 交叉检查通过。界面与 56 张 PNG 只动了 4 张许可截图。
'''
if '## 041 UI 宿主与崩溃分析核查' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

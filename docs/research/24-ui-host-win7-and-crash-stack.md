# UI 宿主与崩溃分析真实闭包、Win7 WebView2 一手资料（041）

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

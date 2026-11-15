# 插件隔离边界与卸载约束（039）

| 项 | 值 |
| --- | --- |
| 当前形态 | 同进程 C ABI 动态库（`libloading`），只做符号读取与版本协商 |
| 宿主进程执行的插件代码 | **无**。`kcu_plugin_init` 不调用 |
| 崩溃隔离 | **未启动**。设置页「插件单独运行，不影响启动器」是演示项 |
| 原因 | `extern "C"` 边界上 Rust panic 会安全 abort 整个进程；`catch_unwind` 不抓 abort，与 foreign exception 交互是 UB |
| 允许展开的 ABI | 只有 `"C-unwind"`；本项目契约是 `"C"`，不换 |
| Symbol 生命周期 | 由 `libloading` 的 `PhantomData<&'lib Library>` 保证；不存进长期结构体、不 `into_raw` |
| 释放次序 | 符号使用 → scope join → 倒序 `Library::close()` |
| close 语义 | `close()` 返回错误；Drop 静默忽略；musl `dlclose` 可能是 no-op、macOS TLS 阻碍卸载。close 成功不等于已卸载 |
| 禁用做法 | `Box::leak` / `mem::forget` 换 `'static`（会失去卸载能力）；先卸库再读符号；把 close 失败当成功 |
| 子进程路线（未启动） | `std::process::Command`：参数不经 shell、显式 `wait` 或 `kill`、`Child` 的 Drop 不回收、避开 `.bat` / `.cmd`、统一信封回传 |
| 版本前置 | Windows 参数编码安全需 MSRV ≥ 1.81.0（CVE-2024-24576 / 43402）；与 Win7 Tier 3 + build-std 的冲突未证实 |
| 未证实 | 真实 `.dll` 加载、MSVC 目标、Win7 运行时、macOS / musl 卸载实测 |

一手来源与推理：`docs/research/22-ffi-unwind-and-library-lifecycle.md`、`docs/decisions/039-plugin-lifecycle-and-isolation.md` F07–F12。

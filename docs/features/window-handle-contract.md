# F041-01 宿主窗口句柄契约

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `HostSurface` 持有 `Option<RawWindowHandle>` 与 `Option<RawDisplayHandle>`；`headless()` 两者皆空，`win32(NonZeroIsize)` 由 `Win32WindowHandle::new` 与 `WindowsDisplayHandle::new` 构造；`platform()` / `display_kind()` 对库枚举变体做只读分类，`display_handle()` 只在 Windows 变体走库提供的安全构造 `DisplayHandle::windows()`；`envelope()` 输出平台与两个布尔量。 |
| 开放了什么 | `src/core/window.rs`：`HostSurface` / `headless` / `win32` / `has_window` / `has_display` / `platform` / `display_kind` / `display_handle` / `envelope`；`src/lightweight/view.rs` 新增 `LightweightView::host_surface()`。 |
| 登记框架 | 依赖 `raw-window-handle 0.6.2`（MIT OR Apache-2.0 OR Zlib / no_std / 零依赖）；是 wry、tao、slint 三家共用的互操作类型层，不动 038 的 libloading、027 的 crossbeam、040 的 http 任何一层。 |
| 用户使用逻辑 | 轻量模式与无头模式明确「没有窗口」，不会偷偷起 WebView；将来正常模式由宿主注入真实句柄时，平台分类与显示句柄构造都由库完成，启动器不会因为自己写错句柄结构而崩；界面卡住或插件想抢句柄时，契约里没有「渲染器已就绪」这种可被误读的字段。 |
| 性能 | 纯值类型，无分配大头、无线程、无 IO、无 unsafe；`platform()` 只是一次枚举匹配。 |

状态：句柄类型层已实现；真实窗口创建、WebView 加载、渲染、崩溃分析未启动。

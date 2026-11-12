# 轻量极简视图状态

| 项 | 值 |
| --- | --- |
| 编号 | F016-04 |
| 状态 | 已实现、已验证 |
| 轮次 | 016 |
| 框架 | lightweight.view |

## 怎么运作

`LightweightView` 持有单主题 Theme::Single、ViewState（Idle / Loading / Ready / Failed / Locked）、选中登录方式、回退阶段、注入式 `WebView2Probe`、日志开关、有界 LogBuffer、core.popup 注册表、诊断行、游戏进程与启动器存活标记、动作计数。`handle(ViewAction, &CancelToken)` 对 9 类动作全部返回 ViewEvent 并写单行诊断；`flow` 串起选登录 → 开始 → 文件面板 → 日志 → 装加载器 → 启动游戏 → 注册弹窗 → 取消，最后 `close_all_popups()` 保证 0 残留。`launch_game` 置 `game_running=true`、`launcher_alive=false`。`EXCLUDED` 固定 13 项排除清单，断言不复用 normal.ui 资产。整页界面演示在 `demos/ui-full-lightweight.html`，实现未进入构建。

## 开放了什么

| 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- |
| `LightweightView::{new,excluded_assets,has_dual_theme,has_embedded_file_manager,footprint_label}` | 无 | Self / &'static [&str] / bool / &str | 无 |
| `handle`、`flow` | ViewAction / AuthKind / CancelToken | ViewEvent / Vec<ViewEvent> | 不 panic |
| `open_popups_for_state`、`close_all_popups` | ViewState / 无 | () / usize | 无 |
| `envelope` | 无 | Envelope（theme / state / game_running / launcher_alive / popups_open / footprint） | 无 |
| `WebView2Probe::{injected,unknown,external_available}` | bool / 无 | Self / bool | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | lightweight.view（B05；007 D03-D06；016 L10-L14） |
| 模块路径 | src/lightweight/view.rs |
| 依赖 | core.asynk / diagnostics / envelope / log / popup；lightweight.login / loaders |
| 约束 | 单主题实现、不加载 normal.ui、无内嵌文件管理器、游戏运行期无常驻进程、模式判定仍在 dispatcher |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 低配首次开机 | dispatcher 选轻量 | 极简单主题视图，不加载重资产 |
| 点任意控件 | 9 类动作 | 都有响应与诊断行 |
| 点文件管理 | 系统面板 | 无内嵌管理器 |
| 点启动游戏 | 拉起进程 | 启动器退出，后台无常驻 |
| 弹窗出现 | 11 类全注册 | 按钮 / ESC / 取消 / 确认 / 宿主可关，流程后 0 残留 |
| 按手感调演示 | 改 ui-full-lightweight.html | 先改演示，确认后才改实现 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | LogBuffer 每 100 行分片，250 行输入后 pending ≤ 100；进程级内存剖析未实测 |
| 启动耗时 | 11 项测试含在全量 0.12s 内 |
| 常驻进程 | 游戏运行期无 |
| 退出条件 | handle 返回 / reset |
| 测量命令 | `cargo test --offline lightweight::view`（11 passed） |
| 浏览器内点击、真实 WebView2、内存剖析 | 受阻 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `view_uses_single_theme`、`excluded_assets_cover_normal_ui_and_heavy_components` | 单主题 / 13 项 | 已证实 |
| `game_runtime_has_no_resident_launcher` | launcher_alive=false | 已证实 |
| `every_catalog_popup_closes_and_none_remain`、`flow_ends_with_zero_open_popups` | 0 残留 | 已证实 |
| `all_view_actions_are_responded_to`、`cancelled_flow_records_failure_without_crashing` | 9 类 / 不崩 | 已证实 |
| `webview2_availability_is_injected_not_hardcoded`、`log_is_bounded_by_shards` | 注入 / 有界 | 已证实 |
| 整页演示浏览器渲染实测 | 未执行 | 受阻 |

# 轻量登录与三级回退

| 项 | 值 |
| --- | --- |
| 编号 | F016-01 |
| 状态 | 已实现、已验证 |
| 轮次 | 016 |
| 框架 | lightweight.login / E01 |

## 怎么运作

`LoginSession::new(AuthKind, premium_allowed)` 初始化：离线直接 Done；网页登录从 ExternalBrowser 起。`advance(&StageAvailability, &CancelToken, pair_code)` 按固定链推进：外置可用→完成；不可用→EmbeddedBrowser（2 级降级）；内置不可用→PairCode（2 级降级，写入连接码）；连接码未确认→300s 超时落 0 级；全耗尽→0 级零级报错。Mojang 且无既有凭据时直接禁正版，第三方不受影响。每步写单行诊断并生成带 request_id 的响应信封。CancelToken 在入口与轮询中检查。

## 开放了什么

| 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- |
| `AuthKind::{code,needs_browser}` | 无 | &str / bool | 无 |
| `LoginSession::new` | AuthKind, bool | Self | 无 |
| `LoginSession::advance` | StageAvailability, CancelToken, &str | Result<LoginStage,LoginError> | Cancelled / Timeout / ZeroLevel |
| `LoginStage::code`、`Fallback::code` | 无 | &str | 无 |
| 常量 `PAIR_CODE_TIMEOUT` | 无 | 300s | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | lightweight.login（B05；E01 auth） |
| 模块路径 | src/lightweight/login.rs |
| 依赖 | core.asynk / diagnostics / envelope；dispatcher.mode.Fallback |
| 约束 | 不写死 WebView2 检测键；可用性由宿主注入；不自行切换模式（007 C08） |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 选离线 | 免浏览器 | 直接完成，低端机零 WebView 负担 |
| 选正版 / 第三方、外置可用 | 系统浏览器登录 | 完成，无降级提示 |
| 外置失败 | 自动切内置 | 提示已切换 |
| 内置失败 | 显示连接码 | 手机登录，300s 可取消 |
| 全部失败 | 零级报错 | 明确修复提示，不崩溃不静默 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 固定大小结构 + 诊断行向量，无堆增长循环 |
| 启动耗时 | 8 项测试含在全量 0.12s 内 |
| 常驻进程 | 无 |
| 退出条件 | advance 返回；取消 / 超时 / 完成 |
| 测量命令 | `cargo test --offline lightweight::login`（8 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `offline_login_needs_no_browser`、`external_browser_succeeds_without_fallback` | Done / 3 级 | 已证实 |
| `first_fallback_goes_to_embedded_browser`、`second_fallback_shows_pair_code` | 2 级 / 连接码 | 已证实 |
| `pair_code_timeout_is_zero_level_error` | Timeout / 0 级 | 已证实 |
| `premium_disabled_disables_mojang_but_not_third_party` | 禁正版 | 已证实 |
| `cancelled_token_stops_login`、`diagnostics_are_single_line_kcu_prefixed` | Cancelled / 单行 | 已证实 |

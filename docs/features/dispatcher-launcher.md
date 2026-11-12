# 统一调度主流程 Dispatcher

| 项 | 值 |
| --- | --- |
| 编号 | F015-04 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 015 |

## 怎么运作

`dispatch(&DispatchInput, &CancelToken)` 全程同步、不 panic。顺序：入口查取消 → 解析 config/launch.json → 逐条解析任务文本并走 core.cache 单飞 → TaskSet 排序去重 → `pick` 合并命令行 → 双击服务器调 core.instance 按权重选实例（用户指定排第一）→ ModeSelector → 正版凭据闸门 → UI 分流 → 弹窗注册与全关闭 → 失败计数（成功清零）→ 连续 3 次进安全模式 → 安全模式仍失败导出 4 行诊断包 → 统一信封与 `[KCU]` 单行诊断。非法模式报错后清掉覆盖值再跑一次，用内置默认继续。headless 无凭据、内存读数拿不到、实例不兼容分别落 1 级、2 级、1 级，均不中断启动。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `Dispatcher::{new,default}` | 函数 | capacity | Self | 0 容量由 core.cache 拒绝 |
| `Dispatcher::dispatch` | 函数 | &DispatchInput, &CancelToken | LaunchOutcome | 错误进信封与诊断，不 panic |
| `Dispatcher::{reset,flush_diagnostics}` | 函数 | 无 | () / Vec<Vec<String>> | 无 |
| `DispatchInput` | 结构 | 任务文本、配置文本、参数、内存、实例、权重等 | 输入集合 | 无 |
| `LaunchOutcome` | 结构 | 无 | mode / task / instance / diagnostics 等 | 无 |
| 常量 | 值 | `FAILURE_THRESHOLD=3`、`DEFAULT_CACHE_CAPACITY=16`、`DEFAULT_CACHE_TTL=30s` | 无 | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | dispatcher.launcher（005-blueprint.md B04；003-remote.md D07 第 2 层） |
| 模块路径 | src/dispatcher/launcher.rs |
| 扩展点 | 无；E04 ui 仅 normal 模式加载 |
| 依赖 | core.envelope / diagnostics / popup / instance / log / cache / asynk / leak |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 双击服务器 | `--server` + 实例列表 | 按权重选兼容实例 | 用户指定版本排第一 |
| 单参数进服 | `--server <地址>` 无服务器条目 | 直接进服 | 跳过实例选择页 |
| 不兼容指定版本 | 用户选了服务端不支持的版本 | 记诊断 | 不崩、不静默 |
| 坏 config / 坏任务 | json 非法 | 报错并跳过该条 | 其余流程继续 |
| 反复启动失败 | 3 次连续失败 | 安全模式 + 内置默认 | 仍失败导出诊断包 |
| 用户取消 | CancelToken 已取消 | 入口返回 | 0 解析、0 副作用 |
| 无头无凭据 | .kcul 且无既有正版文件 | 禁用正版 | 提示可见 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 任务缓存默认 16 条，capacity=4 跑 40 个不同任务后 len/order ≤ 4；inflight=0 |
| 启动耗时 | 20 项测试含在全量 0.11s 内；同一任务文本 10 次 dispatch 解析次数 1 |
| 常驻进程 | 无；dispatch 返回即结束 |
| 退出条件 | dispatch 返回 / cancel / reset |
| 泄漏 | outcome 经 Tracker 跟踪 drop 后 live=0；LogBuffer 每 100 行分片；cache.inflight 用 Weak |
| 测量命令 | `cargo test --offline dispatcher::launcher`（20 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `low_memory_first_run_dispatches_lightweight_without_ui` | lightweight、0 弹窗 | 已证实 |
| `normal_mode_registers_and_closes_every_popup` | popups_open=0 | 已证实 |
| `user_choice_ranks_first_over_habit_weight` | 用户指定实例 a | 已证实 |
| `consecutive_failures_enter_safe_mode_then_export_bundle` | 4 行诊断包 | 已证实 |
| `repeated_task_text_is_parsed_once`、`cache_stays_bounded_over_many_tasks` | 1 次 / ≤4 | 已证实 |
| `cancelled_token_stops_before_any_work` | 0 解析 | 已证实 |
| `outcomes_do_not_leave_live_tracked_objects` | live=0 | 已证实 |
| 进程级内存剖析、GUI 点击端到端 | 未执行 | 受阻 |

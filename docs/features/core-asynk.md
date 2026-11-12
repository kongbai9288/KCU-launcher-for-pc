# 异步任务与多源竞速 asynk

| 项 | 值 |
| --- | --- |
| 编号 | F014-02 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 014 |

## 怎么运作

`CancelToken` 是 `Arc<AtomicBool>`，clone 共享同一标志。`TaskGroup::spawn` 起 std 线程，进入时活跃计数 +1，线程持 `LiveGuard`，退出时计数 -1；`shutdown` 先 cancel 再逐个 join，`Drop` 兜底 join 全部未回收 handle。`race(loaders, timeout)` 为每个源起线程，通过 `mpsc::channel` 送首个结果；收到结果或超时后 cancel 全部，逐个 join，返回 `RaceResult { index, value, live_after_join }`；无结果返回 `RaceError::TimedOut`。loader 执行期间不持锁。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `CancelToken::{new,cancel,is_cancelled}` | 函数 | 无 | Self / () / bool | 无 |
| `TaskGroup::{new,spawn,cancel_token,cancel,live,shutdown}` | 函数 | FnOnce(CancelToken) | usize | 无 |
| `race` | 函数 | IntoIterator<FnOnce>, Duration | Result<RaceResult<T>,RaceError> | `TimedOut` |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.asynk（B03、014 D05、D06、011 第 30 条） |
| 模块路径 | src/core/asynk.rs |
| 扩展点 | E02 download 多源同时下载；E05 automation 定时任务取消 |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 一个模组多源下载 | 多个镜像可用 | 首个源完成 | 其余源请求关闭 |
| 关窗口 / 退出 | 后台任务在跑 | `shutdown` | 任务取消并回收 |
| 定时任务失败重试 | 用户设了编排 | clone token | 可随时取消 |
| 录制 / 截屏开关 | 用户关掉开关 | cancel | 后台线程退出 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 每任务一个线程 + 一个 channel；活跃计数在 join 后归零，`race` 实测 `live_after_join=0` |
| 启动耗时 | 3 源竞速实测首个结果返回即取消其余，非等待全部完成 |
| 常驻进程 | 无；`TaskGroup::drop` 兜底 join |
| 退出条件 | cancel + join |
| 测量命令 | `cargo test --offline core::asynk`（6 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline core::asynk` | 6 passed | 已证实 |
| `race_returns_first_and_cancels_other_sources` | index=0、value=11、live=0 | 已证实 |
| `drop_joins_without_explicit_shutdown` | 4 个任务全部执行完 | 已证实 |
| `race_timeout_reports_error_and_releases_threads` | `TimedOut` | 已证实 |
| `shutdown_joins_every_handle` | joined=5、live=0 | 已证实 |

## 边界

本层用 std 线程与 channel，未引入 async runtime；真实网络请求的取消需要上层在 loader 内轮询 `is_cancelled()`，本层只提供令牌与回收语义。

# 统一信封 Envelope

| 项 | 值 |
| --- | --- |
| 编号 | F013-01 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 013 |

## 怎么运作

`Envelope::new(kind, target)` 用进程内原子计数生成 `kcu-` 前缀 request_id；`payload` 为 `BTreeMap<String,String>`，键序稳定；`with` 插入字段，`with_error` 置 error 且 `ok()` 转 false。空 target 不拦截，由调用方校验。无 I/O、无异步、无超时。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `Envelope::new` | 函数 | Kind, &str | Envelope | 无 |
| `with` / `with_error` / `field` / `ok` | 函数 | &str | Self / Option<&str> / bool | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.envelope（B03、K01） |
| 模块路径 | src/core/envelope.rs |
| 扩展点 | 无，core 不注册扩展 |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 调度器发起任务 | 无 | 构造 request | 拿到唯一 request_id |
| 下游回报 | 有 request | 构造 response / event | 同一链路可追踪 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 每实例一个 BTreeMap，无实测进程级数值，标未实测 |
| 启动耗时 | 无独立启动；`cargo test` 全量 0.00s |
| 常驻进程 | 无 |
| 退出条件 | 值析构 |
| 测量命令 | `cargo test --offline core::envelope`；release rlib 442456 字节 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline core::envelope` | 3 passed | 已证实 |
| `cargo build --release --offline` | Finished | 已证实 |

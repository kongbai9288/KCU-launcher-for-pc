# 诊断行 Diagnostics

| 项 | 值 |
| --- | --- |
| 编号 | F013-02 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 013 |

## 怎么运作

`diag_line(domain, action, target, result, detail)` 按固定 5 段拼单行字符串：`[KCU] <域> <动作> <目标> <结果> <详情>`。不换行、不做转义、不写 I/O；含换行字符的输入由调用方负责净化。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `diag_line` | 函数 | 5 × &str | String | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.diagnostics（K03） |
| 模块路径 | src/core/diagnostics.rs |
| 扩展点 | 无 |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 诊断包导出 | 故障发生 | 逐行输出 | 单行可 grep 的 `[KCU]` 记录 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 一次分配，未实测进程级数值 |
| 启动耗时 | 无 |
| 常驻进程 | 无 |
| 退出条件 | 返回即结束 |
| 测量命令 | `cargo test --offline core::diagnostics` |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline core::diagnostics` | 2 passed | 已证实 |

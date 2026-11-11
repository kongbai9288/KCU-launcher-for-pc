# 用户操作模拟 simulate

| 项 | 值 |
| --- | --- |
| 编号 | F013-09 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 013 |

## 怎么运作

`simulate(server, instances, habit, args, user_choice)` 按固定序列跑一次用户旅程：启动 → 隐私政策弹出并同意 → 声明页 → 注册全部弹窗 → 逐类关闭并校验无残留 → 分支（单参数直达服务器 / 双击服务器选实例）→ 状态持久化 → 完成。每步压入 `Step`，错误进 `FlowReport.errors`，`ok()` 要求 errors 空、弹窗全关、末步为 FlowDone。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `simulate` | 函数 | &ServerEntry, &[Instance], &[VersionWeight], &LaunchArgs, Option<&str> | FlowReport | errors 向量 |
| `FlowReport::ok` | 函数 | 无 | bool | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.userflow（B04、013 H01/H02/H04/H05/H06） |
| 模块路径 | src/core/userflow.rs |
| 扩展点 | 无 |
| 依赖 | std only（复用 core 内 5 个模块） |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 普通启动 | 无 | 同意隐私 → 双击服务器 | 自动进符合版本实例 |
| 用户指定版本 | 用户设置 | 双击服务器 | 用户版本排第一 |
| 命令行单参数 | `--server` | 跳过选择 | 直接进服 |
| 任意路径结束 | 无 | 校验弹窗 | 无残留、无孤儿状态 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 一次流程 11 弹窗 + 步骤向量，未实测进程级数值 |
| 启动耗时 | 纯内存，`cargo test` 全量 0.00s |
| 常驻进程 | 无 |
| 退出条件 | FlowDone |
| 测量命令 | `cargo test --offline core::userflow`（5 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline` 全量 | 37 passed / 0 failed | 已证实 |
| `no_popup_is_left_open_after_any_path` | 3 条路径均 open_count=0 | 已证实 |
| `single_arg_bypasses_selection_and_joins_server` | 直达分支命中 | 已证实 |

## 边界

本层是内存级操作模拟，不是浏览器 / GUI 自动化；真实窗口渲染、WebView2、点击派发未实测，标受阻。用户 013 H01 要求「验证用户正常的操作逻辑」，本层提供可复跑的模拟入口，UI 层接入后须再跑一次端到端。

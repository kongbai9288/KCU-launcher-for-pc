# 功能登记索引

每实现一个功能写一份 md，字段固定为：怎么运作、开放了什么、登记框架、用户使用逻辑、性能。模板见 _template.md。

| 编号 | 功能 | 框架 | 状态 | 文件 |
| --- | --- | --- | --- | --- |
| F001 | 正常模式 UI 设计稿 | normal.ui | 已批准 | normal-ui.md |

F001 状态含义：设计稿已获确认并逐字落盘；未实现、未进入构建。轻量模式排除见 docs/decisions/007-normal-ui.md。

## 计划登记项

| 功能 | 框架归属 |
| --- | --- |
| 统一调度器 | dispatcher |
| 正常启动器 | normal |
| 正常模式 UI | normal.ui |
| 轻量启动器视图 | lightweight.view |
| 无头模式启动器 | headless |
| 手机连接 | normal.lan |
| 一键开服 | normal.server |
| 日志 | core.log |
| 兜底与安全模式 | core.fallback |
| 跨进程统一信封 | core.ipc |

状态值：已批准 / 已实现 / 已验证 / 已合并 / 已进入构建 / 已部署 / 行为已确认。每份功能 md 只声明实际达到的一层。

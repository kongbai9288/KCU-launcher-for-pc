# 功能登记索引

每实现一个功能写一份 md，字段固定为：怎么运作、开放了什么、登记框架、用户使用逻辑、性能。模板见 _template.md。

| 编号 | 功能 | 框架 | 状态 | 文件 |
| --- | --- | --- | --- | --- |
| F001 | 正常模式 UI 设计稿 | normal.ui | 已批准 | normal-ui.md |
| F002 | 统一调度器 | dispatcher | 已批准 | dispatcher.md |
| F003 | 轻量启动器视图 | lightweight.view | 已批准 | lightweight.md |
| F004 | 无头模式启动器 | headless | 已批准 | headless.md |

F001 状态含义：设计稿已获确认并逐字落盘；未实现、未进入构建。轻量模式排除见 docs/decisions/007-normal-ui.md。
F002-F004 状态含义：需求条目已登记；未实现、未进入构建，src/ 为空。

## 计划登记项

| 功能 | 框架归属 |
| --- | --- |
| 正常启动器 | normal |
| 手机连接 | normal.lan |
| 一键开服 | normal.server |
| 日志 | core.log |
| 兜底与安全模式 | core.fallback |
| 跨进程统一信封 | core.ipc |
| UI 框架 | normal.ui |

状态值：已批准 / 已实现 / 已验证 / 已合并 / 已进入构建 / 已部署 / 行为已确认。每份功能 md 只声明实际达到的一层。

## 登记约束

| 编号 | 约束 |
| --- | --- |
| G01 | 状态只声明实际达到的一层，不合并表述。 |
| G02 | 性能未实测时写「未实测」并标受阻，不写推测值。 |
| G03 | 轻量模式 md 不引用 normal.ui 资产，见 docs/checklists/ai-errors.md A26。 |
| G04 | 未证实字段不写进实现，见 docs/research/index.md R03。 |

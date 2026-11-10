# 功能登记索引

每实现一个功能写一份 md，字段固定为：怎么运作、开放了什么、登记框架、用户使用逻辑、性能。模板见 _template.md。

| 编号 | 功能 | 框架 | 状态 | 文件 |
| --- | --- | --- | --- | --- |
| F001 | 正常模式 UI 设计稿 | normal.ui | 已批准 | normal-ui.md |
| F002 | 统一调度器 | dispatcher | 已批准 | dispatcher.md |
| F003 | 轻量启动器视图 | lightweight.view | 已批准 | lightweight.md |
| F004 | 无头模式启动器 | headless | 已批准 | headless.md |
| F005 | 正常启动器 | normal | 已批准 | normal-launcher.md |
| F006 | 手机连接 | normal.lan | 已批准 | lan.md |
| F007 | 一键开服 | normal.server | 已批准 | server.md |
| F008 | 日志 | core.log | 已批准 | log.md |
| F009 | 兜底与安全模式 | core.fallback | 已批准 | fallback.md |
| F010 | 跨进程统一信封 | core.ipc | 已批准 | envelope.md |
| F011 | UI 框架 | normal.ui | 已批准 | ui-framework.md |
| F012 | 正版凭据保护 | core.credential | 已批准 | credential-guard.md |

F001 状态含义：设计稿已获确认并逐字落盘；未实现、未进入构建。轻量模式排除见 docs/decisions/007-normal-ui.md。
F002-F012 状态含义：需求条目已登记；未实现、未进入构建，src/ 为空。
F012 具体保护方案未批准，见 docs/rules/build-preconditions.md L4。

## 011 轮功能输入

| 项 | 值 |
| --- | --- |
| 逐字原文 | docs/spec/11-features-input.txt，268 行，17096 字节 |
| 编号功能 | 1-55 连续，见 docs/features/backlog.md |
| 文件管理清单 | 174 个条目，分组索引见 backlog.md |
| 状态 | 全部已登记 / 未实现 / 未进入构建 |
| 单份功能 md | 每实现一个功能时按 _template.md 单独写一份 |

## 计划登记项

| 状态 | 值 |
| --- | --- |
| 待登记 | 无 |

009 轮曾登记「需求第 6、9、17、18、20、21 节功能块已全部登记」，010 轮核查发现 docs/spec/00-requirements.txt:17 的凭据保护机制未单独成文，已补 F012。docs/spec/00-requirements.txt:228 的玩家分支可取之处保留为调研候选项，不登记为实现项，见 docs/research/12-compliance.md。

## 登记约束

| 编号 | 约束 |
| --- | --- |
| G01 | 状态只声明实际达到的一层，不合并表述。 |
| G02 | 性能未实测时写「未实测」并标受阻，不写推测值。 |
| G03 | 轻量模式 md 不引用 normal.ui 资产，见 docs/checklists/ai-errors.md A26。 |
| G04 | 未证实字段不写进实现，见 docs/research/index.md R03。 |
| G05 | 12 份功能 md 均写明未实现与 src/ 为空，不写入构建状态。 |
| G06 | F012 方案未批准前，F004 不进入 D07 L4 搭建，见 docs/rules/build-preconditions.md。 |
| G07 | backlog.md 的 55 条编号与 174 个文件管理条目不写成已实现；单份功能 md 在实现时才生成。 |

状态值：已批准 / 已实现 / 已验证 / 已合并 / 已进入构建 / 已部署 / 行为已确认。每份功能 md 只声明实际达到的一层。

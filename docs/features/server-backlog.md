# 第 012 轮开服器功能输入登记表

轮次：012
逐字原文：docs/spec/12-server-features-input.txt（64 行，4970 字节，SHA-1 `75a387e1c91b244aa0710bd0ef722c1cf4a2f242`）
状态：全部为「已登记 / 未实现 / 未进入构建」，`src/` 为空
单份功能 md：每实现一个功能时按 docs/features/_template.md 单独写一份，字段固定为怎么运作、开放了什么、登记框架、用户使用逻辑、性能。本表是输入索引。

## 输入结构事实

| 项 | 值 | 四值 |
| --- | --- | --- |
| 首行 | `开服器1.先检查有没有可以直接使用的java`，编号 1 与标题连写 | 已证实 |
| 带点号编号 | 2-24、27，共 23 行 | 已证实 |
| 无点号编号 | `25多实例同时运行的资源配额/调度`，编号 25 与文字连写 | 已证实 |
| 缺号 | 26 | 已证实 |
| 重复编号 | 24 后挂第一组 `·` 条目，25 后挂第二组 `·` 条目，两处均为分节起点 | 已证实 |
| `·` 字符计数 | 35 | 已证实 |
| 独立 `·` 条目行 | 34 | 已证实 |
| 同行首项 | 第 24 条引导句末尾同一行含首个 `·` 条目 | 已证实 |
| 编号功能总数 | 27（含首行连写的 1 与无点号的 25），其中缺 26 | 已证实 |

计数口径与 011 轮同型：`·` 字符 35，独立行 34，差 1 为引导句同行首项。逐字文本以 docs/spec/12-server-features-input.txt 为准，本表不抄写逐项文字。

## 编号功能

| 编号 | 名称 | 框架候选 | 状态 |
| --- | --- | --- | --- |
| 1 | 检查可直接使用的 Java | server.java.detect | 已登记 / 未实现 |
| 2 | 自动下载 jar，进入加载器选择页，可选原版或多个加载器；Java 不可用走镜像，境外用官方源 | server.loader.select | 已登记 / 未实现 |
| 3 | mod 与插件：直连 Modrinth 或复用 CurseForge 同类 API，声明要服务器 mod；插件服官方下载通道 | server.content | 已登记 / 未实现 |
| 4 | AI 自动管理服务器，开放 API 给本地或本地容器 AI 当工具，不给删除权限，需用户手动同意 | server.ai.api | 已登记 / 未实现 |
| 5 | 快捷命令，输入 `/` 弹出候选，输出不带 `/`，中文显示，用户手动选择「原版增强」 | server.command.quick | 已登记 / 未实现 |
| 6 | 快速标注，颜色区分 mod 名称 | server.mod.tag | 已登记 / 未实现 |
| 7 | 手动同意 EULA，可打开官网页面 | server.eula | 已登记 / 未实现 |
| 8 | 模组更新，同模组高版本 jar 自动禁用低版本，仅单实例页可用 | server.mod.update | 已登记 / 未实现 |
| 9 | FTP / SFTP，自动连接，允许访问互联网上的服 | server.remote.ftp | 已登记 / 未实现 |
| 10 | op 锁定，发现未选中的 op 变更自动移出 | server.op.lock | 已登记 / 未实现 |
| 11 | 详细开服文档：绑定域名、管理、更新 | server.docs | 已登记 / 未实现 |
| 12 | 关机需点击关机实例；关窗口需先保存进度 | server.lifecycle | 已登记 / 未实现 |
| 13 | 自动化增量备份，支持选定路径 | server.backup | 已登记 / 未实现 |
| 14 | 快速显示种子号，使用 nbt 能力 | server.world.seed | 已登记 / 未实现 |
| 15 | 实例未关闭时改世界/模组/插件文件夹被锁，提示数据丢失、地形错乱且无法恢复，5 秒后才能继续；单次访问只弹一次，退出重进再弹 | server.fileguard | 已登记 / 未实现 |
| 16 | 快捷输入，快速聊天时自动前置 say 或 talk | server.chat.quick | 已登记 / 未实现 |
| 17 | 定时任务：自动重启、自动开机、自动发命令 | server.scheduler | 已登记 / 未实现 |
| 18 | 成就快速分析、快速管理玩家，需 MC 版本支持 | server.player | 已登记 / 未实现 |
| 19 | 功能锁定与命令黑名单，用于访客模式 | server.guest | 已登记 / 未实现 |
| 20 | 快速导出日志 | server.log.export | 已登记 / 未实现 |
| 21 | RCON 安全通道、看门狗、崩溃自动归因、模组依赖预检、配置快照、TPS/MSPT 仪表盘、玩家概览、审计日志、种子/敏感信息权限提示 | server.ops | 已登记 / 未实现 |
| 22 | 配置 JVM 容量 | server.jvm | 已登记 / 未实现 |
| 23 | 服务端默认配置汉化、快速选择、多实例同步 | server.config.i18n | 已登记 / 未实现 |
| 24 | 第一组分节，下挂 `·` 条目组 A | server.ops.ext | 已登记 / 未实现 |
| 25 | 多实例同时运行的资源配额/调度；下挂 `·` 条目组 B | server.quota | 已登记 / 未实现 |
| 26 | 缺号 | — | 已证实 |
| 27 | PNG 快速设置服务器 logo，自动调整像素 | server.icon | 已登记 / 未实现 |

## 分节 `·` 条目组

组 A（第 24 条后）与组 B（第 25 条后）共 34 个独立条目行，逐字文本见 docs/spec/12-server-features-input.txt。分组索引：

| 组 | 内容 | 框架候选 |
| --- | --- | --- |
| GA1 | Java 多版本管理（下载、切换、按 MC 版本自动推荐） | server.java |
| GA2 | 端口冲突检测 + UPnP 自动映射 | server.network |
| GA3 | 进程守护 / 崩溃自动重启、看门狗 + 崩溃自动归因 | server.watchdog |
| GA4 | 备份保留策略 + 磁盘空间预警、备份完整性校验 + 恢复预览 | server.backup |
| GA5 | 配置快照与回滚（server.properties、ops.json、模组配置等） | server.config.snapshot |
| GA6 | 配置文件可视化编辑 + Schema 校验 | server.config.editor |
| GA7 | 整合包导入导出（mrpack / CurseForge zip）、拖拽安装模组/插件 | server.modpack |
| GA8 | 模组依赖与冲突预检（启动前） | server.mod.deps |
| GA9 | Hangar / Ore 插件源接入 | server.content.plugin |
| GA10 | 服务端/加载器版本回滚、实例模板与克隆、实例导出/导入、远程实例本地化管理 | server.instance |
| GA11 | AI 请求「待确认中心」+ 操作审计、外部文件修改监听与冲突提示 | server.ai.confirm |
| GA12 | RCON 安全通道（仅本地/隧道） | server.rcon |
| GA13 | 日志实时高亮 + 过滤 + 一键上传 mclo.gs | server.log |
| GA14 | 实例分组/标签/搜索、状态卡片截图分享 | server.ui |
| GA15 | 玩家数据概览（在线时长、峰值时段、留存、成就分布） | server.player.stats |
| GA16 | 种子查看的权限提示/访客隐藏 | server.world.seed |
| GA17 | 按需启动 / 空闲休眠 | server.lifecycle |
| GA18 | 定时任务的可视化编排与失败重试 | server.scheduler |
| GB1 | 模组包 lockfile / 版本锁定 | server.mod.lock |
| GB2 | 世界管理：预生成区块、删除维度、切换世界类型 | server.world |
| GB3 | 代理端（Velocity/BungeeCord）配置向导 | server.proxy |
| GB4 | 云备份目标（WebDAV / S3） | server.backup.cloud |
| GB5 | 玩家白名单/封禁批量导入导出 | server.player.list |
| GB6 | 服务器图标 / MOTD 可视化编辑 | server.icon |
| GB7 | 下载源测速与镜像切换、跨实例共享模组缓存 | server.download |
| GB8 | 定时任务的依赖链与失败重试 | server.scheduler |

分组为索引，不逐组计数。

## 与 011 轮输入的重复项

011 轮逐字输入见 docs/spec/11-features-input.txt，登记见 docs/features/backlog.md。重复项按 011 轮 U04「模组尽量去重聚合」列出，不改写任一方的逐字副本。

| 012 条目 | 011 条目 | 关系 |
| --- | --- | --- |
| 13 自动化增量备份 | 44 备份，轻备份只配置，自动化全量加差异压缩包 | 重叠，粒度不同 |
| 17 定时任务 | 22 自动下线/关机/上线/加入服务器 | 重叠，012 增加命令与编排 |
| 20 快速导出日志 | 20 日志系统，每 100 条压缩到一个压缩包 | 重叠，012 增加导出 |
| 21 模组依赖预检、配置快照、TPS/MSPT、审计日志 | 2 模组依赖检测与一键安装；39 思维导图看依赖 | 部分重叠 |
| 21 RCON 安全通道 | 需求 :7 一键开服及 docs/research/06-server.md RCON 一手原文 | 既有一手资料 |
| 22 配置 JVM 容量 | 45 JVM 内存自动分配、回收器选择、模组内存智能分析 | 重叠 |
| 24 整合包导入导出 mrpack | 15 整合包一键安装，拖到主界面 | 重叠 |
| 24 拖拽安装模组/插件 | 15 拖到主界面；011 开头段拖放安装页 | 重叠 |
| 24 实例导出/导入 | 25 版本功能迁移、键盘与服务器文件 | 部分重叠 |
| 24 按需启动/空闲休眠 | 22 自动上线/自动下线 | 重叠 |
| 24 定时任务编排与失败重试 | 22、17 | 重叠 |
| 27 服务器图标 | 011 开头段图标单文件入口 | 部分重叠 |
| 3 插件源 Hangar / Ore | 011 第 46 条 CopperGolemLauncher 插件 | 不同层，不合并 |

重复项合并口径未拍板，见 docs/records/open-questions.md Q-D 组。

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cmp /data/inputs/开服器1.txt docs/spec/12-server-features-input.txt` | exit 0 | 已证实 |
| `sha1sum` 双端 | `75a387e1c91b244aa0710bd0ef722c1cf4a2f242` | 已证实 |
| 带点号编号计数 | 23 行，2-24 与 27 | 已证实 |
| `·` 字符 / 独立行 | 35 / 34 | 已证实 |
| `git ls-files src/` | 输出为空 | 已证实 |
| 浏览器渲染与 Rust 构建实测 | 未执行 | 受阻 |

## 028 轮新增输入

| 编号 | 原文 | 登记 |
| --- | --- | --- |
| S028-01 | 玩家上线提醒 | F028-01 / server-join-alert.md |
| S028-02 | 饼图分析活跃度 | F028-02 / server-activity-pie.md |
| S028-03 | 自动命令支持把服务器出现的命令文字作为触发条件 | F028-03 / server-auto-command-log-trigger.md |

用户标注「只记文档」：三项零实现、零构建、`src/server` 不存在。一手资料见 `docs/research/20-server-log-events.md`，待拍板 Q-028-01 / Q-028-02 记在 F028-03。与 012 台账重复项判定：S028-01 与「22 自动上线/自动下线」不同层（提醒 vs 启停），不合并；S028-02 与「21 TPS/MSPT」不同层（玩家活跃 vs 性能），不合并；S028-03 是 012「17 自动命令」的触发源扩展，按扩展登记不另立功能。

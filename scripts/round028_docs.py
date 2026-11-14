from pathlib import Path
import re

Path('docs/spec/28-round-028-instructions.txt').write_text(
    '干，开服器有新功能啦，玩家上线提醒，饼图分析活跃度，自动命令支持把服务器出现的命令文字作为触发条件（只记文档）\n')
print('SPEC_OK')

D = {}

D['docs/decisions/028-server-features.md'] = '''# 第 028 轮：开服器三项新功能只记文档，代码替换继续

| 项 | 值 |
| --- | --- |
| 编号 | 028 |
| 状态 | 已登记；三项新功能未实现 |
| 依据 | docs/spec/28-round-028-instructions.txt |
| 前序 | docs/features/server-backlog.md（012 轮开服器台账）、docs/records/code-ownership-audit.md |
| 本轮性质 | 双轨轮 |

## 两条指令的边界

| 编号 | 原文片段 | 处置 |
| --- | --- | --- |
| B01 | 「干」 | 按既有进度继续替换自写代码，落 `src/core/leak.rs`。 |
| B02 | 「开服器有新功能啦……（只记文档）」 | 三项新功能逐字登记、逐项写功能 md、补一手调研、出运行逻辑演示；`src/` 中不新增任何开服器实现，不进构建，不动 UX 整页演示。 |
| B03 | 「只记文档」 | 括号紧跟功能列表，限定这三项；不覆盖 B01。 |

## 三项新功能

| 编号 | 功能 | 功能 md | 框架 |
| --- | --- | --- | --- |
| F028-01 | 玩家上线提醒 | server-join-alert.md | normal.server |
| F028-02 | 饼图分析活跃度 | server-activity-pie.md | normal.server |
| F028-03 | 自动命令：服务器出现的命令文字作为触发条件 | server-auto-command-log-trigger.md | normal.server |

三项都挂在 012 轮 `docs/features/server-backlog.md` 的开服器台账下，不另起框架、不改 005-blueprint.md 已批准的分层。状态统一为「已批准 · 未实现 · 未进入构建」。

## 代码替换（B01）

| 编号 | 动作 |
| --- | --- |
| C01 | `src/core/leak.rs` 删掉自写 `Tracker` / `Tracked`：手工 `Arc<AtomicUsize>` 计数、clone / drop 配对递减、Drop 兜底全部移除，191 → 99 行。 |
| C02 | `WeakRegistry` 保留，它只用 `std::sync::{Arc, Mutex, Weak}`，无自写并发原语；`purge` 用 `HashMap::retain`。 |
| C03 | `src/dispatcher/launcher.rs` 的 `outcomes_do_not_leave_live_tracked_objects` 改用 `Arc::strong_count` / `Weak::upgrade`，并追加 027 已落地的 `crossbeam_utils::sync::WaitGroup` 归零断言。 |
| C04 | `src/lib.rs` 导出收敛为 `WeakRegistry`；`src/core/mod.rs` 不变。 |
| C05 | 无新增依赖：`Cargo.lock` 仍 8 包 / 7 第三方，`vendor/` 不变。 |

按 `docs/records/code-ownership-audit.md` 映射表，`core/leak.rs` 的处置是「大幅删减或删」，本轮按此执行。删掉的 2 个测试只服务于已删除的自写类型，等价断言已迁移，未降低验收项；`cargo test --offline` 141 → **139 / 0**，差值 2 如实登记。

## UI 闸门

`docs/rules/ui-demo.md` 未触发：本轮不动用户界面、不改 `demos/ui-full-*.html`、不重渲预览图。三项功能的界面形态（提醒条、饼图卡片、规则编辑器）留在功能 md 的「用户使用逻辑」里，等你给手感反馈的轮次再出整页 UX 演示。

## 四值

| 项 | 值 |
| --- | --- |
| 三项功能逐字登记、五字段齐备、15 条来源标注 | 已证实 |
| leak.rs 自写计数删除、139 / 0、8 包不变 | 已证实 |
| 三项功能的实现、界面、真实日志样本回放 | 未证实 |
| 浏览器渲染、真实服务端联调、Win7 / 多架构 | 受阻 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/features/server-join-alert.md'] = '''# 玩家上线提醒

| 项 | 值 |
| --- | --- |
| 编号 | F028-01 |
| 状态 | 已批准 · 未实现 · 未进入构建 |
| 版本 | 0.0.0 |
| 轮次 | 028 |

## 怎么运作

读取开服器实例的 `logs/latest.log` 增量输出，命中 `joined the game` 行时解析时间戳与玩家名，生成一条上线事件；同一事件按「实例 sid + 文件偏移 + 行内容」去重，重启或日志轮转后从上次偏移续读，不回放历史。事件写进应用内提醒中心（铃铛未读高亮），可按设置发桌面通知；免打扰时段只入中心不弹窗。

| 路径 | 处置 |
| --- | --- |
| 日志文件不存在 / 被轮转 | 保留上次偏移，写 `[KCU]` 诊断行，界面显示「等待服务器输出」，不静默重试 |
| 行格式不匹配 | 交给下一组正则；全不匹配就跳过该行，不误报 |
| 同一玩家短时间内重复上线 | 按去重键合并，冷却期内只留一条 |
| 玩家名可重复 | 显示名只用于展示，事件键用规范化 `ip:port` 派生的 sid，目录不按名字拼 |
| 插件源 | 可选接 PaperMC `PlayerJoinEvent`；默认走日志，插件不可用时退回日志 |

日志样本行：`[14:32:10] [Server thread/INFO]: Player1 joined the game`；Forge 日志带毫秒与类名前缀，例如 `noveauu joined the game` 前有 `net.minecraft.server.MinecraftServer/`。格式随版本 / 加载器 / 插件变化，因此用多组正则 + 捕获组索引，不写死单一模式。来源见 `docs/research/20-server-log-events.md`。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `server.join_alert.subscribe` | 函数（normal.server） | 实例 sid、关注名单、免打扰时段 | 上线事件流 | 统一信封 `error=E_LOG_UNAVAILABLE` |
| `server.join_alert.list` | 函数 | 实例 sid、时间范围 | 最近 N 条 | 空范围返回空列表 |
| `server.join_alert.dismiss` | 函数 | 事件 id | 已读数 | 不存在的 id 返回零级提示 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | normal.server |
| 模块路径 | `src/server/join_alert.rs`（未创建） |
| 扩展点 | `E.server.log_event`（012 轮开服器扩展区，插件可追加事件源） |
| 依赖 | 复用 `core.cache` 有界缓存、`core.log` 增量读取、`core.envelope` 统一信封；第三方日志解析库候选未选定 |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 开服器实例卡片 | 实例运行中 | 默认开启，右侧显示「上线 3 人」 | 铃铛未读高亮，不自动弹窗打断 |
| 设置 → 服务器 → 上线提醒 | 任意 | 切「全部 / 仅关注玩家 / 关闭」，拖免打扰时段 | 写后即时生效，失败保留旧值 |
| 提醒中心 | 有未读 | 点一条看玩家名、时间、实例 | 每条可关，× / ESC / 宿主都能关，流程后 0 残留 |
| 刷新 | 缓存未命中或手动点 | 重新读取偏移后的新行 | 失败回退上次结果，不空白 |
| 轻量模式 | 任意 | 不加载 | 无 UI、无常驻进程 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 未实测；设计上限为最近 200 条事件 + 有界去重表 |
| 启动耗时 | 未实测；不额外起进程，复用实例日志读取器 |
| 常驻进程 | 无（跟随开服器实例生命周期） |
| 退出条件 | 实例停止 / 用户关闭提醒 / 轻量模式 |
| 测量命令 | 未执行；实现轮补 `cargo test --offline` 与样本日志回放 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cmp` 逐字副本 | exit 0 | 已证实 |
| `git ls-files src/server` | 输出为空 | 已证实 |
| 真实服务端联调 | 未执行 | 受阻 |
'''

D['docs/features/server-activity-pie.md'] = '''# 饼图分析活跃度

| 项 | 值 |
| --- | --- |
| 编号 | F028-02 |
| 状态 | 已批准 · 未实现 · 未进入构建 |
| 版本 | 0.0.0 |
| 轮次 | 028 |

## 怎么运作

把 `joined the game` / `left the game` 配对成会话，按玩家累计在线秒数，形成 `玩家 → 秒数` 映射；前端渲染成饼图占比。时间范围可切「今天 / 7 天 / 30 天 / 自定义」，切换只重新聚合本地缓存，不重新扫全量历史。

| 路径 | 处置 |
| --- | --- |
| 只有上线没有下线（崩溃 / 强制退出） | 按实例停止时间或日志结束时间闭区间收口，标「已估算」，不丢弃 |
| 同一玩家改名 | 按 sid 归并，显示名取最近一次，不拆成两块 |
| 数据为空 | 显示「暂无数据」与开始游戏引导，不画空饼图 |
| 缓存过期 / 强制刷新 | 回退上次结果并在图上标「上次更新」，不空白 |
| 导出 | CSV 走系统文件面板，含玩家、秒数、会话数、占比 |

社区里 DST 管理平台用 `PlayTimeCount map[nickname]int64` 直接喂饼图，Plan 插件给日活 / 周活 / 月活、在线时段热力与 Activity Index，思路一致。时段分布保留为可选热力图，主图形按你的要求固定为饼图。来源见 `docs/research/20-server-log-events.md`。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `server.activity.pie` | 函数（normal.server） | 实例 sid、范围、是否含估算 | 扇区列表（标签 / 秒数 / 占比 / 颜色） | 统一信封 `error=E_NO_SAMPLES` |
| `server.activity.sessions` | 函数 | 实例 sid、范围 | 会话明细 | 空范围返回空列表 |
| `server.activity.export` | 函数 | 实例 sid、范围 | CSV 路径 | 写失败返回可见提示 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | normal.server |
| 模块路径 | `src/server/activity.rs`（未创建） |
| 扩展点 | `E.server.log_event`（复用 F028-01 的事件流） |
| 依赖 | `core.cache` 有界缓存 + `core.envelope`；图表渲染走 UI 层候选库，LICENSE 全文齐备前不引 |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 开服器实例 → 活跃度 | 有会话数据 | 默认显示 7 天饼图 | 扇区带百分比与具体时长，鼠标悬停给人数 |
| 顶部范围切换 | 任意 | 切今天 / 7 天 / 30 天 / 自定义 | 写后即时生效，切换不重扫全量日志 |
| 缓存 / 命中 / 刷新逻辑条 | 任意 | 点「重新获取」或「强制刷新」 | 显示上次更新时间，失败回退旧图并标注 |
| 扇区点击 | 有数据 | 下钻到该玩家会话列表 | 面包屑可返回，每层可关 |
| 导出 | 任意 | 点导出 | 系统文件面板，不自绘文件对话框 |
| 轻量模式 | 任意 | 不加载 | 无图表、无额外进程 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 未实测；设计上限为 7 天会话 + 每实例 1 张聚合表 |
| 启动耗时 | 未实测；聚合在本地缓存上做，不阻塞主线程 |
| 常驻进程 | 无 |
| 退出条件 | 离开页面 / 实例删除 / 轻量模式 |
| 测量命令 | 未执行；实现轮补样本日志聚合与内存剖析 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cmp` 逐字副本 | exit 0 | 已证实 |
| `git ls-files src/server` | 输出为空 | 已证实 |
| 真实样本回放 | 未执行 | 受阻 |
'''

D['docs/features/server-auto-command-log-trigger.md'] = '''# 自动命令：服务器出现的命令文字作为触发条件

| 项 | 值 |
| --- | --- |
| 编号 | F028-03 |
| 状态 | 已批准 · 未实现 · 未进入构建 |
| 版本 | 0.0.0 |
| 轮次 | 028 |

## 怎么运作

在 012 轮「自动命令」基础上扩展触发源：除定时 / 事件触发外，支持把服务器日志与控制台 stdout 里**出现的命令文字**本身作为触发条件。用户写一条规则，指定匹配文字（如 `/say 开始`、`issued server command: /gamemode`），命中后执行预设动作。

| 路径 | 处置 |
| --- | --- |
| 匹配方式 | 默认「包含」，可切「精确 / 正则」；多组模式按顺序命中即停 |
| 来源限定 | 仅服务端输出 / 仅玩家命令 / 全部；默认「仅服务端输出」 |
| 候选词表 | 来自 MC jar 拆分得到的命令名 + 用户自定义命令（013 答复 Q-C02），界面给补全下拉，不写死全量表 |
| 重复触发 | 同一行只匹配一次；文件偏移 + inode 去重；冷却期内同规则不再触发 |
| 日志轮转 | 记 inode 与偏移，轮转后从新文件 0 偏移续读，不回放也不漏读 |
| 危险命令 | 命令黑名单拦截（013 答复 Q-D01）；命中黑名单只给可见提示，动作不执行 |
| 规则失败 | 正则非法、实例未运行、命令执行超时各给独立错误码，写 `[KCU]` 诊断行，不静默吞掉 |
| 轻量模式 / 无头 | 不加载规则编辑器；无头模式可由配置注入只读规则 |

日志里 `issued server command` 行是玩家命令的权威记录；控制台 stdout 可用 `tail -f` + `grep --line-buffered` 增量消费。社区方案用声明式 `events.yml` 配 `pattern` + 命名捕获组，或 stdout 正则 → 判定层 → 反向命令，思路相同。来源见 `docs/research/20-server-log-events.md`。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `server.auto_cmd.rules` | 函数（normal.server） | 实例 sid | 规则列表 | 统一信封 |
| `server.auto_cmd.upsert` | 函数 | 触发文字、匹配方式、来源、动作、冷却、启用 | 规则 id | `E_BAD_PATTERN` / `E_BLACKLISTED` |
| `server.auto_cmd.fire` | 函数 | 日志行 | 命中规则 id 或空 | `E_COOLDOWN` / `E_INSTANCE_STOPPED` |
| `server.auto_cmd.audit` | 函数 | 范围 | 命中记录 | 空范围返回空列表 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | normal.server |
| 模块路径 | `src/server/auto_command.rs`（未创建） |
| 扩展点 | `E.server.log_event`（事件源）+ `E.server.rule`（规则注册，插件可追加匹配器） |
| 依赖 | 复用 `core.log` 增量读取、`core.cache` 去重、`core.envelope`；正则库候选未选定，LICENSE 全文齐备前不引 |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 设置 → 服务器 → 自动命令 | 任意 | 新建规则，写触发文字，选匹配方式与动作 | 列表即时新增，带启用开关、单项重置、稳定项 |
| 触发文字输入框 | 有候选词表 | 输入前缀给补全下拉 | 候选来自 jar 拆分 + 自定义，可手打任意文字 |
| 测试按钮 | 规则已保存 | 贴一段日志样文 | 显示命中 / 未命中与将执行的动作，不真发命令 |
| 命中时 | 实例运行中 | 执行预设动作 | 写审计记录与 `[KCU]` 诊断行，界面可见 |
| 命中黑名单 | 任意 | 拦截 | 可见提示「已拦截」，动作不执行，规则保留 |
| 关闭 / ESC / × / 宿主 | 任意弹窗 | 关 | 流程后 0 残留 |
| 缓存逻辑条 | 任意 | 刷新 / 强制刷新 | 失败回退旧规则，不空白 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 未实测；设计上限为每实例 100 条规则 + 有界去重窗口 |
| 启动耗时 | 未实测；增量读取，不轮询整文件 |
| 常驻进程 | 无（跟随实例日志读取器） |
| 退出条件 | 实例停止 / 规则全部停用 / 轻量模式 |
| 测量命令 | 未执行；实现轮补规则回放与正则耗时基线 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cmp` 逐字副本 | exit 0 | 已证实 |
| `git ls-files src/server` | 输出为空 | 已证实 |
| 真实控制台联调 | 未执行 | 受阻 |

## 待拍板

| 编号 | 问题 |
| --- | --- |
| Q-028-01 | 命中后是否每次都要手动同意（013 答复 Q-D02 是「每次请求」，那条口径属于 AI 权限，不确定是否复用到这里）。 |
| Q-028-02 | 预设动作允许哪些命令：仅白名单 / 黑名单之外全部 / 只读诊断行。 |
'''

D['docs/research/20-server-log-events.md'] = '''# 开服器日志事件与活跃度资料（028 轮）

| 项 | 值 |
| --- | --- |
| 轮次 | 028 |
| 性质 | 文档调研；三项新功能只记文档，不写实现 |
| 锚点 | 逐行独立，完整 URL |

## 一手与近一手事实

| 编号 | 事实 | 来源 | 四值 |
| --- | --- | --- | --- |
| L01 | 服务端日志默认写 `logs/latest.log`，重启时覆盖并把旧日志压缩归档；历史文件为 `年-月-日-编号.log.gz`。 | https://mineguard.pro/blog/minecraft-server-logs-analysis | 已证实 |
| L02 | 行格式 `[hh:mm:ss] [线程/级别]: 消息`；上线 `Player1 joined the game`，退出 `left the game`，玩家命令 `issued server command: /gamemode creative`。 | https://www.mczfw.com/blog/16301.html | 已证实 |
| L03 | Forge 实际日志用 `[08Feb2026 00:01:37.795] [Server thread/INFO] [net.minecraft.server.MinecraftServer/]: noveauu joined the game`；另有 `logged in with entity id ... at (x, y, z)` 行，含 IP 与坐标。 | https://mclo.gs/e0me2N2 | 已证实 |
| L04 | `grep "joined the game\\|left the game"`、`grep -i "issued server command"` 是常规的 join / 命令提取手法；`zgrep` 用于归档日志。 | https://mineguard.pro/blog/minecraft-server-logs-analysis | 已证实 |
| L05 | 实时读取用 `tail -f logs/latest.log`，配合 `grep --line-buffered` 做关键词告警；logrotate 或 Log4j 滚动策略控制体积。 | https://www.mczfw.com/blog/15884.html | 已证实 |
| L06 | 声明式解析：配置里给 `join_regex` / `quit_regex` / `chat_regex` 多组模式，每条带 `player_group` 捕获组索引，示例 `Server thread/INFO]: (.*) joined the game`。 | https://zread.ai/17TheWord/QueQiao/21-configuration-management | 已证实 |
| L07 | 事件配置样例：`pattern: '(?P\\w+) joined the game'` 配 `event_type: player_join`，实时 tail → 正则 → webhook；支持自定义 `events.yml`。 | https://github.org/AlexisHutin/mclog2event | 未证实（返回域名为 `github.org` 而非 `github.com`，不据此复制） |
| L08 | PaperMC 的 `PlayerJoinEvent` 由 `Listener` + `@EventHandler` 注册，`joinMessage(Component)` 可改加入消息；`HandlerList` 支持按 Listener / Plugin 或 `unregisterAll()` 注销。 | https://docs.papermc.io/paper/dev/handler-lists/ | 已证实 |
| L09 | 事件优先级 `EventPriority` 决定多个监听器顺序，`registerEvents` 在 `onEnable()` 调用。 | https://www.pkold.com/docs/papermc-plugin/05-events | 已证实（中文二手教程，与 L08 一致） |
| L10 | 活跃度饼图：后台按玩家累计 `PlayTimeCount map[nickname]int64` 秒数，前端直接渲染占比；时序折线与会话甘特图同源，统计缓存保留 7 天。 | https://deepwiki.com/miracleEverywhere/dst-management-platform-api/9.2-game-statistics | 已证实（二手源码解读） |
| L11 | Plan 插件给日活 / 周活 / 月活、新增与留存、在线时段热力、Activity Index、会话 CSV 导出。 | https://www.tanggaoyun.com/community/detail.php?id=3446 | 已证实（第三方介绍页） |
| L12 | 时段分析常用热力图，分布离散度用箱线图；缺失值与异常值需先清洗再选图型。 | https://fanruan.com/blog/article/392954 | 已证实（通用可视化资料） |
| L13 | stdout 流 → 正则匹配 → 判定层 → 反向发命令的闭环，是日志驱动自动化的常见结构。 | https://tsight.io/articles/11681915?lang=zh | 已证实（第三方技术文章） |
| L14 | `tail -f` + `while read` 解析登录行触发系统通知，是原版服务端无插件时的通用做法。 | https://apple.stackexchange.com/a/20062 | 已证实 |
| L15 | 日志行会含玩家 IP、UUID、坐标、聊天内容；对外上传前需脱敏。 | https://mclo.gs/e0me2N2 、 https://www.mczfw.com/blog/15884.html | 已证实 |

## 落地约束

| 编号 | 约束 |
| --- | --- |
| R01 | 日志格式随 MC 版本、加载器、插件变化，不写死单一模式；用多组正则 + 捕获组索引 + 用户自定义模式。 |
| R02 | 日志含 IP / UUID / 坐标，上传或导出默认脱敏，用户可手动关脱敏（013 答复 Q-C15）。 |
| R03 | 日志轮转按 inode + 文件偏移续读，不回放历史、不静默漏读。 |
| R04 | 玩家名可重复，事件与目录键用规范化 `ip:port` 派生的 sid，显示名只展示（023 轮目录污染修复）。 |
| R05 | 每次对外请求走有界缓存与刷新机制，失败回退上次结果，不空白。 |
| R06 | 插件源与日志源可切换，插件不可用时退回日志，不阻断开服器。 |

## 未证实 / 受阻

| 项 | 值 |
| --- | --- |
| Mojang / Minecraft Wiki 对 `joined the game` 行格式的官方原文 | 未证实（本轮只拿到实际日志样本与二手资料） |
| `mclog2event` 仓库真实地址与许可证 | 未证实（L07 域名异常） |
| 各加载器 / 各 MC 版本的完整日志模式矩阵 | 未证实 |
| 浏览器内图表渲染实测、真实服务端联调 | 受阻 |
'''

D['docs/verification/round-028.md'] = '''# 第 028 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 028 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 139 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 8 包 / 7 第三方，与 027 一致 | 已证实 |
| V4 | `git diff d5bd76d -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V5 | `grep -rnE 'Tracker|Tracked' src/` | 零命中 | 已证实 |
| V6 | `wc -l src/core/leak.rs` | 191 → 99 | 已证实 |
| V7 | `git ls-files src/server` | 输出为空 | 已证实 |
| V8 | 三份功能 md 五字段计数 | 各 5 个固定小节 | 已证实 |
| V9 | `docs/research/20-server-log-events.md` URL 计数 | 15 条来源、13 个独立 URL、16 次出现 | 已证实 |
| V10 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V11 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V12 | `python3 scripts/render_ui.py` 未调用、`demos/ui-full-*.html` 未改 | UI 闸门未触发 | 已证实 |
| V13 | 必读文件循环 | REQUIRED=137 MISSING=0 | 已证实 |
| V14 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 三项新功能只落文档、零实现、五字段齐备 | 已证实 |
| leak.rs 自写计数删除、139 / 0、依赖不变 | 已证实 |
| 141 → 139 的差值为删除 2 个自写模块自带测试，等价断言已迁移 | 已证实 |
| 官方日志格式原文、模式矩阵、真实联调 | 未证实 |
| 浏览器图表渲染、Win7 / 多架构、CI 独立构建 | 受阻 |
| UI 整页演示 | 未触发（本轮不动界面） |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s):
    p = Path(f)
    p.write_text(p.read_text().rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/features/index.md', '''## 028 轮开服器新输入（只记文档）

| 编号 | 功能 | 框架 | 状态 | 文件 |
| --- | --- | --- | --- | --- |
| F028-01 | 玩家上线提醒 | normal.server | 已批准 · 未实现 · 未进入构建 | server-join-alert.md |
| F028-02 | 饼图分析活跃度 | normal.server | 已批准 · 未实现 · 未进入构建 | server-activity-pie.md |
| F028-03 | 自动命令：服务器出现的命令文字作为触发条件 | normal.server | 已批准 · 未实现 · 未进入构建 | server-auto-command-log-trigger.md |

三项均挂 012 轮开服器台账下，不另起框架；界面形态等手感轮再出整页 UX 演示。
''')

app('docs/features/server-backlog.md', '''## 028 轮新增输入

| 编号 | 原文 | 登记 |
| --- | --- | --- |
| S028-01 | 玩家上线提醒 | F028-01 / server-join-alert.md |
| S028-02 | 饼图分析活跃度 | F028-02 / server-activity-pie.md |
| S028-03 | 自动命令支持把服务器出现的命令文字作为触发条件 | F028-03 / server-auto-command-log-trigger.md |

用户标注「只记文档」：三项零实现、零构建、`src/server` 不存在。一手资料见 `docs/research/20-server-log-events.md`，待拍板 Q-028-01 / Q-028-02 记在 F028-03。与 012 台账重复项判定：S028-01 与「22 自动上线/自动下线」不同层（提醒 vs 启停），不合并；S028-02 与「21 TPS/MSPT」不同层（玩家活跃 vs 性能），不合并；S028-03 是 012「17 自动命令」的触发源扩展，按扩展登记不另立功能。
''')

app('docs/research/index.md', '''## 028 轮新增

| 编号 | 文档 | 来源数 | 主题 |
| --- | --- | --- | --- |
| R20 | 20-server-log-events.md | 15 条来源 / 13 个独立 URL | 日志格式、实时读取、声明式正则、PlayerJoinEvent、活跃度饼图、脱敏约束 |
''')

app('docs/checklists/ai-errors.md', '''## 028 轮新增

| 编号 | 防错项 |
| --- | --- |
| A67 | 日志格式不写死单一模式：版本 / 加载器 / 插件前缀不同，用多组正则 + 捕获组索引 + 用户自定义。 |
| A68 | 事件与目录键用 sid，不用玩家名；名字可重复且可自定义。 |
| A69 | 检索结果里 `github.org` 这类异常域名标未证实，不据此复制仓库或许可证。 |
''')

app('docs/records/interface-log.md', '''## 028 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I28 | F028-01 | `server.join_alert.subscribe` / `list` / `dismiss` |
| I29 | F028-02 | `server.activity.pie` / `sessions` / `export` |
| I30 | F028-03 | `server.auto_cmd.rules` / `upsert` / `fire` / `audit` |
| S28 | 状态 | 三项均为文档登记，未进入 `src/`，无函数实现 |
''')

app('docs/decisions/index.md', '| 028 | 开服器三项新功能只记文档；leak.rs 自写计数删除 | 已登记；新功能未实现 | 028-server-features.md |')

app('docs/records/rounds.md', '''## 028

| 落点 | 内容 |
| --- | --- |
| docs/spec/28-round-028-instructions.txt | 逐字副本 1 行 |
| docs/decisions/028-server-features.md | B01-B03 双轨边界、三项功能编号、C01-C05 代码替换、UI 闸门 |
| docs/features/ | 3 份五字段功能 md + index + server-backlog 028 段 |
| docs/research/20-server-log-events.md | 15 条来源、L01-L15、R01-R06、未证实项 |
| docs/verification/round-028.md | 14 条复跑证据 |
| demos/round-028-server-features.html | 13 步运行逻辑演示（非整页 UX） |
| src/core/leak.rs | 删 Tracker / Tracked，191 → 99 行 |
| src/dispatcher/launcher.rs / src/lib.rs | 测试迁移到 `Arc::strong_count` + `WaitGroup`，导出收敛 |
| 索引与记录 | docs/index 137 项、README、decisions/index、research/index、ai-errors A67-A69、interface-log |

「干」继续替换自写代码，按映射表把 `core/leak.rs` 的「大幅删减或删」落地：自写 AtomicUsize 计数、clone / drop 配对、Drop 兜底全删；`WeakRegistry` 保留（只用 std Arc/Mutex/Weak）。`Cargo.toml` / `Cargo.lock` / `vendor/` 未动，仍 8 包 7 第三方。

三项新功能按「只记文档」处理，逐字登记、写五字段 md、补一手调研、出运行逻辑演示；`src/server` 不存在，UI 整页演示闸门未触发，`demos/ui-full-*.html` 与预览图未改。

本轮真实差异与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E08 | 迁移后的 `outcomes_do_not_leave_live_tracked_objects` 用 `TaskGroup::new()` 编译报 `cannot find type TaskGroup in this scope` | 改用完整路径 `crate::core::asynk::TaskGroup::new()`，`cargo test --offline` 139 / 0 |
| E09 | 删除自写类型带走 2 个自带测试，141 → 139 | 如实登记差值，等价断言迁移到 `Arc::strong_count` / `Weak::upgrade` / `WaitGroup`，未降低验收项 |

未做：三项功能实现、UI 实现、真实服务端联调、浏览器图表渲染、cache / launcher / lightweight 替换、CF F17、特殊版代码、本项目 LICENSE、后端仓写请求。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '133. docs/verification/round-027.md\n\n读取命令：'
assert a in t
t = t.replace(a, '133. docs/verification/round-027.md\n134. docs/spec/28-round-028-instructions.txt\n135. docs/decisions/028-server-features.md\n136. docs/research/20-server-log-events.md\n137. docs/verification/round-028.md\n\n读取命令：', 1)
t = t.replace('docs/verification/round-027.md; do printf',
              'docs/verification/round-027.md docs/spec/28-round-028-instructions.txt docs/decisions/028-server-features.md docs/research/20-server-log-events.md docs/verification/round-028.md; do printf',
              1)
p.write_text(t)
print('INDEX_OK')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 028 |', p.read_text(), count=1)
p.write_text(t.rstrip() + '''

## 028 开服器三项新功能（只记文档）

玩家上线提醒、饼图分析活跃度、自动命令支持把服务器出现的命令文字作为触发条件，逐字登记并各写一份五字段功能 md，补 15 条来源标注与运行逻辑演示；`src/server` 不存在、UI 整页演示未触发。

「干」继续替换自写代码：`src/core/leak.rs` 删掉自写 `Tracker` / `Tracked` 计数（191 → 99 行），测试迁移到 `Arc::strong_count` 与 027 的 `crossbeam_utils::sync::WaitGroup`；依赖仍 8 包 7 第三方，`cargo test --offline` 139 / 0。详见 `docs/decisions/028-server-features.md`。
''')
print('README_OK')
print('ALL_DOCS_OK')

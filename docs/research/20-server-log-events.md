# 开服器日志事件与活跃度资料（028 轮）

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
| L04 | `grep "joined the game\|left the game"`、`grep -i "issued server command"` 是常规的 join / 命令提取手法；`zgrep` 用于归档日志。 | https://mineguard.pro/blog/minecraft-server-logs-analysis | 已证实 |
| L05 | 实时读取用 `tail -f logs/latest.log`，配合 `grep --line-buffered` 做关键词告警；logrotate 或 Log4j 滚动策略控制体积。 | https://www.mczfw.com/blog/15884.html | 已证实 |
| L06 | 声明式解析：配置里给 `join_regex` / `quit_regex` / `chat_regex` 多组模式，每条带 `player_group` 捕获组索引，示例 `Server thread/INFO]: (.*) joined the game`。 | https://zread.ai/17TheWord/QueQiao/21-configuration-management | 已证实 |
| L07 | 事件配置样例：`pattern: '(?P\w+) joined the game'` 配 `event_type: player_join`，实时 tail → 正则 → webhook；支持自定义 `events.yml`。 | https://github.org/AlexisHutin/mclog2event | 未证实（返回域名为 `github.org` 而非 `github.com`，不据此复制） |
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

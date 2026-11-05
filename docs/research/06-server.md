# 服务端启动与配置

检索日期：2026-11-05
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。

## 目录与文件

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 根目录文件 | server.properties、bukkit.yml、spigot.yml、commands.yml、permissions.yml、eula.txt、ops.json、banned-ips.json、banned-players.json、whitelist.json、usercache.json、help.yml | 已证实 | https://docs.papermc.io/paper/configuration/ |
| 目录 | logs/、config/、plugins/、.paper-remapped/、bStats/、spark/ | 已证实 | https://docs.papermc.io/paper/configuration/ |
| 全局配置 | config/paper-global.yml、config/paper-world-defaults.yml | 已证实 | https://docs.papermc.io/paper/configuration/ |
| 世界级配置 | 各世界文件夹内 paper-world.yml | 已证实 | https://docs.papermc.io/paper/configuration/ |
| 日志 | logs/latest.log 与 gzip 归档 | 已证实 | https://docs.papermc.io/paper/configuration/ |
| eula.txt | eula=false 为默认，必须 eula=true 才能启动 | 已证实 | https://docs.papermc.io/paper/configuration/ |
| EULA 链接 | https://aka.ms/MinecraftEULA | 已证实 | https://docs.papermc.io/paper/configuration/ |
| 首次运行 | 生成 eula.txt，同意后重启 | 未证实 | 第三方部署文档，未取得一手原文 |
| Fabric 模组目录 | mods/ | 已证实 | https://fabricmc.net/ |

## server.properties

Java Edition 1.21.11 生成 68 个键。下表为自动化与联机相关键。

| 键 | 默认值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| enable-rcon | false | 已证实 | https://minecraft.wiki/w/Server.properties |
| rcon.password | 空字符串 | 已证实 | https://minecraft.wiki/w/Server.properties |
| rcon.port | 25575，范围 1-65534 | 已证实 | https://minecraft.wiki/w/Server.properties |
| broadcast-rcon-to-ops | true | 已证实 | https://minecraft.wiki/w/Server.properties |
| broadcast-console-to-ops | true | 已证实 | https://minecraft.wiki/w/Server.properties |
| server-port | 25565 | 已证实 | https://minecraft.wiki/w/Server.properties |
| query.port | 25565 | 已证实 | https://minecraft.wiki/w/Server.properties |
| online-mode | true | 已证实 | https://minecraft.wiki/w/Server.properties |
| motd | A Minecraft Server | 已证实 | https://minecraft.wiki/w/Server.properties |
| max-world-size | 29999984 | 已证实 | https://minecraft.wiki/w/Server.properties |
| max-players | 20 | 已证实 | https://minecraft.wiki/w/Server.properties |
| view-distance | 10，范围 3-32 | 已证实 | https://minecraft.wiki/w/Server.properties |
| simulation-distance | 10，范围 3-32 | 已证实 | https://minecraft.wiki/w/Server.properties |
| white-list | false | 已证实 | https://minecraft.wiki/w/Server.properties |
| level-name | world | 已证实 | https://minecraft.wiki/w/Server.properties |
| gamemode | survival | 已证实 | https://minecraft.wiki/w/Server.properties |
| difficulty | easy | 已证实 | https://minecraft.wiki/w/Server.properties |
| 文件编码 | UTF-8，读取失败回退 ISO-8859-1 | 已证实 | https://minecraft.wiki/w/Server.properties |
| 注释 | 以 # 开头的行忽略 | 已证实 | https://minecraft.wiki/w/Server.properties |
| 行尾 | Windows 写 CRLF，Unix 写 LF | 已证实 | https://minecraft.wiki/w/Server.properties |
| 重新生成 | 文件不存在时启动时生成 | 已证实 | https://minecraft.wiki/w/Server.properties |

## RCON

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 协议 | TCP/IP，明文传输含密码 | 已证实 | https://minecraft.wiki/w/RCON |
| 默认端口 | 25575 | 已证实 | https://minecraft.wiki/w/RCON |
| 启用条件 | enable-rcon=true 且 rcon.password 非空 | 已证实 | https://minecraft.wiki/w/RCON |
| 端口非法 | 非数字或不在 1-65535 时禁用并输出 Invalid rcon port | 已证实 | https://minecraft.wiki/w/RCON |
| 包字段 | Length(int32)、Request ID(int32)、Type(int32)、Payload | 已证实 | https://minecraft.wiki/w/RCON |
| Payload | NULL 结尾的 ASCII 文本，附加 1-byte NULL pad | 已证实 | https://minecraft.wiki/w/RCON |
| Length | 包剩余部分长度 | 已证实 | https://minecraft.wiki/w/RCON |
| 包类型 | 3 登录、2 执行命令、0 多包响应 | 已证实 | https://minecraft.wiki/w/RCON |
| 认证成功 | 返回同 Request ID，Type 2 | 已证实 | https://minecraft.wiki/w/RCON |
| 认证失败 | Request ID = -1 | 已证实 | https://minecraft.wiki/w/RCON |
| 字节序 | 小端（little-endian），与 Java Edition 协议相反 | 已证实 | https://minecraft.wiki/w/RCON → "Integers are little-endian, in contrast with the *Java Edition* protocol." |
| 引入版本 | Java Edition Beta 1.9 Prerelease 4 | 已证实 | https://minecraft.wiki/w/RCON → "Introduced in Java Edition Beta 1.9 Prerelease 4" |
| 分片上限 | S→C 每包 payload 4096 字节（total 4110）；C→S payload 1446（total 1460，页面标 outdated?） | 已证实 | https://minecraft.wiki/w/RCON |
| 分片行为 | 命令输出可跨多个包，每包 4096 字节，末包更短 | 已证实 | https://minecraft.wiki/w/RCON |
| Payload 编码 | ASCII | 已证实 | https://minecraft.wiki/w/RCON |
| Mojang 官方 RCON 文档 | 未取得 | 未证实 | https://minecraft.wiki/w/RCON |

## 005 纠错

| 位置 | 原结论 | 原因 | 修复动作 |
| --- | --- | --- | --- |
| 001 轮 06-server.md:34 | broadcast-rcon-to-ops 默认 false | https://minecraft.wiki/w/RCON 的 false 是示例配置值，不是默认值 | 改为 true，锚点换为 https://minecraft.wiki/w/Server.properties |
| 001 轮 06-server.md:43 | 2-byte pad | 原文拆为 Payload 的 NULL 结尾与 1-byte pad，尾部合计 2 个 NULL | 改为「NULL 结尾 + 1-byte NULL pad」 |
| 001 轮 06-server.md:40,46,48 | 引入版本、字节序、分片上限定为已证实 | 本轮原文核不到对应句子 | 降级为未证实 |

## 008 补证

| 一手原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| Integers are little-endian, in contrast with the *Java Edition* protocol. | 小端 | 已证实 | https://minecraft.wiki/w/RCON |
| Introduced in Java Edition Beta 1.9 Prerelease 4 | Beta 1.9 Prerelease 4 | 已证实 | https://minecraft.wiki/w/RCON |
| The output of the command may be split over multiple packets, each containing 4096 bytes (less for the last packet). | S→C 分片 4096 | 已证实 | https://minecraft.wiki/w/RCON |
| Maximum S->C packet payload length: 4096 (total: 4110) | 4110 | 已证实 | https://minecraft.wiki/w/RCON |
| Maximum C->S packet payload length: 1446 (total: 1460) - outdated? | 页面自带 outdated? 标记 | 已证实（带页面存疑标记） | https://minecraft.wiki/w/RCON |
| Responses are sent back with the same Request ID that you send. In the event of an auth failure ... request ID will be set to `-1`. | 认证失败 -1 | 已证实 | https://minecraft.wiki/w/RCON |

口径：

| 项 | 值 |
| --- | --- |
| 005 轮 62-64 行三项 | 008 轮取得一手原文，升级为已证实 |
| 工具摘要 | 写为 "Java Edition 1.9 prerelease 4"，丢掉 Beta |
| 采用值 | Java Edition Beta 1.9 Prerelease 4，取 EVIDENCE 原文 |
| C→S 1446/1460 | 页面自带 outdated?，不写死为实现硬上限 |
| Mojang 官方 RCON 文档 | 未取得，仍为未证实 |
| minecraft.wiki 归属 | 社区文档，不等于 Mojang 官方原文 |

## 自动化

| 需求项 | 落地接口 | 状态 |
| --- | --- | --- |
| 定时自动开关机 | 进程启动/终止 + 调度器 | 未实现 |
| 自动保存 | RCON save-all | 未实现 |
| 自动发言 | RCON say | 未实现 |
| 自动执行命令 | RCON 类型 2 | 未实现 |
| 玩家 ban/恢复 | banned-players.json / RCON ban pardon | 未实现 |
| 配置汉化 | server.properties、bukkit.yml、spigot.yml、paper-global.yml 键名映射 | 未实现 |
| 本地 AI 工具 API | 本地 HTTP 接口，端点未定 | 未实现 |

约束：
- 自动化类型：定期 / 持续 / 单次。
- 正常启动流程显示 EULA 同意说明。
- server.properties 写入按 UTF-8，保留 # 注释与 CRLF 行尾。

# 服务端启动与配置

检索日期：2026-11-04

## 目录与文件

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 根目录文件 | `server.properties`、`bukkit.yml`、`spigot.yml`、`commands.yml`、`permissions.yml`、`eula.txt`、`ops.json`、`banned-ips.json`、`banned-players.json`、`whitelist.json`、`usercache.json`、`help.yml` | 已证实 | docs.papermc.io configuration / vanilla-data-files |
| 目录 | `logs/`、`config/`、`plugins/`、`.paper-remapped/`、`bStats/`、`spark/` | 已证实 | docs.papermc.io configuration |
| 全局配置 | `config/paper-global.yml`、`config/paper-world-defaults.yml` | 已证实 | 同上 |
| 世界级配置 | 各世界文件夹内 `paper-world.yml` | 已证实 | 同上 |
| 日志 | `logs/latest.log` 与 gzip 归档 | 已证实 | 同上 |
| eula.txt | `eula=false` 为默认，必须 `eula=true` 才能启动 | 已证实 | docs.papermc.io vanilla-data-files |
| EULA 链接 | `https://aka.ms/MinecraftEULA` | 已证实 | 同上 |
| 首次运行 | 生成 `eula.txt`，同意后重启 | 部分已证实 | 第三方部署文档 |
| Fabric 模组目录 | `mods/` | 已证实 | fabricmc.net |

## server.properties

| 键 | 值/默认 | 四值 | 锚点 |
| --- | --- | --- | --- |
| `enable-rcon` | 布尔，启用 RCON | 已证实 | wiki.vg RCON / PaperMC docs |
| `rcon.password` | 空默认 | 已证实 | docs.papermc.io server-properties |
| `rcon.port` | 25575 | 已证实 | 同上 |
| `server-port` | 25565 | 已证实 | 同上 |
| `query.port` | 25565 | 已证实 | 同上 |
| `online-mode` | true | 已证实 | 同上 |
| `motd` | `A Minecraft Server` | 已证实 | 同上 |
| `max-world-size` | 29999984 | 已证实 | 同上 |
| `view-distance` | 10，范围 3-32 | 已证实 | 同上 |
| `simulation-distance` | 10，范围 3-32 | 已证实 | 同上 |
| `white-list` | false | 已证实 | 同上 |
| `broadcast-rcon-to-ops` | false | 已证实 | wiki.vg RCON |

## RCON

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 引入版本 | 1.9-pre4，Source RCON 实现 | 已证实 | wiki.vg Zh:RCON |
| 默认端口 | 25575 | 已证实 | 同上 |
| 字节序 | 小端 | 已证实 | 同上 |
| 包字段 | Length(int)、Request ID(int)、Type(int)、Payload(byte[])、2-byte pad | 已证实 | 同上 |
| 包类型 | 3 登录、2 命令、0 命令响应 | 已证实 | 同上 |
| 认证失败 | Request ID = -1 | 已证实 | 同上 |
| 分片 | S→C 每包最多 4096 字节 | 已证实 | 同上 |
| Payload 编码 | ASCII 文本 | 已证实 | 同上 |
| 结束判定 | 无明确结束包，需额外探活 | 已证实 | 同上 |
| Mojang 官方 RCON 文档 | 未取得 | 未证实 | 使用 wiki.vg 协议描述 |

## 自动化

| 需求项 | 落地接口 | 状态 |
| --- | --- | --- |
| 定时自动开关机 | 进程启动/终止 + 调度器 | 未实现 |
| 自动保存 | RCON `save-all` | 未实现 |
| 自动发言 | RCON `say` | 未实现 |
| 自动执行命令 | RCON 类型 2 | 未实现 |
| 玩家 ban/恢复 | `banned-players.json` / RCON `ban` `pardon` | 未实现 |
| 配置汉化 | `server.properties`、`bukkit.yml`、`spigot.yml`、`paper-global.yml` 键名映射 | 未实现 |
| 本地 AI 工具 API | 本地 HTTP 接口，端点未定 | 未实现 |

约束：
- 自动化类型：定期 / 持续 / 单次。
- 正常启动流程显示 EULA 同意说明。

# 开服器输入中的官方资料与协议一手调研

检索日期：2026-11-11
轮次：012
对应：docs/spec/12-server-features-input.txt 全篇；docs/spec/12-round-012-instructions.txt
锚点格式：完整 URL 或 `path:line`；锚点逐行独立。

## 插件服官方下载通道（用户第 3 条「忘了叫什么」）

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| HG01 | `Hangar is the best place to download plugins. Created by the PaperMC Team` | Hangar 由 PaperMC 团队创建 | 已证实 | https://hangar.papermc.io/?page=0&platform=VELOCITY |
| HG02 | `Hangar allows you to find and download the best Paper plugins, Velocity plugins or Waterfall plugins for your Minecraft server` | 支持 Paper / Velocity / Waterfall 三类插件 | 已证实 | https://hangar.papermc.io/?page=0&platform=VELOCITY |
| HG03 | `Crafted by the PaperMC team & contributors, Hangar is our own dedicated plugin repository, now in open beta!` | PaperMC 自有插件仓库，开放测试状态 | 已证实 | https://papermc.io/ |
| HG04 | `Base: https://hangar.papermc.io/api/v1` / `Hangar plugin repository, search projects and list platform-specific versions.` | API 基址，第三方文档转述 | 已证实 | https://www.eranio.com/docs/api/mp-hangar |
| HG05 | `GET https://hangar.papermc.io/api/v1` 官方 API 文档页 | robots 禁止抓取 | 受阻 | https://hangar.papermc.io/api/v1 |
| HG06 | `Paper plugins: Hangar (hangar.papermc.io) is the official Paper repository` / `Spigot & Bukkit plugins: SpigotMC (spigotmc.org/resources) and BukkitDev (dev.bukkit.org)` / `Sponge plugins: Ore (ore.spongepowered.org) is the Sponge plugin index` / `Modrinth (modrinth.com): newer multi-loader index` | 四类插件源分工 | 已证实 | https://www.g-portal.com/wiki/en?p=4679 |
| HG07 | `Creating the HANGAR_API_TOKEN repository secret` / `Go to your Hangar settings in the profile dropdown and click on "Api keys"` / `tick the create_version permission box` | Hangar 存在 API token 与 create_version 权限，用于发布 | 已证实 | https://docs.papermc.io/misc/hangar-publishing |
| HG08 | `GET /api/projects` / `limit Integer Limits the amount of projects returned (max / default: 25)` / `offset Integer Drops the first n projects` / `q String Search query` / `categories Comma Separated Integer List` | Ore Web API 列表端点 | 已证实 | https://docs.spongepowered.org/6.0.0/en/ore/routes/list-projects.html |
| HG09 | `Official package manager for Sponge.` | Ore 自述 | 已证实 | https://docs.spongepowered.org/6.0.0/en/ore/routes/list-projects.html |
| HG10 | `Hangar / Ore 插件源接入` | 用户第 24 条已自行列出两个名字 | 已证实 | docs/spec/12-server-features-input.txt |
| HG11 | 用户第 3 条所指「官方的下载通道」是否即 HG10 的 Hangar / Ore | 用户同一份文档内两处表述重叠 | 未证实 | docs/spec/12-server-features-input.txt 第 3、24 条 |

结论：插件服官方通道候选为 Hangar（PaperMC 官方）、Ore（Sponge 官方）、SpigotMC / BukkitDev（Spigot/Bukkit 社区）、Modrinth（多加载器索引）。具体选哪一个作为默认源未拍板。Hangar REST 官方文档一手页受阻，HG04 为第三方转述。

## 服务端 mod 声明（用户第 3 条）

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| MS01 | `environment (one of the following values) - client_and_server - client_only - client_only_server_optional - singleplayer_only - server_only - server_only_client_optional - dedicated_server_only - client_or_server - client_or_server_prefers_both - unknown` | Modrinth 搜索 facet `environment` 的 10 个取值 | 已证实 | https://docs.modrinth.com/api/operations/searchprojects/ |
| MS02 | `client_side ... Deprecated - use environment instead.` / `server_side ... Deprecated - use environment instead.` / `Allowed values: required optional unsupported unknown` | 项目详情字段已弃用，改用 `environment` | 已证实 | https://docs.modrinth.com/api/operations/getproject/ |
| MS03 | `project_type ... Allowed values: mod modpack resourcepack shader` | 项目类型取值，无 plugin 独立类型 | 已证实 | https://docs.modrinth.com/api/operations/getproject/ |
| MS04 | `env (optional) ... "env": { "client": "required", "server": "unsupported" }` / `server refers to the dedicated server.` | mrpack 内逐文件 env 标记 | 已证实 | https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack |
| MS05 | `The sectionId ... 6; // the mods` / `gameId ... 432; // Minecraft game id` / `categoryId ... the sub category id of the sectionId` / `modLoaderType` / `pageSize` | CurseForge 搜索按 classId / categoryId / modLoaderType 过滤 | 已证实 | https://xmcl.app/en/core/curseforge/SearchOptions |
| MS06 | CurseForge 官方 API 中与 MS01 等价的 server-only 字段 | 官方 REST 端点页受阻；XMCL 接口表无该字段 | 未证实 | https://docs.curseforge.com/rest-api/endpoint/POST_1_mods/ |
| MS07 | `This MUST contain the SHA1 hash and the SHA512 hash` / `Danger: If you implement an "import ZIP" feature or similar, make sure this field doesn't exit the Minecraft instance directory` / `make sure it doesn't contain .. or start with a drive name` / `server-overrides will be applied after the overrides folder, overwriting its contents` | mrpack 安全约束：哈希、路径穿越防护、服务端覆盖层 | 已证实 | https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack |
| MS08 | `When uploading to Modrinth, the pack is validated so that only URIs from the following domains are allowed: cdn.modrinth.com github.com raw.githubusercontent.com gitlab.com` | 下载域名白名单 | 已证实 | https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack |
| MS09 | `formatVersion ... The current value at the time of writing is 1.` / `modrinth.index.json in the root of the zip` / `MIME type application/x-modrinth-modpack+zip` | mrpack 容器格式 | 已证实 | https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack |

结论：Modrinth 侧可用 `environment` facet 过滤 `server_only` / `dedicated_server_only`；CurseForge 侧未找到等价字段，015 轮 X01-X04 合规冲突仍未解除。

## EULA 与官方页面

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| EU01 | `# Minecraft End(er)-User License Agreement ("EULA")` | 官方页面标题 | 已证实 | https://www.minecraft.net/en-us/eula |
| EU02 | `This EULA is a legal agreement between you and us (Mojang AB and Microsoft Corporation ...)` / `If you buy, download, or use any of our Services, or if you click to accept this EULA, that means you agree to this Minecraft EULA and the Microsoft Services Agreement` | 缔约方与同意行为 | 已证实 | https://www.minecraft.net/en-us/eula |
| EU03 | `A file called eula.txt will be generated after you run the server for the first time. Open it in a text editor and change eula=false to eula=true.` / `If you don't do this, the server will shut down immediately when you try to start it.` | 首次启动生成 eula.txt；不同意则立即退出 | 已证实 | https://minecraft.wiki/w/Tutorial:Setting_up_a_Java_Edition_server |
| EU04 | `Now the server has been set up, and you can simply run it with java -jar server.jar --nogui` | 无 GUI 启动命令 | 已证实 | https://minecraft.wiki/w/Tutorial:Setting_up_a_Java_Edition_server |
| EU05 | 用户第 7 条「打开我的世界官网上面的这个页面」 | 指向 EU01 的 URL | 已证实 | docs/spec/12-server-features-input.txt 第 7 条 |
| EU06 | 用户要求的「手动同意 EULA」在本软件内的写入时机 | EU03 只给文件编辑流程，未给软件内 UI 流程 | 未证实 | EU03 |

## 原版命令 /say 与 /talk

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| CM01 | `Broadcasts message in the chat to all players on the server.` / `Java Edition: say <message>` / `Permission level required: 2 [ JE only ]; 1 [ BE only ]` | `/say` 语法与权限等级 | 已证实 | https://minecraft.wiki/w/Commands/say |
| CM02 | 页面未出现 `/talk` 命令 | 原版 Java 版命令表无 `/talk` | 已证实 | https://minecraft.wiki/w/Commands/say |
| CM03 | `To become or add an operator, type /op <targets> into the server console.` / `You can stop the server by typing stop in the command line` | 服务端控制台命令不带 `/` 前缀 | 已证实 | https://minecraft.wiki/w/Tutorial:Setting_up_a_Java_Edition_server |
| CM04 | 用户第 5 条「即/然后上面就有一些命令的快捷显示，当然被打出来的时候不能有这个/」 | 与 CM03 控制台口径一致 | 已证实 | docs/spec/12-server-features-input.txt 第 5 条 |
| CM05 | 用户第 16 条「自动加入上say或talk实现快速聊天」中的 `talk` | 非原版命令，来源未定 | 未证实 | CM02 |
| CM06 | 「原版增强」的开启方式与命令候选词表来源 | 原版控制台未提供补全建议 API 的一手说明 | 未证实 | CM01-CM03 |

## Java 版本与 MC 版本对应

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| JV01 | `对于1.16.5(1.17:21w18a)及以前的多数游戏版本,官方推荐的Java版本是Oracle Java 1.8.0_51(Java 8)` / `1.12(17w13a) - 1.16.5 ... 必须使用Java 8或更高版本` | Java 8 | 已证实 | https://zh.minecraft.wiki/w/Tutorial:取得遊戲 |
| JV02 | `对于1.17(21w19a) - 1.17.1(1.18:1.18-pre1)的游戏版本,必须使用Java 16或更高版本才能运行` | Java 16 | 已证实 | https://zh.minecraft.wiki/w/Tutorial:取得遊戲 |
| JV03 | `对于1.18(1.18-pre2) - 1.20.4(1.20.5:24w13a)的游戏版本,必须使用Java 17或更高版本才能运行` | Java 17 | 已证实 | https://zh.minecraft.wiki/w/Tutorial:取得遊戲 |
| JV04 | `对于1.20.5(24w14a) - 1.21.11的游戏版本,必须使用Java 21或更高版本才能运行` / `对于26.1(26.1-snapshot-1)及以上的游戏版本,必须使用Java 25或更高版本才能运行` | Java 21 / Java 25 | 已证实 | https://zh.minecraft.wiki/w/Tutorial:取得遊戲 |
| JV05 | `建议使用LTS版Java或最新版的Java` / `建议使用64位的Java` | 64 位与 LTS 建议 | 已证实 | https://zh.minecraft.wiki/w/Tutorial:取得遊戲 |
| JV06 | `Java 21 or later is required to run 1.20.5 (20w14a) and later.` | 英文 wiki 口径 | 已证实 | https://minecraft.wiki/w/Tutorial:Required_Java_versions |
| JV07 | 用户第 1、2、24 条的 Java 自动下载与镜像源 | Oracle / OpenJDK 分发条款与镜像地址 | 未证实 | docs/spec/00-requirements.txt:171-175 |
| JV08 | Java 25 对应 MC 26.1+ 与本项目目标 MC 版本范围 | 未定 | 未证实 | JV04 |

## ops.json 与运行期写入

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| OP01 | `A Minecraft server keeps its people in five JSON files in the server root: ops.json ... whitelist.json ... banned-players.json and banned-ips.json ... usercache.json` / `Every entry is keyed by UUID, not by name.` | 五个 JSON 文件与 UUID 键 | 已证实 | https://renode.space/blog/minecraft-ops-json-whitelist-json-explained |
| OP02 | `The server reads them into memory at startup and writes the whole list back to disk whenever a command changes it, which is why a file you edited by hand while the server was running quietly reverts.` | 运行期手改文件会被内存回写覆盖 | 已证实 | https://renode.space/blog/minecraft-ops-json-whitelist-json-explained |
| OP03 | `The safe rule is short: use /op, /whitelist and /ban while the server runs, and edit the files only with it stopped.` | 运行期走命令，停服才改文件 | 已证实 | https://renode.space/blog/minecraft-ops-json-whitelist-json-explained |
| OP04 | `ops.json ... "uuid": ..., "name": ..., "level": 4, "bypassesPlayerLimit": true` / `level is where hand editing earns its keep` / `1 to 4 Operator permission level` | 字段与 1-4 级 | 已证实 | https://renode.space/blog/minecraft-ops-json-whitelist-json-explained |
| OP05 | `To become or add an operator, type /op <targets> into the server console.` / `Operator status will not be changed if you change your username due to the use of UUID` | `/op` 与 UUID 绑定 | 已证实 | https://minecraft.wiki/w/Tutorial:Setting_up_a_Java_Edition_server |
| OP06 | 用户第 10 条「如果发现op改变且没有在这个页面单独选中,自动移出对应的op」 | 与 OP02 冲突：文件监听拿不到运行期的权威状态 | 已证实（冲突成立） | OP02、docs/spec/12-server-features-input.txt 第 10 条 |

## 种子 NBT 与进度存储

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| NB01 | `*WorldGenSettings:此存档的世界生成设置` / `*seed:数字形式的世界种子` | 新格式种子字段 | 已证实 | https://zh.minecraft.wiki/w/Level.dat_old |
| NB02 | `*RandomSeed:该世界的种子｡当此项不存在时游戏默认为0` | 旧格式种子字段 | 已证实 | https://zh.minecraft.wiki/w/Level.dat_old |
| NB03 | `进度存储文件位于/players/advancements/<uuid>.json` / `当玩家退出世界时,此文件会被立刻保存` / `如果读取过程中产生了I/O异常 ... 且玩家进度全部丢失` | 进度文件格式与读写时机 | 已证实 | https://zh.minecraft.wiki/w/进度存储格式 |
| NB04 | `*DataVersion ... 如果此项不存在则游戏认为此项是1343(Java版1.12.2)` | 版本兼容下限 | 已证实 | https://zh.minecraft.wiki/w/进度存储格式 |
| NB05 | 用户第 14 条「快速显示种子号（需要使用nbt功能）」 | 需同时读 NB01 与 NB02 两套字段 | 已证实 | docs/spec/12-server-features-input.txt 第 14 条 |
| NB06 | viaNBT 与 Rust 集成方式 | 011 轮遗留 Q08 / VN05 | 未证实 | docs/research/15-input-survey.md VN05 |
| NB07 | 旧版本 achievements 与 advancements 的兼容性 | 未取得 | 未证实 | NB03、NB04 |

## 服务器图标、TPS、代理端、端口映射

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| SI01 | `The server icon can be specified by adding server-icon.png image file into the server.jar's working directory` / `shows the server icon in 64×64 pixel size` | 64×64 PNG，放服务端工作目录 | 已证实 | https://minecraft.wiki/w/Server_List |
| SI02 | `create an icon that is 64x64 pixels. Export it in the PNG format` / `You must restart the server after you place the file in the folder` | 需重启才加载 | 已证实 | https://www.spigotmc.org/wiki/server-icon/ |
| SI03 | 用户第 27 条「支持png快速设置服务器logo（会自动调整像素）」 | 自动调整目标为 64×64 需用户确认 | 未批准 | docs/spec/12-server-features-input.txt 第 27 条 |
| TP01 | `TPS means ticks per second ... 20 is the healthy rate` / `MSPT, milliseconds per tick ... must stay under 50 for the server to hold 20 TPS` | TPS / MSPT 定义 | 已证实 | https://minecrafthub.io/articles/what-is-tps-in-minecraft |
| TP02 | `On Paper, /tps reports TPS over the past 1, 5 and 15 minutes, and /mspt reports average, minimum and maximum MSPT` / `both are superseded by /spark` / `/tick query (added in 1.20.3, permission level 3)` | 取值途径与版本门槛 | 已证实 | https://minecrafthub.io/articles/what-is-tps-in-minecraft |
| TP03 | `Folia is a new fork of Paper that adds regionized multithreading` | PaperMC 产品线 | 已证实 | https://papermc.io/ |
| PX01 | `Velocity is a high-performance, scalable Minecraft proxy server` | Velocity 定位 | 已证实 | https://papermc.io/ |
| PX02 | `BungeeCord ... Velocity ... Feature table` / `The Velocity API does not support plugins made for BungeeCord/Waterfall` / `Secure player information forwarding ❌ ❌ ✅` | 两者插件 API 不兼容，转发安全性差异 | 已证实 | https://docs.papermc.io/velocity/comparisons-to-other-proxies/ |
| PX03 | 用户第 25 条「代理端（Velocity/BungeeCord）配置向导」 | 需分别适配两套 API | 已证实 | docs/spec/12-server-features-input.txt |
| UP01 | `In 2013, NAT-PMP was superseded by the IETF Standards Track Port Control Protocol [RFC6887]. PCP builds on NAT-PMP` | NAT-PMP → PCP | 已证实 | https://rfc-editor.org/rfc/rfc6886 |
| UP02 | `UPnP IGD is a large and complicated collection of protocols (360 pages of specification spread over 13 separate documents)` / `For example, a UPnP IGD home gateway allows messages that tell it to change the DNS server addresses` / `If the protocol is misused ... malicious web content ... persistent change to the home gateway's configuration` | UPnP IGD 可被用于改 DNS 的安全风险 | 已证实 | https://rfc-editor.org/rfc/rfc6886 |
| UP03 | 用户第 24 条「端口冲突检测 + UPnP 自动映射」 | 默认是否开启、是否改用 PCP 未定 | 未批准 | UP02 |

## 日志上传 mclo.gs

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| MC01 | `Create a log POST https://api.mclo.gs/1/log application/json` / `Posting content with the content type application/x-www-form-urlencoded is still supported for backwards compatibility, but does not support setting metadata` | 上传端点 | 已证实 | https://api.mclo.gs/ |
| MC02 | `content string The raw log file content as string. Limited to 10.00 MiB and 25,000 lines.` / `source string` / `metadata array` | 字段与上限 | 已证实 | https://api.mclo.gs/ |
| MC03 | 日志外传含玩家 IP / UUID / 种子 / 聊天内容的处置 | 未取得条款与用户授权 | 未证实 | MC01、MC02、docs/spec/12-server-features-input.txt 第 21、24 条 |
| MC04 | 用户第 20 条「快速导出日志」与第 24 条「一键上传 mclo.gs」 | 两个不同动作，后者是外传 | 已证实 | docs/spec/12-server-features-input.txt |

## 012 新增来源

| 编号 | URL | 用途 | 结果 |
| --- | --- | --- | --- |
| P54 | https://hangar.papermc.io/?page=0&platform=VELOCITY | HG01-HG02 | 200 |
| P55 | https://papermc.io/ | HG03、TP03、PX01 | 200 |
| P56 | https://www.eranio.com/docs/api/mp-hangar | HG04 | 200 |
| P57 | https://hangar.papermc.io/api/v1 | HG05 | 受阻，robots 禁止 |
| P58 | https://www.g-portal.com/wiki/en?p=4679 | HG06 | 200 |
| P59 | https://docs.papermc.io/misc/hangar-publishing | HG07 | 200 |
| P60 | https://docs.spongepowered.org/6.0.0/en/ore/routes/list-projects.html | HG08-HG09 | 200 |
| P61 | https://docs.modrinth.com/api/operations/searchprojects/ | MS01 | 200 |
| P62 | https://docs.modrinth.com/api/operations/getproject/ | MS02-MS03 | 200 |
| P63 | https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack | MS04、MS07-MS09 | 200 |
| P64 | https://xmcl.app/en/core/curseforge/SearchOptions | MS05 | 200 |
| P65 | https://docs.curseforge.com/rest-api/endpoint/POST_1_mods/ | MS06 | 受阻 |
| P66 | https://www.minecraft.net/en-us/eula | EU01-EU02 | 200 |
| P67 | https://minecraft.wiki/w/Tutorial:Setting_up_a_Java_Edition_server | EU03-EU04、CM03、OP05 | 200 |
| P68 | https://minecraft.wiki/w/Commands/say | CM01-CM02 | 200 |
| P69 | https://zh.minecraft.wiki/w/Tutorial:取得遊戲 | JV01-JV05 | 200 |
| P70 | https://minecraft.wiki/w/Tutorial:Required_Java_versions | JV06 | 200 |
| P71 | https://renode.space/blog/minecraft-ops-json-whitelist-json-explained | OP01-OP04 | 200 |
| P72 | https://zh.minecraft.wiki/w/Level.dat_old | NB01-NB02 | 200 |
| P73 | https://zh.minecraft.wiki/w/进度存储格式 | NB03-NB04 | 200 |
| P74 | https://api.mclo.gs/ | MC01-MC02 | 200 |
| P75 | https://minecraft.wiki/w/Server_List | SI01 | 200 |
| P76 | https://www.spigotmc.org/wiki/server-icon/ | SI02 | 200 |
| P77 | https://minecrafthub.io/articles/what-is-tps-in-minecraft | TP01-TP02 | 200 |
| P78 | https://docs.papermc.io/velocity/comparisons-to-other-proxies/ | PX02 | 200 |
| P79 | https://rfc-editor.org/rfc/rfc6886 | UP01-UP02 | 200 |

## 未证实 / 受阻

| 项 | 四值 |
| --- | --- |
| Hangar REST 官方 API 文档全文 | 受阻 |
| CurseForge 官方 server-only 等价字段 | 未证实 |
| CurseForge REST 端点页 | 受阻 |
| `/talk` 来源 | 未证实 |
| 「原版增强」命令候选词表来源 | 未证实 |
| Java 镜像源与分发条款 | 未证实 |
| ops.json 运行期权威状态的读取途径 | 未证实 |
| viaNBT 与 Rust 集成方式 | 未证实 |
| 旧版 achievements 兼容 | 未证实 |
| mclo.gs 日志外传条款与用户授权 | 未证实 |
| UPnP 默认开启与否、PCP 替代 | 未批准 |
| server-icon 自动调整目标尺寸 | 未批准 |

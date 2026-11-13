# 服务器列表自动发现与连接权重调研

| 项 | 值 |
| --- | --- |
| 轮次 | 021 |
| 依据 | docs/spec/21-round-021-instructions.txt；020 轮服务器状态理解纠偏 |
| 来源数 | 9 个完整 URL 锚点 + 4 组公开资料 |
| 禁止项 | 中文镜像与社区资料不冒充官方规范；未证实项不写进实现 |

## 一手来源

| 编号 | 来源 | 取到的事实 | 四值 |
| --- | --- | --- | --- |
| R01 | https://minecraft.wiki/w/Server_list_storage_format | `servers.dat`（中文页名为「服务器列表存储格式」）：未压缩 NBT；位于游戏目录根 `/servers.dat`，有备份；默认不存在，仅在游戏内添加过服务器或进入过任何服务器后才创建；根下 `servers` 为 List<Compound>，字段 `acceptTextures`（byte）、`hidden`（byte）、`icon`（String，base64 PNG）、`ip`（String）、`name`（String） | 已证实 |
| R02 | https://zh.minecraft.wiki/w/%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%88%97%E8%A1%A8%E5%AD%98%E5%82%A8%E6%A0%BC%E5%BC%8F | 存储行为：服务器列表本质上是**可见**与**隐藏**两份；可见列表中的服务器「游戏会主动获取信息以同步当前服务器的信息」；隐藏列表最多 16 个，「游戏不会主动同步信息」；通过 Quick Play（快速进入）或直接进入且不在可见列表内的服务器会进隐藏列表；从隐藏列表再次添加会转回可见列表 | 已证实 |
| R03 | https://minecraft.wiki/w/Servers.dat_format | 同样 NBT 结构；`servers.dat` 不保存直接连接 IP（在 options.txt）、不保存 LAN 服务器信息；文件位于启动器配置指定目录的根；`acceptedCodeOfConduct` 为可选字段；`icon` 为 base64 PNG；`name` 可用 § 格式化码 | 已证实 |
| R04 | https://minecraft.wiki/w/Server_list | 原版服务器列表显示：第一行 64×64 图标 + 玩家自定义名称；第二行 MOTD（`server.properties` 的 `motd`，支持 § 颜色码，默认 `A Minecraft Server`）；右上在线人数 + 网络条，悬停显示 ping；ping 分档 0–150 / 150–300 / 300–600 / 600–1000 / >1000 ms / Can't connect；LAN 服务器自动列在底部；列表顺序可用上下箭头或 Shift+↑ / Shift+↓ 调整；首次进入多人游戏有在线游戏提示 | 已证实 |
| R05 | https://minecraft.wiki/w/Java_Edition_protocol/Server_List_Ping | 1.7+ SLP：handshake next state=1 → Status Request → Status Response（JSON 字符串）→ Ping/Pong；JSON 含 `version.name/protocol`、`players.max/online/sample`、`description`（text component）、`favicon`（64×64 PNG base64）、`enforcesSecureChat`；SLP 可被禁用；1.7 前后不兼容 | 已证实 |
| R06 | https://zh.minecraft.wiki/w/Java%E7%89%88%E7%BD%91%E7%BB%9C%E5%8D%8F%E8%AE%AE/%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%88%97%E8%A1%A8%E6%9F%A5%E8%AF%A2 | 中文一手页补充：`description` 原版服务端只可能给字符串但客户端按文本组件解析；`players` 缺失时客户端渲染灰色 `???`；`favicon` 必须 64×64 否则拒绝渲染；`sample` 默认最多 12 个 | 已证实 |
| R07 | https://wikivg.booky.dev/NBT | NBT 示例中 `servers.dat` 永远**未压缩**（与 `level.dat` 的 gzip 相反）；根下 `servers` List，每项至少 `ip`、`name`，可含 `icon`、`acceptTextures` | 已证实（协议社区规范站） |
| R08 | https://github.com/lucide-icons/lucide | 图标沿用 019 的 88 枚，ISC + Feather 派生 MIT | 已证实 |
| R09 | https://minecraft.wiki/w/Server_List_Ping | 与 R05 同源；Notchian 服务端状态响应各字段缺省行为细则未取得 | 未证实 |

## 公开资料与社区事例

| 编号 | 来源 | 取到的事实 | 四值 |
| --- | --- | --- | --- |
| C01 | https://minecraftstatus.com/blog/minecraft-motd-java-status-response | SLP 只证明状态端点应答，不证明能进服、认证健康或人数真实；`version.protocol=-1` 是探测约定值不是损坏；MOTD 是不可信显示数据，渲染成 HTML 必须转义、绝不执行；`favicon` 必须 64×64 PNG data URI；`players` 可缺省 | 已证实（公开资料） |
| C02 | https://www.joingg.co/blog/minecraft-motd-and-server-icon | 打开多人游戏列表时客户端会 ping **每一个已保存服务器**；列表第一行是玩家输入的名字（默认 `Minecraft Server`），其余都来自服务器；`server-icon.png` 需 64×64 且要重启服务端才加载；`enable-status=false` 会让条目看起来离线；MOTD 两行按像素宽度截断 | 已证实（公开资料） |
| C03 | https://www.joingg.co/blog/minecraft-server-list-ping-end-to-end | 五包交换；`description` 是 text component 不是裸字符串；`players.sample` 不是玩家名单；延迟是探测端到服务端往返 | 已证实（公开资料） |
| C04 | https://www.fumora.net/lab/minecraft-server-list-ping-response | 第三方服务端可由 ServerListPingEvent 改 MOTD、人数、图标，取消事件会让客户端看到离线；维护态常通过改 MOTD 表达 | 已证实（公开资料） |
| C05 | https://www.mczfw.com/blog/17718.html | PCL2 以 LoaderCombo 模块化任务链组织启动流程；HMCL / PCL2 / FCL / Pojav 架构对比 | 已证实（社区分析） |
| C06 | https://idctop.com/article/754823.html 与 https://idctop.com/article/671925.html | **第三方启动器一般不读官方 servers.dat，而是各自保存服务器列表**：HMCL 用 `servers.json` / `.bak`，PCL2 用 PCL 目录下 servers 或 setting 相关文件，BakaXL 用含 server 字样的 JSON；`servers.dat_old` 是常见备份；`latest.log` 里 `Connecting to` 能找回地址 | 已证实（社区经验）；逐启动器精确路径标未证实 |
| C07 | https://blog.gitcode.com/bd9d021e23f6564e4df321ca87207b00.html | PCL2-CE 2.11.2 服务器列表改进：重构延迟测试算法、优化 UI 响应速度、增强异常处理、时间排序等值处理 | 已证实（社区版本说明） |
| C08 | https://harmoniya-net.github.io/opys/plugins/serverlist | 社区工具直接生成 `servers.dat` 预填列表，默认路径 `${game_directory}/servers.dat`；该文件会被覆盖，玩家自己加的服会在下次更新时丢失 | 已证实（社区工具文档） |

## 对用户描述的逐条对照

| 用户原话 | 对应事实 | 结论 |
| --- | --- | --- |
| 「用户设置好服务器以后就会自动性的去尝试连接」 | R04 / C02：打开多人游戏列表客户端会 ping 每个已保存服务器；C07 社区启动器有延迟测试算法 | 原版与社区都有，直接沿用 |
| 「获得缓存作为权重进行推荐」 | R02 可见列表由游戏主动同步信息；R05 SLP 结果是一次探测 | 启动器把探测结果缓存为排序权重，是社区已有做法的延伸 |
| 「我的世界会自动在目录当中放置一个专门用来看服务器连接的文件」 | R01 / R02 / R03：`servers.dat`，未压缩 NBT，默认不存在，加过服或进过服才创建 | 已证实；这是自动分析的数据源 |
| 「如果服务器没办法正常连接，那么就会放到下面（用户锁定的不受影响）」 | R04 原版 ping 分档含 Can't connect；C01 SLP 不保证能进服 | 失败沉底 + 锁定项保持原位，属排序策略，不改动游戏文件 |
| 「双击以后就会进入服务器」 | R04 原版列表双击进入；013 轮已登记双击按权重选实例 | 已证实 |
| 「上次使用的实例与上次使用这个服务器的实例然后再去范围进行绑定」 | 013 轮 F07/F08/F09 与 016 轮 dispatcher 权重口径；无一手官方文档 | 项目内部口径，按用户逻辑落地 |
| 「服务器上面显示什么，就按照正常我的世界现实的逻辑和我的世界的发现逻辑进行」 | R04 四元素 + LAN 底部自动列出；R06 字段解析；C02 MOTD/图标来源 | 已证实；不另做一套状态配色与文案 |
| 「其他的地方社区都有相关事例」 | C05 / C06 / C07 / C08 | 已证实；但 C06 指出第三方启动器多数自存列表，KCU 读官方 `servers.dat` 是比社区多做一层，不照抄 |

## 结论

| 编号 | 结论 | 依据 |
| --- | --- | --- |
| J01 | 自动分析读游戏目录 `servers.dat`（未压缩 NBT），只读不写，含可见 / 隐藏 / 快速进入三类来源 | R01 / R02 / C08 |
| J02 | 添加服务器后立即尝试连接；结果与延迟、在线人数、最近使用时间一起缓存为权重 | R02 / R04 / C02 / C07 |
| J03 | 排序：锁定置顶 → 连得上按延迟与最近使用 → 连不上沉底；锁定项不受连接失败影响 | 021 指令 / R04 |
| J04 | 显示照原版：64×64 图标、玩家命名、两行 MOTD（§ 码转义且不当 HTML 执行）、人数、ping 条、版本名、LAN 底部 | R04 / R05 / R06 / C01 |
| J05 | 双击进服：上次用该服的实例 → 上次全局实例 → 兼容范围；锁定实例优先；不兼容给换实例 | 021 指令 / 013 轮口径 |
| J06 | 社区有现成事例，但第三方启动器一般自存列表；KCU 直接读官方 `servers.dat` 属额外一层，需单独验证多实例目录 | C06 |
| J07 | 产品界面不出现内部工程叙事；工程结论只落 docs/，界面只给结果 | 021 指令 |

## 约束

| 编号 | 内容 |
| --- | --- |
| S01 | MOTD 与服务器名是不可信显示数据，渲染必须转义，不执行脚本。 |
| S02 | `servers.dat` 只读；不覆盖玩家在游戏里加的服务器；多实例隔离目录都要扫。 |
| S03 | SLP 只证明状态端点应答，不写成「能进服」。 |
| S04 | 1.20.5 / 1.21 是否改过 `servers.dat` 文件名或结构未取得一手证据，本轮按现有 NBT 结构登记，标未证实。 |
| S05 | 社区启动器精确配置路径来自经验文章，不冒充官方；逐仓库核对前标未证实。 |
| S06 | 以上结论只落设计与演示层，021 轮 `src/` 无变化。 |

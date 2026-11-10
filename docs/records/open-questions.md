# 待拍板问题全集

轮次：012
状态：全部未拍板，用户当轮指令「全部告诉我不要保留」「明天统一处理」
用途：D06 触发、蓝图批准、D07 逐层搭建之前的唯一输入
规则依据：docs/spec/00-requirements.txt:3、:249；docs/decisions/003-remote.md D05-D07；docs/rules/build-preconditions.md

每条给出编号、问题、依据锚点、四值、需要的答复形式。四值：已证实 / 已失败 / 未证实 / 受阻。

## A 组：输入文档结构

| 编号 | 问题 | 依据 | 四值 | 需要的答复 |
| --- | --- | --- | --- | --- |
| Q-A01 | 首行 `开服器1.先检查有没有可以直接使用的java`，编号 1 与标题连写，是否算独立第 1 条 | docs/spec/12-server-features-input.txt:1 | 已证实 | 确认算 / 不算 |
| Q-A02 | `25多实例同时运行的资源配额/调度` 无点号且与文字连写，是否算第 25 条 | docs/spec/12-server-features-input.txt | 已证实 | 确认编号 |
| Q-A03 | 编号缺 26 | docs/features/server-backlog.md 输入结构事实 | 已证实 | 补内容 / 保留缺号 / 顺延 27 |
| Q-A04 | 第 24 条与第 25 条各自下挂一组 `·` 条目，两组是否算独立功能清单 | docs/features/server-backlog.md 分组索引 | 已证实 | 确认分组边界 |
| Q-A05 | `·` 字符 35、独立行 34，差 1 为同行首项；条目总数按 35 还是 34 | docs/spec/12-server-features-input.txt | 已证实 | 确认计数口径 |
| Q-A06 | 第 21 条含「这三项补的是运维闭环，没有它们，定时任务和备份只能在正常情况下工作」，属于设计判断而非功能描述，是否作为验收标准 | docs/spec/12-server-features-input.txt 第 21 条 | 未证实 | 确认验收口径 |

## B 组：既有规则冲突

| 编号 | 问题 | 依据 | 四值 | 需要的答复 |
| --- | --- | --- | --- | --- |
| Q-B01 | 用户当轮说「搜完所有的文档以后就可以彻底开工了」，但同轮又说「拿捏不了的问题全部告诉我，明天统一处理」；本轮未写 `src/`，是否按「明天答复后开工」执行 | docs/spec/12-round-012-instructions.txt；docs/spec/00-requirements.txt:3、:249 | 已证实 | 确认开工时点 |
| Q-B02 | D06 信号：用户写明此前「过一会我会把要求也给你」，本轮又给开服器输入；是否算「实在想不到新功能」 | docs/decisions/003-remote.md D05-D06；docs/spec/11-features-input.txt 开头段 | 未证实 | 明确 D06 触发语 |
| Q-B03 | `005-blueprint.md` 状态未批准，D07 顺序 core → dispatcher → lightweight → headless → normal → UI → 构建 → 部署 是否启用 | docs/decisions/005-blueprint.md；docs/decisions/003-remote.md D07 | 未证实 | 批准或修改蓝图 |
| Q-B04 | X01-X04 中 CF03 缓存字段、CF02 代理路径、CF01 唯一 Key 归属未逐条拍板 | docs/research/12-compliance.md；docs/records/interface-log.md X01-X04 | 已证实 | 四条各选处置 |
| Q-B05 | 011 轮 D13「本地 API 绑定回环、服务器 AI API 为例外」，本轮第 4 条要求「本地或本地有容器的 AI」可调用；容器网桥网段是否放行 | docs/research/14-batch-network.md L01-L04；docs/spec/12-server-features-input.txt 第 4 条 | 已证实（冲突成立） | 回环 / 容器网段 / 隧道，三选一 |
| Q-B06 | 第 2 条「如果在国外就直接使用官方源」直接依赖 011 轮未解决的地域判定口径 | docs/research/13-platform-api.md P01-P07；docs/spec/12-server-features-input.txt 第 2 条 | 已证实（冲突成立） | 物理位置或区域设置，二选一 |
| Q-B07 | 011 轮 D08「Win7 默认轻量」与本轮开服器是否共用同一调度器；开服器在 Win7 上是否允许运行 | docs/decisions/011-feature-input.md D08；docs/research/13-platform-api.md C01-C06 | 未证实 | 确认开服器最低 OS |
| Q-B08 | 011 轮 U04「模组尽量去重聚合」与本轮 13 组重复项，合并口径 | docs/features/server-backlog.md 重复项表 | 已证实 | 合并 / 各自独立 / 以 012 覆盖 |
| Q-B09 | 011 轮 D20 把 `.kcul` 拆为 `.kculf` 与 `kculh`；开服器实例文件是否新增扩展名 | docs/decisions/011-feature-input.md D20 | 未证实 | 确认扩展名集合 |
| Q-B10 | 011 轮 D17 项目 GPLv3、不同许可证动态链接、源文件头许可证、拼接后源与产物对比；本轮拟接入的 Hangar / Ore / mrpack / mclo.gs 各自条款 | docs/research/15-input-survey.md OL01-OL07 | 未证实 | 逐项许可判定 |
| Q-B11 | 011 轮 D02-D03：CF 凭据不进公仓、特殊版单开私仓；本轮第 3 条 CurseForge 调用与第 4 条 AI API 的密钥归属 | docs/decisions/011-feature-input.md D02-D03 | 未证实 | 确认凭据存放位置 |
| Q-B12 | 011 轮 D01 后端仓只读；本轮第 9 条 FTP/SFTP「访问互联网上面的服」是否指向该仓或另一服务 | docs/research/15-input-survey.md BR01-BR08 | 未证实 | 给出目标服务类型 |

## C 组：官方事实与用户描述不一致

| 编号 | 问题 | 依据 | 四值 | 需要的答复 |
| --- | --- | --- | --- | --- |
| Q-C01 | 原版 Java 版无 `/talk`，只有 `/say`（权限等级 2）；第 16 条「自动加入上say或talk」中的 talk 指什么 | docs/research/16-server-platform.md CM01-CM05 | 已证实 | 笔误 / 某插件命令 / 自定义别名 |
| Q-C02 | 第 5 条「输入 `/` 弹候选、输出不带 `/`」与服务端控制台命令一致；候选词表来源未定 | docs/research/16-server-platform.md CM03-CM06 | 未证实 | 内置词表 / 解析服务端帮助 / 用户自维护 |
| Q-C03 | 第 10 条 op 锁定：服务端启动后把 ops.json 读进内存，命令变更时整体回写；运行期手改文件会被静默覆盖，文件监听拿不到权威状态 | docs/research/16-server-platform.md OP01-OP06 | 已证实（冲突成立） | 走 `/op` `/deop` / RCON / 停服改文件 |
| Q-C04 | 第 14 条种子：新格式 `WorldGenSettings` 下的 `seed`，旧格式 `Data` 下的 `RandomSeed`，缺项默认 0；连写为路径记法，一手原文标签不连写；需两套读取 | docs/research/16-server-platform.md NB01-NB02、NB08 | 已证实 | 支持哪些 MC 版本段 |
| Q-C05 | 第 14 条要求用 nbt 能力，viaNBT 是 Java 8 库，与 Rust 集成方式未定（011 轮 Q08） | docs/research/15-input-survey.md VN05 | 未证实 | JNI / 子进程 / 改用 Rust NBT crate |
| Q-C06 | 第 18 条成就分析：进度存于 `world/players/advancements/<uuid>.json`，退出即写，读失败全丢；1.12.2 为 DataVersion 下限 | docs/research/16-server-platform.md NB03-NB04、NB07 | 已证实 | 最低支持 MC 版本 |
| Q-C07 | 第 27 条 PNG logo：官方为 64×64 `server-icon.png`，放服务端工作目录，需重启加载；「自动调整像素」的目标尺寸与比例策略 | docs/research/16-server-platform.md SI01-SI03 | 已证实 | 确认 64×64 / 保持比例 / 是否自动重启 |
| Q-C08 | 第 3 条 CurseForge 侧未找到与 Modrinth `environment` 等价的 server-only 字段 | docs/research/16-server-platform.md MS01-MS06 | 已证实 | 靠 category 启发式 / 仅用 Modrinth / 逐文件校验 |
| Q-C09 | 第 3 条「插件服官方下载通道忘了叫什么」：候选为 Hangar（PaperMC 官方）、Ore（Sponge 官方）、SpigotMC/BukkitDev、Modrinth；第 24 条已自行写出 Hangar / Ore | docs/research/16-server-platform.md HG01-HG11 | 已证实 | 选默认源与备选 |
| Q-C10 | Hangar REST 官方文档页被 robots 拒绝，API 基址仅有第三方转述；Ore `GET /api/projects` 有一手文档 | docs/research/16-server-platform.md HG04-HG08 | 受阻 | 是否接受先用 Ore + 后补 Hangar |
| Q-C11 | 第 7 条 EULA：官方页面为 `https://www.minecraft.net/en-us/eula`；`eula.txt` 首次启动生成，改 `eula=false` 为 `eula=true`，否则立即退出 | docs/research/16-server-platform.md EU01-EU06 | 已证实 | 软件内写入时机：启动前 / 首次启动后 |
| Q-C12 | 第 24 条 Java 多版本：Java 8 / 16 / 17 / 21 / 25 与 MC 版本段已查到；Java 自动下载的镜像源与分发条款未定 | docs/research/16-server-platform.md JV01-JV08 | 未证实 | 镜像地址与许可口径 |
| Q-C13 | 第 24 条 UPnP 自动映射：RFC 6886 记载 UPnP IGD 可被恶意网页改网关 DNS；NAT-PMP 已被 PCP（RFC 6887）取代 | docs/research/16-server-platform.md UP01-UP03 | 已证实 | 默认开 / 默认关 / 改 PCP |
| Q-C14 | 第 25 条代理端：Velocity 与 BungeeCord 插件 API 不兼容，安全转发能力不同 | docs/research/16-server-platform.md PX01-PX03 | 已证实 | 先支持哪一个 / 两个都做 |
| Q-C15 | 第 24 条 mclo.gs：`POST https://api.mclo.gs/1/log`，10 MiB / 25000 行上限；日志外传含玩家 IP、UUID、种子、聊天内容 | docs/research/16-server-platform.md MC01-MC04 | 已证实 | 是否允许外传 / 脱敏规则 / 二次确认 |

## D 组：设计口径未定

| 编号 | 问题 | 依据 | 四值 | 需要的答复 |
| --- | --- | --- | --- | --- |
| Q-D01 | 第 4 条 AI API「不赋予删除权限」：白名单 / 黑名单 / 能力令牌模型 | docs/spec/12-server-features-input.txt 第 4 条 | 未证实 | 三选一 |
| Q-D02 | 第 4 条「告诉对应的请求 ai 需要用户在本软件手动选择同意」与第 24 条「AI 请求待确认中心」：确认粒度是每次请求 / 每类操作 / 每个 AI 身份 | docs/spec/12-server-features-input.txt 第 4、24 条 | 未证实 | 确认粒度 |
| Q-D03 | 第 12 条「关窗口需保存进度才能关上」与第 15 条「强行锁定文件夹」：Windows 进程生命周期、真实文件锁与 UI 拦截的边界 | docs/spec/12-server-features-input.txt 第 12、15 条 | 未证实 | OS 锁 / UI 拦截 / 两者 |
| Q-D04 | 第 15 条 5 秒等待与「单次访问只弹一次，退出重进再弹」的状态存放位置 | docs/spec/12-server-features-input.txt 第 15 条 | 未证实 | 内存 / 实例配置 / 全局配置 |
| Q-D05 | 第 8 条「自动禁用低版本模组」的禁用方式：改扩展名 / 移到子目录 / 写 lockfile | docs/spec/12-server-features-input.txt 第 8 条 | 未证实 | 三选一 |
| Q-D06 | 第 9 条 FTP / SFTP 是客户端访问远程服，与本地实例管理是两套模型；是否并入开服器 | docs/spec/12-server-features-input.txt 第 9 条 | 未证实 | 保留 / 移到文件管理 / 独立模块 |
| Q-D07 | 第 9 条 SFTP 凭据、第 24 条 WebDAV / S3 云备份凭据，与 F012 凭据保护方案未批准 | docs/decisions/011-feature-input.md Q08；docs/features/credential-guard.md | 未证实 | 批准 F012 或给替代 |
| Q-D08 | 第 21 条「RCON 安全通道（仅本地/隧道）」的隧道形式、认证与既有 RCON 小端 / 4096 分片一手原文的对接 | docs/research/06-server.md；docs/spec/12-server-features-input.txt 第 21 条 | 未证实 | 隧道类型 |
| Q-D09 | 第 23 条默认配置汉化：server.properties 68 键已有一手原文，汉化表需人工翻译；「多实例同步」的冲突解决策略 | docs/research/06-server.md；docs/spec/12-server-features-input.txt 第 23 条 | 未证实 | 覆盖 / 合并 / 逐项确认 |
| Q-D10 | 第 24 条「按需启动 / 空闲休眠」与「进程守护 / 崩溃自动重启」互斥，优先级 | docs/spec/12-server-features-input.txt 第 24 条 | 已证实（冲突成立） | 优先级规则 |
| Q-D11 | 第 21 条「崩溃自动归因」的归因输入：退出码 / 日志模式 / crash-report / 混合 | docs/spec/12-server-features-input.txt 第 21 条 | 未证实 | 输入集合 |
| Q-D12 | 第 19 条命令黑名单与第 4 条 AI 权限、第 21 条审计日志是否共用一套策略引擎 | docs/spec/12-server-features-input.txt 第 4、19、21 条 | 未证实 | 共用 / 独立 |
| Q-D13 | 第 24 条「配置文件可视化编辑 + Schema 校验」与各加载器配置 schema 未证实（011 轮遗留） | docs/research/04-loaders.md；docs/research/index.md | 未证实 | 先做 server.properties / 等 schema 补证 |
| Q-D14 | 第 24 条「整合包导入导出（mrpack / CurseForge zip）」：mrpack 规范要求路径穿越防护与下载域名白名单 | docs/research/16-server-platform.md MS07-MS09 | 已证实 | 确认按规范实现 |
| Q-D15 | 第 25 条「多实例资源配额/调度」与 011 轮第 26 条「同时启动多个 MC 版本默认上限 3」是否共用上限 | docs/features/backlog.md 第 26 条 | 未证实 | 确认上限 |
| Q-D16 | 第 11 条开服文档：绑定域名、管理、更新的内容来源与语言 | docs/spec/12-server-features-input.txt 第 11 条 | 未证实 | 自写 / 外链 / 用户给稿 |
| Q-D17 | 第 6 条颜色标注 mod 名称的颜色规则与持久化位置 | docs/spec/12-server-features-input.txt 第 6 条 | 未证实 | 规则表 |
| Q-D18 | 第 2 条「允许选择多个加载器」：Fabric / Forge / NeoForge / Quilt 服务端与代理端组合兼容矩阵未证实 | docs/research/04-loaders.md | 未证实 | 允许的组合 |

## E 组：合规与安全

| 编号 | 问题 | 依据 | 四值 | 需要的答复 |
| --- | --- | --- | --- | --- |
| Q-E01 | CurseForge 第三方 API 条款 CF03 禁止缓存 API 数据，与 011 轮「跨实例共享模组缓存」「下载源测速与镜像切换」冲突 | docs/research/12-compliance.md CF03；docs/spec/12-server-features-input.txt 第 24 条 | 已证实（冲突成立） | 逐条处置 |
| Q-E02 | CF02 不得隐藏身份或地理位置、不得经代理/VPN，与 011 轮「6 个上游主机直连 403」及本轮「境外用官方源」冲突 | docs/research/12-compliance.md CF02；docs/spec/12-server-features-input.txt 第 2 条 | 已证实（冲突成立） | 逐条处置 |
| Q-E03 | CF01 唯一 API Key 不可共享，与「密钥可选」及特殊版私仓方案冲突 | docs/research/12-compliance.md CF01 | 已证实（冲突成立） | 逐条处置 |
| Q-E04 | CF04 竞争产品、CF05 配额书面许可、CF06 30 天无因终止 | docs/research/12-compliance.md CF04-CF06 | 未证实 | 条款解释来源 |
| Q-E05 | Modrinth ToS 已取得 4 条 API License 原文，缓存与限流条款页面未写明 | docs/research/12-compliance.md MR01-MR04 | 未证实 | 是否补一手 |
| Q-E06 | MCIM / BMCLAPI 条款 | docs/research/12-compliance.md | 未证实 | 是否补一手 |
| Q-E07 | mclo.gs 服务条款与日志保留期 | docs/research/16-server-platform.md MC03 | 未证实 | 是否补一手 |
| Q-E08 | Hangar / Ore / SpigotMC 的服务条款与速率限制 | docs/research/16-server-platform.md HG01-HG11 | 未证实 | 是否补一手 |
| Q-E09 | 正常模式 UI 设计稿品牌（FCL）与外部字体 CDN 授权 | docs/decisions/007-normal-ui.md | 未证实 | 替换 / 取得授权 / 停在资产层 |
| Q-E10 | 本项目 LICENSE 未生成；011 轮 D17 指定 GPLv3 | docs/research/15-input-survey.md OL03-OL07 | 未证实 | 确认并生成 |
| Q-E11 | CopperGolemLauncher 许可证全文已取得，复用范围未逐行判定 | docs/licenses/index.md L08 | 未证实 | 插件独立仓方案 |
| Q-E12 | 特殊版私仓未创建、CF 凭据未提供 | docs/decisions/011-feature-input.md D02-D03 | 未证实 | 创建条件 |

## F 组：平台与工具链

| 编号 | 问题 | 依据 | 四值 | 需要的答复 |
| --- | --- | --- | --- | --- |
| Q-F01 | Win7 兼容路径：Tier 3 `*-win7-windows-msvc` + build-std / VxKex / 固定旧版工具链 / 拆分产物 | docs/research/13-platform-api.md C01、RW05-RW12 | 已证实（冲突成立） | 四选一 |
| Q-F02 | 多架构范围：i686 / x86_64 / aarch64 候选；ARM64 Windows 最低 Win10 | docs/research/13-platform-api.md C02-C03、RW01-RW03 | 已证实（部分冲突） | 选定集合 |
| Q-F03 | Win7 + ARM64 同时支持 | docs/research/13-platform-api.md C04 | 已失败 | 放弃其一 |
| Q-F04 | 地域判定口径：物理位置或区域设置 | docs/research/13-platform-api.md P04-P07 | 未证实 | 二选一 |
| Q-F05 | `wProcessorArchitecture` 常量值与 ARM64 宿主区分方案 | docs/research/13-platform-api.md AR04-AR05 | 未证实 | 补一手或改用其他 API |
| Q-F06 | Win7 `SetDefaultDllDirectories` 需 KB2533623 与 `GetProcAddress` | docs/research/13-platform-api.md DL03-DL04 | 已证实 | 纳入构建约束 |
| Q-F07 | rustc / cargo 构建验证 | docs/verification/round-011.md | 受阻 | 提供环境或放宽 |
| Q-F08 | 浏览器内渲染实测 | docs/verification/round-011.md | 受阻 | 提供环境或放宽 |
| Q-F09 | git HTTP 推送受阻，仅 REST Git Data API 快照可用 | docs/rules/push-scope.md | 受阻 | 接受现状 |
| Q-F10 | 6 个上游主机直连、CF REST 端点页、CopperGolem latest release | docs/research/12-compliance.md；docs/research/16-server-platform.md HG05、MS06 | 受阻 | 接受现状或给镜像 |

## G 组：011 轮遗留未解决项

| 编号 | 问题 | 依据 | 四值 |
| --- | --- | --- | --- |
| Q-G01 | Notchian 服务端离线 UUID 行为 | docs/research/02-auth.md | 未证实 |
| Q-G02 | Mojang 官方 RCON 文档 | docs/research/06-server.md | 未证实 |
| Q-G03 | 加载器逐版本 schema | docs/research/04-loaders.md | 未证实 |
| Q-G04 | 令牌保护方案、Azure Client ID | docs/features/credential-guard.md | 未证实 |
| Q-G05 | CREATE_NO_WINDOW 具体值、std::process 超时 API、WebView2 内存占用关系、单文件发布工具链、多操作入口形式 | docs/research/11-runtime.md | 未证实 |
| Q-G06 | 文件管理开源骨干项目选定 | docs/research/15-input-survey.md DS06 | 未证实 |
| Q-G07 | viaNBT 与 Rust 集成方式 | docs/research/15-input-survey.md VN05 | 未证实 |
| Q-G08 | VxKex 对本项目产物链兼容范围 | docs/research/13-platform-api.md RW11 | 未证实 |
| Q-G09 | VxKex 是否随本项目分发 | docs/research/15-input-survey.md VK04 | 未证实 |
| Q-G10 | 陶瓦联机、atomgit 站点与 API | docs/research/15-input-survey.md | 未证实 |
| Q-G11 | viaNBT `LICENSE.txt` 全文 | docs/research/15-input-survey.md VN06 | 未证实 |
| Q-G12 | 008 验证报告 U8 锚点误差待复核 | docs/records/rounds.md 008 段 | 未证实 |
| Q-G13 | v99.99 同名同 sha tag | docs/research/12-compliance.md | 已失败 |
| Q-G14 | 本地提交链与远端 API 提交链哈希不同 | docs/records/rounds.md | 已失败 |

## H 组：开工闸门

| 编号 | 闸门 | 当前值 | 依据 |
| --- | --- | --- | --- |
| Q-H01 | D06 信号 | 未提供 | docs/decisions/003-remote.md D06 |
| Q-H02 | 005-blueprint.md 批准 | 未批准 | docs/decisions/005-blueprint.md |
| Q-H03 | X01-X04 逐条拍板 | 未拍板 | docs/research/12-compliance.md |
| Q-H04 | Q-A 至 Q-G 中标记「需要答复」的项 | 未答复 | 本文件 |
| Q-H05 | 触发链条件 5 | 未满足 | docs/rules/build-preconditions.md |
| Q-H06 | `src/` | 空 | `git ls-files src/` |

Q-H01 至 Q-H06 全部落定前不生成 Cargo.toml、build.rs、target spec、core 层代码。

## 计数

| 组 | 条数 |
| --- | --- |
| A | 6 |
| B | 12 |
| C | 15 |
| D | 18 |
| E | 12 |
| F | 10 |
| G | 14 |
| H | 6 |
| 合计 | 93 |

本文件为本轮全部待拍板项，无删减、无保留。用户当轮指令「全部告诉我不要保留」对应本文件与最终回复。

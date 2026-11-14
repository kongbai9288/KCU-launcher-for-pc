# 调研索引

检索日期：2026-11-05。每条事实带锚点与四值。四值定义见 docs/rules/proof-rules.md。

## 锚点规范

| 项 | 规则 |
| --- | --- |
| 格式 | 完整 URL、`path:line`、`cmd: <命令> → <输出>` |
| 禁止 | 重复引用、裸域名、短名、Markdown 链接、反引号包裹的 URL 片段 |
| 未证实项 | 锚点写来源线索或具体未取得项，不写推测的结论 |
| 受阻项 | 锚点写实际命令与返回码 |

## 文件

| 文件 | 主题 | 已证实 | 未证实 | 受阻 |
| --- | --- | --- | --- | --- |
| 01-hmcl.md | HMCL 结构、构建、许可证、上游版本 | 目录条目、settings.gradle.kts、LICENSE 全文与附加条款、v3.16.4 | 构建任务名、启动命令生成、版本清单解析、复用范围 | 无 |
| 02-auth.md | 登录与认证 | 设备码流、XBL/XSTS/MC 端点、离线 UUID 可复现算法与 v3/v4 一手锚点、authlib-injector 规范原文与路由、ALI 服务发现、Bearer 401 | Notchian 服务端采用离线 UUID 算法、Azure Client ID、旧 Mojang 账号、令牌保护、Xbox 端点一手原文 | 无 |
| 03-download.md | 官方与镜像下载 | Mojang manifest/libraries/assets、BMCLAPI 映射、MCIM 映射、Modrinth/CurseForge 头 | 官方必需请求头、v3 基址、MCIM 服务主体、BMCLAPI SLA | 6 个上游主机直连 403 |
| 04-loaders.md | 加载器 | Fabric Meta README 544 行、profile/json 与 server/json 端点、launcherMeta 字段、fabric-loader 0.20.1 | 逐加载器 version json 注入差异、Forge/NeoForge/Quilt/OptiFine schema | meta.fabricmc.net、meta.quiltmc.org、maven.neoforged.net 直连 403 |
| 05-rust-windows.md | Rust/Windows 运行时 | WebView2 检测键与 GUID、wry-v0.57.1、Rust 1.99.1、tao/egui/slint/iced 许可证、MAX_PATH | 最低 WebView2 版本、固定版本嵌入、Command 参数转义、本地库加载 | rustc/cargo 缺失、static.rust-lang.org 403 |
| 06-server.md | 服务端 | 68 键默认值、UTF-8 与 CRLF、RCON 包字段与认证、字节序、引入版本、分片上限、EULA | Mojang 官方 RCON 文档 | 无 |
| 07-lan.md | 局域网协议 | RFC 6762 / 6763 / 6455 原文 | Bonjour、HTTP 路由认证 TLS、二维码、发现端口 | 无 |
| 08-github-api.md | GitHub REST API | 请求头、两个版本实测 200、认证限流 5000、github/docs 原文 91 行、410 Gone | 未认证限流 60 数值 | docs.github.com 网页直抓 |
| 09-licenses.md | 许可证 | HMCL、wry、tao、egui、iced、authlib-injector、slint 清单、CC BY-SA 4.0 | Blessing Skin | 无 |
| 10-upstream-state.md | 时间、上游版本、网络边界、工具链 | 时钟一致、7 个上游 tag、api.github.com 200、6 个官方文档 200 | 无 | github.com 与 6 个上游主机 403、docs.github.com 与 wiki.vg 抓取、rustc/cargo 缺失 |
| 11-runtime.md | 底层运行时、裁剪、进程管理、本地库加载、单文件发布、玩家分支横评、多操作入口交互 | Cargo profile 默认值、DLL 搜索顺序与 LOAD_LIBRARY_SEARCH 标志、std::process::Command、CommandExt、WebView2 进程组、目标三元组、MSVC 三种部署 | CREATE_NO_WINDOW 具体值、std::process 超时 API、WebView2 内存占用关系、本项目单文件发布工具链、横评排名与开源状态、多操作入口具体形式 | 1 个 MSVC 部署首轮路径抓取被拒 |
| 12-compliance.md | 合规条款、凭据保护、许可证全文、上游版本、阻塞项 | CurseForge 6 条 API 条款、Modrinth 4 条 API License、DPAPI 与 CredWriteW 原文、6 份许可证全文、slint 三许可全文、6 个上游 release tag | CF04-CF06、MCIM / BMCLAPI 条款、Modrinth 缓存限流条款、加载器 schema、Notchian 行为、Forge / NeoForge v99.99 tag | MCIM 仓库定位 2 次 404、未认证 /rate_limit 404 |
| 13-platform-api.md | Win7 兼容、多架构、系统 API 真实签名 | VersionHelpers / GetNativeSystemInfo / GetUserGeoID / GetGeoInfoW / SYSGEOTYPE / GetGeoInfoEx / LOCALE_IGEOID / Rust Windows 目标 / Rust 1.78 变更 / Win7 Tier 3 目标 / SetDefaultDllDirectories 与 KB2533623 | wProcessorArchitecture 常量、Win7 物理位置 API、ARM64 Win7 目标、VxKex 兼容范围、Tier 3 可复现构建 | platform-support/windows.html 直抓 |
| 14-batch-network.md | 批量请求通用法、聚合搜索、本地监听 | N+1 反模式 8 条、Modrinth 批量 projects/versions 与 search limit<=100、CurseForge SDK 批量 modIds 与 pageSize=20、回环绑定 | 多源下载取消语义、翻译源接口、批量 ID 上限、端口清单 | CF REST 端点页 |
| 15-input-survey.md | 011 轮外部项目核实与只读仓 | 后端仓只读元数据、CopperGolemLauncher 许可证全文、PrismLauncher CMakeLists 存在性、ViaNBT / dsh / VxKex、开源许可页 5 字段 | CopperGolemLauncher 复用范围、ViaNBT 集成方式、文件管理骨干项目、陶瓦联机、atomgit | CF REST 端点页、CopperGolem latest release 404 |
| 16-server-platform.md | 012 轮开服器官方资料与协议 | Hangar / Ore / SpigotMC 插件源、Modrinth environment 10 值、mrpack 安全约束、EULA 与 eula.txt、`/say` 与 `/talk`、Java 8/16/17/21/25 映射、ops.json 运行期回写、种子双格式、进度存储、64×64 icon、TPS/MSPT、Velocity/BungeeCord、UPnP/NAT-PMP/PCP、mclo.gs | Hangar 官方 API 文档、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 日志外传条款、旧版 achievements | CF REST 端点页、Hangar API 页 robots 拒绝 |

## 来源类型

| 类型 | 示例 |
| --- | --- |
| 接口返回 | https://api.github.com/repos/HMCL-dev/HMCL/license、/releases/latest、/contents/、/tags |
| 官方文档 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution、https://docs.modrinth.com/api/ |
| 官方仓库 | https://github.com/FabricMC/fabric-meta、https://github.com/yushijinhun/authlib-injector |
| 协议规范 | https://www.rfc-editor.org/rfc/rfc6762、https://www.rfc-editor.org/rfc/rfc6763、https://www.rfc-editor.org/rfc/rfc6455 |
| 社区文档 | https://minecraft.wiki/w/Server.properties、https://minecraft.wiki/w/RCON |

## 005、008、009 与 010 卡点状态

| 001 轮遗留项 | 005 状态 | 008 状态 | 009 状态 | 010 状态 |
| --- | --- | --- | --- | --- |
| HMCL LICENSE 全文 | 已证实，docs/licenses/HMCL-LICENSE.txt | 已证实 | 已证实 | 已证实 |
| 加载器 version json schema | Fabric Meta README 已证实；其余未证实 | 未证实，未变动 | 未证实，未变动 | 二手线索已登记，仍未证实 |
| 离线 UUID 规则 | 算法已证实，Notchian 服务端行为未证实 | 算法补一手锚点已证实；Notchian 服务端行为未证实 | 未证实，未变动 | 社区线索已登记，仍未证实 |
| RCON 默认值 | 已证实，并纠正 broadcast-rcon-to-ops | 已证实 | 已证实 | 已证实 |
| RCON 字节序、引入版本、分片上限 | 降级为未证实 | 已证实，https://minecraft.wiki/w/RCON | 已证实 | 已证实 |
| WebView2 检测键 | 已证实 | 已证实 | 已证实 | 已证实 |
| docs.github.com 直抓 | 仍受阻；经 github/docs 仓库 API 取得一手原文 | 受阻，未变动 | 受阻，未变动 | 受阻，未变动 |
| authlib-injector wiki 直抓 | 已证实，经 GitHub contents API 取得 211 + 668 行原文 | 已证实 | 已证实 | 已证实 |
| 锚点格式不统一 | 10 份文档统一为 URL / path:line / cmd 输出 | 已证实 | 11 份文档统一，已证实 | 12 份文档统一，已证实 |
| 远程仓库创建 | 004 轮已完成 | 已证实 | 已证实 | 已证实 |
| 正常模式 UI | 未提供，未落盘 | 007 轮已落盘 assets/ui/normal-mode-v3.html；未实现、未进入构建 | 未实现，未进入构建 | 未实现，未进入构建 |
| 框架蓝图 | 方案已落盘，未批准 | 未批准，未变动 | 未批准，未变动 | 未批准，未变动 |
| slint 三许可全文 | 未证实 | 未证实，raw.githubusercontent.com 直抓受阻 | 未证实，未变动 | 已证实，docs/licenses/slint-LICENSES/ 3 份全文 |
| Mojang 官方 RCON 文档 | 未证实 | 未证实，未取得 | 未证实，未取得 | 未证实，未取得 |
| KCU 原仓库许可证 | 未证实 | 未证实 | 未证实 | 已证实，docs/licenses/KCU-Launcher-LICENSE.txt |
| CurseForge / Modrinth 服务条款 | 未证实 | 未证实 | 未证实 | 已证实，docs/research/12-compliance.md CF01-CF06 / MR01-MR04 |

## 009 新增调研项

| 需求条目 | 文档 | 状态 |
| --- | --- | --- |
| docs/spec/00-requirements.txt:229 底层运行时、裁剪工具、进程管理、单文件发布、本地库加载 | docs/research/11-runtime.md | 9 份一手原文已落盘；2 项未证实；1 项受阻 |
| docs/spec/00-requirements.txt:228 玩家分支启动器可取之处 | docs/research/11-runtime.md | 页面存在已证实；排名、星级、开源状态未证实；功能项候选未证实 |
| docs/spec/00-requirements.txt:231 电脑端多操作入口交互 | docs/research/11-runtime.md | 具体形式未证实，思路保留 |

## 010 新增调研项

| 需求条目 | 文档 | 状态 |
| --- | --- | --- |
| docs/spec/00-requirements.txt:17 正版凭据保护机制 | docs/research/12-compliance.md、docs/features/credential-guard.md | DPAPI 与 CredWriteW 原文已证实；方案未批准、未实现 |
| docs/spec/00-requirements.txt:171-173 镜像与密钥 | docs/research/12-compliance.md | X01-X04 四项冲突已证实，见 docs/rules/build-preconditions.md |
| docs/spec/00-requirements.txt:230 每轮联网核实现有时间与上游版本状态 | docs/research/12-compliance.md | 6 个 release tag 已证实；2 个 v99.99 tag 已失败 |
| docs/spec/00-requirements.txt:228 玩家分支启动器可取之处 | docs/research/12-compliance.md | 两个一手仓库许可证与 README 已证实；功能清单未证实 |
| docs/spec/00-requirements.txt:249 合规优先于功能进度 | docs/rules/build-preconditions.md | 前置条件清单已落盘，待用户拍板 |

## 011 卡点状态

| 项 | 010 状态 | 011 状态 |
| --- | --- | --- |
| D06 信号 | 未提供 | 未提供，用户写明后续还会给要求 |
| 005-blueprint.md | 未批准 | 未批准 |
| X01-X04 | 已证实，待拍板 | 密钥共享方向已给出；CF03 / CF02 / CF01 仍待逐条拍板 |
| 正常模式 UI 授权 | 未证实 | 未证实 |
| slint 三许可全文 | 已证实 | 已证实 |
| 加载器逐版本 schema | 未证实 | 未证实 |
| Notchian 服务端行为 | 未证实 | 未证实 |
| Mojang 官方 RCON 文档 | 未证实 | 未证实 |
| 锚点格式 | 12 份文档统一 | 15 份文档统一，已证实 |
| Win7 兼容 | 未登记 | 已证实为硬冲突，见 13-platform-api.md C01-C04 |
| Win7 + ARM64 | 未登记 | 已失败 |
| 地域判定口径 | 未登记 | 未证实，物理位置与区域设置语义不同 |
| CF / Modrinth 服务条款 | 已证实 | 已证实 |
| 后端仓 | 未登记 | 只读，4 个 GET，已证实 |

## 011 新增调研项

| 需求条目 | 文档 | 状态 |
| --- | --- | --- |
| docs/spec/11-round-011-instructions.txt 系统 API 真实签名、Win7 兼容、多架构 | docs/research/13-platform-api.md | 12 组一手原文；Win7 与 Rust Tier 1 冲突已证实；ARM64 与 Win7 交集已失败 |
| docs/spec/11-round-011-instructions.txt 网络通用法、逐条目单发请求浪费 | docs/research/14-batch-network.md | N+1 反模式 8 条 + 4 个官方批量端点；禁止逐条目单发 |
| docs/spec/11-features-input.txt 全量功能输入 | docs/features/backlog.md | 55 条编号 + 175 项文件管理清单逐字落盘 |
| docs/spec/11-features-input.txt 第 46、54、6 条与开头段 | docs/research/15-input-survey.md | 外部项目许可证与只读仓已核 |
| docs/spec/00-requirements.txt:230 每轮核上游版本 | docs/research/13-platform-api.md RW07 | Rust 1.99.1、HMCL v3.16.4 已证实 |

## 012 卡点状态

| 项 | 011 状态 | 012 状态 |
| --- | --- | --- |
| D06 信号 | 未提供 | 未提供，用户仍给开服器输入 |
| 005-blueprint.md | 未批准 | 未批准 |
| X01-X04 | 待拍板 | 待拍板，本轮新增 CF 相关冲突 Q-E01 至 Q-E03 |
| 正常模式 UI 授权 | 未证实 | 未证实 |
| 加载器逐版本 schema | 未证实 | 未证实 |
| Notchian 服务端行为 | 未证实 | 未证实 |
| 锚点格式 | 15 份统一 | 16 份统一，已证实 |
| 后端仓只读 | 4 个 GET | 012 轮 0 个写请求，约束延续 |
| 插件服官方通道 | 未登记 | 候选 4 类已证实，默认源未选 |
| 开工闸门 | 条件 1-5 | 条件 1-6，见 build-preconditions.md |
| 待拍板问题 | 未建全集 | docs/records/open-questions.md 93 条 |

## 012 新增调研项

| 需求条目 | 文档 | 状态 |
| --- | --- | --- |
| docs/spec/12-server-features-input.txt 第 3 条插件服官方下载通道 | docs/research/16-server-platform.md HG01-HG11 | 4 类候选已证实；默认源未选 |
| docs/spec/12-server-features-input.txt 第 3 条服务端 mod 声明 | docs/research/16-server-platform.md MS01-MS09 | Modrinth `environment` 10 值已证实；CF 等价字段未证实 |
| docs/spec/12-round-012-instructions.txt「搜完所有的文档」 | docs/research/16-server-platform.md P54-P79 | 26 个来源，2 个受阻 |
| docs/spec/12-round-012-instructions.txt「问题全部告诉我不要保留」 | docs/records/open-questions.md | 93 条，A-H 组 |

## 禁止项

| 编号 | 内容 |
| --- | --- |
| R01 | 未取得 LICENSE 全文前不复制对应组件代码、资源、商标、Client ID。 |
| R02 | 镜像响应不作为官方源、稳定源或授权分发源。 |
| R03 | 未证实字段不写进实现。 |
| R04 | 四值只用已证实 / 已失败 / 未证实 / 受阻；中间态禁用。 |
| R05 | 403 policy_default_denied 记为受阻，不记为上游服务异常。 |

## 020 统一调研

| 项 | 文档 | 状态 |
| --- | --- | --- |
| 插件槽位、设置架构、插件化更新、服务器状态、上层候选许可 | docs/research/17-plugin-settings-survey.md | 12 一手 + 4 公开资料 + 3 受阻，全部完整 URL 锚点 |
| 结论 J01-J06 | docs/research/17-plugin-settings-survey.md | 只供设计层使用，020 轮 `src/` 无变化 |

## 021 服务器列表自动发现

| 项 | 文档 | 状态 |
| --- | --- | --- |
| servers.dat NBT 结构、可见 / 隐藏两份列表、原版四元素与 ping 分档、SLP 字段、社区启动器事例 | docs/research/18-server-list-autodiscovery.md | 9 一手来源 + 8 组公开资料，完整 URL 锚点 |
| 结论 J01-J07 | docs/research/18-server-list-autodiscovery.md | 只供设计层；020 的 server-status.md 页面口径已被取代 |

## 022 异步探测与连接预算

| 项 | 文档 | 状态 |
| --- | --- | --- |
| 并行探测 API、context deadline、启动器异步 ping、背压 / 有界队列 / 连接池上限 / 失败不毁整批 | docs/research/19-async-probe-budget.md | 12 个完整 URL 锚点，J01-J07 结论 |
| Q01-Q04 口径说明 | docs/research/19-async-probe-budget.md | 自主拍板，待用户确认，只落 docs/ |

## 023 i18n / 崩溃 / 稳定标识 / 兼容性

| 项 | 文档 | 状态 |
| --- | --- | --- |
| 18 个完整 URL 锚点、J01-J07 结论、Q01-Q04 口径说明 | docs/research/20-i18n-crash-identity.md | 一手 15 组 + 公开资料 6 组 |
| Fluent / i18n-embed / Sentry SDK / minidump / Breakpad / Win7 Tier 3 / servers.dat 无 ID 字段 | docs/research/20-i18n-crash-identity.md | 已证实 |

## 028 轮新增

| 编号 | 文档 | 来源数 | 主题 |
| --- | --- | --- | --- |
| R20 | 20-server-log-events.md | 15 条来源 / 13 个独立 URL | 日志格式、实时读取、声明式正则、PlayerJoinEvent、活跃度饼图、脱敏约束 |

## 029 轮新增

| 编号 | 文档 | 主题 |
| --- | --- | --- |
| R21 | 029-cache-lru.md 的 T01-T04 / C01-C04 | 缓存库依赖闭包与 Send/Sync 的源码级核查 |

完整 URL：

- https://github.com/jeromefroe/lru-rs/tree/0.12.5
- https://api.github.com/repos/jeromefroe/lru-rs/contents/Cargo.toml?ref=0.12.5
- https://codeload.github.com/jeromefroe/lru-rs/tar.gz/refs/tags/0.12.5
- https://github.com/moka-rs/mini-moka/tree/v0.10.3
- https://github.com/arthurprs/quick-cache/tree/v0.6.18
- https://github.com/contain-rs/linked-hash-map/tree/v0.5.6
- https://api.github.com/repos/jeromefroe/lru-rs/tags?per_page=20

## 030 轮新增

| 编号 | 文档 | 主题 |
| --- | --- | --- |
| R22 | q028-decision-scenarios.md | 日志命令文字触发的授权粒度与动作分级场景 |

完整 URL：

- https://github.com/blyxxyz/lexopt/tree/v0.3.2
- https://api.github.com/repos/blyxxyz/lexopt/contents/Cargo.toml?ref=v0.3.2
- https://codeload.github.com/blyxxyz/lexopt/tar.gz/refs/tags/v0.3.2
- https://api.github.com/repos/blyxxyz/lexopt/tags?per_page=15

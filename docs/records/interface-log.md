# 接口更新记录

更新轮次：011

## 前置索引

| 编号 | 接口 | 文档 | 状态 |
| --- | --- | --- | --- |
| I01 | HMCL 源码与许可证 | docs/research/01-hmcl.md | LICENSE 全文已证实 |
| I02 | Microsoft / Xbox / Minecraft Services / Yggdrasil | docs/research/02-auth.md | authlib-injector 规范原文与离线 UUID v3/v4 一手锚点已证实；Notchian 服务端行为未证实 |
| I03 | Mojang / BMCLAPI / MCIM / Modrinth / CurseForge | docs/research/03-download.md | 6 个上游主机直连受阻 |
| I04 | Forge / NeoForge / Fabric / Quilt / OptiFine | docs/research/04-loaders.md | Fabric Meta README 已证实；其余 schema 未证实 |
| I05 | wry / WebView2 / Win32 / Rust std | docs/research/05-rust-windows.md | WebView2 检测键已证实；rustc/cargo 受阻 |
| I06 | Paper / server.properties / RCON | docs/research/06-server.md | 68 键默认值、字节序、引入版本、分片上限已证实；Mojang 官方 RCON 文档未证实 |
| I07 | mDNS / DNS-SD / WebSocket / 二维码 | docs/research/07-lan.md | RFC 6762 / 6763 / 6455 已证实 |
| I08 | api.github.com | docs/research/08-github-api.md | 已证实 |
| I09 | 第三方许可证 | docs/research/09-licenses.md、docs/licenses/index.md、docs/research/12-compliance.md | 17 份逐字副本已证实，含 slint 三许可全文；Blessing Skin 未证实 |
| I10 | 时间、上游版本、网络边界 | docs/research/10-upstream-state.md | 005 轮新增 |
| I11 | 正常模式 UI 设计稿 | assets/ui/index.md、docs/features/normal-ui.md | 已落盘，授权未证实 |
| I12 | RCON 与 UUID 一手补证 | docs/research/06-server.md、docs/research/02-auth.md | 008 轮新增，见 008 新增来源 |
| I13 | Cargo profile / Win32 DLL 搜索 / std::process / WebView2 进程组 / MSVC 部署 / 目标三元组 | docs/research/11-runtime.md | 009 轮新增，9 份一手原文；2 项未证实；1 项受阻 |
| I14 | CurseForge / Modrinth API 条款、DPAPI / CredWriteW、6 份许可证全文、slint 三许可、上游版本状态 | docs/research/12-compliance.md | 010 轮新增，见 010 新增来源；X01-X04 冲突已证实 |
| I15 | Win32 版本/架构/地理位置 API、Rust Windows 目标与 Win7 Tier 3、DLL 加载边界 | docs/research/13-platform-api.md | 011 轮新增，见 011 新增来源；C01-C04 冲突已证实 |
| I16 | 批量端点、N+1 反模式、回环监听、配置集中 | docs/research/14-batch-network.md | 011 轮新增；CF REST 端点页受阻 |
| I17 | 只读后端仓、CopperGolemLauncher、ViaNBT、dsh、VxKex、开源许可页 5 字段 | docs/research/15-input-survey.md | 011 轮新增；仅 4 个 GET |

## 连接约定

| 接口 | 必需头 | 基址配置 |
| --- | --- | --- |
| api.github.com | `User-Agent`、`Accept: application/vnd.github+json`、`X-GitHub-Api-Version` | 单一配置项 |
| api.github.com 认证 | `Authorization: token <env>`；Bearer 对 GET /user 返回 403 | 环境变量 |
| Modrinth | 唯一可识别 `User-Agent`；写操作 `Authorization` | 单一基础地址配置项 |
| CurseForge | `x-api-key` | 默认镜像，密钥可选 |
| MCIM | 缓存头 `sync_at`；可能要求提交启动器 UA | 镜像基址配置项 |
| RCON | 无 HTTP 头；小端包 | 端口配置项 |
| server.properties | 无 HTTP 头；UTF-8，CRLF on Windows | 文件路径配置项 |
| Win32 DLL 加载 | 无 HTTP 头；SetDefaultDllDirectories + LOAD_LIBRARY_SEARCH_DEFAULT_DIRS | 应用目录配置项 |
| std::process | 无 HTTP 头；args_os 参数，不经 cmd.exe / .bat | 可执行文件配置项 |
| WebView2 进程组 | 无 HTTP 头；单 user data folder 对应单进程集合 | user data folder 配置项 |

## 同步上游

| 项 | 同步内容 |
| --- | --- |
| 版本清单 | piston-meta.mojang.com manifest_v2 |
| libraries/assets | libraries.minecraft.net、resources.download.minecraft.net |
| Java 运行时 | launchermeta.mojang.com java-runtime all.json |
| Mod 元数据 | Modrinth / CurseForge / MCIM |
| 许可证全文 | `GET /repos/{owner}/{repo}/license`、`/contents/{path}` |
| 上游版本 | `GET /repos/{owner}/{repo}/releases/latest`、`/tags?per_page=1` |

## 005 新增来源

| 编号 | 来源 | 用途 | 状态码 |
| --- | --- | --- | --- |
| S01 | https://api.github.com/repos/HMCL-dev/HMCL/license | GPLv3 + 附加条款全文 | 200 |
| S02 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src/zh/ | Yggdrasil 与启动器规范 | 200 |
| S03 | https://api.github.com/repos/FabricMC/fabric-meta/contents/README.md | profile/json 端点与 launcherMeta | 200 |
| S04 | https://api.github.com/repos/github/docs/contents/content/rest/about-the-rest-api/api-versions.md | 410 Gone 与版本头 | 200 |
| S05 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution | WebView2 pv 检测键 | 200 |
| S06 | https://minecraft.wiki/w/Server.properties | 68 键默认值与编码 | 200 |
| S07 | https://minecraft.wiki/w/RCON | RCON 包字段与认证 | 200 |
| S08 | https://www.rfc-editor.org/rfc/rfc6762 | mDNS UDP 5353 与组播地址 | 200 |
| S09 | https://www.rfc-editor.org/rfc/rfc6763 | DNS-SD PTR / SRV / TXT | 200 |
| S10 | https://www.rfc-editor.org/rfc/rfc6455 | WebSocket Upgrade 握手 | 200 |
| S11 | /data/inputs/FCL揉纸启动器-桌面端-v3(1).txt | 正常模式 UI 逐字副本与结构登记 | 文件，172759 字节 |
| S12 | https://miaoda.feishu.cn/fonts/css2 | 设计稿外部字体 CSS | 服务条款未取得 |

## 008 新增来源

| 编号 | 来源 | 用途 | 状态码 |
| --- | --- | --- | --- |
| S13 | https://minecraft.wiki/w/RCON | 字节序、引入版本、分片上限、认证失败 | 200 |
| S14 | https://minecraft.wiki/w/Universally_unique_identifier | 离线 UUID v3、在线 UUID v4 | 200 |
| S15 | https://raw.githubusercontent.com/slint-ui/slint/master/LICENSE.md | slint 三许可全文 | 受阻 |

## 009 新增来源

| 编号 | 来源 | 用途 | 状态码 |
| --- | --- | --- | --- |
| S16 | https://doc.rust-lang.org/cargo/reference/profiles.html | Cargo profile 默认值 | 200 |
| S17 | https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order | DLL 搜索顺序与预加载攻击 | 200 |
| S18 | https://msdn.microsoft.com/zh-tw/windows/apps/ms682586 | LOAD_LIBRARY_SEARCH 中文原文 | 200 |
| S19 | https://technet.microsoft.com/en-us/office/hh310515 | SetDefaultDllDirectories 标志与最低系统 | 200 |
| S20 | https://doc.rust-lang.org/std/process/struct.Command.html | 进程创建与参数 | 200 |
| S21 | https://doc.rust-lang.org/std/os/windows/process/trait.CommandExt.html | Windows CommandExt | 200 |
| S22 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/process-model | WebView2 进程组 | 200 |
| S23 | https://doc.rust-lang.org/rustc/platform-support.html | 目标三元组与 tier | 200 |
| S24 | https://learn.microsoft.com/en-us/cpp/windows/deployment-in-visual-cpp | MSVC 三种部署 | 200 |
| S25 | https://pcl2.ijinshan.com/pages/concepts/minecraft-launchers/ | 第三方横评，标推广措辞 | 200 |
| S26 | https://learn.microsoft.com/en-us/cpp/windows/deploying-visual-cpp-applications | MSVC 部署首轮路径 | 受阻 |

## 010 新增来源

| 编号 | 来源 | 用途 | 状态码 |
| --- | --- | --- | --- |
| S27 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions | CurseForge API 条款 CF01-CF06 | 200 |
| S28 | https://modrinth.com/legal/terms | Modrinth API License MR01-MR04 | 200 |
| S29 | https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata | DPAPI 原文 | 200 |
| S30 | https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credwritew | CredWriteW 原文 | 200 |
| S31 | https://learn.microsoft.com/en-us/windows/win32/secauthn/credential-manager | 凭据管理器提供程序页面 | 200 |
| S32 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES | slint 20 个许可条目与 3 份三许可全文 | 200 |
| S33 | https://api.github.com/repos/kongbai9288/KCU-Launcher/contents/LICENSE 等 6 个 contents 端点 | 6 份许可证逐字副本 | 200 |
| S34 | https://deepwiki.com/ElectronicWave/Elemental/5.2-mod-discovery-system | 加载器 schema 二手线索 | 200 |
| S35 | https://minecraftserver.buzz/minecraft-offline-uuid-generator | 离线 UUID 社区线索 | 200 |
| S36 | https://prismlauncher.org/wiki/getting-started/create-instance/ | Prism 实例创建流程 | 200 |
| S37 | https://api.github.com/repos/Glavo/MCIM、/repos/mcim-api/mcim-api | MCIM 仓库定位 | 受阻，404 |

## 合规冲突登记

| 编号 | 条款 | 现有登记 | 状态 |
| --- | --- | --- | --- |
| X01 | CF03 不得缓存 API 数据 | docs/research/03-download.md 缓存头 sync_at | 已证实 |
| X02 | CF03 不得缓存 API 数据 | docs/spec/00-requirements.txt:172 默认走国内镜像 | 已证实 |
| X03 | CF02 不得隐藏身份或地理位置 | docs/research/03-download.md 6 个上游主机直连 403 | 已证实 |
| X04 | CF01 API Key 不可共享 | docs/spec/00-requirements.txt:171 密钥可选 | 已证实 |

处置见 docs/rules/build-preconditions.md；未取得用户拍板前不生成下载模块代码。

## 011 新增来源

| 编号 | 来源 | 用途 | 状态码 |
| --- | --- | --- | --- |
| S38 | https://learn.microsoft.com/en-us/windows/win32/api/versionhelpers/nf-versionhelpers-iswindows7orgreater | 版本判定 | 200 |
| S39 | https://learn.microsoft.com/zh-cn/windows/desktop/SysInfo/targeting-your-application-at-windows-8-1 | GetVersionEx 弃用 | 200 |
| S40 | https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getnativesysteminfo | 架构判定 | 200 |
| S41 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getusergeoid | 本地地理位置 | 200 |
| S42 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getgeoinfow | GetGeoInfoW | 200 |
| S43 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/ne-winnls-sysgeotype | SYSGEOTYPE | 200 |
| S44 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getgeoinfoex | Win10 1709 限定 | 200 |
| S45 | https://learn.microsoft.com/en-us/windows/win32/intl/locale-igeoid | LOCALE_IGEOID | 200 |
| S46 | https://support.microsoft.com/zh-cn/windows/windows-位置服务和隐私 | 定位服务输入源 | 200 |
| S47 | https://doc.rust-lang.org/rustc/platform-support.html | Windows 目标最低版本 | 200 |
| S48 | https://doc.rust-lang.org/releases.html | Rust 1.78 目标变更 | 200 |
| S49 | https://doc.rust-lang.net.cn/1.85.0/rustc/platform-support/win7-windows-msvc.html | Win7 Tier 3 目标 | 200 |
| S50 | https://vxkex.com/ | VxKex | 200 |
| S51 | https://vibgrate.com/anti-patterns/n-plus-one-network-calls | N+1 反模式通用法 | 200 |
| S52 | https://docs.modrinth.com/api/operations/getprojects/ | 批量 projects | 200 |
| S53 | https://docs.modrinth.com/api/operations/getversions/ | 批量 versions | 200 |
| S54 | https://docs.modrinth.com/api/operations/searchprojects/ | 分页与 facets | 200 |
| S55 | https://docs.curseforge.com/docs/game-integration/unreal/browsing-and-discovery | CF 批量 SDK 与 pageSize=20 | 200 |
| S56 | https://pypi.org/project/curse-api/ | 第三方批量封装 | 200 |
| S57 | https://docs.curseforge.com/rest-api/endpoint/POST_1_mods/ | CF REST 端点页 | 受阻 |
| S58 | https://blog.g5cybersecurity.com/?p=178654/ | 回环绑定 | 200 |
| S59 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher/contents/LICENSE | 许可证全文 | 200 |
| S60 | https://github.com/ViaVersion/ViaNBT | MIT / Java 8 / NBT | 200 |
| S61 | https://awesome-dsh-plugin.com/p/chumoe/dsh-file-manager | dsh 文件管理插件 | 200 |
| S62 | https://api.github.com/repos/kongbai9288/modmarket-backend 等 4 个端点 | 只读元数据 | 200，仅 GET |

## 011 只读仓约束

| 编号 | 内容 |
| --- | --- |
| RO01 | 对用户后端仓只允许 `GET`，本轮 4 个 `GET`、0 个写请求。 |
| RO02 | 端点、密钥、部署配置、README 正文不复制进本公仓。 |
| RO03 | 不 fork、不改分支、不建 issue、不触发自动部署。 |

## 版本弃用

| 接口 | 行为 |
| --- | --- |
| Modrinth 旧版本 | 完全弃用后永久 410 |
| GitHub REST API | 2022-11-28 支持至 2028-03-10；不再支持的版本返回 410 |
| 破坏性变更 | 升版本号并给迁移步骤 |

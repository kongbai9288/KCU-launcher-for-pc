# 接口更新记录

更新轮次：019

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
| I18 | 开服器插件源、服务端 mod 声明、EULA、原版命令、Java 版本映射、ops.json、种子 NBT、server-icon、TPS、代理端、UPnP、mclo.gs | docs/research/16-server-platform.md | 012 轮新增；26 个来源，2 个受阻 |
| I19 | 腾讯 rustup 镜像、rustc/cargo stable、L1 core 模块内部接口 | docs/decisions/013-build-start.md、src/core/ | 013 轮新增；镜像 200，官方分发主机 403 |

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

## 012 新增来源

| 编号 | 来源 | 用途 | 结果 |
| --- | --- | --- | --- |
| S63 | https://hangar.papermc.io/?page=0&platform=VELOCITY | Hangar 官方插件仓库 | 200 |
| S64 | https://papermc.io/ | PaperMC / Hangar / Folia / Velocity | 200 |
| S65 | https://www.eranio.com/docs/api/mp-hangar | Hangar API 基址第三方转述 | 200 |
| S66 | https://hangar.papermc.io/api/v1 | Hangar 官方 API 文档 | 受阻，robots 拒绝 |
| S67 | https://www.g-portal.com/wiki/en?p=4679 | 四类插件源分工 | 200 |
| S68 | https://docs.papermc.io/misc/hangar-publishing | Hangar API token 与权限 | 200 |
| S69 | https://docs.spongepowered.org/6.0.0/en/ore/routes/list-projects.html | Ore Web API | 200 |
| S70 | https://docs.modrinth.com/api/operations/searchprojects/ | environment 10 值 | 200 |
| S71 | https://docs.modrinth.com/api/operations/getproject/ | client_side / server_side 弃用 | 200 |
| S72 | https://support.modrinth.com/en/articles/8802351-modrinth-modpack-format-mrpack | mrpack 格式与安全约束 | 200 |
| S73 | https://xmcl.app/en/core/curseforge/SearchOptions | CF classId / categoryId / modLoaderType | 200 |
| S74 | https://docs.curseforge.com/rest-api/endpoint/POST_1_mods/ | CF 官方 REST 端点页 | 受阻 |
| S75 | https://www.minecraft.net/en-us/eula | 官方 EULA 页面 | 200 |
| S76 | https://minecraft.wiki/w/Tutorial:Setting_up_a_Java_Edition_server | eula.txt、`java -jar --nogui`、`/op` | 200 |
| S77 | https://minecraft.wiki/w/Commands/say | `/say` 与 `/talk` | 200 |
| S78 | https://zh.minecraft.wiki/w/Tutorial:取得遊戲 | Java 版本映射 | 200 |
| S79 | https://minecraft.wiki/w/Tutorial:Required_Java_versions | 英文 Java 版本口径 | 200 |
| S80 | https://renode.space/blog/minecraft-ops-json-whitelist-json-explained | ops.json 运行期回写 | 200 |
| S81 | https://zh.minecraft.wiki/w/Level.dat_old | 种子双格式 | 200 |
| S82 | https://zh.minecraft.wiki/w/进度存储格式 | advancements 存储 | 200 |
| S83 | https://api.mclo.gs/ | 日志上传端点 | 200 |
| S84 | https://minecraft.wiki/w/Server_List | 64×64 server-icon.png | 200 |
| S85 | https://www.spigotmc.org/wiki/server-icon/ | 图标重启加载 | 200 |
| S86 | https://minecrafthub.io/articles/what-is-tps-in-minecraft | TPS / MSPT | 200 |
| S87 | https://docs.papermc.io/velocity/comparisons-to-other-proxies/ | Velocity / BungeeCord 差异 | 200 |
| S88 | https://rfc-editor.org/rfc/rfc6886 | NAT-PMP / PCP / UPnP IGD 风险 | 200 |

## 012 只读仓约束

| 编号 | 内容 |
| --- | --- |
| RO04 | 延续 011 轮 RO01-RO03；本轮对用户后端仓 0 个写请求。 |
| RO05 | 012 轮新增的 FTP / SFTP、WebDAV / S3、mclo.gs 均为候选目标，凭据存放位置未定，见 docs/records/open-questions.md Q-D07。 |

## 013 工具链来源

| 编号 | 来源 | 用途 | 结果 |
| --- | --- | --- | --- |
| S89 | https://mirrors.cloud.tencent.com/rustup/dist/channel-rust-stable.toml | RUSTUP_DIST_SERVER | 200 |
| S90 | https://mirrors.cloud.tencent.com/rustup/rustup/dist/x86_64-unknown-linux-gnu/rustup-init | rustup-init 二进制 | 200，21M |
| S91 | https://mirrors.tencent.com/rustup/dist/channel-rust-stable.toml | 备用镜像 | 200 |
| S92 | https://mirrors.aliyun.com/rustup/dist/channel-rust-stable.toml | 对照 | 403 |
| S93 | https://static.rust-lang.org/dist/channel-rust-stable.toml | 官方分发主机 | 403 |
| S94 | https://api.github.com/repos/rust-lang/rust/releases/latest | release 元数据 | 200 |

| 编号 | 内容 |
| --- | --- |
| RO06 | 013 轮对后端仓 0 个写请求，约束延续 RO01-RO05。 |
| RO07 | 工具链装在仓库外 `/data/workspace/.cargo-home` 与 `/data/workspace/.rustup-home`，不进公仓。 |
| RO08 | CORRECTION：GitHub Actions 不向本地沙盒分发工具链；api.github.com 只取元数据；实际安装路径为腾讯 rustup 镜像。 |

## 014 端点、私仓与 CI 来源

| 编号 | 来源 | 用途 | 结果 |
| --- | --- | --- | --- |
| S95 | https://api.github.com/user | 认证核对 | 200 login=kongbai9288 |
| S96 | https://api.github.com/user/repos | 同名仓检查 | 200，23 仓，无同名 |
| S97 | https://api.github.com/user/repos（POST，private:true） | 特殊版私仓创建 | 201，private=True |
| S98 | https://api.github.com/repos/kongbai9288/KCU-launcher-special/contents/README.md（PUT） | 私仓初始化 | 201，`cd7fc97` |
| S99 | https://mirrors.cloud.tencent.com/rustup | CI `RUSTUP_DIST_SERVER` | 013 轮实测 200 |
| S100 | https://mirrors.cloud.tencent.com/rustup/rustup | CI `RUSTUP_UPDATE_ROOT` | 013 轮实测 200 |

| 编号 | 内容 |
| --- | --- |
| I20 | 014 轮工作流环境变量占位：`KCU_CF_API_KEY`（secrets）、`KCU_MIRROR_BASE` / `KCU_BACKEND_BASE` / `KCU_LANG_PACK_BASE` / `KCU_DOWNLOAD_REGION`（vars）。值由用户填写，仓库零字面量。 |
| I21 | 014 轮 core 内部接口：`Cache::get_or_load`、`TaskGroup::spawn/shutdown`、`race`、`Tracker::track`、`WeakRegistry::insert/get/purge`，见 docs/features/core-*.md。 |
| RO09 | 014 轮对后端仓 0 个写请求，约束延续 RO01-RO08。 |
| RO10 | 私仓仅 README 占位；代码、凭据、后端仓内容均未放入。 |
| RO11 | `env-presence` 步骤只输出 present / absent，不输出值。 |

CORRECTION：013 轮记录的「GitHub Actions 不向本地沙盒分发工具链」仍成立；014 轮把 GitHub Actions 用于 CI 内构建，工具链在 runner 上按腾讯 rustup 镜像安装，不向本地沙盒分发，两条口径不冲突。

## 015 L2 dispatcher 内部接口

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I22 | `dispatcher::json::parse` | &str | dispatcher.json.Json | 含字节位置的 String |
| I23 | `dispatcher::task::LaunchTask::{from_json,from_str,from_args}` | Json / &str / &LaunchArgs | LaunchTask | String |
| I24 | `dispatcher::task::TaskSet::{from_values,from_texts,pick}` | Json 集合 / 文本集合 / &LaunchArgs | TaskSet / LaunchTask | String |
| I25 | `dispatcher::mode::ModeSelector::{select,safe}` | &ModeInput | Result<ModeSelection,String> / ModeSelection | 非法模式含来源 |
| I26 | `dispatcher::launcher::Dispatcher::dispatch` | &DispatchInput, &CancelToken | LaunchOutcome | 错误进信封与诊断，不 panic |
| I27 | `Dispatcher::{reset,flush_diagnostics}` | 无 | () / Vec<Vec<String>> | 无 |

| 编号 | 内容 |
| --- | --- |
| RO12 | 015 轮对后端仓 0 个写请求，约束延续 RO01-RO10。 |
| RO13 | 015 轮未调用任何远端服务接口，未新增外部 API；CF 具体调用方法仍按 F17 由用户在完成时提供。 |
| RO14 | 整页 UI 演示闸门登记在 docs/rules/ui-demo.md；本轮不触发，未生成 ui-full 文件。 |
| RO15 | Cargo.toml / Cargo.lock 未变，无新增 crate；`serde` / `tokio` / `async-std` 计数为 0。 |

## 016 L3 lightweight 内部接口

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I28 | `lightweight::login::LoginSession::{new,advance}` | AuthKind / StageAvailability / CancelToken / 连接码 | Result<LoginStage,LoginError> | Cancelled / Timeout / ZeroLevel |
| I29 | `lightweight::download::Downloader::{new,batch,reset,cf_source_exposed}` | ProviderConfig / &[String] / CancelToken | BatchReply / () / bool | String |
| I30 | `lightweight::loaders::LoaderRegistry::{register,install,version_json_fields,schema_patch}` | LoaderKind / CancelToken | bool / InstallOutcome / Vec / Option | 不写 schema |
| I31 | `lightweight::view::LightweightView::{handle,flow,close_all_popups,envelope}` | ViewAction / AuthKind / CancelToken | ViewEvent / Vec<ViewEvent> / usize / Envelope | 不 panic |
| I32 | `lightweight::view::WebView2Probe::{injected,unknown,external_available}` | bool / 无 | Self / bool | 无 |

| 编号 | 内容 |
| --- | --- |
| RO16 | 016 轮对后端仓 0 个写请求，约束延续 RO01-RO15。 |
| RO17 | 016 轮未调用任何远端服务接口，未新增外部 API；CF 具体调用方法仍按 F17 由用户在完成时提供；本层不暴露 CF 下载源。 |
| RO18 | 批量请求按 011 D12：一次请求带多个 id、每页 20、core.cache 单飞；逐条目单发列为禁止项。 |
| RO19 | WebView2 可用性由宿主注入，不写死检测键；该键仍未证实，真实运行时实测受阻。 |
| RO20 | 加载器逐版本 schema 未证实，`version_json_fields` 恒空、`schema_patch` 恒 None；不生成 version json patch。 |
| RO21 | UI 整页演示闸门 016 轮首次触发，整页演示与实现分开落盘，演示不进 `src/`。 |
| RO22 | Cargo.toml / Cargo.lock 未变，无新增 crate；`serde` / `tokio` / `async-std` 计数为 0。 |

## 017 界面视觉预览

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I33 | `#scene=<name>` URL 路由 | 15 个场景名 | 对应场景画面 | 未知名回落 home |
| I34 | `show(name)` / `dismissOverlay()` | 场景名 / 无 | 可见区块、导航高亮、弹窗清理 | 无 |
| I35 | `openDlg` / `closeDlg` | 标题 / 正文 / id / 关闭动作 | 弹窗画面与 `[KCU]` 诊断行 | 无 |
| I36 | `python3 scripts/render_ui.py` | 无 | 16 张 PNG | 非零退出 |

| 编号 | 内容 |
| --- | --- |
| RO23 | 017 轮对后端仓 0 个写请求，约束延续 RO01-RO22。 |
| RO24 | 截图由本地 chromium 156 渲染，字体走本地 Noto / WenQuanYi；0 次远端请求，未调用任何 API。 |
| RO25 | 公告中心、公告详情、更新提示、维护/活动公告均为演示层，未进入 `src/`；公告族规则见 017 D06/D07。 |
| RO26 | 风格取自样板（配色、圆角、描边、卡片层次、轻噪点），位置重新组织；未复制样板代码、FCL 品牌与外部字体。 |
| RO27 | `src/` 本轮无变化；`cargo test --offline` 仍为 141 passed / 0 failed；Cargo.lock 未变。 |
| RO28 | PNG 预览闸门写入 docs/rules/ui-demo.md G07-G10；每轮动 UI 须复跑 `scripts/render_ui.py`。 |

## 018 纸质 UX 界面

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I37 | `#view=<name>` URL 路由 | 20 个视图名 + 5 个别名 | 对应视图 | 未知名回落 home |
| I38 | `show(name)` / `setTheme(t)` | 视图名 / light-dark | 可见区块、导航、工具条、主题 | 无 |
| I39 | `openDlg` / `closeDlg` | 标题 / 正文 / id / 关闭动作 | 弹窗画面与 `[KCU]` 诊断行 | 无 |
| I40 | `seedNoise(alpha,r,g,b)` | 4 个整数 | 噪点 data URI 注入 CSS 变量 | 无 |
| I41 | `python3 scripts/render_ui.py` | 无 | 21 张 PNG | 非零退出 |

| 编号 | 内容 |
| --- | --- |
| RO29 | 018 轮对后端仓 0 个写请求，约束延续 RO01-RO28。 |
| RO30 | 截图由本地 chromium 渲染，字体走本地 Noto Sans / Noto Serif CJK；噪点由 canvas 固定种子生成；0 次远端请求，未调用任何 API。 |
| RO31 | 源稿 `/data/inputs/FCL揉纸启动器-桌面端-v3(1).txt` 与 007 轮存档 `assets/ui/normal-mode-v3.html` 逐字一致，`cmp exit 0`、双端 SHA-1 `235943d2…e99d`。 |
| RO32 | 视觉 token 同源：米纸 / 墨 / 暗青绿 / 砖红 / 细线 / 半透明卡片 / 深色纸质 / 圆角 4-8-10；位置重排，不采用三栏拖拽与右栏公告。 |
| RO33 | UX HTML 与流程 HTML 分开命名与登记：`demos/ui-full-*.html` 看界面，`demos/round-0XX-*.html` 看逻辑；动 UI 的主交付为 UX HTML + PNG。 |
| RO34 | `src/` 本轮无变化；`cargo test --offline` 仍为 141 passed / 0 failed；Cargo.lock 未变。 |
| RO35 | 渲染脚本每视图带 `?r=<i>` 强制重载，避免主题与弹窗状态串场；仅 S02 为深色纸质。 |
| RO36 | 017 的 `ui-full-kcu-v2.html` 保留文件但标记作废；`demos/preview/` 全部覆盖为纸质版。 |

## 019 使用逻辑、图标与许可

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I42 | `#view=<name>` URL 路由 | 28 个视图名 + 别名 | 对应视图 | 未知名回落 home |
| I43 | `.lb-soft` / `.lb-hard` | 无 | 软刷新取增量 / 强制刷新清缓存 | 失败回退快照 |
| I44 | `<use href="#i-<name>">` | 图标名 | lucide 矢量图形 | 未知名为空 |
| I45 | `renderLic()` / `[data-lic]` | 分组键 | 七列许可表 | 缺失给来源链接 |
| I46 | `rfFail` / `rfRetry` / `rfReset` | 无 | 刷新失败兜底提示 | 保留 12 秒前快照 |
| I47 | `aiTest` / `aiCancel` | 无 | AI 连接状态 | 三类失败分别提示 |
| I48 | `shStart` / `shStop` | 无 | 开服器状态 | 端口占用给建议 |
| I49 | `python3 scripts/render_ui.py` | 无 | 29 张 PNG | 非零退出 |

| 编号 | 内容 |
| --- | --- |
| RO37 | 019 轮对后端仓 0 个写请求，约束延续 RO01-RO36。 |
| RO38 | 88 枚图标取自 `api.github.com/repos/lucide-icons/lucide/contents/icons/*.svg`，逐枚记录 blob SHA 与来源 URL；sprite 内联，0 次远端字体 / 脚本请求。 |
| RO39 | Lucide ISC License（Copyright (c) 2026 Lucide Icons and Contributors）；Feather 派生图标另带 MIT（Cole Bemis, 2013-present）。 |
| RO40 | 演示层已使用 1 组图标；文档层逐字存档 13 组；进入 `src/` 构建 0 项；本项目 LICENSE 未生成。 |
| RO41 | 逻辑条 22 处，每处显示已缓存时间、命中 / 未命中、刷新、强制刷新、状态；点击写 `[KCU]` 诊断行。 |
| RO42 | 刷新 R1–R5 五类触发；失败回退上次缓存，不显示空白；取消 0 副作用；时间戳统一「N 秒前 / N 分钟前 / HH:MM」。 |
| RO43 | `src/` 本轮无变化；`cargo test --offline` 141 passed / 0 failed；Cargo.lock 未变。 |
| RO44 | 019 spec 逐字副本 1 行 782 字节，SHA-1 `ad626f16ec7c6b763d7892951901e6b609042292`。 |
| RO45 | 渲染脚本每视图带 `?r=<i>` 强制重载，仅 S02 为深色纸质。 |

## 020 导航锁定、设置归拢与上层候选

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I50 | `#view=settings&tab=<name>` | 9 个分组名 | 对应设置面板 | 未知名回落 general |
| I51 | `[data-tab]` / `[data-pane]` | 分组名 | 面板切换与诊断行 | 无 |
| I52 | `slotConflict` / `slotReset` / `slotDenyClose` | 无 | 拒绝提示 / 复位 | 拒绝注册 |
| I53 | `setCacheExpired` / `setCacheAll` / `setAiTest` | 无 | 清理、测试反馈 | 二次确认 |
| I54 | `plugUpdate` / `plugRollback` | 无 | 插件包更新或回滚 | 保留旧插件 |
| I55 | `data-v="slots"` / `recommendations` / `handoff` / `upperstack` | 无 | 4 个新视图 | 无 |
| I56 | `python3 scripts/render_ui.py` | 无 | 38 张 PNG | 非零退出 |

| 编号 | 内容 |
| --- | --- |
| RO46 | 020 轮对后端仓 0 个写请求，约束延续 RO01-RO45。 |
| RO47 | 一级导航收敛为 9 项；设置与关于固定 `slot:core.locked.*`；插件区 `slot:plugin.*` 独立。 |
| RO48 | 工具条按视图收敛：设置 / 关于 / 许可 / 槽位 / 总览 / 交接 / 候选等页面隐藏列表网格、刷新、新建实例按钮。 |
| RO49 | 设置 9 分组，每项稳定 `core.*` ID、默认值、写后即时生效、`@modified`、单项重置。 |
| RO50 | 10 处推荐位逐处登记内容 / 权重 / 用户覆盖 / 缓存刷新 / 设置 ID；插件来源走 `plugin.rec.*`。 |
| RO51 | 服务器状态取 SLP 1.7+ JSON 字段；6 类状态、探测间隔 60s、超时 3s、缓存 60s 失败标灰。 |
| RO52 | 插件化更新：签名校验不可禁用，默认只升，回滚需显式比较器，失败保留旧插件，核心二进制不动。 |
| RO53 | 上层实现批准采用第三方代码；12 组候选全部标「候选 · 未进构建」；`src/` 与 Cargo.lock 无变化。 |
| RO54 | 020 spec 逐字副本 1 行 853 字节，SHA-1 `070c6475693e4bd28f41cfbb3d6b6f9b7d6e72f6`。 |
| RO55 | 26 个 `<section class="view` 区块、26 条逻辑条、88 个 `<symbol`、37 张截图视图 / 38 张 PNG。 |
| RO56 | 交接基线 `docs/design/handoff.md`：必读 6 步、已完成 L1-L3、H01-H08 不可变边界。 |

## 021 服务器自动连接与产品文案

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I57 | `data-v="servers"` / `srvAdd` / `srvRecRefresh` / `srvScan` | 无 | 自动连接、重新连接、重读 servers.dat | 连不上沉底 |
| I58 | `[data-lock]` / `[data-join]` | 服务器 ID | 锁定切换、双击进服弹窗 | 无合适实例给换实例 |
| I59 | `[data-gotab]` | 分组名 | 设置页并切到该分组 | 无 |
| I60 | `server-join` / `servers-locked` 路由别名 | 无 | 弹窗 / 失败沉底演示 | 无 |
| I61 | `python3 scripts/render_ui.py` | 无 | 35 产品图 + 1 总览 + 4 内部证据图 | 非零退出 |

| 编号 | 内容 |
| --- | --- |
| RO57 | 021 轮对后端仓 0 个写请求，约束延续 RO01-RO56。 |
| RO58 | spec 逐字副本 1 行 1003 字节，SHA-1 `ec86aa376a193eb5701de49b2f2bd464599189b5`。 |
| RO59 | 产品界面无稳定设置 ID、槽位徽章、交接基线、候选状态；四个内部证据区块标 data-internal 不进导航与总览。 |
| RO60 | 服务器状态页面口径被 021 取代：设置分组改「服务器与连接」，删 SLP 参数 / 6 类状态 / 自定义文案颜色。 |
| RO61 | 排序：锁定置顶且连不上不动 → 连得上按延迟 / 最近使用 / 人数 → 连不上沉底。 |
| RO62 | 双击进服：锁定实例 → 上次玩该服实例 → 上次全局实例 → 兼容范围；不静默失败。 |
| RO63 | `servers.dat` 只读，含可见 / 隐藏 / 快速进入三类来源；不覆盖玩家在游戏里加的服。 |
| RO64 | 显示照游戏内：64×64 图标、玩家命名、两行 MOTD（转义）、人数、ping 五档、版本名。 |
| RO65 | 35 张产品截图 / 4 张内部证据图 / 1 张总览；26 区块、26 逻辑条、88 symbol、9+9 tabs-panes。 |
| RO66 | 020 的 34-slots / 35-recommendations / 36-handoff / 37-upperstack 四张证据图保留，不进总览。 |

## 022 异步探测与设备连接范围

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I62 | `srvProbe(soft)` / `buildPlan()` | 是否增量 | 异步计划、增量渲染 | 已在跑忽略；档位 0 给空计划 |
| I63 | `srvCancel()` / `srvSwitchTier()` | 无 | 停止 / 切档重排 | 未在跑忽略 |
| I64 | `setBudLimit` / `setBudConc` / `setBudTier` | 数值 | 改档位并重算计划 | 无 |
| I65 | `srvRank` / `srvCachedWeight` / `neverSuccess` | 服务器对象 | 排序值与分组 | 无 |
| I66 | `servers-budget` / `servers-history` 路由别名 | 无 | 标准档 / 轻量档演示 | 无 |

| 编号 | 内容 |
| --- | --- |
| RO67 | 022 轮对后端仓 0 个写请求，约束延续 RO01-RO66。 |
| RO68 | spec 逐字副本 1 行 265 字节，SHA-1 `1a99d1a137ad246fa50c9e66958d3792dc54ec2f`。 |
| RO69 | 档位表：标准 limit=4 / conc=3，轻量 limit=2 / conc=2，无界面 0；数值可在设置里改。 |
| RO70 | 新加服务器强制入队、不受 N 裁剪，但占同一份额度，总数仍等于 N。 |
| RO71 | 范围外不发请求、保留上次结果、按缓存权重 200 档；无成功记录不主动连、300 档中段；曾成功本轮失败 900 档沉底；锁定 0 档不动。 |
| RO72 | 取消后不再写新结果、不再发新请求、inflight 归零、队列清空；已完成结果保留。 |
| RO73 | 37 张产品截图 / 4 张内部证据图 / 1 张总览；26 区块、26 逻辑条、88 symbol、9+9 tabs-panes。 |
| RO74 | Q01-Q03 为本轮自主拍板口径，待用户确认，只落 docs/，不写进产品界面。 |

## 023 标识 / i18n / 崩溃反馈

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I67 | `tr(k, fb)` / `applyI18n()` / `setLang(l)` | key / locale | 本地化文本 | 缺 key 回退 fb |
| I68 | `openRename(s)` / `data-rename` | sid | 改名弹窗 | 空名不保存 |
| I69 | `setCrashOn` / `setCrashAddr` / `setCrashMask` | 值 | 崩溃策略 | 无 |
| I70 | `crashView` / `crashExport` | 无 | 预览 / 本地导出 | 无 dump 空态 |
| I71 | `servers-rename` / `servers-samenames` / `i18n-en` 路由别名 | 无 | 演示场景 | 无 |

| 编号 | 内容 |
| --- | --- |
| RO75 | 023 对后端仓 0 个写请求，约束延续 RO01-RO74。 |
| RO76 | spec 逐字副本 1 行 698 字节，SHA-1 `a473ce3dfc83cad84b35991e6053358ccfbd234a`。 |
| RO77 | `sid = UUIDv5(KCU_NAMESPACE, normalize(ip:port))`；目录与缓存只按 sid；显示名可重复可改。 |
| RO78 | 演示层 550+ 个 `data-i18n` 标注点；日志与 `[KCU]` 诊断行不进字典。 |
| RO79 | 崩溃库四层候选全部标「未进构建」；默认不记录、脱敏开、发送前确认、Win7 降级本地 dump。 |
| RO80 | 43 张产品截图 / 4 张内部证据图 / 1 张总览；26 区块、26 逻辑条、88 symbol、10 个设置 tab-pane。 |
| RO81 | Q01-Q04 为本轮自主拍板口径，待用户确认，只落 docs/，不写进产品界面。 |

## 版本弃用

| 接口 | 行为 |
| --- | --- |
| Modrinth 旧版本 | 完全弃用后永久 410 |
| GitHub REST API | 2022-11-28 支持至 2028-03-10；不再支持的版本返回 410 |
| 破坏性变更 | 升版本号并给迁移步骤 |

## 028 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I28 | F028-01 | `server.join_alert.subscribe` / `list` / `dismiss` |
| I29 | F028-02 | `server.activity.pie` / `sessions` / `export` |
| I30 | F028-03 | `server.auto_cmd.rules` / `upsert` / `fire` / `audit` |
| S28 | 状态 | 三项均为文档登记，未进入 `src/`，无函数实现 |

## 030 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I31 | `LaunchArgs::parse` | 签名不变，内部实现换 lexopt；错误面仍 `Result<Self, String>` |
| S29 | 状态 | 参数解析已库化；Q-028-01 / Q-028-02 仍待用户答复，功能 md 结论栏为空 |

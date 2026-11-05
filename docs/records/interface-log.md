# 接口更新记录

更新轮次：009

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
| I09 | 第三方许可证 | docs/research/09-licenses.md、docs/licenses/index.md | 7 份全文已证实；slint 三许可全文未证实 |
| I10 | 时间、上游版本、网络边界 | docs/research/10-upstream-state.md | 005 轮新增 |
| I11 | 正常模式 UI 设计稿 | assets/ui/index.md、docs/features/normal-ui.md | 已落盘，授权未证实 |
| I12 | RCON 与 UUID 一手补证 | docs/research/06-server.md、docs/research/02-auth.md | 008 轮新增，见 008 新增来源 |
| I13 | Cargo profile / Win32 DLL 搜索 / std::process / WebView2 进程组 / MSVC 部署 / 目标三元组 | docs/research/11-runtime.md | 009 轮新增，9 份一手原文；2 项未证实；1 项受阻 |

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

## 版本弃用

| 接口 | 行为 |
| --- | --- |
| Modrinth 旧版本 | 完全弃用后永久 410 |
| GitHub REST API | 2022-11-28 支持至 2028-03-10；不再支持的版本返回 410 |
| 破坏性变更 | 升版本号并给迁移步骤 |

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
| 02-auth.md | 登录与认证 | 设备码流、XBL/XSTS/MC 端点、离线 UUID 可复现算法、authlib-injector 规范原文与路由、ALI 服务发现、Bearer 401 | Notchian 服务端采用离线 UUID 算法、Azure Client ID、旧 Mojang 账号、令牌保护、Xbox 端点一手原文 | 无 |
| 03-download.md | 官方与镜像下载 | Mojang manifest/libraries/assets、BMCLAPI 映射、MCIM 映射、Modrinth/CurseForge 头 | 官方必需请求头、v3 基址、MCIM 服务主体、BMCLAPI SLA | 6 个上游主机直连 403 |
| 04-loaders.md | 加载器 | Fabric Meta README 544 行、profile/json 与 server/json 端点、launcherMeta 字段、fabric-loader 0.20.1 | 逐加载器 version json 注入差异、Forge/NeoForge/Quilt/OptiFine schema | meta.fabricmc.net、meta.quiltmc.org、maven.neoforged.net 直连 403 |
| 05-rust-windows.md | Rust/Windows 运行时 | WebView2 检测键与 GUID、wry-v0.57.1、Rust 1.99.1、tao/egui/slint/iced 许可证、MAX_PATH | 最低 WebView2 版本、固定版本嵌入、Command 参数转义、本地库加载 | rustc/cargo 缺失、static.rust-lang.org 403 |
| 06-server.md | 服务端 | 68 键默认值、UTF-8 与 CRLF、RCON 包字段与认证、EULA | 字节序、引入版本、分片上限、Mojang 官方 RCON 文档 | 无 |
| 07-lan.md | 局域网协议 | RFC 6762 / 6763 / 6455 原文 | Bonjour、HTTP 路由认证 TLS、二维码、发现端口 | 无 |
| 08-github-api.md | GitHub REST API | 请求头、两个版本实测 200、认证限流 5000、github/docs 原文 91 行、410 Gone | 未认证限流 60 数值 | docs.github.com 网页直抓 |
| 09-licenses.md | 许可证 | HMCL、wry、tao、egui、iced、authlib-injector、slint 清单、CC BY-SA 4.0 | slint 三许可全文、Blessing Skin、BMCLAPI、MCIM、Modrinth、CurseForge、KCU 原仓库 | 无 |
| 10-upstream-state.md | 时间、上游版本、网络边界、工具链 | 时钟一致、7 个上游 tag、api.github.com 200、6 个官方文档 200 | 无 | github.com 与 6 个上游主机 403、docs.github.com 与 wiki.vg 抓取、rustc/cargo 缺失 |

## 来源类型

| 类型 | 示例 |
| --- | --- |
| 接口返回 | https://api.github.com/repos/HMCL-dev/HMCL/license、/releases/latest、/contents/、/tags |
| 官方文档 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution、https://docs.modrinth.com/api/ |
| 官方仓库 | https://github.com/FabricMC/fabric-meta、https://github.com/yushijinhun/authlib-injector |
| 协议规范 | https://www.rfc-editor.org/rfc/rfc6762、https://www.rfc-editor.org/rfc/rfc6763、https://www.rfc-editor.org/rfc/rfc6455 |
| 社区文档 | https://minecraft.wiki/w/Server.properties、https://minecraft.wiki/w/RCON |

## 005 卡点状态

| 001 轮遗留项 | 005 状态 |
| --- | --- |
| HMCL LICENSE 全文 | 已证实，docs/licenses/HMCL-LICENSE.txt |
| 加载器 version json schema | Fabric Meta README 已证实；其余未证实 |
| 离线 UUID 规则 | 算法已证实，Notchian 服务端行为未证实 |
| RCON 默认值 | 已证实，并纠正 broadcast-rcon-to-ops |
| WebView2 检测键 | 已证实 |
| docs.github.com 直抓 | 仍受阻；经 github/docs 仓库 API 取得一手原文 |
| authlib-injector wiki 直抓 | 已证实，经 GitHub contents API 取得 211 + 668 行原文 |
| 锚点格式不统一 | 10 份文档统一为 URL / path:line / cmd 输出 |
| 远程仓库创建 | 004 轮已完成 |
| 正常模式 UI | 未提供，未落盘 |
| 框架蓝图 | 方案已落盘，未批准 |

## 禁止项

| 编号 | 内容 |
| --- | --- |
| R01 | 未取得 LICENSE 全文前不复制对应组件代码、资源、商标、Client ID。 |
| R02 | 镜像响应不作为官方源、稳定源或授权分发源。 |
| R03 | 未证实字段不写进实现。 |
| R04 | 四值只用已证实 / 已失败 / 未证实 / 受阻；中间态禁用。 |
| R05 | 403 policy_default_denied 记为受阻，不记为上游服务异常。 |

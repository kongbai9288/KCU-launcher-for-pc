# 调研索引

检索日期：2026-11-04。每条事实带来源 URL 与四值。四值定义见 docs/rules/proof-rules.md。

| 文件 | 主题 | 已证实 | 未证实 | 受阻 |
| --- | --- | --- | --- | --- |
| 01-hmcl.md | HMCL 结构、构建、许可证 | 仓库模块、Gradle、GPLv3 名称与附加条款 | LICENSE 全文、参数生成、版本解析 | 无 |
| 02-auth.md | 正版/离线/第三方登录 | Microsoft 设备码流端点与字段、XBL/XSTS/Minecraft 端点、Yggdrasil 路由 | 离线 UUID 规则、旧账号迁移现状、Azure Client ID 审批 | authlib-injector 规范原文抓取 |
| 03-download.md | 官方与镜像下载 | Mojang manifest/libraries/assets 规则、MCIM 映射、Modrinth/CurseForge 头 | BMCLAPI 当前可用性、v3 基址 | 无 |
| 04-loaders.md | 加载器 | Fabric/Quilt 官方声明 | 五个加载器 version json 注入字段 | 无 |
| 05-rust-windows.md | Rust/Windows 运行时 | wry WebView2、MAX_PATH、longPathAware | 单文件发布、子进程参数转义 | 官方文档部分抓取失败 |
| 06-server.md | 服务端 | Paper 配置目录、server.properties 键、RCON 包格式 | 各服务端当前默认值逐项核对 | 无 |
| 07-lan.md | 局域网协议 | mDNS 标准线索、WebSocket 握手 | KCU 端口、载荷、加密 | 无 |
| 08-github-api.md | GitHub REST API | User-Agent 必需、403、Accept、版本头、限流 | 2026-03-10 版本端点差异 | docs.github.com 直抓被拒 |
| 09-licenses.md | 许可证 | HMCL GPLv3、wry Apache-2.0/MIT | 其余组件许可证全文 | 无 |

## 来源类型

| 类型 | 示例 |
| --- | --- |
| 官方文档 | docs.modrinth.com/api/、docs.curseforge.com/rest-api/、docs.papermc.io、learn.microsoft.com、GitHub 文档中文镜像 |
| 官方仓库 | github.com/HMCL-dev/HMCL、github.com/tauri-apps/wry、github.com/mcmod-info-mirror/mcim-api、BMCLAPI |
| 协议规范 | Microsoft OAuth 2.0 设备授权、Yggdrasil 服务端技术规范、wiki.vg RCON |
| 二手线索 | Minecraft Wiki、社区存档、技术博客 |

## 禁止项

- 未取得 LICENSE 全文前不复制 HMCL 代码、资源、商标、Client ID。
- 镜像响应不作为官方源、稳定源或授权分发源。
- 未证实字段不写进实现。

# 合规条款、凭据保护与阻塞项补证

检索日期：2026-11-05
轮次：010
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。
对应需求：docs/spec/00-requirements.txt:17、:171-173、:228、:230、:249

## CurseForge 第三方 API 条款

来源：https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions

| 编号 | 原文条款 | 四值 | 锚点 |
| --- | --- | --- | --- |
| CF01 | `each Developer will be issued a unique API Key (the “API Key”), which is non-transferable and may not be shared with any third party. Developer may not disclose the API Key to any third party, except to such employees who are subject to corresponding confidentiality obligations` | 已证实 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions |
| CF02 | `Developer shall not, and shall not allow any third party, to ... (e) conceal your identity or geographic location when accessing the API, including accessing the API through a proxy server or VPN;` | 已证实 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions |
| CF03 | `Developer shall not, and shall not allow any third party, to ... (e) save or cache any data obtained through the API or SDK.` | 已证实 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions |
| CF04 | `Developer shall not ... use the API or SDK, or any materials obtained through the API or SDK, in order build any product or service that competes, directly or indirectly, with CF, CurseForge for Studios, or the Platform.` | 已证实 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions |
| CF05 | `Upon the External App exceeding a certain quota ... continued use of the Platform API and/or SDK may (at Overwolf’s sole discretion) require Developer to enter into a written licensing agreement with Overwolf, which license agreement may contain payment requirements` | 已证实 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions |
| CF06 | `Overwolf may terminate these Terms upon written notice if it has justifiable reason to believe that Developer is in material breach ... Overwall may at any time terminate these Terms without cause with respect to any specific External App within 30 days` | 已证实 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions |
| CF07 | 条款归属 Overwolf Ltd.，定义 Developer / External App / Platform API / SDK | 已证实 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions |

## 条款与现有登记的冲突项

| 编号 | 条款 | 现有登记位置 | 冲突内容 | 四值 |
| --- | --- | --- | --- | --- |
| X01 | CF03 不得缓存 API 数据 | docs/research/03-download.md 缓存头 `sync_at` | 镜像缓存与本地元数据缓存字段未逐项核对条款 | 已证实（冲突成立） |
| X02 | CF03 不得缓存 API 数据 | docs/spec/00-requirements.txt:172 默认走国内镜像 | 镜像响应作为缓存源已写入配置项约定 | 已证实（冲突成立） |
| X03 | CF02 不得隐藏身份或地理位置 | docs/research/03-download.md 6 个上游主机直连 403 | 代理或 VPN 路径与该条款不兼容 | 已证实（冲突成立） |
| X04 | CF01 API Key 不可共享 | docs/spec/00-requirements.txt:171 密钥可选 | 每个 Developer 需各自取得唯一 Key；共享单一 Key 的构建方式不合规 | 已证实（冲突成立） |
| X05 | CF04 不得构建竞争产品 | docs/features/server.md、docs/spec/00-requirements.txt:174 商店加载器图标 | 启动器内置 Mod 商店是否落入竞争产品范围未取得条款解释 | 未证实 |
| X06 | CF05 配额与书面许可 | docs/research/08-github-api.md 之外的 API 预算 | 配额阈值由 Overwolf 单方决定，页面未给数值 | 未证实 |
| X07 | CF06 30 天无因终止 | 无对应登记 | 依赖该 API 的功能需可禁用 | 未证实 |

处置条件（docs/spec/00-requirements.txt:249）：X01-X04 已成立，在进入构建前需用户拍板；`src/` 保持为空，未生成任何下载模块代码。

## Modrinth API 条款

来源：https://modrinth.com/legal/terms

| 编号 | 原文条款 | 四值 | 锚点 |
| --- | --- | --- | --- |
| MR01 | `The Modrinth API enables users to perform actions on the Service via their own services, such as their websites and/or applications.` | 已证实 | https://modrinth.com/legal/terms |
| MR02 | `We grant the User of the Modrinth API a limited, non-exclusive, non-sublicensable and revocable license to download, display, query, create, edit, and delete the User Generated Content on the Service via their own services` | 已证实 | https://modrinth.com/legal/terms |
| MR03 | `The User uses the Modrinth API in accordance with these Terms, the Community Standards and all applicable laws and regulations that apply to such use.` | 已证实 | https://modrinth.com/legal/terms |
| MR04 | `Each User using the Modrinth API shall indemnify Modrinth and keep Modrinth indemnified for all claims, proceedings or actions brought by another User or any other third party, including governmental authorities.` | 已证实 | https://modrinth.com/legal/terms |
| MR05 | 缓存、速率限制、具体禁止行为 | 页面未写明 | 未证实 | https://modrinth.com/legal/terms |

## 镜像协议

| 来源 | 内容 | 四值 | 锚点 |
| --- | --- | --- | --- |
| MCIM 协议片段 | `禁止在 MCIM 上对接口进行二次封装`、`未经原始版权所有者授权，严禁通过 MCIM 进行任何形式的转发或二次发布` | 未证实 | 搜索结果片段，一手仓库 URL 未取得 |
| MCIM 仓库定位 | `GET /repos/Glavo/MCIM` 404；`GET /repos/mcim-api/mcim-api` 404 | 受阻 | cmd: python3 urllib → 404 Not Found |
| BMCLAPI | 检索结果为 openbmclapi 部署文档 `CLUSTER_ID` / `CLUSTER_SECRET` / `CLUSTER_BYOC`，非 API 服务条款 | 未证实 | 搜索结果片段，一手条款 URL 未取得 |
| CurseForge 服务条款页面 | 取得 6 条原文 | 已证实 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions |
| Modrinth 服务条款页面 | 取得 4 条原文 | 已证实 | https://modrinth.com/legal/terms |

## 许可证全文补证

| 组件 | SPDX | 文件 | 字节 | SHA-1 前 16 | 四值 | 锚点 |
| --- | --- | --- | --- | --- | --- | --- |
| kongbai9288/KCU-Launcher | GPL-3.0 | docs/licenses/KCU-Launcher-LICENSE.txt | 35149 | 31a3d460bb3c7d988 | 已证实 | https://api.github.com/repos/kongbai9288/KCU-Launcher/contents/LICENSE |
| PrismLauncher/PrismLauncher | GPL-3.0 | 与 KCU-Launcher-LICENSE.txt 同字节同 SHA-1，未另存副本 | 35149 | 31a3d460bb3c7d988 | 已证实 | https://api.github.com/repos/PrismLauncher/PrismLauncher/license |
| MultiMC/Launcher | NOASSERTION | docs/licenses/MultiMC-COPYING.md | 18664 | 59094e5b6f19f4c8 | 已证实 | https://api.github.com/repos/MultiMC/Launcher/contents/COPYING.md |
| MinecraftForge/MinecraftForge | NOASSERTION | docs/licenses/Forge-LICENSE.txt | 27733 | 9b5ee64703a133b6 | 已证实 | https://api.github.com/repos/MinecraftForge/MinecraftForge/contents/LICENSE.txt |
| neoforged/NeoForge | LGPL-2.1 | docs/licenses/NeoForge-LICENSE.txt | 24444 | 98e2b035a83f5f6d | 已证实 | https://api.github.com/repos/neoforged/NeoForge/contents/LICENSE.txt |
| QuiltMC/quilt-loader | Apache-2.0 | docs/licenses/Quilt-LICENSE.txt | 11357 | 92170cdc034b2ff8 | 已证实 | https://api.github.com/repos/QuiltMC/quilt-loader/contents/LICENSE |
| slint-ui/slint 主文件 | NOASSERTION | docs/licenses/slint-LICENSE.txt | 3759 | d3e9bcc7238fd90f | 已证实 | https://api.github.com/repos/slint-ui/slint/contents/LICENSE.md |

文件头部核对：

| 文件 | 首行内容 | 四值 |
| --- | --- | --- |
| MultiMC-COPYING.md | `# MultiMC` / `Portions are licensed under Apache 2.0 License` | 已证实 |
| Forge-LICENSE.txt | `licensed under the terms of the LGPL 2.1` | 已证实 |
| NeoForge-LICENSE.txt | `GNU LESSER GENERAL PUBLIC LICENSE Version 2.1, February 1999` | 已证实 |
| Quilt-LICENSE.txt | `Apache License Version 2.0, January 2004` | 已证实 |

## slint 三许可全文

| 许可 | 文件 | 字节 | SHA-1 前 16 | 四值 | 锚点 |
| --- | --- | --- | --- | --- | --- |
| Royalty-free License 2.0 | docs/licenses/slint-LICENSES/LicenseRef-Slint-Royalty-free-2.0.md | 3620 | f611f298c4a28ad4 | 已证实 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES/LicenseRef-Slint-Royalty-free-2.0.md |
| GNU GPLv3 | docs/licenses/slint-LICENSES/GPL-3.0-only.txt | 34670 | e3bdbf20d43fc066 | 已证实 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES/GPL-3.0-only.txt |
| Commercial license | docs/licenses/slint-LICENSES/LicenseRef-Slint-Software-3.0.md | 9187 | b535523cc612dafe | 已证实 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES/LicenseRef-Slint-Software-3.0.md |

| 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| `You can use the Slint framework under ***any*** of the following licenses, at your choice:` | 三选一 | 已证实 | docs/licenses/slint-LICENSE.txt:17 |
| `Permits use in **proprietary** desktop, mobile, and web applications **at no cost**. Use in embedded systems is excluded.` | Royalty-free 范围 | 已证实 | docs/licenses/slint-LICENSE.txt:19 |
| `Permits use in **open source software** under GPL-compatible terms, **at no cost**` | GPLv3 范围 | 已证实 | docs/licenses/slint-LICENSE.txt:20 |
| `A Commercial license is required for embedded systems, regardless of disclosure.` | 嵌入式需商用许可 | 已证实 | docs/licenses/slint-LICENSE.txt:32 |
| `LICENSES/` 目录条目数 | 20 | 已证实 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES |

005 轮 docs/licenses/index.md L03 登记「三许可全文标未证实」，010 轮取得 3 份全文，L03 改写为已取得并列出具体文件。

## 凭据保护一手原文

对应 docs/spec/00-requirements.txt:17。

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| DP01 | `Typically, only a user with the same logon credential as the user who encrypted the data can decrypt the data. In addition, the encryption and decryption usually must be done on the same computer.` | 绑定到同一用户登录凭据与同一计算机 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata |
| DP02 | `A pointer to a DATA_BLOB structure that contains a password or other additional entropy used to encrypt the data. ... must also be used in the decryption phase.` | 可选熵，加解密需一致 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata |
| DP03 | `When this flag is set, it associates the data encrypted with the current computer instead of with an individual user. Any user on the computer ... can use CryptUnprotectData to decrypt the data.` | `CRYPTPROTECT_LOCAL_MACHINE` 放大可解密范围 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata |
| DP04 | `A pointer to a DATA_BLOB structure that receives the encrypted data.` / `If the function succeeds, the function returns TRUE. If the function fails, it returns FALSE.` | 输出 blob 与布尔返回 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata |
| CM01 | `The CredWrite function creates a new credential or modifies an existing credential in the user's credential set. The new credential is associated with the logon session of the current token. The token must not have the user's security identifier (SID) disabled.` | 绑定到当前令牌登录会话 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credwritew |
| CM02 | `CRED_PRESERVE_CREDENTIAL_BLOB: The credential BLOB from an existing credential is preserved with the same credential name and credential type.` | 保留已有 blob 标志 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credwritew |
| CM03 | 凭据管理器提供程序页面：函数运行在 `LocalSystem` 上下文，不是用户上下文 | 该页面描述提供程序，不是应用级 API | 已证实 | https://learn.microsoft.com/en-us/windows/win32/secauthn/credential-manager |
| CM04 | `CRED_PERSIST_SESSION` / `CRED_PERSIST_LOCAL_MACHINE` / `CRED_PERSIST_ENTERPRISE` 取值 | CredWriteW 页面未写明 | 未证实 | https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credwritew |

约束：

| 编号 | 内容 |
| --- | --- |
| C01 | 不设置 `CRYPTPROTECT_LOCAL_MACHINE`；DP03 会放大可解密范围。 |
| C02 | 凭据不进入日志、诊断包、配置快照。 |
| C03 | 令牌保护方案状态为未批准、未实现；src/ 为空。 |
| C04 | 无头模式复用其他模式留存的正版凭据时走同一保护路径。 |

## 加载器 schema 线索

| 来源 | 内容 | 四值 | 锚点 |
| --- | --- | --- | --- |
| DeepWiki Elemental | `ProfileJson` 含 `inheritsFrom`、`libraries`；`ForgeInstallerProfile` 含 processors 与 `data` HashMap；Quilt `LoaderProfile` 含 `LoaderVersion`、`IntermediaryVersion`、`LauncherMeta` | 未证实 | https://deepwiki.com/ElectronicWave/Elemental/5.2-mod-discovery-system |
| 来源归属 | 第三方项目自动生成的文档，不是加载器官方 schema | 已证实 | https://deepwiki.com/ElectronicWave/Elemental/5.2-mod-discovery-system |
| Forge / NeoForge / Quilt / OptiFine version json 注入差异 | 未取得一手原文 | 未证实 | 一手 schema 未取得 |
| R03 | 未证实字段不写进实现 | 已证实 | docs/research/index.md R03 |

## 离线 UUID 服务端行为

| 来源 | 内容 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 第三方工具站 | `UUID offlineUUID = UUID.nameUUIDFromBytes(("OfflinePlayer:" + username).getBytes(StandardCharsets.UTF_8));`，声称 Bukkit / Spigot / Paper / Purpur / Folia 采用 | 未证实 | https://minecraftserver.buzz/minecraft-offline-uuid-generator |
| 来源归属 | 社区工具站，不是 Mojang 或服务端项目一手原文 | 已证实 | https://minecraftserver.buzz/minecraft-offline-uuid-generator |
| Notchian 服务端采用该算法 | 未取得一手原文 | 未证实 | https://minecraft.wiki/w/Universally_unique_identifier |
| docs/research/02-auth.md 实现禁用约束 | 不解除 | 已证实 | docs/research/02-auth.md 约束段 |

## 玩家分支启动器一手仓库

| 项 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| PrismLauncher/PrismLauncher | GPL-3.0，默认分支 develop，LICENSE 与 KCU 原仓库同字节 | 已证实 | https://api.github.com/repos/PrismLauncher/PrismLauncher |
| MultiMC/Launcher | NOASSERTION，默认分支 develop，COPYING.md 含 Apache 2.0 部分 | 已证实 | https://api.github.com/repos/MultiMC/Launcher |
| Prism README | 6992 字节，SHA-1 前 16 `5f2becce4bbd56c6` | 已证实 | https://api.github.com/repos/PrismLauncher/PrismLauncher/contents/README.md |
| 实例创建流程 | Add Instance → 选择版本与 modloader，或从侧栏导入 mod 平台整合包 | 已证实 | https://prismlauncher.org/wiki/getting-started/create-instance/ |
| mmc-pack.json `formatVersion: 1` / `components` | 领域知识库片段，不是官方格式文档 | 未证实 | 搜索结果片段 |
| Prism / MultiMC 功能项可取之处 | 未逐功能核对官方 wiki 与 LICENSE | 未证实 | 一手功能清单未取得 |

## 上游版本状态

| 仓库 | tag / release | 发布时间 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| HMCL-dev/HMCL | v3.16.4 | 2026-09-17T04:30:46Z | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL/releases/latest |
| FabricMC/fabric-loader | 0.20.1 | 2026-10-19T19:02:45Z | 已证实 | https://api.github.com/repos/FabricMC/fabric-loader/releases/latest |
| tauri-apps/wry | wry-v0.57.1 | 2026-10-23T11:20:46Z | 已证实 | https://api.github.com/repos/tauri-apps/wry/releases/latest |
| rust-lang/rust | 1.99.1 | 2026-10-16T04:47:44Z | 已证实 | https://api.github.com/repos/rust-lang/rust/releases/latest |
| PrismLauncher/PrismLauncher | 11.1.1 | 2026-09-28T22:55:19Z | 已证实 | https://api.github.com/repos/PrismLauncher/PrismLauncher/releases/latest |
| slint-ui/slint | v1.18.1 | 2026-09-21T09:35:54Z | 已证实 | https://api.github.com/repos/slint-ui/slint/releases/latest |
| neoforged/NeoForge | tags?per_page=1 返回 `v99.99` / `cb6f92e` | 与 MinecraftForge 返回同名同 sha | 已证实 | https://api.github.com/repos/neoforged/NeoForge/tags?per_page=1 |
| MinecraftForge/MinecraftForge | tags?per_page=1 返回 `v99.99` / `cb6f92e` | 与 NeoForge 返回同名同 sha | 已证实 | https://api.github.com/repos/MinecraftForge/MinecraftForge/tags?per_page=1 |

| 项 | 值 | 四值 |
| --- | --- | --- |
| `v99.99` 作为当前版本号 | 两个不同仓库返回同一 tag 名与同一 sha，不作为版本结论 | 已失败 |
| 带认证 `GET /rate_limit` | 200，remaining 5000 | 已证实 |
| 未认证 `GET /rate_limit` | 404，Date `Thu, 05 Nov 2026 14:13:48 GMT` | 受阻 |
| 沙盒时钟 | `Thu Nov  5 22:13:48 CST 2026`，与 GMT 头一致 | 已证实 |

## 010 新增来源

| 编号 | URL | 用途 | 结果 |
| --- | --- | --- | --- |
| P01 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions | CurseForge API 条款 6 条 | 200 |
| P02 | https://modrinth.com/legal/terms | Modrinth API License 4 条 | 200 |
| P03 | https://learn.microsoft.com/en-us/windows/win32/api/dpapi/nf-dpapi-cryptprotectdata | DPAPI 原文 | 200 |
| P04 | https://learn.microsoft.com/en-us/windows/win32/api/wincred/nf-wincred-credwritew | CredWriteW 原文 | 200 |
| P05 | https://learn.microsoft.com/en-us/windows/win32/secauthn/credential-manager | 凭据管理器提供程序页面 | 200 |
| P06 | https://api.github.com/repos/kongbai9288/KCU-Launcher/contents/LICENSE | KCU 原仓库 LICENSE 全文 | 200 |
| P07 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES | 20 个许可文件名 | 200 |
| P08 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES/LicenseRef-Slint-Royalty-free-2.0.md | Royalty-free 全文 | 200 |
| P09 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES/GPL-3.0-only.txt | GPLv3 全文 | 200 |
| P10 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES/LicenseRef-Slint-Software-3.0.md | 商用许可全文 | 200 |
| P11 | https://deepwiki.com/ElectronicWave/Elemental/5.2-mod-discovery-system | 加载器 schema 二手线索 | 200 |
| P12 | https://minecraftserver.buzz/minecraft-offline-uuid-generator | 离线 UUID 社区线索 | 200 |
| P13 | https://prismlauncher.org/wiki/getting-started/create-instance/ | Prism 实例创建流程 | 200 |
| P14 | https://api.github.com/repos/Glavo/MCIM | MCIM 仓库定位 | 受阻，404 |
| P15 | https://api.github.com/repos/mcim-api/mcim-api | MCIM 仓库定位 | 受阻，404 |
| P16 | https://minecraft.wiki/w/Universally_unique_identifier | Notchian 行为边界复核 | 200 |

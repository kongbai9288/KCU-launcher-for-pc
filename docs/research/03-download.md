# 下载源、镜像与请求头

检索日期：2026-11-05
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。

## Mojang 官方

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 版本清单 | https://piston-meta.mojang.com/mc/game/version_manifest_v2.json | 已证实 | https://minecraft.wiki/w/Game_files |
| 旧域名 | https://launchermeta.mojang.com/mc/game/version_manifest_v2.json | 已证实 | https://minecraft.wiki/w/Game_files |
| 库下载 | https://libraries.minecraft.net/<package>/<name>/<version>/<name>-<version>.jar | 已证实 | https://minecraft.wiki/w/Game_files |
| 库校验 | 同名 .jar.sha1 | 已证实 | https://minecraft.wiki/w/Game_files |
| 传输 | 必须 HTTPS | 已证实 | https://minecraft.wiki/w/Game_files |
| 版本 JSON 键 | libraries、natives、rules、extract、assetIndex、javaVersion | 已证实 | https://minecraft.wiki/w/Game_files |
| natives | 平台字符串插入 .jar 与版本之间，${arch} 替换为 32/64 | 已证实 | https://minecraft.wiki/w/Game_files |
| rules | action=allow/disallow 与 os 判定下载平台 | 已证实 | https://minecraft.wiki/w/Game_files |
| extract | 解压规则，可排除 META-INF | 已证实 | https://minecraft.wiki/w/Game_files |
| assets | https://resources.download.minecraft.net/<hash 前 2 位>/<完整 hash>，必须 HTTPS | 已证实 | https://minecraft.wiki/w/Game_files |
| asset index | 版本 JSON 中链接，资源含名称、SHA1、size | 已证实 | https://minecraft.wiki/w/Game_files |
| Java 运行时清单 | https://launchermeta.mojang.com/v1/products/java-runtime/.../all.json | 已证实 | https://minecraft.wiki/w/Game_files |
| 官方必需请求头 | 未核实 | 未证实 | 一手文档未取得 |

## BMCLAPI

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| manifest | https://bmclapi2.bangbang93.com/mc/game/version_manifest.json | 已证实 | https://hmcl.huangyuhui.net/ |
| 版本 JSON 替换 | launchermeta.mojang.com、launcher.mojang.com 换为 BMCLAPI 基址 | 已证实 | https://hmcl.huangyuhui.net/ |
| assets | https://bmclapi2.bangbang93.com/assets | 已证实 | https://hmcl.huangyuhui.net/ |
| maven | https://bmclapi2.bangbang93.com/maven | 已证实 | https://hmcl.huangyuhui.net/ |
| authlib-injector | https://bmclapi2.bangbang93.com/mirrors/authlib-injector | 已证实 | https://hmcl.huangyuhui.net/ |
| 主控地址 | https://openbmclapi.bangbang93.com，节点 CLUSTER_ID / CLUSTER_SECRET / CLUSTER_PORT 默认 4000 | 已证实 | https://github.com/bangbang93/openbmclapi |
| HMCL 覆盖参数 | -Dhmcl.bmclapi.override= | 已证实 | https://hmcl.huangyuhui.net/ |
| 当前可用性/SLA | 直连检查跑不动 | 受阻 | cmd: curl https://bmclapi2.bangbang93.com/ → 403 policy_default_denied |

## MCIM

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| Modrinth API 映射 | api.modrinth.com → mod.mcimirror.top/modrinth | 已证实 | https://github.com/mcmod-info-mirror/mcim-api |
| Modrinth CDN 映射 | cdn.modrinth.com → mod.mcimirror.top | 已证实 | https://github.com/mcmod-info-mirror/mcim-api |
| CurseForge 映射 | api.curseforge.com → mod.mcimirror.top/curseforge | 已证实 | https://github.com/mcmod-info-mirror/mcim-api |
| ForgeCDN 映射 | edge.forgecdn.net → mod.mcimirror.top | 已证实 | https://github.com/mcmod-info-mirror/mcim-api |
| 缓存时间头 | sync_at，YYYY-MM-DDTHH:MM:SSZ | 已证实 | https://github.com/mcmod-info-mirror/mcim-api |
| UA 白名单 | 接入前需提交启动器 UA | 已证实 | https://github.com/mcmod-info-mirror/mcim-api |
| 当前仓库状态 | 旧 mcim-api 已由 mcim-rust-api 重写 | 已证实 | https://github.com/mcmod-info-mirror/mcim-api |
| 服务主体/限流/停服公告 | 未核实 | 未证实 | 一手资料未取得 |
| 是否官方 assets/libraries 镜像 | 否 | 已证实 | https://github.com/mcmod-info-mirror/mcim-api |

## Modrinth

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 生产基础地址 | api.modrinth.com | 已证实 | https://docs.modrinth.com/api/ |
| 测试基础地址 | staging-api.modrinth.com | 已证实 | https://docs.modrinth.com/api/ |
| 认证头 | Authorization: <PAT>，多数读请求无需令牌 | 已证实 | https://docs.modrinth.com/api/ |
| 必需头 | 唯一可识别的 User-Agent | 已证实 | https://docs.modrinth.com/api/ |
| UA 建议格式 | github_username/project_name/1.56.0 (contact@launcher.com) | 已证实 | https://docs.modrinth.com/api/ |
| 限流 | 300 次/分钟/IP | 已证实 | https://docs.modrinth.com/api/ |
| 限流头 | X-Ratelimit-Limit、X-Ratelimit-Remaining、X-Ratelimit-Reset | 已证实 | https://docs.modrinth.com/api/ |
| 弃用 | 完全弃用后永久 410 | 已证实 | https://docs.modrinth.com/api/ |
| 破坏性变更 | URL 路径版本号递增并发布迁移步骤 | 已证实 | https://docs.modrinth.com/api/ |
| v3 基础地址 | 文档未给出原文 | 未证实 | https://docs.modrinth.com/api/ |
| v3 直连检查 | 跑不动 | 受阻 | cmd: curl https://api.modrinth.com/v3/ → 403 policy_default_denied |
| labrinth 最新 release | v2.4.3，2022-06-18T23:33:47Z | 已证实 | https://api.github.com/repos/modrinth/labrinth/releases/latest |
| GitHub 令牌兼容 | v3 GA 后停止用于 Modrinth 认证 | 已证实 | https://docs.modrinth.com/api/ |

## CurseForge

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 基础地址 | https://api.curseforge.com | 已证实 | https://docs.curseforge.com/rest-api/ |
| 认证头 | x-api-key | 已证实 | https://docs.curseforge.com/rest-api/ |
| 文件列表 | GET /v1/mods/{modId}/files | 已证实 | https://docs.curseforge.com/rest-api/ |
| 分页 | pageSize 默认/最大 50，index + pageSize <= 10000 | 已证实 | https://docs.curseforge.com/rest-api/ |
| 响应字段 | id、fileName、downloadUrl、hashes、gameVersions、dependencies、modules | 已证实 | https://docs.curseforge.com/rest-api/ |
| CDN 直下 | https://edge.forgecdn.net/files/{id}/{subId}/{filename} | 已证实 | https://blog.curseforge.com/ |
| CDN 无密钥 | 强制执行后返回 401 | 已证实 | https://blog.curseforge.com/ |
| 旧文档头名 | X-Api-Token | 已证实 | https://authors-old.curseforge.com/ |

## 005 网络边界

| 主机 | 状态码 | 四值 |
| --- | --- | --- |
| https://bmclapi2.bangbang93.com/ | 403 | 受阻 |
| https://api.modrinth.com/v3/ | 403 | 受阻 |
| https://meta.fabricmc.net/v2/versions/loader | 403 | 受阻 |
| https://meta.quiltmc.org/v3/versions/loader | 403 | 受阻 |
| https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml | 403 | 受阻 |
| https://static.rust-lang.org/dist/channel-rust-stable.toml | 403 | 受阻 |
| https://api.github.com/rate_limit | 200 | 已证实 |

403 返回体字段：title=Request denied、reason=policy_default_denied、source.policy_name=main-policy。

约束：
- 密钥不写死，走配置项，默认镜像，密钥可选。
- Modrinth 基础地址做成单一配置项。
- 410 与 401 走兜底分级，不崩溃。
- 403 policy_default_denied 记为检查受阻，不记为上游服务异常。

# 下载源、镜像与请求头

检索日期：2026-11-04

## Mojang 官方

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 版本清单 | `https://piston-meta.mojang.com/mc/game/version_manifest_v2.json` | 已证实 | minecraft.wiki Game files |
| 旧域名 | `https://launchermeta.mojang.com/mc/game/version_manifest_v2.json` | 已证实 | 二手文档仍引用 |
| 库下载 | `https://libraries.minecraft.net/<package>/<name>/<version>/<name>-<version>.jar` | 已证实 | minecraft.wiki Game files |
| 库校验 | 同名 `.jar.sha1` | 已证实 | 同上 |
| 传输 | 必须 HTTPS，HTTP 不可用 | 已证实 | 同上 |
| 版本 JSON 键 | `libraries`、`natives`、`rules`、`extract`、`assetIndex`、`javaVersion` | 已证实 | 同上 |
| natives | 平台字符串插入 `.jar` 与版本之间，含 `${arch}` 替换为 32/64 | 已证实 | 同上 |
| rules | `action=allow/disallow` 与 `os` 判定下载平台 | 已证实 | 同上 |
| extract | 解压规则，可排除 `META-INF` | 已证实 | 同上 |
| assets | `https://resources.download.minecraft.net/<hash 前 2 位>/<完整 hash>`，必须 HTTPS | 已证实 | 同上 |
| asset index | 版本 JSON 中链接，资源含名称、SHA1、size | 已证实 | 同上 |
| Java 运行时清单 | `https://launchermeta.mojang.com/v1/products/java-runtime/.../all.json` | 已证实 | 同上 |
| 官方必需请求头 | 未核实 | 未证实 | 一手文档未取得 |

## BMCLAPI

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| manifest | `https://bmclapi2.bangbang93.com/mc/game/version_manifest.json` | 已证实 | MCBBS 存档 / HMCL 参数 |
| 版本 JSON 替换 | `launchermeta.mojang.com`、`launcher.mojang.com` 换为 BMCLAPI 基址 | 已证实 | MCBBS 存档 |
| assets | `https://bmclapi2.bangbang93.com/assets` | 已证实 | 同上 |
| maven | `https://bmclapi2.bangbang93.com/maven` | 已证实 | 同上 |
| authlib-injector | `https://bmclapi2.bangbang93.com/mirrors/authlib-injector` | 已证实 | 同上 |
| 主控地址 | `https://openbmclapi.bangbang93.com`，节点环境变量 `CLUSTER_ID`、`CLUSTER_SECRET`、`CLUSTER_PORT` 默认 4000 | 已证实 | BMCLAPI 官方 GitHub README |
| HMCL 覆盖参数 | `-Dhmcl.bmclapi.override=` | 已证实 | HMCL 参数文档 |
| 当前可用性/SLA | 未核实 | 未证实 | 存档非当前官方站点 |

## MCIM

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| Modrinth API 映射 | `api.modrinth.com` → `mod.mcimirror.top/modrinth` | 已证实 | mcim-api README / 官网 |
| Modrinth CDN 映射 | `cdn.modrinth.com` → `mod.mcimirror.top` | 已证实 | 同上 |
| CurseForge 映射 | `api.curseforge.com` → `mod.mcimirror.top/curseforge` | 已证实 | 官网 URL 替换速览 |
| ForgeCDN 映射 | `edge.forgecdn.net` → `mod.mcimirror.top` | 已证实 | 同上 |
| 缓存时间头 | `sync_at`，格式 `YYYY-MM-DDTHH:MM:SSZ`，调用方自行判断是否信任 | 已证实 | mcim-api README |
| UA 白名单 | 可能添加，接入前需提交启动器 UA | 已证实 | mcim-api README |
| 当前仓库状态 | 旧 mcim-api 已由 mcim-rust-api 重写，旧仓库预计不再维护 | 已证实 | mcim-api README 警告 |
| 服务主体/限流/停服公告 | 未核实 | 未证实 | 一手资料未取得 |
| 是否官方 assets/libraries 镜像 | 否 | 已证实 | 官方定位为 Mod 信息镜像 |

## Modrinth

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 生产基础地址 | `api.modrinth.com` | 已证实 | docs.modrinth.com/api/ |
| 测试基础地址 | `staging-api.modrinth.com` | 已证实 | 同上 |
| 认证头 | `Authorization: <PAT>`，多数读请求无需令牌 | 已证实 | 同上 |
| 必需头 | 唯一可识别的 `User-Agent`；仅 HTTP 库名会增加被封禁概率 | 已证实 | 同上 |
| UA 建议格式 | `github_username/project_name/1.56.0 (contact@launcher.com)` | 已证实 | 同上 |
| 限流 | 300 次/分钟/IP，与是否带令牌无关 | 已证实 | 同上 |
| 限流头 | `X-Ratelimit-Limit`、`X-Ratelimit-Remaining`、`X-Ratelimit-Reset` | 已证实 | 同上 |
| 弃用 | 旧版本立即 deprecated，完全弃用后永久返回 410 | 已证实 | 同上 |
| 破坏性变更 | URL 路径版本号递增并发布迁移步骤 | 已证实 | 同上 |
| v3 基础地址 | 文档未给出 `https://api.modrinth.com/v3` 原文 | 未证实 | 仅外部线索 |
| GitHub 令牌兼容 | v3 GA 后停止用于 Modrinth 认证 | 已证实 | 同上 |

## CurseForge

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 基础地址 | `https://api.curseforge.com` | 已证实 | docs.curseforge.com/rest-api/ |
| 认证头 | `x-api-key`，密钥在 CurseForge for Studios 控制台生成 | 已证实 | 同上 |
| 文件列表 | `GET /v1/mods/{modId}/files` | 已证实 | 同上 |
| 分页 | pageSize 默认/最大 50，`index + pageSize <= 10000` | 已证实 | 同上 |
| 响应字段 | `id`、`fileName`、`downloadUrl`、`hashes`、`gameVersions`、`dependencies`、`modules` 等 | 已证实 | 同上 |
| CDN 直下 | `https://edge.forgecdn.net/files/{id}/{subId}/{filename}`，`x-api-key` 或 `?api-key=` | 已证实 | blog.curseforge.com |
| CDN 无密钥 | 强制执行后返回 401 | 已证实 | 同上 |
| 旧文档头名 | `X-Api-Token` | 已证实 | authors-old.curseforge.com |

约束：
- 密钥不写死，走配置项，默认镜像，密钥可选。
- Modrinth 基础地址做成单一配置项。
- 410 与 401 走兜底分级，不崩溃。

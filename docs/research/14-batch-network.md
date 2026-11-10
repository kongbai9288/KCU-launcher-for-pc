# 批量请求、聚合搜索与本地监听通用法

检索日期：2026-11-11
轮次：011
对应：docs/spec/00-requirements.txt:171-175；docs/spec/11-features-input.txt:注意通过api向模组平台发送请求一次进酒当中可以包含多 json、:模组尽量去重聚合、:下面详细介绍功能 1、:尽量不要把咱们的APi写成共有的API、:本次开发的时候尽量不要api写死、:支持一个模组多源同时下载
锚点格式：完整 URL 或 `path:line`；锚点逐行独立。

## 用户当轮点名的问题

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| U01 | `因为我之前遇到过你每搜索一个模组就会单发一个请求导致算力大量浪费的行为` | 逐条目单发请求被点名 | 已证实 | docs/spec/11-round-011-instructions.txt |
| U02 | `通过api向模组平台发送请求一次进酒当中可以包含多 json` | 一次请求携带多个 ID | 已证实 | docs/spec/11-features-input.txt |
| U03 | `mod页每20个条目显示一次` | 分页粒度 20 | 已证实 | docs/spec/11-features-input.txt 第 1 条 |
| U04 | `可以聚合搜索` / `模组尽量去重聚合，可以引入翻译源` | 聚合与去重 | 已证实 | docs/spec/11-features-input.txt |
| U05 | `对于网络处理上面，你就需要去联网看看别人的通用法` | 需取通用法 | 已证实 | docs/spec/11-round-011-instructions.txt |

## 通用法一手资料：N+1 网络调用反模式

来源：https://vibgrate.com/anti-patterns/n-plus-one-network-calls

| 编号 | 原文 | 值 | 四值 |
| --- | --- | --- | --- |
| N01 | `N+1 network calls fetch a list then make one remote call per item, fanning a single operation into N+1 dependency calls that multiply latency and overload downstreams. Use batch endpoints, request coalescing, or aggregation read models to collapse the fan-out.` | 反模式定义与三类解法 | 已证实 |
| N02 | `Latency grows linearly with N: a 50-item list becomes 51 sequential round trips. The downstream service receives a burst of near-identical small requests, multiplying its load and exhausting its rate limits and connection pools.` | 逐条目单发的后果 | 已证实 |
| N03 | `Batch / multi-get endpoints: pass all IDs in one request (POST /users:batchGet) and resolve them server-side.` | 批量端点 | 已证实 |
| N04 | `Request coalescing (DataLoader): buffer per-item lookups and dispatch a single batched call per tick, with de-duplication.` | 请求合并与去重 | 已证实 |
| N05 | `Backend-for-frontend / aggregation service: assemble the composite response once, close to the data.` | 聚合层 | 已证实 |
| N06 | `Denormalization / read models: pre-join the data the view needs so no per-item call is required.` | 读模型 | 已证实 |
| N07 | `Warning Signs: A loop over a collection that calls a service or API for each element. Distributed traces showing one parent span with N nearly identical child spans.` | 自检信号 | 已证实 |
| N08 | `Verify with traces that N+1 child spans collapse into one batched span and that latency no longer scales with result size.` | 验证口径 | 已证实 |

来源归属：反模式知识库，不是 Modrinth 或 CurseForge 官方文档，标为开发者经验。U05 要求的「别人的通用法」由 N01-N08 与下方官方批量端点共同覆盖。

## Modrinth 官方批量端点

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| M01 | `Get multiple projects` 类端点 `ids required string` / `["AABBCCDD", "EEFFGGHH"]` / `The IDs and/or slugs of the projects` | 一次请求传多个项目 ID 或 slug | 已证实 | https://docs.modrinth.com/api/operations/getprojects/ |
| M02 | `Get multiple versions` / `GET /versions` / `ids required string` / `["AABBCCDD", "EEFFGGHH"]` / `The IDs of the versions` | 一次请求传多个版本 ID | 已证实 | https://docs.modrinth.com/api/operations/getversions/ |
| M03 | `limit: integer default: 10 <= 100` / `The number of results returned by the search` | 搜索单页默认 10、上限 100 | 已证实 | https://docs.modrinth.com/api/operations/searchprojects/ |
| M04 | `offset: integer ... The offset into the search. Skips this number of results` / `index: default: relevance Allowed values: relevance downloads follows newest updated` | 分页与排序 | 已证实 | https://docs.modrinth.com/api/operations/searchprojects/ |
| M05 | `facets: Facets are an essential concept for understanding how to filter out results.` / `project_type categories versions license downloads created_timestamp modified_timestamp` | 一次请求内多条件过滤 | 已证实 | https://docs.modrinth.com/api/operations/searchprojects/ |
| M06 | 单次 `ids` 批量请求的 ID 数量上限 | 官方文档未写明 | 未证实 | https://docs.modrinth.com/api/operations/getprojects/ |
| M07 | U03 的每页 20 条可落在 `limit=20` | M03 允许 <=100 | 已证实 | M03 + U03 |

## CurseForge 官方批量端点

来源：https://docs.curseforge.com/docs/game-integration/unreal/browsing-and-discovery
该页为 CurseForge 官方 Unreal SDK 文档，不是 REST 端点页；REST 页 `https://docs.curseforge.com/rest-api/endpoint/POST_1_mods/` 直抓受阻。

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| C01 | `Get Mods Info By Ids (pins modIds, on_results, on_error), Get Mod Info By Id (modId, on_mod, on_error), Get Files Info By Ids (FileIds, OnResults, OnError)` | 官方 SDK 同时提供单 ID 与多 ID 接口 | 已证实 | https://docs.curseforge.com/docs/game-integration/unreal/browsing-and-discovery |
| C02 | `FCFCoreGetModsFilter: Field Type / default Meaning modIds TArray, empty The mod ids to fetch` | 批量入参为数组 | 已证实 | https://docs.curseforge.com/docs/game-integration/unreal/browsing-and-discovery |
| C03 | `Fill an FCFCoreApiRequestPagination with the page you want.` / `pagination.pageSize = 20;` / `const bool bHasMorePages = (Page.index + Page.pageSize)` | 官方 SDK 示例 `pageSize = 20`，与 U03 一致 | 已证实 | https://docs.curseforge.com/docs/game-integration/unreal/browsing-and-discovery |
| C04 | `FCFCoreSearchModsFilter` / `filter.searchFilter = InText` / `filter.sortField` / `filter.sortOrder` | 搜索条件集中在单次请求 | 已证实 | https://docs.curseforge.com/docs/game-integration/unreal/browsing-and-discovery |
| C05 | `MatchPlatformFiles ... takes an array of file ids and returns the FFile objects matching those ids for the current platform` / `FMatchPlatformFilesFilter ... carries one fileIds array of int64` | 按平台批量筛文件 | 已证实 | https://docs.curseforge.com/docs/game-integration/unreal/browsing-and-discovery |
| C06 | `api.get_mods([285109, 238222]) # returns a list of Mods` / `api.get_files([3940240]) # returns a list of Files matching their id` | 第三方 Python 封装同样走批量入参 | 已证实 | https://pypi.org/project/curse-api/ |
| C07 | REST `POST /v1/mods` 请求体字段与上限 | 官方 REST 端点页不可访问 | 受阻 | https://docs.curseforge.com/rest-api/endpoint/POST_1_mods/ |
| C08 | CurseForge 服务条款对缓存、代理、密钥的约束 | 已证实，见 docs/research/12-compliance.md CF01-CF06 | 已证实 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions |

## 聚合口径

| 编号 | 项 | 值 | 四值 |
| --- | --- | --- | --- |
| A01 | 列表页一次请求取一页，不在列表渲染循环里逐条目发请求 | N03 + M03 + C03 | 已证实 |
| A02 | 详情补全走批量 ID 端点，一次请求携带多个 ID | M01、M02、C01、C02 | 已证实 |
| A03 | 并发逐条目查重先在本地按 ID 去重，再合并为一次批量请求 | N04、U04 | 已证实 |
| A04 | 搜索条件、排序、分页、facet 收进单次请求 | M04、M05、C04 | 已证实 |
| A05 | 每页 20 条落在 `limit=20` / `pageSize=20` | M07、C03 | 已证实 |
| A06 | 一个模组多源同时下载时，某源先完成后关闭其余请求 | 用户当轮输入 | 已证实 |
| A07 | A06 的取消语义：`abort` / `CancellationToken` / 连接池取消的具体实现 | 未取得一手原文 | 未证实 |
| A08 | 去重聚合后引入翻译源的接口与许可证 | 未证实 | docs/spec/11-features-input.txt |
| A09 | 自检：单次父请求下不得出现 N 个近乎相同的子请求 | N07、N08 | 已证实 |

## 本地监听与 API 暴露边界

用户当轮要求：`尽量不要把咱们的APi写成共有的API,防止被别人攻击，内部监听（只有服务器功能让ai用的api不受影响）`。

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| L01 | `Binding a service to the loopback interface (127.0.0.1) is generally secure enough for internal communication` / `The loopback interface only allows connections originating from the same machine. External access is blocked by default.` | 本地 API 绑定回环 | 已证实 | https://blog.g5cybersecurity.com/?p=178654/ |
| L02 | `Verify Binding Address ... Look for lines where the 'Local Address' is 127.0.0.1:port_number` / `Regardless of binding address, always require strong authentication` | 绑定核验与鉴权 | 已证实 | https://blog.g5cybersecurity.com/?p=178654/ |
| L03 | `Control Access with Firewalls ... On Windows Firewall, create an inbound rule that blocks connections to the port except from localhost.` | 防火墙入站规则 | 已证实 | https://blog.g5cybersecurity.com/?p=178654/ |
| L04 | 服务器功能给 AI 用的 API 不受 L01 回环约束 | 用户当轮明确例外 | 已证实 | docs/spec/11-features-input.txt |
| L05 | 绑定 `0.0.0.0` / `[::]` 的端口清单 | 无实现，未生成清单 | 未证实 | src/ 为空 |
| L06 | 端口、主机、基址不写死，集中到配置项 | 用户当轮要求 | 已证实 | docs/spec/11-features-input.txt |

## 配置集中约束

| 编号 | 用户原文 | 约束 | 四值 |
| --- | --- | --- | --- |
| K01 | `尽量不要api写死，还有那些联网的功能的网址` | 端点基址为配置项 | 已证实 |
| K02 | `api主要用于分类操作系统` | API 配置按 OS 分类 | 已证实 |
| K03 | `那些联网他们有可能后面会更新相关的端口` | 端口不写死 | 已证实 |
| K04 | `对于那些图标什么的也只到一个文件当中` | 图标资源单文件入口 | 已证实 |
| K05 | `可以自己选择保存路径` | 保存路径为配置项 | 已证实 |
| K06 | `所有的语言方面的文件都堆在一起` | 语言包集中目录 | 已证实 |
| K07 | `对于未来的变更都尽量把文件归中方便后面维护` | 文件集中 | 已证实 |
| K08 | `§用于表示模板版本号` | 用户自定义镜像 URL 的占位符 | 已证实 |
| K09 | 上述配置的具体字段名与文件位置 | 未定 | 未证实 |

## 与 010 轮合规冲突的关系

| 编号 | 项 | 四值 |
| --- | --- | --- |
| B01 | A02 的批量请求不解除 CF03 禁止缓存 | 已证实，docs/research/12-compliance.md |
| B02 | A01 的分页不解除 CF02 禁止代理或 VPN 访问 | 已证实，docs/research/12-compliance.md |
| B03 | C07 的 REST 端点页受阻不影响 C01-C05 的 SDK 层事实 | 已证实 |
| B04 | 用户当轮给出密钥与镜像处置方向，见 docs/decisions/011-feature-input.md | 已证实 |

## 011 新增来源

| 编号 | URL | 用途 | 结果 |
| --- | --- | --- | --- |
| P34 | https://vibgrate.com/anti-patterns/n-plus-one-network-calls | N01-N08 | 200 |
| P35 | https://docs.modrinth.com/api/operations/getprojects/ | M01 | 200 |
| P36 | https://docs.modrinth.com/api/operations/getversions/ | M02 | 200 |
| P37 | https://docs.modrinth.com/api/operations/searchprojects/ | M03-M05 | 200 |
| P38 | https://docs.curseforge.com/docs/game-integration/unreal/browsing-and-discovery | C01-C05 | 200 |
| P39 | https://pypi.org/project/curse-api/ | C06 | 200 |
| P40 | https://docs.curseforge.com/rest-api/endpoint/POST_1_mods/ | C07 | 受阻，不可访问 |
| P41 | https://blog.g5cybersecurity.com/?p=178654/ | L01-L03 | 200 |
| P42 | https://support.curseforge.com/en/support/solutions/articles/9000207405-curse-forge-3rd-party-api-terms-and-conditions | C08 | 200 |

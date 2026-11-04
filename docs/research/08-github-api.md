# GitHub REST API 请求头

检索日期：2026-11-05
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 基础地址 | https://api.github.com | 已证实 | https://docs.github.com/en/rest |
| User-Agent | 所有 API 请求必须包含有效的 User-Agent | 已证实 | https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api |
| 无 UA | 403 Forbidden | 已证实 | cmd: curl -H 'User-Agent:' https://api.github.com/rate_limit → 403 |
| 带完整头 | 200 | 已证实 | cmd: curl -H 'User-Agent: KCU-Launcher-Desktop/0.0.0' -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' https://api.github.com/rate_limit → 200 |
| Accept | application/vnd.github+json | 已证实 | https://docs.github.com/en/rest/using-the-rest-api/getting-started-with-the-rest-api |
| 版本头 | X-GitHub-Api-Version | 已证实 | https://api.github.com/repos/github/docs/contents/content/rest/about-the-rest-api/api-versions.md |
| 未携带版本头 | 默认使用 {{ defaultRestApiVersion }} | 已证实 | https://api.github.com/repos/github/docs/contents/content/rest/about-the-rest-api/api-versions.md |
| 不再支持的版本 | 410 Gone | 已证实 | https://api.github.com/repos/github/docs/contents/content/rest/about-the-rest-api/api-versions.md |
| 受支持版本 | 2026-03-10、2022-11-28 | 已证实 | https://docs.github.com/zh/rest/about-the-rest-api/api-versions |
| 2022-11-28 支持结束 | 2028-03-10 | 已证实 | https://docs.github.com/zh/rest/about-the-rest-api/api-versions |
| 版本支持期 | 新版本发布后 24 个月 | 已证实 | https://docs.github.com/zh/rest/about-the-rest-api/api-versions |
| 版本 2022-11-28 实测 | 200 | 已证实 | cmd: curl -H 'X-GitHub-Api-Version: 2022-11-28' https://api.github.com/rate_limit → 200 |
| 版本 2026-03-10 实测 | 200 | 已证实 | cmd: curl -H 'X-GitHub-Api-Version: 2026-03-10' https://api.github.com/rate_limit → 200 |
| 省略版本头实测 | 200 | 已证实 | cmd: curl 无版本头 https://api.github.com/rate_limit → 200 |
| 认证限流 | 5000 次/小时 | 已证实 | cmd: GET /rate_limit → resources.core.limit=5000, remaining=4997 |
| 未认证限流 | 60 次/小时 | 未证实 | 未取得响应中的数值；004 轮触发过 403 rate limit exceeded |
| 限流响应头 | x-ratelimit-remaining、x-ratelimit-reset | 已证实 | https://api.github.com/rate_limit |
| rate_limit 端点 | GET /rate_limit，返回 resources.core/search/graphql | 已证实 | https://api.github.com/rate_limit |
| HEAD /rate_limit | 404 | 已失败 | cmd: curl -I https://api.github.com/rate_limit → 404 |
| github/docs 版本文档原文 | 91 行，blob SHA-1 7fba1393bbdbfc3e4fbe886d314fc4c343674594 | 已证实 | https://api.github.com/repos/github/docs/contents/content/rest/about-the-rest-api/api-versions.md |
| docs.github.com 网页直抓 | 被安全审核拒绝 | 受阻 | cmd: web_fetch https://docs.github.com/en/rest/about-the-rest-api/api-versions → ok=false |
| 认证凭据 | 不写入仓库、不写入代码、不写入测试 | 已证实 | docs/checklists/ai-errors.md:26 |
| 认证方案 | Authorization: token；Bearer 对 GET /user 返回 403 policy_default_denied | 已证实 | https://api.github.com/user |

## 005 补证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| GET /repos/github/docs/contents/content/rest/about-the-rest-api/api-versions.md | 200，91 行 | 已证实 |
| GET /rate_limit 带认证 | 200，limit 5000 | 已证实 |
| 三个版本头请求 | 200 / 200 / 200 | 已证实 |

来源：
- https://docs.github.com/en/rest
- https://docs.github.com/zh/rest/about-the-rest-api/api-versions
- https://api.github.com/repos/github/docs/contents/content/rest/about-the-rest-api/api-versions.md
- https://api.github.com/rate_limit

约束：
- 所有 api.github.com 请求统一经单一 HTTP 模块注入 User-Agent、Accept、X-GitHub-Api-Version。
- 403 与限流归二级降级，写诊断行。
- 版本头做成配置项，不散落字符串。

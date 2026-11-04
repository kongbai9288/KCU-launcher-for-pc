# GitHub REST API 请求头

检索日期：2026-11-04

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 基础地址 | `https://api.github.com` | 已证实 | GitHub 文档中文镜像 |
| User-Agent | 所有 API 请求必须包含有效的 User-Agent 头 | 已证实 | GitHub 文档「REST API 入门」镜像 |
| 建议值 | GitHub 用户名或应用名，例如 `Awesome-Octocat-App` | 已证实 | 同上 |
| 无 UA | 请求被拒绝 | 已证实 | 同上 |
| 无效 UA | 403 Forbidden | 已证实 | 同上 |
| Accept | `application/vnd.github+json` | 已证实 | 同上 / gitdocs.cn curl 示例 |
| 版本头 | `X-GitHub-Api-Version`，未携带时默认 `2022-11-28` | 已证实 | githubdocs.cn/rest/overview/api-versions |
| 受支持版本 | `2026-03-10`、`2022-11-28` | 已证实 | 同上 |
| 旧版本支持期 | 新版本发布后至少 24 个月 | 已证实 | 同上 |
| 破坏性变更 | 删除操作、重命名参数/字段、新增必填参数、修改类型、修改鉴权要求等 | 已证实 | 同上 |
| 认证限流 | 5000 次/小时 | 部分已证实 | GitHub 文档镜像 / 第三方汇总 |
| 未认证限流 | 60 次/小时 | 部分已证实 | 同上 |
| 限流响应头 | `x-ratelimit-remaining`、`x-ratelimit-reset` 需逐响应读取 | 部分已证实 | 第三方汇总 |
| rate_limit 端点 | `GET /rate_limit`，返回 `resources.core/search/graphql` 等 | 已证实 | GitHub Enterprise Server 3.22 文档 |
| docs.github.com 直抓 | 被安全审核拒绝 | 受阻 | 本轮 web_fetch 返回 ok=false |
| 认证凭据 | 不写入仓库、不写入代码、不写入测试 | 已证实 | docs/spec/00-requirements.txt 第 16 节 |

来源：
- https://githubdocs.cn/rest/overview/api-versions
- http://gitdocs.cn/en/rest/using-the-rest-api/getting-started-with-the-rest-api?tool=curl
- https://docs.github.com/en/enterprise-server@3.22/rest/rate-limit/rate-limit

约束：
- 所有 api.github.com 请求统一经单一 HTTP 模块注入 `User-Agent`、`Accept`、`X-GitHub-Api-Version`。
- 403 与限流归二级降级，写诊断行。
- 版本头做成配置项，不散落字符串。

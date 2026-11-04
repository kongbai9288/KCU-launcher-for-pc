# 远端公仓创建与推送路径

| 项 | 值 |
| --- | --- |
| 编号 | 004 |
| 状态 | 已实现 |
| 版本 | 0.0.0 |
| 轮次 | 004 |

## 决定了什么

| 编号 | 项 | 值 |
| --- | --- | --- |
| D01 | 远端 | `kongbai9288/KCU-launcher-for-pc` |
| D02 | 地址 | https://github.com/kongbai9288/KCU-launcher-for-pc |
| D03 | clone | https://github.com/kongbai9288/KCU-launcher-for-pc.git |
| D04 | 可见性 | public |
| D05 | 默认分支 | main |
| D06 | 创建时间 | 2026-11-04T05:30:00Z |
| D07 | 请求名 | `KCU launcher for pc` |
| D08 | 实际名 | `KCU-launcher-for-pc` |
| D09 | 原串保留位置 | repository description = `KCU launcher for pc` |
| D10 | 认证方案 | `Authorization: token <env KCU_PAT>`，凭据不入仓库 |
| D11 | 创建接口 | `POST /user/repos` → 201 |
| D12 | 推送路径 | `scripts/push.sh` 先走 git HTTP，403 时降级 `scripts/api_push.py` |
| D13 | API 快照 | GitHub Git Data API：blobs → tree → commit → ref |
| D14 | 本地历史 | 本地 git 提交链与远端 API 提交链不同哈希，树内容一致 |
| D15 | 仓库归属 | 与 github.com/kongbai9288/KCU-Launcher 不合并 |
| D16 | 空仓库初始化 | `PUT /repos/{owner}/{repo}/contents/README.md` → 201，生成初始提交 d0acb0d |
| D17 | 首次快照 | `c76f491`，parent=d0acb0d，42 文件 |

## 名称约束

| 项 | 值 |
| --- | --- |
| 输入 | `KCU launcher for pc` |
| API 返回 | `name: KCU-launcher-for-pc`，HTTP 201 |
| 空格处理 | GitHub 服务端规范化为连字符 |
| description | 保留输入原串 |

## 网络边界

| 主机 | 状态码 | 返回体 |
| --- | --- | --- |
| api.github.com GET /rate_limit，完整请求头 | 200 | 限流信息 |
| api.github.com GET /user，`Authorization: Bearer` | 403 | `Request denied / No policy rule matched the request / policy_default_denied` |
| api.github.com GET /user，`Authorization: token` | 200 | `login: kongbai9288` |
| api.github.com GET /repos/kongbai9288/KCU-launcher-for-pc | 200 | 仓库信息 |
| api.github.com POST /user/repos | 201 | 仓库信息 |
| api.github.com POST /git/blobs，空仓库未初始化 | 409 | `Git Repository is empty.` |
| api.github.com PUT /contents/README.md | 201 | 初始提交，仓库 git 对象可用 |
| api.github.com POST /git/blobs，初始化后 | 201 | blob sha |
| github.com GET 仓库页 | 403 | `Request denied / policy_default_denied` |
| github.com git-receive-pack info/refs | 403 | `Request denied / policy_default_denied` |
| git push 三种认证方式 | 403 | `fatal: unable to access ... 403` |

## 约束

| 编号 | 约束 |
| --- | --- |
| C01 | 所有 api.github.com 请求带 `User-Agent`、`Accept: application/vnd.github+json`、`X-GitHub-Api-Version: 2022-11-28` |
| C02 | `KCU_PAT` 只从环境变量读取，不写文件、不写 git config、不写提交说明、不写日志 |
| C03 | 远端 URL 不含凭据 |
| C04 | 推送前执行凭据扫描与措辞扫描，命中即停止 |
| C05 | API 快照按 `git ls-files` 全量构造树，排除项由 .gitignore 与 push-scope.md 决定 |
| C06 | 单文件 blob 创建失败即中止整轮推送，保留本地提交 |
| C07 | 图标许可证未定，不生成 ICO 与派生图 |

## 验证条件

| 编号 | 命令 | 期望 |
| --- | --- | --- |
| V01 | `curl ... -H "Authorization: token $KCU_PAT" https://api.github.com/user` | 200，login=kongbai9288 |
| V02 | `curl ... https://api.github.com/repos/kongbai9288/KCU-launcher-for-pc` | 200，private=false |
| V03 | `python3 scripts/api_push.py "<message>"` | `[KCU] remote push main OK ... via=git_data_api` |
| V04 | `curl .../git/ref/heads/main` | 200，object.sha 为非空提交 |
| V05 | `! grep -rqE 'gh[p]_' .` | exit 0 |
| V06 | `git hash-object <file>` 与远端 blob sha 比对 | 一致 |
| V07 | `GET /git/trees/<sha>?recursive=1` | 文件数与 `git ls-files` 一致 |

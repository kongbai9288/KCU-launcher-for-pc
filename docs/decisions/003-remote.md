# 远端公仓、每轮推送与搭建阶段

| 项 | 值 |
| --- | --- |
| 编号 | 003 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 003 |

## 决定了什么

| 编号 | 项 | 值 |
| --- | --- | --- |
| D01 | 仓库形态 | GitHub 远端公仓，不与 github.com/kongbai9288/KCU-Launcher 合并 |
| D02 | 仓库地址 | 待用户提供 owner/repo |
| D03 | 每轮交付 | 每轮产物除保密内容外全部进入该远端公仓 |
| D04 | 保密内容 | 不进入暂存区、不进入提交、不进入远端，清单见 docs/rules/push-scope.md |
| D05 | 功能输入阶段 | 用户仍提供功能与 UI，期间只做调研、文档、演示、决策登记 |
| D06 | 统一搭建触发条件 | 用户明确表示不再提供新功能 |
| D07 | 统一搭建顺序 | core → dispatcher → lightweight → headless → normal → UI → 构建 → 部署，逐层进入构建前需前一层独立验证通过 |
| D08 | 当前阶段 | 功能输入阶段，未启动 D07 |
| D09 | 本地仓库 | /data/workspace/kcu-launcher-desktop，第 003 轮产生首个提交 |
| D10 | 推送入口 | scripts/push.sh，远端 URL 由参数传入，代码内不写死 |

## 约束

| 编号 | 约束 |
| --- | --- |
| C01 | 远端创建与推送需认证；无认证时记受阻，不伪造推送结果 |
| C02 | 所有 api.github.com 请求带 `User-Agent`、`Accept: application/vnd.github+json`、`X-GitHub-Api-Version` |
| C03 | 提交说明、合并描述、说明文件不含解释性内容 |
| C04 | 第 001、002 轮产物在本轮一并纳入版本控制，不重写历史 |
| C05 | 单轮内不反复重做凑通过标记 |
| C06 | 底层搭建启动前，docs/spec/00-requirements.txt 第 0.1 条框架蓝图仍需单独确认 |
| C07 | 图标许可证未定，不生成 ICO 与派生图 |

## 验证条件

| 编号 | 命令 | 期望 |
| --- | --- | --- |
| V01 | `curl -sS -o /dev/null -w '%{http_code}' -H 'User-Agent: KCU-Launcher-Desktop/0.0.0' -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' https://api.github.com/rate_limit` | 200 |
| V02 | `curl -sS -o /dev/null -w '%{http_code}' -H 'User-Agent:' https://api.github.com/rate_limit` | 403 |
| V03 | `curl -sS -o /dev/null -w '%{http_code}' -X POST -H 'User-Agent: KCU-Launcher-Desktop/0.0.0' -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' -H 'Content-Type: application/json' -d '{"name":"kcu-launcher-desktop","private":false}' https://api.github.com/user/repos` | 401 |
| V04 | `git rev-list --count HEAD` | >= 1 |
| V05 | `! grep -rqE 'gh[p]_' .` | exit 0 |
| V06 | `scripts/push.sh 2>&1` | 无参数时非零退出，输出 remote url required |

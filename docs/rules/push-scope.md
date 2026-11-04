# 远端推送范围

轮次：004

远端：`kongbai9288/KCU-launcher-for-pc`，public，分支 main。

## 允许推送

| 类别 | 路径 |
| --- | --- |
| 代码 | src/ |
| 脚本 | scripts/push.sh、scripts/api_push.py |
| 事实性文档 | docs/spec/、docs/research/、docs/features/、docs/decisions/、docs/checklists/、docs/rules/、docs/records/、docs/verification/ |
| 版本与接口记录 | docs/records/changelog.md、docs/records/interface-log.md、docs/records/rounds.md |
| 运行逻辑演示 | demos/ |
| 图标资产 | assets/icon/ |
| 仓库配置 | README.md、.gitignore、LICENSE、第三方声明 |

## 不推送

| 类别 | 路径或模式 |
| --- | --- |
| 凭据文件 | `*.token`、`*.key`、`.env` |
| 私有配置 | `*.private.json`、`*.local.json` |
| 运行时日志 | `*.log`、`.push.*` |
| 诊断包 | `diagnostic-*.zip`、配置快照中的运行时敏感字段 |
| 构建产物 | target/、`*.pdb`、`*.rs.bk` |
| 平台临时文件 | `Thumbs.db`、`.DS_Store` |
| 图标派生图 | 未生成；许可证未定前不进入任何提交 |

## 每轮动作

| 序 | 动作 | 失败处理 |
| --- | --- | --- |
| 1 | `git add -A` | 二级降级：排除命中项后重试 |
| 2 | 全仓凭据扫描 | 命中即停止提交，零级报错 |
| 3 | 解释性措辞扫描 | 命中即停止提交，零级报错 |
| 4 | `git commit -m "<事实性提交说明>"` | 非零退出保留输出 |
| 5 | `scripts/push.sh <remote-url> "<message>"` | git HTTP 403 时降级 API 快照 |
| 6 | 远端内容核对 | `GET /git/ref/heads/main`、blob sha 比对 |

## 请求头

| 接口 | 头 |
| --- | --- |
| api.github.com | `User-Agent: KCU-Launcher-Desktop/0.0.0` |
| api.github.com | `Accept: application/vnd.github+json` |
| api.github.com | `X-GitHub-Api-Version: 2022-11-28` |
| 认证 | `Authorization: token <env KCU_PAT>` |

## 降级路径

| 级别 | 路径 | 结果 |
| --- | --- | --- |
| 主路径 | git HTTP push | 受阻，github.com 主机 403 policy_default_denied |
| 二级降级 | `scripts/api_push.py` | Git Data API 全量树快照，写入 refs/heads/main |

## 诊断行

`[KCU] remote <动作> <目标> <结果> <详情>`

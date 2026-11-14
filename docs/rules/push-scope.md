# 远端推送范围

轮次：023

远端：`kongbai9288/KCU-launcher-for-pc`，public，分支 main。
特殊版：`kongbai9288/KCU-launcher-special`，private，分支 main，仅 README 占位。

## 允许推送

| 类别 | 路径 |
| --- | --- |
| 代码 | src/、Cargo.toml、Cargo.lock |
| 构建配置 | Cargo.toml profile 段；不含密钥、不含绝对路径、不含目标三元组硬编码 |
| CI 工作流 | `.github/workflows/ci.yml`，secrets 与 vars 只写引用，不写值 |
| 脚本 | scripts/push.sh、scripts/api_push.py、scripts/render_ui.py |
| 事实性文档 | docs/spec/、docs/research/、docs/features/、docs/decisions/、docs/checklists/、docs/rules/、docs/records/、docs/verification/ |
| 版本与接口记录 | docs/records/changelog.md、docs/records/interface-log.md、docs/records/rounds.md |
| 运行逻辑演示 | demos/ |
| 图标资产 | assets/icon/、assets/icons/（lucide 子集与 manifest） |
| UI 设计稿 | assets/ui/，逐字副本与资产登记 |
| 设计矩阵 | docs/design/，全功能使用逻辑矩阵 |
| 020 设计契约 | docs/design/，槽位 / 推荐 / 状态 / 上层候选 / 交接基线 |
| 020 调研 | docs/research/17-plugin-settings-survey.md |
| 改造脚本 | scripts/round020_ui.py、scripts/round020_views.py |
| 021 改造脚本 | scripts/round021_ui.py、scripts/round021_js.py |
| 021 调研与设计 | docs/research/18-server-list-autodiscovery.md、docs/design/server-list-logic.md、docs/design/ui-product-copy.md |
| 022 改造脚本 | scripts/round022_async.py、scripts/round022_docs.py、scripts/round022_index.py |
| 022 调研与设计 | docs/research/19-async-probe-budget.md、docs/design/async-probe-policy.md |
| 023 改造脚本 | scripts/round023_ux.py、scripts/round023_i18n_cover.py、scripts/round023_docs.py、scripts/round023_index.py |
| 023 调研与设计 | docs/research/20-i18n-crash-identity.md、docs/design/ 四份策略文档 |
| 发行物声明 | THIRD-PARTY-NOTICES.md |
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
| 平台 API 凭据 | 用户当轮未提供；任何取值不进入本公仓、注释、提交说明、日志 |
| 特殊版内容 | 单开私仓构建，不进入本公仓 |
| 只读后端仓内容 | 端点、密钥、部署配置、README 正文不复制进本公仓 |

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
| 空仓库初始化 | `PUT /contents/README.md` | 空仓库 `POST /git/blobs` 返回 409 `Git Repository is empty.`，初始化后可用 |

## 只读仓约束

| 编号 | 内容 |
| --- | --- |
| R01 | 对用户后端仓只允许 `GET`；任何写请求触发零级停止。 |
| R02 | 不读取该仓正文进公仓；不 fork、不改分支、不建 issue。 |
| R03 | 本轮已核：4 个 `GET`、0 个写请求，见 docs/research/15-input-survey.md BR02。 |
| R04 | 每轮重新声明本约束。 |

## 特殊版

| 项 | 值 |
| --- | --- |
| 形态 | 单开私仓，已创建 |
| 地址 | `kongbai9288/KCU-launcher-special`，private，main，HEAD `cd7fc97` |
| 当前内容 | README 占位，仅事实表；无代码、无凭据、无后端仓内容 |
| 放代码条件 | 用户明确同意后；用户手拉工具流 |
| 触发 | 所有任务完成且反复检查未发现漏洞 |
| 使用者 | 用户与其朋友 |
| 正常版本 | 镜像或用户后端，用户后端仅境外场景可连 |
| 凭据 | workflow secrets 占位，值由用户填写 |

## 诊断行

`[KCU] remote <动作> <目标> <结果> <详情>`

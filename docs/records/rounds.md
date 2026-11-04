# 轮次变更记录

## 001

| 落点 | 内容 |
| --- | --- |
| .gitignore | 忽略构建产物、日志、凭据文件 |
| README.md | 项目事实索引 |
| docs/index.md | 文档索引、每轮必读顺序、开工检查命令 |
| docs/spec/00-requirements.txt | 需求原文逐字副本，261 行 |
| docs/spec/01-round-001-instructions.txt | 当轮指令逐字副本，5 行 |
| docs/research/*.md | 9 份主题事实条目与索引 |
| docs/features/index.md | 功能登记索引，当前无条目 |
| docs/features/_template.md | 功能 md 模板，5 个固定字段 |
| docs/decisions/index.md | 决策索引，框架蓝图待确认 |
| docs/checklists/*.md | AI 与 Windows 防错清单 |
| docs/rules/*.md | 证明规则与兜底规则 |
| docs/records/*.md | 版本、接口、轮次记录 |
| demos/round-001-dispatch.html | 统一调度器运行逻辑 HTML |
| src/ | 空目录 |

未做：
- 源码
- 远程仓库创建
- 框架蓝图落盘
- 功能实现

## 002

| 落点 | 内容 |
| --- | --- |
| docs/spec/02-round-002-instructions.txt | 当轮指令逐字副本，1 行 |
| assets/icon/kcu-launcher.jpg | 图标原始字节，175816 字节，JPEG 1440x1440 |
| docs/decisions/002-icon.md | 图标资产决策记录 |
| docs/decisions/index.md | 加入 002 条目与三项待确认 |
| docs/index.md | 必读顺序扩为 10 项，分区加入资产与 002 演示 |
| README.md | 轮次 002，仓库状态与图标路径 |
| docs/records/rounds.md | 本段落 |
| demos/round-002-icon.html | 图标资产登记运行逻辑 HTML |

格式纠正：

| 位置 | 原因 | 修复动作 |
| --- | --- | --- |
| assets/icon/kcu-launcher.png（重命名前路径，已不存在） | 源文件名为 .png，魔数为 JPEG，扩展名与格式不一致 | 重命名为 assets/icon/kcu-launcher.jpg，字节未改动，SHA-1 一致 |

未做：
- 源码
- 远程仓库创建
- 框架蓝图落盘
- 正常模式 UI 落盘
- ICO 与裁切版本
- 功能实现

## 003

| 落点 | 内容 |
| --- | --- |
| docs/spec/03-round-003-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/decisions/003-remote.md | 远端公仓、每轮推送、搭建阶段决策记录 |
| docs/decisions/index.md | 加入 003 条目与触发条件待确认 |
| docs/rules/push-scope.md | 允许推送与不推送清单、每轮动作、诊断行 |
| scripts/push.sh | 参数化远端推送入口，无 URL 硬编码 |
| .gitignore | 追加私有配置、诊断包、探测文件排除项 |
| docs/index.md | 必读顺序扩为 12 项，分区加入推送规则、脚本与 003 演示 |
| README.md | 轮次 003，仓库形态与当前阶段 |
| docs/records/rounds.md | 本段落；002 格式纠正表标注重命名前路径 |
| demos/round-003-remote.html | 远端推送与搭建阶段运行逻辑 HTML |
| 首个本地提交 | 001-003 全部产物纳入版本控制，署名 yuanbao |

远端探测结果：

| 请求 | 状态码 | 结果 |
| --- | --- | --- |
| GET /rate_limit 带完整请求头 | 200 | 已证实 |
| GET /rate_limit 无 User-Agent | 403 | 已证实 |
| POST /user/repos 无认证 | 401 Requires authentication | 受阻 |

未做：
- 远端公仓创建与推送
- 源码
- 框架蓝图落盘
- 正常模式 UI 落盘
- 底层统一搭建

## 004

| 落点 | 内容 |
| --- | --- |
| docs/spec/04-round-004-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/decisions/004-remote-created.md | 公仓创建、名称规范化、网络边界、降级路径 |
| docs/decisions/index.md | 加入 004 条目 |
| docs/rules/push-scope.md | 远端地址、请求头、降级路径、blob sha 核对 |
| scripts/api_push.py | Git Data API 全量树快照，凭据只读环境变量 |
| scripts/push.sh | 重写为 git HTTP 失败后自动降级 API 快照 |
| docs/index.md | 必读顺序扩为 13 项，加入远端信息与 004 演示 |
| README.md | 轮次 004，远端地址、可见性、推送路径 |
| docs/records/rounds.md | 本段落 |
| demos/round-004-remote.html | 公仓创建与 API 快照推送运行逻辑 HTML |
| docs/verification/round-004.md | 第 004 轮独立验证报告，结论部分通过 |

远端动作：

| 动作 | 结果 |
| --- | --- |
| `GET /user`，`Authorization: Bearer` | 403 policy_default_denied |
| `GET /user`，`Authorization: token` | 200，login=kongbai9288 |
| `POST /user/repos`，name=`KCU launcher for pc` | 201，实际名 `KCU-launcher-for-pc` |
| `GET /repos/kongbai9288/KCU-launcher-for-pc` | 200，private=false，default_branch=main |
| git HTTP push，三种认证方式 | 受阻，github.com 主机 403 policy_default_denied |
| `POST /git/blobs`，空仓库未初始化 | 409 `Git Repository is empty.` |
| `PUT /contents/README.md` | 201，初始提交 d0acb0d |
| `scripts/api_push.py` | 启用，二级降级；首次快照 c76f491，42 文件 |

名称差异：

| 输入 | 实际 |
| --- | --- |
| `KCU launcher for pc` | `KCU-launcher-for-pc` |
| 原串 | 保留在 repository description |

未做：
- 源码
- 框架蓝图落盘
- 正常模式 UI 落盘
- 底层统一搭建

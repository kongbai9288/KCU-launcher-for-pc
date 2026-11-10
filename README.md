# KCU Launcher Desktop

| 项 | 值 |
| --- | --- |
| 名称 | KCU Launcher |
| 平台 | Windows 桌面 |
| 语言 | Rust |
| 署名 | yuanbao |
| 仓库形态 | GitHub 远端公仓，独立仓库 |
| 远端 | https://github.com/kongbai9288/KCU-launcher-for-pc |
| 可见性 | public |
| 分支 | main |
| 推送路径 | git HTTP 受阻；REST Git Data API 全量树快照 |
| 当前轮次 | 012 |
| 当前阶段 | 功能输入阶段，未启动底层统一搭建 |
| 图标 | assets/icon/kcu-launcher.jpg |
| 正常模式 UI 设计稿 | assets/ui/normal-mode-v3.html |
| 轻量模式 UI | 独立极简视图，不复用正常模式 UI |
| 功能登记 | docs/features/index.md，F001-F012 已批准未实现；011 输入 55 条 + 175 项见 backlog.md；012 开服器输入 27 个编号位见 server-backlog.md |
| 待拍板问题 | docs/records/open-questions.md，93 条，A-H 组，全部未答复 |
| 一手补证 | RCON 与 UUID、底层运行时、合规条款、Win7 与多架构系统 API、批量请求通用法、开服器官方资料，见 docs/research/index.md |
| 许可证原文 | docs/licenses/index.md，逐字副本 13 份 + slint 三许可全文 3 份 |
| 需求 15 节待办 | 4 条已推进，见 docs/research/11-runtime.md、12-compliance.md、13-platform-api.md |
| 搭建前置条件 | docs/rules/build-preconditions.md，条件 1-6 均未满足 |
| 合规卡点 | X01-X04、Win7 兼容路径、ops.json 回写、UPnP / mclo.gs / mrpack 安全边界已证实，进入构建前需用户拍板 |
| 后端仓 | 只读，仅 GET，内容不进公仓 |
| 特殊版 | 单开私仓，所有任务完成且复核无漏洞后构建 |
| 框架蓝图 | docs/decisions/005-blueprint.md，状态未批准 |
| 许可证 | 未确定 |

## 目录

| 路径 | 内容 |
| --- | --- |
| docs/index.md | 文档索引与每轮必读顺序 |
| docs/spec/ | 需求原文与逐轮指令副本 |
| docs/research/ | 官方文档与开发者经验事实条目 |
| docs/licenses/ | 第三方许可证逐字副本与索引 |
| docs/features/ | 功能登记 |
| docs/decisions/ | 决策记录 |
| docs/checklists/ | 防错清单 |
| docs/rules/ | 证明规则、兜底规则、推送范围 |
| docs/records/ | 版本、接口、轮次记录 |
| docs/verification/ | 独立验证报告 |
| demos/ | 运行逻辑 HTML |
| scripts/push.sh | 推送入口，自动降级 |
| scripts/api_push.py | Git Data API 全量树快照 |
| assets/icon/ | 启动器图标 |
| assets/ui/ | 正常模式 UI 设计稿逐字副本与登记 |
| src/ | 源码目录，当前为空 |

## 四值

已证实 / 已失败 / 未证实 / 受阻。定义见 docs/rules/proof-rules.md。

## 诊断行格式

`[KCU] <域> <动作> <目标> <结果> <详情>`

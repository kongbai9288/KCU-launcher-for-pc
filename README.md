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
| 当前轮次 | 013 |
| 当前阶段 | D06 已触发、D07 已启用；第 1 层 core 已落地，其余 8 层未启动 |
| 图标 | assets/icon/kcu-launcher.jpg |
| 正常模式 UI 设计稿 | assets/ui/normal-mode-v3.html |
| 轻量模式 UI | 独立极简视图，不复用正常模式 UI |
| 功能登记 | docs/features/index.md；F001-F012 已批准未实现；F013-01..09 core 九模块已实现、已验证 |
| 开工依据 | 013 轮 F07/F08/F09；答复台账 docs/records/round-013-answers.md；决策 docs/decisions/013-build-start.md |
| 待拍板问题 | 93 条已答复，细节按用户逻辑落地 |
| 工具链 | rustc / cargo 1.99.1，腾讯 rustup 镜像；`cargo build --release --offline` 与 `cargo test --offline`（37 passed）实测通过 |
| 一手补证 | RCON 与 UUID、底层运行时、合规条款、Win7 与多架构系统 API、批量请求通用法、开服器官方资料，见 docs/research/index.md |
| 许可证原文 | docs/licenses/index.md，逐字副本 13 份 + slint 三许可全文 3 份 |
| 搭建前置条件 | docs/rules/build-preconditions.md，条件 1-6 已满足到开工层；L1 已实现已验证 |
| 合规卡点 | X01-X04 按 F10 以正常情况与用户逻辑落地；CF 下载模块不在 L1 范围 |
| 后端仓 | 只读，仅 GET，内容不进公仓 |
| 特殊版 | 先建私仓、用户同意后再放代码、用户手拉工具流（F63） |
| 框架蓝图 | docs/decisions/005-blueprint.md，状态已批准（F09） |
| 许可证 | F61 决定 GPLv3；LICENSE 文件未生成 |

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
| Cargo.toml | crate 配置，std only，profile 取值已核实 |
| src/lib.rs、src/core/ | 013 轮 L1 core，9 个模块，37 个单元测试 |

## 四值

已证实 / 已失败 / 未证实 / 受阻。定义见 docs/rules/proof-rules.md。

## 诊断行格式

`[KCU] <域> <动作> <目标> <结果> <详情>`

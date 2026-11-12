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
| 当前轮次 | 016 |
| 当前阶段 | D06 已触发、D07 已启用；第 1 层 core、第 2 层 dispatcher、第 3 层 lightweight 已落地，其余 6 层未启动 |
| 图标 | assets/icon/kcu-launcher.jpg |
| 正常模式 UI 设计稿 | assets/ui/normal-mode-v3.html，014 轮起为样板与交互参考，不直接复用 |
| 轻量模式 UI | 独立极简视图，不复用正常模式 UI |
| UI 整页演示闸门 | docs/rules/ui-demo.md；016 轮首次触发，已交付 `demos/ui-full-lightweight.html`，用户手感调整优先于实现 |
| 功能登记 | docs/features/index.md；F001、F004-F012 已批准未实现；F002、F003、F013-01..09、F014-01..03、F015-01..04、F016-01..04 已实现、已验证 |
| 开工依据 | 013 轮 F07/F08/F09；答复台账 docs/records/round-013-answers.md；015 决策 docs/decisions/015-build-continue.md |
| 待拍板问题 | 93 条已答复，细节按用户逻辑落地 |
| 工具链 | rustc / cargo 1.99.1，腾讯 rustup 镜像；`cargo build --release --offline` 与 `cargo test --offline`（141 passed）实测通过 |
| 一手补证 | RCON 与 UUID、底层运行时、合规条款、Win7 与多架构系统 API、批量请求通用法、开服器官方资料，见 docs/research/index.md |
| 许可证原文 | docs/licenses/index.md，逐字副本 13 份 + slint 三许可全文 3 份 |
| 搭建前置条件 | docs/rules/build-preconditions.md，条件 1-6 已满足到开工层；L1、L2、L3 已实现已验证 |
| L2 dispatcher | src/dispatcher/，task / mode / launcher + json 底座；模式判定、安全模式、正版凭据闸门、UI 分流、单参数进服、双击按权重选实例 |
| L3 lightweight | src/lightweight/，login / download / loaders / view；三种登录、三级回退、批量请求每页 20、6 加载器、单主题、游戏运行期无常驻进程 |
| 整页 UI 演示 | demos/ui-full-lightweight.html，016 轮首次触发；6 分区、5 状态、11 弹窗、手感调整区、离线可点；实现未进构建 |
| 合规卡点 | X01-X04 按 F10 以正常情况与用户逻辑落地；CF 下载模块不在 L1/L2 范围 |
| 缓存 / 异步 / 泄漏 | core.cache、core.asynk、core.leak 已实现已验证；CI 有界缓存与并发取消已配置 |
| 工作流环境变量 | `.github/workflows/ci.yml` 设 `KCU_CF_API_KEY` 等 secrets / vars 占位，值由用户填写 |
| CI | 腾讯 rustup 镜像、actions/cache 有界、concurrency 取消、core 与 scan 并行 job |
| 后端仓 | 只读，仅 GET，内容不进公仓 |
| 特殊版 | `kongbai9288/KCU-launcher-special`，private，014 轮已建仓，仅 README 占位；代码待用户同意 |
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
| docs/rules/ | 证明规则、兜底规则、推送范围、UI 整页演示闸门 |
| docs/records/ | 版本、接口、轮次记录 |
| docs/verification/ | 独立验证报告 |
| demos/ | 运行逻辑 HTML |
| scripts/push.sh | 推送入口，自动降级 |
| scripts/api_push.py | Git Data API 全量树快照 |
| assets/icon/ | 启动器图标 |
| assets/ui/ | 正常模式 UI 设计稿逐字副本与登记 |
| Cargo.toml | crate 配置，std only，profile 取值已核实 |
| src/lib.rs、src/core/ | L1 core，12 个模块 |
| src/dispatcher/ | L2 dispatcher，5 个模块，47 项单元测试 |
| src/lightweight/ | L3 lightweight，5 个模块，38 项单元测试 |
| demos/ui-full-lightweight.html | 整页 UI 演示，手感调整入口 |
| 测试命令 | `cargo test --offline` 141 passed / 0 failed；`cargo build --release --offline` 通过 |
| .github/workflows/ci.yml | CI 工作流，secrets / vars 占位、有界缓存、并发取消 |

## 四值

已证实 / 已失败 / 未证实 / 受阻。定义见 docs/rules/proof-rules.md。

## 诊断行格式

`[KCU] <域> <动作> <目标> <结果> <详情>`

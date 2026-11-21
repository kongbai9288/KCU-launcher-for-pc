# AX01–AX24 功能池（064 全量决断）

用户 064 当轮：「全部（不与我们的项目冲突的情况下）」。逐条状态与冲突判定如下。`Planned` ≠ 未批准，是已批准、未实现。起手顺序按工程依赖，不排推荐优先级。

| 编号 | 语义 slug | 状态 | 冲突 | 本轮落点 |
| --- | --- | --- | --- | --- |
| AX01 | home_widgets | Planned | — | 排队（UI 框架 EQ-01） |
| AX02 | game_news | Planned | — | 排队（真实网络 IO 未启动） |
| AX03 | world_editor | Planned | — | 排队（vianbt 11-6） |
| AX04 | mod_rollback | Planned | — | 排队（036 决策 / EQ-13） |
| AX05 | storage_analysis | **DataLayer** | — | `src/core/storage.rs` 已落地 |
| AX06 | download_history | Planned | — | 排队（端点配置化 050） |
| AX07 | doh_support | Planned | network_io_not_started | 排队；技术受阻非需求冲突 |
| AX08 | instance_import | Planned | — | 排队（路径边界 robust） |
| AX09 | upgrade_compat | Planned | — | 排队（034 / 036 / 037） |
| AX10 | first_run_wizard | Planned | — | 排队（00-12 声明页顺序） |
| AX11 | settings_export | Planned | — | 排队（035 配置归一化） |
| AX12 | download_sources | Planned | — | 排队（00-171 密钥不写死） |
| AX13 | appearance_modes | Planned | — | 排队（11-38 深色模式扩展） |
| AX14 | skin_editor | Planned | — | 排队（11-40 预览扩展） |
| AX15 | studio_image_editor | Planned | — | 排队（许可证合规 00-26） |
| AX16 | cn_search_filter | Planned | — | 排队（042 批量编码） |
| AX17 | banner_designer | Planned | — | 排队（零新增第三方） |
| AX18 | lab_generators | Planned | ai_provider_ui_excluded | 配方 / 渐变 / 模组翻译保留；AI 提供商配置页**排除** |
| AX19 | seed_map | Planned | — | 排队（12-14 / 12-50 种子权限） |
| AX20 | projection_workshop | Planned | — | 排队（11-41 预览扩展） |
| AX21 | redstone_multiplayer | Planned | — | 排队（第三方服务端点配置化） |
| AX22 | shimu_account | Planned | — | 排队（境外限制 054） |
| AX23 | client_ai_gate | **GateOnly** | 11:18 gate_only_no_ui | `src/core/client_ai.rs` + v1 第 7 符号；无页面 |
| AX24 | ungrouped_drop | Planned | — | 排队（robust 路径边界） |

## 冲突处置

| 项 | 处置 |
| --- | --- |
| AX23 与 `11:18` | 用户裁决「只留一个口子，不给用户操作页面」：不留 MCP Server、不留 AI 客户端配置片段、不留界面观察；内部类型默认拒绝 |
| AX18 AI 提供商配置页 | 排除该子项 |
| `12-4` 开服器 AI | 不受影响：服务端工具、不赋删除权限、用户手动同意 |

## 约束

- 不复制 Axolotl（GPL-3.0-only）源码；功能按 `11:26` / `00:26` 用已进构建的库实现。
- 所有新弹窗进 `POPUP_SPECS`；所有新公共符号进 `api::v1`；注册表不承载中文 UI 文案。
- 24 项全量决断，但 UI 渲染实现按 063 起的口径「等手感反馈」，UI 闸门未触发前只落数据层与编排。
- 功能池由 `ax_guard.py` 守：24 条唯一、AX23 `GateOnly` + `ui=false`、AX05 `DataLayer`、AX18 排除项留痕、其他文件不得重复声明。

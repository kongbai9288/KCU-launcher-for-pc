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

## 065 补记：AX11 状态覆盖

| 编号 | 064 行 | 065 覆盖 |
| --- | --- | --- |
| AX11 | `Planned` / 排队（035 配置归一化） | **`DataLayer`**：`src/core/settings_io.rs` 已落地导出差集、导入逐键校验、清理回默认；设置页输入控件等 UI 渲染仍未启动 |

状态分层更新为 `Planned 21` / `DataLayer 2`（AX05、AX11）/ `GateOnly 1`（AX23）。`ax_guard.py` 改为动态求和并显式断言 AX05 / AX11，不降断言。064 历史表格行不重写，本补记覆盖结论。

E192：`privacy-consent.json` 与设置文件同目录，清理若按目录清空会抹掉同意记录并绕过 `11:10`。四个状态文件改为表驱动保护，清理只回写内置默认、不删文件。

## 066 补记：AX06 状态覆盖

| 编号 | 064 行 | 066 覆盖 |
| --- | --- | --- |
| AX06 | `Planned` / 排队（端点配置化 050） | **`DataLayer`**：`src/core/download_history.rs` 已落地本地记录、去重饱和、8 类坏输入、原子写、reset 保护；顶部栏任务进度常驻显示属 UI，未启动 |

状态分层更新为 `Planned 20` / `DataLayer 3`（AX05、AX06、AX11）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到 AX05 / AX06 / AX11，动态求和不变。064、065 历史表格行不重写，本补记覆盖结论。

`api::v1` 7 符号不变：AX06 是内部数据层，不扩公共面（`00:137` 接口终点核对）。

## 067 / 068 补记：功能池不动

用户 067 给两段新功能，按 `00:248` 覆盖 066 结尾「按功能池落下一项」预告。`Planned 20` / `DataLayer 3`（AX05、AX06、AX11）/ `GateOnly 1`（AX23）全部不变，`ax_guard.py` 不改。064–066 历史表格行不重写。067 两模块不进 AX 池，属用户当轮原文条目，登记在 `docs/decisions/067-extension-gate-and-launch-progress.md`。

## 069 补记：AX12 状态覆盖

| 编号 | 064 行 | 069 覆盖 |
| --- | --- | --- |
| AX12 | `Planned` / 排队（`00-171` 密钥不写死） | **`DataLayer`**：`src/core/download_sources.rs` 已落地三档策略、严格白名单、密钥缺失降级镜像、受限清单、原子写；下载页 UI 与真实下载 IO 未启动 |

状态分层更新为 `Planned 19` / `DataLayer 4`（AX05、AX06、AX11、AX12）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到四项，动态求和不变（A240）；`src/core/ax.rs` 测试断言同步为 `DataLayer 4` / `Planned 19`。064–068 历史表格行不重写，本补记覆盖结论。

`api::v1` 7 符号不变：AX12 是内部数据层，不扩公共面（`00:137`）。

## 070 补记：AX24 状态覆盖

| 编号 | 064 行 | 070 覆盖 |
| --- | --- | --- |
| AX24 | `Planned` / 排队（robust 路径边界） | **`DataLayer`**：`src/core/instance_drop.rs` 已落地未分组集合、三类别落点计算、路径边界、原子写；内容探测、真实文件移动、拖拽 UI 未启动 |

状态分层更新为 `Planned 18` / `DataLayer 5`（AX05、AX06、AX11、AX12、AX24）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到五项，动态求和不变（A240）；`src/core/ax.rs` 测试断言同步为 `DataLayer 5` / `Planned 18`。064–069 历史表格行不重写，本补记覆盖结论。069 的 D-069-1「AX24 内容探测范围更深」是相对 AX12 的排序理由，本轮收窄范围后落地，见 `docs/decisions/070-instance-drop.md` D-070-2。

`api::v1` 7 符号不变：AX24 是内部数据层，不扩公共面（`00:137`）。

## 071 补记：AX17 状态覆盖

| 编号 | 064 行 | 071 覆盖 |
| --- | --- | --- |
| AX17 | `Planned` / 排队（零新增第三方、许可证合规、UI 框架卡 EQ-01） | **`DataLayer`**：`src/core/banner_design.rs` 已落地图案分层、有界撤销重做栈、最近编辑记录、严格白名单、原子写；give 命令与现代 / 旧版语法兼容、画布渲染、真实导入导出未启动 |

状态分层更新为 `Planned 17` / `DataLayer 6`（AX05、AX06、AX11、AX12、AX17、AX24）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到六项，动态求和不变（A240）；`src/core/ax.rs` 测试断言同步为 `DataLayer 6` / `Planned 17`。064–070 历史表格行不重写，本补记覆盖结论。065 决策曾把 AX17 列入「重 UI 卡 EQ-01」排除表，按 070 对 AX24 的处置口径收窄范围后落地，见 `docs/decisions/071-banner-design.md` D-071-3。

`api::v1` 7 符号不变：AX17 是内部数据层，不扩公共面（`00:137`）。

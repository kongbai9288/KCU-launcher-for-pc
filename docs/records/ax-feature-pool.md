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

## 072 补记：AX01 状态覆盖

| 编号 | 064 行 | 072 覆盖 |
| --- | --- | --- |
| AX01 | `Planned` / 排队（每页可扩展统一格式、UI 框架卡 EQ-01） | **`DataLayer`**：`src/core/widget_layout.rs` 已落地模式 / 槽位顺序 / 固定项 / 有界容量 / 严格白名单 / 原子写；拖拽渲染、组件真实数据接入、固定项绑定语义未启动 |

状态分层更新为 `Planned 16` / `DataLayer 7`（AX05、AX06、AX11、AX12、AX17、AX24、AX01）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到七项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 7` / `Planned 16`。064–071 历史表格行不重写，本补记覆盖结论。069 的 D-069-1「AX01 卡 EQ-01」是相对 AX12 的排序理由，本轮收窄范围后落地，见 `docs/decisions/072-widget-layout.md` D-072-3。

`api::v1` 7 符号不变：AX01 是内部数据层，不扩公共面（`00:137`）。

## 073 补记：AX13 状态覆盖

| 编号 | 064 行 | 073 覆盖 |
| --- | --- | --- |
| AX13 | `Planned` / 排队（i18n 语言包、UI 框架卡 EQ-01、图标集中一个文件） | **`DataLayer`**：`src/core/appearance.rs` 已落地四模式枚举 / 可选强调色 / 有界预设 / 两布尔开关 / 6+2+4 键白名单 / 原子写；主题渲染、背景图加载、强调色应用未启动 |

状态分层更新为 `Planned 15` / `DataLayer 8`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到八项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 8` / `Planned 15`。064–072 历史表格行不重写，本补记覆盖结论。069「AX13 卡 EQ-01」是相对排序理由，本轮收窄范围后落地，见 `docs/decisions/073-appearance.md` D-073-3。

`api::v1` 7 符号不变：AX13 是内部数据层，不扩公共面（`00:137`）。

## 074 补记：AX10 状态覆盖

| 编号 | 064 行 | 074 覆盖 |
| --- | --- | --- |
| AX10 | `Planned` / 排队（统一调度器内置 json 与声明页、弹窗注册表、i18n 语言包） | **`DataLayer`**：`src/core/first_run.rs` 已落地可回退步骤序列 / 三态枚举 / 必选约束 / 有界容量 / 4+3+3 键白名单 / 原子写；向导 UI、Java 真实检测、账号绑定、`.kculf` 解析未启动 |

状态分层更新为 `Planned 14` / `DataLayer 9`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到九项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 9` / `Planned 14`。064–073 历史表格行不重写，本补记覆盖结论。`11:242` 的两天计时 / 手动装拓展包两条启用路径按 A250 都不落，登记 Q-074-02；向导步骤目录来源登记 Q-074-01。

`api::v1` 7 符号不变：AX10 是内部数据层，不扩公共面（`00:137`）。

## 075 补记：AX14 状态覆盖

| 编号 | 064 行 | 075 覆盖 |
| --- | --- | --- |
| AX14 | `Planned` / 排队（UI 框架卡 EQ-01、签名校验优先、零新增第三方） | **`DataLayer`**：`src/core/skin_draft.rs` 已落地并列草稿集合 / 两类分类 / 双态 / 保存间隔上限 / 激活项与离开提醒 / 4+4+2+2 键白名单 / 原子写；皮肤编辑器 UI、纹理导出、3D 旋转预览、皮肤下载未启动 |

状态分层更新为 `Planned 13` / `DataLayer 10`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10、AX14）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到十项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 10` / `Planned 13`。064–074 历史表格行不重写，本补记覆盖结论。`31-axolotl-launcher-features.md:80` 把 AX14 列为「重 UI、渲染方案未定」，按 070–074 处置口径收窄为不碰 UI 渲染后落地；AX15 因与 `banner_design.rs` 撤销重做栈同构，本轮排除并留痕（E276）。草稿保存间隔实际值与「已保存 / 原版」判定口径登记 Q-075-01；按玩家名 / UUID 查询与 PNG 下载的 OR 两路径都不落，登记 Q-075-02。

`api::v1` 7 符号不变：AX14 是内部数据层，不扩公共面（`00:137`）。

## 076 补记：AX09 状态覆盖

| 编号 | 064 行 | 076 覆盖 |
| --- | --- | --- |
| AX09 | `Planned` / 排队（semver 版本比较 034、036 更新决策、037 手动同意升级） | **`DataLayer`**：`src/core/upgrade_plan.rs` 已落地按 id 索引候选项集合 / 三值兼容性 / 三选一决策 / 单条确认且 defer 拒收 / conflict 自动回退 / 派生页码 / 3+6+3+3 键白名单 / 原子写；真实目录复制、升级执行、版本比较执行、升级决策 UI 未启动 |

状态分层更新为 `Planned 12` / `DataLayer 11`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10、AX14、AX09）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到十一项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 11` / `Planned 12`。064–075 历史表格行不重写，本补记覆盖结论。AX09 口径里的 034 / 036 / 037 均为已实现模块（`src/updater/policy.rs` / `src/plugins/upgrade.rs`），不是待拍板 EQ；EQ-13 只挂在 AX04（`ax-feature-pool.md:10`），本轮不碰 AX04。AX02 / AX07 / AX21 / AX22 依赖真实网络 IO / 境外限制，AX03 / AX19 / AX20 依赖 NBT 或投影解析库，AX08 依赖 zip 解析库，AX16 / AX18 属 063 低可信度转述且 AI 提供商配置页已被 062 排除，AX15 与 `banner_design.rs` 撤销栈同构（075 E276），逐项不动并留痕。真实执行层与 `conflict` 强制升级口径登记 Q-076-01 / Q-076-02。

`api::v1` 7 符号不变：AX09 是内部数据层，不扩公共面（`00:137`）。

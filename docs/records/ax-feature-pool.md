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

## 077 补记：AX16 状态覆盖

| 编号 | 064 行 | 077 覆盖 |
| --- | --- | --- |
| AX16 | `Planned` / 排队（端点配置化、批量请求 11-14、percent-encoding 042） | **`DataLayer`**：`src/core/search_filter.rs` 已落地谓词集合 / 排除集合 / 排序规格 / 保存条件 / 历史 / 派生过滤与排序 / 7+5+2+2+5+4 键白名单 / 原子写；真实目录遍历、结果批量操作、快照解析、筛选 UI 未启动 |

状态分层更新为 `Planned 11` / `DataLayer 12`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10、AX14、AX09、AX16）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到十二项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 12` / `Planned 11`。064–076 历史表格行不重写，本补记覆盖结论。

**AX16 与 076 排除清单的关系**：076 补记把 AX16 归到「063 低可信度转述」不动，是相对排序理由而非永久否决。073 的 AX13 同属 063 的 6 项低可信度转述，已按「只取项目原文已决断语义、不取转述具体色号」落地（Q-073-01 留痕）；075 的 AX14 也按「卡 EQ-01 是相对排序理由，收窄为不碰 UI 渲染」处置。本轮照此先例：只取 `11:94-123` / `11:205` / `11:206` / `11:208` 四组 25 条项目原文已决断语义，**不取**「PCL 社区 WikiEntries 数据快照」「中文关键词」「作者 / 环境 / 加载器」这些第三方转述的具体实现，登记 Q-077-01 / Q-077-02。`00:175` 与 `11:206` 的复用要求由「条件维度与排序维度共用 `DIMENSIONS` 一张表、文件管理搜索与模组资源搜索共用本模块」落地（E284 实质缓解）。

AX02 / AX07 / AX21 / AX22 依赖真实网络 IO / 境外限制，AX03 / AX19 / AX20 依赖 NBT 或投影解析库，AX08 依赖 zip 解析库，AX04 的 EQ-13 与 Q-047-01 未拍板，AX15 与 `banner_design.rs` 撤销栈同构（075 E276），AX18 AI 提供商配置页已被 062 排除且生成器缺已决断原文锚点，逐项不动并留痕。

`api::v1` 7 符号不变：AX16 是内部数据层，不扩公共面（`00:137`）。

## 078 补记：AX18 状态与「缺锚点」判定覆盖

| 编号 | 064 行 | 078 覆盖 |
| --- | --- | --- |
| AX18 | `Planned` / `ai_provider_ui_excluded` / 配方 / 渐变 / 模组翻译保留，AI 提供商配置页排除 | **`DataLayer`**：`src/core/generator_session.rs` 已落地并列会话集合 / 三类生成器 / 三值状态 / 双输出格式 / 翻译条目表 / 派生可复制候选 / 5+6+4+3+2+3 键白名单 / 原子写；`conflict` 保留 `ai_provider_ui_excluded`；生成算法、剪贴板写入、翻译执行、AI 提供商端点、UI 渲染未启动 |

状态分层更新为 `Planned 10` / `DataLayer 13`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10、AX14、AX09、AX16、AX18）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到十三项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 13` / `Planned 10`。064–077 历史表格行不重写，本补记覆盖结论。

**A201 覆盖 077 补记的判定**：`:161` 写「AX18 AI 提供商配置页已被 062 排除且**生成器缺已决断原文锚点**，逐项不动并留痕」。本轮 A211 真读 `11-features-input.txt` 268 行与 `12-server-features-input.txt` 64 行全文后，由 `11:29`「模组尽量去重聚合，可以引入翻译源」、`11:210` 第 3 条「支持模组界面翻译」、`11:240` 第 32 条「支持我的世界颜色代码一键复制（包括旧的格式与新json格式）」、`12:6` 第 6 条「快速标注，通过颜色区分mod名称等」推翻「缺锚点」这半句；`11:247` 第 39 条结果四段字段形态作为不透明快照依据。「AI 提供商配置页已被 062 排除」这半句仍成立：`:24` / `:37` 明写排除的是**一个子项**，配方 / 渐变 / 模组翻译三个子项明写「保留」，本轮 `conflict` 字段不动、端点与密钥不落、Q-078-01 留痕。073 AX13、075 AX14、077 AX16 均按同一「相对排序理由 + 收窄不碰 UI 渲染」先例落地，本轮照此执行。

`api::v1` 7 符号不变：AX18 是内部数据层，不扩公共面（`00:137`）。AX02 / AX07 / AX21 / AX22 依赖真实网络 IO / 境外限制，AX03 / AX19 / AX20 依赖 NBT 或投影解析库，AX08 依赖 zip 解析库，AX04 的 EQ-13 与 Q-047-01 未拍板，AX15 与 `banner_design.rs` 撤销栈同构（075 E276），逐项不动并留痕。

## 079 补记：AX19 状态与「依赖 NBT 解析库」判定覆盖

| 编号 | 064 行 | 079 覆盖 |
| --- | --- | --- |
| AX19 | `Planned` / 排队（12-14 / 12-50 种子权限） | **`DataLayer`**：`src/core/seed_access.rs` 已落地种子记录集合 / 访客开关与密码标志 / 权限档位与审计动作双枚举 / 3×2 可见性矩阵 / 有界审计表 / 功能锁定与命令黑名单两集合 / 7+4+4+3+4 键白名单 / 原子写；NBT 从存档读种子、地形探索、全屏地图、密码校验、权限提示 UI 未启动 |

状态分层更新为 `Planned 9` / `DataLayer 14`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10、AX14、AX09、AX16、AX18、AX19）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到十四项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 14` / `Planned 9`。064–078 历史表格行不重写，本补记覆盖结论。

**A201 覆盖 076–078 补记的判定**：`:147` / `:161` / `:175` 写「AX03 / AX19 / AX20 依赖 NBT 或投影解析库……逐项不动并留痕」。该判定针对 `31-axolotl-launcher-features.md:57` 转述的「Java 版种子地图：找村庄 / 史莱姆区块 / 全屏查看 / 从实例存档导入种子」整体，是只核调研描述、未逐行回显 12 号原文时写下的**相对排序理由**（与 077 对 AX18 的「缺锚点」同形态）。本轮 A211 真读 `12-server-features-input.txt` 64 行与 `11-features-input.txt` 268 行全文后确认：NBT 依赖只落在 `12:14` 快速显示种子号中「从实例存档读种子」这一个执行层动作；`12:19` 功能锁定与命令黑名单、`12:24` 审计日志与种子/敏感信息权限提示、`12:50` 种子查看权限提示/访客隐藏、`11:262` 访客模式，四条都是纯元数据语义，不碰 NBT。按 073 AX13、075 AX14、077 AX16、078 AX18 四次「相对排序理由 + 收窄不碰 UI 渲染」先例，本轮照此执行，历史行不重写。转述的地形探索算法与全屏地图 UI 不取，登记 Q-079-01；`12:50` 两并列处置都落枚举、不擅自定优先级，登记 Q-079-02。

`api::v1` 7 符号不变：AX19 是内部数据层，不扩公共面（`00:137`）。AX02 / AX07 / AX21 / AX22 依赖真实网络 IO / 境外限制，AX03 / AX20 依赖 NBT 或投影解析库，AX08 依赖 `.mrpack` / `.zip` 解析库且与 `instance_drop.rs` 同构，AX04 的 EQ-13 与 Q-047-01 未拍板，AX15 与 `banner_design.rs` 撤销栈同构（075 E276），逐项不动并留痕。

## 080 补记：AX21 状态与「依赖真实网络 IO」判定覆盖

| 编号 | 064 行 | 080 覆盖 |
| --- | --- | --- |
| AX21 | `Planned` / 排队（真实网络 IO 未启动） | **`DataLayer`**：`src/core/lan_channel.rs` 已落地四枚举显式 code / 单实例通道状态 / 7+3+4+2+2 键白名单 / `TRANSITIONS` 6 对 / `STAGE_FIELDS` 4 段 / 八个派生纯查询 / 矛盾态三处拒收 / 原子写；真实连接建立、文件传输执行、二维码生成、房间密码校验、协议 UI 未启动 |

状态分层更新为 `Planned 8` / `DataLayer 15`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10、AX14、AX09、AX16、AX18、AX19、AX21）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到十五项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 15` / `Planned 8`。064–079 历史表格行不重写，本补记覆盖结论。

**A201 覆盖 079 补记的判定**：079 补记写「AX02 / AX07 / AX21 / AX22 依赖真实网络 IO / 境外限制……逐项不动并留痕」。该判定针对 `31-axolotl-launcher-features.md:64` 转述的「红石联机（第二家联机服务）、房间号 + 密码创建 / 加入、版本一致时与 FCL 手机端局域网互通」整体，是只核调研描述、未逐行回显 00 号原文时写下的**相对排序理由**（与 077 对 AX18 的「缺锚点」、079 对 AX19 的「依赖 NBT 解析库」同形态）。本轮 A211 真读 `00-requirements.txt` 261 行、`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行全文后确认：`00:20` 明写「手机端还没有支持这个功能，所以说你需要设计协议」，协议定义层本身是原文直接要求、不碰网络 IO；真实网络 IO 只落在「建立连接并传送文件」执行层；054 境外限制只在真实区域判定执行层触发，本轮不判定任何信号、不拉任何端点。按 073 AX13、075 AX14、077 AX16、078 AX18、079 AX19 五次「相对排序理由 + 收窄不碰 UI 渲染」先例，本轮照此执行，历史行不重写。转述的第二家联机服务与 FCL 手机端互通不取，登记 Q-080-02；连接码 / 二维码两条配对路径都落枚举、执行都不落，登记 Q-080-01。

`api::v1` 7 符号不变：AX21 是内部数据层，不扩公共面（`00:137`）。AX02 / AX07 / AX22 依赖真实网络 IO / 境外限制 / 第三方端点且 00 号原文无对应已决断协议锚点，AX03 / AX20 依赖 NBT 或投影解析库，AX08 依赖 `.mrpack` / `.zip` 解析库且与 `instance_drop.rs` 同构（079 补记明写），AX04 的 EQ-13 与 Q-047-01 未拍板，AX15 与 `banner_design.rs` 撤销栈同构（075 E276），逐项不动并留痕。

## 081 补记：AX02 状态与「依赖真实网络 IO」判定覆盖

| 编号 | 064 行 | 081 覆盖 |
| --- | --- | --- |
| AX02 | `Planned` / 排队（真实网络 IO 未启动） | **`DataLayer`**：`src/core/notice_center.rs` 已落地四枚举显式 code / 公告状态索引零内容持有 / 2+7+4+2+3+3 键白名单 / `BUILTIN_ID=declaration` 内置条目不可删 / 八个派生纯查询 / 矛盾态五处调用 / 原子写；真实新闻拉取、版本比对、附件图片解码、公告弹窗渲染未启动 |

状态分层更新为 `Planned 7` / `DataLayer 16`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10、AX14、AX09、AX16、AX18、AX19、AX21、AX02）/ `GateOnly 1`（AX23）。`ax_guard.py` 显式断言扩到十六项，动态求和不变（A240 / A262）；`src/core/ax.rs` 测试断言同步为 `DataLayer 16` / `Planned 7`。064–080 历史表格行不重写，本补记覆盖结论。

**A201 覆盖 080 补记的判定**：080 补记写「AX02 / AX07 / AX22 依赖真实网络 IO / 境外限制 / 第三方端点且 00 号原文无对应已决断协议锚点……逐项不动并留痕」。该判定针对 `31-axolotl-launcher-features.md:25` 转述的「游戏新闻 / 版本更新资讯折叠面板，可直接点开看更新内容」整体，是只核调研描述、未逐行回显 11 号原文与 017 决策时写下的**相对排序理由**（与 077 对 AX18 的「缺锚点」、079 对 AX19 的「依赖 NBT 解析库」、080 对 AX21 的「依赖真实网络 IO」同形态）。本轮 A211 真读 `00-requirements.txt` 261 行、`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行全文与 `017-visual-preview.md` 后确认：`11:12` 声明页「必须内置」、`11:219` 第三方更新指示公告「这个页面可以被取消」、`11:231` 上线提醒、`11:10` 每个弹窗有关闭逻辑、`11:22` 圆圈 i 详情、`11:16` 每页扩展、017 S03/S04/S06 公告中心界面语义，一组 9 条都是纯元数据，公告状态索引不碰网络 IO；真实网络 IO 只落在 `11:12` 从仓库拉版本平台信息、`11:219` 下载更新 url 两个内容获取执行层；054 境外限制只在真实区域判定执行层触发，本轮不判定任何信号、不拉任何端点。按 073 AX13、075 AX14、077 AX16、078 AX18、079 AX19、080 AX21 六次「相对排序理由 + 收窄不碰 UI 渲染」先例，本轮照此执行，历史行不重写。转述的游戏新闻流与版本更新资讯折叠面板不取，登记 Q-081-01；017 S06 两动作与 S04 三动作不擅自合并，登记 Q-081-02。

A217 边界：`src/core/popup.rs:44` / `:49` 已有 `declaration` / `notice` 弹窗占位，`src/core/feature_gate.rs:110` 已有 051 声明页三动作的运行时派生 `Notice`（不持久化、不分类、无已读态）；本轮只接可持久化的公告状态索引数据层，不把弹窗已登记写成功能已实现，不重复实现 051 三动作，`feature_gate.rs` / `popup.rs` / `consent.rs` 零 diff。

`api::v1` 7 符号不变：AX02 是内部数据层，不扩公共面（`00:137`）。AX07 / AX22 依赖真实网络 IO / 境外限制 / 第三方端点且 11 号原文无对应已决断公告锚点，AX03 / AX20 依赖 NBT 或投影解析库，AX08 依赖 `.mrpack` / `.zip` 解析库且与 `instance_drop.rs` 同构（080 补记明写），AX04 的 EQ-13 与 Q-047-01 未拍板，AX15 与 `banner_design.rs` 撤销栈同构（075 E276），逐项不动并留痕。

## 082 补记（083 收口轮落地）

`src/core/ax.rs:20` AX03 `world_editor` `Planned` → `DataLayer`，`conflict` 保持空；`Planned 6` / `DataLayer 17` / `GateOnly 1`。`src/core/world_editor.rs` 落存档编辑会话 + 开源组件许可证状态索引数据层：五枚举十五变体显式 code、七张白名单表、`VERIFIED_LICENSE = "MIT"`、27 类坏输入、`entry_consistent()` 五条规则八处调用、八个派生纯查询、单条突变、原子写、统一信封十值载荷、零内容持有。`api::v1` 7 符号不变，既有 16 个数据层模块零 diff。

081 补记把 AX03 归到「依赖 NBT 解析库」是只核 `31-axolotl-launcher-features.md:26` 转述、未逐行回显 11 / 12 号原文时写下的相对排序说明；`11:213` 第 6 条「通过vianbt向用户提供nbt能力」是已决断且直接点名开源库的锚点，`12:14` / `12:55` 给出字段语义，用户 082 当轮重申报「所有东西都要用开源的，在保证许可证的情况下」。按 073 / 075 / 077 / 078 / 079 / 080 / 081 七次收窄先例，只取项目原文已决断语义，收窄为不引第三方库、不碰真实 NBT 读取写回、不碰 UI 渲染、不写死 vianbt 字段 schema。064–081 历史行不重写（A181 / A201）。Q-082-01（`vianbt` 对应与引入形态）/ Q-082-02（转述五字段与提示）/ Q-082-03（`11:4` 其余四字段）待拍板。剩余 6 项 `Planned`：AX04 / AX07 / AX08 / AX15 / AX20 / AX22，下一声「干」按功能池落下一项。

## 084 补记（083 交付闭环轮）

6 项 `Planned` 保持不变：AX04 `mod_rollback` / AX07 `doh_support` / AX08 `instance_import` / AX15 `studio_image_editor` / AX20 `projection_workshop` / AX22 `shimu_account`；`Planned 6` / `DataLayer 17` / `GateOnly 1`，`api::v1` 7 符号不变，084 `src/` 零改动。A211 真读 `11-features-input.txt` / `12-server-features-input.txt` 全文后找到 AX04 的四条已决断锚点：`11:244`（同版本警告、高版本由用户选择版本后替换、顺序页码弹窗、每个单独选择）、`12:8`（高版本自动禁用低版本 jar，单个实例页面）、`12:33`（配置快照与回滚）、`12:39`（服务端/加载器版本回滚）。按 A267 核 `src/core/ax.rs:21` 真实 name `mod_rollback`、conflict 为空。085 按功能池落 AX04；064–083 历史行不重写（A181 / A201）。

## 085 / 086 补记（AX04 落地与交付闭环）

AX04 `mod_rollback` 由 `Planned` 改 `DataLayer`（085 落地），conflict 保持空、`ui: true`；`Planned 5` / `DataLayer 18` / `GateOnly 1`，`api::v1` 7 符号不变，086 `src/` 零改动。A211 真读全文：085 落地的四锚点为 `11:244` / `12:8` / `12:33` / `12:39`；086 真读全文找出 AX08 `instance_import` 的七锚点 `11:15` / `11:21` / `11:222` / `12:35` / `12:36` / `12:40` / `12:41`，按 A267 核 `src/core/ax.rs` 真实 slug 与 conflict，登记为 087 输入、不代拍、不擅自定 5 项 `Planned` 之间的优先级。剩 5 项：`AX07 doh_support`（conflict `network_io_not_started`）/ `AX08 instance_import` / `AX15 studio_image_editor` / `AX20 projection_workshop` / `AX22 shimu_account`。064–084 历史行不重写（A181 / A201）。

## 087 补记

AX04 `mod_rollback` 保持 `DataLayer`（085 落地），conflict 空、`ui: true`；`Planned 5` / `DataLayer 18` / `GateOnly 1`，`api::v1` 7 符号不变，087 `src/` 零改动。A211 真读全文复核 AX08 `instance_import` 七锚点 `11:15` / `11:21` / `11:222` / `12:35` / `12:36` / `12:40` / `12:41`，按 A267 核 `src/core/ax.rs:24–39` 真实 slug 与 conflict，顺延为 088 输入、不代拍、不擅自定 5 项 `Planned` 之间的优先级。剩 5 项：`AX07 doh_support`（conflict `network_io_not_started`）/ `AX08 instance_import` / `AX15 studio_image_editor` / `AX20 projection_workshop` / `AX22 shimu_account`。064–086 历史行不重写（A181 / A201）。

## 088 补记

AX08 `instance_import` 由 `Planned` 改 `DataLayer`（上一轮落地），conflict 空、`ui: true`；`Planned 4` / `DataLayer 19` / `GateOnly 1`，`api::v1` 7 符号不变，088 `src/` 零改动。A211 真读全文复核 AX08 七锚点 `11:15` / `11:21` / `11:222` / `12:35` / `12:36` / `12:40` / `12:41`；按 A217 核 `src/core/` 既有 `instance.rs` / `instance_drop.rs` 语义不同、不复用。剩 4 项 `Planned`：`AX07 doh_support`（conflict `network_io_not_started`）/ `AX15 studio_image_editor` / `AX20 projection_workshop` / `AX22 shimu_account`。064–087 历史行不重写（A181 / A201）。

## 089 补记

AX08 `instance_import` 保持 `DataLayer`（088 落地），conflict 空、`ui: true`；`Planned 4` / `DataLayer 19` / `GateOnly 1`，`api::v1` 7 符号不变，089 `src/` 零改动。A211 真读全文复核 AX08 七锚点 `11:15` / `11:21` / `11:222` / `12:35` / `12:36` / `12:40` / `12:41`，按 A267 核 `src/core/ax.rs:24–39` 真实 slug 与 conflict，顺延为 090 输入、不代拍、不擅自定 4 项 `Planned` 之间的优先级。剩 4 项：`AX07 doh_support`（conflict `network_io_not_started`）/ `AX15 studio_image_editor` / `AX20 projection_workshop` / `AX22 shimu_account`。064–088 历史行不重写（A181 / A201）。

## 090 补记

AX20 `projection_workshop` 由 `Planned` 改 `DataLayer`（090 落地），conflict 空、`ui: true`；`Planned 3` / `DataLayer 20` / `GateOnly 1`，`api::v1` 7 符号不变。按 A230 逐条核 4 项冲突：AX07 `doh_support`（conflict `network_io_not_started`，技术受阻非需求冲突，真读全文无已决断 DoH 锚点）/ AX15 `studio_image_editor`（与 `banner_design.rs` 撤销栈同构，075 E276）/ AX22 `shimu_account`（浏览器授权依赖真实网络 IO + 第三方端点 + 境外限制 + `11:18` API 不共有）三项排除留痕、状态保持 `Planned`、AX07 conflict 不清，登记 Q-090-01 / Q-090-02；AX20 按 `11:250` 原文已决断锚点收窄落地，历史行不重写（A181 / A201）。A211 真读全文复核六锚点 `11:250` / `11:244` / `11:147` / `11:150` / `11:23` / `11:24` / `11:10` / `12:35` / `12:36`；按 A267 核 `src/core/ax.rs:24–39` 真实 slug，按 A217 核 `src/core/` 无 `projection*` 占位。091 前的剩 3 项：`AX07 doh_support` / `AX15 studio_image_editor` / `AX22 shimu_account`。064–089 历史行不重写（A181 / A201）。

## 091 补记

AX15 `studio_image_editor` 由 `Planned` 改 `DataLayer`（091 落地），conflict 空、`ui: true`；`Planned 2` / `DataLayer 21` / `GateOnly 1`，`api::v1` 7 符号不变。按 A230 逐条核 3 项冲突：AX07 `doh_support`（conflict `network_io_not_started`，技术受阻非需求冲突，真读全文无已决断 DoH 锚点）/ AX22 `shimu_account`（浏览器授权依赖真实网络 IO + 第三方端点 + 境外限制 + `11:18` API 不共有）两项排除留痕、状态保持 `Planned`、AX07 conflict 不清，登记 Q-091-01 / Q-091-02 / Q-091-03；AX15 按 `12:63` 原文已决断锚点收窄落地，历史行不重写（A181 / A201）。A211 真读全文复核八锚点 `12:63` / `12:59` / `11:243` / `11:147` / `11:150` / `11:23` / `11:24` / `11:10` / `11:26` / `11:16` / `12:35` / `12:36`；按 A267 核 `src/core/ax.rs:20–43` 真实 slug，按 A217 核 `src/core/` 无 `studio*` / `image*` / `logo*` / `pixel*` 占位。092 前的剩 2 项：`AX07 doh_support` / `AX22 shimu_account`，两项均卡网络前置 / Q / EQ，按 090 唯一下一步「若回任一 Q / EQ 则改走拍板闭环」转拍板闭环。064–090 历史行不重写（A181 / A201）。

## 092 补记

092 为拍板闭环轮，`src/core/ax.rs` 零改动：AX07 `doh_support` / `Planned` / `network_io_not_started`、AX22 `shimu_account` / `Planned` / 空 conflict、AX23 `client_ai_gate` / `GateOnly` 原样；`Planned 2` / `DataLayer 21` / `GateOnly 1`，`api::v1` 7 符号不变。按 A230 逐条核 2 项冲突并写进 `pending-question-environments.md` 092 段：AX07 技术受阻非需求冲突（EQ-03 Win7 TLS 前置 + 真实网络 IO 未启动，00 / 11 / 12 号全文无 DoH 锚点）、AX22 浏览器授权依赖真实网络 IO + 第三方端点 + `11:7` / 054 境外限制 + `11:18` API 不共有，两项排除留痕、状态保持 `Planned`、AX07 conflict 不清，不擅自定优先级（A208）。Q-091-01 / Q-091-02 / Q-091-03 与 Q-C 口径修正 E375 见 092 段。064–091 历史行不重写（A181 / A201）。

## 093 补记

093 为位置清单交付轮，`src/core/ax.rs` 零改动：AX07 `doh_support` / `Planned` / `network_io_not_started`、AX22 `shimu_account` / `Planned` / 空 conflict、AX23 `client_ai_gate` / `GateOnly` 原样；`Planned 2` / `DataLayer 21` / `GateOnly 1`，`api::v1` 7 符号不变。用户当轮明确指令「提交所有功能写的位置的 txt」按 `00:248` 覆盖 092 唯一下一步「等用户拍板 A 组」；A 组 EQ-03 + AX07、EQ-01 + Q-091-01 + AX22 与其余 11 条 EQ / 4 项 Q-C / 31 条历史 Q 保持「未证实（待拍板）」，不擅自开工、不擅自定 2 项优先级（A208）。位置清单第六节 5 条候选调整全部待拍板未执行。064–092 历史行不重写（A181 / A201）。

## 094 补记

094 为功能归类交付轮，`src/core/ax.rs` 零改动：AX07 `doh_support` / `Planned` / `network_io_not_started`、AX22 `shimu_account` / `Planned` / 空 conflict、AX23 `client_ai_gate` / `GateOnly` 原样；`Planned 2` / `DataLayer 21` / `GateOnly 1`，`api::v1` 7 符号不变。用户当轮明确指令「功能散落、重新归类、详细行为链路」按 `00:248` 覆盖 093 唯一下一步「点第六节 5 条偏差」；A 组最小拍板面、其余 11 条 EQ、Q-C01 / Q-C02 / Q-C08 / Q-037-01、Q-091-01 / 02 / 03 与 D 组 31 条历史 Q 保持「待拍板 / 未证实」。093 的 5 条偏差、094 的 8 条候选规则与 10 条散落归位同为待拍板未执行。064–093 历史行不重写（A181 / A201）。

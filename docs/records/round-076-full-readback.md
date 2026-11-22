# 076 开工逐字复读记录

开工 `Sun Nov 22 10:44:07 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节本轮完整读，分两段回显（1–260 / 261–520），末条仍为 A271，075 无新增防错项。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮**逐行全文回显**（A211 真读全文找已决断条目）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/76-round-076-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/75-round-075-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/74-round-074-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/73-round-073-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a` |
| `docs/records/ax-feature-pool.md` | 11966 | 139 | `72550f456e75ba3508aa9de1df715a11dfe1ec6c6b37d814196a4aeed5e5b355` |
| `docs/records/b-class-status-recheck.md` | 7220 | 88 | `c2dcf769c53be62fc66997e84c86127e4d30fff7aa2fb75361a79476e49302bc` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/075-skin-draft.md` | 17888 | 130 | `13644e882fb02e62d4c15c6b7115d9ab1a82cc011aebe8efb7508fbc132b759c` |
| `docs/decisions/074-first-run.md` | 17164 | 128 | `d0ede6524617c7ffc956bace560a6f8d4b3dc395375c995bc9bd79a3eaf10267` |
| `src/core/ax.rs` | 4544 | 100 | `f64f82770f0d8be45dde549e2f8b5344662bd1d8afdf117a3c7e951b3fd7bbf1` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 17915 | 553 | `25e1674b05d422db18a839fbb40e09b0c743433c96b10138dc1cc48cd9fd51aa` |
| `src/core/mod.rs` | 659 | 37 | `f581a7d29e53275eb5e5ec8a778d197ca182b5ee214db029bb322abc68d19703` |
| `src/core/skin_draft.rs` | 22252 | 628 | `d0e715c6d4953c969ae6aa2b22508f99541d0df2c1ee57930204a7b981788bb3` |
| `src/core/first_run.rs` | 18993 | 563 | `5304b5f142f4b69c0695986be318f43f1aae4b948c20c2970428b4e6348acbb3` |
| `src/updater/policy.rs` | 5310 | 157 | `286b3ba818cb774ad615e7c7723640c830fd30b245f9b9cf9b82a0918d1d6a06` |
| `src/plugins/upgrade.rs` | 5792 | 165 | `06bfb0cdc95a6ddb7d004f12d9134535723d15ed42144c90362682fa63afd8e9` |
| `scripts/ax_guard.py` | 1955 | 49 | `458037d58320f44fc230df12b5f05b754493bcaeb4efd693686e35d6f8b5e2a5` |
| `scripts/api_guard.py` | 1535 | 45 | `bdff880d3d42c9dcc9d82ddf7cdcde8ae7464731716f1cc8e9586ad32971ebbb` |
| `scripts/delivery_guard.py` | 3438 | 100 | `2e940286c4f6aae4259dbd73b5d688c635150dbe85636adb2de582edeb685506` |
| `scripts/skin_draft_guard.py` | 5762 | 139 | `5530570ff2f72f86ae34bba13b748671f1c74bea51e91496d0ddb409210dcf06` |
| `.github/workflows/ci.yml` | 4202 | 121 | `efcaad91a1d12a295585c3370f6351462e479eec70d6c2939172fb9a55e8f190` |
| `docs/index.md` | 45726 | 594 | `07b737160c0f7c0e1b171d860826d9885d5d7d21b0c569c4b24594d62b237f8b` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `76-round-076-instructions.txt:1` | 逐字 `干`（3 字节，SHA-256 `9ee0280b…`，无换行） |
| `75-round-075-instructions.txt:1` / `74` / `73` | 逐字 `干`（各 3 字节，同哈希） |
| `72-round-072-instructions.txt:1` | 117 字节澄清句，已在 072 轮处理并撤回 071 归因（E251 / A266），本轮不重提 |
| `11-features-input.txt:244` | 第 36 条「重复模组同一版本的时候进行警告，如果用户选择继续就继续，如果说版本高于的话就会把原来的版本，由用户选择版本以后再进行，注意这个地方不要一次性把页面都堆在一起，按照顺序去排列，都在一个弹窗中，上面有那种页码，然后呢如果说出现了别的问题，用户还没有进行选择会增加，每一个都是单独的选择」——**已决断、不依赖 EQ**（A211 真读全文找）：逐条选择、顺序排列、页码、未决项增加、每条单独选择 |
| `11-features-input.txt:219` | 第 12 条「支持json用于服主设置对应的模组更新，需要写清楚模组地址,这个json下载更新url，是否检查更新，是否强制更新？是否指定我的世界版本？提示文本为xxx第三方更新指示公告，这个页面可以被取消」——**已决断**：更新策略用 JSON + 明确字段白名单 + 可取消 |
| `11-features-input.txt:205` | 「有些地方用户逻辑也需要对应功能的，你也需要有对应功能啊比如搜索」 |
| `12-server-features-input.txt:37` | 第 24 条第 37 子项「模组依赖与冲突预检（启动前）」 |
| `12-server-features-input.txt:8` | 第 8 条「模组更新功能，如果版本更高同一模组的jar将自动禁用低版本模组（这个功能需要在单个实例页面才能用）」 |
| `12-server-features-input.txt:24` | 第 24 条起 40 个子项（Java 多版本管理 / 端口冲突 / 配置快照与回滚 / 整合包导入导出 / 拖拽安装 / 依赖预检 …），编号 `24` 是条目编号不是单子项行号（A259） |
| `31-axolotl-launcher-features.md:37` | AX09 升级前查看模组兼容性，再选「直接升级」或「复制一份后升级」；来源 `axlmc.org` 首页 / **官方一手**；状态「部分」，口径 `semver 版本比较（034）、036 更新决策、手动同意升级（037）` |
| `31-axolotl-launcher-features.md:80` | 「AX01 / AX14 / AX15 / AX17 / AX20 都是重 UI 功能，渲染方案在 UI 框架口径落定前不能定」——069–075 已按「收窄为不碰 UI 渲染」处置七次，历史行不重写（A201） |
| `src/core/ax.rs:26` | `AxSpec { id: "AX09", name: "upgrade_compat", state: AxState::Planned, conflict: "", ui: true },`（A267 先读真实 name slug） |
| `src/updater/policy.rs:6,13,18,38` | 036 更新决策：`Decision` / `UpdatePolicy` / `decide(current, candidate, policy)` / `verify_then_decide`——单次无状态判定，签名校验优先 |
| `src/plugins/upgrade.rs:9,16,29` | 037 手动同意：`UpgradeDecision` / `UpgradeRequest` / `decide_upgrade(req)`——单次无状态判定 |
| `ax-feature-pool.md` 075 补记 | `Planned 13` / `DataLayer 10`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10、AX14）/ `GateOnly 1`（AX23） |
| `00-requirements.txt:26` | 严格进行调研，直到信息已经达到完全无法失误的情况下再操作 |
| `00-requirements.txt:33` | 每次交付带 HTML 一比一运行逻辑、自我批判、时间戳回显、四值判决、独立验证证据 |
| `00-requirements.txt:34` / `:260` | 每轮开工前完整读一遍本文件与防错清单 |
| `00-requirements.txt:44` | 别人有的功能要有 |
| `00-requirements.txt:54` | 不做过度抽象、不套设计模式、不偷偷加依赖 |
| `00-requirements.txt:110` | 必须处理空值、空集合、越界、超时、编码 |
| `00-requirements.txt:111` | 禁止顺手改无关文件 |
| `00-requirements.txt:114` | 跨进程消息走统一信封 |
| `00-requirements.txt:133` | 需求逐字保存到仓库 |
| `00-requirements.txt:137` | 每次开动前确认文件接口最后一层 |
| `00-requirements.txt:156` | 连续两轮未达通过，停下来向用户报告卡点 |
| `00-requirements.txt:166` | 每个状态只声明实际达到的那一层 |
| `00-requirements.txt:175` | 同类功能尽量复用同一个模块 |
| `00-requirements.txt:230` | 每轮联网核实现有时间与上游版本状态（第 15 节，标注不阻塞当前轮） |
| `00-requirements.txt:245` | 有任何未解决的「已失败 / 未证实 / 受阻」，不发通过标记 |
| `00-requirements.txt:248` | 用户当轮明确指令 > 本文件规则 |
| `00-requirements.txt:249` | 安全与许可证合规 > 功能进度 |
| `00-requirements.txt:209-222` | 12 项输出结构 |
| `ai-errors.md:331` | A164 原始需求逐条分「已决断 / 未决断」核对 |
| `ai-errors.md:354` | A177 用户没拍板选项时按默认执行要显式登记 D 编号 |
| `ai-errors.md:405` | A203 授权成立也要逐值回显具体默认 |
| `ai-errors.md:415` | A208 只回「干」且列需 EQ 拍板的层时先复核台账 |
| `ai-errors.md:423` | A211 已决断、不依赖 EQ 的条目要真读全文找 |
| `ai-errors.md:449` | A217 只接数据层，不把「已登记」写成「已实现」 |
| `ai-errors.md:483` | A246 新增内部数据层不扩 `api::v1` |
| `ai-errors.md:486` | A248 不得把自造约束写成用户当轮指令 |
| `ai-errors.md:487` | A249 新 spec 落盘即触发本轮四件套 |
| `ai-errors.md:488` | A250 原文含 OR 两条路径只落一条，另一条登记待拍板 Q |
| `ai-errors.md:490` | A252 分段求和必须注明口径 |
| `ai-errors.md:493` | A254 网关 502 留 `.git/index.lock`，提交前先核 |
| `ai-errors.md:495` | A255 `Vec::new()` 在 push 前被读触发 E0282 |
| `ai-errors.md:496` | A256 `LOADED_MODULES` 真实结尾还有 `dispatcher.launcher` |
| `ai-errors.md:498` | A258 守卫禁用表不写凭据前缀连续串 |
| `ai-errors.md:501` | A259 二手调研的 NN-MM 是条目编号还是行号要分开核 |
| `ai-errors.md:507` | A263 注入夹具锚点必须唯一 |
| `ai-errors.md:509` | A264 夹具预期与既定上限对齐 |
| `ai-errors.md:510` | A265 演示 LOG 键数等于 NODES 步数 |
| `ai-errors.md:512` | A266 平台拼入用户位次的文本不得当用户当轮指令 |
| `ai-errors.md:513` | A267 改功能池状态前先读真实 name slug |
| `ai-errors.md:514` | A268 G2 四份原文 + G3 决策 `## 9` / `## 10` 锚点留原位 |
| `ai-errors.md:516` | A269 显式 code 枚举守卫要解析 impl 段字面量逐值比对 |
| `ai-errors.md:518` | A270 守卫解析常量表后显式 `EXPECTED` 集合逐值比对 |
| `ai-errors.md:520` | A271 新增测试标识符前先核全仓既有守卫的禁用字面量表 |

## A248 / A266 预检

76 号 spec 全文 3 字节 `干`，逐字副本已落盘；75 / 74 / 73 号 spec 同为 3 字节 `干`（同 SHA-256）；72 号 117 字节澄清句已在 072 轮处理。本轮不重提「工具禁用 / 未遵守 / 偏离」，不把任何平台文本当用户指令。用户当轮明确指令只有一个字：按功能池落下一项。

## A259 复核

`31-axolotl-launcher-features.md:37` 写「12-37 是启动前依赖冲突预检，不是版本升级决策」：`12-37` 是**第 24 条第 37 个子项的条目编号**，真实行号是 `12-server-features-input.txt:37`。`31-axolotl-launcher-features.md:27` 的 `11-36` 是**第 36 条**，真实行号 `11-features-input.txt:244`；`31-axolotl-launcher-features.md:27` 的 `12-24` 是**第 24 条**，对应 `12-server-features-input.txt:24-63` 整段，不是单个行号。`31-axolotl-launcher-features.md:38` 的 `00-12` 误写已在 074 复核。本轮一律用文件行号 `11:244` / `:219` / `:205`、`12:37` / `:8` / `:24`，不把 `11-36` / `12-37` 当行号锚点。31 号调研历史行不重写（A226 / A200 / A259）。

## A211 真读全文找已决断条目

本轮回显 11 号原文 268 行与 12 号原文 64 行全文，逐条核「已决断、不依赖 EQ」的条目。命中升级决策相关五条：`11:244` 第 36 条的「逐条选择 / 顺序排列 / 页码 / 未决项增加 / 每一个都是单独的选择」；`11:219` 第 12 条的「模组更新 JSON + 明确字段 + 页面可取消」；`11:205` 用户逻辑对应功能；`12:37` 模组依赖与冲突预检（启动前）；`12:8` 版本更高自动禁用低版本模组。五条都是项目原文已决断，不依赖 EQ-01 ~ EQ-13、4 条 Q-C，也不依赖真实网络 IO。本轮据此只落**逐条升级决策的持久化数据层**，不碰真实文件复制、版本比较执行与 UI 渲染。

AX09 的口径 `semver 版本比较（034）、036 更新决策、手动同意升级（037）` 三项都是**已实现模块**（`src/updater/policy.rs` 的 `verify_then_decide` 与 `src/plugins/upgrade.rs` 的 `decide_upgrade`），不是待拍板 EQ；EQ-13 只挂在 AX04（`ax-feature-pool.md:10`），本轮不碰 AX04。

## A250 复核：OR 路径

`11:242` 第 34 条的两天 / 拓展包 OR 两路径已在 074 登记 Q-074-02，本轮不涉及。AX09 调研描述的「直接升级」/「复制一份后升级」是两个执行态：本轮**两个都落为显式枚举值**（`direct` / `clone`），不落任何真实执行，不属于「只落其中一条」，不触发 A250 的 Q 要求；但执行层（真实目录复制、由谁执行、失败回退）未启动，另登记 Q-076-01。兼容性预检来源与 `conflict` 时是否仍允许强制升级登记 Q-076-02，不代拍板。

## A271 全仓守卫禁用字面量表预检（开工时实跑）

按 A271，新增测试标识符前先核全仓 `scripts/*_guard.py` 的禁用字面量表，不只核本轮新守卫。实跑 `grep -nE 'FORBIDDEN|for banned|EXPECTED = |banned in' scripts/*_guard.py`：

| 守卫 | 扫全仓还是单文件 | 需避开的字面量 |
| --- | --- | --- |
| `api_guard.py:33` | **全仓 rs，不分测试段** | `Popup::new(` / `PopupKind::` / `catalog()` |
| `ai_gate_guard.py:7` | 单文件 `client_ai.rs` | `TcpListener` / `bind(` / `127.0.0.1` / `/mcp` / `Token` / `token` |
| `download_history_guard.py:19` | 自身全文 | `http://` / `https://` / `SystemTime` / `UNIX_EPOCH` |
| `first_run_guard.py:22` / `banner_design_guard.py:22` / `widget_layout_guard.py:22` / `appearance_guard.py:22` / `skin_draft_guard.py:22` | 各自 `prod` 段 | `STEP_CATALOG` / `minecraft:` / `give ` / `\u00a7` / `PRESET_COLORS` / `calendar` / `SKIN_TABLE` / `texture` / `uuid` / `png` 等 |
| `launch_progress_guard.py:37` | 自身 `prod` 段 | `SystemTime` / `UNIX_EPOCH` / `std::fs` / `TcpListener` / `http://` |

结论：新模块 `upgrade_plan.rs` 的常量名、函数名、测试名一律不出现 `catalog()` / `Popup::new(` / `PopupKind::` / `token` / `http` 连续串 / `minecraft:` / `give ` / `uuid` / `png`；末例测试命名 `serialize_carries_no_choice_table()`（避开 `catalog()`，074 E275 / 075 同形态）。版本号与模组 id 全当不透明字符串，字段名用 `current` / `candidate` 而非 `url`，不写任何 `http` 连续串。守卫脚本自身不写凭据前缀连续串（A258），部署前 `python -m py_compile`（A251）。

## A208 复核（本轮开工前）

用户 076 只发「干」，未点 AX 编号、未回 Q-067-01 ~ 03 / Q-070-01 / Q-071-01 / Q-071-02 / Q-072-01 / Q-072-02 / Q-073-01 / Q-073-02 / Q-074-01 / Q-074-02 / Q-075-01 / Q-075-02 / EQ。按 A202 核 `075-skin-draft.md` 与 `ax-feature-pool.md` 075 补记：075 结尾给出两个分支，主分支「下一声『干』按功能池落下一项（剩 13 项 `Planned`）」，替代分支「回 Q / EQ 拍板」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、UI 渲染闸门、密钥与新增第三方。

## `00:9.1` 连续未达通过的处置（D-076-1）

069 / 070 / 071 / 072 / 073 / 074 / 075 连续七轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 076 当轮明确指令是「干」，按 `00:248` 覆盖。**不中断推进，但卡点在本轮回复、决策、四值里逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；12 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化 |
| 069–075 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层 |
| `11:244` 第 36 条逐条选择 / 页码 / 每条单独选择 | **已决断、不依赖 EQ**（A211 真读全文找） |
| `11:219` 第 12 条模组更新 JSON 字段白名单 + 可取消 | **已决断、不依赖 EQ**（A211 真读全文找） |
| `11:205` 用户逻辑对应功能 | 已决断 |
| `12:37` 启动前依赖冲突预检 / `12:8` 高版本禁用低版本 | 已决断 |
| `00:171` / `00:172` 密钥不写死、默认镜像 | 已决断，069 已落地 |
| AX09 两个执行态的真实目录复制、由谁执行、失败回退 | **未决断**：登记 Q-076-01 |
| 兼容性预检来源、`conflict` 时是否仍允许强制升级 | **未决断**：登记 Q-076-02 |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / A267 / D-076-2）

真读 13 项 `Planned` 全文（AX02、AX03、AX04、AX07、AX08、AX09、AX15、AX16、AX18、AX19、AX20、AX21、AX22）与 065 / 066 / 069–075 的排除清单、`src/core/ax.rs` 24 条唯一 spec、`src/updater/policy.rs` / `src/plugins/upgrade.rs` / `src/core/skin_draft.rs` / `first_run.rs` 真实形态后选 **AX09 upgrade_compat** 的**数据层**，登记为**我的默认 D-076-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX02 / AX07 / AX21 / AX22 | 真实网络 IO / 境外限制 / 第三方端点 / Win7 TLS 前置，不动 |
| AX03 / AX19 / AX20 | NBT / `.litematic` / `.schem` 解析库，零新增第三方约束下不动 |
| AX04 | EQ-13（`ax-feature-pool.md:10`）与 Q-047-01 未拍板，不动 |
| AX08 | zip 解析库，066 已排除 |
| AX16 / AX18 | 063 登记的 6 项低可信度转述；AI 提供商配置页已被 062 排除（`conflict: ai_provider_ui_excluded`） |
| AX15 | Studio 图片编辑的撤销重做栈与 `banner_design.rs:241-263` 同构，075 已登记 E276 排除，历史行不重写 |
| **AX09 收窄后** | `11:244` / `11:219` / `12:37` / `12:8` 四条已决断、不依赖 EQ（A211）；来源 `axlmc.org` 首页**官方一手**，不在 063 低可信度转述内；口径 034 / 036 / 037 均为已实现模块而非待拍板 EQ；`31-axolotl-launcher-features.md:80` 未把 AX09 列入重 UI 阻塞项；收窄为不碰真实文件复制 / 版本比较执行 / UI 渲染 / 网络请求的**逐条升级决策持久化数据层**；语义为按 id 索引的候选项集合 + 三值兼容性 + 三选一决策 + 单条确认 + 派生页码，与 `first_run.rs` 的全局顺序游标、`skin_draft.rs` 的并列草稿双态、`banner_design.rs` 的分层撤销栈、`updater/policy.rs` 的单次无状态判定均不同构 |

不做的（登记 Q / 未启动）：真实目录复制与升级执行（Q-076-01）、兼容性预检来源与 conflict 强制升级口径（Q-076-02）、版本比较执行（由 034 既有模块持有，本层不重复实现）、升级决策 UI 渲染、弹窗分页视图、签名校验接入均未启动。

`src/core/ax.rs:26` 真实 name 是 `upgrade_compat`，实现模块名 `upgrade_plan.rs`；A267 先读后写，不凭文件名猜。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod upgrade_plan;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.upgrade_plan`，锚点用真实结尾 `"core.skin_draft",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX09 `Planned` → `DataLayer`；24 条唯一不变；断言 `DataLayer 11` / `Planned 12` |
| `scripts/ax_guard.py` | 显式断言扩到十一项（…AX14、AX09）；动态求和不变（A240 / A262） |
| `scripts/upgrade_plan_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 25 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/updater/policy.rs` / `src/plugins/upgrade.rs` | 零 diff，判定层由既有模块持有，本层只接注入结果 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `76-round-076-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 520 行完整读；11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 76 / 75 / 74 / 73 / 72 号 spec 逐字副本；不重提工具禁用归因 |
| A268 | G2 四份原文全部列入哈希表；决策 `## 9` / `## 10` 锚点一次排对 |
| A271 | 开工实跑全仓守卫禁用字面量表，测试标识符从首版避开 `catalog()` 等命中串 |
| A211 / A250 / A259 | 真读全文找五条已决断锚点；OR 两执行态都落枚举并登记 Q-076-01；`11-36` / `12-37` 改真实行号 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX09 数据层已实现 / 已验证；真实升级执行、UI 渲染、版本比较执行未启动 |
| `00:54` / `00:111` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / UX / 语言包 / PNG / 036 / 037 |
| `00:114` | 状态变更走统一 `Envelope` |
| `00:175` | 公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES`；版本比较与签名校验由 034 / 036 / 037 持有，本层不重复实现；登记 E284 不写成「已满足」 |
| `00:110` | 7 类根级 + 11 类条目坏输入、空集合 / 越界 / 饱和 / 控制字符 / 矛盾态 / 无 root 全处理 |
| `00:26` / A30 | 模组 id 与 `current` / `candidate` 版本串全当不透明字符串；不解析 semver、不内置镜像地址 / API 基址 / 端口；兼容性判定由调用方注入，不写死上游实值 |
| `00:230` | 属第 15 节调研待办「不阻塞当前轮」；本轮无外部事实依赖，未执行联网，如实登记 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构；LOG 键数 = NODES 步数（A265） |
| A154 / A269 / A270 | `Compat` / `UpgradeMode` 两个枚举显式 `code()` / `parse()`；守卫解析两个 `impl` 段字面量逐值比对；四张常量表用显式 `EXPECTED` 集合逐值比对 |
| A258 / A262 / A263 / A264 / A265 | 新守卫不写凭据连续串、不写死状态计数、注入锚点唯一、夹具与上限对齐、演示键数对齐 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-076-2 ~ D-076-16，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-076-2 | 选 AX09 落数据层 | 我的默认，不写成用户已决断（A177） |
| D-076-3 | 收窄范围 | 不碰真实文件复制 / 版本比较执行 / UI 渲染 / 网络请求 / 签名校验接入，只落逐条升级决策持久化数据层 |
| D-076-4 | 兼容性枚举 | `Compat` = `compatible` / `conflict` / `unknown`，显式 `code()` + `parse()`（A154 / A269）；值由调用方注入 |
| D-076-5 | 决策枚举 | `UpgradeMode` = `defer` / `direct` / `clone`，显式 `code()` + `parse()`；新建缺省 `defer` |
| D-076-6 | 标识与版本串 | `id` / `current` / `candidate` 全当不透明字符串；只校验非空、长度 ≤ `robust::MAX_ID_BYTES`、无控制字符；不解析 semver、不写 `http` 连续串 |
| D-076-7 | 候选项集合 | `Vec<UpgradeChoice>` 显式类型（A255），上限 24（项目自定义容量上限，不宣称上游上限）；`UpgradeChoice { id, current, candidate, compat, mode, confirmed }` 6 键严格白名单；id 去重 |
| D-076-8 | 页码 | `page_size: usize` 取 `1..=10`、缺省 5；`page_count()` / `page_items(page)` 由集合与页大小**派生**，不存全局游标（`11:244`「都在一个弹窗中，上面有那种页码」） |
| D-076-9 | 单条确认 | `confirm(id)` 只作用单条且 `mode == defer` 时返回 `false`；无批量确认函数；`revoke(id)` 是回退入口；`set_mode` 改为 `defer` 时清 `confirmed`（`11:244`「每一个都是单独的选择」+ 037 手动同意） |
| D-076-10 | 冲突回退 | `set_compat` 改成 `conflict` 时把该条 `mode` 重置为 `defer` 并清 `confirmed`；`parse()` 遇 `conflict` + `confirmed=true` 或 `defer` + `confirmed=true` 矛盾态跳过该条（A95 / 036 默认只升） |
| D-076-11 | 顶层白名单 | `KNOWN_KEYS` 3 键唯一，未知键整份拒并给 DEGRADE 行（A189） |
| D-076-12 | 持久化 | `upgrade-plan.json` schema 1，只写 3 键；原子写；`reset` 不删文件并复用 065 四文件保护 |
| D-076-13 | 状态变更事件 | `Kind=Event` / `target=upgrade.plan` / 载荷只带 choices / pending / ready / pages 四个值；id 与版本串不进事件（`00:114`） |
| D-076-14 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |
| D-076-15 | 启用与执行边界 | 真实目录复制、升级执行、版本比较执行、签名校验接入、UI 渲染均未启动；Q-076-01 / Q-076-02 待拍板 |
| D-076-16 | 状态分层与联网核实 | AX09 数据层已实现 / 已验证，其余未启动（`00:166`）；`00:230` 属第 15 节调研待办「不阻塞当前轮」，本轮无外部事实依赖，未执行联网，如实登记 |

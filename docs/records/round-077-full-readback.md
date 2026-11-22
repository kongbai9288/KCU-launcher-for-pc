# 077 开工逐字复读记录

开工 `Sun Nov 22 11:26:50 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节本轮完整读，分两段回显（1–260 / 261–520），末条仍为 A271，076 无新增防错项（E293 本轮无新防错项）。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮**逐行全文回显**（A211 真读全文找已决断条目）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/77-round-077-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/76-round-076-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/75-round-075-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/74-round-074-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/73-round-073-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a` |
| `docs/records/ax-feature-pool.md` | 13526 | 149 | `9dcd07c7ecc16e82104ea42eea1bac32286a9a21fff7053a30159790689e13eb` |
| `docs/records/b-class-status-recheck.md` | 7220 | 88 | `c2dcf769c53be62fc66997e84c86127e4d30fff7aa2fb75361a79476e49302bc` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/063-axolotl-survey.md` | 7944 | 92 | `f6d6e04ea23530cb6409fe2acd434b61e849c84356a8bdb00e3cf295bed5f01e` |
| `docs/decisions/073-appearance.md` | 14072 | 117 | `b2170b621534c5d13bb840f616966c2401b6cbca03b745a549115ccaded21a13` |
| `docs/decisions/075-skin-draft.md` | 17888 | 130 | `13644e882fb02e62d4c15c6b7115d9ab1a82cc011aebe8efb7508fbc132b759c` |
| `docs/decisions/076-upgrade-plan.md` | 21028 | 136 | `b5584d4fa7fcecf275205896a9e0831e79c392bb879dbba8ce36abe4f527ed21` |
| `src/core/ax.rs` | 4554 | 100 | `c9d113076ae4fed17b608bc64aed7eeb0c2269da798f4b5d163ad21b5e9f1fc1` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 17940 | 554 | `051f9700cdb4a5f7f896fa9f77352b2e4bafb7294cf80f1574599b3d53567602` |
| `src/core/mod.rs` | 681 | 38 | `6717c864819ffd63ba93c1a9dd2db87dadc248b37138e87def29a96ed6a95f7c` |
| `src/core/upgrade_plan.rs` | 25509 | 687 | `5547a85d9fef584d7374a95b29a857716ead3be88624fb7cb1b6d611367ad0c7` |
| `scripts/ax_guard.py` | 1963 | 49 | `d9a0b6761d1e6b2c0bd6daea4700025fc2ae58aa58aeef10cd8f6d57c817f107` |
| `scripts/api_guard.py` | 1535 | 45 | `bdff880d3d42c9dcc9d82ddf7cdcde8ae7464731716f1cc8e9586ad32971ebbb` |
| `scripts/delivery_guard.py` | 3438 | 100 | `2e940286c4f6aae4259dbd73b5d688c635150dbe85636adb2de582edeb685506` |
| `scripts/first_run_guard.py` | 5353 | 134 | `de4f99f28fa4a38454eabf286e54f40e94de97b88acdefa1b42a59c4c62f1c38` |
| `scripts/ai_gate_guard.py` | 1854 | 50 | `d5f0d12cfbacd24e7af24b6956ec530e9a5ed3dd5cb9ed73ef7184fe3bc81fec` |
| `scripts/i18n_guard.py` | 2642 | 72 | `d991dd5275d992e3d97f8c3a2d8d5c61fe4205fc24e0872928e532d5944dacfa` |
| `scripts/upgrade_plan_guard.py` | 7132 | 161 | `901559f45766058ee324539b37fd45a65b4e61d8595184920d0af59a124ee4ba` |
| `.github/workflows/ci.yml` | 4286 | 123 | `d3c9a88ad04c60428c415bd38d87f1483706ce520c299addf5beb32d1b75e117` |
| `docs/index.md` | 46231 | 601 | `dee919bb4ceb3eec304df3bda09e870cea72f395b221a39d23ed31225a90addf` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `77-round-077-instructions.txt:1` | 逐字 `干`（3 字节，SHA-256 `9ee0280b…`，无换行） |
| `76` / `75` / `74` / `73` 号 spec | 逐字 `干`（各 3 字节，同 SHA-256） |
| `72-round-072-instructions.txt:1` | 117 字节澄清句，已在 072 轮处理并撤回 071 归因（E251 / A266），本轮不重提 |
| `11-features-input.txt:94-100` | 「搜索文件 / 搜索文件夹 / 按名称搜索 / 按类型搜索 / 按大小搜索 / 按修改时间搜索 / 按路径搜索」——**已决断、不依赖 EQ**（A211 真读全文找） |
| `11-features-input.txt:101-102` | 「搜索当前文件夹 / 搜索子文件夹」——OR 两条范围路径（A250） |
| `11-features-input.txt:109-117` | 「搜索排除 / 搜索过滤 / 高级搜索 / 搜索结果排序 / 搜索结果筛选 / 搜索结果批量操作 / 保存搜索条件 / 搜索历史 / 搜索建议」——九条已决断 |
| `11-features-input.txt:118-123` | 「排序 / 按名称排序 / 按类型排序 / 按大小排序 / 按修改时间排序 / 排序方向切换」——六条已决断 |
| `11-features-input.txt:205` | 「如果说有些地方用户逻辑也需要对应功能的，你也需要有对应功能啊比如搜索」 |
| `11-features-input.txt:206` | 「有些功能你看着办，就是比如他的那些搜索框，他的那些排序按钮，如果有文件管理功能的，就要与正常的文件管理器一样，有那些功能」 |
| `11-features-input.txt:208` | 第 1 条「下载：支持按序下载功能，多线程下载，mod页每20个条目显示一次，可以聚合搜索」——模组页搜索也是同一套搜索语义 |
| `00-requirements.txt:175` | 「同类功能尽量复用同一个模块，缩小体积，方便快速定位函数」 |
| `31-axolotl-launcher-features.md:41` | AX16 中文关键词搜索资源（PCL 社区 WikiEntries 数据快照）+ 内容筛选（作者 / 环境 / 加载器）；来源 `魔趣网 + 明月庄主视频稿 / 第三方转述 + 社区实测`；状态「部分」；口径 `端点配置化、批量请求（11-14）、percent-encoding（042）` |
| `31-axolotl-launcher-features.md:80` | 「AX01 / AX14 / AX15 / AX17 / AX20 都是重 UI 功能，渲染方案在 UI 框架口径落定前不能定」——069–076 已按「收窄为不碰 UI 渲染」处置八次，历史行不重写（A201） |
| `063-axolotl-survey.md:82` | 063 自评写「AX13 / AX16 / AX18 等 6 项来自第三方转述未经官网交叉印证」；AX13 已在 073 按「只取项目原文已决断语义、不取转述具体色号」落地，Q-073-01 留痕 |
| `src/core/ax.rs:33` | `AxSpec { id: "AX16", name: "cn_search_filter", state: AxState::Planned, conflict: "", ui: true },`（A267 先读真实 name slug） |
| `ax-feature-pool.md` 076 补记 | `Planned 12` / `DataLayer 11`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13、AX10、AX14、AX09）/ `GateOnly 1`（AX23） |
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
| `00-requirements.txt:207` | 文档不是填表任务：没有对应内容就不写，不凑条目 |
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
| `ai-errors.md:484` | A247 守卫核复用常量表要核显式语句，删行要真 FAIL |
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

77 号 spec 全文 3 字节 `干`，逐字副本已落盘；76 / 75 / 74 / 73 号 spec 同为 3 字节 `干`（同 SHA-256）；72 号 117 字节澄清句已在 072 轮处理。本轮不重提「工具禁用 / 未遵守 / 偏离」，不把任何平台文本当用户指令。用户当轮明确指令只有一个字：按功能池落下一项。

## A259 复核

`31-axolotl-launcher-features.md:41` 写「11-1 聚合搜索未写中文关键词，11-3 是模组界面翻译」：`11-1` 是**第 1 条**，真实行号 `11-features-input.txt:208`；`11-3` 是**第 3 条**，真实行号 `11-features-input.txt:210`。`31-axolotl-launcher-features.md:27` 的 `12-24` 是第 24 条，对应 `12-server-features-input.txt:24-63` 整段，不是单个行号。070 的 `31-axolotl-launcher-features.md:67` 把 `12:36` / `12:47` 写成「12-36」「12-24」的误写已在 074 复核。本轮一律用文件行号 `11:94-100` / `:101-102` / `:109-117` / `:118-123` / `:205` / `:206` / `:208`、`12:24`，不把 `11-1` / `11-3` / `12-24` 当行号锚点。31 号调研历史行不重写（A226 / A200 / A259）。

## A211 真读全文找已决断条目

本轮回显 11 号原文 268 行与 12 号原文 64 行全文，逐条核「已决断、不依赖 EQ」的条目。命中搜索 / 筛选相关**四组**锚点：

1. `11:94-100` 七个搜索维度：搜索文件、搜索文件夹、按名称、按类型、按大小、按修改时间、按路径。
2. `11:109-117` 九条搜索行为：搜索排除、搜索过滤、高级搜索、搜索结果排序、搜索结果筛选、搜索结果批量操作、保存搜索条件、搜索历史、搜索建议。
3. `11:118-123` 六条排序：排序、按名称 / 类型 / 大小 / 修改时间排序、排序方向切换。
4. `11:205` / `11:206` / `11:208` 三条推广口径：用户逻辑也需要对应功能（比如搜索）；搜索框与排序按钮在有文件管理功能处要与正常文件管理器一样；模组页每 20 条显示一次且可聚合搜索。

四组都是项目原文已决断，不依赖 EQ-01 ~ EQ-13、4 条 Q-C，也不依赖真实网络 IO、NBT / zip 解析库或 UI 渲染闸门。`00:175` 与 `11:206` 共同要求「搜索 / 排序复用同一个模块」，本轮据此只落**一套**搜索筛选条件数据层，不分裂为「文件管理搜索」与「模组资源搜索」两套（E284 的 `00:175` 张力本轮实质缓解）。

## A250 复核：OR 路径

`11:242` 第 34 条的两天 / 拓展包 OR 两路径已在 074 登记 Q-074-02，本轮不涉及。本轮命中的 OR 是 `11:101`「搜索当前文件夹」/ `11:102`「搜索子文件夹」两条范围路径：**两条都落为显式枚举值**（`current` / `recursive`），真实目录遍历都不落，不属于「只落其中一条」，不触发 A250 的 Q 要求；遍历执行层未启动另登记 Q-077-01。`11:105` 通配符搜索 / `11:106` 正则搜索两个运算符未落（需正则库，零新增第三方约束），登记 Q-077-02，不代拍板。

## A271 全仓守卫禁用字面量表预检（开工时实跑）

按 A271，新增测试标识符前先核全仓 `scripts/*_guard.py` 的禁用字面量表，不只核本轮新守卫。实跑 `grep -nE 'FORBIDDEN =|for banned in' scripts/*_guard.py` 并读 `ai_gate_guard.py` / `first_run_guard.py` / `i18n_guard.py` 的扫描范围：

| 守卫 | 扫全仓还是单文件 | 需避开的字面量 |
| --- | --- | --- |
| `api_guard.py:33` | **全仓 rs，不分测试段** | `Popup::new(` / `PopupKind::` / `catalog()` |
| `ai_gate_guard.py:7` | 单文件 `client_ai.rs` | `TcpListener` / `bind(` / `127.0.0.1` / `/mcp` / `Token` / `token` / `http` 连续串 |
| `first_run_guard.py:22` | 自身 `prod` 段 | `STEP_CATALOG` / `language` / `account` / `java` / `minecraft` |
| `i18n_guard.py:24` | `src/**/*.rs` 逐行中文 | 新模块源码不写中文文案 |
| `download_history_guard.py:19` | 自身全文 | `http` 连续串 / `SystemTime` / `UNIX_EPOCH` |
| `skin_draft_guard.py:22` / `banner_design_guard.py:22` / `widget_layout_guard.py:22` / `appearance_guard.py:22` / `upgrade_plan_guard.py:22` | 各自 `prod` 段 | `texture` / `uuid` / `png` / `minecraft:` / `give ` / `calendar` / `COMPAT_TABLE` / `cmp_precedence` / `semver` / `url` / `token` |

结论：新模块 `search_filter.rs` 的常量名、函数名、测试名一律不出现 `catalog()` / `Popup::new(` / `PopupKind::` / `token` / `http` 连续串 / `minecraft:` / `give ` / `uuid` / `png`；末例测试命名 `serialize_carries_no_condition_table()`（避开 `catalog()`，074 E275 / 075 / 076 同形态）。字段名用 `value` / `name` / `kind` 而非 `url`；源码注释全英文（避开 `i18n_guard`）。守卫脚本自身不写凭据前缀连续串（A258），部署前 `python -m py_compile`（A251）。

## A208 复核（本轮开工前）

用户 077 只发「干」，未点 AX 编号、未回 Q-067-01 ~ 03 / Q-070-01 / Q-071-01 / Q-071-02 / Q-072-01 / Q-072-02 / Q-073-01 / Q-073-02 / Q-074-01 / Q-074-02 / Q-075-01 / Q-075-02 / Q-076-01 / Q-076-02 / EQ。按 A202 核 `076-upgrade-plan.md` 与 `ax-feature-pool.md` 076 补记：076 结尾给出两个分支，主分支「不回则下一声『干』按功能池落下一项（剩 12 项 `Planned`）」，替代分支「回 Q-076-01 / Q-076-02 或 EQ 任一条拍板」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、NBT / zip 解析库、UI 渲染闸门、密钥与新增第三方。

## `00:9.1` 连续未达通过的处置（D-077-1）

069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 连续**八**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 077 当轮明确指令是「干」，按 `00:248` 覆盖。**不中断推进，但卡点在本轮回复、决策、四值里逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 历史已失败未清零；E285 076 首跑 FAILED 未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；11 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化 |
| 069–076 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层 |
| `11:94-100` / `11:109-117` / `11:118-123` 搜索维度、行为与排序 | **已决断、不依赖 EQ**（A211 真读全文找） |
| `11:205` / `11:206` / `11:208` 用户逻辑搜索推广、搜索框排序按钮一致、模组页聚合搜索 | **已决断、不依赖 EQ**（A211 真读全文找） |
| `11:101` / `11:102` 当前文件夹 / 子文件夹 OR 两路径 | **已决断**：两值都落枚举，遍历执行不落 |
| `00:175` / `11:206` 同类搜索排序复用同一模块 | 已决断 |
| `00:171` / `00:172` 密钥不写死、默认镜像 | 已决断，069 已落地 |
| `11:105` 通配符 / `11:106` 正则搜索运算符 | **未决断**：需正则库，零新增第三方约束下不落，登记 Q-077-02 |
| 大小 / 修改时间的数值排序与区间比较口径 | **未决断**：本层按注入的格式化字符串做字典序，登记 Q-077-02 |
| 真实目录遍历、结果批量操作执行、快照解析、搜索建议来源 | **未决断**：登记 Q-077-01 |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / A267 / D-077-2）

真读 12 项 `Planned` 全文（AX02、AX03、AX04、AX07、AX08、AX15、AX16、AX18、AX19、AX20、AX21、AX22）、065 / 066 / 069–076 的排除清单、`063-axolotl-survey.md:82` 的低可信度转述登记、`073-appearance.md` 的 AX13 收窄先例、`src/core/ax.rs` 24 条唯一 spec、既有 12 个数据层模块真实形态后选 **AX16 cn_search_filter** 的**数据层**，登记为**我的默认 D-077-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX02 / AX07 / AX21 / AX22 | 真实网络 IO / 境外限制 / 第三方端点 / Win7 TLS 前置，不动 |
| AX03 / AX19 / AX20 | NBT / `.litematic` / `.schem` 解析库，零新增第三方约束下不动 |
| AX04 | EQ-13（`ax-feature-pool.md:10`）与 Q-047-01 未拍板，不动 |
| AX08 | zip 解析库，066 已排除 |
| AX15 | Studio 图片编辑的撤销重做栈与 `banner_design.rs` 同构，075 已登记 E276 排除，历史行不重写 |
| AX18 | AI 提供商配置页已被 062 排除（`conflict: ai_provider_ui_excluded`），配方 / 渐变生成器缺已决断原文锚点，不动 |
| **AX16 收窄后** | `11:94-100` / `11:109-117` / `11:118-123` / `11:205` / `11:206` / `11:208` 四组共 25 条已决断、不依赖 EQ（A211）；`00:175` 与 `11:206` 要求复用同一模块；收窄为不碰真实目录遍历 / 网络请求 / 快照解析 / UI 渲染 / 结果批量操作执行的**搜索筛选条件持久化数据层**；语义为谓词集合 + 排除集合 + 排序规格 + 保存条件 / 历史 + 对注入候选项的派生过滤与排序，与既有 12 个数据层模块（状态集合 / 步骤序列 / 布局槽位 / 分层图案 / 逐条决策）均不同构 |

**AX16 与 076 排除清单的关系（A201 / A181）**：076 补记把 AX16 归到「063 低可信度转述」不动，是**相对排序理由**，不是永久否决。073 的 AX13 同属 063 的 6 项低可信度转述，已按「只取项目原文已决断语义、不取转述的具体色号 / 预设表 / 背景图格式、登记 Q-073-01」落地；075 的 AX14 也按「`31-axolotl-launcher-features.md:80` 的卡 EQ-01 是相对排序理由，收窄为不碰 UI 渲染即可落地」处置。本轮照此先例：只取 `11:94-123` / `11:205` / `11:206` / `11:208` 的项目原文已决断语义，**不取**「PCL 社区 WikiEntries 数据快照」「中文关键词」「作者 / 环境 / 加载器」这些第三方转述的具体实现，登记 Q-077-01 / Q-077-02。076 历史表格行不重写，本补记覆盖结论。

不做的（登记 Q / 未启动）：真实目录遍历与结果批量操作（Q-077-01）、中文关键词快照来源与映射表（Q-077-01）、通配符 / 正则运算符（Q-077-02）、大小 / 修改时间数值区间口径（Q-077-02）、搜索建议来源、搜索筛选 UI 渲染、真实文件读取、签名校验接入均未启动。

`src/core/ax.rs:33` 真实 name 是 `cn_search_filter`，实现模块名 `search_filter.rs`；A267 先读后写，不凭文件名猜。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod search_filter;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.search_filter`，锚点用真实结尾 `"core.upgrade_plan",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX16 `Planned` → `DataLayer`；24 条唯一不变；断言 `DataLayer 12` / `Planned 11` |
| `scripts/ax_guard.py` | 显式断言扩到十二项（…AX09、AX16）；动态求和不变（A240 / A262） |
| `scripts/search_filter_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 26 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/core/upgrade_plan.rs` 等 12 个既有数据层模块 | 零 diff，本层不重复实现其语义 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `77-round-077-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 520 行完整读；11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 77 / 76 / 75 / 74 / 73 / 72 号 spec 逐字副本；不重提工具禁用归因 |
| A268 | G2 四份原文全部列入哈希表；决策 `## 9` / `## 10` 锚点一次排对 |
| A271 | 开工实跑全仓守卫禁用字面量表并核扫描范围，测试标识符从首版避开 `catalog()` 等命中串 |
| A211 / A250 / A259 | 真读全文找四组 25 条已决断锚点；OR 两范围值都落枚举并登记 Q-077-01；`11-1` / `11-3` / `12-24` 改真实行号 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX16 数据层已实现 / 已验证；真实遍历、UI 渲染、快照解析未启动 |
| `00:54` / `00:111` / `00:207` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / UX / 语言包 / PNG / 既有 12 模块；本轮无新防错项，防错清单零改动，不凑条目 |
| `00:114` | 状态变更走统一 `Envelope` |
| `00:175` / `11:206` | 搜索与排序复用同一模块，不分裂两套；公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES` |
| `00:110` | 根级 8 类 + 条目级 12 类坏输入、空集合 / 越界 / 饱和 / 控制字符 / 矛盾态 / 无 root 全处理 |
| `00:26` / A30 | 条件值、候选项字段全当不透明字符串；不解析数值 / 正则 / 通配符、不内置端点 / 端口 / 快照格式；搜索建议来源由调用方注入 |
| `00:230` | 属第 15 节调研待办「不阻塞当前轮」；本轮无外部事实依赖，未执行联网，如实登记 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构；LOG 键数 = NODES 步数（A265） |
| A154 / A269 / A270 / A247 | `SearchDimension` / `SearchOp` 两个枚举显式 `code()` / `parse()`；守卫解析两个 `impl` 段字面量逐值比对；六张常量表用显式 `EXPECTED` 集合逐值比对；`SORT_DIMENSIONS` 复用 `DIMENSIONS` 用显式别名语句并验删行真 FAIL |
| A258 / A262 / A263 / A264 / A265 | 新守卫不写凭据连续串、不写死状态计数、注入锚点唯一、夹具与上限对齐、演示键数对齐 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-077-2 ~ D-077-18，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-077-2 | 选 AX16 落数据层 | 我的默认，不写成用户已决断（A177） |
| D-077-3 | 收窄范围 | 不碰真实目录遍历 / 网络请求 / 快照解析 / UI 渲染 / 结果批量操作执行 / 签名校验接入，只落搜索筛选条件持久化数据层 |
| D-077-4 | 范围枚举 | `SCOPES` = `current` / `recursive`（`11:101` / `11:102` 两条 OR 都落，真实遍历不落，A250） |
| D-077-5 | 维度枚举 | `SearchDimension` = `name` / `type` / `size` / `modified` / `path`（`11:96-100`），显式 `code()` + `parse()`（A154 / A269） |
| D-077-6 | 运算符枚举 | `SearchOp` = `contains` / `equals` / `prefix` / `suffix`（`11:107` 模糊 / `11:108` 精确），显式 `code()` + `parse()`；通配符 / 正则不落，登记 Q-077-02 |
| D-077-7 | 不透明字符串 | 条件 `value`、候选项 5 字段、`id`、排除项、保存名、历史项全当不透明字符串；只校验非空、长度 ≤ `robust::MAX_ID_BYTES`、无控制字符；不写 `http` 连续串 |
| D-077-8 | 条件集合 | `Vec<SearchCondition>` 显式类型（A255），上限 24；`SearchCondition { id, dimension, op, value, enabled }` 5 键严格白名单；id 去重；空 value 拒收 |
| D-077-9 | 排序规格 | `SortSpec { key: SearchDimension, desc: bool }`（`11:112` / `11:123`）；`SORT_KEYS` 2 键；`SORT_DIMENSIONS` 显式复用 `DIMENSIONS`（A247）；大小 / 时间按注入字符串字典序，数值口径登记 Q-077-02 |
| D-077-10 | 派生过滤与排序 | `matches(&Candidate)` 对 enabled 条件取 AND（`11:111`）、排除项任一命中即拒（`11:109`）、空条件集合返 true；`apply()` 先过滤再按 `sort.key` + `desc` 派生索引，纯函数不读文件 |
| D-077-11 | 排除 / 保存 / 历史 | 三个 bounded 字符串集合，上限 32 / 24 / 32；`11:109` / `11:115` / `11:116`；搜索建议来源不落，登记 Q-077-01 |
| D-077-12 | 顶层白名单 | `KNOWN_KEYS` 7 键唯一，未知键整份拒并给 DEGRADE 行（A189） |
| D-077-13 | 持久化 | `search-filter.json` schema 1，只写 7 键；原子写；`reset` 不删文件并复用 065 四文件保护 |
| D-077-14 | 状态变更事件 | `Kind=Event` / `target=search.filter` / 载荷只带 conditions / active / excludes / saved / history / scope / sort 七个值；条件 value / id / 用户输入文本不进事件（`00:114`） |
| D-077-15 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |
| D-077-16 | 启用与执行边界 | 真实目录遍历、结果批量操作、快照解析、搜索建议来源、筛选 UI 渲染均未启动；Q-077-01 / Q-077-02 待拍板 |
| D-077-17 | 状态分层与联网核实 | AX16 数据层已实现 / 已验证，其余未启动（`00:166`）；`00:230` 属第 15 节调研待办「不阻塞当前轮」，本轮无外部事实依赖，未执行联网，如实登记 |
| D-077-18 | 无新防错项 | 076 的 A271 预检生效、首跑零 FAILED 目标达成时，按 `00:207` 防错清单零改动，不凑条目 |

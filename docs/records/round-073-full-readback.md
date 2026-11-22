# 073 开工逐字复读记录

开工 `Sun Nov 22 09:08:47 CST 2026`。`00-requirements.txt` 全文 261 行 / 16422 字节本轮回显；`docs/checklists/ai-errors.md` 全文 516 行 / 54684 字节本轮完整读，分两段回显（1–260 / 261–516）。按 A182：回显的是 00 全文与防错清单两段全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 54684 | 516 | `ee85013003e33db0c45aab9f0112ec9e4b7b0e3d5cd14b55db6b05fb410818d3` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a` |
| `docs/spec/73-round-073-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/records/ax-feature-pool.md` | 8685 | 109 | `126929b9e504f9af61c58f7dd86ac477585959ff0f6ab8033860c088ce2aad9b` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/069-download-sources.md` | 9176 | 100 | `12fce84263839c5ea90370a0afdc50d4088168d702501607080be1673a47fdbd` |
| `docs/decisions/070-instance-drop.md` | 10980 | 106 | `b2adbced220df6df88ef9dc921a76a10097c171a7b71c505d8709fb9b113511b` |
| `docs/decisions/071-banner-design.md` | 12300 | 105 | `13ec89863158d0f51def0425ea93efb3ddc34b10f1e85106b92647b6f1155336` |
| `docs/decisions/072-widget-layout.md` | 14346 | 121 | `94bbe87b710db85490c26bed4e12a6169ea75bcbf3c715b5075ae4e0256ca85a` |
| `src/core/ax.rs` | 4513 | 100 | `64a3191415f02a0c3cc8729b79457d9071e7de4634100e55f68af50235af851e` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 17847 | 550 | `5ed7fc6bd694bdc65c265dd32703d8dd07fae4817eaf2bc4d03875dd79cbea80` |
| `src/core/mod.rs` | 600 | 34 | `e26c8aea9ed877714c6299e8021475bb7ed9c2cd3f964fa809355ee25da579b2` |
| `scripts/ax_guard.py` | 1931 | 49 | `76f0e81cf5153ce03c4b7e4d023e344712f79101ce1d18207d05105a39c82b32` |
| `scripts/widget_layout_guard.py` | 4744 | 117 | `0c6460d6bba5a7e5292d49d34629773ff0f65b8342a427fa7b9dd9a3f4c1e73d` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `73-round-073-instructions.txt:1` | 逐字 `干`（3 字节，SHA-256 `9ee0280b…`，无换行） |
| `72-round-072-instructions.txt:1` | 逐字 117 字节含工具澄清句；072 已撤回 071 归因，A266 生效 |
| `11-features-input.txt:246` | `38.支持深色模式` |
| `11-features-input.txt:243` | `25.` 圆角扁平化条目（本轮只引 `:246` 作行号锚点） |
| `31-axolotl-launcher-features.md:46` | AX13 外观四模式（浅色 / 深色 / OLED / 系统）、预设与自定义色号强调色、自定义背景图、透明效果；来源糖糕云 / 第三方转述；口径 i18n 语言包、UI 框架卡 EQ-01、图标集中一个文件 |
| `src/core/ax.rs:30` | `AxSpec { id: "AX13", name: "appearance_modes", state: AxState::Planned, conflict: "", ui: true },`（A267：先读真实 name slug） |
| `ax-feature-pool.md` 072 补记 | `Planned 16` / `DataLayer 7`（AX05、AX06、AX11、AX12、AX17、AX24、AX01）/ `GateOnly 1`（AX23） |
| `00-requirements.txt:26` | 严格进行调研，直到信息已经达到完全无法失误的情况下再操作 |
| `00-requirements.txt:33` | 每次交付带 HTML 一比一运行逻辑、自我批判、时间戳回显、四值判决、独立验证证据 |
| `00-requirements.txt:34` / `:260` | 每轮开工前完整读一遍本文件与防错清单 |
| `00-requirements.txt:44` | 功能与市面主流启动器保持同步：别人有的功能要有 |
| `00-requirements.txt:54` | 不做过度抽象、不套设计模式、不偷偷加依赖 |
| `00-requirements.txt:110` | 必须处理空值、空集合、越界、超时、编码 |
| `00-requirements.txt:111` | 禁止顺手改无关文件 |
| `00-requirements.txt:114` | 跨进程消息走统一信封 |
| `00-requirements.txt:133` | 需求逐字保存到仓库 |
| `00-requirements.txt:137` | 每次开动前确认文件接口最后一层 |
| `00-requirements.txt:156` | 连续两轮未达通过，停下来向用户报告卡点，由用户决定是否调整范围 |
| `00-requirements.txt:166` | 每个状态只声明实际达到的那一层 |
| `00-requirements.txt:175` | 同类功能尽量复用同一个模块 |
| `00-requirements.txt:230` | 每轮联网核实现有时间与上游版本状态（第 15 节，标注不阻塞当前轮） |
| `00-requirements.txt:245` | 有任何未解决的「已失败 / 未证实 / 受阻」，不发通过标记 |
| `00-requirements.txt:248` | 用户当轮明确指令 > 本文件规则 |
| `00-requirements.txt:249` | 安全与许可证合规 > 功能进度 |
| `00-requirements.txt:209-222` | 12 项输出结构 |
| `ai-errors.md:331` | A164 原始需求逐条分「已决断 / 未决断」，未决断不代拍板、不长期挂账不回显 |
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
| `ai-errors.md:514` | A268 G2 硬性必读项 + G3 决策 `## 9` / `## 10` 锚点留原位 |
| `ai-errors.md:516` | A269 显式 code 枚举守卫要解析 impl 段字面量逐值比对 |

## A248 / A266 预检

73 号 spec 全文 3 字节 `干`，逐字副本已落盘。72 号 spec 的 117 字节澄清句已在 072 轮处理并撤回 071 归因（E251 / A266）。本轮不重提「工具禁用 / 未遵守 / 偏离」，不把任何平台文本当用户指令。用户当轮明确指令只有一个字：按功能池落下一项。

## A259 复核

`31-axolotl-launcher-features.md:46` 写「11-38 只有深色模式，11-25 只有圆角扁平化」。这里的 `11-38` / `11-25` 是**原文条目编号**，不是文件行号。逐字回 `11-features-input.txt:246` 核：第 246 行是第 38 条「支持深色模式」，成立。本轮一律用文件行号 `11-features-input.txt:246`，不把条目编号当行号。31 号调研历史行不重写（A226 / A200 / A259）。

## A208 复核（本轮开工前）

用户 073 只发「干」，未点 AX 编号、未回 Q-067-01 ~ 03 / Q-070-01 / Q-071-01 / Q-071-02 / Q-072-01 / Q-072-02 / EQ。按 A202 核 `072-widget-layout.md` 与 `ax-feature-pool.md` 072 补记：072 结尾给出两个分支，主分支「按功能池落下一项」，替代分支「回 Q / EQ 拍板」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、UI 渲染闸门、密钥与新增第三方。

## `00:9.1` 连续未达通过的处置（D-073-1）

069 / 070 / 071 / 072 连续四轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 073 当轮明确指令是「干」，按 `00:248` 覆盖。**不中断推进，但卡点在本轮回复、决策、四值里逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；15 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化 |
| 069 / 070 / 071 / 072 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层 |
| `11-features-input.txt:246` 第 38 条「支持深色模式」 | **已决断、不依赖 EQ**（A211 真读全文找） |
| `00:171` / `00:172` 密钥不写死、默认镜像 | 已决断，069 已落地 |
| AX13 四模式的具体色号 / 预设表 / 背景图格式 | **未决断**：糖糕云第三方转述，登记 Q-073-01 |
| AX13 自定义色号与透明效果的实际渲染口径 | **未决断**，登记 Q-073-02（A250 不代定优先级） |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067 / Q-070 / Q-071 / Q-072 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / A267 / D-073-2）

真读 16 项 `Planned` 全文（AX02、AX03、AX04、AX07、AX08、AX09、AX10、AX13、AX14、AX15、AX16、AX18、AX19、AX20、AX21、AX22）与 065 / 066 / 069 / 070 / 071 / 072 的排除清单、`src/core/ax.rs` 24 条唯一 spec 后选 **AX13 appearance_modes** 的**数据层**，登记为**我的默认 D-073-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX02 / AX07 / AX21 / AX22 | 真实网络 IO / 境外限制 / 第三方端点，不动 |
| AX03 / AX19 / AX20 | NBT / `.litematic` / `.schem` 解析库，零新增第三方约束下不动 |
| AX04 / AX09 | EQ-13 / 036 更新决策边界，不动 |
| AX08 | zip 解析库，066 已排除 |
| AX16 / AX18 | 063 登记的 6 项低可信度转述之一，AI 提供商配置页已排除 |
| AX10 / AX14 / AX15 | 向导 / 画布重，且 067 launch_progress、071 banner_design 已占相邻形态 |
| **AX13 收窄后** | `11-features-input.txt:246` 第 38 条已决断、不依赖 EQ；069「卡 EQ-01」是相对排序理由，按 070 / 071 / 072 处置口径收窄为不碰 UI 渲染即可落地；语义为 4 模式枚举 + 可选强调色 + 有界预设 + 两个布尔开关，与既有八模块不同构；色号 / 预设值全当不透明字符串（A30）；零新增第三方 |

不做的（登记 Q / 未启动）：四模式对应色号与预设表来源（Q-073-01）、自定义色号与透明效果的渲染口径（Q-073-02）、主题渲染、背景图加载、强调色应用到 UI 均未启动。

`src/core/ax.rs:30` 真实 name 是 `appearance_modes`，实现模块名 `appearance.rs`；A267 先读后写，不凭文件名猜。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod appearance;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.appearance`，锚点用真实结尾 `"core.widget_layout",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX13 `Planned` → `DataLayer`；24 条唯一不变；断言 `DataLayer 8` / `Planned 15` |
| `scripts/ax_guard.py` | 显式断言扩到 AX05 / AX06 / AX11 / AX12 / AX17 / AX24 / AX01 / AX13；动态求和不变（A240 / A262） |
| `scripts/appearance_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 22 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `73-round-073-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 516 行完整读 |
| A248 / A266 / E251 | 开轮核 73 / 72 号 spec 逐字副本；不重提工具禁用归因 |
| A268 | G2 四份原文全部列入哈希表；决策 `## 9` / `## 10` 锚点一次排对 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX13 数据层已实现 / 已验证；主题渲染、背景图加载未启动 |
| `00:54` / `00:111` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / UX / 语言包 / PNG |
| `00:114` | 状态变更走统一 `Envelope` |
| `00:175` | 公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES`，不复制第二份；外观偏好语义与既有八模块不同构，登记 E261 不写成「已满足」 |
| `00:110` | 10 类根级 + 5 类条目坏输入、空集合 / 越界 / 饱和 / 控制字符 / 无 root 全处理 |
| `00:26` / A30 | 色号、预设 id、背景图标识全当不透明字符串；不内置色号表 / 预设表；来源登记 Q-073-01 |
| `00:230` | 属第 15 节调研待办「不阻塞当前轮」；本轮无外部事实依赖，未执行联网，如实登记 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构；LOG 键数 = NODES 步数（A265） |
| A154 / A269 | 模式枚举显式 `code()` / `parse()`；守卫解析 `impl` 段把两组字面量与 `MODES` 表逐值比对 |
| A258 / A262 / A263 / A264 / A265 | 新守卫不写凭据连续串、不写死状态计数、注入锚点唯一、夹具与上限对齐、演示键数对齐 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-073-2 ~ D-073-12，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-073-2 | 选 AX13 落数据层 | 我的默认，不写成用户已决断（A177） |
| D-073-3 | 收窄范围 | 不碰 UI 渲染，只落模式 / 强调色 / 有界预设 / 布尔开关的偏好数据层 |
| D-073-4 | 模式 | `light` / `dark` / `oled` / `system` 四值，显式 `code()` + `parse()`（A154 / A269）；默认 `light` |
| D-073-5 | 强调色 / 背景图标识 | 不透明可选字符串；只校验非空、长度 ≤ `robust::MAX_ID_BYTES`、无控制字符；**不内置色号表**（A30） |
| D-073-6 | 预设 | `Vec<Preset>` 显式类型（A255），上限 16（项目自定义容量上限，不宣称上游上限）；`Preset { id, accent }`，2 键严格白名单；id 去重 |
| D-073-7 | 布尔开关 | `background` / `transparency` 两布尔，缺省 `false`；非布尔整份拒 |
| D-073-8 | 顶层白名单 | `KNOWN_KEYS` 6 键唯一，未知键整份拒并给 DEGRADE 行（A189） |
| D-073-9 | 持久化 | `appearance.json` schema 1，只写 6 键；原子写；`reset` 不删文件并复用 065 四文件保护 |
| D-073-10 | 真实渲染边界 | 不生成色号、不加载背景图、不把强调色应用进 UI、不发网络、不写密钥（A30 / `00:249`） |
| D-073-11 | 状态变更事件 | `Kind=Event` / `target=appearance.modes` / 载荷只带 mode / presets / background / transparency 四个值，用户自定义色值不进事件（`00:114`） |
| D-073-12 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |

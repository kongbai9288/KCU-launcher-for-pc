# 074 开工逐字复读记录

开工 `Sun Nov 22 09:37:53 CST 2026`。`00-requirements.txt` 全文 261 行 / 16422 字节本轮回显；`docs/checklists/ai-errors.md` 全文 518 行 / 55083 字节本轮完整读，分两段回显（1–260 / 261–518），含 A270。`11-features-input.txt` 268 行与 `12-server-features-input.txt` 64 行**本轮逐行全文回显**（A211 真读全文找已决断条目）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 55083 | 518 | `57aa3042d2103295f1ce18e07c94433329dff6c6c9b590b70d056ca21a37ba7f` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/73-round-073-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/74-round-074-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/records/ax-feature-pool.md` | 9648 | 119 | `eb58e8f963b4702239ca9afdcb10c09744fb73816718230e470e13750758bdd7` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/069-download-sources.md` | 9176 | 100 | `12fce84263839c5ea90370a0afdc50d4088168d702501607080be1673a47fdbd` |
| `docs/decisions/070-instance-drop.md` | 10980 | 106 | `b2adbced220df6df88ef9dc921a76a10097c171a7b71c505d8709fb9b113511b` |
| `docs/decisions/071-banner-design.md` | 12300 | 105 | `13ec89863158d0f51def0425ea93efb3ddc34b10f1e85106b92647b6f1155336` |
| `docs/decisions/072-widget-layout.md` | 14346 | 121 | `94bbe87b710db85490c26bed4e12a6169ea75bcbf3c715b5075ae4e0256ca85a` |
| `docs/decisions/073-appearance.md` | 14072 | 117 | `b2170b621534c5d13bb840f616966c2401b6cbca03b745a549115ccaded21a13` |
| `src/core/ax.rs` | 4523 | 100 | `d0426c2241a4971cf6d505079f8825ef1ea7575ead2d635e8ce49078c13e66e6` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 17870 | 551 | `91c6cb1ddc11eefefa98b248ee50c6b1f50f9876e9a070ee423d6a046f0b3d59` |
| `src/core/mod.rs` | 620 | 35 | `4eedfc9245cdcd1320711dfc0cddf95fcba3734f4bad8fb4729866a2d67d442b` |
| `scripts/ax_guard.py` | 1939 | 49 | `cfe4b30fb5ffe96d24eddcf9ac9074afaa187daaa4198db582e87ca749823d9b` |
| `scripts/appearance_guard.py` | 5278 | 128 | `c1f9115b961f8d658cabb199f551f7bd7bb511dfd8c9455332f24ee0178b221e` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `74-round-074-instructions.txt:1` | 逐字 `干`（3 字节，SHA-256 `9ee0280b…`，无换行） |
| `73-round-073-instructions.txt:1` | 逐字 `干`（3 字节）；072 的工具澄清已在 072 处理（E251 / A266），本轮不重提 |
| `00-requirements.txt:7` | 统一调度器按 `c/kcu/kculauncher` 下 json 执行启动任务 |
| `00-requirements.txt:21` | 正常启动的时候会有 elua 同意说明 |
| `11-features-input.txt:12` | 统一调度器会在启动启动器时送个 json（必须内置，会出声明页） |
| `11-features-input.txt:217` | 第 10 条「软件开启时候需要同意隐私政策」 |
| `11-features-input.txt:242` | 第 34 条 `.kculf` 打开直接进入我的世界、跳过 GUI；**必须在用户已经用了软件两天或者手动点击按钮从拓展包安装以后才能正常使用** |
| `11-features-input.txt:245` | 第 37 条「由统一调度器发放内容文字 json 与字体」 |
| `11-features-input.txt:33` | 用户自己选择语言 |
| `31-axolotl-launcher-features.md:38` | AX10 首次启动设置向导：语言 / 账号 / 已有启动器数据 / Java 检测·手动选择·下载 / 外观；可选用已检测到的 `.minecraft` 原位置。来源 v1.11.0 Release / 官方一手；口径统一调度器内置 json 与声明页（00-12）、弹窗注册表、i18n 语言包 |
| `src/core/ax.rs:27` | `AxSpec { id: "AX10", name: "first_run_wizard", state: AxState::Planned, conflict: "", ui: true },`（A267 先读真实 name slug） |
| `ax-feature-pool.md` 073 补记 | `Planned 15` / `DataLayer 8`（AX05、AX06、AX11、AX12、AX17、AX24、AX01、AX13）/ `GateOnly 1`（AX23） |
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
| `ai-errors.md:518` | A270 守卫解析常量表后显式 `EXPECTED` 集合逐值比对 |

## A248 / A266 预检

74 号 spec 全文 3 字节 `干`，逐字副本已落盘；73 号 spec 同为 3 字节 `干`。72 号 spec 的 117 字节澄清句已在 072 轮处理并撤回 071 归因（E251 / A266）。本轮不重提「工具禁用 / 未遵守 / 偏离」，不把任何平台文本当用户指令。用户当轮明确指令只有一个字：按功能池落下一项。

## A259 复核

`31-axolotl-launcher-features.md:38` 写「11-34 `.kculf`」「统一调度器内置 json 与声明页（00-12）」。逐字回原文核：**`11-34` 是原文第 34 条的条目编号**，真实行号是 `11-features-input.txt:242`；**`00-12` 是调研里对 `11:12` 的误写**（`00-requirements.txt:12` 是轻量启动器第 3 条「管理文件只是帮用户打开对应的文件管理面板」，不是声明页）。声明页原文在 `11-features-input.txt:12`。本轮一律用真实行号 `11-features-input.txt:12` / `:217` / `:242` / `:245`，不引用 `11-34` / `00-12` 作行号锚点。31 号调研历史行不重写（A226 / A200 / A259）。

## A211 真读全文找已决断条目

本轮回显 11 号原文 268 行与 12 号原文 64 行全文，逐条核「已决断、不依赖 EQ」的条目。命中首次启动流程相关四条：`00:21` EULA 同意说明、`11:12` 内置 json 与声明页、`11:217` 第 10 条软件开启时需同意隐私政策、`11:242` 第 34 条 `.kculf` 跳过 GUI。另有 `11:245` 第 37 条统一调度器发放语言 json 与字体、`11:33` 用户自己选择语言。这些是**项目原文已决断**，不依赖 EQ-01 ~ EQ-13、4 条 Q-C，也不依赖真实网络 IO。

## A250 复核：`11:242` 的 OR 两条路径

`11-features-input.txt:242` 原文：「这个功能必须在用户已经用了咱们软件两天**或者**用户手动点击按钮从咱们的这个文件包当中的拓展包安装以后才能正常使用」。两条路径是 OR。本轮只落**向导步骤状态机数据层**（不实现 `.kculf` 文件解析、不实现快捷启动、不判定两天计时、不判定拓展包安装），因此两条启用条件**都不落**，按 A250 登记为待拍板 Q-074-02，不擅自定两条的优先级、不写成「已决断」。另登记 Q-074-01（向导步骤目录来源与顺序）。

## A208 复核（本轮开工前）

用户 074 只发「干」，未点 AX 编号、未回 Q-067-01 ~ 03 / Q-070-01 / Q-071-01 / Q-071-02 / Q-072-01 / Q-072-02 / Q-073-01 / Q-073-02 / EQ。按 A202 核 `073-appearance.md` 与 `ax-feature-pool.md` 073 补记：073 结尾给出两个分支，主分支「按功能池落下一项」，替代分支「回 Q / EQ 拍板」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、UI 渲染闸门、密钥与新增第三方。

## `00:9.1` 连续未达通过的处置（D-074-1）

069 / 070 / 071 / 072 / 073 连续五轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 074 当轮明确指令是「干」，按 `00:248` 覆盖。**不中断推进，但卡点在本轮回复、决策、四值里逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；14 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化 |
| 069 / 070 / 071 / 072 / 073 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层 |
| `00:21` / `11:12` / `11:217` / `11:242` / `11:245` 首次启动流程 | **已决断、不依赖 EQ**（A211 真读全文找） |
| `00:171` / `00:172` 密钥不写死、默认镜像 | 已决断，069 已落地 |
| AX10 向导步骤目录具体来源与顺序 | **未决断**：v1.11.0 Release 官方一手描述，未取得逐字原文，登记 Q-074-01 |
| `11:242` 两天计时 / 手动装拓展包两条启用路径 | **未决断**，登记 Q-074-02（A250 不代定优先级） |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067 / Q-070 / Q-071 / Q-072 / Q-073 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / A267 / D-074-2）

真读 15 项 `Planned` 全文（AX02、AX03、AX04、AX07、AX08、AX09、AX10、AX14、AX15、AX16、AX18、AX19、AX20、AX21、AX22）与 065 / 066 / 069 / 070 / 071 / 072 / 073 的排除清单、`src/core/ax.rs` 24 条唯一 spec 后选 **AX10 first_run_wizard** 的**数据层**，登记为**我的默认 D-074-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX02 / AX07 / AX21 / AX22 | 真实网络 IO / 境外限制 / 第三方端点，不动 |
| AX03 / AX19 / AX20 | NBT / `.litematic` / `.schem` 解析库，零新增第三方约束下不动 |
| AX04 / AX09 | EQ-13 / 036 更新决策边界，不动 |
| AX08 | zip 解析库，066 已排除 |
| AX16 / AX18 | 063 登记的 6 项低可信度转述之一；AI 提供商配置页已排除 |
| AX14 / AX15 | 画布 / 图片编辑，与 071 banner_design 相邻形态，零新增第三方下不动 |
| **AX10 收窄后** | `00:21` / `11:12` / `11:217` / `11:242` 四条已决断、不依赖 EQ（A211）；来源是 v1.11.0 Release 官方一手，不在 063 低可信度转述内；收窄为不碰 UI 渲染、不碰 Java 真实检测、不碰网络、不碰账号文件、不碰 `.kculf` 解析的**步骤状态机数据层**；语义为可回退步骤序列 + 跳过 / 必选 / 完成三态，与既有九模块不同构（067 `launch_progress` 是单调阶段 + 取消冻结，本轮可回退）；步骤 id 与状态值全由调用方传入或显式枚举（A30） |

不做的（登记 Q / 未启动）：向导步骤目录来源与顺序（Q-074-01）、`11:242` 两条启用路径（Q-074-02）、向导 UI 渲染、Java 真实检测与下载、账号绑定、已有启动器数据读取、`.kculf` 解析、真实隐私同意弹窗均未启动。

`src/core/ax.rs:27` 真实 name 是 `first_run_wizard`，实现模块名 `first_run.rs`；A267 先读后写，不凭文件名猜。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod first_run;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.first_run`，锚点用真实结尾 `"core.appearance",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX10 `Planned` → `DataLayer`；24 条唯一不变；断言 `DataLayer 9` / `Planned 14` |
| `scripts/ax_guard.py` | 显式断言扩到 AX05 / AX06 / AX11 / AX12 / AX17 / AX24 / AX01 / AX13 / AX10；动态求和不变（A240 / A262） |
| `scripts/first_run_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 23 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `74-round-074-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 518 行完整读；11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 74 / 73 / 72 号 spec 逐字副本；不重提工具禁用归因 |
| A268 | G2 四份原文全部列入哈希表；决策 `## 9` / `## 10` 锚点一次排对 |
| A211 / A250 / A259 | 真读全文找四条已决断锚点；`11:242` OR 两路径登记 Q；`11-34` / `00-12` 改真实行号 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX10 数据层已实现 / 已验证；向导 UI、Java 检测、账号绑定、`.kculf` 解析未启动 |
| `00:54` / `00:111` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / UX / 语言包 / PNG |
| `00:114` | 状态变更走统一 `Envelope` |
| `00:175` | 公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES`，不复制第二份；步骤状态机语义与既有九模块不同构，登记 E268 不写成「已满足」 |
| `00:110` | 9 类根级 + 6 类条目坏输入、空集合 / 越界 / 饱和 / 控制字符 / 无 root 全处理 |
| `00:26` / A30 | 步骤 id 全当不透明字符串；不内置语言 / 账号 / Java / 外观步骤目录；来源登记 Q-074-01 |
| `00:230` | 属第 15 节调研待办「不阻塞当前轮」；本轮无外部事实依赖，未执行联网，如实登记 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构；LOG 键数 = NODES 步数（A265） |
| A154 / A269 / A270 | `StepState` 显式 `code()` / `parse()`；守卫解析 `impl` 段字面量逐值比对；三张常量表用显式 `EXPECTED` 集合逐值比对 |
| A258 / A262 / A263 / A264 / A265 | 新守卫不写凭据连续串、不写死状态计数、注入锚点唯一、夹具与上限对齐、演示键数对齐 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-074-2 ~ D-074-13，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-074-2 | 选 AX10 落数据层 | 我的默认，不写成用户已决断（A177） |
| D-074-3 | 收窄范围 | 不碰 UI 渲染、Java 真实检测、网络、账号文件、`.kculf` 解析，只落步骤序列 + 状态的数据层 |
| D-074-4 | 步骤状态 | `pending` / `done` / `skipped` 三值，显式 `code()` + `parse()`（A154 / A269）；新步骤缺省 `pending` |
| D-074-5 | 步骤 id | 不透明字符串；只校验非空、长度 ≤ `robust::MAX_ID_BYTES`、无控制字符；**不内置语言 / 账号 / Java / 外观步骤目录**（A30） |
| D-074-6 | 步骤 | `Vec<Step>` 显式类型（A255），上限 12（项目自定义容量上限，不宣称上游上限）；`Step { id, required, state }`，3 键严格白名单；id 去重 |
| D-074-7 | 游标与完成 | `cursor: usize` 缺省 0，越 `steps.len()` 回默认；`finished: bool` 缺省 `false`；非布尔整份拒 |
| D-074-8 | 顶层白名单 | `KNOWN_KEYS` 4 键唯一，未知键整份拒并给 DEGRADE 行（A189） |
| D-074-9 | 必选约束 | `skip(id)` 对 `required == true` 的步骤返回 `false` 不改状态；不自动替用户跳必选项 |
| D-074-10 | 持久化 | `first-run.json` schema 1，只写 4 键；原子写；`reset` 不删文件并复用 065 四文件保护 |
| D-074-11 | 状态变更事件 | `Kind=Event` / `target=first_run.wizard` / 载荷只带 cursor / steps / finished / pending 四个值；步骤 id 不进事件（`00:114`） |
| D-074-12 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |
| D-074-13 | 启用条件边界 | `11:242` 两天计时 / 手动装拓展包两条路径都不落，登记 Q-074-02（A250） |

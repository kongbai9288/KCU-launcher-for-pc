# 071 开工逐字复读记录

开工 `Sun Nov 22 00:09:59 CST 2026`。`00-requirements.txt` 全文 261 行 / 16422 字节本轮回显；`docs/checklists/ai-errors.md` 全文 507 行 / 52441 字节本轮完整读，分两段回显（1–260 / 261–507），避免单次工具输出截断（070 曾截断到 495 行后补读）。按 A182：回显的是 00 全文与防错清单两段全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 52441 | 507 | `210dd321fe63e8d03494b58952ed871433f92ca8765a5a7e0b2db3f62d3383aa` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/70-round-070-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/71-round-071-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/records/ax-feature-pool.md` | 6721 | 89 | `c090c440f6fb05e5feeac6381f798d851cc1fd0b8a9c47506858cbae22713c99` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/065-settings-export-import-cleanup.md` | 8491 | 92 | `781807ad56ba77631b04a12383143fb2e08d2213ebbc268befa988bbfab3b027` |
| `docs/decisions/066-download-history.md` | 8596 | 91 | `01ae50a0f2592aa9a6d7973c9acdeb4a9f75a8abf9967fa8219f7c189e32ba80` |
| `docs/decisions/069-download-sources.md` | 9176 | 100 | `12fce84263839c5ea90370a0afdc50d4088168d702501607080be1673a47fdbd` |
| `docs/decisions/070-instance-drop.md` | 10980 | 106 | `b2adbced220df6df88ef9dc921a76a10097c171a7b71c505d8709fb9b113511b` |
| `src/core/ax.rs` | 4493 | 100 | `7824da1de27def973294ac91ec65de4dafeb95e98be164eec4b4bd30fd2dc3f5` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 17795 | 548 | `f4ef7cafa51bc000a8279515a44b9f0e0aac9c5d850db110044be42f18f2c492` |
| `src/core/mod.rs` | 554 | 32 | `6f8e30e4ef4fdf54cf715fb91b69e4561e881b8121c6db9a8040054dd5ad18fa` |
| `scripts/ax_guard.py` | 1915 | 49 | `f934653236871aea9c4bc40d76faba1abc72a3338625d8994df4d79870a75b92` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `71-round-071-instructions.txt:1` | `干`（3 字节，SHA-256 `9ee0280b…`） |
| `70-round-070-instructions.txt:1` | `干`（3 字节） |
| 070 回复「唯一下一步」 | 继续发「干」按功能池落下一项（剩 18 项 `Planned`）；或回 Q-070-01 / Q-067 / EQ 任一条拍板后按拍板值落地 |
| `ax-feature-pool.md` 070 补记 | `Planned 18` / `DataLayer 5`（AX05、AX06、AX11、AX12、AX24）/ `GateOnly 1`（AX23） |
| `31-axolotl-launcher-features.md:55` | AX17 旗帜设计器：图案分层、染料替换、撤销重做、最近编辑记录；旗帜设计 JSON / 物品数据 / give 命令导入导出，兼容现代与旧版语法；来源 v1.11.0 Release / 官方一手；口径零新增第三方、许可证合规、UI 框架卡 EQ-01 |
| `11-features-input.txt:240` | `32.支持我的世界颜色代码一键复制（包括旧的格式与新json格式）` |
| `00-requirements.txt:26` | 严格进行调研，直到信息已经达到完全无法失误的情况下再操作 |
| `00-requirements.txt:33` | 每次交付带 HTML 一比一运行逻辑、自我批判、时间戳回显、四值判决、独立验证证据 |
| `00-requirements.txt:54` | 不做过度抽象、不套设计模式、不偷偷加依赖 |
| `00-requirements.txt:110` | 必须处理空值、空集合、越界、超时、编码 |
| `00-requirements.txt:111` | 禁止顺手改无关文件，差异不超出任务范围 |
| `00-requirements.txt:114` | 跨进程消息走统一信封 |
| `00-requirements.txt:137` | 每次开动前确认文件接口最后一层 |
| `00-requirements.txt:156` | 连续两轮未达通过，停下来向用户报告卡点，由用户决定是否调整范围 |
| `00-requirements.txt:166` | 每个状态只声明实际达到的那一层 |
| `00-requirements.txt:175` | 同类功能尽量复用同一个模块 |
| `00-requirements.txt:230` | 每轮联网核实现有时间与上游版本状态（第 15 节调研待办，标注不阻塞当前轮） |
| `00-requirements.txt:245` | 有任何未解决的「已失败 / 未证实 / 受阻」，不发通过标记 |
| `00-requirements.txt:248` | 用户当轮明确指令 > 本文件规则 |
| `00-requirements.txt:249` | 安全与许可证合规 > 功能进度 |
| `00-requirements.txt:33` / `:209-222` | 12 项输出结构 |
| `ai-errors.md:415` | A208 只回「干」且列需 EQ 拍板的层时先复核台账与摊平可拍环境 |
| `ai-errors.md:423` | A211 已决断、不依赖 EQ 的条目要真读全文找，连续多轮只写状态复核轮等于没推进 |
| `ai-errors.md:331` | A164 原始需求逐条分「已决断 / 未决断」，未决断不代拍板、不长期以未启动挂账不回显 |
| `ai-errors.md:354` | A177 用户没拍板选项时按默认执行要登记 D 编号 |
| `ai-errors.md:405` | A203 授权成立也要逐值回显具体默认 |
| `ai-errors.md:449` | A217 只接数据层，不把「已登记」写成「已实现」 |
| `ai-errors.md:483` | A246 新增内部数据层不扩 `api::v1` |
| `ai-errors.md:486` | A248 不得把自造约束写成用户当轮指令 |
| `ai-errors.md:487` | A249 新 spec 落盘即触发本轮四件套 |
| `ai-errors.md:488` | A250 原文含 OR 两条路径时只落一条，另一条登记待拍板 Q |
| `ai-errors.md:490` | A252 分段求和必须注明口径 |
| `ai-errors.md:493` | A254 网关 502 留 `.git/index.lock`，提交前先核 |
| `ai-errors.md:495` | A255 `Vec::new()` 在 push 前被读触发 E0282 |
| `ai-errors.md:496` | A256 `LOADED_MODULES` 真实结尾还有 `dispatcher.launcher` |
| `ai-errors.md:498` | A258 守卫禁用表不写凭据前缀连续串 |
| `ai-errors.md:501` | A259 二手调研的 NN-MM 是条目编号还是行号要分开核 |
| `ai-errors.md:502` | A260 纯函数用守卫解析函数体核不含 `fs::` |
| `ai-errors.md:503` | A261 守卫核函数调用要带真实参数名 |
| `ai-errors.md:505` | A262 功能轮守卫不写死上一轮状态计数 |
| `ai-errors.md:507` | A263 注入夹具锚点必须唯一，守卫逐行扫描函数体 |

## A259 复核：AX17 调研锚点的编号与行号

`31-axolotl-launcher-features.md:55` 写「11-32 只有颜色代码一键复制」。与 070 的 `11-15` 不同，这里的 `11-32` 是**原文条目编号**：`11-features-input.txt:240` 逐字为 `32.支持我的世界颜色代码一键复制（包括旧的格式与新json格式）`，成立。本轮引用一律带文件行号（`:55` / `:240`），不把条目编号当行号用（A259 / A200）。原文该条含「旧的格式与新json格式」两条路径，按 A250 只落数据层、不写死任一格式字段，另一路径登记 Q-071-02。

## A208 复核（本轮开工前）

用户只发「干」，未点 AX 编号、未回 Q-070-01 / Q-067-01 ~ 03 / EQ。按 A202 核 `070-instance-drop.md` 与 `ax-feature-pool.md` 070 补记：070 结尾给出两个分支，主分支「按功能池落下一项」，替代分支「回 Q / EQ 拍板」；**未列「需 EQ 拍板才能动」的阻塞层**。摊平可拍环境见 `b-class-status-recheck.md:61`，EQ-01 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、UI 渲染闸门、密钥与新增第三方。Q-067-01 ~ Q-067-03 / Q-070-01 属并行待拍板，不阻塞本轮，登记不变。

## `00:9.1` 连续未达通过的冲突裁决（D-071-1）

069 / 070 连续两轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 071 当轮明确指令是 `干`（3 字节，逐字副本已核，A248），按 `00:248`「用户当轮明确指令 > 本文件规则」覆盖。处置：**不中断推进，但卡点在本轮回复与决策里逐条回显**（A164 禁止长期挂账不回显）。根因固定为三项：E213 / E214 / E233 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；18 项 `Planned` 与 UI 闸门未启动。发通过标记的前置条件是用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化（AX23 GateOnly、AX18 AI 提供商配置页排除） |
| 068 / 069 / 070 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层与编排 |
| `00:171` / `00:172` 密钥不写死、默认镜像 | 已决断，069 已落地 |
| `12:36` 拖拽安装 / `12:47` 实例分组 | 已决断，070 已落地数据层 |
| `11:240` 颜色代码一键复制（旧格式 + 新 json 格式） | 已决断有此功能；**两种格式的具体字段结构未取得一手原文，未决断**，不写死 |
| AX17 图案 / 染料 id 表来源 | **未决断**，登记 Q-071-01 |
| AX17 新旧 give 语法兼容 | **未决断**，登记 Q-071-02 |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067-01 ~ 03、Q-070-01 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / D-071-2）

真读 18 项 `Planned` 全文（见 `docs/research/31-axolotl-launcher-features.md:24–67`）与 065 / 066 / 069 / 070 的排除清单后选 **AX17 banner_designer** 的**数据层**，登记为**我的默认 D-071-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX01 / AX10 / AX13 / AX14 / AX15 / AX20 | 重 UI，卡 EQ-01，不动 |
| AX02 / AX07 / AX21 / AX22 | 真实网络 IO / 境外限制 / 第三方端点，不动 |
| AX03 / AX19 / AX20 | NBT / `.litematic` / `.schem` 解析库，零新增第三方约束下不动 |
| AX04 / AX09 | EQ-13 / 036 边界，不动 |
| AX08 | zip 解析库，066 已排除 |
| AX16 / AX18 | 063 登记的 6 项低可信度转述之一；A30 不写死未取得一手原文的字段 |
| **AX17 收窄后** | 来源 v1.11.0 Release / 官方一手；**不写死任何 Minecraft 染料 / 图案 / 格式码**（全当不透明 id 字符串，只做输入边界校验，A30）；只落图案分层 + 有界撤销重做栈 + 最近编辑记录的数据层与编排；零新增第三方；不碰 EQ / 网络 / UI / 密钥 |

065 决策曾把 AX17 列入「重 UI 卡 EQ-01」排除表。按 070 对 AX24 的处置口径：那是相对 AX11 的排序理由，不是永久封禁；本轮收窄为不碰 UI 渲染后落地，由 D-071-3 覆盖，065 历史行不重写（A201 / A164）。

不做的（登记 Q / 未启动）：染料与图案 id 表来源（Q-071-01）；旗帜设计 JSON / 物品数据 / give 命令导入导出与现代 / 旧版语法兼容（Q-071-02，A250 两条路径只落数据层、不代定优先级）；画布渲染、拖拽交互、真实导入导出、NBT 解析均未启动。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod banner_design;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.banner_design`，锚点用真实结尾 `"core.instance_drop",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX17 `Planned` → `DataLayer`；24 条唯一不变；断言 `DataLayer 6` / `Planned 17` |
| `scripts/ax_guard.py` | 显式断言扩到 AX05 / AX06 / AX11 / AX12 / AX17 / AX24；动态求和不变（A240） |
| `scripts/banner_design_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 20 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `71-round-071-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 507 行完整读 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX17 数据层已实现 / 已验证；UI、give 语法、真实导入导出未启动 |
| `00:54` / `00:111` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / UX / 语言包 / PNG |
| `00:114` | 编辑事件走统一 `Envelope` |
| `00:110` | 8 类坏输入回默认、空集合 / 越界 / 栈饱和 / 控制字符 / 无 root 全处理 |
| `00:175` | 撤销重做栈与路径、集合语义不同，新模块；公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES`，不复制第二份 |
| `00:26` / A30 | 不写死染料 / 图案 / 格式码 / give 语法；所有外部值由调用方传入，只校验长度与控制字符 |
| `00:230` | 联网核实属第 15 节调研待办，标注「不阻塞当前轮」；本轮选中的项无外部事实依赖，未执行联网，登记不隐瞒 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构 |
| A258 / A262 / A263 | 新守卫不写凭据前缀连续串、不写死状态计数、注入夹具锚点唯一 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-071-3 ~ D-071-11，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-071-3 | 收窄范围 | 065「AX17 重 UI 卡 EQ-01」改判为「不碰 UI 渲染，只落分层 / 撤销重做 / 最近编辑的数据层」 |
| D-071-4 | 图案与染料 | 均为不透明 id 字符串；只校验非空、长度 ≤ `robust::MAX_ID_BYTES`、无控制字符；**不内置 16 色 / 图案常量表** |
| D-071-5 | 分层上限 | 32（项目自定义容量上限，不宣称 Minecraft 上限）；显式类型 `Vec<Layer>`（A255） |
| D-071-6 | 撤销 / 重做栈 | 会话内内存态，各上限 64；`apply` 推当前态入 undo 并清空 redo；undo / redo 越界返回 `false` 不改状态 |
| D-071-7 | 最近编辑记录 | 设计 id 列表，上限 32，去重饱和（同 id 移到末尾，不新增） |
| D-071-8 | 持久化 | `banner-design.json` schema 1，只写 `schema` / `layers` / `recent` 三键；撤销重做栈不落盘；`reset` 不删文件并复用 065 四文件保护 |
| D-071-9 | 严格白名单 | 顶层 `KNOWN_KEYS` 3 键唯一，未知键整份拒并给 DEGRADE 行（A189） |
| D-071-10 | 真实导出边界 | 不生成 give 命令、不解析物品 NBT、不输出 § 格式码、不发网络、不写密钥（A30 / `00:249`） |
| D-071-11 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |

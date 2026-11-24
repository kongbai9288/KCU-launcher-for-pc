# 090 开工逐字复读记录

开工 `Tue Nov 24 12:08:21 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节完整读、分两段回显（1–260 / 261–520），末条仍为 A271。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮逐行全文回显（A211 真读全文；A244 要求真读原文与防错清单全文并记行数）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。本表哈希记录于 090 四件套写毕、台账补记写毕之前的读时刻；台账与 index 补记后的字节 / 哈希以交付快照为准。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295 |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88 |
| `docs/spec/90-round-090-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/89-round-089-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a |
| `docs/decisions/088-instance-import-delivery.md` | 16416 | 114 | `1c5919fa73e3f92a5c34f99bcd36220843e8f37c235f41e16e17e4449ddddfc7 |
| `docs/decisions/089-delivery-closure.md` | 15506 | 109 | `9fe2e642f008c663036e91769967857637db741976236bbf20a2567944db9d7d |
| `docs/decisions/090-projection-workshop.md` | 本轮生成 | — | — |
| `docs/records/round-089-full-readback.md` | 18284 | 157 | `3fa9b109a1978a99cac408024059736e89a734a79b7b52edae87a3d3dddd08a8 |
| `docs/records/round-090-full-readback.md` | 本轮生成 | — | — |
| `docs/verification/round-089.md` | 11212 | 94 | `e4a9c1ffcfd23603092d6950501788c320ff3d5c5b0daf20cc1d44bbecba2558 |
| `docs/verification/round-090.md` | 本轮生成 | — | — |
| `demos/round-089-delivery.html` | 14965 | 68 | `d57fe444692a89105225ff4d1522775783927ce33ebf979a57c5debaa82f0d94 |
| `demos/round-090-projection.html` | 本轮生成 | — | — |
| `src/core/projection.rs` | 36047 | 994 | `9c2334b374d9808a05f81bb9967785b44d52d7b0e10974949ded208ce3464840 |
| `scripts/projection_guard.py` | 13812 | 300 | `b1e71b378d143405d2b9dc3d9efbb64e01ce3d6fe282c6e755874944eedeb835 |
| `scripts/instance_import_guard.py` | 13815 | 291 | `33a9d0c2b97061892d6630d01a3457be6445111c3e04d54c7f7d21a976a37755 |
| `src/core/ax.rs` | 4643 | 100 | `48d81f5a79aa07f04bc6e6cda6b65cb2c1771f275e2537411469f26bf7286ead |
| `src/core/boot.rs` | 18171 | 563 | `4832f5d758038810a5efa5dbb91491f6b9208bfdd4132b7e47e597a619d87603 |
| `src/core/mod.rs` | 885 | 47 | `c17f62eb7b33e9fe70333e837551c13d8b1e36a96c70c005b97cbb8c2cb2807e |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0 |
| `scripts/ax_guard.py` | 2035 | 49 | `8b916cc452b3fbd7528a7dba196674fd0a585a36d1ea7e77fbcc13686f4342e1 |
| `.github/workflows/ci.yml` | 5054 | 141 | `23c2bb2ae77b28bc45bbfc2259a074f2de6ff705d956b2d2476c20b2d7e51a08 |
| `Cargo.toml` | 916 | 37 | `47346e19c7e0946a55400c83a76e38c94b1d9fa0b90c9b63bac1717316080067 |
| `Cargo.lock` | 3520 | 174 | `bd20d10a30d51c8488fede122dca5ff9224313ca7abb794f66673689daf04044 |
| `THIRD-PARTY-NOTICES.md` | 22344 | 309 | `ac0941e2e2b5300791e036113e31e775c43399da9437460e565329af609babbf |
| `docs/records/rounds.md` | 355684 | 3388 | `0c14428c35631fd6bd88af4bdc66e9793f18fe1358ad652991b0456dad0c761b |
| `docs/records/ax-feature-pool.md` | 32023 | 239 | `7bf0541c2c264589bd170204319cca5599e6f841512707ac02e97cf73fd0d9e8 |
| `docs/index.md` | 50374 | 636 | `ba55cc18525fc91d59b7d5c7f4bdf400a41e5efcf53f4648dd1a259dc23171f1 |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `90-round-090-instructions.txt:1` | 逐字 3 字节 `干`（SHA-256 `9ee0280b…`，无换行），与 89 / 88 / 87 / 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号 spec 同形态 |
| `89-round-089-instructions.txt:1` | 逐字 3 字节 `干`，089 轮已落盘 |
| `72-round-072-instructions.txt:1` | 117 字节工具澄清句，已在 072 处理并撤回 071 归因（E251） |
| `11:250` | 第 41 条：支持投影预览（两个投影模组的文件都支持） |
| `11:244` | 第 36 条：不要一次性把页面都堆在一起，按照顺序去排列，都在一个弹窗中，上面有页码，每一个都是单独的选择 |
| `11:147` / `11:150` | 图片预览 / 预览窗格 |
| `11:23` / `11:24` | 一定分辨率内自动适配页面；区间范围用滑动条（直接一条线） |
| `11:10` | 每一个弹窗都需要有关闭逻辑 |
| `12:35` / `12:36` | 整合包导入导出（mrpack / CurseForge zip）/ 拖拽安装模组 / 插件（088 已落 AX08） |
| `00:133` / `00:34` / `00:260` | 逐字保存、每轮开工完整读 00 与防错清单——本轮执行 |
| `00:137` / `00:245` / `00:248` | 接口终点、通过标记条件、用户当轮明确指令优先——本轮显式核一遍 |
| `00:230` | 每轮联网核实现有时间与上游版本状态——本轮执行远端 ref 与时间核实 |
| `00:9.1` / `00:9.2` / `00:207` | 连续未达通过、测试锁定、文档不凑条目 |
| `ai-errors.md:59` | A50 mrpack 导入不做路径穿越校验 |
| `ai-errors.md:332` | A165 路径校验用标准库 `Component` 逐分量判定 |
| `ai-errors.md:465` | A230 用户说「全部（不与冲突的情况下）」时，逐条核冲突并写进台账，排除子项留痕 |
| `ai-errors.md:476` | A240 改功能池状态后守卫写死 `planned=N` 会误报，改动态求和 |
| `ai-errors.md:487` | A249 一轮落地代码、下一轮才补交付时按新落盘 spec 同时要求两套四件套 |
| `ai-errors.md:512` | A266 平台拼入用户位次的文本不得当成用户当轮指令 |
| `ai-errors.md:513` | A267 改功能池状态前先读真实 `name` slug |
| `ai-errors.md:514` | A268 G2 四份原文与 G3 的 `## 9` / `## 10` 锚点一次排对 |
| `ai-errors.md:271` | A271 新增测试标识符前先核全仓既有守卫禁用字面量表 |
| `docs/decisions/089-delivery-closure.md:12` | 089 唯一下一步写「090 按功能池落下一项」，本轮按 A202 打开核过 |

## A248 / A266 预检

90 号 spec 逐字副本全文 3 字节 `干`，已落盘。按 A248 开轮核 90 / 89 / 88 / 87 / 86 / 85 / 84 / 83 / 82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本：90 / 89 / 88 / 87 / 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号均仅 3 字节 `干`，82 号 159 字节完整句，72 号 117 字节澄清句已在 072 处理。按 A266，平台拼入用户位次的文本不作用户当轮指令、不据此写「未遵守 / 偏离 / 下一步按该行决定」、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080–089 已按同一口径补记，历史回复与历史文件不重写（A181 / A201）。副本里没有的文字不写成用户指令。工具从未禁用，本轮正常调用工具完成验证、提交、推送与打包。

## A145 远端补验

只读 `GET /git/ref/heads/main` 得 `a5b4547b118099988bc90b2c7452d7dfea5e097b`（089 补记，parent `b08c268`），完整 recursive tree `LOCAL 1272 / REMOTE 1272 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`。本地 HEAD `15bf698`（089 补记）、TRACKED 1272、DIRTY 0、无 `.git/index.lock`、无运行中 git 进程、PYC 0；两个 zip 为 089 轮包（主包 1272 项、`ui-previews.zip` 57 项）。

## A230 逐条核冲突（089 唯一下一步点名动作）

按 A230 打开 `docs/research/31-axolotl-launcher-features.md` 全文与 `docs/records/ax-feature-pool.md` 逐条核 4 项 `Planned`：

| 编号 | 真实 slug / conflict | 冲突核验 | 处置 |
| --- | --- | --- | --- |
| AX07 | `doh_support` / `network_io_not_started` | `31-axolotl-launcher-features.md:35` 写「未提。11-13 手动选镜像、11-29 `§` 模板、12-60 下载源测速与镜像切换，均无 DoH。口径：真实网络 IO 未启动、Win7 TLS 前置（EQ-03）」；真读 00 / 11 / 12 号全文，`11:220` / `11:236` / `12:60` 无 DoH 锚点 | **排除留痕**：技术受阻非需求冲突，conflict 保持 `network_io_not_started`，状态保持 `Planned`，EQ-03 不代拍，由 `projection_guard.py` 显式断言 |
| AX15 | `studio_image_editor` / 空 | `31-axolotl-launcher-features.md:43` 写「未提」；075 E276 登记「撤销重做栈与 `src/core/banner_design.rs:241-263` 的 `push_layer` / `undo` / `redo` / `MAX_HISTORY` 同构」；077–089 十一次相对排序理由均排除留痕 | **排除留痕**：状态保持 `Planned`，不悄悄丢掉；UI 框架 EQ-01 未拍，不代拍 |
| AX20 | `projection_workshop` / 空 | `11:250` 第 41 条「支持投影预览（两个投影模组的文件都支持）」是原文已决断、不依赖 EQ 的锚点；`31-axolotl-launcher-features.md:57` 写「部分。11-41 只有预览」；077–089 把 AX20 归「依赖 NBT 或投影解析库」是只核调研描述、未逐行回显 11 号原文时写下的相对排序理由，按 073 / 075 / 077 / 078 / 079 / 080 / 081 / 082 八次收窄先例处理 | **落地**：收窄为两个格式槽位 + 顺序单条预览决策的数据层，不引第三方解析库、不写死投影模组名 / `.litematic` / `.schem` / NBT schema、不碰 UI 渲染、不碰网络端点；状态 `Planned → DataLayer` |
| AX22 | `shimu_account` / 空 | `31-axolotl-launcher-features.md:61` 写「未提。浏览器授权、连接检查、断开关联」；真实网络 IO + 第三方端点 + 境外限制（`11:7` / 054）+ `11:18` API 不共有 | **排除留痕**：状态保持 `Planned`，endpoint 不写死，登记 Q-090-01 |

历史行不重写（A181 / A201），本补记覆盖 077–089 对 AX20 的相对排序判定。AX07 的 `network_io_not_started` 与 AX23 的 `gate_only_no_ui` 都保持原样，不因本轮落地而清 conflict。

## A208 / A202 复核

按 A202 打开 `docs/decisions/089-delivery-closure.md:12` 核尾部：089 写出「090 按功能池落下一项（剩 4 项 `Planned`：AX07 / AX15 / AX20 / AX22）……AX07 的 `network_io_not_started` 按 A230 逐条核冲突；若回任一 Q / EQ 则改走拍板闭环」。按 A208 复核 `b-class-status-recheck.md:85`：EQ-01 ~ EQ-13 仍待拍、未启用，B04 卡 EQ-01 但本轮不动 UI 渲染层（A100），收窄后不依赖 EQ；无「需 EQ 拍板才能动」阻塞层，可开工。按 A267 读 `src/core/ax.rs:20–43` 真实表：AX20 `name` 为 `projection_workshop`、`conflict` 空、`ui: true`，`ax.rs` 断言 `Planned 4` / `DataLayer 19` / `GateOnly 1`；本轮改 AX20 后为 `Planned 3` / `DataLayer 20` / `GateOnly 1`。按 A217 核 `src/core/` 无 `projection*` 占位模块，新模块为 `projection.rs`。

## A211 真读全文与 AX20 收窄锚点

本轮真读 00 / 防错 / 11 / 12 号全文，不是只核哈希与台账状态。AX20 收窄锚点逐字复核：`11:250` 两个投影模组的文件都支持（两个格式槽位 `primary` / `secondary` 都登记，不二选一，A250）、`11:244` 顺序排列 / 一个弹窗 / 页码 / 每个单独选择（`current` 游标 + `resolve_current` 单步推进，禁批量）、`11:147` / `11:150` 图片预览 / 预览窗格（三档视图 `fit` / `original` / `scaled`）、`11:23` / `11:24` 分辨率适配 / 区间滑动条（`MIN_SCALE` / `MAX_SCALE` / `DEFAULT_SCALE` 连续区间，非固定圆点）、`11:10` 弹窗关闭逻辑（`PreviewState::Closed` 必须 `decided`）、`12:35` / `12:36` 路径边界（A50 / A165 `Component` 逐分量）。A154 显式 code 枚举、A269 / A270 常量表 EXPECTED 逐值 + impl 段字面量比对、A260 纯查询段解析函数体无 `fs::`、E330 事件载荷十键不含用户文本，均由 `projection_guard.py` 持有。

## A244 合规复核

| 用户口径 | 原文锚点 | 本轮可核对证据 | 结论 |
| --- | --- | --- | --- |
| 用开源的 | `00:32` / `00:19` / `11:2` / `11:11` | `Cargo.lock` `[[package]]` 26 项、`vendor/` 25 个第三方目录、`docs/licenses/` 58 份 LICENSE 全文、`THIRD-PARTY-NOTICES.md` 309 行、`code-ownership-audit.md` 逐轮登记；085–090 零新增第三方 | 已证实 |
| 保证许可证 | `00:249` / `00:133` / `11:26` / `11:4` / `11:258` / A44 / A45 / A100 / A139 / A141 | 090 复用既有 `serde_json` / `anyhow` / `robust` / `Envelope` / `diag_line` / `settings_io::PROTECTED_FILES`，不引新 crate；58 份 LICENSE 与 309 行声明未变 | 已证实 |
| 停下来问，不硬上 | `00:249` | 085–090 零新增第三方；AX07 / AX22 的真实网络前置按 A230 排除留痕，不硬上 | 已证实 |
| 源与产物对比 | `11:26` / A45 | 090 新增文件为项目自写数据层，非拼接上游源码；真实字节比对执行层未启动 | 已证实（零拼接）+ 未启动 |

## `00:230` 本轮联网核实

| 项 | 一手结果 |
| --- | --- |
| 当前时间 | `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` → `Tue Nov 24 12:08:21 CST 2026` |
| 远端 ref | `GET /git/ref/heads/main` RC=200 → `a5b4547b118099988bc90b2c7452d7dfea5e097b` / parent `b08c268` / message `round 089 addendum: remote sync 1272 files ALL_MATCH` |
| 完整 tree | `1272 / 1272 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 上游版本状态 | 082 已核 `ViaVersion/ViaNBT`：`pushed_at=2026-10-27T14:24:29Z`、`default_branch=master`、`archived=false`、tags `3.0.0` / `2.1.3` / `2.1.2`；085–090 无新增上游依赖，复核状态不变 |

## `00:9.1` 连续未达通过的处置（D-090-1）

069–089 连续**二十一**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 090 当轮明确指令「干」按 `00:248` 覆盖。不中断推进，但卡点在本轮回复、决策、四值里逐条回显（A164）：E213–E366 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；3 项 `Planned` 与真实执行层 / UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不改测试、不降验收项。

## `00:137` 接口终点核对（A244 要求显式核）

| 引用点 | 090 形态 |
| --- | --- |
| `src/core/projection.rs` | 本轮新增 993 行 / 32 单测；五张白名单表、三枚举显式 code、`Component` 路径校验、五条矛盾态规则九处调用、单条突变十入口、原子写、统一信封十值载荷 |
| `src/core/ax.rs` / `boot.rs` / `mod.rs` | AX20 `DataLayer`；`LOADED_MODULES` 在 `core.instance_import` 之后、`dispatcher.launcher` 之前插 `core.projection`（A256）；`pub mod projection;` |
| `src/api.rs` | 零改动，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `scripts/projection_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job；38 组双向注入全真 FAIL |
| `scripts/instance_import_guard.py` / `scripts/ax_guard.py` | 088 守卫写死状态计数按 A240 / A262 改动态持有（E366）；`ax_guard.py` 显式断言表加 `'AX20'` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff，26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| UX HTML / 两语言包 / 56 PNG | 零 diff；AX20 `ui: true` 但 UI 渲染层未启动（A100），守卫核三处不含 `projection-preview.json` |
| 090 新增 | 90 号 spec、`round-090-full-readback.md` / `090-projection-workshop.md` / `round-090.md` / `demos/round-090-projection.html`；台账补记与 `docs/index.md` 必读清单 |

## `00:245` 通过标记条件显式核（A244 要求显式核）

| 条件 | 本轮判定 |
| --- | --- |
| ① 8.1 独立验证结论为「通过」 | 不满足：独立验证「部分通过」，存在已失败 / 未证实 / 未启动 |
| ② 所有结论均为「已证实」 | 不满足：E213–E366 已失败；EQ / Q / 3 项 `Planned` 未证实；真实执行层与 UI 渲染未启动 |
| ③ 自评 ≥ 7 | 满足（7） |
| 结论 | `00:245` 第 2 条 + 第 18 节第 2 优先级：**不发通过标记**，明确写「未通过」及原因（A206） |

## 合规核对表

| 约束 | 090 行为 |
| --- | --- |
| `00:133` 逐字保存 | 90 号 spec 3 字节落盘；89 / 88 / 87 号 spec 已在对应轮次落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显、防错清单 520 行完整读、11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 20 份 spec 逐字副本；平台文本按 A266 不作指令、不进副本；不重提工具禁用归因 |
| A145 / A216 | 远端 `a5b4547` / `1272 / 1272 ALL_MATCH True` 补验；推送用 `base_tree` 增量、`force=false` |
| A230 | 4 项 `Planned` 逐条核冲突，排除子项留痕，AX07 conflict 不清 |
| A140 / A254 | 提交前核无锁、无运行中 git 进程 |
| A249 / A268 | 不删 90 号 spec 规避守卫；补齐 090 四件套；G2 四份原文列入哈希表、G3 `## 9` / `## 10` 锚点一次排对 |
| A159 / A204 / A243 | 38 组双向注入全真 FAIL、0 假 OK、恢复 OK、哈希复原；E366 修复点单独双向验证 |
| A245 / `00:9.2` / A264 | 首跑 1 个 FAILED 保留回显，改夹具（跨槽位单 setter 被一致性拒绝），实现零改动、断言强度不降 |
| A116 / A258 / A205 | CI 三 job 按真实命令实跑；`scripts/__pycache__/` 保持 0 项；两个 zip 按 tracked 清单重打 |
| A252 / A265 | 全量 790 / 0 注明分段求和口径；090 演示五数组 16 项对齐 |
| A267 | 改功能池状态前先读真实 slug；本轮读 `ax.rs:20–43` 后改 AX20 |
| A271 | 新测试标识符先核全仓守卫禁用字面量表，避开 `api_guard.py` 的 `catalog()` 等 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` / `00:207` | 设计说明只走对话不进仓库；E366 属 A240 / A262 已覆盖，防错清单零改动，不凑条目 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-090-*，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-090-1 | 连续二十一轮未通过 | 按 `00:248` 用户当轮「干」覆盖，不中断但逐条回显卡点 |
| D-090-2 | 本轮性质 | **功能轮**：按 A230 逐条核 4 项冲突后落 AX20 `projection_workshop` 数据层；`src/` 只落数据层，UI 渲染不启动 |
| D-090-3 | 功能池 | AX20 `Planned → DataLayer`；AX07 / AX15 / AX22 保持 `Planned`；`Planned 3` / `DataLayer 20` / `GateOnly 1`；AX07 conflict 保持 |
| D-090-4 | 收窄口径 | 两个格式槽位 `primary` / `secondary` 都登记（A250）；不写死投影模组名、`.litematic` / `.schem` / NBT schema、不引第三方、不碰 UI 渲染、不碰网络端点；登记 Q-090-01（AX22 第三方账号关联端点 / 授权形态）与 Q-090-02（两个投影模组具体归属） |
| D-090-5 | 守卫缺口 | 088 守卫写死 `planned=4 data=19` 按 A240 / A262 改动态持有（E366）；新守卫 38 组双向注入；`ax_guard.py` 显式表加 `'AX20'` |
| D-090-6 | 提交范围 | 090 代码 / 守卫 / 五处接线 + 四件套 + 台账一次提交；A11 逐项核 diff 范围 |
| D-090-7 | 推送 | `scripts/api_push.py` 以 `base_tree` 增量 POST，`force=false`；推送后逐项 ALL_MATCH 写进 `rounds.md` 090 补记 |
| D-090-8 | 构建产物与 zip | `scripts/__pycache__/` 保持 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1`；主 zip 按 `git ls-files -z \| zip -@`、`ui-previews.zip` 按 PNG 清单重打 |
| D-090-9 | Q / EQ | 不代拍；Q-090-01 / Q-090-02 与历史 26 组 Q、EQ-01 ~ EQ-13、4 条 Q-C 保持未证实 |
| D-090-10 | 状态分层与通过标记 | AX20 数据层已实现 / 已验证；真实投影文件解析、预览渲染、Studio 打开入口、资源站安装未启动；不发通过标记 |

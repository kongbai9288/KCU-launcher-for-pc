# 091 开工逐字复读记录

开工 `Tue Nov 24 12:58:12 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节完整读、分两段回显（1–260 / 261–520），末条仍为 A271。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮逐行全文回显（A211 真读全文；A244 要求真读原文与防错清单全文并记行数）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。本表哈希记录于 091 四件套写毕、台账补记写毕之前的读时刻；台账与 index 补记后的字节 / 哈希以交付快照为准。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295 |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88 |
| `docs/spec/91-round-091-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/90-round-090-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a |
| `docs/decisions/090-projection-workshop.md` | 15999 | 113 | `3f732f0e05984d94a8536e21c69533ac10f0d3acd3fb502a3643664327924a02 |
| `docs/decisions/091-studio-image.md` | 本轮生成 | — | — |
| `docs/records/round-090-full-readback.md` | 20351 | 175 | `2fe5b6dee994134c5c1a280341ab6c2a430bc7eff373cad0e62d98faf6753bbc |
| `docs/records/round-091-full-readback.md` | 本轮生成 | — | — |
| `docs/verification/round-090.md` | 12767 | 102 | `6be3cdd26d77407651f8fb8b93c89922975d6651b622c1e943031ab13c2a0223 |
| `docs/verification/round-091.md` | 本轮生成 | — | — |
| `demos/round-090-projection.html` | 15561 | 68 | `a09acbe27426a057e8b412674a401e7fa38ab77296d59f37d436b17c05879390 |
| `demos/round-091-studio-image.html` | 本轮生成 | — | — |
| `src/core/studio_image.rs` | 30634 | 881 | `0d8755e38c717a0f9f82100b4452f2eda2a7d2d78b5cb57b9a17e48969e8ccfe |
| `scripts/studio_image_guard.py` | 12323 | 272 | `9f7f815bf91bfd92acaca1df1463111794f8e7a848244bb0c0c12bbb0c6b67bc |
| `scripts/projection_guard.py` | 13817 | 300 | `8fe8455bde434cbe9ae10ee03ef4a756526214684602d0447da6f29444d8754f |
| `src/core/ax.rs` | 4653 | 100 | `7860056846f52a92c587658fbc6a9f1e90cea917a1429b3143c2158d7110ee17 |
| `src/core/boot.rs` | 18196 | 564 | `8e07c75b4f4d83ebe5702fcc18c992819567cb45042b8f034cca3e2e11637270 |
| `src/core/mod.rs` | 907 | 48 | `cf605284775d58713c937670ec47508c5c81c88b3265c446acfe1fbbed041b76 |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0 |
| `scripts/ax_guard.py` | 2043 | 49 | `06978f871b429aa4c53f87f7c38aa32c6d8a224849d3e90d5e7584915606c2d5 |
| `.github/workflows/ci.yml` | 5138 | 143 | `96fa612d9367cce77a1423be1f542bb11e449363f8c37357759579f383abd1d6 |
| `Cargo.toml` | 916 | 37 | `47346e19c7e0946a55400c83a76e38c94b1d9fa0b90c9b63bac1717316080067 |
| `Cargo.lock` | 3520 | 174 | `bd20d10a30d51c8488fede122dca5ff9224313ca7abb794f66673689daf04044 |
| `THIRD-PARTY-NOTICES.md` | 22344 | 309 | `ac0941e2e2b5300791e036113e31e775c43399da9437460e565329af609babbf |
| `docs/records/rounds.md` | 362240 | 3392 | `fd625ffef5150575d9e5c8504734454797835ce7963015ce5fde12164051a58f |
| `docs/records/ax-feature-pool.md` | 33142 | 243 | `c62107ddcbba84afcf650867121d4fcaa29c8f346e22b7299ed1c7898c8c4b0a |
| `docs/index.md` | 50610 | 636 | `bfe600278b63ec9e85e45c223dffb7e3579e5439d4ed391a4639829bdf4a3bd1 |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `91-round-091-instructions.txt:1` | 逐字 3 字节 `干`（SHA-256 `9ee0280b…`，无换行），与 90 / 89 / 88 / 87 / 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号 spec 同形态 |
| `90-round-090-instructions.txt:1` | 逐字 3 字节 `干`，090 轮已落盘 |
| `72-round-072-instructions.txt:1` | 117 字节工具澄清句，已在 072 处理并撤回 071 归因（E251） |
| `12:63` | 第 27 条：支持 png 快速设置服务器 logo（会自动调整像素） |
| `12:59` | 服务器图标 / MOTD 可视化编辑 |
| `11:243` | 第 35 条：对于模组图标支持所有的图片格式(png,gif,svg等等） |
| `11:147` / `11:150` | 图片预览 / 预览窗格 |
| `11:197` / `11:198` / `11:199` | 撤销操作 / 重做操作 / 操作历史 |
| `11:23` / `11:24` | 一定分辨率内自动适配页面；区间范围用滑动条（直接一条线） |
| `11:10` | 每一个弹窗都需要有关闭逻辑 |
| `11:26` | 图像部分单独仓库、许可证、源码与产物对比 |
| `11:16` | 每个页面都能扩展内容这样方便统一格式 |
| `12:35` / `12:36` | 整合包导入导出 / 拖拽安装（088 已落 AX08） |
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
| `docs/decisions/090-projection-workshop.md:12` | 090 唯一下一步写「091 按功能池落下一项」，本轮按 A202 打开核过 |

## A248 / A266 预检

91 号 spec 逐字副本全文 3 字节 `干`，已落盘。按 A248 开轮核 91 / 90 / 89 / 88 / 87 / 86 / 85 / 84 / 83 / 82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本：91 / 90 / 89 / 88 / 87 / 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号均仅 3 字节 `干`，82 号 159 字节完整句，72 号 117 字节澄清句已在 072 处理。按 A266，平台拼入用户位次的文本不作用户当轮指令、不据此写「未遵守 / 偏离 / 下一步按该行决定」、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080–090 已按同一口径补记，历史回复与历史文件不重写（A181 / A201）。副本里没有的文字不写成用户指令。工具从未禁用，本轮正常调用工具完成验证、提交、推送与打包。

## A145 远端补验

只读 `GET /git/ref/heads/main` 得 `f28d5bd11ea7a97f4ba69cd58047777ae5561591`（090 补记，parent `c7f3071`），完整 recursive tree `LOCAL 1279 / REMOTE 1279 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`。本地 HEAD `e60d6c9`（090 补记）、TRACKED 1279、DIRTY 0、无 `.git/index.lock`、无运行中 git 进程、PYC 0；两个 zip 为 090 轮包（主包 1279 项、`ui-previews.zip` 57 项）。

## A230 逐条核冲突（090 唯一下一步点名动作）

按 A230 打开 `docs/research/31-axolotl-launcher-features.md` 全文与 `docs/records/ax-feature-pool.md` 逐条核 3 项 `Planned`：

| 编号 | 真实 slug / conflict | 冲突核验 | 处置 |
| --- | --- | --- | --- |
| AX07 | `doh_support` / `network_io_not_started` | `31-axolotl-launcher-features.md:35` 写「未提。11-13 手动选镜像、11-29 `§` 模板、12-60 下载源测速与镜像切换，均无 DoH。口径：真实网络 IO 未启动、Win7 TLS 前置（EQ-03）」；真读 00 / 11 / 12 号全文，`11:220` / `11:236` / `12:60` 无 DoH 锚点 | **排除留痕**：技术受阻非需求冲突，conflict 保持 `network_io_not_started`，状态保持 `Planned`，EQ-03 不代拍，由 `studio_image_guard.py` 与 `projection_guard.py` 双守卫显式断言 |
| AX22 | `shimu_account` / 空 | `31-axolotl-launcher-features.md:65` 写「未提。浏览器授权、连接检查、断开关联」；真实网络 IO + 第三方端点 + 境外限制（`11:7` / 054）+ `11:18` API 不共有 | **排除留痕**：状态保持 `Planned`，endpoint 不写死，登记 Q-091-01 |
| AX15 | `studio_image_editor` / 空 | `31-axolotl-launcher-features.md:48` 写「未提。口径：零新增第三方、许可证合规（00-26）、UI 框架卡 EQ-01」；075 E276 写「撤销重做栈与 `src/core/banner_design.rs:241-263` 的 `push_layer` / `undo` / `redo` / `MAX_HISTORY` 同构」；077–090 把 AX15 归「同构 / 重 UI」是只核调研描述、未逐行回显 12 号原文时写下的相对排序理由；`12:63`「支持 png 快速设置服务器 logo（会自动调整像素）」是原文已决断、直接点名 png + 自动调整像素、不依赖 EQ 的锚点 | **落地**：按 073 / 075 / 077 / 078 / 079 / 080 / 081 / 082 / 090 九次收窄先例，收窄为两目标槽位 + 图片格式登记 + 像素区间的数据层；不引图像库、不持有图片字节、不碰撤销栈、不碰 UI 渲染、不碰网络端点；状态 `Planned → DataLayer` |

历史行不重写（A181 / A201），本补记覆盖 075–090 对 AX15 的相对排序判定。AX07 的 `network_io_not_started` 与 AX23 的 `gate_only_no_ui` 都保持原样，不因本轮落地而清 conflict。AX15 排除子项留痕：`11:147` / `11:150` 图片预览 / 预览窗格（090 `projection.rs` 已落三档视图，不重复，登记 Q-091-02）、`11:197` / `11:198` / `11:199` 撤销 / 重做 / 操作历史（与 `banner_design.rs` 撤销栈同构，075 E276，本轮不碰，登记 Q-091-03）、Studio 裁剪 / 绘画 / 高亮 / 形状 / 文字 / 擦除六动作（渲染层，A100）。

## A208 / A202 复核

按 A202 打开 `docs/decisions/090-projection-workshop.md:12` 核尾部：090 写出「091 按功能池落下一项（剩 3 项 `Planned`：AX07 / AX15 / AX22）……AX07 与 AX22 的网络前置按 A230 逐条核冲突；若回任一 Q / EQ 则改走拍板闭环」。按 A208 复核 `b-class-status-recheck.md:85`：EQ-01 ~ EQ-13 仍待拍、未启用，B04 卡 EQ-01 但本轮不动 UI 渲染层（A100），收窄后不依赖 EQ；无「需 EQ 拍板才能动」阻塞层，可开工。按 A267 读 `src/core/ax.rs:20–43` 真实表：AX15 `name` 为 `studio_image_editor`、`conflict` 空、`ui: true`，`ax.rs` 断言 `Planned 3` / `DataLayer 20` / `GateOnly 1`；本轮改 AX15 后为 `Planned 2` / `DataLayer 21` / `GateOnly 1`。按 A217 核 `src/core/` 无 `studio*` / `image*` / `logo*` / `pixel*` 占位模块，新模块为 `studio_image.rs`。

## A211 真读全文与 AX15 收窄锚点

本轮真读 00 / 防错 / 11 / 12 号全文，不是只核哈希与台账状态。AX15 收窄锚点逐字复核：`12:63` png 服务器 logo + 自动调整像素（两目标槽位 `logo` / `icon` 都登记，A250）、`12:59` 服务器图标可视化编辑、`11:243` 模组图标支持所有图片格式 png / gif / svg 等等（`IMAGE_FORMATS` 三点名 + `opaque` 兜底，不擅自枚举「等等」）、`11:23` / `11:24` 分辨率适配 / 区间滑动条（`MIN_PIXEL` / `MAX_PIXEL` / `DEFAULT_PIXEL` 连续区间，非固定圆点）、`11:10` 弹窗关闭逻辑（`EditState::Closed` 必须 `decided`）、`11:26` 图像单独仓库 / 许可证（不持有图片字节、不引图像库）、`11:16` 每页扩展统一格式（两槽位同构）、`12:35` / `12:36` 路径边界（A50 / A165 `Component` 逐分量）。A154 显式 code 枚举、A269 / A270 常量表 EXPECTED 逐值 + impl 段字面量比对、A260 纯查询段解析函数体无 `fs::`、E330 事件载荷十键不含用户文本，均由 `studio_image_guard.py` 持有。

## A244 合规复核

| 用户口径 | 原文锚点 | 本轮可核对证据 | 结论 |
| --- | --- | --- | --- |
| 用开源的 | `00:32` / `00:19` / `11:2` / `11:11` | `Cargo.lock` `[[package]]` 26 项、`vendor/` 25 个第三方目录、`docs/licenses/` 58 份 LICENSE 全文、`THIRD-PARTY-NOTICES.md` 309 行、`code-ownership-audit.md` 逐轮登记；085–091 零新增第三方 | 已证实 |
| 保证许可证 | `00:249` / `00:133` / `11:26` / `11:4` / `11:258` / A44 / A45 / A100 / A139 / A141 | 091 复用既有 `serde_json` / `anyhow` / `robust` / `Envelope` / `diag_line` / `settings_io::PROTECTED_FILES`，不引新 crate；58 份 LICENSE 与 309 行声明未变 | 已证实 |
| 停下来问，不硬上 | `00:249` | 085–091 零新增第三方；AX07 / AX22 的真实网络前置按 A230 排除留痕，不硬上 | 已证实 |
| 源与产物对比 | `11:26` / A45 | 091 新增文件为项目自写数据层，非拼接上游源码；真实字节比对执行层未启动 | 已证实（零拼接）+ 未启动 |

## `00:230` 本轮联网核实

| 项 | 一手结果 |
| --- | --- |
| 当前时间 | `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` → `Tue Nov 24 12:58:12 CST 2026` |
| 远端 ref | `GET /git/ref/heads/main` RC=200 → `f28d5bd11ea7a97f4ba69cd58047777ae5561591` / parent `c7f3071` / message `round 090 addendum: remote sync 1279 files ALL_MATCH` |
| 完整 tree | `1279 / 1279 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 上游版本状态 | 082 已核 `ViaVersion/ViaNBT`：`pushed_at=2026-10-27T14:24:29Z`、`default_branch=master`、`archived=false`、tags `3.0.0` / `2.1.3` / `2.1.2`；085–091 无新增上游依赖，复核状态不变 |

## `00:9.1` 连续未达通过的处置（D-091-1）

069–090 连续**二十二**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 091 当轮明确指令「干」按 `00:248` 覆盖。不中断推进，但卡点在本轮回复、决策、四值里逐条回显（A164）：E213–E371 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；2 项 `Planned` 与真实执行层 / UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不改测试、不降验收项。

## `00:137` 接口终点核对（A244 要求显式核）

| 引用点 | 091 形态 |
| --- | --- |
| `src/core/studio_image.rs` | 本轮新增 881 行 / 29 单测；五张白名单表、两枚举显式 code、`Component` 路径校验、五条矛盾态规则八处调用、单条突变八入口、原子写、统一信封十值载荷 |
| `src/core/ax.rs` / `boot.rs` / `mod.rs` | AX15 `DataLayer`；`LOADED_MODULES` 在 `core.projection` 之后、`dispatcher.launcher` 之前插 `core.studio_image`（A256）；`pub mod studio_image;` |
| `src/api.rs` | 零改动，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `scripts/studio_image_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job；41 组双向注入全真 FAIL |
| `scripts/projection_guard.py` / `scripts/ax_guard.py` | 090 守卫把 AX15 写死 `Planned`，091 同步改 `DataLayer`（E369 / A201 / A158）；`ax_guard.py` 显式断言表加 `'AX15'` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff，26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| UX HTML / 两语言包 / 56 PNG | 零 diff；AX15 `ui: true` 但 UI 渲染层未启动（A100），守卫核三处不含 `studio-image.json` |
| 091 新增 | 91 号 spec、`round-091-full-readback.md` / `091-studio-image.md` / `round-091.md` / `demos/round-091-studio-image.html`；台账补记与 `docs/index.md` 必读清单 |

## `00:245` 通过标记条件显式核（A244 要求显式核）

| 条件 | 本轮判定 |
| --- | --- |
| ① 8.1 独立验证结论为「通过」 | 不满足：独立验证「部分通过」，存在已失败 / 未证实 / 未启动 |
| ② 所有结论均为「已证实」 | 不满足：E213–E371 已失败；EQ / Q / 2 项 `Planned` 未证实；真实执行层与 UI 渲染未启动 |
| ③ 自评 ≥ 7 | 满足（7） |
| 结论 | `00:245` 第 2 条 + 第 18 节第 2 优先级：**不发通过标记**，明确写「未通过」及原因（A206） |

## 合规核对表

| 约束 | 091 行为 |
| --- | --- |
| `00:133` 逐字保存 | 91 号 spec 3 字节落盘；90 / 89 / 88 号 spec 已在对应轮次落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显、防错清单 520 行完整读、11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 21 份 spec 逐字副本；平台文本按 A266 不作指令、不进副本；不重提工具禁用归因 |
| A145 / A216 | 远端 `f28d5bd` / `1279 / 1279 ALL_MATCH True` 补验；推送用 `base_tree` 增量、`force=false` |
| A230 | 3 项 `Planned` 逐条核冲突，排除子项留痕，AX07 conflict 不清 |
| A140 / A254 | 提交前核无锁、无运行中 git 进程 |
| A249 / A268 | 不删 91 号 spec 规避守卫；补齐 091 四件套；G2 四份原文列入哈希表、G3 `## 9` / `## 10` 锚点一次排对 |
| A159 / A204 / A243 | 41 组双向注入全真 FAIL、0 假 OK、恢复 OK、哈希复原；E369 修复点单独双向验证 |
| A15 / `00:9.2` / A264 | 首跑 1 个 FAILED 保留回显，改夹具（Draft 状态下 `set_fit(false)` 合法），实现零改动、断言强度不降 |
| A116 / A258 / A205 | CI 三 job 按真实命令实跑；`scripts/__pycache__/` 保持 0 项；两个 zip 按 tracked 清单重打 |
| A252 / A265 | 全量 819 / 0 注明分段求和口径；091 演示五数组 16 项对齐 |
| A267 | 改功能池状态前先读真实 slug；本轮读 `ax.rs:20–43` 后改 AX15 |
| A271 | 新测试标识符先核全仓守卫禁用字面量表，避开 `api_guard.py` 的 `catalog()` 等 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` / `00:207` | 设计说明只走对话不进仓库；E369 / E370 / E371 均属已有规则覆盖，防错清单零改动，不凑条目 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-091-*，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-091-1 | 连续二十二轮未通过 | 按 `00:248` 用户当轮「干」覆盖，不中断但逐条回显卡点 |
| D-091-2 | 本轮性质 | **功能轮**：按 A230 逐条核 3 项冲突后落 AX15 `studio_image_editor` 数据层；`src/` 只落数据层，UI 渲染不启动 |
| D-091-3 | 功能池 | AX15 `Planned → DataLayer`；AX07 / AX22 保持 `Planned`；`Planned 2` / `DataLayer 21` / `GateOnly 1`；AX07 conflict 保持 |
| D-091-4 | 收窄口径 | 两目标槽位 `logo` / `icon` 都登记（A250）；`IMAGE_FORMATS` 只登记原文点名的 png / gif / svg + `opaque` 兜底；像素用 `16–1024` / 默认 `64` 连续区间；不引图像库、不持有图片字节、不碰撤销栈（075 E276）、不碰 UI 渲染、不碰网络端点；登记 Q-091-01（AX22 第三方账号关联端点 / 授权形态）、Q-091-02（图片预览三档视图是否复用 `projection.rs`）、Q-091-03（Studio 编辑动作栈是否复用 `banner_design.rs`） |
| D-091-5 | 守卫缺口 | 090 `projection_guard.py` 写死 AX15 `Planned` 按 A201 / A158 同步改（E369）；新守卫 41 组双向注入；`ax_guard.py` 显式表加 `'AX15'` |
| D-091-6 | 提交范围 | 091 代码 / 守卫 / 五处接线 + E369 联动 + 四件套 + 台账一次提交；A11 逐项核 diff 范围 |
| D-091-7 | 推送 | `scripts/api_push.py` 以 `base_tree` 增量 POST，`force=false`；推送后逐项 ALL_MATCH 写进 `rounds.md` 091 补记 |
| D-091-8 | 构建产物与 zip | `scripts/__pycache__/` 保持 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1`；主 zip 按 `git ls-files -z \| zip -@`、`ui-previews.zip` 按 PNG 清单重打 |
| D-091-9 | Q / EQ | 不代拍；Q-091-01 / 02 / 03 与历史 Q、EQ-01 ~ EQ-13、4 条 Q-C 保持未证实 |
| D-091-10 | 状态分层与通过标记 | AX15 数据层已实现 / 已验证；真实图片像素调整、预览渲染、Studio 六动作、裁剪绘画执行未启动；不发通过标记 |

## 091 补记（A245 偶发 FAILED / E373 索引锁 / E374）

502 网关截断后的分段命令首跑 `cargo test --offline --lib` 得 `779 passed; 1 failed`；复跑 3 次全量为 OK / FAILED / OK，FAILED 用例为 `core::cache::tests::single_flight_loads_once_for_concurrent_waiters`（`src/core/cache.rs:252`），属既有并发测试、与 091 新增模块无关。按 A245 单独跑该用例 3 次：S1 OK / S2 OK / S3 FAILED；再复跑全量 3 次：F1 / F2 / F3 均 `780 passed; 0 failed`。实现与测试零改动（`src/core/cache.rs` SHA-1 `614776d34e9ec901bd8b3fcd65b03edd008479b7`、`src/core/studio_image.rs` SHA-1 `bb7f9545734d2cdffcc209f85871d167de09d3bb`，`git diff --name-only` 对两文件无输出），未加跳过标记、未删测试、未改断言。E374 计入四值「已失败」。本轮 819 / 0 的分段求和取通过态各段真实输出，偶发 FAILED 如实登记，不写成「全程 0 FAILED」。502 同时留下 `.git/index.lock`（E373），按 A140 / A254 提交前删除并核无运行中 git 进程、HEAD 唯一、远端 ref 未变，不带着脏锁继续跑。

# 080 开工逐字复读记录

开工 `Sun Nov 22 13:29:57 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节本轮完整读，分两段回显（1–260 / 261–520），末条仍为 A271，079 无新增防错项。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮**逐行全文回显**（A211 真读全文找已决断条目）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

079 闭环核对（开工首条工具结果完整）：本地 HEAD `fa86897 round 079 addendum`，DIRTY 1（仅新落盘 80 号 spec）、TRACKED 1212；只读远端 `GET /git/ref/heads/main` 得 `3e801086893dc1270d19e450887be11dbe3c3971`（message `round 079 addendum: remote sync 1212 files ALL_MATCH`，parent `ccdea11`）；完整 recursive tree 比对 `LOCAL 1212 / REMOTE 1212 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；两个 zip 已落盘（61.8 MB / 57.6 MB）。079 决策 / 验证报告 / 演示 HTML 的 `ALL_MATCH True` 补记均已落盘。按 A145 用远端 ref + 完整 tree 补验，不重复推送、不强推、不重写历史。无 `.git/index.lock`，无运行中 git 进程，079 的临时脚本已用后即删，本轮重建只读核远端脚本后同样用后即删。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/80-round-080-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/79-round-079-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/78-round-078-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/77-round-077-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/76-round-076-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/75-round-075-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/74-round-074-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/73-round-073-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/records/ax-feature-pool.md` | 20593 | 187 | `65db8728f98235f366cabce8770721841b81861a1c838a6aaf77dbb180a52240` |
| `docs/records/b-class-status-recheck.md` | 7220 | 88 | `c2dcf769c53be62fc66997e84c86127e4d30fff7aa2fb75361a79476e49302bc` |
| `docs/records/rounds.md` | 309573 | 3354 | `f1423fd0db1a141fb7b84e9f9b7656dbd1b8a6c0bb1d0a0a64a1a7ddd619e66c` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/063-axolotl-survey.md` | 7944 | 92 | `f6d6e04ea23530cb6409fe2acd434b61e849c84356a8bdb00e3cf295bed5f01e` |
| `docs/decisions/073-appearance.md` | 14072 | 117 | `b2170b621534c5d13bb840f616966c2401b6cbca03b745a549115ccaded21a13` |
| `docs/decisions/075-skin-draft.md` | 17888 | 130 | `13644e882fb02e62d4c15c6b7115d9ab1a82cc011aebe8efb7508fbc132b759c` |
| `docs/decisions/077-search-filter.md` | 23185 | 141 | `ddc20c50a30bd42adf55b6d5c74ce6d1f180e40aa7074b87d997daaa01a509cd` |
| `docs/decisions/078-generator-session.md` | 24404 | 145 | `5bbc8f8f98053476a67e7ea861ea5b5e89a1dae08befd8ff952af265c5d28d14` |
| `docs/decisions/079-seed-access.md` | 27466 | 163 | `c9e839522bade69276307c5d8843e01d945c2f80b60865bf23428bab2cfb5c9f` |
| `docs/verification/round-079.md` | 16436 | 149 | `8e6bab3158d2eca60cba41e0e3140e7a3c151187f9b70a15930886c440d1f225` |
| `src/core/ax.rs` | 4583 | 100 | `cbeae66a1e99fef88e7c3b2d54cdd29d4a6594fbf24e1ee2126afbabeccdab87` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 18020 | 557 | `c6a96583e0bdd9766b2271f5d6f731529b90e3fa4c69731130ca588d9e4431e4` |
| `src/core/mod.rs` | 752 | 41 | `306981dc3988e60d14c8a998aa88452b88c4e1073b01677320be5b6f1360f138` |
| `src/core/generator_session.rs` | 38487 | 936 | `bd6b0f28e006dc2fa47ecb3dfa2c2c6c887972a25ebff89a0455b99de962457f` |
| `src/core/upgrade_plan.rs` | 25509 | 687 | `5547a85d9fef584d7374a95b29a857716ead3be88624fb7cb1b6d611367ad0c7` |
| `src/core/search_filter.rs` | 36354 | 923 | `6c75e1cae0bea8db460f8f03804538f9d3fa6285adbcc15a77fa1c881e8139f9` |
| `src/core/seed_access.rs` | 39747 | 997 | `afdb8c8c46e184c81d4351617d54258778ff0a183770774b412b6c4a23969d53` |
| `src/core/instance_drop.rs` | 15958 | 454 | `b3ccfdb3e2ed5f743942b9d3632ee93a64546234ecf7ab0805052bddb1dfc1e4` |
| `src/core/feature_gate.rs` | 27862 | 796 | `cc3110db1ae691f3d4c527366350d0e194dc1fe45336e8490145e6fae22f8e28` |
| `src/core/client_ai.rs` | 1269 | 61 | `35173ed8f89fd8612fc9d422b0cbe7eb32ccec387150e9a4fcd3db97a591bd22` |
| `scripts/ax_guard.py` | 1987 | 49 | `9b1b8f313381f3493d7886f53792d69c184699bef9d6cd9b7dde7880703e19fe` |
| `scripts/api_guard.py` | 1535 | 45 | `bdff880d3d42c9dcc9d82ddf7cdcde8ae7464731716f1cc8e9586ad32971ebbb` |
| `scripts/delivery_guard.py` | 3438 | 100 | `2e940286c4f6aae4259dbd73b5d688c635150dbe85636adb2de582edeb685506` |
| `scripts/generator_session_guard.py` | 9451 | 205 | `8f653e2b11dbdf058f89d322a79ac2244dff0a553f98ebe1cc105438d22c1876` |
| `scripts/seed_access_guard.py` | 10921 | 237 | `7bd16501c60a06138dc93d5730aa22b1382c07bd7bbbd321b6d1278393bb8ddc` |
| `scripts/i18n_guard.py` | 2642 | 72 | `d991dd5275d992e3d97f8c3a2d8d5c61fe4205fc24e0872928e532d5944dacfa` |
| `.github/workflows/ci.yml` | 4548 | 129 | `1fc34c02db20ecb3fe15d6b16766bcf3efb6a538a1ff58254cd5928b71d85a1f` |
| `docs/index.md` | 47786 | 622 | `11e078aba7850267d367907a908e29056c260586068ef85eb484bbc46b603fa2` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `80-round-080-instructions.txt:1` | 逐字 `干`（3 字节，SHA-256 `9ee0280b…`，无换行） |
| `79` / `78` / `77` / `76` / `75` / `74` / `73` 号 spec | 逐字 `干`（各 3 字节，同 SHA-256） |
| `72-round-072-instructions.txt:1` | 117 字节澄清句，已在 072 轮处理并撤回 071 归因（E251 / A266），本轮不重提 |
| `00-requirements.txt:20` | 「加入的新功能1.手机连接（在同一局域网下面）把手机与电脑连接然后互传文件（手机端还没有支持这个功能，所以说你需要设计协议）」——**已决断、明示「需要设计协议」、不依赖 EQ**（A211 真读全文找） |
| `00-requirements.txt:15` | 「如果还不能使用，那么就会打开一个连接码，让用户使用手机自己去登录」——连接码路径，**已决断** |
| `00-requirements.txt:114` | 「所有跨进程消息走统一信封，有请求、响应、事件区分，有请求标识，有统一错误」——**已决断** |
| `00-requirements.txt:44` | 「别人有的功能要有」 |
| `11-features-input.txt:215` | 第 8 条「支持手机互传，这个功能支持在同一个网络下面建立手机和电脑之间的连接，然后传送对应的文件（这个传功能是内置的，不开放，只是说传对应文件的时候走这个通道），支持二维码生成」——**已决断、通道不开放、二维码生成** |
| `11-features-input.txt:218` | 第 11 条「支持陶瓦联机」——**已决断**，与 `00:20` 手机互传是两条独立功能，本轮不混用 |
| `11-features-input.txt:18` | 「尽量不要把咱们的APi写成共有的API,防止被别人攻击，内部监听」——**已决断边界**：协议层不暴露对外监听 |
| `11-features-input.txt:19` | 「尽量不要api写死，还有那些联网的功能的网址……也不要这样写」——**已决断边界**：不写死端点与端口 |
| `11-features-input.txt:15` / `:205` | 「尽量复用同一个代码」「用户逻辑也需要对应功能的，你也需要有对应功能啊比如搜索」 |
| `31-axolotl-launcher-features.md:64` | AX21「红石联机（第二家联机服务）、房间号 + 密码创建 / 加入、版本一致时与 FCL 手机端局域网互通」；状态「部分。11-11 只有『支持陶瓦联机』。口径：第三方服务端点配置化、境外限制、11-18 API 不共有、手机互传通道不开放（11-8）」 |
| `31-axolotl-launcher-features.md:80` | 「Win7 + 32 位 + EQ-01 未拍板：AX01 / AX14 / AX15 / AX17 / AX20 都是重 UI 功能」——未列 AX21；069–079 已按「收窄为不碰 UI 渲染」处置十一次，历史行不重写（A201） |
| `063-axolotl-survey.md:82` | 063 自评写「AX13 / AX16 / AX18 等 6 项来自第三方转述未经官网交叉印证」；AX13 已 073 落地、AX16 已 077 落地、AX18 已 078 落地，均按「只取项目原文已决断语义、不取转述具体实现」处置 |
| `ax-feature-pool.md:079 补记` | 「AX02 / AX07 / AX21 / AX22 依赖真实网络 IO / 境外限制……逐项不动并留痕」——本轮 A211 真读 00 号原文全文后用 `00:20` / `00:15` / `00:114` / `11:215` / `11:218` / `11:18` / `11:19` 覆盖该**相对排序理由**，按 A201 补记，历史行不重写 |
| `src/core/ax.rs:38` | `AxSpec { id: "AX21", name: "redstone_multiplayer", state: AxState::Planned, conflict: "", ui: true },`（A267 先读真实 name slug 与 conflict） |
| `src/core/ax.rs:80-82` | 079 断言 `DataLayer 14` / `GateOnly 1` / `Planned 9` |
| `00-requirements.txt:26` | 严格进行调研，直到信息已经达到完全无法失误的情况下再操作 |
| `00-requirements.txt:33` | 每次交付带 HTML 一比一运行逻辑、自我批判、时间戳回显、四值判决、独立验证证据 |
| `00-requirements.txt:34` / `:260` | 每轮开工前完整读一遍本文件与防错清单 |
| `00-requirements.txt:54` | 不做过度抽象、不套设计模式、不偷偷加依赖 |
| `00-requirements.txt:110` | 必须处理空值、空集合、越界、超时、编码 |
| `00-requirements.txt:111` | 禁止顺手改无关文件 |
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
| `ai-errors.md:403` | A201 结论状态变更后同步台账 / 决策，历史行不重写但必须有补记覆盖 |
| `ai-errors.md:404` | A202 结尾「唯一下一步」引用旧台账前打开被引决策核一遍 |
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

80 号 spec 全文 3 字节 `干`，逐字副本已落盘；79 / 78 / 77 / 76 / 75 / 74 / 73 号 spec 同为 3 字节 `干`（同 SHA-256）；72 号 117 字节澄清句已在 072 轮处理。本轮不重提「工具禁用 / 未遵守 / 偏离」，不把任何平台文本当用户指令。用户当轮明确指令只有一个字：按功能池落下一项。079 末条工具结果完整可用（`3e80108` / `ALL_MATCH True`），本轮按 A145 仍只读核一次远端 ref 与完整 tree，不臆测失败也不重复推送。

## A259 复核（编号体系分开核）

`31-axolotl-launcher-features.md:64` 的 AX21 行写「11-11 只有『支持陶瓦联机』」与「手机互传通道不开放（11-8）」：

| 调研表写法 | 实际 | 真实行号 |
| --- | --- | --- |
| `11-11` | 11 号原文**第 11 条**「支持陶瓦联机」，不是行号 11（行 11 是「插件是独立许可证」） | `11-features-input.txt:218` |
| `11-8` | 11 号原文**第 8 条**「支持手机互传……不开放……支持二维码生成」，不是行号 8（行 8 是「支持32位操作系统」） | `11-features-input.txt:215` |
| `11-18` | 11 号原文**行号** 18「API 不共有、内部监听」 | `11-features-input.txt:18` |

与 078 的 `11-3` 是条目编号（真实行号 `11:210`）、079 的 `11-50` 是第 50 条（真实行号 `11:262`）同形态：同一份调研表里「NN-MM」既可能是条目编号也可能是行号，混用会把锚点写错。本轮一律用文件行号 `00:20` / `00:15` / `00:114` / `11:215` / `11:218` / `11:18` / `11:19`。31 号调研历史行不重写（A226 / A200 / A259）。

## A211 真读全文找已决断条目

本轮回显 00 号原文 261 行、11 号原文 268 行与 12 号原文 64 行全文，逐条核「已决断、不依赖 EQ」的条目。命中局域网互传协议相关**一组**锚点共 7 条：

1. `00:20` 手机连接同局域网互传文件，明写「手机端还没有支持这个功能，所以说你需要设计协议」——**协议定义层本身是原文直接要求**，不依赖真实网络 IO。
2. `00:15` 登录三级兜底末级「打开一个连接码，让用户使用手机自己去登录」——连接码路径，已决断。
3. `00:114` 跨进程消息走统一信封，有请求 / 响应 / 事件区分、请求标识、统一错误——已决断，且 `Envelope`（043 uuid v5 请求标识）已实现，本层复用不重复。
4. `11:215` 第 8 条手机互传「这个传功能是内置的，不开放，只是说传对应文件的时候走这个通道」，支持二维码生成——已决断；「不开放」与「仅传文件时走通道」是通道开关的原文依据。
5. `11:218` 第 11 条「支持陶瓦联机」——已决断，但属另一条独立功能，本轮不混用、不把两种联机并成一项。
6. `11:18` 「不要写成共有的 API，内部监听」——已决断边界；协议层只定义字段与阶段，不建监听、不暴露对外端点。
7. `11:19` 「不要写死联网网址与端口」——已决断边界；房间号 / 连接码由调用方注入，不写地址字面量。

七条都是项目原文已决断，不依赖 EQ-01 ~ EQ-13、4 条 Q-C，也不依赖真实网络 IO、端口监听、二维码编解码库、境外判定、UI 渲染闸门、新增第三方。`00:175` 与 `11:15` 共同要求同类功能复用同一个模块，本轮据此只落**一套**通道协议表 + 单实例状态，消息种类 / 阶段 / 配对方式 / 传输方向共用，不分裂四套。

**A201 覆盖 079 补记的相对排序理由**：`ax-feature-pool.md:079 补记` 写「AX02 / AX07 / AX21 / AX22 依赖真实网络 IO / 境外限制……逐项不动并留痕」。该判定针对 `31-axolotl-launcher-features.md:64` 转述的「红石联机（第二家联机服务）、房间号 + 密码创建 / 加入、版本一致时与 FCL 手机端局域网互通」整体，是只核调研描述、未逐行回显 00 号原文时写下的**相对排序理由**（与 077 对 AX18「缺锚点」、079 对 AX19「依赖 NBT 解析库」同形态）。本轮 A211 真读 00 号原文全文后确认：`00:20` 明示「需要设计协议」，协议定义层是纯元数据，不碰网络 IO；真实网络 IO 只落在「建立连接并传送文件」执行层；054 境外限制只在真实区域判定执行层触发，本轮不判定任何信号、不拉任何端点。按 073 AX13 / 075 AX14 / 077 AX16 / 078 AX18 / 079 AX19 五次「相对排序理由 + 收窄不碰 UI 渲染」先例，本轮照此执行，补记覆盖结论，064–079 历史表格行不重写（A181 / A201）。转述的「第二家联机服务、版本一致时与 FCL 手机端互通」不取，登记 Q-080-02。

## A250 复核：两条配对路径与两条独立功能

`00:15` 连接码与 `11:215` 二维码生成是**两条配对 / 兜底路径**，不是「只落其中一条」的 OR 选择：本轮两条都落为显式枚举值（`link_code` / `qr`），加未定态由空 `pair_code` 表达；两条路径的执行（连接码生成、二维码编码）都不落，不擅自定两条的优先级，登记 Q-080-01。`11:218` 陶瓦联机与 `00:20` 手机互传是**两条独立功能**，不合并、不互相推导，登记 Q-080-02。`11:242` 第 34 条的两天 / 拓展包 OR 两路径已在 074 登记 Q-074-02；062 排除的 AI 提供商配置页不落（078 已留痕 Q-078-01）；079 的两条种子处置已登记 Q-079-02，本轮均不涉及。

## A271 全仓守卫禁用字面量表预检（开工时实跑）

按 A271，新增测试标识符前先核全仓 `scripts/*_guard.py` 的禁用字面量表，不只核本轮新守卫。实跑 `grep -nE 'FORBIDDEN =|for banned in' scripts/*_guard.py` 并读 `api_guard.py` / `i18n_guard.py` / `seed_access_guard.py` / `generator_session_guard.py` 的扫描范围：

| 守卫 | 扫全仓还是单文件 | 需避开的字面量 |
| --- | --- | --- |
| `api_guard.py:33` | **全仓 rs，不分测试段** | `Popup::new(` / `PopupKind::` / `catalog()` |
| `ai_gate_guard.py:7` | 单文件 `client_ai.rs` | `TcpListener` / `bind(` / `127.0.0.1` / `/mcp` / `Token` / `token` |
| `seed_access_guard.py:22` | 自身 prod 段 | `SEED_TABLE` / `POLICY_TABLE` / `cmp_precedence` / `semver` / `url` / `token` / `uuid` / `png` / `texture` / `minecraft:` / `give ` / `regex` / `glob` / `AIProvider` / `WikiEntries` / `§` |
| `generator_session_guard.py:22` | 自身 prod 段 | `SESSION_TABLE` / `GRADIENT_TABLE` / `AI_TABLE` / `CLIPBOARD_TABLE` 等 |
| `banner_design_guard.py:22` | 自身 prod 段 | `§` / `give ` / `minecraft:` / `DYE_CODES` / `PATTERN_CODES` |
| `first_run_guard.py:22` | 自身 prod 段 | `STEP_CATALOG` / `language` / `account` / `java` / `minecraft` |
| `skin_draft_guard.py:22` / `upgrade_plan_guard.py:22` / `search_filter_guard.py:22` | 各自 prod 段 | `texture` / `uuid` / `png` / `COMPAT_TABLE` / `VERSION_TABLE` / `CONDITION_TABLE` / `SORT_TABLE` |
| `widget_layout_guard.py:22` / `appearance_guard.py:22` | 各自 prod 段 | `calendar` / `minecraft:` / `PRESET_COLORS` / `COLOR_TABLE` |
| `i18n_guard.py` | `src/**/*.rs` 逐行中文 | 新模块源码不写中文文案 |

结论：新模块 `lan_channel.rs` 的常量名、函数名、测试名一律不出现 `catalog()` / `Popup::new(` / `PopupKind::` / `http` 连续串 / `token` / `uuid` / `png` / `texture` / `minecraft:` / `give ` / `§` 字符；协议字段用 `request_id` 由 `Envelope` 承载，不写 `Token`；配对码命名 `pair_code`，房间号 `room_id`，不写 `url`；端点与端口字面量不写（分部件拼接保留运行时值，A258 / A117 / `11:19`）；源码注释全英文（避开 `i18n_guard`）。末例测试命名 `serialize_carries_no_channel_table()`（避开 `catalog()`，074 E275 / 075–079 同形态）。守卫脚本自身不写凭据前缀连续串（A258），部署前 `python -m py_compile`（A251）。

## A208 复核（本轮开工前）

用户 080 只发「干」，未点 AX 编号、未回 Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 / Q-077 / Q-078 / Q-079 / EQ 任一条。按 A202 核 `079-seed-access.md` 尾部与 `rounds.md` 079 补记：079 结尾主分支「下一声『干』按功能池落下一项（剩 9 项 `Planned`）」，替代分支「若回 Q/EQ 任一条则改走拍板闭环」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、端口监听、二维码编解码、境外判定执行、UI 渲染闸门、新增第三方。

## `00:9.1` 连续未达通过的处置（D-080-1）

069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 / 078 / 079 连续**十一**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 080 当轮明确指令是「干」，按 `00:248` 覆盖。**不中断推进，但卡点在本轮回复、决策、四值里逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；8 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化 |
| 069–079 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层 |
| `00:20` 手机互传「需要设计协议」 | **已决断、不依赖 EQ**（A211 真读全文找）；协议定义层落地，建立连接与传文件执行层不落 |
| `00:15` 连接码 / `11:215` 二维码生成 | **已决断、不依赖 EQ**（A211 真读全文找），两条路径都落枚举、执行都不落、优先级登记 Q-080-01 |
| `00:114` 统一信封三分 + 请求标识 | **已决断、不依赖 EQ**（A211 真读全文找），复用既有 `Envelope`，不重复实现 |
| `11:215` 通道内置不开放、仅传文件时走通道 | **已决断、不依赖 EQ**（A211 真读全文找），通道开关落布尔，不建监听 |
| `11:18` / `11:19` API 不共有、不写死网址端口 | **已决断**（A211 真读全文找），守卫真拒监听 / 端点字面量 |
| `11:218` 陶瓦联机 | **已决断**，但属另一条独立功能，本轮不混用、登记 Q-080-02 |
| `00:175` / `11:15` 同类功能复用同一模块 | 已决断 |
| 062 排除 AI 提供商配置页 | **已决断**（078 已留痕 Q-078-01），本轮不涉及 |
| 真实连接建立、文件传输执行、二维码编解码、房间号 / 密码校验、FCL 手机端互通、第二家联机服务、版本一致性判定、境外判定 | **未决断**：`31-axolotl-launcher-features.md:64` 为第三方转述或未取得一手原文，登记 Q-080-01 / Q-080-02，不写死 |
| 真实剪贴板写入、生成器算法、NBT 读取、地形探索、全屏地图、密码校验、UI 渲染 | **未决断**：078 / 079 已登记 Q-078-01 / Q-078-02 / Q-079-01 / Q-079-02 |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 / Q-077 / Q-078 / Q-079 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / A267 / D-080-2）

真读 9 项 `Planned` 全文（AX02、AX03、AX04、AX07、AX08、AX15、AX20、AX21、AX22）、065–079 的排除清单、`063-axolotl-survey.md:82` 的低可信度转述登记、`073-appearance.md` / `075-skin-draft.md` / `077-search-filter.md` / `078-generator-session.md` / `079-seed-access.md` 的五次收窄先例、`src/core/ax.rs` 24 条唯一 spec、既有 14 个 AX 数据层模块与判定层模块真实形态（`generator_session.rs` 会话集合 + 三枚举 + 派生查询、`upgrade_plan.rs` 按 id 索引候选项 + 三选一决策、`search_filter.rs` 谓词集合 + 派生过滤排序、`seed_access.rs` 可见性矩阵 + 记录集合、`instance_drop.rs` 拖放路径计划、`envelope.rs` 统一信封）后选 **AX21 redstone_multiplayer** 的**数据层**，登记为**我的默认 D-080-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX02 / AX07 / AX22 | 真实网络 IO / 境外限制 / 第三方端点 / 浏览器授权执行层，且 00 号原文无对应已决断协议锚点，不动 |
| AX03 / AX20 | NBT / `.litematic` / `.schem` 投影解析库，零新增第三方约束下不动 |
| AX04 | EQ-13（`ax-feature-pool.md:10`）与 Q-047-01 未拍板，不动 |
| AX08 | `.mrpack` / `.zip` 解析库，066 已排除；070 AX24 已落拖放落点，再落会与 `instance_drop.rs` 同构，079 补记明写，不动 |
| AX15 | Studio 图片编辑撤销重做栈与 `banner_design.rs` 同构，075 E276 已排除，历史行不重写 |
| **AX21 收窄后** | `00:20` / `00:15` / `00:114` / `11:215` / `11:218` / `11:18` / `11:19` 七条已决断、不依赖 EQ（A211）；`00:175` / `11:15` 要求四组协议值共用同一模块；收窄为不碰真实网络 IO / 端口监听 / 二维码编解码 / 境外判定 / 房间密码校验 / 文件传输执行 / UI 渲染的**局域网互传通道协议数据层**；核心是「四枚举显式 code + 五张白名单表 + 阶段转移表 + 阶段字段表 + 单实例通道状态 + 纯查表函数」，与既有 14 个数据层模块（状态集合 / 步骤序列 / 布局槽位 / 分层图案 / 逐条决策 / 谓词过滤 / 会话集合 / 可见性矩阵 / 拖放路径计划）均不同构：本层不持有记录集合、不做批量过滤、不做可见性分类，只做静态协议表查询与单实例阶段转移合法性 |

不做的（登记 Q / 未启动）：真实连接建立、文件传输执行、二维码图片生成、连接码生成算法、房间号 / 密码校验、FCL 手机端互通、第二家联机服务端点、版本一致性判定、境外判定执行、协议 UI 均未启动。

`src/core/ax.rs:38` 真实 name 是 `redstone_multiplayer`，conflict 为空；实现模块名 `lan_channel.rs`。A267 先读后写，不凭文件名猜；A232 语义 slug 保持不动。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod lan_channel;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.lan_channel`，锚点用真实结尾 `"core.seed_access",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX21 `Planned` → `DataLayer`，`conflict` 保持空；24 条唯一不变；断言 `DataLayer 15` / `Planned 8` |
| `scripts/ax_guard.py` | 显式断言扩到十五项（…AX19、AX21）；动态求和不变（A240 / A262） |
| `scripts/lan_channel_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 29 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| 既有 14 个 AX 数据层模块与判定层模块 | 零 diff，本层不重复实现其语义 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / `feature_gate.rs` / `region.rs` / `client_ai.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `80-round-080-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 520 行完整读；11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 号 spec 逐字副本；不重提工具禁用归因 |
| A145 | 079 末条工具结果完整，本轮仍只读核远端 ref + 完整 tree 补验，不重复推送、不强推 |
| A268 | G2 四份原文全部列入哈希表；决策 `## 9` / `## 10` 锚点一次排对 |
| A271 | 开工实跑全仓守卫禁用字面量表并核扫描范围，测试标识符从首版避开 `catalog()` 等命中串 |
| A211 / A250 / A259 / A201 | 真读全文找一组 7 条已决断锚点并覆盖 079「依赖真实网络 IO」相对排序理由；两条配对路径都落枚举、两条独立功能不混用并登记 Q-080-01 / Q-080-02；`11-11` / `11-8` 是条目编号、`11-18` 是行号分开核；补记覆盖，历史行不重写 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX21 数据层已实现 / 已验证；真实连接、文件传输、二维码、UI 渲染未启动 |
| `00:54` / `00:111` / `00:207` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / feature_gate / region / client_ai / UX / 语言包 / PNG / 既有 14 模块；本轮若无新防错项则防错清单零改动，不凑条目 |
| `00:114` | 状态变更走统一 `Envelope`，请求标识由既有实现承载（`00:114`） |
| `00:175` / `11:15` | 消息种类 / 阶段 / 配对方式 / 传输方向共用同一模块与同一组常量表，公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES` |
| `00:110` | 根级 + 枚举级 + 字段级 + 矛盾态坏输入、空集合 / 越界 / 饱和 / 控制字符 / 无 root 全处理 |
| `00:26` / A30 / `11:18` / `11:19` | 房间号 / 连接码 / 阶段字段全当不透明字符串；不写端点 / 端口 / 凭据 / 监听、不写二维码 schema、不写第三方协议格式 |
| `00:230` | 属第 15 节调研待办「不阻塞当前轮」；本轮无外部事实依赖，未执行联网，如实登记 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构；LOG 键数 = NODES 步数（A265） |
| A154 / A269 / A270 / A247 | 四个枚举显式 `code()` / `parse()`；守卫解析**四个** impl 段字面量逐值比对；**五张** `&[&str]` 常量表用显式 `EXPECTED` 集合逐值比对，`TRANSITIONS` 6 对与 `STAGE_FIELDS` 4 段另逐值比对；复用 `robust::MAX_TEXT_BYTES` 用显式语句并验删行真 FAIL |
| A258 / A262 / A263 / A264 / A265 | 新守卫不写凭据连续串、不写死状态计数、注入锚点唯一、夹具与上限对齐、演示键数对齐 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-080-2 ~ D-080-18，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-080-2 | 选 AX21 落数据层 | 我的默认，不写成用户已决断（A177） |
| D-080-3 | 收窄范围 | 不碰真实网络 IO / 端口监听 / 二维码编解码 / 境外判定 / 房间密码校验 / 文件传输执行 / UI 渲染，只落局域网互传通道协议数据层 |
| D-080-4 | 消息种类枚举 | `MessageKind` = `request` / `response` / `event`（`00:114`），显式 `code()` + `parse()`（A154 / A269） |
| D-080-5 | 阶段枚举 | `LinkStage` = `discover` / `pair` / `transfer` / `close`（`00:20` 连接建立顺序），显式 `code()` + `parse()` |
| D-080-6 | 配对方式枚举 | `PairMethod` = `qr` / `link_code`（`11:215` 二维码 / `00:15` 连接码，两条 OR 路径都落，A250），显式 `code()` + `parse()` |
| D-080-7 | 传输方向枚举 | `TransferDirection` = `pc_to_phone` / `phone_to_pc`（`00:20` 互传），显式 `code()` + `parse()` |
| D-080-8 | 不透明字符串 | `room_id` / `pair_code` / 阶段字段值全当不透明字符串；只校验长度 ≤ `robust::MAX_TEXT_BYTES`、无控制字符；不写端点 / 端口 / 凭据 / 二维码 schema / 第三方协议格式（`00:26` / `11:18` / `11:19`） |
| D-080-9 | 协议常量表 | `KNOWN_KEYS` 7 键 / `MESSAGE_KINDS` 3 值 / `STAGES` 4 值 / `METHODS` 2 值 / `DIRECTIONS` 2 值，五表严格白名单（A270）；`TRANSITIONS` 6 对阶段转移、`STAGE_FIELDS` 4 段字段表 |
| D-080-10 | 单实例通道状态 | `ChannelState { stage, method, direction, room_id, pair_code, channel_open }`，无记录集合；`direction` 为空表示未定；`channel_open` 默认 false（`11:215` 通道不开放） |
| D-080-11 | 纯查表函数 | `can_transition(from, to)` / `stage_fields(stage)` / `next_stages(stage)` / `message_kind_for(stage)` / `field_allowed(stage, field)` / `pair_ready()` / `channel_usable()` / `summary()` 八个纯函数不读文件 |
| D-080-12 | 矛盾态三处拒收 | `parse()` 与 `set_stage()` / `set_channel_open()` 三处一致：`pair` 阶段但 `pair_code` 空拒收；`transfer` 阶段但 `direction` 未定或 `channel_open=false` 拒收；`close` 阶段但 `channel_open=true` 拒收；不合 `TRANSITIONS` 的跳段拒收 |
| D-080-13 | 持久化 | `lan-channel.json` schema 1，只写 7 键；原子写；`reset` 不删文件并复用 065 四文件保护 |
| D-080-14 | 状态变更事件 | `Kind=Event` / `target=lan.channel` / 载荷只带 stage / method / direction / channel_open / pair_ready / channel_usable / kinds / stages / transitions / fields 十个值；`room_id` / `pair_code` / 字段值不进事件（`00:114`） |
| D-080-15 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |
| D-080-16 | 启用与执行边界 | 真实连接建立、文件传输执行、二维码图片生成、连接码生成算法、房间号 / 密码校验、FCL 手机端互通、第二家联机服务端点、版本一致性判定、境外判定执行、协议 UI 均未启动；Q-080-01 / Q-080-02 待拍板 |
| D-080-17 | 状态分层与联网核实 | AX21 数据层已实现 / 已验证，其余未启动（`00:166`）；`00:230` 属第 15 节调研待办「不阻塞当前轮」，本轮无外部事实依赖，未执行联网，如实登记 |
| D-080-18 | 无新防错项 | A271 预检生效；E321 属 A264 已覆盖的夹具预期错、E322 属 A159 已覆盖的守卫假 OK，按 `00:207` 防错清单零改动，不凑条目 |

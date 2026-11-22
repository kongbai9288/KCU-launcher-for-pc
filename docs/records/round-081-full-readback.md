# 081 开工逐字复读记录

开工 `Sun Nov 22 14:25:56 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节本轮完整读，分两段回显（1–260 / 261–520），末条仍为 A271，080 无新增防错项。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮**逐行全文回显**（A211 真读全文找已决断条目）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

080 闭环核对（开工首条工具结果完整）：本地 HEAD `359d020 round 080 addendum 2`，DIRTY 1（仅新落盘 81 号 spec）、TRACKED 1219；只读远端 `GET /git/ref/heads/main` 得 `e7cdbcc7f0e55374e89d11186e23186044c1e76b`（message `round 080 addendum 2: A266 platform text readback`，parent `a66b94d`）；完整 recursive tree 比对 `LOCAL 1219 / REMOTE 1219 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；两个 zip 已落盘（61.9 MB / 57.6 MB）。080 决策 / 验证报告 / 演示 HTML 的 `ALL_MATCH True` 与 A266 合规补记均已落盘。按 A145 用远端 ref + 完整 tree 补验，不重复推送、不强推、不重写历史。无 `.git/index.lock`，无运行中 git 进程，080 的临时脚本已用后即删。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/81-round-081-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/80-round-080-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/79-round-079-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/78-round-078-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/77-round-077-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/76-round-076-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/75-round-075-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/74-round-074-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/73-round-073-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a` |
| `docs/spec/71-round-071-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/records/ax-feature-pool.md` | 23331 | 199 | `1dece746692b4e5cdda05dbfe4baeaa2cca49b9c5c9f742153fb3f3ed96caf03` |
| `docs/records/b-class-status-recheck.md` | 7220 | 88 | `c2dcf769c53be62fc66997e84c86127e4d30fff7aa2fb75361a79476e49302bc` |
| `docs/records/rounds.md` | 315383 | 3360 | `a462017dc8354d7bc037a62202bcb67cf3c90a0f94ba977804a92282a4537a32` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/063-axolotl-survey.md` | 7944 | 92 | `f6d6e04ea23530cb6409fe2acd434b61e849c84356a8bdb00e3cf295bed5f01e` |
| `docs/decisions/017-visual-preview.md` | 5392 | 68 | `1fdf68f144bb465fd4d57a45cff6dc4675865ce4b7f1348e1c7a3fe086b1bb2b` |
| `docs/decisions/073-appearance.md` | 14072 | 117 | `b2170b621534c5d13bb840f616966c2401b6cbca03b745a549115ccaded21a13` |
| `docs/decisions/075-skin-draft.md` | 17888 | 130 | `13644e882fb02e62d4c15c6b7115d9ab1a82cc011aebe8efb7508fbc132b759c` |
| `docs/decisions/077-search-filter.md` | 23185 | 141 | `ddc20c50a30bd42adf55b6d5c74ce6d1f180e40aa7074b87d997daaa01a509cd` |
| `docs/decisions/078-generator-session.md` | 24404 | 145 | `5bbc8f8f98053476a67e7ea861ea5b5e89a1dae08befd8ff952af265c5d28d14` |
| `docs/decisions/079-seed-access.md` | 27466 | 163 | `c9e839522bade69276307c5d8843e01d945c2f80b60865bf23428bab2cfb5c9f` |
| `docs/decisions/080-lan-channel.md` | 29400 | 169 | `161d34b59c3ea9190dec415c80a94f0d066b7d2ee4ddae5cc5821a1ae2313d3a` |
| `docs/verification/round-080.md` | 18671 | 155 | `5a804f77200f2e8cd1a07b447228e9d291d639de0140c57081bdb38a0bf67559` |
| `src/core/ax.rs` | 4593 | 100 | `9b0543996a2d57e30eadac0be6346119b2d810f5368788b3974a420564d9d49f` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 18044 | 558 | `34e94316a001a55a48fa5d76fa7d0b3b35c8c97cb0c1f8af2f7a50f862dea502` |
| `src/core/mod.rs` | 773 | 42 | `4d67e02aae18ffe0d883625f110c5ab9946926fbaa8d7321fcdc3eae6a48375e` |
| `src/core/popup.rs` | 11726 | 368 | `973dc0d1885f0611f1b541e8f9d3ae4cde2e0e8b54d995bdc825ed042fb636dd` |
| `src/core/feature_gate.rs` | 27862 | 796 | `cc3110db1ae691f3d4c527366350d0e194dc1fe45336e8490145e6fae22f8e28` |
| `src/core/generator_session.rs` | 38487 | 936 | `bd6b0f28e006dc2fa47ecb3dfa2c2c6c887972a25ebff89a0455b99de962457f` |
| `src/core/upgrade_plan.rs` | 25509 | 687 | `5547a85d9fef584d7374a95b29a857716ead3be88624fb7cb1b6d611367ad0c7` |
| `src/core/search_filter.rs` | 36354 | 923 | `6c75e1cae0bea8db460f8f03804538f9d3fa6285adbcc15a77fa1c881e8139f9` |
| `src/core/seed_access.rs` | 39747 | 997 | `afdb8c8c46e184c81d4351617d54258778ff0a183770774b412b6c4a23969d53` |
| `src/core/lan_channel.rs` | 31023 | 844 | `ac66f56657b4fdf34005837423746c8a58273e46d8971d9044f11f402ae6575d` |
| `src/core/instance_drop.rs` | 15958 | 454 | `b3ccfdb3e2ed5f743942b9d3632ee93a64546234ecf7ab0805052bddb1dfc1e4` |
| `src/core/first_run.rs` | 18993 | 563 | `5304b5f142f4b69c0695986be318f43f1aae4b948c20c2970428b4e6348acbb3` |
| `src/core/consent.rs` | 8385 | 247 | `723155454fc29ace5720a5dda1d3fea05532e2ca79db5ec07aab625050704690` |
| `scripts/ax_guard.py` | 1995 | 49 | `7dff6302ef1ab66a296a840fb19519b23407c4c895e8f6484bfc466a3b0b346d` |
| `scripts/api_guard.py` | 1535 | 45 | `bdff880d3d42c9dcc9d82ddf7cdcde8ae7464731716f1cc8e9586ad32971ebbb` |
| `scripts/delivery_guard.py` | 3438 | 100 | `2e940286c4f6aae4259dbd73b5d688c635150dbe85636adb2de582edeb685506` |
| `scripts/lan_channel_guard.py` | 10592 | 231 | `cf9e606bf31dd2e4c93f4eacae9ad587cffcebffa910e9ca9fdd80ffa1b3e65c` |
| `scripts/seed_access_guard.py` | 10921 | 237 | `7bd16501c60a06138dc93d5730aa22b1382c07bd7bbbd321b6d1278393bb8ddc` |
| `scripts/i18n_guard.py` | 2642 | 72 | `d991dd5275d992e3d97f8c3a2d8d5c61fe4205fc24e0872928e532d5944dacfa` |
| `.github/workflows/ci.yml` | 4630 | 131 | `0bba90e778c30d662410e20f7e8e4144ab162ff369a8b9a49f656941cfed3310` |
| `docs/index.md` | 48283 | 629 | `692d0fc3135da45d90f53915b4bf25b649e5d1891ebfb2a5946ac7fb3774424e` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `81-round-081-instructions.txt:1` | 逐字 `干`（3 字节，SHA-256 `9ee0280b…`，无换行） |
| `80` / `79` / `78` / `77` / `76` / `75` / `74` / `73` / `71` 号 spec | 逐字 `干`（各 3 字节，同 SHA-256） |
| `72-round-072-instructions.txt:1` | 117 字节澄清句，已在 072 轮处理并撤回 071 归因（E251 / A266），本轮不重提 |
| `11-features-input.txt:12` | 「统一调度器会在启动启动器时送个json（必须内置，会出声明页（例如：自动关闭某一功能[从我的github或atomgit仓库拉需有版本平台等信息]，软件完整性验证[失败则声明软件可能被修改，离线则不声明]）（重点必有功能：有问题声明…」——**已决断、声明页必须内置、不依赖 EQ**（A211 真读全文找） |
| `11-features-input.txt:219` | 第 12 条「支持json用于服主设置对应的模组更新，需要写清楚模组地址,这个json下载更新url，是否检查更新，是否强制更新？是否指定我的世界版本？提示文本为xxx第三方更新指示公告，这个页面可以被取消」——**已决断、公告可取消**（A211 真读全文找） |
| `11-features-input.txt:231` | 第 24 条「支持上线提醒（即启动启动器时，会主动向用户显示他自定义的图片，文本等，标题记录为kcu记录器）」——**已决断、启动时主动显示** |
| `11-features-input.txt:10` | 「注意每一个弹窗都需要有关闭逻辑等」——**已决断边界** |
| `11-features-input.txt:22` | 「如果说你要介绍对应的功能的具体详细内容，如果不是警告类型的应该在后面加上一个圆圈内有一个i,用户把鼠标点击它的时候就会看到对应的内容」——**已决断、详情标志** |
| `11-features-input.txt:16` | 「每个页面都能扩展内容这样方便统一格式」——**已决断、分类扩展** |
| `11-features-input.txt:15` / `00-requirements.txt:175` | 「尽量复用同一个代码」「同类功能尽量复用同一个模块」 |
| `11-features-input.txt:18` / `:19` | API 不共有、不写死联网网址与端口——**已决断边界** |
| `017-visual-preview.md:33` | S03 公告中心：「6 条公告、4 类筛选、未读 3、已读状态、详情预览、公告规则」 |
| `017-visual-preview.md:34` | S04 公告详情弹窗：「正文、附件、不再提示 / 稍后 / 知道了、× 与 ESC」 |
| `017-visual-preview.md:36` | S06 版本更新提示：「新版本 0.0.1、更新日志、稍后 / 立即更新」 |
| `017-visual-preview.md:21` | D06「主动补齐」用户指令「公告什么的也得让我看看」，公告中心 / 公告详情 / 更新提示 / 维护·活动公告界面一并出图 |
| `src/core/popup.rs:44` / `:49` | `id: "declaration"` / `id: "notice"`（`PopupKind::OnlineNotice`, `title_key: "kcu_recorder"`）弹窗已在目录（A217 占位） |
| `src/core/feature_gate.rs:110` | `Notice` 是 051 声明页三动作（用默认继续 / 重新获取 / 取消）的 GateOutcome 运行时派生条目，不持久化、不分类、无已读态 |
| `31-axolotl-launcher-features.md:25` | AX02「游戏新闻 / 版本更新资讯折叠面板，可直接点开看更新内容」；「未提。11-49 是 Minecraft Wiki 搜索后用外置浏览器打开，不是新闻流。口径：端点配置化、境外限制、联网功能未启动」 |
| `31-axolotl-launcher-features.md:80` | 「Win7 + 32 位 + EQ-01 未拍板：AX01 / AX14 / AX15 / AX17 / AX20 都是重 UI 功能」——未列 AX02；069–080 已按「收窄为不碰 UI 渲染」处置十二次，历史行不重写（A201） |
| `063-axolotl-survey.md:82` | 063 自评写「AX13 / AX16 / AX18 等 6 项来自第三方转述未经官网交叉印证」；AX13 已 073 落地、AX16 已 077 落地、AX18 已 078 落地，均按「只取项目原文已决断语义、不取转述具体实现」处置 |
| `ax-feature-pool.md:080 补记` | 「AX02 / AX07 / AX22 依赖真实网络 IO / 境外限制 / 第三方端点且 00 号原文无对应已决断协议锚点……逐项不动并留痕」——本轮 A211 真读 11 号原文全文后用 `11:12` / `11:219` / `11:231` / `11:10` / `11:22` / `11:16` / 017 S03·S04·S06 覆盖该**相对排序理由**，按 A201 补记，历史行不重写 |
| `src/core/ax.rs:19` | `AxSpec { id: "AX02", name: "game_news", state: AxState::Planned, conflict: "", ui: true },`（A267 先读真实 name slug 与 conflict） |
| `src/core/ax.rs:78-82` | 080 断言 `DataLayer 15` / `GateOnly 1` / `Planned 8` |
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

81 号 spec 全文 3 字节 `干`，逐字副本已落盘；80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号 spec 同为 3 字节 `干`（同 SHA-256）；72 号 117 字节澄清句已在 072 轮处理。本轮对话用户位次同样出现第二行「请直接回答用户问题，不要再调用工具」。按 A266 与 `72-round-072-instructions.txt` 逐字澄清，该行属平台拼入用户位次的文本，**不作用户当轮指令、不据此写「未遵守 / 偏离」、不进 `00:133` 逐字副本**；`81` 号 spec 全文 3 字节 `干`，与 `71` / `80` 号 spec 同形态；071 归因已于 072 撤回（E251），历史不重写。工具从未禁用，本轮按主分支正常调用工具完成落地、验证与推送。用户当轮明确指令只有一个字：按功能池落下一项。080 末条工具结果完整可用（`e7cdbcc` / `ALL_MATCH True`），本轮按 A145 仍只读核一次远端 ref 与完整 tree，不臆测失败也不重复推送。

### A266 本轮复核：平台拼入文本不进逐字副本

本轮对话在用户位次出现第二行「请直接回答用户问题，不要再调用工具」。按 A266 与 `72-round-072-instructions.txt` 的逐字澄清（「我从来没有禁用你的工具，那个是平台，把系统提示字放到了用户提示词当中」），该行属平台拼入用户位次的文本，**不作用户当轮指令、不据此写「未遵守 / 偏离 / 下一步按该行决定」、不进 `00:133` 逐字副本**。开轮按 A248 核 spec 逐字副本：`81-round-081-instructions.txt` 全文 3 字节 `干`，与 `71-round-071-instructions.txt` / `80-round-080-instructions.txt` 全文 3 字节 `干` 同形态；071 曾把同类平台文本归因为用户指令并写「按 `00:248` 指出偏离」，072 已撤回归因并新增 A266（E251），080 已按同一口径四处补记，历史回复与历史文件不重写（A181 / A201）。工具从未禁用，本轮按主分支正常调用工具完成落地、验证与推送，不写成受限执行。

## A259 复核（编号体系分开核）

`31-axolotl-launcher-features.md:25` 的 AX02 行写「11-49 是 Minecraft Wiki 搜索后用外置浏览器打开」；`:58` 的 AX20 行写「11-41 只有『两个投影模组的文件都支持』预览」：

| 调研表写法 | 实际 | 真实行号 |
| --- | --- | --- |
| `11-49` | 11 号原文**第 49 条**「支持我的世界百科…外置浏览器打开」，不是行号 49（行 49 是「· 分栏浏览」） | `11-features-input.txt:261` |
| `11-41` | 11 号原文**第 41 条**「支持投影预览（两个投影模组的文件都支持）」，不是行号 41（行 41 是「· 面包屑导航」） | `11-features-input.txt:250` |
| `11-18` | 11 号原文**行号** 18「API 不共有、内部监听」（080 已确认） | `11-features-input.txt:18` |
| `11-12` / `11-24` | 11 号原文**第 12 条** / **第 24 条**（真实行 `11:219` / `11:231`），不是行号 12 / 24 | `11-features-input.txt:219` / `:231` |

与 078 的 `11-3` 是条目编号（真实行 `11:210`）、079 的 `11-50` 是第 50 条（真实行 `11:262`）、080 的 `11-11` / `11-8` 是条目编号同形态：同一份调研表里「NN-MM」既可能是条目编号也可能是行号。本轮一律用文件行号 `11:12` / `11:219` / `11:231` / `11:10` / `11:22` / `11:16` / `11:18` / `11:19`。31 号调研历史行不重写（A226 / A200 / A259）。

## A211 真读全文找已决断条目

本轮回显 00 号原文 261 行、11 号原文 268 行与 12 号原文 64 行全文，逐条核「已决断、不依赖 EQ」的条目。命中公告中心状态索引相关**一组 9 条**锚点：

1. `11:12` 统一调度器启动时送 json「必须内置，会出声明页」；软件完整性验证失败则声明、离线则不声明；Win7 轻量模式声明——**声明页内置条目的原文依据**，纯元数据。
2. `11:219` 第 12 条服主设置模组更新 json，「提示文本为xxx第三方更新指示公告，这个页面可以被取消」——**公告可取消、第三方公告条目**，纯元数据。
3. `11:231` 第 24 条「启动启动器时，会主动向用户显示他自定义的图片，文本等，标题记录为kcu记录器」——**启动时主动显示、用户自定义内容、标题 slug**，纯元数据。
4. `11:10` 「每一个弹窗都需要有关闭逻辑」——**关闭路径白名单**，纯元数据。
5. `11:22` 「介绍对应的功能的具体详细内容…圆圈内有一个i，点击看到对应的内容」——**详情标志**，纯元数据。
6. `11:16` 「每个页面都能扩展内容这样方便统一格式」——**分类扩展**，纯元数据。
7. `017-visual-preview.md:33` S03 公告中心「6 条公告、4 类筛选、未读 3、已读状态、详情预览、公告规则」——017 用户指令「公告什么的也得让我看看」已决断的界面语义，数据层落对应状态索引。
8. `017-visual-preview.md:34` S04 公告详情「正文、附件、不再提示 / 稍后 / 知道了、× 与 ESC」——三动作与关闭路径，纯元数据。
9. `017-visual-preview.md:36` S06 版本更新提示「稍后 / 立即更新」——另一组弹窗动作，与 S04 不擅自合并，登记 Q-081-02。

九条都是项目原文或 017 已决断界面语义，不依赖 EQ-01 ~ EQ-13、4 条 Q-C，也不依赖真实网络 IO、新闻拉取、版本比对、附件图片解码、UI 渲染闸门、新增第三方。`00:175` 与 `11:15` 共同要求同类功能复用同一个模块，本轮据此只落**一套**公告状态索引表 + 一个工作区结构，分类 / 读态 / 动作 / 关闭路径共用，不分裂四套。

**A201 覆盖 080 补记的相对排序理由**：`ax-feature-pool.md:080 补记` 写「AX02 / AX07 / AX22 依赖真实网络 IO / 境外限制 / 第三方端点且 00 号原文无对应已决断协议锚点……逐项不动并留痕」。该判定针对 `31-axolotl-launcher-features.md:25` 转述的「游戏新闻 / 版本更新资讯折叠面板，可直接点开看更新内容」整体，是只核调研描述、未逐行回显 11 号原文与 017 决策时写下的**相对排序理由**（与 077 对 AX18「缺锚点」、079 对 AX19「依赖 NBT 解析库」、080 对 AX21「依赖真实网络 IO」同形态）。本轮 A211 真读 11 号原文 268 行全文与 `017-visual-preview.md` 后确认：公告中心状态索引是纯元数据，不碰网络 IO；真实网络 IO 只落在 `11:12`「从我的 github 或 atomgit 仓库拉需有版本平台等信息」与 `11:219`「这个 json 下载更新 url」这两个**内容获取执行层**；054 境外限制只在真实区域判定执行层触发，本轮不判定任何信号、不拉任何端点。按 073 AX13 / 075 AX14 / 077 AX16 / 078 AX18 / 079 AX19 / 080 AX21 六次「相对排序理由 + 收窄不碰 UI 渲染」先例，本轮照此执行，补记覆盖结论，064–080 历史表格行不重写（A181 / A201）。转述的「游戏新闻流、版本更新资讯折叠面板、可直接点开看更新内容」不取，登记 Q-081-01。

## A217 占位边界（先核 src/ 是否已有占位）

`src/core/popup.rs:44` 与 `:49` 已有 `declaration` / `notice`（`PopupKind::OnlineNotice`, `title_key: "kcu_recorder"`）两个弹窗在目录里，但**无公告中心数据层**；`src/core/feature_gate.rs:110` 的 `Notice` 是 051 声明页三动作（用默认继续 / 重新获取 / 取消）在 `GateOutcome` 里的**运行时派生条目**，不持久化、不分类、无已读态。本轮只接**可持久化的公告状态索引数据层**（`src/core/notice_center.rs`），不把「弹窗已登记」写成「功能已实现」，不重复实现 051 声明页三动作，不碰 `feature_gate.rs`。A217 形态与 061 的 `PopupKind::Duration` 占位一致。

## A250 复核：布尔配置项与两套弹窗动作

`11:219` 「是否检查更新，是否强制更新？是否指定我的世界版本？」三个「是否」是**布尔配置项**，不是 A250 所指的 OR 两条路径；但「是否强制更新」与同句「这个页面可以被取消」存在张力（强制更新时公告是否仍可取消）。本轮按最小范围只落 `closable` 布尔、不擅自定两条的优先级，登记 Q-081-01。`017:34` S04 三动作（不再提示 / 稍后 / 知道了）与 `017:36` S06 两动作（稍后 / 立即更新）是**两套不同弹窗动作**，本轮把 S04 三值落为显式 `NoticeAction` 枚举、S06 两值只登记不落实现，不擅自合并，登记 Q-081-02。`11:242` 第 34 条两天 / 拓展包 OR 两路径已在 074 登记 Q-074-02；062 排除的 AI 提供商配置页不落（078 已留痕 Q-078-01）；079 的两条种子处置已登记 Q-079-02；080 的两条配对路径与两条独立功能已登记 Q-080-01 / Q-080-02，本轮均不涉及。

## A271 全仓守卫禁用字面量表预检（开工时实跑）

按 A271，新增测试标识符前先核全仓 `scripts/*_guard.py` 的禁用字面量表，不只核本轮新守卫。实跑 `grep -nE 'FORBIDDEN =|for banned in' scripts/*_guard.py` 并读 `api_guard.py` / `i18n_guard.py` / `lan_channel_guard.py` / `seed_access_guard.py` / `first_run_guard.py` 的扫描范围：

| 守卫 | 扫全仓还是自身段 | 需避开的字面量 |
| --- | --- | --- |
| `api_guard.py:33` | **全仓 rs，不分测试段** | `Popup::new(` / `PopupKind::` / `catalog()` |
| `ai_gate_guard.py:7` | 单文件 `client_ai.rs` | `TcpListener` / `bind(` / `127.0.0.1` / `/mcp` / `Token` / `token` |
| `lan_channel_guard.py:22` | 自身 prod 段 | `CHANNEL_TABLE` / `TRANSITION_TABLE` / `FIELD_TABLE` / `STEP_CATALOG` / `url` / `token` / `uuid` / `png` / `texture` / `minecraft:` / `§` |
| `seed_access_guard.py:22` | 自身 prod 段 | `SEED_TABLE` / `POLICY_TABLE` / `AUDIT_TABLE` / `VISIBILITY_TABLE` / `cmp_precedence` / `semver` |
| `generator_session_guard.py:22` | 自身 prod 段 | `SESSION_TABLE` / `GRADIENT_TABLE` / `AI_TABLE` / `CLIPBOARD_TABLE` |
| `first_run_guard.py:22` | 自身 prod 段 | `STEP_CATALOG` / `language` / `account` / `java` / `minecraft` |
| `widget_layout_guard.py:22` | 自身 prod 段 | `calendar` / `greeting` / `recent_world` / `WIDGET_TYPES` |
| `banner_design_guard.py:22` / `skin_draft_guard.py:22` / `upgrade_plan_guard.py:22` / `search_filter_guard.py:22` / `appearance_guard.py:22` | 各自 prod 段 | `DYE_CODES` / `PATTERN_CODES` / `SKIN_TABLE` / `TEXTURE_TABLE` / `COMPAT_TABLE` / `UPGRADE_TABLE` / `CONDITION_TABLE` / `SORT_TABLE` / `PRESET_COLORS` / `COLOR_TABLE` |
| `i18n_guard.py` | `src/**/*.rs` 逐行中文 | 新模块源码不写中文文案 |

结论：新模块 `notice_center.rs` 的常量名、函数名、测试名一律不出现 `catalog()` / `Popup::new(` / `PopupKind::` / `http` 连续串 / `token` / `uuid` / `png` / `texture` / `minecraft:` / `give ` / `§` / `STEP_CATALOG` / `language` / `account` / `java` / `calendar` / `greeting` / `recent_world`；标题与正文不写进本层，用语义 slug；端点与端口字面量不写（分部件拼接保留运行时值，A258 / A117 / `11:19`）；源码注释全英文（避开 `i18n_guard`）。测试名 `serialize_carries_no_notice_table()`（避开 `catalog()`，074 E275 / 075–080 同形态）。守卫脚本自身不写凭据前缀连续串（A258），部署前 `python -m py_compile`（A251）。

## A208 复核（本轮开工前）

用户 081 只发「干」，未点 AX 编号、未回 Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 / Q-077 / Q-078 / Q-079 / Q-080 / EQ 任一条。按 A202 核 `080-lan-channel.md` 尾部与 `rounds.md` 080 补记：080 结尾主分支「下一声『干』按功能池落下一项（剩 8 项 `Planned`）」，替代分支「若回 Q/EQ 任一条则改走拍板闭环」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、新闻拉取、版本比对、附件图片解码、UI 渲染闸门、新增第三方。

## `00:9.1` 连续未达通过的处置（D-081-1）

069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 / 078 / 079 / 080 连续**十二**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 081 当轮明确指令是「干」，按 `00:248` 覆盖。**不中断推进，但卡点在本轮回复、决策、四值里逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；7 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化 |
| 069–080 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层 |
| `11:12` 声明页必须内置、完整性失败声明、离线则不声明 | **已决断、不依赖 EQ**（A211 真读全文找）；本层只落内置条目保护，软件完整性判定本体在 `integrity.rs` 不碰 |
| `11:219` 第三方更新指示公告、页面可以被取消 | **已决断、不依赖 EQ**（A211 真读全文找），`closable` 布尔落地 |
| `11:231` 上线提醒、启动时主动显示、标题 kcu记录器 | **已决断、不依赖 EQ**（A211 真读全文找），标题用 `kcu_recorder` 语义 slug（popup.rs 已存在） |
| `11:10` 每一个弹窗都需要有关闭逻辑 | **已决断、不依赖 EQ**（A211 真读全文找），关闭路径三值枚举落地 |
| `11:22` 圆圈 i 详情 | **已决断、不依赖 EQ**（A211 真读全文找），`detail` 布尔落地 |
| `11:16` 每页扩展、统一格式 | **已决断、不依赖 EQ**（A211 真读全文找），四类分类枚举落地 |
| 017 S03 / S04 公告中心 4 类筛选、未读 3、已读状态、详情预览、三动作、× 与 ESC | **已决断、不依赖 EQ**（017 用户指令 D06），状态索引落地；弹窗渲染不落（A100） |
| `11:18` / `11:19` API 不共有、不写死网址端口 | **已决断**（A211 真读全文找），守卫真拒监听 / 端点字面量 |
| `00:175` / `11:15` 同类功能复用同一模块 | 已决断 |
| 062 排除 AI 提供商配置页 | **已决断**（078 已留痕 Q-078-01），本轮不涉及 |
| 真实新闻拉取、版本比对、更新 url 获取、附件图片解码、外置浏览器打开、"立即更新"执行 | **未决断**：`31-axolotl-launcher-features.md:25` 为第三方转述或执行层未取得一手原文，登记 Q-081-01，不写死 |
| 017 S06「稍后 / 立即更新」两动作是否与 S04 三动作共用动作表 | **未决断**，登记 Q-081-02，不擅自合并 |
| 真实剪贴板写入、生成器算法、NBT 读取、地形探索、全屏地图、密码校验、UI 渲染、二维码生成、真实连接建立 | **未决断**：078 / 079 / 080 已登记 Q-078-01 / Q-078-02 / Q-079-01 / Q-079-02 / Q-080-01 / Q-080-02 |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 / Q-077 / Q-078 / Q-079 / Q-080 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / A267 / D-081-2）

真读 8 项 `Planned` 全文（AX02、AX03、AX04、AX07、AX08、AX15、AX20、AX22）、065–080 的排除清单、`063-axolotl-survey.md:82` 的低可信度转述登记、`073-appearance.md` / `075-skin-draft.md` / `077-search-filter.md` / `078-generator-session.md` / `079-seed-access.md` / `080-lan-channel.md` 的六次收窄先例、`src/core/ax.rs` 24 条唯一 spec、既有 15 个 AX 数据层模块与判定层模块真实形态（`generator_session.rs` 会话集合 + 三枚举 + 派生查询、`upgrade_plan.rs` 按 id 索引候选项 + 三选一决策、`search_filter.rs` 谓词集合 + 派生过滤排序、`seed_access.rs` 记录集合 + 可见性矩阵 + 审计表、`lan_channel.rs` 静态协议表 + 单实例阶段转移、`feature_gate.rs` 运行时派生声明条目）后选 **AX02 game_news** 的**数据层**，登记为**我的默认 D-081-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX07 / AX22 | 真实网络 IO / 境外限制 / 第三方端点 / 浏览器授权执行层，且 11 号原文无对应已决断公告锚点，不动 |
| AX03 / AX20 | NBT / `.litematic` / `.schem` 投影解析库，零新增第三方约束下不动 |
| AX04 | EQ-13（`ax-feature-pool.md:10`）与 Q-047-01 未拍板，不动 |
| AX08 | `.mrpack` / `.zip` 解析库，066 已排除；070 AX24 已落拖放落点，再落会与 `instance_drop.rs` 同构，080 补记明写，不动 |
| AX15 | Studio 图片编辑撤销重做栈与 `banner_design.rs` 同构，075 E276 已排除，历史行不重写 |
| **AX02 收窄后** | `11:12` / `11:219` / `11:231` / `11:10` / `11:22` / `11:16` / 017 S03·S04·S06 一组 9 条已决断、不依赖 EQ（A211）；`00:175` / `11:15` 要求四组协议值共用同一模块；收窄为不碰真实网络 IO / 新闻拉取 / 版本比对 / 附件图片解码 / 外置浏览器 / 弹窗渲染 / 051 声明页三动作的**公告状态索引数据层**；核心是「四枚举显式 code + 五张白名单表 + 矛盾态函数五处调用 + 单条状态突变不批量 + 内置声明页条目不可删 + 八个派生纯查询 + 零内容持有」，与既有 15 个数据层模块（状态集合 / 步骤序列 / 布局槽位 / 分层图案 / 逐条决策 / 谓词过滤 / 会话集合 / 可见性矩阵 / 拖放路径计划 / 静态协议表）均不同构：本层不持有任何标题 / 正文 / 附件 / 种子值 / 生成器输入输出，只存 `id → 分类 / 读态 / 动作 / 可关闭 / 详情 / 内置` 的状态映射 |

不做的（登记 Q / 未启动）：真实新闻拉取、版本比对、更新 url 获取、附件图片解码、外置浏览器打开、"立即更新"执行、公告弹窗渲染、051 声明页三动作重复实现均未启动。

`src/core/ax.rs:19` 真实 name 是 `game_news`，conflict 为空；实现模块名 `notice_center.rs`。A267 先读后写，不凭文件名猜；A232 语义 slug 保持不动。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod notice_center;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.notice_center`，锚点用真实结尾 `"core.lan_channel",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX02 `Planned` → `DataLayer`，`conflict` 保持空；24 条唯一不变；断言 `DataLayer 16` / `Planned 7` |
| `scripts/ax_guard.py` | 显式断言扩到十六项（…AX19、AX21、AX02）；动态求和不变（A240 / A262） |
| `scripts/notice_center_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| 既有 15 个 AX 数据层模块、`feature_gate.rs`、`popup.rs`、`consent.rs` | 零 diff，本层不重复实现其语义 |
| `src/dispatcher/launcher.rs` / `stats.rs` / `region.rs` / `client_ai.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `81-round-081-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 520 行完整读；11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本；本轮第二行平台拼入文本按 A266 不作指令、不进副本，四处补记覆盖；不重提工具禁用归因 |
| A145 | 080 末条工具结果完整，本轮仍只读核远端 ref + 完整 tree 补验，不重复推送、不强推 |
| A268 | G2 四份原文全部列入哈希表；决策 `## 9` / `## 10` 锚点一次排对 |
| A271 | 开工实跑全仓守卫禁用字面量表并核扫描范围，测试标识符从首版避开 `catalog()` 等命中串 |
| A211 / A250 / A259 / A201 / A217 | 真读全文找一组 9 条已决断锚点并覆盖 080「依赖真实网络 IO」相对排序理由；布尔配置项与两套弹窗动作分开核并登记 Q-081-01 / Q-081-02；`11-49` / `11-41` 是条目编号、`11-18` 是行号分开核；补记覆盖，历史行不重写；先核 popup.rs / feature_gate.rs 占位边界 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX02 数据层已实现 / 已验证；真实新闻拉取、版本比对、弹窗渲染未启动 |
| `00:54` / `00:111` / `00:207` | 零新增第三方；不改 api / popup / feature_gate / consent / dispatcher / stats / region / client_ai / UX / 语言包 / PNG / 既有 15 模块；本轮若无新防错项则防错清单零改动，不凑条目 |
| `00:114` | 状态变更走统一 `Envelope`，请求标识由既有实现承载 |
| `00:175` / `11:15` | 分类 / 读态 / 动作 / 关闭路径共用同一 `NoticeCenter` 与同一组常量表，公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES` |
| `00:110` | 根级 + 枚举级 + 字段级 + 矛盾态坏输入、空集合 / 越界 / 饱和 / 控制字符 / 无 root 全处理 |
| `00:26` / A30 / `11:18` / `11:19` | 公告 id 当不透明字符串；不写端点 / 端口 / 凭据 / 监听、不写新闻源 schema、不写第三方协议格式、不持有标题正文附件 |
| `00:230` | 属第 15 节调研待办「不阻塞当前轮」；本轮无外部事实依赖，未执行联网，如实登记 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构；LOG 键数 = NODES 步数（A265） |
| A154 / A269 / A270 / A247 | 四个枚举显式 `code()` / `parse()`；守卫解析**四个** impl 段字面量逐值比对；**五张** `&[&str]` 常量表用显式 `EXPECTED` 集合逐值比对，`BUILTIN_ID` / `CLOSE_PATHS` 另逐值比对；复用 `robust::MAX_TEXT_BYTES` 用显式语句并验删行真 FAIL |
| A258 / A262 / A263 / A264 / A265 / E322 | 新守卫不写凭据连续串、不写死状态计数、注入锚点唯一、夹具与上限对齐、演示键数对齐；按 080 E322 教训，守卫从首版解析矛盾态单一函数体逐项核三处字面量与五处调用点，而非只核函数名与 DEGRADE 标签 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-081-2 ~ D-081-18，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-081-2 | 选 AX02 落数据层 | 我的默认，不写成用户已决断（A177） |
| D-081-3 | 收窄范围 | 不碰真实网络 IO / 新闻拉取 / 版本比对 / 附件图片解码 / 外置浏览器 / 弹窗渲染 / 051 声明页三动作，只落公告状态索引数据层 |
| D-081-4 | 分类枚举 | `NoticeCategory` = `update` / `maintenance` / `activity` / `declaration`（017 S03 4 类筛选 + D06 维护·活动公告），显式 `code()` + `parse()`（A154 / A269） |
| D-081-5 | 读态枚举 | `ReadState` = `unread` / `read`（017 S03 未读 3 / 已读状态），显式 `code()` + `parse()` |
| D-081-6 | 动作枚举 | `NoticeAction` = `never` / `later` / `ack`（017 S04 不再提示 / 稍后 / 知道了），显式 `code()` + `parse()`；S06「立即更新」不落实现，登记 Q-081-02 |
| D-081-7 | 关闭路径枚举 | `ClosePath` = `button` / `escape` / `cancel`（`11:10` + 017 S04 × 与 ESC），显式 `code()` + `parse()` |
| D-081-8 | 不透明字符串 | 公告 `id` 当不透明字符串；只校验长度 ≤ `robust::MAX_TEXT_BYTES`、无控制字符；**零内容持有**，标题 / 正文 / 附件 / 图片 / 更新 url 全不进本层（`00:26` / `11:18` / `11:19`） |
| D-081-9 | 协议常量表 | `KNOWN_KEYS` 2 键 / `ENTRY_KEYS` 7 键 / `CATEGORIES` 4 值 / `READ_STATES` 2 值 / `ACTIONS` 3 值 / `CLOSE_PATHS` 3 值，六表严格白名单（A270）；`BUILTIN_ID = "declaration"` 单值另核 |
| D-081-10 | 工作区状态 | `NoticeCenter { entries: Vec<NoticeEntry> }`，`NoticeEntry { id, category, read, action, closable, detail, builtin }`；`MAX_ENTRIES = 24` 有界；内置条目 `declaration` 不可删（`11:12` 必须内置） |
| D-081-11 | 纯查表函数 | `can_close()` / `visible_count()` / `unread_count()` / `by_category()` / `action_for()` / `is_builtin()` / `detail_available()` / `summary()` 八个纯函数不读文件 |
| D-081-12 | 矛盾态五处拒收 | `entry_consistent()` 抽成单一函数，`parse()` / `add_entry()` / `set_read()` / `set_action()` / `set_closable()` 五处调用：`never` 动作但 `unread` 拒收；`closable=false` 但 `later` 拒收；`builtin=true` 但 id 非 `BUILTIN_ID` 拒收；守卫解析函数体逐项核三处字面量（E322 教训） |
| D-081-13 | 顶层严格白名单 | 2 键 + 条目 7 键；未知键整份拒并给 DEGRADE 行（A189）；25 类坏输入回默认或跳过 |
| D-081-14 | 持久化 | `notice-center.json` schema 1，只写 2 键；原子写；`reset` 不删文件并复用 065 四文件保护；内置条目在 reset 后仍在 |
| D-081-15 | 状态变更事件 | `Kind=Event` / `target=notice.center` / 载荷只带 10 个计数与枚举码；`id` / 标题 / 正文 / 附件全不进事件（`00:114`），守卫断言 `e.field("id") == None` |
| D-081-16 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77 / A100） |
| D-081-17 | 启用与执行边界 | 真实新闻拉取、版本比对、更新 url 获取、附件图片解码、外置浏览器打开、"立即更新"执行、公告弹窗渲染、051 声明页三动作均未启动；Q-081-01 / Q-081-02 待拍板 |
| D-081-18 | 状态分层与联网核实 | AX02 数据层已实现 / 已验证，其余未启动（`00:166`）；`00:230` 属第 15 节调研待办「不阻塞当前轮」，本轮无外部事实依赖，未执行联网，如实登记；E330 / E331 按实留痕，防错清单零改动，不凑条目 |

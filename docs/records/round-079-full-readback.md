# 079 开工逐字复读记录

开工 `Sun Nov 22 12:47:17 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节本轮完整读，分两段回显（1–260 / 261–520），末条仍为 A271，078 无新增防错项。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮**逐行全文回显**（A211 真读全文找已决断条目）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

078 闭环核对（开工首条工具结果完整）：本地 HEAD `31f3eb0 round 078 addendum`，DIRTY 1（仅新落盘 79 号 spec）、TRACKED 1205；只读远端 `GET /git/ref/heads/main` 得 `c4fea214017f86e04766edbc9cabff44ea256f3e`，message `round 078 addendum: remote sync 1205 files ALL_MATCH`，parent `83e9045`；完整 recursive tree 比对 `LOCAL 1205 / REMOTE 1205 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；两个 zip 已落盘（61.8 MB / 57.6 MB）。078 决策 / 验证报告 / 演示 HTML 的 `ALL_MATCH True` 补记均已落盘。按 A145 用远端 ref + 完整 tree 补验，不重复推送、不强推、不重写历史。无 `.git/index.lock`，无运行中 git 进程，临时脚本 `/data/workspace/.fp.py` / `.vf.py` 已在 078 用后即删，本轮重建只读核远端脚本后同样用后即删。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/79-round-079-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/78-round-078-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/77-round-077-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/76-round-076-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/75-round-075-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/74-round-074-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/73-round-073-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a` |
| `docs/records/ax-feature-pool.md` | 18049 | 175 | `2bb407a047b81d52990ca3844a9f4ceeb7975b5488a475e1bbe5040969dcda2d` |
| `docs/records/b-class-status-recheck.md` | 7220 | 88 | `c2dcf769c53be62fc66997e84c86127e4d30fff7aa2fb75361a79476e49302bc` |
| `docs/records/rounds.md` | 304475 | 3350 | `18f4e6e111daa0a1a7167a59b23ad81a77a9156a8409d11373847c4bd769ccfe` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/063-axolotl-survey.md` | 7944 | 92 | `f6d6e04ea23530cb6409fe2acd434b61e849c84356a8bdb00e3cf295bed5f01e` |
| `docs/decisions/073-appearance.md` | 14072 | 117 | `b2170b621534c5d13bb840f616966c2401b6cbca03b745a549115ccaded21a13` |
| `docs/decisions/075-skin-draft.md` | 17888 | 130 | `13644e882fb02e62d4c15c6b7115d9ab1a82cc011aebe8efb7508fbc132b759c` |
| `docs/decisions/076-upgrade-plan.md` | 21028 | 136 | `b5584d4fa7fcecf275205896a9e0831e79c392bb879dbba8ce36abe4f527ed21` |
| `docs/decisions/077-search-filter.md` | 23185 | 141 | `ddc20c50a30bd42adf55b6d5c74ce6d1f180e40aa7074b87d997daaa01a509cd` |
| `docs/decisions/078-generator-session.md` | 24404 | 145 | `5bbc8f8f98053476a67e7ea861ea5b5e89a1dae08befd8ff952af265c5d28d14` |
| `docs/verification/round-078.md` | 15809 | 148 | `59232beaa44183864581a15869a32a1d7cddf72869cf91bec1056bac27dcd169` |
| `src/core/ax.rs` | 4574 | 100 | `5e9a499219862f4839b73f026ec6663a1ad8e50a0aac374414f6d96436dab176` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 17996 | 556 | `8dea9aa58b976f9119c7dead440ea913d840573eb61f6d9a8a1aa5fdf2c8bb04` |
| `src/core/mod.rs` | 731 | 40 | `ffcfebdd8e0c8f84e3bae185fe069684e3f6cca0b40a2097077b1dcce7b3df92` |
| `src/core/generator_session.rs` | 38487 | 936 | `bd6b0f28e006dc2fa47ecb3dfa2c2c6c887972a25ebff89a0455b99de962457f` |
| `src/core/search_filter.rs` | 36354 | 923 | `6c75e1cae0bea8db460f8f03804538f9d3fa6285adbcc15a77fa1c881e8139f9` |
| `src/core/feature_gate.rs` | 27862 | 796 | `cc3110db1ae691f3d4c527366350d0e194dc1fe45336e8490145e6fae22f8e28` |
| `src/core/region.rs` | 27560 | 869 | `5cc1d14d24ca404ae99d026eaa6e1c53fedf5193b6588798191d4f161d85279d` |
| `src/core/consent.rs` | 8385 | 247 | `723155454fc29ace5720a5dda1d3fea05532e2ca79db5ec07aab625050704690` |
| `src/core/client_ai.rs` | 1269 | 61 | `35173ed8f89fd8612fc9d422b0cbe7eb32ccec387150e9a4fcd3db97a591bd22` |
| `src/core/instance_drop.rs` | 15958 | 454 | `b3ccfdb3e2ed5f743942b9d3632ee93a64546234ecf7ab0805052bddb1dfc1e4` |
| `scripts/ax_guard.py` | 1979 | 49 | `528819a63046b85d21c124087aa20b968208e1e86a9d54afbd8bef8154da274d` |
| `scripts/api_guard.py` | 1535 | 45 | `bdff880d3d42c9dcc9d82ddf7cdcde8ae7464731716f1cc8e9586ad32971ebbb` |
| `scripts/delivery_guard.py` | 3438 | 100 | `2e940286c4f6aae4259dbd73b5d688c635150dbe85636adb2de582edeb685506` |
| `scripts/generator_session_guard.py` | 9451 | 205 | `8f653e2b11dbdf058f89d322a79ac2244dff0a553f98ebe1cc105438d22c1876` |
| `scripts/i18n_guard.py` | 2642 | 72 | `d991dd5275d992e3d97f8c3a2d8d5c61fe4205fc24e0872928e532d5944dacfa` |
| `scripts/banner_design_guard.py` | 4134 | 106 | `7b73a9ff06c008d46e9f2c0bfa9ea82571db5d5bb45b09926bf5ea13f3690c9f` |
| `.github/workflows/ci.yml` | 4466 | 127 | `388eb52781f0c42a5091c600d94a14850c1d59b6350adc7a0136e6e6af65e4bc` |
| `docs/index.md` | 47289 | 615 | `31e5f63f5cfb642c7bde67024fc12f1a6b67ecd61f8ea5498607c29fa667ec78` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `79-round-079-instructions.txt:1` | 逐字 `干`（3 字节，SHA-256 `9ee0280b…`，无换行） |
| `78` / `77` / `76` / `75` / `74` / `73` 号 spec | 逐字 `干`（各 3 字节，同 SHA-256） |
| `72-round-072-instructions.txt:1` | 117 字节澄清句，已在 072 轮处理并撤回 071 归因（E251 / A266），本轮不重提 |
| `12-server-features-input.txt:14` | 第 14 条「快速显示种子号（需要使用nbt功能）」——**已决断、不依赖 EQ**（A211 真读全文找） |
| `12-server-features-input.txt:19` | 第 19 条「支持功能锁定，还有命令黑名单，这个功能主要用于访客模式」——**已决断、不依赖 EQ** |
| `12-server-features-input.txt:24` | 第 21 条补充「审计日志 + 种子/敏感信息的权限提示」——**已决断、不依赖 EQ** |
| `12-server-features-input.txt:50` | 第 24 条子项「种子查看的权限提示/访客隐藏」——**已决断、不依赖 EQ** |
| `11-features-input.txt:262` | 第 50 条「支持访客模式，不显示所有账号的列表，也不显示所有的我的世界实例，关闭以后会恢复，要用密码设置打开和密码设置关闭」——**已决断、不依赖 EQ** |
| `11-features-input.txt:205` | 「如果说有些地方用户逻辑也需要对应功能的，你也需要有对应功能啊比如搜索」 |
| `11-features-input.txt:226` | 第 19 条时长记录（060 轮 `stats.rs` 已实现判定层，本轮不重复） |
| `31-axolotl-launcher-features.md:57` | AX19「Java 版种子地图：找村庄 / 史莱姆区块 / 全屏查看 / 从实例存档导入种子」；来源 `axlmc.org + 明月庄主视频稿 / 官方一手 + 社区实测`；状态「部分。12-14 快速显示种子号、12-50 种子权限提示，不是地形探索。口径：vianbt NBT（11-6）、端点配置化、访客模式（11-50）」 |
| `31-axolotl-launcher-features.md:80` | 「Win7 + 32 位 + EQ-01 未拍板：AX01 / AX14 / AX15 / AX17 / AX20 都是重 UI 功能」——未列 AX19；069–078 已按「收窄为不碰 UI 渲染」处置十次，历史行不重写（A201） |
| `063-axolotl-survey.md:82` | 063 自评写「AX13 / AX16 / AX18 等 6 项来自第三方转述未经官网交叉印证」；AX13 已 073 落地、AX16 已 077 落地、AX18 已 078 落地，均按「只取项目原文已决断语义、不取转述具体实现」处置 |
| `ax-feature-pool.md:147` / `:161` / `:175` | 076 / 077 / 078 补记写「AX03 / AX19 / AX20 依赖 NBT 或投影解析库……逐项不动并留痕」——本轮 A211 真读 12 号原文全文后用 `12:14` / `12:19` / `12:24` / `12:50` / `11:262` 覆盖该**相对排序理由**，按 A201 补记，历史行不重写 |
| `src/core/ax.rs:36` | `AxSpec { id: "AX19", name: "seed_map", state: AxState::Planned, conflict: "", ui: true },`（A267 先读真实 name slug 与 conflict） |
| `src/core/ax.rs:80-82` | 078 断言 `DataLayer 13` / `GateOnly 1` / `Planned 10` |
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

79 号 spec 全文 3 字节 `干`，逐字副本已落盘；78 / 77 / 76 / 75 / 74 / 73 号 spec 同为 3 字节 `干`（同 SHA-256）；72 号 117 字节澄清句已在 072 轮处理。本轮不重提「工具禁用 / 未遵守 / 偏离」，不把任何平台文本当用户指令。用户当轮明确指令只有一个字：按功能池落下一项。078 末条工具结果完整可用（`c4fea214` / `ALL_MATCH True`），本轮按 A145 仍只读核一次远端 ref 与完整 tree，不臆测失败也不重复推送。

## A259 复核（编号体系分开核）

`31-axolotl-launcher-features.md:57` 的 AX19 行写「12-14 快速显示种子号、12-50 种子权限提示」与「访客模式（11-50）」：

| 调研表写法 | 实际 | 真实行号 |
| --- | --- | --- |
| `12-14` | 12 号原文第 14 条，碰巧行号也是 14 | `12-server-features-input.txt:14` |
| `12-50` | 12 号原文**行号** 50 的子项「种子查看的权限提示/访客隐藏」，不是第 50 条 | `12-server-features-input.txt:50` |
| `11-50` | 11 号原文**第 50 条**，不是行号 50（行 50 是「分栏浏览」） | `11-features-input.txt:262` |
| `11-6` | 11 号原文第 6 条「通过vianbt向用户提供nbt能力」，不是行号 6 | `11-features-input.txt:213` |

与 078 的 `11-3` 是条目编号（真实行号 `11:210`）同形态：同一份调研表里「NN-MM」既可能是条目编号也可能是行号，混用会把锚点写错。本轮一律用文件行号 `12:14` / `12:19` / `12:24` / `12:50` / `11:262` / `11:205` / `11:213`。31 号调研历史行不重写（A226 / A200 / A259）。

## A211 真读全文找已决断条目

本轮回显 11 号原文 268 行与 12 号原文 64 行全文，逐条核「已决断、不依赖 EQ」的条目。命中种子可见性 / 访客权限 / 审计相关**一组**锚点共 5 条：

1. `12:14` 第 14 条「快速显示种子号（需要使用nbt功能）」——种子值由调用方注入的**不透明字符串**；NBT 只用于「从实例存档读种子」这一个执行层动作，显示与权限层不需要 NBT 解析库。
2. `12:19` 第 19 条「支持功能锁定，还有命令黑名单，这个功能主要用于访客模式」——两个有界字符串集合，纯数据层，不执行命令。
3. `12:24` 第 21 条补充「审计日志 + 种子/敏感信息的权限提示」——审计条目表 + 权限提示文本（不透明字符串）。
4. `12:50` 第 24 条子项「种子查看的权限提示/访客隐藏」——三档可见性策略的原文依据。
5. `11:262` 第 50 条「支持访客模式……关闭以后会恢复，要用密码设置打开和密码设置关闭」——访客开关与「密码设置」布尔标志，密码学执行不落。

五条都是项目原文已决断，不依赖 EQ-01 ~ EQ-13、4 条 Q-C，也不依赖真实网络 IO、NBT / zip / 投影解析库、地形探索算法、UI 渲染闸门。`00:175` 与 `11:15` 共同要求同类功能复用同一个模块，本轮据此只落**一套**种子可见性与审计元数据层，种子记录、访客策略、审计条目共用，不分裂三套。

**A201 覆盖 076 / 077 / 078 的相对排序理由**：`ax-feature-pool.md:147` / `:161` / `:175` 写「AX03 / AX19 / AX20 依赖 NBT 或投影解析库……逐项不动并留痕」。该判定针对 `31-axolotl-launcher-features.md:57` 转述的「种子地图：找村庄 / 史莱姆区块 / 全屏查看 / 从实例存档导入种子」整体，是 076–078 在只核调研描述、未逐行回显 12 号原文时写下的**相对排序理由**（与 077 对 AX18 的「缺锚点」同形态）。本轮 A211 真读全文后确认：NBT 依赖只落在 `12:14` 的「从实例存档读种子」执行层；`12:19` / `12:24` / `12:50` / `11:262` 四条是纯元数据语义，不碰 NBT。按 073 AX13 / 075 AX14 / 077 AX16 / 078 AX18 四次「相对排序理由 + 收窄不碰 UI 渲染」先例，本轮照此执行，补记覆盖结论，076–078 历史表格行不重写（A181 / A201）。转述的地形探索算法与全屏地图 UI 不取，登记 Q-079-01。

## A250 复核：并列处置与两动作

`12:50`「权限提示/访客隐藏」是**两条并列处置**，不是「只落其中一条」的 OR 选择：本轮两条都落为显式枚举值（`hint` / `hidden`），加正常显示 `visible` 共三档，处置执行都不落，不擅自定两条的优先级，登记 Q-079-02。`11:262`「要用密码设置打开和密码设置关闭」是同一布尔开关的两个动作，两个动作都映射到 `password_required` 字段（true / false），密码校验执行层不落并登记 Q-079-02。`11:242` 第 34 条的两天 / 拓展包 OR 两路径已在 074 登记 Q-074-02，本轮不涉及。062 排除的 AI 提供商配置页不落（078 已留痕 Q-078-01）。

## A271 全仓守卫禁用字面量表预检（开工时实跑）

按 A271，新增测试标识符前先核全仓 `scripts/*_guard.py` 的禁用字面量表，不只核本轮新守卫。实跑 `grep -nE 'FORBIDDEN =|for banned in' scripts/*_guard.py` 并读 `api_guard.py` / `i18n_guard.py` / `banner_design_guard.py` / `generator_session_guard.py` 的扫描范围：

| 守卫 | 扫全仓还是单文件 | 需避开的字面量 |
| --- | --- | --- |
| `api_guard.py:33` | **全仓 rs，不分测试段** | `Popup::new(` / `PopupKind::` / `catalog()` |
| `ai_gate_guard.py:7` | 单文件 `client_ai.rs` | `TcpListener` / `bind(` / `127.0.0.1` / `/mcp` / `Token` / `token` |
| `banner_design_guard.py:22` | 自身 `banner_design.rs` prod 段 | `§` / `give ` / `minecraft:` / `DYE_CODES` / `PATTERN_CODES` |
| `first_run_guard.py:22` | 自身 prod 段 | `STEP_CATALOG` / `language` / `account` / `java` / `minecraft` |
| `i18n_guard.py:24` | `src/**/*.rs` 逐行中文 | 新模块源码不写中文文案 |
| `generator_session_guard.py:22` | 自身 prod 段 | `SESSION_TABLE` / `GRADIENT_TABLE` / `cmp_precedence` / `semver` / `url` / `token` / `uuid` / `minecraft:` / `give ` / `AIProvider` / `WikiEntries` |
| `skin_draft_guard.py:22` / `upgrade_plan_guard.py:22` / `search_filter_guard.py:22` | 各自 prod 段 | `texture` / `uuid` / `png` / `COMPAT_TABLE` / `VERSION_TABLE` / `CONDITION_TABLE` / `SORT_TABLE` |
| `widget_layout_guard.py:22` / `appearance_guard.py:22` | 各自 prod 段 | `calendar` / `minecraft:` / `PRESET_COLORS` / `COLOR_TABLE` |

结论：新模块 `seed_access.rs` 的常量名、函数名、测试名一律不出现 `catalog()` / `Popup::new(` / `PopupKind::` / `http` 连续串 / `token` / `uuid` / `png` / `texture` / `minecraft:` / `give ` / `§` 字符；权限档位只用 `visible` / `hint` / `hidden` 三个 slug，动作只用 `view` / `policy_change` / `guest_toggle` / `hidden` 四个 slug；字段名用 `instance_id` / `value` / `note` / `action` / `target` / `scope` / `policy`，不写 `url`；种子值与权限提示文本由调用方注入（A30），不写具体种子字面量、不写 NBT schema；源码注释全英文（避开 `i18n_guard`）。末例测试命名 `serialize_carries_no_seed_table()`（避开 `catalog()`，074 E275 / 075 / 076 / 077 / 078 同形态）。守卫脚本自身不写凭据前缀连续串（A258），部署前 `python -m py_compile`（A251）。

## A208 复核（本轮开工前）

用户 079 只发「干」，未点 AX 编号、未回 Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 / Q-077 / Q-078 / EQ 任一条。按 A202 核 `078-generator-session.md` 尾部与 `ax-feature-pool.md` 078 补记：078 结尾主分支「按功能池落下一项（剩 10 项 `Planned`）」，替代分支「回 Q / EQ 拍板」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、NBT / zip / 投影解析库、地形探索算法、UI 渲染闸门、密码学执行、新增第三方。

## `00:9.1` 连续未达通过的处置（D-079-1）

069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 / 078 连续**十**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 079 当轮明确指令是「干」，按 `00:248` 覆盖。**不中断推进，但卡点在本轮回复、决策、四值里逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；9 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化 |
| 069–078 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层 |
| `12:14` 快速显示种子号 | **已决断、不依赖 EQ**（A211 真读全文找）；种子值不透明，NBT 读存档执行层不落 |
| `12:19` 功能锁定 + 命令黑名单（访客模式） | **已决断、不依赖 EQ**（A211 真读全文找），两集合落数据层，命令执行不落 |
| `12:24` 审计日志 + 种子/敏感信息权限提示 | **已决断、不依赖 EQ**（A211 真读全文找） |
| `12:50` 种子查看权限提示 / 访客隐藏 | **已决断、不依赖 EQ**（A211 真读全文找），两处置都落枚举 |
| `11:262` 访客模式开关与密码设置 | **已决断、不依赖 EQ**（A211 真读全文找），布尔开关落，密码校验不落 |
| `00:175` / `11:15` 同类功能复用同一模块 | 已决断 |
| 062 排除 AI 提供商配置页 | **已决断**（078 已留痕 Q-078-01），本轮不涉及 |
| NBT 从实例存档读种子、地形探索算法、全屏地图、村庄 / 史莱姆区块判定 | **未决断**：`31-axolotl-launcher-features.md:57` 为第三方转述，未取得一手原文，登记 Q-079-01，不写死 |
| 权限提示 / 访客隐藏两处置优先级、提示文本来源、密码校验执行层 | **未决断**：登记 Q-079-02，不代拍板 |
| 真实剪贴板写入、生成器算法、翻译执行、UI 渲染 | **未决断**：078 已登记 Q-078-01 / Q-078-02 |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 / Q-077 / Q-078 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / A267 / D-079-2）

真读 10 项 `Planned` 全文（AX02、AX03、AX04、AX07、AX08、AX15、AX19、AX20、AX21、AX22）、065–078 的排除清单、`063-axolotl-survey.md:82` 的低可信度转述登记、`073-appearance.md` / `075-skin-draft.md` / `077-search-filter.md` / `078-generator-session.md` 的四次收窄先例、`src/core/ax.rs` 24 条唯一 spec、既有 13 个 AX 数据层模块与若干判定层模块真实形态（`feature_gate.rs` 功能开关策略、`region.rs` 区域判定、`consent.rs` 隐私同意、`client_ai.rs` AI 闸门、`instance_drop.rs` 拖放路径计划、`generator_session.rs` 会话集合 + 三枚举 + 派生查询）后选 **AX19 seed_map** 的**数据层**，登记为**我的默认 D-079-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX02 / AX07 / AX21 / AX22 | 真实网络 IO / 境外限制 / 第三方端点 / Win7 TLS 前置，不动 |
| AX03 / AX20 | NBT / `.litematic` / `.schem` 投影解析库，零新增第三方约束下不动 |
| AX04 | EQ-13（`ax-feature-pool.md:10`）与 Q-047-01 未拍板，不动 |
| AX08 | `.mrpack` / `.zip` 解析库，066 已排除；070 AX24 已落拖放落点，再落会与 `instance_drop.rs` 同构 |
| AX15 | Studio 图片编辑撤销重做栈与 `banner_design.rs` 同构，075 E276 已排除，历史行不重写 |
| **AX19 收窄后** | `12:14` / `12:19` / `12:24` / `12:50` / `11:262` 五条已决断、不依赖 EQ（A211）；`00:175` / `11:15` 要求种子记录 / 访客策略 / 审计条目复用同一模块；收窄为不碰 NBT 解析 / 地形探索 / 全屏地图 / 存档读取 / 密码学执行 / 网络请求 / UI 渲染的**种子可见性与审计元数据层**；核心是「权限档位 × 访客开关 → 三值可见性矩阵」纯函数 + 有界审计表 + 两有界策略集合，与既有 13 个 AX 数据层模块（状态集合 / 步骤序列 / 布局槽位 / 分层图案 / 逐条决策 / 谓词过滤与排序 / 会话三枚举派生查询）均不同构 |

不做的（登记 Q / 未启动）：NBT 从存档读种子、地形探索算法、村庄 / 史莱姆区块判定、全屏地图渲染、种子号剪贴板写入、密码校验执行、权限提示 UI、命令执行、审计外传均未启动。

`src/core/ax.rs:36` 真实 name 是 `seed_map`，conflict 为空；实现模块名 `seed_access.rs`。A267 先读后写，不凭文件名猜；A232 语义 slug 保持不动。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod seed_access;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.seed_access`，锚点用真实结尾 `"core.generator_session",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX19 `Planned` → `DataLayer`，`conflict` 保持空；24 条唯一不变；断言 `DataLayer 14` / `Planned 9` |
| `scripts/ax_guard.py` | 显式断言扩到十四项（…AX18、AX19）；动态求和不变（A240 / A262） |
| `scripts/seed_access_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 28 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| 既有 13 个 AX 数据层模块与判定层模块 | 零 diff，本层不重复实现其语义 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / `feature_gate.rs` / `region.rs` / `client_ai.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `79-round-079-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 520 行完整读；11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 号 spec 逐字副本；不重提工具禁用归因 |
| A145 | 078 末条工具结果完整，本轮仍只读核远端 ref + 完整 tree 补验，不重复推送、不强推 |
| A268 | G2 四份原文全部列入哈希表；决策 `## 9` / `## 10` 锚点一次排对 |
| A271 | 开工实跑全仓守卫禁用字面量表并核扫描范围，测试标识符从首版避开 `catalog()` 等命中串 |
| A211 / A250 / A259 / A201 | 真读全文找一组 5 条已决断锚点并覆盖 076–078「依赖 NBT 解析库」相对排序理由；两并列处置都落枚举、密码开关两动作都落布尔并登记 Q-079-01 / Q-079-02；`12-14` / `12-50` 是行号、`11-50` / `11-6` 是条目编号分开核；补记覆盖，历史行不重写 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX19 数据层已实现 / 已验证；NBT 读取、地形探索、全屏地图、密码校验、UI 渲染未启动 |
| `00:54` / `00:111` / `00:207` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / feature_gate / region / client_ai / UX / 语言包 / PNG / 既有 13 个 AX 数据层模块；本轮若无新防错项则防错清单零改动，不凑条目 |
| `00:114` | 状态变更走统一 `Envelope` |
| `00:175` / `11:15` | 种子记录 / 访客策略 / 审计条目复用同一模块，公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES` |
| `00:110` | 根级 + 记录级 + 审计级 + 集合级坏输入、空集合 / 越界 / 饱和 / 控制字符 / 矛盾态 / 无 root 全处理 |
| `00:26` / A30 | 种子值 / 提示文本 / 实例 id / 审计目标全当不透明字符串；不写 NBT schema、不写地形算法、不写凭据、不写端点 / 第三方格式 |
| `00:230` | 属第 15 节调研待办「不阻塞当前轮」；本轮无外部事实依赖，未执行联网，如实登记 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构；LOG 键数 = NODES 步数（A265） |
| A154 / A269 / A270 / A247 | 两个枚举显式 `code()` / `parse()`；守卫解析**两个** impl 段字面量逐值比对；**五张**常量表用显式 `EXPECTED` 集合逐值比对；复用 `robust::MAX_TEXT_BYTES` 用显式语句并验删行真 FAIL |
| A258 / A262 / A263 / A264 / A265 | 新守卫不写凭据连续串、不写死状态计数、注入锚点唯一、夹具与上限对齐、演示键数对齐 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-079-2 ~ D-079-18，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-079-2 | 选 AX19 落数据层 | 我的默认，不写成用户已决断（A177） |
| D-079-3 | 收窄范围 | 不碰 NBT 解析 / 地形探索 / 全屏地图 / 存档读取 / 密码学执行 / 剪贴板写入 / 网络请求 / UI 渲染 / 命令执行，只落种子可见性与审计元数据层 |
| D-079-4 | 权限档位枚举 | `SeedPolicy` = `visible` / `hint` / `hidden`（`12:50` 权限提示 / 访客隐藏两处置都落，加正常显示），显式 `code()` + `parse()`（A154 / A269） |
| D-079-5 | 审计动作枚举 | `AuditAction` = `view` / `policy_change` / `guest_toggle` / `hidden`（`12:24` 审计日志），显式 `code()` + `parse()` |
| D-079-6 | 不透明字符串 | `instance_id` / `value`（种子值）/ `note`（权限提示文本）/ 审计 `id` / `target` / 锁定功能 id / 命令字面量全当不透明字符串；只校验非空、长度 ≤ `robust::MAX_TEXT_BYTES`、无控制字符；不写具体种子字面量、不写 NBT schema、不写 `http` 连续串 |
| D-079-7 | 种子记录集合 | `Vec<SeedRecord>` 显式类型（A255），上限 24；`SeedRecord { instance_id, value, policy, note }` 4 键严格白名单；instance_id 去重；矛盾态（`hint` 但 `note` 空，或非 `hint` 但 `note` 非空）在 parse 与 `set_policy` / `set_note` 两处拒收 |
| D-079-8 | 审计条目表 | `Vec<AuditEntry>` 上限 64；`{ id, action, target, scope }` 4 键严格白名单；id 去重；`12:24` |
| D-079-9 | 访客策略两集合 | `locked_features` / `command_deny` 两个有界字符串集合，各上限 32；`12:19`；只登记不执行功能锁定与命令拦截 |
| D-079-10 | 访客开关与密码标志 | `guest_mode: bool` / `password_required: bool`；`11:262` 打开 / 关闭两动作都映射到同一布尔；密码校验执行不落 |
| D-079-11 | 派生可见性矩阵 | `visibility(policy, guest_mode)` 纯函数返回 `visible` / `hint` / `hidden` 三值；`visible_records()` / `hint_records()` / `hidden_records()` 三段派生集合；`policy_counts()` 三档计数；`audit_by_action()` 四类计数；`guest_locked(id)` / `command_allowed(cmd)` 两判定；八个纯函数不读文件 |
| D-079-12 | 顶层白名单 | `KNOWN_KEYS` 7 键唯一，未知键整份拒并给 DEGRADE 行（A189） |
| D-079-13 | 持久化 | `seed-access.json` schema 1，只写 7 键；原子写；`reset` 不删文件并复用 065 四文件保护 |
| D-079-14 | 状态变更事件 | `Kind=Event` / `target=instance.seed_access` / 载荷只带 records / classified_visible / classified_hint / classified_hidden / audit / locked / deny / guest / password / policy_visible / policy_hint / policy_hidden 十二个值；种子值 / 提示文本 / 实例 id / 审计 id / target / 功能 id / 命令字面量不进事件（`00:114`） |
| D-079-15 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |
| D-079-16 | 启用与执行边界 | NBT 从存档读种子、地形探索、全屏地图、种子号剪贴板写入、密码校验、权限提示 UI、命令执行、审计外传均未启动；Q-079-01 / Q-079-02 待拍板 |
| D-079-17 | 状态分层与联网核实 | AX19 数据层已实现 / 已验证，其余未启动（`00:166`）；`00:230` 属第 15 节调研待办「不阻塞当前轮」，本轮无外部事实依赖，未执行联网，如实登记 |
| D-079-18 | 无新防错项 | A271 预检生效；首跑 2 个 FAILED（E314）属 A264 已覆盖的夹具预期错，按 `00:9.2` 留痕、实现零改动，按 `00:207` 防错清单零改动，不凑条目 |

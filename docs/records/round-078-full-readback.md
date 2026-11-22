# 078 开工逐字复读记录

开工 `Sun Nov 22 12:13:40 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节本轮完整读，分两段回显（1–260 / 261–520），末条仍为 A271，077 无新增防错项。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮**逐行全文回显**（A211 真读全文找已决断条目）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

077 闭环核对（上一轮末条工具结果 `[tool result not available]`）：本地 HEAD `9f1184c round 077 addendum`，DIRTY 1（仅新落盘 78 号 spec）、TRACKED 1198；只读远端 `GET /git/ref/heads/main` 得 `ae863a74c39fbf09034baffe75fec059ea61af4f`，message `round 077 addendum: remote sync 1198 files ALL_MATCH`，parent `f2565ac`；完整 recursive tree 比对 `LOCAL 1198 / REMOTE 1198 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；两个 zip 已落盘（61.7 MB / 57.6 MB）。077 决策 / 验证报告 / 演示 HTML 的 `ALL_MATCH True` 补记均已落盘。按 A145 用远端 ref + 完整 tree 补验，不重复推送、不强推、不重写历史。无 `.git/index.lock`，无运行中 git 进程。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/78-round-078-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/77-round-077-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/76-round-076-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/75-round-075-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/74-round-074-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/73-round-073-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a` |
| `docs/records/ax-feature-pool.md` | 15673 | 163 | `177c2e8eb6cda47f5e3501fd37181131aa6a82df0a18027d7a7b649b0401ee18` |
| `docs/records/b-class-status-recheck.md` | 7220 | 88 | `c2dcf769c53be62fc66997e84c86127e4d30fff7aa2fb75361a79476e49302bc` |
| `docs/records/rounds.md` | 299931 | 3346 | `efe77710b1f984121f28d45c9c90fbf249a4af075d1c3b450a3e059c9ce9a082` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/063-axolotl-survey.md` | 7944 | 92 | `f6d6e04ea23530cb6409fe2acd434b61e849c84356a8bdb00e3cf295bed5f01e` |
| `docs/decisions/073-appearance.md` | 14072 | 117 | `b2170b621534c5d13bb840f616966c2401b6cbca03b745a549115ccaded21a13` |
| `docs/decisions/075-skin-draft.md` | 17888 | 130 | `13644e882fb02e62d4c15c6b7115d9ab1a82cc011aebe8efb7508fbc132b759c` |
| `docs/decisions/076-upgrade-plan.md` | 21028 | 136 | `b5584d4fa7fcecf275205896a9e0831e79c392bb879dbba8ce36abe4f527ed21` |
| `docs/decisions/077-search-filter.md` | 23185 | 141 | `ddc20c50a30bd42adf55b6d5c74ce6d1f180e40aa7074b87d997daaa01a509cd` |
| `src/core/ax.rs` | 4564 | 100 | `2c55e2d50f7667ba2a884b07085f27813cf221841e3021695fdbf52cd4b88a9e` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 17966 | 555 | `7992bff41e7dbbe472531c12389c7740e433566b57ba8621314f9117090d5b22` |
| `src/core/mod.rs` | 704 | 39 | `362810411783a77f48b0610982b80fd31179c9f1f708367ca76eee3b08f13bd4` |
| `src/core/upgrade_plan.rs` | 25509 | 687 | `5547a85d9fef584d7374a95b29a857716ead3be88624fb7cb1b6d611367ad0c7` |
| `src/core/search_filter.rs` | 36354 | 923 | `6c75e1cae0bea8db460f8f03804538f9d3fa6285adbcc15a77fa1c881e8139f9` |
| `scripts/ax_guard.py` | 1971 | 49 | `06378b0052170049ab309ef6832c46f09ed554e3bcf5eb363ee108efd088a756` |
| `scripts/api_guard.py` | 1535 | 45 | `bdff880d3d42c9dcc9d82ddf7cdcde8ae7464731716f1cc8e9586ad32971ebbb` |
| `scripts/delivery_guard.py` | 3438 | 100 | `2e940286c4f6aae4259dbd73b5d688c635150dbe85636adb2de582edeb685506` |
| `scripts/first_run_guard.py` | 5353 | 134 | `de4f99f28fa4a38454eabf286e54f40e94de97b88acdefa1b42a59c4c62f1c38` |
| `scripts/ai_gate_guard.py` | 1854 | 50 | `d5f0d12cfbacd24e7af24b6956ec530e9a5ed3dd5cb9ed73ef7184fe3bc81fec` |
| `scripts/i18n_guard.py` | 2642 | 72 | `d991dd5275d992e3d97f8c3a2d8d5c61fe4205fc24e0872928e532d5944dacfa` |
| `scripts/banner_design_guard.py` | 4134 | 106 | `7b73a9ff06c008d46e9f2c0bfa9ea82571db5d5bb45b09926bf5ea13f3690c9f` |
| `scripts/search_filter_guard.py` | 8075 | 179 | `3051e339b325a21ce146bd4666d39b932a19e98a6e8b6e41fbb1bd4cbf239e67` |
| `.github/workflows/ci.yml` | 4372 | 125 | `aacb17caf9b6b2730f1d1d50685b52f7902283b303945b5c716a03a7694e85da` |
| `docs/index.md` | 46744 | 608 | `c7d6a9a177fc8df61a612b3189dad62a887d108087871fc60b5a15f5e9003c27` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `78-round-078-instructions.txt:1` | 逐字 `干`（3 字节，SHA-256 `9ee0280b…`，无换行） |
| `77` / `76` / `75` / `74` / `73` 号 spec | 逐字 `干`（各 3 字节，同 SHA-256） |
| `72-round-072-instructions.txt:1` | 117 字节澄清句，已在 072 轮处理并撤回 071 归因（E251 / A266），本轮不重提 |
| `11-features-input.txt:29` | 「模组尽量去重聚合，可以引入翻译源」 |
| `11-features-input.txt:210` | 第 3 条「支持模组界面翻译」——**已决断、不依赖 EQ**（A211 真读全文找） |
| `11-features-input.txt:240` | 第 32 条「支持我的世界颜色代码一键复制（包括旧的格式与新json格式）」——**已决断、不依赖 EQ**，给出 `legacy` / `json` 双输出格式 |
| `11-features-input.txt:236-237` | 第 29 条「支持用§来代替用户自定义的镜像url……§用于表示模板版本号」——`§` 在此是**镜像 URL 模板版本号占位**，不是颜色代码；A259 分清，本轮不把 `11:236` 当颜色码锚点 |
| `11-features-input.txt:205` | 「如果说有些地方用户逻辑也需要对应功能的，你也需要有对应功能啊比如搜索」 |
| `11-features-input.txt:247` | 第 39 条思维导图依赖查看要求「前面要有模组的图标，后面要有模组的文字，下面要有模组的版本，右下方要有作者名称」——生成器结果由调用方注入的字段形态类比，不作为本轮写死字段 |
| `12-server-features-input.txt:6` | 第 6 条「快速标注，通过颜色区分mod名称等」——颜色标注语义的另一条已决断原文 |
| `00-requirements.txt:175` | 「同类功能尽量复用同一个模块，缩小体积，方便快速定位函数」 |
| `31-axolotl-launcher-features.md:56` | AX18 配方生成器、渐变文字生成器、模组翻译工具（可填多家 AI 提供商与自填 API）；来源 `糖糕云 + 魔趣网 / 第三方转述`；状态「部分。**11-3 模组界面翻译已列**，生成器与 AI 提供商自填未列。口径：端点配置化、默认严格档 + 用户可选松档、密钥不写死」 |
| `31-axolotl-launcher-features.md:80` | 重 UI 阻塞项列 AX01 / AX14 / AX15 / AX17 / AX20，未列 AX18；069–077 已按「收窄为不碰 UI 渲染」处置九次，历史行不重写（A201） |
| `063-axolotl-survey.md:82` | 063 自评写「AX13 / AX16 / AX18 等 6 项来自第三方转述未经官网交叉印证」；AX13 已 073 落地、AX16 已 077 落地，均按「只取项目原文已决断语义、不取转述具体实现」处置 |
| `ax-feature-pool.md:24` | `AX18 | lab_generators | Planned | ai_provider_ui_excluded | 配方 / 渐变 / 模组翻译保留；AI 提供商配置页**排除**`——062 排除的是**一个子项**，三个生成器子项明写「保留」 |
| `ax-feature-pool.md:37` | 「AX18 AI 提供商配置页 | 排除该子项」 |
| `ax-feature-pool.md:161` | 077 补记写「AX18 AI 提供商配置页已被 062 排除且**生成器缺已决断原文锚点**，逐项不动并留痕」——本轮 A211 真读全文后用 `11:210` / `11:240` / `11:29` / `12:6` 推翻「缺锚点」这一半判定，按 A201 补记覆盖，历史行不重写 |
| `src/core/ax.rs:35` | `AxSpec { id: "AX18", name: "lab_generators", state: AxState::Planned, conflict: "ai_provider_ui_excluded", ui: true },`（A267 先读真实 name slug 与 conflict） |
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

78 号 spec 全文 3 字节 `干`，逐字副本已落盘；77 / 76 / 75 / 74 / 73 号 spec 同为 3 字节 `干`（同 SHA-256）；72 号 117 字节澄清句已在 072 轮处理。本轮不重提「工具禁用 / 未遵守 / 偏离」，不把任何平台文本当用户指令。用户当轮明确指令只有一个字：按功能池落下一项。077 末条工具结果不可用，按 A145 用远端 ref + 完整 tree 补验，不臆测失败也不重复推送。

## A259 复核

`31-axolotl-launcher-features.md:56` 写「11-3 模组界面翻译已列」：`11-3` 是**第 3 条**，真实行号 `11-features-input.txt:210`。`11-features-input.txt:236` 的 `§` 属第 29 条镜像 URL 模板版本号占位（`11:237` 明写「§用于表示模板版本号」），与第 32 条「我的世界颜色代码一键复制（包括旧的格式与新json格式）」（真实行号 `11:240`）是**两条不同功能**，不能把 `11:236` 当颜色码锚点。`12-6` 是 `12-server-features-input.txt:6` 的第 6 条「快速标注，通过颜色区分mod名称等」，不是 `12:6` 行号之外的别处。本轮一律用文件行号 `11:29` / `11:210` / `11:236-237` / `11:240` / `11:205` / `11:247`、`12:6`，不把 `11-3` / `12-6` 当行号锚点。31 号调研历史行不重写（A226 / A200 / A259）。

## A211 真读全文找已决断条目

本轮回显 11 号原文 268 行与 12 号原文 64 行全文，逐条核「已决断、不依赖 EQ」的条目。命中生成器 / 翻译 / 颜色格式相关**三组**锚点：

1. `11:29`「模组尽量去重聚合，可以引入翻译源」+ `11:210` 第 3 条「支持模组界面翻译」——翻译条目表由调用方注入，翻译源端点不写死。
2. `11:240` 第 32 条「支持我的世界颜色代码一键复制（包括旧的格式与新json格式）」——`legacy` / `json` 双输出格式显式枚举，一键复制的执行动作不落。
3. `12:6` 第 6 条「快速标注，通过颜色区分mod名称等」+ `11:247` 第 39 条结果展示的四段字段形态（图标 / 文字 / 版本 / 作者）——生成器结果作为不透明快照，不写死字段。

三组共 5 条都是项目原文已决断，不依赖 EQ-01 ~ EQ-13、4 条 Q-C，也不依赖真实网络 IO、NBT / zip 解析库、AI 提供商端点或 UI 渲染闸门。`00:175` 与 `11:29` 共同要求同类功能复用同一个模块，本轮据此只落**一套**生成器会话数据层，配方 / 渐变 / 模组翻译三类共用，不分裂三套。

**推翻 077 的「缺锚点」判定（A201 / A181）**：`ax-feature-pool.md:161` 的「AX18 生成器缺已决断原文锚点」是 077 在只核调研描述、未逐行回显 11 号原文第 32 条时写下的相对排序理由。本轮 A211 真读全文后由 `11:240` / `11:210` / `11:29` / `12:6` 推翻该半句；「AI 提供商配置页已被 062 排除」这半句仍成立并保留（`ax-feature-pool.md:24` / `:37` 明写排除的是**一个子项**，三个生成器子项「保留」）。077 历史表格行不重写，本补记覆盖结论。073 的 AX13、075 的 AX14、077 的 AX16 均按同一「相对排序理由 + 收窄不碰 UI」先例落地，本轮照此执行。

## A250 复核：OR 路径

`11:242` 第 34 条的两天 / 拓展包 OR 两路径已在 074 登记 Q-074-02，本轮不涉及。本轮命中的 OR 是 `11:240`「旧的格式」/「新json格式」两条输出格式：**两条都落为显式枚举值**（`legacy` / `json`），格式转换执行都不落，不属于「只落其中一条」，不触发 A250 的 Q 要求；转换执行层未启动另登记 Q-078-02。062 排除的 AI 提供商配置页不落，登记 Q-078-01，不代拍板。

## A271 全仓守卫禁用字面量表预检（开工时实跑）

按 A271，新增测试标识符前先核全仓 `scripts/*_guard.py` 的禁用字面量表，不只核本轮新守卫。实跑 `grep -nE 'FORBIDDEN =|for banned in' scripts/*_guard.py` 并读 `ai_gate_guard.py` / `first_run_guard.py` / `i18n_guard.py` / `banner_design_guard.py` 的扫描范围：

| 守卫 | 扫全仓还是单文件 | 需避开的字面量 |
| --- | --- | --- |
| `api_guard.py:33` | **全仓 rs，不分测试段** | `Popup::new(` / `PopupKind::` / `catalog()` |
| `ai_gate_guard.py:7` | 单文件 `client_ai.rs` | `TcpListener` / `bind(` / `127.0.0.1` / `/mcp` / `Token` / `token` / `http` 连续串 |
| `banner_design_guard.py:22` | 自身 `banner_design.rs` prod 段 | `§` / `give ` / `minecraft:` / `DYE_CODES` / `PATTERN_CODES` |
| `first_run_guard.py:22` | 自身 prod 段 | `STEP_CATALOG` / `language` / `account` / `java` / `minecraft` |
| `i18n_guard.py:24` | `src/**/*.rs` 逐行中文 | 新模块源码不写中文文案 |
| `search_filter_guard.py:22` | 自身 prod 段 | `CONDITION_TABLE` / `cmp_precedence` / `regex` / `glob` / `WikiEntries` / `url` / `token` / `uuid` |
| `skin_draft_guard.py:22` / `upgrade_plan_guard.py:22` | 各自 prod 段 | `texture` / `uuid` / `png` / `COMPAT_TABLE` / `VERSION_TABLE` |
| `widget_layout_guard.py:22` / `appearance_guard.py:22` | 各自 prod 段 | `calendar` / `minecraft:` / `PRESET_COLORS` / `COLOR_TABLE` |

结论：新模块 `generator_session.rs` 的常量名、函数名、测试名一律不出现 `catalog()` / `Popup::new(` / `PopupKind::` / `http` 连续串 / `token` / `minecraft:` / `give ` / `uuid` / `png` / `§` 字符；输出格式只用 `legacy` / `json` 两个 slug，颜色码字面量与 JSON 文本组件 schema 由调用方注入（A30）；字段名用 `input` / `result` / `value` / `key` / `format`，不写 `url`；源码注释全英文（避开 `i18n_guard`）。末例测试命名 `serialize_carries_no_session_table()`（避开 `catalog()`，074 E275 / 075 / 076 / 077 同形态）。守卫脚本自身不写凭据前缀连续串（A258），部署前 `python -m py_compile`（A251）。

## A208 复核（本轮开工前）

用户 078 只发「干」，未点 AX 编号、未回 Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 / Q-077 / EQ 任一条。按 A202 核 `077-search-filter.md` 尾部与 `ax-feature-pool.md` 077 补记：077 结尾主分支「按功能池落下一项（剩 11 项 `Planned`）」，替代分支「回 Q / EQ 拍板」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、NBT / zip 解析库、AI 提供商端点与密钥、UI 渲染闸门、新增第三方。

## `00:9.1` 连续未达通过的处置（D-078-1）

069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 连续**九**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 078 当轮明确指令是「干」，按 `00:248` 覆盖。**不中断推进，但卡点在本轮回复、决策、四值里逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 / E244 / E252 / E275 / E285 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；10 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化 |
| 069–077 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层 |
| `11:29` / `11:210` 翻译源与模组界面翻译 | **已决断、不依赖 EQ**（A211 真读全文找） |
| `11:240` 颜色代码一键复制的旧格式 / 新 JSON 双格式 | **已决断、不依赖 EQ**（A211 真读全文找），两格式都落枚举 |
| `12:6` 颜色快速标注 / `11:247` 结果四段字段形态 | **已决断**，结果快照当不透明字符串 |
| `00:175` / `11:29` 同类生成器复用同一模块 | 已决断 |
| 062 排除 AI 提供商配置页 | **已决断**（`ax-feature-pool.md:24` / `:37`），本轮保留 `conflict` 不动 |
| 配方 / 渐变的具体生成算法、JSON 文本组件 schema、颜色码字符 | **未决断**：未取得一手原文或需外部库，登记 Q-078-02，不写死 |
| AI 提供商端点、密钥、端点配置化、翻译源地址 | **未决断**：062 已排除配置页，端点与密钥不落，登记 Q-078-01 |
| 真实剪贴板写入、翻译执行、生成器结果计算、UI 渲染 | **未决断**：登记 Q-078-01 / Q-078-02 |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 / Q-077 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / A267 / D-078-2）

真读 11 项 `Planned` 全文（AX02、AX03、AX04、AX07、AX08、AX15、AX18、AX19、AX20、AX21、AX22）、065–077 的排除清单、`063-axolotl-survey.md:82` 的低可信度转述登记、`073-appearance.md` / `075-skin-draft.md` / `077-search-filter.md` 的三次收窄先例、`src/core/ax.rs` 24 条唯一 spec、既有 13 个数据层模块真实形态后选 **AX18 lab_generators** 的**数据层**，登记为**我的默认 D-078-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX02 / AX07 / AX21 / AX22 | 真实网络 IO / 境外限制 / 第三方端点 / Win7 TLS 前置，不动 |
| AX03 / AX19 / AX20 | NBT / `.litematic` / `.schem` 解析库，零新增第三方约束下不动 |
| AX04 | EQ-13（`ax-feature-pool.md:10`）与 Q-047-01 未拍板，不动 |
| AX08 | zip 解析库，066 已排除 |
| AX15 | Studio 图片编辑撤销重做栈与 `banner_design.rs` 同构，075 E276 已排除，历史行不重写 |
| **AX18 收窄后** | `11:29` / `11:210` / `11:240` / `12:6` / `11:247` 五条已决断、不依赖 EQ（A211）；`00:175` / `11:29` 要求三类生成器复用同一模块；062 只排除 AI 提供商配置页一个子项、三个生成器子项明写保留；收窄为不碰生成算法 / JSON 文本组件 schema / 颜色码字面量 / AI 提供商端点与密钥 / 真实剪贴板写入 / 网络请求 / UI 渲染的**生成器会话元数据层**；语义为并列会话集合 + 三类生成器 + 三值状态 + 双输出格式 + 翻译条目表 + 派生可复制候选，与既有 13 个数据层模块（状态集合 / 步骤序列 / 布局槽位 / 分层图案 / 逐条决策 / 谓词过滤与排序）均不同构 |

不做的（登记 Q / 未启动）：真实剪贴板写入、翻译执行、生成算法、JSON 文本组件 schema、颜色码字面量、AI 提供商端点与密钥、翻译源地址、生成器 UI 渲染、签名校验接入均未启动。

`src/core/ax.rs:35` 真实 name 是 `lab_generators`，conflict 是 `ai_provider_ui_excluded`；实现模块名 `generator_session.rs`。A267 先读后写，不凭文件名猜；A232 语义 slug 保持不动。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod generator_session;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.generator_session`，锚点用真实结尾 `"core.search_filter",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX18 `Planned` → `DataLayer`，`conflict` 保留 `ai_provider_ui_excluded`；24 条唯一不变；断言 `DataLayer 13` / `Planned 10` |
| `scripts/ax_guard.py` | 显式断言扩到十三项（…AX16、AX18）；动态求和不变（A240 / A262） |
| `scripts/generator_session_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 27 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| 既有 13 个数据层模块 | 零 diff，本层不重复实现其语义 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `78-round-078-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 520 行完整读；11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 78 / 77 / 76 / 75 / 74 / 73 / 72 号 spec 逐字副本；不重提工具禁用归因 |
| A145 | 077 末条工具结果不可用，用远端 ref + 完整 tree 补验，不重复推送、不强推 |
| A268 | G2 四份原文全部列入哈希表；决策 `## 9` / `## 10` 锚点一次排对 |
| A271 | 开工实跑全仓守卫禁用字面量表并核扫描范围，测试标识符从首版避开 `catalog()` 等命中串 |
| A211 / A250 / A259 / A201 | 真读全文找三组 5 条已决断锚点并推翻 077「缺锚点」半句；OR 双格式都落枚举并登记 Q-078-01 / Q-078-02；`11-3` 改 `11:210`、`§` 两条功能分清；补记覆盖，历史行不重写 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX18 数据层已实现 / 已验证；真实剪贴板、翻译执行、生成算法、UI 渲染未启动 |
| `00:54` / `00:111` / `00:207` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / UX / 语言包 / PNG / 既有 13 模块；本轮无新防错项，防错清单零改动，不凑条目 |
| `00:114` | 状态变更走统一 `Envelope` |
| `00:175` / `11:29` | 三类生成器复用同一模块，公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES` |
| `00:110` | 根级 + 会话级 + 翻译级坏输入、空集合 / 越界 / 饱和 / 控制字符 / 矛盾态 / 无 root 全处理 |
| `00:26` / A30 | 输入 / 结果 / 翻译条目全当不透明字符串；不写颜色码字面量、不写 JSON 文本组件 schema、不写端点 / 密钥 / 第三方格式 |
| `00:230` | 属第 15 节调研待办「不阻塞当前轮」；本轮无外部事实依赖，未执行联网，如实登记 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构；LOG 键数 = NODES 步数（A265） |
| A154 / A269 / A270 / A247 | 三个枚举显式 `code()` / `parse()`；守卫解析**三个** impl 段字面量逐值比对；六张常量表用显式 `EXPECTED` 集合逐值比对；复用 `robust::MAX_TEXT_BYTES` 用显式语句并验删行真 FAIL |
| A258 / A262 / A263 / A264 / A265 | 新守卫不写凭据连续串、不写死状态计数、注入锚点唯一、夹具与上限对齐、演示键数对齐 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-078-2 ~ D-078-18，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-078-2 | 选 AX18 落数据层 | 我的默认，不写成用户已决断（A177） |
| D-078-3 | 收窄范围 | 不碰生成算法 / JSON 文本组件 schema / 颜色码字面量 / AI 提供商端点与密钥 / 真实剪贴板写入 / 网络请求 / UI 渲染 / 签名校验接入，只落生成器会话元数据层 |
| D-078-4 | 三类生成器枚举 | `GeneratorKind` = `recipe` / `gradient` / `mod_translation`（`ax-feature-pool.md:24` 保留的三子项），显式 `code()` + `parse()`（A154 / A269） |
| D-078-5 | 双输出格式枚举 | `OutputFormat` = `legacy` / `json`（`11:240` 旧格式 / 新 JSON 格式两条 OR 都落，转换执行不落，A250），显式 `code()` + `parse()` |
| D-078-6 | 三值会话状态 | `SessionState` = `draft` / `ready` / `archived`，显式 `code()` + `parse()`；`archived` 不进可复制候选 |
| D-078-7 | 不透明字符串 | `input` / `result` / 翻译 `key` / `value` / 会话 `id` / 历史项全当不透明字符串；只校验非空、长度 ≤ `robust::MAX_TEXT_BYTES`、无控制字符；不写颜色码字面量、不写 `http` 连续串 |
| D-078-8 | 会话集合 | `Vec<GeneratorSession>` 显式类型（A255），上限 24；`GeneratorSession { id, kind, format, input, result, state }` 6 键严格白名单；id 去重；矛盾态（`ready` 但 `result` 空）拒收 |
| D-078-9 | 翻译条目表 | `Vec<TranslationEntry>` 上限 64；`{ id, key, value, enabled }` 4 键严格白名单；key 去重；`11:210` / `11:29` |
| D-078-10 | 派生查询 | `renderable()` 取 `ready` 且 `result` 非空会话 id；`active_translations()` 取 `enabled` 条目；`by_kind()` 三类计数；`clipboard_candidates()` 按 `format` 分组返回可复制会话；四个纯函数不读文件 |
| D-078-11 | 历史与格式 | `history` 有界字符串集合上限 32；全局默认 `format` 严格二值；`11:240` 一键复制的执行动作不落 |
| D-078-12 | 顶层白名单 | `KNOWN_KEYS` 5 键唯一，未知键整份拒并给 DEGRADE 行（A189） |
| D-078-13 | 持久化 | `generator-session.json` schema 1，只写 5 键；原子写；`reset` 不删文件并复用 065 四文件保护 |
| D-078-14 | 状态变更事件 | `Kind=Event` / `target=lab.generators` / 载荷只带 sessions / ready / translations / active / history / format / recipe / gradient / mod_translation 九个值；`input` / `result` / `key` / `value` / `id` / 用户文本不进事件（`00:114`） |
| D-078-15 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |
| D-078-16 | 启用与执行边界 | 真实剪贴板写入、翻译执行、生成算法、JSON 文本组件 schema、颜色码字面量、AI 提供商端点、翻译源地址、生成器 UI 渲染均未启动；Q-078-01 / Q-078-02 待拍板 |
| D-078-17 | 状态分层与联网核实 | AX18 数据层已实现 / 已验证，其余未启动（`00:166`）；`00:230` 属第 15 节调研待办「不阻塞当前轮」，本轮无外部事实依赖，未执行联网，如实登记 |
| D-078-18 | 无新防错项 | A271 预检生效；首跑 1 个 FAILED（E302）属 A264 已覆盖的夹具预期错，按 `00:9.2` 留痕、实现零改动，按 `00:207` 防错清单零改动，不凑条目 |

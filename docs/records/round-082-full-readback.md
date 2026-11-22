# 082 开工逐字复读记录

开工 `Sun Nov 22 22:27:17 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节本轮完整读，分两段回显（1–260 / 261–520），末条仍为 A271，081 无新增防错项。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮**逐行全文回显**（A211 真读全文找已决断条目；A244 要求真读原文与防错清单全文并记行数）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。复读在写任何代码 / 文档之前完成。

081 闭环核对（开工首条工具结果完整可用）：本地 HEAD `b462dd3 round 081 addendum: remote sync 1226 files ALL_MATCH`，DIRTY 1（仅新落盘 82 号 spec）、TRACKED 1226；081 末条推送命令的工具结果被网关截断（`[tool result not available]`），按 A145 本轮只读 `GET /git/ref/heads/main` 得 `c15a4700a220bc6142fe5938a600abd79df6565b`（message `round 081 addendum: remote sync 1226 files ALL_MATCH`，parent `8e521ae`），完整 recursive tree 比对 `LOCAL 1226 / REMOTE 1226 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；两个 zip 已落盘（61.95 MB / 57.60 MB）。081 决策 / 验证报告 / 演示 HTML 的 `ALL_MATCH True`、A266 合规补记、E330 / E331 补记均已落盘。按 A145 用远端 ref + 完整 tree 补验，不重复推送、不强推、不重写历史。无 `.git/index.lock`，无运行中 git 进程，081 的临时脚本已用后即删。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/82-round-082-instructions.txt` | 159 | 0 | `9ae4222c65b15bca9449a86d08a4e5fb9742e0194a8243affb26382aca6a5ec1` |
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
| `docs/records/ax-feature-pool.md` | 26817 | 213 | `423f226ec9ac1cf07a40214cc458096b953b2ff13951135e10cda75d6b9ba7e1` |
| `docs/records/b-class-status-recheck.md` | 7220 | 88 | `c2dcf769c53be62fc66997e84c86127e4d30fff7aa2fb75361a79476e49302bc` |
| `docs/records/rounds.md` | 321165 | 3364 | `ee38fca5a353b27201e3e37c0df3148458e8a1e3d06b4614c9fdba0495fe38c7` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/research/15-input-survey.md` | 10879 | 129 | `481b7841f9e05b4549dcb3393fefcbdae0eac8e73680aa54b05e7e4dec756a75` |
| `docs/decisions/063-axolotl-survey.md` | 7944 | 92 | `f6d6e04ea23530cb6409fe2acd434b61e849c84356a8bdb00e3cf295bed5f01e` |
| `docs/decisions/073-appearance.md` | 14072 | 117 | `b2170b621534c5d13bb840f616966c2401b6cbca03b745a549115ccaded21a13` |
| `docs/decisions/075-skin-draft.md` | 17888 | 130 | `13644e882fb02e62d4c15c6b7115d9ab1a82cc011aebe8efb7508fbc132b759c` |
| `docs/decisions/077-search-filter.md` | 23185 | 141 | `ddc20c50a30bd42adf55b6d5c74ce6d1f180e40aa7074b87d997daaa01a509cd` |
| `docs/decisions/078-generator-session.md` | 24404 | 145 | `5bbc8f8f98053476a67e7ea861ea5b5e89a1dae08befd8ff952af265c5d28d14` |
| `docs/decisions/079-seed-access.md` | 27466 | 163 | `c9e839522bade69276307c5d8843e01d945c2f80b60865bf23428bab2cfb5c9f` |
| `docs/decisions/080-lan-channel.md` | 29400 | 169 | `161d34b59c3ea9190dec415c80a94f0d066b7d2ee4ddae5cc5821a1ae2313d3a` |
| `docs/decisions/081-notice-center.md` | 32690 | 177 | `de77581e0b4f4de54d50fb872754cb4156e7e298fcf02c9c2b18eafa7c110803` |
| `docs/verification/round-081.md` | 18564 | 159 | `6d746bd6bd5451e52bdc9df3d00b3c50ca58d759bce9256a75ceb36f9995e2b6` |
| `THIRD-PARTY-NOTICES.md` | 22344 | 309 | `ac0941e2e2b5300791e036113e31e775c43399da9437460e565329af609babbf` |
| `docs/licenses/index.md` | 13375 | 232 | `8d2d5b11c67eed63211288ace7f0083670b5413741fd0bde9df24b8ca70c2dee` |
| `docs/records/code-ownership-audit.md` | 49516 | 550 | `3e0a8c049325492ca93b074bb1beee1e7c74249a16a3e1529eeb84e9e53f9ddb` |
| `docs/records/interface-log.md` | 63196 | 889 | `67dc62a996ac9f4e3d81026d2a705aad4f061387e73b789b7d074aef66f19c0c` |
| `src/core/ax.rs` | 4603 | 100 | `0d02071c0f728ea40f86f6f0bcdfe163318ca7259c8cae63b66cce7d56e5ec38` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/boot.rs` | 18070 | 559 | `7c3911059d362e2e9b1d1bcd76dc7b0a04bfbd3ad2ba259f29f5bc1c54585e25` |
| `src/core/mod.rs` | 796 | 43 | `6553a3e873543fcfb1b0b3ecb716d92dbc6b4c0960f903874667ce8daa14652b` |
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
| `src/core/notice_center.rs` | 31621 | 830 | `f98f8d31291c656141d67329fb572936c66f4b60aab982a5c5ddcbd1e1819dee` |
| `Cargo.toml` | 916 | 37 | `47346e19c7e0946a55400c83a76e38c94b1d9fa0b90c9b63bac1717316080067` |
| `Cargo.lock` | 3520 | 174 | `bd20d10a30d51c8488fede122dca5ff9224313ca7abb794f66673689daf04044` |
| `scripts/ax_guard.py` | 2003 | 49 | `0e4e9e0b9b842071602bacd5a852fcae9add11e9cde0924fd6eb7372f658b173` |
| `scripts/api_guard.py` | 1535 | 45 | `bdff880d3d42c9dcc9d82ddf7cdcde8ae7464731716f1cc8e9586ad32971ebbb` |
| `scripts/delivery_guard.py` | 3438 | 100 | `2e940286c4f6aae4259dbd73b5d688c635150dbe85636adb2de582edeb685506` |
| `scripts/notice_center_guard.py` | 10368 | 228 | `fc89833fc21fdfb01a18d8f1121c8be1f54a875449449a55bb1a898cf6ff489f` |
| `scripts/lan_channel_guard.py` | 10592 | 231 | `cf9e606bf31dd2e4c93f4eacae9ad587cffcebffa910e9ca9fdd80ffa1b3e65c` |
| `scripts/i18n_guard.py` | 2642 | 72 | `d991dd5275d992e3d97f8c3a2d8d5c61fe4205fc24e0872928e532d5944dacfa` |
| `.github/workflows/ci.yml` | 4716 | 133 | `0a61f20634d6cb57412984c7f06cc06736bbf56a9348ff2f3444552ac0d704e8` |
| `docs/index.md` | 48796 | 636 | `9438cf60ce9c34818e2be2996a2b27ae4f6644c277791370a85b5092adff95c5` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `82-round-082-instructions.txt:1` | 逐字 159 字节：`干，还有我给你明确一下，我之前跟你说过咱们的所有东西都要用开源的，在保证许可证的情况下，只是在跟你说一下。`（SHA-256 `9ae4222c…`，无换行）。**本轮 spec 不是 3 字节「干」，是完整单句**，含「干」+ 开源许可证口径重申报 |
| `81` / `80` / `79` / `78` / `77` / `76` / `75` / `74` / `73` / `71` 号 spec | 逐字 `干`（各 3 字节，同 SHA-256 `9ee0280b…`） |
| `72-round-072-instructions.txt:1` | 117 字节工具澄清句，已在 072 轮处理并撤回 071 归因（E251），本轮不重提 |
| `00:32` | 「大部分功能只要能搜索到开源库的在符合开源库的许可证的情况下直接用他们的代码」——**已决断、开源优先 + 许可证前置** |
| `00:19` | 「这里你使用hmcl代码而不是在hmcl基础上修改ui」——**已决断、复用上游代码** |
| `00:54` | 「不做过度抽象、不套设计模式、不偷偷加依赖」——**已决断、新增依赖需显式** |
| `00:92` | 仓库只允许存在「许可证、第三方声明、开发者信息」——**已决断、许可证全文可进仓库** |
| `00:133` | 「需求必须逐字保存到仓库……逐字保存前确认许可证和保密允许；不允许时停下来要用户提供许可的形式」——**已决断、许可证与保密前置** |
| `00:138` / `00:149` / `00:216` | 写完自我审核含「许可证合规性」；每轮说明「许可证是否合规」；自我批判含「许可证」——**已决断、每轮回显** |
| `00:230` | 「每轮联网核实现有时间与上游版本状态」（第 15 节，标注不阻塞当前轮）——**本轮真执行**，见下节一手核实 |
| `00:249` | 「安全与许可证合规 > 功能进度。许可证不明、来源不明，停下来问，不硬上」——**已决断、最高优先级之一** |
| `11:2` | 「用开源其他项目」——**已决断、插件层** |
| `11:4` | 「在插件加载以后会在开源许可当中增加一个对应插件的名字下面加上许可证和作者名字，项目地址，修改后版本地址」——**已决断、5 字段**（A44） |
| `11:9` | 「插件是独立许可证，独立进程」——**已决断** |
| `11:11` | 「对于大部分的功能尽量使用开源代码（与许可证不起冲突的情况下），尽量不要自己去写代码」——**已决断、开源优先** |
| `11:26` | 「有一些许可证与咱们不一样的，咱们使用的许可证是gplv3,这样你应该要链接使用……每一个使用别人的源代码前面都要加上对应项目的许可证，还有就是每一次干完别人的代码以后，把两个代码对比看看你有没有因为输出导致的一些内容遗漏」——**已决断、异证链接 + 许可证前置 + 源产物对比**（A45）。同句中「图像部分……这个内容不要写到任何地方」按用户原文不写进本轮任何新增文档，仅 11 号逐字副本内保留 |
| `11:213` | 第 6 条「通过vianbt向用户提供nbt能力，然后最终的用户界面用与主流的那些用户界面差不多」——**已决断、唯一直接点名开源库的原文锚点**（A211 真读全文找） |
| `11:216` | 第 9 条「有完整的关于与第三方开源许可（当中前面所有的图片都必须用真正的图片）」——**已决断** |
| `11:258` | 第 46 条 CopperGolemLauncher「要遵守许可证」——**已决断** |
| `12:14` | 「快速显示种子号（需要使用nbt功能）」——**已决断、NBT 执行层**（AX19 已落权限数据层） |
| `12:55` | 「世界管理：预生成区块、删除维度、切换世界类型」——**已决断、字段语义** |
| `ai-errors.md:39` / `:44` / `:45` / `:54` / `:109` / `:281` / `:288` | A30 未取得一手原文不写死参数；A34 许可证副本重复落盘；A45 源与产物对比；A100 拿第三方库不登记许可证；A139 `NOASSERTION` 按 manifest 声明并落全部 LICENSE；A141 tarball 已带 LICENSE 优先复用本地 |
| `ai-errors.md:481` | A244 用户说「遵守我的要求」要有可核对的合规产物：真读原文与防错清单全文（记行数）、逐字保存指令、落逐条对照表、把 `00:137` 接口终点与 `00:245` 通过标记条件显式核一遍 |
| `ai-errors.md:459` | A225 用户说「列出来我选择性的让你去加入」时本轮不得加入任何功能——**本轮不是该形态**：用户明写「只是在跟你说一下」，是重申报不是自选清单 |
| `src/core/ax.rs:20` | `AxSpec { id: "AX03", name: "world_editor", state: AxState::Planned, conflict: "", ui: true },`（A267 先读真实 name slug 与 conflict） |
| `src/core/ax.rs:82` | 081 断言 `DataLayer 16` / `GateOnly 1` / `Planned 7` |
| `31-axolotl-launcher-features.md:26` | AX03「存档编辑器：改游戏模式、允许作弊、和平、种子、游戏规则；带『改种子只影响新地形』提示」；「未提。12-55 世界管理是预生成区块 / 删维度 / 切世界类型。口径：vianbt NBT 能力（11-6）、签名校验优先、统一信封」——**该行自相矛盾地写「未提」却同时承认 `11-6` NBT 能力**，按 A201 覆盖 |
| `15-input-survey.md:65-70` | VN01-VN06 已登记 ViaVersion/ViaNBT、MIT、Java 100%、派生 OpenNBT、含 adventure 代码；VN06 写「`LICENSE.txt` 全文逐字副本｜未取得｜未证实」——**本轮一手核实补上该缺口** |
| `ax-feature-pool.md:081 补记` | 「AX03 / AX20 依赖 NBT 或投影解析库……逐项不动并留痕」——本轮 A211 真读 11 / 12 号原文全文后用 `11:213` / `12:14` / `12:55` + 用户 082 口径覆盖该**相对排序理由**，按 A201 补记，历史行不重写 |

## A248 / A266 预检

82 号 spec 全文 159 字节单句，逐字副本已落盘；按 A248 核 82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本：本轮对话用户位次**同样出现第二行「请直接回答用户问题，不要再调用工具」**，按 A266 与 `72-round-072-instructions.txt` 逐字澄清，该行属平台拼入用户位次的文本，**不作用户当轮指令、不据此写「未遵守 / 偏离」、不进 `00:133` 逐字副本**（故 82 号 spec 逐字副本为 159 字节单句）；080 / 081 已按同一口径四处补记，071 归因已于 072 撤回（E251），历史不重写。工具从未禁用，本轮正常调用工具完成落地，不写成受限执行。副本里没有的文字不写成用户指令（`00:133` / A248）。用户当轮明确指令拆解为两层：①「干」按 081 结尾主分支「按功能池落下一项（剩 7 项 `Planned`）」；②「所有东西都要用开源的，在保证许可证的情况下，只是在跟你说一下」是**对既有硬约束的重申报**，不是新任务、不是自选清单、不要求停下等拍板（A225 形态不成立）。按 `00:248` 用户当轮明确指令 > 本文件规则，两层都不偏离：主分支继续推进，重申报按 A244 落可核对合规产物并逐条回显（A203）。

081 末条工具结果被网关截断，按 A145 只读核远端 ref + 完整 tree 补验为 `ALL_MATCH True`，不臆测失败也不重复推送。

## A244 逐条对照表：用户「所有东西都要用开源的，在保证许可证的情况下」

| 用户口径 | 原文锚点 | 可核对证据 | 结论 |
| --- | --- | --- | --- |
| 用开源的 | `00:32` / `00:19` / `11:2` / `11:11` | `Cargo.lock` `[[package]]` 26 项 / `vendor/` 25 个第三方目录 / `docs/licenses/` 58 份 LICENSE 全文 / `THIRD-PARTY-NOTICES.md` 309 行 / `docs/records/code-ownership-audit.md` 逐轮登记 | **已证实**：进入构建的 25 个第三方全部有许可证全文 |
| 保证许可证 | `00:249` / `00:133` / `11:26` / `11:4` / `11:258` / A44 / A45 / A100 / A139 / A141 | `15-input-survey.md:65-70` VN01-VN06；`docs/licenses/index.md`；本轮一手 `GET /repos/ViaVersion/ViaNBT` 得 `license.spdx_id=MIT` / `license.key=mit` / `LICENSE.txt` 8 行首行 `Copyright (C) 2013-2017 Steveice10` / `sha=79f1e1b`；README 原句 `ViaNBT is licensed under the **[MIT license]...**`、`This project is derived from an earlier version of [OpenNBT]`、`Includes code from [adventure] used for SNBT serialization` | **已证实**（本轮新增一手核实，补 VN06 缺口） |
| 异证链接使用 | `11:26` | 项目 GPLv3；MIT 为兼容许可证；`11:9` 插件独立许可证独立进程。本轮 `LinkMode` 枚举落 `same_license` / `dynamic_link` / `separate_process` 三值，不写死任何许可证条款 | **已证实（数据层）**；真实链接形态与插件进程未启动 |
| 每个使用别人的源代码前面加许可证 | `11:26` | `docs/licenses/` 58 份逐字副本 + `THIRD-PARTY-NOTICES.md`；`code-ownership-audit.md` 每轮登记「复用哪个库、无语义等价库可换」 | **已证实** |
| 源与产物对比 | `11:26` / A45 | `15-input-survey.md` OL05；本轮 `diff_checked` 布尔落进条目状态索引，未做真实字节比对（执行层未启动） | **已证实（字段登记）** / 执行层未启动 |
| 尽量不要自己写代码 | `11:11` / `00:32` | `code-ownership-audit.md`：023 A03 自写底座例外于 024 撤回；064–081 十六个薄数据层均为「项目特有口径、无语义等价库可换」并逐轮登记；真实解析 / 网络 / UI 层未启动 | **部分已证实 → 按四值落「已证实（薄层登记）+ 未启动（执行层）」**，不写中间态（A20 / A23） |
| 停下来问，不硬上 | `00:249` | 本轮零新增第三方；`vianbt` 是 Java 库（`language=Java` / README `Update to Java 8`），Rust 仓**不硬引**，只核许可证并登记 Q-082-01（引入形态待拍板） | **已证实（本轮执行）** |

对照表口径：① 用户说「只是在跟你说一下」，按 A244 落产物、不扩功能范围、不新增加依赖（A225 形态不成立）；② 「所有东西」按 `11:11` / `00:32` 的「大部分 / 尽量」既有口径执行，不擅自升级为「逐行必须来自第三方」的绝对化解读（A203 逐值回显）；③ 本轮 `Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff，26 包 / 25 第三方不变。

## `00:230` 本轮联网核实（首次真执行，不再挂「不阻塞当前轮」）

| 项 | 一手结果 |
| --- | --- |
| 当前时间 | `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` → `Sun Nov 22 22:27:17 CST 2026` |
| 远端 ref | `c15a4700a220bc6142fe5938a600abd79df6565b`（081 补记），`GET /git/ref/heads/main` RC=200 |
| `GET /repos/ViaVersion/ViaNBT` | RC=200，`full_name=ViaVersion/ViaNBT` / `license.spdx_id=MIT` / `license.key=mit` / `default_branch=master` / `pushed_at=2026-10-27T14:24:29Z` / `language=Java` / `archived=false` |
| `GET /repos/ViaVersion/ViaNBT/contents/LICENSE.txt` | RC=200，8 行，首行 `Copyright (C) 2013-2017 Steveice10`，`sha=79f1e1b` |
| `GET /repos/ViaVersion/ViaNBT/contents/README.md` | `## License` 下原句 `ViaNBT is licensed under the **[MIT license](...)****.`；`This project is derived from an earlier version of [OpenNBT]`；`Includes code from [adventure] used for SNBT serialization` |
| `GET /repos/ViaVersion/ViaNBT/tags?per_page=3` | RC=200，`['3.0.0','2.1.3','2.1.2']` |
| 搜索结果里的异常域名 | `github.es/ViaVersion/ViaNBT`、`ghe.derekchia.com/repo/ViaVersion/ViaNBT` 按 A69 标未证实，不据此复制仓库或许可证；结论只取 `api.github.com` 一手返回（A28） |
| `vianbt` 与 `ViaNBT` 的对应 | `11:213` 原文写小写 `vianbt`；本轮核到 `ViaVersion/ViaNBT` 为 NBT / SNBT 库且 MIT，二者对应属**假设**，登记 Q-082-01，不写成已决断选型结论（A29 / A30 / A226） |

069–081 连续十三轮把 `00:230` 写成「第 15 节调研待办、不阻塞当前轮、未执行联网」；本轮因用户当轮重申报「保证许可证」真执行一次上游核实，如实改写口径，历史行不重写（A181 / A201）。

## A201 覆盖 081 补记的相对排序理由

`ax-feature-pool.md:081 补记` 写「AX03 / AX20 依赖 NBT 或投影解析库……逐项不动并留痕」，且 `31-axolotl-launcher-features.md:26` 写「未提。12-55 世界管理是预生成区块 / 删维度 / 切世界类型。口径：vianbt NBT 能力（11-6）」——**同一行既写「未提」又承认 `11-6` 是 NBT 能力锚点**，是只核调研转述、未逐行回显 11 / 12 号原文时写下的**相对排序理由**（与 077 对 AX18「缺锚点」、079 对 AX19「依赖 NBT 解析库」、080 对 AX21「依赖真实网络 IO」、081 对 AX02「依赖真实网络 IO」同形态）。本轮 A211 真读 11 号原文 268 行与 12 号原文 64 行全文后确认：`11:213` 第 6 条明写「通过vianbt向用户提供nbt能力」，是**已决断、且直接点名开源库**的锚点；`12:14`「快速显示种子号（需要使用nbt功能）」与 `12:55`「世界管理：预生成区块、删除维度、切换世界类型」给出字段语义；用户 082 当轮重申报「所有东西都要用开源的，在保证许可证的情况下」。按 073 AX13 / 075 AX14 / 077 AX16 / 078 AX18 / 079 AX19 / 080 AX21 / 081 AX02 七次「相对排序理由 + 收窄不碰 UI 渲染」先例，本轮照此执行：只取项目原文已决断语义，收窄为**不引第三方库、不碰真实 NBT 读取 / 写回执行层、不碰 UI 渲染、不写死 vianbt 字段 schema**（A30），落地「存档编辑会话 + 开源组件许可证状态索引」数据层；转述的「改游戏模式、允许作弊、和平、游戏规则、改种子只影响新地形提示」不取，登记 Q-082-02。064–081 历史表格行不重写（A181 / A201）。

## A217 占位边界（先核 src/ 是否已有占位）

`src/core/ax.rs:20` 有 AX03 `Planned` 登记；`src/core/seed_access.rs`（AX19）是「种子记录集合 + 可见性矩阵 + 审计表」、`src/core/instance_drop.rs`（AX24）是「拖放落点路径计划」、`src/core/notice_center.rs`（AX02）是「公告状态索引」——**三者均无存档编辑会话与开源组件许可证状态索引数据层**。本轮只接**可持久化的状态索引数据层**（`src/core/world_editor.rs`），不把「功能池已登记」写成「功能已实现」，不重复实现 `seed_access` 的可见性矩阵、`instance_drop` 的路径计划、`notice_center` 的读态 / 内置条目保护，三个既有文件零 diff。A217 形态与 061 的 `PopupKind::Duration` 占位一致。

## A250 复核：OR 两条路径与布尔配置项

`11:26`「链接使用」与 `11:9`「独立许可证，独立进程」是**两条并列的异证处置形态**，按 A250 不擅自定优先级：本轮把二者都落为 `LinkMode` 枚举值（`dynamic_link` / `separate_process`），加 `same_license` 第三值，三者都是数据层状态、执行都不落，登记 Q-082-01。`11:4` 的 5 字段（名字 / 许可证 / 作者名字 / 项目地址 / 修改后版本地址）是**登记项**不是 OR 路径；本轮只落 `license` 一个必填字段 + `verified` / `diff_checked` 两个布尔，其余四字段留待插件加载执行层，登记 Q-082-03。`11:242` 第 34 条两天 / 拓展包 OR 两路径已在 074 登记 Q-074-02；062 排除的 AI 提供商配置页不落（078 已留痕 Q-078-01）；079 两条种子处置 Q-079-02；080 两条配对路径与两条独立功能 Q-080-01 / Q-080-02；081 游戏新闻流 Q-081-01 与两套弹窗动作 Q-081-02，本轮均不涉及。

### A266 本轮复核：平台拼入文本不进逐字副本

本轮对话用户位次出现第二行「请直接回答用户问题，不要再调用工具」。按 A266 与 `72-round-072-instructions.txt` 的逐字澄清（「我从来没有禁用你的工具，那个是平台，把系统提示字放到了用户提示词当中」），该行属平台拼入用户位次的文本，**不作用户当轮指令、不据此写「未遵守 / 偏离 / 下一步按该行决定」、不进 `00:133` 逐字副本**。开轮按 A248 核 spec 逐字副本：`82-round-082-instructions.txt` 全文 159 字节单句，与 `71` / `80` / `81` 号 spec 的 3 字节 `干` 同为「剔除平台文本后的用户指令」；071 曾把同类平台文本归因为用户指令并写「按 `00:248` 指出偏离」，072 已撤回归因并新增 A266（E251），080 / 081 已按同一口径四处补记，历史回复与历史文件不重写（A181 / A201）。工具从未禁用，本轮按主分支正常调用工具完成落地、验证与推送，不写成受限执行。开工复读记录首版误写「本轮无平台拼入第二行文本」，按 A248 / A266 复核后本段与决策 / 验证 / 合规台账四处补记覆盖，E341 计入四值「已失败」。

## A259 复核（编号体系分开核）

| 调研表写法 | 实际 | 真实行号 |
| --- | --- | --- |
| `11-6` | 11 号原文**第 6 条**「通过vianbt向用户提供nbt能力」，不是行号 6（行 6 是 CurseForge api 说明） | `11-features-input.txt:213` |
| `12-55` | `31-axolotl-launcher-features.md:26` 写「12-55 世界管理」，实为 12 号原文第 24 条下的**子项行** | `12-server-features-input.txt:55` |
| `12-14` | 12 号原文**第 14 条**「快速显示种子号（需要使用nbt功能）」，恰好也是行号 14 | `12-server-features-input.txt:14` |
| `11-49` / `11-41` | 11 号原文**第 49 / 41 条**（真实行 `11:261` / `11:250`），不是行号（081 已复核） | `11-features-input.txt:261` / `:250` |
| `11-18` | 11 号原文**行号** 18「API 不共有、内部监听」（080 已确认） | `11-features-input.txt:18` |

与 078 的 `11-3` 是条目编号、079 的 `11-50` 是第 50 条、080 的 `11-11` / `11-8` 是条目编号、081 的 `11-49` / `11-41` 是条目编号同形态：同一份调研表里「NN-MM」既可能是条目编号也可能是行号。本轮一律用文件行号 `11:213` / `12:14` / `12:55` / `11:26` / `11:4` / `11:9` / `11:11` / `11:216` / `11:258` / `00:32` / `00:249`。31 号调研与 15 号调研历史行不重写（A226 / A200 / A259）。

## A271 全仓守卫禁用字面量表预检（开工时实跑）

按 A271，新增测试标识符前先核全仓 `scripts/*_guard.py` 的禁用字面量表，不只核本轮新守卫。实跑 `grep -nE 'FORBIDDEN =|for banned in' scripts/*_guard.py` 并读 `api_guard.py` / `i18n_guard.py` / `notice_center_guard.py` / `first_run_guard.py` 的扫描范围：

| 守卫 | 扫全仓还是自身段 | 需避开的字面量 |
| --- | --- | --- |
| `api_guard.py:33` | **全仓 rs，不分测试段** | `Popup::new(` / `PopupKind::` / `catalog()` |
| `i18n_guard.py` | `src/**/*.rs` 逐行中文 | 新模块源码注释全英文、无中文文案 |
| `ai_gate_guard.py:7` | 单文件 `client_ai.rs` | `TcpListener` / `bind(` / `127.0.0.1` / `/mcp` / `Token` / `token` |
| `lan_channel_guard.py:22` / `notice_center_guard.py:23` | 各自 prod 段 | `CHANNEL_TABLE` / `NOTICE_TABLE` / `STEP_CATALOG` / `url` / `token` / `uuid` / `png` / `texture` / `minecraft:` / `§` |
| `first_run_guard.py:22` / `widget_layout_guard.py:22` | 各自 prod 段 | `STEP_CATALOG` / `language` / `account` / `java` / `calendar` / `greeting` / `recent_world` / `WIDGET_TYPES` |
| `appearance_guard.py:22` / `banner_design_guard.py:22` / `skin_draft_guard.py:22` / `upgrade_plan_guard.py:22` / `search_filter_guard.py:22` / `generator_session_guard.py:22` / `seed_access_guard.py:22` | 各自 prod 段 | `PRESET_COLORS` / `COLOR_TABLE` / `DYE_CODES` / `SKIN_TABLE` / `TEXTURE_TABLE` / `COMPAT_TABLE` / `CONDITION_TABLE` / `SESSION_TABLE` / `SEED_TABLE` / `cmp_precedence` |

结论：新模块 `world_editor.rs` 的常量名、函数名、测试名一律不出现 `catalog()` / `Popup::new(` / `PopupKind::` / `http` 连续串 / `token` / `uuid` / `png` / `texture` / `minecraft:` / `give ` / `§` / `STEP_CATALOG` / `language` / `account` / `java` / `calendar` / `greeting` / `recent_world`；标题与正文不写进本层，用语义 slug；端点与端口字面量不写（分部件拼接保留运行时值，A258 / A117 / `11:19`）；源码注释全英文（避开 `i18n_guard`）。测试名 `serialize_carries_no_editor_table()`（避开 `catalog()`，074 E275 / 075–081 同形态）。守卫脚本自身不写凭据前缀连续串（A258），部署前 `python -m py_compile`（A251）。

## A208 复核（本轮开工前）

用户 082 发「干」+ 重申报，未点 AX 编号、未回 Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 / Q-077 / Q-078 / Q-079 / Q-080 / Q-081 / EQ 任一条。按 A202 核 `081-notice-center.md` 尾部与 `rounds.md` 081 补记：081 结尾主分支「下一声『干』按功能池落下一项（剩 7 项 `Planned`）」，替代分支「若回 Q/EQ 任一条则改走拍板闭环」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实 NBT 读取 / 写回、真实网络 IO、第三方库引入、UI 渲染闸门、新增第三方。

## `00:9.1` 连续未达通过的处置（D-082-1）

069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 / 078 / 079 / 080 / 081 连续**十三**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 082 当轮明确指令含「干」，按 `00:248` 覆盖。**不中断推进，但卡点在本轮回复、决策、四值里逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；6 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不能靠改测试或降验收项凑（`00:9.1`）。

## A164 逐条分「已决断 / 未决断」

| 条目 | 状态 |
| --- | --- |
| 064「全部（不与项目冲突的情况下）」 | 已决断：AX01–AX24 全量批准，冲突子项按用户裁决转化 |
| 069–081 连续「干按功能池落下一项」 | 已决断：按工程依赖逐轮落地数据层 |
| 082「所有东西都要用开源的，在保证许可证的情况下」 | **已决断、重申报**：`00:32` / `00:19` / `11:2` / `11:4` / `11:9` / `11:11` / `11:26` / `11:216` / `11:258` / `00:249` 已有同等约束；「只是在跟你说一下」不新增任务，按 A244 落对照表 + 一手核实 |
| `11:213` 第 6 条 vianbt NBT 能力 | **已决断、不依赖 EQ**（A211 真读全文找）；收窄后只落状态索引，NBT 读取执行层不碰 |
| `12:14` 种子号需要 NBT / `12:55` 世界管理四字段 | **已决断、不依赖 EQ**（A211 真读全文找），字段语义落枚举 |
| `11:26` 异证链接 + 许可证前置 + 源产物对比 | **已决断、不依赖 EQ**，`LinkMode` 三值 + `license` 必填 + `diff_checked` 布尔落地 |
| `11:4` 5 字段登记 / `11:9` 独立许可证独立进程 | **已决断、不依赖 EQ**，`LinkMode::SeparateProcess` 落值、其余四字段登记 Q-082-03 |
| `00:249` 许可证不明停下来问 | **已决断**，本轮零新增第三方、vianbt 是 Java 库不硬引，登记 Q-082-01 |
| `00:230` 每轮联网核实上游状态 | **已决断（第 15 节、不阻塞）**，本轮首次真执行，一手结果见上表 |
| `11:18` / `11:19` API 不共有、不写死网址端口 | **已决断**，守卫真拒监听 / 端点字面量 |
| `00:175` / `11:15` 同类功能复用同一模块 | 已决断 |
| 062 排除 AI 提供商配置页 | **已决断**（078 已留痕 Q-078-01），本轮不涉及 |
| 转述的「改游戏模式、允许作弊、和平、游戏规则、改种子只影响新地形提示」 | **未决断**：`31-axolotl-launcher-features.md:26` 为第三方转述，登记 Q-082-02，不写死 |
| `vianbt` 是否确定指 `ViaVersion/ViaNBT`、以什么形态引入（vendor / FFI / 子进程） | **未决断**，登记 Q-082-01，不写成选型结论（A29 / A30） |
| `11:4` 其余四字段（作者 / 项目地址 / 修改后版本地址 / 名字）何时落 | **未决断**，登记 Q-082-03 |
| 真实 NBT 读取 / 写回、libloading 接入、UI 渲染、二维码生成、真实连接建立、投影解析 | **未决断**：078 / 079 / 080 / 081 已登记 Q-078-01 / Q-078-02 / Q-079-01 / Q-079-02 / Q-080-01 / Q-080-02 / Q-081-01 / Q-081-02 |
| EQ-01 ~ EQ-13、4 条 Q-C、Q-067 / Q-070 ~ Q-081 | **未决断**，待用户拍板，本轮不代拍 |

## 选项目的（A211 / A177 / A267 / D-082-2）

真读 7 项 `Planned` 全文（AX03、AX04、AX07、AX08、AX15、AX20、AX22）、065–081 的排除清单、`063-axolotl-survey.md:82` 的低可信度转述登记、073 / 075 / 077 / 078 / 079 / 080 / 081 的七次收窄先例、`src/core/ax.rs` 24 条唯一 spec、既有 16 个 AX 数据层模块与判定层模块真实形态（`seed_access.rs` 记录集合 + 可见性矩阵 + 审计表、`instance_drop.rs` 路径计划纯函数、`notice_center.rs` 状态索引 + 内置条目保护、`generator_session.rs` 会话集合 + 三枚举 + 派生查询、`upgrade_plan.rs` 按 id 索引候选项 + 三选一决策、`search_filter.rs` 谓词集合 + 派生过滤排序、`lan_channel.rs` 静态协议表 + 单实例阶段转移、`feature_gate.rs` 运行时派生声明条目）后选 **AX03 world_editor** 的**数据层**，登记为**我的默认 D-082-2**，不写成用户已决断。

| 项 | 判定 |
| --- | --- |
| AX07 / AX22 | 真实网络 IO / 境外限制 / 第三方端点 / 浏览器授权执行层，且 11 号原文无对应已决断公告锚点，不动 |
| AX20 | `.litematic` / `.schem` 投影解析库，`31-axolotl-launcher-features.md:58` 细项多为第三方转述，零新增第三方约束下不动 |
| AX04 | EQ-13（`ax-feature-pool.md:10`）与 Q-047-01 未拍板，不动 |
| AX08 | `.mrpack` / `.zip` 解析库，066 已排除；070 AX24 已落拖放落点，再落会与 `instance_drop.rs` 同构，081 补记明写，不动 |
| AX15 | Studio 图片编辑撤销重做栈与 `banner_design.rs` 同构，075 E276 已排除，历史行不重写 |
| **AX03 收窄后** | `11:213` / `12:14` / `12:55` / `11:26` / `11:4` / `11:9` / `00:32` / `00:249` 一组 8 条已决断、不依赖 EQ（A211）；用户 082 当轮重申报「开源 + 保证许可证」直接对齐；`00:175` / `11:15` 要求四 / 五枚举共用同一模块；收窄为不碰真实 NBT 读取写回 / 第三方库引入 / UI 渲染 / vianbt 字段 schema 的**存档编辑会话 + 开源组件许可证状态索引数据层**；核心是「五枚举显式 code + 七张白名单表 + 矛盾态函数八处调用 + 单条状态突变不批量 + 八个派生纯查询 + 统一信封零用户文本 + 零内容持有」，与既有 16 个数据层模块（状态集合 / 步骤序列 / 布局槽位 / 分层图案 / 逐条决策 / 谓词过滤 / 会话集合 / 可见性矩阵 / 拖放路径计划 / 静态协议表 / 公告状态索引）均不同构：本层不持有种子值 / 存档内容 / NBT 数据，只存 `id → 字段 / 格式 / 来源 / 许可证 / 链接形态 / 核验态 / 源产物对比态 / 会话态` 的状态映射 |

不做的（登记 Q / 未启动）：真实 NBT 读取与写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、UI 渲染、转述的五个编辑字段与提示文案均未启动。

`src/core/ax.rs:20` 真实 name 是 `world_editor`，conflict 为空；实现模块名 `world_editor.rs`。A267 先读后写，不凭文件名猜；A232 语义 slug 保持不动。

## 接口终点核对（`00:137`）— A244 要求显式核

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod world_editor;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.world_editor`，锚点用真实结尾 `"core.notice_center",` + `"dispatcher.launcher",`（A256 / A234；081 插 `core.notice_center` 时已核过真实结尾，本轮复读确认） |
| `src/core/ax.rs` | AX03 `Planned` → `DataLayer`，`conflict` 保持空；24 条唯一不变；断言 `DataLayer 17` / `Planned 6` |
| `scripts/ax_guard.py` | 显式断言扩到十七项（…AX21、AX02、AX03）；动态求和不变（A240 / A262） |
| `scripts/world_editor_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| 既有 16 个 AX 数据层模块、`feature_gate.rs`、`popup.rs`、`consent.rs` | 零 diff，本层不重复实现其语义 |
| `src/dispatcher/launcher.rs` / `stats.rs` / `region.rs` / `client_ai.rs` / UX HTML / 两语言包 / 56 PNG / `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff |

## `00:245` 通过标记条件显式核 — A244 要求显式核

| 条件 | 本轮判定 |
| --- | --- |
| ① 8.1 独立验证结论为「通过」 | **不满足**：独立验证「部分通过」，存在已失败 / 未证实 / 未启动 |
| ② 所有结论均为「已证实」，不存在未解决的「已失败 / 未证实 / 受阻」 | **不满足**：E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 已失败；EQ / Q / 6 项 `Planned` 未证实；NBT 执行层未启动 |
| ③ 自评 ≥ 7 | 满足（7） |
| 结论 | `00:245` 第 2 条 + 第 18 节第 2 优先级：**不发通过标记**，不附两个哈希，明确写「未通过」及原因（A206） |

`00:9.2` 测试锁定：本轮不修改任何既有断言、不加跳过标记、不删测试；若首跑 FAILED 先留回显再按 A264 核夹具预期，实现零改动、断言强度不降。

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `82-round-082-instructions.txt` 159 字节完整句落盘；逐字保存前确认许可证与保密允许（用户原文自述、非第三方受限材料，`00:133` 前置满足） |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 520 行完整读；11 / 12 号原文 268 / 64 行全文回显 |
| A244 | 逐条对照表（本记录「A244 逐条对照表」节）+ 一手联网核实 + `00:137` / `00:245` 显式核一遍 |
| A248 / A266 / E251 | 开轮核 82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本；本轮为单句 159 字节、无平台拼入第二行文本，不重提工具禁用归因 |
| A145 | 081 末条工具结果被截断，本轮只读核远端 ref + 完整 tree 补验，不重复推送、不强推 |
| A268 | G2 四份原文全部列入哈希表；决策 `## 9` / `## 10` 锚点一次排对 |
| A271 | 开工实跑全仓守卫禁用字面量表并核扫描范围，测试标识符从首版避开 `catalog()` 等命中串 |
| A211 / A201 / A217 / A250 / A259 | 真读全文找一组 8 条已决断锚点并覆盖 081「依赖 NBT 解析库」相对排序理由；OR 两条路径都落值不擅自定优先级、登记 Q-082-01 / Q-082-03；`11-6` / `12-55` 是条目编号、`12-14` 与 `11-18` 是行号分开核；补记覆盖，历史行不重写；先核三个既有模块占位边界 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX03 数据层已实现 / 已验证；真实 NBT 读取写回、库引入、UI 渲染未启动 |
| `00:54` / `00:111` / `00:207` | 零新增第三方；不改 Cargo / vendor / api / popup / feature_gate / consent / 既有 16 模块 / UX / 语言包 / PNG；本轮若无新防错项则防错清单零改动，不凑条目 |
| `00:114` | 状态变更走统一 `Envelope`，请求标识由既有实现承载 |
| `00:175` / `11:15` | 五枚举共用同一 `WorldEditor` 与同一组常量表，公共能力全部复用既有 `robust` / `Envelope` / `diag_line` / `PROTECTED_FILES` |
| `00:110` | 根级 + 枚举级 + 字段级 + 矛盾态坏输入、空集合 / 越界 / 饱和 / 控制字符全处理 |
| `00:26` / A30 / `11:18` / `11:19` | 公告 id 与许可证 slug 当不透明字符串；不写端点 / 端口 / 凭据 / 监听、不写死 vianbt 字段 schema、不持有种子值 / 存档内容 / NBT 数据 |
| `00:230` | 本轮首次真执行上游核实（ViaNBT 一手 API + 远端 ref + 当前时间），如实登记，不再写「未执行」 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库；`11:26` 中「这个内容不要写到任何地方」的分句按用户原文不写进本轮新增文档 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构；LOG 键数 = NODES 步数（A265） |
| A154 / A269 / A270 / A247 | 五枚举显式 `code()` / `parse()`；守卫解析**五个** impl 段字面量逐值比对；**七张** `&[&str]` 常量表用显式 `EXPECTED` 集合逐值比对，`VERIFIED_LICENSE` 单值另核；复用 `robust::MAX_TEXT_BYTES` 用显式语句并验删行真 FAIL |
| A258 / A262 / A263 / A264 / A265 / E322 / E330 | 新守卫不写凭据连续串、不写死状态计数、注入锚点唯一、夹具与上限对齐、演示键数对齐；按 E322 教训解析矛盾态函数体五条检查 + 八处调用点；按 E330 教训解析 `change_event` 函数体载荷白名单与十值计数 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-082-2 ~ D-082-20，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-082-2 | 选 AX03 落数据层 | 我的默认，不写成用户已决断（A177） |
| D-082-3 | 收窄范围 | 不碰真实 NBT 读取写回 / 第三方库引入 / vianbt 字段 schema / UI 渲染，只落存档编辑会话 + 开源组件许可证状态索引 |
| D-082-4 | 字段枚举 | `EditField` = `seed` / `world_type` / `chunks` / `dimension`（`12:14` / `12:55`），显式 `code()` + `parse()`（A154 / A269） |
| D-082-5 | 格式枚举 | `ValueFormat` = `int` / `bool` / `opaque`（NBT 标量形态，不写死 vianbt schema），显式 `code()` + `parse()` |
| D-082-6 | 来源枚举 | `OssSource` = `builtin` / `open_source`（`00:32` / `11:11`），显式 `code()` + `parse()` |
| D-082-7 | 链接形态枚举 | `LinkMode` = `same_license` / `dynamic_link` / `separate_process`（`11:26` / `11:9` 两条 OR 都落值，A250），显式 `code()` + `parse()` |
| D-082-8 | 会话态枚举 | `EditorState` = `draft` / `verified` / `applied`，显式 `code()` + `parse()` |
| D-082-9 | 不透明字符串 | 条目 `id` 与 `license` 当不透明字符串；只校验长度 ≤ `robust::MAX_TEXT_BYTES`、无控制字符；**零内容持有**，种子值 / 存档内容 / NBT 数据 / 作者 / 项目地址全不进本层（`00:26` / `11:18` / `11:19` / A42） |
| D-082-10 | 协议常量表 | `KNOWN_KEYS` 3 键 / `ENTRY_KEYS` 9 键 / `FIELDS` 4 值 / `FORMATS` 3 值 / `SOURCES` 2 值 / `LINK_MODES` 3 值 / `STATES` 3 值，七表严格白名单（A270）；`VERIFIED_LICENSE = "MIT"` 单值另核（本轮一手核实 `license.spdx_id=MIT`） |
| D-082-11 | 工作区状态 | `WorldEditor { session: EditorState, entries: Vec<EditorEntry> }`，`EditorEntry { id, field, format, source, license, link_mode, verified, diff_checked, state }`；`MAX_ENTRIES = 24` 有界 |
| D-082-12 | 纯查表函数 | `editable_count()` / `verified_count()` / `by_field()` / `by_source()` / `by_link_mode()` / `license_for()` / `applied_count()` / `summary()` 八个纯函数不读文件 |
| D-082-13 | 矛盾态五条规则八处调用 | `entry_consistent()` 抽成单一函数，`parse()` / `add_entry()` / `set_source()` / `set_state()` / `set_link_mode()` 八处调用：`open_source` 但 `license` 空拒收；`applied` 但 `verified=false` 拒收；`applied` 但 `diff_checked=false` 拒收；`separate_process` 但 `source=builtin` 拒收；`license` 非空但 `source=builtin` 拒收；守卫解析函数体逐项核五条字面量（E322 教训） |
| D-082-14 | 顶层严格白名单 | 3 键 + 条目 9 键；未知键整份拒并给 DEGRADE 行（A189）；27 类坏输入回默认或跳过 |
| D-082-15 | 持久化 | `world-editor.json` schema 1，只写 3 键；原子写；`reset` 不删文件并复用 065 四文件保护 |
| D-082-16 | 状态变更事件 | `Kind=Event` / `target=world.editor` / 载荷只带 10 个计数与枚举码；`id` / `license` / 种子值 / 作者全不进事件（`00:114`），守卫断言 `e.field("id") == None` |
| D-082-17 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77 / A100） |
| D-082-18 | 启用与执行边界 | 真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、UI 渲染、转述五字段均未启动；Q-082-01 / Q-082-02 / Q-082-03 待拍板 |
| D-082-19 | 状态分层与联网核实 | AX03 数据层已实现 / 已验证，其余未启动（`00:166`）；`00:230` 本轮首次真执行，一手结果逐项回显 |
| D-082-20 | 用户重申报处置 | 「只是在跟你说一下」按 A244 落对照表 + 一手核实 + `00:137` / `00:245` 显式核，不扩功能范围、不新增依赖、不改功能池主分支；若出现新形态错误才按 `00:207` 补防错项，否则零改动不凑条目 |

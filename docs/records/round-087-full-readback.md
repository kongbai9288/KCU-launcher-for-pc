# 087 开工逐字复读记录

开工 `Mon Nov 23 22:16:40 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节完整读、分两段回显（1–260 / 261–520），末条仍为 A271。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮逐行全文回显（A211 真读全文；A244 要求真读原文与防错清单全文并记行数）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。本表哈希记录于 087 四件套写毕、台账补记写毕之前的读时刻；台账与 index 补记后的字节 / 哈希以交付快照为准。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295 |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88 |
| `docs/spec/87-round-087-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/86-round-086-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/85-round-085-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a |
| `docs/decisions/068-delivery-reconciliation.md` | 8468 | 90 | `0ece2de9960d48a8e52622595f743f7bd65472f6e8467452f65f64443598b796 |
| `docs/decisions/084-delivery-closure.md` | 14011 | 110 | `1e21e89361bbef2657da3dae265155f68110ce63537169341098966d8f22806c |
| `docs/decisions/085-mod-rollback.md` | 12352 | 111 | `71b413eb4202901d63f1fd169102045bf2a2172d85725c1367f63dc283dcb89d |
| `docs/decisions/086-delivery-closure.md` | 13670 | 110 | `4f3db2c1c3c7fae5e0457ac02b6c8874956b0cbe29449b02a8c00fe32cd254af |
| `docs/records/round-086-full-readback.md` | 17837 | 166 | `5c6fdef70e05642177dd76af116dac56b2211a9571fc4c1ed891cbfb8a3563a6 |
| `docs/records/round-087-full-readback.md` | 本轮生成 | — | — |
| `docs/verification/round-086.md` | 11301 | 97 | `f4c866be1935729aa1cd79ca09c02df2cf8685eb31d5b056052c23e4448a7e05 |
| `docs/verification/round-087.md` | 本轮生成 | — | — |
| `demos/round-086-delivery.html` | 15153 | 68 | `2d30131a4a902fd01b8c9847650e3ae4c91d58ebab37a2aee3c59e7e8683170e |
| `demos/round-087-delivery.html` | 本轮生成 | — | — |
| `src/core/mod_rollback.rs` | 37354 | 990 | `696cb7ef7d88964e33664566bf7dee52b1952ee3343cdcff363a3be56c05fb64 |
| `scripts/mod_rollback_guard.py` | 12393 | 269 | `1e4cab4382c9f24fc4dd786b0c7d90b4dcfe22bb99e8a8241324c8707137fddd |
| `src/core/ax.rs` | 4623 | 100 | `e3a91e06bff5cdd71cbdb2938ce013c569d79264606c5f8dce7c7a9e901bb0bf |
| `src/core/boot.rs` | 18120 | 561 | `40a75455d7c5c43858752ac4dab15837e0a90d0af1b3a8fc8a95068bcd0ce273 |
| `src/core/mod.rs` | 840 | 45 | `ecc9e65c4a94d906dee0abe2fb0278f1f11c878811f3c8cf78df0060fa6f19d8 |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0 |
| `scripts/ax_guard.py` | 2019 | 49 | `13e9ea4b202bdb427f83e5a421c2c48ea84bc6acf8c74582fff9d1770d5a1a7a |
| `.github/workflows/ci.yml` | 4884 | 137 | `2cf61a840ca44b1d3050aa9d4882d73f63e1a0369d79fed3bfe319bd15b17f7b |
| `Cargo.toml` | 916 | 37 | `47346e19c7e0946a55400c83a76e38c94b1d9fa0b90c9b63bac1717316080067 |
| `Cargo.lock` | 3520 | 174 | `bd20d10a30d51c8488fede122dca5ff9224313ca7abb794f66673689daf04044 |
| `THIRD-PARTY-NOTICES.md` | 22344 | 309 | `ac0941e2e2b5300791e036113e31e775c43399da9437460e565329af609babbf |
| `docs/records/rounds.md` | 342120 | 3380 | `808a9a01df830da8c06aea6346ac642ba10caca9214b1c713b91277edab5e583 |
| `docs/records/ax-feature-pool.md` | 30030 | 227 | `53cbdca77ef1e1f584920e1856cd8aa7b55b0780ec8f55371b895b2b981b9872 |
| `docs/index.md` | 49758 | 636 | `c6a5a5a800e2ed6fe515f9e6c1034103dba77648f01508990a8964b3bc196d62 |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `87-round-087-instructions.txt:1` | 逐字 3 字节 `干`（SHA-256 `9ee0280b…`，无换行），与 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号 spec 同形态 |
| `86-round-086-instructions.txt:1` | 逐字 3 字节 `干`，086 轮已落盘 |
| `72-round-072-instructions.txt:1` | 117 字节工具澄清句，已在 072 处理并撤回 071 归因（E251） |
| `11:15` / `11:21` / `11:222` / `12:35` / `12:36` / `12:40` / `12:41` | A211 本轮真读全文复核的 AX08 `instance_import` 七锚点，086 已登记，顺延为 088 输入，不代拍 |
| `00:133` / `00:34` / `00:260` | 逐字保存、每轮开工完整读 00 与防错清单——本轮执行 |
| `00:137` / `00:245` / `00:248` | 接口终点、通过标记条件、用户当轮明确指令优先——本轮显式核一遍 |
| `00:230` | 每轮联网核实现有时间与上游版本状态——本轮执行远端 ref 与时间核实 |
| `00:9.1` / `00:9.2` / `00:207` | 连续未达通过、测试锁定、文档不凑条目 |
| `ai-errors.md:292` | A145 推送工具结果被网关截断时，用远端 ref message + 完整 tree 比对补验，不重复推送、不强推、不重写历史 |
| `ai-errors.md:409` | A206 远端未推成时，验证报告 / 决策 / 四值表里的 ALL_MATCH 陈述必须同步改为「未执行 / 受阻」 |
| `ai-errors.md:416` | A209 远端未推成时写「受阻、ALL_MATCH 本轮不成立」；再试一次仍失败就如实登记 |
| `ai-errors.md:443` | A216 推送撞网关 502 时，先用只读 ref 确认远端是否变过，再决定重推 |
| `ai-errors.md:487` | A249 一轮落地代码、下一轮才补交付时，按新落盘 spec 同时要求两套四件套；不删 spec 规避守卫 |
| `ai-errors.md:512` | A266 平台拼入用户位次的文本不得当成用户当轮指令 |
| `ai-errors.md:513` | A267 改功能池状态前先读真实 `name` slug |
| `ai-errors.md:514` | A268 G2 四份原文与 G3 的 `## 9` / `## 10` 锚点一次排对 |
| `docs/decisions/086-delivery-closure.md:12` | 086 唯一下一步写「087 按功能池落下一项」，本轮按 A202 打开核过 |

## A248 / A266 预检

87 号 spec 逐字副本全文 3 字节 `干`，已落盘。按 A248 开轮核 87 / 86 / 85 / 84 / 83 / 82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本：87 / 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号均仅 3 字节 `干`，82 号 159 字节完整句，72 号 117 字节澄清句已在 072 处理。按 A266，平台拼入用户位次的文本不作用户当轮指令、不据此写「未遵守 / 偏离 / 下一步按该行决定」、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080–086 已按同一口径补记，历史回复与历史文件不重写（A181 / A201）。副本里没有的文字不写成用户指令。工具从未禁用，本轮正常调用工具完成提交、推送与打包。

## A145 远端补验：086 补记未推成

086 主快照已推：本地 `b598ac5` / 1255 文件 DIRTY 0，远端 `e4723fb09e3494b0915410fea237f6c5e908181f`（`force=false`，parent `c025a78`，23 项变化 + `base_tree=aa1ac3e`），完整 recursive tree `1255 / 1255 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`。但 086 阶段二补记（5 文件）两次撞网关 502，工具结果不可用；本轮只读 `GET /git/ref/heads/main` 得远端 ref 仍为 `e4723fb…`，完整 tree 比对 `LOCAL 1255 / REMOTE 1255 / DIFF 5 / EXTRA 0 / TRUNCATED False / ALL_MATCH False`，`DIFF_SAMPLE` 为 `docs/decisions/085-mod-rollback.md` / `docs/decisions/086-delivery-closure.md` / `docs/records/rounds.md` / `docs/verification/round-085.md` / `docs/verification/round-086.md`。按 A145 / A216 用远端 ref + 完整 tree 补验，确认远端未变后再决定重推；不重复推送、不强推、不重写历史。按 A206 / A209，086 补记推送结果写「受阻、ALL_MATCH 本轮不成立」，不沿用主快照的模板值。

本地状态：HEAD `7ddca08`（086 补记合并后的本地提交，未推送），TRACKED 1255，DIRTY 1（87 号 spec），无 `.git/index.lock`、无运行中 git 进程、PYC 0。两个 zip 仍是 084 轮旧包：主包 1243 项、`ui-previews.zip` 57 项。

E356（086 已登记）：阶段二命令被网关 502 重试执行两次，补记文本在 5 个文件各写入两次，并产生两个同 message 的本地未推送提交；本地已删重复段、`git reset --soft b598ac5` 合并为单一提交 `7ddca08`，远端历史未重写。E357（本轮新登记）：086 二次推送两次 502 未推成，远端 DIFF 5、ALL_MATCH False；087 按 A145 补验后把补记与 087 产物合并推送，推送成功且逐项 ALL_MATCH 后才写闭环。

## A249 形态判定：087 四件套

087 落 87 号 spec 后 `python3 scripts/delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-087-full-readback.md`。085 / 086 两套四件套本地齐且已随主快照推送；**不删 87 号 spec 规避守卫、不改守卫断言**，按真实轮次补齐 087 的 readback / decision / verification / demo 后复跑 OK，FAIL 原样留痕。

## 068 / 084 先例与本轮性质（A208 / A202 复核）

按 A202 打开 `docs/decisions/086-delivery-closure.md:12` 核尾部：086 写出「087 按功能池落下一项（剩 5 项 `Planned`：AX07 / AX08 / AX15 / AX20 / AX22）」。但 086 补记 5 文件两次 502 未推成、远端 DIFF 5、ALL_MATCH False，交付层断裂；084 决策第 25 行同形态先例写明「083 结尾写出下一声「干」按功能池落下一项，但 083 自身未提交、未推送、无最终回复」，按 068 / 084 先例优先闭环。按 A208 复核 `b-class-status-recheck.md:85`：EQ-01 ~ EQ-13 仍待拍、未启用，B04 卡 EQ-01 但本轮不动 UI，无「需 EQ 拍板才能动」的阻塞层。定本轮为 **086 交付闭环 + 087 开工留痕轮**（D-087-2 我的默认）：`src/` 零改动、零新增第三方、不新开功能池项、5 项 `Planned` 不变，086 决策尾部「087 按功能池落下一项」顺延为 088 唯一下一步，显式登记覆盖（A201）。

## A211 真读全文找出的下一项候选锚点（复核，不代拍）

本轮真读 00 / 防错 / 11 / 12 号全文，不是只核哈希与台账状态。按 A267 先读 `src/core/ax.rs:24–39` 真实表：剩 5 项 `Planned` 为 `AX07 doh_support`（conflict `network_io_not_started`，ui false）、`AX08 instance_import`（conflict 空，ui true）、`AX15 studio_image_editor`（conflict 空，ui true）、`AX20 projection_workshop`（conflict 空，ui true）、`AX22 shimu_account`（conflict 空，ui true）；`ax.rs:82` 断言 `count_by_state(AxState::Planned) == 5`。AX08 七锚点 086 已登记，本轮逐字复核：`11:15` 整合包一键安装拖到主界面、`11:21` 拖动安装显示拖动到此处页面、`11:222` 编号条目、`12:35` 整合包导入导出（mrpack / CurseForge zip）、`12:36` 拖拽安装模组 / 插件、`12:40` 实例模板与克隆、`12:41` 实例导出 / 导入（可移植实例）。七锚点顺延为 088 输入；选哪一项按功能池逐条核冲突后定，087 不代拍、不擅自定 5 项之间的优先级（A250 / A164）。

## A244 合规复核

| 用户口径 | 原文锚点 | 本轮可核对证据 | 结论 |
| --- | --- | --- | --- |
| 用开源的 | `00:32` / `00:19` / `11:2` / `11:11` | `Cargo.lock` `[[package]]` 26 项、`vendor/` 25 个第三方目录、`docs/licenses/` 58 份 LICENSE 全文、`THIRD-PARTY-NOTICES.md` 309 行、`code-ownership-audit.md` 逐轮登记；085–087 零新增第三方 | 已证实 |
| 保证许可证 | `00:249` / `00:133` / `11:26` / `11:4` / `11:258` / A44 / A45 / A100 / A139 / A141 | 085 复用既有 `semver` / `serde_json` / `anyhow`，不引新 crate；58 份 LICENSE 与 309 行声明未变 | 已证实 |
| 停下来问，不硬上 | `00:249` | 085–087 零新增第三方；无语义等价库可换的项目特有口径按 `00:6.1` 只写事实 | 已证实 |
| 源与产物对比 | `11:26` / A45 | 085 新增文件为项目自写数据层，非拼接上游源码；真实字节比对执行层未启动 | 已证实（零拼接）+ 未启动 |

## `00:230` 本轮联网核实

| 项 | 一手结果 |
| --- | --- |
| 当前时间 | `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` → `Mon Nov 23 22:16:40 CST 2026` |
| 远端 ref | `GET /git/ref/heads/main` RC=200 → `e4723fb09e3494b0915410fea237f6c5e908181f` / parent `c025a78` / message `round 085-086: AX04 mod_rollback data layer, guard, delivery closure` |
| 完整 tree | `1255 / 1255 / DIFF 5 / EXTRA 0 / TRUNCATED False / ALL_MATCH False` |
| 上游版本状态 | 082 已核 `ViaVersion/ViaNBT`：`pushed_at=2026-10-27T14:24:29Z`、`default_branch=master`、`archived=false`、tags `3.0.0` / `2.1.3` / `2.1.2`；085–087 无新增上游依赖，复核状态不变 |

## `00:9.1` 连续未达通过的处置（D-087-1）

069–086 连续**十八**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 087 当轮明确指令「干」按 `00:248` 覆盖。不中断推进，但卡点在本轮回复、决策、四值里逐条回显（A164）：E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 / E356 / E357 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；5 项 `Planned` 与真实执行层 / UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不改测试、不降验收项。

## `00:137` 接口终点核对（A244 要求显式核）

| 引用点 | 087 形态 |
| --- | --- |
| `src/` | **零改动**；`src/core/mod_rollback.rs` / `ax.rs` / `boot.rs` / `mod.rs` 保持 085 落地形态 |
| `src/api.rs` | 零改动，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `scripts/mod_rollback_guard.py` / `.github/workflows/ci.yml` | 085 已挂 `scan` job，087 只复核不改动 |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff，26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| UX HTML / 两语言包 / 56 PNG | 零 diff |
| 087 新增文件 | `87` 号 spec、`round-087-full-readback.md` / `087-delivery-closure.md` / `round-087.md` / `demos/round-087-delivery.html`；台账补记与 `docs/index.md` 必读清单 |

## `00:245` 通过标记条件显式核（A244 要求显式核）

| 条件 | 本轮判定 |
| --- | --- |
| ① 8.1 独立验证结论为「通过」 | 不满足：独立验证「部分通过」，存在已失败 / 未证实 / 未启动 |
| ② 所有结论均为「已证实」 | 不满足：E213–E357 已失败；EQ / Q / 5 项 `Planned` 未证实；真实执行层与 UI 渲染未启动 |
| ③ 自评 ≥ 7 | 满足（7） |
| 结论 | `00:245` 第 2 条 + 第 18 节第 2 优先级：**不发通过标记**，明确写「未通过」及原因（A206） |

## 合规核对表

| 约束 | 087 行为 |
| --- | --- |
| `00:133` 逐字保存 | 87 号 spec 3 字节落盘；85 / 86 号 spec 已在 085 / 086 落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显、防错清单 520 行完整读、11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 17 份 spec 逐字副本；平台文本按 A266 不作指令、不进副本；不重提工具禁用归因 |
| A145 / A216 / A206 / A209 | 086 补记两次 502，本轮只读远端 ref + 完整 tree 补验（DIFF 5 / ALL_MATCH False），确认远端未变后合并重推；未推成时写「受阻」，不写模板值 |
| A140 / A254 | 提交前核无锁、无运行中 git 进程；086 的重复本地提交已在 086 轮合并，远端历史未重写 |
| A249 / A268 | 不删 87 号 spec 规避守卫；补齐 087 四件套；G2 四份原文列入哈希表、G3 `## 9` / `## 10` 锚点一次排对 |
| A245 / `00:9.2` | 085 既有并发用例偶发 1 FAILED 如实留痕；087 `src/` 零改动、断言一字未改 |
| A116 / A258 / A205 | CI 三 job 按真实命令实跑；`scripts/__pycache__/` 保持 0 项；两个 zip 按 `git ls-files -z \| zip -@` 重打 |
| A252 / A265 | 全量 726 / 0 注明分段求和口径；087 演示五数组 16 项对齐 |
| A267 | 改功能池状态前先读真实 slug；本轮不改状态，只复核 5 项 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` / `00:207` | 设计说明只走对话不进仓库；本轮无新形态防错项，防错清单零改动，不凑条目 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-087-*，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-087-1 | 连续十八轮未通过 | 按 `00:248` 用户当轮「干」覆盖，不中断但逐条回显卡点 |
| D-087-2 | 本轮性质 | **086 交付闭环 + 087 开工留痕轮**，`src/` 零改动、零新增第三方、不新开功能池项（068 / 084 先例 + A202 + A249）；086 尾部「落下一项」顺延 088 |
| D-087-3 | 功能池 | AX04 保持 `DataLayer`；5 项 `Planned` 不变；AX08 七锚点顺延 088 输入 |
| D-087-4 | 提交范围 | 086 补记（5 文件，已在本地 HEAD `7ddca08` 未推）与 087 全部产物一次提交；A11 逐项核 diff 范围 |
| D-087-5 | 推送 | `scripts/api_push.py` 以 `base_tree` 增量 POST，`force=false`；先按 A145 核远端 ref 未变，推送后逐项 ALL_MATCH 写进 `rounds.md` 087 补记 |
| D-087-6 | 构建产物与 zip | `scripts/__pycache__/` 保持 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1`；主 zip 按 `git ls-files -z \| zip -@`、`ui-previews.zip` 按 `demos/preview/*.png` 清单重打 |
| D-087-7 | Q / EQ | 不代拍；Q-082-01 / 02 / 03 与历史 26 组 Q、EQ-01 ~ EQ-13、4 条 Q-C 保持未证实 |
| D-087-8 | 状态分层与通过标记 | AX04 数据层 085 已实现 / 已验证；086 交付层补记未推成、ALL_MATCH 本轮不成立，087 合并推送后才闭环；不发通过标记 |

# 086 开工逐字复读记录

开工 `Mon Nov 23 13:20:33 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节完整读、分两段回显（1–260 / 261–520），末条仍为 A271，085 / 086 无新增防错项。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮逐行全文回显（A211 真读全文；A244 要求真读原文与防错清单全文并记行数）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。本表哈希记录于 086 四件套写毕、台账补记写毕之前的读时刻；台账与 index 补记后的字节 / 哈希以交付快照为准。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295 |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88 |
| `docs/spec/86-round-086-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/85-round-085-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/84-round-084-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/82-round-082-instructions.txt` | 159 | 0 | `9ae4222c65b15bca9449a86d08a4e5fb9742e0194a8243affb26382aca6a5ec1 |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a |
| `docs/decisions/068-delivery-reconciliation.md` | 8468 | 90 | `0ece2de9960d48a8e52622595f743f7bd65472f6e8467452f65f64443598b796 |
| `docs/decisions/084-delivery-closure.md` | 14011 | 110 | `1e21e89361bbef2657da3dae265155f68110ce63537169341098966d8f22806c |
| `docs/decisions/085-mod-rollback.md` | 11945 | 107 | `a8bc0222029805577e0f041288cca769f44c0ee7285cad380f83711660a4b36d |
| `docs/records/round-085-full-readback.md` | 6894 | 81 | `df645d85b664dca7748f90d6a9b2a2b75acd2d53fe7d97e85017978019516077 |
| `docs/records/round-086-full-readback.md` | 本轮生成 | — | — |
| `docs/verification/round-085.md` | 10371 | 92 | `fc5e5d7b85c338bb9ec27cb5e7a7b89be3ce1244c0f2f5e53d541f127ef04728 |
| `docs/verification/round-086.md` | 本轮生成 | — | — |
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
| `docs/records/rounds.md` | 335543 | 3373 | `ea9f8718a16878454b9322eb206e3a126986e452add508c7b4a89465c90a0f13 |
| `docs/records/ax-feature-pool.md` | 29194 | 223 | `918474f9dfd60a13831c2b6be959efb08ce87c1c056f623e6e2005906799858c |
| `docs/index.md` | 49398 | 636 | `5bcb3f3e5455e081bb79d3b34816446f6879bd13e311c463fc1b7010f1aee106 |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `86-round-086-instructions.txt:1` | 逐字 3 字节 `干`（SHA-256 `9ee0280b…`，无换行），与 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号 spec 同形态 |
| `85-round-085-instructions.txt:1` | 逐字 3 字节 `干`，085 轮已落盘 |
| `82-round-082-instructions.txt:1` | 159 字节完整句（开源许可证口径重申报），082 轮已逐字落盘并按 A244 落对照表 |
| `72-round-072-instructions.txt:1` | 117 字节工具澄清句，已在 072 处理并撤回 071 归因（E251） |
| `11:244` / `12:8` / `12:33` / `12:39` | AX04 四锚点，084 找出、085 落地，086 复核不变 |
| `11:15` / `11:21` / `11:222` / `12:35` / `12:36` / `12:40` / `12:41` | A211 本轮真读全文找出的 AX08 `instance_import` 候选锚点，登记为 087 输入，不代拍 |
| `00:133` / `00:34` / `00:260` | 逐字保存、每轮开工完整读 00 与防错清单——本轮执行 |
| `00:137` / `00:245` / `00:248` | 接口终点、通过标记条件、用户当轮明确指令优先——本轮显式核一遍 |
| `00:230` | 每轮联网核实现有时间与上游版本状态——本轮执行远端 ref 与时间核实 |
| `00:9.1` / `00:9.2` / `00:207` | 连续未达通过、测试锁定、文档不凑条目 |
| `ai-errors.md:487` | A249 一轮落地代码、下一轮才补交付时，`delivery_guard.py` 会按新落盘的 spec 同时要求两套 readback / decision / verification / demo；不删 spec 规避守卫，按真实轮次补齐 |
| `ai-errors.md:512` | A266 平台拼入用户位次的文本不得当成用户当轮指令 |
| `ai-errors.md:513` | A267 改功能池状态前先读真实 `name` slug |
| `ai-errors.md:514` | A268 G2 四份原文与 G3 的 `## 9` / `## 10` 锚点一次排对 |
| `docs/decisions/068-delivery-reconciliation.md` | 068 轮先例：用户只发「干」且上一轮交付层断裂时，`src/` 零改动补齐交付闭环 |
| `docs/decisions/085-mod-rollback.md:12` | 085 唯一下一步写「086 按 068 / 084 先例补 085 交付闭环」 |

## A248 / A266 预检

86 号 spec 逐字副本全文 3 字节 `干`，已落盘。按 A248 开轮核 86 / 85 / 84 / 83 / 82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本：86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号均仅 3 字节 `干`，82 号 159 字节完整句，72 号 117 字节澄清句已在 072 处理。按 A266，平台拼入用户位次的文本不作用户当轮指令、不据此写「未遵守 / 偏离 / 下一步按该行决定」、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080 / 081 / 082 / 083 / 084 / 085 已按同一口径补记，历史回复与历史文件不重写（A181 / A201）。副本里没有的文字不写成用户指令。工具从未禁用，本轮正常调用工具完成提交、推送与打包。

## A145 远端补验与 085 未闭环状态

085 末条全仓凭据扫描工具结果被网关截断不可用，且 085 全轮无最终回复。按 A145 本轮只读 `GET /git/ref/heads/main` 得 `c025a78b945e89213f85e985dc39f8f2f9e36091`（084 补记，parent `918cd90`），完整 recursive tree 比对 `LOCAL 1243 / REMOTE 1243 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`。本地 HEAD 仍为 `f66965a`（084 补记），TRACKED 1243，DIRTY 9（5 项修改 + 4 项新增：85 / 86 号 spec、`src/core/mod_rollback.rs`、`scripts/mod_rollback_guard.py`），无 `.git/index.lock`、无运行中 git 进程、PYC 0。

085 实际落地：`src/core/mod_rollback.rs` 990 行、`scripts/mod_rollback_guard.py` 269 行、`ax.rs` AX04 `Planned → DataLayer`、`boot.rs` 插 `core.mod_rollback`、`mod.rs` 加模块声明、`ax_guard.py` 与 CI `scan` job 扩展；`cargo test --offline --lib` 最终 687 / 0、分段 726 / 0、Win GNU RC=0、42 组双向注入全真 FAIL、31 守卫 0 FAIL、CI 三 job 通过。但 **085 四件套（readback / decision / verification / demo）、台账补记、`docs/index.md`、提交、推送、zip、最终回复全部未落地**。文件已落盘不等于交付已闭环（E353）。按 A145 用远端 ref + 完整 tree 补验，不重复推送、不强推、不重写历史。

## A249 形态判定：两套四件套

085 落地代码与验证；086 落 86 号 spec 后 `python3 scripts/delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-085-full-readback.md`，正是 A249 描述的多套四件套形态。**不删 85 / 86 号 spec 规避守卫**，按真实轮次补齐 085 与 086 各自四件套，并把全部产物一次提交推送、重打 zip。

## 068 / 084 先例与本轮性质（A208 / A202 复核）

按 A202 打开 `docs/decisions/085-mod-rollback.md:12` 核尾部：085 写出「086 按 068 / 084 先例补 085 交付闭环」，但 085 自身四件套、台账、提交、推送、zip、最终回复均缺失。按 A208 复核 `b-class-status-recheck.md:85`：EQ-01 ~ EQ-13 仍待拍、未启用，无「需 EQ 拍板才能动」的阻塞层。按 068 / 084 先例（用户只发「干」且上一轮交付层断裂时，`src/` 零改动补齐交付闭环），本轮定为 **085 交付闭环轮**：`src/` 零改动、零新增第三方、不新开功能池项，AX04 保持 `DataLayer`，`Planned 5` 保持不变（AX07 / AX08 / AX15 / AX20 / AX22）。登记 D-086-2 为我的默认（A177），不写成用户已决断。

## A211 真读全文找出的下一项候选锚点（登记，不代拍）

本轮真读 00 / 防错 / 11 / 12 号全文，不是只核哈希与台账状态。按 A267 先读 `src/core/ax.rs` 真实表：剩 5 项 `Planned` 为 `AX07 doh_support`（conflict `network_io_not_started`，ui false）、`AX08 instance_import`（conflict 空，ui true）、`AX15 studio_image_editor`（conflict 空，ui true）、`AX20 projection_workshop`（conflict 空，ui true）、`AX22 shimu_account`（conflict 空，ui true）。AX08 的已决断候选锚点：

| 锚点 | 原文要点 |
| --- | --- |
| `11:15` | 整合包一键安装，可以拖到主界面直接安装 |
| `11:21` | 拖动安装时显示拖动到此处页面 |
| `11:222` | 同 `11:15` 的编号条目，按真实行号登记 |
| `12:35` | 整合包导入导出（mrpack / CurseForge zip） |
| `12:36` | 拖拽安装模组 / 插件 |
| `12:40` | 实例模板与克隆 |
| `12:41` | 实例导出 / 导入（可移植实例） |

七锚点登记为 087 输入；选哪一项按功能池逐条核冲突后定，086 不代拍、不擅自定 5 项之间的优先级（A250 / A164）。AX07 的 `network_io_not_started` 冲突保持登记。

## A244 合规复核（用户 082 开源许可证重申报）

| 用户口径 | 原文锚点 | 本轮可核对证据 | 结论 |
| --- | --- | --- | --- |
| 用开源的 | `00:32` / `00:19` / `11:2` / `11:11` | `Cargo.lock` `[[package]]` 26 项、`vendor/` 25 个第三方目录、`docs/licenses/` 58 份 LICENSE 全文、`THIRD-PARTY-NOTICES.md` 309 行、`code-ownership-audit.md` 逐轮登记；085 / 086 零新增第三方 | 已证实 |
| 保证许可证 | `00:249` / `00:133` / `11:26` / `11:4` / `11:258` / A44 / A45 / A100 / A139 / A141 | 085 复用既有 `semver` / `serde_json` / `anyhow`，不引新 crate；58 份 LICENSE 与 309 行声明未变 | 已证实 |
| 停下来问，不硬上 | `00:249` | 085 / 086 零新增第三方；无语义等价库可换的项目特有口径按 `00:6.1` 只写事实 | 已证实 |
| 源与产物对比 | `11:26` / A45 | 085 新增文件为项目自写数据层，非拼接上游源码；真实字节比对执行层未启动 | 已证实（零拼接）+ 未启动 |

## `00:230` 本轮联网核实

| 项 | 一手结果 |
| --- | --- |
| 当前时间 | `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` → `Mon Nov 23 13:20:33 CST 2026` |
| 远端 ref | `GET /git/ref/heads/main` RC=200 → `c025a78b945e89213f85e985dc39f8f2f9e36091` / parent `918cd90` / message `round 084 addendum: remote sync 1243 files ALL_MATCH` |
| 完整 tree | 1243 / 1243 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True |
| 上游版本状态 | 082 已核 `ViaVersion/ViaNBT`：`pushed_at=2026-10-27T14:24:29Z`、`default_branch=master`、`archived=false`、tags `3.0.0` / `2.1.3` / `2.1.2`；085 / 086 无新增上游依赖，复核状态不变 |

## `00:9.1` 连续未达通过的处置（D-086-1）

069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 / 078 / 079 / 080 / 081 / 082 / 083 / 084 / 085 连续**十七**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 086 当轮明确指令「干」按 `00:248` 覆盖。不中断推进，但卡点在本轮回复、决策、四值里逐条回显（A164）：E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；5 项 `Planned` 与真实执行层 / UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不改测试、不降验收项。

## `00:137` 接口终点核对（A244 要求显式核）

| 引用点 | 086 形态 |
| --- | --- |
| `src/` | **零改动**；`src/core/mod_rollback.rs` / `ax.rs` / `boot.rs` / `mod.rs` 保持 085 落地形态 |
| `src/api.rs` | 零改动，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `scripts/mod_rollback_guard.py` / `.github/workflows/ci.yml` | 085 已挂 `scan` job，086 只复核不改动 |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff，26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| UX HTML / 两语言包 / 56 PNG | 零 diff |
| 086 新增文件 | `86` 号 spec、`round-085-full-readback.md` / `085-mod-rollback.md` / `round-085.md` / `demos/round-085-mod-rollback.html`、`round-086-full-readback.md` / `086-delivery-closure.md` / `round-086.md` / `demos/round-086-delivery.html`；台账补记与 `docs/index.md` 必读清单 |

## `00:245` 通过标记条件显式核（A244 要求显式核）

| 条件 | 本轮判定 |
| --- | --- |
| ① 8.1 独立验证结论为「通过」 | 不满足：独立验证「部分通过」，存在已失败 / 未证实 / 未启动 |
| ② 所有结论均为「已证实」 | 不满足：E213–E353 已失败；EQ / Q / 5 项 `Planned` 未证实；真实执行层与 UI 渲染未启动 |
| ③ 自评 ≥ 7 | 满足（7） |
| 结论 | `00:245` 第 2 条 + 第 18 节第 2 优先级：**不发通过标记**，明确写「未通过」及原因（A206） |

## 合规核对表

| 约束 | 086 行为 |
| --- | --- |
| `00:133` 逐字保存 | 86 号 spec 3 字节落盘；85 号 spec 已在 085 落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显、防错清单 520 行完整读、11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 16 份 spec 逐字副本；平台文本按 A266 不作指令、不进副本；不重提工具禁用归因 |
| A145 / A140 / A254 | 085 末条工具结果截断，本轮只读远端 ref + 完整 tree 补验；提交前核无锁、无运行中 git 进程 |
| A249 / A268 | 不删 85 / 86 号 spec 规避守卫；两套四件套一次补齐；G2 四份原文列入哈希表、G3 `## 9` / `## 10` 锚点一次排对 |
| A159 / A204 / A243 | 085 的 42 组双向注入结论本轮复核不变；086 无新守卫 |
| A245 / `00:9.2` | 085 既有并发用例偶发 1 FAILED 如实留痕；单独跑 3 次 + 复跑 3 次全量；`src/core/cache.rs` 零 diff、SHA-1 锁定；086 `src/` 零改动 |
| A116 / A258 / A205 | CI 三 job 按真实命令实跑；`scripts/__pycache__/` 保持 0 项；zip 按 `git ls-files -z | zip -@` 打包 |
| A252 / A265 | 全量 726 / 0 注明分段求和口径；两套演示五数组 16 项对齐 |
| A216 / A206 | 增量推送后逐项 ALL_MATCH 才写补记，不用模板值冒充 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` / `00:207` | 设计说明只走对话不进仓库；本轮无新形态防错项，防错清单零改动，不凑条目 |
| `11:26` 用户标「不要写到任何地方」的分句 | 不写进 085 / 086 任何新增文档，仅 11 号逐字副本内保留 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-086-*，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-086-1 | 连续十七轮未通过 | 按 `00:248` 用户当轮「干」覆盖，不中断但逐条回显卡点 |
| D-086-2 | 本轮性质 | **085 交付闭环轮**，`src/` 零改动、零新增第三方、不新开功能池项（068 / 084 先例 + A249） |
| D-086-3 | 功能池 | AX04 保持 `DataLayer`；5 项 `Planned` 不变；AX08 七锚点登记为 087 输入 |
| D-086-4 | 提交范围 | 085 / 086 全部产物一次提交；A11 逐项核 9 项初始 diff + 文档新增 |
| D-086-5 | 推送 | `scripts/api_push.py` 以 `base_tree` 增量 POST，`force=false`；推送后逐项 ALL_MATCH 写进 `rounds.md` 086 补记 |
| D-086-6 | 构建产物与 zip | `scripts/__pycache__/` 保持 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1`；两个 zip 按 `git ls-files -z | zip -@` 重打 |
| D-086-7 | Q / EQ | 不代拍；Q-082-01 / 02 / 03 与历史 26 组 Q、EQ-01 ~ EQ-13、4 条 Q-C 保持未证实 |
| D-086-8 | 状态分层与通过标记 | AX04 数据层 085 已实现 / 已验证；086 交付层已闭环；真实 jar 禁用执行与 UI 渲染未启动；不发通过标记 |

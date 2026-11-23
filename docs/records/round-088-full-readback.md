# 088 开工逐字复读记录

开工 `Tue Nov 24 00:02:16 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节完整读、分两段回显（1–260 / 261–520），末条仍为 A271。`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮逐行全文回显（A211 真读全文；A244 要求真读原文与防错清单全文并记行数）。按 A182：回显的是 00 全文、防错清单两段全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。本表哈希记录于 088 四件套写毕、台账补记写毕之前的读时刻；台账与 index 补记后的字节 / 哈希以交付快照为准。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295 |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88 |
| `docs/spec/88-round-088-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/87-round-087-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/86-round-086-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/72-round-072-instructions.txt` | 117 | 0 | `6a42bb6208266676d4c80c55797fd79e1752b2766d7ff81349a2e6fffda7070a |
| `docs/decisions/068-delivery-reconciliation.md` | 8468 | 90 | `0ece2de9960d48a8e52622595f743f7bd65472f6e8467452f65f64443598b796 |
| `docs/decisions/084-delivery-closure.md` | 14011 | 110 | `1e21e89361bbef2657da3dae265155f68110ce63537169341098966d8f22806c |
| `docs/decisions/087-delivery-closure.md` | 14779 | 108 | `16348be71d651750f2a19f7642967ff3e7f1f9845a9c9baf99c90bd0a86d7b9a |
| `docs/decisions/088-instance-import-delivery.md` | 本轮生成 | — | — |
| `docs/records/round-087-full-readback.md` | 18579 | 158 | `79ec82415c8eb401a7f3df064eae33280f384d516513fa77116e3d47fcf71065 |
| `docs/records/round-088-full-readback.md` | 本轮生成 | — | — |
| `docs/verification/round-087.md` | 11611 | 94 | `fc1300f138cb4339440967758f98b418e80225e2df9c40586a9958953e82b28c |
| `docs/verification/round-088.md` | 本轮生成 | — | — |
| `demos/round-087-delivery.html` | 14979 | 68 | `9ee90e851447cacafba94c1e4ba95cf5c116743ebac2d7cea94ba7c0f46f68a3 |
| `demos/round-088-instance-import.html` | 本轮生成 | — | — |
| `src/core/instance_import.rs` | 27706 | 842 | `6085569e9f2f5eb863cdf0f0bc62f431549eb135e5d10bd5bbf0a0b836e1269c |
| `scripts/instance_import_guard.py` | 13500 | 285 | `5fb6522cf60f7da83aba270d319d3739263440c808980c4405d4160a9c3a5a6d |
| `src/core/ax.rs` | 4633 | 100 | `591202fe0807e8663d9b4c7e1b6ab1d40c1152f7b508ef3a2d7d6817132964ce |
| `src/core/boot.rs` | 18148 | 562 | `4c1037d55a8ef2b1b30ec6f91452bb19b88cf05e5948ffab9081c56546420d3e |
| `src/core/mod.rs` | 865 | 46 | `3a55a595c5e54c6d35a41cfc80061857ec63b075c4c7a057ec1714f85e768057 |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0 |
| `scripts/ax_guard.py` | 2027 | 49 | `145bbc7f0c7e5148281d96d6655d7a3f7a5739cc0c40bdd84ada9e1c6d398c1c |
| `.github/workflows/ci.yml` | 4974 | 139 | `e7aa7020f12e3ad8930f5edd1c5e8969af9176f37d05340513cbf78eebfa3687 |
| `Cargo.toml` | 916 | 37 | `47346e19c7e0946a55400c83a76e38c94b1d9fa0b90c9b63bac1717316080067 |
| `Cargo.lock` | 3520 | 174 | `bd20d10a30d51c8488fede122dca5ff9224313ca7abb794f66673689daf04044 |
| `THIRD-PARTY-NOTICES.md` | 22344 | 309 | `ac0941e2e2b5300791e036113e31e775c43399da9437460e565329af609babbf |
| `docs/records/rounds.md` | 346656 | 3383 | `d5389fd0d80738d2a301500091d8531588a8a9938f987a16253cfd84e7822d83 |
| `docs/records/ax-feature-pool.md` | 30731 | 231 | `e972713dbc4a2e98f18b19dcebba2943cb6082e432d8be85cc24a1ce37fcdbb7 |
| `docs/index.md` | 49938 | 636 | `eb2e7ea2b79b4050b4b283d4380ef3c5debd7fe224e30f02df2733745fc79b08 |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `88-round-088-instructions.txt:1` | 逐字 3 字节 `干`（SHA-256 `9ee0280b…`，无换行），与 87 / 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号 spec 同形态 |
| `87-round-087-instructions.txt:1` | 逐字 3 字节 `干`，087 轮已落盘 |
| `72-round-072-instructions.txt:1` | 117 字节工具澄清句，已在 072 处理并撤回 071 归因（E251） |
| `11:15` / `11:222` | 第 15 条：整合包一键安装，可以拖到主界面直接安装 |
| `11:21` | 拖动安装什么东西的时候，就会显示一个拖动到此处的页面 |
| `12:35` | 整合包导入导出（mrpack / CurseForge zip） |
| `12:36` | 拖拽安装模组 / 插件 |
| `12:40` | 实例模板与克隆 |
| `12:41` | 实例导出 / 导入（可移植实例） |
| `00:133` / `00:34` / `00:260` | 逐字保存、每轮开工完整读 00 与防错清单——本轮执行 |
| `00:137` / `00:245` / `00:248` | 接口终点、通过标记条件、用户当轮明确指令优先——本轮显式核一遍 |
| `00:230` | 每轮联网核实现有时间与上游版本状态——本轮执行远端 ref 与时间核实 |
| `00:9.1` / `00:9.2` / `00:207` | 连续未达通过、测试锁定、文档不凑条目 |
| `ai-errors.md:59` | A50 mrpack 导入不做路径穿越校验（关联 MS07） |
| `ai-errors.md:332` | A165 路径校验用标准库 `Component` 逐分量判定，不要自己删 `../` 字符串 |
| `ai-errors.md:472` | A236 清理设置类功能不能按目录清空 |
| `ai-errors.md:502` | A260 只算路径 / 只算判定的纯函数要用守卫解析函数体核不含 `fs::` 写操作 |
| `ai-errors.md:487` | A249 一轮落地代码、下一轮才补交付时，按新落盘 spec 要求两套四件套；不删 spec 规避守卫 |
| `ai-errors.md:512` | A266 平台拼入用户位次的文本不得当成用户当轮指令 |
| `ai-errors.md:513` | A267 改功能池状态前先读真实 `name` slug |
| `ai-errors.md:514` | A268 G2 四份原文与 G3 的 `## 9` / `## 10` 锚点一次排对 |
| `docs/decisions/087-delivery-closure.md:12` | 087 唯一下一步写「088 按功能池落下一项」，本轮按 A202 打开核过 |

## A248 / A266 预检

88 号 spec 逐字副本全文 3 字节 `干`，已落盘。按 A248 开轮核 88 / 87 / 86 / 85 / 84 / 83 / 82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本：88 / 87 / 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号均仅 3 字节 `干`，82 号 159 字节完整句，72 号 117 字节澄清句已在 072 处理。按 A266，平台拼入用户位次的文本不作用户当轮指令、不据此写「未遵守 / 偏离 / 下一步按该行决定」、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080–087 已按同一口径补记，历史回复与历史文件不重写（A181 / A201）。副本里没有的文字不写成用户指令。工具从未禁用，本轮正常调用工具完成验证、提交、推送与打包。

## A145 远端补验与本地真实状态

只读 `GET /git/ref/heads/main` 得 `d5a8427f1426d24f8d8d6054cec2e8a2b4588ecf`（087 补记，parent `247e765`），完整 recursive tree `LOCAL 1260 / REMOTE 1260 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`。本地 HEAD `b7c6d70`（087 补记）、TRACKED 1260、无 `.git/index.lock`、无运行中 git 进程、PYC 0；两个 zip 为 087 轮包（主包 1260 项、`ui-previews.zip` 57 项）。

`DIRTY 8`（A142 副作用复核，逐项列出）：

| 项 | 形态 |
| --- | --- |
| ` M .github/workflows/ci.yml` | 088 新增 `instance_import_guard` step |
| ` M scripts/ax_guard.py` | 显式断言表加入 `'AX08'` |
| ` M src/core/ax.rs` | AX08 `Planned → DataLayer`，`Planned` 计数断言 5 → 4，DataLayer 表加入 `"AX08"` |
| ` M src/core/boot.rs` | `LOADED_MODULES` 在 `core.instance_drop` 之后、`dispatcher.launcher` 之前插 `core.instance_import` |
| ` M src/core/mod.rs` | 追加 `pub mod instance_import;` |
| `?? docs/spec/88-round-088-instructions.txt` | 本轮逐字落盘 |
| `?? scripts/instance_import_guard.py` | 088 新守卫 13072 字节 |
| `?? src/core/instance_import.rs` | AX08 数据层 842 行 / 28 个单测 |

A249 形态判定：088 代码与守卫在上一轮落地（工具结果未给最终回复），88 号 spec 本轮落盘后 `delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-088-full-readback.md`。085 / 086 / 087 四件套已齐并随主快照推送，本轮只缺 088 一套。**不删 88 号 spec 规避守卫、不改守卫断言**，按真实轮次补齐 088 readback / decision / verification / demo 后复跑 OK，FAIL 原样留痕。

## 068 / 084 / 086 / 087 先例与本轮性质（A208 / A202 复核）

按 A202 打开 `docs/decisions/087-delivery-closure.md:12` 核尾部：087 写出「088 按功能池落下一项（剩 5 项 `Planned`：AX07 / AX08 / AX15 / AX20 / AX22）……AX08 七锚点已登记为输入」。按 A267 读 `src/core/ax.rs:24–39` 真实表：AX08 已改 `DataLayer`（conflict 空、ui true），`Planned` 实为 4（`AX07` / `AX15` / `AX20` / `AX22`），`ax.rs:82` 断言 `count_by_state(AxState::Planned) == 4`；24 行分布 `Planned 4` / `DataLayer 19` / `GateOnly 1`。AX08 七锚点 `11:15` / `11:21` / `11:222` / `12:35` / `12:36` / `12:40` / `12:41` 已由代码收窄落地。按 A217 核 `src/core/` 已有 `instance.rs` / `instance_drop.rs` / `instance_import.rs`：前两者为既有模块（070 的实例清理，语义不同、不复用），`instance_import.rs` 为 AX08 本轮数据层。

按 068 / 084 / 086 / 087 先例（用户只发「干」且上一轮交付层断裂时，`src/` 零改动补齐交付闭环），定本轮为 **088 交付闭环轮**（D-088-2 我的默认）：`src/` 零改动、零新增第三方、不新开功能池项、4 项 `Planned` 不变；087 尾部「落下一项」由 088 代码落地完成，不再顺延。按 A208 复核 `b-class-status-recheck.md:85`：EQ-01 ~ EQ-13 仍待拍、未启用，B04 卡 EQ-01 但本轮不动 UI，无「需 EQ 拍板才能动」阻塞层。

## A211 真读全文与 AX08 收窄锚点

本轮真读 00 / 防错 / 11 / 12 号全文，不是只核哈希与台账状态。AX08 七锚点逐字复核：`11:15` / `11:222` 整合包一键安装拖到主界面、`11:21` 拖动到此处页面（UI 层未启动）、`12:35` mrpack / CurseForge zip 导入导出、`12:36` 拖拽安装模组 / 插件、`12:40` 实例模板与克隆、`12:41` 实例导出 / 导入（可移植实例）。A50 / A165 收窄：mrpack 路径穿越校验用 `std::path::Component` 逐分量判定，拒 `ParentDir` / `RootDir` / `Prefix` / `CurDir`，不做字符串清洗；A236 保护清单、A260 纯查询段无 `fs::` 写操作、A154 显式 code 枚举、A269 / A270 常量表 EXPECTED 逐值 + impl 段字面量比对，均由 `instance_import_guard.py` 持有。

## A244 合规复核

| 用户口径 | 原文锚点 | 本轮可核对证据 | 结论 |
| --- | --- | --- | --- |
| 用开源的 | `00:32` / `00:19` / `11:2` / `11:11` | `Cargo.lock` `[[package]]` 26 项、`vendor/` 25 个第三方目录、`docs/licenses/` 58 份 LICENSE 全文、`THIRD-PARTY-NOTICES.md` 309 行、`code-ownership-audit.md` 逐轮登记；085–088 零新增第三方 | 已证实 |
| 保证许可证 | `00:249` / `00:133` / `11:26` / `11:4` / `11:258` / A44 / A45 / A100 / A139 / A141 | 088 复用既有 `serde_json` / `anyhow` / `robust` / `Envelope` / `diag_line`，不引新 crate；58 份 LICENSE 与 309 行声明未变 | 已证实 |
| 停下来问，不硬上 | `00:249` | 085–088 零新增第三方；无语义等价库可换的项目特有口径按 `00:6.1` 只写事实 | 已证实 |
| 源与产物对比 | `11:26` / A45 | 088 新增文件为项目自写数据层，非拼接上游源码；真实字节比对执行层未启动 | 已证实（零拼接）+ 未启动 |

## `00:230` 本轮联网核实

| 项 | 一手结果 |
| --- | --- |
| 当前时间 | `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` → `Tue Nov 24 00:02:16 CST 2026` |
| 远端 ref | `GET /git/ref/heads/main` RC=200 → `d5a8427f1426d24f8d8d6054cec2e8a2b4588ecf` / parent `247e765` / message `round 087 addendum: remote sync 1260 files ALL_MATCH` |
| 完整 tree | `1260 / 1260 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 上游版本状态 | 082 已核 `ViaVersion/ViaNBT`：`pushed_at=2026-10-27T14:24:29Z`、`default_branch=master`、`archived=false`、tags `3.0.0` / `2.1.3` / `2.1.2`；085–088 无新增上游依赖，复核状态不变 |

## `00:9.1` 连续未达通过的处置（D-088-1）

069–087 连续**十九**轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 088 当轮明确指令「干」按 `00:248` 覆盖。不中断推进，但卡点在本轮回复、决策、四值里逐条回显（A164）：E213–E357 历史已失败未清零；E360 / E361 / E362 本轮新登记；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；4 项 `Planned` 与真实执行层 / UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不改测试、不降验收项。

## `00:137` 接口终点核对（A244 要求显式核）

| 引用点 | 088 形态 |
| --- | --- |
| `src/core/instance_import.rs` | 上一轮落地 842 行 / 28 单测，本轮零改动；六张白名单表、四枚举显式 code、`Component` 路径校验、五条矛盾态规则六处调用、单条突变、原子写、统一信封十值载荷 |
| `src/core/ax.rs` / `boot.rs` / `mod.rs` | 上一轮已接 AX08 `DataLayer` / `core.instance_import` / `pub mod instance_import;`，本轮零改动 |
| `src/api.rs` | 零改动，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `scripts/instance_import_guard.py` / `.github/workflows/ci.yml` | 上一轮已挂 `scan` job；本轮仅修守卫 5 处断言缺口（E361），`src/` 零改动 |
| `scripts/ax_guard.py` | 上一轮已加 `'AX08'`；本轮零改动，历史缺口 E362 单列 |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff，26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| UX HTML / 两语言包 / 56 PNG | 零 diff；AX08 `ui: true` 但 UI 渲染层未启动（A100） |
| 088 新增 | 88 号 spec、`round-088-full-readback.md` / `088-instance-import-delivery.md` / `round-088.md` / `demos/round-088-instance-import.html`；台账补记与 `docs/index.md` 必读清单 |

## `00:245` 通过标记条件显式核（A244 要求显式核）

| 条件 | 本轮判定 |
| --- | --- |
| ① 8.1 独立验证结论为「通过」 | 不满足：独立验证「部分通过」，存在已失败 / 未证实 / 未启动 |
| ② 所有结论均为「已证实」 | 不满足：E213–E362 已失败；EQ / Q / 4 项 `Planned` 未证实；真实执行层与 UI 渲染未启动 |
| ③ 自评 ≥ 7 | 满足（7） |
| 结论 | `00:245` 第 2 条 + 第 18 节第 2 优先级：**不发通过标记**，明确写「未通过」及原因（A206） |

## 合规核对表

| 约束 | 088 行为 |
| --- | --- |
| `00:133` 逐字保存 | 88 号 spec 3 字节落盘；85–87 号 spec 已在对应轮次落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显、防错清单 520 行完整读、11 / 12 号原文 268 / 64 行全文回显 |
| A248 / A266 / E251 | 开轮核 18 份 spec 逐字副本；平台文本按 A266 不作指令、不进副本；不重提工具禁用归因 |
| A145 / A216 | 远端 `d5a8427` / `1260 / 1260 ALL_MATCH True` 补验；推送用 `base_tree` 增量、`force=false` |
| A140 / A254 | 提交前核无锁、无运行中 git 进程 |
| A142 | 分段失败后逐项核 8 项 DIRTY 的真实副作用，不凭幂等判据臆断 |
| A249 / A268 | 不删 88 号 spec 规避守卫；补齐 088 四件套；G2 四份原文列入哈希表、G3 `## 9` / `## 10` 锚点一次排对 |
| A159 / A204 / A243 | 34 组双向注入全真 FAIL、0 假 OK、恢复 OK、哈希复原；首轮 36 组发现 5 假 OK + 1 跨守卫缺口，修守卫后重跑 |
| A245 / `00:9.2` | 088 `src/` 零改动，715 断言一字未改、未加跳过标记 |
| A116 / A258 / A205 | CI 三 job 按真实命令实跑；`scripts/__pycache__/` 保持 0 项；两个 zip 按 tracked 清单重打 |
| A252 / A265 | 全量 754 / 0 注明分段求和口径；088 演示五数组 16 项对齐 |
| A267 | 改功能池状态前先读真实 slug；本轮不改状态，只复核 `Planned 4` |
| A50 / A165 / A260 | 路径校验、纯查询段、保护清单由守卫逐项持有 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` / `00:207` | 设计说明只走对话不进仓库；本轮无新形态防错项，防错清单零改动，不凑条目 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-088-*，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-088-1 | 连续十九轮未通过 | 按 `00:248` 用户当轮「干」覆盖，不中断但逐条回显卡点 |
| D-088-2 | 本轮性质 | **088 交付闭环轮**，`src/` 零改动、零新增第三方、不新开功能池项（068 / 084 / 086 / 087 先例 + A202 + A249） |
| D-088-3 | 功能池 | AX08 保持 `DataLayer`；4 项 `Planned` 不变；087 尾部「落下一项」由 088 代码落地完成，不再顺延 |
| D-088-4 | 守卫缺口 | 修 `instance_import_guard.py` 5 处断言缺口并双向注入重跑；`ax_guard.py` 历史缺口 E362 单列登记、本轮不扩大 diff |
| D-088-5 | 提交范围 | 088 代码 / 守卫 / 五处修改 + 四件套 + 台账一次提交；A11 逐项核 diff 范围 |
| D-088-6 | 推送 | `scripts/api_push.py` 以 `base_tree` 增量 POST，`force=false`；推送后逐项 ALL_MATCH 写进 `rounds.md` 088 补记 |
| D-088-7 | 构建产物与 zip | `scripts/__pycache__/` 保持 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1`；主 zip 按 `git ls-files -z \| zip -@`、`ui-previews.zip` 按 PNG 清单重打 |
| D-088-8 | Q / EQ | 不代拍；Q-082-01 / 02 / 03 与历史 26 组 Q、EQ-01 ~ EQ-13、4 条 Q-C 保持未证实 |
| D-088-9 | 状态分层与通过标记 | AX08 数据层已实现 / 已验证；真实解压落盘、拖拽页面、UI 渲染未启动；不发通过标记 |

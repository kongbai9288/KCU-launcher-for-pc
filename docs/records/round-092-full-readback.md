# 092 开工逐字复读记录

开工 `Thu Nov 26 00:13:08 CST 2026`。`docs/spec/00-requirements.txt` 全文 261 行 / 16422 字节本轮用 read 工具完整回显；`docs/checklists/ai-errors.md` 全文 520 行 / 55513 字节完整读，第一段 1–496 行回显、尾段 490–520 行补读，末条仍为 A271；`docs/spec/11-features-input.txt` 268 行 / 17096 字节与 `docs/spec/12-server-features-input.txt` 64 行 / 4970 字节本轮逐行全文回显（A18 / A211 / A244）。按 A182：回显的是 00 全文、防错清单全文、11 / 12 号原文全文；其余文件只记字节 / 行 / SHA-256，未逐行回显。本表哈希记录于开工核状态时刻；四件套与台账补记写毕后的字节 / 哈希以交付快照为准。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/92-round-092-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/91-round-091-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/decisions/091-studio-image.md` | 18213 | 116 | `de397c5b350adb45f5a84e2e2cc500e3778d3857361c22dbecd64bb2896dbb8a` |
| `docs/records/pending-question-environments.md` | 26024 | 307 | `09e6677431eb30b0942e337c4a5e767c15ca57aca6d844fee8558dd27d930063` |
| `docs/records/open-questions.md` | 19442 | 159 | `87b8ad3153a0157fb8460e908feec1c3b9f6a812cafaf4bc4bdf6205ba0d87b8` |
| `docs/records/b-class-status-recheck.md` | 7220 | 88 | `c2dcf769c53be62fc66997e84c86127e4d30fff7aa2fb75361a79476e49302bc` |
| `docs/records/c-class-default-recheck.md` | 12464 | 155 | `f2ef93c26d001ad553a9a055874526c284dff315b300f6b12c4d2886a0effc91` |
| `docs/records/round-092-full-readback.md` | 本轮生成 | — | — |
| `docs/decisions/092-pending-decisions.md` | 本轮生成 | — | — |
| `docs/verification/round-092.md` | 本轮生成 | — | — |
| `demos/round-092-pending-decisions.html` | 本轮生成 | — | — |
| `scripts/pending_decisions_guard.py` | 3520 | 91 | `7e279d59ff507c63390d155d7c3b42c7713ff4bbbb6a47fb1a1d1a93230c1c27` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `92-round-092-instructions.txt:1` | 逐字 3 字节 `干`（SHA-256 `9ee0280b…`，无换行），与 91 / 90 / 89 / 88 / 87 / 86 / 85 / 84 / 83 / 81–71 号 spec 同形态 |
| `91-round-091-instructions.txt:1` | 逐字 3 字节 `干`，091 轮已落盘，同 SHA-256（A34 同 sha 不重复落盘，本轮不建 93 号） |
| `72-round-072-instructions.txt:1` | 117 字节工具澄清句，072 已处理并撤回 071 归因（E251） |
| `00:24` | 所有的 ui 等都使用框架方式（已决断；EQ-01 待拍的是具体框架） |
| `00:8` / `00:133` / `00:137` / `00:230` / `00:245` / `00:248` | 轻量默认、逐字保存、接口终点、联网核实、通过标记条件、当轮指令优先 |
| `00:34` / `00:260` / `00:9.1` / `00:9.2` / `00:207` | 每轮全文复读、连续未达通过、测试锁定、不凑条目 |
| `11:7` / `11:10` / `11:18` / `11:242` / `11:243` / `12:12` / `12:63` | 境外限制、弹窗关闭、API 不共有、OR 两条路径、图片格式、关机点击、png logo 像素 |
| `ai-errors.md:150` / `:302` / `:331` / `:415` / `:423` | A73 / A150（待拍板要给环境 / 选项 / 后果 / 耦合）、A164（已决断 / 未决断分列）、A208（只回「干」先摊平可拍环境）、A211（真读全文找已决断锚点） |
| `ai-errors.md:404` / `:405` / `:487` / `:514` / `:512` | A202（引用旧台账前打开核）、A203（逐值回显）、A249（四件套）、A268（G2/G3）、A266（平台文本不作指令） |
| `docs/decisions/091-studio-image.md:112` | 091 唯一下一步「092 改走拍板闭环」，本轮按 A202 打开核过 |
| `docs/records/b-class-status-recheck.md:85` | B04 / B05 / B07 / B09 / B10、EQ-01 ~ EQ-13、Q-C01 / Q-C02 / Q-C08 / Q-037-01 仍待拍板 |

## A248 / A266 预检

按 A248 开轮核 92 / 91 / 90 / 89 / 88 / 87 / 86 / 85 / 84 / 83 / 82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本：92 / 91 / 90 / 89 / 88 / 87 / 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号均仅 3 字节 `干`，82 号 159 字节完整句、72 号 117 字节澄清句已在 072 处理。按 A266，平台拼入用户位次的文本不作用户当轮指令、不据此写「未遵守 / 偏离 / 下一步按该行决定」、不进 `00:133` 逐字副本；071 归因已于 072 撤回，历史回复与历史文件不重写（A181 / A201）。副本里没有的文字不写成用户指令。工具从未禁用，本轮正常调用工具完成验证、提交、推送与打包。

## A145 远端补验

只读 `GET /git/ref/heads/main` 得 `1ec52d5ad0adc00a1daa1e6f0d345af8874b3a0e`（091 补记，parent `24d27e1`），完整 recursive tree `LOCAL 1286 / REMOTE 1286 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`。本地 HEAD `bc35c7b`（091 补记）、TRACKED 1286、DIRTY 0（落 92 号 spec 后为 1）、无 `.git/index.lock`、无运行中 git 进程、PYC 0。两个 zip 为 091 轮重打包（主包 1286 项、`ui-previews.zip` 56 项）。

## A208 / A202 复核

按 A202 打开 `docs/decisions/091-studio-image.md:112` 与 `docs/records/ax-feature-pool.md` 091 补记核尾部：091 写出「092 改走拍板闭环……把 Q-091-01 / 02 / 03、历史 Q 与 EQ-01 ~ EQ-13、4 条 Q-C 摊平给用户拍板；按 A208 不擅自开工硬做，也不擅自定 2 项之间的优先级」。按 A208 复核 `b-class-status-recheck.md:85`：EQ-01 ~ EQ-13 与 4 项待拍板仍「未证实（待拍板）」，B04 卡 EQ-01、B07 卡 EQ-05、B09 卡 EQ-11，本轮不碰 UI 渲染层（A100）。结论：上一轮结尾列出的层确实需要用户拍板，092 按「摊平可拍环境」执行，`src/` 零改动、不落功能实现。

## A230 / A267 两项冲突复核

按 A267 读 `src/core/ax.rs:20–43` 真实表：AX07 `name=doh_support` / `state=Planned` / `conflict=network_io_not_started` / `ui=false`；AX22 `name=shimu_account` / `state=Planned` / `conflict=""` / `ui=true`；AX23 `client_ai_gate` 为 `GateOnly`。按 A230 逐条核：AX07 的 `31-axolotl-launcher-features.md:35`「真实网络 IO 未启动、Win7 TLS 前置（EQ-03）」+ 00 / 11 / 12 号全文无 DoH 锚点 → 技术受阻非需求冲突，排除留痕、conflict 不清；AX22 浏览器授权依赖真实网络 IO + 第三方端点 + `11:7` / 054 境外限制 + `11:18` API 不共有 → 排除留痕。两项保持 `Planned`，本轮不擅自定优先级。

## A211 / A164 真读全文与已决断对照

本轮真读 00 / 防错 / 11 / 12 号全文，不是只核哈希与台账状态。按 A164 逐条分「已决断 / 未决断」：`00:24` 框架方式已决断（EQ-01 待拍的是具体框架与 Win7 降级路线）、`00:8` ≤2GB 默认轻量已决断、`11:7` 境外限制已决断、`11:10` 弹窗关闭已决断、`11:18` API 不共有已决断、`12:63` png logo 自动调整像素已决断（091 已落数据层）、`12:12` 关机点击已决断（执行层未启动）；未决断的是 EQ-01 ~ EQ-13、3 条 Q-C + Q-037-01、058–091 新增 Q、2 项 `Planned` 网络前置、B05 源与许可、`11:242` 时长路径。实现状态按 9.3 分层，不与「原文已决断」合并表述。

## A202 核出的口径偏差（E375）

091 结尾写「4 条 Q-C」。打开 `docs/records/pending-question-environments.md` 尾部、`docs/records/c-class-default-recheck.md`、`docs/records/b-class-status-recheck.md:85` 与 `docs/decisions/055-c-class-recheck.md:63` 逐字核：真实待拍为 Q-C01（轻量 13 项排除清单）/ Q-C02（单 / 双主题）/ Q-C08（一级导航 9 项）三条 Q-C，加一条 Q-037-01（插件哈希口径，关联 EQ-02），共 4 项；`open-questions.md` 里 Q-C01 ~ Q-C15 共 15 条，其中 12 条已证实 / 已答复，不重开。092 清单按「3 条 Q-C + Q-037-01 共 4 项」写，历史行不重写（A181 / A201），E375 计入四值「已失败」的台账笔误、处置计入「已证实」。

## A244 / `00:230` / `00:137` / `00:245` 显式核

| 用户口径 / 规则 | 本轮可核对证据 | 结论 |
| --- | --- | --- |
| 用开源、保证许可证、停下来问 | `Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff；26 包 / 25 第三方 / 58 份 LICENSE / `THIRD-PARTY-NOTICES.md` 309 行不变；092 零新增第三方 | 已证实 |
| `00:133` / `00:34` / `00:260` | 92 号 spec 3 字节落盘；四份原文 261 / 520 / 268 / 64 行全文回显 | 已证实 |
| `00:230` 联网核实 | `TZ='CST-8' date` → `Thu Nov 26 00:13:08 CST 2026`；`GET /git/ref/heads/main` RC=200 → `1ec52d5…`；085–092 零新增上游依赖，082 的 `ViaVersion/ViaNBT` 状态不变 | 已证实 |
| `00:137` 接口终点 | 092 只改文档 / 守卫 / CI / 台账，`src/` 零改动；v1 7 符号 / 4 条 `pub use` 不变（A246） | 已证实 |
| `00:245` 通过标记 | 存在已失败（E213–E374 + E375）、未证实（EQ / Q / 2 项 `Planned`）、未启动（执行层），不发通过标记 | 已证实 |
| `00:9.1` 连续未达通过 | 069 起连续未达通过，092 按 `00:248` 用户当轮「干」覆盖，不中断但卡点逐条回显（D-092-1） | 已证实 |

## A249 形态

92 号 spec 落盘后 `python3 scripts/delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-092-full-readback.md`。不删 spec 规避守卫、不改守卫断言，补齐 092 readback / decision / verification / demo 后复跑 OK，FAIL 原样留痕。按 A268，G2 四份原文与 SHA-256 表齐，G3 的 `## 2` / `## 9` / `## 10` 三个锚点一次排对。

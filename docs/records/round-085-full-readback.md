# 085 开工逐字复读记录

085 开工 `Mon Nov 23 12:06:50 CST 2026`。四件套于 086（`13:20:33 CST 2026`）按 A249 补齐；历史回复与历史行不重写（A181 / A201）。按 A182：回显的是 `00-requirements.txt` 全文 261 行 / 16422 字节、`ai-errors.md` 全文 520 行 / 55513 字节（分 1–260 / 261–520 两段）、`11-features-input.txt` 全文 268 行 / 17096 字节、`12-server-features-input.txt` 全文 64 行 / 4970 字节；其余文件只记字节 / 行 / SHA-256，未逐行回显。本表哈希记录于 085 代码写毕、086 四件套落盘前的读时刻；提交快照以最终 `git ls-files -s` 为准。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295 |
| `docs/checklists/ai-errors.md` | 55513 | 520 | `692095a054dbc08592d1f2d28a6c118ee9eda741106786cd81f27370882bdfcd |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88 |
| `docs/spec/85-round-085-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/86-round-086-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/spec/84-round-084-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655 |
| `docs/decisions/084-delivery-closure.md` | 14011 | 110 | `1e21e89361bbef2657da3dae265155f68110ce63537169341098966d8f22806c |
| `src/core/world_editor.rs` | 37285 | 936 | `60097ae4ea2659d9e91399d7164aa9fd5f546bc9a5cbe3b83d04f0442733a68a |
| `src/core/ax.rs` | 4623 | 100 | `e3a91e06bff5cdd71cbdb2938ce013c569d79264606c5f8dce7c7a9e901bb0bf |
| `src/core/boot.rs` | 18120 | 561 | `40a75455d7c5c43858752ac4dab15837e0a90d0af1b3a8fc8a95068bcd0ce273 |
| `src/core/mod.rs` | 840 | 45 | `ecc9e65c4a94d906dee0abe2fb0278f1f11c878811f3c8cf78df0060fa6f19d8 |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0 |
| `scripts/world_editor_guard.py` | 10761 | 232 | `c5e2e4826b1f5f1dd4bd04ea1fe07e2e2a18f816d6b7c9d38f351bd4a523bd58 |
| `scripts/ax_guard.py` | 2019 | 49 | `13e9ea4b202bdb427f83e5a421c2c48ea84bc6acf8c74582fff9d1770d5a1a7a |
| `src/core/mod_rollback.rs` | 37354 | 990 | `696cb7ef7d88964e33664566bf7dee52b1952ee3343cdcff363a3be56c05fb64 |
| `scripts/mod_rollback_guard.py` | 12393 | 269 | `1e4cab4382c9f24fc4dd786b0c7d90b4dcfe22bb99e8a8241324c8707137fddd |
| `docs/records/rounds.md` | 335543 | 3373 | `ea9f8718a16878454b9322eb206e3a126986e452add508c7b4a89465c90a0f13 |
| `docs/records/ax-feature-pool.md` | 29194 | 223 | `918474f9dfd60a13831c2b6be959efb08ce87c1c056f623e6e2005906799858c |
| `docs/index.md` | 49398 | 636 | `5bcb3f3e5455e081bb79d3b34816446f6879bd13e311c463fc1b7010f1aee106 |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `85-round-085-instructions.txt:1` | 逐字 3 字节 `干`（SHA-256 `9ee0280b…`，无换行），与 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号 spec 同形态 |
| `11:244` | 第 36 条：重复模组同一版本警告；用户选择继续则继续；版本高于时由用户选择版本后再进行；不一次性堆页面，按顺序排列、都在一个弹窗中、上面有页码；出现别的问题且用户还没选择会增加，每一个都是单独的选择 |
| `12:8` | 模组更新功能，版本更高同一模组的 jar 自动禁用低版本模组，单个实例页面才能用 |
| `12:33` | 配置快照与回滚（server.properties、ops.json、模组配置等） |
| `12:39` | 服务端/加载器版本回滚 |
| `00:133` / `00:34` / `00:260` | 逐字保存、每轮开工完整读 00 与防错清单 |
| `00:137` / `00:245` / `00:248` | 接口终点、通过标记条件、用户当轮明确指令优先 |
| `00:175` / `11:15` | 同类功能复用同一模块、文件归中 |
| `00:9.2` / `00:9.3` | 测试锁定、状态分层 |
| `A211` / `A244` / `A267` | 真读全文找已决断条目、合规产物、改功能池前读真实 slug |
| `A249` / `A268` | 双套四件套形态、G2/G3 锚点 |

## A145 远端补验

085 开工只读 `GET /git/ref/heads/main` 得 `c025a78b945e89213f85e985dc39f8f2f9e36091`（084 补记，parent `918cd90`），完整 recursive tree `1243 / 1243 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`。本地 HEAD `f66965a`、TRACKED 1243、DIRTY 0、无 `.git/index.lock`、无运行中 git 进程、PYC 0。

## A248 / A266 预检

85 号 spec 逐字副本全文 3 字节 `干`，已落盘。按 A266 与 `72-round-072-instructions.txt` 逐字澄清，平台拼入用户位次的文本不作用户当轮指令、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080 / 081 / 082 / 083 / 084 已按同一口径补记。工具从未禁用，085 正常调用工具完成代码落地与验证。

## A211 真读全文找出的 AX04 已决断锚点

按 A267 先读 `src/core/ax.rs:21` 真实 name 为 `mod_rollback`、conflict 为空、`ui: true`。四锚点（`11:244` / `12:8` / `12:33` / `12:39`）由 084 真读全文找出登记为 085 输入；085 真读 00 / 防错 / 11 / 12 号全文后按四条收窄落地，未代拍 Q / EQ。

## A164 逐条分已决断 / 未决断

| 条目 | 状态 |
| --- | --- |
| 084 唯一下一步「085 按功能池落 AX04」 | 已决断 |
| `11:244` / `12:8` / `12:33` / `12:39` | 已决断、不依赖 EQ |
| Q-082-01 / 02 / 03、Q-067 / Q-070 ~ Q-082、EQ-01 ~ EQ-13、4 条 Q-C | 未决断，待用户拍板 |
| 真实模组 jar 禁用执行、配置快照落盘、UI 页码弹窗渲染 | 未启动（085 只落数据层与判定） |

## `00:137` 接口终点核对

| 引用点 | 085 形态 |
| --- | --- |
| `src/` | 新增 `core/mod_rollback.rs`；改 `ax.rs` / `boot.rs` / `mod.rs` |
| `src/api.rs` | 零改动，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `scripts/mod_rollback_guard.py` / `.github/workflows/ci.yml` | 新增守卫并挂 `scan` job |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` | 零 diff；复用既有 `semver` / `serde_json` / `anyhow` |
| UX HTML / 两语言包 / 56 PNG | 零 diff |

## `00:245` 通过标记条件显式核

① 8.1 独立验证结论为「通过」：不满足（部分通过）；② 所有结论均为「已证实」：不满足（存在已失败 / 未证实 / 未启动）；③ 自评 ≥ 7：满足（7）。按 `00:245` 第 2 条与第 18 节第 2 优先级，不发通过标记。

## 逐值回显（A203 / A177）

全部为我的默认，登记 D-085-*，不写成用户已决断：本轮按 084 唯一下一步落 AX04 数据层；不引新第三方；不扩 `api::v1`；不改 UX；不发通过标记；Q / EQ 不代拍。

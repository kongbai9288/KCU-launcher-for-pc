# 066 开工逐字复读记录

开工 `Sat Nov 21 20:17:01 CST 2026`。`00-requirements.txt` 全文（261 行）与 `docs/checklists/ai-errors.md` 全文（479 行）已完整读过，再读 `11-features-input.txt`、`12-server-features-input.txt`、064 当轮指令与隐私政策全文、065 指令、`ax-feature-pool.md` 全文、065 决策。复读在写任何代码 / 文档之前完成，对应 `00:34` / `00:260` 与 A18。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 47323 | 479 | `60d3216f3b013072d437da81bdeb4cdc62700d936dacfaf0dcfff10908832526` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/64-round-064-instructions.txt` | 4813 | 76 | `d20e36a1241c6feb35ed6e0ffbd21d0301448de8db90e47713d6be4a4b4364fc` |
| `docs/spec/64-privacy-policy-v1.1.txt` | 4638 | 77 | `de3b07c70f6747ae220db8e67c6168eed0b35e992c80334581b154cd80a3e8b8` |
| `docs/spec/65-round-065-instructions.txt` | 4 | 1 | `67997353aa5bff040e44079f327ae485087311fa55006035d03e00cfe29ede15` |
| `docs/spec/66-round-066-instructions.txt` | 24 | 0 | `df6c0d1c547459ee6eb92b992efd1b1fe7c4f3ca0978fe2b0e449f0e1d88a53f` |
| `docs/records/ax-feature-pool.md` | 3984 | 55 | `875fe222e4345dd546d0a459c48070c417a3b053b1df33d0cdb2e367f64cfb08` |
| `docs/decisions/065-settings-export-import-cleanup.md` | 8491 | 92 | `781807ad56ba77631b04a12383143fb2e08d2213ebbc268befa988bbfab3b027` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `66-round-066-instructions.txt:1` | `干，遵守我的要求` |
| `00-requirements.txt:33` | `每次交付必须带 HTML 一比一运行逻辑、自我批判、时间戳回显、四值判决、独立验证证据。` |
| `00-requirements.txt:34` | `每轮开工前完整读一遍本文件与文档目录下的防错清单。` |
| `00-requirements.txt:54` | `不做过度抽象、不套设计模式、不偷偷加依赖。` |
| `00-requirements.txt:111` | `禁止顺手改无关文件，差异不超出任务范围。` |
| `00-requirements.txt:112` | `禁止硬编码环境假设（绝对路径、写死架构名、密钥）。` |
| `00-requirements.txt:137` | `每次开动前，确认文件接口最后一层会到哪里，再开始写。` |
| `00-requirements.txt:140-143` | 通过标记三条同时满足 |
| `00-requirements.txt:166` | `每个状态只声明实际达到的那一层，不合并表述。` |
| `00-requirements.txt:175` | `同类功能尽量复用同一个模块` |
| `00-requirements.txt:179` | `任何单点失败不允许导致应用崩溃或无法启动。失败必须可见、可诊断、可回退。` |
| `00-requirements.txt:209-222` | 输出结构 12 项固定 |
| `00-requirements.txt:245` | `有任何未解决的「已失败 / 未证实 / 受阻」，不发通过标记。` |
| `00-requirements.txt:248` | `用户当轮明确指令 > 本文件规则。` |
| `ai-errors.md:415` | A208：只回「干」且结尾列「需 EQ 拍板才能动」的层时，先复核台账状态，不擅自开工 |
| `ai-errors.md:421` | A211：原文里「已决断、不依赖 EQ」的条目要真读全文找，不能只核哈希与台账状态 |
| `ai-errors.md:472` | A236：清理类功能不能按目录清空，要表驱动列保护清单 |
| `ai-errors.md:477` | A241：守卫核常量表不能全文子串匹配 |
| `ai-errors.md:479` | A243：守卫 FAIL 但行为测试仍通过时如实登记，不改测试凑失败 |
| `ax-feature-pool.md:53` | `Planned 21` / `DataLayer 2` / `GateOnly 1` |
| `ax-feature-pool.md:44` | `UI 闸门未触发前只落数据层与编排` |
| `047-rollback-version-precedence.md:89` | EQ-13 = `Q-047-01 回滚是否需第三条件手动同意`，待拍板 |

## 「遵守我的要求」合规核对（本轮显式复核）

| 约束 | 本轮行为 |
| --- | --- |
| `00:34` / `00:260` 完整读原文与防错清单 | 真读 00 全文 261 行、防错清单 479 行，非 grep 摘要 |
| `00:133` 逐字保存当轮指令 | `docs/spec/66-round-066-instructions.txt` 24 字节，SHA-256 锁定 |
| A208 / A211 复核台账再开工 | 065 结尾预告「按功能池落下一项」；核 `open-questions` 与 047：EQ-13 是回滚第三条件，AX04 卡它；AX06 不碰 EQ |
| `00:137` 接口终点 | 新模块只被 `core/mod.rs`、`boot.rs LOADED_MODULES`、`ax.rs`、`ax_guard.py`、新守卫、CI 引用；**`api::v1` 不加符号**（062 稳定面 7 符号不动）；无 UI / 无网络调用方 |
| `00:54` / `00:111` 零新增依赖、不改无关文件 | 复用 `serde_json` / `robust` / `diagnostics`；不改 `stats.rs`、`settings_io.rs`、`consent.rs` |
| `00:166` 状态分层 | 只把 AX06 数据层标 `DataLayer`；顶部栏任务进度 UI 明确写未启动 |
| `00:245` 通过标记 | 存在未证实 / 未启动项，不发通过标记 |
| `00:209-222` 输出结构 | 本轮回复按 12 项组织 |
| `00:6.1` 仓库边界 | 决策只写「决定了什么、约束、验证条件」；动机走对话 |

## 选项目的复核结论

065 结尾：「继续『干』按功能池落下一项（剩 21 项 Planned）」。逐项核 21 项后，**AX06 download_history** 的数据层满足：不碰 EQ-01 ~ EQ-13、不碰真实网络 IO（只记不请求）、不碰 UI 闸门（顶部栏进度属 UI，不做）、无需新增第三方。AX09 与 036 / EQ-13 边界相邻、AX08 需 zip 解析库、AX04 卡 EQ-13、AX07 卡网络 IO，均不本轮动。

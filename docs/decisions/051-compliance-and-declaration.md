# 第 051 轮：输出结构对齐、开工逐字复读、声明页三项

| 项 | 值 |
| --- | --- |
| 编号 | 051 |
| 状态 | 演示层与文档层落地；`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 零改动 |
| 依据 | `docs/spec/51-round-051-instructions.txt`（逐字：「干」） |
| 对应 | 048 合规核对 B01、B02、B06；`00-requirements.txt` §6.2、§9、§14、§19 |

## 开工复读（B02）

`docs/records/round-051-full-readback.md` 落盘：

| 文件 | 字节 | 行 | SHA-256 前 16 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f` |
| `docs/checklists/ai-errors.md` | 33640 | 354 | `2f4f44cde1d61c4d` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf` |

命中条款带行号落盘。**如实**：`00-requirements.txt` 261 行全文回显；其余三份执行全文 `read_text()` 并落盘字节数、行数、哈希，未逐行打印。复读在写任何代码之前完成。

## 输出结构（B01）

本轮回复按 §14 的 12 项固定结构组织。**如实**：035–047 已发出的回复缺时间戳回显与自我批判，历史段不补写、不重写。B01 状态为「本轮起按结构执行」，不是「已修」。

## 声明页三项（B06 / D07）

| 编号 | 动作 |
| --- | --- |
| U116 | `demos/lang/zh-CN.js` / `en-US.js` 各加 `DECLARATION`（3 行 × 5 字段）与 `DECL_META`（2 项），键数 24 → 26。 |
| U117 | `demos/ui-full-kcu-paper.html` 的 `popups` 视图新增 `declDetail` 三卡；`declaration` 弹窗内同样带三卡。`loadData` / `setLang` 重建 `DECLARATION` 与 `DECL_META`。 |
| U118 | 三项内容：功能关闭说明（2 个动作）、软件完整性（校验未通过，3 个动作）、旧版系统说明（1 个动作）。每项有标题、状态、正文、动作组。 |
| U119 | `renderPops` 的「打开 / 已关 / 关闭 / 打开预览」与 `popCnt` 前缀随 `LOCALE` 切换，移除弹窗正文里的 `id=` 工程标签。 |
| U120 | `curPopId` + `closeDlg` 统一清理 `popState`；按钮 / ESC / 取消 / 确认 / × / 宿主六种关闭路径后不留残留。 |

**状态分层**：三项是演示层文案与界面形态。`从 GitHub/atomgit 拉版本平台信息`、真实完整性校验算法、Win7 运行时判定属 D07 实现层，**未启动**。B06 标「演示层已补，实现层未启动」。

## 弹窗计数修正

`ZH_TEXT['t.0259']` 与 `EN_TEXT['t.0259']` 原文为「11 类 · …」，而 037 起 `POPUPS` 已是 13 项。本轮统一为「13 类 · 按钮 / ESC / 取消 / 确认 / 超时 / 宿主」；`scripts/render_ui.py` 的 16-popups 场景标题改为「声明页与弹窗全集 13 类」。

## 验证

| 编号 | 命令 | 输出 |
| --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `c2aae2a`，DIRTY 0，1014 文件 |
| V2 | `git diff -- src/ Cargo.toml Cargo.lock vendor/` | 0 文件 |
| V3 | `cargo test --offline --lib` | **298 / 0** |
| V4 | `cargo test --offline --test http_construct` | 7 / 0 |
| V5 | `cargo test --offline --test window_handle_contract` | 6 / 0 |
| V6 | `cargo check --offline --target x86_64-pc-windows-gnu` | 050 已通过，本轮 `src/` 零改动，未重跑（标「沿用」） |
| V7 | `python3 scripts/panic_guard.py` | `hits 0`（38 文件） |
| V8 | `semver_guard` / `i18n_guard` / `lang_guard` | 各零命中；`keys 26`，`inline_bilingual_cn_lines 121` |
| V9 | `python3 scripts/p09_scan.py` | `P09_HITS 0` |
| V10 | CI 三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` |
| V11 | `node new Function` 全量 demos HTML + 2 语言包 | `ALL_JS_OK 41` |
| V12 | `yaml.safe_load(ci.yml)` + `ast.parse(scripts/*.py)` | `scan_steps 8` |
| V13 | `python3 scripts/render_ui.py` | `shots=51`，56 张 PNG 重渲 |
| V14 | Playwright `file://` 离线验证 | 中文三卡 / 弹窗三卡 / ESC 关闭 / 英文三卡与 `Home` / 切回中文三卡，**0 控制台错误** |
| V15 | Playwright 弹窗状态 | 关闭后 `popState['declaration'] === false` |
| V16 | `demos/lang` 两包键数与结构 | 各 26 键，`DECLARATION` 3 行，`stable_values_ok` |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E101 | Playwright 首版 ESC 关闭后 `popState['declaration']` 仍为 `true`，面板显示「打开」但弹窗已关 | 加 `curPopId`，`closeDlg` 统一清状态并重渲；复跑断言 `false` |
| E102 | 弹窗页副标题写「11 类」，`POPUPS` 实为 13 项（037 遗留） | 两语言包 `t.0259` 与 `render_ui.py` 场景标题同步改 13 |
| E103 | 验证脚本用 `dlgTitle` / `dlgBody` 取弹窗 DOM，实际 id 是 `mdTitle` / `mdBody`，首次断言 FAIL | 按 HTML 实际 id 改脚本，非改断言口径 |
| E104 | 综合验证命令连续 6 次被网关 502 / 超时截断 | 拆成单条短命令重跑，全部补齐，无降验收项 |

## 四值

| 项 | 值 |
| --- | --- |
| B02 逐字复读证据落盘、4 份哈希与命中行号 | 已证实 |
| B01 本轮按 §14 十二项输出 | 已证实 |
| B06 演示层三项、中英双态、六种关闭零残留 | 已证实 |
| 298 / 0 单元、四守卫、JS/YAML、Playwright 0 错误 | 已证实 |
| `src/` 零改动、26 包 / 25 第三方不变 | 已证实 |
| B01/B02 历史缺失段 | 已失败（不补写、不重写） |
| B06 实现层（拉版本平台信息 / 完整性算法 / Win7 判定） | 未启动 |
| GUI 端到端、真实网络 IO、Win7 运行时 | 受阻 |

## 交付快照

本地主快照 `9d4b292` ↔ 远端 `c79b278`，1020 文件逐项 ALL_MATCH True（DIFF 0 / EXTRA 0 / tree 未截断）。全仓零凭据、后端仓 0 写请求。

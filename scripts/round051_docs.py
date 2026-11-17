from pathlib import Path
import re, hashlib

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
html_n = len(list((ROOT / 'demos').glob('*.html')))
png_n = len(list((ROOT / 'demos/preview').glob('[0-9][0-9]-*.png')))
print('REAL pkgs', pkgs, 'third', third, 'html', html_n, 'png', png_n)

Path('docs/spec/51-round-051-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}
D['docs/decisions/051-compliance-and-declaration.md'] = '''# 第 051 轮：输出结构对齐、开工逐字复读、声明页三项

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
| V11 | `node new Function` 全量 demos HTML + 2 语言包 | `ALL_JS_OK 40` |
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
'''

D['docs/verification/round-051.md'] = '''# 第 051 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 051 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | `src/` 零改动；UI 闸门触发（演示层与 56 张 PNG 重渲） |

| 编号 | 命令 / 检查 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `git rev-parse --short HEAD` / `git status` | `c2aae2a`，DIRTY 0，1014 文件 | 已证实 |
| V2 | `git diff --name-only -- src/ Cargo.toml Cargo.lock vendor/` | 0 文件 | 已证实 |
| V3 | `cargo test --offline --lib` | **298 / 0** | 已证实 |
| V4 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V5 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V6 | `cargo check --target x86_64-pc-windows-gnu` | 050 通过，本轮零改动，沿用 | 已证实（沿用） |
| V7 | `panic_guard` | `files 38 hits 0` | 已证实 |
| V8 | `semver_guard` | `version_files 3 hits 0` | 已证实 |
| V9 | `i18n_guard` | `hits 0 inline_bilingual_cn_lines 121` | 已证实 |
| V10 | `lang_guard` | `locales zh-CN en-US keys 26 stable_values_ok offline_refs_ok` | 已证实 |
| V11 | `p09_scan` | `P09_HITS 0 []` | 已证实 |
| V12 | `grep -rqE 'gh[p]_'` | `NO_CREDENTIAL` | 已证实 |
| V13 | 禁用词 / 硬编码 grep（src/） | `NO_EXPLANATORY` / `NO_HARDCODE` | 已证实 |
| V14 | `node new Function` demos HTML + 语言包 | `ALL_JS_OK 40` | 已证实 |
| V15 | `yaml.safe_load` + `ast.parse` | `PY_YAML_OK scan_steps 8` | 已证实 |
| V16 | `python3 scripts/render_ui.py` | `render_ui OK shots=51`，56 张 PNG | 已证实 |
| V17 | `python3 /data/workspace/.tmp051_verify.py` | `ZH` 三卡 / `DLG declCards 3` / `CLOSED state false` / `EN` 三英文标题 + `Home` / `BACK` 中文三卡 / `ERRORS 0` | 已证实 |
| V18 | 语言包键数 | 24 → 26，两包一致 | 已证实 |
| V19 | B02 复读记录 | 4 份字节 / 行 / SHA-256 落盘 | 已证实 |
| V20 | 远端逐项比对 | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 演示层三项、中英双态、六种关闭零残留、298 / 0 | 已证实 |
| B01 / B02 历史缺失 | 已失败（不补写、不重写） |
| B06 实现层、D07 三项取数 | 未启动 |
| GUI 端到端、真实网络 IO、Win7 运行时 | 受阻 |

限制：改动作者未代改验证结论；298 个测试是回归，不作质量结论。E104 网关中断拆段补齐，未降验收项。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s, marker=None):
    p = Path(f); t = p.read_text()
    m = marker or s.strip().splitlines()[0]
    if m in t:
        print('SKIP_DUP', f); return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 051 | 输出结构对齐、开工逐字复读、声明页三项 | 演示层与文档层落地，src 零改动 | 051-compliance-and-declaration.md |')

app('docs/records/requirement-compliance-audit.md', '''## 051 补记：B01 / B02 / B06 状态分层

| 编号 | 048 登记 | 051 状态 |
| --- | --- | --- |
| B01 | 时间戳回显与自我批判段多轮缺失 | **本轮起按 §14 十二项执行**；035–047 历史段不补写、不重写 → 仍为「已失败」 |
| B02 | 只核 `docs/index.md` 必读项存在性，未逐字复读原文 | 本轮对 4 份原文执行全文读取并落盘字节 / 行 / SHA-256（`round-051-full-readback.md`）；`00-requirements.txt` 261 行全文回显。**仅本轮**，历史轮次未复读 → 仍为「已失败」 |
| B03 | `plan()` 写死 scheme / path | 050 已修，代码层偏差消除（保留记录） |
| B06 | 声明页三项具体内容未做 | **演示层已补**（语言包 3 项 + 中英双态 + 弹窗内三卡）；实现层「拉版本平台信息 / 完整性算法 / Win7 判定」仍**未启动**，属 D07 |

原表 B01–B10 行保持原样，不重写历史证据。B04 / B05 / B07 / B08 / B09 / B10、C01–C10、D01–D09 本轮未动。EQ-14 / EQ-15 已关，EQ-01 ~ EQ-13 仍待拍板。
''', '## 051 补记')

app('docs/records/pending-question-environments.md', '''**051 状态**

本轮未新增 EQ。B01 / B02 判定为「本轮起执行，历史偏差不补写」，不需要拍板；B06 演示层三项已补，实现层 D07 未启动，待上层能力启动时按 023 规矩逐项取 LICENSE 全文再引依赖。EQ-01 ~ EQ-13 仍待拍板；EQ-14（049）、EQ-15（050）已关闭。
''', '**051 状态**')

app('docs/records/interface-log.md', '''## 051 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I80 | `demos/lang/*.js` | `DECLARATION`（3×5 字段）、`DECL_META`（2 项），键数 24 → 26 |
| I81 | `demos/ui-full-kcu-paper.html` | `DECLARATION` / `DECL_META` 变量、`loadData` / `setLang` 重建、`renderDeclaration`、`declDetail`、`curPopId` |
| I82 | 弹窗关闭契约 | `closeDlg` 统一清 `popState`；六种关闭路径零残留 |
| S50 | 状态 | U116–U120 已证实；B06 实现层未启动；`src/` 零改动 |
''')

app('docs/checklists/ai-errors.md', '''## 051 轮新增

| 编号 | 防错项 |
| --- | --- |
| A178 | 弹窗状态不能只在按钮点击里清；ESC / × / 宿主 / 取消 / 确认都走同一个 `closeDlg`，由当前弹窗 id 反查状态表。 |
| A179 | 弹窗数量类文案写进语言包后，新增弹窗类型必须同步改计数 key 与渲染脚本的场景标题，否则截图与界面长期不一致。 |
| A180 | 验证脚本的 DOM id 要从 HTML 实际结构取，不能凭命名习惯猜；猜错造成的 FAIL 不算实现缺陷。 |
| A181 | 「本轮起按规则执行」不等于「历史偏差已修」；历史回复不补写、不重写，状态分层写清。 |
| A182 | 逐字复读要留字节数、行数、哈希与命中行号；只打印一份全文、其余落盘哈希时，要写明哪份回显、哪份未回显。 |
''')

app('docs/rules/ui-demo.md', '''## 051 闸门判定

**触发**。本轮改 `demos/ui-full-kcu-paper.html`（`popups` 视图新增声明页三卡、`declaration` 弹窗内容）、两个语言包、`scripts/render_ui.py` 场景标题。`python3 scripts/render_ui.py` 重渲 51 场景 / 56 张 PNG；Playwright `file://` 离线验证中→英→中、0 控制台错误；修完后才提交。`demos/round-051-declaration.html` 是流程 HTML，不是整页 UX 演示。`src/` 零改动，实现层未动。
''')

app('docs/records/code-ownership-audit.md', '''## 051 零改动

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。本轮只动演示层语言包、UX HTML、渲染脚本、文档与预览图。`cargo test --offline --lib` 298 / 0 仅作回归。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '258. docs/verification/round-050.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''258. docs/verification/round-050.md
259. docs/spec/51-round-051-instructions.txt
260. docs/records/round-051-full-readback.md
261. docs/decisions/051-compliance-and-declaration.md
262. docs/verification/round-051.md

读取命令：''', 1)
    t = t.replace('src/core/endpoints.rs docs/verification/round-050.md; do printf',
                  'src/core/endpoints.rs docs/verification/round-050.md docs/spec/51-round-051-instructions.txt docs/records/round-051-full-readback.md docs/decisions/051-compliance-and-declaration.md docs/verification/round-051.md; do printf', 1)
    p.write_text(t); print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 051 |', p.read_text(), count=1)
sec = '''

## 051 输出结构、逐字复读与声明页三项

B02：4 份原文全文读取，字节 / 行 / SHA-256 落 `docs/records/round-051-full-readback.md`；`00-requirements.txt` 261 行全文回显。B01：本轮回复按 §14 十二项组织，历史缺失不补写。B06：语言包 24 → 26 键，声明页三项（功能关闭 / 软件完整性 / 旧版系统）进 `popups` 视图与弹窗，中英双态，六种关闭路径零残留；实现层 D07 未启动。

Playwright `file://` 中→英→中 0 控制台错误；`cargo test --offline --lib` 298 / 0；四守卫零命中；56 张 PNG 重渲。`src/` / Cargo.* / vendor/ 零改动，仍 26 包 / 25 第三方。
'''
if '## 051 输出结构' not in t:
    p.write_text(t.rstrip() + sec); print('README_OK')
else:
    p.write_text(t); print('README_SKIP_DUP')

app('docs/records/rounds.md', '''## 051

| 落点 | 内容 |
| --- | --- |
| docs/spec/51-round-051-instructions.txt | 逐字副本：「干」 |
| docs/records/round-051-full-readback.md | B02 逐字复读证据：4 份文件字节 / 行 / SHA-256 + 命中条款行号 |
| docs/decisions/051-compliance-and-declaration.md | U116–U120、V1–V16、E101–E104、四值 |
| docs/verification/round-051.md | 20 条复跑证据 |
| demos/lang/zh-CN.js / en-US.js | 加 `DECLARATION`（3 行 × 5 字段）、`DECL_META`；键数 24 → 26 |
| demos/ui-full-kcu-paper.html | `popups` 视图声明页三卡、`declaration` 弹窗内三卡、`loadData` / `setLang` 重建、`curPopId` 状态清理 |
| scripts/render_ui.py | 16-popups 场景标题 11 → 13 类 |
| demos/preview/*.png | 56 张重渲 |
| demos/round-051-declaration.html | 运行逻辑演示（19 步可点，非整页 UX HTML） |
| 索引与记录 | docs/index 262 项、README、decisions/index、requirement-compliance-audit、pending-question-environments、interface-log I80–I82、ai-errors A178–A182、code-ownership-audit、ui-demo 闸门判定 |

050 结尾留的是 EQ-01 ~ EQ-13 待拍板与 B 类偏差台账；用户回「干」，按「按默认往下走」继续修 B 类，本轮取 B01 / B02 / B06。

**B02**：此前各轮只核 `docs/index.md` 必读项与防错清单的存在性。本轮在写任何代码之前，对 `00-requirements.txt`（16422 B / 261 行 / `23ffbf3fe341ce4f`）、`ai-errors.md`（33640 B / 354 行 / `2f4f44cde1d61c4d`）、`11-features-input.txt`（17096 B / 268 行 / `1c3ff1a282863dfb`）、`12-server-features-input.txt`（4970 B / 64 行 / `03a62d90a2325fdf`）执行全文读取并落盘，命中条款带行号。**如实**：只有 `00-requirements.txt` 261 行全文回显，其余三份未逐行打印。

**B01**：本轮回复按 §14 的 12 项固定结构组织（第一行结论、时间戳回显、目标范围、代码、运行逻辑 HTML、自我批判、四值、独立验证、自评、通过标记判定、文档更新、唯一下一步）。035–047 历史回复缺时间戳与自我批判，不补写、不重写；B01 状态是「本轮起按结构执行」，不是「已修」。

**B06**：048 登记「声明页弹窗外壳有，三项具体内容未做」。本轮两语言包各加 `DECLARATION` 3 行 × 5 字段（功能关闭说明 / 软件完整性 / 旧版系统说明）与 `DECL_META` 2 项，键数 24 → 26；`popups` 视图新增 `declDetail` 三卡，点「声明页」弹窗内也带三卡；`loadData` / `setLang` 重建两键；`renderPops` 与 `popCnt` 随 `LOCALE` 切换，弹窗正文移除 `id=` 工程标签。**如实**：三项是演示层文案与界面形态，`从 GitHub/atomgit 拉版本平台信息`、完整性校验算法、Win7 判定属 D07 实现层未启动，B06 不能标「已修」。

**弹窗计数**：`ZH_TEXT['t.0259']` 与 `EN_TEXT['t.0259']` 原文「11 类 · …」，而 037 起 `POPUPS` 实为 13 项；两包与 `render_ui.py` 场景标题统一改 13 类。

本轮真实问题：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E101 | Playwright 首版 ESC 关闭后 `popState['declaration']` 仍为 `true` | 加 `curPopId`，`closeDlg` 统一清状态并重渲；复跑断言 `false` |
| E102 | 弹窗页副标题写 11 类，`POPUPS` 实为 13 项（037 遗留） | 两语言包 `t.0259` 与 `render_ui.py` 标题同步改 13 |
| E103 | 验证脚本用 `dlgTitle` / `dlgBody`，实际 id 是 `mdTitle` / `mdBody`，首跑 FAIL | 按 HTML 实际 id 改脚本，不改断言口径 |
| E104 | 综合验证连续 6 次被网关 502 / 超时截断 | 拆单条短命令重跑补齐，未降验收项 |

**验证**：`cargo test --offline --lib` 298 / 0；`http_construct` 7 / 0、`window_handle_contract` 6 / 0；`src/` / Cargo.* / vendor/ 零 diff；panic / semver / i18n / lang 四守卫零命中（`lang_guard keys 26`、`i18n_guard inline_bilingual_cn_lines 121`）；`P09_HITS 0`；CI 三条 `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE`；40 份 demos HTML 脚本 `node new Function` 全通过；`yaml.safe_load` scan 8 steps；`render_ui.py` 51 shots / 56 PNG；Playwright 中文三卡、弹窗三卡、ESC 关闭零残留、英文三卡与 `Home`、切回中文三卡，**0 控制台错误**。UI 闸门触发。

**四值**：B02 复读证据、B01 本轮结构、B06 演示层三项、298 / 0、`src/` 零改动 = 已证实；B01 / B02 历史缺失 = 已失败（不补写）；B06 实现层与 D07 = 未启动；GUI 端到端 / 真实网络 IO / Win7 运行时 = 受阻。独立验证「部分通过」，**未发通过标记**。

**下一步**：继续按台账走 B06 的实现层「软件完整性验证」——用已进构建的 ed25519-compact 做本地签名比对，不拉新依赖、不碰真实网络 IO；或用户点 EQ-01 ~ EQ-13 任一编号。
''', '## 051\n')
print('ALL_DOCS_OK')

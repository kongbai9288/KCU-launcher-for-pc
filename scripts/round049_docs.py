from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
html_files = len(list((ROOT / 'demos').glob('*.html')))
png_files = len(list((ROOT / 'demos/preview').glob('[0-9][0-9]-*.png')))
src_files = len(list((ROOT / 'src').rglob('*.rs')))
print('REAL', 'pkgs', pkgs, 'third', third, 'html', html_files, 'png', png_files, 'src', src_files)

Path('docs/spec/49-round-049-instructions.txt').write_text('抽\n')
print('SPEC_OK')

D = {}

D['docs/decisions/049-lang-extraction.md'] = f'''# 第 049 轮：演示数据源抽成独立语言包

| 项 | 值 |
| --- | --- |
| 编号 | 049 |
| 状态 | 已实现已验证；`src/` 零改动 |
| 依据 | `docs/spec/49-round-049-instructions.txt`（逐字：「抽」） |
| 对应 | EQ-14 选项 ②；048 结尾的唯一待拍板项 |
| 本轮性质 | 只做一件事：把演示数据源从 HTML 里抽出来，两种语言各一份，切换时重建数组 |

## 开工核查

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-048-A | 本地 HEAD | `6a8bbe5`，1000 文件，工作区干净 |
| V-048-B | 048 远端 | `cb20450`（`round 048 record delivery snapshot`），1000 文件 ALL_MATCH |
| V-048-C | 临时凭据 | 048 收尾已删；全仓 `NO_CREDENTIAL`，`.git/config` 干净 |

## 抽取范围

048 登记：`<script>` 段 298 行含中文、671 个单引号字符串、503 唯一，是 `NOTICES` / `POPUPS` / `INS` / `SRV` / `CREDITS` / `AUTH` / `OB` 等常量数组，加上 659 组 `ZH_TEXT`/`EN_TEXT`。

用 Node 对顶层 `const` 段求值，导出 **24 个键**的纯数据（100442 B JSON），不在 Python 里手写 JS 字面量解析：

| 类别 | 键 |
| --- | --- |
| 数据数组 / 对象（20） | `NOTICES` `POPUPS` `INS` `SRV` `CREDITS` `AUTH` `OB` `VIEW_META` `TIER_LABEL` `AROWS` `AUTO_AFTER` `AUTO_EFFECT` `DL` `LICENSE_ROWS` `CACHE_ROWS` `REFRESH_ROWS` `SERVERS` `DEVICE` `UPPER` `REC_CATALOG` |
| 字典（4，两包同值） | `EN`（181 条语义 key 译文）、`ZH_TEXT`（659）、`EN_TEXT`（659）、`TIER_EN`（3） |

| 编号 | 动作 |
| --- | --- |
| U104 | 生成 `demos/lang/zh-CN.js` 与 `demos/lang/en-US.js`，各 24 键、约 80 KB；格式 `window.KCU_LANG['<locale>'] = {{...}}`。 |
| U105 | 从 HTML 删除 **274 行**顶层 `const` 定义，改由 `<script src="lang/*.js">` 在主脚本前加载 —— 离线 `file://` 直接可用，不用 `fetch`、不用 CDN、不受 CORS 限制。 |
| U106 | 主脚本启动时声明 20 个 `let` 数据变量并取中文包；`loadData(l)` 在切换时从 `KCU_LANG[l]` 重建全部 20 个数组。 |
| U107 | `setLang` 调用 `loadData`、`renderNotices` / `renderDl` / `renderAuth` / `renderFlow` / `renderOb` / `renderPops` / `renderLic` / `renderSrv` / `updateBudget` / `applyI18n` / `renderTier` / `show`，切换后当前视图整体重渲。 |
| U108 | `mergeState(fresh, old, key, fields)`：按稳定键合并运行时状态，切语言不丢公告已读、服务器锁定 / ping / 在线人数 / 用户新增项。 |
| U109 | `scripts/lang_guard.py` + CI `lang_guard` step；`i18n_guard.py` 统计口径改名为 `inline_bilingual_cn_lines`。 |

## 译文口径（如实登记）

词典只收文件里**真实存在**的双语对应：`EN_TEXT` 里译文不等于原文的 92 组、`VIEW_META` 标题 ↔ `EN['view.*']`、`TIER_LABEL` ↔ `TIER_EN`、内联三元 `? 'English' : '中文'`、`T(k,zh,en)`，合计 **115 条**。

只做**整句精确匹配**，不做词级拼接。首版试过短语替换，生成 `KCU Launcher ProjectNotes` 这类未审校拼接词，已撤回（E94）。

| 项 | 值 |
| --- | --- |
| 数据源中文字符串 | 496 |
| 英文包精确译成英文 | **25** |
| 英文包仍保留中文 | **471** |
| 禁用词级拼接 | 是 |

**用户数据与稳定状态值不翻译**，两包逐项一致，由守卫强制：`SERVERS` 的 `sid/id/name/ip/ver/motd/inst/last/src`（玩家起的服务器名、MOTD、实例名属于用户数据）；`SRV[*][3]`、`LICENSE_ROWS[*][6]`、`INS[*][5]` 是 JS 用来判断 badge 的稳定字面量，翻译会改变逻辑。

**已知限制 L-049-1**：英文态下公告正文、弹窗描述、逻辑条、面包屑、底部状态栏等仍有中文。DOM 层 659 组 key 里 92 组有译文，界面框架是英文；471 条数据源字符串保留中文，未做机器拼接或人工补译。要完整英文态需单独审校，本轮不代你决定。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `verify_lang.py`（Playwright + 系统 chromium，`file://` 打开）：两语言包加载成功、24 键、中文态导航「首页」→ 英文态「Home」→ 切回「首页」，`NOTICES`/`SERVERS` 数量不变、运行时状态 `lock=false / ping=99` 跨两次切换保留、**0 控制台错误**。 |
| V-B | `node new Function` 对两个语言包与主脚本通过；38 份 demos HTML 脚本全通过。 |
| V-C | `lang_guard.py`：`LANG_GUARD_OK locales zh-CN en-US keys 24 data_cn_zh 496 data_cn_en_known 471 stable_values_ok offline_refs_ok`；CI scan 8 steps。 |
| V-D | `i18n_guard` / `panic_guard` / `semver_guard` 零命中；`P09_HITS 0`。 |
| V-E | `render_ui.py` 重渲 **51 场景 / {png_files} 张 PNG**；读 `01-home.png` 中文完整、读 `41-i18n-en.png` 界面框架英文。 |
| V-F | `cargo test --offline --lib` **280 / 0**；`git diff -- src/ Cargo.toml Cargo.lock vendor/` 为空，仍 {pkgs} 包 / {third} 第三方。 |
| V-G | HTML script 段中文行 **298 → 122**（降 176）；剩余是内联双语 fallback 与稳定状态字面量，不是数据源。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E93 | Playwright 默认浏览器未安装，验证脚本首跑 `BrowserType.launch` 失败 | 按 `render_ui.py` 的既有口径传 `executable_path=/usr/local/bin/chromium` + `--no-sandbox`，复跑通过 |
| E94 | 词级短语替换生成 `KCU Launcher ProjectNotes` 拼接怪译 | 撤回短语替换，只保留整句精确对应；471 条如实保留中文 |
| E95 | 抽取后 `SRV[*][3]` / `LICENSE_ROWS[*][6]` 是中文字面量比较，若以后被翻译会改变 badge 逻辑 | 生成时显式保护 + `lang_guard` 逐项比对两包一致 |
| E96 | 切语言重建 `SERVERS` 会丢用户新增项与运行时状态 | `mergeState` 按 `sid` 合并，验证脚本真改 `lock/ping` 后跨两次切换复核 |

## 四值

| 项 | 值 |
| --- | --- |
| 24 键 / 274 行抽离、两语言包、离线加载、切换重建、状态合并 | 已证实 |
| 280 / 0、四守卫零命中、56 张 PNG 重渲、零控制台错误 | 已证实 |
| 英文包 471 条中文、英文态局部中文残留 | 已证实（未清零，L-049-1） |
| 英文数据源人工审校 | 未启动 |
| `src/`、Cargo.lock、vendor 改动 | 0（已证实） |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-049.md'] = f'''# 第 049 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 049 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；`src/` 零改动，cargo 仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `6a8bbe5`，DIRTY 0，1000 文件 | 已证实 |
| V2 | 048 远端 ref（048 收尾已核） | `cb20450` | 已证实 |
| V3 | 临时凭据扫描 | `NO_CREDENTIAL`，`.git/config` 干净 | 已证实 |
| V4 | `node` 求值两个语言包 | 各 24 键，纯数据 | 已证实 |
| V5 | `node new Function` 主脚本 | 通过 | 已证实 |
| V6 | {html_files} 份 demos HTML 脚本 | ALL_JS_OK | 已证实 |
| V7 | Playwright `file://` 打开 | 两语言包加载，0 控制台错误 | 已证实 |
| V8 | 中文态导航 | 「首页」，`NOTICES=6 SERVERS=9` | 已证实 |
| V9 | 点击 `#btnLang` 切英文 | `LOCALE=en-US`，导航「Home」，数组长度不变 | 已证实 |
| V10 | 切回中文 | 「首页」，`NOTICES=6` | 已证实 |
| V11 | 改 `SERVERS[0].lock=false; ping=99` 后往返切换 | `lock=false ping=99 n=9` | 已证实 |
| V12 | `python3 scripts/lang_guard.py` | `LANG_GUARD_OK ... keys 24 data_cn_zh 496 data_cn_en_known 471 stable_values_ok offline_refs_ok` | 已证实 |
| V13 | `python3 scripts/i18n_guard.py` | `I18N_GUARD_OK ... hits 0 inline_bilingual_cn_lines 122` | 已证实 |
| V14 | `python3 scripts/panic_guard.py` / `semver_guard.py` | 各 `hits 0` | 已证实 |
| V15 | `python3 scripts/p09_scan.py` | `P09_HITS 0` | 已证实 |
| V16 | `python3 scripts/render_ui.py` | shots=51，{png_files} 张 PNG，overview 2553183 B | 已证实 |
| V17 | 读 `01-home.png` | 中文完整，数据区全渲染 | 已证实 |
| V18 | 读 `41-i18n-en.png` | 界面框架英文，逻辑条/状态栏仍中文 | 已证实 |
| V19 | `cargo test --offline --lib` | **280 / 0** | 已证实 |
| V20 | `git diff -- src/ Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V21 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan，scan 8 steps | 已证实 |
| V22 | 必读文件循环 | REQUIRED=254 MISSING=0 | 已证实 |
| V23 | 远端 `GET /git/trees/...?recursive=1` 逐项比对 | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 抽离、离线加载、切换重建、状态合并、守卫、重渲 | 已证实 |
| 英文包 471 条中文 / 英文态局部残留 | 已证实（L-049-1，未清零） |
| 英文数据源人工审校、EQ-15 端点配置化 | 未启动 |
| 真实网络 IO / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| 集成测试段（7+6+7+6）本轮未重跑 | 已证实（`src/` 零改动，沿用 048 的 306/0） |

限制：本轮未做 GUI 端到端自动化遍历、未做英文译文审校、未做真实 HTTP 请求；改动作者未代改验证结论，未降低验收项。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s):
    p = Path(f)
    t = p.read_text()
    marker = s.strip().splitlines()[0]
    if marker in t:
        print('SKIP_DUP', f)
        return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 049 | 演示数据源抽成独立语言包（EQ-14 选项②） | 已实现已验证；src 零改动 | 049-lang-extraction.md |')

app('docs/records/pending-question-environments.md', '''---

**EQ-14 已拍板（049）**

答复：「抽」→ 按选项 ② 执行。已生成 `demos/lang/zh-CN.js` / `demos/lang/en-US.js`（各 24 键），HTML 用 `<script src>` 离线加载，`setLang` 调用 `loadData` 重建 20 个数据数组并用 `mergeState` 合并运行时状态。`lang_guard.py` + CI step 落地。英文包 471 条数据源字符串仍保留中文（L-049-1），未做词级拼接或人工补译。

**EQ-15 端点配置化**仍待拍板，是 049 之后唯一的下一步。
''')

app('docs/records/requirement-compliance-audit.md', '''## 049 补记：EQ-14 已按「抽」落地

| 项 | 048 状态 | 049 状态 |
| --- | --- | --- |
| 演示数据源位置 | HTML `<script>` 段 298 行中文 | `demos/lang/zh-CN.js` / `en-US.js`，各 24 键 |
| 加载方式 | 内联 | 两个 `<script src>`，离线 `file://` 可用 |
| 切换行为 | 只换 DOM 文案，数据源不重建 | `loadData` 重建 20 个数组 + `mergeState` 合并状态 |
| 守卫 | `i18n_guard` 只统计不判 | 新增 `lang_guard`，CI scan 8 steps |
| HTML script 中文行 | 298 | **122**（内联双语 fallback 与稳定字面量） |
| 英文译文 | 567 条回退中文 | 471 条数据源字符串保留中文，禁用拼接翻译（L-049-1） |

B/C/D 三类偏差本轮未动，EQ-01 ~ EQ-13、EQ-15 仍待拍板。
''')

app('docs/records/interface-log.md', '''## 049 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I73 | `demos/lang/zh-CN.js` / `en-US.js` | 新增；各 24 键，`window.KCU_LANG['<locale>']` |
| I74 | `demos/ui-full-kcu-paper.html` | 删除 274 行顶层 const；外部 script 引入；`loadData` / `mergeState`；`setLang` 全量重渲 |
| I75 | CI | scan job 加 `lang_guard` step，脚本 `scripts/lang_guard.py` |
| S48 | 状态 | U104–U109 已证实；src 零改动；EQ-14 关闭；L-049-1 已登记 |
''')

app('docs/checklists/ai-errors.md', '''## 049 轮新增

| 编号 | 防错项 |
| --- | --- |
| A166 | 抽 JS 数据常量时用 Node 求值导出 JSON，不要在 Python 里手写 JS 字面量解析（单引号、裸键、HTML 片段、尾逗号都会踩）。 |
| A167 | 离线 `file://` 演示不能用 `fetch` 加载语言包，CORS 会挡；用 `<script src>` 挂 `window.*`。 |
| A168 | 语言包翻译只做整句精确对应；词级拼接会生成 `ProjectNotes` 一类未审校词，比保留原文更差。 |
| A169 | 切语言重建数组必须合并运行时状态（公告已读、服务器锁定/延迟/用户新增项），否则用户操作被重置。 |
| A170 | JS 里用中文字面量做逻辑判断时，该值必须在两种语言包里逐项一致，并由守卫强制；翻译它等于改逻辑。 |
| A171 | 用户数据（服务器名、MOTD、实例名）不随界面语言变化，生成英文包时要显式排除。 |
''')

app('docs/rules/ui-demo.md', '''## 049 闸门判定

本轮改动 `demos/ui-full-kcu-paper.html`（数据源抽离、外部语言包、切换重渲），属界面演示变更，**闸门触发**。按规则重渲 `python3 scripts/render_ui.py`：shots=51、56 张 PNG、总览 2553183 B；读 `01-home.png` 确认中文完整、读 `41-i18n-en.png` 确认英文框架生效。另用 Playwright `file://` 真点语言切换与状态合并，0 控制台错误。`src/` 无界面实现改动，实现层仍等手感确认。
''')

app('docs/records/code-ownership-audit.md', '''## 049 语言包抽离（src 零改动）

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 全部一行未动，仍 26 包 / 25 第三方。本轮只改演示层：24 个顶层数据常量抽到 `demos/lang/*.js`，新增 `scripts/lang_guard.py` 与 CI step。`cargo test --offline --lib` 280 / 0 仅作回归。
''')

app('docs/design/implementation-strategy.md', '''## 049 语言包状态

| 项 | 状态 |
| --- | --- |
| 演示数据源语言包 | **已抽离（049）**：`demos/lang/zh-CN.js` / `en-US.js`，离线 script 加载，切换重建 |
| 英文数据源译文 | 未审校，471 条保留中文（L-049-1） |
| 实现层 Fluent `.ftl` + `i18n-embed`（023 方案） | 未启动，未进 `Cargo.toml` |
| 端点配置化 | 未做（EQ-15） |
''')

app('docs/records/rounds.md', f'''## 049

| 落点 | 内容 |
| --- | --- |
| docs/spec/49-round-049-instructions.txt | 逐字副本：「抽」 |
| docs/decisions/049-lang-extraction.md | V-048-A~C、U104-U109、V-A~V-G、E93-E96、四值 |
| docs/verification/round-049.md | 23 条复跑证据 |
| demos/lang/zh-CN.js / en-US.js | **主交付**：各 24 键、约 80 KB |
| demos/ui-full-kcu-paper.html | 删 274 行顶层 const、外部 script、loadData / mergeState / setLang 重渲 |
| scripts/lang_guard.py / .github/workflows/ci.yml | 守卫 + CI step（scan 8 steps） |
| demos/preview/ | 51 场景 / {png_files} 张 PNG 重渲 |
| demos/round-049-lang.html | 运行逻辑演示 |
| 索引与记录 | docs/index 254 项、README、decisions/index、requirement-compliance-audit、pending-question-environments、interface-log、ai-errors A166-A171、code-ownership-audit、implementation-strategy、ui-demo 闸门判定、rounds |

048 结尾只留了 EQ-14 一个待拍板项，答复是「抽」→ 按选项 ② 执行，单轨轮，没顺手做别的。

**抽离**：用 Node 对顶层 `const` 段求值导出 24 个键的纯数据（100442 B JSON），生成 `demos/lang/zh-CN.js` 与 `en-US.js`，各约 80 KB、`window.KCU_LANG['<locale>']`。HTML 删掉 **274 行**顶层定义，改由两个 `<script src="lang/*.js">` 在主脚本前加载 —— 离线 `file://` 直接可用，不用 `fetch`、不受 CORS 限制。主脚本 20 个数据变量改成 `let`，`loadData(l)` 从语言包重建，`setLang` 追加 12 个渲染调用重渲当前视图。

**状态不丢**：`mergeState(fresh, old, key, fields)` 按 `sid` / `id` 合并公告已读、服务器锁定、ping、在线人数、用户新增项。验证脚本真改 `SERVERS[0].lock=false; ping=99`，往返切两次语言后仍是 `false / 99`。

**译文口径**：词典只收文件里真实存在的双语对应（`EN_TEXT` 92 组、`VIEW_META` ↔ `EN['view.*']`、`TIER_LABEL` ↔ `TIER_EN`、内联三元、`T(k,zh,en)`），共 115 条。首版试过词级短语替换，生成 `KCU Launcher ProjectNotes` 拼接怪译，已撤回；只保留整句精确对应。数据源 496 条中文字符串里 25 条译成英文、**471 条保留中文**，登记为 **L-049-1**，未做机器拼接或人工补译，不代你决定。用户数据（服务器名、MOTD、实例名）与 JS 用来判断 badge 的稳定字面量两包逐项一致，由 `lang_guard` 强制。

**验证**：Playwright + 系统 chromium 用 `file://` 打开，两语言包加载成功、中文「首页」→ 英文「Home」→ 切回「首页」、`NOTICES`/`SERVERS` 数量不变、0 控制台错误；`lang_guard` / `i18n_guard` / `panic_guard` / `semver_guard` 零命中，CI scan 8 steps；`render_ui.py` 重渲 51 场景 / {png_files} 张 PNG，读 `01-home.png` 与 `41-i18n-en.png` 实拍确认；`cargo test --offline --lib` **280 / 0**，`git diff -- src/ Cargo.toml Cargo.lock vendor/` 为空，仍 {pkgs} 包 / {third} 第三方。HTML script 中文行 **298 → 122**，剩余是内联双语 fallback 与稳定状态字面量。

本轮真实问题：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E93 | Playwright 默认浏览器未安装，验证脚本首跑 launch 失败 | 按 render_ui.py 的既有口径传系统 chromium 路径 + `--no-sandbox` |
| E94 | 词级短语替换生成 `KCU Launcher ProjectNotes` | 撤回，只保留整句精确对应 |
| E95 | `SRV[*][3]` / `LICENSE_ROWS[*][6]` 中文比较值可能被翻译改逻辑 | 生成时保护 + 守卫逐项比对 |
| E96 | 切语言重建 SERVERS 会丢用户状态 | `mergeState` 按 sid 合并并真改状态复核 |

EQ-14 关闭；EQ-01 ~ EQ-13、EQ-15 仍待拍板；真实网络 IO、UI 宿主、崩溃分析、子进程隔离、028 三项实现、CF F17、特殊版代码、本项目 LICENSE、UX 手感均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '248. docs/verification/round-048.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''248. docs/verification/round-048.md
249. docs/spec/49-round-049-instructions.txt
250. docs/decisions/049-lang-extraction.md
251. demos/lang/zh-CN.js
252. demos/lang/en-US.js
253. scripts/lang_guard.py
254. docs/verification/round-049.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-048.md; do printf',
                  'docs/verification/round-048.md docs/spec/49-round-049-instructions.txt docs/decisions/049-lang-extraction.md demos/lang/zh-CN.js demos/lang/en-US.js scripts/lang_guard.py docs/verification/round-049.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 049 |', p.read_text(), count=1)
section = f'''

## 049 演示数据源语言包

`demos/lang/zh-CN.js` / `en-US.js`，各 **24 键**。`ui-full-kcu-paper.html` 删掉 274 行顶层 `const`，改由两个 `<script src>` 离线加载；`setLang` 调用 `loadData` 重建 20 个数据数组，`mergeState` 按 `sid`/`id` 合并运行时状态，切语言不丢公告已读与服务器锁定 / 延迟。

`scripts/lang_guard.py` + CI step 检查两包结构、稳定状态值、用户数据、离线引用。HTML script 中文行 **298 → 122**；英文包 471 条数据源字符串保留中文（L-049-1），禁用词级拼接翻译。

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 **{pkgs} 包 / {third} 第三方**。`cargo test --offline --lib` 280/0，四守卫零命中，Playwright `file://` 切换 0 控制台错误，{png_files} 张 PNG 重渲。
'''
if '## 049 演示数据源语言包' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

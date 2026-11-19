from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
html_n = len(list((ROOT / 'demos').glob('*.html')))
png_n = len(list((ROOT / 'demos/preview').glob('[0-9][0-9]-*.png')))
print('REAL pkgs', pkgs, 'third', third, 'html', html_n, 'png', png_n)

D = {}

D['docs/verification/round-056.md'] = f'''# 第 056 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 056 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | `src/` 零改动；本轮为状态复核与守卫落地，377 / 0 仅作回归 |

| 编号 | 命令 / 检查 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `git rev-parse --short HEAD` / `git status` | 起 `7aede31`，1054 文件，DIRTY 0 | 已证实 |
| V2 | `git diff --name-only -- src Cargo.toml Cargo.lock vendor demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空 | 已证实 |
| V3 | `cargo test --offline --lib` | **351 / 0** | 已证实 |
| V4 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V5 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V6 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0 | 已证实 |
| V7 | `cargo test --offline --test plugin_abi_load` | 6 / 0 | 已证实 |
| V8 | 全量合计 | **377 / 0** | 已证实 |
| V9 | `cargo check --offline --target x86_64-pc-windows-gnu` | 通过 | 已证实 |
| V10 | `panic_guard` / `semver_guard` | 零命中 / 零命中 | 已证实 |
| V11 | `i18n_guard` / `lang_guard` / `policy_guard` | 零命中 / keys 26 / G1–G8 OK | 已证实 |
| V12 | `delivery_guard` | `DELIVERY_GUARD_OK rounds=[56]` | 已证实 |
| V13 | 注入 A（移走 056 spec 副本） | `G0 current_round_spec_missing`，退出 1 | 已证实 |
| V14 | 注入 B（改 056 决策 `## 2. 时间戳` 标题） | `G3 heading_missing`，退出 1 | 已证实 |
| V15 | 恢复后 `delivery_guard` | OK | 已证实 |
| V16 | `p09_scan` | `P09_HITS 0 []` | 已证实 |
| V17 | CI 三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` | 已证实 |
| V18 | `node new Function` demos HTML + 两语言包 | `ALL_JS_OK {html_n}` | 已证实 |
| V19 | `yaml.safe_load(ci.yml)` | `scan_steps 10`，末步 `delivery_guard` | 已证实 |
| V20 | B02 复读记录 | 5 份字节 / 行 / SHA-256 | 已证实 |
| V21 | 必读读取命令块 | 296 项，`MISSING 0` | 已证实 |
| V22 | 远端只读 ref | `1fe6a90255ec`（054），055 / 056 未更新 | 受阻 |
| V23 | `git push origin main` | `fatal: ... 403`，PUSH_RC 128 | 受阻 |

| 项 | 值 |
| --- | --- |
| E127 / E128 / E129 证据、B 类 10 条结论、五条可拍环境 | 已证实 |
| delivery_guard G1–G8、CI 第 10 步、双向注入、377 / 0 回归 | 已证实 |
| 零 src / 零依赖 / UI 零 diff、{pkgs} 包 / {third} 第三方 | 已证实 |
| 035–047 历史交付格式缺失 | 已失败（不补写） |
| B04 / B05 / B07 / B09 / B10、EQ-01 ~ EQ-13、4 条 Q-C | 未证实（待拍板） |
| 真实网络 IO、UI 宿主、崩溃分析、子进程隔离、GUI 接线 | 未启动 |
| 远端写入、GUI 端到端、Win7 / MSVC / i686 运行时 | 受阻 |

限制：改动作者未代改验证结论；377 个测试是回归，不作质量结论。048 / 051–055 历史验证报告不补写。

## 交付快照（056 收口）

| 项 | 值 |
| --- | --- |
| 远端 `refs/heads/main` | `1fe6a90255ec`（054 补写记录），055 / 056 **未更新** |
| 055 待补推 | `03ba613`（主快照）+ `7aede31`（交付补记） |
| 056 再试推送 | `fatal: ... 403`，PUSH_RC 128；`KCU_PAT` unset、credential 无写凭据、`.git/config` 零 token |
| 逐项 ALL_MATCH | **本轮不成立**（远端仍是 054 树）。不强推、不伪造、不重写远端历史 |
| 两个 zip | 主包按 `git ls-files` 打包（EXTRA 0 / MISSING 0）；预览包 {png_n + 1} 项；均不含 `.git` / `target/` / `__pycache__` |
| 零凭据 | tracked 零凭据；`.git/config` 零 token；`.push056.log` 已删 |
| 开工 / 最终时间戳 | `Thu Nov 19 00:24:32 CST 2026` / 见本轮决策「2. 时间戳」 |

056 结论、复核、六守卫、377 / 0 回归全在本地复跑，不依赖远端写入。
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


app('docs/records/requirement-compliance-audit.md', '''## 056 补记：B 类 10 条状态复核

逐条证据与五条可拍环境在 `docs/records/b-class-status-recheck.md`。本轮**不代用户拍板**；原表 B01–B10 行保持原样，不重写历史证据。

| 编号 | 048 判定 | 056 修正 |
| --- | --- | --- |
| **E127 / B01** | 「时间戳回显与自我批判段多轮缺失」 | 054 / 055 / 056 回复六项齐备，055 决策文件四锚点齐全 → 改判「054 起常态遵守；035–047 历史缺失不补写」 |
| **E127 / B02** | 「没有逐字复读 00-requirements.txt 全文」 | 051–056 共 6 份 `round-NNN-full-readback.md`，每份 5 文件全文遍历 + 哈希 → 改判「051 起常态遵守」 |
| **E128** | （048 未列） | 054 **决策文件**缺 `2. 时间戳` 段与 `## 10. 四值` 标题（回复里有）；不补写 054 文件，从 056 起由 `delivery_guard.py` G3 强制 |
| B03 | 未遵守 | 050 已修（`src/core/endpoints.rs`），补记已同步 |
| B06 | 三项具体内容未做 | 051 / 052 / 053 分层落地（完整性、声明、feature_gate），台账行滞后 |
| **E129 / B08** | 「登记为口径，未实现」 | 054 已落 `src/core/region.rs` 判定层（869 行 / 20 测试 / 零新增依赖）→ 改判「判定层已落地，GUI 接线未启动」 |
| B04 / B05 / B07 / B09 / B10 | 未启动 | 仍**未启动**，各自卡点：EQ-01 / 源仓库与许可未给 / EQ-05 / EQ-11 / B10 口径未决断；本轮不擅自开工 |

B01 / B02 的 035–047 历史偏差仍标「已失败」，不补写、不重写。C 类 10 条（055 复核）状态不变；D01–D09 本轮未动。EQ-14（049）、EQ-15（050）已关闭，EQ-01 ~ EQ-13 仍待拍板。
''', '## 056 补记')

app('docs/decisions/index.md', '| 056 | B 类 10 条状态复核、E127-E129、B→EQ 映射、交付格式守卫 | 结论已落地，delivery_guard + CI 守护 | 056-b-class-recheck.md |')

app('docs/checklists/ai-errors.md', '''## 056 轮新增

| 编号 | 防错项 |
| --- | --- |
| A207 | 「回复里格式齐」不等于「决策留痕齐」：每轮决策文件必须含 `## 2. 时间戳` / `## 9. 自我批判` / `## 10. 四值` / 开工复读四锚点，由 `delivery_guard.py` G3 强制；历史文件缺项只登记、不补写。 |
| A208 | 用户只回「干」且结尾列了「需 EQ 拍板才能动」的层时，先复核台账状态与摊平可拍环境，不擅自开工；硬做会重复 048 批评的 C 类错误。 |
| A209 | 远端 403 未推成时，验证报告 / 决策 / 四值表写「受阻、ALL_MATCH 本轮不成立」；再试一次仍失败就如实登记，不写成「已处理」。 |
''', '## 056 轮新增')

app('docs/records/interface-log.md', '''## 056 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I98 | `scripts/delivery_guard.py` | G1–G8，`GUARD_FROM = 56`，不追溯 054 之前；失败打印 `DELIVERY_GUARD_FAIL reason=` 并退出 1 |
| I99 | `.github/workflows/ci.yml` | `scan` job 第 10 步 `delivery_guard`；前 9 步不变 |
| I100 | `docs/records/b-class-status-recheck.md` | B01–B10 逐条复核、E127–E129、5 条 B→EQ 可拍环境、四值 |
| I101 | 状态 | B04/B05/B07/B09/B10 未开工；`src/` 零改动；远端 403 受阻 |
''')

app('docs/records/code-ownership-audit.md', '''## 056 零改动复核轮

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。本轮不是换库轮，只做 B 类 10 条状态复核、三处台账修正与 `scripts/delivery_guard.py` 守卫；`cargo test --offline` 全量 377 / 0 仅作回归，不作质量结论。023 A03 自写底座例外于 024 撤回的状态不变。
''')

app('docs/records/pending-question-environments.md', '''**056 状态**

B 类 10 条状态复核完成，逐条证据与五条 B→EQ 可拍环境在 `docs/records/b-class-status-recheck.md`：B04 → EQ-01（Win7 WebView2）、B05 → 源仓库与许可未给（无 EQ）、B07 → EQ-05（子进程隔离）、B09 → EQ-11（32 位 / MSVC / i686）、B10 → 推进口径未决断。本轮**不擅自开工**这五条。

E127 / E128 / E129 三处台账滞后已追加补记；`scripts/delivery_guard.py` + CI `scan` 第 10 步守护交付格式六项。EQ-01 ~ EQ-13 仍待拍板，EQ-14（049）、EQ-15（050）已关闭；Q-C01 / Q-C02 / Q-C08 / Q-037-01 仍待拍板。本轮未新增 EQ。
''', '**056 状态**')

app('docs/records/rounds.md', f'''## 056

| 落点 | 内容 |
| --- | --- |
| docs/spec/56-round-056-instructions.txt | 逐字副本：「干」 |
| docs/records/round-056-full-readback.md | B02 复读证据：5 份字节 / 行 / SHA-256 |
| docs/records/b-class-status-recheck.md | **主交付**：B01–B10 逐条复核、E127–E129、5 条可拍环境、四值 |
| docs/decisions/056-b-class-recheck.md | 时间戳 / 自我批判 / 四值 / 三轮迭代自评 9.3 / 交付补记 |
| docs/verification/round-056.md | 23 条复跑证据 + 交付快照 |
| scripts/delivery_guard.py | G1–G8，`GUARD_FROM = 56` |
| .github/workflows/ci.yml | `scan` 9 → 10 steps，新增 `delivery_guard` |
| demos/round-056-b-class.html | 运行逻辑演示（17 步可点，非整页 UX HTML） |
| 补记 | requirement-compliance-audit 056 补记、pending-question-environments 056 状态、decisions/index、ai-errors A207–A209、interface-log I98–I101、code-ownership-audit、README |
| 索引 | docs/index 289 → 296 项 |

055 结尾列「B04 / B05 / B07 / B09 / B10 需 EQ 编号」。用户没给凭据、没回 Q-C、没点 EQ，只回「干」。按 049/050 既有默认「按台账继续、不代拍板」执行；五条全卡 EQ，硬做会重复 048 批评的 C 类错误，故**不擅自开工**，改为状态复核 + 摊平可拍环境 + 防复发守卫。

**B02**：5 份原文全文遍历；`ai-errors.md` 复读时 38518 B / 408 行（A207–A209 在复读之后追加）。

**三个真发现**：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E127 | B01 / B02 台账滞后：051–056 共 6 份 full-readback 齐全；054/055/056 回复六项齐备、055 决策四锚点齐全 | 台账追加 056 补记改判；035–047 历史缺失不补写 |
| E128 | 054 决策文件缺 `2. 时间戳` 段与 `## 10. 四值` 标题（054 回复里有） | 不补写 054 文件；从 056 起由 G3 强制 |
| E129 | B08 台账仍写「未实现」，054 已落 `src/core/region.rs` 869 行 / 20 测试 / 零新增依赖 | 台账追加补记改判「判定层已落地，GUI 接线未启动」 |
| E130 | 056 再试 `git push` → 403，PUSH_RC 128 | 不强推、不伪造 ALL_MATCH；待通道恢复后按 `03ba613 → 7aede31 → 056` 补推 |
| E131 | 双向注入各只触发 1 项 FAIL（**G0** / G3） | 按实记录，不补凑断言 |
| E132 | 注入 B 首版未触发：守卫表格引用同一锚点字符串 | G3 改行首精确匹配，重跑 → `G3 heading_missing`；A210 防复发 |

**B 类结论**：B01/B02 054/051 起常态遵守；B03（050）、B06（051–053）、B08 判定层（054）已落地；B04/B05/B07/B09/B10 未启动，卡点分别 EQ-01 / 源仓库与许可未给 / EQ-05 / EQ-11 / 推进口径未决断。五条具体环境值与「要拍一句」在复核表里，不铺场景。

**delivery_guard**：G1 spec 副本、G2 复读记录、G3 决策四锚点、G4 验证报告、G5 流程 HTML、G6 B 类台账、G7 交付快照、G8 CI step；`GUARD_FROM = 56` 不追溯历史。CI `scan` 新增第 10 步。注入 A（删 spec）→ `G1 FAIL`；注入 B（删 056 决策时间戳段）→ `G3 FAIL`；恢复 → OK。

**三轮真迭代与自评**：8.3（想直接开工 B04；没先核台账；没核 054 决策锚点）→ 8.9（发现 E127–E129、写复核表与 B→EQ 映射、台账补记）→ **9.3**（补 G1–G8、CI step、双向注入、全量回归、流程演示与索引）。未给满分：五条待拍板未拍、上层四块未启动、035–047 历史缺失不补写、远端写入受阻。

**验证**：`cargo test --offline --lib` 351 / 0（src 零改动，仅回归），全量 **377 / 0**；Windows GNU 通过；panic / semver / i18n / lang / policy / delivery 六守卫零命中或 OK；`P09_HITS 0`；CI 三条 `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE`；{html_n} 份 demos HTML 脚本通过；`yaml.safe_load` scan 10 steps；296 项必读 `MISSING 0`。UI 闸门**未触发**：UX HTML、两语言包、{png_n} 张 PNG、`src/`、`Cargo.toml`、`Cargo.lock`、`vendor/` 全部零 diff，仍 {pkgs} 包 / {third} 第三方。

**四值**：E127–E129 证据、B 类逐条结论、五条可拍环境、delivery_guard、377 / 0 = 已证实；035–047 历史缺失 = 已失败（不补写）；B04/B05/B07/B09/B10、EQ-01 ~ EQ-13、4 条 Q-C = 未证实；真实网络 IO / UI 宿主 / 崩溃分析 / 子进程隔离 / GUI 接线 = 未启动；远端写入（403）/ GUI 端到端 / Win7 与 MSVC 与 i686 运行时 = 受阻。独立验证「部分通过」，**未发通过标记**。

**下一步**：给写凭据 / 通道后补推 `03ba613 → 7aede31 → 056` 并逐项比对；或按 EQ 编号拍 B04（EQ-01）/ B07（EQ-05）/ B09（EQ-11）/ B10（推进口径），或给 B05 的 HMCL 仓库与许可；或回 Q-C01 / Q-C02 / Q-C08 / Q-037-01 任一条。
''', '## 056\n')

# CI 第 10 步
p = Path('.github/workflows/ci.yml'); t = p.read_text()
old = '      - name: policy_guard\n        run: python3 scripts/policy_guard.py\n'
if 'name: delivery_guard' in t:
    print('CI_SKIP_DUP')
else:
    assert old in t, 'policy_guard anchor missing'
    p.write_text(t.replace(old, old + '      - name: delivery_guard\n        run: python3 scripts/delivery_guard.py\n', 1))
    print('CI_OK')

# docs/index 289 → 296
p = Path('docs/index.md'); t = p.read_text()
a = '289. demos/round-055-c-class-recheck.html\n\n读取命令：'
if a in t and '290. docs/spec/56-round-056-instructions.txt' not in t:
    t = t.replace(a, '''289. demos/round-055-c-class-recheck.html
290. docs/spec/56-round-056-instructions.txt
291. docs/records/round-056-full-readback.md
292. docs/records/b-class-status-recheck.md
293. docs/decisions/056-b-class-recheck.md
294. docs/verification/round-056.md
295. scripts/delivery_guard.py
296. demos/round-056-b-class.html

读取命令：''', 1)
    t = t.replace('scripts/policy_guard.py demos/round-055-c-class-recheck.html; do printf',
                  'scripts/policy_guard.py demos/round-055-c-class-recheck.html docs/spec/56-round-056-instructions.txt docs/records/round-056-full-readback.md docs/records/b-class-status-recheck.md docs/decisions/056-b-class-recheck.md docs/verification/round-056.md scripts/delivery_guard.py demos/round-056-b-class.html; do printf', 1)
    p.write_text(t); print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md'); t = p.read_text()
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 056 |', t, count=1)
sec = f'''

## 056 B 类 10 条状态复核

`docs/records/b-class-status-recheck.md` 逐条复核 048 核对表的 B 类 10 条，**不代拍板**：E127（B01/B02 自 054/051 起常态遵守，台账滞后）、E128（054 决策文件缺 2 项格式锚点，回复齐备但留痕不齐，不补写）、E129（B08 判定层 054 已落地，台账仍写未实现）三处追加补记。B04 / B05 / B07 / B09 / B10 全卡 EQ，本轮**不擅自开工**，只把五条具体环境值与「要拍一句」摊平。

新增 `scripts/delivery_guard.py`（G1–G8，`GUARD_FROM = 56`，不追溯历史）与 CI `scan` 第 10 步，守护交付格式六项与开工复读留痕；双向注入各 1 项 FAIL，恢复后 OK。`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / {png_n} 张 PNG 全部零 diff，仍 **{pkgs} 包 / {third} 第三方**；`cargo test --offline` 全量 **377 / 0**（仅回归）。远端 `git push` 仍 403，055 / 056 未更新远端，不强推、不伪造 ALL_MATCH。
'''
if '## 056 B 类 10 条状态复核' not in t:
    p.write_text(t.rstrip() + sec); print('README_OK')
else:
    p.write_text(t); print('README_SKIP_DUP')

print('ALL_DOCS_OK')

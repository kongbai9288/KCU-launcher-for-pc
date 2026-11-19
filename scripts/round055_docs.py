from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
html_n = len(list((ROOT / 'demos').glob('*.html')))
png_n = len(list((ROOT / 'demos/preview').glob('[0-9][0-9]-*.png')))
src_n = len(list((ROOT / 'src').rglob('*.rs')))
print('REAL pkgs', pkgs, 'third', third, 'html', html_n, 'png', png_n, 'src_rs', src_n)

D = {}

D['docs/decisions/055-c-class-recheck.md'] = f'''# 第 055 轮：C 类 10 条擅自定默认复核

| 项 | 值 |
| --- | --- |
| 编号 | 055 |
| 状态 | 结论与台账修正已落地；`src/`、`Cargo.toml`、`Cargo.lock`、`vendor/`、UX HTML、两语言包、{png_n} 张 PNG 全部零改动 |
| 依据 | `docs/spec/55-round-055-instructions.txt`（逐字：「干」） |
| 前序 | 054 结尾「下一声『干』我转去处置 048 核对表里一直挂着的 C 类 10 条擅自定默认」 |
| 本轮性质 | 口径复核轮，不是换库轮；UI 闸门未触发 |

## 2. 时间戳

开工 `Wed Nov 18 13:42:54 CST 2026`；最终见 `docs/verification/round-055.md` 交付快照。

## 3. 开工复读（B02）

`docs/records/round-055-full-readback.md`：

| 文件 | 字节 | 行 | SHA-256 前 16 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f` |
| `docs/checklists/ai-errors.md` | 37282 | 396 | `a848c57d07b4d4c1` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf` |
| `docs/spec/55-round-055-instructions.txt` | 4 | 1 | `67997353aa5bff04` |

对 5 份执行全文 `read_text()` 与逐行遍历。`ai-errors.md` 复读时 37282 B / 396 行；A200–A204 在复读之后追加，复读记录取追加前值。本轮为 C 类复核定位原文依据：`00-requirements.txt` 第 9–14 行轻量 5 条、`11-features-input.txt:206`「有些功能你看着办」、`20-round-020-instructions.txt` 第 1 行「不要写进顶上」、`21-round-021-instructions.txt` 第 1 行「显示什么按正常我的世界现实的逻辑」。复读在写任何文档之前完成。

## 4. 范围判定

054 结尾已被用户「干」接续，明确指向 C 类 10 条。本轮**不另起新层**：不碰 B 类剩余项、不碰 D07 实现层、不碰 EQ-01 ~ EQ-13。复核只做三件事：核证据、改台账结论、补具体值回显；**不代用户拍板**。

## 5. 三个真实发现

| 编号 | 现象 | 证据 | 处置 |
| --- | --- | --- | --- |
| E120 | 048 核对表 C05 写「『两个问题 A』未随澄清重审」 | `docs/decisions/033-answer-abbr-and-anyhow.md` 第 1/15/18–30 行、`docs/features/server-auto-command-log-trigger.md:128`、`docs/records/q028-decision-scenarios.md:187`、`docs/records/pending-question-environments.md:105` 均记 033 已结案（A = answer 缩写） | 追加 055 补记修正 C05；031 / 032 决策追加 055 补记覆盖其历史行「待确认 / 未证实」，历史行不重写 |
| E121 | 048 核对表 C06 写「服务器状态按 SLP 六类设计」 | `docs/decisions/021-server-autoconnect.md` 第 9 行「020 把『服务器状态』做成用户配置 SLP 参数，理解偏了；本轮撤回该页面口径」、D07「显示照原版」、D09「删除 SLP 参数、6 类状态、自定义文案颜色」；`docs/design/server-status.md` 第 83 行「不再作为页面设计依据」 | 追加补记同步台账；`server-status.md` 保留为协议事实存档，不作页面依据 |
| E122 | 048 核对表 C08 依据列写 021 | 「有些功能你完全不需要写在顶上，比如接口什么的」在 `docs/spec/20-round-020-instructions.txt`；收敛为 9 项在 `docs/decisions/020-nav-slots-settings.md` D02；021 讲的是服务器自动连接与显示 | 追加补记改依据为 020；9 项逐项补回显 |

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E123 | 054 最终回复「唯一下一步」沿用 C05 错述（「033 澄清后我还没重审的 Q-031-01」），且未打开 033 决策文件核 | `docs/records/rounds.md` 追加「054 结尾错述撤回」；不重写 054 回复、不改 031/032 口径、不重做界面 |
| E124 | 双向注入各只触发 1 项 FAIL（G2 / G5），不是多项 | 按实记录，不补凑断言；防错项 A204 |

## 5b. C 类 10 条复核结论

逐条证据与具体值在 `docs/records/c-class-default-recheck.md`。

| 编号 | 结论 |
| --- | --- |
| C01 | 轻量 13 项排除属范围推断；13 项逐项补回显，登记 Q-C01 待拍板 |
| C02 | 实现层单主题属未拍板；补回显，不擅自加双主题，登记 Q-C02 |
| C03 | 024 W01 已撤回，全仓 6 处引用均带撤回标记，无活例外 → 改判「已撤回且无残留」 |
| C04 | 身份哈希 `sha512(plugin_id)[..16]`；补两种口径的具体后果（内容哈希会使「哈希一致且版本更高」永不成立），Q-037-01 仍待拍板 |
| C05 | **台账笔误**，033 已结案，见 E120 |
| C06 | 10 处推荐位属 019 授权补全，确认；SLP 六类已在 021 撤回，见 E121 |
| C07 | 上层起手顺序已执行且不可回退，登记既成事实，不新增拍板项 |
| C08 | 依据轮次错，见 E122；9 项补回显，登记 Q-C08 |
| C09 | 「看着办」授权成立（013 指令多处、`11-features-input.txt:206`）；三条具体值首次回显，032 后第三条改为 U05 |
| C10 | 两版作废稿保留无冲突，`i18n_guard.py` 已显式排除，确认保留不删 |

待拍板：**Q-C01** 轻量 13 项排除清单 / **Q-C02** 正常模式实现层主题数 / **Q-C08** 一级导航 9 项 / **Q-037-01** 插件哈希口径。**Q-031-01 已关闭**。本轮未新增 EQ；EQ-14（049）、EQ-15（050）已关闭，EQ-01 ~ EQ-13 仍待拍板。

## 6. 口径守护（本轮唯一新增机器检查）

`scripts/policy_guard.py` 八组断言：

| 编号 | 检查 |
| --- | --- |
| G1 | 033 决策含「Q-031-01 结案」与「A 是 answer 缩写」 |
| G2 | 031 / 032 决策都含「## 055 补记」（历史行保留，用补记判定结案） |
| G3 | 合规核对表含 055 补记与 C05 / C06 / C08 三处修正 |
| G4 | `auto-command-policy.md` 默认严格档、Q1-C、Q2-A、U01 回严格 |
| G5 | 三档单调：严格 Q1-C/Q2-A → 标准 Q1-B/Q2-C → 宽松 Q1-A/Q2-D |
| G6 | 环境清单标 Q-031-01 已结案且含 055 状态 |
| G7 | C 类复核表 10 条齐备且含 Q-037-01 |
| G8 | `rounds.md` 含「054 结尾错述撤回」 |

CI `scan` job 新增第 9 步 `policy_guard`。双向注入：删 031 补记段 → `G2 FAIL`（退出 1）；把严格行 `Q1-C` 改成 `Q1-A` → `G5 FAIL`（退出 1）；恢复后 `POLICY_GUARD_OK`。**历史行不重写**，因此用「补记段是否存在」而不是「旧行是否消失」判定结案。

## 7. 三轮真迭代与自评

| 轮 | 分 | 缺什么 | 补什么 |
| --- | --- | --- | --- |
| 初稿 | 8.2 | 只核 10 条状态；没打开 033 决策；没核台账依据轮次；没补具体值 | B02 复读与逐文件核证据 |
| 二稿 | 8.9 | 发现 E120 / E121 / E122 / E123，但缺机器防复发与完整回显 | 写复核表、撤回 054 错述、补 13 项 / 9 项 / 三值 / 两种哈希后果 |
| 终稿 | **9.3** | 缺守护脚本、CI step、双向注入、完整验证与交付 | 补 G1–G8、注入 A/B、全量回归、流程演示、索引与打包 |

自评 **9.3**，未给满分：Q-C01 / Q-C02 / Q-C08 / Q-037-01 未拍板，C01 / C02 / C08 的默认仍是我定的；真实网络 IO / UI 宿主 / 崩溃分析 / 子进程隔离未启动；B01 / B02 历史偏差未补写。

## 8. 验证

| 编号 | 命令 | 输出 |
| --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `6e88f62` 起，DIRTY 1（逐字副本），1046 文件 |
| V2 | `git diff --name-only -- src Cargo.toml Cargo.lock vendor demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空 |
| V3 | `cargo test --offline --lib` | **351 / 0**（src 零改动，仅回归） |
| V4 | `http_construct` / `window_handle_contract` | 7 / 0、6 / 0 |
| V5 | `plugin_lifecycle_load` / `plugin_abi_load` | 7 / 0、6 / 0 |
| V6 | 全量合计 | **377 / 0** |
| V7 | `cargo check --offline --target x86_64-pc-windows-gnu` | 通过 |
| V8 | `panic_guard` / `semver_guard` / `i18n_guard` / `lang_guard` | 零命中 / keys 26 |
| V9 | `policy_guard` | `POLICY_GUARD_OK g5_tiers=3` |
| V10 | 注入 A / B / 恢复 | G2 FAIL / G5 FAIL / OK |
| V11 | `p09_scan` / CI 三条 grep | `P09_HITS 0` / `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` |
| V12 | `node new Function` demos HTML + 语言包 | `ALL_JS_OK {html_n}` |
| V13 | `yaml.safe_load(ci.yml)` | `scan_steps 9`，末步 `policy_guard` |
| V14 | 必读读取命令块 | 289 项，`MISSING 0` |
| V15 | 远端 tree 逐项比对 | **未执行**：远端仍 054 树，`git push` 403 | 受阻 |

全量 377 / 0 是回归，不作质量结论；本轮不动 `src/`，不引依赖，仍 {pkgs} 包 / {third} 第三方。

## 9. 自我批判

- **048 台账自身有三处不准**（C05 笔误、C06 滞后、C08 轮次错），而我 054 结尾直接沿用了其中一处。合规核对表也是我写的，同样需要被复核；本轮只追加补记，不重写历史行。
- **「未决断我擅自定默认」不等于「结论错」**：C03 已撤回、C06 前半属授权、C09 授权成立、C10 无冲突；本轮没有把这些一律改成「待改」，只修正证据状态。
- **不代拍板**：C01 13 项、C02 单主题、C08 9 项、C04 哈希口径四条仍是我定的默认，列出当前值与另一口径，不擅自切换。
- **fail-open 的取舍沿用 054**：本轮复核不动判定层，`src/core/region.rs` 与 351 / 0 只作回归证据。
- 054 结尾错述按「不重写历史回复」口径撤回，只补登记；用户看到的 054 回复本身不改。
- 界面闸门未触发：UX HTML、两语言包、{png_n} 张 PNG 零 diff；`demos/round-055-c-class-recheck.html` 是流程演示，不是 UX HTML。

## 10. 四值

| 项 | 值 |
| --- | --- |
| E120 / E121 / E122 / E123 证据、C 类 10 条逐条结论、具体值回显 | 已证实 |
| policy_guard G1–G8、CI 第 9 步、双向注入、377 / 0 回归 | 已证实 |
| 零 src / 零依赖 / UI 零 diff、{pkgs} 包 / {third} 第三方 | 已证实 |
| B01 / B02 历史缺失 | 已失败（不补写） |
| Q-C01 / Q-C02 / Q-C08 / Q-037-01、EQ-01 ~ EQ-13 | 未证实（待拍板） |
| 真实网络 IO、GUI 接线、UI 宿主、崩溃分析、子进程隔离 | 未启动 |
| GUI 端到端、Win7 / MSVC 运行时 | 受阻 |
'''

D['docs/verification/round-055.md'] = f'''# 第 055 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 055 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | `src/` 零改动；本轮为口径复核与守卫落地，377 / 0 仅作回归 |

| 编号 | 命令 / 检查 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `git rev-parse --short HEAD` / `git status` | 起 `6e88f62`，1046 文件 | 已证实 |
| V2 | `git diff --name-only -- src Cargo.toml Cargo.lock vendor demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空 | 已证实 |
| V3 | `cargo test --offline --lib` | **351 / 0** | 已证实 |
| V4 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V5 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V6 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0 | 已证实 |
| V7 | `cargo test --offline --test plugin_abi_load` | 6 / 0 | 已证实 |
| V8 | 全量合计 | **377 / 0** | 已证实 |
| V9 | `cargo check --offline --target x86_64-pc-windows-gnu` | 通过 | 已证实 |
| V10 | `panic_guard` / `semver_guard` | 零命中 / 零命中 | 已证实 |
| V11 | `i18n_guard` / `lang_guard` | `rs_files 41 hits 0` / `keys 26` | 已证实 |
| V12 | `policy_guard` | `POLICY_GUARD_OK g1_033_closed ... g8_054_retracted` | 已证实 |
| V13 | 注入 A（删 031 补记段） | `G2 FAIL`，退出 1 | 已证实 |
| V14 | 注入 B（严格行 Q1-C → Q1-A） | `G5 FAIL`，退出 1 | 已证实 |
| V15 | 恢复后 `policy_guard` | OK | 已证实 |
| V16 | `p09_scan` | `P09_HITS 0 []` | 已证实 |
| V17 | CI 三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` | 已证实 |
| V18 | `node new Function` demos HTML + 两语言包 | `ALL_JS_OK {html_n}` | 已证实 |
| V19 | `yaml.safe_load(ci.yml)` | `scan_steps 9`，末步 `policy_guard` | 已证实 |
| V20 | B02 复读记录 | 5 份字节 / 行 / SHA-256 | 已证实 |
| V21 | 必读读取命令块 | 289 项，`MISSING 0` | 已证实 |
| V22 | 远端 `GET /git/trees/...?recursive=1` | 只读成功，ref `1fe6a90255ec`（054）；写入未执行 | 受阻 |

| 项 | 值 |
| --- | --- |
| E120 / E121 / E122 / E123 台账修正、C 类逐条结论、具体值回显 | 已证实 |
| B01 / B02 历史缺失 | 已失败（不补写） |
| Q-C01 / Q-C02 / Q-C08 / Q-037-01、EQ-01 ~ EQ-13 | 未证实 |
| 真实网络 IO、GUI 接线、UI 宿主、崩溃分析、子进程隔离 | 未启动 |
| GUI 端到端、Win7 / MSVC 运行时 | 受阻 |

限制：改动作者未代改验证结论；377 个测试是回归，不作质量结论。048 / 051 / 052 / 053 / 054 历史验证报告不补写。
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


app('docs/decisions/index.md', '| 055 | C 类 10 条复核、三处台账修正、Q-031-01 撤回错述 | 结论已落地，policy_guard + CI 守护 | 055-c-class-recheck.md |')

app('docs/checklists/ai-errors.md', '''## 055 轮新增

| 编号 | 防错项 |
| --- | --- |
| A200 | 台账「依据」列写轮次前，打开对应 `docs/spec/NN-round-NN-instructions.txt` 核原文；020 的「不要写进顶上」别写成 021。 |
| A201 | 结论状态变更（如 033 结案 Q-031-01）后，同步所有引用它的台账、决策、场景与环境清单；历史行不重写，但必须有补记覆盖。 |
| A202 | 每轮结尾的「唯一下一步」引用旧台账前，打开被引决策文件核一遍；别把台账笔误当成待办再念一遍。 |
| A203 | 「你看着办」授权成立也要逐值回显具体默认，不能只写「按授权自定」；后续轮次改了值（如 032 U05）要同时标出变更。 |
| A204 | 新增口径守护脚本必须双向注入验证，且确认 CI job 里真的挂上该 step；注入只触发 1 项 FAIL 就记 1 项，不补凑断言。 |
''', '## 055 轮新增')

app('docs/records/interface-log.md', '''## 055 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I94 | `scripts/policy_guard.py` | G1–G8 八组文档断言；失败打印 `POLICY_GUARD_FAIL reason=` 并退出 1 |
| I95 | `.github/workflows/ci.yml` | `scan` job 第 9 步 `policy_guard`；前 8 步不变 |
| I96 | `docs/records/c-class-default-recheck.md` | C01–C10 逐条复核、3 处台账修正、待拍板 4 项、四值 |
| I97 | 状态 | Q-031-01 已关闭；Q-C01 / Q-C02 / Q-C08 / Q-037-01 待拍板；`src/` 零改动 |
| S54 | 口径一致性 | 031 Q1-C + Q2-A、032 三档单调与 U01、033 结案，三者由 G1/G2/G4/G5 守护 |
''')

app('docs/records/code-ownership-audit.md', '''## 055 零改动复核轮

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。本轮不是换库轮，只做 C 类 10 条口径复核、三处台账修正与 `scripts/policy_guard.py` 守卫；`cargo test --offline` 全量 377 / 0 仅作回归，不作质量结论。023 A03 自写底座例外于 024 撤回的状态不变。
''')

app('docs/design/implementation-strategy.md', '''## 055 状态

| 项 | 状态 |
| --- | --- |
| B08 账户地域判定层（054 `src/core/region.rs`） | 已落地，零新增依赖 |
| C 类 10 条擅自定默认 | 已逐条复核，三处台账修正；四条仍待拍板，不擅自改默认 |
| 真实网络 IO、UI 宿主、崩溃分析、子进程隔离 | 未启动，需 EQ-01 / EQ-03 / EQ-04 拍板 |
| 031 / 032 / 033 自动命令口径 | 由 `scripts/policy_guard.py` 守护，CI `scan` 第 9 步 |
''')

app('docs/rules/ui-demo.md', '''## 055 闸门判定

**未触发**。本轮新增 `demos/round-055-c-class-recheck.html`（流程 HTML，不是 UX HTML）、复核表、决策、验证报告与 `scripts/policy_guard.py`。`demos/ui-full-kcu-paper.html`、两个语言包、56 张 PNG 全部零 diff。031 / 032 的界面口径未改，不重做界面、不出新预览图。
''')

app('docs/rules/auto-command-policy.md', '''## 055 复核补记

031 的 Q1-C + Q2-A、P01–P07，032 的三档单调与 U01–U07，033 的 Q-031-01 结案（A = answer 缩写）三者一致，全部有效。048 核对表 C05 曾写「结论未随之重审」属台账笔误，054 结尾沿用该错述，055 已撤回；031 / 032 决策各追加 055 补记覆盖其历史行，历史行不重写。

本文件由 `scripts/policy_guard.py` G4 / G5 守护：默认严格档、Q1-C、Q2-A、U01 回严格，以及严格 Q1-C/Q2-A → 标准 Q1-B/Q2-C → 宽松 Q1-A/Q2-D 的单调性；CI `scan` 第 9 步执行。
''')

app('docs/records/rounds.md', f'''## 055

| 落点 | 内容 |
| --- | --- |
| docs/spec/55-round-055-instructions.txt | 逐字副本：「干」 |
| docs/records/round-055-full-readback.md | B02 复读证据：5 份字节 / 行 / SHA-256 |
| docs/records/c-class-default-recheck.md | **主交付**：C01–C10 逐条复核、3 处台账修正、具体值回显、4 项待拍板、四值 |
| docs/decisions/055-c-class-recheck.md | U/E/V、三轮迭代自评 9.3、自我批判、四值 |
| docs/verification/round-055.md | 22 条复跑证据 |
| scripts/policy_guard.py | G1–G8 口径守护 |
| .github/workflows/ci.yml | `scan` 8 → 9 steps，新增 `policy_guard` |
| demos/round-055-c-class-recheck.html | 运行逻辑演示（19 步可点，非整页 UX HTML） |
| 补记 | 031 / 032 决策、requirement-compliance-audit 055 补记、pending-question-environments 055 状态、rounds「054 结尾错述撤回」 |
| 索引与记录 | docs/index 289 项、README、decisions/index、ai-errors A200–A204、interface-log I94–I97、code-ownership-audit、implementation-strategy、ui-demo、auto-command-policy 复核补记 |

054 结尾写「下一声『干』我转去处置 048 核对表里一直挂着的 C 类 10 条擅自定默认（含你 033 澄清『A 是 answer 缩写』后我还没重审的 Q-031-01）」。用户回「干」，按该指向执行，**不另起新层**：不碰 B 类剩余项、不碰 D07 实现层、不碰 EQ-01 ~ EQ-13。

**B02**：5 份原文全文遍历；`ai-errors.md` 本轮 37282 B / 396 行。为 C 类复核定位原文：`00-requirements.txt` 第 9–14 行轻量 5 条、`11-features-input.txt:206`「有些功能你看着办」、020 指令「不要写进顶上」、021 指令「显示什么按正常我的世界现实的逻辑」。

**三个真实发现**：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E120 | 048 核对表 C05「未随澄清重审」是笔误：033 决策第 1/15/18–30 行、功能 md 第 128 行、q028 第 187 行、环境清单第 105 行均记 Q-031-01 已结案 | 追加补记，031/032 决策加 055 补记，历史行不重写 |
| E121 | 048 C06 仍写「服务器状态按 SLP 六类设计」，021 决策第 9/D07/D09 行已撤回该页面口径，`server-status.md` 第 83 行标「不再作为页面设计依据」 | 台账同步；10 处推荐位属 019 授权补全，确认 |
| E122 | 048 C08 依据写 021，「不要写进顶上」原文在 020 | 改依据为 020，9 项补回显 |
| E123 | 054 结尾沿用 C05 错述且未核 033 文件 | `rounds.md` 追加「054 结尾错述撤回」，不重写 054 回复、不改 031/032 口径、不重做界面 |
| E124 | 双向注入各只触发 1 项 FAIL | 按实记录，不补凑断言（A204） |

**C 类 10 条结论**：C01 13 项排除补回显（Q-C01 待拍板）；C02 单主题补回显（Q-C02）；C03 024 已撤回、6 处引用均带标记、无活例外；C04 补两种哈希口径后果（内容哈希会使升级确认不可达），Q-037-01 仍待拍板；C05 台账笔误；C06 前半确认 / 后半已撤回；C07 顺序既成事实；C08 依据错 + 9 项回显（Q-C08）；C09「看着办」授权成立、三值首次回显（032 后第三条改 U05）；C10 保留无冲突。**Q-031-01 已关闭**，本轮未新增 EQ，未代用户拍板。

**policy_guard**：G1 033 结案、G2 031/032 补记、G3 三处台账修正、G4 默认严格与 U01、G5 三档单调、G6 环境清单、G7 复核表 10 条、G8 054 错述撤回。CI `scan` 新增第 9 步。注入 A（删 031 补记段）→ `G2 FAIL`；注入 B（严格行改 Q1-A）→ `G5 FAIL`；恢复 → OK。

**三轮真迭代与自评**：8.2（只核状态，没打开 033、没核依据轮次、没补具体值）→ 8.9（发现 E120–E123、写复核表、撤回错述、补回显）→ **9.3**（补 G1–G8、CI step、双向注入、全量回归、流程演示与索引）。未给满分：四条待拍板未拍、C01/C02/C08 默认仍是我定的、上层四块未启动、B01/B02 历史偏差未补写。

**验证**：`cargo test --offline --lib` 351 / 0（src 零改动，仅回归），全量 **377 / 0**；Windows GNU 通过；panic / semver / i18n / lang 四守卫零命中，`policy_guard` OK；`P09_HITS 0`；CI 三条 `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE`；{html_n} 份 demos HTML 脚本通过；`yaml.safe_load` scan 9 steps；289 项必读 `MISSING 0`。UI 闸门**未触发**：UX HTML、两语言包、{png_n} 张 PNG、`src/`、`Cargo.toml`、`Cargo.lock`、`vendor/` 全部零 diff，仍 {pkgs} 包 / {third} 第三方。

**四值**：E120–E123 证据、C 类逐条结论、具体值回显、policy_guard、377 / 0 = 已证实；B01/B02 历史缺失 = 已失败（不补写）；Q-C01/Q-C02/Q-C08/Q-037-01、EQ-01 ~ EQ-13 = 未证实；真实网络 IO / GUI 接线 / UI 宿主 / 崩溃分析 / 子进程隔离 = 未启动；GUI 端到端 / Win7 与 MSVC 运行时 = 受阻。独立验证「部分通过」，**未发通过标记**。

**下一步**：B 类剩余 B04（UI 框架）/ B05（HMCL 代码）/ B07（插件独立进程）/ B09（32 位）/ B10（完全无法失误）需 EQ-01 / EQ-03 的 Win7 TLS 与 UI 宿主口径；或用户点 EQ 任一编号 / 回 Q-C01、Q-C02、Q-C08、Q-037-01 任一待拍板项。
''', '## 055\n')

p = Path('docs/index.md')
t = p.read_text()
a = '282. src/core/region.rs\n\n读取命令：'
if a in t and '283. docs/spec/55-round-055-instructions.txt' not in t:
    t = t.replace(a, '''282. src/core/region.rs
283. docs/spec/55-round-055-instructions.txt
284. docs/records/round-055-full-readback.md
285. docs/records/c-class-default-recheck.md
286. docs/decisions/055-c-class-recheck.md
287. docs/verification/round-055.md
288. scripts/policy_guard.py
289. demos/round-055-c-class-recheck.html

读取命令：''', 1)
    t = t.replace('docs/verification/round-054.md src/core/region.rs; do printf',
                  'docs/verification/round-054.md src/core/region.rs docs/spec/55-round-055-instructions.txt docs/records/round-055-full-readback.md docs/records/c-class-default-recheck.md docs/decisions/055-c-class-recheck.md docs/verification/round-055.md scripts/policy_guard.py demos/round-055-c-class-recheck.html; do printf', 1)
    p.write_text(t); print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 055 |', p.read_text(), count=1)
sec = f'''

## 055 C 类 10 条复核

`docs/records/c-class-default-recheck.md` 逐条复核 048 核对表的 C 类 10 条，**不代拍板**：C03 确认 024 已撤回无残留；C05 台账笔误（Q-031-01 早在 033 结案，A = answer 缩写）、C06 台账滞后（SLP 六类已在 021 撤回）、C08 依据轮次错（原文在 020）三处追加补记；054 结尾沿用错述已撤回。C01 13 项排除、C02 单主题、C08 9 项导航、C09 三值、C04 两种哈希后果全部补回显。

新增 `scripts/policy_guard.py`（G1–G8）与 CI `scan` 第 9 步，守护 031 默认严格档、032 三档单调、033 结案；双向注入各 1 项 FAIL，恢复后 OK。`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / {png_n} 张 PNG 全部零 diff，仍 **{pkgs} 包 / {third} 第三方**；`cargo test --offline` 全量 **377 / 0**（仅回归）。待拍板：Q-C01 / Q-C02 / Q-C08 / Q-037-01；Q-031-01 已关闭。
'''
if '## 055 C 类 10 条复核' not in t:
    p.write_text(t.rstrip() + sec); print('README_OK')
else:
    p.write_text(t); print('README_SKIP_DUP')

print('ALL_DOCS_OK')

from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
src_files = list((ROOT / 'src').rglob('*.rs'))
src_lines = sum(len(p.read_text().splitlines()) for p in src_files)
lib_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in src_files)
int_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in (ROOT / 'tests').rglob('*.rs'))
total_tests = lib_tests + int_tests
html_files = len(list((ROOT / 'demos').glob('*.html')))
png_files = len(list((ROOT / 'demos/preview').glob('[0-9][0-9]-*.png')))
print('REAL', 'pkgs', pkgs, 'third', third, 'src_files', len(src_files),
      'src_lines', src_lines, 'lib', lib_tests, 'int', int_tests,
      'total', total_tests, 'html', html_files, 'png', png_files)

Path('docs/spec/48-round-048-instructions.txt').write_text(
    '干，还有就是我之前翻的时候发现了你还是有部分硬编码文字，'
    '还有就是万一有人他喜欢搞暴力测试，功能就会被玩坏，或者喜欢删某些东西，'
    '所以说都需要做预防，还有就是我发现我之前提供给你的那个文档，'
    '除了我自己做出来的决断以外其他的没有被决断的地方你好像有一些没遵守。\n'
)
print('SPEC_OK')

D = {}

D['docs/decisions/048-hardening-i18n-compliance.md'] = f'''# 第 048 轮：硬编码清零、破坏性输入防护、原始需求合规核对

| 项 | 值 |
| --- | --- |
| 编号 | 048 |
| 状态 | 已实现已验证；上层（网络 / UI / 崩溃分析 / 子进程隔离）未启动 |
| 依据 | docs/spec/48-round-048-instructions.txt |
| 前序 | 023 Fluent 方案、032 修 27 处中文 key、046 panic_guard、047 semver_guard、045/047 环境清单 |
| 本轮性质 | 三轨：① 硬编码清零 ② 破坏性场景防护 ③ 原始需求逐条核对；零新增第三方依赖 |

## 开工核查

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-047-A | 远端 ref | `d71e8b5`，message `round 047 rollback version precedence and semver guard` |
| V-047-B | 本地 HEAD | `c97e778`，990 文件，工作区干净 |
| V-047-C | 临时凭据 | 核查后删除，全仓 `NO_CREDENTIAL`、`.git/config` 干净 |

## 一、硬编码文字（你翻到的那部分）

| 位置 | 048 前 | 处置 |
| --- | --- | --- |
| `src/plugins/fault.rs` 产品层 | 4 处中文字符串字面量（标题、正文、两个按钮） | U99：改成 5 个语义 key + `body_args`，`src/` 非测试段中文 **0** |
| `demos/ui-full-kcu-paper.html` DOM 属性 | **399 个** `data-i18n` 值直接是中文（344 唯一） | U100：全换成 `t.NNNN` |
| 同一文件 DOM 纯文本节点 | **405 个**含中文的标签无 `data-i18n` | U100：注入 `data-i18n`，原文收进 `ZH_TEXT` |
| 字典 | 只有 `EN`（88 组语义 key）与一份中文键 `EN_TEXT` | 生成 **659 组** `ZH_TEXT` / `EN_TEXT`，`tr()` 中文态走 `ZH_TEXT` |

032 只修了设置分组里 27 处中文 key，其余 372 处仍在；`src/plugins/fault.rs` 是 037 落地插件故障弹窗时新写的产品层中文。两处都没被之前的守卫覆盖。

| 编号 | 动作 |
| --- | --- |
| U99 | `FaultReport` 改为 `title_key` / `body_key` / `body_args` / `primary_key` / `secondary_key`；原 6 个测试断言同步改 key，未删验收项。 |
| U100 | `scripts/round048_i18n.py` 自动转换：中文 key → 复用同一 `t.NNNN`，纯文本节点在开标签注入属性（不改 DOM 结构）；重生成字典与 `tr()`。JS `new Function` 通过。 |
| U101 | `scripts/i18n_guard.py` + CI `i18n_guard` step：扫 `src/` 37 文件非测试段字符串字面量、有效 UX 演示的 DOM 中文 key 与裸中文节点。双向验证注入 `data-i18n="首页"` → `I18N_GUARD_FAIL 1`，恢复 → `I18N_GUARD_OK`。历史稿 2 份显式排除并输出。 |

**如实登记三处未清零**：
- `<script>` 数据源仍有 **298 行含中文**（671 个单引号字符串 / 503 唯一、11 个模板串、36 个双引号片段），是公告正文、弹窗描述、实例表格等演示数据，不在 DOM 守卫范围；语言包迁移见 EQ-14。
- 英文态 `EN_TEXT` 有 **567 条**回退中文；旧字典只有 88 组语义 key 有译文，词级补译只修了 4 条。DOM 结构已 key 化，译文覆盖不全。
- `ui-full-kcu-v2.html` / `ui-full-lightweight.html` 是 017 / 016 历史稿（018 标记作废），守卫排除，未删除。

## 二、暴力测试与删文件防护

一手资料：https://owasp.org/www-community/attacks/Path_Traversal —— 「By manipulating variables that reference files with dot-dot-slash (../) sequences and its variations or by using absolute file paths, it may be possible to access arbitrary files」；「Validate the user's input by only accepting known good – do not sanitize the data」。Std 文档：`std::path::Component` 把路径拆成 `Prefix` / `RootDir` / `CurDir` / `ParentDir` / `Normal`；`PoisonError::into_inner`（046 已取）。

| 编号 | 场景 | 落地 |
| --- | --- | --- |
| U102 | 超长、空值、控制字符 | `check_text(s, limit)`，返回 `Err` 不 panic |
| U102 | id 洪泛 | `check_ids`：总量 ≤ 10000、单项 ≤ 256B；接入 `http::plan`，构造请求前拦下 |
| U102 | 路径穿越 / 绝对路径 / Windows 保留名 / 超深 | `safe_join(root, rel)`：遍历 `std::path::Component`，拒 `Prefix`/`RootDir`、越出 root 的 `ParentDir`、`CON`/`NUL` 等、控制字符、深度 > 32；接入 `PathResolver::resolve_relative` |
| U102 | 用户删了配置 / 语言包 / 图标 | `read_or_default` 回默认值并返回「是否回退」标志，不 panic；`require_file` 对必需文件给明确错误，不静默创建 |
| U102 | 必需文件被删 | 同上，返回 `Err`，不假装默认值就是真实配置 |
| U102 | 高频重复点击 / 并发打爆 | `OpBudget`：1 秒滚动窗口、原子计数、上限可设；锁中毒走 `PoisonError::into_inner` |
| U102 | 已有防护复核 | `plugins/icon.rs` 的 `MAX_SVG_BYTES = 16 KiB` 已生效（044）；`core/cache.rs` 容量有界（029）；`core/config.rs` 畸形输入硬化（035） |

`src/core/robust.rs` 241 行，8 个测试真跑：删文件→回退→写回→再删→必需文件报错、10 万个 id 被拒、`../` / 绝对路径 / `CON` / 控制字符 / 超深被拒、8 线程并发下 `OpBudget` 不超上限、锁中毒后仍可服务。

`Cargo.toml` / `Cargo.lock` / `vendor/` **一行未动**，仍 {pkgs} 包 / {third} 第三方。**如实登记**：标准库 API 用法 + 项目策略清单，不是第三方库替换。

## 三、原始需求逐条核对

`docs/records/requirement-compliance-audit.md` 把 `00-requirements.txt`（261 行）、`11-features-input.txt`、`12-server-features-input.txt` 与各轮指令分成四类：

| 类 | 数量 | 内容 |
| --- | --- | --- |
| A 已决断且遵守 | 抽样 11 条 | 27 顺延、D06 启用、批量请求、缓存异步、弹窗可关、双击绑定、许可页、槽位锁定、档位、UI 闸门、上层用别人代码 |
| B 已决断但未遵守 | **10 条** | 交付格式缺时间戳/自我批判、开工未逐字复读原文、`/v1/batch` 与 `https` 写死、未用 UI 框架、未引 HMCL 代码、声明页三项内容未做、插件独立进程未实现、境外限制未实现、32 位未验证、未停在「完全无法失误」 |
| C 未决断我擅自定默认 | **10 条** | 轻量 13 项排除、实现层单主题、L1–L3 纯 std 例外（024 已撤）、身份哈希口径、「两个问题 A」未随澄清重审、推荐位 10 处与 SLP 六类、上层起手顺序、一级导航 9 项、028 三个默认值、历史稿保留 |
| D 文档要求但标未启动 | **9 组** | 手机连接、文件管理 40+、开服器 27+、4 项交互细节、LICENSE/图片仓/代码对比、上层 4 块、声明页 3 项、正常启动器 6 项、4 个未验证架构 |

B03 具体证据：`src/lightweight/download.rs::plan` 硬编码 `scheme: "https"`、`path: "/v1/batch"`，而 `core/config.rs` 已有 `endpoints` 表却没被读。C01/C02 是 016 我自己写的「13 项排除」「实现层单主题」，你只给了轻量 5 条功能，没批准排除清单。

新增 **EQ-14**（演示数据源语言包迁移）与 **EQ-15**（端点配置化），具体环境与选项已写进清单和核对表，本轮**未代你决断**。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo test --offline --lib`：**{lib_tests} / 0**（047 是 269；新增 robust 8 / http 2 / paths 1）。 |
| V-B | `http_construct` 7 / 0、`window_handle_contract` 6 / 0、`plugin_lifecycle_load` 7 / 0、`plugin_abi_load` 6 / 0，合计 **{total_tests} / 0**。 |
| V-C | `cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-D | `panic_guard` / `semver_guard` / `i18n_guard` 三守卫零命中；CI scan job 7 个 step。 |
| V-E | `render_ui.py` 重渲 **{png_files} 张 PNG** 通过；首页全尺寸实拍中文完整，没有 key 顶替文案。 |
| V-F | 必读 248 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，{html_files} 份 HTML 脚本通过。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E89 | `i18n_guard` 首版扫全部 `ui-full-*.html`，把 017/016 两份作废历史稿的 299 处中文判 FAIL | 设 `ACTIVE` 集合只判当前有效演示，历史稿显式列进 `excluded_history` 输出 |
| E90 | 词级补译只把 4 条英文译文补上，567 条仍回退中文 | 如实登记，不宣称英文态完整；列 EQ-14 |
| E91 | 首次统计把 `<style>` 内容与 `<title>` 算成裸中文节点 | 守卫与转换脚本都设 `SKIP_TAGS`，重跑后 DOM 裸节点 0 |
| E92 | `render_ui.py` 重渲后需人眼确认中文没被 key 顶替 | 读 `01-home.png` 实拍确认，截图入交付 |

## 四值

| 项 | 值 |
| --- | --- |
| 399 中文 key / 405 裸节点 / 4 处产品层中文清零、659 组字典 | 已证实 |
| robust 8 类场景、{total_tests} / 0、三守卫零命中、零新增依赖 | 已证实 |
| B 类 10 条 / C 类 10 条 / D 类 9 组偏差如实登记 | 已证实 |
| 演示数据源 298 行中文、英文态 567 条回退 | 已证实（未清零） |
| EQ-14 / EQ-15、B/C/D 偏差处置 | 未证实（待拍板） |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-048.md'] = f'''# 第 048 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 048 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 三轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 047 远端 `GET /git/ref/heads/main` | `d71e8b5` | 已证实 |
| V2 | `cargo test --offline --lib` | **{lib_tests} / 0** | 已证实 |
| V3 | `cargo test --offline --lib core::robust` | 8 / 0 | 已证实 |
| V4 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V5 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V6 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0 | 已证实 |
| V7 | `cargo test --offline --test plugin_abi_load` | 6 / 0 | 已证实 |
| V8 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V9 | `python3 scripts/panic_guard.py` | `PANIC_GUARD_OK files 37 hits 0` | 已证实 |
| V10 | `python3 scripts/semver_guard.py` | `SEMVER_GUARD_OK version_files 3 hits 0` | 已证实 |
| V11 | `python3 scripts/i18n_guard.py` | `I18N_GUARD_OK rs_files 37 ux_html 1 hits 0 script_cn_lines_known 298` | 已证实 |
| V12 | i18n 守卫双向验证 | 注入 `data-i18n="首页"` → FAIL 1；恢复 → OK | 已证实 |
| V13 | DOM 中文 key / 裸中文节点统计 | 0 / 0（转换前 399 / 405） | 已证实 |
| V14 | `node new Function` 全部 demos HTML | ALL_JS_OK，{html_files} 份 | 已证实 |
| V15 | `python3 scripts/render_ui.py` | shots=51，{png_files} 张 PNG，overview 2549707 B | 已证实 |
| V16 | 读 `demos/preview/01-home.png` | 中文完整，无 `t.NNNN` 顶替 | 已证实 |
| V17 | `Cargo.lock` 包列表 | **{pkgs} 包 / {third} 第三方**（与 047 相同） | 已证实 |
| V18 | `git diff --name-only -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V19 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan，scan 7 steps | 已证实 |
| V20 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V21 | 禁用词 / 「同上」 / P09 / hardcode 扫描 | 零命中 | 已证实 |
| V22 | 必读文件循环 | REQUIRED=248 MISSING=0 | 已证实 |
| V23 | 合规核对表 | A 抽样 11 / B 10 / C 10 / D 9 组，均非空 | 已证实 |
| V24 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 硬编码清零、破坏性防护、合规核对、{total_tests} / 0 | 已证实 |
| 演示数据源 298 行中文、英文态 567 条回退 | 已证实（未清零，EQ-14） |
| B/C/D 偏差处置、EQ-14 / EQ-15 | 未证实（待拍板） |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| {total_tests} 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。
'''

D['docs/research/30-input-hardening.md'] = '''# 破坏性输入与路径穿越一手资料（048）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://owasp.org/www-community/attacks/Path_Traversal | 「By manipulating variables that reference files with "dot-dot-slash (../)" sequences and its variations or by using absolute file paths, it may be possible to access arbitrary files and directories」；「Validate the user's input by only accepting known good – do not sanitize the data」；「normalize the input before using in file io API's」 | 已证实 |
| https://owasp.org/www-community/attacks/Path_Traversal | 编码变体 `%2e%2e%2f` 代表 `../`；攻击别名 dot-dot-slash / directory traversal / backtracking | 已证实 |
| https://doc.rust-lang.org/std/path/enum.Component.html | `Prefix` / `RootDir` / `CurDir` / `ParentDir` / `Normal` 五种分量；分量由标准库解析，项目侧只做策略判定 | 已证实 |
| https://doc.rust-lang.org/std/sync/struct.PoisonError.html | `pub fn into_inner(self) -> T`；046 已用于锁中毒恢复 | 已证实 |
| https://doc.rust-lang.org/std/fs/fn.read_to_string.html | 读失败返回 `io::Result`，不 panic；048 的 `read_or_default` 据此回退 | 已证实 |
| `src/plugins/icon.rs`（044） | `MAX_SVG_BYTES = 16 KiB`，`s.is_empty() || s.len() > MAX_SVG_BYTES` 已在校验入口 | 已证实 |
| `src/core/cache.rs`（029 / 046） | `LruCache` 容量有界、锁中毒恢复 | 已证实 |

| 编号 | 结论 |
| --- | --- |
| R36 | OWASP 建议「只接受已知好值」而不是清洗输入，048 的 `safe_join` 因此逐分量拒绝，而不是把 `../` 字符串删掉。 |
| R37 | 绝对路径与 `..` 越界是两类独立入口，都要拒；Windows 保留设备名（CON/NUL/COM1…）在 Linux 上也要检查，因为目标平台是 Windows。 |
| R38 | 「删文件」不等于「崩溃」：可选文件回默认值、必需文件给明确错误，二者不能都静默回默认。 |
| R39 | 高频重复与并发洪泛用原子计数 + 滚动窗口限流；锁中毒时按 046 的口径恢复，不让防护模块自身成为崩溃点。 |
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


app('docs/decisions/index.md', '| 048 | 硬编码清零、破坏性输入防护、原始需求合规核对 | 已实现已验证；上层未启动 | 048-hardening-i18n-compliance.md |')
app('docs/research/index.md', '| 30 | 30-input-hardening.md | 路径穿越与破坏性输入一手资料 | 7 已证实 |')

app('docs/records/pending-question-environments.md', '''---

**EQ-14 演示数据源语言包迁移（048）**

环境：`demos/ui-full-kcu-paper.html` 的 `<script>` 段有 `NOTICES` / `POPUPS` / `INS` / `SRV` / `AUTH` / `OB` / `CREDITS` / `AUTO_EFFECT` 等常量数组，298 行含中文（671 个单引号字符串 / 503 唯一、11 个模板串、36 个双引号片段）。023 定的实现方案是 Project Fluent `.ftl` + `i18n-embed`，语言包放 `C:\\KCU\\i18n\\<locale>\\`，插件可追加。当前 `src/` 无 Fluent 依赖（`Cargo.lock` 26 包 / 25 第三方）。英文态 `EN_TEXT` 有 567 条回退中文。

要选：① 实现层按 023 落 Fluent，演示层只保留 key 与最小占位数据 ② 演示层先拆出独立 `demos/lang/*.json`，中文/英文各一份，`setLang` 时重建数组 ③ 演示数据源维持现状，明确标注「仅中文演示数据」，不承诺英文态。

不选：英文态切语言后公告正文、弹窗描述、表格行仍是中文。详见 `docs/records/requirement-compliance-audit.md`。

---

**EQ-15 端点配置化（048）**

环境：`src/lightweight/download.rs::plan` 硬编码 `scheme = "https"`、`path = "/v1/batch"`；`src/core/config.rs` 已有 `endpoints` 表与 `set_endpoint` / `endpoint`，但 `plan()` 没读它。00-requirements 第 7.3 节「禁止硬编码环境假设」，11-features-input「尽量不要 api 写死…那些联网他们有可能后面会更新相关的端口」。

要选：① `plan()` 改从 `Config::endpoint` 取 scheme / authority / path，缺省才回内置 ② 保持代码内常量，但集中到 `src/core/endpoints.rs` 单文件 ③ 维持现状，登记为已知偏差。

不选：B03 保持未遵守。详见 `docs/records/requirement-compliance-audit.md`。
''')

app('docs/records/interface-log.md', '''## 048 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I68 | `src/core/robust` | 新增模块：文本/id 边界、`safe_join`、`read_or_default`、`require_file`、`OpBudget` |
| I69 | `src/core/http` / `paths` | `plan` 接 `check_ids`；新增 `resolve_relative` |
| I70 | `src/plugins/fault` | 4 处产品层中文改 5 个语义 key + `body_args` |
| I71 | `demos/ui-full-kcu-paper.html` | 399 中文 key + 405 裸节点收敛为 659 组 `ZH_TEXT`/`EN_TEXT` |
| I72 | CI | scan job 加 `i18n_guard` step，脚本 `scripts/i18n_guard.py` |
| S47 | 状态 | U99–U103 已证实；零新增依赖；EQ-14 / EQ-15 待拍板 |
''')

app('docs/checklists/ai-errors.md', '''## 048 轮新增

| 编号 | 防错项 |
| --- | --- |
| A161 | 守卫扫 `ui-full-*.html` 时要设 ACTIVE 集合；历史作废稿会淹没结果，排除项要打印出来而不是静默跳过。 |
| A162 | `data-i18n` 的值必须是语义 key，不能是中文文案；中文当 key 等于把语言包写死在标签里。 |
| A163 | 修改 DOM 文案属性后必须重渲 PNG 并人眼读一张，确认没有 key 顶替文案；JS 语法通过不等于渲染正确。 |
| A164 | 原始需求要逐条分「已决断 / 未决断」核对；未决断的条目不能由改动作者代为拍板，也不能长期以「未启动」挂账不回显。 |
| A165 | 路径校验用标准库 `Component` 逐分量判定，不要自己删 `../` 字符串；OWASP 明确「只接受已知好值，不要清洗」。 |
''')

app('docs/rules/ui-demo.md', '''## 048 闸门判定

本轮改动了 `demos/ui-full-kcu-paper.html` 的文案属性（399 个中文 key → 语义 key、405 个裸节点注入 `data-i18n`），属界面演示变更，**闸门触发**。按规则重渲 `python3 scripts/render_ui.py`：shots=51、56 张 PNG、总览 2549707 B；读 `01-home.png` 实拍确认中文完整、无 `t.NNNN` 顶替。`src/` 无界面实现改动，实现层仍等手感确认。
''')

app('docs/records/code-ownership-audit.md', f'''## 048 健壮性与文案归位（零新增依赖）

| 项 | 047 | 048 |
| --- | --- | --- |
| 第三方 crate 进构建 | {third} | **{third}**（不变） |
| `Cargo.lock` 包数 | {pkgs} | **{pkgs}**（不变） |
| `src/` 文件 | 36 | **{len(src_files)}**（+ `core/robust.rs`） |
| `src/` 行数 | 6245 | **{src_lines}** |
| 测试 | 269 单元 + 26 集成 = 295 | **{lib_tests} 单元 + {int_tests} 集成 = {total_tests}** |

`src/core/robust.rs` 241 行：文本/id 边界、基于 `std::path::Component` 的路径策略、文件被删或损坏的回退、必需文件明确报错、`OpBudget` 高频限流。接入 `http::plan` 与 `PathResolver::resolve_relative`。`src/plugins/fault.rs` 4 处产品层中文改成语义 key。

**如实登记**：标准库 API 用法 + 项目策略清单 + 文案归位，不是第三方库替换；`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动。新增 `scripts/i18n_guard.py` 与 CI step。自写通用算法已收敛，剩余是项目特有编排与业务规则。
''')

app('docs/design/implementation-strategy.md', '''## 048 输入防护与文案归位

| 层 | 状态 |
| --- | --- |
| CI `panic_guard` / `semver_guard` / `i18n_guard` | 已实现（046 / 047 / 048） |
| 破坏性输入与路径穿越防护 | **已实现（048）**，零新增依赖 |
| 产品层中文硬编码 | **清零（048）**；演示 DOM 层 key 化完成 |
| 演示数据源语言包 | 未抽离（298 行中文），EQ-14 待拍板 |
| 端点配置化 | 未做（`/v1/batch` 写死），EQ-15 待拍板 |
| 真实窗口 / WebView / 渲染 / 崩溃分析 | 未启动，具体环境见 EQ-01 / EQ-04 / EQ-05 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动，具体环境见 EQ-03 |
''')

app('docs/records/rounds.md', f'''## 048

| 落点 | 内容 |
| --- | --- |
| docs/spec/48-round-048-instructions.txt | 逐字副本 |
| docs/decisions/048-hardening-i18n-compliance.md | V-047-A~C、U99-U103、V-A~V-F、E89-E92、四值 |
| docs/verification/round-048.md | 24 条复跑证据 |
| docs/research/30-input-hardening.md | 7 个锚点 / R36-R39 |
| docs/records/requirement-compliance-audit.md | **主交付之一**：A/B/C/D 四类逐条核对 |
| src/core/robust.rs / http.rs / paths.rs / plugins/fault.rs | 防护模块、接入、文案归位 |
| scripts/round048_i18n.py / i18n_guard.py / .github/workflows/ci.yml | 转换脚本、守卫、CI step |
| demos/ui-full-kcu-paper.html + demos/preview/ | 659 组字典、56 张 PNG 重渲 |
| demos/round-048-hardening.html | 13 步运行逻辑演示 |
| 索引与记录 | docs/index 247 项、README、两个 index、ai-errors A161-A165、code-ownership-audit、implementation-strategy、ui-demo 闸门判定、interface-log、rounds |

你指出三件事：还有硬编码文字、暴力测试/删文件要预防、原始文档里未决断的地方有没遵守。三轨并行处理，没合并成一个「优化」。

**硬编码**：查到 `src/plugins/fault.rs` 4 处产品层中文（037 落地故障弹窗时写的）；`ui-full-kcu-paper.html` 里 399 个 `data-i18n` 值直接是中文（344 唯一）、405 个裸中文文本节点无 key —— 032 只修了设置分组 27 处。全部收敛：产品层改 5 个语义 key + `body_args`，DOM 层生成 659 组 `ZH_TEXT`/`EN_TEXT`，`tr()` 中文态走字典。新增 `i18n_guard.py` + CI step，双向验证注入 `data-i18n="首页"` 即 FAIL、恢复 OK；历史作废稿 2 份显式排除并打印。如实登记三处未清零：script 数据源 298 行中文、英文态 567 条回退中文、两版历史稿。

**破坏性防护**：一手资料取 OWASP Path Traversal（「只接受已知好值，不要清洗」、`%2e%2e%2f` 变体）与 `std::path::Component`。新增 `src/core/robust.rs` 241 行：文本/id 边界、拒绝绝对路径与 `..` 越界、Windows 保留名、超深、控制字符；文件被删/损坏回默认并带标志、必需文件给明确错误；`OpBudget` 1 秒滚动窗口限流。接入 `http::plan`（构造请求前拦 id 洪泛）与 `PathResolver::resolve_relative`。8 个测试真跑删文件→回退→写回→再删、10 万个 id 被拒、8 线程并发不超上限、锁中毒仍可服务。

**合规核对**：`requirement-compliance-audit.md` 把 00-requirements（261 行）+ 两份功能输入分成四类：A 已决断且遵守 11 条、B **已决断但未遵守 10 条**（交付格式缺时间戳/自我批判、开工未逐字复读原文、`/v1/batch` 与 `https` 写死、未用 UI 框架、未引 HMCL 代码、声明页三项内容未做、插件独立进程未实现、境外限制未实现、32 位未验证、未停在「完全无法失误」）、C **未决断我擅自定默认 10 条**（轻量 13 项排除、实现层单主题、L1–L3 纯 std 例外、身份哈希口径、「两个问题 A」未随澄清重审、推荐位 10 处与 SLP 六类、上层起手顺序、一级导航 9 项、028 三个默认值、历史稿保留）、D **文档要求但标未启动 9 组**。新增 EQ-14（演示数据源语言包迁移）与 EQ-15（端点配置化），本轮未代你决断。

验证：{lib_tests} 单元 / 0 + 7 http_construct / 0 + 6 窗口契约 / 0 + 7 lifecycle / 0 + 6 abi / 0 = **{total_tests} / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过；三守卫零命中、CI scan 7 steps、{html_files} 份 HTML 脚本通过。`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 {pkgs} 包 / {third} 第三方。UI 闸门触发：`render_ui.py` 重渲 51 场景 / {png_files} 张 PNG，读 `01-home.png` 实拍确认中文完整、无 key 顶替。

本轮真实问题：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E89 | `i18n_guard` 首版扫全部 `ui-full-*.html`，两份作废历史稿 299 处中文判 FAIL | 设 ACTIVE 集合，排除项显式输出 |
| E90 | 词级补译只修 4 条，567 条英文态仍回退中文 | 如实登记，列 EQ-14 |
| E91 | 首次统计把 `<style>` / `<title>` 算成裸中文节点 | 设 `SKIP_TAGS`，重跑 DOM 裸节点 0 |
| E92 | 文案属性改造后需确认渲染没被 key 顶替 | 读首页 PNG 实拍确认 |

EQ-01 ~ EQ-15 具体环境仍待拍板；真实网络 IO、UI 宿主、崩溃分析、子进程隔离、028 三项实现、CF F17、特殊版代码、本项目 LICENSE、UX 手感均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '241. docs/records/eq13-rollback-conditions.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''241. docs/records/eq13-rollback-conditions.md
242. docs/spec/48-round-048-instructions.txt
243. docs/records/requirement-compliance-audit.md
244. docs/decisions/048-hardening-i18n-compliance.md
245. docs/research/30-input-hardening.md
246. scripts/i18n_guard.py
247. demos/round-048-hardening.html
248. docs/verification/round-048.md

读取命令：''', 1)
    t = t.replace('docs/records/eq13-rollback-conditions.md; do printf',
                  'docs/records/eq13-rollback-conditions.md docs/spec/48-round-048-instructions.txt docs/records/requirement-compliance-audit.md docs/decisions/048-hardening-i18n-compliance.md docs/research/30-input-hardening.md scripts/i18n_guard.py demos/round-048-hardening.html docs/verification/round-048.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 048 |', p.read_text(), count=1)
section = f'''

## 048 硬编码清零、破坏性防护、合规核对

`src/plugins/fault.rs` 4 处产品层中文改成 5 个语义 key；`demos/ui-full-kcu-paper.html` 399 个中文 key 与 405 个裸中文节点收敛为 **659 组** `ZH_TEXT`/`EN_TEXT`；新增 `scripts/i18n_guard.py` 与 CI step，双向验证通过。历史稿 2 份显式排除。

新增 `src/core/robust.rs`：长度/空值/控制字符、id 洪泛、基于 `std::path::Component` 的路径穿越与保留名拒绝、文件被删或损坏回退、必需文件明确报错、`OpBudget` 高频限流。接入 `http::plan` 与 `PathResolver::resolve_relative`。

`docs/records/requirement-compliance-audit.md` 把原始需求逐条分成四类：已决断且遵守 11 条、**已决断但未遵守 10 条**、**未决断我擅自定默认 10 条**、文档要求但标未启动 9 组。新增 EQ-14 / EQ-15 待拍板。

`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 **{pkgs} 包 / {third} 第三方**。`cargo test --offline` 合计 **{total_tests}/0**（{lib_tests} 单元 + {int_tests} 集成），Windows GNU 交叉检查通过，三守卫零命中，56 张 PNG 重渲并人眼确认中文完整。
'''
if '## 048 硬编码清零' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

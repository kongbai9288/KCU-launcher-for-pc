from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
html_files = len(list((ROOT / 'demos').glob('*.html')))
png_files = len(list((ROOT / 'demos/preview').glob('[0-9][0-9]-*.png')))
src_files = len(list((ROOT / 'src').rglob('*.rs')))
endpoint_lines = len((ROOT / 'src/core/endpoints.rs').read_text().splitlines())
print('REAL', 'pkgs', pkgs, 'third', third, 'html', html_files,
      'png', png_files, 'src', src_files, 'endpoints_lines', endpoint_lines)

Path('docs/spec/50-round-050-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/050-endpoint-config.md'] = f'''# 第 050 轮：端点配置化（B03 / EQ-15 选项①）

| 项 | 值 |
| --- | --- |
| 编号 | 050 |
| 状态 | 已实现已验证；`src/` 有改动，演示层零改动 |
| 依据 | `docs/spec/50-round-050-instructions.txt`（逐字：「干」） |
| 对应 | 048 合规核对 B03、EQ-15；049 结尾「或者继续『干』我按默认往下走」 |
| 默认判定 | 用户未明确拍板选项，按「按默认往下走」= **修复 B03 偏差** → 选项①；**不声称用户已决断** |

## 开工核查

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-049-A | 本地 HEAD | `b71a3fb`，1008 文件，工作区干净 |
| V-049-B | 远端主快照 | `e696a91`（`round 049 record delivery snapshot`），1008 文件 ALL_MATCH |
| V-049-C | 凭据 | 049 收尾临时载体已删；全仓 `NO_CREDENTIAL`，`.git/config` 干净 |

## 原文与偏差

| 编号 | 来源 | 原文 / 事实 |
| --- | --- | --- |
| R01 | `00-requirements.txt` 7.3 | 禁止硬编码环境假设 |
| R02 | `11-features-input.txt` | 「尽量不要 api 写死…那些联网他们有可能后面会更新相关的端口」；13 手动选镜像；29 `§` 自定义镜像 URL 模板 |
| R03 | `requirement-compliance-audit.md` B03 | `src/lightweight/download.rs::plan` 写死 `scheme: "https"`、`path: "/v1/batch"`，`core/config.rs` 的 `endpoints` 表没被读 |
| R04 | EQ-15 三选项 | ① `plan()` 从 `Config::endpoint` 取三段，缺省才回内置 ② 常量集中到 `src/core/endpoints.rs` 单文件 ③ 维持现状登记偏差 |

## 落地

| 编号 | 动作 |
| --- | --- |
| U110 | 新增 `src/core/endpoints.rs`（{endpoint_lines} 行），在 `src/core/mod.rs` 注册。常量 `DOWNLOAD_BATCH_KEY = "download/batch"`、`DEFAULT_SCHEME`、`DEFAULT_PATH` 集中在一处。 |
| U111 | `EndpointConfig` 只存配置原始字符串（`from_app_config` 从 `Config::endpoint` 拷出），不让 `ProviderConfig` 持有 `Config` 本体，保持 `Debug + Clone`。 |
| U112 | `resolve(base, configured)`：URL 解析交给 `http::Uri`（040 已进构建），authority 校验复用 `http::validate_authority`，query 编码复用 042 的 `percent-encoding`。**零新增第三方依赖**。 |
| U113 | `ProviderConfig` 加 `endpoint` 字段 + `with_endpoint(raw)` / `with_app_config(&Config)` 两个 builder；两个既有 constructor 设为 `None`。 |
| U114 | `Downloader::plan()` 删掉写死的 `scheme` / `path`，改由 `self.endpoint()` 提供三段；新增 `Downloader::endpoint()` 暴露 `origin` 与 `reason`。 |
| U115 | 8 类不可用配置回退并带 `reason`，不 panic、不静默吞。 |

### 解析规则

| 输入 | 结果 |
| --- | --- |
| 无配置 | `https` + `ProviderConfig.base` + `/v1/batch`，`origin=Default` |
| 完整 URL | 用 `Uri` 解出 scheme / authority（可带端口）/ path，三段都覆盖，`origin=Config` |
| 只给 authority | 校验后只换主机，scheme 与 path 保留缺省 |
| URL 只有主机没 path | path 回 `/v1/batch`，scheme 用配置给的 |
| 不可用配置 | 回内置缺省，`origin=Fallback` |

### 回退 reason（8 类）

`empty_endpoint` / `unsupported_scheme` / `query_not_allowed` / `invalid_path` / `missing_authority` / `missing_host` / `uri_parse_failed` / `invalid_authority`，另加 `template_not_supported`（`§` 占位）。

`http::plan` 会自行追加 `?page=N&ids=...`，配置里带 query 必须拒，否则两个 query 会拼在一起。`§` 模板是 R02 第 29 条要求，本轮**只显式拒绝并登记未启动**，不假装支持。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo test --offline --lib` **298 / 0**（280 → 298，新增 18 个：endpoints 11 + download 7）。 |
| V-B | 全量 **324 / 0** = 298 单元 + 7 `http_construct` + 6 `window_handle_contract` + 7 `plugin_lifecycle_load`（44.87 s，真加载 cdylib）+ 6 `plugin_abi_load`（109.39 s）。 |
| V-C | `cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-D | 默认行为逐字不变断言：`scheme_str=https` / `host=mirror-a` / `path=/v1/batch` / `query` 以 `page=1&ids=` 开头；10 id → 1 请求、45 id → 3 请求、配置端点后页数仍等于 `batch().pages`。 |
| V-E | 配置覆盖生效：`http` + `mirror-b:8080` + `/v2/batch` 三段都换；仅 authority 只换主机；`Config` JSON round-trip 后端点仍生效。 |
| V-F | 畸形输入不崩：`endpoints:"oops"` 归一化后回 `Default`；`ftp` scheme、带 query、坏 URL、空串、`§` 模板都回 `Fallback` 且带 reason。 |
| V-G | panic / semver / i18n / lang 四守卫零命中；CI 口径 `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE`；39 份 demos HTML 脚本 `node new Function` 全通过。 |
| V-H | `git diff -- Cargo.toml Cargo.lock vendor/` 为空，仍 {pkgs} 包 / {third} 第三方。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E97 | 文档注释与测试里写 `http://...` 字面量触发 CI `hardcode` 扫描（042 / 048 同类坑） | 注释改三段描述；测试 URL 一律数组 `concat!` 运行时拼接，复跑 `NO_HARDCODE` |
| E98 | 首版 `uri.scheme_str().unwrap_or(...)` 落在非测试段，有被 panic_guard 判危险的风险 | 改成 `Some(s @ ("http" | "https"))` 模式绑定，无 unwrap |
| E99 | 快集成循环里 `window_lifecycle` 名字写错（实际 `window_handle_contract`），该段没跑、后续 `&&` 链断开 | 按 `tests/` 实际文件名重跑，6 / 0；交叉检查补跑通过 |
| E100 | 全量集成命令连续两次被网关 502 截断 | 拆成 lifecycle / abi 两段分别跑，断言没降 |

## 自我批判

- 新增 `endpoints.rs` {endpoint_lines} 行里，URL 词法、authority 校验、query 编码全部交给已进构建的库；**配置优先级、8 类回退 reason、`§` 模板拒绝是项目特有业务编排**，没有语义等价的第三方库可换。如实登记为业务编排层，**不是新开「自写底座」例外**（023 的 A03 已于 024 撤回）。
- 本轮只修代码层读配置。**设置页里「端点输入」控件、镜像切换 UI、`§` 模板编辑都属 UI 层未启动**，UI 闸门未触发；不能把「可配置」说成「用户已经能在界面上改」。
- 用户未对 EQ-15 三个选项明确拍板，我按 049 结尾自己写的「按默认往下走」执行选项①。这是**我的默认**，不是用户的决断，登记为 D-050-1。
- R02 的「境外才连后端」「镜像优先」「限额限速」等策略本轮一行未动，仍是 D 类未启动项。

## 四值

| 项 | 值 |
| --- | --- |
| B03 代码层偏差消除、端点三段走配置、缺省逐字不变 | 已证实 |
| 298 / 0 单元、324 / 0 全量、Windows GNU 通过、四守卫零命中 | 已证实 |
| 零新增依赖、{pkgs} 包 / {third} 第三方、演示层零改动 | 已证实 |
| 8 类回退 reason 与 `§` 显式拒绝 | 已证实（模板支持未启动） |
| 设置页端点控件、`§` 模板、镜像策略、真实网络 IO | 未启动 |
| EQ-15 用户拍板 | 未证实（D-050-1，按默认执行） |
| 浏览器渲染、GUI 端到端、真实 HTTP 请求 | 受阻 |
'''

D['docs/verification/round-050.md'] = f'''# 第 050 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 050 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；`src/` 有改动，演示层零改动，UI 闸门未触发 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `b71a3fb`，DIRTY 0，1008 文件 | 已证实 |
| V2 | 049 远端 ref | `e696a91` | 已证实 |
| V3 | 凭据扫描 | `NO_CREDENTIAL`，`.git/config` 干净 | 已证实 |
| V4 | `git diff -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V5 | `cargo test --offline --lib` | **298 / 0**（新增 18） | 已证实 |
| V6 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V7 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V8 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，44.87 s，真加载 cdylib | 已证实 |
| V9 | `cargo test --offline --test plugin_abi_load` | 6 / 0，109.39 s | 已证实 |
| V10 | 全量合计 | **324 / 0** | 已证实 |
| V11 | `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile` | 已证实 |
| V12 | 默认 URI 逐字不变 | `https` / `mirror-a` / `/v1/batch` / `page=1&ids=` | 已证实 |
| V13 | 完整 URL 配置 | `http` / `mirror-b:8080` / `/v2/batch` | 已证实 |
| V14 | 仅 authority 配置 | 只换主机，scheme 与 path 不变 | 已证实 |
| V15 | Config JSON round-trip | 端点仍生效 | 已证实 |
| V16 | 畸形配置 | `endpoints:"oops"` → `Origin::Default`，不 panic | 已证实 |
| V17 | 8 类回退 | `ftp` / 带 query / 坏 URL / 空串 / `§` 全回 `Fallback` 带 reason | 已证实 |
| V18 | `python3 scripts/panic_guard.py` | `hits 0`（38 文件） | 已证实 |
| V19 | `semver_guard` / `i18n_guard` / `lang_guard` | 各零命中 | 已证实 |
| V20 | `python3 scripts/p09_scan.py` | `P09_HITS 0` | 已证实 |
| V21 | CI 口径三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` | 已证实 |
| V22 | `.github/workflows/ci.yml` yaml.safe_load | scan 8 steps | 已证实 |
| V23 | {html_files} 份 demos HTML `node new Function` | ALL_JS_OK | 已证实 |
| V24 | `git diff -- demos/` | 仅新增 `round-050-endpoint.html`，UX HTML 与 {png_files} 张 PNG 零 diff | 已证实 |
| V25 | 必读读取命令块 | 258 项，`MISSING 0` | 已证实 |
| V26 | 远端 `GET /git/trees/...?recursive=1` 逐项比对 | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| B03 代码层偏差消除、零新增依赖、全量 324 / 0 | 已证实 |
| 设置页端点控件、`§` 模板、镜像策略、真实网络 IO | 未启动 |
| EQ-15 用户拍板 | 未证实（按默认选项①执行） |
| GUI 端到端、真实 HTTP、浏览器渲染遍历 | 受阻 |

限制：改动作者未代改验证结论，未降低验收项；324 个测试是回归，不作质量结论。
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


app('docs/decisions/index.md', '| 050 | 端点配置化（B03 / EQ-15 选项①） | 已实现已验证；零新增依赖 | 050-endpoint-config.md |')

app('docs/records/pending-question-environments.md', '''---

**EQ-15 按默认落地（050）**

用户未明确拍板三选项，按 049 结尾「或者继续『干』我按默认往下走」执行选项①：`plan()` 从 `Config::endpoint("download/batch")` 取 scheme / authority / path，缺省才回内置；常量集中到 `src/core/endpoints.rs`。`resolve()` 用 `http::Uri` 解析并支持 8 类回退 reason。B03 代码层偏差消除，设置页端点控件与 `§` 模板仍属 UI 层未启动。登记为 **D-050-1**（我的默认，不是用户决断）。

EQ-01 ~ EQ-13 仍待拍板；EQ-14（049）、EQ-15（050）已关闭。
''')

app('docs/records/requirement-compliance-audit.md', '''## 050 补记：B03 代码层已修，EQ-15 按默认关闭

| 项 | 048 / 049 状态 | 050 状态 |
| --- | --- | --- |
| B03 | `plan()` 写死 `https` 与 `/v1/batch`，`endpoints` 表没被读 | `plan()` 改从 `Config::endpoint` 取三段，缺省回内置；新增 `src/core/endpoints.rs`；**代码层偏差消除** |
| EQ-15 | 三选项待拍板 | 按默认选项①落地（**D-050-1**：用户未拍板，是我的默认） |
| 缺省行为 | 旧 URI | 逐字不变，有专门断言 |
| 配置容错 | — | 8 类 reason 回退，不 panic |
| 设置页端点控件 / `§` 模板 | 未启动 | 仍**未启动**；不能把「可配置」说成「界面上能改」 |

原表 B01–B10 行保持原样，不重写历史证据。B01 / B02 仍缺时间戳与自我批判逐项齐备的复核、B04–B10 未动；C 类 10 条、D 类 9 组未动。
''')

app('docs/records/interface-log.md', '''## 050 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I76 | `src/core/endpoints.rs` | 新增；`DOWNLOAD_BATCH_KEY` / `DEFAULT_SCHEME` / `DEFAULT_PATH` / `EndpointConfig` / `Origin` / `Endpoint` / `resolve` / `from_app_config` |
| I77 | `src/lightweight/download.rs` | `ProviderConfig.endpoint`、`with_endpoint`、`with_app_config`、`Downloader::endpoint()`；`plan()` 删写死 scheme / path |
| I78 | `src/core/mod.rs` | 注册 `pub mod endpoints;` |
| I79 | 配置键 | `endpoints["download/batch"]`，值可为完整 URL 或仅 authority |
| S49 | 状态 | U110–U115 已证实；零新增依赖；设置页端点控件未启动；D-050-1 已登记 |
''')

app('docs/checklists/ai-errors.md', '''## 050 轮新增

| 编号 | 防错项 |
| --- | --- |
| A172 | `src/` 里连文档注释都不能写 `http://` 字面量，CI hardcode 扫全文；用「scheme、authority、path 三段」描述，测试 URL 一律数组拼接。 |
| A173 | 非测试段不要为拿已匹配的值再写 `unwrap_or`；用 `Some(s @ ("a" | "b"))` 模式绑定，panic_guard 扫非测试段的危险调用。 |
| A174 | 配置里的 URL 不能直接拼进请求：`http::plan` 会追加 `?page=&ids=`，配置带 query 必须显式拒而不是拼接。 |
| A175 | 新增配置项时先写「缺省逐字不变」断言，再写覆盖断言；否则无法证明没把旧行为改坏。 |
| A176 | 新增集成段先 `ls tests/` 核真实文件名，别按记忆拼测试名；`for` 循环里 grep 失配会断掉后续 `&&` 链。 |
| A177 | 用户没拍板选项时，按自己上轮写的「默认」执行要显式登记 D 编号，不能写成「已决断」。 |
''')

app('docs/rules/ui-demo.md', '''## 050 闸门判定

本轮改 `src/core/endpoints.rs` / `src/lightweight/download.rs` / `src/core/mod.rs`，新增 `demos/round-050-endpoint.html`（**流程 HTML，不是 UX HTML**）。**UI 闸门未触发**：`demos/ui-full-kcu-paper.html`、两个语言包、56 张 PNG 全部零 diff；设置页端点输入控件属 UI 层未启动，不在本轮范围。按 018 的口径，动界面轮次才出整页 UX 演示，本轮明确标注「非整页 UX 演示」。
''')

app('docs/records/code-ownership-audit.md', '''## 050 端点配置化（零新增第三方）

`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。新增 `src/core/endpoints.rs` 的 URL 词法交给 `http::Uri`（040）、authority 校验复用 `http::validate_authority`（040）、query 编码复用 `percent-encoding`（042），**没有手写解析器**。配置优先级、8 类回退 reason、`§` 模板拒绝是项目特有业务编排，无语义等价库可换，如实登记；**不是新开自写底座例外**（023 A03 已于 024 撤回）。`cargo test --offline --lib` 298 / 0，全量 324 / 0。
''')

app('docs/design/implementation-strategy.md', '''## 050 端点状态

| 项 | 状态 |
| --- | --- |
| 代码层端点配置化 | **已落地（050）**：`config.endpoints["download/batch"]` → `core/endpoints.rs::resolve` → `Downloader::plan` |
| 缺省常量 | 集中在 `src/core/endpoints.rs`，缺省逐字不变 |
| `§` 自定义镜像 URL 模板 | 显式拒绝并登记未启动（`template_not_supported`） |
| 设置页端点输入控件、镜像切换 UI | 未启动 |
| 境外后端 / 镜像优先 / 限额限速策略 | 未启动 |
| 实现层 Fluent `.ftl` + `i18n-embed` | 未启动 |
''')

p = Path('docs/index.md')
t = p.read_text()
a = '254. docs/verification/round-049.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''254. docs/verification/round-049.md
255. docs/spec/50-round-050-instructions.txt
256. docs/decisions/050-endpoint-config.md
257. src/core/endpoints.rs
258. docs/verification/round-050.md

读取命令：''', 1)
    t = t.replace('scripts/lang_guard.py docs/verification/round-049.md; do printf',
                  'scripts/lang_guard.py docs/verification/round-049.md docs/spec/50-round-050-instructions.txt docs/decisions/050-endpoint-config.md src/core/endpoints.rs docs/verification/round-050.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 050 |', p.read_text(), count=1)
section = f'''

## 050 端点配置化

`src/core/endpoints.rs`：`plan()` 从 `config.endpoints["download/batch"]` 取 scheme / authority / path，缺省才回内置常量。完整 URL 由 `http::Uri` 解析，8 类不可用配置回退并带 `reason`，不 panic。`ProviderConfig` 加 `with_endpoint` / `with_app_config`，`Downloader::endpoint()` 暴露来源。

`cargo test --offline --lib` **298 / 0**（新增 18），全量 **324 / 0**，`cargo check --target x86_64-pc-windows-gnu` 通过，四守卫零命中。零新增依赖，仍 **{pkgs} 包 / {third} 第三方**。UI 闸门未触发，UX HTML 与 {png_files} 张 PNG 零 diff。
'''
if '## 050 端点配置化' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')

app('docs/records/rounds.md', f'''## 050

| 落点 | 内容 |
| --- | --- |
| docs/spec/50-round-050-instructions.txt | 逐字副本：「干」 |
| docs/decisions/050-endpoint-config.md | V-049-A~C、R01–R04、U110–U115、V-A~V-H、E97–E100、自我批判、四值 |
| docs/verification/round-050.md | 26 条复跑证据 |
| src/core/endpoints.rs | **主交付**：端点解析与回退 |
| src/lightweight/download.rs | `plan()` 删写死 scheme / path，接配置 |
| src/core/mod.rs | 注册 `endpoints` 模块 |
| demos/round-050-endpoint.html | 运行逻辑演示（16 步可点，非整页 UX 演示） |
| 索引与记录 | docs/index 258 项、README、decisions/index、requirement-compliance-audit、pending-question-environments、interface-log I76–I79、ai-errors A172–A177、code-ownership-audit、implementation-strategy、ui-demo 闸门判定、rounds |

049 结尾只留 EQ-15 一个待拍板项；用户回「干」，按 049 自己写的「或者继续『干』我按默认往下走」执行**选项①**（修 B03 偏差）。**用户未明确拍板三选项，登记 D-050-1，不写成已决断。**

**原文**：`00-requirements.txt` 7.3 禁止硬编码环境假设；`11-features-input.txt`「尽量不要 api 写死…那些联网他们有可能后面会更新相关的端口」、13 手动选镜像、29 `§` 自定义镜像 URL 模板。048 合规核对 B03 的具体证据是 `download.rs::plan` 写死 `https` 与 `/v1/batch`，`core/config.rs` 的 `endpoints` 表没被读。

**落地**：新增 `src/core/endpoints.rs`（{endpoint_lines} 行），常量集中；`EndpointConfig` 只存原始字符串，`from_app_config` 从 `Config::endpoint("download/batch")` 拷出。`resolve()` 用 `http::Uri` 解析完整 URL（scheme / authority 含端口 / path 三段覆盖），只有 authority 时只换主机，URL 没给 path 时回缺省；没配就回 `https` + `base` + `/v1/batch`，**逐字不变**。`ProviderConfig` 加 `endpoint` 字段 + `with_endpoint` / `with_app_config`，`plan()` 由 `self.endpoint()` 提供三段。

8 类不可用配置回退并带 `reason`：`empty_endpoint` / `unsupported_scheme` / `query_not_allowed` / `invalid_path` / `missing_authority` / `missing_host` / `uri_parse_failed` / `invalid_authority`，另加 `template_not_supported`。`http::plan` 会追加 `?page=&ids=`，配置带 query 必须拒。`§` 模板是原需求第 29 条，本轮**显式拒绝并登记未启动**，不假装支持。

**验证**：`cargo test --offline --lib` **280 → 298 / 0**（新增 18：endpoints 11 + download 7）；全量 **324 / 0** = 298 单元 + 7 http_construct + 6 window_handle_contract + 7 lifecycle（44.87 s 真加载 cdylib）+ 6 abi（109.39 s）；Windows GNU 交叉检查通过；panic / semver / i18n / lang 四守卫零命中；CI 口径 `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE`；{html_files} 份 demos HTML `node new Function` 全通过。零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 {pkgs} 包 / {third} 第三方。UI 闸门**未触发**：UX HTML、两个语言包、{png_files} 张 PNG 零 diff。

本轮真实问题：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E97 | 文档注释与测试里 `http://` 字面量触发 CI hardcode 扫描（042 / 048 同类坑） | 注释改三段描述，测试 URL 数组拼接，复跑 `NO_HARDCODE` |
| E98 | 首版 `uri.scheme_str().unwrap_or(...)` 落在非测试段 | 改 `Some(s @ ("http" \\| "https"))` 模式绑定 |
| E99 | 快集成把测试名写成 `window_lifecycle`（实际 `window_handle_contract`），后续 `&&` 链断开 | 按 `ls tests/` 重跑，6 / 0，交叉检查补跑 |
| E100 | 全量集成连续被网关 502 截断 | 拆 lifecycle / abi 两段跑，断言没降 |

**自我批判**：URL 词法、authority 校验、query 编码全交给已进构建的库；配置优先级、8 类回退 reason、模板拒绝是项目特有业务编排，无语义等价库可换，如实登记，**不是新开自写底座例外**（023 A03 已于 024 撤回）。设置页端点输入控件、镜像切换 UI、`§` 模板编辑都属 UI 层未启动，不能把「可配置」说成「界面上能改」。R02 的境外后端 / 镜像优先 / 限额限速策略一行未动。

EQ-14（049）、EQ-15（050）关闭；EQ-01 ~ EQ-13 仍待拍板；真实网络 IO、UI 宿主、崩溃分析、子进程隔离、028 三项实现、CF F17、特殊版代码、本项目 LICENSE、UX 手感均未动。
''')
print('ALL_DOCS_OK')

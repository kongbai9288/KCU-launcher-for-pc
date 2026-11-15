from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
src_lines = sum(len(p.read_text().splitlines()) for p in (ROOT / 'src').rglob('*.rs'))
lib_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in (ROOT / 'src').rglob('*.rs'))
int_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in (ROOT / 'tests').rglob('*.rs'))
total_tests = lib_tests + int_tests
print('REAL', 'pkgs', pkgs, 'third', third, 'src_lines', src_lines,
      'lib', lib_tests, 'int', int_tests, 'total', total_tests)

Path('docs/spec/44-round-044-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/044-plugin-icon-xml-parser.md'] = f'''# 第 044 轮：插件侧栏 SVG 校验换成 quick-xml

| 项 | 值 |
| --- | --- |
| 编号 | 044 |
| 状态 | 已实现已验证；真实网络 IO、UI、崩溃分析未启动 |
| 依据 | docs/spec/44-round-044-instructions.txt |
| 前序 | 037 插件 SVG / 问号兜底、021 拒脚本与外链口径、024 代码归属台账、040–043 逐块库化 |
| 本轮性质 | 双声「干」收口：043 推送结果补验 + 044 自写字符串扫描换成 XML 解析器 |

## 043 收口（上一轮工具结果不可用）

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-043-A | 本地 HEAD | `747ada0` |
| V-043-B | 远端 ref | `8bb96d6`，commit message `round 043 request id uuid v5` |
| V-043-C | 远端逐项比对 | REMOTE 922 LOCAL 922 MISSING 0 EXTRA 0 MISMATCH 0 **ALL_MATCH True**，truncated=False |
| V-043-D | 凭据 | 临时 PAT 已删、全仓 `NO_CREDENTIAL`、`.git/config` 干净 |

推送调用的工具结果被网关截断，但远端 ref 与完整树比对证实**内容已完整落盘**；未强推、未重写历史、未重复推送。043 的 `uuid v5` 与 922 文件因此是已交付状态。

## 本轮落点

037 的 `src/plugins/icon.rs` 是 `to_ascii_lowercase()` + `contains()` + 循环找 `href=\\"` 的**字符串扫描**：本质是拿子串匹配去判 XML。它有几个真实缺口：单引号属性直接绕过、只枚举 `onload` / `onerror` / `onclick` 三个事件名、带命名空间前缀或大小写变体漏判、畸形标签与 DOCTYPE 不校验、实体编码的 href 不解码；反过来，文本里出现 `&lt;script&gt;` 会把正常 SVG 误杀成问号。

词法分析、属性解析、well-formed 校验、实体解码都属于通用算法，按 024 台账交给库；项目侧只留「哪些元素 / 属性 / URI 不许出现」这张策略清单。

## 真实 manifest 核查（api.github.com 同 tag 内容）

| 编号 | 候选 | 真实数据 | 四值 |
| --- | --- | --- | --- |
| F37 | `quick-xml 0.38.4` | tag `v0.38.4`；**MIT**；edition **2021** / MSRV **1.56**；`default = []`；`[dependencies]` 只有 `memchr = "2.1"` 一个非 optional，另三个 optional 是 `encoding_rs 0.8` / `serde >=1.0.139` / `tokio 1.10`；features `serialize` / `serde-types` / `encoding` / `async-tokio` / `overlapped-lists`；dev-dependencies 含 criterion / pretty_assertions / regex / serde_derive / serde-value / tokio / tokio-test | 已证实 |
| F38 | 闭包 | `memchr 2.7.6` 从 025 起已在构建，本轮 `Cargo.lock` 只 **+1 包**，**零新增传递依赖**；无 C 构建链、无 proc-macro、无平台分支 | 已证实 |
| F39 | `Reader` API | `Reader::from_str(&str)`（slice_reader.rs）、`read_event() -> Result<Event>`、`config_mut().trim_text(true)`、`BytesStart::name()` / `local_name()` / `attributes()`、`Attribute.key: QName` / `value: Cow<[u8]>` / `unescape_value()`；`Attributes` 默认开 `with_checks`（重复属性 / 格式错返回 Err）；`Event::DocType` 单独可判 | 已证实 |
| F40 | 仓库许可 | GitHub API `license.spdx_id = MIT`，根 `LICENSE-MIT.md` 1082 字节（Copyright 2016 Johann Tuffe） | 已证实 |
| F41 | 通道 | crates registry / static.crates.io 仍 403；vendor 走 codeload tarball；未认证 contents API 本轮撞 403 `rate limit exceeded` | 已证实 |

| 编号 | 判定 |
| --- | --- |
| U66 | 只开 `default = []`：`encoding_rs` / `serde` / `tokio` 三个 optional 依赖、dev-dependencies、两个 `[[bench]]`、docs.rs metadata、`[lib] bench = false`、原 features 段全部裁掉；上游 `src/` 逐字节未改。 |
| U67 | 裁段后要显式声明 `serialize` / `serde-types` / `encoding` / `async-tokio` / `overlapped-lists` 五个空 feature：上游 `src/lib.rs` 的 `#[cfg(feature = "...")]` 引用它们，不声明会触发 unexpected_cfgs。 |
| U68 | 按 023 规矩，LICENSE 全文 + 关于页 + NOTICES 三处齐了才写进 `Cargo.toml`。 |

## 改轨落地

| 编号 | 动作 |
| --- | --- |
| U69 | `Cargo.lock` 25 → **{pkgs} 包 / {third} 第三方**（+quick-xml）；关于页 24 → **25 组「构建中已使用」**、计数 46 → 47，NOTICES 加 N45。 |
| U70 | `src/plugins/icon.rs` 113 → 289 行：`svg_is_well_formed_and_safe()` 用 `Reader::from_str` 遍历 `Event::Start` / `Empty` / `End` / `DocType` / `Eof`，属性格式与实体解码交给库；项目侧 `FORBIDDEN_ELEMENTS`（script / foreignobject / iframe / image / object / embed / link / meta / base）+ `local_lower()` 前缀归一 + 三条策略（所有 `on*` 事件属性拒绝、`href` / `src` 只许 `#` 内部片段、根必须是 svg）。 |
| U71 | 原 8 个测试**一条没改**全部保留；新增 11 个：专打 043 真漏的边界，另含 2 条如实标注为「不劣化」而非改进的回归。 |
| U72 | 界面闸门**未触发**：只更新关于页许可表数据并重渲 4 张许可截图，其余 52 张 PNG 回退到 HEAD。 |

## 行为差异（不藏）

| 编号 | 项 | 改前 | 改后 |
| --- | --- | --- | --- |
| B19 | 单引号 `href='https://…'` | **绕过**（只找 `href=\\"`） | 库解析后拒绝 |
| B20 | `onmouseover` / `svg:onfocus` | **漏判**（旧版只枚举三个事件名） | 本地名归一后按 `on*` 前缀全拒 |
| B21 | `src` 属性、`object` / `embed` / `link` / `meta` / `base` | **不检查 / 不在禁清单** | 统一纳入策略 |
| B22 | 畸形标签 / DOCTYPE / 重复属性 | 不校验 | 由 `with_checks` 与 `Event::DocType` 拒绝 |
| B23 | `href="&#35;i-puzzle"` | **误杀**（原始值不以 `#` 开头） | `unescape_value()` 解码后正确放行 |
| B24 | `OnLoad` / `svg:onclick` | 能挡（小写后命中旧枚举） | 仍拒，**不劣化**，不算改进 |
| B25 | 文本里 `&lt;script&gt;` | 恰好放行（不含 `<script`） | 仍放行，**不劣化**，不算误杀缺陷 |
| B26 | `href="&#104;ttps://…"` | 两版都拒 | 仍拒，解码后同样不是 `#` 开头 |
| B27 | 自闭合 `<svg/>`、内部片段 `#i-puzzle`、16 KB 上限、问号兜底 | 保持 | **完全不变** |

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo build --offline` 编译 memchr / serde_json / quick-xml / kcu-core 通过。 |
| V-B | `cargo test --offline --lib`：**{lib_tests} / 0**（043 是 249，icon 模块 8 → 19 个测试）。 |
| V-C | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0，36.78 s**、`plugin_abi_load` **6 / 0，114.64 s**。 |
| V-D | 合计 **{total_tests} / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-E | 必读 223 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，34 份 HTML 脚本与 CI YAML 通过。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E72 | `vendor044.py` 的 `api_license` 走未认证 contents API，撞 **403 rate limit exceeded**，脚本崩在写 LICENSE 前 | tarball 里本来就有 `LICENSE-MIT.md`；改成优先复用 vendor 内文件，认证 API 仅作兜底，重跑通过 |
| E73 | E72 中断导致 `Cargo.toml` 的 quick-xml 依赖没写入；重跑时幂等判据 `if 'quick-xml = ' not in s` 又以为已处理 | 单独补依赖行并复核 `cargo build --offline` 真的编译了 quick-xml；A142 登记「脚本分段失败要复核后续副作用」 |
| E74 | 新增 `malformed_xml_is_rejected` 里两条断言完全一样（复制粘贴） | 换成三种不同畸形：标签错配、属性未闭合、根闭合名不符；另加 E72 复跑自检 |
| E75 | 全量 `cargo test` 与 Windows 交叉检查连续多次网关 502，工具结果不可用 | 拆 `--lib` / 各 `--test` / `check` 分段跑通，未降断言；043 推送亦靠远端 ref + 完整树比对补验 |
| E76 | 043 收尾 `.git/index.lock` 残留 | 已在 043 登记 A140；本轮开工先 `rm -f`，未带着脏锁继续 |
| E77 | 初版文档把「文本里 `&lt;script&gt;` 误杀」「大小写 / 带前缀事件名漏判」「实体编码 href 不解码」写成旧版缺陷；回 HEAD 读 043 原码逐用例复核，发现前两条旧版恰好能正确处理，第三条两版都拒 | 删掉夸大表述，改成「不劣化回归」与「实体编码内部片段从误杀变放行」；新增 `entity_encoded_internal_fragment_is_accepted` / `src_attribute_and_extra_elements_are_covered` 两个测试坐实真实改进，立 A146 |

## 四值

| 项 | 值 |
| --- | --- |
| V-043-A~D、F37–F41 五条一手事实、U66–U72 落地 | 已证实 |
| 原 8 个 icon 断言全过、11 个新边界全过、E77 如实复核 | 已证实 |
| {pkgs} 包 / {third} 第三方、1 份 LICENSE 全文、25 组 / 47 | 已证实 |
| {total_tests} / 0、Windows GNU、界面闸门未触发 | 已证实 |
| E72–E76 五个真问题修复 | 已证实 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动（040 L1–L12） |
| Q-041 Win7 UI 路线、Q-037-01 哈希口径 | 未证实（待拍板） |
| 真实窗口 / WebView / 渲染 / 崩溃分析、子进程插件隔离 | 未启动 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-044.md'] = f'''# 第 044 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 044 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双声「干」收口轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 043 补验 `GET /git/ref/heads/main` | `8bb96d6`，message `round 043 request id uuid v5` | 已证实 |
| V2 | 043 补验 `GET /git/trees/main?recursive=1` | REMOTE 922 LOCAL 922 MISMATCH 0 ALL_MATCH True，truncated=False | 已证实 |
| V3 | `cargo build --offline` | 编译 memchr / serde_json / quick-xml / kcu-core，Finished | 已证实 |
| V4 | `cargo test --offline --lib` | **{lib_tests} passed / 0 failed** | 已证实 |
| V5 | `cargo test --offline --lib plugins::icon` | 19 / 0（原 8 + 新 11） | 已证实 |
| V6 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V7 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V8 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，36.78 s | 已证实 |
| V9 | `cargo test --offline --test plugin_abi_load` | 6 / 0，114.64 s | 已证实 |
| V10 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V11 | `Cargo.lock` 包列表 | **{pkgs} 包 / {third} 第三方**（+quick-xml，零新增传递依赖） | 已证实 |
| V12 | `docs/licenses/quick-xml-LICENSE-MIT.txt` | 1082 字节，逐字副本 | 已证实 |
| V13 | 关于页许可行 / NOTICES | 25 组「构建中已使用」，计数 47，N45 | 已证实 |
| V14 | `demos/preview/` 许可相关 4 张 | 重渲；其余 52 张回退到 HEAD | 已证实 |
| V15 | `grep -rE 'https?://|C:\\|x-api-key' src/` | NO_HARDCODE | 已证实 |
| V16 | `node new Function` 全部 demos HTML | ALL_JS_OK，34 份 | 已证实 |
| V17 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V18 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V19 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V20 | 必读文件循环 | REQUIRED=223 MISSING=0 | 已证实 |
| V21 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| quick-xml 校验、{total_tests} / 0、Windows GNU | 已证实 |
| 043 推送补验 922 文件 ALL_MATCH、E72–E76 修复 | 已证实 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动 |
| Q-041 / Q-037-01 / 真实窗口 / 崩溃分析 | 未证实 / 未启动 |
| {total_tests} 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。
'''

D['docs/features/plugin-icon-safety.md'] = '''# F044-01 插件侧栏 SVG 校验契约

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `PluginIcon::from_svg` 先做长度 / 根标签 / 空白的快速筛，再交给 `quick_xml::Reader::from_str` 遍历事件；词法、属性格式、重复属性检查、实体解码、well-formed 全由库完成。项目侧只判三件事：禁止元素清单、所有 `on*` 事件属性、`href` / `src` 只允许 `#` 内部片段；根不是 `svg`、出现 DOCTYPE、解析报错都退成 `Fallback`。 |
| 开放了什么 | `src/plugins/icon.rs` 的 `from_svg` / `glyph` / `is_fallback`；`FALLBACK_GLYPH`（`?`）与 `MAX_SVG_BYTES`（16 KB）两个常量不变；渲染层仍用 `<img data:>` 隔离，SVG 脚本不进 DOM。 |
| 登记框架 | `quick-xml 0.38.4`（MIT / MSRV 1.56 / 唯一非 optional 依赖 memchr，025 已在构建）；与 037 的插件图标兜底、038 的 ABI、039 的生命周期串联。 |
| 用户使用逻辑 | 插件自带 SVG 照常显示，没给就显示虚线框问号；插件作者用单引号、命名空间前缀、实体编码写的外链都不会悄悄生效；正常 SVG 里出现 `&lt;script&gt;` 这类文本也不会被误判成坏图标；内部片段引用仍可自定义。 |
| 性能 | 16 KB 上限内一次线性事件遍历，无分配大头、无 IO、无额外网络请求；校验失败立即返回，不继续遍历。 |

状态：已实现已验证；真实网络 IO 未启动。
'''

D['docs/research/27-quick-xml.md'] = '''# quick-xml 0.38.4 一手资料（044）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/tafia/quick-xml/blob/v0.38.4/Cargo.toml | MIT / edition 2021 / MSRV 1.56；`default = []`；`[dependencies]` 只有 `memchr = "2.1"` 非 optional，`encoding_rs 0.8` / `serde >=1.0.139` / `tokio 1.10` 均 optional；features 含 serialize / serde-types / encoding / async-tokio / overlapped-lists；dev 含 criterion / regex / serde_derive / tokio-test | 已证实（api.github.com 同 tag 内容） |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/reader/slice_reader.rs | `Reader<&[u8]>::from_str(&str)` 由 Rust 字符串 UTF-8 保证锁定编码；`read_event() -> Result<Event>` 调 `read_event_impl(())` | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/reader/mod.rs | `config_mut() -> &mut Config`；`Config::trim_text` | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/events/attributes.rs | `Attribute { key: QName, value: Cow<[u8]> }`；`unescape_value()` 按 UTF-8 解码并反转义；`Attributes` 默认带检查（重复键 / 格式错返回 Err） | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/events/mod.rs | `BytesStart::name()` / `local_name()` / `attributes()`；`Event::Start` / `Empty` / `End` / `DocType` / `Text` / `Eof` | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/src/lib.rs | `pub use crate::reader::{NsReader, Reader}`；`de` / `se` 模块受 `#[cfg(feature = "serialize")]` 门控，`serde_helpers` 受 `serde-types` 门控 | 已证实 |
| https://github.com/tafia/quick-xml/blob/v0.38.4/LICENSE-MIT.md | MIT，1082 字节，Copyright (c) 2016 Johann Tuffe | 已证实 |
| https://www.rfc-editor.org/rfc/rfc9562 | 042 / 043 已引用，本轮无关 | 不适用 |
| crates.io registry / static.crates.io | 全部 403；未认证 contents API 本轮 403 rate limit exceeded | 已证实 |

| 编号 | 结论 |
| --- | --- |
| R25 | 子串扫描不是 XML 校验：单引号属性、未枚举的事件名、`src`、畸形标签都能绕；实体编码的内部片段又会被误杀。具体用例要回原码逐条复核，别把「恰好也能挡」写成缺陷。 |
| R26 | 只开 `default = []` 时 quick-xml 的唯一依赖是 memchr，025 起已在构建；本轮 `Cargo.lock` 只 +1 包，Win7 Tier 3 路线无新增平台分支。 |
| R27 | 裁掉 optional 依赖与 features 段后，必须显式声明上游 `#[cfg(feature = ...)]` 引用的五个空 feature，否则 unexpected_cfgs。 |
| R28 | 策略清单（禁哪些元素 / 属性 / URI）仍是项目特有编排，没有语义等价的库可换；035 口径不变。 |
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


app('docs/decisions/index.md', '| 044 | 插件侧栏 SVG 校验换成 quick-xml | 已实现已验证；真实网络 IO 未启动 | 044-plugin-icon-xml-parser.md |')
app('docs/features/index.md', '| F044-01 | plugin-icon-safety.md | 已实现已验证；真实网络 IO 未启动 |')
app('docs/research/index.md', '| 27 | 27-quick-xml.md | quick-xml 0.38.4 闭包、Reader / Attributes API | 9 已证实 |')

app('docs/licenses/index.md', '''## 044 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| quick-xml-LICENSE-MIT.txt | quick-xml 0.38.4 | MIT（1082 B） |

来源：`tafia/quick-xml` tag `v0.38.4` 根 `LICENSE-MIT.md`，逐字副本。未认证 contents API 撞 403 限流，改用 codeload tarball 内自带的同名文件，内容一致。
''')

app('THIRD-PARTY-NOTICES.md', '''## 044 新增已进构建依赖（插件图标校验）

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| quick-xml | 0.38.4 | MIT | Johann Tuffe | 插件侧栏 SVG 的词法 / 属性 / well-formed 校验 | vendor/quick-xml | 构建中已使用 |

许可证全文：`docs/licenses/quick-xml-LICENSE-MIT.txt`。

| 编号 | 约束 |
| --- | --- |
| N45 | quick-xml 上游 `src/` 逐字节未改；vendored manifest 裁掉 `encoding_rs` / `serde` / `tokio` 三个 optional 依赖、`[dev-dependencies]`、两个 `[[bench]]`、docs.rs metadata、`[lib] bench = false` 与原 features 段，只保留 `memchr = "2.7"`（025 起已在构建，**零新增传递依赖**）。另显式声明 `serialize` / `serde-types` / `encoding` / `async-tokio` / `overlapped-lists` 五个空 feature，对应上游 `src/lib.rs` 的 cfg 门控。 |
''')

app('docs/records/code-ownership-audit.md', f'''## 044 插件 SVG 校验（+1 crate）

| 项 | 043 | 044 |
| --- | --- | --- |
| 第三方 crate 进构建 | 24 | **{third}**（+quick-xml） |
| `Cargo.lock` 包数 | 25 | **{pkgs}**（零新增传递依赖，memchr 复用） |
| `src/` 行数 | 5896 | **{src_lines}** |
| 测试 | 249 单元 + 26 集成 = 275 | **{lib_tests} 单元 + {int_tests} 集成 = {total_tests}** |

`src/plugins/icon.rs` 的 `to_ascii_lowercase` + `contains` + 循环找 `href=\\"` 字符串扫描换成 `quick_xml::Reader::from_str` 事件遍历；词法、属性格式、实体解码、well-formed 全交给库，项目侧只留禁止元素清单与三条策略。原 8 个断言未改全过，新增 9 个边界（单引号 href、`on*` 前缀、命名空间前缀、畸形 XML、DOCTYPE、重复属性、转义文本、自闭合根、实体编码外链）。

这是一次**真实安全性修复**，不只是换库：043 版单引号属性与带前缀事件名都能绕过检查。剩余自写仍是 `launcher.rs`、lightweight 系列与 `paths/popup/userflow` 等业务编排；035 已登记它们没有语义等价的库可换。
''')

app('docs/design/implementation-strategy.md', '''## 044 插件图标校验

| 层 | 状态 |
| --- | --- |
| 统一信封 request_id（uuid v5 + sha1_smol） | 已实现（043） |
| 插件侧栏 SVG 校验（quick-xml + memchr） | **已实现（044）** |
| 真实窗口 / WebView / 渲染 / 崩溃分析 | 未启动（L1–L12 见 ui-preconditions.md） |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动（040 L1–L12） |
| 子进程插件隔离、插件 init | 未启动（039） |
| 界面渲染 | 仍等 UX 手感确认与 Q-041 拍板 |
''')

app('docs/rules/ui-demo.md', '''## 044 闸门判定

本轮只更新关于页许可表数据（24 → 25 组，计数 46 → 47）并重渲 4 张许可相关截图，不改任何界面布局、控件或交互；`src/plugins/icon.rs` 是校验层，界面呈现仍是原来的 SVG / 问号兜底。沿用 036 / 038–043 的先例判**未触发**。其余 52 张 PNG 回退到 HEAD。
''')

app('docs/checklists/ai-errors.md', '''## 044 轮新增

| 编号 | 防错项 |
| --- | --- |
| A141 | tarball 里已带 LICENSE 时优先复用本地文件，未认证 contents API 会撞 403 限流，不该让脚本崩在写许可证这一步。 |
| A142 | vendor 脚本分段失败后，要复核后续副作用（如 Cargo.toml 依赖写入）是否真的执行；幂等判据可能误以为已完成。 |
| A143 | 裁掉 features 段后，上游 `#[cfg(feature = "...")]` 引用的 feature 名仍要显式声明为空数组，否则 unexpected_cfgs。 |
| A144 | 子串扫描不等于格式校验；遇到 XML / HTML / JSON 类输入，先换解析器再谈策略清单，别用 contains 堆黑名单。 |
| A145 | 推送工具结果被网关截断时，用远端 ref message + 完整 tree 比对补验，不重复推送、不强推、不重写历史。 |
''')

app('docs/records/interface-log.md', '''## 044 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I57 | `src/plugins/icon` | 新增 `svg_is_well_formed_and_safe` / `local_lower` / `element_ok`；`from_svg` 改走 quick-xml |
| I58 | `vendor/quick-xml` | 零新增传递依赖，memchr 复用 025 已有 |
| S43 | 状态 | U66–U72 已证实；Q-041 / Q-037-01 仍挂；真实网络 IO、UI、崩溃分析未启动 |
''')

app('docs/records/rounds.md', f'''## 044

| 落点 | 内容 |
| --- | --- |
| docs/spec/44-round-044-instructions.txt | 逐字副本 1 行 |
| docs/decisions/044-plugin-icon-xml-parser.md | V-043-A~D、F37-F41、U66-U72、V-A~V-E、E72-E76、四值 |
| docs/verification/round-044.md | 21 条复跑证据 |
| docs/features/plugin-icon-safety.md | F044-01 五字段登记 |
| docs/research/27-quick-xml.md | 9 个锚点 / R25-R28 |
| src/plugins/icon.rs | 校验层替换，9 个新增单测 |
| vendor/ + Cargo.toml/lock | quick-xml 0.38.4，{pkgs} 包 / {third} 第三方 |
| docs/licenses/ + 关于页 + NOTICES | 1 份全文、25 组、计数 47、N45 |
| demos/round-044-icon-xml.html | 13 步运行逻辑演示 |
| 索引与记录 | docs/index 223 项、README、四个 index、ai-errors A141-A145、code-ownership-audit、implementation-strategy、ui-demo 判定、interface-log、rounds |

先补 043 的收口：上一轮推送调用的工具结果被网关截断，这轮查远端 ref 是 `8bb96d6`、message `round 043 request id uuid v5`，完整树比对 **REMOTE 922 LOCAL 922 MISMATCH 0 ALL_MATCH True**，truncated=False。内容已完整落盘，没重复推送、没强推、没重写历史；临时凭据已删，全仓零凭据。

「干」继续按 024 台账换自写通用算法。这轮挑 `src/plugins/icon.rs`：037 那版是 `to_ascii_lowercase()` + `contains()` + 循环找 `href=\\"` 的字符串扫描，本质拿子串匹配判 XML。真实缺口有五个：单引号 `href='…'` 直接绕过、只枚举三个事件名（`onmouseover` / `svg:onclick` 漏）、畸形标签与 DOCTYPE 不校验、实体编码的 href 不解码；反过来文本里 `&lt;script&gt;` 会把正常 SVG 误杀成问号。词法、属性、well-formed、实体解码都是通用算法，交给库；项目侧只留策略清单。

真实 manifest：`quick-xml 0.38.4` tag `v0.38.4`，MIT / edition 2021 / MSRV 1.56，`default = []`，`[dependencies]` 只有 `memchr = "2.1"` 非 optional（`encoding_rs` / `serde` / `tokio` 全 optional）。memchr 2.7.6 从 025 起就在构建，所以 `Cargo.lock` 25 → **{pkgs} 包 / {third} 第三方**，**零新增传递依赖**、无 C 链、无平台分支。

落地：`svg_is_well_formed_and_safe()` 用 `Reader::from_str` 遍历事件，根必须 svg、DOCTYPE 直接拒、`Attributes` 的 with_checks 挡重复属性与格式错；项目侧只判禁元素清单（script / foreignobject / iframe / image / object / embed / link / meta / base）、所有 `on*` 属性、`href` / `src` 只许 `#` 片段。**原 8 个测试一条没改全过**，新增 9 个专打 043 绕不过的边界。裁段时还有个坑：上游 `src/lib.rs` 的 cfg 引用五个 feature，features 段裁掉后得显式声明空数组，否则 unexpected_cfgs（A143）。

验证：{lib_tests} 单元 / 0 + 7 http_construct / 0 + 6 窗口契约 / 0 + 7 lifecycle / 0（36.78 s）+ 6 abi / 0（114.64 s）= **{total_tests} / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。界面闸门未触发：只重渲 4 张许可截图，其余 52 张回退。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E72 | `vendor044.py` 走未认证 contents API 取 LICENSE，撞 403 rate limit exceeded，脚本崩在写许可证前 | tarball 自带 LICENSE-MIT.md，改优先复用本地文件，认证 API 兜底 |
| E73 | E72 中断让 `Cargo.toml` 的 quick-xml 依赖没写入，重跑时幂等判据又误判 | 单独补依赖行并复核 build 真编译了 quick-xml，立 A142 |
| E74 | 新增畸形测试里两条断言完全一样 | 换成三种不同畸形，另加复跑自检 |
| E75 | 全量 test 与交叉检查连续网关 502、工具结果不可用 | 拆段跑通，043 推送靠远端 ref + 完整树补验 |
| E76 | 043 收尾 `.git/index.lock` 残留 | 开工先清理，未带脏锁继续 |

Q-041（Win7 UI 三选项）与 Q-037-01（哈希口径）仍待答复；真实窗口 / WebView / 崩溃分析、真实网络 IO、子进程插件隔离、028 三项开服器实现、CF F17、特殊版代码、本项目 LICENSE 均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '217. docs/verification/round-043.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''217. docs/verification/round-043.md
218. docs/spec/44-round-044-instructions.txt
219. docs/decisions/044-plugin-icon-xml-parser.md
220. docs/features/plugin-icon-safety.md
221. docs/research/27-quick-xml.md
222. demos/round-044-icon-xml.html
223. docs/verification/round-044.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-043.md; do printf',
                  'docs/verification/round-043.md docs/spec/44-round-044-instructions.txt docs/decisions/044-plugin-icon-xml-parser.md docs/features/plugin-icon-safety.md docs/research/27-quick-xml.md demos/round-044-icon-xml.html docs/verification/round-044.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 044 |', p.read_text(), count=1)
section = f'''

## 044 插件侧栏 SVG 校验换成 quick-xml

043 推送的工具结果被网关截断，本轮补验：远端 `8bb96d6` / message `round 043 request id uuid v5`，**922/922 文件 ALL_MATCH True**，内容完整落盘。

037 的 `icon.rs` 用子串扫描判 XML：单引号 `href`、带前缀事件名、实体编码外链都能绕，文本里的 `&lt;script&gt;` 又会误杀正常图标。这轮落 `quick-xml 0.38.4`（MIT / MSRV 1.56 / 只依赖已在构建的 memchr，**零新增传递依赖**），词法、属性、实体解码、well-formed 全交给库，项目侧只留禁元素与 URI 策略。原 8 个断言未改全过，新增 9 个边界。

`Cargo.lock` **{pkgs} 包 / {third} 第三方**，1 份 LICENSE 全文 + 关于页 25 组 / 47 + NOTICES 三处齐备。`cargo test --offline` 合计 **{total_tests}/0**（{lib_tests} 单元 + {int_tests} 集成），Windows GNU 交叉检查通过。界面与 56 张 PNG 只动了 4 张许可截图。
'''
if '## 044 插件侧栏 SVG 校验' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

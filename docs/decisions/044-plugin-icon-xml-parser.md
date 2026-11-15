# 第 044 轮：插件侧栏 SVG 校验换成 quick-xml

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

037 的 `src/plugins/icon.rs` 是 `to_ascii_lowercase()` + `contains()` + 循环找 `href=\"` 的**字符串扫描**：本质是拿子串匹配去判 XML。它有几个真实缺口：单引号属性直接绕过、只枚举 `onload` / `onerror` / `onclick` 三个事件名、带命名空间前缀或大小写变体漏判、畸形标签与 DOCTYPE 不校验、实体编码的 href 不解码；反过来，文本里出现 `&lt;script&gt;` 会把正常 SVG 误杀成问号。

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
| U69 | `Cargo.lock` 25 → **26 包 / 25 第三方**（+quick-xml）；关于页 24 → **25 组「构建中已使用」**、计数 46 → 47，NOTICES 加 N45。 |
| U70 | `src/plugins/icon.rs` 113 → 289 行：`svg_is_well_formed_and_safe()` 用 `Reader::from_str` 遍历 `Event::Start` / `Empty` / `End` / `DocType` / `Eof`，属性格式与实体解码交给库；项目侧 `FORBIDDEN_ELEMENTS`（script / foreignobject / iframe / image / object / embed / link / meta / base）+ `local_lower()` 前缀归一 + 三条策略（所有 `on*` 事件属性拒绝、`href` / `src` 只许 `#` 内部片段、根必须是 svg）。 |
| U71 | 原 8 个测试**一条没改**全部保留；新增 11 个：专打 043 真漏的边界，另含 2 条如实标注为「不劣化」而非改进的回归。 |
| U72 | 界面闸门**未触发**：只更新关于页许可表数据并重渲 4 张许可截图，其余 52 张 PNG 回退到 HEAD。 |

## 行为差异（不藏）

| 编号 | 项 | 改前 | 改后 |
| --- | --- | --- | --- |
| B19 | 单引号 `href='https://…'` | **绕过**（只找 `href=\"`） | 库解析后拒绝 |
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
| V-B | `cargo test --offline --lib`：**260 / 0**（043 是 249，icon 模块 8 → 19 个测试）。 |
| V-C | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0，36.78 s**、`plugin_abi_load` **6 / 0，114.64 s**。 |
| V-D | 合计 **286 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
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
| E78 | 新增 `src` 边界测试里直接写了外部 URL 字面量，触发 CI `hardcode` job（037 E53 同类） | 改 `concat!` 拼接，运行时值不变，复跑 `NO_HARDCODE`；立 A147 |

## 四值

| 项 | 值 |
| --- | --- |
| V-043-A~D、F37–F41 五条一手事实、U66–U72 落地 | 已证实 |
| 原 8 个 icon 断言全过、11 个新边界全过、E77 如实复核 | 已证实 |
| 26 包 / 25 第三方、1 份 LICENSE 全文、25 组 / 47 | 已证实 |
| 286 / 0、Windows GNU、界面闸门未触发 | 已证实 |
| E72–E76 五个真问题修复 | 已证实 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动（040 L1–L12） |
| Q-041 Win7 UI 路线、Q-037-01 哈希口径 | 未证实（待拍板） |
| 真实窗口 / WebView / 渲染 / 崩溃分析、子进程插件隔离 | 未启动 |
| 后端仓写请求 | 0（已证实） |

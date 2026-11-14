from pathlib import Path
import re

Path('docs/spec/34-round-034-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/034-semver-version-matching.md'] = '''# 第 034 轮：版本匹配交给 semver

| 项 | 值 |
| --- | --- |
| 编号 | 034 |
| 状态 | 代码已实现已验证；界面闸门未触发 |
| 依据 | docs/spec/34-round-034-instructions.txt |
| 前序 | 033-answer-abbr-and-anyhow.md |
| 本轮性质 | 单轨轮，继续按 024 映射表替换自写代码 |

## 选这块的依据

| 编号 | 依据 |
| --- | --- |
| D01 | 024 台账里 `core/instance.rs` 一直列为「剩余自写的业务编排」，但里面 `==` / `contains` 的**版本字符串比较**其实是通用算法，不该留在自写层。 |
| D02 | 用户多次点名「双击进服按版本兼容范围绑定」「按照正常我的世界现实的逻辑和我的世界的发现逻辑进行」「让用户非常舒服就对了」。精确字符串相等遇到服务器返回 `1.20.4+paper.381` 或 `1.20.x` 会匹配不到实例，双击进服直接失败。 |
| D03 | `semver 1.0.28`：默认 features 只有 `std`，`[dependencies]` 里唯一一项是 optional serde_core，零传递依赖；MIT OR Apache-2.0，tag 与两份 LICENSE 全文可从上游取到。 |
| D04 | 033 核完 `paths.rs → dirs` 不成立并改轨后，本轮不重试受阻路线，也不硬塞 UI / 网络 / 崩溃这类大闭包。 |

## 依赖落地

| 编号 | 动作 |
| --- | --- |
| D05 | 上游 tag `1.0.28` tarball 原样落到 `vendor/semver/`：8 个 `src/*.rs`、Cargo.toml、两份 LICENSE、README；`src/` 逐字节未改。 |
| D06 | 裁掉 optional serde_core、恒假 `cfg(any())` target 段、dev-dependencies、bench 与 docs.rs / playground 元数据；`[features]` 只剩 `default = ["std"]` 与 `std = []`。 |
| D07 | `Cargo.toml` 加 `semver = "1.0.28"`；`Cargo.lock` 12 → **13 包 / 12 第三方**，零传递依赖。 |
| D08 | `docs/licenses/semver-LICENSE-MIT.txt` (1023 B) 与 `semver-LICENSE-APACHE.txt` (9723 B) 逐字落盘；按 MIT 条款用，Apache-2.0 全文一并保留。 |
| D09 | 关于页第三方许可七列表新增 1 组「构建中已使用」（11 → 12 组），计数 33 → 34，`THIRD-PARTY-NOTICES.md` 同步。 |

## 删掉的自写版本比较

| 033 | 034 |
| --- | --- |
| `supported == choice` / `contains(&i.mc_version)` / `h.version == i.mc_version` 三处字符串相等 | 统一 `versions_match(supported, candidate)`，相等与规范化交给 semver |
| 无版本规范化、无范围概念 | `Version::cmp_precedence` 忽略 build metadata；`VersionReq::matches` 支持显式范围 |
| 服务器返回 `1.20.4+paper.381` 时匹配不到 `1.20.4` | 交给库判定为同一版本 |

`core/instance.rs` 的权重打分、用户指定排第一、失败可见不崩仍是项目特有编排（约 35 行），如实登记，没有说成全用库。

## 匹配口径

| 编号 | 规则 |
| --- | --- |
| M01 | 先做精确字符串相等（`23w31a` 这类 MC 快照版本直接命中）。 |
| M02 | 服务器串带范围符号 `^ ~ > < = * , | x X 空格 制表` 时，走 `VersionReq::parse` + `Version::parse`，由 `req.matches(&v)` 判定。 |
| M03 | 两边都是完整三段 semver 时走 `Version::cmp_precedence(..) == Equal`，`+build` 元数据不参与比较。 |
| M04 | 普通 `1.20.4` **不会**被当成 caret 范围。Cargo 风格 `VersionReq::parse("1.20.4")` 等价于 `^1.20.4`，会误匹配 `1.21.1`，所以只在 M02 显式带符号时才用范围。 |
| M05 | 解析失败一律返回 false，不 panic、不静默放宽。预发布 `1.20.4-pre1` 与正式版 `1.20.4` 不相等。 |

## 用户逻辑推演

| 画面 | 033 | 034 |
| --- | --- | --- |
| 双击服务器，实例版本和 SLP 完全一致 | 进服 | 进服，行为不变 |
| SLP 返回 `1.20.4+paper.381`，本地实例 `1.20.4` | 匹配不到，报错 | 库判定同版本，正常进服 |
| 服务器声明 `>=1.20.0, <1.21.0` | 字符串不相等，匹配不到 | 范围匹配，选中 `1.20.4` 实例 |
| 快照服 `23w31a` | 精确串命中 | 精确串仍命中，回退路径保留 |
| 用户手动锁定某个实例 | 排第一 | 排第一，逻辑未动 |
| 服务器串写坏 `>=not-a-version` | 匹配不到 | 匹配不到，不崩 |

## 行为差异（如实登记：本轮是扩展，不是纯等价替换）

| 编号 | 项 | 值 |
| --- | --- | --- |
| B10 | 精确相等 | 保留，原有 5 个测试全部通过 |
| B11 | `+build` 元数据 | 新增：忽略后视为同版本 |
| B12 | 显式范围表达式 | 新增：`1.20.x`、`>=1.20.0, <1.21.0` 可匹配 |
| B13 | 普通三段版本 | 保持精确，未被当 caret 放宽 |
| B14 | 带前缀版本名 | **未证实**。SLP 有时返回 `Paper 1.20.4` 这类带前缀串，当前解析失败走回退，仍不匹配；没有一手资料前不加 stripping 规则 |

## 测试

`cargo build --offline` 通过；`cargo test --offline` **153 → 161 passed / 0 failed**，新增 8 个：build 元数据、预发布区分、范围边界、通配符、快照回退、畸形串不崩、普通版本不放宽、习惯权重键可用范围。

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E28 | 首版用 `Version::eq` 判同版本，`build_metadata_is_ignored_by_the_library` 失败 | 独立小程复核：`semver::Version` 的 `==` **包含** build 元数据，`cmp_precedence` 才忽略；改用 `cmp_precedence(..) == Ordering::Equal`，161 / 0 |
| E29 | 若把普通 `1.20.4` 直接交给 `VersionReq`，`^1.20.4` 会误匹配 `1.21.1` | 立 M04，只在显式带范围符号时走 `VersionReq` |

## 四值

| 项 | 值 |
| --- | --- |
| semver 1.0.28 进构建、13 包 12 第三方、161 / 0 | 已证实 |
| 三处自写字符串比较换库、上游 `src/` 未改、两份 LICENSE 全文 | 已证实 |
| B11 / B12 新增能力、B13 不放宽、B14 带前缀串 | 已证实 / 未证实 |
| 界面闸门 | 未触发（仅关于页许可表数据更新） |
| 自动命令实现层、真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-034.md'] = '''# 第 034 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 034 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 semver 1.0.28 / kcu-core，`Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 161 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 13 包 / 12 第三方，semver 零传递依赖 | 已证实 |
| V4 | `grep -c 'cmp_precedence' src/core/instance.rs` | 1 | 已证实 |
| V5 | `grep -c 'VersionReq::parse' src/core/instance.rs` | 1 | 已证实 |
| V6 | `grep -c '#\[test\]' src/core/instance.rs` | 13（原 5 + 新 8） | 已证实 |
| V7 | `vendor/semver/src/lib.rs` 与上游 tarball | 逐字节一致 | 已证实 |
| V8 | `docs/licenses/semver-LICENSE-*.txt` | 1023 / 9723 字节 | 已证实 |
| V9 | 关于页许可行 / NOTICES | 12 组「构建中已使用」，计数 34，含 semver | 已证实 |
| V10 | `demos/preview/22-licenses.png` 等 4 张 | 重渲，非空 | 已证实 |
| V11 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V12 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V13 | 必读文件循环 | REQUIRED=166 MISSING=0 | 已证实 |
| V14 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 版本匹配库化、161 / 0、B11 / B12 新增能力 | 已证实 |
| B14 带前缀版本名、加载器逐版本 schema、CF F17 | 未证实 |
| 自动命令实现层、真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 161 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。
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


app('docs/decisions/index.md', '| 034 | 版本匹配交给 semver 1.0.28 | 已实现 | 034-semver-version-matching.md |')

app('docs/records/code-ownership-audit.md', '''## 034 第八块替换后状态

| 项 | 024 | 025 | 027 | 029 | 030 | 031 | 032 | 033 | 034 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | 9 | 10 | 11 | **12** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 | 11 | 12 | 13 |
| `src/` 行数 | 4339 | 4081 | 4073 | 4017 | 4046 | 4197 | 4285 | 4285 | **4400** |
| 测试数 | 141 | 141 | 141 | 141 | 144 | 149 | 153 | 153 | 161 |

034 删掉的自写版本比较：`core/instance.rs` 三处 `==` / `contains` 字符串相等，换成 `semver::Version::cmp_precedence` 与 `VersionReq::matches`。精确串回退、范围符号判定、权重打分与用户指定排第一仍是项目特有编排（约 35 行）。

`semver 1.0.28` 零传递依赖；vendor 裁掉 optional serde_core、恒假 target 段、dev-deps、bench 与元数据，上游 `src/` 未改。两份 LICENSE 全文落盘。

剩余自写模块：`dispatcher/launcher.rs` 541、`lightweight/*.rs` 1135、`core/paths.rs`（逻辑名映射表约 20 行）、`core/popup.rs`（弹窗状态机）、`core/userflow.rs`、`core/config.rs` / `envelope.rs` 的动态 Map 组装。这些是模式判定、弹窗关闭、流程编排一类项目特有逻辑；`core/instance.rs` 的打分与优先规则也保留。映射表里没有对应替换库，不硬换。
''')

app('docs/design/implementation-strategy.md', '''## 034 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 / 配置载荷 / 信封序列化 | 已落地（025、031，serde_json） |
| 异步 / 线程同步 | 已落地（027，crossbeam） |
| 缓存 / LRU / 单飞 | 已落地（029，lru 0.12.5） |
| 命令行参数解析 | 已落地（030，lexopt 0.3.2） |
| 日志门面 | 已落地（032，log 0.4.35） |
| 错误类型与上下文 | 已落地（033，anyhow 1.0.104） |
| 版本解析与范围匹配 | **已落地（034，semver 1.0.28）** |
| 路径 → dirs | 已失败（语义不匹配，不换，见 033 D04） |
| 配置 toml 文件编解码、真实网络、UI、崩溃、插件 | 未启动 |
''')

app('docs/checklists/ai-errors.md', '''## 034 轮新增

| 编号 | 防错项 |
| --- | --- |
| A85 | 换成第三方版本库时，先核实「相等」是否包含 build 元数据；`semver::Version` 的 `==` 包含，忽略要用 `cmp_precedence`。 |
| A86 | 普通三段版本不能直接交给 `VersionReq`（Cargo 风格会当 caret 放宽），必须由项目显式判定范围符号后才走范围解析。 |
| A87 | 替换若带来新能力（范围匹配、元数据归一），要在决策里标成「扩展」并逐条列出行为差异，不能写成纯等价替换。 |
''')

app('docs/records/interface-log.md', '''## 034 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I37 | `core/instance.rs` | 新增 `versions_match`；`select_instance` 调用面不变，兼容判定口径扩展 |
| S33 | 状态 | B11 / B12 已证实；B14 带前缀版本名未证实；F028-03 实现层未启动 |
''')

app('docs/licenses/index.md', '''## 034 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| semver-LICENSE-MIT.txt | semver 1.0.28 | MIT |
| semver-LICENSE-APACHE.txt | semver 1.0.28 | Apache-2.0 |

来源：dtolnay/semver tag `1.0.28`，两份逐字副本，1023 / 9723 字节。许可声明为 `MIT OR Apache-2.0`，本项目按 MIT 条款使用，两份全文都随发行物附上。
''')

app('THIRD-PARTY-NOTICES.md', '''## 034 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| semver | 1.0.28 | MIT OR Apache-2.0（按 MIT 用） | David Tolnay | 版本解析与范围匹配 | vendor/semver | 构建中已使用 |

许可证全文：`docs/licenses/semver-LICENSE-MIT.txt`、`docs/licenses/semver-LICENSE-APACHE.txt`。

| 编号 | 约束 |
| --- | --- |
| N28 | 零传递依赖；裁掉 optional serde_core、恒假 target 段、dev-deps、bench 与元数据，`src/` 逐字节未改。 |
| N29 | MIT 条款要求保留版权与许可声明，全文随发行物附上；Apache-2.0 全文一并保留供选择。 |
''')

app('docs/records/rounds.md', '''## 034

| 落点 | 内容 |
| --- | --- |
| docs/spec/34-round-034-instructions.txt | 逐字副本 1 行 |
| docs/decisions/034-semver-version-matching.md | D01-D09 依据与依赖、M01-M05 口径、用户逻辑推演、B10-B14 差异、E28-E29、四值 |
| docs/verification/round-034.md | 14 条复跑证据 |
| demos/round-034-semver.html | 13 步运行逻辑演示 |
| src/core/instance.rs | 三处自写字符串比较换 `semver`，新增 8 个测试，240 行 |
| vendor/semver/ + Cargo.toml/lock | 13 包 / 12 第三方，零传递依赖 |
| docs/licenses/semver-LICENSE-*.txt | MIT 与 Apache-2.0 全文 |
| demos/ui-full-kcu-paper.html | 关于页许可七列表新增 semver（11 → 12 组），计数 33 → 34 |
| 索引与记录 | docs/index 166 项、README、decisions/index、licenses/index、ai-errors A85-A87、code-ownership-audit、implementation-strategy、THIRD-PARTY-NOTICES、interface-log、rounds |

「干」继续替换自写代码：`core/instance.rs` 的 `==` / `contains` 三处版本字符串比较换成 `semver 1.0.28` 的 `Version::cmp_precedence` 与 `VersionReq::matches`。精确串相等保留（MC 快照版本）、普通三段版本不被当 caret 放宽、显式范围符号才走范围解析、解析失败不崩。用户指定实例排第一与习惯权重排序未动。

**本轮是扩展，不是纯等价替换**：新增 `+build` 元数据归一与 `1.20.x` / `>=1.20.0, <1.21.0` 范围匹配；原有 5 个测试全部通过。带前缀版本名（如 `Paper 1.20.4`）当前仍走回退不匹配，标未证实，没有一手资料前不擅自 stripping。

界面闸门**未触发**：本轮不动界面布局，只更新关于页许可表数据并重渲 4 张许可相关截图。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E28 | 首版用 `Version::eq` 判同版本，`build_metadata_is_ignored_by_the_library` 失败 | 独立小程复核 `==` 包含 build 元数据，改 `cmp_precedence(..) == Ordering::Equal`，161 / 0 |
| E29 | 普通 `1.20.4` 交给 `VersionReq` 会当 `^1.20.4` 误匹配 `1.21.1` | 立 M04，只在显式带范围符号时走范围解析 |

028 三项开服器功能仍按「只记文档」零实现。未做：UI 实现、真实运行时 / GUI / 跨平台构建、launcher / lightweight 业务模块替换、CF F17、特殊版代码、本项目 LICENSE、后端仓写请求。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '161. docs/verification/round-033.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '161. docs/verification/round-033.md\n162. docs/spec/34-round-034-instructions.txt\n163. docs/decisions/034-semver-version-matching.md\n164. docs/rules/auto-command-policy.md\n165. docs/licenses/semver-LICENSE-MIT.txt\n166. docs/verification/round-034.md\n\n读取命令：', 1)
    t = t.replace('docs/verification/round-033.md; do printf',
                  'docs/verification/round-033.md docs/spec/34-round-034-instructions.txt docs/decisions/034-semver-version-matching.md docs/rules/auto-command-policy.md docs/licenses/semver-LICENSE-MIT.txt docs/verification/round-034.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 034 |', p.read_text(), count=1)
section = '''

## 034 版本匹配交给 semver

`core/instance.rs` 三处自写字符串比较换成 `semver 1.0.28`：精确串相等保留（MC 快照版本）、普通三段版本不被当 caret 放宽、显式范围符号才走 `VersionReq`、解析失败不崩。新增 `+build` 元数据归一与 `1.20.x` / `>=1.20.0, <1.21.0` 范围匹配；用户指定实例排第一与习惯权重排序未动。

零传递依赖，`Cargo.lock` 13 包 / 12 第三方，`cargo test --offline` 161/0。带前缀版本名（如 `Paper 1.20.4`）当前仍走回退，标未证实。口径与行为差异见 `docs/decisions/034-semver-version-matching.md`。
'''
if '## 034 版本匹配' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

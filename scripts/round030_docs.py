from pathlib import Path
import re

Path('docs/spec/30-round-030-instructions.txt').write_text('干，两个q交代下场景不然不好判断\n')
print('SPEC_OK')

D = {}

D['docs/decisions/030-args-and-q-scenarios.md'] = '''# 第 030 轮：参数解析换 lexopt，Q-028 两条问题铺场景

| 项 | 值 |
| --- | --- |
| 编号 | 030 |
| 状态 | 代码已实现、已验证；两条待拍板问题仍待答复 |
| 依据 | docs/spec/30-round-030-instructions.txt |
| 前序 | 029-cache-lru.md、docs/features/server-auto-command-log-trigger.md 待拍板段 |
| 本轮性质 | 双轨轮 |

## 两条指令的边界

| 编号 | 原文片段 | 处置 |
| --- | --- | --- |
| B01 | 「干」 | 继续按 `docs/records/code-ownership-audit.md` 映射表替换自写代码，落 `src/core/args.rs`。 |
| B02 | 「两个q交代下场景不然不好判断」 | 把 Q-028-01 / Q-028-02 铺成可判断的画面，写 `docs/records/q028-decision-scenarios.md`；不替用户拍板、不改功能 md 的结论。 |

## B01：参数解析换成 lexopt 0.3.2

| 编号 | 动作 |
| --- | --- |
| C01 | 查 `blyxxyz/lexopt` tag 列表（v0.3.2 / v0.3.1 / …），取 v0.3.2 manifest：零依赖、单文件 `src/lib.rs`、MIT、edition 2018、无 proc-macro、无 build.rs。 |
| C02 | 从 codeload tarball 精准提取 `src/lib.rs` + `Cargo.toml` + `LICENSE`（29 215 字节 tarball / 1055 字节 LICENSE）；裁掉 manifest 的 `[profile.test]` 段，上游 `src/` 一行未改。 |
| C03 | `Cargo.toml` 加 `lexopt = "0.3.2"`；`Cargo.lock` 9 → **10 包 / 9 第三方**；`vendor/` 加 1 个目录。 |
| C04 | `src/core/args.rs` 删掉手写 `peekable()` + `match tok.as_str()` + `it.next()` 取值 + 手写错误串；改用 `lexopt::Parser::from_args` / `Arg::{Long, Value}` / `parser.value()` / `Arg::unexpected()`。 |
| C05 | 保留项目特有的语义层：`--join-server` 别名、6 个字段、`extras`、`joins_server()`、`headless()`、统一 `Result<String, String>` 错误面。这层约 66 行是业务编排，不是参数解析器。 |

### 删掉的自写解析逻辑

| 025–029 | 030 |
| --- | --- |
| `xs.into_iter().map(Into::into).peekable()` 手工游标 | `Parser::from_args` |
| `match tok.as_str()` 字符串前缀比对 | `Arg::Long(&str)` 枚举匹配 |
| `it.next().ok_or_else(...)` 取值 | `parser.value()`（含 `MissingValue` 错误类型） |
| `other.starts_with('-')` 判未知 flag | `Arg::unexpected()` |
| 手写 `"--server requires a value"` 等 6 条错误串 | 库的 `Error` 转 String |

### 行为差异（如实登记）

| 编号 | 项 | 029 | 030 |
| --- | --- | --- | --- |
| B10 | `--instance=alpha` | 报 `unknown flag` | **接受**（lexopt 的 `--opt=value`） |
| B11 | `--` 之后全部 token | 按 `-` 开头仍报错 | **全部作为 positional** 进 `extras` |
| B12 | `-q` 短选项 / `-abc` 组合 | 报 `unknown flag` | 交给 `Arg::Short`，当前未注册故仍报错，但错误串来自库 |
| B13 | 非 Unicode 值 | `String` 天然不会 | 显式 `OsString::into_string()` 报「value is not valid unicode」 |
| B14 | 未知 flag 错误串 | `unknown flag: --nope` | `unexpected option '--nope'` |

B10 / B11 是能力升级（更符合命令行惯例），B12 / B14 是错误文案口径变化，未发现调用方依赖精确文案。原 5 个测试断言（单参数进服、别名、缺值拒绝、未知 flag 拒绝、kculf/kculh 分离）全部保留未改。

### 新增测试

| 编号 | 断言 |
| --- | --- |
| N01 | `--instance=alpha` 等值语法被接受。 |
| N02 | `--` 之后的 `--server literal` 只进 `extras`，不触发进服。 |
| N03 | positional 与选项混排时 `extras` 保持顺序。 |

`cargo test --offline` **141 → 144 / 0**。

## B02：两条 Q 的场景交代

写 `docs/records/q028-decision-scenarios.md`，不替用户拍板。要点：

| 编号 | 内容 |
| --- | --- |
| S01 | 说明两条问题的来历：013 的 Q-D02「每次请求」是 **AI 接口**授权，F028-03 是**日志驱动自动化**，不是同一类请求。 |
| S02 | 点出共同背景：日志里 `issued server command: /op Notch` 是**玩家输入的文字**，不是服务器真的执行过命令，触发源天然「输入不可信」。 |
| S03 | Q-028-01 铺 4 个画面：凌晨无人值守的卡顿预警、玩家聊天文字诱导、模组刷屏、规则「测试」按钮预览；给 Q1-A / Q1-B / Q1-C 三个口径及各自后果。 |
| S04 | Q-028-02 把动作分 C1–C5 五类（只读 / 游戏内广播 / 服务器命令 / 启动器侧动作 / 外部动作），点名 `/save-all` 撞崩服、`/op` 撞诱导、`/stop` 撞刷屏、C5 撞脱敏四个风险画面；给 Q2-A / Q2-B / Q2-C / Q2-D 四个口径。 |
| S05 | 写出耦合矩阵：越不弹确认，动作白名单越得收紧；建议一次拍 `Q1-B + Q2-C` 或 `Q1-A + Q2-B`。 |
| S06 | 相邻三项 N01–N03（来源限定默认值、冷却秒数、外传脱敏）按既有「你看着办」自行定默认，不占用户这次答复。 |

**倾向只写在场景文档里，没写进功能 md**：Q1-B（按动作分级）、Q2-B 打底 + Q2-C 可见面。功能 md 的「待拍板」段改为指向场景文档，结论栏仍为空。

## 四值

| 项 | 值 |
| --- | --- |
| 10 包 / 9 第三方、144 / 0、原 5 断言未改 | 已证实 |
| 手写参数解析器删除、lexopt 上游源码未改、MIT 全文落盘 | 已证实 |
| 两个 Q 的 4 + 4 个场景、耦合矩阵、建议组合 | 已证实 |
| Q-028-01 / Q-028-02 的用户答复与最终口径 | 未证实（待答复） |
| 真实 GUI 端到端、Win7 / 多架构、CI 独立构建 | 受阻 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-030.md'] = '''# 第 030 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 030 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile`，编译 lexopt 0.3.2 / kcu-core | 已证实 |
| V2 | `cargo test --offline` | 144 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 10 包 / 9 第三方 | 已证实 |
| V4 | `grep -c 'lexopt' src/core/args.rs` | 3（prelude / Parser::from_args / value 签名） | 已证实 |
| V5 | `grep -c 'peekable\\|starts_with' src/core/args.rs` | 0 | 已证实 |
| V6 | `git diff 54a29d7 -- vendor/lexopt/src/lib.rs` | 不存在（新文件）；与上游 tag tarball 逐字节一致 | 已证实 |
| V7 | `docs/licenses/lexopt-LICENSE.txt` | 1055 字节，MIT，Copyright (c) 2021 Jan Verbeek | 已证实 |
| V8 | `grep -c '构建中已使用' demos/ui-full-kcu-paper.html` | 9 | 已证实 |
| V9 | `docs/records/q028-decision-scenarios.md` 场景计数 | Q1 4 个、Q2 4 个风险画面、5 类动作、耦合矩阵 1 张 | 已证实 |
| V10 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V11 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V12 | 必读文件循环 | REQUIRED=146 MISSING=0 | 已证实 |
| V13 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 参数解析库化、144 / 0、依赖闭包零传递 | 已证实 |
| 两个 Q 的场景交代完整、无代拍板 | 已证实 |
| `docs/features/server-auto-command-log-trigger.md` 结论栏仍为空 | 已证实 |
| 两个 Q 最终口径、三项相邻默认值落地 | 未证实 |
| 真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 |
| 144 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)

MARKERS = {}

def app(f, s):
    p = Path(f)
    t = p.read_text()
    marker = s.strip().splitlines()[0]
    if marker in t:
        print('SKIP_DUP', f)
        return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 030 | 参数解析换 lexopt；Q-028 两条问题铺场景 | 代码已实现；两 Q 待答复 | 030-args-and-q-scenarios.md |')

app('docs/records/code-ownership-audit.md', '''## 030 第四块替换后状态

| 项 | 024 | 025 | 027 | 028 | 029 | 030 |
| --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 7 | 8 | **9** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 8 | 9 | 10 |
| `dispatcher/json.rs` | 336 | 77 | 77 | 77 | 77 | 77 |
| `core/asynk.rs` | 258 | 258 | 250 | 250 | 250 | 250 |
| `core/leak.rs` | 191 | 191 | 191 | 99 | 99 | 99 |
| `core/cache.rs` | 304 | 304 | 304 | 304 | 327 | 327 |
| `core/args.rs` | 91 行手写解析 | 91 | 91 | 91 | 91 | **120（实现段 66，含语义层）** |
| `src/` 行数 | 4339 | 4081 | 4073 | 3986 | 4017 | 4046 |

030 删掉的自写参数解析器：手工 `peekable` 游标、字符串前缀 match、`it.next()` 取值、手写 6 条错误串、`starts_with('-')` 未知 flag 判定。换成 `lexopt 0.3.2`（零依赖、单文件、MIT）。保留的 66 行是 6 个字段、别名、统一错误面、`joins_server()` / `headless()` 这类项目特有语义，不是解析器。

剩余自写模块：`dispatcher/launcher.rs` 541、`lightweight/*.rs` 1135、`core/config.rs`（BTreeMap 注入）、`core/paths.rs`（逻辑名映射）、`core/log.rs`（分片缓冲）、`core/popup.rs`、`core/userflow.rs`、`core/instance.rs`、`core/envelope.rs`、`core/diagnostics.rs`。后两者是跨进程协议定义，不在替换映射内；其余按本文件映射继续推进。
''')

app('docs/design/implementation-strategy.md', '''## 030 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 | 已落地（025，serde_json） |
| 异步 / 线程同步 | 已落地（027，crossbeam） |
| 缓存容量 / LRU / 单飞 | 已落地（029，lru 0.12.5） |
| 命令行参数解析 | **已落地（030，lexopt 0.3.2）** |
| 配置 / 路径 / 日志 / 真实网络 / UI / 崩溃 / 插件 | 未启动 |
''')

app('THIRD-PARTY-NOTICES.md', '''## 030 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| lexopt | 0.3.2 | MIT | Jan Verbeek (c) 2021 | 命令行参数解析 | vendor/lexopt | 构建中已使用 |

许可证全文：`docs/licenses/lexopt-LICENSE.txt`。

| 编号 | 约束 |
| --- | --- |
| N22 | 上游 tarball 的 `[profile.test]` 段对依赖无效，裁掉以免本地目录源解析告警；`src/lib.rs` 未改。 |
| N23 | MIT 条款要求保留版权与许可声明，全文随发行物附上。 |
''')

app('docs/licenses/index.md', '''## 030 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| lexopt-LICENSE.txt | lexopt 0.3.2 | MIT |

来源：blyxxyz/lexopt tag `v0.3.2` 内的 LICENSE，逐字副本，1055 字节。
''')

app('docs/checklists/ai-errors.md', '''## 030 轮新增

| 编号 | 防错项 |
| --- | --- |
| A73 | 待拍板问题不能只写一句问号：必须给具体使用场景、每个选项的后果、以及与其他问题的耦合关系，否则用户无法判断。 |
| A74 | 参数解析库化时保留项目语义层（别名、统一错误面、业务判定），不要把业务字段一起塞进库调用里。 |
| A75 | 引用 013 轮答复前先核它原本问的是什么：Q-D02「每次请求」是 AI 接口授权，不能默认复用到日志触发的服务器自动化。 |
''')

app('docs/research/index.md', '''## 030 轮新增

| 编号 | 文档 | 主题 |
| --- | --- | --- |
| R22 | q028-decision-scenarios.md | 日志命令文字触发的授权粒度与动作分级场景 |

完整 URL：

- https://github.com/blyxxyz/lexopt/tree/v0.3.2
- https://api.github.com/repos/blyxxyz/lexopt/contents/Cargo.toml?ref=v0.3.2
- https://codeload.github.com/blyxxyz/lexopt/tar.gz/refs/tags/v0.3.2
- https://api.github.com/repos/blyxxyz/lexopt/tags?per_page=15
''')

app('docs/records/interface-log.md', '''## 030 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I31 | `LaunchArgs::parse` | 签名不变，内部实现换 lexopt；错误面仍 `Result<Self, String>` |
| S29 | 状态 | 参数解析已库化；Q-028-01 / Q-028-02 仍待用户答复，功能 md 结论栏为空 |
''')

app('docs/records/rounds.md', '''## 030

| 落点 | 内容 |
| --- | --- |
| docs/spec/30-round-030-instructions.txt | 逐字副本 1 行 |
| docs/decisions/030-args-and-q-scenarios.md | B01/B02 边界、C01-C05、B10-B14、S01-S06、四值 |
| docs/records/q028-decision-scenarios.md | **两条 Q 的场景交代**（本轮用户重点） |
| docs/verification/round-030.md | 13 条复跑证据 |
| demos/round-030-args-q.html | 13 步运行逻辑演示（含场景分支） |
| src/core/args.rs | 手写参数解析器删除，换 lexopt 0.3.2，91 → 120 行（新增 3 测试） |
| vendor/lexopt/ + Cargo.toml/lock | 10 包 / 9 第三方 |
| docs/licenses/lexopt-LICENSE.txt | MIT 全文 1055 字节 |
| demos/ui-full-kcu-paper.html / demos/preview/ | 关于页 9 组「构建中已使用」，2 张截图重渲 |
| 索引与记录 | docs/index 146 项、README、decisions/index、research/index、licenses/index、ai-errors A73-A75、code-ownership-audit、implementation-strategy、THIRD-PARTY-NOTICES、interface-log、rounds |

「干」继续替换自写代码，按映射表落第四块 `core/args.rs`。选 lexopt 0.3.2 的理由：零依赖、单文件、MIT、无 proc-macro，Win7 Tier 3 / 多架构友好，不重撞 libc。

「两个q交代下场景」按用户要求铺成可判断的画面，不代拍板：

| 编号 | 场景 |
| --- | --- |
| Q1-A | 凌晨三点无人值守的卡顿预警（每次同意 → 自动化失效；不弹 → 可能写坏存档） |
| Q1-B | 玩家公屏打字 `/op Steve` 诱导命中（日志里的命令文字是文本，不是授权） |
| Q1-C | 模组每秒刷一行关键字（60 个弹窗 vs 冷却合并） |
| Q1-D | 规则「测试」按钮只该预览，不该弹同意也不该真发命令 |
| Q2 | 动作分 C1 只读 / C2 广播 / C3 服务器命令 / C4 启动器侧 / C5 外传；点名 `/save-all` 撞崩服、`/op` 撞诱导、`/stop` 撞刷屏、C5 撞脱敏 |

另写出耦合矩阵与建议组合 `Q1-B + Q2-C` / `Q1-A + Q2-B`。倾向只写在场景文档，功能 md 结论栏仍为空。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E13 | 首版 `args.rs` 把 `Arg::Value(OsString)` 直接 push 进 `Vec<String>`，且把 `unexpected()` 当成 Parser 方法 | 改 `into_string()` 显式转换，`unexpected()` 属 `impl Arg` 不是 Parser；复跑 144 / 0 |
| E14 | 029 的文档脚本重跑造成过重复追加，本轮脚本 `app()` 与 README 段全部改为幂等 | 030 脚本一次运行无重复 |

028 的三项开服器功能仍按「只记文档」零实现。未做：UI 实现、真实运行时 / GUI / 跨平台构建、launcher / lightweight 业务模块替换、CF F17、特殊版代码、本项目 LICENSE、后端仓写请求。
''')

# 功能 md 待拍板段指向场景文档
p = Path('docs/features/server-auto-command-log-trigger.md')
t = p.read_text()
old = '''## 待拍板

| 编号 | 问题 |
| --- | --- |
| Q-028-01 | 命中后是否每次都要手动同意（013 答复 Q-D02 是「每次请求」，那条口径属于 AI 权限，不确定是否复用到这里）。 |
| Q-028-02 | 预设动作允许哪些命令：仅白名单 / 黑名单之外全部 / 只读诊断行。 |'''
new = '''## 待拍板

| 编号 | 问题 | 场景 |
| --- | --- | --- |
| Q-028-01 | 命中后是否每次都要手动同意（013 答复 Q-D02 是「每次请求」，那条口径属于 AI 接口授权，不是日志驱动的服务器自动化）。 | docs/records/q028-decision-scenarios.md 场景 A–D |
| Q-028-02 | 预设动作允许哪些命令：C1–C5 五类怎么取舍，黑名单是否不可禁用。 | 同文档 C1–C5 与四个风险画面 |

结论栏仍为空；耦合矩阵与建议组合见场景文档，用户答复后才写回本文件。'''
if old in t:
    p.write_text(t.replace(old, new, 1))
    print('FUNC_MD_OK')
elif '结论栏仍为空' in t:
    print('FUNC_MD_SKIP_DUP')
else:
    raise AssertionError('func md anchor missing')

p = Path('docs/index.md')
t = p.read_text()
a = '141. docs/verification/round-029.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '141. docs/verification/round-029.md\n142. docs/spec/30-round-030-instructions.txt\n143. docs/decisions/030-args-and-q-scenarios.md\n144. docs/records/q028-decision-scenarios.md\n145. docs/licenses/lexopt-LICENSE.txt\n146. docs/verification/round-030.md\n\n读取命令：', 1)
    t = t.replace('docs/verification/round-029.md; do printf',
                  'docs/verification/round-029.md docs/spec/30-round-030-instructions.txt docs/decisions/030-args-and-q-scenarios.md docs/records/q028-decision-scenarios.md docs/licenses/lexopt-LICENSE.txt docs/verification/round-030.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 030 |', p.read_text(), count=1)
section = '''

## 030 参数解析换 lexopt，两条 Q 铺场景

`src/core/args.rs` 的手写 `peekable` 游标、字符串前缀 match、`it.next()` 取值与 6 条错误串全部删除，换成 `lexopt 0.3.2`（零依赖、单文件、MIT）。`Cargo.lock` 10 包 / 9 第三方，`cargo test --offline` 144/0，原 5 个断言未改。

Q-028-01 / Q-028-02 按你的要求铺成能判断的画面：凌晨无人值守的卡顿预警、玩家聊天文字诱导、模组刷屏、规则测试预览；动作分只读 / 广播 / 服务器命令 / 启动器侧 / 外传五类，点名 `/save-all` 撞崩服、`/op` 撞诱导、`/stop` 撞刷屏、外传撞脱敏。含耦合矩阵与建议组合，不代拍板。见 `docs/records/q028-decision-scenarios.md`。
'''
if '## 030 参数解析换 lexopt' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

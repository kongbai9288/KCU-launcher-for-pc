from pathlib import Path
import re

Path('docs/spec/32-round-032-instructions.txt').write_text('干，用户可选松档\n')
print('SPEC_OK')

# ---------- 功能 md：R04 改写 + 档位段 ----------
p = Path('docs/features/server-auto-command-log-trigger.md')
t = p.read_text()
old = '''| R04 | F028-03 在 Q2-A 下**不会真的向服务器发命令**，实际形态是「日志关键词提醒器 + 每次确认」。若本意是还要能自动执行游戏内动作，需改 Q2 口径。 |'''
new = '''| R04 | **严格档**下 F028-03 不会真的向服务器发命令，实际形态是「日志关键词提醒器 + 每次确认」。032 起用户可自行切到标准 / 宽松档，勾选 C3 后才会发命令；默认仍是严格档。 |'''
assert old in t
t = t.replace(old, new, 1)

anchor = '''## 待用户确认的歧义'''
assert anchor in t
tier_section = '''## 032 用户可选松档

| 项 | 值 |
| --- | --- |
| 默认档 | **严格**（031 的 P01–P07 不变） |
| 可选档 | 标准 / 宽松，由用户在设置里主动切换 |
| 切换 | 二次确认，列差异与风险，可取消，随时切回 |
| 插件 | 不能替用户切档，不能放宽默认档 |

三档矩阵与不可变边界见 `docs/rules/auto-command-policy.md`。

| 编号 | 落地约束 |
| --- | --- |
| P08 | 三档单调变松：确认粒度「每次问 → 只读免问 → 授权后全免」，动作范围「仅 C1 → 五类逐项 → 五类全可开」。 |
| P09 | 每次切档写 `[KCU]` 诊断行与审计记录；每条命中仍写审计，即使该档免确认。 |
| P10 | C5 外传永远二次确认且默认脱敏，不随档位放开（013 Q-C15 的硬口径）。 |
| P11 | 黑名单在宽松档可逐条显式解除，每条单独二次确认、界面标红、写审计；默认全锁。 |
| P12 | 「测试」按钮任何档都只预览，不弹同意、不真发动作。 |

## 待用户确认的歧义'''
t = t.replace(anchor, tier_section, 1)
p.write_text(t)
print('FUNC_MD_OK')

# ---------- 规则文档：改成默认档 + 可选档矩阵 ----------
p = Path('docs/rules/auto-command-policy.md')
t = p.read_text()
t = t.replace('| 状态 | 已拍板、已写进界面演示；实现层未启动 |', '| 状态 | 已拍板；031 严格档为默认，032 起用户可选松档；实现层未启动 |')
t = t.replace('| 依据 | 031 用户答复「按最严格去执行」 |', '| 依据 | 031「按最严格去执行」；032「用户可选松档」 |')
t = t.rstrip() + '''

---

## 032 用户可选松档

| 项 | 值 |
| --- | --- |
| 默认 | **严格档**（本文件上半部 P01–P07 全部适用） |
| 用户动作 | 设置 → 自动命令 → 宽严程度，自己点「标准」或「宽松」 |
| 触发条件 | 只有用户本人能切；插件、更新器、首次启动、重置默认值都不能切 |
| 回退 | 「恢复严格」常驻，随时可切回；切换记录审计 |

### 三档矩阵

| 档 | 确认粒度 | 动作范围 | 夜间无人值守 | 风险 |
| --- | --- | --- | --- | --- |
| 严格（默认） | **Q1-C** 每次命中都问 | **Q2-A** 仅 C1 只读 | 失效 | 最低 |
| 标准 | **Q1-B** C1 自动，C2–C5 每次问 | **Q2-C** 五类逐项，默认只 C1 | 只读动作有效 | 中 |
| 宽松 | **Q1-A** 规则级一次性授权后自动 | **Q2-D** 五类全可开，黑名单可逐条解除 | 有效 | 高 |

三档单调变松，不出现「更松的档反而问得更多」的倒挂。031 的 P01–P07 只在严格档整体适用；标准 / 宽松档按上表覆盖 P01、P02、P03，其余 P04–P07 仍适用。

### 任何档都不能越过的边界

| 编号 | 规则 |
| --- | --- |
| U01 | 新装、重置默认、插件安装、插件化更新后，档位一律回到严格。 |
| U02 | 切档只能由用户在设置里主动做；插件不能调用切档接口，不能替用户确认。 |
| U03 | 切档弹二次确认，列清「切过去以后会多做什么、有什么风险、仍不会做什么」；取消 / × / ESC / 宿主都能关，流程后 0 残留。 |
| U04 | 切档写 `[KCU]` 诊断行与审计记录；每条命中仍写审计，即使该档免确认。 |
| U05 | C5 外传永远二次确认且默认脱敏，不随档位放开（013 Q-C15）。 |
| U06 | 「测试」按钮任何档都只预览命中与将执行的动作，不弹同意、不真发动作。 |
| U07 | 黑名单 `/op /deop /ban /stop /restart /whitelist` 默认全锁；宽松档可逐条显式解除，每条单独二次确认、界面标红、写审计。 |

### 后果更新

| 编号 | 后果 |
| --- | --- |
| R01 | 严格档夜间自动化失效；标准 / 宽松档由用户自己打开，失效问题得到补救，代价由用户承担。 |
| R02 | 严格档双重保险；标准 / 宽松档仍保留 P04「仅服务端输出」与 U05 外传确认。 |
| R03 | 严格档由 P05 收敛为一条待确认 + 计数；非严格档按该档确认粒度执行，仍写审计。 |
| R04 | 严格档不发服务器命令；标准 / 宽松档用户勾选 C3 后才按该档确认粒度发。 |

### 界面落点（032）

| 编号 | 落点 |
| --- | --- |
| U08 | 设置 → 自动命令 → 顶部「宽严程度」三张档位卡，默认严格高亮，当前档徽章可见。 |
| U09 | 切档二次确认弹窗 `demos/preview/47-tier-switch.png`；「恢复严格」按钮常驻。 |
| U10 | 非严格档把「能做的事」从静态徽章换成五类勾选，每类带风险小字；严格档全部置灰。 |
| U11 | 预览图 `46-settings-tiers.png` / `47-tier-switch.png` / `48-loose-actions.png`；整页演示 `demos/ui-full-kcu-paper.html`。 |

界面文案走语义 key（`auto.tier.*` / `auto.a1`…），不把中文当 key，不写工程标识、槽位 ID 或策略编号。
'''
p.write_text(t)
print('POLICY_OK')

# ---------- 场景文档追加 032 ----------
p = Path('docs/records/q028-decision-scenarios.md')
t = p.read_text()
t = t.replace('| 状态 | 031 已答复；按最严格口径落地 |', '| 状态 | 031 按最严格落地；032 起用户可选松档 |')
t = t.rstrip() + '''

---

## 032 补充：用户可选松档

用户原话：`干，用户可选松档`。

| 项 | 变化 |
| --- | --- |
| 默认 | 严格档不变（Q1-C + Q2-A） |
| 新增 | 设置里由用户主动切「标准」或「宽松」，二次确认、可随时切回 |
| 未变 | 严格档的 P04–P07、外传二次确认、测试只预览、插件不能替用户切 |

三档矩阵、U01–U07、后果 R01–R04 的更新见 `docs/rules/auto-command-policy.md`。

| 场景 | 031 严格 | 032 标准 / 宽松 |
| --- | --- | --- |
| A 凌晨无人值守 | 失效 | 用户自己打开后有效，代价由用户承担 |
| B 玩家文字诱导 | 只读 + 每次问 | 仍只认服务端输出；外传仍单独确认 |
| C 模组刷屏 | 一条待确认 + 计数 | 按该档确认粒度执行，仍写审计 |
| D 规则测试 | 只预览 | 只预览 |

Q-031-01 字母歧义这次没有答复，仍挂在 `docs/features/server-auto-command-log-trigger.md` 待确认；「可选松档」不改变 031 严格档的判定依据。
'''
p.write_text(t)
print('SCENARIOS_OK')

D = {}

D['docs/decisions/032-user-selectable-tiers.md'] = '''# 第 032 轮：用户可选松档，日志门面换 log crate

| 项 | 值 |
| --- | --- |
| 编号 | 032 |
| 状态 | A 轨已落地界面与规则、B 轨代码已实现已验证 |
| 依据 | docs/spec/32-round-032-instructions.txt |
| 前序 | 031-strict-policy-and-config.md、auto-command-policy.md |
| 本轮性质 | 双轨轮 |

## 两条指令的边界

| 编号 | 原文片段 | 处置 |
| --- | --- | --- |
| A01 | 「用户可选松档」 | 031 最严格口径保留为**默认档**，新增标准 / 宽松两档由用户主动切换；写三档矩阵、七条不可变边界、界面演示与 3 张预览图。 |
| B01 | 「干」 | 继续按 `docs/records/code-ownership-audit.md` 映射表替换自写代码，落 `core/log.rs` 与 `core/diagnostics.rs`。 |

## A01：用户可选松档

| 编号 | 动作 |
| --- | --- |
| C01 | 三档单调变松：严格（Q1-C + Q2-A）→ 标准（Q1-B + Q2-C）→ 宽松（Q1-A + Q2-D）。不出现「更松反而问得更多」的倒挂。 |
| C02 | 默认档恒为严格；新装、重置、插件安装、插件化更新后一律回严格。 |
| C03 | 切档只能用户在设置里主动做，二次确认弹窗列「会多做什么 / 有什么风险 / 仍不会做什么」；取消 / × / ESC / 宿主都能关，流程后 0 残留。 |
| C04 | 七条不可变边界 U01–U07：切档审计、每条命中仍记审计、C5 外传永远二次确认且默认脱敏、测试只预览、黑名单逐条解锁。 |
| C05 | 后果更新：R01 夜间自动化在标准 / 宽松档由用户自己打开；R04 严格档不发命令，非严格档勾选 C3 后才发。 |
| C06 | 界面：设置 → 自动命令 → 顶部三张档位卡、当前档徽章、常驻「恢复严格」；非严格档把「能做的事」换成五类勾选带风险小字。 |
| C07 | 顺带修掉 031 分组里把中文当 `data-i18n` key 的 27 处，改成 `auto.*` 语义 key 并补英文条目，回应早先的文案硬编码批评。 |

### 用户逻辑推演

| 画面 | 处理 |
| --- | --- |
| 用户只想被提醒 | 什么都不动，默认严格档已经是 |
| 用户夜里想让卡顿预警自己跑 | 自己点「标准」，二次确认后生效，可随时点「恢复严格」 |
| 服主想让规则授权一次就一直自动 | 自己点「宽松」，逐类勾动作，黑名单要一条一条单独解 |
| 插件想偷偷放宽 | U02 拒绝，插件不能调用切档接口 |
| 切完忘了自己切过 | 当前档徽章常驻 + 审计记录可查 |
| 英文界面 | 语义 key 走 `auto.tier.*`，切语言时档位卡与动作行一起重渲 |

### 四值

| 项 | 值 |
| --- | --- |
| 三档矩阵、U01–U07、R01–R04 更新、语义 key 27 处 | 已证实 |
| 3 张新预览图、整页演示可点 | 已证实 |
| Q-031-01 字母歧义 | 未证实（本次仍未答复） |
| 自动命令实现层、真实运行时 | 未启动 / 受阻 |

## B01：日志门面换成 log 0.4.35

| 编号 | 动作 |
| --- | --- |
| D01 | 查 `rust-lang/log` tag v0.4.35 的 manifest：`[dependencies]` 四项全是 optional，`[dev-dependencies]` 与 proc-macro2 note 与运行时无关。 |
| D02 | vendor 时裁掉 optional deps、dev deps 与引用外部 crate 的 features 行，重建 `[features]` 只留 14 个无外部引用的开关；`src/` 原样保留，上游源码一行未改。 |
| D03 | `Cargo.toml` 加 `log = { version = "0.4.35", default-features = false, features = ["std"] }`；`Cargo.lock` 10 → **11 包 / 10 第三方**，log 零传递依赖。 |
| D04 | `core/log.rs` 删掉自写 `push(&mut self, line)` / `flush(&mut self)`；`LogBuffer` 实现 `log::Log`，`log(&self, &Record)` 写缓冲，`flush(&self)` 走库契约，`take_shards()` 取分片。内部状态改 `Mutex<Inner>` 以支持 `&self`。 |
| D05 | `core/diagnostics.rs` 保留 `diag_line` 格式函数，新增 `emit(&LogBuffer, ...)` 经 `Record` 走门面。 |
| D06 | `dispatcher/launcher.rs` 2 处、`lightweight/view.rs` 1 处 + 1 处测试调用面同步换成 `record(...)` / `take_shards()`。 |

### 删掉的自写日志 API

| 031 | 032 |
| --- | --- |
| `pub fn push(&mut self, line: impl Into<String>)` | `impl Log for LogBuffer { fn log(&self, &Record) }` |
| `pub fn flush(&mut self) -> Vec<Vec<String>>` | `pub fn take_shards(&self)` + `Log::flush(&self)` |
| `Vec<String> current` / `Vec<Vec<String>> shards` 直接字段 | `Mutex<Inner>` 内部可变性 |
| 调用方直接拼字符串再 push | `record(fmt::Arguments, Level, target)` / `diagnostics::emit` |

分片策略（每 N 行一片）仍是项目特有约 30 行，如实登记，没有说成「全用库」。

### 行为差异

| 编号 | 项 | 031 | 032 |
| --- | --- | --- | --- |
| B10 | 写入方法 | `&mut self` | `&self`（库 trait 契约） |
| B11 | 取分片 | `flush()` 返回 Vec | `take_shards()` 返回 Vec；`Log::flush()` 丢弃缓冲 |
| B12 | 行内容 | 原样字符串 | `Record::args().to_string()`，等价 |
| B13 | 日志级别 / target | 不存在 | `Level` 与 `target` 进门面，当前实现全部接收 |

### 新增测试

| 编号 | 断言 |
| --- | --- |
| N01 | `Log::enabled` 对 Trace 级 Metadata 返回 true。 |
| N02 | `record()` helper 经门面写入且内容一致。 |
| N03 | `Log::flush(&self)` 后分片与待写都归零。 |
| N04 | `diagnostics::emit` 输出与 `diag_line` 完全一致。 |

`cargo test --offline` **149 → 153 / 0**，原 3 个 LogBuffer 断言与 2 个 diagnostics 断言未改。

### 本轮真实失败与修复（全部留痕）

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E17 | 裁 manifest 后 `kv_unstable_serde` 仍引用 `kv_serde`，Cargo 解析整个目录源失败 | 重建 `[features]` 为 14 个零外部引用开关 |
| E18 | `g.shards.push(std::mem::take(&mut g.current))` 触发 E0499 双可变借用 | 拆成 `let done = ...; g.shards.push(done);` |
| E19 | 测试里 `format_args!` 链式构造 `Record` 触发 E0716 临时值提前释放 | `let args = format_args!(...)` 绑定后再 `builder().args(args)` |
| E20 | 档位初始化绑定被同名字符串误判为已存在而跳过 | 改用 init 段特有字符串作幂等判据，补插并复验 |

## 四值

| 项 | 值 |
| --- | --- |
| 三档矩阵、U01–U07、3 张预览图、语义 key 27 处 | 已证实 |
| log 0.4.35 进构建、153 / 0、11 包 10 第三方 | 已证实 |
| 上游 `src/` 未改、MIT 与 Apache-2.0 全文落盘 | 已证实 |
| Q-031-01 字母歧义 | 未证实 |
| 自动命令实现层、真实 GUI 端到端、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-032.md'] = '''# 第 032 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 032 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile`，编译 log 0.4.35 / kcu-core | 已证实 |
| V2 | `cargo test --offline` | 153 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 11 包 / 10 第三方 | 已证实 |
| V4 | `grep -c 'pub fn push' src/core/log.rs` | 0 | 已证实 |
| V5 | `grep -c 'impl Log for LogBuffer' src/core/log.rs` | 1 | 已证实 |
| V6 | `vendor/log/src/lib.rs` 与上游 tag tarball | 逐字节一致 | 已证实 |
| V7 | `docs/licenses/log-LICENSE-MIT.txt` / `log-LICENSE-APACHE.txt` | 1071 / 10847 字节 | 已证实 |
| V8 | `docs/rules/auto-command-policy.md` | 三档矩阵 1 张、U01–U07 七条、R01–R04 更新 | 已证实 |
| V9 | `demos/ui-full-kcu-paper.html` | `id="tierCards"` 1 处、`data-tier=` 3 处、`auto.tier.*` 语义 key ≥ 12 处 | 已证实 |
| V10 | `demos/preview/46,47,48-*.png` | 三文件非空，1440×900 | 已证实 |
| V11 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V12 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V13 | 必读文件循环 | REQUIRED=156 MISSING=0 | 已证实 |
| V14 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 用户可选松档、默认严格不变、日志门面库化 | 已证实 |
| 153 / 0、零传递依赖、上游源码未改 | 已证实 |
| Q-031-01 字母歧义 | 未证实 |
| 自动命令实现层、真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 153 测试仅作回归，不作质量结论 | 已证实 |

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


app('docs/decisions/index.md', '| 032 | 用户可选松档；日志门面换 log crate | A 已落地、B 已实现 | 032-user-selectable-tiers.md |')

app('docs/rules/index.md', '''## 032 更新

| 文档 | 变化 |
| --- | --- |
| docs/rules/auto-command-policy.md | 从单一最严格口径改为「默认严格 + 用户可选标准 / 宽松」三档矩阵，新增 U01–U11 |
''')

app('docs/records/code-ownership-audit.md', '''## 032 第六块替换后状态

| 项 | 024 | 025 | 027 | 029 | 030 | 031 | 032 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | 9 | **10** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 | 11 |
| `core/config.rs` + `envelope.rs` | 双 BTreeMap | 同 | 同 | 同 | 同 | serde_json::Map | serde_json::Map |
| `core/log.rs` | 56 行自写 API | 56 | 56 | 56 | 56 | 56 | **约 105（含 6 测试，分片策略约 30 行）** |
| `src/` 行数 | 4339 | 4081 | 4073 | 4017 | 4046 | 4197 | 约 4270 |

032 删掉的自写日志 API：`push(&mut self, ...)` / `flush(&mut self) -> Vec` / 直接字段与直接调用面。换成 `log 0.4.35` 的 `Log` trait：`log(&self, &Record)` 写缓冲、`flush(&self)` 走库契约、`take_shards()` 取分片；`diagnostics::emit` 经 `Record` 走门面。内部 `Mutex<Inner>` 与每 N 行分片是项目特有约 30 行，如实登记。

log 零传递依赖；vendor 时裁掉 optional deps、dev deps 与引用外部 crate 的 features 行，上游 `src/` 未改。MIT 与 Apache-2.0 全文都落 `docs/licenses/`，按 MIT 用。

剩余自写模块：`dispatcher/launcher.rs` 541、`lightweight/*.rs` 1135、`core/paths.rs`、`core/popup.rs`、`core/userflow.rs`、`core/instance.rs`。这些是模式判定、用户指定实例排第一、双击绑定一类项目特有编排，映射表里没有对应替换库，不硬换。
''')

app('docs/design/implementation-strategy.md', '''## 032 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 / 配置载荷 / 信封序列化 | 已落地（025、031，serde_json） |
| 异步 / 线程同步 | 已落地（027，crossbeam） |
| 缓存 / LRU / 单飞 | 已落地（029，lru 0.12.5） |
| 命令行参数解析 | 已落地（030，lexopt 0.3.2） |
| 日志门面 | **已落地（032，log 0.4.35）** |
| 配置 toml 文件编解码、路径、真实网络、UI、崩溃、插件 | 未启动 |
''')

app('docs/checklists/ai-errors.md', '''## 032 轮新增

| 编号 | 防错项 |
| --- | --- |
| A79 | 「默认最严格」与「用户可选松档」并存时，必须写明默认档、切换主体、二次确认、回退入口与插件禁令，不能把「可选」写成默认放宽。 |
| A80 | 多档位要单调变松，逐档核对「确认粒度」与「动作范围」两个维度，不能出现更松的档反而问得更多。 |
| A81 | 演示层新增文案用语义 key（如 `auto.tier.*`），不把中文文本当 `data-i18n` key；切语言时动态渲染的区块要一起重渲。 |
''')

app('docs/records/interface-log.md', '''## 032 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I34 | `LogBuffer` | `push` / `flush` 移除；新增 `record` / `take_shards`，实现 `log::Log` |
| I35 | `diagnostics` | `diag_line` 保留，新增 `emit` |
| S31 | 状态 | 三档默认严格；Q-028-01 = Q1-C、Q-028-02 = Q2-A 仅适用于严格档；F028-03 实现层未启动 |
''')

app('docs/licenses/index.md', '''## 032 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| log-LICENSE-MIT.txt | log 0.4.35 | MIT |
| log-LICENSE-APACHE.txt | log 0.4.35 | Apache-2.0 |

来源：rust-lang/log tag `v0.4.35`，两份逐字副本，1071 / 10847 字节。许可声明为 `MIT OR Apache-2.0`，本项目按 MIT 条款使用，两份全文都随发行物附上。
''')

app('THIRD-PARTY-NOTICES.md', '''## 032 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| log | 0.4.35 | MIT OR Apache-2.0（按 MIT 用） | The Rust Project Developers (c) 2014 | 日志门面 | vendor/log | 构建中已使用 |

许可证全文：`docs/licenses/log-LICENSE-MIT.txt`、`docs/licenses/log-LICENSE-APACHE.txt`。

| 编号 | 约束 |
| --- | --- |
| N24 | `default-features = false, features = ["std"]`，零传递依赖；vendor 裁掉 optional deps、dev deps 与外部 features 引用，`src/` 未改。 |
| N25 | MIT 条款要求保留版权与许可声明，全文随发行物附上；Apache-2.0 全文一并保留供选择。 |
''')

app('docs/records/rounds.md', '''## 032

| 落点 | 内容 |
| --- | --- |
| docs/spec/32-round-032-instructions.txt | 逐字副本 1 行 |
| docs/decisions/032-user-selectable-tiers.md | A01/B01 边界、三档矩阵、U01–U07、C01-C07、D01-D06、E17-E20、四值 |
| docs/features/server-auto-command-log-trigger.md | R04 改写，新增 P08–P12 与「032 用户可选松档」段 |
| docs/rules/auto-command-policy.md | 单一口径 → 默认严格 + 可选标准 / 宽松，U01–U11，后果更新 |
| docs/records/q028-decision-scenarios.md | 追加 032 段与四场景对照 |
| docs/verification/round-032.md | 14 条复跑证据 |
| demos/round-032-tiers.html | 13 步运行逻辑演示 |
| demos/ui-full-kcu-paper.html / preview | 三张档位卡、切档二次确认、非严格档五类勾选；3 张新预览图（46 / 47 / 48）；031 分组 27 处中文 key 改语义 key |
| src/core/log.rs / diagnostics.rs | 自写日志 API 换 `log::Log`，新增 `emit` |
| src/dispatcher/launcher.rs / lightweight/view.rs | 调用面同步 |
| vendor/log/ + Cargo.toml/lock | 11 包 / 10 第三方 |
| docs/licenses/log-LICENSE-*.txt | MIT 与 Apache-2.0 全文 |
| 索引与记录 | docs/index 156 项、README、decisions/index、rules/index、licenses/index、ai-errors A79-A81、code-ownership-audit、implementation-strategy、THIRD-PARTY-NOTICES、interface-log、rounds |

「用户可选松档」按「默认严格 + 用户主动切标准 / 宽松」落地。三档单调变松：严格 Q1-C + Q2-A → 标准 Q1-B + Q2-C → 宽松 Q1-A + Q2-D。七条不可变边界含默认回严格、切档二次确认与审计、C5 外传永远二次确认、插件不能替用户切档、黑名单逐条解锁。R01 夜间失效在标准 / 宽松档由用户自己打开；R04 严格档不发命令，勾选 C3 后才发。Q-031-01 字母歧义这次没答复，仍挂着。

「干」继续替换自写代码：`core/log.rs` 的自写 `push` / `flush` 全删，换成 `log 0.4.35` 的 `Log` trait；`diagnostics.rs` 新增 `emit`。零传递依赖，153 / 0。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E17 | 裁 log manifest 后 `kv_unstable_serde` 仍引用已删 feature，整个目录源解析失败 | 重建 `[features]` 为 14 个零外部引用开关 |
| E18 | `g.shards.push(std::mem::take(&mut g.current))` E0499 双可变借用 | 拆两步 |
| E19 | 测试里 `format_args!` 链式构造 Record E0716 临时值提前释放 | `let args` 绑定延长生命周期 |
| E20 | 档位初始化绑定被同名字符串误判已存在而跳过 | 换 init 段特有字符串作幂等判据，补插复验 |

028 三项开服器功能仍按「只记文档」零实现。未做：UI 实现、真实运行时 / GUI / 跨平台构建、launcher / lightweight 业务模块替换、CF F17、特殊版代码、本项目 LICENSE、后端仓写请求。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '151. docs/verification/round-031.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '151. docs/verification/round-031.md\n152. docs/spec/32-round-032-instructions.txt\n153. docs/decisions/032-user-selectable-tiers.md\n154. docs/rules/auto-command-policy.md\n155. docs/licenses/log-LICENSE-MIT.txt\n156. docs/verification/round-032.md\n\n读取命令：', 1)
    t = t.replace('docs/verification/round-031.md; do printf',
                  'docs/verification/round-031.md docs/spec/32-round-032-instructions.txt docs/decisions/032-user-selectable-tiers.md docs/rules/auto-command-policy.md docs/licenses/log-LICENSE-MIT.txt docs/verification/round-032.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 032 |', p.read_text(), count=1)
section = '''

## 032 用户可选松档，日志门面换 log crate

031 的最严格口径保留为**默认档**，设置里新增「宽严程度」三张档位卡：严格（每次问 + 只记录）/ 标准（记录免问 + 五类逐项）/ 宽松（授权一次后自动 + 全可开）。切档只能用户本人做，二次确认列清差异与风险，随时「恢复严格」；插件、更新、重置都不能替用户放宽。C5 外传永远二次确认且默认脱敏。规则全文见 `docs/rules/auto-command-policy.md`。

`core/log.rs` 的自写 `push` / `flush` 全删，换成 `log 0.4.35` 的 `Log` trait；`diagnostics.rs` 新增 `emit`。零传递依赖，`Cargo.lock` 11 包 / 10 第三方，`cargo test --offline` 153/0。

顺带把 031 分组里 27 处「中文当 i18n key」改成 `auto.*` 语义 key 并补英文条目。
'''
if '## 032 用户可选松档' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

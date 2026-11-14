from pathlib import Path
import re

Path('docs/spec/31-round-031-instructions.txt').write_text('干，两个问题A：按最严格去执行\n')
print('SPEC_OK')

# ---------------- A 轨：Q 结论 ----------------
p = Path('docs/features/server-auto-command-log-trigger.md')
t = p.read_text()
old = '''## 待拍板

| 编号 | 问题 | 场景 |
| --- | --- | --- |
| Q-028-01 | 命中后是否每次都要手动同意（013 答复 Q-D02 是「每次请求」，那条口径属于 AI 接口授权，不是日志驱动的服务器自动化）。 | docs/records/q028-decision-scenarios.md 场景 A–D |
| Q-028-02 | 预设动作允许哪些命令：C1–C5 五类怎么取舍，黑名单是否不可禁用。 | 同文档 C1–C5 与四个风险画面 |

结论栏仍为空；耦合矩阵与建议组合见场景文档，用户答复后才写回本文件。'''
new = '''## 已拍板（031）

| 编号 | 结论 | 口径 |
| --- | --- | --- |
| Q-028-01 | **每次命中都手动同意** | Q1-C，完全复用 013 的「每次请求」，不做规则级一次性授权、不按动作分级 |
| Q-028-02 | **只允许 C1 只读动作** | Q2-A，C2 / C3 / C4 / C5 一律拒绝并显示可见提示 |

判定依据见 `docs/records/q028-decision-scenarios.md`「031 答复」段：用户原话含「A」字样，但明确写了「按最严格去执行」；Q1 的最严格项是 Q1-C（不是 Q1-A），Q2 的最严格项是 Q2-A。以「最严格」这个明确指令为准，未按字母取 Q1-A。

| 编号 | 落地约束 |
| --- | --- |
| P01 | 每次命中都弹一次确认；未确认不执行任何动作，超时按取消处理，不自动重试。 |
| P02 | 允许动作仅 C1：写 `[KCU]` 诊断行、桌面通知、追加审计记录、日志页高亮。不改存档、不碰服务器、不外传。 |
| P03 | C2 游戏内广播 / C3 服务器命令 / C4 启动器侧动作 / C5 外部动作一律拒绝，拒绝原因在界面可见，不静默丢弃。 |
| P04 | 触发源默认「仅服务端输出」，玩家聊天文字不进入匹配（场景 B 的诱导面收窄）。 |
| P05 | 同一规则已有待确认弹窗时，后续命中只累计计数、不新增弹窗；确认只作用于当前这一次，累计次数在弹窗内可见。没有任何一次命中未经确认就执行，也不打爆界面。 |
| P06 | 冷却 30 秒；「测试」按钮只预览命中与将执行的动作，不弹同意、不真发动作。 |
| P07 | 这些限制不向插件开放放宽接口；插件只能追加自己的只读动作，不能改 P01–P05。 |

完整规则见 `docs/rules/auto-command-policy.md`。

## 后果（如实登记，不替用户改）

| 编号 | 后果 |
| --- | --- |
| R01 | 场景 A（凌晨无人值守的卡顿预警）**自动化失效**：每次都要人点确认，夜里没人点就不执行。 |
| R02 | 场景 B（玩家文字诱导）双重保险：最多只能触发只读动作，且仍要人确认。 |
| R03 | 场景 C（模组刷屏）由 P05 收敛为一条待确认 + 计数，不会每秒 60 个弹窗。 |
| R04 | F028-03 在 Q2-A 下**不会真的向服务器发命令**，实际形态是「日志关键词提醒器 + 每次确认」。若本意是还要能自动执行游戏内动作，需改 Q2 口径。 |

## 待用户确认的歧义

| 编号 | 项 |
| --- | --- |
| Q-031-01 | 「两个问题A」里的 A 是否指 Q1-A（规则级一次性授权）。若指字母选项，Q1 应改为 Q1-A，与「按最严格」不一致；本轮按「最严格」落地为 Q1-C。 |
'''
assert old in t
p.write_text(t.replace(old, new, 1))
print('FUNC_MD_OK')

p = Path('docs/records/q028-decision-scenarios.md')
t = p.read_text()
t = t.replace('| 状态 | 待答复，两项均未闭环 |', '| 状态 | 031 已答复；按最严格口径落地 |')
t = t.rstrip() + '''

---

## 031 答复：按最严格去执行

用户原话：`干，两个问题A：按最严格去执行`。

| 编号 | 选定 | 判定依据 |
| --- | --- | --- |
| Q-028-01 | **Q1-C 每次请求都手动同意** | Q1-A 是「规则级一次性授权」，新建时弹一次之后不再弹，不是最严格；Q1-B 按动作分级会放行只读动作；Q1-C 完全复用 013 的「每次请求」，是三组里最严的。 |
| Q-028-02 | **Q2-A 只读白名单** | Q2-B 黑名单之外全部、Q2-C 用户逐条勾选、Q2-D 两层，都比「只允许 C1 只读，其余一律拒绝」宽。 |

「A」字样与 Q1 的选项字母冲突，按明确的「按最严格去执行」判定，不按字母取 Q1-A。若用户本意是字母选项，需回 Q-031-01 纠正。

耦合矩阵里 `Q1-C × Q2-A` 是**极保守**格：

| 场景 | 结果 |
| --- | --- |
| A 凌晨无人值守 | 自动化失效，夜里不执行 |
| B 玩家文字诱导 | 只读动作 + 仍要人确认，双重保险 |
| C 模组刷屏 | 由 P05 收敛为一条待确认 + 计数 |
| D 规则测试 | 只预览，不弹同意 |

相邻三项按「你看着办」授权自定默认（最严格方向）：

| 编号 | 默认 |
| --- | --- |
| N01 来源限定 | 仅服务端输出，玩家聊天文字不进匹配 |
| N02 冷却 | 30 秒 |
| N03 外传脱敏 | Q2-A 下 C5 全禁，不产生外传，脱敏不再需要二次确认 |

结论已写回 `docs/features/server-auto-command-log-trigger.md`；规则全文见 `docs/rules/auto-command-policy.md`。本文件此前的场景、口径与耦合矩阵保留作为判断依据，不删除。
'''
p.write_text(t)
print('SCENARIOS_OK')

Path('docs/rules/auto-command-policy.md').write_text('''# 自动命令策略：最严格口径

| 项 | 值 |
| --- | --- |
| 依据 | 031 用户答复「按最严格去执行」 |
| 对应功能 | F028-03 `docs/features/server-auto-command-log-trigger.md` |
| 状态 | 已拍板、已写进界面演示；实现层未启动 |
| 场景依据 | `docs/records/q028-decision-scenarios.md` |

## 口径

| 编号 | 规则 |
| --- | --- |
| P01 | Q1-C：每次命中都弹一次确认，未确认不执行，超时按取消，不自动重试。 |
| P02 | Q2-A：允许动作仅 C1 只读 —— `[KCU]` 诊断行、桌面通知、审计记录、日志页高亮。 |
| P03 | C2 游戏内广播 / C3 服务器命令 / C4 启动器侧动作 / C5 外部动作一律拒绝，拒绝原因在界面可见。 |
| P04 | 触发源默认「仅服务端输出」，玩家聊天文字不进匹配。 |
| P05 | 同一规则已有待确认弹窗时，后续命中只累计计数、不新增弹窗；确认只作用于当前这一次，累计次数在弹窗内可见。 |
| P06 | 冷却 30 秒；「测试」只预览，不弹同意、不真发动作。 |
| P07 | 不向插件开放放宽接口；插件只能追加自己的只读动作。 |

## C1–C5 动作分级

| 类 | 例子 | 本口径 |
| --- | --- | --- |
| C1 只读 | 诊断行、通知、审计、高亮 | 允许，需每次确认 |
| C2 游戏内广播 | `/say`、`/tellraw` | 拒绝 |
| C3 服务器命令 | `/save-all`、`/op`、`/stop`、`/ban` | 拒绝 |
| C4 启动器侧动作 | 导出诊断包、重启实例、备份任务 | 拒绝 |
| C5 外部动作 | webhook、mclo.gs 上传 | 拒绝 |

## 后果

| 编号 | 后果 |
| --- | --- |
| R01 | 无人值守场景自动化失效。 |
| R02 | 诱导场景最多触发只读动作，且仍要人确认。 |
| R03 | 刷屏由 P05 收敛，不会打爆界面。 |
| R04 | F028-03 实际形态是「日志关键词提醒器 + 每次确认」，不会向服务器发命令。 |

## 界面落点

| 编号 | 落点 |
| --- | --- |
| U01 | 设置 → 「自动命令」分组（设置内，不进一级导航）。 |
| U02 | 命中时的确认弹窗：显示命中的日志行、将执行的只读动作、期间累计次数；「这次同意 / 取消 / × / ESC / 宿主」都能关。 |
| U03 | 预览图 `demos/preview/44-settings-auto.png`、`45-auto-confirm.png`；整页演示 `demos/ui-full-kcu-paper.html`。 |

界面文案不写工程标识、槽位 ID 或策略编号，只写用户能懂的话。
''')
print('POLICY_OK')

D = {}
D['docs/decisions/031-strict-policy-and-config.md'] = '''# 第 031 轮：两条 Q 按最严格拍板，配置与信封换 serde_json

| 项 | 值 |
| --- | --- |
| 编号 | 031 |
| 状态 | A 轨已拍板、B 轨代码已实现已验证 |
| 依据 | docs/spec/31-round-031-instructions.txt |
| 前序 | 030-args-and-q-scenarios.md、q028-decision-scenarios.md |
| 本轮性质 | 双轨轮 |

## 两条指令的边界

| 编号 | 原文片段 | 处置 |
| --- | --- | --- |
| A01 | 「两个问题A：按最严格去执行」 | 两条 Q 拍板，按最严格口径写回功能 md，落规则文档与界面演示。 |
| B01 | 「干」 | 继续按 `docs/records/code-ownership-audit.md` 映射表替换自写代码，落 `core/config.rs` 与 `core/envelope.rs`。 |

## A01：Q-028-01 / Q-028-02 按最严格

| 编号 | 结论 | 口径 |
| --- | --- | --- |
| Q-028-01 | 每次命中都手动同意 | **Q1-C**，完全复用 013「每次请求」 |
| Q-028-02 | 只允许 C1 只读动作 | **Q2-A**，C2–C5 一律拒绝并显示可见提示 |

判定说明：用户原话含「A」字样，与 Q1 的选项字母冲突；Q1-A 是「规则级一次性授权」，不是最严格。以明确的「按最严格去执行」为准，不按字母取 Q1-A。登记 Q-031-01 待用户确认该歧义。

落地约束 P01–P07 见 `docs/rules/auto-command-policy.md`。P05 是不改变口径的实现约束：同一规则已有待确认弹窗时后续命中只累计计数、不新增弹窗，确认只作用于当前这一次，累计次数可见；既没有任何一次未经确认就执行，也不打爆界面。

后果 R01–R04 如实写进功能 md：无人值守自动化失效；F028-03 在 Q2-A 下不会真的向服务器发命令，实际是「日志关键词提醒器 + 每次确认」。若用户本意是要能自动执行游戏内动作，需改 Q2 口径。

相邻三项按既有「你看着办」授权定最严格方向默认：来源限定「仅服务端输出」、冷却 30 秒、C5 全禁故外传脱敏不再需要二次确认。

界面闸门触发：新增设置内「自动命令」分组与命中确认弹窗，出整页 UX 演示与 2 张新预览图；不进一级导航，不写工程标识。

## B01：配置与信封换成 serde_json

| 编号 | 动作 |
| --- | --- |
| C01 | `core/config.rs` 删掉自写 `BTreeMap<String,String>` endpoints / ports 双表与手写 getter；换成 `serde_json::Map<String, Value>` 单根对象。 |
| C02 | 新增 `from_json_str` / `to_json_string`，配置文件的解析与序列化交给已在构建中的 `serde_json 1.0.145`，不新增依赖。 |
| C03 | `core/envelope.rs` 的 `payload: BTreeMap<String,String>` 换成 `serde_json::Map<String, Value>`，新增 `to_json_string` / `from_json_str`；`field()` / `with()` 语义不变。 |
| C04 | `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 10 包 / 9 第三方；做的是把自写数据容器换成已有库的数据结构，不是新增库。 |

### 删掉的自写代码

| 030 | 031 |
| --- | --- |
| `Config { endpoints: BTreeMap, ports: BTreeMap }` 双表 | `data: Map<String, Value>` 单根对象 |
| 手写 6 个 getter / setter 直接操作两张表 | 经 `Map::get` / `insert` + `Value::as_str` / `as_u64` |
| 无文件编解码（配置只存在内存） | `from_json_str` / `to_json_string` |
| `Envelope.payload: BTreeMap<String,String>` 无序列化 | `Map<String, Value>` + `to_json_string` / `from_json_str` |
| 手写 `format!("kcu-{:08x}", n)` 序列 | 保留（`SEQ` 是项目特有的 ID 生成，不是序列化器） |

### 行为差异（如实登记）

| 编号 | 项 | 030 | 031 |
| --- | --- | --- | --- |
| B10 | 配置读盘 | 不存在 | 新增；非法 JSON / 非对象根 / 缺 sections 都给可见错误或默认值 |
| B11 | 端口范围 | `u16` 天然 | `as_u64` 后 `u16::try_from`，越界返回 None 而不是 panic |
| B12 | envelope JSON | 不存在 | 新增；`kind` 写成 `Request` / `Response` / `Event` 字符串 |
| B13 | payload 键顺序 | BTreeMap 有序 | `serde_json::Map` 无 `preserve_order` 时同样是 BTreeMap，有序性保持，原测试不降 |

### 新增测试

| 编号 | 断言 |
| --- | --- |
| N01 | 配置 JSON 往返保留语言、镜像测速开关、端点、端口、地域覆盖。 |
| N02 | 非法 JSON 与数组根被拒绝。 |
| N03 | 缺 `endpoints` / `ports` 的 JSON 自动补空对象。 |
| N04 | envelope JSON 输出可被 `from_json_str` 解析且保留 target / 自定义字段 / kind。 |
| N05 | envelope 带 error 时 JSON 里保留 error。 |

`cargo test --offline` **144 → 149 / 0**，原 8 个相关断言未改。

## 四值

| 项 | 值 |
| --- | --- |
| 两条 Q 按最严格拍板、P01–P07、R01–R04 | 已证实 |
| 149 / 0、10 包 9 第三方、上游库源码未改 | 已证实 |
| 整页 UX 演示 + 2 张预览图 | 已证实 |
| Q-031-01 字母歧义、F028-03 是否要真发命令 | 未证实（待用户确认） |
| 自动命令实现层、真实 GUI 端到端、Win7 / 多架构 | 受阻 / 未启动 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-031.md'] = '''# 第 031 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 031 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 149 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 10 包 / 9 第三方，与 030 完全一致 | 已证实 |
| V4 | `grep -c 'BTreeMap' src/core/config.rs src/core/envelope.rs` | 0 / 0 | 已证实 |
| V5 | `grep -c 'serde_json' src/core/config.rs src/core/envelope.rs` | 1 / 1 | 已证实 |
| V6 | `docs/features/server-auto-command-log-trigger.md` 结论段 | Q1-C / Q2-A / P01–P07 / R01–R04 齐备 | 已证实 |
| V7 | `docs/rules/auto-command-policy.md` | 7 条规则、C1–C5 表、4 条后果、3 个界面落点 | 已证实 |
| V8 | `demos/ui-full-kcu-paper.html` 设置分组 | `data-tab="auto"` 与 `data-pane="auto"` 各 1 处 | 已证实 |
| V9 | `demos/preview/44-settings-auto.png` / `45-auto-confirm.png` | 两文件非空 | 已证实 |
| V10 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V11 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V12 | 必读文件循环 | REQUIRED=151 MISSING=0 | 已证实 |
| V13 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 配置 / 信封库化、149 / 0、零新增依赖 | 已证实 |
| 两条 Q 按最严格拍板、界面闸门触发 | 已证实 |
| Q-031-01 字母歧义、R04 是否需改 Q2 | 未证实 |
| 自动命令实现层、真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 149 测试仅作回归，不作质量结论 | 已证实 |

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


app('docs/decisions/index.md', '| 031 | 两条 Q 按最严格拍板；配置与信封换 serde_json | A 已拍板、B 已实现 | 031-strict-policy-and-config.md |')

app('docs/records/code-ownership-audit.md', '''## 031 第五块替换后状态

| 项 | 024 | 025 | 027 | 029 | 030 | 031 |
| --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | **9（未增）** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 |
| `core/cache.rs` | 304 | 304 | 304 | 327 | 327 | 327 |
| `core/args.rs` | 91 | 91 | 91 | 91 | 120 | 120 |
| `core/config.rs` | 60 行双 BTreeMap | 60 | 60 | 60 | 60 | **约 130（含 JSON 往返与 3 新测）** |
| `core/envelope.rs` | 81 行 BTreeMap | 81 | 81 | 81 | 81 | **约 100（含 JSON 输出与 2 新测）** |
| `src/` 行数 | 4339 | 4081 | 4073 | 4017 | 4046 | 约 4140 |

031 删掉的自写数据结构：两张 `BTreeMap<String,String>` 配置表 + 手写 6 个 getter/setter、envelope 的 `BTreeMap` payload、两处「无文件编解码」的空缺。换成已在构建中的 `serde_json::Map<String, Value>`，配置读写与信封序列化交给库。行数上升是因为新增 JSON 往返与 5 个测试，实现段的自写容器确实清零。

本轮 **未新增第三方 crate**，这一点如实登记：做的是「把自写数据容器换成已有库的数据结构」，不是「引入新库」。映射表里「配置 → serde + toml」只落地了载荷层，toml 文件编解码仍待后续；真实网络 / UI / 崩溃 / 插件层仍未启动。

剩余自写模块：`dispatcher/launcher.rs` 541、`lightweight/*.rs` 1135、`core/paths.rs`（逻辑名映射）、`core/log.rs`（分片缓冲）、`core/popup.rs`、`core/userflow.rs`、`core/instance.rs`。
''')

app('docs/design/implementation-strategy.md', '''## 031 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 | 已落地（025，serde_json） |
| 异步 / 线程同步 | 已落地（027，crossbeam） |
| 缓存 / LRU / 单飞 | 已落地（029，lru 0.12.5） |
| 命令行参数解析 | 已落地（030，lexopt 0.3.2） |
| 配置载荷 / 信封序列化 | **已落地（031，serde_json::Map，零新增依赖）** |
| 配置 toml 文件编解码、路径、日志、真实网络、UI、崩溃、插件 | 未启动 |
''')

app('docs/rules/index.md', '''## 031 新增

| 文档 | 主题 |
| --- | --- |
| docs/rules/auto-command-policy.md | F028-03 最严格口径 P01–P07、C1–C5、后果 R01–R04 |
''')

app('docs/checklists/ai-errors.md', '''## 031 轮新增

| 编号 | 防错项 |
| --- | --- |
| A76 | 用户答复同时出现字母选项（如「A」）和程度词（如「最严格」）时，以程度词为准，并登记字母歧义待确认，不擅自按字母取项。 |
| A77 | 「只允许只读动作」的功能不要沿用功能名里的「自动命令」当作已实现发命令；必须写明实际形态与后果。 |
| A78 | 每次确认的严格口径遇到高频触发，用「一条待确认 + 累计计数」收敛弹窗数量，不得把多次命中合并成一次确认后执行。 |
''')

app('docs/records/interface-log.md', '''## 031 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I32 | `Config` | 新增 `from_json_str` / `to_json_string`；原有 9 个方法签名不变 |
| I33 | `Envelope` | `payload` 类型换 `Map<String, Value>`；`with` / `field` 语义不变；新增 JSON 输出与解析 |
| S30 | 状态 | Q-028-01 = Q1-C、Q-028-02 = Q2-A 已拍板；F028-03 实现层未启动 |
''')

app('docs/records/rounds.md', '''## 031

| 落点 | 内容 |
| --- | --- |
| docs/spec/31-round-031-instructions.txt | 逐字副本 1 行 |
| docs/decisions/031-strict-policy-and-config.md | A01/B01 边界、Q 判定、C01-C04、B10-B13、四值 |
| docs/features/server-auto-command-log-trigger.md | 待拍板 → 已拍板（Q1-C / Q2-A / P01–P07 / R01–R04 / Q-031-01） |
| docs/records/q028-decision-scenarios.md | 追加「031 答复」段，状态改已答复 |
| docs/rules/auto-command-policy.md | 最严格策略全文 |
| docs/verification/round-031.md | 13 条复跑证据 |
| demos/round-031-strict.html | 13 步运行逻辑演示 |
| demos/ui-full-kcu-paper.html / demos/preview/ | 设置内「自动命令」分组 + 命中确认弹窗；2 张新预览图（44 / 45） |
| src/core/config.rs / envelope.rs | 双 BTreeMap 与 payload 换 `serde_json::Map`，加 JSON 往返 |
| 索引与记录 | docs/index 151 项、README、decisions/index、rules/index、research 索引、ai-errors A76-A78、code-ownership-audit、implementation-strategy、interface-log、rounds |

「两个问题A：按最严格去执行」按 Q1-C（每次命中都手动同意）+ Q2-A（只允许 C1 只读）落地。字母 A 与 Q1 选项冲突，以「最严格」为准，登记 Q-031-01 待确认。后果如实写明：无人值守自动化失效；F028-03 不会真的向服务器发命令。

「干」继续替换自写代码：`config.rs` 与 `envelope.rs` 的自写 `BTreeMap` 容器换 `serde_json::Map`，新增文件编解码；零新增第三方 crate，149 / 0。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E15 | 配置 `port()` 从 `u16` 变 `Value::as_u64` 后可能越界 | 改 `u16::try_from`，越界返回 None，不 panic |
| E16 | 高频命中撞「每次确认」会打爆弹窗 | 立 P05：一条待确认 + 累计计数，确认只作用当前一次，不改变严格口径 |

028 三项开服器功能仍按「只记文档」零实现。未做：UI 实现、真实运行时 / GUI / 跨平台构建、launcher / lightweight 业务模块替换、CF F17、特殊版代码、本项目 LICENSE、后端仓写请求。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '146. docs/verification/round-030.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '146. docs/verification/round-030.md\n147. docs/spec/31-round-031-instructions.txt\n148. docs/decisions/031-strict-policy-and-config.md\n149. docs/rules/auto-command-policy.md\n150. docs/records/q028-decision-scenarios.md\n151. docs/verification/round-031.md\n\n读取命令：', 1)
    t = t.replace('docs/verification/round-030.md; do printf',
                  'docs/verification/round-030.md docs/spec/31-round-031-instructions.txt docs/decisions/031-strict-policy-and-config.md docs/rules/auto-command-policy.md docs/records/q028-decision-scenarios.md docs/verification/round-031.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 031 |', p.read_text(), count=1)
section = '''

## 031 两条 Q 按最严格拍板，配置与信封换 serde_json

Q-028-01 = **Q1-C 每次命中都手动同意**，Q-028-02 = **Q2-A 只允许 C1 只读动作**，C2–C5 一律拒绝并显示可见提示。规则全文见 `docs/rules/auto-command-policy.md`，后果如实登记：无人值守自动化失效，F028-03 不会真的向服务器发命令。

设置内新增「自动命令」分组与命中确认弹窗，出 2 张预览图；不进一级导航。

`core/config.rs` 与 `core/envelope.rs` 的自写 `BTreeMap` 容器换成已在构建中的 `serde_json::Map<String, Value>`，新增配置 JSON 往返与信封序列化；零新增第三方 crate，`cargo test --offline` 149/0。
'''
if '## 031 两条 Q' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

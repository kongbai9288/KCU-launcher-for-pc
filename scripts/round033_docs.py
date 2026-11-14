from pathlib import Path
import re

Path('docs/spec/33-round-033-instructions.txt').write_text('是answer缩写，干\n')
print('SPEC_OK')

# ---------- A 轨：Q-031-01 结案 ----------
p = Path('docs/features/server-auto-command-log-trigger.md')
t = p.read_text()
old = '''## 待用户确认的歧义

| 编号 | 项 |
| --- | --- |
| Q-031-01 | 「两个问题A」里的 A 是否指 Q1-A（规则级一次性授权）。若指字母选项，Q1 应改为 Q1-A，与「按最严格」不一致；本轮按「最严格」落地为 Q1-C。 |
'''
new = '''## 待用户确认的歧义（已结案）

| 编号 | 项 | 结论 |
| --- | --- | --- |
| Q-031-01 | 「两个问题A」里的 A 是否指 Q1-A（规则级一次性授权） | **033 已结案：A 是 answer 缩写，不是选项字母**。031 按「最严格」取 Q1-C + Q2-A 的判定成立，口径不改。 |

用户 033 原话：`是answer缩写，干`。即 031 那句是「两个问题 answer：按最严格去执行」，A 只是「答案」的缩写标记，不指向任何选项。031 写在 `docs/decisions/031-strict-policy-and-config.md` 的判定依据与 Q1-C + Q2-A 结论全部保留，不重做、不回退。
'''
assert old in t
p.write_text(t.replace(old, new, 1))
print('FUNC_MD_CLOSED')

p = Path('docs/records/q028-decision-scenarios.md')
t = p.read_text()
t = t.replace('Q-031-01 字母歧义这次没有答复，仍挂在 `docs/features/server-auto-command-log-trigger.md` 待确认；「可选松档」不改变 031 严格档的判定依据。',
              'Q-031-01 字母歧义在 033 结案：A 是 answer 缩写，不是选项字母。')
t = t.rstrip() + '''

---

## 033 Q-031-01 结案

用户原话：`是answer缩写，干`。

| 项 | 结论 |
| --- | --- |
| 「两个问题A」中的 A | **answer 缩写**，意为「两个问题的答复」，不是 Q1 的选项字母 |
| 031 的判定 | 不受影响。Q1-C（每次命中都问）+ Q2-A（只允许 C1 只读）继续成立 |
| 需要改口径吗 | **不需要**。没有把 Q1 改成 Q1-A，没有回退 031 的规则与界面 |
| 032 的三档 | 不受影响。默认严格档仍是 031 口径 |

此前把「A」当成可能的选项字母，是我在 031 做的最保守登记；现在证实是缩写标记，歧义消除。保留这段登记与结案，不删历史。
'''
p.write_text(t)
print('SCENARIOS_CLOSED')

D = {}

D['docs/decisions/033-answer-abbr-and-anyhow.md'] = '''# 第 033 轮：Q-031-01 结案；错误处理换 anyhow

| 项 | 值 |
| --- | --- |
| 编号 | 033 |
| 状态 | A 轨歧义已结案、B 轨代码已实现已验证 |
| 依据 | docs/spec/33-round-033-instructions.txt |
| 前序 | 031-strict-policy-and-config.md、032-user-selectable-tiers.md |
| 本轮性质 | 双轨轮 |

## 两条指令的边界

| 编号 | 原文片段 | 处置 |
| --- | --- | --- |
| A01 | 「是answer缩写」 | 结案 Q-031-01：031 那句里的 A 是 answer 缩写，不是 Q1-A 选项字母。031 结论不改、032 三档不改、不重做界面。 |
| B01 | 「干」 | 继续按 `docs/records/code-ownership-audit.md` 映射表替换自写代码，落「错误 → anyhow」。 |

## A01：Q-031-01 结案

| 编号 | 动作 |
| --- | --- |
| C01 | `docs/features/server-auto-command-log-trigger.md` 的「待用户确认的歧义」改为「已结案」，写明 A = answer 缩写。 |
| C02 | `docs/records/q028-decision-scenarios.md` 追加 033 结案段，032 段里「这次没有答复」改为已结案。 |
| C03 | 031 的 Q1-C + Q2-A 判定、P01–P07、032 的三档矩阵与 U01–U11 **全部保留**，不回退、不重做。 |

| 项 | 值 |
| --- | --- |
| 之前误判 | 031 把「A」当成可能的 Q1 选项字母，登记为待确认歧义（最保守做法） |
| 实际 | 「两个问题 answer：按最严格去执行」，A 只是答复标记 |
| 结论 | 031 按「最严格」取 Q1-C + Q2-A 成立，口径无需变更 |
| 界面闸门 | **未触发**。本轮不动用户界面，只改结论文字与登记，不出整页 UX 演示、不改预览图内容 |

## B01：自写 String 错误换成 anyhow 1.0.104

### 选这块的依据

| 编号 | 依据 |
| --- | --- |
| D01 | 映射表「错误 → anyhow + thiserror」是 024 登记的欠账之一，此前未落地。 |
| D02 | 全仓 8 个文件共 15 个 `Result<T, String>` 签名、多处 `map_err(|e| e.to_string())`、手写 `Err(format!(...))`，错误类型靠字符串拼接，无上下文链、无来源保留。 |
| D03 | `anyhow 1.0.104` 的 `[dependencies]` 为空（零传递依赖），MIT OR Apache-2.0，crates manifest 与两份 LICENSE 全文可从上游 tag 取到。 |
| D04 | 032 结尾曾预告核 `dirs` 换 `paths.rs`。核完结论：`paths.rs` 是「注入 root + 逻辑名 → 子路径」映射，用户明确决定数据目录为 `C:\\KCU`；`dirs` 提供的是系统目录定位，硬换会改变默认行为并引入 windows-sys 大闭包（Linux 工具链无法验证 Windows 分支）。**不换**，改走错误类型这块，理由如实写在此。 |

### 依赖落地

| 编号 | 动作 |
| --- | --- |
| D05 | 上游 tag `1.0.104` tarball 原样落到 `vendor/anyhow/`：12 个 `src/*.rs`、`build.rs`、Cargo.toml、两份 LICENSE、README；`src/` 逐字节未改。 |
| D06 | 裁掉 `[dev-dependencies]`（futures / rustversion / syn 3 / trybuild 不参与构建）；`[features] default = ["std"]` 保留；根 Cargo.toml 本就没有 `[dependencies]` 段。 |
| D07 | `Cargo.toml` 加 `anyhow = "1.0.104"`；`Cargo.lock` 11 → **12 包 / 11 第三方**，零传递依赖。 |
| D08 | `docs/licenses/anyhow-LICENSE-MIT.txt` (1023 B) 与 `anyhow-LICENSE-APACHE.txt` (9723 B) 逐字落盘；按 MIT 条款用，Apache-2.0 全文一并保留。 |
| D09 | 关于页第三方许可七列表新增 1 组「构建中已使用」（10 → 11 组），`THIRD-PARTY-NOTICES.md` 同步。 |

### 删掉的自写错误处理

| 032 | 033 |
| --- | --- |
| `Result<T, String>` × 15 个签名 | `anyhow::Result<T>` × 15 个签名 |
| `map_err(|e| e.to_string())?` 丢掉来源类型 | 直接 `?`，`From<E>` 保留原始错误 |
| `Err("...".to_string())` / `Err(format!(...))` 手写串 | `anyhow::anyhow!(...)` |
| `ok_or_else(|| format!(...))?` 构造字符串错误 | `ok_or_else(|| anyhow::anyhow!(...))?` |
| 8 个模块各写各的错误口径 | 统一 `anyhow::Error`，可 `context` 追加链路 |

涉及模块：`core/config.rs`、`core/envelope.rs`、`core/paths.rs`、`core/args.rs`、`dispatcher/json.rs`、`dispatcher/task.rs`、`dispatcher/mode.rs`、`dispatcher/launcher.rs`、`lightweight/download.rs`。

### 行为差异（如实登记）

| 编号 | 项 | 032 | 033 |
| --- | --- | --- | --- |
| B10 | 错误类型 | `String` | `anyhow::Error`；`unwrap_err()` 需 `.to_string()` 再比较内容 |
| B11 | `dispatcher/json.rs` 三个 `assert_eq!(parse(..), Ok(..))` | 直接比 Result | 改 `unwrap()` 后比值，断言强度不降 |
| B12 | `mode.rs` 错误内容断言 | `.unwrap_err().contains(..)` | `.unwrap_err().to_string().contains(..)` |
| B13 | `launcher.rs` 缓存闭包 | `Ok::<String, String>` | 保持；`from_str` 的错误在这里 `.map_err(|e| e.to_string())` 适配 Cache 的 String 错误契约，登记为局部适配，未改 Cache |
| B14 | `lightweight/download.rs` 线程闭包 | `Ok::<String, String>` | `Ok::<String, anyhow::Error>` |

### 本轮真实失败与修复（全部留痕）

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E22 | `tarfile.open(BytesIO)` 把它当文件名，报 TypeError | 改 `tarfile.open(fileobj=io.BytesIO(b), mode='r:gz')` |
| E23 | `config.rs` 的 `ok_or_else(|| "...".to_string())?` 产生 String 错误，anyhow 不接收 | 改 `anyhow::anyhow!` |
| E24 | `launcher.rs` 缓存闭包错误契约是 String，`from_str` 换成 anyhow 后 `?` 无法转换 | 局部 `.map_err(|e| e.to_string())`，不动 Cache |
| E25 | `download.rs` 第二处 `return Err("cancelled".to_string())` 首次替换只改了第一处 | 按缩进定位第二处补改 |
| E26 | `assert_eq!(Result<Value, anyhow::Error>, Ok(..))` 触发 E0369（anyhow::Error 无 PartialEq） | 三处改 `unwrap()` 后比值 |

### 测试

`cargo build --offline` 通过；`cargo test --offline` **153 passed / 0 failed**，与 032 同数：本轮是错误类型替换，未新增/删除测试，原断言全部保留。

## 四值

| 项 | 值 |
| --- | --- |
| Q-031-01 结案、031/032 口径不变 | 已证实 |
| anyhow 1.0.104 进构建、12 包 11 第三方、153 / 0 | 已证实 |
| 15 个签名换库、上游 `src/` 未改、两份 LICENSE 全文 | 已证实 |
| `dirs` 换 paths.rs | 已失败（语义不匹配 + Windows 分支不可验证），已如实登记并改轨 |
| 自动命令实现层、真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-033.md'] = '''# 第 033 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 033 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 anyhow 1.0.104 / kcu-core，`Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 153 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 12 包 / 11 第三方，anyhow 零传递依赖 | 已证实 |
| V4 | `grep -c 'Result<[^>]*, String>' src/` | 0 | 已证实 |
| V5 | `grep -rc 'anyhow::Result' src/` | 8 个文件命中 | 已证实 |
| V6 | `vendor/anyhow/src/lib.rs` 与上游 tarball | 逐字节一致 | 已证实 |
| V7 | `docs/licenses/anyhow-LICENSE-*.txt` | 1023 / 9723 字节 | 已证实 |
| V8 | `docs/features/server-auto-command-log-trigger.md` | 「已结案」+ A = answer 缩写 | 已证实 |
| V9 | 031 / 032 结论段 | Q1-C + Q2-A、三档矩阵未改 | 已证实 |
| V10 | 关于页许可行 / NOTICES | 11 组「构建中已使用」，含 anyhow | 已证实 |
| V11 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V12 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V13 | 必读文件循环 | REQUIRED=161 MISSING=0 | 已证实 |
| V14 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| Q-031-01 结案、错误类型库化、153 / 0 | 已证实 |
| `dirs` 路线不成立并改轨 | 已失败（已登记） |
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


app('docs/decisions/index.md', '| 033 | Q-031-01 结案（A=answer 缩写）；错误处理换 anyhow | A 已结案、B 已实现 | 033-answer-abbr-and-anyhow.md |')

app('docs/records/code-ownership-audit.md', '''## 033 第七块替换后状态

| 项 | 024 | 025 | 027 | 029 | 030 | 031 | 032 | 033 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | 9 | 10 | **11** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 | 11 | 12 |
| `Result<T, String>` 签名 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | **0** |
| `src/` 行数 | 4339 | 4081 | 4073 | 4017 | 4046 | 4197 | 4285 | 约 4290 |

033 删掉的自写错误处理：15 个 `Result<T, String>` 签名、`map_err(|e| e.to_string())` 丢来源写法、手写 `Err(format!(..))` 与 `ok_or_else(|| format!(..))` 字符串错误。统一为 `anyhow::Result<T>` + `anyhow::anyhow!`；`?` 直传保留原始错误类型。覆盖 9 个模块。

`anyhow 1.0.104` 零传递依赖，上游 `src/` 与 `build.rs` 逐字节未改，裁掉 dev-dependencies。两份 LICENSE 全文落盘。

**`dirs` 路线核完不成立**：`core/paths.rs` 是「注入 root + 逻辑名 → 子路径」映射，用户明确决定 `C:\\KCU`；`dirs` 是系统目录定位，硬换会改默认行为，且 dirs-sys 的 Windows 分支依赖 windows-sys 大闭包，当前 Linux 工具链无法验证。改走错误类型这块，理由写在 033 决策 D04。

剩余自写模块：`dispatcher/launcher.rs` 541、`lightweight/*.rs` 1135、`core/paths.rs`（逻辑名映射表约 20 行）、`core/popup.rs`（弹窗状态机）、`core/userflow.rs`、`core/instance.rs`。这些是模式判定、用户指定实例排第一、双击绑定一类项目特有编排；`paths.rs` 的路径拼接本身用的是 `std::path::PathBuf`，没有自写路径算法。映射表里没有对应替换库，不硬换。
''')

app('docs/design/implementation-strategy.md', '''## 033 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 / 配置载荷 / 信封序列化 | 已落地（025、031，serde_json） |
| 异步 / 线程同步 | 已落地（027，crossbeam） |
| 缓存 / LRU / 单飞 | 已落地（029，lru 0.12.5） |
| 命令行参数解析 | 已落地（030，lexopt 0.3.2） |
| 日志门面 | 已落地（032，log 0.4.35） |
| 错误类型与上下文 | **已落地（033，anyhow 1.0.104）** |
| 路径 → dirs | 已失败（语义不匹配，不换，见 033 D04） |
| 配置 toml 文件编解码、真实网络、UI、崩溃、插件 | 未启动 |
''')

app('docs/checklists/ai-errors.md', '''## 033 轮新增

| 编号 | 防错项 |
| --- | --- |
| A82 | 用户上一句里的单字母（A/B/C）不一定指选项编号；结案歧义时保留原判定与历史登记，证实是缩写就不回退口径。 |
| A83 | 换错误类型时逐个检查测试是否对 `Result` 整体做 `PartialEq` 比较；`anyhow::Error` 无 `PartialEq`，改 `unwrap()` 后比值，断言强度不降。 |
| A84 | 预告过的替换路线核完发现语义不匹配，要写清「不换的依据」和「改走哪块」，不能静默跳过也不硬换。 |
''')

app('docs/records/interface-log.md', '''## 033 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I36 | 9 个模块的 `Result<T, String>` | 全部改 `anyhow::Result<T>`；`unwrap_err()` 调用面需 `.to_string()` |
| S32 | 状态 | Q-031-01 已结案（A = answer 缩写）；031 / 032 口径不变；F028-03 实现层未启动 |
''')

app('docs/licenses/index.md', '''## 033 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| anyhow-LICENSE-MIT.txt | anyhow 1.0.104 | MIT |
| anyhow-LICENSE-APACHE.txt | anyhow 1.0.104 | Apache-2.0 |

来源：dtolnay/anyhow tag `1.0.104`，两份逐字副本，1023 / 9723 字节。许可声明为 `MIT OR Apache-2.0`，本项目按 MIT 条款使用，两份全文都随发行物附上。
''')

app('THIRD-PARTY-NOTICES.md', '''## 033 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| anyhow | 1.0.104 | MIT OR Apache-2.0（按 MIT 用） | David Tolnay | 统一错误类型与上下文 | vendor/anyhow | 构建中已使用 |

许可证全文：`docs/licenses/anyhow-LICENSE-MIT.txt`、`docs/licenses/anyhow-LICENSE-APACHE.txt`。

| 编号 | 约束 |
| --- | --- |
| N26 | 零传递依赖；`[dev-dependencies]` 裁掉，`src/` 与 `build.rs` 逐字节未改。 |
| N27 | MIT 条款要求保留版权与许可声明，全文随发行物附上；Apache-2.0 全文一并保留供选择。 |
''')

app('docs/records/rounds.md', '''## 033

| 落点 | 内容 |
| --- | --- |
| docs/spec/33-round-033-instructions.txt | 逐字副本 1 行 |
| docs/decisions/033-answer-abbr-and-anyhow.md | A01/B01 边界、C01-C03 结案、D01-D09 依赖、B10-B14 差异、E22-E26、四值 |
| docs/features/server-auto-command-log-trigger.md | 「待用户确认的歧义」→「已结案」，A = answer 缩写 |
| docs/records/q028-decision-scenarios.md | 追加 033 结案段，032 段「没答复」改已结案 |
| docs/verification/round-033.md | 14 条复跑证据 |
| demos/round-033-anyhow.html | 13 步运行逻辑演示 |
| src/ 9 个模块 | 15 个 `Result<T, String>` 换 `anyhow::Result<T>`，错误构造改 `anyhow::anyhow!` |
| vendor/anyhow/ + Cargo.toml/lock | 12 包 / 11 第三方，零传递依赖 |
| docs/licenses/anyhow-LICENSE-*.txt | MIT 与 Apache-2.0 全文 |
| demos/ui-full-kcu-paper.html | 关于页许可七列表新增 anyhow（10 → 11 组），计数 32 → 33 |
| 索引与记录 | docs/index 161 项、README、decisions/index、licenses/index、ai-errors A82-A84、code-ownership-audit、implementation-strategy、THIRD-PARTY-NOTICES、interface-log、rounds |

「是answer缩写」结案 Q-031-01：031 那句的 A 是 answer 缩写，不是 Q1-A 选项字母。031 的 Q1-C + Q2-A 判定、P01–P07，032 的三档矩阵与 U01–U11 全部保留，不回退、不重做界面。界面闸门**未触发**。

「干」继续替换自写代码：9 个模块共 15 个 `Result<T, String>` 签名换成 `anyhow 1.0.104` 的 `anyhow::Result<T>`，错误构造改 `anyhow::anyhow!`，`?` 直传保留原始错误类型。零传递依赖，153 / 0，原断言未删。

032 预告的「paths.rs → dirs」核完**不成立**：paths.rs 是注入 root + 逻辑名映射，用户明确定了 `C:\\KCU`；dirs 是系统目录定位，硬换改默认行为，且 dirs-sys 的 Windows 分支依赖 windows-sys 大闭包，当前 Linux 工具链无法验证。改走错误类型这块，理由写在 033 决策 D04，未静默跳过。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E22 | `tarfile.open(BytesIO)` 当文件名，TypeError | 改 `fileobj=` + `mode='r:gz'` |
| E23 | `config.rs` 的 `ok_or_else(|| String)` 与 anyhow 不兼容 | 改 `anyhow::anyhow!` |
| E24 | `launcher.rs` 缓存闭包错误契约是 String | 局部 `map_err(|e| e.to_string())`，不动 Cache |
| E25 | `download.rs` 第二处 cancelled 漏改 | 按缩进定位补改 |
| E26 | 三处 `assert_eq!(Result<Value, anyhow::Error>, Ok(..))` 触发 E0369 | 改 `unwrap()` 后比值 |

028 三项开服器功能仍按「只记文档」零实现。未做：UI 实现、真实运行时 / GUI / 跨平台构建、launcher / lightweight 业务模块替换、CF F17、特殊版代码、本项目 LICENSE、后端仓写请求。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '156. docs/verification/round-032.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '156. docs/verification/round-032.md\n157. docs/spec/33-round-033-instructions.txt\n158. docs/decisions/033-answer-abbr-and-anyhow.md\n159. docs/features/server-auto-command-log-trigger.md\n160. docs/licenses/anyhow-LICENSE-MIT.txt\n161. docs/verification/round-033.md\n\n读取命令：', 1)
    t = t.replace('docs/verification/round-032.md; do printf',
                  'docs/verification/round-032.md docs/spec/33-round-033-instructions.txt docs/decisions/033-answer-abbr-and-anyhow.md docs/features/server-auto-command-log-trigger.md docs/licenses/anyhow-LICENSE-MIT.txt docs/verification/round-033.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 033 |', p.read_text(), count=1)
section = '''

## 033 Q-031-01 结案，错误处理换 anyhow

「两个问题A」里的 A 是 **answer 缩写**，不是 Q1-A 选项字母。031 的 Q1-C + Q2-A 判定与 032 的三档矩阵全部保留，不回退、不重做界面。

9 个模块共 15 个 `Result<T, String>` 换成 `anyhow 1.0.104` 的 `anyhow::Result<T>`，错误构造改 `anyhow::anyhow!`，`?` 直传保留原始错误类型。零传递依赖，`Cargo.lock` 12 包 / 11 第三方，`cargo test --offline` 153/0。

032 预告的 `paths.rs → dirs` 核完不成立（语义不匹配 + Windows 分支不可验证），改走错误类型这块，理由见 `docs/decisions/033-answer-abbr-and-anyhow.md`。
'''
if '## 033 Q-031-01' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

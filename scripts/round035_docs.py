from pathlib import Path
import re

Path('docs/spec/35-round-035-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/035-route-check-and-config-hardening.md'] = '''# 第 035 轮：三条路线核完改轨；配置访问换成库的安全 API

| 项 | 值 |
| --- | --- |
| 编号 | 035 |
| 状态 | 三条路线核完不成立（已登记）；改轨代码已实现已验证 |
| 依据 | docs/spec/35-round-035-instructions.txt |
| 前序 | 034-semver-version-matching.md |
| 本轮性质 | 单轨轮；**未新增第三方 crate** |

## 上一轮留下的两步

034 结尾写明：核 `toml` 配置编解码与 `tracing` 日志落地两层有没有零大闭包的通用库可换，闭包过大或 Windows 分支不可验证就如实登记改轨。本轮把这两层连同 024 台账里挂着的 `thiserror` 一起核完。

## 三条路线的一手核查结果

数据来自 api.github.com `contents/Cargo.toml?ref=<tag>`，逐字段统计，不用记忆值。

| 编号 | 路线 | 一手数据 | 判定 |
| --- | --- | --- | --- |
| R01 | `toml-rs/toml v0.25.19` | workspace 根 `edition = "2024"` / `rust-version = "1.85"`；`crates/toml` 有 23 项依赖行，含 `indexmap 2.13`、`winnow 1.0`、`foldhash 0.2`、`serde_core`、`serde_spanned`、`serde_derive`；`toml_edit` 再带一层 `indexmap` + `winnow` | **不成立** |
| R02 | `tokio-rs/tracing`（tag `tracing-subscriber-0.3.23`） | `tracing 0.1.44` 本身只带 `tracing-core 0.1.36` + `pin-project-lite`，但 `tracing-subscriber 0.3.23` 有 33 项依赖行，含 `regex-automata`、`once_cell`、`nu-ansi-term`、`sharded-slab`、`thread_local`、`matchers`、`smallvec` | **不成立** |
| R03 | `dtolnay/thiserror 2.0.21` | `thiserror-impl` 依赖 `proc-macro2 1.0.74` + `quote 1.0.35` + `syn 3`，proc-macro 链 | **不成立** |

### R01 不换的依据

| 编号 | 项 |
| --- | --- |
| R01-A | 项目 `edition = "2021"`，Win7 目标是 Tier 3 + build-std。toml 0.25 的 MSRV 1.85 / edition 2024 在该工具链组合下**未证实**，不能拿当前沙盒 1.99.1 编译通过当成 Win7 可用。 |
| R01-B | `core/config.rs` 当前配置文件是 **JSON**（031 已把两张 BTreeMap 换成 `serde_json::Map`，`from_json_str` / `to_json_string`、插件与设置的读写都按 JSON）。换成 TOML 会改磁盘格式，是行为变更，不是库替换。 |
| R01-C | `indexmap` / `winnow` / `folldhash` / `serde_spanned` 这条闭包在 026 的 mini-moka 尝试里已经证明：离线 vendor 下每多一层就多一处软链 / 恒假 target / feature 引用要裁，且 Windows 分支不可验证。 |

### R02 不换的依据

| 编号 | 项 |
| --- | --- |
| R02-A | 032 已经把 `core/log.rs` 的 `push` / `flush` 换成 `log 0.4.35` 的 `Log` trait，日志门面**已落地**。再叠 `tracing` 是功能重叠，不是删自写代码。 |
| R02-B | 没有 subscriber 就收不到事件；而 `tracing-subscriber` 的 33 项依赖里 `regex-automata` / `sharded-slab` / `thread_local` 在 Win7 Tier 3 下未证实。 |
| R02-C | 真要上结构化诊断，正确做法是给现有 `LogBuffer` 加 subscriber 适配层，且与 `[KCU]` 诊断行格式绑定；格式是硬约束，不在本轮动。 |

### R03 不换的依据

| 编号 | 项 |
| --- | --- |
| R03-A | 逐文件核过：全仓 5 个 `*Error` enum（`RaceError`、`SelectError`、`LoginError`、`CacheError`、`PopupError` 系）**都没有 `Display` / `std::error::Error` 实现**，是纯数据 enum，用 `PartialEq` 断言比较。没有自写样板可删。 |
| R03-B | 引 `thiserror` 只会新增 derive 与 proc-macro 链，不减少任何一行自写代码，属于为引库而引库。 |
| R03-C | 033 已用 `anyhow 1.0.104` 统一了函数返回错误类型；枚举型领域错误保持纯数据更贴合现有断言。 |

## 改轨落地：配置访问换成 serde_json 的安全 API

三条路线都不成立，按 034 结尾的约定改轨到一块**零新依赖、零正常路径行为变更**的真实缺陷修复。

| 编号 | 动作 |
| --- | --- |
| C01 | `core/config.rs` 删除 4 个 `expect("endpoints object")` / `expect("ports object")` 与 2 处 `self.data["endpoints"]` 下标访问。 |
| C02 | 新增 `ensure_object(data, key)`：`entry().or_insert_with()` 后校验 `is_object()`，非对象时归一化为 `Value::Object(Map::new())`；`empty()` 与 `from_json_str()` 共用同一函数，不再各写一份 `or_insert`。 |
| C03 | 4 个私有访问器改成返回 `Option<&Map<..>>`，6 个公开读写方法全部走 `get` / `get_mut` + `as_object` 链，异常输入返回 `None` 或空集合，不再 panic。 |
| C04 | `has_policy_endpoint()` / `endpoint_keys()` 走同一条 Option 链，异常输入分别返回 false / 空 Vec。 |

用的是**已在构建中**的 `serde_json::Map` + `serde_json::Value`（025 落地）与 `anyhow`（033 落地）。`Cargo.toml` / `Cargo.lock` / `vendor/` **一行未动**，仍 13 包 / 12 第三方。

### 修掉的真实缺陷

`from_json_str(r#"{"endpoints":"oops"}"#)` 在 034 版能通过解析，但随后任何 `endpoint()` / `set_endpoint()` 调用都会触发 `Index` 或 `expect` panic。配置来自 `C:\\KCU` 磁盘文件，可能被手工编辑、旧版本残留或插件写坏；在启动路径上 panic 与「让用户舒服」和 Win7 崩溃兜底直接冲突。

| 输入 | 034 | 035 |
| --- | --- | --- |
| 正常 JSON | 正常读写 | 完全一致 |
| `endpoints` 是字符串 / 数组 / null | 后续调用 panic | 归一化为对象，读返回 None，写可恢复 |
| `ports` 是布尔 / 数组 | 后续调用 panic | 同上 |
| 归一化后再 `to_json_string` → `from_json_str` | — | 字段与 policy 前缀仍完整 |

### 测试

`cargo build --offline` 通过；`cargo test --offline` **161 → 164 passed / 0 failed**，新增 3 个（7 → 10）：畸形 endpoints/ports 不 panic、畸形输入后仍可写、归一化后往返不丢字段。原有 7 个 config 测试全部通过，断言未降。

## 024 映射表阶段性收敛

| 层 | 状态 |
| --- | --- |
| JSON 解析 / 配置载荷 / 信封序列化 | 已落地（025、031、035，serde_json） |
| 异步 / 线程同步 | 已落地（027，crossbeam） |
| 缓存 / LRU / 单飞 | 已落地（029，lru 0.12.5） |
| 命令行参数解析 | 已落地（030，lexopt 0.3.2） |
| 日志门面 | 已落地（032，log 0.4.35） |
| 错误类型与上下文 | 已落地（033，anyhow 1.0.104） |
| 版本解析与范围匹配 | 已落地（034，semver 1.0.28） |
| 路径 → dirs | 已失败（033 D04，语义不匹配） |
| 配置 → toml、日志 → tracing、错误枚举 → thiserror | 已失败（035 R01–R03，一手数据） |
| 真实网络 / UI / 崩溃系统 / 插件 ABI / 更新器 | **未启动** |

**口径必须说清**：收敛的是「把自写通用算法换成成熟库」这一项，不是项目做完。`launcher.rs` 547、`lightweight/*.rs` 1135、`core/paths.rs` 76、`popup.rs` 239、`userflow.rs` 196 等仍是项目特有编排（模式优先级、用户指定实例排第一、双击绑定、弹窗必可关、统一信封），没有语义等价的通用库，硬换会改行为。真正还没做的上层能力（UI 宿主、真实网络、崩溃分析、插件 ABI、更新器）依旧标「未启动」，等动到那一层时按 023 的规矩逐项取 LICENSE 全文、登记关于页与 NOTICES 后再引依赖。

## 四值

| 项 | 值 |
| --- | --- |
| R01–R03 一手核查、三条路线均不成立 | 已证实 |
| 4 处 expect + 2 处下标删除、归一化、164 / 0、零新依赖 | 已证实 |
| 正常路径行为一致、异常路径不再 panic | 已证实 |
| 界面闸门 | 未触发（本轮不动界面，关于页许可表仍 12 组 / 34） |
| Win7 Tier 3 + build-std 下 toml MSRV 1.85 | 未证实 |
| 上层能力（UI / 网络 / 崩溃 / 插件）、自动命令实现层 | 未启动 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-035.md'] = '''# 第 035 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 035 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮，未新增第三方 crate，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 164 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 13 包 / 12 第三方，与 034 一致 | 已证实 |
| V4 | `grep -c 'expect(' src/core/config.rs` | 0 | 已证实 |
| V5 | `grep -c 'data\\["' src/core/config.rs` | 0 | 已证实 |
| V6 | `grep -c 'ensure_object' src/core/config.rs` | 5 | 已证实 |
| V7 | `grep -c '#\\[test\\]' src/core/config.rs` | 10（原 7 + 新 3） | 已证实 |
| V8 | R01/R02/R03 上游 manifest 探测 | 三条一手数据均写入 035 决策 | 已证实 |
| V9 | 关于页许可表 / NOTICES | 12 组 / 34，本轮无变更 | 已证实 |
| V10 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V11 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V12 | 必读文件循环 | REQUIRED=171 MISSING=0 | 已证实 |
| V13 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 三条路线核完、改轨缺陷修复、164 / 0、零新依赖 | 已证实 |
| 正常路径行为一致 | 已证实 |
| Win7 Tier 3 下 toml MSRV 1.85、tracing-subscriber 闭包 | 未证实 |
| 上层能力（UI / 网络 / 崩溃 / 插件）、自动命令实现层 | 未启动 |
| 164 测试仅作回归，不作质量结论 | 已证实 |

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


app('docs/decisions/index.md', '| 035 | 三条路线核完改轨；配置访问换 serde_json 安全 API | 改轨已实现 | 035-route-check-and-config-hardening.md |')

app('docs/records/code-ownership-audit.md', '''## 035 映射表阶段性收敛

| 项 | 024 | 025 | 027 | 029 | 030 | 031 | 032 | 033 | 034 | 035 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | 9 | 10 | 11 | 12 | **12（本轮 0 新增）** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 | 11 | 12 | 13 | 13 |
| 测试数 | 141 | 141 | 141 | 141 | 144 | 149 | 153 | 153 | 161 | 164 |

035 核完三条挂账路线，全部不成立：`toml 0.25.19`（edition 2024 / MSRV 1.85 + indexmap/winnow 大闭包 + 会把 JSON 配置改成 TOML）、`tracing`（与已落地 `log` 门面重叠，subscriber 33 项依赖）、`thiserror`（proc-macro 链，且 5 个错误 enum 根本没有 Display/Error 实现可换）。一手 manifest 数据见 035 决策 R01–R03。

改轨落地：`core/config.rs` 删掉 4 处 `expect` 与 2 处下标访问，新增 `ensure_object` 归一化，6 个公开读写方法全走 `serde_json` 的 `get`/`get_mut` + `as_object` 链。修掉「配置文件里 endpoints 被写坏 → 启动路径 panic」这个真实缺陷。用的是已在构建中的 serde_json + anyhow，零新依赖。

**收敛口径**：结掉的是「自写通用算法换成熟库」这一项，不是项目做完。剩余 `launcher.rs` 547、`lightweight/*.rs` 1135、`core/paths.rs` 76、`popup.rs` 239、`userflow.rs` 196 等是项目特有编排（模式优先级、用户指定实例排第一、双击绑定、弹窗必可关、统一信封），无语义等价通用库。UI 宿主、真实网络、崩溃分析、插件 ABI、更新器仍标「未启动」。
''')

app('docs/design/implementation-strategy.md', '''## 035 收敛与剩余

| 层 | 状态 |
| --- | --- |
| L1–L3 通用算法（JSON / 异步 / 缓存 / 参数 / 日志 / 错误 / 版本） | 已全部换成熟库，见 024 台账 |
| 配置 → toml、日志 → tracing、错误枚举 → thiserror | 已失败（035 R01–R03），不重试 |
| 路径 → dirs | 已失败（033 D04） |
| 项目特有编排（dispatcher / lightweight / popup / userflow / paths） | 保留，无语义等价通用库 |
| 上层能力：UI 宿主、真实网络、崩溃分析、插件 ABI、更新器 | **未启动**；动到该层时按 023 逐项取 LICENSE 全文并登记关于页与 NOTICES |
''')

app('docs/checklists/ai-errors.md', '''## 035 轮新增

| 编号 | 防错项 |
| --- | --- |
| A88 | 预告过的库替换路线，要拿上游 manifest 的真实 edition / MSRV / 依赖行数判定，不能用「我记得这个库很小」。 |
| A89 | 换配置格式（JSON → TOML）属于行为变更，不算库替换；磁盘格式与插件读写面都要一起核。 |
| A90 | 引 derive 型库前先数一下自写样板行数；本地 enum 没有 Display/Error 实现时，引 thiserror 不删任何一行。 |
| A91 | 「映射表收敛」只表示自写通用算法换完，不能写成项目做完；上层未启动能力要逐项列清。 |
''')

app('docs/records/interface-log.md', '''## 035 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I38 | `Config` 公开读写方法 | 签名不变；异常输入从 panic 改为返回 None / 空集合 / 归一化 |
| S34 | 状态 | R01–R03 已失败；配置缺陷已修复；F028-03 实现层未启动 |
''')

app('docs/records/rounds.md', '''## 035

| 落点 | 内容 |
| --- | --- |
| docs/spec/35-round-035-instructions.txt | 逐字副本 1 行 |
| docs/decisions/035-route-check-and-config-hardening.md | R01-R03 一手数据、不换依据、C01-C04 改轨、缺陷对照、024 收敛表、四值 |
| docs/verification/round-035.md | 13 条复跑证据 |
| demos/round-035-route-check.html | 13 步运行逻辑演示 |
| src/core/config.rs | 4 处 expect + 2 处下标删除，ensure_object 归一化，新增 3 测试 |
| 索引与记录 | docs/index 171 项、README、decisions/index、ai-errors A88-A91、code-ownership-audit、implementation-strategy、interface-log、rounds |

「干」按 034 结尾的两步走：核 `toml` / `tracing` / `thiserror` 三条挂账路线。三条都拿上游 manifest 一手数据判为**不成立** —— toml 0.25.19 是 edition 2024 / MSRV 1.85 且带 indexmap+winnow 大闭包，还会把现用 JSON 配置改成 TOML；tracing 与 032 已落地的 `log` 门面重叠，subscriber 有 33 项依赖；thiserror 是 proc-macro 链，而本地 5 个错误 enum 根本没有 Display/Error 实现可删。

改轨落地：`core/config.rs` 的 4 处 `expect` 与 2 处 `self.data["..."]` 下标换成 `serde_json` 的 `get`/`get_mut` + `as_object` 链，新增 `ensure_object` 归一化。修掉真实缺陷：配置文件里 `endpoints` 被写坏时，034 版任何读写都会 panic，而配置来自 `C:\\KCU` 磁盘、可能被手工编辑或插件写坏。**零新依赖**，13 包 / 12 第三方不变，`cargo test --offline` 161 → **164 / 0**，原 7 个 config 测试全过。

**024 映射表阶段性收敛**：结掉的是「自写通用算法换成熟库」，不是项目做完。剩余 `launcher.rs` 547、`lightweight/*.rs` 1135、`paths/popup/userflow` 是项目特有编排；UI 宿主、真实网络、崩溃分析、插件 ABI、更新器仍标「未启动」，动到该层时按 023 逐项取 LICENSE 全文并登记关于页与 NOTICES。

界面闸门**未触发**：本轮不动界面，关于页许可表仍 12 组 / 34，预览图未重渲。

028 三项开服器功能仍按「只记文档」零实现。未做：UI 实现、真实运行时 / GUI / 跨平台构建、CF F17、特殊版代码、本项目 LICENSE、后端仓写请求。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '166. docs/verification/round-034.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '166. docs/verification/round-034.md\n167. docs/spec/35-round-035-instructions.txt\n168. docs/decisions/035-route-check-and-config-hardening.md\n169. src/core/config.rs\n170. demos/round-035-route-check.html\n171. docs/verification/round-035.md\n\n读取命令：', 1)
    t = t.replace('docs/verification/round-034.md; do printf',
                  'docs/verification/round-034.md docs/spec/35-round-035-instructions.txt docs/decisions/035-route-check-and-config-hardening.md src/core/config.rs demos/round-035-route-check.html docs/verification/round-035.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 035 |', p.read_text(), count=1)
section = '''

## 035 三条路线核完改轨；配置访问换成库的安全 API

`toml 0.25.19`（edition 2024 / MSRV 1.85 + indexmap/winnow 大闭包 + 会把 JSON 配置改成 TOML）、`tracing`（与已落地的 `log` 门面重叠，subscriber 33 项依赖）、`thiserror`（proc-macro 链，本地错误 enum 没有 Display/Error 可删）三条路线核完均判不成立，一手 manifest 数据见 `docs/decisions/035-route-check-and-config-hardening.md`。

改轨修复：`core/config.rs` 删掉 4 处 `expect` 与 2 处下标访问，新增 `ensure_object` 归一化，读写全走 `serde_json` 的 `get`/`get_mut` + `as_object` 链。配置文件写坏时不再在启动路径 panic。**零新依赖**，`cargo test --offline` 164/0。

024 映射表阶段性收敛：结掉「自写通用算法换成熟库」，不是项目做完；UI 宿主、真实网络、崩溃分析、插件 ABI、更新器仍标未启动。
'''
if '## 035 三条路线' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

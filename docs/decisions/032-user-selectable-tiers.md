# 第 032 轮：用户可选松档，日志门面换 log crate

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
| E21 | 切到宽松档后「命中以后」「这样设置以后」仍显示严格档文案 | 两块改按档位动态渲染，三档各一套文案，补英文条目，重渲 46 / 47 / 48 复核 |

## 四值

| 项 | 值 |
| --- | --- |
| 三档矩阵、U01–U07、3 张预览图、语义 key 27 处 | 已证实 |
| log 0.4.35 进构建、153 / 0、11 包 10 第三方 | 已证实 |
| 上游 `src/` 未改、MIT 与 Apache-2.0 全文落盘 | 已证实 |
| Q-031-01 字母歧义 | 未证实 |
| 自动命令实现层、真实 GUI 端到端、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 后端仓写请求 | 0（已证实） |

## 055 补记：Q-031-01 已由 033 结案

032 第 47 行与第 109 行「Q-031-01 字母歧义 | 未证实」是 032 当时的历史行，按 048 B01 口径**不重写**。

033（`docs/decisions/033-answer-abbr-and-anyhow.md` A01）已结案：A 是 answer 缩写；031 结论、032 三档矩阵与 U01–U07 **全部保留**，不回退、不重做界面。048 C05 台账笔误与 054 结尾错述已在 055 撤回。

口径状态：默认严格档、三档单调、七条不可变边界全部有效；Q-031-01 **已关闭**。由 `scripts/policy_guard.py` G2/G4/G5 守护。

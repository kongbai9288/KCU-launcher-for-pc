# 第 045 轮：锁中毒修复 + 待拍板问题的具体环境

| 项 | 值 |
| --- | --- |
| 编号 | 045 |
| 状态 | 已实现已验证；真实网络 IO、UI、崩溃分析未启动 |
| 依据 | docs/spec/45-round-045-instructions.txt |
| 前序 | 044 quick-xml、026 mini-moka libc 受阻、035 路线核查先例、043/044 推送补验 |
| 本轮性质 | 双轨：① 主交付 = 待拍板问题的具体环境清单；② 「干」= 核一条库化路线 + 修一个真实缺陷 |

## 主交付：具体环境

`docs/records/pending-question-environments.md`，12 条 EQ-01 ~ EQ-12。写法按你的要求：只列 OS 版本、组件版本、运行时条件、一手数据、要选的项、不选的后果；不铺场景，不做类比。覆盖 Win7 UI 三选项、插件哈希口径、真实网络 IO / TLS、崩溃分析、子进程隔离、CF API、特殊版私仓、本项目 LICENSE、028 三项、UX 手感、验证环境受阻事实、本轮路线核查结论。

## 库化路线核查（一手 manifest）

| 编号 | 候选 | 真实数据 | 四值 |
| --- | --- | --- | --- |
| F42 | `parking_lot 0.12.5` | tag **`parking_lot-v0.12.5`**（不是 `0.12.5`）；`MIT OR Apache-2.0` / edition 2021 / MSRV **1.71** / `default = []`；依赖 `parking_lot_core 0.9.12`（path `core`）+ `lock_api 0.4.14`（path `lock_api`） | 已证实 |
| F43 | `lock_api 0.4.14` | `MIT OR Apache-2.0` / MSRV 1.71.0；`[dependencies]` 只有 `scopeguard 1.1.0`（default-features = false）+ 两个 optional（owning_ref / serde）；`default = ["atomic_usize"]` | 已证实 |
| F44 | `parking_lot_core 0.9.12` | `MIT OR Apache-2.0` / MSRV 1.71.0；`[dependencies]` = `cfg-if 1.0.0` + `smallvec 1.6.1` + 两个 optional（petgraph / backtrace）；`[target.'cfg(unix)'.dependencies] libc 0.2.95`；`[target.'cfg(windows)'.dependencies] windows-link 0.2.0`；`deadlock_detection` 才拉 petgraph / backtrace | 已证实 |
| F45 | 已有可复用 | `cfg-if 1.0.5`（038）、`windows-link 0.2.1`（038）已在构建 | 已证实 |
| F46 | libc 通道 | `rust-lang/libc` tag `0.2.177` 可读（`MIT OR Apache-2.0` / edition 2021 / MSRV 1.63），但 026 轮 mini-moka 大闭包已因 libc 受阻；`src/` 平台模块数量大 | 已证实 |

| 编号 | 判定 |
| --- | --- |
| U73 | 只换一个锁实现要拉 6 个新包（parking_lot / core / lock_api / scopeguard / smallvec / libc），其中 unix 分支 libc 是 026 已受阻项。判**不成立**，不重走，不偷偷塞依赖。 |
| U74 | 改轨到标准库提供的 `PoisonError::into_inner`。`src/core/log.rs` 原 4 处 `.expect("log mutex")`：任一线程持锁 panic 后，后续所有日志调用连锁 panic，日志路径会把进程带崩。 |
| U75 | 这一处改动**如实登记为标准库 API 用法修正，不是第三方库替换**，不包装成「全用库」。035 已登记 `LogBuffer` 的分片策略是项目特有编排，无语义等价库可换。 |
| U76 | `Cargo.toml` / `Cargo.lock` / `vendor/` **一行未动**，仍 26 包 / 25 第三方。 |

## 缺陷修复

| 编号 | 动作 |
| --- | --- |
| U77 | `LogBuffer::lock()` 用 `self.inner.lock().unwrap_or_else(PoisonError::into_inner)`；`shard_count` / `pending` / `take_shards` / `Log::log` 四处统一走它。 |
| U78 | 新增 2 个测试，用 `std::thread::scope` 在持锁期间 `panic!` 真的把 Mutex 毒化，再验证中毒后仍能写日志、`take_shards` 能取回、分片与 flush 计数不变。044 版在这两个测试里会 panic。 |
| U79 | `src/core/log.rs` 143 → **187** 行；原 6 个测试一条未改全过。 |

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo test --offline --lib core::log`：**8 / 0**（原 6 + 新 2）。 |
| V-B | `cargo test --offline --lib`：**262 / 0**（044 是 260）。 |
| V-C | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0**、`plugin_abi_load` **6 / 0**。 |
| V-D | 合计 **288 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-E | 必读 229 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，35 份 HTML 脚本与 CI YAML 通过。 |
| V-F | 界面闸门**未触发**：`src/core/log.rs` 不产生界面变化，`demos/preview/` 零 diff，`ui-full-kcu-paper.html` 零 diff。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E79 | parking_lot 的 tag 用 `0.12.5` / `0.12.4` 查 contents 全部 404 | 列真实 tags，锁定 `parking_lot-v0.12.5`；A148 登记 mono-repo tag 前缀要实核（与 042 A 系列同类） |
| E80 | 初版把「换锁」写成第三方库替换 | 回 026 / 035 先例复核后改口径，U75 明确登记为标准库 API 用法修正 |

## 四值

| 项 | 值 |
| --- | --- |
| F42–F46 五条一手事实、U73–U79 落地 | 已证实 |
| EQ-01 ~ EQ-12 十二条具体环境 | 已证实（参数与一手锚点均在库） |
| 288 / 0、Windows GNU、零新增依赖 | 已证实 |
| E79–E80 两个真问题处置 | 已证实 |
| 第三方锁实现 | 未启动（U73 判不成立，EQ-12 挂待选） |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| Q-041 / Q-037-01 / CF F17 / 特殊版代码 / LICENSE / 028 实现 / UX 手感 | 未证实（EQ-01 ~ EQ-10 已给具体环境） |
| 后端仓写请求 | 0（已证实） |

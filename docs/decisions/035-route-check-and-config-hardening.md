# 第 035 轮：三条路线核完改轨；配置访问换成库的安全 API

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

`from_json_str(r#"{"endpoints":"oops"}"#)` 在 034 版能通过解析，但随后任何 `endpoint()` / `set_endpoint()` 调用都会触发 `Index` 或 `expect` panic。配置来自 `C:\KCU` 磁盘文件，可能被手工编辑、旧版本残留或插件写坏；在启动路径上 panic 与「让用户舒服」和 Win7 崩溃兜底直接冲突。

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

## 本轮自查记录

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E30 | 首版文档把 config 测试数写成「原 8 + 新 3 = 11」；回 `git show HEAD:src/core/config.rs` 逐个数得 **原 7 + 新 3 = 10** | 决策、验证报告 V7、rounds、脚本模板统一改成 7 / 10 / 3，断言未动 |
| E31 | `docs/index.md` 自检报 3 处历史重复条目（`demos/preview/index.md`、`docs/records/q028-decision-scenarios.md`、`docs/rules/auto-command-policy.md`） | 属前序轮次已存在的编号重复，非本轮引入；**不重写历史编号**，以免连锁改动读取命令与 REQUIRED 计数，如实登记待单独整理 |

另：本轮界面闸门未触发，关于页许可表仍 12 组 / 34，预览图未重渲；`demos/preview/` 无改动。

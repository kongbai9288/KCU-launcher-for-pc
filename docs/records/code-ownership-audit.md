# 代码归属自查：到底用了多少自己写的代码

| 项 | 值 |
| --- | --- |
| 轮次 | 024 |
| 触发 | 用户「赶快自查，你到底用了多少个自己写的代码……对你的代码没有任何信心」 |
| 性质 | 全量盘点，不改代码、不新增演示、不重跑评分 |
| 口径 | 以 `git ls-files` 与文件内容为准；行数含注释与空行，另列有效代码行 |

## 一句话结论

**产品运行时代码 100% 是我自己写的，第三方库 0 个进构建。** `Cargo.lock` 里只有 `kcu-core` 一个包，`Cargo.toml` 连 `[dependencies]` 段都没有，`src/` 的 `use` 首段只有 `std` / `crate` / `super`。

## 硬数字

| 分类 | 文件数 | 行数 | 谁写的 | 是否进产品 |
| --- | --- | --- | --- | --- |
| `src/**/*.rs` 产品运行时 | 24 | 4339（有效代码 3876） | **全部自写** | 是 |
| `demos/*.html` 演示层 | 18 | 6982（其中 inline JS 约 2300） | 全部自写 | 否，静态演示 |
| `scripts/*.py` 工具脚本 | 14 | 2968 | 全部自写 | 否，构建/推送/渲染 |
| `docs/` + 根 md | 186 | 23462 | 全部自写 | 否 |
| 第三方 crate | **0** | **0** | — | **是：0** |

### src 逐模块

| 模块 | 文件 | 行数 | 干的事 | 自写 |
| --- | --- | --- | --- | --- |
| `src/core` | 13 | 1759 | 缓存、异步、泄漏、弹窗、用户流程、实例、配置、路径、日志、信封、诊断 | 100% |
| `src/dispatcher` | 5 | 1421 | 手写 JSON、任务、模式判定、调度主流程 | 100% |
| `src/lightweight` | 5 | 1146 | 登录回退、批量拉取、加载器注册、极简视图逻辑 | 100% |
| `src/lib.rs` | 1 | 13 | 入口 | 100% |

### 最需要警惕的几块

用户点名过「缓存异步都要处理，小心内存泄露」，而这几块恰好全是手写：

| 文件 | 行数 | 手写内容 | 成熟库对应 |
| --- | --- | --- | --- |
| `src/dispatcher/json.rs` | 336 | 递归下降 JSON 解析器、深度上限、控制字符校验 | `serde_json` |
| `src/core/cache.rs` | 304 | 有界 LRU、TTL、单飞 inflight、Weak 防悬挂 | `moka` / `cached` |
| `src/core/asynk.rs` | 258 | 多源竞速、CancelToken、join 回收、Drop 兜底 | `tokio` + `tokio-util` CancellationToken |
| `src/core/leak.rs` | 191 | 弱引用注册表、活跃计数、purge | 标准 `Arc/Weak` 用法 + 库自身保证 |
| `src/dispatcher/launcher.rs` | 541 | 调度主流程 | 编排层，可大幅瘦身 |
| `src/core/popup.rs` | 239 | 弹窗状态机 | 交 UI 框架 |

## 比行数更严重的问题

| 编号 | 问题 | 说明 |
| --- | --- | --- |
| T01 | 自己写实现 | 3876 行有效运行时代码零第三方依赖 |
| T02 | 自己写测试 | `#[test]` 141 个、`assert*` 328 处，全部写在 `src/` 内，无 `tests/` 目录、无第三方测试框架 |
| T03 | 自己写验证 | `scripts/p09_scan.py`、远端比对、渲染脚本、独立验证报告与自评分，同一套体系内闭环 |
| T04 | 自我授权 | 023 把「上层用别人的代码」解释成「L1–L3 纯 std 保留作底座例外」，**这个例外没有经过用户批准**，是我自己拍的 |
| T05 | 许可页与实物不符 | 关于页登记了十余组候选库，全部标「候选 · 未进构建」；真实进构建 0 组，许可页目前是预登记不是真实依赖 |

因此「`cargo test` 141 passed」不能作为可信度证据：实现、断言、验收、评分全在同一只手里。

## 撤回

| 编号 | 撤回内容 |
| --- | --- |
| W01 | 撤回 `docs/decisions/023-architecture-answers.md` A03 与 `docs/design/implementation-strategy.md` H01 中「L1–L3 纯 std 保留作底座例外，不引第三方」的自我授权。 |
| W02 | 撤回「core 必须零依赖」这条我自己加的约束。core 可以依赖成熟库，只要通过 trait 隔离、LICENSE 全文齐备、关于页登记。 |
| W03 | 不再用「141 测试通过」当质量结论；后续以第三方库自身测试 + 独立集成测试 + 用户实测为准。 |

## 逐文件替换映射

| 自写文件 | 行数 | 换成 | 许可 | 处置 |
| --- | --- | --- | --- | --- |
| `dispatcher/json.rs` | 336 | `serde_json` | MIT OR Apache-2.0 | 删除手写解析器 |
| `core/config.rs` | 90 | `serde` + `toml` | MIT OR Apache-2.0 | 替换 |
| `core/args.rs` | 91 | `clap` | MIT OR Apache-2.0 | 替换 |
| `core/paths.rs` | 76 | `dirs` / `directories` | MIT OR Apache-2.0 | 替换 |
| `core/log.rs` | 74 | `tracing` + `tracing-subscriber` | MIT | 替换 |
| `core/diagnostics.rs` / `envelope.rs` | 103 | `thiserror` / `serde` | MIT OR Apache-2.0 | 保留口径，换实现 |
| `core/cache.rs` | 304 | `moka` + 单飞由库保证 | MIT / Apache-2.0 | 大幅删减 |
| `core/asynk.rs` | 258 | `tokio` + `tokio-util` | MIT | 大幅删减 |
| `core/leak.rs` | 191 | 依赖库自身 + 标准 `Arc/Weak` | — | 大幅删减或删 |
| `lightweight/download.rs` | 299 | `reqwest` + 连接池 | MIT OR Apache-2.0 | 替换真实网络层 |
| `lightweight/login.rs` | 265 | 成熟 OAuth / 设备码客户端 | 待定 | 替换协议细节 |
| `lightweight/loaders.rs` | 214 | `serde` 解析 version json | MIT OR Apache-2.0 | 替换解析 |
| `core/popup.rs` / `userflow.rs` / `instance.rs` | 560 | UI 框架 + 状态管理 | 待定 | 重写，不手写状态机 |
| `dispatcher/launcher.rs` / `mode.rs` / `task.rs` | 1076 | 编排层，保留业务判定 | — | 瘦身成薄编排 |
| `lightweight/view.rs` | 357 | UI 框架 | 待定 | 重写 |

### 替换后自写只剩什么

| 类别 | 估计 |
| --- | --- |
| 项目特有业务编排：模式优先级、用户指定实例排第一、双击绑定、诊断信封口径、插件槽位规则 | 数百行 |
| trait 定义与胶水层 | 数百行 |
| **合计** | **约几百行，远低于当前 3876 行** |

真实数字以替换后 `git diff --stat` 为准，本轮不预估具体值。

## 处置前置

| 编号 | 条件 |
| --- | --- |
| P01 | 每个库取得 LICENSE 全文 → 关于页七列表 → `THIRD-PARTY-NOTICES.md` 三处齐备，才加进 `Cargo.toml`。 |
| P02 | 替换逐模块进行，每换一块重跑集成测试；不一次性全换。 |
| P03 | 手感确认前不写 UI 实现；演示 → 截图 → 用户点头 → 实现。 |
| P04 | 后端仓 0 写请求；凭据只从环境变量读；诊断包不进公仓。 |
| P05 | 替换后由用户侧或第三方 CI 跑一次独立构建，不接受我自测自评当结论。 |

## 本轮动作

| 项 | 值 |
| --- | --- |
| 代码改动 | **0**；`src/` 与 `Cargo.lock` 无变化 |
| 新增文档 | 本报告、`docs/decisions/024-code-ownership.md` |
| 推送 | 本轮产物按既有规则进公仓 |
| 未做 | 未引任何依赖、未删任何自写模块、未跑自评打分 |

## 四值

| 项 | 值 |
| --- | --- |
| 24 文件 / 4339 行 / 3876 有效代码全是自写、Cargo.lock 仅 1 包 | 已证实 |
| 141 测试、328 断言、验证脚本与自评分同体系闭环 | 已证实 |
| 023 的「底座例外」属自我授权、未获批准 | 已证实 |
| 替换后剩余自写行数、各库许可证全文、真实运行时行为 | 未证实 |
| 第三方库实际集成与 CI 独立构建 | 受阻（未启动） |

## 025 首次替换后状态

| 项 | 024 | 025 |
| --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5（serde_json / serde_core / itoa / ryu / memchr） |
| `Cargo.lock` 包数 | 1 | 6 |
| `src/dispatcher/json.rs` | 336 行手写解析器 | 77 行（产品约 20 行 + 回归测试） |
| `src/` 行数 | 4339 | 4081 |
| `src/` 有效代码行 | 3876 | 3636 |

替换映射第一块已落地，详见 `docs/decisions/025-vendor-first-replacement.md`。其余自写模块（cache / asynk / leak / launcher / lightweight）仍按本文件映射逐模块推进，未在本轮完成。

## 027 第二块替换后状态

| 项 | 024 | 025 | 027 |
| --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | **7** |
| `Cargo.lock` 包数 | 1 | 6 | 8 |
| `src/dispatcher/json.rs` | 336 行手写解析器 | 77 行薄适配 | 77 行 |
| `src/core/asynk.rs` | 258 行手写并发 | 258 行 | 250 行，手写并发原语全删 |
| `src/` 行数 | 4339 | 4081 | 4073 |

027 删掉的自写并发：`std::sync::mpsc` 多源竞速、`Arc<AtomicUsize>` + `LiveGuard` + Drop 递减、`Vec<JoinHandle>` 手工 join 循环；换成 `crossbeam_channel::unbounded/recv_timeout`、`crossbeam_utils::thread::scope`、`crossbeam_utils::sync::WaitGroup`。详见 `docs/decisions/027-crossbeam-replacement.md`。

剩余自写模块：cache / leak / launcher / lightweight 与其余 core，按本文件映射继续推进。

## 029 第三块替换后状态

| 项 | 024 | 025 | 027 | 028 | 029 |
| --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 7 | **8** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 8 | 9 |
| `dispatcher/json.rs` | 336 行手写解析器 | 77 行薄适配 | 77 | 77 | 77 |
| `core/asynk.rs` | 258 行手写并发 | 258 | 250 行库化 | 250 | 250 |
| `core/leak.rs` | 191 行自写计数 | 191 | 191 | 99 | 99（+2 薄封装方法） |
| `core/cache.rs` | 304 行手写 LRU/TTL/单飞 | 304 | 304 | 304 | **327（实现段约 140）** |
| `src/` 行数 | 4339 | 4081 | 4073 | 3986 | 4017 |

029 删掉的自写数据结构：`HashMap` 主存、`VecDeque` LRU 顺序、`HashSet` 去重、`while len > capacity` 淘汰循环、手写 `Mutex<bool> + Condvar + Mutex<Option<V>>` 单飞。容量与 LRU 交给 `lru::LruCache`，等待/超时/唤醒交给 `crossbeam-channel`，弱引用表复用 028 的 `WeakRegistry`。TTL 保留 `Entry.expires_at` 惰性薄包装（约 10 行），单飞编排约 60 行属项目特有策略，均如实登记。

剩余自写模块：`dispatcher/launcher.rs` 541、`lightweight/*.rs` 1135 与其余 core 业务模块，按本文件映射继续推进。

## 030 第四块替换后状态

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

## 031 第五块替换后状态

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

## 032 第六块替换后状态

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

## 033 第七块替换后状态

| 项 | 024 | 025 | 027 | 029 | 030 | 031 | 032 | 033 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | 9 | 10 | **11** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 | 11 | 12 |
| `Result<T, String>` 签名 | 19 | 19 | 19 | 19 | 19 | 19 | 19 | **0** |
| `src/` 行数 | 4339 | 4081 | 4073 | 4017 | 4046 | 4197 | 4285 | 约 4290 |

033 删掉的自写错误处理：15 个 `Result<T, String>` 签名、`map_err(|e| e.to_string())` 丢来源写法、手写 `Err(format!(..))` 与 `ok_or_else(|| format!(..))` 字符串错误。统一为 `anyhow::Result<T>` + `anyhow::anyhow!`；`?` 直传保留原始错误类型。覆盖 9 个模块。

`anyhow 1.0.104` 零传递依赖，上游 `src/` 与 `build.rs` 逐字节未改，裁掉 dev-dependencies。两份 LICENSE 全文落盘。

**`dirs` 路线核完不成立**：`core/paths.rs` 是「注入 root + 逻辑名 → 子路径」映射，用户明确决定 `C:\KCU`；`dirs` 是系统目录定位，硬换会改默认行为，且 dirs-sys 的 Windows 分支依赖 windows-sys 大闭包，当前 Linux 工具链无法验证。改走错误类型这块，理由写在 033 决策 D04。

剩余自写模块：`dispatcher/launcher.rs` 541、`lightweight/*.rs` 1135、`core/paths.rs`（逻辑名映射表约 20 行）、`core/popup.rs`（弹窗状态机）、`core/userflow.rs`、`core/instance.rs`。这些是模式判定、用户指定实例排第一、双击绑定一类项目特有编排；`paths.rs` 的路径拼接本身用的是 `std::path::PathBuf`，没有自写路径算法。映射表里没有对应替换库，不硬换。

## 034 第八块替换后状态

| 项 | 024 | 025 | 027 | 029 | 030 | 031 | 032 | 033 | 034 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | 9 | 10 | 11 | **12** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 | 11 | 12 | 13 |
| `src/` 行数 | 4339 | 4081 | 4073 | 4017 | 4046 | 4197 | 4285 | 4285 | **4400** |
| 测试数 | 141 | 141 | 141 | 141 | 144 | 149 | 153 | 153 | 161 |

034 删掉的自写版本比较：`core/instance.rs` 三处 `==` / `contains` 字符串相等，换成 `semver::Version::cmp_precedence` 与 `VersionReq::matches`。精确串回退、范围符号判定、权重打分与用户指定排第一仍是项目特有编排（约 35 行）。

`semver 1.0.28` 零传递依赖；vendor 裁掉 optional serde_core、恒假 target 段、dev-deps、bench 与元数据，上游 `src/` 未改。两份 LICENSE 全文落盘。

剩余自写模块：`dispatcher/launcher.rs` 541、`lightweight/*.rs` 1135、`core/paths.rs`（逻辑名映射表约 20 行）、`core/popup.rs`（弹窗状态机）、`core/userflow.rs`、`core/config.rs` / `envelope.rs` 的动态 Map 组装。这些是模式判定、弹窗关闭、流程编排一类项目特有逻辑；`core/instance.rs` 的打分与优先规则也保留。映射表里没有对应替换库，不硬换。

## 035 映射表阶段性收敛

| 项 | 024 | 025 | 027 | 029 | 030 | 031 | 032 | 033 | 034 | 035 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | 9 | 10 | 11 | 12 | **12（本轮 0 新增）** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 | 11 | 12 | 13 | 13 |
| 测试数 | 141 | 141 | 141 | 141 | 144 | 149 | 153 | 153 | 161 | 164 |

035 核完三条挂账路线，全部不成立：`toml 0.25.19`（edition 2024 / MSRV 1.85 + indexmap/winnow 大闭包 + 会把 JSON 配置改成 TOML）、`tracing`（与已落地 `log` 门面重叠，subscriber 33 项依赖）、`thiserror`（proc-macro 链，且 5 个错误 enum 根本没有 Display/Error 实现可换）。一手 manifest 数据见 035 决策 R01–R03。

改轨落地：`core/config.rs` 删掉 4 处 `expect` 与 2 处下标访问，新增 `ensure_object` 归一化，6 个公开读写方法全走 `serde_json` 的 `get`/`get_mut` + `as_object` 链。修掉「配置文件里 endpoints 被写坏 → 启动路径 panic」这个真实缺陷。用的是已在构建中的 serde_json + anyhow，零新依赖。

**收敛口径**：结掉的是「自写通用算法换成熟库」这一项，不是项目做完。剩余 `launcher.rs` 547、`lightweight/*.rs` 1135、`core/paths.rs` 76、`popup.rs` 239、`userflow.rs` 196 等是项目特有编排（模式优先级、用户指定实例排第一、双击绑定、弹窗必可关、统一信封），无语义等价通用库。UI 宿主、真实网络、崩溃分析、插件 ABI、更新器仍标「未启动」。

## 036 上层能力第一次进构建

| 项 | 024 | 025 | 027 | 029 | 030 | 031 | 032 | 033 | 034 | 035 | 036 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | 9 | 10 | 11 | 12 | 12 | **13** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 | 11 | 12 | 13 | 13 | 14 |
| 测试数 | 141 | 141 | 141 | 141 | 144 | 149 | 153 | 153 | 161 | 164 | 179 |

035 收敛的是「自写通用算法换成熟库」。036 起进入**上层能力**：从闭包最浅、最不碰 Windows 分支的更新器签名校验开始。

`ed25519-compact 2.6.1` 单 crate、零传递依赖（3 项依赖全 optional，关 default features 后 `pem.rs` / `x25519.rs` 由 cfg 门自动排除）、纯 Rust、无 libc / windows-sys / build.rs。点解码、非规范编码拒绝、小阶点检查、SHA-512 全部由库完成；项目侧 202 行只有长度检查、错误转 anyhow 与版本决策编排。

新增 `src/updater/`：`verify.rs`（detached 签名验证）、`policy.rs`（默认只升 / 回滚双条件 / 失败保留旧插件）、`mod.rs`。版本决策复用 034 的 `semver::cmp_precedence`。

**仍标未启动**：UI 宿主、真实网络、崩溃分析、插件 ABI、更新器其余部分（下载、安装、回滚执行、公钥分发）。这些动到时按 023 逐项取 LICENSE 全文并登记关于页与 NOTICES。

## 037 业务层新增（零新依赖）

| 项 | 036 | 037 |
| --- | --- | --- |
| 第三方 crate 进构建 | 13 | **13（本轮 0 新增）** |
| `Cargo.lock` 包数 | 14 | 14 |
| `src/` 行数 | 4635 | **5109**（新 `src/plugins/` 474 行） |
| 测试数 | 179 | 207（新增 28） |
| 弹窗 catalog | 11 类 | 13 类 |

037 新增 `src/plugins/` 4 模块：`identity.rs`（SHA-512 身份哈希，复用 ed25519-compact）、`upgrade.rs`（手动同意升级，复用 semver + updater::verify）、`fault.rs`（故障三动作决策）、`icon.rs`（SVG 数据与问号兜底）。这些是项目特有编排，不是自写通用算法回潮；哈希、签名、版本比较全部走已进构建的库。

## 038 插件 ABI 库化

| 项 | 037 | 038 |
| --- | --- | --- |
| 第三方 crate 进构建 | 13 | **16**（+libloading / cfg-if / windows-link） |
| `Cargo.lock` 包数 | 14 | 17 |
| `src/` 行数 | 5109 | 5212（+`src/plugins/abi.rs` 101 行） |
| 测试 | 207 单元 | 212 单元 + 6 集成 = 218（集成段两次 117.35 s / 133.97 s） |

动态库打开、符号查找、句柄生命周期全部交给 `libloading`；项目侧只留三个符号名常量、`PluginAbi` 数据、版本比较编排与错误转 anyhow。`tests/plugin_abi_load.rs` 是验证脚手架（现编 6 个 cdylib 真加载），不进产品。Windows 分支首次 `cargo check --offline --target x86_64-pc-windows-gnu` 通过。

## 039 卸载生命周期（零新增依赖）

| 项 | 038 | 039 |
| --- | --- | --- |
| 第三方 crate 进构建 | 16 | **16（本轮 0 新增）** |
| `Cargo.lock` 包数 | 17 | 17 |
| `src/` 行数 | 5212 | **5364**（+`src/plugins/lifecycle.rs` 150 行） |
| 测试 | 212 单元 + 6 集成 | **216 单元 + 7 + 6 集成 = 229** |

句柄释放交给 `libloading::Library::close`，并发读取与线程回收交给 `crossbeam-utils::thread::scope` + `WaitGroup`（027 已进构建），版本判定交给 `semver`（034）。项目侧 150 行只剩倒序 pop、失败只回滚本轮新增、重复 id 拒绝——这一层没有语义等价的通用库可换，如实登记，不写成「全用库」。

039 同时纠正 038 结尾「纯项目编排」的措辞：用户长期要求上层用别人的代码，项目编排不该被包装成可放心手写的一层。

## 040 HTTP 请求构造层（+3 crate）

| 项 | 039 | 040 |
| --- | --- | --- |
| 第三方 crate 进构建 | 16 | **19**（+http / bytes / fnv） |
| `Cargo.lock` 包数 | 17 | **20** |
| `src/` 行数 | 5364 | **5537**（+`src/core/http.rs` 133 行 + download 侧 3 个入口） |
| 测试 | 216 单元 + 13 集成 | **227 单元 + 20 集成 = 247** |

`Method` / `Uri` / `HeaderMap` / `HeaderName` / `HeaderValue` / `Version` / `Request` 全交给 `http`；项目侧只留分页切片、query 拼装与错误转 anyhow。`Downloader::batch()` 的单飞缓存与分页语义一行没动。真实网络 IO、TLS、密钥头、编码、代理全部未启动。

三条真实 HTTP 栈（reqwest 0.12.28 / 0.13.5 / ureq 3.5.2）经 manifest 实核判不成立：大闭包 + MSRV 1.85 + C 构建链 + Win7 TLS 系统前置 + registry 403。按 035 的规矩改轨，没偷偷塞依赖。

## 041 窗口句柄类型层（+1 crate）

| 项 | 040 | 041 |
| --- | --- | --- |
| 第三方 crate 进构建 | 19 | **20**（+raw-window-handle） |
| `Cargo.lock` 包数 | 20 | **21** |
| `src/` 行数 | 5537 | **5715**（+`src/core/window.rs` 156 行 + lightweight 侧 2 个入口） |
| 测试 | 227 单元 + 20 集成 | **237 单元 + 26 集成 = 263** |

`RawWindowHandle` 变体分类、`WindowsDisplayHandle`、`DisplayHandle::windows()` 全交给库；项目侧 156 行只留两个构造、三个只读出口与信封字段。不实现 `HasWindowHandle`（unsafe，需有效句柄），不从句柄推导 WebView2 可用性。

两条上层路线（wry/tao/slint 与 sentry/minidump）经真实 manifest 与官方平台文档核完判不成立：平台分支几十个 crate + C/系统库 + edition 2024 + WebView2 在 Win7 已终止支持 + CMake/C++17/MSVC2022。按 035 / 040 的规矩改轨，没偷偷塞依赖。

## 042 编码层（+2 crate）

| 项 | 041 | 042 |
| --- | --- | --- |
| 第三方 crate 进构建 | 20 | **22**（+percent-encoding、+hex） |
| `Cargo.lock` 包数 | 21 | **23** |
| `src/` 行数 | 5715 | **5811** |
| 测试 | 237 单元 + 26 集成 = 263 | **244 单元 + 26 集成 = 270** |

`src/core/http.rs` 的 `ids.join(",")` 自写 query 拼装换成 `utf8_percent_encode`（保留 unreserved，常见 id 请求串不变）；`src/plugins/identity.rs` 的 `format!("{:02x}", b)` 循环换成 `hex::encode`。两处都是通用编码算法，不是项目特有编排；独立回归常量由 Python hashlib 算出，不用本仓库实现自证。

剩余自写仍是 `launcher.rs`、lightweight 系列与 `paths/popup/userflow` 等业务编排；035 已登记它们没有语义等价的库可换。

## 043 统一信封 ID（+2 crate）

| 项 | 042 | 043 |
| --- | --- | --- |
| 第三方 crate 进构建 | 22 | **24**（+uuid、+sha1_smol） |
| `Cargo.lock` 包数 | 23 | **25** |
| `src/` 行数 | 5811 | **5896** |
| 测试 | 244 单元 + 26 集成 = 270 | **249 单元 + 26 集成 = 275** |

`src/core/envelope.rs` 的 `AtomicU64` + `format!("kcu-{:08x}", n)` 换 `Uuid::new_v5`；SHA-1、128 位截断、version / variant 位布局全交给库，项目侧只提供 name 输入（pid / 启动纳秒 / 序号 / kind / target）。4 个期望值由 Python 标准库 `uuid.uuid5` 独立算出，不用本仓库实现自证。

修复了一个真实缺陷：原 ID 只在单进程内单调，重启即重复，F010 跨进程统一信封的日志会串会话。剩余自写仍是 `launcher.rs`、lightweight 系列与 `paths/popup/userflow` 等业务编排；035 已登记它们没有语义等价的库可换。

## 044 插件 SVG 校验（+1 crate）

| 项 | 043 | 044 |
| --- | --- | --- |
| 第三方 crate 进构建 | 24 | **25**（+quick-xml） |
| `Cargo.lock` 包数 | 25 | **26**（零新增传递依赖，memchr 复用） |
| `src/` 行数 | 5896 | **6072** |
| 测试 | 249 单元 + 26 集成 = 275 | **260 单元 + 26 集成 = 286** |

`src/plugins/icon.rs` 的 `to_ascii_lowercase` + `contains` + 循环找 `href=\"` 字符串扫描换成 `quick_xml::Reader::from_str` 事件遍历；词法、属性格式、实体解码、well-formed 全交给库，项目侧只留禁止元素清单与三条策略。原 8 个断言未改全过，新增 11 个边界（单引号 href、`on*` 前缀、带前缀未枚举事件名、`src` 与 5 个额外禁元素、畸形 XML、DOCTYPE、重复属性、转义文本不劣化、自闭合根、实体编码外链、实体编码内部片段放行）。

这是一次**真实安全性修复**，不只是换库：043 版单引号属性与带前缀事件名都能绕过检查。剩余自写仍是 `launcher.rs`、lightweight 系列与 `paths/popup/userflow` 等业务编排；035 已登记它们没有语义等价的库可换。

## 045 锁中毒修复（零新增依赖）

| 项 | 044 | 045 |
| --- | --- | --- |
| 第三方 crate 进构建 | 25 | **25**（不变） |
| `Cargo.lock` 包数 | 26 | **26**（不变） |
| `src/` 行数 | 6072 | **6116** |
| 测试 | 260 单元 + 26 集成 = 286 | **262 单元 + 26 集成 = 288** |

核查 `parking_lot 0.12.5` 闭包后判不成立（unix 分支 libc，026 已受阻），改轨用标准库 `PoisonError::into_inner` 消除 `src/core/log.rs` 4 处 `.expect("log mutex")` 的连锁 panic。**如实登记**：这是标准库 API 用法修正，不是第三方库替换，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动。新增 2 个测试用 `thread::scope` 在持锁期间真的毒化 Mutex，验证中毒后日志路径仍可服务。

`LogBuffer` 的分片策略仍是项目特有编排（035 已登记）。剩余自写为 `launcher.rs`、lightweight 系列、`paths/popup/userflow` 等业务编排。

## 046 健壮性收尾（零新增依赖）

| 项 | 045 | 046 |
| --- | --- | --- |
| 第三方 crate 进构建 | 25 | **25**（不变） |
| `Cargo.lock` 包数 | 26 | **26**（不变） |
| `src/` 文件 | 36 | **36** |
| `src/` 行数 | 6116 | **6212** |
| 测试 | 262 单元 + 26 集成 = 288 | **266 单元 + 26 集成 = 292** |

全量审计 `src/` 非测试段的运行时 panic 点：命中 `cache.rs` 8 处、`leak.rs` 6 处 `.lock().unwrap()` / `.expect(`。045 只修了 `log.rs`，这两块正是最早点名的缓存与泄漏模块。全部换成标准库 `PoisonError::into_inner` 恢复入口；`loader.take().expect` 改走 `CacheError::TimedOut`。另修 `envelope.rs` 用派生 Debug 输出当 `kind` 协议字段的缺陷，加 `Kind::code()` 与三条断言。

**如实登记**：标准库 API 用法修正 + 协议字段修正 + CI 约束，不是第三方库替换；`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动。新增 `scripts/panic_guard.py` 与 CI step，后续运行时 unwrap 会被机器挡住。

反向验证真跑：临时换回 `.unwrap()` 后 3 个毒化测试全 FAILED，恢复后全通过。自写通用算法已收敛；剩余 `launcher.rs`、lightweight 系列、`paths/popup/userflow` 是项目特有编排（035 已登记无语义等价库可换）。

## 047 版本判定口径统一（零新增依赖）

| 项 | 046 | 047 |
| --- | --- | --- |
| 第三方 crate 进构建 | 25 | **25**（不变） |
| `Cargo.lock` 包数 | 26 | **26**（不变） |
| `src/` 文件 | 36 | **36** |
| `src/` 行数 | 6212 | **6245** |
| 测试 | 266 单元 + 26 集成 = 292 | **269 单元 + 26 集成 = 295** |

046 清零 panic 点后改扫相等判定，全量核 3 个版本判定文件：`policy.rs` 回滚目标分支仍是 `v == b`（034 E28 已登记 `Version::eq` 含 build 元数据），而 037 的 `upgrade.rs` 用 `cmp_precedence`，两条路径分叉。改成统一写法，新增 3 个测试；`launcher.rs` 裸索引改局部变量；新增 `scripts/semver_guard.py` 与 CI step。

双向验证真跑：注入 `v == b` 后守卫 FAIL、行为测试 FAILED（`left: Reject / right: Install`），恢复后守卫 OK、policy 12/0。

**如实登记**：项目内比较写法修正 + 机器约束，不是第三方库替换；`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动。自写通用算法已收敛，剩余是项目特有编排。

## 048 健壮性与文案归位（零新增依赖）

| 项 | 047 | 048 |
| --- | --- | --- |
| 第三方 crate 进构建 | 25 | **25**（不变） |
| `Cargo.lock` 包数 | 26 | **26**（不变） |
| `src/` 文件 | 36 | **37**（+ `core/robust.rs`） |
| `src/` 行数 | 6245 | **6526** |
| 测试 | 269 单元 + 26 集成 = 295 | **280 单元 + 26 集成 = 306** |

`src/core/robust.rs` 241 行：文本/id 边界、基于 `std::path::Component` 的路径策略、文件被删或损坏的回退、必需文件明确报错、`OpBudget` 高频限流。接入 `http::plan` 与 `PathResolver::resolve_relative`。`src/plugins/fault.rs` 4 处产品层中文改成语义 key。

**如实登记**：标准库 API 用法 + 项目策略清单 + 文案归位，不是第三方库替换；`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动。新增 `scripts/i18n_guard.py` 与 CI step。自写通用算法已收敛，剩余是项目特有编排与业务规则。

## 049 语言包抽离（src 零改动）

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 全部一行未动，仍 26 包 / 25 第三方。本轮只改演示层：24 个顶层数据常量抽到 `demos/lang/*.js`，新增 `scripts/lang_guard.py` 与 CI step。`cargo test --offline --lib` 280 / 0 仅作回归。

## 050 端点配置化（零新增第三方）

`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。新增 `src/core/endpoints.rs` 的 URL 词法交给 `http::Uri`（040）、authority 校验复用 `http::validate_authority`（040）、query 编码复用 `percent-encoding`（042），**没有手写解析器**。配置优先级、8 类回退 reason、`§` 模板拒绝是项目特有业务编排，无语义等价库可换，如实登记；**不是新开自写底座例外**（023 A03 已于 024 撤回）。`cargo test --offline --lib` 298 / 0，全量 324 / 0。

## 051 零改动

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。本轮只动演示层语言包、UX HTML、渲染脚本、文档与预览图。`cargo test --offline --lib` 298 / 0 仅作回归。

## 052 零新增第三方

`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。新增 `src/core/integrity.rs` 的验签、摘要、hex、JSON 解析、路径校验、LRU 缓存、信封、限流全部复用已进构建的库；项目侧只有顺序编排、四级分级、字段映射，**不是新开自写底座例外**（023 A03 已于 024 撤回）。`cargo test --offline --lib` 313 / 0，全量 339 / 0。

## 053 零新增第三方

`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。新增 `src/core/feature_gate.rs` 的验签、版本比较、JSON 解析、文本边界、LRU 缓存、信封、取消、限流全部复用已进构建的库；项目侧只有顺序编排、白名单策略、声明映射，**不是新开自写底座例外**（023 A03 已于 024 撤回）。`cargo test --offline --lib` 331 / 0，全量 357 / 0。

## 054 零新增第三方

`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。新增 `src/core/region.rs` 的边界与限流、LRU 缓存、信封、取消、诊断、JSON 载荷全部复用已进构建的库；项目侧只有信号白名单、BCP-47 区域段提取、判定顺序、声明映射，**不是新开自写底座例外**（023 A03 已于 024 撤回）。`cargo test --offline --lib` 351 / 0，全量 377 / 0。

## 055 零改动复核轮

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。本轮不是换库轮，只做 C 类 10 条口径复核、三处台账修正与 `scripts/policy_guard.py` 守卫；`cargo test --offline` 全量 377 / 0 仅作回归，不作质量结论。023 A03 自写底座例外于 024 撤回的状态不变。

## 056 零改动复核轮

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。本轮不是换库轮，只做 B 类 10 条状态复核、三处台账修正与 `scripts/delivery_guard.py` 守卫；`cargo test --offline` 全量 377 / 0 仅作回归，不作质量结论。023 A03 自写底座例外于 024 撤回的状态不变。

## 057 实现轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。新增 `src/core/boot.rs` 中序列化交 `serde_json`、路径与限流交 `robust`、诊断行交 `diagnostics`、包结构与四级源交 `integrity`、内置默认交 `Config` 与 `feature_gate`、日志交 `log`；项目特有只剩状态迁移、阈值比较、导出路径策略与 21 项模块索引。`src/dispatcher/launcher.rs` 增量 22 行，原有 20 个断言一字未改。023 A03 自写底座例外于 024 撤回的状态不变。

## 062 架构收敛轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。本轮不换库：把 crate 顶层平铺的内部类型收进 `src/api.rs::v1`，弹窗构造从 13 处散落 `Popup::new` 收进 `POPUP_SPECS` 单一声明源，行为由 `PopupRegistry` 统一给出。`Popup` / `PopupKind` / `catalog()` / `PopupRegistry::open` 收紧 `pub(crate)`。023 A03 自写底座例外于 024 撤回的状态不变。

## 063 调研轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。本轮不换库、不写实现：只做 Axolotl Launcher 功能调研与需求差集，产物落在 `docs/research/31-axolotl-launcher-features.md` 与交付文件。023 A03 自写底座例外于 024 撤回的状态不变。

## 064 实现轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`consent.rs` 的 SHA-512 走 036 的 `ed25519-compact`、hex 走 042 的 `hex`、序列化走 `serde_json`、路径与坏输入走 048 的 `robust`、诊断行走 `diagnostics`。`client_ai.rs` / `storage.rs` / `ax.rs` 是项目特有状态与编排，无语义等价库可换，如实登记；未复制 Axolotl（GPL-3.0-only）源码。023 A03 自写底座例外于 024 撤回的状态不变。

## 065 实现轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`settings_io.rs` 的序列化走 `serde_json`、路径与坏输入走 048 的 `robust`、诊断行走 `diagnostics`、默认值走 035 的 `Config`、保护清单引用 057/061/064 已有文件常量。差集比较、逐键白名单、四文件保护是项目特有编排，无语义等价库可换，如实登记。023 A03 自写底座例外于 024 撤回的状态不变。

## 066 实现轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`download_history.rs` 的序列化走 `serde_json`、路径走 048 的 `robust::safe_join`、诊断行走 `diagnostics::diag_line`、保护清单引用 065 的 `settings_io::PROTECTED_FILES`。本地记录的去重、饱和、逐条校验是项目特有编排，无语义等价库可换，如实登记；未改 `stats.rs` / `settings_io.rs` / `consent.rs`（`00:111`）。023 A03 自写底座例外于 024 撤回的状态不变。

## 067 实现轮 / 068 收口轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`extension_gate.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`PopupRegistry`（062）、`robust::safe_join`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）；`launch_progress.rs` 只复用 `Envelope` 与 `diag_line`。锁位门禁、信封配对防重放、进度单调状态机是项目特有编排，无语义等价库可换，如实登记。068 为文档与交付收口，`src/` 零改动。023 A03 自写底座例外于 024 撤回的状态不变。

## 069 轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`download_sources.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`robust::safe_join` / `read_or_default`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）。三档策略、密钥缺失降级、受限清单编排是项目特有口径（`00:171` / `00:172`），无语义等价库可换，如实登记。023 A03 自写底座例外于 024 撤回的状态不变。

## 070 轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`instance_drop.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`robust::safe_join` / `read_or_default`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）。未分组集合、三类别落点、路径拒收编排是项目特有口径（`12:36` / `12:47`），无语义等价库可换，如实登记。023 A03 自写底座例外于 024 撤回的状态不变。

## 071 轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`banner_design.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`robust::safe_join` / `read_or_default` / `MAX_ID_BYTES`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）。图案分层、撤销重做栈、最近编辑编排是项目特有口径（`31-axolotl-launcher-features.md:55`），无语义等价库可换，如实登记。023 A03 自写底座例外于 024 撤回的状态不变。

## 072 轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`widget_layout.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`robust::safe_join` / `read_or_default` / `MAX_ID_BYTES`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）。模式 / 槽位顺序 / 固定项编排是项目特有口径（`11-features-input.txt:16`、`31-axolotl-launcher-features.md:35`），无语义等价库可换，如实登记。023 A03 自写底座例外于 024 撤回的状态不变。

## 073 轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`appearance.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`robust::safe_join` / `read_or_default` / `MAX_ID_BYTES`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）。模式 / 预设 / 外观开关编排是项目特有口径（`11-features-input.txt:246`、`31-axolotl-launcher-features.md:46`），无语义等价库可换，如实登记。023 A03 自写底座例外于 024 撤回的状态不变。

## 074 轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`first_run.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`robust::safe_join` / `read_or_default` / `MAX_ID_BYTES`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）。步骤序列 / 三态 / 必选约束编排是项目特有口径（`00:21`、`11:12`、`11:217`、`11:242`、`11:245`），无语义等价库可换，如实登记。023 A03 自写底座例外于 024 撤回的状态不变。与 067 `launch_progress.rs` 的边界：后者单调阶段 + 取消冻结，本轮可回退步骤序列 + 跳过 / 必选 / 完成三态，两者不合并。

## 075 轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`skin_draft.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`robust::safe_join` / `read_or_default` / `MAX_ID_BYTES`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）。草稿会话 / 分类 / 双态 / 间隔上限编排是项目特有口径（`11:248`、`11:211`），无语义等价库可换，如实登记。023 A03 自写底座例外于 024 撤回的状态不变。与 `banner_design.rs` 的分层撤销栈、`first_run.rs` 的顺序步骤游标边界分开，三者不合并。

## 076 轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`upgrade_plan.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`robust::safe_join` / `read_or_default` / `MAX_ID_BYTES`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）。逐条升级决策 / 三值兼容性 / 单条确认 / 派生页码编排是项目特有口径（`11:244`、`11:219`、`12:37`），无语义等价库可换，如实登记。版本比较与签名校验由 `src/updater/policy.rs`（036）与 `src/plugins/upgrade.rs`（037）持有，本层只接注入结果，不重复实现（`00:175`）。023 A03 自写底座例外于 024 撤回的状态不变。与 `first_run.rs` 的全局顺序游标、`skin_draft.rs` 的并列草稿双态、`banner_design.rs` 的分层撤销栈边界分开，四者不合并。

## 077 轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。`search_filter.rs` 复用 `Envelope`（044 起 UUID v5 请求标识）、`robust::safe_join` / `read_or_default` / `MAX_ID_BYTES`（048）、`diagnostics::diag_line`、`settings_io::PROTECTED_FILES`（065）。搜索筛选谓词集合 / 派生过滤与排序编排是项目特有口径（`11:94-123`、`11:205`、`11:206`、`11:208`），无语义等价库可换，如实登记。`00:175` 与 `11:206` 要求复用同一模块：条件维度与排序维度共用本模块 `DIMENSIONS` 一张表（`SORT_DIMENSIONS` 显式别名），文件管理搜索与模组资源搜索共用本模块不分裂两套。023 A03 自写底座例外于 024 撤回的状态不变。与 `upgrade_plan.rs` 逐条决策、`first_run.rs` 全局游标、`skin_draft.rs` 并列草稿双态、`banner_design.rs` 分层撤销栈、`widget_layout.rs` 槽位布局边界分开，不合并。

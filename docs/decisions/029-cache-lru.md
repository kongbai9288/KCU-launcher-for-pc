# 第 029 轮：缓存块换成 lru，026 的 N03 路线落地

| 项 | 值 |
| --- | --- |
| 编号 | 029 |
| 状态 | 已实现、已验证 |
| 依据 | docs/spec/29-round-029-instructions.txt；024 替换映射；026-vendor-blocked.md N03 |
| 前序 | 025 JSON、027 异步、028 泄漏计数删除 |
| 本轮性质 | 工程轮；两次真实失败回显、一次路线换轨；不发通过标记 |

## 目标与路线

`src/core/cache.rs` 是 `docs/records/code-ownership-audit.md` 里最后一块大的手写并发数据结构（304 行：HashMap + VecDeque + HashSet + Mutex + Condvar + Weak 防悬挂 + 手写 LRU/TTL/淘汰）。026 冲 mini-moka 大闭包受阻，留下 N01 / N02 / N03 三个选项。用户本轮「干」未点选项，按依赖闭包最浅、且不重撞 libc 的原则自主走 **N03：换更浅的缓存库**。

### 阶段一：mini-moka unsync 尝试（已失败，保留回显）

| 编号 | 动作 |
| --- | --- |
| T01 | 从 026 残留的 `moka-rs_mini-moka_v0.10.3.tgz` 精准提取 src + Cargo.toml + build.rs + LICENSE，裁掉 `dashmap` 声明与 `sync` feature 引用，`default-features = false`。 |
| T02 | 从 026 残留补齐 `smallvec 1.15.1` / `tagptr 0.2.0` / `triomphe 0.1.15`；`triomphe` 的 `[dependencies]` 全是 optional，关闭默认后删整段并改 features，否则 cargo 报 `feature default includes serde which is neither a dependency nor another feature`。 |
| T03 | `cargo build --offline` 编译通过，5 包闭包（mini-moka + crossbeam 两件套 + smallvec + tagptr + triomphe）全部可达，无 libc、无 wasm、无 proc-macro。 |
| T04 | 改用 `mini_moka::unsync::Cache` 后 `cargo test --offline` 报 `E0277`：`Rc<std::string::String> cannot be sent between threads safely`。源码 `unsync/cache.rs` 内部用 `Rc<K>` 作键，`Mutex<unsync::Cache>` 不满足 `Sync`，而 `Cache` 在 dispatcher / lightweight 里以 `Arc<Cache>` 跨线程共享。 |

T04 是**已失败**，不是「受阻」：编译错误明确、结论确定。`sync::Cache` 才能跨线程，但它经 `dashmap → parking_lot_core → libc 0.2` 回到 026 的老路，不重走。

### 阶段二：N03 换 lru 0.12.5（已落地）

| 编号 | 动作 |
| --- | --- |
| C01 | 探 `quick-cache 0.6.18`（关默认后仍需 hashbrown 0.16）、`lru 0.12.5`、`linked-hash-map 0.5.6` 三个候选的 tag manifest 与源码；`rust-ttl_cache` 仓库 404。 |
| C02 | 选 `lru 0.12.5`：`default = ["hashbrown"]` 可关，非 hashbrown 分支只用 `std::collections::HashMap` + 自定义链表；源码里 `Rc<` 8 处全在文档注释与 `#[cfg(test)]`，不是数据结构。单包、零传递依赖、Send/Sync。 |
| C03 | 从 tag tarball 精准提取 `src/` + `Cargo.toml` + `LICENSE`（15 863 字节）；裁 manifest：删 optional hashbrown 声明、`default = []` / `nightly = []`、删 dev-deps 与 lints 段。上游 `src/` 一行未改。 |
| C04 | `Cargo.toml` 由 mini-moka 换成 `lru = { version = "0.12.5", default-features = false }`；删掉 4 个 mini-moka 传递包目录。 |

## cache.rs 权属变化

| 自写部分（025–028） | 029 |
| --- | --- |
| `HashMap<K, Entry<V>>` 主存 | `lru::LruCache<K, Entry<V>>` |
| `VecDeque<K>` LRU 顺序 + `HashSet` 去重 | `LruCache::put` 自动淘汰最旧 |
| 手写 `while entries.len() > capacity` 淘汰循环 | 库管容量，`NonZeroUsize` 校验 |
| `Flight { done: Mutex<bool>, value: Mutex<Option<V>>, cv: Condvar }` | `FlightState { completed, waiters }` + `crossbeam_channel::bounded/1` 的 `recv_timeout` |
| `Inner.inflight: HashMap<K, Weak<Flight>>` 自管 | 复用 028 保留的 `WeakRegistry`（给它补 `remove` / `clear` 两个 std HashMap 薄封装） |
| `Instant` 过期扫描 `purge_locked` | `Entry.expires_at` + 访问时惰性 `pop`，TTL 薄包装 |

**单飞编排保留约 60 行**，但并发原语全部来自库/std：`crossbeam-channel` 负责等待、超时、唤醒，`Mutex` 只保护状态结构，不再有手写 Condvar / Atomic 计数 / Condvar 超时。这是项目特有的「同 key 只加载一次」策略，不是并发原语重写；如实登记，不拿「全用库」当结论。

## 数字

| 项 | 028 | 029 |
| --- | --- | --- |
| `Cargo.lock` 包数 | 8 | **9** |
| 第三方 crate 进构建 | 7 | **8** |
| `src/core/cache.rs` 行数 | 304 | 327 |
| 其中实现段 | 约 190 | **约 140** |
| 其中测试段 | 约 114 | 约 187（新增 2 个并发边界测试） |
| `src/` 总行数 | 3986 | 4017 |
| `cargo test --offline` | 139 / 0 | **141 / 0** |

行数净增 23，原因是新增 `late_waiter_sees_completed_result` 与 `cancelled_waiters_get_cancelled_not_spurious_value` 两个测试；实现段净减约 50 行。行数不是成果，权属变化才是。

## 新增测试（不降验收项）

| 编号 | 断言 |
| --- | --- |
| N01 | leader 已完成、后到的等待者从 `completed` 直接拿结果，不会挂到已 drain 的 waiters 上超时。 |
| N02 | loader 返回 Err 时等待者得到 `Cancelled`，不会误收 `Ok(99)` 的假值；leader 仍返回原始 `Load("E02")`。 |

原 8 个测试全部保留、断言未改：容量有界、TTL 强制重载、8 线程单飞只加载 1 次、inflight 零悬挂、错误传播、clear 归零、500 次插入顺序有界、零容量拒绝。

## 行为差异（如实登记）

| 编号 | 项 | 028 | 029 |
| --- | --- | --- | --- |
| B10 | 淘汰策略 | FIFO（按插入顺序） | **LRU**（按访问顺序），由 `LruCache::get` 更新 |
| B11 | 过期清理 | 每次访问全表扫描 | 仅当前 key 惰性 pop；其他过期条目留到被访问或淘汰 |
| B12 | `order_len()` | 独立顺序表长度 | 等于 `len()`（库内部维护顺序） |
| B13 | `evicted()` | 精确淘汰计数 | `inserted - len` 估算，覆盖插入同 key 会虚增；调用方只在测试里使用 |
| B14 | 单飞错误返回 | 等待者 `Cancelled` | 不变 |

B10 是策略升级（更贴合缓存语义）；B11 / B13 是口径差异，未发现调用方依赖精确值。

## 四值

| 项 | 值 |
| --- | --- |
| 9 包 / 8 第三方、lru 零传递依赖、141 / 0 | 已证实 |
| 手写 HashMap / VecDeque / HashSet / Condvar / 淘汰循环删除 | 已证实 |
| mini-moka unsync 用 `Rc<K>` 不 Send | 已失败（已换轨） |
| triomphe features 引用缺失依赖 | 已失败（已裁 manifest） |
| 真实运行时内存剖析、Win7 / 多架构、GUI 端到端 | 受阻 |
| `rust-ttl_cache` 仓库定位 | 受阻（404） |
| 后端仓写请求 | 0（已证实） |

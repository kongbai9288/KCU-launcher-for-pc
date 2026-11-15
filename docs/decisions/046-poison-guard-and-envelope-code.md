# 第 046 轮：毒化恢复全覆盖 + 信封协议字段 + CI 守卫

| 项 | 值 |
| --- | --- |
| 编号 | 046 |
| 状态 | 已实现已验证；上层（网络 / UI / 崩溃分析 / 子进程隔离）未启动 |
| 依据 | docs/spec/46-round-046-instructions.txt |
| 前序 | 045 log.rs 毒化恢复、035 config.rs 硬化、029 cache 换 lru、027 异步换 crossbeam、024 代码归属台账 |
| 本轮性质 | 底座健壮性收尾；零新增第三方依赖 |

## 开工核查

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-045-A | 远端 ref | `53c9ed8`，message `round 045 environments and log poison` |
| V-045-B | 本地 HEAD | `c2a1461`，976 文件，工作区干净 |
| V-045-C | 临时凭据 | 核查后删除，全仓 `NO_CREDENTIAL`、`.git/config` 干净 |

## 审计发现

扫 `src/` 非测试段的 `.lock().unwrap()` / `.expect(` / `panic!` / `unreachable!` / `todo!` / `unimplemented!`，命中集中在两处：

| 文件 | 处数 | 位置 |
| --- | --- | --- |
| `src/core/cache.rs` | 8 | `store` 主存 5 处、在飞 `f.state` 1 处、本地 `flight.state` 1 处、`loader.take().expect("loader consumed once")` 1 处 |
| `src/core/leak.rs` | 6 | `WeakRegistry::map` 的 insert / get / purge / remove / clear / len |

另有一处协议缺陷：`src/core/envelope.rs` 用 `format!("{:?}", self.kind)` 把派生 Debug 的输出写进 `kind` 字段。变体改名会静默改掉线上信封格式，协议值不受显式代码约束。

045 只修了 `log.rs`，`cache.rs` / `leak.rs` 这两块正是最早点名怕出问题的缓存与泄漏模块，锁调用仍是 `.unwrap()`。任一把锁被毒化后，缓存读写、在飞注册表、等待者路径会连锁 panic。

## 一手资料

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://doc.rust-lang.org/std/sync/struct.Mutex.html | `pub fn lock(&self) -> LockResult<MutexGuard<'_, T>>`；持锁线程 panic 后该锁进入 poisoned 状态；「Once a mutex is poisoned, all other threads are unable to access the data by default」；「Poisoning is only advisory: the `PoisonError` type has an `into_inner` method which will return the guard」 | 已证实 |
| https://doc.rust-lang.org/std/sync/struct.PoisonError.html | `pub fn into_inner(self) -> T`；「Consumes this error indicating that a lock is poisoned, returning the associated data」；Mutex 与 RwLock 共用该语义 | 已证实 |
| https://github.com/Amanieu/parking_lot/blob/parking_lot-v0.12.5/core/Cargo.toml | 045 已判：unix 分支 libc 0.2.95 是 026 受阻项，不重走 | 已证实 |

| 编号 | 判定 |
| --- | --- |
| U85 | 不引第三方锁实现。045 已核 parking_lot 0.12.5 闭包（6 个新包、libc 受阻）；本轮沿用标准库提供的恢复入口，不新增依赖。 |
| U86 | 如实登记：这是标准库 API 用法修正 + 协议字段修正 + CI 约束，**不是第三方库替换**。 |

## 落地

| 编号 | 动作 |
| --- | --- |
| U87 | `src/core/leak.rs` 加 `fn lock() -> MutexGuard<'_, HashMap<K, Weak<V>>>`，`unwrap_or_else(PoisonError::into_inner)`；6 处调用点统一走它（含跨行的 `get()`）。 |
| U88 | `src/core/cache.rs` 加 `Cache::store_lock()` 与 `Flight::lock()` 两个恢复入口；7 处 `lock().unwrap()` 全部替换。 |
| U89 | `loader.take().expect("loader consumed once")` 改成 `match loader.take() { Some(f) => f(), None => return Err(CacheError::TimedOut) }`。循环里 loader 已取走时返回超时，不 panic。 |
| U90 | `src/core/envelope.rs` 加 `Kind::code()` 显式返回 `Request` / `Response` / `Event`；`to_json_string` 改用它，新增测试把三个协议值锁死。 |
| U91 | `scripts/panic_guard.py` 扫 `src/` 36 个文件非测试段，命中 `.lock().unwrap()` / `.expect(` / `panic!` / `unreachable!` / `todo!` / `unimplemented!` 即退出 1；白名单只列 `cache.rs` 构造函数的 `NonZeroUsize::new(capacity).expect("capacity > 0")`（前一行 `assert!(capacity > 0)` 保证）。 |
| U92 | `.github/workflows/ci.yml` 的 scan job 加 `panic_guard` step。后续新写的运行时 unwrap 会被 CI 挡住，不依赖改动作者自觉。 |
| U93 | `Cargo.toml` / `Cargo.lock` / `vendor/` **一行未动**，仍 26 包 / 25 第三方。 |

## 反向验证（真跑，不是推断）

把 U87 / U88 的恢复入口临时换回 `.unwrap()`，跑三个毒化测试：

```
core::cache::tests::poisoned_store_still_serves_cache      FAILED
core::cache::tests::poisoned_flight_state_does_not_crash_waiters FAILED
core::leak::tests::poisoned_registry_still_serves          FAILED
```

回显里出现 `panicked at src/core/cache.rs:64:27`、`src/core/cache.rs:45:27`、`src/core/leak.rs:22:25` 三处连锁 panic。恢复成 `PoisonError::into_inner` 后三个测试全部通过。这坐实了 U87–U89 修的是可达缺陷，不是纸面推断。临时备份文件已删，仓库无残留。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo test --offline --lib`：**266 / 0**（045 是 262；新增 cache 2 / leak 1 / envelope 1 共 4 个测试）。 |
| V-B | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0，28.45 s**、`plugin_abi_load` **6 / 0，69.88 s**。 |
| V-C | 合计 **292 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-D | `python3 scripts/panic_guard.py` → `PANIC_GUARD_OK files 36 hits 0`；`.github/workflows/ci.yml` yaml.safe_load 通过，jobs=core/scan。 |
| V-E | 必读 235 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，36 份 HTML 脚本通过。 |
| V-F | 界面闸门**未触发**：`demos/preview/` 与 `demos/ui-full-kcu-paper.html` 零 diff。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E81 | `leak.rs` 的 `get()` 把 `.lock()` 与 `.unwrap()` 拆成两行，首轮字符串替换漏掉，`panic_guard.py` 立刻报命中 | 单独重写该方法为单行 `self.lock().get(key)...`，复跑守卫通过 |
| E82 | `panic_guard.py` 白名单用「整行相等」比对，`let cap = ...` 与白名单字符串不匹配，误报 1 处 | 改成「文件 + 子串包含」匹配，A152 登记 |
| E83 | 全量 `cargo test --tests` 与交叉检查连续网关 502、工具结果不可用 | 拆 `--lib` / 两组 `--test` / lifecycle / abi / `check` 分段跑通，断言没降 |
| E84 | `src/core/envelope.rs` 的协议字段靠派生 Debug 输出，改名会静默改协议 | 加 `Kind::code()` 与三条断言锁死（U90） |

## 四值

| 项 | 值 |
| --- | --- |
| 两条 std 一手原文、U85–U93 落地 | 已证实 |
| 反向验证 3 个测试在 unwrap 版 FAILED、恢复后 PASS | 已证实 |
| 292 / 0、Windows GNU、panic_guard 零命中、零新增依赖 | 已证实 |
| E81–E84 四个真问题处置 | 已证实 |
| 第三方锁实现 | 未启动（U85 沿用 045 判定） |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| EQ-01 ~ EQ-12 十二条具体环境 | 已交（045），待拍板 |
| 后端仓写请求 | 0（已证实） |

# std::sync Mutex poisoning 一手资料（046）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://doc.rust-lang.org/std/sync/struct.Mutex.html | `pub fn lock(&self) -> LockResult<MutexGuard<'_, T>>`；「If another user of this mutex panicked while holding the mutex, then this call will return an error once the mutex is acquired. The acquired mutex guard will be contained in the returned error.」；「Once a mutex is poisoned, all other threads are unable to access the data by default」 | 已证实 |
| https://doc.rust-lang.org/std/sync/struct.Mutex.html | 「Poisoning is only advisory: the `PoisonError` type has an `into_inner` method which will return the guard that would have otherwise been returned on a successful lock.」 | 已证实 |
| https://doc.rust-lang.org/std/sync/struct.PoisonError.html | `pub fn into_inner(self) -> T`；「Consumes this error indicating that a lock is poisoned, returning the associated data.」；Mutex 与 RwLock 共用该语义 | 已证实 |
| https://doc.rust-lang.org/std/sync/struct.PoisonError.html | 「For a lock in the poisoned state, unless the state is cleared manually, all future acquisitions will return this error.」 | 已证实 |
| https://github.com/Amanieu/parking_lot/blob/parking_lot-v0.12.5/core/Cargo.toml | 045 判定：unix 分支 libc 0.2.95 是 026 受阻项，只换锁要拉 6 个新包，不重走 | 已证实 |

| 编号 | 结论 |
| --- | --- |
| R32 | `.lock().unwrap()` 不是局部写法问题：锁一旦被毒化，后续所有获取都返回 Err，调用点全部连锁 panic。缓存、在飞请求表、弱引用注册表三条路径同时受影响。 |
| R33 | `PoisonError::into_inner` 是标准库显式提供的恢复入口，注释写明「Poisoning is only advisory」。用它不需要第三方锁实现。 |
| R34 | 恢复后拿回的 guard 内数据可能处于不一致状态；日志缓冲、缓存条目、弱引用表都是可重建 / 可清理的容器，恢复后继续服务不会放大损坏。 |
| R35 | CI 守卫比人工自觉可靠：把危险调用列成可复跑的扫描项，新增调用点会立刻被挡住。 |

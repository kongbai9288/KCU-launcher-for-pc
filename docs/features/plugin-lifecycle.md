# F039-01 插件倒序卸载与失败回滚

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `PluginSet` 按加载顺序持有 `libloading::Library`；`push` 复用同一句柄做 ABI 判定；`load_many` 记 `base`，失败时 `rollback_to(base)` 倒序 close 本轮新增；`probe_scoped` 在 `crossbeam::thread::scope` 内并发读 ABI 并用 `WaitGroup` 确认归零；`unload_all` 倒序 pop + `Library::close()`，错误进 `UnloadReport.errors` 不中断。 |
| 开放了什么 | `src/plugins/lifecycle.rs`：`PluginSet` / `UnloadReport` / `new` / `len` / `is_empty` / `active_ids` / `push` / `load_many` / `probe_scoped` / `unload_all`；`src/plugins/mod.rs` 导出。 |
| 登记框架 | 挂在 038 的 ABI 契约之上，复用 `libloading`（038）与 `crossbeam-utils`（027）；不新增第三方 crate，不动关于页与 NOTICES。 |
| 用户使用逻辑 | 装一批插件时有一个没过 ABI 校验，只把这一批新加载的退掉，之前能用的照常用；退出或更新时按「后装的先退」释放，不会留半加载状态；重复 id 不会偷偷开两个句柄；再点一次卸载不会报错。插件代码不在宿主进程执行，崩溃不会拖走启动器。 |
| 性能 | `push` 单次打开、O(n) 查重、`Symbol` 不留长期引用；`probe_scoped` 由 scoped thread 自动 join，`WaitGroup::wait` 不阻塞即代表无在飞使用；集成夹具 `OnceLock` 缓存把编译次数从 10 降到 2，50.50 s。Windows GNU 目标 `cargo check` 通过；macOS / musl 的 dlclose 行为未证实。 |

状态：卸载生命周期已实现；子进程隔离与插件 init 执行未启动。

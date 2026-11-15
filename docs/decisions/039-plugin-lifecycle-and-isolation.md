# 第 039 轮：插件卸载顺序落地，隔离边界如实标未启动

| 项 | 值 |
| --- | --- |
| 编号 | 039 |
| 状态 | 卸载生命周期已实现已验证；**崩溃隔离未启动** |
| 依据 | docs/spec/39-round-039-instructions.txt |
| 前序 | 038-plugin-abi-libloading.md U19、037-plugin-upgrade-fault-icon.md、020 插件化更新约束 |
| 本轮性质 | 单轨轮：上层第三块的收尾 + 一处措辞纠正 |

## 先纠 038 的一处措辞

038 结尾写「下一轮走插件隔离与卸载顺序（不拉新闭包、**纯项目编排**）」。这个说法和你一直强调的「上层实现都用别人的代码」「对你的代码没有任何信心」是冲突的：项目编排恰恰是最容易出错、也最不该由我手写的一层。本轮按 038 的 U19 继续推进，但把能交给库的部分全部交出去，并在这里把措辞改掉。

| 项 | 038 措辞 | 039 实际 |
| --- | --- | --- |
| 句柄打开 / 符号解析 / 释放 | 已交给 `libloading` | 不变 |
| 并发符号读取与线程回收 | 未涉及 | 交给 `crossbeam-utils::thread::scope` + `WaitGroup`（027 已进构建） |
| 版本判定 | 已交给 `semver` | 不变 |
| 项目侧剩余 | 称为「纯项目编排」 | **150 行顺序策略**：倒序 pop、失败只回滚本轮新增、重复 id 拒绝。如实标：这一层没有语义等价的通用库可换 |

**零新增第三方 crate**：`Cargo.lock` 仍 17 包 / 16 第三方，关于页仍 16 组 / 38，NOTICES 与 CI 未改。

## 查到的硬事实：同进程 C ABI 接不住插件崩溃

这是本轮最该摆到台面上的一条。设置页那条「插件单独运行，不影响启动器」目前**只是演示**，不是已实现。

| 编号 | 事实 | 来源 |
| --- | --- | --- |
| F07 | 展开遇到不允许展开的 ABI 边界时，Rust `panic` 会让进程**安全 abort**；外部异常进入 Rust 是 UB | https://doc.rust-lang.org/nomicon/ffi.html |
| F08 | `extern "C"` + `panic=unwind` → panic 到边界 abort；`panic=abort` → 直接 abort；`extern "C-unwind"` 才允许穿过 | https://rust-lang.github.io/rfcs/2945-c-unwind-abi.html |
| F09 | `catch_unwind` 只抓 unwinding panic，不抓 abort 的；它与 foreign exception 的交互是未定义 | https://doc.rust-lang.org/std/panic/fn.catch_unwind.html |
| F10 | 因此 `kcu_plugin_init` **不在宿主进程执行**。插件 init 与主逻辑放到子进程边界后才能谈「崩溃不影响启动器」 | 由 F07–F09 推出 |
| F11 | `libloading::Symbol` 用 `PhantomData<&'lib Library>` 绑定库生命周期；`Library::close()` 才返回错误，Drop 会静默忽略；部分平台 `dlclose` 是 no-op、macOS 的 TLS 也会阻碍卸载 | https://docs.rs/crate/libloading/0.6.7/source/src/lib.rs 、 https://users.rust-lang.org/t/how-to-avoid-library-and-symbol-drops-in-crate-libloading/85701/9 |
| F12 | `Command` 参数不经 shell、字面量传递；**Child 的 Drop 既不 kill 也不 reap**，错误路径早返回会泄漏运行中的进程；Windows `.bat` / `.cmd` 是例外（CVE-2024-24576 / CVE-2024-43402，Rust 1.81.0） | https://doc.rust-lang.org/1.82.0/std/process/struct.Command.html |

| 编号 | 处置 |
| --- | --- |
| U20 | `src/plugins/` 只做加载、版本协商、符号数值读取与倒序释放；**不调用 `kcu_plugin_init`**，不让插件代码在宿主进程里跑起来。 |
| U21 | 子进程隔离标**未启动**。真做时走 `Command`（参数不经 shell）+ 显式 `wait` / `kill` + 避开 `.bat` / `.cmd` + 统一信封回传；不做 `Box::leak` 换 `'static`（F11 已说明那会失去卸载能力）。 |
| U22 | MSRV ≥ 1.81.0 才能安全处理 Windows 参数编码，与 011 定的 Win7 Tier 3 + build-std 路线可能冲突，标**未证实**，本轮不改工具链。 |
| U23 | `close()` 成功不等于「已卸载」（F11）；`UnloadReport.errors` 登记 close 错误但不中断后续释放，不把 close 失败伪装成成功。 |
| U24 | 界面层**不改**：设置里那条隔离口径保持原样，不加「未实现」标签（按 021 轮「强调这些是废话」的口径），真实状态只在文档登记。 |

## 落地内容

`src/plugins/lifecycle.rs` 150 行：

| 编号 | 规则 |
| --- | --- |
| U25 | `push`：同 id 先拒；`abi::open` 只打开一次，复用同一句柄做 `read_abi` + `compatible`，不重复 dlopen；ABI 不过时句柄随作用域 Drop。 |
| U26 | `load_many`：记 `base`，任一失败 `rollback_to(base)` 倒序释放**本轮新增**，之前已加载的保持可用；错误带出失败的插件 id。 |
| U27 | `probe_scoped`：`crossbeam::thread::scope` 里对每个库 spawn 一个读 ABI 的线程，`WaitGroup` 在所有引用 drop 后 `wait()` 返回，证明无在飞符号使用；`Symbol` 不存进结构体（038 U17）。 |
| U28 | `unload_all`：倒序 `pop` + `Library::close()`，重复调用幂等；返回 `UnloadReport { unloaded, errors }`。 |
| U29 | 顺序是「符号使用 → scope join → 倒序卸载」，与 F11 的父子释放次序一致；不先卸库再读符号。 |

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo build --offline` 通过；`cargo check --offline --target x86_64-pc-windows-gnu` 通过（038 加的交叉检查仍成立）。 |
| V-B | `cargo test --offline --lib`：**216 / 0**（038 是 212，新增 4 个生命周期单测）。 |
| V-C | `cargo test --offline --test plugin_lifecycle_load`：**7 / 0，50.50 s**。真加载 3 个 `.so`、倒序卸载、scope 读符号、重复 id、ABI 不符回滚、二次卸载、卸载后归零、缺路径回滚。 |
| V-D | `cargo test --offline --test plugin_abi_load`：**6 / 0，125.71 s**（038 回归）。 |
| V-E | 合计 **229 / 0**。夹具用 `OnceLock` 缓存 2 个 cdylib，把集成段从 10 次 rustc 编译降到 2 次；039 的 50.50 s 对比 038 的 133.97 s，缓存命中直接省掉重复编译。 |
| V-F | 网关连续 4 次 502 后，拆成 `--lib` / `--test` / `check` 三段各自跑通；命令拆分与夹具缓存都留痕，未改断言。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E46 | `read_abi(...).map(...) == Ok(ABI_MAJOR)` 报 E0369，`anyhow::Error` 不实现 `PartialEq` | 改 `matches!(read_abi(lib), Ok(a) if a.major == ABI_MAJOR)` |
| E47 | `filter(|h| h.join()...)` 里 `ScopedJoinHandle::join` 消耗 self，报 E0507 | 改 `into_iter().filter_map(|h| h.join().ok()).filter(|ok| *ok).count()` |
| E48 | `PluginSet` derive `Debug` 但内部 `Loaded` 没有，报 E0277 | `Loaded` 补 `#[derive(Debug)]`，`Library` 本身实现 Debug |
| E49 | 单测 `let s = PluginSet::new()` 后调 `unload_all()` 报 E0596 | 改 `let mut s` |
| E50 | 全量 `cargo test` 连续 4 次网关 502 | 拆三段执行；集成夹具改 `OnceLock` 缓存，耗时从 ~134 s 降到 50.50 s，未降验收项 |
| E51 | 初版留了两个只被单测调用的纯函数（`has_id` / `reverse_order`） | 删掉，行为验证全部移到真加载集成测试，避免为测试造生产代码 |

## 四值

| 项 | 值 |
| --- | --- |
| 卸载顺序 / 回滚 / scope 归零 / 229 测试 / 零新增依赖 | 已证实 |
| F07–F12 六条一手事实、U20–U29 规则 | 已证实 |
| 同进程 C ABI 无法隔离崩溃、设置页隔离项只是演示 | 已证实 |
| 子进程隔离、真实 `.dll`、插件 init 执行、卸载顺序在 macOS / musl 的实测 | 未启动 / 未证实 |
| MSVC 目标、Win7 运行时、MSRV ≥1.81 与 Tier 3 冲突 | 未证实 / 受阻 |
| 界面闸门 | 未触发（界面与 56 张 PNG 全部不动） |
| 后端仓写请求 | 0（已证实） |

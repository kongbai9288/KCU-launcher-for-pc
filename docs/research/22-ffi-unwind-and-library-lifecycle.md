# 跨 FFI 展开与动态库生命周期一手资料（039）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://doc.rust-lang.org/nomicon/ffi.html | 展开遇到不允许展开的 ABI 边界时，Rust panic 会让进程安全中止；外部异常进入 Rust 是未定义行为；`catch_unwind` 与外部异常交互未定义 | 已证实（页面直抓） |
| https://rust-lang.github.io/rfcs/2945-c-unwind-abi.html | `extern "C"` + `panic=unwind` → panic 到边界 abort；`panic=abort` → 直接 abort；`"C-unwind"` 允许穿过；`"C"` 与 `"C-unwind"` 之间无函数指针 coercion | 已证实 |
| https://doc.rust-lang.org/std/panic/fn.catch_unwind.html | 只抓 unwinding panic，不抓 abort 的；跨 foreign exception 捕获行为未指定 | 已证实 |
| https://docs.rs/crate/libloading/0.6.7/source/src/lib.rs | `Symbol<'lib, T>` 用 `PhantomData` 绑定 `Library`；`Library::close(self)` 才返回错误，Drop 忽略错误；底层数据结构在 close 出错时仍可能泄漏 | 已证实 |
| https://users.rust-lang.org/t/how-to-avoid-library-and-symbol-drops-in-crate-libloading/85701/9 | musl 的 `dlclose` 是 no-op；macOS 仅在部分情况支持卸载，TLS 会阻碍；`Box::leak` 换取 `'static` 会失去卸载能力 | 已证实（社区讨论，含 rustc 贡献者回复） |
| https://doc.rust-lang.org/1.82.0/std/process/struct.Command.html | 参数不经 shell、字面量传递；`cmd.exe` / `.bat` 用非标准解码，恶意参数可执行任意命令；`Child` 无 Drop 实现，句柄离开作用域后进程仍运行 | 已证实 |
| https://dev-doc.rust-lang.org/src/std/process.rs.html | `Command::new("ls -l")` 会按字面量找程序；参数必须逐个 `.arg` 传入 | 已证实 |
| https://doc.rust-lang.net.cn/1.79.0/nomicon/ffi.html | 中文镜像同口径：非 `-unwind` ABI 边界上 panic 导致进程安全中止 | 已证实（交叉核对） |
| Win7 Tier 3 + build-std 下 MSRV ≥ 1.81.0 与 `windows-link` raw-dylib 的共存 | 运行时验证 | 受阻 |

| 编号 | 结论 |
| --- | --- |
| R04 | 同进程 `"C"` ABI 动态库无法隔离插件 panic，任何「插件崩了不影响启动器」的承诺都必须落在子进程边界上。 |
| R05 | 因此 038 契约里的 `kcu_plugin_init` 不能在宿主进程调用；符号只读取数值，不执行插件函数。 |
| R06 | 卸载顺序必须遵循父（Library）晚于子（Symbol）释放；`close()` 的错误要登记，不能静默当成功。 |
| R07 | 子进程路线里 `Child` 必须显式回收，错误路径早返回会泄漏运行中的进程，这与 014 的 CancelToken / join 回收是同一类问题。 |
| R08 | `Command` 在 Windows 的 `.bat` / `.cmd` 例外要求 MSRV ≥ 1.81.0；该前置与 011 定的 Win7 路线冲突，未证实前不写进构建约束。 |

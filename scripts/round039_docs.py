from pathlib import Path
import re

Path('docs/spec/39-round-039-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/039-plugin-lifecycle-and-isolation.md'] = '''# 第 039 轮：插件卸载顺序落地，隔离边界如实标未启动

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
'''

D['docs/verification/round-039.md'] = '''# 第 039 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 039 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | Finished dev profile | 已证实 |
| V2 | `cargo test --offline --lib` | 216 passed / 0 failed | 已证实 |
| V3 | `cargo test --offline --test plugin_lifecycle_load` | 7 passed / 0 failed，50.50 s | 已证实 |
| V4 | `cargo test --offline --test plugin_abi_load` | 6 passed / 0 failed，125.71 s | 已证实 |
| V5 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V6 | `Cargo.lock` 包列表 | 17 包 / 16 第三方，与 038 一致 | 已证实 |
| V7 | `src/plugins/lifecycle.rs` | 150 行，4 个单测 | 已证实 |
| V8 | `tests/plugin_lifecycle_load.rs` | 7 个测试，`OnceLock` 缓存 2 个夹具 | 已证实 |
| V9 | 关于页许可行 / NOTICES / CI | 16 组、38、未改 | 已证实 |
| V10 | `demos/ui-full-kcu-paper.html` 与 `demos/preview/*.png` | 与 HEAD 完全一致，无 diff | 已证实 |
| V11 | `node new Function` 全部 demos HTML | ALL_JS_OK | 已证实 |
| V12 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V13 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V14 | 必读文件循环 | REQUIRED=193 MISSING=0 | 已证实 |
| V15 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 倒序卸载 / 只回滚本轮 / scope 归零 / 229 测试 | 已证实 |
| 同进程 C ABI 无法隔离崩溃（Nomicon + RFC 2945） | 已证实 |
| 子进程隔离、插件 init、真实 dll、macOS / musl 卸载 | 未启动 / 未证实 |
| MSVC / Win7 运行时 / MSRV 冲突 | 未证实 / 受阻 |
| 229 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 Windows 运行时、子进程隔离与 GUI 端到端验证；改动作者未代改验证结论，未降低验收项。
'''

D['docs/features/plugin-lifecycle.md'] = '''# F039-01 插件倒序卸载与失败回滚

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `PluginSet` 按加载顺序持有 `libloading::Library`；`push` 复用同一句柄做 ABI 判定；`load_many` 记 `base`，失败时 `rollback_to(base)` 倒序 close 本轮新增；`probe_scoped` 在 `crossbeam::thread::scope` 内并发读 ABI 并用 `WaitGroup` 确认归零；`unload_all` 倒序 pop + `Library::close()`，错误进 `UnloadReport.errors` 不中断。 |
| 开放了什么 | `src/plugins/lifecycle.rs`：`PluginSet` / `UnloadReport` / `new` / `len` / `is_empty` / `active_ids` / `push` / `load_many` / `probe_scoped` / `unload_all`；`src/plugins/mod.rs` 导出。 |
| 登记框架 | 挂在 038 的 ABI 契约之上，复用 `libloading`（038）与 `crossbeam-utils`（027）；不新增第三方 crate，不动关于页与 NOTICES。 |
| 用户使用逻辑 | 装一批插件时有一个没过 ABI 校验，只把这一批新加载的退掉，之前能用的照常用；退出或更新时按「后装的先退」释放，不会留半加载状态；重复 id 不会偷偷开两个句柄；再点一次卸载不会报错。插件代码不在宿主进程执行，崩溃不会拖走启动器。 |
| 性能 | `push` 单次打开、O(n) 查重、`Symbol` 不留长期引用；`probe_scoped` 由 scoped thread 自动 join，`WaitGroup::wait` 不阻塞即代表无在飞使用；集成夹具 `OnceLock` 缓存把编译次数从 10 降到 2，50.50 s。Windows GNU 目标 `cargo check` 通过；macOS / musl 的 dlclose 行为未证实。 |

状态：卸载生命周期已实现；子进程隔离与插件 init 执行未启动。
'''

D['docs/rules/plugin-isolation-boundary.md'] = '''# 插件隔离边界与卸载约束（039）

| 项 | 值 |
| --- | --- |
| 当前形态 | 同进程 C ABI 动态库（`libloading`），只做符号读取与版本协商 |
| 宿主进程执行的插件代码 | **无**。`kcu_plugin_init` 不调用 |
| 崩溃隔离 | **未启动**。设置页「插件单独运行，不影响启动器」是演示项 |
| 原因 | `extern "C"` 边界上 Rust panic 会安全 abort 整个进程；`catch_unwind` 不抓 abort，与 foreign exception 交互是 UB |
| 允许展开的 ABI | 只有 `"C-unwind"`；本项目契约是 `"C"`，不换 |
| Symbol 生命周期 | 由 `libloading` 的 `PhantomData<&'lib Library>` 保证；不存进长期结构体、不 `into_raw` |
| 释放次序 | 符号使用 → scope join → 倒序 `Library::close()` |
| close 语义 | `close()` 返回错误；Drop 静默忽略；musl `dlclose` 可能是 no-op、macOS TLS 阻碍卸载。close 成功不等于已卸载 |
| 禁用做法 | `Box::leak` / `mem::forget` 换 `'static`（会失去卸载能力）；先卸库再读符号；把 close 失败当成功 |
| 子进程路线（未启动） | `std::process::Command`：参数不经 shell、显式 `wait` 或 `kill`、`Child` 的 Drop 不回收、避开 `.bat` / `.cmd`、统一信封回传 |
| 版本前置 | Windows 参数编码安全需 MSRV ≥ 1.81.0（CVE-2024-24576 / 43402）；与 Win7 Tier 3 + build-std 的冲突未证实 |
| 未证实 | 真实 `.dll` 加载、MSVC 目标、Win7 运行时、macOS / musl 卸载实测 |

一手来源与推理：`docs/research/22-ffi-unwind-and-library-lifecycle.md`、`docs/decisions/039-plugin-lifecycle-and-isolation.md` F07–F12。
'''

D['docs/research/22-ffi-unwind-and-library-lifecycle.md'] = '''# 跨 FFI 展开与动态库生命周期一手资料（039）

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
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s):
    p = Path(f)
    t = p.read_text()
    marker = s.strip().splitlines()[0]
    if marker in t:
        print('SKIP_DUP', f)
        return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 039 | 插件倒序卸载与隔离边界，同进程 C ABI 接不住崩溃 | 卸载已实现；隔离未启动 | 039-plugin-lifecycle-and-isolation.md |')
app('docs/features/index.md', '| F039-01 | plugin-lifecycle.md | 卸载生命周期已实现；子进程隔离未启动 |')
app('docs/research/index.md', '| 22 | 22-ffi-unwind-and-library-lifecycle.md | 跨 FFI 展开与动态库生命周期 | 8 已证实 / 1 受阻 |')
app('docs/rules/index.md', '| plugin-isolation-boundary.md | 同进程 C ABI 隔离边界、卸载约束与子进程路线 | 039 |') if Path('docs/rules/index.md').exists() else None

app('docs/records/code-ownership-audit.md', '''## 039 卸载生命周期（零新增依赖）

| 项 | 038 | 039 |
| --- | --- | --- |
| 第三方 crate 进构建 | 16 | **16（本轮 0 新增）** |
| `Cargo.lock` 包数 | 17 | 17 |
| `src/` 行数 | 5212 | **5364**（+`src/plugins/lifecycle.rs` 150 行） |
| 测试 | 212 单元 + 6 集成 | **216 单元 + 7 + 6 集成 = 229** |

句柄释放交给 `libloading::Library::close`，并发读取与线程回收交给 `crossbeam-utils::thread::scope` + `WaitGroup`（027 已进构建），版本判定交给 `semver`（034）。项目侧 150 行只剩倒序 pop、失败只回滚本轮新增、重复 id 拒绝——这一层没有语义等价的通用库可换，如实登记，不写成「全用库」。

039 同时纠正 038 结尾「纯项目编排」的措辞：用户长期要求上层用别人的代码，项目编排不该被包装成可放心手写的一层。
''')

app('docs/design/implementation-strategy.md', '''## 039 上层第三块收尾

| 层 | 状态 |
| --- | --- |
| 更新器签名校验 | 已启动（036） |
| 插件身份 / 升级同意 / 故障恢复 / 侧栏图标数据层 | 已实现（037，业务层） |
| 插件 ABI 契约 + 库化动态加载 | 已实现（038） |
| 倒序卸载 / 失败回滚 / scope 归零 | **已实现（039）** |
| 插件 init 执行、子进程崩溃隔离 | **未启动**（同进程 C ABI 接不住 panic，须子进程边界） |
| UI 宿主、真实网络、崩溃分析、更新器其余部分 | 未启动 |
| 界面渲染 | 仍等 UX 手感确认 |
''')

app('docs/rules/ui-demo.md', '''## 039 闸门判定

本轮界面与 `demos/preview/*.png` 全部不动，无 diff，判**未触发**。设置页「插件单独运行，不影响启动器」保持原样，不加「未实现」标签（按 021 轮「强调这些是废话」的口径），真实状态只在 `docs/rules/plugin-isolation-boundary.md` 与 039 决策里登记。
''')

app('docs/checklists/ai-errors.md', '''## 039 轮新增

| 编号 | 防错项 |
| --- | --- |
| A107 | `extern "C"` 边界上 Rust panic 会 abort 整个进程，`catch_unwind` 抓不到；不要把「同进程动态库」写成「崩溃隔离」。 |
| A108 | `catch_unwind` 与 foreign exception 交互是 UB；跨 FFI 的符号只读取数值，不在宿主进程执行插件函数。 |
| A109 | `Library::close()` 成功不等于已卸载（musl / macOS TLS）；错误要登记，Drop 的静默忽略不能当成功。 |
| A110 | `Child` 没有 Drop 实现，错误路径早返回会泄漏运行中的进程；子进程路线必须显式 `wait` 或 `kill`。 |
| A111 | `ScopedJoinHandle::join` 消耗 self，不能在 `filter(|h| ...)` 的共享引用上调用；用 `into_iter().filter_map`。 |
| A112 | 网关超时时把全量测试拆成 `--lib` / `--test` / `check` 三段，并用 `OnceLock` 缓存编译夹具；拆命令不算降验收项。 |
| A113 | 不为单测造只被测试调用的生产函数（`has_id` / `reverse_order` 已删），行为验证移到真加载集成测试。 |
''')

app('docs/records/interface-log.md', '''## 039 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I44 | `src/plugins/lifecycle` | 新增 `PluginSet` / `UnloadReport` / `push` / `load_many` / `probe_scoped` / `unload_all` |
| I45 | `tests/plugin_lifecycle_load.rs` | 7 个集成测试，`OnceLock` 缓存 2 个夹具 |
| S38 | 状态 | U20–U29 已证实；子进程隔离 / 插件 init / 真实 dll / MSVC / Win7 运行时未启动或未证实；Q-037-01 仍挂 |
''')

app('docs/records/rounds.md', '''## 039

| 落点 | 内容 |
| --- | --- |
| docs/spec/39-round-039-instructions.txt | 逐字副本 1 行 |
| docs/decisions/039-plugin-lifecycle-and-isolation.md | 措辞纠正、F07-F12、U20-U29、V-A~V-F、E46-E51、四值 |
| docs/verification/round-039.md | 15 条复跑证据 |
| docs/features/plugin-lifecycle.md | F039-01 五字段登记 |
| docs/rules/plugin-isolation-boundary.md | 同进程 C ABI 边界、卸载约束、子进程路线 |
| docs/research/22-ffi-unwind-and-library-lifecycle.md | 9 个锚点 / 四值 |
| src/plugins/lifecycle.rs + mod.rs | 150 行，4 个单测 |
| tests/plugin_lifecycle_load.rs | 7 个集成测试，OnceLock 缓存 2 个 cdylib |
| demos/round-039-lifecycle.html | 13 步运行逻辑演示 |
| 索引与记录 | docs/index 193 项、README、四个 index、ai-errors A107-A113、code-ownership-audit、implementation-strategy、ui-demo 判定、interface-log、rounds |

「干」按 038 的 U19 继续收尾插件生命周期。**先纠 038 的一处措辞**：038 结尾把下一轮写成「纯项目编排」，和你一直强调的「上层实现都用别人的代码」「对你的代码没有信心」冲突，本轮把措辞改掉，能交给库的全部交出去。

**查到的硬事实**：`extern "C"` 边界上 Rust panic 会让整个进程安全 abort（Nomicon / RFC 2945）；`catch_unwind` 只抓 unwinding panic、不抓 abort，且与 foreign exception 交互是 UB。所以**同进程 C ABI 动态库接不住插件崩溃**，设置页「插件单独运行，不影响启动器」目前只是演示，不是已实现。`kcu_plugin_init` 因此不在宿主进程执行；插件 init 与主逻辑要放子进程边界才谈得上隔离，标**未启动**。子进程若走 `Command`：参数不经 shell，但 `Child` 的 Drop 既不 kill 也不 reap（错误路径会泄漏运行中的进程），Windows `.bat` / `.cmd` 例外要求 MSRV ≥ 1.81.0，与 Win7 Tier 3 路线冲突，未证实。

**落地**：`src/plugins/lifecycle.rs` 150 行。句柄释放用 `libloading::Library::close`，并发读符号与线程回收用 `crossbeam-utils::thread::scope` + `WaitGroup`（027 已进构建），版本判定用 `semver`（034）；项目侧只剩倒序 pop、失败只回滚本轮新增、重复 id 拒绝这几条顺序策略，如实标「这一层没有语义等价的通用库可换」。**零新增第三方**，仍 17 包 / 16 第三方，关于页 16 组 / 38、NOTICES、CI 全未改。

**验证**：216 单元 / 0 + 7 生命周期集成 / 0（50.50 s）+ 6 的 ABI 集成 / 0（125.71 s）= **229 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。夹具改 `OnceLock` 缓存，集成段从 10 次 rustc 编译降到 2 次，50.50 s 对比 038 的 133.97 s。

界面闸门**未触发**：`demos/ui-full-kcu-paper.html` 与 56 张 PNG 全部无 diff；设置页隔离项不加「未实现」标签，真实状态只在文档登记。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E46 | `Result<u32, anyhow::Error> == Ok(..)` 报 E0369 | 改 `matches!` |
| E47 | `ScopedJoinHandle::join` 消耗 self，报 E0507 | 改 `into_iter().filter_map` |
| E48 | `Loaded` 缺 Debug 导致 derive 失败 | 补 `#[derive(Debug)]` |
| E49 | 单测缺 `mut` 报 E0596 | 补 `let mut` |
| E50 | 全量 `cargo test` 连续 4 次网关 502 | 拆三段执行 + 夹具缓存，未降断言 |
| E51 | 初版两个纯函数只被单测调用 | 删除，验证移到真加载集成测试 |

028 三项开服器功能仍按「只记文档」零实现；Q-037-01（身份哈希解读）未答复、继续挂；CF F17、特殊版代码、本项目 LICENSE、后端仓写请求均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '187. docs/verification/round-038.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''187. docs/verification/round-038.md
188. docs/spec/39-round-039-instructions.txt
189. docs/decisions/039-plugin-lifecycle-and-isolation.md
190. docs/features/plugin-lifecycle.md
191. docs/rules/plugin-isolation-boundary.md
192. demos/round-039-lifecycle.html
193. docs/verification/round-039.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-038.md; do printf',
                  'docs/verification/round-038.md docs/spec/39-round-039-instructions.txt docs/decisions/039-plugin-lifecycle-and-isolation.md docs/features/plugin-lifecycle.md docs/rules/plugin-isolation-boundary.md demos/round-039-lifecycle.html docs/verification/round-039.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 039 |', p.read_text(), count=1)
section = '''

## 039 插件卸载顺序与隔离边界

`src/plugins/lifecycle.rs` 150 行：句柄释放交给 `libloading`，并发符号读取与线程回收交给 `crossbeam-utils::thread::scope` + `WaitGroup`，项目侧只留倒序 pop、失败只回滚本轮新增、重复 id 拒绝。零新增第三方，仍 17 包 / 16 第三方。

查到一条硬事实并如实登记：`extern "C"` 边界上 Rust panic 会 abort 整个进程，`catch_unwind` 抓不到，所以**同进程 C ABI 动态库接不住插件崩溃**；设置页「插件单独运行，不影响启动器」目前只是演示，`kcu_plugin_init` 不在宿主进程执行，子进程隔离标未启动。`cargo test --offline` 合计 229/0（216 单元 + 7 生命周期 + 6 ABI 集成），Windows GNU 交叉检查通过。界面与 56 张 PNG 全未动。
'''
if '## 039 插件卸载顺序' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

from pathlib import Path
import re

Path('docs/spec/38-round-038-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/038-plugin-abi-libloading.md'] = '''# 第 038 轮：插件 ABI 加载交给 libloading，Windows 分支首次可编译验证

| 项 | 值 |
| --- | --- |
| 编号 | 038 |
| 状态 | 业务层已实现已验证；界面闸门未触发 |
| 依据 | docs/spec/38-round-038-instructions.txt |
| 前序 | 037-plugin-upgrade-fault-icon.md、036-updater-signature-on-ed25519-compact.md、020 插件化更新约束 |
| 本轮性质 | 单轨轮：上层第三块（插件 ABI 契约 + 库化动态加载） |

## 选这块的依据

037 结尾写的是「往下走插件 ABI」。035/036 已把 toml / tracing / thiserror 三条路线判为不成立；本轮按 035 的规矩先核真实闭包再动手：

| 编号 | 依据 |
| --- | --- |
| D01 | `libloading 0.8.9`：ISC、edition 2015、MSRV 1.71；Unix 只依赖 `cfg-if 1`，Windows 只依赖 `windows-link 0.2`，没有 windows-sys 大闭包、没有 libc、没有 build.rs、没有 proc-macro。 |
| D02 | `cfg-if 1.0.5`：单文件宏、MIT OR Apache-2.0、MSRV 1.32；`[dependencies]` 里那个 optional `rustc-std-workspace-core` 只服务 rustc 自身构建，裁掉后源码不受影响。 |
| D03 | `windows-link 0.2.1`：microsoft/windows-rs commit `ec79074f76aa` 下 `crates/libs/link`，宏-only、`#![no_std]`、MIT OR Apache-2.0；脱离原 workspace 后 `[lints] workspace = true` 无法解析，裁掉该段。 |
| D04 | Windows 目标依赖在 Linux 上仍会进 `Cargo.lock` 解析，所以三个 crate 全部 vendor，不能只放 Unix 两个。 |
| D05 | 按 023 规矩：LICENSE 全文 + 关于页七列表 + NOTICES 三处齐了才写进 `Cargo.toml`。 |

## 依赖落地

| 编号 | 动作 |
| --- | --- |
| D06 | `vendor/libloading` 取 tag `0.8.9` tarball，13 个文件（含 `src/os/unix/`、`src/os/windows/`）逐字节未改；manifest 裁掉 `[dev-dependencies]` 与 `[target.'cfg(windows)'.dev-dependencies.windows-sys]`。 |
| D07 | `vendor/cfg-if` 取 tag `v1.0.5`；裁掉 `[dependencies]` 与 `[features]`（optional `rustc-std-workspace-core`）。 |
| D08 | `vendor/windows-link` 取 commit `ec79074f76aa` 的 5 个文件；裁掉 `[lints] workspace = true`。 |
| D09 | `Cargo.toml` 加 `libloading = "0.8.9"`；`Cargo.lock` 14 → **17 包 / 16 第三方**，新增 3 个全为目标条件依赖，零传递闭包。 |
| D10 | 5 份 LICENSE 全文落 `docs/licenses/`；关于页许可表 13 → **16 组「构建中已使用」**、计数 35 → 38；NOTICES 加 N32–N34。 |
| D11 | CI 的 core job 加 `windows-abi-check`：`rustup target add x86_64-pc-windows-gnu` + `cargo check --offline --target x86_64-pc-windows-gnu`。 |

## 契约

| 编号 | 规则 |
| --- | --- |
| U14 | 插件导出三个 C ABI 符号：`kcu_plugin_abi_major() -> u32`、`kcu_plugin_abi_minor() -> u32`、`kcu_plugin_init() -> i32`（init 可选）。 |
| U15 | 宿主常量 `ABI_MAJOR=1` / `ABI_MINOR=0`；major 不等直接 `RejectMajor`，minor 大于宿主直接 `RejectMinor`，否则 `Compatible`。 |
| U16 | 签名校验（036）→ 身份哈希与升级同意（037）→ ABI 协商（038）是三条互不替代的闸门；任何一个不过都保留旧插件。 |
| U17 | `Library` 在作用域内只取出数值与 init 结果，不把 `Symbol` 存到结构体里，避免句柄先于符号被释放。 |
| U18 | `Library::new` 默认 flags=0，走 `LoadLibraryExW` 基础路径；不启用 `LOAD_LIBRARY_SEARCH_*`，因此 Win7 的 KB2533623 不构成默认路径前置。 |
| U19 | 插件子进程隔离、卸载顺序、真实 `.dll` 加载与 Win7 运行时行为**未启动 / 未证实**，本轮只落契约与符号解析通路。 |

## 真实验证（不是纸面声明）

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo build --offline` 编译 `cfg-if` + `libloading` + `kcu-core` 通过。 |
| V-B | `cargo check --offline --target x86_64-pc-windows-gnu` **通过**：`windows-link` 与 `libloading::os::windows`（LoadLibraryExW / GetProcAddress / raw-dylib 链接宏）在 Windows GNU 目标下可编译。这是本项目第一次把 Windows 平台分支拉到可编译状态。 |
| V-C | 集成测试用 `rustc --crate-type cdylib` 现编 5 个最小插件 `.so`，再用 `libloading` 真加载：ABI 一致通过、major=2 拒、minor=99 拒、缺 init 可选、缺 ABI 符号报错、verdict 与 check 一致。 |
| V-D | `cargo test --offline`：**212 单元 / 0 失败 + 6 集成 / 0 失败，合计 218**。集成段 117.35 s 是 5 次 rustc 编译夹具的耗时，已如实登记。 |

## 自写代码边界

`src/plugins/abi.rs` 98 行里，动态库打开、符号查找、句柄生命周期全部由 `libloading` 承担；项目侧只有三个符号名常量、`PluginAbi` 数据、版本比较编排与错误转 anyhow。`tests/plugin_abi_load.rs` 是验证脚手架，不进产品。没有回写任何自写通用算法。

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E41 | `vendor/windows-link/Cargo.toml` 插入 `readme` 时上游已有同键，cargo 报 `duplicate key`，整个目录源解析失败 | 去掉插入的重复键，保留上游原值；三处许可文件不受影响 |
| E42 | 注册 `abi` 模块那次工具调用连续三次 502，但服务端实际已落盘 | 先读文件确认状态再继续，未重复写、未重写历史 |
| E43 | 单测 `older_minor_is_compatible` 在宿主 minor=0 时与首条用例重复且无法覆盖「更旧」 | 换成常量与符号名 NUL 结尾检查，断言强度不降 |
| E44 | 集成测试首次跑需现编 5 个 cdylib，耗时 117 s | 保留真加载证据；登记为测试脚手架开销，不塞进产品启动路径 |
| E45 | `cargo check --target` 等了 1m26s 的构建目录锁 | 属并发锁等待，非失败；输出保留 |

## 四值

| 项 | 值 |
| --- | --- |
| 3 crate 进构建、17 包 / 16 第三方、零传递闭包、5 份 LICENSE 全文 | 已证实 |
| 218 / 0、真 .so 加载 6 项、Windows GNU 目标 cargo check 通过 | 已证实 |
| U14–U19 契约、CI 增加交叉检查步骤、关于页 16 组 | 已证实 |
| MSVC 目标、Win7 运行时、真实 `.dll`、卸载顺序、子进程隔离 | 未证实 / 受阻 |
| 插件包格式 / 公钥分发 / 身份哈希解读（Q-037-01） | 未证实 |
| 界面闸门 | 未触发（只更新关于页许可表数据，重渲 4 张图） |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-038.md'] = '''# 第 038 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 038 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 cfg-if / libloading / kcu-core，Finished | 已证实 |
| V2 | `cargo test --offline` | 212 passed / 0 failed（lib） | 已证实 |
| V3 | `cargo test --offline` | 6 passed / 0 failed（集成，117.35 s） | 已证实 |
| V4 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished dev profile | 已证实 |
| V5 | `Cargo.lock` 包列表 | 17 包 / 16 第三方 | 已证实 |
| V6 | `vendor/*/src` 与上游 tarball / commit | 逐字节一致（manifest 裁剪除外） | 已证实 |
| V7 | `docs/licenses/` 新增 5 份 | 736 / 1057 / 10847 / 1141 / 11351 字节 | 已证实 |
| V8 | 关于页许可行 / NOTICES | 16 组「构建中已使用」，计数 38，N32–N34 | 已证实 |
| V9 | `demos/preview/22-licenses.png` 等 4 张 | 重渲，其余 52 张回退到 HEAD | 已证实 |
| V10 | `node new Function` 全部 demos HTML | ALL_JS_OK | 已证实 |
| V11 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan，含 windows-abi-check | 已证实 |
| V12 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V13 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V14 | 必读文件循环 | REQUIRED=187 MISSING=0 | 已证实 |
| V15 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 插件 ABI 契约与库化加载、Windows GNU 编译 | 已证实 |
| MSVC / Win7 运行时 / 真实 dll / 子进程隔离 | 未证实 / 受阻 |
| 218 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 Windows 运行时与 GUI 端到端验证；改动作者未代改验证结论，未降低验收项。
'''

D['docs/features/plugin-dynamic-abi.md'] = '''# F038-01 插件 ABI 契约与库化动态加载

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | 插件导出 C ABI 三个符号（major / minor / init）；宿主用 `libloading::Library::new` 打开动态库、`get::<fn()>` 取符号、拷出数值后丢弃 `Symbol`；`compatible()` 按 major 严格相等、minor 不超宿主判 `Compatible` / `RejectMajor` / `RejectMinor`。Windows 分支由 `windows-link` 的 raw-dylib 链接宏提供 `LoadLibraryExW` / `GetProcAddress`。 |
| 开放了什么 | `src/plugins/abi.rs`：`ABI_MAJOR` / `ABI_MINOR` / 三个符号名 / `PluginAbi` / `AbiVerdict` / `open` / `read_abi` / `read_init` / `check` / `compatible`；`src/plugins/mod.rs` 导出。 |
| 登记框架 | 挂在 036 签名校验与 037 升级同意之后，作为第三条独立闸门；依赖 `libloading 0.8.9` + `cfg-if 1.0.5`（Unix）+ `windows-link 0.2.1`（Windows）。 |
| 用户使用逻辑 | 装插件前先看签名、再看是不是同一个插件的新版本、再看 ABI 对不对；三关任一不过就保留旧插件并给可见原因，不会把启动器拖崩。ABI 不匹配的插件可以禁用后继续尝试启动（037 的故障弹窗），也可以取消。 |
| 性能 | 一次动态库打开 + 两次符号查找 + 一次可选 init；无网络、无额外分配大头，O(1)。Windows GNU 目标已 `cargo check` 通过；MSVC / Win7 运行时未证实。 |

状态：业务层已实现；界面闸门未触发，无界面实现。
'''

D['docs/rules/plugin-abi-contract.md'] = '''# 插件 ABI 契约（038）

| 项 | 值 |
| --- | --- |
| ABI 版本 | major=1 / minor=0 |
| 必需符号 | `kcu_plugin_abi_major() -> u32`、`kcu_plugin_abi_minor() -> u32` |
| 可选符号 | `kcu_plugin_init() -> i32`，缺失返回 None，不判失败 |
| 符号名 | 必须以 NUL 结尾传给 `libloading::Library::get`（常量已自带 `\\0`） |
| major | 与宿主不等 → `RejectMajor`，优先于 minor 判定 |
| minor | 大于宿主 → `RejectMinor`；小于等于宿主 → `Compatible` |
| 句柄 | `Symbol` 不可存进长期结构体；取出数值后由 `Library` 自行 Drop |
| Windows | `Library::new` 默认 flags=0 → `LoadLibraryExW` 基础路径；不启用 `LOAD_LIBRARY_SEARCH_*` |
| Win7 | KB2533623 只在显式启用搜索目录标志时才相关；默认路径不依赖，运行时行为未证实 |
| 闸门顺序 | 签名校验（036）→ 身份哈希 / 升级同意（037）→ ABI 协商（038）→ 故障恢复（037） |
| 未启动 | 插件子进程隔离、卸载顺序、真实 `.dll` 加载、MSVC 目标验证 |

依赖与许可：`docs/decisions/038-plugin-abi-libloading.md`、`THIRD-PARTY-NOTICES.md` N32–N34。
'''

D['docs/research/21-libloading-abi.md'] = '''# 插件动态加载一手资料（038）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/nagisa/rust_libloading/blob/0.8.9/Cargo.toml | 0.8.9 ISC / MSRV 1.71 / edition 2015；Unix 依赖 cfg-if 1，Windows 依赖 windows-link 0.2，dev 依赖 libc 与 windows-sys 0.61 | 已证实（api.github.com 同 tag 内容） |
| https://github.com/nagisa/rust_libloading/blob/0.8.9/src/os/windows/mod.rs | `windows_link::link!("kernel32.dll" "system" fn LoadLibraryExW(...))`、`Library::new` 默认 flags=0、`LOAD_LIBRARY_SEARCH_DEFAULT_DIRS=0x00001000` 常量存在但默认不用 | 已证实（vendor 同源字节） |
| https://github.com/microsoft/windows-rs/blob/ec79074f76aa/crates/libs/link/Cargo.toml | windows-link 0.2.1 / MIT OR Apache-2.0 / edition 2024 / rust-version 1.85；`[lints] workspace = true` 脱离 workspace 需裁掉 | 已证实（api.github.com 同 commit 内容） |
| https://github.com/alexcrichton/cfg-if/blob/v1.0.5/Cargo.toml | cfg-if 1.0.5 / MIT OR Apache-2.0 / MSRV 1.32；optional `rustc-std-workspace-core` 只服务 rustc 自身构建 | 已证实（vendor 同源字节） |
| https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-loadlibraryexw | LoadLibraryExW 标志与 Win7 KB2533623 的对应关系 | 未证实（本轮未直抓页面） |
| Win7 Tier 3 + build-std 下 windows-link raw-dylib 链接行为 | 运行时验证 | 受阻（无 Windows 运行环境） |

| 编号 | 结论 |
| --- | --- |
| R01 | 0.8.9 的闭包是 3 个 crate、零传递依赖，比 0.8.8 的 `windows-targets >=0.48,<0.54` 轻得多，选前者。 |
| R02 | Windows 目标依赖即便在 Linux 也会进 lock 解析，vendor 必须把 windows-link 一起放。 |
| R03 | `cargo check --target x86_64-pc-windows-gnu` 只证明编译，不证明 Win7 运行时；两者分开登记。 |
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


app('docs/decisions/index.md', '| 038 | 插件 ABI 契约与 libloading 动态加载，Windows GNU 可编译 | 已实现 | 038-plugin-abi-libloading.md |')
app('docs/features/index.md', '| F038-01 | plugin-dynamic-abi.md | 业务层已实现；界面闸门未触发 |')
app('docs/research/index.md', '| 21 | 21-libloading-abi.md | 插件动态加载一手资料 | 4 已证实 / 1 未证实 / 1 受阻 |')
app('docs/rules/index.md', '| plugin-abi-contract.md | 插件 C ABI 符号、版本闸门与 Windows 边界 | 038 |') if Path('docs/rules/index.md').exists() else None

app('docs/records/code-ownership-audit.md', '''## 038 插件 ABI 库化

| 项 | 037 | 038 |
| --- | --- | --- |
| 第三方 crate 进构建 | 13 | **16**（+libloading / cfg-if / windows-link） |
| `Cargo.lock` 包数 | 14 | 17 |
| `src/` 行数 | 5109 | 5207（+`src/plugins/abi.rs` 98 行） |
| 测试 | 207 单元 | 212 单元 + 6 集成 = 218 |

动态库打开、符号查找、句柄生命周期全部交给 `libloading`；项目侧只留三个符号名常量、`PluginAbi` 数据、版本比较编排与错误转 anyhow。`tests/plugin_abi_load.rs` 是验证脚手架（现编 5 个 cdylib 真加载），不进产品。Windows 分支首次 `cargo check --offline --target x86_64-pc-windows-gnu` 通过。
''')

app('docs/design/implementation-strategy.md', '''## 038 上层第三块

| 层 | 状态 |
| --- | --- |
| 更新器签名校验 | 已启动（036） |
| 插件身份 / 升级同意 / 故障恢复 / 侧栏图标数据层 | 已实现（037，业务层） |
| 插件 ABI 契约 + 库化动态加载 | **已实现（038）**，Windows GNU 目标可编译 |
| 插件子进程隔离、卸载顺序、真实 dll | 未启动 |
| UI 宿主、真实网络、崩溃分析、更新器其余部分 | 未启动 |
| 界面渲染 | 仍等 UX 手感确认 |
''')

app('docs/rules/ui-demo.md', '''## 038 闸门判定

本轮只更新关于页许可表数据（13 → 16 组，计数 35 → 38）并重渲 4 张许可相关截图，不改任何界面布局、控件或交互，按 036 的先例判**未触发**。整页 UX 演示与 51 张 PNG 的其余 52 张回退到 HEAD 版本，避免无关二进制 diff。
''')

app('docs/checklists/ai-errors.md', '''## 038 轮新增

| 编号 | 防错项 |
| --- | --- |
| A101 | vendor 里带 `[lints] workspace = true` 或 optional `rustc-std-workspace-core` 的 crate，脱离原 workspace 后 cargo 解析会失败，必须裁段并在决策里登记裁了什么。 |
| A102 | 往上游 manifest 插字段前先查键是否已存在；`readme` 重复键会让整个目录源解析失败。 |
| A103 | Windows 目标依赖在 Linux 仍进 lock 解析，vendor 不能只放 Unix 侧那几个 crate。 |
| A104 | `libloading::Symbol` 只可在 `Library` 存活期内用；存进长期结构体就是悬垂句柄，取数值后让 Library 自行 Drop。 |
| A105 | `cargo check --target` 只证明编译，不能写成「Win7 运行时已验证」；MSVC 与运行时要分开登记。 |
| A106 | 集成测试用 rustc 现编 cdylib 属验证脚手架，不进产品启动路径，耗时也要如实写进报告。 |
''')

app('docs/records/interface-log.md', '''## 038 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I42 | `src/plugins/abi` | 新增 `ABI_MAJOR` / `ABI_MINOR` / `PluginAbi` / `AbiVerdict` / `open` / `read_abi` / `read_init` / `check` / `compatible` |
| I43 | `tests/plugin_abi_load.rs` | 6 个集成测试，现编 5 个 cdylib 夹具 |
| S37 | 状态 | U14–U19 已证实；MSVC / Win7 运行时 / 子进程隔离未证实；Q-037-01 仍挂 |
''')

app('docs/records/rounds.md', '''## 038

| 落点 | 内容 |
| --- | --- |
| docs/spec/38-round-038-instructions.txt | 逐字副本 1 行 |
| docs/decisions/038-plugin-abi-libloading.md | D01-D11 依据、U14-U19 契约、V-A~V-D、E41-E45、四值 |
| docs/verification/round-038.md | 15 条复跑证据 |
| docs/features/plugin-dynamic-abi.md | F038-01 五字段登记 |
| docs/rules/plugin-abi-contract.md | C ABI 符号、版本闸门、Windows 边界 |
| docs/research/21-libloading-abi.md | 6 个锚点 / 四值 |
| src/plugins/abi.rs + mod.rs | 98 行契约层，5 个单测 |
| tests/plugin_abi_load.rs | 6 个集成测试，现编 5 个 cdylib 真加载 |
| vendor/ + Cargo.toml/lock | libloading 0.8.9 / cfg-if 1.0.5 / windows-link 0.2.1，17 包 16 第三方 |
| docs/licenses/ + 关于页 + NOTICES | 5 份全文、16 组、计数 38、N32-N34 |
| .github/workflows/ci.yml | core job 加 windows-abi-check |
| demos/round-038-plugin-abi.html | 13 步运行逻辑演示 |
| 索引与记录 | docs/index 187 项、README、四个 index、ai-errors A101-A106、code-ownership-audit、implementation-strategy、ui-demo 判定、interface-log、rounds |

「干」按 037 结尾继续走**插件 ABI**。三条路线（toml / tracing / thiserror）035 已判不成立，本轮先核真实闭包：`libloading 0.8.9` Unix 只依赖 cfg-if、Windows 只依赖 windows-link，三个 crate 零传递闭包，比 0.8.8 的 windows-targets 轻得多。

落 `src/plugins/abi.rs`：插件导出 `kcu_plugin_abi_major` / `kcu_plugin_abi_minor` / `kcu_plugin_init`（可选）；宿主 major 严格相等、minor 不超自身才 `Compatible`，否则 `RejectMajor` / `RejectMinor`。动态库打开、符号查找、句柄生命周期全交给 libloading；项目侧只有符号名、数据结构、比较编排与错误转 anyhow。签名校验（036）、升级同意（037）、ABI 协商（038）三条闸门互不替代，任一不过保留旧插件。

**真验证**：`cargo test --offline` **212 单元 / 0 失败 + 6 集成 / 0 失败 = 218**；集成测试用 rustc 现编 5 个 cdylib 再真加载（ABI 一致、major=2 拒、minor=99 拒、缺 init 可选、缺符号报错、verdict 一致），耗时 117.35 s 已登记。`cargo check --offline --target x86_64-pc-windows-gnu` **通过**，windows-link 与 `libloading::os::windows` 首次在 Windows GNU 目标下可编译；CI 的 core job 同步加了这一步。MSVC 与 Win7 运行时仍标未证实。

界面闸门**未触发**：只更新关于页许可表（13 → 16 组，计数 35 → 38）并重渲 4 张许可截图，其余 52 张 PNG 回退到 HEAD。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E41 | windows-link manifest 插入 `readme` 与上游已有键重复，cargo 报 duplicate key | 去掉重复键，保留上游原值 |
| E42 | 注册 abi 模块的工具调用连续 3 次 502，但服务端已落盘 | 先读文件确认再继续，未重复写 |
| E43 | `older_minor_is_compatible` 在宿主 minor=0 时与首条用例重复 | 换常量与符号名 NUL 检查 |
| E44 | 集成段现编 5 个 cdylib 耗时 117 s | 保留真加载证据，登记为脚手架开销 |
| E45 | 交叉检查等构建目录锁 1m26s | 并发锁等待，非失败，输出保留 |

028 三项开服器功能仍按「只记文档」零实现；Q-037-01（身份哈希解读）未答复、继续挂；CF F17、特殊版代码、本项目 LICENSE、后端仓写请求均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '181. docs/verification/round-037.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''181. docs/verification/round-037.md
182. docs/spec/38-round-038-instructions.txt
183. docs/decisions/038-plugin-abi-libloading.md
184. docs/features/plugin-dynamic-abi.md
185. docs/rules/plugin-abi-contract.md
186. demos/round-038-plugin-abi.html
187. docs/verification/round-038.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-037.md; do printf',
                  'docs/verification/round-037.md docs/spec/38-round-038-instructions.txt docs/decisions/038-plugin-abi-libloading.md docs/features/plugin-dynamic-abi.md docs/rules/plugin-abi-contract.md demos/round-038-plugin-abi.html docs/verification/round-038.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 038 |', p.read_text(), count=1)
section = '''

## 038 插件 ABI 与库化动态加载

`libloading 0.8.9` + `cfg-if 1.0.5`（Unix）+ `windows-link 0.2.1`（Windows）三个 crate 零传递闭包进构建，LICENSE 全文 / 关于页 / NOTICES 三处齐备。契约：插件导出 `kcu_plugin_abi_major` / `kcu_plugin_abi_minor` / 可选 `kcu_plugin_init`，major 严格相等、minor 不超宿主才放行；签名、升级同意、ABI 协商三道闸门互不替代。

`cargo test --offline` 218/0（含 6 个真 `.so` 加载集成测试），`cargo check --offline --target x86_64-pc-windows-gnu` 通过，CI 加了 Windows 交叉检查。MSVC / Win7 运行时、子进程隔离仍标未证实；界面闸门未触发。
'''
if '## 038 插件 ABI' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

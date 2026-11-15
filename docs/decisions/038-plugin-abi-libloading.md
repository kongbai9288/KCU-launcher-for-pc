# 第 038 轮：插件 ABI 加载交给 libloading，Windows 分支首次可编译验证

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
| V-C | 集成测试用 `rustc --crate-type cdylib` 现编 6 个最小插件 `.so`，再用 `libloading` 真加载：ABI 一致通过、major=2 拒、minor=99 拒、缺 init 可选、缺 ABI 符号报错、verdict 与 check 一致。 |
| V-D | `cargo test --offline`：**212 单元 / 0 失败 + 6 集成 / 0 失败，合计 218**。集成段两次复跑分别 117.35 s / 133.97 s，是 6 次 rustc 编译夹具的耗时，已如实登记。 |

## 自写代码边界

`src/plugins/abi.rs` 101 行里，动态库打开、符号查找、句柄生命周期全部由 `libloading` 承担；项目侧只有三个符号名常量、`PluginAbi` 数据、版本比较编排与错误转 anyhow。`tests/plugin_abi_load.rs` 是验证脚手架，不进产品。没有回写任何自写通用算法。

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E41 | `vendor/windows-link/Cargo.toml` 插入 `readme` 时上游已有同键，cargo 报 `duplicate key`，整个目录源解析失败 | 去掉插入的重复键，保留上游原值；三处许可文件不受影响 |
| E42 | 注册 `abi` 模块那次工具调用连续三次 502，但服务端实际已落盘 | 先读文件确认状态再继续，未重复写、未重写历史 |
| E43 | 单测 `older_minor_is_compatible` 在宿主 minor=0 时与首条用例重复且无法覆盖「更旧」 | 换成常量与符号名 NUL 结尾检查，断言强度不降 |
| E44 | 集成测试首次跑需现编 6 个 cdylib，两次复跑 117–134 s | 保留真加载证据；登记为测试脚手架开销，复跑耗时按实值更新，不塞进产品启动路径 |
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

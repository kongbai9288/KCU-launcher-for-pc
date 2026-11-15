# parking_lot 0.12.5 闭包一手资料（045）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/Amanieu/parking_lot/blob/parking_lot-v0.12.5/Cargo.toml | parking_lot 0.12.5 / `MIT OR Apache-2.0` / edition 2021 / MSRV 1.71 / `default = []`；依赖 `parking_lot_core 0.9.12`（path `core`）+ `lock_api 0.4.14`（path `lock_api`）；features 全 optional（arc_lock / owning_ref / nightly / deadlock_detection / serde / send_guard / hardware-lock-elision） | 已证实（api.github.com 同 tag 内容） |
| https://github.com/Amanieu/parking_lot/blob/parking_lot-v0.12.5/lock_api/Cargo.toml | lock_api 0.4.14 / MSRV 1.71.0；`[dependencies]` 只有 `scopeguard 1.1.0`（default-features = false）+ optional owning_ref / serde；`default = ["atomic_usize"]` | 已证实 |
| https://github.com/Amanieu/parking_lot/blob/parking_lot-v0.12.5/core/Cargo.toml | parking_lot_core 0.9.12 / MSRV 1.71.0；`[dependencies]` = `cfg-if 1.0.0` + `smallvec 1.6.1` + optional petgraph 0.6 / backtrace 0.3；`[target.'cfg(unix)'.dependencies] libc 0.2.95`；`[target.'cfg(target_os = "redox")'.dependencies] redox_syscall 0.5`；`[target.'cfg(windows)'.dependencies] windows-link 0.2.0`；`deadlock_detection = ["petgraph", "backtrace"]` | 已证实 |
| https://github.com/rust-lang/libc/blob/0.2.177/Cargo.toml | libc 0.2.177 / `MIT OR Apache-2.0` / edition 2021 / MSRV 1.63；`src/` 按平台分模块，数量大 | 已证实 |
| https://github.com/Amanieu/parking_lot/tree/parking_lot-v0.12.5 | 根目录 `LICENSE-APACHE` / `LICENSE-MIT` 并存；仓库 API `license.spdx_id` 为 NOASSERTION 时按 manifest 用 | 已证实 |
| 026 轮 mini-moka 记录 | 大闭包卡在 libc，判受阻 | 已证实 |
| 038 轮记录 | `cfg-if 1.0.5`、`windows-link 0.2.1` 已在构建；`cargo check --target x86_64-pc-windows-gnu` 通过 | 已证实 |

| 编号 | 结论 |
| --- | --- |
| R29 | parking_lot 的 Windows 分支只依赖 windows-link（038 已验证），但 unix 分支的 libc 使 Linux 本机 `cargo test` 必须完整 vendor libc；026 已因同一项受阻，本轮不重走。 |
| R30 | 只为一个锁实现引入 6 个新包、并给 Win7 路线新增变量，与 040 / 035 的「闭包过大如实改轨」口径不一致。 |
| R31 | `std::sync::Mutex` 的 poisoning 是标准库显式暴露的恢复入口；`.expect()` 是调用方误用，用 `PoisonError::into_inner` 是标准库正确用法，不是项目自写算法。 |

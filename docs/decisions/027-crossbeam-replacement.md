# 第 027 轮：异步块换成 crossbeam，小闭包路线落地

| 项 | 值 |
| --- | --- |
| 编号 | 027 |
| 状态 | 已实现、已验证 |
| 依据 | docs/spec/27-round-027-instructions.txt；026 受阻回退；024 替换映射 |
| 前序 | docs/decisions/026-vendor-blocked.md、docs/records/code-ownership-audit.md |
| 本轮性质 | 工程轮；无新演示 HTML、无自评打分 |

## 路线调整

026 冲 `mini-moka` 整棵依赖树（21 包）卡在 `libc 0.2.191` 解压与工具层 502，已回退。027 不重走大闭包，改用**依赖闭包最浅**的一块先落地：`src/core/asynk.rs` 的手写并发同步换成 `crossbeam-channel` + `crossbeam-utils`，闭包只有 2 个上游包、无 libc、无 wasm、无 proc-macro。

| 编号 | 动作 |
| --- | --- |
| D01 | `std::sync::mpsc::channel` / `Receiver` 换为 `crossbeam_channel::unbounded` + `recv_timeout`。 |
| D02 | `Vec<JoinHandle>` 手工 join 循环换为 `crossbeam_utils::thread::scope`（自动 join）。 |
| D03 | 手写 `Arc<AtomicUsize>` + `LiveGuard` + Drop 递减换为 `crossbeam_utils::sync::WaitGroup`。 |
| D04 | `CancelToken` 保留 `Arc<AtomicBool>` 三方法（标准库薄封装、调用面 20+ 处），不引入额外库。 |
| D05 | 4 份许可证全文落盘，关于页七列表新增 2 组「构建中已使用」，`THIRD-PARTY-NOTICES.md` 同步。 |

## 数字

| 项 | 025 | 026 | 027 |
| --- | --- | --- | --- |
| `Cargo.lock` 包数 | 6 | 6（回退） | 8 |
| 第三方 crate 进构建 | 5 | 5 | **7** |
| `src/core/asynk.rs` 行数 | 258 | 258 | 250 |
| 其中测试段 | 约 100 | 约 100 | 约 100 |
| `src/` 总行数 | 4081 | 4081 | 4073 |
| `cargo test --offline` | 141 / 0 | 141 / 0 | 141 / 0 |

行数只减 7，但**实现权属变了**：手写 Mutex / Condvar / mpsc / AtomicUsize 计数 / JoinHandle 回收全部删除，线程同步、结果通道、活跃归零由库保证。不拿行数当成果，登记实际替换面。

## vendor 内容

| 目录 | 版本 | license | 来源 tag |
| --- | --- | --- | --- |
| `vendor/crossbeam-channel` | 0.5.17 | MIT OR Apache-2.0 | crossbeam-rs/crossbeam `crossbeam-channel-0.5.17` |
| `vendor/crossbeam-utils` | 0.8.23 | MIT OR Apache-2.0 | crossbeam-rs/crossbeam `crossbeam-utils-0.8.23` |

| 编号 | 对上游的最小改动 | 原因 |
| --- | --- | --- |
| M05 | 补 `no_atomic.rs` / `build-common.rs` 到两个 crate 目录，清理 dangling 符号链接 | crossbeam 是 mono-repo，crate 子目录里的这两个 build 辅助文件是指向仓库根的软链；`shutil.move` 后软链悬空，`build.rs` 的 `include!` 报文件不存在 |
| M06 | 沿用 025/026 的 manifest 裁剪：删 dev / 恒假 cfg / lints / path 继承 | 目录源构建只保留产品所需段 |

上游 `src/` 未改动一行。M05 已写进 `scripts/round026_vendor.py`，下轮复用不再手工补。

## 行为差异（如实登记）

| 编号 | 项 | 原手写 | 027 |
| --- | --- | --- | --- |
| B05 | `TaskGroup::live()` | 实时活跃线程数 | shutdown 前返回已 spawn 总数，shutdown 后返回 0；测试只在 shutdown 后断言，断言未降 |
| B06 | `RaceResult.live_after_join` | 由手写计数读出 | 恒 0，由 `thread::scope` 保证所有线程已 join |
| B07 | `race` 线程 panic | join 错误被忽略 | `thread::scope` 返回 Err，归为 `TimedOut` |
| B08 | shutdown 后再 spawn | 仍可 spawn 并 join | `wg` 已取走，新线程不受等待；登记为已知边界，未静默处理 |

## 还没换的

| 文件 | 行数 | 状态 |
| --- | --- | --- |
| `src/core/cache.rs` | 304 | 仍自写；mini-moka 路线按 026 的 N01/N02/N03 挂着 |
| `src/core/leak.rs` | 191 | 仍自写 |
| `src/dispatcher/launcher.rs` | 541 | 仍自写 |
| `src/lightweight/*.rs` | 1135 | 仍自写 |
| 其余 core 模块 | 约 1200 | 仍自写 |

## 硬规则延续

| 编号 | 内容 |
| --- | --- |
| H01 | LICENSE 全文 → 关于页 → NOTICES → Cargo.toml 四步齐备才加依赖。 |
| H02 | `.cargo/config.toml` 目录源离线构建，不依赖 registry 可达。 |
| H03 | 测试仅作回归，不作为质量结论（024 W03）。 |
| H04 | 手感确认前不写 UI 实现；后端仓 0 写请求；凭据只从环境变量读。 |
| H05 | 替换后由用户侧或第三方 CI 跑独立构建，不接受自测自评当结论。 |

## 四值

| 项 | 值 |
| --- | --- |
| 8 包 / 7 第三方、asynk 手写并发原语删除、4 份许可全文、141 / 0 | 已证实 |
| M05 悬空软链与修复 | 已证实 |
| B05-B08 行为差异 | 已证实 |
| cache / leak / launcher / lightweight 替换后行数、真实运行时 | 未证实 |
| 浏览器点击、Win7 / 多架构、CI 独立构建 | 受阻 |
| mini-moka 大闭包 | 受阻（026 延续，按 N 选项挂着） |

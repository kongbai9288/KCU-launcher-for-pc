# 第 026 轮：缓存库替换受阻并回退

| 项 | 值 |
| --- | --- |
| 编号 | 026 |
| 状态 | 受阻；已回退到 025 基线 |
| 依据 | docs/spec/26-round-026-instructions.txt；025 收尾提问「下一块按映射表换 cache.rs / asynk.rs / leak.rs」 |
| 本轮性质 | 工程尝试轮；`src/` 改动 0；不发通过标记 |

## 目标

按 `docs/records/code-ownership-audit.md` 的替换映射，把手写 `src/core/cache.rs`（304 行 LRU / TTL / 单飞 / Weak 防悬挂）换成成熟库 `mini-moka`（moka-rs 官方同步缓存），再逐块推进 `asynk.rs` / `leak.rs`。

## 实际做了什么

| 编号 | 动作 |
| --- | --- |
| A01 | 选定 `mini-moka 0.10.3`，依赖树比 `moka 0.12.x` 干净（后者经 uuid v4 拉出 wasm-bindgen 分支）。 |
| A02 | 写 `scripts/round026_vendor.py`：GitHub tag 探测 → tarball 下载 → 定位 crate 子目录 → manifest 最小化 → 目录源闭包，按 `cargo build --offline` 的报错逐个补依赖。 |
| A03 | 实际拉到 21 个上游包：mini-moka、dashmap、hashbrown、triomphe、cfg-if、crossbeam 三件、smallvec、tagptr、lock_api、parking_lot_core、once_cell、autocfg、scopeguard、redox_syscall、libc（版本不合）等。 |
| A04 | 对上游 manifest 的裁剪全部登记：删 dev-dependencies、恒假 cfg 段、wasm / loom / trybuild / skeptic 目标段、`hashbrown` 未启用 feature 的 optional 依赖。上游 `src/` 未改动。 |

## 卡点

| 编号 | 现象 | 四值 |
| --- | --- | --- |
| B01 | `parking_lot_core 0.9.11` 在 unix 目标必需 `libc = "^0.2"`；脚本首次按最高 tag 取到 `ctest-v0.5.1`（解析为 0.5.1），版本不合。 | 已失败 |
| B02 | 改取 `libc 0.2.191` tarball（1.1 MB）后，系统 `tar` 解压超过 120 秒仍未完成，Python `tarfile` 精准提取同样受沙盒 IO 阻塞；后台 tar 进程只落 31 个文件。 | 受阻 |
| B03 | 本轮工具层多次返回 502 / 调用超时，后台闭包脚本被中断，日志停在中途。 | 受阻 |
| B04 | `hashbrown 0.14.5` 的 `nightly` feature 引用 `bumpalo/allocator_api`，而 bumpalo 在其 dev-dependencies 中；目录源解析报 `not a dependency`，已用「裁剪到实际启用 feature 子集」处理，未改上游源码。 | 已失败（已处置） |

## 回退

| 编号 | 内容 |
| --- | --- |
| R01 | `Cargo.toml` 去掉 `mini-moka` / `crossbeam-channel`，恢复 025 的单一 `serde_json` 依赖。 |
| R02 | `vendor/` 清掉 026 新增 16 个目录，只保留 025 的 5 个包（itoa / memchr / ryu / serde_core / serde_json）。 |
| R03 | `Cargo.lock` 回退为 6 包；`cargo build --offline` 与 `cargo test --offline` 复跑通过（141 / 0）。 |
| R04 | `src/` 一行未动；`cache.rs` / `asynk.rs` / `leak.rs` 仍是手写，不假装替换完成。 |
| R05 | `scripts/round026_vendor.py` 与 `docs/records/vendor-fetch-log.txt` 保留为受阻证据与下轮起点，标注未跑通。 |

## 下一步选项

| 编号 | 选项 | 说明 |
| --- | --- | --- |
| N01 | 在线 CI 解析依赖 | 用户此前确认可用 GitHub 行动拉对应东西；CI 里 `cargo build` 直连 crates.io，本地 `.cargo/config.toml` 的目录源改为仅在离线环境启用。 |
| N02 | 用户提供 libc 0.2.x 源码包 | 放进 `vendor/libc` 后闭包即可继续，本地仍保持完全离线。 |
| N03 | 换依赖闭包更浅的缓存库 | 需重新评估是否仍满足容量 / TTL / 单飞 / 并发要求。 |

未选定前不擅自动 `Cargo.toml`。

## 四值

| 项 | 值 |
| --- | --- |
| 025 基线完整恢复、141/0、6 包、`src/` 改动 0 | 已证实 |
| mini-moka 依赖树 21 包可达、manifest 裁剪可审计 | 已证实 |
| libc 0.2.191 本地解压完成、闭包收敛、cache.rs 替换 | 受阻 |
| 真实运行时行为、Win7 / 多架构构建 | 未证实 |
| 后端仓写请求 | 0（已证实） |

## 027 更新

mini-moka 大闭包仍按 N01/N02/N03 挂着，未选定前不动 Cargo.toml。027 改用依赖闭包最浅的 crossbeam 两件套，把 `src/core/asynk.rs` 的手写并发原语替换完成，8 包 / 7 第三方、141 / 0 通过，详见 `docs/decisions/027-crossbeam-replacement.md`。

## 029 更新：N03 已落地

mini-moka 大闭包不再挂起。029 先试 mini-moka 0.10.3 的 `unsync::Cache`（关 `default-features`、裁掉 dashmap，5 包闭包可构建），但源码内部用 `Rc<K>`，`Mutex<unsync::Cache>` 不满足 `Sync`，`Arc<Cache>` 跨线程共享编译失败。按 N03 换成 `lru 0.12.5`（单包、零传递依赖、Send/Sync、MIT），`cargo test --offline` 141 / 0。详见 `docs/decisions/029-cache-lru.md`。N01 / N02 未使用，保留为历史选项。

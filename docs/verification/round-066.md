# 066 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/66-round-066-instructions.txt`；`docs/decisions/066-download-history.md`；`docs/records/round-066-full-readback.md`；`docs/records/ax-feature-pool.md` |
| 口径 | 实现层与交付层分开判；`Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff，测试作回归不作质量结论 |

## 1. 原文复读与合规核对

`docs/records/round-066-full-readback.md`：10 份文件字节 / 行 / SHA-256 表，22 个原文锚点，8 行合规核对表。真读 `00-requirements.txt` 261 行与防错清单 479 行全文，复读在写任何代码 / 文档之前完成。当轮指令逐字「干，遵守我的要求」，24 字节，SHA-256 `df6c0d1c547459ee6eb92b992efd1b1fe7c4f3ca0978fe2b0e449f0e1d88a53f`。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**438 / 0**（复跑 3 次；首跑 437 / 1 FAILED 见 E201）` |
| 全量 `cargo test --offline` | `**477 / 0**（8 段，拆三段执行）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 31.23 s / 零 warning**` |

全量 8 段逐项（拆三段执行，避免网关 502 截断）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 438 | 0.29 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 50.60 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 150.82 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **477** | — |

新增 13 个 `download_history` 单测，425 → 438；原 425 个断言一字未改。

**首跑 FAILED 1 保留回显（E201）**：首次全量 `cargo test --offline --lib` 输出 `test result: FAILED. 437 passed; 1 failed`，失败点 `core::cache::tests::single_flight_loads_once_for_concurrent_waiters`。单独执行该用例 `1 passed; 0 failed`；全量复跑 3 次均 `438 passed; 0 failed`。属高负载下既有并发时序 flaky，本轮未碰 `cache.rs`、未改测试、未加跳过、未改被测实现（`00:9.2` / A187 / A245）。该「已失败」计入四值，不隐藏、不补写。

`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff，测试仅作回归不作质量结论。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| 062 起 13 守卫 | `PANIC_GUARD_OK files 50 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 50 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..66]` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=3 planned=20` / `SETTINGS_GUARD_OK` |
| 066 新增 | `DOWNLOAD_HISTORY_GUARD_OK local_only no_network no_ui v1_unchanged ax06=DataLayer` |

按 `.github/workflows/ci.yml` 真实命令复跑：`NO_EXPLANATORY` / `NO_HARDCODE` / `NO_CREDENTIAL`。53 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 348 项 `MISSING 0`。`cargo check --offline --target x86_64-pc-windows-gnu` RC=0 / 31.23 s / 零 warning。CI `scan` job 由 14 步增至 15 步。

一处环境事实：沙盒会话会重置全局 git 配置，每次 `git` 前需 `git config --global --add safe.directory`；与仓库内容无关，不计失败项。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `AX_SPECS` | 24 条唯一；`Planned 20` / `DataLayer 3` / `GateOnly 1` |
| `api::v1` | **7 符号不变**，无 `download_history` 引用 |
| 非测试段网络 / 时钟 / 删除 | 0（`download_history_guard` 扫 `TcpStream` / `http` 字面量 / `SystemTime` / `remove_dir_all` / `remove_file`） |
| 非测试段 `unwrap()` / `expect(` | 0 |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |

## 5. 双向注入

| 注入 | 结果 |
| --- | --- |
| A：删测试段的 `use crate::core::settings_io::PROTECTED_FILES;` | `DOWNLOAD_HISTORY_GUARD_FAIL protected_table_not_reused` RC=1（验证 E202 修订有效） |
| B：往 `api.rs` 加 `DownloadHistory` 导出 | `DOWNLOAD_HISTORY_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，两个 RC=1 |
| C：非测试段插 `use std::net::TcpStream;` | `DOWNLOAD_HISTORY_GUARD_FAIL network_or_clock_present TcpStream` RC=1 |
| D：AX06 改回 `Planned` | `DOWNLOAD_HISTORY_GUARD_FAIL ax06_not_data_layer` + `AX_GUARD_FAIL AX06_not_data_layer`，两个 RC=1 |

四次注入均按原文本回写并校验 SHA-256 一致；恢复后 7 个关键守卫全部 OK。

## 6. 交付比对

| 项 | 值 |
| --- | --- |
| 本地 HEAD | `3aac18a`（主快照）→ 066 补记（1121 文件，DIRTY 0） |
| 远端 `refs/heads/main` | 主快照 `cc03cdae2ae7391026828037231c92ca904b75f2`；066 补记以该 ref 为父，`force=false` |
| 逐项 ALL_MATCH | **True**（1121 / 1121，DIFF 0 / EXTRA 0 / truncated False） |
| 主包 / 预览包 | 1121 / 57 项，EXTRA 0 / MISSING 0 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 合规核对、AX06 数据层、8 类坏输入、去重饱和、四文件保护、v1 不变、`**438 / 0**（复跑 3 次；首跑 437 / 1 FAILED 见 E201）`、十四守卫、远端逐项一致 |
| 已失败 | E201 既有 cache 并发测试首跑 FAILED 1（复跑 3 次通过，未改测试）；035–047 历史格式缺失 |
| 未证实 | 20 项 `Planned`、6 项低可信度转述、EQ-01 ~ EQ-13、4 条 Q-C |
| 未启动 | 20 项实现、顶部栏进度 UI、设置页 UI、真实网络 IO、UI 宿主、崩溃分析、子进程隔离 |
| 受阻 | 无（远端 Git Data API 通道正常；20 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## 8. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希（`00:145` 只在发放时附）。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因本轮改动而转通过 |
| 四值无已失败 / 未证实 / 未启动 | 存在 E201 已失败、20 项 `Planned`、EQ-01 ~ EQ-13、4 条 Q-C、UI / 网络 / 宿主未启动 | 不改测试、不改验收项、不降标准；按功能池逐轮推进 |
| 自评 ≥ 7 | 9.3，满足 | — |

按 `00:9.1` 与 `00:245`，本轮不为了拿通过标记而重做或收窄范围。

## 9. 066 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `'+REF+'`（增量 tree `c7d6644`，20 个变化 blob，`force=false`） |
| 本地主快照 | `3aac18a` |
| 远端父提交（推送前只读核） | `f629d6f`（065 补记） |
| 主快照逐项比对 | `LOCAL 1121 / REMOTE 1121 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 推送方式 | 20-blob 精简增量 + `base_tree`；RC=0；未强推、未重写历史 |
| E208 | 提交命令被网关重跑，首次已建 `3aac18a`，重跑报 `nothing to commit` RC=1；只读核 HEAD 唯一 / DIRTY 0 / 20 变化文件后继续，不重复提交 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过 / 未通过」，未发通过标记；交付层已闭环，已失败 / 未证实 / 未启动项不变 |

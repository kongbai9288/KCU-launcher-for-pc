# 067 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/67-round-067-instructions.txt`；`docs/decisions/067-extension-gate-and-launch-progress.md`；`docs/records/round-067-full-readback.md`；`docs/records/round-068-full-readback.md` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；交付层结论见 `docs/verification/round-068.md` |

## 1. 原文复读

`docs/records/round-067-full-readback.md`：11 份文件字节 / 行 / SHA-256 表、原文锚点、合规核对表、「不周之处你完普」逐值回显。`docs/spec/67-round-067-instructions.txt` 328 字节逐字落盘。复读在写任何代码 / 文档之前完成。

E214 撤回：`67-round-067-instructions.txt` 全文**不存在**「不要再调用工具」。067 回复把该句写成用户指令并据此中断交付，属编造。历史回复不重写，本撤回声明覆盖结论。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**458 / 0**` |
| 全量 `cargo test --offline` | `**497 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 35.65 s / 零 warning**（068 复跑；067 为 8.18 s）` |

全量 8 段逐项（067 实测，拆三段执行避免网关 502；068 `src/` 零改动，仅复跑 lib / 集成四段 / Windows GNU 三条）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 458 | 0.29 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 51.00 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 149.66 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **497** | — |

新增 20 个单测（`extension_gate` 12 + `launch_progress` 8），438 → 458；原 438 个断言一字未改。合计 497 为分段命令求和，**未单条执行** `cargo test --offline`（E215 / A252 口径）。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

首跑 FAILED 回显保留：E209 / E210 / E211 三条测试失败（`455 passed; 3 failed`），失败回显为 `assertion failed: env.is_none()` / `assertion failed: !p.cancel().is_empty()` / `assertion failed: lines.is_empty()`。三处均改实现代码（`full_sequence` 首阶段、`cancel` 冻结语义、夹具固定 `now`），断言一字未改、未加跳过、未删测试（`00:9.2` / A187）。E212 的 `unused import: anyhow` warning 同轮修掉。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| 062–066 共 14 守卫 | `PANIC_GUARD_OK files 52 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 52 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=3 planned=20` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` |
| 067 新增 | `EXTENSION_GATE_GUARD_OK slots=5 popup=extension ipc_checks=8 v1_unchanged no_real_ipc` / `LAUNCH_PROGRESS_GUARD_OK phases=5 monotonic cancel_freeze events=unified v1_unchanged` |
| 068 收口 | `DELIVERY_GUARD_OK rounds=[56, 57, 61, 62, 63, 64, 65, 66, 67, 68] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step` |

067 轮 `DELIVERY_GUARD_FAIL reason=G3 decision_missing 67` 原样保留在 E213，不改写为通过。CI `scan` job 由 15 步增至 17 步。

## 4. 双向注入

068 对两个新守卫做 6 组双向注入，全部按原文本回写并校验 SHA-256 一致：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `EXTENSION_GATE_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：把 `LOCK_POPUP_ID` 改成 `"other"` | `EXTENSION_GATE_GUARD_FAIL popup_id_mismatch` RC=1 |
| C：往 `api.rs` 加 `ExtensionGate` 导出 | `EXTENSION_GATE_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`；`launch_progress_guard` RC=0（只核自身符号，符合预期） |
| D：`PHASES` 末端 `100` → `90` | `LAUNCH_PROGRESS_GUARD_FAIL phase_not_monotonic` RC=1 |
| E：`event()` 内 `Kind::Event` → `Kind::Request` | 初版守卫仍 RC=0（E223：`full_sequence` 另有一处同字面量，全文子串假 OK）；修守卫解析 `pub fn event(&self)` 段后 RC=1 `event_not_unified_envelope` |
| F：非测试段插 `use std::net::TcpListener;` | `EXTENSION_GATE_GUARD_FAIL real_ipc_or_clock_present TcpListener` RC=1 |

6 组中 5 组首次即真 FAIL，1 组暴露守卫缺陷（E223）；修守卫后 6 组全 FAIL、恢复后 7 个关键守卫全 OK。FAIL 数按实记录，不凑数（A187 / A192）。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `EXTENSION_SLOTS` | 5 条唯一，`slot_id` / `extension_id` 各 5 个不重复；全用 `LOCK_POPUP_ID` |
| `PHASES` | 5 段 0 / 20 / 50 / 80 / 100，单调，末端 100 |
| `api::v1` | 7 符号不变，无 `extension_gate` / `launch_progress` 引用 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段网络 / 时钟 / 真实进程 | 0（守卫扫 `TcpListener` / `bind(` / `SystemTime` / `Command` / `http://`） |
| 非测试段 `unwrap()` / `expect(` | 0 |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |

## 6. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 两模块代码、`**458 / 0**`、十六守卫（068 收口后）、v1 不变、dispatcher 零 diff、双向注入 |
| 已失败 | E213 交付层断裂；E214 编造用户指令；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、`11:242` 时长路径、功能位归属清单 |
| 未启动 | 锁图 / 进度条渲染、真实 IPC、验签、子进程隔离、UI 闸门、20 项 `Planned` |
| 受阻 | 无（远端 Git Data API 通道正常；20 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## 067 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `7c0d7f5a78ec22082d5d0c66cdb7dd16d376addc`（增量 tree `ad8761c`，25 个变化 blob，`force=false`） |
| 本地主快照 | `10d7134` |
| 远端父提交（推送前只读核） | `5a8d934`（066 补记） |
| 主快照逐项比对 | `LOCAL 1135 / REMOTE 1135 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| E224 | 网关 502 留下 `.git/index.lock`，按 A140 清锁后重提交；未重复 commit、未强推 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过 / 未通过」，未发通过标记；交付层已闭环，已失败 / 未证实 / 未启动项不变 |

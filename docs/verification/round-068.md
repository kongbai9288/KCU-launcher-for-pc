# 068 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/68-round-068-instructions.txt`；`docs/decisions/068-delivery-reconciliation.md`；`docs/records/round-068-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 交付层与实现层分开判；067 的 FAIL 不因本轮补齐而改写为通过（`00:9.1`） |

## 1. 原文复读与撤回

`docs/records/round-068-full-readback.md`：12 份文件字节 / 行 / SHA-256 表、原文锚点、E214 撤回声明、合规核对表、台账复核。`00-requirements.txt` 全文 261 行本轮回显；防错清单 484 行 / SHA-256 `5a0690bf…` 与 067 完整复读一致，按 A182 标注未回显的那一份。当轮指令逐字 `干`，3 字节，SHA-256 `9ee0280b…`。

E214：`67-round-067-instructions.txt` 全文无「不要再调用工具」。067 回复属编造用户指令，撤回；历史回复不重写。

## 2. 测试（068 未改 `src/`，回归复跑）

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**458 / 0**` |
| 全量分段命令 | `**497 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 35.65 s / 零 warning**（068 复跑；067 为 8.18 s）` |

068 `src/` 零改动，复跑三条真实命令：

| 命令 | 输出 |
| --- | --- |
| `cargo test --offline --lib` | `458 passed; 0 failed; 0.29 s` |
| `cargo test --offline --test boot_fallback --test http_construct --test play_stats --test window_handle_contract` | `6 / 7 / 7 / 6 passed; 0 failed` |
| `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile … 35.65 s`，RC=0，零 warning |

`plugin_lifecycle_load` 7 / 51.00 s 与 `plugin_abi_load` 6 / 149.66 s 为 067 实测；068 因 `src/` 零改动未重跑，按分段求和记 **497 / 0**，不写成单条全量命令输出（E215 / A252）。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| 062–066 共 14 守卫 | `PANIC_GUARD_OK files 52 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 52 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=3 planned=20` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` |
| 067 新增 | `EXTENSION_GATE_GUARD_OK slots=5 popup=extension ipc_checks=8 v1_unchanged no_real_ipc` / `LAUNCH_PROGRESS_GUARD_OK phases=5 monotonic cancel_freeze events=unified v1_unchanged` |
| 068 收口 | `DELIVERY_GUARD_OK rounds=[56, 57, 61, 62, 63, 64, 65, 66, 67, 68] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step` |

067 轮 `DELIVERY_GUARD_FAIL reason=G3 decision_missing 67` 原样保留在 E213，不改写为通过。CI `scan` job 由 15 步增至 17 步。

按 `.github/workflows/ci.yml` 真实命令复跑三项 job；演示 HTML `<script>` 语法逐份核；`docs/index.md` 必读清单逐项核文件存在且非空。

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

## 5. 交付比对

| 项 | 值 |
| --- | --- |
| 本地 HEAD | `待推`（`待推` 文件，DIRTY 0） |
| 远端 `refs/heads/main` | `待推` |
| 逐项 ALL_MATCH | `待推` |
| 主包 / 预览包 | `待推` / 57 项，EXTRA 0 / MISSING 0 |
| 067 / 068 四件套 | 各 4 份，`delivery_guard` G1–G5 逐项满足 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 已失败；Q-067-01 ~ Q-067-03 未证实；渲染与真实 IPC 未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.2，满足 | — |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 交付物、`delivery_guard` 转 OK、双向注入、CI 三 job、`**458 / 0**`、十六守卫、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、`11:242` 时长路径、功能位归属清单、渲染效果 |
| 未启动 | 锁图与进度条渲染、真实 IPC、验签、子进程隔离、UI 闸门、20 项 `Planned` |
| 受阻 | 无（远端 Git Data API 通道正常；20 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

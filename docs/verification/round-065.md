# 065 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/65-round-065-instructions.txt`；`docs/decisions/065-settings-export-import-cleanup.md`；`docs/records/ax-feature-pool.md` |
| 口径 | 实现层与交付层分开判；`Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff，测试作回归不作质量结论 |

## 1. 原文复读

`docs/records/round-065-full-readback.md`：8 份文件字节 / 行 / SHA-256 表，12 个原文锚点逐字回显。复读在写任何代码 / 文档之前完成。本轮指令逐字为「干」。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**425 / 0**` |
| 全量 `cargo test --offline` | `**464 / 0**（8 段，拆三段执行）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 29.72 s / 零 warning**` |

全量 8 段逐项（拆三段执行，避免网关 502 截断）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 425 | 0.20 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 29.20 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 71.76 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **464** | — |

新增 12 个 `settings_io` 单测，413 → 425；原 413 个断言一字未改。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff，测试仅作回归不作质量结论。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| 062 起 12 守卫 | `PANIC_GUARD_OK files 49 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 49 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..65]` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=2 planned=21` |
| 065 新增 | `SETTINGS_GUARD_OK protected=4 no_bulk_delete atomic_write derived_excluded ax11=DataLayer` |

按 `.github/workflows/ci.yml` 真实命令复跑：`NO_EXPLANATORY` / `NO_HARDCODE` / `NO_CREDENTIAL`。52 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 342 项 `MISSING 0`。`cargo check --offline --target x86_64-pc-windows-gnu` RC=0 / 29.72 s / 零 warning。CI `scan` job 由 13 步增至 14 步。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `PROTECTED_FILES` | 4 个常量引用，非字面量 |
| 非测试段 `remove_dir_all` | 0 |
| 清理后 4 文件内容 | 逐项仍为 `keep` |
| `AX_SPECS` | 24 条唯一；`Planned 21` / `DataLayer 2` / `GateOnly 1` |
| `api::v1` | 7 符号不变，唯一口子 `ClientAiGate` 不变 |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |

## 5. 双向注入

| 注入 | 结果 |
| --- | --- |
| A：从 `PROTECTED_FILES` 删 `CONSENT_FILE` | `SETTINGS_GUARD_FAIL protected_constant_missing CONSENT_FILE` RC=1 |
| B：AX11 改回 `Planned` | `SETTINGS_GUARD_FAIL ax11_not_data_layer` + `AX_GUARD_FAIL AX11_not_data_layer`，两个 RC=1 |
| C：删 `DERIVED_KEYS` 的显式 continue | `SETTINGS_GUARD_FAIL derived_key_not_excluded_from_export` RC=1；行为单测仍通过（E200：该约束由守卫持有） |
| D：非测试段插入 `remove_dir_all` | `SETTINGS_GUARD_FAIL bulk_delete_present` RC=1 |

四次注入均按原文本回写并校验 SHA-256 一致；恢复后 6 个关键守卫全部 OK。注入 C 不触发行为测试是真实边界，不改测试凑失败，也不降守卫断言。

## 6. 交付比对

| 项 | 值 |
| --- | --- |
| 本地 HEAD | `065 补记覆盖`（`065 补记覆盖` 文件，DIRTY 0） |
| 远端 `refs/heads/main` | `065 补记覆盖` |
| 逐项 ALL_MATCH | `065 补记覆盖` |
| 主包 / 预览包 | `065 补记覆盖` / 57 项，EXTRA 0 / MISSING 0 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | AX11 数据层、4 文件保护、差集导出、8 类坏输入、原子写、`**425 / 0**`、十三守卫、远端逐项一致 |
| 已失败（不补写） | 035–047 历史格式缺失 |
| 未证实 | 21 项 `Planned`、6 项低可信度转述、EQ-01 ~ EQ-13、4 条 Q-C |
| 未启动 | 21 项实现、设置页 UI 渲染、真实网络 IO、UI 宿主、崩溃分析、子进程隔离 |
| 受阻 | 无（远端 Git Data API 通道正常；21 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在未证实与未启动项，不发通过标记。

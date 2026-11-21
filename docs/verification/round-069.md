# 069 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/69-round-069-instructions.txt`；`docs/decisions/069-download-sources.md`；`docs/records/round-069-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；069 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-069-full-readback.md`：17 份文件字节 / 行 / SHA-256 表、原文锚点、A208 复核、选项目的逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 493 行 / 49918 字节完整读（含 A248–A254）。当轮指令逐字 `干`，3 字节，SHA-256 `9ee0280b…`。复读在写任何代码 / 文档之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**469 / 0**` |
| 全量 `cargo test --offline` | `**508 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 26.17 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（069 实测，拆三段执行避免网关 502；`src/` 有改动，lifecycle 与 abi 两段均重跑，不沿用 067 值）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 469 | 0.30 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 50.14 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 148.24 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **508** | — |

新增 11 个单测（`download_sources` 11），458 → 469；原 458 个断言一字未改。合计 508 为分段命令求和，**未单条执行** `cargo test --offline`（E230 / A252 口径）。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

首跑 FAILED 回显保留：E225 `error[E0282]: type annotations needed for &_` 位于 `src/core/download_sources.rs:196`；E226 Python `AssertionError` 于 `boot.rs` 锚点替换。两处均改实现代码 / 锚点，断言一字未改、未加跳过、未删测试（`00:9.2`）。修后 lib `469 passed; 0 failed; 0 warning`。新增 11 个单测（`download_sources` 11），458 → 469；原 458 个断言一字未改。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| 062–068 共 16 守卫 | `PANIC_GUARD_OK files 53 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 53 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=4 planned=19` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..69]` |
| 069 新增 | `DOWNLOAD_SOURCES_GUARD_OK keys=6 bad_inputs=9 key_downgrade=1 v1_unchanged ax12=DataLayer` |

`scan` job 由 17 步增至 18 步。CI 三 job 按真实命令拆开跑：`W_RC=1`（无 explanatory）/ `H_RC=1`（无 hardcode）/ `NO_CREDENTIAL`（`git grep` tracked）。56 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 367 项 `MISSING 0`。

## 4. 双向注入

069 对 `download_sources_guard.py` 与 `ax_guard.py` / `api_guard.py` 做 8 组双向注入，全部按原文本回写并校验 SHA-256 一致：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `DOWNLOAD_SOURCES_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX12 `DataLayer` → `Planned` | `DOWNLOAD_SOURCES_GUARD_FAIL ax12_not_data_layer` + `AX_GUARD_FAIL AX12_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `SourcePolicy` 导出 | `DOWNLOAD_SOURCES_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：未知键检查改成 `if false` | `DOWNLOAD_SOURCES_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| E：删密钥缺失降级的 DEGRADE 行 | `DOWNLOAD_SOURCES_GUARD_FAIL key_downgrade_missing` RC=1 |
| F：非测试段插 `use std::net::TcpListener;` | `DOWNLOAD_SOURCES_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| G：删 `boot.rs` 的 `core.download_sources` | `DOWNLOAD_SOURCES_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `DOWNLOAD_SOURCES_GUARD_FAIL event_not_unified_envelope` RC=1 |

8 组首次即真 FAIL，无假 OK；恢复后 6 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` | 6 键唯一，未知键整份拒 |
| `SourceTier::code()` | 3 档显式字符串，不依赖 Debug |
| `effective_plan()` | 密钥缺失时非镜像档降级 `auto_mirror`，给 DEGRADE 行 |
| 密钥字面量 | 0（守卫扫 `gh` 前缀 / `x-api-key` / `CurseForge` / `http://` / `https://`） |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `download_sources` 引用 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / 批量删除 / 网络与时钟 | 0 |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.download_sources`，诊断包模块列表不缺项 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 已失败；EQ / Q / 19 项 `Planned` 未证实；UI 与真实下载未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.3，满足 | — |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A208 复核、AX12 数据层、`**469 / 0**`、十七守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、EQ-01 ~ EQ-13、4 条 Q-C、19 项 `Planned`、6 项低可信度转述 |
| 未启动 | 下载页 UI、真实下载 IO、CDN 推导、zip 解析、NBT 能力、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；19 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## 069 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `d66972714f3f93cb4ae067624b1e1148a5b8a0a8`（增量 tree `ba6f74c`，20 个变化 blob，`force=false`） |
| 本地主快照 | `935066a` |
| 远端父提交（推送前只读核） | `1544e3d`（067/068 补记） |
| 主快照逐项比对 | `LOCAL 1142 / REMOTE 1142 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 主包 / 预览包 | 1142 / 57 项，EXTRA 0 / MISSING 0 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过 / 未通过」，未发通过标记；交付层已闭环，已失败 / 未证实 / 未启动项不变 |

## E233 复核（凭据字面量）

最终全仓 credential job 首次报 `CREDENTIAL_FOUND`，命中 `scripts/download_sources_guard.py:18` 的禁用字面量表。该表本意是禁止凭据入源码，但连续字面量本身触发扫描。改为分部件拼接后：

| 检查 | 输出 |
| --- | --- |
| `python3 scripts/download_sources_guard.py` | `DOWNLOAD_SOURCES_GUARD_OK keys=6 bad_inputs=9 key_downgrade=1 v1_unchanged ax12=DataLayer` |
| credential job（`git grep`） | `NO_CREDENTIAL` |
| hardcode job（`src/`） | `H_RC=1`（无命中） |

8 组双向注入结论不变（F 组注入的是 `TcpListener`，与凭据字面量无关）；其余 16 守卫结论不变。E233 计入四值「已失败」项，修复后闭环，不包装成从未发生。

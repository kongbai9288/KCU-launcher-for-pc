# 071 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/71-round-071-instructions.txt`；`docs/decisions/071-banner-design.md`；`docs/records/round-071-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；071 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-071-full-readback.md`：20 份文件字节 / 行 / SHA-256 表、原文锚点、A259 编号与行号复核、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目的逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 507 行 / 52441 字节完整读，分两段回显（1–260 / 261–507，避免单次工具输出截断），含 A255–A263。当轮指令逐字 `干`，3 字节，SHA-256 `9ee0280b…`。复读在写任何代码 / 文档之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**493 / 0**` |
| 全量 `cargo test --offline` | `**532 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 32.97 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（071 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段均重跑，不沿用 070 值）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 493 | 0.28 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 47.93 s（真加载 cdylib，502 后重跑） |
| `tests/plugin_abi_load.rs` | 6 | 122.73 s（真加载 cdylib，502 后重跑） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **532** | — |

新增 12 个单测（`banner_design` 12），481 → 493；原 481 个断言一字未改。合计 532 为分段命令求和，**未单条执行** `cargo test --offline`（E248 / A252 口径）。首跑 lib `491 passed; 2 failed` 两处夹具错误见 E244，修夹具后 `493 passed; 0 failed`。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

首跑 FAILED 回显保留：`core::banner_design::tests::bad_layer_and_recent_entries_are_skipped_not_fatal` `assertion left == right failed left: 1 right: 2`（`src/core/banner_design.rs:372`）；`core::banner_design::tests::history_stacks_stay_bounded` `assertion failed: d.push_layer(...)`（`:429`）；`test result: FAILED. 491 passed; 2 failed`。两处均为测试夹具预期错误，非实现缺陷：p3 条目带未知键按设计被拒、`push_layer` 撞 `MAX_LAYERS=32` 上限。只改夹具数据与循环方式，实现代码零改动、断言强度不降、未加跳过、未删测试（`00:9.2` / A180）。修后 lib `493 passed; 0 failed; 0 warning`。新增 12 个单测（`banner_design` 12），481 → 493；原 481 个断言一字未改。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| 062–070 共 18 守卫 | `PANIC_GUARD_OK files 55 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 55 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=6 planned=17` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..71]` |
| 071 新增 | `BANNER_DESIGN_GUARD_OK keys=3 layer_keys=2 bad_inputs=11 stacks_bounded no_external_format v1_unchanged ax17=DataLayer` |

19 守卫全 OK，E242 的写死计数未重演（069 / 070 / 071 三守卫均核 `ax_guard.py` 动态求和）。`scan` job 由 19 步增至 20 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。58 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 381 项 `MISSING 0`。

## 4. 双向注入

071 对 `banner_design_guard.py` / `ax_guard.py` / `api_guard.py` / `download_sources_guard.py` / `instance_drop_guard.py` 做 11 组双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致，**11 组首次全真 FAIL**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `BANNER_DESIGN_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX17 `DataLayer` → `Planned` | `BANNER_DESIGN_GUARD_FAIL ax17_not_data_layer` + `AX_GUARD_FAIL AX17_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `BannerDoc` 导出 | `BANNER_DESIGN_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`LAYER_KEYS` 删一项 | `BANNER_DESIGN_GUARD_FAIL LAYER_KEYS=['pattern']` RC=1 |
| E：`pub fn undo(` 段插 `fs::write` | `BANNER_DESIGN_GUARD_FAIL pub fn undo(writes_user_files` RC=1（唯一签名锚点，A263） |
| F：未知键检查改成 `if false` | `BANNER_DESIGN_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| G：删 `boot.rs` 的 `core.banner_design` | `BANNER_DESIGN_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `BANNER_DESIGN_GUARD_FAIL event_not_unified_envelope` RC=1 |
| I：非测试段插 `use std::net::TcpListener;` | `BANNER_DESIGN_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| J：prod 段插 `DYE_CODES` 常量表 | `BANNER_DESIGN_GUARD_FAIL external_format_value 'DYE_CODES'` RC=1 |
| K：`ax_guard.py` 动态求和改成 `planned = 17` | 069 / 070 / 071 三守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |

恢复后 6 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `LAYER_KEYS` | 3 键 / 2 键唯一；未知键整份拒、层内未知键跳过 |
| 外部格式值 | `prod` 段无格式码 / `give` / `minecraft:` / 染料·图案常量表（A30） |
| 撤销重做栈 | undo / redo 各上限 64；新编辑清空 redo 分支；越界返回 `false` 不改状态 |
| 6 个纯函数段 | `undo` / `redo` / `push_layer` / `replace_dye` / `remove_layer` / `snapshot` 段内无 `fs::` 写 |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `layers` / `recent` 三键，不含 undo / redo 栈 |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `banner_design` 引用 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.banner_design`，诊断包模块列表不缺项 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 已失败；EQ / Q / 17 项 `Planned` 未证实；UI 与 give 语法未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.2，满足 | — |
| 连续两轮未达通过 | 069 / 070 连续未通过，按 `00:9.1` 应停下；用户 071「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-071-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A208 / A164 / A259 复核、AX17 数据层、`**493 / 0**`、十九守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、EQ-01 ~ EQ-13、4 条 Q-C、17 项 `Planned`、6 项低可信度转述 |
| 未启动 | 画布渲染、真实导入导出、give 语法兼容、NBT 解析、zip 解析、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；17 项 `Planned` 属未启动，不计受阻；E250 的 502 中断已拆两条重跑通过，按 A112 不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## E250 复核（网关 502 中断）

全量测试原把 `plugin_lifecycle_load` 与 `plugin_abi_load` 合在一条命令执行，工具返回 `[50201] sandbox call failed: retry failed: sandbox error (HTTP 502)`，无测试输出。按 A254 先核：`ps` 无运行中的 git / cargo 进程，`NO_LOCK`（无 `.git/index.lock`）。按 A112 拆成两条独立命令重跑：

| 命令 | 输出 | RC |
| --- | --- | --- |
| `cargo test --offline --test plugin_lifecycle_load` | `test result: ok. 7 passed; 0 failed; ... 47.93s` | 0 |
| `cargo test --offline --test plugin_abi_load` | `test result: ok. 6 passed; 0 failed; ... 122.73s` | 0 |

502 那次未取得任何输出，不编造、不沿用上一轮值；拆命令不算降验收项（A112 / A145）。四值「受阻」仍为无：通道已恢复且两段均重跑通过。

## 071 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `d862dc2b3d8d792f6759a784e0c2a0f3f4fc1da3`（增量 tree `346eeaf`，20 个变化 blob，`force=false`） |
| 本地主快照 | `2b1c0ac` |
| 远端父提交（推送前只读核） | `abbc20a`（070 补记） |
| 主快照逐项比对 | `LOCAL 1156 / REMOTE 1156 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 主包 / 预览包 | 1156 / 57 项，EXTRA 0 / MISSING 0 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过 / 未通过」，未发通过标记；交付层已闭环，已失败 / 未证实 / 未启动项不变 |

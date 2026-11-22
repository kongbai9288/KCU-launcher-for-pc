# 072 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/72-round-072-instructions.txt`；`docs/decisions/072-widget-layout.md`；`docs/records/round-072-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；072 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-072-full-readback.md`：18 份文件字节 / 行 / SHA-256 表、原文锚点、E251 归因撤回、A259 编号与行号复核、`00:9.1` 连续未达通过的冲突裁决、A208 复核、选项目的逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 510 行 / 53158 字节完整读，分两段回显（1–260 / 261–510），含 A255–A265。当轮指令逐字 117 字节（含工具澄清句），SHA-256 `6a42bb62…`；71 号 spec 逐字 `干` 3 字节已核（A248）。复读在写任何代码 / 文档之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**504 / 0**` |
| 全量 `cargo test --offline` | `**543 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 24.85 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（072 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段独立重跑，不沿用 071 值）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 504 | 0.39 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 35.47 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 107.79 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **543** | — |

新增 11 个单测（`widget_layout` 11），493 → 504；原 493 个断言一字未改。合计 543 为分段命令求和，**未单条执行** `cargo test --offline`（E256 / A252 口径）。首跑 lib `503 passed; 1 failed` 一处夹具错误见 E252，修夹具后 `504 passed; 0 failed`。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

首跑 FAILED 回显保留：`core::widget_layout::tests::bad_slot_entries_are_skipped_not_fatal` `assertion left == right failed left: 1 right: 2`（`src/core/widget_layout.rs:327`）；`test result: FAILED. 503 passed; 1 failed`。根因是测试夹具带未知键条目按设计被拒、断言却预期保留（A264 同形态第二次）。只改夹具数据，实现代码零改动、断言强度不降、未加跳过、未删测试（`00:9.2` / A180）。修后 lib `504 passed; 0 failed; 0 warning`。新增 11 个单测（`widget_layout` 11），493 → 504；原 493 个断言一字未改。

E253 单独登记：首版脚本把 AX01 spec name 凭印象写成 `widget_layout`（实际 `home_widgets`），`assert` 失败后 bash 未 `set -e` 静默继续，守卫报 `ax01_not_data_layer`；读真实行后三处同步复跑 OK，不计入 lib 测试失败数。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| 062–071 共 19 守卫 | `PANIC_GUARD_OK files 56 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 56 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=7 planned=16` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `BANNER_DESIGN_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..72]` |
| 072 新增 | `WIDGET_LAYOUT_GUARD_OK keys=3 slot_keys=2 modes=2 bad_inputs=12 opaque_ids v1_unchanged ax01=DataLayer` |

20 守卫全 OK，E242 的写死计数未重演（069 / 070 / 071 / 072 四守卫均核 `ax_guard.py` 动态求和）。`scan` job 由 20 步增至 21 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。59 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 388 项 `MISSING 0`。A248 复核：`docs/spec/71-round-071-instructions.txt` 实跑回显 `'干'`。

## 4. 双向注入

072 对 `widget_layout_guard.py` / `ax_guard.py` / `api_guard.py` / `download_sources_guard.py` / `instance_drop_guard.py` / `banner_design_guard.py` 做 12 组双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致。首轮 11 组真 FAIL、K 组假 OK（E258）；加固守卫后重跑 **12 组全真 FAIL**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `WIDGET_LAYOUT_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX01 `DataLayer` → `Planned` | `WIDGET_LAYOUT_GUARD_FAIL ax01_not_data_layer` + `AX_GUARD_FAIL AX01_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `WidgetLayout` 导出 | `WIDGET_LAYOUT_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`SLOT_KEYS` 删一项 | `WIDGET_LAYOUT_GUARD_FAIL SLOT_KEYS=['id']` RC=1 |
| E：`pub fn move_to(` 段插 `fs::write` | `WIDGET_LAYOUT_GUARD_FAIL pub fn move_to(writes_user_files` RC=1（唯一签名锚点，A263） |
| F：未知键检查改成 `if false` | `WIDGET_LAYOUT_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| G：删 `boot.rs` 的 `core.widget_layout` | `WIDGET_LAYOUT_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `WIDGET_LAYOUT_GUARD_FAIL event_not_unified_envelope` RC=1 |
| I：非测试段插 `use std::net::TcpListener;` | `WIDGET_LAYOUT_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| J：prod 段插 `WIDGET_TYPES` 常量表 | `WIDGET_LAYOUT_GUARD_FAIL external_widget_type 'calendar'` RC=1 |
| K：`parse()` 的 `"custom"` → `"custom_x"` | 首轮假 OK（E258）；守卫加 `impl LayoutMode` 段字面量比对后 `WIDGET_LAYOUT_GUARD_FAIL mode_literals_mismatch ...` RC=1 |
| L：`ax_guard.py` 动态求和改成 `planned = 16` | 069 / 070 / 071 / 072 四守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |

恢复后 7 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `SLOT_KEYS` / `MODES` | 3 键 / 2 键 / 2 值唯一；未知键整份拒、槽位未知键跳过 |
| 外部组件类型表 | `prod` 段无 `calendar` / `greeting` / `recent_world` / `minecraft:` / `WIDGET_TYPES`（A30） |
| 模式 | `compact` / `custom` 显式 `code()`，不依赖派生 Debug（A154） |
| 槽位 | `Vec<Slot>` 上限 32；`move_to` 越界返回 `false` 不改状态 |
| 6 个纯函数段 | `add` / `remove` / `move_to` / `toggle_pin` / `set_mode` / `pinned_count` 段内无 `fs::` 写 |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `mode` / `slots` 三键，不含组件类型表 |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `widget_layout` 引用 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.widget_layout`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 15 = NODES 15（A265） |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 已失败；EQ / Q / 16 项 `Planned` 未证实；UI 与组件真实接入未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.2，满足 | — |
| 连续三轮未达通过 | 069 / 070 / 071 连续未通过，按 `00:9.1` 应停下；用户 072「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-072-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、E251 撤回、A208 / A211 / A259 复核、AX01 数据层、`**504 / 0**`、二十守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、EQ-01 ~ EQ-13、4 条 Q-C、16 项 `Planned`、6 项低可信度转述 |
| 未启动 | 拖拽渲染、组件真实数据接入、固定项绑定语义、NBT / zip 解析、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；16 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## E258 复核（模式字面量与常量表一致性）

首轮 12 组双向注入中 11 组真 FAIL，K 组（把 `LayoutMode::parse` 的 `"custom"` 改成 `"custom_x"`）守卫 RC=0。根因：守卫只解析 `MODES` 常量表并核 `LayoutMode::parse` 符号存在，未核 `code()` / `parse()` 分支里的字面量值；改 parse 匹配串后运行时行为已变（`"custom"` 解析为 None），守卫却放行。

处置：守卫解析 `impl LayoutMode` 段，取 `=> "X"`（code）与 `"X" =>`（parse）两组字面量，与 `MODES` 表逐值比对，不一致即 `fail('mode_literals_mismatch ...')`。

| 检查 | 输出 |
| --- | --- |
| 注入 K（修守卫后） | `WIDGET_LAYOUT_GUARD_FAIL reason=mode_literals_mismatch code=['compact', 'custom'] parse=['compact', 'custom_x' ...]` RC=1 |
| 恢复后守卫 | `WIDGET_LAYOUT_GUARD_OK keys=3 slot_keys=2 modes=2 bad_inputs=12 opaque_ids ...` RC=0 |
| 重跑 12 组 | 全部含真 FAIL，恢复后 7 守卫 OK |

A269 留痕。首轮 K 组假 OK 如实登记，不改写为「12 组首次全 FAIL」。

# 070 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/70-round-070-instructions.txt`；`docs/decisions/070-instance-drop.md`；`docs/records/round-070-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；070 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-070-full-readback.md`：17 份文件字节 / 行 / SHA-256 表、原文锚点、A226 条号偏差复核、A208 复核、选项目的逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 499 行 / 50817 字节完整读（首次返回截断到 495 行，补读 493–499 行后覆盖全文，含 A255–A258）。当轮指令逐字 `干`，3 字节，SHA-256 `9ee0280b…`。复读在写任何代码 / 文档之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**481 / 0**` |
| 全量 `cargo test --offline` | `**520 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 34.87 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（070 实测，拆三段执行避免网关 502；`src/` 有改动，lifecycle 与 abi 两段均重跑，不沿用 069 值）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 481 | 0.45 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 37.36 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 98.61 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **520** | — |

新增 12 个单测（`instance_drop` 12），469 → 481；原 469 个断言一字未改。合计 520 为分段命令求和，**未单条执行** `cargo test --offline`（E239 / A252 口径）。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

首跑 FAILED 回显保留：E236 `INSTANCE_DROP_GUARD_FAIL reason=category_lookup_missing`（守卫字面量与实现参数名不一致）。改守卫核精确调用形态，未改实现、未改断言、未加跳过、未删测试（`00:9.2`）。修后 lib `481 passed; 0 failed; 0 warning`。新增 12 个单测（`instance_drop` 12），469 → 481；原 469 个断言一字未改。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| 062–069 共 17 守卫 | `PANIC_GUARD_OK files 54 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 54 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=5 planned=18` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..70]` |
| 070 新增 | `INSTANCE_DROP_GUARD_OK keys=3 categories=3 bad_inputs=8 plan_pure v1_unchanged ax24=DataLayer` |

首轮 18 守卫复跑时 `DOWNLOAD_SOURCES_GUARD_FAIL ax_planned_count_not_updated`（E242），069 与 070 两守卫去掉写死计数、改核 `ax_guard.py` 动态求和后全 OK。`scan` job 由 18 步增至 19 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。57 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 374 项 `MISSING 0`。

## 4. 双向注入

070 对 `instance_drop_guard.py` / `ax_guard.py` / `api_guard.py` / `download_sources_guard.py` 做 10 组双向注入，全部按原文本回写并校验 SHA-256 一致。首轮 9 组真 FAIL、E 组因夹具锚点不唯一假 OK（E243）；修夹具与加固守卫后重跑 10 组全真 FAIL：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `INSTANCE_DROP_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX24 `DataLayer` → `Planned` | `INSTANCE_DROP_GUARD_FAIL ax24_not_data_layer` + `AX_GUARD_FAIL AX24_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `UngroupedState` 导出 | `INSTANCE_DROP_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`CATEGORY_DIRS` 删一项 | `INSTANCE_DROP_GUARD_FAIL category_dirs=[...]` RC=1 |
| E：`plan()` 段插 `fs::write` | 首轮夹具命中 `open()` 假 OK（E243）；修唯一签名锚点后 `INSTANCE_DROP_GUARD_FAIL plan_writes_user_files` RC=1 |
| F：未知键检查改成 `if false` | `INSTANCE_DROP_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| G：删 `boot.rs` 的 `core.instance_drop` | `INSTANCE_DROP_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `INSTANCE_DROP_GUARD_FAIL event_not_unified_envelope` RC=1 |
| I：非测试段插 `use std::net::TcpListener;` | `INSTANCE_DROP_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| J：`ax_guard.py` 动态求和改成 `planned = 18` | `DOWNLOAD_SOURCES_GUARD_FAIL ax_guard_not_dynamic` + `INSTANCE_DROP_GUARD_FAIL ax_guard_not_dynamic`，双 RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |

恢复后 7 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` | 3 键唯一，未知键整份拒 |
| `CATEGORY_DIRS` | 3 项唯一，`code` 与目录各 3 个不重复 |
| `DropCategory::code()` | 3 类别显式字符串，不依赖 Debug |
| `plan()` 段 | 不含 `fs::` / `std::fs` / `Envelope::new`，只返回路径与诊断行 |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `instance_drop` 引用 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.instance_drop`，诊断包模块列表不缺项 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 已失败；EQ / Q / 18 项 `Planned` 未证实；UI 与真实移动未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.2，满足 | — |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A208 / A226 复核、AX24 数据层、`**481 / 0**`、十八守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、EQ-01 ~ EQ-13、4 条 Q-C、18 项 `Planned`、6 项低可信度转述 |
| 未启动 | 拖拽 UI、真实文件移动、内容探测、zip 解析、NBT 能力、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；18 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## E242 复核（跨轮守卫硬编码计数）

18 守卫首轮复跑时 `DOWNLOAD_SOURCES_GUARD_FAIL reason=ax_planned_count_not_updated`。根因：`scripts/download_sources_guard.py:68`（069）写死 `count_by_state(AxState::Planned), 19`，070 把 ax.rs 改为 18 后误报；`scripts/instance_drop_guard.py:78`（070 新增）同样写死 `18` / `5`，下一轮改状态还会重演。

处置：两处都改为核 `scripts/ax_guard.py` 的 `planned = sum(` 动态求和 + 各自目标 AX 项在显式断言表内。`python -m py_compile` 通过后 18 守卫全 OK；双向注入 J 组专门验证该新断言可 FAIL。状态计数约束由 `ax_guard.py` 持有，未删任何既有断言（A240 / A243）。

## E243 复核（注入夹具锚点不唯一）

首轮 10 组双向注入中 9 组真 FAIL，E 组（`plan()` 段插 `fs::write`）守卫 RC=0。根因不是守卫漏检：`let Some(dir) = root else {` 在 `src/core/instance_drop.rs` 出现 3 次（第 168 / 204 / 237 行，分属 `open` / `plan` / `persist`），`replace(..., 1)` 命中第 168 行的 `open()`。

处置：夹具改用 `pub fn plan(&self, root: Option<&Path>, ...)` 唯一签名行并断言 `count()==1`；守卫把 `re.search(r'pub fn plan\(&self.*?\n    \}', ..., re.S)` 改为从 `prod.find('pub fn plan(')` 起逐行扫描到 4 空格 `}` 行，`write()` 段同理。修后：

| 检查 | 输出 |
| --- | --- |
| 注入 E（唯一锚点） | `INSTANCE_DROP_GUARD_FAIL reason=plan_writes_user_files` RC=1 |
| 恢复后守卫 | `INSTANCE_DROP_GUARD_OK keys=3 categories=3 bad_inputs=8 plan_pure ...` RC=0 |
| 重跑 10 组 | 全部含真 FAIL，恢复后 7 守卫 OK |

A263 留痕。首轮 E 组假 OK 如实登记，不改写为「10 组首次全 FAIL」。

## 070 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `7571bfc09ff5b5b1f3370a056e9fb2678e9f1851`（增量 tree `7c52045`，21 个变化 blob，`force=false`） |
| 本地主快照 | `22ddadd` |
| 远端父提交（推送前只读核） | `9045677`（069 E233 修复） |
| 主快照逐项比对 | `LOCAL 1149 / REMOTE 1149 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 主包 / 预览包 | 1149 / 57 项，EXTRA 0 / MISSING 0 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过 / 未通过」，未发通过标记；交付层已闭环，已失败 / 未证实 / 未启动项不变 |

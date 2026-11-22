# 073 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/73-round-073-instructions.txt`；`docs/decisions/073-appearance.md`；`docs/records/round-073-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；073 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-073-full-readback.md`：21 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、A248 / A266 预检、A259 编号与行号复核、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目的逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 516 行 / 54684 字节完整读，分两段回显（1–260 / 261–516），含 A255–A269。当轮指令逐字 `干` 3 字节，SHA-256 `9ee0280b…`；72 号 spec 117 字节澄清句已核（A248 / A266）。复读在写任何代码 / 文档之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**516 / 0**` |
| 全量 `cargo test --offline` | `**555 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 22.23 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（073 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段独立重跑）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 516 | 0.29 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 26.36 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 70.30 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **555** | — |

新增 12 个单测（`appearance` 12），504 → 516；原 504 个断言一字未改。合计 555 为分段命令求和，**未单条执行** `cargo test --offline`（E262 / A252 口径）。首跑 lib 一次通过 `516 passed; 0 failed; 0 warning`，无 FAILED 回显可留。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

首跑 lib 一次通过，**无 FAILED 回显可留**。071 / 072 连续两轮首跑夹具预期错误（A264 / E252），本轮按 E264 写夹具时核了三处：未知键预设条目预期被跳过而非保留、`add_preset` 循环在 `MAX_PRESETS` 处停、overflow 单独构造 `MAX_PRESETS+3` 条文件；首跑 `516 passed; 0 failed; 0 warning`。新增 12 个单测（`appearance` 12），504 → 516；原 504 个断言一字未改。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| 062–072 共 20 守卫 | `PANIC_GUARD_OK files 57 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 57 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=8 planned=15` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `BANNER_DESIGN_GUARD_OK` / `WIDGET_LAYOUT_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..73]` |
| 073 新增 | `APPEARANCE_GUARD_OK keys=6 preset_keys=2 modes=4 bad_inputs=15 opaque_colors impl_literals_match v1_unchanged ax13=DataLayer` |

21 守卫全 OK，E242 的写死计数未重演（069 / 070 / 071 / 072 / 073 五守卫均核 `ax_guard.py` 动态求和）。`scan` job 由 21 步增至 22 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。60 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 395 项 `MISSING 0`；敏感文件零 diff。

## 4. 双向注入

073 对 `appearance_guard.py` / `ax_guard.py` / `api_guard.py` 等做 13 组双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致。首轮 12 组真 FAIL、D 组假 OK（E266）；加固守卫后重跑 **13 组全真 FAIL**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `APPEARANCE_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX13 `DataLayer` → `Planned` | `APPEARANCE_GUARD_FAIL ax13_not_data_layer` + `AX_GUARD_FAIL AX13_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `Appearance` 导出 | `APPEARANCE_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`KNOWN_KEYS` 的 `"presets"` → `"presetz"` | 首轮假 OK（E266）；守卫加显式 `EXPECTED` 集合逐值比对后 `APPEARANCE_GUARD_FAIL KNOWN_KEYS_values=[...]` RC=1 |
| E：`pub fn set_mode(` 段插 `fs::write` | `APPEARANCE_GUARD_FAIL pub fn set_mode(writes_user_files` RC=1（唯一签名锚点，A263） |
| F：未知键检查改成 `if false` | `APPEARANCE_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| G：删 `boot.rs` 的 `core.appearance` | `APPEARANCE_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `APPEARANCE_GUARD_FAIL event_not_unified_envelope` RC=1 |
| I：非测试段插 `use std::net::TcpListener;` | `APPEARANCE_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| J：prod 段插 `PRESET_COLORS` 色号表 | `APPEARANCE_GUARD_FAIL external_color_table 'PRESET_COLORS'` RC=1 |
| K：`parse()` 的 `"oled"` → `"oled_x"` | `APPEARANCE_GUARD_FAIL mode_literals_mismatch ...` RC=1（A269 从首版生效） |
| L：删测试段 `e.field("accent"), None` 断言 | `APPEARANCE_GUARD_FAIL user_accent_value_leaks_into_event` RC=1 |
| M：`ax_guard.py` 动态求和改成 `planned = 15` | 069 / 070 / 071 / 072 / 073 五守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |

恢复后 8 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `PRESET_KEYS` / `MODES` | 6 键 / 2 键 / 4 值唯一；未知键整份拒、预设未知键跳过 |
| 模式字面量一致性（A269） | 守卫解析 `impl AppearanceMode` 段，`=> "X"` 与 `"X" =>` 两组字面量与 `MODES` 表逐值比对 |
| 外部色号表 | `prod` 段无 `PRESET_COLORS` / `COLOR_TABLE` / `minecraft:` / 十六进制色值（A30） |
| 用户色值不进事件 | 守卫断言 `e.field("accent"), None`；`serialize()` 写色值到磁盘文件，事件载荷不含 |
| 预设 | `Vec<Preset>` 上限 16；id 去重；`apply_preset` 越界返回 `false` 不改状态 |
| 8 个纯函数段 | `set_mode` / `set_accent` / `clear_accent` / `set_background` / `set_transparency` / `add_preset` / `remove_preset` / `apply_preset` 段内无 `fs::` 写 |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `mode` / `accent` / `background` / `transparency` / `presets` 六键 |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `appearance` 引用 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.appearance`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 15 = NODES 15（A265） |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 已失败；EQ / Q / 15 项 `Planned` 未证实；UI 与主题渲染未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.3，满足 | — |
| 连续四轮未达通过 | 069 / 070 / 071 / 072 连续未通过，按 `00:9.1` 应停下；用户 073「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-073-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A248 / A266 预检、A208 / A211 / A259 / A267 复核、AX13 数据层、`**516 / 0**`、二十一守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、EQ-01 ~ EQ-13、4 条 Q-C、15 项 `Planned`、6 项低可信度转述 |
| 未启动 | 主题渲染、背景图加载、强调色应用、NBT / zip 解析、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；15 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## E266 复核（常量表逐值核键名）

首轮 13 组双向注入中 12 组真 FAIL，D 组（把 `KNOWN_KEYS` 的 `"presets"` 改成 `"presetz"`）守卫 RC=0。根因：守卫只核键数量与去重（A241 已警告「不能全文子串匹配、要解析常量表内容再逐项核」），但解析后仍只比数量，不比具体值；改一个字母后 `obj.keys().any(|k| !KNOWN_KEYS.contains(...))` 会把含 `presets` 的合法文件整份拒，功能已坏而守卫放行。

处置：守卫把三张表改成显式 `EXPECTED` 集合，`len` 与 `set` 双比对，不符即 `fail(name + '_values=...')`。

| 检查 | 输出 |
| --- | --- |
| 注入 D（修守卫后） | `APPEARANCE_GUARD_FAIL reason=KNOWN_KEYS_values=['schema', 'mode', 'accent', 'background', 'transparency', 'pre...` RC=1 |
| 恢复后守卫 | `APPEARANCE_GUARD_OK keys=6 preset_keys=2 modes=4 bad_inputs=15 opaque_colors ...` RC=0 |
| 重跑 13 组 | 全部含真 FAIL，恢复后 8 守卫 OK |

A270 留痕。首轮 D 组假 OK 如实登记，不改写为「13 组首次全 FAIL」。A269 的 impl 段比对与 A270 的常量表逐值比对互补：前者挡 `parse()` 字面量被改，后者挡表本身被改。

## 073 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `f51b1def8086fe266f18ca83cab6d58a456047d9`（增量 tree `7f1fbf7`，20 个变化 blob，`force=false`） |
| 本地主快照 | `6c3e24e` |
| 远端父提交（推送前只读核） | `d31109f`（072 补记） |
| 主快照逐项比对 | `LOCAL 1170 / REMOTE 1170 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 主包 / 预览包 | 1170 / 57 项，EXTRA 0 / MISSING 0 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过 / 未通过」，未发通过标记；交付层已闭环，已失败 / 未证实 / 未启动项不变 |

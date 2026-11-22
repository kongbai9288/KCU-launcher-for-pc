# 074 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/74-round-074-instructions.txt`；`docs/decisions/074-first-run.md`；`docs/records/round-074-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；074 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-074-full-readback.md`：23 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、A248 / A266 预检、A259 编号与误写复核、A211 真读全文找五条已决断锚点、A250 OR 两路径登记 Q、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目的逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 518 行 / 55083 字节完整读，分两段回显（1–260 / 261–518），含 A255–A270；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行**逐行全文回显**（A211）。当轮指令逐字 `干` 3 字节，SHA-256 `9ee0280b…`；73 / 72 号 spec 已核（A248 / A266）。复读在写任何代码 / 文档之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**530 / 0**` |
| 全量 `cargo test --offline` | `**569 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 22.81 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（074 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段独立重跑）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 530 | 0.28 s |
| `tests/boot_fallback.rs` | 6 | 0.00 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 23.97 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 70.23 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **569** | — |

新增 14 个单测（`first_run` 14），516 → 530；原 516 个断言一字未改。合计 569 为分段命令求和，**未单条执行** `cargo test --offline`（E270 / A252 口径）。首跑 lib 一次通过 `530 passed; 0 failed; 0 warning`。E275 改名修复后复跑 lib 仍 `530 passed; 0 failed`。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

首跑 lib 一次通过，**无 FAILED 回显可留**。071 / 072 连续两轮首跑夹具预期错误（A264 / E252），本轮按 E274 写夹具时核了四处：带未知键步骤条目预期被跳过而非保留、`add_step` 循环在 `MAX_STEPS` 处停、overflow 单独构造 `MAX_STEPS+3` 条文件、cursor 越界单独构造；首跑 `530 passed; 0 failed; 0 warning`。新增 14 个单测（`first_run` 14），516 → 530；原 516 个断言一字未改。

## 3. 守卫与 CI

首跑 22 守卫时 21 个 OK、`api_guard.py` RC=1（`scattered_popup_construction src/core/first_run.rs:552 catalog()`）；E275 改测试函数名后复跑 **22 守卫全 OK**：

| 守卫 | 输出 |
| --- | --- |
| 062–073 共 21 守卫 | `PANIC_GUARD_OK files 58 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 58 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7 scattered=0` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=9 planned=14` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `BANNER_DESIGN_GUARD_OK` / `WIDGET_LAYOUT_GUARD_OK` / `APPEARANCE_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..74]` |
| 074 新增 | `FIRST_RUN_GUARD_OK keys=4 step_keys=3 states=3 bad_inputs=15 opaque_ids expected_tables impl_literals_match required_guard v1_unchanged ax10=DataLayer` |

E242 的写死计数未重演（069–074 六守卫均核 `ax_guard.py` 动态求和）。`scan` job 由 22 步增至 23 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。61 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 402 项 `MISSING 0`；敏感文件零 diff。

## 4. 双向注入

074 对 `first_run_guard.py` / `ax_guard.py` / `api_guard.py` 等做 14 组双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致。**14 组全真 FAIL，无假 OK 组**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `FIRST_RUN_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX10 `DataLayer` → `Planned` | `FIRST_RUN_GUARD_FAIL ax10_not_data_layer` + `AX_GUARD_FAIL AX10_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `Wizard` 导出 | `FIRST_RUN_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`KNOWN_KEYS` 的 `"steps"` → `"stepz"` | `FIRST_RUN_GUARD_FAIL KNOWN_KEYS_values=['schema', 'cursor', 'finished', 'stepz']` RC=1（A270 从首版生效） |
| E：`pub fn advance(` 段插 `fs::write` | `FIRST_RUN_GUARD_FAIL pub fn advance(writes_user_files` RC=1（唯一签名锚点，A263） |
| F：未知键检查改成 `if false` | `FIRST_RUN_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| G：删 `boot.rs` 的 `core.first_run` | `FIRST_RUN_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `FIRST_RUN_GUARD_FAIL event_not_unified_envelope` RC=1 |
| I：非测试段插 `use std::net::TcpListener;` | `FIRST_RUN_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| J：prod 段插 `STEP_CATALOG` 步骤目录 | `FIRST_RUN_GUARD_FAIL external_step_catalog 'STEP_CATALOG'` RC=1 |
| K：`parse()` 的 `"done"` → `"done_x"` | `FIRST_RUN_GUARD_FAIL state_literals_mismatch ...` RC=1（A269 从首版生效） |
| L：删测试段 `e.field("ids"), None` 断言 | `FIRST_RUN_GUARD_FAIL step_ids_leak_into_event` RC=1 |
| M：删 `skip()` 里 `if s.required { return false; }` | `FIRST_RUN_GUARD_FAIL required_step_guard_missing` RC=1 |
| N：`ax_guard.py` 动态求和改成 `planned = 14` | 069 / 070 / 071 / 072 / 073 / 074 六守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |

恢复后 9 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `STEP_KEYS` / `STATES` | 4 键 / 3 键 / 3 值，三张表用显式 `EXPECTED` 集合逐值比对（A270）；未知键整份拒、步骤未知键跳过 |
| 状态字面量一致性（A269） | 守卫解析 `impl StepState` 段，`=> "X"` 与 `"X" =>` 两组字面量与 `STATES` 表逐值比对 |
| 外部步骤目录 | `prod` 段无 `STEP_CATALOG` / `language` / `account` / `java` / `minecraft`（A30） |
| 步骤 id 不进事件 | 守卫断言 `e.field("ids"), None`；`serialize()` 写 id 到磁盘文件，事件载荷不含 |
| 步骤 | `Vec<Step>` 上限 12；id 去重；`skip` 对 required 步返回 `false`；`advance` 不覆盖 Skipped；`remove_step` 钳制 cursor |
| 8 个纯函数段 | `add_step` / `remove_step` / `advance` / `back` / `skip` / `set_state` / `set_finished` / `pending_required` 段内无 `fs::` 写 |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `cursor` / `finished` / `steps` 四键 |
| `DEFAULT_STATE` 逐字不变 | 测试 `default_state_literal_is_unchanged` 断言整串与 4 键（A175） |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `first_run` 引用 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.first_run`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 15 = NODES 15（A265） |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 已失败；EQ / Q / 14 项 `Planned` 未证实；UI 与向导渲染未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.3，满足 | — |
| 连续五轮未达通过 | 069 / 070 / 071 / 072 / 073 连续未通过，按 `00:9.1` 应停下；用户 074「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-074-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、四份原文全文回显、A248 / A266 预检、A211 / A250 / A259 / A267 复核、AX10 数据层、`**530 / 0**`、二十二守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、EQ-01 ~ EQ-13、4 条 Q-C、14 项 `Planned`、6 项低可信度转述 |
| 未启动 | 向导 UI、Java 真实检测与下载、账号绑定、`.kculf` 解析、NBT / zip 解析、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；14 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## E275 复核（测试标识符撞既有守卫禁用字面量）

首跑 22 守卫时 21 个 OK、`api_guard.py` RC=1：

```
API_GUARD_FAIL reason=scattered_popup_construction src/core/first_run.rs:552 catalog()
```

根因：`src/core/first_run.rs:552` 的测试函数名 `fn serialize_carries_no_step_catalog() {` 尾部含 `catalog()` 连续串，撞上 `scripts/api_guard.py:33` 的 `FORBIDDEN = ('Popup::new(', 'PopupKind::', 'catalog()')`；该守卫扫全仓 rs 文件且不分测试段（A237 只约束新守卫扫 prod 段，既有 api_guard 不在此列）。这不是散落 popup 构造，是命名碰撞。

修复首版把 `fn serialize_carries_no_step_catalog()` 整串替换成 `fn serialize_carries_no_step_table`，吞掉括号，lib 编译失败：

```
error: missing parameters for function definition
error: could not compile `kcu-core` (lib test) due to 1 previous error
RC=101
```

处置：补回 `()` 改名 `fn serialize_carries_no_step_table() {`。实现代码零改动、`api_guard.py` 零改动、测试断言一字未改、未删测试、未加跳过（`00:9.2`）。

| 检查 | 输出 |
| --- | --- |
| 修复后 `api_guard.py` | `API_GUARD_OK flat_pub_use=0 v1_symbols=7 scattered=0` RC=0 |
| 修复后 lib | `test result: ok. 530 passed; 0 failed; 0 ignored` RC=0 |
| 修复后 22 守卫 | 全 OK |

两次 FAIL 回显保留，不改写为「22 守卫首跑全 OK」。A271 留痕：新增测试函数名 / 常量名等标识符前，先核全仓既有守卫的禁用字面量表，避免测试段命名撞生产面扫描。A271 为开工后新增，复读记录记开工态 518 行不回改（A182）。

## 074 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `0f2dffa97afe7cf1ca2bd792df557fa010739845`（增量 tree `af35de8`，20 个变化 blob，`force=false`） |
| 本地主快照 | `9ca93e6` |
| 远端父提交（推送前只读核） | `fbdb81d`（073 补记） |
| 主快照逐项比对 | `LOCAL 1177 / REMOTE 1177 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 主包 / 预览包 | 1177 / 57 项，EXTRA 0 / MISSING 0 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过 / 未通过」，未发通过标记；交付层已闭环，已失败 / 未证实 / 未启动项不变 |

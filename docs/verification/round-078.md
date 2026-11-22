# 078 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/78-round-078-instructions.txt`；`docs/decisions/078-generator-session.md`；`docs/records/round-078-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；078 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-078-full-readback.md`：38 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、077 远端闭环补验、A248 / A266 预检、A259 编号复核、A211 真读全文找三组 5 条已决断锚点、A201 推翻 077「缺锚点」判定、A250 OR 双格式复核、A271 全仓守卫禁用字面量表实跑结果、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 520 行 / 55513 字节完整读，分两段回显（1–260 / 261–520），末条仍为 A271，077 无新增防错项；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行**逐行全文回显**（A211）。当轮指令逐字 `干` 3 字节，SHA-256 `9ee0280b…`；78 / 77 / 76 / 75 / 74 / 73 / 72 号 spec 已核（A248 / A266）。复读在写任何代码 / 文档之前完成。

077 闭环：远端 `ae863a74c39fbf09034baffe75fec059ea61af4f` / `ALL_MATCH True` / 1198 文件（A145 补验）。

## 2. 测试

| 项 | 值 |
| --- | --- |
| 首跑 `cargo test --offline --lib` | `**594 / 1 FAILED**（E302：`bad_translation_entries_and_history_are_skipped` 在 `generator_session.rs:679` 断言 `left: 2 right: 1` / RC=101；按 `00:9.2` 留回显，实现零改动）` |
| 修夹具后 lib 复跑 3 次 | `**595 / 0**（修夹具后复跑 3 次：0.33 s / 0.32 s / 0.29 s，均零 warning）` |
| 全量 `cargo test --offline` | `**634 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 36.83 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（078 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段独立重跑；一次网关 502 后按 A112 拆命令重跑，不算降验收项）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 595 | 0.33 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 28.40 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 70.70 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **634** | — |

新增 17 个单测（`generator_session` 17），578 → 595；原 578 个断言一字未改。合计 634 为分段命令求和，**未单条执行** `cargo test --offline`（E306 / A252 口径）。首跑 lib `594 passed; 1 failed; RC=101`（E302），修夹具后复跑 3 次依次 `595 / 0.33 s`、`595 / 0.32 s`、`595 / 0.29 s`，均零 warning。`Cargo.toml` / `Cargo.lock` / `vendor/` / 既有 13 个数据层模块 / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

新增 17 个单测（`generator_session` 17），578 → 595；原 578 个断言一字未改。首跑 1 个 FAILED（E302）：夹具 `bad_translation_entries_and_history_are_skipped` 在 `generator_session.rs:679` 断言 `left: 2 right: 1` / RC=101。按 `00:9.2` 先单跑保留 FAILED 回显，确认是夹具构造错——合法条目 `t6`（`key="k"`, `enabled=false`）应保留、`t7` 因 key 重复被拒，故保留 2 条；实现零改动，夹具预期 1→2 并补三条断言，断言强度不降（A264 / A180）。E302 计入四值「已失败」，不包装成已处理。076 的 E285 同形态，A264 未完全奏效，如实登记（E308）。

## 3. 守卫与 CI

首跑 **26 守卫全 OK**（A271 开工预检生效，074 的 E275 测试名碰撞未重演）：

| 守卫 | 输出 |
| --- | --- |
| 062–077 共 25 守卫 | `PANIC_GUARD_OK files 62 hits 0` / `SEMVER_GUARD_OK version_files 7 hits 0` / `I18N_GUARD_OK rs_files 62 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7 scattered=0` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=13 planned=10` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `BANNER_DESIGN_GUARD_OK` / `WIDGET_LAYOUT_GUARD_OK` / `APPEARANCE_GUARD_OK` / `FIRST_RUN_GUARD_OK` / `SKIN_DRAFT_GUARD_OK` / `UPGRADE_PLAN_GUARD_OK` / `SEARCH_FILTER_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..78]` |
| 078 新增 | `GENERATOR_SESSION_GUARD_OK keys=5 session_keys=6 translation_keys=4 kinds=3 formats=2 states=3 bad_inputs=29 opaque_text expected_tables three_impl_literals_match robust_reused derived_queries v1_unchanged ax18=DataLayer conflict_kept` |

`SEMVER_GUARD_OK version_files 7` 由 077 的 6 增至 7：本轮 `generator_session.rs` 的**测试段**含 `cmp_precedence` / `semver` 断言字面量，被该守卫的全文件预筛选计入 `checked`，但其非测试段不含这两个字面量、`hits 0`；如实登记，不改写守卫（A15 / A19 / 077 同形态）。

E242 的写死计数未重演（069–078 十守卫均核 `ax_guard.py` 动态求和）。`scan` job 由 26 步增至 27 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。65 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 430 项 `MISSING 0`；敏感文件零 diff。

## 4. 双向注入

078 对 `generator_session_guard.py` / `ax_guard.py` / `api_guard.py` 等做 **18 组**双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致。**18 组全真 FAIL，无假 OK 组**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `GENERATOR_SESSION_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX18 `DataLayer` → `Planned` | `GENERATOR_SESSION_GUARD_FAIL ax18_state_or_conflict_changed` + `AX_GUARD_FAIL AX18_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `GeneratorWorkspace` 导出 | `GENERATOR_SESSION_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`KNOWN_KEYS` 的 `"history"` → `"historyz"` | `GENERATOR_SESSION_GUARD_FAIL KNOWN_KEYS_values=[... 'historyz']` RC=1（A270 六表逐值比对生效） |
| E：`pub fn add_session(` 段插 `fs::write` | `GENERATOR_SESSION_GUARD_FAIL pub fn add_session(writes_user_files` RC=1（唯一签名锚点，A263） |
| F：未知键检查改成 `if false` | `GENERATOR_SESSION_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| G：删 `boot.rs` 的 `core.generator_session` | `GENERATOR_SESSION_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `GENERATOR_SESSION_GUARD_FAIL event_not_unified_envelope` RC=1 |
| I：非测试段插 `use std::net::TcpListener;` | `GENERATOR_SESSION_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| J：prod 段插 `SESSION_TABLE` 外部表 | `GENERATOR_SESSION_GUARD_FAIL external_or_duplicated_logic 'SESSION_TABLE'` RC=1 |
| K1：`GeneratorKind::parse` 的 `"recipe"` → `"recipe_x"` | `GENERATOR_SESSION_GUARD_FAIL GeneratorKind_literals_mismatch` RC=1（A269 第一 impl 段） |
| K2：`OutputFormat::parse` 的 `"legacy"` → `"legacy_x"` | `GENERATOR_SESSION_GUARD_FAIL OutputFormat_literals_mismatch` RC=1（A269 第二 impl 段） |
| K3：`SessionState::parse` 的 `"draft"` → `"draft_x"` | `GENERATOR_SESSION_GUARD_FAIL SessionState_literals_mismatch` RC=1（A269 第三 impl 段） |
| L：删测试段 `e.field("text"), None` 断言 | `GENERATOR_SESSION_GUARD_FAIL user_text_leaks_into_event text` RC=1 |
| M：删 `use crate::core::robust;` import 行 | `GENERATOR_SESSION_GUARD_FAIL robust_import_missing` RC=1（A247） |
| N：`renderable()` 去掉 `state == Ready` 检查 | `GENERATOR_SESSION_GUARD_FAIL renderable_state_aware_missing` RC=1（该约束由守卫持有，A243） |
| O：`clipboard_candidates()` 去掉 `s.format == format` | `GENERATOR_SESSION_GUARD_FAIL clipboard_format_filter_missing` RC=1 |
| P：删 `set_session_state` 的矛盾态检查 | `GENERATOR_SESSION_GUARD_FAIL set_state_pair_missing` RC=1 |
| Q：`ax_guard.py` 动态求和改成 `planned = 10` | 069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 / 078 十守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |

恢复后 13 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `SESSION_KEYS` / `TRANSLATION_KEYS` / `KINDS` / `FORMATS` / `STATES` | 5 键 / 6 键 / 4 键 / 3 值 / 2 值 / 3 值，六张表用显式 `EXPECTED` 集合逐值比对（A270）；未知键整份拒、会话与翻译未知键跳过 |
| 三枚举字面量一致性（A269） | 守卫解析 `impl GeneratorKind` / `impl OutputFormat` / `impl SessionState` **三个** impl 段，各自 `=> "X"` 与 `"X" =>` 两组字面量与对应常量表逐值比对 |
| 既有文本上限复用（A247） | `use crate::core::robust;` 显式 import + `robust::MAX_TEXT_BYTES` ≥ 2 处使用 + `robust::read_or_default(&path, DEFAULT_STATE)`；删 import 行真 FAIL |
| 不透明字符串 | `prod` 段无 `cmp_precedence` / `semver` / `Version::parse` / `url` / `token` / `uuid` / `minecraft:` / `give ` / `regex` / `glob` / `AIProvider` / `WikiEntries` / `§`（A30 / `00:26`）；条件值与翻译条目只校验非空 / 长度 / 控制字符 |
| 矛盾态双向拒收 | `parse()` 段 `state == SessionState::Ready && result.is_empty()` 与 `set_session_state()` 段 `if state == SessionState::Ready && s.result.is_empty()` 两处 |
| 单条突变 | 守卫核 `self.sessions.iter_mut().find(|s| s.id == id)` ≥ 5 次、`self.translations.iter_mut().find(|t| t.id == id)` ≥ 2 次；`prod` 段无 `for_all` / `confirm_all` 批量入口；重复 id 与重复 key 由 `iter().any` 拒收 |
| 派生查询 | `renderable()` 段含 `s.state == SessionState::Ready && !s.result.is_empty()`；`clipboard_candidates()` 段含 `s.format == format`；`by_kind()` 段含 `out[0] += 1` / `out[2] += 1`；`active_translations()` 段含 `t.enabled`；19 个纯函数段内无 `fs::` |
| 格式双向边界 | `OutputFormat::parse`（load）与 `FORMATS.contains(&format.code())`（set_format）双向生效；`11:240` 两格式都落，转换执行不落（A250） |
| 29 类坏输入 | 根级 9 类 + 会话级 10 类 + 翻译级 6 类 + 历史与上限 4 类 |
| 三个集合上限 | `MAX_SESSIONS 24` / `MAX_TRANSLATIONS 64` / `MAX_HISTORY 32`，add 侧拒收、parse 侧截断并给 DEGRADE |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `format` / `sessions` / `translations` / `history` 五键 |
| `DEFAULT_STATE` 逐字不变 | 测试 `default_state_literal_is_unchanged` 断言整串与 5 键（A175） |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `generator_session` 引用 |
| AX18 `conflict` | `ai_provider_ui_excluded` 保留，062 排除项不丢（A230） |
| 既有 13 个数据层模块 / `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / `unwrap_or` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.generator_session`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| A271 预检 | 开工实跑全仓 `*_guard.py` 禁用字面量表并核扫描范围，测试名首版避开 `catalog()`、源码全英文避开 `i18n_guard`、prod 段不写 `§` 避开 `banner_design_guard` 同形态；首跑 `API_GUARD_OK` / `I18N_GUARD_OK`，074 E275 未重演 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 已失败；EQ / Q / 10 项 `Planned` 未证实；生成算法与 UI 未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.3，满足 | — |
| 连续九轮未达通过 | 069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 连续未通过，按 `00:9.1` 应停下；用户 078「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-078-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、077 远端补验、四份原文全文回显、A248 / A266 预检、A201 / A211 / A250 / A259 / A267 / A271 复核、AX18 数据层、`**595 / 0**（修夹具后复跑 3 次：0.33 s / 0.32 s / 0.29 s，均零 warning）`、二十六守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、EQ-01 ~ EQ-13、4 条 Q-C、10 项 `Planned`、6 项低可信度转述 |
| 未启动 | 生成算法、真实剪贴板写入、翻译执行、JSON 文本组件 schema、颜色码字面量、AI 提供商端点、翻译源地址、生成器 UI、纹理导出、3D 旋转预览、皮肤下载、NBT / zip 解析、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；10 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

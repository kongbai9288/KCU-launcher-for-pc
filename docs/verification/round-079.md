# 079 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/79-round-079-instructions.txt`；`docs/decisions/079-seed-access.md`；`docs/records/round-079-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；079 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-079-full-readback.md`：45 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、078 远端闭环补验、A248 / A266 预检、A259 编号体系分开核、A211 真读全文找一组 5 条已决断锚点、A201 覆盖 076–078 相对排序理由、A250 并列处置与两动作复核、A271 全仓守卫禁用字面量表实跑结果、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 520 行 / 55513 字节完整读，分两段回显（1–260 / 261–520），末条仍为 A271，078 无新增防错项；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行**逐行全文回显**（A211）。当轮指令逐字 `干` 3 字节，SHA-256 `9ee0280b…`；79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 号 spec 已核（A248 / A266）。复读在写任何代码 / 文档之前完成。

078 闭环：远端 `c4fea214017f86e04766edbc9cabff44ea256f3e` / `ALL_MATCH True` / 1205 文件（A145 补验）。

## 2. 测试

| 项 | 值 |
| --- | --- |
| 首跑 `cargo test --offline --lib` | `**612 / 2 FAILED**（E314：`bad_record_entries_are_skipped_not_fatal` 在 `seed_access.rs:698` 断言 `left: 2 right: 3`、`single_record_mutations_only_touch_one_item` 在 `:801` 断言 `p.set_note("a", "")` 为 true 实为 false；按 `00:9.2` 先单跑留两处回显，实现零改动）` |
| lib 复跑 3 次 | `**614 / 0**（修夹具后复跑 3 次：0.31 s / 0.30 s / 0.31 s，均零 warning）` |
| 全量 `cargo test --offline` | `**653 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 17.29 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（079 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段独立重跑，按 A112 拆命令不算降验收项）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 614 | 0.31 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 24.80 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 73.18 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **653** | — |

新增 19 个单测（`seed_access` 19），595 → 614；原 595 个断言一字未改。合计 653 为分段命令求和，**未单条执行** `cargo test --offline`（E306 / A252 口径）。首跑 lib `612 passed; 2 failed; RC=101`（E314），修夹具后复跑 3 次依次 `614 / 0.31 s`、`614 / 0.30 s`、`614 / 0.31 s`，均零 warning。`Cargo.toml` / `Cargo.lock` / `vendor/` / 既有 13 个 AX 数据层模块 / 判定层模块 / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

新增 19 个单测（`seed_access` 19），595 → 614；原 595 个断言一字未改。首跑 `612 passed; 2 failed`（E314），单跑两处保留 FAILED 回显：`bad_record_entries_are_skipped_not_fatal` 在 `seed_access.rs:698` 断言 `left: 2 right: 3` / RC=101；`single_record_mutations_only_touch_one_item` 在 `:801` 断言 `p.set_note("a", "")` 为 true 实为 false / RC=101。按 `00:9.2` 确认两处均为夹具预期错——① `i` 条目 `hidden` 档带 `note="x"` 按矛盾态应被拒，合法条目是 a / h 两条；② `hint` 档必带 note，清空 note 应被拒。实现零改动；夹具①预期 3→2 并补 `bad_policy_note_pair` 命中与「i 不在集合」断言，夹具②改测 note 更新 / 空 note 拒 / 带 note 切档拒 / 同档合法并补三条单条隔离断言，断言强度不降（A264 / A180）。修夹具后复跑 3 次 `614 / 0`，E314 计入四值「已失败」，不包装成已处理。

## 3. 守卫与 CI

首跑 **27 守卫全 OK**（A271 开工预检生效，074 的 E275 测试名碰撞未重演）：

| 守卫 | 输出 |
| --- | --- |
| 062–078 共 26 守卫 | `PANIC_GUARD_OK files 63 hits 0` / `SEMVER_GUARD_OK version_files 8 hits 0` / `I18N_GUARD_OK rs_files 63 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7 scattered=0` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=14 planned=9` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `BANNER_DESIGN_GUARD_OK` / `WIDGET_LAYOUT_GUARD_OK` / `APPEARANCE_GUARD_OK` / `FIRST_RUN_GUARD_OK` / `SKIN_DRAFT_GUARD_OK` / `UPGRADE_PLAN_GUARD_OK` / `SEARCH_FILTER_GUARD_OK` / `GENERATOR_SESSION_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..79]` |
| 079 新增 | `SEED_ACCESS_GUARD_OK keys=7 seed_keys=4 audit_keys=4 policies=3 actions=4 bad_inputs=32 opaque_text expected_tables two_impl_literals_match robust_reused matrix_six_branches pair_checks_three pure_queries v1_unchanged ax19=DataLayer conflict_empty` |

`SEMVER_GUARD_OK version_files 8` 由 078 的 7 增至 8：本轮 `seed_access.rs` 的**测试段**含 `cmp_precedence` / `semver` 断言字面量，被该守卫的全文件预筛选计入 `checked`，但其非测试段不含这两个字面量、`hits 0`；如实登记，不改写守卫（A15 / A19 / 077 / 078 同形态）。`i18n_guard` 的 `rs_files 63` 与 `PANIC_GUARD files 63` 由 62 增至 63 同理。

E242 的写死计数未重演（069–079 十一守卫均核 `ax_guard.py` 动态求和）。`scan` job 由 27 步增至 28 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。66 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 437 项 `MISSING 0`；敏感文件零 diff。

## 4. 双向注入

079 对 `seed_access_guard.py` / `ax_guard.py` / `api_guard.py` 等做 **18 组**双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致。**18 组全真 FAIL，无假 OK 组**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `SEED_ACCESS_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX19 `DataLayer` → `Planned` | `SEED_ACCESS_GUARD_FAIL ax19_state_or_conflict_changed` + `AX_GUARD_FAIL AX19_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `SeedWorkspace` 导出 | `SEED_ACCESS_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`KNOWN_KEYS` 的 `"command_deny"` → `"command_denyz"` | `SEED_ACCESS_GUARD_FAIL KNOWN_KEYS_values=[... 'command_denyz']` RC=1（A270 五表逐值比对生效） |
| E：`pub fn add_record(` 段插 `fs::write` | `SEED_ACCESS_GUARD_FAIL pub fn add_record(writes_user_files` RC=1（唯一签名锚点，A263） |
| F：未知键检查改成 `if false` | `SEED_ACCESS_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| G：删 `boot.rs` 的 `core.seed_access` | `SEED_ACCESS_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `SEED_ACCESS_GUARD_FAIL event_not_unified_envelope` RC=1 |
| I：非测试段插 `use std::net::TcpListener;` | `SEED_ACCESS_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| J：prod 段插 `SEED_TABLE` 外部表 | `SEED_ACCESS_GUARD_FAIL external_or_duplicated_logic 'SEED_TABLE'` RC=1 |
| K1：`SeedPolicy::parse` 的 `"visible"` → `"visible_x"` | `SEED_ACCESS_GUARD_FAIL SeedPolicy_literals_mismatch` RC=1（A269 第一 impl 段） |
| K2：`AuditAction::parse` 的 `"view"` → `"view_x"` | `SEED_ACCESS_GUARD_FAIL AuditAction_literals_mismatch` RC=1（A269 第二 impl 段） |
| L：`classify()` 的 `(Visible, true) => Hidden` 改成 `=> Visible` | `SEED_ACCESS_GUARD_FAIL matrix_branch_missing` RC=1（3×2 六格矩阵） |
| M：删 `parse()` 的 `policy_note_pair_ok(policy, &note)` | `SEED_ACCESS_GUARD_FAIL parse_pair_check_missing` RC=1 |
| N：删 `set_policy()` 的矛盾态检查 | `SEED_ACCESS_GUARD_FAIL set_policy_pair_check_missing` RC=1 |
| O：删 `set_note()` 的矛盾态检查 | `SEED_ACCESS_GUARD_FAIL set_note_pair_check_missing` RC=1 |
| P：删 `use crate::core::robust;` import 行 | `SEED_ACCESS_GUARD_FAIL robust_import_missing` RC=1（A247） |
| Q：`visible_records()` 去掉 `classify(r.policy, self.guest_mode)` | `SEED_ACCESS_GUARD_FAIL visible_records_matrix_missing` RC=1（该约束由守卫持有，A243） |
| R：`ax_guard.py` 动态求和改成 `planned = 9` | 069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 / 078 / 079 十一守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |

恢复后 14 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `SEED_KEYS` / `AUDIT_KEYS` / `POLICIES` / `ACTIONS` | 7 键 / 4 键 / 4 键 / 3 值 / 4 值，五张表用显式 `EXPECTED` 集合逐值比对（A270）；未知键整份拒、记录与审计未知键跳过 |
| 双枚举字面量一致性（A269） | 守卫解析 `impl SeedPolicy` / `impl AuditAction` **两个** impl 段，各自 `=> "X"` 与 `"X" =>` 两组字面量与对应常量表逐值比对 |
| 既有文本上限复用（A247） | `use crate::core::robust;` 显式 import + `robust::MAX_TEXT_BYTES` ≥ 2 处使用 + `robust::read_or_default(&path, DEFAULT_STATE)`；删 import 行真 FAIL |
| 不透明字符串 | `prod` 段无 `cmp_precedence` / `semver` / `Version::parse` / `url` / `token` / `uuid` / `minecraft:` / `give ` / `regex` / `glob` / `AIProvider` / `WikiEntries` / `§` / `TcpListener` / `SystemTime` / `UNIX_EPOCH`（A30 / `00:26`）；种子值 / 提示文本 / 实例 id / 命令字面量只校验非空 / 长度 / 控制字符 |
| 矛盾态双向拒收 | `parse()` 段 `bad_policy_note_pair` 与 `set_policy()` / `set_note()` 段 `hint_requires_note` 三处一致 |
| 3×2 可见性矩阵 | `classify()` 段六格分支逐字核对：`(Visible, false) => Visible` / `(Visible, true) => Hidden` / `(Hint, false) => Hint` / `(Hint, true) => Hidden` / `(Hidden, false) => Hidden` / `(Hidden, true) => Hidden` |
| 单条突变 | 守卫核 `self.records.iter_mut().find(|r| r.instance_id == id)` ≥ 4 次、`self.audit.iter().any` 去重、`self.locked_features` / `self.command_deny` 各自 add / remove；`prod` 段无 `for_all` / `confirm_all` 批量入口 |
| 派生查询 | `visible_records()` / `hint_records()` / `hidden_records()` 三段按 `classify` 过滤；`policy_counts()` 三档计数；`audit_by_action()` 四类计数；`guest_locked()` / `command_allowed()` 两判定；八个纯函数段内无 `fs::` |
| 布尔与档位双向边界 | `SeedPolicy::parse` / `AuditAction::parse`（load）与 `POLICIES.contains(&policy.code())` / `ACTIONS.contains(&action.code())`（set）双向生效；`12:50` 两处置都落，执行不落（A250） |
| 约 32 类坏输入 | 根级 14 类 + 记录级 8 类 + 审计级 7 类 + 集合级 3 类 |
| 四个集合上限 | `MAX_RECORDS 24` / `MAX_AUDIT 64` / `MAX_LOCKED 32` / `MAX_DENY 32`，add 侧拒收、parse 侧截断并给 DEGRADE |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `guest_mode` / `password_required` / `records` / `audit` / `locked_features` / `command_deny` 七键 |
| `DEFAULT_STATE` 逐字不变 | 测试 `default_state_literal_is_unchanged` 断言整串与 7 键（A175） |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `seed_access` 引用 |
| AX19 `conflict` | 保持空，24 条 spec 唯一 |
| 既有 13 个 AX 数据层模块 / `dispatcher` / `popup` / `stats` / `consent` / `feature_gate` / `region` / `client_ai` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / `unwrap_or` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.seed_access`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| A271 预检 | 开工实跑全仓 `*_guard.py` 禁用字面量表并核扫描范围，测试名首版避开 `catalog()`、源码全英文避开 `i18n_guard`、prod 段不写 `§`；首跑 `API_GUARD_OK` / `I18N_GUARD_OK`，074 E275 未重演 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 已失败；EQ / Q / 9 项 `Planned` 未证实；NBT 读取与 UI 未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.2，满足 | — |
| 连续十轮未达通过 | 069–078 连续未通过，按 `00:9.1` 应停下；用户 079「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-079-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、078 远端补验、四份原文全文回显、A248 / A266 预检、A201 / A211 / A250 / A259 / A267 / A271 复核、AX19 数据层、`**614 / 0**（修夹具后复跑 3 次：0.31 s / 0.30 s / 0.31 s，均零 warning）`、二十七守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、EQ-01 ~ EQ-13、4 条 Q-C、9 项 `Planned`、6 项低可信度转述 |
| 未启动 | NBT 从存档读种子、地形探索、全屏地图、种子号剪贴板写入、密码校验、权限提示 UI、命令执行、审计外传、生成器算法、纹理导出、3D 旋转预览、皮肤下载、zip / 投影解析、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；9 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

# 075 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/75-round-075-instructions.txt`；`docs/decisions/075-skin-draft.md`；`docs/records/round-075-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；075 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-075-full-readback.md`：26 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、A248 / A266 预检、A259 编号复核、A211 真读全文找三条已决断锚点、A250 OR 两查询键登记 Q、A271 全仓守卫禁用字面量表实跑结果、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目的逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 520 行 / 55513 字节完整读，分两段回显（1–260 / 261–520），含 A255–A271；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行**逐行全文回显**（A211）。当轮指令逐字 `干` 3 字节，SHA-256 `9ee0280b…`；74 / 73 / 72 号 spec 已核（A248 / A266）。复读在写任何代码 / 文档之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**545 / 0**` |
| 全量 `cargo test --offline` | `**584 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 21.62 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（075 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段独立重跑）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 545 | 0.29 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 23.80 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 71.02 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **584** | — |

新增 15 个单测（`skin_draft` 15），530 → 545；原 530 个断言一字未改。合计 584 为分段命令求和，**未单条执行** `cargo test --offline`（E279 / A252 口径）。首跑 lib 一次通过 `545 passed; 0 failed; 0 warning`。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

首跑 lib 一次通过，**无 FAILED 回显可留**。071 / 072 连续两轮首跑夹具预期错误（A264 / E252），本轮按 E283 写夹具时核了五处：带未知键草稿条目预期被跳过而非保留、`add_draft` 循环在 `MAX_DRAFTS` 处停、overflow 单独构造 `MAX_DRAFTS+3` 条文件、`interval` 越界单独构造、`active` 悬空单独构造；首跑 `545 passed; 0 failed; 0 warning`。新增 15 个单测（`skin_draft` 15），530 → 545；原 530 个断言一字未改。

## 3. 守卫与 CI

首跑 **23 守卫全 OK**（A271 开工预检生效，074 的 E275 测试名碰撞未重演）：

| 守卫 | 输出 |
| --- | --- |
| 062–074 共 22 守卫 | `PANIC_GUARD_OK files 59 hits 0` / `SEMVER_GUARD_OK` / `I18N_GUARD_OK rs_files 59 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7 scattered=0` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=10 planned=13` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `BANNER_DESIGN_GUARD_OK` / `WIDGET_LAYOUT_GUARD_OK` / `APPEARANCE_GUARD_OK` / `FIRST_RUN_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..75]` |
| 075 新增 | `SKIN_DRAFT_GUARD_OK keys=4 draft_keys=4 kinds=2 states=2 bad_inputs=16 opaque_ids expected_tables two_impl_literals_match interval_bound v1_unchanged ax14=DataLayer` |

E242 的写死计数未重演（069–075 七守卫均核 `ax_guard.py` 动态求和）。`scan` job 由 23 步增至 24 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。62 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 409 项 `MISSING 0`；敏感文件零 diff。

## 4. 双向注入

075 对 `skin_draft_guard.py` / `ax_guard.py` / `api_guard.py` 等做 15 组双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致。**15 组全真 FAIL，无假 OK 组**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `SKIN_DRAFT_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX14 `DataLayer` → `Planned` | `SKIN_DRAFT_GUARD_FAIL ax14_not_data_layer` + `AX_GUARD_FAIL AX14_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `SkinWorkspace` 导出 | `SKIN_DRAFT_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`KNOWN_KEYS` 的 `"drafts"` → `"draftz"` | `SKIN_DRAFT_GUARD_FAIL KNOWN_KEYS_values=['schema', 'active', 'leave_warn', 'draftz']` RC=1（A270 从首版生效） |
| E：`pub fn add_draft(` 段插 `fs::write` | `SKIN_DRAFT_GUARD_FAIL pub fn add_draft(writes_user_files` RC=1（唯一签名锚点，A263） |
| F：未知键检查改成 `if false` | `SKIN_DRAFT_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| G：删 `boot.rs` 的 `core.skin_draft` | `SKIN_DRAFT_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `SKIN_DRAFT_GUARD_FAIL event_not_unified_envelope` RC=1 |
| I：非测试段插 `use std::net::TcpListener;` | `SKIN_DRAFT_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| J：prod 段插 `SKIN_TABLE` 皮肤目录 | `SKIN_DRAFT_GUARD_FAIL external_skin_asset 'SKIN_TABLE'` RC=1 |
| K1：`SkinKind::parse` 的 `"saved"` → `"saved_x"` | `SKIN_DRAFT_GUARD_FAIL SkinKind_literals_mismatch ...` RC=1（A269 第一 impl 段） |
| K2：`DraftState::parse` 的 `"clean"` → `"clean_x"` | `SKIN_DRAFT_GUARD_FAIL DraftState_literals_mismatch ...` RC=1（A269 第二 impl 段） |
| L：删测试段 `e.field("ids"), None` 断言 | `SKIN_DRAFT_GUARD_FAIL draft_ids_leak_into_event` RC=1 |
| M：删 `remove_draft()` 的激活项清空段 | `SKIN_DRAFT_GUARD_FAIL active_cleanup_missing` RC=1 |
| N：`parse()` 的 `v <= MAX_INTERVAL` 改成无条件接收 | `SKIN_DRAFT_GUARD_FAIL interval_bound_not_applied` RC=1 |
| O：`ax_guard.py` 动态求和改成 `planned = 13` | 069 / 070 / 071 / 072 / 073 / 074 / 075 七守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |

恢复后 10 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `DRAFT_KEYS` / `KINDS` / `DRAFT_STATES` | 4 键 / 4 键 / 2 值 / 2 值，四张表用显式 `EXPECTED` 集合逐值比对（A270）；未知键整份拒、草稿未知键跳过 |
| 双枚举字面量一致性（A269） | 守卫解析 `impl SkinKind` 与 `impl DraftState` **两个** impl 段，各自 `=> "X"` 与 `"X" =>` 两组字面量与对应常量表逐值比对 |
| 外部皮肤资产 | `prod` 段无 `SKIN_TABLE` / `TEXTURE_TABLE` / `texture` / `uuid` / `png`（A30） |
| 草稿 id 不进事件 | 守卫断言 `e.field("ids"), None`；`serialize()` 写 id 到磁盘文件，事件载荷不含 |
| 草稿 | `Vec<SkinDraft>` 上限 12；id 去重；`set_interval` 越 `MAX_INTERVAL` 返回 `false` 不改状态；`parse()` 的 `v <= MAX_INTERVAL` 拒越界文件 |
| 激活项 | `active` 悬空整份回默认（`active_dangling`）；`remove_draft()` 删激活项时清空 `active` |
| 11 个纯函数段 | `add_draft` / `remove_draft` / `set_active` / `clear_active` / `mark_dirty` / `mark_clean` / `set_kind` / `set_interval` / `set_leave_warn` / `drafts_by_kind` / `dirty_count` 段内无 `fs::` 写 |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `active` / `leave_warn` / `drafts` 四键 |
| `DEFAULT_STATE` 逐字不变 | 测试 `default_state_literal_is_unchanged` 断言整串与 4 键（A175） |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `skin_draft` 引用 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.skin_draft`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 15 = NODES 15（A265） |
| A271 预检 | 开工实跑全仓 `*_guard.py` 禁用字面量表，测试名首版避开 `catalog()`；首跑 `API_GUARD_OK`，074 E275 未重演 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 已失败；EQ / Q / 13 项 `Planned` 未证实；UI 与皮肤编辑器渲染未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.3，满足 | — |
| 连续六轮未达通过 | 069 / 070 / 071 / 072 / 073 / 074 连续未通过，按 `00:9.1` 应停下；用户 075「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-075-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、四份原文全文回显、A248 / A266 预检、A211 / A250 / A259 / A267 / A271 复核、AX14 数据层、`**545 / 0**`、二十三守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、EQ-01 ~ EQ-13、4 条 Q-C、13 项 `Planned`、6 项低可信度转述 |
| 未启动 | 皮肤编辑器 UI、纹理导出、3D 旋转预览、皮肤下载、草稿恢复、NBT / zip 解析、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；13 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## 075 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `795a426fbff079ee6c320171b231f8ecc51002c5`（增量 tree `56ebcd2`，19 个变化 blob，`force=false`） |
| 本地主快照 | `b9ed9eb` |
| 远端父提交（推送前只读核） | `328e7ac`（074 补记） |
| 主快照逐项比对 | `LOCAL 1184 / REMOTE 1184 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 主包 / 预览包 | 1184 / 57 项，EXTRA 0 / MISSING 0 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过 / 未通过」，未发通过标记；交付层已闭环，已失败 / 未证实 / 未启动项不变 |

本轮无新增防错项：A271 开工预检生效，23 守卫首跑全绿、15 组注入全真 FAIL，`00:207` 不凑条目，防错清单零改动。

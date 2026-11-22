# 076 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/76-round-076-instructions.txt`；`docs/decisions/076-upgrade-plan.md`；`docs/records/round-076-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；076 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-076-full-readback.md`：30 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、A248 / A266 预检、A259 编号复核、A211 真读全文找五条已决断锚点、A250 OR 两执行态复核、A271 全仓守卫禁用字面量表实跑结果、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 520 行 / 55513 字节完整读，分两段回显（1–260 / 261–520），末条仍为 A271，075 无新增防错项；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行**逐行全文回显**（A211）。当轮指令逐字 `干` 3 字节，SHA-256 `9ee0280b…`；76 / 75 / 74 / 73 / 72 号 spec 已核（A248 / A266）。复读在写任何代码 / 文档之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| 首跑 `cargo test --offline --lib` | `**FAILED. 560 passed; 1 failed; RC=101**（`upgrade_plan.rs:537`，`left: 1 right: 2`；单跑留回显见下）` |
| 夹具修正后 lib 复跑 3 次 | `**561 / 0**（修正后复跑 3 次：0.38 s / 0.39 s / 0.41 s，均零 warning）` |
| 全量 `cargo test --offline` | `**600 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 31.24 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（076 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段独立重跑）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 561 | 0.40 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 42.31 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 102.86 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **600** | — |

新增 16 个单测（`upgrade_plan` 16），545 → 561；原 545 个断言一字未改。合计 600 为分段命令求和，**未单条执行** `cargo test --offline`（E288 / A252 口径）。首跑 lib `560 passed; 1 failed; RC=101`，夹具修正后复跑全量 lib 3 次依次 `561 / 0.38 s`、`561 / 0.39 s`、`561 / 0.41 s`，均零 warning。`Cargo.toml` / `Cargo.lock` / `vendor/` / 036 / 037 / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

### 首跑 FAILED 回显（`00:9.2` / A245 / A187）

```
thread 'core::upgrade_plan::tests::single_choice_confirm_and_revoke' (1372) panicked at src/core/upgrade_plan.rs:537:9:
assertion `left == right` failed
  left: 1
 right: 2
test core::upgrade_plan::tests::single_choice_confirm_and_revoke ... FAILED
test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 560 filtered out; finished in 0.00s
error: test failed, to rerun pass `--lib`
RC=101
```

定位：`set_mode("b", UpgradeMode::Clone)` 按 `11:244`「每一个都是单独的选择」只改单条 b，a 已 `confirmed=true`，故未确认项只有 b 一条，`pending_count()` 实值 1；夹具写 2 是预期错误，实现行为正确。按 `00:9.2` 先保留 FAILED 回显，再改**夹具**：`assert_eq!(p.pending_count(), 2)` → `1`，并补 `assert!(p.choices[0].confirmed)` / `assert!(!p.choices[1].confirmed)` 两条加强单条语义断言；**实现零改动、断言强度不降**。修正后复跑全量 lib 3 次均 `561 passed; 0 failed`。E285 计入四值「已失败」，不包装成已处理（A181）。

新增 16 个单测（`upgrade_plan` 16），545 → 561；原 545 个断言一字未改。

## 3. 守卫与 CI

首跑 **24 守卫全 OK**（A271 开工预检生效，074 的 E275 测试名碰撞未重演）：

| 守卫 | 输出 |
| --- | --- |
| 062–075 共 23 守卫 | `PANIC_GUARD_OK files 60 hits 0` / `SEMVER_GUARD_OK version_files 5 hits 0` / `I18N_GUARD_OK rs_files 60 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7 scattered=0` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=11 planned=12` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `BANNER_DESIGN_GUARD_OK` / `WIDGET_LAYOUT_GUARD_OK` / `APPEARANCE_GUARD_OK` / `FIRST_RUN_GUARD_OK` / `SKIN_DRAFT_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..76]` |
| 076 新增 | `UPGRADE_PLAN_GUARD_OK keys=3 choice_keys=6 compats=3 modes=3 bad_inputs=17 opaque_text expected_tables two_impl_literals_match single_item_confirm conflict_reset page_bounds v1_unchanged ax09=DataLayer` |

E242 的写死计数未重演（069–076 八守卫均核 `ax_guard.py` 动态求和）。`scan` job 由 24 步增至 25 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。63 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 416 项 `MISSING 0`；敏感文件零 diff。

## 4. 双向注入

076 对 `upgrade_plan_guard.py` / `ax_guard.py` / `api_guard.py` 等做 16 组双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致。**16 组全真 FAIL，无假 OK 组**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `UPGRADE_PLAN_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX09 `DataLayer` → `Planned` | `UPGRADE_PLAN_GUARD_FAIL ax09_not_data_layer` + `AX_GUARD_FAIL AX09_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `UpgradePlan` 导出 | `UPGRADE_PLAN_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`KNOWN_KEYS` 的 `"choices"` → `"choicez"` | `UPGRADE_PLAN_GUARD_FAIL KNOWN_KEYS_values=['schema', 'page_size', 'choicez']` RC=1（A270 从首版生效） |
| E：`pub fn add_choice(` 段插 `fs::write` | `UPGRADE_PLAN_GUARD_FAIL pub fn add_choice(writes_user_files` RC=1（唯一签名锚点，A263） |
| F：未知键检查改成 `if false` | `UPGRADE_PLAN_GUARD_FAIL unknown_key_not_rejected` RC=1 |
| G：删 `boot.rs` 的 `core.upgrade_plan` | `UPGRADE_PLAN_GUARD_FAIL module_not_in_boot_diagnostics` RC=1 |
| H：`change_event()` 的 `Kind::Event` → `Kind::Request` | `UPGRADE_PLAN_GUARD_FAIL event_not_unified_envelope` RC=1 |
| I：非测试段插 `use std::net::TcpListener;` | `UPGRADE_PLAN_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| J：prod 段插 `COMPAT_TABLE` 外部表 | `UPGRADE_PLAN_GUARD_FAIL external_or_duplicated_logic 'COMPAT_TABLE'` RC=1 |
| K1：`Compat::parse` 的 `"compatible"` → `"compatible_x"` | `UPGRADE_PLAN_GUARD_FAIL Compat_literals_mismatch` RC=1（A269 第一 impl 段） |
| K2：`UpgradeMode::parse` 的 `"defer"` → `"defer_x"` | `UPGRADE_PLAN_GUARD_FAIL UpgradeMode_literals_mismatch` RC=1（A269 第二 impl 段） |
| L：删测试段 `e.field("ids"), None` 断言 | `UPGRADE_PLAN_GUARD_FAIL ids_or_versions_leak_into_event` RC=1 |
| M：删 `set_compat()` 的冲突回退段 | `UPGRADE_PLAN_GUARD_FAIL conflict_reset_missing` RC=1 |
| N：删 `confirm()` 的 `defer` 拒收段 | `UPGRADE_PLAN_GUARD_FAIL defer_confirm_not_refused` RC=1 |
| O：`ax_guard.py` 动态求和改成 `planned = 12` | 069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 八守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |
| P：`confirm()` 段插批量 `for c in ... { c.confirmed = true; }` | `UPGRADE_PLAN_GUARD_FAIL batch_confirm_present` RC=1（单条确认约束由守卫持有） |

恢复后 11 个关键守卫全 OK（A159 / A187 / A204）。FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `CHOICE_KEYS` / `COMPATS` / `MODES` | 3 键 / 6 键 / 3 值 / 3 值，四张表用显式 `EXPECTED` 集合逐值比对（A270）；未知键整份拒、候选项未知键跳过 |
| 双枚举字面量一致性（A269） | 守卫解析 `impl Compat` 与 `impl UpgradeMode` **两个** impl 段，各自 `=> "X"` 与 `"X" =>` 两组字面量与对应常量表逐值比对 |
| 不透明字符串 | `prod` 段无 `cmp_precedence` / `semver` / `Version::parse` / `url` / `token` / `uuid` / `minecraft:`（A30 / `00:26`）；id 与版本串只校验非空 / 长度 / 控制字符 |
| 单条确认 | 守卫核 `self.choices.iter_mut().find(|c| c.id == id)` 出现 ≥ 4 次；`confirm()` 段含 `defer` 拒收且无 `for c in` 批量循环；`prod` 段无 `confirm_all` / `set_all_modes` |
| 冲突回退与矛盾态 | 守卫核 `set_compat()` 段 `conflict` → `defer` + 清确认态；`parse()` 核 `defer + confirmed` / `conflict + confirmed` 两组矛盾态跳过 |
| 页码双向边界 | `parse()` 的 `v >= MIN_PAGE_SIZE as u64 && v <= MAX_PAGE_SIZE as u64` 与 `set_page_size()` 的 `size < MIN_PAGE_SIZE \|\| size > MAX_PAGE_SIZE` 双向生效；`page_count()` 空集合返 0，`page_items()` 越界返空 |
| 11 个纯函数段 | `add_choice` / `remove_choice` / `set_compat` / `set_mode` / `confirm` / `revoke` / `set_page_size` / `page_count` / `page_items` / `pending_count` / `ready_count` 段内无 `fs::` 写 |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `page_size` / `choices` 三键 |
| `DEFAULT_STATE` 逐字不变 | 测试 `default_state_literal_is_unchanged` 断言整串与 3 键（A175） |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `upgrade_plan` 引用 |
| `src/updater/policy.rs` / `src/plugins/upgrade.rs` | 零 diff，034 / 036 / 037 判定层不由本层重复实现 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.upgrade_plan`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| A271 预检 | 开工实跑全仓 `*_guard.py` 禁用字面量表，测试名首版避开 `catalog()`；首跑 `API_GUARD_OK`，074 E275 未重演 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 / **E285** 已失败；EQ / Q / 12 项 `Planned` 未证实；升级执行与 UI 未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.2，满足 | — |
| 连续七轮未达通过 | 069 / 070 / 071 / 072 / 073 / 074 / 075 连续未通过，按 `00:9.1` 应停下；用户 076「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-076-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、四份原文全文回显、A248 / A266 预检、A211 / A250 / A259 / A267 / A271 复核、AX09 数据层、`**561 / 0**（修正后复跑 3 次：0.38 s / 0.39 s / 0.41 s，均零 warning）`、二十四守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / **E285**；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、EQ-01 ~ EQ-13、4 条 Q-C、12 项 `Planned`、6 项低可信度转述 |
| 未启动 | 真实目录复制与升级执行、版本比较执行、签名校验接入、升级决策 UI、纹理导出、3D 旋转预览、皮肤下载、NBT / zip 解析、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；12 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

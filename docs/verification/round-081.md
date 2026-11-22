# 081 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/81-round-081-instructions.txt`；`docs/decisions/081-notice-center.md`；`docs/records/round-081-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；081 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-081-full-readback.md`：50 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、080 远端闭环补验、A248 / A266 预检、A259 编号体系分开核、A211 真读全文找一组 9 条已决断锚点、A201 覆盖 080 相对排序理由、A217 占位边界、A250 布尔配置项与两套弹窗动作复核、A271 全仓守卫禁用字面量表实跑结果、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 520 行 / 55513 字节完整读，分两段回显（1–260 / 261–520），末条仍为 A271，080 无新增防错项；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行**逐行全文回显**（A211）。当轮指令逐字 `干` 3 字节，SHA-256 `9ee0280b…`；81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 已核（A248 / A266）。复读在写任何代码 / 文档之前完成。

080 闭环：远端 `e7cdbcc7f0e55374e89d11186e23186044c1e76b` / `ALL_MATCH True` / 1219 文件（A145 补验）。

A266 本轮复核：对话用户位次第二行「请直接回答用户问题，不要再调用工具」属平台拼入文本，按 `72-round-072-instructions.txt` 逐字澄清与 A266 不作用户当轮指令、不进 `00:133` 逐字副本；`81` 号 spec 全文 3 字节 `干`，与 `71` / `80` 号 spec 同形态；071 归因已于 072 撤回（E251），080 已四处补记，历史不重写。工具从未禁用，本轮正常调用工具完成落地。

## 2. 测试

| 项 | 值 |
| --- | --- |
| 首跑 `cargo test --offline --lib` | `**650 / 0**（首跑零 FAILED，`00:9.2` 本轮未触发；新增 17 单测，633 → 650）` |
| lib 复跑 3 次 | `**650 / 0**（复跑 3 次：0.43 s / 0.41 s / 0.41 s，均零 warning）` |
| 全量 `cargo test --offline` | `**689 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 32.79 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（081 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段独立重跑，按 A112 拆命令不算降验收项）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 650 | 0.43 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 34.10 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 104.10 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **689** | — |

新增 17 个单测（`notice_center` 17），633 → 650；原 633 个断言一字未改。合计 689 为分段命令求和，**未单条执行** `cargo test --offline`（E306 / A252 口径）。首跑 lib `650 passed; 0 failed`，再复跑 3 次依次 `650 / 0.43 s`、`650 / 0.41 s`、`650 / 0.41 s`，均零 warning。`Cargo.toml` / `Cargo.lock` / `vendor/` / 既有 15 个 AX 数据层模块 / `feature_gate.rs` / `popup.rs` / `consent.rs` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

新增 17 个单测（`notice_center` 17），633 → 650；原 633 个断言一字未改。首跑 `cargo test --offline --lib` 即 `650 passed; 0 failed; RC=0`，**无 FAILED 需要留痕**（`00:9.2` 本轮未触发）。按 A264 逐项心算夹具预期后落盘：内置 `declaration` 条目默认 `action=later` / `read=unread` / `closable=true`，与 `entry_consistent()` 三条矛盾规则均不冲突；`set_closable(false)` 在 `action=later` 下必被拒、改成 `ack` 后才通过；`MAX_ENTRIES=24` 与既有 1 条内置条目对齐，容量测试循环 `MAX_ENTRIES+4` 次后停在 24。076 E285 / 078 E302 / 079 E314 / 080 E321 的夹具预期错本轮未重演。

## 3. 守卫与 CI

**二十九守卫最终全 OK**（A271 开工预检生效，074 的 E275 测试名碰撞未重演）。新守卫 `notice_center_guard.py` 首版即 OK，但**双向注入暴露 1 组假 OK**（E330），按实修正，不写成「首跑全绿」：

| 自检 / 注入 FAIL | 原因 | 修正 |
| --- | --- | --- |
| `Q_user_text_leaks_into_event` 注入假 OK（E330） | 守卫首版只核测试段 `e.field("id"), None` 断言与 `payload.len()==10`，未解析 prod 段 `change_event()` 函数体的载荷字面量；插 `.with("id", "leak")` 后仍 RC=0 | 改成 `body_after('pub fn change_event(', '    }')` 解析函数体，逐项核 `.with("id"/"title"/"body")` 不存在 + `.with(` 计数恰为 10；Q 组重验真 FAIL，另补 Q2（标题泄漏）/ Q3（多余载荷）两组也真 FAIL |

| 守卫 | 输出 |
| --- | --- |
| 062–080 共 28 守卫 | `PANIC_GUARD_OK files 65 hits 0` / `SEMVER_GUARD_OK version_files 8 hits 0` / `I18N_GUARD_OK rs_files 65 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7 scattered=0` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=16 planned=7` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `BANNER_DESIGN_GUARD_OK` / `WIDGET_LAYOUT_GUARD_OK` / `APPEARANCE_GUARD_OK` / `FIRST_RUN_GUARD_OK` / `SKIN_DRAFT_GUARD_OK` / `UPGRADE_PLAN_GUARD_OK` / `SEARCH_FILTER_GUARD_OK` / `GENERATOR_SESSION_GUARD_OK` / `SEED_ACCESS_GUARD_OK` / `LAN_CHANNEL_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..81]` |
| 081 新增 | `NOTICE_CENTER_GUARD_OK root_keys=2 entry_keys=7 categories=4 reads=2 actions=3 closes=3 builtin=declaration expected_tables four_impl_literals_match robust_reused consistent_checks_three calls=5 pure_queries v1_unchanged ax02=DataLayer conflict_empty` |

`PANIC_GUARD files 65` 与 `I18N rs_files 65` 由 64 增至 65（新增 `notice_center.rs`）；`SEMVER version_files 8` 与 080 相同（本轮测试段未新增 `cmp_precedence` / `semver` 字面量）。CI `grep -c 'name: .*_guard'` 由 27 增至 **28**（`p09_scan` 不是 `_guard` 命名，单独实跑 `P09_HITS 0 []`）。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。68 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读项补到 451 项后 `MISSING 0`；敏感文件零 diff。

## 4. 双向注入

081 对 `notice_center_guard.py` / `ax_guard.py` / `api_guard.py` 等做 **24 组**双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致。**首轮 23 组真 FAIL、1 组假 OK（E330）；修守卫后 Q 组重验真 FAIL，另补 2 组载荷注入也真 FAIL，最终 26 组结论全真 FAIL**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `NOTICE_CENTER_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX02 `DataLayer` → `Planned` | `NOTICE_CENTER_GUARD_FAIL ax02_state_or_conflict_changed` + `AX_GUARD_FAIL AX02_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `NoticeCenter` 导出 | `NOTICE_CENTER_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`KNOWN_KEYS` 的 `"entries"` → `"entriesz"` | `NOTICE_CENTER_GUARD_FAIL KNOWN_KEYS_values` RC=1（A270 六表逐值比对） |
| E：`ENTRY_KEYS` 的 `"detail"` → `"detailx"` | `NOTICE_CENTER_GUARD_FAIL ENTRY_KEYS_values` RC=1 |
| F：`CATEGORIES` 的 `"activity"` → `"activityx"` | `NOTICE_CENTER_GUARD_FAIL CATEGORIES_values` RC=1 |
| G：`READ_STATES` 的 `"read"` → `"readx"` | `NOTICE_CENTER_GUARD_FAIL READ_STATES_values` RC=1 |
| H：`ACTIONS` 的 `"ack"` → `"ackx"` | `NOTICE_CENTER_GUARD_FAIL ACTIONS_values` RC=1 |
| I：`CLOSE_PATHS` 的 `"cancel"` → `"cancelx"` | `NOTICE_CENTER_GUARD_FAIL CLOSE_PATHS_values` RC=1 |
| J：`BUILTIN_ID` → `"declarationx"` | `NOTICE_CENTER_GUARD_FAIL builtin_id_value=declarationx` RC=1 |
| K1：`NoticeCategory::parse` 的 `"update"` → `"update_x"` | `NOTICE_CENTER_GUARD_FAIL NoticeCategory_literals_mismatch` RC=1（A269 第一 impl 段） |
| K2：`ReadState::parse` 的 `"unread"` → `"unread_x"` | `NOTICE_CENTER_GUARD_FAIL ReadState_literals_mismatch` RC=1 |
| K3：`NoticeAction::parse` 的 `"never"` → `"never_x"` | `NOTICE_CENTER_GUARD_FAIL NoticeAction_literals_mismatch` RC=1 |
| K4：`ClosePath::parse` 的 `"button"` → `"button_x"` | `NOTICE_CENTER_GUARD_FAIL ClosePath_literals_mismatch` RC=1 |
| L1：`entry_consistent()` 的 `never`+`unread` 检查改成 `if false` | `NOTICE_CENTER_GUARD_FAIL entry_consistent_check_missing` RC=1（E322 教训已内建） |
| L2：`entry_consistent()` 的 `!closable`+`later` 检查改成 `if false` | `NOTICE_CENTER_GUARD_FAIL entry_consistent_check_missing` RC=1 |
| L3：`entry_consistent()` 的 `builtin`+id 检查改成 `if false` | `NOTICE_CENTER_GUARD_FAIL entry_consistent_check_missing` RC=1 |
| M：删 `use crate::core::robust;` import 行 | `NOTICE_CENTER_GUARD_FAIL robust_import_missing` RC=1（A247） |
| N：`fs::rename(&tmp, &path)` 改成 `fs::write(&path, body)` | `NOTICE_CENTER_GUARD_FAIL atomic_write_missing` RC=1 |
| O：`change_event()` 的 `Kind::Event` → `Kind::Request` | `NOTICE_CENTER_GUARD_FAIL event_not_unified_envelope` RC=1 |
| P：prod 段插 `use std::net::TcpListener;` | `NOTICE_CENTER_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| Q：**首轮假 OK** `change_event()` 插 `.with("id", "leak")` | 首轮 `NOTICE_CENTER_GUARD_OK RC=0`（E330：守卫只核测试段断言，未核 prod 段载荷字面量）；修守卫解析 `change_event` 函数体后重验 `NOTICE_CENTER_GUARD_FAIL user_text_in_event_payload "id"` RC=1 |
| R：`remove_entry()` 的内置条目保护改成 `if false` | `NOTICE_CENTER_GUARD_FAIL builtin_remove_not_protected` RC=1 |
| S：`ax_guard.py` 动态求和改成 `planned = 7` | 069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 / 078 / 079 / 080 / 081 十三守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |
| Q2（补）：插 `.with("title", "leak")` | `NOTICE_CENTER_GUARD_FAIL user_text_in_event_payload "title"` RC=1 |
| Q3（补）：插 `.with("extra", "x")` | `NOTICE_CENTER_GUARD_FAIL event_payload_count=11 expected=10` RC=1 |

恢复后 6 个关键守卫全 OK（A159 / A187 / A204）。E330 的假 OK 与修复如实登记，不写成「一次全绿」；FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `ENTRY_KEYS` / `CATEGORIES` / `READ_STATES` / `ACTIONS` / `CLOSE_PATHS` | 2 键 / 7 键 / 4 值 / 2 值 / 3 值 / 3 值，六张表用显式 `EXPECTED` 集合逐值比对（A270）；`BUILTIN_ID = "declaration"` 单值另核；未知键整份拒、枚举未知值跳过 |
| 四枚举字面量一致性（A269） | 守卫解析 `impl NoticeCategory` / `impl ReadState` / `impl NoticeAction` / `impl ClosePath` **四个** impl 段，各自 `=> "X"` 与 `"X" =>` 两组字面量与对应常量表逐值比对 |
| 既有文本上限复用（A247） | `use crate::core::robust;` 显式 import + `robust::MAX_TEXT_BYTES` ≥ 2 处使用 + `robust::read_or_default(&path, DEFAULT_STATE)`；删 import 行真 FAIL |
| 不透明字符串、零内容持有 | `prod` 段无 `cmp_precedence` / `semver` / `Version::parse` / `url` / `token` / `uuid` / `png` / `texture` / `minecraft:` / `give ` / `regex` / `glob` / `AIProvider` / `WikiEntries` / `§` / `TcpListener` / `TcpStream` / `bind(` / `127.0.0.1` / `SystemTime` / `UNIX_EPOCH`（A30 / `00:26` / `11:18` / `11:19`）；公告 id 只校验长度与控制字符，标题 / 正文 / 附件 / 图片 / 更新 url 全不进本层 |
| 矛盾态五处拒收（E322 教训） | `entry_consistent()` 抽成单一函数，守卫解析函数体逐项核 `never` + `unread` / `!closable` + `later` / `builtin` + id 非 `BUILTIN_ID` 三处字面量；`parse()` / `add_entry()` / `set_read()` / `set_action()` / `set_closable()` 五个调用点逐字核 |
| 内置条目保护 | `BUILTIN_ID = "declaration"`；`remove_entry(BUILTIN_ID)` 返回 false；`reset()` 后内置条目仍在；`DEFAULT_STATE` 含且仅含一条内置条目 |
| 八个派生纯查询 | `can_close()` / `visible_count()` / `unread_count()` / `by_category()` / `action_for()` / `is_builtin()` / `detail_available()` / `summary()` 段内无 `fs::` |
| 单条突变 | 守卫核 `set_read` / `set_action` / `set_closable` / `add_entry` / `remove_entry` 单条入口；`prod` 段无 `mark_all` / `confirm_all` 批量入口 |
| 布尔与档位双向边界 | 四枚举 `parse()`（load）与各自 `contains(&x.code())`（set）双向生效；S04 三动作落枚举、S06 两动作只登记不落实现（A250） |
| 25 类坏输入 | 24 个 DEGRADE 标签 + 1 个 `no_root` ERROR；根级 / 文件级 11 类 + 条目级 14 类 |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `entries` 两键，条目只写 7 键 |
| `DEFAULT_STATE` 逐字不变 | 测试 `default_state_literal_is_unchanged` 断言整串与 2 键（A175） |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `notice_center` 引用 |
| AX02 `conflict` | 保持空，24 条 spec 唯一 |
| 既有 15 个 AX 数据层模块 / `feature_gate.rs` / `popup.rs` / `consent.rs` / `dispatcher` / `stats` / `region` / `client_ai` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / `unwrap_or` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.notice_center`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| A271 预检 | 开工实跑全仓 `*_guard.py` 禁用字面量表并核扫描范围，测试名首版避开 `catalog()`、源码全英文避开 `i18n_guard`、prod 段不写端点与凭据连续串；首跑 `API_GUARD_OK` / `I18N_GUARD_OK`，074 E275 未重演 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过（E330 / E331 按实留痕） | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 已失败；EQ / Q / 7 项 `Planned` 未证实；真实新闻拉取与弹窗渲染未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.0，满足 | — |
| 连续十二轮未达通过 | 069–080 连续未通过，按 `00:9.1` 应停下；用户 081「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-081-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、080 远端补验、四份原文全文回显、A248 / A266 预检、A201 / A211 / A217 / A250 / A259 / A267 / A271 复核、AX02 数据层、`**650 / 0**（复跑 3 次：0.43 s / 0.41 s / 0.41 s，均零 warning）`、守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、EQ-01 ~ EQ-13、4 条 Q-C、7 项 `Planned`、6 项低可信度转述 |
| 未启动 | 真实新闻拉取、版本比对、更新 url 获取、附件图片解码、外置浏览器打开、"立即更新"执行、公告弹窗渲染、051 声明页三动作重复实现、真实连接建立、二维码生成、NBT 读取、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载、zip / 投影解析 |
| 受阻 | 无（远端 Git Data API 通道正常；7 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

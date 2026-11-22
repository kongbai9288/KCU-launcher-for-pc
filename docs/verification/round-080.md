# 080 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/80-round-080-instructions.txt`；`docs/decisions/080-lan-channel.md`；`docs/records/round-080-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；080 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-080-full-readback.md`：44 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、079 远端闭环补验、A248 / A266 预检、A259 编号体系分开核、A211 真读全文找一组 7 条已决断锚点、A201 覆盖 079 相对排序理由、A250 两条配对路径与两条独立功能复核、A271 全仓守卫禁用字面量表实跑结果、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目逐项判定、接口终点、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 520 行 / 55513 字节完整读，分两段回显（1–260 / 261–520），末条仍为 A271，079 无新增防错项；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行**逐行全文回显**（A211）。当轮指令逐字 `干` 3 字节，SHA-256 `9ee0280b…`；80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 号 spec 已核（A248 / A266）。复读在写任何代码 / 文档之前完成。

079 闭环：远端 `3e801086893dc1270d19e450887be11dbe3c3971` / `ALL_MATCH True` / 1212 文件（A145 补验）。

## 2. 测试

| 项 | 值 |
| --- | --- |
| 首跑 `cargo test --offline --lib` | `**632 / 1 FAILED**（E321 第一处：`set_channel_open_three_way_contradiction` 在 `lan_channel.rs:681` 断言 `!p.clear_direction()` 实为 true；按 `00:9.2` 先单跑留回显，实现零改动）→ 修夹具后复跑仍 **632 / 1 FAILED**（E321 第二处：同一用例 `:692`）→ 第二次修夹具后 **633 / 0**` |
| lib 复跑 3 次 | **633 / 0**（修夹具后复跑 3 次：0.41 s / 0.39 s / 0.39 s，均零 warning） |
| 全量 `cargo test --offline` | `**672 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 23.31 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |

全量 8 段逐项（080 实测，拆三段执行；`src/` 有改动，lifecycle 与 abi 两段独立重跑，按 A112 拆命令不算降验收项）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 633 | 0.41 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 34.75 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 102.11 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **672** | — |

新增 19 个单测（`lan_channel` 19），614 → 633；原 614 个断言一字未改。合计 672 为分段命令求和，**未单条执行** `cargo test --offline`（E306 / A252 口径）。首跑 lib `632 passed; 1 failed; RC=101`（E321 第一处），修夹具后复跑仍 `632 passed; 1 failed; RC=101`（E321 第二处），第二次修夹具后 `633 passed; 0 failed`，再复跑 3 次依次 `633 / 0.41 s`、`633 / 0.39 s`、`633 / 0.39 s`，均零 warning。`Cargo.toml` / `Cargo.lock` / `vendor/` / 既有 14 个 AX 数据层模块 / 判定层模块 / UX HTML / 两语言包 / 56 张 PNG 全部零 diff。

新增 19 个单测（`lan_channel` 19），614 → 633；原 614 个断言一字未改。首跑 `632 passed; 1 failed; RC=101`：`set_channel_open_three_way_contradiction` 在 `lan_channel.rs:681` 断言 `!p.clear_direction()` 实为 true。按 `00:9.2` 先单跑留 FAILED 回显，确认夹具把 Pair 阶段的 `clear_direction()` 误写成应被拒（实现只在 Transfer 阶段拒），属夹具预期错、实现零改动；改夹具并补 8 条断言（清方向后重开通道被拒、重新设方向、进入 Transfer、Transfer 阶段持续锁定等）。修后复跑仍 `632 passed; 1 failed; RC=101`：同一用例 `:692` 把 Transfer 阶段的 `clear_direction()` 写成应成功，第二次按实留回显后改夹具并补 4 条断言（Transfer 持续拒、退回 Pair 后可清），实现仍零改动、断言强度不降（A264 / A180）。第三次 `633 passed; 0 failed`。E321 计入四值「已失败」，不包装成已处理；076 E285 / 078 E302 / 079 E314 同形态重演（E319）。

## 3. 守卫与 CI

**二十八守卫最终全 OK**（A271 开工预检生效，074 的 E275 测试名碰撞未重演）。新守卫 `lan_channel_guard.py` 首版 4 次自检 FAIL 按实修正，**不写成「首跑全绿」**：

| 自检 FAIL | 原因 | 修正 |
| --- | --- | --- |
| `text_bound_not_reused count=1` | A247 要求 prod 段 `robust::MAX_TEXT_BYTES` ≥ 2 处，实现只有 1 处 | 在 `parse()` 的 `direction_raw` 加显式长度校验（真实健壮性检查，非凑数），prod 段第二处使用落地 |
| `enum_parse_not_explicit MessageKind::parse` | 守卫凭印象核四个 `Type::parse` 调用，但 `MessageKind` 只由 `message_kind_for()` 产出、不解析输入（A157 / A261） | 改成核三个 load 侧 `parse` 调用 + 测试段 `MessageKind::parse`  exercised + `pub fn message_kind_for(` 存在 |
| `atomic_write_missing` | `body_after()` 同时接受 `}` 与 `    }`，顶层 `fn write(` 被内部 `if let` 块的 `    }` 截断（A263） | 加 `closer` 参数：顶层函数用 `}`、impl 内方法用 `    }` |
| `H_parse_pair_check_removed` 注入假 OK（E322） | 守卫只核 `fn state_consistent(` 存在与 DEGRADE 标签，未核函数体四处检查（A159 / A243） | 改成解析函数体逐项核 `pair_code.is_empty()` / `direction.is_none()` / `!channel_open` / Close-Discover 分支，H 组重验真 FAIL |

| 守卫 | 输出 |
| --- | --- |
| 062–079 共 27 守卫 | `PANIC_GUARD_OK files 64 hits 0` / `SEMVER_GUARD_OK version_files 8 hits 0` / `I18N_GUARD_OK rs_files 64 hits 0` / `LANG_GUARD_OK` / `POLICY_GUARD_OK` / `P09_HITS 0 []` / `API_GUARD_OK v1_symbols=7 scattered=0` / `POPUP_GUARD_OK specs=13` / `PRIVACY_GUARD_OK` / `AI_GATE_OK` / `AX_GUARD_OK specs=24 gate_only=1 data_layer=15 planned=8` / `SETTINGS_GUARD_OK` / `DOWNLOAD_HISTORY_GUARD_OK` / `EXTENSION_GATE_GUARD_OK` / `LAUNCH_PROGRESS_GUARD_OK` / `DOWNLOAD_SOURCES_GUARD_OK` / `INSTANCE_DROP_GUARD_OK` / `BANNER_DESIGN_GUARD_OK` / `WIDGET_LAYOUT_GUARD_OK` / `APPEARANCE_GUARD_OK` / `FIRST_RUN_GUARD_OK` / `SKIN_DRAFT_GUARD_OK` / `UPGRADE_PLAN_GUARD_OK` / `SEARCH_FILTER_GUARD_OK` / `GENERATOR_SESSION_GUARD_OK` / `SEED_ACCESS_GUARD_OK` / `DELIVERY_GUARD_OK rounds=[56..80]` |
| 080 新增 | `LAN_CHANNEL_GUARD_OK keys=7 kinds=3 stages=4 methods=2 directions=2 transitions=6 field_segments=4 bad_inputs=23 opaque_text expected_tables four_impl_literals_match robust_reused pair_checks_three pure_queries v1_unchanged ax21=DataLayer conflict_empty` |

`PANIC_GUARD files 64` 与 `I18N rs_files 64` 由 63 增至 64（新增 `lan_channel.rs`）；`SEMVER version_files 8` 与 079 相同（本轮测试段未新增 `cmp_precedence` / `semver` 字面量）。`scan` job 由 28 步增至 29 步。CI 三 job 按真实命令拆开跑：`W_RC=1` / `H_RC=1` / `NO_CREDENTIAL`（`git grep` tracked）。67 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 444 项 `MISSING 0`；敏感文件零 diff。

## 4. 双向注入

080 对 `lan_channel_guard.py` / `ax_guard.py` / `api_guard.py` 等做 **18 组**双向注入。按 A263，每组注入前先 `count()==1` 核锚点唯一；全部按原文本回写并校验 SHA-256 一致。**首轮 17 组真 FAIL、1 组假 OK（E322）；修守卫后 H 组重验真 FAIL，最终 18 组全真 FAIL**：

| 注入 | 结果 |
| --- | --- |
| A：删测试段 `use crate::core::settings_io::PROTECTED_FILES;` | `LAN_CHANNEL_GUARD_FAIL protected_table_not_reused` RC=1 |
| B：AX21 `DataLayer` → `Planned` | `LAN_CHANNEL_GUARD_FAIL ax21_state_or_conflict_changed` + `AX_GUARD_FAIL AX21_not_data_layer`，双 RC=1 |
| C：往 `api.rs` 加 `ChannelState` 导出 | `LAN_CHANNEL_GUARD_FAIL v1_surface_expanded` + `API_GUARD_FAIL v1_surface_changed`，双 RC=1 |
| D：`KNOWN_KEYS` 的 `"channel_open"` → `"channel_openz"` | `LAN_CHANNEL_GUARD_FAIL KNOWN_KEYS_values` RC=1（A270 五表逐值比对） |
| E：`TRANSITIONS` 的 `("transfer","close")` → `("transfer","closex")` | `LAN_CHANNEL_GUARD_FAIL TRANSITIONS_values` RC=1 |
| F：`STAGE_FIELDS` 的 `("pair", ...)` → `("pairx", ...)` | `LAN_CHANNEL_GUARD_FAIL STAGE_FIELDS_segments` RC=1 |
| G1：`MessageKind::parse` 的 `"request"` → `"request_x"` | `LAN_CHANNEL_GUARD_FAIL MessageKind_literals_mismatch` RC=1（A269 第一 impl 段） |
| G2：`LinkStage::parse` 的 `"pair"` → `"pair_x"` | `LAN_CHANNEL_GUARD_FAIL LinkStage_literals_mismatch` RC=1 |
| G3：`PairMethod::parse` 的 `"qr"` → `"qr_x"` | `LAN_CHANNEL_GUARD_FAIL PairMethod_literals_mismatch` RC=1 |
| G4：`TransferDirection::parse` 的 `"pc_to_phone"` → `"pc_to_phone_x"` | `LAN_CHANNEL_GUARD_FAIL TransferDirection_literals_mismatch` RC=1 |
| H：**首轮假 OK** `state_consistent` 的 `pair_code.is_empty()` 检查改成 `if false` | 首轮 `LAN_CHANNEL_GUARD_OK RC=0`（E322：守卫只核函数名与 DEGRADE 标签）；修守卫解析函数体逐项核四处检查后重验 `LAN_CHANNEL_GUARD_FAIL parse_pair_check_missing pair_code.is_empty()` RC=1 |
| I：删 `set_stage()` 的 `!self.pair_ready()` 检查 | `LAN_CHANNEL_GUARD_FAIL set_stage_pair_check_missing` RC=1 |
| J：删 `set_channel_open()` 的 `direction.is_none() || !pair_ready()` 检查 | `LAN_CHANNEL_GUARD_FAIL set_channel_open_pair_check_missing` RC=1 |
| K：删 `use crate::core::robust;` import 行 | `LAN_CHANNEL_GUARD_FAIL robust_import_missing` RC=1（A247） |
| L：`can_transition()` 的 `TRANSITIONS.iter().any(...)` 改成 `true` | `LAN_CHANNEL_GUARD_FAIL transition_table_not_queried` RC=1 |
| M：`fs::rename(&tmp, &path)` 改成 `fs::write(&path, body)` | `LAN_CHANNEL_GUARD_FAIL atomic_write_missing` RC=1 |
| N：`change_event()` 的 `Kind::Event` → `Kind::Request` | `LAN_CHANNEL_GUARD_FAIL event_not_unified_envelope` RC=1 |
| O：prod 段插 `use std::net::TcpListener;` | `LAN_CHANNEL_GUARD_FAIL forbidden_literal TcpListener` RC=1 |
| P：`ax_guard.py` 动态求和改成 `planned = 8` | 069 / 070 / 071 / 072 / 073 / 074 / 075 / 076 / 077 / 078 / 079 / 080 十二守卫全 `ax_guard_not_dynamic` RC=1；`ax_guard` 自身 RC=0（被注入对象，符合预期） |

恢复后 6 个关键守卫全 OK（A159 / A187 / A204）。E322 的假 OK 与修复如实登记，不写成「一次全绿」；FAIL 数按实记录，不凑数。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `MESSAGE_KINDS` / `STAGES` / `METHODS` / `DIRECTIONS` | 7 键 / 3 值 / 4 值 / 2 值 / 2 值，五张表用显式 `EXPECTED` 集合逐值比对（A270）；`TRANSITIONS` 6 对、`STAGE_FIELDS` 4 段另逐值比对；未知键整份拒、枚举未知值跳过 |
| 四枚举字面量一致性（A269） | 守卫解析 `impl MessageKind` / `impl LinkStage` / `impl PairMethod` / `impl TransferDirection` **四个** impl 段，各自 `=> "X"` 与 `"X" =>` 两组字面量与对应常量表逐值比对 |
| 既有文本上限复用（A247） | `use crate::core::robust;` 显式 import + `robust::MAX_TEXT_BYTES` ≥ 2 处使用 + `robust::read_or_default(&path, DEFAULT_STATE)`；删 import 行真 FAIL |
| 不透明字符串 | `prod` 段无 `cmp_precedence` / `semver` / `Version::parse` / `url` / `token` / `uuid` / `png` / `texture` / `minecraft:` / `give ` / `regex` / `glob` / `AIProvider` / `WikiEntries` / `§` / `TcpListener` / `TcpStream` / `bind(` / `127.0.0.1` / `SystemTime` / `UNIX_EPOCH`（A30 / `00:26` / `11:18` / `11:19`）；房间号 / 连接码 / 字段值只校验长度与控制字符 |
| 矛盾态三处拒收 | `parse()` 段 `bad_pair_without_code` / `bad_transfer_without_direction` / `bad_close_with_open_channel` 与 `set_stage()` / `set_channel_open()` 段三处一致 |
| 阶段转移表 | `TRANSITIONS` 六对逐字核对；`can_transition()` 纯查表，不合表跳段拒收 |
| 八个派生纯查询 | `can_transition()` / `stage_fields()` / `next_stages()` / `message_kind_for()` / `field_allowed()` / `pair_ready()` / `channel_usable()` / `summary()` 段内无 `fs::` |
| 单条突变 | 守卫核 `set_stage` / `set_method` / `set_direction` / `set_pair_code` / `set_room_id` / `set_channel_open` 六个单条入口；`prod` 段无 `for_all` / `confirm_all` 批量入口 |
| 布尔与档位双向边界 | `LinkStage::parse` / `PairMethod::parse` / `TransferDirection::parse` / `MessageKind::parse`（load）与 `LinkStage::parse` / `PairMethod::parse` / `TransferDirection::parse`（load）与 `can_transition` / `METHODS.contains` / `DIRECTIONS.contains`（set）双向生效；`MessageKind` 不解析输入，只由 `message_kind_for()` 产出，`parse` 在测试段核；两条配对路径都落，执行不落（A250） |
| 23 类 load 坏输入 + 突变拒收 | 根级 12 类 + 枚举级 8 类 + 字段级 6 类 + 矛盾态 4 类 |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `stage` / `method` / `direction` / `room_id` / `pair_code` / `channel_open` 七键 |
| `DEFAULT_STATE` 逐字不变 | 测试 `default_state_literal_is_unchanged` 断言整串与 7 键（A175） |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `lan_channel` 引用 |
| AX21 `conflict` | 保持空，24 条 spec 唯一 |
| 既有 14 个 AX 数据层模块 / `dispatcher` / `popup` / `stats` / `consent` / `feature_gate` / `region` / `client_ai` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / `unwrap_or` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.lan_channel`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| A271 预检 | 开工实跑全仓 `*_guard.py` 禁用字面量表并核扫描范围，测试名首版避开 `catalog()`、源码全英文避开 `i18n_guard`、prod 段不写端点与凭据连续串；首跑 `API_GUARD_OK` / `I18N_GUARD_OK`，074 E275 未重演 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过（E321 / E322 按实留痕） | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 已失败；EQ / Q / 8 项 `Planned` 未证实；真实连接与 UI 未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 9.0，满足 | — |
| 连续十一轮未达通过 | 069–079 连续未通过，按 `00:9.1` 应停下；用户 080「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-080-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、079 远端补验、四份原文全文回显、A248 / A266 预检、A201 / A211 / A250 / A259 / A267 / A271 复核、AX21 数据层、**633 / 0**（修夹具后复跑 3 次：0.41 s / 0.39 s / 0.39 s，均零 warning）、二十八守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322；035–047 历史格式缺失 |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、EQ-01 ~ EQ-13、4 条 Q-C、8 项 `Planned`、6 项低可信度转述 |
| 未启动 | 真实连接建立、文件传输执行、二维码生成、连接码算法、房间密码校验、FCL 互通、第二家联机服务端点、版本一致性判定、境外判定执行、协议 UI、生成器算法、NBT 读取、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载、zip / 投影解析 |
| 受阻 | 无（远端 Git Data API 通道正常；8 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## 080 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `33776623023f443e6fe1fd4fb1d59b1fa832d1ac`（增量 tree `2449352`，19 个变化 blob，`force=false`） |
| 本地主快照 | `c89959f` |
| 远端父提交（推送前只读核） | `3e80108`（079 补记） |
| 主快照逐项比对 | `LOCAL 1219 / REMOTE 1219 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 主包 / 预览包 | 1219 / 57 项，EXTRA 0 / MISSING 0 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| `.git/index.lock` | 提交前核无残留、无运行中 git 进程（A254 / A140），提交 RC=0 |
| 独立验证结论 | 仍「部分通过 / 未通过」，未发通过标记；交付层已闭环，已失败 / 未证实 / 未启动项不变 |

本轮无新增防错项：A271 开工预检生效，28 守卫最终全绿、18 组注入最终全真 FAIL，`00:207` 不凑条目，防错清单零改动。首跑 2 次 FAILED（E321）与双向注入首轮 1 组假 OK（E322）按 `00:9.2` / A159 留痕并计入四值「已失败」，历史回复不重写（A181）。076 E285 / 078 E302 / 079 E314 同形态重演（E319），如实登记。

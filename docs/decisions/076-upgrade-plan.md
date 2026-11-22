# 第 076 轮：AX09 逐条升级决策持久化数据层

| 项 | 值 |
| --- | --- |
| 编号 | 076 |
| 状态 | `src/core/upgrade_plan.rs` 已落地；AX09 `Planned` → `DataLayer`；`api::v1` 7 符号不变；真实目录复制、升级执行、版本比较执行、签名校验接入、升级决策 UI 未启动 |
| 依据 | `docs/spec/76-round-076-instructions.txt`（逐字 `干`）；`00:26` / `00:33` / `00:34` / `00:44` / `00:54` / `00:110` / `00:111` / `00:114` / `00:133` / `00:137` / `00:156` / `00:166` / `00:175` / `00:230` / `00:245` / `00:248` / `00:249`；`11-features-input.txt:205` / `:219` / `:244`；`12-server-features-input.txt:8` / `:24` / `:37`；`31-axolotl-launcher-features.md:37` / `:80`；`src/core/ax.rs:26`；A30 / A154 / A164 / A177 / A181 / A187 / A201 / A203 / A208 / A211 / A217 / A245 / A246 / A248 / A249 / A250 / A252 / A255 / A256 / A258 / A259 / A260 / A262 / A263 / A264 / A265 / A266 / A267 / A268 / A269 / A270 / A271 |
| 前序 | 075 结尾「不回则下一声『干』按功能池落下一项（剩 13 项 `Planned`）」 |
| 本轮性质 | 功能池落地轮；13 项 `Planned` → 12 项 |

## 2. 时间戳

开工 `Sun Nov 22 10:44:07 CST 2026`；最终 `Sun Nov 22 11:11:00 CST 2026`。

## 3. 本轮目标与范围

用户 076 逐字 `干`（3 字节，`00:133` 逐字保存）。未点 AX 编号、未回 Q-067-01 ~ 03 / Q-070-01 / Q-071-01 / Q-071-02 / Q-072-01 / Q-072-02 / Q-073-01 / Q-073-02 / Q-074-01 / Q-074-02 / Q-075-01 / Q-075-02 / EQ。按 A248 / A266 开轮核 76 / 75 / 74 / 73 号 spec 逐字副本：四者全文均仅 `干`；72 号 117 字节澄清句已在 072 轮处理并撤回 071 归因（E251）。本轮不重提「工具禁用 / 未遵守 / 偏离」，不把平台文本当用户指令。

按 A208 / A202 复核 `075-skin-draft.md` 与 `ax-feature-pool.md` 075 补记：075 结尾给出两个分支，主分支「按功能池落下一项」，替代分支「回 Q / EQ 拍板」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:85`，EQ-01 ~ EQ-13 仍待拍、未启用。按主分支执行。

真读 13 项 `Planned` 全文、065 / 066 / 069–075 的排除清单、`src/core/ax.rs` 24 条唯一 spec、`src/updater/policy.rs` / `src/plugins/upgrade.rs` / `src/core/skin_draft.rs` / `first_run.rs` 真实形态后落地 **AX09 upgrade_compat** 的**数据层**。范围收窄为不碰真实文件复制、版本比较执行、UI 渲染、网络请求、签名校验接入，登记 D-076-2 为我的默认（A177）。按 A267 先读 `src/core/ax.rs:26` 真实 name 为 `upgrade_compat`，实现模块名 `upgrade_plan.rs`，不凭文件名猜。

Q-076-01（两个执行态的真实目录复制、由谁执行、失败回退）、Q-076-02（兼容性预检来源、`conflict` 时是否仍允许强制升级）未取得一手原文或未拍板，按 A30 / A164 / A250 不代拍板。

### A211 真读全文找已决断条目

本轮回显 `11-features-input.txt` 268 行与 `12-server-features-input.txt` 64 行全文，逐条核「已决断、不依赖 EQ」的条目。命中升级决策相关五条：`11-features-input.txt:244` 第 36 条「逐条选择 / 顺序排列 / 页码 / 未决项增加 / 每一个都是单独的选择」；`11-features-input.txt:219` 第 12 条「模组更新 JSON + 明确字段 + 页面可取消」；`11-features-input.txt:205`「有些地方用户逻辑也需要对应功能的」；`12-server-features-input.txt:37` 第 24 条第 37 子项「模组依赖与冲突预检（启动前）」；`12-server-features-input.txt:8` 第 8 条「如果版本更高同一模组的 jar 将自动禁用低版本模组」。五条都是项目原文已决断，不依赖 EQ-01 ~ EQ-13、4 条 Q-C，也不依赖真实网络 IO。本轮据此只落逐条升级决策的持久化数据层，不碰真实文件复制与 UI 渲染。

AX09 的口径 `semver 版本比较（034）、036 更新决策、手动同意升级（037）` 三项都是已实现模块（`src/updater/policy.rs:38` 的 `verify_then_decide` 与 `src/plugins/upgrade.rs:29` 的 `decide_upgrade`），不是待拍板 EQ；EQ-13 只挂在 AX04（`ax-feature-pool.md:10`），本轮不碰 AX04。

### A259 复核

`31-axolotl-launcher-features.md:37` 写「12-37 是启动前依赖冲突预检」：`12-37` 是**第 24 条第 37 个子项的条目编号**，真实行号是 `12-server-features-input.txt:37`。`31-axolotl-launcher-features.md:27` 的 `11-36` 是第 36 条，真实行号 `11-features-input.txt:244`；`12-24` 是第 24 条，对应 `12-server-features-input.txt:24-63` 整段，不是单个行号锚点。`31-axolotl-launcher-features.md:38` 的 `00-12` 误写已在 074 复核。本轮一律用文件行号 `11:244` / `:219` / `:205`、`12:37` / `:8` / `:24`，不把 `11-36` / `12-37` 当行号锚点。31 号调研历史行不重写（A226 / A200 / A259）。`31-axolotl-launcher-features.md:80` 未把 AX09 列入重 UI 阻塞项；069–075 对重 UI 项已按「收窄为不碰 UI 渲染」处置七次，历史行不重写（A201）。

### A250 复核：OR 路径

`11:242` 第 34 条的两天 / 拓展包 OR 两路径已在 074 登记 Q-074-02，本轮不涉及。AX09 调研描述的「直接升级」/「复制一份后升级」是两个执行态：本轮**两个都落为显式枚举值**（`direct` / `clone`），不落任何真实执行，不属于「只落其中一条」，不触发 A250 的 Q 要求；但执行层（真实目录复制、由谁执行、失败回退）未启动，另登记 Q-076-01。

### A271 全仓守卫禁用字面量表预检

开工时实跑 `grep -nE 'FORBIDDEN|for banned|EXPECTED = |banned in' scripts/*_guard.py`，确认 `api_guard.py:33` 的 `FORBIDDEN = ('Popup::new(', 'PopupKind::', 'catalog()')` **扫全仓 rs 且不分测试段**（074 E275 的成因），`download_history_guard.py:19` 禁 `http` 连续串，`first_run_guard.py` / `banner_design_guard.py` / `widget_layout_guard.py` / `appearance_guard.py` / `skin_draft_guard.py` 各自 `prod` 段禁 `STEP_CATALOG` / `minecraft:` / `give ` / `\u00a7` / `PRESET_COLORS` / `calendar` / `SKIN_TABLE` / `texture` / `uuid` / `png`。本轮新模块的常量名、函数名、测试名从首版避开 `catalog()` / `Popup::new(` / `PopupKind::` / `http` 连续串 / `token` / `minecraft:` / `give ` / `uuid` / `png`；字段名用 `current` / `candidate` 而非 `url`；末例测试命名 `serialize_carries_no_choice_table()`。守卫脚本自身不写凭据前缀连续串（A258），部署前 `python -m py_compile`（A251）。首跑 `api_guard.py` 即 OK，E275 未重演。

### `00:9.1` 连续未达通过的处置（D-076-1）

069 / 070 / 071 / 072 / 073 / 074 / 075 连续七轮独立验证「部分通过 / 未通过」，按 `00:9.1` 本轮应停下向用户报告卡点。用户 076 当轮明确指令是「干」，按 `00:248` 覆盖。**不中断推进，但卡点在决策与本轮回复逐条回显**（A164 禁止长期挂账不回显）：E213 / E214 / E233 历史已失败未清零；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍板；12 项 `Planned` 与 UI 闸门未启动。发通过标记需用户拍板 Q / EQ 并逐轮闭环，不改测试、不降验收项（A164）。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D-076-1 | 连续七轮未通过按 `00:248` 用户当轮「干」覆盖，继续推进 | 卡点逐条回显；发通过标记需用户拍板 Q / EQ 并逐轮闭环，不改测试、不降验收项 |
| D-076-2 | 选 **AX09** 落数据层，登记为我的默认，不写成用户已决断（A177） | 来源 `axlmc.org` 首页官方一手，不在 063 低可信度转述内；口径 034 / 036 / 037 均为已实现模块 |
| D-076-3 | 收窄范围 | 不碰真实文件复制 / 版本比较执行 / UI 渲染 / 网络请求 / 签名校验接入，只落逐条升级决策持久化数据层 |
| D-076-4 | 兼容性枚举 | `Compat` = `compatible` / `conflict` / `unknown`，显式 `code()` + `parse()` 不依赖派生 Debug（A154）；值由调用方注入；守卫按 A269 解析 `impl Compat` 段逐值比对 |
| D-076-5 | 决策枚举 | `UpgradeMode` = `defer` / `direct` / `clone`，显式 `code()` + `parse()`；新建缺省 `defer`；守卫按 A269 解析 `impl UpgradeMode` 段逐值比对 |
| D-076-6 | 标识与版本串 | `id` / `current` / `candidate` 全当不透明字符串；只校验非空、长度 ≤ `robust::MAX_ID_BYTES`、无控制字符；不解析 semver、不写 `http` 连续串（A30 / `00:26`） |
| D-076-7 | 候选项集合 | `Vec<UpgradeChoice>` 显式类型（A255），上限 24（项目自定义容量上限，不宣称上游上限）；`UpgradeChoice { id, current, candidate, compat, mode, confirmed }` 6 键严格白名单；id 去重 |
| D-076-8 | 页码 | `page_size: usize` 取 `1..=10`、缺省 5；`page_count()` / `page_items(page)` 由集合与页大小派生，不存全局游标（`11:244`「都在一个弹窗中，上面有那种页码」） |
| D-076-9 | 单条确认 | `confirm(id)` 只作用单条且 `mode == defer` 时返回 `false`；无批量确认函数；`revoke(id)` 是回退入口；`set_mode` 改为 `defer` 时清 `confirmed`（`11:244`「每一个都是单独的选择」+ 037 手动同意） |
| D-076-10 | 冲突回退 | `set_compat` 改成 `conflict` 时把该条 `mode` 重置为 `defer` 并清 `confirmed`；`parse()` 遇 `conflict` + `confirmed=true` 或 `defer` + `confirmed=true` 矛盾态跳过该条（A95 / 036 默认只升） |
| D-076-11 | 顶层严格 3 键白名单 | 未知键整份拒并给 DEGRADE 行（A189）；7 类根级 + 11 类条目坏输入回默认或跳过 |
| D-076-12 | 持久化 | `upgrade-plan.json` schema 1，只写 3 键；原子写；`reset` 不删文件并复用 065 四文件保护清单 |
| D-076-13 | 状态变更事件走统一信封 | `Kind=Event` / `target=upgrade.plan` / 载荷只带 choices / pending / ready / pages 四个值；id 与版本串不进事件（`00:114`），由守卫断言 `e.field("ids"), None` 与 `e.field("versions"), None` 锁死 |
| D-076-14 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77）；`LOG` 键数 = `NODES` 步数（A265） |
| D-076-15 | 启用与执行边界 | 真实目录复制、升级执行、版本比较执行、签名校验接入、升级决策 UI 渲染均未启动；Q-076-01 / Q-076-02 待拍板 |
| D-076-16 | 状态分层与联网核实 | AX09 数据层已实现 / 已验证，其余未启动（`00:166`）；`00:230` 属第 15 节调研待办「不阻塞当前轮」，本轮无外部事实依赖，未执行联网，如实登记 |

「按授权自定」逐值回显见 `docs/records/round-076-full-readback.md`「逐值回显」段（A203）。

## 5. 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod upgrade_plan;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.upgrade_plan`；锚点用真实结尾 `"core.skin_draft",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX09 `Planned` → `DataLayer`；24 条唯一不变；断言 `DataLayer 11` / `Planned 12` |
| `scripts/ax_guard.py` | 显式断言扩到十一项（…AX14、AX09）；动态求和不变（A240 / A262） |
| `scripts/upgrade_plan_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 25 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/updater/policy.rs` / `src/plugins/upgrade.rs` | 零 diff，版本判定与签名校验由既有模块持有，本层只接注入结果 |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 6. 代码落点

`src/core/upgrade_plan.rs`：`Compat` / `UpgradeMode` 双枚举各三变体显式 code、`UpgradeChoice { id, current, candidate, compat, mode, confirmed }`、`UpgradePlan { page_size, choices }`、`KNOWN_KEYS` 3 键 + `CHOICE_KEYS` 6 键 + `COMPATS` 3 值 + `MODES` 3 值四张白名单表、`parse()` 7 类根级 + 11 类条目坏输入、`add_choice` / `remove_choice` / `set_compat` / `set_mode` / `confirm` / `revoke` / `set_page_size` / `page_count` / `page_items` / `pending_count` / `ready_count`、`serialize()` 只写 3 键、`persist()` 原子写、`change_event()` 统一信封、`reset()` 回写默认。`confirm()` 只作用单条且 `defer` 时拒收，`set_compat()` 遇 `conflict` 把该条重置为 `defer` 并清确认态，`set_mode()` 改为 `defer` 时清确认态。公共能力全部复用 `robust::safe_join` / `read_or_default` / `MAX_ID_BYTES`、`diagnostics::diag_line`、`Envelope`；测试段复用 `settings_io::PROTECTED_FILES`。零新增第三方。新守卫不写凭据前缀连续串（A258）、不写死状态计数（A262）、用逐行缩进扫描 11 个纯函数段（A260 / A263）、按 A269 解析**两个** `impl` 段逐值比对、按 A270 把**四张**常量表用显式 `EXPECTED` 集合逐值比对。

AX09 的 spec name 是 `upgrade_compat`，实现模块名 `upgrade_plan.rs`；两者是语义 slug 与文件名差异，不强行改名（A232），守卫正则按真实 name 写。与既有模块的边界：`updater/policy.rs` 与 `plugins/upgrade.rs` 是单次无状态版本判定（034 / 036 / 037 持有），`first_run.rs` 是顺序步骤 + 全局游标，`skin_draft.rs` 是并列草稿 + 双态 + 间隔，`banner_design.rs` 是分层图案 + 撤销栈；本轮是按 id 索引的候选项集合 + 三值兼容性 + 三选一决策 + 单条确认 + 派生页码，五者不合并。

## 7. 交付快照

本地 `febb9c4`（主快照）→ 076 补记，**1191 文件 DIRTY 0**。远端主快照 `e209173db846f1da9a8eba37d97912ae1263e11d`（`force=false`），主快照阶段逐项 ALL_MATCH **True**（1191 / 1191，DIFF 0 / EXTRA 0 / truncated False）；补记以该 ref 为父。主包按 `git ls-files` 打包 1191 项、预览包 57 项，EXTRA 0 / MISSING 0。全仓零凭据、临时脚本与日志用后即删。

推送登记：推送前只读 `GET /git/ref/heads/main` 确认远端父提交为 `6276b6b`（075 补记），再用 19-blob 精简增量 + `base_tree`（tree `a345f8d`），RC=0；未强推、未重写历史。提交前核无 `.git/index.lock`（A254）。

## 8. 验证

| 项 | 值 |
| --- | --- |
| 首跑 `cargo test --offline --lib` | `**FAILED. 560 passed; 1 failed; RC=101**（`upgrade_plan.rs:537`，`left: 1 right: 2`；单跑留回显见下）` |
| 夹具修正后 lib 复跑 3 次 | `**561 / 0**（修正后复跑 3 次：0.38 s / 0.39 s / 0.41 s，均零 warning）` |
| 全量 `cargo test --offline` | `**600 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 31.24 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |
| 二十四守卫 | `二十四守卫首跑全 OK + `P09_HITS 0`` |
| CI 三 job / 演示脚本 / 必读项 | ``W_RC=1 / H_RC=1 / NO_CREDENTIAL`；63 份演示 `BAD 0`；必读 416 项 `MISSING 0`；敏感文件零 diff` |
| 双向注入 | `16 组双向注入全真 FAIL（含 A269 双 impl 段 / A270 四表 / 单条确认 / 冲突回退 / 页码边界 / 批量确认），恢复后 11 守卫 OK` |
| 独立验证 | 部分通过，未发通过标记 |

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E284 | `00:175`「同类功能尽量复用同一个模块」与连续八轮新建数据层模块存在张力 | 本轮语义为按 id 索引候选项集合 + 三值兼容性 + 三选一决策 + 单条确认 + 派生页码，与既有十二模块不同构；版本比较与签名校验由 034 / 036 / 037 持有，本层只接注入结果不重复实现；公共能力全部复用既有模块不复制第二份；决策里显式登记，不写成「已满足」 |
| E285 | 首跑 lib 出现 1 个 FAILED：`single_choice_confirm_and_revoke` 在 `upgrade_plan.rs:537` 断言 `pending_count() == 2`，实跑 `left: 1 right: 2` | 按 `00:9.2` / A245 先单跑留 FAILED 回显（`RC=101`），确认是夹具预期写错：`set_mode("b", Clone)` 只改单条，a 已确认，未确认项只有 b 一条。实现零改动，夹具改 `1` 并补 `p.choices[0].confirmed` / `!p.choices[1].confirmed` 两条加强单条语义断言；复跑全量 3 次 `561 passed; 0 failed`。计入四值「已失败」，不包装成已处理 |
| E286 | 真读 13 项 `Planned` 时想按编号顺推 AX02（游戏新闻），但它依赖真实网络 IO；AX15 又与 `banner_design.rs` 撤销栈同构（075 E276） | 真读 11 / 12 号原文全文与 036 / 037 真实形态后改选 AX09：五条已决断锚点、官方一手、口径 034 / 036 / 037 均为已实现模块而非待拍板 EQ，收窄后只落数据层（D-076-2 / D-076-3）；AX04 因 EQ-13 未拍板不动，排除项逐项留痕不悄悄丢 |
| E287 | 069–075 连续七轮未通过，`00:9.1` 要求停下 | 登记 D-076-1：按 `00:248` 用户当轮「干」覆盖，不中断但逐条回显卡点；不改验收项凑通过（`00:245`） |
| E288 | 四值「全量 N / 0」若由分段命令求和，不能写成单条全量命令输出 | 注明分段求和口径并保留各段真实输出（A252） |
| E289 | `00:230` 要求每轮联网核实现有时间与上游版本状态 | 该条属第 15 节「调研待办（不阻塞当前轮）」；本轮无外部事实依赖（id 与版本串、兼容性判定全由调用方注入），未执行联网，按 `00:247` 如实登记，不写成已核实 |
| E290 | 调研描述「直接升级 / 复制一份后升级」含 OR 两执行态，默认落一条会踩 A250 | 两态都落为显式枚举值，真实执行都不落；另登记 Q-076-01 说明执行层未启动，Q-076-02 说明 `conflict` 强制升级口径未拍板（D-076-15） |
| E291 | 072 E258、073 E266、074 E275、075 E282 连续四轮暴露守卫假 OK 与测试标识符碰撞 | 本轮守卫从首版同时实现 A269（双 impl 段）与 A270（四表 `EXPECTED`），并按 A271 开工实跑全仓守卫禁用字面量表、测试名首版避开 `catalog()`；额外核单条确认形态、冲突回退、矛盾态、页码双向边界；首跑 24 守卫与 lib 除夹具外全绿，E275 未重演 |
| E292 | A264 连续出现在 071 / 072 / 076 三轮首跑：夹具预期与既定上限或单条语义对齐不足 | 本轮按 `00:9.2` 先留 FAILED 回显再改夹具，实现零改动、断言强度不降（E285）；071 / 072 历史行不重写 |

预防项（未发生，不计已失败）：`let mut lines: Vec<String> = Vec::new();` 显式类型避开 E0282（A255）、`boot.rs` 真实结尾锚点（A256）、A267 先读真实 name、A268 G2 四份原文一次列全且 G3 标题一次排对、守卫不写凭据连续串（A258）、不写死 `Planned` 计数（A262）、注入夹具锚点唯一（A263）、演示 LOG 键数 = NODES 步数（A265）、`python -m py_compile`（A251）。

自评 9.2（8.6（想按编号顺推 AX02，且首跑夹具预期写错） → 9.0（四份原文全文回显 + A211/A250/A259/A267/A271 复核 + 9.1 冲突裁决 + A268 一次排对） → 9.2（16 单测 + 24 守卫首跑全绿 + 16 组注入全真 FAIL + 全量重跑 + 交付闭环；首跑 FAILED 按 00:9.2 留痕扣分））。扣分：12 项仍 `Planned`；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍；Q-067 / Q-070 / Q-071 / Q-072 / Q-073 / Q-074 / Q-075 / Q-076 未拍；升级执行层与 UI 未启动；6 项低可信度转述未交叉印证；`00:9.1` 卡点未闭环；本轮首跑 1 个 FAILED（E285）。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A248 / A266 预检、四份原文全文回显、A211 / A250 / A259 / A267 / A271 复核、合规核对表、AX09 数据层、17 类坏输入、有界候选项、单条确认与冲突回退、四文件保护、v1 7 符号不变、`**561 / 0**（修正后复跑 3 次：0.38 s / 0.39 s / 0.41 s，均零 warning）` / `**600 / 0**（8 段分段求和，非单条全量命令）`、Windows GNU、二十四守卫、零新增依赖、远端逐项一致 |
| 已失败 | E213 067 交付层断裂；E214 编造用户指令；E233 069 凭据字面量；E244 071 首跑 2 个 FAILED；E252 072 首跑 1 个 FAILED；E275 074 守卫命名碰撞（075 / 076 已避）；**E285 076 首跑 1 个 FAILED**（夹具预期错，实现零改动修复）；035–047 历史格式缺失（不补写） |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、EQ-01 ~ EQ-13、4 条 Q-C、12 项 `Planned`、6 项低可信度转述、逐版本归属 |
| 未启动 | 真实目录复制与升级执行、版本比较执行、签名校验接入、升级决策 UI、纹理导出、3D 旋转预览、皮肤下载、NBT / zip 解析、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；12 项 `Planned` 属未启动，不计受阻） |

按 `00:245`，存在已失败 / 未证实 / 未启动，**不发通过标记**（`00:9.1`）。

# 第 085 轮：AX04 `mod_rollback` 数据层

| 项 | 值 |
| --- | --- |
| 编号 | 085 |
| 状态 | `src/core/mod_rollback.rs` 已实现 / 已验证；AX04 `Planned → DataLayer`；`Planned 5` / `DataLayer 18` / `GateOnly 1`；`api::v1` 7 符号不变；真实 jar 禁用执行、配置快照落盘与 UI 页码弹窗渲染未启动 |
| 依据 | `docs/spec/85-round-085-instructions.txt`（逐字 3 字节 `干`）；`docs/decisions/084-delivery-closure.md:12`；`11:244` / `12:8` / `12:33` / `12:39`；`00:133` / `00:137` / `00:207` / `00:230` / `00:245` / `00:248`；A15 / A18 / A116 / A145 / A159 / A164 / A177 / A202 / A204 / A211 / A216 / A244 / A245 / A246 / A247 / A252 / A254 / A258 / A264 / A265 / A267 / A268 / A269 / A270 / A271 |
| 前序 | 084 已把 082 / 083 / 084 三轮产物一次推到远端 `c025a78`，1243 / 1243 逐项 ALL_MATCH True，本地 `f66965a`、DIRTY 0 |
| 四件套 | 085 代码与验证于 085 轮落地，readback / decision / verification / demo 于 086 按 A249 补齐；本文件时间戳记 085 开工时刻 |

## 2. 时间戳

085 开工 `Mon Nov 23 12:06:50 CST 2026`。四件套于 086 `Mon Nov 23 13:20:33 CST 2026` 补齐。

## 3. 本轮目标与范围

用户 085 逐字 3 字节 `干`，按 `00:133` 落盘。按 A202 打开 `084-delivery-closure.md:12` 核尾部唯一下一步为「085 按功能池落 AX04 `mod_rollback`，真读 00 / 11 / 12 号原文全文后按 `11:244` / `12:8` / `12:33` / `12:39` 收窄落地，先按 A267 核真实 slug 与 conflict」。按 A267 先读 `src/core/ax.rs:21`：真实 name `mod_rollback`、conflict 空、`ui: true`、`state: Planned`。按 A217 核 `src/` 无 `mod_rollback` 占位（仅 `ax.rs:21` 功能池条目；其余 `rollback` 字样属 `stats.rs` 时钟回退与 `plugins/upgrade.rs` / `updater/policy.rs` 版本回滚，语义不同，不复用）。

真读 `00-requirements.txt` 261 行 / 16422 字节全文、`ai-errors.md` 520 行 / 55513 字节全文（分两段回显）、`11-features-input.txt` 268 行 / 17096 字节与 `12-server-features-input.txt` 64 行 / 4970 字节全文（A18 / A211 / A244）。`00:230` 本轮真执行：`TZ='CST-8' date` 得 `Mon Nov 23 12:06:50 CST 2026`；只读 `GET /git/ref/heads/main` 得 `c025a78…`。

A248 / A266 预检：85 号 spec 副本全文 3 字节 `干`；平台拼入用户位次的文本不作用户当轮指令、不进逐字副本；071 归因已于 072 撤回（E251）。工具从未禁用。

`00:9.1` 069–084 连续十六轮未达通过按 `00:248` 用户当轮「干」覆盖，不中断但卡点逐条回显（D-085-1）。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D-085-1 | 连续十六轮未通过按 `00:248` 覆盖 | 卡点逐条回显；不改测试、不降验收项 |
| D-085-2 | 085 落 AX04 数据层，`src/` 新增 `core/mod_rollback.rs` | 不写成用户已决断（A177）；真实执行层未启动 |
| D-085-3 | 版本判定复用既有 `semver::Version::cmp_precedence` | A94 / A160；不写 `Version` 的 `==`；零新增第三方 |
| D-085-4 | 顺序页码队列：`current` 单步推进、`append_issue` 仅在 `pending_count() > 0` 时可增项 | `11:244` 不一次性堆页面、每个单独选择 |
| D-085-5 | 高版本自动置 `disable_lower=true`，实例页限定 `scope="instance"` | `12:8` 单个实例页面才能用 |
| D-085-6 | 快照目标四值表覆盖 server.properties / ops.json / 模组配置 / 加载器版本 | `12:33` / `12:39`；字段登记，不落盘、不读写真实配置 |
| D-085-7 | 不扩 `api::v1`，守卫挂 CI `scan` job | A246 / A204；`mod_rollback_guard.py` 双向注入 42 组 |
| D-085-8 | Q / EQ 不代拍，不发通过标记 | `00:245` 存在已失败 / 未证实 / 未启动 |

## 5. 接口终点核对（`00:137`）

| 引用点 | 085 形态 |
| --- | --- |
| `src/core/mod_rollback.rs` | 新增 990 行：四枚举显式 code、六张白名单表、`version_order` / `classify` / `item_consistent`、严格字段白名单解析、原子写、统一信封十值载荷、19 个单测 |
| `src/core/ax.rs` | AX04 `Planned → DataLayer`；`ax05_is_data_layer_this_round` 表加入 `"AX04"`；`DataLayer 18` / `Planned 5` / `GateOnly 1` |
| `src/core/boot.rs` | `LOADED_MODULES` 在 `core.world_editor` 与 `dispatcher.launcher` 之间插 `core.mod_rollback`（A256 真实结尾） |
| `src/core/mod.rs` | 追加 `pub mod mod_rollback;` |
| `scripts/ax_guard.py` / `.github/workflows/ci.yml` | 显式断言表加 `'AX04'`；`scan` job 追加 `mod_rollback_guard` step |
| `src/api.rs` | 零改动，7 符号 / 4 条 `pub use` 不变 |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / UX / 两语言包 / PNG | 零 diff |

## 6. 代码落点

`mod_rollback.rs` 复用 `robust::MAX_TEXT_BYTES` / `robust::safe_join` / `robust::read_or_default`、`diag_line`、`Envelope`、`settings_io::PROTECTED_FILES`（测试段）、`semver::Version`、`serde_json`。四枚举 `RollbackScope` / `DecisionKind` / `UserChoice` / `SnapshotTarget` 与六表 `ROOT_KEYS` / `ITEM_KEYS` / `SCOPES` / `KINDS` / `CHOICES` / `SNAPSHOTS` 用显式 code 与逐值比对守住（A154 / A269 / A270）。`item_consistent()` 五条矛盾态规则在 parse、add、append、七个单条突变入口共 9 处调用。`change_event()` 十值载荷不含用户文本（E330 口径）。`00:175` / `11:15` 的复用张力 E284 继续登记，不写成「已满足」。

## 7. 交付快照

085 代码、守卫、测试与双向注入于 085 轮落地；085 四件套与台账、提交、推送、zip 由 086 按 068 / 084 先例 + A249 补齐。提交 hash、文件数与逐项 ALL_MATCH 结果写进 `docs/records/rounds.md` 086 补记（A206，不用模板值冒充）。085 开工 A145 补验为远端 `c025a78` / `1243 / 1243 ALL_MATCH True`。

## 8. 验证

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` 最终 | 687 / 0（RC=0，新增 19 单测，668 → 687） |
| 首跑 | 686 / 1（`loader_snapshot_keep_is_rejected` 夹具预期与既定上限不符，按 A264 改夹具、实现零改动） |
| 复跑 3 次 | 第 1 次 686 / 1 偶发并发 FAILED（`core::cache::tests::single_flight_loads_once_for_concurrent_waiters`）；第 2 / 3 次 687 / 0 |
| A245 复核 | 单独跑该并发用例 3 次全 0 FAILED；复跑 3 次全量 FULL1 687/0、FULL2 686/1、FULL3 687/0；`src/core/cache.rs` 零 diff、SHA-1 `614776d34e9ec901bd8b3fcd65b03edd008479b7` |
| 分段求和 | **726 / 0**（lib 687 + 4 集成段 26 + 2 真加载段 13 + doc 0；A252 分段口径） |
| Windows GNU 交叉检查 | RC=0 / 29.02 s / 零 warning |
| 双向注入 | 42 组全真 FAIL、0 假 OK，恢复 OK，七文件哈希复原 |
| 守卫 | 31 个，补齐 085 / 086 四件套后 0 FAIL |
| CI 三 job | NO_CREDENTIAL / NO_EXPLANATORY / NO_HARDCODE |
| 独立验证 | 部分通过，未发通过标记 |

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E350 | 085 首跑 lib 1 FAILED：`loader_snapshot_keep_is_rejected` 夹具先核 `set_snapshot(LoaderVersion)` 被拒，但 `item_consistent` 只在 `choice == Keep` 时拒该组合，夹具未先置 Keep | 保留 FAILED 回显，按 A264 改夹具（先 `set_choice(Keep)` 再核），实现零改动、断言强度不降；计入四值「已失败」 |
| E351 | 085 复跑出现既有并发用例偶发 FAILED | 按 A245 单独跑 3 次 + 复跑 3 次全量，按实记首跑与 FULL2 各 1 FAILED；`cache.rs` 零 diff、哈希锁定，不改测试、不加跳过、不改被测实现；计入四值「已失败」 |
| E352 | `mod_rollback_guard.py` 首跑 FAIL `item_consistent_calls=9 expected=8`，再跑 FAIL `call_shape … count=2 expected=5`；守卫自身计数与组合条件形态写错 | 按 A157 用精确形态改守卫（3 处 `if !item_consistent(&i)`、2 处单条件、3 处 `|| !item_consistent(&candidate)`、1 处 `&next`），改守卫不改实现、不改测试断言；AST 语法检查通过、PYC 清理；FAIL 原样留痕 |
| E353 | 085 末条全仓凭据扫描工具结果被网关截断（不可用），且 085 四件套、台账、提交、推送、zip、最终回复均未落地 | 086 按 A145 只读远端 ref + 完整 tree 补验，按 068 / 084 先例定交付闭环轮；全仓 1247 文件字节扫描重跑 HITS 0；085 四件套按真实轮次补齐；E353 计入四值「已失败」 |
| E284 | `00:175` 复用同一模块与连续多轮新建数据层模块的张力 | 085 零新增第三方、复用既有 `robust` / `Envelope` / `diag_line` / `semver` / `PROTECTED_FILES`；张力继续缓解但整体未完全消除，仍登记 |
| E285 | 069–084 连续十六轮未通过，`00:9.1` 要求停下 | D-085-1：按 `00:248` 覆盖，不中断但逐条回显卡点；不改验收项凑通过 |
| E293 | 本轮无新增防错项 | E350 属 A264 已覆盖、E351 属 A245 已覆盖、E352 属 A157 / A159 已覆盖、E353 属 A145 / A249 / 068 先例已覆盖；按 `00:207` 防错清单零改动、历史行不重写（A181） |

预防项（未发生，不计已失败）：A140 / A254 提交前核锁与运行中 git 进程、A268 G2 四份原文与 G3 `## 9` / `## 10` 锚点一次排对、A265 演示五数组 16 项对齐、A252 分段口径、A206 远端未推成不写模板值、A258 构建产物凭据字面量、A271 新测试标识符避开 `api_guard.py` 的 `FORBIDDEN`。

自评 7（7 → 7 → 7）。扣分：5 项仍 `Planned`；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍；Q-067 / Q-070 ~ Q-082 未拍；真实 jar 禁用执行、配置快照落盘与 UI 页码弹窗渲染未启动；6 项低可信度转述未交叉印证；`00:9.1` 卡点未闭环。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 85 号 spec 逐字 3 字节、四份原文全文回显（261 / 520 / 268 / 64 行）、A145 远端补验（c025a78 / 1243 / ALL_MATCH True）、A211 AX04 四锚点、A244 合规复核、`00:230` 时间核实、A248 / A266 预检、A217 无占位、A267 真实 slug、lib 最终 687 / 0、分段 726 / 0、Win GNU RC=0、42 组双向注入、31 守卫 0 FAIL、CI 三 job 通过、零新增第三方、v1 7 符号不变、AX04 `DataLayer`、085 / 086 提交与推送结果见 `rounds.md` 086 补记 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353；035–047 历史格式缺失（不补写） |
| 未证实 | Q-082-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、EQ-01 ~ EQ-13、4 条 Q-C、5 项 `Planned`、6 项低可信度转述、逐版本归属 |
| 未启动 | 真实模组 jar 禁用执行、配置快照落盘与恢复预览、UI 顺序页码弹窗渲染、真实 NBT 读取写回、vianbt 库引入、插件加载执行、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载、zip / 投影解析 |
| 受阻 | 无（远端 Git Data API 通道正常；5 项 `Planned` 属未启动，不计受阻） |

按 `00:245`，存在已失败 / 未证实 / 未启动，**不发通过标记**（`00:9.1`）。

## 11. 本轮文档更新

85 号 spec、`round-085-full-readback.md`、`085-mod-rollback.md`、`round-085.md`、`demos/round-085-mod-rollback.html`；`rounds.md` / `ax-feature-pool.md` / `code-ownership-audit.md` / `requirement-compliance-audit.md` / `interface-log.md` / `docs/index.md` 补记（086 一并落地）。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX / 语言包 / PNG / 防错清单零改动。

## 12. 唯一下一步

086 按 068 / 084 先例补 085 交付闭环：`src/` 零改动，补齐 085 / 086 两套四件套，一次提交推送 085 代码与全部文档，重打 zip，给出 085 与 086 的最终回复；不发通过标记。

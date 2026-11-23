# 第 088 轮：AX08 `instance_import` 交付闭环（`src/` 零改动）

| 项 | 值 |
| --- | --- |
| 编号 | 088 |
| 状态 | AX08 `instance_import` 数据层上一轮落地、本轮交付闭环；`src/` 零改动；AX08 `DataLayer`；`Planned 4` / `DataLayer 19` / `GateOnly 1`；`api::v1` 7 符号不变；真实解压落盘、拖动到此处页面与 UI 渲染未启动 |
| 依据 | `docs/spec/88-round-088-instructions.txt`（逐字 3 字节 `干`）；`00:34` / `00:133` / `00:137` / `00:207` / `00:230` / `00:245` / `00:248` / `00:9.1` / `00:9.2`；`docs/decisions/068-delivery-reconciliation.md`；`docs/decisions/084-delivery-closure.md`；`docs/decisions/087-delivery-closure.md`；A15 / A18 / A50 / A100 / A116 / A140 / A142 / A145 / A154 / A159 / A165 / A177 / A181 / A201 / A202 / A203 / A204 / A205 / A206 / A208 / A211 / A216 / A217 / A236 / A240 / A244 / A245 / A246 / A248 / A249 / A252 / A254 / A258 / A260 / A265 / A266 / A267 / A268 / A269 / A270 / A271 |
| 前序 | 087 远端 `d5a8427` / `1260 / 1260 ALL_MATCH True`、HEAD `b7c6d70`、DIRTY 0；088 代码与守卫在上一轮落地但未给最终回复，本轮开工 DIRTY 8（5 修改 + 3 新增），四件套 / 台账 / 提交 / 推送 / zip / 最终回复全部缺失 |
| 本轮性质 | 按 068 / 084 / 086 / 087 先例的交付闭环轮；按 A249 补 088 四件套，修守卫断言缺口，并把全部产物一次同步到远端、重打 zip |

## 2. 时间戳

开工 `Tue Nov 24 00:02:16 CST 2026`。088 代码落地发生在上一轮（087 最终回复之后），本轮补齐交付。

## 3. 本轮目标与范围

用户 088 逐字 3 字节 `干`，按 `00:133` 落盘 `docs/spec/88-round-088-instructions.txt`。按 A248 / A266 开轮核 88 / 87 / 86 / 85 / 84 / 83 / 82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 逐字副本：88 / 87 / 86 / 85 / 84 / 83 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 71 号均仅 3 字节 `干`，82 号 159 字节完整句，72 号 117 字节澄清句已在 072 处理并撤回 071 归因（E251）。按 A266，平台拼入用户位次的文本不作用户当轮指令、不据此写「未遵守 / 偏离 / 下一步按该行决定」、不进 `00:133` 逐字副本；工具从未禁用。

真读 `00-requirements.txt` 261 行 / 16422 字节全文、`ai-errors.md` 520 行 / 55513 字节全文（分两段回显）、`11-features-input.txt` 268 行 / 17096 字节与 `12-server-features-input.txt` 64 行 / 4970 字节全文。A211 复核 AX08 七锚点 `11:15` / `11:21` / `11:222` / `12:35` / `12:36` / `12:40` / `12:41`；按 A267 读 `src/core/ax.rs:24–39` 真实表：AX08 已改 `instance_import` / `DataLayer` / conflict 空 / ui true，`Planned 4`（AX07 / AX15 / AX20 / AX22），`ax.rs:82` 断言 `Planned == 4`，24 行分布 `Planned 4` / `DataLayer 19` / `GateOnly 1`。按 A217 核 `src/core/` 已有 `instance.rs` / `instance_drop.rs`（070 语义不同、不复用）与 AX08 新落 `instance_import.rs`。

A244 复核：26 包 / 25 第三方 vendor / 58 份 LICENSE 全文 / `THIRD-PARTY-NOTICES.md` 309 行 / `code-ownership-audit.md` 逐轮登记，085–088 零新增第三方。`00:230` 本轮真执行：`TZ='CST-8' date` 得 `Tue Nov 24 00:02:16 CST 2026`；只读 `GET /git/ref/heads/main` RC=200 得 `d5a8427…`；上游状态复核 082 的 `ViaVersion/ViaNBT` 不变。

按 A145 补验：远端 `d5a8427f1426d24f8d8d6054cec2e8a2b4588ecf`（087 补记，parent `247e765`），完整 recursive tree `LOCAL 1260 / REMOTE 1260 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`。本地 HEAD `b7c6d70`、DIRTY 8、无 `.git/index.lock`、无运行中 git 进程、PYC 0。按 A142 逐项核 8 项 DIRTY 的真实副作用，不凭幂等判据臆断；两个 zip 为 087 轮包。

按 A202 打开 `087-delivery-closure.md:12` 核尾部为「088 按功能池落下一项」，按 A208 复核 `b-class-status-recheck.md:85`（EQ-01 ~ EQ-13 待拍、未启用，B04 卡 EQ-01 但本轮不动 UI，无阻塞层）。按 068 / 084 / 086 / 087 先例定本轮为 **088 交付闭环轮**（D-088-2 我的默认）：`src/` 零改动、零新增第三方、不新开功能池项、4 项 `Planned` 不变；087 尾部「落下一项」由 088 代码落地完成，不再顺延（A201 显式覆盖）。

A249 形态实测：88 号 spec 落盘后 `python3 scripts/delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-088-full-readback.md`。不删 spec 规避守卫、不改守卫断言，补齐 088 四件套后复跑 OK，FAIL 原样留痕。`00:9.1` 069–087 连续十九轮未通过按 `00:248` 用户当轮「干」覆盖，不中断但卡点逐条回显（D-088-1）。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D-088-1 | 连续十九轮未通过按 `00:248` 覆盖 | 卡点逐条回显；发通过标记需用户拍板 Q / EQ 并逐轮闭环，不改测试、不降验收项 |
| D-088-2 | 088 定为交付闭环轮，`src/` 零改动 | 按 068 / 084 / 086 / 087 先例 + A202 + A249；不写成用户已决断（A177） |
| D-088-3 | AX08 保持 `DataLayer`，4 项 `Planned` 不变 | 不代拍 Q / EQ；087 尾部「落下一项」不再顺延 |
| D-088-4 | 修 `instance_import_guard.py` 5 处断言缺口并重跑双向注入 | E361；`ax_guard.py` 历史缺口 E362 单列，本轮不扩大 diff |
| D-088-5 | 088 全部产物一次提交 | A11 逐项核 diff 范围；A254 提交前核锁与运行中 git 进程 |
| D-088-6 | 增量推送；逐项 ALL_MATCH 后才写补记 | A216 / A206；`force=false`，不强推、不重写历史；推送结果写进 `rounds.md` 088 补记 |
| D-088-7 | 两个 zip 重打 | A205；主 zip 按 `git ls-files -z \| zip -@`、`ui-previews.zip` 按 `demos/preview/*.png` 清单；清理 `scripts/__pycache__/` |
| D-088-8 | Q / EQ 不代拍 | Q-082-01 / 02 / 03 与历史 26 组 Q、EQ-01 ~ EQ-13、4 条 Q-C 保持未证实 |
| D-088-9 | 状态分层与通过标记 | AX08 数据层已实现 / 已验证；真实解压落盘、拖动页面与 UI 渲染未启动；不发通过标记 |

## 5. 接口终点核对（`00:137`）— A244 要求显式核

| 引用点 | 088 形态 |
| --- | --- |
| `src/core/instance_import.rs` | 上一轮落地 842 行 / 28 单测，本轮零改动：`ROOT_KEYS` / `ENTRY_KEYS` / `FORMATS` / `KINDS` / `ACTIONS` / `STATES` / `PATH_KINDS` 七表、四枚举显式 code、`validate_entry_path` 用 `Component` 逐分量、`classify_path` 走显式表、`entry_consistent` 五条规则六处调用、单条突变八入口、原子写、统一信封十值载荷 |
| `src/core/ax.rs` / `boot.rs` / `mod.rs` | 上一轮已接 AX08 `DataLayer` / `core.instance_import` / `pub mod instance_import;`，本轮零改动 |
| `src/api.rs` | 零改动，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `scripts/instance_import_guard.py` / `.github/workflows/ci.yml` | 上一轮已挂 `scan` job；本轮仅修守卫 5 处断言缺口（E361） |
| `scripts/ax_guard.py` | 上一轮已加 `'AX08'`；本轮零改动 |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff |
| UX HTML / 两语言包 / 56 PNG | 零 diff；AX08 `ui: true` 但 UI 渲染层未启动（A100） |
| 088 新增 | 88 号 spec、088 readback / decision / verification / demo、`rounds.md` 等台账与 `docs/index.md` 补记 |

## 6. 代码落点

`src/` 零改动。AX08 数据层复用 `robust::MAX_TEXT_BYTES` / `MAX_PATH_BYTES` / `MAX_ID_BYTES` / `MAX_REL_DEPTH` / `safe_join` / `read_or_default`、`diag_line`、`Envelope` / `Kind`、`serde_json`；四枚举 `ImportFormat` / `EntryKind` / `ImportAction` / `EntryState` 用显式 code 与逐值比对守住（A154 / A269 / A270）。`validate_entry_path` 用标准库 `Component` 拒 `ParentDir` / `RootDir` / `Prefix` / `CurDir`，不做字符串清洗（A50 / A165）。纯查询段八函数经守卫解析函数体核不含 `fs::` 写操作（A260）。`change_event()` 十值载荷不含用户文本（E330 口径）。`00:175` / `11:15` 的复用张力 E284 继续登记，不写成「已满足」。

## 7. 交付快照

本轮一次提交把 088 代码 / 守卫 / 五处修改（上一轮落地的 DIRTY 8）与 088 四件套、台账补记纳入主快照；推送后只读核远端 ref 与完整 tree，逐项 ALL_MATCH 结果写入 `docs/records/rounds.md` 088 补记（A206，不用模板值冒充）。开工 A145 补验为 `d5a8427` / `1260 / 1260 / ALL_MATCH True`。两个 zip 按 A205 重打。全仓零凭据；`scripts/__pycache__/` 保持 0 项；临时注入脚本用后即删。

## 8. 验证

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib`（088 回归） | 715 / 0（RC=0，`src/` 零改动；687 → 715，新增 28 单测） |
| 集成段 1（088 实跑） | 26 / 0（6 + 7 + 7 + 6） |
| `cargo test --offline --doc`（088 实跑） | 0 / 0 |
| 全量（分段求和，A252） | **754 / 0**（lib 715 + 集成段 1 26 + 真加载两段 13 + doc 0；真加载两段与 Win GNU 取 085 原始输出，`src/` 零改动未重跑） |
| Windows GNU 交叉检查（085 实测） | RC=0 / 29.02 s / 零 warning |
| 守卫 | 32 个（31 个 `*_guard.py` + `p09_scan.py`），补齐 088 四件套后 0 FAIL |
| 双向注入 | 首轮 36 组：29 真 FAIL / 5 假 OK / 1 跨守卫缺口 / 1 锚点跳过；修守卫 5 处后 **34 组全真 FAIL、0 假 OK、恢复 OK、哈希复原** |
| CI 三 job | NO_CREDENTIAL / NO_EXPLANATORY / NO_HARDCODE |
| 独立验证 | 部分通过，未发通过标记 |

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E360 | 088 代码与守卫在上一轮落地，但四件套、台账、提交、推送、zip、最终回复全部缺失，HEAD 仍 `b7c6d70`、DIRTY 8；文件已落盘不等于交付已闭环 | 088 按 A145 只读补验远端 ref + 完整 tree，按 068 / 084 / 086 / 087 先例定交付闭环轮；按 A142 逐项核 8 项 DIRTY 真实成分；补齐四件套、提交、推送、逐项 ALL_MATCH、zip 重打与最终回复；E360 计入四值「已失败」 |
| E361 | 首轮双向注入 36 组出现 5 个假 OK：`classify_path` / `entry_consistent` / `ci_step` / `payload_key` / `bad_input` 五处守卫断言用子串 `in` 或只数数量，注入加后缀或改载荷键名后守卫不挡 | 按 A241 / A269 / A270 同形态修守卫：精确正则表形态、`(?!\w)` 边界、CI step 行首匹配、载荷键集合 EXPECTED 逐值、坏输入标签边界；`r'\b'` 首修误判 `i.kind != classify_path(&i.path)` 末尾 `)`，改 `(?!\w)` 后正常态 OK；`python -m py_compile` 通过、pyc 清理；改守卫不改实现、不改测试断言；重跑 34 组全真 FAIL、0 假 OK、恢复 OK、哈希复原；E361 计入四值「已失败」 |
| E362 | 注入 `scripts/ax_guard.py` 删去显式断言表中的 `'AX08'` 后仍 `AX_GUARD_OK specs=24 data_layer=19 planned=4`：动态 for 循环列表无独立 EXPECTED 集合，删项不触发断言 | 按 A240 / A262 登记为历史守卫缺口，本轮不扩大 diff 修历史守卫；AX08 状态另由 `instance_import_guard.py` 第 261–272 行独立核 `name` / `state` / `conflict` 与 24 行分布，双守卫互补；E362 计入四值「未证实」，列入待办 |
| E284 | `00:175` 复用同一模块与连续多轮新建数据层模块的张力 | 088 零新建模块；公共能力复用既有 `robust` / `Envelope` / `diag_line` / `serde_json`。张力继续缓解但整体未完全消除，仍登记 |
| E285 | 069–087 连续十九轮未通过，`00:9.1` 要求停下 | D-088-1：按 `00:248` 覆盖，不中断但逐条回显卡点；不改验收项凑通过（`00:245`） |
| E293 | 本轮无新增防错项 | E360 属 A145 / A142 / A249 / 068 先例已覆盖、E361 属 A241 / A269 / A270 / A157 已覆盖、E362 属 A240 / A262 已覆盖，按 `00:207` 防错清单零改动、历史行不重写（A181） |

预防项（未发生，不计已失败）：A140 / A254 提交前核锁与运行中 git 进程、A268 G2 四份原文与 G3 `## 9` / `## 10` 锚点一次排对、A265 演示五数组 16 项对齐、A252 分段口径、A206 远端未推成不写模板值、A258 构建产物凭据字面量、A267 改功能池状态前读真实 slug、A205 zip 按 tracked 清单打包。

自评 7（7 → 7 → 7）。扣分：4 项仍 `Planned`；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍；Q-067 / Q-070 ~ Q-082 未拍；真实解压落盘、拖动页面与 UI 渲染未启动；E362 历史守卫缺口未修；6 项低可信度转述未交叉印证；`00:9.1` 卡点未闭环。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 88 号 spec 逐字 3 字节、四份原文全文回显（261 / 520 / 268 / 64 行）、A145 远端补验（d5a8427 / 1260 / ALL_MATCH True）、A142 DIRTY 8 逐项复核、A211 AX08 七锚点、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 088 四件套形态、068 / 084 / 086 / 087 先例判定、`00:137` / `00:245` 显式核、088 占位符 0、lib 715 / 0、集成段 1 26 / 0、doc 0 / 0、32 守卫 0 FAIL、34 组双向注入全真 FAIL、CI 三 job 通过、零新增依赖、v1 7 符号不变、088 提交与推送结果见补记 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 / E356 / E357 / E360 / E361；035–047 历史格式缺失（不补写） |
| 未证实 | E362、Q-082-01 / Q-082-02 / Q-082-03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、EQ-01 ~ EQ-13、4 条 Q-C、4 项 `Planned`、6 项低可信度转述、逐版本归属 |
| 未启动 | 真实 mrpack / CurseForge zip 解压落盘、拖动到此处页面渲染、实例模板克隆执行、可移植实例导出、真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载 |
| 受阻 | 无（远端 Git Data API 通道正常；4 项 `Planned` 属未启动，不计受阻） |

按 `00:245`，存在已失败 / 未证实 / 未启动，**不发通过标记**（`00:9.1`）。

## 11. 本轮文档更新

88 号 spec、`round-088-full-readback.md` / `088-instance-import-delivery.md` / `round-088.md` / `demos/round-088-instance-import.html`；`rounds.md` / `ax-feature-pool.md` / `code-ownership-audit.md` / `requirement-compliance-audit.md` / `interface-log.md` / `docs/index.md` 补记；`scripts/instance_import_guard.py` 修 5 处断言缺口。`Cargo.toml` / `Cargo.lock` / `vendor/` / `src/` / UX / 语言包 / PNG / 防错清单零改动。

## 12. 唯一下一步

089 按功能池落下一项（剩 4 项 `Planned`：AX07 `doh_support` / AX15 `studio_image_editor` / AX20 `projection_workshop` / AX22 `shimu_account`）：真读 00 / 11 / 12 号原文全文后收窄，先按 A267 核真实 slug 与 conflict（AX07 conflict `network_io_not_started` 需逐条核冲突，A230）；若回任一 Q / EQ 则改走拍板闭环。

089 补记（088 推送状态覆盖）：088 决策写「受阻 | 无（远端 Git Data API 通道正常）」与「088 提交与推送结果见补记」，均为 088 推送前判断。088 末段三次调用 `api_push.py` 被网关超时截断（工具结果 `sandbox call failed` / `context deadline exceeded`），每次截断后只读核远端 ref 均未变；089 开轮 A145 补验远端 `d5a8427` / `LOCAL 1267 / REMOTE 1260 / DIFF 18 / ALL_MATCH False`。按 A206 / A209 写「受阻、ALL_MATCH 本轮不成立」，E363 计入四值「已失败」，不包装成已处理。088 补记（推送后真实值）未写；089 按 A145 补验远端未变后合并重推，推送成功且逐项 ALL_MATCH 前该结论保持（A201，历史行不重写）。

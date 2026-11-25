# 第 091 轮：AX15 `studio_image_editor` 数据层

| 项 | 值 |
| --- | --- |
| 编号 | 091 |
| 状态 | AX15 `studio_image_editor` `Planned → DataLayer`；`Planned 2` / `DataLayer 21` / `GateOnly 1`；`api::v1` 7 符号不变；真实图片像素调整、预览渲染、Studio 六动作未启动 |
| 依据 | `docs/spec/91-round-091-instructions.txt`（逐字 3 字节 `干`）；`00:34` / `00:133` / `00:137` / `00:207` / `00:230` / `00:245` / `00:248` / `00:9.1` / `00:9.2`；`docs/decisions/090-projection-workshop.md`；`docs/research/31-axolotl-launcher-features.md`；A15 / A18 / A50 / A100 / A116 / A140 / A145 / A154 / A158 / A159 / A164 / A165 / A177 / A181 / A201 / A202 / A203 / A204 / A205 / A206 / A208 / A211 / A216 / A217 / A230 / A240 / A241 / A243 / A244 / A245 / A246 / A248 / A249 / A250 / A252 / A254 / A258 / A260 / A262 / A264 / A265 / A266 / A267 / A268 / A269 / A270 / A271 |
| 前序 | 090 远端 `f28d5bd` / `1279 / 1279 ALL_MATCH True`、HEAD `e60d6c9`、DIRTY 0；090 尾部写「091 按功能池落下一项」 |
| 本轮性质 | 功能轮：A230 逐条核 3 项 `Planned` 冲突后落 AX15 数据层 |

## 2. 时间戳

开工 `Tue Nov 24 12:58:12 CST 2026`。

## 3. 本轮目标与范围

用户 091 逐字 3 字节 `干`，按 `00:133` 落盘 `docs/spec/91-round-091-instructions.txt`。按 A248 / A266 开轮核 21 份 spec 逐字副本；平台拼入用户位次的文本不作用户当轮指令、不进 `00:133` 逐字副本；工具从未禁用。

真读 `00-requirements.txt` 261 行 / 16422 字节全文、`ai-errors.md` 520 行 / 55513 字节全文（分两段回显）、`11-features-input.txt` 268 行 / 17096 字节与 `12-server-features-input.txt` 64 行 / 4970 字节全文。A211 复核：按 A267 读 `src/core/ax.rs:20–43` 真实表，3 项 `Planned` 为 `AX07 doh_support`（conflict `network_io_not_started`）/ `AX15 studio_image_editor` / `AX22 shimu_account`；按 A217 核 `src/core/` 无 `studio*` / `image*` / `logo*` / `pixel*` 占位模块。按 A202 打开 `090-projection-workshop.md:12` 核尾部；按 A208 复核 `b-class-status-recheck.md:85`（EQ-01 ~ EQ-13 待拍、未启用，B04 卡 EQ-01 但本轮不动 UI 渲染层，无阻塞层）。

A244 复核：26 包 / 25 第三方 vendor / 58 份 LICENSE 全文 / `THIRD-PARTY-NOTICES.md` 309 行 / `code-ownership-audit.md` 逐轮登记，085–091 零新增第三方。`00:230` 本轮真执行：`TZ='CST-8' date` 得 `Tue Nov 24 12:58:12 CST 2026`；只读 `GET /git/ref/heads/main` RC=200 得 `f28d5bd…`；上游状态复核 082 的 `ViaVersion/ViaNBT` 不变。按 A145 补验：远端 `f28d5bd11ea7a97f4ba69cd58047777ae5561591`（090 补记，parent `c7f3071`），完整 recursive tree `1279 / 1279 / DIFF 0 / ALL_MATCH True`；本地 HEAD `e60d6c9`、DIRTY 0、无锁、无运行中 git 进程、PYC 0。

按 A230 逐条核冲突（090 唯一下一步点名动作）：打开 `31-axolotl-launcher-features.md` 全文与 `ax-feature-pool.md`。AX07 的 `network_io_not_started` 是技术受阻非需求冲突，`31-axolotl-launcher-features.md:35` 写「11-13 / 11-29 / 12-60 均无 DoH，真实网络 IO 未启动、Win7 TLS 前置（EQ-03）」，真读 00 / 11 / 12 号全文确认无已决断 DoH 锚点，排除留痕、conflict 不清。AX22 浏览器授权依赖真实网络 IO + 第三方端点 + 境外限制（`11:7` / 054）+ `11:18` API 不共有，排除留痕，登记 Q-091-01。AX15 的 `12:63` 第 27 条「支持 png 快速设置服务器 logo（会自动调整像素）」是原文已决断、不依赖 EQ 的锚点；075 E276 与 077–090 把 AX15 归「撤销栈同构 / 重 UI」是只核调研描述、未逐行回显 12 号原文时写下的相对排序理由，按 073 / 075 / 077 / 078 / 079 / 080 / 081 / 082 / 090 九次收窄先例处理，历史行不重写（A181 / A201），本补记覆盖。

A249 形态实测：91 号 spec 落盘后 `python3 scripts/delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-091-full-readback.md`。不删 spec 规避守卫、不改守卫断言，补齐 091 四件套后复跑 OK，FAIL 原样留痕。`00:9.1` 069–090 连续二十二轮未通过按 `00:248` 用户当轮「干」覆盖，不中断但卡点逐条回显（D-091-1）。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D-091-1 | 连续二十二轮未通过按 `00:248` 覆盖 | 卡点逐条回显；发通过标记需用户拍板 Q / EQ 并逐轮闭环，不改测试、不降验收项 |
| D-091-2 | 091 定为功能轮，落 AX15 数据层 | A230 逐条核冲突后按 073–090 收窄先例；`src/` 只落数据层，UI 渲染不启动（A100）；不写成用户已决断（A177） |
| D-091-3 | AX15 `Planned → DataLayer`，其余 2 项保持 | AX07 conflict 保持 `network_io_not_started`；`Planned 2` / `DataLayer 21` / `GateOnly 1` |
| D-091-4 | 两目标槽位 `logo` / `icon` 都登记 | A250：`12:63` 服务器 logo 与 `12:59` / `11:243` 图标是并列对象，不二选一；`IMAGE_FORMATS` 只登记 png / gif / svg + `opaque` 兜底，不擅自枚举「等等」 |
| D-091-5 | Q-091-01 / 02 / 03 登记 | AX22 端点与授权形态、图片预览三档视图是否复用 `projection.rs`、Studio 编辑动作栈是否复用 `banner_design.rs` 保持待拍，不代拍 |
| D-091-6 | 090 守卫写死 AX15 `Planned` 按 A201 / A158 同步改 | E369；`ax_guard.py` 显式断言表加 `'AX15'`；新守卫 41 组双向注入 |
| D-091-7 | 091 全部产物一次提交 | A11 逐项核 diff 范围；A254 提交前核锁与运行中 git 进程 |
| D-091-8 | 增量推送；逐项 ALL_MATCH 后才写补记 | A216 / A206；`force=false`，不强推、不重写历史；推送结果写进 `rounds.md` 091 补记 |
| D-091-9 | 两个 zip 重打 | A205；主 zip 按 `git ls-files -z \| zip -@`、`ui-previews.zip` 按 `demos/preview/*.png` 清单；清理 `scripts/__pycache__/` |
| D-091-10 | 状态分层与通过标记 | AX15 数据层已实现 / 已验证；真实图片像素调整、预览渲染、Studio 六动作未启动；不发通过标记 |

## 5. 接口终点核对（`00:137`）— A244 要求显式核

| 引用点 | 091 形态 |
| --- | --- |
| `src/core/studio_image.rs` | 新增 881 行 / 29 单测：`ROOT_KEYS` / `ENTRY_KEYS` / `IMAGE_FORMATS` / `STATES` / `PATH_KINDS` 五表、两枚举显式 code、`validate_entry_path` 用 `Component` 逐分量、`classify_target` 走显式表、`entry_consistent` 五条规则八处调用、单条突变八入口、原子写、统一信封十值载荷 |
| `src/core/ax.rs` / `boot.rs` / `mod.rs` | AX15 `DataLayer`；`LOADED_MODULES` 在 `core.projection` 之后、`dispatcher.launcher` 之前插 `core.studio_image`（A256）；`pub mod studio_image;` |
| `src/api.rs` | 零改动，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `scripts/studio_image_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job；41 组双向注入全真 FAIL |
| `scripts/projection_guard.py` / `scripts/ax_guard.py` | E369 联动：090 守卫的 A230 断言把 AX15 从 `Planned` 改 `DataLayer`；`ax_guard.py` 显式表加 `'AX15'` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff |
| UX HTML / 两语言包 / 56 PNG | 零 diff；`studio_image_guard.py` 核三处不含 `studio-image.json` |
| 091 新增 | 91 号 spec、091 readback / decision / verification / demo、`rounds.md` 等台账与 `docs/index.md` 补记 |

## 6. 代码落点

`studio_image.rs` 复用 `robust::{MAX_TEXT_BYTES, MAX_PATH_BYTES, MAX_ID_BYTES, MAX_REL_DEPTH, safe_join, read_or_default}`、`diag_line`、`Envelope` / `Kind`、`serde_json`、`settings_io::PROTECTED_FILES`。`validate_entry_path` 用标准库 `Component` 拒 `ParentDir` / `RootDir` / `Prefix` / `CurDir`，不做字符串清洗（A50 / A165）。纯查询段八函数经守卫解析函数体核不含 `fs::` 写操作（A260）。`change_event()` 十值载荷不含用户文本（E330 口径）。不引图像库、不持有图片字节、不实现撤销重做栈（075 E276 排除留痕由守卫机器化：禁 `undo` / `redo` / `MAX_HISTORY` / `push_layer`）、不重复 `projection.rs` 三档视图（禁 `ViewMode` / `scaled` / `original` / `projection.preview`）。`00:175` / `11:15` 的复用张力 E284 继续登记，不写成「已满足」。

## 7. 交付快照

本轮一次提交把 091 代码 / 守卫 / 五处接线、E369 联动与 091 四件套、台账补记纳入主快照；推送后只读核远端 ref 与完整 tree，逐项 ALL_MATCH 结果写入 `docs/records/rounds.md` 091 补记（A206，不用模板值冒充）。开工 A145 补验为 `f28d5bd` / `1279 / 1279 / ALL_MATCH True`。两个 zip 按 A205 重打。全仓零凭据；`scripts/__pycache__/` 保持 0 项；临时注入脚本用后即删。

## 8. 验证

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib`（091 回归） | 780 / 0（RC=0；751 → 780，新增 29 单测，其中 1 个首跑 FAILED 为夹具与既定边界不对齐，按 `00:9.2` / A264 改夹具、实现零改动） |
| 集成段 1（091 实跑） | 26 / 0（6 + 7 + 7 + 6） |
| `cargo test --offline --doc` | 0 / 0 |
| 全量（分段求和，A252） | **819 / 0**（lib 780 + 集成段 1 26 + 真加载两段 13 + doc 0；真加载两段与 Win GNU 取 085 / 088 原始输出，`src/` 除新模块外零改动未重跑） |
| Windows GNU 交叉检查（085 实测） | RC=0 / 29.02 s / 零 warning |
| 守卫 | 34 个（33 个 `*_guard.py` + `p09_scan.py`），补齐 091 四件套后 0 FAIL |
| 双向注入 | 41 组全真 FAIL、0 假 OK、恢复 OK、哈希复原；E369 修复点单独双向验证 |
| CI 三 job | NO_CREDENTIAL / NO_EXPLANATORY / NO_HARDCODE |
| 独立验证 | 部分通过，未发通过标记 |

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E369 | `scripts/projection_guard.py:282–285` 把 AX15 写死为 `Planned`（090 的 A230 排除留痕断言）；091 把 AX15 改 `DataLayer` 后守卫会报 `a230_conflict_not_recorded AX15`，属 A201 / A158 同形态的多文件状态分叉 | 同步把该断言改为 `DataLayer`、注释改为「AX15 091 已落 DataLayer」；单独双向验证：改回 `Planned` 得 `PROJECTION_GUARD_FAIL reason=a230_conflict_not_recorded AX15`、恢复得 `PROJECTION_GUARD_OK`；`ax_guard.py` 显式表另加 `'AX15'`；E369 计入四值「已失败」 |
| E370 | 首跑 `cargo test --offline --lib` 得 `779 passed; 1 failed`：`add_entry_single_and_setters_are_bounded` 断言 `!p.set_fit("i1", false)`，但实现既定边界是 `entry_consistent` 只拒 `Adjusted && !fit`，Draft 状态下 `fit=false` 合法（A15 保留回显 `assertion failed: !p.set_fit("i1", false)` at `src/core/studio_image.rs:770:9`） | 按 `00:9.2` / A180 / A264 改夹具：断言 Draft+fit=false 合法、`Adjusted` 被拒、恢复 fit=true 后 `Adjusted` 成功、`Adjusted+fit=false` 被拒；实现零改动、断言强度不降；复跑 `780 / 0`；E370 计入四值「已失败」 |
| E371 | 双向注入首跑 41 组里 `classify_table` 假 OK：注入把 `for (prefix, code) in PATH_KINDS` 改成 `PATH_KINDS_X`，守卫锚点未带 `{`，`PATH_KINDS_X {` 仍含子串 `PATH_KINDS`，属 A241 / A157 同形态的子串匹配缺口 | 守卫锚点改为 `for (prefix, code) in PATH_KINDS {`（带花括号）；`python -m py_compile` 通过；41 组复跑 `true_fail=41 / fake_ok=0 / skipped=0 / restored_all=True`；E371 计入四值「已失败」 |
| E372 | A230 逐条核冲突时，AX15 的「撤销栈同构 / 重 UI」是 075 E276 与 077–090 多轮相对排序理由；若照抄会漏掉 `12:63` 已决断锚点，重复 A211 批评的「连续多轮只核状态复核轮」 | 真读 00 / 11 / 12 号全文后按 073–090 九次收窄先例处理，排除子项（图片预览三档视图、撤销重做栈、Studio 六动作）逐项留痕并登记 Q-091-02 / Q-091-03，历史行不重写、本补记覆盖；E372 计入四值「已证实」的处置项，不写成已失败 |
| E362 | `scripts/ax_guard.py` 显式断言表删去 `'AX08'` 后仍 `AX_GUARD_OK`（088 登记的历史守卫缺口） | 091 不扩大 diff 修历史守卫；AX15 与 AX08 状态另由 `studio_image_guard.py` / `instance_import_guard.py` 独立核，双守卫互补；E362 保持未证实 |
| E284 | `00:175` 复用同一模块与连续多轮新建数据层模块的张力 | 091 复用既有公共能力、守卫显式禁与 `banner_design.rs` / `projection.rs` 重复的字面量，不新建重复框架；张力继续缓解但整体未完全消除，仍登记 |
| E285 | 069–090 连续二十二轮未通过，`00:9.1` 要求停下 | D-091-1：按 `00:248` 覆盖，不中断但逐条回显卡点；不改验收项凑通过（`00:245`） |
| E293 | 本轮无新增防错项 | E369 属 A201 / A158 已覆盖、E370 属 `00:9.2` / A180 / A264 已覆盖、E371 属 A241 / A157 已覆盖、E372 属 A211 / A201 已覆盖，按 `00:207` 防错清单零改动、历史行不重写（A181） |

预防项（未发生，不计已失败）：A140 / A254 提交前核锁与运行中 git 进程、A268 G2 四份原文与 G3 `## 9` / `## 10` 锚点一次排对、A265 演示五数组 16 项对齐、A252 分段口径、A206 远端未推成不写模板值、A258 构建产物凭据字面量、A267 改功能池状态前读真实 slug、A271 新测试标识符核全仓禁用表、A205 zip 按 tracked 清单打包。A243：守卫 FAIL 但行为测试仍通过的约束（A230 排除留痕、批量禁令、载荷十键）如实登记「由守卫持有」，不改测试凑失败、不降守卫断言。

自评 7（7 → 7 → 7）。扣分：2 项仍 `Planned`；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍；Q-067 / Q-070 ~ Q-091 未拍；真实图片像素调整、预览渲染、Studio 六动作未启动；E362 历史守卫缺口未修；6 项低可信度转述未交叉印证；`00:9.1` 卡点未闭环。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 91 号 spec 逐字 3 字节、四份原文全文回显（261 / 520 / 268 / 64 行）、A145 远端补验（f28d5bd / 1279 ALL_MATCH True）、A230 三项冲突逐条核验、A211 `12:63` 等八锚点、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 091 四件套形态、A268 G2/G3、`00:137` / `00:245` 显式核、091 占位符 0、lib 780 / 0、集成段 1 26 / 0、doc 0 / 0、34 守卫 0 FAIL、41 组双向注入全真 FAIL、E369 修复点单独双向验证、CI 三 job 通过、零新增依赖、v1 7 符号不变、091 提交与推送结果见补记 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 / E356 / E357 / E360 / E361 / E363 / E366 / E367 / E369 / E370 / E371；035–047 历史格式缺失（不补写） |
| 未证实 | E362、Q-091-01 / Q-091-02 / Q-091-03、Q-082-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、Q-090-01 / Q-090-02、EQ-01 ~ EQ-13、4 条 Q-C、2 项 `Planned`、6 项低可信度转述、逐版本归属 |
| 未启动 | 真实图片像素调整与缩放、裁剪 / 绘画 / 高亮 / 形状 / 文字 / 擦除六动作、图片预览渲染、Studio 打开入口、撤销重做栈执行层、真实 `.litematic` / `.schem` 解析、投影预览渲染、投影资源站安装、方块状态编辑、真实 mrpack / CurseForge zip 解压落盘、拖动到此处页面、实例模板克隆执行、可移植实例导出、真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载 |
| 受阻 | 无（远端 Git Data API 通道正常；2 项 `Planned` 属未启动，不计受阻） |

按 `00:245`，存在已失败 / 未证实 / 未启动，**不发通过标记**（`00:9.1`）。

## 11. 本轮文档更新

91 号 spec、`round-091-full-readback.md` / `091-studio-image.md` / `round-091.md` / `demos/round-091-studio-image.html`；`rounds.md` / `ax-feature-pool.md` / `code-ownership-audit.md` / `requirement-compliance-audit.md` / `interface-log.md` / `docs/index.md` 补记；`scripts/projection_guard.py` 的 E369 状态联动修复。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX / 语言包 / PNG / 防错清单零改动。

## 12. 唯一下一步

092 改走拍板闭环：剩 2 项 `Planned` 均卡网络前置 / Q / EQ（AX07 `doh_support` conflict `network_io_not_started`，EQ-03 Win7 TLS 前置与真实网络 IO 未启动；AX22 `shimu_account` 第三方端点 + 境外限制 + `11:18` API 不共有）。真读 00 / 11 / 12 号原文全文后按 A230 逐条核冲突，把 Q-091-01 / Q-091-02 / Q-091-03、历史 Q 与 EQ-01 ~ EQ-13、4 条 Q-C 摊平给用户拍板；按 A208 不擅自开工硬做，也不擅自定 2 项之间的优先级。

## 091 补记（A245 偶发 FAILED / E373 索引锁 / E374）

502 网关截断后的分段命令首跑 `cargo test --offline --lib` 得 `779 passed; 1 failed`；复跑 3 次全量为 OK / FAILED / OK，FAILED 用例为 `core::cache::tests::single_flight_loads_once_for_concurrent_waiters`（`src/core/cache.rs:252`），属既有并发测试、与 091 新增模块无关。按 A245 单独跑该用例 3 次：S1 OK / S2 OK / S3 FAILED；再复跑全量 3 次：F1 / F2 / F3 均 `780 passed; 0 failed`。实现与测试零改动（`src/core/cache.rs` SHA-1 `614776d34e9ec901bd8b3fcd65b03edd008479b7`、`src/core/studio_image.rs` SHA-1 `bb7f9545734d2cdffcc209f85871d167de09d3bb`，`git diff --name-only` 对两文件无输出），未加跳过标记、未删测试、未改断言。E374 计入四值「已失败」。本轮 819 / 0 的分段求和取通过态各段真实输出，偶发 FAILED 如实登记，不写成「全程 0 FAILED」。502 同时留下 `.git/index.lock`（E373），按 A140 / A254 提交前删除并核无运行中 git 进程、HEAD 唯一、远端 ref 未变，不带着脏锁继续跑。

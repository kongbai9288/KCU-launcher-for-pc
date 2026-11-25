# 091 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/91-round-091-instructions.txt`（3 字节 `干`）；`docs/decisions/090-projection-workshop.md`；`docs/decisions/091-studio-image.md`；`docs/records/round-090-full-readback.md`；`docs/records/round-091-full-readback.md`；`scripts/delivery_guard.py`；`scripts/studio_image_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；A230 冲突逐条核；091 代码与四件套一次同步到远端 |

## 1. 原文复读

`docs/records/round-091-full-readback.md`：四份原文逐字副本（`00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt`）字节 / 行 / SHA-256 表、原文锚点、A145 远端补验、A230 三项冲突逐条核验、A208 / A202 复核、A211 AX15 八锚点、A244 逐条对照表、`00:230` 联网核实、`00:9.1` 冲突裁决、`00:137` 接口终点与 `00:245` 通过标记条件显式核、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；`ai-errors.md` 520 行 / 55513 字节完整读、分两段回显，末条仍为 A271；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行逐行全文回显（A18 / A211 / A244）。91 号 spec 逐字 3 字节 `干`，SHA-256 `9ee0280b…`。

A145 远端补验：只读 `GET /git/ref/heads/main` RC=200 得 `f28d5bd11ea7a97f4ba69cd58047777ae5561591`（090 补记，parent `c7f3071`），完整 recursive tree `LOCAL 1279 / REMOTE 1279 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；本地 HEAD `e60d6c9`、DIRTY 0、无锁、无运行中 git 进程、PYC 0。按 A145 / A216 远端写入以 `base_tree` 增量、`force=false`，不强推、不重写历史。

A266 本轮复核：按 `72-round-072-instructions.txt` 逐字澄清与 A266，平台拼入用户位次的文本不作用户当轮指令、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080–090 已按同一口径补记，历史不重写。工具从未禁用。

`00:230` 本轮真执行：`TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` 得 `Tue Nov 24 12:58:12 CST 2026`；`GET /git/ref/heads/main` RC=200 得 `f28d5bd…`；上游状态复核 082 的 `ViaVersion/ViaNBT` 不变，085–091 零新增上游依赖。

A230 逐条核冲突：`31-axolotl-launcher-features.md` 全文与 `ax-feature-pool.md` 逐条核 3 项 `Planned`。AX07 `network_io_not_started`（技术受阻非需求冲突，`31-...:35` 写真实网络 IO 未启动 / Win7 TLS 前置 EQ-03）排除留痕、conflict 保持；AX22 浏览器授权依赖真实网络 IO + 第三方端点 + 境外限制 + `11:18` API 不共有，排除留痕并登记 Q-091-01；AX15 的 `12:63` 第 27 条「支持 png 快速设置服务器 logo（会自动调整像素）」是原文已决断、不依赖 EQ 的锚点，075 E276 与 077–090 的「撤销栈同构 / 重 UI」属相对排序理由，按 073–090 九次收窄先例落地数据层，排除子项（图片预览三档视图 / 撤销重做栈 / Studio 六动作）逐项留痕，历史行不重写（A181 / A201）。

按 A267 读 `src/core/ax.rs:20–43` 真实 slug 与 conflict；按 A217 核 `src/core/` 无 `studio*` / `image*` / `logo*` / `pixel*` 占位模块。按 A208 复核 `b-class-status-recheck.md:85`：EQ-01 ~ EQ-13 待拍、未启用，B04 卡 EQ-01 但本轮不动 UI 渲染层（A100），无阻塞层。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib`（091 回归） | **780 / 0**（RC=0 / 0.42 s；751 → 780，新增 29 单测） |
| 集成段 1（091 实跑） | **26 / 0**（6 + 7 + 7 + 6） |
| `cargo test --offline --doc`（091 实跑） | **0 / 0** |
| 全量 `cargo test --offline` | **819 / 0**（分段求和） |
| Windows GNU 交叉检查（085 实测） | **通过 / RC=0 / 29.02 s / 零 warning** |

全量 **819 / 0** 为分段求和（A252），各段真实输出：

| 段 | 命令 | 通过 |
| --- | --- | --- |
| lib | `cargo test --offline --lib` | 780 |
| 集成 1 | `--test boot_fallback --test http_construct --test play_stats --test window_handle_contract` | 6 + 7 + 7 + 6 = 26 |
| 集成 2 | `--test plugin_lifecycle_load` | 7（085 原始输出 60.39 s） |
| 集成 3 | `--test plugin_abi_load` | 6（085 原始输出 147.88 s） |
| doc | `cargo test --offline --doc` | 0 |
| 交叉检查 | `cargo check --offline --target x86_64-pc-windows-gnu` | RC=0 / 29.02 s（085 原始输出） |

091 实跑 lib / 集成段 1 / doc（RC 均为 0）；集成段 2 / 3 与 Win GNU 取 085 / 088 原始输出，`src/` 除新模块外零改动未重跑，不写成单条 `cargo test --offline` 的输出（A15 / A252）。`tests/` 真实文件名按 A176 先 `ls tests/*.rs` 核实为 6 个。

首跑 `cargo test --offline --lib` 得 `779 passed; 1 failed`，FAILED 为 `core::studio_image::tests::add_entry_single_and_setters_are_bounded`：`assertion failed: !p.set_fit("i1", false)` at `src/core/studio_image.rs:770:9`。实现按 `entry_consistent` 的「只拒 `Adjusted && !fit`」正确允许 Draft 状态下关闭自动调整。按 `00:9.2` / A180 / A264 保留 FAILED 回显，改夹具为断言 Draft+fit=false 合法、`Adjusted` 被拒、恢复 fit=true 后 `Adjusted` 成功、`Adjusted+fit=false` 被拒，实现零改动、断言强度不降，复跑 `780 / 0`（E370 计入四值「已失败」）。既有 751 断言一字未改、未加跳过标记、未删测试。

## 3. 守卫与 CI

`scripts/studio_image_guard.py` 挂 `.github/workflows/ci.yml` `scan` job。091 复扫 34 个守卫（33 个 `scripts/*_guard.py` 加 `scripts/p09_scan.py`）。落 91 号 spec 后 `delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-091-full-readback.md`（A249），补齐 091 四件套后 `DELIVERY_GUARD_OK rounds=[… 88, 89, 90, 91] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step`。

连锁缺口 E369：`scripts/projection_guard.py:282–285` 把 AX15 写死为 `Planned`，091 改 AX15 状态后守卫会报 `a230_conflict_not_recorded AX15`。按 A201 / A158 同步改为 `DataLayer` 并改注释；单独双向验证：改回 `Planned` 得 `PROJECTION_GUARD_FAIL reason=a230_conflict_not_recorded AX15`、恢复得 `PROJECTION_GUARD_OK`。`scripts/ax_guard.py` 显式断言表加 `'AX15'`，`src/core/ax.rs` 测试断言同步为 `DataLayer 21` / `Planned 2`。

`studio_image_guard.py` 双向注入首跑 41 组得 `true_fail=40 / fake_ok=1`：`classify_table` 注入把 `for (prefix, code) in PATH_KINDS` 改成 `PATH_KINDS_X`，守卫锚点未带 `{`，子串仍匹配导致假 OK（E371 / A241 / A157）。锚点改为带花括号后 `python -m py_compile` 通过，41 组复跑 **全真 FAIL、0 假 OK、0 跳过、恢复后守卫 OK、全文件 SHA-256 复原**（A159 / A204 / A243）：覆盖五张表逐值、两 impl 段 code/parse、`Component` 路径校验、`classify_target` 显式表、`entry_consistent` 五条函数体与八处调用、纯查询段、坏输入标签边界、单条突变八入口、批量禁令、原子写、统一信封、载荷 10 键、用户文本、`api::v1` 面、AX15 状态 / slug / conflict、A230 两项排除留痕、boot 模块、mod 声明、CI step。`r'\b'` 边界沿用 `(?!\w)` 修正（E361）。A243：守卫 FAIL 但行为测试仍通过的约束（A230 排除留痕、批量禁令、载荷十键）如实登记「由守卫持有」，不改测试凑失败、不降守卫断言。

CI 三 job 按 A116 实跑真实命令：`credential` → `NO_CREDENTIAL`（全仓字节扫描 HITS 0、`git grep` tracked 0 命中、`ci.yml` 0 命中）；`wording` → `NO_EXPLANATORY`；`hardcode` → `NO_HARDCODE`。`scripts/__pycache__/` 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1` 复跑。`panic_guard` / `i18n_guard` / `api_guard` 全仓扫描型守卫 0 FAIL（A271：新测试标识符先核禁用字面量表，避开 `api_guard.py` 的 `catalog()` 等）。

`demos/round-091-studio-image.html` 的 JS `new Function()` 语法检查通过，五数组均 16 项对齐（A265）；`docs/index.md` 必读清单逐文件核存在非空。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| A249 四件套 | 085 / 086 / 087 / 088 / 089 / 090 / 091 的 spec、readback、decision、verification、demo 全部齐；`delivery_guard.py` G1–G8 全过 |
| 091 占位符 | 0 |
| `api::v1` | 7 符号 / 4 条 `pub use` 不变（A246） |
| AX15 | `DataLayer`，`conflict` 空；`Planned 2` / `DataLayer 21` / `GateOnly 1` |
| A230 排除留痕 | AX07 `Planned` / `network_io_not_started`、AX22 `Planned` / 空，由双守卫显式断言 |
| 零新增第三方 | `Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff；26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| 全仓凭据 | `NO_CREDENTIAL`；`scripts/__pycache__/` 0 项；临时注入脚本用后即删 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| 091 决策 G3 | `## 2. 时间戳` / `## 9. 自我批判` / `## 10. 四值` 行首精确匹配（A268） |
| 提交与推送 | 主快照 hash、文件数、逐项 ALL_MATCH 写进 `docs/records/rounds.md` 091 补记（A206）；见第 5 节 |

## 5. 提交与远端核对

091 按 A254 提交前 `ps -eo pid,cmd` 核无运行中 git 进程、无 `.git/index.lock`；按 A11 逐项核 `git status --porcelain` 全部属 091 范围，无顺手改无关文件。按 A216 用 `scripts/api_push.py` 以 `base_tree` 增量 POST 只传变化条目，`force=false`，不强推、不重写历史；推送后只读 `GET /git/ref/heads/main` 得新 ref，并用 `git ls-files -s -z` 全量 path+blob sha 与远端 recursive tree 求差集，逐项 ALL_MATCH 结果写进 `rounds.md` 091 补记。两个 zip 按 A205 重打：主 zip 用 `git ls-files -z | zip -@`，`ui-previews.zip` 用 `demos/preview/*.png` 清单，项数分别等于 tracked 数与 PNG 数，EXTRA 0 / MISSING 0。具体 hash 与数值见补记，不在推送成功前写模板值。

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因功能轮落地而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213–E371 已失败；EQ / Q / 2 项 `Planned` 未证实；真实图片像素调整与 UI 渲染未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 7，满足 | — |
| 连续二十二轮未达通过 | 069–090 连续未通过，按 `00:9.1` 应停下；用户 091「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-091-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A145 远端补验、四份原文全文回显、A230 三项冲突逐条核验、A211 AX15 八锚点、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 091 四件套、A268 G2/G3、`00:137` / `00:245` 显式核、091 占位符 0、41 组双向注入全真 FAIL、E369 修复点单独双向验证、lib 780 / 0 与分段 819 / 0、Win GNU RC=0、34 守卫 0 FAIL、CI 三 job 通过、零新增依赖、v1 不变、091 提交与推送结果见补记 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 / E356 / E357 / E360 / E361 / E363 / E366 / E367 / E369 / E370 / E371；035–047 历史格式缺失 |
| 未证实 | E362、Q-091-01 / Q-091-02 / Q-091-03、Q-082-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、Q-090-01 / Q-090-02、EQ-01 ~ EQ-13、4 条 Q-C、2 项 `Planned`、6 项低可信度转述 |
| 未启动 | 真实图片像素调整与缩放、裁剪 / 绘画 / 高亮 / 形状 / 文字 / 擦除六动作、图片预览渲染、Studio 打开入口、撤销重做栈执行层、真实 `.litematic` / `.schem` 解析、投影预览渲染、投影资源站安装、方块状态编辑、真实 mrpack / CurseForge zip 解压落盘、拖动到此处页面、实例模板克隆执行、可移植实例导出、真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载 |
| 受阻 | 无（远端 Git Data API 通道正常；2 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

## 091 补记（A245 偶发 FAILED / E373 索引锁 / E374）

502 网关截断后的分段命令首跑 `cargo test --offline --lib` 得 `779 passed; 1 failed`；复跑 3 次全量为 OK / FAILED / OK，FAILED 用例为 `core::cache::tests::single_flight_loads_once_for_concurrent_waiters`（`src/core/cache.rs:252`），属既有并发测试、与 091 新增模块无关。按 A245 单独跑该用例 3 次：S1 OK / S2 OK / S3 FAILED；再复跑全量 3 次：F1 / F2 / F3 均 `780 passed; 0 failed`。实现与测试零改动（`src/core/cache.rs` SHA-1 `614776d34e9ec901bd8b3fcd65b03edd008479b7`、`src/core/studio_image.rs` SHA-1 `bb7f9545734d2cdffcc209f85871d167de09d3bb`，`git diff --name-only` 对两文件无输出），未加跳过标记、未删测试、未改断言。E374 计入四值「已失败」。本轮 819 / 0 的分段求和取通过态各段真实输出，偶发 FAILED 如实登记，不写成「全程 0 FAILED」。502 同时留下 `.git/index.lock`（E373），按 A140 / A254 提交前删除并核无运行中 git 进程、HEAD 唯一、远端 ref 未变，不带着脏锁继续跑。

# 088 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/88-round-088-instructions.txt`（3 字节 `干`）；`docs/decisions/087-delivery-closure.md`；`docs/decisions/088-instance-import-delivery.md`；`docs/records/round-087-full-readback.md`；`docs/records/round-088-full-readback.md`；`scripts/delivery_guard.py`；`scripts/instance_import_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；088 代码上一轮落地、本轮按 A249 补齐交付并一次同步到远端 |

## 1. 原文复读

`docs/records/round-088-full-readback.md`：四份原文逐字副本（`00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt`）字节 / 行 / SHA-256 表、原文锚点、DIRTY 8 逐项复核、A145 远端补验、A248 / A266 预检、A249 形态判定、068 / 084 / 086 / 087 先例、A211 AX08 七锚点、A244 逐条对照表、`00:230` 联网核实、`00:9.1` 冲突裁决、`00:137` 接口终点与 `00:245` 通过标记条件显式核、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；`ai-errors.md` 520 行 / 55513 字节完整读、分两段回显，末条仍为 A271；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行逐行全文回显（A18 / A211 / A244）。88 号 spec 逐字 3 字节 `干`，SHA-256 `9ee0280b…`。

A145 远端补验：只读 `GET /git/ref/heads/main` RC=200 得 `d5a8427f1426d24f8d8d6054cec2e8a2b4588ecf`（087 补记，parent `247e765`），完整 recursive tree `LOCAL 1260 / REMOTE 1260 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；本地 HEAD `b7c6d70`、DIRTY 8、无锁、无运行中 git 进程、PYC 0。按 A142 逐项核 8 项 DIRTY：5 项修改（ci.yml / ax_guard.py / ax.rs / boot.rs / mod.rs）+ 3 项新增（88 号 spec / instance_import_guard.py / instance_import.rs），全部属 AX08 落地范围，无顺手改无关文件（A11）。088 四件套、台账、提交、推送、zip、最终回复全部缺失（E360）。

A266 本轮复核：按 `72-round-072-instructions.txt` 逐字澄清与 A266，平台拼入用户位次的文本不作用户当轮指令、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080–087 已按同一口径补记，历史不重写。工具从未禁用。

`00:230` 本轮真执行：`TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` 得 `Tue Nov 24 00:02:16 CST 2026`；`GET /git/ref/heads/main` RC=200 得 `d5a8427…`；上游状态复核 082 的 `ViaVersion/ViaNBT` 不变，085–088 零新增上游依赖。

A211 本轮真读全文复核的 AX08 七锚点：`11:15` / `11:222` 整合包一键安装拖到主界面、`11:21` 拖动到此处页面、`12:35` mrpack / CurseForge zip 导入导出、`12:36` 拖拽安装模组 / 插件、`12:40` 实例模板与克隆、`12:41` 实例导出 / 导入。按 A267 核 `src/core/ax.rs:24–39` 真实 slug 与 conflict，AX08 `instance_import` / `DataLayer` / conflict 空 / ui true，`Planned 4`、`DataLayer 19`、`GateOnly 1`。按 A217 核 `src/core/` 已有 `instance.rs` / `instance_drop.rs`（070 语义不同）与 AX08 新落 `instance_import.rs`。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib`（088 回归） | **715 / 0**（RC=0 / 0.38 s，`src/` 零改动；687 → 715，新增 28 单测） |
| 集成段 1（088 实跑） | **26 / 0**（6 + 7 + 7 + 6，RC=0） |
| `cargo test --offline --doc`（088 实跑） | **0 / 0**（RC=0） |
| 全量 `cargo test --offline` | **754 / 0**（分段求和） |
| Windows GNU 交叉检查（085 实测） | **通过 / RC=0 / 29.02 s / 零 warning** |

全量 **754 / 0** 为分段求和（A252），各段真实输出：

| 段 | 命令 | 通过 |
| --- | --- | --- |
| lib | `cargo test --offline --lib` | 715 |
| 集成 1 | `--test boot_fallback --test http_construct --test play_stats --test window_handle_contract` | 6 + 7 + 7 + 6 = 26 |
| 集成 2 | `--test plugin_lifecycle_load` | 7（085 原始输出 60.39 s） |
| 集成 3 | `--test plugin_abi_load` | 6（085 原始输出 147.88 s） |
| doc | `cargo test --offline --doc` | 0 |
| 交叉检查 | `cargo check --offline --target x86_64-pc-windows-gnu` | RC=0 / 29.02 s（085 原始输出） |

088 实跑 lib / 集成段 1 / doc（RC 均为 0）；集成段 2 / 3 与 Win GNU 取 085 原始输出，`src/` 零改动未重跑，不写成单条 `cargo test --offline` 的输出（A15 / A252）。`tests/` 真实文件名按 A176 核为 6 个。088 `src/` 零改动，715 个断言一字未改、未加跳过标记、未删测试（`00:9.2` / A16）。085 的 E350 / E351 仍计入四值「已失败」，不包装成已处理。

## 3. 守卫与 CI

088 复扫 32 个守卫（31 个 `scripts/*_guard.py` 加 `scripts/p09_scan.py`）。落 88 号 spec 后 `delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-088-full-readback.md`（A249），补齐 088 四件套后 `DELIVERY_GUARD_OK rounds=[… 85, 86, 87, 88] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step`，32 守卫 0 FAIL。

`scripts/instance_import_guard.py` 挂 `.github/workflows/ci.yml` `scan` job。首轮双向注入 36 组得 `true_fail=29 fake_ok=5 skipped=2`：5 个假 OK 落在 `classify_path` 表名、`entry_consistent` 检查、`ci_step` name、事件载荷键、坏输入标签五处子串 `in` / 只数数量断言；2 个跳过为锚点不唯一与重复用例。按 A241 / A269 / A270 修守卫 5 处（精确正则表形态、`(?!\w)` 边界、CI step 行首匹配、载荷键 `PAYLOAD_EXPECTED` 逐值、坏输入标签边界）；首次边界修法 `r'\b'` 误判 `i.kind != classify_path(&i.path)` 末尾 `)`，守卫正常态 FAIL `entry_consistent_check_missing`，改 `(?!\w)` 后正常态 `INSTANCE_IMPORT_GUARD_OK root_keys=4 entry_keys=6 formats=4 kinds=5 actions=5 states=3 path_kinds=4 four_impl_literals_match component_path_check consistent_checks_five calls=6 pure_queries event_payload=10 v1_unchanged ax08=DataLayer planned=4 data=19`。`python -m py_compile` 通过（A251）、`scripts/__pycache__/` 已清理。

重跑注入 **34 组全真 FAIL、0 假 OK、0 跳过、恢复后守卫 OK、七文件 SHA-256 复原**（A159 / A204 / A243）：覆盖七张表逐值、四 impl 段 code/parse、`Component` 路径校验、`classify_path` 显式表、`entry_consistent` 五条函数体与六处调用、纯查询段、坏输入标签、单条突变八入口、pending 闸门、单步推进、批量禁令、原子写、统一信封、载荷 10 键、用户文本、`api::v1` 面、AX08 状态 / slug / conflict、boot 模块、mod 声明、CI step。E361 计入四值「已失败」。

跨守卫一组：注入 `scripts/ax_guard.py` 删去 `'AX08'` 后仍 `AX_GUARD_OK specs=24 data_layer=19 planned=4`，动态列表无独立 EXPECTED（E362），本轮不修历史守卫，AX08 状态另由 `instance_import_guard.py:261–272` 独立核 `name` / `state` / `conflict` 与 24 行分布，双守卫互补；E362 计入未证实。

CI 三 job 按 A116 实跑真实命令：`credential` → `NO_CREDENTIAL`（`git grep` tracked 0 命中、`ci.yml` 0 命中）；`wording` → `NO_EXPLANATORY`；`hardcode` → `NO_HARDCODE`。`scripts/__pycache__/` 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1` 复跑。

`demos/round-088-instance-import.html` 的 JS `new Function()` 语法检查通过，五数组均 16 项对齐（A265）；`docs/index.md` 必读清单逐文件核存在非空。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| A249 四件套 | 085 / 086 / 087 / 088 的 spec、readback、decision、verification、demo 全部齐；`delivery_guard.py` G1–G8 全过 |
| 088 占位符 | 0 |
| `api::v1` | 7 符号 / 4 条 `pub use` 不变；088 `src/` 零改动 |
| AX08 | `DataLayer`，`conflict` 空；`Planned 4` / `DataLayer 19` / `GateOnly 1` |
| 零新增第三方 | `Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff；26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| 全仓凭据 | `NO_CREDENTIAL`；`scripts/__pycache__/` 0 项；临时注入脚本用后即删 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| 088 决策 G3 | `## 2. 时间戳` / `## 9. 自我批判` / `## 10. 四值` 行首精确匹配（A268） |
| 提交与推送 | 主快照 hash、文件数、逐项 ALL_MATCH 写进 `docs/records/rounds.md` 088 补记（A206）；见第 5 节 |

## 5. 提交与远端核对

088 按 A254 提交前 `ps -eo pid,cmd` 核无运行中 git 进程、无 `.git/index.lock`；按 A11 逐项核 `git status --porcelain` 全部属 088 范围。按 A216 用 `scripts/api_push.py` 以 `base_tree` 增量 POST 只传变化条目，`force=false`，不强推、不重写历史；推送后只读 `GET /git/ref/heads/main` 得新 ref，并用 `git ls-files -s -z` 全量 path+blob sha 与远端 recursive tree 求差集，逐项 ALL_MATCH 结果写进 `rounds.md` 088 补记。两个 zip 按 A205 重打：主 zip 用 `git ls-files -z | tr '\0' '\n' | zip -@`，`ui-previews.zip` 用 `demos/preview/*.png` 清单，项数分别等于 tracked 数与 PNG 数，EXTRA 0 / MISSING 0。具体 hash 与数值见补记，不在推送成功前写模板值。

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层闭环而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213–E361 已失败；E362 / EQ / Q / 4 项 `Planned` 未证实；真实解压落盘与 UI 渲染未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 7，满足 | — |
| 连续十九轮未达通过 | 069–087 连续未通过，按 `00:9.1` 应停下；用户 088「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-088-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A145 远端补验、A142 DIRTY 8 复核、四份原文全文回显、A211 AX08 七锚点、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 088 四件套、068 / 084 / 086 / 087 先例判定、`00:137` / `00:245` 显式核、088 占位符 0、34 组双向注入全真 FAIL、lib 715 / 0 与分段 754 / 0、Win GNU RC=0、32 守卫 0 FAIL、CI 三 job 通过、零新增依赖、v1 不变、088 提交与推送结果见补记 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 / E356 / E357 / E360 / E361；035–047 历史格式缺失 |
| 未证实 | E362、Q-082-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、EQ-01 ~ EQ-13、4 条 Q-C、4 项 `Planned`、6 项低可信度转述 |
| 未启动 | 真实 mrpack / CurseForge zip 解压落盘、拖动到此处页面渲染、实例模板克隆执行、可移植实例导出、真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载 |
| 受阻 | 无（远端 Git Data API 通道正常；4 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

089 补记（088 推送状态覆盖）：088 决策写「受阻 | 无（远端 Git Data API 通道正常）」与「088 提交与推送结果见补记」，均为 088 推送前判断。088 末段三次调用 `api_push.py` 被网关超时截断（工具结果 `sandbox call failed` / `context deadline exceeded`），每次截断后只读核远端 ref 均未变；089 开轮 A145 补验远端 `d5a8427` / `LOCAL 1267 / REMOTE 1260 / DIFF 18 / ALL_MATCH False`。按 A206 / A209 写「受阻、ALL_MATCH 本轮不成立」，E363 计入四值「已失败」，不包装成已处理。088 补记（推送后真实值）未写；089 按 A145 补验远端未变后合并重推，推送成功且逐项 ALL_MATCH 前该结论保持（A201，历史行不重写）。
089 补记之二（088 交付层闭环）：088 阶段三次 `api_push.py` 被网关超时截断、远端 `d5a8427` / DIFF 18 / ALL_MATCH False。089 按 A145 补验远端未变后合并推送，远端 `b08c268` / `1272 / 1272 / ALL_MATCH True`，088 补记（受阻登记）与 089 四件套一并入远端，受阻状态解除；E363 三次网关超时仍计入四值「已失败」，不包装成已处理（A201，历史行不重写）。

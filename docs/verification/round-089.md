# 089 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/89-round-089-instructions.txt`（3 字节 `干`）；`docs/decisions/088-instance-import-delivery.md`；`docs/decisions/089-delivery-closure.md`；`docs/records/round-088-full-readback.md`；`docs/records/round-089-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；088 补记与 089 四件套按 A145 / A249 一次同步到远端 |

## 1. 原文复读

`docs/records/round-089-full-readback.md`：四份原文逐字副本（`00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt`）字节 / 行 / SHA-256 表、原文锚点、088 推送未成状态、A145 远端补验、A248 / A266 预检、A249 形态判定、068 / 084 / 086 / 087 先例、A211 AX08 七锚点复核、A244 逐条对照表、`00:230` 联网核实、`00:9.1` 冲突裁决、`00:137` 接口终点与 `00:245` 通过标记条件显式核、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；`ai-errors.md` 520 行 / 55513 字节完整读、分两段回显，末条仍为 A271；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行逐行全文回显（A18 / A211 / A244）。89 号 spec 逐字 3 字节 `干`，SHA-256 `9ee0280b…`。

088 闭环：本地 HEAD `6f1868c` / 1267 文件 DIRTY 0，88 号 spec 与 088 四件套齐、已随本地提交纳入；但 088 末段三次调用 `scripts/api_push.py` 均被网关超时截断（工具结果 `sandbox call failed` / `context deadline exceeded`），每次截断后只读核远端 ref 均未变。089 开轮 A145 补验：只读 `GET /git/ref/heads/main` 得 `d5a8427f1426d24f8d8d6054cec2e8a2b4588ecf`（087 补记，parent `247e765`），完整 recursive tree `LOCAL 1267 / REMOTE 1260 / DIFF 18 / EXTRA 0 / TRUNCATED False / ALL_MATCH False`，`DIFF_SAMPLE` 含 `.github/workflows/ci.yml` / `demos/round-088-instance-import.html` / `docs/decisions/088-instance-import-delivery.md` / `docs/index.md`。本地无锁、无运行中 git 进程、PYC 0。按 A145 / A216 先核远端 ref 未变再重推，不重复推送、不强推、不重写历史；按 A206 / A209 在推送成功且逐项 ALL_MATCH 前写「受阻、ALL_MATCH 本轮不成立」，不沿用 087 模板值。088 补记未写、两个 zip 为 087 旧包、088 无最终回复。

A266 本轮复核：按 `72-round-072-instructions.txt` 逐字澄清与 A266，平台拼入用户位次的文本不作用户当轮指令、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080–088 已按同一口径补记，历史不重写。工具从未禁用，089 正常调用工具完成提交、推送与打包。

`00:230` 本轮真执行：`TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` 得 `Tue Nov 24 00:59:25 CST 2026`；`GET /git/ref/heads/main` RC=200 得 `d5a8427…`；上游状态复核 082 的 `ViaVersion/ViaNBT` 不变，085–089 零新增上游依赖。

A211 本轮真读全文复核的 AX08 候选锚点：`11:15` / `11:21` / `11:222` / `12:35` / `12:36` / `12:40` / `12:41`。按 A267 核 `src/core/ax.rs:24–39` 的 4 项 `Planned` 真实 slug 与 conflict，`ax.rs:82` 断言 `Planned == 4`。七锚点顺延为 090 输入，089 不落地、不代拍。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib`（089 回归） | **715 / 0**（RC=0，`src/` 零改动） |
| 集成段 1（089 实跑） | **26 / 0**（6 + 7 + 7 + 6） |
| `cargo test --offline --doc`（089 实跑） | **0 / 0** |
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

089 实跑 lib / 集成段 1 / doc（RC 均为 0）；集成段 2 / 3 与 Win GNU 取 085 / 088 原始输出，`src/` 零改动未重跑，不写成单条 `cargo test --offline` 的输出（A15 / A252）。`tests/` 真实文件名按 A176 先 `ls tests/*.rs` 核实为 6 个。089 `src/` 零改动，原 715 个断言一字未改、未加跳过标记、未删测试（`00:9.2` / A16）。E350 / E351 仍计入四值「已失败」，不包装成已处理。

## 3. 守卫与 CI

`scripts/instance_import_guard.py` 挂 `.github/workflows/ci.yml` `scan` job；089 复扫 32 个守卫（31 个 `scripts/*_guard.py` 加 `scripts/p09_scan.py`），落 89 号 spec 后 `delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-089-full-readback.md`（A249），补齐 089 四件套后 `DELIVERY_GUARD_OK rounds=[… 85, 86, 87, 88, 89] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step`，32 守卫 0 FAIL。

088 的双向注入结论本轮复核不变（A159 / A204 / A243）：首轮 36 组得 29 真 FAIL / 5 假 OK / 1 跨守卫缺口 / 1 锚点跳过；修 `instance_import_guard.py` 5 处断言缺口后 **34 组全真 FAIL、0 假 OK、恢复 OK、七文件哈希复原**；`scripts/ax_guard.py` 删 `'AX08'` 后仍 OK 的历史缺口 E362 单列，AX08 状态由 `instance_import_guard.py:261–272` 独立核，双守卫互补。

CI 三 job 按 A116 实跑真实命令：`credential` → `NO_CREDENTIAL`（全仓字节扫描 HITS 0、`git grep` tracked 0 命中、`ci.yml` 0 命中）；`wording` → `NO_EXPLANATORY`；`hardcode` → `NO_HARDCODE`。`scripts/__pycache__/` 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1` 复跑，未再生成 pyc。

`demos/round-089-delivery.html` 的 JS `new Function()` 语法检查通过，五数组均 16 项对齐（A265）；`docs/index.md` 必读清单逐文件核存在非空。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| A249 四件套 | 085 / 086 / 087 / 088 / 089 的 spec、readback、decision、verification、demo 全部齐；`delivery_guard.py` G1–G8 全过 |
| 088 / 089 占位符 | 0 |
| `api::v1` | 7 符号 / 4 条 `pub use` 不变；089 `src/` 零改动 |
| AX08 | `DataLayer`，`conflict` 空；`Planned 4` / `DataLayer 19` / `GateOnly 1` |
| 零新增第三方 | `Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff；26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| 全仓凭据 | `NO_CREDENTIAL`；`scripts/__pycache__/` 0 项；临时脚本用后即删 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| 089 决策 G3 | `## 2. 时间戳` / `## 9. 自我批判` / `## 10. 四值` 行首精确匹配（A268） |
| 提交与推送 | 主快照 hash、文件数、逐项 ALL_MATCH 写进 `docs/records/rounds.md` 089 补记（A206）；见第 5 节 |

## 5. 提交与远端核对

089 按 A254 提交前 `ps -eo pid,cmd` 核无运行中 git 进程、无 `.git/index.lock`；按 A11 逐项核 `git status --porcelain` 全部属 088 覆盖补记 / 089 范围，无顺手改无关文件。按 A145 先只读核远端 ref 仍为 `d5a8427`、DIFF 18，再按 A216 用 `scripts/api_push.py` 以 `base_tree` 增量 POST 只传变化条目，`force=false`，不强推、不重写历史；推送后只读 `GET /git/ref/heads/main` 得新 ref，并用 `git ls-files -s -z` 全量 path+blob sha 与远端 recursive tree 求差集，逐项 ALL_MATCH 结果写进 `rounds.md` 089 补记。两个 zip 按 A205 重打：主 zip 用 `git ls-files -z | zip -@`，`ui-previews.zip` 用 `demos/preview/*.png` 清单，项数分别等于 tracked 数与 PNG 数，EXTRA 0 / MISSING 0。具体 hash 与数值见补记，不在推送成功前写模板值。

089 补记（推送后真实值）：主快照本地 `ec6dec9` / 1272 文件 DIRTY 0；远端 ref `b08c268c338f36ca0828aab4c49d4e729f59ed68`（`force=false`，parent `d5a8427`），23 项变化 + `base_tree=48e9e4f` 增量推送 RC=0，完整 recursive tree `1272 / 1272 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`。088 补记与 089 四件套随本次推送闭环，受阻状态解除；E363 两次以上网关超时仍计入已失败。本补记以该 ref 为父二次推送（A206，不用模板值冒充）。
## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层闭环而转通过 |
| 四值无已失败 / 未证实 / 未启动 / 受阻 | E213–E363 已失败；EQ / Q / 4 项 `Planned` 未证实；真实解压落盘与 UI 渲染未启动；088 推送未成 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 7，满足 | — |
| 连续二十轮未达通过 | 069–088 连续未通过，按 `00:9.1` 应停下；用户 089「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-089-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A145 远端补验、四份原文全文回显、A211 AX08 七锚点复核、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 089 四件套、068 / 084 / 086 / 087 先例判定、`00:137` / `00:245` 显式核、088 / 089 占位符 0、088 双向注入 34 组全真 FAIL、lib 715 / 0 与分段 754 / 0、Win GNU RC=0、32 守卫 0 FAIL、CI 三 job 通过、零新增依赖、v1 不变、089 提交与推送结果见补记 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 / E356 / E357 / E360 / E361 / E363；035–047 历史格式缺失 |
| 未证实 | E362、Q-082-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、EQ-01 ~ EQ-13、4 条 Q-C、4 项 `Planned`、6 项低可信度转述 |
| 未启动 | 真实 mrpack / CurseForge zip 解压落盘、拖动到此处页面渲染、实例模板克隆执行、可移植实例导出、真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载 |
| 受阻 | 088 三次推送被网关超时截断，远端 `d5a8427` / DIFF 18 / ALL_MATCH False；089 按 A145 补验后合并重推，推送成功且逐项 ALL_MATCH 前该结论保持（A206 / A209） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动 / 受阻项，不发通过标记。

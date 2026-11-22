# 084 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/84-round-084-instructions.txt`（3 字节 `干`）；`docs/decisions/082-world-editor.md`；`docs/decisions/083-delivery-reconciliation.md`；`docs/decisions/084-delivery-closure.md`；`docs/records/round-082-full-readback.md`；`docs/records/round-083-full-readback.md`；`docs/records/round-084-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；082 / 083 / 084 三套四件套按 A249 一次交齐并一次同步到远端 |

## 1. 原文复读

`docs/records/round-084-full-readback.md`：四份原文逐字副本（`00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt`）字节 / 行 / SHA-256 表、原文锚点、083 未闭环状态、A145 远端补验、A248 / A266 预检、A249 形态判定、068 先例、A211 AX04 锚点、A244 逐条对照表、`00:230` 联网核实、`00:9.1` 冲突裁决、A164 逐条分已决断 / 未决断、`00:137` 接口终点与 `00:245` 通过标记条件显式核、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；`ai-errors.md` 520 行 / 55513 字节完整读、分两段回显，末条仍为 A271；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行逐行全文回显（A18 / A211 / A244）。84 号 spec 逐字 3 字节 `干`，SHA-256 `9ee0280b…`。

082 闭环：末条工具结果被网关截断，按 A145 只读 `GET /git/ref/heads/main` 得 `c15a4700a220bc6142fe5938a600abd79df6565b`（081 补记，parent `8e521ae`），完整 recursive tree `1226 / 1226 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；本地 HEAD `b462dd3`、DIRTY 13、无锁、无运行中 git 进程。083 收口轮补齐 082 四件套 25 个占位符、083 四件套、台账、28 组双向注入、CI 三 job；083 末条工具结果同样被网关截断，083 全轮无最终回复，HEAD 仍 `b462dd3`、DIRTY 24、未提交未推送、zip 为 081 轮 15:09 旧包。084 按 A145 再次只读补验同一 ref 与完整 tree，不重复推送、不强推、不重写历史。

A266 本轮复核：按 `72-round-072-instructions.txt` 逐字澄清与 A266，平台拼入用户位次的文本不作用户当轮指令、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080 / 081 / 082 / 083 已按同一口径补记，历史不重写。工具从未禁用，084 正常调用工具完成提交、推送与打包。

`00:230` 本轮真执行：`TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` 得 `Mon Nov 23 00:38:45 CST 2026`；`GET /git/ref/heads/main` RC=200 得 `c15a470…`；上游状态复核 082 的 `ViaVersion/ViaNBT`（`pushed_at=2026-10-27T14:24:29Z`、`archived=false`、tags 三项）不变，084 零新增上游依赖。

A211 本轮真读全文找出的 AX04 已决断锚点：`11:244` 第 36 条（同版本警告、高版本由用户选择版本后替换、顺序页码弹窗、每个单独选择）、`12:8`（高版本自动禁用低版本 jar，单个实例页面）、`12:33`（配置快照与回滚）、`12:39`（服务端/加载器版本回滚）；按 A267 核 `src/core/ax.rs:21` 真实 name `mod_rollback`、conflict 为空。锚点登记为 085 输入，084 不落地 AX04。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib`（084 回归） | **668 / 0**（RC=0，0.37 s，`src/` 零改动） |
| 082 首跑 lib | 668 / 0（新增 18 单测，650 → 668） |
| 082 lib 复跑 3 次 | 第 1 次 667 / 1 偶发并发 FAILED（`core::cache::tests::single_flight_loads_once_for_concurrent_waiters` / `src/core/cache.rs:252`）；第 2 / 3 次 668 / 0；A245 单独跑 3 次该用例与复跑 3 次全量均 0 FAILED，`src/core/cache.rs` 零 diff、SHA-1 `614776d34e9ec901bd8b3fcd65b03edd008479b7` |
| 全量 `cargo test --offline` | **707 / 0**（分段求和） |
| Windows GNU 交叉检查 | **通过 / RC=0 / 24.23 s / 零 warning** |

全量 **707 / 0** 为分段求和（A252），各段真实输出：

| 段 | 命令 | 通过 |
| --- | --- | --- |
| lib | `cargo test --offline --lib` | 668 |
| 集成 1 | `--test boot_fallback --test http_construct --test play_stats --test window_handle_contract` | 6 + 7 + 7 + 6 = 26 |
| 集成 2 | `--test plugin_lifecycle_load` | 7（23.35 s） |
| 集成 3 | `--test plugin_abi_load` | 6（69.10 s） |
| doc | `cargo test --offline --doc` | 0 |
| 交叉检查 | `cargo check --offline --target x86_64-pc-windows-gnu` | RC=0 / 24.23 s |

`tests/` 真实文件名按 A176 先 `ls tests/*.rs` 核实为 6 个。084 `src/` 零改动，原 668 个断言一字未改、未加跳过标记、未删测试（`00:9.2` / A16）。E340 仍计入四值「已失败」，不包装成已处理。

## 3. 守卫与 CI

`scripts/world_editor_guard.py` 挂 `.github/workflows/ci.yml` `scan` job；084 复扫 30 个守卫，落 84 号 spec 后 `delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-084-full-readback.md`（A249），补齐 084 四件套后 `DELIVERY_GUARD_OK rounds=[… 82, 83, 84] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step`，30 守卫 0 FAIL。

083 补跑的双向注入 28 组结论本轮复核不变（A159 / A204 / A243）：覆盖七表逐值、五 impl 段、A247 复用、坏输入标签、`VERIFIED_LICENSE` 单值、矛盾态函数体、事件载荷用户文本、禁用字面量、统一信封、未知键拒收、纯查询段、单条突变、保护清单、原子写、枚举边界、载荷计数、AX03 状态、boot 模块、CI step、v1 面、ax_guard、显式 Vec 类型、矛盾态调用计数；**28 组全真 FAIL、0 假 OK**，恢复后 `WORLD_EDITOR_GUARD_OK`、六文件哈希复原。

CI 三 job 按 A116 实跑真实命令：`credential` → `NO_CREDENTIAL`（083 已清理 `scripts/__pycache__/download_sources_guard.cpython-312.pyc`，084 守卫统一 `PYTHONDONTWRITEBYTECODE=1` 复跑，未再生成该产物）；`wording` → `NO_EXPLANATORY`；`hardcode` → `NO_HARDCODE`。`git grep -lE` 扫 tracked 0 命中、`.git/config` 0 命中。全量措辞扫描（`src/ demos/ docs/records/ docs/decisions/ scripts/`）17 命中全在 066–082 的历史 readback 与 `063-axolotl-survey.md`，均为引用 `00:6.1` 规则时出现的「设计动机」字面量；084 新增文档零命中，历史行按 A181 不重写，如实登记。CI `wording` job 只扫 `src/`，结论 `NO_EXPLANATORY` 不受影响。

三套演示 `demos/round-082-world-editor.html` / `demos/round-083-delivery.html` / `demos/round-084-delivery.html` 的 JS `new Function()` 语法检查通过，五数组均 16 项对齐（A265）；`docs/index.md` 必读清单逐文件核存在非空。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| A249 三套四件套 | 082 / 083 / 084 的 spec、readback、decision、verification、demo 全部齐；`delivery_guard.py` G1–G8 全过 |
| 082 占位符 | 25 个 `@…@` → 0（`grep -rho '@[A-Z_]*@'` 复核），全填真实命令输出 |
| `api::v1` | 7 符号 / 4 条 `pub use` 不变；084 `src/` 零改动 |
| AX03 | `DataLayer`，`conflict` 空；`Planned 6` / `DataLayer 17` / `GateOnly 1` |
| 零新增第三方 | `Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff；26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| 全仓凭据 | `NO_CREDENTIAL`；`scripts/__pycache__/` 0 项；临时脚本用后即删 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| 083 / 084 决策 G3 | `## 2. 时间戳` / `## 9. 自我批判` / `## 10. 四值` 行首精确匹配（A268） |
| 提交与推送 | 主快照 hash、文件数、逐项 ALL_MATCH 写进 `docs/records/rounds.md` 084 补记（A206）；见第 5 节 |

## 5. 提交与远端核对

084 按 A254 提交前 `ps -eo pid,cmd` 核无运行中 git 进程、无 `.git/index.lock`；按 A11 逐项核 `git status --porcelain` 24 项（10 项修改 + 14 项新增）全部属 082 / 083 / 084 范围，无顺手改无关文件。按 A216 用 `scripts/api_push.py` 以 `base_tree` 增量 POST 只传变化条目，`force=false`，不强推、不重写历史；推送后只读 `GET /git/ref/heads/main` 得新 ref，并用 `git ls-files -s -z` 全量 path+blob sha 与远端 recursive tree 求差集，逐项 ALL_MATCH 结果写进 `rounds.md` 084 补记。两个 zip 按 `git ls-files -z | zip -@` 重打，项数等于 tracked 数，EXTRA 0 / MISSING 0（A205）。具体 hash 与数值见补记，不在推送成功前写模板值。

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层闭环而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213–E346 已失败；EQ / Q / 6 项 `Planned` 未证实；真实 NBT 读取写回与 UI 渲染未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 7，满足 | — |
| 连续十五轮未达通过 | 069–083 连续未通过，按 `00:9.1` 应停下；用户 084「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-084-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A145 三次远端补验、四份原文全文回显、A211 AX04 四锚点、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 三套四件套、068 先例判定、`00:137` / `00:245` 显式核、082 占位符 25 → 0、083 双向注入 28 组全真 FAIL、lib 668 / 0 与分段 707 / 0、Win GNU RC=0、30 守卫 0 FAIL、CI 三 job 通过、零新增依赖、v1 不变、084 提交与推送结果见补记 |
| 已失败 | E349（084 综合验证首次截断 + `dubious ownership` 假 DIRTY 0，拆短命令重跑后真实 28 项）、E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349；035–047 历史格式缺失 |
| 未证实 | Q-082-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、EQ-01 ~ EQ-13、4 条 Q-C、6 项 `Planned`、6 项低可信度转述 |
| 未启动 | 真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、存档编辑 UI 渲染、真实连接建立、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载、zip / 投影解析 |
| 受阻 | 无（远端 Git Data API 通道正常；6 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

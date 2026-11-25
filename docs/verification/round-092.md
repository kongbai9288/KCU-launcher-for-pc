# 092 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/92-round-092-instructions.txt`（3 字节 `干`）；`docs/decisions/091-studio-image.md`；`docs/decisions/092-pending-decisions.md`；`docs/records/round-091-full-readback.md`；`docs/records/round-092-full-readback.md`；`scripts/delivery_guard.py`；`scripts/pending_decisions_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；A230 冲突逐条核；092 清单 / 守卫 / 四件套一次同步到远端 |

## 1. 原文复读

`docs/records/round-092-full-readback.md`：四份原文逐字副本（`00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt`）字节 / 行 / SHA-256 表、原文锚点、A145 远端补验、A208 / A202 复核、A230 / A267 两项冲突、A211 / A164 已决断与未决断分列、A202 核出的 E375 口径偏差、A244 / `00:230` / `00:137` / `00:245` 显式核、A249 形态。`00-requirements.txt` 全文 261 行 / 16422 字节回显；`ai-errors.md` 520 行 / 55513 字节完整读（1–496 行回显、490–520 行补读），末条仍为 A271；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行逐行全文回显（A18 / A211 / A244）。92 号 spec 逐字 3 字节 `干`，SHA-256 `9ee0280b…`，与 91 号同形态（A34 不重复落盘、不建 93 号）。

A145 远端补验：只读 `GET /git/ref/heads/main` RC=200 得 `1ec52d5ad0adc00a1daa1e6f0d345af8874b3a0e`（091 补记，parent `24d27e1`），完整 recursive tree `LOCAL 1286 / REMOTE 1286 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；本地 HEAD `bc35c7b`、DIRTY 0、无锁、无运行中 git 进程、PYC 0。按 A145 / A216 远端写入以 `base_tree` 增量、`force=false`，不强推、不重写历史。

A266 本轮复核：平台拼入用户位次的文本不作用户当轮指令、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080–091 已按同一口径补记，历史不重写。工具从未禁用。

`00:230` 本轮真执行：`TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` 得 `Thu Nov 26 00:13:08 CST 2026`；`GET /git/ref/heads/main` RC=200 得 `1ec52d5…`；082 的 `ViaVersion/ViaNBT` 上游状态不变，085–092 零新增上游依赖。

A202 / A208 复核：打开 `091-studio-image.md:112` 与 `ax-feature-pool.md` 091 补记，091 唯一下一步为「092 改走拍板闭环……把 Q-091-01 / 02 / 03、历史 Q 与 EQ-01 ~ EQ-13、4 条 Q-C 摊平给用户拍板；按 A208 不擅自开工硬做，也不擅自定 2 项之间的优先级」。复核 `b-class-status-recheck.md:85`：EQ-01 ~ EQ-13 与 4 项待拍板仍「未证实（待拍板）」，B04 卡 EQ-01、B07 卡 EQ-05、B09 卡 EQ-11，本轮不碰 UI 渲染层（A100），无「可绕过拍板先落实现」的层。

A230 逐条核冲突：按 A267 读 `src/core/ax.rs:20–43`，AX07 `doh_support` / `Planned` / `network_io_not_started` / `ui=false`；AX22 `shimu_account` / `Planned` / 空 conflict / `ui=true`；AX23 `client_ai_gate` 为 `GateOnly`。AX07 的 `31-axolotl-launcher-features.md:35` 写「真实网络 IO 未启动、Win7 TLS 前置（EQ-03）」，00 / 11 / 12 号全文无 DoH 锚点 → 技术受阻非需求冲突，排除留痕、conflict 保持；AX22 浏览器授权依赖真实网络 IO + 第三方端点 + `11:7` / 054 境外限制 + `11:18` API 不共有 → 排除留痕。两项保持 `Planned`，不擅自定优先级。

A202 核出的口径偏差 E375：091 结尾写「4 条 Q-C」，打开 `pending-question-environments.md` 尾部、`c-class-default-recheck.md`、`b-class-status-recheck.md:85`、`055-c-class-recheck.md:63` 逐字核：真实待拍为 Q-C01 / Q-C02 / Q-C08 三条 Q-C 加一条 Q-037-01（插件哈希口径，关联 EQ-02），共 4 项；`open-questions.md` 里 Q-C01 ~ Q-C15 共 15 条，其中 12 条已证实 / 已答复，不重开。092 清单按「3 条 Q-C + Q-037-01 共 4 项」写，历史行不重写（A181 / A201）。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib`（092 实跑） | **780 / 0**（RC=0 / 0.34 s） |
| 集成段 1（092 实跑） | **26 / 0**（6 + 7 + 7 + 6，RC=0） |
| `cargo test --offline --doc`（092 实跑） | **0 / 0**（RC=0） |
| 全量 `cargo test --offline` | **819 / 0**（分段求和） |
| Windows GNU 交叉检查（085 实测） | **通过 / RC=0 / 29.02 s / 零 warning** |

全量 **819 / 0** 为分段求和（A252），各段真实输出：

| 段 | 命令 | 通过 |
| --- | --- | --- |
| lib | `cargo test --offline --lib` | 780（092 实跑 `test result: ok. 780 passed; 0 failed`） |
| 集成 1 | `--test boot_fallback --test http_construct --test play_stats --test window_handle_contract` | 6 + 7 + 7 + 6 = 26（092 实跑四行 `test result: ok.`） |
| 集成 2 | `--test plugin_lifecycle_load` | 7（085 原始输出 60.39 s） |
| 集成 3 | `--test plugin_abi_load` | 6（085 原始输出 147.88 s） |
| doc | `cargo test --offline --doc` | 0（092 实跑） |
| 交叉检查 | `cargo check --offline --target x86_64-pc-windows-gnu` | RC=0 / 29.02 s（085 原始输出） |

092 实跑 lib / 集成段 1 / doc（RC 均为 0，`src/` 零改动）；集成段 2 / 3 与 Win GNU 取 085 / 088 原始输出，未重跑，不写成单条 `cargo test --offline` 的输出（A15 / A252）。`tests/` 真实文件名按 A176 先 `ls tests/*.rs` 核实为 6 个。092 首跑 lib 即 `780 passed; 0 failed`，未触发 A245 的偶发并发 FAILED；E374 仍按 091 登记保留在四值「已失败」。既有 780 断言一字未改、未加跳过标记、未删测试。

## 3. 守卫与 CI

`scripts/pending_decisions_guard.py` 挂 `.github/workflows/ci.yml` `scan` job。092 复扫 35 个守卫（34 个 `scripts/*_guard.py` 加 `scripts/p09_scan.py`）。落 92 号 spec 后 `delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-092-full-readback.md`，补齐 readback 后为 `DELIVERY_GUARD_FAIL reason=G3 decision_missing 92`，补齐 092 四件套后 `DELIVERY_GUARD_OK rounds=[… 89, 90, 91, 92] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step`（A249 / A268）。

`pending_decisions_guard.py` 双向注入 **20 组全真 FAIL、0 假 OK、0 跳过、恢复后守卫 OK、全文件 SHA-256 复原**（`INJECT092 total=20 true_fail=20 fake_ok=0 skipped=0 restored_all=True`，A159 / A204 / A243）：覆盖 092 段标题、C 组 EQ 表 13 行逐值解析、Q-091 三条、4 项 Q-C、AX07 / AX22 锚点、`12:63` / `11:18` 原文锚点、EQ-14 / EQ-15 闭合句、A164 两个分列标题、A73 四要素表头与 `耦合` 字面量、状态词、不代拍禁词、AX07 状态与 conflict、CI step、`api::v1` 稳定面、D-092 逐值回显。守卫不靠全文子串（A241 / A270）：C 组表按 `^\| (EQ-\d\d) \|[^\n]*\| 未证实（待拍板） \|$` 逐行解析后与 EXPECTED 集合比对；A 组四要素表头按精确行核；闭合句按精确串核；decision 文件缺文件时返回明确 FAIL 而非 traceback（A10）。A243：守卫 FAIL 但行为测试仍通过的约束（清单完整性、不代拍、AX 状态）如实登记「由守卫持有」，不改测试凑失败、不降守卫断言。

`demos/round-092-pending-decisions.html` 的 JS `new Function()` 语法检查通过，NODES / LOG / MINI1 / MINI2 / MINI3 均 16 项对齐（A265）；`docs/index.md` 必读清单逐文件核存在非空。CI 三 job 按 A116 实跑真实命令，输出见第 5 节补记。`scripts/__pycache__/` 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1` 复跑。`panic_guard` / `i18n_guard` / `api_guard` 全仓扫描型守卫 0 FAIL（092 `src/` 零改动，A271 不触发）。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| A249 四件套 | 085–092 的 spec、readback、decision、verification、demo 全部齐；`delivery_guard.py` G1–G8 全过 |
| 092 占位符 | 0 |
| `api::v1` | 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/` / `Cargo.*` / `vendor/` | 零 diff；无新增模块、无新增测试标识符 |
| 功能池 | AX07 / AX22 保持 `Planned`，AX07 conflict 保持 `network_io_not_started`；`Planned 2` / `DataLayer 21` / `GateOnly 1` |
| 清单口径 | EQ-01 ~ EQ-13 共 13 条待拍；EQ-14 / EQ-15 已关闭；3 条 Q-C + Q-037-01 共 4 项；31 条历史 Q 按轮次分组；A164 已决断 / 未决断分列 |
| 零新增第三方 | 26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| 全仓凭据 | 见第 5 节补记；`scripts/__pycache__/` 0 项；临时生成脚本用后即删 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| 092 决策 G3 | `## 2. 时间戳` / `## 9. 自我批判` / `## 10. 四值` 行首精确匹配（A268） |
| 提交与推送 | 主快照 hash、文件数、逐项 ALL_MATCH 写进 `docs/records/rounds.md` 092 补记（A206）；见第 5 节 |

## 5. 提交、远端核对与 CI 三 job 实跑

092 按 A254 提交前 `ps -eo pid,cmd` 核无运行中 git 进程、无 `.git/index.lock`；按 A11 逐项核 `git status --porcelain` 全部属 092 范围。按 A216 用 `scripts/api_push.py` 以 `base_tree` 增量 POST 只传变化条目，`force=false`，不强推、不重写历史；推送后只读 `GET /git/ref/heads/main` 得新 ref，并用完整 recursive tree 求差集，逐项 ALL_MATCH 结果写进 `rounds.md` 092 补记。两个 zip 按 A205 重打：主 zip 用 `git ls-files -z | zip -@`，`ui-previews.zip` 用 `demos/preview/*.png` 清单。推送真实结果：本地提交 `df6170e`（`round 092: pending decisions flattened, guard and delivery`，14 项 staged、TRACKED 1286 → 1292、DIRTY 0、无锁）；远端 `GET /git/ref/heads/main` → `d65c0d1a3be2abd62065d3d550b28b46174a4261`，parent `1ec52d5`，message 与本地一致；`api_push.py` 输出 `remote blob 1292 OK concurrent=8 remote_reused=1153` / `remote tree main INCREMENTAL changes=14 base_tree=79f4398` / `remote push main OK commit=d65c0d1 files=1292 via=git_data_api`，RC=0、`force=false`。完整 recursive tree 复核 `LOCAL 1292 / REMOTE 1292 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`（A145 / A206，逐项写实际结果，不用模板值）。

CI 三 job 按 A116 实跑 `ci.yml` 真实命令：`credential` → `NO_CREDENTIAL`（全仓字节扫描 1292 文件 hits 0、`git grep -lE` tracked 0 命中、`ci.yml` 0 命中）、`wording` → `NO_EXPLANATORY`、`hardcode` → `NO_HARDCODE`。092 新文件宽口径措辞扫描 0 命中、占位符 0、`scripts/__pycache__/` 0 项。A11 逐项核 `git status --porcelain` 14 项全部属 092 范围，`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff（A208 不擅自开工）。

两个 zip 按 A205 重打：主包 `git ls-files | zip -q -@` 1292 项、`ui-previews.zip` 按 `demos/preview/*.png` 清单 56 项，`MAIN_DIFF 0 / EXTRA 0 / MISSING 0 / PREVIEW_DIFF 0 / PYC_IN_MAIN 0 / DIR_ENTRIES 0`；主包 62372802 字节、预览包 57594422 字节。

E373 / E374 为 091 登记的索引锁与偶发并发 FAILED；092 首跑 lib 即 `780 passed; 0 failed`，未触发 A245，E374 仍按 091 保留在四值「已失败」。092 无网关 502、无 `.git/index.lock` 残留、无重复「干」登记（92 号 spec 与 91 号同 sha，按 A34 不重复落盘、不建 93 号）。补记自身推送后的最终远端 ref 在对话回显（A206）。

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因摊平清单而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213–E375 已失败；EQ / Q / 2 项 `Planned` 未证实；真实网络 IO / UI 宿主 / 渲染层未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 7，满足 | — |
| 连续未达通过 | 069 起连续未通过，按 `00:9.1` 应停下；用户 092「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-092-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 92 号 spec 逐字 3 字节、四份原文全文回显、A145 远端补验、A230 两项冲突逐条核验、A211 / A164 分列、A202 核出 E375 并补记覆盖、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 092 四件套、A268 G2/G3、`00:137` / `00:245` 显式核、092 占位符 0、20 组双向注入全真 FAIL、lib 780 / 0 与分段 819 / 0、Win GNU RC=0、35 守卫 0 FAIL、CI 三 job 通过、零新增依赖、`src/` 零改动、v1 不变、092 提交与推送结果见补记 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 / E356 / E357 / E360 / E361 / E363 / E366 / E367 / E369 / E370 / E371 / E374 / E375；035–047 历史格式缺失 |
| 未证实 | E362、EQ-01 ~ EQ-13（13 条）、Q-C01 / Q-C02 / Q-C08 / Q-037-01、Q-091-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、Q-082-01 / 02 / 03、Q-090-01 / Q-090-02、2 项 `Planned`、6 项低可信度转述、逐版本归属、B05 源仓库与许可、`11:242` 时长路径 |
| 未启动 | 真实网络 IO、DoH、浏览器授权、UI 宿主与渲染、子进程隔离、32 位 / MSVC / Win7 运行时、真实图片像素调整与缩放、Studio 六动作、图片预览渲染、撤销重做栈执行层、真实 `.litematic` / `.schem` 解析、投影资源站安装、方块状态编辑、真实 mrpack / CurseForge zip 解压落盘、拖动到此处页面、实例模板克隆执行、可移植实例导出、真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载 |
| 受阻 | 无（远端 Git Data API 通道正常；2 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

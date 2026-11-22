# 083 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/83-round-083-instructions.txt`（3 字节 `干`）；`docs/spec/82-round-082-instructions.txt`；`docs/decisions/082-world-editor.md`；`docs/decisions/083-delivery-reconciliation.md`；`docs/records/round-082-full-readback.md`；`docs/records/round-083-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；082 与 083 两套四件套按 A249 一次交齐 |

## 1. 原文复读

`docs/records/round-083-full-readback.md`：46 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、082 未闭环状态、A145 远端补验、A248 / A266 预检、A249 形态判定、068 先例、A244 逐条对照表、`00:230` 联网核实、`00:9.1` 冲突裁决、A164 逐条分已决断 / 未决断、`00:137` 接口终点与 `00:245` 通过标记条件显式核、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；`ai-errors.md` 520 行 / 55513 字节完整读、分两段回显，末条仍为 A271；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行逐行全文回显（A211 / A244）。83 号 spec 逐字 3 字节 `干`，SHA-256 `9ee0280b…`。

082 闭环：末条工具结果被网关截断，按 A145 只读 `GET /git/ref/heads/main` 得 `c15a4700a220bc6142fe5938a600abd79df6565b`（081 补记，parent `8e521ae`），完整 recursive tree `1226 / 1226 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；本地 HEAD `b462dd3`、DIRTY 13、无锁、无运行中 git 进程。082 主快照未提交未推送，两个 zip 为 081 轮旧包。

A266 本轮复核：按 `72-round-072-instructions.txt` 逐字澄清与 A266，平台拼入用户位次的文本不作用户当轮指令、不进 `00:133` 逐字副本；071 归因已于 072 撤回（E251），080 / 081 / 082 已按同一口径补记，历史不重写。工具从未禁用，083 正常调用工具完成收口。

`00:230` 本轮真执行：`TZ='CST-8' date` 得 `Sun Nov 22 23:20:39 CST 2026` / `23:53:09 CST 2026`；`GET /git/ref/heads/main` RC=200 得 `c15a470…`；上游状态复核 082 的 `ViaVersion/ViaNBT`（`pushed_at=2026-10-27T14:24:29Z`、`archived=false`、tags 三项）不变，083 零新增上游依赖。

## 2. 测试

| 项 | 值 |
| --- | --- |
| 首跑 `cargo test --offline --lib`（082） | **668 / 0**（RC=0，新增 18 单测，650 → 668） |
| lib 复跑 3 次（083 复核） | 第 1 次 `667 passed; 1 failed; RC=101`（`core::cache::tests::single_flight_loads_once_for_concurrent_waiters` 在 `src/core/cache.rs:252` panic）；第 2 / 3 次 `668 / 0` |
| A245 单独跑与复跑 | 单独跑该用例 3 次均 `1 passed; 0 failed`；复跑 3 次全量均 `668 / 0`；`src/core/cache.rs` 零 diff、SHA-1 `614776d34e9ec901bd8b3fcd65b03edd008479b7` |
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

`tests/` 真实文件名按 A176 先 `ls tests/*.rs` 核实为 6 个。083 `src/` 零改动，原 668 个断言一字未改、未加跳过标记、未删测试（`00:9.2` / A16）。E340 计入四值「已失败」，不包装成已处理。

## 3. 守卫与 CI

`scripts/world_editor_guard.py` 挂 `.github/workflows/ci.yml` `scan` job；083 复扫 30 个守卫，补齐 083 四件套后 0 FAIL。守卫从 082 首版即实现 A269（五个 impl 段逐值比对）、A270（七张 `&[&str]` 常量表显式 `EXPECTED` 集合逐值 + `VERIFIED_LICENSE` 单值另核）、A247（显式 import + `MAX_TEXT_BYTES` ≥ 2 处 + `read_or_default` 复用）、E322 教训（矛盾态单一函数函数体五条检查 + 八处调用点）、E330 教训（`change_event()` 函数体载荷白名单 + 十值计数）、A258（分部件拼接保留运行时值）、A260（纯查询段无 `fs::`）、A263（注入锚点唯一）。

CI 三 job 按 A116 实跑真实命令：`credential` 首次 `CREDENTIAL_FOUND`（RC=1）；定位命中 `scripts/__pycache__/download_sources_guard.cpython-312.pyc`（Python 常量折叠把源码里分部件拼接的凭据前缀还原成连续串，A258 构建产物侧延伸），`git grep -lE` 扫 tracked 0 命中、`.git/config` 0 命中；清理 `scripts/__pycache__/` 后复跑 `NO_CREDENTIAL`；`wording` → `NO_EXPLANATORY`、`hardcode` → `NO_HARDCODE`。E342 计入「已失败」，不写成「未发生」。守卫统一 `PYTHONDONTWRITEBYTECODE=1` 复跑（A205 / A258）。

`python3 scripts/delivery_guard.py`：83 号 spec 落盘后首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-083-full-readback.md`（A249 形态），补齐 083 四件套后 `DELIVERY_GUARD_OK rounds=[… 82, 83] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step`。演示 `demos/round-082-world-editor.html` 与 `demos/round-083-delivery.html` 的 JS `new Function()` 语法检查通过，五数组均 16 项对齐（A265）；`docs/index.md` 必读清单逐文件核存在非空。

## 4. 双向注入

083 收口轮补跑 28 组（A159 / A204 / A243），覆盖：七表逐值（A / B）、五 impl 段（C）、A247 复用（D / E）、坏输入标签（F）、`VERIFIED_LICENSE` 单值（G）、矛盾态函数体（H）、事件载荷用户文本（J / K / L）、禁用字面量（M）、统一信封（N）、未知键拒收（O / AD）、纯查询段（P）、单条突变（Q）、保护清单复用（R）、原子写（S）、枚举边界（T）、载荷计数断言（U）、AX03 状态（V）、boot 模块（X）、CI step（Y）、v1 面（Z）、ax_guard（AA）、显式 Vec 类型（AB）、矛盾态调用计数（AC）。**28 组全真 FAIL，0 假 OK**；每组恢复后 `WORLD_EDITOR_GUARD_OK`，六个被注入文件（`world_editor.rs` / `ax.rs` / `boot.rs` / `ci.yml` / `api.rs` / `ax_guard.py`）哈希复原。按 A243，行为测试无法区分的实现边界由守卫持有，未改测试凑失败、未降守卫断言。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| A249 双套四件套 | 082 / 083 的 spec（82 / 83）、readback、decision、verification、demo 全部齐；`delivery_guard.py` G1–G8 全过 |
| 082 占位符 | 25 个 `@…@` → 0（`grep -rho '@[A-Z_]*@'` 复核），全填真实命令输出 |
| `KNOWN_KEYS` / `ENTRY_KEYS` / `FIELDS` / `FORMATS` / `SOURCES` / `LINK_MODES` / `STATES` | 3 / 9 / 4 / 3 / 2 / 3 / 3 键，七表 `EXPECTED` 逐值；`VERIFIED_LICENSE = "MIT"` 单值 |
| 五枚举显式 code | 15 变体，`impl` 段 `=> "X"` 与 `"X" =>` 两组字面量与表逐值一致 |
| 矛盾态 | `entry_consistent()` 五条规则、八处调用；守卫解析函数体与调用计数 |
| 事件载荷 | `change_event()` 十值、`.with(` 计数恰为 10，用户文本 `id` / `license` / `title` / `body` 不进载荷 |
| `api::v1` | 7 符号 / 4 条 `pub use` 不变；083 零改动 |
| AX03 | `DataLayer`，`conflict` 空；`Planned 6` / `DataLayer 17` / `GateOnly 1` |
| 零新增第三方 | `Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff；26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| 全仓凭据 | `NO_CREDENTIAL`（清理 `scripts/__pycache__/` 后）；临时脚本用后即删 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| 082 四件套 A266 补记 | 复读 / 决策 / 验证 / 合规台账四处覆盖，历史行不重写 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213–E342 已失败；EQ / Q / 6 项 `Planned` 未证实；真实 NBT 读取写回与 UI 渲染未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 7，满足 | — |
| 连续十四轮未达通过 | 069–082 连续未通过，按 `00:9.1` 应停下；用户 083「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-083-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、A145 远端补验、四份原文全文回显、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 双套四件套、068 先例判定、`00:137` / `00:245` 显式核、082 占位符 25 → 0、082 双向注入 28 组全真 FAIL、lib 668 / 0 与分段 707 / 0、Win GNU RC=0、30 守卫 0 FAIL、CI 三 job 复跑通过、零新增依赖、v1 不变 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342；035–047 历史格式缺失 |
| 未证实 | Q-082-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、EQ-01 ~ EQ-13、4 条 Q-C、6 项 `Planned`、6 项低可信度转述 |
| 未启动 | 真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、存档编辑 UI 渲染、真实连接建立、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载、zip / 投影解析 |
| 受阻 | 无（远端 Git Data API 通道正常；6 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

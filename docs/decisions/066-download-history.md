# 第 066 轮：AX06 下载历史数据层（按 00 全约束复核）

| 项 | 值 |
| --- | --- |
| 编号 | 066 |
| 状态 | AX06 `Planned` → `DataLayer`；`api::v1` 7 符号不变；零新增第三方；UI 闸门未触发 |
| 依据 | `docs/spec/66-round-066-instructions.txt`（逐字）；`00:34` / `00:54` / `00:111` / `00:112` / `00:133` / `00:137` / `00:166` / `00:175` / `00:179` / `00:209-222` / `00:245` / `00:248`；A208 / A211 / A236 / A241；`docs/records/ax-feature-pool.md`；`docs/records/round-066-full-readback.md` |
| 前序 | 065 结尾「继续『干』按功能池落下一项（剩 21 项 Planned）」 |
| 本轮性质 | 实现轮；`src/` 新增 1 模块 + 3 处接线；`Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff |

## 2. 时间戳

开工 `Sat Nov 21 20:17:01 CST 2026`；最终 `Sat Nov 21 20:42:59 CST 2026`。

## 3. 本轮目标与范围

当轮逐字「干，遵守我的要求」。按 `00:248` 执行；「遵守我的要求」不产生新功能，本轮把 `00` 全文（261 行）与防错清单全文（479 行）真读一遍，并在 `docs/records/round-066-full-readback.md` 落「合规核对表」逐条对照。

按 A208 复核台账：065 结尾预告「按功能池落下一项」，未列「需 EQ 拍板才能动」的层；核 `047-rollback-version-precedence.md:89`，EQ-13 是「回滚是否需第三条件手动同意」，AX04 卡它。按 A211 真读功能池 21 项后选 **AX06 download_history** 的数据层：不碰 EQ-01 ~ EQ-13、不碰真实网络 IO（只记不请求）、不碰 UI 闸门（顶部栏任务进度属 UI，不做）、无需新增第三方。AX09 与 036 / EQ-13 边界相邻、AX08 需 zip 解析库、AX07 卡网络 IO，均不本轮动。

顶部栏任务进度常驻显示、设置页输入控件等 UI 渲染仍未启动；按 `00:166` 只声明数据层，不合并表述。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D-066-1 | AX06 状态 `Planned` → `DataLayer` | `AX_SPECS` 状态分层 `Planned 20` / `DataLayer 3`（AX05 / AX06 / AX11）/ `GateOnly 1`；`ax_guard.py` 显式断言扩到三项；064 与 065 历史行不重写，功能池 066 补记覆盖 |
| D-066-2 | **`api::v1` 不加符号** | 按 `00:137` 复核接口终点：新模块只被 `core/mod.rs`、`boot.rs LOADED_MODULES`、`ax.rs`、`ax_guard.py`、新守卫、CI 引用；062 稳定面 7 符号与 064 唯一口子均不动 |
| D-066-3 | 下载历史只落本地记录：`open` / `record` / `query` / `reset` | 6 类资源类型与 3 类结果封闭表；`key` 去重、超 256 条淘汰最旧；`at` 由调用方注入，不读系统时钟；无网络、无 UI、无凭据 |
| D-066-4 | 结构级坏输入整份回默认、条目级坏输入剔除该条，全部给 `[KCU]` DEGRADE 行 | 8 类：空 / 非 JSON / 非 object / 超 64 KiB / schema≠1 / entries 非数组 / 条目多余键或坏类型 / 非法 kind·result·控制字符；`00:179` 失败可见不崩 |
| D-066-5 | `reset` 只回写内置默认，**不删任何文件** | 复用 065 `settings_io::PROTECTED_FILES` 做逐项读回断言（A236）；`write_all` / `write_default` 均 `.tmp` + `fs::rename`，无残留 |
| D-066-6 | 零新增第三方，仍 26 包 / 25 第三方 | 复用 `serde_json` / `robust::safe_join` / `diagnostics::diag_line`；不改 `stats.rs`、`settings_io.rs`、`consent.rs`（`00:111`）；UX HTML、两语言包、56 张 PNG 零 diff |

## 5. 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | `pub mod download_history;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.download_history`，诊断包模块列表不缺项 |
| `src/core/ax.rs` | AX06 `DataLayer`；`AX_SPECS` 仍 24 条唯一 |
| `src/api.rs` | **零改动**，v1 仍 7 符号 |
| `scripts/ax_guard.py` / `download_history_guard.py` / `.github/workflows/ci.yml` | 守卫与 CI 第 15 步 |
| UI / 网络调用方 | 无 |

## 6. 交付快照

本地 `3aac18a`（主快照）→ 066 补记，**1121 文件 DIRTY 0**。远端主快照 `cc03cdae2ae7391026828037231c92ca904b75f2`（`force=false`），主快照阶段逐项 ALL_MATCH **True**（1121 / 1121，DIFF 0 / EXTRA 0 / truncated False）；066 补记以该 ref 为父。主包按 `git ls-files` 打包 1121 项、预览包 57 项，EXTRA 0 / MISSING 0。全仓零凭据、临时日志与注入备份已删。

推送登记：推送前只读 `GET /git/ref/heads/main` 确认远端父提交为 `f629d6f`（065 补记），再用 20-blob 精简增量 + `base_tree`（tree `c7d6644`），RC=0；未强推、未重写历史。

## 7. 验证

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**438 / 0**（复跑 3 次；首跑 437 / 1 FAILED 见 E201）` |
| 全量 `cargo test --offline` | `**477 / 0**（8 段，拆三段执行）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 31.23 s / 零 warning**` |
| 十四守卫 | `十四守卫 OK + `P09_HITS 0`` |
| CI 三 job / 演示脚本 / 必读项 | ``NO_EXPLANATORY` / `NO_HARDCODE` / `NO_CREDENTIAL`；53 份演示脚本 `BAD 0`；必读 348 项 `MISSING 0`` |
| 独立验证 | 部分通过，未发通过标记 |

## 8. 运行逻辑演示

`demos/round-066-download-history.html`：17 步可点，非 UX HTML。UI 闸门未触发，按 `00:14` 第 5 项交付运行逻辑演示而非整页 UI 演示。

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E201 | 首次全量 `cargo test --offline --lib` 报 `437 passed / 1 FAILED`，失败点是既有 `core::cache::tests::single_flight_loads_once_for_concurrent_waiters` | 单独跑该测试通过、全量复跑 3 次均 `438 / 0`；属高负载下既有并发时序 flaky，本轮未碰 `cache.rs`、未改测试、未加跳过（`00:9.2` / A187）；计入「已失败」不隐藏 |
| E202 | `download_history_guard.py` 初版用全文子串核 `PROTECTED_FILES` 复用，重犯 A241 | 改成核测试段显式 `use crate::core::settings_io::PROTECTED_FILES;`，注入删该行会真 FAIL |
| E203 | 改 AX06 状态后，功能池 064 表格行仍写 `Planned` | 按 065 口径用 066 补记覆盖，不重写历史行（`00:166` / A201） |
| E204 | 「遵守我的要求」易被写成一句口头承诺而无产物 | 落 `round-066-full-readback.md` 合规核对表：真读行数、逐字 SHA、EQ 复核、`00:137` 接口终点、状态分层、通过标记、输出结构、仓库边界逐条对照 |
| E205 | 首跑 flaky 时若按模板写「全量通过」会构成 A15 谎报 | 验证报告保留首跑 `FAILED 1` 原样与三次复跑输出，四值表列「已失败」项 |
| E206 | 新模块若把 `at` 取自 `SystemTime` 会把本机时钟写进可移植数据 | `at` 由调用方注入；守卫禁 `SystemTime` / `UNIX_EPOCH` |
| E207 | 下载历史与 061 `play-stats.json`、065 `launch.json` 同目录，`reset` 若按目录清空会抹掉同意与状态文件 | D-066-5 只回写自身文件；单测对四个保护文件逐项读回 `keep` |
| E208 | `git add -A && git commit` 被网关重跑：首次已创建 `3aac18a`，重跑报 `nothing to commit, working tree clean` RC=1 | 先只读核 `git log -1` / `DIRTY 0` / `git diff --name-only 1aa53a4..HEAD` 20 文件，确认主快照唯一且完整，再继续推送；不重复 commit、不强推（A216 / A145） |

自评 9.3（8.7（想按编号顺推 AX01） → 9.1（真读全文 + 合规核对表 + EQ 复核） → 9.3（v1 不扩面 + 十四守卫 + 四组注入 + flaky 如实登记））。扣分：20 项仍 `Planned`；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍；顶部栏进度 UI 未启动；6 项低可信度转述未交叉印证；既有 cache 并发 flaky 未定位到根因。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 合规核对表 / AX06 数据层 / 8 类坏输入 / 去重与饱和 / 四文件保护 / v1 7 符号不变 / `**438 / 0**（复跑 3 次；首跑 437 / 1 FAILED 见 E201）` / `**477 / 0**（8 段，拆三段执行）` / 十四守卫 / 零新增依赖 / 远端逐项一致 |
| 已失败 | E201 既有 `cache` 并发测试首跑 FAILED 1（复跑 3 次通过，未改测试）；035–047 历史格式缺失（不补写） |
| 未证实 | 20 项 `Planned`、6 项低可信度转述、逐版本归属、EQ-01 ~ EQ-13、4 条 Q-C |
| 未启动 | 20 项实现、顶部栏任务进度 UI、设置页 UI 渲染、真实网络 IO、UI 宿主、崩溃分析、子进程隔离 |
| 受阻 | 无（远端 Git Data API 通道正常；20 项 `Planned` 属未启动，不计受阻） |

按 `00:245`，存在已失败 / 未证实 / 未启动，**不发通过标记**（`00:9.1`）。

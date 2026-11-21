# 第 062 轮：API 面收紧与弹窗注册表

| 项 | 值 |
| --- | --- |
| 编号 | 062 |
| 状态 | 已实现、已验证；未进入 UI 渲染层 |
| 依据 | `docs/spec/62-round-062-instructions.txt`（逐字）；`11-features-input.txt:18`；`00-requirements.txt:24/25/114/137/173/175`；`11-features-input.txt:15/16/19` |
| 前序 | 061 结尾「回任一 EQ / Q-C 项；或下一声『干』按台账找下一条已决断、不依赖 EQ 的原文功能」 |
| 本轮性质 | 原文合规补漏 + 架构收敛实现轮；零新增第三方依赖 |

## 2. 时间戳

开工 `Fri Nov 20 23:47:55 CST 2026`；最终 `Sat Nov 21 00:32:06 CST 2026`。

## 3. 本轮目标与范围

用户只回「干」+ 两条提醒。按 056 的 A208，B04 / B05 / B07 / B09 / B10 仍全卡 EQ，硬开会重复 048 批评的 C 类错误，本轮不动。按 057 的 A211 真读 `00-requirements.txt` / `11-features-input.txt` 全文，确认两条提醒都是**既有原文的重申**，不是新需求：

| 用户措辞 | 原文 |
| --- | --- |
| 各种各样的 api 尽量收紧，升级也好升级 | `11:18` 不写成共有 API；`00:25` 少选平台固定 API 升级快；`11:19` API 不写死便于换系统 / 换端口；`00:175` 同类复用同一模块 |
| 弹窗像注册表一样，行为统一效率高 | `00:24` UI 用框架方式统一管理；`11:16` 每页可扩展内容方便统一格式；`00:114` 统一信封；`11:15` 复用同一代码、文件归中 |

`00:137`「每次开动前，确认文件接口最后一层会到哪里」：本轮先核 `src/lib.rs` 顶层导出面、`tests/` 对 crate 顶层的引用（只有 `tests/boot_fallback.rs:3` 的 `CancelToken`）、三处业务模块对 `catalog()` / `Popup::new` 的引用，再动手。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D01 | `src/lib.rs` 删掉 12 行 `pub use`（29 个内部具体类型平铺成共有 API）→ **0 行**；新增 `src/api.rs` 的 `pub mod v1` 作为唯一稳定公共面 | 4 个内部模块路径保留（`tests/` 与演示依赖），但不再顶层平铺再导出 |
| D02 | `api::v1` 白名单 6 个符号：`CancelToken` / `Envelope` / `Kind` / `PopupRegistry` / `CloseAction` / `PopupOpenError` | 新增对外符号必须显式升 `v2` 并给迁移步骤（`00:173`）；`api_guard.py` 锁白名单 |
| D03 | `src/core/popup.rs` 新增 `PopupSpec` 静态表 13 条作为唯一声明源；`catalog()` 从表派生 | `Popup` / `PopupKind` / `PopupSpec` / `POPUP_SPECS` / `catalog()` / `Popup::new` / `PopupRegistry::open` 全部收紧 `pub(crate)`；对外只剩注册表 |
| D04 | `open_registered(id)` 查表构造、未知 id 返回 `Err(PopupOpenError::UnknownId)` 且不落表；`open_all_registered()` / `close_all_registered()` 统一全表行为 | 业务模块不再各自循环，行为由注册表一处给出；重复 open 覆盖不增 `len()` |
| D05 | `userflow.rs` / `dispatcher/launcher.rs` / `lightweight/view.rs` 三处改走注册表 | 原有断言一字未改；`userflow` 保留「privacy 先单独确认」既有流程 |
| D06 | `scripts/api_guard.py` + `scripts/popup_guard.py`，CI `scan` 加 2 步 | 锁顶层平铺=0 / v1 白名单 / 业务模块零散落构造 / 13 条 spec 全有 close path |

## 5. 设计与代码

| 文件 | 变化 |
| --- | --- |
| `src/api.rs` | 新增；`v1` 6 行再导出，注释写明破坏性变更升 `v2` |
| `src/lib.rs` | 12 行 `pub use` → 0；新增 `pub mod api;`，保留 4 个内部模块 |
| `src/core/popup.rs` | 整表重写：`PopupSpec` / `POPUP_SPECS` / `from_spec` / `open_registered` / `open_all_registered` / `close_all_registered` / `registered_ids` / `PopupOpenError`；原 6 个测试一字未改，新增 6 个 |
| `src/core/userflow.rs` | 去掉 `catalog` / 散落 `Popup::new`；走 `open_registered` + `registered_ids` + `close_all_registered` |
| `src/dispatcher/launcher.rs` | 去掉 `catalog` / `CloseAction` import；走 `open_all_registered` / `close_all_registered` |
| `src/lightweight/view.rs` | 同上；`open_popups_for_state` / `close_all_popups` 行为不变 |
| `tests/boot_fallback.rs` | 第 3 行 import 改 `kcu_core::api::v1::CancelToken`（改路径，不动断言） |
| `.github/workflows/ci.yml` | `scan` 加 `api_guard` / `popup_guard` 两步 |

零新增第三方：`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。UI 闸门未触发：UX HTML、两语言包、56 张 PNG 零 diff。

## 6. 原文合规补漏

048 核对表 B 类只到 B10，漏了两条与「框架方式」的代码层可落地部分。本轮补 062 补记，不重写历史行。

| 编号 | 原文 | 048 状态 | 062 结论 |
| --- | --- | --- | --- |
| B11 | `11:18` 不要把咱们的 API 写成共有的 API | **未登记** | `lib.rs` 平铺 29 符号是违反；代码层已消除 |
| B12 | `00:25` 少选平台固定 API，升级快 | **未单列**（散见 038/040/041/044 核查） | 补登记；既有结论不变，不新写实现 |
| B04 局部 | `00:24` UI 用框架方式统一管理 | 已登记，卡 EQ-01 | 弹窗注册表属**代码层可落地部分**，不等 UI 宿主；UI 框架仍卡 EQ-01 |

## 7. 验证结论

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**387 / 0**（381 + 6），零 warning` |
| 全量 `cargo test --offline` | `**426 / 0**（8 段全部 ok）` |
| `cargo check --offline --target x86_64-pc-windows-gnu` | `**通过 / RC=0 / 13.66 s / 零 warning**（修 E165 后）` |
| 八守卫 | `八守卫 OK + `P09_HITS 0`；CI `NO_EXPLANATORY` / `NO_HARDCODE` / `NO_CREDENTIAL`` |
| 双向注入 | `A → `API_GUARD_FAIL top_level_pub_use=1` / RC=1；B → `POPUP_GUARD_FAIL unknown_id_not_rejected` + 单测 FAILED 1（`left Ok(()) right Err(UnknownId)`）/ RC=101；恢复 387 / 0` |
| 独立验证 | 部分通过，未发通过标记 |

## 8. 交付快照

本地 `062 补记覆盖`，`062 补记覆盖` 文件 DIRTY 0。远端 `062 补记覆盖`，逐项 ALL_MATCH `062 补记覆盖`。两个 zip 按 `git ls-files` 打包。全仓零凭据、临时日志与注入备份已删。

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E156 | 048 核对表漏 `11:18`「不写成共有 API」 | 补 B11 |
| E157 | `00:25` 未单列，散在多轮核查里 | 补 B12 |
| E158 | B04 只记 UI 框架，没把弹窗注册表当作代码层可落地部分 | 补 B04 局部；UI 框架仍标未启动 |
| E159 | `userflow.rs:56` 绕过 `catalog()` 直接 `Popup::new` | 改走 `open_registered` |
| E160 | `popup_guard.py` 首版把 `struct PopupSpec {` 定义也算成一条 spec，得 14 | 过滤 `id: "` 字面量行，复跑 `specs=13` |
| E161 | 后台 lib 编译进程被网关 502 清掉，日志空 / rc 未写（E154 复发） | `setsid` 隔离 + `CARGO_INCREMENTAL=0` 避开沙盒硬链接退化，重跑 |
| E162 | 收紧 `pub(crate)` 后 `pub fn catalog() -> Vec<Popup>` 会 private-in-public | `catalog()` 一并 `pub(crate)`，`api::v1` 不导出 `Popup` |
| E163 | `PopupRegistry::open` 若保持 pub 会接收 `pub(crate)` 参数 | 一并收紧，对外只留 `open_registered` / `open_all_registered` |
| E164 | 删 import 删过头 | `src/lightweight/view.rs:204` 仍用 `CloseAction::Button`，首版把整行 import 删成只剩 `PopupRegistry`，`cargo test --lib` 报 E0433 | 只删本轮真正不再引用的符号，不整行删 | 恢复 `{CloseAction, PopupRegistry}`，复跑 387 / 0；登记 A224 |
| E165 | 收紧 `pub(crate)` 后 Windows GNU 交叉检查出 2 条 dead_code warning | `Popup.kind` / `Popup.title` 非测试构建无人读；`catalog()` 只被 `#[cfg(test)]` 用 | 不留 warning，也不删字段掩盖 | `catalog()` 收进 `#[cfg(test)]`；两个元数据字段显式 `#[allow(dead_code)]` 并注明保留用途；复跑 Windows GNU 零 warning、lib 387 / 0 |
| E166 | 后台 Popen 编译进程两次被网关 502 清掉，日志空 / rc 未写（E154 复发） | 不能凭脚本宣称编译通过 | 改前台执行 + `CARGO_INCREMENTAL=0` 避开沙盒硬链接退化 |
| E167 | 全量测试前台 370 s 被网关 502 截断在 abi 第 2 个测试 | 不能拿半截日志当全量结论 | 拆三段：`--lib`、`--test` 五合一段、单独 `plugin_abi_load`，三段 RC 全 0 后合并计数 |

自评 9.4（初稿 8.5（只想做状态复核） → 真读原文定位两条漏项 9.0 → 收紧落地 + 双向注入 9.4）。扣分：远端推送依赖通道、UI 框架 / 真实网络 / 崩溃分析 / 子进程隔离未启动、EQ 未拍。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 顶层平铺 0、v1 六符号、13 条 spec 单一声明源、三处业务模块统一入口、`**387 / 0**（381 + 6），零 warning`、八守卫、双向注入、零新增依赖、远端逐项一致 |
| 已失败（不补写） | 035–047 历史格式缺失 |
| 未证实 | EQ-01 ~ EQ-13、4 条 Q-C、B05 / B07 / B09 / B10、UI 框架选型 |
| 未启动 | UI 渲染接线、真实网络 IO、UI 宿主、崩溃分析、子进程隔离 |
| 受阻 | 无（055–059 远端受阻已于 060 解除；本轮 Git Data API 通道正常） |

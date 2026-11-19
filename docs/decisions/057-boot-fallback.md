# 第 057 轮：§12 启动级兜底

| 项 | 值 |
| --- | --- |
| 编号 | 057 |
| 状态 | 已实现、已验证；未进入 UI 渲染层 |
| 依据 | `docs/spec/57-round-057-instructions.txt`（逐字：「干」）；`docs/spec/00-requirements.txt` 第 12 节 |
| 前序 | 056 结尾列「B04 / B05 / B07 / B09 / B10 需 EQ 拍板」 |
| 本轮性质 | 实现轮；零新增第三方依赖 |

## 2. 时间戳

开工 `Thu Nov 19 12:02:30 CST 2026`；最终 `Thu Nov 19 12:31:58 CST 2026`。

## 3. 本轮目标与范围

用户只回「干」，未给写凭据、未回 Q-C、未点 EQ。按 049/050 既有默认「按台账继续、不代拍板」执行，但不再写状态复核轮：真读 `00-requirements.txt` 第 12 节后，选一条**已决断、未落地、不依赖任何 EQ** 的原文实现。

B04 / B05 / B07 / B09 / B10 仍全卡 EQ，本轮不动。选 §12 的四条原因写对话，不进仓库。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D01 | 新增 `src/core/boot.rs`：`BootState` 持久化连续失败计数、`Tier` 四级分级、`export` 诊断包落盘 | 零新增第三方；序列化 `serde_json`、路径 `robust::safe_join`、限流 `robust::OpBudget`、诊断行 `core::diagnostics`、包结构 `core::integrity::DiagnosticBundle`、四级源 `core::integrity::Level` |
| D02 | `dispatcher/launcher.rs` 接线：`DispatchInput.export_dir` / `LaunchOutcome.bundle_path`；`diagnostic_ready` 时构造真实四项并调用 `boot::export` | 原 `diagnostic_bundle` 四行摘要保留；原 20 个断言不改；`export_dir=None` 时行为与 056 一致 |
| D03 | 安全模式仍失败时导出 `diagnostic-bundle.json`，含 `lines` / `config_snapshot` / `runtime` / `modules` 四字段 | 无导出目录给可见 `SKIP`；目录创建失败、写失败、超量、控制字符一律给 `[KCU]` `ERROR` 行，不崩 |
| D04 | 状态文件 `boot-state.json`；删、非 JSON、超 4096 B、schema≠1、failures 非法一律回 `{"schema":1,"failures":0}` | 回退给可见诊断；`AtomicU32::try_update` 饱和；成功归零；写失败可见 |

## 5. 设计与代码

| 文件 | 行 | 内容 |
| --- | --- | --- |
| `src/core/boot.rs` | 新增 | 常量 10 项；`Tier` 四变体 `code()` / `action()` / `line()`；`classify(Option<Level>)`；`safe_mode_reached`；`BootState::open/record/builtin_defaults`；`export`；`validate_dir` / `parse_state` / `validate_bundle` / `loaded_modules`；16 个单元测试 |
| `src/core/mod.rs` | +1 | `pub mod boot;` |
| `src/dispatcher/launcher.rs` | +2 import / +2 字段 / +2 构造 / +16 导出段 | 真实四项替换「core,dispatcher」硬编码摘要；`bundle_path` 回传 |
| `tests/boot_fallback.rs` | 新增 6 个集成测试 | 端到端导出、无目录可见、状态文件删后恢复、包删后重导、坏状态恢复再持久化、8×8 并发 |

`LOADED_MODULES` 为 `core/mod.rs` 与 `dispatcher/launcher.rs` 的 21 项事实性索引，不推导、不枚举运行时句柄。

## 6. 运行逻辑演示

`demos/round-057-boot-fallback.html`，17 步可点，非整页 UX HTML。UI 闸门未触发：UX HTML、两语言包、56 张 PNG 零 diff。

## 7. 验证条件

| 编号 | 条件 |
| --- | --- |
| V1 | `cargo test --offline --lib` 367 / 0，零 warning |
| V2 | `cargo test --offline --test boot_fallback` 6 / 0 |
| V3 | `cargo check --offline --target x86_64-pc-windows-gnu` 通过 |
| V4 | 六守卫零命中或 OK；`P09_HITS 0` |
| V5 | 注入 A（`bundle_path=None`）→ 集成测试 FAILED；注入 B（删 schema 校验）→ FAILED；恢复全过 |
| V6 | 主包按 `git ls-files` 打包，EXTRA 0 / MISSING 0 |
| V7 | 远端写入如实登记，不伪造 ALL_MATCH |

## 8. 本轮真问题

| 编号 | 位置 | 现象 | 后果 | 处置 |
| --- | --- | --- | --- | --- |
| E134 | `src/core/boot.rs` `record` | 首版 `fetch_update(...).unwrap_or(0)` | Err 分支把计数重置为 0；且 `fetch_update` 在 rustc 1.99 已 deprecated | 改 `Ok(v) | Err(v) => v` 取旧值；`try_update` 替 `fetch_update`；零 warning |
| E135 | `src/core/boot.rs` | 顶层 `use std::path::Path` 未被非测试段使用 | lib 构建产生 unused_imports warning | 顶层只留 `PathBuf`，测试模块单独引 `Path` |
| E136 | `src/core/boot.rs` `export` | `e.kind() as u8` 对 non_exhaustive `ErrorKind` 有转换风险 | 未来工具链可能编译失败 | 改 `format!("{:?}", e.kind())` |
| E137 | `tests/boot_fallback.rs` | 占位首版误写 `kcu_core::boot_unused_guard::*` | 编译必然失败 | 整份重写为 6 个真实集成测试；`CancelToken` 从 crate 根导入 |
| E138 | `tests/boot_fallback.rs` | `dispatcher::CancelToken` 不存在 | 编译失败 | 改 `kcu_core::CancelToken` |
| E139 | 全量验证第一次调用被网关 502 截断 | 无输出 | 拿不到回归结论 | 拆 lib / 集成两段各跑一次，367 / 0 与 6 / 0 |

注入 A 与注入 B 的失败回显保留在 `docs/verification/round-057.md`。测试文件未因注入修改断言。

## 9. 自我批判

| 项 | 结论 |
| --- | --- |
| 幻觉 | 未把 `dispatcher` 已有的 safe_mode 说成本轮新增；051/052/053 的四级与包结构明确标为已有，本轮只补持久化与落盘 |
| 验证 | 六条集成真读文件、真删文件、真并发；注入 A/B 证明接线与回退生效；367 / 0 仅作回归 |
| 工程 | 零新增依赖；`src/dispatcher/launcher.rs` 增量 22 行，原有 20 个测试断言一字未改 |
| 布局 | UI 闸门未触发；演示是独立流程 HTML |
| 安全 | 路径走 `safe_join`；导出目录由输入给出，不写死；状态与包都做尺寸、schema、控制字符、数量边界 |
| 许可证 | 未引入新 crate；`serde_json` / `lru` / `log` / `anyhow` / `crossbeam-utils` 均已在 025–044 取得全文并登记 |
| 用户逻辑 | `export_dir=None` 时所有既有行为不变；暴力删除、并发、限流、饱和各有测试 |

自评 **9.4**（8.4 初稿想继续状态复核 → 8.9 真读原文找到 §12 缺口 → 9.4 落地实现、接线、注入、回归、交付）。未给满分：远端写入受阻；GUI 接线未启动；EQ-01 ~ EQ-13 仍待拍板。

## 10. 四值

| 项 | 值 |
| --- | --- |
| §12 持久化计数、安全模式内置默认、四项诊断包落盘、四级分级 | 已证实 |
| 367 / 0、6 / 0、Windows GNU、六守卫、双向注入 | 已证实 |
| 零新增依赖（26 包 / 25 第三方）、零 UI diff | 已证实 |
| 035–047 历史交付格式缺失 | 已失败（不补写） |
| B04 / B05 / B07 / B09 / B10、EQ-01 ~ EQ-13、4 条 Q-C | 未证实（待拍板） |
| 真实网络 IO、UI 宿主、崩溃分析、子进程隔离、GUI 接线 | 未启动 |
| 远端写入（403）、GUI 端到端、Win7 / MSVC / i686 运行时 | 受阻 |

独立验证「部分通过」，**未发通过标记**。

## 交付补记

| 项 | 值 |
| --- | --- |
| 远端 `refs/heads/main` | `1fe6a90255ec`（054 补写记录），055 / 056 / 057 未更新 |
| 待补推 | `03ba613` → `7aede31` → `0902962` → 057 两次提交 |
| 写凭据 | `KCU_PAT` unset、credential 无写凭据、`.git/config` 零 token |
| 逐项 ALL_MATCH | 本轮不成立；不强推、不伪造、不重写远端历史 |
| 两个 zip | 主包按 `git ls-files` 打包，预览包 57 项 |
| 零凭据 | tracked 零凭据；临时日志与注入备份已删 |

最终交付快照与时间戳见 `docs/verification/round-057.md`。

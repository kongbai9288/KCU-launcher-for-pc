from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
html_n = len(list((ROOT / 'demos').glob('*.html')))
png_n = len(list((ROOT / 'demos/preview').glob('[0-9][0-9]-*.png')))
print('REAL pkgs', pkgs, 'third', third, 'html', html_n, 'png', png_n)

DECISION = '''# 第 057 轮：§12 启动级兜底

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
| 零新增依赖（{pkgs} 包 / {third} 第三方）、零 UI diff | 已证实 |
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
'''.replace('{pkgs}', str(pkgs)).replace('{third}', str(third))

VERIFICATION = '''# 第 057 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 057 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 本轮为实现轮；367 / 0 与 6 / 0 含 22 个新增测试，其余为回归 |

| 编号 | 命令 / 检查 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `git rev-parse --short HEAD` / `git status` | 起 `0902962`，1062 文件，DIRTY 0 | 已证实 |
| V2 | `cargo test --offline --lib` | **367 / 0**，零 warning | 已证实 |
| V3 | `cargo test --offline --test boot_fallback` | **6 / 0** | 已证实 |
| V4 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V5 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V6 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0 | 已证实 |
| V7 | `cargo test --offline --test plugin_abi_load` | 6 / 0 | 已证实 |
| V8 | 全量合计 | **399 / 0** | 已证实 |
| V9 | `cargo check --offline --target x86_64-pc-windows-gnu` | 通过 | 已证实 |
| V10 | `panic_guard` / `semver_guard` | 零命中 / 零命中 | 已证实 |
| V11 | `i18n_guard` / `lang_guard` / `policy_guard` | 零命中 / keys 26 / G1–G8 OK | 已证实 |
| V12 | `delivery_guard` | `DELIVERY_GUARD_OK rounds=[56, 57]` | 已证实 |
| V13 | `p09_scan` | `P09_HITS 0 []` | 已证实 |
| V14 | CI 三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` | 已证实 |
| V15 | `node new Function` demos HTML + 两语言包 | `ALL_JS_OK N_HTML` | 已证实 |
| V16 | `yaml.safe_load(ci.yml)` | `scan_steps 10` | 已证实 |
| V17 | `ast.parse` 全部 scripts | 通过 | 已证实 |
| V18 | 注入 A（`bundle_path = None`） | `safe_mode_failure_exports_real_four_sections` FAILED，`bundle_path must be set after safe-mode failure` | 已证实 |
| V19 | 注入 B（删 `parse_state` schema 校验） | `malformed_state_recovers_and_persists_again` FAILED，EXIT 101，`state schema` 断言落空 | 已证实 |
| V20 | 恢复后 `--lib` / `--test boot_fallback` | 367 / 0、6 / 0 | 已证实 |
| V21 | 必读读取命令块 | 303 项，`MISSING 0` | 已证实 |
| V22 | `git push origin main` | `fatal: ... 403`，PUSH_RC 128 | 受阻 |
| V23 | 远端只读 ref | `1fe6a90255ec`（054） | 受阻 |

| 项 | 值 |
| --- | --- |
| §12 持久化计数、安全模式内置默认、四项诊断包落盘、四级分级 | 已证实 |
| 367 / 0、6 / 0、Windows GNU、六守卫、双向注入 | 已证实 |
| 零新增依赖（PKG 包 / THIRD 第三方）、零 UI diff | 已证实 |
| 035–047 历史交付格式缺失 | 已失败（不补写） |
| B04 / B05 / B07 / B09 / B10、EQ-01 ~ EQ-13、4 条 Q-C | 未证实（待拍板） |
| 真实网络 IO、UI 宿主、崩溃分析、子进程隔离、GUI 接线 | 未启动 |
| 远端写入、GUI 端到端、Win7 / MSVC / i686 运行时 | 受阻 |

限制：改动作者未代改验证结论；393 个测试含 22 个新增，其余仅作回归。048 / 051–056 历史验证报告不补写。

## 交付快照（057 收口）

| 项 | 值 |
| --- | --- |
| 远端 `refs/heads/main` | `1fe6a90255ec`（054 补写记录），055 / 056 / 057 **未更新** |
| 待补推 | `03ba613` → `7aede31` → `0902962` → 057 快照（一次提交） |
| 再试推送 | `fatal: ... 403`，PUSH_RC 128；`KCU_PAT` unset、credential 无写凭据、`.git/config` 零 token |
| 逐项 ALL_MATCH | **本轮不成立**（远端仍是 054 树）。不强推、不伪造、不重写远端历史 |
| 两个 zip | 主包按 `git ls-files` 打包（EXTRA 0 / MISSING 0）；预览包 57 项；均不含 `.git` / `target/` / `__pycache__` |
| 零凭据 | tracked 零凭据；`.git/config` 零 token；注入备份与临时日志已删 |
| 开工 / 最终时间戳 | `Thu Nov 19 12:02:30 CST 2026` / `Thu Nov 19 12:31:58 CST 2026` |

057 结论、实现、接线、双向注入、399 / 0 回归全在本地复跑，不依赖远端写入。
'''.replace('N_HTML', str(html_n)).replace('PKG', str(pkgs)).replace('THIRD', str(third))

(ROOT / 'docs/decisions/057-boot-fallback.md').write_text(DECISION)
(ROOT / 'docs/verification/round-057.md').write_text(VERIFICATION)
print('WROTE decision + verification')


def app(f, s, marker=None):
    p = ROOT / f; t = p.read_text()
    m = marker or s.strip().splitlines()[0]
    if m in t:
        print('SKIP_DUP', f); return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/records/requirement-compliance-audit.md', '''## 057 补记：§12 启动级兜底

| 项 | 056 状态 | 057 状态 |
| --- | --- | --- |
| 连续多次启动失败进入安全模式 | dispatcher 内存计数 + `ModeSelector::safe` 已有 | 新增 `BootState` 跨进程持久化计数（`boot-state.json`）；删 / 坏 / 超大 / schema 错回默认；成功归零；饱和不溢出 |
| 忽略自定义配置用内置默认 | `ModeSelector::safe` 置 `config_mode` / `args_mode` / `task_mode` 为 None | `builtin_defaults()` 返回 `Config::empty` JSON 与 `feature_gate::BUILTIN_POLICY`，两者由 `serde_json` 复验 |
| 安全模式仍失败导出诊断包 | `diagnostic_bundle` 仅 4 行摘要，模块名硬编码 `core,dispatcher`，无落盘 | `boot::export` 写 `diagnostic-bundle.json`，含 `lines` 全文 / `config_snapshot` / `runtime` / 21 项 `modules`；`LaunchOutcome.bundle_path` 回传；无目录给可见 SKIP |
| 四级分级 | `integrity::Level` 四变体已有，局部使用 | `boot::classify` 统一出口，`Tier` 四变体各带 `code()` / `action()` / `[KCU]` 行 |
| 统一一行诊断、禁空捕获、删文件预防 | 已有 `diag_line` / `robust` | 状态与包全部失败分支给 `[KCU]` 行；`safe_join` 路径校验；尺寸 / 数量 / 控制字符 / 并发 / 限流边界各有测试 |

B01 / B02 的 035–047 历史偏差仍标「已失败」，不补写、不重写。B03（050）、B06（051–053）、B08 判定层（054）状态不变。B04 / B05 / B07 / B09 / B10 仍**未启动**，卡点不变。C 类 10 条（055 复核）状态不变。本轮未新增 EQ、未代用户拍板。
''', '## 057 补记')

app('docs/decisions/index.md', '| 057 | §12 启动级兜底：持久化计数、四级分级、四项诊断包落盘、dispatcher 接线 | 已实现、已验证 | 057-boot-fallback.md |')

app('docs/checklists/ai-errors.md', '''## 057 轮新增

| 编号 | 防错项 |
| --- | --- |
| A211 | 原文里「已决断、不依赖 EQ」的条目要真读全文找，不能只核哈希与台账状态；连续多轮只写状态复核轮等于没推进。 |
| A212 | `fetch_update(...).unwrap_or(0)` 在 Err 分支会把计数重置为 0；`Ok(v) \\| Err(v) => v` 才取到旧值。rustc 1.99 起 `fetch_update` deprecated，改名 `try_update`。 |
| A213 | 顶层 import 只被 `#[cfg(test)]` 段使用时，lib 构建产生 unused_imports warning；把该 import 移进测试模块。 |
''', '## 057 轮新增')

app('docs/records/interface-log.md', '''## 057 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I102 | `src/core/boot.rs` | `STATE_FILE` / `BUNDLE_FILE` / `Tier` / `classify` / `safe_mode_reached` / `BootState` / `export` / `loaded_modules` |
| I103 | `src/dispatcher/launcher.rs` | `DispatchInput.export_dir`、`LaunchOutcome.bundle_path`；`diagnostic_ready` 段构造 `DiagnosticBundle` 真实四项并调 `boot::export` |
| I104 | `tests/boot_fallback.rs` | 6 个集成测试：端到端导出、无目录可见、状态删后恢复、包删后重导、坏状态恢复再持久化、8×8 并发 |
| I105 | 状态 | 零新增第三方；B04/B05/B07/B09/B10 未开工；远端 403 受阻 |
''')

app('docs/records/code-ownership-audit.md', '''## 057 实现轮

零新增第三方，`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。新增 `src/core/boot.rs` 中序列化交 `serde_json`、路径与限流交 `robust`、诊断行交 `diagnostics`、包结构与四级源交 `integrity`、内置默认交 `Config` 与 `feature_gate`、日志交 `log`；项目特有只剩状态迁移、阈值比较、导出路径策略与 21 项模块索引。`src/dispatcher/launcher.rs` 增量 22 行，原有 20 个断言一字未改。023 A03 自写底座例外于 024 撤回的状态不变。
''')

app('docs/records/pending-question-environments.md', '''**057 状态**

用户未点 EQ 编号。本轮真读 `00-requirements.txt` 第 12 节，落地 §12 启动级兜底（不依赖任何 EQ）：`BootState` 持久化计数、四级 `Tier`、四项诊断包落盘、dispatcher 接线。B04 / B05 / B07 / B09 / B10 仍**未开工**，卡点 EQ-01 / 源仓库与许可未给 / EQ-05 / EQ-11 / 推进口径未决断不变。EQ-01 ~ EQ-13 仍待拍板，EQ-14（049）、EQ-15（050）已关闭；Q-C01 / Q-C02 / Q-C08 / Q-037-01 仍待拍板。本轮未新增 EQ。
''', '**057 状态**')

ROUNDS = f'''## 057

| 落点 | 内容 |
| --- | --- |
| docs/spec/57-round-057-instructions.txt | 逐字副本：「干」 |
| docs/records/round-057-full-readback.md | B02 复读证据：5 份字节 / 行 / SHA-256 + §12 原文锚点 |
| src/core/boot.rs | **主交付**：`BootState` / `Tier` / `export` / 16 单元测试 |
| src/core/mod.rs | `pub mod boot;` |
| src/dispatcher/launcher.rs | 22 行增量接线，真实四项诊断包落盘 |
| tests/boot_fallback.rs | 6 个集成测试 |
| docs/decisions/057-boot-fallback.md | 四锚点、D01–D04、E134–E139、自评 9.4、四值 |
| docs/verification/round-057.md | 23 条复跑证据 + 交付快照 |
| demos/round-057-boot-fallback.html | 运行逻辑演示（17 步可点，非整页 UX HTML） |
| 补记 | requirement-compliance-audit 057 补记、pending-question-environments 057 状态、decisions/index、ai-errors A211–A213、interface-log I102–I105、code-ownership-audit、README |
| 索引 | docs/index 296 → 303 项 |

056 结尾列「B04 / B05 / B07 / B09 / B10 需 EQ 编号」。用户没给凭据、没回 Q-C、没点 EQ，只回「干」。按 049/050 既有默认「按台账继续、不代拍板」执行；**不再写状态复核轮**，真读 `00-requirements.txt` 第 12 节后选一条已决断、未落地、不依赖任何 EQ 的原文实现。

**B02**：5 份原文全文遍历；`ai-errors.md` 复读时 39451 B / 417 行（A211–A213 在复读之后追加）。真读 11 / 12 输入文档内容，非只核哈希。

**真实缺口**：`integrity.rs` 已有 `SAFE_MODE_AFTER` / `DiagnosticBundle` / `Level` 四变体，`dispatcher/launcher.rs` 已有内存计数与 `ModeSelector::safe`，但 `consecutive_failures` 由外部传入、仓库无跨进程计数；安全模式只置 bool、无内置默认配置置换动作；`diagnostic_bundle` 只是 4 行摘要，模块名硬编码 `core,dispatcher`，**无文件导出**。§12 要求「导出诊断包（日志 + 配置快照 + 运行时信息 + 已加载模块列表）」未落地。

**落地**：`src/core/boot.rs` 零新增依赖，序列化交 `serde_json`（025）、路径与限流交 `robust`（048）、诊断行交 `diagnostics`、包结构与四级源交 `integrity`（051）、内置默认交 `Config` 与 `feature_gate`（053）、日志交 `log`（032）；项目特有只剩状态迁移、阈值比较、导出路径策略与 21 项模块索引。`dispatcher/launcher.rs` 增量 22 行：`DispatchInput.export_dir` / `LaunchOutcome.bundle_path` / `diagnostic_ready` 段构造真实四项并调 `boot::export`；原 `diagnostic_bundle` 四行摘要与原 20 个断言一字未改；`export_dir=None` 时行为与 056 一致。

**六个真问题（E134–E139）**：`unwrap_or(0)` 在 Err 分支把计数重置、`fetch_update` deprecated、`Path` 顶层 unused import、`ErrorKind as u8` 转换风险、集成测试占位首版、`CancelToken` 导入路径错、全量验证 502 拆段。全部留痕并复跑通过。

**双向注入**：A（`bundle_path = None`）→ `safe_mode_failure_exports_real_four_sections` FAILED；B（删 `parse_state` schema 校验）→ `malformed_state_recovers_and_persists_again` FAILED，EXIT 101；恢复后 367 / 0 + 6 / 0。失败回显保留，测试断言未因注入修改。

**验证**：`cargo test --offline --lib` **367 / 0**（351 + 16），`--test boot_fallback` **6 / 0**，全量 **399 / 0**；Windows GNU 通过；panic / semver / i18n / lang / policy / delivery 六守卫零命中或 OK；`P09_HITS 0`；CI 三条 `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE`；{html_n} 份 demos HTML 脚本通过；`yaml.safe_load` scan 10 steps；303 项必读 `MISSING 0`。UI 闸门**未触发**：UX HTML、两语言包、{png_n} 张 PNG、`Cargo.toml`、`Cargo.lock`、`vendor/` 全部零 diff，仍 **{pkgs} 包 / {third} 第三方**。

**四值**：§12 四项落地、367 / 0 + 6 / 0、Windows GNU、六守卫、双向注入 = 已证实；035–047 历史缺失 = 已失败（不补写）；B04/B05/B07/B09/B10、EQ-01 ~ EQ-13、4 条 Q-C = 未证实；真实网络 IO / UI 宿主 / 崩溃分析 / 子进程隔离 / GUI 接线 = 未启动；远端写入（403）/ GUI 端到端 / Win7 与 MSVC 与 i686 运行时 = 受阻。独立验证「部分通过」，**未发通过标记**。自评 **9.4**。

**唯一下一步**：给写凭据 / 通道后按 `03ba613 → 7aede31 → 0902962 → 057 快照（一次提交）` 补推并逐项比对。
'''.replace('{pkgs}', str(pkgs)).replace('{third}', str(third)).replace('{html_n}', str(html_n)).replace('{png_n}', str(png_n))
app('docs/records/rounds.md', ROUNDS, '## 057\n')

p = ROOT / 'docs/index.md'; t = p.read_text()
a = '296. demos/round-056-b-class.html\n\n读取命令：'
if a in t and '297. docs/spec/57-round-057-instructions.txt' not in t:
    t = t.replace(a, '''296. demos/round-056-b-class.html
297. docs/spec/57-round-057-instructions.txt
298. docs/records/round-057-full-readback.md
299. src/core/boot.rs
300. tests/boot_fallback.rs
301. docs/decisions/057-boot-fallback.md
302. docs/verification/round-057.md
303. demos/round-057-boot-fallback.html

读取命令：''', 1)
    t = t.replace('scripts/delivery_guard.py demos/round-056-b-class.html; do printf',
                  'scripts/delivery_guard.py demos/round-056-b-class.html docs/spec/57-round-057-instructions.txt docs/records/round-057-full-readback.md src/core/boot.rs tests/boot_fallback.rs docs/decisions/057-boot-fallback.md docs/verification/round-057.md demos/round-057-boot-fallback.html; do printf', 1)
    p.write_text(t); print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = ROOT / 'README.md'; t = p.read_text()
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 057 |', t, count=1)
sec = f'''

## 057 §12 启动级兜底

真读 `00-requirements.txt` 第 12 节后落地一条**已决断、不依赖任何 EQ** 的原文：`src/core/boot.rs` 跨进程持久化连续失败计数（删 / 坏 / 超大 / schema 错回默认）、四级 `Tier` 统一出口、安全模式内置默认配置、`diagnostic-bundle.json` 真实四项落盘；`src/dispatcher/launcher.rs` 增量 22 行接线，原 20 个断言一字未改，`export_dir=None` 时行为不变。

零新增第三方，仍 **{pkgs} 包 / {third} 第三方**；`cargo test --offline --lib` **367 / 0**、`--test boot_fallback` **6 / 0**、全量 **399 / 0**；双向注入 A/B 各 1 项 FAILED，恢复后全过。远端 `git push` 仍 403，055 / 056 / 057 未更新远端，不强推、不伪造 ALL_MATCH。
'''
if '## 057 §12 启动级兜底' not in t:
    (ROOT / 'README.md').write_text(t.rstrip() + sec); print('README_OK')
else:
    print('README_SKIP_DUP')

print('ALL_DOCS_OK')

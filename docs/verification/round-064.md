# 064 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/64-round-064-instructions.txt`；`docs/decisions/064-privacy-policy-and-ax-pool.md`；`docs/records/ax-feature-pool.md` |
| 口径 | 实现层与交付层分开判；`Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff，测试作回归不作质量结论 |

## 1. 原文复读

`docs/records/round-064-full-readback.md`：8 份文件字节 / 行 / SHA-256 表，12 个原文锚点逐字回显。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | SHA-256 |
| --- | --- | --- |
| `docs/spec/64-privacy-policy-v1.1.txt` | 4638 | `de3b07c70f6747ae220db8e67c6168eed0b35e992c80334581b154cd80a3e8b8` |
| `docs/spec/64-round-064-instructions.txt` | 4813 | `d20e36a1241c6feb35ed6e0ffbd21d0301448de8db90e47713d6be4a4b4364fc` |

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**413 / 0**` |
| 全量 `cargo test --offline` | `**452 / 0**（8 段，拆三段执行）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 10.33 s / 零 warning**` |

全量 8 段逐项（拆三段执行，避免网关 502 截断）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 413 | 0.19 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 48.81 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 116.91 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **452** | — |

新增 26 个单测（consent 10 / client_ai 4 / storage 6 / ax 6），387 → 413；原 387 个断言一字未改。`Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff，测试仅作回归不作质量结论。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| `panic_guard` | `PANIC_GUARD_OK files 48 hits 0` |
| `semver_guard` | `SEMVER_GUARD_OK version_files 4 hits 0` |
| `i18n_guard` | `I18N_GUARD_OK rs_files 48 ux_html 1 hits 0` |
| `lang_guard` | `LANG_GUARD_OK locales zh-CN en-US keys 26` |
| `policy_guard` | `POLICY_GUARD_OK g1_033_closed ... g8_054_retracted` |
| `delivery_guard` | `DELIVERY_GUARD_OK rounds=[56, 57, 61, 62, 63, 64]` |
| `p09_scan` | `P09_HITS 0 []` |
| `api_guard` | `API_GUARD_OK flat_pub_use=0 v1_symbols=7 scattered=0` |
| `popup_guard` | `POPUP_GUARD_OK specs=13 ids_unique=13 close_path=all` |
| `privacy_guard` | `PRIVACY_GUARD_OK verbatim policy=v1.1 effective=2026-11-21 popup=privacy` |
| `ai_gate_guard` | `AI_GATE_OK port=1 no_listener no_ui no_token deny_by_default` |
| `ax_guard` | `AX_GUARD_OK specs=24 gate_only=1 data_layer=1 planned=22` |

按 `.github/workflows/ci.yml` 真实命令复跑：`NO_EXPLANATORY` / `NO_HARDCODE` / `NO_CREDENTIAL`。51 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 336 项 `MISSING 0`。`cargo check --offline --target x86_64-pc-windows-gnu` RC=0 / 10.33 s / 零 warning。

一处环境事实：沙盒会话会重置全局 git 配置，每次 `git` 前需 `git config --global --add safe.directory`；与仓库内容无关，不计失败项。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| 政策文件 SHA-256 | `de3b07c70f6747ae220db8e67c6168eed0b35e992c80334581b154cd80a3e8b8` |
| `consent.rs` 引用方式 | `include_str!("../../docs/spec/64-privacy-policy-v1.1.txt")` |
| `src/` 政策正文重复 | 0（`privacy_guard` 扫全 `src`） |
| `AX_SPECS` | 24 条唯一，单一声明源 |
| `api::v1` | 7 符号，唯一新增 `ClientAiGate` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |

## 5. 双向注入

| 注入 | 结果 |
| --- | --- |
| A：把 `client_ai.rs` 的 `submit` 改成返回 `Ok` | `AI_GATE_FAIL not_deny_by_default` + `ClientAiGate` 单测 FAILED |
| B：把 AX23 改成 `Planned` / `ui=true` | `AX_GUARD_FAIL ax23_not_gate_only` |
| C：改政策文件一个字 | `PRIVACY_GUARD_FAIL policy_not_verbatim` |
| D：删 `api.rs` 的口子行 | `API_GUARD_FAIL v1_surface_changed` + `AI_GATE_FAIL v1_port_count=0` |

| 注入 | 结果 |
| --- | --- |
| A：`client_ai.rs` 的 `submit` 改返回 `Ok` | `AI_GATE_FAIL not_deny_by_default` RC=1；恢复后 OK |
| B：AX23 改 `Planned` / `ui=true` | `AX_GUARD_FAIL ax23_not_gate_only` RC=1；恢复后 OK |
| C：政策文件 `v1.1` 改 `v1.2` | `PRIVACY_GUARD_FAIL policy_not_verbatim` RC=1；恢复后 SHA 一致 |
| D：删 `api.rs` 的口子行 | `API_GUARD_FAIL v1_surface_changed` + `AI_GATE_FAIL v1_port_count=0`，两个 RC=1；恢复后 OK |

注入 A 首版未触发（E189）：守卫用全文子串判断，测试断言里同名 `Err(ClientAiError::NotEnabled)` 让替换失效；改成只判 `submit` 函数体后真触发。四次注入的恢复均按原文本回写并校验 SHA-256 一致。

## 6. 交付比对

| 项 | 值 |
| --- | --- |
| 本地 HEAD | `064 补记覆盖`（`064 补记覆盖` 文件，DIRTY 0） |
| 远端 `refs/heads/main` | `064 补记覆盖` |
| 逐项 ALL_MATCH | `064 补记覆盖` |
| 主包 / 预览包 | `064 补记覆盖` / 57 项，EXTRA 0 / MISSING 0 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 政策逐字、24 条 spec、v1 第 7 符号、同意闸门、AX05 数据层、`**413 / 0**`、十二守卫、远端逐项一致 |
| 已失败（不补写） | 035–047 历史格式缺失 |
| 未证实 | 6 项低可信度转述、逐版本归属、EQ-01 ~ EQ-13、4 条 Q-C、22 项 `Planned` |
| 未启动 | 22 项实现、GUI 渲染接线、真实网络 IO、UI 宿主、崩溃分析、子进程隔离 |
| 受阻 | 无（远端 Git Data API 通道正常；22 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在未证实与未启动项，不发通过标记。

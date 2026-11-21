# 063 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/63-round-063-instructions.txt`；`docs/decisions/063-axolotl-survey.md` |
| 口径 | 实现层与交付层分开判；`src/` 零改动，测试仅作回归不作质量结论 |

## 1. 原文复读

`docs/records/round-063-full-readback.md`：5 份文件字节 / 行 / SHA-256 表，10 个原文锚点逐字回显。复读在写任何文件之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**387 / 0**` |
| 全量 `cargo test --offline` | `**426 / 0**（8 段，拆三段执行）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 16.07 s / 零 warning**` |

全量 8 段逐项（拆三段执行，避免网关 502 截断）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 387 | 0.16 s |
| `tests/boot_fallback.rs` | 6 | 0.01 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.00 s |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 24.00 s（真加载 cdylib） |
| `tests/plugin_abi_load.rs` | 6 | 70.55 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **426** | — |

`src/` 相对 062 补记 `3a92515` 零 diff，测试仅作回归不作质量结论。

## 3. 守卫与 CI

| 守卫 | 输出 |
| --- | --- |
| `panic_guard` | `PANIC_GUARD_OK files 44 hits 0` |
| `semver_guard` | `SEMVER_GUARD_OK version_files 4 hits 0` |
| `i18n_guard` | `I18N_GUARD_OK rs_files 44 ux_html 1 hits 0 inline_bilingual_cn_lines 121` |
| `lang_guard` | `LANG_GUARD_OK locales zh-CN en-US keys 26 ...` |
| `policy_guard` | `POLICY_GUARD_OK g1_033_closed ... g8_054_retracted` |
| `delivery_guard` | `DELIVERY_GUARD_OK rounds=[56, 57, 61, 62, 63] g1_spec ... g8_ci_step` |
| `p09_scan` | `P09_HITS 0 []` |
| `api_guard` | `API_GUARD_OK flat_pub_use=0 v1_symbols=6 scattered=0` |
| `popup_guard` | `POPUP_GUARD_OK specs=13 ids_unique=13 close_path=all catalog_derived unknown_rejected` |

按 `.github/workflows/ci.yml` 真实命令复跑：`NO_EXPLANATORY` / `NO_HARDCODE` / `NO_CREDENTIAL`。50 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 326 项 `MISSING 0`。

一处环境事实：沙盒会话重置全局 git 配置，每次 `git` 前需 `git config --global --add safe.directory`；与仓库内容无关，不计失败项。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| 主交付与仓库副本 SHA-256 一致 | ``da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01`（两处一致）` |
| `src/` 相对 062 补记 diff | ``0`（相对 `3a92515`，`src/ Cargo.toml Cargo.lock vendor/` 全部零 diff）` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 零 diff，26 包 / 25 第三方 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |

## 5. 交付比对

| 项 | 值 |
| --- | --- |
| 本地 HEAD | `706e885`（主快照）→ 063 补记（1093 文件，DIRTY 0） |
| 远端 `refs/heads/main` | 主快照 `619650d6773bacc8f83e3d8ef1298fff2939b1f3`；063 补记以该 ref 为父，`force=false` |
| 逐项 ALL_MATCH | **True**（1093 / 1093，DIFF 0 / EXTRA 0 / truncated False） |
| 主包 / 预览包 | 1093 / 57 项，EXTRA 0 / MISSING 0 |

## 6. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 候选清单、逐字对照、零功能加入、零新增依赖、`**387 / 0**`、九守卫、远端逐项一致 |
| 已失败（不补写） | 035–047 历史格式缺失 |
| 未证实 | 6 项低可信度转述、逐版本归属、AX23 冲突处置、EQ-01 ~ EQ-13、4 条 Q-C |
| 未启动 | AX01–AX24、UI 渲染接线、真实网络 IO、UI 宿主、崩溃分析、子进程隔离 |
| 受阻 | 无（远端 Git Data API 通道正常；隐私政策全文为下轮输入，不计受阻） |

独立验证仍「部分通过」，存在未证实与未启动项，不发通过标记。

## 063 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `'+REF+'`（增量 tree `89572f2`，13 个变化 blob，`force=false`） |
| 本地主快照 | `706e885` |
| 主快照逐项比对 | `LOCAL 1093 / REMOTE 1093 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| 推送方式 | 13-blob 精简增量 + `base_tree`；未走全量 `api_push.py`，RC=0 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过」，未发通过标记；交付层已闭环，未证实 / 未启动项不变 |

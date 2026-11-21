# 062 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/62-round-062-instructions.txt`；`docs/decisions/062-api-surface-and-popup-registry.md` |
| 独立验证口径 | 实现层与交付层分开判；测试仅作回归，不作质量结论 |

## 1. 原文复读

`docs/records/round-062-full-readback.md`：5 份文件字节 / 行 / SHA-256 表；11 个原文锚点逐字回显。复读在写任何代码之前完成。

## 2. 测试

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**387 / 0**（381 + 6），零 warning` |
| 全量 `cargo test --offline` | `**426 / 0**（8 段全部 ok）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 13.66 s / 零 warning**（修 E165 后）` |

全量 8 段逐项（拆三段执行，避免网关 502 截断）：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 387 | 0.16 s |
| `tests/boot_fallback.rs` | 6 | 0.07 s |
| `tests/http_construct.rs` | 7 | 0.00 s |
| `tests/play_stats.rs` | 7 | 0.06 s |
| `tests/plugin_lifecycle_load.rs` | 7 | 62.28 s（真加载 cdylib） |
| `tests/window_handle_contract.rs` | 6 | 0.00 s |
| `tests/plugin_abi_load.rs` | 6 | 145.26 s（真加载 cdylib） |
| `Doc-tests kcu_core` | 0 | 0.00 s |
| **合计** | **426** | — |

061 全量 420 → 062 全量 426，增量恰为 `popup.rs` 新增 6 个测试；原有断言一字未改。`tests/boot_fallback.rs:3` 只改 import 路径，不动断言。

## 3. 守卫

| 守卫 | 输出 |
| --- | --- |
| `panic_guard` | `PANIC_GUARD_OK files 44 hits 0` |
| `semver_guard` | `SEMVER_GUARD_OK version_files 4 hits 0` |
| `i18n_guard` | `I18N_GUARD_OK rs_files 44 ux_html 1 hits 0 inline_bilingual_cn_lines 121` |
| `lang_guard` | `LANG_GUARD_OK locales zh-CN en-US keys 26 ...` |
| `policy_guard` | `POLICY_GUARD_OK g1_033_closed ... g8_054_retracted` |
| `delivery_guard` | `DELIVERY_GUARD_OK rounds=[56, 57, 61, 62] g1_spec ... g8_ci_step` |
| `p09_scan` | `P09_HITS 0 []` |
| `api_guard`（062 新增） | `API_GUARD_OK flat_pub_use=0 v1_symbols=6 scattered=0` |
| `popup_guard`（062 新增） | `POPUP_GUARD_OK specs=13 ids_unique=13 close_path=all catalog_derived unknown_rejected` |

按 `.github/workflows/ci.yml` 真实命令复跑：`NO_EXPLANATORY` / `NO_HARDCODE` / `NO_CREDENTIAL`。49 份演示 HTML 的 `<script>` 语法 `BAD 0`；`docs/index.md` 必读 320 项 `MISSING 0`。CI `scan` 新增 `api_guard` / `popup_guard` 两步。

## 4. 双向注入

| 注入 | 动作 | 结果 |
| --- | --- | --- |
| A | `往 `src/lib.rs` 追加一行 `pub use core::popup::PopupRegistry;`（顶层平铺回潮）` | ``API_GUARD_FAIL reason=top_level_pub_use=1`，RC=1；恢复后 OK` |
| B | `把 `open_registered` 的 `.ok_or(PopupOpenError::UnknownId)?` 换成 `.unwrap_or(&POPUP_SPECS[0])`（未知 id 不拒绝）` | ``POPUP_GUARD_FAIL reason=unknown_id_not_rejected` RC=1；`unknown_id_is_rejected_and_does_not_enter_registry` FAILED 1 项（`left Ok(()) right Err(UnknownId)`）RC=101` |
| 恢复 | 文件哈希与备份一致 + 复跑 | `两备份哈希逐项一致；`API_GUARD_OK` / `POPUP_GUARD_OK`；`cargo test --offline --lib` **387 / 0**，RC=0` |

注入 A 回显：

```
=== INJECT A: 恢复一行顶层 pub use ===
API_GUARD_FAIL reason=top_level_pub_use=1
A_RC=1
```

注入 B 回显：

```
POPUP_GUARD_FAIL reason=unknown_id_not_rejected
B_GUARD_RC=1
assertion `left == right` failed
  left: Ok(())
 right: Err(UnknownId)
failures: core::popup::tests::unknown_id_is_rejected_and_does_not_enter_registry
test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 386 filtered out
B_TEST_RC=101
```

恢复：`API_GUARD_OK` / `POPUP_GUARD_OK` / `387 passed; 0 failed` / RC=0；`sha256sum src/lib.rs` 与备份一致（`03bd9f8d…`）、`src/core/popup.rs` 与备份一致（`973dc0d1…`）。失败数量按实记录各 1 项，未补凑断言（A199）。测试文件未因注入修改断言。

## 5. 交付比对

| 项 | 值 |
| --- | --- |
| 本地 HEAD | `42e8c25`（主快照）→ 062 补记（1087 文件，DIRTY 0） |
| 远端 `refs/heads/main` | 主快照 `e53f67e515eb5770d732f0fea3aeffe9e058fd60`；062 补记以该 ref 为父，`force=false` |
| 逐项 ALL_MATCH | **True**（1087 / 1087，DIFF 0 / EXTRA 0 / truncated False） |
| 主包 | 1087 项，EXTRA 0 / MISSING 0；预览包 57 项 |

## 6. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | B11 代码层消除、B12 补登记、B04 局部落地、13 条 spec、`**387 / 0**（381 + 6），零 warning`、八守卫、双向注入、零新增依赖 |
| 已失败（不补写） | 035–047 历史格式缺失 |
| 未证实 | EQ-01 ~ EQ-13、4 条 Q-C、B05 / B07 / B09 / B10 |
| 未启动 | UI 渲染接线、真实网络 IO、UI 宿主、崩溃分析、子进程隔离 |
| 受阻 | 无（055–059 远端受阻已于 060 解除；本轮 Git Data API 通道正常） |

独立验证仍「部分通过」，存在未证实与未启动项，不发通过标记。

## 062 补记：远端写入闭环

| 项 | 值 |
| --- | --- |
| 远端主快照 | `'+REF+'`（增量 tree `3de197d`，22 个变化 blob，`force=false`） |
| 本地主快照 | `42e8c25` |
| 逐项比对 | `LOCAL 1087 / REMOTE 1087 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True` |
| E168 | `api_push.py` 后台两次被网关 502 清掉、前台 HTTP 超时；改精简增量推送后 RC=0，不重写历史、不强推 |
| 凭据 | 会话内有效 PAT 经环境变量传入；未写入仓库、日志或包；临时脚本与日志用后即删 |
| 独立验证结论 | 仍「部分通过」，未发通过标记；实现层与交付层已闭环，未证实 / 未启动项不变 |

# 061 独立验证报告

| 项 | 值 |
| --- | --- |
| 编号 | 061 |
| 独立验证结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/decisions/061-play-stats.md` V1–V7 |
| 远端 `refs/heads/main` | 061 补记覆盖 |

## 1. 时间戳

开工 `Fri Nov 20 00:19:02 CST 2026`；最终 `Fri Nov 20 13:42:43 CST 2026`。

## 2. 开工复读证据

`docs/records/round-061-full-readback.md`：5 份原文逐行遍历、字节 / 行 / SHA-256。

| 文件 | 字节 | 行 | SHA-256 前 12 |
| --- | --- | --- | --- |
| `00-requirements.txt` | 16422 | 261 | `23ffbf3fe341` |
| `ai-errors.md` | 41234 | 443 | `5f763a0678a1` |
| `11-features-input.txt` | 17096 | 268 | `1c3ff1a28286` |
| `12-server-features-input.txt` | 4970 | 64 | `03a62d90a232` |
| `61-round-061-instructions.txt` | 3 | 1 | `9ee0280bc49c` |

原文锚点：`11-features-input.txt:226`（第 19 条四项）、`:233`（第 26 条限额 3）、`00-requirements.txt:181/182/109-114`。

## 3. 构建与测试（命令 + 输出）

| 编号 | 命令 | 输出 |
| --- | --- | --- |
| V1 | `cargo test --offline --lib` | `test result: ok. 381 passed; 0 failed` |
| V2 | `cargo test --offline --test play_stats` | `test result: ok. 7 passed; 0 failed; finished in 0.06s` |
| V3 | `cargo test --offline`（全量） | `**420 / 0**（8 段全部 ok，RC=0）` |
| V4 | `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile ... in 1m 01s`，RC=0 |
| V5 | `cargo --version` / `rustc --version` | `1.99.1 (5f94df478 2026-08-27)` / `1.99.1 (58cf8f9c3 2026-10-13)` |

工具链环境变量：`CARGO_HOME=/data/workspace/.cargo-home`、`RUSTUP_HOME=/data/workspace/.rustup-home`、`PATH` 加 `.cargo-home/bin`（E147）。长命令走后台 Popen + 日志/rc 分片读取（E151）；全量与 Windows 检查并行时 cargo 文件锁排队，两进程均正常完成（E150）。

`全量 8 段逐项：

| 段 | 通过 | 耗时 |
| --- | --- | --- |
| `unittests src/lib.rs` | 381 | 0.90s |
| `tests/boot_fallback.rs` | 6 | 0.07s |
| `tests/http_construct.rs` | 7 | 0.01s |
| `tests/play_stats.rs` | 7 | 0.01s |
| `tests/plugin_abi_load.rs` | 6 | 249.71s（真加载 cdylib） |
| `tests/plugin_lifecycle_load.rs` | 7 | 117.22s（真加载 cdylib） |
| `tests/window_handle_contract.rs` | 6 | 0.01s |
| `Doc-tests kcu_core` | 0 | 0.00s |
| **合计** | **420** | — |

恢复注入后单独复跑 `cargo test --offline --lib` → `381 passed; 0 failed`，RC=0；`sha256sum src/core/stats.rs` 与备份一致，`schema` 校验段存在。`

## 4. 守卫与扫描

| 命令 | 输出 |
| --- | --- |
| `python3 scripts/panic_guard.py` | `PANIC_GUARD_OK files 42 hits 0` |
| `python3 scripts/semver_guard.py` | `SEMVER_GUARD_OK` |
| `python3 scripts/i18n_guard.py` | `I18N_GUARD_OK` |
| `python3 scripts/lang_guard.py` | `LANG_GUARD_OK` |
| `python3 scripts/policy_guard.py` | `POLICY_GUARD_OK` |
| `python3 scripts/delivery_guard.py` | `DELIVERY_GUARD_OK rounds=[56, 57, 61]` |
| `python3 scripts/p09_scan.py` | `P09_HITS 0 []` |
| `.github/workflows/ci.yml` 三个 job | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` |

`六守卫实测：

| 守卫 | 输出 |
| --- | --- |
| `panic_guard` | `PANIC_GUARD_OK files 43 hits 0` |
| `semver_guard` | `SEMVER_GUARD_OK version_files 4 hits 0` |
| `i18n_guard` | `I18N_GUARD_OK rs_files 43 ux_html 1 hits 0 inline_bilingual_cn_lines 121` |
| `lang_guard` | `LANG_GUARD_OK locales zh-CN en-US keys 26 data_cn_zh 510 stable_values_ok offline_refs_ok` |
| `policy_guard` | `POLICY_GUARD_OK g1_033_closed ... g8_054_retracted` |
| `delivery_guard` | `DELIVERY_GUARD_OK rounds=[56, 57, 61] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step` |
| `p09_scan` | `P09_HITS 0 []` |

按 `.github/workflows/ci.yml` 真实命令复跑：`NO_EXPLANATORY` / `NO_HARDCODE` / `NO_CREDENTIAL`。首跑 `credential` 得到 `CREDENTIAL_FOUND`，定位到 `docs/records/push-credential-audit.md:65` 与 `docs/records/rounds.md:3218` 两处**历史文档**用凭据前缀字面量描述形态（059 起存量失败项，非本轮引入，E152），改成等义描述后复跑 `NO_CREDENTIAL`。`hardcode` job 只扫 `src/`，`tests/http_construct.rs` 里的测试 URL 字面量不在该 job 范围；首版自作主张扫 `src/+tests/` 得到误报，按 CI 真实命令复核后更正（E155）。`

## 5. 双向注入

| 注入 | 改动 | 结果 |
| --- | --- | --- |
| A | `src/core/stats.rs` 的 `show_popup: !silent` 改为 `show_popup: true` | ``core::stats::tests::silent_record_keeps_data_but_suppresses_popup` FAILED 1 项，`assertion failed: !o.show_popup` at `src/core/stats.rs:359`，`test result: FAILED. 0 passed; 1 failed; 380 filtered out`，RC=101` |
| B | `parse_stats` 的 `schema` 校验段删除 | ``core::stats::tests::malformed_and_wrong_schema_files_fall_back` FAILED 1 项，`assertion left == right failed / left: 7 / right: 0`，`test result: FAILED. 0 passed; 1 failed; 380 filtered out`，RC=101` |
| 恢复 | `git checkout` 备份还原后复跑 | ``sha256sum src/core/stats.rs` 与 `/data/workspace/.stats061.bak` 一致（`ab8d45e4…`），`stats schema` 校验段存在；`cargo test --offline --lib` → `381 passed; 0 failed`，RC=0` |

失败回显保留在本报告下方；测试文件未因注入修改断言（§9.2）。

`注入 A 失败回显：

```
--- RUN stats::tests::silent_record_keeps_data_but_suppresses_popup ---
thread 'core::stats::tests::silent_record_keeps_data_but_suppresses_popup' panicked at src/core/stats.rs:359:9:
assertion failed: !o.show_popup
failures: core::stats::tests::silent_record_keeps_data_but_suppresses_popup
test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 380 filtered out
RC=101
```

注入 B 失败回显：

```
--- RUN stats::tests::malformed_and_wrong_schema_files_fall_back ---
assertion `left == right` failed
  left: 7
 right: 0
failures: core::stats::tests::malformed_and_wrong_schema_files_fall_back
test result: FAILED. 0 passed; 1 failed; 0 ignored; 0 measured; 380 filtered out
RC=101
```

后台注入脚本在 `RESTORE` 段被网关 502 清掉进程组，未写出 rc（E154）；不据此宣称恢复完成，改用文件哈希 + `schema` 校验存在性 + 单独复跑 381 / 0 三项外部证据。失败数量按实记录各 1 项，未补凑断言（A199）。测试文件未因注入修改断言。`

## 6. 交付比对

| 项 | 值 |
| --- | --- |
| 本地 HEAD | 061 补记覆盖（DIRTY 0） |
| 远端 `refs/heads/main` | 061 补记覆盖 |
| 逐项 ALL_MATCH | 061 补记覆盖 |
| 主包 | 按 `git ls-files` 打包，项数见 061 补记 |
| 零凭据 | tracked 零 token 字面量；`.git/config` 零 token；临时 PAT 与临时脚本用后即删 |
| `Cargo.toml` / `Cargo.lock` / `vendor/` | 一行未动，26 包 / 25 第三方 |
| UI | UX HTML、两语言包、56 张 PNG 零 diff |

## 7. 四值

| 项 | 值 |
| --- | --- |
| 第 19 条数据层、三项时长、静默口径、活跃上限 3、异常与删除边界 | 已证实 |
| 381 / 0、7 / 0、`**420 / 0**（8 段全部 ok，RC=0）`、Windows GNU、六守卫、双向注入 | 已证实 |
| 零新增依赖、零 UI diff | 已证实 |
| 远端逐项 ALL_MATCH | 061 补记覆盖 |
| 035–047 历史交付格式缺失 | 已失败（不补写） |
| B04 / B05 / B07 / B09 / B10、EQ-01 ~ EQ-13、4 条 Q-C | 未证实（待拍板） |
| 显示层、真实游戏进程结束事件源、真实网络 IO、UI 宿主、崩溃分析、子进程隔离 | 未启动 |
| GUI 端到端、Win7 / MSVC / i686 运行时 | 受阻 |

## 8. 结论

独立验证**部分通过**：实现层、回归层、交付层均有可复现外部证据，但存在「未证实（待拍板）」「未启动」「受阻」三类未解决项，按 §9 三条发放条件**未发通过标记**。自评 9.3 为辅助信号，不覆盖独立验证结论。

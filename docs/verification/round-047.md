# 第 047 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 047 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 底座正确性收尾轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 046 远端 `GET /git/ref/heads/main` | `4e059dc`，message `round 046 poison guard and envelope kind code` | 已证实 |
| V2 | `cargo test --offline --lib` | **269 / 0** | 已证实 |
| V3 | `cargo test --offline --lib updater::policy` | 12 / 0（原 9 + 新 3） | 已证实 |
| V4 | 行为反向验证（临时换回 `v == b`） | `FAILED`，`left: Reject / right: Install` | 已证实 |
| V5 | 守卫反向验证（临时换回 `v == b`） | `SEMVER_GUARD_HIT policy.rs:30 == b)`、`FAIL 1` | 已证实 |
| V6 | `python3 scripts/semver_guard.py`（恢复后） | `SEMVER_GUARD_OK version_files 3 hits 0` | 已证实 |
| V7 | `python3 scripts/panic_guard.py` | `PANIC_GUARD_OK files 36 hits 0` | 已证实 |
| V8 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V9 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V10 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，62.31 s | 已证实 |
| V11 | `cargo test --offline --test plugin_abi_load` | 6 / 0，121.15 s | 已证实 |
| V12 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V13 | `Cargo.lock` 包列表 | **26 包 / 25 第三方**（与 046 相同） | 已证实 |
| V14 | `git diff --name-only -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V15 | `git diff --name-only -- demos/preview/ demos/ui-full-kcu-paper.html` | 空（界面闸门未触发） | 已证实 |
| V16 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan，scan 含 semver_guard | 已证实 |
| V17 | `node new Function` 全部 demos HTML | ALL_JS_OK，37 份 | 已证实 |
| V18 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V19 | 禁用词 / 「同上」 / P09 / hardcode 扫描 | 零命中 | 已证实 |
| V20 | 必读文件循环 | REQUIRED=241 MISSING=0 | 已证实 |
| V21 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 回滚判定修正、双向验证、双守卫、295 / 0 | 已证实 |
| E85–E88 处置、零新增依赖 | 已证实 |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| Q-047-01（EQ-13） | 待拍板 |
| EQ-01 ~ EQ-12 | 已交具体环境，待拍板 |
| 295 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。

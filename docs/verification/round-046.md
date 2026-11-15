# 第 046 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 046 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 底座健壮性收尾轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 045 远端 `GET /git/ref/heads/main` | `53c9ed8`，message `round 045 environments and log poison` | 已证实 |
| V2 | `cargo test --offline --lib` | **266 / 0** | 已证实 |
| V3 | `cargo test --offline --lib core::cache::tests::poisoned` | 2 / 0 | 已证实 |
| V4 | `cargo test --offline --lib core::leak::tests::poisoned` | 1 / 0 | 已证实 |
| V5 | 反向验证（临时换回 `.unwrap()`） | 3 个毒化测试全 FAILED，回显 3 处连锁 panic | 已证实 |
| V6 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V7 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V8 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，28.45 s | 已证实 |
| V9 | `cargo test --offline --test plugin_abi_load` | 6 / 0，69.88 s | 已证实 |
| V10 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V11 | `python3 scripts/panic_guard.py` | `PANIC_GUARD_OK files 36 hits 0` | 已证实 |
| V12 | `git diff --name-only -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V13 | `Cargo.lock` 包列表 | **26 包 / 25 第三方**（与 045 相同） | 已证实 |
| V14 | `git diff --name-only -- demos/preview/ demos/ui-full-kcu-paper.html` | 空（界面闸门未触发） | 已证实 |
| V15 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan，scan 含 credential / wording / hardcode / panic_guard | 已证实 |
| V16 | `node new Function` 全部 demos HTML | ALL_JS_OK，36 份 | 已证实 |
| V17 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V18 | 禁用词 / 「同上」 / P09 / hardcode 扫描 | 零命中 | 已证实 |
| V19 | 必读文件循环 | REQUIRED=235 MISSING=0 | 已证实 |
| V20 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 毒化恢复全覆盖、协议字段显式化、CI 守卫、292 / 0 | 已证实 |
| 反向验证、E81–E84 处置、零新增依赖 | 已证实 |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| 第三方锁实现 | 未启动（U85） |
| EQ-01 ~ EQ-12 | 已交具体环境，待拍板 |
| 292 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。

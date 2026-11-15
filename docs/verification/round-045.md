# 第 045 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 045 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo test --offline --lib core::log` | **8 / 0**（原 6 + 毒化回归 2） | 已证实 |
| V2 | `cargo test --offline --lib` | **262 / 0** | 已证实 |
| V3 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V4 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V5 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0 | 已证实 |
| V6 | `cargo test --offline --test plugin_abi_load` | 6 / 0 | 已证实 |
| V7 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V8 | `Cargo.lock` 包列表 | **26 包 / 25 第三方**（与 044 相同，零新增依赖） | 已证实 |
| V9 | `git diff --name-only HEAD~1..HEAD -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V10 | `git diff --name-only -- demos/preview/ demos/ui-full-kcu-paper.html` | 空（界面闸门未触发） | 已证实 |
| V11 | `grep -rE 'https?://|C:\|x-api-key' src/` | NO_HARDCODE | 已证实 |
| V12 | `node new Function` 全部 demos HTML | ALL_JS_OK，35 份 | 已证实 |
| V13 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V14 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V15 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V16 | 必读文件循环 | REQUIRED=229 MISSING=0 | 已证实 |
| V17 | 环境清单 12 条 | EQ-01 ~ EQ-12 全部非空 | 已证实 |
| V18 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 锁中毒修复、288 / 0、Windows GNU、零新增依赖 | 已证实 |
| EQ-01 ~ EQ-12 具体环境、E79–E80 处置 | 已证实 |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| 第三方锁实现 | 未启动（U73 判不成立） |
| 288 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。

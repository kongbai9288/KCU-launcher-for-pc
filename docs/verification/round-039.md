# 第 039 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 039 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | Finished dev profile | 已证实 |
| V2 | `cargo test --offline --lib` | 216 passed / 0 failed | 已证实 |
| V3 | `cargo test --offline --test plugin_lifecycle_load` | 7 passed / 0 failed，50.50 s | 已证实 |
| V4 | `cargo test --offline --test plugin_abi_load` | 6 passed / 0 failed，125.71 s | 已证实 |
| V5 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V6 | `Cargo.lock` 包列表 | 17 包 / 16 第三方，与 038 一致 | 已证实 |
| V7 | `src/plugins/lifecycle.rs` | 150 行，4 个单测 | 已证实 |
| V8 | `tests/plugin_lifecycle_load.rs` | 7 个测试，`OnceLock` 缓存 2 个夹具 | 已证实 |
| V9 | 关于页许可行 / NOTICES / CI | 16 组、38、未改 | 已证实 |
| V10 | `demos/ui-full-kcu-paper.html` 与 `demos/preview/*.png` | 与 HEAD 完全一致，无 diff | 已证实 |
| V11 | `node new Function` 全部 demos HTML | ALL_JS_OK | 已证实 |
| V12 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V13 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V14 | 必读文件循环 | REQUIRED=193 MISSING=0 | 已证实 |
| V15 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 倒序卸载 / 只回滚本轮 / scope 归零 / 229 测试 | 已证实 |
| 同进程 C ABI 无法隔离崩溃（Nomicon + RFC 2945） | 已证实 |
| 子进程隔离、插件 init、真实 dll、macOS / musl 卸载 | 未启动 / 未证实 |
| MSVC / Win7 运行时 / MSRV 冲突 | 未证实 / 受阻 |
| 229 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 Windows 运行时、子进程隔离与 GUI 端到端验证；改动作者未代改验证结论，未降低验收项。

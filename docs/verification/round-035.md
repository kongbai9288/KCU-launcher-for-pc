# 第 035 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 035 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮，未新增第三方 crate，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 164 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 13 包 / 12 第三方，与 034 一致 | 已证实 |
| V4 | `grep -c 'expect(' src/core/config.rs` | 0 | 已证实 |
| V5 | `grep -c 'data\["' src/core/config.rs` | 0 | 已证实 |
| V6 | `grep -c 'ensure_object' src/core/config.rs` | 5 | 已证实 |
| V7 | `grep -c '#\[test\]' src/core/config.rs` | 10（原 7 + 新 3） | 已证实 |
| V8 | R01/R02/R03 上游 manifest 探测 | 三条一手数据均写入 035 决策 | 已证实 |
| V9 | 关于页许可表 / NOTICES | 12 组 / 34，本轮无变更 | 已证实 |
| V10 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V11 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V12 | 必读文件循环 | REQUIRED=171 MISSING=0 | 已证实 |
| V13 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 三条路线核完、改轨缺陷修复、164 / 0、零新依赖 | 已证实 |
| 正常路径行为一致 | 已证实 |
| Win7 Tier 3 下 toml MSRV 1.85、tracing-subscriber 闭包 | 未证实 |
| 上层能力（UI / 网络 / 崩溃 / 插件）、自动命令实现层 | 未启动 |
| 164 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。

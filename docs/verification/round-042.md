# 第 042 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 042 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 041 收口 `GET /git/ref/heads/main` + `GET /git/trees/main?recursive=1` | `599edc7`；REMOTE 852 LOCAL 852 MISMATCH 0 ALL_MATCH True | 已证实 |
| V2 | `cargo build --offline` | 编译 hex / percent-encoding / kcu-core，Finished | 已证实 |
| V3 | `cargo test --offline --lib` | **244 passed / 0 failed** | 已证实 |
| V4 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V5 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V6 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，36.19 s | 已证实 |
| V7 | `cargo test --offline --test plugin_abi_load` | 6 / 0，109.30 s | 已证实 |
| V8 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V9 | `Cargo.lock` 包列表 | **23 包 / 22 第三方** | 已证实 |
| V10 | `docs/licenses/pe-LICENSE-*.txt` / `hex-LICENSE-*.txt` | 1072 / 10847 / 1125 / 11358 字节 | 已证实 |
| V11 | 关于页许可行 / NOTICES | 22 组「构建中已使用」，计数 44，N41–N42 | 已证实 |
| V12 | `demos/preview/` 许可相关 4 张 | 重渲；其余 52 张回退到 HEAD | 已证实 |
| V13 | `grep -rE 'https?://|C:\|x-api-key' src/` | NO_HARDCODE | 已证实 |
| V14 | `node new Function` 全部 demos HTML | ALL_JS_OK，32 份 | 已证实 |
| V15 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V16 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V17 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V18 | 必读文件循环 | REQUIRED=211 MISSING=0 | 已证实 |
| V19 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| query 编码、hex 编码、270 / 0、Windows GNU | 已证实 |
| 041 收口 852 文件 ALL_MATCH、E63–E66 修复 | 已证实 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动 |
| Q-041 / Q-037-01 / 真实窗口 / 崩溃分析 | 未证实 / 未启动 |
| 270 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。

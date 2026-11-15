# 第 044 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 044 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双声「干」收口轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 043 补验 `GET /git/ref/heads/main` | `8bb96d6`，message `round 043 request id uuid v5` | 已证实 |
| V2 | 043 补验 `GET /git/trees/main?recursive=1` | REMOTE 922 LOCAL 922 MISMATCH 0 ALL_MATCH True，truncated=False | 已证实 |
| V3 | `cargo build --offline` | 编译 memchr / serde_json / quick-xml / kcu-core，Finished | 已证实 |
| V4 | `cargo test --offline --lib` | **260 passed / 0 failed** | 已证实 |
| V5 | `cargo test --offline --lib plugins::icon` | 19 / 0（原 8 + 新 11） | 已证实 |
| V6 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V7 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V8 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，36.78 s | 已证实 |
| V9 | `cargo test --offline --test plugin_abi_load` | 6 / 0，114.64 s | 已证实 |
| V10 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V11 | `Cargo.lock` 包列表 | **26 包 / 25 第三方**（+quick-xml，零新增传递依赖） | 已证实 |
| V12 | `docs/licenses/quick-xml-LICENSE-MIT.txt` | 1082 字节，逐字副本 | 已证实 |
| V13 | 关于页许可行 / NOTICES | 25 组「构建中已使用」，计数 47，N45 | 已证实 |
| V14 | `demos/preview/` 许可相关 4 张 | 重渲；其余 52 张回退到 HEAD | 已证实 |
| V15 | `grep -rE 'https?://|C:\|x-api-key' src/` | NO_HARDCODE | 已证实 |
| V16 | `node new Function` 全部 demos HTML | ALL_JS_OK，34 份 | 已证实 |
| V17 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V18 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V19 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V20 | 必读文件循环 | REQUIRED=223 MISSING=0 | 已证实 |
| V21 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| quick-xml 校验、286 / 0、Windows GNU | 已证实 |
| 043 推送补验 922 文件 ALL_MATCH、E72–E76 修复 | 已证实 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动 |
| Q-041 / Q-037-01 / 真实窗口 / 崩溃分析 | 未证实 / 未启动 |
| 286 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。

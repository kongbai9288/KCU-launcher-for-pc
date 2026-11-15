# 第 041 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 041 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 raw-window-handle / kcu-core，Finished | 已证实 |
| V2 | `cargo test --offline --lib` | 237 passed / 0 failed | 已证实 |
| V3 | `cargo test --offline --test window_handle_contract` | 6 passed / 0 failed | 已证实 |
| V4 | `cargo test --offline --test http_construct` | 7 passed / 0 failed | 已证实 |
| V5 | `cargo test --offline --test plugin_lifecycle_load` | 7 passed / 0 failed，43.18 s | 已证实 |
| V6 | `cargo test --offline --test plugin_abi_load` | 6 passed / 0 failed，111.95 s | 已证实 |
| V7 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V8 | `Cargo.lock` 包列表 | 21 包 / 20 第三方 | 已证实 |
| V9 | `docs/licenses/rwh-LICENSE-*.md` | 1064 / 10174 / 836 字节 | 已证实 |
| V10 | 关于页许可行 / NOTICES | 20 组「构建中已使用」，计数 42，N38–N40 | 已证实 |
| V11 | `demos/preview/` 许可相关 4 张 | 重渲；其余 52 张回退到 HEAD | 已证实 |
| V12 | `grep -rE 'https?://|C:\|x-api-key' src/` | NO_HARDCODE | 已证实 |
| V13 | `node new Function` 全部 demos HTML | ALL_JS_OK，31 份 | 已证实 |
| V14 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V15 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V16 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V17 | 必读文件循环 | REQUIRED=205 MISSING=0 | 已证实 |
| V18 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |
| V19 | `scripts/api_push.py` 增量树推送 | 852 文件，base_tree 增量条目，ref 更新成功 | 已证实 |

| 项 | 值 |
| --- | --- |
| 句柄类型层、263 / 0、Windows GNU 编译 | 已证实 |
| UI 宿主 / 崩溃分析两条栈判不成立 | 已证实 |
| Win7 + WebView2 官方口径不成立 | 已证实 |
| 真实窗口 / WebView / 渲染 / 崩溃分析 | 未启动 |
| Win7 UI 路线取舍、dpi 仓库、MSVC / Win7 运行时 | 未证实 / 受阻 |
| 263 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实窗口创建、WebView 加载、崩溃捕获与 GUI 端到端验证；改动作者未代改验证结论，未降低验收项。

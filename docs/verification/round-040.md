# 第 040 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 040 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 fnv / bytes / http / kcu-core，Finished | 已证实 |
| V2 | `cargo test --offline --lib` | 227 passed / 0 failed | 已证实 |
| V3 | `cargo test --offline --test http_construct` | 7 passed / 0 failed | 已证实 |
| V4 | `cargo test --offline --test plugin_lifecycle_load` | 7 passed / 0 failed，43.27 s | 已证实 |
| V5 | `cargo test --offline --test plugin_abi_load` | 6 passed / 0 failed，110.86 s | 已证实 |
| V6 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V7 | `Cargo.lock` 包列表 | 20 包 / 19 第三方 | 已证实 |
| V8 | `vendor/*/src` 与上游 tag tarball | 逐字节一致（manifest 裁剪除外） | 已证实 |
| V9 | `docs/licenses/` 新增 5 份 | 1059 / 10835 / 1055 / 1056 / 10847 字节 | 已证实 |
| V10 | 关于页许可行 / NOTICES | 19 组「构建中已使用」，计数 41，N35–N37 | 已证实 |
| V11 | `demos/preview/22-licenses.png` 等 4 张 | 重渲，其余 52 张回退到 HEAD | 已证实 |
| V12 | `grep -rE 'https?://|C:\|x-api-key' src/` | NO_HARDCODE（修掉 037 存量命中后） | 已证实 |
| V13 | `node new Function` 全部 demos HTML | ALL_JS_OK | 已证实 |
| V14 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V15 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V16 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V17 | 必读文件循环 | REQUIRED=199 MISSING=0 | 已证实 |
| V18 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 请求构造标准化、247 / 0、Windows GNU 编译 | 已证实 |
| reqwest / ureq / rustls 三条网络栈判不成立 | 已证实 |
| 真实网络 IO、TLS、密钥头、编码、代理 | 未启动 |
| Win7 TLS 系统前置、MSRV 冲突、rustls Win7 运行时 | 未证实 / 受阻 |
| 247 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTPS 请求、Windows 运行时与 GUI 端到端验证；改动作者未代改验证结论，未降低验收项。

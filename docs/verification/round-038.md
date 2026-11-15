# 第 038 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 038 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 cfg-if / libloading / kcu-core，Finished | 已证实 |
| V2 | `cargo test --offline` | 212 passed / 0 failed（lib） | 已证实 |
| V3 | `cargo test --offline` | 6 passed / 0 failed（集成，复跑 133.97 s；首次 117.35 s） | 已证实 |
| V4 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished dev profile | 已证实 |
| V5 | `Cargo.lock` 包列表 | 17 包 / 16 第三方 | 已证实 |
| V6 | `vendor/*/src` 与上游 tarball / commit | 逐字节一致（manifest 裁剪除外） | 已证实 |
| V7 | `docs/licenses/` 新增 5 份 | 736 / 1057 / 10847 / 1141 / 11351 字节 | 已证实 |
| V8 | 关于页许可行 / NOTICES | 16 组「构建中已使用」，计数 38，N32–N34 | 已证实 |
| V9 | `demos/preview/22-licenses.png` 等 4 张 | 重渲，其余 52 张回退到 HEAD | 已证实 |
| V10 | `node new Function` 全部 demos HTML | ALL_JS_OK | 已证实 |
| V11 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan，含 windows-abi-check | 已证实 |
| V12 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V13 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V14 | 必读文件循环 | REQUIRED=187 MISSING=0 | 已证实 |
| V15 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 插件 ABI 契约与库化加载、Windows GNU 编译 | 已证实 |
| MSVC / Win7 运行时 / 真实 dll / 子进程隔离 | 未证实 / 受阻 |
| 218 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 Windows 运行时与 GUI 端到端验证；改动作者未代改验证结论，未降低验收项。

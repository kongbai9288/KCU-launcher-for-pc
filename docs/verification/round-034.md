# 第 034 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 034 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 semver 1.0.28 / kcu-core，`Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 161 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 13 包 / 12 第三方，semver 零传递依赖 | 已证实 |
| V4 | `grep -c 'cmp_precedence' src/core/instance.rs` | 1 | 已证实 |
| V5 | `grep -c 'VersionReq::parse' src/core/instance.rs` | 1 | 已证实 |
| V6 | `grep -c '#\[test\]' src/core/instance.rs` | 13（原 5 + 新 8） | 已证实 |
| V7 | `vendor/semver/src/lib.rs` 与上游 tarball | 逐字节一致 | 已证实 |
| V8 | `docs/licenses/semver-LICENSE-*.txt` | 1023 / 9723 字节 | 已证实 |
| V9 | 关于页许可行 / NOTICES | 12 组「构建中已使用」，计数 34，含 semver | 已证实 |
| V10 | `demos/preview/22-licenses.png` 等 4 张 | 重渲，非空 | 已证实 |
| V11 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V12 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V13 | 必读文件循环 | REQUIRED=166 MISSING=0 | 已证实 |
| V14 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 版本匹配库化、161 / 0、B11 / B12 新增能力 | 已证实 |
| B14 带前缀版本名、加载器逐版本 schema、CF F17 | 未证实 |
| 自动命令实现层、真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 161 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。

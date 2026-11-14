# 第 036 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 036 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 ed25519-compact 2.6.1 / kcu-core，`Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 179 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 14 包 / 13 第三方，ed25519-compact 零传递依赖 | 已证实 |
| V4 | `grep -c '#\[test\]' src/updater/*.rs` | 15（verify 6 + policy 9） | 已证实 |
| V5 | `grep -c 'cmp_precedence' src/updater/policy.rs` | 1 | 已证实 |
| V6 | `vendor/ed25519-compact/src/lib.rs` 与上游 tarball | 逐字节一致 | 已证实 |
| V7 | `docs/licenses/ed25519-compact-LICENSE.txt` | 1073 字节，MIT / Frank Denis | 已证实 |
| V8 | 关于页许可行 / NOTICES | 13 组「构建中已使用」，计数 35，含 ed25519-compact | 已证实 |
| V9 | `demos/preview/22-licenses.png` 等 4 张 | 重渲，非空 | 已证实 |
| V10 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V11 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V12 | 必读文件循环 | REQUIRED=176 MISSING=0 | 已证实 |
| V13 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 上层第一块库化、179 / 0、U01–U07 | 已证实 |
| 公钥来源 / 插件包格式 / 密钥轮换、Win7 交叉编译 | 未证实 / 受阻 |
| UI 宿主 / 真实网络 / 崩溃分析 / 插件 ABI / 更新器其余部分 | 未启动 |
| 179 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。

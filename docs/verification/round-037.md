# 第 037 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 037 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双轨轮，界面层仅演示；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 207 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 14 包 / 13 第三方，与 036 一致 | 已证实 |
| V4 | `grep -c '#\[test\]' src/plugins/*.rs` | 28 | 已证实 |
| V5 | `grep -c 'user_confirmed_upgrade' src/plugins/upgrade.rs` | 3 | 已证实 |
| V6 | `grep -c 'assert_eq!(r.len(), 13)' src/core/popup.rs` | 1 | 已证实 |
| V7 | `grep -c 'plug-q' demos/ui-full-kcu-paper.html` | 2 | 已证实 |
| V8 | `node new Function` 整页 UX 脚本 | 通过 | 已证实 |
| V9 | `python3 scripts/render_ui.py` | 51 shots + overview | 已证实 |
| V10 | 三张新 PNG 目视复核 | 问号 / 升级按钮 / 故障三动作均可见 | 已证实 |
| V11 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V12 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V13 | 必读文件循环 | REQUIRED=181 MISSING=0 | 已证实 |
| V14 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 业务层三条口径与 207 / 0 | 已证实 |
| 界面实现 | 未启动（仅演示） |
| 身份哈希解读、插件包格式、公钥分发、ABI、Win7 | 未证实 / 受阻 |
| 207 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。

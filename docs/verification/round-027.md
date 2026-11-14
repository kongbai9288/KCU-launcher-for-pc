# 第 027 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 027 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 工程轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile`；编译 crossbeam-utils / crossbeam-channel / kcu-core | 已证实 |
| V2 | `cargo test --offline` | 141 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 8 包，7 个第三方 | 已证实 |
| V4 | `git diff 28a646b -- src/core/asynk.rs` | 删除 mpsc / AtomicUsize / LiveGuard / JoinHandle 循环 | 已证实 |
| V5 | `grep -c 'crossbeam' src/core/asynk.rs` | 4 | 已证实 |
| V6 | `ls docs/licenses/crossbeam*` | 4 份全文 | 已证实 |
| V7 | `grep -c '构建中已使用' demos/ui-full-kcu-paper.html` | 7 | 已证实 |
| V8 | `python3 scripts/render_ui.py` | `render_ui OK shots=43` | 已证实 |
| V9 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V10 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V11 | 必读文件循环 | REQUIRED=133 MISSING=0 | 已证实 |
| V12 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 第三方运行时 7 组、手写并发原语删除、许可全文齐备 | 已证实 |
| 141 测试仅作回归，不作质量结论 | 已证实 |
| B05-B08 行为差异已登记、测试断言未降级 | 已证实 |
| cache / leak / launcher / lightweight 替换 | 未启动 |
| mini-moka 大闭包、真实网络 / GUI / Win7 / CI 独立构建 | 受阻 |

限制：本轮只换 asynk 一块，未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。

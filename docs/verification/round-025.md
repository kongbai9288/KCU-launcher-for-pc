# 第 025 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 025 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 工程轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `CARGO_INCREMENTAL=0 cargo build --offline` | `Finished dev profile`；编译 itoa / memchr / ryu / serde_core / serde_json / kcu-core | 已证实 |
| V2 | `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | `['itoa','kcu-core','memchr','ryu','serde_core','serde_json']` | 已证实 |
| V4 | `grep -c '^name = ' Cargo.lock` | 6 | 已证实 |
| V5 | `src/dispatcher/json.rs` 行数 | 77（024 为 336） | 已证实 |
| V6 | `git diff 379dc97..HEAD -- src/` | json.rs 删除手写解析器、task.rs / launcher.rs / mod.rs 适配 | 已证实 |
| V7 | `du -sh vendor` / `find vendor -type f` | 1.7M / 146 文件 | 已证实 |
| V8 | `ls docs/licenses/*-LICENSE-* \| wc -l` | 9 份新增 | 已证实 |
| V9 | `grep -c '构建中已使用' demos/ui-full-kcu-paper.html` | 5 | 已证实 |
| V10 | `python3 scripts/render_ui.py` | `render_ui OK shots=43` | 已证实 |
| V11 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V12 | `python3 scripts/p09_scan.py` | P09_HITS 0 | 已证实 |
| V13 | 禁用词 / 「同上」 / 品牌外链扫描 | 全部零命中 | 已证实 |
| V14 | 必读文件循环 | REQUIRED=128 MISSING=0 | 已证实 |
| V15 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 第三方 crate 真实进构建、手写 JSON 解析器删除、许可全文齐备 | 已证实 |
| 141 测试通过仅作回归，不作质量结论 | 已证实（024 W03 延续） |
| 深度上限 64 → 128 的行为差异 | 已证实；测试相应改为 200 层，断言未降级 |
| memchr 的 Unlicense 全文 | 受阻（上游仓库只提供 LICENSE-MIT，按 MIT 条款使用并如实登记） |
| 剩余自写模块替换、真实运行时、浏览器点击、Win7 构建、CI 独立构建 | 受阻 / 未证实 |

限制：本轮 vendor 源码由工具脚本搬运并落 `.cargo-checksum.json`，上游 `src/` 未改动；未引入 registry 在线依赖，未做真实网络与 GUI 验证。改动作者未代改验证结论，未降低验收项。

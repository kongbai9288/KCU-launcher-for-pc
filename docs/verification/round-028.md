# 第 028 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 028 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 139 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 8 包 / 7 第三方，与 027 一致 | 已证实 |
| V4 | `git diff d5bd76d -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V5 | `grep -rnE 'Tracker|Tracked' src/` | 零命中 | 已证实 |
| V6 | `wc -l src/core/leak.rs` | 191 → 99 | 已证实 |
| V7 | `git ls-files src/server` | 输出为空 | 已证实 |
| V8 | 三份功能 md 五字段计数 | 各 5 个固定小节 | 已证实 |
| V9 | `docs/research/20-server-log-events.md` URL 计数 | 15 条来源、13 个独立 URL、16 次出现 | 已证实 |
| V10 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V11 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V12 | `python3 scripts/render_ui.py` 未调用、`demos/ui-full-*.html` 未改 | UI 闸门未触发 | 已证实 |
| V13 | 必读文件循环 | REQUIRED=137 MISSING=0 | 已证实 |
| V14 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 三项新功能只落文档、零实现、五字段齐备 | 已证实 |
| leak.rs 自写计数删除、139 / 0、依赖不变 | 已证实 |
| 141 → 139 的差值为删除 2 个自写模块自带测试，等价断言已迁移 | 已证实 |
| 官方日志格式原文、模式矩阵、真实联调 | 未证实 |
| 浏览器图表渲染、Win7 / 多架构、CI 独立构建 | 受阻 |
| UI 整页演示 | 未触发（本轮不动界面） |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。

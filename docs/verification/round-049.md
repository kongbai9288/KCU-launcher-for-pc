# 第 049 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 049 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；`src/` 零改动，cargo 仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `6a8bbe5`，DIRTY 0，1000 文件 | 已证实 |
| V2 | 048 远端 ref（048 收尾已核） | `cb20450` | 已证实 |
| V3 | 临时凭据扫描 | `NO_CREDENTIAL`，`.git/config` 干净 | 已证实 |
| V4 | `node` 求值两个语言包 | 各 24 键，纯数据 | 已证实 |
| V5 | `node new Function` 主脚本 | 通过 | 已证实 |
| V6 | 39 份 demos HTML 脚本 | ALL_JS_OK | 已证实 |
| V7 | Playwright `file://` 打开 | 两语言包加载，0 控制台错误 | 已证实 |
| V8 | 中文态导航 | 「首页」，`NOTICES=6 SERVERS=9` | 已证实 |
| V9 | 点击 `#btnLang` 切英文 | `LOCALE=en-US`，导航「Home」，数组长度不变 | 已证实 |
| V10 | 切回中文 | 「首页」，`NOTICES=6` | 已证实 |
| V11 | 改 `SERVERS[0].lock=false; ping=99` 后往返切换 | `lock=false ping=99 n=9` | 已证实 |
| V12 | `python3 scripts/lang_guard.py` | `LANG_GUARD_OK ... keys 24 data_cn_zh 496 data_cn_en_known 471 stable_values_ok offline_refs_ok` | 已证实 |
| V13 | `python3 scripts/i18n_guard.py` | `I18N_GUARD_OK ... hits 0 inline_bilingual_cn_lines 122` | 已证实 |
| V14 | `python3 scripts/panic_guard.py` / `semver_guard.py` | 各 `hits 0` | 已证实 |
| V15 | `python3 scripts/p09_scan.py` | `P09_HITS 0` | 已证实 |
| V16 | `python3 scripts/render_ui.py` | shots=51，56 张 PNG，overview 2553183 B | 已证实 |
| V17 | 读 `01-home.png` | 中文完整，数据区全渲染 | 已证实 |
| V18 | 读 `41-i18n-en.png` | 界面框架英文，逻辑条/状态栏仍中文 | 已证实 |
| V19 | `cargo test --offline --lib` | **280 / 0** | 已证实 |
| V20 | `git diff -- src/ Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V21 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan，scan 8 steps | 已证实 |
| V22 | 必读文件循环 | REQUIRED=254 MISSING=0 | 已证实 |
| V23 | 远端 `GET /git/trees/...?recursive=1` 逐项比对 | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 抽离、离线加载、切换重建、状态合并、守卫、重渲 | 已证实 |
| 英文包 471 条中文 / 英文态局部残留 | 已证实（L-049-1，未清零） |
| 英文数据源人工审校、EQ-15 端点配置化 | 未启动 |
| 真实网络 IO / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| 集成测试段（7+6+7+6）本轮未重跑 | 已证实（`src/` 零改动，沿用 048 的 306/0） |

限制：本轮未做 GUI 端到端自动化遍历、未做英文译文审校、未做真实 HTTP 请求；改动作者未代改验证结论，未降低验收项。

## 交付快照

| 项 | 值 |
| --- | --- |
| 本地提交 | `5ae2b1a` |
| 远端主快照 | `fe00c6f`（`round 049 extract demo data into standalone language packs`） |
| 远端 tree | `53c350c` |
| 文件数 | 本地 1008 / 远端 blob 1008 |
| 逐项比对 | `ALL_MATCH True`，DIFF 0，EXTRA 0，tree `truncated=false` |
| 通道 | GitHub Git Data API，8 线程并发、增量树；推送调用两次被网关 502 截断，查远端 ref 确认已落地，未强推、未重写历史 |
| 凭据 | 临时载体在仓库外，核对后删除；全仓 `NO_CREDENTIAL`，`.git/config` 干净 |

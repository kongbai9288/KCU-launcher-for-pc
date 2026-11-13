# 第 022 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 022 |
| 验证对象 | 异步探测、设备连接范围、失败历史分类、37 张产品视图、109 项必读 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 按 021 P01 精简，不生成双哈希；变更以 git 提交号为准，证据为下列可复跑命令 |

## 复跑证据

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `python3 scripts/render_ui.py` | `render_ui OK shots=37`；`demos/preview/*.png` = 42 | 已证实 |
| V2 | `node -e` 遍历 `demos/*.html` | `ALL_JS_OK 18` | 已证实 |
| V3 | `python3 -c compile` ×4 | `PY_OK` | 已证实 |
| V4 | `python3 scripts/p09_scan.py` | `P09_HITS 0 []`，exit 0 | 已证实 |
| V5 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V6 | `! grep -rE '为了\|目的是\|方便用户\|让用户能够\|这样用户\|部分已证实\|为什么' src/ demos/ README.md docs/...` | NO_EXPLANATORY | 已证实 |
| V7 | `! grep -rE 'FCL\|揉纸启动器\|https?://' demos/ui-full-kcu-paper.html` | NO_BRAND_EXT | 已证实 |
| V8 | `! grep -rE '同上' docs/research/` | NO_REPEAT | 已证实 |
| V9 | `grep -c 'srvSync'` / `grep -c 'budget-cell'` / `grep -c 'data-internal="1"'` | 0 / 4 / 4 | 已证实 |
| V10 | `grep -c '<symbol'` / `grep -c 'class="logicbar"'` / `grep -c '<section class="view'` | 88 / 26 / 26 | 已证实 |
| V11 | 必读文件循环 | REQUIRED=109 MISSING=0 | 已证实 |
| V12 | `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| V13 | `git diff 3c87d21..HEAD -- src/ Cargo.lock` | 空 | 已证实 |
| V14 | `git status --porcelain` 提交后 | 空 | 已证实 |
| V15 | 远端 `GET /git/trees/...?recursive=1` 比对 | 见推送段 | 已证实 / 受阻（无认证时） |

## 判定

| 项 | 值 |
| --- | --- |
| 演示层异步、双上限、新服入队、失败分类、锁定不动 | 已证实 |
| 界面证据 37 张产品视图、P09 零命中、零凭据、零禁用词 | 已证实 |
| 真实 TCP 并发、真实超时取消、真实内存剖析 | 受阻 |
| 浏览器内实际点击（截图为静态帧） | 受阻 |
| Q01-Q03 口径确认、用户手感反馈 | 未证实 |
| 真实客户端实现、`src/` 变化 | 未启动 |
| 本地链与远端链提交号不同（内容等价） | 已失败 |

## 未闭环项

| 编号 | 内容 |
| --- | --- |
| U01 | Q01「范围」单位、Q02「按权重中去排序」、Q03 档位数值，均为本轮自主拍板，待用户确认。 |
| U02 | 用户尚未按 37 张图给手感反馈；UI 实现按闸门未进构建。 |
| U03 | 真实网络与真实并发池未实测；演示层是 setTimeout 模拟的异步队列。 |
| U04 | 1.20.5 / 1.21 的 servers.dat 结构变化未取得一手证据。 |

## 限制说明

本轮验证只覆盖可在本环境复跑的静态与脚本检查；浏览器内交互、真实网络、跨平台构建不在本轮能力内，未以推测补全。改动作者未代改验证结论，未降低验收项。

# 全功能使用逻辑补全

| 项 | 值 |
| --- | --- |
| 编号 | F019-01 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 019 |
| 依据 | docs/decisions/019-ux-logic-lucide.md；docs/design/ux-logic-matrix.md |

## 怎么运作

`docs/design/ux-logic-matrix.md` 定义 L01–L12 骨架，U01–U20 共 20 个功能逐项填 12 项；另落缓存分层 4 层、刷新触发 R1–R5、推荐位 6 处、状态徽章 11 类、并发冲突 8 种、许可动态追加结构、三视图空错加载细则。`demos/ui-full-kcu-paper.html` 把骨架落到 22 个视图区块：每个区块顶部 `logicbar` 显示已缓存时间、命中/未命中计数、就绪状态、刷新与强制刷新两个动作；点击后写 `[KCU]` 诊断行并更新时间戳。新增 8 个视图覆盖服务器推荐、第三方许可、数据与缓存、刷新机制、状态与降级、AI 接口、开服器、无头模式。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `#view=`、导航、逻辑条按钮、许可分组 chip、刷新失败模拟、缓存清理、AI 测试、开服启停 |
| 输出 | 28 张 PNG、`[KCU]` 诊断行、时间戳与命中数更新 |
| 错误路径 | 刷新失败回退上次缓存不空白；失败层单独标错；取消 0 副作用 |
| 空值 | 六态独立画面，空态给入口而非空白 |
| 超时 | 连接码 300s、轮询退避、关页即停 |
| 编码 | UTF-8，本地字体栈 |
| 排除项 | 源稿品牌、外部字体 CDN、三栏拖拽、位置照搬 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `#view=<name>` | URL 路由 | 28 个视图名 + 别名 | 对应视图 | 未知名回落 home |
| `.lb-soft` / `.lb-hard` | 按钮 | 无 | 软刷新取增量 / 强制刷新清缓存 | 失败回退快照 |
| `renderLic()` | 函数 | 分组键 | 七列许可表 | 缺失给来源链接 |
| `rfFail` / `rfRetry` | 按钮 | 无 | 刷新失败兜底提示 | 保留 12 秒前快照 |
| `python3 scripts/render_ui.py` | 脚本 | 无 | 29 张 PNG | 非零退出 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo（docs/rules/ui-demo.md G01-G15；019 D01-D12） |
| 模块路径 | docs/design/ux-logic-matrix.md、demos/ui-full-kcu-paper.html、demos/preview/、scripts/render_ui.py |
| 扩展点 | E04 ui 仅服务 normal；lightweight 独立视图；headless 不加载界面 |
| 关键抽象 | K01 Envelope、K03 Diagnostics、K08 UiFrame（仍未进实现） |
| 依赖 | chromium、playwright、PIL；无新增 crate |
| 约束 | 每个功能填满 12 骨架项；每视图有逻辑条；PNG 闸门每轮复跑 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 总览图 | 看 28 个视图 | 判断推荐、缓存、刷新是否都在 |
| 任一视图逻辑条 | 点刷新 / 强制刷新 | 时间戳与命中数更新，写诊断行 |
| 首页推荐服务器卡 | 点全部服务器 | 进推荐位与权重口径 |
| 数据与缓存 | 看四层占用与清理 | 命中率、TTL、失效条件可见 |
| 刷新机制 | 点模拟刷新失败 | 看到回退缓存不空白的提示 |
| 关于 → 第三方许可 | 看七列表与分组 | 许可证、项目、构建状态一目了然 |

## 性能

| 项 | 值 |
| --- | --- |
| 渲染耗时 | 28 张 1440×900 截图一次跑完，每帧等待 300ms |
| 产物体积 | 单张 0.7–1.2M，总览 1408616 字节 |
| 常驻进程 | chromium 无头进程跑完即退出 |
| 网络 | 0 次远端请求，图标内联 sprite |
| 测量命令 | `python3 scripts/render_ui.py` |
| 四值 | 已证实（脚本实跑；用户端交互体验需人工确认） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=28` | 已证实 |
| `ls demos/preview/*.png \| wc -l` | 29 | 已证实 |
| `grep -c '<section class="view'` | 22 | 已证实 |
| `grep -c 'class="logicbar"'` | 22 | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| 用户在手机端查看与手感反馈 | 未发生 | 未证实 |

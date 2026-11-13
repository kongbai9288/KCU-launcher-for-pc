# 界面视觉全集与预览

| 项 | 值 |
| --- | --- |
| 编号 | F017-01 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 017 |
| 依据 | docs/decisions/017-visual-preview.md；docs/spec/17-round-017-instructions.txt |

## 怎么运作

`demos/ui-full-kcu-v2.html` 是单文件整页演示，15 个场景由 `data-scene` 区块与 `#scene=` 路由控制，`show()` 切换可见区块并同步导航高亮、底部状态条与弹窗状态。`scripts/render_ui.py` 用本地 chromium 逐个 `goto` 并截 1440×900 PNG，PIL 把缩略图拼成 `demos/preview/00-overview.png`。公告数据在 `NOTICES` 数组，弹窗目录在 `POPUPS` 数组，实例、服务器、引导步骤、开源致谢各自成表；场景切换调用 `dismissOverlay()` 清弹窗残留。整页离线可点，KCU 标识为内联 SVG。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `#scene=`、导航点击、铃铛、主题按钮、手感调整下拉 |
| 输出 | 15 个场景画面、PNG 预览、总览拼图、`[KCU]` 诊断行 |
| 错误路径 | 弹窗类场景独立渲染；切换场景清残留；关闭路径含按钮 / ESC / 取消 / 确认 / 宿主 |
| 空值 | 空态、加载态、错误态、被锁态、离线态均有独立画面 |
| 超时 | 连接码 300s 在登录场景可见 |
| 编码 | UTF-8，中文字体走本地栈 |
| 排除项 | FCL 品牌、样板代码、外部字体 CDN、三栏拖拽、位置照搬 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `#scene=<name>` | URL 路由 | 15 个场景名 | 对应场景 | 未知名回落 home |
| `show(name)` | 函数 | 场景名 | 可见区块 / 导航 / 状态条 | 无 |
| `dismissOverlay()` | 函数 | 无 | 清弹窗状态 | 无 |
| `openDlg / closeDlg` | 函数 | 标题 / 正文 / id / 关闭动作 | 弹窗画面与诊断行 | 无 |
| `python3 scripts/render_ui.py` | 脚本 | 无 | 16 张 PNG | 非零退出 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo（docs/rules/ui-demo.md G01-G10；docs/decisions/017-visual-preview.md） |
| 模块路径 | demos/ui-full-kcu-v2.html、demos/preview/、scripts/render_ui.py |
| 扩展点 | E04 ui 仅服务 normal；lightweight 独立场景，不共用组件 |
| 关键抽象 | K01 Envelope、K03 Diagnostics、K08 UiFrame（仍未进实现） |
| 依赖 | chromium 系统路径、playwright、PIL；无新增 crate |
| 约束 | 风格取自样板、位置重排；演示与实现分开落盘；PNG 闸门每轮复跑 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 对话里点开总览图 | 看 15 个缩略画面 | 一眼判断布局、配色、公告长相 |
| 点开单张 PNG | 看某个界面全尺寸 | 按手感提意见 |
| 点开整页 HTML | 点导航、铃铛、主题、公告、弹窗 | 可离线交互 |
| 提修改意见 | 改演示与截图 | 确认后才进实现 |
| 轻量模式 | 看独立极简画面 | 不与正常模式共用组件 |

## 性能

| 项 | 值 |
| --- | --- |
| 渲染耗时 | 15 张 1440×900 截图一次跑完，脚本内每帧等待 260ms |
| 产物体积 | 单张 127K–268K，总览 770K，预览打包 3.8M |
| 常驻进程 | chromium 无头进程跑完即退出 |
| 网络 | 0 次远端请求，字体走本地 Noto / WenQuanYi |
| 测量命令 | `python3 scripts/render_ui.py` |
| 四值 | 已证实（脚本实跑；用户端交互体验需人工确认） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=15` | 已证实 |
| `ls demos/preview/*.png \| wc -l` | 16 | 已证实 |
| `test -f demos/preview/00-overview.png` | 1444×1776 | 已证实 |
| `! grep -rE 'https?://\|FCL\|揉纸启动器' demos/ui-full-kcu-v2.html` | exit 0 | 已证实 |
| `git diff 6d09a10..HEAD -- src/` | 空 | 已证实 |
| 用户在手机端查看与手感反馈 | 未发生 | 未证实 |

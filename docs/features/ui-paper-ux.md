# 纸质质感 UX 界面全集

| 项 | 值 |
| --- | --- |
| 编号 | F018-01 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 018 |
| 依据 | docs/decisions/018-paper-ux.md；docs/spec/18-round-018-instructions.txt |

## 怎么运作

`demos/ui-full-kcu-paper.html` 是单文件 UX 演示，1440×900 桌面窗口骨架：40px 标题栏（K 字标 / 名称 / 胶囊搜索 / 日月切换 / 窗控三键）、精简左导航（可折叠为 64px）、56px 工具条（衬线标题 / 面包屑 / 列表-网格分段 / 操作按钮）、卡片流主区、28px 状态栏。20 个视图由 `data-view` 区块与 `#view=` 路由控制，`show()` 切换可见区块、同步导航高亮与工具条文案、清理弹窗与抽屉残留。浅色米纸与深色纸质两套色板定义在 `:root` 与 `.win[data-theme="dark"]`，折痕由三道线性渐变叠加径向高光构成，细噪点由 canvas 固定种子生成 data URI 注入 `--noise` / `--noise-dark`，无远端资源。

`scripts/render_ui.py` 用本地 chromium 逐视图以不同 query 强制重载并截 1440×900 PNG，PIL 拼 4 列 5 行总览 `demos/preview/00-overview.png`。公告数据 `NOTICES` 6 条、弹窗目录 `POPUPS` 11 类、实例 `INS` 7 条、服务器 `SRV` 3 条、引导 `OB` 4 步、致谢 `CREDITS` 9 项；诊断行写入日志页与抽屉两处。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `#view=`、导航点击、主题按钮、侧栏收起、分段切换、公告筛选、弹窗、日志抽屉、右键菜单、手感调整下拉 |
| 输出 | 20 个视图画面、21 张 PNG、`[KCU]` 单行诊断 |
| 错误路径 | 弹窗类视图独立渲染；切换视图清弹窗/抽屉/右键菜单残留；关闭路径含按钮 / ESC / 取消 / 确认 / 宿主 |
| 空值 | 空态、加载态、错误态、被锁态、安全模式、离线态六态独立画面 |
| 超时 | 连接码 300s 在登录视图可见 |
| 编码 | UTF-8；标题走本地衬线，正文走本地无衬线 |
| 排除项 | 源稿代码、标题、favicon、品牌文本、外部字体 CDN、三栏拖拽、右栏公告、位置照搬 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `#view=<name>` | URL 路由 | 20 个视图名 + 5 个别名 | 对应视图 | 未知名回落 home |
| `show(name)`、`setTheme(t)` | 函数 | 视图名 / light-dark | 可见区块、导航、工具条、主题 | 无 |
| `openDlg` / `closeDlg` | 函数 | 标题 / 正文 / id / 关闭动作 | 弹窗画面与诊断行 | 无 |
| `seedNoise(alpha,r,g,b)` | 函数 | 4 个整数 | data URI 背景变量 | 无 |
| `python3 scripts/render_ui.py` | 脚本 | 无 | 21 张 PNG | 非零退出 |

别名：`home-dark`、`home-light`、`narrow`、`context`、`logs-drawer`、`notice-detail`、`update`。

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo（docs/rules/ui-demo.md G01-G12；018 D01-D10） |
| 模块路径 | demos/ui-full-kcu-paper.html、demos/preview/、scripts/render_ui.py |
| 扩展点 | E04 ui 仅服务 normal；lightweight 独立视图，不共用组件 |
| 关键抽象 | K01 Envelope、K03 Diagnostics、K08 UiFrame（仍未进实现） |
| 依赖 | chromium 系统路径、playwright、PIL；无新增 crate |
| 约束 | 纸质色板同源、位置重排、演示与实现分开落盘、PNG 闸门每轮复跑 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 对话里点开总览图 | 看 20 个缩略画面 | 一眼判断纸质风格、布局、公告长相 |
| 点开单张 PNG | 看某个视图全尺寸 | 按手感提意见 |
| 点开 UX HTML | 点导航、主题、收起、公告、弹窗、抽屉、右键 | 可离线交互 |
| 提修改意见 | 改演示与截图 | 确认后才进实现 |
| 轻量模式 | 看独立极简画面 | 不与正常模式共用组件 |

## 性能

| 项 | 值 |
| --- | --- |
| 渲染耗时 | 20 张 1440×900 截图一次跑完，脚本内每帧等待 300ms |
| 产物体积 | 单张 0.9–1.1M，总览 983491 字节，预览打包约 24M |
| 常驻进程 | chromium 无头进程跑完即退出 |
| 网络 | 0 次远端请求，字体走本地 Noto / WenQuanYi |
| 测量命令 | `python3 scripts/render_ui.py` |
| 四值 | 已证实（脚本实跑；用户端交互体验需人工确认） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=20` | 已证实 |
| `ls demos/preview/*.png \| wc -l` | 21 | 已证实 |
| `test -f demos/preview/00-overview.png` | 1462×1392 | 已证实 |
| `cmp 源稿 assets/ui/normal-mode-v3.html` | exit 0 | 已证实 |
| `! grep -rE 'FCL\|揉纸启动器\|https?://' demos/ui-full-kcu-paper.html` | exit 0 | 已证实 |
| `git diff 52e02c1..HEAD -- src/` | 空 | 已证实 |
| 用户在手机端查看与手感反馈 | 未发生 | 未证实 |

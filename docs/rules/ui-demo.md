# 用户界面整页演示规则

| 项 | 值 |
| --- | --- |
| 编号 | R-UI-01 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 015 建立；016 首次触发；017 增 PNG 闸门；018 纸质质感与 UX 形态纠正；019 使用逻辑补全与 lucide；020 导航锁定与设置归拢 |
| 依据 | docs/spec/15-round-015-instructions.txt F02/F03；docs/decisions/015-build-continue.md D02-D04 |

## 触发

| 条件 | 是否触发 |
| --- | --- |
| 新增、修改、删除用户可见界面元素 | 触发 |
| 改动调度、下载、数据结构、文档、测试、CI | 不触发 |
| 仅调整运行逻辑演示 HTML | 不触发 |
| 轻量模式极简视图改动 | 触发，单独交付，不复用 normal.ui 资产 |

## 交付物

| 编号 | 项 | 值 |
| --- | --- | --- |
| G01 | 命名 | `demos/ui-full-<主题>.html` |
| G02 | 形态 | 整页 HTML，覆盖该界面全部可见区域与交互状态 |
| G03 | 禁止形态 | 运行逻辑状态机、局部截图、文字描述、仅一张静态图 |
| G04 | 离线 | 可离线打开，不依赖外部字体 CDN 与远端脚本 |
| G05 | 字体 | 失败走本地字体栈 |
| G06 | 品牌 | KCU 标识；不直接复用 assets/ui/normal-mode-v3.html 的 FCL 品牌 |

## 覆盖范围

| 编号 | 项 |
| --- | --- |
| C01 | 导航、侧栏、主内容、状态栏 |
| C02 | 弹窗全类型，每个有关闭路径 |
| C03 | 深浅主题切换 |
| C04 | 空态、加载态、错误态、被锁态 |
| C05 | 每个可点击控件有响应 |
| C06 | 流程结束 0 个未关弹窗 |
| C07 | 低配轻量视图单独演示，不加载 normal.ui 资产 |
| C08 | 双击服务器按权重选实例、用户指定排第一、单参数进服的界面入口 |

## 用户回路

| 步 | 动作 |
| --- | --- |
| 1 | 交付整页演示 |
| 2 | 用户按手感提出调整 |
| 3 | 先改演示，再交付确认 |
| 4 | 确认后才改实现 |
| 5 | 实现与演示分开落盘，演示不进 `src/` |

用户调整意见优先于当前实现，见 docs/decisions/015-build-continue.md D04。

## 每轮检查

| 检查 | 命令 |
| --- | --- |
| 触发判定 | 对照本文件「触发」表 |
| 演示存在 | `test -f demos/ui-full-*.html`（触发轮次） |
| 离线依赖 | `! grep -rE '<script[^>]+src=|<link[^>]+href=\"https?:' demos/ui-full-*.html` |
| 关闭路径 | `grep -c 'close' demos/ui-full-*.html` > 0 |
| 主题 | `grep -c 'data-theme\|theme-toggle' demos/ui-full-*.html` > 0 |
| 品牌隔离 | `! grep -rE 'FCL|揉纸启动器' demos/ui-full-*.html` |

## 轮次状态

| 轮次 | 判定 | 交付物 |
| --- | --- | --- |
| 015 | 不触发（仅调度逻辑） | 无 ui-full 文件；`demos/round-015-dispatcher.html` 是运行逻辑演示，不计入 G01 |
| 016 | **已触发**（L3 lightweight 极简视图） | `demos/ui-full-lightweight.html` |
| 017 | **已触发**（正常模式界面重排 + 公告族补齐） | `demos/ui-full-kcu-v2.html`、`demos/preview/00-overview.png` + 15 张场景 PNG；**风格取错，已作废** |
| 018 | **已触发**（纸质质感重做 + UX 形态纠正） | `demos/ui-full-kcu-paper.html`、`demos/preview/00-overview.png` + 20 张视图 PNG |
| 019 | **已触发**（28 视图、逻辑条、lucide、第三方许可页） | `demos/ui-full-kcu-paper.html` 更新、`demos/preview/00-overview.png` + 28 张视图 PNG、THIRD-PARTY-NOTICES.md |
| 020 | **已触发**（26 区块 / 37 截图视图、锁定槽位、设置九分组、推荐位总览、上层候选、交接基线） | `demos/ui-full-kcu-paper.html` 更新、`demos/preview/00-overview.png` + 37 张视图 PNG、THIRD-PARTY-NOTICES.md 第五节 |

016 触发记录：

| 编号 | 项 | 值 |
| --- | --- | --- |
| T01 | 依据 | docs/decisions/016-build-continue.md D02-D05 |
| T02 | 交付物 | `demos/ui-full-lightweight.html`，整页、6 分区、5 状态、11 弹窗、离线可点、KCU 标识 |
| T03 | 主题口径 | 演示层深浅预览供手感调整；实现层默认单主题（007 D04）。用户对演示的调整优先于实现 |
| T04 | 手感回路 | 交付演示 → 用户按手感调整 → 先改演示 → 确认后改实现；本轮实现未进入构建 |
| T05 | 运行逻辑演示 | `demos/round-016-lightweight.html` 不计入 G01 |
| T06 | 轻量独立性 | 不复用 normal.ui、设计稿、揉纸纹理、双主题实现、三栏拖拽、日志抽屉 |

016 轮检查命令：

```
test -f demos/ui-full-lightweight.html
! grep -rE '<script[^>]+src=|<link[^>]+href="https?:' demos/ui-full-lightweight.html
! grep -rE 'FCL|揉纸启动器' demos/ui-full-lightweight.html
grep -c 'data-theme' demos/ui-full-lightweight.html
grep -c 'close' demos/ui-full-lightweight.html
node -e "const fs=require('fs');const m=fs.readFileSync('demos/ui-full-lightweight.html','utf8').match(/<script>([\s\S]*?)<\/script>/);new Function(m[1]);"
```

## 017 增补

| 编号 | 项 | 值 |
| --- | --- | --- |
| G07 | 提交形态 | 动 UI 的轮次须交 PNG 预览与 `00-overview.png` 总览；HTML 单文件仍按 G01-G06 交付 |
| G08 | 渲染 | `python3 scripts/render_ui.py`，本地 chromium 按 `#scene=` 截图，全程离线 |
| G09 | 风格与位置 | 样板只取配色、圆角、描边、卡片层次、轻噪点；位置重新组织，不采用三栏拖拽与组件照搬 |
| G10 | 主动补齐 | 公告中心、公告详情、更新提示、首次启动引导、维护/活动公告等界面一并出图，不待用户逐项点名 |

017 场景清单 S01-S15 见 docs/decisions/017-visual-preview.md；每张图的说明见 demos/preview/index.md。

017 轮检查命令：

```
test -f demos/ui-full-kcu-v2.html
test -f demos/preview/00-overview.png
ls demos/preview/*.png | wc -l
! grep -rE 'https?://|FCL|揉纸启动器' demos/ui-full-kcu-v2.html
node -e "const fs=require('fs');const m=fs.readFileSync('demos/ui-full-kcu-v2.html','utf8').match(/<script>([\s\S]*?)<\/script>/);new Function(m[1]);"
grep -c '<section class="scene' demos/ui-full-kcu-v2.html
```

017 手感回路：PNG 总览 → 用户按图提意见 → 先改演示与截图 → 确认后才改实现。本轮 `src/` 无变化。

## 018 增补

| 编号 | 项 | 值 |
| --- | --- | --- |
| G11 | 风格源 | 样板纸质色板、折痕纹理、衬线标题、小圆角、细描边、半透明卡片、窗口 chrome；浅色米纸 + 深色纸质两套。不得另定一套配色冒充「风格取自样板」 |
| G12 | 交付形态 | **UX HTML** ＝ 桌面窗口、导航、工具条、卡片、表格、弹窗、抽屉、状态栏，命名 `demos/ui-full-*.html`；**流程 HTML** ＝ 步骤节点、状态机、诊断行、信封、阶段判定，命名 `demos/round-0XX-*.html`。动 UI 的轮次主交付只能是 UX HTML + PNG，流程 HTML 不得替代 |

018 视觉 token 对照表与 S01-S20 清单见 docs/decisions/018-paper-ux.md；逐图说明见 demos/preview/index.md。

018 轮检查命令：

```
test -f demos/ui-full-kcu-paper.html
test -f demos/preview/00-overview.png
ls demos/preview/*.png | wc -l
! grep -rE 'FCL|揉纸启动器|https?://' demos/ui-full-kcu-paper.html
node -e "const fs=require('fs');const m=fs.readFileSync('demos/ui-full-kcu-paper.html','utf8').match(/<script>([\s\S]*?)<\/script>/);new Function(m[1]);"
grep -c '<section class="view' demos/ui-full-kcu-paper.html
```

018 手感回路：PNG 总览 → 用户按图提意见 → 先改演示与截图 → 确认后才改实现。本轮 `src/` 无变化；017 的 `ui-full-kcu-v2.html` 保留文件但标记作废。

## 019 增补

| 编号 | 项 | 值 |
| --- | --- | --- |
| G13 | 图标 | 全站 lucide，内联 sprite，无 CDN / 图标字体 / 全量 sprite；逐枚来源与 SHA 记 manifest；ISC + Feather MIT 登记进关于页 |
| G14 | 使用逻辑 | 每个功能填满 L01–L12；每个视图区块顶部逻辑条显示已缓存时间、命中/未命中、刷新、强制刷新、状态 |
| G15 | 第三方许可 | 关于页一级入口 + 七列表 + 分组筛选 + 插件动态追加；发行物随附 THIRD-PARTY-NOTICES.md；构建状态如实标注 |

019 检查命令：

```
test -f THIRD-PARTY-NOTICES.md
test -f assets/icons/lucide-subset.svg
grep -c '<symbol' demos/ui-full-kcu-paper.html
grep -c 'class="logicbar"' demos/ui-full-kcu-paper.html
grep -c '<section class="view' demos/ui-full-kcu-paper.html
ls demos/preview/*.png | wc -l
! grep -rE 'FCL|揉纸启动器|https?://' demos/ui-full-kcu-paper.html
! grep -rqE 'gh[p]_' .
```

019 手感回路：PNG 总览 → 用户按图提意见 → 先改演示与截图 → 确认后才改实现。本轮 `src/` 无变化。

## 020 增补

| 编号 | 项 | 值 |
| --- | --- | --- |
| G16 | 导航 | 一级导航收敛为 9 项日常操作；设置与关于固定在 `slot-core` 锁定容器；插件区 `slot-plugin` 只能追加 |
| G17 | 设置归拢 | 9 个分组 chip，每视图区块保留逻辑条；AI 接口 / 缓存 / 刷新 / 状态 / 无头 / 许可不再占一级入口 |
| G18 | 工具条收敛 | 设置、关于、许可、槽位、总览、交接、候选等页面隐藏列表网格 / 刷新 / 新建实例按钮 |

020 检查命令：

```
test -f docs/design/handoff.md
test -f docs/design/nav-slot-contract.md
grep -c '<section class="view' demos/ui-full-kcu-paper.html
grep -c 'class="logicbar"' demos/ui-full-kcu-paper.html
ls demos/preview/*.png | wc -l
! grep -rE 'FCL|揉纸启动器|https?://' demos/ui-full-kcu-paper.html
! grep -rqE 'gh[p]_' .
```

020 手感回路：PNG 总览 → 用户按图提意见 → 先改演示与截图 → 确认后才改实现。本轮 `src/` 与 Cargo.lock 无变化。

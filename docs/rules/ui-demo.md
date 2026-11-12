# 用户界面整页演示规则

| 项 | 值 |
| --- | --- |
| 编号 | R-UI-01 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 015 建立；016 首次触发 |
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

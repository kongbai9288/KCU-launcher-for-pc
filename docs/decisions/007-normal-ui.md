# 正常模式 UI 与轻量模式分流

| 项 | 值 |
| --- | --- |
| 编号 | 007 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 007 |
| 依据 | docs/spec/07-round-007-instructions.txt |

## 决定了什么

| 编号 | 项 | 值 |
| --- | --- | --- |
| D01 | 正常模式 UI | 采用用户 007 轮提供的 v3 设计稿，逐字副本 assets/ui/normal-mode-v3.html |
| D02 | 资产状态 | 已落盘、已登记；未实现、未进入构建 |
| D03 | 轻量模式 UI | 独立视图，与正常模式 UI 无共用组件、无共用资产 |
| D04 | 轻量模式排除项 | normal.ui 框架、设计稿、揉纸纹理、浅色/深色双主题、三栏拖拽、table.grid、衣柜、工具箱、设备桥接面板、分步向导、右键菜单、日志抽屉 |
| D05 | 轻量模式视图范围 | 三种登录入口、外置浏览器 → 内置浏览器 → 连接码三级回退、基础日志 |
| D06 | 轻量模式进程 | 游戏运行期无常驻后台进程，见 docs/spec/00-requirements.txt:16 |
| D07 | UI 框架归属 | K08 UiFrame 与 E04 ui 扩展点仅服务 normal 模式，见 docs/decisions/005-blueprint.md:38,49 |
| D08 | 品牌与授权 | 设计稿内 FCL、揉纸启动器、favicon 文本 F、状态栏版本号、外部字体 CDN 均登记为非 KCU 资产，授权未取得前不进构建 |
| D09 | 搭建阶段 | 仍为 003-remote.md D05 功能输入阶段；D06 触发信号未提供，未启动 D07 逐层搭建 |
| D10 | 无头模式 | 不加载任何 UI，见 docs/spec/00-requirements.txt:17 |

## 约束

| 编号 | 约束 |
| --- | --- |
| C01 | src/ 保持空目录；本轮不写实现代码。 |
| C02 | 设计稿原始字节不改动；派生文件另存并单独登记。 |
| C03 | lightweight 构建不引用 assets/ui/ 下任何文件。 |
| C04 | lightweight 构建不引入 normal.ui 的 crate 与字体资源。 |
| C05 | 外部字体 CSS 失败时走本地字体栈，按二级降级写诊断行。 |
| C06 | 品牌标记不替换 KCU 标识、不进入安装包、不进入窗口标题。 |
| C07 | 未取得授权前不复制设计稿代码进 src/。 |
| C08 | 模式判定入口单一，位于 dispatcher；UI 层不自行切换模式。 |
| C09 | 本决策不修改 005-blueprint.md 的未批准状态。 |

## 验证条件

| 编号 | 命令 | 期望 |
| --- | --- | --- |
| V01 | `sha1sum assets/ui/normal-mode-v3.html` | 235943d217560d89f8e0598c7f78b902d993e99d |
| V02 | `cmp /data/inputs/FCL揉纸启动器-桌面端-v3(1).txt assets/ui/normal-mode-v3.html` | exit 0 |
| V03 | `git ls-files src/` | 输出为空 |
| V04 | `! grep -rE 'FCL|揉纸启动器' src/` | exit 0 |
| V05 | `! grep -rqE 'gh[p]_' .` | exit 0 |
| V06 | `grep -c 'nav-item' assets/ui/normal-mode-v3.html` | 10 个导航标签 |
| V07 | `按 docs/checklists/ai-errors.md A23 执行` | exit 0 |
| V08 | `node -e "new Function(script)"` demos/round-007-normal-ui.html | exit 0 |

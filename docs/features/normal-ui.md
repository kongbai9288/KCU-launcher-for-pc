# 正常模式 UI

| 项 | 值 |
| --- | --- |
| 编号 | F001 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 007 |
| 资产 | assets/ui/normal-mode-v3.html |

## 怎么运作

| 项 | 值 |
| --- | --- |
| 输入 | 用户 007 轮提供的 HTML 设计稿，172759 字节，2729 行 |
| 处理 | 逐字落盘 assets/ui/；登记结构事实、品牌标记、外部资源、许可证边界；写决策 007-normal-ui.md |
| 输出 | 资产文件 1 份、资产登记 1 份、功能登记 1 份、决策 1 份、HTML 演示 1 份 |
| 错误路径 | 来源字节不一致时停止落盘并保留 cmp 输出；品牌标记命中构建闸门时零级报错 |
| 空值 | 外部字体 CSS 返回空或失败时走本地字体栈，不阻塞窗口渲染 |
| 超时 | 外部资源请求超时归二级降级，写入诊断行 |
| 编码 | UTF-8 逐字副本，字节未改动 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| assets/ui/normal-mode-v3.html | 文件 | 无 | HTML 文档 | 文件缺失返回统一错误 |
| assets/ui/index.md | 文件 | 无 | 结构事实与约束 | 文件缺失返回统一错误 |
| docs/decisions/007-normal-ui.md | 文件 | 无 | 模式分流与边界 | 文件缺失返回统一错误 |
| demos/round-007-normal-ui.html | 文件 | 模式选择 | 状态机输出 | 无效模式返回统一错误 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | normal.ui |
| 模块路径 | src/ui/（未实现，src/ 为空） |
| 扩展点 | E04 ui，见 docs/decisions/005-blueprint.md:49 |
| 关键抽象 | K08 UiFrame，见 docs/decisions/005-blueprint.md:38 |
| 依赖 | 未引入任何 crate |
| 排除 | lightweight 不加载本框架、本资产、本分类下的揉纸纹理与双主题资源，见 docs/decisions/007-normal-ui.md |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 正常模式启动 | 内存 > 2GB，或 config/launch.json 指定 normal | 加载 normal.ui 框架 | 显示 10 项导航的桌面窗口 |
| 轻量模式启动 | 内存 ≤ 2GB 且首次，或配置指定 lightweight | 跳过 normal.ui 加载 | 进入极简登录视图 |
| 无头模式 | .kcul 或 cmd 入口 | 跳过全部 UI | 直接启动游戏 |
| 主题切换 | 正常模式窗口 | 点击标题栏按钮 | 浅色 / 深色切换 |
| 侧栏收起 | 正常模式窗口 | 点击收起侧栏 | .win.narrow，64px |
| 三栏拖拽 | 正常模式窗口 | 拖动 grip | 导航宽度变化 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 未实测 |
| 启动耗时 | 未实测 |
| 常驻进程 | normal 模式有；lightweight 模式 MC 运行期无，见 docs/spec/00-requirements.txt:16 |
| 退出条件 | 窗口关闭；游戏进程回收 |
| 测量命令 | 无 |
| 四值 | 受阻，无浏览器与 rustc/cargo 环境，无法执行渲染与构建测量 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `sha1sum /data/inputs/FCL揉纸启动器-桌面端-v3(1).txt assets/ui/normal-mode-v3.html` | 两行同为 235943d217560d89f8e0598c7f78b902d993e99d | 已证实 |
| `cmp` 来源与落盘 | exit 0 | 已证实 |
| `git ls-files src/` | 输出为空 | 已证实 |
| `node -e "new Function(script)"` demos/round-007-normal-ui.html | JS_SYNTAX_OK | 已证实 |
| 浏览器内渲染实测 | 未执行 | 受阻 |
| 品牌标记授权 | 未取得 | 未证实 |

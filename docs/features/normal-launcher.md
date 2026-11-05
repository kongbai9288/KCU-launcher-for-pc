# 正常启动器

| 项 | 值 |
| --- | --- |
| 编号 | F005 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 009 |
| 依据 | docs/spec/00-requirements.txt:18-21 |

## 怎么运作

| 项 | 值 |
| --- | --- |
| 实现状态 | 未实现，src/ 为空 |
| 输入 | LaunchTask、账号凭据、版本清单、Java 路径、实例配置 |
| 处理 | 任务解析 → 依赖下载 → 版本 json 生成启动参数 → 进程启动 → 日志回收 |
| 输出 | 游戏进程、日志文件、诊断行 |
| UI | 加载 normal.ui，见 docs/features/ui-framework.md |
| EULA | 正常启动流程显示 EULA 同意说明 |
| 错误路径 | 缺依赖、Java 不可用、版本 json 解析失败、进程退出非零 → 零级或一级失败可见 |
| 空值 | 空账号、空版本、空列表按内置默认处理 |
| 超时 | 下载、进程启动、IPC 均设超时 |
| 编码 | json 按 UTF-8；路径按 OsStr；命令行参数走 args_os |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| 启动任务 | 函数 | LaunchTask | 进程句柄 | 统一错误 |
| 版本清单 | 函数 | 版本标识 | 文件集合 | 统一错误 |
| 实例配置 | 文件 | 实例 json | 实例对象 | 统一错误 |
| EULA 状态 | 函数 | eula.txt | 同意 / 未同意 | 统一错误 |
| 日志 | 函数 | 日志行 | 日志文件 | 统一错误 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | normal |
| 模块路径 | src/normal/（未实现） |
| 扩展点 | E01 auth、E02 download、E03 loader、E04 ui，见 docs/decisions/005-blueprint.md |
| 关键抽象 | K05 LaunchTask、K01 Envelope、K02 PathResolver、K03 Diagnostics、K04 FallbackLevel、K07 Provider、K08 UiFrame |
| 依赖 | 未引入任何 crate |
| 约束 | 不合并 KCU-Launcher 原仓库；HMCL 代码复用范围未证实，见 docs/research/01-hmcl.md |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 正常模式启动 | 内存 > 2GB 或 config/launch.json 指定 | 加载窗口 | 显示 10 项导航 |
| 首次正常启动 | eula.txt 未同意 | 显示 EULA 说明 | 同意后写入 eula=true |
| 版本切换 | 实例已存在 | 选择版本 | 启动对应版本 |
| 游戏运行 | 进程已启动 | 日志回收 | 日志窗口可见 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 未实测 |
| 启动耗时 | 未实测 |
| 常驻进程 | 有，正常模式窗口进程 |
| 退出条件 | 窗口关闭且游戏进程回收 |
| 测量命令 | 无 |
| 四值 | 受阻，无 rustc/cargo 与 Windows 运行环境 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `git ls-files src/` | 输出为空 | 已证实 |
| `grep -n '正常启动器' docs/spec/00-requirements.txt` | 行 18 | 已证实 |
| 运行时行为实测 | 未执行 | 受阻 |

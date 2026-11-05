# 无头模式启动器

| 项 | 值 |
| --- | --- |
| 编号 | F004 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 008 |
| 依据 | docs/spec/00-requirements.txt:17、docs/decisions/007-normal-ui.md D10 |

## 怎么运作

| 项 | 值 |
| --- | --- |
| 实现状态 | 未实现，src/ 为空 |
| 输入 | .kcul 文件中的 json；cmd 参数；c/kcu/kculauncher/ 下的任务 json |
| 处理 | 解析任务 → 组装 LaunchTask → 直接启动游戏进程 |
| 输出 | 游戏进程、日志、诊断行 |
| UI | 不加载任何 UI，包含 normal.ui 与 lightweight.view |
| 正版限制 | 仅当用户此前通过其他模式留存正版凭据时可用；否则禁用正版登录 |
| 凭据保护 | 方案未定，未证实，见 docs/research/02-auth.md:57 |
| 错误路径 | json 解析失败、缺字段、无 Java、凭据不可用 → 零级报错或安全模式；连续失败导出诊断包 |
| 空值 | 缺字段、空集合按内置默认处理 |
| 超时 | 任务读取、进程启动、IPC 均设超时 |
| 编码 | json 与日志按 UTF-8；命令行参数按 args_os / OsString |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| .kcul 文件 | 文件 | 桌面双击 | 游戏进程 | 统一错误 |
| cmd 入口 | CLI | args_os 参数 | 游戏进程 | 统一错误 |
| 任务 json | 文件 | 字段集合 | LaunchTask | 统一错误 |
| LaunchTask | 函数 | 任务对象 | 启动参数 | 统一错误 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | headless |
| 模块路径 | src/headless/（未实现） |
| 扩展点 | E01 auth（受凭据保护约束）、E02 download、E03 loader |
| 关键抽象 | K05 LaunchTask、K01 Envelope、K02 PathResolver、K03 Diagnostics、K04 FallbackLevel |
| 依赖 | 未引入任何 crate |
| 约束 | 不加载 UI；路径集中单一模块；无效 UTF-8 参数不触发 panic，见 docs/checklists/windows-errors.md W02-W03 |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 桌面双击 .kcul | 文件含 json | 直接启动 | 无界面，进入游戏 |
| cmd | 传入参数 | 直接启动 | 无界面，进入游戏 |
| 正版登录 | 此前无正版凭据 | 禁用并提示 | 零级或一级失败可见 |
| 任务文件 | c/kcu/kculauncher/ 下存在 json | 按 json 执行 | 对应启动任务 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 未实测 |
| 启动耗时 | 未实测 |
| 常驻进程 | 无 UI 进程；游戏进程由任务拉起 |
| 退出条件 | 游戏进程退出 |
| 测量命令 | 无 |
| 四值 | 受阻，无 rustc/cargo 与 Windows 运行环境 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `git ls-files src/` | 输出为空 | 已证实 |
| `grep -n '无头模式' docs/spec/00-requirements.txt` | 行 17 | 已证实 |
| 凭据保护机制 | 未取得 | 未证实 |
| 运行时行为实测 | 未执行 | 受阻 |

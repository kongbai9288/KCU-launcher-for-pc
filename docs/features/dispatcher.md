# 统一调度器

| 项 | 值 |
| --- | --- |
| 编号 | F002 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 008 |
| 依据 | docs/spec/00-requirements.txt:6-8、:17 |

## 怎么运作

| 项 | 值 |
| --- | --- |
| 实现状态 | 未实现，src/ 为空 |
| 输入 | c/kcu/kculauncher/ 下的 json 任务文件；config/launch.json；.kcul 文件；cmd 参数；系统内存；首次启动标记 |
| 处理 | 读取任务 → 组装 LaunchTask → ModeSelector 判定 → 启动对应 launcher 入口 |
| 输出 | 启动任务与模式选择结果；诊断行 |
| 模式规则 | 内存 ≤ 2GB 且首次启动 → lightweight；否则 normal；config/launch.json 显式指定时覆盖判定；.kcul 或 cmd 无头入口 → headless |
| 错误路径 | json 解析失败、缺字段、内存检测失败、模式值非法 → 零级报错或安全模式；连续多次失败导出诊断包 |
| 空值 | 任务文件缺失、空集合、空字段按内置默认处理，不返回空值 |
| 超时 | 任务读取、子进程启动、IPC 均设超时 |
| 编码 | json 按 UTF-8 显式声明；路径按 OsStr 处理 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| 任务文件 | 文件 | c/kcu/kculauncher/*.json | LaunchTask | 统一错误，含 request_id |
| 模式覆盖 | 文件 | config/launch.json 的 mode 字段 | 模式值 | 非法值返回统一错误 |
| .kcul 入口 | 文件 | 桌面双击或 cmd | headless 任务 | 统一错误 |
| ModeSelector | 函数 | 内存、首次标记、覆盖值 | dispatcher/normal/lightweight/headless | 统一错误 |
| LaunchTask | 函数 | 任务 json | 统一任务对象 | 统一错误 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | dispatcher |
| 模块路径 | src/dispatcher/（未实现） |
| 扩展点 | 无；模式分支固定为 4 类 |
| 关键抽象 | K05 LaunchTask、K06 ModeSelector、K01 Envelope、K02 PathResolver、K03 Diagnostics、K04 FallbackLevel，见 docs/decisions/005-blueprint.md |
| 依赖 | 未引入任何 crate |
| 约束 | 模式判定入口单一；UI 层不自行切换模式，见 docs/decisions/007-normal-ui.md C08 |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 首次启动 | 内存 ≤ 2GB，无覆盖配置 | 自动进入 lightweight | 极简登录视图 |
| 首次启动 | 内存 > 2GB，无覆盖配置 | 自动进入 normal | 正常模式窗口 |
| 手动控制 | 编辑 config/launch.json | 指定模式 | 覆盖自动判定 |
| 任务文件 | c/kcu/kculauncher/ 下存在 json | 按 json 执行启动任务 | 对应启动器启动 |
| .kcul / cmd | 桌面双击或命令行 | 无头执行 | 不显示界面，直接启动游戏 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 未实测 |
| 启动耗时 | 未实测 |
| 常驻进程 | 调度器在任务分发后退出；lightweight 模式游戏运行期无常驻后台进程 |
| 退出条件 | 任务分发完成或超时 |
| 测量命令 | 无 |
| 四值 | 受阻，无 rustc/cargo 与 Windows 运行环境 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `git ls-files src/` | 输出为空 | 已证实 |
| `grep -n '统一调度器' docs/spec/00-requirements.txt` | 行 6 | 已证实 |
| 浏览器 / 运行时行为实测 | 未执行 | 受阻 |

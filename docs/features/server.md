# 一键开服

| 项 | 值 |
| --- | --- |
| 编号 | F007 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 009 |
| 依据 | docs/spec/00-requirements.txt:21 |

## 怎么运作

| 项 | 值 |
| --- | --- |
| 实现状态 | 未实现，src/ 为空 |
| 输入 | 服务端 jar 选择；插件 / 模组集合；自动化配置；玩家管理动作；本地 AI 工具调用 |
| 处理 | jar 启动 → server.properties / 配置文件读写 → RCON 连接 → 自动化调度 → 玩家管理 → 配置汉化 |
| 输出 | 服务端进程、控制台日志、RCON 响应、诊断行 |
| 自动化类型 | 定期 / 持续 / 单次 |
| 动作 | 定时自动开关机、自动保存、自动发言、自动执行命令、玩家自动 ban / 恢复 |
| 本地 AI 工具 API | 本地 HTTP 接口，端点未定 |
| 配置汉化 | server.properties、bukkit.yml、spigot.yml、paper-global.yml 键名映射 |
| 错误路径 | jar 缺失、EULA 未同意、RCON 认证失败、端口占用、配置文件写入失败 → 零级或一级失败可见 |
| 空值 | 空插件集合、空玩家列表、空配置项按内置默认处理 |
| 超时 | 进程启动、RCON、IPC、自动化调度均设超时 |
| 编码 | server.properties 按 UTF-8，保留 # 注释，Windows 行尾 CRLF，启动时重新生成 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| 开服 / 关服 | 函数 | jar 路径、参数 | 进程句柄 | 统一错误 |
| RCON 命令 | 函数 | 类型 2 包、命令文本 | 响应包 | 统一错误 |
| 自动化 | 函数 | 类型、周期、动作 | 任务句柄 | 统一错误 |
| 玩家管理 | 函数 | ban / pardon 动作 | 执行结果 | 统一错误 |
| 本地 AI 工具 API | HTTP | 端点未定 | 端点未定 | 统一错误 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | normal.server |
| 模块路径 | src/server/（未实现） |
| 扩展点 | E05 automation、E07 server_jar，见 docs/decisions/005-blueprint.md |
| 关键抽象 | K09 Automation、K10 ServerToolApi、K01 Envelope、K02 PathResolver、K03 Diagnostics、K04 FallbackLevel |
| 依赖 | 未引入任何 crate |
| 一手锚点 | https://minecraft.wiki/w/RCON、https://minecraft.wiki/w/Server.properties、https://docs.papermc.io/paper/configuration/ |
| 未证实项 | Mojang 官方 RCON 文档 |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 控制导航项 | 正常模式窗口 | 打开面板 | 显示服务端状态 |
| 一键开服 | jar 与 EULA 就绪 | 点击启动 | 服务端进程启动 |
| 自动化 | 服务端运行 | 配置定期 / 持续 / 单次任务 | 按周期执行 |
| 玩家管理 | RCON 已连接 | 选择动作 | ban / 恢复 |
| 配置汉化 | 配置文件存在 | 打开映射视图 | 键名显示中文 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 未实测 |
| 启动耗时 | 未实测 |
| 常驻进程 | 服务端进程；正常模式窗口进程 |
| 退出条件 | 关服动作或窗口关闭 |
| 测量命令 | 无 |
| 四值 | 受阻，无 rustc/cargo、服务端 jar 与 Windows 运行环境 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `git ls-files src/` | 输出为空 | 已证实 |
| `grep -n '服务器启动' docs/spec/00-requirements.txt` | 行 21 | 已证实 |
| `grep -n 'little-endian' docs/research/06-server.md` | 行 62 | 已证实 |
| 服务端与 RCON 运行时实测 | 未执行 | 受阻 |

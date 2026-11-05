# 跨进程统一信封

| 项 | 值 |
| --- | --- |
| 编号 | F010 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 009 |
| 依据 | docs/spec/00-requirements.txt:114 |

## 怎么运作

| 项 | 值 |
| --- | --- |
| 实现状态 | 未实现，src/ 为空 |
| 输入 | 请求、响应、事件；request_id；payload；统一 error |
| 处理 | 序列化 → 传输 → 反序列化 → 按 type 分派 |
| 输出 | 请求响应对、事件流、统一错误 |
| 消息类型 | request / response / event |
| 错误路径 | 字段缺失、request_id 重复、序列化失败、超时 → 统一 error，禁止空捕获 |
| 空值 | 空 payload、空 error 字段按结构默认值处理 |
| 超时 | 每个请求设超时，响应超时返回统一错误 |
| 编码 | UTF-8；二进制数据显式编码声明 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| 请求 | IPC | request_id、type、target、payload | response | 统一错误 |
| 响应 | IPC | request_id、payload、error | 无 | 统一错误 |
| 事件 | IPC | type、target、payload | 无 | 统一错误 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.ipc |
| 模块路径 | src/core/（未实现） |
| 扩展点 | 无 |
| 关键抽象 | K01 Envelope、K03 Diagnostics、K04 FallbackLevel |
| 依赖 | 未引入任何 crate |
| 约束 | 所有跨进程消息走统一信封；有请求标识；有统一错误 |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 启动任务 | 调度器发起 | 发送 request | 收到 response |
| 状态变更 | 子进程或模块 | 发送 event | 视图更新 |
| 错误返回 | 任一侧失败 | 填充 error | 上层按级别处理 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 未实测 |
| 启动耗时 | 未实测 |
| 常驻进程 | 随宿主模式 |
| 退出条件 | 宿主退出 |
| 测量命令 | 无 |
| 四值 | 受阻，无 rustc/cargo 与 Windows 运行环境 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `git ls-files src/` | 输出为空 | 已证实 |
| `grep -n '统一信封' docs/spec/00-requirements.txt` | 行 114 | 已证实 |
| `grep -n 'K01' docs/decisions/005-blueprint.md` | 行 31 | 已证实 |
| 跨进程消息实测 | 未执行 | 受阻 |

# 启动参数 LaunchArgs

| 项 | 值 |
| --- | --- |
| 编号 | F013-06 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 013 |

## 怎么运作

`parse` 逐 token 读 `--server` / `--join-server` / `--instance` / `--mode` / `--kculf` / `--kculh` / `--lang`；缺值返回 Err，未知 flag 返回 Err，非 flag token 进 extras。`joins_server()` 为真即单参数直达服务器；`headless()` 由 `kculh` 或 `mode=headless` 触发。`kculf` 与 `kculh` 分离，对应 011 D20。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `LaunchArgs::parse` | 函数 | IntoIterator<Item=Into<String>> | Result<Self,String> | 缺值 / 未知 flag |
| `joins_server` / `headless` | 函数 | 无 | bool | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.args（B03、K05、013 U01） |
| 模块路径 | src/core/args.rs |
| 扩展点 | 无 |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 命令行给一个参数 | 无 | `--server mc.example.net:25565` | 跳过 GUI 直接进服 |
| 双击 `.kculf` | 文件已关联 | 走 kculf 分支 | 进 MC，跳过 GUI |
| `kculh` | 无头任务 | 走 headless 分支 | 无 UI |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 与 token 数线性，未实测进程级数值 |
| 启动耗时 | 无 |
| 常驻进程 | 无 |
| 退出条件 | 返回即结束 |
| 测量命令 | `cargo test --offline core::args`（5 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline core::args` | 5 passed | 已证实 |

## 边界

013 U01 用户指出文档缺「指定一个参数就可以加入服务器」，本层补齐；参数与服务器列表双击共用同一进服动作，具体协议对接未实现，标未证实。

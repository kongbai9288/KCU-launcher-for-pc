# LaunchTask 与任务集合

| 项 | 值 |
| --- | --- |
| 编号 | F015-02 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 015 |

## 怎么运作

`LaunchTask::from_json` 只接受顶层 object，读取 id / kind / server / instance / mode / kculf / kculh / version / lang / headless / extras；空字符串字段跳过，缺字段保留内置默认（id=`default`、kind=`launch`）。`headless=true` 且无 kculh 时补一个 kculh 值。`from_args` 把命令行转成任务：单参数 `--server` 生成 `join` 任务，`--mode`、`--instance`、`.kculf`、`.kculh` 原样带入。`TaskSet::from_values` 按 id 排序并去重；`pick` 优先命令行进服任务，其次取 headless 任务，再取首个任务，空集合返回默认任务。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `LaunchTask::{from_json,from_str,from_args,headless,joins_server}` | 函数 | Json / &str / &LaunchArgs | LaunchTask / bool | String |
| `TaskSet::{from_values,from_texts,pick,len,is_empty}` | 函数 | Json 集合 / 文本集合 / &LaunchArgs | TaskSet / LaunchTask / usize / bool | String |
| `TaskKind::{parse,code}` | 函数 | &str | TaskKind / &str | 未知值落 Unknown |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | dispatcher.task（K05 LaunchTask，005-blueprint.md B04） |
| 模块路径 | src/dispatcher/task.rs |
| 扩展点 | 无；任务字段由核心解析，不由扩展点注册 |
| 依赖 | std only，复用 core.args 与 dispatcher.json |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| c/kcu/kculauncher 下多个 json | 用户放置任务 | 按 id 排序去重 | 执行顺序稳定，同 id 不重复 |
| 命令行单参数进服 | `--server <地址>` | 生成 cmd 任务 | 覆盖任务文件 |
| .kcul / `--kculh` | 双击或命令行 | headless 任务优先 | 不加载界面 |
| 坏任务文件 | json 非法 | 报错并禁用该条 | 其余任务继续 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 任务数与输入文件数同阶；id 排序用稳定排序，无额外索引 |
| 启动耗时 | 8 项测试含在全量 0.11s 内 |
| 常驻进程 | 无 |
| 退出条件 | 返回任务集合或错误 |
| 测量命令 | `cargo test --offline dispatcher::task`（8 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `empty_fields_fall_back_to_defaults`、`empty_task_set_yields_default_task` | 默认任务 | 已证实 |
| `task_set_is_sorted_deduped_and_picks_headless_first` | 3 条、取 h | 已证实 |
| `cmd_arg_overrides_task_files`、`single_arg_generates_join_task` | cmd 任务 | 已证实 |
| `root_must_be_object` | 非 object 报错 | 已证实 |

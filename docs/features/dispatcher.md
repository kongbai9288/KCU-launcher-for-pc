# 统一调度器

| 项 | 值 |
| --- | --- |
| 编号 | F002 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 008 登记；015 实现 |
| 依据 | docs/spec/00-requirements.txt:6-8、:17、:179-182；docs/decisions/015-build-continue.md |

## 怎么运作

| 项 | 值 |
| --- | --- |
| 实现状态 | src/dispatcher/ 5 文件，103 项全量测试中 dispatcher 占 47 项 |
| 输入 | DispatchInput：任务 json 文本集合、config/launch.json 文本、LaunchArgs、内存字节数、首次启动标记、.kcul 标记、既有正版凭据标记、服务器条目、实例列表、版本权重、用户指定版本、CancelToken |
| 处理 | JSON 解析 → LaunchTask / TaskSet → 命令行合并 → 双击服务器按权重选实例 → ModeSelector 判定 → 弹窗注册与关闭 → 失败计数 → 安全模式 → 诊断包 → 统一信封 |
| 输出 | LaunchOutcome：mode、task、instance、diagnostics、premium_allowed、ui_loaded、popups_open、safe_mode、diagnostic_bundle、cancelled、Envelope |
| 模式规则 | 强制无头 > args.mode > config/launch.json > task.mode > 自动判定；`≤ 2147483648 字节 && 首次` → lightweight；否则 normal |
| 错误路径 | json 解析失败 → 0 级报错不崩；非法模式 → 0 级报错并用内置默认继续；内存检测失败 → 2 级降级 normal；headless 无凭据 → 1 级禁用正版；连续 3 次失败 → 安全模式，仍失败导出诊断包 |
| 空值 | 空任务集合、空 json 对象、空字段 → 内置默认 LaunchTask，不返回空值 |
| 超时 | 缓存加载 2 秒；CancelToken 在入口与中途检查 |
| 编码 | json 按 UTF-8 解析，`\uXXXX` 与中文 UTF-8 均覆盖；路径仍由 core.paths 按 OsStr 处理 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `json::parse` | 函数 | &str | Json | String，含字节位置 |
| `LaunchTask::{from_json,from_str,from_args}` | 函数 | Json / &str / &LaunchArgs | LaunchTask | String |
| `TaskSet::{from_values,from_texts,pick}` | 函数 | Json 集合 / 文本集合 / &LaunchArgs | TaskSet / LaunchTask | String |
| `ModeSelector::{select,safe}` | 函数 | &ModeInput | Result<ModeSelection,String> / ModeSelection | 非法模式含来源 |
| `Dispatcher::{new,dispatch,reset,flush_diagnostics}` | 函数 | capacity / &DispatchInput / &CancelToken | LaunchOutcome / () | 不 panic，错误进信封与诊断 |
| `Dispatcher.cache` | 字段 | Arc<Cache<String,String>> | 有界缓存 | `CacheError` |
| `Dispatcher.parse_calls` | 字段 | Arc<AtomicUsize> | 解析次数 | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | dispatcher（005-blueprint.md B04；003-remote.md D07 第 2 层） |
| 模块路径 | src/dispatcher/{json,task,mode,launcher,mod}.rs |
| 扩展点 | 无；模式分支固定 4 类；E04 ui 仅 normal 模式加载 |
| 关键抽象 | K05 LaunchTask、K06 ModeSelector、K01 Envelope、K03 Diagnostics、K04 FallbackLevel |
| 依赖 | std only；复用 core.cache / core.asynk / core.leak / core.popup / core.instance / core.log |
| 约束 | 模式判定入口单一；UI 层不自行切换模式（007-normal-ui.md C08）；Cargo.toml / Cargo.lock 未变 |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 首次启动 | 内存 ≤ 2 GiB，无覆盖配置 | 自动 lightweight | 极简视图，不加载 UI 框架 |
| 首次启动 | 内存 > 2 GiB，无覆盖配置 | 自动 normal | 正常模式，弹窗全注册全关闭 |
| 手动控制 | 编辑 config/launch.json | 指定模式 | 覆盖自动判定 |
| 命令行 | `--mode` | 指定模式 | 优先于配置文件 |
| 任务文件 | c/kcu/kculauncher/ 下 json | 按 id 排序去重后执行 | 对应启动任务 |
| .kcul / cmd | 双击或 `--kculh` | 强制 headless | 不显示界面；无既有正版凭据时禁用正版 |
| 双击服务器 | 服务器条目 + 实例列表 | 按版本权重选实例 | 用户指定版本排第一 |
| 单参数进服 | `--server <地址>` | 直接进服 | 跳过实例选择页 |
| 反复启动失败 | 3 次连续失败 | 安全模式 + 内置默认 | 仍失败导出诊断包 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 任务缓存容量默认 16，可注入；40 个不同任务以 capacity=4 实测 len/order ≤ 4，inflight=0 |
| 启动耗时 | 全量 103 项测试 0.11s；单轮 dispatch 为同步内存操作，无 I/O |
| 常驻进程 | 无；dispatch 返回即结束；CancelToken 取消时 0 解析、0 副作用 |
| 退出条件 | dispatch 返回；reset 清缓存、日志、失败计数与安全态 |
| 测量命令 | `cargo test --offline dispatcher::launcher::tests::repeated_task_text_is_parsed_once`、`cache_stays_bounded_over_many_tasks`、`cancelled_token_stops_before_any_work` |
| 泄漏 | outcome 经 core.leak Tracker 跟踪，drop 后 live=0；LogBuffer 每 100 行分片 |
| 四值 | 已证实（cargo test 实跑；进程级内存剖析未实测） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline dispatcher::` | 47 passed / 0 failed | 已证实 |
| `cargo test --offline` | 103 passed / 0 failed / 0 ignored / 0 measured | 已证实 |
| `cargo build --release --offline` | 通过 | 已证实 |
| `git ls-files src/dispatcher/ \| wc -l` | 5 | 已证实 |
| 浏览器 / GUI 点击端到端、Windows 运行时实测 | 未执行 | 受阻 |

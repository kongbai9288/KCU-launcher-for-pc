# ModeSelector 与兜底分级

| 项 | 值 |
| --- | --- |
| 编号 | F015-03 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 015 |

## 怎么运作

`LOW_MEMORY_BYTES = 2147483648`。`select(&ModeInput)` 按固定优先级判定：force_headless → args_mode → config_mode → task_mode → 自动判定。显式值经 `Mode::parse` 校验，非法值返回含来源的零级错误；空字符串跳过。`memory_unknown` 时直接 normal 并置 2 级降级；`mem_bytes ≤ 2147483648 && first_run` → lightweight；否则 normal。`safe(&ModeInput)` 返回 safe。`ModeSelection` 同时给出 reason、fallback、premium_allowed、ui_loaded、memory_degraded：headless 无既有凭据 → 1 级且禁用正版；safe → 2 级、忽略自定义配置、禁用正版与 UI；仅 normal 的 `ui_loaded=true`。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `ModeSelector::{select,safe}` | 函数 | &ModeInput | Result<ModeSelection,String> / ModeSelection | 非法模式含来源 |
| `Mode::{code,parse,loads_ui}` | 函数 | &str / 无 | &str / Option<Mode> / bool | 无 |
| `Fallback::code` | 函数 | 无 | "0"/"1"/"2"/"3" | 无 |
| `ModeInput`、`ModeSelection` | 结构 | 内存、首次、覆盖值、凭据 | 模式与分级 | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | dispatcher.mode（K06 ModeSelector、K04 FallbackLevel） |
| 模块路径 | src/dispatcher/mode.rs |
| 扩展点 | 无；模式分支固定 4 类（007-normal-ui.md C08） |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 低配首次开机 | ≤ 2 GiB 且首次 | 自动 lightweight | 极简视图 |
| 常规开机 | > 2 GiB | 自动 normal | 正常窗口 |
| 编辑 config/launch.json | 显式 mode | 覆盖自动判定 | 用户指定生效 |
| 命令行 `--mode` | 显式 mode | 优先于配置文件 | 用户指定生效 |
| .kcul / cmd 无头 | 强制无头 | headless | 不显示界面；无凭据时禁用正版 |
| 内存读数拿不到 | memory_unknown | 2 级降级 normal | 提示已切换 |
| 连续失败 | 安全模式 | safe | 忽略自定义配置 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 固定大小结构，无堆分配增长 |
| 启动耗时 | 12 项测试含在全量 0.11s 内 |
| 常驻进程 | 无 |
| 退出条件 | 返回 ModeSelection 或错误 |
| 测量命令 | `cargo test --offline dispatcher::mode`（12 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `threshold_is_two_gib`、`low_memory_first_run_selects_lightweight` | 2147483648 / lightweight | 已证实 |
| `args_override_beats_config`、`config_override_beats_automatic_mode` | 覆盖生效 | 已证实 |
| `invalid_mode_is_zero_level_error` | 含来源报错 | 已证实 |
| `headless_without_credential_disables_premium` | 1 级、禁正版 | 已证实 |
| `only_normal_loads_ui`、`unknown_memory_degrades_to_normal_with_level_two` | UI 分流、2 级 | 已证实 |

# 路径解析 PathResolver

| 项 | 值 |
| --- | --- |
| 编号 | F013-03 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 013 |

## 怎么运作

逻辑名 → 相对段映射表（config / logs / icons / lang / instances / backups / dialogs_state / diag），`resolve` 用注入的 root 拼接 PathBuf；未知逻辑名返回 Err。`from_env(key)` 从环境变量取 root，未设置返回 Err。root 由调用方注入，模块内不含盘符、不含绝对路径字面量。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `PathResolver::new` / `from_env` | 函数 | root / env key | Self | Err(String) |
| `resolve` | 函数 | &str 逻辑名 | PathBuf | `unknown logical name` |
| `logical_names` / `root` | 函数 | 无 | Vec<&str> / &Path | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.paths（B03、K02） |
| 模块路径 | src/core/paths.rs |
| 扩展点 | 无；新增逻辑名改本表，不改 core 外部 |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 自选保存路径 | 用户在设置里给根目录 | 注入 root | 全部分区落在同一根下 |
| 图标集中 | 用户换图标 | 改 assets/icons 单文件 | 其余代码不动 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 8 条静态映射，未实测进程级数值 |
| 启动耗时 | 无 |
| 常驻进程 | 无 |
| 退出条件 | 值析构 |
| 测量命令 | `cargo test --offline core::paths`（4 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline core::paths` | 4 passed | 已证实 |
| `grep -rn 'C:\\\\' src/` | 无命中 | 已证实 |

## 边界

用户 F36 / F49 指定「C 盘 KCU 文件夹」为默认位置；本层只暴露注入点，不写死盘符，遵守 005-blueprint.md C03。具体默认值由 config 层下发，未在本层实现，标未证实。

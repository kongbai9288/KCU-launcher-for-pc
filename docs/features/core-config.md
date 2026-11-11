# 配置 Config

| 项 | 值 |
| --- | --- |
| 编号 | F013-04 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 013 |

## 怎么运作

`Config::empty(os_class)` 建空配置；端点与端口按 key 注入 BTreeMap，模块内无 URL、无端口字面量。`language` 默认 `zh-CN`，可改；`mirror_speedtest` 默认 true。`set_download_region` 只写 `region_override`，`download_region()` 是唯一读取口，`has_policy_endpoint()` 用于确认没有把该值接进地区禁用策略。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `set_endpoint` / `endpoint` | 函数 | key, url | Option<&str> | 无 |
| `set_port` / `port` | 函数 | key, u16 | Option<u16> | 无 |
| `set_download_region` / `download_region` | 函数 | &str | Option<&str> | 无 |
| `has_policy_endpoint` | 函数 | 无 | bool | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.config（B03、K07、011 D14、D11） |
| 模块路径 | src/core/config.rs |
| 扩展点 | E02 download / E01 auth 的端点由本层注入 |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 换语言包 | 调度器下发 | 改 `language` | 全 UI 文案源切换 |
| 换镜像 / 端口 | 用户或更新包 | 改端点与端口 | 不重新编译 |
| 强制境外 | 用户手动 | `set_download_region` | 只影响下载源选择 |
| 地区禁用下载 | 未来功能 | 不读 `download_region()` | 与软策略隔离，F53 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 两张 BTreeMap，未实测进程级数值 |
| 启动耗时 | 无 |
| 常驻进程 | 无 |
| 退出条件 | 值析构 |
| 测量命令 | `cargo test --offline core::config`（4 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline core::config` | 4 passed | 已证实 |
| `grep -rnE 'https?://|:[0-9]{4,5}' src/core/config.rs` | 无字面量 | 已证实 |

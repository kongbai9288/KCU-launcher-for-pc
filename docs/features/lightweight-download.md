# Provider 与批量下载

| 项 | 值 |
| --- | --- |
| 编号 | F016-02 |
| 状态 | 已实现、已验证 |
| 轮次 | 016 |
| 框架 | lightweight.download / E02 / K07 |

## 怎么运作

`ProviderConfig` 提供 Mojang / BMCLAPI 两源、注入式 base、可选 API Key、`region_override` 与镜像测速开关；`pick_source` 在强制境外时选 Mojang，否则保持配置源，`has_policy_endpoint` 恒 false（地域软策略只用于下载选择，不与地区禁用复用）。`Downloader::batch` 把 id 列表按每页 20 切块，每块用 `source:page:joined_ids` 作缓存键走 core.cache 单飞，一次请求带多个 id；返回 items / pages / request_count / 统一信封 / 单行诊断。空集合不发请求；CancelToken 在入口与分页间检查；CF 下载源本层不暴露，密钥不落源码。

## 开放了什么

| 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- |
| `ProviderConfig::{mojang,bmclapi,with_api_key,with_region,pick_source,has_policy_endpoint}` | &str | Self / DownloadSource / bool | 无 |
| `Downloader::{new,batch,reset,cf_source_exposed}` | ProviderConfig / &[String] / CancelToken | BatchReply / () / bool | String |
| `BatchReply` | 无 | items / pages / request_count / envelope / diagnostics | 无 |
| 常量 `PAGE_SIZE=20`、`DEFAULT_CACHE_CAPACITY=32` | 无 | usize | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | lightweight.download（B05；E02 download；K07 Provider） |
| 模块路径 | src/lightweight/download.rs |
| 依赖 | core.cache / asynk / diagnostics / envelope |
| 约束 | 011 D12 批量化：逐条目单发列为禁止项；CF F17 未提供前不暴露 CF；X01-X04 未拍板 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 搜模组列表 | 一次请求带多个 id | 每页 20 条，不逐条目单发 |
| 反复拉同一批 | 走单飞缓存 | 10 次只发 1 次 |
| 强制境外 | 选地域软策略 | 只改下载源，不影响地区禁用策略 |
| 填 API Key | 可选注入 | 源码零凭据 |
| 网络断开 / 取消 | CancelToken 或空集合 | 0 请求，不崩 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 缓存容量 32、TTL 30s；60 次不同批次后 len/order ≤ 32；inflight=0 |
| 请求数 | 10 id → 1 次；45 id → 3 页 3 次；空集合 → 0 次 |
| 常驻进程 | 无 |
| 退出条件 | batch 返回 / reset 清态 |
| 测量命令 | `cargo test --offline lightweight::download`（12 passed） |
| 真实网络、CF 端点、镜像测速实测 | 受阻 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `one_request_for_ten_ids_not_ten` | 10 items / 1 request | 已证实 |
| `forty_five_ids_use_three_pages_and_three_requests` | 3 / 3 | 已证实 |
| `repeated_batch_is_single_flight`、`cache_stays_bounded_and_order_does_not_grow` | 1 次 / ≤32 | 已证实 |
| `region_override_only_affects_download_selection`、`api_key_is_injected_not_hardcoded` | 软策略 / 注入 | 已证实 |
| `curseforge_source_is_not_exposed`、`cancel_stops_before_any_network_call` | false / 0 请求 | 已证实 |

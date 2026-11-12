# 有界缓存 Cache

| 项 | 值 |
| --- | --- |
| 编号 | F014-01 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 014 |

## 怎么运作

`Cache::new(capacity, ttl)` 拒绝 0 容量。`get_or_load(key, timeout, loader)` 先清过期项并查表；命中直接返回。未命中且已有 in-flight 时，等待 `Condvar` 直到完成或超时；否则当前调用方成为 leader，在 `inflight` 登记 `Weak<Flight<V>>` 后释放锁再执行 loader，结果写回条目并 `notify_all`。`Err` 走 `CacheError::Load`，等待超时走 `TimedOut`，leader 未写值走 `Cancelled`。插入时按容量从 `order` 头部淘汰；`purge_locked` 每次清过期项、过滤无效 order 条目并按 key 去重。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `Cache::new` / `get_or_load` | 函数 | usize, Duration / K, Duration, FnOnce | Self / Result<V,CacheError<E>> | `Load` / `TimedOut` / `Cancelled` |
| `len` / `capacity` / `evicted` / `inflight_count` / `order_len` / `clear` | 函数 | 无 | usize / u64 / () | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.cache（B03、014 D04、D06） |
| 模块路径 | src/core/cache.rs |
| 扩展点 | E02 download 的聚合请求与多源去重由本层提供底座 |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 模组聚合搜索 | 一次请求带多个 json | 同 key 并发只加载一次 | 不重复发请求 |
| 模组图标浏览 | 条目滚出视野 | 条目按容量淘汰 | 内存有界 |
| 镜像地址变更 | 用户改 vars | 过期后重取 | 新端点生效 |
| 导出诊断包 | 用户点导出 | `clear` | 缓存态归零 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 条目数 ≤ capacity；order 长度 ≤ capacity；8 并发等同一 key 实测 loader 调用 1 次 |
| 启动耗时 | 无独立启动；全量测试 0.10s |
| 常驻进程 | 无 |
| 退出条件 | 值析构；inflight 用 Weak，加载结束 `remove` |
| 测量命令 | `cargo test --offline core::cache`（8 passed）；`cargo build --release --offline` rlib 610080 字节 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline core::cache` | 8 passed | 已证实 |
| `capacity_bounds_entry_count` | len ≤ 2，evicted ≥ 4 | 已证实 |
| `single_flight_loads_once_for_concurrent_waiters` | 8 线程、calls=1 | 已证实 |
| `order_stays_bounded_after_many_inserts` | 500 次插入后 order ≤ 3 | 已证实 |
| `inflight_is_weak_and_never_dangles` | inflight_count=0 | 已证实 |

## 边界

CF03 禁止缓存的合规冲突仍登记在 12-compliance.md；本层是通用底座，不绑定任何上游端点，是否用于 CF 数据由上层按 X 拍板决定。

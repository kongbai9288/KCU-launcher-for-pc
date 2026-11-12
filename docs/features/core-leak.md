# 泄漏探测与弱引用注册表 leak

| 项 | 值 |
| --- | --- |
| 编号 | F014-03 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 014 |

## 怎么运作

`Tracker::track(value)` 把值装进 `Arc<T>` 并活跃计数 +1；`Tracked<T>` 的 `Clone` 计数 +1，`Drop` 计数 -1，`downgrade()` 产出 `Weak<T>`。`WeakRegistry<K,V>` 只存 `Weak<V>`，`get` 用 `upgrade()`，`purge()` 清理已释放条目并返回清除数。双向链表场景用 `Mutex<Option<Weak<Node>>>`，避免 `Arc` 环。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `Tracker::{new,track,live}` | 函数 | T / 无 | Tracked<T> / usize | 无 |
| `Tracked::{get,downgrade,strong_count}` | 函数 | 无 | &T / Weak<T> / usize | 无 |
| `WeakRegistry::{new,insert,get,purge,len}` | 函数 | K, &Arc<V> / &K / 无 | Option<Arc<V>> / usize | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.leak（B03、014 D06） |
| 模块路径 | src/core/leak.rs |
| 扩展点 | 全层通用；cache.inflight、asynk.LiveGuard 复用同一计数字段口径 |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 打开再关闭一个页面 | 组件被 track | 页面关闭 | `live()` 归零 |
| 模组图标缓存 | 条目被弱引用登记 | 原对象释放 | `get` 返回 None、`purge` 清理 |
| 导出诊断包 | 用户点导出 | 读 `live()` | 非零即列出残留 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 一个 `Arc<AtomicUsize>` + 一个 `Mutex<HashMap<K,Weak<V>>>`；5 个用例全部断言归零 |
| 启动耗时 | 无独立启动 |
| 常驻进程 | 无 |
| 退出条件 | `Tracked` 全部 drop |
| 测量命令 | `cargo test --offline core::leak`（5 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline core::leak` | 5 passed | 已证实 |
| `tracked_releases_on_drop` | live 1 → 0 | 已证实 |
| `weak_link_breaks_cycle_and_reaches_zero` | strong_count=1、live 2 → 0 | 已证实 |
| `weak_registry_does_not_keep_value_alive` | purge=1、len=0 | 已证实 |
| `clone_increments_and_all_drops_return_to_zero` | 2 → 1 → 0 | 已证实 |

## 边界

本层是进程内计数与弱引用语义，不是 OS 级内存剖析；WebView2 / GUI 侧的真实内存占用需在浏览器渲染实测环境里另行测，标受阻。

# F043-01 统一信封 request_id 契约

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `Envelope::new` 把 `pid / 启动纳秒 / 进程内序号 / kind / target` 组成一个 name，`derive_id` 交给 `Uuid::new_v5(&Uuid::NAMESPACE_OID, …)` 生成 RFC 9562 版本 5 UUID；SHA-1 摘要、128 位截断、version 与 variant 位设置全由库完成。`to_json_string` 原样带上这个 ID。 |
| 开放了什么 | `src/core/envelope.rs` 的 `derive_id` / `Envelope::new` / `to_json_string`；`with` / `with_error` / `ok` / `field` / `from_json_str` 一行没动。 |
| 登记框架 | `uuid 1.18.1`（Apache-2.0 OR MIT / MSRV 1.63）+ `sha1_smol 1.0.1`（BSD-3-Clause）；只开 `std` + `v5`，无 rng、无平台分支、无 C 构建链。与 031 的 serde_json 载荷、032 的 log 门面、040 的 http 类型层串联。 |
| 用户使用逻辑 | 诊断包、审计日志、插件请求、跨进程统一信封都能用同一个 ID 串起来；重启启动器、同时开多个实例、pid 被系统复用，都不会把两次会话的请求混成一条；ID 不含随机数，低配机器与 Win7 上生成行为一致。 |
| 性能 | 每个信封一次 SHA-1（20 字节命名空间 + 短 name）+ 一次格式化；无分配大头、无 IO、无锁竞争（序号用 Relaxed 原子加）。 |

状态：已实现已验证；真实网络 IO 未启动。

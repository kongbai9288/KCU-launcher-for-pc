# F042-01 批量请求 query 编码契约

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `build_request` 把每个模组 id 单独交给 `utf8_percent_encode(id, ID_ENCODE_SET)`，编码结果用字面 `,` 连接成一个 `ids` 参数；`ID_ENCODE_SET` 由 `CONTROLS` 加 query 里会破坏语义的字符构成，保留 unreserved；非 ASCII 字节由库按 UTF-8 转义；最终 `Uri` 仍由 `http` crate 解析。 |
| 开放了什么 | `src/core/http.rs` 的 `build_request` / `plan` / `validate_authority`；`plan` 的分页与「10 个 id 一次请求、45 个三次请求」语义一行没动。 |
| 登记框架 | `percent-encoding 2.3.1`（MIT OR Apache-2.0 / edition 2018 / MSRV 1.51 / 零依赖）；与 040 的 `http 1.3.1` 类型层、029 的 `lru` 单飞缓存、027 的 crossbeam 并发层串联。 |
| 用户使用逻辑 | 搜一批模组时还是一次请求，不会因为某个模组名带空格、`&`、中文就悄悄丢几个；镜像看到的 id 与用户选的一一对应；编码前的常见 id 请求串不变，不会让已有缓存 key 或服务端规则突然失效。 |
| 性能 | 每页最多 20 个 id，逐 id 编码是线性小操作；无额外网络请求、无分配大头、无异步任务。 |

状态：请求构造层已实现已验证；真实网络 IO 未启动。

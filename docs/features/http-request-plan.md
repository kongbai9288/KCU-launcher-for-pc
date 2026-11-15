# F040-01 批量请求构造标准化

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `RequestSpec` 由调用方给 scheme / authority / path / headers；`build_request` 用 `http::Uri::from_str` 解析完整串、`Method::GET`、`Version::HTTP_11`、`HeaderName::parse` + `HeaderValue::from_str` 构造 `Request<()>`；`plan` 按 `page_size` 切片，每页一个标准请求。`Downloader::plan()` / `validate_base()` 接到现有配置上，`batch()` 行为不变。 |
| 开放了什么 | `src/core/http.rs`：`RequestSpec` / `PAGE_SIZE` / `validate_authority` / `build_request` / `plan`；`src/lightweight/download.rs` 新增 `plan()` / `validate_base()`。 |
| 登记框架 | 依赖 `http 1.3.1` + `bytes 1.11.1` + `fnv 1.0.7`，`itoa 1.0.15` 复用 025 的既有 vendor；不动 `libloading`（038）/ `crossbeam`（027）/ `lru`（029）任何一层。 |
| 用户使用逻辑 | 一次批量查询只按页发请求，10 个模组一次、45 个模组三次，不会每个模组各发一次；镜像地址填错了当场给可见错误，不静默拼出坏 URL；批量结果仍走原来的单飞缓存，重复查不重复占连接。 |
| 性能 | 每页一次 `Uri` 解析 + 一次 HeaderMap 构造，O(页内 id 数)；无网络、无分配大头、无后台线程。`http` 是纯类型 crate，不做 IO。 |

状态：请求构造层已实现；真实网络 IO 未启动。

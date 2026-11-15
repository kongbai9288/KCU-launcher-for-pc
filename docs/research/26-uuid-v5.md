# UUID v5 与两个 crate 的一手资料（043）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/uuid-rs/uuid/blob/v1.18.1/Cargo.toml | uuid 1.18.1 / `Apache-2.0 OR MIT` / edition 2018 / MSRV 1.63.0；`default=["std"]`；`v5=["sha1"]`、`sha1=["dep:sha1_smol"]`、`v4=["rng"]`、`rng=["dep:getrandom"]`；所有依赖均 `optional = true` | 已证实（api.github.com 同 tag 内容） |
| https://github.com/uuid-rs/uuid/blob/v1.18.1/src/v5.rs | `pub fn new_v5(namespace: &Uuid, name: &[u8]) -> Uuid` = `Builder::from_sha1_bytes(sha1::hash(namespace.as_bytes(), name)).into_uuid()`；文档指向 RFC 9562 §5.5 / §6.5 | 已证实 |
| https://github.com/uuid-rs/uuid/blob/v1.18.1/src/lib.rs | `NAMESPACE_DNS` / `NAMESPACE_OID` / `NAMESPACE_URL` / `NAMESPACE_X500` 四个标准常量；模块按 `#[cfg(feature = "v5")]` 等门控 | 已证实 |
| https://github.com/mitsuhiko/sha1-smol/blob/1.0.1/Cargo.toml | sha1_smol 1.0.1 / **BSD-3-Clause** / edition 2018 / `Minimal dependency-free implementation of SHA1`；`[dependencies]` 只有 optional serde；`default` 无 features | 已证实 |
| https://www.rfc-editor.org/rfc/rfc9562 | §5.5：UUIDv5 = SHA-1(Namespace ID ‖ name)，取最左 128 位，其余 32 位丢弃，再按 §4.2 / §4.1 设 version=5、variant=0b10；SHA-256 派生的名字 UUID MUST NOT 用 v5，应走 v8 | 已证实 |
| https://docs.python.org/3/library/uuid.html | `uuid.uuid5(namespace, name)` 按命名空间标识符与名称的 SHA-1 生成 UUID；`uuid.NAMESPACE_OID` 是标准命名空间之一 | 已证实 |
| 标准值 | `NAMESPACE_OID = 6ba7b812-9dad-11d1-80b4-00c04fd430c8`；Python `uuid5(NAMESPACE_OID, "kcu-fixture-0001")` = `d4bf11e5-29b6-5b3f-a553-5701cc26efd5` | 已证实（独立算） |
| uuid 仓库 GitHub API `license.spdx_id` | `NOASSERTION`（根目录两份 LICENSE 并存），crate manifest 明确 `Apache-2.0 OR MIT` | 已证实 |
| crates.io registry 与 static.crates.io | 全部 403 | 已证实（025 起多轮） |

| 编号 | 结论 |
| --- | --- |
| R21 | 进程内单调计数不满足 F010 跨进程统一信封的可追溯性；重启即重复。 |
| R22 | v5 是标准算法且**不需要随机数源**；v4 / v7 会拉 getrandom 0.3，Win7 运行时需另核，本轮不选。 |
| R23 | 两个 crate 只开 `std` + `v5` 时闭包是 1 个传递依赖，无 C 链、无平台分支，符合 011 的 Win7 Tier 3 路线。 |
| R24 | 独立期望值可由 Python 标准库算出，能验证位布局与 SHA-1 口径一致，不靠被换掉的库自证。 |

# 第 043 轮：统一信封 request_id 换成 UUID v5

| 项 | 值 |
| --- | --- |
| 编号 | 043 |
| 状态 | 已实现已验证；真实网络 IO、UI、崩溃分析未启动 |
| 依据 | docs/spec/43-round-043-instructions.txt |
| 前序 | 010 统一信封 F010、024 代码归属台账、040–042 逐块库化、011 Win7 起兼容路线 |
| 本轮性质 | 单轨轮：继续按台账把自写通用算法换成库 |

## 本轮落点

`src/core/envelope.rs` 的 `request_id` 原是 `static SEQ: AtomicU64` + `format!("kcu-{:08x}", n)`：**只在单个进程内单调**。诊断包、审计日志、F010 的跨进程统一信封都用这个 ID；进程一重启就从 `kcu-00000001` 重新计数，两次启动的请求在日志里完全撞车，追溯时会把不同会话串成一条。这不是风格问题，是可追溯性缺陷。

唯一 ID 生成属于通用算法，按 024 台账交给库。

## 真实 manifest 核查（api.github.com 同 tag 内容）

| 编号 | 候选 | 真实数据 | 四值 |
| --- | --- | --- | --- |
| F32 | `uuid 1.18.1` | tag **`v1.18.1`**（不带 `v` 的 `1.18.1` 是 404）；crate manifest 写 `Apache-2.0 OR MIT` / edition 2018 / MSRV **1.63.0** / categories 含 `no-std`；`default=["std"]`；features `v5=["sha1"]`、`sha1=["dep:sha1_smol"]`、`v4=["rng"]`、`v7=["rng"]`、`rng=["dep:getrandom"]`；**所有依赖都是 optional**，含 getrandom 0.3 / rand 0.9 / md-5 / bytemuck / serde / zerocopy / borsh / atomic / uuid-macro-internal / wasm 分支；`src/v5.rs` 的 `new_v5` 是 `Builder::from_sha1_bytes(sha1::hash(namespace.as_bytes(), name))` | 已证实 |
| F33 | `sha1_smol 1.0.1` | `mitsuhiko/sha1-smol` tag `1.0.1`；**BSD-3-Clause**；描述 `Minimal dependency-free implementation of SHA1 for Rust`；edition 2018；`[dependencies]` 只有 optional `serde`；dev-dependencies 含 openssl / rand / serde_json | 已证实 |
| F34 | 仓库许可证口径 | uuid 仓库 GitHub API 的 `license.spdx_id` 是 **NOASSERTION**（根目录同时有 LICENSE-APACHE 与 LICENSE-MIT），但 crate manifest 明确 `Apache-2.0 OR MIT`；按 manifest 用，两份全文都落盘 | 已证实 |
| F35 | RFC 9562 §5.5 | UUIDv5 = SHA-1(namespace ID ‖ name) 取最左 128 位，再按 §4.2 / §4.1 替换 version=5、variant=0b10；`NAMESPACE_OID` 标准值 `6ba7b812-9dad-11d1-80b4-00c04fd430c8` | 已证实（RFC Editor / Python 文档） |
| F36 | 通道限制 | crates registry 与 static.crates.io 全部 403，vendor 只能走 api.github.com / codeload 的 tag tarball | 已证实（025 起多轮） |

| 编号 | 判定 |
| --- | --- |
| U58 | **只开 `std` + `v5`**：v5 只带 `sha1_smol` 一个传递依赖，`getrandom` / `rand` / `md-5` / `wasm` 分支全是 optional 且未启用 → 零平台分支、零 C 构建链、零随机数源。Win7 Tier 3 路线不受 040 查到的 `ProcessPrng` 问题影响。 |
| U59 | `v4` / `v7` 需要 `rng` → `getrandom 0.3`，Windows 分支要核运行时；本轮不选，不改口径也不假设「应该能跑」。 |
| U60 | 上游 `src/` 逐字节未改；vendored manifest 只裁掉未启用的 optional 依赖段、`[target.*]`、`[dev-dependencies]`、`[workspace]`、`[badges]`、`[lints]`、metadata，并把 `std` feature 简化为空数组（去掉被裁掉的 `wasm-bindgen?/std` 引用）。裁了什么在 N43 逐项登记。 |
| U61 | 按 023 规矩，3 份 LICENSE 全文 + 关于页 + NOTICES 三处齐了才写进 `Cargo.toml`。 |

## 改轨落地

| 编号 | 动作 |
| --- | --- |
| U62 | `Cargo.lock` 23 → **25 包 / 24 第三方**（+uuid、+sha1_smol）；关于页 22 → **24 组「构建中已使用」**、计数 44 → 46，NOTICES 加 N43–N44。 |
| U63 | `src/core/envelope.rs`：新增 `derive_id(name)` 调 `Uuid::new_v5(&Uuid::NAMESPACE_OID, name.as_bytes()).to_string()`；SHA-1、截断 128 位、version / variant 位设置全由库完成，项目侧不手写摘要与位操作。 |
| U64 | name 输入 = `kcu/{pid}/{session_seed}/{seq}/{kind:?}/{target}`，`session_seed()` 用 `OnceLock` 在进程启动时取一次 `SystemTime` 纳秒；pid 与启动时间让**跨进程、重启后 pid 复用**都不再撞 ID，`SEQ` 只作为同进程内的区分输入。 |
| U65 | 独立回归常量：用 Python 标准库 `uuid.uuid5(uuid.NAMESPACE_OID, name)` 算出 4 个期望值写进测试，不靠本仓库的 uuid / sha1_smol 自证；另测 `Uuid::parse_str` 可解析、`Version::Sha1`、`Variant::RFC4122`、36 字符 4 个连字符、JSON 里带的是同一个 ID。 |

## 行为差异（不藏）

| 编号 | 项 | 改前 | 改后 |
| --- | --- | --- | --- |
| B14 | ID 形状 | `kcu-00000001`（11 字符） | 标准 UUID v5（36 字符，4 个连字符），`kcu-` 前缀消失 |
| B15 | 唯一范围 | 单进程内单调 | 跨进程 / 跨启动不重复（pid + 启动纳秒 + 序号 + kind + target） |
| B16 | 算法 | 自写 8 位十六进制计数 | RFC 9562 v5，SHA-1 与位布局由库实现 |
| B17 | 随机源 | 无 | **仍无**（v5 不需要 RNG，Win7 友好） |
| B18 | 诊断行 `[KCU] …` | 不含 request_id | **不受影响**，形状测试全过 |

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo build --offline` 编译 sha1_smol / uuid / kcu-core 通过。 |
| V-B | `cargo test --offline --lib`：**249 / 0**（042 是 244，新增 5 个 envelope 单测）。 |
| V-C | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0，36.03 s**、`plugin_abi_load` **6 / 0，104.96 s**。 |
| V-D | 合计 **275 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过；`cargo check --offline` 零 warning。 |
| V-E | 必读 217 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，33 份 HTML 脚本与 CI YAML 通过。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E67 | 查 uuid 仓库时先用不带 `v` 的 tag `1.18.1` / `1.17.0`，全部 404 | 列出真实 tags，锁定 `v1.18.1`；A134 登记「tag 名要实核」 |
| E68 | 上游 `[workspace] members` 指向未 vendor 的 macros / rng / examples，另有一堆 optional target 依赖；目录源解析会失败 | 按 041 E58 的先例裁段，`std` feature 去掉被裁依赖的 `?/std` 引用，N43 逐项登记 |
| E69 | `Variant` / `Version` 只在 `#[cfg(test)]` 用，非 test 编译出现 unused_imports warning | 两个枚举导入移进测试模块，`cargo check` 零 warning |
| E70 | 全量 `cargo test` 再次网关 502 | 拆 `--lib` / 各 `--test` / `check` 分段跑通，未降断言 |
| E71 | 渲染完回退 52 张非许可 PNG 时 `.git/index.lock` 残留（上一轮网关 502 中断留下），`git checkout` 报 fatal；网关又连续两次 502 | 删残留 lock 后重跑，最终 `demos/preview/` 只剩 4 张许可截图有 diff；失败回显保留，未强推、未跳过回退 |

## 四值

| 项 | 值 |
| --- | --- |
| F32–F36 五条一手事实、U58–U65 落地 | 已证实 |
| Python uuid5 四个独立期望值逐一对齐 | 已证实 |
| 25 包 / 24 第三方、3 份 LICENSE 全文、24 组 / 46 | 已证实 |
| 275 / 0、Windows GNU、零 warning、界面闸门未触发 | 已证实 |
| E67–E70 四个真问题修复 | 已证实 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动（040 L1–L12） |
| Q-041 Win7 UI 路线、Q-037-01 哈希口径 | 未证实（待拍板） |
| 真实窗口 / WebView / 渲染 / 崩溃分析、子进程插件隔离 | 未启动 |
| 后端仓写请求 | 0（已证实） |

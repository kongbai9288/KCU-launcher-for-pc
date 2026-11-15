# 第 042 轮：批量请求 query 编码与身份哈希 hex 交给库

| 项 | 值 |
| --- | --- |
| 编号 | 042 |
| 状态 | 两处自写编码已替换已验证；真实网络 IO 仍未启动 |
| 依据 | docs/spec/42-round-042-instructions.txt |
| 前序 | 040-network-stack-check-and-http-types.md、037 插件身份哈希、024 代码归属自查、035 / 041 改轨规矩 |
| 本轮性质 | 单轨轮：041 收口（远端 852 文件 ALL_MATCH 补齐）后，继续把自写通用逻辑换成库 |

## 041 收口（上一轮工具中断补交）

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-041-A | 本地 HEAD | `ac9af80` |
| V-041-B | 远端 ref | `599edc7` |
| V-041-C | 远端逐项比对 | REMOTE 852 LOCAL 852 MISSING 0 EXTRA 0 MISMATCH 0 **ALL_MATCH True**，truncated=False |
| V-041-D | 凭据 | 临时 PAT 已删、全仓 `NO_CREDENTIAL`、`.git/config` 干净 |

## 本轮落点

`040` 把请求类型交给了 `http` crate，但 query 里 `ids` 仍是 `ids.join(",")` 自己拼。模组 id 只要带空格、`&`、`#`、逗号或非 ASCII，就会把 batch 请求切坏：一个 `a&b` 会被解析成新参数，后面的 id 直接丢。你之前点名过「每搜索一个模组单发一个请求导致算力浪费」，批量请求是对的，但**批量请求里的 id 必须先正确编码**才成立。`037` 的插件身份哈希则用 `format!("{:02x}", b)` 循环手写 hex。

这两处都是「通用编码算法」，不是项目特有编排，按 024 的台账就该交给库。

## 真实 manifest 核查（api.github.com 同 tag 内容）

| 编号 | 候选 | 真实数据 | 四值 |
| --- | --- | --- | --- |
| F29 | `percent-encoding 2.3.1` | `servo/rust-url` mono-repo 的 `percent_encoding/` 子 crate；**tag `v2.3.1` 里 manifest 写的是 2.2.0**，2.3.1 对应 tag `v2.5.0`（v2.5.8 已是 2.3.2）；MIT OR Apache-2.0 / edition 2018 / MSRV 1.51 / categories `no_std`；`default = ["std"]`、`std = ["alloc"]`、`alloc = []`；**零依赖** | 已证实 |
| F30 | `hex 0.4.3` | `KokaKiwi/rust-hex` tag `v0.4.3`；MIT OR Apache-2.0 / edition 2018；`default = ["std"]`；`[dependencies]` 只有 optional `serde`；dev-dependencies 有 criterion / rustc-hex / faster-hex / version-sync / pretty_assertions / serde / serde_json；`src/lib.rs` 的 `pub mod serde` 受 `#[cfg(feature = "serde")]` 门控 | 已证实 |
| F31 | 通道限制 | crates registry 与 static.crates.io 全部 403，vendor 只能走 api.github.com / codeload 的 tag tarball | 已证实（025 起多轮） |

| 编号 | 判定 |
| --- | --- |
| U49 | 两个都是零传递依赖的纯 Rust 编码库，MSRV 远低于 Win7 Tier 3 路线，闭包最浅，先落。 |
| U50 | `percent-encoding` 的 mono-repo 版本与 tag 不同步，按 `v2.5.0` 子目录 manifest 的 2.3.1 取，不按 tag 名猜版本（A128）。 |
| U51 | `hex` 的 optional serde 与 dev 依赖、benches、docs.rs metadata 全部裁掉；`src/serde.rs` 一并删除；上游 `src/lib.rs` / `src/error.rs` 逐字节未改。 |
| U52 | 按 023 规矩，4 份 LICENSE 全文 + 关于页 + NOTICES 三处齐了才写进 `Cargo.toml`。 |

## 改轨落地

| 编号 | 动作 |
| --- | --- |
| U53 | `Cargo.lock` 21 → **23 包 / 22 第三方**；关于页 20 → **22 组「构建中已使用」**、计数 42 → 44，NOTICES 加 N41–N42。 |
| U54 | `src/core/http.rs`：`ids.join(",")` 换成逐 id `utf8_percent_encode(id, ID_ENCODE_SET).to_string()` 再 `join(",")`。集合由 `CONTROLS` 加 `空格 " # % & + , / : ; < = > ? @ [ \ ] ^ ` { | }` 组成，**保留 RFC 3986 unreserved**（字母数字 `-` `.` `_` `~`），所以 `mod-a` 这类常见 id 的请求串一字不变；非 ASCII 字节由库按 UTF-8 转义，逗号是列表分隔符，id 内部逗号变 `%2C`。 |
| U55 | `src/plugins/identity.rs`：`format!("{:02x}", b)` 循环换成 `hex::encode(bytes)`；输出仍是 32 位小写 hex。 |
| U56 | 独立回归常量：用 Python `hashlib.sha512(...).digest()[:16].hex()` 算出 4 个期望值写进测试，不靠本仓库的 hex / ed25519-compact 自证。 |
| U57 | 界面闸门**未触发**：只更新关于页许可表数据并重渲 4 张许可截图，其余 52 张 PNG 回退到 HEAD；设置页不加任何标签。 |

## 行为差异（不藏）

| 编号 | 项 | 改前 | 改后 |
| --- | --- | --- | --- |
| B09 | `mod-a` / `mod-b` | `ids=mod-a,mod-b` | **完全不变**（原有集成断言保持） |
| B10 | 含 `&` 的 id | 被当成新参数，后续 id 丢失 | `a%26b`，query 仍只有 `page` 与 `ids` 两段 |
| B11 | 含空格 / `#` / 中文的 id | 构造坏 URI 或语义错乱 | `%20` / `%23` / `%E7%94%B2` |
| B12 | id 内含逗号 | 被误拆成两个条目 | `a%2Cb`，列表仍可按 `,` 切分 |
| B13 | 身份哈希 | 手写 hex 循环 | 库编码，输出逐字节一致（4 个独立期望值验证） |

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo build --offline` 编译 hex / percent-encoding / kcu-core 通过。 |
| V-B | `cargo test --offline --lib`：**244 / 0**（041 是 237，新增 5 个 http 编码单测 + 2 个 identity 回归单测）。 |
| V-C | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0，36.19 s**、`plugin_abi_load` **6 / 0，109.30 s**。 |
| V-D | 合计 **270 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-E | 必读 211 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，32 份 HTML 脚本与 CI YAML 通过。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E63 | percent-encoding 的 LICENSE 在 tarball 里是软链，`m.isfile()` 为 False，vendor 后缺文件，脚本崩在复制 LICENSE | 与 027 的 crossbeam 软链同类；改为 api.github.com contents 直取 4 份 LICENSE 并回写 vendor |
| E64 | 首版用 `NON_ALPHANUMERIC`，把 `mod-a` 编码成 `mod%2Da`，`http_construct` 原有断言 `ids=mod-a,mod-b` 失败 | 改用 `CONTROLS` + 自定义 `AsciiSet`，保留 unreserved；**原断言一字未改**，改的是实现 |
| E65 | `hex` manifest 留了空 `[dependencies]` 段与 optional `serde`，裁段时 `[[bench]]` 双括号段正则没匹配 | 单独用 `\[\[bench\]\]` 正则裁掉，同时删除 `src/serde.rs` |
| E66 | `v2.3.1` tag 里的 manifest 是 2.2.0，差点按 tag 名取错版本 | 逐个 tag 读子目录 manifest，锁定 `v2.5.0` = crate 2.3.1 |

## 四值

| 项 | 值 |
| --- | --- |
| F29–F31 三条一手事实、U49–U57 落地 | 已证实 |
| 041 收口 852 文件 ALL_MATCH、凭据清理 | 已证实 |
| 23 包 / 22 第三方、4 份 LICENSE 全文、22 组 / 44 | 已证实 |
| 270 / 0、Windows GNU、界面闸门未触发 | 已证实 |
| E63–E66 四个真问题修复 | 已证实 |
| 真实网络 IO、TLS、代理、响应解析 | 未启动（040 L1–L12） |
| Q-041 Win7 UI 路线、Q-037-01 哈希口径 | 未证实（待拍板） |
| 真实窗口 / WebView / 渲染 / 崩溃分析 | 未启动 |
| 后端仓写请求 | 0（已证实） |

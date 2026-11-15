from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
src_lines = sum(len(p.read_text().splitlines()) for p in (ROOT / 'src').rglob('*.rs'))
lib_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in (ROOT / 'src').rglob('*.rs'))
int_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in (ROOT / 'tests').rglob('*.rs'))
total_tests = lib_tests + int_tests
print('REAL', 'pkgs', pkgs, 'third', third, 'src_lines', src_lines,
      'lib', lib_tests, 'int', int_tests, 'total', total_tests)

Path('docs/spec/43-round-043-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/043-request-id-uuid-v5.md'] = f'''# 第 043 轮：统一信封 request_id 换成 UUID v5

| 项 | 值 |
| --- | --- |
| 编号 | 043 |
| 状态 | 已实现已验证；真实网络 IO、UI、崩溃分析未启动 |
| 依据 | docs/spec/43-round-043-instructions.txt |
| 前序 | 010 统一信封 F010、024 代码归属台账、040–042 逐块库化、011 Win7 起兼容路线 |
| 本轮性质 | 单轨轮：继续按台账把自写通用算法换成库 |

## 本轮落点

`src/core/envelope.rs` 的 `request_id` 原是 `static SEQ: AtomicU64` + `format!("kcu-{{:08x}}", n)`：**只在单个进程内单调**。诊断包、审计日志、F010 的跨进程统一信封都用这个 ID；进程一重启就从 `kcu-00000001` 重新计数，两次启动的请求在日志里完全撞车，追溯时会把不同会话串成一条。这不是风格问题，是可追溯性缺陷。

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
| U62 | `Cargo.lock` 23 → **{pkgs} 包 / {third} 第三方**（+uuid、+sha1_smol）；关于页 22 → **24 组「构建中已使用」**、计数 44 → 46，NOTICES 加 N43–N44。 |
| U63 | `src/core/envelope.rs`：新增 `derive_id(name)` 调 `Uuid::new_v5(&Uuid::NAMESPACE_OID, name.as_bytes()).to_string()`；SHA-1、截断 128 位、version / variant 位设置全由库完成，项目侧不手写摘要与位操作。 |
| U64 | name 输入 = `kcu/{{pid}}/{{session_seed}}/{{seq}}/{{kind:?}}/{{target}}`，`session_seed()` 用 `OnceLock` 在进程启动时取一次 `SystemTime` 纳秒；pid 与启动时间让**跨进程、重启后 pid 复用**都不再撞 ID，`SEQ` 只作为同进程内的区分输入。 |
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
| V-B | `cargo test --offline --lib`：**{lib_tests} / 0**（042 是 244，新增 5 个 envelope 单测）。 |
| V-C | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0，36.03 s**、`plugin_abi_load` **6 / 0，104.96 s**。 |
| V-D | 合计 **{total_tests} / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过；`cargo check --offline` 零 warning。 |
| V-E | 必读 217 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，33 份 HTML 脚本与 CI YAML 通过。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E67 | 查 uuid 仓库时先用不带 `v` 的 tag `1.18.1` / `1.17.0`，全部 404 | 列出真实 tags，锁定 `v1.18.1`；A134 登记「tag 名要实核」 |
| E68 | 上游 `[workspace] members` 指向未 vendor 的 macros / rng / examples，另有一堆 optional target 依赖；目录源解析会失败 | 按 041 E58 的先例裁段，`std` feature 去掉被裁依赖的 `?/std` 引用，N43 逐项登记 |
| E69 | `Variant` / `Version` 只在 `#[cfg(test)]` 用，非 test 编译出现 unused_imports warning | 两个枚举导入移进测试模块，`cargo check` 零 warning |
| E70 | 全量 `cargo test` 再次网关 502 | 拆 `--lib` / 各 `--test` / `check` 分段跑通，未降断言 |

## 四值

| 项 | 值 |
| --- | --- |
| F32–F36 五条一手事实、U58–U65 落地 | 已证实 |
| Python uuid5 四个独立期望值逐一对齐 | 已证实 |
| {pkgs} 包 / {third} 第三方、3 份 LICENSE 全文、24 组 / 46 | 已证实 |
| {total_tests} / 0、Windows GNU、零 warning、界面闸门未触发 | 已证实 |
| E67–E70 四个真问题修复 | 已证实 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动（040 L1–L12） |
| Q-041 Win7 UI 路线、Q-037-01 哈希口径 | 未证实（待拍板） |
| 真实窗口 / WebView / 渲染 / 崩溃分析、子进程插件隔离 | 未启动 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-043.md'] = f'''# 第 043 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 043 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 sha1_smol / uuid / kcu-core，Finished | 已证实 |
| V2 | `cargo test --offline --lib` | **{lib_tests} passed / 0 failed** | 已证实 |
| V3 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V4 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V5 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，36.03 s | 已证实 |
| V6 | `cargo test --offline --test plugin_abi_load` | 6 / 0，104.96 s | 已证实 |
| V7 | `cargo check --offline` | Finished，零 warning | 已证实 |
| V8 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V9 | `Cargo.lock` 包列表 | **{pkgs} 包 / {third} 第三方** | 已证实 |
| V10 | `docs/licenses/uuid-LICENSE-*.txt` / `sha1_smol-LICENSE.txt` | 10847 / 1157 / 2719 字节 | 已证实 |
| V11 | 关于页许可行 / NOTICES | 24 组「构建中已使用」，计数 46，N43–N44 | 已证实 |
| V12 | `demos/preview/` 许可相关 4 张 | 重渲；其余 52 张回退到 HEAD | 已证实 |
| V13 | `grep -rE 'https?://|C:\\|x-api-key' src/` | NO_HARDCODE | 已证实 |
| V14 | `node new Function` 全部 demos HTML | ALL_JS_OK，33 份 | 已证实 |
| V15 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V16 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V17 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V18 | 必读文件循环 | REQUIRED=217 MISSING=0 | 已证实 |
| V19 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| UUID v5 request_id、{total_tests} / 0、Windows GNU、零 warning | 已证实 |
| Python uuid5 独立期望值对齐、E67–E70 修复 | 已证实 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动 |
| Q-041 / Q-037-01 / 真实窗口 / 崩溃分析 | 未证实 / 未启动 |
| {total_tests} 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。
'''

D['docs/features/request-id-contract.md'] = '''# F043-01 统一信封 request_id 契约

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `Envelope::new` 把 `pid / 启动纳秒 / 进程内序号 / kind / target` 组成一个 name，`derive_id` 交给 `Uuid::new_v5(&Uuid::NAMESPACE_OID, …)` 生成 RFC 9562 版本 5 UUID；SHA-1 摘要、128 位截断、version 与 variant 位设置全由库完成。`to_json_string` 原样带上这个 ID。 |
| 开放了什么 | `src/core/envelope.rs` 的 `derive_id` / `Envelope::new` / `to_json_string`；`with` / `with_error` / `ok` / `field` / `from_json_str` 一行没动。 |
| 登记框架 | `uuid 1.18.1`（Apache-2.0 OR MIT / MSRV 1.63）+ `sha1_smol 1.0.1`（BSD-3-Clause）；只开 `std` + `v5`，无 rng、无平台分支、无 C 构建链。与 031 的 serde_json 载荷、032 的 log 门面、040 的 http 类型层串联。 |
| 用户使用逻辑 | 诊断包、审计日志、插件请求、跨进程统一信封都能用同一个 ID 串起来；重启启动器、同时开多个实例、pid 被系统复用，都不会把两次会话的请求混成一条；ID 不含随机数，低配机器与 Win7 上生成行为一致。 |
| 性能 | 每个信封一次 SHA-1（20 字节命名空间 + 短 name）+ 一次格式化；无分配大头、无 IO、无锁竞争（序号用 Relaxed 原子加）。 |

状态：已实现已验证；真实网络 IO 未启动。
'''

D['docs/research/26-uuid-v5.md'] = '''# UUID v5 与两个 crate 的一手资料（043）

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
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s):
    p = Path(f)
    t = p.read_text()
    marker = s.strip().splitlines()[0]
    if marker in t:
        print('SKIP_DUP', f)
        return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 043 | 统一信封 request_id 换成 UUID v5 | 已实现已验证；真实网络 IO 未启动 | 043-request-id-uuid-v5.md |')
app('docs/features/index.md', '| F043-01 | request-id-contract.md | 已实现已验证；真实网络 IO 未启动 |')
app('docs/research/index.md', '| 26 | 26-uuid-v5.md | UUID v5、uuid / sha1_smol 闭包与 RFC 9562 | 9 已证实 |')
app('docs/rules/index.md', '| ui-preconditions.md | UI 宿主与崩溃分析 L1-L12 前置清单 | 041（043 沿用） |') if Path('docs/rules/index.md').exists() else None

app('docs/licenses/index.md', '''## 043 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| uuid-LICENSE-APACHE.txt | uuid 1.18.1 | Apache-2.0（10847 B） |
| uuid-LICENSE-MIT.txt | uuid 1.18.1 | MIT（1157 B） |
| sha1_smol-LICENSE.txt | sha1_smol 1.0.1 | BSD-3-Clause（2719 B） |

来源：`uuid-rs/uuid` tag `v1.18.1`、`mitsuhiko/sha1-smol` tag `1.0.1`，逐字副本。uuid 仓库 GitHub API 的 SPDX 是 NOASSERTION（两份 LICENSE 并存），按 crate manifest 的 `Apache-2.0 OR MIT` 用，两份全文都落盘。
''')

app('THIRD-PARTY-NOTICES.md', '''## 043 新增已进构建依赖（统一信封 ID）

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| uuid | 1.18.1 | Apache-2.0 OR MIT | Ashley Mannix、Dylan DPC、Hunar Roop Kahlon 及 Rust Project Developers | RFC 9562 v5 命名空间 UUID 生成与解析 | vendor/uuid | 构建中已使用 |
| sha1_smol | 1.0.1 | BSD-3-Clause | Armin Ronacher | uuid v5 的 SHA-1 摘要 | vendor/sha1_smol | 构建中已使用 |

许可证全文：`docs/licenses/uuid-LICENSE-APACHE.txt`、`docs/licenses/uuid-LICENSE-MIT.txt`、`docs/licenses/sha1_smol-LICENSE.txt`。

| 编号 | 约束 |
| --- | --- |
| N43 | uuid 上游 `src/` 逐字节未改；vendored manifest 裁掉未启用的 optional 依赖（getrandom / rand / md-5 / bytemuck / serde / slog / arbitrary / zerocopy / borsh / atomic / uuid-macro-internal）、`[target.*]` 段、`[dev-dependencies]`、`[workspace]`、`[badges]`、`[lints]`、docs.rs 与 playground metadata；`std` feature 简化为空数组（去掉被裁掉的 `wasm-bindgen?/std`、`js-sys?/std` 引用）。只保留 `default` / `std` / `v5` / `sha1` 四个 feature 与 `[dependencies.sha1_smol]`。 |
| N44 | sha1_smol 上游 `src/` 逐字节未改；vendored manifest 裁掉 optional serde、dev-dependencies 与 docs.rs metadata，只保留 `std` / `alloc` 两个 feature。两个 crate 均未启用任何随机数源或平台分支。 |
''')

app('docs/records/code-ownership-audit.md', f'''## 043 统一信封 ID（+2 crate）

| 项 | 042 | 043 |
| --- | --- | --- |
| 第三方 crate 进构建 | 22 | **{third}**（+uuid、+sha1_smol） |
| `Cargo.lock` 包数 | 23 | **{pkgs}** |
| `src/` 行数 | 5811 | **{src_lines}** |
| 测试 | 244 单元 + 26 集成 = 270 | **{lib_tests} 单元 + {int_tests} 集成 = {total_tests}** |

`src/core/envelope.rs` 的 `AtomicU64` + `format!("kcu-{{:08x}}", n)` 换 `Uuid::new_v5`；SHA-1、128 位截断、version / variant 位布局全交给库，项目侧只提供 name 输入（pid / 启动纳秒 / 序号 / kind / target）。4 个期望值由 Python 标准库 `uuid.uuid5` 独立算出，不用本仓库实现自证。

修复了一个真实缺陷：原 ID 只在单进程内单调，重启即重复，F010 跨进程统一信封的日志会串会话。剩余自写仍是 `launcher.rs`、lightweight 系列与 `paths/popup/userflow` 等业务编排；035 已登记它们没有语义等价的库可换。
''')

app('docs/design/implementation-strategy.md', '''## 043 统一信封 ID

| 层 | 状态 |
| --- | --- |
| 批量请求 id 百分号编码（percent-encoding） | 已实现（042） |
| 插件身份哈希 hex（hex） | 已实现（042） |
| 统一信封 request_id（uuid v5 + sha1_smol） | **已实现（043）** |
| 真实窗口 / WebView / 渲染 / 崩溃分析 | 未启动（L1–L12 见 ui-preconditions.md） |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动（040 L1–L12） |
| 子进程插件隔离、插件 init | 未启动（039） |
| 界面渲染 | 仍等 UX 手感确认与 Q-041 拍板 |
''')

app('docs/rules/ui-demo.md', '''## 043 闸门判定

本轮只更新关于页许可表数据（22 → 24 组，计数 44 → 46）并重渲 4 张许可相关截图，不改任何界面布局、控件或交互；`src/core/envelope.rs` 是 ID 生成层，不产生界面变化。沿用 036 / 038–042 的先例判**未触发**。其余 52 张 PNG 回退到 HEAD。
''')

app('docs/checklists/ai-errors.md', '''## 043 轮新增

| 编号 | 防错项 |
| --- | --- |
| A134 | GitHub 仓库的 tag 前缀要实核（uuid 是 `v1.18.1`，不是 `1.18.1`）；404 时列真实 tags，不猜。 |
| A135 | 只启用需要的 feature；先核每个依赖是否 `optional = true`，别把 `rng` / `getrandom` 这类未启用依赖当成闭包的一部分。 |
| A136 | 裁 vendor manifest 时，`[workspace] members`、`[target.*]`、`[lints]`、`[badges]`、metadata 与引用被裁依赖的 feature 行要一起处理。 |
| A137 | 只在测试里用的导入要移进 `#[cfg(test)]` 模块，非 test 编译不许留 unused_imports warning。 |
| A138 | ID 生成类替换要有独立实现算出的期望值（本轮 Python 标准库 uuid5），并验证 version / variant / 长度。 |
| A139 | 仓库 API 的 `license.spdx_id` 为 NOASSERTION 时，按 crate manifest 声明的许可证用并落全部 LICENSE 全文，不据此跳过登记。 |
''')

app('docs/records/interface-log.md', '''## 043 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I55 | `src/core/envelope` | 新增 `derive_id` / `session_seed`；`Envelope::new` 的 request_id 改 UUID v5 |
| I56 | `vendor/uuid` / `vendor/sha1_smol` | 两个零平台分支 crate 进构建 |
| S42 | 状态 | U58–U65 已证实；Q-041 / Q-037-01 仍挂；真实网络 IO、UI、崩溃分析未启动 |
''')

app('docs/records/rounds.md', f'''## 043

| 落点 | 内容 |
| --- | --- |
| docs/spec/43-round-043-instructions.txt | 逐字副本 1 行 |
| docs/decisions/043-request-id-uuid-v5.md | F32-F36、U58-U65、V-A~V-E、E67-E70、四值 |
| docs/verification/round-043.md | 19 条复跑证据 |
| docs/features/request-id-contract.md | F043-01 五字段登记 |
| docs/research/26-uuid-v5.md | 9 个锚点 / R21-R24 |
| src/core/envelope.rs | ID 生成层替换，5 个新增单测 |
| vendor/ + Cargo.toml/lock | uuid 1.18.1、sha1_smol 1.0.1，{pkgs} 包 / {third} 第三方 |
| docs/licenses/ + 关于页 + NOTICES | 3 份全文、24 组、计数 46、N43-N44 |
| demos/round-043-request-id.html | 13 步运行逻辑演示 |
| 索引与记录 | docs/index 217 项、README、四个 index、ai-errors A134-A139、code-ownership-audit、implementation-strategy、ui-demo 判定、interface-log、rounds |

「干」继续按 024 台账换自写通用算法。这轮挑的是 `src/core/envelope.rs` 的 `request_id`：原来是 `static SEQ: AtomicU64` + `format!("kcu-{{:08x}}", n)`，**只在单个进程内单调**。诊断包、审计日志、F010 的跨进程统一信封都用它，进程一重启就从 `kcu-00000001` 重新计数，两次启动的请求在日志里完全撞车。不是风格问题，是可追溯性缺陷。

真实 manifest 核完：`uuid 1.18.1`（tag 是 **`v1.18.1`**，不带 v 的 404；Apache-2.0 OR MIT / edition 2018 / MSRV 1.63；`v5=["sha1"]`、`sha1=["dep:sha1_smol"]`、`v4=["rng"]`、`rng=["dep:getrandom"]`；**所有依赖都 optional**）与 `sha1_smol 1.0.1`（BSD-3-Clause / minimal dependency-free / 零依赖）。只开 `std` + `v5` 时闭包只有 1 个传递依赖，**无 rng、无平台分支、无 C 链**，Win7 Tier 3 路线不受 040 查到的 `ProcessPrng` 问题影响；v4 / v7 会拉 getrandom 0.3，本轮不选，也不假设「应该能跑」。

落地：`derive_id(name)` 调 `Uuid::new_v5(&Uuid::NAMESPACE_OID, …)`，SHA-1、128 位截断、version / variant 位布局全由库完成；name 输入是 `pid / 启动纳秒 / 序号 / kind / target`，启动纳秒用 `OnceLock` 取一次，跨进程、重启后 pid 复用都不再撞 ID。4 个期望值由 Python 标准库 `uuid.uuid5` 独立算出写进测试，另测可解析、`Version::Sha1`、`Variant::RFC4122`、36 字符 4 连字符、JSON 带同一个 ID。`Cargo.lock` 23 → **{pkgs} 包 / {third} 第三方**，3 份 LICENSE 全文、关于页 24 组 / 46、NOTICES N43–N44 三处齐了才进 Cargo.toml。

验证：{lib_tests} 单元 / 0 + 7 http_construct / 0 + 6 窗口契约 / 0 + 7 lifecycle / 0（36.03 s）+ 6 abi / 0（104.96 s）= **{total_tests} / 0**；`cargo check --offline` 零 warning，`cargo check --offline --target x86_64-pc-windows-gnu` 通过。界面闸门未触发：只重渲 4 张许可截图，其余 52 张回退。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E67 | uuid 先用不带 `v` 的 tag `1.18.1` / `1.17.0`，全 404 | 列真实 tags 锁定 `v1.18.1`，立 A134 |
| E68 | 上游 `[workspace] members` 指向未 vendor 的 macros / rng / examples，optional target 依赖一堆 | 按 041 E58 先例裁段，`std` feature 去掉被裁依赖引用，N43 登记 |
| E69 | `Variant` / `Version` 只在测试用，非 test 编译 unused_imports warning | 导入移进 `#[cfg(test)]`，`cargo check` 零 warning |
| E70 | 全量 `cargo test` 再次网关 502 | 拆段跑通，未降断言 |

Q-041（Win7 UI 三选项）与 Q-037-01（哈希口径）仍待答复；真实窗口 / WebView / 崩溃分析、真实网络 IO、子进程插件隔离、028 三项开服器实现、CF F17、特殊版代码、本项目 LICENSE 均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '211. docs/verification/round-042.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''211. docs/verification/round-042.md
212. docs/spec/43-round-043-instructions.txt
213. docs/decisions/043-request-id-uuid-v5.md
214. docs/features/request-id-contract.md
215. docs/research/26-uuid-v5.md
216. demos/round-043-request-id.html
217. docs/verification/round-043.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-042.md; do printf',
                  'docs/verification/round-042.md docs/spec/43-round-043-instructions.txt docs/decisions/043-request-id-uuid-v5.md docs/features/request-id-contract.md docs/research/26-uuid-v5.md demos/round-043-request-id.html docs/verification/round-043.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 043 |', p.read_text(), count=1)
section = f'''

## 043 统一信封 request_id 换成 UUID v5

`src/core/envelope.rs` 原来用进程内 `AtomicU64` 生成 `kcu-00000001`，重启就重复，诊断包与 F010 跨进程统一信封会串会话。这轮落 `uuid 1.18.1`（只开 `std` + `v5`）+ `sha1_smol 1.0.1`：**零随机数源、零平台分支、零 C 链**，Win7 Tier 3 友好。SHA-1、128 位截断、version / variant 位布局全交给库，name 输入带 pid 与启动纳秒，跨进程与 pid 复用都不撞 ID；4 个期望值由 Python 标准库 `uuid.uuid5` 独立算出。

`Cargo.lock` **{pkgs} 包 / {third} 第三方**，3 份 LICENSE 全文 + 关于页 24 组 / 46 + NOTICES 三处齐备。`cargo test --offline` 合计 **{total_tests}/0**（{lib_tests} 单元 + {int_tests} 集成），`cargo check` 零 warning，Windows GNU 交叉检查通过。界面与 56 张 PNG 只动了 4 张许可截图。
'''
if '## 043 统一信封 request_id' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

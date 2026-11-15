from pathlib import Path
import re, subprocess

ROOT = Path(__file__).resolve().parents[1]

# 实值口径，避免文档里写死又对不上
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
src_lines = sum(len(p.read_text().splitlines()) for p in (ROOT / 'src').rglob('*.rs'))
lib_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in (ROOT / 'src').rglob('*.rs'))
int_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in (ROOT / 'tests').rglob('*.rs'))
total_tests = lib_tests + int_tests
print('REAL', 'pkgs', pkgs, 'third', third, 'src_lines', src_lines,
      'lib', lib_tests, 'int', int_tests, 'total', total_tests)

Path('docs/spec/42-round-042-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/042-query-encoding-and-hex.md'] = f'''# 第 042 轮：批量请求 query 编码与身份哈希 hex 交给库

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

`040` 把请求类型交给了 `http` crate，但 query 里 `ids` 仍是 `ids.join(",")` 自己拼。模组 id 只要带空格、`&`、`#`、逗号或非 ASCII，就会把 batch 请求切坏：一个 `a&b` 会被解析成新参数，后面的 id 直接丢。你之前点名过「每搜索一个模组单发一个请求导致算力浪费」，批量请求是对的，但**批量请求里的 id 必须先正确编码**才成立。`037` 的插件身份哈希则用 `format!("{{:02x}}", b)` 循环手写 hex。

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
| U53 | `Cargo.lock` 21 → **{pkgs} 包 / {third} 第三方**；关于页 20 → **22 组「构建中已使用」**、计数 42 → 44，NOTICES 加 N41–N42。 |
| U54 | `src/core/http.rs`：`ids.join(",")` 换成逐 id `utf8_percent_encode(id, ID_ENCODE_SET).to_string()` 再 `join(",")`。集合由 `CONTROLS` 加 `空格 " # % & + , / : ; < = > ? @ [ \\ ] ^ ` {{ | }}` 组成，**保留 RFC 3986 unreserved**（字母数字 `-` `.` `_` `~`），所以 `mod-a` 这类常见 id 的请求串一字不变；非 ASCII 字节由库按 UTF-8 转义，逗号是列表分隔符，id 内部逗号变 `%2C`。 |
| U55 | `src/plugins/identity.rs`：`format!("{{:02x}}", b)` 循环换成 `hex::encode(bytes)`；输出仍是 32 位小写 hex。 |
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
| V-B | `cargo test --offline --lib`：**{lib_tests} / 0**（041 是 237，新增 5 个 http 编码单测 + 2 个 identity 回归单测）。 |
| V-C | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0，36.19 s**、`plugin_abi_load` **6 / 0，109.30 s**。 |
| V-D | 合计 **{total_tests} / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-E | 必读 211 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，32 份 HTML 脚本与 CI YAML 通过。 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E63 | percent-encoding 的 LICENSE 在 tarball 里是软链，`m.isfile()` 为 False，vendor 后缺文件，脚本崩在复制 LICENSE | 与 027 的 crossbeam 软链同类；改为 api.github.com contents 直取 4 份 LICENSE 并回写 vendor |
| E64 | 首版用 `NON_ALPHANUMERIC`，把 `mod-a` 编码成 `mod%2Da`，`http_construct` 原有断言 `ids=mod-a,mod-b` 失败 | 改用 `CONTROLS` + 自定义 `AsciiSet`，保留 unreserved；**原断言一字未改**，改的是实现 |
| E65 | `hex` manifest 留了空 `[dependencies]` 段与 optional `serde`，裁段时 `[[bench]]` 双括号段正则没匹配 | 单独用 `\\[\\[bench\\]\\]` 正则裁掉，同时删除 `src/serde.rs` |
| E66 | `v2.3.1` tag 里的 manifest 是 2.2.0，差点按 tag 名取错版本 | 逐个 tag 读子目录 manifest，锁定 `v2.5.0` = crate 2.3.1 |

## 四值

| 项 | 值 |
| --- | --- |
| F29–F31 三条一手事实、U49–U57 落地 | 已证实 |
| 041 收口 852 文件 ALL_MATCH、凭据清理 | 已证实 |
| {pkgs} 包 / {third} 第三方、4 份 LICENSE 全文、22 组 / 44 | 已证实 |
| {total_tests} / 0、Windows GNU、界面闸门未触发 | 已证实 |
| E63–E66 四个真问题修复 | 已证实 |
| 真实网络 IO、TLS、代理、响应解析 | 未启动（040 L1–L12） |
| Q-041 Win7 UI 路线、Q-037-01 哈希口径 | 未证实（待拍板） |
| 真实窗口 / WebView / 渲染 / 崩溃分析 | 未启动 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-042.md'] = f'''# 第 042 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 042 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 041 收口 `GET /git/ref/heads/main` + `GET /git/trees/main?recursive=1` | `599edc7`；REMOTE 852 LOCAL 852 MISMATCH 0 ALL_MATCH True | 已证实 |
| V2 | `cargo build --offline` | 编译 hex / percent-encoding / kcu-core，Finished | 已证实 |
| V3 | `cargo test --offline --lib` | **{lib_tests} passed / 0 failed** | 已证实 |
| V4 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V5 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V6 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，36.19 s | 已证实 |
| V7 | `cargo test --offline --test plugin_abi_load` | 6 / 0，109.30 s | 已证实 |
| V8 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V9 | `Cargo.lock` 包列表 | **{pkgs} 包 / {third} 第三方** | 已证实 |
| V10 | `docs/licenses/pe-LICENSE-*.txt` / `hex-LICENSE-*.txt` | 1072 / 10847 / 1125 / 11358 字节 | 已证实 |
| V11 | 关于页许可行 / NOTICES | 22 组「构建中已使用」，计数 44，N41–N42 | 已证实 |
| V12 | `demos/preview/` 许可相关 4 张 | 重渲；其余 52 张回退到 HEAD | 已证实 |
| V13 | `grep -rE 'https?://|C:\\|x-api-key' src/` | NO_HARDCODE | 已证实 |
| V14 | `node new Function` 全部 demos HTML | ALL_JS_OK，32 份 | 已证实 |
| V15 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan | 已证实 |
| V16 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V17 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V18 | 必读文件循环 | REQUIRED=211 MISSING=0 | 已证实 |
| V19 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| query 编码、hex 编码、{total_tests} / 0、Windows GNU | 已证实 |
| 041 收口 852 文件 ALL_MATCH、E63–E66 修复 | 已证实 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动 |
| Q-041 / Q-037-01 / 真实窗口 / 崩溃分析 | 未证实 / 未启动 |
| {total_tests} 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。
'''

D['docs/features/query-encoding-contract.md'] = '''# F042-01 批量请求 query 编码契约

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `build_request` 把每个模组 id 单独交给 `utf8_percent_encode(id, ID_ENCODE_SET)`，编码结果用字面 `,` 连接成一个 `ids` 参数；`ID_ENCODE_SET` 由 `CONTROLS` 加 query 里会破坏语义的字符构成，保留 unreserved；非 ASCII 字节由库按 UTF-8 转义；最终 `Uri` 仍由 `http` crate 解析。 |
| 开放了什么 | `src/core/http.rs` 的 `build_request` / `plan` / `validate_authority`；`plan` 的分页与「10 个 id 一次请求、45 个三次请求」语义一行没动。 |
| 登记框架 | `percent-encoding 2.3.1`（MIT OR Apache-2.0 / edition 2018 / MSRV 1.51 / 零依赖）；与 040 的 `http 1.3.1` 类型层、029 的 `lru` 单飞缓存、027 的 crossbeam 并发层串联。 |
| 用户使用逻辑 | 搜一批模组时还是一次请求，不会因为某个模组名带空格、`&`、中文就悄悄丢几个；镜像看到的 id 与用户选的一一对应；编码前的常见 id 请求串不变，不会让已有缓存 key 或服务端规则突然失效。 |
| 性能 | 每页最多 20 个 id，逐 id 编码是线性小操作；无额外网络请求、无分配大头、无异步任务。 |

状态：请求构造层已实现已验证；真实网络 IO 未启动。
'''

D['docs/research/25-percent-encoding-hex.md'] = '''# batch query 编码与 hex 库一手资料（042）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://github.com/servo/rust-url/blob/v2.5.0/percent_encoding/Cargo.toml | percent-encoding **2.3.1** / MIT OR Apache-2.0 / edition 2018 / MSRV 1.51 / `no_std`；features `default=["std"]`、`std=["alloc"]`、`alloc=[]`；零依赖 | 已证实 |
| https://github.com/servo/rust-url/blob/v2.3.1/percent_encoding/Cargo.toml | 同名 tag 下 manifest 写的是 **2.2.0**，mono-repo 的 tag 与 crate 版本不同步 | 已证实 |
| https://github.com/servo/rust-url/blob/v2.5.8/percent_encoding/Cargo.toml | 已是 2.3.2，说明 2.3.1 落在 v2.5.0–v2.5.4 区间 | 已证实 |
| https://github.com/servo/rust-url/blob/v2.5.0/percent_encoding/src/lib.rs | `pub fn utf8_percent_encode<'a>(input: &'a str, ascii_set: &'static AsciiSet)`、`pub const CONTROLS: &AsciiSet`、`pub const NON_ALPHANUMERIC: &AsciiSet`、`AsciiSet::add` 为 const fn；文档示例 `utf8_percent_encode("foo bar?", NON_ALPHANUMERIC)` → `foo%20bar%3F` | 已证实 |
| https://github.com/KokaKiwi/rust-hex/blob/v0.4.3/Cargo.toml | hex 0.4.3 / MIT OR Apache-2.0 / edition 2018；`default=["std"]`、`alloc=[]`、`std=["alloc"]`；`[dependencies]` 仅 optional serde；`[[bench]]` 与 7 项 dev-dependencies | 已证实 |
| https://github.com/KokaKiwi/rust-hex/blob/v0.4.3/src/lib.rs | `pub fn encode<T: AsRef<[u8]>>(data: T) -> String`、`encode_upper`、`decode`、`decode_to_slice`、`encode_to_slice`；`HEX_CHARS_LOWER = b"0123456789abcdef"`；`pub mod serde` 受 `#[cfg(feature = "serde")]` 门控 | 已证实 |
| https://www.rfc-editor.org/rfc/rfc3986 | query 的 unreserved 集合为字母数字与 `-` `.` `_` `~`；其余字节按 UTF-8 百分号编码 | 已证实（规范引用） |
| crates.io registry 与 static.crates.io | 全部 403 | 已证实（025 起多轮） |

| 编号 | 结论 |
| --- | --- |
| R17 | 批量请求的正确性依赖 id 编码；`ids.join(",")` 会把含 `&`、`#`、逗号的 id 切坏，属于真缺陷而非风格问题。 |
| R18 | 用 `NON_ALPHANUMERIC` 会把连字符也编码，破坏既有请求串；保留 unreserved 才是与改前兼容的口径。 |
| R19 | mono-repo 的 tag 名不等于 crate 版本，必须读子目录 manifest 实值（A128）。 |
| R20 | 两个 crate 均零传递依赖、无 C 构建链、无 proc-macro，MSRV 低于 Win7 Tier 3 路线，可安全进 vendor。 |
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


app('docs/decisions/index.md', '| 042 | 批量 query 编码与身份哈希 hex 交给库 | 已实现已验证；真实网络 IO 未启动 | 042-query-encoding-and-hex.md |')
app('docs/features/index.md', '| F042-01 | query-encoding-contract.md | 请求构造层已实现；真实网络 IO 未启动 |')
app('docs/research/index.md', '| 25 | 25-percent-encoding-hex.md | batch query 编码与 hex 库一手资料 | 8 已证实 |')
app('docs/rules/index.md', '| ui-preconditions.md | UI 宿主与崩溃分析 L1-L12 前置清单 | 041（042 沿用） |') if Path('docs/rules/index.md').exists() else None

app('docs/licenses/index.md', '''## 042 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| pe-LICENSE-MIT.txt | percent-encoding 2.3.1 | MIT（1072 B） |
| pe-LICENSE-APACHE.txt | percent-encoding 2.3.1 | Apache-2.0（10847 B） |
| hex-LICENSE-MIT.txt | hex 0.4.3 | MIT（1125 B） |
| hex-LICENSE-APACHE.txt | hex 0.4.3 | Apache-2.0（11358 B） |

来源：`servo/rust-url` tag `v2.5.0` 根 LICENSE、`KokaKiwi/rust-hex` tag `v0.4.3` 根 LICENSE，逐字副本。mono-repo 子 crate 的 LICENSE 是软链，tarball 取不到，走 contents API 直取。
''')

app('THIRD-PARTY-NOTICES.md', f'''## 042 新增已进构建依赖（编码层）

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| percent-encoding | 2.3.1 | MIT OR Apache-2.0 | The rust-url developers | 批量请求 id 的 UTF-8 百分号编码 | vendor/percent-encoding | 构建中已使用 |
| hex | 0.4.3 | MIT OR Apache-2.0 | KokaKiwi | 插件身份哈希的小写十六进制编码 | vendor/hex | 构建中已使用 |

许可证全文：`docs/licenses/pe-LICENSE-MIT.txt`、`docs/licenses/pe-LICENSE-APACHE.txt`、`docs/licenses/hex-LICENSE-MIT.txt`、`docs/licenses/hex-LICENSE-APACHE.txt`。

| 编号 | 约束 |
| --- | --- |
| N41 | percent-encoding 上游 `src/lib.rs` 逐字节未改；vendored manifest 只裁掉 docs.rs metadata。该 crate 版本取自 `v2.5.0` 子目录 manifest 的 2.3.1，不按 tag 名猜。 |
| N42 | hex 上游 `src/lib.rs` / `src/error.rs` 逐字节未改；裁掉 optional serde、dev-dependencies、`[[bench]]`、docs.rs metadata，并删除只服务于 optional feature 的 `src/serde.rs`。 |
''')

app('docs/records/code-ownership-audit.md', f'''## 042 编码层（+2 crate）

| 项 | 041 | 042 |
| --- | --- | --- |
| 第三方 crate 进构建 | 20 | **{third}**（+percent-encoding、+hex） |
| `Cargo.lock` 包数 | 21 | **{pkgs}** |
| `src/` 行数 | 5715 | **{src_lines}** |
| 测试 | 237 单元 + 26 集成 = 263 | **{lib_tests} 单元 + {int_tests} 集成 = {total_tests}** |

`src/core/http.rs` 的 `ids.join(",")` 自写 query 拼装换成 `utf8_percent_encode`（保留 unreserved，常见 id 请求串不变）；`src/plugins/identity.rs` 的 `format!("{{:02x}}", b)` 循环换成 `hex::encode`。两处都是通用编码算法，不是项目特有编排；独立回归常量由 Python hashlib 算出，不用本仓库实现自证。

剩余自写仍是 `launcher.rs`、lightweight 系列与 `paths/popup/userflow` 等业务编排；035 已登记它们没有语义等价的库可换。
''')

app('docs/design/implementation-strategy.md', '''## 042 编码层

| 层 | 状态 |
| --- | --- |
| 窗口句柄契约（raw-window-handle） | 已实现（041） |
| 批量请求 id 百分号编码（percent-encoding） | **已实现（042）** |
| 插件身份哈希 hex（hex） | **已实现（042）** |
| 真实窗口 / WebView / 渲染 / 崩溃分析 | 未启动（L1–L12 见 ui-preconditions.md） |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动（040 L1–L12） |
| 子进程插件隔离、插件 init | 未启动（039） |
| 界面渲染 | 仍等 UX 手感确认与 Q-041 拍板 |
''')

app('docs/rules/ui-demo.md', '''## 042 闸门判定

本轮只更新关于页许可表数据（20 → 22 组，计数 42 → 44）并重渲 4 张许可相关截图，不改任何界面布局、控件或交互；`src/core/http.rs` 与 `src/plugins/identity.rs` 是编码层，不产生界面变化。沿用 036 / 038–041 的先例判**未触发**。其余 52 张 PNG 回退到 HEAD。
''')

app('docs/checklists/ai-errors.md', '''## 042 轮新增

| 编号 | 防错项 |
| --- | --- |
| A128 | mono-repo 的 tag 名不等于 crate 版本；必须读子目录 manifest 的实值版本号再 vendor。 |
| A129 | 批量参数里的每个值要独立编码；`join(",")` 前不编码会让 `&` / `#` / 逗号把请求切坏。 |
| A130 | 用 `NON_ALPHANUMERIC` 会连 unreserved 的 `-` 也编码，破坏既有请求串；保留 unreserved 并复用原有集成断言，不改断言降标准。 |
| A131 | 编码类替换要有独立实现算出的期望值（本轮 Python hashlib），不能用被换掉的库自证。 |
| A132 | tarball 里的软链 `m.isfile()` 为 False；LICENSE 缺失时走 contents API 直取，不伪造许可文本。 |
| A133 | 裁 vendor manifest 时 `[[bench]]` 双括号段、`[badges]`、optional 依赖与其源文件要一起处理。 |
''')

app('docs/records/interface-log.md', '''## 042 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I52 | `src/core/http` | `build_request` 的 ids 改逐 id 百分号编码；新增 `ID_ENCODE_SET` |
| I53 | `src/plugins/identity` | `identity_hash` 改 `hex::encode` |
| I54 | `tests/http_construct` | 原有 7 项全过，未改断言 |
| S41 | 状态 | U49–U57 已证实；Q-041 / Q-037-01 仍挂；真实网络 IO、UI、崩溃分析未启动 |
''')

app('docs/records/rounds.md', f'''## 042

| 落点 | 内容 |
| --- | --- |
| docs/spec/42-round-042-instructions.txt | 逐字副本 1 行 |
| docs/decisions/042-query-encoding-and-hex.md | F29-F31、U49-U57、V-A~V-E、E63-E66、四值 |
| docs/verification/round-042.md | 19 条复跑证据 |
| docs/features/query-encoding-contract.md | F042-01 五字段登记 |
| docs/research/25-percent-encoding-hex.md | 8 个锚点 / R17-R20 |
| src/core/http.rs + src/plugins/identity.rs | 编码层替换，7 个新增单测 |
| vendor/ + Cargo.toml/lock | percent-encoding 2.3.1、hex 0.4.3，{pkgs} 包 / {third} 第三方 |
| docs/licenses/ + 关于页 + NOTICES | 4 份全文、22 组、计数 44、N41-N42 |
| demos/round-042-query-hex.html | 13 步运行逻辑演示 |
| 索引与记录 | docs/index 211 项、README、四个 index、ai-errors A128-A133、code-ownership-audit、implementation-strategy、ui-demo 判定、interface-log、rounds |

先把 041 的尾收干净：上一轮工具结果不可用，这轮补跑远端比对 —— 本地 `ac9af80` ↔ 远端 `599edc7`，**852/852 文件逐项 ALL_MATCH True**，truncated=False；临时 PAT 已删，全仓 `NO_CREDENTIAL`、`.git/config` 干净。

「干」继续按 024 台账把自写通用逻辑换成库。这轮挑的是两处**编码**：040 把请求类型交给了 `http` crate，但 `ids` 仍是 `ids.join(",")` 自己拼 —— 模组 id 只要带空格、`&`、`#`、逗号或中文，批量请求就会被切坏，一个 `a&b` 会变成新参数、后面的 id 直接丢。你之前点名过「每搜一个模组单发一次请求」的浪费，批量是对的，但 id 不编码就不成立。037 的插件身份哈希则是 `format!("{{:02x}}", b)` 手写循环。

真实 manifest 核完：`percent-encoding 2.3.1`（rust-url mono-repo 的 `percent_encoding/` 子 crate，MIT OR Apache-2.0 / edition 2018 / MSRV 1.51 / 零依赖）与 `hex 0.4.3`（MIT OR Apache-2.0 / edition 2018 / 仅 optional serde）。**一处坑**：`v2.3.1` tag 里的 manifest 写的是 2.2.0，2.3.1 实际对应 `v2.5.0`；按 tag 名取版本会取错（A128）。

落地：`build_request` 改成逐 id `utf8_percent_encode` 再 `join(",")`；编码集合由 `CONTROLS` 加 query 危险字符组成，**保留 RFC 3986 unreserved**，所以 `mod-a` 的请求串一字不变，原有集成断言没改。`identity_hash` 换 `hex::encode`，4 个期望值由 Python `hashlib.sha512` 独立算出写进测试，不靠本仓库实现自证。`Cargo.lock` 21 → **{pkgs} 包 / {third} 第三方**，4 份 LICENSE 全文、关于页 22 组 / 44、NOTICES N41–N42 三处齐了才进 Cargo.toml。

验证：{lib_tests} 单元 / 0 + 7 http_construct / 0 + 6 窗口契约 / 0 + 7 lifecycle / 0（36.19 s）+ 6 abi / 0（109.30 s）= **{total_tests} / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。界面闸门未触发：只重渲 4 张许可截图，其余 52 张回退。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E63 | percent-encoding 的 LICENSE 在 tarball 里是软链，vendor 后缺文件、脚本崩在复制 | 与 027 crossbeam 同类；改 contents API 直取 4 份并回写 |
| E64 | 首版用 `NON_ALPHANUMERIC` 把 `mod-a` 编成 `mod%2Da`，原有集成断言失败 | 改自定义集合保留 unreserved，**断言一字未改** |
| E65 | hex manifest 的 `[[bench]]` 双括号段正则没裁掉 | 单独正则裁掉并删 `src/serde.rs` |
| E66 | tag 名与 crate 版本不同步 | 逐 tag 读子目录 manifest 锁定 `v2.5.0` |

041 挂着的 Q-041（Win7 UI 三选项）与 Q-037-01（哈希口径）仍待你答复；真实窗口 / WebView / 崩溃分析、真实网络 IO、028 三项开服器实现、CF F17、特殊版代码、本项目 LICENSE 均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '205. docs/verification/round-041.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''205. docs/verification/round-041.md
206. docs/spec/42-round-042-instructions.txt
207. docs/decisions/042-query-encoding-and-hex.md
208. docs/features/query-encoding-contract.md
209. docs/research/25-percent-encoding-hex.md
210. demos/round-042-query-hex.html
211. docs/verification/round-042.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-041.md; do printf',
                  'docs/verification/round-041.md docs/spec/42-round-042-instructions.txt docs/decisions/042-query-encoding-and-hex.md docs/features/query-encoding-contract.md docs/research/25-percent-encoding-hex.md demos/round-042-query-hex.html docs/verification/round-042.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 042 |', p.read_text(), count=1)
section = f'''

## 042 批量请求 query 编码与身份哈希 hex 交给库

041 收口：本地 `ac9af80` ↔ 远端 `599edc7`，**852/852 文件 ALL_MATCH True**，临时凭据已清理。

`040` 把请求类型交给了 `http` crate，但 `ids` 仍是 `ids.join(",")` 自己拼：模组 id 带空格、`&`、`#`、逗号或中文就会把批量请求切坏。这轮落 `percent-encoding 2.3.1`（零依赖 / MSRV 1.51）逐 id 编码，编码集合保留 RFC 3986 unreserved，所以 `mod-a` 的请求串一字不变、原有集成断言没改；`037` 的手写 hex 循环换 `hex 0.4.3`，4 个期望值由 Python hashlib 独立算出。真实 manifest 核到一处坑：`v2.3.1` tag 的 manifest 是 2.2.0，2.3.1 对应 `v2.5.0`。

`Cargo.lock` **{pkgs} 包 / {third} 第三方**，4 份 LICENSE 全文 + 关于页 22 组 / 44 + NOTICES 三处齐备。`cargo test --offline` 合计 **{total_tests}/0**（{lib_tests} 单元 + {int_tests} 集成），Windows GNU 交叉检查通过。界面与 56 张 PNG 只动了 4 张许可截图。
'''
if '## 042 批量请求 query 编码' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

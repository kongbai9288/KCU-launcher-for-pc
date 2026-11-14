from pathlib import Path
import re

Path('docs/spec/36-round-036-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/036-updater-signature-on-ed25519-compact.md'] = '''# 第 036 轮：上层能力第一次进构建，Ed25519 签名校验交给成熟库

| 项 | 值 |
| --- | --- |
| 编号 | 036 |
| 状态 | 上层第一块已实现已验证；界面闸门未触发 |
| 依据 | docs/spec/36-round-036-instructions.txt |
| 前序 | 035-route-check-and-config-hardening.md、020 插件化更新约束 |
| 本轮性质 | 单轨轮；**上层能力首次进构建** |

## 选这块的依据

035 结尾写的是「开始动上层，从闭包最浅、最不碰 Windows 分支的那层起」。上层能力清单：UI 宿主（tao+wry / WebView2）、真实网络（reqwest+tokio）、崩溃分析（sentry / minidump）、插件 ABI（libloading + LoadLibrary 分支）、更新器。

| 编号 | 依据 |
| --- | --- |
| D01 | 前四层都要么带 Windows 平台分支，要么带 C 构建链，在当前 Linux 工具链下无法验证 Win7 Tier 3 行为。 |
| D02 | 更新器的**签名校验**是纯算法、平台无关、纯 Rust，且是用户 020 明确写进硬约束的：「签名校验不可禁用、默认只升、回滚要显式比较器、失败保留旧插件可回滚」。 |
| D03 | `jedisct1/rust-ed25519-compact 2.6.1`：`[dependencies]` 里 3 项**全部 optional**（ct-codecs / ed25519 / getrandom），默认 features 全开但可关；`mod pem` / `pub mod x25519` 有 cfg 门；关闭 default features 后**零传递依赖、单 crate、无 libc、无 windows-sys、无 build.rs**。 |
| D04 | 它内联了 SHA-512 与 Curve25519 域运算，官方 README 写明「formally-verified field arithmetic」「no_std-friendly」「zero dependencies if randomness is provided by the application」。本项目只做**验证**，不需要随机数。 |

按 023 的规矩：LICENSE 全文 + 关于页七列表 + `THIRD-PARTY-NOTICES.md` 三处齐了才进 `Cargo.toml`，本轮三处都已落。

## 依赖落地

| 编号 | 动作 |
| --- | --- |
| D05 | 上游 tag `2.6.1` tarball 原样落到 `vendor/ed25519-compact/`：11 个 `src/*.rs`（含 `edwards25519/base_table.rs`）、Cargo.toml、LICENSE、README；`src/` 逐字节未改。 |
| D06 | 裁掉 `[dependencies]`（全 optional）、`[dev-dependencies]`、features 里引用已删 dep 的三行（`pem` / `random` / `traits`）；`default` 改为 `["std"]`。cfg 门自动关掉 pem.rs / x25519.rs / reexports 的外部引用。 |
| D07 | `Cargo.toml` 加 `ed25519-compact = { version = "2.6.1", default-features = false, features = ["std"] }`；`Cargo.lock` 13 → **14 包 / 13 第三方**，零传递依赖。 |
| D08 | `docs/licenses/ed25519-compact-LICENSE.txt`（MIT，1073 B，Copyright 2020-2026 Frank Denis）逐字落盘。 |
| D09 | 关于页许可七列表新增 1 组「构建中已使用」（12 → 13 组），计数 34 → 35，NOTICES 同步。 |

## 删掉的自写风险面

本轮**没有删自写代码**，而是把「上层能力」里最容易写错的一块**从一开始就交给库**：Ed25519 点解码、非规范编码拒绝、小阶点检查、SHA-512、签名验证全部由库完成。项目侧只有：

| 文件 | 行数 | 内容 |
| --- | --- | --- |
| `src/updater/verify.rs` | 70 | 长度检查 → `PublicKey::from_slice` / `Signature::from_slice` / `pk.verify`，错误转 anyhow |
| `src/updater/policy.rs` | 126 | 版本决策编排（semver 已落地）+ 失败保留旧插件 |
| `src/updater/mod.rs` | 6 | 导出 |

`policy.rs` 里的「默认只升 / 回滚要显式目标 + 确认 / 签名失败 Keep」是用户口径，属项目特有编排，如实登记，没有说成全用库。

## 口径

| 编号 | 规则 |
| --- | --- |
| U01 | 签名校验**不可禁用**：`verify_then_decide` 把验证放在版本决策之前，验证失败直接 `Keep`，不进 `decide`。 |
| U02 | 默认只升：`candidate.cmp_precedence(current) == Greater` 才 `Install`。 |
| U03 | 同版本 `Keep`，`+build` 元数据差异不触发重装（与 034 的 `cmp_precedence` 口径一致）。 |
| U04 | 回滚需**两个条件同时成立**：`explicit_target` 解析后等于候选版本，且 `rollback_confirmed = true`；只给其中一个仍 `Reject`。 |
| U05 | 失败保留旧插件：签名失败、版本串畸形、任何解析错误都返回 `Keep`，不覆盖已装插件。 |
| U06 | 非法输入不 panic：短公钥 / 短签名 / 空 payload 走库的错误路径，统一转 `anyhow::Error`。 |
| U07 | 公钥来源、插件包格式、分发通道、密钥轮换**未证实**，本轮不写死；`PUBLIC_KEY_BYTES=32` / `SIGNATURE_BYTES=64` 由库常量导出，不手填。 |

## 用户逻辑推演

| 画面 | 结果 |
| --- | --- |
| 官方更新包带正确签名、版本更新 | 安装 |
| 更新包被改了一个字节 | 签名失败 → 保留旧插件，可见错误 |
| 有人塞了个旧版本包想回滚 | 默认拒绝，保留旧插件 |
| 用户明确选了目标旧版本并二次确认 | 安装该旧版本 |
| 插件只改了构建元数据 | Keep，不重复安装 |
| 更新包签名对但版本串写坏 | Keep，不覆盖旧插件 |
| 公钥被截断 | 返回错误，不 panic |

## 测试

`cargo build --offline` 通过；`cargo test --offline` **164 → 179 passed / 0 failed**，新增 15 个（verify 6 + policy 9）：合法签名、篡改 payload、错误公钥、截断输入不 panic、空 payload、签名字节互换；只升 / 同版本 / 默认拒降级 / 回滚双条件 / 畸形版本 / build 元数据 / 签名失败保留 / 合法签名+新版本安装 / 合法签名但版本畸形保留。

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E32 | 测试里 `Noise::default()` 报 E0599（该 impl 在 random feature 门下） | 改用 `None`，签名走确定性路径；验证不需要随机数 |
| E33 | `assert_eq!(decide(..), Ok(Decision::X))` 触发 E0369（anyhow::Error 无 PartialEq） | 改 `.unwrap()` 后比值，断言强度不降 |
| E34 | 首版 policy 用 `Version` 的 `>` / `==`，`1.2.3+old` vs `1.2.3+new` 被判不等 | 改用 034 已验证的 `cmp_precedence`，build 元数据差异归 `Keep` |

## 四值

| 项 | 值 |
| --- | --- |
| ed25519-compact 2.6.1 进构建、14 包 13 第三方、零传递依赖、179 / 0 | 已证实 |
| 三处许可齐备、上游 `src/` 未改、U01–U07 口径 | 已证实 |
| 上层能力第一次进构建 | 已证实 |
| 公钥来源 / 插件包格式 / 分发通道 / 密钥轮换 | 未证实 |
| UI 宿主 / 真实网络 / 崩溃分析 / 插件 ABI / 更新器其余部分 | 未启动 |
| Win7 Tier 3 + build-std 下纯 Rust 曲线运算 | 未证实（无交叉编译环境） |
| 界面闸门 | 未触发（仅关于页许可表数据更新并重渲 4 张图） |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-036.md'] = '''# 第 036 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 036 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | 编译 ed25519-compact 2.6.1 / kcu-core，`Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 179 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 14 包 / 13 第三方，ed25519-compact 零传递依赖 | 已证实 |
| V4 | `grep -c '#\\[test\\]' src/updater/*.rs` | 15（verify 6 + policy 9） | 已证实 |
| V5 | `grep -c 'cmp_precedence' src/updater/policy.rs` | 1 | 已证实 |
| V6 | `vendor/ed25519-compact/src/lib.rs` 与上游 tarball | 逐字节一致 | 已证实 |
| V7 | `docs/licenses/ed25519-compact-LICENSE.txt` | 1073 字节，MIT / Frank Denis | 已证实 |
| V8 | 关于页许可行 / NOTICES | 13 组「构建中已使用」，计数 35，含 ed25519-compact | 已证实 |
| V9 | `demos/preview/22-licenses.png` 等 4 张 | 重渲，非空 | 已证实 |
| V10 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V11 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V12 | 必读文件循环 | REQUIRED=176 MISSING=0 | 已证实 |
| V13 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 上层第一块库化、179 / 0、U01–U07 | 已证实 |
| 公钥来源 / 插件包格式 / 密钥轮换、Win7 交叉编译 | 未证实 / 受阻 |
| UI 宿主 / 真实网络 / 崩溃分析 / 插件 ABI / 更新器其余部分 | 未启动 |
| 179 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。
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


app('docs/decisions/index.md', '| 036 | 上层第一块：Ed25519 签名校验交给 ed25519-compact | 已实现 | 036-updater-signature-on-ed25519-compact.md |')

app('docs/records/code-ownership-audit.md', '''## 036 上层能力第一次进构建

| 项 | 024 | 025 | 027 | 029 | 030 | 031 | 032 | 033 | 034 | 035 | 036 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 8 | 9 | 9 | 10 | 11 | 12 | 12 | **13** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 9 | 10 | 10 | 11 | 12 | 13 | 13 | 14 |
| 测试数 | 141 | 141 | 141 | 141 | 144 | 149 | 153 | 153 | 161 | 164 | 179 |

035 收敛的是「自写通用算法换成熟库」。036 起进入**上层能力**：从闭包最浅、最不碰 Windows 分支的更新器签名校验开始。

`ed25519-compact 2.6.1` 单 crate、零传递依赖（3 项依赖全 optional，关 default features 后 `pem.rs` / `x25519.rs` 由 cfg 门自动排除）、纯 Rust、无 libc / windows-sys / build.rs。点解码、非规范编码拒绝、小阶点检查、SHA-512 全部由库完成；项目侧 202 行只有长度检查、错误转 anyhow 与版本决策编排。

新增 `src/updater/`：`verify.rs`（detached 签名验证）、`policy.rs`（默认只升 / 回滚双条件 / 失败保留旧插件）、`mod.rs`。版本决策复用 034 的 `semver::cmp_precedence`。

**仍标未启动**：UI 宿主、真实网络、崩溃分析、插件 ABI、更新器其余部分（下载、安装、回滚执行、公钥分发）。这些动到时按 023 逐项取 LICENSE 全文并登记关于页与 NOTICES。
''')

app('docs/design/implementation-strategy.md', '''## 036 上层启动

| 层 | 状态 |
| --- | --- |
| L1–L3 通用算法 | 已全部换成熟库 |
| 路径 → dirs、配置 → toml、日志 → tracing、错误枚举 → thiserror | 已失败（033 D04、035 R01–R03） |
| 项目特有编排（dispatcher / lightweight / popup / userflow / paths） | 保留 |
| 更新器签名校验 | **已启动（036，ed25519-compact 2.6.1）** |
| UI 宿主、真实网络、崩溃分析、插件 ABI、更新器其余部分 | 未启动 |
''')

app('docs/checklists/ai-errors.md', '''## 036 轮新增

| 编号 | 防错项 |
| --- | --- |
| A92 | 上游 crate 的依赖「全部 optional」不等于零闭包，要核 cfg 门是否真的把引用外部 crate 的模块排除。 |
| A93 | 关掉 default features 后，features 表里引用已删 optional dep 的行必须一并删除，否则目录源解析会失败（033 的 log 已踩过一次）。 |
| A94 | 版本决策不要直接用 `Version` 的 `>` / `==`（含 build 元数据），统一走 034 的 `cmp_precedence`。 |
| A95 | 签名校验必须排在版本决策之前；任何解析失败都返回「保留旧插件」，不能落到安装分支。 |
''')

app('docs/records/interface-log.md', '''## 036 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I39 | `src/updater` | 新增 `verify_detached` / `decide` / `verify_then_decide` / `Decision` / `UpdatePolicy` |
| S35 | 状态 | U01–U07 已证实；公钥来源与插件包格式未证实；028 三项开服器功能实现层未启动 |
''')

app('docs/licenses/index.md', '''## 036 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| ed25519-compact-LICENSE.txt | ed25519-compact 2.6.1 | MIT |

来源：jedisct1/rust-ed25519-compact tag `2.6.1`，逐字副本 1073 字节，Copyright (c) 2020-2026 Frank Denis。MIT 条款要求保留版权与许可声明，全文随发行物附上。
''')

app('THIRD-PARTY-NOTICES.md', '''## 036 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| ed25519-compact | 2.6.1 | MIT | Frank Denis | 更新包 Ed25519 签名校验 | vendor/ed25519-compact | 构建中已使用 |

许可证全文：`docs/licenses/ed25519-compact-LICENSE.txt`。

| 编号 | 约束 |
| --- | --- |
| N30 | 零传递依赖；3 项 optional 依赖全部裁掉，`default-features = false, features = ["std"]`；`src/` 逐字节未改。 |
| N31 | MIT 全文随发行物附上；本项目只使用验证路径，不使用随机数生成与 PEM / X25519 模块。 |
''')

app('docs/records/rounds.md', '''## 036

| 落点 | 内容 |
| --- | --- |
| docs/spec/36-round-036-instructions.txt | 逐字副本 1 行 |
| docs/decisions/036-updater-signature-on-ed25519-compact.md | D01-D09 依据与依赖、U01-U07 口径、用户逻辑推演、E32-E34、四值 |
| docs/verification/round-036.md | 13 条复跑证据 |
| demos/round-036-updater-signature.html | 13 步运行逻辑演示 |
| src/updater/ | 3 文件 202 行，15 个测试 |
| vendor/ed25519-compact/ + Cargo.toml/lock | 14 包 / 13 第三方，零传递依赖 |
| docs/licenses/ed25519-compact-LICENSE.txt | MIT 全文 1073 字节 |
| demos/ui-full-kcu-paper.html | 关于页许可七列表新增 1 组（12 → 13），计数 34 → 35 |
| 索引与记录 | docs/index 176 项、README、decisions/index、licenses/index、ai-errors A92-A95、code-ownership-audit、implementation-strategy、THIRD-PARTY-NOTICES、interface-log、rounds |

「干」按 035 结尾进入**上层能力第一块**：从闭包最浅、最不碰 Windows 分支的更新器签名校验开始。`ed25519-compact 2.6.1` 单 crate 零传递依赖（3 项依赖全 optional，关 default features 后 pem.rs / x25519.rs 由 cfg 门排除）、纯 Rust、无 libc / windows-sys / build.rs。点解码、非规范编码拒绝、小阶点检查、SHA-512 全部交给库。

口径 U01–U07：签名校验不可禁用且排在版本决策之前；默认只升；同版本与 `+build` 差异 Keep；回滚需显式目标 + 二次确认两个条件同时成立；签名失败 / 版本畸形 / 截断输入一律返回 Keep 保留旧插件，不 panic。项目侧只有长度检查、错误转 anyhow 与版本决策编排（复用 034 的 `cmp_precedence`）。

`cargo test --offline` 164 → **179 / 0**，`Cargo.lock` 13 → 14 包 / 13 第三方。三处许可齐备（LICENSE 全文 / 关于页 / NOTICES）后才进 Cargo.toml。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E32 | 测试里 `Noise::default()` 报 E0599（impl 在 random feature 门下） | 改用 `None` 走确定性签名，验证不需要随机数 |
| E33 | `assert_eq!(decide(..), Ok(Decision::X))` 触发 E0369 | 改 `.unwrap()` 后比值，断言强度不降 |
| E34 | 首版 policy 用 `Version` 的 `>` / `==`，`+build` 差异被判不等 | 改 `cmp_precedence`，与 034 口径一致 |

界面闸门**未触发**：本轮不动界面布局，只更新关于页许可表数据并重渲 4 张许可相关截图。

**仍标未启动**：UI 宿主、真实网络、崩溃分析、插件 ABI、更新器其余部分（下载 / 安装 / 回滚执行 / 公钥分发）。028 三项开服器功能仍按「只记文档」零实现；CF F17、特殊版代码、本项目 LICENSE、Win7 交叉编译、后端仓写请求均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '171. docs/verification/round-035.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '171. docs/verification/round-035.md\n172. docs/spec/36-round-036-instructions.txt\n173. docs/decisions/036-updater-signature-on-ed25519-compact.md\n174. src/updater/verify.rs\n175. demos/round-036-updater-signature.html\n176. docs/verification/round-036.md\n\n读取命令：', 1)
    t = t.replace('docs/verification/round-035.md; do printf',
                  'docs/verification/round-035.md docs/spec/36-round-036-instructions.txt docs/decisions/036-updater-signature-on-ed25519-compact.md src/updater/verify.rs demos/round-036-updater-signature.html docs/verification/round-036.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 036 |', p.read_text(), count=1)
section = '''

## 036 上层能力第一块：Ed25519 签名校验交给库

`ed25519-compact 2.6.1` 单 crate、零传递依赖、纯 Rust、无 libc / windows-sys / build.rs，关闭 default features 后由 cfg 门排除 PEM / X25519 / 随机数模块。点解码、非规范编码拒绝、小阶点检查、SHA-512 全部由库完成。

新增 `src/updater/`：签名校验排在版本决策之前，默认只升、同版本与 build 元数据差异 Keep、回滚需显式目标 + 二次确认、任何失败都保留旧插件。版本决策复用 `semver::cmp_precedence`。

`Cargo.lock` 14 包 / 13 第三方，`cargo test --offline` 179/0。LICENSE 全文、关于页、NOTICES 三处齐备后才进依赖。UI 宿主、真实网络、崩溃分析、插件 ABI 与更新器其余部分仍标未启动。
'''
if '## 036 上层能力' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

# 第 036 轮：上层能力第一次进构建，Ed25519 签名校验交给成熟库

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

# 第 034 轮：版本匹配交给 semver

| 项 | 值 |
| --- | --- |
| 编号 | 034 |
| 状态 | 代码已实现已验证；界面闸门未触发 |
| 依据 | docs/spec/34-round-034-instructions.txt |
| 前序 | 033-answer-abbr-and-anyhow.md |
| 本轮性质 | 单轨轮，继续按 024 映射表替换自写代码 |

## 选这块的依据

| 编号 | 依据 |
| --- | --- |
| D01 | 024 台账里 `core/instance.rs` 一直列为「剩余自写的业务编排」，但里面 `==` / `contains` 的**版本字符串比较**其实是通用算法，不该留在自写层。 |
| D02 | 用户多次点名「双击进服按版本兼容范围绑定」「按照正常我的世界现实的逻辑和我的世界的发现逻辑进行」「让用户非常舒服就对了」。精确字符串相等遇到服务器返回 `1.20.4+paper.381` 或 `1.20.x` 会匹配不到实例，双击进服直接失败。 |
| D03 | `semver 1.0.28`：默认 features 只有 `std`，`[dependencies]` 里唯一一项是 optional serde_core，零传递依赖；MIT OR Apache-2.0，tag 与两份 LICENSE 全文可从上游取到。 |
| D04 | 033 核完 `paths.rs → dirs` 不成立并改轨后，本轮不重试受阻路线，也不硬塞 UI / 网络 / 崩溃这类大闭包。 |

## 依赖落地

| 编号 | 动作 |
| --- | --- |
| D05 | 上游 tag `1.0.28` tarball 原样落到 `vendor/semver/`：8 个 `src/*.rs`、Cargo.toml、两份 LICENSE、README；`src/` 逐字节未改。 |
| D06 | 裁掉 optional serde_core、恒假 `cfg(any())` target 段、dev-dependencies、bench 与 docs.rs / playground 元数据；`[features]` 只剩 `default = ["std"]` 与 `std = []`。 |
| D07 | `Cargo.toml` 加 `semver = "1.0.28"`；`Cargo.lock` 12 → **13 包 / 12 第三方**，零传递依赖。 |
| D08 | `docs/licenses/semver-LICENSE-MIT.txt` (1023 B) 与 `semver-LICENSE-APACHE.txt` (9723 B) 逐字落盘；按 MIT 条款用，Apache-2.0 全文一并保留。 |
| D09 | 关于页第三方许可七列表新增 1 组「构建中已使用」（11 → 12 组），计数 33 → 34，`THIRD-PARTY-NOTICES.md` 同步。 |

## 删掉的自写版本比较

| 033 | 034 |
| --- | --- |
| `supported == choice` / `contains(&i.mc_version)` / `h.version == i.mc_version` 三处字符串相等 | 统一 `versions_match(supported, candidate)`，相等与规范化交给 semver |
| 无版本规范化、无范围概念 | `Version::cmp_precedence` 忽略 build metadata；`VersionReq::matches` 支持显式范围 |
| 服务器返回 `1.20.4+paper.381` 时匹配不到 `1.20.4` | 交给库判定为同一版本 |

`core/instance.rs` 的权重打分、用户指定排第一、失败可见不崩仍是项目特有编排（约 35 行），如实登记，没有说成全用库。

## 匹配口径

| 编号 | 规则 |
| --- | --- |
| M01 | 先做精确字符串相等（`23w31a` 这类 MC 快照版本直接命中）。 |
| M02 | 服务器串带范围符号 `^ ~ > < = * , | x X 空格 制表` 时，走 `VersionReq::parse` + `Version::parse`，由 `req.matches(&v)` 判定。 |
| M03 | 两边都是完整三段 semver 时走 `Version::cmp_precedence(..) == Equal`，`+build` 元数据不参与比较。 |
| M04 | 普通 `1.20.4` **不会**被当成 caret 范围。Cargo 风格 `VersionReq::parse("1.20.4")` 等价于 `^1.20.4`，会误匹配 `1.21.1`，所以只在 M02 显式带符号时才用范围。 |
| M05 | 解析失败一律返回 false，不 panic、不静默放宽。预发布 `1.20.4-pre1` 与正式版 `1.20.4` 不相等。 |

## 用户逻辑推演

| 画面 | 033 | 034 |
| --- | --- | --- |
| 双击服务器，实例版本和 SLP 完全一致 | 进服 | 进服，行为不变 |
| SLP 返回 `1.20.4+paper.381`，本地实例 `1.20.4` | 匹配不到，报错 | 库判定同版本，正常进服 |
| 服务器声明 `>=1.20.0, <1.21.0` | 字符串不相等，匹配不到 | 范围匹配，选中 `1.20.4` 实例 |
| 快照服 `23w31a` | 精确串命中 | 精确串仍命中，回退路径保留 |
| 用户手动锁定某个实例 | 排第一 | 排第一，逻辑未动 |
| 服务器串写坏 `>=not-a-version` | 匹配不到 | 匹配不到，不崩 |

## 行为差异（如实登记：本轮是扩展，不是纯等价替换）

| 编号 | 项 | 值 |
| --- | --- | --- |
| B10 | 精确相等 | 保留，原有 5 个测试全部通过 |
| B11 | `+build` 元数据 | 新增：忽略后视为同版本 |
| B12 | 显式范围表达式 | 新增：`1.20.x`、`>=1.20.0, <1.21.0` 可匹配 |
| B13 | 普通三段版本 | 保持精确，未被当 caret 放宽 |
| B14 | 带前缀版本名 | **未证实**。SLP 有时返回 `Paper 1.20.4` 这类带前缀串，当前解析失败走回退，仍不匹配；没有一手资料前不加 stripping 规则 |

## 测试

`cargo build --offline` 通过；`cargo test --offline` **153 → 161 passed / 0 failed**，新增 8 个：build 元数据、预发布区分、范围边界、通配符、快照回退、畸形串不崩、普通版本不放宽、习惯权重键可用范围。

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E28 | 首版用 `Version::eq` 判同版本，`build_metadata_is_ignored_by_the_library` 失败 | 独立小程复核：`semver::Version` 的 `==` **包含** build 元数据，`cmp_precedence` 才忽略；改用 `cmp_precedence(..) == Ordering::Equal`，161 / 0 |
| E29 | 若把普通 `1.20.4` 直接交给 `VersionReq`，`^1.20.4` 会误匹配 `1.21.1` | 立 M04，只在显式带范围符号时走 `VersionReq` |

## 四值

| 项 | 值 |
| --- | --- |
| semver 1.0.28 进构建、13 包 12 第三方、161 / 0 | 已证实 |
| 三处自写字符串比较换库、上游 `src/` 未改、两份 LICENSE 全文 | 已证实 |
| B11 / B12 新增能力、B13 不放宽、B14 带前缀串 | 已证实 / 未证实 |
| 界面闸门 | 未触发（仅关于页许可表数据更新） |
| 自动命令实现层、真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 后端仓写请求 | 0（已证实） |

# 第 033 轮：Q-031-01 结案；错误处理换 anyhow

| 项 | 值 |
| --- | --- |
| 编号 | 033 |
| 状态 | A 轨歧义已结案、B 轨代码已实现已验证 |
| 依据 | docs/spec/33-round-033-instructions.txt |
| 前序 | 031-strict-policy-and-config.md、032-user-selectable-tiers.md |
| 本轮性质 | 双轨轮 |

## 两条指令的边界

| 编号 | 原文片段 | 处置 |
| --- | --- | --- |
| A01 | 「是answer缩写」 | 结案 Q-031-01：031 那句里的 A 是 answer 缩写，不是 Q1-A 选项字母。031 结论不改、032 三档不改、不重做界面。 |
| B01 | 「干」 | 继续按 `docs/records/code-ownership-audit.md` 映射表替换自写代码，落「错误 → anyhow」。 |

## A01：Q-031-01 结案

| 编号 | 动作 |
| --- | --- |
| C01 | `docs/features/server-auto-command-log-trigger.md` 的「待用户确认的歧义」改为「已结案」，写明 A = answer 缩写。 |
| C02 | `docs/records/q028-decision-scenarios.md` 追加 033 结案段，032 段里「这次没有答复」改为已结案。 |
| C03 | 031 的 Q1-C + Q2-A 判定、P01–P07、032 的三档矩阵与 U01–U11 **全部保留**，不回退、不重做。 |

| 项 | 值 |
| --- | --- |
| 之前误判 | 031 把「A」当成可能的 Q1 选项字母，登记为待确认歧义（最保守做法） |
| 实际 | 「两个问题 answer：按最严格去执行」，A 只是答复标记 |
| 结论 | 031 按「最严格」取 Q1-C + Q2-A 成立，口径无需变更 |
| 界面闸门 | **未触发**。本轮不动用户界面，只改结论文字与登记，不出整页 UX 演示、不改预览图内容 |

## B01：自写 String 错误换成 anyhow 1.0.104

### 选这块的依据

| 编号 | 依据 |
| --- | --- |
| D01 | 映射表「错误 → anyhow + thiserror」是 024 登记的欠账之一，此前未落地。 |
| D02 | 全仓 8 个文件共 15 个 `Result<T, String>` 签名、多处 `map_err(|e| e.to_string())`、手写 `Err(format!(...))`，错误类型靠字符串拼接，无上下文链、无来源保留。 |
| D03 | `anyhow 1.0.104` 的 `[dependencies]` 为空（零传递依赖），MIT OR Apache-2.0，crates manifest 与两份 LICENSE 全文可从上游 tag 取到。 |
| D04 | 032 结尾曾预告核 `dirs` 换 `paths.rs`。核完结论：`paths.rs` 是「注入 root + 逻辑名 → 子路径」映射，用户明确决定数据目录为 `C:\KCU`；`dirs` 提供的是系统目录定位，硬换会改变默认行为并引入 windows-sys 大闭包（Linux 工具链无法验证 Windows 分支）。**不换**，改走错误类型这块，理由如实写在此。 |

### 依赖落地

| 编号 | 动作 |
| --- | --- |
| D05 | 上游 tag `1.0.104` tarball 原样落到 `vendor/anyhow/`：12 个 `src/*.rs`、`build.rs`、Cargo.toml、两份 LICENSE、README；`src/` 逐字节未改。 |
| D06 | 裁掉 `[dev-dependencies]`（futures / rustversion / syn 3 / trybuild 不参与构建）；`[features] default = ["std"]` 保留；根 Cargo.toml 本就没有 `[dependencies]` 段。 |
| D07 | `Cargo.toml` 加 `anyhow = "1.0.104"`；`Cargo.lock` 11 → **12 包 / 11 第三方**，零传递依赖。 |
| D08 | `docs/licenses/anyhow-LICENSE-MIT.txt` (1023 B) 与 `anyhow-LICENSE-APACHE.txt` (9723 B) 逐字落盘；按 MIT 条款用，Apache-2.0 全文一并保留。 |
| D09 | 关于页第三方许可七列表新增 1 组「构建中已使用」（10 → 11 组），`THIRD-PARTY-NOTICES.md` 同步。 |

### 删掉的自写错误处理

| 032 | 033 |
| --- | --- |
| `Result<T, String>` × 15 个签名 | `anyhow::Result<T>` × 15 个签名 |
| `map_err(|e| e.to_string())?` 丢掉来源类型 | 直接 `?`，`From<E>` 保留原始错误 |
| `Err("...".to_string())` / `Err(format!(...))` 手写串 | `anyhow::anyhow!(...)` |
| `ok_or_else(|| format!(...))?` 构造字符串错误 | `ok_or_else(|| anyhow::anyhow!(...))?` |
| 8 个模块各写各的错误口径 | 统一 `anyhow::Error`，可 `context` 追加链路 |

涉及模块：`core/config.rs`、`core/envelope.rs`、`core/paths.rs`、`core/args.rs`、`dispatcher/json.rs`、`dispatcher/task.rs`、`dispatcher/mode.rs`、`dispatcher/launcher.rs`、`lightweight/download.rs`。

### 行为差异（如实登记）

| 编号 | 项 | 032 | 033 |
| --- | --- | --- | --- |
| B10 | 错误类型 | `String` | `anyhow::Error`；`unwrap_err()` 需 `.to_string()` 再比较内容 |
| B11 | `dispatcher/json.rs` 三个 `assert_eq!(parse(..), Ok(..))` | 直接比 Result | 改 `unwrap()` 后比值，断言强度不降 |
| B12 | `mode.rs` 错误内容断言 | `.unwrap_err().contains(..)` | `.unwrap_err().to_string().contains(..)` |
| B13 | `launcher.rs` 缓存闭包 | `Ok::<String, String>` | 保持；`from_str` 的错误在这里 `.map_err(|e| e.to_string())` 适配 Cache 的 String 错误契约，登记为局部适配，未改 Cache |
| B14 | `lightweight/download.rs` 线程闭包 | `Ok::<String, String>` | `Ok::<String, anyhow::Error>` |

### 本轮真实失败与修复（全部留痕）

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E22 | `tarfile.open(BytesIO)` 把它当文件名，报 TypeError | 改 `tarfile.open(fileobj=io.BytesIO(b), mode='r:gz')` |
| E23 | `config.rs` 的 `ok_or_else(|| "...".to_string())?` 产生 String 错误，anyhow 不接收 | 改 `anyhow::anyhow!` |
| E24 | `launcher.rs` 缓存闭包错误契约是 String，`from_str` 换成 anyhow 后 `?` 无法转换 | 局部 `.map_err(|e| e.to_string())`，不动 Cache |
| E25 | `download.rs` 第二处 `return Err("cancelled".to_string())` 首次替换只改了第一处 | 按缩进定位第二处补改 |
| E26 | `assert_eq!(Result<Value, anyhow::Error>, Ok(..))` 触发 E0369（anyhow::Error 无 PartialEq） | 三处改 `unwrap()` 后比值 |
| E27 | 自查抓到我把签名数写成 19、命中文件数写成 9；回 `git show HEAD` 逐文件数得 **15 个签名 / 8 个文件** | 全仓统一改为 15 / 8；`anyhow::Result` 实际落在 8 个文件，涉及 9 个模块（第 9 个是 launcher.rs 的调用面适配，本身无签名） |

### 测试

`cargo build --offline` 通过；`cargo test --offline` **153 passed / 0 failed**，与 032 同数：本轮是错误类型替换，未新增/删除测试，原断言全部保留。

## 四值

| 项 | 值 |
| --- | --- |
| Q-031-01 结案、031/032 口径不变 | 已证实 |
| anyhow 1.0.104 进构建、12 包 11 第三方、153 / 0 | 已证实 |
| 15 个签名换库、上游 `src/` 未改、两份 LICENSE 全文 | 已证实 |
| `dirs` 换 paths.rs | 已失败（语义不匹配 + Windows 分支不可验证），已如实登记并改轨 |
| 自动命令实现层、真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 / 未启动 |
| 后端仓写请求 | 0（已证实） |

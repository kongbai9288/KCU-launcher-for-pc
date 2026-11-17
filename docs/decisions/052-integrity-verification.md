# 第 052 轮：B06 实现层软件完整性验证

| 项 | 值 |
| --- | --- |
| 编号 | 052 |
| 状态 | `src/` 已落地；演示层与 PNG 零改动；UI 闸门未触发 |
| 依据 | `docs/spec/52-round-052-instructions.txt`（逐字：「干」） |
| 对应 | 048 合规核对 B06 / D07；051 补记「实现层未启动」；`00-requirements.txt` §7.3、§9.3、§12、§14、§18.6 |

## 开工复读（B02）

`docs/records/round-052-full-readback.md`：

| 文件 | 字节 | 行 | SHA-256 前 16 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f` |
| `docs/checklists/ai-errors.md` | 34458 | 364 | `b08e96ae816e4895` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf` |

对 4 份执行全文 `read_text()` 与逐行遍历。防错清单 364 行**全文回显**（A182 点名、此前从未逐字打印）；`00-requirements.txt` 261 行已于 051 全文回显；另两份全文遍历、未逐行打印。复读在写任何代码之前完成。`ai-errors.md` 哈希较 051 变化是 051 自己追加 A178–A182 所致。

## 范围判定

051 结尾写「继续按台账走 B06 的实现层软件完整性验证 —— 用已进构建的 ed25519-compact 做本地签名比对，不拉新依赖、不碰真实网络 IO；或用户点 EQ-01 ~ EQ-13 任一编号」。用户回「干」，按默认走前者。**不声称用户已决断**（D-052-1，沿用 050 的 A177）。

## 落地

| 编号 | 动作 |
| --- | --- |
| U121 | `src/core/integrity.rs`（608 行），`src/core/mod.rs` 注册。零新增第三方：`Cargo.toml` / `Cargo.lock` / `vendor/` 未动，仍 26 包 / 25 第三方。 |
| U122 | 验签复用 036 `updater::verify::verify_detached`（ed25519-compact），**排在解析之前**；失败不解析清单，符合 036 A95。 |
| U123 | manifest 解析用 `serde_json::Value` 的 `get` / `as_str` / `as_array`（031 的口径），空集合、缺字段、超 4096 项、摘要非 128 位 hex 全返回 `Fatal`，无 `expect` / 下标 panic。 |
| U124 | 路径走 `robust::safe_join`（048，标准库 `Component`），拒绝对路径、`..` 越界、Windows 保留名、控制字符、超深；摘要用 `ed25519_compact::sha512` + 042 的 `hex`。 |
| U125 | `Level` 四级 `Ok` / `Degraded` / `FeatureDisabled` / `Fatal`，`code()` 显式字符串（046 A154）；映射见 `docs/features/software-integrity.md`。 |
| U126 | 摘要缓存复用 029 的 `Cache`（lru）：`path:len -> sha512hex`，容量 256 / TTL 30 s / 加载超时 5 s；`refresh()` 全清。**签名与判定每次重跑，不缓存结论**。 |
| U127 | `OpBudget`（048）限 64 次/秒；超限返回 `integrity.rate_limited` / `FeatureDisabled`，**不返回通过**，高频调用不能绕过校验。 |
| U128 | 连续失败 ≥ `SAFE_MODE_AFTER=3` → `safe_mode=1` + `DiagnosticBundle`（诊断行 / 配置快照 / 运行时信息 / 已加载模块列表）。阈值与 `src/dispatcher/launcher.rs` 第 3 次失败进安全模式一致（A158 全量核对）。 |
| U129 | 结果带 `Envelope::new(Kind::Response, "core.integrity")`，`code` / `level` / `checked` / `safe_mode` 字段，非 `Ok` 用 `with_error`；诊断行走 `diag_line`，单行 `[KCU]` 前缀。 |

**信任根口径**：`public_key` / `signature` / `manifest_bytes` / `root` / `read` 全部由调用方注入，代码不内置任何密钥、不写绝对路径、不发网络请求。符合 §7.3「禁止硬编码环境假设（绝对路径、写死架构名、密钥）」与 A12 / A13。发行物的公钥分发流程**未启动**。

## 演示层三个动作到结果码的映射

| 演示层动作（051 `DECLARATION`） | 实现层条件 | 结果 |
| --- | --- | --- |
| 用默认继续 | `level != Ok` 且 `safe_mode=0` | 忽略自定义配置用内置默认，不加载被篡改内容 |
| 重新获取 | 任意非 `Ok` | `refresh()` 后重走 `verify()`；限流态等窗口滚动 |
| 取消 | 任意 | 不继续启动，保留诊断行 |

**如实**：051 的三卡与按钮是静态预览，未接实现层回调；渲染层接线属 UI 层未启动，本轮不动 UX HTML。

## 验证

| 编号 | 命令 | 输出 |
| --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `2cbe9fd`，DIRTY 0，1020 文件 |
| V2 | `git diff -- src/ Cargo.toml Cargo.lock vendor/` | 仅 `src/core/mod.rs` + 新增 `src/core/integrity.rs`；Cargo.* / vendor/ 零改动 |
| V3 | `cargo test --offline --lib core::integrity` | **15 / 0**，零 warning |
| V4 | `cargo test --offline --lib` | **313 / 0**（298 + 15） |
| V5 | `http_construct` / `window_handle_contract` | 7 / 0，6 / 0 |
| V6 | `plugin_lifecycle_load` / `plugin_abi_load` | 7 / 0（54.54 s），6 / 0（116.87 s），真加载 cdylib |
| V7 | 全量合计 | **339 / 0** |
| V8 | `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile`，35.04 s |
| V9 | `panic_guard` / `semver_guard` / `i18n_guard` / `lang_guard` | `files 39 hits 0` / `hits 0` / `hits 0` / `keys 26` |
| V10 | `p09_scan` | `P09_HITS 0 []` |
| V11 | CI 三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` |
| V12 | `node new Function` demos HTML + 2 语言包 | `ALL_JS_OK 42` |
| V13 | `yaml.safe_load(ci.yml)` + `ast.parse(scripts/*.py)` | `scan_steps 8` |
| V14 | 反向验证（A159） | 反转验签判定 → **9 FAILED / 6 passed**；恢复 → 15 / 0 |
| V15 | `git diff --name-only -- demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空；56 张 PNG 未改 |
| V16 | 远端 `GET /git/trees/...?recursive=1` 逐项比对 | ALL_MATCH True |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E105 | 首版 `hex::encode(h.as_ref())` 编译前不确定 `sha512::Hash` 是否实现 `AsRef` | 编译验证通过；未改断言 |
| E106 | 全局替换 `disk` → `_disk` 误改 7 处，其中 5 处仍引用 `disk`，触发 6 个 E0425 | 全部恢复，按编译警告精确定位 3 行改 `_disk`；复跑 313 / 0 零 warning |
| E107 | 反向验证注入后 9 个测试 FAILED，不是预估的 2 个 | 如实记录 9 个；证明验签是所有正向路径的共同前置，未调整测试 |
| E108 | abi 集成首跑被网关 502 截断 | 等待后重跑 6 / 0，断言没降 |

## 自我批判

- 本轮 **零新增第三方**，全部复用已进构建的库：验签 036、摘要 ed25519-compact（037 已用）、hex 042、serde_json 031、路径 048、缓存 029、信封 031、限流 048。项目侧只有顺序编排、分级策略、字段映射 —— 这些无语义等价库可换，如实登记为业务编排层，**不是新开自写底座例外**（023 A03 已于 024 撤回）。
- **不缓存校验结论**是刻意取舍：缓存结果会在文件被替换后误判通过。缓存只省 SHA-512 计算，`path:len` 键让长度变化必然重算；同长度同路径的内容替换仍依赖 TTL 30 s，这是已知窗口，写进 `docs/features/software-integrity.md`，不写成「完全无风险」。
- B06 只补了**签名比对**这一项。`从 GitHub/atomgit 拉版本平台信息`、manifest 生成与公钥分发、Win7 运行时判定仍属 D07 **未启动**；不能把 B06 整体写成「已修」。
- 演示层三个按钮仍是静态预览，未接 `Outcome` 回调；渲染层接线属 UI 层，本轮 UI 闸门未触发，不动 UX HTML。
- 用户未点 EQ 编号，按 051 结尾的默认执行，登记 **D-052-1**，不写成已决断。
- 051 刚立的 B01 / B02 本轮照做：防错清单全文回显、回复按 §14 十二项；035–047 历史偏差仍不补写。

## 四值

| 项 | 值 |
| --- | --- |
| B02 复读证据、防错清单 364 行全文回显 | 已证实 |
| B06 实现层签名比对、四级兜底、安全模式诊断包 | 已证实 |
| 313 / 0 单元、339 / 0 全量、Windows GNU、四守卫、反向验证 9 FAILED | 已证实 |
| 零新增依赖、26 包 / 25 第三方、演示层零改动 | 已证实 |
| B01 / B02 历史缺失、B06 其余两项、D07 取数与分发 | 已失败 / 未启动 |
| EQ-01 ~ EQ-13 拍板 | 未证实 |
| GUI 端到端、真实网络 IO、Win7 / MSVC 运行时 | 受阻 |

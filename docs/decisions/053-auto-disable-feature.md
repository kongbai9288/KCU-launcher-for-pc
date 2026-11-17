# 第 053 轮：B06 第二项自动关闭功能判定层

| 项 | 值 |
| --- | --- |
| 编号 | 053 |
| 状态 | `src/` 已落地；演示层与 PNG 零改动；UI 闸门未触发 |
| 依据 | `docs/spec/53-round-053-instructions.txt`（逐字：「干」） |
| 对应 | 048 合规核对 B06 / D07；原文第 5、12 行；§7.3、§9.3、§12、§14、§18.6 |

## 开工复读（B02）

`docs/records/round-053-full-readback.md`：

| 文件 | 字节 | 行 | SHA-256 前 16 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f` |
| `docs/checklists/ai-errors.md` | 35200 | 374 | `a82a69f8f8aea321` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf` |

对 4 份执行全文 `read_text()` 与逐行遍历。**本轮全文回显 `11-features-input.txt` 268 行**（048 合规核对 C/D 类所依据的功能原文，此前从未逐字打印）；`00-requirements.txt` 261 行 051 已回显，`ai-errors.md` 364 行 052 已回显，本轮为 374 行（052 追加 A183–A187 所致），`12-server-features-input.txt` 全文遍历未逐行打印。复读在写任何代码之前完成。

**复读发现的真实偏差（E109）**：原文第 12 行「软件完整性验证[失败则声明软件可能被修改，**离线则不声明**]」。052 的 `Outcome` 没有 `offline` / `declaration` 字段，失败一律会触发声明。本轮补上，见 U130。

## 范围判定

052 结尾写「继续按台账走 B06 剩余两项中的『自动关闭某功能』——从版本平台信息得到可用范围后关闭对应入口，属真实网络 IO 层，需 EQ-01 / EQ-03 的 Win7 TLS 口径拍板才能动」。用户回「干」，未点 EQ 编号。按 050 的 A177，把**不碰真实网络 IO 的判定层**先落地：平台策略字节、公钥、签名、设备能力、当前版本、日期全部由调用方注入，取数与分发仍标未启动。登记 **D-053-1**（我的默认，不是用户决断），不写成已拍板。

## 统一调研

`docs/research/21-feature-gate.md`：3 组关键词 6 条结果，采用 4 条、不采用 2 条，完整 URL 与一手原句逐条落盘。

| 编号 | 来源要点 | 落地 |
| --- | --- | --- |
| R01 | 签名快照本地判定；评估失败要有文档化的 fail-open/fail-closed 默认；断开控制平面验证本地安全默认；每条 flag 有 owner / expiry / safe default | U131–U134 |
| R02 | 活跃上限、禁止嵌套 flag、禁止用 flag 放 API URL 与凭据、CI 检查过期 | U134 / U135 / U138 |
| R03 | VS Code when-clause 用上下文键选择性启用/禁用 UI 元素 | U136（只做布尔键查表，不实现表达式解析器） |
| R04 | Minecraft Launcher 设置页开关默认 OFF | 一般形态参考，不照抄开关名 |

未证实：VS Code 官方原站 when-clause 正文（只取到中文镜像）、平台版本信息 schema、真实网络 IO、Win7 / MSVC 运行时。

## 落地

| 编号 | 动作 |
| --- | --- |
| U130 | **修 052 遗留**：`VerifyInput` 加 `offline`，`Outcome` 加 `declaration`；`finish()` 里 `declaration = level != Ok && !offline`，信封加 `declaration` / `offline`，诊断行加 `declaration=0/1`；新增 3 个测试（离线失败不声明但仍分级、在线失败声明、通过永不声明）。 |
| U131 | `src/core/feature_gate.rs`（796 行），`src/core/mod.rs` 注册。零新增第三方：`Cargo.toml` / `Cargo.lock` / `vendor/` 未动，仍 26 包 / 25 第三方。 |
| U132 | `BUILTIN_POLICY` 编译进模块（原文「必须内置」），空条目；策略缺失 / 空 / 超 256 KiB → 回退，`source=builtin`。 |
| U133 | 验签复用 036 `verify_detached` 且**排在解析之前**；失败回退内置默认，不解析内容、不关任何功能。 |
| U134 | `parse_entries` 用 `serde_json` 严格字段白名单，`FORBIDDEN_ENTRY_KEYS` 拒 9 类键；`schema!=1` / 超 512 条 / 非对象 / `default` 非法 / `expires` 畸形 → 内置默认。 |
| U135 | `KNOWN_FEATURES` 14 项白名单，未知 id 忽略；`CORE_LOCKED` 两项（设置 / 关于）永不关闭；单条独立判定，无嵌套依赖。 |
| U136 | `DeviceCaps.context` 宿主注入布尔键，`requires` 全真才启用；本模块不做系统检测。 |
| U137 | `min_app` / `max_app` 用 034 的 `semver::Version::cmp_precedence`，不用 `==`；`0.5.0+paper.1` 与 `0.5.0` 同 precedence 的测试覆盖。 |
| U138 | `expires` 按 ISO `YYYY-MM-DD` 校验，过期条目忽略不生效。 |
| U139 | 每处关闭生成 `Notice`（语义 `reason_key` / `closable` / 三动作）并写一条单行 `[KCU]` 诊断；与 051 声明页三项对齐，流程结束 0 残留。 |
| U140 | 判定缓存复用 029 `Cache`（128 / TTL 30 s / 加载超时 5 s），键含 `id:app_version:today`；`refresh()` 全清后重跑签名与全部判定，**签名与结论不缓存**。 |
| U141 | `CancelToken`（027）取消 → 空结果、0 副作用、缓存不变；`OpBudget`（048）限流 → `gate.rate_limited`，不关功能。 |
| U142 | `GateOutcome` 带 `Envelope::new(Kind::Response,"core.feature_gate")`，字段 `code` / `source` / `policy_version` / `features` / `disabled` / `notices` / `cancel`；异常 code 用 `with_error`。 |

**信任根口径**：全部输入由调用方注入，代码不内置密钥、不写绝对路径、不发网络请求、不检测系统。符合 §7.3 与 A12 / A13。内置的是**默认策略数据**（原文要求），不是 API 地址或凭据。

## 三轮真迭代与自评

| 轮 | 分 | 缺什么 | 补什么 |
| --- | --- | --- | --- |
| 初稿 | 8.2 | 只做平台版本范围；漏原文第 5 行设备能力；离线口径与完整性验证混用；052 遗留没发现 | 补 `DeviceCaps`、拆两条离线口径、B02 复读发现 E109 |
| 二稿 | 8.9 | 缺内置默认策略、未知 id 防护、核心锁定、禁止字段、fail-open、缓存刷新、取消 | 补 U131–U135 / U140 / U141 |
| 终稿 | **9.4** | 缺过期 flag、policy_version 进信封、每条关闭的可关声明、双向反向验证 | 补 U137–U139、E112 / E113 两次注入 |

自评 9.4，未给满分：平台取数、公钥分发、渲染层接线未启动；调研只取到 VS Code 中文镜像而非官方原站；`expires` 是字符串日期比较，依赖调用方注入 ISO 格式，未做时区处理（已写进未启动项）。

## 验证

| 编号 | 命令 | 输出 |
| --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `7aae835`，DIRTY 0，1028 文件 |
| V2 | `git diff --name-only -- Cargo.toml Cargo.lock vendor/` | 空 |
| V3 | `cargo test --offline --lib core::feature_gate` | **15 / 0** |
| V4 | `cargo test --offline --lib` | **331 / 0**（052 的 313 + 15 + 3），零 warning |
| V5 | `http_construct` / `window_handle_contract` | 7 / 0，6 / 0 |
| V6 | `plugin_lifecycle_load` / `plugin_abi_load` | 7 / 0（36.45 s），6 / 0（108.13 s），真加载 cdylib |
| V7 | 全量合计 | **357 / 0** |
| V8 | `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile`，14.96 s |
| V9 | `panic_guard` / `semver_guard` | `files 40 hits 0` / `version_files 4 hits 0` |
| V10 | `i18n_guard` / `lang_guard` | `hits 0` / `keys 26 stable_values_ok` |
| V11 | `p09_scan` | `P09_HITS 0 []` |
| V12 | CI 三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` |
| V13 | `node new Function` demos HTML + 2 语言包 | `ALL_JS_OK 43` |
| V14 | `yaml.safe_load(ci.yml)` + `ast.parse(scripts/*.py)` | `scan_steps 8` |
| V15 | 反向注入 A（允许未知 id） | **1 FAILED / 14 passed**；恢复 15 / 0 |
| V16 | 反向注入 B（反转验签判定） | **10 FAILED / 5 passed**；恢复 331 / 0 |
| V17 | `git diff -- demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空；56 张 PNG 未改 |
| V18 | 必读读取命令块 | 275 项，`MISSING 0` |
| V19 | 远端 `GET /git/trees/...?recursive=1` 逐项比对 | ALL_MATCH True |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E109 | B02 复读发现 052 缺原文「离线则不声明」 | U130 补 `offline` / `declaration` 与 3 个测试；052 历史报告不补写 |
| E110 | `GateInput` derive `Debug` 因 `CancelToken` 无 `Debug` 触发 E0277 | 去掉 `Debug` derive（该结构不需要），不动 027 的模块 |
| E111 | 文件头注释引用原文含「为了」，触发 CI wording 扫描 | 改述为不含禁用词的描述，复跑 `NO_EXPLANATORY` |
| E112 | 反向注入「允许未知 id」只有 1 个测试 FAILED | 按实记录 1，不按预估写；该防护只有一条专属断言，不加测试凑数 |
| E113 | 反向注入「反转验签」10 个测试 FAILED | 按实记录 10；证明验签是全部平台路径的共同前置 |
| E114 | 综合验证命令被网关 502 截断 | 拆成单条短命令重跑补齐，未降验收项 |

## 自我批判

- **零新增第三方**：验签 036、版本 034、JSON 031、边界与限流 048、缓存 029、信封 031、取消 027、诊断 032 全部复用。项目侧只有顺序编排、白名单策略、声明映射，无语义等价库可换；不是新开自写底座例外（023 A03 已于 024 撤回）。
- **B06 只补到判定层**：原文「从我的 github 或 atomgit 仓库拉需有版本平台等信息」的取数、签发、公钥分发仍属 D07 未启动，不能把 B06 整体写成「已修」。051 演示层三项、052 完整性、053 判定层，是三块各自落地的状态分层。
- **离线口径不混用**：052 的「离线不声明」专指软件完整性验证；053 的自动关闭功能是本地判定，离线仍显示声明但来源标 `builtin`。若一律套「离线不声明」，用户反而看不到哪些功能被关了。
- **fail-open 的代价**：极端情况下平台明确要求关闭的功能，在签名不符时仍会启用。这是刻意取舍（误关比不关更糟），写进 `docs/features/auto-disable-feature.md`，不写成「完全无风险」。
- **演示层三按钮仍是静态预览**，未接 `GateOutcome` 回调；渲染层接线属 UI 层，本轮 UI 闸门未触发，UX HTML 与 56 张 PNG 零 diff。
- 用户未点 EQ 编号，按 052 结尾默认执行，登记 D-053-1，不写成已决断。

## 四值

| 项 | 值 |
| --- | --- |
| B02 复读证据、功能原文 268 行全文回显、E109 修正 | 已证实 |
| B06 第二项判定层、内置默认、fail-open、声明与刷新 | 已证实 |
| 331 / 0 单元、357 / 0 全量、Windows GNU、四守卫、双向注入 | 已证实 |
| 零新增依赖、26 包 / 25 第三方、演示层零改动 | 已证实 |
| B01 / B02 历史缺失 | 已失败（不补写） |
| B06 平台取数 / 签发 / 公钥分发 / 渲染层接线 / Win7 判定 | 未启动 |
| EQ-01 ~ EQ-13 拍板 | 未证实 |
| GUI 端到端、真实网络 IO、Win7 / MSVC 运行时 | 受阻 |

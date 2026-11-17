# 第 054 轮：B08 境外离线账户限制本地判定层

| 项 | 值 |
| --- | --- |
| 编号 | 054 |
| 状态 | `src/` 已落地；UX HTML / 语言包 / 56 张 PNG 零改动；UI 闸门未触发 |
| 依据 | `docs/spec/54-round-054-instructions.txt`（逐字：「干」） |
| 对应 | 048 合规核对 B08；原文第 7 行；§7.3、§9.3、§12、§14、§18.6 |

## 开工复读（B02）

`docs/records/round-054-full-readback.md`：

| 文件 | 字节 | 行 | SHA-256 前 16 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f` |
| `docs/checklists/ai-errors.md` | 36208 | 385 | `e71a7c3e795b8d17` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf` |
| `docs/spec/53-round-053-instructions.txt` | 4 | 1 | `67997353aa5bff04` |

对 5 份执行全文 `read_text()` 与逐行遍历。**本轮全文回显 `docs/spec/12-server-features-input.txt` 64 行**（开服器功能原文，此前从未逐行打印）；`ai-errors.md` 本轮 385 行（053 追加 A188–A193 所致）。复读在写任何代码之前完成。

**复读发现的真实边界（E115）**：`src/core/config.rs` 早有 `region_override` / `set_download_region("overseas")` / `download_region()`，测试名 `region_override_only_exposed_for_download_selection`；演示层 `t.0409` 写着「仅下载选择，不复用为地区禁用」。B08 是**用户原文**，要求的是账户登录/注册的地域限制，不能被我自己写的演示文案压过。处置：新建独立 `signals` 链、**不读写 `download_region`**，`t.0409` 的修正登记 **D-054-2**，等 UI 闸门触发的轮次再改，本轮不动演示。

## 范围判定

053 结尾写「B06 三项的判定层已齐，剩下全在 D07 实现层……真实网络 IO 需 EQ-01 / EQ-03 拍板；或用户点 EQ-01 ~ EQ-13 任一编号」。用户回「干」，未点 EQ 编号。按 050 的 A177 继续走 048 核对表剩余 B 类偏差，选 **B08**：它有明确原文、不碰真实网络 IO（原文反而**禁止**网络打法）、不碰 UI 闸门。登记 **D-054-1**（我的默认，不是用户决断）。

## 统一调研

`docs/research/22-region-signals.md`：3 组关键词 9 条结果，采用 5 条、不采用 4 条，完整 URL 与一手原句逐条落盘。

| 编号 | 来源要点 | 落地 |
| --- | --- | --- |
| R01 | Microsoft Learn BCP-47：区域子标签是 ISO 3166-1 alpha-2（2 字母大写）或 UN M49（3 位数字）；`zh-yue-HK`、`de-DE-u-co-phonebk` 示例；子标签会变更 | U146 `region_subtag()` 只取第一个合法区域段，跳过 script / extlang / extension；不实现完整解析器 |
| R02 | MSDN `GetUserDefaultLocaleName`：可取自定义区域，数据不保证跨机器或跨运行一致 | U144 全部由宿主注入，不调系统 API、不缓存跨运行结论 |
| R03 | ProxyWhereabouts：「IP geolocation is an inference, not a measurement」；VPN 出口节点；要提供 fallbacks 与申诉 | U145 禁用键白名单；U151 声明三动作含「手动指定地区」 |
| R04 | GeoIPHub 2026：「The recurring failure mode is over-blocking」「One signal should never trigger a hard block」「design for uncertainty」 | U146 双信号一致；U147 单一/冲突 → Unknown；U153 限流与取消不误禁 |
| R05 | tsight.io：Locale 不等于国家，`zh-Hans-CN` 是本地化环境不是地理标识；偏好协商 + 用户显式设置优先 | U144 / U148 用户覆盖排第一、locale 与时区作两个独立偏好信号 |

不采用：IP2Location 商业产品页（正是原文禁止的网络打法）、kakunin-ip.click GeoIP 词条（与 R03/R04 重复）、CSDN `setlocale` 实验博客（不作结论来源）、bcp47.antfu.me 在线工具页（规范以 R01 为准）。未证实：Windows `LOCALE_SCOUNTRY` 官方原文、IANA 时区到地理区域的权威映射、原文「物理位置」的精确定义、特殊版标识注入方式。

## 落地

| 编号 | 动作 |
| --- | --- |
| U143 | 原文第 7 行拆成 6 条独立规则分别落地，不合并成一句「境外就禁」 |
| U144 | `src/core/region.rs`（869 行）：`RegionInput.signals` 宿主注入；**不读写 `config.download_region`**；不发网络请求、不读 IP、不做 GeoIP、不检测系统、不内置密钥 |
| U145 | `ALLOWED_SIGNAL_KEYS` 8 键白名单、`FORBIDDEN_SIGNAL_KEYS` 16 类禁用键（10 类网络探测 + 6 类凭据/地址）；任一出现整份信号作废，回退不限制 |
| U146 | `region_subtag()` 取 BCP-47 区域段；`MAINLAND_TIMEZONES` 2 项；**locale 明确非 CN 且时区明确非大陆，两信号一致才判 `Outside`** |
| U147 | 单一信号、冲突信号（`zh-CN` + `America/New_York`）、缺信号一律 `Unknown → 不限制`；信号畸形 / 超长 / 超 16 键 → `region.signal_invalid`，`allowed=true` |
| U148 | 判定优先级：`special_build` 全局豁免 > `user_override` > `authenticated`（正版后正常） > `region=Mainland` 恢复 > 账户与动作范围 > 拒绝 |
| U149 | `account=offline` 且 `action∈{login,register}` 且 `Outside` → `allowed=false`；两种动作各生成一条可关声明，`id=region.offline_login` / `region.offline_register` |
| U150 | 原文只点名离线账户；`third_party` / `mojang` 保持可用，**不扩大范围**；登记 D-054-2（未决断，按最小范围执行） |
| U151 | `RegionNotice` 语义 `reason_key` / `closable` / 三动作（改用正版、手动指定地区、取消），每条写一条单行 `[KCU]` 诊断；流程结束 0 残留 |
| U152 | 判定缓存复用 029 `Cache`（128 / TTL 30 s / 加载超时 5 s），键含 region / source / account / action / special / authenticated / locale；`refresh()` 全清重跑 |
| U153 | `CancelToken`（027）取消 → 空结果、0 副作用、缓存不变；`OpBudget`（048）限流 → `region.rate_limited`，`allowed=true` 不误禁 |
| U154 | `offline` 键允许注入且过边界校验，但**显式不参与判定**；诊断行与信封带 `network_probe=0`，与 053 的「离线不声明」口径分层 |
| U155 | `RegionOutcome` 带 `Envelope::new(Kind::Response,"core.region")`；`diagnostic_payload()` 只输出判定结论，不带原始信号、不带 IP |

**零新增第三方**：`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。边界与限流 048、缓存 029、信封 031、取消 027、诊断 032、`serde_json::json!` 031 全部复用；项目侧只有信号白名单、区域解析、判定顺序、声明映射，无语义等价库可换，不是新开自写底座例外（023 A03 已于 024 撤回）。

## 三轮真迭代与自评

| 轮 | 分 | 缺什么 | 补什么 |
| --- | --- | --- | --- |
| 初稿 | 8.3 | 只做「境外禁离线」；漏原文第 6 条禁网络打法、漏 `config.download_region` 既有口径、漏双信号防误伤、漏特殊版/正版/大陆三条豁免 | B02 复读发现 E115；拆 6 条约束；建独立链 |
| 二稿 | 8.9 | 缺禁用键白名单、fail-open、声明三动作、缓存刷新、取消限流 | 补 U145 / U147 / U151 / U152 / U153 |
| 终稿 | **9.4** | 缺 B02 全文回显、调研一手原句与不采用项、双向反向注入、离线口径与 053 分层 | 补 64 行回显、R01–R05、E116/E117、U154 |

自评 9.4，未给满分：真实网络 IO / GUI 接线 / 特殊版标识注入未启动；「物理位置」精确定义与 IANA 时区权威映射未证实；`t.0409` 演示文案按 UI 闸门规则留到动界面的轮次修正。

## 验证

| 编号 | 命令 | 输出 |
| --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `950e21c`，DIRTY 0，1037 文件；远端 `4167881`，1037 文件 ALL_MATCH |
| V2 | `git diff --name-only -- Cargo.toml Cargo.lock vendor/` | 空 |
| V3 | `cargo test --offline --lib core::region` | **20 / 0** |
| V4 | `cargo test --offline --lib` | **351 / 0**（331 + 20），零 warning |
| V5 | `http_construct` / `window_handle_contract` | 7 / 0，6 / 0 |
| V6 | `plugin_lifecycle_load` / `plugin_abi_load` | 7 / 0（29.57 s），6 / 0（77.67 s），真加载 cdylib |
| V7 | 全量合计 | **377 / 0** |
| V8 | `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile`，16.03 s |
| V9 | `panic_guard` / `semver_guard` | `files 41 hits 0` / `version_files 4 hits 0` |
| V10 | `i18n_guard` / `lang_guard` | `rs_files 41 hits 0` / `keys 26 stable_values_ok` |
| V11 | `p09_scan` | `P09_HITS 0 []` |
| V12 | CI 三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` |
| V13 | `node new Function` demos HTML + 2 语言包 | `ALL_JS_OK 44` |
| V14 | `yaml.safe_load(ci.yml)` + `ast.parse(scripts/*.py)` | `scan_steps 8` |
| V15 | 反向注入 A（境外不限制） | **5 FAILED / 15 passed**；恢复 20 / 0 |
| V16 | 反向注入 B（单一信号即判境外） | **1 FAILED / 19 passed**；恢复 351 / 0 |
| V17 | `git diff -- demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空；56 张 PNG 未改 |
| V18 | 必读读取命令块 | 282 项，`MISSING 0` |
| V19 | 远端 `GET /git/trees/...?recursive=1` 逐项比对 | ALL_MATCH True |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E115 | B02 复读发现 `config.rs::download_region` 与演示层 `t.0409` 的既有口径，与 B08 用户原文冲突 | 建独立信号链不读写 `download_region`；`t.0409` 修正登记 D-054-2，UI 闸门未触发故不改演示 |
| E116 | `RegionInput` derive `Debug` 因 `CancelToken` 无 `Debug` 触发 E0277（与 053 E110 同类） | 去掉 `Debug` derive，不动 027 模块；防错项 A193 已覆盖此类 |
| E117 | 未用导入 `MAX_TEXT_BYTES` 与 `Signals.offline` 字段 dead_code | 删导入；`offline` 改为「允许键但显式不参与判定」，零 warning |
| E118 | 反向注入 A 5 FAILED、B 1 FAILED | 按实记录，不凑数；B 只有一条专属断言故只 1 个 FAILED |
| E119 | 综合验证命令被网关 502 截断（与 053 E114 同类） | 拆成单条短命令重跑补齐，未降验收项 |

## 自我批判

- **B08 只补到判定层**：原文「物理位置」的取数、特殊版标识注入、GUI 接线仍属 D07 未启动，不能把 B08 整体写成「已修」。048 核对表状态改为「判定层已落地，余项未启动」。
- **用户原文 > 我写的演示文案**：`t.0409` 是我自己加的默认口径，B08 是用户原文。两者冲突时按原文实现，演示层修正排队等 UI 闸门，不偷偷改界面也不假装没冲突。
- **fail-open 的代价**：极端情况下确在境外的离线账户，若信号只有一个或互相冲突，仍可登录。这是刻意取舍（错杀比漏判更糟，且原文点名怕误伤），写进功能 md，不写成「完全无风险」。
- **不扩大范围**：原文只点名离线账户，第三方登录与正版保持可用。这是未决断口径 D-054-2，按最小范围执行并登记，不写成已拍板。
- **离线口径三层分开**：052/053 完整性验证「离线不声明」、053 自动关闭功能「离线仍声明但标内置」、054 账户限制「offline 不参与判定」，三条互不套用。
- 用户未点 EQ 编号，按 053 结尾默认继续走 B 类台账，登记 D-054-1，不写成已决断。
- 演示层三按钮仍是静态预览，本轮 UI 闸门未触发，UX HTML、两语言包、56 张 PNG 零 diff。

## 四值

| 项 | 值 |
| --- | --- |
| B02 复读证据、开服器原文 64 行全文回显、E115 边界发现 | 已证实 |
| B08 判定层、6 条原文约束、双信号防误伤、独立链、fail-open | 已证实 |
| 351 / 0 单元、377 / 0 全量、Windows GNU、四守卫、双向注入 | 已证实 |
| 零新增依赖、26 包 / 25 第三方、演示层零改动 | 已证实 |
| B01 / B02 历史缺失、演示层 `t.0409` 口径差异 | 已失败（不补写）/ 已登记 |
| 真实网络 IO、GUI 接线、特殊版标识注入、Win7 声明文案 | 未启动 |
| EQ-01 ~ EQ-13 拍板、物理位置定义、IANA 映射、特殊版标识 | 未证实 |
| GUI 端到端、Win7 / MSVC 运行时 | 受阻 |

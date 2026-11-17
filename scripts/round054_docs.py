from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
html_n = len(list((ROOT / 'demos').glob('*.html')))
png_n = len(list((ROOT / 'demos/preview').glob('[0-9][0-9]-*.png')))
src_n = len(list((ROOT / 'src').rglob('*.rs')))
region_lines = len((ROOT / 'src/core/region.rs').read_text().splitlines())
print('REAL pkgs', pkgs, 'third', third, 'html', html_n, 'png', png_n,
      'src_rs', src_n, 'region_lines', region_lines)

Path('docs/spec/54-round-054-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/features/region-offline-restriction.md'] = '''# 境外离线账户登录/注册限制（B08）

| 字段 | 值 |
| --- | --- |
| 编号 | F054-01 / B08 / D07 |
| 状态 | 判定层已落地（`src/core/region.rs`）；真实网络 IO、GUI 接线、特殊版标识注入未启动 |
| 原文 | `docs/spec/11-features-input.txt` 第 7 行 |
| 触发 | 启动登录/注册流程前，由调度器注入本地信号、用户覆盖、特殊版标记、账户类型、正版权状态 |
| 输出 | `RegionOutcome { code, region, source, account, action, allowed, reason_key, notices, diagnostics, envelope, cancelled }` |

## 原文拆成 6 条独立规则

| 序号 | 原文约束 | 落地 |
| --- | --- | --- |
| 1 | 除了特殊版本以外 | `special_build=1` 全局豁免，排在判定最前 |
| 2 | 发现玩家的物理位置处于国外 | locale 区域子标签明确非 `CN` **且** IANA 时区明确非大陆 → `Outside` |
| 3 | 离线账户的登录与注册都不可以使用 | `account=offline` 且 `action∈{login,register}` 且 `region=Outside` → `allowed=false` |
| 4 | 这个功能在这个场景下只有在正版后才能正常使用 | `authenticated=1` → 放行 |
| 5 | 位于中国大陆地区功能将恢复正常 | `region=Mainland` → 放行 |
| 6 | **不能使用那种网络连接打法，因为那有可能误伤加速器、VPN** | 不发请求、不读 IP、不做 GeoIP；`FORBIDDEN_SIGNAL_KEYS` 拒 10 类网络/凭据键，出现即整份信号作废 |

## 输入信号（宿主注入，本模块不检测系统）

| 键 | 含义 | 校验 |
| --- | --- | --- |
| `locale` | BCP-47 语言标签 | 只做形状校验与区域子标签提取，不实现完整解析器 |
| `timezone` | IANA 时区 | `Area/Location` 形状校验 |
| `user_override` | `mainland` / `outside` | 用户显式覆盖，排在信号判定之前 |
| `special_build` | `1` / `0` | 特殊版标记，由调用方注入，不写死版本名或仓库地址 |
| `account` | `offline` / `third_party` / `mojang` | 未知 → `Unknown` |
| `authenticated` | `1` / `0` | 正版已验证 |
| `action` | `login` / `register` | 未知 → 放行 |
| `offline` | `1` / `0` | **允许注入且过边界校验，但显式不参与判定**：网络可达与否不改变账户限制结论 |

禁用键（16 类，出现即整份作废）：`ip` / `geoip` / `vpn` / `proxy` / `asn` / `isp` / `network_probe` / `latitude` / `longitude` / `country_by_ip` / `url` / `endpoint` / `token` / `key` / `secret` / `api`。

## 防误伤（fail-open 文档化）

| 情况 | 结论 |
| --- | --- |
| 只有一个信号（只有 locale 或只有 timezone） | `Unknown` → 不限制 |
| 两个信号冲突（如 `zh-CN` 配 `America/New_York`） | `Unknown` → 不限制 |
| 信号缺失 / 畸形 / 超长 / 控制字符 / 禁用键 | `region.signal_invalid` → 不限制 |
| 限流 / 取消 | 不限制；取消 0 副作用 |
| 用户显式覆盖 | 排在信号之前，用户说了算 |
| 未知账户类型 / 未知动作 | 不限制 |

理由：调研 R03「IP geolocation is an inference, not a measurement」、R04「One signal should never trigger a hard block」、R05「Locale 不等于国家」。原文第 7 行点名怕误伤加速器与 VPN，因此宁可少判，不可错杀。

## 不扩大范围

原文只点名**离线账户**。`third_party` 与 `mojang` 保持可用，未擅自把限制扩大到第三方登录或正版登录；此口径登记 **D-054-2**（未决断，按最小范围执行），待用户拍板。

## 与下载源地域判定分开

`core/config.rs` 的 `download_region` / `set_download_region("overseas")` 只服务于下载源选择（050）。演示层 `t.0409` 写着「仅下载选择，不复用为地区禁用」，但 B08 是**用户原文**，不能被我写的演示文案压过。本模块使用独立的 `signals` 与 `user_override`，**不读写 `download_region`**。两条链分开、不混用同一份状态；`t.0409` 那句需在动 UI 的轮次修正，本轮 UI 闸门未触发故不改演示。

## 声明、缓存与诊断

每处拒绝生成一条 `RegionNotice`：语义 `reason_key`、`closable=true`、三动作 `region.act.premium` / `region.act.override` / `region.act.cancel`（改用正版 / 手动指定地区 / 取消），并写一条单行 `[KCU]` 诊断；流程结束 0 残留。判定缓存容量 128 / TTL 30 s，`refresh()` 全清后重跑；`offline` 与 `locale_tag` 只进诊断，不参与判定。统一信封 `core.region` 带 `network_probe=0` 显式字段。

## 离线口径分层（不与 053 混用）

| 模块 | 离线时 |
| --- | --- |
| 软件完整性验证（052 / 053 U130） | 失败仍分级、仍记诊断、仍不给通过，但**不弹声明页**（原文「离线则不声明」） |
| 自动关闭功能（053） | 本地判定，仍显示声明，来源标 `builtin` |
| 账户地域限制（本项） | `offline` 键显式不参与判定，网络可达与否不改变结论 |

## 未启动 / 未证实

- 从任何远端取「物理位置」或版本平台信息（原文禁止网络打法，且 schema 未证实）
- 特殊版本如何标识、由谁注入
- IANA 时区到地理区域的权威映射表（本模块只用 2 个大陆时区白名单）
- 原文「物理位置」的精确定义与可接受误差
- GUI 接线、Win7 声明文案、真实网络 IO、Win7 / MSVC 运行时

## 验证

`cargo test --offline --lib core::region` 20 / 0；`cargo test --offline --lib` 351 / 0；全量 377 / 0；反向注入「境外不限制」5 FAILED、「单一信号即判境外」1 FAILED，恢复后 351 / 0；Windows GNU 交叉检查通过。零新增第三方。
'''

D['docs/decisions/054-region-offline-restriction.md'] = f'''# 第 054 轮：B08 境外离线账户限制本地判定层

| 项 | 值 |
| --- | --- |
| 编号 | 054 |
| 状态 | `src/` 已落地；UX HTML / 语言包 / {png_n} 张 PNG 零改动；UI 闸门未触发 |
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
| U144 | `src/core/region.rs`（{region_lines} 行）：`RegionInput.signals` 宿主注入；**不读写 `config.download_region`**；不发网络请求、不读 IP、不做 GeoIP、不检测系统、不内置密钥 |
| U145 | `ALLOWED_SIGNAL_KEYS` 8 键白名单、`FORBIDDEN_SIGNAL_KEYS` 16 类禁用键（10 类网络探测 + 6 类凭据/地址）；任一出现整份信号作废，回退不限制 |
| U146 | `region_subtag()` 取 BCP-47 区域段；`MAINLAND_TIMEZONES` 2 项；**locale 明确非 CN 且时区明确非大陆，两信号一致才判 `Outside`** |
| U147 | 单一信号、冲突信号（`zh-CN` + `America/New_York`）、缺信号一律 `Unknown → 不限制`；信号畸形 / 超长 / 超 16 键 → `region.signal_invalid`，`allowed=true` |
| U148 | 判定优先级：`special_build` 全局豁免 > `user_override` > `authenticated`（正版后正常） > `region=Mainland` 恢复 > 账户与动作范围 > 拒绝 |
| U149 | `account=offline` 且 `action∈{{login,register}}` 且 `Outside` → `allowed=false`；两种动作各生成一条可关声明，`id=region.offline_login` / `region.offline_register` |
| U150 | 原文只点名离线账户；`third_party` / `mojang` 保持可用，**不扩大范围**；登记 D-054-2（未决断，按最小范围执行） |
| U151 | `RegionNotice` 语义 `reason_key` / `closable` / 三动作（改用正版、手动指定地区、取消），每条写一条单行 `[KCU]` 诊断；流程结束 0 残留 |
| U152 | 判定缓存复用 029 `Cache`（128 / TTL 30 s / 加载超时 5 s），键含 region / source / account / action / special / authenticated / locale；`refresh()` 全清重跑 |
| U153 | `CancelToken`（027）取消 → 空结果、0 副作用、缓存不变；`OpBudget`（048）限流 → `region.rate_limited`，`allowed=true` 不误禁 |
| U154 | `offline` 键允许注入且过边界校验，但**显式不参与判定**；诊断行与信封带 `network_probe=0`，与 053 的「离线不声明」口径分层 |
| U155 | `RegionOutcome` 带 `Envelope::new(Kind::Response,"core.region")`；`diagnostic_payload()` 只输出判定结论，不带原始信号、不带 IP |

**零新增第三方**：`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 {pkgs} 包 / {third} 第三方。边界与限流 048、缓存 029、信封 031、取消 027、诊断 032、`serde_json::json!` 031 全部复用；项目侧只有信号白名单、区域解析、判定顺序、声明映射，无语义等价库可换，不是新开自写底座例外（023 A03 已于 024 撤回）。

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
| V13 | `node new Function` demos HTML + 2 语言包 | `ALL_JS_OK {html_n}` |
| V14 | `yaml.safe_load(ci.yml)` + `ast.parse(scripts/*.py)` | `scan_steps 8` |
| V15 | 反向注入 A（境外不限制） | **5 FAILED / 15 passed**；恢复 20 / 0 |
| V16 | 反向注入 B（单一信号即判境外） | **1 FAILED / 19 passed**；恢复 351 / 0 |
| V17 | `git diff -- demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空；{png_n} 张 PNG 未改 |
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
- 演示层三按钮仍是静态预览，本轮 UI 闸门未触发，UX HTML、两语言包、{png_n} 张 PNG 零 diff。

## 四值

| 项 | 值 |
| --- | --- |
| B02 复读证据、开服器原文 64 行全文回显、E115 边界发现 | 已证实 |
| B08 判定层、6 条原文约束、双信号防误伤、独立链、fail-open | 已证实 |
| 351 / 0 单元、377 / 0 全量、Windows GNU、四守卫、双向注入 | 已证实 |
| 零新增依赖、{pkgs} 包 / {third} 第三方、演示层零改动 | 已证实 |
| B01 / B02 历史缺失、演示层 `t.0409` 口径差异 | 已失败（不补写）/ 已登记 |
| 真实网络 IO、GUI 接线、特殊版标识注入、Win7 声明文案 | 未启动 |
| EQ-01 ~ EQ-13 拍板、物理位置定义、IANA 映射、特殊版标识 | 未证实 |
| GUI 端到端、Win7 / MSVC 运行时 | 受阻 |
'''

D['docs/verification/round-054.md'] = f'''# 第 054 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 054 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | `src/` 有改动；UX HTML / 语言包 / {png_n} 张 PNG 零改动，UI 闸门未触发 |

| 编号 | 命令 / 检查 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `git rev-parse --short HEAD` / `git status` | `950e21c`，DIRTY 0，1037 文件 | 已证实 |
| V2 | `git diff --name-only -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V3 | `cargo test --offline --lib core::region` | **20 / 0** | 已证实 |
| V4 | `cargo test --offline --lib` | **351 / 0**，零 warning | 已证实 |
| V5 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V6 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V7 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，29.57 s，真加载 cdylib | 已证实 |
| V8 | `cargo test --offline --test plugin_abi_load` | 6 / 0，77.67 s | 已证实 |
| V9 | 全量合计 | **377 / 0** | 已证实 |
| V10 | `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile`，16.03 s | 已证实 |
| V11 | `panic_guard` | `files 41 hits 0` | 已证实 |
| V12 | `semver_guard` | `version_files 4 hits 0` | 已证实 |
| V13 | `i18n_guard` | `rs_files 41 hits 0 inline_bilingual_cn_lines 121` | 已证实 |
| V14 | `lang_guard` | `keys 26 stable_values_ok offline_refs_ok` | 已证实 |
| V15 | `p09_scan` | `P09_HITS 0 []` | 已证实 |
| V16 | `grep -rqE 'gh[p]_'` | `NO_CREDENTIAL` | 已证实 |
| V17 | 禁用词 / 硬编码 grep（src/） | `NO_EXPLANATORY` / `NO_HARDCODE` | 已证实 |
| V18 | `node new Function` demos HTML + 语言包 | `ALL_JS_OK {html_n}` | 已证实 |
| V19 | `yaml.safe_load` + `ast.parse` | `PY_YAML_OK scan_steps 8` | 已证实 |
| V20 | 反向注入 A（境外不限制） | 5 FAILED / 15 passed；恢复 20 / 0 | 已证实 |
| V21 | 反向注入 B（单一信号即判境外） | 1 FAILED / 19 passed；恢复 351 / 0 | 已证实 |
| V22 | `git diff -- demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空 | 已证实 |
| V23 | B02 复读记录 | 5 份字节 / 行 / SHA-256；开服器原文 64 行全文回显 | 已证实 |
| V24 | 必读读取命令块 | 282 项，`MISSING 0` | 已证实 |
| V25 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| B08 判定层、E115 边界发现、351 / 0、377 / 0 | 已证实 |
| B01 / B02 历史缺失、`t.0409` 演示层口径差异 | 已失败 / 已登记（不补写） |
| 真实网络 IO、GUI 接线、特殊版标识注入 | 未启动 |
| EQ-01 ~ EQ-13 拍板、物理位置定义、IANA 映射 | 未证实 |
| GUI 端到端、Win7 / MSVC 运行时 | 受阻 |

限制：改动作者未代改验证结论；377 个测试是回归，不作质量结论。E119 网关截断拆段补齐，未降验收项。048 / 051 / 052 / 053 历史验证报告按 B01 口径不补写。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s, marker=None):
    p = Path(f); t = p.read_text()
    m = marker or s.strip().splitlines()[0]
    if m in t:
        print('SKIP_DUP', f); return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 054 | B08 境外离线账户限制判定层 | src 落地，零新增依赖 | 054-region-offline-restriction.md |')

app('docs/records/requirement-compliance-audit.md', '''## 054 补记：B08 判定层落地、口径差异登记

| 编号 | 048 / 053 状态 | 054 状态 |
| --- | --- | --- |
| B08 | 登记为口径，未实现；「物理位置 + 区域设置」判定方式未落地 | **判定层已落地**：`src/core/region.rs`，原文第 7 行 6 条约束分别实现；双信号一致才判境外；禁用键白名单拒网络探测；fail-open 不误伤；零新增依赖 |
| B08 余项 | 真实网络 IO、GUI 接线、特殊版标识注入、Win7 声明文案 | 仍**未启动**，属 D07 |
| D-054-2 | — | 演示层 `t.0409`「仅下载选择，不复用为地区禁用」是我写的默认口径，与 B08 用户原文冲突；按原文实现独立链，`t.0409` 修正等 UI 闸门触发的轮次，本轮不改演示 |

B01 / B02 历史偏差仍标「已失败」，不补写、不重写。B03（050 已修）、B06（051/052/053 分层落地）、B04 / B05 / B07 / B09 / B10、C01–C10、D01–D09 本轮未动。EQ-14（049）、EQ-15（050）已关，EQ-01 ~ EQ-13 仍待拍板。
''', '## 054 补记')

app('docs/records/pending-question-environments.md', '''**054 状态**

本轮未新增 EQ。用户回「干」而非点 EQ 编号，按 053 结尾默认继续走 048 核对表剩余 B 类偏差，选 **B08**（明确原文、不碰真实网络 IO、不碰 UI 闸门），登记 **D-054-1**（我的默认，不是用户决断）。新增 **D-054-2**：原文只点名离线账户，第三方登录与正版保持可用，按最小范围执行；若用户本意要扩大到全部账户类型，需明确拍板。EQ-01 / EQ-03 的 Win7 TLS 口径仍是真实网络 IO 层的前置；EQ-01 ~ EQ-13 仍待拍板，EQ-14（049）、EQ-15（050）已关闭。
''', '**054 状态**')

app('docs/records/interface-log.md', '''## 054 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I90 | `src/core/region.rs` | `RegionGate` / `RegionInput` / `RegionOutcome` / `RegionNotice` / `Region` / `AccountKind` / `Action` / `DecisionSource` / `ALLOWED_SIGNAL_KEYS` / `FORBIDDEN_SIGNAL_KEYS` / `MAINLAND_TIMEZONES` / `region_subtag` / `diagnostic_payload` |
| I91 | 复用接口 | `robust::check_text`/`OpBudget`(048)、`cache::Cache`(029)、`Envelope`(031)、`CancelToken`(027)、`diag_line`(032)、`serde_json::json!`(031) |
| I92 | 常量 | `MAX_SIGNAL_BYTES=128`、`MAX_SIGNAL_KEYS=16`、`CACHE_CAPACITY=128`、`CACHE_TTL_SECS=30`、`LOAD_TIMEOUT_SECS=5` |
| I93 | 状态 | U143–U155 已证实；零新增依赖；真实网络 IO / GUI 接线 / 特殊版标识注入未启动 |
| S53 | 独立链 | 不读写 `config.rs::download_region`；`offline` 键显式不参与判定 |
''')

app('docs/checklists/ai-errors.md', '''## 054 轮新增

| 编号 | 防错项 |
| --- | --- |
| A194 | 原文禁止网络打法时，信号白名单要**真的拒** `ip` / `geoip` / `vpn` / `asn` 等键，别只在文档写「不用」；出现即整份信号作废。 |
| A195 | 用户原文与我写的演示文案冲突时，以用户原文为准；演示文案的修正登记待办，等 UI 闸门触发的轮次再改，不偷偷改界面也不假装没冲突。 |
| A196 | 单一信号不做硬拒绝；两个独立信号一致才判区域，冲突与缺失走 Unknown 并放行，避免误伤。 |
| A197 | 限制范围只覆盖原文点名的对象（此处为离线账户），不擅自扩大到第三方登录或正版；未决断口径按最小范围执行并登记。 |
| A198 | 「离线」字段在不同模块口径不同：完整性验证离线不声明、自动关闭功能离线仍声明标内置、账户限制离线不参与判定，三条互不套用。 |
| A199 | 反向注入的 FAILED 数量按实记录，防护只有一条专属断言时就是 1 个 FAILED，不为凑数补测试。 |
''')

app('docs/rules/ui-demo.md', '''## 054 闸门判定

**未触发**。本轮新增 `src/core/region.rs` 与 `demos/round-054-region.html`（**流程 HTML，不是 UX HTML**）、功能登记、调研与文档。`demos/ui-full-kcu-paper.html`、两个语言包、56 张 PNG 全部零 diff。B08 的拒绝声明目前在判定层生成 `RegionNotice`（语义 key + 三动作），**未接演示层按钮、未渲染到任何界面**；动到那层才按闸门规则出整页演示与预览图。演示层 `t.0409`「仅下载选择，不复用为地区禁用」与 B08 用户原文冲突，登记 D-054-2，修正排队等 UI 闸门。
''')

app('docs/records/code-ownership-audit.md', '''## 054 零新增第三方

`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。新增 `src/core/region.rs` 的边界与限流、LRU 缓存、信封、取消、诊断、JSON 载荷全部复用已进构建的库；项目侧只有信号白名单、BCP-47 区域段提取、判定顺序、声明映射，**不是新开自写底座例外**（023 A03 已于 024 撤回）。`cargo test --offline --lib` 351 / 0，全量 377 / 0。
''')

app('docs/design/implementation-strategy.md', '''## 054 境外离线账户限制状态

| 项 | 状态 |
| --- | --- |
| 原文第 7 行 6 条约束、双信号防误伤、禁用键白名单、fail-open | **已落地（054）**：`src/core/region.rs`，零新增依赖 |
| 可关声明三动作、判定缓存与 `refresh()`、取消 0 副作用 | 已落地 |
| 独立链不读写 `download_region`、`offline` 不参与判定 | 已落地 |
| 真实网络 IO、特殊版标识注入、GUI 接线、Win7 声明文案 | 未启动（D07） |
| 演示层 `t.0409` 口径修正 | 未启动（等 UI 闸门，D-054-2） |
''')

p = Path('docs/index.md')
t = p.read_text()
a = '275. src/core/feature_gate.rs\n\n读取命令：'
if a in t:
    t = t.replace(a, '''275. src/core/feature_gate.rs
276. docs/spec/54-round-054-instructions.txt
277. docs/records/round-054-full-readback.md
278. docs/research/22-region-signals.md
279. docs/decisions/054-region-offline-restriction.md
280. docs/features/region-offline-restriction.md
281. docs/verification/round-054.md
282. src/core/region.rs

读取命令：''', 1)
    t = t.replace('docs/verification/round-053.md src/core/feature_gate.rs; do printf',
                  'docs/verification/round-053.md src/core/feature_gate.rs docs/spec/54-round-054-instructions.txt docs/records/round-054-full-readback.md docs/research/22-region-signals.md docs/decisions/054-region-offline-restriction.md docs/features/region-offline-restriction.md docs/verification/round-054.md src/core/region.rs; do printf', 1)
    p.write_text(t); print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 054 |', p.read_text(), count=1)
sec = f'''

## 054 境外离线账户限制判定层（B08）

`src/core/region.rs`：原文第 7 行 6 条约束分别落地；只用宿主注入的 locale / timezone 本地信号，**双信号一致才判境外**，单一或冲突信号一律放行；`ip` / `geoip` / `vpn` / `asn` 等 16 类键出现即整份作废；特殊版豁免、正版后正常、大陆恢复、用户覆盖排第一；只限制离线账户的登录与注册，不扩大到第三方与正版；每处拒绝一条可关声明与三动作。**不读写 `config.download_region`**，两条链分开。

`cargo test --offline --lib` **351 / 0**，全量 **377 / 0**，Windows GNU 交叉检查通过，四守卫零命中，双向反向注入 5 + 1 FAILED、恢复后 351 / 0。零新增依赖，仍 **{pkgs} 包 / {third} 第三方**。UI 闸门未触发，UX HTML 与 {png_n} 张 PNG 零 diff。
'''
if '## 054 境外离线账户限制判定层' not in t:
    p.write_text(t.rstrip() + sec); print('README_OK')
else:
    p.write_text(t); print('README_SKIP_DUP')

app('docs/records/rounds.md', f'''## 054

| 落点 | 内容 |
| --- | --- |
| docs/spec/54-round-054-instructions.txt | 逐字副本：「干」 |
| docs/records/round-054-full-readback.md | B02 复读证据：5 份字节 / 行 / SHA-256；开服器原文 64 行全文回显 |
| docs/research/22-region-signals.md | 统一调研：3 组关键词 9 条，采用 5 条 / 不采用 4 条，完整 URL 与一手原句 |
| docs/decisions/054-region-offline-restriction.md | U143–U155、V1–V19、E115–E119、三轮迭代与自评 9.4、四值 |
| docs/verification/round-054.md | 25 条复跑证据 |
| docs/features/region-offline-restriction.md | F054-01 五字段登记、6 条原文约束、输入信号、防误伤、独立链、离线口径分层、未启动项 |
| src/core/region.rs | **主交付**：{region_lines} 行，B08 判定层 |
| src/core/mod.rs | 注册 `pub mod region;` |
| demos/round-054-region.html | 运行逻辑演示（21 步可点，非整页 UX HTML） |
| 索引与记录 | docs/index 282 项、README、decisions/index、requirement-compliance-audit、pending-question-environments、interface-log I90–I93、ai-errors A194–A199、code-ownership-audit、implementation-strategy、ui-demo 闸门判定 |

053 结尾写「B06 三项的判定层已齐，剩下全在 D07 实现层……真实网络 IO 需 EQ-01 / EQ-03 拍板；或用户点 EQ-01 ~ EQ-13 任一编号」。用户回「干」，未点编号；按 050 的 A177 继续走 048 核对表剩余 B 类偏差，选 **B08**：明确原文、不碰真实网络 IO（原文反而禁止网络打法）、不碰 UI 闸门，登记 **D-054-1**（我的默认，不是用户决断）。

**B02**：对 5 份原文执行全文 `read_text()` 与逐行遍历；`docs/spec/12-server-features-input.txt` 4970 B / 64 行 / `03a62d90a2325fdf` **全文回显**（开服器功能原文，此前从未逐行打印）。`ai-errors.md` 本轮 36208 B / 385 行（053 追加 A188–A193 所致）。复读在写任何代码之前完成。

**E115（复读发现的真实边界）**：`src/core/config.rs` 早有 `region_override` / `set_download_region("overseas")` / `download_region()` 与测试 `region_override_only_exposed_for_download_selection`；演示层 `t.0409` 写着「仅下载选择，不复用为地区禁用」。B08 是**用户原文**，要求账户登录/注册的地域限制，不能被我自己写的演示文案压过。处置：新建独立 `signals` 链、**不读写 `download_region`**；`t.0409` 修正登记 **D-054-2**，等 UI 闸门触发的轮次再改，本轮不动演示。

**统一调研**：3 组关键词 9 条结果，采用 R01 Microsoft Learn BCP-47 区域子标签、R02 MSDN `GetUserDefaultLocaleName` 本地偏好性质、R03 ProxyWhereabouts「IP geolocation is an inference, not a measurement」、R04 GeoIPHub「One signal should never trigger a hard block」、R05 tsight.io「Locale 不等于国家」；不采用 IP2Location 商业页（正是原文禁止的网络打法）、kakunin-ip.click 词条（与 R03/R04 重复）、CSDN `setlocale` 实验博客、bcp47.antfu.me 工具页。完整 URL 与一手原句在 `docs/research/22-region-signals.md`。未证实：Windows `LOCALE_SCOUNTRY` 官方原文、IANA 时区权威映射、「物理位置」精确定义、特殊版标识注入方式。

**落地**：原文第 7 行拆 6 条独立规则；`ALLOWED_SIGNAL_KEYS` 8 键 / `FORBIDDEN_SIGNAL_KEYS` 16 类（10 类网络探测 + 6 类凭据地址），任一禁用键出现即整份作废；`region_subtag()` 取 BCP-47 区域段，不实现完整解析器；**locale 明确非 CN 且时区明确非大陆，两信号一致才判 Outside**；单一 / 冲突 / 缺失 → `Unknown` 放行；优先级 `special_build` > `user_override` > `authenticated` > Mainland 恢复 > 账户动作范围；`account=offline` 且 `action∈{{login,register}}` 且 Outside → 拒绝 + 可关声明（三动作：改用正版 / 手动指定地区 / 取消）+ 单行 `[KCU]` 诊断；`third_party` / `mojang` 不扩大（D-054-2）；缓存 128 / TTL30 / `refresh()` 全清；取消 0 副作用、限流不误禁；`offline` 键显式不参与判定，信封带 `network_probe=0`；`diagnostic_payload()` 不带原始信号。**零新增第三方**，`Cargo.toml` / `Cargo.lock` / `vendor/` 未动，仍 {pkgs} 包 / {third} 第三方。

**离线口径三层分开**：052/053 完整性验证「离线不声明」、053 自动关闭功能「离线仍声明但标内置」、054 账户限制「offline 不参与判定」，三条互不套用。

**三轮真迭代与自评**：8.3（只做境外禁离线，漏禁网络打法 / 既有口径 / 双信号 / 三条豁免）→ 8.9（补禁用键白名单、fail-open、声明三动作、缓存刷新、取消限流）→ **9.4**（补 64 行全文回显、调研一手原句与不采用项、双向反向注入、离线口径分层）。未给满分：真实网络 IO / GUI 接线 / 特殊版标识注入未启动；「物理位置」精确定义与 IANA 映射未证实；`t.0409` 演示文案按闸门规则留到动界面的轮次。

本轮真实问题：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E115 | B02 复读发现 `config.download_region` 与 `t.0409` 既有口径和 B08 原文冲突 | 独立链 + D-054-2，本轮不改演示 |
| E116 | `RegionInput` derive `Debug` 因 `CancelToken` 无 `Debug` 触发 E0277（与 053 E110 同类） | 去掉 `Debug` derive，不动 027 模块 |
| E117 | 未用导入 `MAX_TEXT_BYTES` 与 `Signals.offline` dead_code | 删导入；`offline` 改为允许键但显式不参与判定，零 warning |
| E118 | 反向注入 A 5 FAILED、B 1 FAILED | 按实记录，不凑数 |
| E119 | 综合验证命令被网关 502 截断（与 053 E114 同类） | 拆单条短命令重跑补齐，未降验收项 |

**验证**：`cargo test --offline --lib core::region` 20 / 0；`cargo test --offline --lib` **351 / 0**（331 + 20，零 warning）；`http_construct` 7 / 0、`window_handle_contract` 6 / 0、`plugin_lifecycle_load` 7 / 0（29.57 s 真加载 cdylib）、`plugin_abi_load` 6 / 0（77.67 s）；全量 **377 / 0**；Windows GNU 交叉检查通过（16.03 s）；panic / semver / i18n / lang 四守卫零命中（`files 41 hits 0`、`version_files 4 hits 0`、`rs_files 41`、`keys 26`）；`P09_HITS 0`；CI 三条 `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE`；{html_n} 份 demos HTML `node new Function` 全通过；`yaml.safe_load` scan 8 steps；反向注入 5 + 1 FAILED → 恢复 351 / 0。UI 闸门**未触发**：UX HTML、两语言包、{png_n} 张 PNG 零 diff。

**四值**：B02 复读、E115 边界发现、B08 判定层、351 / 0、377 / 0、零新增依赖 = 已证实；B01 / B02 历史缺失、`t.0409` 口径差异 = 已失败 / 已登记（不补写）；真实网络 IO / GUI 接线 / 特殊版标识注入 / Win7 声明文案 = 未启动；EQ-01 ~ EQ-13 拍板 / 物理位置定义 / IANA 映射 = 未证实；GUI 端到端 / Win7 与 MSVC 运行时 = 受阻。独立验证「部分通过」，**未发通过标记**。

**下一步**：B 类剩余 B04（UI 框架）/ B05（HMCL 代码）/ B07（插件独立进程）/ B09（32 位）/ B10（完全无法失误），以及 D07 实现层，均需 EQ-01 / EQ-03 的 Win7 TLS 与 UI 宿主口径拍板；或用户点 EQ 任一编号。
''', '## 054\n')
print('ALL_DOCS_OK')

# 境外离线账户登录/注册限制（B08）

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

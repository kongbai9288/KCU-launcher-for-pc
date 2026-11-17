# 境外离线账户限制：本地区域信号与误伤防护调研

| 项 | 值 |
| --- | --- |
| 轮次 | 054 |
| 主题 | B08：原文第 7 行「物理位置」如何在不走网络打法的前提下判定 |
| 检索 | 3 组关键词，返回 9 条；采用 5 条，不采用 4 条 |
| 口径 | 结论只取检索返回正文原句；URL 写完整，不写裸域名短名，不写「同上」 |

## 采用的一手资料

### R01 BCP-47 区域子标签

- URL：https://learn.microsoft.com/en-us/globalization/locale/standard-locale-names
- 正文要点：「IETF BCP 47 is the standard that defines the most-commonly used format for specifying a locale.」表格列「ISO 3166-1 alpha-2 region subtag OR UN M49 region subtag / 2 letters or 3 digits, respectively / Recommended: UPPERCASE」；示例 `zh-yue-HK`（Cantonese for Hong Kong SAR）、`de-AT`、`ca-ES-valencia`、`de-DE-u-co-phonebk`；并写明「Region subtags have changed as well.」
- 落地：`region_subtag()` 只取第一个 2 字母大写或 3 位数字的子标签，跳过主语言、3 字母 extlang、4 字母 script（`Hans`）、单字母 extension（`u`）与小写变体（`co`）。`zh-Hans-CN` → `CN`、`de-DE-u-co-phonebk` → `DE`、`sr-Latn-001` → `001`。**不实现完整 BCP-47 解析器**（避免自写通用解析器），只做形状校验 + 区域子标签提取。
- 状态：已证实（Microsoft Learn 正文可检索）。

### R02 Windows 用户默认区域是本地偏好，不是地理事实

- URL：https://msdn.microsoft.com/zh-cn/data/dd318136
- 正文要点：「Retrieves the user default locale name.」「The application should call this function in preference to GetUserDefaultLCID if designed to run only on Windows Vista and later.」「This function can retrieve data from custom locales. Data is not guaranteed to be the same from computer to computer or between runs of an application.」「If your application must persist or transmit data, see Using Persistent Locale Data.」
- 落地：区域、时区全部由宿主注入 `signals`，本模块不调用任何系统 API、不缓存跨运行结论；用户显式 `user_override` 排在信号判定之前（对应「偏好协商 + 显式设置优先」）。
- 状态：已证实（MSDN 中文页正文可检索）；该页只说明本地区域名的性质，不提供「物理位置」判定方法，不作为地理结论来源。

### R03 IP 定位是推断而非测量

- URL：https://proxywhereabouts.com/guides-location-inaccuracy.html
- 正文要点：「IP geolocation is an inference, not a measurement.」「When traffic exits through a VPN or proxy, geolocation reflects the exit node's region, not the user's physical location.」「Detections are probabilistic and should be communicated with caveats.」「Use as a coarse signal」「Provide fallbacks」「offer appeals for misclassification」。
- 落地：`FORBIDDEN_SIGNAL_KEYS` 拒 `ip` / `geoip` / `vpn` / `proxy` / `asn` / `isp` / `network_probe` / `latitude` / `longitude` / `country_by_ip`；任何受限结果都给可关声明与「手动指定地区」动作（对应 fallbacks / appeals）。
- 状态：已证实（该页正文可检索）；站点为代理检测服务商指南，只取局限性与解释规范，不取其产品结论。

### R04 硬拒绝的反复失败模式是过度阻断

- URL：https://geoiphub.com/blog/how-accurate-is-ip-geolocation
- 正文要点：「The recurring failure mode is over-blocking: hard-denying a user because an IP appears to be in the wrong city」「One signal should never trigger a hard block.」「design for uncertainty」「Use the Radius, Not the Pin」「Special-case mobile, CGNAT, and Private Relay」「country and region carry the decision; city is context, not evidence」。
- 落地：**双信号一致才判 Outside**；单一信号、冲突信号、缺信号一律 `Unknown → 不限制`；信号畸形 / 超长 / 禁用键 / 限流 / 取消一律 `allowed=true`；缓存只缓存「允许/拒绝」结论，输入变了由 `refresh()` 全清重跑。
- 状态：已证实（该页正文可检索）；文中 2026 年精度数值未取用，只取设计原则。

### R05 Locale 不等于国家

- URL：https://tsight.io/articles/13316429
- 正文要点：「将『Locale』与『国家』划等号是一种危险的简化」「Locale（本地化环境）是语言、文化习惯、数字格式、货币符号以及时区规则的集合体」「zh-Hans-CN 描述的是『中国大陆使用的简体中文』，而非仅仅是一个『中国』的地理标识」「基于 IP 或硬编码国家代码来推断用户偏好，往往会忽略海外华人群体或跨文化办公场景的复杂性」「应使用 Accept-Language HTTP 头作为首选信号，并结合用户 Profile 中的显式设置进行优先级降级」。
- 落地：`locale` 与 `timezone` 作为两个独立偏好信号；两者冲突即 Unknown；`user_override` 优先；不把 `zh-Hans-CN` 当 GPS 坐标。
- 状态：已证实（该页正文可检索）；中文技术文章，只取概念辨析，不取 Go 标准库实现细节。

## 不采用

| 来源 | 原因 |
| --- | --- |
| https://www.ip2location.com/#geolocation-banner | 商业 GeoIP 产品页，正文是「Accurate IP Geolocation and Proxy Detection」与自家数据库能力；正是原文第 7 行禁止的网络连接打法，不作设计依据。 |
| https://kakunin-ip.click/zh/glossary/geoip | GeoIP 词条，讲精度与「仅凭 GeoIP 结果做出重要决策（如拒绝访问）可能会错误地阻止合法用户」；与 R03 / R04 重复，且为商业站术语页，不重复引用。 |
| https://blog.csdn.net/snakepc12138/article/details/135372873 | `setlocale` / `GetLocaleInfoEx` 代码页实验博客；可作 Windows 本地信号的旁证，但正文是实验输出而非规范，不作结论来源。 |
| https://bcp47.antfu.me | 在线 BCP-47 解析工具页，只给 `zh-CN` → `zh-Hans-CN` 的解析示例；不作规范来源，规范以 R01 为准。 |

## 未证实 / 受阻

| 项 | 值 |
| --- | --- |
| Windows `GetLocaleInfoEx` + `LOCALE_SCOUNTRY` 官方原文 | 未证实；本轮只从 CSDN 转述看到，已列入不采用，不据其写死字段 |
| IANA 时区到地理区域的权威映射表 | 未证实；本模块只用 2 个大陆时区白名单，其余时区视为「非大陆」而非「境外证据」 |
| 原文「物理位置」的精确定义与可接受误差 | 未证实；原文只写结果要求与禁止项，未给判定口径 |
| 特殊版本如何标识、由谁注入 | 未证实；本模块只收 `special_build` 布尔，不写死版本名或仓库地址 |
| 真实网络 IO、GUI 端到端、Win7 / MSVC 运行时 | 受阻 / 未启动 |

## 与项目既有决断的关系

| 轮次 | 既有决断 | 054 处理 |
| --- | --- | --- |
| 050 | `config.rs::download_region` 只用于下载源选择；演示层 `t.0409` 写「仅下载选择，不复用为地区禁用」 | B08 是**用户原文**，不能被我写的演示文案压过；新建独立 `signals` 链，不读写 `download_region`。`t.0409` 需在动 UI 的轮次修正，登记 D-054-2，本轮 UI 闸门未触发故不改演示 |
| 053 | 输入全部由调用方注入；fail-open；`Notice` 三动作；缓存 + `refresh()`；`locale_tag` 只进诊断 | 同模式复用，不新增系统检测 |
| 049 | 切语言不改逻辑 | `locale_tag` 只进诊断行，不参与判定 |
| 048 | 文本 / id 边界与 `OpBudget` 限流 | 所有信号键与值过 `robust::check_text`，限流不误禁 |
| 036 / 052 / 053 | 签名与结论不缓存、离线口径分层 | 053 的「离线不声明」只属于软件完整性验证；本模块 `offline` 键显式不参与判定，两条口径不混用 |
| 023 / 024 | 上层用别人的代码，自写底座例外已撤回 | 零新增第三方，边界 / 缓存 / 信封 / 取消 / 诊断全复用已进构建的库 |

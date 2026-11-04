# 登录与认证

检索日期：2026-11-04

## Microsoft 设备码流

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 设备码端点 | `POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/devicecode` | 已证实 | learn.microsoft.com v2-oauth2-device-code |
| tenant | `common` / `consumers` / `organizations` | 已证实 | 同上 |
| 请求体 | `client_id`、`scope`，Content-Type: application/x-www-form-urlencoded | 已证实 | 同上 |
| 响应字段 | `device_code`、`user_code`、`verification_uri`、`expires_in`、`interval`、`message` | 已证实 | 同上 |
| 默认有效期 | `expires_in` 900 秒（15 分钟） | 已证实 | 同上 |
| 令牌端点 | `POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token` | 已证实 | 同上 |
| 令牌请求 | `grant_type=urn:ietf:params:oauth:grant-type:device_code`、`client_id`、`device_code` | 已证实 | 同上 |
| 令牌响应 | `access_token`、`refresh_token`、`expires_in` | 已证实 | 同上 |
| 轮询错误 | `authorization_pending`、`authorization_declined`、`bad_verification_code`、`expired_token` | 已证实 | 同上 |
| 轮询间隔 | 至少间隔 `interval` 秒 | 已证实 | 同上 |
| Xbox scope | `xboxlive.signin`、`xboxlive.offline_access` | 已证实 | devdocs.xbox.com 游戏网站 Xbox 登录 |
| 授权码兑换 | `POST https://login.microsoftonline.com/consumers/oauth2/v2.0/token`，含 `client_secret`、`grant_type=authorization_code` | 已证实 | devdocs.xbox.com |
| Azure Client ID 审批状态 | 未核实 | 未证实 | 一手资料未取得 |

## Xbox Live / XSTS / Minecraft Services

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| XBL 端点 | `POST https://user.auth.xboxlive.com/user/authenticate` | 已证实 | zh.minecraft.wiki/w/Mojang_API |
| XBL 请求 | `Properties.AuthMethod=RPS`、`SiteName=user.auth.xboxlive.com`、`RpsTicket=d=<access_token>`、`RelyingParty=http://auth.xboxlive.com`、`TokenType=JWT` | 已证实 | 同上 |
| XBL 响应 | `Token`、`IssueInstant`、`NotAfter`、`DisplayClaims.xui[].uhs` | 已证实 | 同上 |
| XSTS 端点 | `POST https://xsts.auth.xboxlive.com/xsts/authorize` | 已证实 | 同上 |
| XSTS 请求 | `SandboxId=RETAIL`、`UserTokens=[<XBL Token>]`、`RelyingParty=rp://api.minecraftservices.com/`、`TokenType=JWT` | 已证实 | 同上 |
| XSTS 失败 | HTTP 401 | 已证实 | 同上 |
| Minecraft 登录 | `POST https://api.minecraftservices.com/authentication/login_with_xbox`，`identityToken=XBL3.0 x=<uhs>;<XSTS Token>` | 已证实 | 同上 |
| 登录响应 | `access_token`、`token_type=Bearer`、`expires_in`、`username` | 已证实 | 同上 |
| 档案 | `GET https://api.minecraftservices.com/minecraft/profile`，Bearer 认证，返回 `id`、`name` | 已证实 | 同上 |
| 所有权 | `GET https://api.minecraftservices.com/entitlements/license?requestId=`，返回 `items` | 已证实 | 同上 |
| 缺令牌 | HTTP 401 | 已证实 | 同上 |
| Microsoft 官方规范原文 | 未取得端点级原文，以上为二手协议文档 | 部分已证实 | Minecraft Wiki |

## 离线与第三方

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 离线 UUID 规则 | 未取得官方 namespace/版本/字节序文档 | 未证实 | 禁止写死实现 |
| 旧 Mojang 账号当前状态 | 未核实 | 未证实 | 一手资料未取得 |
| authlib-injector 规范 | X-Authlib-Injector-API-Location 响应头做服务发现；根路径返回 `meta`、`skinDomains`、`signaturePublickey` | 已证实 | 规范检索片段 |
| Yggdrasil 路由 | `/authserver/authenticate`、`/authserver/refresh`、`/authserver/validate`、`/authserver/invalidate`、`/authserver/signout`、`/sessionserver/session/minecraft/join`、`/sessionserver/session/minecraft/hasJoined`、`/sessionserver/session/minecraft/profile/{uuid}` | 部分已证实 | 第三方实现路由表，非规范原文 |
| 规范原文抓取 | 失败 | 受阻 | github.com wiki 链接被安全审核拒绝 |
| Blessing Skin | PEM、RSA >= 4096 bit 私钥；`/api/yggdrasil` 验证；明文邮箱密码需 HTTPS；Let's Encrypt 需 Java >= 8u101 | 已证实 | blessing.netlify.app/yggdrasil-api/setup |
| 令牌存储保护 | 无头模式复用凭据需保护机制，具体方案未定 | 未证实 | 需求条目 |

来源：
- https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code
- https://devdocs.xbox.com/zh-CN/services/xbox-services/fundamentals/s2s-auth-calls/service-authentication/live-website-authentication
- https://zh.minecraft.wiki/w/Mojang_API
- https://blessing.netlify.app/yggdrasil-api/setup
- https://github.com/yushijinhun/authlib-injector/wiki/Yggdrasil服務端技術規範

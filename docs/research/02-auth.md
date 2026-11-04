# 登录与认证

检索日期：2026-11-05
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。

## Microsoft 设备码流

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 设备码端点 | POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/devicecode | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| tenant | common / consumers / organizations | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| 请求体 | client_id、scope，Content-Type: application/x-www-form-urlencoded | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| 响应字段 | device_code、user_code、verification_uri、expires_in、interval、message | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| 默认有效期 | expires_in 900 秒 | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| 令牌端点 | POST https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| 令牌请求 | grant_type=urn:ietf:params:oauth:grant-type:device_code、client_id、device_code | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| 令牌响应 | access_token、refresh_token、expires_in | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| 轮询错误 | authorization_pending、authorization_declined、bad_verification_code、expired_token | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| 轮询间隔 | 至少间隔 interval 秒 | 已证实 | https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code |
| Xbox scope | xboxlive.signin、xboxlive.offline_access | 已证实 | https://devdocs.xbox.com/zh-CN/services/xbox-services/fundamentals/s2s-auth-calls/service-authentication/live-website-authentication |
| Azure Client ID 审批状态 | 未核实 | 未证实 | 一手资料未取得 |

## Xbox Live / XSTS / Minecraft Services

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| XBL 端点 | POST https://user.auth.xboxlive.com/user/authenticate | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| XBL 请求 | Properties.AuthMethod=RPS、SiteName=user.auth.xboxlive.com、RpsTicket=d=<access_token>、RelyingParty=http://auth.xboxlive.com、TokenType=JWT | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| XBL 响应 | Token、IssueInstant、NotAfter、DisplayClaims.xui[].uhs | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| XSTS 端点 | POST https://xsts.auth.xboxlive.com/xsts/authorize | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| XSTS 请求 | SandboxId=RETAIL、UserTokens、RelyingParty=rp://api.minecraftservices.com/、TokenType=JWT | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| XSTS 失败 | HTTP 401 | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| Minecraft 登录 | POST https://api.minecraftservices.com/authentication/login_with_xbox，identityToken=XBL3.0 x=<uhs>;<XSTS Token> | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| 登录响应 | access_token、token_type=Bearer、expires_in、username | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| 档案 | GET https://api.minecraftservices.com/minecraft/profile，Bearer 认证，返回 id、name | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| 所有权 | GET https://api.minecraftservices.com/entitlements/license?requestId= | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| 缺令牌 | HTTP 401 | 已证实 | https://zh.minecraft.wiki/w/Mojang_API |
| 上述端点的 Mojang/Microsoft 一手原文 | 未取得 | 未证实 | https://zh.minecraft.wiki/w/Mojang_API |

## 离线与第三方

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 离线 UUID 算法 | MD5(UTF-8("OfflinePlayer:"+name))，置 version=3、variant=2 | 已证实 | cmd: python3 → OFFLINE_UUID 'Notch' b50ad385-829d-3141-a216-7e7d7539ba7f |
| 大小写敏感 | Notch → b50ad385…；notch → 42653081… | 已证实 | cmd: python3 → OFFLINE_UUID 'notch' 42653081-a90e-3475-b3d6-3550cdb43f8e |
| Notchian 服务端采用该算法 | 社区协议规范文本，未取得 Mojang 官方原文 | 未证实 | cmd: web_search "minecraft.wiki OfflinePlayer UUID v3 nameUUIDFromBytes offline mode protocol page" → web_doc 8 片段 |
| 旧 Mojang 账号当前状态 | 未核实 | 未证实 | 一手资料未取得 |
| authlib-injector 启动器技术规范 | 211 行，blob SHA-1 f466bf13dcce78a6bc1417c7f83b9d1bb03c85dd | 已证实 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src/zh/启动器技术规范.md |
| Yggdrasil 服务端技术规范 | 668 行，blob SHA-1 c0bab4ff3e938dfa75ab34f8f667843ebf6d0121 | 已证实 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src/zh/Yggdrasil-服务端技术规范.md |
| API Root | 启动器保存验证服务器 API 地址；URL 未标协议时补全为 HTTPS | 已证实 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src/zh/启动器技术规范.md |
| ALI 服务发现 | 响应头 X-Authlib-Injector-API-Location 指向 API 地址，可为绝对或相对 URL | 已证实 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src/zh/启动器技术规范.md |
| 元数据获取 | 启动前向 API 地址发 GET，响应 meta、skinDomains、signaturePublickey | 已证实 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src/zh/启动器技术规范.md |
| Yggdrasil 路由 | /authserver/authenticate、/refresh、/validate、/invalidate、/signout、/sessionserver/session/minecraft/join、/hasJoined、/profile/{uuid}、/api/profiles/minecraft | 已证实 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src/zh/Yggdrasil-服务端技术规范.md |
| 第三方认证头 | Authorization: Bearer {accessToken}；缺失或无效返回 401 | 已证实 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src/zh/Yggdrasil-服务端技术规范.md |
| 规范原文抓取 | 200，经 GitHub contents API | 已证实 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src |
| Blessing Skin | PEM、RSA >= 4096 bit 私钥；/api/yggdrasil；明文邮箱密码需 HTTPS | 已证实 | https://blessing.netlify.app/yggdrasil-api/setup |
| 令牌存储保护 | 无头模式复用凭据需保护机制，具体方案未定 | 未证实 | docs/spec/00-requirements.txt:17 |

## 005 补证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| GET /repos/yushijinhun/authlib-injector/contents/wiki/src | 200，SUMMARY.md、en、zh | 已证实 |
| GET /contents/wiki/src/zh/启动器技术规范.md | 200，211 行 | 已证实 |
| GET /contents/wiki/src/zh/Yggdrasil-服务端技术规范.md | 200，668 行 | 已证实 |

来源：
- https://learn.microsoft.com/zh-cn/entra/identity-platform/v2-oauth2-device-code
- https://zh.minecraft.wiki/w/Mojang_API
- https://api.github.com/repos/yushijinhun/authlib-injector/contents/wiki/src
- https://blessing.netlify.app/yggdrasil-api/setup

约束：
- 离线 UUID 算法不写进实现，直到 Notchian 服务端行为取得一手确认。
- 第三方登录凭据不写入日志与诊断包。

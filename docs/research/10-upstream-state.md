# 时间与上游状态

检索日期：2026-11-05
锚点格式：完整 URL 或 `cmd: <命令> → <输出>`；锚点逐行独立。

## 时间核实

| 来源 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 沙盒时钟 | Thu Nov 5 00:14:34 CST 2026 | 已证实 | cmd: TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y' → Thu Nov  5 00:14:34 CST 2026 |
| 网络时钟 | Wed, 04 Nov 2026 16:14:34 GMT | 已证实 | cmd: curl -sSI https://api.github.com/rate_limit → date: Wed, 04 Nov 2026 16:14:34 GMT |
| 时区换算 | GMT+8 = 2026-11-05 00:14:34 CST，与沙盒一致 | 已证实 | cmd: date 与 date 头比对 |
| 会话标注日期 | 2026-11-05 Thursday | 已证实 | 会话上下文 |
| HEAD /rate_limit | 404 | 已失败 | cmd: curl -I https://api.github.com/rate_limit → HTTP/2 404 |

## 上游版本状态

| 组件 | 最新值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| HMCL | v3.16.4，2026-09-17T04:30:46Z | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL/releases/latest |
| wry | wry-v0.57.1，2026-10-23T11:20:46Z | 已证实 | https://api.github.com/repos/tauri-apps/wry/releases/latest |
| rust | 1.99.1，2026-10-16T04:47:44Z | 已证实 | https://api.github.com/repos/rust-lang/rust/releases/latest |
| fabric-loader | 0.20.1，2026-10-19T19:02:45Z | 已证实 | https://api.github.com/repos/FabricMC/fabric-loader/releases/latest |
| quilt-loader | 0.31.0-beta.5（tags 首项） | 已证实 | https://api.github.com/repos/QuiltMC/quilt-loader/tags?per_page=1 |
| NeoForge | v99.99 占位 tag，不作版本依据 | 已证实 | https://api.github.com/repos/neoforged/NeoForge/tags?per_page=1 |
| labrinth | v2.4.3，2022-06-18T23:33:47Z | 已证实 | https://api.github.com/repos/modrinth/labrinth/releases/latest |
| QuiltMC/quilt-loader releases/latest | 404 Not Found | 已失败 | https://api.github.com/repos/QuiltMC/quilt-loader/releases/latest |
| neoforged/NeoForge releases/latest | 404 Not Found | 已失败 | https://api.github.com/repos/neoforged/NeoForge/releases/latest |
| HMCL 仓库最后推送 | 2026-11-04T14:23:24Z | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL |

## 网络边界

| 主机或入口 | 状态码 | 四值 | 锚点 |
| --- | --- | --- | --- |
| https://api.github.com/rate_limit | 200 | 已证实 | cmd: curl -H 'User-Agent: KCU-Launcher-Desktop/0.0.0' → 200 |
| https://github.com/kongbai9288/KCU-launcher-for-pc | 403 policy_default_denied | 受阻 | cmd: curl → 403 |
| https://github.com/kongbai9288/KCU-launcher-for-pc.git/info/refs | 403 policy_default_denied | 受阻 | cmd: curl → 403 |
| https://bmclapi2.bangbang93.com/ | 403 policy_default_denied | 受阻 | cmd: curl → 403 |
| https://api.modrinth.com/v3/ | 403 policy_default_denied | 受阻 | cmd: curl → 403 |
| https://meta.fabricmc.net/v2/versions/loader | 403 policy_default_denied | 受阻 | cmd: curl → 403 |
| https://meta.quiltmc.org/v3/versions/loader | 403 policy_default_denied | 受阻 | cmd: curl → 403 |
| https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml | 403 policy_default_denied | 受阻 | cmd: curl → 403 |
| https://static.rust-lang.org/dist/channel-rust-stable.toml | 403 policy_default_denied | 受阻 | cmd: curl → 403 |
| https://docs.github.com/en/rest/about-the-rest-api/api-versions | 安全审核拒绝 | 受阻 | cmd: web_fetch → ok=false |
| https://wiki.vg/RCON | 无法获取 | 受阻 | cmd: web_fetch → ok=false |
| https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution | 200 | 已证实 | cmd: web_fetch → EVIDENCE |
| https://minecraft.wiki/w/Server.properties | 200 | 已证实 | cmd: web_fetch → EVIDENCE |
| https://minecraft.wiki/w/RCON | 200 | 已证实 | cmd: web_fetch → EVIDENCE |
| https://www.rfc-editor.org/rfc/rfc6762 | 200 | 已证实 | cmd: web_fetch → EVIDENCE |
| https://www.rfc-editor.org/rfc/rfc6763 | 200 | 已证实 | cmd: web_fetch → EVIDENCE |
| https://www.rfc-editor.org/rfc/rfc6455 | 200 | 已证实 | cmd: web_fetch → EVIDENCE |

## 工具链

| 项 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| rustc | command not found | 受阻 | cmd: rustc --version → command not found |
| cargo | command not found | 受阻 | cmd: cargo --version → command not found |
| python3 | 3.10.19 | 已证实 | cmd: python3 --version |
| node | 可用 | 已证实 | cmd: node -e "new Function(...)" → JS_SYNTAX_OK |

## 约束

| 编号 | 约束 |
| --- | --- |
| U01 | 每轮开工执行时间戳命令并用 HTTP Date 头核对。 |
| U02 | 403 policy_default_denied 记为检查受阻，不记为上游服务异常。 |
| U03 | 占位 tag 不写进实现。 |
| U04 | rustc / cargo 缺失时 Rust 代码不进入构建验证。 |

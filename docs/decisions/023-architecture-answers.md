# 第 023 轮：六项质疑的正面答复与实现路线

| 项 | 值 |
| --- | --- |
| 编号 | 023 |
| 状态 | 已批准（设计层）；实现层未启动 |
| 逐字指令 | docs/spec/23-round-023-instructions.txt |
| 前序 | 021-server-autoconnect.md、022-async-budget.md、020-nav-slots-settings.md、013-build-start.md D07 |
| 本轮性质 | 质疑答复轮；承认三处偏差，给出可落地的库映射与层边界 |

## 先认三处

| 编号 | 偏差 | 处置 |
| --- | --- | --- |
| A01 | 用显示名当目录键的风险真实存在。022 的列表用内部编号 `s1..s9`，但设计文字没写死「名称不进路径」，实现时极易顺手拿 `name` 拼目录 | 023 定死 ID / 显示名 / 路径三者分离，见 `docs/design/stable-identity.md` |
| A02 | UX HTML 里中文文案大量 inline 硬编码，英文切换一开始只覆盖导航与按钮 | 023 建立 key 机制并扩到 550+ 个标注点，界面文案一律走 `tr()`；实现层用 `.ftl` 后源码零文案 |
| A03 | L1 core、L2 dispatcher、L3 lightweight 用纯 std 手写，与 020「上层实现都用别人的代码」不一致 | **该处置在 024 撤回**：底座例外属自我授权、未经用户批准，见 docs/decisions/024-code-ownership.md W01 |

## 六问逐条答复

### Q1 同名会污染目录

**会，已修。** `servers.dat` 里 `name` 是玩家自定义、可重复、无唯一 ID 字段（R14 / R15）。023 起：

| 概念 | 值 | 可变性 | 用途 |
| --- | --- | --- | --- |
| `sid` | `UUIDv5(KCU_NAMESPACE, normalize(ip:port))`，形如 `sv-2101b6d4` | 不变 | 目录名、缓存键、连接记录主键、双击进服绑定 |
| `name` | 玩家起的名字 | 随时可改 | 只作显示 |
| 目录 | `C:\KCU\servers\<sid>\` | 不随改名变 | 图标、延迟、失败历史、实例绑定 |

同名允许；改名只改 `name`；大小写折叠、路径字符白名单 `[a-z0-9-]`；缓存按 `sid` 分片。演示里放了两台同名服务器（`40-servers-samenames.png`），各带「同名」标签、各自延迟与记录，改其中一台不影响另一台。

### Q2 i18n 打算用什么实现

**Project Fluent `.ftl` + `i18n-embed`（MIT）+ `fluent`（Apache-2.0 OR MIT）**，理由：FTL 原生处理复数 / 参数 / 变体，`i18n-embed` 提供系统语言探测、资源嵌入与 `fl!()` 编译期 key 检查，`fallback_language` 就是「缺资源不白屏」的一手机制（R01-R04）。

| 项 | 口径 |
| --- | --- |
| 资源 | `C:\KCU\i18n\<locale>\*.ftl`，按模块分 domain；插件可追加自己的 `.ftl` |
| key | 语义 id，如 `server.join.instance`；源码不留中文 |
| 选择 | 默认跟随系统区域设置，用户可在设置里覆盖；回退链 `zh-CN → en-US`，缺 key 显示兜底文案不显示 key 名 |
| 不翻译 | 日志、`[KCU]` 诊断行、统一信封、API 线格式保持英文，避免错误归因和插件协议被本地化 |
| 演示层 | 已建 `tr()` / `applyI18n()` / 语言切换，550+ 标注点，`41-i18n-en.png` 可见；中文暂作缺资源兜底文本，实现层搬进 `.ftl` 后删除 |
| 许可 | 关于页与 `THIRD-PARTY-NOTICES.md` 登记 fluent / i18n-embed 两组 |

**不自己造**：复数规则、CLDR、语言协商、RTL 全部交给库，不写字符串拼接。

### Q3 名字不能自定义吗

**能。** 每行名称旁有改名入口（`39-servers-rename.png`），弹窗可取消、ESC / × / 宿主关闭，确认后只写显示名，写诊断行 `sid unchanged=true`。同名、空格、特殊字符都允许；不允许的是把名字当路径。

### Q4 信号格下标具体延迟

**已加。** 五格信号条下面一行小字 `42 ms`（`38-servers-latency.png`），取本轮 ping 结果，等宽数字右对齐；连不上给「连不上」，不编数字。`srv-ver` 里原有的 `· 42 ms` 保留作版本行上下文，两处不冲突。

### Q5 崩溃分析系统

**接别人的，分四层**（R05-R11）：

| 层 | 库 | 许可 | 作用 |
| --- | --- | --- | --- |
| 捕获 | `sentry-minidump` | MIT | 独立进程写 minidump，主进程死了也能落盘 |
| 解析 | `minidump` / `minidump-processor` | MIT | 本地读 dump、出栈，不需联网 |
| 后端 | `sentry-native`（Breakpad BSD-3-Clause / Crashpad） | MIT | 跨平台 native crash 后端 |
| 上报 | Sentry Rust SDK | MIT | DSN 由用户填，服务端不打包 |

| 约束 | 值 |
| --- | --- |
| 默认 | 不记录；用户选「先问我，再发送」或「只留本地」 |
| 脱敏 | 默认抹掉服务器地址、聊天、玩家名、存档内容；用户可手动关 |
| 确认 | 发送前弹一次完整内容预览，可取消 |
| 路径 | `C:\KCU\diagnostics` |
| Win7 | sentry-native 官方矩阵写 Win10 以下「应支持但未自动测试」（R11），所以 Win7 降级为本地 dump + 手动导出，不假设云端上报可用 |
| 服务端许可 | Sentry Web 应用是 FSL-1.1-Apache-2.0、非 OSI（R07 / R08）；项目只用 MIT 的 SDK，自托管由用户自行部署 |
| 界面 | 设置 → 崩溃反馈（`42-settings-crash.png`），不写 DSN / minidump / SDK 这些工程词 |

### Q6 打算用什么方式实现那些功能

**分层映射，逐层引库，core 只认 trait。** 完整表在 `docs/design/implementation-strategy.md`，摘要：

| 层 | 现状 | 实现手段 |
| --- | --- | --- |
| L1 core | 已落地，纯 std，141 测试 | **保留**。无依赖、可离线测、Win7 Tier 3 友好；不塞第三方 |
| L2 dispatcher | 已落地，纯 std | 保留；任务 / 模式判定 / 统一信封不引库 |
| L3 lightweight | 已落地，纯 std 逻辑 | 保留逻辑；批量请求与缓存单飞已自测 |
| L4 headless | 未启动 | `serde` + `toml` 做配置；命令与信封沿用 core |
| L5 normal / UI | 演示层 43 视图，实现未进构建 | `tao` + `wry`（或 slint 三许可二选一，需先定授权）；Fluent 管文案；Lucide ISC 图标 |
| L6 网络 | 未实现 | `reqwest` + `tokio`，连接池 / 批量 / 超时 / 取消；Modrinth 批量 id 一次请求 |
| L7 崩溃 | 未实现 | 上面 Q5 四层 |
| L8 插件与更新 | 设计已定 | `libloading` + C ABI / 子进程隔离；更新器作为插件，签名校验不可禁用 |
| L9 构建部署 | 未实现 | Win7 `*-win7-windows-msvc` Tier 3 + build-std；多架构 i686 / x86_64 / aarch64 |

| 硬规则 | 内容 |
| --- | --- |
| H01 | 第三方库只在 L4+ 注入，core 通过 trait 拿能力，不直接依赖 crate |
| H02 | 每个库取得 LICENSE 全文、写进关于页七列表与 `THIRD-PARTY-NOTICES.md` 后才加进 Cargo.toml；本轮 6 组全部标「候选 · 未进构建」 |
| H03 | 插件只能往 `slot:plugin.*` 追加；`core.locked.settings` / `core.locked.about` 固定不动 |
| H04 | 更新只换插件包，核心二进制不动；签名校验不可禁用，失败保留旧插件 |
| H05 | 手感确认前不写 UI 实现；演示 → 截图 → 用户点头 → 实现 |
| H06 | 后端仓 0 个写请求；凭据只从环境变量读 |

## 本轮落地

| 落点 | 内容 |
| --- | --- |
| UX HTML | i18n 字典与语言切换、550+ 标注点、稳定 `sid`、同名两项、改名弹窗、信号格延迟小字、崩溃反馈设置分组、许可表新增 6 组候选 |
| 截图 | 43 张产品视图 + 4 张内部证据图 + 总览，共 48 张 PNG |
| 文档 | `docs/research/20-i18n-crash-identity.md`、`docs/design/stable-identity.md`、`docs/design/i18n-policy.md`、`docs/design/crash-reporting.md`、`docs/design/implementation-strategy.md`、2 份功能 md、本决策 |
| 不变 | `src/` 与 Cargo.lock 无变化；L4 及以下未启动 |

## 待确认

| 编号 | 项 |
| --- | --- |
| Q01 | 「引入别人的崩溃分析系统」是否包含用户自建 Sentry 服务端；本轮按「只接 SDK」处理 |
| Q02 | UI 宿主选 tao+wry 还是 slint（三许可，商业授权需判定） |
| Q03 | Win7 的 TLS 栈（rustls 静态 / 系统 SChannel）与崩溃上报通道 |
| Q04 | 43 张图的手感反馈；反馈后先改演示，再进实现 |

## 四值

| 项 | 值 |
| --- | --- |
| 六项质疑逐条答复、43 视图、i18n 切换可见、同名与改名可见、延迟小字可见 | 已证实 |
| 库许可与官方矩阵、Win7 Tier 3、servers.dat 无 ID 字段 | 已证实 |
| 真实 minidump、真实 SLP、真实 Win7 构建、浏览器内点击、Fluent 运行时集成 | 受阻 |
| Q01-Q04、L4 及以下实现、LICENSE 全文取得 | 未证实 |

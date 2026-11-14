# i18n、崩溃分析、稳定标识与兼容性调研

| 项 | 值 |
| --- | --- |
| 轮次 | 023 |
| 依据 | docs/spec/23-round-023-instructions.txt；用户对目录污染、硬编码文案、i18n、自定义名称、延迟标注、崩溃分析、实现架构的六项质疑 |
| 来源数 | 18 个完整 URL 锚点 |
| 范围 | 只回答「用什么实现」，不写业务代码；`src/` 本轮无变化 |

## 一手来源

| 编号 | 来源 | 取到的事实 | 四值 |
| --- | --- | --- | --- |
| R01 | https://lib.rs/crates/fluent | `fluent` 是 Project Fluent 的 Rust 实现，许可证 `Apache-2.0 OR MIT`；`FluentBundle` + `FluentResource` 运行时解析 `.ftl`；FTL 支持复数、性别、变格等自然语言表达 | 已证实 |
| R02 | https://github.com/projectfluent/fluent-rs | fluent-rs 仓库同时含 LICENSE-APACHE 与 LICENSE-MIT；FTL 语法 `hello-user = Hello, { $username }!`；自然语言复杂度由语法承担 | 已证实 |
| R03 | https://lib.rs/crates/i18n-embed | MIT；`fluent-system` 与 `gettext-system` 两套后端；`desktop-requester` 用 `sys-locale` 读系统语言；`i18n.toml` 指定 `fallback_language`；资源目录 `i18n/{language}/{domain}.ftl`；`fl!()` 宏提供编译期 key 检查 | 已证实 |
| R04 | https://lib.rs/crates/embedded-i18n | MIT；编译期 i18n 把翻译变成 `&'static str`，缺 key 编译报错；对比表明确「桌面应用带可下载语言包、Fluent 全特性时，运行时库更合适」；复数 CLDR 40 种语言、locale 回退链 `fr-CA → fr → en` | 已证实 |
| R05 | https://sentry.io/changelog/rust-sdk-0493-native-crash-reporting-minidumps/ | Sentry Rust SDK 0.49.3 起原生崩溃上报：Linux / macOS / Windows 捕获 native crash（如段错误）为 minidump 并发送；panic 本来已上报；`minidump` feature + `MinidumpIntegration` 启用 | 已证实 |
| R06 | https://lib.rs/crates/sentry-minidump | MIT；独立崩溃报告进程：app 进程 spawn 一个 crash reporter 并持有句柄，reporter 进程不返回、自建 client 跑 minidump server；`crashes_dir` 可配；仅 Linux / macOS / Windows 构建；scope 变更不跨进程，要显式同步 | 已证实 |
| R07 | http://open.sentry.io/licensing | Sentry 官方许可说明：所有 SDK 用 MIT；新项目默认 Apache-2.0；**主 Web 应用用 FSL-1.1-Apache-2.0**，非 OSI 认证开源，两年后转 Apache-2.0 | 已证实 |
| R08 | https://wiki.licenseware.io/wiki/sentry-functional-source-license-and-self-hosted | FSL 允许内部自用、非商业教育研究，禁止把部署好的 Sentry 作为竞品对外售卖；SDK 与服务端许可分开 | 已证实 |
| R09 | https://www.lib.rs/crates/minidump | MIT；`Minidump::read_path` 只读本地 dump，`get_stream::<T>()` 按需解析流； richer stackwalk / symbolication 用 minidump-processor；纯解析不联网 | 已证实 |
| R10 | https://reverseengineering.wiki/index.php/Library:Breakpad | Google Breakpad 为 BSD-3-Clause；写 MDMP 格式 minidump，`dump_syms` / `minidump_stackwalk` 做符号化；Crashpad 在 Chromium 中接替 Breakpad；Sentry Native 可用 Breakpad 后端 | 已证实 |
| R11 | https://hysenlabs.com/projects/getsentry-sentry-native | sentry-native 为 MIT，CMake 构建，后端 Breakpad / Crashpad；官方支持矩阵写有「Windows 10 / Server 2016 以下版本应能支持但未自动测试，可能出问题」；Crashpad 后端与客户端 stackwalk 仅 Linux / Windows / macOS；HTTP transport 依赖 curl 或自实现 | 已证实（第三方对官方矩阵的整理） |
| R12 | https://blog.rust-lang.org/2024/02/26/Windows-7/ | Rust 1.78 起 Tier 1 Windows 目标最低为 Windows 10；新增 `x86_64-win7-windows-msvc` / `i686-win7-windows-msvc` 两个 Tier 3 目标 | 已证实 |
| R13 | https://doc.rust-lang.net.cn/rustc/platform-support/win7-windows-msvc.html | Tier 3；无预编译产物，需 `build-std` 或自编译 Rust；C 代码用 MSVC `cl.exe` 或 `clang-cl`；生成的二进制在 Wine / 原生 Windows 可跑 | 已证实 |
| R14 | https://zh.minecraft.wiki/w/Servers.dat格式 | `servers.dat` 是未压缩 NBT，根下 `servers` 列表每项含 `ip`（地址及端口）、`name`（玩家自定义名称）、`icon`、`hidden`、`acceptTextures`；**没有唯一 ID 字段**；可见 / 隐藏两份列表，隐藏最多 16 项 | 已证实 |
| R15 | https://minecraft.wiki/w/servers.dat_format | 与 R14 一致；`name` 是玩家定义的名字，允许格式化代码；文件位于启动器 profile 指定目录根 | 已证实 |

## 公开工程资料

| 编号 | 来源 | 取到的事实 | 四值 |
| --- | --- | --- | --- |
| C01 | https://wal.sh/research/2026-naming-for-isolation | 五种命名形态：lossy slug / slug+digest / digest only / reversible escape / assigned name；结论「名称只能当标签，要唯一就追加精确输入的摘要」；Windows / macOS 默认文件系统大小写不敏感，`Feat` 与 `feat` 会指向同一个目录；任何把用户名字拼进路径、shell、URL 的步骤都要当敌意输入处理 | 已证实 |
| C02 | https://blog.daryledesilva.com?p=505/ | 「Store Files by ID, Not by Slug」：存储路径用不可变 ID（ULID / UUID / 整数），可读名称只作 metadata；改名只改 `display_name`，下载链接与目录不动 | 已证实 |
| C03 | https://uuidgenerators.net/uuid-v5-generator | UUID v5 = SHA-1(namespace + name)，同一输入跨机器跨语言得到同一 ID；适合 URL / 文件路径 / 外部键做去重与幂等导入；不具保密性，不能当不可预测令牌 | 已证实 |
| C04 | https://bytebench.dev/guides/uuid-and-id-generation-guide | 稳定 ID 一旦签出不改；不要把业务语义编码进 ID；公开 ID 要稳定且不含敏感信息 | 已证实 |
| C05 | https://ask.csdn.net/questions/9262825 | rustup 1.26+ 起 Win7 被主动拒绝；Win7 原生 TLS 1.0，需 KB3045999 才有 TLS 1.2，缺 ALPN / SNI / OCSP，导致 reqwest 底层 HTTP 客户端初始化失败（社区问答，非官方文档） | 未证实 |
| C06 | https://lib.rs/crates/sentry-minidump 与 R11 交叉 | 崩溃捕获放独立进程，主进程崩溃时仍可写 dump；Win7 属「未自动测试」区间，不能直接假设可用 | 已证实 |

## 逐条对照用户质疑

| 用户质疑 | 对应事实 | 结论 |
| --- | --- | --- |
| 同名服务器会污染目录 | R14 / R15 证实 `servers.dat` 只有 `name` 与 `ip`，`name` 可重复且无 ID；C01 / C02 证实名称不能当路径键 | J01：显示名、稳定 ID、路径三者分离 |
| 文字还是硬编码 | R01-R04 给出运行时 `.ftl` 资源方案，源码只留 key | J02：实现层 Fluent + i18n-embed，源码零界面文案 |
| 名字不能自定义吗 | R14 的 `name` 本就是玩家定义字段 | J03：可改，且改名不动 ID |
| 崩溃分析系统 | R05-R11 给出 SDK / minidump / Breakpad / sentry-native 四层与各自许可 | J04：接成熟崩溃库，默认不外发 |
| 兼容性不好 | R12 / R13 的 Win7 Tier 3、R11 的「Win10 以下未自动测试」 | J05：Win7 走本地 dump + 用户确认，不假设云端可用 |
| 没按架构来 | 013-016 的 L1-L3 用纯 std 手写，与 020 D「上层用别人的代码」有偏差 | J06：core 保留，L4 起按库映射表注入，不再手写替代 |

## 结论

| 编号 | 结论 | 依据 |
| --- | --- | --- |
| J01 | `sid = UUIDv5(项目 namespace, normalize(ip:port))`；目录 `C:\KCU\servers\<sid>\`；`name` 只作显示，可重复、可改、不进路径；路径字符白名单 `[a-z0-9-]`，大小写折叠 | R14 / R15 / C01 / C02 / C03 / C04 |
| J02 | 实现层用 Project Fluent `.ftl` + `i18n-embed`（MIT）+ `fluent`（Apache-2.0 OR MIT）；语义 key、复数与参数由库处理；语言包放 `C:\KCU\i18n\<locale>\*.ftl`，插件可追加；默认跟随系统区域设置，用户可覆盖；缺 key 回退中文且不显示 key 名 | R01 / R02 / R03 / R04 |
| J03 | 日志、`[KCU]` 诊断行、统一信封保持英文线格式，不进 i18n 字典；界面文案才本地化 | R04 的 locale 回退链与工程惯例；023 自定口径 |
| J04 | 崩溃层接 `sentry-minidump`（MIT，独立进程）+ `minidump`（MIT，本地解析）+ `sentry-native`（MIT，Breakpad BSD-3 / Crashpad 后端）；DSN 由用户填写、默认不记录不外发、发送前可见内容与二次确认、脱敏默认开 | R05 / R06 / R07 / R08 / R09 / R10 / R11 |
| J05 | Win7 用 `x86_64-win7-windows-msvc` / `i686-win7-windows-msvc` + build-std；崩溃层在 Win7 未自动测试，降级为本地 minidump 落盘 + 用户手动导出；TLS 栈不在本轮拍板 | R11 / R12 / R13 / C05 |
| J06 | 服务端许可边界：只接 Sentry SDK（MIT），不把 Sentry Web 应用（FSL-1.1-Apache-2.0，非 OSI）打包进发行物；自托管由用户自己部署 | R07 / R08 |
| J07 | L1-L3 纯 std 保留作稳定底座；L4 起每个能力挂到一个成熟库，core 只认 trait；取得 LICENSE 全文后才进构建；关于页与 `THIRD-PARTY-NOTICES.md` 动态登记 | 020 D / 023 决策 |

## 口径说明

| 编号 | 项 | 我的理解 | 状态 |
| --- | --- | --- | --- |
| Q01 | 「引入别人的崩溃分析系统」 | 理解为接入第三方崩溃捕获 / 聚合 SDK 与本地 minidump 解析库，不是把整套服务端塞进启动器 | 未证实（设计决策） |
| Q02 | 「按我的架构」 | 理解为 D07 逐层 + 上层第三方库 + 插件化 + 设置关于锁定；L1-L3 的纯 std 属于底座例外，需明确登记 | 未证实（设计决策） |
| Q03 | 延迟数值单位 | 毫秒，取本轮 SLP ping 结果；无结果给「连不上」不编造数字 | 项目口径 |
| Q04 | 语言回退 | 缺资源回退 zh-CN；日志不翻译；RTL 由 Fluent 与宿主处理，不在本轮演示 | 项目口径 |

## 约束

| 编号 | 内容 |
| --- | --- |
| S01 | 所有新库标「候选 · 未进构建」，取得 LICENSE 全文并写进关于页后才引依赖。 |
| S02 | 崩溃上报默认关、脱敏默认开、发送前二次确认；不填接收地址只落本地。 |
| S03 | 同名服务器各自独立缓存、排序、连接记录；改名不触发重新探测、不移动目录。 |
| S04 | 演示层中文仍作缺资源兜底文本；实现层 `.ftl` 落地后源码不保留界面文案。 |
| S05 | 本轮结论只落设计层与演示层；真实 SLP、真实 minidump、真实 Win7 构建与浏览器内点击均未实测，标受阻。 |

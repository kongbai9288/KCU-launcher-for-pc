from pathlib import Path

D = {}

D['docs/design/stable-identity.md'] = '''# 稳定标识与目录隔离

| 项 | 值 |
| --- | --- |
| 轮次 | 023 |
| 状态 | 已批准（设计层） |
| 依据 | docs/research/20-i18n-crash-identity.md R14 / R15 / C01-C04；docs/decisions/023-architecture-answers.md Q1 |
| 取代 | 022 之前任何「按名称建目录 / 按名称做缓存键」的隐含口径 |

## 三种概念

| 概念 | 生成 | 可变 | 用途 | 禁止 |
| --- | --- | --- | --- | --- |
| `sid` | `UUIDv5(KCU_NAMESPACE, normalize(ip:port))` | 不变 | 目录名、缓存键、连接记录主键、双击绑定、插件引用 | 不暴露给玩家当名字；不含业务语义 |
| `name` | 玩家输入 / `servers.dat` 的 `name` | 随时可改、可重复 | 列表显示、搜索、推荐位文案 | 不拼路径、不拼 shell、不拼 URL、不做主键 |
| 目录 | `C:\\KCU\\servers\\<sid>\\` | 不随改名变 | 图标、延迟、失败历史、实例绑定、诊断快照 | 不含用户可控字符 |

`normalize(ip:port)`：去空白、域名小写、缺省端口补 25565、IPv6 用括号包裹、大小写折叠。命名空间 `KCU_NAMESPACE` 是项目固定 UUID，生成一次不再变（C03）。

## 路径规则

| 编号 | 约束 |
| --- | --- |
| P01 | 目录名只出 `[a-z0-9-]`；`sid` 本身已满足，任何插件拼接都要过同一白名单。 |
| P02 | Windows / macOS 默认大小写不敏感，`Feat` 与 `feat` 视为同一个目录（C01）；生成前统一小写。 |
| P03 | 不把 `name` 或 `ip` 原文直接当目录；`ip` 里有 `:` `.` `[` `]` 等路径敏感字符。 |
| P04 | 缓存分片 `C:\\KCU\\cache\\servers\\<sid>\\`，不按名称分片。 |
| P05 | 改名只写 `name` 字段，不移动目录、不重算权重、不触发重新探测。 |
| P06 | 同名服务器条目各自独立：`sid` 不同即不同实体；列表用「同名」标签提示，不合并、不去重。 |
| P07 | `servers.dat` 只读；启动器不写回游戏文件（021 D02）。隐藏列表条目同样按 `ip` 生成 `sid`。 |
| P08 | 重复导入同一地址时按 `sid` 幂等合并，不新建目录。 |

## 演示证据

| 文件 | 内容 |
| --- | --- |
| 40-servers-samenames.png | 两台同名服务器并列，各自延迟 / 记录 / 同名标签 |
| 39-servers-rename.png | 改名弹窗，改完 `sid unchanged=true` |
| 21-servers.png | 列表按 `sid` 渲染，显示名只作 label |

## 边界

| 项 | 值 |
| --- | --- |
| 已落地 | UX HTML 的 `sid` 字段、同名两项、改名交互、诊断行 |
| 未落地 | 真实 UUIDv5 计算、真实磁盘目录、真实 NBT 解析、`servers.dat` 回写冲突处理 |
| 四值 | 演示层已证实；真实文件系统行为标受阻 |
'''

D['docs/design/i18n-policy.md'] = '''# 界面文案与 i18n 策略

| 项 | 值 |
| --- | --- |
| 轮次 | 023 |
| 状态 | 已批准（设计层） |
| 依据 | docs/research/20-i18n-crash-identity.md R01-R04；docs/decisions/023-architecture-answers.md Q2 |

## 选型

| 组件 | 库 | 许可 | 职责 |
| --- | --- | --- | --- |
| 资源格式 | Project Fluent `.ftl` | 规范 | 复数、参数、变体、术语 |
| 运行时 | `fluent` | Apache-2.0 OR MIT | 解析与格式化 |
| 装载 | `i18n-embed` + `fl!()` | MIT | 资源嵌入、系统语言探测、编译期 key 检查、`fallback_language` |

编译期方案（`embedded-i18n`，MIT）适合无分配器固件；桌面带可下载语言包与完整 Fluent 特性时，R04 明确运行时库更合适，本项目不采用编译期方案。

## 资源与回退

| 项 | 口径 |
| --- | --- |
| 目录 | `C:\\KCU\\i18n\\<locale>\\<domain>.ftl` |
| key | 语义 id，如 `server.join.instance`；源码不保留中文 |
| 选择 | `DesktopLanguageRequester` 读系统区域设置；用户在设置 → 常规覆盖 |
| 回退 | `zh-CN → en-US`，缺 key 显示兜底文案，不显示 key 名、不空白 |
| 语言包 | 插件可追加自己的 `.ftl`；追加不改动核心 domain |
| 复数 / 性别 / 参数 | 交给 FTL 选择器，代码不拼字符串 |
| RTL | 交给 Fluent 与宿主布局，本轮不演示 |
| 不翻译 | 日志、`[KCU]` 诊断行、统一信封、API 线格式、错误码、第三方项目名 |

## 演示层与实现层的差别

| 项 | 演示层（023 已做） | 实现层（L5 待做） |
| --- | --- | --- |
| 文案存放 | HTML 元素里保留中文作缺资源兜底 | 全部搬进 `.ftl`，源码零文案 |
| key | 英文语义 key + 中文原文临时 key 并存 | 统一语义 id |
| 切换 | `tr()` / `applyI18n()` / `btnLang` / 设置下拉 | `i18n_embed::select()` + `fl!()` |
| 覆盖 | 550+ 标注点，41-i18n-en.png 可见 | 100% 界面文案 |
| 覆盖不全时 | 英文界面局部保留中文，如实标注 | 编译期 key 检查直接报错 |

## 用户逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 标题栏「中 / EN」 | 点一下 | 整页切换，不重启、不丢当前视图 |
| 设置 → 常规 → 界面语言 | 选 English | 同上，写盘失败保留旧值并可见报错 |
| 插件装了新语言包 | 自动出现 | 下拉多一项，缺 key 回退中文 |
| 语言包损坏 / 缺失 | 启动 | 回退中文，不白屏、不弹工程报错 |

## 边界

| 项 | 值 |
| --- | --- |
| 已落地 | 演示层字典、切换、550+ 标注点、41-i18n-en.png |
| 未落地 | 真实 `.ftl` 文件、`fl!()` 集成、插件语言包隔离、RTL 实测 |
| 四值 | 演示层已证实；运行时集成标受阻 |
'''

D['docs/design/crash-reporting.md'] = '''# 崩溃捕获与诊断策略

| 项 | 值 |
| --- | --- |
| 轮次 | 023 |
| 状态 | 已批准（设计层） |
| 依据 | docs/research/20-i18n-crash-identity.md R05-R11 / R12-R13 / C06；docs/decisions/023-architecture-answers.md Q5 |

## 分层

| 层 | 库 | 许可 | 职责 | 状态 |
| --- | --- | --- | --- | --- |
| 捕获 | `sentry-minidump` | MIT | 独立进程写 minidump，主进程崩溃仍可落盘 | 候选 · 未进构建 |
| 解析 | `minidump` / `minidump-processor` | MIT | 本地读 dump、出栈，不联网 | 候选 · 未进构建 |
| 后端 | `sentry-native` | MIT | Breakpad（BSD-3-Clause）/ Crashpad 跨平台后端 | 候选 · 未进构建 |
| 上报 | Sentry Rust SDK | MIT | 用户填 DSN 后才发 | 候选 · 未进构建 |
| 服务端 | Sentry self-hosted | FSL-1.1-Apache-2.0 | 用户自行部署，不打包进发行物 | 不引入 |

## 默认与开关

| 项 | 默认 | 可选 |
| --- | --- | --- |
| 记录 | 不记录 | 先问我再发送 / 只留本地 / 不记录 |
| 接收地址 | 空 | 用户自填；空则只落本地 |
| 脱敏 | 开 | 可手动关 |
| 发送确认 | 每次一次 | 不可禁用 |
| 诊断包 | `C:\\KCU\\diagnostics` | 只读展示 + 导出 |
| 保留 | 最近 N 份、容量有界 | 设置里可调 |

## 脱敏清单

| 类别 | 处理 |
| --- | --- |
| 服务器地址、端口、MOTD | 默认抹掉 |
| 玩家名、UUID、聊天 | 默认抹掉 |
| 存档内容、种子 | 不进包 |
| 凭据、令牌、DSN 本身 | 不进包 |
| 版本、系统版本、架构、窗口、崩溃前操作步骤、退出码 | 保留 |
| 崩溃前最近日志行 | 保留但过脱敏 |

## Win7 与多架构降级

| 平台 | 口径 |
| --- | --- |
| Win10+ / x86_64 / aarch64 | 四层全开，用户确认后上报 |
| Win7 Tier 3（build-std） | sentry-native 官方矩阵写 Win10 以下「应支持但未自动测试」（R11）；降级为本地 minidump 落盘 + 手动导出，不假设云端通道可用 |
| i686 | 同上，dump 本地落盘 |
| 无界面 / 轻量 | 不加载 UI；崩溃仍按同一策略落盘，不弹窗打断游戏 |

## 用户逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 设置 → 崩溃反馈 | 选「先问我，再发送」 | 出错后弹一次完整内容预览 |
| 预览弹窗 | 取消 / × / ESC | 0 外发、0 浮层残留 |
| 预览弹窗 | 确认 | 过脱敏后发送；失败保留本地 dump 并可见提示 |
| 看最近一次 / 导出诊断包 | 点击 | 只读展示或导出到用户选的位置 |
| 不填接收地址 | 直接出错 | 只落本地，状态显示「只留在本地」 |

## 与既有约束的衔接

| 编号 | 内容 |
| --- | --- |
| X01 | 013 的日志脱敏决策（mclo.gs 上传前脱敏）沿用同一脱敏器，不写第二套 |
| X02 | 诊断包不进公仓推送范围（`docs/rules/push-scope.md` 的 `diagnostic-*.zip` 排除项） |
| X03 | 崩溃库全部登记关于页七列表与 `THIRD-PARTY-NOTICES.md`；许可证全文取得前不引依赖 |
| X04 | 插件崩溃隔离在独立进程，不拖垮启动器（020 D） |

## 边界

| 项 | 值 |
| --- | --- |
| 已落地 | 设置分组、开关、脱敏口径、预览与导出交互、许可登记、42-settings-crash.png |
| 未落地 | 真实 minidump、真实上报、真实 Win7 构建、符号服务器 |
| 四值 | 设计层已证实；运行时标受阻 |
'''

D['docs/design/implementation-strategy.md'] = '''# 功能到实现的分层映射

| 项 | 值 |
| --- | --- |
| 轮次 | 023 |
| 状态 | 已批准（设计层）；实现层未启动 |
| 依据 | docs/decisions/023-architecture-answers.md Q6；013 D07 逐层顺序；020 上层第三方库约束 |

## 分层现状与手段

| 层 | 能力 | 现状 | 实现手段 | 依赖边界 |
| --- | --- | --- | --- | --- |
| L1 core | 缓存 / 异步 / 泄漏 / 用户流程 / 弹窗 | 已落地，纯 std，141 测试 | **保留纯 std** | 不引第三方 crate |
| L2 dispatcher | 任务 / JSON / 模式判定 / 统一信封 | 已落地，纯 std | 保留 | 不引 |
| L3 lightweight | 登录回退 / 批量拉取 / 加载器注册 / 极简视图逻辑 | 已落地，纯 std | 保留逻辑 | 视图渲染交给 L5 宿主 |
| L4 headless | 无界面调度、配置、命令 | 未启动 | `serde` + `toml`，配置读写；命令与信封沿用 core | L4 起允许引库 |
| L5 normal / UI | 43 个产品视图（演示层） | 实现未进构建 | `tao` + `wry`（或 slint，授权待定）；Fluent 管文案；Lucide ISC 图标 | 只走 `K08 UiFrame` |
| L6 网络 | 批量、镜像、超时、取消 | 未实现 | `reqwest` + `tokio`，连接池有界、批量 id 一次请求、CancelToken | core 只认 `NetProvider` trait |
| L7 崩溃 | 捕获 / 解析 / 上报 | 未实现 | Q5 四层库 | core 只认 `CrashSink` trait |
| L8 插件与更新 | 槽位、隔离、签名 | 设计已定 | `libloading` + C ABI / 子进程隔离；更新器作为插件 | 插件不碰 `core.locked.*` |
| L9 构建部署 | Win7 / 多架构 / 发行物 | 未实现 | `*-win7-windows-msvc` Tier 3 + build-std；i686 / x86_64 / aarch64 | CI 用腾讯 rustup 镜像 |

## 功能 → 库 → 许可证 → 状态

| 功能 | 库 | 许可证 | 状态 |
| --- | --- | --- | --- |
| 窗口与 WebView | tao / wry | Apache-2.0 / MIT（双） | 候选 · 未进构建 |
| 界面文案 | fluent / i18n-embed | Apache-2.0 OR MIT / MIT | 候选 · 未进构建 |
| 图标 | Lucide | ISC（Feather 派生 MIT） | 演示层已使用 |
| 配置序列化 | serde / toml | MIT OR Apache-2.0 / MIT OR Apache-2.0 | 候选 · 未进构建 |
| 网络与异步 | reqwest / tokio | MIT OR Apache-2.0 / MIT | 候选 · 未进构建 |
| 崩溃捕获 | sentry-minidump / minidump / sentry-native | MIT / MIT / MIT | 候选 · 未进构建 |
| 崩溃后端 | Breakpad | BSD-3-Clause | 候选 · 未进构建 |
| 稳定 ID | uuid | MIT OR Apache-2.0 | 候选 · 未进构建 |
| 错误与诊断 | anyhow / tracing | MIT OR Apache-2.0 / MIT | 候选 · 未进构建 |
| 插件装载 | libloading | ISC | 候选 · 未进构建 |
| 更新签名 | ed25519-dalek / minisign 方案 | BSD-3-Clause / MIT | 候选 · 未进构建 |
| 本地存储 | rusqlite（可选） | MIT | 候选 · 未进构建 |

## 硬规则

| 编号 | 内容 |
| --- | --- |
| H01 | 第三方只在 L4+ 注入；core 通过 trait 拿能力，不直接依赖 crate。 |
| H02 | LICENSE 全文 + 关于页七列表 + `THIRD-PARTY-NOTICES.md` 三处齐备后才加进 Cargo.toml。 |
| H03 | 插件加载后动态追加其项目名、许可证、作者、项目地址、修改后版本地址。 |
| H04 | 设置与关于锁定在 `core.locked.*`；插件只往 `slot:plugin.*` 追加。 |
| H05 | 更新只换插件包；核心二进制不动；签名校验不可禁用；失败保留旧插件可回滚。 |
| H06 | 手感回路：演示 → 截图 → 用户确认 → 实现；本轮 `src/` 与 Cargo.lock 无变化。 |
| H07 | 后端仓 0 写请求；凭据只从环境变量读；诊断包不进公仓。 |

## 不再手写的清单

| 能力 | 原做法 | 023 起 |
| --- | --- | --- |
| JSON 解析 | L2 手写递归下降 | core / dispatcher 保留（无依赖可测）；L4+ 业务 JSON 用 `serde_json` |
| 网络批量 | L3 手写批量演示 | 真实请求交给 reqwest 连接池与批量接口 |
| 复数 / 语言协商 | 演示层字典 | `.ftl` + `i18n-embed` |
| 原生崩溃栈 | 未做 | minidump 系列 |
| 插件 ABI | 未做 | C ABI + libloading / 子进程 |
| 窗口与渲染 | HTML 演示 | tao + wry |

## 交接口径

| 项 | 值 |
| --- | --- |
| 底座 | L1-L3 纯 std 已测，不动 |
| 下一层 | L4 headless；开工前需 Q02（UI 宿主授权）与手感反馈落定 |
| 新对话 | 读 `docs/index.md` 必读项 + `docs/design/handoff.md` 即可接上 |
| 未证实 | Q01-Q04、L4 以下实现、LICENSE 全文取得、真实 Win7 构建 |
'''


def fm(fid, title, frame, how, opened, reg, user, perf, verify):
    return f'''# {title}

| 项 | 值 |
| --- | --- |
| 编号 | {fid} |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 023 |
| 依据 | docs/decisions/023-architecture-answers.md；docs/research/20-i18n-crash-identity.md |

## 怎么运作

{how}

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `{frame}` |
| 输出 | 界面渲染、诊断行、截图证据 |
| 错误路径 | 缺资源回退中文；改名取消 0 副作用；崩溃上报取消 0 外发 |
| 空值 | 无服务器给添加入口；无 dump 给「看最近一次」空态 |
| 超时 | 单台 deadline 沿用 022 |
| 排除项 | 名称不进路径；日志不本地化 |

## 开放了什么

{opened}

## 登记框架

{reg}

## 用户使用逻辑

{user}

## 性能

{perf}

## 验证

{verify}
'''


D['docs/features/stable-identity-rename.md'] = fm(
    'F023-01', '稳定标识、同名与改名', 'ui.demo / servers.identity',
    '''每台服务器有不变的 `sid`（由规范化 `ip:port` 派生），显示名 `name` 可重复、可随时改。列表、缓存、连接记录、双击绑定全部按 `sid` 索引；目录 `C:\\KCU\\servers\\<sid>\\` 只含白名单字符。改名弹窗可取消 / ESC / × / 宿主关闭，确认后只写 `name`，写诊断行 `sid unchanged=true`，不移动目录、不重算权重、不触发重新探测。''',
    '''| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `srv.sid` | 字段 | `ip:port` | 稳定 ID | 地址冲突按 sid 幂等 |
| `openRename(s)` | 函数 | 服务器对象 | 改名弹窗 | 空名不保存 |
| `data-rename` | 按钮 | sid | 打开弹窗 | 无 |
| `data-lock` / `data-join` | 按钮 | sid | 锁定 / 进服 | 找不到 sid 忽略 |
| `srvNote(s)` | 函数 | 服务器对象 | 同名 / 范围外 / 连不上标签 | 无 |''',
    '''| 项 | 值 |
| --- | --- |
| 框架 | ui.demo / servers.identity（023 Q1） |
| 模块路径 | demos/ui-full-kcu-paper.html、docs/design/stable-identity.md、39-servers-rename.png、40-servers-samenames.png |
| 扩展点 | 插件可补服务器来源，必须产出同样规范的 sid |
| 关键抽象 | K03 Diagnostics、K08 UiFrame（未进实现） |
| 依赖 | 无新增 crate；UUIDv5 实现层用 uuid crate |
| 约束 | 名称不进路径；大小写折叠；路径字符白名单 |''',
    '''| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 服务器列表 | 看两台同名 | 各自独立，带「同名」标签 |
| 名称旁铅笔 | 改名 | 只换显示名，记录与排序保留 |
| 双击 | 进服 | 按 sid 绑定上次实例 |''',
    '''| 项 | 值 |
| --- | --- |
| 排序 | 一次 sort，按 sid 无关缓存权重 |
| 内存 | 每条只多一个短字符串 |
| 磁盘 | 每服务器一个目录，不随改名增长 |
| 测量命令 | `grep -c "sid:'sv-"` = 10 |
| 四值 | 已证实（演示层） |''',
    '''| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `39-servers-rename.png` | 改名弹窗与同名标签可见 | 已证实 |
| `40-servers-samenames.png` | 两台同名各自延迟 | 已证实 |
| 真实 UUIDv5 / 真实目录写盘 | 未实测 | 受阻 |''')

D['docs/features/i18n-crash-settings.md'] = fm(
    'F023-02', 'i18n 切换与崩溃反馈设置', 'ui.demo / i18n + settings.crash',
    '''界面文案统一走 `tr(key, fallback)`，中文在演示层作缺资源兜底；标题栏「中 / EN」与设置 → 常规 → 界面语言都能切，切换不重启、不丢当前视图、不白屏。日志与 `[KCU]` 诊断行保持英文线格式，不进字典。设置 → 崩溃反馈给出记录开关、接收地址、脱敏、诊断包位置、看最近一次、导出；默认不记录、脱敏开、发送前二次确认、不填地址只落本地。''',
    '''| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `tr(k, fb)` / `applyI18n()` | 函数 | key / 兜底 | 本地化文本 | 缺 key 回退 fb |
| `setLang(l)` / `btnLang` | 函数 / 按钮 | locale | 整页重渲染 | 无 |
| `setLang` 下拉 | 设置 | zh-CN / en-US | 同上 | 写盘失败保留旧值 |
| `setCrashOn` / `setCrashAddr` / `setCrashMask` | 设置 | 值 | 崩溃策略 | 无 |
| `crashView` / `crashExport` | 按钮 | 无 | 预览 / 本地导出 | 无 dump 给空态 |''',
    '''| 项 | 值 |
| --- | --- |
| 框架 | ui.demo / i18n、ui.demo / settings.crash（023 Q2 / Q5） |
| 模块路径 | demos/ui-full-kcu-paper.html、docs/design/i18n-policy.md、docs/design/crash-reporting.md、41-i18n-en.png、42-settings-crash.png |
| 扩展点 | 插件可追加 `.ftl` 语言包与崩溃上下文，不覆盖核心 domain |
| 关键抽象 | K03 Diagnostics、K08 UiFrame |
| 依赖 | 演示层无；实现层 fluent / i18n-embed / sentry-minidump 均为候选未进构建 |
| 约束 | 默认不外发；脱敏默认开；许可登记后进构建 |''',
    '''| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 标题栏 中 / EN | 点一下 | 整页切换 |
| 设置 → 常规 | 选 English | 同上 |
| 设置 → 崩溃反馈 | 选只留本地 | 出错只落盘 |
| 看最近一次 | 点击 | 只读预览，可取消 |''',
    '''| 项 | 值 |
| --- | --- |
| 切换 | 一次遍历 550+ 标注点，无网络请求 |
| 资源 | 演示层字典常驻；实现层 `.ftl` 按需装载 |
| 崩溃 | 默认 0 外发、0 常驻上报进程 |
| 测量命令 | `grep -c 'data-i18n='` 与 `node new Function` |
| 四值 | 已证实（演示层） |''',
    '''| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `41-i18n-en.png` | 导航 / 设置 / 按钮英文可见 | 已证实 |
| `42-settings-crash.png` | 崩溃反馈分组可见 | 已证实 |
| 真实 `.ftl` 集成、真实 minidump、真实上报 | 未实测 | 受阻 |''')

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f, len(c.splitlines()))

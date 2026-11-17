# 自动关闭功能：版本平台信息与设备能力判定调研

| 项 | 值 |
| --- | --- |
| 轮次 | 053 |
| 主题 | B06 第二项「自动关闭某一功能」的一手做法 |
| 检索 | 3 组关键词，返回 6 条；采用 4 条，不采用 2 条 |
| 口径 | 结论只取检索返回的正文原句；URL 写完整，不写裸域名短名，不写「同上」 |

## 采用的一手资料

### R01 签名快照与本地判定

- URL：https://z-soft.com.vn/blog/feature-flags-safe-rollout
- 正文要点：「Distribute signed snapshots and evaluate locally to avoid making a central flag service a request-path dependency.」「Flag evaluation failure has a documented fail-open or fail-closed default.」「Disconnect the flag control plane and verify local safe defaults.」「Every flag owner, creation date, expiry and safe default.」「Exercise every kill switch under representative load.」
- 落地：`GateInput` 注入策略字节 + 公钥 + 签名，`verify_detached`（036）本地验签；`BUILTIN_POLICY` 编译进模块，断开 / 签名不符 / 畸形一律回退且不关闭任何功能；每条策略带 `owner` / `expires` / `default`；`refresh()` 可重跑；限流态单测覆盖高频调用。
- 状态：已证实（该页正文可检索）；站点性质为技术博客，非标准规范，只作设计依据，不作规范引用。

### R02 四类开关、活跃上限与禁止项

- URL：https://propelius.tech/blogs/feature-flags-saas-release-management-best-practices
- 正文要点：「Operations Flags (Kill Switches): Instantly disable a feature or external dependency if it breaks.」「Cap Active Flags at 50-100」「Nested flags: if (flagA && flagB) creates exponential complexity」「Using flags for config: API URLs, DB creds belong in env vars, not flags」「CI check that fails if flag active >90 days without update」。
- 落地：`MAX_POLICY_ENTRIES=512`（本项目上限取更严的运行期边界，非照抄 50–100）；`FORBIDDEN_ENTRY_KEYS` 拒 `url` / `endpoint` / `token` / `key` / `secret` / `api` / `password` / `credential` / `depends_on`；条目单条独立判定、无嵌套依赖；`expires` 过期即忽略。
- 状态：已证实（该页正文可检索）；上限数值按本项目边界自定，登记为项目决断，不写成上游结论。

### R03 设备能力上下文键

- URL：http://vscode.net.cn/api/references/when-clause-contexts
- 正文要点：「Visual Studio Code 会根据 VS Code 用户界面中哪些元素是可见且活动的，来设置各种上下文键和特定的值。这些上下文可用于有选择地启用或禁用扩展命令以及菜单、视图等 UI 元素。」示例 `"when": "debuggersAvailable && !inDebugMode"`；逻辑运算符表列 `!` / `&&` / `||` 与优先级。
- 落地：`DeviceCaps.context` 是 `BTreeMap<String,bool>`，`requires` 列表要求全部为真才启用；**不实现 when 表达式解析器**（避免自写通用解析器），只做布尔键查表，表达式能力留在宿主侧。
- 状态：已证实（中文文档镜像正文可检索）；**官方原站 `https://code.visualstudio.com/api/references/when-clause-contexts` 本轮未取得正文**，标未证实，不据其写死字段。

### R04 启动器设置页与开关形态

- URL：https://minecraft.wiki/w/Minecraft_Launcher?oldid=3782896
- 正文要点：设置页含 General / Accounts / About 三页；「Use beta version of the Launcher (OFF)」「Keep the Launcher open while games are running (OFF)」「Animate transitions between pages in the Launcher (OFF)」等开关默认 OFF。
- 落地：作为「功能开关默认状态可见」的一般参考；本项目默认档位口径沿用 032 的严格默认，不照抄具体开关名。
- 状态：已证实（该页正文可检索）；仅作形态参考，不作行为依据。

## 不采用

| 来源 | 原因 |
| --- | --- |
| https://vscode.cool/ | 检索返回的是 VS Code 入门视频教程目录（调试技巧、logpoints、条件断点），与功能开关判定无关。 |
| Minecraft Wiki `Minecraft Launcher: Difference between revisions` | 检索结果标记不可展示，正文只给设置项列表片段，无法核对版本与上下文，不作为结论来源。 |

## 未证实 / 受阻

| 项 | 值 |
| --- | --- |
| VS Code 官方原站 when-clause 文档正文 | 未证实（本轮只取到中文镜像） |
| 平台版本信息的具体字段（GitHub / atomgit 仓库返回什么） | 未证实；原文第 12 行只写「需有版本平台等信息」，未给 schema |
| 真实网络 IO | 未启动；040 已核 reqwest / ureq / rustls 的 MSRV 与 Win7 TLS 前置，需 EQ-01 / EQ-03 拍板 |
| 平台策略签发与公钥分发流程 | 未启动 |
| GUI 端到端、Win7 / MSVC 运行时 | 受阻 |

## 与项目既有决断的关系

- 020：`core.locked.settings` / `core.locked.about` 位置锁定 → 本轮 `CORE_LOCKED` 永不关闭。
- 032：严格为默认、用户可选松档 → 本轮「评估失败一律不关」是同向的安全默认。
- 036 / 052：签名校验排在决策之前、不缓存结论 → 本轮验签排在解析之前。
- 034 / 047：版本相等用 `cmp_precedence`，不用 `==` → 本轮 `min_app` / `max_app` 同样处理。
- 049：切语言不改逻辑 → 本轮 `locale` 只进诊断行，不参与判定。
- 048：路径 / 文本边界 → 本轮 id / owner / requires / expires 全走 `robust::check_text`。

# 第 037 轮：身份哈希一致才升级 / 插件故障三动作 / 侧栏 SVG 与问号

| 项 | 值 |
| --- | --- |
| 编号 | 037 |
| 状态 | 业务层已实现已验证；**界面层仅演示，未进实现** |
| 依据 | docs/spec/37-round-037-instructions.txt |
| 前序 | 036-updater-signature-on-ed25519-compact.md、020 插件化更新约束、docs/rules/ui-demo.md |
| 本轮性质 | 双轨轮：业务层落地 + UI 闸门触发 |

## 三条需求与落点

| 编号 | 用户原话要点 | 业务层 | 界面层 |
| --- | --- | --- | --- |
| P01 | 两个插件哈希一致 → 比对版本 → 手动同意才能安装（叫升级） | `src/plugins/upgrade.rs` 已实现 | `demos/preview/50-plugin-upgrade.png` 演示，未进实现 |
| P02 | 插件有问题 → 报告弹窗 → 底部「禁用继续尝试启动 / 取消」 | `src/plugins/fault.rs` 已实现 | `demos/preview/51-plugin-fault.png` 演示，未进实现 |
| P03 | 插件自带 SVG 显示侧栏，没有用问号 | `src/plugins/icon.rs` 已实现 | `demos/preview/49-plugin-icons.png` 演示，未进实现 |

按 `docs/rules/ui-demo.md`：动用户界面的轮次先交整页 UX 演示与 PNG，**确认后才写实现**。本轮 `src/` 里落的是身份哈希、决策编排、数据层与弹窗注册表，不含任何渲染代码；侧栏视觉、两个弹窗的按钮布局都只在 `demos/ui-full-kcu-paper.html` 里。

## 口径解读（一处要你确认）

「两个插件的哈希值满足一致」按**插件身份哈希**实现：`sha512(plugin_id)` 取前 16 字节转 32 位小写 hex。理由：若指包内容哈希，两个包字节相同就不该有版本差异，也没有「升级」这件事；身份哈希一致才代表同一个插件的新旧两个版本。若你本意是包内容哈希，说一句我改，其余口径不动。

## P01 升级：撤回 036 的自动安装

036 的 U02 是「同插件新版本自动 Install」。本轮用户明确要求手动同意，按当轮指令优先覆盖：

| 编号 | 规则 | 与 036 关系 |
| --- | --- | --- |
| U08 | 签名校验仍排在最前且不可禁用，失败直接 Keep | 保留 U01 |
| U09 | 身份哈希不一致 / 没有已装版本 → 新插件安装，不叫升级 | 新增 |
| U10 | 身份哈希一致 + 候选版本更高 → **必须 `user_confirmed_upgrade`** 才 Install，否则 Keep | **覆盖 U02 的自动安装** |
| U11 | 同版本 / `+build` 差异 → Keep | 保留 U03 |
| U12 | 降级 → 显式目标 + 回滚确认 + 手动同意三者齐备才 Install | 在 U04 上再加一层 |
| U13 | 签名失败 / 版本串畸形 / 公钥截断 → Keep 或错误，不 panic、不覆盖旧插件 | 保留 U05/U06 |

版本比较继续走 034 的 `semver::cmp_precedence`，没重写比较器。

## P02 插件故障

| 编号 | 规则 |
| --- | --- |
| F01 | 报告内容含插件名与失败原因，弹窗标题「插件加载失败」。 |
| F02 | 底部两个动作：「禁用并继续尝试启动」「取消」。 |
| F03 | 禁用只从本次启动的活跃列表里移除该插件，其他插件照常加载，`retry_count + 1`。 |
| F04 | 取消中止启动、不写禁用集合；× / ESC 与「取消」等价。 |
| F05 | 所有插件都被禁用后 `should_continue()` 为 false，不再空转重试。 |
| F06 | 每个弹窗必可关、流程结束 0 残留：`PopupKind` 新增 `PluginUpgradeConfirm` / `PluginFault`，catalog 11 → **13 类**，`core/popup.rs` 与轻量视图的计数断言同步 13。 |

## P03 侧栏图标

| 编号 | 规则 |
| --- | --- |
| I01 | 插件提供 SVG → 直接在侧栏显示，颜色跟随主题（`currentColor`）。 |
| I02 | 没提供 / 空串 / 不是 `<svg` / 超过 16 KiB → 问号 `?`，虚线框 + 衬线字重，与 lucide 图标同宽 18px。 |
| I03 | 最小格式检查：拒 `<script` / `<foreignObject` / `<iframe` / `<image` 与 `onload` 等事件属性；`href` 只允许 `#` 内部片段，外链一律问号。 |
| I04 | **不做内容白名单**（按你之前「下载白名单先不要搞，留高度自定义」的口径）；渲染层用 `<img src="data:image/svg+xml">` 隔离，SVG 里的脚本不进 DOM 执行。 |
| I05 | `FALLBACK_GLYPH = "?"` 由库常量导出，界面不另写一份。 |

## 本轮依赖与许可

**零新增第三方 crate**。`Cargo.lock` 仍是 14 包 / 13 第三方；SHA-512 用已在构建中的 `ed25519-compact::sha512`（036 引入），版本比较用 `semver`（034），签名用 `updater::verify`（036）。关于页许可表仍 13 组 / 35，NOTICES 未变。

## 测试

`cargo build --offline` 通过；`cargo test --offline` **179 → 207 passed / 0 failed**，新增 28 个：

| 模块 | 数量 | 覆盖 |
| --- | --- | --- |
| `plugins/identity.rs` | 5 | 同 ID 同哈希、不同 ID、空 ID、hex 口径、UTF-8 |
| `plugins/upgrade.rs` | 9 | 需手动同意、不同身份新装、无已装、同版本、build 差异、降级三条件、签名失败、畸形串、截断公钥 |
| `plugins/fault.rs` | 6 | 报告与两动作、只禁用故障插件、取消不禁用、全禁用停止、×/ESC 映射、原因带出 |
| `plugins/icon.rs` | 8 | 缺失、空串、合法 SVG、非 SVG、脚本与事件、外链、超长、内部片段引用 |

## 本轮真实失败与修复

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E35 | `UpgradeRequest` derive `Default` 报 E0277（`Identity` 没有 Default） | 给 `Identity` 加 `Default`，默认空串只用于构造，不参与匹配 |
| E36 | 测试里 raw string `r#"<svg><use href="#i-puzzle"/></svg>"#` 被内部 `"#` 提前截断，报 3 处语法错 | 改 `r##"..."##` |
| E37 | 首版把 `href="#i-puzzle"` 也判成外链 | 改成遍历所有 `href="..."` 值，只放行 `#` 开头，外链仍问号 |
| E38 | 新增两类弹窗后 `lightweight/view.rs` 硬编码 11 的断言失败 | 同步 13，遍历式关闭逻辑未动 |
| E39 | 重渲后发现 `.modal` 半透明，背后设置卡片文字透进弹窗影响阅读 | `.modal` 改 `background:var(--paper-hi)`，深色主题单独给 `#323330`，51 张图全量重渲 |

## 四值

| 项 | 值 |
| --- | --- |
| 三条业务口径、207 / 0、零新增依赖、catalog 13 类 | 已证实 |
| 51 张预览图重渲、3 张新场景、整页 UX 可离线点 | 已证实 |
| 界面实现（侧栏渲染 / 弹窗组件） | **未启动**（等手感确认） |
| 「哈希」= 身份哈希这一解读 | 未证实（待你一句确认） |
| 插件包格式 / 公钥分发 / ABI 加载 / 真实运行时 / Win7 交叉编译 | 未证实 / 受阻 |
| 后端仓写请求 | 0（已证实） |
| E40 | 新增 `data-i18n="plugin.nav.*"` 等语义 key 落在标签属性里，被 P09 当成界面工程话命中 9 次 | `scripts/p09_scan.py` 在 findall 前剥掉 HTML 标签，只扫可见文本；断言与正则一字未改，注入自检 `core.locked.settings` 作为可见文本仍能命中，属性值不命中。属扫描域修正，未降标准 |

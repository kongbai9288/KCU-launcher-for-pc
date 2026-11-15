from pathlib import Path
import re

Path('docs/spec/37-round-037-instructions.txt').write_text(
    '干，就是我有个要求如果两个插件的哈系值满足一致，那么在对比版本号用户得手动同意才能安装（这叫升级），'
    '如果说插件本身有问题那我就直接报告弹窗，底下提示可以禁用继续尝试启动取消。'
    '插件可以自己提供svg以在侧边栏显示，如果没有，则用问号来表示。\n')
print('SPEC_OK')

D = {}

D['docs/decisions/037-plugin-upgrade-fault-icon.md'] = '''# 第 037 轮：身份哈希一致才升级 / 插件故障三动作 / 侧栏 SVG 与问号

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
'''

D['docs/verification/round-037.md'] = '''# 第 037 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 037 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 双轨轮，界面层仅演示；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile` | 已证实 |
| V2 | `cargo test --offline` | 207 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 14 包 / 13 第三方，与 036 一致 | 已证实 |
| V4 | `grep -c '#\\[test\\]' src/plugins/*.rs` | 28 | 已证实 |
| V5 | `grep -c 'user_confirmed_upgrade' src/plugins/upgrade.rs` | 3 | 已证实 |
| V6 | `grep -c 'assert_eq!(r.len(), 13)' src/core/popup.rs` | 1 | 已证实 |
| V7 | `grep -c 'plug-q' demos/ui-full-kcu-paper.html` | 2 | 已证实 |
| V8 | `node new Function` 整页 UX 脚本 | 通过 | 已证实 |
| V9 | `python3 scripts/render_ui.py` | 51 shots + overview | 已证实 |
| V10 | 三张新 PNG 目视复核 | 问号 / 升级按钮 / 故障三动作均可见 | 已证实 |
| V11 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V12 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V13 | 必读文件循环 | REQUIRED=181 MISSING=0 | 已证实 |
| V14 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 业务层三条口径与 207 / 0 | 已证实 |
| 界面实现 | 未启动（仅演示） |
| 身份哈希解读、插件包格式、公钥分发、ABI、Win7 | 未证实 / 受阻 |
| 207 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。
'''

D['docs/features/plugin-upgrade-consent.md'] = '''# F037-01 插件升级需手动同意

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | 已装插件与候选包各算身份哈希（`sha512(plugin_id)` 前 16 字节 hex）；一致才进版本比较。签名校验先过，再由 `semver::cmp_precedence` 判新旧；更高版本必须 `user_confirmed_upgrade` 才 Install。 |
| 开放了什么 | `src/plugins/identity.rs::identity_hash`、`src/plugins/upgrade.rs::decide_upgrade` / `UpgradeRequest` / `UpgradeDecision`；`src/plugins/mod.rs` 导出。 |
| 登记框架 | 挂在 `src/updater/` 之上（036 的签名校验与版本决策），不新增第三方 crate。 |
| 用户使用逻辑 | 两个包被认成同一个插件时弹「确认升级插件」，显示 1.2.3 → 1.3.0 与签名通过；点「升级」才装，「暂不升级」/ × / Esc 都保留旧插件。降级仍需显式目标 + 回滚确认 + 手动同意。签名失败一律保留旧插件。 |
| 性能 | 一次 SHA-512 + 一次 Ed25519 验证 + 一次 semver 解析；无网络、无额外分配大头，O(1)。 |

状态：业务层已实现；界面层仅演示（50-plugin-upgrade.png），未进实现。
'''

D['docs/features/plugin-fault-recovery.md'] = '''# F037-02 插件故障报告与三动作

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | 加载失败生成 `PluginFault { plugin_id, reason }` → `fault_report()` 出标题/正文/两个动作 → `handle_fault()` 按 `DisableAndContinue` / `Cancel` 改 `StartupPlan`。 |
| 开放了什么 | `src/plugins/fault.rs::fault_report` / `handle_fault` / `StartupPlan::active_plugins` / `should_continue`；`PopupKind::PluginFault` 进 catalog。 |
| 登记框架 | 挂在启动流程的插件装载阶段；弹窗注册表 `src/core/popup.rs` 统一管理关闭路径。 |
| 用户使用逻辑 | 弹窗直接报告哪个插件出了什么问题；底部「禁用并继续尝试启动」只跳过这一个插件再试一次，「取消」中止启动，× / Esc 等同取消。禁用只影响本次启动，其他插件照常加载；全被禁用后不再空转。流程结束 0 残留。 |
| 性能 | BTreeSet 查删 O(log n)，无重试风暴；`retry_count` 单调递增可见。 |

状态：业务层已实现；界面层仅演示（51-plugin-fault.png），未进实现。
'''

D['docs/features/plugin-sidebar-icon.md'] = '''# F037-03 插件侧栏 SVG 与问号兜底

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `PluginIcon::from_svg(Option<&str>)`：合法 SVG 原样保留；缺失/空/非 svg/超 16 KiB/含脚本或外链 → `Fallback`，`glyph()` 返回 `?`。 |
| 开放了什么 | `src/plugins/icon.rs::PluginIcon` / `FALLBACK_GLYPH` / `MAX_SVG_BYTES`。 |
| 登记框架 | 挂在插件清单解析到侧栏槽位注册之间；渲染层由 UI 宿主负责（本轮未实现）。 |
| 用户使用逻辑 | 插件自带图标就显示自己的；没给的显示虚线框问号，尺寸与 lucide 图标一致，深浅主题都清楚。SVG 里的 `href="#..."` 内部引用放行，外部引用退回问号。不做内容白名单，留高度自定义。 |
| 性能 | 单次线性扫描，上限 16 KiB；渲染走 `<img data:>` 隔离，脚本不进 DOM。 |

状态：业务层已实现；界面层仅演示（49-plugin-icons.png），未进实现。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s):
    p = Path(f)
    t = p.read_text()
    marker = s.strip().splitlines()[0]
    if marker in t:
        print('SKIP_DUP', f)
        return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 037 | 身份哈希升级 / 插件故障三动作 / 侧栏 SVG 与问号 | 业务层已实现，界面层仅演示 | 037-plugin-upgrade-fault-icon.md |')

app('docs/features/index.md', '''## 037 新增

| 编号 | 文件 | 状态 |
| --- | --- | --- |
| F037-01 | plugin-upgrade-consent.md | 业务层已实现；界面层仅演示 |
| F037-02 | plugin-fault-recovery.md | 业务层已实现；界面层仅演示 |
| F037-03 | plugin-sidebar-icon.md | 业务层已实现；界面层仅演示 |
''')

app('docs/records/code-ownership-audit.md', '''## 037 业务层新增（零新依赖）

| 项 | 036 | 037 |
| --- | --- | --- |
| 第三方 crate 进构建 | 13 | **13（本轮 0 新增）** |
| `Cargo.lock` 包数 | 14 | 14 |
| `src/` 行数 | 4635 | **5109**（新 `src/plugins/` 474 行） |
| 测试数 | 179 | 207（新增 28） |
| 弹窗 catalog | 11 类 | 13 类 |

037 新增 `src/plugins/` 4 模块：`identity.rs`（SHA-512 身份哈希，复用 ed25519-compact）、`upgrade.rs`（手动同意升级，复用 semver + updater::verify）、`fault.rs`（故障三动作决策）、`icon.rs`（SVG 数据与问号兜底）。这些是项目特有编排，不是自写通用算法回潮；哈希、签名、版本比较全部走已进构建的库。
''')

app('docs/design/implementation-strategy.md', '''## 037 上层第二块

| 层 | 状态 |
| --- | --- |
| 更新器签名校验 | 已启动（036） |
| 插件身份 / 升级同意 / 故障恢复 / 侧栏图标数据层 | **已实现（037，业务层）** |
| 插件 ABI、UI 宿主、真实网络、崩溃分析、更新器其余部分 | 未启动 |
| 界面渲染（侧栏 SVG、两个弹窗） | 仅 UX 演示，等手感确认后写实现 |
''')

app('docs/rules/ui-demo.md', '''## 037 闸门触发记录

| 项 | 值 |
| --- | --- |
| 触发原因 | 侧栏插件图标与两个新弹窗属用户界面 |
| 交付 | `demos/ui-full-kcu-paper.html` 整页更新 + 51 张 PNG（新增 49/50/51 三张） |
| 实现层 | **未写**；`src/` 只落业务决策与数据层，不含渲染代码 |
| 下一步 | 用户按图给手感意见 → 改演示 → 确认后才写进实现 |

另修 `E39`：`.modal` 半透明导致背后卡片文字透进弹窗，改为不透明纸质底，51 张图全量重渲。
''')

app('docs/checklists/ai-errors.md', '''## 037 轮新增

| 编号 | 防错项 |
| --- | --- |
| A96 | 「两个插件哈希一致」先判是身份哈希还是包内容哈希；内容哈希一致时字节相同，版本号不该变，硬套升级会写出永远不触发的分支。 |
| A97 | 用户当轮口径覆盖前序自动安装规则时，要在决策里显式写「撤回 / 覆盖」，不能两条并存。 |
| A98 | 插件 SVG 检查只做格式与外链兜底，不加内容白名单；`href="#..."` 内部片段必须放行。 |
| A99 | 弹窗 catalog 新增类型后，所有硬编码弹窗数的断言要一起核（`core/popup.rs`、`lightweight/view.rs`）。 |
| A100 | 动界面的轮次，`src/` 里只能落业务逻辑；渲染层留在 UX 演示等确认，不能把演示 HTML 当成实现完成。 |
''')

app('docs/records/interface-log.md', '''## 037 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I40 | `src/plugins` | 新增 identity_hash / decide_upgrade / handle_fault / PluginIcon |
| I41 | `core::popup::catalog` | 11 → 13 类，新增 PluginUpgradeConfirm / PluginFault |
| S36 | 状态 | U08–U13 / F01–F06 / I01–I05 已证实；界面实现未启动 |
''')

app('docs/records/rounds.md', '''## 037

| 落点 | 内容 |
| --- | --- |
| docs/spec/37-round-037-instructions.txt | 当轮指令逐字副本 1 行 |
| docs/decisions/037-plugin-upgrade-fault-icon.md | P01-P03 落点、口径解读、U08-U13 / F01-F06 / I01-I05、E35-E39、四值 |
| docs/verification/round-037.md | 14 条复跑证据 |
| docs/features/ | F037-01 / 02 / 03 三份五字段登记 |
| src/plugins/ | 4 模块 474 行、28 个测试 |
| src/core/popup.rs、src/lightweight/view.rs | catalog 11 → 13 类，计数断言同步 |
| demos/ui-full-kcu-paper.html | 侧栏 3 插件（2 SVG + 1 问号）、两个弹窗、设置三条口径、弹窗全集 13 类 |
| demos/preview/ | 51 张 PNG 全量重渲，新增 49 / 50 / 51 |
| 索引与记录 | docs/index 181 项、README、decisions/index、features/index、ai-errors A96-A100、code-ownership-audit、implementation-strategy、ui-demo 触发记录、interface-log、rounds |

「干」继续上层；本轮把三条新需求拆成**业务层落地**与**界面层演示**两轨：

1. **升级手动同意**：身份哈希（`sha512(plugin_id)` 前 16 字节 hex）一致才比对版本；签名校验仍排最前不可禁用；版本更高也**必须用户手动同意**才 Install，否则保留旧插件。这**覆盖 036 U02 的自动安装**，已显式登记撤回。不同身份 / 无已装版本属新装，不叫升级；降级仍要显式目标 + 回滚确认 + 手动同意三者齐备。
2. **插件故障**：弹窗报告插件名与原因，底部「禁用并继续尝试启动」「取消」，× / Esc 等同取消；禁用只跳过该插件，其他照常加载，全禁用后不再空转。catalog 从 11 → **13 类**，两类新弹窗都必可关、流程后 0 残留。
3. **侧栏图标**：插件自带 SVG 直接显示，没给 / 格式不对 / 超 16 KiB / 含脚本外链 → 虚线框问号 `?`。不做内容白名单（按你「留高度自定义」的口径），`href="#..."` 内部片段放行，渲染层用 `<img data:>` 隔离。

**零新增第三方 crate**：SHA-512 用 036 的 ed25519-compact、版本比较用 034 的 semver、签名用 036 的 updater::verify。`cargo test --offline` 179 → **207 / 0**，`Cargo.lock` 仍 14 包 / 13 第三方。

**UI 闸门本轮触发**：整页 UX 演示与 51 张 PNG 已交（重点看 49 / 50 / 51）；按 `docs/rules/ui-demo.md`，**界面渲染实现未写**，`src/` 里只有身份哈希、决策编排与数据层。等手感确认后才写进实现。

本轮真实问题与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E35 | `UpgradeRequest` derive Default 报 E0277 | `Identity` 加 Default |
| E36 | raw string 被内部 `"#` 截断，3 处语法错 | 改 `r##"..."##` |
| E37 | 首版把 `href="#i-puzzle"` 判成外链 | 遍历 href 值，只放行 `#` 开头 |
| E38 | 新增两类弹窗后轻量视图硬编码 11 的断言失败 | 同步 13 |
| E39 | `.modal` 半透明，背后文字透进弹窗 | 改不透明纸质底，51 张图全量重渲 |

028 三项开服器功能仍按「只记文档」零实现；CF F17、特殊版代码、本项目 LICENSE、真实运行时 / GUI / 跨平台、后端仓写请求均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '176. docs/verification/round-036.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''176. docs/verification/round-036.md
177. docs/spec/37-round-037-instructions.txt
178. docs/decisions/037-plugin-upgrade-fault-icon.md
179. docs/features/plugin-upgrade-consent.md
180. demos/preview/51-plugin-fault.png
181. docs/verification/round-037.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-036.md; do printf',
                  'docs/verification/round-036.md docs/spec/37-round-037-instructions.txt docs/decisions/037-plugin-upgrade-fault-icon.md docs/features/plugin-upgrade-consent.md demos/preview/51-plugin-fault.png docs/verification/round-037.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 037 |', p.read_text(), count=1)
section = '''

## 037 插件升级 / 故障 / 侧栏图标

三条新需求拆两轨：业务层落地，界面层只交 UX 演示。

- 身份哈希一致才比对版本；签名校验不可禁用；**升级必须手动同意**（覆盖 036 的自动安装），未同意保留旧插件。
- 插件故障弹窗报告原因，底部「禁用并继续尝试启动 / 取消」，× / Esc 等同取消；弹窗目录 11 → 13 类。
- 插件自带 SVG 显示侧栏，没有就用问号；不做内容白名单，内部片段引用放行。

零新增依赖，`cargo test --offline` 207/0。51 张预览图全量重渲，重点看 `49-plugin-icons` / `50-plugin-upgrade` / `51-plugin-fault`。按 UI 闸门规则，界面渲染实现等你确认后才写。
'''
if '## 037 插件升级' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

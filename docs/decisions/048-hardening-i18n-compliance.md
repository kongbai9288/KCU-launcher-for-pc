# 第 048 轮：硬编码清零、破坏性输入防护、原始需求合规核对

| 项 | 值 |
| --- | --- |
| 编号 | 048 |
| 状态 | 已实现已验证；上层（网络 / UI / 崩溃分析 / 子进程隔离）未启动 |
| 依据 | docs/spec/48-round-048-instructions.txt |
| 前序 | 023 Fluent 方案、032 修 27 处中文 key、046 panic_guard、047 semver_guard、045/047 环境清单 |
| 本轮性质 | 三轨：① 硬编码清零 ② 破坏性场景防护 ③ 原始需求逐条核对；零新增第三方依赖 |

## 开工核查

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-047-A | 远端 ref | `d71e8b5`，message `round 047 rollback version precedence and semver guard` |
| V-047-B | 本地 HEAD | `c97e778`，990 文件，工作区干净 |
| V-047-C | 临时凭据 | 核查后删除，全仓 `NO_CREDENTIAL`、`.git/config` 干净 |

## 一、硬编码文字（你翻到的那部分）

| 位置 | 048 前 | 处置 |
| --- | --- | --- |
| `src/plugins/fault.rs` 产品层 | 4 处中文字符串字面量（标题、正文、两个按钮） | U99：改成 5 个语义 key + `body_args`，`src/` 非测试段中文 **0** |
| `demos/ui-full-kcu-paper.html` DOM 属性 | **399 个** `data-i18n` 值直接是中文（344 唯一） | U100：全换成 `t.NNNN` |
| 同一文件 DOM 纯文本节点 | **405 个**含中文的标签无 `data-i18n` | U100：注入 `data-i18n`，原文收进 `ZH_TEXT` |
| 字典 | 只有 `EN`（88 组语义 key）与一份中文键 `EN_TEXT` | 生成 **659 组** `ZH_TEXT` / `EN_TEXT`，`tr()` 中文态走 `ZH_TEXT` |

032 只修了设置分组里 27 处中文 key，其余 372 处仍在；`src/plugins/fault.rs` 是 037 落地插件故障弹窗时新写的产品层中文。两处都没被之前的守卫覆盖。

| 编号 | 动作 |
| --- | --- |
| U99 | `FaultReport` 改为 `title_key` / `body_key` / `body_args` / `primary_key` / `secondary_key`；原 6 个测试断言同步改 key，未删验收项。 |
| U100 | `scripts/round048_i18n.py` 自动转换：中文 key → 复用同一 `t.NNNN`，纯文本节点在开标签注入属性（不改 DOM 结构）；重生成字典与 `tr()`。JS `new Function` 通过。 |
| U101 | `scripts/i18n_guard.py` + CI `i18n_guard` step：扫 `src/` 37 文件非测试段字符串字面量、有效 UX 演示的 DOM 中文 key 与裸中文节点。双向验证注入 `data-i18n="首页"` → `I18N_GUARD_FAIL 1`，恢复 → `I18N_GUARD_OK`。历史稿 2 份显式排除并输出。 |

**如实登记三处未清零**：
- `<script>` 数据源仍有 **298 行含中文**（671 个单引号字符串 / 503 唯一、11 个模板串、36 个双引号片段），是公告正文、弹窗描述、实例表格等演示数据，不在 DOM 守卫范围；语言包迁移见 EQ-14。
- 英文态 `EN_TEXT` 有 **567 条**回退中文；旧字典只有 88 组语义 key 有译文，词级补译只修了 4 条。DOM 结构已 key 化，译文覆盖不全。
- `ui-full-kcu-v2.html` / `ui-full-lightweight.html` 是 017 / 016 历史稿（018 标记作废），守卫排除，未删除。

## 二、暴力测试与删文件防护

一手资料：https://owasp.org/www-community/attacks/Path_Traversal —— 「By manipulating variables that reference files with dot-dot-slash (../) sequences and its variations or by using absolute file paths, it may be possible to access arbitrary files」；「Validate the user's input by only accepting known good – do not sanitize the data」。Std 文档：`std::path::Component` 把路径拆成 `Prefix` / `RootDir` / `CurDir` / `ParentDir` / `Normal`；`PoisonError::into_inner`（046 已取）。

| 编号 | 场景 | 落地 |
| --- | --- | --- |
| U102 | 超长、空值、控制字符 | `check_text(s, limit)`，返回 `Err` 不 panic |
| U102 | id 洪泛 | `check_ids`：总量 ≤ 10000、单项 ≤ 256B；接入 `http::plan`，构造请求前拦下 |
| U102 | 路径穿越 / 绝对路径 / Windows 保留名 / 超深 | `safe_join(root, rel)`：遍历 `std::path::Component`，拒 `Prefix`/`RootDir`、越出 root 的 `ParentDir`、`CON`/`NUL` 等、控制字符、深度 > 32；接入 `PathResolver::resolve_relative` |
| U102 | 用户删了配置 / 语言包 / 图标 | `read_or_default` 回默认值并返回「是否回退」标志，不 panic；`require_file` 对必需文件给明确错误，不静默创建 |
| U102 | 必需文件被删 | 同上，返回 `Err`，不假装默认值就是真实配置 |
| U102 | 高频重复点击 / 并发打爆 | `OpBudget`：1 秒滚动窗口、原子计数、上限可设；锁中毒走 `PoisonError::into_inner` |
| U102 | 已有防护复核 | `plugins/icon.rs` 的 `MAX_SVG_BYTES = 16 KiB` 已生效（044）；`core/cache.rs` 容量有界（029）；`core/config.rs` 畸形输入硬化（035） |

`src/core/robust.rs` 241 行，8 个测试真跑：删文件→回退→写回→再删→必需文件报错、10 万个 id 被拒、`../` / 绝对路径 / `CON` / 控制字符 / 超深被拒、8 线程并发下 `OpBudget` 不超上限、锁中毒后仍可服务。

`Cargo.toml` / `Cargo.lock` / `vendor/` **一行未动**，仍 26 包 / 25 第三方。**如实登记**：标准库 API 用法 + 项目策略清单，不是第三方库替换。

## 三、原始需求逐条核对

`docs/records/requirement-compliance-audit.md` 把 `00-requirements.txt`（261 行）、`11-features-input.txt`、`12-server-features-input.txt` 与各轮指令分成四类：

| 类 | 数量 | 内容 |
| --- | --- | --- |
| A 已决断且遵守 | 抽样 11 条 | 27 顺延、D06 启用、批量请求、缓存异步、弹窗可关、双击绑定、许可页、槽位锁定、档位、UI 闸门、上层用别人代码 |
| B 已决断但未遵守 | **10 条** | 交付格式缺时间戳/自我批判、开工未逐字复读原文、`/v1/batch` 与 `https` 写死、未用 UI 框架、未引 HMCL 代码、声明页三项内容未做、插件独立进程未实现、境外限制未实现、32 位未验证、未停在「完全无法失误」 |
| C 未决断我擅自定默认 | **10 条** | 轻量 13 项排除、实现层单主题、L1–L3 纯 std 例外（024 已撤）、身份哈希口径、「两个问题 A」未随澄清重审、推荐位 10 处与 SLP 六类、上层起手顺序、一级导航 9 项、028 三个默认值、历史稿保留 |
| D 文档要求但标未启动 | **9 组** | 手机连接、文件管理 40+、开服器 27+、4 项交互细节、LICENSE/图片仓/代码对比、上层 4 块、声明页 3 项、正常启动器 6 项、4 个未验证架构 |

B03 具体证据：`src/lightweight/download.rs::plan` 硬编码 `scheme: "https"`、`path: "/v1/batch"`，而 `core/config.rs` 已有 `endpoints` 表却没被读。C01/C02 是 016 我自己写的「13 项排除」「实现层单主题」，你只给了轻量 5 条功能，没批准排除清单。

新增 **EQ-14**（演示数据源语言包迁移）与 **EQ-15**（端点配置化），具体环境与选项已写进清单和核对表，本轮**未代你决断**。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo test --offline --lib`：**280 / 0**（047 是 269；新增 robust 8 / http 2 / paths 1）。 |
| V-B | `http_construct` 7 / 0、`window_handle_contract` 6 / 0、`plugin_lifecycle_load` 7 / 0、`plugin_abi_load` 6 / 0，合计 **306 / 0**。 |
| V-C | `cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-D | `panic_guard` / `semver_guard` / `i18n_guard` 三守卫零命中；CI scan job 7 个 step。 |
| V-E | `render_ui.py` 重渲 **56 张 PNG** 通过；首页全尺寸实拍中文完整，没有 key 顶替文案。 |
| V-F | 必读 248 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，38 份 HTML 脚本通过。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E89 | `i18n_guard` 首版扫全部 `ui-full-*.html`，把 017/016 两份作废历史稿的 299 处中文判 FAIL | 设 `ACTIVE` 集合只判当前有效演示，历史稿显式列进 `excluded_history` 输出 |
| E90 | 词级补译只把 4 条英文译文补上，567 条仍回退中文 | 如实登记，不宣称英文态完整；列 EQ-14 |
| E91 | 首次统计把 `<style>` 内容与 `<title>` 算成裸中文节点 | 守卫与转换脚本都设 `SKIP_TAGS`，重跑后 DOM 裸节点 0 |
| E92 | `render_ui.py` 重渲后需人眼确认中文没被 key 顶替 | 读 `01-home.png` 实拍确认，截图入交付 |

## 四值

| 项 | 值 |
| --- | --- |
| 399 中文 key / 405 裸节点 / 4 处产品层中文清零、659 组字典 | 已证实 |
| robust 8 类场景、306 / 0、三守卫零命中、零新增依赖 | 已证实 |
| B 类 10 条 / C 类 10 条 / D 类 9 组偏差如实登记 | 已证实 |
| 演示数据源 298 行中文、英文态 567 条回退 | 已证实（未清零） |
| EQ-14 / EQ-15、B/C/D 偏差处置 | 未证实（待拍板） |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| 后端仓写请求 | 0（已证实） |

## 交付快照

本地 `976c0d1` ↔ 远端 `d7dd6a2`，1000 文件逐项 ALL_MATCH True（DIFF 0 / EXTRA 0）。远端 message 与本地一致。全仓零凭据、后端仓 0 写请求。

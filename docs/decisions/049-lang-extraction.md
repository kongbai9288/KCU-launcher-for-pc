# 第 049 轮：演示数据源抽成独立语言包

| 项 | 值 |
| --- | --- |
| 编号 | 049 |
| 状态 | 已实现已验证；`src/` 零改动 |
| 依据 | `docs/spec/49-round-049-instructions.txt`（逐字：「抽」） |
| 对应 | EQ-14 选项 ②；048 结尾的唯一待拍板项 |
| 本轮性质 | 只做一件事：把演示数据源从 HTML 里抽出来，两种语言各一份，切换时重建数组 |

## 开工核查

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-048-A | 本地 HEAD | `6a8bbe5`，1000 文件，工作区干净 |
| V-048-B | 048 远端 | `cb20450`（`round 048 record delivery snapshot`），1000 文件 ALL_MATCH |
| V-048-C | 临时凭据 | 048 收尾已删；全仓 `NO_CREDENTIAL`，`.git/config` 干净 |

## 抽取范围

048 登记：`<script>` 段 298 行含中文、671 个单引号字符串、503 唯一，是 `NOTICES` / `POPUPS` / `INS` / `SRV` / `CREDITS` / `AUTH` / `OB` 等常量数组，加上 659 组 `ZH_TEXT`/`EN_TEXT`。

用 Node 对顶层 `const` 段求值，导出 **24 个键**的纯数据（100442 B JSON），不在 Python 里手写 JS 字面量解析：

| 类别 | 键 |
| --- | --- |
| 数据数组 / 对象（20） | `NOTICES` `POPUPS` `INS` `SRV` `CREDITS` `AUTH` `OB` `VIEW_META` `TIER_LABEL` `AROWS` `AUTO_AFTER` `AUTO_EFFECT` `DL` `LICENSE_ROWS` `CACHE_ROWS` `REFRESH_ROWS` `SERVERS` `DEVICE` `UPPER` `REC_CATALOG` |
| 字典（4，两包同值） | `EN`（181 条语义 key 译文）、`ZH_TEXT`（659）、`EN_TEXT`（659）、`TIER_EN`（3） |

| 编号 | 动作 |
| --- | --- |
| U104 | 生成 `demos/lang/zh-CN.js` 与 `demos/lang/en-US.js`，各 24 键、约 80 KB；格式 `window.KCU_LANG['<locale>'] = {...}`。 |
| U105 | 从 HTML 删除 **274 行**顶层 `const` 定义，改由 `<script src="lang/*.js">` 在主脚本前加载 —— 离线 `file://` 直接可用，不用 `fetch`、不用 CDN、不受 CORS 限制。 |
| U106 | 主脚本启动时声明 20 个 `let` 数据变量并取中文包；`loadData(l)` 在切换时从 `KCU_LANG[l]` 重建全部 20 个数组。 |
| U107 | `setLang` 调用 `loadData`、`renderNotices` / `renderDl` / `renderAuth` / `renderFlow` / `renderOb` / `renderPops` / `renderLic` / `renderSrv` / `updateBudget` / `applyI18n` / `renderTier` / `show`，切换后当前视图整体重渲。 |
| U108 | `mergeState(fresh, old, key, fields)`：按稳定键合并运行时状态，切语言不丢公告已读、服务器锁定 / ping / 在线人数 / 用户新增项。 |
| U109 | `scripts/lang_guard.py` + CI `lang_guard` step；`i18n_guard.py` 统计口径改名为 `inline_bilingual_cn_lines`。 |

## 译文口径（如实登记）

词典只收文件里**真实存在**的双语对应：`EN_TEXT` 里译文不等于原文的 92 组、`VIEW_META` 标题 ↔ `EN['view.*']`、`TIER_LABEL` ↔ `TIER_EN`、内联三元 `? 'English' : '中文'`、`T(k,zh,en)`，合计 **115 条**。

只做**整句精确匹配**，不做词级拼接。首版试过短语替换，生成 `KCU Launcher ProjectNotes` 这类未审校拼接词，已撤回（E94）。

| 项 | 值 |
| --- | --- |
| 数据源中文字符串 | 496 |
| 英文包精确译成英文 | **25** |
| 英文包仍保留中文 | **471** |
| 禁用词级拼接 | 是 |

**用户数据与稳定状态值不翻译**，两包逐项一致，由守卫强制：`SERVERS` 的 `sid/id/name/ip/ver/motd/inst/last/src`（玩家起的服务器名、MOTD、实例名属于用户数据）；`SRV[*][3]`、`LICENSE_ROWS[*][6]`、`INS[*][5]` 是 JS 用来判断 badge 的稳定字面量，翻译会改变逻辑。

**已知限制 L-049-1**：英文态下公告正文、弹窗描述、逻辑条、面包屑、底部状态栏等仍有中文。DOM 层 659 组 key 里 92 组有译文，界面框架是英文；471 条数据源字符串保留中文，未做机器拼接或人工补译。要完整英文态需单独审校，本轮不代你决定。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `verify_lang.py`（Playwright + 系统 chromium，`file://` 打开）：两语言包加载成功、24 键、中文态导航「首页」→ 英文态「Home」→ 切回「首页」，`NOTICES`/`SERVERS` 数量不变、运行时状态 `lock=false / ping=99` 跨两次切换保留、**0 控制台错误**。 |
| V-B | `node new Function` 对两个语言包与主脚本通过；39 份 demos HTML 脚本全通过。 |
| V-C | `lang_guard.py`：`LANG_GUARD_OK locales zh-CN en-US keys 24 data_cn_zh 496 data_cn_en_known 471 stable_values_ok offline_refs_ok`；CI scan 8 steps。 |
| V-D | `i18n_guard` / `panic_guard` / `semver_guard` 零命中；`P09_HITS 0`。 |
| V-E | `render_ui.py` 重渲 **51 场景 / 56 张 PNG**；读 `01-home.png` 中文完整、读 `41-i18n-en.png` 界面框架英文。 |
| V-F | `cargo test --offline --lib` **280 / 0**；`git diff -- src/ Cargo.toml Cargo.lock vendor/` 为空，仍 26 包 / 25 第三方。 |
| V-G | HTML script 段中文行 **298 → 122**（降 176）；剩余是内联双语 fallback 与稳定状态字面量，不是数据源。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E93 | Playwright 默认浏览器未安装，验证脚本首跑 `BrowserType.launch` 失败 | 按 `render_ui.py` 的既有口径传 `executable_path=/usr/local/bin/chromium` + `--no-sandbox`，复跑通过 |
| E94 | 词级短语替换生成 `KCU Launcher ProjectNotes` 拼接怪译 | 撤回短语替换，只保留整句精确对应；471 条如实保留中文 |
| E95 | 抽取后 `SRV[*][3]` / `LICENSE_ROWS[*][6]` 是中文字面量比较，若以后被翻译会改变 badge 逻辑 | 生成时显式保护 + `lang_guard` 逐项比对两包一致 |
| E96 | 切语言重建 `SERVERS` 会丢用户新增项与运行时状态 | `mergeState` 按 `sid` 合并，验证脚本真改 `lock/ping` 后跨两次切换复核 |

## 四值

| 项 | 值 |
| --- | --- |
| 24 键 / 274 行抽离、两语言包、离线加载、切换重建、状态合并 | 已证实 |
| 280 / 0、四守卫零命中、56 张 PNG 重渲、零控制台错误 | 已证实 |
| 英文包 471 条中文、英文态局部中文残留 | 已证实（未清零，L-049-1） |
| 英文数据源人工审校 | 未启动 |
| `src/`、Cargo.lock、vendor 改动 | 0（已证实） |
| 后端仓写请求 | 0（已证实） |

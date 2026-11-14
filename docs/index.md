# 文档索引

检索日期：2026-11-12
更新轮次：019

## 每轮开工必读顺序

1. docs/spec/00-requirements.txt
2. docs/spec/01-round-001-instructions.txt
3. docs/spec/02-round-002-instructions.txt
4. docs/spec/03-round-003-instructions.txt
5. docs/spec/04-round-004-instructions.txt
6. docs/spec/05-round-005-instructions.txt
7. docs/spec/06-round-006-instructions.txt
8. docs/spec/07-round-007-instructions.txt
9. docs/spec/08-round-008-instructions.txt
10. docs/spec/09-round-009-instructions.txt
11. docs/spec/10-round-010-instructions.txt
12. docs/spec/11-round-011-instructions.txt
13. docs/spec/11-features-input.txt
14. docs/spec/12-round-012-instructions.txt
15. docs/spec/12-server-features-input.txt
16. docs/checklists/ai-errors.md
17. docs/checklists/windows-errors.md
18. docs/rules/proof-rules.md
19. docs/rules/fallback-rules.md
20. docs/rules/push-scope.md
21. docs/rules/build-preconditions.md
22. docs/research/index.md
23. docs/features/index.md
24. docs/records/rounds.md
25. docs/records/open-questions.md
26. docs/features/backlog.md
27. docs/features/server-backlog.md
28. docs/research/16-server-platform.md
29. docs/decisions/012-server-input.md
30. docs/spec/13-round-013-instructions.txt
31. docs/spec/13-round-013-instructions-part2.txt
32. docs/records/round-013-answers.md
33. docs/decisions/013-build-start.md
34. Cargo.toml
35. src/lib.rs
36. src/core/mod.rs
37. docs/features/core-userflow.md
38. docs/features/core-popup.md
39. docs/spec/14-round-014-instructions.txt
40. docs/decisions/014-build-continue.md
41. .github/workflows/ci.yml
42. docs/features/core-cache.md
43. docs/features/core-asynk.md
44. docs/features/core-leak.md
45. docs/spec/15-round-015-instructions.txt
46. docs/decisions/015-build-continue.md
47. docs/rules/ui-demo.md
48. src/dispatcher/mod.rs
49. docs/features/dispatcher.md
50. docs/features/dispatcher-json.md
51. docs/features/dispatcher-task.md
52. docs/features/dispatcher-mode.md
53. docs/features/dispatcher-launcher.md
54. docs/spec/16-round-016-instructions.txt
55. docs/decisions/016-build-continue.md
56. src/lightweight/mod.rs
57. docs/features/lightweight.md
58. docs/features/lightweight-login.md
59. docs/features/lightweight-download.md
60. docs/features/lightweight-loaders.md
61. docs/features/lightweight-view.md
62. docs/spec/17-round-017-instructions.txt
63. docs/decisions/017-visual-preview.md
64. demos/preview/index.md
65. docs/features/ui-visual-catalog.md
66. scripts/render_ui.py
67. docs/spec/18-round-018-instructions.txt
68. docs/decisions/018-paper-ux.md
69. demos/preview/index.md
70. docs/features/ui-paper-ux.md
71. demos/ui-full-kcu-paper.html
72. docs/spec/19-round-019-instructions.txt
73. docs/decisions/019-ux-logic-lucide.md
74. docs/design/ux-logic-matrix.md
75. docs/features/ux-logic-completion.md
76. docs/features/lucide-icon-system.md
77. docs/features/third-party-licenses-about.md
78. THIRD-PARTY-NOTICES.md
79. docs/spec/20-round-020-instructions.txt
80. docs/decisions/020-nav-slots-settings.md
81. docs/research/17-plugin-settings-survey.md
82. docs/design/nav-slot-contract.md
83. docs/design/recommendation-catalog.md
84. docs/design/server-status.md
85. docs/design/upper-layer-stack.md
86. docs/design/handoff.md
87. docs/features/nav-slot-lock.md
88. docs/features/settings-groups.md
89. docs/features/recommendation-catalog.md
90. docs/features/server-status-settings.md
91. docs/features/upper-layer-thirdparty.md
92. docs/features/handoff-baseline.md
93. docs/spec/21-round-021-instructions.txt
94. docs/decisions/021-server-autoconnect.md
95. docs/research/18-server-list-autodiscovery.md
96. docs/design/server-list-logic.md
97. docs/design/ui-product-copy.md
98. docs/features/server-autoconnect.md
99. docs/features/servers-dat-analysis.md
100. docs/features/server-join-binding.md
101. docs/features/ui-product-copy.md
102. docs/spec/22-round-022-instructions.txt
103. docs/decisions/022-async-budget.md
104. docs/research/19-async-probe-budget.md
105. docs/design/async-probe-policy.md
106. docs/features/server-async-probe.md
107. docs/features/server-failure-history.md
108. docs/verification/round-022.md
109. scripts/round022_async.py
110. docs/spec/23-round-023-instructions.txt
111. docs/decisions/023-architecture-answers.md
112. docs/research/20-i18n-crash-identity.md
113. docs/design/stable-identity.md
114. docs/design/i18n-policy.md
115. docs/design/crash-reporting.md
116. docs/design/implementation-strategy.md
117. docs/features/stable-identity-rename.md
118. docs/features/i18n-crash-settings.md
119. docs/verification/round-023.md
120. scripts/round023_ux.py
121. scripts/round023_i18n_cover.py
122. scripts/round023_docs.py
123. docs/records/code-ownership-audit.md
124. docs/decisions/024-code-ownership.md

读取命令：

```
cd /data/workspace/kcu-launcher-desktop
for f in docs/spec/00-requirements.txt docs/spec/01-round-001-instructions.txt docs/spec/02-round-002-instructions.txt docs/spec/03-round-003-instructions.txt docs/spec/04-round-004-instructions.txt docs/spec/05-round-005-instructions.txt docs/spec/06-round-006-instructions.txt docs/spec/07-round-007-instructions.txt docs/spec/08-round-008-instructions.txt docs/spec/09-round-009-instructions.txt docs/spec/10-round-010-instructions.txt docs/spec/11-round-011-instructions.txt docs/spec/11-features-input.txt docs/spec/12-round-012-instructions.txt docs/spec/12-server-features-input.txt docs/checklists/ai-errors.md docs/checklists/windows-errors.md docs/rules/proof-rules.md docs/rules/fallback-rules.md docs/rules/push-scope.md docs/rules/build-preconditions.md docs/research/index.md docs/features/index.md docs/records/rounds.md docs/records/open-questions.md docs/features/backlog.md docs/features/server-backlog.md docs/research/16-server-platform.md docs/decisions/012-server-input.md docs/spec/13-round-013-instructions.txt docs/spec/13-round-013-instructions-part2.txt docs/records/round-013-answers.md docs/decisions/013-build-start.md Cargo.toml src/lib.rs src/core/mod.rs docs/features/core-userflow.md docs/features/core-popup.md docs/spec/14-round-014-instructions.txt docs/decisions/014-build-continue.md .github/workflows/ci.yml docs/features/core-cache.md docs/features/core-asynk.md docs/features/core-leak.md docs/spec/15-round-015-instructions.txt docs/decisions/015-build-continue.md docs/rules/ui-demo.md src/dispatcher/mod.rs docs/features/dispatcher.md docs/features/dispatcher-json.md docs/features/dispatcher-task.md docs/features/dispatcher-mode.md docs/features/dispatcher-launcher.md docs/spec/16-round-016-instructions.txt docs/decisions/016-build-continue.md src/lightweight/mod.rs docs/features/lightweight.md docs/features/lightweight-login.md docs/features/lightweight-download.md docs/features/lightweight-loaders.md docs/features/lightweight-view.md docs/spec/17-round-017-instructions.txt docs/decisions/017-visual-preview.md demos/preview/index.md docs/features/ui-visual-catalog.md scripts/render_ui.py docs/spec/18-round-018-instructions.txt docs/decisions/018-paper-ux.md demos/preview/index.md docs/features/ui-paper-ux.md demos/ui-full-kcu-paper.html docs/spec/19-round-019-instructions.txt docs/decisions/019-ux-logic-lucide.md docs/design/ux-logic-matrix.md docs/features/ux-logic-completion.md docs/features/lucide-icon-system.md docs/features/third-party-licenses-about.md THIRD-PARTY-NOTICES.md docs/spec/20-round-020-instructions.txt docs/decisions/020-nav-slots-settings.md docs/research/17-plugin-settings-survey.md docs/design/nav-slot-contract.md docs/design/recommendation-catalog.md docs/design/server-status.md docs/design/upper-layer-stack.md docs/design/handoff.md docs/features/nav-slot-lock.md docs/features/settings-groups.md docs/features/recommendation-catalog.md docs/features/server-status-settings.md docs/features/upper-layer-thirdparty.md docs/features/handoff-baseline.md docs/spec/21-round-021-instructions.txt docs/decisions/021-server-autoconnect.md docs/research/18-server-list-autodiscovery.md docs/design/server-list-logic.md docs/design/ui-product-copy.md docs/features/server-autoconnect.md docs/features/servers-dat-analysis.md docs/features/server-join-binding.md docs/features/ui-product-copy.md docs/spec/22-round-022-instructions.txt docs/decisions/022-async-budget.md docs/research/19-async-probe-budget.md docs/design/async-probe-policy.md docs/features/server-async-probe.md docs/features/server-failure-history.md docs/verification/round-022.md scripts/round022_async.py docs/spec/23-round-023-instructions.txt docs/decisions/023-architecture-answers.md docs/research/20-i18n-crash-identity.md docs/design/stable-identity.md docs/design/i18n-policy.md docs/design/crash-reporting.md docs/design/implementation-strategy.md docs/features/stable-identity-rename.md docs/features/i18n-crash-settings.md docs/verification/round-023.md scripts/round023_ux.py scripts/round023_i18n_cover.py scripts/round023_docs.py docs/records/code-ownership-audit.md docs/decisions/024-code-ownership.md; do printf '%s %s\n' "$f" "$(wc -l < "$f")"; done
```

## 分区

| 分区 | 入口 | 职责 |
| --- | --- | --- |
| 需求规格 | docs/spec/00-requirements.txt | 需求原文 |
| 011 功能输入 | docs/spec/11-features-input.txt | 55 条编号功能与 175 项文件管理清单逐字副本 |
| 012 开服器输入 | docs/spec/12-server-features-input.txt | 开服器编号功能与分节条目逐字副本 |
| 待拍板问题全集 | docs/records/open-questions.md | 93 条，A-H 组，013 轮已答复 |
| 013 答复台账 | docs/records/round-013-answers.md | 76 片段逐字编号、语义映射、不写死项 |
| 013 开工决策 | docs/decisions/013-build-start.md | D06/D07、工具链纠正、G 组默认、H 组硬要求 |
| Rust crate | Cargo.toml | std only，profile 默认值已核实；015 轮未新增依赖 |
| L1 core 源码 | src/core/ | 12 个模块 |
| L1 功能登记 | docs/features/core-*.md | 12 份，字段固定五段 |
| L2 dispatcher 源码 | src/dispatcher/ | 5 个模块，47 项单元测试 |
| L2 功能登记 | docs/features/dispatcher*.md | 5 份，字段固定五段 |
| 全量测试 | Cargo.toml | 141 passed / 0 failed / 0 ignored / 0 measured |
| L3 lightweight 源码 | src/lightweight/ | 5 个模块，38 项单元测试 |
| L3 功能登记 | docs/features/lightweight*.md | 5 份，字段固定五段 |
| 015 决策 | docs/decisions/015-build-continue.md | UI 整页演示闸门、L2 开工、L01-L14 |
| 016 决策 | docs/decisions/016-build-continue.md | L3 落地、UI 整页演示首次触发、主题口径处置 |
| 017 决策 | docs/decisions/017-visual-preview.md | PNG 预览闸门、公告族补齐；风格项由 018 撤回 |
| 018 决策 | docs/decisions/018-paper-ux.md | 纸质质感重做、UX/流程形态区分、W01/W02、S01-S20、E01-E05 |
| UX 整页演示 | demos/ui-full-kcu-paper.html | 1440×900 桌面窗口、20 视图、纸质两套主题、离线可点 |
| 作废演示 | demos/ui-full-kcu-v2.html | 017 风格取错，保留文件不复用 |
| 界面预览 | demos/preview/ | 43 张产品视图 PNG + 4 张内部证据图 + 00-overview.png 总览 + index.md |
| 渲染脚本 | scripts/render_ui.py | 本地 chromium 截图与拼图，每视图强制重载，0 次远端请求 |
| 020 决策 | docs/decisions/020-nav-slots-settings.md | 导航瘦身、锁定槽位、设置归拢、推荐目录、上层第三方、交接基线 |
| 020 调研 | docs/research/17-plugin-settings-survey.md | 12 一手 + 4 公开资料 + 3 受阻，完整 URL 锚点 |
| 021 设计 | docs/design/ | server-list-logic、ui-product-copy；020 的 server-status 页面口径已被 021 取代 |
| 022 设计 | docs/design/ | async-probe-policy；取代 021 的同步遍历口径 |
| 023 设计 | docs/design/ | stable-identity、i18n-policy、crash-reporting、implementation-strategy |
| 020 设计 | docs/design/ | nav-slot-contract、recommendation-catalog、server-status、upper-layer-stack、handoff |
| 019 决策 | docs/decisions/019-ux-logic-lucide.md | 使用逻辑骨架、lucide、第三方许可、自评迭代 |
| 使用逻辑矩阵 | docs/design/ux-logic-matrix.md | U01–U20 × L01–L12、缓存分层、刷新触发、推荐位 |
| 图标资产 | assets/icons/ | lucide 88 枚一手 SVG 与 manifest |
| 发行物声明 | THIRD-PARTY-NOTICES.md | 关于页同一份清单 |
| UI 闸门规则 | docs/rules/ui-demo.md | 023 增 G23：i18n 切换、改名、延迟小字、崩溃反馈的用户可见口径 |
| 014 决策 | docs/decisions/014-build-continue.md | 私仓、secrets 占位、样板化 UX、缓存异步泄漏防护 |
| CI 工作流 | .github/workflows/ci.yml | secrets / vars 占位、有界缓存、并发取消、并行 job |
| 特殊版私仓 | kongbai9288/KCU-launcher-special | private，仅 README 占位，代码待用户同意 |
| 调研 | docs/research/index.md | 外部事实、锚点、四值 |
| 合规与阻塞项 | docs/research/12-compliance.md | API 条款、凭据保护、许可证全文、上游版本、X01-X07 |
| 系统 API 与平台 | docs/research/13-platform-api.md | Win7、多架构、版本/架构/位置 API、Rust 目标冲突 |
| 网络通用法 | docs/research/14-batch-network.md | 批量端点、N+1 反模式、回环监听、配置集中 |
| 外部项目核实 | docs/research/15-input-survey.md | 只读后端仓、CopperGolemLauncher、ViaNBT、dsh、VxKex |
| 开服器官方资料 | docs/research/16-server-platform.md | 插件源、mrpack、EULA、原版命令、Java 版本、ops.json、种子 NBT、icon、UPnP、mclo.gs |
| 底层运行时调研 | docs/research/11-runtime.md | Cargo profile、DLL 搜索、进程管理、WebView2 进程组、目标三元组、MSVC 部署 |
| 许可证原文 | docs/licenses/index.md | 逐字副本与 slint 三许可全文 |
| 功能登记 | docs/features/index.md | F001-F012；011 输入见 backlog.md；012 输入见 server-backlog.md |
| 决策 | docs/decisions/index.md | 状态分层记录 |
| 防错 | docs/checklists/ | AI 与 Windows 防错清单 |
| 规则 | docs/rules/ | 四值判决、兜底分级、推送范围、搭建前置条件 |
| 记录 | docs/records/ | 版本、接口、轮次、问题全集 |
| 验证 | docs/verification/ | 独立验证报告 |
| UI 资产 | assets/ui/index.md | 正常模式 UI 逐字副本与结构登记 |
| 图标资产 | assets/icon/kcu-launcher.jpg | 启动器图标原始字节 |
| 演示 | demos/round-001-dispatch.html | 统一调度器运行逻辑 |
| 演示 | demos/round-002-icon.html | 图标资产登记运行逻辑 |
| 演示 | demos/round-003-remote.html | 远端推送与搭建阶段运行逻辑 |
| 演示 | demos/round-004-remote.html | 公仓创建与 API 快照推送运行逻辑 |
| 演示 | demos/round-006-closeout.html | 005 收口与 006 交付运行逻辑 |
| 演示 | demos/round-007-normal-ui.html | 正常模式 UI 与轻量分流运行逻辑 |
| 演示 | demos/round-008-mode-views.html | 模式视图登记与补证运行逻辑 |
| 演示 | demos/round-009-coverage.html | 需求覆盖与底层调研运行逻辑 |
| 演示 | demos/round-010-compliance.html | 合规阻塞与搭建前置运行逻辑 |
| 演示 | demos/round-011-input.html | 功能输入与硬冲突判定运行逻辑 |
| 演示 | demos/round-012-server-input.html | 开服器输入与 93 条问题闸门运行逻辑 |
| 演示 | demos/round-013-core.html | core 编译、用户操作模拟、11 类弹窗关闭逻辑 |
| 演示 | demos/round-014-cache-async.html | 缓存单飞、多源竞速取消、泄漏归零、工作流占位 |
| 演示 | demos/round-015-dispatcher.html | L2 调度判定、模式分流、安全模式、用户操作模拟；运行逻辑演示，非整页 UI |
| 整页 UI 演示 | demos/ui-full-lightweight.html | 016 轮触发：轻量极简整页、6 分区、5 状态、11 弹窗、手感调整区、离线可点 |
| 演示 | demos/round-016-lightweight.html | L3 三级回退、批量请求、无常驻进程；运行逻辑演示，非整页 UI |
| 界面预览总览 | demos/preview/00-overview.png | 023 轮 43 个产品视图缩略拼图，直接看界面长相 |
| 界面预览单图 | demos/preview/01-20 | 首页、深色纸质、公告中心、公告详情、更新、引导、实例、网格、下载、模组、登录、日志、抽屉、设置、关于、弹窗、轻量、异常、收起、右键 |
| 脚本 | scripts/push.sh | 推送入口，自动降级 |
| 脚本 | scripts/api_push.py | Git Data API 全量树快照 |

## 远端

| 项 | 值 |
| --- | --- |
| 仓库 | kongbai9288/KCU-launcher-for-pc |
| 地址 | https://github.com/kongbai9288/KCU-launcher-for-pc |
| 可见性 | public |
| 分支 | main |
| 推送路径 | git HTTP 受阻；REST Git Data API 全量树快照 |
| 用户后端仓 | 只读，仅 GET，内容不进公仓 |
| 特殊版 | `kongbai9288/KCU-launcher-special`，private，014 轮已建仓，仅 README 占位 |
| 特殊版放代码条件 | 用户明确同意后，用户手拉工具流 |

## 每轮开工前检查

| 检查 | 命令 |
| --- | --- |
| 时间戳 | `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` |
| 网络时钟 | `curl -sSI -H 'User-Agent: KCU-Launcher-Desktop/0.0.0' https://api.github.com/rate_limit \| grep -i '^date:'` |
| 文档完整性 | 上方读取命令 |
| 凭据扫描 | `! grep -rqE 'gh[p]_' .` |
| 解释性措辞扫描 | `! grep -rE '为什么\|这意味着\|值得注意的是\|综上所述\|让我们看看' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| 中间态扫描 | `! grep -rE '部分已证实' docs/research/ docs/features/ docs/records/ docs/decisions/` |
| 重复引用扫描 | `! grep -rE '同上' docs/research/` |
| 品牌元素扫描 | `! grep -rE 'FCL\|揉纸启动器' src/` |
| 推广措辞扫描 | `! grep -rE '表现得最优\|使用人数最多\|社区反馈最积极' docs/features/ docs/decisions/` |
| 功能状态扫描 | `test -z "$(grep -L '未实现' docs/features/dispatcher.md docs/features/lightweight.md docs/features/headless.md docs/features/normal-launcher.md docs/features/lan.md docs/features/server.md docs/features/log.md docs/features/fallback.md docs/features/envelope.md docs/features/ui-framework.md docs/features/credential-guard.md)"` |
| 编号功能完整性 | `grep -cE '^\| [0-9]+ \|' docs/features/backlog.md` |
| 逐条目单发扫描 | `grep -n '每搜索一个模组' docs/spec/11-round-011-instructions.txt` |
| 物理位置口径扫描 | `grep -n 'GEOID_NOT_AVAILABLE' docs/research/13-platform-api.md` |
| Win7 目标扫描 | `grep -n 'require at least Windows 10' docs/research/13-platform-api.md` |
| 问题全集完整性 | `grep -cE '^\| Q-[A-H][0-9]' docs/records/open-questions.md` |
| 原版 `/talk` 扫描 | `grep -c '未出现' docs/research/16-server-platform.md` |
| ops.json 回写扫描 | `grep -c 'writes the whole list back' docs/research/16-server-platform.md` |
| src/ 空扫描（013 轮前） | `test -z "$(git ls-files src/)"`，013 轮起改为非空断言 |
| Rust 构建 | `cargo build --release --offline` |
| Rust 测试 | `cargo test --offline`，当前 141 passed / 0 failed |
| dispatcher 分项 | `cargo test --offline dispatcher::`，47 passed（json 7 / task 8 / mode 12 / launcher 20） |
| lightweight 分项 | `cargo test --offline lightweight::`，38 passed（login 8 / download 12 / loaders 7 / view 11） |
| dispatcher / lightweight 依赖 | `grep -c 'serde\|tokio\|async-std' Cargo.lock` 为 0 |
| UI 闸门触发 | 019 轮已触发；`test -f demos/ui-full-kcu-paper.html`；`test -f demos/preview/00-overview.png`；`ls demos/preview/*.png \| wc -l` = 48 |
| 图标与使用逻辑 | `grep -c '<symbol'` = 88；`grep -c 'class="logicbar"'` = 26；`grep -c '<section class="view'` = 26；对照 ux-logic-matrix.md C01-C20 |
| 021 产品文案 | `grep -c 'class="setid"'` = 0；`grep -c 'data-internal="1"'` = 4；`grep -o 'data-gotab="' \| wc -l` = 3；对照 docs/design/ui-product-copy.md P09 |
| 021 服务器逻辑 | `grep -c 'srv-row'` > 0；`21-servers.png` / `34-servers-join.png` / `35-servers-locked.png` 可见 |
| 022 异步与连接范围 | `grep -c 'budget-cell'` = 4；`python3 scripts/p09_scan.py` = P09_HITS 0；`36-servers-budget.png` / `37-servers-history.png` 可见 |
| 023 标识 / i18n / 崩溃 | `grep -c "sid:'sv-"` = 10；`41-i18n-en.png` / `39-servers-rename.png` / `42-settings-crash.png` 可见 |
| 第三方许可 | `test -f THIRD-PARTY-NOTICES.md`；关于页一级入口与七列表可见 |
| 风格与位置 | 对照 018 视觉 token 表逐值核验；`! grep -rE 'FCL\|揉纸启动器\|https?://' demos/ui-full-kcu-paper.html` |
| 交付形态 | UX HTML `demos/ui-full-*.html` 与流程 HTML `demos/round-0XX-*.html` 分开命名 |
| 场景覆盖 | 对照 docs/decisions/018-paper-ux.md S01-S20 逐项点图；仅 S02 为深色 |
| 排除项 | `cargo test --offline excluded_assets_cover_normal_ui_and_heavy_components` |
| 批量请求 | `cargo test --offline one_request_for_ten_ids_not_ten` |
| 弹窗关闭路径 | `cargo test --offline core::popup`，11 类全部可关 |
| 用户操作模拟 | `cargo test --offline core::userflow`，双击 / 指定 / 单参数 / 无残留 |
| 缓存有界与单飞 | `cargo test --offline core::cache`，8 passed，order ≤ capacity |
| 异步取消与回收 | `cargo test --offline core::asynk`，6 passed，live=0 |
| 泄漏归零 | `cargo test --offline core::leak`，5 passed |
| 工作流凭据 | `! grep -rE 'gh[p]_' .github/workflows/`，只写 secrets 引用 |
| 工作流语法 | `python3 -c "import yaml;yaml.safe_load(open('.github/workflows/ci.yml'))"` |
| 代码注释 | `! grep -rE '为了|目的是|方便用户|让用户能够|这样用户' src/` |

## 搭建前置条件

| 条件 | 012 值 | 013 值 |
| --- | --- | --- |
| D06 信号 | 未提供 | 已触发 F07/F08 |
| 005-blueprint.md | 未批准 | 已批准 F09 |
| X01-X04 用户拍板 | 未拍板 | F10 按正常情况与用户逻辑落地；CF 下载模块不在 L1 |
| Win7 兼容路径 | 未选 | Tier 3 + build-std F64 |
| 多架构范围 | 未定 | 全选；放弃 Win7 下 ARM64 F65/F66 |
| 地域判定口径 | 未定 | 物理位置 + 区域设置，软策略、只用于下载选择 F67/F52/F53 |
| 待拍板问题 93 条 | 未答复 | 已答复，细节按用户逻辑落地 |
| 开工时点 S1/S2 | 并列登记 | F07 判定「现在就是明天」，按 S1 开工 |
| src/ | 空 | L1 core 12 模块 + L2 dispatcher 5 模块 + L3 lightweight 5 模块已落地 |
| 工具链 | rustc/cargo 受阻 | rustc / cargo 1.99.1，腾讯 rustup 镜像 |

详见 docs/rules/build-preconditions.md 条件 1-6 与 docs/decisions/013-build-start.md。

## 未写入项

- L2 dispatcher、L3 lightweight：已实现、已验证；L4 headless 及以下 6 层未启动。
- 整页 UX 演示：016 轻量版；017 v2 作废；018 纸质版；019 28 视图；020 37 视图；021 去工程化、服务器页重做；023 稳定标识、i18n、崩溃反馈、延迟小字、实现路线，43 张产品视图 + 4 张内部证据图；用户按手感调整后先改演示与截图、确认后才改实现。
- 轻量 UI 实现：未进入构建；演示层深浅主题预览不写进单主题实现。
- 正常模式 UI 实现：014 轮定为样板参考、KCU 品牌重新实现，未进入构建。
- UI 设计稿品牌与字体：E09 卡点关闭，设计稿不直接复用。
- 图标 ICO 与裁切版本：未生成。
- 本项目 LICENSE：F61 决定 GPLv3，文件未生成。
- 特殊版私仓：已建仓，代码待用户明确同意后放入。
- 后端仓任何写请求：0。
- CF API 方法：workflow 设 secrets 占位，值由用户填写；具体调用方法 F17 由用户在完成时提供。
- 插件源默认选择、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 日志外传条款：未证实。
- 浏览器内渲染实测、GUI 点击端到端、rustc 交叉编译 Win7 目标：受阻。
- 011 遗留未证实项与 012 的 G 组默认：见 docs/decisions/013-build-start.md。

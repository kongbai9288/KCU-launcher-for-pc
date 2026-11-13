# 功能登记索引

每实现一个功能写一份 md，字段固定为：怎么运作、开放了什么、登记框架、用户使用逻辑、性能。模板见 _template.md。

| 编号 | 功能 | 框架 | 状态 | 文件 |
| --- | --- | --- | --- | --- |
| F001 | 正常模式 UI 设计稿 | normal.ui | 已批准 | normal-ui.md |
| F002 | 统一调度器 | dispatcher | 已实现、已验证 | dispatcher.md |
| F003 | 轻量启动器视图 | lightweight.view | 已实现、已验证 | lightweight.md |
| F004 | 无头模式启动器 | headless | 已批准 | headless.md |
| F005 | 正常启动器 | normal | 已批准 | normal-launcher.md |
| F006 | 手机连接 | normal.lan | 已批准 | lan.md |
| F007 | 一键开服 | normal.server | 已批准 | server.md |
| F008 | 日志 | core.log | 已批准 | log.md |
| F009 | 兜底与安全模式 | core.fallback | 已批准 | fallback.md |
| F010 | 跨进程统一信封 | core.ipc | 已批准 | envelope.md |
| F011 | UI 框架 | normal.ui | 已批准 | ui-framework.md |
| F012 | 正版凭据保护 | core.credential | 已批准 | credential-guard.md |
| F013-01 | 统一信封 | core.envelope | 已实现、已验证 | core-envelope.md |
| F013-02 | 诊断行 | core.diagnostics | 已实现、已验证 | core-diagnostics.md |
| F013-03 | 路径解析 | core.paths | 已实现、已验证 | core-paths.md |
| F013-04 | 配置 | core.config | 已实现、已验证 | core-config.md |
| F013-05 | 日志缓冲 | core.log | 已实现、已验证 | core-log.md |
| F013-06 | 启动参数 | core.args | 已实现、已验证 | core-args.md |
| F013-07 | 实例选择 | core.instance | 已实现、已验证 | core-instance.md |
| F013-08 | 弹窗与关闭 | core.popup | 已实现、已验证 | core-popup.md |
| F013-09 | 用户操作模拟 | core.userflow | 已实现、已验证 | core-userflow.md |
| F014-01 | 有界缓存 | core.cache | 已实现、已验证 | core-cache.md |
| F014-02 | 异步任务与多源竞速 | core.asynk | 已实现、已验证 | core-asynk.md |
| F014-03 | 泄漏探测与弱引用注册表 | core.leak | 已实现、已验证 | core-leak.md |
| F015-01 | JSON 解析底座 | dispatcher.json | 已实现、已验证 | dispatcher-json.md |
| F015-02 | LaunchTask 与任务集合 | dispatcher.task | 已实现、已验证 | dispatcher-task.md |
| F015-03 | ModeSelector 与兜底分级 | dispatcher.mode | 已实现、已验证 | dispatcher-mode.md |
| F015-04 | 统一调度主流程 | dispatcher.launcher | 已实现、已验证 | dispatcher-launcher.md |
| F016-01 | 轻量登录与三级回退 | lightweight.login | 已实现、已验证 | lightweight-login.md |
| F016-02 | Provider 与批量下载 | lightweight.download | 已实现、已验证 | lightweight-download.md |
| F016-03 | 加载器注册与安装 | lightweight.loaders | 已实现、已验证 | lightweight-loaders.md |
| F016-04 | 轻量极简视图状态 | lightweight.view | 已实现、已验证 | lightweight-view.md |
| F017-01 | 界面视觉全集与预览 | ui.demo | 已实现、已验证（演示层；风格项作废） | ui-visual-catalog.md |
| F018-01 | 纸质质感 UX 界面全集 | ui.demo | 已实现、已验证（演示层） | ui-paper-ux.md |
| F019-01 | 全功能使用逻辑补全 | ui.demo | 已实现、已验证（演示层） | ux-logic-completion.md |
| F019-02 | lucide 图标系统 | assets.icons | 已实现、已验证（演示层） | lucide-icon-system.md |
| F019-03 | 关于页第三方许可说明 | legal.notices | 已实现、已验证（演示层） | third-party-licenses-about.md |
| F020-01 | 导航瘦身与核心槽位锁定 | ui.demo / plugins.slots | 已实现、已验证（演示层） | nav-slot-lock.md |
| F020-02 | 设置九分组与自定义项归拢 | ui.demo / settings | 已实现、已验证（演示层） | settings-groups.md |
| F020-03 | 推荐位目录与排序自定义 | ui.demo / recommendations | 已实现、已验证（演示层） | recommendation-catalog.md |
| F020-04 | 服务器状态设置 | ui.demo / settings.status | 已实现、已验证（演示层） | server-status-settings.md |
| F020-05 | 上层实现第三方候选登记 | legal.notices | 已实现、已验证（演示层） | upper-layer-thirdparty.md |
| F020-06 | 可交接底层基线 | docs.design / handoff | 已实现、已验证（演示层） | handoff-baseline.md |
| F021-01 | 服务器自动连接与缓存权重 | ui.demo / servers | 已实现、已验证（演示层） | server-autoconnect.md |
| F021-02 | 游戏内服务器列表自动分析 | ui.demo / servers.scan | 已实现、已验证（演示层） | servers-dat-analysis.md |
| F021-03 | 双击进服与实例范围绑定 | ui.demo / servers.join | 已实现、已验证（演示层） | server-join-binding.md |
| F021-04 | 产品界面去工程化 | ui.demo / copy | 已实现、已验证（演示层） | ui-product-copy.md |
| F022-01 | 异步探测与设备连接范围 | ui.demo / servers.probe | 已实现、已验证（演示层） | server-async-probe.md |
| F022-02 | 失败历史分类与权重排序 | ui.demo / servers.rank | 已实现、已验证（演示层） | server-failure-history.md |

F001 状态含义：设计稿已获确认并逐字落盘；未实现、未进入构建。轻量模式排除见 docs/decisions/007-normal-ui.md。
F002-F012 状态含义：需求条目已登记；未实现、未进入构建。
F012 具体保护方案未批准，见 docs/rules/build-preconditions.md L4。
F013-01..09 状态含义：013 轮 D07 第一层 core 已落地，`cargo build --release --offline` 与 `cargo test --offline`（37 passed）实测通过；未进入上层组装、未部署、未做浏览器 / GUI 端到端。

## 013 轮 core 层

| 项 | 值 |
| --- | --- |
| 触发 | 003-remote.md D06（F07/F08）、005-blueprint.md 已批准（F09） |
| 顺序 | D07 第 1 层，其余层未启动 |
| 模块 | 9 个，src/core/ 下逐一登记 |
| 单份功能 md | 9 份，字段固定五段 |
| 弹窗关闭 | catalog 11 类全部可关，`assert` 级测试覆盖 |
| 用户操作模拟 | simulate 覆盖双击选实例、用户权重第一、单参数直达、无残留弹窗 |
| 工具链 | rustc / cargo 1.99.1，腾讯 rustup 镜像 |
| 未进入 | dispatcher 及以下 8 层、UI 渲染、真实窗口点击 |

## 011 轮功能输入

| 项 | 值 |
| --- | --- |
| 逐字原文 | docs/spec/11-features-input.txt，268 行，17096 字节 |
| 编号功能 | 1-55 连续，见 docs/features/backlog.md |
| 文件管理清单 | 175 个条目，分组索引见 backlog.md |
| 状态 | 全部已登记 / 未实现 / 未进入构建 |
| 单份功能 md | 每实现一个功能时按 _template.md 单独写一份 |

## 计划登记项

| 状态 | 值 |
| --- | --- |
| 待登记 | 无 |

009 轮曾登记「需求第 6、9、17、18、20、21 节功能块已全部登记」，010 轮核查发现 docs/spec/00-requirements.txt:17 的凭据保护机制未单独成文，已补 F012。docs/spec/00-requirements.txt:228 的玩家分支可取之处保留为调研候选项，不登记为实现项，见 docs/research/12-compliance.md。

## 登记约束

| 编号 | 约束 |
| --- | --- |
| G01 | 状态只声明实际达到的一层，不合并表述。 |
| G02 | 性能未实测时写「未实测」并标受阻，不写推测值。 |
| G03 | 轻量模式 md 不引用 normal.ui 资产，见 docs/checklists/ai-errors.md A26。 |
| G04 | 未证实字段不写进实现，见 docs/research/index.md R03。 |
| G05 | 12 份功能 md 均写明未实现与 src/ 为空，不写入构建状态。 |
| G06 | F012 方案未批准前，F004 不进入 D07 L4 搭建，见 docs/rules/build-preconditions.md。 |
| G07 | backlog.md 的 55 条编号与 175 个文件管理条目不写成已实现；单份功能 md 在实现时才生成。 |
| G08 | server-backlog.md 的 27 个编号位（缺 26）与 34 行 `·` 条目不写成已实现；单份功能 md 在实现时才生成。 |
| G09 | 012 与 011 的 13 组重复项并列登记；013 轮 F14 决定合并，见 docs/features/server-backlog.md。 |
| G10 | F013 各 md 的性能栏未实测进程级数值时写「未实测」，不写推测值。 |
| G11 | core 模块新增弹窗类型须进 `catalog()` 并通过 `missing_close_path()` 为空的检查。 |
| G12 | `src/` 内注释不写功能目的说明；技术不变量写进 md 与本索引，不写进代码注释。 |
| G13 | F014 三模块均为 std only；不引入 async runtime、不新增 Cargo.lock 条目。 |
| G14 | 缓存条目、order、inflight 三处都须在测试里有界或归零断言。 |
| G15 | 异步任务须 cancel + join 双重收口；`TaskGroup::drop` 兜底不得删除。 |
| G16 | 动 UI 的轮次须先交付整页 HTML 演示，规则见 docs/rules/ui-demo.md；运行逻辑演示不计入。 |
| G17 | dispatcher 不引入 serde 与 async runtime；Cargo.lock 不新增条目。 |
| G18 | 模式判定优先级固定：强制无头 > args > config > task > 自动判定；非法模式报错后用内置默认继续。 |
| G19 | 轻量视图不加载 normal.ui 与 13 项重资产；整页演示单独交付，不复用设计稿。 |
| G20 | 逐条目单发请求列为禁止项；一次请求带多个 id，每页 20，core.cache 单飞。 |
| G21 | 未证实字段不写进实现：加载器 version json 注入字段为空、WebView2 检测键由宿主注入、CF 源本层不暴露。 |
| G22 | 动 UI 的轮次须交 PNG 预览与总览拼图，HTML 单文件不再作为唯一可见交付。 |
| G23 | 样板只取配色、圆角、描边、卡片层次；位置重新组织，不照搬三栏拖拽与组件位置。 |
| G24 | 公告中心、详情、更新提示、首次启动引导等界面主动出图，不待用户逐项点名。 |
| G25 | 场景切换清弹窗残留；弹窗类场景单独渲染；流程结束 0 未关弹窗。 |
| G26 | 风格取自样板须逐项对照色板、纹理、衬线、圆角、窗口 chrome；不得另定配色冒充同源。 |
| G27 | UX HTML 与流程 HTML 分开命名；动 UI 的轮次主交付为 UX HTML + PNG 预览。 |
| G28 | 每个视图渲染前强制重载，避免主题与弹窗状态串到后续截图。 |
| G29 | 每个功能填满 L01–L12 使用逻辑骨架，缺一判未补全。 |
| G30 | 每个视图区块顶部有逻辑条：缓存时间、命中数、刷新、强制刷新、状态。 |
| G31 | 使用第三方代码须在关于页与发行物声明许可证与项目，构建状态如实。 |
| G32 | 设置与关于固定在锁定槽位，插件与更新包不可改写。 |
| G33 | 推荐位与服务器状态的自定义项全部落在设置。 |
| G34 | 上层实现采用第三方代码，逐项取得 LICENSE 全文后才引入依赖。 |
| G35 | 添加服务器后自动连接，结果缓存为排序权重；锁定置顶、连不上沉底。 |
| G36 | 服务器显示照游戏内，不另做状态配色与文案。 |
| G37 | 产品界面不写工程叙事；内部证据页不进导航与总览。 |
| G38 | 自动连接异步、并发有上限、队列有界、可取消；总额卡在设备档位内。 |
| G39 | 新加服务器一定连一次但不扩总额度；范围外保留上次结果、不发请求。 |
| G40 | 无成功案例且测过的不主动重连、按缓存权重排中段；曾成功但本轮失败沉底；锁定不受影响。 |

## 018 轮纸质 UX 界面

| 项 | 值 |
| --- | --- |
| 输入 | docs/spec/18-round-018-instructions.txt，1 行 122 字节 |
| 决策 | docs/decisions/018-paper-ux.md W01/W02、D01-D10、S01-S20、E01-E05 |
| UX HTML | demos/ui-full-kcu-paper.html，1440×900 桌面窗口，20 视图，离线可点 |
| 预览 | demos/preview/ 20 张 PNG + 00-overview.png 总览 + index.md |
| 渲染脚本 | scripts/render_ui.py，本地 chromium，每视图强制重载，0 次远端请求 |
| 规则 | docs/rules/ui-demo.md G11-G12、轮次状态表 018 行 |
| 源码 | `src/` 本轮无变化；演示与实现分开落盘 |
| 017 处置 | ui-full-kcu-v2.html 风格取错，保留文件但标记作废；预览目录全部覆盖 |
| 手感回路 | 先看图 → 提意见 → 先改演示与截图 → 确认后才改实现 |

## 017 轮界面视觉预览

| 项 | 值 |
| --- | --- |
| 输入 | docs/spec/17-round-017-instructions.txt，1 行 259 字节 |
| 决策 | docs/decisions/017-visual-preview.md D01-D10、S01-S15 |
| 整页演示 | demos/ui-full-kcu-v2.html，15 场景，布局重排，离线可点 |
| 预览 | demos/preview/ 16 张 PNG，含 00-overview.png 总览 |
| 渲染脚本 | scripts/render_ui.py，本地 chromium，0 次远端请求 |
| 预览索引 | demos/preview/index.md |
| 规则 | docs/rules/ui-demo.md G07-G10、轮次状态表 017 行 |
| 源码 | `src/` 本轮无变化；演示与实现分开落盘 |
| 手感回路 | 先看图 → 提意见 → 先改演示与截图 → 确认后才改实现 |

## 016 轮 L3 lightweight

| 项 | 值 |
| --- | --- |
| 输入 | docs/spec/16-round-016-instructions.txt，逐字「干」4 字节 |
| 决策 | docs/decisions/016-build-continue.md D01-D08、L01-L15、U01-U09 |
| 模块 | src/lightweight/{login,download,loaders,view,mod}.rs |
| 单份功能 md | 4 份 + F003 更新，字段固定五段 |
| 测试 | `cargo test --offline` 141 passed / 0 failed；lightweight 占 38 项 |
| 构建 | `cargo build --release --offline` 通过；Cargo.lock 未变 |
| UI 闸门 | **已触发**，docs/rules/ui-demo.md 016 段 |
| 整页演示 | demos/ui-full-lightweight.html，6 分区、5 状态、11 弹窗、离线可点、KCU 标识 |
| 运行逻辑演示 | demos/round-016-lightweight.html，13 节点，不计入 G01 |
| 手感回路 | 演示先落盘 → 用户按手感调整 → 先改演示 → 确认后才改实现 |
| 未进入 | L4 headless 及以下 6 层、UI 实现、CF 下载模块、特殊版代码 |

## 015 轮 L2 dispatcher

| 项 | 值 |
| --- | --- |
| 输入 | docs/spec/15-round-015-instructions.txt，4 片段 |
| 决策 | docs/decisions/015-build-continue.md D01-D08、U01-U08 |
| 模块 | src/dispatcher/{json,task,mode,launcher,mod}.rs |
| 单份功能 md | 4 份 + F002 更新，字段固定五段 |
| 测试 | `cargo test --offline` 103 passed / 0 failed；dispatcher 占 47 项 |
| 构建 | `cargo build --release --offline` 通过 |
| UI 闸门 | docs/rules/ui-demo.md，本轮不触发 |
| 演示 | demos/round-015-dispatcher.html 为运行逻辑演示，不是整页 UI 演示 |
| 未进入 | L3 lightweight 及以下、UI 实现、CF 下载模块、特殊版代码 |

## 014 轮 core 扩展

| 项 | 值 |
| --- | --- |
| 输入 | docs/spec/14-round-014-instructions.txt，7 片段 |
| 决策 | docs/decisions/014-build-continue.md D01-D08 |
| 模块 | core.cache / core.asynk / core.leak |
| 单份功能 md | 3 份，字段固定五段 |
| 测试 | `cargo test --offline` 56 passed / 0 failed；新增 19 项 |
| 构建 | `cargo build --release --offline` rlib 610080 字节 |
| 工作流 | `.github/workflows/ci.yml`，secrets 占位、有界缓存、并发取消、并行 job |
| 私仓 | `kongbai9288/KCU-launcher-special`，private，仅 README 占位 |
| UI 稿 | 降级为样板与交互参考，KCU 品牌重新实现 |
| 未进入 | L2 dispatcher 及以下 8 层、UI 实现、CF 下载模块、特殊版代码 |

## 012 轮开服器输入

| 项 | 值 |
| --- | --- |
| 逐字原文 | docs/spec/12-server-features-input.txt，64 行，4970 字节 |
| 编号功能 | 1-27，其中 26 缺号、1 与 25 与文字连写 |
| `·` 条目 | 字符 35、独立行 34，分组 A / B 共 26 行索引（GA1-GA18、GB1-GB8） |
| 登记表 | docs/features/server-backlog.md |
| 状态 | 全部已登记 / 未实现 / 未进入构建 |
| 待拍板问题 | docs/records/open-questions.md，93 条 |
| 开工闸门 | docs/decisions/012-server-input.md D03；Q-H01 至 Q-H06 未满足 |

状态值：已批准 / 已实现 / 已验证 / 已合并 / 已进入构建 / 已部署 / 行为已确认。每份功能 md 只声明实际达到的一层。

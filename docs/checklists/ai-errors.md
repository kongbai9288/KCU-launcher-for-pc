# AI 防错清单

来源：docs/spec/00-requirements.txt 第 6、7.3、8、9、18 节。

扫描域：`src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/`。
`docs/spec/`、`docs/checklists/`、`docs/rules/`、`docs/verification/`、`docs/index.md` 为规格、词表与验证产物，含禁用词字面量，不纳入措辞扫描。

| 编号 | 禁止项 | 检查命令 |
| --- | --- | --- |
| A01 | 套话开场 | `! grep -rE '好的|没问题|让我来|接下来我们将|需要注意的是' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A02 | 无信息量强调 | `! grep -rE '值得注意的是|需要强调的是|重要的是|务必注意' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A03 | 总结式重复 | `! grep -rE '综上所述|总而言之|总的来说|简而言之' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A04 | 假装热情、拟人化安慰、emoji、装饰性分隔线、非功能性加粗 | `! grep -rE '很棒的问题|别担心|没关系|慢慢来|相信你' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A05 | 注释里的修饰性副词 | `! grep -rE '优雅地|巧妙地|完美地' src/ demos/` |
| A06 | 教程式口吻 | `! grep -rE '你将学会|本文将介绍|让我们看看' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A07 | 空泛承诺 | `! grep -rE '后续会完善|暂时这样|以后优化' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A08 | 解释性内容 | `! grep -rE '为什么|这意味着|动机|权衡|架构理由' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A09 | 空捕获、捕获后返回空值 | 代码审查 |
| A10 | 只写正常路径；未处理空值、空集合、越界、超时、编码 | 代码审查 + 边界测试 |
| A11 | 顺手改无关文件 | `git diff --name-only` 逐项核对本轮范围 |
| A12 | 硬编码绝对路径、架构名、密钥 | `! grep -rE 'C:\\\\|gh[p]_|github_pat_|x-api-key *=' src/ demos/ README.md` |
| A13 | 路径散落多处 | 路径模块单一入口 |
| A14 | 跨进程消息无统一信封、无请求标识、无统一错误 | 代码审查 |
| A15 | 谎报验证结果、编造命令输出 | 每条结论附真实命令与输出 |
| A16 | 改测试、加跳过、删测试来让分支通过 | 测试文件 SHA-1 锁定 |
| A17 | 把凭据写入仓库 | `! grep -rqE 'gh[p]_' .` |
| A18 | 每轮开工未完整读本文档与需求原文 | 按 docs/index.md 读取命令执行 |
| A19 | 用时间戳冒充后续动作证据 | 证据只认 8.1 原始产物核对 |
| A20 | 中间态四值 | 每条结论落到四值之一 |
| A21 | 403 policy_default_denied 写成服务故障 | `! grep -rE '服务不可用|服务故障' docs/research/` |
| A22 | 示例配置值当成默认值 | `grep -n 'broadcast-rcon-to-ops' docs/research/06-server.md` 与 https://minecraft.wiki/w/Server.properties 逐项比对 |
| A23 | 四值使用「部分已证实」 | `! grep -rE '部分已证实' docs/research/ docs/features/ docs/records/ docs/decisions/` |
| A24 | 锚点写「同上」或裸域名短名 | `! grep -rE '同上' docs/research/`；逐行核对 URL 完整性 |
| A25 | 设计稿品牌元素进入实现代码 | `! grep -rE 'FCL|揉纸启动器' src/ 2>/dev/null` |
| A26 | 轻量模式引用正常模式 UI 资产 | `! grep -rE 'assets/ui|normal-mode-v3' src/ 2>/dev/null` |
| A27 | 逐字副本字节被改动 | `cmp` 来源与落盘；SHA-1 双端一致 |
| A28 | 工具摘要与一手原文不一致时采用摘要（关联 A22） | `grep -n 'Introduced in' docs/research/06-server.md`；结论只取 EVIDENCE 原句 |
| A29 | 第三方推广页排名写成选型结论（关联 R02） | `! grep -rE '表现得最优|使用人数最多|社区反馈最积极' docs/features/ docs/decisions/` |
| A30 | 未取得一手原文就写死构建参数或进程参数 | `grep -n '未证实' docs/research/11-runtime.md`；构建配置生成前逐项核对 |
| A31 | 功能登记写成已实现（关联 9.3 状态分层） | `test -z "$(grep -L '未实现' docs/features/dispatcher.md docs/features/lightweight.md docs/features/headless.md docs/features/normal-launcher.md docs/features/lan.md docs/features/server.md docs/features/log.md docs/features/fallback.md docs/features/envelope.md docs/features/ui-framework.md docs/features/credential-guard.md)"` |
| A32 | 服务条款原文未取得就写死镜像缓存或共享密钥（关联 18.6） | `grep -n 'CF01\|CF02\|CF03\|CF04' docs/research/12-compliance.md` |
| A33 | 两个不同上游返回同名同 sha 的 tag 当成版本号（关联 A28） | `grep -n 'v99.99' docs/research/12-compliance.md`；结论标已失败 |
| A34 | 许可证逐字副本重复落盘 | `sha1sum docs/licenses/*.txt docs/licenses/*.md` 逐项核对；同 sha 只留一份 |
| A35 | 功能 md 的验证命令输出写推测值（关联 A15） | 每条 `grep -c` / `grep -n` 先实跑再写入 |
| A36 | 逐条目单发网络请求（关联 14-batch-network.md N01） | `grep -n '每搜索一个模组' docs/spec/11-round-011-instructions.txt` |
| A37 | 把 Windows 区域设置当成物理位置（关联 13-platform-api.md P01-P04） | `grep -n 'GEOID_NOT_AVAILABLE' docs/research/13-platform-api.md` |
| A38 | 用 GetVersionEx 判定 OS 版本（关联 OS03） | `grep -n 'versionhelpers' docs/research/13-platform-api.md` |
| A39 | 写死 API 基址、端口、图标路径、语言包路径（关联 K01-K07） | `grep -n 'K01' docs/research/14-batch-network.md` |
| A40 | 把 Win10+ Rust 目标当成 Win7 可用（关联 RW01-RW04） | `grep -n 'require at least Windows 10' docs/research/13-platform-api.md` |
| A41 | 对只读后端仓发写请求（关联 BR01-BR02） | `grep -n '只允许' docs/research/15-input-survey.md`；每轮核对请求方法 |
| A42 | 把 id 具体值写进文档（关联 PL03、PL05） | `grep -n '未读取、未写入' docs/research/15-input-survey.md` |
| A43 | 编号功能登记漏条（关联 backlog.md 55 条） | `grep -cE '^\| [0-9]+ \|' docs/features/backlog.md` |
| A44 | 插件开源许可页缺 5 字段（关联 OL01） | `grep -n 'OL01' docs/research/15-input-survey.md` |
| A45 | 拼接开源代码后不做源与产物对比（关联 OL05） | `grep -n 'OL05' docs/research/15-input-survey.md` |
| A46 | 把 `/talk` 当原版命令（关联 CM02） | `grep -c '未出现' docs/research/16-server-platform.md` |
| A47 | 运行期监听 ops.json 判定 op 变更（关联 OP02） | `grep -c 'writes the whole list back' docs/research/16-server-platform.md` |
| A48 | 把区域设置或 GEOID 当物理位置（关联 A37） | `grep -c '不等于物理位置' docs/checklists/windows-errors.md` |
| A49 | 把 mclo.gs 上传当本地导出（关联 MC03） | `grep -c '一键上传 mclo.gs' docs/features/server-backlog.md` |
| A50 | mrpack 导入不做路径穿越校验（关联 MS07） | `grep -c 'exit the Minecraft instance directory' docs/research/16-server-platform.md` |
| A51 | 待拍板问题漏条（关联 open-questions.md 93 条） | `grep -cE '^\| Q-[A-H][0-9]' docs/records/open-questions.md` |
| A52 | 未答复 Q-H 组就写 src/（关联 :249） | 013 轮起改为 `test -n "$(git ls-files src/)"`，D06 已触发 |
| A53 | 弹窗缺关闭路径（关联 013 H03） | `cargo test --offline every_catalog_popup` |
| A54 | 单参数无法加入服务器（关联 013 U01） | `cargo test --offline single_arg` |
| A55 | 双击服务器时用户权重不排第一（关联 013 U02） | `cargo test --offline user_choice_ranks_first` |
| A56 | 流程结束残留未关弹窗（关联 013 H06） | `cargo test --offline no_popup_is_left_open` |
| A57 | 缓存无容量上限或 order 无限增长（关联 014 D04/D06） | `cargo test --offline capacity_bounds_entry_count`、`order_stays_bounded_after_many_inserts` |
| A58 | 同 key 并发重复加载（关联 011 聚合请求、014 D04） | `cargo test --offline single_flight_loads_once` |
| A59 | 多源下载一个完成后其余未取消、线程未 join（关联 011 第 30 条、014 D05） | `cargo test --offline race_returns_first_and_cancels_other_sources`、`drop_joins_without_explicit_shutdown` |
| A60 | 活跃计数不归零或弱引用注册表未清理（关联 014 D06） | `cargo test --offline core::leak` |
| A61 | 工作流出现凭据字面量（关联 014 D01） | `! grep -rE 'gh[p]_' .github/workflows/` |
| A62 | 动 UI 的轮次未交付整页 HTML 演示（关联 015 D02） | `test -f demos/ui-full-*.html`（触发轮次）；规则 docs/rules/ui-demo.md |
| A63 | 把运行逻辑演示当成整页 UI 演示（关联 015 D05/U07） | `grep -n '运行逻辑' demos/round-015-dispatcher.html`；ui-full 命名核对 |
| A64 | dispatcher 引入 serde 或 async runtime（关联 015 D06 L02） | `grep -c 'serde\|tokio\|async-std' Cargo.lock` 为 0；`cargo tree --offline` 只有 kcu-core |
| A65 | 模式判定优先级写反或非法模式直接崩（关联 015 L05） | `cargo test --offline args_override_beats_config`、`invalid_mode_reports_and_falls_back_without_crashing` |
| A66 | 连续失败不进安全模式、不导出诊断包，或 UI 模式残留未关弹窗（关联 015 L06/L09） | `cargo test --offline consecutive_failures_enter_safe_mode_then_export_bundle`、`normal_mode_registers_and_closes_every_popup` |
| A67 | 动轻量视图却未交付整页 HTML 演示（关联 016 D02） | `test -f demos/ui-full-lightweight.html`；docs/rules/ui-demo.md 016 段 |
| A68 | 轻量实现复用 normal.ui、设计稿、双主题实现或内嵌文件管理器（关联 016 L10/L11） | `cargo test --offline excluded_assets_cover_normal_ui_and_heavy_components`、`view_uses_single_theme`、`file_manager_is_system_panel_only` |
| A69 | 逐条目单发请求或未做单飞缓存（关联 011 D12、016 L07） | `cargo test --offline one_request_for_ten_ids_not_ten`、`repeated_batch_is_single_flight` |
| A70 | 写死加载器 version json 字段、WebView2 检测键或暴露 CF 源（关联 016 L05/L08/L09） | `cargo test --offline installed_loader_returns_record_without_schema_fields`、`webview2_availability_is_injected_not_hardcoded`、`curseforge_source_is_not_exposed` |
| A71 | 游戏运行期残留常驻后台进程，或弹窗流程后未清零（关联 016 L13/L14） | `cargo test --offline game_runtime_has_no_resident_launcher`、`flow_ends_with_zero_open_popups` |
| A72 | 动 UI 却只交 md/HTML、未交 PNG 预览与总览（关联 017 D01/G07） | `test -f demos/preview/00-overview.png`；`ls demos/preview/*.png \| wc -l` |
| A73 | 照搬样板三栏拖拽、组件位置或复用 FCL 品牌（关联 017 D03-D05） | `! grep -rE 'FCL\|揉纸启动器\|https?://' demos/ui-full-kcu-v2.html`；布局按 D04 核对 |
| A74 | 漏公告中心、公告详情、更新提示、首次启动引导等界面（关联 017 D06/D07） | 对照 docs/decisions/017-visual-preview.md S01-S15 逐项点图 |
| A75 | 场景切换残留上一个弹窗，导致多张截图内容相同（关联 017 实测） | `dismissOverlay()` 在 `show()` 开头；逐张核对 `demos/preview/*.png` 不重复 |
| A76 | 另定一套配色冒充「风格取自样板」（关联 018 W01） | 对照 docs/decisions/018-paper-ux.md 视觉 token 表逐值核验 |
| A77 | 用流程 HTML（步骤节点 / 状态机）替代 UX HTML 交付界面（关联 018 W02/G12） | 命名核对 `demos/ui-full-*.html` vs `demos/round-0XX-*.html`；主交付须含 PNG |
| A78 | 仅改 hash 不重载导致主题串场（关联 018 E01） | `scripts/render_ui.py` 每场景带 `?r=<i>`；核对仅 S02 为深色 |
| A79 | 深色主题漏窗口级 color 覆盖导致文字不可读（关联 018 E03） | `.win[data-theme="dark"]` 含 `color:var(--ink)`；逐张核对深色图可读性 |
| A80 | 用字符或 emoji 冒充 lucide 图标（关联 019 D01） | 字符图标残留扫描 = 0；`grep -c '<symbol'` = 88；引用缺失数 = 0 |
| A81 | 某个视图缺缓存 / 刷新 / 推荐逻辑证据（关联 019 D03/D05） | `grep -c 'class="logicbar"'` = 22；对照 docs/design/ux-logic-matrix.md C01-C12 |
| A82 | 第三方许可只写在文档、关于页没有入口或七列表（关联 019 D07） | `test -f THIRD-PARTY-NOTICES.md`；`demos/preview/22-licenses.png` 可见七列 |
| A83 | 把文档层调研组件写成已进入构建（关联 019 D08） | 构建状态列逐行核对：演示层 1 组、文档层 13 组、src/ 0 项 |
| A84 | 图标拼接字面量残留进 HTML（关联 019 实测） | `! grep -n "I('" demos/ui-full-kcu-paper.html`；逐张核对按钮文字 |
| A85 | 把配置类功能挂到一级导航（关联 020 D02） | 一级导航仅 9 项日常操作；AI 接口 / 缓存 / 刷新 / 状态 / 无头 / 许可不在其中 |
| A86 | 设置或关于被插件与更新包覆盖（关联 020 D05） | `grep -c 'slot-core'` = 1；两个 locked 徽章；冲突拒绝演示可见 |
| A87 | 推荐位只写 6 处、服务器状态只写字段不写设置项（关联 020 D10-D11） | 10 位目录与 6 类状态逐项核对；设置 ID 列完整 |
| A88 | 上层第三方代码写成已进入构建（关联 020 D13） | 12 组候选全部标「候选 · 未进构建」；`src/` 与 Cargo.lock 无变化 |
| A89 | 新对话丢上下文（关联 020 D14） | `docs/design/handoff.md` 6 步与 H01-H08 不可变边界；关于页交接卡片 |
| A90 | 把内部工程叙事写进产品界面（关联 021 D01） | `grep -c 'class="setid"'` = 0；`grep -c 'data-internal="1"'` = 4；产品导航无槽位 ID / 交接基线 / 候选状态 |
| A91 | 把服务器状态做成用户配 SLP 参数（关联 021 D09） | 设置分组名「服务器与连接」；无探测方式 / 超时 / 状态文案颜色；改为自动连接、排序、读取游戏内列表、双击进服 |
| A92 | 锁定项被连接失败下沉（关联 021 D05 / 用户逻辑） | `35-servers-locked.png` 中锁定项保持靠前；`srvRank` 中 lock 返回 0 |
| A93 | 同步遍历全部服务器状态（关联 022 D01） | `srvProbe` 用 worker-pull 异步队列；`srvSync` 已移除；`grep -c 'srvSync'` = 0 |
| A94 | 服务器越多连接数越涨（关联 022 D02-D04） | `DEVICE` 档位表 limit / concurrency 双上限；新服仍占同一份额度，`buildPlan` 用 slice(0,limit) |
| A95 | 把无成功记录的服务器沉底或反复重连（关联 022 D06） | `neverSuccess` 分组不进 probe 计划；`srvRank` 给 300 档中段；`37-servers-history.png` 可见 |
| A96 | 取消后仍写新结果（关联 022 A04） | `applyResult` 前检查 `PROBE.cancelled`；取消后 inflight 归零、队列清空 |
| A97 | 用显示名拼目录 / 缓存键（关联 023 Q1） | SERVERS 每项带 `sid`；`data-lock` / `data-join` / `data-rename` 全用 sid；`C:\KCU\servers\<sid>` 只含白名单字符 |
| A98 | 界面文案写死在渲染代码里（关联 023 Q2） | `grep -c 'data-i18n='` > 500；动态文本走 `tr()`；`41-i18n-en.png` 英文可见 |
| A99 | 崩溃信息默认外传（关联 023 Q5） | `setCrashOn` 默认不记录、`setCrashAddr` 可空、脱敏默认开、发送前确认 |
| A100 | 拿第三方库不登记许可证（关联 023 H02） | 关于页 22 组、`THIRD-PARTY-NOTICES.md` 新增 6 组候选均标「未进构建」 |

## 输出结构

1. 本轮行动或结论
2. 时间戳回显
3. 本轮目标与范围
4. 设计与代码
5. 运行逻辑演示
6. 自我批判
7. 四值判决
8. 独立验证证据
9. 自评
10. 通过标记或未通过
11. 本轮文档更新
12. 唯一下一步

## 冲突优先级

独立验证结论 > 自评 > 时间戳；四值判决 > 通过标记；仓库内容边界 > 文档完整性；幻觉红线 > 输出结构完整性；用户当轮明确指令 > 本文件规则；安全与许可证合规 > 功能进度。

## 028 轮新增

| 编号 | 防错项 |
| --- | --- |
| A67 | 日志格式不写死单一模式：版本 / 加载器 / 插件前缀不同，用多组正则 + 捕获组索引 + 用户自定义。 |
| A68 | 事件与目录键用 sid，不用玩家名；名字可重复且可自定义。 |
| A69 | 检索结果里 `github.org` 这类异常域名标未证实，不据此复制仓库或许可证。 |

## 029 轮新增

| 编号 | 防错项 |
| --- | --- |
| A70 | 引入缓存/并发库前先核 `Send + Sync`：`unsync` 变体可能内部用 `Rc<K>`，外面套 `Mutex` 也不能跨 `Arc` 共享。 |
| A71 | 裁 manifest 时删了 optional 依赖，必须同步删 `[features]` 里对它的引用，否则 cargo 报 `feature ... includes ... which is neither a dependency nor another feature`。 |
| A72 | 单飞广播要留持久 `completed` 状态：只在完成时 drain waiters，后到等待者会挂到空队列上超时。 |

## 030 轮新增

| 编号 | 防错项 |
| --- | --- |
| A73 | 待拍板问题不能只写一句问号：必须给具体使用场景、每个选项的后果、以及与其他问题的耦合关系，否则用户无法判断。 |
| A74 | 参数解析库化时保留项目语义层（别名、统一错误面、业务判定），不要把业务字段一起塞进库调用里。 |
| A75 | 引用 013 轮答复前先核它原本问的是什么：Q-D02「每次请求」是 AI 接口授权，不能默认复用到日志触发的服务器自动化。 |

## 031 轮新增

| 编号 | 防错项 |
| --- | --- |
| A76 | 用户答复同时出现字母选项（如「A」）和程度词（如「最严格」）时，以程度词为准，并登记字母歧义待确认，不擅自按字母取项。 |
| A77 | 「只允许只读动作」的功能不要沿用功能名里的「自动命令」当作已实现发命令；必须写明实际形态与后果。 |
| A78 | 每次确认的严格口径遇到高频触发，用「一条待确认 + 累计计数」收敛弹窗数量，不得把多次命中合并成一次确认后执行。 |

## 032 轮新增

| 编号 | 防错项 |
| --- | --- |
| A79 | 「默认最严格」与「用户可选松档」并存时，必须写明默认档、切换主体、二次确认、回退入口与插件禁令，不能把「可选」写成默认放宽。 |
| A80 | 多档位要单调变松，逐档核对「确认粒度」与「动作范围」两个维度，不能出现更松的档反而问得更多。 |
| A81 | 演示层新增文案用语义 key（如 `auto.tier.*`），不把中文文本当 `data-i18n` key；切语言时动态渲染的区块要一起重渲。 |

## 033 轮新增

| 编号 | 防错项 |
| --- | --- |
| A82 | 用户上一句里的单字母（A/B/C）不一定指选项编号；结案歧义时保留原判定与历史登记，证实是缩写就不回退口径。 |
| A83 | 换错误类型时逐个检查测试是否对 `Result` 整体做 `PartialEq` 比较；`anyhow::Error` 无 `PartialEq`，改 `unwrap()` 后比值，断言强度不降。 |
| A84 | 预告过的替换路线核完发现语义不匹配，要写清「为什么不换」和「改走哪块」，不能静默跳过也不硬换。 |

## 034 轮新增

| 编号 | 防错项 |
| --- | --- |
| A85 | 换成第三方版本库时，先核实「相等」是否包含 build 元数据；`semver::Version` 的 `==` 包含，忽略要用 `cmp_precedence`。 |
| A86 | 普通三段版本不能直接交给 `VersionReq`（Cargo 风格会当 caret 放宽），必须由项目显式判定范围符号后才走范围解析。 |
| A87 | 替换若带来新能力（范围匹配、元数据归一），要在决策里标成「扩展」并逐条列出行为差异，不能写成纯等价替换。 |

## 035 轮新增

| 编号 | 防错项 |
| --- | --- |
| A88 | 预告过的库替换路线，要拿上游 manifest 的真实 edition / MSRV / 依赖行数判定，不能用「我记得这个库很小」。 |
| A89 | 换配置格式（JSON → TOML）属于行为变更，不算库替换；磁盘格式与插件读写面都要一起核。 |
| A90 | 引 derive 型库前先数一下自写样板行数；本地 enum 没有 Display/Error 实现时，引 thiserror 不删任何一行。 |
| A91 | 「映射表收敛」只表示自写通用算法换完，不能写成项目做完；上层未启动能力要逐项列清。 |

## 036 轮新增

| 编号 | 防错项 |
| --- | --- |
| A92 | 上游 crate 的依赖「全部 optional」不等于零闭包，要核 cfg 门是否真的把引用外部 crate 的模块排除。 |
| A93 | 关掉 default features 后，features 表里引用已删 optional dep 的行必须一并删除，否则目录源解析会失败（033 的 log 已踩过一次）。 |
| A94 | 版本决策不要直接用 `Version` 的 `>` / `==`（含 build 元数据），统一走 034 的 `cmp_precedence`。 |
| A95 | 签名校验必须排在版本决策之前；任何解析失败都返回「保留旧插件」，不能落到安装分支。 |

## 037 轮新增

| 编号 | 防错项 |
| --- | --- |
| A96 | 「两个插件哈希一致」先判是身份哈希还是包内容哈希；内容哈希一致时字节相同，版本号不该变，硬套升级会写出永远不触发的分支。 |
| A97 | 用户当轮口径覆盖前序自动安装规则时，要在决策里显式写「撤回 / 覆盖」，不能两条并存。 |
| A98 | 插件 SVG 检查只做格式与外链兜底，不加内容白名单；`href="#..."` 内部片段必须放行。 |
| A99 | 弹窗 catalog 新增类型后，所有硬编码弹窗数的断言要一起核（`core/popup.rs`、`lightweight/view.rs`）。 |
| A100 | 动界面的轮次，`src/` 里只能落业务逻辑；渲染层留在 UX 演示等确认，不能把演示 HTML 当成实现完成。 |

## 038 轮新增

| 编号 | 防错项 |
| --- | --- |
| A101 | vendor 里带 `[lints] workspace = true` 或 optional `rustc-std-workspace-core` 的 crate，脱离原 workspace 后 cargo 解析会失败，必须裁段并在决策里登记裁了什么。 |
| A102 | 往上游 manifest 插字段前先查键是否已存在；`readme` 重复键会让整个目录源解析失败。 |
| A103 | Windows 目标依赖在 Linux 仍进 lock 解析，vendor 不能只放 Unix 侧那几个 crate。 |
| A104 | `libloading::Symbol` 只可在 `Library` 存活期内用；存进长期结构体就是悬垂句柄，取数值后让 Library 自行 Drop。 |
| A105 | `cargo check --target` 只证明编译，不能写成「Win7 运行时已验证」；MSVC 与运行时要分开登记。 |
| A106 | 集成测试用 rustc 现编 cdylib 属验证脚手架，不进产品启动路径，耗时也要如实写进报告。 |

## 039 轮新增

| 编号 | 防错项 |
| --- | --- |
| A107 | `extern "C"` 边界上 Rust panic 会 abort 整个进程，`catch_unwind` 抓不到；不要把「同进程动态库」写成「崩溃隔离」。 |
| A108 | `catch_unwind` 与 foreign exception 交互是 UB；跨 FFI 的符号只读取数值，不在宿主进程执行插件函数。 |
| A109 | `Library::close()` 成功不等于已卸载（musl / macOS TLS）；错误要登记，Drop 的静默忽略不能当成功。 |
| A110 | `Child` 没有 Drop 实现，错误路径早返回会泄漏运行中的进程；子进程路线必须显式 `wait` 或 `kill`。 |
| A111 | `ScopedJoinHandle::join` 消耗 self，不能在 `filter(|h| ...)` 的共享引用上调用；用 `into_iter().filter_map`。 |
| A112 | 网关超时时把全量测试拆成 `--lib` / `--test` / `check` 三段，并用 `OnceLock` 缓存编译夹具；拆命令不算降验收项。 |
| A113 | 不为单测造只被测试调用的生产函数（`has_id` / `reverse_order` 已删），行为验证移到真加载集成测试。 |

## 040 轮新增

| 编号 | 防错项 |
| --- | --- |
| A114 | 引网络栈前先拉真实 manifest 逐字段核闭包、MSRV、edition、C 构建链与 Windows 分支，不凭印象判「轻量」。 |
| A115 | `Uri::builder().authority()` 不做严格主机名校验；要严格校验用 `Uri::from_str` 解析完整串。 |
| A116 | CI 的 `hardcode` / `credential` / `wording` job 要按 job 内容实跑，不能只验 YAML 语法；037 遗留的两处测试字面量就是这么漏到 040 的。 |
| A117 | 源码里出现 `https?://` 连续串会被 CI 拦；测试需要完整 URL 时用 `concat!` 分部件拼接，运行时值不变。 |
| A118 | vendor 里带 `[workspace]` / `[lints] workspace = true` / dev-dependencies 的 crate 必须裁段，并登记裁了什么。 |
| A119 | Win7 上 HTTPS 的前置不只在代码：KB3140245、DefaultSecureProtocols、SChannel 配置、rustls 的 ProcessPrng 补丁要分开登记，不能写成「编出来就能跑」。 |

## 041 轮新增

| 编号 | 防错项 |
| --- | --- |
| A120 | 引 UI 宿主或崩溃分析前先拉真实 manifest 与官方平台支持页，核平台分支、C/系统库、MSRV、edition 与 Win7 运行时口径。 |
| A121 | 官方写「最后支持版本 / 不再支持 / 未自动测试」时，不能写成「编出来应该能跑」；须把取舍摆给用户。 |
| A122 | 用项目自有类型前先读它的真实方法名（本轮 `Envelope` 是 `field()` 不是 `get()`），不凭印象调。 |
| A123 | 仓库路径要实核，组织改名后旧路径会 404；取不到就标受阻，不猜来源。 |
| A124 | 裁 vendor manifest 时，optional 依赖与引用它的 feature 行要一起裁，否则目录源解析失败。 |
| A125 | unsafe trait（`HasWindowHandle`）要求句柄真实有效；core 层没有窗口时不实现、不伪造。 |
| A126 | 句柄类型层不得推导 WebView2 可用性；可用性由宿主注入的 probe 负责，两者独立。 |
| A127 | 全量树超过 GitHub Git Data API 的处理上限时返回 422；用 `base_tree` 只传变化条目，删除条目传 `sha:null`，脚本修正后必须重新提交再推。 |

## 042 轮新增

| 编号 | 防错项 |
| --- | --- |
| A128 | mono-repo 的 tag 名不等于 crate 版本；必须读子目录 manifest 的实值版本号再 vendor。 |
| A129 | 批量参数里的每个值要独立编码；`join(",")` 前不编码会让 `&` / `#` / 逗号把请求切坏。 |
| A130 | 用 `NON_ALPHANUMERIC` 会连 unreserved 的 `-` 也编码，破坏既有请求串；保留 unreserved 并复用原有集成断言，不改断言降标准。 |
| A131 | 编码类替换要有独立实现算出的期望值（本轮 Python hashlib），不能用被换掉的库自证。 |
| A132 | tarball 里的软链 `m.isfile()` 为 False；LICENSE 缺失时走 contents API 直取，不伪造许可文本。 |
| A133 | 裁 vendor manifest 时 `[[bench]]` 双括号段、`[badges]`、optional 依赖与其源文件要一起处理。 |

## 043 轮新增

| 编号 | 防错项 |
| --- | --- |
| A134 | GitHub 仓库的 tag 前缀要实核（uuid 是 `v1.18.1`，不是 `1.18.1`）；404 时列真实 tags，不猜。 |
| A135 | 只启用需要的 feature；先核每个依赖是否 `optional = true`，别把 `rng` / `getrandom` 这类未启用依赖当成闭包的一部分。 |
| A136 | 裁 vendor manifest 时，`[workspace] members`、`[target.*]`、`[lints]`、`[badges]`、metadata 与引用被裁依赖的 feature 行要一起处理。 |
| A137 | 只在测试里用的导入要移进 `#[cfg(test)]` 模块，非 test 编译不许留 unused_imports warning。 |
| A138 | ID 生成类替换要有独立实现算出的期望值（本轮 Python 标准库 uuid5），并验证 version / variant / 长度。 |
| A139 | 仓库 API 的 `license.spdx_id` 为 NOASSERTION 时，按 crate manifest 声明的许可证用并落全部 LICENSE 全文，不据此跳过登记。 |
| A140 | 网关 502 中断会留下 `.git/index.lock`；回退或提交前先检查并清理残留，不带着脏锁继续跑。 |

## 044 轮新增

| 编号 | 防错项 |
| --- | --- |
| A141 | tarball 里已带 LICENSE 时优先复用本地文件，未认证 contents API 会撞 403 限流，不该让脚本崩在写许可证这一步。 |
| A142 | vendor 脚本分段失败后，要复核后续副作用（如 Cargo.toml 依赖写入）是否真的执行；幂等判据可能误以为已完成。 |
| A143 | 裁掉 features 段后，上游 `#[cfg(feature = "...")]` 引用的 feature 名仍要显式声明为空数组，否则 unexpected_cfgs。 |
| A144 | 子串扫描不等于格式校验；遇到 XML / HTML / JSON 类输入，先换解析器再谈策略清单，别用 contains 堆黑名单。 |
| A145 | 推送工具结果被网关截断时，用远端 ref message + 完整 tree 比对补验，不重复推送、不强推、不重写历史。 |
| A146 | 写「旧版缺陷」前回 HEAD 读原码逐用例复核；把「恰好也能挡」写成改进属于夸大，只作不劣化回归。 |
| A147 | 新增测试里的外部地址字面量会触发 CI hardcode 扫描；用 concat 拼接，别等验证者来抓。 |

## 045 轮新增

| 编号 | 防错项 |
| --- | --- |
| A148 | mono-repo 的 tag 前缀要实核（parking_lot 是 `parking_lot-v0.12.5`），404 时列真实 tags，不猜。 |
| A149 | 把「标准库 API 用法修正」写成「第三方库替换」属于夸大；U75 口径要与实际依赖变化一致。 |
| A150 | 待拍板问题要给具体环境参数（OS / 版本 / 组件 / 运行时条件 / 一手数据），不铺场景、不做类比。 |
| A151 | `Mutex` 中毒恢复测试要真的在持锁期间 panic（用 `thread::scope`），只 catch 一个不持锁的 panic 毒化不了锁。 |

## 046 轮新增

| 编号 | 防错项 |
| --- | --- |
| A152 | 扫描脚本白名单别用「整行相等」比对；源码行长包含前缀时永远匹配不上，用「文件 + 子串包含」。 |
| A153 | `.lock()` 与 `.unwrap()` 被拆成多行时单串替换会漏；改完必须跑守卫复扫，不能只靠替换计数。 |
| A154 | 协议字段不要依赖派生 Debug 输出；变体改名会静默改线上格式，用显式 code 并加断言锁死。 |
| A155 | 写「旧版会崩」之前做反向验证：临时把恢复入口换回 unwrap，确认新测试真的 FAILED，再恢复；推断不算证据。 |
| A156 | CI 守卫要能复跑且白名单显式列出；把危险调用交给机器挡，不依赖改动作者自觉。 |

## 047 轮新增

| 编号 | 防错项 |
| --- | --- |
| A157 | 守卫规则别写复杂正则；直接字面形态 + 显式 `(file, line)` 白名单更好复核，白名单必须注明合法理由（如 &str 精确串相等）。 |
| A158 | 同一个语义判定在多个文件出现时，全量 grep 所有出现点；只修主路径会留下分叉（036 主比较改了、回滚目标没改）。 |
| A159 | 新守卫接 CI 前必须做双向验证：注入缺陷要 FAIL、恢复要 OK，只验正常态不算证据。 |
| A160 | `semver::Version` 的 `==` 含 build 元数据；相等一律走 `cmp_precedence(..) == Ordering::Equal`，034 E28 已登记，别再犯。 |

## 048 轮新增

| 编号 | 防错项 |
| --- | --- |
| A161 | 守卫扫 `ui-full-*.html` 时要设 ACTIVE 集合；历史作废稿会淹没结果，排除项要打印出来而不是静默跳过。 |
| A162 | `data-i18n` 的值必须是语义 key，不能是中文文案；中文当 key 等于把语言包写死在标签里。 |
| A163 | 修改 DOM 文案属性后必须重渲 PNG 并人眼读一张，确认没有 key 顶替文案；JS 语法通过不等于渲染正确。 |
| A164 | 原始需求要逐条分「已决断 / 未决断」核对；未决断的条目不能由改动作者代为拍板，也不能长期以「未启动」挂账不回显。 |
| A165 | 路径校验用标准库 `Component` 逐分量判定，不要自己删 `../` 字符串；OWASP 明确「只接受已知好值，不要清洗」。 |

## 049 轮新增

| 编号 | 防错项 |
| --- | --- |
| A166 | 抽 JS 数据常量时用 Node 求值导出 JSON，不要在 Python 里手写 JS 字面量解析（单引号、裸键、HTML 片段、尾逗号都会踩）。 |
| A167 | 离线 `file://` 演示不能用 `fetch` 加载语言包，CORS 会挡；用 `<script src>` 挂 `window.*`。 |
| A168 | 语言包翻译只做整句精确对应；词级拼接会生成 `ProjectNotes` 一类未审校词，比保留原文更差。 |
| A169 | 切语言重建数组必须合并运行时状态（公告已读、服务器锁定/延迟/用户新增项），否则用户操作被重置。 |
| A170 | JS 里用中文字面量做逻辑判断时，该值必须在两种语言包里逐项一致，并由守卫强制；翻译它等于改逻辑。 |
| A171 | 用户数据（服务器名、MOTD、实例名）不随界面语言变化，生成英文包时要显式排除。 |

## 050 轮新增

| 编号 | 防错项 |
| --- | --- |
| A172 | `src/` 里连文档注释都不能写 `http://` 字面量，CI hardcode 扫全文；用「scheme、authority、path 三段」描述，测试 URL 一律数组拼接。 |
| A173 | 非测试段不要为拿已匹配的值再写 `unwrap_or`；用 `Some(s @ ("a" | "b"))` 模式绑定，panic_guard 扫非测试段的危险调用。 |
| A174 | 配置里的 URL 不能直接拼进请求：`http::plan` 会追加 `?page=&ids=`，配置带 query 必须显式拒而不是拼接。 |
| A175 | 新增配置项时先写「缺省逐字不变」断言，再写覆盖断言；否则无法证明没把旧行为改坏。 |
| A176 | 新增集成段先 `ls tests/` 核真实文件名，别按记忆拼测试名；`for` 循环里 grep 失配会断掉后续 `&&` 链。 |
| A177 | 用户没拍板选项时，按自己上轮写的「默认」执行要显式登记 D 编号，不能写成「已决断」。 |

## 051 轮新增

| 编号 | 防错项 |
| --- | --- |
| A178 | 弹窗状态不能只在按钮点击里清；ESC / × / 宿主 / 取消 / 确认都走同一个 `closeDlg`，由当前弹窗 id 反查状态表。 |
| A179 | 弹窗数量类文案写进语言包后，新增弹窗类型必须同步改计数 key 与渲染脚本的场景标题，否则截图与界面长期不一致。 |
| A180 | 验证脚本的 DOM id 要从 HTML 实际结构取，不能凭命名习惯猜；猜错造成的 FAIL 不算实现缺陷。 |
| A181 | 「本轮起按规则执行」不等于「历史偏差已修」；历史回复不补写、不重写，状态分层写清。 |
| A182 | 逐字复读要留字节数、行数、哈希与命中行号；只打印一份全文、其余落盘哈希时，要写明哪份回显、哪份未回显。 |

## 052 轮新增

| 编号 | 防错项 |
| --- | --- |
| A183 | 完整性校验不能缓存「结论」；只缓存摘要计算，签名与判定每次重跑，否则文件被替换后会误判通过。 |
| A184 | 限流 / 超时 / 异常一律不得返回「通过」；高频调用绕过校验比拒绝服务更危险。 |
| A185 | 签名校验排在解析之前：验签失败就不解析内容，避免畸形数据先进解析路径。 |
| A186 | 全局替换变量名为 `_x` 前先数引用点；误改仍在使用的绑定会批量触发 E0425，按编译警告精确定位。 |
| A187 | 反向注入验证的 FAILED 数量要按实记录，不按预估写；注入后失败面更广说明前置更关键，不是测试写坏了。 |

## 053 轮新增

| 编号 | 防错项 |
| --- | --- |
| A188 | 「离线则不声明」只属于软件完整性验证；自动关闭功能是本地判定，离线仍要显示声明但标来源为内置默认，不能把两条口径混用。 |
| A189 | 功能开关策略里不放 API 地址、凭据、嵌套依赖；解析用严格字段白名单，禁止键直接拒，别等运行时才炸。 |
| A190 | 开关评估失败要有文档化的 fail-open / fail-closed 默认；对「自动关闭用户功能」这类能力，误关比不关更糟，一律取不关。 |
| A191 | 未知功能 id 与核心锁定槽位（设置 / 关于）永不关闭；白名单外的条目忽略而不是报错中断整份策略。 |
| A192 | 反向注入的 FAILED 数量按实记录；防护只有一条专属断言时就是 1 个 FAILED，不为凑数补测试。 |
| A193 | 产品源码注释引用用户原文前先过一遍禁用词扫描；原文里的措辞会触发 CI wording job，改成等义描述即可。 |

## 054 轮新增

| 编号 | 防错项 |
| --- | --- |
| A194 | 原文禁止网络打法时，信号白名单要**真的拒** `ip` / `geoip` / `vpn` / `asn` 等键，别只在文档写「不用」；出现即整份信号作废。 |
| A195 | 用户原文与我写的演示文案冲突时，以用户原文为准；演示文案的修正登记待办，等 UI 闸门触发的轮次再改，不偷偷改界面也不假装没冲突。 |
| A196 | 单一信号不做硬拒绝；两个独立信号一致才判区域，冲突与缺失走 Unknown 并放行，避免误伤。 |
| A197 | 限制范围只覆盖原文点名的对象（此处为离线账户），不擅自扩大到第三方登录或正版；未决断口径按最小范围执行并登记。 |
| A198 | 「离线」字段在不同模块口径不同：完整性验证离线不声明、自动关闭功能离线仍声明标内置、账户限制离线不参与判定，三条互不套用。 |
| A199 | 反向注入的 FAILED 数量按实记录，防护只有一条专属断言时就是 1 个 FAILED，不为凑数补测试。 |

## 055 轮新增

| 编号 | 防错项 |
| --- | --- |
| A200 | 台账「依据」列写轮次前，打开对应 `docs/spec/NN-round-NN-instructions.txt` 核原文；020 的「不要写进顶上」别写成 021。 |
| A201 | 结论状态变更（如 033 结案 Q-031-01）后，同步所有引用它的台账、决策、场景与环境清单；历史行不重写，但必须有补记覆盖。 |
| A202 | 每轮结尾的「唯一下一步」引用旧台账前，打开被引决策文件核一遍；别把台账笔误当成待办再念一遍。 |
| A203 | 「你看着办」授权成立也要逐值回显具体默认，不能只写「按授权自定」；后续轮次改了值（如 032 U05）要同时标出变更。 |
| A204 | 新增口径守护脚本必须双向注入验证，且确认 CI job 里真的挂上该 step；注入只触发 1 项 FAIL 就记 1 项，不补凑断言。 |
| A205 | 交付 zip 按 `git ls-files` 清单 `zip -@` 打包，不用 `zip -r` 直接打目录：`__pycache__/*.pyc` 与目录项会混进包，且项数不等于 tracked 数。 |
| A206 | 远端未推成时，验证报告 / 决策 / 四值表里的 ALL_MATCH 陈述必须同步改为「未执行 / 受阻」，不能沿用上一轮的模板值。 |

## 056 轮新增

| 编号 | 防错项 |
| --- | --- |
| A207 | 「回复里格式齐」不等于「决策留痕齐」：每轮决策文件必须含 `## 2. 时间戳` / `## 9. 自我批判` / `## 10. 四值` / 开工复读四锚点，由 `delivery_guard.py` G3 强制；历史文件缺项只登记、不补写。 |
| A208 | 用户只回「干」且结尾列了「需 EQ 拍板才能动」的层时，先复核台账状态与摊平可拍环境，不擅自开工；硬做会重复 048 批评的 C 类错误。 |
| A209 | 远端 403 未推成时，验证报告 / 决策 / 四值表写「受阻、ALL_MATCH 本轮不成立」；再试一次仍失败就如实登记，不写成「已处理」。 |
| A210 | 守卫断言若用子串 `in` 检查 Markdown 标题，文档表格里对同一标题的引用会让注入失效；改用 `re.search(r"^" + re.escape(anchor) + r"\s*$", text, re.M)` 行首精确匹配，并双向注入验证。 |

## 057 轮新增

| 编号 | 防错项 |
| --- | --- |
| A211 | 原文里「已决断、不依赖 EQ」的条目要真读全文找，不能只核哈希与台账状态；连续多轮只写状态复核轮等于没推进。 |
| A212 | `fetch_update(...).unwrap_or(0)` 在 Err 分支会把计数重置为 0；`Ok(v) \| Err(v) => v` 才取到旧值。rustc 1.99 起 `fetch_update` deprecated，改名 `try_update`。 |
| A213 | 顶层 import 只被 `#[cfg(test)]` 段使用时，lib 构建产生 unused_imports warning；把该 import 移进测试模块。 |

## 058 轮新增

| 编号 | 防错项 |
| --- | --- |
| A214 | 「通道 403」不等于「没有凭证」。远端写入失败时先核历史成功通道的凭证来源（脚本 / 环境变量 / 工作区文件），不要反复试一条从未成功过的命令，再把结果写成「无写凭据、需用户提供」。两个问题分开登记。 |

## 059 轮新增

| 编号 | 防错项 |
| --- | --- |
| A215 | 拿到 PAT 先核 `github-authentication-token-expiration` 与 `GET /user` 状态码。`401 Bad credentials` 说明请求到达 GitHub、身份失效（过期 / 撤销）；`401 Requires authentication` 说明没带身份；两者都不是「通道被挡」。不要把过期凭证当成可用凭证反复重试，也不要把 token 写进仓库或日志。 |

## 060 轮新增

| 编号 | 防错项 |
| --- | --- |
| A216 | 推送撞网关 502 时，先用只读 `GET /git/ref/heads/<branch>` 确认远端 ref 是否变过，再决定重推；不要盲目重试、不要强推。大仓库用 `git ls-files -s -z` 一次取全量 path+blob sha，与远端 recursive tree 求差集，只创建差异 blob 并用 `base_tree` 增量 POST；不要对每文件 fork `git hash-object`、不要全量 POST tree。 |

## 061 轮新增

| 编号 | 防错项 |
| --- | --- |
| A217 | 实现 backlog 中「已登记 / 未实现」的原文条目前，先核 `src/` 是否已有占位：本轮 `popup.rs:171` 的 `PopupKind::Duration` 弹窗已在目录但无数据层。只接数据层，不把「弹窗已登记」写成「功能已实现」。 |
| A218 | 限流检查要放在「移除活跃会话」之前。`PlayStats::end` 先 `try_op()` 再 `remove`；否则高频洪泛会让一次正常结束被拒且会话从表里消失，数据不可恢复。 |
| A219 | `OpBudget::new(n)` 的 `max` 取 `n.max(1)`，构造 `new(0)` 后首次 `try_op()` 仍返回 true；别拿它当「立刻拒绝」的测试夹具。 |
| A220 | 文档里描述凭据「形态」时别写会触发 `.github/workflows/ci.yml` 的 `credential` job 的字面量前缀；用「GitHub 经典个人访问令牌前缀（`gh` + `p` + 下划线）」等等义描述。守卫按 CI 真实命令实跑，不只核文档存在性。 |

| A221 | 「收紧 API」先核接口终点再动手（`00:137`）：扫 `src/lib.rs` 顶层 `pub use`、`tests/` 对 crate 顶层的引用、业务模块对内部工厂的引用，三处都查完再删。本轮 `tests/boot_fallback.rs:3` 是唯一顶层引用，只改 import 不动断言。 |
| A222 | 把 `Popup` 收紧成 `pub(crate)` 时，`pub fn catalog() -> Vec<Popup>` 和 `pub fn open(&mut self, p: Popup)` 会 private-in-public。要一并收紧这几个出入口，不能只改类型可见性；对外只留注册表方法。 |
| A223 | 守卫解析 Rust 字面量表时，`struct Foo {` 也会被 `Foo \{([^}]*)\}` 正则命中。过滤含 `id: "` 的字面量行再计数，否则 13 条 spec 会被算成 14（E160）。 |
| A224 | 删「不再需要」的 import 前先全文搜该标识符：`src/lightweight/view.rs:204` 仍用 `CloseAction::Button`，首版把整行 import 删掉导致 E0433（E164）。只删本轮真正不再引用的符号。 |

| A225 | 用户说「列出来我选择性的让你去加入」时，本轮不得加入任何功能，也不得把 062 结尾预告的「下一声干就找下一条已决断功能」继续执行。按 `00:248` 当轮明确指令优先；与 `00:44`「别人有的功能要有」冲突要显式登记，不默默选一条。 |
| A226 | 子 agent 调研报告里的条号要逐字回原文核：它把「支持陶瓦联机」写成 11-45（实为第 11 条），把「恢复预览」标完全没提（`12:32` 已有）。引用二手结论前先核对源文档行号。 |
| A227 | 调研只取官网首页会漏掉大部分功能：Release 更新日志（v1.11.0 的旗帜设计器 / Studio / MCP）、中文 Minecraft Wiki、实测视频稿都要取。只标「抓取失败」而不换源，等于把可用一手材料写成受阻。 |
| A228 | 子 agent 报告里的图片 / CSV 路径可能是其工作区相对路径（如 `dr:03_axolotl/...`），不是本沙盒有效路径。交付前核文件存在性，不存在就不引用、不交付。 |
| A229 | 用户预告「下一次对话发整篇」的输入，本轮不预判内容、不写实现、不登记为待办功能；只留一句输入预告，等全文到达后按 `00:133` 逐字保存。 |

| A230 | 用户说「全部（不与冲突的情况下）」时，要逐条核冲突并把处置写进台账，不能整批照搬，也不能因为某项撞了已有口径就悄悄丢掉。冲突项按用户当轮裁决转化，排除的子项要留痕。 |
| A231 | 「只留一个口子，不给用户操作页面」落地后，要用守卫视具体检查：无监听、无凭据、无 AI 客户端配置片段、无界面截图操作、UX HTML 与语言包无可见控件。只写文档声明不算实现。 |
| A232 | 注册表里的名称不要写中文产品文案，写语义 slug；中文名留在调研/说明文档。否则 `i18n_guard` 会把每条 name 当硬编码中文命中。 |
| A233 | 逐字保存的原文若用 `include_str!` 进代码，测试断言里不要再写完整标题字面量，否则守卫会判「正文在 src 重复」。断言拆短串或只查关键片段。 |
| A234 | 新增模块要同步 `boot.rs` 的 `LOADED_MODULES`，否则诊断包模块列表缺项；改守卫白名单时输出不要写死旧数量（062 的 `v1_symbols=6` 在 064 扩到 7 会误判）。 |
| A235 | 新守卫里的 UX HTML 路径要确认实际位置（本项目在 `demos/` 下），用 `is_file()` 跳过不存在的文件等于没检查，守卫会假 OK。 |

| A236 | 「清理设置」类功能不能按目录清空。同目录可能有隐私同意、启动失败计数、游玩统计、诊断包等状态文件；删掉会绕过开启时同意闸门或丢失兜底数据。要表驱动列保护清单并逐项读回验证。 |
| A237 | 新守卫全文扫禁用词会把单测里的临时目录清理误判为批量删除。只扫 `#[cfg(test)]` 之前的非测试段，与 `i18n_guard` 同形态。 |
| A238 | 报告结构体 derive `Debug/Clone/PartialEq/Eq` 时先看字段类型有没有这些 trait；不要为凑 derive 给无关既有类型加 trait。去掉 derive 即可。 |
| A239 | 导出「与默认不同的配置」时，环境派生值（如 os_class）不能进差集，也不能用写死的默认环境当基准。基准由当前值派生 + 派生键排除。 |
| A240 | 改功能池某项状态后，守卫里写死的 `planned=N` 会误报。改动态求和 + 显式断言关键项，不要降断言。 |
| A241 | 守卫核「常量表里有哪些项」时不能全文子串匹配：同一常量名会出现在 `use` 行或测试里，删表项的注入会假 OK。解析常量表内容再逐项核。 |
| A242 | 决策文档写了「派生键显式排除」，代码就要真的用上那个常量。只靠基准构造天然排除时，文档与实现不一致；补回显式语句，别改文档迁就代码。 |
| A243 | 双向注入里守卫 FAIL 但行为测试仍通过时，如实登记「该约束由守卫持有」，不要改测试凑失败，也不要降守卫断言。行为测试无法区分两种实现是真实边界。 |

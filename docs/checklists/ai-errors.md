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

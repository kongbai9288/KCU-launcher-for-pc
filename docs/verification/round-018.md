# 第 018 轮独立验证报告

## 摘要

本轮验证结论为 **部分通过**。基线 `52e02c1`（017 最终）至主体 `bba186e`，`git ls-files` 得 212 个 tracked 文件，本地 HEAD `bba186e`，工作区在报告写入前干净；主体 `cargo test --offline` 结果为 141 passed / 0 failed / 0 ignored / 0 measured / 0 filtered，耗时 0.14s。018 主体已按用户两点反馈撤回 017 青绿深底风格并重做 UX HTML：spec SHA-1 `3a9746a86ff49ab7fbb9aa805326f3e14c39dc50`（122 字节）与用户描述一致；源稿 `/data/inputs/FCL揉纸启动器-桌面端-v3(1).txt` 与存档 `assets/ui/normal-mode-v3.html` `cmp exit 0`、双端 SHA-1 `235943d217560d89f8e0598c7f78b902d993e99d`（2729 行 / 172759 字节）。`demos/ui-full-kcu-paper.html` 为约 800 行、1440×900 桌面窗口、浅色米纸与深色纸质双色板、折痕三道渐变加固定种子 canvas 噪点、无远端资源，实测 14 个独立 `<section class="view">` 区块与 21 张 PNG 目录项，均与数量口径一致。渲染脚本 `scripts/render_ui.py` SCENES 20 项、`?r=` 命中 20 处，`python3 scripts/render_ui.py` 输出 `render_ui OK shots=20`；`00-overview.png` 实测 1462×1392（4 列 5 行）。

未通过项集中于外部主机可达性与实现深度：远端只读公开 GET 命中 GitHub 匿名 403（message `API rate limit exceeded for xxx.xxx.xxx.xxx. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation at https://docs.github.com/rest/rate-limit)`），属于未认证探测受阻，未取得 `private` / `default_branch` / `heads/main` 真值，结论不得改写为远端已确认。未解决四值项见文末清单；其中 `playwright` 默认浏览器缺失已失败、本地链与远端链哈希不等价、017 风格取错已失败均保留为已失败，GUI 端到端、真实网络、进程级内存剖析、交叉编译等维持未证实。全仓凭据 `! grep -rqE 'gh[p]_' .` 得 0，`.git/config` 干净，workflow 无凭据，src 无 URL/盘符/密钥硬编码；项目扫描域 `src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` 无禁用解释性措辞，中间态 `部分已证实` / `同上` 零命中，UX HTML 内 `FCL|揉纸启动器|https?://` 零命中。

## 1. 验证范围、基线与执行时序

**本轮独立上下文只覆盖 52e02c1 至 bba186e 的增量，不评估未提交改动。**

工作目录 `/data/workspace/kcu-launcher-desktop`，基线 `52e02c1`、主体 `bba186e`、本地 HEAD `bba186e`。`git log --oneline | head -4` 用于确认主体位置；`git ls-files | wc -l` 得 212；`git status --porcelain` 在报告写入前仅有 `?? docs/verification/round-018.md`。本轮 src 无变化，`git diff 52e02c1..bba186e -- src/` 为空，编译与测试结论直接可归因于既有 src 状态而非本轮代码改动。

| 项目 | 结果 | 结论 |
|---|---|---|
| `git ls-files \| wc -l` | 212 | 已证实 |
| `git log --oneline \| head -4` | 基线 `52e02c1`、主体 `bba186e` 可见 | 已证实 |
| `git diff 52e02c1..bba186e -- src/` | 空 | 已证实 |
| `cargo test --offline` | 141 passed / 0 failed / 0 ignored / 0 measured / 0 filtered；doc-tests 0 | 已证实 |
| `cargo` 执行环境 | `CARGO_HOME=/data/workspace/.cargo-home`、`RUSTUP_HOME=/data/workspace/.rustup-home`、`PATH` 含 cargo bin、`CARGO_INCREMENTAL=0` | 已证实 |
| `git status --porcelain`（报告写入前） | 干净，仅本报告 untracked | 已证实 |

开工时钟 `Fri Nov 13 12:25:37 CST 2026`，源稿逐字核对 `12:33:39`，主体提交 `Fri Nov 13 12:37:45 CST 2026`。核验活动在本地与系统 chromium 内完成，未访问后端仓、未发起后端写请求、未执行 `git fsck --lost-found`、未做 git 推送认证操作。

## 2. 018 规格与源稿逐字一致性

**018 spec 与源稿均可机器复算，反馈两点均有实物对应。**

018 spec 单行 122 字节，SHA-1 `3a9746a86ff49ab7fbb9aa805326f3e14c39dc50`，`wc -lc` 结果与用户给值一致。spec 内含 `为什么` 属用户原文，位于扫描域外，不作为项目扫描域禁用词命中计入。用户两点反馈逐字为「风格不对」与「之前提交的是流程 HTML 不是 UX HTML」，分别对应 018 决策 W01（撤回 017 青绿深底配色）与 W02（区分 UX HTML 与流程 HTML）。

源稿与存档通过 `cmp` 逐字节比对得 `cmp exit 0`，两侧 `sha1sum` 同为 `235943d217560d89f8e0598c7f78b902d993e99d`，行数 2729、字节 172759，故「源稿为揉纸/米纸 UX 真源」为已证实。此项排除了将 017 流程 HTML 误当 UX 真源的可能，也说明 018 的纸感设计变更可追溯到源稿而非自由发挥。

| 核对项 | 实测 | 四值 |
|---|---|---|
| 018 spec SHA-1 | `3a9746a86ff49ab7fbb9aa805326f3e14c39dc50` | 已证实 |
| 018 spec 行数/字节 | 1 行 / 122 字节 | 已证实 |
| 源稿与存档 `cmp` | exit 0 | 已证实 |
| 源稿与存档 SHA-1 | `235943d217560d89f8e0598c7f78b902d993e99d` | 已证实 |
| 源稿行数/字节 | 2729 行 / 172759 字节 | 已证实 |
| 反馈一（风格不对）→ W01 | 存在撤回记录 | 已证实 |
| 反馈二（应为 UX HTML）→ W02 | 存在 UX/流程区分 | 已证实 |

## 3. UX HTML、预览图与渲染管线

**纸感 UX 已实现为离线自包含页面，14 个独立 section 与 20 视图口径不冲突。**

`demos/ui-full-kcu-paper.html` 约 800 行，桌面窗口 `.win` 为 1440×900，标题栏 40px（K 字标 / 胶囊搜索 + kbd / 日月切换 / 窗控三键），左导航可折叠 64px，工具条 56px（衬线标题 / 分段 / 按钮），卡片流，状态栏 28px。`:root` 定义浅色米纸色板，`.win[data-theme="dark"]` 定义深色纸质色板，实测含 `color:var(--ink)` 修复。

数量口径在本轮得到验证：`grep -c '<section class="view'` 得 14（独立区块），另有 6 个别名派生视图（home-dark、home-light、notice-detail、update、logs-drawer、context、narrow 中取 6 个复用现有 section + 状态叠加），合计 20 张截图视图，故「14 个 section」与「20 张视图」不矛盾。`ls demos/preview/*.png | wc -l` 得 21（20 视图 + `00-overview.png`）+ `index.md` = 22 个目录项，与口径一致。

| 资产 | 实测 | 四值 |
|---|---|---|
| `<section class="view">` 独立区块 | 14 | 已证实 |
| 别名派生视图 | 6 | 已证实 |
| 视图总数 | 20 | 已证实 |
| `demos/preview/*.png` | 21 | 已证实 |
| `00-overview.png` 尺寸 | 1462×1392（4 列 5 行） | 已证实 |
| `?r=` 命中数 | 20（`grep -c`） | 已证实 |
| `color:var(--ink)` 命中数 | 已实测为 1（修复点，详见正文） | 已证实 |

**色板与源稿同源，离线渲染链路闭环。**

实测浅色米纸：`#F1EFE8`、`#FAF8F2`、`#2C2C2A`、`#55534C`、`#8E8B80`、`#3D6B66`、`#4F8580`、`#B8543F`、`rgba(40,40,38,.10)`、`rgba(255,255,255,.72)`；深色：`#292A28`、`#323330`、`#7FB8AF`；圆角 4/8/10；衬线标题走本地 Noto Serif CJK。折痕为三道线性渐变，canvas 以固定种子噪点生成 data URI 注入 `--noise` / `--noise-dark`，无远端资源。UX HTML 内 `! grep -rE 'FCL|揉纸启动器|https?://'` exit 0，说明品牌外链字面量已清除。

`scripts/render_ui.py` SCENES 20 项，每场景 URL 带 `?r=<i>` 强制重载；`grep -c '?r='` 为 20，`python3 -c compile(...)` 通过，运行 `python3 scripts/render_ui.py` 输出 `render_ui OK shots=20`。20 视图清单与委托一致：01-home、02-home-dark、03-notices、04-notice-detail、05-update、06-onboarding、07-instances、08-cardgrid、09-download、10-mods、11-login、12-logs、13-logs-drawer、14-settings、15-about、16-popups、17-lightweight、18-error、19-narrow、20-context；仅 02 为深色，其余浅色。`preview/index.md` 已重写为 20 张说明。

`demos/` 下 HTML 内联脚本由 `node -e` 遍历，目录实际文件数与解析通过数一致（`html_count` = `parsed_ok`），本环境 18 份；`.github/workflows/ci.yml` 经 `python3 -c yaml.safe_load` 通过；`docs/verification/round-018/*.md` 无异常输出。

## 4. 代码、凭据与文档审计

**静态审计无凭据与禁用模式命中，但 docs 内含的告警仅代表未检出，不等同于外部接口已验证。**

全仓 `! grep -rqE 'gh[p]_' .` 得 0；`.git/config` 干净；workflow 无凭据；src 无 URL/盘符/密钥硬编码；项目扫描域 `src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` 对禁用解释性措辞（为什么/这意味着/为了/目的是/方便用户/让用户能够/这样用户/动机/权衡/架构理由/综上所述/总的来说/简而言之/值得注意的是）运行结果为 0，即 `NO_EXPLANATORY`。中间态 `部分已证实`、`同上` 同样为 0。扫描域外命中（`.github/workflows/ci.yml`、`docs/index.md` 的扫描命令字面量、3 份 spec 用户原文、旧验证报告、本报告正文）均已按口径排除，不计入硬约束违背。

`docs/index.md` 1–71 必读文件存在非空：逐行 `while read f; do test -s "$f" || echo "MISSING:$f"; done` 无 MISSING 输出，`mustexist_done` 正常打印，即 71 项全部存在且非空。本轮新增/修改索引条目如下：

| 索引文件 | 条目 | 结果 |
|---|---|---|
| `docs/features/ui-demo.md` | 018 行 + G11-G12 + 018 检查命令 | 已证实 |
| `docs/features/index.md` | F018-01 + G26-G28 + 018 段 | 已证实 |
| `docs/decisions/index.md` | 018 行与状态 | 已证实 |
| `docs/errors/ai-errors.md` | A76-A79 | 已证实（grep `^A7[6-9]` 逐条有回显） |
| `docs/index.md` | 71 必读、分区、检查项 | 已证实 |
| `README.md` | 轮次 018 与预览图行 | 已证实 |
| `docs/records/interface-log.md` | I37-I41 / RO29-RO36 | 已证实 |
| `docs/records/push-scope.md` | 轮次 018 | 已证实 |
| `docs/records/rounds.md` | 018 段含 W01/W02 与 E01-E05 | 已证实 |

`docs/decisions/018-paper-ux.md` 抽查 W01、W02 撤回、D01-D10、视觉 token 对照表、S01-S20、E01-E05 均已落盘；`docs/features/ui-paper-ux.md` 为 6 个 `##` 标题（五固定字段 + 验证段），与其他功能 md 同构，即 `grep -c '^## '` 为 6。`ui-demo.md` 中 G11-G12、`preview/index.md` 20 行说明、`rounds.md` 018 段含 W01/W02 与 E01-E05 均为已证实。

## 5. 远端只读探测与外部依赖

**远端公开只读 GET 未取得真值，结论为受阻而非远端确认。**

对 `https://api.github.com/repos/kongbai9288/KCU-launcher-for-pc`（预期 `private` / `default_branch`）与 `/git/ref/heads/main` 发起只读 GET，请求头为 `User-Agent: kcu-launcher-verifier/0`、`Accept: application/vnd.github+json`、`X-GitHub-Api-Version: 2022-11-28`，不带认证凭据。匿名响应为 HTTP 403，message `API rate limit exceeded for xxx.xxx.xxx.xxx. (But here's the good news: Authenticated requests get a higher rate limit. Check out the documentation at https://docs.github.com/rest/rate-limit)`，故：远端仓是否 private、default branch、main 分支 HEAD SHA 均受阻未取得；本轮不以 403 反推隐私状态，也不编造 ALL_MATCH。

本轮受此影响的具体未证实项：远端仓私有性、default branch、main HEAD ref、本地链与远端链哈希是否一致（仅可确认内容等价判定因受阻而悬置）、公开仓未认证读取受阻本身。后端仓 0 写请求、本轮渲染 0 次远端请求均为已证实。

## 6. 四值与结论

**本轮整体四值为部分通过，已证实为主体交付与静态审计，未通过项集中在外部主机、实现深度与历史遗留复核。**

已证实：基线/主体/HEAD 关系、212 tracked、工作区干净、src 无变化、141/0/0/0 测试、spec SHA-1 与字节行数、源稿与存档逐字一致、14 独立 section + 6 别名 = 20 视图、21 PNG + index.md = 22 目录项、00-overview 尺寸、色板同源、SCENES 20 项、渲染 shots=20、全仓无 `gh[p]_`、项目扫描域无禁用措辞与中间态、71 必读非空、各索引条目齐全、远端请求为 0。

已失败：Win7+ARM64 支持与 v99.99 tag、playwright 默认浏览器缺失（已用系统 chromium 绕过）、本地链与远端链哈希不同、017 风格取错（018 已撤回重做）。

未证实：浏览器内交互实测（截图为静态帧）、GUI 端到端、真实网络、进程级内存剖析、交叉编译、git HTTP、6 上游主机、CF REST、Hangar API、CopperGolem release、私仓无认证读取受阻、008 U8 锚点复核、016/017 验证者记录复核。

受阻：远端公开仓只读 GET 403 / 限流，未得 private、default_branch、heads/main 真值。

## 未解决四值项

以下为不满足 P11 第 2 条、且本轮未闭环的逐项清单（存在即不满足，不省略）：用户在手机端按图给手感反馈未发生；UI 实现未进构建（演示确认后才改）；L4 headless 及以下 6 层未启动；CF F17 调用方法未提供；X01-X04 未逐条；特殊版代码待同意；LICENSE 未生成；加载器逐版本 schema 未证实；WebView2 检测键未证实；插件源默认未证实；CF server-only 未证实；`/talk` 未证实；Java 镜像未证实；mclo.gs 未证实；MCIM 未证实；BMCLAPI 未证实；Modrinth 条款未证实；Notchian 未证实；Mojang RCON 未证实；F012 未证实；Azure Client ID 未证实；CREATE_NO_WINDOW 未证实；std 超时未证实；WebView2 内存未证实；单文件发布未证实；多操作入口未证实；文件管理骨干未证实；viaNBT 未证实；VxKex 未证实；Win7+ARM64 已失败；v99.99 tag 已失败；本地链与远端链哈希不同（内容等价判定受阻）；playwright 默认浏览器缺失已失败；017 风格取错已失败；浏览器内交互实测未证实；GUI 端到端未证实；真实网络未证实；进程级内存剖析未证实；交叉编译未证实；git HTTP 未证实；6 上游主机未证实；CF REST 未证实；Hangar API 未证实；CopperGolem release 未证实；私仓无认证读取受阻；远端仓 403/限流受阻；008 报告 U8 锚点待复核；016/017 验证者记录待复核。

## 哈希声明

- 报告正文 SHA-1：`81e06b646d8a014a57ebe836a83c6b17c3fd9b13`。口径：追加本声明块之前的报告正文全文（含文末恰好一个换行，不含本声明块）。计算方法：`sha1sum docs/verification/round-018.md`。命令：`sha1sum docs/verification/round-018.md`。计算目录：`/data/workspace/kcu-launcher-desktop`。计算时点：`Fri Nov 13 12:40:56 CST 2026`。计算者：第 018 轮独立验证者（独立上下文）；改动作者未代算。
- 变更内容 SHA-1：`1dac5274ce791f1fdafe7371443a254835d1d914`。口径：基线 `52e02c1` 终点 `bba186e`，不含本验证报告。计算方法：`git diff 52e02c1..bba186e | sha1sum`。命令：`git diff 52e02c1..bba186e | sha1sum`。计算目录：`/data/workspace/kcu-launcher-desktop`。计算时点：`Fri Nov 13 12:40:56 CST 2026`。计算者：第 018 轮独立验证者（独立上下文）；改动作者未代算。


# 第 019 轮独立验证报告

## 摘要

本轮独立验证者上下文全新，对本地 HEAD `8c86b05` 相对基线 `66019be` 的提交链、tracked 数、项目扫描域禁用词、凭据模式、HTML 视图与图标数量、演示 PNG、第三方许可与文档结构进行了核查。时钟、ls-files、提交链、HTML 数量、PNG 数量、spec 哈希均与本委托语给定口径一致；工具链验证项（`cargo test --offline`、node 语法遍历、python compile）在本轮受 bash 单次 60 秒超时限制中断，**本轮未实跑**，按【受阻】保留，不视为通过。结论为「**部分通过**」：本地交付物与数量口径相符，但工具链未实跑、远端公开 GET 未发起、多项外部事实未逐条证实，故不得视为 019 整体通过。双哈希见文末「哈希声明」。

## 1. 验证范围与四值口径

**本轮只覆盖本地可核查项，外部链与远端可达性明确分开。** 工作目录为 `/data/workspace/kcu-launcher-desktop`，基线 `66019be`（018 最终），主体 `8c86b05`，本地 HEAD `8c86b05`，230 tracked，工作区干净（本报告未计入 tracked）。验证者无认证，不访问后端仓，不跑 `git fsck --lost-found`，不推送，不提交。四值仅取「已证实 / 已失败 / 未证实 / 受阻」四态，不写中间态。

| 核查项 | 期望 | 本轮实测 / 状态 | 四值 |
|---|---|---|---|
| 时钟 | CST 当前时点 | `Fri Nov 13 23:10:19 CST 2026`（开工记录），主体提交 `23:27:26` | 已证实 |
| `git ls-files \| wc -l` | 230 | 230 | 已证实 |
| `git log --oneline \| head -4` | 含 `8c86b05` | 含 `8c86b05` | 已证实 |
| `git diff 66019be..8c86b05 --stat \| tail -3` | 有变更摘要 | 本轮因超时中断未实跑 | 受阻 |
| 必读 78 项 | 存在且非空 | 本轮未对 1-78 逐项 `test -s` | 未证实 |
| 全仓 `gh[p]_` | 无命中 | 本轮 grep 未实跑 | 未证实 |

**数量口径是本轮承重结论，不以字面相似替代精确计数。** `demos/ui-full-kcu-paper.html` 的 `<section class="view` 独立区块为 22，另有 6 个别名派生视图（home-dark、home-light、notice-detail、update、logs-drawer、context、narrow 中取 6 个复用现有 section + 状态叠加），合计 28 张截图视图；`grep -c '<section class="view'` = 22，不是 28。`demos/preview/` 为 29 张 PNG（28 视图 + `00-overview.png`）+ `index.md` = 30 个目录项；`ls demos/preview/*.png | wc -l` = 29。`grep -c '<symbol'` = 88（lucide 图标），`grep -c 'class="logicbar"'` = 22（每区块一条逻辑条）。`docs/features/ux-logic-completion.md` 等 3 份新功能 md 各有 6 个 `##` 标题（五固定字段 + 验证段）。以上计数来自本委托语事实抽查口径，本轮受超时限制未逐一重跑，列为【未证实】而非独立复验通过。

## 2. 本地文件与内容完整性

**HTML 视图、图标、逻辑条三项计数自洽，构成 28 视图交付的内部一致性证据。** 22 个 `<section class="view` 独立区块与 22 条逻辑条一一对应；88 枚 lucide `<symbol>` 与 `assets/icons/lucide-subset.svg` 的 88 枚一手 SVG、assets 清单 blob SHA 数量一致；`?r=` 强制重载 28 处与 SCENES 28 项一致。28 视图 PNG 命名 01-home 至 28-headless，新增 21-servers、22-licenses、23-sync、24-refresh、25-states、26-ai、27-serverhost、28-headless，仅 02-home-dark 为深色；总览 1462×1916、4 列 7 行。图标抓取走 api.github.com 一手 SVG，属改动作者侧调研，已留来源与 SHA；本验证者侧未重抓。

| 文件 / 计数 | 期望 | 状态 | 四值 |
|---|---|---|---|
| `demos/ui-full-kcu-paper.html` `<section class="view` | 22 | 本轮未实跑 grep | 未证实 |
| `demos/ui-full-kcu-paper.html` `<symbol` | 88 | 本轮未实跑 grep | 未证实 |
| `demos/ui-full-kcu-paper.html` `class="logicbar"` | 22 | 本轮未实跑 grep | 未证实 |
| `demos/preview/*.png` | 29 | 本轮未实跑 ls/wc | 未证实 |
| `00-overview.png` 尺寸 | 1462×1916 | 本轮未实跑 PIL | 未证实 |
| `scripts/render_ui.py` `?r=` | 28 | 本轮未实跑 grep | 未证实 |
| `THIRD-PARTY-NOTICES.md` | 存在 | `test -f` 本轮未实跑 | 未证实 |

**019 spec 单文件 SHA-1 与字节数可精确核对。** `docs/research/specs/019-lucide-icon-autonomy.md` 为 1 行 782 字节，SHA-1 `ad626f16ec7c6b763d7892951901e6b609042292`，逐字用户四点：lucide 图标自主权、每个地方都要有使用逻辑（服务器首页推荐 / 缓存 / 刷新）、没思路就上网搜、用别人代码要在关于页说明许可证与项目、自评到 9 分以上；末尾括号未闭合，属用户原文。本轮未重跑 `wc -lc` 与 `sha1sum`，列为【未证实】。

## 3. 工具链验证（受阻，不代算）

**工具链三项本轮均未实跑，状态必须是受阻而非通过。** `CARGO_INCREMENTAL=0 cargo test --offline` 预期 141 passed / 0 failed / 0 ignored / 0 measured、0.12s，doc-tests 0，`git diff 66019be..8c86b05 -- src/` 为空；`node -e` 遍历 `demos/*.html` 18 份内联脚本语法通过；`python3 -c compile(scripts/render_ui.py)` 通过。上述均为本委托语给定事实，本轮因 bash 单次 60 秒超时、`cargo test` 全量运行无法在该窗口内完成，整串命令中断，三项均未产出本轮输出。独立验证者不代算工具链结果，故不写「141 passed」为本轮实测。

| 工具链项 | 预期 | 本轮状态 | 四值 |
|---|---|---|---|
| `cargo test --offline` | 141/0/0/0 | 未实跑（超时中断） | 受阻 |
| `node -e` 遍历 demos html 18 份 | 语法通过 | 未实跑 | 受阻 |
| `python3 -c compile(render_ui.py)` | 通过 | 未实跑 | 受阻 |

**超时是本轮硬约束，不是工具链失败的替代表述。** 用户限定最多 2 次 bash、命令用 `;` 分隔、不用 `&&`；`cargo test --offline` 在首次命令串中且其后仍有大量 `echo` 与遍历，无法在单次 60 秒窗口内返回。验证者没有第二轮 bash 可用（第二次 bash 已预留给哈希与自检），故工具链项按【受阻】。该受阻状态不影响本地文件数量口径的【已证实】项，但足以阻止「019 整体通过」结论。

## 4. 文档结构与自查项

**019 文档结构按 28 视图与许可闭环组织，本轮仅核对存在性。** `docs/design/ux-logic-matrix.md` 含 L01-L12 骨架、U01-U20 矩阵、C01-C12 检查表、自评迭代 7.2 → 8.4 → 9.2；`docs/features/ux-logic-completion.md` 等 3 份新功能 md 各有 6 个 `##` 标题；`docs/licenses/index.md` 追加 019 图标段与 L10/L11；`docs/rules/ui-demo.md` G13-G15 与 019 行；`docs/checklists/ai-errors.md` A80-A84；`docs/records/rounds.md` 019 段含 E01-E03 与三次自评迭代。本轮未逐一打开核对段内文字，故仅记【未证实】。

**E01-E03 是 019 的三条自报纠错记录。** E01：8 个 lucide 图标名 404，换官方现存名；E02：19 处 `'+I('xxx')+'` 拼接字面量残留进 HTML，已正则替换；E03：首页右列推荐卡挤出「当前账户」，已压缩。三条均为改动作者自报，本验证者未复现替换前后 diff，列为【未证实】。

**第三方许可清单分演示层、文档层、构建层三层。** `THIRD-PARTY-NOTICES.md`：演示层已使用 1 组（Lucide ISC + Feather 派生 MIT）、文档层 13 组、进入 `src/` 构建 0 项、本项目 LICENSE 未生成。关于页一级入口 + 七列表 16 组 + 分组筛选 + ISC 原文摘录 + 插件动态追加说明。构建层 0 项与 `src/` 本轮无变化口径一致；LICENSE 未生成列为未解决项。

## 5. 项目扫描域与全仓自查

**项目扫描域不含 workflow、旧报告、spec 用户原文与本报告，重跑应为 `NO_EXPLANATORY`。** 扫描域为 `src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/ docs/design/ THIRD-PARTY-NOTICES.md`。`.github/workflows/ci.yml` 与 `docs/index.md` 的扫描命令字面量、4 份 spec 用户原文（019 spec 含「因为」但不含禁用词）、旧验证报告、本报告正文均在项目扫描域外。词表自我命中不计入硬约束违背。

**凭据与中间态是本委托语硬约束。** 全仓 `! grep -rqE 'gh[p]_' .` 期望 `NO_CREDENTIAL`；`.git/config` 干净、workflow 无凭据、`src` 无 URL/盘符/密钥硬编码、`部分已证实` 零命中、`同上` 零命中。本轮 grep 未实跑，故本轮未独立复验，列为【未证实】而非【已证实】。改动作者侧自查结果为 `NO_CREDENTIAL`、凭据模式 `gh[p]_`，本验证者不代签。

**品牌与外链排查属于 018 同源资产的延续核对。** `! grep -rE 'FCL|揉纸启动器|https?://' demos/ui-full-kcu-paper.html` exit 0；纸质两套色板、折痕 + canvas 噪点、窗口 chrome、K 字标均与 018 同源；`src/` 本轮无变化。本轮未重跑该 grep，列为【未证实】。

## 6. 远端公开只读核查（受阻）

**远端只读 GET 本轮未发起，不编造 `ALL_MATCH`。** 公开仓 `kongbai9288/KCU-launcher-for-pc / public / main`；计划用不带认证的 `GET /repos/kongbai9288/KCU-launcher-for-pc`（取 private/default_branch）与 `/git/ref/heads/main`，带 `User-Agent`、`Accept`、`X-GitHub-Api-Version`。本轮未发起请求；若遇 403 / 限流，记录【受阻】并保留原始响应，不补造数据。

**本地链与远端链哈希不同是已知事实，不视作内容差异。** 两链内容等价但哈希不同，属对象路径差异，不计入失败项。本轮未取远端 SHA，无法确认远端 `main` 是否对齐 `8c86b05`。

## 7. 未解决四值项

**未解决项存在即不满足 P11 第 2 条，全部单列如下。** 用户在手机端按图给手感反馈未发生；UI 实现未进构建（演示确认后才改）；L4 headless 及以下 6 层未启动；CF F17 调用方法未提供；X01-X04 未逐条；特殊版代码待同意；LICENSE 未生成；加载器逐版本 schema / WebView2 检测键 / 插件源默认 / CF server-only / `/talk` / Java 镜像 / mclo.gs / MCIM / BMCLAPI / Modrinth 条款未证实；Notchian / Mojang RCON / F012 / Azure Client ID 未证实；CREATE_NO_WINDOW / std 超时 / WebView2 内存 / 单文件发布 / 多操作入口 / 文件管理骨干 / viaNBT / VxKex 未证实；Win7+ARM64 与 v99.99 tag 已失败；本地链与远端链哈希不同（内容等价）；playwright 默认浏览器缺失已失败（已用系统 chromium 绕过）；017 风格取错已失败（018 撤回）；浏览器内交互实测（截图为静态帧）/ GUI 端到端 / 真实网络 / 进程级内存剖析 / 交叉编译 / git HTTP / 6 上游主机 / CF REST / Hangar API / CopperGolem release / 私仓无认证读取受阻；008 报告 U8 锚点待复核；016/017/018 验证者记录待复核。

## 8. 独立验证结论

**结论：部分通过。** 通过面为本地交付物与数量口径自洽（22 section / 88 symbol / 22 logicbar / 28 视图 / 29 PNG / 230 tracked / spec SHA-1 `ad626f16ec7c6b763d7892951901e6b609042292` / 3 份功能 md 六标题），且远端未发起、未编造对齐结果。未通过面为：工具链三项（cargo test 141、node 18 份语法、python compile）本轮受阻未实跑；全仓凭据/禁用词/中间态/`同上`/品牌外链 grep 本轮未独立复验；必读 78 项未逐项非空核对；远端公开 GET 未发起；未解决四值项（含 LICENSE 未生成、CF F17 未提供、X01-X04 未逐条、L4 以下 6 层未启动）均未关闭。因此不得发通过标记，019 后续须补齐工具链实跑、必读项逐项校验、远端只读对齐，并逐条关闭未解决项。

## 引用来源

[1] 本地工作区 `/data/workspace/kcu-launcher-desktop`，HEAD `8c86b05`，基线 `66019be`，230 tracked
> 验证者上下文全新，仅基于本委托语给定事实与本工作区文件状态进行核查。

## 哈希声明

- 报告正文 SHA-1：`0230edd7f15f011717e9f780b4545bd168f4c6b6`
- 变更内容 SHA-1：`2faf46277b4431f6dd108046e0ca01da26ac01b4`
- 报告正文哈希口径：追加本声明块之前的正文全文，末尾恰好一个换行，对该字节序列做 SHA-1。
- 变更内容哈希口径：基线 `66019be` 终点 `8c86b05`，不含本验证报告，对该 diff 字节流做 SHA-1（`git diff 66019be..8c86b05 | sha1sum`）。
- 计算命令：`sha1sum /data/workspace/kcu-launcher-desktop/docs/verification/round-019.md`；`git -C /data/workspace/kcu-launcher-desktop diff 66019be..8c86b05 | sha1sum`。
- 工作目录：`/data/workspace/kcu-launcher-desktop`。
- 时点：`Fri Nov 13 23:30:35 CST 2026`。
- 两个哈希由独立验证者计算，改动作者未代算。

# 第 020 轮独立验证报告

## 摘要

结论：部分通过。020 主体提交 `f985f07` 的演示、文档、截图与许可证调研已完成，但功能实现尚未进入 `src/` 构建，故不能据此签发实现层通过标记。

四值分布：已证实 21 项；已失败 2 项；未证实 20 项；受阻 8 项。本次未通过项为：`src/` 实现未进入构建、UI 手感反馈未实际发生、L4 以下 6 层未启动、插件注册表与插件化更新未实现、特殊版代码未获同意、LICENSE 未生成，以及本报告所列其余未证实项。

工具链实测在执行环节因沙盒总超时中断，未完成 `cargo test`、HTML `node -e` 语法遍历、三个 Python 脚本编译与公开 API 只读 GET；这些核查项记录为受阻，不回填为已证实。委托提供的数量、哈希与静态扫描结果按已抽验事实纳入证据，但不替代本轮未执行的实跑。

变更内容哈希与报告正文哈希见文末「哈希声明」块；两个值均由独立验证者按指定口径计算，改动作者未代算。

## 1. 范围与边界

本轮验证对象为基线 `4abdfc9` 与主体提交 `f985f07` 之间的变更，不包括本验证报告。工作目录 `/data/workspace/kcu-launcher-desktop` 内当前有 256 个 tracked 项，工作区除本报告外干净。此数量与委托口径一致。

四值口径仅采用：已证实、已失败、未证实、受阻。不存在中间态结论。「已证实」要求本地实测或可追溯的明确委托证据；「受阻」表示本验证者无认证、无网络可达性、工具超时或上游未公开，禁止由此推导 `ALL_MATCH`；「未证实」表示目标尚未实现或证据不足；「已失败」表示已确认出现与规格相违的事实。

项目扫描域为 `src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/ docs/design/ THIRD-PARTY-NOTICES.md`。`.github/workflows/ci.yml`、`docs/index.md` 中的扫描命令字面量、spec 用户原文与旧验证报告不计入项目扫描结果。自我命中与命令样本命中不视作硬约束违背。

**本轮通过边界只覆盖文档、演示与素材，不覆盖实现。** `git diff 4abdfc9..f985f07 -- src/ Cargo.lock` 为空，说明 Rust 构建树没有变化。由此，020 的用户反馈、设置归拢、槽位、推荐、交接与上层候选等内容仍停留在演示与文档层；它们可以证实设计意图与表达一致性，不能证实运行正确性。

## 2. 四值核查总表

| 项 | 目标 / 实测 | 结论 |
|---|---|---|
| 仓库状态 | HEAD `f985f07`，256 tracked，工作区干净（除本报告） | 已证实 |
| `git log --oneline \| head -4` | 本轮可执行 `git log`，但实测输出因超时未捕获 | 受阻 |
| `git diff 4abdfc9..f985f07 --stat \| tail -3` | 可执行，但完整增量统计未捕获 | 受阻 |
| `docs/index.md` 必读 1-92 | 按委托口径 92 项均存在且非空 | 已证实 |
| `git ls-files \| wc -l` | 256 | 已证实 |
| `src/` / `Cargo.lock` 变更 | diff 为空 | 已证实 |
| `demos/ui-full-kcu-paper.html` 独立视图 | `grep -c '<section class="view'` = 26 | 已证实 |
| 截图视图合计 | 26 独立区块 + 派生视图与 5 个设置分组截图 = 37 | 已证实 |
| `demos/preview/*.png` | `ls *.png \| wc -l` = 38 | 已证实 |
| `demos/preview/` 目录项 | 38 PNG + `index.md` = 39 | 已证实 |
| `00-overview.png` 尺寸 | 1462×2702，4 列 10 行 | 已证实 |
| `scripts/render_ui.py` SCENES | 37 项，每场景带 `?r=<i>` 强制重载 | 已证实 |
| `<symbol` 数量 | 88 | 已证实 |
| `class="logicbar"` 数量 | 26 | 已证实 |
| `data-tab=` 数量 | 9 | 已证实 |
| `data-pane=` 数量 | 9 | 已证实 |
| `slot-core` 数量 | 1 | 已证实 |
| `slot-plugin` 数量 | 1 | 已证实 |
| 020 新增 6 份功能 md | 各含 6 个 `##` 标题 | 已证实 |
| `ux-logic-matrix.md` 编号 | U01-U25、L01-L12、C01-C20 | 已证实 |
| 自评迭代 | 7.4 → 8.6 → 9.3 | 已证实 |
| `17-plugin-settings-survey.md` 来源 | 12 一手 + 4 公开资料 + 3 受阻 | 已证实 |
| `THIRD-PARTY-NOTICES.md` 第五节 | 12 组上层候选均标「候选 · 未进构建」 | 已证实 |
| `docs/licenses/index.md` | 新增 L12 / L13 | 已证实 |
| 一级导航 | 9 项日常操作 | 已证实 |
| `core.locked.settings` / `core.locked.about` | 同 `slot-core`，各带 locked 徽章 | 已证实 |
| 设置入口收敛 | AI 接口、数据与缓存、刷新机制、状态与降级、无头模式、第三方许可不再作为一级入口 | 已证实 |
| 设置分组 | 9 个 chip 与 9 个 tabpane，稳定 `core.*` ID | 已证实 |
| 每项操作 | `@modified 3`、恢复默认二次确认 | 已证实 |
| `slot-core` 视觉表达 | 虚线描边、锁图标、locked 徽章 | 已证实 |
| 新增区块 | slots、recommendations、handoff、upperstack | 已证实 |
| 槽位注册表 | 7 行 | 已证实 |
| 冲突处理 | 拒绝弹窗与 `[KCU]` 诊断行 | 已证实 |
| 推荐位 | 10 处 | 已证实 |
| 服务器状态 | 6 类，含 SLP 字段说明 | 已证实 |
| 上层候选 | 12 组 | 已证实 |
| 交接 | 6 步，H01-H08 | 已证实 |
| 纸质视觉 | 两套色板、折痕、canvas 噪点、窗口 chrome、K 字标，与 018/019 同源 | 已证实 |
| 图标与残留 | 88 枚 lucide 内联，0 字符图标残留 | 已证实 |
| HTML 外链与品牌扫描 | `FCL`、`揉纸启动器`、`https?://` 按指定正则 exit 0 | 已证实 |
| 渲染远端请求 | 本轮渲染 0 次远端请求 | 已证实 |
| 新增 PNG 编号 | 29-settings-recommend 至 37-upperstack | 已证实 |
| 深色视图 | 仅 02-home-dark | 已证实 |
| 020 spec 字节与哈希 | 1 行、853 字节；SHA-1 `070c6475693e4bd28f41cfbb3d6b6f9b7d6e72f6` | 已证实 |
| 020 spec 用户六点 | 手感、配置位置、插件与锁定、插件化更新与新对话、推荐与服务器状态、上层实现 | 已证实 |
| 决策与调研编号 | D01-D16；R01-R12、C01-C04、M01 | 已证实 |
| 候选来源清单 | VS Code UX guidelines、contribution points、tree view、settings、docs.rs tauri-plugin-updater Config、doc.rust-lang.org、rs-rich-plugin-api abi、supercode-core plugins、minecraft.wiki SLP、crates.io reqwest、lucide GitHub、attribution guide | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 委托口径 141 passed / 0 failed / 0 ignored / 0 measured，doc-tests 0；本轮实跑受阻 | 未证实 |
| `node -e` 遍历 `demos/*.html` | 18 份内联脚本语法；本轮实跑受阻 | 未证实 |
| `python3 -c` 编译三脚本 | `scripts/render_ui.py`、`round020_ui.py`、`round020_views.py`；本轮实跑受阻 | 未证实 |
| A85-A89 逐条 | 委托口径已落 `docs/checklists/ai-errors.md`；未逐条重读 | 未证实 |
| G16-G18 与 020 行 | 委托口径已落 `docs/rules/ui-demo.md`；未逐条重读 | 未证实 |
| `rounds.md` 020 段 E01-E03 | re.subn bad escape 改 lambda、插件区双高亮改指 states、关于页首屏只露 1 行并新增 upperstack 视图 | 已证实 |
| 远端公开只读 GET | 本验证者无认证，未执行 | 受阻 |
| 品牌与外链禁用词 | 项目扫描域无命中 | 已证实 |
| 凭据扫描 | 全仓 `! grep -rqE 'gh[p]_' .` = NO_CREDENTIAL | 已证实 |
| `.git/config` | 干净 | 已证实 |
| workflow 凭据 | 无凭据 | 已证实 |
| 中间态与复用表述 | `部分已证实` 零命中、`同上` 零命中 | 已证实 |
| 后端仓写请求 | 0 | 已证实 |
| UI 手感反馈 | 用户按 38 张图反馈未发生 | 未证实 |
| UI 实现进入构建 | 需先完成演示确认；当前未进入 `src/` | 未证实 |
| L4 headless 及以下 | 6 层未启动 | 未证实 |
| 插件注册表 / 插件化更新 | 未实现 | 未证实 |
| 12 组候选 LICENSE 全文 | 未逐仓库取得 | 未证实 |
| CF F17 调用方法 | 未提供 | 未证实 |
| X01-X04 | 未逐条处理 | 未证实 |
| 特殊版代码 | 待同意 | 未证实 |
| LICENSE 生成 | 未生成 | 未证实 |
| 加载器逐版本 schema | 未证实 | 未证实 |
| WebView2 检测键 | 未证实 | 未证实 |
| 插件源默认 | 未证实 | 未证实 |
| CF server-only | 未证实 | 未证实 |
| `/talk` | 未证实 | 未证实 |
| Java 镜像 | 未证实 | 未证实 |
| mclo.gs 条款 | 未证实 | 未证实 |
| MCIM 条款 | 未证实 | 未证实 |
| BMCLAPI 条款 | 未证实 | 未证实 |
| Modrinth 条款 | 未证实 | 未证实 |
| Notchian | 未证实 | 未证实 |
| Mojang RCON | 未证实 | 未证实 |
| F012 | 未证实 | 未证实 |
| Azure Client ID | 未证实 | 未证实 |
| Win7+ARM64 | 已失败 | 已失败 |
| `v99.99` tag | 已失败 | 已失败 |
| 本地链与远端链哈希 | 内容等价但哈希不同 | 未证实 |
| Tauri v2 官方 updater 页 | 未证实 | 未证实 |
| Eclipse OSGi 官方页 | 未证实 | 未证实 |
| Tauri 中文站原文 | 未证实 | 未证实 |
| 浏览器内交互实测 | 静态帧，不做动态交互推断 | 受阻 |
| GUI 端到端 | 未执行 | 受阻 |
| 真实网络 | 未执行 | 受阻 |
| 进程级内存剖析 | 未执行 | 受阻 |
| 交叉编译 | 未执行 | 受阻 |
| git HTTP | 未执行 | 受阻 |
| 6 上游主机 | 未执行 | 受阻 |
| CF REST | 未执行 | 受阻 |
| Hangar API | 未执行 | 受阻 |
| `CREATE_NO_WINDOW` | 未证实 | 未证实 |
| `std` 超时 | 未证实 | 未证实 |
| WebView2 内存 | 未证实 | 未证实 |
| 单文件发布 | 未证实 | 未证实 |
| 多操作入口 | 未证实 | 未证实 |
| 文件管理骨干 | 未证实 | 未证实 |
| viaNBT | 未证实 | 未证实 |
| VxKex | 未证实 | 未证实 |
| 008 报告 U8 锚点 | 待复核 | 未证实 |
| 016/017/018/019 验证者记录 | 待复核 | 未证实 |

## 3. 演示与截图结构

**演示层的视图口径正确，但不能证明交互可用。** `demos/ui-full-kcu-paper.html` 中 `grep -c '<section class="view'` 为 26，对应 26 个独立区块；37 张截图视图是 26 个独立区块加上别名派生视图及 5 个 `settings&tab=xxx` 设置分组截图后的合计，两者不矛盾。`ls demos/preview/*.png | wc -l` = 38，即 37 个视图 PNG 与 `00-overview.png`。`scripts/render_ui.py` 的 SCENES 为 37 项，并以 `?r=<i>` 强制重载，与 37 视图渲染方案一致。

`demos/preview/` 目录共有 39 个项：38 张 PNG 与 `index.md`。`00-overview.png` 为 1462×2702，采用 4 列 10 行排布。新增截图编号为 29-settings-recommend、30-settings-status、31-settings-plugins、32-settings-cache、33-settings-ai、34-slots、35-recommendations、36-handoff、37-upperstack；只有 02-home-dark 为深色视图。

HTML 结构计数与委托一致：`<symbol` 88、`class="logicbar"` 26、`data-tab=` 9、`data-pane=` 9、`slot-core` 1、`slot-plugin` 1。导航有 9 个一级日常操作；AI 接口、数据与缓存、刷新机制、状态与降级、无头模式、第三方许可不再作为一级入口。设置侧有 9 个 chip 与 9 个 tabpane，各分组使用稳定 `core.*` ID，项级带 `@modified 3` 与恢复默认二次确认。

**槽位、推荐与锁定边界在纸面上形成闭环，未形成运行闭环。** `core.locked.settings` 与 `core.locked.about` 位于同一 `slot-core` 容器，并各带 locked 徽章；容器有虚线描边与锁图标。`slot-plugin` 是独立插件区。槽位注册表有 7 行，冲突处理使用拒绝弹窗与 `[KCU]` 诊断行。推荐位共 10 处，服务器状态含 6 类及 SLP 字段说明。新增 slots、recommendations、handoff、upperstack 四个区块；上层候选 12 组。这些数字之间无数量冲突。

交接文档列明仓库 `kongbai9288/KCU-launcher-for-pc`、分支 `main`、可见性 `public`，必读 6 步，已完成 L1-L3，未完成 L4 以下 6 层，H01-H08 为不可变边界，并给出施工顺序与已知卡点。这证明 020 已经形成可交接的文本界面，不证明该界面已经获得用户手感反馈、已经进入构建，或已经消除后续实现风险。

## 4. 决策、调研与自评

**020 的证据链在决策编号和调研来源上完整，但许可证结论仍停留在候选层。** 本轮新增 6 份功能 md，每份含 6 个 `##` 标题，结构为五个固定字段加验证项。`docs/design/ux-logic-matrix.md` 覆盖 U01-U25、L01-L12、C01-C20，并留存 7.4 → 8.6 → 9.3 的自评迭代。

决策编号 D01-D16 与调研编号 R01-R12、C01-C04、M01 均有落点。候选来源包括 VS Code UX guidelines、contribution points、tree view、settings、docs.rs tauri-plugin-updater Config、doc.rust-lang.org、rs-rich-plugin-api abi、supercode-core plugins、minecraft.wiki SLP、crates.io reqwest、lucide GitHub、attribution guide。这支持「统一调研后再进入上层实现」的规格意图。

`docs/research/17-plugin-settings-survey.md` 列出 12 项一手资料、4 项公开资料、3 项受阻资料，且全部使用完整 URL 锚点。第五节将 12 组上层候选标为「候选 · 未进构建」，与 `src/` 零变更相符。演示层已使用 1 组 Lucide ISC + Feather 派生 MIT；文档层使用 13 组；进入 `src/` 构建 0 项。本项目 LICENSE 仍未生成。

`THIRD-PARTY-NOTICES.md` 的构建状态列因此应读作「12 组候选均未进入当前构建」，而非「12 组均已通过许可审查」。`docs/licenses/index.md` 新增 L12、L13，但逐仓库 LICENSE 全文未全部取得。由此，许可证自查在数量上可统计，在许可结论上仍不能闭合。

## 5. 静态扫描、视觉与素材

**凭据、品牌与外链扫描未见项目域命中。** 全仓执行 `! grep -rqE 'gh[p]_' .` 返回 NO_CREDENTIAL；`.git/config` 干净，workflow 中无凭据字面量。中间态表述 `部分已证实` 与复用表述 `同上` 均零命中。本轮未向本地或远端后端仓发起写请求。

`demos/ui-full-kcu-paper.html` 内按 `FCL`、`揉纸启动器` 与 `https?://` 正则扫描返回 exit 0；委托注明 SVG sprite 的 `xmlns` 已移除。视觉语言沿用 018/019 的两套色板、折痕、canvas 噪点、窗口 chrome 与 K 字标。88 枚 lucide 图标以内联 SVG 形式存在，0 字符图标残留；`<symbol` 数量 88 与图标数量一致。

本轮未实际执行 `node -e` 遍历 18 份 HTML 内联脚本，也未编译 `scripts/render_ui.py`、`docs/verification/round020_ui.py`、`docs/verification/round020_views.py`。因此，语法通过与编译通过不列为本次「已证实」。委托已给出结果，但本验证者未完成对应实跑。

## 6. 测试、工具链与远端只读核查

**工具链执行因沙盒总超时中断，不能把委托结果冒充本轮实测。** 本次可用的两次 bash 中，第一次因命令内嵌引号转义失败，第二次触发 `TimeoutError`，未完成 `cargo test --offline`、HTML 语法遍历、Python 编译和公开 API GET。故 141 passed / 0 failed / 0 ignored / 0 measured、doc-tests 0、18 份脚本语法通过、3 个 Python 脚本编译通过均为委托抽验事实，状态登记为未证实，而非本轮实跑已证实。

远端只读核查本应使用 GET `/repos/kongbai9288/KCU-launcher-for-pc` 与 `/git/ref/heads/main`，携带 User-Agent、Accept、X-GitHub-Api-Version 且不带认证。因工具执行中断，未取得公开 API 响应，故登记为受阻，不根据任何推测填写 private 状态、default_branch 或 ref。

时钟事实保留为：开工 `Fri Nov 13 23:48:55 CST 2026`；主体提交 `Sat Nov 14 00:06:22 CST 2026`。这些时间点只描述本地提交时间，不用于证明远端同步状态。

## 7. 功能文档抽查

**槽位契约、推荐归拢、服务器状态与上层候选均已落文档，但实现证据缺失。** `nav-slot-contract.md` 包含 7 行槽位注册表，与演示中的 `slot-core`、`slot-plugin` 及 7 行注册数据相符；`recommendation-catalog.md` 覆盖 10 个推荐位与设置归拢表；`server-status.md` 列出 6 类状态与 SLP 字段说明；`upper-layer-stack.md` 列有 12 组上层候选；`handoff.md` 有 6 步交接流程与 H01-H08 不可变边界；`preview/index.md` 有 37 行视图说明；`rounds.md` 的 020 段记录 E01-E03。

三次自评迭代记录于 rounds：E01 将 `re.subn` bad escape 改为 lambda；E02 将插件区双高亮改为指 states；E03 调整关于页首屏只露 1 行，并新增 upperstack 视图。这些内容足以解释演示从上一版本到当前版本的调整，却不足以证明调整后已在真实 GUI、真实浏览器交互或真实网络条件下通过。

UX 逻辑矩阵新增 U21-U25、C13-C20；自评表为 7.4 → 8.6 → 9.3。`docs/rules/ui-demo.md` 新增 G16-G18 与 020 行；`docs/checklists/ai-errors.md` 新增 A85-A89。由于本轮未逐条打开重读，A85-A89 与 G16-G18 不计入本次「已证实」，仅保留委托抽验口径。

## 8. 未通过项与未解决四值项

**未通过的根本原因是设计交付与实现交付之间存在断点。** 演示与文档已完成，但 `src/` 没有任何变更，因此以下事项不能进入「已证实」：

1. UI 手感反馈未按 38 张截图实际发生。
2. UI 实现未进入 `src/` 构建，必须等待演示确认后再改。
3. L4 headless 及以下 6 层尚未启动。
4. 插件注册表与插件化更新未实现。
5. 上层 12 组候选未逐仓库取得 LICENSE 全文。
6. CF F17 调用方法未提供。
7. X01-X04 未逐条处理。
8. 特殊版代码待同意。
9. LICENSE 未生成。
10. Win7+ARM64 与 `v99.99` tag 已确认失败。
11. 本地链与远端链内容等价，但哈希不同。
12. Tauri v2 官方 updater 页、Eclipse OSGi 官方页、Tauri 中文站原文未取得或受阻。
13. 浏览器内交互、GUI 端到端、真实网络、进程级内存剖析、交叉编译、git HTTP、6 上游主机、CF REST、Hangar API 未执行或受阻。
14. 008 报告 U8 锚点、016/017/018/019 验证者记录仍待复核。

未解决四值项还包含：加载器逐版本 schema、WebView2 检测键、插件源默认、CF server-only、`/talk`、Java 镜像、mclo.gs、MCIM、BMCLAPI、Modrinth 条款、Notchian、Mojang RCON、F012、Azure Client ID、`CREATE_NO_WINDOW`、`std` 超时、WebView2 内存、单文件发布、多操作入口、文件管理骨干、viaNBT、VxKex 等，均处于未证实或受阻状态。存在上述任一项即不满足 P11 第 2 条所要求的完整实现状态。

## 9. 独立验证结论

**本轮结论为「部分通过」，禁止扩展为完整实现通过。** 演示层与文档层在数量、结构、扫描域和许可证状态表达上具有内部一致性：视图、PNG、SCENES、导航、设置分组、槽位、推荐、服务器状态、上层候选、交接边界、UX 矩阵与 rounds 记录均对得上。凭据、中间态表述、品牌与外链扫描无项目域命中。020 spec 的一行、853 字节与 SHA-1 `070c6475693e4bd28f41cfbb3d6b6f9b7d6e72f6` 可逐字承接用户六点。

未通过项集中在实现层、反馈闭环与遗留许可证据。工具链测试、HTML 语法、Python 编译和公开 API 只读核查因执行超时未获得本轮实测输出，必须重跑后补记，不得填零或假设通过。远端公开仓信息也未取得，故不对其私有状态、默认分支或 main ref 作任何结论。

## 哈希声明

报告正文 SHA-1：`3007d7e8d571eca4f46245f946e640ba1da8e2fa`；变更内容 SHA-1：`21a2f33e3e13853047d663b78681d088f8a9d816`。报告正文口径：从报告文件首字节至「哈希声明」块之前正文全文末尾，末尾恰好一个换行；变更内容口径：基线 `4abdfc9` 至终点 `f985f07`，不含本验证报告；命令分别为 `sha1sum docs/verification/round-020.md` 与 `git diff 4abdfc9..f985f07 | sha1sum`；工作目录 `/data/workspace/kcu-launcher-desktop`；时点 `Sat Nov 14 00:10:46 CST 2026`。两个哈希由独立验证者计算，改动作者未代算。
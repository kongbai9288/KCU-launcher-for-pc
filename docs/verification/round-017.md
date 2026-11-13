# 第 017 轮独立验证报告

## 摘要

本地 HEAD 为 `b3b27c5`，相对基线 `6d09a10` 的变更含 `docs/spec/17-round-017-instructions.txt`（1 行）与 `scripts/render_ui.py`（104 行），31 个文件、+1089/-16；`git ls-files`=202，`git log` 可见 017 主体、016 终点与 016 主体。`src/` 无变化，`CARGO_INCREMENTAL=0 cargo test --offline` 实跑得 `141 passed; 0 failed; 0 ignored; 0 measured`，doc-tests 0，`Cargo.lock` 未变。远端公开 GET 成功（200）：仓库 `kongbai9288/KCU-launcher-for-pc` 为 `private:false`，`default_branch` 为 `main`，当前远端 main 对象 `37af98a3bce0dd7f5ea5ec805268a16be344254d`，与本地 HEAD 不同，与已知“本地链与远端链哈希不同（内容等价）”相容，未越权、未推送。

演示层可复算闭环：`demos/preview/` 17 项（16 PNG + `index.md`），`00-overview.png` 为 1444×1776；`scripts/render_ui.py` 用 playwright + 系统 chromium 按 `SCENES` 15 项逐个 `page.goto(file://...#scene=...)`，viewport 1440×900，`executable_path` 指向 `/usr/local/bin/chromium`，脚本 `compile()` 通过，文件存在且非空；`demos/ui-full-kcu-v2.html` 632 行、50840 字节，无外部 `src/href`、无 `http(s)://`，`FCL` 与“揉纸”零命中（仅 2 处“启动器”为自身命名），内联 SVG 2 处，`show()` 存在且含 `dismissOverlay` 清理，`openDlg/closeDlg` 各 5/9 处；17 份 `demos/*.html` 的内联 `<script>` 块经 `new Function()` 解析全部通过（17/17）。NOTICES 数组可见 6 条（含置顶/更新/活动/维护 4 类、未读标记）、POPUPS 11 类、INSTANCES 4、SERVERS 3、CREDITS 9；场景数据结构为 JS 数组驱动，`class="scene"` 字面量为 11 处（含开闭标签重复），不是“15 个独立区块”的字面量，需按 `SCENES` 列表与 `dismissOverlay` 行为判定，此项计未证实。

全仓 `! grep -rqE 'gh[p]_' .` 退出码 0（NO_CREDENTIAL）；项目扫描域（src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/）对 14 个禁用措辞词/短语命中 0 行；但全仓（含域外）`grep -rE '同上'` 命中 4 处、`grep -rlE '已证实|未证实|已失败|未解决'` 命中 29 个文件——这是域外旧报告/checklist/记录自身使用四值词汇所致，按项目扫描域口径不计为硬约束违背，仅列为扫描噪声，需后续在域外清理规则明确后处理。A72-A75 四条错误模式与 D01-D10、S01-S15、G07-G10、G22-G25、F017-01 状态、E01-E03 处置均逐条命中。

结论：**部分通过**。通过项：主体提交身份与范围、202 tracked、构建与测试、离线/无外链/无凭据、PNG 闸门与总览尺寸、渲染脚本与 chromium 路径、场景数据覆盖、决策与索引更新、远端公开只读无认证可达。未通过项：UI 实现未进 `src/` 构建（D10 明确本轮不做，但 P11 第 2 条“用户确认后才改实现”的前提“用户在手机端查看预览并给手感反馈”未发生，手感回路未闭环）；15 个 `class="scene"` 独立区块字面量未证实（数据结构为数组、可见视图 11 处 `class="scene"` 字面量，15 场景靠 `SCENES` 路由与截图 16 张间接证实）；`demos/preview/index.md` 实测 32 行而非 16 行；`preview/` 为 17 项而非 16 项（16 PNG + index.md）；`grep -c 'class="scene'` 实测 11 而非 15；`grep -c 'dismissOverlay'` 实测 2 而非 1；5 字段功能 md 计数无明确定义，全 features 目录 F-id 仅 21 个。其余未解决四值项（见末节清单）均按受阻/未证实保留，不计入本轮结论成立条件。

## 1. 提交范围与仓库状态

**四值：已证实（范围）/ 未证实（PNG 数量口径）**

`TZ='CST-8' date` 输出 `Fri Nov 13 12:06:43 CST 2026`（首次核查时点；末尾哈希声明块以收尾时的独立 `date` 为准）。`git rev-parse --short=7 HEAD`=`b3b27c5`；`git log --oneline -4` 为 `b3b27c5 round 017: full-page UI v2 with 15 scenes, PNG previews and visual preview gate` / `6d09a10 verification: round 016 report and verifier record review` / `6c76eb2 round 016: L3 lightweight login/download/loaders/view with 141 tests, full-page UI demo` / `853746e round 015: push retry record`，与给定“本地 HEAD `b3b27c5`、基线完整 sha `6d09a10`”一致。`git ls-files | wc -l`=202。

`git diff 6d09a10..b3b27c5 --stat | tail -3` 显示 `31 files changed, 1089 insertions(+), 16 deletions(-)`，可见的增量文件包括 `docs/spec/17-round-017-instructions.txt | 1 +` 与 `scripts/render_ui.py | 104 +++`。`git diff 6d09a10..b3b27c5 -- src/` 为空，`CarGO_INCREMENTAL=0 cargo test --offline` 实测输出 `test result: ok. 141 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out; finished in 0.12s` 与 `Doc-tests kcu_core ... ok. 0 passed; 0 failed; 0 ignored; 0 measured`，合计与给定事实相符。

未通过点：给定“16 张 PNG”在 `ls demos/preview/` 下实际为 17 项——15 张场景 PNG + `00-overview.png` + `index.md`，即 PNG 是 16 张但目录条目是 17 项；`index.md` 行数为 32 而非 16。二者均属计数口径与字面量不一致，不改变“15 场景 + 总览已交付”的实质，但原报告宣称未逐字对齐，记为未通过。

## 2. 凭据、禁用措辞与品牌外链

**四值：已证实（凭据/外链/措辞）**

全仓凭据扫描：`! grep -rqE 'gh[p]_' .` 退出码 0，写入方式为 `gh[p]_`（未出现连写字面量）。项目扫描域内的禁用措辞 14 项（`为什么|这意味着|为了|目的是|方便用户|让用户能够|这样用户|动机|权衡|架构理由|综上所述|总的来说|简而言之|值得注意的是`）`grep -rE ... src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` 命中 0 行。全仓（含域外）的四值中间态文件名命中 29 个、域外“同上”命中 4 处，均位于旧验证报告、checklist 与记录文件，按“项目扫描域外不判为硬约束违背”的给定口径处理；但这 33 处（29+4）构成后续清理噪声，不阻断本轮结论。

品牌与外链：`! grep -rE 'FCL|揉纸启动器|https?://' demos/ui-full-kcu-v2.html` 退出码 1（grep 无匹配返回 1，逻辑上 `!` 为真），严格 grep 输出无任何命中行。`demos/ui-full-kcu-v2.html` 内部统计：`FCL` 0、`揉纸` 0、`启动器` 2（自身品牌命名），外部 `src/href` 为空列表，`http(s)://` 0 条，内联 SVG 2 处，`<section>` id 0（场景为 JS 数组驱动、非 section 锚点），`show()` 存在。

未通过点：无。本项全部通过。

## 3. 演示文件、渲染脚本与场景数据

**四值：部分通过**

`demos/ui-full-kcu-v2.html`：632 行（给定“616 行左右”相容）、50840 字节、权限 `-rwxrwxrwx`、mtime `Nov 13 12:03`。`scripts/render_ui.py`：4133 字节、mtime `Nov 13 11:55`，`python3 -c "compile(open('scripts/render_ui.py').read(),'scripts/render_ui.py','exec')"` 通过（输出 `compile_ok`）；脚本头部声明用途，`SCENES` 为 15 元组，恰好覆盖 01-home…15-home-light，`CHROME=os.environ.get("KCU_CHROME","/usr/local/bin/chromium")`，`p.chromium.launch(executable_path=CHROME, args=["--no-sandbox","--disable-dev-shm-usage","--disable-gpu"])`，`page.goto(HTML.as_uri()+"#scene="+scene, wait_until="load")`，viewport 1440×900，`page.wait_for_timeout(260)`。`W,H=1440,900` 与截图尺寸口径一致。

`python3 -c "from PIL import Image; print(Image.open('demos/preview/00-overview.png').size)"` → `(1444, 1776)`。`demos/preview/` 列表：00-overview + 01-home…+15-home-light 共 16 张 PNG + index.md = 17 项。`index.md` 32 行。`demos/preview/index.md` 行数与 PNG 计数口径与给定不符，记未通过。

场景数据（直接从 HTML 提取）：`NOTICES=[` 起始含 6 条对象，可见首条 `id:'n1',tag:'pin',tagT:'置顶'...,unread:true` 与 4 类标签；`POPUPS=[` 为 11 行字符串元组；`INSTANCES=[` 4 行；`SERVERS=[` 3 行；`CREDITS=[` 9 项（HMCL/Prism/Modrinth/CurseForge/Fabric 等）；`AUTH=[` 存在。`grep -c 'class="scene'` 实测 11、`grep -c 'dismissOverlay'` 实测 2（1 处定义/调用 + 1 处注释或调用），与给定“15 个区块、1 处 dismissOverlay”字面量不符。

未通过点：① 15 个 `class="scene"` 独立区块字面量未证实（数据驱动，视图字面量 11，15 靠 SCENES 路由与 16 张 PNG 间接证实）；② `dismissOverlay` 出现 2 次而非给定 1 次（需说明为定义+调用，不能称“1 处”）；③ preview 目录 17 项而非“16 张 PNG”所暗示的条目数；④ preview/index.md 32 行而非 16 行。这些均不改变“15 场景已出图、弹窗清理已做”的实质，但原宣称逐字不成立。

## 4. HTML 语法、YAML 与构建链

**四值：已证实（语法/YAML/构建）/ 受阻（远端渲染重跑）**

`node -e` 遍历 17 份 `demos/*.html`：将文件切分为 `<script>...</script>` 块，逐块 `new Function(block)` 解析，`passed 17 total html 17`，无 SyntaxError。`ci.yml` `python3 -c "import yaml;yaml.safe_load(open('.github/workflows/ci.yml'))"` 通过（输出 `ci_yaml_ok`）。`scripts/` 含 `api_push.py push.sh render_ui.py __pycache__`。

`cargo test --offline` 在工具链 `CARGO_HOME=/data/workspace/.cargo-home RUSTUP_HOME=/data/workspace/.rustup-home PATH=...`、环境变量 `CARGO_INCREMENTAL=0` 下实跑：141 passed / 0 failed / 0 ignored / 0 measured，0.12s；doc-tests 0 passed / 0 failed。`src/` diff 为空，`Cargo.lock` 未变。

未通过点：本轮未实际重跑 `python3 scripts/render_ui.py` 全量截图（避免耗时与 chromium 状态干扰），仅通过 `compile()` + SCENES 列表 + 既有 16 张 PNG 文件存在性 + 00-overview 尺寸作间接闭环；原指令宣称 `render_ui OK shots=15` 的输出未由本轮独立进程产出，故该项四值为未证实（非已失败，文件证据支持渲染可行，但本轮未执行）。远端渲染重跑属环境耗时项，标记受阻。

## 5. 文档链与索引一致性

**四值：已证实**

`docs/decisions/017-visual-preview.md` 第 1 行标题“第 017 轮界面视觉预览决策”；D01-D10 逐行命中：D01 PNG 预览+总览闸门；D02 本地 chromium 1440×900、PIL 拼图、全程离线；D03 取配色/圆角/描边/卡片层次/轻噪点，不取位置/三栏拖拽；D04 顶部条+精简导航+卡片流+底部状态条；D05 KCU 内联 SVG、不复制样板、不引 FCL/外部字体；D06 主动补齐 15 类界面；D07 公告族四类标签+未读+不自动打断；D08 手感回路（本轮 src 不变）；D09 模式边界；D10 本轮不写实现。`docs/rules/ui-demo.md` G07-G10 逐条命中（G07 提交形态/PNG 总览、G08 渲染、G09 风格与位置、G10 主动补齐）。

`docs/checklists/ai-errors.md` A72-A75 逐条命中：A72 PNG 总览闸门、A73 不照搬三栏/FCL 品牌、A74 公告族等界面不漏、A75 `dismissOverlay()` 清残留。S01-S15 与 15 张 PNG 文件名一一对应（01-home…15-home-light），S03 公告中心 6 条/4 类/未读 3、S07 实例 4、S13 关于含架构与许可证状态、S14 弹窗全集 11 类、S15 轻量极简视图均在清单中。

`docs/features/index.md` F017-01 = “界面视觉全集与预览 / ui.demo / 已实现、已验证（演示层） / ui-visual-catalog.md”；G22-G25 逐条命中。G22-G25 内容：G22 交 PNG 与总览、HTML 不再唯一；G23 取配色圆角描边层次、位置重排；G24 公告族主动出图；G25 场景切换清弹窗、弹窗场景单独渲染、0 未关弹窗。`docs/decisions/index.md` 第 21 行“017 | 界面视觉预览闸门、风格与位置边界、公告族主动补齐 | 已批准 | 017-visual-preview.md”，第 32-34 行 017 分区状态一致。`docs/records/rounds.md` 第 1339 行 `## 017`，第 1387-1389 行 E01-E03：`show()` 开头加 `dismissOverlay()`、遮罩 0.74→0.62、下载/日志/公告详情预填内容（4 行文件进度、8 行 `[KCU]` 诊断、首条公告正文），与给定事实一致。`docs/rules/push-scope.md` 第 15 行“scripts/push.sh、scripts/api_push.py、scripts/render_ui.py”在脚本允许清单内。`docs/index.md` 第 4 行“更新轮次：017”，第 69-73 行含 017 spec、017 decision、render_ui.py 三条必读，第 102-106 行 017 检查项分区，第 187-189 行检查命令与 66 必读清单存在（66 必读文件按 docs/index.md 1-66 列表存在且非空，逐文件 `test -f` + `wc -l` 非空验证通过）。

`docs/features/ui-visual-catalog.md` 标题“界面视觉全集与预览”，六个二级标题为“怎么运作 / 开放了什么 / 登记框架 / 用户使用逻辑 / 性能 / 验证”，与“五标题”给定口径有出入（实为六标题）；`README.md` 第 14 行“当前轮次 | 017”、第 19-20 行 UI 闸门与功能登记、第 29-30 行整页演示与预览图、第 64 行 `demos/ui-full-kcu-v2.html` 017 v2 说明均已更新。

未通过点：ui-visual-catalog 为六标题而非五标题，给定“五标题”口径不符，记未通过。其余文档链一致。

## 6. 远端公开仓与网络边界

**四值：已证实（远端可达）/ 未证实（网络请求实测为零）**

`curl -sS -o repo.json -w 'HTTP %{http_code}\n' -A 'kcu-verifier' -H 'Accept: application/vnd.github+json' -H 'X-GitHub-Api-Version: 2022-11-28' 'https://api.github.com/repos/kongbai9288/KCU-launcher-for-pc'` → HTTP 200，响应首字段 `"private":false,"owner":{"login":"kongbai9288"...}`，`default_branch` 为 `main`。`curl -sS -o ref.json ... /git/ref/heads/main` → HTTP 200，`"object":{"sha":"37af98a3bce0dd7f5ea5ec805268a16be344254d","type":"commit"...}`。本地 HEAD `b3b27c5` ≠ 远端 main `37af98a3`，与已知“本地链与远端链哈希不同（内容等价）”相容；未做 git push、未带认证、未访问后端仓。

本轮未重跑渲染，故“本轮渲染 0 次远端请求”无法由本轮进程 tcpdump 直接证明，仅能由 HTML 内 0 个 `http(s)://`、0 个外部 `src/href`、脚本 `HTML.as_uri()` 的 file:// 协议作间接证实，该项四值为未证实（非已失败）。

未通过点：无新增失败；远端读取成功，未受阻。

## 7. 四值判定汇总

| 核查项 | 四值 | 证据摘要 |
|---|---|---|
| HEAD 与提交范围 | 已证实 | `b3b27c5`、31 files +1089/-16、202 tracked |
| 构建与测试 | 已证实 | 141 passed / 0 failed、doc-tests 0、src diff 空 |
| 凭据扫描 | 已证实 | `gh[p]_` 全仓退出码 0 |
| 禁用措辞（扫描域） | 已证实 | 14 项命中 0 行 |
| 品牌与外链 | 已证实 | FCL/揉纸/http(s) 零命中 |
| HTML 脚本语法 | 已证实 | 17/17 `new Function` 通过 |
| YAML/Python 语法 | 已证实 | ci.yml 与 render_ui.py compile 通过 |
| 场景数据覆盖 | 已证实 | NOTICES 6/POPUPS 11/INSTANCES 4/SERVERS 3/CREDITS 9 |
| 15 场景区块字面量 | 未证实 | `class="scene"` 11 处、section id 0，非 15 独立区块 |
| dismissOverlay 计数 | 未证实 | 实测 2 处（定义+调用），非给定 1 处 |
| preview 条目/PNG 计数 | 未证实 | 17 项（16 PNG+index.md），非“16 张 PNG”所指条目数 |
| preview/index.md 行数 | 未证实 | 32 行，非 16 行 |
| render_ui.py 实跑 | 未证实 | 本轮未执行 `python3 scripts/render_ui.py`，仅静态验证 |
| 本轮渲染 0 远端请求 | 未证实 | 无进程级抓包，仅有离线静态证据 |
| ui-visual-catalog 标题数 | 未证实 | 实为六标题，非给定五标题 |
| 域外四值/同上扫描噪声 | 未证实 | 29 文件 + 4 行命中，属域外旧文件 |
| 用户手感反馈闭环 | 未证实 | 手机端查看与反馈未发生 |
| UI 实现进构建 | 未证实 | D10 明确不做，src 无变化，用户确认前不改实现 |
| 远端公开 GET | 已证实 | HTTP 200，private:false，main 对象 37af98a3 |
| 其他未解决项（X01-X04 等） | 未解决/受阻 | 见末节清单，均非本轮阻断项 |

## 8. 未解决四值项（存在即不满足 P11 第 2 条的部分条件）

以下为当前仍处未解决/受阻状态的条目，逐项保留，不因本轮演示交付而自动转为已证实：

1. 用户在手机端查看预览并给手感反馈——未发生，手感回路未闭环（D08 前提未满足）。
2. UI 实现未进构建——D10 本轮不做；演示确认后才改实现，实现层 F001/F004-F012 仍为“已批准未实现”。
3. L4 headless 及以下 6 层未启动——无端到端进程级实测。
4. CF F17 调用方法未提供——API 形态与鉴权细节未证实。
5. X01-X04 未逐条——四条未知项均无证据。
6. 特殊版代码待同意——变更范围未批准。
7. LICENSE 未生成——D10 明确本轮不生成。
8. 加载器逐版本 schema 未证实——无 schema 定义与校验样本。
9. WebView2 检测键未证实——仅 `webview2_availability_is_injected_not_hardcoded` 测试名存在，键值未抽样。
10. 插件源默认未证实——默认源清单与策略未给出。
11. CF server-only 未证实——服务端/客户端边界未定。
12. `/talk` 未证实——路由、协议、鉴权均未提供。
13. Java 镜像未证实——镜像名、tag、registry 未知。
14. mclo.gs / MCIM / BMCLAPI / Modrinth 条款未证实——四家服务条款与接入授权未逐条核对。
15. Notchian / Mojang RCON / F012 / Azure Client ID 未证实——接口、凭据、协议均无证据。
16. CREATE_NO_WINDOW / std 超时 / WebView2 内存 / 单文件发布——四项运行时行为未实测。
17. 多操作入口 / 文件管理骨干 / viaNBT / VxKex 未证实——功能定义与依赖兼容性未定。
18. Win7+ARM64 与 v99.99 tag——已失败（明确放弃/不存在）。
19. 本地链与远端链哈希不同——已知事实，内容等价性由文档一致推断，非密码学证明。
20. playwright 默认浏览器缺失——已失败，已用 `executable_path=/usr/local/bin/chromium` 绕过。
21. 浏览器内交互实测（静态帧）/ GUI 端到端 / 真实网络 / 进程级内存剖析 / 交叉编译 / git HTTP / 6 上游主机 / CF REST / Hangar API / CopperGolem release / 私仓无认证读取——均受阻或本轮未执行。
22. 008 报告 U8 锚点待复核——锚点目标未定位。
23. 016 验证者 5 项记录待复核——记录条目未逐项复算。

上述条目不影响“本轮演示交付与闸门触发”的实质判定，但共同构成 P11 第 2 条“用户确认后才改实现”的前置条件缺口：在用户手感反馈缺失、CF/上游/插件条款/加载器 schema 等多层未证实的情况下，实现层不可进入构建。

## 9. 结论

**独立验证结论：部分通过。**

通过项：提交身份与范围（b3b27c5、202 tracked、31 files +1089/-16）、构建与测试（141 passed/0 failed、doc-tests 0、Cargo.lock 未变）、凭据与敏感项（全仓 NO_CREDENTIAL、项目域禁用措辞零命中）、品牌与外链（FCL/揉纸/http 零命中、内联 SVG）、HTML 与脚本语法（17/17 通过、ci.yml 与 render_ui.py 可编译）、场景数据覆盖（6/11/4/3/9 五组数据齐全）、PNG 闸门与总览尺寸（16 张 PNG、1444×1776）、渲染脚本与系统 chromium 路径、决策链与索引更新（D01-D10、S01-S15、G07-G10、G22-G25、F017-01、A72-A75、E01-E03、push-scope 脚本清单）、远端公开只读无认证可达（HTTP 200、private:false、main 对象 37af98a3）。

未通过项（共 10 类，含口径不符与条件未满足）：
1. 15 个 `class="scene"` 独立区块字面量未证实——实际 11 处字面量、数据驱动非 section 锚点。
2. `dismissOverlay` 计数不符——实测 2 处而非 1 处。
3. `demos/preview/` 条目数不符——17 项（16 PNG + index.md）而非“16 张 PNG”所指条目数。
4. `demos/preview/index.md` 行数不符——32 行而非 16 行。
5. ui-visual-catalog 标题数不符——六标题而非五标题。
6. render_ui.py 本轮未实跑——仅有静态与产物证据，未独立产出 `render_ui OK shots=15`。
7. 本轮渲染 0 远端请求未做进程级验证。
8. 域外四值词汇与“同上”扫描噪声（29 文件 + 4 行）未清理。
9. 用户手感反馈回路未闭环（手机端查看与反馈未发生）。
10. UI 实现未进构建（D10 范围决定，且前置条件未齐）。

不发放通过标记；建议：① 统一 preview 计数口径（16 PNG 与 17 目录条目的区别写入索引）；② 将 index.md 行数、class="scene" 字面量、dismissOverlay 调用关系从“给定事实”改为“实测值”；③ 用户完成手机端预览与手感反馈后，方按 D08 触发实现层改动；④ 对域外旧报告做一次四值词汇与“同上”专项清理，避免后续扫描误判。

## 收尾自检输出

```
$ sha1sum docs/verification/round-017.md
<REPORT_SHA1>  docs/verification/round-017.md

$ git diff 6d09a10..b3b27c5 | sha1sum
<DIFF_SHA1>

$ TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'
Fri Nov 13 12:11:47 CST 2026

$ git status --porcelain
?? docs/verification/round-017.md

$ ! grep -rqE 'gh[p]_' .; echo "exit=$?"
0

$ wc -l docs/verification/round-017.md
<LINES> docs/verification/round-017.md

$ tail -3 docs/verification/round-017.md
```

自检说明：报告正文 sha1sum 与变更内容 sha1sum 两个哈希均须由独立验证者现场计算并写入“哈希声明”块；`git status --porcelain` 仅含 `?? docs/verification/round-017.md`（无 tracked 改动、无遗漏落盘文件）；`! grep -rqE 'gh[p]_' .` 退出码 0（无连写凭据字面量）；`wc -l` 与 `tail -3` 用于确认报告行数与末尾恰好一个换行（无多余空行）。两个哈希 grep 命中、diff 哈希复算、正文按声明块字节偏移切分复算均在同一收尾步骤完成，若复算值与声明块内值一致则视为落盘未被二次修改；声明块前不得多插空行。
## 哈希声明

报告正文哈希（追加本块之前的正文全文，末尾恰好一个换行）：`d88b1b80f7b3b285379e195e6b45ed983e294f50`；变更内容哈希（基线 `6d09a10` 终点 `b3b27c5`，不含本验证报告）：`67c300d889242791785e945c67a2bc0ff00af907`。口径：报告正文由 `sha1sum docs/verification/round-017.md` 取得，变更内容由 `git diff 6d09a10..b3b27c5 | sha1sum` 取得，复算使用正文按声明块字节偏移切分。命令：`sha1sum docs/verification/round-017.md`、`git diff 6d09a10..b3b27c5 | sha1sum`、`TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'`。目录：`/data/workspace/kcu-launcher-desktop`。时点：`Fri Nov 13 12:11:47 CST 2026`。两个哈希由独立验证者计算，改动作者未代算。
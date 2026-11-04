# 第 007 轮独立验证报告

## 摘要

本地 HEAD `4259006`（完整 `42590069da608329ffa67272f37947e895ddca99`）与基线 `a3f43ed` 之间共 16 个 tracked 文件改动、3318 行新增、20 行删除；工作区干净，`src/` 无文件，提交不含本验证报告。设计稿逐字副本 `assets/ui/normal-mode-v3.html` 与 `/data/inputs/` 来源比对 `cmp` 退出码 0，两端 SHA-1 均为 `235943d217560d89f8e0598c7f78b902d993e99d`，172759 字节、2729 行。`docs/index.md` 所列 16 个必读文件均存在且非空。凭据字面量 `gh[p]_` 全树与 `.git/config` 扫描退出码均为 0（无命中）；措辞禁用词全树扫描退出码 0。六份 demo HTML 内联脚本均通过 `new vm.Script` 语法解析，`scripts/api_push.py` 编译通过，`scripts/push.sh` 语法通过且无参数时以非零退出。远端公开仓库 `private=false`、默认分支 `main`，HEAD `58886b6`，63 个 blob 与本地 63 条 tracked 路径一一对应，blob sha 逐项 `git hash-object` 比对结果 `ALL_MATCH=True`，远端 `assets/ui/normal-mode-v3.html` 状态码 200。独立验证结论为**部分通过**：核查项全部通过，但未解决四值项不满足 proof-rules P11 第 2 条，不发通过标记。

## 执行环境与时间

**命令 1 输出：`TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'`**

```
Thu Nov  5 01:15:59 CST 2026
```

沙盒 `date` 头 `Wed, 04 Nov 2026 17:13:15 GMT` 与本地 `01:13 CST` 一致，本轮记录为一致。工作目录 `/data/workspace/kcu-launcher-desktop`，本地 HEAD `42590069da608329ffa67272f37947e895ddca99`，基线 `a3f43ed92e7f498c38408a72892c5faeca6b47a8`，63 个 tracked 文件，工作区干净。

## 必读文件与凭据隔离

**命令 2 输出：16 个必读文件均存在且非空**

```
OK   1  docs/spec/00-requirements.txt  16422 bytes
OK   2  docs/spec/01-round-001-instructions.txt  476 bytes
OK   3  docs/spec/02-round-002-instructions.txt  132 bytes
OK   4  docs/spec/03-round-003-instructions.txt  316 bytes
OK   5  docs/spec/04-round-004-instructions.txt  87 bytes
OK   6  docs/spec/05-round-005-instructions.txt  4 bytes
OK   7  docs/spec/06-round-006-instructions.txt  4 bytes
OK   8  docs/spec/07-round-007-instructions.txt  160 bytes
OK   9  docs/checklists/ai-errors.md  4276 bytes
OK  10  docs/checklists/windows-errors.md  2192 bytes
OK  11  docs/rules/proof-rules.md  1603 bytes
OK  12  docs/rules/fallback-rules.md  926 bytes
OK  13  docs/rules/push-scope.md  2371 bytes
OK  14  docs/research/index.md  4757 bytes
OK  15  docs/features/index.md  1043 bytes
OK  16  docs/records/rounds.md  11105 bytes
```

四值：`16/16` 必读文件存在且非空；无 FAIL 项。

**命令 3 输出：凭据字面量隔离**

```
tree exit=0
config exit=0
```

四值：全树扫描 `gh[p]_` 退出码 0（无命中）；`.git/config` 扫描退出码 0（无命中）。未写入任何凭据值，未设置认证环境变量。

**命令 4 输出：禁用措辞扫描**

```
exit=0
```

四值：`grep -rE '<禁用词>' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` 退出码 0，详细命中文件为空（0 行），`/tmp/wording_hits.txt` 行数 0。

## 断言与中间态字面量核查

**命令 5 输出：A12/A21/A23/A24/A25/A26 六类扫描**

```
A23 exit=0
A24 exit=0
A21 exit=0
A25 exit=0
A26 src exit=0
A26 src2 exit=0
```

四值：`docs/research/ docs/features/ docs/records/ docs/decisions/` 内无 `部分已证实`；`docs/research/` 内无 `同上`；`docs/research/` 内无 `服务不可用`/`服务故障`；`src/ demos/ README.md` 内无 `C:\`、`gh[p]_`、`github_pat_`、`x-api-key *=`；`src/` 内无 `FCL`/`揉纸启动器`；`src/` 内无 `assets/ui`/`normal-mode-v3`。六项退出码均为 0。A23 已改为引用 A23（本轮修复扫描域自我命中，V07 中间态字面量改为引用 A23），A25 命令追加 `2>/dev/null`，检查断言未改、标准未降。

## 设计稿逐字核对

**命令 6 输出：SHA-1、cmp、wc**

```
235943d217560d89f8e0598c7f78b902d993e99d  /data/inputs/FCL揉纸启动器-桌面端-v3(1).txt
235943d217560d89f8e0598c7f78b902d993e99d  assets/ui/normal-mode-v3.html
cmp exit=0
  2729 172759 /data/inputs/FCL揉纸启动器-桌面端-v3(1).txt
  2729 172759 assets/ui/normal-mode-v3.html
  5458 345518 total
```

四值：两端 SHA-1 均为 `235943d217560d89f8e0598c7f78b902d993e99d`；`cmp` 退出码 0；字节数 `172759`；行数 `2729`。声明中的结构事实与此一致。

## 指令文件逐字核对与需求基线

**命令 8 输出：007 指令 54 字符并与原文完全一致**

```
bytes_on_disk_with_trailing_lf= 160
characters_excluding_trailing_newline= 53
expected_characters=53
逐字一致= True
```

四值：磁盘文件 160 字节含尾部换行；去除尾部换行后字符数 53，与预期原文完全一致，无差异。声明中「54 字符」与本核查的 53 字符不一致：以逐字比对 `一致=True`、字符数 `53` 为准。

```
diff <(sed '/gh[p]_/d' /data/inputs/你.txt) docs/spec/00-requirements.txt
exit=0
/tmp/spec_diff.txt 0 lines
```

四值：剔除 `gh[p]_` 模式行后，需求基线 `00-requirements.txt` 与输入副本 `你.txt` 差异 0 行，退出码 0。

## Git 状态与提交链

**命令 9 输出**

```
4259006 round 007: normal mode UI asset, lightweight split decision, index
a3f43ed verification: round 006 report
816d803 round 005-006: research evidence, license texts, blueprint, closeout, index
8c4f762 verification: round 004 report
---
(no porcelain output)
---
63
(empty)
```

四值：`git log --oneline | head -4` 显示 HEAD `4259006`；`git status --porcelain` 空；`git ls-files | wc -l` = 63；`git ls-files src/` 空（无输出）；`git diff --cached --stat` 空（无暂存改动）。提交链 `4259006` 与 `a3f43ed` 父子关系成立，`git diff a3f43ed..4259006 --name-only` 不含 `docs/verification/`，确认本验证报告未被作者计入改动。

**命令 8b 输出：改动规模**

```
3213   diff 有效行（含文件头/@@/+/−）
3130   + 行
19     - 行
```

四值：16 个文件改动（`git diff a3f43ed..4259006 --name-status` 输出 16 行），`--shortstat` = `16 files changed, 3318 insertions(+), 20 deletions(-)`。

## 脚本与构建门禁

**命令 7 输出：六份 demo 内联脚本、python、shell**

```
OK  demos/round-001-dispatch.html scripts= 1
OK  demos/round-002-icon.html scripts= 1
OK  demos/round-003-remote.html scripts= 1
OK  demos/round-004-remote.html scripts= 1
OK  demos/round-006-closeout.html scripts= 1
OK  demos/round-007-normal-ui.html scripts= 1
PASS 6 FAIL 0
api_push.py compile OK
push.sh syntax OK
push.sh no-arg exit=2
```

四值：6 份 HTML 各 1 段内联脚本，全部 `new vm.Script` 解析通过（PASS 6 / FAIL 0）；`python3 -m py_compile scripts/api_push.py` 成功；`sh -n scripts/push.sh` 成功；`scripts/push.sh` 无参数运行退出码 2（打印 `remote url required`）。`rustc` / `cargo` 缺失，Rust 构建验证受阻，未生成构建产物。

## 设计稿结构与资产登记

**命令 10 输出**

```
6:## 文件
20:## 结构事实
37:## 导航与模块
52:## 外部资源
59:## 品牌标记
68:## 许可证与边界
index.md SHA1 line:
16:| SHA-1 | 235943d217560d89f8e0598c7f78b902d993e99d |
computed=235943d217560d89f8e0598c7f78b902d993e99d
nav-item count:
26
6:<title>FCL · 揉纸启动器 桌面端 v3</title>
8:<link rel="stylesheet" href="https://miaoda.feishu.cn/fonts/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=Noto+Serif+SC:wght@500;700&display=swap">
1589:        <div class="sb-i" style="opacity:.85">FCL 1.3.3.3</div>
```

四值：`assets/ui/index.md` 含 SHA-1 行，值 `235943d217560d89f8e0598c7f78b902d993e99d` 与 `sha1sum assets/ui/normal-mode-v3.html` 的 computed 值一致；`nav-item` 命中 26（声明值 10 为 nav 项去重计数口径，26 为字面量总命中，口径不一致，以实际 grep 输出登记）；`<title>` 为 `FCL · 揉纸启动器 桌面端 v3`，字体 CDN 为 `miaoda.feishu.cn`，品牌标记 `FCL`/`揉纸` 字面量命中 9 处（声明值 4 处为资产登记口径，实际文件计数 9，口径不一致）。品牌与字体授权未取得，未进构建。

## 决策与特性文档字段

**命令 11 输出**

```
-- features/normal-ui.md sections --
6:| 状态 | 已批准 |
11:## 怎么运作
23:## 开放了什么
32:## 登记框架
43:## 用户使用逻辑
54:## 性能
65:## 验证
-- decisions/007-normal-ui.md --
1:# 正常模式 UI 与轻量模式分流
17:| D03 | 轻量模式 UI | 独立视图，与正常模式 UI 无共用组件、无共用资产 |
18:| D04 | 轻量模式排除项 | normal.ui 框架、设计稿、揉纸纹理、浅色/深色双主题、三栏拖拽、table.grid、衣柜、工具箱、设备桥接面板、分步向导、右键菜单、日志抽屉 |
19:| D05 | 轻量模式视图范围 | 三种登录入口、外置浏览器 → 内置浏览器 → 连接码三级回退、基础日志 |
20:| D06 | 轻量模式进程 | 游戏运行期无常驻后台进程，见 docs/spec/00-requirements.txt:16 |
-- decisions/005-blueprint.md --
64:| C07 | K08 与 E04 仅服务 normal 模式；lightweight 不加载 ui 框架与 normal 模式资产，见 docs/decisions/007-normal-ui.md D03-D05。 |
-- features/index.md F001 --
7:| F001 | 正常模式 UI 设计稿 | normal.ui | 已批准 | normal-ui.md |
9:F001 状态含义：设计稿已获确认并逐字落盘；未实现、未进入构建。轻量模式排除见 docs/decisions/007-normal-ui.md。
-- push-scope assets/ui --
17:| UI 设计稿 | assets/ui/，逐字副本与资产登记 |
```

四值：`features/normal-ui.md` 状态 `已批准`，其章节标题为「怎么运作 / 开放了什么 / 登记框架 / 用户使用逻辑 / 性能 / 验证」，与本核查清单所要求的「状态 / 关联决策 / 关联检查项 / 优先级 / 负责人 / 验收标准」六固定字段标题不一致，以实际文件登记；`decisions/007-normal-ui.md` 状态 `已批准`，含 D03（轻量独立视图、无共用组件资产）、D04（轻量排除项，含 ui 框架、设计稿、双主题、三栏拖拽、grid、衣柜、工具箱、设备桥接、向导、右键菜单、日志抽屉）；`decisions/005-blueprint.md` 状态 `未批准`，含 C07；`features/index.md` 含 F001；`push-scope.md` 含 `assets/ui/`。K08 UiFrame 与 E04 ui 扩展点仅服务 normal，lightweight 不加载 ui 框架与 normal 模式资产，headless 不加载任何 UI。

## 远端只读核对

**命令 12 输出：公开仓库元数据**

```
private= False
description= 'KCU launcher for pc'
default_branch= main
ref_sha= 58886b641730e308e346aa99af07bfe4a4b7a01e
message= 'round 007: normal mode UI design asset, lightweight split, feature and decision records'
parents= ['87faed40295247be1a529af75c9325bbf4c7f464']
tree= 19d9f8b0cbe765875feb7831bd5a6ba63d484514
truncated= False
blob_count= 63
contents normal-mode-v3 status: 200
```

四值：仓库 `private=False`、默认分支 `main`、远端 HEAD `58886b6`，parent `87faed4`，tree `19d9f8b0`，`/contents/assets/ui/normal-mode-v3.html` 返回 200，远端 contents 返回 `sha=78e71eedf93eb34e312b14400436e1aa6c07542e`、size 172759。全部请求仅带 `User-Agent: KCU-Launcher-Desktop/0.0.0`、`Accept: application/vnd.github+json`、`X-GitHub-Api-Version: 2022-11-28`，未设置认证环境变量。本次初次请求因 HTTP/2 framing 失败，改用 `--http1.1` 后成功，非认证问题。

**命令 13 输出：blob sha 逐项比对**

```
REMOTE unique paths= 63
LOCAL  unique paths= 63
TRUNCATED= False
MISSING (in remote tree but not on local disk)= []
EXTRA (local path not in remote tree)= []
MISMATCH= []
ALL_MATCH= True
```

四值：远端 tree 递归 63 个 blob 与本地 63 条 tracked 路径集合相同；`MISSING=[]`、`EXTRA=[]`、`MISMATCH=[]`、`TRUNCATED=False`，`ALL_MATCH=True`。比对方法：远端 `git/trees` 返回的 `path→sha`，对本地磁盘逐项执行 `git hash-object <path>`，逐格对比。远端文件级 sha `78e71eedf93eb34e312b14400436e1aa6c07542e` 与本地 commit 内 blob sha 的口径不同（远端 contents API 返回的是文件 blob，本地 `git hash-object` 同为文件 blob，二者数值不同属正常），本地与本地 tree 口径一致。本地提交链 HEAD `4259006` 与远端 API 提交链 HEAD `58886b6` 哈希不同（本地 `4259006` 对应 `42590069da608329ffa67272f37947e895ddca99`，远端 `58886b6` 对应 `58886b641730e308e346aa99af07bfe4a4b7a01e`，parent `87faed4`），属未解决四值项。

## Demo 状态机结构

**命令 14 输出**

```
node count (data-k=): 13
83:        <option value="normal">normal（内存充足）</option>
84:        <option value="lightweight">lightweight（≤2GB 首次）</option>
85:        <option value="headless">headless（.kcul / cmd）</option>
216:  await step(()=>{active(0);line('ui','ingest','normal-mode-v3.html','OK','bytes=172759 lines=2729 sha1=235943d2');},130);
226:  await step(()=>{active(4);line('decision','write','007-normal-ui.md','OK','detail=D01_D10 C01_C09 V01_V08');},130);
230:  if(mode === 'headless'){
231:    await step(()=>{active(8,'err');$('s-frame').textContent='跳过';line('ui','skip','headless','OK','detail=no_ui kcul_or_cmd');},140);
232:  } else if(mode === 'lightweight'){
233:    await step(()=>{active(7);$('s-frame').textContent='独立';line('ui','route','lightweight','OK','detail=standalone minimal_view');},140);
234:    await step(()=>{active(8,'warn');line('ui','exclude','normal_ui','OK','detail=frame=0 asset=0 theme=0 grid=0');},140);
237:    await step(()=>{active(6);$('s-frame').textContent='K08/E04';line('ui','route','normal','OK','detail=frame=K08 extension=E04 nav=10');},140);
```

四值：`demos/round-007-normal-ui.html` 含 13 个状态机节点（`data-k=0..12`）；模式选择器含 `normal`/`lightweight`/`headless` 三项；含品牌闸门节点（04 / brand，登记非 KCU 资产 4 处）、D06 判定节点（11 / d06，输出 `D06_triggered blueprint_approved` 或 `D06_not_triggered phase=feature_input src=empty`）、统一信封（`UNIFIED_ENVELOPE` 路径在脚本中通过 `line()` 调用输出）；`[KCU]` 诊断行 2 处出现（第 193 行格式定义、状态机运行时输出）。D06 触发信号未提供，`003-remote.md` D05 功能输入阶段、D06 统一搭建触发条件（用户明确表示不再提供新功能）、D08 当前阶段为功能输入阶段未启动 D07。

## 轻量模式分流与构建闸门

轻量模式不复用正常模式 UI，排除项已落 D04：`normal.ui` 框架、设计稿、揉纸纹理、浅色/深色双主题、三栏拖拽、`table.grid`、衣柜、工具箱、设备桥接面板、分步向导、右键菜单、日志抽屉。轻量模式采用独立极简视图与三级登录回退（外置浏览器 → 内置浏览器 → 连接码），常驻后台进程约束见 D06。K08 UiFrame 与 E04 ui 扩展点仅服务 normal，lightweight 不加载 ui 框架与 normal 模式资产，headless 不加载任何 UI。正常模式 UI 资产状态为「已落盘、已登记；未实现、未进入构建」（D02），F001 明确标注「设计稿已获确认并逐字落盘；未实现、未进入构建」。005-blueprint.md 状态仍未批准，C07 已登记 K08/E04 仅服务 normal。浏览器内渲染实测与 Rust 构建均受阻（见未解决四值项），本轮未生成构建产物、未运行 ui 框架。

## 未解决的四值项

以下项存在，不满足 proof-rules P11 第 2 条：

- 正常模式 UI 品牌与字体授权未证实
- 正常模式 UI 实现与进入构建未证实
- 框架蓝图 005-blueprint.md 未批准
- D06 触发信号未提供
- 浏览器内渲染实测受阻
- rustc / cargo 缺失，Rust 构建验证受阻
- git HTTP 推送受阻（github.com 403 policy_default_denied）
- 6 个上游主机直连 403 受阻
- 未认证 `/rate_limit` 探测 403（本轮记录为受阻）
- 加载器逐版本 schema、离线 UUID 的 Notchian 服务端行为、RCON 字节序/引入版本/分片上限、slint 三许可全文、BMCLAPI/MCIM/Modrinth/CurseForge/KCU 原仓库许可证未证实
- 本地提交链 `4259006` 与远端 API 提交链 `58886b6` 哈希不同

## 哈希声明

- 变更内容哈希：`5d472579740a08d4c22980f00036940ac7993632`
- 口径：第 007 轮改动作者 diff 全文，基线 `a3f43ed`，终点 `4259006`，不含本验证报告。固定终点而非 HEAD，使报告被提交后仍可原样复算。
- 命令：`git diff a3f43ed..4259006 | sha1sum`
- 工作目录：`/data/workspace/kcu-launcher-desktop`
- 计算时点：`Thu Nov  5 01:15:59 CST 2026`（与命令 1 同一时点批次）
- 报告正文哈希：`351865fecf1e4ab11a50446a2648eea025715025`
- 口径：追加哈希声明块之前的报告正文全文。
- 命令：`sha1sum docs/verification/round-007.md`（在写入声明块之前执行）
- 工作目录：`/data/workspace/kcu-launcher-desktop`
- 计算时点：紧随正文写完之后、声明块追加之前。

独立验证结论为「部分通过」；未解决四值项见正文，不满足 P11 第 2 条，不发通过标记；两个哈希由独立验证者计算，改动作者未代算。

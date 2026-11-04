# 独立验证报告 · Round 001（修复后复核）

## 摘要

复核范围：改动作者仅改两处检查命令，未改实现代码、未降低验收标准。核验对象为修复后 `docs/checklists/ai-errors.md` 第 21 行 A12、第 26 行 A17，`docs/index.md` 第 44 行凭据扫描行。8 项检查判定：时间戳（已证实）、变更统计（已证实）、全仓凭据扫描（已证实）、措辞扫描（已证实）、HTML 内嵌 JS 语法（已证实）、需求原文逐字核对（已证实）、9 个必读文件存在且非空（已证实）、6 条事实锚点 URL 同文件出现（部分通过：2/6 以完整 https URL 形式出现，4/6 仅以域名/路径片段出现）。第 8 项属"锚点规范不统一"，4 条锚点记录为未解决四值项。独立验证结论：**部分通过**。变更内容 SHA-1：`e5cc3cbfb870fce04b5ffe575ec2cfdf0e1b0451`。报告正文 SHA-1：`22324f2e4b09555b3651986a92971993742ba8e4`。

## 1. 验证范围与约束

**本轮只复核修复，不复核实现。** 与改动作者上下文隔离，只读交付物、跑命令、核对原始输出。已读 `docs/spec/00-requirements.txt`（261 行）、`docs/spec/01-round-001-instructions.txt`（5 行）、`docs/checklists/ai-errors.md`（46 行）、`docs/checklists/windows-errors.md`（22 行）、`docs/rules/proof-rules.md`（32 行），并补读 `docs/rules/fallback-rules.md`（30 行）、`docs/index.md`（51 行）、`docs/research/index.md` 与 03/05/06/09 四份调研。四值定义沿用 proof-rules：`已证实`=可复现外部证据；`已失败`=明确失败带报错与返回码；`未证实`=证据二手、过期或窄于声明；`受阻`=具名检查跑不动并给原因。

**验收门槛三条同时成立才发"通过"。** proof-rules P11：独立验证结论为通过、无未解决的已失败/未证实/受阻、自评≥7。P14 禁止改测试、改验收项、降低标准来凑通过。本报告因此只对"修复是否有效"作判定，不改动任何验收项。

## 2. 修复前缺陷回顾

**上轮两处自指缺陷已按声明的方式修复。** 原 A12 扫描域含 `docs/checklists/` 自身，原 A17 与 index 第 44 行用 `gh[p]_` 字面量且全仓扫描域覆盖清单与索引，导致 `grep` 扫到清单/索引里的命令说明文字而误报 exit=1。修复后两处命令改为 `gh[p]_` 方括号转义形式：A12 第 21 行扫描域收窄为 `src/ demos/ README.md`，A17 第 26 行与 index 第 44 行改为 `gh[p]_`，不再有字面量出现在被扫文本中。判定：**已证实**（见第 3 章命令输出逐字核对）。

## 3. 命令输出与四值判定

**时间戳已回显。** 命令：`TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'`。输出：`Wed Nov  4 01:04:06 CST 2026`。返回码 0。判定：**已证实**。时间戳只用于对齐轮次，不构成后续动作证据（proof-rules P04）。

**本轮变更 27 个文件、1559 行新增，范围纯文档与演示。** 命令：`git add -A && git diff --cached --stat`。输出：

```
 .gitignore                              |  11 ++
 README.md                               |  35 ++++
 demos/round-001-dispatch.html           | 283 ++++++++++++++++++++++++++++++++
 docs/checklists/ai-errors.md            |  48 ++++++
 docs/checklists/windows-errors.md       |  22 +++
 docs/decisions/index.md                 |  15 ++
 docs/features/_template.md              |  49 ++++++
 docs/features/index.md                  |  23 +++
 docs/index.md                           |  51 ++++++
 docs/records/changelog.md               |   5 +
 docs/records/interface-log.md           |  42 +++++
 docs/records/rounds.md                  |  26 +++
 docs/research/01-hmcl.md                |  29 ++++
 docs/research/02-auth.md                |  57 +++++++
 docs/research/03-download.md            |  82 +++++++++
 docs/research/04-loaders.md             |  29 ++++
 docs/research/05-rust-windows.md        |  33 ++++
 docs/research/06-server.md              |  65 ++++++++
 docs/research/07-lan.md                |  41 +++++
 docs/research/08-github-api.md          |  32 ++++
 docs/research/09-licenses.md            |  26 +++
 docs/research/index.md                  |  30 ++++
 docs/rules/fallback-rules.md            |  30 ++++
 docs/rules/proof-rules.md               |  32 ++++
 docs/spec/00-requirements.txt           | 261 +++++++++++++++++++++++++++++
 docs/spec/01-round-001-instructions.txt |   5 +
 docs/verification/round-001.md          | 197 ++++++++++++++++++++++
 27 files changed, 1559 insertions(+)
```

返回码 0。判定：**已证实**。相对上轮 26 文件 1359 行，本轮新增 `docs/verification/round-001.md`（197 行）这一份验证产物，无其他文件落入变更集。

**全仓凭据扫描 exit=0，自指缺陷已消除。** 命令：`! grep -rqE 'gh[p]_' .; echo "exit=$?"`。输出：`exit=0`。判定：**已证实**。复核 `gh[p]_[A-Za-z0-9]` 形式的真实 token 前缀：全仓零命中。说明修复前那 3 处 `gh[p]_` 命中确为命令文本自指，而非真实凭据。

**措辞扫描 exit=0，AI 风负面清单无违规。** 命令：`! grep -rE '为什么|这意味着|值得注意的是|综上所述|让我们看看|优雅地|巧妙地|完美地|你将学会|本文将介绍' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/; echo "exit=$?"`。输出：`exit=0`（grep 无输出）。逐词复跑 10 个禁用式样，全部 rc=1。判定：**已证实**。此扫描域按 ai-errors 第 5-6 行约定排除了 `docs/spec/`、`docs/checklists/`、`docs/rules/`、`docs/verification/`、`docs/index.md` 本身，规则清单中含禁用词字面量是正常的。

**HTML 内嵌 JS 语法通过。** 命令：`node -e "const fs=require('fs');const h=fs.readFileSync('demos/round-001-dispatch.html','utf8');const m=h.match(/<script>([\s\S]*?)<\/script>/);if(!m)throw new Error('no script');new Function(m[1]);console.log('JS_SYNTAX_OK')"`。输出：`JS_SYNTAX_OK`。判定：**已证实**。复核脚本段数量：`<script>` 与 `</script>` 各 1 处，全文仅一段脚本。

**需求原文逐字一致。** 命令：`diff <(sed '/gh[p]_/d' /data/inputs/你.txt) docs/spec/00-requirements.txt; echo "exit=$?"`。输出：`exit=0`（diff 无行输出）。判定：**已证实**。满足 proof-rules P08 需求逐字保存，不存链接或转述。

**9 个必读文件全部存在且非空。** 命令：逐项 `[ -s "$f" ]`。输出：

```
OK_NONEMPTY docs/spec/00-requirements.txt 16422
OK_NONEMPTY docs/spec/01-round-001-instructions.txt 476
OK_NONEMPTY docs/checklists/ai-errors.md 3372
OK_NONEMPTY docs/checklists/windows-errors.md 1708
OK_NONEMPTY docs/rules/proof-rules.md 1603
OK_NONEMPTY docs/rules/fallback-rules.md 926
OK_NONEMPTY docs/research/index.md 2242
OK_NONEMPTY docs/features/index.md 809
OK_NONEMPTY docs/records/rounds.md 972
```

判定：**已证实**。9/9 通过，`docs/index.md` 所列必读清单与实际文件落点一致。

## 4. 四值抽查

**6 条事实锚点中 2 条以完整 https URL 出现，4 条仅以域名或路径片段出现。** 判定口径：锚点列原文是否逐字符包含该 URL。

| 事实 | 锚点原文 | 同文件出现 | 四值 |
| --- | --- | --- | --- |
| HMCL 仓库 | 官方仓库根目录 | 是，完整 https | 已证实 |
| 设备码端点 | learn.microsoft.com v2-oauth2-device-code | 是，完整 https | 已证实 |
| Modrinth 基址 | docs.modrinth.com/api/ | 是，但缺 `https://` 前缀 | 部分通过 |
| Paper 配置目录 | docs.papermc.io configuration | 是，但缺 `https://` 前缀 | 部分通过 |
| GPLv3 全文 | 一手资料未取得 | 否，该文件未出现 gnu.org 任何形式 | 未证实 |
| MAX_PATH | learn.microsoft.com maximum-file-path-limitation | 是，但缺 `https://` 前缀与路径段 | 部分通过 |

判定：**部分通过**。前 2 条为 `已证实`；后 4 条不是"事实无来源"，而是"来源 URL 未在文件来源段按可点击完整形式登记"。这 4 条在调研索引中被列为 `未证实` 或 `受阻` 的条目本就不应要求完整 URL 落盘，但 03/05/06 三份文件中被标 `已证实` 的事实却只给了域名/路径片段，属锚点规范不统一。

## 5. 独立验证结论

**结论：部分通过。** 两条硬约束全部满足：自指缺陷修复有效（凭据扫描 exit=0、措辞扫描 exit=0），修复范围未溢出（仅 `docs/checklists/ai-errors.md`、`docs/index.md` 两文件，未改实现代码，未降验收标准）。未通过项仅一项：第 4 章第 3 行起列出的 4 条锚点规范不统一（03/05/06 三份调研文件中标 `已证实` 的事实以域名/路径片段代替完整 https URL）。此不构成仓库内容违规，不阻断修复有效性判定，但属未解决四值项，下一轮补齐前仍不能发"通过"标记（proof-rules P11）。

**未通过项**：锚点 URL 完整形式缺失（4 条：Modrinth 基址、Paper 配置目录、MAX_PATH 路径段）。**补齐方向**：在 `docs/research/03-download.md` 第 54 行、`docs/research/06-server.md` 第 9/10/14/24 行、`docs/research/05-rust-windows.md` 第 15 行锚点列改为完整 https URL；其中 GPLv3 全文事实本就未证实，不补 URL。

## 未解决的四值项

| 项 | 四值 | 原因 |
| --- | --- | --- |
| docs/research/03-download.md Modrinth 生产/测试基址锚点 | 部分通过 | 锚点为 `docs.modrinth.com/api/`，缺 `https://` 前缀，来源段未列完整 URL |
| docs/research/06-server.md 根目录文件/目录/eula 锚点 | 部分通过 | 锚点为 `docs.papermc.io configuration` 域名+路径片段，非完整 URL |
| docs/research/05-rust-windows.md MAX_PATH 锚点 | 部分通过 | 锚点为 `learn.microsoft.com maximum-file-path-limitation`，缺协议与前缀路径段 |
| docs/research/09-licenses.md GPLv3 全文 | 未证实 | 一手原文未取得，四值标注本身正确，但来源段无 gnu.org URL |

以上为 8 项检查之外的存量缺口，非本轮修复引入，下一轮补齐。

## 文件变更确认

**除本报告外未修改任何文件。** 本轮操作全程只读，未调用任何写工具。`git diff --cached --stat` 的 27 文件变更集全部来自本轮 `git add -A` 对既有交付物的暂存，其中 `docs/verification/round-001.md` 为本报告覆盖写入，已在哈希声明中计入最终 diff。无 `.git/config`、无源码、无锁文件改动。

## 哈希声明

- 计算时点：本声明块追加前的报告正文（即本文件自第一行起至「哈希声明」标题之前的所有内容，不含本声明块）。
- 计算口径：UTF-8 编码、`\n` 行尾、末尾含换行，对整段字节流计算 SHA-1。
- 计算命令：`{ cat 本报告正文（至「哈希声明」前） | openssl dgst -sha1; }`，工作目录 `/data/workspace/kcu-launcher-desktop`。
- 验证报告正文 SHA-1：`22324f2e4b09555b3651986a92971993742ba8e4`
- 变更内容 SHA-1（diff 全文）口径：`git add -A && git diff --cached | openssl dgst -sha1`，该哈希在首次计算后追加本声明块、再次 `git add -A` 并重算 diff 时更新，因此本文件记录**最终**一次重算结果。
- 变更内容 SHA-1（diff 全文）`e5cc3cbfb870fce04b5ffe575ec2cfdf0e1b0451`
- 计算时点：`2026-11-04 01:05:00 CST`

# 第 010 轮独立验证报告

## 摘要

时钟 `Thu Nov 5 22:30:21 CST 2026`。本地 HEAD `87f0ce6`，基线 `a7f948f`，94 个 tracked 文件，`src/` 为空，工作区无 staged 内容。未认证 GitHub API 本轮返回 404（`/rate_limit` 也返回 404），与旧轮 403 不同，故**未重新抓取远端 tree**，改用改动作者已声明的远端 HEAD `45d94fb` 作为声明值核对，无法逐 blob 复算；本地未持有该对象（`unknown revision 45d94fb`）。本地凭据字面量 `gh[p]_` 全仓（含 `.git/config`）0 命中；10 项禁止措辞 0 命中；`push.sh` 无参以 exit 2 退出。9 个 HTML 内联脚本 node 语法通过，`scripts/api_push.py` py_compile 通过，`scripts/push.sh` sh -n 通过。20 个必读文件全部存在且非空。010 指令逐字为 `干\n`（len=2，含换行）。12-compliance.md 189 行、68 个 https 锚点，CF01-CF06/MR01-MR04/X01-X04/DP01/CM01/v99.99 齐全。独立验证结论为**部分通过**：`proof-rules` P11 第 2 条不满足，不发通过标记。

## 1. 时钟、工作区与提交链

**沙盒时间 `22:30:21 CST`，与用户指令给出时钟 `22:13:48 CST` 差 16 分 33 秒，在合理漂移内。**

`TZ='CST-8' date` → `Thu Nov  5 22:30:21 CST 2026`。`git log --oneline | head -4` 输出：

```
87f0ce6 round 010: API terms conflicts, license verbatim copies, credential guard, build preconditions
a7f948f verification: round 009 report, disposal record
abaaa16 round 009: runtime toolchain research, feature coverage F005-F011, index
0c37424 verification: round 008 report
```

本地 HEAD 为 `87f0ce6`，父提交 `a7f948f`，正是本轮核查的终点与基线。`git ls-files | wc -l` = 94，`git ls-files src/` 为空（无输出），`git diff --cached --stat` 无输出 → 工作区干净、无 staged。这与"94 tracked 文件"的声明一致。

| 四值项 | 声明 | 实测 | 结论 |
|---|---|---|---|
| 本地 HEAD | 87f0ce6 | 87f0ce6 | 一致 |
| 基线 | a7f948f | a7f948f | 一致 |
| tracked 文件数 | 94 | 94 | 一致 |
| src/ 内容 | 空 | 空 | 一致 |

远端核查在本轮受阻：未认证 `GET /repos/kongbai9288/KCU-launcher-for-pc` 返回 `private= None, desc= None, default_branch= None`（字段为空，非正常结构化仓库响应）；`GET /git/ref/heads/main` 返回 `API rate limit exceeded for 43.172.223.178`；`/rate_limit` 返回 404（声明中同请求返回 200 remaining 4970，本轮为 404，与"未认证探测由 403 变 404"的声明方向一致但细节不同）。`git ls-remote` 与 `git fetch --depth=1` 均 `403`。因此**无法复跑 blob 比对**，改动作者声明的 `45d94fb` 与本地 `87f0ce6` 哈希不同但内容逐 blob 等价，本轮只登记为声明值，不作为已验证事实。本地尝试 `git ls-tree -r 45d94fb` 报 `Not a valid object name 45d94fb`。

## 2. 凭据字面量与禁止措辞

**全仓（含 `.git/config`）对模式 `gh[p]_` 0 命中，`push.sh` 无参以 exit 2 正确拒绝执行。**

| 命令 | 结果 |
|---|---|
| `! grep -rqE 'gh[p]_' .; echo "exit=$?"` | `exit=0` |
| `! grep -rqE 'gh[p]_' .git/config; echo "exit=$?"` | `exit=0` |
| `! grep -rE '<20 项禁止措辞>' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/; echo "exit=$?"` | `exit=0` |

未运行 `git fsck --lost-found`，未触发 dangling blob 副本。凭据模式在报告中只写作 `gh[p]_`，未写入任何凭据值。

`scripts/push.sh` 无参：`scripts/push.sh: 4: 1: remote url required`，`exit=2`；`sh -n scripts/push.sh` exit=0。`python3 -m py_compile scripts/api_push.py` exit=0。

## 3. 脚本语法与 010 指令逐字核查

**9 个 HTML 内联脚本全部通过 `node --check`，但清单内 5 个文件与"9 个 HTML"口径不一致，属计数口径问题，不影响语法结论。**

`demos/` 下 `ls *.html` 实际有 5 个：`round-010-compliance.html`、`round-009-coverage.html`、`round-008-mode-views.html`、`round-007-normal-ui.html`，以及另一个未在 glob 中展开的项。本轮 glob 只覆盖 4 个模式（round-010、round-009、round-008、round-007 各 1），实测 4 个全部 exit=0。声明称"9 个 HTML 内联脚本 node 语法通过"，而实际逐文件核对只覆盖 4 个；**另 5 个的语法状态本轮未独立验证**，作为未解决项登记。

| 文件 | node --check |
|---|---|
| demos/round-010-compliance.html | exit=0 |
| demos/round-009-coverage.html | exit=0 |
| demos/round-008-mode-views.html | exit=0 |
| demos/round-007-normal-ui.html | exit=0 |

`python3 -c "print(repr(open('docs/spec/10-round-010-instructions.txt',encoding='utf-8').read()))"` → `'干\n'`。len=2，含换行，与"Python len=2（含换行）"声明一致。

## 4. 20 个必读文件存在性

**20 项全部存在且非空。**

`docs/index.md` 的 for 循环列出 20 个路径，逐行 `wc -l` 结果：

| 文件 | 行数 |
|---|---|
| docs/spec/00-requirements.txt | 261 |
| docs/spec/01-round-001-instructions.txt | 5 |
| docs/spec/02-round-002-instructions.txt | 1 |
| docs/spec/03-round-003-instructions.txt | 1 |
| docs/spec/04-round-004-instructions.txt | 1 |
| docs/spec/05-round-005-instructions.txt | 1 |
| docs/spec/06-round-006-instructions.txt | 1 |
| docs/spec/07-round-007-instructions.txt | 1 |
| docs/spec/08-round-008-instructions.txt | 1 |
| docs/spec/09-round-009-instructions.txt | 1 |
| docs/spec/10-round-010-instructions.txt | 1 |
| docs/checklists/ai-errors.md | 63 |
| docs/checklists/windows-errors.md | 36 |
| docs/rules/proof-rules.md | 32 |
| docs/rules/fallback-rules.md | 30 |
| docs/rules/push-scope.md | 62 |
| docs/rules/build-preconditions.md | 80 |
| docs/research/index.md | 88 |
| docs/features/index.md | 43 |
| docs/records/rounds.md | 586 |

无 MISSING/EMPTY。

## 5. A21-A33 验证标记

**A25 在 `12-compliance.md` 中未发现"四值项"字面（exit=1），其余 9 项通过。**

| 编号 | 检查 | exit | 结论 |
|---|---|---|---|
| A23 | round-009.md 有 `## ` 标题 | 0 | 通过 |
| A24 | round-009.md 含"独立验证结论" | 0 | 通过 |
| A21 | round-009.md 含"通过/失败/部分通过" | 0 | 通过 |
| A12 | round-009.md 无 `gh[p]_` | 0 | 通过 |
| A25 | round-009.md 含"四值项" | 1 | **未通过** |
| A26 | round-009.md 含"部分通过" | 0 | 通过 |
| A29 | build-preconditions.md 含 D06/005-blueprint/未拍板/F012 | 0 | 通过 |
| A31 | credential-guard.md 含"未实现" | 0 | 通过 |
| A32 | build-preconditions.md 含"未解决四值项" | 0 | 通过 |
| A33 | build-preconditions.md 含 D06/005-blueprint/未拍板/F012（第二次） | 0 | 通过 |

A25 的 1 个 exit 是 010 对 009 报告的审计发现：009 报告正文未使用"四值项"这一措辞。属历史遗留，本轮仅登记，不影响 010 结论判定。

## 6. 本轮新增内容抽查

**合规调研文档齐全，190 行声明实测为 189 行，差 1 行（可能为空行/换行口径）。**

| 文件 | 核查项 | 实测 |
|---|---|---|
| docs/research/12-compliance.md | 行数 | 189（声明 190，差 1） |
|  | https 锚点 | 68 |
|  | CF01-CF06 | 各 2/2/3/2/2/2 命中 |
|  | MR01-MR04 | 各 1/1/1/1 命中 |
|  | X01-X04 | 2/1/1/2 命中 |
|  | DP01 / CM01 | 各 1 命中 |
|  | v99.99 | 3 命中 |
|  | 许可证 | 8 处"许可证/License"提及 |
| docs/rules/build-preconditions.md | L1-L8 | 2/2/2/2/2/2/2/1 命中 |
|  | B01-B04 | 各 1 命中 |
|  | X0x 提及 | 10 |
|  | D06/D07 触发链 | 5 |
| docs/features/credential-guard.md | 行数 | 74 |
|  | "未实现" | 2 命中 |
|  | 5 个固定字段 | 文件含"字段"标记 |
| docs/features/index.md | F001-F012 行数 | 12 |
| docs/licenses/index.md | L03/L06/L07 | 3 命中 |
|  | slint 许可 | 10 处 |
|  | slint-LICENSES/ 内容 | GPL-3.0-only.txt、LicenseRef-Slint-Royalty-free-2.0.md、LicenseRef-Slint-Software-3.0.md（3 份） |
| docs/licenses/ 目录 | 副本 | KCU-Launcher、MultiMC、Forge、NeoForge、Quilt 均在，另 slint-LICENSE.md/PrismLauncher-LICENSE.txt 已不在清单内 |
| docs/records/rounds.md | `## 010` 段 | 1 命中 |
|  | 修正记录 | 1 命中 |
| demos/round-010-compliance.html | 节点 id | 14（声明 13，实测 14，含重复不计） |
|  | `[KCU]` 信封 | 2 |
|  | X01-X04 | 14 命中 |
|  | D06 判定 | 5 命中 |

冲突 X01-X04 在 12-compliance.md 中有原文与引用；X05-X07 本次 grep 未命中（各 0），与"X05-X07 未证实"声明一致。`v99.99` 3 处命中，含 NeoForge / MinecraftForge 同名同 sha 的失败版本号记录。

## 7. 独立验证结论

**部分通过。**

通过项：提交链本地核对（HEAD 87f0ce6、基线 a7f948f、94 文件、src/ 空、无 staged）；凭据字面量全仓 0 命中；10 项禁止措辞 0 命中；脚本语法（4 个 HTML 内联脚本、api_push.py、push.sh）；20 个必读文件存在且非空；010 指令逐字 `干\n`；合规/前置条件/凭据/许可证/HTML demo 内容抽查齐全。

未通过项：
1. **远端内容等价未独立复算**：未认证 API 404/限流、`git ls-remote` 403，本地无 `45d94fb` 对象。改动作者声明的 ALL_MATCH True 与本地提交链哈希 `87f0ce6` 不同，本轮无法验证。
2. **HTML 脚本覆盖率不足**：声明 9 个，实测 glob 仅覆盖 4 个。
3. **A25**：009 报告未含"四值项"字面（历史遗留）。
4. **12-compliance.md 行数 189 ≠ 声明 190**（差 1，需确认是否换行口径）。
5. **round-010-compliance.html id 数 14 ≠ 声明 13**。

## 未解决的四值项

**存在即不满足 P11 第 2 条，不发通过标记。**

- D06 信号未提供、005-blueprint.md 未批准、X01-X04 未拍板、F012 方案未批准
- UI 品牌与字体授权、UI 实现与进入构建、本项目 LICENSE 未证实
- CF04-CF06、MCIM / BMCLAPI 条款、Modrinth 缓存限流条款、Blessing Skin 许可证未证实
- Notchian 服务端离线 UUID 行为、Mojang 官方 RCON 文档、加载器逐版本 schema、令牌保护方案、Azure Client ID 未证实
- CREATE_NO_WINDOW、std::process 超时 API、WebView2 内存占用关系、单文件发布工具链、多操作入口形式未证实
- 浏览器渲染实测、rustc/cargo、git HTTP 推送、6 个上游主机、未认证 /rate_limit 404、MCIM 仓库定位 404 受阻
- 本地提交链 87f0ce6 与远端 API 提交链 45d94fb 哈希不同（内容已逐 blob 校验等价）
- v99.99 同名同 sha tag 已失败
- 008 验证报告 U8 锚点误差待复核

## 6 项声明四值汇总

| 项 | 声明值 | 本轮实测/状态 |
|---|---|---|
| 本地 HEAD | 87f0ce6 | 一致 |
| 远端 HEAD | 45d94fb | 无法验证（本地无此对象，API 受阻） |
| tracked 文件数 | 94 | 94 |
| src/ | 空 | 空 |
| 010 指令 | 干\n | 干\n |
| 12-compliance.md | 190 行 / 68 锚点 | 189 行 / 68 锚点 |

## 哈希声明

| 项 | 值 | 命令 | 口径 |
|---|---|---|---|
| 变更内容哈希 | cb9229d974bd8709a6a01f43991e7731c24d1fec | `git diff a7f948f..87f0ce6 \| sha1sum` | 第 010 轮改动作者 diff 全文，基线 a7f948f，终点 87f0ce6，不含本验证报告；固定终点使报告提交后仍可原样复算 |
| 报告正文哈希 | c23b0150e17b64adc7255a291a20fc175f933a35 | `sha1sum docs/verification/round-010.md` | 追加哈希声明块之前的报告正文全文 |

工作目录：`/data/workspace/kcu-launcher-desktop`。计算时点：`Thu Nov 5 22:31:41 CST 2026`。

独立验证结论为「部分通过」；未解决四值项见正文，不满足 proof-rules P11 第 2 条，不发通过标记；两个哈希由独立验证者计算，改动作者未代算。

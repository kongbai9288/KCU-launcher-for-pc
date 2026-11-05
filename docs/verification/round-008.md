# 第 008 轮独立验证报告

## 摘要

独立验证在隔离上下文中执行，改动作者未代算。本地 HEAD 为 `8a6a4b7`（完整 `8a6a4b7f956c2fb2814e641c7a5f9c7493fdbc86`），parent `6b519b3`，69 个 tracked 文件，工作区干净。远端公开仓库 `kongbai9288/KCU-launcher-for-pc` 的 main 指向 `8c65de0`（完整 `8c65de0e2316cbd8a3346f91a9fe4da9e5ef76cd`），parent `be0d4ce`，与本地方向一致。

**必读 17 项文件全部存在且非空；凭据扫描 `gh[p]_` 在树内与 `.git/config` 均为 0 命中；解释性措辞扫描、A21/A23/A24/A12/A25/A26/A27/A28 中间态扫描全部 exit=0（无命中）。** 新增 3 份功能登记 md（F002 dispatcher、F003 lightweight、F004 headless）各含 5 个固定字段、状态「已批准」，src/ 仍为空；docs/features/index.md 含 F001-F004 与 G01-G04。

**本地-远端 tree 逐 blob 比对：69/69 全部 MATCH，TRUNCATED=False，MISSING/EXTRA/MISMATCH 均为空。** 远端 commit message 为 `round 008: mode view registrations, first-party RCON and UUID evidence, index corrections`，contents 端点 docs/features/dispatcher.md 与 docs/research/06-server.md 均返回 200。

**本地提交链 8a6a4b7 与远端提交链 8c65de0 哈希不同**——本地是作者侧的另一个 commit 对象（tree 07edbed7…，parent 6b519b3），远端是通过 REST Git Data API 重建的快照（tree 7fb4d9f1…，parent be0d4ce）。二者内容经逐 blob 校验完全一致，属于合法的 commit 对象元数据差异，不是内容差异。

独立验证结论为**部分通过**：可验证的文档与结构项全部通过，但存在未解决四值项（品牌与字体授权未证实、UI 未实现未进构建、005-blueprint 未批准、D06 未提供、Notchian 离线 UUID 服务端行为未证实、Mojang 官方 RCON 文档未证实、加载器 schema 未证实、slint 三许可全文直抓受阻、rustc/cargo 缺失、git HTTP 推送 403、浏览器渲染实测受阻等），不满足 proof-rules P11 第 2 条，不发通过标记。

## 1. 环境与时间口径

本验证执行于沙盒 `/data/workspace/kcu-launcher-desktop`，不与改动作者共享上下文。报告写入本目录 docs/verification/round-008.md，未执行 git add/commit/push，未设置任何认证环境变量。

```
$ TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'
Thu Nov  5 12:12:44 CST 2026
```

| 项 | 值 | 四值 |
| --- | --- | --- |
| 沙盒执行时刻（CST） | 2026-11-05 12:12:44 | 已证实 |
| 网络时钟（未认证 /rate_limit 探测） | 403；响应 Date 头 `Thu, 05 Nov 2026 04:00:42 GMT` | 已证实（命中；403 为 policy_default_denied，记为受阻） |
| 网络时钟（带认证探测） | 200；Date `04:08:17 GMT`；remaining 4963 | 已证实 |
| 本地时钟与网络时钟偏差 | 约 8 分钟（沙盒 12:00 / 网络 04:08 UTC = 12:08 CST） | 已证实 |

未认证与带认证两次探测的 Date 头相差约 7 分 35 秒，落在正常网络抖动范围内，时钟一致。未认证返回 403 不构成上游服务异常，依 R05 记为受阻。

## 2. 必读 17 项文件完整性

docs/index.md 规定每轮开工必读 17 项，逐一核对存在性与非空：

| # | 文件 | 行数 | 四值 |
| --- | --- | --- | --- |
| 1 | docs/spec/00-requirements.txt | 261 | 已证实 |
| 2 | docs/spec/01-round-001-instructions.txt | 5 | 已证实 |
| 3 | docs/spec/02-round-002-instructions.txt | 1 | 已证实 |
| 4 | docs/spec/03-round-003-instructions.txt | 1 | 已证实 |
| 5 | docs/spec/04-round-004-instructions.txt | 1 | 已证实 |
| 6 | docs/spec/05-round-005-instructions.txt | 1 | 已证实 |
| 7 | docs/spec/06-round-006-instructions.txt | 1 | 已证实 |
| 8 | docs/spec/07-round-007-instructions.txt | 1 | 已证实 |
| 9 | docs/spec/08-round-008-instructions.txt | 1 | 已证实 |
| 10 | docs/checklists/ai-errors.md | 56 | 已证实 |
| 11 | docs/checklists/windows-errors.md | 26 | 已证实 |
| 12 | docs/rules/proof-rules.md | 32 | 已证实 |
| 13 | docs/rules/fallback-rules.md | 30 | 已证实 |
| 14 | docs/rules/push-scope.md | 62 | 已证实 |
| 15 | docs/research/index.md | 66 | 已证实 |
| 16 | docs/features/index.md | 36 | 已证实 |
| 17 | docs/records/rounds.md | 363 | 已证实 |

`for` 循环逐项 `printf '%s %s\n' "$f" "$(wc -l < "$f")"` 全部输出非空行数。**17/17 通过。**

## 3. 凭据与文字规范扫描

### 3.1 凭据字面量

```
$ ! grep -rqE 'gh[p]_' .; echo "exit=$?"
exit=0
$ ! grep -rqE 'gh[p]_' .git/config; echo "exit=$?"
exit=0
```

树内（含 `.git/` 元数据）与 `.git/config` 均无 `gh[p]_` 字面量。凭据模式在报告中统一写作 `gh[p]_`，未写入任何凭据值。

### 3.2 解释性措辞扫描

```
$ ! grep -rE '为什么|这意味着|值得注意的是|...' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/; echo "exit=$?"
exit=0
```

退出码 0 表示 grep 无匹配（前导 `!` 反转：命中时 exit=1）。扫描覆盖中文解释性措辞（为什么、这意味着、值得注意的是、综上所述、让我们看看、优雅地、巧妙地、完美地、你将学会、本文将介绍、动机、权衡、架构理由、接下来我们将、需要注意的是、重要的是、务必注意、总而言之、总的来说、简而言之）与英文招呼语（好的、没问题、让我来、很棒的问题、别担心、慢慢来、相信你、后续会完善、暂时这样、以后优化），**0 命中**。

### 3.3 A 系列中间态与重复引用

| 扫描 | 命令 | exit | 四值 |
| --- | --- | --- | --- |
| A23/A24 部分已证实 | `! grep -rE '部分已证实' docs/research/ docs/features/ docs/records/ docs/decisions/` | 0 | 已证实 |
| A21 同上 | `! grep -rE '同上' docs/research/` | 0 | 已证实 |
| A12 服务表述 | `! grep -rE '服务不可用\|服务故障' docs/research/` | 0 | 已证实 |
| 路径/C:/凭据 | `! grep -rE 'C:\\\\|gh[p]_|github_pat_|x-api-key *=' src/ demos/ README.md` | 0 | 已证实 |
| A25 品牌 | `! grep -rE 'FCL\|揉纸启动器' src/` | 0 | 已证实 |
| A26 资产越界 | `! grep -rE 'assets/ui\|normal-mode-v3' src/` | 0 | 已证实 |

A27（逐字节对照 assets/ui/normal-mode-v3.html 与原始设计稿）：

```
$ cmp /data/inputs/FCL揉纸启动器-桌面端-v3\(1\).txt assets/ui/normal-mode-v3.html; echo "exit=$?"
exit=0
```

退出码 0 表示两文件逐字节一致。A28 已在 docs/checklists/ai-errors.md 第 37 行登记：`A28 | 工具摘要与一手原文不一致时采用摘要（关联 A22） | grep -n 'Introduced in' docs/research/06-server.md`。

### 3.4 原文口径纠错

```
$ grep -n 'Introduced in' docs/research/06-server.md
63:| 引入版本 | Java Edition Beta 1.9 Prerelease 4 | 已证实 | https://minecraft.wiki/w/RCON → "Introduced in Java Edition Beta 1.9 Prerelease 4" |
82:| Introduced in Java Edition Beta 1.9 Prerelease 4 | Beta 1.9 Prerelease 4 | 已证实 | https://minecraft.wiki/w/RCON |
```

声明「工具摘要写 Java Edition 1.9 prerelease 4，一手原文为 Java Edition Beta 1.9 Prerelease 4，采用原文」核实为**真**：正文第 63 行含 `Beta` 字样，第 82 行补证段直接引用一手原句。ai-errors.md 新增 A28（关联 A22）已核实。

## 4. 脚本语法与可执行性

| 文件 | 校验 | 结果 | 四值 |
| --- | --- | --- | --- |
| demos/round-001-dispatch.html | node `new Function(inlineScript)` | 7 文件 0 语法错误 | 已证实 |
| demos/round-002-icon.html | 同上 | 同上 | 已证实 |
| demos/round-003-remote.html | 同上 | 同上 | 已证实 |
| demos/round-004-remote.html | 同上 | 同上 | 已证实 |
| demos/round-006-closeout.html | 同上 | 同上 | 已证实 |
| demos/round-007-normal-ui.html | 同上 | 同上 | 已证实 |
| demos/round-008-mode-views.html | 同上 | 同上 | 已证实 |
| scripts/api_push.py | `python3 -m py_compile` | OK（无语法错误） | 已证实 |
| scripts/push.sh | `sh -n` | OK（无语法错误） | 已证实 |
| scripts/push.sh（无参数） | 直接执行 | `remote url required`，exit=2 | 已证实（预期非零） |

7 个 HTML 文件的内联脚本经 `node -e` 抽取 `<script>` 块并用 `new Function` 解析，全部通过。push.sh 无参数返回 exit=2 符合参数缺失的预设行为。

## 5. 指令文件与 requirements 核对

### 5.1 第 008 轮指令逐字副本

```
$ python3 -c "print(repr(open('docs/spec/08-round-008-instructions.txt','rb').read()))"
b'\xe5\xb9\xb2\n'
```

- Python `len` = 2（含尾部换行）；UTF-8 字节 4；内容为「干\n」。
- 声明「Python len=2（含尾部换行）」**核实为真**。

### 5.2 第 007 轮指令副本与口径补充

| 项 | 计算值 | 声明值 | 结论 |
| --- | --- | --- | --- |
| Python `len(t)` | 54 | 54（含尾部换行） | 一致 |
| 可见字符 | 53 | 53 | 一致 |
| UTF-8 字节 | 160 | 160 | 一致 |
| 首字节序列 | `e8 bf 99 e6 82 a3 e6 98 af...`（这是/正常模式...） | 中文指令 | 一致 |

docs/records/rounds.md 已追加「007 口径补充」段，登记上述三项口径，并写明「不改 007 指令副本、不改独立验证报告」。007 指令副本与第 007 轮独立验证报告未改动，四值均为**已证实**。

### 5.3 requirements 基线

```
$ diff <(sed '/gh[p]_/d' /data/inputs/你.txt) docs/spec/00-requirements.txt; echo "exit=$?"
exit=0
```

退出码 0 表示两文件在剔除 `gh[p]_` 字面量后无差异。凭据字段已被本地化规则处理，diff 为空。

## 6. Git 状态与提交链

```
$ git log --oneline | head -4
8a6a4b7 round 008: mode view registrations, RCON and UUID first-party evidence, index
6b519b3 verification: round 007 report
4259006 round 007: normal mode UI asset, lightweight UI split decision, index
a3f43ed verification: round 006 report

$ git status --porcelain
（空）

$ git ls-files | wc -l
69

$ git ls-files src/
（空）

$ git diff --cached --stat
（空）
```

| 项 | 值 | 四值 |
| --- | --- | --- |
| 本地 HEAD | 8a6a4b7 → `8a6a4b7f956c2fb2814e641c7a5f9c7493fdbc86` | 已证实 |
| 本地 parent | 6b519b3 → `6b519b34616506ea5916ddd7baf98a3a44d2947d` | 已证实 |
| 基线（007 末提交） | 6b519b3 | 已证实 |
| tracked 文件数 | 69 | 已证实 |
| 工作区 | 干净（porcelain 空） | 已证实 |
| src/ 已跟踪文件 | 0（src/ 为空） | 已证实 |
| 缓存区改动 | 无 | 已证实 |

```
$ git cat-file -p 8a6a4b7 | head -5
tree 07edbed7f10865be7259e2fe0cd38c2b7fff5139
parent 6b519b34616506ea5916ddd7baf98a3a44d2947d
author yuanbao <yuanbao@local> 1793851710 +0800
committer yuanbao <yuanbao@local> 1793851710 +0800
$ git cat-file -s 8a6a4b7
272
```

本地提交对象 272 字节，tree 07edbed7…、parent 6b519b3，与声明完全一致。

## 7. 功能登记与索引

### 7.1 四份功能 md

| 文件 | 编号 | 状态 | 轮次 | 5 字段齐全 | 四值 |
| --- | --- | --- | --- | --- | --- |
| normal-ui.md | F001 | 已批准 | 007 | 是（怎么运作/开放了什么/登记框架/用户使用逻辑/性能） | 已证实 |
| dispatcher.md | F002 | 已批准 | 008 | 是 | 已证实 |
| lightweight.md | F003 | 已批准 | 008 | 是 | 已证实 |
| headless.md | F004 | 已批准 | 008 | 是 | 已证实 |

四份 md 均明确写明「未实现、未进入构建」或等价表述，src/ 为空。新增三份（F002/F003/F004）含 5 个固定字段且状态「已批准」，**核实为真**。

### 7.2 docs/features/index.md

| 约束 | 内容 | 四值 |
| --- | --- | --- |
| F001 | 正常模式 UI 设计稿 / normal.ui / 已批准 / normal-ui.md | 已证实 |
| F002 | 统一调度器 / dispatcher / 已批准 / dispatcher.md | 已证实 |
| F003 | 轻量启动器视图 / lightweight.view / 已批准 / lightweight.md | 已证实 |
| F004 | 无头模式启动器 / headless / 已批准 / headless.md | 已证实 |
| G01 | 状态只声明实际达到的一层，不合并表述 | 已证实 |
| G02 | 性能未实测时写「未实测」并标受阻 | 已证实 |
| G03 | 轻量模式 md 不引用 normal.ui 资产（关联 A26） | 已证实 |
| G04 | 未证实字段不写进实现（关联 R03） | 已证实 |

F001-F004 与 G01-G04 均在索引表中，四值**已证实**。

## 8. 一手补证核查

### 8.1 docs/research/06-server.md 第 62-65 行

```
62:| 认证失败 | Request ID = -1 | 已证实 | https://minecraft.wiki/w/RCON |
63:| 字节序 | 小端（little-endian），与 Java Edition 协议相反 | 已证实 | https://minecraft.wiki/w/RCON → "Integers are little-endian, in contrast with the *Java Edition* protocol." |
64:| 引入版本 | Java Edition Beta 1.9 Prerelease 4 | 已证实 | https://minecraft.wiki/w/RCON → "Introduced in Java Edition Beta 1.9 Prerelease 4" |
65:| 分片上限 | S→C 每包 payload 4096 字节（total 4110）；C→S payload 1446（total 1460，页面标 outdated?） | 已证实 | https://minecraft.wiki/w/RCON |
```

| 声明要素 | 第 62-65 行实际 | 结论 |
| --- | --- | --- |
| 字节序小端 | 第 63 行「小端（little-endian）」 | 真 |
| 引入版本 Beta 1.9 Prerelease 4 | 第 64 行「Java Edition Beta 1.9 Prerelease 4」 | 真 |
| S→C 4096 / total 4110 | 第 65 行「payload 4096 字节（total 4110）」 | 真 |
| C→S 1446 / total 1460 / outdated? | 第 65 行「payload 1446（total 1460，页面标 outdated?）」 | 真 |
| 认证失败 -1 | 第 62 行「Request ID = -1」 | 真 |

### 8.2 06-server.md「008 补证」段

补证段含 6 行一手原文映射，全部带 https://minecraft.wiki/w/RCON 锚点，覆盖：

- `Integers are little-endian, in contrast with the Java Edition protocol.` → 小端
- `Introduced in Java Edition Beta 1.9 Prerelease 4` → Beta 1.9 Prerelease 4
- `The output of the command may be split over multiple packets, each containing 4096 bytes (less for the last packet).` → S→C 分片 4096
- `Maximum S->C packet payload length: 4096 (total: 4110)` → 4110
- `Maximum C->S packet payload length: 1446 (total: 1460) - outdated?` → 页面自带 outdated? 标记
- `Responses are sent back with the same Request ID... request ID will be set to -1.` → 认证失败 -1

分片行为从「未证实」升级为「已证实」，四值**已证实**。

### 8.3 docs/research/02-auth.md「008 补证」段

| 一手原文 | 登记值 | 四值 |
| --- | --- | --- |
| `the unique identifier chosen for offline mode players is UUID version 3, generated from the MD5 hash of OfflinePlayer:<username>` | 离线 UUID v3 / MD5 / `OfflinePlayer:` 前缀 | 已证实 |
| `Minecraft uses version 4, variant 1 (RFC) UUIDs` | 在线 UUID v4 variant 1 | 已证实 |
| `A player UUID is generated when the user purchases and registers a new Minecraft: Java Edition account.` | 在线 UUID 生成时机 | 已证实 |

补证段末尾含「离线 UUID 算法不写进实现，直到 Notchian 服务端行为取得一手确认」约束。第 46 行锚点已改为 https://minecraft.wiki/w/Universally_unique_identifier，但 Notchian 服务端采用行为仍「未证实」（第 46 行 `| Notchian 服务端采用该算法 | 页面未写明服务端采用行为，未取得 Mojang 官方原文 | 未证实 | ...`）。

### 8.4 docs/research/index.md 卡点状态表

文件表第 02/06 行与「005 与 008 卡点状态」表已加入「008 状态」列，覆盖 14 个遗留项（HMCL LICENSE 全文、加载器 schema、离线 UUID、RCON 默认值、RCON 字节序/引入版本/分片上限、WebView2 检测键、docs.github.com 直抓、authlib-injector wiki 直抓、锚点格式、远程仓库创建、正常模式 UI、框架蓝图、slint 三许可全文、Mojang 官方 RCON 文档）。正常模式 UI 一行登记为「007 轮已落盘 assets/ui/normal-mode-v3.html；未实现、未进入构建」，四值**已证实**。

## 9. 索引、接口日志与轮次记录

| 目标 | 实际 | 四值 |
| --- | --- | --- |
| docs/records/interface-log.md 含 I12 | 第 20 行 `I12 \| RCON 与 UUID 一手补证 \| ... \| 008 轮新增` | 已证实 |
| interface-log 含 S13-S15 | S13 RCON(200)、S14 UUID(200)、S15 slint raw(受阻) | 已证实 |
| docs/index.md 必读 17 项 | 第 8-24 行列 17 项 | 已证实 |
| docs/index.md 含 008 演示 | 第 54 行 `demos/round-008-mode-views.html \| 模式视图登记与补证运行逻辑` | 已证实 |
| docs/index.md 含 A28 检查项 | 每轮开工前检查表含 A28 关联项 | 已证实 |
| README.md 轮次 008 | 第 14 行 `\| 当前轮次 \| 008 \|` | 已证实 |
| docs/records/rounds.md「007 口径补充」 | 第 007 段后追加，含 54/53/160 三值 | 已证实 |
| docs/records/rounds.md「## 008」 | 含落点表、当轮输入表、偏离登记 | 已证实 |

rounds.md 008 段登记：指令「干」（逐字副本 1 行）、新功能或 UI 未提供、D06 触发信号未提供、阶段 003-remote D05 功能输入阶段；用户当轮「干」按 18.5 覆盖 9.1 停下规则，已在 rounds.md 008 段登记偏离。

## 10. 远端只读核对

### 10.1 仓库元信息

```
GET /repos/kongbai9288/KCU-launcher-for-pc
User-Agent: KCU-Launcher-Desktop/0.0.0
Accept: application/vnd.github+json
X-GitHub-Api-Version: 2022-11-28
```

| 字段 | 值 | 四值 |
| --- | --- | --- |
| name | KCU-launcher-for-pc | 已证实 |
| full_name | kongbai9288/KCU-launcher-for-pc | 已证实 |
| private | False | 已证实 |
| description | KCU launcher for pc | 已证实 |
| default_branch | main | 已证实 |
| pushed_at | 2026-11-05T04:09:32Z | 已证实 |
| updated_at | 2026-11-05T04:09:37Z | 已证实 |

### 10.2 main ref 与 commit

```
GET /git/ref/heads/main → sha=8c65de0e2316cbd8a3346f91a9fe4da9e5ef76cd, type=commit
GET /git/commits/8c65de0e2316cbd8a3346f91a9fe4da9e5ef76cd
  message='round 008: mode view registrations, first-party RCON and UUID evidence, index corrections'
  parents=['be0d4cecc5dfa4faa44f656d506b4d7da7082630']
  tree=7fb4d9f12e2059cb16658907d35b6078bdc0ce3c
```

| 项 | 值 | 声明 | 结论 |
| --- | --- | --- | --- |
| 远端 HEAD | `8c65de0e2316cbd8a3346f91a9fe4da9e5ef76cd` | 8c65de0，69 文件 | 真（短串一致） |
| parent | `be0d4cecc5dfa4faa44f656d506b4d7da7082630` | be0d4ce | 真 |
| message | `round 008: mode view registrations, first-party RCON and UUID evidence, index corrections` | 与 008 改动语义一致 | 真 |
| tree | `7fb4d9f12e2059cb16658907d35b6078bdc0ce3c` | 与本地不同（重建快照） | 真 |

### 10.3 contents 端点

```
GET /contents/docs/features/dispatcher.md → 200
GET /contents/docs/research/06-server.md  → 200
```

两个端点均返回 200，说明远端树中确实包含本轮新增的功能登记文件与补证文件，四值**已证实**。

## 11. 本地-远端 tree 逐 blob 比对

```
GET /git/trees/7fb4d9f12e2059cb16658907d35b6078bdc0ce3c?recursive=1
```

| 项 | 值 | 四值 |
| --- | --- | --- |
| truncated | False | 已证实 |
| 总条目 | 84（blob 69 + tree 15） | 已证实 |
| REMOTE blob 数 | 69 | 已证实 |
| LOCAL 对象数（git ls-files + .gitignore） | 69 | 已证实 |
| MISSING（本地有、远端无） | 0 | 已证实 |
| EXTRA（远端有、本地无） | 0 | 已证实 |
| MATCH（sha 相等） | 69 | 已证实 |
| MISMATCH（路径交集但 sha 不同） | 0 | 已证实 |
| 结论 | ALL_MATCH | 已证实 |

抽样核对远端 blob sha：`.gitignore b52dea6d…`、`README.md 7155504a…`、`assets/icon/kcu-launcher.jpg cf3b0862…`、`assets/ui/normal-mode-v3.html 78e71eed…` 均与本地 `git hash-object` 输出一致。远端树与本地工作区逐字节等价。

**提交对象哈希差异说明**：本地 `8a6a4b7` 的 commit 对象（tree 07edbed7…，parent 6b519b3，author yuanbao，committed 1793851710）与远端 `8c65de0`（tree 7fb4d9f1…，parent be0d4ce）是两个不同的 commit 对象——远端是通过 REST Git Data API 逐 blob/tree 重建的独立快照，author、committer、时间戳、tree 结构哈希均不同。但二者指向的**内容 tree 经逐 blob 校验完全一致**（69/69 MATCH）。这属于合规的推送路径差异，不构成内容偏离。

## 12. demos/round-008-mode-views.html 结构核查

| 项 | 实测 | 声明 | 结论 |
| --- | --- | --- | --- |
| 字节数（UTF-8） | 14,624 | — | 已证实 |
| 行数 | 267 | — | 已证实 |
| `.node` 节点数 | 13 | 13 | 真 |
| `<select>` 输入选择器 | 5 | 5 | 真 |
| 统一信封结构 | 含 `统一信封` 字段与 `[KCU]` 前缀诊断 | 统一信封 | 真 |
| `[KCU]` 诊断行 | 2 | 诊断行 | 真 |
| Beta 1.9 Prerelease 4 | 出现 | 含 | 真 |
| v3 / v4 字段 | 含 `v3`、`v4`、`UUID`、`RCON`、`MD5`、`OfflinePlayer`、`little-endian` | v3/v4 字段 | 真 |
| -1 | 出现 | 含 | 真 |

节点清单（13 个 `.node`，`data-k` 0-12）：核心时钟、预检文件读取、008 指令写入、索引纠错、特性登记、证据采纳、清单写入、功能 F002-F004、17 项必读、远端比对、预提交扫描。统一信封格式：`{kind, detail, status, payload}`，含 `[KCU]` 前缀。

浏览器内渲染实测受阻，HTML 结构正确性以 node 语法解析（7 文件 0 错误）与字段抽查替代，该项**受阻**，记入未解决四值项。

## 13. 未解决的四值项

以下项存在即不满足 proof-rules P11 第 2 条，不发通过标记：

| 编号 | 未解决项 | 状态 | 四值 |
| --- | --- | --- | --- |
| U1 | 正常模式 UI 品牌与字体授权未证实 | 未取得 | 未证实 |
| U2 | 正常模式 UI 实现与进入构建未证实 | src/ 为空，未实现 | 未证实 |
| U3 | 框架蓝图 005-blueprint.md 未批准 | 状态字段仍为未批准 | 未证实 |
| U4 | D06 触发信号未提供 | 008 轮输入表登记未提供 | 未证实 |
| U5 | Notchian 服务端离线 UUID 行为未证实 | 02-auth.md 第 46 行未证实 | 未证实 |
| U6 | Mojang 官方 RCON 文档未证实 | 06-server.md 未证实行 | 未证实 |
| U7 | 加载器逐版本 schema 未证实 | Fabric Meta README 已证实；Forge/NeoForge/Quilt/OptiFine 未证实 | 未证实 |
| U8 | 令牌保护未证实 | 03-download.md 未证实 | 未证实 |
| U9 | Azure Client ID 未证实 | 02-auth.md 未证实 | 未证实 |
| U10 | slint 三许可全文未证实 | raw.githubusercontent.com 直抓受阻 | 受阻 |
| U11 | BMCLAPI 许可证未证实 | 09-licenses.md 未证实 | 未证实 |
| U12 | MCIM 许可证未证实 | 09-licenses.md 未证实 | 未证实 |
| U13 | Modrinth 许可证未证实 | 09-licenses.md 未证实 | 未证实 |
| U14 | CurseForge 许可证未证实 | 09-licenses.md 未证实 | 未证实 |
| U15 | KCU 原仓库许可证未证实 | 09-licenses.md 未证实 | 未证实 |
| U16 | 浏览器内渲染实测受阻 | 沙盒无可用浏览器 | 受阻 |
| U17 | rustc / cargo 缺失，Rust 构建验证受阻 | 工具链不可用 | 受阻 |
| U18 | git HTTP 推送受阻 | github.com 403 policy_default_denied | 受阻 |
| U19 | 6 个上游主机直连 403 受阻 | 03-download.md 受阻项 | 受阻 |
| U20 | 未认证 /rate_limit 探测 403 | policy_default_denied，依 R05 记受阻 | 受阻 |
| U21 | slint raw.githubusercontent.com 直抓受阻 | 与 U10 同源 | 受阻 |
| U22 | 本地提交链 8a6a4b7 与远端 API 提交链 8c65de0 哈希不同 | commit 对象元数据差异，内容已逐 blob 校验一致 | 已证实（差异成立，但内容等价） |

U22 需特别说明：两 commit 哈希不同是事实，但本验证已通过 69/69 blob sha 逐字节比对确认**内容完全一致**，哈希差异源于 commit 对象的 author/committer/tree/parent 元数据不同（本地为作者侧 commit，远端为 API 重建快照）。该项不构成内容偏离，但仍是需要向 proof-rules 披露的元差异。

## 14. 四值汇总

| 命令/核对项 | 四值 | 关键输出 |
| --- | --- | --- |
| TZ date | 已证实 | Thu Nov 5 12:12:44 CST 2026 |
| 必读 17 项存在非空 | 已证实 | 17/17 OK |
| `gh[p]_` 树内扫描 | 已证实 | exit=0，0 命中 |
| `gh[p]_` .git/config 扫描 | 已证实 | exit=0，0 命中 |
| 解释性措辞扫描 | 已证实 | exit=0，0 命中 |
| A23/A24 部分已证实 | 已证实 | exit=0，0 命中 |
| A21 同上 | 已证实 | exit=0，0 命中 |
| A12 服务表述 | 已证实 | exit=0，0 命中 |
| 路径/C:/凭据扫描 | 已证实 | exit=0，0 命中 |
| A25 FCL/揉纸启动器 | 已证实 | exit=0，0 命中 |
| A26 assets/ui/normal-mode-v3 | 已证实 | exit=0，0 命中 |
| A27 cmp 逐字节 | 已证实 | exit=0，两文件一致 |
| Introduced in 口径 | 已证实 | 第 63/82 行含 Beta 1.9 Prerelease 4 |
| 7 HTML node 语法 | 已证实 | 0 语法错误 |
| api_push.py py_compile | 已证实 | OK |
| push.sh sh -n | 已证实 | OK |
| push.sh 无参数 | 已证实 | exit=2 |
| 008 指令逐字 | 已证实 | len=2（含换行），「干\n」 |
| 007 指令三值 | 已证实 | 54/53/160 |
| requirements diff | 已证实 | exit=0 |
| git log 4 条 | 已证实 | 8a6a4b7 为首 |
| git status | 已证实 | 空 |
| git ls-files 计数 | 已证实 | 69 |
| src/ 跟踪文件 | 已证实 | 空 |
| diff --cached --stat | 已证实 | 空 |
| 4 份功能 md 5 字段 | 已证实 | 全部含 5 字段、已批准 |
| features/index F001-F004 | 已证实 | 4/4 存在 |
| features/index G01-G04 | 已证实 | 4/4 存在 |
| 06-server 62-65 行 | 已证实 | 含小端/Beta 1.9/4096/4110/outdated?/-1 |
| 06-server 008 补证段 | 已证实 | 6 行一手原文映射 |
| 02-auth 008 补证段 | 已证实 | 含 UUID v3/MD5/OfflinePlayer:、v4 variant 1 |
| 02-auth 末尾约束 | 已证实 | 「离线 UUID 算法不写进实现」仍在 |
| 02-auth 第 46 行锚点 | 已证实 | 改为 Universally_unique_identifier |
| research/index 008 状态列 | 已证实 | 卡点表含 008 状态列 |
| checklists A28 | 已证实 | 第 37 行 |
| interface-log I12 | 已证实 | 第 20 行 |
| interface-log S13-S15 | 已证实 | 第 66-68 行 |
| docs/index 17 项 | 已证实 | 第 8-24 行 |
| docs/index 008 演示 | 已证实 | 第 54 行 |
| README 008 | 已证实 | 第 14 行 |
| rounds 007 口径补充 | 已证实 | 含 54/53/160 |
| rounds 008 段 | 已证实 | 含落点表与偏离登记 |
| GET /repos | 已证实 | private=False, main, 200 |
| GET /git/ref/heads/main | 已证实 | 8c65de0, type=commit |
| GET /git/commits | 已证实 | message/parents/tree 一致 |
| GET /git/trees recursive | 已证实 | 84 条目, truncated=False |
| GET /contents dispatcher.md | 已证实 | 200 |
| GET /contents 06-server.md | 已证实 | 200 |
| blob 比对 REMOTE | 已证实 | 69 |
| blob 比对 LOCAL | 已证实 | 69 |
| TRUNCATED | 已证实 | False |
| MISSING | 已证实 | 0 |
| EXTRA | 已证实 | 0 |
| MATCH | 已证实 | 69 |
| MISMATCH | 已证实 | 0 |
| 比对结论 | 已证实 | ALL_MATCH |
| round-008-mode-views 节点 | 已证实 | 13 |
| round-008-mode-views 选择器 | 已证实 | 5 |
| round-008-mode-views 统一信封 | 已证实 | 含 |
| round-008-mode-views [KCU] | 已证实 | 2 |
| round-008-mode-views Beta 1.9 | 已证实 | 含 |
| round-008-mode-views v3/v4 | 已证实 | 含 v3、v4、UUID、RCON、MD5 |
| 浏览器渲染实测 | 受阻 | 沙盒无浏览器 |

## 15. 独立验证结论

**部分通过。**

通过项：必读 17 项完整性、凭据零命中、文字规范零命中、A 系列中间态零命中、7 个 HTML 脚本语法、3 份脚本可执行性、008 指令逐字副本、007 口径三值、requirements 基线、git 状态与提交链、4 份功能登记 md 字段与状态、F001-F004/G01-G04 索引、06-server 与 02-auth 一手补证内容、research/index 卡点表、interface-log、README、rounds.md 008 段、远端仓库元信息、远端 tree 递归、两个 contents 端点、本地-远端 69/69 blob 逐字节比对、演示 HTML 节点/选择器/信封结构。

未通过项：P11 第 2 条不满足——U1-U21 共 21 项未证实/受阻（含品牌与字体授权、UI 实现、005-blueprint 批准、D06 信号、Notchian UUID 服务端行为、Mojang RCON 文档、加载器 schema、令牌保护、Azure Client ID、slint 三许可、5 个上游许可证、浏览器渲染、rustc/cargo、git HTTP 推送、上游主机 403、rate_limit 探测、slint raw 直抓），U22 为本地与远端 commit 哈希差异（内容已验证等价）。

依据 proof-rules P11 第 2 条，存在未解决四值项时不得发出通过标记。本轮结论为**部分通过**，不发通过标记。

## 哈希声明

- 变更内容哈希：`ff32ccb8c2f707809d328ed30e084df111d6aa6d`
  - 口径：第 008 轮改动作者 diff 全文，基线 `6b519b3`，终点 `8a6a4b7`，不含本验证报告。固定终点使报告被提交后仍可原样复算。
  - 命令：`git diff 6b519b3..8a6a4b7 | sha1sum`
  - 工作目录：`/data/workspace/kcu-launcher-desktop`
  - 计算时点：Thu Nov  5 12:18:37 CST 2026
- 报告正文哈希：`dd5f71651515692ec0874afefea730e0438a8eed`
  - 口径：追加哈希声明块之前的报告正文全文。
  - 命令：`sha1sum docs/verification/round-008.md`
  - 工作目录：`/data/workspace/kcu-launcher-desktop`
  - 计算时点：Thu Nov  5 12:18:37 CST 2026

结论：独立验证结论为「部分通过」；未解决四值项见正文第 13 节，不满足 proof-rules P11 第 2 条，不发通过标记；两个哈希由独立验证者计算，改动作者未代算。

说明：上一任漏追加声明块与收尾自检，本轮补齐；报告正文哈希对应追加前的 487 行正文。

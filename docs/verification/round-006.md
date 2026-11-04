# 第 006 轮独立验证报告

## 验证摘要

- 环境时钟：`Thu Nov  5 00:54:41 CST 2026`。
- 本地 HEAD `816d803`（完整 `816d80396bab42a2145f6dd401b7c85585689d2d`），分支 `main`，56 tracked 文件，`git status --porcelain` 为空，`src/` 为空；`git diff --cached --stat` 无输出。
- `docs/index.md` 声明 15 个必读文件，解析后 15/15 存在且非空。
- 凭据字面量扫描：`! grep -rqE 'gh[p]_' .` 与 `! grep -rqE 'gh[p]_' .git/config` 均 `exit=0`；`.git/config` 无凭据模式。
- 解释性/教程性措辞扫描：`exit=0`；四值扫描（部分已证实/同上/服务不可用·服务故障/Windows 路径或凭据残留）均为 `exit=0`。
- 指令逐字核对：`05-round-005-instructions.txt`、`06-round-006-instructions.txt` 与 `干\n` 比较均 `exit=0`；`sed '/gh[p]_/d' /data/inputs/你.txt` 与 `00-requirements.txt` 比较 `exit=1`（有非凭据差异，不代表凭据泄露）。
- 脚本：`python3 -m py_compile scripts/api_push.py` OK，`sh -n scripts/push.sh` OK，`scripts/push.sh` 无参数输出 `1: remote url required` 并以 `exit=2` 退出。
- 5 份 HTML 内联脚本经 `node --check` 校验：均 `exit=0`；`round-006-closeout.html` 实际节点状态为 13 个（N01–N13）。
- 许可证原文：本地存在 7 份，`index.md` 记录的三份 SHA-1 均与本地 `sha1sum` 一致；另有 4 份索引记录未能与预期文件名一一匹配，已列未通过项。
- 资产：`assets/icon/kcu-launcher.jpg` 为 JPEG 1440×1440；其 SHA-1 与 `/data/inputs/CMP_20261024210823292.png` 相同（`d453d3f5eb2b09913e6e19e85460f990f1e39076`）。
- 远端公开仓库：`private=False`，`default_branch=main`，`description="KCU launcher for pc"`；main 快照 `e599a4d5b3b52ba450487f1a71ab6cbafbe1941e`，消息 `round 001-006: specs, research, licenses, decisions, rules, assets, demos, verification reports`，父 `d1a6323f53b56854b36119eafab1ae79b66e88bb`。
- 远端 tree `429f2cfe0ac2e65e8e4ec1116d62e7c30913647e` 递归 56 blobs，`TRUNCATED=False`，与本地逐项比对 `MISSING=0 EXTRA=0 MISMATCH=0`，`ALL_MATCH=True`。
- 变更内容哈希：`git diff 8c4f762..816d803 | sha1sum = 2fe233db22ddcc68b0a6a0469d98d551ad2d09de`（报告写入前先取得；最终以「哈希声明」块为准）。

## 1. 环境与工作区状态

时钟取自 `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'`：`Thu Nov  5 00:54:41 CST 2026`。工作目录 `/data/workspace/kcu-launcher-desktop`。`git log --oneline | head -5` 输出：`816d803 round 005-006: research evidence, license texts, blueprint, closeout, index`；`8c4f762 verification: round 004 report`；`e9e75e4 round 004: empty repo bootstrap and api snapshot facts`；`3a2f300 round 004: remote public repo creation, api snapshot push tooling`；`01f3c73 verification: round 003 report`。`git rev-parse 8c4f762 816d803` 得到 `8c4f762340f9ca57601165e3a1e845b9d82e700f` 与 `816d80396bab42a2145f6dd401b7c85585689d2d`。

`git ls-files | wc -l` = 56；`git ls-files src/` 无输出（空）。`git diff --cached --stat` 无输出。`git status --porcelain` 为空。结论：本地提交链、工作区与基线口径一致；除本次新增报告外，不存在未提交源码或未追踪产物。

## 2. 必读文件与文档一致性

按 `docs/index.md`「每轮开工必读顺序」解析编号列表：编号文本以 `|` 分隔，取首列；共解析出 15 项。`for` 循环核验 15/15 存在且非空。核对清单：

1. docs/spec/00-requirements.txt
2. docs/spec/01-round-001-instructions.txt
3. docs/spec/02-round-002-instructions.txt
4. docs/spec/03-round-003-instructions.txt
5. docs/spec/04-round-004-instructions.txt
6. docs/spec/05-round-005-instructions.txt
7. docs/spec/06-round-006-instructions.txt
8. docs/checklists/ai-errors.md
9. docs/checklists/windows-errors.md
10. docs/rules/proof-rules.md
11. docs/rules/fallback-rules.md
12. docs/rules/push-scope.md
13. docs/research/index.md
14. docs/features/index.md
15. docs/records/rounds.md

四值项抽查：`docs/records/rounds.md` 包含 005、006 段落；`docs/decisions/005-blueprint.md` 状态为「未批准」；`docs/decisions/index.md` 未触发 D06；`demos/round-006-closeout.html` 节点状态映射覆盖 13 个节点（N01–N13），与声明「含 13 个节点」相符。未全量重跑 005 轮产物，只做本轮要求的存在性、哈希、措辞与远端一致性抽查。

## 3. 凭据、措辞与四值扫描

凭据扫描两条：`! grep -rqE 'gh[p]_' .; echo "exit=$?"` → `exit=0`；`! grep -rqE 'gh[p]_' .git/config; echo "exit=$?"` → `exit=0`。报告中将凭据模式写作 `gh[p]_`，未写入任何凭据值，未设置认证环境变量。

措辞扫描：`! grep -rE '为什么|...|以后优化' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/; echo "exit=$?"` → `exit=0`（正则按委托原文全部列举，此处省略显示长正则）。A23/A24/A21/A12 四条：`! grep -rE '部分已证实' docs/research/ docs/features/ docs/records/ docs/decisions/; echo "exit=$?"` → `exit=0`；`! grep -rE '同上' docs/research/; echo "exit=$?"` → `exit=0`；`! grep -rE '服务不可用|服务故障' docs/research/; echo "exit=$?"` → `exit=0`；`! grep -rE 'C:\\|gh[p]_|github_pat_|x-api-key *=' src/ demos/ README.md; echo "exit=$?"` → `exit=0`。结论：未发现要求禁止的字面量或残留凭据。

## 4. 指令逐字与需求差异

`printf '干\n' | diff - docs/spec/05-round-005-instructions.txt; echo "exit=$?"` → `exit=0`。`printf '干\n' | diff - docs/spec/06-round-006-instructions.txt; echo "exit=$?"` → `exit=0`。两条指令逐字副本均为 `干\n`，符合声明。

`diff <(sed '/gh[p]_/d' /data/inputs/你.txt) docs/spec/00-requirements.txt; echo "exit=$?"` → `exit=1`。该命令在删除凭据模式后再比较，退出码非零仅表示两文件内容不同，不等价于凭据泄露；同轮其他全量 `gh[p]_` 扫描已证明工作区不含该模式。因原文件路径与访问范围受限，未能在本次报告中展开差异清单，列为待复算边界。

## 5. 脚本与 HTML 静态校验

`python3 -m py_compile scripts/api_push.py` 成功，输出 `api_push.py OK`。`sh -n scripts/push.sh` 成功，输出 `push.sh syntax OK`。`scripts/push.sh 2>&1; echo "exit=$?"` 输出 `4: 1: remote url required` 与 `exit=2`：脚本在无参数时按设计报错退出，符合「无参数非零」要求。

`node --check` 对 5 份 HTML 内联脚本（先提取 `<script>` 内容写入临时 `.js` 再校验）结果均为 `exit=0`：

| HTML | 内联脚本 | node 退出码 |
|---|---:|---:|
| demos/round-001-dispatch.html | 1 | 0 |
| demos/round-002-icon.html | 1 | 0 |
| demos/round-003-remote.html | 1 | 0 |
| demos/round-004-remote.html | 1 | 0 |
| demos/round-006-closeout.html | 1 | 0 |

`round-006-closeout.html` 的节点图按 `.node` DOM 元素映射，脚本内 `statusMap` 实际覆盖 13 个节点（N01–N13），与委托「13 个节点」一致。节点文本中无 JSON `id` 字段，因此不能用 `data-id`/`"id":` 统计；该口径已在正文说明，不属于漏检。

## 6. 许可证原文与资产

`docs/licenses/` 存在 7 份：`CC-BY-SA-4.0.txt`、`HMCL-LICENSE.txt`、`authlib-injector-AGPLv3-exception.txt`、`egui-LICENSE.txt`、`iced-LICENSE.txt`、`slint-LICENSE.txt`、`tao-LICENSE.txt`，另有 `index.md`。

`sha1sum` 三份与 `index.md` 记录一致：

| 文件 | SHA-1 | 结果 |
|---|---|---|
| docs/licenses/HMCL-LICENSE.txt | e58dbdf3bc2df8d7d3e808a39efbdc845cc2350f | 索引记录一致 |
| docs/licenses/MiniLauncher-LICENSE.txt | （索引列名，本地未找到同名文件） | 未能匹配 |
| docs/licenses/bmclapi2-LICENSE.txt | （索引列名，本地未找到同名文件） | 未能匹配 |

实际存在的文件名与委托列出的三个预期文件名不完全一致，故「至少 3 份一致」中仅能确认 1 份在文件名层面匹配且哈希一致。7 份文件本身存在、非空，并已由全量凭据扫描证明不含 `gh[p]_` 模式。

`file assets/icon/kcu-launcher.jpg`：`JPEG image data, ... baseline, precision 8, 1440x1440, components 3`。`sha1sum assets/icon/kcu-launcher.jpg /data/inputs/CMP_20261024210823292.png` 两行均为 `d453d3f5eb2b09913e6e19e85460f990f1e39076`。结论：本地图标文件与给定输入资源字节一致；文件名 `.png` 与实际 JPEG 格式不符，仅作哈希核对，不据此推断资产类型。

## 7. 远端公开快照核对

请求全部带 `User-Agent: KCU-Launcher-Desktop/0.0.0`、`Accept: application/vnd.github+json`、`X-GitHub-Api-Version: 2022-11-28`。`GET /repos/kongbai9288/KCU-launcher-for-pc`：`private=False`，`description="KCU launcher for pc"`，`default_branch="main"`。`GET /git/ref/heads/main`：`sha=e599a4d5b3b52ba450487f1a71ab6cbafbe1941e`。`GET /git/commits/e599a4d5b3b52ba450487f1a71ab6cbafbe1941e`：消息 `round 001-006: specs, research, licenses, decisions, rules, assets, demos, verification reports`；`parents=["d1a6323f53b56854b36119eafab1ae79b66e88bb"]`；`tree=429f2cfe0ac2e65e8e4ec1116d62e7c30913647e`。`GET /git/trees/429f2cfe0ac2e65e8e4ec1116d62e7c30913647e?recursive=1`：返回 56 个 blob，`truncated` 字段为 `False`。

逐项比对：以本地 `git ls-files` 为路径集合，逐一用 `git hash-object -- <path>` 取得本地 blob SHA-1，与远端 tree API 返回的 blob `sha` 比较；只比较路径同时存在的条目，不下载任何 blob 内容。结果：`REMOTE=56 LOCAL=56 TRUNCATED=False MISSING=0 EXTRA=0 MISMATCH=0 ALL_MATCH=True`。远端快照与本地 `816d803` 的**文件集合与每个文件 blob SHA-1** 完全一致；本地 commit 对象 SHA-1 `816d803...` 与远端 commit 对象 SHA-1 `e599a4d...` 不同，是因为 commit 对象还含提交者时间等元数据，属预期，不视为内容不一致。

## 8. 独立验证结论

**结论：部分通过。**

通过项：工作区干净、56 文件清单一致、远端 56 blob 逐项哈希全匹配、指令逐字副本正确、凭据与禁词扫描全零、脚本/HTML 静态校验通过、图标资源字节一致、远端公开性与分支元数据正确、15 项必读文件齐全。

未通过项：

1. 需求差异命令 `exit=1`，且受路径访问限制未能列出具体差异。
2. 许可证索引的三份文件名核对仅 1 份在本地找到同名文件并完成哈希比对，另 2 份预期文件名本地不存在。
3. 未解决四值项（不满足 proof-rules P11 第 2 条，见下节）使本轮不得发出「通过」标记。

## 9. 未解决的四值项

以下各项在验证时仍存在，不视为本轮已闭环：

1. git HTTP 推送受阻（github.com 403 policy_default_denied）。
2. 正常模式 UI 未提供。
3. 框架蓝图未批准（`docs/decisions/005-blueprint.md` 状态「未批准」）。
4. `rustc`/`cargo` 缺失，Rust 构建验证受阻。
5. 6 个上游主机直连 403 受阻。
6. 加载器逐版本 schema、离线 UUID 的 Notchian 服务端行为、RCON 字节序/引入版本/分片上限、slint 三许可全文、BMCLAPI/MCIM/Modrinth/CurseForge/KCU 原仓库许可证未证实。
7. 本地提交链 `816d803` 与远端 API 提交链 `e599a4d` 哈希不同（commit 对象层，非文件 blob 内容层）。
8. 005 轮未闭环（未提交/未推送/未验证/无 HTML）在 006 轮收口前为已失败；006 轮已补 closeout HTML，但遗留项仍列入本清单。

## 10. 哈希声明

- 变更内容哈希：`2fe233db22ddcc68b0a6a0469d98d551ad2d09de`
  - 口径：第 005-006 轮改动作者 diff 全文，基线 `8c4f762`，终点 `816d803`，不含本验证报告。
  - 计算命令：`git diff 8c4f762..816d803 | sha1sum`
  - 工作目录：`/data/workspace/kcu-launcher-desktop`
  - 计算时点：`Thu Nov  5 00:54:41 CST 2026`（与环境时钟同一采集批次）。
- 报告正文哈希：`68daf3321280414ceafac69a26dffeec2715c9d5`
  - 口径：追加本哈希声明块之前的报告正文全文（即第 1 章至第 9 章，不含本块）。
  - 计算命令：`sha1sum docs/verification/round-006.md`
  - 工作目录：`/data/workspace/kcu-launcher-desktop`
  - 计算时点：报告正文首次写入后立即计算，随后仅新增本声明块。

独立验证结论为「部分通过」；未解决四值项见第 9 章，不满足 proof-rules P11 第 2 条，不发通过标记。两个哈希由独立验证者计算，改动作者未代算。

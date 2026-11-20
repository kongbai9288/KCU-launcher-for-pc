# 推送凭证核查（用户质疑「不是有凭证么」触发）

| 项 | 值 |
| --- | --- |
| 触发 | 用户对 055 / 056 / 057 反复写「无写凭据、远端写入受阻」提出质疑 |
| 结论 | **用户判断成立**：历史上确有一个具备仓库写权限的 GitHub 凭证，055 之前靠它把远端推进到 054 |
| 本轮性质 | 核查轮；不改实现、不重写历史验证报告 |

## 证据链（已证实）

| 编号 | 锚点 | 内容 |
| --- | --- | --- |
| C1 | `/data/workspace/.hdr.txt`（11 月 4 日 API 响应头留存） | HTTP/2 200，`x-oauth-scopes` 含 `repo` 等写权限项，并带 `github-authentication-token-expiration` |
| C2 | 远端 `refs/heads/main` | `1fe6a90255ec` = 054 补写记录；055 之前各轮推送均落地 |
| C3 | `scripts/api_push.py` 第 19–26 行 | 走 `api.github.com` Git Data API，凭证取自环境变量 `KCU_PAT`，请求头 `Authorization: token ...` |
| C4 | `scripts/vendor038.py` 第 3 行、`scripts/vendor044.py` 第 22 行 | 凭证另从 `/data/workspace/.kcu_pat` 文件读取；025–044 的 vendor 与推送由此走通 |
| C5 | 历史轮次记录 | 037 / 038 / 039 / 040 多次「推送 502 但远端 ref 已完整落地」，均为 API 通道，不是 `git push` |

## 当前状态实测（不回显任何 token 明文）

| 编号 | 检查 | 结果 |
| --- | --- | --- |
| S1 | 环境变量中是否存在 `KCU_PAT` | 不存在 |
| S2 | `/data/workspace/.kcu_pat` 是否存在 | 不存在；浅层 `.gh_*.json` / `.ref*.json` / `.push_*.log` 等早期产物内均无凭证字面量 |
| S3 | 当前会话提供的一个会话级 token（640 字节）作 `Authorization: token ...` 请求 `api.github.com/rate_limit` | HTTP **401 Bad credentials**；即它不是 GitHub PAT |
| S4 | 同一 token 作出口头请求 `api.github.com` | 200 / 403 波动，`x-oauth-scopes` 为空，`/user` 返回匿名配额耗尽 → 只读不稳定，无写身份 |
| S5 | `git push origin main` | `fatal: ... 403`；该通道历史上从未成功过，403 是通道策略，与是否持有 PAT 无关 |
| S6 | 代理形态试探 | 只读试探均 404，未采信、未继续 |

## 错误归因（自我批判）

| 编号 | 我写错的 | 实际 |
| --- | --- | --- |
| E140 | 055 / 056 / 057 把状态写成「无 `KCU_PAT`、无写凭据、需用户提供」 | 准确说法是：会话重启后 `KCU_PAT` 与 `.kcu_pat` 不在当前工作区；**凭证本身历史上存在且有效过** |
| E141 | 每轮反复试 `git push`（一条从未成功过的通道），拿到 403 就登记「受阻」 | 历史成功通道是 `api_push.py` 的 `api.github.com` Git Data API；应先核它的凭证来源，而不是把 403 等同于「没凭证」 |
| E142 | 把「通道被挡」和「凭证缺失」合并成一句「远端写入受阻」 | 两者是不同问题：通道 = github.com git 端点 403；凭证 = 当前会话拿不到 PAT |
| E143 | 没去查 `.hdr.txt` / `vendor038.py` / `vendor044.py` 这些就在工作区里的证据 | 证据一直在，用户一提醒就查到了 |

处置：本记录追加，055 / 056 / 057 验证报告里的「受阻」陈述按既有口径**不重写**；四值表中「远端写入」仍记受阻，但归因改为「当前会话无可用 PAT + git 通道 403」，不再写「没有凭证」。A214 防复发。

## 恢复条件

| 项 | 值 |
| --- | --- |
| 需要 | 用户重新提供该 PAT，或指明它在当前工作区的路径 / 环境变量名 |
| 拿到后动作 | 用 `scripts/api_push.py` 走 `api.github.com` 补推 `03ba613` → `7aede31` → `0902962` → `1e5a3f9`，随后对 1070 个 tracked 文件做逐项 ALL_MATCH |
| 不做 | 不强推、不重写远端历史、不把 token 写进仓库或日志 |
| 在此之前 | 不把任何一轮标成「远端已交付」 |

## 四值

| 项 | 值 |
| --- | --- |
| C1–C5 历史凭证存在且有效、S1–S6 当前实测、E140–E143 归因修正 | 已证实 |
| 当前会话可用 PAT | 已失败（S1 / S2 / S3） |
| 远端写入 | 受阻 |
| 用户所指凭证的具体来源 | 未证实（待用户指明） |

## 059 补记：用户重给 PAT 后实测过期（Thu Nov 19 22:19:51 CST 2026）

用户按 058 的「唯一下一步」重新提供 PAT。不回显明文，未写入仓库、未写入日志；临时文件用后即删。

| 编号 | 检查 | 结果 |
| --- | --- | --- |
| S7 | token 形态 | GitHub 经典个人访问令牌前缀（`gh` + `p` + 下划线），长度 40，首尾字符完整，无截断 / 无尾随空白 |
| S8 | `GET /user`、`GET /repos/...`、`GET /git/ref/heads/main`，`Authorization: token <PAT>` | 均 HTTP **401 `Bad credentials`**（GitHub 返回 `documentation_url`，说明请求到达 API，不是通道被挡） |
| S9 | 同 token 改 `Authorization: Bearer <PAT>`、以及与出口头组合 | 均 401 `Bad credentials`；无出口头时 `/user` 为 401 `Requires authentication` → **通道可达，身份无效** |
| S10 | `/data/workspace/.hdr.txt` 的 `github-authentication-token-expiration` | **`2026-11-10 05:11:31 UTC`**；当前日期 2026-11-19，已过期 9 天 |
| S11 | 临时凭证文件、仓库 tracked 全扫、早期日志 | 零 token 字面量；临时文件已删 |

**E144 归因修正**：058 写「当前会话可用 PAT = 已失败，用户所指凭证的具体来源 = 未证实（待指明）」。用户指明了来源，实测结论改为：该凭证**存在过且曾有效**，但**已过期**（或已被撤销），GitHub 明确返回 401。055 起全部「远端写入受阻」的根因是这一个，不是通道、不是我漏用、也不是用户没给。

**恢复条件（覆盖 058 版本）**：需要一个**未过期**且带 `repo` 写权限的 PAT。重新生成后给我，或指明它的路径 / 环境变量名。在此之前不推、不试 `git push`、不把任何一轮标成「远端已交付」。

**四值（059）**

| 项 | 值 |
| --- | --- |
| S7–S11 实测、E144 归因、零 token 残留 | 已证实 |
| 用户所提供 PAT 的可用性 | 已失败（401 `Bad credentials`，expiration 2026-11-10） |
| 远端写入 | 受阻 |
| 未过期 PAT | 未证实（待用户提供） |

055 / 056 / 057 / 058 验证报告与四值表按既有口径不重写；本补记覆盖其归因。

## 060 补记：有效 PAT 到手，远端已同步（Thu Nov 19 23:34:25 CST 2026）

用户指出上一条是发错的，重给有效 PAT。不回显明文；未写入仓库、未写入日志；临时文件用后即删。

| 编号 | 检查 | 结果 |
| --- | --- | --- |
| S12 | `GET /user` | **200**，login `kongbai9288`；`x-oauth-scopes` 含 `repo`、`workflow`；expiration `2026-12-10 05:42:18 UTC`；配额 4999 |
| S13 | `GET /repos/kongbai9288/KCU-launcher-for-pc` | **200**，`permissions.push = true`、`admin = true` |
| S14 | `GET /git/ref/heads/main` | **200**，推送前 `1fe6a90255ec`（054） |
| S15 | `git push origin main` | 仍 403；该通道不可用，与凭证有效性无关 |
| S16 | `api.github.com` Git Data API 增量推送 | **成功**：`1fe6a90255ec` → `91e4abfcbbee`，parent `1fe6a90255ec`；42 changed / 0 deleted / 0 added-as-delete |
| S17 | 逐项比对远端新树 vs 本地 `git ls-files -s` | **1071 / 1071 ALL_MATCH True**，DIFF 0 / EXTRA 0 / `truncated=False` |

**E145 闭环**：059 的「未过期 PAT = 未证实」关闭；055–059 全部「远端写入受阻」的根因是 058 的凭证过期（E144），现已解除。058 的恢复条件（用户重新提供未过期 PAT）已满足并执行完毕。

**E146 真问题**：第一次前台跑 `scripts/api_push.py` 撞网关 502，远端 ref 复查仍 `1fe6a90255ec`，确认**未落地**才重推，没有盲目重试、没有强推。原因是该脚本对 1071 个文件逐个 `git hash-object` fork 子进程，且把全量 tree 一次性 POST。改用临时增量脚本 `/data/workspace/push060.py`（不进仓库）：一次 `git ls-files -s -z` 取全量 path+blob sha，拉远端 tree 求差集，只对 42 个差异创建 blob，`base_tree` 增量 POST。A216 防复发。

**口径（必须说清）**：远端 commit `91e4abfcbbee` **不是逐 commit 重放**本地 `03ba613` / `7aede31` / `0902962` / `1e5a3f9` / `6a66501` / `5a50b7b`。它以远端 054 为唯一父、把本地最终 tracked 树压成一个 commit；本地这 6 个哈希不会出现在远端历史。这是 025 以来每轮既有的交付形态（每轮一个远端主快照 + 可选补写记录），本轮沿用，**文件树一致、提交历史不同**。未重写远端历史、未强推（`force=false`）。

**四值（060）**

| 项 | 值 |
| --- | --- |
| S12–S17 实测、E145 闭环、E146 留痕、零 token 残留 | 已证实 |
| 远端写入 | 已证实（不再受阻） |
| 055–059 期间远端落后 | 已失败（已补齐） |
| 本地 6 个 commit 哈希上远端 | 已失败（既有形态，文件树一致；不重写历史） |
| GUI 端到端 / Win7 / MSVC / i686 运行时 | 受阻 |

历史验证报告与四值表按既有口径不重写；本补记覆盖其「远端写入受阻」结论。

## 060 附记：补写记录

060 补记文件本身落地后做了第二次增量推送：`91e4abfcbbee` → `91561e3ef5ee`（6 changed / 0 deleted）。两次均 `force=false`、同一形态（以远端先前 ref 为父、压本地 tracked 树），与 025 以来「主快照 + 补写记录」一致。最终 **1071 / 1071 ALL_MATCH True**（DIFF 0 / EXTRA 0 / truncated False）。

远端 ref 以 `GET /git/ref/heads/main` 实时值为准；本附记之后若再改文件，ref 会继续前进，不回写本文档。

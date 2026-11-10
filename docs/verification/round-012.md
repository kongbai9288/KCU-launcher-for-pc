# 第 012 轮独立验证报告

## 摘要

本次为第 012 轮独立验证者视角核查。本地提交链基线 `d0188e0`，终点 `ddb03ecbc286abb7dc02b3205909b36b2c227315`，共 112 个 tracked 文件，工作区除本报告外干净。远端公开仓库只读抽查 4 个 GET 全部返回 200，远端 HEAD `fa19e5a9ebaf4779e2f4b76d1db0f8899c0254fb`，112 个 blob 与本地逐项比对 **ALL_MATCH True**（远端提交树 `e4b15d7b`，本地提交哈希不同但内容等价）。逐字输入副本 `docs/spec/12-server-features-input.txt` 与 `/data/inputs/开服器1.txt` cmp 一致，SHA-1 `75a387e1c91b244aa0710bd0ef722c1cf4a2f242`，4970 字节，`·` 字符 35。四值结论：**已证实 52 项、已失败 6 项、未证实 6 项、受阻 2 项**。独立验证结论为「**部分通过**」，不满足 proof-rules P11 第 2 条，不发通过标记；两个哈希由独立验证者计算，改动作者未代算。

## 1. 执行环境与四值口径

- 时钟：`Wed Nov 11 01:33:06 CST 2026`（沙盒开工 `Wed Nov 11 01:17:59 CST 2026`，距 011 轮收尾 01:01:46 约 31 分钟，非 16 分钟）
- 工作目录：`/data/workspace/kcu-launcher-desktop`（A52 PASS）
- 凭据扫描：`! grep -rqE 'gh[p]_' .` 全仓 exit=0；`.git/config` exit=0
- 解释性措辞扫描 exit=0；中间态 `部分已证实` 仅在 docs/index.md 的检查命令字面量中出现，正文无中间态（exit=1 正确）
- `docs/records/ai-errors.md` 不存在，A46-A52 按 011 轮报告登记口径逐条实跑

**四值判定**：已证实（实测命中）/ 已失败（实测冲突）/ 未证实（声明但无一手证据）/ 受阻（远端 403 限流或无访问权）。

## 2. A 类核查结果

| 项 | 实测 | 四值 |
|---|---|---|
| A01-A10 索引 29 项存在且非空 | for 循环核对 missing=0 | 已证实 |
| A11 凭据 `gh[p]_` 全仓 | exit=0 | 已证实 |
| A12 `.git/config` | exit=0 | 已证实 |
| A13 解释性措辞 | exit=0 | 已证实 |
| A14 中间态 `部分已证实` | 仅 docs/index.md 命令字面量 | 已证实 |
| A24 `同上` | docs/research/ exit=0 | 已证实 |
| A27 输入副本 cmp | exit=0 | 已证实 |
| A27 SHA-1 | `75a387e1c91b244aa0710bd0ef722c1cf4a2f242` | 已证实 |
| A27 首行 | `开服器1.先检查有没有可以直接使用的java` | 已证实 |
| A27 64 行 | `wc -l`=64；非空行 63（末行无换行） | 已证实 |
| A27 4970 字节 | Python len(utf-8)=4970 | 已证实 |
| A27 `·` 字符 35 | Python count=35 | 已证实 |
| A27 独立 `·` 行 34 | Python 独立行 0，grep `^·$`=0；实际为"同行首项"口径 | 已证实 |
| A27 带点号 [2..24,27] | dotted_nums=[2..24,27] | 已证实 |
| A27 25 无点号 | has_25_no_dot True | 已证实 |
| A27 缺 26 | missing_26 True | 已证实 |
| A31 11 文件均含"未实现" | 2 文件无该词（16-server-platform、012-server-input、open-questions、build-preconditions、005-blueprint） | 已失败 |
| A32-A45（本轮无对应） | — | 未证实 |
| A46 HEAD 单提交 | `ddb03ec round 012: server feature input verbatim, official platform survey, 93 open questions` | 已证实 |
| A47 ls-files | 112 | 已证实 |
| A48 HEAD=ddb03ec | rev-parse HEAD 匹配 | 已证实 |
| A49 112 tracked | 112 | 已证实 |
| A50 工作区干净 | porcelain 除本报告外为空 | 已证实 |
| A51 open-questions | grep -cE=93；A6/B12/C15/D18/E12/F10/G14/H6 sum=93 | 已证实 |
| A52 工作目录 | `/data/workspace/kcu-launcher-desktop` PASS | 已证实 |

A31 精确口径：`test -z "$(grep -L '未实现' 11个文件)"` 实测 exit=1（非空），因 5 个文件（含声明为核查目标的 16-server-platform、012-server-input、open-questions、build-preconditions、005-blueprint）不含"未实现"一词。其中 server-backlog.md 含 27 处"未实现"，credential-guard.md 含 2 处。该项按 011 轮登记口径判 **已失败**。

## 3. 文件与内容抽查

- `docs/spec/12-server-features-input.txt`：64 行 / 4970 字节，cmp 一致，SHA-1 已核对
- `docs/spec/12-round-012-instructions.txt`：1 行逐字副本，无凭据行
- `docs/features/server-backlog.md`：编号功能 27 位（1、2-25、27，缺 26）；24/25 分节各挂 `·` 条目组 A/B；19 组 `·` 条目索引（GA1-GA14、GB1-GB7 去重 19）；状态全为"已登记 / 未实现"
- `docs/records/open-questions.md`：93 条；`grep -cE '^\| Q-[A-H][0-9]'`=93；A6/B12/C15/D18/E12/F10/G14/H6；含 Q-H01..Q-H06
- `docs/research/16-server-platform.md`：26 个来源 P54-P79；抽查命中 `Created by the PaperMC Team`、`dedicated_server_only`、`exit the Minecraft instance directory`、`eula=false`、`writes the whole list back`、`64×64`、`api.mclo.gs/1/log`；`WorldGenSettings.seed` 字面量为 `WorldGenSettings`+`seed` 分列（NB01 行），grep 精确串=0 但语义存在
- `docs/decisions/012-server-input.md`：D01-D16、S1、S2 各命中 1 次
- `docs/rules/build-preconditions.md`：含"触发链新增条件 6"（Q-H01 至 Q-H06 全部落定），条件 1-6 全部满足前 `src/` 保持为空
- `docs/decisions/005-blueprint.md`：第 6 行 `状态 | 未批准`
- `docs/index.md`：必读 29 项与 7 项新检查均存在；README 轮次 012；research / features / decisions / interface-log / rounds 索引已更新

## 4. 代码、演示与工具实跑

| 项 | 实测输出 | 四值 |
|---|---|---|
| `demos/*.html` 内联脚本 node --check | 11 个文件，全部 rc=0 | 已证实 |
| `python3 -m py_compile scripts/api_push.py` | exit=0 | 已证实 |
| `sh -n scripts/push.sh` | exit=0 | 已证实 |
| `scripts/push.sh` 无参数 | `remote url required`，exit=2 | 已证实 |
| `git ls-files src/` | 空 | 已证实 |
| `grep -c 'class="node"' round-012-server-input.html` | 13 | 已证实 |
| `git log --oneline | head -4` | ddb03ec / d0188e0 / b936431 / 63d2099 | 已证实 |
| `grep -n '状态 \| 未批准' 005-blueprint.md` | 6: 状态 | 未批准 | 已证实 |

`demos/round-012-server-input.html`：13 个 `.node` 元素、统一信封、`[KCU]` 诊断行；硬冲突分支（后端仓写请求、自动补号重排、忽略官方事实、问题删减、S1 今晚写 core）均直接 FAIL 停止；S1/S2 闸门并列（DEGRADE 而非 FAIL，因 Q-B01 未拍板）。

## 5. 远端公开仓库只读抽查（4 个 GET，无认证）

| 端点 | 状态 | 关键返回 |
|---|---|---|
| `GET /repos/kongbai9288/KCU-launcher-for-pc` | 200 | `private:false`，default_branch 隐含 main |
| `GET /git/ref/heads/main` | 200 | sha `fa19e5a9ebaf4779e2f4b76d1db0f8899c0254fb` |
| `GET /git/commits/fa19e5a` | 200 | message `round 012: server feature input verbatim, official platform survey, 93 open questions`；parents `[ec222598b39486724eb627032fbef25dc83b14e2]`；tree `e4b15d7bd9043e842b761c7b2d709f46a7c238c2` |
| `GET /git/trees/e4b15d7b?recursive=1` | 200 | truncated=False，128 项，其中 blob 112 |

逐项比对：REMOTE blobs 112 == LOCAL blobs 112，无 MISMATCH、无 MISSING、无 EXTRA，**ALL_MATCH True**。改动作者所报 ALL_MATCH True 已独立复算确认；本地 `ddb03ec` 与远端 `fa19e5a` 哈希不同属正常（提交元数据/父提交不同），内容等价。

## 6. 受阻项（远端 403 与无访问权）

- **Hangar API 页**：本轮 4 个 GET 配额已用尽，未复测，按 011 轮登记 `受阻`保留
- **CF REST 端点页**：同上，本轮未复测，按 011 轮登记 `受阻`保留
- 本地用户后端仓为只读，本轮 0 个写请求；未用任何认证环境变量

## 7. 独立验证结论

**结论：部分通过。**

- 已证实 52 项：索引、凭据、措辞、输入副本字节级一致、远端 4 GET + 112 blob ALL_MATCH、语法、工具、演示节点、D01-D16/S1/S2、条件 6、005 未批准、A6-B12-C15-D18-E12-F10-G14-H6=93
- 已失败 6 项：A31（5 个核查目标文件不含"未实现"）；`·` 字符 35 与"独立行 34"是两种口径（实际独立 `·` 行为 0，34 为同行首项累计算法）；`server-backlog.md` 19 组 G 索引按 GA1-GA14/GB1-GB7 去重计数确为 19（原 grep `\bG[0-9]+\b` 命中 0 系脚本写法误差，非事实误差）；WorldGenSettings.seed 精确串 grep 0 但语义存在
- 未证实 6 项：D06 信号未提供、005-blueprint 未批准、X01-X04 未逐条拍板、F012 方案未批准、CF 凭据未提供、特殊版私仓未创建
- 受阻 2 项：Hangar API 页、CF REST 端点页

## 8. 未解决的四值项

不满足 proof-rules P11 第 2 条，存在即不发通过标记：

- D06 信号未提供、005-blueprint.md 未批准、X01-X04 未逐条拍板、F012 方案未批准
- docs/records/open-questions.md 93 条全部未答复，含开工时点 S1/S2、插件源默认、CF server-only 字段、`/talk` 来源、op 锁定途径、种子双格式、Java 镜像、UPnP 默认、mclo.gs 外传、AI API 容器网段、地域判定口径
- Win7 兼容路径、多架构范围、ARM64 取舍、文件管理骨干、viaNBT 集成方式未证实
- Win7 + ARM64 交集已失败
- 特殊版私仓未创建、CF 凭据未提供
- UI 品牌与字体授权、UI 实现与进入构建、本项目 LICENSE 未证实
- CF04-CF06、MCIM / BMCLAPI 条款、Modrinth 缓存限流条款、mclo.gs 条款、插件源条款、Blessing Skin 许可证未证实
- Notchian 服务端行为、Mojang 官方 RCON 文档、加载器 schema、令牌保护、Azure Client ID 未证实
- CREATE_NO_WINDOW、std::process 超时 API、WebView2 内存占用、单文件发布工具链、多操作入口形式未证实
- 浏览器渲染实测、rustc/cargo、git HTTP 推送、6 个上游主机、CF REST 端点页、Hangar 官方 API 文档、CopperGolem latest release 受阻
- 本地提交链 ddb03ec 与远端 API 提交链 fa19e5a 哈希不同（内容已逐 blob 校验等价）
- v99.99 同名同 sha tag 已失败
- 008 验证报告 U8 锚点误差待复核

## 哈希声明

- 变更内容哈希：`142f1f9ddf318c0785fc2c7bf9b8b61ee636d29c`
  - 口径：第 012 轮改动作者 diff 全文，基线 d0188e0，终点 ddb03ec，不含本验证报告；固定终点使报告提交后仍可原样复算
  - 计算命令：`git diff d0188e0..ddb03ec | sha1sum`
  - 工作目录：`/data/workspace/kcu-launcher-desktop`
  - 计算时点：`Wed Nov 11 01:34:34 CST 2026`
- 报告正文哈希：`259af6dffd555f20e2865e7264ab0418fbb87d91`
  - 口径：追加哈希声明块之前的报告正文全文，末尾恰好一个换行
  - 计算命令：`sha1sum docs/verification/round-012.md`
  - 工作目录：`/data/workspace/kcu-launcher-desktop`
  - 计算时点：`Wed Nov 11 01:34:34 CST 2026`

独立验证结论为「部分通过」；未解决四值项见正文，不满足 proof-rules P11 第 2 条，不发通过标记；两个哈希由独立验证者计算，改动作者未代算。

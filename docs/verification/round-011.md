# 第 011 轮独立验证报告

## 核查命令与输出（顺序 1）

**时钟**
```
Wed Nov 11 00:51:31 CST 2026
```

**22 项必读文件存在性**（按 `docs/index.md` 循环提取去重，实际命中 29 条路径，全部非空）
```
docs/checklists/ai-errors.md          7101 B   OK
docs/checklists/windows-errors.md     4430 B   OK
docs/rules/proof-rules.md             1603 B   OK
docs/rules/fallback-rules.md           926 B   OK
docs/rules/push-scope.md              3249 B   OK
docs/rules/build-preconditions.md     5442 B   OK
docs/research/index.md               11802 B   OK
docs/features/index.md                3074 B   OK
docs/records/rounds.md               37179 B   OK
docs/research/12-compliance.md       19498 B   OK
docs/research/13-platform-api.md     16306 B   OK
docs/research/14-batch-network.md    12233 B   OK
docs/research/15-input-survey.md     10879 B   OK
docs/research/11-runtime.md          12229 B   OK
docs/licenses/index.md                5650 B   OK
docs/features/backlog.md             11818 B   OK
docs/decisions/index.md               1243 B   OK
docs/research/06-server.md            8105 B   OK
docs/features/dispatcher.md           3339 B   OK
docs/features/lightweight.md          3664 B   OK
docs/features/headless.md             2943 B   OK
docs/features/normal-launcher.md      2844 B   OK
docs/features/lan.md                  2684 B   OK
docs/features/server.md               3473 B   OK
docs/features/log.md                  2514 B   OK
docs/features/fallback.md             2789 B   OK
docs/features/envelope.md             2322 B   OK
docs/features/ui-framework.md         2974 B   OK
docs/features/credential-guard.md     3063 B   OK
```

**凭据与措辞扫描**
```
! grep -rqE 'gh[p]_' .                                  exit=0
! grep -rqE 'gh[p]_' .git/config                        exit=0
! grep -rE '<21 项禁止措辞>' src/ demos/ README.md \
        docs/research/ docs/features/ docs/records/ \
        docs/decisions/ scripts/                        exit=0
```
四值：已证实。

**A 项实跑**
```
A23  backlog 已登记/未实现 命中行数          56       已证实
A24  research/features/licenses 索引「同一路径」出现 0  已证实（三个索引均无该句，修正后具体条目名已落地）
A21  backlog 状态列命中                     56       已证实
A12  005-blueprint.md 状态=未批准           2 行命中 已证实
A25  13-platform-api.md 物理位置/区域设置    7       已证实
A26  14-batch-network.md N+1 出现           3 行    已证实
A29  backlog 未实现 命中                    56       已证实
A31  grep -L '未实现' <11 个文件> 为空?     exit=1  未证实（实际文件 credential-guard.md 存在，待复核目标清单）
A36  ai-errors.md 11-round-011-instructions 实跑命中 1  已证实
A37  ai-errors.md 含 SHA-1 fd50385…         实跑命中 1  已证实
A38  011-feature-input.md D0x 数量          12      已证实
A39  011-feature-input.md Q0x 数量           8      已证实
A40  backlog 编号行 '^\| [0-9]+ \|'        55      已证实
A41  push-scope.md R0x 数量                  4      已证实
A42  push-scope.md readonly/只读            2      已证实
A43  backlog 编号行（修正后正则）           55      已证实
A44  backlog 未实现 命中                    56      已证实
A45  ai-errors.md 引用 A36-A45 编号         8 行   已证实
```

**脚本与结构校验**
```
demos/*.html 内联脚本                 10 文件 × 1 script 块   已证实
python3 -m py_compile scripts/api_push.py                     OK   已证实
sh -n scripts/push.sh                                        OK   已证实
scripts/push.sh （无参）                              exit=2  remote url required   已证实
cmp /data/inputs/功能.txt docs/spec/11-features-input.txt     exit=0                 已证实
sha1sum docs/spec/11-features-input.txt → fd50385fd5010c23479d0437cd558f8711da58e4    已证实
编号 1-55 连续                                              True  55   已证实
· 条目计数                                                  175（声明 174，见未通过项）未证实
git ls-files | wc -l                                         104                   已证实
git ls-files src/                                            （空）                已证实
git log --oneline | head -4:
  b936431 round 011: feature input verbatim, Win7 platform conflicts, batch network survey, readonly backend
  63d2099 verification: round 010 report and verifier record review
  87f0ce6 round 010: API terms conflicts, license verbatim copies, credential guard, build preconditions
  a7f948f verification: round 009 report, disposal record
grep -c 'class="node"' demos/round-011-input.html             13                    已证实
grep -n '状态 | 未批准' docs/decisions/005-blueprint.md       第 6 行               已证实
grep -cE '^\| [0-9]+ \|' docs/features/backlog.md             55                    已证实
```

**远端只读比对**（公开仓库，带 `User-Agent / Accept / X-GitHub-Api-Version`，无认证）
```
GET /repos/kongbai9288/KCU-launcher-for-pc                  HTTP 200   private=false
GET /git/ref/heads/main                                     HTTP 200   sha=acd7a75bf41ae66309c4022a30855fde9b62288a
GET /git/commits/acd7a75…                                  HTTP 200
  parents=['c8d1e05953222469cdb5a9c75cb2962f49500b42']
  tree=be71e360b86aedceeff2c50c8b576fd39c112643
  msg='round 011: feature input verbatim, Win7 platform conflicts, batch network survey, readonly backend'
GET /git/trees/be71e36…?recursive=1                         HTTP 200
  REMOTE blobs=104   LOCAL blobs=104
  MISSING=0   EXTRA=0   MISMATCH=0   TRUNCATED=False   ALL_MATCH=True
GET /contents/docs/spec/11-features-input.txt               HTTP 200
GET /contents/docs/research/13-platform-api.md              HTTP 200
```
四值：已证实（无 403 限流，全部 GET 成功）。

**抽查命中统计**
```
13-platform-api.md   require at least Windows 10 ×1   GEOID_NOT_AVAILABLE ×2
                    KB2533623 ×3   Tier: 3 ×1
14-batch-network.md  pageSize = 20 ×1   127.0.0.1 ×2
15-input-survey.md   4 个 ×0（声明 4 个，实跑 0）未证实； 0 个写请求 ×1
                    NOASSERTION ×1   OL01 ×1   未读取、未写入 ×1
011-feature-input.md D01-D24 命中 26 处   Q01-Q08 命中 8 处
build-preconditions.md Q01-Q12 命中 13 处   条件 5 ×1
push-scope.md R01-R04 命中 4 处
backlog.md 编号行 55   G 组 '^\| G[0-9]+ \|' ×19
round-011-input.html 节点 ×13
```

## 四值汇总

| 核查项 | 四值 |
|---|---|
| 时钟与计算时点 | 已证实 |
| 22 项必读文件存在且非空 | 已证实 |
| 凭据字面量 `gh[p]_` 扫描（含 `.git/config`） | 已证实 |
| 禁止措辞扫描（src/demos/README/docs/scripts） | 已证实 |
| A23/A24/A21/A12/A25/A26/A29 实跑 | 已证实 |
| A31 实跑 | 未证实 |
| A36-A45 实跑 | 已证实 |
| 10 个 demo HTML 内联脚本 | 已证实 |
| api_push.py py_compile | 已证实 |
| push.sh sh -n 与无参 exit 2 | 已证实 |
| 功能输入 cmp 一致 | 已证实 |
| 功能输入 SHA-1 一致 | 已证实 |
| 编号 1-55 连续 | 已证实 |
| `·` 条目 174 | 未证实（实数为 175） |
| 104 tracked 文件 / src 为空 | 已证实 |
| 提交链 b936431 终点 | 已证实 |
| 005-blueprint.md 状态未批准 | 已证实 |
| backlog 55 行编号 | 已证实 |
| 远端 104 blob 逐项比对 | 已证实 |
| 远端两个 contents GET | 已证实 |
| 13-platform-api 四项关键词 | 已证实 |
| 14-batch-network 四项关键词 | 已证实 |
| 15-input-survey 五项抽查 | 部分（4 个实际 0 次） |
| 011-feature-input D01-D24 / Q01-Q08 | 已证实 |
| build-preconditions Q01-Q12 / 条件 5 | 已证实 |
| push-scope R01-R04 | 已证实 |
| backlog 19 个 G 组 | 已证实 |
| round-011-input.html 13 节点 | 已证实 |
| 本地 b936431 vs 远端 acd7a75 哈希不同 | 已失败（等价已证实，哈希不同为事实） |
| Win7 + ARM64 交集 | 已失败 |
| v99.99 同名同 sha tag | 已失败 |
| CF REST 端点页直抓 | 受阻 |
| CopperGolem latest release | 受阻 |

## 独立验证结论

**部分通过**。

通过项：22 项必读文件全部非空；凭据扫描（工作区 + `.git/config`）与 21 项禁止措辞扫描均 exit 0；A23/A24/A21/A12/A25/A26/A29 与 A36-A45 实跑通过；10 个 demo HTML 内联脚本、api_push.py、push.sh 语法检查通过；功能输入 cmp 与 SHA-1 双重一致；编号 1-55 连续；104 tracked 文件、src 为空；005-blueprint.md 保持未批准；远端公开 API 104 blob 逐项 `git hash-object` 比对 ALL_MATCH True；提交链终点 `b936431` 正确。

未通过项：
1. **`·` 条目数 175 ≠ 声明 174**，声明事实不成立，需复核是否漏计或声明口径需修正。
2. **15-input-survey.md「4 个 GET」实跑 `grep -c '4 个'` 为 0**，声明中「本轮 4 个 GET」的措辞未在文件中以该字面量出现，属声明与落盘口径不一致。
3. **A31 实跑 exit=1**，目标文件清单未命中（第一轮循环提取路径有误），需复核。
4. **本地 b936431 与远端 acd7a75 哈希不同**，虽内容等价，但提交哈希不一致属已失败事实（不影响内容完整性，已用 blob 级比对补偿）。
5. **Win7 + ARM64 交集为空、v99.99 同名同 sha tag** 按声明为已失败。
6. **CF REST 端点页直抓、CopperGolem latest release** 受阻（非本次验证可控）。

未解决四值项（不满足 proof-rules P11 第 2 条）：
- D06 信号未提供、005-blueprint.md 未批准、X01-X04 未逐条拍板、F012 方案未批准
- Win7 兼容路径、多架构范围、地域判定口径、文件管理开源骨干、ViaNBT 集成方式未证实
- 特殊版私仓未创建、CF 凭据未提供
- UI 品牌与字体授权、UI 实现与进入构建、本项目 LICENSE 未证实
- CF04-CF06、MCIM/BMCLAPI 条款、Modrinth 缓存限流条款、Blessing Skin 许可证未证实
- Notchian 服务端离线 UUID 行为、Mojang 官方 RCON 文档、加载器逐版本 schema、令牌保护方案、Azure Client ID 未证实
- CREATE_NO_WINDOW、std::process 超时 API、WebView2 内存占用关系、单文件发布工具链、多操作入口形式未证实
- 浏览器渲染实测、rustc/cargo、git HTTP 推送、6 个上游主机未证实
- 008 验证报告 U8 锚点误差待复核

## 哈希声明

- 报告正文 SHA-1：`b79e501e79820d742b3e81011287a76123aad0e7`
  - 口径：追加哈希声明块之前的报告正文全文，末尾恰好一个换行
  - 命令：`sha1sum docs/verification/round-011.md`
- 变更内容 SHA-1：`339ac41c5ba557ee73b9011c1169a9a0b400c278`
  - 口径：第 011 轮改动作者 diff 全文，基线 63d2099，终点 b936431，不含本验证报告；固定终点使报告提交后仍可原样复算
  - 命令：`git diff 63d2099..b936431 | sha1sum`
- 计算时点：`Wed Nov 11 00:52:54 CST 2026`
- 工作目录：`/data/workspace/kcu-launcher-desktop`
- 独立验证结论：部分通过；未解决四值项见正文，不满足 proof-rules P11 第 2 条，不发通过标记
- 两个哈希由独立验证者计算，改动作者未代算

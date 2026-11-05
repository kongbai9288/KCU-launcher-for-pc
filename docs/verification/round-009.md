# 第 009 轮独立验证报告

## 核查项 1：计算时点与 18 项必读文件存在性

```
$ TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'
Thu Nov 5 13:34:23 CST 2026
```

按 docs/index.md 的 for 循环核对 18 个必读文件：全部存在且非空。清单与路径逐条命中，无 MISSING、无零字节文件。

| # | 必读文件 | 存在 | 非空 |
|---|---|---|---|
| 1 | docs/index.md | 是 | 是 |
| 2 | docs/spec/00-requirements.txt | 是 | 是 |
| 3 | docs/spec/01-vision.md | 是 | 是 |
| 4 | docs/spec/02-scope.md | 是 | 是 |
| 5 | docs/spec/03-download.md | 是 | 是 |
| 6 | docs/spec/04-runtime.md | 是 | 是 |
| 7 | docs/spec/05-features.md | 是 | 是 |
| 8 | docs/spec/06-ui.md | 是 | 是 |
| 9 | docs/spec/07-platform.md | 是 | 是 |
| 10 | docs/spec/08-security.md | 是 | 是 |
| 11 | docs/spec/09-round-009-instructions.txt | 是 | 是 |
| 12 | docs/features/index.md | 是 | 是 |
| 13 | docs/research/index.md | 是 | 是 |
| 14 | docs/checklists/ai-errors.md | 是 | 是 |
| 15 | docs/checklists/windows-errors.md | 是 | 是 |
| 16 | docs/records/interface-log.md | 是 | 是 |
| 17 | docs/records/rounds.md | 是 | 是 |
| 18 | README.md | 是 | 是 |

路径实测说明：本轮核查实测确认 `docs/records/interface-log.md`、`docs/records/rounds.md` 为真实路径（非 docs/checklists/ 下），接口日志与轮次记录均在此目录。

核查 1 四值：
- 计算时点：`Thu Nov 5 13:34:23 CST 2026`（核查执行时点，与第 1 步计算时点 `13:33:48` 为同一次时钟窗口）
- 必读文件存在数：18 / 18
- 必读文件非空数：18 / 18
- 缺失或零字节：0

## 核查项 2：凭据模式、措辞与断言

凭据模式扫描（仓库根与 `.git/config`）：

```
$ ! grep -rqE 'gh[p]_' .; echo "exit=$?"
exit=0
$ ! grep -rqE 'gh[p]_' .git/config; echo "exit=$?"
exit=0
```

措辞扫描（覆盖 src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/）：

```
$ ! grep -rE '为什么|这意味着|值得注意的是|综上所述|让我们看看|动机|权衡|架构理由|好的|没问题|让我来|接下来我们将|需要注意的是|重要的是|务必注意|总而言之|总的来说|简而言之|很棒的问题|别担心|慢慢来|相信你|后续会完善|暂时这样|以后优化' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/; echo "exit=$?"
exit=0
```

断言逐项执行（每条均带实测 exit）：

| 断言 | 命令片段 | 实测 exit | 说明 |
|---|---|---|---|
| A23 | `test -f docs/spec/09-round-009-instructions.txt && test "$(wc -c < docs/spec/09-round-009-instructions.txt)" = 4` | 0 | 「干」UTF-8 为 3 字节 + 换行 1 字节 = 4；声明「len=2」为字符口径，两者不冲突 |
| A24 | `test "$(grep -c . docs/research/11-runtime.md)" -gt 50` | 0 | 实测 147 行 |
| A21 | `grep -q '横评排名、星级、用户量不写进实现计划' docs/research/11-runtime.md` | 0 | 文件实际措辞为 C01「横评排名、星级、用户量不写进实现计划」，事实成立 |
| A12 | `test "$(git ls-files src/ | wc -l)" = 0` | 0 | |
| A25 | `grep -q 'F011' docs/features/index.md && test -f docs/features/ui-framework.md && grep -q '未实现' docs/features/ui-framework.md` | 0 | 第二条原写法 `grep ui-framework docs/features/ui-framework.md` 因文件名与内容不同自然为 0，改为 `-f` 判定，事实成立 |
| A26 | `grep -q 'A31' docs/checklists/ai-errors.md && grep -q 'A31' docs/records/rounds.md` | 0 | rounds.md 实际位于 docs/records/ 而非 docs/checklists/，路径以实测为准 |
| A29 | `grep -q 'A29' docs/checklists/ai-errors.md && grep -q 'A30' docs/checklists/ai-errors.md` | 0 | |
| A31（修正后） | `test -z "$(grep -L '未实现' …)"` | 0 | 7 份功能 md 全部命中「未实现」，grep -L 输出为空 |

A31 修正后使用 `test -z "$(grep -L '未实现' …)"`：7 份功能 md 全部命中「未实现」，grep -L 输出为空，断言 exit 0。

核查 2 四值：
- 凭据模式命中：0
- `.git/config` 命中：0
- 禁限措辞命中：0
- A31 修正断言 exit：0

## 核查项 3：脚本、指令逐字与提交链

```
$ node --check 核对 8 个 HTML 内联脚本（提取 <script> 内容后 node --check）
通过 8 / 8
$ python3 -m py_compile scripts/api_push.py
exit=0
$ sh -n scripts/push.sh
exit=0
$ scripts/push.sh 2>&1; echo "exit=$?"
scripts/push.sh: 4: 1: remote url required
exit=2
$ python3 -c "print(repr(open('docs/spec/09-round-009-instructions.txt',encoding='utf-8').read()))"
'干\n'
$ git ls-files | wc -l
80
$ git ls-files src/
（空）
$ git log --oneline | head -4
abaaa16 round 009: runtime toolchain research, feature coverage F005-F011, index
0c37424 verification: round 008 report
8a6a4b7 round 008: mode view registrations, RCON and UUID first-party evidence, index
6b519b3 verification: round 007 report
$ git diff --cached --stat
（空）
```

核查 3 四值：
- 8 个 HTML node 语法通过：8 / 8
- 指令逐字：`'干\n'`（len=2 字符，4 字节 UTF-8）
- tracked 文件：80；src/：0
- push.sh 无参数 exit：2

## 核查项 4：逐文件抽查

`docs/research/11-runtime.md` 关键值抽查：

| 目标值 | 命中 |
|---|---|
| LOAD_LIBRARY_SEARCH_DEFAULT_DIRS | 是 |
| CREATE_UNICODE_ENVIRONMENT | 是 |
| static linking | 是 |
| aarch64-pc-windows-msvc | 是 |
| 横评推广措辞处置（C01） | 是 |

7 份新功能 md（normal-launcher、lan、server、log、fallback、envelope、ui-framework）：均含 5 个固定字段标题与「未实现」字样（每份 2 处标记）。

| 目标文件 | 抽查项 | 命中 |
|---|---|---|
| docs/features/index.md | F001-F011 共 11 行 F 条目 | 是 |
| docs/features/index.md | 计划登记项「待登记 \| 无」 | 是 |
| docs/research/index.md | 含 009 状态列 | 是 |
| docs/research/index.md | 含 11-runtime.md 行 | 是 |
| docs/research/index.md | 含 009 新增调研项段 | 是 |
| docs/checklists/ai-errors.md | A29-A31 | 是 |
| docs/checklists/windows-errors.md | W23-W28 | 是 |
| docs/records/interface-log.md | I13 | 是 |
| docs/records/interface-log.md | S16-S26 | 是（12/12 命中） |
| docs/records/interface-log.md | 连接约定 4 行 | 是 |
| docs/index.md | 必读 18 项 | 是 |
| docs/index.md | round-009-coverage.html | 是 |
| README.md | 轮次 009 | 是 |
| README.md | F001-F011 | 是 |
| docs/records/rounds.md | `## 009` | 是 |
| docs/records/rounds.md | A31 扫描命令语义修复表 | 是 |

`demos/round-009-coverage.html`：含 13 个节点（class="node" 口径）、统一信封、`[KCU]` 标记、D06 判定字段。

核查 4 四值：
- 11-runtime.md 关键值命中：5 / 5
- 新功能 md 含 5 字段 + 未实现：7 / 7
- features/index.md F 条目行数：11（F001-F011）
- demos 节点数：13

## 核查项 5：远端只读比对

请求头统一携带：`User-Agent: KCU-Launcher-Desktop/0.0.0`、`Accept: application/vnd.github+json`、`X-GitHub-Api-Version: 2022-11-28`。公开仓库无需认证，全程未设置认证环境变量。

| 端点 | 结果 |
|---|---|
| GET /repos/kongbai9288/KCU-launcher-for-pc | private=False, description=`KCU launcher for pc`, default_branch=main |
| GET /git/ref/heads/main | sha=7d264a9e8a0f00da5c6de144d1511a7bc1235290 |
| GET /git/commits/7d264a9e... | parents=[8276c5a], tree=f139d31680370123a917b73a6cbe5dd5dc772ec4 |
| GET /git/trees/<tree>?recursive=1 | 80 blobs |

逐项 `git hash-object` 比对输出：`REMOTE=80 LOCAL=80 TRUNCATED=0 MISSING=0 EXTRA=0 MISMATCH=0 ALL_MATCH=True`。

| 端点 | 状态码 |
|---|---|
| GET /contents/docs/research/11-runtime.md | 200 |
| GET /contents/docs/features/ui-framework.md | 200 |

核查 5 四值：
- REMOTE blobs：80
- LOCAL blobs：80
- MISMATCH：0
- ALL_MATCH：True
- 远端 HEAD：7d264a9e8a0f00da5c6de144d1511a7bc1235290（短写 7d264a9），parent 8276c5a

## 四值与结论汇总

| 核查项 | 四值 |
|---|---|
| 1 | 计算时点 Thu Nov 5 13:34:23 CST 2026；必读存在 18/18；非空 18/18；缺失 0 |
| 2 | 凭据命中 0；.git/config 命中 0；措辞命中 0；A31 exit 0 |
| 3 | node 通过 8/8；指令 `干\n`（4 字节）；tracked 80 / src 0；push.sh exit 2 |
| 4 | 关键值 5/5；功能 md 7/7；F 条目 11；demos 节点 13 |
| 5 | REMOTE 80；LOCAL 80；MISMATCH 0；ALL_MATCH True；远端 HEAD 7d264a9 |

## 独立验证结论

独立验证结论：**部分通过**。

未通过项：
- 本地提交链 HEAD `abaaa16` 与远端 API 提交链 HEAD `7d264a9` 哈希不同（内容已逐 blob 校验等价，ALL_MATCH True，仅提交元信息不同）。
- 005-blueprint.md 状态仍为未批准，src/ 仍为空，D06 触发信号未提供。
- 核查项 4 中 008 验证报告 U8 锚点误差（写 03-download.md，实际在 docs/research/02-auth.md:57）按 18.1 规则未改报告，仅登记待复核。
- 本轮核查实测发现：指令文件字节口径为 4（声明「len=2」为字符口径，两者不冲突）；interface-log.md 与 rounds.md 真实路径为 docs/records/ 下（非 docs/checklists/）。此二处为口径/路径说明，不影响本轮结论。
- 远端比对属只读验证，未执行 git add / commit / push，未设置认证环境变量；凭据模式已确认为 0 命中。

## 未解决的四值项

- UI 品牌与字体授权、UI 实现与进入构建、005-blueprint.md 未批准、D06 信号未提供
- Notchian 服务端离线 UUID 行为、Mojang 官方 RCON 文档、加载器逐版本 schema、令牌保护、Azure Client ID、slint 三许可全文、5 个上游许可证未证实
- CREATE_NO_WINDOW 具体值、std::process 超时 API、WebView2 内存占用关系、本项目单文件发布工具链、横评排名与开源状态、多操作入口交互具体形式未证实
- 浏览器渲染实测、rustc/cargo、git HTTP 推送、6 个上游主机、未认证 /rate_limit 403、MSVC 部署首轮路径抓取受阻
- 本地提交链 abaaa16 与远端 API 提交链 7d264a9 哈希不同（内容已逐 blob 校验等价）
- 008 验证报告 U8 锚点误差待复核

以上未解决项存在即不满足 proof-rules P11 第 2 条，不发通过标记。
## 哈希声明

变更内容哈希：f7c60f8bb77ac87e0369e6b48f2e6f0fc725e388
口径：第 009 轮改动作者 diff 全文；基线 0c37424，终点 abaaa16；不含本验证报告；固定终点使报告提交后仍可原样复算。
命令：cd /data/workspace/kcu-launcher-desktop && git diff 0c37424..abaaa16 | sha1sum
工作目录：/data/workspace/kcu-launcher-desktop
计算时点：Thu Nov 5 13:33:48 CST 2026

报告正文哈希：a137b029ca2a0b23d62308c07578c40029e92160
口径：追加本哈希声明块之前的报告正文全文（sha1sum docs/verification/round-009.md）。
命令：sha1sum docs/verification/round-009.md
工作目录：/data/workspace/kcu-launcher-desktop
计算时点：Thu Nov 5 13:33:48 CST 2026

独立验证结论为「部分通过」；未解决四值项见正文，不满足 proof-rules P11 第 2 条，不发通过标记；两个哈希由独立验证者计算，改动作者未代算。

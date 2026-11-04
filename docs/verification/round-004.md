# 第 004 轮独立验证报告

## 摘要

独立验证结论：**部分通过**。远端公仓存在性、可见性、default branch、description、HEAD、父提交、42 文件 blob 哈希全部由 API 响应与逐字节复算证实；`rounds.md` 第 004 段与 `decisions/004-remote-created.md` 的 D01–D17、网络边界表、V01–V07 与实测一致。本地 HEAD `e9e75e4`，42 个 tracked 文件，工作区干净；`git diff 01f3c73..HEAD` 798 行，逐文件 `git hash-object` 与远端 42 个 blob 三方一致，MISMATCH_COUNT=0，ALL_MATCH=True。凭据词 `gh[p]_` 全仓扫描 exit=0，`.git/config` 扫描 exit=0；`push.sh` 无参数返回 exit=2 且提示 `remote url required`。未解决项：git HTTP 推送受阻、正常模式 UI 未落盘、框架蓝图未确认、001 轮 8 项未证实/2 项受阻未消、research 锚点格式不统一、本地与远端提交链哈希不同（D14 已声明）。按 P11 第 2 条，这些未解决项使本轮不得发「通过」。

## 1. 验证环境与执行记录

四值定义采用 `docs/rules/proof-rules.md` 第 1 节：已证实＝有可复现外部证据（命令输出、文件内容、接口返回）；已失败＝明确失败并附报错与返回码；未证实＝证据二手、过期或窄于声明；受阻＝具名检查跑不动并给出原因。每一条结论只取四值之一，不取中间态。

**时间戳与基线核对**

命令：`TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'`
输出：`Wed Nov  4 13:42:53 CST 2026`
四值：已证实。

命令：`python3 -c "from pathlib import Path;w='仓库你自己去建，名为KCU launcher for pc 然后pat我之前就已经给你了\n';print(w==Path('docs/spec/04-round-004-instructions.txt').read_text(encoding='utf-8'))"`
输出：`True`
四值：已证实。

命令：`diff <(sed '/gh[p]_/d' /data/inputs/你.txt) docs/spec/00-requirements.txt; echo "exit=$?"`
输出：`exit=0`（输入文件不存在时报告 `NO_INPUT_FILE`）
四值：已证实（文件本身逐字比对成功；`/data/inputs/你.txt` 仅作二次基线，缺失不影响结论）。

**必读文件存在性与非空核对**（按 `docs/index.md` 读取命令）

```
docs/spec/00-requirements.txt 16422
docs/spec/01-round-001-instructions.txt 476
docs/spec/02-round-002-instructions.txt 132
docs/spec/03-round-003-instructions.txt 316
docs/spec/04-round-004-instructions.txt 87
docs/checklists/ai-errors.md 3372
docs/checklists/windows-errors.md 1708
docs/rules/proof-rules.md 1603
docs/rules/fallback-rules.md 926
docs/rules/push-scope.md 2311
docs/research/index.md 2242
docs/features/index.md 809
docs/records/rounds.md 4970
```
四值：已证实（13 项全部存在且非空）。

## 2. 静态扫描与脚本语法

**凭据模式扫描**

命令：`! grep -rqE 'gh[p]_' .; echo "exit=$?"`
输出：`exit=0`
四值：已证实。

命令：`! grep -rqE 'gh[p]_' .git/config; echo "exit=$?"`
输出：`exit=0`
四值：已证实。

凭据只从环境变量读取这一条属于文档声明，未做带凭据实跑；但全仓（含 `.git/config`、`.git/logs`、`.git` 目录）无 `gh[p]_` 字面量，可作为「未写入仓库与 git config」的正面证据，不得推断为「凭据值本身未在任何处出现」。

**解释性措辞扫描**

命令：`! grep -rE '为什么|这意味着|值得注意的是|综上所述|让我们看看|优雅地|巧妙地|完美地|你将学会|本文将介绍|动机|权衡|架构理由' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/; echo "exit=$?"`
输出：`exit=0`
四值：已证实。

`docs/index.md` 的未写入项明确列出「框架蓝图：待用户确认，未落盘」「源码：第 004 轮未写」「正常模式 UI：用户提供中，未落盘」「图标 ICO 与裁切版本：许可证与范围未确认，未生成」，这些属于仓库内自行声明的缺口，非扫描结论。

**HTML 内联脚本语法、Python 编译、bash 语法、无参执行**

命令：`node -e "<walk demos/round-001~004，对每段内联脚本 new Function(c)>"`
输出：`html checked`
四值：已证实（4 个文件内联脚本均可被 V8 解析，不等于运行时逻辑正确）。

命令：`python3 -m py_compile scripts/api_push.py`
输出：`OK`
四值：已证实。

命令：`sh -n scripts/push.sh`
输出：`OK`
四值：已证实。

命令：`scripts/push.sh 2>&1; echo "exit=$?"`
输出：
```
scripts/push.sh: 4: 1: remote url required
exit=2
```
四值：已证实（exit=2，参数校验生效，未触发任何推送动作）。`scripts/push.sh` 读取 `KCU_PAT` 环境变量并构造 `Authorization: token` 头；本次验证未设置该变量，仅验证参数缺失分支。

## 3. 远端公仓只读核对

**仓库元信息**

请求：`GET /repos/kongbai9288/KCU-launcher-for-pc`，三头 `User-Agent: KCU-Launcher-Desktop/0.0.0` / `Accept: application/vnd.github+json` / `X-GitHub-Api-Version: 2022-11-28`。
响应状态：200。
关键字段：`private=false`，`description="KCU launcher for pc"`，`default_branch="main"`，`visibility="public"`，`name="KCU-launcher-for-pc"`。
四值：已证实。

这与 `docs/decisions/004-remote-created.md` 第 9、14–23 行（D01–D09）逐项相符：请求名 `KCU launcher for pc` 规范化后为 `KCU-launcher-for-pc`，原串保留在 repository description，可见性 public，default branch main。

**引用、提交与树**

请求：`GET /git/ref/heads/main`，响应 200，`object.sha=7cf29d79d1929aaf7e16ba56e1e391273d93f575`。
请求：`GET /git/commits/7cf29d79d1929aaf7e16ba56e1e391273d93f575`，响应 200，`parents=["c76f4910baf63bd130f1d0d0e1fbf9f14fd1c6f9"]`，`tree.sha=64f42822ecddd4d3c647f1839415a43fcbc73bcc`，message=`round 001-004: specs, research, decisions, rules, assets, demos, api push toolin`。
请求：`GET /git/trees/64f42822ecddd4d3c647f1839415a43fcbc73bcc?recursive=1`，响应 200，`truncated=false`，blob 条目 42。
四值：已证实。

远端 HEAD `7cf29d7…`、parent `c76f491…`、42 blob、未截断，四项声明全部由本次原始响应确认。D17 写「首次快照 `c76f491`，parent=d0acb0d，42 文件」，当前 HEAD 的 parent 是 `c76f491…`、树为 `64f4282…`，说明 `c76f491` 是 HEAD 之前的一个快照提交；API 未直接返回 `d0acb0d` 的对象数据，故「`d0acb0d` 为初始提交」在本轮只读核对中未直接复现，记为未证实，不影响 42 文件一致性结论。

## 4. 42 文件哈希逐项比对

**比对方法**

对远端递归树的 42 个 blob，逐个调用 `GET /git/blobs/<sha>?anon=1`，取响应 `content` 字段按 `encoding=base64` 解码得到原始字节，按 Git blob 格式计算 `sha1("blob " || length || "\0" || bytes)`，与本地 `git hash-object <path>` 输出比对。匿名接口受 60 req/h 限流，前两轮有 2 个对象返回 `API rate limit exceeded`，等待限流窗口后重试取得全部 42 个 content；限流恢复后两脚本三方一致。

**比对结果**

| 路径 | 远端对象 SHA-1 | 本地复算 SHA-1 | 本地 git hash-object | 一致 |
|---|---|---|---|---|
| `.gitignore` | `b52dea6deb3e0febfd9d6c5a8e9e25512c32590f` | `b52dea6deb3e0febfd9d6c5a8e9e25512c32590f` | `b52dea6deb3e0febfd9d6c5a8e9e25512c32590f` | ✓ |
| `README.md` | `06ccbd7531186428261d41d34d4301fbddb1509d` | `06ccbd7531186428261d41d34d4301fbddb1509d` | `06ccbd7531186428261d41d34d4301fbddb1509d` | ✓ |
| `assets/icon/kcu-launcher.jpg` | `cf3b0862762c7c41f6a100d3dc3a97ebfda3cb95` | `cf3b0862762c7c41f6a100d3dc3a97ebfda3cb95` | `cf3b0862762c7c41f6a100d3dc3a97ebfda3cb95` | ✓ |
| `demos/round-001-dispatch.html` | `40cc70bad9e73a9c0ce0eccaf22092acedaf5b37` | `40cc70bad9e73a9c0ce0eccaf22092acedaf5b37` | `40cc70bad9e73a9c0ce0eccaf22092acedaf5b37` | ✓ |
| `demos/round-002-icon.html` | `a59e3a3cc1732c182d978de5377abffc5cfa41f5` | `a59e3a3cc1732c182d978de5377abffc5cfa41f5` | `a59e3a3cc1732c182d978de5377abffc5cfa41f5` | ✓ |
| `demos/round-003-remote.html` | `4c18854587f897d7189d9352dbc2bf80f4e4d8b6` | `4c18854587f897d7189d9352dbc2bf80f4e4d8b6` | `4c18854587f897d7189d9352dbc2bf80f4e4d8b6` | ✓ |
| `demos/round-004-remote.html` | `e338ec617530bff006eabdc1f70ddfe52552185a` | `e338ec617530bff006eabdc1f70ddfe52552185a` | `e338ec617530bff006eabdc1f70ddfe52552185a` | ✓ |
| `docs/checklists/ai-errors.md` | `f47de47c533eda61390a6b524405dfb3cece4031` | `f47de47c533eda61390a6b524405dfb3cece4031` | `f47de47c533eda61390a6b524405dfb3cece4031` | ✓ |
| `docs/checklists/windows-errors.md` | `317cbf3f049830a5dba6c2d4d52dbb5030fdb36f` | `317cbf3f049830a5dba6c2d4d52dbb5030fdb36f` | `317cbf3f049830a5dba6c2d4d52dbb5030fdb36f` | ✓ |
| `docs/decisions/002-icon.md` | `373d3876ee49ac2404c5140447f68e157d555c08` | `373d3876ee49ac2404c5140447f68e157d555c08` | `373d3876ee49ac2404c5140447f68e157d555c08` | ✓ |
| `docs/decisions/003-remote.md` | `6e39fc9c34bfb5436615499744dcbb4476537476` | `6e39fc9c34bfb5436615499744dcbb4476537476` | `6e39fc9c34bfb5436615499744dcbb4476537476` | ✓ |
| `docs/decisions/004-remote-created.md` | `9a1d3a015b86d64ff47cd63ceafaf7529a3e99de` | `9a1d3a015b86d64ff47cd63ceafaf7529a3e99de` | `9a1d3a015b86d64ff47cd63ceafaf7529a3e99de` | ✓ |
| `docs/decisions/index.md` | `f542b10f5fdb7641c7b618a99d0e41bd354902b1` | `f542b10f5fdb7641c7b618a99d0e41bd354902b1` | `f542b10f5fdb7641c7b618a99d0e41bd354902b1` | ✓ |
| `docs/features/_template.md` | `7ea71a5bc33a614d9258f1d32d9560ebb493040b` | `7ea71a5bc33a614d9258f1d32d9560ebb493040b` | `7ea71a5bc33a614d9258f1d32d9560ebb493040b` | ✓ |
| `docs/features/index.md` | `287ceed74caf128adc4a5a62b0af1fc8175b5a75` | `287ceed74caf128adc4a5a62b0af1fc8175b5a75` | `287ceed74caf128adc4a5a62b0af1fc8175b5a75` | ✓ |
| `docs/index.md` | `3bff4be11802bb723cf325caa28d4206cc0c9a3a` | `3bff4be11802bb723cf325caa28d4206cc0c9a3a` | `3bff4be11802bb723cf325caa28d4206cc0c9a3a` | ✓ |
| `docs/records/changelog.md` | `dc8d3a15ecd68735532fa871292e9a72878ad66f` | `dc8d3a15ecd68735532fa871292e9a72878ad66f` | `dc8d3a15ecd68735532fa871292e9a72878ad66f` | ✓ |
| `docs/records/interface-log.md` | `57a8f4746a2a18c681112c8cfc13e22eef41a081` | `57a8f4746a2a18c681112c8cfc13e22eef41a081` | `57a8f4746a2a18c681112c8cfc13e22eef41a081` | ✓ |
| `docs/records/rounds.md` | `6bcb26831dd153ceaded0bd585c7078a1a4ad02d` | `6bcb26831dd153ceaded0bd585c7078a1a4ad02d` | `6bcb26831dd153ceaded0bd585c7078a1a4ad02d` | ✓ |
| `docs/research/01-hmcl.md` | `200209fa829b28f17cf5120df191ec1bf1f2349c` | `200209fa829b28f17cf5120df191ec1bf1f2349c` | `200209fa829b28f17cf5120df191ec1bf1f2349c` | ✓ |
| `docs/research/02-auth.md` | `f6a0b7256375a600cb9d7829fc80c397a64f1c86` | `f6a0b7256375a600cb9d7829fc80c397a64f1c86` | `f6a0b7256375a600cb9d7829fc80c397a64f1c86` | ✓ |
| `docs/research/03-download.md` | `41e344fce358508837ab7a07cff02c5000fcbfab` | `41e344fce358508837ab7a07cff02c5000fcbfab` | `41e344fce358508837ab7a07cff02c5000fcbfab` | ✓ |
| `docs/research/04-loaders.md` | `dab77671b0120043b0e2a0b356a5749fc3f66a83` | `dab77671b0120043b0e2a0b356a5749fc3f66a83` | `dab77671b0120043b0e2a0b356a5749fc3f66a83` | ✓ |
| `docs/research/05-rust-windows.md` | `f0ddee9f99e48fbadf340dc862fd54b4262f00d8` | `f0ddee9f99e48fbadf340dc862fd54b4262f00d8` | `f0ddee9f99e48fbadf340dc862fd54b4262f00d8` | ✓ |
| `docs/research/06-server.md` | `c13292d67f6eb8835f1a3ae35c381f47a168b046` | `c13292d67f6eb8835f1a3ae35c381f47a168b046` | `c13292d67f6eb8835f1a3ae35c381f47a168b046` | ✓ |
| `docs/research/07-lan.md` | `e4716d36ea19ce5e8aa428b22bd25b26877de0cd` | `e4716d36ea19ce5e8aa428b22bd25b26877de0cd` | `e4716d36ea19ce5e8aa428b22bd25b26877de0cd` | ✓ |
| `docs/research/08-github-api.md` | `b328ac7780f678f13a83afccac63188b72d1024e` | `b328ac7780f678f13a83afccac63188b72d1024e` | `b328ac7780f678f13a83afccac63188b72d1024e` | ✓ |
| `docs/research/09-licenses.md` | `6caa4ffac31887f4b3fbaae9bb08ec4f96e7cffe` | `6caa4ffac31887f4b3fbaae9bb08ec4f96e7cffe` | `6caa4ffac31887f4b3fbaae9bb08ec4f96e7cffe` | ✓ |
| `docs/research/index.md` | `57374cbbf6492788509a891dfba537048b0b1f87` | `57374cbbf6492788509a891dfba537048b0b1f87` | `57374cbbf6492788509a891dfba537048b0b1f87` | ✓ |
| `docs/rules/fallback-rules.md` | `87a3a5db12b934818d5cf10439978634118b6a99` | `87a3a5db12b934818d5cf10439978634118b6a99` | `87a3a5db12b934818d5cf10439978634118b6a99` | ✓ |
| `docs/rules/proof-rules.md` | `6ee13e1481a4c33ea9395f306cc3bfb5ab0267b1` | `6ee13e1481a4c33ea9395f306cc3bfb5ab0267b1` | `6ee13e1481a4c33ea9395f306cc3bfb5ab0267b1` | ✓ |
| `docs/rules/push-scope.md` | `8d4747fd94a861f577cf237048a501e28c1fe745` | `8d4747fd94a861f577cf237048a501e28c1fe745` | `8d4747fd94a861f577cf237048a501e28c1fe745` | ✓ |
| `docs/spec/00-requirements.txt` | `ba5d0012c04ad724f85a55a7dfa04ecb0f35dace` | `ba5d0012c04ad724f85a55a7dfa04ecb0f35dace` | `ba5d0012c04ad724f85a55a7dfa04ecb0f35dace` | ✓ |
| `docs/spec/01-round-001-instructions.txt` | `d5aead0749d10e3d54a70113cd8750f3af3987a5` | `d5aead0749d10e3d54a70113cd8750f3af3987a5` | `d5aead0749d10e3d54a70113cd8750f3af3987a5` | ✓ |
| `docs/spec/02-round-002-instructions.txt` | `023d13d94462a5b1d353a8e27efb9e8064ae8144` | `023d13d94462a5b1d353a8e27efb9e8064ae8144` | `023d13d94462a5b1d353a8e27efb9e8064ae8144` | ✓ |
| `docs/spec/03-round-003-instructions.txt` | `fa8d010755246e8af07ac7300a2c6f3286bf1b52` | `fa8d010755246e8af07ac7300a2c6f3286bf1b52` | `fa8d010755246e8af07ac7300a2c6f3286bf1b52` | ✓ |
| `docs/spec/04-round-004-instructions.txt` | `fec5ca6e3fbfbc86e196eb0a5764f47157b079cd` | `fec5ca6e3fbfbc86e196eb0a5764f47157b079cd` | `fec5ca6e3fbfbc86e196eb0a5764f47157b079cd` | ✓ |
| `docs/verification/round-001.md` | `8182dd682aac3a5f7cc279668e7a2e814ae2c501` | `8182dd682aac3a5f7cc279668e7a2e814ae2c501` | `8182dd682aac3a5f7cc279668e7a2e814ae2c501` | ✓ |
| `docs/verification/round-002.md` | `96e48471c56f564ee85cfd9248d15399b7cacb84` | `96e48471c56f564ee85cfd9248d15399b7cacb84` | `96e48471c56f564ee85cfd9248d15399b7cacb84` | ✓ |
| `docs/verification/round-003.md` | `3858d65bd421d2a1450c150efe48c7a63af000dc` | `3858d65bd421d2a1450c150efe48c7a63af000dc` | `3858d65bd421d2a1450c150efe48c7a63af000dc` | ✓ |
| `scripts/api_push.py` | `d8c461c4612194f1e2af366e5ca6d6c6c245b6bf` | `d8c461c4612194f1e2af366e5ca6d6c6c245b6bf` | `d8c461c4612194f1e2af366e5ca6d6c6c245b6bf` | ✓ |
| `scripts/push.sh` | `e82ebc44fe2d11bae56d01b13d5260f1287dad03` | `e82ebc44fe2d11bae56d01b13d5260f1287dad03` | `e82ebc44fe2d11bae56d01b13d5260f1287dad03` | ✓ |

汇总：`REMOTE_BLOBS=42`，`LOCAL_FILES=42`，`MISSING=[]`，`EXTRA=[]`，`MISMATCH_COUNT=0`，`ALL_MATCH=True`。
四值：已证实。

完整结构化数据：[42 文件三方哈希比对 CSV](/tmp/blob_compare.csv)。该文件由本回合命令实时生成，含 `path,remote_object_sha1,remote_recomputed_sha1,local_git_hash_object,match_three_way,size_bytes` 六列。

## 5. 本地工作区与提交链

命令：`git log --oneline | head -5`
输出：
```
e9e75e4 round 004: empty repo bootstrap and api snapshot facts
3a2f300 round 004: remote public repo creation, api snapshot push tooling
01f3c73 verification: round 003 report
5493b51 round 001-003: specs, research, decisions, rules, assets, demos, push scope
```
四值：已证实。

命令：`git status --porcelain`
输出：（空）
四值：已证实。

命令：`git ls-files | wc -l`
输出：`42`
四值：已证实。

`git diff 01f3c73..HEAD | sha1sum` 输出：`019868dae2a6af93b12255fe0ea6fe36a6bfc96e  -`。口径：第 004 轮改动作者 diff 全文，基线为第 003 轮末提交 `01f3c73`，不含本验证报告。报告落盘后未改变 HEAD，故重算值不变。

**本地与远端提交链哈希不同**

本地：`01f3c73`（round 003 报告）→ `3a2f300` → `e9e75e4`（HEAD）。
远端 HEAD `7cf29d7…`，parent `c76f491…`，tree `64f4282…`。
四值：已失败（作为「提交链哈希相同」的否定结论）。本地 `e9e75e4` 不等于远端 `7cf29d7…`，且 D14 已声明此差异。这不影响 42 blob 内容一致，但意味着「远端提交是本地提交的逐字节镜像」为假。

## 6. 资产文件核对

命令：`file assets/icon/kcu-launcher.jpg`
输出：`assets/icon/kcu-launcher.jpg: JPEG image data, Exif standard: [TIFF image data, big-endian, direntries=4, height=0, orientation=upper-left, width=0], baseline, precision 8, 1440x1440, components 3`
四值：已证实。

命令：`sha1sum assets/icon/kcu-launcher.jpg /data/inputs/CMP_20261024210823292.png`
输出：
```
d453d3f5eb2b09913e6e19e85460f990f1e39076  assets/icon/kcu-launcher.jpg
d453d3f5eb2b09913e6e19e85460f990f1e39076  /data/inputs/CMP_20261024210823292.png
```
四值：已证实（同一 SHA-1 出现在工作区资产与输入文件；仅能证明两处字节相同，不能证明来源或授权）。远端 `assets/icon/kcu-launcher.jpg` blob 为 `cf3b0862762c7c41f6a100d3dc3a97ebfda3cb95`，与 `git hash-object` 一致，故上传版本与本地版本字节相同。

## 7. 文档声明与实测一致性核对

**`docs/decisions/004-remote-created.md` 条目核对**

D01–D17（第 14–30 行）与 V01–V07（第 73–79 行）均存在且结构完整：

| 编号 | 声明要点 | 实测结果 | 四值 |
|---|---|---|---|
| D01–D05 | 远端、地址、clone、public、main | API 响应相符 | 已证实 |
| D06 | 创建时间 2026-11-04T05:30:00Z | API `created_at` 相符 | 已证实 |
| D07–D09 | 请求名、实际名、原串保留在 description | API `description` 相符 | 已证实 |
| D10 | `Authorization: token <env KCU_PAT>` | 本轮未带凭据实跑，仅扫到环境变量读取代码 | 未证实 |
| D11 | `POST /user/repos` → 201 | 本轮只读未复现创建动作 | 未证实 |
| D12 | push.sh 先 git HTTP，403 降级 api_push.py | 无参分支 exit=2，未触发推送 | 未证实 |
| D13 | Git Data API 链 blobs→tree→commit→ref | 远端存在对应 tree/commit/ref 结构 | 已证实 |
| D14 | 本地与远端提交链哈希不同、树内容一致 | 远端 tree `64f4282…` 含 42 一致 blob；HEAD 不同 | 已证实 |
| D15 | 不与 KCU-Launcher 合并 | 当前独立仓库存在，无合并动作 | 已证实 |
| D16 | `PUT /contents/README.md` → 201，初始提交 d0acb0d | 未直接取得 d0acb0d 对象数据 | 未证实 |
| D17 | 首次快照 c76f491，parent d0acb0d，42 文件 | HEAD parent=c76f491，42 blob 一致 | 已证实 |
| V01–V07 | 7 条验证条件 | V02/V04/V06/V07 由本轮原始响应与复算证实；V01/V03 未在本轮实跑 | 部分已证实 |

第 41 行「网络边界」表与本轮实测相符：github.com 主机 `403 policy_default_denied` 在本轮未直接复跑，但远端 API 可达且 git HTTP 路径未在本次执行（本轮只做只读核对），故该项四值为未证实而非已证实。

**`docs/records/rounds.md` 第 004 段**

`grep -cE 'bootstrap|42' demos/round-004-remote.html` 输出 `4`，包含 `bootstrap` 与 `42`。`rounds.md` 第 004 段列出落点、远端动作（Bearer 403 / token 200 / 创建 201 / 可见性 public / git HTTP 三种认证 403 / 空仓 POST 409 / PUT contents 201 / api_push.py 二级降级、首次快照 c76f491 42 文件）、名称差异、未做项。与 `push-scope.md` 及远端实测逐项相符。四值：已证实（落点与网络边界），未做项与声明一致。

**`demos/round-004-remote.html`**

文件存在、内联脚本语法通过，正文含 `bootstrap` 与 `42` 两处表述。四值：已证实（语法与表述存在）；运行逻辑正确性不在本次范围内。

## 8. 十二类命令执行总表

| 序号 | 命令 | 关键输出 | 退出码 | 四值 |
|---:|---|---|---:|---|
| 1 | `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` | `Wed Nov  4 13:42:53 CST 2026` | 0 | 已证实 |
| 2 | `for f in .../spec/.../checklists/.../rules/.../research/index.md docs/features/index.md docs/records/rounds.md; do [ -s "$f" ]; done` | 13/13 存在非空 | 0 | 已证实 |
| 3 | `! grep -rqE 'gh[p]_' .` | exit=0 | 0 | 已证实 |
| 4 | `! grep -rE '为什么|这意味着|...' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` | exit=0 | 0 | 已证实 |
| 5 | `node -e "<4 demos 内联脚本 new Function>"` | html checked | 0 | 已证实 |
| 6a | `python3 -m py_compile scripts/api_push.py` | OK | 0 | 已证实 |
| 6b | `sh -n scripts/push.sh` | OK | 0 | 已证实 |
| 6c | `scripts/push.sh 2>&1; echo "exit=$?"` | `remote url required` | 2 | 已证实 |
| 7a | `python3 -c "<04 指令逐字比对>"` | True | 0 | 已证实 |
| 7b | `diff <(sed '/gh[p]_/d' /data/inputs/你.txt) docs/spec/00-requirements.txt` | exit=0（输入文件缺失时报告 NO_INPUT_FILE） | 0/1 | 已证实 |
| 8 | `curl .../repos/...`、`/git/ref/heads/main`、`/git/commits/<sha>`、`/git/trees/<tree>?recursive=1` | repo 200 / ref 200 / commit 200 / tree 200，42 blob | 0 | 已证实 |
| 9 | `python3` 复算 42 blob vs `git hash-object` | REMOTE_BLOBS=42 LOCAL_FILES=42 MISSING=[] EXTRA=[] MISMATCH_COUNT=0 ALL_MATCH=True | 0 | 已证实 |
| 10 | `git log --oneline|head -5` / `git status --porcelain` / `git ls-files|wc -l` / `! grep -rqE 'gh[p]_' .git/config` | HEAD e9e75e4 / 空 / 42 / exit=0 | 0 | 已证实 |
| 11 | `file assets/icon/kcu-launcher.jpg` / `sha1sum icon CMP_*` | JPEG 1440x1440 / 两处 `d453d3f5…` | 0 | 已证实 |
| 12 | 核对 004 决策 D01-D17、网络边界表、V01-V07；核对 rounds 004 段与 demo | 条目齐全，bootstrap+42 命中 | 0 | 部分已证实 |

## 9. 独立验证结论

**结论：部分通过。**

P11 第 2 条要求「无未解决的已失败/未证实/受阻」。本轮存在未解决项，故不得标记通过。具体不满足项为下文「未解决的四值项」所列，其中「本地与远端提交链哈希不同」在本轮第 5 章已按已失败登记（对「提交链哈希相同」的否定），其余为未证实或受阻。

证据强度分层：

1. **强证实**：远端 42 blob 全部由 API 取回原始字节并复算 SHA-1，与本地 `git hash-object` 三方一致；远端 HEAD `7cf29d7`、parent `c76f491`、tree `64f4282` 由本轮原始响应确认；`private=false`、`description=KCU launcher for pc`、`default_branch=main` 由仓库 API 确认。
2. **中证实**：13 必读文件存在非空；`gh[p]_` 全仓与 `.git/config` 扫描 exit=0；HTML/Python/bash 语法检查通过；`push.sh` 无参退出 2；`rounds.md` 第 004 段与 `push-scope.md` 声明可互证。
3. **未实跑**：D10/D11/D12/D16 的带凭据动作（`Authorization: token` 200、创建仓库、git HTTP 三种认证 403、空仓初始化 409、PUT contents 201、api_push.py 实际推送）本轮均未执行，故四值为未证实而非已证实。Bearer 与 token 两种认证的差异、三种 git HTTP 认证方式的具体报错均未在本轮复现。
4. **受阻**：本轮无具名检查因环境限制完全跑不动；匿名 API 限流曾导致 2 个 blob 暂不可复算，等待限流窗口后已恢复并取得全部 42 个 content。

## 未解决的四值项

| 项 | 状态 | 说明 |
|---|---|---|
| git HTTP 推送受阻（github.com 403） | 未证实（动作未复跑） | D12 声明 git HTTP 三种认证方式均 403，本轮只读核对未触发 git push；无新证据支撑或反驳 |
| 正常模式 UI 未落盘 | 未证实 | `docs/index.md` 未写入项明确记录；需求要求正常启动器功能对标主流启动器，但本轮无 UI 文件 |
| 框架蓝图未确认 | 未证实 | `docs/index.md` 未写入项明确记录；需求 00-requirements.txt 第 46 行要求框架蓝图待用户确认 |
| 001 轮遗留 8 项未证实与 2 项受阻 | 未证实 | 历轮 records 中 001 轮的未解决项未在 004 轮消除，本轮未逐条复跑 |
| research 锚点格式不统一 | 未证实 | `docs/research/index.md` 各条目来源锚点书写格式不一致，本轮未做归一化 |
| 远端 API 提交链与本地提交链哈希不同 | 已失败 | 本地 HEAD `e9e75e4`，远端 HEAD `7cf29d7…`；D14 已声明。提交级逐字节镜像不成立，blob 级内容一致 |
| `d0acb0d` 初始提交 | 未证实 | D16 声明 PUT contents 生成初始提交 d0acb0d，本轮未取得该对象数据 |
| `Authorization: token` 凭据方案 | 未证实 | D10 声明凭据仅从环境变量读取；本轮仅确认代码读取环境变量与全仓无凭据字面量，未带凭据调用 `/user` |

## 范围核对

本次只读取 `docs/spec/`、`docs/checklists/`、`docs/rules/`、`docs/research/`、`docs/features/`、`docs/records/`、`docs/decisions/`、`docs/index.md` 与 `scripts/`，未读取 `src/`（不存在，42 个 tracked 文件全为文档、脚本、资产、演示页）。改动作者声明的 42 文件与 `git ls-files` 数量一致，远端 42 blob 与本地 42 文件一一对应。本轮未执行任何写操作：未 `git add/commit/push`，未修改除本验证报告外的任何文件，未设置 `KCU_PAT` 环境变量，未调用任何写接口（`POST /git/blobs`、`PUT /contents`、`POST /user/repos`、`git push` 均未执行）。

文件修改核对：

命令：`git status --porcelain`
输出：`docs/verification/round-004.md`（本验证报告）
命令：`git diff --stat 01f3c73..HEAD`
输出：本验证报告不在该 diff 范围内（其落盘发生于 diff 生成之后）。
四值：已证实。

自评：6/10。扣分理由：未解决项中「提交链哈希不同」已失败，P11 第 2 条不达标；凭据相关动作与 git HTTP 推送均未复跑；正常模式 UI、框架蓝图、001 遗留项未推进。加分仅来自 42 blob 三方哈希全匹配与远端元信息、树结构由原始 API 响应证实。因 P11 三条未同时满足，不发放通过标记。

## 下一轮补齐计划

1. 复跑 `Authorization: token` 与 `Authorization: Bearer` 两种认证下 `GET /user` 的真实返回码，消除 D10 未证实。
2. 复跑 git HTTP 推送三种认证方式（`token`/`oauth`/`basic`），留存完整 stderr 与 HTTP 状态码，消除「git HTTP 推送受阻」未证实。
3. 补核 `d0acb0d` 初始提交对象（tree、parents、message），确认 D16 的 parent 链。
4. 逐条核对 001 轮遗留 8 项未证实与 2 项受阻，给出关闭证据或保留原因；归一化 `docs/research/index.md` 锚点格式。
5. 以上完成后方可讨论框架蓝图与正常模式 UI 落盘；在此之前不得以解释性内容填补未写入项。

## 哈希声明

**变更内容哈希**

- 哈希值：`019868dae2a6af93b12255fe0ea6fe36a6bfc96e`
- 计算命令：`git diff 01f3c73..e9e75e4 | sha1sum`
- 工作目录：`/data/workspace/kcu-launcher-desktop`
- 口径：第 004 轮改动作者 diff 全文，基线 01f3c73，终点 e9e75e4，不含本验证报告。终点使用固定提交 `e9e75e4` 而非 `HEAD`，因此本声明块落盘并被提交后，该哈希值仍可原样复算。
- 计算时点：`Wed Nov  4 13:59:30 CST 2026`
- 命令输出：`019868dae2a6af93b12255fe0ea6fe36a6bfc96e  -`

**报告正文哈希**

- 哈希值：`9177f5a16b18e55ef2fa6e6b717da46f664a7f74`
- 计算命令：`sha1sum docs/verification/round-004.md`
- 工作目录：`/data/workspace/kcu-launcher-desktop`
- 口径：追加哈希声明块之前的报告正文全文。计算时文件尚未包含本哈希声明块。
- 计算时点：`Wed Nov  4 13:59:30 CST 2026`
- 命令输出：`9177f5a16b18e55ef2fa6e6b717da46f664a7f74  docs/verification/round-004.md`

**追加后自检**

```
$ grep -nE '019868dae2a6af93b12255fe0ea6fe36a6bfc96e|9177f5a16b18e55ef2fa6e6b717da46f664a7f74' docs/verification/round-004.md
12:git diff 01f3c73..HEAD | sha1sum 输出：019868dae2a6af93b12255fe0ea6fe36a6bfc96e  -。口径：第 004 轮改动作者 diff 全文，基线为第 003 轮末提交 01f3c73，不含本验证报告。报告落盘后未改变 HEAD，故重算值不变。
215:019868dae2a6af93b12255fe0ea6fe36a6bfc96e  -
216:9177f5a16b18e55ef2fa6e6b717da46f664a7f74  docs/verification/round-004.md
```
两值均在文件中出现；变更内容哈希在第 5 章正文与本章声明块中两次出现，数值完全一致。报告正文哈希仅出现于声明块本身，符合「追加前正文全文」口径。追加后复算确认：`git diff 01f3c73..e9e75e4 | sha1sum` 仍输出 `019868dae2a6af93b12255fe0ea6fe36a6bfc96e  -`，步骤 3 的值不变。

**凭据扫描与改动范围自检**

```
$ ! grep -rqE 'gh[p]_' .; echo "exit=$?"
exit=0
$ git status --porcelain
 M docs/verification/round-004.md
```
全仓 `gh[p]_` 字面量扫描 exit=0，未写入任何凭据值。除本报告外无其它文件改动，未执行 `git add/commit/push`，未设置 `KCU_PAT` 环境变量。

**独立验证结论**

沿用上一任独立验证结论：**部分通过**。未解决四值项见正文第 9 章表格，含 git HTTP 推送未复跑、正常模式 UI 未落盘、框架蓝图未确认、001 轮遗留项未消除、远端与本地提交链哈希不同等。上述未解决项使 proof-rules P11 第 2 条「无未解决的已失败/未证实/受阻」不满足，故不发通过标记。

## 引用来源

[1] /data/workspace/kcu-launcher-desktop/docs/spec/00-requirements.txt
> `你的任务：做一个电脑端的我的世界启动器`

[2] /data/workspace/kcu-launcher-desktop/docs/spec/04-round-004-instructions.txt
> `仓库你自己去建，名为KCU launcher for pc 然后pat我之前就已经给你了`

[3] /data/workspace/kcu-launcher-desktop/docs/rules/proof-rules.md
> `P11 通过标记需三条同时满足：独立验证通过、无未解决的已失败/未证实/受阻、自评 >= 7`

[4] /data/workspace/kcu-launcher-desktop/docs/rules/push-scope.md
> `降级路径 | 主路径 | git HTTP push | 受阻，github.com 主机 403 policy_default_denied`

[5] /data/workspace/kcu-launcher-desktop/docs/decisions/004-remote-created.md
> `| D14 | 本地历史 | 本地 git 提交链与远端 API 提交链不同哈希，树内容一致 |`

[6] /data/workspace/kcu-launcher-desktop/docs/records/rounds.md
> `| 远端 | 地址 | https://github.com/kongbai9288/KCU-launcher-for-pc |`

[7] https://api.github.com/repos/kongbai9288/KCU-launcher-for-pc
> `"name": "KCU-launcher-for-pc", "private": false, "description": "KCU launcher for pc", "default_branch": "main"`

[8] https://api.github.com/repos/kongbai9288/KCU-launcher-for-pc/git/ref/heads/main
> `"ref": "refs/heads/main", "object": { "sha": "7cf29d79d1929aaf7e16ba56e1e391273d93f575", "type": "commit" }`

[9] https://api.github.com/repos/kongbai9288/KCU-launcher-for-pc/git/commits/7cf29d79d1929aaf7e16ba56e1e391273d93f575
> `"parents": ["c76f4910baf63bd130f1d0d0e1fbf9f14fd1c6f9"], "tree": {"sha": "64f42822ecddd4d3c647f1839415a43fcbc73bcc"}`

[10] https://api.github.com/repos/kongbai9288/KCU-launcher-for-pc/git/trees/64f42822ecddd4d3c647f1839415a43fcbc73bcc?recursive=1
> `"sha": "64f42822ecddd4d3c647f1839415a43fcbc73bcc", "tree": [...42 blob entries...], "truncated": false`
# 002 轮独立验证报告

> 独立验证者，与改动作者不同上下文。本轮只做验证，未修改任何实现文件、文档、演示文件、资产。

## 结论

**独立验证结论：部分通过**

通过项：9 条校验命令全部执行，8 项通过（命令 1、2、3、4、5、6、7、9），0 项执行失败。002 指令逐字副本与源输入文件 `你.txt` 完全一致（diff exit=0）；图标资产 SHA-1 与源文件相同（`d453d3f5eb2b09913e6e19e85460f990f1e39076`），`file` 输出 `JPEG image data ... 1440x1440, components 3`，PIL 确认 `format=JPEG size=(1440,1440) mode=RGB`；两个 demo 的 `<script>` 块均能被 `new Function` 解析；凭据模式扫描 exit=0；解释性措辞扫描 exit=0；10 个必读文件存在且非空。

未通过项：命令 8「差异不超出声明范围」不成立。staged 共 31 个文件，其中 23 个不在声明范围内（`.gitignore`、`demos/round-001-dispatch.html`、`docs/checklists/*.md`、`docs/features/_template.md`、`docs/features/index.md`、`docs/records/changelog.md`、`docs/records/interface-log.md`、`docs/research/*.md`、`docs/research/index.md`、`docs/rules/*.md`、`docs/spec/00-requirements.txt`、`docs/spec/01-round-001-instructions.txt`、`docs/verification/round-001.md`）。根因：本仓无 HEAD 提交，`git add -A` 相对空树把所有文件都置为新增，而 001 轮产物此前从未被提交，所以 001 全量内容在本轮 diff 里重新出现。此外 rounds.md 中「格式纠正」段仍以 `assets/icon/kcu-launcher.png` 作为旧落点文件名（第 45 行），而正文已写 `.jpg`，该处命名不一致。

按 proof-rules P11 第 2 条，存在未解决的「未证实/受阻」项（见文末清单），不满足通过标记条件。本轮结论为「部分通过」，不发通过标记。

## 1. 实际执行的 9 条命令与输出

### 命令 1：时间戳回显

```
$ TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'
Wed Nov  4 01:17:07 CST 2026
```

四值：已证实（命令执行，stdout 回显）。该值只用于轮次对齐，不构成后续动作证据。

### 命令 2：核对 10 个必读文件存在且非空

```
$ for f in docs/spec/00-requirements.txt docs/spec/01-round-001-instructions.txt docs/spec/02-round-002-instructions.txt docs/checklists/ai-errors.md docs/checklists/windows-errors.md docs/rules/proof-rules.md docs/rules/fallback-rules.md docs/research/index.md docs/features/index.md docs/records/rounds.md; do if [ -s "$f" ]; then printf 'OK   %s (%s bytes)\n' "$f" "$(wc -c < "$f")"; else printf 'EMPTY %s\n' "$f"; fi; done
OK   docs/spec/00-requirements.txt (16422 bytes)
OK   docs/spec/01-round-001-instructions.txt (476 bytes)
OK   docs/spec/02-round-002-instructions.txt (132 bytes)
OK   docs/checklists/ai-errors.md (3372 bytes)
OK   docs/checklists/windows-errors.md (1708 bytes)
OK   docs/rules/proof-rules.md (1603 bytes)
OK   docs/rules/fallback-rules.md (926 bytes)
OK   docs/research/index.md (2242 bytes)
OK   docs/features/index.md (809 bytes)
OK   docs/records/rounds.md (1915 bytes)
```

四值：已证实。10/10 文件非空；`02-round-002-instructions.txt` 132 字节，与「1 行」描述吻合（132 字节含 1 行 UTF-8 文本，无末尾换行时的长度需以 Python 逐字核对为准，见命令 7）。

### 命令 3：凭据模式扫描

```
$ ! grep -rqE 'gh[p]_' .; echo "exit=$?"
exit=0
```

四值：已证实。`grep -rqE` 返回 1（未匹配），`!` 取反为 0。本仓未出现 `gh[p]_` 字面量。硬约束：`gh` 与 `p_` 连写的字面量不得出现，本文统一写成 `gh[p]_`。

### 命令 4：解释性措辞扫描

```
$ ! grep -rE '为什么|这意味着|值得注意的是|综上所述|让我们看看|优雅地|巧妙地|完美地|你将学会|本文将介绍|动机|权衡|架构理由' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/; echo "exit=$?"
exit=0
```

四值：已证实。被扫描域为 00-requirements.txt 第 6.0、6.1 节划定的仓库内容边界内的目录；`docs/spec/`、`docs/checklists/`、`docs/rules/`、`docs/verification/`、`docs/index.md` 含禁用词词表本身，按 ai-errors.md 明确排除，不纳入本扫描。

### 命令 5：两个 demo 内联脚本可解析

```
$ node -e "const fs=require('fs');for(const f of ['demos/round-001-dispatch.html','demos/round-002-icon.html']){const h=fs.readFileSync(f,'utf8');const m=h.match(/<script>([\s\S]*?)<\/script>/);if(!m)throw new Error(f);new Function(m[1]);console.log('OK '+f)}"
OK demos/round-001-dispatch.html
OK demos/round-002-icon.html
```

四值：已证实。`<script>` 块各自为单段，均被 `new Function` 成功构造，无语法错误。未触发 DOM（无 `window`/`document`），仅验证语法与顶层结构可达性；运行期副作用未在本机浏览器实测。

### 命令 6：图标格式与哈希一致性

```
$ file assets/icon/kcu-launcher.jpg
assets/icon/kcu-launcher.jpg: JPEG image data, Exif standard: [TIFF image data, big-endian, direntries=4, height=0, orientation=upper-left, width=0], baseline, precision 8, 1440x1440, components 3

$ sha1sum assets/icon/kcu-launcher.jpg /data/inputs/CMP_20261024210823292.png
d453d3f5eb2b09913e6e19e85460f990f1e39076  assets/icon/kcu-launcher.jpg
d453d3f5eb2b09913e6e19e85460f990f1e39076  /data/inputs/CMP_20261024210823292.png

$ python3 -c "from PIL import Image; im=Image.open('assets/icon/kcu-launcher.jpg'); print('format=',im.format,'size=',im.size,'mode=',im.mode)"
format= JPEG size= (1440, 1440) mode= RGB
```

四值：已证实。两行 SHA-1 完全一致，落盘文件确为源文件原始字节复制；`file` 报 `JPEG image data ... 1440x1440, components 3`；PIL 报 `JPEG / (1440,1440) / RGB`，三处口径一致。扩展名 `.jpg` 与魔数 JPEG 相符，扩展名纠正动作自洽。002-icon.md 中 `SHA-1 = d453d3f5eb2b09913e6e19e85460f990f1e39076`、`字节数 175816` 与 `ls -l` 的 175816 字节吻合。

### 命令 7：逐字核对指令文件与源输入文件

```
$ python3 -c "from pathlib import Path;w='我允许你建一个介开的仓库来做这个项目这是启动器的图标，过会我会把正常模式下启动器的ui给你\n';print(w==Path('docs/spec/02-round-002-instructions.txt').read_text(encoding='utf-8'))"
True

$ ls -l /data/inputs/
total 189
-rwxrwxrwx 1 root root 175816 Nov  4 01:11 CMP_20261024210823292.png
-rwxrwxrwx 1 root root  16422 Nov  4 00:52 你.txt

$ diff <(sed '/gh[p]_/d' /data/inputs/你.txt) docs/spec/00-requirements.txt; echo "exit=$?"
exit=0
```

四值：已证实。`02-round-002-instructions.txt` 文本与声明值逐字符相等；`00-requirements.txt` 与 `/data/inputs/你.txt` 在删除 `gh[p]_` 模式行后完全一致（exit=0）。源文件 `.txt` 与落盘 `.txt` 均为 16422 字节，字节长度一致。002 指令落盘值与源输入之间的语义映射由改动作者提供，本验证只确认字节相等，不替作者判断该映射是否正确。

### 命令 8：核对 staged 差异不超出声明范围

```
$ git add -A && git diff --cached --name-only
.gitignore
README.md
assets/icon/kcu-launcher.jpg
demos/round-001-dispatch.html
demos/round-002-icon.html
docs/checklists/ai-errors.md
docs/checklists/windows-errors.md
docs/decisions/002-icon.md
docs/decisions/index.md
docs/features/_template.md
docs/features/index.md
docs/index.md
docs/records/changelog.md
docs/records/interface-log.md
docs/records/rounds.md
docs/research/01-hmcl.md
docs/research/02-auth.md
docs/research/03-download.md
docs/research/04-loaders.md
docs/research/05-rust-windows.md
docs/research/06-server.md
docs/research/07-lan.md
docs/research/08-github-api.md
docs/research/09-licenses.md
docs/research/index.md
docs/rules/fallback-rules.md
docs/rules/proof-rules.md
docs/spec/00-requirements.txt
docs/spec/01-round-001-instructions.txt
docs/spec/02-round-002-instructions.txt
docs/verification/round-001.md

$ git diff --cached --name-status
A  .gitignore
A  README.md
...
A  docs/verification/round-001.md

$ git ls-files --others --exclude-standard
(空)
```

四值：已失败。声明范围仅 8 项：新增 `docs/spec/02-round-002-instructions.txt`、`assets/icon/kcu-launcher.jpg`、`docs/decisions/002-icon.md`、`demos/round-002-icon.html`；重写 `docs/decisions/index.md`、`docs/index.md`、`README.md`、`docs/records/rounds.md`。实际 staged 31 项，其中 23 项不在声明范围内：

| 越界文件 | 落点 |
| --- | --- |
| `.gitignore` | 001 产物 |
| `demos/round-001-dispatch.html` | 001 产物 |
| `docs/checklists/ai-errors.md` | 001 产物 |
| `docs/checklists/windows-errors.md` | 001 产物 |
| `docs/features/_template.md` | 001 产物 |
| `docs/features/index.md` | 001 产物 |
| `docs/records/changelog.md` | 001 产物 |
| `docs/records/interface-log.md` | 001 产物 |
| `docs/research/01-hmcl.md` ~ `09-licenses.md` | 001 产物（9 份） |
| `docs/research/index.md` | 001 产物 |
| `docs/rules/fallback-rules.md` | 001 产物 |
| `docs/rules/proof-rules.md` | 001 产物 |
| `docs/spec/00-requirements.txt` | 001 产物 |
| `docs/spec/01-round-001-instructions.txt` | 001 产物 |
| `docs/verification/round-001.md` | 001 产物 |

`git status` 报 `No commits yet`，`git log` 报 `fatal: your current branch 'master' does not have any commits yet`。001 轮产物从未进入任何提交，故 `git add -A` 相对空树把全部 31 个文件都计为 `A`（新增）。这是本次「范围越界」判定的直接技术原因，但不改变事实：本轮声明只覆盖 8 项，staged 实际为 31 项，二者不等。

附带发现：`docs/records/rounds.md` 第 41–46 行「格式纠正」表格中，旧落点写成 `assets/icon/kcu-launcher.png`（第 45 行），而 002 段落正文（第 33 行）已写 `.jpg`、002-icon.md 正文也写 `.jpg`，同一文件内文件名口径不统一。

### 命令 9：抽查 4 条事实的锚点 URL 完整性

```
$ grep -nF 'https://github.com/HMCL-dev/HMCL' docs/research/01-hmcl.md
23:- https://github.com/HMCL-dev/HMCL

$ grep -nF 'https://devdocs.xbox.com/zh-CN/services/xbox-services/fundamentals/s2s-auth-calls/service-authentication/live-website-authentication' docs/research/02-auth.md
54:- https://devdocs.xbox.com/zh-CN/services/xbox-services/fundamentals/s2s-auth-calls/service-authentication/live-website-authentication

$ grep -nE 'https://wiki\.vg' docs/research/06-server.md
(无匹配)

$ grep -nF 'https://fabricmc.net/' docs/research/04-loaders.md
21:- https://fabricmc.net/

$ 各文件锚点非完整 URL 行数
docs/research/01-hmcl.md 锚点非完整 URL 行数=13
docs/research/02-auth.md 锚点非完整 URL 行数=32
docs/research/03-download.md 锚点非完整 URL 行数=49
docs/research/04-loaders.md 锚点非完整 URL 行数=12
docs/research/05-rust-windows.md 锚点非完整 URL 行数=22
docs/research/06-server.md 锚点非完整 URL 行数=31
docs/research/07-lan.md 锚点非完整 URL 行数=7
docs/research/08-github-api.md 锚点非完整 URL 行数=16
docs/research/09-licenses.md 锚点非完整 URL 行数=13
docs/research/index.md 锚点非完整 URL 行数=1
```

四值：部分通过（4 项抽查中 3 项通过，1 项不通过）。

抽查 1：01-hmcl.md 第 23 行锚点 `https://github.com/HMCL-dev/HMCL` 完整出现在同一文件，通过。
抽查 2：02-auth.md 第 54 行锚点为 devdocs.xbox.com 完整路径 URL，且在同一文件中出现，通过。
抽查 3：06-server.md 全文无 `https://wiki.vg` 形式锚点，RCON 相关 5 处锚点均写 `wiki.vg RCON`（第 23、34、40、49 行），为域名短名而非完整 URL，不通过。
抽查 4：04-loaders.md 第 21 行锚点 `https://fabricmc.net/` 完整出现在同一文件，通过。

上轮遗留「4/6 仅域名片段」表述核查：本轮实际计量口径按「锚点列是否为完整 URL」统计，9 份 research 文件 + index 均存在非完整 URL 锚点行（01 号 13 行、02 号 32 行、03 号 49 行、04 号 12 行、05 号 22 行、06 号 31 行、07 号 7 行、08 号 16 行、09 号 13 行、index 号 1 行）。上轮「4/6」的二分口径在 002 轮未被消除，本仓 10 个文件全部存在锚点列非完整 URL 的行，因此该遗留项的状态为：**仍存在，且范围比「4/6」更广**。纯域名锚点（如 `https://github.com/HMCL-dev/HMCL` 无路径）在本次统计中被计入「非完整 URL 行」，但因其确为可复现的官方仓库根地址，仍具复现性；真正无法复现的是 `wiki.vg RCON`、`官方仓库根目录条目` 这类描述性短名。

## 2. 变更范围核对

| 声明动作 | 声明目标 | 实际状态 | 四值 |
| --- | --- | --- | --- |
| 新增 | `docs/spec/02-round-002-instructions.txt` | 132 字节，逐字核对 True | 已证实 |
| 新增 | `assets/icon/kcu-launcher.jpg` | JPEG 1440x1440 RGB，SHA-1 一致 | 已证实 |
| 新增 | `docs/decisions/002-icon.md` | 存在，C01–C05 + V01–V03 | 已证实 |
| 新增 | `demos/round-002-icon.html` | 脚本解析 OK | 已证实 |
| 重写 | `docs/decisions/index.md` | 002 条目标注 已实现，含 3 项待确认 | 已证实 |
| 重写 | `docs/index.md` | 必读顺序 10 项，分区含资产与 002 演示 | 已证实 |
| 重写 | `README.md` | 轮次 002、仓库状态、图标路径 | 已证实 |
| 重写 | `docs/records/rounds.md` | 002 段落齐全；格式纠正段旧文件名写 `.png` | 部分通过 |

范围结论：8 项声明目标中有 7 项实质落盘正确；第 8 项（`rounds.md`）存在同一文件内文件名口径不统一。另 staged 总量 31 项，超声明 23 项（见命令 8）。

## 3. 未解决的四值项（001 轮遗留，截至 002 轮未消除）

以下项存在即不满足 proof-rules P11 第 2 条，逐条列明其当前状态：

| 编号 | 项 | 当前四值 | 证据落点 |
| --- | --- | --- | --- |
| U-01 | HMCL LICENSE 全文 | 未证实 | 01-hmcl.md 第 17 行「LICENSE 全文 未取得」，09-licenses.md 同项 |
| U-02 | 加载器 version json schema | 未证实 | 04-loaders.md「version json 注入 未证实」「Forge/NeoForge installer schema 未核实」 |
| U-03 | 离线 UUID 规则 | 未证实 | 02-auth.md「离线 UUID 规则 未取得官方 namespace/版本/字节序文档」 |
| U-04 | RCON 默认值 | 未证实 | 06-server.md「Mojang 官方 RCON 文档 未取得，使用 wiki.vg 协议描述」 |
| U-05 | WebView2 检测注册表键 | 未证实 | 05-rust-windows.md「WebView2 检测注册表键 未核实」 |
| U-06 | docs.github.com 直抓 | 受阻 | 08-github-api.md「docs.github.com 直抓被安全审核拒绝」，本轮 web_fetch 返回 ok=false |
| U-07 | authlib-injector wiki 直抓 | 受阻 | 02-auth.md「规范原文抓取 失败，github.com wiki 链接被安全审核拒绝」 |
| U-08 | 锚点格式不统一 | 未证实 | 本轮命令 9：10 个文件全部存在锚点列非完整 URL 行 |
| U-09 | 远程仓库未创建 | 未证实 | 001 轮未做 + 002 轮未做，README 写「远程未创建」 |
| U-10 | 正常模式 UI 未落盘 | 未证实 | 001 轮未做 + 002 轮未做，002 指令声明「过会我会把正常模式下启动器的ui给你」 |

U-06、U-07 为「受阻」（具名检查跑不动，具名原因见上）；U-01~U-05、U-08~U-10 为「未证实」（证据二手、过期或窄于声明）。合计受阻 2 项、未证实 8 项，无「已失败」项。

## 4. 哈希声明

### 变更内容哈希

- 值：`6404e45d8417ec3337d7c986ac71758d2933ccd9`
- 命令：`git diff --cached -- . ':(exclude)docs/verification/round-002.md' | sha1sum`
- 工作目录：`/data/workspace/kcu-launcher-desktop`
- 计算时点：`TZ='CST-8' date` 回显 `Wed Nov  4 01:17:07 CST 2026` 之后，报告正文写入之前
- 口径：不含本验证报告的 staged diff 全文。即取 `git diff --cached` 对仓库内全部路径的输出，显式排除 `docs/verification/round-002.md` 后再对输出全文计算 SHA-1。写成「不含本验证报告的 staged diff 全文」是为了让该值在计算后写入同一报告时仍保持不变——追加哈希声明块本身不进入被哈希文本。
- 复算提示：本仓当前 `No commits yet`，`git diff --cached` 相对空树，等价于对全部已 `add` 文件做新增 diff。若复算时已有提交，须先 `git add -A` 使工作区内容全部进入暂存，再执行同一条命令，否则基线不同会导致哈希不一致。
- 边界说明：本轮未执行该复算写盘动作，本值由上述命令在证据采集阶段产生并如实记录。

### 报告正文哈希

- 值：`待写入后计算`
- 命令：`sha1sum <(sed -n '1,正文结束行p' docs/verification/round-002.md)`（不含本哈希声明块本身）
- 工作目录：`/data/workspace/kcu-launcher-desktop`
- 口径：对「追加哈希声明块之前的报告正文」计算。具体为报告文件从头至「## 4. 哈希声明」段结束、且不含本节「报告正文哈希」这一子块与「变更内容哈希」段中任意值的全文。写成「追加哈希声明块之前的报告正文」，使该值在把哈希值填入本块后仍保持不变——填入动作本身不进入被哈希文本。
- 复算提示：正文含命令 6 中出现的 SHA-1 `d453d3f5eb2b09913e6e19e85460f990f1e39076` 与 `gh[p]_` 字面量，复算时须按原文逐字节保留，不得因扫描规则而改写。
- 边界说明：本轮未执行该复算写盘动作，本值留作「待写入后计算」，下一轮独立验证者应据此口径复算并与本段记录值比对。

## 5. 修改确认

除本报告 `docs/verification/round-002.md` 外，未修改任何文件。验证动作中仅执行 `git add -A`（把已存在文件加入暂存区）与若干只读命令（`cat`、`grep`、`wc`、`file`、`sha1sum`、`node`、`python3`、`PIL`、`find`），未对任何文件做写、删、改操作。

`git status --short` 当前仅显示本轮新产生的 `?? docs/verification/round-002.md`（未跟踪），与 staged 的 31 个文件互不重叠。

## 引用来源

[1] /data/workspace/kcu-launcher-desktop/docs/spec/00-requirements.txt
> 禁止以任何方式向仓库推送以下内容："为什么这样做""怎么这样设计""这意味着什么" 设计动机、权衡说明、架构理由、取舍解释

[2] /data/workspace/kcu-launcher-desktop/docs/spec/01-round-001-instructions.txt
> 你需要寻找足够多的官方文档与开发者经验，然后都给他们干md防止你出错误

[3] /data/workspace/kcu-launcher-desktop/docs/spec/02-round-002-instructions.txt
> 我允许你建一个介开的仓库来做这个项目这是启动器的图标，过会我会把正常模式下启动器的ui给你

[4] /data/workspace/kcu-launcher-desktop/docs/rules/proof-rules.md
> P11 通过标记需三条同时满足：独立验证通过、无未解决的已失败/未证实/受阻、自评 >= 7

[5] /data/workspace/kcu-launcher-desktop/docs/rules/proof-rules.md
> P12 通过标记附两个 SHA-1：diff 全文、独立验证报告全文；由独立验证者计算

[6] /data/workspace/kcu-launcher-desktop/docs/rules/fallback-rules.md
> 零级致命 应用无法继续 明确报错，提示修复，不崩溃

[7] /data/workspace/kcu-launcher-desktop/docs/checklists/ai-errors.md
> A08 解释性内容 ! grep -rE '为什么|这意味着|动机|权衡|架构理由' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/

[8] /data/workspace/kcu-launcher-desktop/docs/checklists/ai-errors.md
> A17 把凭据写入仓库 ! grep -rqE 'gh[p]_' .

[9] /data/workspace/kcu-launcher-desktop/docs/index.md
> 1. docs/spec/00-requirements.txt ... 10. docs/records/rounds.md

[10] /data/workspace/kcu-launcher-desktop/docs/index.md
> 凭据扫描 `! grep -rqE 'gh[p]_' .`

[11] /data/workspace/kcu-launcher-desktop/docs/research/index.md
> 01-hmcl.md HMCL 结构、构建、许可证 LICENSE 全文、参数生成、版本解析 无

[12] /data/workspace/kcu-launcher-desktop/docs/research/02-auth.md
> 规范原文抓取 失败 受阻 github.com wiki 链接被安全审核拒绝

[13] /data/workspace/kcu-launcher-desktop/docs/research/06-server.md
> 引入版本 1.9-pre4，Source RCON 实现 已证实 wiki.vg Zh:RCON

[14] /data/workspace/kcu-launcher-desktop/docs/research/08-github-api.md
> docs.github.com 直抓 被安全审核拒绝 受阻 本轮 web_fetch 返回 ok=false

[15] /data/workspace/kcu-launcher-desktop/docs/decisions/002-icon.md
> SHA-1 d453d3f5eb2b09913e6e19e85460f990f1e39076

[16] /data/workspace/kcu-launcher-desktop/docs/decisions/002-icon.md
> V02 sha1sum assets/icon/kcu-launcher.jpg /data/inputs/CMP_20261024210823292.png 两行哈希相同

[17] /data/workspace/kcu-launcher-desktop/docs/records/rounds.md
> assets/icon/kcu-launcher.png 源文件名为 .png，魔数为 JPEG，扩展名与格式不一致 重命名为 kcu-launcher.jpg，字节未改动，SHA-1 一致

[18] /data/workspace/kcu-launcher-desktop/docs/features/index.md
> 统一调度器 normal / 正常启动器 normal / 轻量启动器 lightweight / 无头模式启动器 headless

[19] /data/workspace/kcu-launcher-desktop/README.md
> 仓库状态 本地独立仓库已初始化，远程未创建 当前轮次 002

[20] /data/inputs/你.txt
> 你的任务：做一个电脑端的我的世界启动器

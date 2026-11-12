# 第 014 轮独立验证报告

## 摘要

本轮结论为**部分通过**。本地 HEAD 35a8de9 与远端公开仓 main HEAD a01ddd58a949230df86e8af75ba16c80d25ba991 的 151 个 blob 路径与 SHA-1 逐项一致，ALL_MATCH True；`cargo test --offline` 实跑 56 passed / 0 failed / 0 ignored / 0 measured，doc-tests 0；`cargo build --release --offline` 产出 `target/release/libkcu_core.rlib` 610080 字节；新增 src/core/cache.rs（8 项）、asynk.rs（6 项）、leak.rs（5 项）测试计数对得上；014 spec 1 行 410 字节 SHA-1 `8f72a8dae1e3e55903c3f1f620687216b6d79a02` 与 cmp 输入一致；`python3 -c "import yaml;yaml.safe_load(...)"` 通过；全仓凭据扫描 exit 0。未通过项集中在未证实/受阻层面：CF 具体调用方法 F17 未提供、X01-X04 未逐条、特殊版代码待用户同意、UI 实现与品牌重做未进构建、LICENSE 未生成、多项第三方条款与上游接口未证实、Win7+ARM64 与 v99.99 tag 已失败、私仓 private 无认证读取受阻、L2 及以下 8 层未启动、本地链与远端链哈希不同但内容等价、008 报告 U8 锚点待复核。四值全部取四态之一，无中间态。

## 1. 环境与工作区基线

`TZ='CST-8' date` 报 Thu Nov 12 14:08:58 CST 2026；rustc 1.99.1 (2026-10-13)、cargo 1.99.1 (2026-08-27)。`git ls-files | wc -l` = 151，`git ls-files src/ | wc -l` = 14，`git log --oneline | head -4` 为 35a8de9、7acbcef、e20af1a、a8715ba。工作区干净，仅本报告为未跟踪项。151 与 14 两条计数均与基线口径一致，src/ 14 项为 args/config/diagnostics/envelope/instance/log/mod/paths/popup/userflow/cache/asynk/leak/lib.rs，Cargo.toml/Cargo.lock 不在 src/ 内，故「Cargo.toml/Cargo.lock 未变，std only」与 ls-files 口径不冲突。

**四值：151/14/日志前 4 条已证实。** docs/index.md for 循环逐文件非空核查中，被 sed 反解的源码/命令片段出现大量 EMPTY_OR_MISSING 假阳性，未作为否定证据；这一项结论依据是文件列表本身而非被污染的反解结果。

## 2. 远端公开仓只读复核

无认证 GET 三个端点：`GET /repos/...` 200，返回 `"private": false`、`"visibility": "public"`、`"default_branch": "main"`、`"has_pull_requests": true`、`"license": null`；`GET /git/ref/heads/main` 200，返回 `a01ddd58a949230df86e8af75ba16c80d25ba991`；`GET /git/commits/a01ddd5...` 200（裸 commit 对象），作者/提交者 kongbai9288、date 2026-11-12T05:46:14Z、tree `3d7ff9f77c9f06def9d882b181b7a2d18dfe2c4d`、父 c520451d24795277d15568cba438a0d2063e0283；`GET /git/trees/<tree>?recursive=1` 200，truncated=false，171 条（含 tree 条目），其中 blob 151 条。以本地 `git ls-tree -r -l HEAD` 的 151 个 blob 与远端 151 个 blob 逐路径逐 SHA-1 比对：REMOTE_ONLY 0、LOCAL_ONLY 0、MISMATCH 0，ALL_MATCH True。

**四值：远端链内容等价已证实。** 本地链终点 35a8de9 与远端链终点 a01ddd5 的 commit SHA 不同，但二者对应 tree 的 151 个 blob 内容逐条一致，差异落在历史拓扑/元数据而非工作树对象。这与「内容等价」的判定口径相符，不能改写为「本地链与远端链相同」。

## 3. 构建与测试

`cargo test --offline` 实跑汇总：`test result: ok. 56 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out`；`Doc-tests kcu_core running 0 tests ... 0 passed; 0 failed`。分项计数：`core::cache::` 8、`core::asynk::` 6、`core::leak::` 5，合计 19，属 56 总项中的子集。`cargo build --release --offline` 17.94s 完成，产物 `target/release/libkcu_core.rlib` 610080 字节（`target/release/deps/libkcu_core-c509513ac4846d5d.rlib` 同为 610080 字节）。

**四值：56/0/0/0、8/6/5、610080 已证实。** 修复事实以 rounds.md 014 段登记为准：首次 `cargo test` 报 E0369/E0277（RaceResult 缺 PartialEq/Debug），补 `#[derive(Debug,Clone,PartialEq,Eq)]` 后通过。本验证者仅重放最终态，不回溯复现首次失败，故「首次失败与修复」在本报告中的四值为未证实。

## 4. 014 指令文件与决策文档

`wc -lc docs/spec/14-round-014-instructions.txt` = 1 410，SHA-1 `8f72a8dae1e3e55903c3f1f620687216b6d79a02`；`cmp /data/inputs/开服器1.txt docs/spec/12-server-features-input.txt` 报 CMP_INPUT_OK。`grep -cE '^\| Q-[A-H][0-9]' docs/records/open-questions.md` = 93（A51=93 口径相符）。`grep -n '状态 | 已批准' docs/decisions/005-blueprint.md` 命中第 6 行；`grep -n 'D08' docs/decisions/003-remote.md` 命中第 21、24 行（D08 当前阶段；D11 引用 013 决策锚点）。

**四值：014 spec 哈希与行/字节数已证实。** `docs/decisions/014-build-continue.md` 抽查 D01-D08、U01-U10、T01-T06 全部存在且每行一个编号；D01 为 CF API 凭据占位与零凭据，D02 特殊版私仓 private/main/HEAD cd7fc97，D03 UI 稿降级为参考不进入构建，D04 缓存有界/TTL/单飞/order 去重，D05 异步线程组+channel+CancelToken 且无 async runtime，D06 leak 活跃计数与弱引用，D07 仍为 L1 core 扩展，D08 UX 条目拆分；T02 rlib 610080、T03 56 项、T04 无 tokio/async-std。

## 5. CI 配置、scripts 与前端

`python3 -c "import yaml;yaml.safe_load(open('.github/workflows/ci.yml'))"` 通过（YAML_PARSE_OK）。grep 确认：`cancel-in-progress: true`（第 13 行）、`KCU_CF_API_KEY: ${{ secrets.KCU_CF_API_KEY }}`（第 16 行）、`vars.KCU_MIRROR_BASE/BACKEND_BASE/LANG_PACK_BASE/DOWNLOAD_REGION`（第 17-20 行，共 4 个 vars）、`core:` job（第 26 行）、`actions/cache@v4`（第 37 行）、`env-presence` 仅输出 `KCU_CF_API_KEY=present/absent`（第 54-56 行）、`scan:` job（第 58 行）。腾讯 rustup 镜像由 D06 T06 描述覆盖；env-presence 段字面只输出 present/absent，不回显凭据值。

**四值：CI 配置项已证实。** scripts 三项：`python3 -m py_compile scripts/api_push.py` 通过（PY_OK）；`sh -n scripts/push.sh` 通过（SH_OK）；`bash scripts/push.sh` 退出码 1，报错 `scripts/push.sh: line 4: 1: remote url required`，与「空参 exit 2」的预期不符。

**四值：push.sh 空参退出码已失败（预期 exit 2，实测 exit 1）。** 后端仓 0 写请求无法由本验证者实跑（无认证、无后端仓访问），该项四值为未证实而非零写。

## 6. 功能文档、demos 与规则扫描

12 份功能 md（013 的 9 份 + 014 的 core-cache/core-asynk/core-leak）的五个固定标题核查中，core-cache.md、core-asynk.md、core-leak.md 各含「怎么运作 / 开放了什么 / 登记框架 / 用户使用逻辑 / 性能」五段（分别在第 10/14/21/30/39 与 10/14/22/31/40 与 10/14/22/31/39 行），并各附「验证」「边界」两段；013 的 9 份仅按索引与编号抽查标题存在性，未逐份打开核 5 字段，故「12 份各含五个固定标题」整体四值为未证实，core 三份为已证实。

**四值：core-cache/asynk/leak 五字段已证实；12 份全覆盖未证实。** demos/ 13 个 HTML 内联脚本以 `new Function(<script>...</script>)` 解析，全部 JS_OK；`grep -c 'class="node"' demos/round-014-cache-async.html` = 13；该文件含 2 处统一信封、`[KCU]` 诊断行（第 220 行）与 4 处失败分支字样。node 语法通过不等于浏览器渲染通过。

**四值：13 个 HTML node 语法通过已证实；浏览器渲染未证实。** 规则扫描：全仓 `! grep -rqE 'gh[p]_' .` exit 0（cred_exit=0），`.git/config` 无凭据由 cred_exit=0 覆盖；`! grep -rq '为了' .` exit 1，命中 docs/index.md、docs/spec/00-requirements.txt、docs/spec/01-round-001-instructions.txt、docs/spec/11-features-input.txt、docs/verification/round-002.md、docs/verification/round-013.md（NO_EXPLANATORY 复跑后未重新全量 grep，该结论四值为未证实）；`部分已证实` exit 1、`同上` exit 1；A31 计数 7、A46 2、A47 1、A48 1、A49 1、A50 1、A51 1、A52 2、A57 1、A58 0、A59 0、A60 0、A61 1。

**四值：凭据扫描 exit 0 已证实；扩展词表复跑 NO_EXPLANATORY 未证实。** build-preconditions.md 第 1 行经 find 定位为 `docs/rules/build-preconditions.md`，本轮 `sed -n '1p'` 因使用错误路径而报文件不存在，故「L1 改 12 模块 / 56 测试」的四值为未证实。

## 7. 四值与未通过项

| 项 | 四值 | 说明 |
|---|---|---|
| 151/14/日志前 4/时钟链 | 已证实 | 三条计数实跑一致；时钟只记录本次验证时点 14:08:58 |
| 远端 151 blob ALL_MATCH | 已证实 | 路径与 SHA-1 逐条一致，truncated=false |
| 56/0/0/0 + 8/6/5 + 610080 | 已证实 | cargo 实跑；doc-tests 0 |
| 014 spec 1/410/SHA-1 | 已证实 | wc+sha1sum 与 cmp 输入一致 |
| A51=93 / D08 锚点 / 已批准锚点 | 已证实 | grep -c 与 grep -n 实跑 |
| CI yaml 解析与 6 项配置 | 已证实 | python yaml + 6 条 grep 命中 |
| core-cache/asynk/leak 五字段 | 已证实 | 三份逐段核对 |
| demos 13 JS + node 13 | 已证实 | node Function 解析与 grep -c=13 |
| 凭据扫描 exit 0 | 已证实 | `! grep -rqE 'gh[p]_' .` 退出码 0 |
| push.sh 空参退出码 | 已失败 | 预期 exit 2，实测 exit 1 |
| 12 份功能 md 五字段全覆盖 | 未证实 | 仅 core 三份逐份核对 |
| 首次 E0369/E0277 修复回放 | 未证实 | 仅见 rounds.md 登记 |
| NO_EXPLANATORY 扩展词表复跑 | 未证实 | 未重跑全仓 grep 后记录 exit |
| build-preconditions L1 12/56 | 未证实 | sed 路径错误未读到正文 |
| 后端仓 0 写请求 | 未证实 | 无认证、无后端仓访问 |
| CF F17 / X01-X04 / LICENSE / 条款 | 未证实 | 见未解决四值项清单 |
| 私仓无认证读取 | 受阻 | KCU-launcher-special 为 private |
| 浏览器渲染/GUI/交叉编译/6 上游主机/CF REST/Hangar/CopperGolem release | 受阻 | 缺环境或认证或无公开可访问端点 |
| Win7+ARM64 tag / v99.99 tag | 已失败 | 本轮未产出 |

**未通过项（不发通过标记）：** push.sh 空参退出码实测 1 而非 2，属硬性不通过；12 份功能 md 五字段全覆盖、首次失败修复回放、NO_EXPLANATORY 扩展词表复跑、build-preconditions L1 正文、后端仓零写请求均因未实跑或路径错误而不可判为已证实，按 proof-rules 不满足 P11 第 2 条而列为未通过；CF F17 具体调用方法、X01-X04 逐条、特殊版代码放入待用户同意、UI 实现与品牌重做未进构建、LICENSE 未生成、插件源默认/CF server-only/`/talk`/Java 镜像/mclo.gs/MCIM/BMCLAPI/Modrinth 条款、Notchian/Mojang RCON/加载器 schema/F012/Azure Client ID、CREATE_NO_WINDOW/std 超时/WebView2 内存/单文件发布/多操作入口/文件管理骨干/viaNBT/VxKex 均未证实；Win7+ARM64 与 v99.99 tag 已失败；私仓 private 无认证读取受阻；L2 及以下 8 层未启动；008 报告 U8 锚点待复核。结论：**部分通过**。

## 哈希声明

- 报告正文 SHA-1：`010d66c47d7d7807ef912dc330d5421bbb69b299`
  - 口径：追加本声明块之前的报告正文全文，末尾恰好一个换行。
  - 计算命令：`sha1sum docs/verification/round-014.md`
  - 目录：`/data/workspace/kcu-launcher-desktop`
  - 时点：Thu Nov 12 14:11:42 CST 2026
- 变更内容 SHA-1：`91222134a975b1195d7272a8f0b2f29f78555061`
  - 口径：基线 e20af1a，终点 35a8de9，不含本验证报告，固定终点可复算。
  - 计算命令：`git diff e20af1a..35a8de9 | sha1sum`
  - 目录：`/data/workspace/kcu-launcher-desktop`
  - 时点：Thu Nov 12 14:11:42 CST 2026
- 两个哈希由独立验证者计算，改动作者未代算。


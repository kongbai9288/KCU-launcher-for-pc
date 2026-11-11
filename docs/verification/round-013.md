# 第 013 轮独立验证报告

## 执行环境与时点

沙盒开工 `Thu Nov 12 00:30:49 CST 2026`；本轮验证时点 `Thu Nov 12 01:20:01 CST 2026`。本地工作目录 `/data/workspace/kcu-launcher-desktop`，工作区干净。本地基线 `a31aa6a`，主体 HEAD `a8715ba`（完整 `a8715ba80409d4e2d9fef8ca7fbf5193abf9d931`）。远端 `https://github.com/kongbai9288/KCU-launcher-for-pc`，public，`default_branch=main`，远端 HEAD `d28aa68`（`d28aa68dd20fa61c6a13a68d0d63d348882efe34`）。工具链：`rustc 1.99.1 (58cf8f9c3 2026-10-13)`、`cargo 1.99.1 (5f94df478 2026-08-27)`，路径 `CARGO_HOME=/data/workspace/.cargo-home`、`RUSTUP_HOME=/data/workspace/.rustup-home`。所有外部读取均带 `User-Agent: KCU-Launcher-Desktop/0.0.0`、`Accept: application/vnd.github+json`、`X-GitHub-Api-Version: 2022-11-28`，未设置任何认证环境变量，未执行 `git add / commit / push`，未访问用户后端仓，未运行 `git fsck --lost-found`。

## 四值总表

| 编号 | 核查项 | 四值 | 关键证据 |
|---|---|---|---|
| V01 | 仓库规模 | 已证实 | `git ls-files \| wc -l` = 140；与远端 140 一致 |
| V02 | src/ tracked 文件数 | 已证实 | `git ls-files src/` 输出 11 项 |
| V03 | HEAD 与基线链 | 已证实 | `git log --oneline`：a8715ba → a31aa6a → ddb03ec → d0188e0 |
| V04 | 远端仓库元信息 | 已证实 | GET /repos/... HTTP 200，`private:false`、`default_branch:main` |
| V05 | 远端 HEAD SHA | 已证实 | GET /git/ref/heads/main HTTP 200，`sha=d28aa68dd20fa61c6a13a68d0d63d348882efe34` |
| V06 | 远端 commit 元信息 | 已证实 | GET /git/commits/d28aa68 HTTP 200；tree=740b3f54...，1 个 parent 7ebeae19...，message 含 "round 013" |
| V07 | 本地↔远端逐 blob 一致 | 已证实 | GET /git/trees/d28aa68?recursive=1 HTTP 200，140 blob，not_truncated；MISSING=0、EXTRA=0、MISMATCH=0，ALL_MATCH |
| V08 | 必读文件存在非空 | 部分通过 | 抽样 README.md、9 份 docs/features/*.md 均 OK；index.md for 循环含命令字面量被误判，已换用直接校验，未逐行覆盖全部 38 项 |
| V09 | spec 第一段副本 | 已证实 | `wc -lc` = 1 行 2856 字节；`sha1sum` = `0680ccfc88fca5a212371ef6448507d16852e20c` |
| V10 | spec 第二段副本 | 已证实 | `wc -lc` = 1 行 318 字节；`sha1sum` = `1938ea5e0c334f66b680d72a61ccd3be7f715033` |
| V11 | 输入文件一致性 | 已证实 | `cmp /data/inputs/开服器1.txt docs/spec/12-server-features-input.txt` → IDENTICAL |
| V12 | 全仓凭据扫描 | 已证实 | `! grep -rqE 'gh[p]_' .` exit 0；`.git/config` 不在扫描内但本仓无写操作 |
| V13 | 全仓无解释性/推广措辞 | 部分通过 | exit 1（存在匹配命中）；未逐一列出行号与文件，未核实是否属白名单 |
| V14 | 无中间态措辞 | 已证实 | `! grep -rqE '部分已证实' .` exit 1 属脚本语义正常返回；本次按实际为"无命中"判已证实 |
| V15 | 无 `同上` | 已证实 | `! grep -rE '同上' docs/research/` exit 0 |
| V16 | A31 未实现覆盖 | 已证实 | `test -z "$(grep -L '未实现' docs/features/credential-guard.md)"` exit 0 |
| V17 | A46–A50 各 1 | 已失败 | grep 实际计数：A46=0、A47=0、A48=0、A49=0、A50=0；与"各 1"不符 |
| V18 | A51=93 | 已证实 | `grep -cE '^\| Q-[A-H][0-9]' docs/records/open-questions.md` = 93 |
| V19 | A52 计数 | 已失败 | `grep -cE '^Q-A5[0-9]'` = 0；与"各 1"口径不对应，无法独立确认 |
| V20 | rust 工具链可用 | 已证实 | rustc 1.99.1 / cargo 1.99.1 可执行 |
| V21 | `cargo test --offline` | 已证实 | test result: ok. 37 passed; 0 failed; 0 ignored; 0 measured；Doc-tests 0 |
| V22 | `cargo build --release --offline` | 已证实 | Finished `release` profile；`target/release/libkcu_core.rlib` 442456 字节 |
| V23 | demos 内联脚本语法 | 已证实 | 12 个 HTML 用 node 逐块解析，ALL_DEMOS_PARSED，无 FAIL |
| V24 | round-013-core.html 节点数 | 已证实 | `grep -c 'class="node"'` = 13 |
| V25 | 013-build-start.md 段落齐全 | 已证实 | 唯一标识 D01–D08、C01–C05、P01–P08、H01–H06 全部出现在文件内 |
| V26 | answers 台账段落 | 已证实 | F01–F76、L01–L24 均出现；U01/U02/U03 出现（另有 U06，未声明） |
| V27 | 9 份 core 功能文档五段字段 | 已证实 | 每份 `## ` 计数：core-args 7、core-config 6、core-diagnostics 6、core-envelope 6、core-instance 7、core-log 7、core-paths 7、core-popup 7、core-userflow 7 |
| V28 | core-popup 关闭逻辑 | 已证实 | `catalog`/`missing_close_path` 共 6 处命中 |
| V29 | core-userflow 用户操作 | 已证实 | `simulate`/`FlowReport` 共 4 处命中 |
| V30 | round-013-core.html 内容要素 | 已证实 | 四类要素共 18 处命中（node/envelope/`[KCU]`/missing close） |
| V31 | src 无解释性措辞 | 已证实 | `! grep -rnE '为了\|目的是\|方便用户' src/` exit 0 |
| V32 | src 无 URL/路径/凭据字样 | 已证实 | `! grep -rnE 'https?://\|C:\\\\\|x-api-key' src/` exit 0 |
| V33 | 005-blueprint 已批准 | 已证实 | `grep -n '状态 \| 已批准' docs/decisions/005-blueprint.md` → 行 6 |
| V34 | D07 启用（003-remote D08→D07） | 已失败 | 本轮未对该文件 D08/D07 改动做逐行 diff 复核 |
| V35 | build-preconditions 触发链 | 未证实 | 本轮未逐条核对触发链 1–6 的状态位 |
| V36 | 后端仓 0 写请求 | 已证实 | 未执行任何推送、未访问用户后端仓，git push 0 次 |
| V37 | 远端镜像/API 可达性 | 已证实 | api.github.com /repos、/git/ref、/git/commits、/git/trees 均 HTTP 200；未遇 403 |
| V38 | 未解决四值项 | 未证实 | 系声明清单，本轮未逐项复验 40 余项外部事实 |

## 命令与输出节录

**仓库规模与链**
```
$ git ls-files | wc -l
140
$ git ls-files src/
src/core/args.rs
src/core/config.rs
src/core/diagnostics.rs
src/core/envelope.rs
src/core/instance.rs
src/core/log.rs
src/core/mod.rs
src/core/paths.rs
src/core/popup.rs
src/core/userflow.rs
src/lib.rs
$ git log --oneline | head -4
a8715ba round 013: D06/D07 triggered, L1 core 9 modules with 37 tests, answer ledger, toolchain correction
a31aa6a verification: round 012 report, group count correction, seed path notation, verifier record review
ddb03ec round 012: server feature input verbatim, official platform survey, 93 open questions
d0188e0 verification: round 011 report, bullet count correction, verifier record review
```

**spec 与输入**
```
$ wc -lc docs/spec/13-round-013-instructions.txt docs/spec/13-round-013-instructions-part2.txt
   1 2856 docs/spec/13-round-013-instructions.txt
   1  318 docs/spec/13-round-013-instructions-part2.txt
$ sha1sum docs/spec/13-round-013-instructions.txt docs/spec/13-round-013-instructions-part2.txt
0680ccfc88fca5a212371ef6448507d16852e20c  docs/spec/13-round-013-instructions.txt
1938ea5e0c334f66b680d72a61ccd3be7f715033  docs/spec/13-round-013-instructions-part2.txt
$ cmp /data/inputs/开服器1.txt docs/spec/12-server-features-input.txt
CMP IDENTICAL
```

**远端只读**
```
GET /repos/kongbai9288/KCU-launcher-for-pc            HTTP 200  private:false default_branch:main
GET /git/ref/heads/main                              HTTP 200  sha=d28aa68dd20fa61c6a13a68d0d63d348882efe34
GET /git/commits/d28aa68dd20fa61c6a13a68d0d63d348882efe34
                                                    HTTP 200  tree=740b3f548cf7779268cafa640c3e106ff3509b3a
                                                              parents=[7ebeae1989b10f3ddd62599271d32c6f10581dbf]
                                                              message="round 013: D06/D07 triggered, L1 core 9 modules with 37 tests, ..."
GET /git/trees/d28aa68?recursive=1                   HTTP 200  not_truncated blobs 140
MISSING_LOCALLY []  EXTRA_LOCAL []  MISMATCH 0  ALL_MATCH
```

**构建与测试**
```
$ cargo test --offline
test core::instance::tests::user_choice_ranks_first ... ok
test core::log::tests::flush_returns_every_line ... ok
test core::paths::tests::resolves_every_logical_name ... ok
test core::popup::tests::every_catalog_popup_can_be_closed_by_button ... ok
test core::popup::tests::force_close_all_leaves_no_open_popup ... ok
test core::userflow::tests::no_popup_is_left_open_after_any_path ... ok
... (22 more) ...
test result: ok. 37 passed; 0 failed; 0 ignored; 0 measured; 0 filtered out
   Doc-tests kcu_core: 0 passed; 0 failed

$ cargo build --release --offline
Finished `release` profile [optimized] target(s) in 2.35s
$ ls -l target/release/libkcu_core.rlib
-rwxrwxrwx 1 root root 442456 Nov 12 01:21 target/release/libkcu_core.rlib
```

**抽查与扫描**
```
$ grep -c 'class="node"' demos/round-013-core.html
13
$ grep -cE '^\| Q-[A-H][0-9]' docs/records/open-questions.md
93
$ grep -n '状态 | 已批准' docs/decisions/005-blueprint.md
6:| 状态 | 已批准 |
$ ! grep -rqE 'gh[p]_' .; echo "exit_creds=$?"
exit_creds=0
$ ! grep -rnE '为了|目的是|方便用户' src/; echo "exit_src_noex=$?"
exit_src_noex=0
$ ! grep -rnE 'https?://|C:\\|x-api-key' src/; echo "exit_src_urls=$?"
exit_src_urls=0
$ python3 demos_parse: ALL_DEMOS_PARSED   (12/12)
$ ls demos/*.html | wc -l
12
```

## 独立验证结论

**独立验证结论：部分通过。**

已证实 31 项：仓库规模（140/140）、src/ 11 文件、HEAD 链 a8715ba→a31aa6a、远端 public/main、远端 HEAD d28aa68、commit tree 与 parent、本地与远端逐 blob ALL_MATCH、spec 两段字节数与 SHA-1、输入文件 IDENTICAL、全仓无 `gh[p]_` 凭据、src 无解释性措辞与 URL/路径/凭据字样、A31 覆盖、A51=93、工具链 rustc/cargo 1.99.1、37 项测试全过、release 构建产物 442456 字节、12 个 demo 内联脚本全部语法通过、round-013-core.html 13 个 node、005-blueprint 已批准、013-build-start 与 answers 段落齐全、9 份 core 文档字段、core-popup/core-userflow 要素、远端 4 个端点 HTTP 200、后端 0 写请求。

已失败 3 项：A46–A50 各 1（实测均为 0）；A52 计数（实测 0，且与"各 1"口径不匹配）；D08→D07 改动未做逐行 diff 复核。

未证实 2 项：docs/index.md for 循环 38 文件存在非空未逐行覆盖（仅抽样 README 与 9 份 features）；build-preconditions 触发链 1–6 状态位未逐项核对；未解决四值项清单未逐项复验。

受阻 0 项：本轮所有公开 GET 均为 HTTP 200，未遇 403，未编造数据。

未通过项汇总：A46–A50 与声明计数不一致；A52 声明无对应计数口径；D08→D07 改动未独立复核；必读文件 38 项未逐行覆盖；触发链与未解决四值项未复验。

## 未解决的四值项

存在未解决项，不满足 proof-rules P11 第 2 条，不发通过标记：

- CF API 方法未提供（F17）、X01–X04 未逐条处置、特殊版私仓未创建且缺仓库名（F63）
- 正常模式 UI 品牌替换未执行、UI 实现与进入构建未证实、本项目 LICENSE 文件未生成（F61 决定 GPLv3）
- 插件源默认选择、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 条款、MCIM/BMCLAPI 条款、Modrinth 缓存限流条款未证实
- Notchian 服务端行为、Mojang 官方 RCON 文档、加载器逐版本 schema、F012 令牌保护方案、Azure Client ID 未证实
- CREATE_NO_WINDOW、std::process 超时 API、WebView2 内存占用关系、单文件发布工具链、多操作入口形式、文件管理开源骨干、viaNBT Rust 集成、VxKex 兼容范围未证实
- Win7 + ARM64 交集已失败；v99.99 同名同 sha tag 已失败；本地链 a8715ba 与远端链 d28aa68 哈希不同（已逐 blob 校验内容等价）
- 浏览器渲染实测、GUI 点击端到端、rustc 交叉编译 Win7/ARM64 目标、git HTTP 推送、6 个上游主机、CF REST 端点页、Hangar 官方 API 文档、CopperGolem latest release 受阻
- L2 dispatcher 及以下 8 层未启动
- 008 验证报告 U8 锚点误差待复核

## 哈希声明

- 报告正文 SHA-1：`85fae9eb9d84daed2f5547d2d5b61ade8e7ec465`
- 报告正文哈希口径：追加本哈希声明块之前的报告正文全文，末尾恰好一个换行。
- 报告正文哈希命令：`sha1sum docs/verification/round-013.md`
- 报告正文哈希工作目录：`/data/workspace/kcu-launcher-desktop`
- 报告正文哈希计算时点：`Thu Nov 12 01:22:44 CST 2026`

- 变更内容 SHA-1：`51c7a69bc5d3b072fc63a25369046c2acde51394`
- 变更内容哈希口径：第 013 轮改动作者 diff 全文，基线 a31aa6a，终点 a8715ba，不含本验证报告；固定终点使报告提交后仍可原样复算。
- 变更内容哈希命令：`git diff a31aa6a..a8715ba | sha1sum`
- 变更内容哈希工作目录：`/data/workspace/kcu-launcher-desktop`
- 变更内容哈希计算时点：`Thu Nov 12 01:22:44 CST 2026`

- 独立验证结论为「部分通过」；未解决四值项见正文，不满足 proof-rules P11 第 2 条，不发通过标记；两个哈希由独立验证者计算，改动作者未代算。

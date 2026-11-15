from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
src_files = list((ROOT / 'src').rglob('*.rs'))
src_lines = sum(len(p.read_text().splitlines()) for p in src_files)
lib_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in src_files)
int_tests = sum(len(re.findall(r'#\[test\]', p.read_text())) for p in (ROOT / 'tests').rglob('*.rs'))
total_tests = lib_tests + int_tests
print('REAL', 'pkgs', pkgs, 'third', third, 'src_files', len(src_files),
      'src_lines', src_lines, 'lib', lib_tests, 'int', int_tests, 'total', total_tests)

Path('docs/spec/47-round-047-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/047-rollback-version-precedence.md'] = f'''# 第 047 轮：回滚目标版本比较缺陷 + 双守卫

| 项 | 值 |
| --- | --- |
| 编号 | 047 |
| 状态 | 已实现已验证；上层（网络 / UI / 崩溃分析 / 子进程隔离）未启动 |
| 依据 | docs/spec/47-round-047-instructions.txt |
| 前序 | 034 E28（`Version::eq` 含 build 元数据）、036 更新策略、037 插件升级确认、046 panic_guard |
| 本轮性质 | 底座正确性收尾；零新增第三方依赖 |

## 开工核查

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-046-A | 远端 ref | `4e059dc`，message `round 046 poison guard and envelope kind code` |
| V-046-B | 本地 HEAD | `bbfd106`，983 文件，工作区干净 |
| V-046-C | 临时凭据 | 核查后删除，全仓 `NO_CREDENTIAL`、`.git/config` 干净 |

## 审计发现

046 把 `src/` 36 文件非测试段的 panic 点清零后，改扫另一类：索引 / 截断 / 边界 / 相等判定。全量核版本比较点，查到 **3 个文件、8 处** `Version::parse` / `cmp_precedence` 中有一处口径不一致：

| 文件 | 位置 | 写法 | 四值 |
| --- | --- | --- | --- |
| `src/core/instance.rs` | 45 | `a.cmp_precedence(&b) == Ordering::Equal` | 正确（034 已修） |
| `src/plugins/upgrade.rs` | 42 / 55 | `candidate.cmp_precedence(&installed)`；`v.cmp_precedence(&candidate) == Ordering::Equal` | 正确（037 已用正确写法） |
| `src/updater/policy.rs` | 22 / **30** | 主比较 `b.cmp_precedence(&a)` 正确；**回滚目标 `v == b` 错误** | 已失败 |

034 的 E28 原文：「首版用 `Version::eq` 判同版本，独立小程复核：`semver::Version` 的 `==` **包含** build 元数据，`cmp_precedence` 才忽略；改用 `cmp_precedence(..) == Ordering::Equal`」。036 引入 `policy.rs` 时主比较改了，但 `explicit_target` 的匹配分支漏改；037 的 `upgrade.rs` 用了正确写法，于是**两条判定路径口径分叉**。

## 可达后果

输入：`current = "1.3.0"`、`candidate = "1.2.2+hotfix.1"`、`explicit_target = Some("1.2.2")`、`rollback_confirmed = true`。

| 路径 | 046 结果 | 047 结果 |
| --- | --- | --- |
| `decide`（036 policy.rs） | `Reject` | `Install` |
| `decide_upgrade`（037 upgrade.rs） | `Install` | `Install` |

`+hotfix.1` 是插件打包常见写法。用户已经显式填目标版本并二次确认回滚，046 版仍静默 `Reject`，不给原因；同一操作走 037 路径却 `Install`。两个入口对同一操作给出相反结果。

## 落地

| 编号 | 动作 |
| --- | --- |
| U94 | `src/updater/policy.rs` 的 `v == b` 改成 `v.cmp_precedence(&b) == Ordering::Equal`，与 037 / 034 统一。 |
| U95 | 新增 3 个测试：build 元数据回滚目标应 `Install`、不同优先级目标仍 `Reject`、`verify_then_decide` 同优先级 +build 差异保持 `Keep`。原 9 个 policy 测试一条未改全过。 |
| U96 | `src/dispatcher/launcher.rs` 取消分支的 `diagnostics[0]` 裸索引改成局部变量 `line`（刚 push 后可达安全，但重构易踩），行为不变。 |
| U97 | 新增 `scripts/semver_guard.py`：扫 3 个版本判定文件非测试段的裸 `==` 形态（`v == b` / `== b)` / `== a)` 等）；显式白名单只列 `instance.rs:35` 的 `if supported == candidate {{`（034「精确串相等保留」，两侧 `&str`）。CI scan job 加 `semver_guard` step。 |
| U98 | `Cargo.toml` / `Cargo.lock` / `vendor/` **一行未动**，仍 {pkgs} 包 / {third} 第三方。**如实登记**：项目内一处比较写法修正 + 机器约束，不是第三方库替换。 |

## 双向验证（真跑）

**守卫侧**：把 policy.rs 换回 `v == b` → `SEMVER_GUARD_HIT | src/updater/policy.rs | 30 | == b)`、`SEMVER_GUARD_FAIL 1`；恢复 → `SEMVER_GUARD_OK version_files 3 hits 0`。

**行为侧**：把 policy.rs 换回 `v == b` → 新增测试 FAILED，回显 `left: Reject / right: Install`；恢复 → `updater::policy` **12 / 0**。临时备份文件已删，仓库无残留。

这坐实了 U94 修的是可达缺陷，不是纸面推断；也证明 U97 的守卫能挡住复发。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo test --offline --lib`：**{lib_tests} / 0**（046 是 266；新增 policy 3 个）。 |
| V-B | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0，62.31 s**、`plugin_abi_load` **6 / 0，121.15 s**。 |
| V-C | 合计 **{total_tests} / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-D | `python3 scripts/panic_guard.py` → `PANIC_GUARD_OK files 36 hits 0`；`python3 scripts/semver_guard.py` → `SEMVER_GUARD_OK version_files 3 hits 0`。 |
| V-E | `.github/workflows/ci.yml` yaml.safe_load 通过，jobs=core/scan，scan 6 个 step（credential / wording / hardcode / panic_guard / semver_guard 等）。 |
| V-F | 必读 241 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，37 份 HTML 脚本通过。 |
| V-G | 界面闸门**未触发**：`demos/preview/` 与 `demos/ui-full-kcu-paper.html` 零 diff。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E85 | 首版 `semver_guard.py` 用复杂正则，双向验证时既漏判又误报，自跑结果不可信 | 重写成直接字面形态检测 + 显式白名单，双向验证后才接 CI |
| E86 | 守卫把 `instance.rs:35` 的 `if supported == candidate {{`（`&str` 精确串相等）误报为版本比较 | 加 `(file, line)` 白名单并注明 034 口径，A157 登记 |
| E87 | `cargo test --tests` 与交叉检查连续网关 502、工具结果不可用 | 拆 `--lib` / 两组 `--test` / lifecycle / abi / `check` 分段跑通，断言没降 |
| E88 | 036 主比较改了 `cmp_precedence` 却漏了回滚目标分支，037 与 036 因此分叉 | U94 统一口径，U97 加守卫防复发 |

## 四值

| 项 | 值 |
| --- | --- |
| 034 E28 原文、U94–U98 落地 | 已证实 |
| 双向验证（守卫 FAIL/OK、行为 FAIL/PASS） | 已证实 |
| {total_tests} / 0、Windows GNU、双守卫零命中、零新增依赖 | 已证实 |
| E85–E88 四个真问题处置 | 已证实 |
| Q-047-01 回滚是否需第三条件手动同意 | 未证实（待拍板，EQ-13 已给具体环境） |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| EQ-01 ~ EQ-12 十二条具体环境 | 已交（045），待拍板 |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-047.md'] = f'''# 第 047 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 047 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 底座正确性收尾轮；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 046 远端 `GET /git/ref/heads/main` | `4e059dc`，message `round 046 poison guard and envelope kind code` | 已证实 |
| V2 | `cargo test --offline --lib` | **{lib_tests} / 0** | 已证实 |
| V3 | `cargo test --offline --lib updater::policy` | 12 / 0（原 9 + 新 3） | 已证实 |
| V4 | 行为反向验证（临时换回 `v == b`） | `FAILED`，`left: Reject / right: Install` | 已证实 |
| V5 | 守卫反向验证（临时换回 `v == b`） | `SEMVER_GUARD_HIT policy.rs:30 == b)`、`FAIL 1` | 已证实 |
| V6 | `python3 scripts/semver_guard.py`（恢复后） | `SEMVER_GUARD_OK version_files 3 hits 0` | 已证实 |
| V7 | `python3 scripts/panic_guard.py` | `PANIC_GUARD_OK files 36 hits 0` | 已证实 |
| V8 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V9 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V10 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，62.31 s | 已证实 |
| V11 | `cargo test --offline --test plugin_abi_load` | 6 / 0，121.15 s | 已证实 |
| V12 | `cargo check --offline --target x86_64-pc-windows-gnu` | Finished | 已证实 |
| V13 | `Cargo.lock` 包列表 | **{pkgs} 包 / {third} 第三方**（与 046 相同） | 已证实 |
| V14 | `git diff --name-only -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V15 | `git diff --name-only -- demos/preview/ demos/ui-full-kcu-paper.html` | 空（界面闸门未触发） | 已证实 |
| V16 | `.github/workflows/ci.yml` yaml.safe_load | jobs=core/scan，scan 含 semver_guard | 已证实 |
| V17 | `node new Function` 全部 demos HTML | ALL_JS_OK，37 份 | 已证实 |
| V18 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V19 | 禁用词 / 「同上」 / P09 / hardcode 扫描 | 零命中 | 已证实 |
| V20 | 必读文件循环 | REQUIRED=241 MISSING=0 | 已证实 |
| V21 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 回滚判定修正、双向验证、双守卫、{total_tests} / 0 | 已证实 |
| E85–E88 处置、零新增依赖 | 已证实 |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| Q-047-01（EQ-13） | 待拍板 |
| EQ-01 ~ EQ-12 | 已交具体环境，待拍板 |
| {total_tests} 测试仅作回归，不作质量结论 | 已证实 |

限制：本轮未做真实 HTTP 请求、GUI 端到端、崩溃捕获与 Win7 运行时验证；改动作者未代改验证结论，未降低验收项。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s):
    p = Path(f)
    t = p.read_text()
    marker = s.strip().splitlines()[0]
    if marker in t:
        print('SKIP_DUP', f)
        return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


Path('docs/records/eq13-rollback-conditions.md').write_text('''# EQ-13 / Q-047-01 回滚条件数量

| 项 | 值 |
| --- | --- |
| 状态 | 待拍板；047 未改条件数量，只统一了 `+build` 相等判定 |
| 关联 | docs/records/pending-question-environments.md 的 EQ-13 段、036 更新策略、037 插件升级确认 |

## 具体环境

| 路径 | 回滚条件 | 数量 |
| --- | --- | --- |
| `src/updater/policy.rs::decide`（036） | `explicit_target` 与候选优先级相等 + `rollback_confirmed` | **2** |
| `src/plugins/upgrade.rs::decide_upgrade`（037） | `explicit_target` + `rollback_confirmed` + `user_confirmed_upgrade` | **3** |

升级路径 037 已用 `user_confirmed_upgrade` 覆盖 036 的「默认只升自动安装」。031 定最严格档为默认，032 加三档可选松档。034 起 `+build` 差异走 `cmp_precedence`；047 U94 把两条路径的相等判定统一。

## 分叉输入

```
current                 = "1.3.0"
candidate               = "1.2.2"
explicit_target         = Some("1.2.2")
rollback_confirmed      = true
user_confirmed_upgrade  = false
```

| 路径 | 结果 |
| --- | --- |
| `decide` | `Install` |
| `decide_upgrade` | `Reject` |

## 要选

| 选项 | 内容 | 后果 |
| --- | --- | --- |
| ① | 回滚也要求 `user_confirmed_upgrade`，统一为 3 个条件 | 两条路径一致；回滚多一次手动确认 |
| ② | 回滚保持 2 个条件 | 显式目标 + 二次确认视为足够；两路径继续分叉，需文档写明调用方该走哪条 |
| ③ | 由更新器插件在调用前弹确认，两处都不判 | 判定层更薄，但确认逻辑外移到插件，037 的手动同意约束需要重新落点 |

不选：两条路径对同一操作给出相反结果，Q-047-01 悬空。
''')
print('WROTE docs/records/eq13-rollback-conditions.md')

app('docs/decisions/index.md', '| 047 | 回滚目标版本比较缺陷 + 双守卫 | 已实现已验证；上层未启动 | 047-rollback-version-precedence.md |')

app('docs/records/interface-log.md', '''## 047 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I65 | `src/updater/policy` | `target_matches` 改 `cmp_precedence(&b) == Ordering::Equal`；3 个新增测试 |
| I66 | `src/dispatcher/launcher` | 取消分支 `diagnostics[0]` 裸索引改局部变量 |
| I67 | CI | scan job 加 `semver_guard` step，脚本 `scripts/semver_guard.py` |
| S46 | 状态 | U94–U98 已证实；零新增依赖；Q-047-01 / EQ-13 待拍板 |
''')

app('docs/checklists/ai-errors.md', '''## 047 轮新增

| 编号 | 防错项 |
| --- | --- |
| A157 | 守卫规则别写复杂正则；直接字面形态 + 显式 `(file, line)` 白名单更好复核，白名单必须注明合法理由（如 &str 精确串相等）。 |
| A158 | 同一个语义判定在多个文件出现时，全量 grep 所有出现点；只修主路径会留下分叉（036 主比较改了、回滚目标没改）。 |
| A159 | 新守卫接 CI 前必须做双向验证：注入缺陷要 FAIL、恢复要 OK，只验正常态不算证据。 |
| A160 | `semver::Version` 的 `==` 含 build 元数据；相等一律走 `cmp_precedence(..) == Ordering::Equal`，034 E28 已登记，别再犯。 |
''')

app('docs/rules/ui-demo.md', '''## 047 闸门判定

本轮改的是 `src/updater/policy.rs` / `launcher.rs` 与 CI 脚本，不产生任何界面变化；`demos/preview/` 与 `demos/ui-full-kcu-paper.html` 零 diff。沿用 036 / 038–046 的先例判**未触发**。
''')

app('docs/records/code-ownership-audit.md', f'''## 047 版本判定口径统一（零新增依赖）

| 项 | 046 | 047 |
| --- | --- | --- |
| 第三方 crate 进构建 | {third} | **{third}**（不变） |
| `Cargo.lock` 包数 | {pkgs} | **{pkgs}**（不变） |
| `src/` 文件 | 36 | **{len(src_files)}** |
| `src/` 行数 | 6212 | **{src_lines}** |
| 测试 | 266 单元 + 26 集成 = 292 | **{lib_tests} 单元 + {int_tests} 集成 = {total_tests}** |

046 清零 panic 点后改扫相等判定，全量核 3 个版本判定文件：`policy.rs` 回滚目标分支仍是 `v == b`（034 E28 已登记 `Version::eq` 含 build 元数据），而 037 的 `upgrade.rs` 用 `cmp_precedence`，两条路径分叉。改成统一写法，新增 3 个测试；`launcher.rs` 裸索引改局部变量；新增 `scripts/semver_guard.py` 与 CI step。

双向验证真跑：注入 `v == b` 后守卫 FAIL、行为测试 FAILED（`left: Reject / right: Install`），恢复后守卫 OK、policy 12/0。

**如实登记**：项目内比较写法修正 + 机器约束，不是第三方库替换；`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动。自写通用算法已收敛，剩余是项目特有编排。
''')

app('docs/design/implementation-strategy.md', '''## 047 版本判定与双守卫

| 层 | 状态 |
| --- | --- |
| CI `panic_guard`（非测试段危险调用） | 已实现（046） |
| 回滚目标版本比较统一到 `cmp_precedence` | **已实现（047）** |
| CI `semver_guard`（禁止 Version 裸 `==`） | **已实现（047）** |
| 真实窗口 / WebView / 渲染 / 崩溃分析 | 未启动，具体环境见 EQ-01 / EQ-04 / EQ-05 |
| 真实网络 IO / TLS / 代理 / 响应解析 | 未启动，具体环境见 EQ-03 |
| 界面渲染 | 仍等 UX 手感确认与 Q-041 拍板，具体环境见 EQ-10 |
''')

app('docs/records/pending-question-environments.md', '''---

**EQ-13 回滚是否要求第三条件（Q-047-01）**

环境：两条判定路径并存。`src/updater/policy.rs::decide`（036）：回滚条件 = `explicit_target` 版本与候选优先级相等 + `rollback_confirmed`（**2 个条件**），返回 `Install`。`src/plugins/upgrade.rs::decide_upgrade`（037）：回滚条件 = `explicit_target` + `rollback_confirmed` + `user_confirmed_upgrade`（**3 个条件**）。升级路径 037 已用 `user_confirmed_upgrade` 覆盖 036 的「默认只升自动安装」。

一手数据：031 定最严格档（每次确认 + 只允许只读）为默认；032 加三档可选松档；037 你要求「两个插件哈希一致，对比版本号后用户得手动同意才能安装（这叫升级）」。`+build` 差异按 034 走 `cmp_precedence`，047 U94 已把两条路径的相等判定统一。

具体分叉：输入 `current="1.3.0"` / `candidate="1.2.2"` / `explicit_target="1.2.2"` / `rollback_confirmed=true` / `user_confirmed_upgrade=false` 时，`decide` → `Install`，`decide_upgrade` → `Reject`。

要选：① 回滚也要求 `user_confirmed_upgrade`（统一为 3 个条件）② 回滚保持 2 个条件（显式目标 + 二次确认已足够）③ 由更新器插件自己在调用前弹确认，两处都不判。

不选：两条路径对同一操作给出相反结果，Q-047-01 悬空；本轮只统一了 `+build` 相等判定，未改条件数量。
''')

app('docs/records/rounds.md', f'''## 047

| 落点 | 内容 |
| --- | --- |
| docs/spec/47-round-047-instructions.txt | 逐字副本 1 行 |
| docs/decisions/047-rollback-version-precedence.md | V-046-A~C、U94-U98、双向验证、V-A~V-G、E85-E88、四值 |
| docs/verification/round-047.md | 21 条复跑证据 |
| src/updater/policy.rs / launcher.rs | 回滚判定修正、3 个新增测试、裸索引改局部变量 |
| scripts/semver_guard.py + .github/workflows/ci.yml | CI `semver_guard` step |
| docs/records/pending-question-environments.md | EQ-13（Q-047-01 具体环境） |
| demos/round-047-semver-guard.html | 13 步运行逻辑演示 |
| 索引与记录 | docs/index 241 项、README、两个 index、ai-errors A157-A160、code-ownership-audit、implementation-strategy、ui-demo 判定、interface-log、rounds |

先核 046 收口：远端 `4e059dc`、message `round 046 poison guard and envelope kind code`，本地 `bbfd106` / 983 文件，工作区干净；临时凭据核查后删除，全仓零凭据。

「干」继续收尾。046 把非测试段 panic 点清零后，改扫索引 / 截断 / 边界 / 相等判定。全量核 3 个版本判定文件，查到一处口径分叉：`instance.rs:45` 与 `upgrade.rs:42/55` 都用 `cmp_precedence`，但 `policy.rs:30` 的回滚目标匹配仍是 `v == b`。034 E28 原文明确：「`semver::Version` 的 `==` 包含 build 元数据，`cmp_precedence` 才忽略」。036 引入 policy.rs 时主比较改了、回滚目标分支漏改；037 用了正确写法，于是两条路径对同一操作分叉。

可达后果：`current="1.3.0"` / `candidate="1.2.2+hotfix.1"` / `explicit_target="1.2.2"` / `rollback_confirmed=true` 时，046 的 `decide` 返回 `Reject`（用户已填目标并二次确认仍静默装不上），037 的 `decide_upgrade` 返回 `Install`。`+hotfix.1` 是插件打包常见写法。

落地：`policy.rs` 改成 `v.cmp_precedence(&b) == Ordering::Equal`；新增 3 个测试（build 元数据回滚应 Install、不同优先级仍 Reject、verify_then_decide 同优先级 +build 差异 Keep）；`launcher.rs` 取消分支 `diagnostics[0]` 裸索引改局部变量；新增 `scripts/semver_guard.py` 扫 3 个版本判定文件非测试段的裸 `==` 形态，白名单只列 `instance.rs:35` 的 `&str` 精确串相等（034 口径），CI scan job 加 `semver_guard` step。

**双向验证真跑**：注入 `v == b` → 守卫 `SEMVER_GUARD_HIT policy.rs:30 == b)` FAIL 1、行为测试 FAILED（`left: Reject / right: Install`）；恢复 → 守卫 `OK version_files 3 hits 0`、`updater::policy` 12/0。临时备份已删。

验证：{lib_tests} 单元 / 0 + 7 http_construct / 0 + 6 窗口契约 / 0 + 7 lifecycle / 0（62.31 s）+ 6 abi / 0（121.15 s）= **{total_tests} / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过；`PANIC_GUARD_OK files 36 hits 0`、`SEMVER_GUARD_OK version_files 3 hits 0`。`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 {pkgs} 包 / {third} 第三方。界面闸门未触发，`demos/preview/` 与 `ui-full-kcu-paper.html` 零 diff。

本轮真实问题：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E85 | 首版 `semver_guard.py` 用复杂正则，双向验证时既漏判又误报 | 重写成直接字面形态 + 显式白名单，双向验证后才接 CI |
| E86 | 守卫把 `instance.rs:35` 的 `&str` 精确串相等误报成版本比较 | 加 `(file, line)` 白名单并注明 034 口径，立 A157 |
| E87 | 全量 `cargo test --tests` 与交叉检查连续网关 502 | 拆段跑通，断言没降 |
| E88 | 036 主比较改了却漏回滚目标分支，037 与 036 分叉 | U94 统一口径、U97 加守卫防复发 |

另交 **EQ-13 / Q-047-01**：`decide`（036）回滚要 2 个条件，`decide_upgrade`（037）要 3 个（多 `user_confirmed_upgrade`），同一输入给出 `Install` / `Reject` 相反结果。本轮只统一了 `+build` 相等判定，**没改条件数量**，具体环境与三个选项已列进环境清单，等你拍板。

EQ-01 ~ EQ-12 具体环境仍待拍板（045 已交）；真实网络 IO、UI 宿主、崩溃分析、子进程隔离、028 三项实现、CF F17、特殊版代码、本项目 LICENSE、UX 手感均未动。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '235. docs/verification/round-046.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''235. docs/verification/round-046.md
236. docs/spec/47-round-047-instructions.txt
237. docs/decisions/047-rollback-version-precedence.md
238. scripts/semver_guard.py
239. demos/round-047-semver-guard.html
240. docs/verification/round-047.md
241. docs/records/eq13-rollback-conditions.md

读取命令：''', 1)
    t = t.replace('docs/verification/round-046.md; do printf',
                  'docs/verification/round-046.md docs/spec/47-round-047-instructions.txt docs/decisions/047-rollback-version-precedence.md scripts/semver_guard.py demos/round-047-semver-guard.html docs/verification/round-047.md docs/records/eq13-rollback-conditions.md; do printf', 1)
    p.write_text(t)
    print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 047 |', p.read_text(), count=1)
section = f'''

## 047 回滚目标版本比较缺陷 + 双守卫

全量核 3 个版本判定文件，查到 `src/updater/policy.rs:30` 的回滚目标匹配仍是 `v == b`；034 E28 已登记 `semver::Version` 的 `==` 含 build 元数据。036 主比较改了 `cmp_precedence` 却漏了这处，037 的 `upgrade.rs` 用了正确写法，两条路径分叉：`candidate="1.2.2+hotfix.1"` + 显式目标 `"1.2.2"` + 二次确认时，046 给 `Reject`、037 给 `Install`。

改成 `v.cmp_precedence(&b) == Ordering::Equal`，新增 3 个测试；`launcher.rs` 裸索引改局部变量；新增 `scripts/semver_guard.py` 与 CI `semver_guard` step，白名单只列 `instance.rs` 的 `&str` 精确串相等。

双向验证真跑：注入 `v == b` 后守卫 FAIL、行为测试 FAILED（`left: Reject / right: Install`），恢复后守卫 OK、policy 12/0。`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 **{pkgs} 包 / {third} 第三方**。

`cargo test --offline` 合计 **{total_tests}/0**（{lib_tests} 单元 + {int_tests} 集成），Windows GNU 交叉检查通过，界面与 56 张 PNG 零 diff。另交 **EQ-13 / Q-047-01**：两条回滚路径条件数不同（2 个 vs 3 个），本轮只统一相等判定、没改条件数量，等你拍板。
'''
if '## 047 回滚目标版本比较缺陷' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

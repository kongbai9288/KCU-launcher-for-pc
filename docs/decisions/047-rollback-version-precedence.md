# 第 047 轮：回滚目标版本比较缺陷 + 双守卫

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
| U97 | 新增 `scripts/semver_guard.py`：扫 3 个版本判定文件非测试段的裸 `==` 形态（`v == b` / `== b)` / `== a)` 等）；显式白名单只列 `instance.rs:35` 的 `if supported == candidate {`（034「精确串相等保留」，两侧 `&str`）。CI scan job 加 `semver_guard` step。 |
| U98 | `Cargo.toml` / `Cargo.lock` / `vendor/` **一行未动**，仍 26 包 / 25 第三方。**如实登记**：项目内一处比较写法修正 + 机器约束，不是第三方库替换。 |

## 双向验证（真跑）

**守卫侧**：把 policy.rs 换回 `v == b` → `SEMVER_GUARD_HIT | src/updater/policy.rs | 30 | == b)`、`SEMVER_GUARD_FAIL 1`；恢复 → `SEMVER_GUARD_OK version_files 3 hits 0`。

**行为侧**：把 policy.rs 换回 `v == b` → 新增测试 FAILED，回显 `left: Reject / right: Install`；恢复 → `updater::policy` **12 / 0**。临时备份文件已删，仓库无残留。

这坐实了 U94 修的是可达缺陷，不是纸面推断；也证明 U97 的守卫能挡住复发。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo test --offline --lib`：**269 / 0**（046 是 266；新增 policy 3 个）。 |
| V-B | `http_construct` **7 / 0**、`window_handle_contract` **6 / 0**、`plugin_lifecycle_load` **7 / 0，62.31 s**、`plugin_abi_load` **6 / 0，121.15 s**。 |
| V-C | 合计 **295 / 0**；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-D | `python3 scripts/panic_guard.py` → `PANIC_GUARD_OK files 36 hits 0`；`python3 scripts/semver_guard.py` → `SEMVER_GUARD_OK version_files 3 hits 0`。 |
| V-E | `.github/workflows/ci.yml` yaml.safe_load 通过，jobs=core/scan，scan 6 个 step（credential / wording / hardcode / panic_guard / semver_guard 等）。 |
| V-F | 必读 241 项非空，凭据 / 禁用词 / `同上` / P09 / hardcode 全零命中，37 份 HTML 脚本通过。 |
| V-G | 界面闸门**未触发**：`demos/preview/` 与 `demos/ui-full-kcu-paper.html` 零 diff。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E85 | 首版 `semver_guard.py` 用复杂正则，双向验证时既漏判又误报，自跑结果不可信 | 重写成直接字面形态检测 + 显式白名单，双向验证后才接 CI |
| E86 | 守卫把 `instance.rs:35` 的 `if supported == candidate {`（`&str` 精确串相等）误报为版本比较 | 加 `(file, line)` 白名单并注明 034 口径，A157 登记 |
| E87 | `cargo test --tests` 与交叉检查连续网关 502、工具结果不可用 | 拆 `--lib` / 两组 `--test` / lifecycle / abi / `check` 分段跑通，断言没降 |
| E88 | 036 主比较改了 `cmp_precedence` 却漏了回滚目标分支，037 与 036 因此分叉 | U94 统一口径，U97 加守卫防复发 |

## 四值

| 项 | 值 |
| --- | --- |
| 034 E28 原文、U94–U98 落地 | 已证实 |
| 双向验证（守卫 FAIL/OK、行为 FAIL/PASS） | 已证实 |
| 295 / 0、Windows GNU、双守卫零命中、零新增依赖 | 已证实 |
| E85–E88 四个真问题处置 | 已证实 |
| Q-047-01 回滚是否需第三条件手动同意 | 未证实（待拍板，EQ-13 已给具体环境） |
| 真实网络 IO / TLS / UI 宿主 / 崩溃分析 / 子进程隔离 | 未启动 |
| EQ-01 ~ EQ-12 十二条具体环境 | 已交（045），待拍板 |
| 后端仓写请求 | 0（已证实） |

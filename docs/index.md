# 文档索引

检索日期：2026-11-12
更新轮次：014

## 每轮开工必读顺序

1. docs/spec/00-requirements.txt
2. docs/spec/01-round-001-instructions.txt
3. docs/spec/02-round-002-instructions.txt
4. docs/spec/03-round-003-instructions.txt
5. docs/spec/04-round-004-instructions.txt
6. docs/spec/05-round-005-instructions.txt
7. docs/spec/06-round-006-instructions.txt
8. docs/spec/07-round-007-instructions.txt
9. docs/spec/08-round-008-instructions.txt
10. docs/spec/09-round-009-instructions.txt
11. docs/spec/10-round-010-instructions.txt
12. docs/spec/11-round-011-instructions.txt
13. docs/spec/11-features-input.txt
14. docs/spec/12-round-012-instructions.txt
15. docs/spec/12-server-features-input.txt
16. docs/checklists/ai-errors.md
17. docs/checklists/windows-errors.md
18. docs/rules/proof-rules.md
19. docs/rules/fallback-rules.md
20. docs/rules/push-scope.md
21. docs/rules/build-preconditions.md
22. docs/research/index.md
23. docs/features/index.md
24. docs/records/rounds.md
25. docs/records/open-questions.md
26. docs/features/backlog.md
27. docs/features/server-backlog.md
28. docs/research/16-server-platform.md
29. docs/decisions/012-server-input.md
30. docs/spec/13-round-013-instructions.txt
31. docs/spec/13-round-013-instructions-part2.txt
32. docs/records/round-013-answers.md
33. docs/decisions/013-build-start.md
34. Cargo.toml
35. src/lib.rs
36. src/core/mod.rs
37. docs/features/core-userflow.md
38. docs/features/core-popup.md
39. docs/spec/14-round-014-instructions.txt
40. docs/decisions/014-build-continue.md
41. .github/workflows/ci.yml
42. docs/features/core-cache.md
43. docs/features/core-asynk.md
44. docs/features/core-leak.md

读取命令：

```
cd /data/workspace/kcu-launcher-desktop
for f in docs/spec/00-requirements.txt docs/spec/01-round-001-instructions.txt docs/spec/02-round-002-instructions.txt docs/spec/03-round-003-instructions.txt docs/spec/04-round-004-instructions.txt docs/spec/05-round-005-instructions.txt docs/spec/06-round-006-instructions.txt docs/spec/07-round-007-instructions.txt docs/spec/08-round-008-instructions.txt docs/spec/09-round-009-instructions.txt docs/spec/10-round-010-instructions.txt docs/spec/11-round-011-instructions.txt docs/spec/11-features-input.txt docs/spec/12-round-012-instructions.txt docs/spec/12-server-features-input.txt docs/checklists/ai-errors.md docs/checklists/windows-errors.md docs/rules/proof-rules.md docs/rules/fallback-rules.md docs/rules/push-scope.md docs/rules/build-preconditions.md docs/research/index.md docs/features/index.md docs/records/rounds.md docs/records/open-questions.md docs/features/backlog.md docs/features/server-backlog.md docs/research/16-server-platform.md docs/decisions/012-server-input.md docs/spec/13-round-013-instructions.txt docs/spec/13-round-013-instructions-part2.txt docs/records/round-013-answers.md docs/decisions/013-build-start.md Cargo.toml src/lib.rs src/core/mod.rs docs/features/core-userflow.md docs/features/core-popup.md docs/spec/14-round-014-instructions.txt docs/decisions/014-build-continue.md .github/workflows/ci.yml docs/features/core-cache.md docs/features/core-asynk.md docs/features/core-leak.md; do printf '%s %s\n' "$f" "$(wc -l < "$f")"; done
```

## 分区

| 分区 | 入口 | 职责 |
| --- | --- | --- |
| 需求规格 | docs/spec/00-requirements.txt | 需求原文 |
| 011 功能输入 | docs/spec/11-features-input.txt | 55 条编号功能与 175 项文件管理清单逐字副本 |
| 012 开服器输入 | docs/spec/12-server-features-input.txt | 开服器编号功能与分节条目逐字副本 |
| 待拍板问题全集 | docs/records/open-questions.md | 93 条，A-H 组，013 轮已答复 |
| 013 答复台账 | docs/records/round-013-answers.md | 76 片段逐字编号、语义映射、不写死项 |
| 013 开工决策 | docs/decisions/013-build-start.md | D06/D07、工具链纠正、G 组默认、H 组硬要求 |
| Rust crate | Cargo.toml | std only，profile 默认值已核实 |
| L1 core 源码 | src/ | 12 个模块，56 个单元测试 |
| L1 功能登记 | docs/features/core-*.md | 12 份，字段固定五段 |
| 014 决策 | docs/decisions/014-build-continue.md | 私仓、secrets 占位、样板化 UX、缓存异步泄漏防护 |
| CI 工作流 | .github/workflows/ci.yml | secrets / vars 占位、有界缓存、并发取消、并行 job |
| 特殊版私仓 | kongbai9288/KCU-launcher-special | private，仅 README 占位，代码待用户同意 |
| 调研 | docs/research/index.md | 外部事实、锚点、四值 |
| 合规与阻塞项 | docs/research/12-compliance.md | API 条款、凭据保护、许可证全文、上游版本、X01-X07 |
| 系统 API 与平台 | docs/research/13-platform-api.md | Win7、多架构、版本/架构/位置 API、Rust 目标冲突 |
| 网络通用法 | docs/research/14-batch-network.md | 批量端点、N+1 反模式、回环监听、配置集中 |
| 外部项目核实 | docs/research/15-input-survey.md | 只读后端仓、CopperGolemLauncher、ViaNBT、dsh、VxKex |
| 开服器官方资料 | docs/research/16-server-platform.md | 插件源、mrpack、EULA、原版命令、Java 版本、ops.json、种子 NBT、icon、UPnP、mclo.gs |
| 底层运行时调研 | docs/research/11-runtime.md | Cargo profile、DLL 搜索、进程管理、WebView2 进程组、目标三元组、MSVC 部署 |
| 许可证原文 | docs/licenses/index.md | 逐字副本与 slint 三许可全文 |
| 功能登记 | docs/features/index.md | F001-F012；011 输入见 backlog.md；012 输入见 server-backlog.md |
| 决策 | docs/decisions/index.md | 状态分层记录 |
| 防错 | docs/checklists/ | AI 与 Windows 防错清单 |
| 规则 | docs/rules/ | 四值判决、兜底分级、推送范围、搭建前置条件 |
| 记录 | docs/records/ | 版本、接口、轮次、问题全集 |
| 验证 | docs/verification/ | 独立验证报告 |
| UI 资产 | assets/ui/index.md | 正常模式 UI 逐字副本与结构登记 |
| 图标资产 | assets/icon/kcu-launcher.jpg | 启动器图标原始字节 |
| 演示 | demos/round-001-dispatch.html | 统一调度器运行逻辑 |
| 演示 | demos/round-002-icon.html | 图标资产登记运行逻辑 |
| 演示 | demos/round-003-remote.html | 远端推送与搭建阶段运行逻辑 |
| 演示 | demos/round-004-remote.html | 公仓创建与 API 快照推送运行逻辑 |
| 演示 | demos/round-006-closeout.html | 005 收口与 006 交付运行逻辑 |
| 演示 | demos/round-007-normal-ui.html | 正常模式 UI 与轻量分流运行逻辑 |
| 演示 | demos/round-008-mode-views.html | 模式视图登记与补证运行逻辑 |
| 演示 | demos/round-009-coverage.html | 需求覆盖与底层调研运行逻辑 |
| 演示 | demos/round-010-compliance.html | 合规阻塞与搭建前置运行逻辑 |
| 演示 | demos/round-011-input.html | 功能输入与硬冲突判定运行逻辑 |
| 演示 | demos/round-012-server-input.html | 开服器输入与 93 条问题闸门运行逻辑 |
| 演示 | demos/round-013-core.html | core 编译、用户操作模拟、11 类弹窗关闭逻辑 |
| 演示 | demos/round-014-cache-async.html | 缓存单飞、多源竞速取消、泄漏归零、工作流占位 |
| 脚本 | scripts/push.sh | 推送入口，自动降级 |
| 脚本 | scripts/api_push.py | Git Data API 全量树快照 |

## 远端

| 项 | 值 |
| --- | --- |
| 仓库 | kongbai9288/KCU-launcher-for-pc |
| 地址 | https://github.com/kongbai9288/KCU-launcher-for-pc |
| 可见性 | public |
| 分支 | main |
| 推送路径 | git HTTP 受阻；REST Git Data API 全量树快照 |
| 用户后端仓 | 只读，仅 GET，内容不进公仓 |
| 特殊版 | `kongbai9288/KCU-launcher-special`，private，014 轮已建仓，仅 README 占位 |
| 特殊版放代码条件 | 用户明确同意后，用户手拉工具流 |

## 每轮开工前检查

| 检查 | 命令 |
| --- | --- |
| 时间戳 | `TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'` |
| 网络时钟 | `curl -sSI -H 'User-Agent: KCU-Launcher-Desktop/0.0.0' https://api.github.com/rate_limit \| grep -i '^date:'` |
| 文档完整性 | 上方读取命令 |
| 凭据扫描 | `! grep -rqE 'gh[p]_' .` |
| 解释性措辞扫描 | `! grep -rE '为什么\|这意味着\|值得注意的是\|综上所述\|让我们看看' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| 中间态扫描 | `! grep -rE '部分已证实' docs/research/ docs/features/ docs/records/ docs/decisions/` |
| 重复引用扫描 | `! grep -rE '同上' docs/research/` |
| 品牌元素扫描 | `! grep -rE 'FCL\|揉纸启动器' src/` |
| 推广措辞扫描 | `! grep -rE '表现得最优\|使用人数最多\|社区反馈最积极' docs/features/ docs/decisions/` |
| 功能状态扫描 | `test -z "$(grep -L '未实现' docs/features/dispatcher.md docs/features/lightweight.md docs/features/headless.md docs/features/normal-launcher.md docs/features/lan.md docs/features/server.md docs/features/log.md docs/features/fallback.md docs/features/envelope.md docs/features/ui-framework.md docs/features/credential-guard.md)"` |
| 编号功能完整性 | `grep -cE '^\| [0-9]+ \|' docs/features/backlog.md` |
| 逐条目单发扫描 | `grep -n '每搜索一个模组' docs/spec/11-round-011-instructions.txt` |
| 物理位置口径扫描 | `grep -n 'GEOID_NOT_AVAILABLE' docs/research/13-platform-api.md` |
| Win7 目标扫描 | `grep -n 'require at least Windows 10' docs/research/13-platform-api.md` |
| 问题全集完整性 | `grep -cE '^\| Q-[A-H][0-9]' docs/records/open-questions.md` |
| 原版 `/talk` 扫描 | `grep -c '未出现' docs/research/16-server-platform.md` |
| ops.json 回写扫描 | `grep -c 'writes the whole list back' docs/research/16-server-platform.md` |
| src/ 空扫描（013 轮前） | `test -z "$(git ls-files src/)"`，013 轮起改为非空断言 |
| Rust 构建 | `cargo build --release --offline` |
| Rust 测试 | `cargo test --offline`，当前 56 passed / 0 failed |
| 弹窗关闭路径 | `cargo test --offline core::popup`，11 类全部可关 |
| 用户操作模拟 | `cargo test --offline core::userflow`，双击 / 指定 / 单参数 / 无残留 |
| 缓存有界与单飞 | `cargo test --offline core::cache`，8 passed，order ≤ capacity |
| 异步取消与回收 | `cargo test --offline core::asynk`，6 passed，live=0 |
| 泄漏归零 | `cargo test --offline core::leak`，5 passed |
| 工作流凭据 | `! grep -rE 'gh[p]_' .github/workflows/`，只写 secrets 引用 |
| 工作流语法 | `python3 -c "import yaml;yaml.safe_load(open('.github/workflows/ci.yml'))"` |
| 代码注释 | `! grep -rE '为了|目的是|方便用户|让用户能够|这样用户' src/` |

## 搭建前置条件

| 条件 | 012 值 | 013 值 |
| --- | --- | --- |
| D06 信号 | 未提供 | 已触发 F07/F08 |
| 005-blueprint.md | 未批准 | 已批准 F09 |
| X01-X04 用户拍板 | 未拍板 | F10 按正常情况与用户逻辑落地；CF 下载模块不在 L1 |
| Win7 兼容路径 | 未选 | Tier 3 + build-std F64 |
| 多架构范围 | 未定 | 全选；放弃 Win7 下 ARM64 F65/F66 |
| 地域判定口径 | 未定 | 物理位置 + 区域设置，软策略、只用于下载选择 F67/F52/F53 |
| 待拍板问题 93 条 | 未答复 | 已答复，细节按用户逻辑落地 |
| 开工时点 S1/S2 | 并列登记 | F07 判定「现在就是明天」，按 S1 开工 |
| src/ | 空 | L1 core 12 模块已落地（013 的 9 个 + 014 的 3 个） |
| 工具链 | rustc/cargo 受阻 | rustc / cargo 1.99.1，腾讯 rustup 镜像 |

详见 docs/rules/build-preconditions.md 条件 1-6 与 docs/decisions/013-build-start.md。

## 未写入项

- L2 dispatcher 及以下 8 层：未启动。
- 正常模式 UI 实现：014 轮定为样板参考、KCU 品牌重新实现，未进入构建。
- UI 设计稿品牌与字体：E09 卡点关闭，设计稿不直接复用。
- 图标 ICO 与裁切版本：未生成。
- 本项目 LICENSE：F61 决定 GPLv3，文件未生成。
- 特殊版私仓：已建仓，代码待用户明确同意后放入。
- 后端仓任何写请求：0。
- CF API 方法：workflow 设 secrets 占位，值由用户填写；具体调用方法 F17 由用户在完成时提供。
- 插件源默认选择、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 日志外传条款：未证实。
- 浏览器内渲染实测、GUI 点击端到端、rustc 交叉编译 Win7 目标：受阻。
- 011 遗留未证实项与 012 的 G 组默认：见 docs/decisions/013-build-start.md。

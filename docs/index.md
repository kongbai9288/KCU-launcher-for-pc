# 文档索引

检索日期：2026-11-11
更新轮次：012

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

读取命令：

```
cd /data/workspace/kcu-launcher-desktop
for f in docs/spec/00-requirements.txt docs/spec/01-round-001-instructions.txt docs/spec/02-round-002-instructions.txt docs/spec/03-round-003-instructions.txt docs/spec/04-round-004-instructions.txt docs/spec/05-round-005-instructions.txt docs/spec/06-round-006-instructions.txt docs/spec/07-round-007-instructions.txt docs/spec/08-round-008-instructions.txt docs/spec/09-round-009-instructions.txt docs/spec/10-round-010-instructions.txt docs/spec/11-round-011-instructions.txt docs/spec/11-features-input.txt docs/spec/12-round-012-instructions.txt docs/spec/12-server-features-input.txt docs/checklists/ai-errors.md docs/checklists/windows-errors.md docs/rules/proof-rules.md docs/rules/fallback-rules.md docs/rules/push-scope.md docs/rules/build-preconditions.md docs/research/index.md docs/features/index.md docs/records/rounds.md docs/records/open-questions.md docs/features/backlog.md docs/features/server-backlog.md docs/research/16-server-platform.md docs/decisions/012-server-input.md; do printf '%s %s\n' "$f" "$(wc -l < "$f")"; done
```

## 分区

| 分区 | 入口 | 职责 |
| --- | --- | --- |
| 需求规格 | docs/spec/00-requirements.txt | 需求原文 |
| 011 功能输入 | docs/spec/11-features-input.txt | 55 条编号功能与 175 项文件管理清单逐字副本 |
| 012 开服器输入 | docs/spec/12-server-features-input.txt | 开服器编号功能与分节条目逐字副本 |
| 待拍板问题全集 | docs/records/open-questions.md | 93 条，A-H 组，无删减 |
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
| 特殊版 | 单开私仓，所有任务完成且复核无漏洞后构建 |

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
| src/ 空扫描 | `test -z "$(git ls-files src/)"` |

## 搭建前置条件

| 条件 | 当前值 |
| --- | --- |
| D06 信号 | 未提供 |
| 005-blueprint.md | 未批准 |
| X01-X04 用户拍板 | 未拍板 |
| Win7 兼容路径 | 未选 |
| 多架构范围 | 未定 |
| 地域判定口径 | 未定 |
| 待拍板问题 93 条 | 未答复 |
| 开工时点 S1/S2 | 并列登记，未确认 |
| src/ | 空 |

详见 docs/rules/build-preconditions.md 条件 1-6。

## 未写入项

- 框架蓝图：005-blueprint.md 已落盘，状态未批准。
- 源码：src/ 为空。
- 正常模式 UI 实现：设计稿已落盘，未实现、未进入构建。
- UI 设计稿品牌与字体授权：未取得。
- 图标 ICO 与裁切版本：未生成。
- 本项目 LICENSE：未定，未生成。
- 特殊版私仓：未创建。
- 后端仓任何写请求：0。
- 插件源默认选择、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 日志外传条款：未证实。
- 011 轮遗留未证实项与 012 轮 Q-A 至 Q-G：见 docs/records/open-questions.md。
- 浏览器内渲染实测、rustc / cargo 构建验证：受阻。

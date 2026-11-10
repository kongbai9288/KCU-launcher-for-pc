# 文档索引

检索日期：2026-11-11
更新轮次：011

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
14. docs/checklists/ai-errors.md
15. docs/checklists/windows-errors.md
16. docs/rules/proof-rules.md
17. docs/rules/fallback-rules.md
18. docs/rules/push-scope.md
19. docs/rules/build-preconditions.md
20. docs/research/index.md
21. docs/features/index.md
22. docs/records/rounds.md

读取命令：

```
cd /data/workspace/kcu-launcher-desktop
for f in docs/spec/00-requirements.txt docs/spec/01-round-001-instructions.txt docs/spec/02-round-002-instructions.txt docs/spec/03-round-003-instructions.txt docs/spec/04-round-004-instructions.txt docs/spec/05-round-005-instructions.txt docs/spec/06-round-006-instructions.txt docs/spec/07-round-007-instructions.txt docs/spec/08-round-008-instructions.txt docs/spec/09-round-009-instructions.txt docs/spec/10-round-010-instructions.txt docs/spec/11-round-011-instructions.txt docs/spec/11-features-input.txt docs/checklists/ai-errors.md docs/checklists/windows-errors.md docs/rules/proof-rules.md docs/rules/fallback-rules.md docs/rules/push-scope.md docs/rules/build-preconditions.md docs/research/index.md docs/features/index.md docs/records/rounds.md; do printf '%s %s\n' "$f" "$(wc -l < "$f")"; done
```

## 分区

| 分区 | 入口 | 职责 |
| --- | --- | --- |
| 需求规格 | docs/spec/00-requirements.txt | 需求原文 |
| 011 功能输入 | docs/spec/11-features-input.txt | 55 条编号功能与 175 项文件管理清单逐字副本 |
| 调研 | docs/research/index.md | 外部事实、锚点、四值 |
| 合规与阻塞项 | docs/research/12-compliance.md | API 条款、凭据保护、许可证全文、上游版本、X01-X07 |
| 系统 API 与平台 | docs/research/13-platform-api.md | Win7、多架构、版本/架构/位置 API、Rust 目标冲突 |
| 网络通用法 | docs/research/14-batch-network.md | 批量端点、N+1 反模式、回环监听、配置集中 |
| 外部项目核实 | docs/research/15-input-survey.md | 只读后端仓、CopperGolemLauncher、ViaNBT、dsh、VxKex |
| 底层运行时调研 | docs/research/11-runtime.md | Cargo profile、DLL 搜索、进程管理、WebView2 进程组、目标三元组、MSVC 部署 |
| 许可证原文 | docs/licenses/index.md | 逐字副本与 slint 三许可全文 |
| 功能登记 | docs/features/index.md | F001-F012；011 轮输入见 docs/features/backlog.md |
| 决策 | docs/decisions/index.md | 状态分层记录 |
| 防错 | docs/checklists/ | AI 与 Windows 防错清单 |
| 规则 | docs/rules/ | 四值判决、兜底分级、推送范围、搭建前置条件 |
| 记录 | docs/records/ | 版本、接口、轮次 |
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
| 原文口径扫描 | `grep -n 'Introduced in' docs/research/06-server.md` |
| 推广措辞扫描 | `! grep -rE '表现得最优\|使用人数最多\|社区反馈最积极' docs/features/ docs/decisions/` |
| 功能状态扫描 | `test -z "$(grep -L '未实现' docs/features/dispatcher.md docs/features/lightweight.md docs/features/headless.md docs/features/normal-launcher.md docs/features/lan.md docs/features/server.md docs/features/log.md docs/features/fallback.md docs/features/envelope.md docs/features/ui-framework.md docs/features/credential-guard.md)"` |
| 合规条款扫描 | `grep -n 'CF01\|CF02\|CF03\|CF04' docs/research/12-compliance.md` |
| tag 同名同 sha 扫描 | `grep -n 'v99.99' docs/research/12-compliance.md` |
| N+1 反模式扫描 | `grep -n '每搜索一个模组' docs/spec/11-features-input.txt` |
| 物理位置口径扫描 | `grep -n 'GEOID_NOT_AVAILABLE' docs/research/13-platform-api.md` |
| Win7 目标扫描 | `grep -n 'require at least Windows 10' docs/research/13-platform-api.md` |
| 编号功能完整性 | `grep -cE '^\| [0-9]+ \|' docs/features/backlog.md` |
| 逐条目单发扫描 | `grep -n '每搜索一个模组' docs/spec/11-round-011-instructions.txt` |

## 搭建前置条件

| 条件 | 当前值 |
| --- | --- |
| D06 信号 | 未提供 |
| 005-blueprint.md | 未批准 |
| X01-X04 用户拍板 | 未拍板 |
| Win7 兼容路径 | 未选 |
| 多架构范围 | 未定 |
| 地域判定口径 | 未定 |
| src/ | 空 |

详见 docs/rules/build-preconditions.md。

## 未写入项

- 框架蓝图：005-blueprint.md 已落盘，状态未批准。
- 源码：src/ 为空。
- 正常模式 UI 实现：设计稿已落盘，未实现、未进入构建。
- UI 设计稿品牌与字体授权：未取得。
- 图标 ICO 与裁切版本：未生成。
- 本项目 LICENSE：未定，未生成。
- 特殊版私仓：未创建。
- Notchian 服务端离线 UUID 行为、Mojang 官方 RCON 文档、加载器逐版本 schema、令牌保护方案、Azure Client ID：未证实。
- CREATE_NO_WINDOW 具体值、std::process 超时 API、WebView2 内存占用关系、本项目单文件发布工具链：未证实。
- 电脑端多操作入口交互具体形式：未证实。
- CF04-CF06、MCIM / BMCLAPI 条款、Modrinth 缓存限流条款：未证实。
- Win7 兼容路径、ARM64 与 Win7 交集、地域判定口径、文件管理开源骨干、ViaNBT 集成方式：未证实或已失败。

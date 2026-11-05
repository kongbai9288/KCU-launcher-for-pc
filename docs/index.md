# 文档索引

检索日期：2026-11-05
更新轮次：008

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
10. docs/checklists/ai-errors.md
11. docs/checklists/windows-errors.md
12. docs/rules/proof-rules.md
13. docs/rules/fallback-rules.md
14. docs/rules/push-scope.md
15. docs/research/index.md
16. docs/features/index.md
17. docs/records/rounds.md

读取命令：

```
cd /data/workspace/kcu-launcher-desktop
for f in docs/spec/00-requirements.txt docs/spec/01-round-001-instructions.txt docs/spec/02-round-002-instructions.txt docs/spec/03-round-003-instructions.txt docs/spec/04-round-004-instructions.txt docs/spec/05-round-005-instructions.txt docs/spec/06-round-006-instructions.txt docs/spec/07-round-007-instructions.txt docs/spec/08-round-008-instructions.txt docs/checklists/ai-errors.md docs/checklists/windows-errors.md docs/rules/proof-rules.md docs/rules/fallback-rules.md docs/rules/push-scope.md docs/research/index.md docs/features/index.md docs/records/rounds.md; do printf '%s %s\n' "$f" "$(wc -l < "$f")"; done
```

## 分区

| 分区 | 入口 | 职责 |
| --- | --- | --- |
| 需求规格 | docs/spec/00-requirements.txt | 需求原文 |
| 调研 | docs/research/index.md | 外部事实、锚点、四值 |
| 许可证原文 | docs/licenses/index.md | 7 份第三方逐字副本 |
| 功能登记 | docs/features/index.md | 每个功能一份 md |
| 决策 | docs/decisions/index.md | 状态分层记录 |
| 防错 | docs/checklists/ | AI 与 Windows 防错清单 |
| 规则 | docs/rules/ | 四值判决、兜底分级、推送范围 |
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

## 未写入项

- 框架蓝图：005-blueprint.md 已落盘，状态未批准。
- 源码：src/ 为空。
- 正常模式 UI 实现：设计稿已落盘，未实现、未进入构建。
- UI 设计稿品牌与字体授权：未取得。
- 图标 ICO 与裁切版本：许可证与范围未确认，未生成。
- 本项目 LICENSE：未定，未生成。
- Notchian 服务端离线 UUID 行为、Mojang 官方 RCON 文档、slint 三许可全文：未证实。

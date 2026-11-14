# 第 028 轮：开服器三项新功能只记文档，代码替换继续

| 项 | 值 |
| --- | --- |
| 编号 | 028 |
| 状态 | 已登记；三项新功能未实现 |
| 依据 | docs/spec/28-round-028-instructions.txt |
| 前序 | docs/features/server-backlog.md（012 轮开服器台账）、docs/records/code-ownership-audit.md |
| 本轮性质 | 双轨轮 |

## 两条指令的边界

| 编号 | 原文片段 | 处置 |
| --- | --- | --- |
| B01 | 「干」 | 按既有进度继续替换自写代码，落 `src/core/leak.rs`。 |
| B02 | 「开服器有新功能啦……（只记文档）」 | 三项新功能逐字登记、逐项写功能 md、补一手调研、出运行逻辑演示；`src/` 中不新增任何开服器实现，不进构建，不动 UX 整页演示。 |
| B03 | 「只记文档」 | 括号紧跟功能列表，限定这三项；不覆盖 B01。 |

## 三项新功能

| 编号 | 功能 | 功能 md | 框架 |
| --- | --- | --- | --- |
| F028-01 | 玩家上线提醒 | server-join-alert.md | normal.server |
| F028-02 | 饼图分析活跃度 | server-activity-pie.md | normal.server |
| F028-03 | 自动命令：服务器出现的命令文字作为触发条件 | server-auto-command-log-trigger.md | normal.server |

三项都挂在 012 轮 `docs/features/server-backlog.md` 的开服器台账下，不另起框架、不改 005-blueprint.md 已批准的分层。状态统一为「已批准 · 未实现 · 未进入构建」。

## 代码替换（B01）

| 编号 | 动作 |
| --- | --- |
| C01 | `src/core/leak.rs` 删掉自写 `Tracker` / `Tracked`：手工 `Arc<AtomicUsize>` 计数、clone / drop 配对递减、Drop 兜底全部移除，191 → 99 行。 |
| C02 | `WeakRegistry` 保留，它只用 `std::sync::{Arc, Mutex, Weak}`，无自写并发原语；`purge` 用 `HashMap::retain`。 |
| C03 | `src/dispatcher/launcher.rs` 的 `outcomes_do_not_leave_live_tracked_objects` 改用 `Arc::strong_count` / `Weak::upgrade`，并追加 027 已落地的 `crossbeam_utils::sync::WaitGroup` 归零断言。 |
| C04 | `src/lib.rs` 导出收敛为 `WeakRegistry`；`src/core/mod.rs` 不变。 |
| C05 | 无新增依赖：`Cargo.lock` 仍 8 包 / 7 第三方，`vendor/` 不变。 |

按 `docs/records/code-ownership-audit.md` 映射表，`core/leak.rs` 的处置是「大幅删减或删」，本轮按此执行。删掉的 2 个测试只服务于已删除的自写类型，等价断言已迁移，未降低验收项；`cargo test --offline` 141 → **139 / 0**，差值 2 如实登记。

## UI 闸门

`docs/rules/ui-demo.md` 未触发：本轮不动用户界面、不改 `demos/ui-full-*.html`、不重渲预览图。三项功能的界面形态（提醒条、饼图卡片、规则编辑器）留在功能 md 的「用户使用逻辑」里，等你给手感反馈的轮次再出整页 UX 演示。

## 四值

| 项 | 值 |
| --- | --- |
| 三项功能逐字登记、五字段齐备、15 条来源标注 | 已证实 |
| leak.rs 自写计数删除、139 / 0、8 包不变 | 已证实 |
| 三项功能的实现、界面、真实日志样本回放 | 未证实 |
| 浏览器渲染、真实服务端联调、Win7 / 多架构 | 受阻 |
| 后端仓写请求 | 0（已证实） |

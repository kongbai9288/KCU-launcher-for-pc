# 第 19 条：游戏时长记录

| 项 | 值 |
| --- | --- |
| 状态 | 数据层已实现（061）；显示层未启动 |
| 原文 | `docs/spec/11-features-input.txt:226` 逐字保存 |
| 模块 | `src/core/stats.rs`；`dispatcher::Dispatcher::finish_session` |
| 存储 | `play-stats.json`，`schema=1`，`total_seconds` 与 `instances` 两项 |
| 口径 | 单次 = ended − started；总时长与每实例时长累加；快捷启动写数据且 `show_popup=false` |
| 边界 | 空 id、控制字符、超长 id 拒绝；时钟回拨记 0；单次上限 30 天；实例上限 4096；并发会话上限 3（第 26 条）；1 秒 64 次限流；文件删 / 坏 / 超大 / schema 错回默认；锁中毒恢复；写失败可见 |
| 已复用 | `serde_json`、`robust::read_or_default` / `safe_join` / `OpBudget` / `check_text`、`diagnostics::diag_line`、标准库 `PoisonError::into_inner` |
| 未启动 | 显示层：`PopupKind::Duration` 已在 `popup.rs:171` 目录，未接数据；真实游戏进程结束事件源 |
| 许可 | 零新增第三方；既有 crate 全文在 `docs/licenses/` |

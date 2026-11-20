# 061 开工逐字复读记录

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 41234 | 443 | `5f763a0678a1f89076348fcfdb6731b30aac41c5782f6c9d2703b2a5306ec296` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/61-round-061-instructions.txt` | 3 | 1 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |

复读在写任何代码/文档之前完成。本轮真读 `00-requirements.txt` 第 6 / 7.3 / 8 / 11 / 12 / 14 / 18 节全文，`11-features-input.txt` 第 19 / 26 条逐字，`12-server-features-input.txt` 全文，防错清单 A194–A216 全文。

| 原文锚点 | 内容 |
| --- | --- |
| `11-features-input.txt:226` | `19.每次游戏结束的时候显示玩了多长时间，并且有记录总时长，对应每一个实例 时长（这些都是咱们启动器的时长）（如果是快捷启动则静默记录）` |
| `11-features-input.txt:233` | `26.支持同时启动多个我的世界版本（默认最大的限额为3个）` |
| `00-requirements.txt:181` | 启动级兜底：连续多次启动失败进入安全模式，忽略自定义配置用内置默认；安全模式仍失败，导出诊断包 |
| `00-requirements.txt:182` | 诊断输出统一一行：`[KCU] <域> <动作> <目标> <结果> <详情>` |
| `00-requirements.txt:109-114` | 禁止空捕获、捕获后返回空值；必须处理空值、空集合、越界、超时、编码；禁止顺手改无关文件；路径集中在一个类或模块改；跨进程消息走统一信封 |
| `00-requirements.txt:52-55` | 代码与注释冷淡、直接、事实性；禁 AI 风；不做过度抽象、不偷偷加依赖 |
| `00-requirements.txt:244-249` | 独立验证结论 > 自评；四值判决 > 通过标记；安全与许可证合规 > 功能进度 |
| `docs/features/backlog.md:33` | `19 | 单次时长、总时长、每实例时长，快捷启动静默记录 | normal.stats | 已登记 / 未实现` |
| `src/core/popup.rs:171` | `Popup::new("duration", PopupKind::Duration, "play_duration")` 已在目录，无数据层 |

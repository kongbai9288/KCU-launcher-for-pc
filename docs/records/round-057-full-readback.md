# 057 开工逐字复读记录

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 39451 | 417 | `b8400e9332bb30ea26b1f329a174d8a603ff1dedc3cce9188b39c4029ef9a6a0` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/57-round-057-instructions.txt` | 4 | 1 | `67997353aa5bff040e44079f327ae485087311fa55006035d03e00cfe29ede15` |

复读在写任何代码/文档之前完成。本轮真读 00-requirements.txt 第 12 节、11-features-input.txt 第 12/29 行、12-server-features-input.txt 全文。

| 原文锚点 | 内容 |
| --- | --- |
| 00-requirements §12 | 启动级兜底：连续多次启动失败进入安全模式，忽略自定义配置用内置默认；安全模式仍失败，导出诊断包（日志 + 配置快照 + 运行时信息 + 已加载模块列表） |
| 00-requirements §12 | 分级：零级致命 / 一级功能失效 / 二级降级 / 三级忽略；诊断输出统一一行 `[KCU] <域> <动作> <目标> <结果> <详情>`；禁用空捕获 |
| 00-requirements §7.3 | 禁止空捕获；必须处理空值、空集合、越界、超时、编码；禁止硬编码环境假设 |

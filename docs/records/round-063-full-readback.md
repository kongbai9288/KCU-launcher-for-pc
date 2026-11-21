# 063 开工逐字复读记录

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 43187 | 457 | `3169adff4b7b94f804e61b8c1d970cec578cea44acabc2624924125b9697fb23` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/63-round-063-instructions.txt` | 228 | 0 | `f92348ac3bc6802fb6d04f5dcbb398985404043cecb2160ab29410d6ac9da9f9` |

复读在写任何代码 / 文档之前完成。本轮真读 `00-requirements.txt` 全文（含第 44 行、第 18 节裁决顺序）、`11-features-input.txt` 55 条全文、`12-server-features-input.txt` 全文、防错清单 A194–A224 全文。

| 原文锚点 | 内容 |
| --- | --- |
| `63-round-063-instructions.txt` | 用户当轮逐字原文 |
| `00-requirements.txt:44` | `功能与市面主流启动器保持同步：别人有的功能要有。` |
| `00-requirements.txt:248` | `用户当轮明确指令 > 本文件规则。用户临时要求偏离规则时，先执行，同时指出偏离了哪条规则。` |
| `11-features-input.txt:18` | `尽量不要把咱们的APi写成共有的API,防止被别人攻击，内部监听（只有服务器功能让ai用的api不受影响）` |
| `11-features-input.txt:11` | `支持陶瓦联机`（第 11 条；子 agent 报告误写为 11-45） |
| `11-features-input.txt:45` | `jvm内存自动分配`（第 45 条） |
| `12-server-features-input.txt:32` | `备份完整性校验 + 恢复预览` |
| `12-server-features-input.txt:4` | `支持ai自动管理服务器即开放api让运行在本地的或者是在本地有容器的ai能直接把这个当做工具使用，但是不赋予删除权限并且告诉对应的请求ai需要用户在本软件手动选择同意` |
| `00-requirements.txt:133` | `需求必须逐字保存到仓库` |
| `00-requirements.txt:73-94` | 仓库内容边界：禁止解释性内容进仓库 |

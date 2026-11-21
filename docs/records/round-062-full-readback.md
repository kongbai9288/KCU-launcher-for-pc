# 062 开工逐字复读记录

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 42217 | 452 | `741d0fbf71fe3f5662364ea213f83010d856f914dec92bba34911ba8b5107e56` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/62-round-062-instructions.txt` | 217 | 0 | `bc09aac748beb50867fdd0ed6719976d8d912bc3eabfb95990ccf77578b25e3d` |

复读在写任何代码 / 文档之前完成。本轮真读 `00-requirements.txt` 第 6 / 7.3 / 8 / 11 / 12 / 14 / 18 节全文，`11-features-input.txt` 第 11–19 行逐字，`12-server-features-input.txt` 全文，防错清单 A194–A220 全文。

| 原文锚点 | 内容 |
| --- | --- |
| `11-features-input.txt:18` | `尽量不要把咱们的APi写成共有的API,防止被别人攻击，内部监听（只有服务器功能让ai用的api不受影响）` |
| `00-requirements.txt:25` | `尽量少选择平台固定的api，这样的话快速升级版本什么的都快` |
| `00-requirements.txt:24` | `注：所有的ui等都使用框架方式，这样统一管理起来方便` |
| `11-features-input.txt:16` | `每个页面都能扩展内容这样方便统一格式` |
| `11-features-input.txt:15` | `尽量复用同一个代码，对于未来的变更都尽量把文件归中方便后面维护` |
| `11-features-input.txt:19` | `尽量不要api写死，还有那些联网的功能的网址，api主要用于分类操作系统,方便以后万一要是被别的系统的时候更容易做...为了更新方便，也不要这样写` |
| `00-requirements.txt:114` | `所有跨进程消息走统一信封，有请求、响应、事件区分，有请求标识，有统一错误。` |
| `00-requirements.txt:137` | `每次开动前，确认文件接口最后一层会到哪里，再开始写。` |
| `00-requirements.txt:173` | `破坏性变更升版本号并给迁移步骤。` |
| `00-requirements.txt:175` | `同类功能尽量复用同一个模块，缩小体积，方便快速定位函数。` |
| `src/lib.rs`（061 版） | 12 行 `pub use` 平铺 29 个内部具体类型 |
| `src/core/popup.rs`（061 版） | `catalog()` 用 13 处 `Popup::new` 逐条构造；`userflow.rs:56` 绕过目录直接构造 |

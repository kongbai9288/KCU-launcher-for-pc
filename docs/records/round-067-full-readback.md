# 067 开工逐字复读记录

开工 `Sat Nov 21 21:07:24 CST 2026`。`00-requirements.txt` 全文（261 行）与 `docs/checklists/ai-errors.md` 全文（484 行）已完整读过；再读 `11-features-input.txt` 第 34 条、`12-server-features-input.txt` 第 19 条、066 指令与决策结尾、功能池全文、`envelope.rs` / `popup.rs` / `settings_io.rs` 现状。复读在写任何代码 / 文档之前完成，对应 `00:34` / `00:260` / A18。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 48240 | 484 | `5a0690bfa49ac9fab8cfd87ccb0210d6af6d08db2e429ce6c86da6ade8f2a16d` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/66-round-066-instructions.txt` | 24 | 0 | `df6c0d1c547459ee6eb92b992efd1b1fe7c4f3ca0978fe2b0e449f0e1d88a53f` |
| `docs/spec/67-round-067-instructions.txt` | 328 | 1 | `3ff582d4a5d6234da2a5af06c74d69220b5ea8a5983d8e4bf4e47f58002e00fe` |
| `docs/records/ax-feature-pool.md` | 4660 | 65 | `5b9d1a7b5e96847e06fbcf9e736586b9c3bdd8cdcca8d5ecaac422566f838ab6` |
| `docs/decisions/066-download-history.md` | 8596 | 91 | `01ae50a0f2592aa9a6d7973c9acdeb4a9f75a8abf9967fa8219f7c189e32ba80` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `src/core/popup.rs` | 11726 | 368 | `973dc0d1885f0611f1b541e8f9d3ae4cde2e0e8b54d995bdc825ed042fb636dd` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `67-round-067-instructions.txt:1` | `干.还有我说下扩展包是要安装才能用对应功能[即原功能位有锁图，点开会提示安装，注意两进程通讯的安全性]（win平台有便携app限制，才有这个扩展），关于统一调度器启动后进入全量启动器时会有加载进度条用于等待加载完成。不周之处你完普` |
| `00-requirements.txt:114` | `所有跨进程消息走统一信封，有请求、响应、事件区分，有请求标识，有统一错误。` |
| `00-requirements.txt:137` | `每次开动前，确认文件接口最后一层会到哪里，再开始写。` |
| `00-requirements.txt:166` | `每个状态只声明实际达到的那一层，不合并表述。` |
| `00-requirements.txt:175` | `同类功能尽量复用同一个模块，缩小体积，方便快速定位函数。` |
| `00-requirements.txt:179` | `任何单点失败不允许导致应用崩溃或无法启动。失败必须可见、可诊断、可回退。` |
| `00-requirements.txt:248` | `用户当轮明确指令 > 本文件规则。` |
| `00-requirements.txt:73-94` | 仓库内容边界：设计动机、取舍解释不进仓库 |
| `00-requirements.txt:209-222` | 输出结构 12 项固定 |
| `00-requirements.txt:245` | `有任何未解决的「已失败 / 未证实 / 受阻」，不发通过标记。` |
| `11-features-input.txt:242` | 第 34 条：`.kculf` 功能「必须在用户已经用了咱们软件两天或者用户手动点击按钮从咱们的这个文件包当中的拓展包安装以后才能正常使用」 |
| `11-features-input.txt:242` 复核 | 原文含 **OR 两条路径**：使用满两天 / 手动安装拓展包。本轮只落「安装」路径；「使用满两天」时长路径未落数据层，登记 **Q-067-02** 待拍板，不擅自替用户决定两条路径的优先级（A164） |
| `12-server-features-input.txt:19` | 第 19 条：访客模式的「功能锁定」与命令黑名单 |
| `envelope.rs:27-41` | `Kind::{Request, Response, Event}` / `Envelope::request_id` / `with_error` / `ok()` |
| `popup.rs:53` | `id: "extension"` 已注册，`PopupKind::ExtensionInstall`，062 起 13 条 spec |
| `settings_io.rs:23` | `PROTECTED_FILES` 4 项，065 起复用 |
| `ai-errors.md:449` | A217：已登记占位只接数据层，不写成功能已实现 |
| `ai-errors.md:392` | A195：用户原文与演示文案冲突时以用户原文为准，演示修正等 UI 闸门 |
| `ai-errors.md:405` | A203：授权成立也要逐值回显具体默认 |
| `ai-errors.md:383` | A190：自动关闭用户功能一律取不关 |
| `ai-errors.md:396` | A198：不同模块同名字段口径互不套用 |
| `ai-errors.md:483` | A246：新增内部数据层不扩 `api::v1` |
| `066-download-history.md` 结尾 | 预告「继续按功能池落下一项（剩 20 项 Planned）」 |

## 合规核对表（`00:34` / `00:260` / A244）

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存当轮指令 | `docs/spec/67-round-067-instructions.txt` 328 字节 / SHA-256 `3ff582d4...`；错别字「完普」原样保留 |
| `00:34` / `00:260` / A18 | 真读 00 全文 261 行、防错清单 484 行，非 grep 摘要 |
| `00:137` 接口终点 | 新模块只被 `core/mod.rs`、`boot.rs LOADED_MODULES`、守卫、CI、演示引用；**`api::v1` 7 符号不动**；`popup.rs` 复用已有 `extension` spec 不新增类型；`dispatch()` 20 个断言一字不改 |
| `00:248` 优先级 | 用户当轮给新功能，覆盖 066 结尾「按功能池落下一项」预告；AX 池 20 项本轮不动，登记 D-067-1 |
| `00:54` / `00:111` | 零新增第三方；不改 `dispatcher/launcher.rs`、`stats.rs`、`consent.rs`、`cache.rs`、UX HTML、两语言包、56 张 PNG |
| `00:166` 状态分层 | 只声明数据层与编排；锁图渲染、进度条渲染、真实 IPC 通道、子进程隔离均未启动 |
| `00:114` | 安装请求 / 响应 / 进度事件全走 `Envelope`，显式 `Kind` 区分与 `request_id` 配对 |
| `00:179` | 8 类坏输入、超时、重放、越权、写盘失败全部给 `[KCU]` 行，不崩 |
| `00:245` / `00:9.1` | 存在未证实 / 未启动 / 已失败项，不发通过标记 |
| `00:6.1` / `00:224` | 便携 app 限制属解释性内容，只走对话，不进仓库 |
| `00:209-222` | 本轮回复按 12 项输出结构 |

## 「不周之处你完普」逐值回显（A203）

用户授权补全考虑不周之处，按 A203 逐值列出具体默认，全部标为**我的默认（D-067-2 ~ D-067-8）**，不写成用户已决断。

| 编号 | 补全项 | 具体默认值 |
| --- | --- | --- |
| D-067-2 | 功能位锁状态 | 默认全部 `Locked`，安装对应扩展后才 `Unlocked`；未登记功能位返回 `Unknown` 不崩 |
| D-067-3 | 点开提示 | 复用 062 已注册 `extension` 弹窗，不新增弹窗类型（13 条 spec 不变） |
| D-067-4 | 两进程通讯安全 | 请求-响应 `request_id` 配对；`Event` 不顶替安装完成；`target` 白名单；`extension_id` 与请求绑定；超时由调用方注入；错误信封拒；pending 上限 16；消费后移除防重放 |
| D-067-5 | 真实 IPC 边界 | 不启动真实进程、不绑定端口、不读系统时钟；只落信封层校验；子进程隔离 EQ-05 未拍板 |
| D-067-6 | 加载进度 | 5 阶段单调状态机；阶段与百分比只增不回退；失败 / 取消 / 超时可见；取消 0 副作用；渲染层未启动 |
| D-067-7 | 安装状态持久化 | `extension-installs.json`，schema 1，8 类坏输入回默认，原子写，复用 065 四文件保护清单 |
| D-067-8 | 功能位清单 | 最小默认映射表 5 条（含 `headless.kculf` 呼应 11:242）；具体功能位归属哪个扩展包登记 Q-067-01 待拍板 |
| D-067-9 | 演示层冲突 | UX 演示有「扩展」槽位与「扩展安装确认」弹窗文案，但缺锁图元素；按 A195 登记待办，UI 闸门触发时补，本轮不改界面 |
| D-067-10 | 访客模式区分 | `12:19` 的「功能锁定」是访客模式权限，与本轮「未安装扩展包锁位」不是同一机制，不复用、不混淆 |

## 冲突复核结论

一处口径需显式区分：`A190` 规定「自动关闭用户功能」误关比不关更糟一律取不关；本轮是「未安装扩展包则功能位锁定」，属用户当轮明确要求，按 `00:248` 优先，不套用 A190，按 A198 登记为独立口径。

一处优先级覆盖：066 结尾预告按 AX 功能池落下一项；用户当轮给两段新功能，按 `00:248` 本轮改为落地新功能，AX 池 20 项 `Planned` 不动。

选项目的复核：两段新功能均不碰 EQ-01 ~ EQ-13、不碰真实网络 IO、不碰 UI 渲染闸门、无需新增第三方；`11:242` 与 062 `popup.rs:53` 提供原文与占位锚点，A217 口径下只接数据层。

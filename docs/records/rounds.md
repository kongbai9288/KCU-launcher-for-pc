# 轮次变更记录

## 001

| 落点 | 内容 |
| --- | --- |
| .gitignore | 忽略构建产物、日志、凭据文件 |
| README.md | 项目事实索引 |
| docs/index.md | 文档索引、每轮必读顺序、开工检查命令 |
| docs/spec/00-requirements.txt | 需求原文逐字副本，261 行 |
| docs/spec/01-round-001-instructions.txt | 当轮指令逐字副本，5 行 |
| docs/research/*.md | 9 份主题事实条目与索引 |
| docs/features/index.md | 功能登记索引，当前无条目 |
| docs/features/_template.md | 功能 md 模板，5 个固定字段 |
| docs/decisions/index.md | 决策索引，框架蓝图待确认 |
| docs/checklists/*.md | AI 与 Windows 防错清单 |
| docs/rules/*.md | 证明规则与兜底规则 |
| docs/records/*.md | 版本、接口、轮次记录 |
| demos/round-001-dispatch.html | 统一调度器运行逻辑 HTML |
| src/ | 空目录 |

未做：
- 源码
- 远程仓库创建
- 框架蓝图落盘
- 功能实现

## 002

| 落点 | 内容 |
| --- | --- |
| docs/spec/02-round-002-instructions.txt | 当轮指令逐字副本，1 行 |
| assets/icon/kcu-launcher.jpg | 图标原始字节，175816 字节，JPEG 1440x1440 |
| docs/decisions/002-icon.md | 图标资产决策记录 |
| docs/decisions/index.md | 加入 002 条目与三项待确认 |
| docs/index.md | 必读顺序扩为 10 项，分区加入资产与 002 演示 |
| README.md | 轮次 002，仓库状态与图标路径 |
| docs/records/rounds.md | 本段落 |
| demos/round-002-icon.html | 图标资产登记运行逻辑 HTML |

格式纠正：

| 位置 | 原因 | 修复动作 |
| --- | --- | --- |
| assets/icon/kcu-launcher.png（重命名前路径，已不存在） | 源文件名为 .png，魔数为 JPEG，扩展名与格式不一致 | 重命名为 assets/icon/kcu-launcher.jpg，字节未改动，SHA-1 一致 |

未做：
- 源码
- 远程仓库创建
- 框架蓝图落盘
- 正常模式 UI 落盘
- ICO 与裁切版本
- 功能实现

## 003

| 落点 | 内容 |
| --- | --- |
| docs/spec/03-round-003-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/decisions/003-remote.md | 远端公仓、每轮推送、搭建阶段决策记录 |
| docs/decisions/index.md | 加入 003 条目与触发条件待确认 |
| docs/rules/push-scope.md | 允许推送与不推送清单、每轮动作、诊断行 |
| scripts/push.sh | 参数化远端推送入口，无 URL 硬编码 |
| .gitignore | 追加私有配置、诊断包、探测文件排除项 |
| docs/index.md | 必读顺序扩为 12 项，分区加入推送规则、脚本与 003 演示 |
| README.md | 轮次 003，仓库形态与当前阶段 |
| docs/records/rounds.md | 本段落；002 格式纠正表标注重命名前路径 |
| demos/round-003-remote.html | 远端推送与搭建阶段运行逻辑 HTML |
| 首个本地提交 | 001-003 全部产物纳入版本控制，署名 yuanbao |

远端探测结果：

| 请求 | 状态码 | 结果 |
| --- | --- | --- |
| GET /rate_limit 带完整请求头 | 200 | 已证实 |
| GET /rate_limit 无 User-Agent | 403 | 已证实 |
| POST /user/repos 无认证 | 401 Requires authentication | 受阻 |

未做：
- 远端公仓创建与推送
- 源码
- 框架蓝图落盘
- 正常模式 UI 落盘
- 底层统一搭建

## 004

| 落点 | 内容 |
| --- | --- |
| docs/spec/04-round-004-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/decisions/004-remote-created.md | 公仓创建、名称规范化、网络边界、降级路径 |
| docs/decisions/index.md | 加入 004 条目 |
| docs/rules/push-scope.md | 远端地址、请求头、降级路径、blob sha 核对 |
| scripts/api_push.py | Git Data API 全量树快照，凭据只读环境变量 |
| scripts/push.sh | 重写为 git HTTP 失败后自动降级 API 快照 |
| docs/index.md | 必读顺序扩为 13 项，加入远端信息与 004 演示 |
| README.md | 轮次 004，远端地址、可见性、推送路径 |
| docs/records/rounds.md | 本段落 |
| demos/round-004-remote.html | 公仓创建与 API 快照推送运行逻辑 HTML |
| docs/verification/round-004.md | 第 004 轮独立验证报告，结论部分通过 |

远端动作：

| 动作 | 结果 |
| --- | --- |
| `GET /user`，`Authorization: Bearer` | 403 policy_default_denied |
| `GET /user`，`Authorization: token` | 200，login=kongbai9288 |
| `POST /user/repos`，name=`KCU launcher for pc` | 201，实际名 `KCU-launcher-for-pc` |
| `GET /repos/kongbai9288/KCU-launcher-for-pc` | 200，private=false，default_branch=main |
| git HTTP push，三种认证方式 | 受阻，github.com 主机 403 policy_default_denied |
| `POST /git/blobs`，空仓库未初始化 | 409 `Git Repository is empty.` |
| `PUT /contents/README.md` | 201，初始提交 d0acb0d |
| `scripts/api_push.py` | 启用，二级降级；首次快照 c76f491，42 文件 |

名称差异：

| 输入 | 实际 |
| --- | --- |
| `KCU launcher for pc` | `KCU-launcher-for-pc` |
| 原串 | 保留在 repository description |

未做：
- 源码
- 框架蓝图落盘
- 正常模式 UI 落盘
- 底层统一搭建

## 005

| 落点 | 内容 |
| --- | --- |
| docs/spec/05-round-005-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/licenses/*.txt | 7 份第三方许可证原文 |
| docs/licenses/index.md | 来源、许可证、字节、SHA-1、约束 |
| docs/research/01-09.md | 9 份重写：锚点统一、四值纠正、一手证据补齐 |
| docs/research/10-upstream-state.md | 时间核实、上游版本、网络边界、工具链 |
| docs/research/index.md | 10 份索引、锚点规范、卡点状态 |
| docs/decisions/005-blueprint.md | 分层、目录、扩展点、关键抽象方案，状态未批准 |
| docs/decisions/index.md | 蓝图待确认，D06 未触发 |
| docs/checklists/ai-errors.md | A21-A24 |
| docs/checklists/windows-errors.md | W19-W20 |
| docs/records/interface-log.md | I10、S01-S10、连接约定 |

一手证据：

| 项 | 结果 |
| --- | --- |
| HMCL LICENSE 全文 | 200，685 行，35507 字节 |
| authlib-injector 规范 | 200，启动器 211 行、服务端 668 行 |
| Fabric Meta README | 200，544 行，profile/json 与 launcherMeta |
| github/docs api-versions.md | 200，91 行，410 Gone 规则 |
| WebView2 检测键 | 200，4 个注册表位置与 pv (REG_SZ) |
| server.properties | 200，68 键默认值 |
| RFC 6762 / 6763 / 6455 | 200 |
| 上游版本 | HMCL v3.16.4、wry-v0.57.1、Rust 1.99.1、fabric-loader 0.20.1 |
| 两个 API 版本头 | 200 / 200 / 200 |

纠错：

| 位置 | 原结论 | 修复动作 |
| --- | --- | --- |
| 001 轮 06-server.md:34 | broadcast-rcon-to-ops 默认 false | 改为 true，示例值与默认值分离 |
| 001 轮 06-server.md:43 | 2-byte pad | 改为 NULL 结尾 + 1-byte NULL pad |
| 001-002 轮四值 | 中间态 | 全部改为四值之一，A23 锁定 |
| 001-004 轮锚点 | 裸域名、短名、重复引用 | 10 份统一为 URL / path:line / cmd 输出 |

005 轮未闭环：

| 项 | 状态 |
| --- | --- |
| 本地提交 | 未执行 |
| 远端推送 | 未执行 |
| 独立验证 | 未执行 |
| HTML 演示 | 未生成 |
| 轮次记录 | 未写入 |
| 索引与 README 更新 | 未执行 |

## 006

| 落点 | 内容 |
| --- | --- |
| docs/spec/06-round-006-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/research/01-10.md | 10 份锚点说明改为「锚点逐行独立」 |
| docs/research/index.md | 清理 3 处被扫描域内的禁用词字面量 |
| docs/decisions/005-blueprint.md | V03 改为引用 A23 |
| docs/index.md | 必读 15 项、006 演示与 licenses 分区 |
| README.md | 轮次 006 |
| docs/records/rounds.md | 005、006 两段 |
| demos/round-006-closeout.html | 005 收口与 006 交付运行逻辑 HTML |
| docs/verification/round-006.md | 第 006 轮独立验证报告 |

扫描域自我命中修复：

| 检查 | 修复前命中 | 修复动作 |
| --- | --- | --- |
| A23 中间态扫描 | docs/research/index.md 2 处、005-blueprint.md 1 处 | 被扫描域内字面量移出，检查命令不动 |
| A24 重复引用扫描 | 10 份 research 文档声明行 | 声明行改为「锚点逐行独立」 |
| A21 服务状态扫描 | docs/research/index.md R05 | 改为「不记为上游服务异常」 |

未做：
- 源码与 src/ 实现
- 底层统一搭建
- 正常模式 UI
- 框架蓝图批准
- rustc / cargo 构建验证

## 007

| 落点 | 内容 |
| --- | --- |
| docs/spec/07-round-007-instructions.txt | 当轮指令逐字副本，1 行，54 字符 |
| assets/ui/normal-mode-v3.html | 正常模式 UI 设计稿逐字副本，172759 字节，2729 行 |
| assets/ui/index.md | 结构事实、导航、外部资源、品牌标记、许可证边界 |
| docs/features/normal-ui.md | F001 功能登记，5 个固定字段 |
| docs/features/index.md | F001 条目、轻量模式视图计划项 |
| docs/decisions/007-normal-ui.md | D01-D10、C01-C09、V01-V08 |
| docs/decisions/index.md | 007 已批准；正常模式 UI 已落盘、未实现 |
| docs/decisions/005-blueprint.md | C07，K08 与 E04 仅服务 normal |
| docs/rules/push-scope.md | 轮次 007，允许清单加入 assets/ui/ |
| docs/checklists/ai-errors.md | A25-A27 |
| docs/checklists/windows-errors.md | W21-W22 |
| docs/records/interface-log.md | I11、S11-S12 |
| docs/index.md | 必读 16 项、UI 资产分区、007 演示、品牌扫描 |
| README.md | 轮次 007、正常模式 UI 与轻量模式 UI 条目 |
| docs/records/rounds.md | 本段落 |
| demos/round-007-normal-ui.html | 正常模式 UI 与轻量分流运行逻辑 HTML |
| docs/verification/round-007.md | 第 007 轮独立验证报告 |

用户提供内容：

| 项 | 值 |
| --- | --- |
| 正常模式 UI | FCL 揉纸启动器桌面端 v3 HTML 设计稿 |
| 轻量模式约束 | 不复用正常模式 UI，保持极简 |
| 字节核对 | cmp exit 0，SHA-1 235943d217560d89f8e0598c7f78b902d993e99d 双端一致 |

结构事实：

| 项 | 值 |
| --- | --- |
| 分区注释 | 23 |
| 唯一 class | 274 |
| id 属性 | 157，唯一 156 |
| JS 函数 | 39 |
| 导航项 | 10 |
| CSS 变量 | 21 |
| 外部 URL | 2，其中 1 个为字体 CDN |
| 品牌标记 | 4 处，行 6、7、1589 与全文件计数 |

决策边界：

| 项 | 值 |
| --- | --- |
| 框架归属 | K08 UiFrame、E04 ui 仅服务 normal |
| lightweight | 独立视图，排除 UI 框架、设计稿、双主题、三栏、网格、衣柜、工具箱、设备桥接面板、向导、右键菜单、日志抽屉 |
| headless | 不加载任何 UI |
| 品牌与字体授权 | 未取得，不进构建 |
| D06 | 未提供，仍为功能输入阶段，src/ 保持空 |

扫描域自我命中修复：

| 检查 | 修复前命中 | 修复动作 |
| --- | --- | --- |
| A23 中间态扫描 | docs/decisions/007-normal-ui.md V07 | 改为引用 A23，字面量移出被扫描域，检查命令不动 |
| A25 品牌扫描 | src/ 空目录导致 grep stderr | 命令追加 2>/dev/null，断言不变 |

未做：
- 源码与 src/ 实现
- 底层统一搭建
- 正常模式 UI 实现与构建
- 框架蓝图批准
- 品牌与字体授权取得
- 浏览器内渲染实测
- rustc / cargo 构建验证

007 口径补充（独立验证者指出「53 字符」后复核）：

| 项 | 值 |
| --- | --- |
| Python `len(t)` | 54，含尾部换行 |
| 可见字符 | 53 |
| UTF-8 字节 | 160 |
| 007 段「54 字符」 | 指含换行的 Python 长度，口径表述含糊 |
| 处理 | 不改 007 指令副本、不改独立验证报告；本段登记口径 |

## 008

| 落点 | 内容 |
| --- | --- |
| docs/spec/08-round-008-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/features/dispatcher.md | F002 统一调度器，5 个固定字段 |
| docs/features/lightweight.md | F003 轻量启动器视图，5 个固定字段 |
| docs/features/headless.md | F004 无头模式启动器，5 个固定字段 |
| docs/features/index.md | F002-F004 入表、G01-G04 约束 |
| docs/research/06-server.md | RCON 三项升级为已证实，追加 008 补证段 |
| docs/research/02-auth.md | 离线 UUID 与在线 UUID 一手锚点，追加 008 补证段 |
| docs/research/index.md | 文件表与卡点状态表更新到 008 |
| docs/checklists/ai-errors.md | A28，工具摘要与原文不一致时取原文 |
| docs/index.md | 必读 17 项、008 演示、A28 检查项 |
| README.md | 轮次 008 |
| docs/records/interface-log.md | I12、S13-S14 |
| docs/records/rounds.md | 007 口径补充、008 段 |
| demos/round-008-mode-views.html | 模式视图登记与补证运行逻辑 HTML |
| docs/verification/round-008.md | 第 008 轮独立验证报告 |

当轮输入：

| 项 | 值 |
| --- | --- |
| 指令 | 「干」，逐字副本 1 行 |
| 新功能或 UI | 未提供 |
| D06 触发信号 | 未提供 |
| 阶段 | 003-remote.md D05 功能输入阶段，未启动 D07 |
| 偏离 | 9.1 连续未达应停下由用户决定范围；按 18.5 以用户当轮指令继续执行 |

补证：

| 项 | 008 结果 | 锚点 |
| --- | --- | --- |
| RCON 字节序 | 已证实，小端 | https://minecraft.wiki/w/RCON |
| RCON 引入版本 | 已证实，Java Edition Beta 1.9 Prerelease 4 | https://minecraft.wiki/w/RCON |
| RCON 分片上限 | 已证实，S→C 4096 / total 4110；C→S 1446 / total 1460 带页面 outdated? 标记 | https://minecraft.wiki/w/RCON |
| RCON 认证失败 | 已证实，Request ID = -1 | https://minecraft.wiki/w/RCON |
| 离线 UUID | 已证实，v3 / MD5 / `OfflinePlayer:<username>` | https://minecraft.wiki/w/Universally_unique_identifier |
| 在线 UUID | 已证实，v4 variant 1 RFC | https://minecraft.wiki/w/Universally_unique_identifier |
| Notchian 服务端采用离线 UUID 算法 | 未证实，页面未写明 | https://minecraft.wiki/w/Universally_unique_identifier |
| Mojang 官方 RCON 文档 | 未证实，未取得 | https://minecraft.wiki/w/RCON |
| slint 三许可全文 | 未证实，raw.githubusercontent.com 直抓受阻 | https://raw.githubusercontent.com/slint-ui/slint/master/LICENSE.md |

口径纠错：

| 项 | 值 |
| --- | --- |
| 工具摘要 | 写为 "Java Edition 1.9 prerelease 4"，丢掉 Beta |
| 采用值 | Java Edition Beta 1.9 Prerelease 4，取一手原文 |
| 新增防错 | A28，关联 A22 |
| 实现约束 | 02-auth.md 离线 UUID 实现禁用约束不解除 |

索引纠错：

| 位置 | 原值 | 修复动作 |
| --- | --- | --- |
| docs/research/index.md 卡点表 | 正常模式 UI「未提供，未落盘」 | 改为 007 轮已落盘、未实现、未进入构建 |
| docs/research/index.md 文件表 02/06 行 | 未证实列含 RCON 三项 | 移入已证实列 |
| docs/research/index.md 卡点表 | 只有 005 状态一列 | 加 008 状态列与 2 行新卡点 |

功能登记：

| 编号 | 功能 | 框架 | 状态 |
| --- | --- | --- | --- |
| F002 | 统一调度器 | dispatcher | 已批准，未实现 |
| F003 | 轻量启动器视图 | lightweight.view | 已批准，未实现 |
| F004 | 无头模式启动器 | headless | 已批准，未实现 |

未做：
- 源码与 src/ 实现
- 底层统一搭建
- 框架蓝图批准
- 正常模式 UI 实现与构建
- 品牌与字体授权取得
- 加载器逐版本 schema、Notchian 服务端行为、令牌保护、Mojang 官方 RCON 文档、slint 三许可全文补证
- 浏览器内渲染实测
- rustc / cargo 构建验证

## 009

| 落点 | 内容 |
| --- | --- |
| docs/spec/09-round-009-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/research/11-runtime.md | 底层运行时、裁剪、进程管理、本地库加载、单文件发布、玩家分支横评、多操作入口交互 |
| docs/research/index.md | 文件表加 11-runtime.md；卡点表加 009 状态列；新增 009 调研项段 |
| docs/features/normal-launcher.md | F005 正常启动器，5 个固定字段 |
| docs/features/lan.md | F006 手机连接，5 个固定字段 |
| docs/features/server.md | F007 一键开服，5 个固定字段 |
| docs/features/log.md | F008 日志，5 个固定字段 |
| docs/features/fallback.md | F009 兜底与安全模式，5 个固定字段 |
| docs/features/envelope.md | F010 跨进程统一信封，5 个固定字段 |
| docs/features/ui-framework.md | F011 UI 框架，5 个固定字段 |
| docs/features/index.md | F001-F011 全表、计划登记项清空、G01-G05 |
| docs/checklists/ai-errors.md | A29-A31 |
| docs/checklists/windows-errors.md | W23-W28 |
| docs/records/interface-log.md | I13、连接约定 4 行、S16-S26 |
| docs/index.md | 必读 18 项、11-runtime 分区、009 演示、A29-A31 检查 |
| README.md | 轮次 009、F001-F011 |
| docs/records/rounds.md | 本段落 |
| demos/round-009-coverage.html | 需求覆盖与底层调研运行逻辑 HTML |
| docs/verification/round-009.md | 第 009 轮独立验证报告 |

当轮输入：

| 项 | 值 |
| --- | --- |
| 指令 | 「干」，逐字副本 1 行 |
| 新功能或 UI | 未提供 |
| D06 触发信号 | 未提供 |
| 阶段 | 003-remote.md D05 功能输入阶段，未启动 D07 |
| 偏离 | 9.1 连续未达应停下由用户决定范围；按 18.5 以用户当轮指令继续执行 |

需求 15 节待办推进：

| 需求条目 | 009 处理 | 四值 |
| --- | --- | --- |
| :228 玩家分支启动器可取之处 | 横评页面存在与推广措辞已登记；排名、星级、开源状态标未证实；功能项候选标未证实，不写进实现计划 | 已证实 / 未证实 |
| :229 底层官方文档 | 9 份一手原文落盘 11-runtime.md；2 项未证实；1 项受阻 | 已证实 / 未证实 / 受阻 |
| :230 每轮联网核实现有时间与上游版本状态 | 开工时钟与网络 date 头核对；带认证 /rate_limit 200 | 已证实 |
| :231 电脑端多操作入口交互 | 具体形式未证实，思路保留，不套用手机手势 | 未证实 |

一手补证：

| 主题 | 值 | 锚点 |
| --- | --- | --- |
| Cargo release 默认 | opt-level=3、lto=false、panic="unwind"、codegen-units=16、strip="none"、rpath=false | https://doc.rust-lang.org/cargo/reference/profiles.html |
| DLL 安全搜索模式 | 当前目录第 11 位；禁用时第 8 位 | https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order |
| LOAD_LIBRARY_SEARCH_DEFAULT_DIRS | 0x00001000 | https://technet.microsoft.com/en-us/office/hh310515 |
| std::process 参数 | 不经 shell；cmd.exe / .bat 非标准解码 | https://doc.rust-lang.org/std/process/struct.Command.html |
| CommandExt | creation_flags 与 CREATE_UNICODE_ENVIRONMENT 按位或；raw_arg 不转义 | https://doc.rust-lang.org/std/os/windows/process/trait.CommandExt.html |
| WebView2 进程组 | 单 browser process + 多 renderer + helper，绑定单个 user data folder | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/process-model |
| MSVC 部署 | central / local / static linking | https://learn.microsoft.com/en-us/cpp/windows/deployment-in-visual-cpp |
| 目标三元组 | x86_64-pc-windows-msvc / gnu、aarch64-pc-windows-msvc；Tier 1-3 | https://doc.rust-lang.org/rustc/platform-support.html |

口径与边界：

| 项 | 值 |
| --- | --- |
| 横评页面归属 | PCL2 相关站点，含推广措辞；不作选型结论，见 A29 |
| 未证实项 | CREATE_NO_WINDOW 具体值、std::process 超时 API、WebView2 内存占用关系、本项目单文件发布工具链、横评排名与开源状态、多操作入口形式 |
| 受阻项 | MSVC 部署首轮路径抓取被拒，改用另一路径取得 |
| 008 验证报告 U8 锚点 | 报告写「03-download.md」，实际令牌保护在 docs/research/02-auth.md:57；按 18.1 未改报告，本段登记待复核 |
| src/ | 仍为空 |

功能登记收口：

| 项 | 值 |
| --- | --- |
| 已登记 | F001-F011，11 份 |
| 计划登记项 | 无 |
| 状态 | 全部「已批准」，全部写明未实现、未进入构建 |
| 约束 | G05 锁定状态表述 |

扫描命令语义修复：

| 检查 | 修复前 | 修复后 |
| --- | --- | --- |
| A31 功能状态扫描 | `! grep -L '未实现' …` 在全部命中时仍 exit 0，取反为 1，误报 STATE_FOUND | `test -z "$(grep -L '未实现' …)"`，判定输出为空 |
| 同步位置 | docs/checklists/ai-errors.md、docs/index.md | 断言含义不变，判定 10 份 md 均含未实现标记 |
| 扫描域自我命中 | A29 推广措辞字面量在 docs/research/11-runtime.md，不在 A29 检查域 docs/features/ docs/decisions/ | 无需改动 |

零级凭据扫描命中处置：

| 项 | 值 |
| --- | --- |
| 时点 | 独立验证者收尾自检，13:37-13:38 |
| 命中位置 | `.git/lost-found/other/` 下 5 个 blob 副本 |
| 来源 | git fsck 残留产物，非工作区文件、非 refs 可达对象 |
| 验证者报告 | 收尾自检保留 `exit=1`，按 18.1 未改报告 |
| 改动作者处置 | 删除 `.git/lost-found/`，重跑全仓扫描 |
| 复扫结果 | `NO_CREDENTIAL`、`NO_CREDENTIAL_WORKTREE`、`.git/config` 无命中 |
| git 完整性 | HEAD 不变、tracked 80、工作区仅新增验证报告 |
| 边界 | 凭据事项按第 16 节不展开 |

报告正文哈希口径复核：

| 项 | 值 |
| --- | --- |
| 声明值 | `a137b029ca2a0b23d62308c07578c40029e92160` |
| 复核方式 | 按 `## 哈希声明` 字节偏移切分报告全文，取声明块之前正文算 SHA-1 |
| 复核结果 | 精确切分得 `a137b029ca2a0b23d62308c07578c40029e92160`，一致 |
| 全文哈希 | `53a697bf034434600756e33683cb962b24a3a048`，与正文哈希不同，口径成立 |
| 变更内容哈希 | `f7c60f8bb77ac87e0369e6b48f2e6f0fc725e388`，固定终点复算一致 |
| 验证者自述 | 报告曾截断为 0 字节后重建；两个哈希重建后重新计算并写入声明块 |

未做：
- 源码与 src/ 实现
- 底层统一搭建
- 框架蓝图批准
- 正常模式 UI 实现与构建
- 品牌与字体授权取得
- 加载器逐版本 schema、Notchian 服务端行为、令牌保护、Mojang 官方 RCON 文档、slint 三许可全文补证
- 浏览器内渲染实测
- rustc / cargo 构建验证

## 010

| 落点 | 内容 |
| --- | --- |
| docs/spec/10-round-010-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/research/12-compliance.md | 合规条款、凭据保护、许可证全文、上游版本、阻塞项补证 |
| docs/licenses/index.md | 逐字副本表 12 行、slint 三许可全文段、重复副本处理、L03/L06/L07 |
| docs/licenses/ | 新增 6 份逐字副本与 slint-LICENSES/ 3 份三许可全文 |
| docs/features/credential-guard.md | F012 正版凭据保护，5 个固定字段 |
| docs/features/index.md | F012 入表、G05/G06、009 轮「全部登记」措辞纠错 |
| docs/rules/build-preconditions.md | D06/D07 触发链、L1-L8 前置、X01-X06、B01-B04 |
| docs/research/index.md | 文件表加 12-compliance.md、卡点表加 010 状态列、010 新增调研项段 |
| docs/checklists/ai-errors.md | A31 列表补 F012、A32-A35 |
| docs/checklists/windows-errors.md | W29-W32 |
| docs/records/interface-log.md | I14、S27-S37、合规冲突登记段 |
| docs/index.md | 必读 20 项、12-compliance / build-preconditions 分区、010 演示、检查项 |
| README.md | 轮次 010、F001-F012、合规卡点 |
| docs/records/rounds.md | 本段落 |
| demos/round-010-compliance.html | 合规阻塞与搭建前置运行逻辑 HTML |
| docs/verification/round-010.md | 第 010 轮独立验证报告 |

当轮输入：

| 项 | 值 |
| --- | --- |
| 指令 | 「干」，逐字副本 1 行 |
| 新功能或 UI | 未提供 |
| D06 触发信号 | 未提供 |
| 阶段 | 003-remote.md D05 功能输入阶段，未启动 D07 |
| 偏离 | 9.1 连续未达应停下由用户决定范围；按 18.5 以用户当轮指令继续执行 |

合规冲突发现：

| 编号 | 条款原文 | 现有登记 | 四值 |
| --- | --- | --- | --- |
| X01 | CF03 `save or cache any data obtained through the API or SDK` 禁止 | docs/research/03-download.md 缓存头 sync_at | 已证实 |
| X02 | CF03 同上 | docs/spec/00-requirements.txt:172 默认走国内镜像 | 已证实 |
| X03 | CF02 `conceal your identity or geographic location ... proxy server or VPN` 禁止 | docs/research/03-download.md 6 个上游主机直连 403 | 已证实 |
| X04 | CF01 `unique API Key ... non-transferable and may not be shared with any third party` | docs/spec/00-requirements.txt:171 密钥可选 | 已证实 |
| X05 | CF04 竞争产品范围 | 未取得条款解释 | 未证实 |
| X06 | CF05 配额阈值 | 页面未给数值 | 未证实 |

处置：按 docs/spec/00-requirements.txt:249 与 18.6，X01-X04 落在已登记字段上，进入构建前需用户拍板；本轮未生成下载模块代码、未改 03-download.md 已有字段、未自行选择一条执行另一条忽略。前置条件清单落在 docs/rules/build-preconditions.md。

许可证补证：

| 项 | 值 |
| --- | --- |
| 新增逐字副本 | KCU-Launcher、MultiMC、Forge、NeoForge、Quilt 共 5 份；Prism 与 KCU 同字节未另存 |
| slint 三许可全文 | Royalty-free 2.0 / GPL-3.0-only / Commercial 共 3 份，目录 20 条目 |
| slint 主文件原文 | 三选一、Royalty-free 不含嵌入式、嵌入式需商用许可 |
| 005 轮 L03 | 「三许可全文标未证实」改写为已取得并列具体文件 |
| 重复副本 | slint-LICENSE.md 与 slint-LICENSE.txt 同 sha，删除前者；PrismLauncher-LICENSE.txt 与 KCU 同 sha，删除前者 |
| SPDX | KCU GPL-3.0、Prism GPL-3.0、MultiMC NOASSERTION、Forge NOASSERTION、NeoForge LGPL-2.1、Quilt Apache-2.0 |

凭据保护：

| 项 | 值 |
| --- | --- |
| DPAPI | CryptProtectData 绑定同一用户登录凭据与同一计算机；可选熵加解密需一致；CRYPTPROTECT_LOCAL_MACHINE 放大可解密范围 |
| CredWriteW | 凭据关联当前令牌登录会话，令牌用户 SID 被禁用时失败 |
| F012 | 需求 docs/spec/00-requirements.txt:17 补登记，状态已批准、方案未批准、未实现 |
| C01-C04 | 不用机器标志、凭据不进日志与诊断包、方案未批准、无头模式走同一路径 |
| 未证实 | CRED_PERSIST_* 取值、令牌刷新周期、Azure Client ID |

上游版本状态（需求 :230）：

| 项 | 值 |
| --- | --- |
| 已证实 | HMCL v3.16.4、fabric-loader 0.20.1、wry-v0.57.1、Rust 1.99.1、Prism 11.1.1、slint v1.18.1 |
| 已失败 | NeoForge 与 MinecraftForge 的 tags?per_page=1 均返回 `v99.99` / `cb6f92e`，同名同 sha，不作为版本结论 |
| 时钟 | 沙盒 `Thu Nov  5 22:13:48 CST 2026`；未认证 /rate_limit 404，Date `Thu, 05 Nov 2026 14:13:48 GMT`；带认证 200 remaining 5000 |
| 冲突 | 未认证探测由 001-009 轮的 403 变为本轮 404，如实登记，不沿用旧值 |

玩家分支一手仓库（需求 :228）：

| 项 | 值 |
| --- | --- |
| PrismLauncher/PrismLauncher | GPL-3.0，默认分支 develop，README 6992 字节 |
| MultiMC/Launcher | NOASSERTION，默认分支 develop，COPYING.md 含 Apache 2.0 部分 |
| 实例创建流程 | Add Instance → 选择版本与 modloader 或导入整合包 |
| mmc-pack.json 格式 | 领域知识库片段，标未证实 |
| 功能清单 | 未逐功能核对官方 wiki，标未证实 |

修正记录：

| 位置 | 原值 | 修复 |
| --- | --- | --- |
| docs/research/12-compliance.md 初稿 | `docs/research/index.md:65` 指向 R03 | 改为 `docs/research/index.md R03`，避开行号漂移 |
| docs/research/12-compliance.md 初稿 | `docs/research/02-auth.md:74` 指向实现禁用约束 | 改为约束段描述，实际行 92 |
| docs/features/credential-guard.md 初稿 | `grep -c 'CryptProtectData'` 写输出 4 | 实跑为 0；改用 `grep -c 'cryptprotectdata'` 输出 5，A35 登记 |
| docs/features/index.md G05 | 11 份功能 md | 改为 12 份 |
| docs/checklists/ai-errors.md A31 | 10 个文件 | 加入 credential-guard.md，共 11 个 |
| docs/features/index.md 009 轮措辞 | 「需求第 6、9、17、18、20、21 节功能块已全部登记」 | :17 凭据保护当时未单独成文，010 轮补 F012 并纠错 |

未做：
- 源码与 src/ 实现
- 底层统一搭建
- 框架蓝图批准
- 正常模式 UI 实现与构建
- 品牌与字体授权取得
- X01-X06 用户拍板
- MCIM / BMCLAPI 一手条款、Modrinth 缓存限流条款、加载器逐版本 schema、Notchian 服务端行为、Mojang 官方 RCON 文档补证
- 浏览器内渲染实测
- rustc / cargo 构建验证

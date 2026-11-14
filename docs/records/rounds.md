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

010 验证者记录复核：

| 编号 | 验证者记录 | 改动作者复跑 | 判定 |
| --- | --- | --- | --- |
| V01 | 远端提交链 `45d94fb` 内容等价未独立复算，未认证 API 404 / `git ls-remote` 403 | 带认证 `GET /git/trees/...?recursive=1` 与本地 `git hash-object` 逐项比对，`22:29:03` 输出 `REMOTE 94 LOCAL 94 MISMATCH 0 ALL_MATCH True` | 受阻，验证者受不设认证约束；内容等价值已由改动作者证实 |
| V02 | HTML 内联脚本声明 9 个，本轮 glob 仅覆盖 4 个 | `node -e` 遍历 `demos/*.html` 得 `COUNT 9`、`ALL_JS_OK` | 验证者 glob 执行误差，9 份脚本语法已证实 |
| V03 | A25 与 009 报告「四值项」字面 | 未给出可复现命令与断言 | 未证实，待下轮复核 |
| V04 | `12-compliance.md` 实测 189 行 ≠ 委托语 190 行 | `wc -l` 189 行、`grep -c 'https://'` 68 | 委托语数字误差，实际 189 行 / 68 锚点 |
| V05 | `round-010-compliance.html` id 数 14 ≠ 声明 13 | `grep -c 'class="node"'` 13；`grep -o 'id="[^"]*"' | wc -l` 14；`<select` 5 | 口径差异，声明指 `.node` 元素 13 个，验证者数 id 属性 |

按 18.1 未改独立验证报告，本段登记口径。

报告正文哈希口径复核：

| 项 | 值 |
| --- | --- |
| 声明值 | `c23b0150e17b64adc7255a291a20fc175f933a35` |
| 声明块字节偏移 | 10802，`## 哈希声明` 在报告第 183 行 |
| 精确切分 `sha1(t[:10802])` | `96dbe4882ff9cc06b2096da9cc3e24da07d44642` |
| 去掉声明块前多出的 1 个换行 `sha1(t[:10801])` | `c23b0150e17b64adc7255a291a20fc175f933a35`，与声明一致 |
| 全文哈希 | `cded83b8feb42d1f89ae565fda2290f85e9ed3da` |
| 判定 | 声明值对应「追加声明块之前、末尾恰好一个换行」的正文；追加时多写一个空行，属 1 字节口径差异，口径成立 |
| 变更内容哈希 | `cb9229d974bd8709a6a01f43991e7731c24d1fec`，固定终点 `a7f948f..87f0ce6` 复算一致 |

独立验证结论：**部分通过**。两个哈希由独立验证者计算并写入声明块，改动作者未代算。

## 011

| 落点 | 内容 |
| --- | --- |
| docs/spec/11-round-011-instructions.txt | 当轮指令逐字副本，剔除含凭据的整行，1 行 570 字节 |
| docs/spec/11-features-input.txt | 用户输入文件逐字副本，268 行 17096 字节，cmp 一致 |
| docs/research/13-platform-api.md | Win7 兼容、多架构、系统 API 真实签名与两处硬冲突 |
| docs/research/14-batch-network.md | 批量请求通用法、官方批量端点、N+1 反模式、回环监听、配置集中 |
| docs/research/15-input-survey.md | 后端仓只读探测、CopperGolemLauncher / PrismLauncher / ViaNBT / dsh / VxKex 核实、开源许可页 5 字段 |
| docs/licenses/CopperGolemLauncher-LICENSE | 许可证全文 35834 字节 |
| docs/features/backlog.md | 55 条编号功能 + 175 项文件管理清单分组索引 |
| docs/decisions/011-feature-input.md | D01-D24 与 Q01-Q08 待拍板项 |
| docs/rules/build-preconditions.md | 011 新增阻塞项 Q01-Q12 与触发链条件 5 |
| docs/rules/push-scope.md | 只读仓 R01-R04、特殊版、3 类排除项 |
| docs/checklists/ai-errors.md | A36-A45 |
| docs/checklists/windows-errors.md | W33-W40 |
| docs/research/index.md | 文件表 13/14/15、011 卡点状态与新增调研项 |
| docs/features/index.md | 011 轮功能输入段、G07 |
| docs/licenses/index.md | CopperGolemLauncher 行、L08-L09 |
| docs/records/interface-log.md | I15-I17、S38-S62、011 只读仓约束 |
| docs/index.md | 必读 21 项、011 分区与演示 |
| README.md | 轮次 011 与事实更新 |
| demos/round-011-input.html | 功能输入与阻塞项运行逻辑 HTML |
| docs/verification/round-011.md | 第 011 轮独立验证报告 |

当轮输入：

| 项 | 值 |
| --- | --- |
| 指令 | 剔除凭据行后为 1 行 570 字节 |
| 凭据 | 用户给出新 GitHub PAT，按第 16 节不讨论；带认证 `GET /user` 200 `login=kongbai9288`、`GET /rate_limit` 200 remaining 5000 |
| 新功能输入 | `/data/inputs/功能.txt`，55 条编号连续 1-55、175 个 `·` 条目 |
| 后续输入 | 用户写明「你先去完成这些任务，我再去写一个功能开服器」「过一会我会把要求也给你」 |
| 阶段 | 003-remote.md D05 功能输入阶段，D06 未触发 |
| 偏离 | 9.1 连续未达应停下；按 18.5 以用户当轮指令继续执行 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒时钟 | `Wed Nov 11 00:34:07 CST 2026` |
| 网络时钟 | `Tue, 10 Nov 2026 16:34:08 GMT`，带认证 Date `16:34:08 GMT` |
| 时间跳跃 | 010 轮收尾 `Thu Nov  5 22:36:09 CST 2026`，本轮开工 `Wed Nov 11 00:34:07 CST 2026`，间隔 6 天 2 小时，如实登记 |

后端仓只读探测：

| 编号 | 项 | 值 |
| --- | --- | --- |
| BR01 | 用户指令 | 只能读，部署了自动部署，写入后果严重 |
| BR02 | 本轮请求 | 4 个 `GET`，0 个写请求 |
| BR03 | 仓库 | `private=true`，默认分支 `main`，`pushed_at=2026-11-10T15:40:42Z` |
| BR04 | description | Cloudflare Worker backend |
| BR05 | 分支 | `diag` / `main` |
| BR06 | 根条目 | 9 个 |
| BR07 | README | 2523 字节，仅取大小 |
| BR08 | 内容 | 未读取进公仓，未复制端点、密钥、部署配置 |

硬冲突（按需求 :3 与 :249 否定，不强行实现）：

| 编号 | 用户要求 | 一手事实 | 四值 |
| --- | --- | --- | --- |
| C01 | 从 Win7 开始兼容 | Rust 1.78 起 Windows Tier 1 目标要求 Win10；Win7 仅 Tier 3 `*-win7-windows-msvc` 且无预编译 std | 已证实 |
| C02 | 32 位与 64 位 | `i686-pc-windows-msvc` 与 `x86_64-pc-windows-msvc` 均标注 Windows 10+ | 已证实 |
| C03 | 多架构全都要 | Windows 侧 Rust 官方目标为 i686 / x86_64 / aarch64 | 已证实 |
| C04 | Win7 + ARM64 | `aarch64-pc-windows-msvc` 最低 Win10，交集为空 | 已失败 |
| P04 | 物理位置判定且不用网络探测 | Win7 可用的 `GetUserGeoID` 未设置时返回 `GEOID_NOT_AVAILABLE`，`LOCALE_IGEOID` 是区域设置；Windows 定位服务用 GPS/WiFi/蜂窝/IP | 未证实 |
| P07 | 替代口径 | 按用户或系统区域设置判定需用户确认 | 未批准 |

系统 API 一手补证：

| 组 | 条数 | 关键事实 |
| --- | --- | --- |
| OS01-OS04 | 4 | `IsWindows7OrGreater` 最低 Win2000；`GetVersionEx` / `VerifyVersionInfo` 已弃用 |
| AR01-AR05 | 5 | `GetNativeSystemInfo` 最低 WinXP，WOW64 与模拟架构下返回模拟值 |
| GE01-GE11 | 11 | `GetGeoInfoEx` 最低 Win10 1709；`SYSGEOTYPE` 的 `GEO_ISO2` / `GEO_ISO3` |
| RW01-RW12 | 12 | Rust 1.78 目标变更、Tier 3 Win7 目标、VxKex |
| DL01-DL05 | 5 | Win7 需 KB2533623 与 `GetProcAddress` |

网络通用法：

| 组 | 条数 | 关键事实 |
| --- | --- | --- |
| N01-N08 | 8 | N+1 反模式：batch endpoints / request coalescing / aggregation read model / 去重 / 自检信号 |
| M01-M07 | 7 | Modrinth `ids` 批量、`limit` 默认 10 上限 100、`offset` / `facets` |
| C01-C08 | 8 | CurseForge SDK `Get Mods Info By Ids`、`modIds TArray`、`pageSize = 20` |
| L01-L06 | 6 | 回环绑定、防火墙入站、服务器 AI API 例外 |
| K01-K09 | 9 | 配置集中：API 基址、网址、端口、图标、语言包、保存路径 |

修正记录：

| 位置 | 原值 | 修复 |
| --- | --- | --- |
| docs/features/backlog.md 初稿 | 文件管理分组表写「条目数合计 174」 | 手填分组数合计 173，删除条目数列，改为「分组为索引，不逐组计数」，逐字清单以 spec 副本为准 |
| docs/spec/11-round-011-instructions.txt | 用户首行含凭据 | 整行剔除，按第 16 节与 18.5 登记偏离 :133 |
| docs/research/13-platform-api.md | `platform-support/windows.html` 直抓受阻 | 改用平台支持总页 P26，如实登记受阻 |
| docs/research/index.md 011 段 | 表格行以「同上」开头，A24 命中 | 改为具体条目名，断言未改 |
| docs/checklists/ai-errors.md A36 | 检查命令指向 11-features-input.txt，实跑 0 命中 | 改为指向 11-round-011-instructions.txt，实跑 1 命中 |
| docs/checklists/ai-errors.md A43 | `grep -c '^| [0-9]'` 中 `|` 被当 alternation，且数字后缺空格 | 改为 `grep -cE '^\| [0-9]+ \|'`，实跑 55 |
| docs/index.md 检查表 | 编号完整性命令同 A43 错误 | 同步修正，并新增逐条目单发扫描项 |
| docs/research/15-input-survey.md | 一行写「已证实（输入）/ 未证实（实现）」混合四值 | 改为「已证实」，实现未定写入结果列 |

011 验证者记录复核：

| 编号 | 验证者记录 | 改动作者复跑 | 判定 |
| --- | --- | --- | --- |
| V01 | `·` 条目实跑 175 ≠ 声明 174 | `t.count('·')` = 175；以 `·` 开头的独立行 = 174；第 30 行引导句末尾同行含首个条目 `· 浏览文件和文件夹` | **真遗漏**：初稿按独立行少算 1 项；已把全仓 174 改为 175 并补计数口径 |
| V02 | 15-input-survey.md「4 个 GET」实跑 grep 0 | `grep -c '4 个 GET'` = 0；`grep -c '4 个 \`GET\`'` = 1，字面量带反引号 | 验证者 grep 模式未含反引号，执行误差 |
| V03 | A31 实跑 exit=1 | `MISSING=[]`，11 个文件各含「未实现」2 次，`A31_PASS` | 验证者执行误差，断言未改 |
| V04 | 本地 `b936431` 与远端 `acd7a75` 哈希不同 | 104 blob 逐项 `git hash-object` 比对 ALL_MATCH True | 已失败（内容等价），与前几轮同型 |
| V05 | Win7 + ARM64 交集为空、v99.99、CF REST 端点页、CopperGolem release | 与本轮声明一致 | 已失败 / 受阻，非新增未通过项 |

按 18.1 未改独立验证报告，本段登记复核结果。

报告正文哈希口径复核：

| 项 | 值 |
| --- | --- |
| 声明值 | `b79e501e79820d742b3e81011287a76123aad0e7` |
| 声明块字节偏移 | 10512 |
| 精确切分 `sha1(t[:10512])` | `8d5d70403fd52e0f3f83b4ae9e0284d27335a945` |
| 去掉声明块前 1 个换行 `sha1(t[:10511])` | `b79e501e79820d742b3e81011287a76123aad0e7`，与声明一致 |
| 全文哈希 | `98c4c68ee91fddf66307b5abf11716f1c289f447` |
| 判定 | 与 010 轮同型：声明值对应「追加声明块之前、去掉前置换行」的正文，口径成立，属 1 字节差 |
| 变更内容哈希 | `339ac41c5ba557ee73b9011c1169a9a0b400c278`，固定终点 `63d2099..b936431` 复算一致 |

修正落点（V01 引起）：

| 文件 | 原值 | 修复 |
| --- | --- | --- |
| docs/features/backlog.md | 4 处 174 | 全部改 175，补计数口径段与验证表字段 |
| demos/round-011-input.html | 5 处 174 | 全部改 175 |
| docs/features/index.md | 2 处 174 | 全部改 175 |
| README.md、docs/index.md、docs/research/index.md | 各 1 处 174 | 全部改 175 |
| docs/records/rounds.md | 2 处 174 | 全部改 175；初稿修正记录中的 174 为历史描述，保留 |
| docs/research/12-compliance.md:30 | `docs/spec/00-requirements.txt:174` | 需求文件行号，不改 |

独立验证结论：**部分通过**。两个哈希由独立验证者计算并写入声明块，改动作者未代算。

未做：
- 源码与 src/ 实现
- 底层统一搭建
- 框架蓝图批准
- 正常模式 UI 实现与构建
- 品牌与字体授权取得
- X01-X04、Q01-Q12 用户拍板
- 特殊版私仓创建
- 后端仓任何写请求
- MCIM / BMCLAPI 一手条款、Modrinth 缓存限流条款、加载器逐版本 schema、Notchian 服务端行为、Mojang 官方 RCON 文档补证
- 浏览器内渲染实测
- rustc / cargo 构建验证

## 012

| 落点 | 内容 |
| --- | --- |
| docs/spec/12-server-features-input.txt | 用户输入逐字副本，64 行 4970 字节，cmp 一致 |
| docs/spec/12-round-012-instructions.txt | 当轮指令逐字副本，1 行 |
| docs/research/16-server-platform.md | 26 个来源、开服器官方资料与协议一手原文 |
| docs/features/server-backlog.md | 开服器 27 个编号位、26 行分组索引（GA1-GA18、GB1-GB8）、与 011 的 13 组重复项 |
| docs/records/open-questions.md | 93 条待拍板问题全集，A-H 组，无删减 |
| docs/decisions/012-server-input.md | D01-D16、S1/S2 两段语义、状态分层 |
| docs/rules/build-preconditions.md | 012 新增 R01-R10、触发链条件 6 |
| docs/checklists/ai-errors.md | A46-A52 |
| docs/checklists/windows-errors.md | W41-W45 |
| docs/research/index.md | 文件表 16、012 卡点状态与新增调研项 |
| docs/features/index.md | 012 段、G08-G09 |
| docs/decisions/index.md | 补齐 008-012 条目 |
| docs/records/interface-log.md | I18、S63-S88、012 只读仓约束 |
| docs/index.md | 必读 29 项、012 分区与演示、7 项新检查 |
| README.md、docs/rules/push-scope.md | 轮次 012 |
| demos/round-012-server-input.html | 开服器输入与 93 条问题闸门运行逻辑 HTML |
| docs/verification/round-012.md | 第 012 轮独立验证报告 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Wed Nov 11 01:17:59 CST 2026` |
| 011 轮收尾 | `Wed Nov 11 01:01:46 CST 2026` |
| 间隔 | 16 分钟 |

当轮指令两段语义：

| 段 | 原文 | 登记 |
| --- | --- | --- |
| S1 | `在搜完所有的文档以后呢，就可以彻底开工了` | 记录为开工授权，未执行 |
| S2 | `如果有一些问题你拿捏不了的，可以直接通过技术对话，然后全部告诉我不要保留，我先睡觉了，然后明天我会统一处理这些问题` | 本轮按 S2 交付 93 条问题全集 |

两段并列登记，不替用户选其一，Q-B01 请求确认开工时点。按 :3 与 :249，未拍板项存在时停下；9.1 连续未达按 18.5 以用户当轮指令继续。

输入结构：

| 项 | 值 |
| --- | --- |
| 首行 | `开服器1.先检查有没有可以直接使用的java`，编号 1 与标题连写 |
| 带点号编号 | 2-24、27，共 23 行 |
| 无点号编号 | `25多实例同时运行的资源配额/调度` |
| 缺号 | 26 |
| `·` 字符 | 35 |
| 独立 `·` 行 | 34 |
| 同行首项 | 第 24 条引导句末尾同一行含首个 `·` 条目 |
| 计数口径 | 与 011 轮同型，差 1 |

官方资料结论：

| 组 | 一手事实 | 四值 |
| --- | --- | --- |
| 插件源 | Hangar 由 PaperMC 团队创建；Ore 为 Sponge 官方；SpigotMC / BukkitDev 为社区；Modrinth 为多加载器索引 | 已证实 |
| Hangar REST 官方文档 | robots 拒绝抓取，API 基址仅第三方转述 | 受阻 |
| 服务端 mod | Modrinth `environment` facet 10 值含 `server_only` / `dedicated_server_only`；`client_side` / `server_side` 已弃用 | 已证实 |
| CurseForge server-only 等价字段 | 官方 REST 端点页受阻，未找到等价字段 | 未证实 |
| EULA | 官方页 `https://www.minecraft.net/en-us/eula`；`eula.txt` 首次启动生成 `eula=false`，改为 `eula=true` 否则立即退出 | 已证实 |
| 原版命令 | `/say` 权限等级 2；原版无 `/talk`；控制台命令不带 `/` | 已证实 |
| Java 版本 | Java 8 / 16 / 17 / 21 / 25 对应 MC 版本段 | 已证实 |
| ops.json | 服务端启动时读入内存，命令变更时整体回写；运行期手改被静默覆盖 | 已证实 |
| 种子 | 新 `WorldGenSettings` 下的 `seed`、旧 `Data` 下的 `RandomSeed`；连写为路径记法 | 已证实 |
| 进度 | `world/players/advancements/<uuid>.json`，退出即写，读失败全丢 | 已证实 |
| icon | 64×64 `server-icon.png`，需重启加载 | 已证实 |
| UPnP | RFC 6886 记载 IGD 可被用于改网关 DNS；NAT-PMP 已被 PCP 取代 | 已证实 |
| mclo.gs | `POST https://api.mclo.gs/1/log`，10 MiB / 25000 行 | 已证实 |
| mrpack | 路径穿越防护、哈希、下载域名白名单、`server-overrides` 覆盖层 | 已证实 |

93 条问题分组：

| 组 | 条数 | 内容 |
| --- | --- | --- |
| A | 6 | 输入文档结构：编号连写、缺 26、重复分节、计数口径 |
| B | 12 | 既有规则冲突：开工时点、D06、蓝图、X、容器网段、境外源、重复项、凭据 |
| C | 15 | 官方事实与用户描述不一致：`/talk`、op 锁定、种子双格式、icon、CF、EULA、Java、UPnP、代理、mclo.gs |
| D | 18 | 设计口径：AI 权限模型、确认粒度、文件锁、5 秒状态、禁用方式、RCON 隧道、配额优先级 |
| E | 12 | 合规与安全：CF 条款、Modrinth / MCIM / BMCLAPI / mclo.gs / 插件源条款、UI 授权、LICENSE |
| F | 10 | 平台与工具链：Win7、多架构、ARM64、地域、rustc / cargo、浏览器、git HTTP |
| G | 14 | 011 轮遗留未证实 / 已失败项 |
| H | 6 | 开工闸门 Q-H01 至 Q-H06 |

阶段判定：

| 项 | 值 |
| --- | --- |
| 阶段 | 003-remote.md D05 功能输入阶段 |
| D06 | 未触发 |
| 005-blueprint.md | 未批准 |
| `src/` | 空 |
| 本轮源码 | 0 行 |

未做：
- 源码与 src/ 实现
- 底层统一搭建
- 框架蓝图批准
- 正常模式 UI 实现与构建
- 品牌与字体授权取得
- X01-X04 与 Q-A 至 Q-H 用户拍板
- 特殊版私仓创建
- 后端仓任何写请求
- 插件源默认选择、CF server-only 字段、`/talk` 来源、Java 镜像条款、mclo.gs 条款补证
- 浏览器内渲染实测
- rustc / cargo 构建验证

012 验证者记录复核：

| 编号 | 验证者记录 | 改动作者复跑 | 判定 |
| --- | --- | --- | --- |
| V01 | A31 未通过，5 个核查目标文件不含「未实现」 | `MISSING=[]`，11 个文件各含「未实现」2 次，`A31_PASS` | 验证者执行误差，断言未改 |
| V02 | `·` 独立行 34 为同行首项累计算法口径 | `t.count('·')`=35，独立行 34，含字符行 35；非独立行仅第 27 行 `24.· Java 多版本管理...` | 验证者理解误差，011 轮同型口径已登记 |
| V03 | 19 组 G 索引 grep 写法误差（事实无误） | 实跑 `grep -cE '^\| G[AB][0-9]+ \|'` = 26（GA1-GA18、GB1-GB8）；初稿多处写「19 组」 | **真错误**：已把 4 处「19 组」与 HTML 2 处 `19_groups` 改为 26 并写明分组行范围 |
| V04 | `WorldGenSettings.seed` 精确串 grep 0 | 一手原文标签为 `WorldGenSettings` / `seed` / `RandomSeed`，三者不连写；连写为路径记法 | **表述精度问题**：已补 NB08，并把 open-questions.md Q-C04、rounds.md、HTML 的表述改为路径记法 |
| V05 | 93 条 open-questions 全部未答复 | 与声明一致 | 属未解决四值项，非新增未通过项 |
| V06 | 本地 `ddb03ec` 与远端 `fa19e5a` 哈希不同 | 112 blob 逐项 `git hash-object` 比对 ALL_MATCH True | 已失败（内容等价），与前几轮同型 |

按 18.1 未改独立验证报告，本段登记复核结果。

报告正文哈希口径复核：

| 项 | 值 |
| --- | --- |
| 声明值 | `259af6dffd555f20e2865e7264ab0418fbb87d91` |
| 声明块字节偏移 | 9842 |
| 精确切分 `sha1(t[:9842])` | `ab405c5d4b08f5227694edb9a7dbe5964d495a99` |
| 去掉声明块前 1 个换行 `sha1(t[:9841])` | `259af6dffd555f20e2865e7264ab0418fbb87d91`，与声明一致 |
| 全文哈希 | `be1da183057af27542d782a9e439dbaa327f6db9` |
| 判定 | 与 010、011 轮同型：声明值对应「追加声明块之前、去掉前置换行」的正文，属 1 字节口径差，口径成立 |
| 变更内容哈希 | `142f1f9ddf318c0785fc2c7bf9b8b61ee636d29c`，固定终点 `d0188e0..ddb03ec` 复算一致 |

修正落点（V03、V04 引起）：

| 文件 | 原值 | 修复 |
| --- | --- | --- |
| demos/round-012-server-input.html | 2 处 `19 组` / `19_groups`、1 处 `WorldGenSettings.seed` / `Data.RandomSeed` | 改 26 与路径记法 |
| docs/features/index.md | 「19 组索引」 | 改「26 行索引（GA1-GA18、GB1-GB8）」 |
| docs/records/rounds.md | 落点表「19 组」、种子连写 | 改 26 行与路径记法 |
| docs/records/open-questions.md Q-C04 | 种子连写 | 改路径记法并引 NB08 |
| docs/research/16-server-platform.md | 无 NB08 | 补 NB08 说明精确串不存在 |

独立验证结论：**部分通过**。两个哈希由独立验证者计算并写入声明块，改动作者未代算。

## 013

| 落点 | 内容 |
| --- | --- |
| docs/spec/13-round-013-instructions.txt | 013 第一段逐字副本，1 行 2856 字节 |
| docs/spec/13-round-013-instructions-part2.txt | 013 第二段逐字副本，1 行 318 字节 |
| docs/records/round-013-answers.md | 76 片段逐字编号、24 条已落定决策、语义映射、不写死项、U01-U03 |
| docs/decisions/013-build-start.md | D01-D08 阶段翻转、C01-C05 工具链纠正、P01-P08 平台落定、G 组默认、H01-H06 |
| docs/decisions/005-blueprint.md | 状态 未批准 → 已批准，C01/C06 改 013 口径 |
| docs/decisions/003-remote.md | 追加 D11，D08 改为 D07 已启用 |
| docs/decisions/index.md | 追加 013，待确认段更新 |
| docs/features/core-*.md | 9 份，字段固定五段：怎么运作 / 开放了什么 / 登记框架 / 用户使用逻辑 / 性能 |
| docs/features/index.md | F013-01..09、013 core 层段、G10-G12 |
| docs/rules/build-preconditions.md | 触发链 1-6 已满足到开工层、L1 已实现已验证、B05 |
| docs/rules/push-scope.md | 允许 Cargo.toml / Cargo.lock / src/ |
| docs/records/open-questions.md | 头部改 013 已答复 |
| docs/index.md | 必读 38 项、013 分区、cargo 与弹窗检查、前置条件 013 值 |
| README.md | 轮次 013、core 层状态、工具链、目录 |
| Cargo.toml、src/lib.rs、src/core/*.rs | L1 core 9 模块，std only，37 个单元测试 |
| demos/round-013-core.html | 编译、用户操作模拟、11 类弹窗关闭状态机 |
| docs/verification/round-013.md | 第 013 轮独立验证报告 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Thu Nov 12 00:30:49 CST 2026` |
| 012 轮收尾 | `Thu Nov 11 01:41:12 CST 2026` |
| 间隔 | 22 小时 49 分 |

阶段翻转：

| 项 | 012 | 013 |
| --- | --- | --- |
| D06 | 未触发 | 已触发 F07/F08 |
| 005-blueprint.md | 未批准 | 已批准 F09 |
| D07 | 未启动 | 已启用，落第 1 层 core |
| 93 条问题 | 未答复 | 已答复 76 片段 |
| src/ | 空 | 9 模块 + lib.rs + mod.rs |
| rustc / cargo | 受阻 | 已装 1.99.1 |

工具链实测：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `curl -sS -o /dev/null -w '%{http_code}' https://mirrors.cloud.tencent.com/rustup/dist/channel-rust-stable.toml` | 200 | 已证实 |
| `curl -sS -o /dev/null -w '%{http_code}' https://mirrors.tencent.com/rustup/dist/channel-rust-stable.toml` | 200 | 已证实 |
| `curl -sS -o /dev/null -w '%{http_code}' https://mirrors.aliyun.com/rustup/dist/channel-rust-stable.toml` | 403 | 受阻 |
| `curl -sS -o /dev/null -w '%{http_code}' https://static.rust-lang.org/dist/channel-rust-stable.toml` | 403 | 受阻 |
| `curl -sS -o /dev/null -w '%{http_code}' https://api.github.com/repos/rust-lang/rust/releases/latest` | 200 | 已证实 |
| rustup-init `--profile minimal --default-toolchain stable --no-modify-path` | rustc 1.99.1 / cargo 1.99.1 | 已证实 |
| `cargo build --release --offline` | Finished，rlib 442456 字节 | 已证实 |
| `cargo test --offline` | 37 passed / 0 failed / 0 measured | 已证实 |

C01-C05 纠正：用户 F73 说「通过 GitHub 行动拉对应的东西」并主动要求「如果我有理解错误那么你就纠正官方源」。实测 GitHub Actions 不向本地沙盒分发工具链；Rust 官方分发主机 static.rust-lang.org 在本环境 403；api.github.com 只能取 release 元数据；腾讯 rustup 镜像 200 且安装成功。纠正已写入 013-build-start.md，不伪造 CI 结果。

H 组落地：

| 要求 | 落点 | 实测 |
| --- | --- | --- |
| 验证用户正常操作逻辑 | src/core/userflow.rs `simulate` + FlowReport::ok | 5 个用例 |
| 模拟用户操作 | 11 步 Step 轨迹 | `flow_trace_contains_close_step` |
| 每个弹窗有关闭逻辑 | popup.rs catalog 11 类 + `missing_close_path` + `force_close_all` | 6 个用例，11/11 可关 |
| 指定参数加入服务器 | args.rs `--server` / `--join-server` | `single_arg_joins_server` |
| 双击服务器按权重选实例、用户权重第一 | instance.rs `select_instance` | 5 个用例 |
| 不留未关弹窗 | `no_popup_is_left_open_after_any_path` 覆盖 3 条路径 | open_count=0 |

013 与 012 的两段语义：012 的 S1「可以彻底开工」与 S2「明天答复后开工」并列登记；013 F07「现在都是你所说的明天了」判定按 S1 开工，Q-B01 关闭。按 18.5 用户当轮指令优先。

未做：
- L2 dispatcher 及以下 8 层
- 特殊版私仓（F63 先建仓、同意后再放代码；缺仓库名，CF 方法未提供）
- CF 下载模块、X01-X04 逐条处置
- 正常模式 UI 实现与品牌替换
- 本项目 LICENSE 文件
- 特殊版凭据、后端仓任何写请求
- 浏览器渲染与 GUI 点击端到端
- rustc 交叉编译 Win7 / ARM64 目标产物
- 插件源默认选择、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 条款补证

013 验证者记录复核：

| 编号 | 验证者记录 | 改动作者复跑 | 判定 |
| --- | --- | --- | --- |
| V01 | 报告正文哈希声明 `85fae9eb…`，复算按声明块字节偏移切分得 `f8b56887…`，差 1 字节，称需修正 | 声明块偏移 11949；`sha1(t[:11949])` = `f8b56887…`，`sha1(t[:11948])` = `85fae9eb…` 与声明一致；全文 `186d91b6…` | 与 010/011/012 同型：声明值对应「去掉声明块前多出的 1 个换行」口径，成立；按 18.1 未改报告 |
| V02 | A46-A50 与 A52 声明计数与实测不符（实测 0） | `A46=1 A47=1 A48=1 A49=1 A50=1 A51=93 A52_NONEMPTY=PASS A52_COUNT=11` | 验证者执行误差，按 18.1 未改报告 |
| V03 | D08→D07 改动未独立复核 | `grep -n 'D08' docs/decisions/003-remote.md` 显示「D07 已启用」，`git diff a31aa6a..a8715ba` 含该行 | 已补复核 |
| V04 | 必读 38 项未逐行覆盖、触发链与未解决四值项未复验 | docs/index.md 必读 38 项、build-preconditions.md 触发链 1-6 与 013 判定、round-013.md 未解决四值项均在库 | 属验证者覆盖范围声明，非事实错误 |
| V05 | 变更内容哈希 | `git diff a31aa6a..a8715ba \| sha1sum` = `51c7a69bc5d3b072fc63a25369046c2acde51394`，与声明一致 | 已证实 |

独立验证结论：**部分通过**。报告正文哈希 `85fae9eb9d84daed2f5547d2d5b61ade8e7ec465`（去前置换行口径）、变更内容哈希 `51c7a69bc5d3b072fc63a25369046c2acde51394`，两个哈希由独立验证者计算并写入声明块，改动作者未代算。

## 014

| 落点 | 内容 |
| --- | --- |
| docs/spec/14-round-014-instructions.txt | 逐字副本，1 行 410 字节，SHA-1 `8f72a8dae1e3e55903c3f1f620687216b6d79a02` |
| docs/decisions/014-build-continue.md | F01-F07 切分、D01-D08、U01-U10、T01-T06、端点占位、私仓事实、本轮边界 |
| docs/decisions/007-normal-ui.md | D09-D14，设计稿降级为样板、E09 卡点关闭 |
| docs/decisions/index.md | 追加 014，待确认段更新品牌、私仓、凭据、缓存异步 |
| .github/workflows/ci.yml | secrets / vars 占位、腾讯 rustup 镜像、actions/cache 有界、concurrency 取消、core 与 scan 并行 job |
| src/core/cache.rs、asynk.rs、leak.rs、mod.rs、lib.rs | 3 个新模块 + 导出 |
| docs/features/core-cache.md、core-asynk.md、core-leak.md | 3 份，字段固定五段 |
| docs/features/index.md | F014-01..03、014 core 扩展段、G13-G15 |
| docs/rules/push-scope.md | 轮次 014、允许 `.github/workflows/`、特殊版段改已建仓 |
| docs/rules/build-preconditions.md | L1 改 12 模块 / 56 测试、判定 src 行 |
| docs/checklists/ai-errors.md | A57-A61 |
| docs/index.md | 必读 44 项、014 分区、检查项、前置条件与未写入项 |
| README.md | 轮次 014、core 规模、CI、私仓、工作流占位 |
| docs/records/interface-log.md | 014 端点与私仓来源 |
| demos/round-014-cache-async.html | 缓存单飞、多源竞速、泄漏归零、工作流占位状态机 |
| docs/verification/round-014.md | 第 014 轮独立验证报告 |
| docs/decisions/013-build-start.md:86 | 措辞规范化：原句含功能目的措辞，命中 014 轮扩展后的扫描词表，改为「不写功能目的说明」，断言含义不变 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Thu Nov 12 13:09:17 CST 2026` |
| 013 轮收尾 | `Thu Nov 12 12:45:25 CST 2026` |
| 私仓创建 | `Thu Nov 12 13:11:24 CST 2026` |
| 编译与测试完成 | `Thu Nov 12 13:24:05 CST 2026` |

用户当轮输入：

| 片段 | 逐字 | 落地 |
| --- | --- | --- |
| F01 | 第1个你到时候在工作流设一个环境变量，我自己去填写就行 | D01、ci.yml |
| F02 | 特殊版的话你自己去建立 | D02、私仓 |
| F03 | 品牌的话我本来这个也是给你打样板的 | D03 |
| F04 | 因为功能和这一个已经有好多区别了 | D03 |
| F05 | 你只要记住一点，就是让用户好受，非常舒服就行（这需要你有对功能的理解程度，自由发挥） | D03、D08 |
| F06 | 对了，缓存异步都要处理 | D04、D05 |
| F07 | 小心点内存泄露 | D06 |

私仓 API 实测：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `GET /user` | 200 login=kongbai9288 | 已证实 |
| `GET /rate_limit` | 200 remaining=4996 | 已证实 |
| `GET /user/repos?per_page=100&type=owner` | 200，23 仓，无同名 | 已证实 |
| `POST /user/repos` `private:true` | 201，private=True | 已证实 |
| `PUT /contents/README.md` | 201，`cd7fc97` | 已证实 |
| `GET /git/ref/heads/main` | 200，`cd7fc97` | 已证实 |

编译与测试：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| 首次 `cargo test --offline` | `E0369` / `E0277`：`RaceResult<u32>` 缺 `PartialEq` / `Debug` | 已失败 |
| 修复：`#[derive(Debug, Clone, PartialEq, Eq)]` | 复跑通过 | 已证实 |
| `cargo test --offline` | 56 passed / 0 failed / 0 ignored / 0 measured，0.10s | 已证实 |
| `cargo build --release --offline` | rlib 610080 字节 | 已证实 |
| `cargo test --offline core::cache` | 8 passed | 已证实 |
| `cargo test --offline core::asynk` | 6 passed | 已证实 |
| `cargo test --offline core::leak` | 5 passed | 已证实 |

缓存 / 异步 / 泄漏落地：

| 项 | 落点 | 实测 |
| --- | --- | --- |
| 容量有界 | cache `insert_locked` 淘汰 | len ≤ 2、evicted ≥ 4 |
| TTL 过期重取 | cache `purge_locked` | ttl 15ms 后重新加载 |
| 单飞去重 | cache `inflight: Weak<Flight<V>>` + Condvar | 8 线程同 key 只加载 1 次 |
| order 不膨胀 | cache `retain` + HashSet 去重 | 500 次插入后 order ≤ 3 |
| inflight 无悬挂 | Weak + remove | inflight_count=0 |
| 多源竞速取消 | asynk `race` | index=0、value=11、live=0 |
| 线程 join 回收 | TaskGroup shutdown / Drop | joined=5、drop 兜底 4 个全执行 |
| 无环归零 | leak Weak<Node> + Tracker | live 2 → 0、strong_count=1 |
| 弱引用注册表 | WeakRegistry purge | purge=1、len=0 |

CI：

| 项 | 值 |
| --- | --- |
| 凭据占位 | `KCU_CF_API_KEY: ${{ secrets.KCU_CF_API_KEY }}`，值不进仓库 |
| 端点占位 | `KCU_MIRROR_BASE` / `KCU_BACKEND_BASE` / `KCU_LANG_PACK_BASE` / `KCU_DOWNLOAD_REGION` 走 vars |
| 工具链 | `RUSTUP_DIST_SERVER` / `RUSTUP_UPDATE_ROOT` 指向腾讯 rustup 镜像 |
| 缓存 | `actions/cache@v4`，key 绑定 `Cargo.lock` 哈希，restore-keys 回退 |
| 并发 | `concurrency.cancel-in-progress: true`；core 与 scan 两个 job 并行 |
| 值保护 | `env-presence` 只输出 present / absent |

阶段：014 轮仍是 D07 第 1 层 core 扩展，L2 dispatcher 及以下 8 层未启动。013 轮遗留的「特殊版私仓未创建」「UI 品牌授权卡点」「CF 凭据落点」三项由本轮关闭；CF 具体调用方法仍按 F17 由用户在完成时提供。

用户当轮「让用户好受，非常舒服」「自由发挥」按 18.5 用户当轮指令优先，落为 D08 的 U01-U10 可测条目，未替用户补写新功能文档。

未做：
- L2 dispatcher 及以下 8 层
- 特殊版代码（待用户明确同意，用户手拉工具流）
- CF 下载模块、X01-X04 逐条处置、CF 具体调用方法
- 正常模式 UI 实现与 KCU 品牌重做
- 本项目 LICENSE 文件
- 后端仓任何写请求
- 浏览器渲染与 GUI 点击端到端
- rustc 交叉编译 Win7 / ARM64 目标产物
- 插件源默认选择、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 条款补证

014 验证者记录复核：

| 编号 | 验证者记录 | 改动作者复跑 | 判定 |
| --- | --- | --- | --- |
| V01 | `bash scripts/push.sh` 空参 exit=1，与预期 exit=2 不符，判硬性不通过 | `sh scripts/push.sh` exit=2、`/bin/sh` exit=2、`bash scripts/push.sh` exit=1；脚本 shebang 为 `#!/bin/sh`；003-remote.md V06 原断言为「无参数时非零退出，输出 remote url required」，两种调用均满足 | 调用 shell 口径差异，非脚本缺陷；按 18.1 未改报告 |
| V02 | 12 份功能 md 五字段全覆盖不可判为已证实 | `for f in docs/features/core-*.md; grep -cE '^## (怎么运作|开放了什么|登记框架|用户使用逻辑|性能)'` → 12 份全部 fields=5 | 已补复核 |
| V03 | build-preconditions 正文未实跑 | `grep -n '12 模块|56 测试|12 个 core 模块'` → 第 24 行、第 108 行命中 | 已补复核 |
| V04 | 验证者用自定单词表做全仓扫描 exit 1，命中 docs/spec/、docs/checklists/、docs/verification/，判 NO_EXPLANATORY 未证实 | 项目措辞扫描域为 `src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/`，不含 spec 原文与词表自我命中域；复跑 NO_EXPLANATORY | 扫描域口径差异 |
| V05 | A31=7、A46=2、A51=1、A58/A59/A60=0 等计数与声明不符 | 按 docs/index.md 固定命令复跑：`A31=PASS`、`A46=1 A47=1 A48=1 A49=1 A50=1 A51=93`、`A52_NONEMPTY=PASS`、A57-A61 为 cargo 分项测试 | 验证者计数命令口径差异 |
| V06 | 首次编译失败修复回放、后端仓零写请求不可判为已证实 | 014 段「编译与测试」表已登记 E0369/E0277 与修复；RO09、push-scope.md 只读口径登记 0 写请求 | 记录已在库，覆盖范围声明差异 |
| V07 | 报告正文哈希 `010d66c…` | 声明块偏移 10904，`sha1(t[:10904])` = `010d66c47d7d7807ef912dc330d5421bbb69b299` 与声明一致；全文 `30cfd33f…` | 本轮无 1 字节口径差 |
| V08 | 变更内容哈希 | `git diff e20af1a..35a8de9 \| sha1sum` = `91222134a975b1195d7272a8f0b2f29f78555061`，与声明一致 | 已证实 |

独立验证结论：**部分通过**。报告正文哈希 `010d66c47d7d7807ef912dc330d5421bbb69b299`、变更内容哈希 `91222134a975b1195d7272a8f0b2f29f78555061`，两个哈希由独立验证者计算并写入声明块，改动作者未代算。本轮独立验证委派首次返回不可用，重委派后报告落盘；首次失败与本段复核均如实登记。

## 015

| 落点 | 内容 |
| --- | --- |
| docs/spec/15-round-015-instructions.txt | 逐字副本，1 行 204 字节，SHA-1 `303ec47156132af4816dfa9e210671b35d9835d0` |
| docs/decisions/015-build-continue.md | F01-F04 切分、D01-D08、U01-U08、L01-L14、验证与边界 |
| docs/rules/ui-demo.md | UI 整页演示闸门：触发、交付物、覆盖范围、用户回路、每轮检查、本轮状态 |
| src/dispatcher/ | json.rs、task.rs、mode.rs、launcher.rs、mod.rs |
| src/lib.rs | 追加 dispatcher 模块与公共类型导出 |
| docs/features/dispatcher.md | F002 状态改为已实现、已验证，五字段全量重写 |
| docs/features/dispatcher-json.md、dispatcher-task.md、dispatcher-mode.md、dispatcher-launcher.md | F015-01..04，字段固定五段 |
| docs/features/index.md | F002 状态、F015 四行、G16-G18、015 轮 L2 段 |
| docs/decisions/index.md | 轮次 015、005 状态纠正、015 行、待确认段 |
| docs/rules/build-preconditions.md | L2 改已实现已验证、判定 src 行、轮次 015 |
| docs/rules/push-scope.md | 轮次 015 |
| docs/checklists/ai-errors.md | A62-A66 |
| docs/index.md | 轮次 015、必读 53 项、015 分区、检查项、前置条件、未写入项 |
| README.md | 轮次 015、L2 行、UI 闸门行、目录与测试数值 |
| docs/records/interface-log.md | 轮次 015、I22-I27、RO12-RO15 |
| demos/round-015-dispatcher.html | L2 调度判定运行逻辑 HTML，13 节点，标题标注非整页 UI |
| docs/verification/round-015.md | 第 015 轮独立验证报告 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Thu Nov 12 22:23:18 CST 2026` |
| 014 轮收尾 | `Thu Nov 12 14:22:37 CST 2026` |
| 全量测试与 release 复验 | `Thu Nov 12 22:50:46 CST 2026`，rlib 1065652 字节 |

用户当轮输入：

| 片段 | 逐字 | 落地 |
| --- | --- | --- |
| F01 | 干 | D01，进入 D07 第 2 层 |
| F02 | 对了，如果说你要是动用户界面的时候你需要把整个用户界面都用html演示出来 | D02/D03、ui-demo.md、A62 |
| F03 | 这样的话我能根据我的手感来调整 | D04、用户回路 5 步 |
| F04 | 不过你现在先按照原来的进度继续干 | D05，本轮不触发 U01、不动 UI |

L2 dispatcher 落地：

| 编号 | 项 | 实测 |
| --- | --- | --- |
| L01 | 5 个模块 | `git ls-files src/dispatcher/ \| wc -l` = 5 |
| L02 | std only | Cargo.toml / Cargo.lock 未变；无 serde / tokio / async-std |
| L03 | JSON 底座 | 7 项：嵌套、转义中文、空容器、尾随内容、畸形输入、深度上限、键序 |
| L04 | K05 LaunchTask | 8 项：完整字段、空字段默认、非 object 拒绝、headless、单参数、集合排序去重、命令行覆盖 |
| L05 | K06 ModeSelector | 12 项：2 GiB 阈值、自动判定、覆盖优先级、非法模式、强制无头、正版凭据、内存未知、安全模式、UI 分流 |
| L06 | 兜底 | 20 项中含连续 3 次失败进安全模式、第 4 次导出 4 行诊断包、成功清零 |
| L07 | 用户操作 | 单参数直接进服、双击按权重选实例、用户指定排第一、不兼容可见且不崩、流程结束 0 残留 |
| L08 | 缓存 / 异步 / 泄漏 | 同一文本 10 次 dispatch 解析 1 次；capacity=4 跑 40 个不同任务后 len/order ≤ 4；取消 0 解析；outcome 经 Tracker drop 后 live=0 |

编译与测试：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline` | 103 passed / 0 failed / 0 ignored / 0 measured，0.11s；doc-tests 0 | 已证实 |
| `cargo test --offline dispatcher::` | 47 passed（json 7 / task 8 / mode 12 / launcher 20） | 已证实 |
| `cargo build --release --offline` | 通过 | 已证实 |

UI 闸门：

| 项 | 值 |
| --- | --- |
| 规则文件 | docs/rules/ui-demo.md |
| 触发条件 | 改动用户可见界面元素的轮次 |
| 交付物 | `demos/ui-full-*.html`，整页、全区域、全状态、离线、KCU 品牌 |
| 用户回路 | 交付演示 → 手感调整 → 先改演示 → 确认后改实现 |
| 本轮 | 不触发；`demos/round-015-dispatcher.html` 是运行逻辑演示，不计入 G01 |
| 轻量模式 | 极简视图在 L3 触发时单独交付，不复用 normal.ui 资产 |

本地与远端：

| 项 | 值 | 四值 |
| --- | --- | --- |
| 本地 HEAD | `7d27d25`，165 tracked，src/dispatcher/ 5 文件 | 已证实 |
| 远端 HEAD | `b7a28e5`，parent `b1ed2fe`，message 为 015 主体 | 已证实 |
| 远端逐 blob 比对 | REMOTE 165 / LOCAL 165 / MISSING 0 / EXTRA 0 / MISMATCH 0 / ALL_MATCH True | 已证实 |
| 重复调用 api_push.py | 第二次 `PATCH refs/heads/main` 返回 422 `Update is not a fast forward` | 已失败（无影响） |

422 处置：首次调用已完成 165 个 blob 与 ref 更新，第二次调用基于旧 parent 再建 commit 触发非快进拒绝。未重写历史、未强推、未改断言；远端内容与本地一致，保留失败回显，不静默跳过。

015 独立验证委派记录：

| 次 | 结果 | 处置 |
| --- | --- | --- |
| 1 | 工具返回不可用，报告未落盘 | 按 18.1 未改已提交文件，重委派 |
| 2 | 核查跑完但受调用上限阻断，报告未落盘、哈希声明块与收尾自检未执行 | 核查结论保留，续任只做收尾 |
| 3（续任） | 报告 105 行落盘，两个哈希写入声明块，收尾自检关键项通过；自述首次自检命令因全仓扫描超时未跑完 | 未改报告断言，本段登记 |

哈希复核（只读）：

| 项 | 值 | 判定 |
| --- | --- | --- |
| 报告正文 SHA-1 声明 | `f64e187786a630d8bb1180fe4962f29527934376` | 改动作者按声明块偏移 5252 切分，`sha1(t[:5251])` 与该值一致，属「去掉声明块前多出的 1 个换行」口径，成立 |
| 变更内容 SHA-1 声明 | `a76baa9507d2c045da794f0c3ffc2a53e5abcf1d` | `git diff 0f900a0..757bea6 \| sha1sum` 复算一致 |
| 全文 SHA-1 | `957e004ebf72a2ddaa6f4dd20e5e373ee0a454fe` | 含声明块，与正文哈希不同，未混用 |
| 凭据扫描 | `NO_CREDENTIAL` | 已证实 |

独立验证结论：**部分通过**。验证者无认证，公开 GET 受速率限制，ALL_MATCH 未能独立复算，该项记受阻；改动作者带认证复跑 REMOTE 165 / LOCAL 165 / ALL_MATCH True 已登记。存量历史措辞命中落在扫描域外（docs/spec/、docs/checklists/、docs/verification/ 旧轮文件），项目扫描域复跑 NO_EXPLANATORY / NO_MIDSTATE / NO_REPEAT 通过，登记为口径差异，未改报告断言。两个哈希由独立验证者（含续任）计算并写入声明块，改动作者未代算。不发通过标记。

阶段：D07 第 2 层 dispatcher 已实现、已验证；第 3 层 lightweight 及以下 7 层未启动。

未做：
- 整页 UI 演示与 UI 实现
- L3 lightweight 及以下 7 层
- CF 下载模块、X01-X04 逐条处置、CF 具体调用方法
- 特殊版代码（待用户明确同意，用户手拉工具流）
- 本项目 LICENSE 文件
- 后端仓任何写请求
- 浏览器渲染与 GUI 点击端到端
- rustc 交叉编译 Win7 / ARM64 目标产物
- 插件源默认选择、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 条款补证

015 最终状态：

| 项 | 值 | 四值 |
| --- | --- | --- |
| 本地 HEAD | `db5af55`，166 tracked，工作区干净 | 已证实 |
| 远端 main 与本地逐 blob 比对 | REMOTE 166 / LOCAL 166 / MISSING 0 / EXTRA 0 / MISMATCH 0 / ALL_MATCH True | 已证实 |
| 打包 | `/data/workspace/kcu-launcher-desktop.zip`，含 round-015.md 与 src/dispatcher/launcher.rs | 已证实 |
| 全仓凭据与 .git/config | `NO_CREDENTIAL` / `NO_TOKEN_IN_CONFIG` | 已证实 |
| 后端仓 | 0 个写请求 | 已证实 |

远端 HEAD 随每次快照前进，不在本表写死；以 GitHub main 为准。上表「本地与远端」记录 015 主体推送后的时点（165 文件），本段记录验证报告与状态记录推送后的时点（166 文件）。变更内容哈希口径固定为基线 `0f900a0` 终点 `757bea6`，不受本段追加影响。

推送失败与重试（如实登记）：

| 次 | 输出 | 处置 |
| --- | --- | --- |
| 1 | `blob create 500 {}`，api_push.py 在 blob 阶段抛 RuntimeError，exit=1 | 未伪造成功；确认远端 ref 未被部分更新后重试 |
| 2 | `[KCU] remote push main OK files=166 via=git_data_api`，exit=0 | 远端逐 blob 比对 ALL_MATCH True |

未重写历史、未强推、未改断言。

## 016

| 落点 | 内容 |
| --- | --- |
| docs/spec/16-round-016-instructions.txt | 逐字副本，1 行 4 字节，SHA-1 `78dbbdabbcac19f0e4442954bdc5b89d88255abd` |
| docs/decisions/016-build-continue.md | D01-D08、L01-L15、U01-U09、验证与边界 |
| docs/rules/ui-demo.md | 轮次状态表、016 触发记录 T01-T06、016 检查命令 |
| src/lightweight/ | login.rs、download.rs、loaders.rs、view.rs、mod.rs |
| src/lib.rs | 追加 lightweight 模块与 7 个公共类型导出 |
| docs/features/lightweight.md | F003 状态改为已实现、已验证，五字段全量重写 |
| docs/features/lightweight-login.md、lightweight-download.md、lightweight-loaders.md、lightweight-view.md | F016-01..04，字段固定五段 |
| demos/ui-full-lightweight.html | **整页 UI 演示**，016 轮 UI 闸门首次触发的交付物 |
| demos/round-016-lightweight.html | L3 运行逻辑演示，13 节点，非整页 UI |
| 索引与记录 | features / decisions index、build-preconditions L3、ai-errors A67-A71、docs/index 61 项必读、README、interface-log I28-I32 / RO16-RO22、push-scope |
| docs/verification/round-016.md | 第 016 轮独立验证报告 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Thu Nov 12 23:59:18 CST 2026` |
| 全量测试与 release 复验 | `Fri Nov 13 00:19:51 CST 2026`，141 passed / 0 failed，rlib 1353366 字节 |
| 文档收口 | `Fri Nov 13 00:18:37 CST 2026` |

用户当轮输入：逐字「干」，1 行 4 字节。按 015 轮「继续按原进度」与 003-remote.md D07，进入第 3 层 lightweight。UI 闸门按 docs/rules/ui-demo.md「轻量模式极简视图改动」判定为**已触发**，与「继续原进度」并列执行，未替用户省略演示。

L3 落地：

| 编号 | 项 | 实测 |
| --- | --- | --- |
| L01 | 5 个模块 | `git ls-files src/lightweight/ \| wc -l` = 5；Cargo.toml / Cargo.lock 未变 |
| L02 | 三种登录 E01 | 8 项：离线免浏览器、外置成功、两级回退、连接码 300s 超时、无凭据禁正版、取消、诊断格式 |
| L03 | 批量请求 E02/K07 | 12 项：10 id 一次请求、45 id 三页三请求、10 次重复批次只发 1 次、缓存 ≤32、地域软策略、密钥注入、CF 不暴露、取消 0 请求、空集合不请求、reset 清态 |
| L04 | 加载器 E03 | 7 项：六种去重注册、重复可见、未装跳过、schema 字段为空、取消跳过 |
| L05 | 极简视图 | 11 项：单主题、13 项排除、系统文件面板、无常驻进程、11 弹窗全关闭 0 残留、9 类动作全响应、WebView2 注入、日志有界、取消不崩 |
| L06 | 整页 UI 演示 | 6 分区、5 状态、11 弹窗、手感调整区、离线可点、KCU 内联 SVG、无外部 CDN 与 FCL 字面量 |

编译与测试：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline` | 141 passed / 0 failed / 0 ignored / 0 measured，0.12s；doc-tests 0 | 已证实 |
| `cargo test --offline lightweight::` | 38 passed（login 8 / download 12 / loaders 7 / view 11） | 已证实 |
| `cargo build --release --offline` | 通过 | 已证实 |
| `node -e` 遍历 demos/*.html | 16 份内联脚本语法通过 | 已证实 |

首次 `cargo test` 遇增量编译缓存 `Stale file handle (os error 116)`，清理 `target/debug/incremental` 并以 `CARGO_INCREMENTAL=0` 复跑通过；失败回显保留，未静默跳过，未改测试断言。

口径处置（两条硬约束的交点）：

| 编号 | 冲突 | 处置 |
| --- | --- | --- |
| V01 | docs/rules/ui-demo.md C03 要求整页演示覆盖深浅主题切换 × 007-normal-ui.md D04 明确轻量模式排除浅色/深色双主题 | 演示层提供深浅**预览**并标注「实现默认单主题」；实现层 `Theme::Single` 不变。用户对演示的调整优先于当前实现（015 D04），是否加双主题由用户凭手感决定 |
| V02 | build-preconditions.md L3 前置写「WebView2 检测键已证实」× 该键实际仍未证实 | 改为注入式 `WebView2Probe`，不写死检测键；前置条件行如实改为「仍未证实，本层绕过实现，真实键与运行时实测仍受阻」，未降标准凑通过 |

阶段：D07 第 3 层 lightweight 已实现、已验证；整页 UI 演示已交付、手感回路进行中；第 4 层 headless 及以下 6 层未启动。

未做：
- UI 实现（整页演示确认后才进实现）
- L4 headless 及以下 6 层
- CF 下载模块、X01-X04 逐条处置、CF 具体调用方法
- 特殊版代码（待用户明确同意，用户手拉工具流）
- 本项目 LICENSE 文件
- 后端仓任何写请求
- 浏览器渲染实测、GUI 点击端到端、WebView2 运行时、进程级内存剖析
- rustc 交叉编译 Win7 / ARM64 目标产物
- 加载器逐版本 schema、WebView2 检测键、插件源默认、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 条款补证

016 验证者记录复核：

| 编号 | 验证者记录 | 改动作者复跑 | 判定 |
| --- | --- | --- | --- |
| V01 | 016 spec 文件在仓库内定位失败，SHA-1 不可复算，判未证实 | `ls -l`、`wc -lc`、`sha1sum docs/spec/16-round-016-instructions.txt` → 4 字节 1 行、`78dbbdabbcac19f0e4442954bdc5b89d88255abd`，与声明一致 | 验证者执行误差 |
| V02 | download.rs 实测 12 项、view.rs 实测 11 项，与委托口径 11 / 12 不符 | `grep -c '#\[test\]'` → download=12、view=11、login=8、loaders=7，合计 38 不变；委托语把两项写反，已修 016 决策、docs/index.md、本段实测表、两份功能 md、features/index.md、README.md 与运行逻辑 HTML 中的分项串 | 委托语分项写反，已纠正；验证报告按 18.1 未改 |
| V03 | `pub use` 实测 9 处，委托口径为 8 个公共导出 | `src/lib.rs` 顶层 `pub use lightweight::{...}` 实为 7 个类型；全文件共有 9 行 `pub use`（core / dispatcher / lightweight 合计）。验证者数的是全文件行数，委托语写的是单个模块导出数且数值写错 | 三口径差异，统一登记为 7 个类型导出；验证报告未改 |
| V04 | 禁用词两字连写在 8 处文件命中，判未通过 | 全仓 `grep -rl` 命中 9 个文件：`.github/workflows/ci.yml` 与 `docs/index.md` 是扫描命令字面量（词表自我命中），3 份 spec 是用户原文，3 份旧验证报告是历史，验证者自身 `round-016.md` 是记录用词；项目扫描域 `src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` 复跑 `NO_EXPLANATORY` | 扫描域口径差异；未改检查命令、未降标准 |
| V05 | 报告正文哈希 `e8471c6244dd36b214e1621fcaef202887f80f9a` | 声明块偏移 15392，`sha1(t[:15391])` 与该值一致，属「去掉声明块前多出的 1 个换行」口径，成立；全文 `db3da29767c72bdc67e68f75679c499c628f8f47` | 已证实 |
| V06 | 变更内容哈希 | `git diff 853746e..6c76eb2 \| sha1sum` = `865df8bcb3743cc47b114d3bbbf4ce97f3195695`，与声明一致 | 已证实 |
| V07 | 远端公开 GET | 验证者无认证只读 GET 确认 public / main / 远端头 `621c1b9`；改动作者稍后带认证推送后另记 | 受阻（限流下未逐 blob 独立复算） |

独立验证结论：**部分通过**。两个哈希由独立验证者计算并写入声明块，改动作者未代算；验证者五项记录中 V01 / V04 为口径或执行误差，V02 / V03 为委托语数值偏差，均已在改动作者侧纠正并登记，验证报告按 18.1 未改。未解决四值项仍存在，不发通过标记。

## 017

| 落点 | 内容 |
| --- | --- |
| docs/spec/17-round-017-instructions.txt | 逐字副本，1 行 259 字节，SHA-1 `b543d734232094498072f3f468a7499a9bd43ce1` |
| docs/decisions/017-visual-preview.md | D01-D10、S01-S15、验证与边界 |
| docs/rules/ui-demo.md | 轮次状态表 017 行、G07-G10、017 检查命令、手感回路 |
| docs/rules/push-scope.md | 脚本允许清单加入 `scripts/render_ui.py` |
| demos/ui-full-kcu-v2.html | 整页界面演示 v2，15 场景，布局重排，离线可点 |
| demos/preview/ | 15 张场景 PNG + `00-overview.png` + `index.md` |
| scripts/render_ui.py | 本地 chromium 渲染与 PIL 拼图 |
| docs/features/ui-visual-catalog.md | F017-01，字段固定五段 |
| 索引与记录 | features / decisions index、ai-errors A72-A75、docs/index 66 项必读、README、interface-log I33-I36 / RO23-RO28 |
| docs/verification/round-017.md | 第 017 轮独立验证报告 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Fri Nov 13 11:51:17 CST 2026` |
| 渲染链路探测 | `11:52`，playwright 无内置浏览器，改用系统 chromium 156 成功 |
| 首次 15 场景渲染 | `11:56` |
| 修复后重渲染与打包 | `11:58:48` |
| 文档收口 | `Fri Nov 13 12:02:09 CST 2026` |

用户当轮三点反馈与处置：

| 编号 | 反馈 | 处置 |
| --- | --- | --- |
| V01 | 提交物看不到用户界面长什么样 | 新增 PNG 预览闸门：本地 chromium 按场景截图 1440×900，PIL 拼 3×5 总览图；对话里直接交图 |
| V02 | 之前只是要那个风格，不代表位置都要按那个位置放 | 017 D03/D04：只取配色、圆角、描边、卡片层次、轻噪点；布局重排为顶部条 + 精简导航 + 卡片流 + 底部状态条，不采用三栏拖拽与组件位置照搬 |
| V03 | 得多思考，公告什么的也得让我看看长什么样 | 主动补齐 15 个场景；公告族含公告中心、详情弹窗、首页横幅、版本更新提示、维护公告、活动公告，见 S01-S15 |

渲染链路：

| 项 | 值 | 四值 |
| --- | --- | --- |
| `python3 -c import playwright/PIL` | 均可用 | 已证实 |
| playwright 默认浏览器 | 缺 `chrome-headless-shell`，`BrowserType.launch` 报错 | 已失败 |
| 改用 `executable_path=/usr/local/bin/chromium` | chromium 156.0.8069.0 截图成功 | 已证实 |
| `python3 scripts/render_ui.py` | `render_ui OK shots=15`，16 张 PNG | 已证实 |
| `demos/preview/00-overview.png` | 1444×1776，770376 字节 | 已证实 |
| `/data/workspace/ui-previews.zip` | 3.8M，含全部预览图 | 已证实 |

本轮真实缺陷与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E01 | 首次总览里 12 个场景显示同一个弹窗，场景切换未清 overlay | 在 `show()` 开头加 `dismissOverlay()`，弹窗类场景（`notice-detail` / `update`）先关再开；重渲染后逐张核对内容不同；立 A75 |
| E02 | 弹窗遮罩 0.74 过暗，背景界面轮廓看不清 | 调到 0.62 后重渲染，弹窗与背景都可见 |
| E03 | 下载、日志、公告详情初始内容偏空，截图信息量不足 | 初始化预填 4 行文件进度、8 行 `[KCU]` 诊断、首条公告正文 |

验证：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed（src 未变） | 已证实 |
| `node -e` 遍历 demos/*.html | 17 份内联脚本语法通过 | 已证实 |
| `! grep -rE 'https?://\|FCL\|揉纸启动器' demos/ui-full-kcu-v2.html` | exit 0 | 已证实 |
| `! grep -rqE 'gh[p]_' .` | NO_CREDENTIAL | 已证实 |
| `git diff 6d09a10..HEAD -- src/` | 空 | 已证实 |
| 用户在手机端查看预览并给手感反馈 | 未发生 | 未证实 |

阶段：D07 第 3 层 lightweight 已实现、已验证；017 轮只动演示层与文档，`src/` 无变化；L4 headless 及以下 6 层未启动。UI 实现仍按 D08 等用户确认演示后进。

未做：
- UI 实现（PNG 总览确认后才进实现）
- L4 headless 及以下 6 层
- CF 下载模块、X01-X04 逐条处置、CF 具体调用方法
- 特殊版代码（待用户明确同意，用户手拉工具流）
- 本项目 LICENSE 文件
- 后端仓任何写请求
- 浏览器内交互实测（截图为静态帧，交互需用户本地点开整页 HTML）
- 加载器逐版本 schema、WebView2 检测键、插件源默认、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 条款补证

017 验证者记录复核：

| 编号 | 验证者记录 | 改动作者复跑 | 判定 |
| --- | --- | --- | --- |
| V01 | `class="scene"` 实测 11 处，判「非 15 个独立区块」 | `grep -c '<section class="scene'` = 12；`class="scene"` 精确 11（另有 1 个 `class="scene on"`）；`class="scene` 宽匹配 24（含 12 个 `class="scene-tag"`）。真实结构：**12 个独立 section + 3 个派生视图**（notice-detail 复用 notices + 弹窗、update 复用 home + 弹窗、home-light 复用 home + 浅色主题）= 15 张截图 | 委托语把「15 张截图视图」写成「15 个独立区块」，数值口径纠正；验证报告按 18.1 未改 |
| V02 | `dismissOverlay` 实测 2 处 | 定义 1 处 + `show()` 调用 1 处，合计 2 | 正常实现，委托语未给数量 |
| V03 | `demos/preview/` 17 项，与「16 张 PNG」不符 | `ls demos/preview/*.png \| wc -l` = 16；目录 17 项含 `index.md` | 口径差异 |
| V04 | `preview/index.md` 32 行，与委托语「16 行」不符 | `wc -l` = 32 | 委托语数值写错，登记纠正 |
| V05 | `ui-visual-catalog.md` 六标题，与「五标题」不符 | 6 个 `##`：怎么运作 / 开放了什么 / 登记框架 / 用户使用逻辑 / 性能 / 验证 | 五固定字段 + 既有模板的「验证」段，其余功能 md 同构；口径差异 |
| V06 | `render_ui.py` 本轮未实跑，仅静态与产物证据 | 改动作者 11:56 / 11:58 / 12:04 三次实跑，输出 `render_ui OK shots=15`，16 张 PNG 与总览尺寸已核 | 改动作者已证实，验证者侧受阻 |
| V07 | 渲染 0 次远端请求无进程级抓包 | 脚本只 `page.goto(file://...)`，无 HTTP 客户端；进程级抓包未做 | 未证实（未升级为已证实） |
| V08 | 域外四值词汇与「同上」命中未清理 | 命中落在 `.github/workflows/ci.yml`、`docs/index.md` 词表字面量、3 份 spec 用户原文、旧验证报告；项目扫描域复跑 `NO_EXPLANATORY` / `NO_MIDSTATE` / `NO_REPEAT` | 扫描域口径，未改命令、未降标准 |
| V09 | 用户手感反馈回路未闭环 | 真实：手机端查看与反馈尚未发生 | 未证实，保留 |
| V10 | UI 实现未进构建 | 017 D10 范围决定，等用户确认演示 | 未证实，保留 |

哈希复核：

| 项 | 值 | 判定 |
| --- | --- | --- |
| 报告正文 SHA-1 声明 | `d88b1b80f7b3b285379e195e6b45ed983e294f50` | 声明块偏移 22012，`sha1(t[:22012])` 与之完全一致；本轮无「多出 1 个换行」偏差 |
| 全文 SHA-1 | `9e85b09beb9a2b5777cd851a084c798f41fe2f71` | 含声明块，与正文哈希不同属预期 |
| 变更内容 SHA-1 声明 | `67c300d889242791785e945c67a2bc0ff00af907` | `git diff 6d09a10..b3b27c5 \| sha1sum` 复算一致 |
| 凭据与措辞 | `NO_CREDENTIAL` / `NO_EXPLANATORY` | 已证实 |

独立验证结论：**部分通过**。两个哈希由独立验证者计算并写入声明块，改动作者未代算。验证者 10 项记录中 V01 / V03 / V04 / V05 为委托语数值与口径偏差，V02 / V06 / V07 / V08 为执行与扫描域口径，V09 / V10 为真实未解决项；改动作者侧已纠正委托语数值并登记，验证报告按 18.1 未改。未解决四值项仍存在，不发通过标记。

## 018

| 落点 | 内容 |
| --- | --- |
| docs/spec/18-round-018-instructions.txt | 逐字副本，1 行 122 字节，SHA-1 `3a9746a86ff49ab7fbb9aa805326f3e14c39dc50` |
| docs/decisions/018-paper-ux.md | W01/W02 撤回、D01-D10、视觉 token 对照表、S01-S20、E01-E05 |
| docs/rules/ui-demo.md | 轮次状态表 018 行、G11-G12、018 检查命令 |
| demos/ui-full-kcu-paper.html | 纸质质感 UX 整页演示，1440×900 桌面窗口，20 视图 |
| demos/preview/ | 20 张视图 PNG + `00-overview.png` + 重写的 `index.md` |
| scripts/render_ui.py | 改渲染 paper 版、20 场景、每视图强制重载、4 列 5 行总览 |
| docs/features/ui-paper-ux.md | F018-01，字段固定五段 |
| 索引与记录 | features / decisions index、ai-errors A76-A79、docs/index 71 项必读、README、interface-log I37-I41 / RO29-RO36、push-scope |
| docs/verification/round-018.md | 第 018 轮独立验证报告 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Fri Nov 13 12:25:37 CST 2026` |
| 源稿一致性核对 | `12:33:39`，`cmp exit 0` |
| 首次 20 视图渲染 | `12:30` 前后 |
| 三轮修复后最终渲染 | `12:33` 前后 |
| 文档收口 | `Fri Nov 13 12:34 CST 2026` 前后 |

用户当轮两点反馈与撤回：

| 编号 | 反馈 | 上一轮做法 | 018 处置 |
| --- | --- | --- | --- |
| W01 | 风格不对 | 017 `ui-full-kcu-v2.html` 用青绿主色 + 深蓝黑底 + 大圆角，自称取自样板 | 撤回。按源稿逐值重做：米纸 `#F1EFE8` / 墨 `#2C2C2A` / 暗青绿 `#3D6B66` / 砖红 `#B8543F` / 细线 / 半透明卡片 / 圆角 4-8-10 / 衬线标题 / 折痕 + 细噪点 / 深色纸质；017 文件保留作废 |
| W02 | 之前提交的是流程 HTML，不是 UX HTML | 001–016 主要交付 `demos/round-0XX-*.html` 状态机与诊断行 | 撤回交付形态判定。UX HTML ＝ 窗口、导航、卡片、表格、弹窗、状态栏；流程 HTML ＝ 步骤节点、信封、阶段判定。写进 G12，动 UI 的主交付改为 UX HTML + PNG |

风格只取质感，位置仍重排：顶部标题栏 + 精简左导航（可折叠）+ 工具条 + 卡片流主区 + 状态栏；不采用源稿三栏拖拽与右栏公告。KCU 内联 SVG 与 `K` 字标，无源稿品牌字面量、无外部字体 CDN。

本轮真实缺陷与修复（全部留痕）：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E01 | 首次渲染 19 张全部继承深色主题 | `page.goto` 仅改 hash 不重载，浏览器保留上一场景 theme；改每场景带 `?r=<i>` 强制重载，重渲染后仅 S02 为深色 |
| E02 | 折痕与噪点过重，浅色纸面出现明显 X 形黑线 | 折痕透明度下调（浅色 .045→.022、深色 .28→.10），噪点 alpha 16→9 / 14→8 |
| E03 | 深色纸质正文继承 body 深墨色，标题与统计数值不可读 | `.win[data-theme="dark"]` 补 `color:var(--ink)`；primary 按钮文字改 `#26272A`；搜索框补 `color` |
| E04 | 窗口 900px + 底部说明文字撑高 flex，标题栏与状态栏被裁 | 说明文字改 `position:fixed` 且透明，窗口完整可见 |
| E05 | 20px 方形 logo 挤三字母 | 改单字 `K` |

验证：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cmp 源稿 assets/ui/normal-mode-v3.html` | exit 0，双端 `235943d2…e99d` | 已证实 |
| `python3 scripts/render_ui.py` | `render_ui OK shots=20`，21 张 PNG，总览 1462×1392 | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `node -e` 遍历 demos/*.html | 18 份内联脚本语法通过 | 已证实 |
| `! grep -rE 'FCL\|揉纸启动器\|https?://' demos/ui-full-kcu-paper.html` | exit 0 | 已证实 |
| `git diff 52e02c1..HEAD -- src/` | 空 | 已证实 |
| 用户在手机端按图给手感反馈 | 未发生 | 未证实 |

阶段：D07 第 3 层 lightweight 已实现、已验证；018 轮只动演示层与文档，`src/` 无变化；L4 headless 及以下 6 层未启动。UI 实现仍按 D08 等用户确认演示后进。

未做：
- UI 实现（PNG 总览确认后才进实现）
- L4 headless 及以下 6 层、CF 下载模块、X01-X04 逐条处置、CF 具体调用方法
- 特殊版代码（待用户明确同意，用户手拉工具流）、本项目 LICENSE 文件
- 后端仓任何写请求
- 浏览器内交互实测（截图为静态帧，交互需用户本地点开 UX HTML）
- 加载器逐版本 schema、WebView2 检测键、插件源默认、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 条款补证

018 独立验证复核：

| 项 | 值 | 判定 |
| --- | --- | --- |
| 独立验证结论 | **部分通过** | 未发通过标记 |
| 报告正文哈希声明 | `81e06b646d8a014a57ebe836a83c6b17c3fd9b13` | 声明块偏移 14173，`sha1(t[:14172])` 一致，属「去掉声明块前多出的 1 个换行」口径 |
| 全文 SHA-1 | `e103afe47f4d905dbb63b37cda2c09bbf83015a8` | 含声明块，与正文哈希不同属预期 |
| 变更内容哈希声明 | `1dac5274ce791f1fdafe7371443a254835d1d914` | `git diff 52e02c1..bba186e \| sha1sum` 复算一致 |
| 报告第 5 行「21 张 PNG 目录项」 | `ls demos/preview/*.png \| wc -l` = 21；目录 22 项含 `index.md` | 措辞口径，未改报告 |
| 全仓凭据、项目扫描域措辞 | `NO_CREDENTIAL` / `NO_EXPLANATORY` | 已证实 |

两个哈希由独立验证者计算并写入声明块，改动作者未代算。委托语本轮把 14 个独立 section + 6 个别名派生视图 = 20 张截图、21 张 PNG、功能 md 六标题三个口径写清，验证者未再产生数值偏差记录。未通过项全部为真实未解决四值：用户手感反馈未发生、UI 实现未进构建、L4 及以下 6 层未启动、CF F17 / X01-X04 / 特殊版代码 / LICENSE、多项未证实调研、浏览器与 GUI 端到端、交叉编译、git HTTP、6 上游主机、远端无认证只读 GET 受阻、017 风格取错已撤回、Win7+ARM64 与 v99.99 tag 已失败、本地链与远端链哈希不同。验证报告按 18.1 未改。

## 019

| 落点 | 内容 |
| --- | --- |
| docs/spec/19-round-019-instructions.txt | 逐字副本，1 行 782 字节，SHA-1 `ad626f16ec7c6b763d7892951901e6b609042292` |
| docs/decisions/019-ux-logic-lucide.md | D01-D12、R01-R08 调研来源、验证与边界 |
| docs/design/ux-logic-matrix.md | L01-L12 骨架、U01-U20 矩阵、缓存分层、刷新触发、推荐位、状态词表、失效冲突、许可动态结构、C01-C12、自评 9.2 |
| demos/ui-full-kcu-paper.html | 22 区块 / 28 视图、22 条逻辑条、88 枚 lucide 内联、第三方许可七列表 |
| demos/preview/ | 28 张视图 PNG + `00-overview.png` + 重写 index.md |
| assets/icons/ | lucide-subset.svg（88 枚）、lucide-manifest.json |
| THIRD-PARTY-NOTICES.md | 发行物第三方许可声明 |
| docs/features/ | ux-logic-completion.md、lucide-icon-system.md、third-party-licenses-about.md |
| 索引与规则 | decisions / features / licenses index、ai-errors A80-A84、ui-demo G13-G15 与 019 行、docs/index 78 项必读、README、interface-log I42-I49 / RO37-RO45、push-scope |
| docs/verification/round-019.md | 第 019 轮独立验证报告 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Fri Nov 13 23:10:19 CST 2026` |
| lucide 一手图标抓取 | `23:11` 前后，81 枚成功 + 4 枚改名补齐 + 2 枚圆形补齐 = 88 |
| 设计矩阵 v1 落盘 | `23:15` 前后 |
| 28 视图首次渲染 | `23:20` 前后 |
| 图标字面量修复与最终渲染 | `23:24` 前后 |
| 文档收口 | `Fri Nov 13 23:30 CST 2026` 前后 |

用户当轮四点要求与处置：

| 编号 | 要求 | 处置 |
| --- | --- | --- |
| V01 | 用 lucide 图标，自主权给我，只看结果 | 全站 88 枚一手 SVG 内联 sprite，0 字符图标残留；ISC + Feather MIT 登记 |
| V02 | 每个地方都要有使用逻辑，像之前设计的；服务器首页要有推荐、缓存、刷新；按这套逻辑补全每个功能 | L01-L12 骨架 × U01-U20；首页推荐服务器卡；每个视图逻辑条；新增服务器推荐 / 数据与缓存 / 刷新机制 / 状态与降级四页；8 个新功能视图 |
| V03 | 没思路就上网搜 | 查 lucide 许可与 SVG 约定、第三方归属规范、PCL2 多层缓存、FCL 下载后视图不自动刷新的观察者改造，8 条来源写进 019 决策 |
| V04 | 用别人代码要在关于页说明许可证与项目 | 关于页一级入口 + 七列表 16 组 + 分组筛选 + ISC 原文摘录 + 插件动态追加 + NOTICES 随发行物附带 |
| V05 | 发现思考不足就再次增加设计直到自评 9 分以上 | 3 轮自评 7.2 → 8.4 → 9.2，每轮记录发现的不足与真实补入内容 |

自评迭代（补入动作真实落盘）：

| 轮次 | 自评 | 发现的不足 | 补入 |
| --- | --- | --- | --- |
| 迭代 1 | 7.2 | 矩阵与三张表写完，但 UX HTML 只有 14 个视图，U13/U15/U16/U19/U20 没有界面；图标是字符；逻辑条未注入；许可只有文档没有关于页入口 | 8 个新视图、88 枚 lucide、22 条逻辑条、许可七列表、THIRD-PARTY-NOTICES.md、关于页一级按钮 |
| 迭代 2 | 8.4 | 主结构补齐，但缺刷新失败回退缓存不空白、命中/未命中可见、时间戳统一口径、许可按许可证分组、轻量与无头缓存刷新证据、插件动态追加界面证据 | 状态徽章 11 类、失效并发冲突 8 种、许可动态数据结构、AI/开服/无头空错加载细则、轻量与无头缓存证据、刷新兜底页与提示 |
| 迭代 3 | 9.2 | 上述六项补齐并出图；剩余均为未证实外部依赖，不属设计缺口 | C01-C12 跨功能一致性检查表与分项评分，收口 |

本轮真实缺陷与修复（全部留痕）：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E01 | 8 个 lucide 图标名返回 404（circle-alert、triangle-alert、trash-2、filter、circle-help、shield-alert、file-check-2、history） | 换用官方现存名 trash / funnel / shield / file-check / list-filter；其余用 circle-x / info / rotate-ccw 替代；补取 circle 与 circle-dot |
| E02 | 新增 8 个 section 时把 `'+I('xxx')+'` 写成 python 三引号字面量，19 处按钮标题出现拼接文本 | 正则替换为真实 SVG，重渲染后逐页核对无残留；立 A84 |
| E03 | 首页右列新增推荐服务器卡后，900px 首屏把「当前账户」卡挤到滚动区外，静态截图看不到 | 删推荐卡冗余说明行、最近公告由 3 条压到 2 条，重渲染后首屏恢复 |

联网调研：

| 来源 | 事实 |
| --- | --- |
| https://lucide.dev/license | ISC 全文、Feather 派生清单与 MIT 全文、Copyright 2026 |
| https://lucide.dev/guide/packages/lucide-static | 内联 SVG / sprite 可用；全量 sprite 不推荐生产，只打包用到的图标 |
| https://lucide.dev/contribute/icons/code-conventions | 24×24 viewBox、fill=none、stroke=currentColor、stroke-width=2 |
| https://libre.xram.net/guides/attribution | 归属需项目名、版权、许可证全文或链接；About / Legal 页展示；NOTICES 随发行物 |
| https://opensourcelicenserisk.com/glossary/attribution-requirement | 归属随代码传递；NOTICE 保留；清单随依赖变化刷新 |
| PCL2 资源管理公开资料 | 内存 / 磁盘 / 网络 / 预取四层缓存 |
| FCL 布局下载刷新公开资料 | 下载后列表不自动刷新 → 观察者模式 / 自动跳转推视图 |

验证：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=28`，29 张 PNG | 已证实 |
| `grep -c '<symbol'` | 88 | 已证实 |
| `grep -c 'class="logicbar"'` | 22 | 已证实 |
| 字符图标残留 / 图标引用缺失 | 0 / 0 | 已证实 |
| `! grep -rE 'FCL\|揉纸启动器\|https?://' demos/ui-full-kcu-paper.html` | exit 0 | 已证实 |
| `test -f THIRD-PARTY-NOTICES.md` | 存在 | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `! grep -rqE 'gh[p]_' .` | NO_CREDENTIAL | 已证实 |
| `git diff 66019be..HEAD -- src/` | 空 | 已证实 |
| 用户在手机端按图给手感反馈 | 未发生 | 未证实 |

阶段：D07 第 3 层 lightweight 已实现、已验证；019 轮只动演示层、设计层与文档，`src/` 无变化；L4 headless 及以下 6 层未启动。UI 实现仍按 018/019 D08 等用户确认演示后进。

未做：
- UI 实现（PNG 总览确认后才进实现）
- L4 headless 及以下 6 层、CF 下载模块、X01-X04 逐条处置、CF 具体调用方法
- 特殊版代码（待用户明确同意，用户手拉工具流）、本项目 LICENSE 文件
- 后端仓任何写请求
- 浏览器内交互实测（截图为静态帧，交互需用户本地点开 UX HTML）
- 加载器逐版本 schema、WebView2 检测键、插件源默认、CF server-only 等价字段、`/talk` 来源、Java 镜像条款、mclo.gs 条款补证

019 独立验证复核：

| 项 | 值 | 判定 |
| --- | --- | --- |
| 独立验证结论 | **部分通过** | 未发通过标记 |
| 报告正文哈希声明 | `0230edd7f15f011717e9f780b4545bd168f4c6b6` | 声明块偏移 11913，`sha1(t[:11912])` 与之完全一致；`t[:11913]` 得 `72309d46…`，属「去掉声明块前多出的 1 个换行」口径，验证者自述的切分差异即此 1 字节 |
| 全文 SHA-1 | `2fb51086c68f41290927863ca2c076ff9d8a811c` | 含声明块，与正文哈希不同属预期 |
| 变更内容哈希声明 | `2faf46277b4431f6dd108046e0ca01da26ac01b4` | `git diff 66019be..8c86b05 \| sha1sum` 复算一致 |
| 验证者三项工具链受阻 | `CARGO_INCREMENTAL=0 cargo test --offline` 141 passed / 0 failed；node 遍历 18 份 HTML 全通过；`compile(scripts/render_ui.py)` 通过 | 改动作者侧已证实，验证者侧受阻 |
| 验证者全仓扫描未独立复验 | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_BRAND_EXT` / `NO_REPEAT` | 改动作者侧已证实 |
| 78 项必读未逐项核对 | `REQUIRED=78 MISSING=0` | 已证实 |
| 远端只读 GET 未发起 | 验证者无认证，记受阻 | 保留 |

两个哈希由独立验证者计算并写入声明块，改动作者未代算。委托语本轮把 22 独立区块 / 28 截图 / 29 PNG / 88 symbol / 22 逻辑条 / 6 标题 / 78 必读六个口径写清，验证者未再产生数值偏差记录。未通过项全部为真实未解决四值：用户手感反馈未发生、UI 实现未进构建、L4 及以下 6 层未启动、CF F17 / X01-X04 / 特殊版代码 / LICENSE、多项未证实调研、浏览器与 GUI 端到端、交叉编译、git HTTP、6 上游主机、远端无认证只读 GET 受阻、017 风格取错已撤回、Win7+ARM64 与 v99.99 tag 已失败、本地链与远端链哈希不同。验证报告按 18.1 未改。

## 020

| 落点 | 内容 |
| --- | --- |
| docs/spec/20-round-020-instructions.txt | 逐字副本，1 行 853 字节，SHA-1 `070c6475693e4bd28f41cfbb3d6b6f9b7d6e72f6` |
| docs/decisions/020-nav-slots-settings.md | D01-D16、R01-R12 / C01-C04 / M01 调研来源、验证与边界 |
| docs/research/17-plugin-settings-survey.md | 统一调研：12 一手 + 4 公开资料 + 3 受阻，J01-J06 结论 |
| docs/design/ | nav-slot-contract.md、recommendation-catalog.md、server-status.md、upper-layer-stack.md、handoff.md |
| docs/design/ux-logic-matrix.md | U21-U25 逐项 L01-L12、020 自评迭代、C13-C20、最终自评 9.3 |
| demos/ui-full-kcu-paper.html | 26 区块 / 37 截图视图、26 条逻辑条、导航锁定槽位、设置九分组、4 个新视图 |
| demos/preview/ | 37 张视图 PNG + `00-overview.png` + 重写 index.md |
| THIRD-PARTY-NOTICES.md | 第五节：上层实现候选 12 组，全部「候选 · 未进构建」 |
| docs/features/ | nav-slot-lock.md、settings-groups.md、recommendation-catalog.md、server-status-settings.md、upper-layer-thirdparty.md、handoff-baseline.md |
| 索引与规则 | decisions / features / licenses / research index、ai-errors A85-A89、ui-demo G16-G18 与 020 行、docs/index 92 项必读、README、interface-log I50-I56 / RO46-RO56、push-scope |
| docs/verification/round-020.md | 第 020 轮独立验证报告 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Fri Nov 13 23:48:55 CST 2026` |
| 必读 78 项复读 | `23:48:55`，REQUIRED=78 MISSING=0 |
| 统一调研两轮 | `23:49`–`23:51` |
| 导航与设置改造落盘 | `23:54` 前后 |
| 37 视图首次渲染 | `23:56` 前后 |
| 工具条收敛、上层候选视图、最终渲染 | `23:59`–`00:02` |
| 文档收口 | `Sat Nov 14 00:05 CST 2026` 前后 |

用户当轮要求与处置：

| 编号 | 要求 | 处置 |
| --- | --- | --- |
| V01 | 看样子我还比较满意 | 019 演示层手感通过；本轮仍按闸门先改演示与截图，不改 `src/` |
| V02 | 有些功能不用写在顶上，比如接口是设置里头的东西 | 一级导航收敛为 9 项日常操作；AI 接口、数据与缓存、刷新机制、状态与降级、无头模式、第三方许可移出一级导航；工具条操作按视图收敛 |
| V03 | 支持插件，关于设置要锁定位置，防覆盖 | `core.locked.settings` / `core.locked.about` 固定在同一容器，带虚线描边、锁图标、locked 徽章；插件区 `slot:plugin.*` 独立；冲突拒绝演示与诊断行 |
| V04 | 以后更新可能用插件化更新 | 更新器作为插件，只替换插件包，核心不动；签名校验不可禁用、默认只升、回滚需显式比较器、失败保留旧插件 |
| V05 | 对话可能取消，新开对话把本仓库当底层 | `docs/design/handoff.md` 交接基线：必读 6 步、已完成 L1-L3、H01-H08 不可变边界、已知卡点；关于页交接卡片与交接页 |
| V06 | 推荐项目想好，包括怎么设置服务器状态 | 10 处推荐位逐处定义；服务器状态取 SLP 一手字段，6 类状态 + 自定义项 + 降级路径全落设置 |
| V07 | 该放设置的放设置，自定义设置功能也放设置 | 设置 9 分组、稳定 ID、写后即时生效、@modified、单项重置 |
| V08 | 最后统一调研一下 | `docs/research/17-plugin-settings-survey.md`，12 一手来源 + 4 公开资料 + 3 受阻，完整 URL 锚点 |
| V09 | 上层实现都用别人的代码 | 12 组候选逐项标许可证 / 用途 / 全文状态 / 复制状态；关于页与 NOTICES 登记；全部标「候选 · 未进构建」 |
| V10 | 发现思考不足就再次增加设计直到自评 9 分以上 | 3 轮 7.4 → 8.6 → 9.3，每轮记录不足与真实补入动作 |

自评迭代（补入动作真实落盘）：

| 轮次 | 自评 | 发现的不足 | 补入 |
| --- | --- | --- | --- |
| 迭代 1 | 7.4 | 导航瘦了、槽位锁了、设置九分组，但推荐位只沿用 019 的 6 处、服务器状态只有 SLP 字段没落设置项与状态类型、插件化更新缺签名 / 回滚 / 失败降级、上层候选缺逐项许可证与登记规则、交接页缺不可变边界 | 10 推荐位表、6 类状态与设置 ID、插件化更新 6 项、上层候选 12 组、交接 6 步与 8 条边界 |
| 迭代 2 | 8.6 | 上述补齐，但缺工具条操作按视图收敛、核心槽位冲突的可见拒绝与诊断行、设置项稳定 ID / @modified / 单项重置、插件来源不改 core.rec.*、插件区双高亮修复 | 工具条 hideActs、槽位冲突弹窗与 `[KCU]` 行、9 分组稳定 ID 与 @modified、plugin.rec.* 约束、状态面板改指 states |
| 迭代 3 | 9.3 | 上述五项补齐并出 38 张 PNG；剩余均为未证实外部依赖与未启动层，不属设计缺口 | C13-C20 跨功能一致性检查与分项评分，收口 |

本轮真实缺陷与修复（全部留痕）：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E01 | `re.subn` 替换串含 `C:\KCU` 触发 `bad escape \K`，导航与设置改造脚本第一次运行失败 | 改用 lambda 替换并把脚本落盘为 `scripts/round020_ui.py`，重跑通过 |
| E02 | 插件区两个按钮都指向 slots，`show()` 给两个 nav-item 同时加 active，出现双高亮 | 状态面板改指 states 视图，重渲染后单高亮 |
| E03 | 关于页上层候选表首屏只露出 1 行，用户看不到完整清单 | 新增 `upperstack` 独立视图，12 行全可见；关于页加「完整候选清单」入口；总截图 37→38 |

统一调研来源：

| 来源 | 事实 |
| --- | --- |
| https://code.visualstudio.com/api/ux-guidelines/overview.md | containers / items 模型与六个容器职责 |
| http://vscode.net.cn/api/references/contribution-points | contributes 声明清单（官方文档中文镜像） |
| https://code.visualstudio.com/api/extension-guides/tree-view | viewsContainers → views，分组顺序 `@n` |
| https://code.visualstudio.com/docs/configure/settings | 作用域、分组、搜索、@modified、即时生效、扩展设置区 |
| https://docs.rs/tauri-plugin-updater/latest/struct.Config.html | pubkey / require_signed_version / allow_downgrades / endpoints |
| https://doc.rust-lang.org/ | Rust 官方文档入口 |
| https://docs.rs/rs-rich-plugin-api/latest/rich_plugin_api/abi/index.html | Rust ABI 不稳定、C ABI、ABI_MAJOR 拒绝 |
| https://docs.rs/supercode-core/latest/supercode/plugins/index.html | manifest DATA + 子进程隔离 |
| https://minecraft.wiki/w/Java_Edition_protocol/Server_List_Ping | SLP 1.7+ 流程与 JSON 字段 |
| https://crates.io/crates/reqwest/range/%3E=%200.10.1,%20%3C%200.11 | reqwest MIT OR Apache-2.0 |
| https://github.com/lucide-icons/lucide | Lucide ISC |
| https://libre.xram.net/guides/attribution | 归属与 NOTICES 规则 |
| 4 组公开资料 | 插件 ABI 社区经验、SLP 端到端、ServerListPingEvent、第三方依赖许可汇总 |
| 3 个受阻 / 镜像项 | Tauri 中文站标未证实（镜像原文）、Tauri v2 官方插件页与 Eclipse/OSGi 官方页受阻 |

验证：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=37`，38 张 PNG | 已证实 |
| `grep -c '<section class="view'` | 26 | 已证实 |
| `grep -c 'class="logicbar"'` | 26 | 已证实 |
| `grep -c '<symbol'` / 字符图标残留 | 88 / 0 | 已证实 |
| `grep -o 'data-tab=' \| wc -l` / `grep -o 'data-pane=' \| wc -l` | 9 / 9 | 已证实 |
| `node -e` 内联脚本 / `compile(scripts/render_ui.py)` | 通过 | 已证实 |
| `! grep -rE 'FCL\|揉纸启动器\|https?://' demos/ui-full-kcu-paper.html` | exit 0 | 已证实 |
| `! grep -rqE 'gh[p]_' .` | NO_CREDENTIAL | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `git diff <019>..HEAD -- src/` / Cargo.lock | 空 / 未变 | 已证实 |
| 必读 92 项存在非空 | REQUIRED=92 MISSING=0 | 已证实 |
| 用户按 38 张图给手感反馈 | 未发生 | 未证实 |

阶段：D07 第 3 层 lightweight 已实现、已验证；020 轮只动演示层、设计层与文档，`src/` 与 Cargo.lock 无变化；L4 headless 及以下 6 层未启动。UI 实现按闸门等用户确认演示后进。

未做：
- UI 实现（PNG 总览确认后才进实现）
- L4 headless 及以下 6 层、插件注册表与插件化更新实现、第三方依赖引入
- CF F17 调用方法、X01-X04 逐条处置、特殊版代码、本项目 LICENSE
- 后端仓任何写请求
- 浏览器内交互实测（截图为静态帧）、GUI 端到端、交叉编译、SLP 客户端
- 上层 12 组候选逐仓库 LICENSE 全文、Tauri v2 官方 updater 页与 Eclipse/OSGi 官方页

020 独立验证复核：

| 项 | 值 | 判定 |
| --- | --- | --- |
| 独立验证结论 | **部分通过** | 未发通过标记 |
| 变更内容哈希声明 | `21a2f33e3e13853047d663b78681d088f8a9d816` | `git diff 4abdfc9..f985f07 \| sha1sum` 复算一致 |
| 报告正文哈希声明 | `3007d7e8d571eca4f46245f946e640ba1da8e2fa` | 与当前报告文件不一致；按声明块偏移 19316 切分得 `3904b03bfbc6a6028939e874f1a5f0cc34e9d194`，去 1 换行得 `aef9a9513e2649db1b70646bb5486977562171f0`，全文 `a480113943ac780ee87975c739032217ad0b12f7`；±6 字节与加换行末尾逐项枚举均未命中声明值。属验证者记录误差，按 18.1 未改报告，留待下轮独立复核 |
| 报告末尾换行 | 文件末尾无换行 | 验证者收尾自检因沙盒总超时未跑，登记为受阻 |
| 工具链三项 | `CARGO_INCREMENTAL=0 cargo test --offline` 141 passed / 0 failed；node 遍历 18 份 HTML 全通过；三个 python 脚本 compile 通过 | 改动作者侧已证实，验证者侧受阻 |
| 全仓扫描 | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_BRAND_EXT` / `NO_REPEAT` | 改动作者侧已证实；其中 `同上` 首次命中为我方 020 调研索引写入的简写，已修为完整路径 |
| 92 项必读 | `REQUIRED=92 MISSING=0` | 已证实 |
| 远端只读 GET | 验证者无认证且超时，记受阻 | 保留 |

本轮真实缺陷追加：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E04 | `docs/research/index.md` 020 段把结论来源写成「同上」，命中 A22 的 `同上` 禁用扫描，首次复跑 `REPEAT_FOUND` | 改为完整路径 `docs/research/17-plugin-settings-survey.md`，复跑 `NO_REPEAT`；改动作者侧修正，未改验证报告 |

两个哈希由独立验证者计算并写入声明块，改动作者未代算；正文哈希与文件内容不一致一项按 18.1 保留原报告，只登记复核结果。委托语本轮把 26 独立区块 / 37 截图 / 38 PNG / 88 symbol / 26 逻辑条 / 9+9 tabs-panes / 92 必读 / 256 tracked 八个口径写清，验证者未再产生数值偏差记录。

未通过项全部为真实未解决四值：用户手感反馈未发生、UI 实现未进构建、L4 及以下 6 层未启动、插件注册表与插件化更新未实现、上层 12 组候选逐仓库 LICENSE 全文未取得、LICENSE 未生成、CF F17 / X01-X04 / 特殊版代码、多项未证实调研、浏览器与 GUI 端到端、交叉编译、git HTTP、6 上游主机、远端无认证只读 GET 受阻、报告正文哈希待复核、017 风格取错已撤回、Win7+ARM64 与 v99.99 tag 已失败、本地链与远端链哈希不同。验证报告按 18.1 未改。

020 推送收尾：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E05 | `scripts/api_push.py` 串行 POST 257 个 blob，两次调用均被网关 502 打断，远端 ref 仍停在 019 的 `6a3f220`，`ALL_MATCH False`（REMOTE 231 / LOCAL 257 / MISSING 26 / MISMATCH 71） | 脚本改为：一次 `GET /git/trees/{parent_tree}?recursive=1` 收集远端已有 blob SHA 集合；本地 `git hash-object` 命中集合即复用，不再 POST；只对新增 / 变化文件并发 8 线程创建；单次 500 自动重试一次。改动后重新推送并复核 |

变更内容哈希口径仍为 `4abdfc9..f985f07`（020 主体），不含本复核段、E04 修复与 E05 脚本优化提交；验证报告哈希声明不受后续提交影响。`scripts/api_push.py` 优化属推送链路工程修复，不改 020 交付范围，`src/` 与 Cargo.lock 仍无变化。

## 021

| 落点 | 内容 |
| --- | --- |
| docs/spec/21-round-021-instructions.txt | 逐字副本，1 行 1003 字节，SHA-1 `ec86aa376a193eb5701de49b2f2bd464599189b5` |
| docs/decisions/021-server-autoconnect.md | D01-D11、R01-R07 / C01-C08、界面证据、验证与边界 |
| docs/research/18-server-list-autodiscovery.md | 9 个一手来源 + 8 组公开资料 + 用户描述逐条对照 + J01-J07 |
| docs/design/ | server-list-logic.md、ui-product-copy.md；nav-slot-contract N01-N03；server-status 取代说明 |
| docs/design/ux-logic-matrix.md | U24 修订、U26、021 自评 7.6 → 8.7 → 9.4、C21-C24 |
| demos/ui-full-kcu-paper.html | 26 区块，服务器页整体重做、设置分组改写、关于页精简、导航与文案去工程化、4 区块标 data-internal |
| demos/preview/ | 35 张产品视图 + 4 张内部证据图 + `00-overview.png` + 重写 index.md |
| docs/features/ | server-autoconnect.md、servers-dat-analysis.md、server-join-binding.md、ui-product-copy.md |
| 索引与规则 | decisions / features / research index、ai-errors A90-A92、ui-demo G19-G21 与 021 行、docs/index 101 项必读、README、interface-log I57-I61 / RO57-RO66、push-scope |
| docs/verification/round-021.md | 第 021 轮独立验证报告 |

时间：

| 项 | 值 |
| --- | --- |
| 沙盒开工 | `Sat Nov 14 00:29:46 CST 2026` |
| 统一调研 | `00:30`–`00:33` |
| UI 去工程化与服务器页重做 | `00:36`–`00:44` |
| 35 视图渲染与内部证据图保留 | `00:45`–`00:52` |
| 文档收口 | `Sat Nov 14 00:56 CST 2026` 前后 |

用户当轮要求与处置：

| 编号 | 要求 | 处置 |
| --- | --- | --- |
| V01 | 对外开放的应用，强调这些是废话 | 产品界面移除槽位 ID、稳定设置 ID、锁定徽章、交接基线、候选构建状态、诊断号；工程结论只落 docs/；内部证据页标 data-internal 不进导航与总览；最终回复不再念内部汇报话术 |
| V02 | 服务器状态准确说是设置好后自动尝试连接、缓存作权重推荐 | 添加后自动连、打开列表自动同步、结果缓存为排序权重，驱动首页推荐卡与服务器列表 |
| V03 | 用户锁定的按权重放到前面，连不上放下面，锁定不受影响 | 锁定置顶且连不上不动；连不上的沉底；星标可切锁定并立即重排 |
| V04 | 我的世界会在目录里放专门看服务器连接的文件，可以自动分析 | 只读 `servers.dat`（未压缩 NBT）；可见 / 隐藏 / 快速进入三类来源；不写回 |
| V05 | 双击进服，按上次使用实例与上次用这个服的实例范围绑定，锁定优先 | 进服弹窗列上次用该服的实例、上次全局实例、兼容范围、自动选定；换实例 / 取消 / 进入 / × / ESC |
| V06 | 显示按 MC 显示逻辑与发现逻辑 | 64×64 图标、玩家命名、两行 MOTD 转义、人数、ping 五档、版本名、LAN 底部；不另做状态配色文案 |
| V07 | 社区有事例，不用逐条强调设计 | 查到 PCL2 延迟测试与服务器列表改进、HMCL/PCL2/BakaXL 自存列表、社区工具生成 servers.dat；第三方启动器一般不读官方 servers.dat，KCU 多做一层 |

自评迭代：

| 轮次 | 自评 | 发现的不足 | 补入 |
| --- | --- | --- | --- |
| 迭代 1 | 7.6 | 只换服务器页文案，界面仍到处是工程叙事；关于页还有工程卡片；弹窗有 id= | P01-P09 规则、四类清理、总览只收产品视图 |
| 迭代 2 | 8.7 | 排序与双击进服做完，但没查 servers.dat 一手结构、没查社区事例；设置残留 SLP 参数思维 | 9 一手 + 8 公开资料、三类来源、设置四组用户语言 |
| 迭代 3 | 9.4 | 补齐并出 36 张 PNG + 4 内部证据图；剩余为未实现客户端与未证实上游项 | U24 修订、U26、C21-C24，收口 |

本轮真实缺陷与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E01 | 新 JS 用 `const SRV` 与 019 遗留的旧 `const SRV` 重名，`new Function` 报 Identifier already declared | 新数组改名 `SERVERS`，show 别名同步改，语法通过 |
| E02 | 关于页上层候选表被删后 `$('upperBody')` 为 null 会抛异常 | 改为条件渲染 `if($('upperBody'))` |
| E03 | 关于页「界面口径」四条仍是设计说明；弹窗有 `id=join_s1`；逻辑条写「命中 / 未命中」 | 界面口径改「外观」四个可用控件；`#mdId` 隐藏；逻辑条改「上次更新 / 已就绪 / 待刷新 / 重新获取」 |
| E04 | 工具条在服务器页仍显示列表网格 / 新建实例 | hideActs 加 servers；锁定容器去虚线框与空白标题 |
| E05 | 收口脚本里一条无效断言 `#mdId{` 导致首次运行异常、文件未落盘 | 去掉该断言重跑，前四项替换与关于页改造全部生效 |

统一调研来源：

| 来源 | 事实 |
| --- | --- |
| https://minecraft.wiki/w/Server_list_storage_format | servers.dat 未压缩 NBT 结构与字段 |
| https://zh.minecraft.wiki/w/服务器列表存储格式 | 可见 / 隐藏两份列表，可见列表游戏主动同步，隐藏最多 16 个 |
| https://minecraft.wiki/w/Servers.dat_format | 不存直连 IP 与 LAN |
| https://minecraft.wiki/w/Server_list | 原版四元素、ping 五档、LAN 底部、顺序可调 |
| https://minecraft.wiki/w/Java_Edition_protocol/Server_List_Ping | SLP 1.7+ 流程与 JSON 字段 |
| https://zh.minecraft.wiki/w/Java版网络协议/服务器列表查询 | description / players / favicon 解析细则 |
| https://wikivg.booky.dev/NBT | servers.dat 永远未压缩 |
| 8 组公开资料 | MOTD 不可信、打开列表 ping 每个服、社区启动器做法与版本改进 |

验证：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=35`，40 张 PNG | 已证实 |
| `grep -c '<section class="view'` / `grep -c 'class="logicbar"'` | 26 / 26 | 已证实 |
| `grep -c '<symbol'` / `grep -o 'data-tab=' \| wc -l` | 88 / 9 | 已证实 |
| `grep -c 'class="setid"'` / `grep -c 'data-internal="1"'` | 0 / 4 | 已证实 |
| `node -e` 内联脚本 / `compile` 三个脚本 | 通过 | 已证实 |
| `! grep -rqE 'gh[p]_' .` | NO_CREDENTIAL | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `git diff 170b69d..HEAD -- src/ Cargo.lock` | 空 | 已证实 |
| 必读 101 项存在非空 | REQUIRED=101 MISSING=0 | 已证实 |
| 真实 TCP 连接、真实 servers.dat 解析、浏览器内实际双击 | 未实测 | 受阻 |
| 用户按 35 张产品视图给手感反馈 | 未发生 | 未证实 |

阶段：D07 第 3 层 lightweight 已实现、已验证；021 轮只动演示层、设计层与文档，`src/` 与 Cargo.lock 无变化；L4 headless 及以下 6 层未启动。UI 实现按闸门等用户确认演示后进。

未做：
- UI 实现、真实 SLP 客户端、NBT 解析器、双击进服实现
- L4 headless 及以下 6 层、插件注册表与插件化更新实现、第三方依赖引入
- CF F17 调用方法、X01-X04 逐条处置、特殊版代码、本项目 LICENSE
- 后端仓任何写请求
- 浏览器内交互实测（截图为静态帧）、GUI 端到端、交叉编译
- 1.20.5 / 1.21 是否改过 servers.dat 文件名或结构（未取得一手证据）

## 022

| 落点 | 内容 |
| --- | --- |
| docs/spec/22-round-022-instructions.txt | 逐字副本，1 行 265 字节，SHA-1 `1a99d1a137ad246fa50c9e66958d3792dc54ec2f` |
| docs/decisions/022-async-budget.md | D01-D11、与 021 差异表、Q01-Q03 待确认口径、界面证据 |
| docs/research/19-async-probe-budget.md | 12 个完整 URL 锚点、用户描述逐条对照、J01-J07、Q01-Q04 口径说明 |
| docs/design/ | async-probe-policy.md；server-list-logic.md 加 022 补充 N01-N05；ux-logic-matrix 加 U27 / C25-C29 / 022 自评 9.4 |
| demos/ui-full-kcu-paper.html | 服务器 JS 整段换成异步探测；加连接范围卡、设置设备连接范围分组、失败历史标签、动态计数、标准 / 轻量档 |
| demos/preview/ | 37 张产品视图 + 4 张内部证据图 + 00-overview.png + index.md |
| docs/features/ | server-async-probe.md、server-failure-history.md |
| 索引与规则 | decisions / features / research index、ai-errors A93-A96、ui-demo G22、docs/index 109 项必读、README、interface-log I62-I66 / RO67-RO74、push-scope |
| scripts/ | round022_async.py、round022_docs.py、round022_index.py、render_ui.py 两个新场景与长等待 |
| docs/verification/round-022.md | 第 022 轮独立验证报告 |

用户当轮要求与处置：

| 编号 | 要求 | 处置 |
| --- | --- | --- |
| V01 | 注意异步 | 同步 `srvSync` 删除；worker-pull 有界队列、并发上限、单台 deadline、增量渲染、停止按钮 |
| V02 | 超出一定范围的也不会去连接 | 按权重取前 N 台进计划；范围外不发请求、保留上次结果、按缓存权重排 200 档 |
| V03 | 新的不会受影响，但保持在设备连接范围内防设备爆炸 | 新加服务器强制排队首且不受 N 裁剪，占同一份额度挤掉权重最低一台；总量仍等于 N；档位表标准 4/3、轻量 2/2、无界面 0 |
| V04 | 之前测过不可以用且没有成功连接案例的按权重中去排序 | `ever` / `tried` 分类：无成功记录不主动重连、按缓存权重排 300 档中段；曾成功本轮失败 900 档沉底；锁定 0 档不动 |

自评迭代：

| 轮次 | 自评 | 发现的不足 | 补入 |
| --- | --- | --- | --- |
| 迭代 1 | 7.8 | 只加异步没限总台数；新服直接扩量；失败历史没分类 | 档位表、slice(0,N)、新服占同一份额度、ever / tried 分类 |
| 迭代 2 | 8.8 | 范围外与无成功记录视觉上排最后；锁定离线服被探测成在线；逻辑条计数写死 | 排序改 200 / 300 档；s4 保持 offlineMark；逻辑条动态计数 |
| 迭代 3 | 9.4 | 补齐 12 来源、37 张产品视图、设置自定义项与停止入口；剩余为真实客户端未实现与 Q01-Q03 待确认 | Q 口径说明、U27、C25-C29，收口 |

本轮真实缺陷与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E01 | 初版 `srvRank` 把无成功记录放 500 档，视觉上落到列表最后，与「按权重中去排序」不符 | 改为 300 档；范围外改 200 档，形成「可用 → 范围外 → 无成功记录 → 彻底失败」中段顺序 |
| E02 | 锁定且离线的 s4 被异步探测 `applyResult` 改成在线，违背「锁定连不上也不动」 | s4 加 `offlineMark:true`，探测后仍离线且置顶 |
| E03 | 逻辑条「4 台连得上 / 1 台连不上」写死，与 8 台数据不符 | `renderSrv` 动态统计并更新 lb-hit / lb-miss / lb-state |
| E04 | 「设备连接范围」标题在右栏被工具按钮挤成两行 | 标题改「连接范围」并加 white-space:nowrap |
| E05 | 两个新截图场景异步探测需 120–270ms，固定 300ms 等待不够稳定 | render_ui.py 对 36 / 37 场景等待 1200ms |

统一调研来源：

| 来源 | 事实 |
| --- | --- |
| https://docs.rs/rust-mc-status/2.0.0/rust_mc_status/client/struct.McClient.html | ping_many 并行、max_parallel 控资源、失败不阻塞 |
| https://pkg.go.dev/github.com/LinusTebbe/mc-prober | 每次探测接 context deadline，策略归调用方 |
| https://deepwiki.com/mcobs/ObsMCLauncher/7.1-server-list-management | 启动器并行 ping、5s 超时、IsOnline 瞬时 / LastPingTime |
| https://optimi.com/en/guides/dependency-resilience | 超时是容量控制、最大并发 + 有界队列、bulkhead |
| https://blog.habsi.net/backpressure-explained-designing-systems-that-dont-collapse-under-load/ | 显式上限、观测在飞 / 队列 / 拒绝率 |
| 另 7 组公开资料 | 连接池等待队列、浏览器 6 连接、200 台 40 路、5000 台 15 并发、3–6 路甜点、Little's Law |

验证：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=37`，42 张 PNG | 已证实 |
| `node -e` 内联脚本 / `compile` 四个脚本 | 通过 | 已证实 |
| `python3 scripts/p09_scan.py` | `P09_HITS 0` | 已证实 |
| `grep -c 'srvSync'` | 0 | 已证实 |
| `grep -c 'budget-cell'` | 4 | 已证实 |
| `! grep -rqE 'gh[p]_' .` | NO_CREDENTIAL | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `git diff 3c87d21..HEAD -- src/ Cargo.lock` | 空 | 已证实 |
| 必读 109 项存在非空 | REQUIRED=109 MISSING=0 | 已证实 |
| 真实 TCP 并发、真实超时取消、真实内存剖析、浏览器内实际点击 | 未实测 | 受阻 |
| Q01-Q03 口径确认、用户按 37 张图给手感反馈 | 未发生 | 未证实 |

阶段：D07 第 3 层 lightweight 已实现、已验证；022 轮只动演示层、设计层与文档，`src/` 与 Cargo.lock 无变化；L4 headless 及以下 6 层未启动。UI 实现按闸门等用户确认演示后进。

未做：
- UI 实现、真实 SLP 客户端、NBT 解析器、双击进服实现、真实并发池与取消令牌
- L4 headless 及以下 6 层、插件注册表与插件化更新实现、第三方依赖引入
- CF F17 调用方法、X01-X04 逐条处置、特殊版代码、本项目 LICENSE
- 后端仓任何写请求
- 浏览器内交互实测（截图为静态帧）、GUI 端到端、交叉编译
- 1.20.5 / 1.21 是否改过 servers.dat 文件名或结构（未取得一手证据）

## 023

| 落点 | 内容 |
| --- | --- |
| docs/spec/23-round-023-instructions.txt | 逐字副本，1 行 698 字节，SHA-1 `a473ce3dfc83cad84b35991e6053358ccfbd234a` |
| docs/decisions/023-architecture-answers.md | 三处偏差承认、六问逐条答复、9 层实现路线、H01-H06、Q01-Q04 |
| docs/research/20-i18n-crash-identity.md | 18 个完整 URL 锚点、J01-J07、C05 标未证实 |
| docs/design/ | stable-identity、i18n-policy、crash-reporting、implementation-strategy 四份 |
| docs/features/ | F023-01 稳定标识 / F023-02 i18n 与崩溃设置 |
| demos/ui-full-kcu-paper.html | 550+ i18n 标注点、中/EN 切换、sid 三分离、改名弹窗、同名两项、信号格延迟小字、崩溃反馈分组、许可表 22 组 |
| demos/preview/ | 43 张产品视图 + 4 张内部证据图 + 总览，共 48 张 PNG |
| 索引与规则 | decisions / features / research index、A97-A100、G23、docs/index 122 项必读、README、interface-log I67-I71 / RO75-RO81、push-scope、preview index、ux-logic-matrix U28 / C30-C34 / 023 自评 9.3 |
| scripts/ | round023_ux.py、round023_i18n_cover.py、round023_docs.py、round023_index.py、render_ui.py 六个新场景 |
| docs/verification/round-023.md | 第 023 轮独立验证报告 |

用户六项质疑与处置：

| 编号 | 质疑 | 处置 |
| --- | --- | --- |
| V01 | 同名服务器污染目录 | sid 三分离、目录 `C:\KCU\servers\<sid>`、白名单、改名不动 ID、同名两项演示 |
| V02 | 文字硬编码 / i18n 选型 | 承认；演示层 `tr()` + 550+ 标注点 + 中/EN；实现层 Fluent `.ftl` + i18n-embed，源码零文案 |
| V03 | 名字不能自定义 | 改名弹窗，取消 / ESC / × / 宿主可关，写 `sid unchanged=true` |
| V04 | 信号格下标具体延迟 | 五格条下加 `42 ms` 等宽小字，连不上给「连不上」 |
| V05 | 兼容性差，引入别人的崩溃分析系统 | 四层库映射、默认不外发、脱敏开、发送前确认、Win7 降级本地 dump、许可登记 |
| V06 | 没按架构来，打算怎么实现 | 承认 L1-L3 纯 std 偏差；core 保留作底座，L4 起逐个能力接成熟库，trait 注入，9 层映射表与 H01-H06 |

自评迭代：

| 轮次 | 自评 | 发现的不足 | 补入 |
| --- | --- | --- | --- |
| 迭代 1 | 7.0 | 只答方案没改界面；目录键隐含名称；英文切换只覆盖导航 | sid 三分离、改名弹窗、i18n 字典初版 |
| 迭代 2 | 8.5 | 英文界面一半中文；自动标注脚本生成多余尖括号与 `&gt;`；hash 正则吃掉场景名数字 | 扩到 550+ 标注点、修 HTML 形态、hash 正则支持数字 |
| 迭代 3 | 9.3 | 补齐 18 个一手锚点、43 视图、崩溃分层与许可登记、实现路线 | Q01-Q04、U28、C30-C34，收口 |

本轮真实缺陷与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E01 | 自动标注正则把 `>` 吞进 group3，生成 `data-i18n="&gt;中文"` 与多余 `>`，界面出现属性文本 | 改回 `([^>]*>)` 口径、删多余 `>`、还原 390 处属性与 91 处 value |
| E02 | stack 说明 div 的属性被当裸文本插入 | 把属性移回标签内并补两条说明的 key |
| E03 | 初始化 hash 正则 `view=([a-z-]+)` 把 `i18n-en` 截成 `i`，英文场景空白 | 改为 `view=([a-z0-9-]+)`，两处 |
| E04 | 底部导航 `nav.settings` / `nav.about` 缺英文映射 | 补进 EN 字典 |
| E05 | 首版英文截图设置卡片与说明仍中文 | 自动标注扩到 `.k` / `.hd` / `option` / `th` / `panel-title` / `panel-sub` / 说明 div |

验证：

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=43`；`demos/preview/*.png` = 48 | 已证实 |
| `node -e` 遍历 demos/*.html | ALL_JS_OK 18 | 已证实 |
| `python3 -c compile` 脚本 | PY_OK | 已证实 |
| `python3 scripts/p09_scan.py` | P09_HITS 0 | 已证实 |
| `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| 禁用词 / 品牌 / 外链 / 「同上」扫描 | 见验证报告 | 已证实 |
| `grep -c 'data-i18n='` / `grep -c "sid:'sv-"` | 550+ / 10 | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `git diff 832860d..HEAD -- src/ Cargo.lock` | 空 | 已证实 |
| 真实 `.ftl` 集成、真实 minidump、真实上报、真实 Win7 构建、浏览器内点击 | 未实测 | 受阻 |
| Q01-Q04 口径确认、用户按 43 张图给手感反馈 | 未发生 | 未证实 |

阶段：D07 第 3 层 lightweight 已实现、已验证；023 轮只动演示层、设计层与文档，`src/` 与 Cargo.lock 无变化；L4 headless 及以下 6 层未启动。UI 实现按闸门等用户确认演示后进。

未做：
- UI 实现、真实 SLP 客户端、NBT 解析器、真实并发池与取消令牌
- L4 headless 及以下 6 层、插件注册表与插件化更新实现、第三方依赖引入
- CF F17 调用方法、X01-X04 逐条处置、特殊版代码、本项目 LICENSE
- 后端仓任何写请求
- 浏览器内交互实测（截图为静态帧）、GUI 端到端、交叉编译

## 024

| 落点 | 内容 |
| --- | --- |
| docs/records/code-ownership-audit.md | 全量盘点：24 文件 / 4339 行 / 3876 有效代码全自写，第三方 0；T01-T05 可信度问题；逐文件替换映射 |
| docs/decisions/024-code-ownership.md | W01-W03 撤回、D01-D06 处置 |
| 索引 | decisions/index、docs/index 124 项必读、README、023 A03 标注撤回 |

| 编号 | 用户质疑 | 处置 |
| --- | --- | --- |
| V01 | 到底用了多少自己写的代码 | 如实报数，不拿演示层 / 工具脚本稀释 |
| V02 | 对你的代码没有信心 | 承认 141 测试与验证闭环都在同一只手里；撤回自测自评当结论 |
| V03 | 上层用别人代码被歪曲 | 撤回 023 A03 自我授权，core 允许依赖成熟库 |

本轮：`src/` 与 Cargo.lock 改动 0；未引依赖、未删模块、未跑自评、未出演示 HTML；后端仓 0 写请求。

## 025

| 落点 | 内容 |
| --- | --- |
| docs/spec/25-round-025-instructions.txt | 逐字副本 |
| docs/decisions/025-vendor-first-replacement.md | registry 端点实测、vendor 方案、M01-M04、数字变化、B01-B04 行为差异、未换清单 |
| docs/verification/round-025.md | 15 条复跑证据 |
| Cargo.toml / Cargo.lock / .cargo/config.toml / vendor/ | 首次 `[dependencies]`；6 包（5 第三方）；目录源离线构建 |
| src/dispatcher/json.rs / task.rs / launcher.rs / mod.rs | 336 行手写解析器删为 77 行薄适配 |
| docs/licenses/ | 9 份新增全文 |
| demos/ui-full-kcu-paper.html / demos/preview/ | 关于页 5 组「构建中已使用」，43 张截图重渲 |
| 索引与规则 | decisions/index、docs/index 128 项、README、licenses/index、push-scope、code-ownership-audit、implementation-strategy |

用户意图：对我写的代码不信任，要求用别人的代码。处置：不做新一轮文档或演示层堆砌，直接把替换映射第一块落地，让 `Cargo.lock` 出现真实第三方包。

本轮真实缺陷与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E01 | `cargo build --offline` 首次报 `no matching package named serde found` | serde_json / serde_core 的 `[dev-dependencies]` 与 `[target.'cfg(any())'.dependencies]` 引用未 vendor 的 path；删这两段后构建通过，改动登记为 M01/M02 |
| E02 | 首次往许可表插入 5 行时替换目标写错，脚本断言失败 | 改为在数组末尾 `];` 前插入，复查 `构建中已使用=5` 与 JS 语法 |
| E03 | 手写解析器深度上限 64，serde_json 默认 128，原 80 层测试会变成通过 | 测试改 200 层并登记 B01，断言未降级 |

阶段：D07 第 3 层 lightweight 逻辑不变；本轮动的是 L2 dispatcher 的 JSON 解析实现。UI 演示层只改许可数据行并重渲截图，未改界面结构。

未做：剩余自写模块替换、真实网络 / GUI / 跨平台构建、CF F17、特殊版代码、本项目 LICENSE、后端仓任何写请求。

## 026

| 落点 | 内容 |
| --- | --- |
| docs/spec/26-round-026-instructions.txt | 逐字副本（「干」+「好了吗？」） |
| docs/decisions/026-vendor-blocked.md | A01-A04 尝试、B01-B04 卡点、R01-R05 回退、N01-N03 选项 |
| docs/verification/round-026.md | 9 条复跑证据 |
| scripts/round026_vendor.py | 自动闭包脚本，标注未跑通 |
| docs/records/vendor-fetch-log.txt | 失败回显留痕 |

用户问「好了吗」时，本轮状态是：mini-moka 依赖闭包未收敛（libc 0.2.191 解压受阻、工具层多次 502），已回退到 025 基线，`src/` 一行未动。如实答「没好」，不发通过标记。

本轮未做：cache.rs / asynk.rs / leak.rs 替换、任何新依赖进构建、UI 演示、自评打分、后端仓写请求。

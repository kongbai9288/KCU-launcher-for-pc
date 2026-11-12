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
| docs/decisions/013-build-start.md:86 | 措辞规范化：原句含「为了干什么」命中 014 轮扩展后的措辞扫描词表，改为「不写功能目的说明」，断言含义不变 |

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

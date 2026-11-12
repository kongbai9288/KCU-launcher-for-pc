# 第 016 轮继续搭建决策

| 项 | 值 |
| --- | --- |
| 编号 | 016 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 016 |
| 逐字指令 | docs/spec/16-round-016-instructions.txt，1 行 4 字节，SHA-1 `78dbbdabbcac19f0e4442954bdc5b89d88255abd` |
| 前序阶段 | 015 轮 D07 第 2 层 dispatcher 已实现、已验证，103 项测试 |

## 决策

| 编号 | 项 | 值 | 依据 |
| --- | --- | --- | --- |
| D01 | 本轮动作 | 继续 D07 逐层搭建，进入第 3 层 lightweight | 003-remote.md D07；015 轮「继续」语义 |
| D02 | UI 闸门 | **触发**。轻量极简视图属用户可见界面，按 docs/rules/ui-demo.md 交付整页 HTML | 015 D02、ui-demo.md「轻量模式极简视图改动」 |
| D03 | 整页演示 | `demos/ui-full-lightweight.html`，整页、全区域、全状态、离线可点、本地字体栈、KCU 标识 | ui-demo.md G01-G06、C01-C08 |
| D04 | 用户回路 | 演示先落盘 → 用户按手感调整 → 先改演示 → 确认后才改实现 | 015 D04；F02/F03 |
| D05 | 主题口径 | 演示层提供深浅主题**预览**（手感调整用，明确标注）；实现层按 007 D04 默认**单主题**，不写进轻量实现，除非用户确认要加 | ui-demo.md C03 × 007-normal-ui.md D04；D04 用户调整优先 |
| D06 | 落地层 | B05：login、download、loaders，外加 view 与 mod；`src/lightweight/` | 005-blueprint.md B05 |
| D07 | 未落地层 | headless、normal、ui、server、lan、build、部署；UI 实现未进入构建 | 003-remote.md D07 |
| D08 | 轻量硬约束 | 独立极简视图，不复用 normal.ui；游戏运行期无常驻后台进程 | 007 D03/D06；需求 :16 |

## L3 落地

| 编号 | 项 | 值 |
| --- | --- | --- |
| L01 | 模块 | src/lightweight/{login,download,loaders,view,mod}.rs，5 文件 |
| L02 | 依赖 | std only；复用 core.cache / asynk / leak / envelope / diagnostics / log / popup；Cargo.toml 与 Cargo.lock 未变 |
| L03 | E01 三种登录 | Mojang / Offline / ThirdParty；离线免浏览器；Mojang 无既有凭据时零级禁用正版，第三方不受影响 |
| L04 | 三级回退 | 外置浏览器 → 内置浏览器 → 连接码；每级写 2 级降级诊断；连接码 300s 超时落 0 级；全失败不崩 |
| L05 | WebView2 | `WebView2Probe` 可用性由宿主注入，不写死注册表检测键（该键仍未证实） |
| L06 | K07 Provider | Mojang / BMCLAPI 两源；镜像测速软策略；`region_override` 只用于下载源选择，不与地区禁用复用；API Key 注入式、可选 |
| L07 | 批量请求 | 一次请求带多个 id，每页 20；10 个 id 一次请求、45 个 id 三页三请求；逐条目单发列为禁止项；core.cache 单飞，10 次重复批次只发 1 次 |
| L08 | CF 边界 | 本层不暴露 CurseForge 下载源；CF F17 具体调用方法未提供，X01-X04 未逐条拍板 |
| L09 | E03 加载器 | 六种注册、去重、排序；只登记标识与安装结果，**不写死 version json 注入字段**（逐版本 schema 未证实） |
| L10 | 视图排除 | 13 项：normal.ui、设计稿、揉纸纹理、双主题实现、三栏拖拽、table.grid、衣柜、工具箱、设备桥接面板、分步向导、右键菜单、日志抽屉、内嵌文件管理器 |
| L11 | 文件管理 | 只返回打开系统文件管理面板动作，不内嵌管理器 |
| L12 | 日志 | LogBuffer 每 100 行分片，有界 |
| L13 | 进程模型 | `launch_game` 后 `game_running=true`、`launcher_alive=false`，游戏运行期无常驻后台进程 |
| L14 | 弹窗与用户操作 | 11 类目录全注册全关闭，流程结束 0 残留；9 类视图动作全部有响应；取消可中断 |
| L15 | 诊断 | 全部 `[KCU] <域> <动作> <目标> <结果> <详情>` 单行；统一信封带 request_id |

## 整页演示覆盖

| 编号 | 项 | 落点 |
| --- | --- | --- |
| U01 | 导航与分区 | 6 个页签：登录、下载、加载器、文件与日志、状态覆盖、弹窗全集 |
| U02 | 主内容 | 三种登录卡片、三级回退链、连接码框、下载源与批量结果、6 个加载器、基础日志 |
| U03 | 状态栏 | 内存占用示意（标未实测）、后台进程、网络请求数、弹窗残留 |
| U04 | 深浅主题 | 演示层预览切换，标注「实现默认单主题」 |
| U05 | 状态覆盖 | 空态、加载态、错误态、被锁态、就绪，5 种 |
| U06 | 弹窗 | 11 类，按钮 / ESC / 取消 / 确认 / 宿主 5 类关闭路径，全部关闭后 0 残留 |
| U07 | 手感调整 | 主题、间距、字号、圆角、重置；每改一次写诊断行 |
| U08 | 品牌与离线 | KCU 标识内联 SVG；无外部字体 CDN 与远端脚本；无 FCL / 揉纸启动器字面量 |
| U09 | 轻量说明 | 页头标 ≤2GiB 自动进入、单主题、无常驻进程；下载页标每页 20、禁逐条目单发、CF 不暴露 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline` | 141 passed / 0 failed / 0 ignored / 0 measured，0.12s；doc-tests 0 | 已证实 |
| `cargo test --offline lightweight::` | 38 passed（login 8 / download 12 / loaders 7 / view 11） | 已证实 |
| `cargo build --release --offline` | 通过，rlib 1353366 字节 | 已证实 |
| `git ls-files src/lightweight/ \| wc -l` | 5 | 已证实 |
| `node -e` 遍历 demos/*.html | 16 份内联脚本语法通过 | 已证实 |
| `grep -c 'class="node"' demos/round-016-lightweight.html` | 13 | 已证实 |
| `! grep -rE 'FCL\|揉纸启动器\|https?://' demos/ui-full-lightweight.html` | exit 0 | 已证实 |

## 本轮边界

| 项 | 值 |
| --- | --- |
| 落地 | L3 lightweight 5 文件、整页 UI 演示、运行逻辑演示、4 份功能 md、1 份决策、索引与记录 |
| 未落地 | L4 headless 及以下 6 层、UI 实现、CF 下载模块、特殊版代码、LICENSE 文件 |
| 后端仓 | 0 个写请求 |
| 凭据 | 全仓零字面量，`.git/config` 干净 |
| 用户手感回路 | 已触发，整页演示已交付；用户对演示的调整意见优先于当前实现 |

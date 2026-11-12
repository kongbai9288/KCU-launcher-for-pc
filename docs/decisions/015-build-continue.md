# 第 015 轮继续搭建决策

| 项 | 值 |
| --- | --- |
| 编号 | 015 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 015 |
| 逐字指令 | docs/spec/15-round-015-instructions.txt，1 行 204 字节，SHA-1 `303ec47156132af4816dfa9e210671b35d9835d0` |
| 前序阶段 | 014 轮 D07 第 1 层 core 扩展完成，12 模块、56 测试 |

## 本轮输入切分

| 片段 | 逐字 | 落定 |
| --- | --- | --- |
| F01 | 干 | D01 |
| F02 | 对了，如果说你要是动用户界面的时候你需要把整个用户界面都用html演示出来 | D02、D03 |
| F03 | 这样的话我能根据我的手感来调整 | D02、D04 |
| F04 | 不过你现在先按照原来的进度继续干 | D05 |

## 决策

| 编号 | 项 | 值 | 依据 |
| --- | --- | --- | --- |
| D01 | 本轮动作 | 继续 D07 逐层搭建，进入第 2 层 dispatcher | F01、003-remote.md D07 |
| D02 | UI 演示闸门 | 改动用户界面的轮次，必须交付一份覆盖该界面全部可见区域与交互状态的整页 HTML 演示；不是运行逻辑状态机，不是局部截图，不是文字描述 | F02 |
| D03 | 演示验收 | 整页演示须可离线打开、可点击、深浅主题与关键控件可切换；用户凭手感调整后，改动再进入实现 | F02、F03 |
| D04 | 手感调整回路 | 用户对整页演示的调整意见优先于当前实现；演示与实现分开落盘，演示文件不进 `src/` | F03 |
| D05 | 本轮是否触发 | 不触发；本轮不动用户界面，按原进度推进 dispatcher | F04 |
| D06 | 落地层 | B04：task、mode、launcher，外加 json 解析底座；`src/dispatcher/` | 005-blueprint.md B04 |
| D07 | 未落地层 | lightweight、headless、normal、UI、构建、部署及 server/lan 分支 | 003-remote.md D07、005-blueprint.md B01 |
| D08 | UI 稿定位 | 沿用 014 D03：样板与交互参考，不直接复用；整页演示将按 KCU 品牌重新绘制 | 014-build-continue.md D03 |

## UI 闸门细则

| 编号 | 项 | 值 |
| --- | --- | --- |
| U01 | 触发条件 | 本轮或后续轮次新增、修改、删除任何用户可见界面元素 |
| U02 | 交付物 | `demos/ui-full-*.html`，整页、全区域、全状态 |
| U03 | 内容范围 | 导航、侧栏、主内容、弹窗、状态栏、深浅主题、空态、加载态、错误态、关闭路径 |
| U04 | 交互范围 | 每个可点击控件有响应；每个弹窗有关闭逻辑；流程结束 0 残留 |
| U05 | 用户回路 | 用户按手感提出调整 → 先改演示 → 确认后再改实现 |
| U06 | 不触发条件 | 仅改动调度逻辑、下载逻辑、数据结构、文档、测试、CI |
| U07 | 本轮状态 | 不触发，未生成 ui-full 演示；本轮 HTML 为 dispatcher 运行逻辑演示 |
| U08 | 轻量模式 | 极简视图独立；其整页演示在 lightweight 层触发时单独交付，不复用 normal.ui 资产 |

规则文件：docs/rules/ui-demo.md。防错项：docs/checklists/ai-errors.md A62。

## L2 dispatcher 落地

| 编号 | 项 | 值 |
| --- | --- | --- |
| L01 | 模块 | src/dispatcher/json.rs、task.rs、mode.rs、launcher.rs、mod.rs |
| L02 | 依赖 | std only；未引入 serde、未引入 async runtime、Cargo.toml / Cargo.lock 未变 |
| L03 | JSON 底座 | 递归下降解析 object / array / string / number / bool / null；拒绝尾随内容、前导零、控制字符、深度 > 64；`\uXXXX` 与中文 UTF-8 |
| L04 | K05 LaunchTask | 任务 json → 统一任务；缺字段按内置默认；空集合返回默认任务；任务集合按 id 排序去重；命令行单参数进服覆盖任务文件 |
| L05 | K06 ModeSelector | 强制无头 > 命令行 > config/launch.json > 任务 > 自动判定；`≤ 2 GiB && 首次` → lightweight，否则 normal；非法模式零级报错；内存检测失败二级降级 |
| L06 | 启动级兜底 | 连续 3 次失败进入安全模式、忽略自定义配置用内置默认；安全模式仍失败导出诊断包（日志 / 配置快照 / 运行时信息 / 已加载模块列表） |
| L07 | 分级 | 0 致命明确报错不崩、1 功能失效禁用提示、2 自动切换提示、3 记日志 |
| L08 | 正版凭据保护 | headless 且无既有正版文件 → `premium_allowed=false`；有则允许；安全模式一律 false |
| L09 | UI 分流 | 仅 normal 加载 ui 框架；lightweight / headless / safe 不加载；弹窗全部注册并全部关闭 |
| L10 | 用户操作 | 单参数直接进服、双击服务器按权重选符合版本实例、用户指定排第一、不兼容可见且不崩、流程结束 0 残留 |
| L11 | 缓存 | 复用 core.cache；同一任务文本 10 次 dispatch 只解析 1 次；40 个不同任务后 len/order ≤ 4；inflight=0 |
| L12 | 异步 | 复用 core.asynk 的 CancelToken；dispatch 入口与中途检查取消；无常驻后台进程 |
| L13 | 泄漏 | outcome 经 Tracker 跟踪，drop 后 live 归零；cache inflight 用 Weak；LogBuffer 有界分片；reset 清态 |
| L14 | 诊断 | 全部 `[KCU] <域> <动作> <目标> <结果> <详情>` 单行；统一信封带 request_id 与 error |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline` | 103 passed / 0 failed / 0 ignored / 0 measured | 已证实 |
| `cargo test --offline dispatcher::` | json 7 + task 8 + mode 12 + launcher 20 = 47 passed | 已证实 |
| `cargo build --release --offline` | 通过，rlib 1065652 字节 | 已证实 |
| `git ls-files src/dispatcher/ \| wc -l` | 5 | 已证实 |

## 本轮边界

| 项 | 值 |
| --- | --- |
| 落地 | L2 dispatcher 5 文件、5 份功能 md、1 份决策、1 份规则、1 份运行逻辑 HTML、索引与记录 |
| 未落地 | L3 lightweight 及以下、整页 UI 演示、UI 实现、CF 下载模块、特殊版代码、LICENSE 文件 |
| 后端仓 | 0 个写请求 |
| 凭据 | 全仓零字面量，`.git/config` 干净 |
| 用户手感回路 | 未触发，等到动 UI 的轮次执行 U01-U08 |

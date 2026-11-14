# 功能到实现的分层映射

| 项 | 值 |
| --- | --- |
| 轮次 | 023 |
| 状态 | 已批准（设计层）；实现层未启动 |
| 依据 | docs/decisions/023-architecture-answers.md Q6；013 D07 逐层顺序；020 上层第三方库约束 |

## 分层现状与手段

| 层 | 能力 | 现状 | 实现手段 | 依赖边界 |
| --- | --- | --- | --- | --- |
| L1 core | 缓存 / 异步 / 泄漏 / 用户流程 / 弹窗 | 已落地，纯 std，141 测试 | **保留纯 std** | 不引第三方 crate |
| L2 dispatcher | 任务 / JSON / 模式判定 / 统一信封 | 已落地，纯 std | 保留 | 不引 |
| L3 lightweight | 登录回退 / 批量拉取 / 加载器注册 / 极简视图逻辑 | 已落地，纯 std | 保留逻辑 | 视图渲染交给 L5 宿主 |
| L4 headless | 无界面调度、配置、命令 | 未启动 | `serde` + `toml`，配置读写；命令与信封沿用 core | L4 起允许引库 |
| L5 normal / UI | 43 个产品视图（演示层） | 实现未进构建 | `tao` + `wry`（或 slint，授权待定）；Fluent 管文案；Lucide ISC 图标 | 只走 `K08 UiFrame` |
| L6 网络 | 批量、镜像、超时、取消 | 未实现 | `reqwest` + `tokio`，连接池有界、批量 id 一次请求、CancelToken | core 只认 `NetProvider` trait |
| L7 崩溃 | 捕获 / 解析 / 上报 | 未实现 | Q5 四层库 | core 只认 `CrashSink` trait |
| L8 插件与更新 | 槽位、隔离、签名 | 设计已定 | `libloading` + C ABI / 子进程隔离；更新器作为插件 | 插件不碰 `core.locked.*` |
| L9 构建部署 | Win7 / 多架构 / 发行物 | 未实现 | `*-win7-windows-msvc` Tier 3 + build-std；i686 / x86_64 / aarch64 | CI 用腾讯 rustup 镜像 |

## 功能 → 库 → 许可证 → 状态

| 功能 | 库 | 许可证 | 状态 |
| --- | --- | --- | --- |
| 窗口与 WebView | tao / wry | Apache-2.0 / MIT（双） | 候选 · 未进构建 |
| 界面文案 | fluent / i18n-embed | Apache-2.0 OR MIT / MIT | 候选 · 未进构建 |
| 图标 | Lucide | ISC（Feather 派生 MIT） | 演示层已使用 |
| 配置序列化 | serde / toml | MIT OR Apache-2.0 / MIT OR Apache-2.0 | 候选 · 未进构建 |
| 网络与异步 | reqwest / tokio | MIT OR Apache-2.0 / MIT | 候选 · 未进构建 |
| 崩溃捕获 | sentry-minidump / minidump / sentry-native | MIT / MIT / MIT | 候选 · 未进构建 |
| 崩溃后端 | Breakpad | BSD-3-Clause | 候选 · 未进构建 |
| 稳定 ID | uuid | MIT OR Apache-2.0 | 候选 · 未进构建 |
| 错误与诊断 | anyhow / tracing | MIT OR Apache-2.0 / MIT | 候选 · 未进构建 |
| 插件装载 | libloading | ISC | 候选 · 未进构建 |
| 更新签名 | ed25519-dalek / minisign 方案 | BSD-3-Clause / MIT | 候选 · 未进构建 |
| 本地存储 | rusqlite（可选） | MIT | 候选 · 未进构建 |

## 硬规则

| 编号 | 内容 |
| --- | --- |
| H01 | 第三方只在 L4+ 注入；core 通过 trait 拿能力，不直接依赖 crate。 |
| H02 | LICENSE 全文 + 关于页七列表 + `THIRD-PARTY-NOTICES.md` 三处齐备后才加进 Cargo.toml。 |
| H03 | 插件加载后动态追加其项目名、许可证、作者、项目地址、修改后版本地址。 |
| H04 | 设置与关于锁定在 `core.locked.*`；插件只往 `slot:plugin.*` 追加。 |
| H05 | 更新只换插件包；核心二进制不动；签名校验不可禁用；失败保留旧插件可回滚。 |
| H06 | 手感回路：演示 → 截图 → 用户确认 → 实现；本轮 `src/` 与 Cargo.lock 无变化。 |
| H07 | 后端仓 0 写请求；凭据只从环境变量读；诊断包不进公仓。 |

## 不再手写的清单

| 能力 | 原做法 | 023 起 |
| --- | --- | --- |
| JSON 解析 | L2 手写递归下降 | core / dispatcher 保留（无依赖可测）；L4+ 业务 JSON 用 `serde_json` |
| 网络批量 | L3 手写批量演示 | 真实请求交给 reqwest 连接池与批量接口 |
| 复数 / 语言协商 | 演示层字典 | `.ftl` + `i18n-embed` |
| 原生崩溃栈 | 未做 | minidump 系列 |
| 插件 ABI | 未做 | C ABI + libloading / 子进程 |
| 窗口与渲染 | HTML 演示 | tao + wry |

## 交接口径

| 项 | 值 |
| --- | --- |
| 底座 | L1-L3 纯 std 已测，不动 |
| 下一层 | L4 headless；开工前需 Q02（UI 宿主授权）与手感反馈落定 |
| 新对话 | 读 `docs/index.md` 必读项 + `docs/design/handoff.md` 即可接上 |
| 未证实 | Q01-Q04、L4 以下实现、LICENSE 全文取得、真实 Win7 构建 |

## 025 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 | **已落地**：手写 `dispatcher/json.rs` 换为 `serde_json`，vendor 目录源离线构建通过 |
| 配置序列化 / 参数 / 路径 / 日志 / 缓存 / 异步 / 网络 / UI / 崩溃 / 插件 | 未启动，仍为自写或候选 |

registry 在本环境被 403 阻断，故采用 `vendor/` + `.cargo/config.toml` 目录源；正式联网 CI 可改用 registry 直连，业务代码不需改动。

## 027 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 | 已落地（025，serde_json） |
| 异步 / 线程同步 | **已落地（027，crossbeam-channel + crossbeam-utils）** |
| 缓存 | 未启动；mini-moka 大闭包按 026 的 N 选项挂着 |
| 配置 / 参数 / 路径 / 日志 / 网络 / UI / 崩溃 / 插件 | 未启动，仍为自写或候选 |

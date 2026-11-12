# 轻量启动器视图

| 项 | 值 |
| --- | --- |
| 编号 | F003 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 008 登记；016 实现 |
| 依据 | docs/spec/00-requirements.txt:9-16；docs/decisions/007-normal-ui.md D03-D06；docs/decisions/016-build-continue.md |

## 怎么运作

`src/lightweight/` 5 模块：login（E01 三种登录 + 三级回退）、download（K07 Provider + 批量请求）、loaders（E03 六种注册）、view（极简视图状态、排除项、进程模型）、mod。纯 std，复用 core.cache / asynk / envelope / diagnostics / log / popup。视图由 `LightweightView` 持有单主题、有界日志、弹窗注册表、游戏进程与启动器存活标记；`WebView2Probe` 可用性由宿主注入，不写死检测键。`launch_game` 后启动器退出，游戏运行期无常驻后台进程。整页界面演示见 `demos/ui-full-lightweight.html`，用户按手感调整后先改演示、确认后才改实现。

| 项 | 值 |
| --- | --- |
| 实现状态 | 141 项全量测试中 lightweight 占 38 项 |
| 输入 | AuthKind、StageAvailability、ProviderConfig、批 id 列表、LoaderKind、ViewAction、CancelToken |
| 输出 | LoginStage / BatchReply / InstallOutcome / ViewEvent、统一信封、单行诊断 |
| 视图范围 | 三种登录入口、三级回退链、连接码、下载源、6 加载器、基础日志、系统文件面板 |
| 错误路径 | 外置失败 → 内置；内置失败 → 连接码；连接码超时 → 0 级报错；坏配置与取消均不崩 |
| 空值 | 空账号、空下载源、空 id 集合、空加载器列表按内置默认处理 |
| 超时 | 连接码 300s；缓存加载 5s；CancelToken 全程检查 |
| 编码 | json 与日志 UTF-8；路径由 core.paths 按 OsStr 处理 |
| 排除项 | 13 项，见 docs/decisions/016-build-continue.md L10 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `LoginSession::{new,advance}` | 函数 | AuthKind / StageAvailability / CancelToken / 连接码 | Result<LoginStage,LoginError> | Cancelled / Timeout / ZeroLevel |
| `Downloader::{new,batch,reset,cf_source_exposed}` | 函数 | ProviderConfig / &[String] / CancelToken | BatchReply | String |
| `LoaderRegistry::{register,install,codes,version_json_fields}` | 函数 | LoaderKind / CancelToken | bool / InstallOutcome / Vec | 不写 schema |
| `LightweightView::{handle,flow,close_all_popups,envelope}` | 函数 | ViewAction / AuthKind / CancelToken | ViewEvent / Vec<ViewEvent> / usize / Envelope | 不 panic |
| `WebView2Probe::{injected,unknown,external_available}` | 函数 | bool / 无 | Self / bool | 无 |

子模块功能登记：docs/features/lightweight-login.md、lightweight-download.md、lightweight-loaders.md、lightweight-view.md。

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | lightweight.view（005-blueprint.md B05；003-remote.md D07 第 3 层） |
| 模块路径 | src/lightweight/{login,download,loaders,view,mod}.rs |
| 扩展点 | E01 auth、E02 download（仅 Mojang / BMCLAPI）、E03 loader；E04 ui 不加载 |
| 关键抽象 | K01 Envelope、K02 PathResolver、K03 Diagnostics、K04 FallbackLevel、K07 Provider |
| 依赖 | std only；Cargo.toml / Cargo.lock 未变 |
| 约束 | 不加载 normal.ui、不引用 assets/ui/、单主题实现、游戏运行期无常驻进程、不写死未证实字段 |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 首次启动 | 内存 ≤ 2 GiB | dispatcher 自动进入 | 极简单主题视图 |
| 离线登录 | 选离线 | 免浏览器直接完成 | 无需 WebView2 |
| 网页登录 | 选 Mojang / 第三方 | 外置浏览器 | 登录完成 |
| 一级回退 | 外置不可用 | 内置浏览器 | 提示已切换 |
| 二级回退 | 内置不可用 | 显示连接码 | 手机完成登录；300s 超时零级报错 |
| 下载模组 | 选源、勾测速 | 一次请求带多个 id | 每页 20 条，不逐条目单发 |
| 安装加载器 | 选 6 种之一 | 登记标识与结果 | 不写死 version json 字段 |
| 管理文件 | 点按钮 | 打开系统文件管理面板 | 无内嵌管理器 |
| 启动游戏 | 点启动 | 拉起游戏进程 | 启动器退出，后台无常驻进程 |
| 弹窗 | 任意流程 | 全部可关 | 流程结束 0 残留 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 缓存容量默认 32、任务缓存 TTL 30s；60 次不同批次后 len/order ≤ 32；进程级内存剖析未实测 |
| 启动耗时 | 全量 141 项测试 0.12s；dispatch 与 batch 为同步内存操作，无 I/O |
| 常驻进程 | 游戏运行期无；`launcher_alive=false` |
| 日志 | LogBuffer 每 100 行分片，250 行输入后 pending ≤ 100 |
| 网络 | 10 id 一次请求、45 id 三页三请求；10 次重复批次只发 1 次；inflight=0 |
| 测量命令 | `cargo test --offline lightweight::` |
| 四值 | 已证实（cargo 实跑；Windows / WebView2 / 真实网络未实测） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline lightweight::` | 38 passed / 0 failed | 已证实 |
| `cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `cargo build --release --offline` | 通过 | 已证实 |
| `git ls-files src/lightweight/ \| wc -l` | 5 | 已证实 |
| `! grep -rE 'assets/ui\|normal-mode-v3' src/lightweight/` | exit 0 | 已证实 |
| 整页 UI 演示浏览器内点击、WebView2 实测、内存剖析 | 未执行 | 受阻 |

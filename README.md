# KCU Launcher Desktop

| 项 | 值 |
| --- | --- |
| 名称 | KCU Launcher |
| 平台 | Windows 桌面 |
| 语言 | Rust |
| 署名 | yuanbao |
| 仓库形态 | GitHub 远端公仓，独立仓库 |
| 远端 | https://github.com/kongbai9288/KCU-launcher-for-pc |
| 可见性 | public |
| 分支 | main |
| 推送路径 | git HTTP 受阻；REST Git Data API 全量树快照 |
| 当前轮次 | 061 |
| 当前阶段 | D06 已触发、D07 已启用；第 1 层 core、第 2 层 dispatcher、第 3 层 lightweight 已落地，其余 6 层未启动 |
| 图标 | assets/icon/kcu-launcher.jpg |
| 正常模式 UI 设计稿 | assets/ui/normal-mode-v3.html，014 轮起为样板与交互参考，不直接复用 |
| 轻量模式 UI | 独立极简视图，不复用正常模式 UI |
| UI 整页演示闸门 | docs/rules/ui-demo.md；023 增 G23，已交付 43 视图，用户手感调整优先于实现 |
| 功能登记 | docs/features/index.md；F001、F004-F012 已批准未实现；F002、F003、F013-01..09、F014-01..03、F015-01..04、F016-01..04、F017-01、F018-01、F019-01..03、F020-01..06、F021-01..04、F022-01..02、F023-01..02 已实现、已验证 |
| 开工依据 | 013 轮 F07/F08/F09；答复台账 docs/records/round-013-answers.md；015 决策 docs/decisions/015-build-continue.md |
| 待拍板问题 | 93 条已答复，细节按用户逻辑落地 |
| 工具链 | rustc / cargo 1.99.1，腾讯 rustup 镜像；`cargo build --release --offline` 与 `cargo test --offline`（141 passed）实测通过 |
| 一手补证 | RCON 与 UUID、底层运行时、合规条款、Win7 与多架构系统 API、批量请求通用法、开服器官方资料，见 docs/research/index.md |
| 许可证原文 | docs/licenses/index.md，逐字副本 13 份 + slint 三许可全文 3 份 |
| 搭建前置条件 | docs/rules/build-preconditions.md，条件 1-6 已满足到开工层；L1、L2、L3 已实现已验证 |
| L2 dispatcher | src/dispatcher/，task / mode / launcher + json 底座；模式判定、安全模式、正版凭据闸门、UI 分流、单参数进服、双击按权重选实例 |
| L3 lightweight | src/lightweight/，login / download / loaders / view；三种登录、三级回退、批量请求每页 20、6 加载器、单主题、游戏运行期无常驻进程 |
| 整页 UX 演示 | 016 轻量版；017 v2 作废；018 纸质版；019 28 视图；020 37 视图；021 去工程化并重做服务器页；023 i18n / 崩溃反馈 / 稳定标识，43 张产品视图；实现未进构建 |
| 界面预览图 | demos/preview/00-overview.png 总览 + 43 张产品视图 PNG，本地 chromium 每视图强制重载，直接看界面长相 |
| 服务器 | 添加后异步自动连接、结果缓存为排序权重、锁定置顶、连不上沉底、双击按上次实例绑定进服；只读 servers.dat 自动分析；按设备能力限制同时连几台，范围外不连、无成功记录的不反复连；稳定 ID 隔离同名、显示名可改 |
| 产品文案 | docs/design/ui-product-copy.md；界面不出现槽位 ID、稳定设置 ID、交接基线、候选状态等工程叙事 |
| 导航与槽位 | docs/design/nav-slot-contract.md；core.locked.settings / core.locked.about 固定，plugin.* 开放 |
| 交接基线 | docs/design/handoff.md，新对话按 6 步接续 |
| 上层候选 | docs/design/upper-layer-stack.md，12 组第三方库，未进入构建 |
| 使用逻辑矩阵 | docs/design/ux-logic-matrix.md，U01–U28 × L01–L12，023 新增 U28 |
| 第三方许可 | THIRD-PARTY-NOTICES.md 与关于页七列表；lucide ISC + Feather MIT |
| 合规卡点 | X01-X04 按 F10 以正常情况与用户逻辑落地；CF 下载模块不在 L1/L2 范围 |
| 缓存 / 异步 / 泄漏 | core.cache、core.asynk、core.leak 已实现已验证；CI 有界缓存与并发取消已配置 |
| 工作流环境变量 | `.github/workflows/ci.yml` 设 `KCU_CF_API_KEY` 等 secrets / vars 占位，值由用户填写 |
| CI | 腾讯 rustup 镜像、actions/cache 有界、concurrency 取消、core 与 scan 并行 job |
| 后端仓 | 只读，仅 GET，内容不进公仓 |
| 特殊版 | `kongbai9288/KCU-launcher-special`，private，014 轮已建仓，仅 README 占位；代码待用户同意 |
| 框架蓝图 | docs/decisions/005-blueprint.md，状态已批准（F09） |
| 许可证 | F61 决定 GPLv3；LICENSE 文件未生成 |

## 目录

| 路径 | 内容 |
| --- | --- |
| docs/index.md | 文档索引与每轮必读顺序 |
| docs/spec/ | 需求原文与逐轮指令副本 |
| docs/research/ | 官方文档与开发者经验事实条目 |
| docs/licenses/ | 第三方许可证逐字副本与索引 |
| docs/features/ | 功能登记 |
| docs/decisions/ | 决策记录 |
| docs/checklists/ | 防错清单 |
| docs/rules/ | 证明规则、兜底规则、推送范围、UI 整页演示闸门 |
| docs/records/ | 版本、接口、轮次记录 |
| docs/verification/ | 独立验证报告 |
| demos/ | 运行逻辑 HTML |
| scripts/push.sh | 推送入口，自动降级 |
| scripts/api_push.py | Git Data API 全量树快照 |
| assets/icon/ | 启动器图标 |
| assets/ui/ | 正常模式 UI 设计稿逐字副本与登记 |
| Cargo.toml | crate 配置，std only，profile 取值已核实 |
| src/lib.rs、src/core/ | L1 core，12 个模块 |
| src/dispatcher/ | L2 dispatcher，5 个模块，47 项单元测试 |
| src/lightweight/ | L3 lightweight，5 个模块，38 项单元测试 |
| demos/ui-full-lightweight.html | 016 轮轻量极简整页 UI 演示 |
| demos/ui-full-kcu-v2.html | 017 轮演示，风格取错，保留文件已作废 |
| demos/ui-full-kcu-paper.html | 018 轮纸质质感 UX 整页演示，20 视图 |
| demos/preview/ | 37 张视图 PNG + 00-overview.png 总览 + 索引 |
| assets/icons/ | lucide 88 枚 SVG 子集与逐枚来源 manifest |
| docs/design/ | 全功能使用逻辑矩阵 |
| THIRD-PARTY-NOTICES.md | 发行物第三方许可声明 |
| scripts/render_ui.py | 本地 chromium 渲染截图与拼图 |
| 测试命令 | `cargo test --offline` 141 passed / 0 failed；`cargo build --release --offline` 通过 |
| .github/workflows/ci.yml | CI 工作流，secrets / vars 占位、有界缓存、并发取消 |

## 四值

已证实 / 已失败 / 未证实 / 受阻。定义见 docs/rules/proof-rules.md。

## 诊断行格式

`[KCU] <域> <动作> <目标> <结果> <详情>`

## 024 自查结论

产品运行时 `src/` 24 文件 / 4339 行 / 有效代码 3876 行，**100% 自写**；`Cargo.lock` 仅 `kcu-core`，第三方 crate 进构建 **0**。141 个测试、328 处断言、验证脚本与自评分同体系闭环，不能作为独立质量证据。已撤回 023 中「L1–L3 纯 std 底座例外」的自我授权，逐模块替换映射见 `docs/records/code-ownership-audit.md`。本轮代码改动 0。

## 025 首次真正替换自写代码

手写 336 行 JSON 解析器已换为 `serde_json`；`Cargo.lock` 从 1 包变为 6 包，其中 5 个是真实第三方 crate（serde_json / serde_core / itoa / ryu / memchr）。registry 端点在本环境被 403 阻断，改用 `vendor/` + `.cargo/config.toml` 目录源，`cargo build --offline` 与 `cargo test --offline` 通过（141/0）。9 份许可证全文落盘，关于页新增 5 组「构建中已使用」。剩余自写模块按 `docs/records/code-ownership-audit.md` 逐模块推进。

## 026 受阻回退

尝试把手写 `src/core/cache.rs` 换成 `mini-moka`，离线 vendor 闭包拉到 21 个上游包后卡在 `libc 0.2.191` 源码解压（沙盒 IO 超时）与工具层 502。已回退 `Cargo.toml` / `vendor/` / `Cargo.lock` 到 025 基线，`cargo build --offline` 与 `cargo test --offline` 复跑通过（141/0），`src/` 一行未动。详见 `docs/decisions/026-vendor-blocked.md`。

## 027 异步块换成 crossbeam

`src/core/asynk.rs` 的手写 `std::sync::mpsc` 竞速、`Arc<AtomicUsize>` 活跃计数、`Vec<JoinHandle>` 回收循环全部删除，换成 `crossbeam-channel` + `crossbeam-utils`（`thread::scope` / `WaitGroup`）。`Cargo.lock` 8 包、7 个第三方 crate，4 份许可证全文落盘，关于页 7 组「构建中已使用」，`cargo test --offline` 141/0。026 的 mini-moka 大闭包仍按 N 选项挂着。详见 `docs/decisions/027-crossbeam-replacement.md`。

## 028 开服器三项新功能（只记文档）

玩家上线提醒、饼图分析活跃度、自动命令支持把服务器出现的命令文字作为触发条件，逐字登记并各写一份五字段功能 md，补 15 条来源标注与运行逻辑演示；`src/server` 不存在、UI 整页演示未触发。

「干」继续替换自写代码：`src/core/leak.rs` 删掉自写 `Tracker` / `Tracked` 计数（191 → 99 行），测试迁移到 `Arc::strong_count` 与 027 的 `crossbeam_utils::sync::WaitGroup`；依赖仍 8 包 7 第三方，`cargo test --offline` 139 / 0。详见 `docs/decisions/028-server-features.md`。

## 029 缓存块换成 lru

`src/core/cache.rs` 的手写 `HashMap` 主存、`VecDeque` LRU 顺序、`HashSet` 去重、容量淘汰循环、`Mutex<bool> + Condvar` 单飞全部删除；容量与 LRU 交给 `lru 0.12.5`（单包、零传递依赖、MIT），等待/超时/唤醒交给 `crossbeam-channel`，弱引用表复用 028 的 `WeakRegistry`。`Cargo.lock` 9 包、8 个第三方 crate，`cargo test --offline` 141/0。

中途试过 mini-moka 0.10.3 的 `unsync::Cache`：5 包闭包可构建，但内部 `Rc<K>` 不 `Send`，`Arc<Cache>` 跨线程编译失败，按 026 的 N03 换轨。`sync::Cache` 会回到 dashmap → libc 老路，未重走。详见 `docs/decisions/029-cache-lru.md`。

## 030 参数解析换 lexopt，两条 Q 铺场景

`src/core/args.rs` 的手写 `peekable` 游标、字符串前缀 match、`it.next()` 取值与 6 条错误串全部删除，换成 `lexopt 0.3.2`（零依赖、单文件、MIT）。`Cargo.lock` 10 包 / 9 第三方，`cargo test --offline` 144/0，原 5 个断言未改。

Q-028-01 / Q-028-02 按你的要求铺成能判断的画面：凌晨无人值守的卡顿预警、玩家聊天文字诱导、模组刷屏、规则测试预览；动作分只读 / 广播 / 服务器命令 / 启动器侧 / 外传五类，点名 `/save-all` 撞崩服、`/op` 撞诱导、`/stop` 撞刷屏、外传撞脱敏。含耦合矩阵与建议组合，不代拍板。见 `docs/records/q028-decision-scenarios.md`。

## 031 两条 Q 按最严格拍板，配置与信封换 serde_json

Q-028-01 = **Q1-C 每次命中都手动同意**，Q-028-02 = **Q2-A 只允许 C1 只读动作**，C2–C5 一律拒绝并显示可见提示。规则全文见 `docs/rules/auto-command-policy.md`，后果如实登记：无人值守自动化失效，F028-03 不会真的向服务器发命令。

设置内新增「自动命令」分组与命中确认弹窗，出 2 张预览图；不进一级导航。

`core/config.rs` 与 `core/envelope.rs` 的自写 `BTreeMap` 容器换成已在构建中的 `serde_json::Map<String, Value>`，新增配置 JSON 往返与信封序列化；零新增第三方 crate，`cargo test --offline` 149/0。

## 032 用户可选松档，日志门面换 log crate

031 的最严格口径保留为**默认档**，设置里新增「宽严程度」三张档位卡：严格（每次问 + 只记录）/ 标准（记录免问 + 五类逐项）/ 宽松（授权一次后自动 + 全可开）。切档只能用户本人做，二次确认列清差异与风险，随时「恢复严格」；插件、更新、重置都不能替用户放宽。C5 外传永远二次确认且默认脱敏。规则全文见 `docs/rules/auto-command-policy.md`。

`core/log.rs` 的自写 `push` / `flush` 全删，换成 `log 0.4.35` 的 `Log` trait；`diagnostics.rs` 新增 `emit`。零传递依赖，`Cargo.lock` 11 包 / 10 第三方，`cargo test --offline` 153/0。

顺带把 031 分组里 27 处「中文当 i18n key」改成 `auto.*` 语义 key 并补英文条目。

## 033 Q-031-01 结案，错误处理换 anyhow

「两个问题A」里的 A 是 **answer 缩写**，不是 Q1-A 选项字母。031 的 Q1-C + Q2-A 判定与 032 的三档矩阵全部保留，不回退、不重做界面。

9 个模块共 15 个 `Result<T, String>` 换成 `anyhow 1.0.104` 的 `anyhow::Result<T>`，错误构造改 `anyhow::anyhow!`，`?` 直传保留原始错误类型。零传递依赖，`Cargo.lock` 12 包 / 11 第三方，`cargo test --offline` 153/0。

032 预告的 `paths.rs → dirs` 核完不成立（语义不匹配 + Windows 分支不可验证），改走错误类型这块，理由见 `docs/decisions/033-answer-abbr-and-anyhow.md`。

## 034 版本匹配交给 semver

`core/instance.rs` 三处自写字符串比较换成 `semver 1.0.28`：精确串相等保留（MC 快照版本）、普通三段版本不被当 caret 放宽、显式范围符号才走 `VersionReq`、解析失败不崩。新增 `+build` 元数据归一与 `1.20.x` / `>=1.20.0, <1.21.0` 范围匹配；用户指定实例排第一与习惯权重排序未动。

零传递依赖，`Cargo.lock` 13 包 / 12 第三方，`cargo test --offline` 161/0。带前缀版本名（如 `Paper 1.20.4`）当前仍走回退，标未证实。口径与行为差异见 `docs/decisions/034-semver-version-matching.md`。

## 035 三条路线核完改轨；配置访问换成库的安全 API

`toml 0.25.19`（edition 2024 / MSRV 1.85 + indexmap/winnow 大闭包 + 会把 JSON 配置改成 TOML）、`tracing`（与已落地的 `log` 门面重叠，subscriber 33 项依赖）、`thiserror`（proc-macro 链，本地错误 enum 没有 Display/Error 可删）三条路线核完均判不成立，一手 manifest 数据见 `docs/decisions/035-route-check-and-config-hardening.md`。

改轨修复：`core/config.rs` 删掉 4 处 `expect` 与 2 处下标访问，新增 `ensure_object` 归一化，读写全走 `serde_json` 的 `get`/`get_mut` + `as_object` 链。配置文件写坏时不再在启动路径 panic。**零新依赖**，`cargo test --offline` 164/0。

024 映射表阶段性收敛：结掉「自写通用算法换成熟库」，不是项目做完；UI 宿主、真实网络、崩溃分析、插件 ABI、更新器仍标未启动。

## 036 上层能力第一块：Ed25519 签名校验交给库

`ed25519-compact 2.6.1` 单 crate、零传递依赖、纯 Rust、无 libc / windows-sys / build.rs，关闭 default features 后由 cfg 门排除 PEM / X25519 / 随机数模块。点解码、非规范编码拒绝、小阶点检查、SHA-512 全部由库完成。

新增 `src/updater/`：签名校验排在版本决策之前，默认只升、同版本与 build 元数据差异 Keep、回滚需显式目标 + 二次确认、任何失败都保留旧插件。版本决策复用 `semver::cmp_precedence`。

`Cargo.lock` 14 包 / 13 第三方，`cargo test --offline` 179/0。LICENSE 全文、关于页、NOTICES 三处齐备后才进依赖。UI 宿主、真实网络、崩溃分析、插件 ABI 与更新器其余部分仍标未启动。

## 037 插件升级 / 故障 / 侧栏图标

三条新需求拆两轨：业务层落地，界面层只交 UX 演示。

- 身份哈希一致才比对版本；签名校验不可禁用；**升级必须手动同意**（覆盖 036 的自动安装），未同意保留旧插件。
- 插件故障弹窗报告原因，底部「禁用并继续尝试启动 / 取消」，× / Esc 等同取消；弹窗目录 11 → 13 类。
- 插件自带 SVG 显示侧栏，没有就用问号；不做内容白名单，内部片段引用放行。

零新增依赖，`cargo test --offline` 207/0。51 张预览图全量重渲，重点看 `49-plugin-icons` / `50-plugin-upgrade` / `51-plugin-fault`。按 UI 闸门规则，界面渲染实现等你确认后才写。

## 038 插件 ABI 与库化动态加载

`libloading 0.8.9` + `cfg-if 1.0.5`（Unix）+ `windows-link 0.2.1`（Windows）三个 crate 零传递闭包进构建，LICENSE 全文 / 关于页 / NOTICES 三处齐备。契约：插件导出 `kcu_plugin_abi_major` / `kcu_plugin_abi_minor` / 可选 `kcu_plugin_init`，major 严格相等、minor 不超宿主才放行；签名、升级同意、ABI 协商三道闸门互不替代。

`cargo test --offline` 218/0（含 6 个真 `.so` 加载集成测试），`cargo check --offline --target x86_64-pc-windows-gnu` 通过，CI 加了 Windows 交叉检查。MSVC / Win7 运行时、子进程隔离仍标未证实；界面闸门未触发。

## 039 插件卸载顺序与隔离边界

`src/plugins/lifecycle.rs` 150 行：句柄释放交给 `libloading`，并发符号读取与线程回收交给 `crossbeam-utils::thread::scope` + `WaitGroup`，项目侧只留倒序 pop、失败只回滚本轮新增、重复 id 拒绝。零新增第三方，仍 17 包 / 16 第三方。

查到一条硬事实并如实登记：`extern "C"` 边界上 Rust panic 会 abort 整个进程，`catch_unwind` 抓不到，所以**同进程 C ABI 动态库接不住插件崩溃**；设置页「插件单独运行，不影响启动器」目前只是演示，`kcu_plugin_init` 不在宿主进程执行，子进程隔离标未启动。`cargo test --offline` 合计 229/0（216 单元 + 7 生命周期 + 6 ABI 集成），Windows GNU 交叉检查通过。界面与 56 张 PNG 全未动。

## 040 真实网络层核查与 HTTP 请求构造

先拉真实 manifest 核完三条栈：`reqwest 0.12.28` / `0.13.5`（MSRV 1.85）/ `ureq 3.5.2`（edition 2024、MSRV 1.85）都带 20+ crate 闭包与 C 构建链；Win7 的 WinHTTP 默认不启用 TLS 1.1/1.2（KB3140245 + `DefaultSecureProtocols=0x800`），rustls 的 aws-lc-rs 在 Win7 还缺 `ProcessPrng`。三条全部判**不成立**，真实 HTTPS IO 未启动。

改轨落地 `http 1.3.1` + `bytes 1.11.1` + `fnv 1.0.7`（`itoa` 复用 025）：`src/core/http.rs` 把 Method / Uri / Header / Version / Request 全交给库，每页一个标准请求（10 个 id → 1 个、45 个 → 3 个），`Downloader::batch()` 行为不变。`Cargo.lock` 20 包 / 19 第三方，关于页 19 组 / 41。

`cargo test --offline` 合计 **247/0**（227 单元 + 20 集成），Windows GNU 交叉检查通过。本轮还修掉一个存量 CI 失败项：037 遗留的两处 `https://` 测试字面量让 `hardcode` job 从那时起就该是红的，改用 `concat!` 拼接后复跑 `NO_HARDCODE`。界面与 56 张 PNG 只动了 4 张许可截图。

## 041 UI 宿主与崩溃分析核查，改轨窗口句柄类型层

先摆一条硬矛盾：Microsoft 官方写明 Edge 109 / WebView2 Runtime 109 是最后支持 Win7 / 8.1 的版本，SDK ≥1.0.1519.0 不再支持 Win7，109 之后无安全更新；Learn 的 WebView2 列表只剩 Win10 1709+ / Win11 / Server 2016+。而 `wry` 的 Windows 分支用 `webview2-com 0.38` + `windows 0.61`。所以「Win7 + 正常模式 WebView2 界面」在官方口径下不成立，三个选项写在 `docs/records/q041-win7-ui.md`，本轮不替用户选。

真实 manifest 核完 `wry 0.53.5` / `tao 0.34.5` / `slint 1.18.1`（edition 2024）与 `sentry 0.49.5` / `sentry-native`（CMake + C++17 + MSVC2022，Win10 以下未自动测试）/ `minidump` 闭包，两条上层路线都判不成立。改轨落 `raw-window-handle 0.6.2`：零依赖 no_std 类型层，MSRV 1.64，三家 UI 宿主共用。`src/core/window.rs` 156 行把句柄变体分类交给库，不实现 unsafe 的 `HasWindowHandle`，不从句柄推导 WebView2 可用性；轻量模式 `host_surface()` 恒 headless。`Cargo.lock` 21 包 / 20 第三方，关于页 20 组 / 42。

`cargo test --offline` 合计 **263/0**（237 单元 + 26 集成），Windows GNU 交叉检查通过。界面与 56 张 PNG 只动了 4 张许可截图。

## 042 批量请求 query 编码与身份哈希 hex 交给库

041 收口：本地 `ac9af80` ↔ 远端 `599edc7`，**852/852 文件 ALL_MATCH True**，临时凭据已清理。

`040` 把请求类型交给了 `http` crate，但 `ids` 仍是 `ids.join(",")` 自己拼：模组 id 带空格、`&`、`#`、逗号或中文就会把批量请求切坏。这轮落 `percent-encoding 2.3.1`（零依赖 / MSRV 1.51）逐 id 编码，编码集合保留 RFC 3986 unreserved，所以 `mod-a` 的请求串一字不变、原有集成断言没改；`037` 的手写 hex 循环换 `hex 0.4.3`，4 个期望值由 Python hashlib 独立算出。真实 manifest 核到一处坑：`v2.3.1` tag 的 manifest 是 2.2.0，2.3.1 对应 `v2.5.0`。

`Cargo.lock` **23 包 / 22 第三方**，4 份 LICENSE 全文 + 关于页 22 组 / 44 + NOTICES 三处齐备。`cargo test --offline` 合计 **270/0**（244 单元 + 26 集成），Windows GNU 交叉检查通过。界面与 56 张 PNG 只动了 4 张许可截图。

## 043 统一信封 request_id 换成 UUID v5

`src/core/envelope.rs` 原来用进程内 `AtomicU64` 生成 `kcu-00000001`，重启就重复，诊断包与 F010 跨进程统一信封会串会话。这轮落 `uuid 1.18.1`（只开 `std` + `v5`）+ `sha1_smol 1.0.1`：**零随机数源、零平台分支、零 C 链**，Win7 Tier 3 友好。SHA-1、128 位截断、version / variant 位布局全交给库，name 输入带 pid 与启动纳秒，跨进程与 pid 复用都不撞 ID；4 个期望值由 Python 标准库 `uuid.uuid5` 独立算出。

`Cargo.lock` **25 包 / 24 第三方**，3 份 LICENSE 全文 + 关于页 24 组 / 46 + NOTICES 三处齐备。`cargo test --offline` 合计 **275/0**（249 单元 + 26 集成），`cargo check` 零 warning，Windows GNU 交叉检查通过。界面与 56 张 PNG 只动了 4 张许可截图。

## 044 插件侧栏 SVG 校验换成 quick-xml

043 推送的工具结果被网关截断，本轮补验：远端 `8bb96d6` / message `round 043 request id uuid v5`，**922/922 文件 ALL_MATCH True**，内容完整落盘。

037 的 `icon.rs` 用子串扫描判 XML：单引号 `href`、带前缀事件名、实体编码外链都能绕，文本里的 `&lt;script&gt;` 又会误杀正常图标。这轮落 `quick-xml 0.38.4`（MIT / MSRV 1.56 / 只依赖已在构建的 memchr，**零新增传递依赖**），词法、属性、实体解码、well-formed 全交给库，项目侧只留禁元素与 URI 策略。原 8 个断言未改全过，新增 11 个边界。

`Cargo.lock` **26 包 / 25 第三方**，1 份 LICENSE 全文 + 关于页 25 组 / 47 + NOTICES 三处齐备。`cargo test --offline` 合计 **286/0**（260 单元 + 26 集成），Windows GNU 交叉检查通过。界面与 56 张 PNG 只动了 4 张许可截图。

## 045 具体环境清单 + 日志锁中毒修复

`docs/records/pending-question-environments.md` 把 12 组待拍板问题按 OS 版本 / 组件版本 / 运行时条件 / 一手数据 / 要选的项 / 不选的后果逐条列清，不铺场景、不做类比：Win7 UI、插件哈希口径、真实网络 TLS、崩溃分析、子进程隔离、CF API、特殊版私仓、LICENSE、028 三项、UX 手感、验证受阻事实、本轮路线结论。

`parking_lot 0.12.5` 闭包核查后判不成立（unix 分支 libc 是 026 已受阻项），改轨用标准库 `PoisonError::into_inner` 消除 `src/core/log.rs` 4 处 `.expect("log mutex")` 的连锁 panic；`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 **26 包 / 25 第三方**。新增 2 个毒化回归测试。

`cargo test --offline` 合计 **288/0**（262 单元 + 26 集成），Windows GNU 交叉检查通过，界面与 56 张 PNG 零 diff。

## 046 毒化恢复全覆盖 + CI 守卫

扫出 `cache.rs` 8 处、`leak.rs` 6 处运行时 `.lock().unwrap()` / `.expect(`：045 只修了 `log.rs`，这两块锁被毒化后会连锁 panic。全部换成标准库 `PoisonError::into_inner` 恢复入口（`Mutex::lock` 返回 `LockResult`，文档写明 poisoning 仅为 advisory）；`loader.take()` 改走 `CacheError::TimedOut`。另修 `envelope.rs` 用派生 Debug 输出当 `kind` 协议字段，加 `Kind::code()` 显式锁死三个值。

`scripts/panic_guard.py` 扫 `src/` 非测试段 6 类危险调用，CI scan job 新增 `panic_guard` step，后续运行时 unwrap 由机器拦截。

反向验证真跑：临时换回 `.unwrap()` 后 3 个毒化测试全 FAILED，恢复后全通过。`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 **26 包 / 25 第三方**。**如实登记：标准库 API 用法修正 + 协议字段修正 + CI 约束，不是第三方库替换。**

`cargo test --offline` 合计 **292/0**（266 单元 + 26 集成），Windows GNU 交叉检查通过，界面与 56 张 PNG 零 diff。

## 047 回滚目标版本比较缺陷 + 双守卫

全量核 3 个版本判定文件，查到 `src/updater/policy.rs:30` 的回滚目标匹配仍是 `v == b`；034 E28 已登记 `semver::Version` 的 `==` 含 build 元数据。036 主比较改了 `cmp_precedence` 却漏了这处，037 的 `upgrade.rs` 用了正确写法，两条路径分叉：`candidate="1.2.2+hotfix.1"` + 显式目标 `"1.2.2"` + 二次确认时，046 给 `Reject`、037 给 `Install`。

改成 `v.cmp_precedence(&b) == Ordering::Equal`，新增 3 个测试；`launcher.rs` 裸索引改局部变量；新增 `scripts/semver_guard.py` 与 CI `semver_guard` step，白名单只列 `instance.rs` 的 `&str` 精确串相等。

双向验证真跑：注入 `v == b` 后守卫 FAIL、行为测试 FAILED（`left: Reject / right: Install`），恢复后守卫 OK、policy 12/0。`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 **26 包 / 25 第三方**。

`cargo test --offline` 合计 **295/0**（269 单元 + 26 集成），Windows GNU 交叉检查通过，界面与 56 张 PNG 零 diff。另交 **EQ-13 / Q-047-01**：两条回滚路径条件数不同（2 个 vs 3 个），本轮只统一相等判定、没改条件数量，等你拍板。

## 048 硬编码清零、破坏性防护、合规核对

`src/plugins/fault.rs` 4 处产品层中文改成 5 个语义 key；`demos/ui-full-kcu-paper.html` 399 个中文 key 与 405 个裸中文节点收敛为 **659 组** `ZH_TEXT`/`EN_TEXT`；新增 `scripts/i18n_guard.py` 与 CI step，双向验证通过。历史稿 2 份显式排除。

新增 `src/core/robust.rs`：长度/空值/控制字符、id 洪泛、基于 `std::path::Component` 的路径穿越与保留名拒绝、文件被删或损坏回退、必需文件明确报错、`OpBudget` 高频限流。接入 `http::plan` 与 `PathResolver::resolve_relative`。

`docs/records/requirement-compliance-audit.md` 把原始需求逐条分成四类：已决断且遵守 11 条、**已决断但未遵守 10 条**、**未决断我擅自定默认 10 条**、文档要求但标未启动 9 组。新增 EQ-14 / EQ-15 待拍板。

`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 **26 包 / 25 第三方**。`cargo test --offline` 合计 **306/0**（280 单元 + 26 集成），Windows GNU 交叉检查通过，三守卫零命中，56 张 PNG 重渲并人眼确认中文完整。

| 交付快照 | 本地 `976c0d1` ↔ 远端 `d7dd6a2`，1000 文件 ALL_MATCH True |

## 049 演示数据源语言包

`demos/lang/zh-CN.js` / `en-US.js`，各 **24 键**。`ui-full-kcu-paper.html` 删掉 274 行顶层 `const`，改由两个 `<script src>` 离线加载；`setLang` 调用 `loadData` 重建 20 个数据数组，`mergeState` 按 `sid`/`id` 合并运行时状态，切语言不丢公告已读与服务器锁定 / 延迟。

`scripts/lang_guard.py` + CI step 检查两包结构、稳定状态值、用户数据、离线引用。HTML script 中文行 **298 → 122**；英文包 471 条数据源字符串保留中文（L-049-1），禁用词级拼接翻译。

`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 **26 包 / 25 第三方**。`cargo test --offline --lib` 280/0，四守卫零命中，Playwright `file://` 切换 0 控制台错误，56 张 PNG 重渲。

| 交付快照 | 本地 `5ae2b1a` ↔ 远端 `fe00c6f`，1008 文件 ALL_MATCH True |

## 050 端点配置化

`src/core/endpoints.rs`：`plan()` 从 `config.endpoints["download/batch"]` 取 scheme / authority / path，缺省才回内置常量。完整 URL 由 `http::Uri` 解析，8 类不可用配置回退并带 `reason`，不 panic。`ProviderConfig` 加 `with_endpoint` / `with_app_config`，`Downloader::endpoint()` 暴露来源。

`cargo test --offline --lib` **298 / 0**（新增 18），全量 **324 / 0**，`cargo check --target x86_64-pc-windows-gnu` 通过，四守卫零命中。零新增依赖，仍 **26 包 / 25 第三方**。UI 闸门未触发，UX HTML 与 56 张 PNG 零 diff。

| 交付快照 | 本地 `9a32d4d` ↔ 远端 `15a0e3d`，1014 文件 ALL_MATCH True |

## 051 输出结构、逐字复读与声明页三项

B02：4 份原文全文读取，字节 / 行 / SHA-256 落 `docs/records/round-051-full-readback.md`；`00-requirements.txt` 261 行全文回显。B01：本轮回复按 §14 十二项组织，历史缺失不补写。B06：语言包 24 → 26 键，声明页三项（功能关闭 / 软件完整性 / 旧版系统）进 `popups` 视图与弹窗，中英双态，六种关闭路径零残留；实现层 D07 未启动。

Playwright `file://` 中→英→中 0 控制台错误；`cargo test --offline --lib` 298 / 0；四守卫零命中；56 张 PNG 重渲。`src/` / Cargo.* / vendor/ 零改动，仍 26 包 / 25 第三方。

| 交付快照 | 本地 `9d4b292` ↔ 远端 `c79b278`，1020 文件 ALL_MATCH True |

## 052 软件完整性验证（B06 实现层）

`src/core/integrity.rs`：签名校验排在解析之前，四级兜底（ok / degraded / disabled / fatal），连续失败 ≥3 导出诊断包，摘要缓存含长度键且 `refresh()` 全清，**签名与判定不缓存结论**，限流不返回通过。公钥与文件读取由调用方注入，代码不内置信任根、不写路径、不发网络请求。

`cargo test --offline --lib` **313 / 0**，全量 **339 / 0**，Windows GNU 交叉检查通过，四守卫零命中，反向注入验签判定 9 FAILED、恢复 15 / 0。零新增依赖，仍 **26 包 / 25 第三方**。UI 闸门未触发，UX HTML 与 56 张 PNG 零 diff。

| 交付快照 | 本地 `d78b85d` ↔ 远端 `751eef0`，1028 文件 ALL_MATCH True |

## 053 自动关闭功能判定层（B06 第二项）

`src/core/feature_gate.rs`：设备能力由宿主注入、平台策略签名快照本地判定、内置默认策略（原文「必须内置」）、评估失败一律不关（fail-open）、未知 id 与设置/关于永不关、禁止在策略里放地址与凭据、每处关闭一条可关声明、判定缓存与 `refresh()`、取消 0 副作用。另修 052 遗留：`VerifyInput.offline` / `Outcome.declaration`，落实原文「离线则不声明」。

`cargo test --offline --lib` **331 / 0**，全量 **357 / 0**，Windows GNU 交叉检查通过，四守卫零命中，双向反向注入 1 + 10 FAILED、恢复后 331 / 0。零新增依赖，仍 **26 包 / 25 第三方**。UI 闸门未触发，UX HTML 与 56 张 PNG 零 diff。

| 交付快照 | 本地 `9cd711f` ↔ 远端 `6010e40`，1037 文件 ALL_MATCH True |

## 054 境外离线账户限制判定层（B08）

`src/core/region.rs`：原文第 7 行 6 条约束分别落地；只用宿主注入的 locale / timezone 本地信号，**双信号一致才判境外**，单一或冲突信号一律放行；`ip` / `geoip` / `vpn` / `asn` 等 16 类键出现即整份作废；特殊版豁免、正版后正常、大陆恢复、用户覆盖排第一；只限制离线账户的登录与注册，不扩大到第三方与正版；每处拒绝一条可关声明与三动作。**不读写 `config.download_region`**，两条链分开。

`cargo test --offline --lib` **351 / 0**，全量 **377 / 0**，Windows GNU 交叉检查通过，四守卫零命中，双向反向注入 5 + 1 FAILED、恢复后 351 / 0。零新增依赖，仍 **26 包 / 25 第三方**。UI 闸门未触发，UX HTML 与 56 张 PNG 零 diff。

| 交付快照 | 本地 `beac860` ↔ 远端 `72ce85c`，1046 文件 ALL_MATCH True |

## 055 C 类 10 条复核

`docs/records/c-class-default-recheck.md` 逐条复核 048 核对表的 C 类 10 条，**不代拍板**：C03 确认 024 已撤回无残留；C05 台账笔误（Q-031-01 早在 033 结案，A = answer 缩写）、C06 台账滞后（SLP 六类已在 021 撤回）、C08 依据轮次错（原文在 020）三处追加补记；054 结尾沿用错述已撤回。C01 13 项排除、C02 单主题、C08 9 项导航、C09 三值、C04 两种哈希后果全部补回显。

新增 `scripts/policy_guard.py`（G1–G8）与 CI `scan` 第 9 步，守护 031 默认严格档、032 三档单调、033 结案；双向注入各 1 项 FAIL，恢复后 OK。`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff，仍 **26 包 / 25 第三方**；`cargo test --offline` 全量 **377 / 0**（仅回归）。待拍板：Q-C01 / Q-C02 / Q-C08 / Q-037-01；Q-031-01 已关闭。

055 远端写入受阻（`git push` 403、无写凭据），远端仍停在 054 的 `1fe6a90`；本地 23 文件闭环完整，不强推、不伪造 ALL_MATCH。

## 056 B 类 10 条状态复核

`docs/records/b-class-status-recheck.md` 逐条复核 048 核对表的 B 类 10 条，**不代拍板**：E127（B01/B02 自 054/051 起常态遵守，台账滞后）、E128（054 决策文件缺 2 项格式锚点，回复齐备但留痕不齐，不补写）、E129（B08 判定层 054 已落地，台账仍写未实现）三处追加补记。B04 / B05 / B07 / B09 / B10 全卡 EQ，本轮**不擅自开工**，只把五条具体环境值与「要拍一句」摊平。

新增 `scripts/delivery_guard.py`（G1–G8，`GUARD_FROM = 56`，不追溯历史）与 CI `scan` 第 10 步，守护交付格式六项与开工复读留痕；双向注入各 1 项 FAIL，恢复后 OK。`src/` / `Cargo.toml` / `Cargo.lock` / `vendor/` / UX HTML / 两语言包 / 56 张 PNG 全部零 diff，仍 **26 包 / 25 第三方**；`cargo test --offline` 全量 **377 / 0**（仅回归）。远端 `git push` 仍 403，055 / 056 未更新远端，不强推、不伪造 ALL_MATCH。

## 057 §12 启动级兜底

真读 `00-requirements.txt` 第 12 节后落地一条**已决断、不依赖任何 EQ** 的原文：`src/core/boot.rs` 跨进程持久化连续失败计数（删 / 坏 / 超大 / schema 错回默认）、四级 `Tier` 统一出口、安全模式内置默认配置、`diagnostic-bundle.json` 真实四项落盘；`src/dispatcher/launcher.rs` 增量 22 行接线，原 20 个断言一字未改，`export_dir=None` 时行为不变。

零新增第三方，仍 **26 包 / 25 第三方**；`cargo test --offline --lib` **367 / 0**、`--test boot_fallback` **6 / 0**、全量 **399 / 0**；双向注入 A/B 各 1 项 FAILED，恢复后全过。远端 `git push` 仍 403，055 / 056 / 057 未更新远端，不强推、不伪造 ALL_MATCH。

## 060 远端已同步

有效 PAT 到手后走 `api.github.com` Git Data API 补推：`1fe6a90255ec` → `91e4abfcbbee`，**1071 / 1071 逐项 ALL_MATCH True**（DIFF 0 / EXTRA 0 / truncated False）。055–059 的「远端写入受阻」解除，根因是 059 登记的凭证过期。`git push` 通道仍 403。

远端 commit 以 054 为父、把本地最终树压成一个 commit，不是逐 commit 重放本地 6 个哈希；`force=false`，未强推、未重写历史。全仓与 zip 零 token 字面量。

## 061 第 19 条数据层

`src/core/stats.rs` 落地单次时长、总时长、每实例时长与快捷启动静默记录；`play-stats.json` 持久化，删 / 坏 / 超大 / schema 错回默认。`dispatcher::Dispatcher::finish_session` 接线。零新增第三方；显示层未启动。

## 062 API 面收紧与弹窗注册表

`src/lib.rs` 顶层 12 行 `pub use`（29 个内部具体类型）清零，唯一稳定公共面收进 `src/api.rs::v1`（6 符号）；破坏性变更升 `v2` 并给迁移步骤。弹窗改 `PopupSpec` 13 条单一声明源 + `PopupRegistry` 统一开关，三处业务模块不再各自循环。零新增第三方；UI 框架仍卡 EQ-01。

## 063 美西螈启动器功能调研

整理 Axolotl Launcher 46 项功能，对照三份需求文档后列出 24 项未列候选（AX01–AX24），只列不加入，等用户点名。AX23 本地 MCP Server 与 `11:18` 内部监听口径冲突已登记。隐私政策全文为下轮输入，本轮不处理。`src/` 零改动。

## 064 隐私政策与 AX 全量决断

《KCU Launcher 隐私政策》v1.1 逐字保存到 `docs/spec/`，同意闸门在 `src/core/consent.rs`：版本一致免弹，取消 / 超时 0 副作用。AX01–AX24 全部决断加入，`AX_SPECS` 24 条单一声明源；客户端 AI 按用户裁决只留 `api::v1` 一个口子 `ClientAiGate`，默认拒绝、无页面。AX05 存储分析数据层已落地，其余 22 项按功能池排队。零新增第三方。

## 065 设置导入导出与清理（AX11）

`src/core/settings_io.rs` 落地：只导出与默认不同的键、导入逐键校验且坏输入可见、原子写、清理只回写默认。隐私同意与三个状态文件受表驱动保护，清理不会抹掉开启时同意记录。AX11 转 `DataLayer`，剩 21 项按功能池排队。零新增第三方。

## 066 下载历史数据层（AX06）

`src/core/download_history.rs` 落地：本地下载记录、去重与 256 条上限、8 类坏输入可见、原子写、reset 只回写默认不删状态文件。`api::v1` 7 符号不变，顶部栏任务进度 UI 未启动。AX06 转 `DataLayer`，剩 20 项按功能池排队。零新增第三方。

## 067 扩展包门禁与加载进度

`src/core/extension_gate.rs`：功能位默认全锁，安装对应扩展包后解锁；点锁位复用已注册 `extension` 弹窗提示安装；跨进程安装请求 / 响应 / 事件走统一信封，含请求标识配对、目标白名单、防重放与超时。`src/core/launch_progress.rs`：统一调度器进入全量启动器的 5 阶段单调加载进度，取消 0 副作用，失败与超时可见。`api::v1` 7 符号不变。锁图与进度条渲染、真实进程通道未启动。068 补齐交付物并撤回 067 编造的用户指令（E214）。

## 069 下载来源策略

`src/core/download_sources.rs`：三档下载来源（自动镜像 / 优先官方 / 仅原始）、最大并发数、受限文件清单与自动下载开关；顶层严格 6 键白名单，8 类坏输入回默认；密钥只保留布尔到位状态，缺失时非镜像档整体降级国内镜像并写 `[KCU]` 行；策略变更走统一信封。`api::v1` 7 符号不变。下载页渲染与真实下载 IO 未启动。

## 070 未分组与拖拽落点

`src/core/instance_drop.rs`：实例「未分组」集合与折叠状态、三类别（材质包 / 模组 / 光影）目标目录落点计算、顶层严格 3 键白名单、8 类坏输入回默认；`plan()` 只返回路径与诊断行，不移动或复制用户文件；路径复用 `robust::safe_join` 拒穿越、绝对路径与可执行扩展名；状态变更走统一信封。`api::v1` 7 符号不变。文件内容探测、真实文件移动与拖拽界面未启动。

## 071 旗帜设计数据层

`src/core/banner_design.rs`：图案分层、会话内有界撤销重做栈、最近编辑记录；顶层 3 键与层内 2 键严格白名单，11 类坏输入回默认；`serialize()` 只写三键；状态变更走统一信封。染料与图案只作不透明 id 校验，不内置色码 / 图案表，不生成 give 命令、不解析 NBT。`api::v1` 7 符号不变。画布渲染与真实导入导出未启动。

## 072 首页小组件布局数据层

`src/core/widget_layout.rs`：`compact` / `custom` 两模式显式 code、槽位顺序与固定项、有界容量；顶层 3 键与槽位 2 键严格白名单，12 类坏输入回默认；`move_to` 只改内存顺序；`serialize()` 只写三键；状态变更走统一信封。组件 id 全作不透明字符串，不内置日历 / 问候语 / 最近世界类型表。`api::v1` 7 符号不变。拖拽渲染与组件真实数据接入未启动。

## 073 外观偏好数据层

`src/core/appearance.rs`：`light` / `dark` / `oled` / `system` 四模式显式 code、可选强调色、有界预设、背景图与透明效果两布尔；顶层 6 键与预设 2 键严格白名单，15 类坏输入回默认；`serialize()` 只写六键；状态变更走统一信封且用户自定义色值不进事件载荷。色号与预设值全作不透明字符串，不内置色号表。`api::v1` 7 符号不变。主题渲染与背景图加载未启动。

## 074 首次启动向导步骤状态机数据层

`src/core/first_run.rs`：`pending` / `done` / `skipped` 三态显式 code、可回退游标、必选步骤拒跳、跳过态不被前进覆盖、步骤上限 12；顶层 4 键与步骤 3 键严格白名单，15 类坏输入回默认；`serialize()` 只写四键；状态变更走统一信封且步骤 id 不进事件载荷。步骤 id 全作不透明字符串，不内置语言 / 账号 / Java / 外观步骤目录。`api::v1` 7 符号不变。向导 UI、Java 真实检测、账号绑定、`.kculf` 解析未启动。

## 075 皮肤草稿会话元数据层

`src/core/skin_draft.rs`：`saved` / `original` 两类与 `clean` / `dirty` 双态显式 code、并列草稿集合上限 12、保存间隔 `0..=3600` 越界拒、激活项悬空回默认且删除时自动清空、离开提醒缺省开；顶层 4 键与草稿 4 键严格白名单，16 类坏输入回默认；`serialize()` 只写四键；状态变更走统一信封且草稿 id 不进事件载荷。草稿 id 全作不透明字符串，不内置皮肤目录 / 玩家名 / UUID / PNG 路径。`api::v1` 7 符号不变。皮肤编辑器 UI、纹理导出、3D 旋转预览、按玩家名 / UUID 查询与 PNG 下载未启动。

## 076 逐条升级决策数据层

`src/core/upgrade_plan.rs`：`compatible` / `conflict` / `unknown` 三值兼容性与 `defer` / `direct` / `clone` 三选一决策显式 code、按 id 索引候选项集合上限 24、页码 `1..=10` 由集合派生不存游标、单条确认且 `defer` 拒收、`conflict` 自动回退到 `defer` 并清确认态、矛盾态整条跳过；顶层 3 键与候选项 6 键严格白名单，17 类坏输入回默认；`serialize()` 只写三键；状态变更走统一信封且 id 与版本串不进事件载荷。模组 id 与 `current` / `candidate` 版本串全作不透明字符串，不解析 semver、不写死上游实值。`api::v1` 7 符号不变。真实目录复制、升级执行、版本比较执行、签名校验接入、升级决策 UI 未启动。

## 077 搜索筛选条件数据层

`src/core/search_filter.rs`：`name` / `type` / `size` / `modified` / `path` 五维度与 `contains` / `equals` / `prefix` / `suffix` 四运算符显式 code、`current` / `recursive` 两范围值都落、条件集合 / 排除集合 / 保存条件 / 搜索历史四个有界集合、排序规格与方向切换、`matches()` 对启用条件取 AND 且排除项任一命中即拒、`apply()` 先过滤再派生排序索引且不读文件；顶层 7 键与条件 5 键 / 排序 2 键严格白名单，21 类坏输入回默认或跳过；`serialize()` 只写七键；状态变更走统一信封且条件值 / id / 用户文本不进事件载荷。条件值与候选项字段全作不透明字符串，不解析数值 / 正则 / 通配符、不写死上游实值。`api::v1` 7 符号不变。真实目录遍历、结果批量操作、快照解析、筛选 UI 未启动。

## 078 生成器会话数据层

`src/core/generator_session.rs`：`recipe` / `gradient` / `mod_translation` 三类生成器、`legacy` / `json` 双输出格式、`draft` / `ready` / `archived` 三值会话状态显式 code；会话集合 / 翻译条目表 / 历史三个有界集合；`renderable()` / `active_translations()` / `by_kind()` / `clipboard_candidates()` 四个派生纯查询；顶层 5 键与会话 6 键 / 翻译 4 键严格白名单，29 类坏输入回默认或跳过；`ready` 但结果为空在解析与设置两处拒收；`serialize()` 只写五键；状态变更走统一信封且输入 / 结果 / 键 / 值 / id 不进事件载荷。输入与结果全作不透明字符串，不解析算法、不写颜色码字面量、不写端点与密钥。`api::v1` 7 符号不变。生成算法、真实剪贴板写入、翻译执行、生成器 UI 未启动。

## 079 种子可见性与审计数据层

`src/core/seed_access.rs`：`visible` / `hint` / `hidden` 三档权限、`view` / `policy_change` / `guest_toggle` / `hidden` 四类审计动作显式 code；访客模式开关与密码设置标志；种子记录 / 审计条目 / 功能锁定 / 命令黑名单四个有界集合；`classify()` 3×2 六格可见性矩阵与三段派生集合、三档计数、四类审计计数、锁定与命令两判定；`hint` 档必带权限提示文本且非 `hint` 档必空，在解析与两处单条设置共三处拒收；顶层 7 键与记录 4 键 / 审计 4 键严格白名单，32 类坏输入回默认或跳过；`serialize()` 只写七键；状态变更走统一信封且种子值 / 提示文本 / 实例 id / 审计 target / scope 不进事件载荷。种子值与提示文本全作不透明字符串，不解析 NBT、不写地形算法、不写密码学、不写端点与密钥。`api::v1` 7 符号不变。NBT 从存档读种子、地形探索、全屏地图、密码校验、权限提示 UI 未启动。

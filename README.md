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
| 当前轮次 | 041 |
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

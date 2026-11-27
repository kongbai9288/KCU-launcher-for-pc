# 待拍板问题：具体环境

本文件只列参数、版本、组件、运行时条件与已证实事实。不铺场景，不做类比。每条末尾是你要选的项和不选的后果。

---

**EQ-01 Win7 正常模式 UI**

环境：目标 OS = Windows 7 SP1 x86 / x64；Win7 + ARM64 已放弃；Win10 / Win11 x64 / aarch64 保留。rustc 1.99.1（腾讯 rustup 镜像）。`x86_64-pc-windows-gnu` 的 `cargo check --offline` 通过；`x86_64-pc-windows-msvc` / `i686-pc-windows-msvc` 未执行。Win7 路线 = Tier 3 + build-std（011）。

事实：正常模式 UI 宿主候选 tao + wry，Windows 后端依赖 WebView2。微软支持矩阵中 WebView2 Evergreen Runtime 最低 Windows 10，Win7 无分发。`src/` 当前零窗口创建、零渲染代码。`src/core/window.rs` 只有 raw-window-handle 的句柄描述符。

要选：① Win7 上正常模式降级为轻量视图（不加载 WebView2）② 随包分发固定版本 WebView2 Runtime（授权与体积未证实）③ 放弃 Win7 正常模式，Win7 只保留轻量。

不选：L4 UI 宿主不启动。

---

**EQ-02 插件哈希口径（Q-037-01）**

环境：两个插件包文件（Windows `.dll` / Linux `.so`），同一 `plugin_id`；版本号取插件 manifest 的 semver，比较走 034 的 `cmp_precedence`（忽略 `+build`）。

事实：现实现 `src/plugins/identity.rs` = `sha512(plugin_id.as_bytes())[..16]` 的 32 位小写 hex，4 个期望值由 Python `hashlib.sha512` 独立算出。判定链 = 签名校验（036 ed25519-compact）→ 身份哈希一致 → 版本比较 → 手动同意弹窗（037）。

关键：若改成包内容哈希 `sha512(整文件字节)`，两包字节相同则版本必相同（无升级分支），字节不同则哈希必不同（不进升级分支）。内容哈希下升级确认弹窗不可达。

要选：① 保持身份哈希（现实现）② 改内容哈希，并同时重新定义「同一插件」的判定键。

不选：037 的升级确认口径悬空。

---

**EQ-03 真实网络 IO（040 L1–L12）**

环境：crates registry / static.crates.io = 403（025 起多轮）；codeload.github.com tarball = 200；api.github.com = 200（带认证，remaining 约 4900）。`Cargo.lock` 26 包 / 25 第三方，全部走 `vendor/` 目录源，`.cargo/config.toml` 做替换。Win7 WinHTTP 默认不启用 TLS 1.1 / 1.2，需 KB3140245 + `DefaultSecureProtocols=0x800`；SChannel 组件需另配；aws-lc-rs 在 Win7 缺 `ProcessPrng`。

候选真实 manifest：reqwest 0.13.5 MSRV 1.85；ureq 3.5.2 edition 2024 / MSRV 1.85 / rustls 0.23.46 + getrandom + winreg；reqwest 0.12.28 默认带 hyper / hyper-util / tokio / tower 系列。

现状：`http 1.3.1` + `bytes` + `fnv`（040）只构造请求，`percent-encoding 2.3.1`（042）编码批量 id；**零 socket 连接、零 TLS、零代理、零响应解析**。

要选：① 给可用镜像 / 代理地址 ② Win7 只做本地功能，网络走系统组件 ③ 指定 TLS 后端（native-tls SChannel / rustls + 自配随机源）。

不选：下载、模组搜索、CurseForge / Modrinth API 不启动。

---

**EQ-04 崩溃分析**

环境：候选链 = sentry-minidump（MIT）→ minidump（MIT）→ sentry-native（MIT；Breakpad BSD-3 / Crashpad 后端）→ Sentry Rust SDK（MIT）。Sentry 服务端许可 FSL-1.1-Apache-2.0（非 OSI），只接 SDK、不打包服务端。Sentry 官方矩阵：Win10 以下「应支持但未自动测试」。

现状：默认不记录、脱敏默认开、发送前弹完整内容二次确认、DSN 用户自填。`demos/preview/42-settings-crash.png` 是演示，非实现。Win7 方案 = 本地 dump + 手动导出，不假设云端可用。

要选：① 是否包含你自建的 Sentry 服务端（DSN 来源）② Win7 是否只落 `C:\KCU\diagnostics`。

不选：崩溃反馈不进 `Cargo.toml`。

---

**EQ-05 插件子进程隔离（039）**

环境：`extern "C"` 边界上 Rust panic → 进程 abort，`catch_unwind` 抓不到，与 foreign exception 交互是 UB（Nomicon / RFC 2945 原文）。`std::process::Command`：参数不经 shell；`Child` 的 Drop 既不 kill 也不 reap；Windows `.bat` / `.cmd` 例外要求 MSRV ≥ 1.81.0，与 Win7 Tier 3 + build-std 冲突。

现状：ABI（038 libloading）+ 生命周期（039）都是同进程 C ABI 动态库；`kcu_plugin_init` 不在宿主进程执行；插件 init 与主逻辑未接子进程边界。

要选：① 子进程边界方案（独立进程 + IPC / 命令通道）② Win7 是否接受不做自动回收。

不选：设置页「插件单独运行，不影响启动器」保持演示状态。

---

**EQ-06 CurseForge API 方法（CF F17）**

环境：`.github/workflows/ci.yml` 已设 `KCU_CF_API_KEY` secrets 占位（014），值由你填。CF 3rd-party API 条款（010）X01–X04：CF03 禁止 `save or cache any data`；CF02 不得隐藏身份或地理位置、不得经代理 / VPN；CF01 唯一 API Key 不可共享；CF04 竞争产品 / CF05 配额书面许可 / CF06 30 天无因终止未拍板。

现状：`src/core/http.rs` 无端点、无认证头、无响应解析；国内镜像 MCIM / BMCLAPI 条款未补。

要选：给端点、参数、认证方式、缓存与镜像口径（你说完成时给）。

不选：CF 下载不启动；X01–X04 保持未拍板。

---

**EQ-07 特殊版私仓**

环境：`kongbai9288/KCU-launcher-special`，private / main，已建；仅 README 占位，0 代码、0 凭据。后端仓全程 0 写请求。

要选：是否同意把代码放进去。

不选：代码仍只留在公仓主仓（`kongbai9288/KCU-launcher-for-pc`）。

---

**EQ-08 本项目 LICENSE**

环境：仓库根目录无 LICENSE 文件。013 轮 Q-E10「本项目 LICENSE 生成 GPLv3 吗」你答「用」。`docs/licenses/` 已有 20+ 份第三方逐字全文，`THIRD-PARTY-NOTICES.md` 已逐项登记 25 组构建中依赖。

要选：确认生成 GPL-3.0 全文 + 版权持有人写法。

不选：开源分发无主许可证。

---

**EQ-09 028 三项开服器功能**

环境：F028-01 玩家上线提醒 / F028-02 饼图分析活跃度 / F028-03 命令文字触发条件，三份功能 md 已登记，指令为「只记文档」。031 定最严格档（每次确认 + 只允许只读动作）为默认；032 加三档可选松档；Q-031-01 已答「A 是 answer 缩写」。

要选：是否解除「只记文档」进入实现。

不选：三项保持未实现，`src/` 零相关代码。

---

**EQ-10 UX 手感**

环境：`demos/ui-full-kcu-paper.html` 离线可点；56 张 PNG；纸质色板 `#F1EFE8` / `#2C2C2A` / `#3D6B66` / `#B8543F`；88 枚 lucide SVG（Lucide ISC，派生自 Feather 的部分另带 MIT）。`src/` 零界面渲染代码。正常模式实现层默认单主题（007 D04），深浅双主题目前只在演示层预览。

要选：纸纹强度 / 公告位置 / 衬线标题字号 / 深色主题是否进实现层。

不选：UI 实现不启动。

---

**EQ-11 验证环境（受阻事实，非待拍板）**

| 项 | 值 |
| --- | --- |
| rustc / cargo | 1.99.1，腾讯 rustup 镜像可用 |
| `cargo check --offline --target x86_64-pc-windows-gnu` | 通过（038 起每轮） |
| `*-msvc` / i686 / aarch64 / Win7 运行时 | 未执行 |
| 浏览器渲染实测、GUI 端到端 | 无 GUI 环境，未验证 |
| `cargo test --offline` | 044 为 286 / 0；045 为 288 / 0 |
| git HTTP 推送 | 403；走 api.github.com git data API |
| 远端 `main` | 044 为 `14a16cd`，969 文件 ALL_MATCH True |
| 交叉编译 aarch64 / i686 Win7 | Tier 3 + build-std 未执行 |

---

**EQ-12 045 本轮新增：parking_lot 路线核查结论**

环境：`parking_lot 0.12.5`（tag `parking_lot-v0.12.5`，MIT OR Apache-2.0，edition 2021，MSRV 1.71）闭包 = `parking_lot_core 0.9.12` + `lock_api 0.4.14` + `scopeguard 1.1.0` + `smallvec 1.6.1` + `cfg-if 1.0`（038 已有）+ **unix 分支 `libc 0.2.95`** + windows 分支 `windows-link 0.2.0`（038 已有 0.2.1）。026 轮 mini-moka 大闭包已因 libc 受阻。

结论：不引。改轨用标准库 `PoisonError::into_inner` 消除 `src/core/log.rs` 的锁中毒连锁 panic。这不是第三方库替换，文档如实登记，不包装成「全用库」。

要选：若坚持第三方锁实现，需先给 libc 0.2.x 的可用通道（tag 通道已核到 `rust-lang/libc 0.2.177` 可读，但未 vendor）。

不选：锁实现保持标准库 `Mutex`，仅中毒恢复路径由 `PoisonError::into_inner` 接管。

---

**EQ-13 回滚是否要求第三条件（Q-047-01）**

环境：两条判定路径并存。`src/updater/policy.rs::decide`（036）：回滚条件 = `explicit_target` 与候选优先级相等 + `rollback_confirmed`（**2 个条件**），返回 `Install`。`src/plugins/upgrade.rs::decide_upgrade`（037）：回滚条件 = `explicit_target` + `rollback_confirmed` + `user_confirmed_upgrade`（**3 个条件**）。升级路径 037 已用 `user_confirmed_upgrade` 覆盖 036 的「默认只升自动安装」。

一手数据：031 定最严格档（每次确认 + 只允许只读）为默认；032 加三档可选松档；037 你要求「两个插件哈希一致，对比版本号后用户得手动同意才能安装（这叫升级）」。`+build` 差异按 034 走 `cmp_precedence`，047 U94 已把两条路径的相等判定统一。

具体分叉：输入 `current="1.3.0"` / `candidate="1.2.2"` / `explicit_target="1.2.2"` / `rollback_confirmed=true` / `user_confirmed_upgrade=false` 时，`decide` → `Install`，`decide_upgrade` → `Reject`。

要选：① 回滚也要求 `user_confirmed_upgrade`（统一为 3 个条件）② 回滚保持 2 个条件（显式目标 + 二次确认已足够）③ 由更新器插件自己在调用前弹确认，两处都不判。

不选：两条路径对同一操作给出相反结果，Q-047-01 悬空；047 只统一了 `+build` 相等判定，未改条件数量。单页见 `docs/records/eq13-rollback-conditions.md`。

---

**EQ-14 演示数据源语言包迁移（048）**

环境：`demos/ui-full-kcu-paper.html` 的 `<script>` 段有 `NOTICES` / `POPUPS` / `INS` / `SRV` / `AUTH` / `OB` / `CREDITS` / `AUTO_EFFECT` 等常量数组，298 行含中文（671 个单引号字符串 / 503 唯一、11 个模板串、36 个双引号片段）。023 定的实现方案是 Project Fluent `.ftl` + `i18n-embed`，语言包放 `C:\KCU\i18n\<locale>\`，插件可追加。当前 `src/` 无 Fluent 依赖（`Cargo.lock` 26 包 / 25 第三方）。英文态 `EN_TEXT` 有 567 条回退中文。

要选：① 实现层按 023 落 Fluent，演示层只保留 key 与最小占位数据 ② 演示层先拆出独立 `demos/lang/*.json`，中文/英文各一份，`setLang` 时重建数组 ③ 演示数据源维持现状，明确标注「仅中文演示数据」，不承诺英文态。

不选：英文态切语言后公告正文、弹窗描述、表格行仍是中文。详见 `docs/records/requirement-compliance-audit.md`。

---

**EQ-15 端点配置化（048）**

环境：`src/lightweight/download.rs::plan` 硬编码 `scheme = "https"`、`path = "/v1/batch"`；`src/core/config.rs` 已有 `endpoints` 表与 `set_endpoint` / `endpoint`，但 `plan()` 没读它。00-requirements 第 7.3 节「禁止硬编码环境假设」，11-features-input「尽量不要 api 写死…那些联网他们有可能后面会更新相关的端口」。

要选：① `plan()` 改从 `Config::endpoint` 取 scheme / authority / path，缺省才回内置 ② 保持代码内常量，但集中到 `src/core/endpoints.rs` 单文件 ③ 维持现状，登记为已知偏差。

不选：B03 保持未遵守。详见 `docs/records/requirement-compliance-audit.md`。

---

**EQ-14 已拍板（049）**

答复：「抽」→ 按选项 ② 执行。已生成 `demos/lang/zh-CN.js` / `demos/lang/en-US.js`（各 24 键），HTML 用 `<script src>` 离线加载，`setLang` 调用 `loadData` 重建 20 个数据数组并用 `mergeState` 合并运行时状态。`lang_guard.py` + CI step 落地。英文包 471 条数据源字符串仍保留中文（L-049-1），未做词级拼接或人工补译。

EQ-15（端点配置化）仍待拍板，是 049 之后唯一的下一步。

**EQ-15 按默认落地（050）**

用户未明确拍板三选项，按 049 结尾「或者继续『干』我按默认往下走」执行选项①：`plan()` 从 `Config::endpoint("download/batch")` 取 scheme / authority / path，缺省才回内置；常量集中到 `src/core/endpoints.rs`。`resolve()` 用 `http::Uri` 解析并支持 8 类回退 reason。B03 代码层偏差消除，设置页端点控件与 `§` 模板仍属 UI 层未启动。登记为 **D-050-1**（我的默认，不是用户决断）。

EQ-01 ~ EQ-13 仍待拍板；EQ-14（049）、EQ-15（050）已关闭。

**051 状态**

本轮未新增 EQ。B01 / B02 判定为「本轮起执行，历史偏差不补写」，不需要拍板；B06 演示层三项已补，实现层 D07 未启动，待上层能力启动时按 023 规矩逐项取 LICENSE 全文再引依赖。EQ-01 ~ EQ-13 仍待拍板；EQ-14（049）、EQ-15（050）已关闭。

**052 状态**

本轮未新增 EQ。用户回「干」而非点 EQ 编号，按 051 结尾默认执行 B06 实现层签名比对，登记 **D-052-1**（我的默认，不是用户决断）。EQ-01 ~ EQ-13 仍待拍板；EQ-14（049）、EQ-15（050）已关闭。

**053 状态**

本轮未新增 EQ。用户回「干」而非点 EQ 编号，按 052 结尾默认把 B06 第二项的**本地判定层**落地（平台策略、公钥、设备能力全部由调用方注入，不碰真实网络 IO），登记 **D-053-1**（我的默认，不是用户决断）。EQ-01 / EQ-03 的 Win7 TLS 口径仍是真实网络 IO 层的前置；EQ-01 ~ EQ-13 仍待拍板，EQ-14（049）、EQ-15（050）已关闭。

**054 状态**

本轮未新增 EQ。用户回「干」而非点 EQ 编号，按 053 结尾默认继续走 048 核对表剩余 B 类偏差，选 **B08**（明确原文、不碰真实网络 IO、不碰 UI 闸门），登记 **D-054-1**（我的默认，不是用户决断）。新增 **D-054-2**：原文只点名离线账户，第三方登录与正版保持可用，按最小范围执行；若用户本意要扩大到全部账户类型，需明确拍板。EQ-01 / EQ-03 的 Win7 TLS 口径仍是真实网络 IO 层的前置；EQ-01 ~ EQ-13 仍待拍板，EQ-14（049）、EQ-15（050）已关闭。

**055 状态**

C 类 10 条复核完成，逐条证据与具体值在 `docs/records/c-class-default-recheck.md`。Q-031-01 已答「A 是 answer 缩写」并于 033 结案；048 C05 台账笔误、054 结尾错述均已撤回，031/032 追加 055 补记，`scripts/policy_guard.py` + CI `policy_guard` step 守护口径不被回退。

新增待拍板（只列口径）：**Q-C01** 轻量 13 项排除清单（当前 13 项 / 可增删）；**Q-C02** 正常模式实现层主题数（当前单主题 / 深浅双主题）；**Q-C08** 一级导航项数（当前 9 项 / 可增删）；**Q-037-01** 插件哈希口径（当前身份哈希 `sha512(plugin_id)[..16]` / 内容哈希，两种后果见复核表 C04）。EQ-01 ~ EQ-13 仍待拍板，EQ-14（049）、EQ-15（050）已关闭；本轮未新增 EQ。

**056 状态**

B 类 10 条状态复核完成，逐条证据与五条 B→EQ 可拍环境在 `docs/records/b-class-status-recheck.md`：B04 → EQ-01（Win7 WebView2）、B05 → 源仓库与许可未给（无 EQ）、B07 → EQ-05（子进程隔离）、B09 → EQ-11（32 位 / MSVC / i686）、B10 → 推进口径未决断。本轮**不擅自开工**这五条。

E127 / E128 / E129 三处台账滞后已追加补记；`scripts/delivery_guard.py` + CI `scan` 第 10 步守护交付格式六项。EQ-01 ~ EQ-13 仍待拍板，EQ-14（049）、EQ-15（050）已关闭；Q-C01 / Q-C02 / Q-C08 / Q-037-01 仍待拍板。本轮未新增 EQ。

**057 状态**

用户未点 EQ 编号。本轮真读 `00-requirements.txt` 第 12 节，落地 §12 启动级兜底（不依赖任何 EQ）：`BootState` 持久化计数、四级 `Tier`、四项诊断包落盘、dispatcher 接线。B04 / B05 / B07 / B09 / B10 仍**未开工**，卡点 EQ-01 / 源仓库与许可未给 / EQ-05 / EQ-11 / 推进口径未决断不变。EQ-01 ~ EQ-13 仍待拍板，EQ-14（049）、EQ-15（050）已关闭；Q-C01 / Q-C02 / Q-C08 / Q-037-01 仍待拍板。本轮未新增 EQ。

## 092 摊平

状态：092 复核，不代拍。范围：EQ-01 ~ EQ-13（13 条；EQ-14 / EQ-15 已关闭）、3 条 Q-C + Q-037-01（共 4 项）、Q-091-01 / Q-091-02 / Q-091-03、058–091 新增 Q 共 31 条、2 项 `Planned`。每条状态一律「待拍板 / 未证实」。历史行不重写（A181 / A201）。

### A 组：阻塞 2 项 `Planned`（拍板面最小）

| 项 | 环境 | 选项 | 后果 | 耦合 |
| --- | --- | --- | --- | --- |
| EQ-03 + AX07 `doh_support` | Win7 SP1 x86/x64；KB3140245 / DefaultSecureProtocols / SChannel / rustls ProcessPrng 补丁分开登记（A119）；`src/core/http.rs` 只有 plan 构造器，无 TcpStream；`31-axolotl-launcher-features.md:35` 写「真实网络 IO 未启动、Win7 TLS 前置（EQ-03）」；00 / 11 / 12 号全文无 DoH 锚点 | ① 先起真实网络执行层再落 DoH ② 保持 `Planned`，DoH 降级为端点配置项 ③ 明确不做 DoH 并从功能池撤下 | ① 需新增网络栈与 Win7 运行时验证，体积与 MSRV 变化；② 不引入依赖，AX07 conflict 保持 `network_io_not_started`；③ 与「别人有的功能要有」（00:44）冲突，需显式撤回 | EQ-01（UI 框架）、EQ-11（i686 / MSVC / Win7 运行时）、Q-091-01（AX22 端点）、B10（推进口径） |
| EQ-01 + Q-091-01 + AX22 `shimu_account` | WebView2 Evergreen Runtime 最低 Win10，Win7 无分发；`11:7` 境外离线账户限制、054 双信号 Unknown 放行；`11:18` API 不共有（063 `client_ai_gate` 为 GateOnly）；第三方端点 / 浏览器授权形态 / 签名校验口径未给 | ① 给出端点与授权形态后再落 ② 只落「断开关联」本地状态、不碰网络 ③ 保持 `Planned` | ① 需端点配置化 + 境外限制判定先定；② 不写死端点，但功能只剩本地开关；③ 2 项 `Planned` 继续挂账 | EQ-03、EQ-01、B05（HMCL 源与许可未给）、`11:7` / 054 |
| Q-091-02 + Q-091-03 | 090 `projection.rs` 已落 fit / original / scaled 三档视图；075 `banner_design.rs` 撤销栈 `MAX_HISTORY=64`；091 `studio_image.rs` 显式不碰两者（E369 口径） | ① 复用既有模块 ② 各模块独立注册表 ③ 等 EQ-01 拍板后一次定 | ① 减少重复常量表，边界由守卫持有；② 三份同构数据层，A284 张力继续；③ UI 闸门不开则两者都停在文档层 | A100（UI 渲染层）、EQ-01、`00:175` 复用口径 |

### B 组：3 条 Q-C + Q-037-01（共 4 项）

| 项 | 环境 / 已证实事实 | 选项 | 后果 | 耦合 |
| --- | --- | --- | --- | --- |
| Q-C01 | 轻量 13 项排除清单，当前 13 项 | 增删清单 | 改动影响 `excluded_assets_cover_normal_ui_and_heavy_components` 断言 | A68 / 016 |
| Q-C02 | 正常模式实现层单主题 / 深浅双主题 | 单主题 / 双主题 | 双主题需 `view_uses_single_theme` 反向验证 | A79 / 018 |
| Q-C08 | 一级导航当前 9 项 | 增删项 | 配置类功能挂一级导航会撞 A85 | A85 / 020 |
| Q-037-01 | 身份哈希 `sha512(plugin_id)[..16]`；改内容哈希后升级确认弹窗不可达（本文件 EQ-02 段） | 保持身份哈希 / 改内容哈希并重定义「同一插件」判定键 | 后者使 037 升级确认口径悬空 | EQ-02 / A96 |

091 结尾写「4 条 Q-C」。按 A202 打开 `pending-question-environments.md` 尾部、`c-class-default-recheck.md`、`b-class-status-recheck.md:85` 核：真实待拍为 Q-C01 / Q-C02 / Q-C08 三条 Q-C 加一条 Q-037-01，共 4 项，Q-037-01 不属 Q-C 组。口径修正登记 E375，历史行不重写（A181 / A201）。

### C 组：EQ-01 ~ EQ-13 逐编号索引（不重复铺场景，A150）

| 编号 | 台账锚点 | 状态 |
| --- | --- | --- |
| EQ-01 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-02 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-03 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-04 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-05 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-06 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-07 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-08 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-09 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-10 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-11 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-12 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
| EQ-13 | `pending-question-environments.md` 048–057 段；`b-class-status-recheck.md:61` | 未证实（待拍板） |
EQ-14（048 新增 / 049 按选项②关闭）、EQ-15（048 新增 / 050 按选项①关闭）已关闭，不计入 13 条待拍。逐条环境 / 事实 / 选项 / 后果见本文件 048–057 段，092 不重写。

### D 组：058–091 新增 Q 全集（31 条，按轮次）

- 067 轮：Q-067-01 / Q-067-03（定义见 `docs/decisions/067-*.md`，状态未证实 / 待拍板）
- 070 轮：Q-070-01（定义见 `docs/decisions/070-*.md`，状态未证实 / 待拍板）
- 071 轮：Q-071-01 / Q-071-02（定义见 `docs/decisions/071-*.md`，状态未证实 / 待拍板）
- 072 轮：Q-072-01 / Q-072-02（定义见 `docs/decisions/072-*.md`，状态未证实 / 待拍板）
- 073 轮：Q-073-01 / Q-073-02（定义见 `docs/decisions/073-*.md`，状态未证实 / 待拍板）
- 074 轮：Q-074-01 / Q-074-02（定义见 `docs/decisions/074-*.md`，状态未证实 / 待拍板）
- 075 轮：Q-075-01 / Q-075-02（定义见 `docs/decisions/075-*.md`，状态未证实 / 待拍板）
- 076 轮：Q-076-01 / Q-076-02（定义见 `docs/decisions/076-*.md`，状态未证实 / 待拍板）
- 077 轮：Q-077-01 / Q-077-02（定义见 `docs/decisions/077-*.md`，状态未证实 / 待拍板）
- 078 轮：Q-078-01 / Q-078-02（定义见 `docs/decisions/078-*.md`，状态未证实 / 待拍板）
- 079 轮：Q-079-01 / Q-079-02（定义见 `docs/decisions/079-*.md`，状态未证实 / 待拍板）
- 080 轮：Q-080-01 / Q-080-02（定义见 `docs/decisions/080-*.md`，状态未证实 / 待拍板）
- 081 轮：Q-081-01 / Q-081-02（定义见 `docs/decisions/081-*.md`，状态未证实 / 待拍板）
- 082 轮：Q-082-01（定义见 `docs/decisions/082-*.md`，状态未证实 / 待拍板）
- 090 轮：Q-090-01 / Q-090-02（定义见 `docs/decisions/090-*.md`，状态未证实 / 待拍板）
- 091 轮：Q-091-01 / Q-091-02 / Q-091-03（定义见 `docs/decisions/091-*.md`，状态未证实 / 待拍板）
Q-028-01 / Q-028-02、Q-031-01（033 已关闭）、Q-047-01、Q-A ~ Q-H 组（013 已答复，见 `docs/records/round-013-answers.md`）不重开；`docs/records/open-questions.md` 93 条（`grep -cE '^\| Q-[A-H][0-9]'` 实跑 93）状态列以该文件为准，092 不把词频当条数（A35）。

### 已决断

真读 00 / 11 / 12 号全文后逐条分列（A164）。以下为原文已决断、不依赖 EQ 的锚点；实现状态另按 9.3 分层，不合并表述：
- `00:24`「所有的ui等都使用框架方式」已决断；EQ-01 待拍的是具体框架与 Win7 降级路线，不是「要不要框架」。
- `00:8` ≤2GB 首次默认轻量、可经 `launch.json` 手动控制；`boot.rs` 已落判定层。
- `11:7` 境外离线账户限制、不得用网络打法；054 已落双信号 + Unknown 放行。
- `11:10` 每一个弹窗都需要有关闭逻辑；`popup.rs` 已落同一 `closeDlg`。
- `11:18` 不把 API 写成共有；063 `client_ai_gate` 为 GateOnly。
- `12:63` png 快速设置服务器 logo 自动调整像素；091 已落 AX15 数据层，六动作与渲染层未启动。
- `12:12` 关机需点击关机实例、关窗口须先保存；原文已决断，执行层未启动。

### 未决断

EQ-01 ~ EQ-13（13 条）、3 条 Q-C + Q-037-01、Q-091-01 / 02 / 03、D 组 31 条历史 Q、2 项 `Planned` 的网络前置、B05 的 HMCL 源仓库与许可、`11:242` 第 34 条「使用满两天」时长路径（Q-067-02）、6 项低可信度转述、逐版本归属。全部保持「待拍板 / 未证实」，092 不代拍、不定 2 项 `Planned` 之间的优先级（A208 / A164 / A250）。

### 092 逐值默认（A203 / A177，均为我的默认，不写成用户已决断）

D-092-1 本轮性质：拍板闭环轮，`src/` 零改动、`Cargo.*` 零 diff、不落功能实现。D-092-2 清单口径：只列环境 / 选项 / 后果 / 耦合，状态一律待拍板。D-092-3 Q-C 口径修正：3 条 Q-C + Q-037-01 共 4 项（E375）。D-092-4 EQ 口径：EQ-01 ~ EQ-13 共 13 条待拍，EQ-14 / EQ-15 已关闭。D-092-5 功能池不变：`Planned 2` / `DataLayer 21` / `GateOnly 1`，AX07 conflict 保持 `network_io_not_started`。D-092-6 新增 `scripts/pending_decisions_guard.py` 挂 CI `scan`，双向注入按实记数。D-092-7 四件套 + 台账补记 + 两个 zip 重打，一次提交一次增量推送。D-092-8 按 `00:245` 不发通过标记。D-092-9 唯一下一步：等用户拍板，按 A208 不擅自开工硬做。

## 093 状态

093 用户当轮明确指令为提交功能位置 txt，按 `00:248` 覆盖 092「等用户拍板 A 组」的预告。A 组最小拍板面（EQ-03 + AX07、EQ-01 + Q-091-01 + AX22）、其余 11 条 EQ、Q-C01 / Q-C02 / Q-C08 / Q-037-01、Q-091-01 / 02 / 03 与 D 组 31 条历史 Q 仍全部「待拍板 / 未证实」。位置清单第六节新增 5 条候选调整，同为待拍板未执行。092 段历史行不重写（A181 / A201）。

## 094 补记

094 用户当轮明确指令为功能重新归类与详细行为链路，按 `00:248` 覆盖 093「点第六节 5 条偏差」的预告。A 组最小拍板面（EQ-03 + AX07、EQ-01 + Q-091-01 + AX22）、其余 11 条 EQ、Q-C01 / Q-C02 / Q-C08 / Q-037-01、Q-091-01 / 02 / 03 与 D 组 31 条历史 Q 仍全部「待拍板 / 未证实」。094 新增 8 条候选归类规则与 10 条散落归位，同为待拍板未执行。092 / 093 段历史行不重写（A181 / A201）。

## 095 补记

095 用户当轮明确表示归位方案由用户设计、稍后给，按 `00:248` 覆盖 094「点第三 / 四 / 五 / 六节里要执行哪几条归位」的预告。A 组最小拍板面（EQ-03 + AX07、EQ-01 + Q-091-01 + AX22）、其余 11 条 EQ、Q-C01 / Q-C02 / Q-C08 / Q-037-01、Q-091-01 / 02 / 03 与 D 组 31 条历史 Q 仍全部「待拍板 / 未证实」。095 新增 7 条真漏候选域、4 条部分覆盖展开与 2 条锚点补挂，同为待拍板未执行。092 / 093 / 094 段历史行不重写（A181 / A201）。

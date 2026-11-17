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

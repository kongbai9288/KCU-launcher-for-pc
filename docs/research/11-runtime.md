# 底层运行时、裁剪、进程管理与本地库加载

检索日期：2026-11-05
轮次：009
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。
对应需求：docs/spec/00-requirements.txt:229、:230、:231

## Cargo profile

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| strip 可选值 | `"none"`、`"debuginfo"`、`"symbols"`；布尔 `true` = `"symbols"`，`false` = `"none"`；默认 `"none"` | 已证实 | https://doc.rust-lang.org/cargo/reference/profiles.html |
| lto 可选值 | `true` / `"fat"` / `"thin"` / `false` / `"off"`；release 默认 `false` | 已证实 | https://doc.rust-lang.org/cargo/reference/profiles.html |
| panic 可选值 | `"unwind"` / `"abort"`；release 默认 `"unwind"` | 已证实 | https://doc.rust-lang.org/cargo/reference/profiles.html |
| codegen-units | 大于 0 的整数；incremental 默认 256，non-incremental 默认 16 | 已证实 | https://doc.rust-lang.org/cargo/reference/profiles.html |
| opt-level 可选值 | `0` `1` `2` `3` `"s"` `"z"`；release 默认 `3` | 已证实 | https://doc.rust-lang.org/cargo/reference/profiles.html |
| debug 可选值 | `0`/`false`/`"none"`、`"line-tables-only"`、`1`/`"limited"`、`2`/`true`/`"full"` | 已证实 | https://doc.rust-lang.org/cargo/reference/profiles.html |
| split-debuginfo | 字符串，值与编译器一致；macOS 默认 `unpacked` | 已证实 | https://doc.rust-lang.org/cargo/reference/profiles.html |
| incremental | `true` / `false`；可被 `CARGO_INCREMENTAL` 或 `build.incremental` 覆盖 | 已证实 | https://doc.rust-lang.org/cargo/reference/profiles.html |
| release 默认集合 | `opt-level=3`、`debug=false`、`strip="none"`、`debug-assertions=false`、`overflow-checks=false`、`lto=false`、`panic="unwind"`、`incremental=false`、`codegen-units=16`、`rpath=false` | 已证实 | https://doc.rust-lang.org/cargo/reference/profiles.html |

## Windows 本地库加载

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 安全 DLL 搜索模式启用 | 当前目录位于搜索顺序第 11 位，在应用加载目录之后 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order |
| 安全 DLL 搜索模式禁用 | 当前目录前移至第 8 位，紧跟应用加载目录 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order |
| SetDllDirectory | 指定非空目录时有效禁用安全 DLL 搜索模式；传 NULL 恢复 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order |
| 预加载攻击 | 攻击者控制被搜索目录时可放置同名恶意 DLL | 已证实 | https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order |
| LOAD_LIBRARY_SEARCH 标志 | 可与 `LoadLibraryEx` 或 `SetDefaultDllDirectories` 组合指定搜索顺序 | 已证实 | https://msdn.microsoft.com/zh-tw/windows/apps/ms682586 |
| LOAD_LIBRARY_SEARCH_APPLICATION_DIR | `0x00000200` | 已证实 | https://technet.microsoft.com/en-us/office/hh310515 |
| LOAD_LIBRARY_SEARCH_SYSTEM32 | `0x00000800` | 已证实 | https://technet.microsoft.com/en-us/office/hh310515 |
| LOAD_LIBRARY_SEARCH_USER_DIRS | `0x00000400` | 已证实 | https://technet.microsoft.com/en-us/office/hh310515 |
| LOAD_LIBRARY_SEARCH_DEFAULT_DIRS | `0x00001000`，为 APPLICATION_DIR + SYSTEM32 + USER_DIRS 组合 | 已证实 | https://technet.microsoft.com/en-us/office/hh310515 |
| 标志组合搜索顺序 | DLL_LOAD_DIR → APPLICATION_DIR → USER_DIRS → SYSTEM32 | 已证实 | https://technet.microsoft.com/en-us/office/hh310515 |
| SetDefaultDllDirectories 最低支持 | Windows 8 / Windows Server 2012；Windows 7、2008 R2、Vista、2008 需 KB2533623 并用 GetProcAddress | 已证实 | https://technet.microsoft.com/en-us/office/hh310515 |
| 进程默认搜索路径 | 仅作用于调用进程，进程生命周期内持续；不可回退到标准搜索路径 | 已证实 | https://technet.microsoft.com/en-us/office/hh310515 |

## 进程管理

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| Command::new | 以程序路径创建配置，builder 方法在 spawn 前修改 | 已证实 | https://doc.rust-lang.org/std/process/struct.Command.html |
| spawn | 启动子进程并返回句柄 | 已证实 | https://doc.rust-lang.org/std/process/struct.Command.html |
| output | 启动子进程，等待结束并收集全部输出 | 已证实 | https://doc.rust-lang.org/std/process/struct.Command.html |
| status | 启动子进程，等待结束并收集退出状态 | 已证实 | https://doc.rust-lang.org/std/process/struct.Command.html |
| 参数不经 shell | 引号、转义、词分割、glob、变量替换均不生效 | 已证实 | https://doc.rust-lang.org/std/process/struct.Command.html |
| Windows 参数解码 | `cmd.exe` 与 `.bat` 使用非标准解码，不可信输入存在注入风险 | 已证实 | https://doc.rust-lang.org/std/process/struct.Command.html |
| creation_flags | 传给 `CreateProcess`，总是与 `CREATE_UNICODE_ENVIRONMENT` 按位或 | 已证实 | https://doc.rust-lang.org/std/os/windows/process/trait.CommandExt.html |
| raw_arg | 追加字面文本，不加引号、不做转义 | 已证实 | https://doc.rust-lang.org/std/os/windows/process/trait.CommandExt.html |
| force_quotes | 强制所有参数用引号包裹 | 已证实 | https://doc.rust-lang.org/std/os/windows/process/trait.CommandExt.html |
| CREATE_NO_WINDOW 具体值 | 页面未写明 | 未证实 | https://doc.rust-lang.org/std/os/windows/process/trait.CommandExt.html |
| std::process 超时 API | 页面未写明 | 未证实 | https://doc.rust-lang.org/std/process/struct.Command.html |

## WebView2 进程模型

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 进程组组成 | 单个 browser process + 一个或多个 renderer + GPU / Audio 等 helper | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/process-model |
| browser process | 每个进程组只有一个，不与 renderer 数量同增 | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/process-model |
| renderer 数量 | 随 Site Isolation 与不同 disconnected origin 数量变化 | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/process-model |
| user data folder | 进程集合与单个 user data folder 绑定；多个 folder 各建一组进程 | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/process-model |
| 环境共享 | 配置相同（含同一 user data folder）的多个 `CoreWebView2Environment` 复用同一进程集合 | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/process-model |
| 内存占用与进程数关系 | 页面未写明 | 未证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/process-model |

## 单文件发布与目标三元组

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 目标三元组 | 告知编译器输出类型的字符串 | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| x86_64-pc-windows-msvc | 64 位 MSVC，Windows 10+ / Server 2016+ | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| x86_64-pc-windows-gnu | 64 位 MinGW，Windows 10+ / Server 2016+ | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| aarch64-pc-windows-msvc | ARM64 Windows MSVC | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| Tier 1 | 带宿主工具，自动测试保证 host tools 通过 | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| Tier 2 | 带宿主工具，自动构建保证 host tools 可构建 | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| Tier 3 | 代码库支持，不自动构建或测试 | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| MSVC 运行库三种部署 | central deployment、local deployment、static linking | 已证实 | https://learn.microsoft.com/en-us/cpp/windows/deployment-in-visual-cpp |
| central deployment | DLL 装入 `Windows\System32`；32 位库在 x64 上装入 `Windows\SysWow64`；来源为 Redistributable package 或 .msm merge modules | 已证实 | https://learn.microsoft.com/en-us/cpp/windows/deployment-in-visual-cpp |
| local deployment | 库文件装入应用目录，与可执行文件同目录 | 已证实 | https://learn.microsoft.com/en-us/cpp/windows/deployment-in-visual-cpp |
| static linking | 库代码编入应用，生成无 DLL 依赖的单二进制 | 已证实 | https://learn.microsoft.com/en-us/cpp/windows/deployment-in-visual-cpp |
| 本项目单文件发布工具链 | 未选定，不写死目标三元组 | 未证实 | docs/checklists/windows-errors.md:18 |

## 玩家分支启动器横评

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 横评页面存在 | 列出 PCL2、HMCL、MultiMC、Prism Launcher、BakaXL、原版启动器，维度为平台、内置搜索、下载速度、Mod 管理、多实例 | 已证实 | https://pcl2.ijinshan.com/pages/concepts/minecraft-launchers/ |
| 页面归属 | PCL2 相关站点，含「PCL2 在所有维度上都表现得最优」「国内使用人数最多、社区反馈最积极」等推广措辞 | 已证实 | https://pcl2.ijinshan.com/pages/concepts/minecraft-launchers/ |
| 各启动器排名与星级 | 第三方推广页，无一手数据，不作选型结论 | 未证实 | https://pcl2.ijinshan.com/pages/concepts/minecraft-launchers/ |
| 各启动器开源状态 | 页面声称均开源，未逐仓库核对 LICENSE | 未证实 | https://pcl2.ijinshan.com/pages/concepts/minecraft-launchers/ |
| 功能项候选 | 内置 Mod 搜索、多线程下载、多下载源、多实例、Java 运行时配置、账号验证 | 未证实 | https://pcl2.ijinshan.com/pages/concepts/minecraft-launchers/ |

约束：

| 编号 | 内容 |
| --- | --- |
| C01 | 横评排名、星级、用户量不写进实现计划与选型记录。 |
| C02 | 功能项候选未逐仓库取得 LICENSE 前不复制代码、资源、商标。 |
| C03 | Cargo profile 取值只在构建配置确认后写入，不写死工具链。 |
| C04 | 本地库加载使用 SetDefaultDllDirectories + LOAD_LIBRARY_SEARCH_DEFAULT_DIRS 顺序；不调用 SetDllDirectory 非空路径。 |
| C05 | 进程参数走 `arg` / `args_os`，不使用 `raw_arg` 拼接不可信输入；不经过 `cmd.exe` / `.bat`。 |
| C06 | 超时由外层实现，std::process 页面未提供超时 API，不假装有。 |

## 电脑端多操作入口交互

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 具体形式 | 未定 | 未证实 | docs/spec/00-requirements.txt:231 |
| 约束 | 一个入口承载多个操作的思路保留，不套用手机手势 | 已证实 | docs/spec/00-requirements.txt:231 |

## 009 一手来源清单

| 编号 | URL | 用途 | 结果 |
| --- | --- | --- | --- |
| R01 | https://doc.rust-lang.org/cargo/reference/profiles.html | Cargo profile 默认值 | 200 |
| R02 | https://learn.microsoft.com/en-us/windows/win32/dlls/dynamic-link-library-search-order | DLL 搜索顺序 | 200 |
| R03 | https://msdn.microsoft.com/zh-tw/windows/apps/ms682586 | LOAD_LIBRARY_SEARCH 中文原文 | 200 |
| R04 | https://technet.microsoft.com/en-us/office/hh310515 | SetDefaultDllDirectories 标志与最低系统 | 200 |
| R05 | https://doc.rust-lang.org/std/process/struct.Command.html | 进程创建与参数 | 200 |
| R06 | https://doc.rust-lang.org/std/os/windows/process/trait.CommandExt.html | Windows CommandExt | 200 |
| R07 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/process-model | WebView2 进程组 | 200 |
| R08 | https://doc.rust-lang.org/rustc/platform-support.html | 目标三元组与 tier | 200 |
| R09 | https://learn.microsoft.com/en-us/cpp/windows/deployment-in-visual-cpp | MSVC 运行库三种部署 | 200 |
| R10 | https://pcl2.ijinshan.com/pages/concepts/minecraft-launchers/ | 第三方横评，标推广措辞 | 200 |
| R11 | https://learn.microsoft.com/en-us/cpp/windows/deploying-visual-cpp-applications | 首轮路径 | 受阻，抓取被拒 |

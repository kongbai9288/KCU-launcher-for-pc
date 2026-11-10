# Win7 兼容、多架构与系统 API 一手调研

检索日期：2026-11-11
轮次：011
对应：docs/spec/00-requirements.txt:25、:42、:229；docs/spec/11-features-input.txt:开头段、:支持32位操作系统和64位操作系统、:对win7默认进入轻量模式、:支持多个处理器架构、:系统api等调用你需要看看他的真实的api
锚点格式：完整 URL 或 `path:line`；锚点逐行独立。

## 版本判定真实 API

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| OS01 | `Indicates if the current OS version matches, or is greater than, the Windows 7 version.` / `True if the current OS version matches, or is greater than the Windows 7 version; otherwise, false.` | `IsWindows7OrGreater()` 返回值语义 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/versionhelpers/nf-versionhelpers-iswindows7orgreater |
| OS02 | `Header: versionhelpers.h` / `Minimum supported client: Windows 2000 Professional [desktop apps only]` | Win7 上可用 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/versionhelpers/nf-versionhelpers-iswindows7orgreater |
| OS03 | `在 Windows 8.1 及更高版本中,已弃用 GetVersion 和 GetVersionEx 函数｡截至Windows 10,VerifyVersionInfo 函数也已弃用｡` / `如果应用程序不专门面向Windows 8.1或更高版本,则函数将返回Windows 8版本 (6.2)` | `GetVersion` / `GetVersionEx` / `VerifyVersionInfo` 已弃用且需 manifest 才能取真实版本 | 已证实 | https://learn.microsoft.com/zh-cn/windows/desktop/SysInfo/targeting-your-application-at-windows-8-1 |
| OS04 | `GetVersion､ GetVersionEx､ VerifyVersionInfo 和 版本帮助程序函数 仅适用于桌面应用` | 桌面应用限定 | 已证实 | https://learn.microsoft.com/zh-cn/windows/desktop/SysInfo/targeting-your-application-at-windows-8-1 |

约束：版本判定走 `versionhelpers.h`，不走 `GetVersionEx`；应用清单需声明支持的 Windows 版本。OS03 的 manifest 声明本轮未确认具体字段，标未证实。

## 处理器架构判定真实 API

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| AR01 | `VOID GetNativeSystemInfo( [out] LPSYSTEM_INFO lpSystemInfo );` | 函数签名 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getnativesysteminfo |
| AR02 | `If the function is called from a 64-bit application, it is equivalent to the GetSystemInfo function. If the function is called from an x86 or x64 application running on a 64-bit system that does not have an Intel64 or x64 processor (such as ARM64), it will return information as if the system is x86 only if x86 emulation is supported (or x64 if x64 emulation is also supported).` | WOW64 与模拟架构下返回值受模拟层影响 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getnativesysteminfo |
| AR03 | `Minimum supported client : Windows XP [desktop apps | UWP apps]` | Win7 上可用 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getnativesysteminfo |
| AR04 | `wProcessorArchitecture` 的 `PROCESSOR_ARCHITECTURE_INTEL` / `_AMD64` / `_ARM64` 取值 | GetNativeSystemInfo 页面未列出 | 未证实 | https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getnativesysteminfo |
| AR05 | 32 位进程在 64 位系统上读取原生架构 | AR02 已证实；需配合 `IsWow64Process2` 才能区分 ARM64 宿主 | 未证实 | AR02 页面未给完整方案 |

## 本地地理位置 API（用户指定不走网络探测）

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| GE01 | `GEOID GetUserGeoID( [in] GEOCLASS GeoClass );` | 函数签名 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getusergeoid |
| GE02 | `Returns the geographical location identifier of the user if SetUserGeoID has been called before to set the identifier. If no geographical location identifier has been set for the user, the function returns GEOID_NOT_AVAILABLE.` | 未调用 `SetUserGeoID` 时返回 `GEOID_NOT_AVAILABLE` | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getusergeoid |
| GE03 | `Minimum supported client : Windows XP [desktop apps | UWP apps]` / `Library : Kernel32.lib ; DLL : Kernel32.dll` | Win7 上可用 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getusergeoid |
| GE04 | `int GetGeoInfoW( [in] GEOID Location, [in] GEOTYPE GeoType, [out, optional] LPWSTR lpGeoData, [in] int cchData, [in] LANGID LangId );` | 函数签名 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getgeoinfow |
| GE05 | `Minimum supported client: Windows XP [desktop apps | UWP apps]` / `The function returns 0 if it does not succeed.` | Win7 上可用，失败返回 0 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getgeoinfow |
| GE06 | `GEO_ISO2 Value:0x0004 The ISO 2-letter country/region code.` / `GEO_ISO3 Value:0x0005 The ISO 3-letter country/region code.` / `GEO_LATITUDE Value:0x0002` / `GEO_LONGITUDE Value:0x0003` | `SYSGEOTYPE` 取值 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/ne-winnls-sysgeotype |
| GE07 | `GEO_NATION Value:0x0001 ... Starting with Windows 10, version 1709:This value is not supported for the GetGeoInfoEx function, and should not be used.` | Win10 1709+ 对 `GetGeoInfoEx` 不推荐 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/ne-winnls-sysgeotype |
| GE08 | `int GetGeoInfoEx( [in] PWSTR location, [in] GEOTYPE geoType, [out, optional] PWSTR geoData, [in] int geoDataCount );` / `Minimum supported client : Windows 10, version 1709 [desktop apps only]` | `GetGeoInfoEx` 在 Win7 不可用 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getgeoinfoex |
| GE09 | `A 32-bit signed number that uniquely identifies a geographical location.` / `it can be used as a key to access a database record that contains specific information about a country/region` | `LOCALE_IGEOID` 常量语义 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/intl/locale-igeoid |
| GE10 | `打开定位服务后,它将结合使用全球定位服务 (GPS) ､附近的无线接入点和路由器､手机信号塔､IP 地址或默认位置来确定设备的位置` | Windows 定位服务使用 GPS/WiFi/蜂窝/IP/默认位置 | 已证实 | https://support.microsoft.com/zh-cn/windows/windows-位置服务和隐私 |
| GE11 | `关闭定位服务后,Windows 和应用将无法访问设备位置` | 用户可关闭 | 已证实 | https://support.microsoft.com/zh-cn/windows/windows-位置服务和隐私 |

## 位置判定与用户要求的边界

| 编号 | 项 | 四值 | 依据 |
| --- | --- | --- | --- |
| P01 | 用户要求「发现玩家的物理位置」且「不能使用那种网络连接打法，因为那有可能误伤加速器，vpn」 | 已证实 | docs/spec/11-features-input.txt 开头段 |
| P02 | GE10 的 IP 地址定位属于网络探测，落在 P01 排除范围 | 已证实 | GE10 |
| P03 | `GetUserGeoID` / `GetGeoInfoW` / `LOCALE_IGEOID` 读的是用户或系统设定的区域标识，不是设备物理位置 | 已证实 | GE02、GE09 |
| P04 | Win7 上存在任何不联网、可判定设备物理位置的系统 API | 未证实 | 一手文档未给出；GE02 明确未设置时返回 `GEOID_NOT_AVAILABLE` |
| P05 | 离线账户限制按「物理位置」判定的可实现方案 | 未证实 | 依赖 P04 |
| P06 | 用户允许该判定在正版登录后放行、在中国大陆地区恢复正常 | 已证实 | docs/spec/11-features-input.txt 开头段 |
| P07 | 替代口径：按用户或系统区域设置判定，需用户确认是否接受 | 未批准 | P03 与 P01 语义不同 |

处置：P01 与 P03 的语义差已登记，不把区域设置冒充物理位置写进实现；`src/` 为空。按 docs/spec/00-requirements.txt:3 与 :249，该项在进入实现前需用户拍板。

## Win7 与 Rust 官方目标的硬冲突

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| RW01 | `i686-pc-windows-msvc 32-bit MSVC (Windows 10+, Windows Server 2016+, Pentium 4)` | 32 位 Tier 1 目标最低 Win10 | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| RW02 | `x86_64-pc-windows-msvc 64-bit MSVC (Windows 10+, Windows Server 2016+)` | 64 位 Tier 1 目标最低 Win10 | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| RW03 | `aarch64-pc-windows-msvc ARM64 Windows MSVC` / `aarch64-pc-windows-gnullvm ARM64 MinGW (Windows 10+), LLVM ABI` | ARM64 目标最低 Win10 | 已证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| RW04 | `Version 1.78.0 (2024-05-02) ... Target changes: Windows tier 1 targets now require at least Windows 10` | Rust 1.78 起 Tier 1 Windows 目标要求 Win10 | 已证实 | https://doc.rust-lang.org/releases.html |
| RW05 | `x86_64-win7-windows-msvc` / `Tier: 3` / `Windows 目标继续支持 Windows 7` / `Rust 不为此目标发布预编译的工件 ... 使用 build-std 或类似工具构建您自己的副本` | Win7 目标为 Tier 3，需自建 std | 已证实 | https://doc.rust-lang.net.cn/1.85.0/rustc/platform-support/win7-windows-msvc.html |
| RW06 | `支持 core､alloc､std 和 test 的所有功能` / `目标维护者 @roblabla` / `兼容的 C 代码可以使用 MSVC 的 cl.exe 或 LLVM 的 clang-cl 构建` / `xwin splat --output winsdk` | Tier 3 目标能力与工具链要求 | 已证实 | https://doc.rust-lang.net.cn/1.85.0/rustc/platform-support/win7-windows-msvc.html |
| RW07 | 当前上游 Rust 版本 `1.99.1` | 高于 1.78 | 已证实 | https://api.github.com/repos/rust-lang/rust/releases/latest |
| RW08 | `aarch64-win7-windows-msvc` 目标 | 平台支持页未列出；ARM64 Windows 为 Win10+ | 未证实 | https://doc.rust-lang.org/rustc/platform-support.html |
| RW09 | VxKex 是 `a free, open‑source set of API extensions for Windows 7 that lets many modern apps built for Windows 8/10/11 run on the older OS by injecting compatibility DLLs without modifying system files` | Win7 API 扩展层 | 已证实 | https://vxkex.com/ |
| RW10 | VxKex 仓库 `https://github.com/i486/VxKex`，启用方式为程序属性页勾选 | 外部件，不随本项目分发 | 已证实 | https://www.nihendiao.com/?p=4536/ |
| RW11 | VxKex 对 Rust 编译产物、WebView2、加载器进程的兼容范围 | 未证实 | 一手列表未取得 |
| RW12 | 开发者经验：Tier 3 目标需 `build-std`、PE 导入表重定向、`clang-cl` / `lld-link` / `xwin` | 已证实 | https://tixbay.net/?m=20260702/ |

## 冲突结论（需求 :3、:249）

| 编号 | 用户要求 | 一手事实 | 四值 |
| --- | --- | --- | --- |
| C01 | 从 Win7 开始兼容 | Rust 1.78 起 Tier 1 Windows 目标要求 Win10；Win7 仅 Tier 3 且无预编译 std | 已证实（冲突成立） |
| C02 | 支持 32 位与 64 位 | `i686-pc-windows-msvc` 与 `x86_64-pc-windows-msvc` 均为 Win10+ | 已证实（冲突成立） |
| C03 | 支持多个处理器架构「我全都要」 | Windows 侧 Rust 官方目标为 i686 / x86_64 / aarch64；ARM64 最低 Win10 | 已证实（部分冲突） |
| C04 | Win7 + ARM64 同时支持 | RW03 与 RW08 交集为空 | 已失败 |
| C05 | Win7 默认进入轻量模式 | 用户当轮指令，与 docs/spec/00-requirements.txt:8 的 2GB 首次默认并列登记 | 已证实 |
| C06 | Win7 声明页文案「win7系统已经老旧，你已进入轻量模式，如使用其他高级功能，我们建议使用VxKex支持」 | 用户指定原文，落在统一调度器启动声明页 | 已证实 |

可行路径（均未批准、未实现）：

| 路径 | 依据 | 四值 |
| --- | --- | --- |
| 走 `*-win7-windows-msvc` Tier 3 + `build-std` 自建工具链 | RW05、RW06、RW12 | 未证实 |
| 走 VxKex 让 Win10+ 产物在 Win7 运行 | RW09、RW10、C06 文案 | 未证实 |
| 固定旧版 Rust 工具链 | RW04 | 未证实 |
| 拆分产物：Win7 用非 Rust 组件，Win10+ 用 Rust | 需求 :43 形态为 Rust | 未证实 |

按 docs/spec/00-requirements.txt:249，C01-C04 进入构建前需用户拍板；`src/` 保持为空，未生成 Cargo.toml、build.rs、target spec。

## DLL 加载的 Win7 边界

| 编号 | 原文 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| DL01 | `BOOL SetDefaultDllDirectories( [in] DWORD DirectoryFlags );` | 函数签名 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-setdefaultdlldirectories |
| DL02 | `LOAD_LIBRARY_SEARCH_DEFAULT_DIRS 0x00001000` / `This value represents the recommended maximum number of directories an application should include in its DLL search path.` | 标志值与语义 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-setdefaultdlldirectories |
| DL03 | `Minimum supported client: Windows 8 [desktop apps only], KB2533623 on Windows 7, Windows Server 2008 R2, Windows Vista, and Windows Server 2008` | Win7 需 KB2533623 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-setdefaultdlldirectories |
| DL04 | `Windows 7 ... To call this function in an application, use the GetProcAddress function to retrieve its address from Kernel32.dll. KB2533623 must be installed on the target platform.` | Win7 需动态取址 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-setdefaultdlldirectories |
| DL05 | `If the function fails, the return value is zero. To get extended error information, call GetLastError.` | 失败返回与诊断 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-setdefaultdlldirectories |

docs/checklists/windows-errors.md W24 的 KB2533623 与 `GetProcAddress` 由 DL03、DL04 补为一手原文。

## 011 新增来源

| 编号 | URL | 用途 | 结果 |
| --- | --- | --- | --- |
| P17 | https://learn.microsoft.com/en-us/windows/win32/api/versionhelpers/nf-versionhelpers-iswindows7orgreater | OS01-OS02 | 200 |
| P18 | https://learn.microsoft.com/zh-cn/windows/desktop/SysInfo/targeting-your-application-at-windows-8-1 | OS03-OS04 | 200 |
| P19 | https://learn.microsoft.com/en-us/windows/win32/api/sysinfoapi/nf-sysinfoapi-getnativesysteminfo | AR01-AR03 | 200 |
| P20 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getusergeoid | GE01-GE03 | 200 |
| P21 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getgeoinfow | GE04-GE05 | 200 |
| P22 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/ne-winnls-sysgeotype | GE06-GE07 | 200 |
| P23 | https://learn.microsoft.com/en-us/windows/win32/api/winnls/nf-winnls-getgeoinfoex | GE08 | 200 |
| P24 | https://learn.microsoft.com/en-us/windows/win32/intl/locale-igeoid | GE09 | 200 |
| P25 | https://support.microsoft.com/zh-cn/windows/windows-位置服务和隐私 | GE10-GE11 | 200 |
| P26 | https://doc.rust-lang.org/rustc/platform-support.html | RW01-RW03 | 200 |
| P27 | https://doc.rust-lang.org/releases.html | RW04 | 200 |
| P28 | https://doc.rust-lang.net.cn/1.85.0/rustc/platform-support/win7-windows-msvc.html | RW05-RW06 | 200 |
| P29 | https://api.github.com/repos/rust-lang/rust/releases/latest | RW07 | 200 |
| P30 | https://vxkex.com/ | RW09 | 200 |
| P31 | https://www.nihendiao.com/?p=4536/ | RW10 | 200 |
| P32 | https://tixbay.net/?m=20260702/ | RW12 | 200 |
| P33 | https://learn.microsoft.com/en-us/windows/win32/api/libloaderapi/nf-libloaderapi-setdefaultdlldirectories | DL01-DL05 | 200 |

## 未证实 / 受阻

| 项 | 四值 |
| --- | --- |
| 应用清单中版本声明的具体字段 | 未证实 |
| `wProcessorArchitecture` 常量值与 ARM64 宿主区分方案 | 未证实 |
| Win7 上判定设备物理位置的非网络系统 API | 未证实 |
| `aarch64-win7-windows-msvc` 目标 | 未证实 |
| VxKex 对本项目产物链的兼容范围 | 未证实 |
| Tier 3 自建工具链在本项目的可复现构建 | 未证实 |
| `https://doc.rust-lang.org/rustc/platform-support/windows.html` 直抓 | 受阻，页面不可访问，改用 P26 平台支持总页 |

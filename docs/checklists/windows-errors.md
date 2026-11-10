# Windows 防错清单

| 编号 | 项 | 约束 |
| --- | --- | --- |
| W01 | MAX_PATH | 默认 260 字符；扩展路径用 `\\?\`；需 `LongPathsEnabled=1` 与应用清单 `longPathAware` |
| W02 | 编码 | Windows 路径与命令行参数为 UTF-16；用 `args_os()`、`OsString`、`PathBuf` |
| W03 | `args()` panic | 无效 UTF-8 触发 panic，改用 `args_os()` |
| W04 | Win32 宽字符 | 使用 `W` 后缀结构与函数；`dwSize` 必须赋值 |
| W05 | UTF-16 转 String | `String::from_utf16_lossy` 后按 `\0` 截断 |
| W06 | WebView2 | 运行时依赖需检测；缺失时降级到外置浏览器 / 连接码 |
| W07 | UAC | 不假设管理员权限；写入系统目录前检测并降级到用户目录 |
| W08 | 路径集中 | 所有路径经单一模块生成，不散落 `C:\` 字面量 |
| W09 | 盘符大小写 | 不假设盘符大小写敏感性与当前工作目录 |
| W10 | 文件占用 | Minecraft 运行时文件可能被占用，写入前检测句柄占用 |
| W11 | 中文路径 | 全链路按 `OsStr` 处理，JSON 配置按 UTF-8 读写并显式声明编码 |
| W12 | 进程残留 | 轻量启动器在游戏运行期间无常驻进程；退出前回收子进程句柄 |
| W13 | 超时 | 网络、进程启动、RCON、IPC 均设超时，不无限等待 |
| W14 | 注册表 | 读取失败按二级降级处理并写诊断行 |
| W15 | 编码回显 | 日志输出统一 UTF-8；控制台代码页差异不进入判断逻辑 |
| W16 | 长路径清单 | `embed-resource` + `.rc` + build script，构建产物需带清单 |
| W17 | 杀软误报 | 不写死排除项；诊断包记录已加载模块列表 |
| W18 | 单文件发布 | 未确定工具链前不写死目标三元组 |
| W19 | WebView2 检测 | 检查 pv (REG_SZ) 于 4 个注册表位置；缺失、空字符串或 0.0.0.0 时降级外置浏览器 / 连接码 |
| W20 | server.properties 写入 | UTF-8，保留 # 注释，Windows 行尾 CRLF，启动时重新生成 |
| W21 | 外部字体 CDN | 加载失败走本地字体栈，二级降级并写诊断行；不阻塞窗口渲染 |
| W22 | 窗口拖拽 CSS | -webkit-app-region 仅适用于 webview 桌面壳；无 WebView2 时不加载该设计稿 |
| W23 | DLL 预加载 | SetDllDirectory 非空路径会禁用安全搜索模式；用 SetDefaultDllDirectories + LOAD_LIBRARY_SEARCH_DEFAULT_DIRS |
| W24 | SetDefaultDllDirectories 最低系统 | Windows 8 / Server 2012；Windows 7、2008 R2、Vista、2008 需 KB2533623 并用 GetProcAddress |
| W25 | 进程参数 | std::process 参数不经 shell；`cmd.exe` / `.bat` 非标准解码，不可信输入不走 raw_arg |
| W26 | 进程超时 | std::process 页面未提供超时 API；超时由外层实现，不假设 wait 自带超时 |
| W27 | WebView2 进程组 | 单 browser process + 多 renderer 绑定同一 user data folder；多个 folder 各建一组进程 |
| W28 | MSVC 运行库部署 | central / local / static linking 三种；未选定工具链前不写死目标三元组，关联 W18 |
| W29 | DPAPI 用户绑定 | CryptProtectData 默认绑定同一用户登录凭据与同一计算机；加解密需同一可选熵 |
| W30 | DPAPI 机器标志 | 不设置 CRYPTPROTECT_LOCAL_MACHINE；该标志使本机任意用户可解密 |
| W31 | CredWriteW 会话绑定 | 凭据关联当前令牌登录会话，令牌用户 SID 被禁用时失败；不假设跨登录会话可用 |
| W32 | 凭据不落明文 | 凭据不进入日志、诊断包、配置快照、提交与远端 |
| W33 | Win7 与 Rust Tier 1 | Rust 1.78 起 Windows Tier 1 目标要求 Win10；Win7 走 Tier 3 `*-win7-windows-msvc` 且需 build-std |
| W34 | Win7 DLL 安全搜索 | SetDefaultDllDirectories 需 KB2533623，用 GetProcAddress 从 Kernel32.dll 动态取址 |
| W35 | OS 版本判定 | 用 IsWindows7OrGreater；GetVersionEx 已弃用，未面向 Win8.1+ 时返回 6.2 |
| W36 | 架构判定 | GetNativeSystemInfo 在 WOW64 与模拟架构下返回模拟值，不直接等同宿主架构 |
| W37 | 多架构产物 | i686 / x86_64 / aarch64 候选；ARM64 Windows 最低 Win10，Win7 无 ARM64 |
| W38 | 本地监听 | 绑定回环地址，防火墙入站仅允许 localhost；服务器 AI API 为用户指定例外 |
| W39 | 位置判定 | 不走 IP 地理定位；GetUserGeoID 未设置时返回 GEOID_NOT_AVAILABLE，不等于物理位置 |
| W40 | GetGeoInfoEx | 最低 Win10 1709，Win7 不可用；Win7 侧只用 GetUserGeoID / GetGeoInfoW |
| W41 | eula.txt | 首次启动生成 eula=false；改为 eula=true 前服务端立即退出；官方页 https://www.minecraft.net/en-us/eula |
| W42 | server-icon.png | 64×64 PNG，放服务端工作目录，需重启加载 |
| W43 | ops.json 运行期写入 | 服务端启动时读入内存，命令变更时整体回写；运行期手改会被静默覆盖 |
| W44 | Java 版本 | Java 8 / 16 / 17 / 21 / 25 对应 MC 版本段不同，按版本自动推荐 |
| W45 | UPnP IGD | RFC 6886 记载可被用于改网关 DNS；NAT-PMP 已被 PCP 取代，默认开启与否待拍板 |

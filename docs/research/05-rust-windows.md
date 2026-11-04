# Rust 桌面栈与 Windows 运行时

检索日期：2026-11-05
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| wry 引擎 | Windows 使用 WebView2 | 已证实 | https://github.com/tauri-apps/wry |
| wry 窗口 | 使用 TAO 创建窗口并重新导出 | 已证实 | https://github.com/tauri-apps/wry |
| wry 许可证 | Apache-2.0 / MIT 双许可 | 已证实 | https://github.com/tauri-apps/wry |
| wry 最新 release | wry-v0.57.1，2026-10-23T11:20:46Z | 已证实 | https://api.github.com/repos/tauri-apps/wry/releases/latest |
| WebView2 检测 GUID | {F3017226-FE2A-4295-8BDF-00C3A9A7E4C5} | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution |
| 64 位 Windows 检测键 | HKLM\SOFTWARE\WOW6432Node\Microsoft\EdgeUpdate\Clients\{GUID}；HKCU\Software\Microsoft\EdgeUpdate\Clients\{GUID} | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution |
| 32 位 Windows 检测键 | HKLM\SOFTWARE\Microsoft\EdgeUpdate\Clients\{GUID} | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution |
| 检测值 | pv (REG_SZ)，需存在且大于 0.0.0.0 | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution |
| 未安装判定 | 键缺失，或值为 null / 空字符串 / 0.0.0.0 | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution |
| API 检测 | GetAvailableCoreWebView2BrowserVersionString 返回 nullptr 表示未安装 | 已证实 | https://learn.microsoft.com/en-us/microsoft-edge/webview2/concepts/deployment-distribution |
| WebView2 Runtime 最低版本 | 未核实 | 未证实 | 官方页面未给出单一最低版本号 |
| 固定版本嵌入 | 未核实 | 未证实 | 官方页面未抓取对应段落 |
| tao 许可证 | Apache-2.0，11323 字节 | 已证实 | docs/licenses/tao-LICENSE.txt:1-2 |
| egui 许可证 | Apache-2.0，10850 字节 | 已证实 | docs/licenses/egui-LICENSE.txt:1-3 |
| slint 许可证 | 三许可清单 Royalty-free 2.0 / GPLv3 / Commercial | 已证实 | docs/licenses/slint-LICENSE.txt:15-22 |
| slint 三许可全文 | LICENSES/ 目录内各全文未逐项取得 | 未证实 | docs/licenses/slint-LICENSE.txt:12-13 |
| iced 许可证 | MIT，1073 字节 | 已证实 | docs/licenses/iced-LICENSE.txt:3-10 |
| MAX_PATH | 260 字符 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation |
| 扩展长度前缀 | \\?\，上限 32767 字符 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation |
| 注册表项 | HKLM\SYSTEM\CurrentControlSet\Control\FileSystem LongPathsEnabled REG_DWORD = 1 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation |
| 应用清单 | 必须包含 longPathAware | 已证实 | https://learn.microsoft.com/en-us/windows/win32/fileio/maximum-file-path-limitation |
| 嵌入清单方式 | embed-resource + .rc + build script | 未证实 | 二手实践，完整 URL 未取得 |
| Windows 路径编码 | UTF-16，Unix 为原始字节 | 已证实 | https://doc.rust-lang.org/std/ffi/index.html |
| args_os() | 不做 UTF-8 校验，返回 OsString | 已证实 | https://doc.rust-lang.org/std/env/fn.args_os.html |
| args() | 无效 UTF-8 会 panic | 已证实 | https://doc.rust-lang.org/std/env/fn.args.html |
| Path / PathBuf | 直接接受 &OsStr / OsString | 已证实 | https://doc.rust-lang.org/std/path/struct.Path.html |
| Win32 宽字符 | PROCESSENTRY32W、Process32FirstW、Process32NextW，dwSize 必须设置 | 已证实 | https://learn.microsoft.com/en-us/windows/win32/api/tlhelp32/ns-tlhelp32-processentry32w |
| UTF-16 转换 | String::from_utf16_lossy 后按 \0 截断 | 已证实 | https://doc.rust-lang.org/std/string/struct.String.html |
| Rust Command Windows 参数转义规则 | 未核实 | 未证实 | 官方原文未取得 |
| 单文件发布工具链 | 未确定 | 受阻 | cmd: rustc --version → command not found；cargo --version → command not found |
| 本地库加载规则 | 未核实 | 未证实 | 官方原文未取得 |
| Rust 最新 release tag | 1.99.1，2026-10-16T04:47:44Z | 已证实 | https://api.github.com/repos/rust-lang/rust/releases/latest |
| static.rust-lang.org 直连 | 403 policy_default_denied | 受阻 | cmd: curl https://static.rust-lang.org/dist/channel-rust-stable.toml → 403 |

## 005 补证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| web_fetch learn.microsoft.com WebView2 distribution | 200，pv (REG_SZ) 与 4 个注册表位置 | 已证实 |
| GET /repos/tauri-apps/wry/releases/latest | 200，wry-v0.57.1 | 已证实 |
| GET /repos/rust-lang/rust/releases/latest | 200，1.99.1 | 已证实 |
| GET /repos/{tao,egui,slint,iced}/license | 200，4 份全文落盘 | 已证实 |

约束：
- 路径集中在单一模块，不散落硬编码。
- 外部输入用 OsString 承接，禁止 unwrap() 兜底。
- 长路径清单与注册表项不作为默认环境假设，需检测后降级。
- WebView2 缺失时降级到外置浏览器或连接码。

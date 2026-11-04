# Rust 桌面栈与 Windows 运行时

检索日期：2026-11-04

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| wry 引擎 | Windows 使用 Microsoft Edge Chromium 提供的 WebView2 | 已证实 | github.com/tauri-apps/wry README |
| wry 窗口 | 使用 TAO 创建窗口并重新导出 | 已证实 | 同上 |
| wry 许可证 | Apache-2.0 / MIT 双许可 | 已证实 | 同上 |
| WebView2 Runtime 最低版本 | 未核实 | 未证实 | 官方页面未抓取 |
| WebView2 检测注册表键 | 未核实 | 未证实 | 同上 |
| 固定版本嵌入 | 未核实 | 未证实 | 同上 |
| egui / slint / iced 对比 | 未取得许可证全文、MSRV、渲染方式、体积原文 | 未证实 | 无一手原文 |
| tao 许可证 | 未取得原文 | 未证实 | 无一手原文 |
| MAX_PATH | 260 字符 | 已证实 | learn.microsoft.com maximum-file-path-limitation |
| 扩展长度前缀 | `\\?\`，上限 32767 字符 | 已证实 | 同上 |
| 注册表项 | `HKLM\SYSTEM\CurrentControlSet\Control\FileSystem LongPathsEnabled` REG_DWORD = 1 | 已证实 | 同上 |
| 应用清单 | 必须包含 `longPathAware` | 已证实 | 同上 |
| 嵌入清单方式 | `embed-resource` crate + `.rc` + build script | 已证实 | DEV Community 长路径实践 |
| Windows 路径编码 | UTF-16，Unix 为原始字节 | 已证实 | Rust FAQ OsStr / OsString |
| `args_os()` | 不做 UTF-8 校验，返回 `OsString` | 已证实 | 同上 |
| `args()` | 无效 UTF-8 会 panic | 已证实 | 同上 |
| `Path`/`PathBuf` | 直接接受 `&OsStr`/`OsString` | 已证实 | 同上 |
| Win32 宽字符 | `PROCESSENTRY32W`、`Process32FirstW`、`Process32NextW`，`dwSize` 必须设置 | 已证实 | TrainSec Windows System Programming In Rust |
| UTF-16 转换 | `String::from_utf16_lossy` 后按 `\0` 截断 | 已证实 | 同上 |
| Rust `Command` Windows 参数转义规则 | 未核实 | 未证实 | 官方原文未取得 |
| 单文件发布工具链 | 未确定 | 受阻 | 无 `.cargo/config.toml`、无构建配置 |
| 本地库加载规则 | 未核实 | 未证实 | 官方原文未取得 |

约束：
- 路径集中在单一模块，不散落硬编码。
- 外部输入用 `OsString` 承接，禁止 `unwrap()` 兜底。
- 长路径清单与注册表项不作为默认环境假设，需检测后降级。

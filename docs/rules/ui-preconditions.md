# UI 宿主与崩溃分析前置条件清单（041）

| 编号 | 前置项 | 当前四值 |
| --- | --- | --- |
| L1 | Q-041 的 Win7 UI 路线拍板（A / B / C） | 未证实（待用户答复） |
| L2 | 选一条 UI 宿主并完成 vendor（wry / tao / slint 三条已判不成立） | 不成立 / 未证实 |
| L3 | Win7 的 WebView2 Runtime 109 固定版兼容性、SDK ≥1.0.1519.0 的边界 | 未证实 / 受阻 |
| L4 | UI 宿主各平台分支的 C/系统库（webkit2gtk、gtk、windows 0.61、objc2、jni/ndk） | 未证实 |
| L5 | 句柄互操作类型层（raw-window-handle） | **已落地（041）** |
| L6 | 崩溃分析：sentry-native 的 CMake + C++17 + MSVC2022 + zlib + Crashpad/Breakpad | 未证实 / 不成立 |
| L7 | Win10 以下「应支持但未自动测试」的运行时验证、`.pdb` / Clang 工具链 | 受阻 |
| L8 | DSN 用户自填、脱敏默认开、发送前确认、诊断包落盘 | 未启动 |
| L9 | 插件 ABI 的 UI 扩展点、核心槽位锁定（020）与句柄归属 | 未启动 |
| L10 | i18n `.ftl` 落地、lucide 图标、纸质主题进入实现 | 未启动 |
| L11 | 整页 UX HTML + PNG 演示 | 已落地（017–020，未确认） |
| L12 | 手感确认后再写界面实现（015 闸门） | 未证实（待用户反馈） |

| 项 | 值 |
| --- | --- |
| 本轮已落地 | L5；L11 沿用既有演示 |
| 硬约束 | L1 未拍板前不引 UI 宿主；L6–L7 未闭环前不引崩溃分析；不把 WebView2 在 Win7 的终止支持写成「应该能跑」 |
| 界面 | 设置页不新增任何「未实现」标签，前置状态只在文档登记 |

一手来源：`docs/research/24-ui-host-win7-and-crash-stack.md`、`docs/decisions/041-ui-crash-stack-check-and-window-handle.md`。

# Q-041：Win7 与正常模式 UI 的取舍（待你拍板）

## 冲突

011 定的是「Win7 起兼容、多架构」。Microsoft 官方：Edge 109 / WebView2 Runtime 109 是最后支持 Win7 / 8.1 的版本，SDK ≥1.0.1519.0 不再支持 Win7，109 之后无安全更新，Fixed >109 在 Win7 上无法启动；Microsoft Learn 的 WebView2 支持列表只剩 Win10 1709+ / Win11 / Server 2016+。`wry` 的 Windows 分支用 `webview2-com 0.38` + `windows 0.61`，属新 SDK 线。

## 三个选项

| 编号 | 做法 | 后果 |
| --- | --- | --- |
| Q1-A | 正常模式限定 Win10+；Win7 只跑轻量模式与无头模式 | 与官方支持一致，最稳；Win7 用户拿不到那套完整界面 |
| Q1-B | Win7 用固定版 WebView2 Runtime 109 | 能跑旧界面，但 2023 年后无安全更新，且 `wry` 新 SDK 未必兼容 109，需要额外验证 |
| Q1-C | 换非 WebView2 的 UI 宿主（slint software renderer 等） | 绕开运行时，但 slint 1.18.1 是 edition 2024 + 大闭包，与 Win7 Tier 3 的冲突仍未证实 |

## 共同约束

| 编号 | 项 |
| --- | --- |
| Q1-01 | 三个选项都不改 020 的「设置 / 关于锁定在核心槽位」，插件只往扩展区加 |
| Q1-02 | 轻量模式继续不加载任何 UI 宿主（016 / 041 U47） |
| Q1-03 | 无论选哪个，动界面前先出整页 UX HTML 与 PNG，按 015 闸门等手感确认 |
| Q1-04 | 本轮不替你选；`src/` 里 `HostSurface` 只是句柄类型层，不代表任何一选项已启用 |

状态：待答复。不写进实现。

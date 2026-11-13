# lucide 图标系统

| 项 | 值 |
| --- | --- |
| 编号 | F019-02 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 019 |
| 依据 | docs/decisions/019-ux-logic-lucide.md D01-D02；THIRD-PARTY-NOTICES.md |

## 怎么运作

`assets/icons/lucide-subset.svg` 是 88 枚 lucide 一手 SVG 的离线 sprite，逐枚 `<symbol id="i-<name>" viewBox="0 0 24 24">`。`assets/icons/lucide-manifest.json` 记录每枚图标名、GitHub blob SHA 与官方来源 URL。`demos/ui-full-kcu-paper.html` 把 sprite 内联进 body，CSS 类 `.li` 统一 16px、currentColor、2px 描边、圆角端点；导航 / 统计 / 标题栏分别覆写尺寸。全站字符图标清零，图标名缺失数为 0。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；未进 `src/` |
| 输入 | `#i-<name>` 引用 |
| 输出 | 88 枚矢量图标，深浅主题自动换色 |
| 错误路径 | 引用不存在的 symbol 时留空，扫描脚本判未证实 |
| 空值 | 无图标处留文字，不用占位字符 |
| 超时 | 不涉及 |
| 编码 | UTF-8 SVG 路径 |
| 排除项 | 外部 CDN、图标字体、全量 sprite、品牌 logo |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `<use href="#i-<name>">` | SVG 引用 | 图标名 | 图形 | 未知名为空 |
| `ic(n)` | 函数 | 图标名 | SVG 字符串 | 无 |
| `assets/icons/lucide-manifest.json` | 数据 | 无 | 88 条来源记录 | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo / assets.icons |
| 模块路径 | assets/icons/lucide-subset.svg、assets/icons/lucide-manifest.json、demos/ui-full-kcu-paper.html |
| 扩展点 | 新增图标须同步 sprite、manifest、许可页计数 |
| 关键抽象 | K08 UiFrame（仍未进实现） |
| 依赖 | 无运行时依赖 |
| 约束 | 只打包用到的图标；遵循 lucide SVG 约定；ISC + Feather MIT 双许可登记 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 任意界面 | 看导航、按钮、状态栏 | 线性图标与文字同色，深浅主题一致 |
| 深色主题 | 切换 | 图标随 `currentColor` 自动变浅 |
| 关于 → 第三方许可 | 看 Lucide 行 | 许可证、版权、用途、来源、构建状态可见 |

## 性能

| 项 | 值 |
| --- | --- |
| sprite 体积 | 约 19KB，内联一次 |
| 网络 | 0 次请求，无字体下载 |
| 渲染 | SVG use 引用，无 JS 逐枚绘制 |
| 测量命令 | `wc -c assets/icons/lucide-subset.svg` |
| 四值 | 已证实 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `grep -c '<symbol'` | 88 | 已证实 |
| 图标引用覆盖率扫描 | missing 0 | 已证实 |
| 字符图标残留扫描 | 0 | 已证实 |
| `! grep -rE 'https?://' demos/ui-full-kcu-paper.html` | exit 0 | 已证实 |

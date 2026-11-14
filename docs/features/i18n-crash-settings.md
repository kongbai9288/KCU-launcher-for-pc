# i18n 切换与崩溃反馈设置

| 项 | 值 |
| --- | --- |
| 编号 | F023-02 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 023 |
| 依据 | docs/decisions/023-architecture-answers.md；docs/research/20-i18n-crash-identity.md |

## 怎么运作

界面文案统一走 `tr(key, fallback)`，中文在演示层作缺资源兜底；标题栏「中 / EN」与设置 → 常规 → 界面语言都能切，切换不重启、不丢当前视图、不白屏。日志与 `[KCU]` 诊断行保持英文线格式，不进字典。设置 → 崩溃反馈给出记录开关、接收地址、脱敏、诊断包位置、看最近一次、导出；默认不记录、脱敏开、发送前二次确认、不填地址只落本地。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `ui.demo / i18n + settings.crash` |
| 输出 | 界面渲染、诊断行、截图证据 |
| 错误路径 | 缺资源回退中文；改名取消 0 副作用；崩溃上报取消 0 外发 |
| 空值 | 无服务器给添加入口；无 dump 给「看最近一次」空态 |
| 超时 | 单台 deadline 沿用 022 |
| 排除项 | 名称不进路径；日志不本地化 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `tr(k, fb)` / `applyI18n()` | 函数 | key / 兜底 | 本地化文本 | 缺 key 回退 fb |
| `setLang(l)` / `btnLang` | 函数 / 按钮 | locale | 整页重渲染 | 无 |
| `setLang` 下拉 | 设置 | zh-CN / en-US | 同上 | 写盘失败保留旧值 |
| `setCrashOn` / `setCrashAddr` / `setCrashMask` | 设置 | 值 | 崩溃策略 | 无 |
| `crashView` / `crashExport` | 按钮 | 无 | 预览 / 本地导出 | 无 dump 给空态 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo / i18n、ui.demo / settings.crash（023 Q2 / Q5） |
| 模块路径 | demos/ui-full-kcu-paper.html、docs/design/i18n-policy.md、docs/design/crash-reporting.md、41-i18n-en.png、42-settings-crash.png |
| 扩展点 | 插件可追加 `.ftl` 语言包与崩溃上下文，不覆盖核心 domain |
| 关键抽象 | K03 Diagnostics、K08 UiFrame |
| 依赖 | 演示层无；实现层 fluent / i18n-embed / sentry-minidump 均为候选未进构建 |
| 约束 | 默认不外发；脱敏默认开；许可登记后进构建 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 标题栏 中 / EN | 点一下 | 整页切换 |
| 设置 → 常规 | 选 English | 同上 |
| 设置 → 崩溃反馈 | 选只留本地 | 出错只落盘 |
| 看最近一次 | 点击 | 只读预览，可取消 |

## 性能

| 项 | 值 |
| --- | --- |
| 切换 | 一次遍历 550+ 标注点，无网络请求 |
| 资源 | 演示层字典常驻；实现层 `.ftl` 按需装载 |
| 崩溃 | 默认 0 外发、0 常驻上报进程 |
| 测量命令 | `grep -c 'data-i18n='` 与 `node new Function` |
| 四值 | 已证实（演示层） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `41-i18n-en.png` | 导航 / 设置 / 按钮英文可见 | 已证实 |
| `42-settings-crash.png` | 崩溃反馈分组可见 | 已证实 |
| 真实 `.ftl` 集成、真实 minidump、真实上报 | 未实测 | 受阻 |

# 服务器状态设置

| 项 | 值 |
| --- | --- |
| 编号 | F020-04 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 020 |
| 依据 | docs/decisions/020-nav-slots-settings.md；docs/design/ |

## 怎么运作

状态取 SLP 1.7+ 的 JSON 字段：`version.name/protocol`、`players.max/online/sample`、`description`（text component）、`favicon`（64×64 PNG base64）、`enforcesSecureChat`。6 类状态：在线、维护中、离线、满员、私有、自定义。来源可切 SLP + 手动覆盖 / 仅手动 / 插件提供；探测间隔 60s、超时 3s、缓存 60s 失败标灰；显示位置首页推荐卡、服务器列表、状态栏、右键菜单多选；状态文案与颜色可自定义；变更写 `[KCU]` 诊断行。超时、协议禁用、缺 `version.name`、裸字符串 `description`、favicon 尺寸不符各有降级路径。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `ui.demo / settings.status` |
| 输出 | 界面证据与 `[KCU]` 诊断行 |
| 错误路径 | 冲突 / 失败 / 取消均可见，0 副作用扩散 |
| 空值 | 空态给入口，不显示空白 |
| 超时 | 按设置项可配 |
| 编码 | UTF-8 |
| 排除项 | 源稿品牌、外部 CDN、未证实字段 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `#view=settings&tab=status` | 路由 | 无 | 状态设置分组 | 无 |
| `core.status.*` | 设置 ID | 用户值 | 状态判定与显示 | 超时标灰 |
| `data-v="servers"` | 路由 | 无 | 服务器推荐与状态入口 | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo / settings.status（020 D11） |
| 模块路径 | docs/design/server-status.md、30-settings-status.png、21-servers.png |
| 扩展点 | `plugin.status.*` 可提供状态来源 |
| 关键抽象 | K03 Diagnostics、K08 UiFrame（仍未进实现） |
| 依赖 | 无 |
| 约束 | 失败回退缓存，不空白；不静默重试 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 设置 → 服务器状态 | 切探测方式、改间隔 | 写后即时生效 |
| 服务器页 | 看状态条 | 绿 / 金 / 灰点与上次探测时间 |
| 日志 | 看诊断行 | 状态变更可追溯 |

## 性能

| 项 | 值 |
| --- | --- |
| 并发 | 上限 3，慢源竞速取消 |
| 缓存 | 60s，有界 |
| 测量命令 | `grep -c 'core.status.' docs/design/server-status.md` |
| 四值 | 已证实（设计层；SLP 客户端未实现） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `demos/preview/30-settings-status.png` | 状态类型、显示位置、变更历史可见 | 已证实 |
| https://minecraft.wiki/w/Java_Edition_protocol/Server_List_Ping | SLP 字段一手原文 | 已证实 |

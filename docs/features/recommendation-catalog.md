# 推荐位目录与排序自定义

| 项 | 值 |
| --- | --- |
| 编号 | F020-03 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 020 |
| 依据 | docs/decisions/020-nav-slots-settings.md；docs/design/ |

## 怎么运作

10 处推荐位逐处定义：首页启动卡、首页推荐服务器、版本页、下载页、模组页、公告中心、加载器、Java、镜像源、插件。每处有推荐内容、默认权重、用户覆盖规则、缓存刷新口径、稳定设置 ID。推荐总控含总开关、权重可自定义、用户指定永远排第一、不感兴趣只降权不隐藏、来源本地 / 官方 / 插件三类可插拔、事件驱动 + 定时软刷新、5min 容量有界缓存。插件来源走 `plugin.rec.*`，不改 `core.rec.*` 权重口径。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `ui.demo / recommendations` |
| 输出 | 界面证据与 `[KCU]` 诊断行 |
| 错误路径 | 冲突 / 失败 / 取消均可见，0 副作用扩散 |
| 空值 | 空态给入口，不显示空白 |
| 超时 | 按设置项可配 |
| 编码 | UTF-8 |
| 排除项 | 源稿品牌、外部 CDN、未证实字段 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `data-v="recommendations"` | 路由 | 无 | 10 位总览表 | 无 |
| `#view=settings&tab=recommend` | 路由 | 无 | 推荐设置分组 | 无 |
| `REC_CATALOG` | 数据 | 无 | 10 行表格 | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo / recommendations（020 D10） |
| 模块路径 | docs/design/recommendation-catalog.md、35-recommendations.png、29-settings-recommend.png |
| 扩展点 | `plugin.rec.*` |
| 关键抽象 | K08 UiFrame（仍未进实现） |
| 依赖 | 无 |
| 约束 | 10 位统一口径，用户指定压过系统推荐 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 导航推荐位总览 | 看 10 行表 | 权重、覆盖、缓存、设置 ID 一目了然 |
| 设置 → 推荐与排序 | 改权重、看 @modified | 写后即时生效 |
| 首页推荐服务器卡 | 点全部服务器 | 进推荐位与权重口径页 |

## 性能

| 项 | 值 |
| --- | --- |
| 表格 | 10 行，一次渲染 |
| 网络 | 0 次远端请求 |
| 测量命令 | `grep -c 'core.rec.' docs/design/recommendation-catalog.md` |
| 四值 | 已证实 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `demos/preview/35-recommendations.png` | 10 行全可见 | 已证实 |
| `grep -c 'RC0'` docs/design/recommendation-catalog.md | 10 | 已证实 |

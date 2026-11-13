# 关于页第三方许可说明

| 项 | 值 |
| --- | --- |
| 编号 | F019-03 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 019 |
| 依据 | docs/decisions/019-ux-logic-lucide.md D07-D09；THIRD-PARTY-NOTICES.md |

## 怎么运作

关于页工具区一级按钮「查看第三方许可」直达 `licenses` 视图。七列表列出 16 组组件：项目 / 版本 / 许可证 / 版权 / 用途 / 来源 / 构建状态；按许可证分组 chip 筛选（ISC / MIT / Apache-2.0 / GPL 系 / NOASSERTION）。Lucide ISC 原文摘录与 Feather MIT 说明同页可见；插件动态追加、缺失处理、NOTICES 随发行物附带、服务条款与代码许可分开四条规则各有独立卡片。`THIRD-PARTY-NOTICES.md` 是同一份清单的发行物副本，离线可读。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；进入 `src/` 构建的第三方代码 0 项 |
| 输入 | 关于页按钮、导航、分组 chip、刷新 / 重新扫描 |
| 输出 | 七列表、原文摘录、时间戳、诊断行 |
| 错误路径 | 全文缺失给来源链接与「稍后」，不编造许可文本 |
| 空值 | 清单为空时明确写「未随包附带许可清单」 |
| 超时 | 不涉及 |
| 编码 | UTF-8 |
| 排除项 | 用 NOASSERTION 推断为无许可证；把文档层说成已使用 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `data-v="licenses"` | 路由 | 无 | 许可视图 | 无 |
| `renderLic()` | 函数 | 分组键 | 表格行 | 无 |
| `[data-lic]` | chip | 分组名 | 筛选后的表 | 无 |
| 插件动态追加 | 事件 | 插件元数据 5 字段 | 新增一行 | 缺失给来源链接 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo / legal.notices |
| 模块路径 | demos/ui-full-kcu-paper.html（licenses 视图）、THIRD-PARTY-NOTICES.md、docs/licenses/、assets/icons/lucide-manifest.json |
| 扩展点 | 插件加载后动态追加；依赖树变更后强制刷新清单 |
| 关键抽象 | K03 Diagnostics、K08 UiFrame（仍未进实现） |
| 依赖 | 无 |
| 约束 | 构建状态如实标注；服务条款与代码许可证分开；本项目 LICENSE 未生成 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 关于页 | 点「查看第三方许可」 | 七列表与分组筛选 |
| 许可页 | 点 ISC / MIT / Apache | 按许可证分组看组件 |
| 许可页 | 看构建状态列 | 区分演示层已使用、文档层、未生成 |
| 发行物 | 打开 THIRD-PARTY-NOTICES.md | 与界面同一份清单 |

## 性能

| 项 | 值 |
| --- | --- |
| 行数 | 16 组，一次渲染 |
| 网络 | 0 次请求，清单离线可读 |
| 测量命令 | `grep -c '<tr' demos/preview/index.md` 不适用；以视图截图为准 |
| 四值 | 已证实 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `test -f THIRD-PARTY-NOTICES.md` | 存在 | 已证实 |
| `grep -c 'data-lic=' demos/ui-full-kcu-paper.html` | 6 | 已证实 |
| `demos/preview/22-licenses.png` | 1440×900，七列表可见 | 已证实 |
| 逐组件许可证全文取得 | 13 组逐字副本已在 docs/licenses/ | 已证实 |
| 未取得全文的条目 | CopperGolemLauncher THIRD_PARTY_NOTICES 等 | 未证实 |

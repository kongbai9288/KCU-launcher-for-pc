# 上层实现第三方候选登记

| 项 | 值 |
| --- | --- |
| 编号 | F020-05 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 020 |
| 依据 | docs/decisions/020-nav-slots-settings.md；docs/design/ |

## 怎么运作

上层实现批准采用第三方代码。12 组候选逐项标层、候选项目、许可证、用途、LICENSE 全文状态、复制状态：tao + wry、slint、egui / iced、serde + serde_json、reqwest、tokio、semver、sha2、anyhow + thiserror、libloading、tauri-plugin-updater / self_update、rusqlite。全部标「候选 · 未进构建」；slint 三许可全文已取得，其余待逐项核对。复用规则 U01-U08 写进 `docs/design/upper-layer-stack.md`；关于页与 THIRD-PARTY-NOTICES.md 登记同一份清单；插件加载后动态追加插件许可信息。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `legal.notices / ui.demo.upperstack` |
| 输出 | 界面证据与 `[KCU]` 诊断行 |
| 错误路径 | 冲突 / 失败 / 取消均可见，0 副作用扩散 |
| 空值 | 空态给入口，不显示空白 |
| 超时 | 按设置项可配 |
| 编码 | UTF-8 |
| 排除项 | 源稿品牌、外部 CDN、未证实字段 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `data-v="upperstack"` | 路由 | 无 | 12 行候选表 | 无 |
| `UPPER` | 数据 | 无 | 关于页与候选页表格 | 缺失给来源链接 |
| 插件动态追加 | 事件 | 插件元数据 5 字段 | 新增许可行 | 不编造许可文本 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | legal.notices / ui.demo.upperstack（020 D13） |
| 模块路径 | docs/design/upper-layer-stack.md、THIRD-PARTY-NOTICES.md、15-about.png、37-upperstack.png |
| 扩展点 | 插件许可动态追加 |
| 关键抽象 | K03 Diagnostics、K08 UiFrame（仍未进实现） |
| 依赖 | 无新增 crate |
| 约束 | 取得 LICENSE 全文前不复制代码；构建状态如实标注 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 关于 → 完整候选清单 | 看 12 行表 | 许可证、用途、全文状态、复制状态 |
| 关于 → 许可清单 | 看七列表 | 与 NOTICES 同一份 |
| 许可页 | 点分组 chip | 按许可证筛选 |

## 性能

| 项 | 值 |
| --- | --- |
| 表格 | 12 行，一次渲染 |
| 网络 | 0 次远端请求 |
| 测量命令 | `grep -c '候选 · 未进构建' docs/design/upper-layer-stack.md` |
| 四值 | 已证实 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `demos/preview/37-upperstack.png` | 12 行候选全可见 | 已证实 |
| `test -f THIRD-PARTY-NOTICES.md` | 存在 | 已证实 |

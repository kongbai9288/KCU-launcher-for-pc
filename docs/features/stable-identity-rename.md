# 稳定标识、同名与改名

| 项 | 值 |
| --- | --- |
| 编号 | F023-01 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 023 |
| 依据 | docs/decisions/023-architecture-answers.md；docs/research/20-i18n-crash-identity.md |

## 怎么运作

每台服务器有不变的 `sid`（由规范化 `ip:port` 派生），显示名 `name` 可重复、可随时改。列表、缓存、连接记录、双击绑定全部按 `sid` 索引；目录 `C:\KCU\servers\<sid>\` 只含白名单字符。改名弹窗可取消 / ESC / × / 宿主关闭，确认后只写 `name`，写诊断行 `sid unchanged=true`，不移动目录、不重算权重、不触发重新探测。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `ui.demo / servers.identity` |
| 输出 | 界面渲染、诊断行、截图证据 |
| 错误路径 | 缺资源回退中文；改名取消 0 副作用；崩溃上报取消 0 外发 |
| 空值 | 无服务器给添加入口；无 dump 给「看最近一次」空态 |
| 超时 | 单台 deadline 沿用 022 |
| 排除项 | 名称不进路径；日志不本地化 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `srv.sid` | 字段 | `ip:port` | 稳定 ID | 地址冲突按 sid 幂等 |
| `openRename(s)` | 函数 | 服务器对象 | 改名弹窗 | 空名不保存 |
| `data-rename` | 按钮 | sid | 打开弹窗 | 无 |
| `data-lock` / `data-join` | 按钮 | sid | 锁定 / 进服 | 找不到 sid 忽略 |
| `srvNote(s)` | 函数 | 服务器对象 | 同名 / 范围外 / 连不上标签 | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo / servers.identity（023 Q1） |
| 模块路径 | demos/ui-full-kcu-paper.html、docs/design/stable-identity.md、39-servers-rename.png、40-servers-samenames.png |
| 扩展点 | 插件可补服务器来源，必须产出同样规范的 sid |
| 关键抽象 | K03 Diagnostics、K08 UiFrame（未进实现） |
| 依赖 | 无新增 crate；UUIDv5 实现层用 uuid crate |
| 约束 | 名称不进路径；大小写折叠；路径字符白名单 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 服务器列表 | 看两台同名 | 各自独立，带「同名」标签 |
| 名称旁铅笔 | 改名 | 只换显示名，记录与排序保留 |
| 双击 | 进服 | 按 sid 绑定上次实例 |

## 性能

| 项 | 值 |
| --- | --- |
| 排序 | 一次 sort，按 sid 无关缓存权重 |
| 内存 | 每条只多一个短字符串 |
| 磁盘 | 每服务器一个目录，不随改名增长 |
| 测量命令 | `grep -c "sid:'sv-"` = 10 |
| 四值 | 已证实（演示层） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `39-servers-rename.png` | 改名弹窗与同名标签可见 | 已证实 |
| `40-servers-samenames.png` | 两台同名各自延迟 | 已证实 |
| 真实 UUIDv5 / 真实目录写盘 | 未实测 | 受阻 |

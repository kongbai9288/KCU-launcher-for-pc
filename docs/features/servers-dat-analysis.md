# 游戏内服务器列表自动分析

| 项 | 值 |
| --- | --- |
| 编号 | F021-02 |
| 状态 | 已实现、已验证（演示层） |
| 轮次 | 021 |
| 依据 | docs/decisions/021-server-autoconnect.md；docs/design/server-list-logic.md |

## 怎么运作

只读扫描各实例目录下的 `servers.dat`（未压缩 NBT，游戏加过服或进过服才生成），解析 `servers` List 的 `name` / `ip` / `icon` / `hidden` / `acceptTextures`；区分可见列表、隐藏列表（最多 16 个、游戏不同步）、Quick Play 与直接连接落进隐藏列表的地址。默认导入可见与快速进入过的，隐藏列表可不导；文件不存在给空态，NBT 解析失败跳过该目录并可见提示，不影响其它实例。不写回、不覆盖玩家在游戏里加的服。

| 项 | 值 |
| --- | --- |
| 实现状态 | 演示层；`src/` 本轮无变化 |
| 输入 | `ui.demo / servers.scan` |
| 输出 | 界面证据与 `[KCU]` 诊断行 |
| 错误路径 | 连不上沉底、解析失败跳过、取消 0 副作用 |
| 空值 | 空态给添加服务器入口 |
| 超时 | 慢源竞速取消 |
| 编码 | UTF-8；MOTD 转义后显示 |
| 排除项 | 不写回 `servers.dat`、不自定义状态配色 |

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `srvScan` / `setSrvScan` | 按钮 | 无 | 读取结果与诊断行 | 文件不存在给空态 |
| `srvScanState` / `srvScanLog` | 状态 | 无 | 目录数、可见 / 隐藏 / 快速进入计数 | 解析失败跳过 |
| `settings&tab=status` | 路由 | 无 | 自动读取开关与导入范围 | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | ui.demo / servers.scan（021 D06） |
| 模块路径 | docs/research/18-server-list-autodiscovery.md、docs/design/server-list-logic.md、21-servers.png、30-settings-status.png |
| 扩展点 | 插件可补其它来源 |
| 关键抽象 | K03 Diagnostics |
| 依赖 | NBT 解析器为上层第三方候选，未进入构建 |
| 约束 | 只读；多实例隔离目录逐个扫 |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 服务器页 | 点重新读取 | 显示 3 个实例目录 / 可见 4 / 隐藏 2 / 快速进入 1 |
| 设置 → 服务器与连接 | 切自动读取、隐藏列表、快速进入 | 写后即时生效 |
| 没有加过服 | 打开文件 | 空态给添加服务器 |

## 性能

| 项 | 值 |
| --- | --- |
| 扫描 | 多目录串行，单目录失败不阻塞 |
| 内存 | 只保留列表条目，不载入完整 NBT 树 |
| 测量命令 | `grep -c 'servers.dat' docs/design/server-list-logic.md` |
| 四值 | 已证实（设计层） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| https://minecraft.wiki/w/Server_list_storage_format | NBT 结构一手原文 | 已证实 |
| 真实 `servers.dat` 解析 | 未实测 | 受阻 |

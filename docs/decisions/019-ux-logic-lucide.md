# 第 019 轮使用逻辑补全、lucide 图标与第三方许可页

| 项 | 值 |
| --- | --- |
| 编号 | 019 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 019 |
| 逐字指令 | docs/spec/19-round-019-instructions.txt，1 行 782 字节，SHA-1 `ad626f16ec7c6b763d7892951901e6b609042292` |
| 前序 | 018 纸质 UX 界面、20 视图、UX/流程 HTML 形态区分 |

## 决策

| 编号 | 项 | 值 | 依据 |
| --- | --- | --- | --- |
| D01 | 图标 | 全站替换为 lucide：88 枚图标取自 `lucide-icons/lucide` main 分支 `icons/*.svg` 一手 SVG，内联 sprite，无 CDN、无字体依赖；遵循 24×24 viewBox / `fill=none` / `stroke=currentColor` / `stroke-width=2` 约定 | 本轮指令「用 lucide 图标」；https://lucide.dev/guide/packages/lucide-static；https://lucide.dev/contribute/icons/code-conventions |
| D02 | 图标许可 | Lucide ISC License，Copyright (c) 2026 Lucide Icons and Contributors；派生自 Feather 的图标另带 MIT，Copyright (c) 2013-present Cole Bemis；登记进关于页与 THIRD-PARTY-NOTICES.md | https://lucide.dev/license |
| D03 | 使用逻辑骨架 | 统一 12 项 L01–L12：入口首屏 / 推荐默认 / 缓存 / 刷新 / 空态 / 加载 / 错误 / 关闭 / 权限 / 状态可见 / 性能 / 可发现；每个功能必须填满，缺一判未补全 | 本轮指令「每一个地方都要有使用逻辑」「像我之前设计的」 |
| D04 | 功能矩阵 | U01–U20 共 20 个功能逐项填 12 骨架；另落缓存分层 4 层、刷新触发 R1–R5、推荐位 6 处、缓存失效并发冲突 8 种 | docs/design/ux-logic-matrix.md |
| D05 | 用户举例落地 | 首页「推荐服务器」卡；服务器页推荐位与权重口径（用户指定排第一）；每个视图顶部逻辑条显示已缓存时间、命中/未命中、刷新、强制刷新；新增「数据与缓存」四层总控与「刷新机制」R1–R5 页 | 本轮指令「服务器首页肯定得有推荐、缓存机制、刷新机制」 |
| D06 | UX 视图扩展 | 20 → 28 视图 / 22 个独立区块；新增服务器推荐、第三方许可、数据与缓存、刷新机制、状态与降级、AI 接口、开服器、无头模式 | D05 与 D03 |
| D07 | 第三方许可页 | 关于页一级入口「查看第三方许可」；七列表（项目 / 版本 / 许可证 / 版权 / 用途 / 来源 / 构建状态）16 组；按许可证分组筛选；Lucide ISC 原文摘录；插件动态追加说明 | 本轮指令「使用别人的代码需要在关于页面第三方许可说明」；https://libre.xram.net/guides/attribution |
| D08 | 发行物声明 | 新增 THIRD-PARTY-NOTICES.md，与关于页展示同一份清单，离线可读；如实标注「演示层已使用 1 组、文档层 13 组、进入 `src/` 构建 0 项」 | 本轮指令；开源归属规范 |
| D09 | 插件许可 | 插件加载后动态追加插件名、许可证、作者名、项目地址、修改后版本地址；全文缺失给来源链接与「稍后」，不编造 | docs/licenses/index.md L09 |
| D10 | 联网补思路 | 查到 lucide 许可、SVG 约定、第三方归属规范、PCL2 多层缓存、FCL 布局下载后视图不自动刷新的观察者改造；按「推荐 / 缓存 / 刷新」骨架吸收，不照抄实现 | 本轮指令「没思路就上网搜」 |
| D11 | 自评迭代 | 3 轮：7.2 → 8.4 → 9.2；每轮记录发现的不足与补入内容，补入动作真实落盘 | 本轮指令「自评到 9 分以上」 |
| D12 | 范围 | 只交付 UX HTML、PNG、图标资产、许可声明、设计矩阵与文档；`src/` 本轮无变化，不进构建、不生成 LICENSE | 003 D07；018 D10 |

## 调研来源

| 编号 | 来源 | 取到的事实 | 四值 |
| --- | --- | --- | --- |
| R01 | https://lucide.dev/license | ISC 全文；Feather 派生图标清单与 MIT 全文；Copyright 年份 | 已证实 |
| R02 | https://lucide.dev/guide/packages/lucide-static | 支持内联 SVG / sprite；全量 sprite 不推荐生产，应只打包用到的图标 | 已证实 |
| R03 | https://lucide.dev/contribute/icons/code-conventions | 24×24 viewBox、fill=none、stroke=currentColor、stroke-width=2、圆角端点 | 已证实 |
| R04 | https://github.com/lucide-icons/lucide/contents/icons/*.svg | 88 枚图标一手 SVG 与逐枚 blob SHA | 已证实 |
| R05 | https://libre.xram.net/guides/attribution | 归属需项目名、版权、许可证全文或链接；发行二进制应在 About / Legal 页展示；THIRD-PARTY-NOTICES 随发行物附带 | 已证实 |
| R06 | https://opensourcelicenserisk.com/glossary/attribution-requirement | 归属义务随代码传递；NOTICE 文件保留；许可清单随依赖变化刷新 | 已证实 |
| R07 | PCL2 资源管理架构公开资料 | 内存 / 磁盘 / 网络 / 预取四层缓存 | 已证实 |
| R08 | FCL 布局下载刷新机制公开资料 | 下载后列表不自动刷新 → 观察者模式 / 自动跳转推视图更新 | 已证实 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=28`，29 张 PNG | 已证实 |
| `grep -c '<section class="view'` | 22 | 已证实 |
| `grep -c '<symbol'` | 88 | 已证实 |
| 字符图标残留扫描 | 0 | 已证实 |
| `! grep -rE 'FCL\|揉纸启动器\|https?://' demos/ui-full-kcu-paper.html` | exit 0 | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `git diff 66019be..HEAD -- src/` | 空 | 已证实 |
| 用户在手机端按图给手感反馈 | 未发生 | 未证实 |

## 边界

| 项 | 值 |
| --- | --- |
| 落地 | 88 枚图标资产与 manifest、28 视图 UX HTML、29 张 PNG、设计矩阵、许可页与 NOTICES、决策与功能 md、索引与记录 |
| 未落地 | UI 实现、L4 headless 及以下 6 层、CF 下载模块、特殊版代码、本项目 LICENSE |
| 后端仓 | 0 个写请求 |
| 凭据 | 全仓零字面量 |

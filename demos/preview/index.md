# 界面预览图索引（023 · 43 个产品视图）

| 项 | 值 |
| --- | --- |
| 轮次 | 023 |
| 来源 | `demos/ui-full-kcu-paper.html`，按 `#view=` 切换，26 个独立区块，43 张产品截图 + 4 张内部证据图 |
| 形态 | **UX HTML**：1440×900 桌面窗口，标题栏 / 导航 / 工具条 / 卡片 / 表格 / 弹窗 / 抽屉 / 状态栏 |
| 风格 | 米纸色板、衬线标题、折痕高光、细噪点、小圆角、细描边、半透明卡片；深色纸质主题独立一套 |
| 图标 | lucide 88 枚一手 SVG 内联 sprite，ISC + Feather 派生 MIT，无 CDN |
| 使用逻辑 | 26 个区块各有逻辑条：已缓存时间、命中 / 未命中、刷新、强制刷新、状态 |
| 023 信息架构 | 一级导航 9 项；设置与关于固定在底部；扩展区独立；产品界面不出现工程叙事；标题栏语言切换、服务器改名、延迟小字、崩溃反馈分组 |
| 渲染 | `python3 scripts/render_ui.py`，本地 chromium，每场景强制重载，离线 |
| 总览 | `00-overview.png`，只收 43 个产品视图，4 列 11 行，1462×2964 |
| 打包 | `/data/workspace/ui-previews.zip`，含本目录全部 PNG |
| 内部证据 | `34-slots.png` / `35-recommendations.png` / `36-handoff.png` / `37-upperstack.png` 为设计证据，不进产品导航、不进总览 |

| 文件 | 视图 | 看什么 |
| --- | --- | --- |
| 00-overview.png | 总览 | 37 个视图一眼看全 |
| 01-home.png | 首页 · 米纸质感 | 公告横幅、四统计、启动卡、推荐服务器、手感调整 |
| 02-home-dark.png | 深色纸质主题 | 同一布局的深色纸底与浅墨字 |
| 03-notices.png | 公告中心 | 6 条公告、4 类标签、3 未读高亮 |
| 04-notice-detail.png | 公告详情弹窗 | 正文、附件、不再提示 / 稍后 / 知道了 |
| 05-update.png | 版本更新提示 | 更新日志与操作按钮 |
| 06-onboarding.png | 首次启动引导 | 4 步向导、C 盘 KCU 数据目录 |
| 07-instances.png | 实例列表 | 纸感表格、7 个实例、五类状态徽章 |
| 08-cardgrid.png | 网格视图 | 列表/网格分段切换后的卡片流 |
| 09-download.png | 下载队列 | 批量文件、进度、取消、下载源软策略 |
| 10-mods.png | 模组管理表格 | 110 个模组与状态徽章 |
| 11-login.png | 登录 | 三种登录、三级回退链、账户卡 |
| 12-logs.png | 运行日志 | [KCU] 单行诊断、导出诊断包 |
| 13-logs-drawer.png | 日志抽屉 | 抽屉形态与关闭路径 |
| 14-settings.png | 设置 · 常规 | 9 分组 chip、稳定 ID、@modified、锁定徽章 |
| 15-about.png | 关于 | 核心槽位锁定、交接基线、上层候选、第三方许可入口 |
| 16-popups.png | 弹窗全集 | 11 类弹窗与关闭状态 |
| 17-lightweight.png | 轻量模式 | 极简窗口与 13 项排除边界 |
| 18-error.png | 异常与边界六态 | 空 / 加载 / 错误 / 被锁 / 安全模式 / 离线 |
| 19-narrow.png | 侧栏收起态 | 导航折叠为图标条 |
| 20-context.png | 右键菜单 | 纸感上下文菜单 |
| 21-servers.png | 服务器列表 | 自动连接结果、MC 风格 MOTD / 人数 / ping 条 / 版本、锁定置顶、失败沉底 |
| 22-licenses.png | 第三方许可七列表 | 16 组组件、分组筛选、ISC 原文摘录 |
| 23-sync.png | 数据与缓存总控 | 设置内二级页：四层缓存、容量条、命中率 |
| 24-refresh.png | 刷新机制 R1–R5 | 五种触发、失败回退缓存不空白 |
| 25-states.png | 状态与降级 | 六态 + 缓存兜底 + 降级链 |
| 26-ai.png | AI 容器接口 | 设置内展开页：用户自填、每次请求确认 |
| 27-serverhost.png | 开服器 | 一键开服、EULA 启动前写入、UPnP 默认关 |
| 28-headless.png | 无头模式 | 统一信封、任务优先级、无 UI |
| 29-settings-recommend.png | 设置 · 推荐与排序 | 推荐总控、10 位表、权重自定义 |
| 30-settings-status.png | 设置 · 服务器与连接 | 自动连接、排序、读取游戏内列表、双击进服 |
| 34-servers-join.png | 双击进服 | 实例绑定弹窗与三个按钮 |
| 35-servers-locked.png | 连不上沉底 | 锁定项保持靠前，失败项排最后 |
| 36-servers-budget.png | 设备连接范围 | 标准档 4 台 / 3 路，预算四格、范围外标签 |
| 37-servers-history.png | 轻量档与失败历史 | 2 台 / 2 路，无成功记录按权重排中段 |
| 38-servers-latency.png | 信号格延迟 | 五格信号条下标 42 ms / 96 ms / 120 ms |
| 39-servers-rename.png | 改名弹窗 | 只改显示名，同名标签可见 |
| 40-servers-samenames.png | 同名服务器 | 两台同名不同地址，各自独立 |
| 41-i18n-en.png | English 界面 | 导航 / 设置 / 按钮 / 说明切换为英文 |
| 42-settings-crash.png | 崩溃反馈 | 默认不外发、脱敏开、可导出 |
| 43-licenses-updated.png | 第三方许可 | 新增 6 组候选库登记 |
| 31-settings-plugins.png | 设置 · 插件与更新 | 插件清单、插件化更新、回滚模拟 |
| 32-settings-cache.png | 设置 · 缓存与刷新 | 四层 TTL、普通 / 强制刷新、失败回退 |
| 33-settings-ai.png | 设置 · AI 容器接口 | 地址自填、权限、失败分类 |

流程 HTML（`demos/round-0XX-*.html`）与 UX HTML 分开：前者是步骤节点与状态机，只说明逻辑；后者是用户实际看到的界面。动 UI 的轮次主交付必须是 UX HTML + PNG 预览。021 起产品界面不写工程叙事，规则见 `docs/design/ui-product-copy.md`。

纸质样板只取质感，位置重新组织；KCU 品牌内联 SVG，无外部字体与远端脚本。第三方许可见 `THIRD-PARTY-NOTICES.md` 与 22-licenses.png、37-upperstack.png。

手感回路：先看图 → 提意见 → 先改演示与截图 → 确认后才改实现。本目录是演示产物，未进入 `src/`。

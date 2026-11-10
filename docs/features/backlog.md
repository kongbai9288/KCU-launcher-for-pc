# 第 011 轮功能输入登记表

轮次：011
逐字原文：docs/spec/11-features-input.txt（268 行，17096 字节，SHA-1 `fd50385fd5010c23479d0437cd558f8711da58e4`）
编号连续性：1-55 连续，无缺号
文件管理清单：175 个 `·` 条目
状态：全部为「已登记 / 未实现 / 未进入构建」，`src/` 为空

每实现一个功能时，按 docs/features/_template.md 单独写一份 md，字段固定为：怎么运作、开放了什么、登记框架、用户使用逻辑、性能。本表是输入索引，不代替单份功能 md。框架列为候选，未批准。

## 编号功能 1-55

| 编号 | 名称 | 框架候选 | 状态 |
| --- | --- | --- | --- |
| 1 | 按序下载、多线程下载、每页 20 条、聚合搜索 | normal.mod.download | 已登记 / 未实现 |
| 2 | 模组依赖检测与一键安装 | normal.mod.deps | 已登记 / 未实现 |
| 3 | 模组界面翻译 | normal.mod.i18n | 已登记 / 未实现 |
| 4 | 录屏与截屏，快捷键开启后台进程，5GB 与 2 小时并联熔断，结束引导保存目录 | normal.media | 已登记 / 未实现 |
| 5 | 快捷键绑定 | core.hotkey | 已登记 / 未实现 |
| 6 | viaNBT 提供 NBT 能力，界面接近主流 | normal.nbt | 已登记 / 未实现 |
| 7 | 启动页服务器列表、双击进入、版本权重选择 | normal.server.list | 已登记 / 未实现 |
| 8 | 手机互传，局域网，二维码，通道内置不开放 | normal.lan | 已登记 / 未实现 |
| 9 | 关于与第三方开源许可，前置图片为真实图片 | normal.about | 已登记 / 未实现 |
| 10 | 启动同意隐私政策 | normal.privacy | 已登记 / 未实现 |
| 11 | 陶瓦联机 | normal.lan | 已登记 / 未实现 |
| 12 | 服主模组更新 json，公告页可取消 | normal.server.modupdate | 已登记 / 未实现 |
| 13 | 手动选择镜像下载 Java 与游戏实例 | core.download.mirror | 已登记 / 未实现 |
| 14 | 模组更新与模组管理 | normal.mod | 已登记 / 未实现 |
| 15 | 整合包一键安装，拖到主界面 | normal.modpack | 已登记 / 未实现 |
| 16 | 加载器自动安装 | core.loader | 已登记 / 未实现 |
| 17 | 每个 MC 绑定账号，默认账号可切换 | normal.account | 已登记 / 未实现 |
| 18 | 未成年人模式，禁用下载，防沉迷 | normal.account | 已登记 / 未实现 |
| 19 | 单次时长、总时长、每实例时长，快捷启动静默记录 | normal.stats | 已登记 / 未实现 |
| 20 | 日志系统，每 100 条压缩到一个压缩包 | core.log | 已登记 / 未实现 |
| 21 | UUID 手动填写 | normal.account | 已登记 / 未实现 |
| 22 | 自动下线、自动关机、自动上线、自动加入服务器 | normal.scheduler | 已登记 / 未实现 |
| 23 | 模组收藏 | normal.mod | 已登记 / 未实现 |
| 24 | 上线提醒，标题「kcu记录器」，自定义图片与文本 | normal.notice | 已登记 / 未实现 |
| 25 | 版本功能迁移，键盘与服务器文件，多版本应用，弹窗提示 | normal.instance | 已登记 / 未实现 |
| 26 | 同时启动多个 MC 版本，默认上限 3 | dispatcher | 已登记 / 未实现 |
| 27 | 内存或存储不足友情提示 | core.diagnostics | 已登记 / 未实现 |
| 28 | 日志按 mod 提示内容选择 | core.log | 已登记 / 未实现 |
| 29 | `§` 作为用户自定义镜像 URL 的模板版本号占位符 | core.download.mirror | 已登记 / 未实现 |
| 30 | 一个模组多源同时下载，先完成即关闭其余请求 | core.download | 已登记 / 未实现 |
| 31 | 动态查看 CPU 性能信息 | core.diagnostics | 已登记 / 未实现 |
| 32 | MC 颜色代码一键复制，旧格式与新 json 格式 | normal.tool | 已登记 / 未实现 |
| 33 | 语言与语言包选择和管理 | core.i18n | 已登记 / 未实现 |
| 34 | `.kculf` 跳过 GUI 直接进 MC，无头用 `kculh`，两天或拓展包解锁 | headless | 已登记 / 未实现 |
| 35 | 模组图标支持全部图片格式 | normal.mod.icon | 已登记 / 未实现 |
| 36 | 重复模组同版本警告，单弹窗分页顺序逐项选择 | normal.mod | 已登记 / 未实现 |
| 37 | 统一调度器发放文字 json 与字体，语言文件集中 | core.i18n | 已登记 / 未实现 |
| 38 | 深色模式 | normal.ui | 已登记 / 未实现 |
| 39 | 思维导图查看模组依赖，含图标、文字、版本、作者 | normal.mod.deps | 已登记 / 未实现 |
| 40 | 皮肤预览，正向，可 3D 旋转，与角色选择同页 | normal.account.skin | 已登记 / 未实现 |
| 41 | 投影预览，支持两个投影模组的文件 | normal.tool | 已登记 / 未实现 |
| 42 | 文件一键补全，有版本 json 时补其余文件 | core.download | 已登记 / 未实现 |
| 43 | 多实例共用同版本同哈希同加载器 mod，手动选中，启动时选中 | normal.instance | 已登记 / 未实现 |
| 44 | 备份，轻备份只配置，自动化全量加差异压缩包 | normal.instance.backup | 已登记 / 未实现 |
| 45 | JVM 内存自动分配，回收器选择，模组内存智能分析 | core.jvm | 已登记 / 未实现 |
| 46 | CopperGolemLauncher 插件，单开仓，默认不内置，引导下载 | plugin | 已登记 / 未实现 |
| 47 | 放音乐，未启动 MC 时播放，可导入 mp4 | normal.media | 已登记 / 未实现 |
| 48 | 微软账号 token 到期前 7 天提醒 | normal.account | 已登记 / 未实现 |
| 49 | MC 百科，按语言定 wiki 站点，失败进英文，外置浏览器打开 | normal.wiki | 已登记 / 未实现 |
| 50 | 访客模式，隐藏账号与实例，密码开关 | normal.account | 已登记 / 未实现 |
| 51 | 同实例模组启用禁用方案，变动提示 | normal.mod | 已登记 / 未实现 |
| 52 | 二分法模组可用性检验 | normal.mod | 已登记 / 未实现 |
| 53 | 自定义环境变量与 JVM 参数，逐条收藏 | core.jvm | 已登记 / 未实现 |
| 54 | 正版 id 复用提示与自填，token 与 id 走系统保护 | normal.account | 已登记 / 未实现 |
| 55 | CurseForge 镜像与后端分流，境外两者都使用，镜像优先 | core.download | 已登记 / 未实现 |

## 文件管理清单分组

逐字条目见 docs/spec/11-features-input.txt「这里的文件管理除了你找到的别人的开源骨干里的其他功能以外，必须包含以下功能」段，共 175 项。

计数口径：`·` 字符共 175 个；其中 174 个为独立条目行，1 个为第 30 行引导句末尾同行的首个条目 `· 浏览文件和文件夹`。条目总数为 175。011 轮初稿按「独立条目行」记为 174，漏掉同行那 1 项，独立验证者指出后已修正。

分组如下：

| 组 | 内容 | 框架候选 |
| --- | --- | --- |
| G01 | 浏览、目录树浏览/展开/折叠/搜索/拖放 | normal.filemanager.tree |
| G02 | 前进、后退、向上、刷新、地址栏、面包屑、路径跳转、自动补全、侧边栏、快捷访问、收藏目录、最近访问 | normal.filemanager.nav |
| G03 | 多标签页、多窗口、分栏浏览 | normal.filemanager.window |
| G04 | 定位游戏根/实例/版本/模组/资源包/光影包/存档/截图/配置目录 | normal.filemanager.locate |
| G05 | 打开文件、打开文件夹、打开所在目录、默认程序、其他程序、终端中打开、系统文件管理器中显示 | normal.filemanager.open |
| G06 | 新建文件夹、新建文件 | normal.filemanager.edit |
| G07 | 复制、剪切、粘贴、移动、拖放复制、拖放移动 | normal.filemanager.transfer |
| G08 | 重命名、批量重命名、查找替换、正则、编号、前后缀增删、扩展名批量、大小写转换 | normal.filemanager.rename |
| G09 | 删除、永久删除、回收站、还原文件、清空回收站 | normal.filemanager.trash |
| G10 | 多选、全选、反选 | normal.filemanager.select |
| G11 | 文件/文件夹搜索，按名称/类型/大小/修改时间/路径，当前/子文件夹/隐藏，内容、通配符、正则、模糊、精确、排除、过滤、高级、结果排序/筛选/批量操作、保存条件、历史、建议 | normal.filemanager.search |
| G12 | 排序、四种排序键、方向切换、分组显示、按类型/日期/大小分组、文件筛选 | normal.filemanager.sort |
| G13 | 图标/列表/详细信息/缩略图/平铺/紧凑视图、图标与缩略图大小、列宽、列顺序、自定义列、显示隐藏文件与扩展名、系统文件 | normal.filemanager.view |
| G14 | 文件预览、图片/文本/压缩包预览、预览窗格、详细信息面板、状态栏、文件与文件夹属性、大小、数量、创建/修改/访问时间、路径、复制路径、权限、只读、磁盘空间、目录占用 | normal.filemanager.preview |
| G15 | 压缩、解压、解压到指定目录、加密、解压密码、分卷压缩与解压、校验、修复 | normal.filemanager.archive |
| G16 | 创建快捷方式、文件锁定提示、文件占用提示、自动刷新、文件变更监视 | normal.filemanager.watch |
| G17 | 传输进度、复制队列、暂停、恢复、取消、后台、断点续传、完成提示、失败重试 | normal.filemanager.transfer |
| G18 | 冲突处理、覆盖确认、跳过、保留两者、自动重命名 | normal.filemanager.conflict |
| G19 | 撤销、重做、操作历史、批量确认、批量预览、错误提示、重试、跳过错误 | normal.filemanager.history |

分组为索引，不逐组计数。逐字文本与 175 个条目以 docs/spec/11-features-input.txt 为准，本表不抄写逐项文字，避免输出遗漏。

用户补充约束：文件管理的搜索框、排序按钮等交互与正常文件管理器一致；「有些功能你看着办」；用户逻辑需要对应功能时同样要有，例如搜索；开源骨干项目待选定，见 docs/research/15-input-survey.md DS06。

## 开头段约束索引

| 项 | 登记位置 |
| --- | --- |
| 插件使用逻辑近似 dsh，不直接使用，用开源其他项目 | docs/research/15-input-survey.md DS01-DS06 |
| 模块化、更新友好 | docs/decisions/011-feature-input.md D15 |
| 插件加载后开源许可页动态增加 5 字段 | docs/research/15-input-survey.md OL01 |
| 设备不支持时功能可关闭 | docs/decisions/011-feature-input.md D18、D19 |
| CF 凭据不进仓库、特殊版单开私仓 | docs/decisions/011-feature-input.md D02、D03 |
| 境外离线账户限制与正版例外 | docs/decisions/011-feature-input.md D06、D07 |
| 32 位与 64 位、多架构、Win7 默认轻量 | docs/decisions/011-feature-input.md D08-D10 |
| 插件独立许可证、独立进程 | docs/research/15-input-survey.md OL06 |
| 每个弹窗关闭逻辑 | docs/decisions/011-feature-input.md D21 |
| 开源复用优先、许可证头、拼接后对比 | docs/decisions/011-feature-input.md D17、D22 |
| 统一调度器启动 json 与语言包 | docs/decisions/011-feature-input.md D18、D19 |
| 一次请求含多个 json、去重聚合 | docs/research/14-batch-network.md |
| 复用同一代码、文件归中 | docs/research/14-batch-network.md K06、K07 |
| 保存路径可选、API 不写死、网址端口不写死、图标单文件 | docs/research/14-batch-network.md K01-K05 |
| 本地 API 不公开、内部监听、服务器 AI API 例外 | docs/research/14-batch-network.md L01-L04 |
| 拖放安装页、圆圈 i 说明、分辨率适配与滚动、线状滑动条、圆角扁平化、页面可扩展 | docs/decisions/011-feature-input.md D21 |
| GPLv3 与动态链接 | docs/research/15-input-survey.md OL03 |
| 多语言文件集中、语言包由统一调度器发放 | docs/decisions/011-feature-input.md D18 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cmp /data/inputs/功能.txt docs/spec/11-features-input.txt` | exit 0 | 已证实 |
| `sha1sum` 双端 | `fd50385fd5010c23479d0437cd558f8711da58e4` | 已证实 |
| 正则 `^\s*\d+\.` 计数 | 55，1-55 连续 | 已证实 |
| `·` 字符计数（含同行首项） | 175 | 已证实 |
| `git ls-files src/` | 输出为空 | 已证实 |
| 浏览器渲染与 Rust 构建实测 | 未执行 | 受阻 |

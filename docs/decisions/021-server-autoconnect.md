# 第 021 轮服务器自动连接、产品界面去工程化

| 项 | 值 |
| --- | --- |
| 编号 | 021 |
| 状态 | 已批准 |
| 轮次 | 021 |
| 逐字指令 | docs/spec/21-round-021-instructions.txt，1 行 1003 字节，SHA-1 `ec86aa376a193eb5701de49b2f2bd464599189b5` |
| 前序 | 020 服务器状态设置页（SLP 参数 / 6 类状态 / 自定义文案颜色） |
| 纠偏 | 020 把「服务器状态」做成用户配置 SLP 参数，理解偏了；本轮撤回该页面口径 |

## 决策

| 编号 | 项 | 值 | 依据 |
| --- | --- | --- | --- |
| D01 | 产品界面去工程化 | 界面上不出现槽位 ID、交接基线、候选构建状态、稳定设置 ID、锁定徽章、内部诊断号等工程叙事；工程结论只落 docs/ | 021 指令「作为一个对外开放的应用，强调这些不是废话吗」 |
| D02 | 020 内部证据页处置 | 槽位注册表、推荐位总览、交接基线、上层候选四个区块保留在 HTML 与 docs/ 作为设计证据，但**不进产品导航、不进总览拼图** | D01 |
| D03 | 锁定功能保留但不喊出来 | 设置与关于仍固定在导航底部同一容器、插件与更新包不可改写；界面去掉虚线框、锁图标说明、locked 徽章 | 020 D05 继续有效；021 D01 去掉标签 |
| D04 | 自动连接 | 用户添加完服务器立即自动尝试连接；打开列表时自动同步一次；结果缓存下来作为排序权重 | 021 指令 / R02 / R04 / C02 |
| D05 | 排序 | 锁定置顶（连不上也不动）→ 连得上按延迟、最近使用、在线人数、版本兼容 → 连不上沉底 | 021 指令 / R04 |
| D06 | 自动分析 | 只读各实例目录的 `servers.dat`（未压缩 NBT）；覆盖可见列表、隐藏列表、快速进入过的地址；不写回、不覆盖玩家在游戏里加的服 | 021 指令 / R01 / R02 / C08 |
| D07 | 显示照原版 | 64×64 图标、玩家命名、两行 MOTD（§ 码转义、不当 HTML 执行）、在线人数 / 上限、ping 条五档、版本名；MOTD 缺省与 `???` 人数按游戏内表现 | 021 指令 / R04 / R05 / R06 |
| D08 | 双击进服 | 上次玩这个服用的实例 → 上次用过的实例 → 只在版本兼容范围里挑；锁定实例优先；没有合适实例给「换实例」，不静默失败 | 021 指令 / 013 F07-F09 |
| D09 | 设置口径 | 「服务器状态」分组改「服务器与连接」：自动连接、排序、读取游戏内列表、双击进服四组；删除 SLP 参数、6 类状态、自定义文案颜色 | D01 / D04-D08 |
| D10 | 社区事例 | 查到 PCL2 延迟测试算法与服务器列表改进、HMCL/PCL2/BakaXL 自存列表、社区工具生成 servers.dat；第三方启动器一般不读官方 servers.dat，KCU 多做一层 | 021 指令「社区都有相关事例」/ C05-C08 |
| D11 | 范围 | 只交付 UX HTML、36 张 PNG、设计 / 调研 / 决策 / 功能 md、索引与规则；`src/` 与 Cargo.lock 无变化 | 003 D07 / 020 D16 |

## 调研来源

| 编号 | 来源 | 事实 |
| --- | --- | --- |
| R01 | https://minecraft.wiki/w/Server_list_storage_format | servers.dat 未压缩 NBT 结构与字段 |
| R02 | https://zh.minecraft.wiki/w/%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%88%97%E8%A1%A8%E5%AD%98%E5%82%A8%E6%A0%BC%E5%BC%8F | 可见 / 隐藏两份列表，可见列表游戏主动同步，隐藏最多 16 个 |
| R03 | https://minecraft.wiki/w/Servers.dat_format | 不存直连 IP 与 LAN；字段补充 |
| R04 | https://minecraft.wiki/w/Server_list | 原版四元素、ping 分档、LAN 底部、顺序可调 |
| R05 | https://minecraft.wiki/w/Java_Edition_protocol/Server_List_Ping | SLP 1.7+ 流程与 JSON 字段 |
| R06 | https://zh.minecraft.wiki/w/Java%E7%89%88%E7%BD%91%E7%BB%9C%E5%8D%8F%E8%AE%AE/%E6%9C%8D%E5%8A%A1%E5%99%A8%E5%88%97%E8%A1%A8%E6%9F%A5%E8%AF%A2 | description / players / favicon 解析细则 |
| R07 | https://wikivg.booky.dev/NBT | servers.dat 永远未压缩 |
| C01-C08 | 见 docs/research/18-server-list-autodiscovery.md | MOTD 不可信、打开列表 ping 每个服、社区启动器做法 |

## 界面证据

| 文件 | 视图 |
| --- | --- |
| 21-servers.png | 服务器列表：锁定置顶、连不上沉底、MC 风格 MOTD / 人数 / ping 条 / 版本 |
| 30-settings-status.png | 设置 → 服务器与连接：自动连接、排序、读取游戏内列表、双击进服 |
| 34-servers-join.png | 双击进服实例绑定弹窗 |
| 35-servers-locked.png | 一台连不上后沉底、锁定项保持靠前 |
| 15-about.png | 关于页精简：版本 / 外观 / 第三方许可 / 开源致谢 |
| 14-settings.png | 设置页：无稳定 ID、无槽位徽章、无工程说明 |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=35`，40 张 PNG（35 产品视图 + 1 总览 + 4 内部证据图） | 已证实 |
| `node -e` 内联脚本 | JS_SYNTAX_OK | 已证实 |
| `grep -c 'class="setid"'` | 0 | 已证实 |
| `grep -c 'data-internal="1"'` | 4 | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `git diff 170b69d..HEAD -- src/ Cargo.lock` | 空 | 已证实 |
| 浏览器内实际双击、真实 TCP 连接、真实 servers.dat 解析 | 未实测 | 受阻 |

## 边界

| 项 | 值 |
| --- | --- |
| 落地 | UX HTML 26 区块 / 35 产品视图 / 40 PNG、服务器页重做、设置分组改写、关于页精简、导航与文案去工程化、调研与决策、4 份功能 md |
| 未落地 | 真实 SLP 客户端、servers.dat NBT 解析实现、双击进服实现、UI 实现 |
| 后端仓 | 0 个写请求 |

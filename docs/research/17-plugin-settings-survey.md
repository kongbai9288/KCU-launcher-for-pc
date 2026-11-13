# 插件槽位、设置架构、插件化更新与服务器状态统一调研

| 项 | 值 |
| --- | --- |
| 轮次 | 020 |
| 依据 | docs/spec/20-round-020-instructions.txt「最后再统一调研一下」 |
| 来源数 | 12 个，全部为完整 URL 锚点 |
| 禁止项 | R02 镜像响应不作为官方源；社区经验与官方规范分开登记；未证实项不写进实现 |

## 一手来源

| 编号 | 来源 | 取到的事实 | 四值 |
| --- | --- | --- | --- |
| R01 | https://code.visualstudio.com/api/ux-guidelines/overview.md | VS Code UI 分 containers 与 items；Activity Bar、Primary Sidebar、Secondary Sidebar、Editor、Panel、Status Bar 各有明确职责；扩展向容器贡献 items，不改写容器本身 | 已证实 |
| R02 | http://vscode.net.cn/api/references/contribution-points | 贡献点是 package.json `contributes` 的 JSON 声明；含 views、viewsContainers、menus、configuration、commands、keybindings、submenus 等；扩展通过声明注册，不直接改宿主布局 | 已证实（官方文档中文镜像，事实与 R01 互证） |
| R03 | https://code.visualstudio.com/api/extension-guides/tree-view | `contributes.viewsContainers` 先注册容器，`contributes.views` 再注册视图；视图 visibility 可 visible / collapsed / hidden；`view/title`、`view/item/context` 分组追加动作，`group` 用 `@n` 指定顺序 | 已证实 |
| R04 | https://code.visualstudio.com/docs/configure/settings | 用户设置全局、工作区设置覆盖用户设置；部分应用级设置（更新、安全）不可被工作区覆盖；设置编辑器按分组、支持搜索与 `@modified` 过滤；扩展通过 `contributes.configuration` 加自己的设置，改动即时生效；齿轮可复制 ID / 重置 | 已证实 |
| R05 | https://docs.rs/tauri-plugin-updater/latest/struct.Config.html | `pubkey` 存公钥内容；`require_signed_version` 要求签名携带版本，防止把旧签名配新版本号强制降级；`allow_downgrades` 允许非更新版本，默认 false；`endpoints` 为更新端点数组；三个 `dangerous_*` 开关默认关闭 | 已证实 |
| R06 | https://doc.rust-lang.org/ | Rust 官方文档入口；标准库、Cargo Book、Reference、Rustonomicon 分册；ABI 稳定性说明需看具体条目，不在本页推断 | 已证实（入口） |
| R07 | https://docs.rs/rs-rich-plugin-api/latest/rich_plugin_api/abi/index.html | 「Rust's own ABI is unstable, so nothing Rust-specific crosses the boundary」；`ABI_MAJOR` 不兼容变更时递增，宿主拒绝不同 major 的插件；native dylib 导出单个 `extern "C"` 入口返回 descriptor；宿主在信任布局前先读 major/minor | 已证实 |
| R08 | https://docs.rs/supercode-core/latest/supercode/plugins/index.html | 插件为目录内 manifest（DATA），代码只作为宿主派生的子进程运行，不链入宿主地址空间；理由含内存安全、跨构建版本、语言无关、沙箱、信任门 | 已证实 |
| R09 | https://minecraft.wiki/w/Java_Edition_protocol/Server_List_Ping | SLP 1.7+ 流程：handshake 的 next state = 1 → Status Request（无字段）→ Status Response（JSON 字符串）→ Ping/Pong；JSON 含 `version.name/protocol`、`players.max/online/sample`、`description`（text component）、`favicon`（64×64 PNG base64）、`enforcesSecureChat`；SLP 可被禁用；1.7 前后不兼容 | 已证实 |
| R10 | https://crates.io/crates/reqwest/range/%3E=%200.10.1,%20%3C%200.11 | reqwest 声明 `MIT OR Apache-2.0`；Windows / macOS 走系统 TLS | 已证实（元数据页） |
| R11 | https://github.com/lucide-icons/lucide | 图标库 ISC；本轮沿用 019 已取得的 88 枚逐枚 blob SHA | 已证实 |
| R12 | https://libre.xram.net/guides/attribution | 归属需项目名、版权、许可证全文或链接；发行二进制应在 About / Legal 页展示；THIRD-PARTY-NOTICES 随发行物附带；清单随依赖变化刷新 | 已证实 |

## 公开资料与社区经验（不作官方规范）

| 编号 | 来源 | 取到的事实 | 四值 |
| --- | --- | --- | --- |
| C01 | https://blog.csdn.net/2301_81410839/article/details/162604610 | 插件 ABI 先冻结再扩展；跨库边界用 C ABI、宿主分配缓冲、插件填充；高风险插件进程隔离；配置签名、路径遍历与版本回滚防护、耗时预算 | 已证实（公开资料） |
| C02 | https://www.joingg.co/blog/minecraft-server-list-ping-end-to-end | SLP 五包交换；`description` 是 text component 不是裸字符串；`version.name` 缺失导致版本 unknown；favicon 严格 64×64 PNG；`players.sample` 不是玩家列表；延迟是探测端到服务端的往返 | 已证实（公开资料，与 R09 互证） |
| C03 | https://www.fumora.net/lab/minecraft-server-list-ping-response | 服务端插件通过 `ServerListPingEvent` 改 MOTD、人数、图标，可取消事件使客户端看到离线；维护状态常通过改 MOTD 表达 | 已证实（公开资料，第三方服务端行为） |
| C04 | 第三方项目 THIRD_PARTY_NOTICES 汇总（serde / serde_json、reqwest、tokio、semver、sha2、anyhow、thiserror、regex、url、windows-sys、libloading、rusqlite、chrono、axum） | 常见许可证组合 MIT OR Apache-2.0 / MIT / ISC；发布构建须以当前 Cargo.lock 与各 crate 自带许可证文件为准 | 已证实（声明文本）；逐项核对为未证实 |

## 中文镜像与受阻项

| 编号 | 来源 | 状态 |
| --- | --- | --- |
| M01 | https://tauri.org.cn/v1/guides/distribution/updater/ | 签名密钥丢失后无法给既有安装推送更新；中文镜像，按 R02 不作官方源，事实与 R05 的 `pubkey` 语义互证，标未证实（镜像原文） |
| M02 | Tauri v2 updater 官方插件页直抓 | 受阻，本轮未取得一手全文；更新器核心事实以 R05 docs.rs 结构为准 |
| M03 | Eclipse / OSGi 扩展注册表官方页 | 受阻，本轮未取得；槽位保留规则以 R01-R03 为准 |

## 结论（只供设计层使用，不等于实现）

| 编号 | 结论 | 依据 |
| --- | --- | --- |
| J01 | 核心槽位应固定 ID、固定容器、固定顺序；插件只向 `plugin.*` 容器追加条目 | R01、R02、R03 |
| J02 | 设置按分组、稳定 ID、作用域、搜索、`@modified`、单项重置组织；应用级设置不可被插件覆盖 | R04 |
| J03 | 插件清单用 DATA manifest，代码走子进程 / 稳定 C ABI，`ABI_MAJOR` 不匹配拒绝加载 | R07、R08、C01 |
| J04 | 插件化更新必须签名校验，版本比较默认只升，回滚需显式比较器，失败保留旧插件 | R05、M01 |
| J05 | 服务器状态取 SLP JSON 字段；维护态可由服务端插件改 MOTD；探测失败回退缓存并标灰 | R09、C02、C03 |
| J06 | 第三方代码进入构建前逐项取得 LICENSE 全文，在关于页与 NOTICES 声明 | R12、C04 |

## 约束

| 编号 | 内容 |
| --- | --- |
| S01 | 社区经验与官方规范分开，不互相冒充。 |
| S02 | 中文镜像不单独作为已证实来源。 |
| S03 | 第三方项目声明不等于 crates.io 官方元数据；候选库逐项核对前标未证实。 |
| S04 | 以上结论只落设计与演示层，020 轮 `src/` 无变化。 |

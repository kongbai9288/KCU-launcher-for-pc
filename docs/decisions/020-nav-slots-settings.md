# 第 020 轮导航瘦身、槽位锁定、设置归拢与统一调研

| 项 | 值 |
| --- | --- |
| 编号 | 020 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 020 |
| 逐字指令 | docs/spec/20-round-020-instructions.txt，1 行 853 字节，SHA-1 `070c6475693e4bd28f41cfbb3d6b6f9b7d6e72f6` |
| 前序 | 019 使用逻辑矩阵、88 枚 lucide、第三方许可页、28 视图 |

## 决策

| 编号 | 项 | 值 | 依据 |
| --- | --- | --- | --- |
| D01 | 手感回路 | 用户「看样子我还比较满意」= 019 演示层通过；本轮仍先改演示与截图，不改 `src/` | 019 D12 / ui-demo.md 手感回路 |
| D02 | 导航瘦身 | 一级导航收敛为 9 项日常操作；AI 接口、数据与缓存、刷新机制、状态与降级、无头模式、第三方许可从一级导航移走；工具条操作按视图收敛 | 020 指令「有些功能你完全不需要写在顶上，比如接口什么的」 |
| D03 | 配置归拢 | 设置页 9 个分组：常规 / 下载与镜像 / 缓存与刷新 / 推荐与排序 / 服务器状态 / AI 容器接口 / 插件与更新 / 隐私与诊断 / 实验性；自定义项全部落在设置 | 020 指令「把该放在设置的放在设置，有些需要自定义的设置功能，也要放在设置」 |
| D04 | 设置项约定 | 每项稳定 ID（`core.*`）、默认值、作用范围、写后即时生效、失败保留旧值、可搜索、`@modified` 过滤、单项重置 | R04 VS Code 设置编辑器 |
| D05 | 核心锁定槽位 | `core.locked.settings` 与 `core.locked.about` 固定在导航底部同一容器，ID / 位置 / 顺序三者不可变更；插件与更新包不可改写、隐藏、重排 | 020 指令「不把关于设置什么的给锁定在一个位置的话，有可能会被覆盖」 |
| D06 | 插件区 | `slot:plugin.*` 独立容器，插件只能追加条目；`plugin.settings.*`、`plugin.about.credits`、`plugin.rec.*` 为其余开放槽位 | R01-R03 VS Code containers / items / contribution points |
| D07 | 冲突处置 | 声明 `core.*` 一律拒绝注册，保留原条目，显示可见拒绝提示，写 `[KCU]` 诊断行，插件自身不崩溃 | D05 / 020 指令 |
| D08 | 插件清单校验 | manifest 为 DATA，代码走 C ABI 或子进程隔离；`ABI_MAJOR` 不匹配拒绝；摘要 + 签名 + 路径遍历防护 + 耗时预算 | R07 / R08 / C01 |
| D09 | 插件化更新 | 更新器作为插件；更新包只替换插件包，核心二进制不动；签名校验不可禁用；默认只升，回滚需显式比较器；失败保留旧插件 | R05 / M01 / 020 指令 |
| D10 | 推荐位补全 | 10 处推荐位逐处定义内容、权重、用户覆盖、缓存刷新、设置 ID；推荐来源本地 / 官方 / 插件三类可插拔 | 020 指令「推荐的那些项目什么的你都想好」 |
| D11 | 服务器状态 | 取 SLP JSON 字段；在线 / 维护中 / 离线 / 满员 / 私有 / 自定义 6 类；探测间隔、超时、缓存、文案颜色、显示位置、变更历史全部可设置 | R09 / C02 / C03 / 020 指令 |
| D12 | 统一调研 | 12 个一手来源 + 4 组公开资料 + 3 个受阻项，全部完整 URL 锚点，登记 `docs/research/17-plugin-settings-survey.md` | 020 指令「最后再统一调研一下」 |
| D13 | 上层第三方代码 | 批准上层实现采用第三方库；12 组候选逐项标许可证、用途、全文状态、复制状态；取得 LICENSE 全文前不复制；关于页与 NOTICES 登记 | 020 指令「上层的实现都用别人的代码，就行了」/ U01-U08 |
| D14 | 交接基线 | 新增 `docs/design/handoff.md`，把当前仓库定义为可被新对话当底层直接接续的基线，列必读 6 步、已完成层、8 条不可变边界、已知卡点 | 020 指令「新开一个对话把这个当做底层直接写」 |
| D15 | 自评迭代 | 3 轮 7.4 → 8.6 → 9.3，每轮记录发现的不足与真实补入动作 | 019 规则延续 |
| D16 | 范围 | 只交付 UX HTML、38 张 PNG、设计 / 调研 / 决策 / 功能 md、索引与规则；`src/` 与 Cargo.lock 无变化，不启 L4 | 003 D07 / 019 D12 |

## 调研来源

| 编号 | 来源 | 事实 | 四值 |
| --- | --- | --- | --- |
| R01 | https://code.visualstudio.com/api/ux-guidelines/overview.md | containers / items 模型与六个容器职责 | 已证实 |
| R02 | http://vscode.net.cn/api/references/contribution-points | contributes 声明清单 | 已证实（官方文档中文镜像） |
| R03 | https://code.visualstudio.com/api/extension-guides/tree-view | viewsContainers → views，分组顺序 `@n` | 已证实 |
| R04 | https://code.visualstudio.com/docs/configure/settings | 作用域、分组、搜索、@modified、即时生效、扩展设置区 | 已证实 |
| R05 | https://docs.rs/tauri-plugin-updater/latest/struct.Config.html | pubkey / require_signed_version / allow_downgrades / endpoints | 已证实 |
| R06 | https://doc.rust-lang.org/ | Rust 官方文档入口 | 已证实（入口） |
| R07 | https://docs.rs/rs-rich-plugin-api/latest/rich_plugin_api/abi/index.html | Rust ABI 不稳定、C ABI、ABI_MAJOR 拒绝 | 已证实 |
| R08 | https://docs.rs/supercode-core/latest/supercode/plugins/index.html | manifest DATA + 子进程隔离 | 已证实 |
| R09 | https://minecraft.wiki/w/Java_Edition_protocol/Server_List_Ping | SLP 1.7+ 流程与 JSON 字段 | 已证实 |
| R10 | https://crates.io/crates/reqwest/range/%3E=%200.10.1,%20%3C%200.11 | reqwest MIT OR Apache-2.0 | 已证实 |
| R11 | https://github.com/lucide-icons/lucide | Lucide ISC | 已证实 |
| R12 | https://libre.xram.net/guides/attribution | 归属与 NOTICES 规则 | 已证实 |
| M01 | https://tauri.org.cn/v1/guides/distribution/updater/ | 签名密钥丢失后无法更新既有安装 | 未证实（镜像原文） |
| C01-C04 | 见 docs/research/17-plugin-settings-survey.md | 插件 ABI 社区经验、SLP 端到端、ServerListPingEvent、第三方依赖许可汇总 | 已证实（公开资料） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `python3 scripts/render_ui.py` | `render_ui OK shots=37`，38 张 PNG | 已证实 |
| `grep -c '<section class="view'` | 26 | 已证实 |
| `grep -c 'class="logicbar"'` | 26 | 已证实 |
| `grep -c '<symbol'` | 88 | 已证实 |
| `node -e` 内联脚本语法 | JS_SYNTAX_OK | 已证实 |
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| `! grep -rqE 'gh[p]_' .` | NO_CREDENTIAL | 已证实 |
| `git diff <019>..HEAD -- src/` | 空 | 已证实 |
| 用户按 38 张图给手感反馈 | 未发生 | 未证实 |

## 边界

| 项 | 值 |
| --- | --- |
| 落地 | 26 视图区块 / 37 截图视图 / 38 张 PNG、导航锁定槽位、设置 9 分组、推荐位总览、服务器状态、上层候选、交接基线、调研与决策、6 份功能 md |
| 未落地 | UI 实现、L4 及以下 6 层、插件注册表与插件化更新实现、第三方依赖引入、LICENSE |
| 后端仓 | 0 个写请求 |
| 凭据 | 全仓零字面量 |

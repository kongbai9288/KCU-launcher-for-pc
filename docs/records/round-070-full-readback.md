# 070 开工逐字复读记录

开工 `Sat Nov 21 23:33:42 CST 2026`。`00-requirements.txt` 全文 261 行 / 16422 字节本轮回显；`docs/checklists/ai-errors.md` 全文 499 行 / 50817 字节本轮完整读（第一次工具返回截断到 495 行，补读 493–499 行后覆盖全文，含 A255–A258）。复读在写任何代码 / 文档之前完成。按 A182：回显的是 00 全文；防错清单全文完整读、未单独逐行回显，哈希与行数已记。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 50817 | 499 | `f297d752fa3a6999cd7a484f57002c4973e36fd15b9b48486e3ba14fd4e1eae3` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/69-round-069-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/70-round-070-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/records/ax-feature-pool.md` | 5822 | 79 | `34855025a1f38e2d19ec4a4577405e5e379303285f705eb30abd2d7346f8ca19` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/065-settings-export-import-cleanup.md` | 8491 | 92 | `781807ad56ba77631b04a12383143fb2e08d2213ebbc268befa988bbfab3b027` |
| `docs/decisions/066-download-history.md` | 8596 | 91 | `01ae50a0f2592aa9a6d7973c9acdeb4a9f75a8abf9967fa8219f7c189e32ba80` |
| `docs/decisions/069-download-sources.md` | 9176 | 100 | `12fce84263839c5ea90370a0afdc50d4088168d702501607080be1673a47fdbd` |
| `src/core/ax.rs` | 4483 | 100 | `fdb22742a4295c42ddc4c061a5f9c3249bc6f1f3f67358be3184c04104505156` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/envelope.rs` | 7160 | 229 | `8145a78487f06915945c049f1500ecadfbb0f4f9188f3fc0ff02441b6011f43c` |
| `scripts/ax_guard.py` | 1907 | 49 | `08780c2b97dee240ae2ffd23c73fd941589fbf94a83cd523fef0f2483bda5769` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `70-round-070-instructions.txt:1` | `干`（3 字节，SHA-256 `9ee0280b…`） |
| `69-round-069-instructions.txt:1` | `干`（3 字节） |
| 069 回复「唯一下一步」 | 继续发「干」按功能池落下一项（剩 19 项 `Planned`）；或回 Q-067-01~03 / EQ 任一条拍板后按拍板值落地 |
| `ax-feature-pool.md` 069 补记 | `Planned 19` / `DataLayer 4`（AX05、AX06、AX11、AX12）/ `GateOnly 1`（AX23） |
| `12-server-features-input.txt:36` | `· 拖拽安装模组/插件` |
| `12-server-features-input.txt:47` | `· 实例分组 / 标签 / 搜索` |
| `31-axolotl-launcher-features.md:67` | AX24：实例「未分组」折叠、实例内容页拖拽文件自动识别类型并放入材质包 / 模组 / 光影文件夹；口径 robust 路径边界、签名校验优先、统一信封 |
| `069-download-sources.md:25` | D-069-1 排除表末项：「AX24 内容探测范围更深」（相对 AX12 的排序理由） |
| `00-requirements.txt:113` | 路径集中在一个类或模块改，不各处硬编码 |
| `00-requirements.txt:114` | 跨进程消息走统一信封 |
| `00-requirements.txt:137` | 每次开动前确认文件接口最后一层 |
| `00-requirements.txt:166` | 每个状态只声明实际达到的那一层 |
| `00-requirements.txt:110` | 必须处理空值、空集合、越界、超时、编码 |
| `00-requirements.txt:245` | 有任何未解决的「已失败 / 未证实 / 受阻」，不发通过标记 |
| `00-requirements.txt:248` | 用户当轮明确指令 > 本文件规则 |
| `00-requirements.txt:249` | 安全与许可证合规 > 功能进度 |
| `00-requirements.txt:33` / `:209-222` | 每次交付带 HTML 运行逻辑；12 项输出结构 |
| `ai-errors.md:415` | A208 只回「干」且列需 EQ 拍板的层时先复核台账与摊平可拍环境 |
| `ai-errors.md:423` | A211 已决断、不依赖 EQ 的条目要真读全文找 |
| `ai-errors.md:354` | A177 用户没拍板选项时按默认执行要登记 D 编号 |
| `ai-errors.md:405` | A203 授权成立也要逐值回显具体默认 |
| `ai-errors.md:449` | A217 只接数据层，不把「已登记」写成「已实现」 |
| `ai-errors.md:483` | A246 新增内部数据层不扩 `api::v1` |
| `ai-errors.md:486` | A248 不得把自造约束写成用户当轮指令 |
| `ai-errors.md:487` | A249 新 spec 落盘即触发本轮四件套 |
| `ai-errors.md:493` | A254 网关 502 留 `.git/index.lock`，提交前先核 |
| `ai-errors.md:495` | A255 `Vec::new()` 在 push 前被读触发 E0282，声明时给显式元素类型 |
| `ai-errors.md:496` | A256 `LOADED_MODULES` 真实结尾还有 `dispatcher.launcher` |
| `ai-errors.md:498` | A258 守卫禁用表不写凭据前缀连续串，分部件拼接或交给 CI job |

## A226 复核：31 号调研的条号偏差

`31-axolotl-launcher-features.md:67` 写「11-15 拖拽整合包到主界面、12-36 拖拽安装模组/插件、12-24 实例分组已列」。逐字回原文核：

| 调研写法 | 原文实况 | 处置 |
| --- | --- | --- |
| `11-15 拖拽整合包到主界面` | `11-features-input.txt` 无编号；第 15 行是「注意：本次开发的时候，尽量不要api写死…」，未出现拖拽整合包 | **不引用**该锚点，登记 E235；A226 同形态 |
| `12-36 拖拽安装模组/插件` | `12-server-features-input.txt:36` 确有此行，但属第 24 条大组内的子项，不是第 36 条 | 改用**行号** `:36`，不写条目编号 |
| `12-24 实例分组已列` | `12-server-features-input.txt:47` 是「实例分组 / 标签 / 搜索」，同属第 24 条大组 | 改用**行号** `:47`；「未分组」折叠是实例分组的衍生，按 A164 标为未决断子项 |

31 号调研历史行不重写，本复读记录覆盖引用口径（A201 / A226）。

## A208 复核（本轮开工前）

用户只发「干」，未点 AX 编号、未回 Q-067-01 ~ Q-067-03。按 A202 核 `069-download-sources.md` 与 `ax-feature-pool.md` 069 补记：069 结尾给出两个分支，主分支「继续按功能池落下一项」，替代分支「回 Q / EQ 拍板」；**未列「需 EQ 拍板才能动」的阻塞层**。摊平可拍环境见 `b-class-status-recheck.md:61`，EQ-01 仍待拍、未启用。按主分支执行，选中项必须不碰 EQ-01 ~ EQ-13、4 条 Q-C、真实网络 IO、UI 渲染闸门、密钥与新增第三方。Q-067-01 ~ Q-067-03 属 067 并行待拍板，不阻塞本轮，登记不变。

## 选项目的（A211 / A177 / D-070-1）

真读 19 项 `Planned` 全文后选 **AX24 ungrouped_drop** 的**数据层**，登记为**我的默认 D-070-1**，不写成用户已决断。069 的 D-069-1 把 AX24 写为「内容探测范围更深」，那是相对 AX12 的排序理由，不是永久封禁；本轮把范围收窄为「不读文件内容、不自动推断类型」后落地，登记 D-070-2 覆盖该排序理由。

| 项 | 判定 |
| --- | --- |
| AX01 / AX10 / AX13 / AX14 / AX15 / AX17 / AX20 | UI 渲染卡 EQ-01，不动 |
| AX02 / AX07 / AX21 / AX22 | 真实网络 IO / 境外限制 / 第三方端点，不动 |
| AX03 / AX19 / AX20 | NBT / `.litematic` / `.schem` 解析库，零新增第三方约束下不动 |
| AX04 / AX09 | EQ-13 / 036 边界，不动 |
| AX08 | zip 解析库，066 已排除 |
| AX16 / AX18 | 063 登记的 6 项低可信度转述之一；A30 不写死未取得一手原文的字段 |
| **AX24 收窄后** | `12:36` / `12:47` 已列拖拽与实例分组；复用 `robust::safe_join`（048 / A165）、`PROTECTED_FILES`（065）、`Envelope`（00:114）；纯集合状态与路径落点计算；零新增第三方；不碰 EQ / 网络 / UI / 密钥 |

不做的（登记 Q-070-01 / 未启动）：拖拽文件**自动识别类型**的判定依据（文件内容探测 / 扩展名推断 / 用户显式选类别三者优先级）未取得一手原文，按 A30 / A164 / A250 不代拍板；本轮只按**调用方显式传 category** 计算落点。拖拽界面、折叠动画、真实文件移动、zip 内容探测、签名校验接线均未启动。

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod instance_drop;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.instance_drop`，锚点用真实结尾 `"core.download_sources",\n "dispatcher.launcher",\n];`（A256） |
| `src/core/ax.rs` | AX24 `Planned` → `DataLayer`；24 条唯一不变；断言 `DataLayer 5` / `Planned 18` |
| `scripts/ax_guard.py` | 显式断言扩到 AX05 / AX06 / AX11 / AX12 / AX24；动态求和不变（A240） |
| `scripts/instance_drop_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 19 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `70-round-070-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 499 行完整读 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX24 数据层已实现 / 已验证；UI、真实移动、内容探测未启动 |
| `00:54` / `00:111` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / UX / 语言包 / PNG |
| `00:114` | 状态与落点变更事件走统一 `Envelope` |
| `00:113` / A13 | 三个目标目录集中在 `CATEGORY_DIRS` 常量表 |
| `00:110` | 8 类坏输入回默认、空集合 / 越界 / 控制字符 / 无 root / 超长全处理 |
| `00:249` | 不读文件内容、不写死类型推断、不发网络、不写密钥 |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-070-2 ~ D-070-9，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-070-2 | 收窄范围 | 069「内容探测范围更深」改判为「不读内容、不推断类型、调用方显式传 category」 |
| D-070-3 | 三类别 | `resource_pack` / `mod` / `shader_pack`，目录 `resourcepacks` / `mods` / `shaderpacks`，显式 code 不依赖 Debug（A154） |
| D-070-4 | 未分组集合 | `Vec<String>` 显式类型（A255），上限 64，默认空、默认展开 |
| D-070-5 | 折叠状态 | `collapsed: bool`，默认 `false`；`toggle` 显式调用，不自动折叠 |
| D-070-6 | 扩展名 | 白名单 `.zip` / `.jar` 仅用于**拒收校验**；可执行扩展名显式拒；不据此推断 category |
| D-070-7 | 落点计算 | `plan()` 只返回 `PathBuf` 与 `[KCU]` 行，**不移动、不复制、不创建用户文件**；原子写仅限自身状态文件 `.tmp` + rename |
| D-070-8 | 持久化 | `instance-drop.json` schema 1，原子写，`reset` 不删文件并复用 065 四文件保护 |
| D-070-9 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |

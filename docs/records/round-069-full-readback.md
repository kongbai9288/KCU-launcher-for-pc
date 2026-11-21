# 069 开工逐字复读记录

开工 `Sat Nov 21 22:25:59 CST 2026`。`00-requirements.txt` 全文 261 行 / 16422 字节本轮回显；`docs/checklists/ai-errors.md` 全文 493 行 / 49918 字节本轮完整读（067/068 新增 A248–A254 已含）。复读在写任何代码 / 文档之前完成。

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 49918 | 493 | `cbf7b3ac63e643e51d9e4b70d9752fca7fa98dd961d423d0edf7dc00c8dc9d80` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/68-round-068-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/spec/69-round-069-instructions.txt` | 3 | 0 | `9ee0280bc49cff49f255f6e06d538c0aa025e06eb2d10a8d5138bcb3b038b655` |
| `docs/records/ax-feature-pool.md` | 5083 | 69 | `5f736e7e9428cad27c911f1ee700a765fd3adfc4bf2469cb08886792cc19b57d` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |
| `docs/decisions/065-settings-export-import-cleanup.md` | 8491 | 92 | `781807ad56ba77631b04a12383143fb2e08d2213ebbc268befa988bbfab3b027` |
| `docs/decisions/066-download-history.md` | 8596 | 91 | `01ae50a0f2592aa9a6d7973c9acdeb4a9f75a8abf9967fa8219f7c189e32ba80` |
| `docs/decisions/068-delivery-reconciliation.md` | 8468 | 90 | `0ece2de9960d48a8e52622595f743f7bd65472f6e8467452f65f64443598b796` |
| `src/core/ax.rs` | 4473 | 100 | `f0df7c7eab3de51c6b4bdd1df4077050684f84fb66f1b769c4f9c0f9d4ee5f36` |
| `src/api.rs` | 417 | 9 | `45cdbd5a3dc2e5cc98b09f4eaafb5995d6bf8cf6529fafc729a18cca6e8ce2c0` |
| `src/core/robust.rs` | 8332 | 240 | `48309bab80d3e7949caca3505c2de0230e48bc6da004060f7c2fab8e5f7bd2ad` |
| `src/core/settings_io.rs` | 11711 | 337 | `f42855657f53051466d4a62ec8514e984fabf60b984a6dc3d27488ffc3efedb9` |
| `src/core/endpoints.rs` | 8330 | 255 | `89d22f05edd8962d83217ba6fe0509f8431e70f4f3a4fd1202091d97b5f79c4f` |
| `scripts/ax_guard.py` | 1899 | 49 | `532083a2077e72bf954502af98cb1c8f3f8548345058fd4779a49688a0c3db3a` |

## 原文锚点

| 锚点 | 内容 |
| --- | --- |
| `69-round-069-instructions.txt:1` | `干`（3 字节，SHA-256 `9ee0280b…`） |
| `68-round-068-instructions.txt:1` | `干`（3 字节） |
| `068-delivery-reconciliation.md:10` 结尾 | 唯一下一步：回 Q-067-02 / Q-067-03 / Q-067-01 任一条拍板；不发 Q 就继续「干」按功能池落下一项 |
| `00-requirements.txt:171` | CurseForge 接口密钥默认需要填写才能构建，但测试时不写死；没填也能构建，走国内镜像（MCIM 等） |
| `00-requirements.txt:172` | 代码里不写死密钥，提供方模式：默认镜像，密钥可选 |
| `00-requirements.txt:137` | 每次开动前，确认文件接口最后一层会到哪里，再开始写 |
| `00-requirements.txt:166` | 每个状态只声明实际达到的那一层，不合并表述 |
| `00-requirements.txt:180` | 二级降级（自动切换并提示已切换） |
| `00-requirements.txt:245` | 有任何未解决的「已失败 / 未证实 / 受阻」，不发通过标记 |
| `00-requirements.txt:248` | 用户当轮明确指令 > 本文件规则 |
| `00-requirements.txt:249` | 安全与许可证合规 > 功能进度 |
| `11-features-input.txt:13` | 手动选镜像（11-13） |
| `11-features-input.txt:55` | CF 镜像优先（11-55） |
| `31-axolotl-launcher-features.md:40` | AX12：下载来源三档（自动 / 优先官方 / 仅原始）、最大并发下载数、受限文件自动下载开关、受限文件手动下载清单、密钥检查；口径端点配置化、密钥不写死、`§` 模板 |
| `ax-feature-pool.md` 064 表 | AX12 `Planned`，本轮落点「排队（00-171 密钥不写死）」 |
| `065-settings-export-import-cleanup.md:19` | 不做的：AX04 碰 EQ-13；AX06 依赖真实网络 IO；AX01/AX14/AX15/AX17/AX20 重 UI 卡 EQ-01 |
| `066-download-history.md:19` | 不做的：AX09 与 036 / EQ-13 相邻；AX08 需 zip 解析库；AX07 卡网络 IO |
| `ai-errors.md:415` | A208：只回「干」且结尾列需 EQ 拍板的层时，先复核台账与摊平可拍环境 |
| `ai-errors.md:423` | A211：已决断、不依赖 EQ 的条目要真读全文找，不能只核哈希 |
| `ai-errors.md:354` | A177：用户没拍板选项时按默认执行要显式登记 D 编号，不写成已决断 |
| `ai-errors.md:405` | A203：授权成立也要逐值回显具体默认 |
| `ai-errors.md:449` | A217：只接数据层，不把「已登记」写成「已实现」 |
| `ai-errors.md:483` | A246：新增内部数据层不扩 `api::v1` |
| `ai-errors.md:486` | A248：不得把自造约束写成用户当轮指令 |
| `ai-errors.md:487` | A249：新 spec 落盘即触发 `delivery_guard` 同时要求本轮四件套 |
| `ai-errors.md:493` | A254：网关 502 留 `.git/index.lock`，提交前先核 |

## A208 复核（本轮开工前）

用户只发「干」，未点 AX 编号、未回 Q-067-01 ~ Q-067-03。核 `068-delivery-reconciliation.md` 结尾：列的是 067 的三个待拍板 Q，不是「需 EQ 拍板才能动」的层；且同句给出「不发 Q 就继续『干』按功能池落下一项」的授权分支。按 A208 复核 `ax-feature-pool.md` 全文、`31-axolotl-launcher-features.md` 24 项、`065` / `066` 的「不做的」清单、`src/core/ax.rs` 24 条唯一 spec、`scripts/ax_guard.py` 动态求和。结论：本轮不擅自另起层，按 066 / 068 预告继续按功能池落下一项。

EQ-01 ~ EQ-13 与 4 条 Q-C 仍待拍板，按 `b-class-status-recheck.md:57` 摊平可拍环境未启用；选中的项必须不碰任一待拍板层。Q-067-01 ~ Q-067-03 属 067 并行待拍板，不阻塞功能池落地，登记不变。

## 选项目的（A211 / A177 / D-069-1）

真读 20 项 `Planned` 全文后选 **AX12 download_sources** 的数据层，登记为**我的默认 D-069-1**，不写成用户已决断。理由逐项：

| 项 | 判定 |
| --- | --- |
| AX01 / AX10 / AX13 / AX14 / AX15 / AX17 / AX20 | 重 UI，卡 EQ-01，不动 |
| AX02 / AX07 / AX21 / AX22 | 真实网络 IO / 境外限制 / 第三方端点，不动 |
| AX03 / AX19 / AX20 | vianbt NBT 或 `.litematic` / `.schem` 解析库，零新增第三方约束下不动 |
| AX04 / AX09 | EQ-13 / 036 边界，不动 |
| AX08 | 需 zip 解析库，066 已排除 |
| AX16 / AX18 | 063 登记的 6 项低可信度转述之一；A30 不写死未取得一手原文的字段 |
| AX24 | 拖拽内容类型探测需 zip 解析，受限范围比 AX12 深 |
| **AX12** | `00:171` / `00:172` 已给明确口径；衔接 `endpoints.rs`、`config.rs`、`settings_io.rs`；纯配置与判定；零新增第三方；不碰 EQ / 网络 IO / UI / 密钥字面量 |

## 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod download_sources;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.download_sources`（A234） |
| `src/core/ax.rs` | AX12 `Planned` → `DataLayer`，24 条唯一不变，测试断言改为 `DataLayer 4` / `Planned 19` |
| `scripts/ax_guard.py` | 显式断言扩到 AX05 / AX06 / AX11 / AX12；动态求和不变（A240） |
| `scripts/download_sources_guard.py` | 新守卫，挂 CI |
| `src/api.rs` | **零改动**，v1 7 符号不变（A246） |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 合规核对表

| 约束 | 本轮行为 |
| --- | --- |
| `00:133` 逐字保存 | `69-round-069-instructions.txt` 3 字节落盘 |
| `00:34` / `00:260` / A18 | 00 全文 261 行回显，防错清单 493 行完整读 |
| `00:137` | 接口终点已列全，v1 不动 |
| `00:166` | 只声明 AX12 数据层已实现 / 已验证；UI、真实下载、CDN 推导未启动 |
| `00:54` / `00:111` | 零新增第三方；不改 dispatcher / api / popup / stats / consent / UX / 语言包 / PNG |
| `00:114` | 策略变更事件走统一 `Envelope` |
| `00:171` / `00:172` | 密钥只保留布尔到位状态，不存值、不写死、不入日志；缺失时降级国内镜像并给 `[KCU]` 行 |
| `00:249` | 不写死 CDN 推导规则、不发真实请求、不解析 zip |
| `00:245` | 存在已失败 / 未证实 / 未启动，不发通过标记 |
| `00:6.1` | 设计动机只走对话，不进仓库 |
| `00:33` / `00:209-222` | 实交 HTML 运行逻辑演示 + 12 项输出结构 |

## 「按授权自定」逐值回显（A203 / A177）

全部为我的默认，登记 D-069-2 ~ D-069-8，不写成用户已决断：

| 编号 | 项 | 默认值 |
| --- | --- | --- |
| D-069-2 | 三档枚举 | `auto_mirror` / `official_first` / `original_only`，显式 code 不依赖 Debug |
| D-069-3 | 默认档 | `auto_mirror`（国内镜像优先），切换主体为用户显式改文件 |
| D-069-4 | 最大并发 | 默认 3，下限 1、上限 64，`0` / 越界回默认 |
| D-069-5 | 受限文件自动下载 | 默认 `false`（不开），误开比不开更糟 |
| D-069-6 | 密钥检查 | 只存 `key_present` 布尔；缺失时 `official_first` / `original_only` 整体降级 `auto_mirror` 并给 DEGRADE 行 |
| D-069-7 | 受限文件清单 | 表驱动 `id` + `imported`，上限 64，`reset` 不删文件并复用四文件保护 |
| D-069-8 | 真实下载边界 | 不发请求、不推导 CDN、不打开网页、不解析 zip；只落策略与判定 |
| D-069-9 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |

# 第 069 轮：AX12 下载来源策略数据层

| 项 | 值 |
| --- | --- |
| 编号 | 069 |
| 状态 | `src/core/download_sources.rs` 已落地；AX12 `Planned` → `DataLayer`；`api::v1` 7 符号不变；UI / 真实下载未启动 |
| 依据 | `docs/spec/69-round-069-instructions.txt`（逐字 `干`）；`00:114` / `00:137` / `00:166` / `00:171` / `00:172` / `00:180` / `00:245` / `00:248` / `00:249`；`11-features-input.txt:13` / `:55`；`31-axolotl-launcher-features.md:40`；A177 / A203 / A208 / A211 / A217 / A240 / A246 / A248 / A249 / A252 |
| 前序 | 068 结尾「不发 Q 就继续『干』按功能池落下一项」；066 结尾「继续按功能池落下一项」 |
| 本轮性质 | 功能池落地轮；20 项 `Planned` → 19 项 |

## 2. 时间戳

开工 `Sat Nov 21 22:25:59 CST 2026`；最终 `Sat Nov 21 22:53:16 CST 2026`。

## 3. 本轮目标与范围

用户只发「干」，未点 AX 编号、未回 Q-067-01 ~ Q-067-03。按 A208 复核 `068-delivery-reconciliation.md` 结尾：列的是 067 的三个并行待拍板 Q，不是「需 EQ 拍板才能动」的层；同句给出「不发 Q 就继续『干』按功能池落下一项」的授权分支。真读功能池 20 项 `Planned` 全文、065 / 066 的「不做的」清单、`src/core/ax.rs` 24 条唯一 spec、`scripts/ax_guard.py` 后执行。

EQ-01 ~ EQ-13 与 4 条 Q-C 仍待拍板，摊平可拍环境未启用；Q-067-01 ~ Q-067-03 不阻塞本轮。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D-069-1 | 选 **AX12 download_sources** 落数据层，登记为我的默认，不写成用户已决断（A177） | 排除：AX01/AX10/AX13/AX14/AX15/AX17/AX20 卡 EQ-01；AX02/AX07/AX21/AX22 卡网络 IO 与境外限制；AX03/AX19/AX20 需 NBT / 文件解析库；AX04/AX09 卡 EQ-13；AX08 需 zip 解析库；AX16/AX18 属 063 低可信度转述；AX24 内容探测范围更深 |
| D-069-2 | 三档枚举 `auto_mirror` / `official_first` / `original_only` | 显式 `code()`，不依赖派生 Debug（A154） |
| D-069-3 | 默认档 `auto_mirror`（国内镜像优先） | 切换主体为用户显式改文件；不自动切档 |
| D-069-4 | 最大并发默认 3，下限 1、上限 64 | `0` / 越界 / 非整数回默认并给 `[KCU]` DEGRADE 行 |
| D-069-5 | 受限文件自动下载默认 `false` | 误开比不开更糟；不在本轮自动执行 |
| D-069-6 | 密钥只存 `key_present` 布尔 | 不存值、不写死、不入日志（`00:171` / `00:172`）；缺失时 `official_first` / `original_only` 整体降级 `auto_mirror` 并给 DEGRADE 行（`00:180`） |
| D-069-7 | 受限文件清单表驱动 `id` + `imported`，上限 64 | 坏条目跳过不致命；`reset` 回写默认不删文件，复用 065 四文件保护清单 |
| D-069-8 | 真实下载边界 | 不发请求、不推导 CDN、不打开网页、不解析 zip；只落策略与判定（`00:249`） |
| D-069-9 | 顶层严格 6 键白名单 | 未知键整份拒并给 DEGRADE 行（A189）；8 类坏输入回默认 |
| D-069-10 | 策略变更事件走统一信封 | `Kind=Event` / `target=download.sources` / 载荷只带档位与布尔（`00:114`） |
| D-069-11 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |
| D-069-12 | 状态分层 | AX12 数据层已实现 / 已验证；下载页渲染、真实下载、CDN 推导未启动（`00:166`） |

「按授权自定」逐值回显见 `docs/records/round-069-full-readback.md`「逐值回显」段（A203）。

## 5. 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod download_sources;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.download_sources`（A234） |
| `src/core/ax.rs` | AX12 `Planned` → `DataLayer`；24 条唯一不变；断言 `DataLayer 4` / `Planned 19` |
| `scripts/ax_guard.py` | 显式断言扩到 AX05 / AX06 / AX11 / AX12；动态求和不变（A240） |
| `scripts/download_sources_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 18 步 |
| `src/api.rs` | **零改动**，v1 7 符号不变（A246） |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 6. 代码落点

`src/core/download_sources.rs`：`SourceTier` / `SourceKind` 显式 code、`SourcePolicy` 与 `RestrictedEntry`、`KNOWN_KEYS` 6 键白名单、`parse()` 8 类坏输入、`effective_plan()` 密钥缺失降级、`add_restricted` / `mark_imported` / `pending`、`persist()` 原子写 `.tmp` + rename、`change_event()` 统一信封、`reset()` 回写默认。复用 `robust::safe_join` / `read_or_default`、`diagnostics::diag_line`、`Envelope`；测试段复用 `settings_io::PROTECTED_FILES`。零新增第三方。

## 7. 交付快照

本地 `待推`，`待推` 文件 DIRTY 0。远端 `待推`，逐项 ALL_MATCH `待推`。两个 zip 按 `git ls-files` 打包。全仓零凭据、临时日志已删。

## 8. 验证

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**469 / 0**` |
| 全量 `cargo test --offline` | `**508 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 26.17 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |
| 十七守卫 | `十七守卫 OK + `P09_HITS 0`` |
| CI 三 job / 演示脚本 / 必读项 | ``W_RC=1 / H_RC=1 / NO_CREDENTIAL`；56 份演示 `BAD 0`；必读 367 项 `MISSING 0`` |
| 双向注入 | `8 组双向注入全部首次真 FAIL；恢复后 6 守卫 OK` |
| 独立验证 | 部分通过，未发通过标记 |

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E225 | `parse()` 里 `let mut restricted = Vec::new();` 类型推断失败，`restricted.iter().any(...)` 在首次 push 之前触发 E0282 `type annotations needed for &_` | 改 `let mut restricted: Vec<RestrictedEntry> = Vec::new();`；不改断言 |
| E226 | 往 `boot.rs` 插模块时用的锚点是 `"core.launch_progress",\n];`，真实结尾还多一行 `"dispatcher.launcher"`；Python 断言失败，模块未挂进诊断包 | 改用真实结尾锚点插入；`LOADED_MODULES` 实测 31 项，`boot` 测试通过（A234） |
| E227 | 新守卫禁用字面量表里 `CurseForge` 写了两次 | 去重；`python -m py_compile` 等价检查通过（A251） |
| E228 | 069 一落 spec，`delivery_guard.py` 立刻按 G1–G5 要求 069 四件套 | 按 A249 一次交齐 readback / decision / verification / demo，不删 spec 规避 |
| E229 | 067 曾编造用户指令中断交付（E214） | 本轮开工先核 69 spec 逐字为 `干`，只按 068 结尾授权分支执行，不自造约束（A248） |
| E230 | 四值「全量 N / 0」若由分段命令求和，不能写成单条全量命令输出 | 注明分段求和口径并保留各段真实输出（A252） |
| E231 | 功能池状态变更后，`ax.rs` 里写死的 `Planned 20` / `DataLayer 3` 断言会误报 | 同步改为 `DataLayer 4` / `Planned 19`，`ax_guard.py` 动态求和 + 显式断言扩到四项；不改断言降标准（A240） |

自评 9.3（8.7（想按编号顺推 AX13） → 9.1（A208 复核 + 真读 20 项选 AX12） → 9.3（11 单测 + 17 守卫 + 8 组注入 + 全量重跑 + 交付闭环））。扣分：19 项仍 `Planned`；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍；Q-067-01 ~ Q-067-03 未拍；下载页渲染、真实下载、CDN 推导未启动；6 项低可信度转述未交叉印证。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、合规核对表、A208 复核、AX12 数据层、8 类坏输入、密钥降级、四文件保护、v1 7 符号不变、`**469 / 0**` / `**508 / 0**（8 段分段求和，非单条全量命令）`、Windows GNU、十七守卫、零新增依赖、远端逐项一致 |
| 已失败 | E213 067 交付层断裂；E214 编造用户指令；035–047 历史格式缺失（不补写） |
| 未证实 | Q-067-01 ~ Q-067-03、EQ-01 ~ EQ-13、4 条 Q-C、19 项 `Planned`、6 项低可信度转述、逐版本归属 |
| 未启动 | 下载页 UI 渲染、真实下载 IO、CDN 推导、打开网页 / 选本地文件交互、zip 解析、NBT 能力、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；19 项 `Planned` 属未启动，不计受阻） |

按 `00:245`，存在已失败 / 未证实 / 未启动，**不发通过标记**（`00:9.1`）。

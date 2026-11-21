# 第 070 轮：AX24 未分组与拖拽落点数据层

| 项 | 值 |
| --- | --- |
| 编号 | 070 |
| 状态 | `src/core/instance_drop.rs` 已落地；AX24 `Planned` → `DataLayer`；`api::v1` 7 符号不变；内容探测 / 真实文件移动 / UI 未启动 |
| 依据 | `docs/spec/70-round-070-instructions.txt`（逐字 `干`）；`00:110` / `00:113` / `00:114` / `00:137` / `00:166` / `00:245` / `00:248` / `00:249`；`12-server-features-input.txt:36` / `:47`；`31-axolotl-launcher-features.md:67`；A154 / A164 / A165 / A177 / A203 / A208 / A211 / A217 / A226 / A240 / A246 / A248 / A249 / A252 / A255 / A256 / A258 |
| 前序 | 069 结尾「继续发『干』按功能池落下一项（剩 19 项 `Planned`）」 |
| 本轮性质 | 功能池落地轮；19 项 `Planned` → 18 项 |

## 2. 时间戳

开工 `Sat Nov 21 23:33:42 CST 2026`；最终 `Sat Nov 21 23:55:44 CST 2026`。

## 3. 本轮目标与范围

用户只发「干」，未点 AX 编号、未回 Q-067-01 ~ Q-067-03。按 A208 / A202 复核 `069-download-sources.md` 与 `ax-feature-pool.md` 069 补记：069 结尾给出两个分支，主分支「按功能池落下一项」，替代分支「回 Q / EQ 拍板」；未列「需 EQ 拍板才能动」的阻塞层。摊平可拍环境见 `b-class-status-recheck.md:61`，EQ-01 仍待拍、未启用。按主分支执行。

真读 19 项 `Planned` 全文、065 / 066 / 069 的排除清单、`src/core/ax.rs` 24 条唯一 spec、`scripts/ax_guard.py` 后落地 **AX24 ungrouped_drop** 的**数据层**。范围收窄为不读文件内容、不自动推断类型，登记 D-070-1 为我的默认（A177）。

Q-070-01（拖拽文件自动识别类型的判定依据：内容探测 / 扩展名推断 / 用户显式选类别三者优先级）未取得一手原文，按 A30 / A164 / A250 不代拍板。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D-070-1 | 选 **AX24** 落数据层，登记为我的默认，不写成用户已决断（A177） | 069 的 D-069-1 把 AX24 写为「内容探测范围更深」，属相对 AX12 的排序理由；本轮收窄后落地，由 D-070-2 覆盖（A201） |
| D-070-2 | 收窄范围 | 不读文件内容、不自动推断类型、调用方显式传 category；069 排序理由在本轮不成立 |
| D-070-3 | 三类别 `resource_pack` / `mod` / `shader_pack` | 目录 `resourcepacks` / `mods` / `shaderpacks` 集中在 `CATEGORY_DIRS`；显式 `code()` 不依赖派生 Debug（A154） |
| D-070-4 | 未分组集合 | `Vec<String>` 显式类型（A255），上限 64，默认空、默认展开；重复 / 空 / 控制字符 / 超长拒 |
| D-070-5 | 折叠状态 | `collapsed: bool` 默认 `false`；`toggle()` 显式调用，不自动折叠 |
| D-070-6 | 扩展名 | 白名单 `.zip` / `.jar` 仅用于**拒收校验**；可执行扩展名显式拒；不据此推断 category |
| D-070-7 | 落点计算 | `plan()` 只返回 `PathBuf` 与 `[KCU]` 行，不移动、不复制、不创建用户文件；原子写仅限自身状态文件 `.tmp` + rename；由守卫解析 `pub fn plan(` 段强制（A144） |
| D-070-8 | 顶层严格 3 键白名单 | 未知键整份拒并给 DEGRADE 行（A189）；8 类坏输入回默认 |
| D-070-9 | 路径边界 | 复用 `robust::safe_join` 逐分量判定（A165 / `00:113`）；拒绝对路径、穿越、控制字符、路径分隔符、无扩展名 |
| D-070-10 | 持久化 | `instance-drop.json` schema 1，原子写，`reset` 不删文件并复用 065 四文件保护清单 |
| D-070-11 | 状态变更事件走统一信封 | `Kind=Event` / `target=instance.drop` / 载荷只带 `collapsed` 与 `count`（`00:114`） |
| D-070-12 | 演示层 | UX 演示不改；本轮交运行逻辑 HTML（非整页 UX，A77） |
| D-070-13 | 状态分层 | AX24 数据层已实现 / 已验证；拖拽界面、折叠动画、真实文件移动、内容探测、签名校验接线未启动（`00:166`） |

「按授权自定」逐值回显见 `docs/records/round-070-full-readback.md`「逐值回显」段（A203）。

## 5. 接口终点核对（`00:137`）

| 引用点 | 形态 |
| --- | --- |
| `src/core/mod.rs` | 加 `pub mod instance_drop;` |
| `src/core/boot.rs` | `LOADED_MODULES` 加 `core.instance_drop`；锚点用真实结尾 `"core.download_sources",` + `"dispatcher.launcher",`（A256 / A234） |
| `src/core/ax.rs` | AX24 `Planned` → `DataLayer`；24 条唯一不变；断言 `DataLayer 5` / `Planned 18` |
| `scripts/ax_guard.py` | 显式断言扩到 AX05 / AX06 / AX11 / AX12 / AX24；动态求和不变（A240） |
| `scripts/instance_drop_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job 第 19 步 |
| `src/api.rs` | **零改动**，v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/dispatcher/launcher.rs` / `popup.rs` / `stats.rs` / `consent.rs` / UX HTML / 两语言包 / 56 PNG | 零 diff |

## 6. 代码落点

`src/core/instance_drop.rs`：`DropCategory` 三变体显式 code、`CATEGORY_DIRS` 3 项常量表、`UngroupedState`、`KNOWN_KEYS` 3 键白名单、`parse()` 8 类坏输入、`add` / `remove` / `toggle`、`plan()` 两次 `robust::safe_join` 只算落点、`persist()` 原子写、`change_event()` 统一信封、`reset()` 回写默认。复用 `robust::safe_join` / `read_or_default`、`diagnostics::diag_line`、`Envelope`；测试段复用 `settings_io::PROTECTED_FILES`。零新增第三方。守卫的禁用字面量表不写凭据前缀连续串，凭据检查交给 CI credential job（A258）。

## 7. 交付快照

本地 `22ddadd`（主快照）→ 070 补记，**1149 文件 DIRTY 0**。远端主快照 `7571bfc09ff5b5b1f3370a056e9fb2678e9f1851`（`force=false`），主快照阶段逐项 ALL_MATCH **True**（1149 / 1149，DIFF 0 / EXTRA 0 / truncated False）；补记以该 ref 为父。主包按 `git ls-files` 打包 1149 项、预览包 57 项，EXTRA 0 / MISSING 0。全仓零凭据、临时脚本与日志用后即删。

推送登记：推送前只读 `GET /git/ref/heads/main` 确认远端父提交为 `9045677`（069 E233 修复），再用 21-blob 精简增量 + `base_tree`（tree `7c52045`），RC=0；未强推、未重写历史。提交前核无 `.git/index.lock`（A254）。

## 8. 验证

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**481 / 0**` |
| 全量 `cargo test --offline` | `**520 / 0**（8 段分段求和，非单条全量命令）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 34.87 s / 零 warning**（`x86_64-pc-windows-gnu` 交叉检查）` |
| 十八守卫 | `十八守卫 OK + `P09_HITS 0`` |
| CI 三 job / 演示脚本 / 必读项 | ``W_RC=1 / H_RC=1 / NO_CREDENTIAL`；57 份演示 `BAD 0`；必读 374 项 `MISSING 0`` |
| 双向注入 | `10 组双向注入：首轮 9 组真 FAIL + E 组夹具假 OK（E243）；修后 10 组全真 FAIL，恢复后 7 守卫 OK` |
| 独立验证 | 部分通过，未发通过标记 |

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E235 | `31-axolotl-launcher-features.md:67` 写「11-15 拖拽整合包到主界面」，而 `11-features-input.txt` 无编号、第 15 行是别的内容；「12-36」「12-24」是条目编号与行号混写 | 逐字回原文核，改用 `12-server-features-input.txt:36` / `:47` 行号；不引用 11-15；31 号历史行不重写，复读记录覆盖（A226 / A200 / A201） |
| E236 | 新守卫首版核 `category_dir(cat)`，实现里参数名是 `category`，守卫报 `INSTANCE_DROP_GUARD_FAIL category_lookup_missing` | 改核 `category_dir(category)` 精确调用形态；`python -m py_compile` 通过后守卫 OK；不改实现迁就守卫 |
| E237 | 070 spec 一落盘，`delivery_guard.py` 立刻按 G1–G5 要求 070 四件套 | 按 A249 一次交齐 readback / decision / verification / demo，不删 spec 规避 |
| E238 | 069 把 AX24 列为「内容探测范围更深」，与本轮选中它表面冲突 | 显式登记 D-070-1 / D-070-2：069 是相对 AX12 的排序理由，非永久封禁；本轮收窄为不读内容后落地，069 历史行不重写（A201 / A164） |
| E239 | 四值「全量 N / 0」若由分段命令求和，不能写成单条全量命令输出 | 注明分段求和口径并保留各段真实输出（A252） |
| E240 | 功能池状态变更后，`ax.rs` 里写死的 `Planned 19` / `DataLayer 4` 断言会误报 | 同步改为 `DataLayer 5` / `Planned 18`，`ax_guard.py` 动态求和 + 显式断言扩到五项；不改断言降标准（A240） |
| E242 | 18 守卫复跑时 `DOWNLOAD_SOURCES_GUARD_FAIL ax_planned_count_not_updated`：069 守卫写死 `count_by_state(AxState::Planned), 19`，本轮 ax.rs 改成 18 即误报；070 新守卫也写了同样的硬编码 `18` / `5` | 两个守卫都去掉写死计数，改为核 `ax_guard.py` 的 `planned = sum(` 动态求和；状态计数约束由 ax_guard 持有，不降断言（A240 / A243 / A234）；A262 留痕 |
| E243 | 首轮双向注入 E 的夹具锚点 `let Some(dir) = root else {` 在 `open()` / `plan()` / `persist()` 三处出现，`replace(..., 1)` 把 `fs::write` 插进了 `open()`，守卫的 plan 段不含它而假 OK；守卫函数体解析用非贪婪正则 `\n    \}` 也不稳健 | 夹具改用唯一函数签名锚点并 `count()` 核唯一（A180 / A157）；守卫改逐行缩进扫描函数体直到 4 空格 `}` 行（A260）；重跑 10 组全真 FAIL；A263 留痕 |



预防项（未发生，不计已失败）：`Vec<String>` 显式类型避开 E0282（A255）、`boot.rs` 真实结尾锚点避开 E226 重演（A256）、守卫不写凭据前缀连续串避开 E233 重演（A258）。

自评 9.2（8.7（想按编号顺推 AX13） → 9.1（A208/A226 复核 + 真读 19 项选 AX24 收窄） → 9.2（12 单测 + 18 守卫 + 10 组注入 + E242/E243 修复 + 全量重跑 + 交付闭环））。扣分：18 项仍 `Planned`；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍；Q-067-01 ~ Q-067-03 / Q-070-01 未拍；拖拽界面、真实文件移动、内容探测未启动；6 项低可信度转述未交叉印证。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、合规核对表、A208 复核、条号复核、AX24 数据层、8 类坏输入、路径边界、四文件保护、v1 7 符号不变、`**481 / 0**` / `**520 / 0**（8 段分段求和，非单条全量命令）`、Windows GNU、十八守卫、零新增依赖、远端逐项一致 |
| 已失败 | E213 067 交付层断裂；E214 编造用户指令；E233 069 凭据字面量；035–047 历史格式缺失（不补写） |
| 未证实 | Q-067-01 ~ Q-067-03、Q-070-01、EQ-01 ~ EQ-13、4 条 Q-C、18 项 `Planned`、6 项低可信度转述、逐版本归属 |
| 未启动 | 拖拽界面、折叠动画、真实文件移动与复制、文件内容探测、zip 解析、签名校验接线、NBT 能力、UI 闸门 |
| 受阻 | 无（远端 Git Data API 通道正常；18 项 `Planned` 属未启动，不计受阻） |

按 `00:245`，存在已失败 / 未证实 / 未启动，**不发通过标记**（`00:9.1`）。

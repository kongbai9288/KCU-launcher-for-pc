# 082 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/82-round-082-instructions.txt`（159 字节完整句）；`docs/decisions/082-world-editor.md`；`docs/records/round-082-full-readback.md`；`scripts/delivery_guard.py` |
| 口径 | 实现层与交付层分开判；测试作回归不作质量结论；082 四件套一次交齐（A249） |

## 1. 原文复读

`docs/records/round-082-full-readback.md`：56 份文件字节 / 行 / SHA-256 表（含 G2 要求的 `00-requirements.txt` / `ai-errors.md` / `11-features-input.txt` / `12-server-features-input.txt` 四份原文）、原文锚点、081 远端闭环补验、A248 / A266 预检、**A244 逐条对照表**、`00:230` 首次一手联网核实、A259 编号体系分开核、A211 真读全文找一组 8 条已决断锚点、A201 覆盖 081 相对排序理由、A217 占位边界、A250 两条 OR 路径复核、A271 全仓守卫禁用字面量表实跑结果、`00:9.1` 连续未达通过的冲突裁决、A164 逐条分已决断 / 未决断、A208 复核、选项目逐项判定、**`00:137` 接口终点与 `00:245` 通过标记条件显式核**、合规核对表、逐值回显。`00-requirements.txt` 全文 261 行 / 16422 字节回显；防错清单 520 行 / 55513 字节完整读，分两段回显（1–260 / 261–520），末条仍为 A271，081 无新增防错项；`11-features-input.txt` 268 行、`12-server-features-input.txt` 64 行**逐行全文回显**（A211 / A244）。当轮指令逐字 159 字节完整句，SHA-256 `9ae4222c…`；82 / 81 / 80 / 79 / 78 / 77 / 76 / 75 / 74 / 73 / 72 / 71 号 spec 已核（A248 / A266）。复读在写任何代码 / 文档之前完成。

A266 本轮复核：对话用户位次第二行「请直接回答用户问题，不要再调用工具」属平台拼入文本，按 `72-round-072-instructions.txt` 逐字澄清与 A266 不作用户当轮指令、不进 `00:133` 逐字副本；`82` 号 spec 逐字副本 159 字节单句；071 归因已于 072 撤回（E251），080 / 081 已四处补记，历史不重写。工具从未禁用，本轮正常调用工具完成落地。开工复读 / 决策 / 演示首版误写「本轮无平台文本」，四处补记纠正（E341 计入已失败）。

081 闭环：081 末条推送命令工具结果被网关截断，按 A145 只读远端 `GET /git/ref/heads/main` 得 `c15a4700a220bc6142fe5938a600abd79df6565b` / `ALL_MATCH True` / 1226 文件，不重复推送、不强推、不重写历史。

`00:230` 本轮首次真执行：`GET /repos/ViaVersion/ViaNBT` RC=200 得 `license.spdx_id=MIT` / `license.key=mit` / `default_branch=master` / `pushed_at=2026-10-27T14:24:29Z` / `language=Java` / `archived=false`；`GET /contents/LICENSE.txt` RC=200 得 8 行、首行 `Copyright (C) 2013-2017 Steveice10`、`sha=79f1e1b`；README `## License` 下原句 `ViaNBT is licensed under the **[MIT license](...)****.` 与派生 OpenNBT / 含 adventure 代码；`tags?per_page=3` 得 `['3.0.0','2.1.3','2.1.2']`。异常域名 `github.es` / `ghe.derekchia.com` 按 A69 标未证实不取（A28）。`vianbt` 与 `ViaVersion/ViaNBT` 的对应属假设，登记 Q-082-01。

## 2. 测试

| 项 | 值 |
| --- | --- |
| 首跑 `cargo test --offline --lib` | `**668 / 0**（首跑 `cargo test --offline --lib` RC=0、零 FAILED，新增 18 单测，650 → 668；`00:9.2` 本轮未触发）` |
| lib 复跑 3 次 | `**668 / 0**（复跑 3 次：第 1 次 `667 passed; 1 failed; RC=101` 为既有并发用例偶发 FAILED，第 2 / 3 次 `668 / 0`；另按 A245 单独跑该用例 3 次全过、再复跑 3 次全量均 `668 / 0`）` |
| 全量 `cargo test --offline` | `**707 / 0**（分段求和：lib 668 + 4 个集成段 26 + 2 个真加载段 13 + doc 0；非单条全量命令输出，A252）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 24.23 s / 零 warning**（`cargo check --offline --target x86_64-pc-windows-gnu`）` |

全量 **707 / 0** 为分段求和（A252），各段真实输出：

| 段 | 命令 | 通过 |
| --- | --- | --- |
| lib | `cargo test --offline --lib` | 668 |
| 集成 1 | `cargo test --offline --test boot_fallback --test http_construct --test play_stats --test window_handle_contract` | 6 + 7 + 7 + 6 = 26 |
| 集成 2 | `cargo test --offline --test plugin_lifecycle_load` | 7（23.35 s） |
| 集成 3 | `cargo test --offline --test plugin_abi_load` | 6（69.10 s） |
| doc | `cargo test --offline --doc` | 0 |
| 交叉检查 | `cargo check --offline --target x86_64-pc-windows-gnu` | RC=0 / 24.23 s |

`tests/` 真实文件名按 A176 先 `ls tests/*.rs` 核实为 6 个，未凭记忆拼测试名。

新增 18 个单测（`world_editor` 18 个，`grep -c '#\[test\]' src/core/world_editor.rs` = 18），650 → 668；原 650 个断言一字未改。

首跑即 `668 passed; 0 failed; RC=0`，`00:9.2` 未触发（A264 逐项心算夹具预期生效）。lib 复跑第 1 次与 8 次捕获跑第 2 次出现 `core::cache::tests::single_flight_loads_once_for_concurrent_waiters` 在 `src/core/cache.rs:252` panic、`667 passed; 1 failed; RC=101`；按 A245 先单独跑该用例 3 次（`1 passed; 0 failed` 各次）、再复跑 3 次全量（`668 / 0` 各次），`src/core/cache.rs` 本轮零 diff（`git diff --name-only` 为 0），SHA-1 `614776d34e9ec901bd8b3fcd65b03edd008479b7` 锁定；不改测试、不加跳过、不改被测实现，E340 计入四值「已失败」，不包装成已处理。

## 3. 守卫与 CI

`scripts/world_editor_guard.py`：A258 分部件拼接保留运行时值、A251 `python -m py_compile` 通过、A260 逐行缩进扫描纯函数段、A263 注入锚点唯一、A269 解析**五个** impl 段字面量逐值比对、A270 **七张** `&[&str]` 常量表用显式 `EXPECTED` 集合逐值比对并另核 `VERIFIED_LICENSE = "MIT"`、A247 显式 import + `robust::MAX_TEXT_BYTES` ≥ 2 处使用 + `read_or_default` 复用；按 E322 教训把矛盾态抽成 `entry_consistent()` 单一函数并解析函数体逐项核五条字面量与八处调用点；按 E330 教训解析 `change_event()` 函数体逐项核用户文本不进载荷 + `.with(` 计数恰为 10。挂 `.github/workflows/ci.yml` `scan` job（083 收口轮复核在 132 行后）。

30 个守卫复扫：`world_editor_guard.py` OK，其余 28 个 OK；`delivery_guard.py` 在 83 号 spec 落盘后按 A249 要求 083 四件套，补齐后复扫 0 FAIL。CI 三 job 按 A116 实跑：credential 首次 `CREDENTIAL_FOUND`（RC=1，命中 `scripts/__pycache__/download_sources_guard.cpython-312.pyc`——Python 常量折叠把源码里分部件拼接的凭据前缀还原成连续串，A258 的构建产物侧延伸），清理 `scripts/__pycache__/` 后 `NO_CREDENTIAL`；wording `NO_EXPLANATORY`、hardcode `NO_HARDCODE`。`git grep -lE` 扫 tracked 0 命中、`.git/config` 0 命中；E342 如实计入「已失败」，不写成「未发生」。演示 `demos/round-082-world-editor.html` 的 JS `new Function()` 语法检查通过，NODES / LOG / STATE 三数组与 MINI1 / MINI2 / MINI3 均 16 项对齐（A265）；`docs/index.md` 必读清单逐文件核存在非空。

## 4. 双向注入

083 收口轮补跑（`world_editor_guard.py` 接 CI 前必须双向验证，A159 / A204）。28 组注入缺陷覆盖：七表逐值（A / B）、五 impl 段（C）、A247 复用（D / E）、坏输入标签（F）、`VERIFIED_LICENSE` 单值（G）、矛盾态函数体（H）、事件载荷用户文本（J / K / L）、禁用字面量（M）、统一信封（N）、未知键拒收（O / AD）、纯查询段（P）、单条突变（Q）、保护清单复用（R）、原子写（S）、枚举边界（T）、载荷计数断言（U）、AX03 状态（V）、boot 模块（X）、CI step（Y）、v1 面（Z）、ax_guard（AA）、显式 Vec 类型（AB）、矛盾态调用计数（AC）。**28 组全真 FAIL，0 假 OK**；每组恢复后 `WORLD_EDITOR_GUARD_OK`，六个被注入文件（`world_editor.rs` / `ax.rs` / `boot.rs` / `ci.yml` / `api.rs` / `ax_guard.py`）哈希复原。按 A243，行为测试无法区分的实现边界由守卫持有，未改测试凑失败、未降守卫断言。

## 5. 交付逐字核对

| 项 | 值 |
| --- | --- |
| `KNOWN_KEYS` / `ENTRY_KEYS` / `FIELDS` / `FORMATS` / `SOURCES` / `LINK_MODES` / `STATES` | 3 键 / 9 键 / 4 值 / 3 值 / 2 值 / 3 值 / 3 值，七张表用显式 `EXPECTED` 集合逐值比对（A270）；`VERIFIED_LICENSE = "MIT"` 单值另核；未知键整份拒、枚举未知值跳过 |
| 五枚举字面量一致性（A269） | 守卫解析 `impl EditField` / `impl ValueFormat` / `impl OssSource` / `impl LinkMode` / `impl EditorState` **五个** impl 段，各自 `=> "X"` 与 `"X" =>` 两组字面量与对应常量表逐值比对 |
| 既有文本上限复用（A247） | `use crate::core::robust;` 显式 import + `robust::MAX_TEXT_BYTES` ≥ 2 处使用 + `robust::read_or_default(&path, DEFAULT_STATE)`；删 import 行真 FAIL |
| 不透明字符串、零内容持有 | `prod` 段无 `cmp_precedence` / `semver` / `Version::parse` / `url` / `token` / `uuid` / `png` / `texture` / `minecraft:` / `give ` / `regex` / `glob` / `§` / `TcpListener` / `TcpStream` / `bind(` / `127.0.0.1` / `SystemTime` / `UNIX_EPOCH`（A30 / `00:26` / `11:18` / `11:19`）；条目 `id` 与 `license` 只校验长度与控制字符，种子值 / 存档内容 / NBT 数据 / 作者 / 项目地址全不进本层 |
| 矛盾态五条规则八处调用（E322 教训） | `entry_consistent()` 抽成单一函数，守卫解析函数体逐项核 `open_source`+空 license / `applied`+`!verified` / `applied`+`!diff_checked` / `separate_process`+`builtin` / 非空 license+`builtin` 五条字面量；`parse()` / `add_entry()` / `set_source()` / `set_state()` / `set_link_mode()` 八个调用点逐字核 |
| 八个派生纯查询 | `editable_count()` / `verified_count()` / `by_field()` / `by_source()` / `by_link_mode()` / `license_for()` / `applied_count()` / `summary()` 段内无 `fs::` |
| 单条突变 | 守卫核 `set_field` / `set_source` / `set_state` / `set_link_mode` / `set_verified` / `set_diff_checked` / `add_entry` / `remove_entry` 单条入口；`prod` 段无 `mark_all` / `confirm_all` 批量入口 |
| 布尔与档位双向边界 | 五枚举 `parse()`（load）与各自 `contains(&x.code())`（set）双向生效；`LinkMode` 三值覆盖 `11:26` / `11:9` 两条 OR 路径（A250） |
| 27 类坏输入 | 26 个 DEGRADE 标签 + 1 个 `no_root` ERROR；守卫按显式列表逐项核（根级 / 文件级 / 条目级 / 矛盾态 / 容量 / 无 root） |
| `write()` 段 | `fs::rename(&tmp, &path)` 原子写，仅自身状态文件 |
| `serialize()` | 只写 `schema` / `session` / `entries` 三键，条目只写 9 键 |
| `DEFAULT_STATE` 逐字不变 | 测试 `default_state_literal_is_unchanged` 断言整串与 3 键（A175） |
| `api::v1` | 7 符号不变，4 条 `pub use`，无 `world_editor` 引用 |
| AX03 `conflict` | 保持空，24 条 spec 唯一 |
| 既有 16 个 AX 数据层模块 / `feature_gate.rs` / `popup.rs` / `consent.rs` / `dispatcher` / `stats` / `region` / `client_ai` | 零 diff |
| 非测试段 `unwrap()` / `expect(` / `unwrap_or` / 批量删除 / 网络与时钟 | 0 |
| 凭据前缀连续串 | 0（守卫不写，凭据交给 CI credential job，A258） |
| 保护清单复用 | 测试段 `use crate::core::settings_io::PROTECTED_FILES;`，四文件逐项读回 `keep` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff，26 包 / 25 第三方 / 58 份 LICENSE 全文 / 309 行声明不变 |
| UX HTML / 两语言包 / 56 张 PNG | 零 diff |
| `LOADED_MODULES` | 新增 `core.world_editor`，诊断包模块列表不缺项 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| A271 预检 | 开工实跑全仓 `*_guard.py` 禁用字面量表并核扫描范围，测试名首版避开 `catalog()`、源码全英文避开 `i18n_guard`、prod 段不写端点与凭据连续串；首跑 `API_GUARD_OK` / `I18N_GUARD_OK`，074 E275 未重演 |
| `change_event()` 载荷（E330 教训） | 守卫解析函数体逐项核 `.with("id"/"license"/"title"/"body")` 不存在 + `.with(` 计数恰为 10；用户文本不进事件 |

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交付层补齐而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 已失败；EQ / Q / 6 项 `Planned` 未证实；真实 NBT 读取写回与 UI 渲染未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 7，满足 | — |
| 连续十三轮未达通过 | 069–081 连续未通过，按 `00:9.1` 应停下；用户 082「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-082-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 逐字保存、081 远端补验、四份原文全文回显、A244 逐条对照表、`00:230` 首次一手联网核实、A248 / A266 预检、A201 / A211 / A217 / A250 / A259 / A267 / A271 复核、`00:137` / `00:245` 显式核、AX03 数据层、`**668 / 0**（复跑 3 次：第 1 次 `667 passed; 1 failed; RC=101` 为既有并发用例偶发 FAILED，第 2 / 3 次 `668 / 0`；另按 A245 单独跑该用例 3 次全过、再复跑 3 次全量均 `668 / 0`）`、守卫、双向注入、v1 不变、零新增依赖、远端逐项一致 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341；035–047 历史格式缺失 |
| 未证实 | Q-082-01 / Q-082-02 / Q-082-03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、EQ-01 ~ EQ-13、4 条 Q-C、6 项 `Planned`、6 项低可信度转述 |
| 未启动 | 真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、存档编辑 UI 渲染、真实连接建立、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载、zip / 投影解析 |
| 受阻 | 无（远端 Git Data API 通道正常；6 项 `Planned` 属未启动，不计受阻）。本地 CI credential job 首次 RC=1 已定位并清理、复跑通过，登记 E342 计入「已失败」 |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

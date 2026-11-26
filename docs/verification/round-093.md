# 093 独立验证报告

| 项 | 值 |
| --- | --- |
| 结论 | **部分通过**，未发通过标记 |
| 依据 | `docs/spec/93-round-093-instructions.txt`（183 字节）；`docs/decisions/093-feature-locations.md`；`docs/records/round-093-full-readback.md`；`docs/records/round-093-feature-locations.txt`；`scripts/feature_locations.py`；`scripts/feature_locations_guard.py` |
| 口径 | 位置清单逐项与真实文件比对；测试作回归不作质量结论；候选调整只登记未执行；093 清单 / 守卫 / 四件套一次同步到远端 |

## 1. 原文复读与开轮状态

`docs/records/round-093-full-readback.md`：四份原文逐行校验复读（261 / 520 / 268 / 64 行，SHA-256 表、首末行与锚点行）、93 号 spec 逐字 183 字节、A145 远端补验、A202 / A208 / `00:248` 复核、A211 / A164 分列、A244 / `00:230` / `00:137` / `00:245` 显式核、A249 形态。按 A182 写明：本轮回显逐行校验结果与 93 号 spec 全文，四份正文未在对话重打全文（092 已全文回显）。

93 号 spec 逐字：`干，还有你需要向我提交现在所有功能写的位置的txt，估计这么多轮下来有些功能放的位置应该要改一下了（包括设置当中的具体设置项）`，183 字节，SHA-256 `cbc9d64c4e229f37`，与 92 号 3 字节 `干` 不同形态（A34 不重复落盘、不建 94 号）。按 A202 打开 `092-pending-decisions.md` 尾部核 092 唯一下一步为「等用户拍板 A 组」；按 `00:248` 用户当轮明确指令覆盖该预告，093 转位置清单交付轮，A 组 EQ / Q 仍全部未证实（E377）。

A145：`GET /git/ref/heads/main` RC=200 得 `5c9313e284d5ac8dd6b5947265f184d423bc88fc`（092 补记，parent `d65c0d1`），完整 recursive tree `LOCAL 1292 / REMOTE 1292 / DIFF 0 / EXTRA 0 / TRUNCATED False / ALL_MATCH True`；本地 HEAD `b0c6c7b`、DIRTY 0、无锁、无运行中 git 进程、PYC 0。`00:230` 本轮真执行：`TZ='CST-8' date` 得 `Thu Nov 26 13:30:12 CST 2026`；085–093 零新增上游依赖。

## 2. 位置清单逐项核对（A15 / A35）

`python3 scripts/feature_locations.py` 输出 `FEATURE_LOCATIONS_OK path=docs/records/round-093-feature-locations.txt bytes=41046 lines=521 sha256=1d506c26b380f498`。清单定稿时（093 文件已落地）脚本内 `sh()` 实跑：`src/core/*.rs` 48 / 22332 行、`src/*.rs` 2、`tests/*.rs` 6、`scripts/*_guard.py` 35（含本轮新增 1 个）、`demos/*.html` 80、`demos/preview/*.png` 56、`docs/decisions/*.md` 86、`docs/verification/*.md` 88、`docs/features/*.md` 72、`docs/design/*.md` 13、`docs/index.md` 必读清单 523 项、tracked 1300。开工 A145 时（093 文件未落地）为 79 / 85 / 87 / 515 / 1292，两口径并列不混用（E379）。

逐项覆盖核对：48 个模块文件名全部在 txt 第二节；24 项 AX 全部在第三节；`settings_io.rs` 的 6 个根键、`PROTECTED_FILES` 4 项实值（`boot-state.json` / `diagnostic-bundle.json` / `privacy-consent.json` / `play-stats.json`）、6 个上限常量在 4.1；18 个 `DEFAULT_STATE` 的键与原始 JSON、40 张 `*_KEYS` 白名单逐值在 4.2 / 4.3；11 个 `data-pane`、15 个 `id="set*"`、逐项 `data-i18n` 键与首个 option 默认值在 4.4；`core.*` 稳定 ID 全集在 4.5；两份语言包 `set.*` / `t.*` 键计数在 4.6；「界面语言」5 处位置链在 4.7。

E378 实证（偏差 1）：`docs/decisions/020-nav-slots-settings.md` D03 与 `docs/features/settings-groups.md` 记 9 分组、测量命令写 `grep -c 'data-pane='` 输出 9；实跑 `demos/ui-full-kcu-paper.html` 得 `data-tab` 11 / `data-pane` 11（general / download / cache / recommend / status / ai / plugins / crash / privacy / experimental / auto）。`scripts/settings_guard.py` 全文无 tab 数断言，故 092 轮 34 个既有守卫全绿。093 不重写历史文档、不改 HTML、不改语言包、不改守卫断言（A181 / A201 / `00:9.2`），只在清单登记 3 个候选与影响面。

5 条偏差（分组数不一致 / 设置项真值分散 6 处 / 48 模块同构堆积 / 索引按轮次 / 功能池 24 项与 48 模块非一一对应）每条含现状、候选 A/B/C、影响面、「状态：待拍板，未执行。」；txt 全文无「已迁移 / 已执行 / 已决断 / 已拍板 / 用户已选」。本轮采用候选 C（只交清单）与偏差 4 的候选 A（本 txt 即功能域索引），均不移动文件。

## 3. 测试、守卫与 CI

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib`（093 实跑） | **780 / 0**（RC=0，`src/` 零改动） |
| 集成段 1（093 实跑） | **26 / 0**（6 + 7 + 7 + 6，RC=0） |
| `cargo test --offline --doc`（093 实跑） | **0 / 0**（RC=0） |
| 全量 `cargo test --offline` | **819 / 0**（分段求和） |
| Windows GNU 交叉检查（085 实测） | **通过 / RC=0 / 29.02 s / 零 warning** |

全量 **819 / 0** 为分段求和（A252）：lib 780（093 实跑 `test result: ok. 780 passed; 0 failed`）、集成段 1 26（093 实跑四行 `test result: ok.`）、集成段 2 7 与段 3 6（085 原始输出 60.39 s / 147.88 s）、doc 0（093 实跑）、Win GNU RC=0（085 原始输出）。`tests/` 真实文件名按 A176 先 `ls tests/*.rs` 核实为 6 个。093 首跑 lib 即 `780 passed; 0 failed`，未触发 A245；E374 仍按 091 登记保留在四值「已失败」。既有断言一字未改、未加跳过标记、未删测试。

`scripts/feature_locations_guard.py` 挂 `.github/workflows/ci.yml` `scan` job。093 复扫 36 项（35 个 `scripts/*_guard.py` + `scripts/p09_scan.py`）。落 93 号 spec 后 `delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-093-full-readback.md`，补齐 093 四件套后 `DELIVERY_GUARD_OK rounds=[… 90, 91, 92, 93] g1_spec g2_readback g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step`（A249 / A268）。

双向注入 **16 组全真 FAIL、0 假 OK、0 跳过、恢复后守卫 OK、全文件 SHA-256 复原**（A159 / A204 / A243）：覆盖 txt 缺失 / 过短、模块名删除、AX 删除、6 根键逐个删除、pane 删除、15 个 `set*` 控件删除、5 条偏差标题删除、「待拍板，未执行。」计数、禁词「已执行」注入、候选 / 影响面 / 位置链段删除、复现锚点删除、`src/` 注入脏文件、CI step 删除、decision 默认回显删除、生成脚本复现锚点删除。守卫逐值解析而非全文子串（A241 / A270）：模块名来自 `src/core/*.rs` 实枚举、AX 来自 `ax.rs` 正则、根键来自 `settings_io.rs` 常量表、pane / 控件来自 HTML 实跑。A10：txt 缺失返回明确 FAIL 而非 traceback。A243：守卫 FAIL 但行为测试仍通过的约束（清单完整性、未执行口径、零 src diff）如实登记「由守卫持有」，不改测试凑失败、不降守卫断言。

`demos/round-093-feature-locations.html` 的 JS `new Function()` 语法检查通过，NODES / LOG / MINI1 / MINI2 / MINI3 均 16 项对齐（A265）；`docs/index.md` 必读清单逐文件核存在非空。CI 三 job 按 A116 实跑真实命令，输出见第 5 节补记。`scripts/__pycache__/` 0 项；守卫统一 `PYTHONDONTWRITEBYTECODE=1` 复跑。`panic_guard` / `i18n_guard` / `api_guard` 全仓扫描型守卫 0 FAIL（093 `src/` 零改动，A271 不触发）。

## 4. 交付逐字核对

| 项 | 值 |
| --- | --- |
| A249 四件套 | 085–093 的 spec、readback、decision、verification、demo 全部齐；`delivery_guard.py` G1–G8 全过 |
| 093 占位符 | 0 |
| `api::v1` | 7 符号 / 4 条 `pub use` 不变（A246） |
| `src/` / `Cargo.*` / `vendor/` | 零 diff；无新增模块、无新增测试标识符 |
| 功能池 | AX07 / AX22 保持 `Planned`，AX07 conflict 保持 `network_io_not_started`；`Planned 2` / `DataLayer 21` / `GateOnly 1` |
| 位置清单 | 521 行 / 41046 字节；48 模块 / 24 AX / 6 根键 / 11 pane / 15 控件 / 5 条偏差逐值覆盖 |
| 零新增第三方 | 26 包 / 25 第三方 / 58 份 LICENSE / 309 行声明不变 |
| 全仓凭据 | 见第 5 节补记；`scripts/__pycache__/` 0 项；临时生成脚本用后即删 |
| 演示 LOG 键数 | 16 = NODES 16（A265） |
| 093 决策 G3 | `## 2. 时间戳` / `## 9. 自我批判` / `## 10. 四值` 行首精确匹配（A268） |
| 提交与推送 | 主快照 hash、文件数、逐项 ALL_MATCH 写进 `docs/records/rounds.md` 093 补记（A206）；见第 5 节 |

## 5. 提交、远端核对与 CI 三 job 实跑

093 按 A254 提交前 `ps -eo pid,cmd` 核无运行中 git 进程、无 `.git/index.lock`；按 A11 逐项核 `git status --porcelain` 全部属 093 范围。按 A216 用 `scripts/api_push.py` 以 `base_tree` 增量 POST 只传变化条目，`force=false`，不强推、不重写历史；推送后只读 `GET /git/ref/heads/main` 得新 ref，并用完整 recursive tree 求差集，逐项 ALL_MATCH 结果写进 `rounds.md` 093 补记。两个 zip 按 A205 重打：主 zip 用 `git ls-files -z | zip -@`，`ui-previews.zip` 用 `demos/preview/*.png` 清单。具体 hash、CI 三 job 实跑输出与数值见补记，不在推送成功前写模板值（A206 / A116）。

## 6. 未通过项与补齐计划（`00:9.1`）

**结论：未通过**，不发通过标记，不附两个哈希。

| 未通过项 | 原因 | 下一轮补齐 |
| --- | --- | --- |
| 8.1 独立验证结论 | 部分通过 | 未证实与未启动项按台账逐轮闭环，不因交清单而转通过 |
| 四值无已失败 / 未证实 / 未启动 | E213–E379 已失败；EQ / Q / 5 条候选后果未证实；迁移执行与执行层未启动 | 不改测试、不改验收项、不降标准 |
| 自评 ≥ 7 | 7，满足 | — |
| 连续未达通过 | 069 起连续未通过，按 `00:9.1` 应停下；用户 093「干」按 `00:248` 覆盖，卡点在决策与回复回显（D-093-1） | 发通过标记需用户拍板 Q / EQ 并逐轮闭环 |

## 7. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 93 号 spec 逐字 183 字节、四份原文逐行校验复读、A145 远端补验、A202 / `00:248` 覆盖核、A211 / A164 分列、E378 偏差实证、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 093 四件套、A268 G2/G3、`00:137` / `00:245` 显式核、093 占位符 0、位置清单 521 行逐值覆盖、16 组双向注入全真 FAIL、lib 780 / 0 与分段 819 / 0、Win GNU RC=0、36 守卫 0 FAIL、CI 三 job 通过、零新增依赖、`src/` 零改动、v1 不变、093 提交与推送结果见补记 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 / E356 / E357 / E360 / E361 / E363 / E366 / E367 / E369 / E370 / E371 / E374 / E375 / E377 / E378 / E379；035–047 历史格式缺失 |
| 未证实 | E362、EQ-01 ~ EQ-13（13 条）、Q-C01 / Q-C02 / Q-C08 / Q-037-01、Q-091-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、Q-082-01 / 02 / 03、Q-090-01 / Q-090-02、2 项 `Planned`、5 条候选调整后果、6 项低可信度转述、逐版本归属、B05 源仓库与许可、`11:242` 时长路径 |
| 未启动 | 真实网络 IO、DoH、浏览器授权、UI 宿主与渲染、子进程隔离、32 位 / MSVC / Win7 运行时、文件位置迁移执行、真实图片像素调整与缩放、Studio 六动作、图片预览渲染、撤销重做栈执行层、真实 `.litematic` / `.schem` 解析、投影资源站安装、方块状态编辑、真实 mrpack / CurseForge zip 解压落盘、拖动到此处页面、实例模板克隆执行、可移植实例导出、真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载 |
| 受阻 | 无（远端 Git Data API 通道正常；2 项 `Planned` 属未启动，不计受阻） |

独立验证仍「部分通过」，存在已失败 / 未证实 / 未启动项，不发通过标记。

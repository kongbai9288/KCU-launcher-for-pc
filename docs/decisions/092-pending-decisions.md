# 第 092 轮：拍板闭环 / 摊平可拍环境

| 项 | 值 |
| --- | --- |
| 编号 | 092 |
| 状态 | `src/` 零改动、`Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff；`Planned 2` / `DataLayer 21` / `GateOnly 1` 不变；`api::v1` 7 符号不变；待拍板清单已摊平，未代拍 |
| 依据 | `docs/spec/92-round-092-instructions.txt`（逐字 3 字节 `干`）；`00:34` / `00:133` / `00:137` / `00:164` / `00:203` / `00:207` / `00:230` / `00:245` / `00:248` / `00:9.1` / `00:9.2` / `00:14`；`docs/decisions/091-studio-image.md`；`docs/records/pending-question-environments.md`；`docs/records/b-class-status-recheck.md`；`docs/records/c-class-default-recheck.md`；A15 / A18 / A73 / A116 / A140 / A145 / A150 / A158 / A159 / A164 / A177 / A181 / A201 / A202 / A203 / A204 / A206 / A208 / A210 / A211 / A216 / A230 / A241 / A243 / A244 / A246 / A248 / A249 / A250 / A252 / A254 / A258 / A265 / A266 / A267 / A268 / A270 / A271 |
| 前序 | 091 远端 `1ec52d5` / `1286 / 1286 ALL_MATCH True`、HEAD `bc35c7b`、DIRTY 0；091 唯一下一步写「092 改走拍板闭环」 |
| 本轮性质 | 拍板闭环轮：摊平可拍环境，不落功能实现（A208） |

## 2. 时间戳

开工 `Thu Nov 26 00:13:08 CST 2026`。

## 3. 本轮目标与范围

用户 092 逐字 3 字节 `干`，按 `00:133` 落盘 `docs/spec/92-round-092-instructions.txt`。按 A248 / A266 开轮核 22 份 spec 逐字副本；平台拼入用户位次的文本不作用户当轮指令、不进 `00:133` 逐字副本；工具从未禁用。

真读 `00-requirements.txt` 261 行 / 16422 字节全文、`ai-errors.md` 520 行 / 55513 字节全文（1–496 行回显、490–520 行补读）、`11-features-input.txt` 268 行 / 17096 字节与 `12-server-features-input.txt` 64 行 / 4970 字节全文。A211 / A164 复核：不是只核哈希与台账状态，真读全文后逐条分「已决断 / 未决断」。`00:24` 框架方式、`00:8` ≤2GB 默认轻量、`11:7` 境外限制、`11:10` 弹窗关闭、`11:18` API 不共有、`12:63` png logo 自动调整像素、`12:12` 关机点击均为原文已决断；EQ-01 待拍的是具体框架与 Win7 降级路线，不是「要不要框架」。实现状态按 9.3 分层，不与「原文已决断」合并表述。

按 A202 打开 `091-studio-image.md:112` 与 `ax-feature-pool.md` 091 补记核尾部，确认 091 唯一下一步为「092 改走拍板闭环……把 Q-091-01 / 02 / 03、历史 Q 与 EQ-01 ~ EQ-13、4 条 Q-C 摊平给用户拍板；按 A208 不擅自开工硬做，也不擅自定 2 项之间的优先级」。按 A208 复核 `b-class-status-recheck.md:85`：EQ-01 ~ EQ-13 与 4 项待拍板仍「未证实（待拍板）」，B04 卡 EQ-01、B07 卡 EQ-05、B09 卡 EQ-11，本轮不碰 UI 渲染层（A100）。结论：上一轮结尾列出的层确实需要用户拍板，092 按「摊平可拍环境」执行。

按 A230 / A267 读 `src/core/ax.rs:20–43` 真实表并逐条核 2 项 `Planned`：AX07 `doh_support` / `network_io_not_started`（`31-axolotl-launcher-features.md:35` 写真实网络 IO 未启动、Win7 TLS 前置 EQ-03，00 / 11 / 12 号全文无 DoH 锚点）→ 技术受阻非需求冲突，排除留痕、conflict 不清；AX22 `shimu_account`（浏览器授权依赖真实网络 IO + 第三方端点 + `11:7` / 054 境外限制 + `11:18` API 不共有）→ 排除留痕。两项保持 `Planned`，本轮不擅自定优先级。

A244 复核：26 包 / 25 第三方 vendor / 58 份 LICENSE 全文 / `THIRD-PARTY-NOTICES.md` 309 行 / `code-ownership-audit.md` 逐轮登记，085–092 零新增第三方。`00:230` 本轮真执行：`TZ='CST-8' date` 得 `Thu Nov 26 00:13:08 CST 2026`；只读 `GET /git/ref/heads/main` RC=200 得 `1ec52d5…`；082 的 `ViaVersion/ViaNBT` 上游状态不变。按 A145 补验：远端 `1ec52d5ad0adc00a1daa1e6f0d345af8874b3a0e`（091 补记，parent `24d27e1`），完整 recursive tree `1286 / 1286 / DIFF 0 / ALL_MATCH True`；本地 HEAD `bc35c7b`、DIRTY 0、无锁、无运行中 git 进程、PYC 0。

A249 形态实测：92 号 spec 落盘后 `python3 scripts/delivery_guard.py` 首跑 `DELIVERY_GUARD_FAIL reason=missing docs/records/round-092-full-readback.md`，补齐 readback 后为 `DELIVERY_GUARD_FAIL reason=G3 decision_missing 92`。不删 spec 规避守卫、不改守卫断言，补齐 092 四件套后复跑 OK，FAIL 原样留痕。`00:9.1` 069 起连续未达通过按 `00:248` 用户当轮「干」覆盖，不中断但卡点逐条回显（D-092-1）。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D-092-1 | 092 定为拍板闭环轮 | `src/` 零改动、`Cargo.*` 零 diff、不落功能实现；连续未达通过按 `00:248` 覆盖，卡点逐条回显 |
| D-092-2 | 摊平清单只列环境 / 选项 / 后果 / 耦合 | 状态一律「待拍板 / 未证实」，不代拍、不写「已拍板 / 用户已选」（A73 / A150 / A164） |
| D-092-3 | Q-C 口径修正为 3 条 Q-C + Q-037-01 共 4 项 | A202 打开 `pending-question-environments.md` / `c-class-default-recheck.md` / `b-class-status-recheck.md:85` 核出 091「4 条 Q-C」为笔误，登记 E375，历史行不重写（A181 / A201） |
| D-092-4 | EQ 口径为 EQ-01 ~ EQ-13 共 13 条待拍 | EQ-14（049 关闭）/ EQ-15（050 关闭）不计入；逐条环境 / 事实 / 选项 / 后果沿用 048–057 段，不重复铺场景（A150） |
| D-092-5 | 功能池状态不变 | AX07 `Planned` + `network_io_not_started`、AX22 `Planned` + 空 conflict；`Planned 2` / `DataLayer 21` / `GateOnly 1`；AX07 conflict 不清（A230） |
| D-092-6 | 新增 `scripts/pending_decisions_guard.py` 挂 CI `scan` | 核清单 13 条 EQ 逐行、Q-091 三条、4 项 Q-C、2 项 AX 锚点、A164 分列、A73 四要素表头、不代拍、`api::v1` 稳定面；双向注入按实记数（A159 / A204 / A270） |
| D-092-7 | 四件套 + 台账补记 + 两个 zip 一次提交 | A11 逐项核 diff 范围；A205 按 tracked 清单打包；A254 提交前核锁与运行中 git 进程 |
| D-092-8 | 增量推送，`force=false` | A216 / A206；推后逐项 ALL_MATCH 才写进 `rounds.md` 092 补记，不用模板值 |
| D-092-9 | 按 `00:245` 不发通过标记 | 存在已失败 / 未证实 / 未启动；唯一下一步为等用户拍板，按 A208 不擅自开工硬做 |

## 5. 接口终点核对（`00:137`）— A244 要求显式核

| 引用点 | 092 形态 |
| --- | --- |
| `src/` | 零改动；无新增模块、无新增测试标识符（A271 本轮不触发） |
| `src/core/ax.rs` / `src/api.rs` | 零改动；AX07 / AX22 状态与 conflict 原样；v1 7 符号 / 4 条 `pub use` 不变（A246） |
| `docs/records/pending-question-environments.md` | 追加「## 092 摊平」段：A 组 3 行阻塞项、B 组 4 项 Q-C、C 组 EQ-01 ~ EQ-13 逐行索引、D 组 31 条历史 Q、已决断 / 未决断分列、D-092 逐值 |
| `scripts/pending_decisions_guard.py` / `.github/workflows/ci.yml` | 新守卫挂 `scan` job，第 34 个 `*_guard.py` |
| `Cargo.toml` / `Cargo.lock` / `vendor/` / `docs/licenses/` / `THIRD-PARTY-NOTICES.md` | 零 diff |
| UX HTML / 两语言包 / 56 PNG | 零 diff；A100 渲染层闸门未触发 |
| 092 新增 | 92 号 spec、readback / decision / verification / demo、`rounds.md` 等台账与 `docs/index.md` 补记 |

## 6. 清单落点

`pending-question-environments.md` 的 092 段按「拍板面最小」分组：A 组列出阻塞 2 项 `Planned` 的三行（EQ-03 + AX07、EQ-01 + Q-091-01 + AX22、Q-091-02 + Q-091-03），每行给具体环境、选项、后果、耦合（A73 / A150）；B 组 4 项 Q-C；C 组 13 条 EQ 逐编号索引，指向既有 048–057 段；D 组从 `091-studio-image.md` 四值「未证实」行真实提取的 31 条历史 Q，按轮次分组，定义锚点指向各轮决策；E 组已决断 / 未决断分列。`open-questions.md` 93 条（`grep -cE '^\| Q-[A-H][0-9]'` 实跑 93）状态列以该文件为准，不把词频当条数（A35）。Q-A ~ Q-H 组 013 已答复、Q-031-01 033 已关闭，不重开。

## 7. 交付快照

本轮一次提交把 092 清单 / 守卫 / CI / 四件套 / 台账补记纳入主快照；推送后只读核远端 ref 与完整 tree，逐项 ALL_MATCH 结果写入 `docs/records/rounds.md` 092 补记（A206，不用模板值）。开工 A145 补验为 `1ec52d5` / `1286 / 1286 / ALL_MATCH True`。两个 zip 按 A205 重打。全仓零凭据；`scripts/__pycache__/` 保持 0 项；临时生成脚本用后即删。

## 8. 验证

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib`（092 实跑） | 780 / 0（RC=0 / 0.34 s；`src/` 零改动，与 091 同） |
| 集成段 1（092 实跑） | 26 / 0（6 + 7 + 7 + 6，RC=0） |
| `cargo test --offline --doc`（092 实跑） | 0 / 0（RC=0） |
| 全量（分段求和，A252） | **819 / 0**（lib 780 + 集成段 1 26 + 真加载两段 13 + doc 0；真加载两段与 Win GNU 取 085 / 088 原始输出，`src/` 零改动未重跑） |
| Windows GNU 交叉检查（085 实测） | RC=0 / 29.02 s / 零 warning |
| 守卫 | 35 个（34 个 `*_guard.py` + `p09_scan.py`），补齐 092 四件套后 0 FAIL |
| 双向注入 | 实跑输出见 `docs/verification/round-092.md` 第 3 节，按实记数（A192 不凑数） |
| CI 三 job | 按 A116 实跑真实命令 |
| 独立验证 | 部分通过，未发通过标记 |

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E375 | 091 结尾写「4 条 Q-C」，按 A202 打开 `pending-question-environments.md` 尾部、`c-class-default-recheck.md`、`b-class-status-recheck.md:85`、`055-c-class-recheck.md:63` 逐字核：真实待拍为 Q-C01 / Q-C02 / Q-C08 三条 Q-C 加一条 Q-037-01（插件哈希口径，关联 EQ-02），共 4 项；Q-037-01 不属 Q-C 组。属 A202 批评的「把台账笔误当待办再念一遍」 | 092 清单按「3 条 Q-C + Q-037-01 共 4 项」写，守卫逐值核四项；历史行不重写（A181 / A201），本补记覆盖。笔误计入四值「已失败」，处置计入「已证实」 |
| E376 | `00:9.1` 069 起连续未达通过，规则要求停下由用户决定是否调整范围 | D-092-1：按 `00:248` 用户当轮「干」覆盖，不中断但卡点（已失败 / 未证实 / 未启动 / 拍板未闭环）在决策、验证、回复逐条回显；不改验收项凑通过（`00:245`） |
| E362 | `scripts/ax_guard.py` 显式断言表删去 `'AX08'` 后仍 `AX_GUARD_OK`（088 登记的历史守卫缺口） | 092 不扩大 diff 修历史守卫；AX15 与 AX08 状态另由 `studio_image_guard.py` / `instance_import_guard.py` 独立核，双守卫互补；保持未证实 |
| E284 | `00:175` 复用同一模块与连续多轮新建数据层模块的张力 | 092 零新增模块、不新建重复框架；张力继续缓解但整体未完全消除，仍登记 |

预防项（未发生，不计已失败）：A140 / A254 提交前核锁与运行中 git 进程；A268 G2 四份原文与 G3 `## 2` / `## 9` / `## 10` 锚点一次排对；A265 演示五数组对齐；A252 分段口径；A206 远端未推成不写模板值；A258 凭据字面量分部件拼接；A267 改功能池状态前读真实 slug（本轮不改状态）；A271 新测试标识符核全仓禁用表（本轮 `src/` 零改动，不触发）；A205 zip 按 tracked 清单打包。A241 / A270 落地缺口预防：新守卫不靠全文子串，用 C 组 EQ 表逐行解析 + A 组四要素表头精确行 + 闭合句精确串；注入按全局替换真 FAIL。A243：守卫 FAIL 但行为测试仍通过的约束（清单完整性、不代拍、AX 状态）如实登记「由守卫持有」，不改测试凑失败、不降守卫断言。

自评 7（7 → 7 → 7）。扣分：2 项仍 `Planned`；EQ-01 ~ EQ-13 与 4 项 Q-C 未拍；31 条历史 Q 未拍；真实网络 IO / UI 宿主 / 子进程隔离 / 渲染层未启动；E362 历史守卫缺口未修；6 项低可信度转述未交叉印证；`00:9.1` 卡点与拍板闭环未闭环。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | 92 号 spec 逐字 3 字节、四份原文全文回显（261 / 520 / 268 / 64 行）、A145 远端补验（1ec52d5 / 1286 ALL_MATCH True）、A230 两项冲突逐条核验、A211 / A164 已决断与未决断分列、A202 核出 E375 口径偏差并补记覆盖、A244 合规复核、`00:230` 联网核实、A248 / A266 预检、A249 092 四件套形态、A268 G2/G3、`00:137` / `00:245` 显式核、092 占位符 0、lib 780 / 0、集成段 1 26 / 0、doc 0 / 0、35 守卫 0 FAIL、双向注入实跑、CI 三 job 通过、零新增依赖、`src/` 零改动、v1 7 符号不变、092 提交与推送结果见补记 |
| 已失败 | E213 / E214 / E233 / E244 / E252 / E275 / E285 / E302 / E314 / E321 / E322 / E330 / E331 / E340 / E341 / E342 / E346 / E349 / E350 / E351 / E352 / E353 / E356 / E357 / E360 / E361 / E363 / E366 / E367 / E369 / E370 / E371 / E374 / E375；035–047 历史格式缺失（不补写） |
| 未证实 | E362、EQ-01 ~ EQ-13（13 条）、Q-C01 / Q-C02 / Q-C08 / Q-037-01、Q-091-01 / 02 / 03、Q-067-01 ~ Q-067-03、Q-070-01、Q-071-01 / Q-071-02、Q-072-01 / Q-072-02、Q-073-01 / Q-073-02、Q-074-01 / Q-074-02、Q-075-01 / Q-075-02、Q-076-01 / Q-076-02、Q-077-01 / Q-077-02、Q-078-01 / Q-078-02、Q-079-01 / Q-079-02、Q-080-01 / Q-080-02、Q-081-01 / Q-081-02、Q-082-01 / 02 / 03、Q-090-01 / Q-090-02、2 项 `Planned`、6 项低可信度转述、逐版本归属、B05 源仓库与许可、`11:242` 时长路径 |
| 未启动 | 真实网络 IO、DoH、浏览器授权、UI 宿主与渲染、子进程隔离、32 位 / MSVC / Win7 运行时、真实图片像素调整与缩放、Studio 六动作、图片预览渲染、撤销重做栈执行层、真实 `.litematic` / `.schem` 解析、投影资源站安装、方块状态编辑、真实 mrpack / CurseForge zip 解压落盘、拖动到此处页面、实例模板克隆执行、可移植实例导出、真实 NBT 读取写回、vianbt 库引入、源码与产物真实字节比对、插件加载执行、二维码生成、地形探索、全屏地图、纹理导出、3D 旋转预览、皮肤下载 |
| 受阻 | 无（远端 Git Data API 通道正常；2 项 `Planned` 属未启动，不计受阻） |

按 `00:245`，存在已失败 / 未证实 / 未启动，**不发通过标记**（`00:9.1`）。

## 11. 本轮文档更新

92 号 spec、`round-092-full-readback.md` / `092-pending-decisions.md` / `round-092.md` / `demos/round-092-pending-decisions.html`；`pending-question-environments.md` 092 段；`rounds.md` / `ax-feature-pool.md` / `code-ownership-audit.md` / `requirement-compliance-audit.md` / `interface-log.md` / `docs/index.md` 补记；`scripts/pending_decisions_guard.py` 与 `.github/workflows/ci.yml` 新 step。`Cargo.toml` / `Cargo.lock` / `vendor/` / `src/` / UX / 语言包 / PNG / 防错清单零改动。

## 12. 唯一下一步

等用户拍板 A 组最小拍板面：EQ-03 + AX07 `doh_support`（选 ① 先起真实网络执行层 / ② 保持 `Planned` 降级为端点配置项 / ③ 明确不做）与 EQ-01 + Q-091-01 + AX22 `shimu_account`（选 ① 给端点与授权形态 / ② 只落本地断开关联 / ③ 保持 `Planned`）；其余 11 条 EQ、3 条 Q-C + Q-037-01、Q-091-02 / 03 与 31 条历史 Q 在 `pending-question-environments.md` 092 段可逐项拍。按 A208 不擅自开工硬做，也不擅自定 2 项 `Planned` 之间的优先级。

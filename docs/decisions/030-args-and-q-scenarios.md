# 第 030 轮：参数解析换 lexopt，Q-028 两条问题铺场景

| 项 | 值 |
| --- | --- |
| 编号 | 030 |
| 状态 | 代码已实现、已验证；两条待拍板问题仍待答复 |
| 依据 | docs/spec/30-round-030-instructions.txt |
| 前序 | 029-cache-lru.md、docs/features/server-auto-command-log-trigger.md 待拍板段 |
| 本轮性质 | 双轨轮 |

## 两条指令的边界

| 编号 | 原文片段 | 处置 |
| --- | --- | --- |
| B01 | 「干」 | 继续按 `docs/records/code-ownership-audit.md` 映射表替换自写代码，落 `src/core/args.rs`。 |
| B02 | 「两个q交代下场景不然不好判断」 | 把 Q-028-01 / Q-028-02 铺成可判断的画面，写 `docs/records/q028-decision-scenarios.md`；不替用户拍板、不改功能 md 的结论。 |

## B01：参数解析换成 lexopt 0.3.2

| 编号 | 动作 |
| --- | --- |
| C01 | 查 `blyxxyz/lexopt` tag 列表（v0.3.2 / v0.3.1 / …），取 v0.3.2 manifest：零依赖、单文件 `src/lib.rs`、MIT、edition 2018、无 proc-macro、无 build.rs。 |
| C02 | 从 codeload tarball 精准提取 `src/lib.rs` + `Cargo.toml` + `LICENSE`（29 215 字节 tarball / 1055 字节 LICENSE）；裁掉 manifest 的 `[profile.test]` 段，上游 `src/` 一行未改。 |
| C03 | `Cargo.toml` 加 `lexopt = "0.3.2"`；`Cargo.lock` 9 → **10 包 / 9 第三方**；`vendor/` 加 1 个目录。 |
| C04 | `src/core/args.rs` 删掉手写 `peekable()` + `match tok.as_str()` + `it.next()` 取值 + 手写错误串；改用 `lexopt::Parser::from_args` / `Arg::{Long, Value}` / `parser.value()` / `Arg::unexpected()`。 |
| C05 | 保留项目特有的语义层：`--join-server` 别名、6 个字段、`extras`、`joins_server()`、`headless()`、统一 `Result<String, String>` 错误面。这层约 66 行是业务编排，不是参数解析器。 |

### 删掉的自写解析逻辑

| 025–029 | 030 |
| --- | --- |
| `xs.into_iter().map(Into::into).peekable()` 手工游标 | `Parser::from_args` |
| `match tok.as_str()` 字符串前缀比对 | `Arg::Long(&str)` 枚举匹配 |
| `it.next().ok_or_else(...)` 取值 | `parser.value()`（含 `MissingValue` 错误类型） |
| `other.starts_with('-')` 判未知 flag | `Arg::unexpected()` |
| 手写 `"--server requires a value"` 等 6 条错误串 | 库的 `Error` 转 String |

### 行为差异（如实登记）

| 编号 | 项 | 029 | 030 |
| --- | --- | --- | --- |
| B10 | `--instance=alpha` | 报 `unknown flag` | **接受**（lexopt 的 `--opt=value`） |
| B11 | `--` 之后全部 token | 按 `-` 开头仍报错 | **全部作为 positional** 进 `extras` |
| B12 | `-q` 短选项 / `-abc` 组合 | 报 `unknown flag` | 交给 `Arg::Short`，当前未注册故仍报错，但错误串来自库 |
| B13 | 非 Unicode 值 | `String` 天然不会 | 显式 `OsString::into_string()` 报「value is not valid unicode」 |
| B14 | 未知 flag 错误串 | `unknown flag: --nope` | `unexpected option '--nope'` |

B10 / B11 是能力升级（更符合命令行惯例），B12 / B14 是错误文案口径变化，未发现调用方依赖精确文案。原 5 个测试断言（单参数进服、别名、缺值拒绝、未知 flag 拒绝、kculf/kculh 分离）全部保留未改。

### 新增测试

| 编号 | 断言 |
| --- | --- |
| N01 | `--instance=alpha` 等值语法被接受。 |
| N02 | `--` 之后的 `--server literal` 只进 `extras`，不触发进服。 |
| N03 | positional 与选项混排时 `extras` 保持顺序。 |

`cargo test --offline` **141 → 144 / 0**。

## B02：两条 Q 的场景交代

写 `docs/records/q028-decision-scenarios.md`，不替用户拍板。要点：

| 编号 | 内容 |
| --- | --- |
| S01 | 说明两条问题的来历：013 的 Q-D02「每次请求」是 **AI 接口**授权，F028-03 是**日志驱动自动化**，不是同一类请求。 |
| S02 | 点出共同背景：日志里 `issued server command: /op Notch` 是**玩家输入的文字**，不是服务器真的执行过命令，触发源天然「输入不可信」。 |
| S03 | Q-028-01 铺 4 个画面：凌晨无人值守的卡顿预警、玩家聊天文字诱导、模组刷屏、规则「测试」按钮预览；给 Q1-A / Q1-B / Q1-C 三个口径及各自后果。 |
| S04 | Q-028-02 把动作分 C1–C5 五类（只读 / 游戏内广播 / 服务器命令 / 启动器侧动作 / 外部动作），点名 `/save-all` 撞崩服、`/op` 撞诱导、`/stop` 撞刷屏、C5 撞脱敏四个风险画面；给 Q2-A / Q2-B / Q2-C / Q2-D 四个口径。 |
| S05 | 写出耦合矩阵：越不弹确认，动作白名单越得收紧；建议一次拍 `Q1-B + Q2-C` 或 `Q1-A + Q2-B`。 |
| S06 | 相邻三项 N01–N03（来源限定默认值、冷却秒数、外传脱敏）按既有「你看着办」自行定默认，不占用户这次答复。 |

**倾向只写在场景文档里，没写进功能 md**：Q1-B（按动作分级）、Q2-B 打底 + Q2-C 可见面。功能 md 的「待拍板」段改为指向场景文档，结论栏仍为空。

## 四值

| 项 | 值 |
| --- | --- |
| 10 包 / 9 第三方、144 / 0、原 5 断言未改 | 已证实 |
| 手写参数解析器删除、lexopt 上游源码未改、MIT 全文落盘 | 已证实 |
| 两个 Q 的 4 + 4 个场景、耦合矩阵、建议组合 | 已证实 |
| Q-028-01 / Q-028-02 的用户答复与最终口径 | 未证实（待答复） |
| 真实 GUI 端到端、Win7 / 多架构、CI 独立构建 | 受阻 |
| 后端仓写请求 | 0（已证实） |

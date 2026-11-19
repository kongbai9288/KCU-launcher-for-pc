# 第 031 轮：两条 Q 按最严格拍板，配置与信封换 serde_json

| 项 | 值 |
| --- | --- |
| 编号 | 031 |
| 状态 | A 轨已拍板、B 轨代码已实现已验证 |
| 依据 | docs/spec/31-round-031-instructions.txt |
| 前序 | 030-args-and-q-scenarios.md、q028-decision-scenarios.md |
| 本轮性质 | 双轨轮 |

## 两条指令的边界

| 编号 | 原文片段 | 处置 |
| --- | --- | --- |
| A01 | 「两个问题A：按最严格去执行」 | 两条 Q 拍板，按最严格口径写回功能 md，落规则文档与界面演示。 |
| B01 | 「干」 | 继续按 `docs/records/code-ownership-audit.md` 映射表替换自写代码，落 `core/config.rs` 与 `core/envelope.rs`。 |

## A01：Q-028-01 / Q-028-02 按最严格

| 编号 | 结论 | 口径 |
| --- | --- | --- |
| Q-028-01 | 每次命中都手动同意 | **Q1-C**，完全复用 013「每次请求」 |
| Q-028-02 | 只允许 C1 只读动作 | **Q2-A**，C2–C5 一律拒绝并显示可见提示 |

判定说明：用户原话含「A」字样，与 Q1 的选项字母冲突；Q1-A 是「规则级一次性授权」，不是最严格。以明确的「按最严格去执行」为准，不按字母取 Q1-A。登记 Q-031-01 待用户确认该歧义。

落地约束 P01–P07 见 `docs/rules/auto-command-policy.md`。P05 是不改变口径的实现约束：同一规则已有待确认弹窗时后续命中只累计计数、不新增弹窗，确认只作用于当前这一次，累计次数可见；既没有任何一次未经确认就执行，也不打爆界面。

后果 R01–R04 如实写进功能 md：无人值守自动化失效；F028-03 在 Q2-A 下不会真的向服务器发命令，实际是「日志关键词提醒器 + 每次确认」。若用户本意是要能自动执行游戏内动作，需改 Q2 口径。

相邻三项按既有「你看着办」授权定最严格方向默认：来源限定「仅服务端输出」、冷却 30 秒、C5 全禁故外传脱敏不再需要二次确认。

界面闸门触发：新增设置内「自动命令」分组与命中确认弹窗，出整页 UX 演示与 2 张新预览图；不进一级导航，不写工程标识。

## B01：配置与信封换成 serde_json

| 编号 | 动作 |
| --- | --- |
| C01 | `core/config.rs` 删掉自写 `BTreeMap<String,String>` endpoints / ports 双表与手写 getter；换成 `serde_json::Map<String, Value>` 单根对象。 |
| C02 | 新增 `from_json_str` / `to_json_string`，配置文件的解析与序列化交给已在构建中的 `serde_json 1.0.145`，不新增依赖。 |
| C03 | `core/envelope.rs` 的 `payload: BTreeMap<String,String>` 换成 `serde_json::Map<String, Value>`，新增 `to_json_string` / `from_json_str`；`field()` / `with()` 语义不变。 |
| C04 | `Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 10 包 / 9 第三方；做的是把自写数据容器换成已有库的数据结构，不是新增库。 |

### 删掉的自写代码

| 030 | 031 |
| --- | --- |
| `Config { endpoints: BTreeMap, ports: BTreeMap }` 双表 | `data: Map<String, Value>` 单根对象 |
| 手写 6 个 getter / setter 直接操作两张表 | 经 `Map::get` / `insert` + `Value::as_str` / `as_u64` |
| 无文件编解码（配置只存在内存） | `from_json_str` / `to_json_string` |
| `Envelope.payload: BTreeMap<String,String>` 无序列化 | `Map<String, Value>` + `to_json_string` / `from_json_str` |
| 手写 `format!("kcu-{:08x}", n)` 序列 | 保留（`SEQ` 是项目特有的 ID 生成，不是序列化器） |

### 行为差异（如实登记）

| 编号 | 项 | 030 | 031 |
| --- | --- | --- | --- |
| B10 | 配置读盘 | 不存在 | 新增；非法 JSON / 非对象根 / 缺 sections 都给可见错误或默认值 |
| B11 | 端口范围 | `u16` 天然 | `as_u64` 后 `u16::try_from`，越界返回 None 而不是 panic |
| B12 | envelope JSON | 不存在 | 新增；`kind` 写成 `Request` / `Response` / `Event` 字符串 |
| B13 | payload 键顺序 | BTreeMap 有序 | `serde_json::Map` 无 `preserve_order` 时同样是 BTreeMap，有序性保持，原测试不降 |

### 新增测试

| 编号 | 断言 |
| --- | --- |
| N01 | 配置 JSON 往返保留语言、镜像测速开关、端点、端口、地域覆盖。 |
| N02 | 非法 JSON 与数组根被拒绝。 |
| N03 | 缺 `endpoints` / `ports` 的 JSON 自动补空对象。 |
| N04 | envelope JSON 输出可被 `from_json_str` 解析且保留 target / 自定义字段 / kind。 |
| N05 | envelope 带 error 时 JSON 里保留 error。 |

`cargo test --offline` **144 → 149 / 0**，原 8 个相关断言未改。

## 四值

| 项 | 值 |
| --- | --- |
| 两条 Q 按最严格拍板、P01–P07、R01–R04 | 已证实 |
| 149 / 0、10 包 9 第三方、上游库源码未改 | 已证实 |
| 整页 UX 演示 + 2 张预览图 | 已证实 |
| Q-031-01 字母歧义、F028-03 是否要真发命令 | 未证实（待用户确认） |
| 自动命令实现层、真实 GUI 端到端、Win7 / 多架构 | 受阻 / 未启动 |
| 后端仓写请求 | 0（已证实） |

## 055 补记：Q-031-01 已由 033 结案

031 第 25 行「登记 Q-031-01 待用户确认该歧义」与第 82 行「Q-031-01 字母歧义、F028-03 是否要真发命令 | 未证实（待用户确认）」是 031 当时的历史行，按 048 B01 口径**不重写**。

033（`docs/decisions/033-answer-abbr-and-anyhow.md` A01）已结案：**A 是 answer 缩写，不是 Q1-A 选项字母**；031 按「最严格」取 Q1-C + Q2-A 的判定成立，P01–P07 不改，032 三档不改，不重做界面。048 核对表 C05 写「结论未随之重审」属台账笔误；054 结尾沿用该错述，055 已撤回（`docs/records/rounds.md`「054 结尾错述撤回」）。

口径状态：Q1-C / Q2-A / P01–P07 全部有效；Q-031-01 **已关闭**。由 `scripts/policy_guard.py` G1/G2 守护。

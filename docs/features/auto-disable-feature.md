# 自动关闭某一功能

| 字段 | 值 |
| --- | --- |
| 编号 | F053-01 / B06 第二项 / D07 |
| 状态 | 判定层已落地（`src/core/feature_gate.rs`）；平台取数与公钥分发未启动 |
| 原文 | `docs/spec/11-features-input.txt` 第 5 行、第 12 行 |
| 触发 | 启动前由调度器注入策略字节、公钥、签名、设备能力、当前版本、日期 |
| 输出 | `GateOutcome { source, code, features, notices, diagnostics, envelope, cancelled, policy_version }` |

## 两个来源

1. **设备能力**：`DeviceCaps.context` 是宿主注入的布尔上下文键，`requires` 列表全为真才启用；本模块不做系统检测。
2. **平台策略**：签名快照本地判定；`schema=1`、`policy_version`、`entries[]`，每条含 `id` / `owner` / `expires` / `reason_key` / `requires` / `min_app` / `max_app` / `default`。

原文第 12 行要求送的 json「必须内置」：`BUILTIN_POLICY` 编译进模块，空条目。控制平面断开、签名不符、策略被删、畸形、超限时一律回退到它，且**不执行任何关闭**。

## 顺序

1. 取消 → 空结果、0 副作用
2. 限流 → 不关功能、给明确 code
3. 策略缺失 / 空 / 超 256 KiB → 内置默认
4. 验签（036）→ 失败回退内置默认，**不解析内容**
5. `serde_json` 严格字段白名单 → 畸形 / 禁用键 / 超 512 条 → 内置默认
6. 逐条独立判定：`requires` 全真 + `min_app`/`max_app` 用 `cmp_precedence` + `expires` 未过期
7. 不满足 → `enabled=false` + 一条可关声明

## 安全默认（fail-open，文档化）

| 情况 | 结果 |
| --- | --- |
| 验签失败 / 畸形 / 超限 / 控制平面断开 | 内置默认，不关任何功能 |
| 未知 `id` | 忽略，不关 |
| `core.locked.settings` / `core.locked.about` | 永不关闭（020 锁定） |
| 条目判定输入异常（版本解析失败等） | `enabled=true` |
| 过期条目 | 忽略，不生效 |
| 限流 / 取消 | 不关功能 |

字段白名单拒绝 `url` / `endpoint` / `token` / `key` / `secret` / `api` / `password` / `credential` / `depends_on`：功能开关里不放 API 地址、不放凭据、不放嵌套依赖。

## 声明与刷新

每处关闭生成一条 `Notice`：语义 `reason_key`、`closable=true`、三动作 `gate.act.default` / `gate.act.refresh` / `gate.act.cancel`（与 051 声明页三项对齐），并写一条单行 `[KCU]` 诊断。判定缓存容量 128 / TTL 30 s，`refresh()` 全清后重跑签名与全部判定；**签名与结论不缓存**。

## 离线口径（与完整性验证分开）

| 项 | 离线时 |
| --- | --- |
| 软件完整性验证（052） | 失败仍分级、仍记诊断、仍不给通过，但**不弹声明页**（原文「离线则不声明」） |
| 自动关闭功能（本项） | 本地判定，仍显示声明，来源标 `builtin`，不假装是平台下发 |

## 未启动

- 从 GitHub / atomgit 拉版本平台信息（schema 未证实）
- 平台策略签发与公钥分发
- 真实网络 IO（040 已核 MSRV 与 Win7 TLS 前置，需 EQ-01 / EQ-03 拍板）
- 演示层三按钮到 `GateOutcome` 的渲染层接线
- Win7 运行时判定与声明文案

## 验证

`cargo test --offline --lib core::feature_gate` 15 / 0；`cargo test --offline --lib` 331 / 0；全量 357 / 0；反向注入「允许未知 id」1 FAILED、「反转验签」10 FAILED，恢复后 331 / 0；Windows GNU 交叉检查通过。

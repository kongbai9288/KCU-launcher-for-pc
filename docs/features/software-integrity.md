# 软件完整性验证

| 字段 | 值 |
| --- | --- |
| 编号 | F052-01 / B06 / D07 |
| 状态 | 实现层已落地（`src/core/integrity.rs`）；取数与发行物签名流程未启动 |
| 触发 | 启动前读取 manifest、公钥、签名；文件读取由调用方注入 |
| 输入 | `manifest_bytes` / `public_key` / `signature` / `root` / `consecutive_failures` / `config_snapshot` / `runtime` / `modules` |
| 输出 | `Outcome { level, code, envelope, diagnostics, checked, mismatches, safe_mode, bundle }` |

## 顺序

1. manifest 空或超 1 MiB → `integrity.manifest_size` / `Fatal`
2. 签名校验（036 `verify_detached`）→ 失败 `integrity.signature` / `FeatureDisabled`，不解析内容
3. `serde_json` 逐字段解析 → 畸形、空清单、超 4096 项、摘要格式错 → `integrity.manifest_parse` / `Fatal`
4. 逐文件：`robust::safe_join` → 读字节 → 长度上限 64 MiB → `sha512` + `hex` → 比对
5. 缺失 → `Degraded`；内容不符 / 路径非法 / 超限 → `FeatureDisabled`；全通过 → `Ok`

## 兜底分级

| 级 | code | 处置 |
| --- | --- | --- |
| 零级 | `integrity.manifest_size` / `integrity.manifest_parse` / `integrity.digest_cache` | 明确报错，不崩 |
| 一级 | `integrity.signature` / `integrity.content_mismatch` / `integrity.path` / `integrity.file_size` / `integrity.rate_limited` | 禁用自定义配置并提示 |
| 二级 | `integrity.missing_file` | 自动用内置默认并提示已切换 |
| 三级 | 记 `[KCU]` 单行诊断 | 不中断 |

连续失败 ≥3 → `safe_mode=1`，导出诊断包（诊断行 + 配置快照 + 运行时信息 + 已加载模块列表）。阈值与 `src/dispatcher/launcher.rs` 第 3 次失败进安全模式一致。

## 缓存与刷新

`Cache<String,String>` 存 `path:len -> sha512hex`，容量 256 / TTL 30 s / 加载超时 5 s。长度进 key，内容变长必然重算；`refresh()` 全清。**签名与判定每次重跑，不缓存结论**。`OpBudget` 限 64 次/秒，超出返回 `disabled`，不返回 `ok`。

## 演示层三个动作的映射

| 演示层动作 | 实现层条件 | 结果 |
| --- | --- | --- |
| 用默认继续 | `level != Ok` 且 `safe_mode=0` | 忽略自定义配置，用内置默认；不加载被篡改内容 |
| 重新获取 | 任意非 `Ok` | `refresh()` 后重走 `verify()`；限流态等窗口滚动 |
| 取消 | 任意 | 不继续启动，保留诊断行 |

**如实**：051 的 `DECLARATION` 三卡与按钮是静态预览，未接实现层回调；渲染层接线属 UI 层未启动。

## 未启动

- 从 GitHub / atomgit 拉版本平台信息
- 发行物 manifest 生成、签名与公钥分发
- Win7 老旧系统运行时判定
- 真实磁盘 IO 接入（`read` 目前由调用方注入）
- 演示层按钮到 `Outcome` 的渲染层接线

## 验证

`cargo test --offline --lib core::integrity` 15 / 0；反向反转验签判定后 9 个测试 FAILED，恢复后 15 / 0；`cargo test --offline --lib` 313 / 0；全量 339 / 0；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。

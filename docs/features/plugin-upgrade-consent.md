# F037-01 插件升级需手动同意

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | 已装插件与候选包各算身份哈希（`sha512(plugin_id)` 前 16 字节 hex）；一致才进版本比较。签名校验先过，再由 `semver::cmp_precedence` 判新旧；更高版本必须 `user_confirmed_upgrade` 才 Install。 |
| 开放了什么 | `src/plugins/identity.rs::identity_hash`、`src/plugins/upgrade.rs::decide_upgrade` / `UpgradeRequest` / `UpgradeDecision`；`src/plugins/mod.rs` 导出。 |
| 登记框架 | 挂在 `src/updater/` 之上（036 的签名校验与版本决策），不新增第三方 crate。 |
| 用户使用逻辑 | 两个包被认成同一个插件时弹「确认升级插件」，显示 1.2.3 → 1.3.0 与签名通过；点「升级」才装，「暂不升级」/ × / Esc 都保留旧插件。降级仍需显式目标 + 回滚确认 + 手动同意。签名失败一律保留旧插件。 |
| 性能 | 一次 SHA-512 + 一次 Ed25519 验证 + 一次 semver 解析；无网络、无额外分配大头，O(1)。 |

状态：业务层已实现；界面层仅演示（50-plugin-upgrade.png），未进实现。

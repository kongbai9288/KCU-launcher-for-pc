# EQ-13 / Q-047-01 回滚条件数量

| 项 | 值 |
| --- | --- |
| 状态 | 待拍板；047 未改条件数量，只统一了 `+build` 相等判定 |
| 关联 | docs/records/pending-question-environments.md 的 EQ-13 段、036 更新策略、037 插件升级确认 |

## 具体环境

| 路径 | 回滚条件 | 数量 |
| --- | --- | --- |
| `src/updater/policy.rs::decide`（036） | `explicit_target` 与候选优先级相等 + `rollback_confirmed` | **2** |
| `src/plugins/upgrade.rs::decide_upgrade`（037） | `explicit_target` + `rollback_confirmed` + `user_confirmed_upgrade` | **3** |

升级路径 037 已用 `user_confirmed_upgrade` 覆盖 036 的「默认只升自动安装」。031 定最严格档为默认，032 加三档可选松档。034 起 `+build` 差异走 `cmp_precedence`；047 U94 把两条路径的相等判定统一。

## 分叉输入

```
current                 = "1.3.0"
candidate               = "1.2.2"
explicit_target         = Some("1.2.2")
rollback_confirmed      = true
user_confirmed_upgrade  = false
```

| 路径 | 结果 |
| --- | --- |
| `decide` | `Install` |
| `decide_upgrade` | `Reject` |

## 要选

| 选项 | 内容 | 后果 |
| --- | --- | --- |
| ① | 回滚也要求 `user_confirmed_upgrade`，统一为 3 个条件 | 两条路径一致；回滚多一次手动确认 |
| ② | 回滚保持 2 个条件 | 显式目标 + 二次确认视为足够；两路径继续分叉，需文档写明调用方该走哪条 |
| ③ | 由更新器插件在调用前弹确认，两处都不判 | 判定层更薄，但确认逻辑外移到插件，037 的手动同意约束需要重新落点 |

不选：两条路径对同一操作给出相反结果，Q-047-01 悬空。

# 第 012 轮开服器输入决策记录

轮次：012
状态：已批准（用户当轮明确指令）；实现、验证、合并、构建、部署、行为确认均未达到
依据：docs/spec/12-round-012-instructions.txt、docs/spec/12-server-features-input.txt、docs/spec/00-requirements.txt:3、:249、18.5、18.6

| 编号 | 决定了什么 | 约束 | 验证条件 |
| --- | --- | --- | --- |
| D01 | 开服器输入逐字落盘 | 不改字节、不抄摘要代替原文 | docs/spec/12-server-features-input.txt cmp 一致 |
| D02 | 全量问题清单 | 无删减、无保留、落到四值、给出需要的答复形式 | docs/records/open-questions.md 93 条 |
| D03 | 本轮不写 `src/` | 用户同轮写明「明天统一处理这些问题」；按 :3、:249 未拍板项进入实现前停下 | `git ls-files src/` 为空 |
| D04 | D06 未触发 | 用户当轮仍给新功能输入，且写明后续处理问题 | docs/decisions/003-remote.md D05 |
| D05 | 蓝图仍未批准 | 005-blueprint.md 状态不变 | docs/decisions/005-blueprint.md |
| D06 | X01-X04 未解除 | CF03 / CF02 / CF01 逐条待拍板 | docs/research/12-compliance.md |
| D07 | 插件源候选 | Hangar / Ore / SpigotMC / BukkitDev / Modrinth；默认源未选 | docs/research/16-server-platform.md HG01-HG11 |
| D08 | 服务端 mod 声明 | Modrinth 用 `environment` facet；CurseForge 等价字段未证实 | docs/research/16-server-platform.md MS01-MS06 |
| D09 | 官方事实优先 | `/talk` 非原版、ops.json 运行期回写、种子双格式、64×64 icon、UPnP 风险、mclo.gs 外传，全部照一手原文登记 | docs/research/16-server-platform.md |
| D10 | 重复项不合并 | 与 011 轮 13 组重叠项并列登记，合并口径待拍板 | docs/features/server-backlog.md |
| D11 | 配置集中 | 端点、端口、图标、语言包、保存路径仍按 011 轮 D14 | docs/research/14-batch-network.md K01-K09 |
| D12 | 网络批量化 | 012 轮同样禁止逐条目单发请求 | docs/research/14-batch-network.md N01-N08 |
| D13 | 后端仓只读 | 延续 011 轮 D01，本轮 0 个写请求 | docs/rules/push-scope.md R01-R04 |
| D14 | 凭据不进公仓 | 延续 011 轮 D02 | docs/rules/push-scope.md |
| D15 | 单份功能 md | 每实现一个功能时按 _template.md 单独写，本轮只做输入索引 | docs/features/server-backlog.md |
| D16 | 阶段判定 | 仍为 003-remote.md D05 功能输入阶段 | docs/features/index.md |

## 状态分层

| 层 | 值 |
| --- | --- |
| 已批准 | D01-D16 |
| 已实现 | 无 |
| 已验证 | 无 |
| 已合并 | 无 |
| 已进入构建 | 无 |
| 已部署 | 无 |
| 行为已确认 | 无 |

## 用户当轮指令的两段语义

| 段 | 原文 | 登记 |
| --- | --- | --- |
| S1 | `在搜完所有的文档以后呢，就可以彻底开工了` | 记录为开工授权，未执行；触发条件见 Q-H01 至 Q-H06 |
| S2 | `如果有一些问题你拿捏不了的，可以直接通过技术对话，然后全部告诉我不要保留，我先睡觉了，然后明天我会统一处理这些问题` | 记录为「问题全集 + 明天答复后开工」，本轮按 S2 交付 |

S1 与 S2 并列登记，不替用户选其一。Q-B01 请求确认开工时点。按 :3 与 :249，未拍板项存在时停下。

## 偏离登记

| 规则 | 偏离 | 依据 |
| --- | --- | --- |
| 9.1 连续未达应停下由用户决定范围 | 用户继续给功能输入，按当轮指令继续执行 | 18.5 |
| 用户当轮「可以彻底开工」 | 本轮未写 `src/`，见 D03 与 Q-B01 | :3、:249、S2 |
| :133 逐字保存 | 012 无凭据行，指令与输入均逐字 | 无偏离 |

## 进入实现前需用户拍板

见 docs/records/open-questions.md A-H 组共 93 条。Q-H01 至 Q-H06 全部落定后按 D07 从 core 逐层搭建。

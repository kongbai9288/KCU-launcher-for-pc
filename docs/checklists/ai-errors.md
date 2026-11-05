# AI 防错清单

来源：docs/spec/00-requirements.txt 第 6、7.3、8、9、18 节。

扫描域：`src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/`。
`docs/spec/`、`docs/checklists/`、`docs/rules/`、`docs/verification/`、`docs/index.md` 为规格、词表与验证产物，含禁用词字面量，不纳入措辞扫描。

| 编号 | 禁止项 | 检查命令 |
| --- | --- | --- |
| A01 | 套话开场 | `! grep -rE '好的|没问题|让我来|接下来我们将|需要注意的是' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A02 | 无信息量强调 | `! grep -rE '值得注意的是|需要强调的是|重要的是|务必注意' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A03 | 总结式重复 | `! grep -rE '综上所述|总而言之|总的来说|简而言之' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A04 | 假装热情、拟人化安慰、emoji、装饰性分隔线、非功能性加粗 | `! grep -rE '很棒的问题|别担心|没关系|慢慢来|相信你' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A05 | 注释里的修饰性副词 | `! grep -rE '优雅地|巧妙地|完美地' src/ demos/` |
| A06 | 教程式口吻 | `! grep -rE '你将学会|本文将介绍|让我们看看' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A07 | 空泛承诺 | `! grep -rE '后续会完善|暂时这样|以后优化' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A08 | 解释性内容 | `! grep -rE '为什么|这意味着|动机|权衡|架构理由' src/ demos/ README.md docs/research/ docs/features/ docs/records/ docs/decisions/ scripts/` |
| A09 | 空捕获、捕获后返回空值 | 代码审查 |
| A10 | 只写正常路径；未处理空值、空集合、越界、超时、编码 | 代码审查 + 边界测试 |
| A11 | 顺手改无关文件 | `git diff --name-only` 逐项核对本轮范围 |
| A12 | 硬编码绝对路径、架构名、密钥 | `! grep -rE 'C:\\\\|gh[p]_|github_pat_|x-api-key *=' src/ demos/ README.md` |
| A13 | 路径散落多处 | 路径模块单一入口 |
| A14 | 跨进程消息无统一信封、无请求标识、无统一错误 | 代码审查 |
| A15 | 谎报验证结果、编造命令输出 | 每条结论附真实命令与输出 |
| A16 | 改测试、加跳过、删测试来让分支通过 | 测试文件 SHA-1 锁定 |
| A17 | 把凭据写入仓库 | `! grep -rqE 'gh[p]_' .` |
| A18 | 每轮开工未完整读本文档与需求原文 | 按 docs/index.md 读取命令执行 |
| A19 | 用时间戳冒充后续动作证据 | 证据只认 8.1 原始产物核对 |
| A20 | 中间态四值 | 每条结论落到四值之一 |
| A21 | 403 policy_default_denied 写成服务故障 | `! grep -rE '服务不可用|服务故障' docs/research/` |
| A22 | 示例配置值当成默认值 | `grep -n 'broadcast-rcon-to-ops' docs/research/06-server.md` 与 https://minecraft.wiki/w/Server.properties 逐项比对 |
| A23 | 四值使用「部分已证实」 | `! grep -rE '部分已证实' docs/research/ docs/features/ docs/records/ docs/decisions/` |
| A24 | 锚点写「同上」或裸域名短名 | `! grep -rE '同上' docs/research/`；逐行核对 URL 完整性 |
| A25 | 设计稿品牌元素进入实现代码 | `! grep -rE 'FCL|揉纸启动器' src/ 2>/dev/null` |
| A26 | 轻量模式引用正常模式 UI 资产 | `! grep -rE 'assets/ui|normal-mode-v3' src/ 2>/dev/null` |
| A27 | 逐字副本字节被改动 | `cmp` 来源与落盘；SHA-1 双端一致 |
| A28 | 工具摘要与一手原文不一致时采用摘要（关联 A22） | `grep -n 'Introduced in' docs/research/06-server.md`；结论只取 EVIDENCE 原句 |
| A29 | 第三方推广页排名写成选型结论（关联 R02） | `! grep -rE '表现得最优|使用人数最多|社区反馈最积极' docs/features/ docs/decisions/` |
| A30 | 未取得一手原文就写死构建参数或进程参数 | `grep -n '未证实' docs/research/11-runtime.md`；构建配置生成前逐项核对 |
| A31 | 功能登记写成已实现（关联 9.3 状态分层） | `test -z "$(grep -L '未实现' docs/features/dispatcher.md docs/features/lightweight.md docs/features/headless.md docs/features/normal-launcher.md docs/features/lan.md docs/features/server.md docs/features/log.md docs/features/fallback.md docs/features/envelope.md docs/features/ui-framework.md)"` |

## 输出结构

1. 本轮行动或结论
2. 时间戳回显
3. 本轮目标与范围
4. 设计与代码
5. 运行逻辑演示
6. 自我批判
7. 四值判决
8. 独立验证证据
9. 自评
10. 通过标记或未通过
11. 本轮文档更新
12. 唯一下一步

## 冲突优先级

独立验证结论 > 自评 > 时间戳；四值判决 > 通过标记；仓库内容边界 > 文档完整性；幻觉红线 > 输出结构完整性；用户当轮明确指令 > 本文件规则；安全与许可证合规 > 功能进度。

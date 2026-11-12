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
| A31 | 功能登记写成已实现（关联 9.3 状态分层） | `test -z "$(grep -L '未实现' docs/features/dispatcher.md docs/features/lightweight.md docs/features/headless.md docs/features/normal-launcher.md docs/features/lan.md docs/features/server.md docs/features/log.md docs/features/fallback.md docs/features/envelope.md docs/features/ui-framework.md docs/features/credential-guard.md)"` |
| A32 | 服务条款原文未取得就写死镜像缓存或共享密钥（关联 18.6） | `grep -n 'CF01\|CF02\|CF03\|CF04' docs/research/12-compliance.md` |
| A33 | 两个不同上游返回同名同 sha 的 tag 当成版本号（关联 A28） | `grep -n 'v99.99' docs/research/12-compliance.md`；结论标已失败 |
| A34 | 许可证逐字副本重复落盘 | `sha1sum docs/licenses/*.txt docs/licenses/*.md` 逐项核对；同 sha 只留一份 |
| A35 | 功能 md 的验证命令输出写推测值（关联 A15） | 每条 `grep -c` / `grep -n` 先实跑再写入 |
| A36 | 逐条目单发网络请求（关联 14-batch-network.md N01） | `grep -n '每搜索一个模组' docs/spec/11-round-011-instructions.txt` |
| A37 | 把 Windows 区域设置当成物理位置（关联 13-platform-api.md P01-P04） | `grep -n 'GEOID_NOT_AVAILABLE' docs/research/13-platform-api.md` |
| A38 | 用 GetVersionEx 判定 OS 版本（关联 OS03） | `grep -n 'versionhelpers' docs/research/13-platform-api.md` |
| A39 | 写死 API 基址、端口、图标路径、语言包路径（关联 K01-K07） | `grep -n 'K01' docs/research/14-batch-network.md` |
| A40 | 把 Win10+ Rust 目标当成 Win7 可用（关联 RW01-RW04） | `grep -n 'require at least Windows 10' docs/research/13-platform-api.md` |
| A41 | 对只读后端仓发写请求（关联 BR01-BR02） | `grep -n '只允许' docs/research/15-input-survey.md`；每轮核对请求方法 |
| A42 | 把 id 具体值写进文档（关联 PL03、PL05） | `grep -n '未读取、未写入' docs/research/15-input-survey.md` |
| A43 | 编号功能登记漏条（关联 backlog.md 55 条） | `grep -cE '^\| [0-9]+ \|' docs/features/backlog.md` |
| A44 | 插件开源许可页缺 5 字段（关联 OL01） | `grep -n 'OL01' docs/research/15-input-survey.md` |
| A45 | 拼接开源代码后不做源与产物对比（关联 OL05） | `grep -n 'OL05' docs/research/15-input-survey.md` |
| A46 | 把 `/talk` 当原版命令（关联 CM02） | `grep -c '未出现' docs/research/16-server-platform.md` |
| A47 | 运行期监听 ops.json 判定 op 变更（关联 OP02） | `grep -c 'writes the whole list back' docs/research/16-server-platform.md` |
| A48 | 把区域设置或 GEOID 当物理位置（关联 A37） | `grep -c '不等于物理位置' docs/checklists/windows-errors.md` |
| A49 | 把 mclo.gs 上传当本地导出（关联 MC03） | `grep -c '一键上传 mclo.gs' docs/features/server-backlog.md` |
| A50 | mrpack 导入不做路径穿越校验（关联 MS07） | `grep -c 'exit the Minecraft instance directory' docs/research/16-server-platform.md` |
| A51 | 待拍板问题漏条（关联 open-questions.md 93 条） | `grep -cE '^\| Q-[A-H][0-9]' docs/records/open-questions.md` |
| A52 | 未答复 Q-H 组就写 src/（关联 :249） | 013 轮起改为 `test -n "$(git ls-files src/)"`，D06 已触发 |
| A53 | 弹窗缺关闭路径（关联 013 H03） | `cargo test --offline every_catalog_popup` |
| A54 | 单参数无法加入服务器（关联 013 U01） | `cargo test --offline single_arg` |
| A55 | 双击服务器时用户权重不排第一（关联 013 U02） | `cargo test --offline user_choice_ranks_first` |
| A56 | 流程结束残留未关弹窗（关联 013 H06） | `cargo test --offline no_popup_is_left_open` |
| A57 | 缓存无容量上限或 order 无限增长（关联 014 D04/D06） | `cargo test --offline capacity_bounds_entry_count`、`order_stays_bounded_after_many_inserts` |
| A58 | 同 key 并发重复加载（关联 011 聚合请求、014 D04） | `cargo test --offline single_flight_loads_once` |
| A59 | 多源下载一个完成后其余未取消、线程未 join（关联 011 第 30 条、014 D05） | `cargo test --offline race_returns_first_and_cancels_other_sources`、`drop_joins_without_explicit_shutdown` |
| A60 | 活跃计数不归零或弱引用注册表未清理（关联 014 D06） | `cargo test --offline core::leak` |
| A61 | 工作流出现凭据字面量（关联 014 D01） | `! grep -rE 'gh[p]_' .github/workflows/` |

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

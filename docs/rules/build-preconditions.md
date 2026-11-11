# 底层搭建前置条件清单

轮次：013
状态：已触发（013 轮 F07/F08/F09）
对应：docs/spec/00-requirements.txt:249、docs/decisions/003-remote.md D05-D08、docs/decisions/005-blueprint.md C06

## 触发链

| 序 | 条件 | 010-012 值 | 013 值 | 来源 |
| --- | --- | --- | --- | --- |
| 1 | 用户提供 D06 信号（明确不再有新功能） | 未提供 | **已提供** F07/F08 | docs/decisions/003-remote.md D06 |
| 2 | 005-blueprint.md 状态为已批准 | 未批准 | **已批准** F09 | docs/decisions/005-blueprint.md:6 |
| 3 | 本清单 X01-X04 用户拍板 | 未拍板 | F10 授权按正常情况与用户逻辑落地；CF 下载模块不在 L1 范围 | docs/records/round-013-answers.md |
| 4 | 逐层独立验证通过 | 未开始 | L1 本轮独立验证进行中 | docs/decisions/003-remote.md D07 |
| 5 | Q-H01 至 Q-H06 全部落定 | 未满足 | 013 答复后满足到开工层 | docs/records/open-questions.md |
| 6 | Q-A 至 Q-G 细节 | 未答复 | 已答复，细节按用户逻辑落地 | docs/records/round-013-answers.md |

013 轮起 L1 已落地：`src/` 非空，Cargo.toml 存在，crate 依赖为 std only。X01-X04 仍登记为已证实冲突，但不阻塞不含下载模块的 core 层。

## D07 逐层顺序与前置

| 层 | 目标 | 前置条件 | 当前四值 |
| --- | --- | --- | --- |
| L1 | core | 蓝图已批准；K01-K04、K07 抽象确认 | **已实现、已验证**；9 模块、37 测试、release 构建通过 |
| L2 | dispatcher | L1 独立验证通过；F002 已批准 | 未证实；013 轮未启动 |
| L3 | lightweight | L2 通过；F003 已批准；WebView2 检测键已证实 | 未证实 |
| L4 | headless | L3 通过；F004 已批准；F012 凭据保护方案已批准 | 未证实 |
| L5 | normal | L4 通过；F005 已批准；HMCL 代码复用范围已证实 | 未证实 |
| L6 | UI | L5 通过；F011 已批准；UI 稿品牌与字体授权已取得 | 未证实 |
| L7 | 构建 | L6 通过；Cargo profile 取值确认；目标三元组确认 | 未证实 |
| L8 | 部署 | L7 通过；MSVC 运行库部署方式确认 | 未证实 |

## 010 轮新增阻塞项

| 编号 | 阻塞项 | 四值 | 来源 |
| --- | --- | --- | --- |
| X01 | CurseForge CF03 与缓存字段冲突 | 已证实 | docs/research/12-compliance.md |
| X02 | CurseForge CF03 与默认镜像配置冲突 | 已证实 | docs/research/12-compliance.md |
| X03 | CurseForge CF02 与代理/VPN 路径冲突 | 已证实 | docs/research/12-compliance.md |
| X04 | CurseForge CF01 与共享 API Key 冲突 | 已证实 | docs/research/12-compliance.md |
| X05 | CF04 竞争产品范围 | 未证实 | docs/research/12-compliance.md |
| X06 | CF05 配额阈值 | 未证实 | docs/research/12-compliance.md |
| X07 | CF06 30 天无因终止，依赖该 API 的功能需可禁用 | 未证实 | docs/research/12-compliance.md |

X01-X04 落在 docs/spec/00-requirements.txt:171-172、docs/research/03-download.md 已登记的字段上。按 docs/spec/00-requirements.txt:249，进入构建前由用户拍板；不自行选一条执行、另一条忽略。

## 未解决四值项

| 类别 | 项 | 四值 |
| --- | --- | --- |
| 授权 | UI 稿品牌与字体授权 | 未证实 |
| 授权 | 本项目 LICENSE | 未证实 |
| 批准 | 005-blueprint.md | 未证实 |
| 批准 | F012 凭据保护方案 | 未证实 |
| 信号 | D06 | 未证实 |
| 协议 | CF04 / CF05 / CF06 / MCIM / BMCLAPI 条款 | 未证实 |
| 协议 | Modrinth 缓存与限流条款 | 未证实 |
| 实现 | Notchian 服务端离线 UUID 行为 | 未证实 |
| 实现 | 加载器逐版本 schema | 未证实 |
| 实现 | 令牌保护、Azure Client ID | 未证实 |
| 实现 | CREATE_NO_WINDOW、std::process 超时 API、WebView2 内存占用关系 | 未证实 |
| 实现 | 单文件发布工具链、多操作入口交互形式 | 未证实 |
| 环境 | 浏览器渲染、rustc/cargo | 受阻 |
| 网络 | git HTTP 推送、6 个上游主机、未认证 /rate_limit、MCIM 仓库定位 | 受阻 |

## 011 新增阻塞项

| 编号 | 阻塞项 | 四值 | 来源 |
| --- | --- | --- | --- |
| Q01 | Win7 兼容路径未选（Tier 3 自建 std / VxKex / 旧版工具链 / 拆分产物） | 已证实（冲突成立） | docs/research/13-platform-api.md C01 |
| Q02 | 多架构范围与 ARM64 取舍未定 | 已证实（部分冲突） | docs/research/13-platform-api.md C03 |
| Q03 | Win7 与 ARM64 同时支持 | 已失败 | docs/research/13-platform-api.md C04 |
| Q04 | 地域判定口径未定（物理位置或区域设置） | 未证实 | docs/research/13-platform-api.md P04-P07 |
| Q05 | 文件管理开源骨干项目未选定 | 未证实 | docs/research/15-input-survey.md DS06 |
| Q06 | ViaNBT 与 Rust 集成方式未定 | 未证实 | docs/research/15-input-survey.md VN05 |
| Q07 | VxKex 兼容范围 | 未证实 | docs/research/13-platform-api.md RW11 |
| Q08 | 后端仓只读 | 已证实（硬约束） | docs/research/15-input-survey.md BR01-BR02 |
| Q09 | CF 凭据未提供，特殊版私仓未创建 | 未证实 | docs/decisions/011-feature-input.md D02-D03 |
| Q10 | UI 稿品牌与字体授权 | 未证实 | docs/decisions/007-normal-ui.md |
| Q11 | D06 触发信号 | 未证实 | docs/decisions/003-remote.md D06 |
| Q12 | 005-blueprint.md 批准 | 未证实 | docs/decisions/005-blueprint.md |

触发链新增条件 5：Q01-Q12 中标记为「进入构建前需用户拍板」的项全部落定。条件 1-5 全部满足前，`src/` 保持为空。

## 012 新增阻塞项

| 编号 | 阻塞项 | 四值 | 来源 |
| --- | --- | --- | --- |
| R01 | 开工时点：用户同轮给出「可以彻底开工」与「问题明天统一处理」 | 已证实（并列登记） | docs/decisions/012-server-input.md S1/S2 |
| R02 | 待拍板问题全集 93 条，A-H 组 | 已证实 | docs/records/open-questions.md |
| R03 | D06 信号、005-blueprint.md 批准、X01-X04 逐条拍板 | 未证实 | Q-H01 至 Q-H03 |
| R04 | 插件源默认选择、CurseForge server-only 等价字段 | 未证实 | docs/research/16-server-platform.md HG11、MS06 |
| R05 | `/talk` 来源、op 锁定途径、种子双格式、Java 镜像、UPnP 默认、mclo.gs 外传 | 未证实 | docs/research/16-server-platform.md |
| R06 | AI API 容器网段与回环约束冲突 | 已证实（冲突成立） | Q-B05 |
| R07 | 「境外用官方源」与地域判定口径冲突 | 已证实（冲突成立） | Q-B06 |
| R08 | ops.json 运行期内存回写与文件监听冲突 | 已证实（冲突成立） | Q-C03 |
| R09 | UPnP IGD 安全风险、mrpack 路径穿越、mclo.gs 日志外传 | 已证实 | Q-C13、Q-D14、Q-C15 |
| R10 | 重复功能项合并口径 | 未证实 | Q-B08 |

触发链新增条件 6：docs/records/open-questions.md 的 Q-H01 至 Q-H06 全部落定。条件 1-6 全部满足前，`src/` 保持为空，不生成 Cargo.toml、build.rs、target spec。

## 判定

| 项 | 010-012 值 | 013 值 |
| --- | --- | --- |
| 通过标记 | 不发 | 本层不发全局通过标记；L1 单独结论见 docs/verification/round-013.md |
| 原因 | 存在未解决的已失败 / 未证实 / 受阻；独立验证结论为部分通过；自评 < 7 | X01-X04、品牌替换、CF API 方法、UI 端到端仍未闭环 |
| src/ | 空 | 9 个 core 模块 + lib.rs + mod.rs |
| 下一层动作 | 用户拍板 D06、蓝图、X01-X04 | L2 dispatcher，须先完成 L1 独立验证 |

## 约束

| 编号 | 内容 |
| --- | --- |
| B01 | 本清单只列条件与四值，不列实现步骤。 |
| B02 | 条件未满足时不修改 005-blueprint.md 状态字段；013 轮已满足后按用户指令修改。 |
| B03 | 条件未满足时不生成 Cargo.toml、build.rs、src/ 下任何文件；013 轮条件满足后按 D07 生成。 |
| B04 | 每轮重新核对条件 1-6。 |
| B05 | 013 轮起 L1 只做纯 std 实现，不引入外部 crate、不碰下载模块、不写死端点与盘符。 |

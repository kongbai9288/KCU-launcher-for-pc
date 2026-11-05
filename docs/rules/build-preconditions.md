# 底层搭建前置条件清单

轮次：010
状态：待用户拍板
对应：docs/spec/00-requirements.txt:249、docs/decisions/003-remote.md D05-D08、docs/decisions/005-blueprint.md C06

## 触发链

| 序 | 条件 | 当前值 | 来源 |
| --- | --- | --- | --- |
| 1 | 用户提供 D06 信号（明确不再有新功能） | 未提供 | docs/decisions/003-remote.md D06 |
| 2 | 005-blueprint.md 状态为已批准 | 未批准 | docs/decisions/005-blueprint.md:6 |
| 3 | 本清单 X01-X04 用户拍板 | 未拍板 | docs/research/12-compliance.md |
| 4 | 逐层独立验证通过 | 未开始 | docs/decisions/003-remote.md D07 |

条件 1-4 全部满足前，`src/` 保持为空，不生成构建配置，不引入 crate。

## D07 逐层顺序与前置

| 层 | 目标 | 前置条件 | 当前四值 |
| --- | --- | --- | --- |
| L1 | core | 蓝图已批准；K01-K04、K07 抽象确认 | 未证实 |
| L2 | dispatcher | L1 独立验证通过；F002 已批准 | 未证实 |
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

## 判定

| 项 | 值 |
| --- | --- |
| 通过标记 | 不发 |
| 原因 | 存在未解决的已失败 / 未证实 / 受阻；独立验证结论为部分通过；自评 < 7 |
| src/ | 空 |
| 下一层动作 | 用户拍板 D06、蓝图、X01-X04 |

## 约束

| 编号 | 内容 |
| --- | --- |
| B01 | 本清单只列条件与四值，不列实现步骤。 |
| B02 | 条件未满足时不修改 005-blueprint.md 状态字段。 |
| B03 | 条件未满足时不生成 Cargo.toml、build.rs、src/ 下任何文件。 |
| B04 | 每轮重新核对条件 1-4。 |

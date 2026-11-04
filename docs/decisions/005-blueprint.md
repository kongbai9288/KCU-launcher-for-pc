# 框架蓝图方案

| 项 | 值 |
| --- | --- |
| 编号 | 005 |
| 状态 | 未批准 |
| 版本 | 0.0.0 |
| 轮次 | 005 |
| 对应需求 | docs/spec/00-requirements.txt:46 |

## 方案条目

| 编号 | 类 | 值 |
| --- | --- | --- |
| B01 | 分层 | core → dispatcher → lightweight / headless / normal → ui / server / lan → build |
| B02 | 目录 | src/core/、src/dispatcher/、src/lightweight/、src/headless/、src/normal/、src/ui/、src/server/、src/lan/、src/build/ |
| B03 | core | envelope、paths、log、config、fallback、provider、args |
| B04 | dispatcher | task、mode、launcher |
| B05 | lightweight | login、download、loaders |
| B06 | headless | entry、kcul |
| B07 | normal | eula、ui、server、lan |
| B08 | ui | frame、components |
| B09 | server | jar、rcon、automation、config_zh、tools |
| B10 | lan | discovery、protocol、transfer |
| B11 | build | bundle、manifest |

## 关键抽象

| 编号 | 名称 | 输入输出 | 约束来源 |
| --- | --- | --- | --- |
| K01 | Envelope | request / response / event、request_id、统一 error | docs/spec/00-requirements.txt:114 |
| K02 | PathResolver | 逻辑名 → PathBuf | docs/spec/00-requirements.txt:113 |
| K03 | Diagnostics | 单行 `[KCU] <域> <动作> <目标> <结果> <详情>` | docs/spec/00-requirements.txt:182 |
| K04 | FallbackLevel | 0 / 1 / 2 / 3，安全模式，诊断包 | docs/spec/00-requirements.txt:179-182 |
| K05 | LaunchTask | c/kcu/kculauncher/*.json 与 .kcul → 统一任务 | docs/spec/00-requirements.txt:7,17 |
| K06 | ModeSelector | 内存 ≤ 2GB 且首次 → lightweight；config/launch.json 覆盖 | docs/spec/00-requirements.txt:8 |
| K07 | Provider | 默认镜像、密钥可选、基址配置项 | docs/spec/00-requirements.txt:171-173 |
| K08 | UiFrame | 组件注册表，normal 模式共用 | docs/spec/00-requirements.txt:24 |
| K09 | Automation | 定期 / 持续 / 单次 | docs/spec/00-requirements.txt:21 |
| K10 | ServerToolApi | 本地 AI 工具管理入口 | docs/spec/00-requirements.txt:21 |

## 扩展点

| 编号 | 扩展点 | 注册内容 |
| --- | --- | --- |
| E01 | auth | mojang、离线、第三方 |
| E02 | download | 官方、BMCLAPI、MCIM、Modrinth、CurseForge |
| E03 | loader | Fabric、Forge、NeoForge、Quilt、LiteLoader、OptiFine |
| E04 | ui | normal 模式组件 |
| E05 | automation | 定期、持续、单次 |
| E06 | lan | 发现、协议、文件互传 |
| E07 | server_jar | 常用服务端 jar |

## 约束

| 编号 | 约束 |
| --- | --- |
| C01 | 本方案未批准；src/ 保持空目录。 |
| C02 | 未证实字段不写进实现。 |
| C03 | 不写死目标三元组、绝对路径、密钥。 |
| C04 | 语言范围中文与英文。 |
| C05 | 扩展点注册不修改 core 模块。 |
| C06 | 统一搭建启动需 003-remote.md D06 触发且本方案状态为已批准。 |
| C07 | K08 与 E04 仅服务 normal 模式；lightweight 不加载 ui 框架与 normal 模式资产，见 docs/decisions/007-normal-ui.md D03-D05。 |

## 验证条件

| 编号 | 命令 | 期望 |
| --- | --- | --- |
| V01 | `git ls-files src/` | 输出为空 |
| V02 | `! grep -rE 'C:\\\\|gh[p]_|x-api-key *=' src/` | exit 0 |
| V03 | `按 docs/checklists/ai-errors.md A23 执行` | exit 0 |
| V04 | `! grep -rE '同上' docs/research/` | exit 0 |
| V05 | `rustc --version` | 可用后进入构建验证 |

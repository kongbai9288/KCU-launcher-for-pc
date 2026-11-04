# HMCL 结构与许可证

检索日期：2026-11-05
锚点格式：完整 URL 或 `path:line`；锚点逐行独立。

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| 仓库 | github.com/HMCL-dev/HMCL | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL |
| 根目录条目 | HMCL、HMCLCore、HMCLBoot、buildSrc、config、docs、gradle、lib、minecraft、LICENSE、settings.gradle.kts、build.gradle.kts、gradlew、gradlew.bat、gradlew.ps1、AGENTS.md | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL/contents/ |
| settings.gradle.kts | 14 行，rootProject.name = HMCL3，含 include 与 minecraftLibraries 目录映射 | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL/contents/settings.gradle.kts |
| 构建系统 | Gradle Kotlin DSL 多模块 | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL/contents/ |
| 精确构建任务名 | 未取得 | 未证实 | build.gradle.kts 原文未读取 |
| UI | JavaFX | 已证实 | https://hmcl.huangyuhui.net/ |
| 支持加载器 | Forge、NeoForge、Fabric、Quilt、LiteLoader、OptiFine、Cleanroom | 已证实 | https://hmcl.huangyuhui.net/ |
| 许可证名称 | GPLv3，repo 字段 license.spdx_id = GPL-3.0 | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL |
| LICENSE 全文 | 685 行，35507 字节，SHA-1 e58dbdf3bc2df8d7d3e808a39efbdc845cc2350f | 已证实 | docs/licenses/HMCL-LICENSE.txt:1-685 |
| 附加条款 1 | 分发修改版须以合理方式更改软件名称或版本号，Under GPLv3 7(c) | 已证实 | docs/licenses/HMCL-LICENSE.txt:679-681 |
| 附加条款 2 | 不得移除程序显示的版权声明，Under GPLv3 7(b) | 已证实 | docs/licenses/HMCL-LICENSE.txt:683-684 |
| /license 端点 spdx_id | null，name=LICENSE | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL/license |
| 最新 release | v3.16.4，发布 2026-09-17T04:30:46Z | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL/releases/latest |
| 仓库最后推送 | 2026-11-04T14:23:24Z，默认分支 main | 已证实 | https://api.github.com/repos/HMCL-dev/HMCL |
| 可复用代码范围 | 未确定 | 未证实 | 依赖本项目许可证与分发形态判定 |
| 启动命令生成 | DefaultLauncher.generateCommandLine 参数顺序未核对 | 未证实 | https://github.com/HMCL-dev/HMCL |
| 版本清单解析 | inheritsFrom、库规则、SHA-1、asset index 处理未核对 | 未证实 | https://github.com/HMCL-dev/HMCL |

## 005 补证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| GET /repos/HMCL-dev/HMCL/license | 200，base64 解码 35507 字节 | 已证实 |
| GET /repos/HMCL-dev/HMCL/contents/ | 200，24 个根目录条目 | 已证实 |
| GET /repos/HMCL-dev/HMCL/releases/latest | 200，tag_name v3.16.4 | 已证实 |

来源：
- https://github.com/HMCL-dev/HMCL
- https://hmcl.huangyuhui.net/
- https://api.github.com/repos/HMCL-dev/HMCL/license

约束：
- 不复制代码、资源、商标、登录 Client ID，直到复用范围经许可证核对。
- 主语言 Java，与本项目 Rust 不共享二进制接口。

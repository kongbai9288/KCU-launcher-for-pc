# 第 011 轮输入中外部项目与只读仓核实

检索日期：2026-11-11
轮次：011
对应：docs/spec/11-features-input.txt 第 9、46、54 条与开头段；docs/spec/11-round-011-instructions.txt
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。

## 后端仓只读约束

| 编号 | 项 | 值 | 四值 |
| --- | --- | --- | --- |
| BR01 | 用户当轮指令「我后端的那个仓你只能读，因为他被我部署了自动部署，如果说你不想去处理了，后果是毁灭性的」 | 只读硬约束 | 已证实 |
| BR02 | 本轮对该仓发出的请求 | 4 个 `GET`，未发出 `POST` / `PUT` / `PATCH` / `DELETE` | 已证实 |
| BR03 | `GET /repos/kongbai9288/modmarket-backend` | 200，`private=true`，`default_branch=main`，`pushed_at=2026-11-10T15:40:42Z` | 已证实 |
| BR04 | description 字段 | `Cloudflare Worker backend: GitHub OAuth + CurseForge proxy for ModMark` | 已证实 |
| BR05 | `GET /branches` | 200，2 个分支 `diag` / `main` | 已证实 |
| BR06 | `GET /contents/` | 200，9 个根条目：`.github`、`.gitignore`、`README.md`、`SECURITY_AUDIT.md`、`V1_MERGE.md`、`package.json`、`src`、`test.txt` | 已证实 |
| BR07 | `GET /contents/README.md` | 200，2523 字节 | 已证实 |
| BR08 | README 正文、端点、密钥、部署配置内容 | 未读取进公仓，未复制进任何文档、代码、注释、提交说明 | 已证实 |
| BR09 | 正常版本走用户后端仅限境外场景 | 用户当轮要求 | 已证实 |
| BR10 | 后端仓 URL 是否写入公仓文档 | 仅出现在用户逐字输入副本；本项目撰写文档不写具体端点与内容 | 已证实 |

约束：

| 编号 | 内容 |
| --- | --- |
| C01 | 对该仓只允许 `GET`，任何写请求触发零级停止。 |
| C02 | 不读取仓库内容进公仓，不复制端点、密钥、部署配置。 |
| C03 | 不 fork、不改分支、不建 issue、不触发自动部署路径。 |
| C04 | 每轮重新声明本约束，见 docs/rules/push-scope.md。 |

## CopperGolemLauncher（第 46 条）

| 编号 | 项 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| CG01 | 仓库存在 | `copper-lamp/CopperGolemLauncher`，默认分支 `main` | 已证实 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher |
| CG02 | description | `为 Minecraft Bedrock 打造的现代化模块化启动器：把版本、账户与游戏内容，收进一个干净、迅捷的入口` | 已证实 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher |
| CG03 | `license.spdx_id` | `NOASSERTION` | 已证实 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher/license |
| CG04 | 根目录条目 | 23 个，含 `LICENSE`、`THIRD_PARTY_NOTICES`、`Cargo.toml`、`copper-module-abi`、`frontend`、`native`、`patches` | 已证实 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher/contents/ |
| CG05 | `LICENSE` 逐字副本 | `docs/licenses/CopperGolemLauncher-LICENSE`，35834 字节，SHA-1 前 16 `97b9e831e4b309bd` | 已证实 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher/contents/LICENSE |
| CG06 | `LICENSE` 头部 | `CopperGolem Launcher \| Copyright (C) 2026 copper-lamp \| This program is free software: you can redistribute it and/or modify it under the terms of the GNU General` | 已证实 | docs/licenses/CopperGolemLauncher-LICENSE:1-4 |
| CG07 | `GET /releases/latest` | 404 Not Found | 受阻 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher/releases/latest |
| CG08 | 用户要求 | 做成插件，适配 UI 后单开一个仓库发出；遵守许可证；本项目默认不内置；插件系统默认显示并引导下载 | 已证实 | docs/spec/11-features-input.txt 第 46 条 |
| CG09 | 许可证全文与附加条款逐行核对 | 已取得全文，未逐行判定可复用范围 | 未证实 | CG05 |
| CG10 | 插件独立仓与适配 UI 的交付形态 | 未定 | 未证实 | 用户当轮输入 |

按 docs/spec/00-requirements.txt:249，CG09 未证实前不复制该项目代码、资源、商标。

## PrismLauncher CMakeLists 中的 id（第 54 条）

| 编号 | 项 | 值 | 四值 |
| --- | --- | --- | --- |
| PL01 | 用户要求复用 `https://github.com/PrismLauncher/PrismLauncher/blob/develop/CMakeLists.txt` 中的 id，需给出风险提示，或允许用户自填 id | 已证实 | docs/spec/11-features-input.txt 第 54 条 |
| PL02 | 文档需公开「链接使用别人项目的 id」这一事实 | 已证实 | docs/spec/11-features-input.txt 第 54 条 |
| PL03 | id 具体值不写进文档、不在用户界面公开，可写进代码 | 已证实 | docs/spec/11-features-input.txt 第 54 条 |
| PL04 | `GET /repos/PrismLauncher/PrismLauncher/contents/CMakeLists.txt` | 200，24721 字节；仅确认文件存在与大小 | 已证实 |
| PL05 | id 具体值 | 未读取、未写入本文档、未写入任何仓库文件 | 已证实 |
| PL06 | 令牌与 id 的操作系统保护路径 | 见 docs/features/credential-guard.md、docs/research/12-compliance.md DP01-DP04 | 已证实 |
| PL07 | 风险提示文案与自填 id 的交互 | 未定 | 未证实 |

## ViaNBT（第 6 条）

| 编号 | 项 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| VN01 | `ViaVersion / ViaNBT` | `A library for dealing with Minecraft NBT.` / `NBT and SNBT` | 已证实 | https://github.com/ViaVersion/ViaNBT |
| VN02 | 许可证 | `MIT license` | 已证实 | https://github.com/ViaVersion/ViaNBT |
| VN03 | 语言 | `Java 100.0%` / `Update to Java 8` | 已证实 | https://github.com/ViaVersion/ViaNBT |
| VN04 | 派生关系 | `This project is derived from an earlier version of OpenNBT` | 已证实 | https://github.com/ViaVersion/ViaNBT |
| VN05 | 与本项目 Rust 形态的集成方式（JNI、子进程、或改用 Rust NBT crate） | 未取得一手方案 | 未证实 | 用户当轮输入 |
| VN06 | `LICENSE.txt` 全文逐字副本 | 未取得 | 未证实 | https://github.com/ViaVersion/ViaNBT |

## dsh 文件管理插件（开头段）

| 编号 | 项 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| DS01 | 用户要求 | 文件管理「使用逻辑」大致与 dsh 类似；不直接使用 dsh；用开源其他项目 | 已证实 | docs/spec/11-features-input.txt 开头段 |
| DS02 | `chumoe/dsh-file-manager` | MIT，`window.__ModuleLoader__.load({ id, factory })` 的 JS/React 模块，路由经 `ctx.connection.fetch.register` | 已证实 | https://awesome-dsh-plugin.com/p/chumoe/dsh-file-manager |
| DS03 | 写入策略 | `writes are temp-file + atomic rename and compare the base mtime to surface external modification as 409 conflict` | 已证实 | https://awesome-dsh-plugin.com/p/chumoe/dsh-file-manager |
| DS04 | 解压策略 | `Extraction goes to a temporary directory inside the workspace and only then moves entries to a unique destination name` | 已证实 | https://awesome-dsh-plugin.com/p/chumoe/dsh-file-manager |
| DS05 | 技术栈差异 | JS/React 插件模块，不是 Rust 桌面组件 | 已证实 | DS02 |
| DS06 | 直接复用的开源文件管理骨干项目 | 未选定 | 未证实 | 用户当轮输入 |

## VxKex（声明页文案）

| 编号 | 项 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- | --- |
| VK01 | `VxKex is a free, open‑source set of API extensions for Windows 7 that lets many modern apps built for Windows 8/10/11 run on the older OS by injecting compatibility DLLs without modifying system files.` | Win7 API 扩展层 | 已证实 | https://vxkex.com/ |
| VK02 | 仓库 `https://github.com/i486/VxKex` | 开源 | 已证实 | https://www.nihendiao.com/?p=4536/ |
| VK03 | 用户指定声明页文案含「我们建议使用VxKex支持」 | 已证实 | docs/spec/11-features-input.txt 开头段 |
| VK04 | VxKex 是否随本项目分发 | 未定 | 未证实 | 用户当轮输入 |

## 其他专有名词

| 项 | 一手结果 | 四值 |
| --- | --- | --- |
| 陶瓦联机（第 11 条） | 未取得项目或协议的一手来源 | 未证实 |
| atomgit（声明页来源仓库） | 用户列为候选来源，未核实站点与 API | 未证实 |
| `§` 模板版本号（第 29 条） | 用户自定义镜像 URL 占位符，示例 `https://www.example.com/v1/download/<§>` | 已证实 |
| `.kculf` / `kculh`（第 34 条） | 用户当轮给出的扩展名；`.kculf` 跳过 GUI 直接进 MC，`kculh` 为无头 | 已证实 |
| 「用了咱们软件两天」/ 拓展包解锁 | 用户当轮条件，计时与解锁实现未定 | 未证实 |
| 「5gb 2小时」「并联关系」熔断（第 4 条） | 用户当轮阈值已登记，实现未定 | 已证实 |

## 开源许可页动态条目规则

| 编号 | 用户原文 | 约束 | 四值 |
| --- | --- | --- | --- |
| OL01 | `如果说插件当中有使用别人的开源代码的，在插件加载以后会在开源许可当中增加一个对应插件的名字下面加上许可证和作者名字，项目地址，修改后版本地址` | 5 个字段：插件名、许可证、作者名、项目地址、修改后版本地址 | 已证实 |
| OL02 | `有完整的关于与第三方开源许可（当中前面所有的图片都必须用真正的图片）` | 关于页与第三方开源许可页完整 | 已证实 |
| OL03 | `咱们使用的许可证是gplv3,这样你应该要链接使用` | 项目 GPLv3，不同许可证用动态链接 | 已证实 |
| OL04 | `每一个使用别人的源代码前面都要加上对应项目的许可证` | 源文件头许可证声明 | 已证实 |
| OL05 | `每一次干完别人的代码以后，把两个代码对比看看你有没有因为输出导致的一些内容遗漏` | 拼接后做源与产物对比 | 已证实 |
| OL06 | 插件独立许可证、独立进程 | 已证实 | docs/spec/11-features-input.txt 开头段 |
| OL07 | 本项目 LICENSE 文件 | 未生成 | 未证实 |

## 011 新增来源

| 编号 | URL | 用途 | 结果 |
| --- | --- | --- | --- |
| P43 | https://api.github.com/repos/kongbai9288/modmarket-backend | BR03-BR04，只读 GET | 200 |
| P44 | https://api.github.com/repos/kongbai9288/modmarket-backend/branches | BR05，只读 GET | 200 |
| P45 | https://api.github.com/repos/kongbai9288/modmarket-backend/contents/ | BR06，只读 GET | 200 |
| P46 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher | CG01-CG02 | 200 |
| P47 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher/license | CG03 | 200 |
| P48 | https://api.github.com/repos/copper-lamp/CopperGolemLauncher/contents/LICENSE | CG05-CG06 | 200 |
| P49 | https://api.github.com/repos/PrismLauncher/PrismLauncher/contents/CMakeLists.txt | PL04 | 200 |
| P50 | https://github.com/ViaVersion/ViaNBT | VN01-VN04 | 200 |
| P51 | https://awesome-dsh-plugin.com/p/chumoe/dsh-file-manager | DS02-DS04 | 200 |
| P52 | https://vxkex.com/ | VK01 | 200 |
| P53 | https://www.nihendiao.com/?p=4536/ | VK02 | 200 |

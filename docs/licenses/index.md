# 第三方许可证原文索引

检索日期：2026-11-05
更新轮次：011
来源接口：`GET https://api.github.com/repos/{owner}/{repo}/license`、`GET https://api.github.com/repos/{owner}/{repo}/contents/{path}`，全部返回 200。

## 逐字副本

| 文件 | 对应组件 | 许可证 | 字节 | SHA-1 前 16 | 来源 |
| --- | --- | --- | --- | --- | --- |
| HMCL-LICENSE.txt | HMCL-dev/HMCL | GPLv3 + Additional Terms 2 条 | 35507 | e58dbdf3bc2df8d7 | https://api.github.com/repos/HMCL-dev/HMCL/license |
| authlib-injector-AGPLv3-exception.txt | yushijinhun/authlib-injector | AGPLv3 + authlib-injector exception | 35009 | fa2b278a86803b82 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/AGPLv3-with-authlib-injector-exception.txt |
| CC-BY-SA-4.0.txt | authlib-injector wiki 文档 | CC BY-SA 4.0 | 20138 | b5235802028a1681 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/CC-BY-SA-4.0.txt |
| tao-LICENSE.txt | tauri-apps/tao | Apache-2.0 | 11323 | 3d9ca858ae047e05 | https://api.github.com/repos/tauri-apps/tao/license |
| egui-LICENSE.txt | emilk/egui | Apache-2.0 | 10850 | 5feaf15b3fa7d2d | https://api.github.com/repos/emilk/egui/license |
| slint-LICENSE.txt | slint-ui/slint 主文件 | 三许可清单 | 3759 | d3e9bcc7238fd90f | https://api.github.com/repos/slint-ui/slint/contents/LICENSE.md |
| iced-LICENSE.txt | iced-rs/iced | MIT | 1073 | 838038d9f1f56e6 | https://api.github.com/repos/iced-rs/iced/license |
| KCU-Launcher-LICENSE.txt | kongbai9288/KCU-Launcher | GPL-3.0 | 35149 | 31a3d460bb3c7d9 | https://api.github.com/repos/kongbai9288/KCU-Launcher/contents/LICENSE |
| MultiMC-COPYING.md | MultiMC/Launcher | NOASSERTION，含 Apache 2.0 部分 | 18664 | 59094e5b6f19f4c | https://api.github.com/repos/MultiMC/Launcher/contents/COPYING.md |
| Forge-LICENSE.txt | MinecraftForge/MinecraftForge | NOASSERTION，头部写 LGPL 2.1 | 27733 | 9b5ee64703a133b | https://api.github.com/repos/MinecraftForge/MinecraftForge/contents/LICENSE.txt |
| NeoForge-LICENSE.txt | neoforged/NeoForge | LGPL-2.1 | 24444 | 98e2b035a83f5f6 | https://api.github.com/repos/neoforged/NeoForge/contents/LICENSE.txt |
| Quilt-LICENSE.txt | QuiltMC/quilt-loader | Apache-2.0 | 11357 | 92170cdc034b2ff | https://api.github.com/repos/QuiltMC/quilt-loader/contents/LICENSE |
| CopperGolemLauncher-LICENSE | copper-lamp/CopperGolemLauncher | NOASSERTION，头部为 GNU General 条款 | 35834 | 97b9e831e4b309bd | https://api.github.com/repos/copper-lamp/CopperGolemLauncher/contents/LICENSE |

## slint 三许可全文

目录：`docs/licenses/slint-LICENSES/`。来源 https://api.github.com/repos/slint-ui/slint/contents/LICENSES ，该目录 20 个条目，本轮取得 3 份三许可全文。

| 文件 | 许可 | 字节 | SHA-1 前 16 | 来源 |
| --- | --- | --- | --- | --- |
| LicenseRef-Slint-Royalty-free-2.0.md | Royalty-free License 2.0 | 3620 | f611f298c4a28ad4 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES/LicenseRef-Slint-Royalty-free-2.0.md |
| GPL-3.0-only.txt | GNU GPLv3 | 34670 | e3bdbf20d43fc066 | https://api.github.com/repos/slint-ui/slint/contents/LICENSES/GPL-3.0-only.txt |
| LicenseRef-Slint-Software-3.0.md | Commercial license | 9187 | b535523cc612dafe | https://api.github.com/repos/slint-ui/slint/contents/LICENSES/LicenseRef-Slint-Software-3.0.md |

主文件原文：docs/licenses/slint-LICENSE.txt:17-22 写明三选一、Royalty-free 不含嵌入式、GPLv3 用于开源软件、嵌入式需商用许可。

## 重复副本处理

| 文件 | 处置 | 依据 |
| --- | --- | --- |
| slint-LICENSE.md | 010 轮误存，与 slint-LICENSE.txt 同字节同 SHA-1，已删除 | `sha1sum` 双文件一致 |
| PrismLauncher-LICENSE.txt | 与 KCU-Launcher-LICENSE.txt 同字节同 SHA-1，未另存副本 | https://api.github.com/repos/PrismLauncher/PrismLauncher/license 返回 GPL-3.0 |

## 许可证 endpoint 返回

| 仓库 | spdx_id | name | 轮次 |
| --- | --- | --- | --- |
| HMCL-dev/HMCL | null | LICENSE | 005 |
| tauri-apps/tao | null | LICENSE | 005 |
| emilk/egui | null | LICENSE-APACHE | 005 |
| slint-ui/slint | null | LICENSE.md | 005 |
| iced-rs/iced | null | LICENSE | 005 |
| kongbai9288/KCU-Launcher | GPL-3.0 | LICENSE | 010 |
| PrismLauncher/PrismLauncher | GPL-3.0 | LICENSE | 010 |
| MultiMC/Launcher | NOASSERTION | COPYING.md | 010 |
| MinecraftForge/MinecraftForge | NOASSERTION | LICENSE.txt | 010 |
| neoforged/NeoForge | LGPL-2.1 | LICENSE.txt | 010 |
| QuiltMC/quilt-loader | Apache-2.0 | LICENSE | 010 |

`GET /repos/HMCL-dev/HMCL` 返回 `license.spdx_id = GPL-3.0`。`/license` 端点因附加条款返回 null。

## 约束

| 编号 | 约束 |
| --- | --- |
| L01 | 本目录为第三方逐字副本，字节未改动。 |
| L02 | 本目录不构成本项目许可证声明；本项目 LICENSE 未生成。 |
| L03 | slint 三许可全文已取得，见上方 3 份文件；`LICENSES/` 其余 17 个条目未逐项取得。 |
| L04 | CC BY-SA 4.0 对应 wiki 文档，不对应 authlib-injector 代码。 |
| L05 | 商用、分发、改作列在 docs/research/09-licenses.md 登记，不在本目录推断。 |
| L06 | Forge / MultiMC 的 NOASSERTION 以文件头部为准，不以 SPDX 缺失推断无许可证。 |
| L07 | 服务条款与代码许可证分开登记，见 docs/research/12-compliance.md。 |
| L08 | CopperGolemLauncher 的 `THIRD_PARTY_NOTICES` 存在但未取得全文，复用范围未证实，见 docs/research/15-input-survey.md CG09。 |
| L09 | 插件独立许可证；插件加载后在开源许可页动态增加插件名、许可证、作者名、项目地址、修改后版本地址。 |

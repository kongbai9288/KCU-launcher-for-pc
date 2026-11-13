# 第三方软件声明

| 项 | 值 |
| --- | --- |
| 项目 | KCU Launcher for PC |
| 轮次 | 019 |
| 生成依据 | docs/licenses/index.md；assets/icons/lucide-manifest.json；docs/research/09-licenses.md；docs/research/12-compliance.md |
| 状态 | 演示层已使用 1 项；文档层逐字存档 13 组；进入 `src/` 构建的第三方代码 0 项 |
| 本项目 LICENSE | 未生成 |

本文件随发行物附带。应用内「关于 → 第三方许可」展示同一份清单，离线可读。清单按许可证分组渲染，插件加载后动态追加插件名、许可证、作者、项目地址、修改后版本地址。

## 一、演示层已使用

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 构建状态 |
| --- | --- | --- | --- | --- | --- | --- |
| Lucide | 图标子集 88 枚，取自 main 分支 | ISC License | Copyright (c) 2026 Lucide Icons and Contributors | 界面图标，内联 SVG sprite，无 CDN | https://lucide.dev/license ；https://github.com/lucide-icons/lucide | 演示层已使用；未进 `src/` |
| Feather 派生图标 | Lucide 中派生自 Feather 的部分 | MIT License | Copyright (c) 2013-present Cole Bemis | 同上；派生清单见 lucide 官方许可页 | https://lucide.dev/license | 演示层已使用；未进 `src/` |

Lucide ISC 原文：

> Permission to use, copy, modify, and/or distribute this software for any purpose with or without fee is hereby granted, provided that the above copyright notice and this permission notice appear in all copies.
> THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS.

MIT 原文对应段落见 https://lucide.dev/license 的 Feather 派生列表；88 枚图标的逐枚来源与 blob SHA 记录在 `assets/icons/lucide-manifest.json`，SVG 子集在 `assets/icons/lucide-subset.svg`。图标遵循 Lucide SVG 约定：24×24 viewBox、`fill="none"`、`stroke="currentColor"`、`stroke-width=2`、圆角端点与拐角，无 transform / filter / 显式描边色。

## 二、文档层逐字存档，未复制代码

| 项目 | 许可证 | 逐字副本 | 用途 |
| --- | --- | --- | --- |
| HMCL-dev/HMCL | GPLv3 + Additional Terms 2 条 | docs/licenses/HMCL-LICENSE.txt | 启动器行为调研 |
| kongbai9288/KCU-Launcher | GPL-3.0 | docs/licenses/KCU-Launcher-LICENSE.txt | 项目谱系调研 |
| PrismLauncher/PrismLauncher | GPL-3.0（与上一行同字节同 SHA-1） | 未另存副本 | 许可证核对 |
| yushijinhun/authlib-injector | AGPLv3 + authlib-injector exception | docs/licenses/authlib-injector-AGPLv3-exception.txt | 第三方登录调研 |
| authlib-injector wiki | CC BY-SA 4.0 | docs/licenses/CC-BY-SA-4.0.txt | 文档调研；不对应代码 |
| tauri-apps/tao | Apache-2.0 | docs/licenses/tao-LICENSE.txt | 窗口方案候选 |
| emilk/egui | Apache-2.0 | docs/licenses/egui-LICENSE.txt | UI 方案候选 |
| iced-rs/iced | MIT | docs/licenses/iced-LICENSE.txt | UI 方案候选 |
| slint-ui/slint | 三许可（Royalty-free 2.0 / GPL-3.0-only / Commercial 3.0） | docs/licenses/slint-LICENSE.txt、docs/licenses/slint-LICENSES/ | UI 方案候选 |
| MultiMC/Launcher | NOASSERTION（含 Apache 2.0 部分，以文件头为准） | docs/licenses/MultiMC-COPYING.md | 启动器方案候选 |
| MinecraftForge/MinecraftForge | NOASSERTION（头部 LGPL 2.1） | docs/licenses/Forge-LICENSE.txt | 加载器调研 |
| neoforged/NeoForge | LGPL-2.1 | docs/licenses/NeoForge-LICENSE.txt | 加载器调研 |
| QuiltMC/quilt-loader | Apache-2.0 | docs/licenses/Quilt-LICENSE.txt | 加载器调研 |
| copper-lamp/CopperGolemLauncher | NOASSERTION（头部 GNU General 条款） | docs/licenses/CopperGolemLauncher-LICENSE | 候选；复用范围未证实 |

## 三、服务条款与代码许可证分开

| 服务 | 状态 |
| --- | --- |
| CurseForge 第三方 API 条款 | X01–X04 未拍板，见 docs/research/12-compliance.md |
| Modrinth 条款 | 4 条 API License 原文已取得 |
| MCIM / BMCLAPI / mclo.gs / Hangar / Ore / SpigotMC | 条款未证实 |

服务条款约束不因取得代码 LICENSE 而默认放行。

## 四、约束

| 编号 | 内容 |
| --- | --- |
| N01 | 未取得 LICENSE 全文前不复制对应组件代码、资源、商标、Client ID。 |
| N02 | NOASSERTION 以文件头部为准，不推断为无许可证。 |
| N03 | 清单随依赖变化刷新；强制刷新重新扫描依赖树；显示清单生成时间。 |
| N04 | 插件独立许可证；插件加载后在关于页动态增加插件名、许可证、作者名、项目地址、修改后版本地址。 |
| N05 | 某条全文缺失给来源链接与「稍后」，不编造许可文本。 |
| N06 | 进入 `src/` 的第三方代码为 0；清单中「已使用」仅限演示层图标。 |

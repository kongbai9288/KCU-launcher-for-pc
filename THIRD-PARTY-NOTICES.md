# 第三方软件声明

| 项 | 值 |
| --- | --- |
| 项目 | KCU Launcher for PC |
| 轮次 | 019；020 增补上层候选 |
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

## 五、上层实现候选（020，未进入构建）

用户批准上层实现采用第三方代码。以下 12 组为候选，全部**未进入 `src/` 构建**；逐项取得 LICENSE 全文后才允许复制代码、资源、商标、Client ID。完整设计见 `docs/design/upper-layer-stack.md`，界面证据见 `demos/preview/37-upperstack.png`。

| 层 | 候选 | 许可证 | 用途 | 全文状态 | 复制状态 |
| --- | --- | --- | --- | --- | --- |
| UI 窗口 / WebView | tao + wry | Apache-2.0 / MIT | 桌面窗口与网页渲染 | 待逐项核对 | 候选 · 未进构建 |
| UI 方案备选 | slint | 三许可（Royalty-free / GPLv3 / Commercial） | 声明式界面 | 三许可全文已取得 | 候选 · 未进构建 |
| UI 方案备选 | egui / iced | Apache-2.0 / MIT | 即时模式界面 | 待逐项核对 | 候选 · 未进构建 |
| 序列化 | serde + serde_json | MIT OR Apache-2.0 | 配置 / 清单 / 统一信封 | 待逐项核对 | 候选 · 未进构建 |
| 网络 | reqwest | MIT OR Apache-2.0 | 批量请求 / 单飞 / 竞速 | 待逐项核对 | 候选 · 未进构建 |
| 异步 | tokio | MIT | 任务调度与取消 | 待逐项核对 | 候选 · 未进构建 |
| 版本比较 | semver | MIT OR Apache-2.0 | 插件化更新版本判定 | 待逐项核对 | 候选 · 未进构建 |
| 哈希 / 校验 | sha2 | MIT OR Apache-2.0 | 文件与插件摘要 | 待逐项核对 | 候选 · 未进构建 |
| 错误 | anyhow + thiserror | MIT OR Apache-2.0 | 错误链 | 待逐项核对 | 候选 · 未进构建 |
| 插件加载 | libloading | ISC | 动态库加载（C ABI） | 待逐项核对 | 候选 · 未进构建 |
| 更新 | tauri-plugin-updater / self_update | Apache-2.0 / MIT | 签名校验与回滚 | 待逐项核对 | 候选 · 未进构建 |
| 本地存储 | rusqlite | MIT | 索引与状态缓存 | 待逐项核对 | 候选 · 未进构建 |

许可证来源：crates.io 元数据页、第三方项目 THIRD_PARTY_NOTICES 声明、docs/licenses/ 逐字副本。docs/licenses/ 已有 tao、egui、iced、slint 主文件与 slint 三许可全文；其余条目未逐仓库取得全文，标未证实。发布构建以当前 Cargo.lock 与各 crate 自带许可证文件为最终依据。

| 编号 | 约束 |
| --- | --- |
| N07 | 上层候选逐项取得 LICENSE 全文后才允许复制；取得前只登记，不引入依赖。 |
| N08 | 每项进关于页七列表与本文件：项目名、版本、许可证、版权、用途、来源、是否进入构建。 |
| N09 | NOASSERTION 以文件头部为准；GPL / LGPL / 三许可分别判定；服务条款与代码许可证分开。 |
| N10 | 插件加载后动态追加插件名、许可证、作者、项目地址、修改后版本地址。 |

## 023 新增候选（i18n 与崩溃分析）

| 层 | 候选 | 许可证 | 用途 | 全文状态 | 复制状态 |
| --- | --- | --- | --- | --- | --- |
| 界面文案 | fluent（Project Fluent） | Apache-2.0 OR MIT | `.ftl` 运行时解析与格式化 | 待逐项核对 | 候选 · 未进构建 |
| 语言装载 | i18n-embed | MIT | 资源嵌入、系统语言探测、`fl!()` key 检查 | 待逐项核对 | 候选 · 未进构建 |
| 崩溃捕获 | sentry-minidump | MIT | 独立进程写 minidump | 待逐项核对 | 候选 · 未进构建 |
| 本地解析 | minidump | MIT | 本地读 dump 与出栈 | 待逐项核对 | 候选 · 未进构建 |
| 崩溃后端 | Breakpad | BSD-3-Clause | native crash 后端之一 | 待逐项核对 | 候选 · 未进构建 |
| 崩溃封装 | sentry-native | MIT | Breakpad / Crashpad 后端封装 | 待逐项核对 | 候选 · 未进构建 |

服务端边界：Sentry Web 应用为 FSL-1.1-Apache-2.0（非 OSI 认证开源，两年后转 Apache-2.0），项目只接 MIT 许可的 SDK，不把服务端打包进发行物；自托管由用户自行部署。

| 编号 | 约束 |
| --- | --- |
| N11 | 上述 6 组与既有 12 组一致：LICENSE 全文取得并写进关于页后才允许加进 Cargo.toml。 |
| N12 | 插件加载后动态追加其语言包与崩溃扩展的许可信息。 |
| N13 | 服务条款、代码许可证、服务端许可三者分开登记，不因拿到 LICENSE 就默认放行。 |

## 025 已进构建依赖（非候选）

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| serde_json | 1.0.145 | MIT OR Apache-2.0 | Erick Tryzelaar, David Tolnay | 任务 JSON 解析 | vendor/serde_json | 构建中已使用 |
| serde_core | 1.0.228 | MIT OR Apache-2.0 | serde-rs | serde_json 依赖 | vendor/serde_core | 构建中已使用 |
| itoa | 1.0.15 | MIT OR Apache-2.0 | David Tolnay | 整数格式化 | vendor/itoa | 构建中已使用 |
| ryu | 1.0.20 | Apache-2.0 OR BSL-1.0 | David Tolnay | 浮点格式化 | vendor/ryu | 构建中已使用 |
| memchr | 2.7.6 | Unlicense OR MIT | Andrew Gallant | 字节搜索 | vendor/memchr | 构建中已使用 |

许可证全文：`docs/licenses/serde_json-LICENSE-{MIT,APACHE}.txt`、`serde_core-LICENSE-{MIT,APACHE}.txt`、`itoa-LICENSE-{MIT,APACHE}.txt`、`ryu-LICENSE-{APACHE,BOOST}.txt`、`memchr-LICENSE-MIT.txt`。

| 编号 | 约束 |
| --- | --- |
| N14 | memchr 的 license 字段为 `Unlicense OR MIT`，上游仓库只提供 LICENSE-MIT 文件；本项目按 MIT 条款使用，Unlicense 全文未单独取得，如实登记。 |
| N15 | ryu 为 `Apache-2.0 OR BSL-1.0`，两份全文均已落盘，按 Apache-2.0 条款使用。 |
| N16 | vendor 内上游 `src/` 原样保留；manifest 仅删 dev / 恒假 cfg 段，改动可 diff 审计。 |
| N17 | 后续每引入一个库，重复 H02 四步：LICENSE 全文 → 关于页 → 本文件 → Cargo.toml。 |

## 027 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| crossbeam-channel | 0.5.17 | MIT OR Apache-2.0 | crossbeam-rs | 多源竞速结果通道 | vendor/crossbeam-channel | 构建中已使用 |
| crossbeam-utils | 0.8.23 | MIT OR Apache-2.0 | crossbeam-rs | 线程组与活跃归零 | vendor/crossbeam-utils | 构建中已使用 |

许可证全文：`docs/licenses/crossbeam-channel-LICENSE-{MIT,APACHE}.txt`、`crossbeam-utils-LICENSE-{MIT,APACHE}.txt`。

| 编号 | 约束 |
| --- | --- |
| N18 | crossbeam 为 mono-repo，crate 子目录的 `no_atomic.rs` / `build-common.rs` 原本是指向仓库根的软链；vendor 时改为真实文件副本，上游 `src/` 未改。 |
| N19 | 按 MIT 条款使用，Apache-2.0 全文同时随附。 |

## 029 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| lru | 0.12.5 | MIT | Jerome Froelich (c) 2016 | 有界 LRU 容量与淘汰 | vendor/lru | 构建中已使用 |

许可证全文：`docs/licenses/lru-LICENSE.txt`。

| 编号 | 约束 |
| --- | --- |
| N20 | 以 `default-features = false` 使用，避免引入 hashbrown；上游 `src/` 未改，manifest 裁掉 optional 依赖与 dev-deps 仅用于目录源构建。 |
| N21 | MIT 条款要求保留版权与许可声明，全文随发行物附上。 |

## 030 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| lexopt | 0.3.2 | MIT | Jan Verbeek (c) 2021 | 命令行参数解析 | vendor/lexopt | 构建中已使用 |

许可证全文：`docs/licenses/lexopt-LICENSE.txt`。

| 编号 | 约束 |
| --- | --- |
| N22 | 上游 tarball 的 `[profile.test]` 段对依赖无效，裁掉以免本地目录源解析告警；`src/lib.rs` 未改。 |
| N23 | MIT 条款要求保留版权与许可声明，全文随发行物附上。 |

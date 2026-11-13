# 上层实现第三方候选清单

| 项 | 值 |
| --- | --- |
| 轮次 | 020 |
| 状态 | 已批准采用第三方代码；候选清单未进入构建 |
| 依据 | 020 指令「上层的实现都用别人的代码，就行了」；013 轮「因为我对你的没有信心」 |
| 登记 | 关于页七列表、THIRD-PARTY-NOTICES.md、`37-upperstack.png` |

## 候选清单（12 组）

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

许可证来源：crates.io 元数据页、第三方项目 THIRD_PARTY_NOTICES 声明、docs/licenses/ 逐字副本。`docs/licenses/` 已有 tao、egui、iced、slint 主文件与三许可全文；其余条目本轮未逐仓库取得全文，标未证实。

## 复用规则

| 编号 | 规则 |
| --- | --- |
| U01 | 逐项取得 LICENSE 全文后才允许复制代码、资源、商标、Client ID。 |
| U02 | 每项进关于页七列表与 THIRD-PARTY-NOTICES.md：项目名、版本、许可证、版权、用途、来源、是否进入构建。 |
| U03 | NOASSERTION 以文件头部为准，不推断为无许可证。 |
| U04 | GPL / LGPL / 三许可分别判定，不默认放行；服务条款与代码许可证分开。 |
| U05 | 插件加载后动态追加插件名、许可证、作者、项目地址、修改后版本地址。 |
| U06 | 全文缺失给来源链接与「稍后」，不编造许可文本。 |
| U07 | 发布构建以当前 Cargo.lock 与各 crate 自带许可证文件为最终依据。 |
| U08 | 轻量模式不加载 WebView2 重资产，上层 UI 候选只服务 normal。 |

## 与既有已用组件的区别

| 类别 | 内容 | 状态 |
| --- | --- | --- |
| 演示层已使用 | Lucide 88 枚图标（ISC + Feather 派生 MIT） | 已证实 |
| 文档层逐字存档 | 13 组启动器 / 加载器 / UI 项目许可证 | 已证实 |
| 上层实现候选 | 12 组 Rust 生态库 | 未证实 / 候选 |
| 进入 `src/` 构建 | 0 项 | 已证实 |

## 边界

| 项 | 值 |
| --- | --- |
| 已落地 | 关于页候选表、`37-upperstack.png`、本清单、NOTICES 追加段 |
| 未落地 | 依赖引入、Cargo.toml 变更、许可证全文逐项取得 |
| `src/` / Cargo.lock | 020 轮无变化 |

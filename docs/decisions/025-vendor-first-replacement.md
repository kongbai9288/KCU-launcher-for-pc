# 第 025 轮：第一次真正把自写代码换成别人的代码

| 项 | 值 |
| --- | --- |
| 编号 | 025 |
| 状态 | 已实现、已验证 |
| 依据 | docs/spec/25-round-025-instructions.txt；024 撤回自我授权；用户「对你的代码没有任何信心」 |
| 前序 | docs/records/code-ownership-audit.md 的逐文件替换映射 |
| 本轮性质 | 工程轮；无新演示 HTML、无自评打分、输出收敛 |

## 做了什么

| 编号 | 动作 |
| --- | --- |
| D01 | 删除 `src/dispatcher/json.rs` 里 336 行手写递归下降 JSON 解析器，替换为 `serde_json::Value` 的类型别名 + 3 行 `parse()` + 一个 5 行 `StringField` trait。 |
| D02 | 主 `Cargo.toml` 首次出现 `[dependencies]`；`Cargo.lock` 从 1 个包变为 6 个包，其中 **5 个是真实第三方 crate**。 |
| D03 | 上游源码通过 codeload / api.github.com 打包下载，原样放进 `vendor/`，`.cargo/config.toml` 做 source replacement，`cargo build --offline` 与 `cargo test --offline` 真实通过。 |
| D04 | 9 份许可证全文落 `docs/licenses/`，关于页七列表追加 5 组「构建中已使用」，`THIRD-PARTY-NOTICES.md` 同步登记。 |
| D05 | 行为差异如实登记：深度上限由手写 64 变为 serde_json 默认 128。 |

## 通道实测

| 端点 | 结果 |
| --- | --- |
| `mirrors.cloud.tencent.com/crates.io-index/config.json` | 404 |
| `rsproxy.cn/index/config.json` | 403 |
| `index.crates.io/config.json` | 403 |
| `static.crates.io/...crate` | 403 |
| `mirrors.huaweicloud.com/repository/rust/crates-io/config.json` | 403 `policy_default_denied` |
| `mirrors.tuna.tsinghua.edu.cn/crates.io-index/config.json` | 403 |
| `mirrors.aliyun.com/crates.io-index/config.json` | 403 |
| `mirrors.cloud.tencent.com/rustup/dist/...` | 200（工具链通道，与 crates 无关） |
| `api.github.com/repos/serde-rs/json/tarball/v1.0.145` | 200 |
| `codeload.github.com/serde-rs/json/tar.gz/refs/tags/v1.0.145` | 200 |

registry 通道全部被挡，GitHub 源码打包通道可用。用户此前确认「腾讯的镜像下载或 api.github 工具流 100% 可用」，实测结论与之一致：工具链走腾讯镜像，crate 源码走 GitHub 打包。

## vendor 内容

| 目录 | 版本 | license 字段 | 来源 |
| --- | --- | --- | --- |
| `vendor/serde_json` | 1.0.145 | MIT OR Apache-2.0 | serde-rs/json tag v1.0.145 |
| `vendor/serde_core` | 1.0.228 | MIT OR Apache-2.0 | serde-rs/serde tag v1.0.228 的 `serde_core/` 子目录 |
| `vendor/itoa` | 1.0.15 | MIT OR Apache-2.0 | dtolnay/itoa tag 1.0.15 |
| `vendor/ryu` | 1.0.20 | Apache-2.0 OR BSL-1.0 | dtolnay/ryu tag 1.0.20 |
| `vendor/memchr` | 2.7.6 | Unlicense OR MIT | BurntSushi/memchr tag 2.7.6 |

| 编号 | 对上游 manifest 的最小改动 | 原因 |
| --- | --- | --- |
| M01 | 删除 `[dev-dependencies]` 段 | 段内引用 `../serde`、`serde_derive`、`serde_bytes`、`serde_stacker` 等未 vendor 的 path / registry 包；只影响上游自身测试，不影响产品构建 |
| M02 | 删除 `[target.'cfg(any())'.dependencies]` 段 | 该 cfg 恒假，仅用于上游锁版本对齐；段内 `serde` 未 vendor |
| M03 | 每个目录写 `.cargo-checksum.json` = `{"files":{},"package":null}` | cargo vendor 目录源的必需元数据 |
| M04 | 裁剪 `testdata/`、`benches/`、`examples/`、CI 配置 | 仓库体积控制；产品 `src/` 与 `Cargo.toml`、`build.rs`、LICENSE 全部保留 |

上游 `src/` 未改动一行。改动只落在 manifest 的 dev / 恒假 cfg 段，可逐文件 diff 审计。

## 数字变化

| 项 | 024 | 025 |
| --- | --- | --- |
| `Cargo.lock` 包数 | 1 | 6（5 个第三方） |
| `Cargo.toml [dependencies]` | 无 | `serde_json` |
| `src/dispatcher/json.rs` | 336 行 | 77 行（产品代码约 20 行，其余为回归测试） |
| `src/` 总行数 | 4339 | 4081 |
| `src/` 有效代码行 | 3876 | 3636 |
| `cargo test --offline` | 141 / 0 | 141 / 0 |
| 关于页「构建中已使用」组数 | 0 | 5 |

## 行为差异（如实登记）

| 编号 | 项 | 手写实现 | serde_json |
| --- | --- | --- | --- |
| B01 | 嵌套深度上限 | 64 | 默认 128，超过报 recursion limit exceeded |
| B02 | 数字表示 | `f64` | `Number`（整数保留精确值） |
| B03 | 对象键顺序 | BTreeMap 有序 | 默认 Map 为 BTreeMap，同样有序（未启用 `preserve_order`） |
| B04 | 尾随内容 / 前导零 / 控制字符 | 手写拒绝 | 库拒绝 |

`rejects_excessive_depth` 测试由 80 层改为 200 层，并在 `docs/verification/round-025.md` 记录原因；没有悄悄降低验收项，断言仍是「超限被拒」。

## 还没换的（不假装做完）

| 文件 | 行数 | 状态 |
| --- | --- | --- |
| `src/core/cache.rs` | 304 | 仍自写 |
| `src/core/asynk.rs` | 258 | 仍自写 |
| `src/core/leak.rs` | 191 | 仍自写 |
| `src/dispatcher/launcher.rs` | 541 | 仍自写 |
| `src/lightweight/*.rs` | 1135 | 仍自写 |
| 其余 core 模块 | 约 1200 | 仍自写 |

本轮只落地替换映射的第一块。剩余块按 `docs/records/code-ownership-audit.md` 逐模块推进，每换一块重跑一次集成测试。

## 硬规则

| 编号 | 内容 |
| --- | --- |
| H01 | vendor 目录内上游 `src/` 保持原样；任何修改走 `[patch]` 或换版本，不改上游代码。 |
| H02 | 新依赖需：LICENSE 全文 → 关于页七列表 → `THIRD-PARTY-NOTICES.md` → 加进 `Cargo.toml`，四步齐备。 |
| H03 | `.cargo/config.toml` 固定 offline + 目录源，构建不依赖 registry 可达性。 |
| H04 | 测试仅作回归，不作为质量结论（024 W03 延续）。 |
| H05 | 后端仓 0 写请求；凭据只从环境变量读；诊断包不进公仓。 |

## 四值

| 项 | 值 |
| --- | --- |
| registry 端点全部 403 / 404、GitHub 打包 200 | 已证实 |
| `cargo build --offline` / `cargo test --offline` 通过、Cargo.lock 5 个第三方包 | 已证实 |
| 9 份许可全文落盘、关于页 5 组已进构建登记 | 已证实 |
| 手写 JSON 解析器删除、深度上限变化 | 已证实 |
| 剩余自写模块替换后行数、真实网络 / UI / 跨平台行为 | 未证实 |
| 浏览器内点击、Win7 构建、CI 独立构建 | 受阻 |

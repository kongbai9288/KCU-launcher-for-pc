# 第 013 轮开工决策与工具链纠正

轮次：013
状态：已批准（用户当轮明确指令）
依据：docs/spec/13-round-013-instructions.txt、docs/spec/13-round-013-instructions-part2.txt、docs/records/round-013-answers.md

## 阶段判定

| 编号 | 项 | 012 值 | 013 值 |
| --- | --- | --- | --- |
| D01 | 时间 | 明天答复 | 用户声明「现在都是你所说的明天了」 |
| D02 | 新功能 | 未提供 | 用户声明「目前我没有想到新的功能理论上应该不会有」 |
| D03 | D06 | 未触发 | **已触发** |
| D04 | 005-blueprint.md | 未批准 | **已批准** |
| D05 | D07 逐层搭建 | 未启动 | **已启用**，本轮落 core 层 |
| D06 | Q-H01 至 Q-H06 | 未满足 | 已满足到可开工层；未答复细节按 013-answers.md L 组与 G 组默认落地 |
| D07 | src/ | 空 | core 层已落地，`cargo build` / `cargo test` 实测 |
| D08 | 阶段 | 003-remote.md D05 功能输入 | D07 逐层搭建第一层 |

## 工具链纠正（用户 F73 要求「如果我有理解错误那么你就纠正官方源」）

| 编号 | 用户表述 | 实测 | 纠正 |
| --- | --- | --- | --- |
| C01 | 通过 GitHub 行动拉对应的东西 | GitHub Actions 是 CI 服务，不向本地沙盒分发可执行工具链 | 不适用于「在当前环境装 rustc / cargo」 |
| C02 | 官方源 | `https://static.rust-lang.org/dist/channel-rust-stable.toml` → 403 | Rust 官方工具链分发主机在本环境不可达，不是 API 调用能绕过 |
| C03 | api.github.com 获取一个 | `https://api.github.com/repos/rust-lang/rust/releases/latest` → 200 | 只能取 release 元数据；rustc / cargo / std 二进制不在 GitHub Releases 资产里 |
| C04 | 腾讯镜像下载 | `https://mirrors.cloud.tencent.com/rustup/dist/channel-rust-stable.toml` → 200；`rustup-init` → 200 | **本轮实际成功路径**，用户判断成立 |
| C05 | 落地命令 | `RUSTUP_DIST_SERVER=https://mirrors.cloud.tencent.com/rustup`、`RUSTUP_UPDATE_ROOT=https://mirrors.cloud.tencent.com/rustup/rustup`、rustup-init `--profile minimal --default-toolchain stable` | rustc 1.99.1、cargo 1.99.1 已装，`CARGO_HOME` / `RUSTUP_HOME` 置于仓库外 |

结论：用户「腾讯镜像可用」成立且已验证；「GitHub 行动拉工具链」在本场景不成立，已按 C01-C03 纠正，不据此伪造 CI 结果。`api.github.com` 继续用于 release 元数据与远端推送。

## 平台落定

| 编号 | 项 | 值 | 片段 |
| --- | --- | --- | --- |
| P01 | Win7 路径 | Tier 3 + build-std | F64 |
| P02 | 多架构 | i686 / x86_64 / aarch64 全选 | F65 |
| P03 | Win7 下 ARM64 | 放弃 | F66 |
| P04 | 地域口径 | 物理位置 + 区域设置，软策略 | F67、F52、F53 |
| P05 | 地域用途 | 只用于下载选择；不与「特定地区禁止下载」复用 | F52、F53 |
| P06 | 工具链 | rustc / cargo stable 1.99.1 | F70、F24 |
| P07 | 推送 | PAT 允许；git HTTP 受阻时走 REST Git Data API | F72 |
| P08 | KB2533623 / GetProcAddress | 纳入构建约束 | F69 |

## G 组默认（用户 F74 授权自行判定）

| 编号 | 011 遗留 | 013 默认 |
| --- | --- | --- |
| G01 | Notchian 离线 UUID 行为 | 不写进实现；沿用 02-auth.md 禁用约束 |
| G02 | Mojang 官方 RCON 文档 | 沿用 06-server.md 已证实一手原文，不补编 |
| G03 | 加载器逐版本 schema | 不写进实现；仅保留端点配置项 |
| G04 | 令牌保护、Azure Client ID | F012 方案未写入本层；不内嵌任何 ID |
| G05 | CREATE_NO_WINDOW / std 超时 / WebView2 内存 / 单文件发布 / 多操作入口 | 按用户逻辑落地，不写死未证实值 |
| G06 | 文件管理开源骨干 | 未选定，不引入 |
| G07 | viaNBT 集成 | 改 Rust 侧实现（F23），本层不引入依赖 |
| G08 / G09 | VxKex | 兼容范围与分发不写进本层 |
| G10 / G11 | 陶瓦联机 / atomgit / viaNBT LICENSE | 不写进本层 |
| G12 | 008 报告 U8 锚点误差 | 保留待复核，不代改报告 |
| G13 | v99.99 tag | 已失败，不当版本号 |
| G14 | 本地/远端链哈希不同 | 内容等价，沿用 API 快照 |

## H 组硬要求

| 编号 | 要求 | 落地 | 验证 |
| --- | --- | --- | --- |
| H01 | 验证用户正常操作逻辑 | src/core/userflow.rs `simulate` | `cargo test` 用例 |
| H02 | 模拟用户操作 | `FlowTrace.steps` 逐步输出 | `test_flow_trace_covers_all_steps` |
| H03 | 每个弹窗有关闭逻辑 | src/core/popup.rs `Dialog::close`、`DialogRegistry::assert_all_closable` | `test_every_dialog_can_close` |
| H04 | 指定参数加入服务器 | src/core/args.rs `join_server_directly` | `test_arg_joins_server_directly` |
| H05 | 双击服务器按权重选符合版本实例，用户权重第一 | src/core/instance.rs `select_instance` | `test_double_click_*`、`test_user_choice_ranks_first` |
| H06 | 操作顺畅、不残留弹窗 | `FlowState::open_dialogs` 收敛 | `test_no_open_dialog_after_flow` |

## 本轮边界

| 项 | 值 |
| --- | --- |
| 落地层 | D07 第 1 层 core（B03：envelope、paths、log、config、diagnostics、args、popup、instance、userflow） |
| 未落地层 | dispatcher、lightweight、headless、normal、ui、server、lan、build、部署 |
| CF 下载模块 | 不触碰；X01-X04 不影响本层；CF API 方法等用户完成时给（F17） |
| 特殊版私仓 | 先创建、用户同意后再放代码（F63） |
| 正常模式 UI | 品牌替换已批准，实现未进入本层 |
| 外部依赖 | 0；离线可编译 |

## 代码注释约束

只写技术不变量与边界，不写功能目的说明。见 docs/spec/00-requirements.txt 与用户 013 轮前序指令。

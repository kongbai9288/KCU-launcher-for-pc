# 第 011 轮功能输入决策记录

轮次：011
状态：已批准（用户当轮明确指令）；实现、验证、合并、构建、部署、行为确认均未达到
依据：docs/spec/11-round-011-instructions.txt、docs/spec/11-features-input.txt、docs/spec/00-requirements.txt:18.5、:249

| 编号 | 决定了什么 | 约束 | 验证条件 |
| --- | --- | --- | --- |
| D01 | 后端仓只读 | 只发 `GET`；不写、不 fork、不改分支、不建 issue、不触发自动部署；内容不进公仓 | 每轮核对请求方法；docs/research/15-input-survey.md BR02 |
| D02 | CF API 凭据不进入本公仓 | 用户当轮未提供该凭据值；仅给出处置方向 | docs/spec/11-features-input.txt 开头段 |
| D03 | 特殊版单开私仓构建 | 触发条件：所有任务完成，且反复检查未发现漏洞；仅用户与朋友使用；正常版本不含该凭据 | docs/decisions/003-remote.md D05-D06；用户当轮输入 |
| D04 | 正常版本走镜像或用户后端 | 用户后端仅境外场景可连；镜像优先于用户后端 | docs/spec/11-features-input.txt 第 55 条 |
| D05 | 010 轮 X01-X04 状态 | 密钥共享方向已由 D02/D03 给出；CF03 缓存字段、CF02 代理路径、CF01 唯一 Key 归属仍未逐条拍板 | docs/research/12-compliance.md X01-X04；docs/rules/build-preconditions.md |
| D06 | 离线账户地域限制 | 不使用网络探测手段；物理位置与区域设置的语义差已登记 | docs/research/13-platform-api.md P01-P07 |
| D07 | 境外限制的正版例外与中国大陆恢复 | 正版登录后放行；位于中国大陆地区功能恢复正常 | docs/spec/11-features-input.txt 开头段 |
| D08 | Win7 默认进入轻量模式 | 与需求 :8 的 2GB 首次默认并列登记；统一调度器声明页使用用户指定文案 | docs/research/13-platform-api.md C05-C06 |
| D09 | Win7 兼容与 Rust 官方目标冲突 | Tier 1 Windows 目标最低 Win10；Win7 仅 Tier 3 且需自建 std；ARM64 与 Win7 交集为空 | docs/research/13-platform-api.md C01-C04 |
| D10 | 多架构候选 | `i686` / `x86_64` / `aarch64` 为候选；不写死目标三元组 | docs/research/13-platform-api.md RW01-RW08 |
| D11 | 系统 API 取值以一手原文为准 | 版本判定走 `versionhelpers.h`；不走 `GetVersionEx`；架构判定走 `GetNativeSystemInfo`；Win7 的 `SetDefaultDllDirectories` 需 KB2533623 与 `GetProcAddress` | docs/research/13-platform-api.md OS01-OS04、AR01-AR03、DL01-DL05 |
| D12 | 网络请求批量化 | 列表页一次请求取一页；详情走批量 ID 端点；逐条目单发请求列为禁止项；每页 20 条 | docs/research/14-batch-network.md N01-N08、M01-M07、C01-C05 |
| D13 | 本地 API 不暴露 | 绑定回环；服务器功能给 AI 用的 API 为用户当轮例外 | docs/research/14-batch-network.md L01-L04 |
| D14 | 配置集中 | API 基址、联网网址、端口、图标、语言包、保存路径不写死；按 OS 分类 | docs/research/14-batch-network.md K01-K09 |
| D15 | 插件体系 | 独立进程、独立许可证、模块化；加载后在开源许可页增加 5 个字段 | docs/research/15-input-survey.md OL01、OL06 |
| D16 | CopperGolemLauncher 插件 | 单开仓库、适配 UI、遵守许可证；本项目默认不内置；插件系统默认显示并引导下载；许可证全文已取得 | docs/research/15-input-survey.md CG01-CG10 |
| D17 | 项目许可证 | GPLv3；不同许可证用动态链接；源文件前加对应项目许可证头；拼接后做源与产物对比 | docs/research/15-input-survey.md OL03-OL05 |
| D18 | 统一调度器启动输入 | 内置 json 声明页：自动关闭功能声明、软件完整性验证、Win7 文案；语言包含文字 json 与字体 | docs/spec/11-features-input.txt 开头段 |
| D19 | 启动声明页细则 | 功能关闭声明从用户 github 或 atomgit 仓库拉取，带版本与平台信息；完整性验证失败声明软件可能被修改，离线不声明 | docs/spec/11-features-input.txt 开头段 |
| D20 | 文件扩展名修订 | `.kculf` 跳过 GUI 直接进 MC，需两天或拓展包解锁；无头模式用 `kculh`；覆盖需求 :17 的 `.kcul` | docs/spec/11-features-input.txt 第 34 条；18.5 |
| D21 | UI 约束 | 每个弹窗有关闭逻辑；非警告说明用圆圈 i 点击展开；分辨率自适应与溢出滚动；区间设置用无圆点线状滑动条；圆角扁平化；拖放安装显示拖放页；每个页面可扩展 | docs/spec/11-features-input.txt 开头段 |
| D22 | 复用优先 | 尽量使用开源代码拼接，不自写；许可证不明时按 18.6 停下 | docs/spec/11-features-input.txt 开头段；00-requirements.txt:31-32 |
| D23 | 阶段判定 | 仍为 003-remote.md D05 功能输入阶段；用户当轮写明「过一会我会把要求也给你」，D06 未触发 | docs/spec/11-features-input.txt 开头段 |
| D24 | 本轮不写源码 | `src/` 为空；不生成 Cargo.toml、build.rs、target spec、下载模块 | docs/rules/build-preconditions.md B01-B04 |

## 状态分层

| 层 | 值 |
| --- | --- |
| 已批准 | D01-D24 |
| 已实现 | 无 |
| 已验证 | 无 |
| 已合并 | 无 |
| 已进入构建 | 无 |
| 已部署 | 无 |
| 行为已确认 | 无 |

## 进入实现前需用户拍板的项

| 编号 | 项 | 来源 |
| --- | --- | --- |
| Q01 | C09 Win7 兼容路径：Tier 3 自建 std / VxKex / 旧版工具链 / 拆分产物 | docs/research/13-platform-api.md C01-C04 |
| Q02 | 多架构范围与 ARM64 取舍 | docs/research/13-platform-api.md C03-C04 |
| Q03 | 地域判定口径：物理位置或区域设置 | docs/research/13-platform-api.md P04-P07 |
| Q04 | CF03 / CF02 / CF01 逐条处置 | docs/research/12-compliance.md X01-X04 |
| Q05 | D06 触发信号与 005-blueprint.md 批准 | docs/decisions/003-remote.md D06、005-blueprint.md |
| Q06 | UI 设计稿品牌与字体授权 | docs/decisions/007-normal-ui.md |
| Q07 | 文件管理开源骨干项目选定 | docs/research/15-input-survey.md DS06 |
| Q08 | ViaNBT 与 Rust 的集成方式 | docs/research/15-input-survey.md VN05 |

## 偏离登记

| 规则 | 偏离 | 依据 |
| --- | --- | --- |
| :133 需求逐字保存 | 当轮指令副本剔除含凭据的整行 | 第 16 节不讨论项 + 18.5 |
| 9.1 连续未达应停下由用户决定范围 | 用户继续给功能输入，按当轮指令继续执行 | 18.5 |
| :8 首次默认轻量的 2GB 条件 | 新增 Win7 默认轻量 | 18.5 |
| :17 `.kcul` 无头扩展名 | 拆为 `.kculf` 与 `kculh` | 18.5 |

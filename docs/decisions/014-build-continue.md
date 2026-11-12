# 第 014 轮继续搭建决策

| 项 | 值 |
| --- | --- |
| 编号 | 014 |
| 状态 | 已批准 |
| 版本 | 0.0.0 |
| 轮次 | 014 |
| 逐字指令 | docs/spec/14-round-014-instructions.txt，1 行 410 字节，SHA-1 `8f72a8dae1e3e55903c3f1f620687216b6d79a02` |
| 前序阶段 | 013 轮 D06 已触发、D07 已启用、L1 core 9 模块 37 测试 |

## 本轮输入切分

| 片段 | 逐字 | 落定 |
| --- | --- | --- |
| F01 | 第1个你到时候在工作流设一个环境变量，我自己去填写就行 | D01 |
| F02 | 特殊版的话你自己去建立 | D02 |
| F03 | 品牌的话我本来这个也是给你打样板的 | D03 |
| F04 | 因为功能和这一个已经有好多区别了 | D03 |
| F05 | 你只要记住一点，就是让用户好受，非常舒服就行（这需要你有对功能的理解程度，自由发挥） | D03、D08 |
| F06 | 对了，缓存异步都要处理 | D04、D05 |
| F07 | 小心点内存泄露 | D06 |

## 决策

| 编号 | 项 | 值 | 依据 |
| --- | --- | --- | --- |
| D01 | CF API 凭据 | `.github/workflows/ci.yml` 设 `KCU_CF_API_KEY: ${{ secrets.KCU_CF_API_KEY }}` 占位；值由用户填写；仓库、注释、提交说明、日志零凭据 | F01、F17 |
| D02 | 特殊版私仓 | `kongbai9288/KCU-launcher-special`，private，main，HEAD `cd7fc97`；仅建仓 + README 占位；代码在用户同意后放入，用户手拉工具流 | F02、F63 |
| D03 | 正常模式 UI 稿 | `assets/ui/normal-mode-v3.html` 降级为样板与交互参考；不直接进入构建；KCU 品牌重新实现；E09「品牌与字体授权未取得」卡点关闭 | F03、F04、F05 |
| D04 | 缓存 | `.github/workflows/ci.yml` 用 `actions/cache@v4`，key 绑定 `Cargo.lock` 哈希；`src/core/cache.rs` 有界容量、TTL、单飞去重、order 去重 | F06 |
| D05 | 异步 | `src/core/asynk.rs` 线程组 + `mpsc::channel` + `CancelToken` + join 回收；CI 用 `concurrency.cancel-in-progress` 与并行 `core` / `scan` job；不引入 async runtime | F06、013-build-start.md C01-C05 |
| D06 | 内存泄漏防护 | `src/core/leak.rs` 活跃计数与弱引用注册表；`cache.inflight` 用 `Weak`；`TaskGroup::drop` 兜底 join；`order` 去重有界 | F07 |
| D07 | 阶段 | 仍为 D07 第 1 层 core 扩展；L2 dispatcher 及以下 8 层未启动 | 003-remote.md D07 |
| D08 | UX 验收 | 用户「让用户好受，非常舒服」拆为可测条目，见下表 | F05 |

## D08 可测条目

| 编号 | 条目 | 落点 | 验证 |
| --- | --- | --- | --- |
| U01 | 任意弹窗有且可枚举关闭路径 | core.popup catalog 11 类 | `cargo test --offline every_catalog_popup` |
| U02 | 流程结束不残留未关弹窗 | core.userflow FlowReport | `no_popup_is_left_open_after_any_path` |
| U03 | 双击服务器按权重选实例、用户指定排第一 | core.instance | `user_choice_ranks_first_in_flow` |
| U04 | 单参数直接进服 | core.args | `single_arg_bypasses_selection_and_joins_server` |
| U05 | 重复请求不重复加载 | core.cache 单飞 | `single_flight_loads_once_for_concurrent_waiters` |
| U06 | 多源下载一个完成即取消其余 | core.asynk race | `race_returns_first_and_cancels_other_sources` |
| U07 | 长任务可取消、可等待、无遗留线程 | core.asynk TaskGroup | `cancel_stops_worker`、`drop_joins_without_explicit_shutdown` |
| U08 | 缓存有界、过期重取、order 不膨胀 | core.cache | `capacity_bounds_entry_count`、`order_stays_bounded_after_many_inserts` |
| U09 | 对象释放后活跃计数归零 | core.leak | `tracked_releases_on_drop`、`weak_link_breaks_cycle_and_reaches_zero` |
| U10 | 低配不加载 normal.ui 资产 | 007-normal-ui.md D03-D05、lightweight 独立视图 | 013/014 决策一致 |

## 工具链与运行时口径

| 编号 | 项 | 值 |
| --- | --- | --- |
| T01 | 依赖 | std only，Cargo.lock 仅 `kcu-core` 一条 |
| T02 | 编译 | `cargo build --release --offline` 通过，rlib 610080 字节 |
| T03 | 测试 | `cargo test --offline` 56 passed / 0 failed / 0 ignored / 0 measured |
| T04 | 异步运行时 | 无 tokio / async-std；std 线程 + channel |
| T05 | 不引入运行时依据 | 离线可编译、Win7 Tier 3 + build-std、i686 / x86_64 / aarch64 全选、跨目标产物不叠加运行时内存占用 |
| T06 | CI 工具链 | `RUSTUP_DIST_SERVER` / `RUSTUP_UPDATE_ROOT` 指向腾讯 rustup 镜像，与 013 轮实测路径一致 |

## 端点与占位

| 环境变量 | 来源 | 值 |
| --- | --- | --- |
| `KCU_CF_API_KEY` | `secrets.KCU_CF_API_KEY` | 用户填写，仓库无字面量 |
| `KCU_MIRROR_BASE` | `vars.KCU_MIRROR_BASE` | 用户填写，不写死 |
| `KCU_BACKEND_BASE` | `vars.KCU_BACKEND_BASE` | 用户填写，不写死 |
| `KCU_LANG_PACK_BASE` | `vars.KCU_LANG_PACK_BASE` | 用户填写，不写死 |
| `KCU_DOWNLOAD_REGION` | `vars.KCU_DOWNLOAD_REGION` | 用户填写，仅用于下载源选择 |

`env-presence` 步骤只输出 present / absent，不输出值。

## 私仓事实

| 项 | 值 |
| --- | --- |
| 创建 API | `POST /user/repos`，`private: true`，响应 201 |
| README 初始化 | `PUT /contents/README.md`，201，`cd7fc97` |
| 可见性核对 | `private: true` |
| 代码 | 未放入 |
| 凭据 | 未放入 |
| 后端仓内容 | 未复制 |
| 用户后续动作 | 同意后放代码、手拉工具流、在 Secrets 填值 |

## 本轮边界

| 项 | 值 |
| --- | --- |
| 落地 | 3 个 core 模块、3 份功能 md、1 个 workflow、私仓建仓、索引与记录 |
| 未落地 | L2 dispatcher 及以下 8 层、UI 实现、CF 下载模块、特殊版代码、本地 LICENSE 文件 |
| 后端仓 | 0 个写请求 |
| 凭据 | 全仓零字面量，`.git/config` 干净 |

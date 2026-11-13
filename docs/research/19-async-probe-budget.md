# 异步探测、连接预算与背压调研

| 项 | 值 |
| --- | --- |
| 轮次 | 022 |
| 依据 | docs/spec/22-round-022-instructions.txt；021 服务器自动连接设计的补强 |
| 来源数 | 12 个完整 URL 锚点（3 份官方库文档 + 9 组公开资料 / 社区实现） |
| 范围 | 只补异步、并发上限、有界队列、失败历史分类；不改 021 的 servers.dat 与显示口径 |

## 一手来源

| 编号 | 来源 | 取到的事实 | 四值 |
| --- | --- | --- | --- |
| R01 | https://docs.rs/rust-mc-status/2.0.0/rust_mc_status/client/struct.McClient.html | `ping_many(&[ServerInfo])` 并行查询多台服务器，`with_max_parallel(5)` 控制并发上限，`with_timeout(5s)`；返回顺序与输入一致；DNS 与 SRV 缓存跨查询共享；**失败查询不阻塞其它查询**；文档明确「Use with_max_parallel() to control resource usage」 | 已证实（官方 Rust API 文档） |
| R02 | https://pkg.go.dev/github.com/LinusTebbe/mc-prober | 每次调用只做一次探测、库本身不带策略；调度、跨调用重试、滞后、指标、存储属于调用方；每次探测接 `context.Context`，deadline 包住整次交换（含所有读）；`WithMaxStatusSize 512 KiB`、`WithSkipFavicon`、`WithSkipPing` 等用于限资源；Prober 不可变且可并发使用 | 已证实（官方 Go 包文档） |
| R03 | https://deepwiki.com/mcobs/ObsMCLauncher/7.1-server-list-management | 第三方启动器 `ServerManager` 用 `TcpClient` 异步握手检查，`Task.WhenAny` + 5000ms 延迟做超时，失败返回 -1；`IsOnline` 是「上次 ping 的瞬时状态」、`LastPingTime` 记录上次成功查询；服务器列表加载 / 刷新时**并行**检查状态；配置整体序列化到 `config.json` | 已证实（社区实现镜像） |

## 公开资料

| 编号 | 来源 | 取到的事实 | 四值 |
| --- | --- | --- | --- |
| C01 | https://optimi.com/en/guides/dependency-resilience | 「A timeout is a capacity control」：无界等待占住 worker、连接、内存与请求槽；每个依赖客户端都要有最大并发数与**有界队列**，到顶后显式选排队带 deadline / 返回缓存 / 丢弃低优先级 / 快速失败；无界内部队列会把短暂上游变慢变成内存压力与长尾；bulkhead 按依赖隔离，别让一个慢依赖耗尽共享池 | 已证实（公开工程指南） |
| C02 | https://blog.habsi.net/backpressure-explained-designing-systems-that-dont-collapse-under-load/ | 每个队列、池、缓冲、并发操作都要有显式上限；要观测队列深度、在飞数、连接占用、超时率、拒绝率（看分位数不是均值）；超时是背压信号而不是单纯错误；反模式：无界内存队列、无限重试、共享线程池、扩容不缩池份额 | 已证实（公开工程指南） |
| C03 | https://async-concurrency.com/network-io-protocol-handling/connection-pooling-and-keepalive | 连接池是有界的；池耗尽时协程挂到 FIFO 等待队列而不是空转 CPU 或立刻报错；`unbounded gather` 一万个 URL 不会创建一万个连接，绝大多数会停在 connector waiter 上，但等待不可见，必须配显式 gate | 已证实（公开工程指南） |
| C04 | https://networkspy.app/blog/browser-connection-pool-limits-http1-http2 | HTTP/1.1 浏览器同域常见约 6 条并行连接，第 7 个请求会排队；好 API 行为包括「避免不必要的启动扇出、缓存稳定的启动数据、合并紧耦合读、延迟非关键调用」 | 已证实（公开资料，引用 MDN） |
| C05 | https://lanyiyun.blog.csdn.net/article/details/153921675 | HTTP/1.1 浏览器同域经验值 6–8 连接；HTTP/2 单连接多流（服务端常设 100–128）；连接总数受 FD / `ulimit -n` / `somaxconn` 等 OS 硬上限约束；连接数 ≠ 线程数 ≠ QPS，要分层看 | 已证实（公开资料） |
| C06 | https://juejin.cn/post/7704619107316367375 | 200 台设备用 40 路并发轮询；超时预算要分段，只设总超时是常见错误；队列必须有界，满了之后显式选阻塞 / 丢旧数据 / 落本地缓冲；服务自己要吐本轮耗时、成功数、各类超时数、队列深度 | 已证实（公开实践复盘） |
| C07 | https://dev.to/draginox/building-a-real-time-minecraft-server-monitor-with-nextjs-4e4j | 5000+ 服务器监控用 `BATCH_SIZE=400`、`CONCURRENT_PINGS=15`、`Promise.allSettled`（一台超时不毁整批）、5 秒超时；最坏情况 15 台 / 5 秒；多层缓存 TTL：`SERVER_PING 360s` 略长于探测周期 | 已证实（公开实现） |
| C08 | https://blog.filestack.com/?post_type=post&p=15850 | 浏览器批量任务 3–6 路并行是甜点，超过连接上限只会加不可见排队并饿死其它请求；给出 15 行 worker-pull 有界并发池：固定 N 个 worker 从队列取任务直到空，单个失败只记录不中止全部 | 已证实（公开实现） |
| C09 | https://dev.to/gitlab_3188/a-free-endpoint-isnt-slow-its-queued-a-littles-law-load-probe-37ac | 429 是背压信号不是加速信号；立即重试会造成 retry storm；Little's Law 定在飞预算 `MAX_IN_FLIGHT = ceil(target_rps * p95_seconds)`；要测出拐点而不是猜并发数 | 已证实（公开工程指南） |

## 对用户描述的逐条对照

| 用户原话 | 对应事实 | 本轮设计 |
| --- | --- | --- |
| 「注意异步啊」 | R01 `ping_many` 并行 + 失败不阻塞；R02 每次探测带 context deadline；R03 启动器并行检查状态；C08 worker-pull | 探测走异步队列，UI 先渲染上次结果再增量更新；取消后不再写新结果 |
| 「超出一定范围的也不会去连接了」 | C01 最大并发 + 有界队列；C03 池耗尽挂等待队列；C04 避免启动扇出；C05 OS 硬上限 | 按权重取前 N 台进入本次探测计划，范围外不发请求、保留上次结果 |
| 「新的不会受影响」 | C01 到顶后显式选策略；C07 批次化 | 新加服务器强制排到队首且不受 N 裁剪，但仍占同一份额度（挤掉权重最低的一台） |
| 「保持在设备连接的范围内防止设备爆炸」 | C01 超时是容量控制、bulkhead 隔离；C02 显式上限 + 观测；C05 FD / 队列硬上限；C06 有界队列；C09 在飞预算 | 设备档位表：标准 4 台 / 3 路、轻量 2 台 / 2 路、无界面 0；并发与总台数双上限；单台超时跳过；队列有界可停 |
| 「之前测过不可以用、而且没有成功连接案例的」 | R03 `IsOnline` 是瞬时状态、`LastPingTime` 是上次成功；R02 滞后 / 重试策略归调用方 | 把「瞬时失败」与「有没有成功案例」分开：有成功案例的继续参与后续探测；没有成功案例且测过的不主动重连 |
| 「那就会按照权重中去排序」 | C01 返回缓存结果是到顶后的合法降级；C07 多层缓存 | 这类服务器不沉底，用缓存权重排在中段（可用项之后、范围外之前、彻底失败之前） |

## 结论

| 编号 | 结论 | 依据 |
| --- | --- | --- |
| J01 | 探测必须异步、并发有上限、队列有界、单台有 deadline；不能对全部服务器一次性扇出 | R01 / R02 / C01 / C02 / C03 / C08 |
| J02 | 「范围」取设备档位给的总台数，按权重截取；范围外保留上次结果且不发请求 | C01 / C04 / C05 / C07 |
| J03 | 新加服务器不受裁剪，但整体探测总量仍卡在档位内，避免「加一台就多一路」把设备打满 | C01 / C06 / C09 |
| J04 | 轻量机器自动降档：更少的探测台数与更低的并发，呼应 007 D04 与 016 轻量极简视图 | C01 / C05 / 项目既有约束 |
| J05 | 失败历史分两类：`ever`（有成功案例）继续探测、本轮失败沉底；`never`（测过且无成功案例）不主动探测、按缓存权重排中段 | R02 / R03 / C01 |
| J06 | 锁定项始终置顶，且不因失败历史或范围裁剪改变位置 | 021 D05 / 022 指令 |
| J07 | 观测信号要有：本次可连、同时连接、在飞 / 队列、本次不连、上次同步时间、取消入口 | C02 / C06 |

## 口径说明（本轮自主拍板，待用户确认）

| 编号 | 项 | 我的理解 |
| --- | --- | --- |
| Q01 | 「超出一定范围」的单位 | 理解为「本次自动连接的总台数 + 同时连接路数」两个上限，不是地理范围、不是权重阈值。数值由设备档位给，用户可在设置里改。 |
| Q02 | 「新的不会受影响」 | 新加服务器一定立即连一次，不被 N 裁剪；但它占同一份额度，不额外扩总量。 |
| Q03 | 「按权重中去排序」 | 理解为「按缓存权重排在中段」，不沉底、不置顶、不反复探测。演示里落在可用项与彻底失败项之间。 |
| Q04 | 「防止设备爆炸」 | 内存 / 连接数 / 协程数都不随服务器总数线性增长；队列有界、取消后 0 个新请求。 |

以上四条不是用户逐字给定的规格，是设计决策；按 021 D01 只落 docs/，不写进产品界面文案。

## 约束

| 编号 | 内容 |
| --- | --- |
| S01 | 探测结果只能增量写入，UI 不能被同步等待阻塞；取消后不再写新结果、不再发新请求。 |
| S02 | 队列有界；到顶后排队带 deadline，不无限堆积、不立刻重试。 |
| S03 | 范围外与无成功记录的服务器仍留在列表里，不隐藏、不删除。 |
| S04 | 档位数值（4/3、2/2）是项目自定，不是官方文档值；C04 / C05 的 3–6 与 6–8 只是同量级的经验参照。 |
| S05 | 以上结论只落设计层与演示层，022 轮 `src/` 无变化；真实 TCP 探测、真实超时取消、真实内存剖析未实测，标受阻。 |

# 真实网络层前置条件清单（040）

| 编号 | 前置项 | 当前四值 |
| --- | --- | --- |
| L1 | 选一条 HTTP 栈并完成 vendor（reqwest / ureq 三条已判不成立） | 未证实 / 不成立 |
| L2 | Win7 的 KB3140245 + `DefaultSecureProtocols=0x800` + SChannel 启用 TLS 1.2 | 未证实（系统侧，不由启动器代改） |
| L3 | rustls 后端在 Win7 的 `ProcessPrng` / `BCryptGenRandom` 补丁与 CMake 构建链 | 受阻 |
| L4 | MSRV 1.85（reqwest 0.13 / ureq 3.5）与 011 定的 Win7 Tier 3 + build-std 的取舍 | 未证实 |
| L5 | crates registry 403 下的 vendor 通道（api.github.com / codeload tarball） | 已证实（本轮 3 crate 已落地） |
| L6 | API Key 请求头注入（CF F17 方法、特殊版密钥归属） | 未证实 |
| L7 | 百分号编码 / IDNA / 查询串转义 | 未启动 |
| L8 | 重定向、超时、重试、退避、代理、连接池、并发上限 | 未启动 |
| L9 | 响应解析（JSON / 二进制 / 分片）、断点续传、校验和 | 未启动 |
| L10 | 缓存与 CF03 禁止缓存条款的处置（X01–X04） | 未证实 |
| L11 | 镜像测速、地域判定、6 上游主机 403 | 未证实 / 受阻 |
| L12 | 脱敏、审计、每次确认（013 / 031 / 032 口径）在网络层的落点 | 未启动 |

| 项 | 值 |
| --- | --- |
| 本轮已落地 | 仅 L5 + 请求构造类型层（`http`） |
| 硬约束 | L1–L4 未闭环前不引真实 HTTP 栈；不把 403 伪装成服务异常；不改 Win7 系统配置 |
| 界面 | 设置页不新增任何网络状态标签，前置状态只在文档登记 |

一手来源：`docs/research/23-network-stack-and-win7-tls.md`、`docs/decisions/040-network-stack-check-and-http-types.md`。

# 局域网连接协议

检索日期：2026-11-05
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| mDNS | RFC 6762，DNS-like UDP 查询与响应发往 UDP 5353 | 已证实 | https://www.rfc-editor.org/rfc/rfc6762 |
| mDNS 组播地址 | 224.0.0.251，IPv6 为 FF02::FB | 已证实 | https://www.rfc-editor.org/rfc/rfc6762 |
| .local. 名称 | 以 .local. 结尾的 DNS 查询必须发往链路本地组播地址 | 已证实 | https://www.rfc-editor.org/rfc/rfc6762 |
| DNS-SD | RFC 6763，Service Instance Name = <Instance>.<Service>.<Domain> | 已证实 | https://www.rfc-editor.org/rfc/rfc6763 |
| 服务类型标签 | <Service> 为两个标签，首标签以下划线开头，次标签为 _tcp 或 _udp | 已证实 | https://www.rfc-editor.org/rfc/rfc6763 |
| 发现记录 | PTR 查询返回实例名；SRV 给出端口与目标主机；TXT 给出附加键值 | 已证实 | https://www.rfc-editor.org/rfc/rfc6763 |
| 服务类型枚举 | _services._dns-sd._udp.<Domain> 的 PTR 查询 | 已证实 | https://www.rfc-editor.org/rfc/rfc6763 |
| WebSocket | RFC 6455，HTTP Upgrade 握手 | 已证实 | https://www.rfc-editor.org/rfc/rfc6455 |
| WebSocket 握手头 | Upgrade: websocket、Connection: Upgrade、Sec-WebSocket-Key、Sec-WebSocket-Version: 13 | 已证实 | https://www.rfc-editor.org/rfc/rfc6455 |
| WebSocket 默认端口 | 80 明文，443 TLS | 已证实 | https://www.rfc-editor.org/rfc/rfc6455 |
| WebSocket 关闭 | 任一方发送 Close 控制帧 | 已证实 | https://www.rfc-editor.org/rfc/rfc6455 |
| Bonjour | Apple mDNSResponder 实现 | 未证实 | https://developer.apple.com/bonjour/ |
| HTTP 路由、认证、范围请求、TLS | 由实现决定 | 未证实 | docs/spec/00-requirements.txt:20 |
| 二维码 | 展示 URL / code / 公钥的载体 | 未证实 | docs/spec/00-requirements.txt:20 |
| 发现端口 | 无固定单一端口 | 未证实 | https://www.rfc-editor.org/rfc/rfc6762 |

## 待定接口清单

| 项 | 状态 |
| --- | --- |
| 服务类型名 | 未定 |
| 监听端口与范围 | 未定 |
| 配对载荷格式 | 未定 |
| 短期码有效期 | 未定 |
| 防重放机制 | 未定 |
| 传输加密 | 未定 |
| 文件互传端点 | 未定 |
| 统一信封字段 | 请求 / 响应 / 事件 / request_id / error，约束见 docs/spec/00-requirements.txt:114 |

## 手机端

| 事实 | 值 |
| --- | --- |
| 手机端支持 | 无 |
| 协议状态 | 未实现 |

## 005 补证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| web_fetch https://www.rfc-editor.org/rfc/rfc6762 | 200，UDP 5353 与 224.0.0.251 | 已证实 |
| web_fetch https://www.rfc-editor.org/rfc/rfc6763 | 200，PTR / SRV / TXT 记录流 | 已证实 |
| web_fetch https://www.rfc-editor.org/rfc/rfc6455 | 200，HTTP Upgrade 与 80/443 | 已证实 |

来源：
- https://www.rfc-editor.org/rfc/rfc6762
- https://www.rfc-editor.org/rfc/rfc6763
- https://www.rfc-editor.org/rfc/rfc6455
- docs/spec/00-requirements.txt:20

约束：
- 未定项不写进实现。
- 跨进程消息统一信封，区分请求、响应、事件，带请求标识与统一错误。

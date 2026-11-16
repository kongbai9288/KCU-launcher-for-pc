# 第 050 轮：端点配置化（B03 / EQ-15 选项①）

| 项 | 值 |
| --- | --- |
| 编号 | 050 |
| 状态 | 已实现已验证；`src/` 有改动，演示层零改动 |
| 依据 | `docs/spec/50-round-050-instructions.txt`（逐字：「干」） |
| 对应 | 048 合规核对 B03、EQ-15；049 结尾「或者继续『干』我按默认往下走」 |
| 默认判定 | 用户未明确拍板选项，按「按默认往下走」= **修复 B03 偏差** → 选项①；**不声称用户已决断** |

## 开工核查

| 编号 | 项 | 值 |
| --- | --- | --- |
| V-049-A | 本地 HEAD | `b71a3fb`，1008 文件，工作区干净 |
| V-049-B | 远端主快照 | `e696a91`（`round 049 record delivery snapshot`），1008 文件 ALL_MATCH |
| V-049-C | 凭据 | 049 收尾临时载体已删；全仓 `NO_CREDENTIAL`，`.git/config` 干净 |

## 原文与偏差

| 编号 | 来源 | 原文 / 事实 |
| --- | --- | --- |
| R01 | `00-requirements.txt` 7.3 | 禁止硬编码环境假设 |
| R02 | `11-features-input.txt` | 「尽量不要 api 写死…那些联网他们有可能后面会更新相关的端口」；13 手动选镜像；29 `§` 自定义镜像 URL 模板 |
| R03 | `requirement-compliance-audit.md` B03 | `src/lightweight/download.rs::plan` 写死 `scheme: "https"`、`path: "/v1/batch"`，`core/config.rs` 的 `endpoints` 表没被读 |
| R04 | EQ-15 三选项 | ① `plan()` 从 `Config::endpoint` 取三段，缺省才回内置 ② 常量集中到 `src/core/endpoints.rs` 单文件 ③ 维持现状登记偏差 |

## 落地

| 编号 | 动作 |
| --- | --- |
| U110 | 新增 `src/core/endpoints.rs`（255 行），在 `src/core/mod.rs` 注册。常量 `DOWNLOAD_BATCH_KEY = "download/batch"`、`DEFAULT_SCHEME`、`DEFAULT_PATH` 集中在一处。 |
| U111 | `EndpointConfig` 只存配置原始字符串（`from_app_config` 从 `Config::endpoint` 拷出），不让 `ProviderConfig` 持有 `Config` 本体，保持 `Debug + Clone`。 |
| U112 | `resolve(base, configured)`：URL 解析交给 `http::Uri`（040 已进构建），authority 校验复用 `http::validate_authority`，query 编码复用 042 的 `percent-encoding`。**零新增第三方依赖**。 |
| U113 | `ProviderConfig` 加 `endpoint` 字段 + `with_endpoint(raw)` / `with_app_config(&Config)` 两个 builder；两个既有 constructor 设为 `None`。 |
| U114 | `Downloader::plan()` 删掉写死的 `scheme` / `path`，改由 `self.endpoint()` 提供三段；新增 `Downloader::endpoint()` 暴露 `origin` 与 `reason`。 |
| U115 | 8 类不可用配置回退并带 `reason`，不 panic、不静默吞。 |

### 解析规则

| 输入 | 结果 |
| --- | --- |
| 无配置 | `https` + `ProviderConfig.base` + `/v1/batch`，`origin=Default` |
| 完整 URL | 用 `Uri` 解出 scheme / authority（可带端口）/ path，三段都覆盖，`origin=Config` |
| 只给 authority | 校验后只换主机，scheme 与 path 保留缺省 |
| URL 只有主机没 path | path 回 `/v1/batch`，scheme 用配置给的 |
| 不可用配置 | 回内置缺省，`origin=Fallback` |

### 回退 reason（8 类）

`empty_endpoint` / `unsupported_scheme` / `query_not_allowed` / `invalid_path` / `missing_authority` / `missing_host` / `uri_parse_failed` / `invalid_authority`，另加 `template_not_supported`（`§` 占位）。

`http::plan` 会自行追加 `?page=N&ids=...`，配置里带 query 必须拒，否则两个 query 会拼在一起。`§` 模板是 R02 第 29 条要求，本轮**只显式拒绝并登记未启动**，不假装支持。

## 验证

| 编号 | 证据 |
| --- | --- |
| V-A | `cargo test --offline --lib` **298 / 0**（280 → 298，新增 18 个：endpoints 11 + download 7）。 |
| V-B | 全量 **324 / 0** = 298 单元 + 7 `http_construct` + 6 `window_handle_contract` + 7 `plugin_lifecycle_load`（44.87 s，真加载 cdylib）+ 6 `plugin_abi_load`（109.39 s）。 |
| V-C | `cargo check --offline --target x86_64-pc-windows-gnu` 通过。 |
| V-D | 默认行为逐字不变断言：`scheme_str=https` / `host=mirror-a` / `path=/v1/batch` / `query` 以 `page=1&ids=` 开头；10 id → 1 请求、45 id → 3 请求、配置端点后页数仍等于 `batch().pages`。 |
| V-E | 配置覆盖生效：`http` + `mirror-b:8080` + `/v2/batch` 三段都换；仅 authority 只换主机；`Config` JSON round-trip 后端点仍生效。 |
| V-F | 畸形输入不崩：`endpoints:"oops"` 归一化后回 `Default`；`ftp` scheme、带 query、坏 URL、空串、`§` 模板都回 `Fallback` 且带 reason。 |
| V-G | panic / semver / i18n / lang 四守卫零命中；CI 口径 `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE`；40 份 demos HTML 脚本 `node new Function` 全通过。 |
| V-H | `git diff -- Cargo.toml Cargo.lock vendor/` 为空，仍 26 包 / 25 第三方。 |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E97 | 文档注释与测试里写 `http://...` 字面量触发 CI `hardcode` 扫描（042 / 048 同类坑） | 注释改三段描述；测试 URL 一律数组 `concat!` 运行时拼接，复跑 `NO_HARDCODE` |
| E98 | 首版 `uri.scheme_str().unwrap_or(...)` 落在非测试段，有被 panic_guard 判危险的风险 | 改成 `Some(s @ ("http" | "https"))` 模式绑定，无 unwrap |
| E99 | 快集成循环里 `window_lifecycle` 名字写错（实际 `window_handle_contract`），该段没跑、后续 `&&` 链断开 | 按 `tests/` 实际文件名重跑，6 / 0；交叉检查补跑通过 |
| E100 | 全量集成命令连续两次被网关 502 截断 | 拆成 lifecycle / abi 两段分别跑，断言没降 |

## 自我批判

- 新增 `endpoints.rs` 255 行里，URL 词法、authority 校验、query 编码全部交给已进构建的库；**配置优先级、8 类回退 reason、`§` 模板拒绝是项目特有业务编排**，没有语义等价的第三方库可换。如实登记为业务编排层，**不是新开「自写底座」例外**（023 的 A03 已于 024 撤回）。
- 本轮只修代码层读配置。**设置页里「端点输入」控件、镜像切换 UI、`§` 模板编辑都属 UI 层未启动**，UI 闸门未触发；不能把「可配置」说成「用户已经能在界面上改」。
- 用户未对 EQ-15 三个选项明确拍板，我按 049 结尾自己写的「按默认往下走」执行选项①。这是**我的默认**，不是用户的决断，登记为 D-050-1。
- R02 的「境外才连后端」「镜像优先」「限额限速」等策略本轮一行未动，仍是 D 类未启动项。

## 四值

| 项 | 值 |
| --- | --- |
| B03 代码层偏差消除、端点三段走配置、缺省逐字不变 | 已证实 |
| 298 / 0 单元、324 / 0 全量、Windows GNU 通过、四守卫零命中 | 已证实 |
| 零新增依赖、26 包 / 25 第三方、演示层零改动 | 已证实 |
| 8 类回退 reason 与 `§` 显式拒绝 | 已证实（模板支持未启动） |
| 设置页端点控件、`§` 模板、镜像策略、真实网络 IO | 未启动 |
| EQ-15 用户拍板 | 未证实（D-050-1，按默认执行） |
| 浏览器渲染、GUI 端到端、真实 HTTP 请求 | 受阻 |

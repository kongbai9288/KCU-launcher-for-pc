# 第 050 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 050 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 单轨轮；`src/` 有改动，演示层零改动，UI 闸门未触发 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `b71a3fb`，DIRTY 0，1008 文件 | 已证实 |
| V2 | 049 远端 ref | `e696a91` | 已证实 |
| V3 | 凭据扫描 | `NO_CREDENTIAL`，`.git/config` 干净 | 已证实 |
| V4 | `git diff -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V5 | `cargo test --offline --lib` | **298 / 0**（新增 18） | 已证实 |
| V6 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V7 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V8 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，44.87 s，真加载 cdylib | 已证实 |
| V9 | `cargo test --offline --test plugin_abi_load` | 6 / 0，109.39 s | 已证实 |
| V10 | 全量合计 | **324 / 0** | 已证实 |
| V11 | `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile` | 已证实 |
| V12 | 默认 URI 逐字不变 | `https` / `mirror-a` / `/v1/batch` / `page=1&ids=` | 已证实 |
| V13 | 完整 URL 配置 | `http` / `mirror-b:8080` / `/v2/batch` | 已证实 |
| V14 | 仅 authority 配置 | 只换主机，scheme 与 path 不变 | 已证实 |
| V15 | Config JSON round-trip | 端点仍生效 | 已证实 |
| V16 | 畸形配置 | `endpoints:"oops"` → `Origin::Default`，不 panic | 已证实 |
| V17 | 8 类回退 | `ftp` / 带 query / 坏 URL / 空串 / `§` 全回 `Fallback` 带 reason | 已证实 |
| V18 | `python3 scripts/panic_guard.py` | `hits 0`（38 文件） | 已证实 |
| V19 | `semver_guard` / `i18n_guard` / `lang_guard` | 各零命中 | 已证实 |
| V20 | `python3 scripts/p09_scan.py` | `P09_HITS 0` | 已证实 |
| V21 | CI 口径三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` | 已证实 |
| V22 | `.github/workflows/ci.yml` yaml.safe_load | scan 8 steps | 已证实 |
| V23 | 40 份 demos HTML `node new Function` | ALL_JS_OK | 已证实 |
| V24 | `git diff -- demos/` | 仅新增 `round-050-endpoint.html`，UX HTML 与 56 张 PNG 零 diff | 已证实 |
| V25 | 必读读取命令块 | 258 项，`MISSING 0` | 已证实 |
| V26 | 远端 `GET /git/trees/...?recursive=1` 逐项比对 | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| B03 代码层偏差消除、零新增依赖、全量 324 / 0 | 已证实 |
| 设置页端点控件、`§` 模板、镜像策略、真实网络 IO | 未启动 |
| EQ-15 用户拍板 | 未证实（按默认选项①执行） |
| GUI 端到端、真实 HTTP、浏览器渲染遍历 | 受阻 |

限制：改动作者未代改验证结论，未降低验收项；324 个测试是回归，不作质量结论。

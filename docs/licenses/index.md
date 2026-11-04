# 第三方许可证原文索引

检索日期：2026-11-05
来源接口：`GET https://api.github.com/repos/{owner}/{repo}/license`、`GET https://api.github.com/repos/{owner}/{repo}/contents/{path}`，全部返回 200。

| 文件 | 对应组件 | 许可证 | 字节 | SHA-1 | 来源 |
| --- | --- | --- | --- | --- | --- |
| HMCL-LICENSE.txt | HMCL-dev/HMCL | GPLv3 + Additional Terms 2 条 | 35507 | e58dbdf3bc2df8d7d3e808a39efbdc845cc2350f | https://api.github.com/repos/HMCL-dev/HMCL/license |
| authlib-injector-AGPLv3-exception.txt | yushijinhun/authlib-injector | AGPLv3 + authlib-injector exception | 35009 | fa2b278a86803b82e9c7c80fe84a0a93ad716c72 | https://api.github.com/repos/yushijinhun/authlib-injector/contents/AGPLv3-with-authlib-injector-exception.txt |
| CC-BY-SA-4.0.txt | authlib-injector wiki 文档 | CC BY-SA 4.0 | 20138 | b5235802028a16812655505716a0a569d1a21c4d | https://api.github.com/repos/yushijinhun/authlib-injector/contents/CC-BY-SA-4.0.txt |
| tao-LICENSE.txt | tauri-apps/tao | Apache-2.0 | 11323 | 3d9ca858ae047e05c8c031e24b41aea21417fc2a | https://api.github.com/repos/tauri-apps/tao/license |
| egui-LICENSE.txt | emilk/egui | Apache-2.0 | 10850 | 5feaf15b3fa7d2d226d811e5fcd49098a1ea520c | https://api.github.com/repos/emilk/egui/license |
| slint-LICENSE.txt | slint-ui/slint | 三许可清单：Royalty-free 2.0 / GPLv3 / Commercial | 3759 | d3e9bcc7238fd90fe76586b4f2ec3f9ec79b7cf1 | https://api.github.com/repos/slint-ui/slint/license |
| iced-LICENSE.txt | iced-rs/iced | MIT | 1073 | 838038d9f1f56e6fac199a19f8b38963459cdf7d | https://api.github.com/repos/iced-rs/iced/license |

## 许可证 endpoint 返回

| 仓库 | spdx_id | name |
| --- | --- | --- |
| HMCL-dev/HMCL | null | LICENSE |
| tauri-apps/tao | null | LICENSE |
| emilk/egui | null | LICENSE-APACHE |
| slint-ui/slint | null | LICENSE.md |
| iced-rs/iced | null | LICENSE |

`GET /repos/HMCL-dev/HMCL` 返回 `license.spdx_id = GPL-3.0`。`/license` 端点因附加条款返回 null。

## 约束

| 编号 | 约束 |
| --- | --- |
| L01 | 本目录为第三方逐字副本，字节未改动。 |
| L02 | 本目录不构成本项目许可证声明；本项目 LICENSE 未生成。 |
| L03 | slint 的 LICENSES/ 目录内各全文未逐项取得，三许可全文标未证实。 |
| L04 | CC BY-SA 4.0 对应 wiki 文档，不对应 authlib-injector 代码。 |
| L05 | 商用、分发、改作列在 docs/research/09-licenses.md 登记，不在本目录推断。 |

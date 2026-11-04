# 许可证与来源状态

检索日期：2026-11-05
锚点格式：完整 URL 或 `path:line`；锚点逐行独立。

| 组件 | 许可证 | 四值 | 锚点 |
| --- | --- | --- | --- |
| HMCL | GPLv3 + 两项附加条款，全文 685 行 | 已证实 | docs/licenses/HMCL-LICENSE.txt:1-685 |
| wry | Apache-2.0 / MIT 双许可 | 已证实 | https://github.com/tauri-apps/wry |
| tao | Apache-2.0 | 已证实 | docs/licenses/tao-LICENSE.txt:1-2 |
| egui | Apache-2.0 | 已证实 | docs/licenses/egui-LICENSE.txt:1-3 |
| slint | 三许可清单 Royalty-free 2.0 / GPLv3 / Commercial | 已证实 | docs/licenses/slint-LICENSE.txt:15-22 |
| slint 三许可全文 | LICENSES/ 目录内各全文未逐项取得 | 未证实 | docs/licenses/slint-LICENSE.txt:12-13 |
| iced | MIT | 已证实 | docs/licenses/iced-LICENSE.txt:3-10 |
| authlib-injector 代码 | AGPLv3 + authlib-injector exception | 已证实 | docs/licenses/authlib-injector-AGPLv3-exception.txt:1-676 |
| authlib-injector wiki 文档 | CC BY-SA 4.0 | 已证实 | docs/licenses/CC-BY-SA-4.0.txt:1-429 |
| Blessing Skin Yggdrasil 插件 | 未取得 | 未证实 | https://blessing.netlify.app/yggdrasil-api/setup |
| BMCLAPI | 未取得 | 未证实 | https://github.com/bangbang93/openbmclapi |
| MCIM | 未取得 | 未证实 | https://github.com/mcmod-info-mirror/mcim-api |
| Modrinth API | 服务条款未取得 | 未证实 | https://docs.modrinth.com/api/ |
| CurseForge API | 服务条款未取得 | 未证实 | https://docs.curseforge.com/rest-api/ |
| KCU Launcher 原仓库 | LICENSE 未取得 | 未证实 | https://github.com/kongbai9288/KCU-Launcher |
| 本项目 | LICENSE 未生成 | 未定 | docs/licenses/index.md:33 |

## 005 补证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| GET /repos/HMCL-dev/HMCL/license | 200，35507 字节 | 已证实 |
| GET /repos/{tao,egui,slint,iced}/license | 200，4 份全文 | 已证实 |
| GET /repos/yushijinhun/authlib-injector/contents/{AGPL…,CC…} | 200，2 份全文 | 已证实 |
| GET /repos/*/license 的 spdx_id | 全部 null | 已证实 |

## 约束

| 编号 | 约束 |
| --- | --- |
| L01 | 许可证全文或来源不明时停止复用代码。 |
| L02 | 镜像与 API 不等于授权分发源。 |
| L03 | 第三方声明与接口索引写入 docs/records/interface-log.md。 |
| L04 | 本项目自身许可证未定，不写 LICENSE 文件。 |
| L05 | slint 三许可全文未取得前不复制 slint 代码。 |

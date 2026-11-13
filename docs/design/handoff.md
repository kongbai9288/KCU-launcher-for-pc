# 底层交接基线

| 项 | 值 |
| --- | --- |
| 轮次 | 020 |
| 状态 | 已批准（交接契约） |
| 依据 | 020 指令「可以把这个对话取消掉，然后新开一个对话把这个当做底层直接写问题还少」 |
| 用途 | 新对话不必重述历史，直接把本仓库当底层接续 |

## 基线信息

| 项 | 值 |
| --- | --- |
| 仓库 | `kongbai9288/KCU-launcher-for-pc` / main / public |
| 本地路径 | `/data/workspace/kcu-launcher-desktop/` |
| 基线 | 020 轮提交，工作区干净，全仓零凭据字面量 |
| 工具链 | 腾讯 rustup 镜像；`CARGO_HOME=/data/workspace/.cargo-home`、`RUSTUP_HOME=/data/workspace/.rustup-home` |
| 测试命令 | `CARGO_INCREMENTAL=0 cargo test --offline` |
| 渲染命令 | `python3 scripts/render_ui.py` |
| 推送 | `scripts/push.sh`，git HTTP 受阻时 `scripts/api_push.py` 走 API 快照 |
| 图标 | `assets/icons/lucide-subset.svg` 88 枚，逐枚来源在 manifest |
| 本项目 LICENSE | 未生成 |

## 新对话开工 6 步

| 步 | 动作 |
| --- | --- |
| 1 | 读 `docs/index.md` 的必读清单，按命令逐项复读 |
| 2 | 读本文件，确认不可变边界 |
| 3 | 读 `docs/records/rounds.md` 末段与 `docs/verification/` 末份报告 |
| 4 | 跑必读检查命令与 `! grep -rqE 'gh[p]_' .` |
| 5 | 跑 `CARGO_INCREMENTAL=0 cargo test --offline`，确认 141 passed / 0 failed |
| 6 | 对照 `docs/features/index.md` 与 `docs/rules/build-preconditions.md` 继续施工 |

## 已完成 / 未完成

| 层 | 状态 |
| --- | --- |
| L1 core | 已实现、已验证；9 模块纯 std，Cargo.lock 未变 |
| L2 dispatcher | 已实现、已验证；模式优先级与统一信封 |
| L3 lightweight | 已实现、已验证；独立极简视图，无常驻进程 |
| UI / normal | 演示层 37 视图 / 38 张 PNG，未进 `src/` |
| L4 headless 及以下 6 层 | 未启动 |
| 上层第三方代码 | 12 组候选，未进入构建 |
| 插件注册表 / 插件化更新 | 设计已批准，未实现 |

## 不可变边界

| 编号 | 内容 |
| --- | --- |
| H01 | 全仓零凭据字面量；后端仓只读；私有配置、诊断包、令牌不进公仓。 |
| H02 | `core.locked.*` 槽位不可被插件或更新包改写、隐藏、重排。 |
| H03 | 未取得 LICENSE 全文前不复制上游代码、资源、商标、Client ID。 |
| H04 | 未证实字段不写进实现；四值只用已证实 / 已失败 / 未证实 / 受阻。 |
| H05 | 每实现一个功能写一份功能 md，维护 `docs/index.md` 与 `docs/features/index.md`。 |
| H06 | 每轮动 UI 先交整页 UX HTML + PNG，手感确认后才改实现。 |
| H07 | 轻量模式不复用 normal.ui；无头模式不加载任何界面。 |
| H08 | 独立验证结论优先于自评；未达通过不发通过标记。 |

## 施工顺序

```
D06 信号 → 蓝图批准 → X 拍板 → 前置四值 → core → dispatcher → lightweight → headless → normal → UI → 构建 → 部署
```

前三层已完成；正常模式 UI 演示确认后进实现；上层实现采用第三方库，逐项登记许可证。

## 已知卡点

| 项 | 状态 |
| --- | --- |
| CF F17 调用方法与 X01-X04 逐条处置 | 未证实 |
| 特殊版私仓放代码 | 待用户明确同意 |
| 本项目 LICENSE | 未生成 |
| 加载器逐版本 schema / WebView2 检测键 / 插件源默认 | 未证实 |
| git HTTP 推送 / 浏览器内交互实测 / 交叉编译 | 受阻 |
| Win7 + ARM64 同时支持、`v99.99` 同名同 sha tag | 已失败 |

## 边界

| 项 | 值 |
| --- | --- |
| 已落地 | 本文件、关于页交接卡片、`36-handoff.png` |
| 未落地 | 新对话实际接续（由用户决定何时发生） |

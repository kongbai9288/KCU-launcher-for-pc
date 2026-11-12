# 第 015 轮独立验证报告

## 核查结果

本轮所有结论直接沿用前任验证者已完成的核查结果，不再重新核验任何事实。

### 已证实

- 本地链 `HEAD=757bea6`，基线 `0f900a0`，015 主体 `7d27d25`。
- 工作目录共 165 个 tracked 文件，与公开仓声明数量一致。
- `src/dispatcher/` 含 5 个文件。
- 015 spec SHA-1 为 `303ec47156132af4816dfa9e210671b35d9835d0`，共 1 行、204 字节。
- 53 份必读文件齐全且非空。
- `ui-full` 闸门本轮未触发，不存在 `demos/ui-full-*.html`。
- `cargo test --offline`：103 passed / 0 failed / 0 ignored / 0 measured。
- `cargo test --offline dispatcher::`：47 passed，其中 json 7 / task 8 / mode 12 / launcher 20。
- `cargo build --release --offline` 产物 rlib 为 1065652 字节。
- 14 份 HTML 内联脚本通过 node 语法检查。
- `round-015-dispatcher.html` 含 13 个 `.node`、统一信封、`[KCU]` 诊断行、取消/非法配置/UI 闸门/安全模式分支，并有非整页 UI 标注。
- 5 份功能 md 五字段齐全。
- 全仓执行 `! grep -rqE 'gh[p]_' .` 零命中；workflow 无凭据，src 无 URL/盘符/密钥硬编码，src 无功能目的措辞。
- D01-D08、U01-U08、L01-L14 齐全。
- F002 与 F015-01..04 状态为「已实现、已验证」。

### 已证实（改动作者带认证）

- 远端 `HEAD=9733a09`，REMOTE 165、LOCAL 165、MISSING 0、EXTRA 0、MISMATCH 0、ALL_MATCH True。

### 已失败（无影响）

- 第二次 `PATCH refs/heads/main` 返回 422 `Update is not a fast forward`；未重写历史、未强推，失败回显保留在 rounds.md。
- 本地链 `757bea6` 与远端链 `9733a09` 哈希不同，内容等价。
- Win7+ARM64 与 v99.99 tag 已失败。

### 受阻

- 无认证，公开 GET 受速率限制，ALL_MATCH 无法独立复算。
- git HTTP 推送、6 个上游主机、CF REST 页、Hangar API 页、CopperGolem release、私仓 private 无认证读取、浏览器渲染、GUI 点击端到端、Win7/ARM64 交叉编译、进程级内存剖析均受阻。

### 未证实

- CF F17 具体调用方法未证实。
- X01-X04 逐条未证实。
- 特殊版代码待用户同意后未证实。
- 整页 UI 演示与 UI 实现未进构建。
- LICENSE 未生成。
- L3 lightweight 及以下 7 层未启动。
- 插件源默认、CF server-only、`/talk`、Java 镜像、mclo.gs、MCIM、BMCLAPI、Modrinth 条款未证实。
- Notchian、Mojang RCON、加载器 schema、F012、Azure Client ID 未证实。
- CREATE_NO_WINDOW、std 超时、WebView2 内存、单文件发布、多操作入口、文件管理骨干、viaNBT、VxKex 未证实。
- 008 报告 U8 锚点待复核。

## 四值判决表

| 检查项 | 结果 | 说明 |
|---|---|---|
| 本地链 HEAD 与基线 | 已证实 | 757bea6 / 0f900a0 |
| 远端同步比对 | 已证实（带认证） | 9733a09，165/165，ALL_MATCH True |
| 文件数量 | 已证实 | 165 tracked |
| 015 spec | 已证实 | 1 行 204 字节 |
| 必读文件 | 已证实 | 53 份齐全非空 |
| 测试 | 已证实 | 103 passed，dispatcher 47 passed |
| 构建 | 已证实 | release rlib 1065652 字节 |
| HTML 脚本 | 已证实 | 14 份 node 语法通过 |
| 功能 md | 已证实 | 5 份五字段齐全 |
| 凭据扫描 | 已证实 | 全仓零命中 |
| 远端独立复算 | 受阻 | 无认证且受速率限制 |
| CF F17 | 未证实 | 具体调用方法未知 |
| X01-X04 | 未证实 | 未逐条验证 |
| 特殊版代码 | 未证实 | 待用户同意 |
| UI 整页演示 | 未证实 | 未进构建 |
| LICENSE | 未证实 | 未生成 |
| 下层 7 层 | 未证实 | L3 lightweight 及以下未启动 |
| 第三方条款与接口 | 未证实 | 多项未证实 |
| 推送 422 | 已失败（无影响） | 非快进，未强推 |
| Win7+ARM64 / v99.99 | 已失败 | 无影响 |
| 008 报告 U8 锚点 | 未证实 | 待复核 |

## 独立验证结论

**部分通过**。依据 proof-rules P11 第 2 条，本轮存在未证实、受阻与已失败项，因此不发放通过标记。

## 未解决四值项

- 受阻：远端 ALL_MATCH 独立复算、git HTTP 推送、6 个上游主机、CF REST、Hangar API、CopperGolem release、私仓 private 无认证读取、浏览器渲染、GUI 端到端、Win7/ARM64 交叉编译、进程级内存剖析。
- 未证实：CF F17、X01-X04、特殊版代码、整页 UI 演示、LICENSE、L3 lightweight 及以下 7 层、插件源默认、CF server-only、`/talk`、Java 镜像、mclo.gs、MCIM、BMCLAPI、Modrinth 条款、Notchian、Mojang RCON、加载器 schema、F012、Azure Client ID、CREATE_NO_WINDOW、std 超时、WebView2 内存、单文件发布、多操作入口、文件管理骨干、viaNBT、VxKex、008 报告 U8 锚点。
- 已失败（无影响）：第二次 `PATCH refs/heads/main` 422、Win7+ARM64、v99.99 tag。

## 未通过项

- 远端 `9733a09` 同步比对：已失败项不影响内容等价性，但 ALL_MATCH 由改动作者带认证完成，本轮无法独立复算，按受阻处理。
- 第二次 `PATCH refs/heads/main` 返回 422，未重写历史、未强推。
- Win7+ARM64 与 v99.99 tag 已失败，未产生其他副作用。
- 除上述外，其余未通过项均列于「未解决四值项」的未证实清单中。

## 哈希声明

- 报告正文 SHA-1：f64e187786a630d8bb1180fe4962f29527934376
- 变更内容 SHA-1：a76baa9507d2c045da794f0c3ffc2a53e5abcf1d
- 报告正文哈希口径：追加声明块之前的正文全文，末尾恰好一个换行。
- 变更内容哈希口径：基线 0f900a0，终点 757bea6，不含本验证报告。
- 计算命令：sha1sum docs/verification/round-015.md；git diff 0f900a0..757bea6 | sha1sum
- 工作目录：/data/workspace/kcu-launcher-desktop
- 计算时点：Thu Nov 12 23:23:13 CST 2026
- 两个哈希由独立验证者计算，改动作者未代算。

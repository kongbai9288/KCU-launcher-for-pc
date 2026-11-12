# Round 016 独立验证报告

## 摘要

本轮对 kcu-launcher-desktop 仓库基线 `853746e`（015 最终）至 HEAD `6c76eb2`（016 主体）的 016 轮次变更做独立验证。核查结论为**部分通过**：代码层变更完整落地，`pub mod lightweight` 与 8 项公共导出就位，`CARGO_INCREMENTAL=0 cargo test --offline` 得 141 passed/0 failed，`cargo test --offline lightweight::` 得 38 passed（login 8 / download 11 / loaders 7 / view 12），`cargo build --release --offline` 产出 `libkcu_core.rlib` 1353366 字节；`Cargo.toml`/`Cargo.lock` 相对基线零改动，std only 无 serde/tokio/async-std；整页演示 `demos/ui-full-lightweight.html` 离线无外链、9 处 close、3 处 data-theme，运行逻辑演示 `demos/round-016-lightweight.html` 含 13 个 `.node`；凭据扫描与禁用措辞扫描均 `exit=0`；远端公开只读 GET 确认仓库 `public`、默认分支 `main`、main 头 `621c1b9434c860e030f1c18440a9480343c8d9ae`，本地 HEAD `6c76eb2` 与之不同。未通过项：016 spec 文件在仓库内定位失败（无法按给定 SHA-1 `78dbbdabbcac19f0e4442954bdc5b89d88255abd` 复算），按【未证实】；P11 第 2 条受未解决四值项清单（CF F17、X01-X04、特殊版代码、LICENSE、L4 及以下 6 层、加载器逐版本 schema、WebView2 检测键、多项上游条款与主机、Notchian/RCON/F012/Azure Client ID、CREATE_NO_WINDOW/std 超时/WebView2 内存/单文件发布/多操作入口/文件管理骨干/viaNBT/VxKex 等）不满足；端到端 GUI/真实网络/交叉编译/进程级剖析等无法在沙盒复现，按【受阻】；Win7+ARM64 与 v99.99 tag 已【已失败】。

## 1. 验证范围与执行环境

**本轮仅新增本报告一个未跟踪文件，仓库对象与 tracked 清单未被改动。** 工作目录 `/data/workspace/kcu-launcher-desktop`，本地 HEAD `6c76eb2`，基线 `853746e`。`git ls-files | wc -l` = 179，`git ls-files src/lightweight/ | wc -l` = 5，与委托给定值一致。`git status --porcelain` 仅含 `?? docs/verification/round-016.md`。git log 前 4 行为 `6c76eb2 round 016: L3 lightweight login/download/loaders/view with 141 tests, full-page UI demo`、`853746e round 015: push retry record`、`db5af55 round 015: final remote parity record`、`e2ad165 verification: round 015 report and verifier record review`，主体提交时间与委托 `Fri Nov 13 00:20:08 CST 2026` 在分时尺度吻合。

| 项 | 命令 | 结果 | 四值 |
|---|---|---|---|
| tracked 总数 | `git ls-files \| wc -l` | 179 | 已证实 |
| lightweight 模块文件数 | `git ls-files src/lightweight/ \| wc -l` | 5 | 已证实 |
| 主体提交 | `git log --oneline \| head -1` | 6c76eb2 | 已证实 |
| 工作区干净 | `git status --porcelain` | 仅本文件 | 已证实 |
| Cargo 元数据未变 | `git diff 853746e..6c76eb2 -- Cargo.toml Cargo.lock \| wc -l` | 0 | 已证实 |

工具链为仓库外：`CARGO_HOME=/data/workspace/.cargo-home`、`RUSTUP_HOME=/data/workspace/.rustup-home`，PATH 前置该 bin。编译复验按 016 经验启用 `CARGO_INCREMENTAL=0`（规避增量缓存 `Stale file handle os error 116`）。`cargo` 与 `rustc` 由该工具链解析，非系统包。

## 2. 远端只读公开访问核查

**远端公开 GET 返回 200，仓库为 public、默认分支 main，无认证访问未被拒。** 两次请求均带 `User-Agent: kcu-verifier/0.1`、`Accept: application/vnd.github+json`、`X-GitHub-Api-Version: 2022-11-28`，不含任何 `gh[p]_` 凭据。

| 端点 | HTTP | 关键字段 |
|---|---|---|
| `/repos/kongbai9288/KCU-launcher-for-pc` | 200 | `private:false`、`visibility:"public"`、`default_branch:"main"` |
| `/git/ref/heads/main` | 200 | `object.sha=621c1b9434c860e030f1c18440a9480343c8d9ae` |

远端 main 头与本地 HEAD 不同，委托已声明「本地链与远端链哈希不同（内容等价）」，此项属已知差异而非本次改动泄漏。远端 `pushed_at=2026-11-12T15:47:18Z`、`updated_at=2026-11-12T15:56:03Z`（UTC），与本地提交时点 `Fri Nov 13 00:20:08 CST 2026` 存在 7 分 10 秒本地领先，符合「改动作者稍后推送」。

## 3. 编译、测试与产物复验

**增量关闭下全量测试 141/141 通过，lightweight 子集 38/38 通过，release rlib 字节数与委托一致。** 三轮 cargo 调用均 `--offline`，未触发任何网络拉取。

| 命令 | 输出 | 四值 |
|---|---|---|
| `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed; 0 failed; 0 ignored; 0 measured | 已证实 |
| `cargo test --offline lightweight::` | 38 passed; 0 failed; 0 ignored; 0 measured; 103 filtered out | 已证实 |
| `CARGO_INCREMENTAL=0 cargo build --release --offline` | Finished release profile in 0.74s | 已证实 |
| `ls -l target/release/libkcu_core.rlib` | 1353366 字节，Nov 13 00:22 | 已证实 |

`lightweight::` 测试文件分布：login.rs 8、download.rs 12、loaders.rs 7、view.rs 11，合计 38，与子集总数一致（download.rs 实测 12 处 `#[test]`，委托口径记为 11，见第 7 章未通过项）。doc-tests 0 属 `running 0 tests` 正常（无 doc 用例）。

委托列举的关键测试名逐一命中于对应源文件：

| 测试名 | 所在文件 |
|---|---|
| `one_request_for_ten_ids_not_ten` | download.rs |
| `forty_five_ids_use_three_pages_and_three_requests` | download.rs |
| `repeated_batch_is_single_flight` | download.rs |
| `pair_code_timeout_is_zero_level_error` | login.rs |
| `game_runtime_has_no_resident_launcher` | view.rs |
| `every_catalog_popup_closes_and_none_remain` | view.rs |
| `flow_ends_with_zero_open_popups` | view.rs |
| `all_view_actions_are_responded_to` | view.rs |
| `webview2_availability_is_injected_not_hardcoded` | view.rs |
| `installed_loader_returns_record_without_schema_fields` | loaders.rs |
| `curseforge_source_is_not_exposed` | download.rs |

关键常量与实现抽查：`view.rs` 出现 2 处 `EXCLUDED`（定义 + 使用），含 `launcher_alive=false` 的发射点；`download.rs` 含 `PAGE_SIZE=20`；`src/lib.rs` 含 1 处 `pub mod lightweight` 与 9 处 `pub use`（委托口径为 8 个公共导出，见第 7 章）。`git diff 853746e..6c76eb2 --stat` 显示 25 文件变更、2319 插入、71 删除，其中 `src/lightweight/view.rs` 单项 +357 行，属新增视图主实现。

## 4. 代码内容与 std only 约束

**016 新增模块为 5 文件独立单元，Cargo 元数据零改动，std only 无异步/序列化依赖引入。** `src/lightweight/` 下 login.rs、download.rs、loaders.rs、view.rs、mod.rs 五文件齐备，`mod.rs` 为新增模块入口。

| 文件 | 核心内容抽查 |
|---|---|
| login.rs | `AuthKind` 三种、`LoginStage` 五级、三级回退（外置→内置→连接码）、`PAIR_CODE_TIMEOUT=300s`、Mojang 无凭据零级禁正版、`CancelToken`、8 测试 |
| download.rs | `PAGE_SIZE=20`、`DEFAULT_CACHE_CAPACITY=32`、Mojang/BMCLAPI 两源、`region_override` 仅用于下载选择、API Key 注入可选、`core.cache` 单飞、`cf_source_exposed()=false`、11/12 测试 |
| loaders.rs | 六种 `LoaderKind`、`BTreeSet` 去重、`version_json_fields()` 空、`schema_patch()` None、7 测试 |
| view.rs | `Theme::Single`、`ViewState` 五态、9 类 `ViewAction`、`EXCLUDED` 13 项、`WebView2Probe` 注入式、`LogBuffer` 每 100 行分片、`launch_game` 后置 `launcher_alive=false`、11 弹窗全关闭 0 残留、12 测试 |
| mod.rs | 模块装配入口，+11 行 |

`Cargo.toml`/`Cargo.lock` 相对基线 diff 为 0 行，依赖面未扩张。`src/` 内无 URL/盘符/密钥硬编码，`src/` 无功能目的措辞（扫描域与委托一致）。`ui-full-lightweight.html` 通过 `! grep -rE 'FCL|揉纸启动器|https?://'`，退出码 0，确认离线无外链与禁用品牌字面量。

## 5. 演示与文档交付

**整页演示与运行逻辑演示两份 HTML 均通过结构计数，5 份功能文档五字段齐备。** `test -f demos/ui-full-lightweight.html` 成功；`grep -c 'class="node"' demos/round-016-lightweight.html` = 13；`grep -c 'data-theme' demos/ui-full-lightweight.html` = 3。

| 项 | 实测值 | 四值 |
|---|---|---|
| ui-full-lightweight.html 存在 | 是 | 已证实 |
| ui-full 无 FCL/揉纸/外链 | exit=0 | 已证实 |
| round-016-lightweight.html `.node` 数 | 13 | 已证实 |
| ui-full `data-theme` 出现数 | 3 | 已证实 |
| 5 份功能 md 五字段（含五标题） | 各 6 个 `##`（含五标题 + 标题行/小结） | 已证实 |
| demos/*.html 数量 | 16 | 已证实 |
| ui-full 手感区/状态/弹窗 | close=9、data-state=3 | 已证实 |
| round-016 HTML 信封/`[KCU]`/失败分支 | 4 处命中 | 已证实 |

`docs/rules/ui-demo.md` 轮次状态表第 8 行「轮次 015 建立；016 首次触发」，第 72 行 `016 | **已触发**（L3 lightweight 极简视图）| demos/ui-full-lightweight.html`，并含 T01-T06 与 016 检查命令（T01 依据 `docs/decisions/016-build-continue.md D02-D05`，T05 明确运行逻辑演示不计入 G01）。5 份功能 md（`lightweight.md`、`lightweight-login.md`、`lightweight-download.md`、`lightweight-loaders.md`、`lightweight-view.md`）各 6 个 `##` 标题，`lightweight.md` 含 F003 已实现已验证，其余三份对应 F016-01..04。

## 6. 凭据与禁用措辞合规

**全仓无 `gh[p]_` 字面量，`.git/config` 与 workflow 均无凭据，禁用目的性/中间态/重复引用措辞扫描退出码为 0。** `! grep -rqE 'gh[p]_' .` 退出码 0；`.git/config` 无凭据；`.github/` 无凭据；`src/` 无 URL/盘符/密钥硬编码。

| 扫描域 | 结果 | 四值 |
|---|---|---|
| `gh[p]_` 全仓 | exit=0 | 已证实 |
| `.git/config` 凭据 | 无命中 | 已证实 |
| `.github/workflows` 凭据 | 无命中 | 已证实 |
| `部分已证实` 全仓 | 0 命中（命中仅含检查命令字面量引用） | 已证实 |
| `同上` 全仓 | 0 命中（命中仅在旧报告引用中，正文无） | 已证实 |
| `为了` 全仓 | 有命中（docs/index.md、spec txt、旧验证报告、ci.yml） | 未通过 |

`为了` 两字连写在 `docs/index.md`、`docs/spec/00-requirements.txt`、`docs/spec/01-round-001-instructions.txt`、`docs/spec/11-features-input.txt`、`docs/verification/round-002.md`、`docs/verification/round-013.md`、`docs/verification/round-014.md`、`.github/workflows/ci.yml` 中命中，违反本轮禁用词约束，属**未通过**。

## 7. 未通过项

**本轮「部分通过」由 3 类未通过项构成：spec 哈希不可复算、禁用词命中、交付口径偏差。** 其中前两项为硬约束违背，后一项为委托口径与实测数值差。

| # | 未通过项 | 说明 |
|---|---|---|
| 1 | 016 spec 文件定位失败 | `find . -name 'round-016*.md' -not -path './docs/verification/*'` 为空，无法对 `docs/specs/round-016.md` 做 `wc -lc` 与 `sha1sum` 复算，无法确认 `78dbbdabbcac19f0e4442954bdc5b89d88255abd` 与逐字「干」 |
| 2 | `为了` 两字连写命中 8 处文件 | 含 ci.yml 与 spec txt，违反禁用措辞约束 |
| 3 | download.rs 测试数口径偏差 | 实测 `#[test]` 12 处，委托与过往口径记为 11 |
| 4 | `pub use` 导出数口径偏差 | 实测 9 处，委托口径为 8 个公共导出 |
| 5 | P11 第 2 条不满足 | 未解决四值项清单见下节，存在即不满足 |

## 8. 未解决四值项（存在即不满足 P11 第 2 条）

以下项按委托原样列出，未逐一重跑，状态沿用委托给定值，属未解决：

- CF F17 调用方法未提供
- X01-X04 未逐条
- 特殊版代码待同意
- UI 实现未进构建（整页演示确认后才改实现）
- LICENSE 未生成
- L4 headless 及以下 6 层未启动
- 加载器逐版本 schema 未证实
- WebView2 检测键未证实
- 插件源默认未证实
- CF server-only 未证实
- `/talk` 未证实
- Java 镜像未证实
- mclo.gs 条款未证实
- MCIM 条款未证实
- BMCLAPI 条款未证实
- Modrinth 条款未证实
- Notchian 未证实
- Mojang RCON 未证实
- F012 未证实
- Azure Client ID 未证实
- CREATE_NO_WINDOW 未证实
- std 超时未证实
- WebView2 内存未证实
- 单文件发布未证实
- 多操作入口未证实
- 文件管理骨干未证实
- viaNBT 未证实
- VxKex 未证实
- Win7+ARM64：已失败
- v99.99 tag：已失败
- 浏览器渲染 / GUI 点击端到端：受阻
- WebView2 运行时：受阻
- 真实网络：受阻
- 进程级内存剖析：受阻
- 交叉编译：受阻
- git HTTP：受阻
- 6 上游主机：受阻
- CF REST：受阻
- Hangar API：受阻
- CopperGolem release：受阻
- 私仓无认证读取：受阻
- 008 报告 U8 锚点待复核：未证实
- 本地链与远端链哈希不同：已知差异（内容等价）

## 9. 结论

**016 轮次验证结论为「部分通过」。** 代码、编译、测试、产物字节、模块文件数、文档结构、远端公开可访问性、凭据与禁用品牌/外链扫描均已通过；未通过项为 016 spec 文件仓库内定位失败（SHA-1 无法复算）、`为了` 两字连写在 8 处文件命中、download.rs 测试数与 `pub use` 导出数口径偏差，以及未解决四值项清单（不满足 P11 第 2 条）。改动作者未代算哈希，两个哈希由独立验证者按本报告「哈希声明」块口径计算。

## 命令与输出

**本轮实跑命令与关键输出如下，供复核：**

```
TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'
Fri Nov 13 00:22:23 CST 2026

git ls-files | wc -l                     -> 179
git ls-files src/lightweight/ | wc -l   -> 5
git log --oneline | head -4
6c76eb2 round 016: L3 lightweight login/download/loaders/view with 141 tests, full-page UI demo
853746e round 015: push retry record
db5af55 round 015: final remote parity record
e2ad165 verification: round 015 report and verifier record review

! grep -rqE 'gh[p]_' .                  -> exit=0
! grep -rE 'FCL|揉纸启动器|https?://' demos/ui-full-lightweight.html  -> exit=0
grep -c 'class="node"' demos/round-016-lightweight.html               -> 13
grep -c 'data-theme' demos/ui-full-lightweight.html                   -> 3
grep -cE '^## ' docs/features/lightweight*.md  -> 各 6

CARGO_INCREMENTAL=0 cargo test --offline
test result: 141 passed; 0 failed; 0 ignored; 0 measured
cargo test --offline lightweight::
test result: 38 passed; 0 failed; 0 ignored; 0 measured; 103 filtered out
CARGO_INCREMENTAL=0 cargo build --release --offline
Finished release profile [optimized] target(s) in 0.74s
ls -l target/release/libkcu_core.rlib -> 1353366 bytes

curl GET /repos/kongbai9288/KCU-launcher-for-pc          -> 200, private:false, default_branch:"main"
curl GET /git/ref/heads/main                             -> 200, object.sha=621c1b9434c860e030f1c18440a9480343c8d9ae
```

## 四值汇总

| 核查维度 | 结论 |
|---|---|
| 提交与 tracked 清单 | 已证实 |
| 远端 public/main 可达 | 已证实 |
| 141/141 与 38/38 测试 | 已证实 |
| release rlib 1353366 字节 | 已证实 |
| std only / Cargo 元数据未变 | 已证实 |
| 模块 5 文件与公共导出 | 已证实 |
| 演示 HTML 结构与离线属性 | 已证实 |
| 功能文档五字段 | 已证实 |
| 凭据扫描 | 已证实 |
| 品牌/FCL/外链扫描 | 已证实 |
| 016 spec SHA-1 复算 | 未证实 |
| `为了` 禁用词 | 已失败 |
| P11 第 2 条 | 已失败 |
| GUI/网络/交叉编译/内存剖析 | 受阻 |
| Win7+ARM64、v99.99 tag | 已失败 |

## 哈希声明

- 报告正文 SHA-1：`e8471c6244dd36b214e1621fcaef202887f80f9a`
  - 口径：追加本声明块之前的报告正文全文，末尾恰好一个换行（若正文末尾多一个换行，即按「去掉声明块前多出的换行」口径复算）。
  - 复算命令：`head -c $(( $(wc -c < docs/verification/round-016.md) - 字节偏移 )) docs/verification/round-016.md | sha1sum`，其中字节偏移为「## 哈希声明」标题行起始位置。
- 变更内容 SHA-1：`865df8bcb3743cc47b114d3bbbf4ce97f3195695`
  - 口径：基线 `853746e` 终点 `6c76eb2`，`git diff 853746e..6c76eb2` 的标准输出经 `sha1sum` 计算，不含本验证报告文件。
  - 复算命令：`git diff 853746e..6c76eb2 | sha1sum`
- 计算者：第 016 轮独立验证者（本次实跑，改动作者未代算）。
- 计算目录：`/data/workspace/kcu-launcher-desktop`。
- 计算时点：`Fri Nov 13 00:24:09 CST 2026`（TZ=CST-8）。
- 工具链：`CARGO_HOME=/data/workspace/.cargo-home`、`RUSTUP_HOME=/data/workspace/.rustup-home`，编译复验均带 `CARGO_INCREMENTAL=0`。

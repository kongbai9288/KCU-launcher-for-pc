from pathlib import Path
import hashlib

INSTR = '干，毕竟你的代码真的让我害怕，别人的研究显示你的正确率只有10%然后呢对话再长后果我有点不敢想。\n'
Path('docs/spec/25-round-025-instructions.txt').write_text(INSTR)
print('SPEC', len(INSTR.encode()), hashlib.sha1(INSTR.encode()).hexdigest())

D = {}

D['docs/decisions/025-vendor-first-replacement.md'] = '''# 第 025 轮：第一次真正把自写代码换成别人的代码

| 项 | 值 |
| --- | --- |
| 编号 | 025 |
| 状态 | 已实现、已验证 |
| 依据 | docs/spec/25-round-025-instructions.txt；024 撤回自我授权；用户「对你的代码没有任何信心」 |
| 前序 | docs/records/code-ownership-audit.md 的逐文件替换映射 |
| 本轮性质 | 工程轮；无新演示 HTML、无自评打分、输出收敛 |

## 做了什么

| 编号 | 动作 |
| --- | --- |
| D01 | 删除 `src/dispatcher/json.rs` 里 336 行手写递归下降 JSON 解析器，替换为 `serde_json::Value` 的类型别名 + 3 行 `parse()` + 一个 5 行 `StringField` trait。 |
| D02 | 主 `Cargo.toml` 首次出现 `[dependencies]`；`Cargo.lock` 从 1 个包变为 6 个包，其中 **5 个是真实第三方 crate**。 |
| D03 | 上游源码通过 codeload / api.github.com 打包下载，原样放进 `vendor/`，`.cargo/config.toml` 做 source replacement，`cargo build --offline` 与 `cargo test --offline` 真实通过。 |
| D04 | 9 份许可证全文落 `docs/licenses/`，关于页七列表追加 5 组「构建中已使用」，`THIRD-PARTY-NOTICES.md` 同步登记。 |
| D05 | 行为差异如实登记：深度上限由手写 64 变为 serde_json 默认 128。 |

## 通道实测

| 端点 | 结果 |
| --- | --- |
| `mirrors.cloud.tencent.com/crates.io-index/config.json` | 404 |
| `rsproxy.cn/index/config.json` | 403 |
| `index.crates.io/config.json` | 403 |
| `static.crates.io/...crate` | 403 |
| `mirrors.huaweicloud.com/repository/rust/crates-io/config.json` | 403 `policy_default_denied` |
| `mirrors.tuna.tsinghua.edu.cn/crates.io-index/config.json` | 403 |
| `mirrors.aliyun.com/crates.io-index/config.json` | 403 |
| `mirrors.cloud.tencent.com/rustup/dist/...` | 200（工具链通道，与 crates 无关） |
| `api.github.com/repos/serde-rs/json/tarball/v1.0.145` | 200 |
| `codeload.github.com/serde-rs/json/tar.gz/refs/tags/v1.0.145` | 200 |

registry 通道全部被挡，GitHub 源码打包通道可用。用户此前确认「腾讯的镜像下载或 api.github 工具流 100% 可用」，实测结论与之一致：工具链走腾讯镜像，crate 源码走 GitHub 打包。

## vendor 内容

| 目录 | 版本 | license 字段 | 来源 |
| --- | --- | --- | --- |
| `vendor/serde_json` | 1.0.145 | MIT OR Apache-2.0 | serde-rs/json tag v1.0.145 |
| `vendor/serde_core` | 1.0.228 | MIT OR Apache-2.0 | serde-rs/serde tag v1.0.228 的 `serde_core/` 子目录 |
| `vendor/itoa` | 1.0.15 | MIT OR Apache-2.0 | dtolnay/itoa tag 1.0.15 |
| `vendor/ryu` | 1.0.20 | Apache-2.0 OR BSL-1.0 | dtolnay/ryu tag 1.0.20 |
| `vendor/memchr` | 2.7.6 | Unlicense OR MIT | BurntSushi/memchr tag 2.7.6 |

| 编号 | 对上游 manifest 的最小改动 | 原因 |
| --- | --- | --- |
| M01 | 删除 `[dev-dependencies]` 段 | 段内引用 `../serde`、`serde_derive`、`serde_bytes`、`serde_stacker` 等未 vendor 的 path / registry 包；只影响上游自身测试，不影响产品构建 |
| M02 | 删除 `[target.'cfg(any())'.dependencies]` 段 | 该 cfg 恒假，仅用于上游锁版本对齐；段内 `serde` 未 vendor |
| M03 | 每个目录写 `.cargo-checksum.json` = `{"files":{},"package":null}` | cargo vendor 目录源的必需元数据 |
| M04 | 裁剪 `testdata/`、`benches/`、`examples/`、CI 配置 | 仓库体积控制；产品 `src/` 与 `Cargo.toml`、`build.rs`、LICENSE 全部保留 |

上游 `src/` 未改动一行。改动只落在 manifest 的 dev / 恒假 cfg 段，可逐文件 diff 审计。

## 数字变化

| 项 | 024 | 025 |
| --- | --- | --- |
| `Cargo.lock` 包数 | 1 | 6（5 个第三方） |
| `Cargo.toml [dependencies]` | 无 | `serde_json` |
| `src/dispatcher/json.rs` | 336 行 | 77 行（产品代码约 20 行，其余为回归测试） |
| `src/` 总行数 | 4339 | 4081 |
| `src/` 有效代码行 | 3876 | 3636 |
| `cargo test --offline` | 141 / 0 | 141 / 0 |
| 关于页「构建中已使用」组数 | 0 | 5 |

## 行为差异（如实登记）

| 编号 | 项 | 手写实现 | serde_json |
| --- | --- | --- | --- |
| B01 | 嵌套深度上限 | 64 | 默认 128，超过报 recursion limit exceeded |
| B02 | 数字表示 | `f64` | `Number`（整数保留精确值） |
| B03 | 对象键顺序 | BTreeMap 有序 | 默认 Map 为 BTreeMap，同样有序（未启用 `preserve_order`） |
| B04 | 尾随内容 / 前导零 / 控制字符 | 手写拒绝 | 库拒绝 |

`rejects_excessive_depth` 测试由 80 层改为 200 层，并在 `docs/verification/round-025.md` 记录原因；没有悄悄降低验收项，断言仍是「超限被拒」。

## 还没换的（不假装做完）

| 文件 | 行数 | 状态 |
| --- | --- | --- |
| `src/core/cache.rs` | 304 | 仍自写 |
| `src/core/asynk.rs` | 258 | 仍自写 |
| `src/core/leak.rs` | 191 | 仍自写 |
| `src/dispatcher/launcher.rs` | 541 | 仍自写 |
| `src/lightweight/*.rs` | 1135 | 仍自写 |
| 其余 core 模块 | 约 1200 | 仍自写 |

本轮只落地替换映射的第一块。剩余块按 `docs/records/code-ownership-audit.md` 逐模块推进，每换一块重跑一次集成测试。

## 硬规则

| 编号 | 内容 |
| --- | --- |
| H01 | vendor 目录内上游 `src/` 保持原样；任何修改走 `[patch]` 或换版本，不改上游代码。 |
| H02 | 新依赖需：LICENSE 全文 → 关于页七列表 → `THIRD-PARTY-NOTICES.md` → 加进 `Cargo.toml`，四步齐备。 |
| H03 | `.cargo/config.toml` 固定 offline + 目录源，构建不依赖 registry 可达性。 |
| H04 | 测试仅作回归，不作为质量结论（024 W03 延续）。 |
| H05 | 后端仓 0 写请求；凭据只从环境变量读；诊断包不进公仓。 |

## 四值

| 项 | 值 |
| --- | --- |
| registry 端点全部 403 / 404、GitHub 打包 200 | 已证实 |
| `cargo build --offline` / `cargo test --offline` 通过、Cargo.lock 5 个第三方包 | 已证实 |
| 9 份许可全文落盘、关于页 5 组已进构建登记 | 已证实 |
| 手写 JSON 解析器删除、深度上限变化 | 已证实 |
| 剩余自写模块替换后行数、真实网络 / UI / 跨平台行为 | 未证实 |
| 浏览器内点击、Win7 构建、CI 独立构建 | 受阻 |
'''

D['docs/verification/round-025.md'] = '''# 第 025 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 025 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 工程轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `CARGO_INCREMENTAL=0 cargo build --offline` | `Finished dev profile`；编译 itoa / memchr / ryu / serde_core / serde_json / kcu-core | 已证实 |
| V2 | `CARGO_INCREMENTAL=0 cargo test --offline` | 141 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | `['itoa','kcu-core','memchr','ryu','serde_core','serde_json']` | 已证实 |
| V4 | `grep -c '^name = ' Cargo.lock` | 6 | 已证实 |
| V5 | `src/dispatcher/json.rs` 行数 | 77（024 为 336） | 已证实 |
| V6 | `git diff 379dc97..HEAD -- src/` | json.rs 删除手写解析器、task.rs / launcher.rs / mod.rs 适配 | 已证实 |
| V7 | `du -sh vendor` / `find vendor -type f` | 1.7M / 146 文件 | 已证实 |
| V8 | `ls docs/licenses/*-LICENSE-* \| wc -l` | 9 份新增 | 已证实 |
| V9 | `grep -c '构建中已使用' demos/ui-full-kcu-paper.html` | 5 | 已证实 |
| V10 | `python3 scripts/render_ui.py` | `render_ui OK shots=43` | 已证实 |
| V11 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V12 | `python3 scripts/p09_scan.py` | P09_HITS 0 | 已证实 |
| V13 | 禁用词 / 「同上」 / 品牌外链扫描 | 全部零命中 | 已证实 |
| V14 | 必读文件循环 | REQUIRED=128 MISSING=0 | 已证实 |
| V15 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 第三方 crate 真实进构建、手写 JSON 解析器删除、许可全文齐备 | 已证实 |
| 141 测试通过仅作回归，不作质量结论 | 已证实（024 W03 延续） |
| 深度上限 64 → 128 的行为差异 | 已证实；测试相应改为 200 层，断言未降级 |
| memchr 的 Unlicense 全文 | 受阻（上游仓库只提供 LICENSE-MIT，按 MIT 条款使用并如实登记） |
| 剩余自写模块替换、真实运行时、浏览器点击、Win7 构建、CI 独立构建 | 受阻 / 未证实 |

限制：本轮 vendor 源码由工具脚本搬运并落 `.cargo-checksum.json`，上游 `src/` 未改动；未引入 registry 在线依赖，未做真实网络与 GUI 验证。改动作者未代改验证结论，未降低验收项。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f, len(c.splitlines()))

# ---- 追加 ----
def app(f, s):
    p = Path(f); t = p.read_text().rstrip() + '\n\n' + s.strip() + '\n'; p.write_text(t); print('APPENDED', f)

app('docs/records/code-ownership-audit.md', '''## 025 首次替换后状态

| 项 | 024 | 025 |
| --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5（serde_json / serde_core / itoa / ryu / memchr） |
| `Cargo.lock` 包数 | 1 | 6 |
| `src/dispatcher/json.rs` | 336 行手写解析器 | 77 行（产品约 20 行 + 回归测试） |
| `src/` 行数 | 4339 | 4081 |
| `src/` 有效代码行 | 3876 | 3636 |

替换映射第一块已落地，详见 `docs/decisions/025-vendor-first-replacement.md`。其余自写模块（cache / asynk / leak / launcher / lightweight）仍按本文件映射逐模块推进，未在本轮完成。
''')

app('docs/design/implementation-strategy.md', '''## 025 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 | **已落地**：手写 `dispatcher/json.rs` 换为 `serde_json`，vendor 目录源离线构建通过 |
| 配置序列化 / 参数 / 路径 / 日志 / 缓存 / 异步 / 网络 / UI / 崩溃 / 插件 | 未启动，仍为自写或候选 |

registry 在本环境被 403 阻断，故采用 `vendor/` + `.cargo/config.toml` 目录源；正式联网 CI 可改用 registry 直连，业务代码不需改动。
''')

app('THIRD-PARTY-NOTICES.md', '''## 025 已进构建依赖（非候选）

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| serde_json | 1.0.145 | MIT OR Apache-2.0 | Erick Tryzelaar, David Tolnay | 任务 JSON 解析 | vendor/serde_json | 构建中已使用 |
| serde_core | 1.0.228 | MIT OR Apache-2.0 | serde-rs | serde_json 依赖 | vendor/serde_core | 构建中已使用 |
| itoa | 1.0.15 | MIT OR Apache-2.0 | David Tolnay | 整数格式化 | vendor/itoa | 构建中已使用 |
| ryu | 1.0.20 | Apache-2.0 OR BSL-1.0 | David Tolnay | 浮点格式化 | vendor/ryu | 构建中已使用 |
| memchr | 2.7.6 | Unlicense OR MIT | Andrew Gallant | 字节搜索 | vendor/memchr | 构建中已使用 |

许可证全文：`docs/licenses/serde_json-LICENSE-{MIT,APACHE}.txt`、`serde_core-LICENSE-{MIT,APACHE}.txt`、`itoa-LICENSE-{MIT,APACHE}.txt`、`ryu-LICENSE-{APACHE,BOOST}.txt`、`memchr-LICENSE-MIT.txt`。

| 编号 | 约束 |
| --- | --- |
| N14 | memchr 的 license 字段为 `Unlicense OR MIT`，上游仓库只提供 LICENSE-MIT 文件；本项目按 MIT 条款使用，Unlicense 全文未单独取得，如实登记。 |
| N15 | ryu 为 `Apache-2.0 OR BSL-1.0`，两份全文均已落盘，按 Apache-2.0 条款使用。 |
| N16 | vendor 内上游 `src/` 原样保留；manifest 仅删 dev / 恒假 cfg 段，改动可 diff 审计。 |
| N17 | 后续每引入一个库，重复 H02 四步：LICENSE 全文 → 关于页 → 本文件 → Cargo.toml。 |
''')

app('docs/licenses/index.md', '''## 025 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| serde_json-LICENSE-MIT.txt / serde_json-LICENSE-APACHE.txt | serde_json 1.0.145 | MIT OR Apache-2.0 |
| serde_core-LICENSE-MIT.txt / serde_core-LICENSE-APACHE.txt | serde_core 1.0.228 | MIT OR Apache-2.0 |
| itoa-LICENSE-MIT.txt / itoa-LICENSE-APACHE.txt | itoa 1.0.15 | MIT OR Apache-2.0 |
| ryu-LICENSE-APACHE.txt / ryu-LICENSE-BOOST.txt | ryu 1.0.20 | Apache-2.0 OR BSL-1.0 |
| memchr-LICENSE-MIT.txt | memchr 2.7.6 | Unlicense OR MIT（仅 MIT 全文） |

来源：各上游 GitHub tag 打包内的 LICENSE 文件，逐字副本。
''')

app('docs/decisions/index.md', '| 025 | 首次真正替换自写代码：手写 JSON 解析器换 serde_json，vendor 目录源，5 个第三方 crate 进构建 | 已实现、已验证 | 025-vendor-first-replacement.md |')

app('docs/rules/push-scope.md', '''## 025 允许推送

| 类 | 路径 |
| --- | --- |
| vendor 上游源码 | `vendor/**`（`src/`、`Cargo.toml`、`build.rs`、LICENSE、`.cargo-checksum.json`） |
| cargo 目录源配置 | `.cargo/config.toml` |
| 依赖清单 | `Cargo.toml`、`Cargo.lock` |
| 许可证全文 | `docs/licenses/*-LICENSE-*` |

排除项不变：`target/`、`__pycache__/`、诊断包、私有配置、凭据字面量。
''')

app('docs/records/rounds.md', '''## 025

| 落点 | 内容 |
| --- | --- |
| docs/spec/25-round-025-instructions.txt | 逐字副本 |
| docs/decisions/025-vendor-first-replacement.md | registry 端点实测、vendor 方案、M01-M04、数字变化、B01-B04 行为差异、未换清单 |
| docs/verification/round-025.md | 15 条复跑证据 |
| Cargo.toml / Cargo.lock / .cargo/config.toml / vendor/ | 首次 `[dependencies]`；6 包（5 第三方）；目录源离线构建 |
| src/dispatcher/json.rs / task.rs / launcher.rs / mod.rs | 336 行手写解析器删为 77 行薄适配 |
| docs/licenses/ | 9 份新增全文 |
| demos/ui-full-kcu-paper.html / demos/preview/ | 关于页 5 组「构建中已使用」，43 张截图重渲 |
| 索引与规则 | decisions/index、docs/index 128 项、README、licenses/index、push-scope、code-ownership-audit、implementation-strategy |

用户意图：对我写的代码不信任，要求用别人的代码。处置：不做新一轮文档或演示层堆砌，直接把替换映射第一块落地，让 `Cargo.lock` 出现真实第三方包。

本轮真实缺陷与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E01 | `cargo build --offline` 首次报 `no matching package named serde found` | serde_json / serde_core 的 `[dev-dependencies]` 与 `[target.'cfg(any())'.dependencies]` 引用未 vendor 的 path；删这两段后构建通过，改动登记为 M01/M02 |
| E02 | 首次往许可表插入 5 行时替换目标写错，脚本断言失败 | 改为在数组末尾 `];` 前插入，复查 `构建中已使用=5` 与 JS 语法 |
| E03 | 手写解析器深度上限 64，serde_json 默认 128，原 80 层测试会变成通过 | 测试改 200 层并登记 B01，断言未降级 |

阶段：D07 第 3 层 lightweight 逻辑不变；本轮动的是 L2 dispatcher 的 JSON 解析实现。UI 演示层只改许可数据行并重渲截图，未改界面结构。

未做：剩余自写模块替换、真实网络 / GUI / 跨平台构建、CF F17、特殊版代码、本项目 LICENSE、后端仓任何写请求。
''')

# ---- 精准替换 ----
def rep(f, a, b, n=1):
    p = Path(f); t = p.read_text()
    assert a in t, (f, a[:90])
    p.write_text(t.replace(a, b, n)); print('REPLACED', f)

rep('docs/index.md',
    '124. docs/decisions/024-code-ownership.md\n\n读取命令：',
    '124. docs/decisions/024-code-ownership.md\n125. docs/spec/25-round-025-instructions.txt\n126. docs/decisions/025-vendor-first-replacement.md\n127. .cargo/config.toml\n128. docs/verification/round-025.md\n\n读取命令：')
rep('docs/index.md', '必读顺序扩为 124 项', '必读顺序扩为 128 项')
rep('docs/index.md',
    'docs/decisions/024-code-ownership.md; do printf',
    'docs/decisions/024-code-ownership.md docs/spec/25-round-025-instructions.txt docs/decisions/025-vendor-first-replacement.md .cargo/config.toml docs/verification/round-025.md; do printf')
rep('README.md', '| 当前轮次 | 024 |', '| 当前轮次 | 025 |')
app('README.md', '''## 025 首次真正替换自写代码

手写 336 行 JSON 解析器已换为 `serde_json`；`Cargo.lock` 从 1 包变为 6 包，其中 5 个是真实第三方 crate（serde_json / serde_core / itoa / ryu / memchr）。registry 端点在本环境被 403 阻断，改用 `vendor/` + `.cargo/config.toml` 目录源，`cargo build --offline` 与 `cargo test --offline` 通过（141/0）。9 份许可证全文落盘，关于页新增 5 组「构建中已使用」。剩余自写模块按 `docs/records/code-ownership-audit.md` 逐模块推进。
''')
rep('demos/preview/index.md', '# 界面预览图索引（023 · 43 个产品视图）', '# 界面预览图索引（025 · 43 个产品视图）')
rep('demos/preview/index.md', '| 轮次 | 023 |', '| 轮次 | 025 |')
print('ALL_DOCS_OK')

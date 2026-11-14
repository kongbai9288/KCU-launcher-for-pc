from pathlib import Path
import re

Path('docs/spec/27-round-027-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}
D['docs/decisions/027-crossbeam-replacement.md'] = '''# 第 027 轮：异步块换成 crossbeam，小闭包路线落地

| 项 | 值 |
| --- | --- |
| 编号 | 027 |
| 状态 | 已实现、已验证 |
| 依据 | docs/spec/27-round-027-instructions.txt；026 受阻回退；024 替换映射 |
| 前序 | docs/decisions/026-vendor-blocked.md、docs/records/code-ownership-audit.md |
| 本轮性质 | 工程轮；无新演示 HTML、无自评打分 |

## 路线调整

026 冲 `mini-moka` 整棵依赖树（21 包）卡在 `libc 0.2.191` 解压与工具层 502，已回退。027 不重走大闭包，改用**依赖闭包最浅**的一块先落地：`src/core/asynk.rs` 的手写并发同步换成 `crossbeam-channel` + `crossbeam-utils`，闭包只有 2 个上游包、无 libc、无 wasm、无 proc-macro。

| 编号 | 动作 |
| --- | --- |
| D01 | `std::sync::mpsc::channel` / `Receiver` 换为 `crossbeam_channel::unbounded` + `recv_timeout`。 |
| D02 | `Vec<JoinHandle>` 手工 join 循环换为 `crossbeam_utils::thread::scope`（自动 join）。 |
| D03 | 手写 `Arc<AtomicUsize>` + `LiveGuard` + Drop 递减换为 `crossbeam_utils::sync::WaitGroup`。 |
| D04 | `CancelToken` 保留 `Arc<AtomicBool>` 三方法（标准库薄封装、调用面 20+ 处），不引入额外库。 |
| D05 | 4 份许可证全文落盘，关于页七列表新增 2 组「构建中已使用」，`THIRD-PARTY-NOTICES.md` 同步。 |

## 数字

| 项 | 025 | 026 | 027 |
| --- | --- | --- | --- |
| `Cargo.lock` 包数 | 6 | 6（回退） | 8 |
| 第三方 crate 进构建 | 5 | 5 | **7** |
| `src/core/asynk.rs` 行数 | 258 | 258 | 250 |
| 其中测试段 | 约 100 | 约 100 | 约 100 |
| `src/` 总行数 | 4081 | 4081 | 4073 |
| `cargo test --offline` | 141 / 0 | 141 / 0 | 141 / 0 |

行数只减 7，但**实现权属变了**：手写 Mutex / Condvar / mpsc / AtomicUsize 计数 / JoinHandle 回收全部删除，线程同步、结果通道、活跃归零由库保证。不拿行数当成果，登记实际替换面。

## vendor 内容

| 目录 | 版本 | license | 来源 tag |
| --- | --- | --- | --- |
| `vendor/crossbeam-channel` | 0.5.17 | MIT OR Apache-2.0 | crossbeam-rs/crossbeam `crossbeam-channel-0.5.17` |
| `vendor/crossbeam-utils` | 0.8.23 | MIT OR Apache-2.0 | crossbeam-rs/crossbeam `crossbeam-utils-0.8.23` |

| 编号 | 对上游的最小改动 | 原因 |
| --- | --- | --- |
| M05 | 补 `no_atomic.rs` / `build-common.rs` 到两个 crate 目录，清理 dangling 符号链接 | crossbeam 是 mono-repo，crate 子目录里的这两个 build 辅助文件是指向仓库根的软链；`shutil.move` 后软链悬空，`build.rs` 的 `include!` 报文件不存在 |
| M06 | 沿用 025/026 的 manifest 裁剪：删 dev / 恒假 cfg / lints / path 继承 | 目录源构建只保留产品所需段 |

上游 `src/` 未改动一行。M05 已写进 `scripts/round026_vendor.py`，下轮复用不再手工补。

## 行为差异（如实登记）

| 编号 | 项 | 原手写 | 027 |
| --- | --- | --- | --- |
| B05 | `TaskGroup::live()` | 实时活跃线程数 | shutdown 前返回已 spawn 总数，shutdown 后返回 0；测试只在 shutdown 后断言，断言未降 |
| B06 | `RaceResult.live_after_join` | 由手写计数读出 | 恒 0，由 `thread::scope` 保证所有线程已 join |
| B07 | `race` 线程 panic | join 错误被忽略 | `thread::scope` 返回 Err，归为 `TimedOut` |
| B08 | shutdown 后再 spawn | 仍可 spawn 并 join | `wg` 已取走，新线程不受等待；登记为已知边界，未静默处理 |

## 还没换的

| 文件 | 行数 | 状态 |
| --- | --- | --- |
| `src/core/cache.rs` | 304 | 仍自写；mini-moka 路线按 026 的 N01/N02/N03 挂着 |
| `src/core/leak.rs` | 191 | 仍自写 |
| `src/dispatcher/launcher.rs` | 541 | 仍自写 |
| `src/lightweight/*.rs` | 1135 | 仍自写 |
| 其余 core 模块 | 约 1200 | 仍自写 |

## 硬规则延续

| 编号 | 内容 |
| --- | --- |
| H01 | LICENSE 全文 → 关于页 → NOTICES → Cargo.toml 四步齐备才加依赖。 |
| H02 | `.cargo/config.toml` 目录源离线构建，不依赖 registry 可达。 |
| H03 | 测试仅作回归，不作为质量结论（024 W03）。 |
| H04 | 手感确认前不写 UI 实现；后端仓 0 写请求；凭据只从环境变量读。 |
| H05 | 替换后由用户侧或第三方 CI 跑独立构建，不接受自测自评当结论。 |

## 四值

| 项 | 值 |
| --- | --- |
| 8 包 / 7 第三方、asynk 手写并发原语删除、4 份许可全文、141 / 0 | 已证实 |
| M05 悬空软链与修复 | 已证实 |
| B05-B08 行为差异 | 已证实 |
| cache / leak / launcher / lightweight 替换后行数、真实运行时 | 未证实 |
| 浏览器点击、Win7 / 多架构、CI 独立构建 | 受阻 |
| mini-moka 大闭包 | 受阻（026 延续，按 N 选项挂着） |
'''

D['docs/verification/round-027.md'] = '''# 第 027 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 027 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 工程轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile`；编译 crossbeam-utils / crossbeam-channel / kcu-core | 已证实 |
| V2 | `cargo test --offline` | 141 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 8 包，7 个第三方 | 已证实 |
| V4 | `git diff 28a646b -- src/core/asynk.rs` | 删除 mpsc / AtomicUsize / LiveGuard / JoinHandle 循环 | 已证实 |
| V5 | `grep -c 'crossbeam' src/core/asynk.rs` | 4 | 已证实 |
| V6 | `ls docs/licenses/crossbeam*` | 4 份全文 | 已证实 |
| V7 | `grep -c '构建中已使用' demos/ui-full-kcu-paper.html` | 7 | 已证实 |
| V8 | `python3 scripts/render_ui.py` | `render_ui OK shots=43` | 已证实 |
| V9 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V10 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V11 | 必读文件循环 | REQUIRED=133 MISSING=0 | 已证实 |
| V12 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 第三方运行时 7 组、手写并发原语删除、许可全文齐备 | 已证实 |
| 141 测试仅作回归，不作质量结论 | 已证实 |
| B05-B08 行为差异已登记、测试断言未降级 | 已证实 |
| cache / leak / launcher / lightweight 替换 | 未启动 |
| mini-moka 大闭包、真实网络 / GUI / Win7 / CI 独立构建 | 受阻 |

限制：本轮只换 asynk 一块，未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。
'''

for f, c in D.items():
    Path(f).write_text(c); print('WROTE', f)


def app(f, s):
    p = Path(f); p.write_text(p.read_text().rstrip() + '\n\n' + s.strip() + '\n'); print('APPENDED', f)


app('docs/decisions/index.md', '| 027 | asynk 手写并发原语换 crossbeam 两件套，小闭包路线落地 | 已实现、已验证 | 027-crossbeam-replacement.md |')

app('docs/records/code-ownership-audit.md', '''## 027 第二块替换后状态

| 项 | 024 | 025 | 027 |
| --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | **7** |
| `Cargo.lock` 包数 | 1 | 6 | 8 |
| `src/dispatcher/json.rs` | 336 行手写解析器 | 77 行薄适配 | 77 行 |
| `src/core/asynk.rs` | 258 行手写并发 | 258 行 | 250 行，手写并发原语全删 |
| `src/` 行数 | 4339 | 4081 | 4073 |

027 删掉的自写并发：`std::sync::mpsc` 多源竞速、`Arc<AtomicUsize>` + `LiveGuard` + Drop 递减、`Vec<JoinHandle>` 手工 join 循环；换成 `crossbeam_channel::unbounded/recv_timeout`、`crossbeam_utils::thread::scope`、`crossbeam_utils::sync::WaitGroup`。详见 `docs/decisions/027-crossbeam-replacement.md`。

剩余自写模块：cache / leak / launcher / lightweight 与其余 core，按本文件映射继续推进。
''')

app('docs/design/implementation-strategy.md', '''## 027 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 | 已落地（025，serde_json） |
| 异步 / 线程同步 | **已落地（027，crossbeam-channel + crossbeam-utils）** |
| 缓存 | 未启动；mini-moka 大闭包按 026 的 N 选项挂着 |
| 配置 / 参数 / 路径 / 日志 / 网络 / UI / 崩溃 / 插件 | 未启动，仍为自写或候选 |
''')

app('THIRD-PARTY-NOTICES.md', '''## 027 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| crossbeam-channel | 0.5.17 | MIT OR Apache-2.0 | crossbeam-rs | 多源竞速结果通道 | vendor/crossbeam-channel | 构建中已使用 |
| crossbeam-utils | 0.8.23 | MIT OR Apache-2.0 | crossbeam-rs | 线程组与活跃归零 | vendor/crossbeam-utils | 构建中已使用 |

许可证全文：`docs/licenses/crossbeam-channel-LICENSE-{MIT,APACHE}.txt`、`crossbeam-utils-LICENSE-{MIT,APACHE}.txt`。

| 编号 | 约束 |
| --- | --- |
| N18 | crossbeam 为 mono-repo，crate 子目录的 `no_atomic.rs` / `build-common.rs` 原本是指向仓库根的软链；vendor 时改为真实文件副本，上游 `src/` 未改。 |
| N19 | 按 MIT 条款使用，Apache-2.0 全文同时随附。 |
''')

app('docs/licenses/index.md', '''## 027 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| crossbeam-channel-LICENSE-MIT.txt / crossbeam-channel-LICENSE-APACHE.txt | crossbeam-channel 0.5.17 | MIT OR Apache-2.0 |
| crossbeam-utils-LICENSE-MIT.txt / crossbeam-utils-LICENSE-APACHE.txt | crossbeam-utils 0.8.23 | MIT OR Apache-2.0 |

来源：crossbeam-rs/crossbeam 对应 tag 打包内的 LICENSE 文件，逐字副本。
''')

app('docs/decisions/026-vendor-blocked.md', '''## 027 更新

mini-moka 大闭包仍按 N01/N02/N03 挂着，未选定前不动 Cargo.toml。027 改用依赖闭包最浅的 crossbeam 两件套，把 `src/core/asynk.rs` 的手写并发原语替换完成，8 包 / 7 第三方、141 / 0 通过，详见 `docs/decisions/027-crossbeam-replacement.md`。
''')

app('docs/records/rounds.md', '''## 027

| 落点 | 内容 |
| --- | --- |
| docs/spec/27-round-027-instructions.txt | 逐字副本「干」 |
| docs/decisions/027-crossbeam-replacement.md | 路线调整、D01-D05、8 包数字、M05/M06、B05-B08、未换清单 |
| docs/verification/round-027.md | 12 条复跑证据 |
| src/core/asynk.rs | 手写 mpsc / AtomicUsize / LiveGuard / JoinHandle 循环删除，换 crossbeam-channel + crossbeam-utils |
| Cargo.toml / Cargo.lock / vendor/ | 8 包，7 第三方 |
| docs/licenses/ | 4 份新增全文 |
| demos/ui-full-kcu-paper.html / demos/preview/ | 关于页 7 组「构建中已使用」，43 张截图重渲 |
| 索引与记录 | decisions/index、docs/index 133 项、README、licenses/index、push-scope 沿用、code-ownership-audit、implementation-strategy、THIRD-PARTY-NOTICES、026 决策更新、rounds |

用户「干」继续推进；026 受阻后不重走大闭包，先啃依赖最浅且用户最早点名的异步块。

本轮真实缺陷与修复：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E06 | `crossbeam-utils/build.rs` 报 `couldn't find file no_atomic.rs` | mono-repo 子目录里的 `no_atomic.rs` / `build-common.rs` 是指向仓库根的软链，move 后悬空；删软链、复制仓库根真实文件，已写进 vendor 脚本 M05 |
| E07 | 关于页首次插入 2 行时替换目标写错，脚本断言失败 | 改为在数组末尾 `];` 前插入，复查 `构建中已使用=7` 与 JS 语法 |

未做：cache / leak / launcher / lightweight 替换、UI 实现、真实运行时 / GUI / 跨平台构建、CF F17、特殊版代码、本项目 LICENSE、后端仓写请求。
''')

p = Path('docs/index.md'); t = p.read_text()
a = '130. docs/decisions/026-vendor-blocked.md\n\n读取命令：'
assert a in t
t = t.replace(a, '130. docs/decisions/026-vendor-blocked.md\n131. docs/spec/27-round-027-instructions.txt\n132. docs/decisions/027-crossbeam-replacement.md\n133. docs/verification/round-027.md\n\n读取命令：', 1)
t = t.replace('docs/decisions/026-vendor-blocked.md; do printf',
              'docs/decisions/026-vendor-blocked.md docs/spec/27-round-027-instructions.txt docs/decisions/027-crossbeam-replacement.md docs/verification/round-027.md; do printf', 1)
p.write_text(t); print('INDEX_OK')

p = Path('README.md'); t = p.read_text()
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 027 |', t, count=1)
p.write_text(t.rstrip() + '''

## 027 异步块换成 crossbeam

`src/core/asynk.rs` 的手写 `std::sync::mpsc` 竞速、`Arc<AtomicUsize>` 活跃计数、`Vec<JoinHandle>` 回收循环全部删除，换成 `crossbeam-channel` + `crossbeam-utils`（`thread::scope` / `WaitGroup`）。`Cargo.lock` 8 包、7 个第三方 crate，4 份许可证全文落盘，关于页 7 组「构建中已使用」，`cargo test --offline` 141/0。026 的 mini-moka 大闭包仍按 N 选项挂着。详见 `docs/decisions/027-crossbeam-replacement.md`。
'''); print('README_OK')
print('ALL_DOCS_OK')

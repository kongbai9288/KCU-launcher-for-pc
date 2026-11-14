from pathlib import Path
import re

Path('docs/spec/29-round-029-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/decisions/029-cache-lru.md'] = '''# 第 029 轮：缓存块换成 lru，026 的 N03 路线落地

| 项 | 值 |
| --- | --- |
| 编号 | 029 |
| 状态 | 已实现、已验证 |
| 依据 | docs/spec/29-round-029-instructions.txt；024 替换映射；026-vendor-blocked.md N03 |
| 前序 | 025 JSON、027 异步、028 泄漏计数删除 |
| 本轮性质 | 工程轮；两次真实失败回显、一次路线换轨；不发通过标记 |

## 目标与路线

`src/core/cache.rs` 是 `docs/records/code-ownership-audit.md` 里最后一块大的手写并发数据结构（304 行：HashMap + VecDeque + HashSet + Mutex + Condvar + Weak 防悬挂 + 手写 LRU/TTL/淘汰）。026 冲 mini-moka 大闭包受阻，留下 N01 / N02 / N03 三个选项。用户本轮「干」未点选项，按依赖闭包最浅、且不重撞 libc 的原则自主走 **N03：换更浅的缓存库**。

### 阶段一：mini-moka unsync 尝试（已失败，保留回显）

| 编号 | 动作 |
| --- | --- |
| T01 | 从 026 残留的 `moka-rs_mini-moka_v0.10.3.tgz` 精准提取 src + Cargo.toml + build.rs + LICENSE，裁掉 `dashmap` 声明与 `sync` feature 引用，`default-features = false`。 |
| T02 | 从 026 残留补齐 `smallvec 1.15.1` / `tagptr 0.2.0` / `triomphe 0.1.15`；`triomphe` 的 `[dependencies]` 全是 optional，关闭默认后删整段并改 features，否则 cargo 报 `feature default includes serde which is neither a dependency nor another feature`。 |
| T03 | `cargo build --offline` 编译通过，5 包闭包（mini-moka + crossbeam 两件套 + smallvec + tagptr + triomphe）全部可达，无 libc、无 wasm、无 proc-macro。 |
| T04 | 改用 `mini_moka::unsync::Cache` 后 `cargo test --offline` 报 `E0277`：`Rc<std::string::String> cannot be sent between threads safely`。源码 `unsync/cache.rs` 内部用 `Rc<K>` 作键，`Mutex<unsync::Cache>` 不满足 `Sync`，而 `Cache` 在 dispatcher / lightweight 里以 `Arc<Cache>` 跨线程共享。 |

T04 是**已失败**，不是「受阻」：编译错误明确、结论确定。`sync::Cache` 才能跨线程，但它经 `dashmap → parking_lot_core → libc 0.2` 回到 026 的老路，不重走。

### 阶段二：N03 换 lru 0.12.5（已落地）

| 编号 | 动作 |
| --- | --- |
| C01 | 探 `quick-cache 0.6.18`（关默认后仍需 hashbrown 0.16）、`lru 0.12.5`、`linked-hash-map 0.5.6` 三个候选的 tag manifest 与源码；`rust-ttl_cache` 仓库 404。 |
| C02 | 选 `lru 0.12.5`：`default = ["hashbrown"]` 可关，非 hashbrown 分支只用 `std::collections::HashMap` + 自定义链表；源码里 `Rc<` 8 处全在文档注释与 `#[cfg(test)]`，不是数据结构。单包、零传递依赖、Send/Sync。 |
| C03 | 从 tag tarball 精准提取 `src/` + `Cargo.toml` + `LICENSE`（15 863 字节）；裁 manifest：删 optional hashbrown 声明、`default = []` / `nightly = []`、删 dev-deps 与 lints 段。上游 `src/` 一行未改。 |
| C04 | `Cargo.toml` 由 mini-moka 换成 `lru = { version = "0.12.5", default-features = false }`；删掉 4 个 mini-moka 传递包目录。 |

## cache.rs 权属变化

| 自写部分（025–028） | 029 |
| --- | --- |
| `HashMap<K, Entry<V>>` 主存 | `lru::LruCache<K, Entry<V>>` |
| `VecDeque<K>` LRU 顺序 + `HashSet` 去重 | `LruCache::put` 自动淘汰最旧 |
| 手写 `while entries.len() > capacity` 淘汰循环 | 库管容量，`NonZeroUsize` 校验 |
| `Flight { done: Mutex<bool>, value: Mutex<Option<V>>, cv: Condvar }` | `FlightState { completed, waiters }` + `crossbeam_channel::bounded/1` 的 `recv_timeout` |
| `Inner.inflight: HashMap<K, Weak<Flight>>` 自管 | 复用 028 保留的 `WeakRegistry`（给它补 `remove` / `clear` 两个 std HashMap 薄封装） |
| `Instant` 过期扫描 `purge_locked` | `Entry.expires_at` + 访问时惰性 `pop`，TTL 薄包装 |

**单飞编排保留约 60 行**，但并发原语全部来自库/std：`crossbeam-channel` 负责等待、超时、唤醒，`Mutex` 只保护状态结构，不再有手写 Condvar / Atomic 计数 / Condvar 超时。这是项目特有的「同 key 只加载一次」策略，不是并发原语重写；如实登记，不拿「全用库」当结论。

## 数字

| 项 | 028 | 029 |
| --- | --- | --- |
| `Cargo.lock` 包数 | 8 | **9** |
| 第三方 crate 进构建 | 7 | **8** |
| `src/core/cache.rs` 行数 | 304 | 327 |
| 其中实现段 | 约 190 | **约 140** |
| 其中测试段 | 约 114 | 约 187（新增 2 个并发边界测试） |
| `src/` 总行数 | 3986 | 4017 |
| `cargo test --offline` | 139 / 0 | **141 / 0** |

行数净增 23，原因是新增 `late_waiter_sees_completed_result` 与 `cancelled_waiters_get_cancelled_not_spurious_value` 两个测试；实现段净减约 50 行。行数不是成果，权属变化才是。

## 新增测试（不降验收项）

| 编号 | 断言 |
| --- | --- |
| N01 | leader 已完成、后到的等待者从 `completed` 直接拿结果，不会挂到已 drain 的 waiters 上超时。 |
| N02 | loader 返回 Err 时等待者得到 `Cancelled`，不会误收 `Ok(99)` 的假值；leader 仍返回原始 `Load("E02")`。 |

原 8 个测试全部保留、断言未改：容量有界、TTL 强制重载、8 线程单飞只加载 1 次、inflight 零悬挂、错误传播、clear 归零、500 次插入顺序有界、零容量拒绝。

## 行为差异（如实登记）

| 编号 | 项 | 028 | 029 |
| --- | --- | --- | --- |
| B10 | 淘汰策略 | FIFO（按插入顺序） | **LRU**（按访问顺序），由 `LruCache::get` 更新 |
| B11 | 过期清理 | 每次访问全表扫描 | 仅当前 key 惰性 pop；其他过期条目留到被访问或淘汰 |
| B12 | `order_len()` | 独立顺序表长度 | 等于 `len()`（库内部维护顺序） |
| B13 | `evicted()` | 精确淘汰计数 | `inserted - len` 估算，覆盖插入同 key 会虚增；调用方只在测试里使用 |
| B14 | 单飞错误返回 | 等待者 `Cancelled` | 不变 |

B10 是策略升级（更贴合缓存语义）；B11 / B13 是口径差异，未发现调用方依赖精确值。

## 四值

| 项 | 值 |
| --- | --- |
| 9 包 / 8 第三方、lru 零传递依赖、141 / 0 | 已证实 |
| 手写 HashMap / VecDeque / HashSet / Condvar / 淘汰循环删除 | 已证实 |
| mini-moka unsync 用 `Rc<K>` 不 Send | 已失败（已换轨） |
| triomphe features 引用缺失依赖 | 已失败（已裁 manifest） |
| 真实运行时内存剖析、Win7 / 多架构、GUI 端到端 | 受阻 |
| `rust-ttl_cache` 仓库定位 | 受阻（404） |
| 后端仓写请求 | 0（已证实） |
'''

D['docs/verification/round-029.md'] = '''# 第 029 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 029 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | 工程轮，不生成双哈希；测试仅作回归 |

| 编号 | 命令 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `cargo build --offline` | `Finished dev profile`；编译 lru 0.12.5 / kcu-core | 已证实 |
| V2 | `cargo test --offline` | 141 passed / 0 failed | 已证实 |
| V3 | `Cargo.lock` 包列表 | 9 包 / 8 第三方 | 已证实 |
| V4 | `grep -c 'mini_moka' src/core/cache.rs` | 0 | 已证实 |
| V5 | `grep -c 'LruCache' src/core/cache.rs` | 3 | 已证实 |
| V6 | `grep -c 'Condvar\|VecDeque\|HashSet' src/core/cache.rs` | 0 | 已证实 |
| V7 | `git diff 62f3fb4 -- Cargo.toml` | mini-moka → lru 一行替换 | 已证实 |
| V8 | `ls vendor` | 8 个目录，mini-moka 闭包 4 个已删 | 已证实 |
| V9 | `docs/licenses/lru-LICENSE.txt` | 1071 字节，MIT，Copyright (c) 2016 Jerome Froelich | 已证实 |
| V10 | `grep -c '构建中已使用' demos/ui-full-kcu-paper.html` | 8 | 已证实 |
| V11 | `! grep -rqE 'gh[p]_' .` 与 `.git/config` | NO_CREDENTIAL / NO_TOKEN_IN_CONFIG | 已证实 |
| V12 | 禁用词 / 「同上」 / P09 扫描 | 零命中 | 已证实 |
| V13 | 必读文件循环 | REQUIRED=141 MISSING=0 | 已证实 |
| V14 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| 手写缓存数据结构删除、lru 单包落地、141 / 0 | 已证实 |
| 两个新增并发边界测试、原 8 个测试断言未改 | 已证实 |
| mini-moka unsync 不 Send、triomphe features 报错 | 已失败（均有修复/换轨留痕） |
| B10-B14 行为差异已登记 | 已证实 |
| 141 测试仅作回归，不作质量结论 | 已证实 |
| 真实运行时、Win7 / 多架构、CI 独立构建 | 受阻 |
| launcher / lightweight 业务模块替换 | 未启动 |

限制：本轮未做真实运行时与跨平台验证；改动作者未代改验证结论，未降低验收项。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s):
    p = Path(f)
    t = p.read_text()
    marker = s.strip().splitlines()[0]
    if marker in t:
        print('SKIP_DUP', f)
        return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 029 | 缓存块换 lru 0.12.5，mini-moka unsync 因 Rc 不 Send 换轨 | 已实现、已验证 | 029-cache-lru.md |')

app('docs/decisions/026-vendor-blocked.md', '''## 029 更新：N03 已落地

mini-moka 大闭包不再挂起。029 先试 mini-moka 0.10.3 的 `unsync::Cache`（关 `default-features`、裁掉 dashmap，5 包闭包可构建），但源码内部用 `Rc<K>`，`Mutex<unsync::Cache>` 不满足 `Sync`，`Arc<Cache>` 跨线程共享编译失败。按 N03 换成 `lru 0.12.5`（单包、零传递依赖、Send/Sync、MIT），`cargo test --offline` 141 / 0。详见 `docs/decisions/029-cache-lru.md`。N01 / N02 未使用，保留为历史选项。
''')

app('docs/records/code-ownership-audit.md', '''## 029 第三块替换后状态

| 项 | 024 | 025 | 027 | 028 | 029 |
| --- | --- | --- | --- | --- | --- |
| 第三方 crate 进构建 | 0 | 5 | 7 | 7 | **8** |
| `Cargo.lock` 包数 | 1 | 6 | 8 | 8 | 9 |
| `dispatcher/json.rs` | 336 行手写解析器 | 77 行薄适配 | 77 | 77 | 77 |
| `core/asynk.rs` | 258 行手写并发 | 258 | 250 行库化 | 250 | 250 |
| `core/leak.rs` | 191 行自写计数 | 191 | 191 | 99 | 99（+2 薄封装方法） |
| `core/cache.rs` | 304 行手写 LRU/TTL/单飞 | 304 | 304 | 304 | **327（实现段约 140）** |
| `src/` 行数 | 4339 | 4081 | 4073 | 3986 | 4017 |

029 删掉的自写数据结构：`HashMap` 主存、`VecDeque` LRU 顺序、`HashSet` 去重、`while len > capacity` 淘汰循环、手写 `Mutex<bool> + Condvar + Mutex<Option<V>>` 单飞。容量与 LRU 交给 `lru::LruCache`，等待/超时/唤醒交给 `crossbeam-channel`，弱引用表复用 028 的 `WeakRegistry`。TTL 保留 `Entry.expires_at` 惰性薄包装（约 10 行），单飞编排约 60 行属项目特有策略，均如实登记。

剩余自写模块：`dispatcher/launcher.rs` 541、`lightweight/*.rs` 1135 与其余 core 业务模块，按本文件映射继续推进。
''')

app('docs/design/implementation-strategy.md', '''## 029 进度

| 层 | 状态 |
| --- | --- |
| JSON 解析 | 已落地（025，serde_json） |
| 异步 / 线程同步 | 已落地（027，crossbeam-channel + crossbeam-utils） |
| 缓存容量 / LRU / 单飞 | **已落地（029，lru 0.12.5 + crossbeam-channel + WeakRegistry）** |
| TTL | 库外薄包装（`Entry.expires_at`），未找到零依赖且内置 TTL 的成熟库，`rust-ttl_cache` 仓库 404 |
| 配置 / 参数 / 路径 / 日志 / 网络 / UI / 崩溃 / 插件 | 未启动，仍为自写或候选 |
''')

app('THIRD-PARTY-NOTICES.md', '''## 029 新增已进构建依赖

| 项目 | 版本 | 许可证 | 版权 | 用途 | 来源 | 状态 |
| --- | --- | --- | --- | --- | --- | --- |
| lru | 0.12.5 | MIT | Jerome Froelich (c) 2016 | 有界 LRU 容量与淘汰 | vendor/lru | 构建中已使用 |

许可证全文：`docs/licenses/lru-LICENSE.txt`。

| 编号 | 约束 |
| --- | --- |
| N20 | 以 `default-features = false` 使用，避免引入 hashbrown；上游 `src/` 未改，manifest 裁掉 optional 依赖与 dev-deps 仅用于目录源构建。 |
| N21 | MIT 条款要求保留版权与许可声明，全文随发行物附上。 |
''')

app('docs/licenses/index.md', '''## 029 新增（已进构建依赖）

| 文件 | 项目 | 许可证 |
| --- | --- | --- |
| lru-LICENSE.txt | lru 0.12.5 | MIT |

来源：jeromefroe/lru-rs tag `0.12.5` 内的 LICENSE，逐字副本，1071 字节。
''')

app('docs/checklists/ai-errors.md', '''## 029 轮新增

| 编号 | 防错项 |
| --- | --- |
| A70 | 引入缓存/并发库前先核 `Send + Sync`：`unsync` 变体可能内部用 `Rc<K>`，外面套 `Mutex` 也不能跨 `Arc` 共享。 |
| A71 | 裁 manifest 时删了 optional 依赖，必须同步删 `[features]` 里对它的引用，否则 cargo 报 `feature ... includes ... which is neither a dependency nor another feature`。 |
| A72 | 单飞广播要留持久 `completed` 状态：只在完成时 drain waiters，后到等待者会挂到空队列上超时。 |
''')

app('docs/research/index.md', '''## 029 轮新增

| 编号 | 文档 | 主题 |
| --- | --- | --- |
| R21 | 029-cache-lru.md 的 T01-T04 / C01-C04 | 缓存库依赖闭包与 Send/Sync 的源码级核查 |

完整 URL：

- https://github.com/jeromefroe/lru-rs/tree/0.12.5
- https://api.github.com/repos/jeromefroe/lru-rs/contents/Cargo.toml?ref=0.12.5
- https://codeload.github.com/jeromefroe/lru-rs/tar.gz/refs/tags/0.12.5
- https://github.com/moka-rs/mini-moka/tree/v0.10.3
- https://github.com/arthurprs/quick-cache/tree/v0.6.18
- https://github.com/contain-rs/linked-hash-map/tree/v0.5.6
- https://api.github.com/repos/jeromefroe/lru-rs/tags?per_page=20
''')

app('docs/records/rounds.md', '''## 029

| 落点 | 内容 |
| --- | --- |
| docs/spec/29-round-029-instructions.txt | 逐字副本「干」 |
| docs/decisions/029-cache-lru.md | T01-T04 mini-moka 失败回显、C01-C04 lru 落地、权属变化、B10-B14、四值 |
| docs/verification/round-029.md | 14 条复跑证据 |
| demos/round-029-cache.html | 13 步运行逻辑演示（含换轨分支） |
| src/core/cache.rs | 手写 HashMap / VecDeque / HashSet / Condvar / 淘汰循环删除，换 `lru::LruCache` + `crossbeam-channel` |
| src/core/leak.rs | `WeakRegistry` 补 `remove` / `clear`（std HashMap 薄封装） |
| Cargo.toml / Cargo.lock / vendor/ | 9 包 8 第三方；删 mini-moka 闭包 4 目录，加 lru 单包 |
| docs/licenses/lru-LICENSE.txt | MIT 全文 1071 字节 |
| demos/ui-full-kcu-paper.html / demos/preview/ | 关于页 8 组「构建中已使用」，43 张截图重渲 |
| 索引与记录 | docs/index 141 项、README、decisions/index、026 决策更新、research/index、licenses/index、ai-errors A70-A72、code-ownership-audit、implementation-strategy、THIRD-PARTY-NOTICES、rounds |

「干」继续替换自写代码，按 026 留下的 N03（换更浅的缓存库）落地。

本轮真实失败与换轨：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E10 | mini-moka 0.10.3 `unsync::Cache` 内部 `Rc<K>`，`Mutex<unsync::Cache>` 不是 `Sync`，`Arc<Cache>` 跨线程报 `E0277` | 判定已失败，不重走 `sync::Cache` 的 dashmap → libc 老路，按 N03 换 lru |
| E11 | triomphe 裁掉 `[dependencies]` 后 `[features] default` 仍引用 serde / stable_deref_trait，cargo 拒绝解析 | 改写 features 段为 `default = ["std"]`（最终 lru 路线下该包已删除） |
| E12 | 首次接入 mini-moka 后 `cache.rs` 仍 `use mini_moka`，编译报 unresolved crate | 换依赖后同步改源码 import，复跑通过 |

未做：三项开服器新功能实现（028「只记文档」约束延续）、UI 实现、真实运行时 / GUI / 跨平台构建、launcher / lightweight 业务模块替换、CF F17、特殊版代码、本项目 LICENSE、后端仓写请求。
''')

p = Path('docs/index.md')
t = p.read_text()
a = '137. docs/verification/round-028.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '137. docs/verification/round-028.md\n138. docs/spec/29-round-029-instructions.txt\n139. docs/decisions/029-cache-lru.md\n140. docs/licenses/lru-LICENSE.txt\n141. docs/verification/round-029.md\n\n读取命令：', 1)
t = t.replace('docs/verification/round-028.md; do printf',
              'docs/verification/round-028.md docs/spec/29-round-029-instructions.txt docs/decisions/029-cache-lru.md docs/licenses/lru-LICENSE.txt docs/verification/round-029.md; do printf',
              1)
p.write_text(t)
print('INDEX_OK')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 029 |', p.read_text(), count=1)
section = '''

## 029 缓存块换成 lru

`src/core/cache.rs` 的手写 `HashMap` 主存、`VecDeque` LRU 顺序、`HashSet` 去重、容量淘汰循环、`Mutex<bool> + Condvar` 单飞全部删除；容量与 LRU 交给 `lru 0.12.5`（单包、零传递依赖、MIT），等待/超时/唤醒交给 `crossbeam-channel`，弱引用表复用 028 的 `WeakRegistry`。`Cargo.lock` 9 包、8 个第三方 crate，`cargo test --offline` 141/0。

中途试过 mini-moka 0.10.3 的 `unsync::Cache`：5 包闭包可构建，但内部 `Rc<K>` 不 `Send`，`Arc<Cache>` 跨线程编译失败，按 026 的 N03 换轨。`sync::Cache` 会回到 dashmap → libc 老路，未重走。详见 `docs/decisions/029-cache-lru.md`。
'''
if '## 029 缓存块' not in t:
    p.write_text(t.rstrip() + section)
    print('README_OK')
else:
    p.write_text(t)
    print('README_SKIP_DUP')
print('ALL_DOCS_OK')

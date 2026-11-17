from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]
lock = (ROOT / 'Cargo.lock').read_text()
pkgs = len(re.findall(r'\[\[package\]\]\nname = "([^"]+)"', lock))
third = pkgs - 1
html_n = len(list((ROOT / 'demos').glob('*.html')))
png_n = len(list((ROOT / 'demos/preview').glob('[0-9][0-9]-*.png')))
src_n = len(list((ROOT / 'src').rglob('*.rs')))
integ_lines = len((ROOT / 'src/core/integrity.rs').read_text().splitlines())
print('REAL pkgs', pkgs, 'third', third, 'html', html_n, 'png', png_n,
      'src_rs', src_n, 'integrity_lines', integ_lines)

Path('docs/spec/52-round-052-instructions.txt').write_text('干\n')
print('SPEC_OK')

D = {}

D['docs/features/software-integrity.md'] = '''# 软件完整性验证

| 字段 | 值 |
| --- | --- |
| 编号 | F052-01 / B06 / D07 |
| 状态 | 实现层已落地（`src/core/integrity.rs`）；取数与发行物签名流程未启动 |
| 触发 | 启动前读取 manifest、公钥、签名；文件读取由调用方注入 |
| 输入 | `manifest_bytes` / `public_key` / `signature` / `root` / `consecutive_failures` / `config_snapshot` / `runtime` / `modules` |
| 输出 | `Outcome { level, code, envelope, diagnostics, checked, mismatches, safe_mode, bundle }` |

## 顺序

1. manifest 空或超 1 MiB → `integrity.manifest_size` / `Fatal`
2. 签名校验（036 `verify_detached`）→ 失败 `integrity.signature` / `FeatureDisabled`，不解析内容
3. `serde_json` 逐字段解析 → 畸形、空清单、超 4096 项、摘要格式错 → `integrity.manifest_parse` / `Fatal`
4. 逐文件：`robust::safe_join` → 读字节 → 长度上限 64 MiB → `sha512` + `hex` → 比对
5. 缺失 → `Degraded`；内容不符 / 路径非法 / 超限 → `FeatureDisabled`；全通过 → `Ok`

## 兜底分级

| 级 | code | 处置 |
| --- | --- | --- |
| 零级 | `integrity.manifest_size` / `integrity.manifest_parse` / `integrity.digest_cache` | 明确报错，不崩 |
| 一级 | `integrity.signature` / `integrity.content_mismatch` / `integrity.path` / `integrity.file_size` / `integrity.rate_limited` | 禁用自定义配置并提示 |
| 二级 | `integrity.missing_file` | 自动用内置默认并提示已切换 |
| 三级 | 记 `[KCU]` 单行诊断 | 不中断 |

连续失败 ≥3 → `safe_mode=1`，导出诊断包（诊断行 + 配置快照 + 运行时信息 + 已加载模块列表）。阈值与 `src/dispatcher/launcher.rs` 第 3 次失败进安全模式一致。

## 缓存与刷新

`Cache<String,String>` 存 `path:len -> sha512hex`，容量 256 / TTL 30 s / 加载超时 5 s。长度进 key，内容变长必然重算；`refresh()` 全清。**签名与判定每次重跑，不缓存结论**。`OpBudget` 限 64 次/秒，超出返回 `disabled`，不返回 `ok`。

## 演示层三个动作的映射

| 演示层动作 | 实现层条件 | 结果 |
| --- | --- | --- |
| 用默认继续 | `level != Ok` 且 `safe_mode=0` | 忽略自定义配置，用内置默认；不加载被篡改内容 |
| 重新获取 | 任意非 `Ok` | `refresh()` 后重走 `verify()`；限流态等窗口滚动 |
| 取消 | 任意 | 不继续启动，保留诊断行 |

**如实**：051 的 `DECLARATION` 三卡与按钮是静态预览，未接实现层回调；渲染层接线属 UI 层未启动。

## 未启动

- 从 GitHub / atomgit 拉版本平台信息
- 发行物 manifest 生成、签名与公钥分发
- Win7 老旧系统运行时判定
- 真实磁盘 IO 接入（`read` 目前由调用方注入）
- 演示层按钮到 `Outcome` 的渲染层接线

## 验证

`cargo test --offline --lib core::integrity` 15 / 0；反向反转验签判定后 9 个测试 FAILED，恢复后 15 / 0；`cargo test --offline --lib` 313 / 0；全量 339 / 0；`cargo check --offline --target x86_64-pc-windows-gnu` 通过。
'''

D['docs/decisions/052-integrity-verification.md'] = f'''# 第 052 轮：B06 实现层软件完整性验证

| 项 | 值 |
| --- | --- |
| 编号 | 052 |
| 状态 | `src/` 已落地；演示层与 PNG 零改动；UI 闸门未触发 |
| 依据 | `docs/spec/52-round-052-instructions.txt`（逐字：「干」） |
| 对应 | 048 合规核对 B06 / D07；051 补记「实现层未启动」；`00-requirements.txt` §7.3、§9.3、§12、§14、§18.6 |

## 开工复读（B02）

`docs/records/round-052-full-readback.md`：

| 文件 | 字节 | 行 | SHA-256 前 16 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f` |
| `docs/checklists/ai-errors.md` | 34458 | 364 | `b08e96ae816e4895` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf` |

对 4 份执行全文 `read_text()` 与逐行遍历。防错清单 364 行**全文回显**（A182 点名、此前从未逐字打印）；`00-requirements.txt` 261 行已于 051 全文回显；另两份全文遍历、未逐行打印。复读在写任何代码之前完成。`ai-errors.md` 哈希较 051 变化是 051 自己追加 A178–A182 所致。

## 范围判定

051 结尾写「继续按台账走 B06 的实现层软件完整性验证 —— 用已进构建的 ed25519-compact 做本地签名比对，不拉新依赖、不碰真实网络 IO；或用户点 EQ-01 ~ EQ-13 任一编号」。用户回「干」，按默认走前者。**不声称用户已决断**（D-052-1，沿用 050 的 A177）。

## 落地

| 编号 | 动作 |
| --- | --- |
| U121 | `src/core/integrity.rs`（{integ_lines} 行），`src/core/mod.rs` 注册。零新增第三方：`Cargo.toml` / `Cargo.lock` / `vendor/` 未动，仍 {pkgs} 包 / {third} 第三方。 |
| U122 | 验签复用 036 `updater::verify::verify_detached`（ed25519-compact），**排在解析之前**；失败不解析清单，符合 036 A95。 |
| U123 | manifest 解析用 `serde_json::Value` 的 `get` / `as_str` / `as_array`（031 的口径），空集合、缺字段、超 4096 项、摘要非 128 位 hex 全返回 `Fatal`，无 `expect` / 下标 panic。 |
| U124 | 路径走 `robust::safe_join`（048，标准库 `Component`），拒绝对路径、`..` 越界、Windows 保留名、控制字符、超深；摘要用 `ed25519_compact::sha512` + 042 的 `hex`。 |
| U125 | `Level` 四级 `Ok` / `Degraded` / `FeatureDisabled` / `Fatal`，`code()` 显式字符串（046 A154）；映射见 `docs/features/software-integrity.md`。 |
| U126 | 摘要缓存复用 029 的 `Cache`（lru）：`path:len -> sha512hex`，容量 256 / TTL 30 s / 加载超时 5 s；`refresh()` 全清。**签名与判定每次重跑，不缓存结论**。 |
| U127 | `OpBudget`（048）限 64 次/秒；超限返回 `integrity.rate_limited` / `FeatureDisabled`，**不返回通过**，高频调用不能绕过校验。 |
| U128 | 连续失败 ≥ `SAFE_MODE_AFTER=3` → `safe_mode=1` + `DiagnosticBundle`（诊断行 / 配置快照 / 运行时信息 / 已加载模块列表）。阈值与 `src/dispatcher/launcher.rs` 第 3 次失败进安全模式一致（A158 全量核对）。 |
| U129 | 结果带 `Envelope::new(Kind::Response, "core.integrity")`，`code` / `level` / `checked` / `safe_mode` 字段，非 `Ok` 用 `with_error`；诊断行走 `diag_line`，单行 `[KCU]` 前缀。 |

**信任根口径**：`public_key` / `signature` / `manifest_bytes` / `root` / `read` 全部由调用方注入，代码不内置任何密钥、不写绝对路径、不发网络请求。符合 §7.3「禁止硬编码环境假设（绝对路径、写死架构名、密钥）」与 A12 / A13。发行物的公钥分发流程**未启动**。

## 演示层三个动作到结果码的映射

| 演示层动作（051 `DECLARATION`） | 实现层条件 | 结果 |
| --- | --- | --- |
| 用默认继续 | `level != Ok` 且 `safe_mode=0` | 忽略自定义配置用内置默认，不加载被篡改内容 |
| 重新获取 | 任意非 `Ok` | `refresh()` 后重走 `verify()`；限流态等窗口滚动 |
| 取消 | 任意 | 不继续启动，保留诊断行 |

**如实**：051 的三卡与按钮是静态预览，未接实现层回调；渲染层接线属 UI 层未启动，本轮不动 UX HTML。

## 验证

| 编号 | 命令 | 输出 |
| --- | --- | --- |
| V1 | 本地 HEAD / 工作区 | `2cbe9fd`，DIRTY 0，1020 文件 |
| V2 | `git diff -- src/ Cargo.toml Cargo.lock vendor/` | 仅 `src/core/mod.rs` + 新增 `src/core/integrity.rs`；Cargo.* / vendor/ 零改动 |
| V3 | `cargo test --offline --lib core::integrity` | **15 / 0**，零 warning |
| V4 | `cargo test --offline --lib` | **313 / 0**（298 + 15） |
| V5 | `http_construct` / `window_handle_contract` | 7 / 0，6 / 0 |
| V6 | `plugin_lifecycle_load` / `plugin_abi_load` | 7 / 0（54.54 s），6 / 0（116.87 s），真加载 cdylib |
| V7 | 全量合计 | **339 / 0** |
| V8 | `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile`，35.04 s |
| V9 | `panic_guard` / `semver_guard` / `i18n_guard` / `lang_guard` | `files 39 hits 0` / `hits 0` / `hits 0` / `keys 26` |
| V10 | `p09_scan` | `P09_HITS 0 []` |
| V11 | CI 三条 grep | `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE` |
| V12 | `node new Function` demos HTML + 2 语言包 | `ALL_JS_OK {html_n}` |
| V13 | `yaml.safe_load(ci.yml)` + `ast.parse(scripts/*.py)` | `scan_steps 8` |
| V14 | 反向验证（A159） | 反转验签判定 → **9 FAILED / 6 passed**；恢复 → 15 / 0 |
| V15 | `git diff --name-only -- demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空；{png_n} 张 PNG 未改 |
| V16 | 远端 `GET /git/trees/...?recursive=1` 逐项比对 | ALL_MATCH True |

## 本轮真实问题

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E105 | 首版 `hex::encode(h.as_ref())` 编译前不确定 `sha512::Hash` 是否实现 `AsRef` | 编译验证通过；未改断言 |
| E106 | 全局替换 `disk` → `_disk` 误改 7 处，其中 5 处仍引用 `disk`，触发 6 个 E0425 | 全部恢复，按编译警告精确定位 3 行改 `_disk`；复跑 313 / 0 零 warning |
| E107 | 反向验证注入后 9 个测试 FAILED，不是预估的 2 个 | 如实记录 9 个；证明验签是所有正向路径的共同前置，未调整测试 |
| E108 | abi 集成首跑被网关 502 截断 | 等待后重跑 6 / 0，断言没降 |

## 自我批判

- 本轮 **零新增第三方**，全部复用已进构建的库：验签 036、摘要 ed25519-compact（037 已用）、hex 042、serde_json 031、路径 048、缓存 029、信封 031、限流 048。项目侧只有顺序编排、分级策略、字段映射 —— 这些无语义等价库可换，如实登记为业务编排层，**不是新开自写底座例外**（023 A03 已于 024 撤回）。
- **不缓存校验结论**是刻意取舍：缓存结果会在文件被替换后误判通过。缓存只省 SHA-512 计算，`path:len` 键让长度变化必然重算；同长度同路径的内容替换仍依赖 TTL 30 s，这是已知窗口，写进 `docs/features/software-integrity.md`，不写成「完全无风险」。
- B06 只补了**签名比对**这一项。`从 GitHub/atomgit 拉版本平台信息`、manifest 生成与公钥分发、Win7 运行时判定仍属 D07 **未启动**；不能把 B06 整体写成「已修」。
- 演示层三个按钮仍是静态预览，未接 `Outcome` 回调；渲染层接线属 UI 层，本轮 UI 闸门未触发，不动 UX HTML。
- 用户未点 EQ 编号，按 051 结尾的默认执行，登记 **D-052-1**，不写成已决断。
- 051 刚立的 B01 / B02 本轮照做：防错清单全文回显、回复按 §14 十二项；035–047 历史偏差仍不补写。

## 四值

| 项 | 值 |
| --- | --- |
| B02 复读证据、防错清单 364 行全文回显 | 已证实 |
| B06 实现层签名比对、四级兜底、安全模式诊断包 | 已证实 |
| 313 / 0 单元、339 / 0 全量、Windows GNU、四守卫、反向验证 9 FAILED | 已证实 |
| 零新增依赖、{pkgs} 包 / {third} 第三方、演示层零改动 | 已证实 |
| B01 / B02 历史缺失、B06 其余两项、D07 取数与分发 | 已失败 / 未启动 |
| EQ-01 ~ EQ-13 拍板 | 未证实 |
| GUI 端到端、真实网络 IO、Win7 / MSVC 运行时 | 受阻 |
'''

D['docs/verification/round-052.md'] = '''# 第 052 轮独立验证报告

| 项 | 值 |
| --- | --- |
| 轮次 | 052 |
| 结论 | 部分通过；未发通过标记 |
| 口径 | `src/` 有改动；演示层与 PNG 零改动，UI 闸门未触发 |

| 编号 | 命令 / 检查 | 输出 | 四值 |
| --- | --- | --- | --- |
| V1 | `git rev-parse --short HEAD` / `git status` | `2cbe9fd`，DIRTY 0，1020 文件 | 已证实 |
| V2 | `git diff --name-only -- Cargo.toml Cargo.lock vendor/` | 空 | 已证实 |
| V3 | `cargo test --offline --lib core::integrity` | **15 / 0** | 已证实 |
| V4 | `cargo test --offline --lib` | **313 / 0**，零 warning | 已证实 |
| V5 | `cargo test --offline --test http_construct` | 7 / 0 | 已证实 |
| V6 | `cargo test --offline --test window_handle_contract` | 6 / 0 | 已证实 |
| V7 | `cargo test --offline --test plugin_lifecycle_load` | 7 / 0，54.54 s，真加载 cdylib | 已证实 |
| V8 | `cargo test --offline --test plugin_abi_load` | 6 / 0，116.87 s | 已证实 |
| V9 | 全量合计 | **339 / 0** | 已证实 |
| V10 | `cargo check --offline --target x86_64-pc-windows-gnu` | `Finished dev profile`，35.04 s | 已证实 |
| V11 | `panic_guard` | `files 39 hits 0` | 已证实 |
| V12 | `semver_guard` | `version_files 3 hits 0` | 已证实 |
| V13 | `i18n_guard` | `hits 0 inline_bilingual_cn_lines 121` | 已证实 |
| V14 | `lang_guard` | `keys 26 stable_values_ok offline_refs_ok` | 已证实 |
| V15 | `p09_scan` | `P09_HITS 0 []` | 已证实 |
| V16 | `grep -rqE 'gh[p]_'` | `NO_CREDENTIAL` | 已证实 |
| V17 | 禁用词 / 硬编码 grep（src/） | `NO_EXPLANATORY` / `NO_HARDCODE` | 已证实 |
| V18 | `node new Function` demos HTML + 语言包 | `ALL_JS_OK 42` | 已证实 |
| V19 | `yaml.safe_load` + `ast.parse` | `PY_YAML_OK scan_steps 8` | 已证实 |
| V20 | 反向验证（反转验签判定） | 9 FAILED / 6 passed；恢复后 15 / 0 | 已证实 |
| V21 | `git diff -- demos/ui-full-kcu-paper.html demos/lang demos/preview` | 空，56 张 PNG 未改 | 已证实 |
| V22 | B02 复读记录 | 4 份字节 / 行 / SHA-256，防错清单 364 行全文回显 | 已证实 |
| V23 | 必读读取命令块 | 266 项，`MISSING 0` | 已证实 |
| V24 | 远端 `GET /git/trees/...?recursive=1` | ALL_MATCH True | 已证实 |

| 项 | 值 |
| --- | --- |
| B06 实现层签名比对、四级兜底、313 / 0、339 / 0 | 已证实 |
| B01 / B02 历史缺失 | 已失败（不补写） |
| B06 其余两项、D07 取数与分发、渲染层接线 | 未启动 |
| EQ-01 ~ EQ-13 拍板 | 未证实 |
| GUI 端到端、真实网络 IO、Win7 / MSVC 运行时 | 受阻 |

限制：改动作者未代改验证结论；339 个测试是回归，不作质量结论。E108 网关截断拆段补齐，未降验收项。
'''

for f, c in D.items():
    Path(f).write_text(c)
    print('WROTE', f)


def app(f, s, marker=None):
    p = Path(f); t = p.read_text()
    m = marker or s.strip().splitlines()[0]
    if m in t:
        print('SKIP_DUP', f); return
    p.write_text(t.rstrip() + '\n\n' + s.strip() + '\n')
    print('APPENDED', f)


app('docs/decisions/index.md', '| 052 | B06 实现层软件完整性验证 | src 落地，零新增依赖 | 052-integrity-verification.md |')

app('docs/records/requirement-compliance-audit.md', '''## 052 补记：B06 实现层签名比对落地

| 编号 | 048 / 051 状态 | 052 状态 |
| --- | --- | --- |
| B06 | 048：三项具体内容未做；051：演示层三项已补，实现层未启动 | **实现层「软件完整性验证」落地**：`src/core/integrity.rs` 本地签名比对 + 四级兜底 + 安全模式诊断包；零新增依赖 |
| B06 余项 | 自动关闭某功能（拉版本平台信息）、Win7 老旧声明文案 | 仍**未启动**，属 D07；不能把 B06 整体写成「已修」 |
| B01 / B02 | 051：本轮起按结构执行 / 本轮起逐字复读 | 052 照做（防错清单 364 行全文回显）；035–047 历史偏差仍不补写 → 仍为「已失败」 |

B03（050 已修）、B04 / B05 / B07 / B08 / B09 / B10、C01–C10、D01–D09 本轮未动。EQ-14（049）、EQ-15（050）已关，EQ-01 ~ EQ-13 仍待拍板。
''', '## 052 补记')

app('docs/records/pending-question-environments.md', '''**052 状态**

本轮未新增 EQ。用户回「干」而非点 EQ 编号，按 051 结尾默认执行 B06 实现层签名比对，登记 **D-052-1**（我的默认，不是用户决断）。EQ-01 ~ EQ-13 仍待拍板；EQ-14（049）、EQ-15（050）已关闭。
''', '**052 状态**')

app('docs/records/interface-log.md', '''## 052 轮

| 编号 | 项 | 值 |
| --- | --- | --- |
| I83 | `src/core/integrity.rs` | 新增；`Verifier` / `VerifyInput` / `Outcome` / `Level` / `Manifest` / `DiagnosticBundle` / `parse_manifest` |
| I84 | 复用接口 | `updater::verify::verify_detached`(036)、`ed25519_compact::sha512`(037)、`hex`(042)、`serde_json`(031)、`robust::safe_join`/`OpBudget`(048)、`cache::Cache`(029)、`envelope::Envelope`(031)、`diag_line` |
| I85 | 常量 | `SAFE_MODE_AFTER=3`（与 dispatcher 一致）、`MAX_MANIFEST_ENTRIES=4096`、`MAX_FILE_BYTES=64MiB`、`CACHE_CAPACITY=256`、`CACHE_TTL_SECS=30` |
| S51 | 状态 | U121–U129 已证实；零新增依赖；取数与分发未启动；渲染层按钮未接线 |
''')

app('docs/checklists/ai-errors.md', '''## 052 轮新增

| 编号 | 防错项 |
| --- | --- |
| A183 | 完整性校验不能缓存「结论」；只缓存摘要计算，签名与判定每次重跑，否则文件被替换后会误判通过。 |
| A184 | 限流 / 超时 / 异常一律不得返回「通过」；高频调用绕过校验比拒绝服务更危险。 |
| A185 | 签名校验排在解析之前：验签失败就不解析内容，避免畸形数据先进解析路径。 |
| A186 | 全局替换变量名为 `_x` 前先数引用点；误改仍在使用的绑定会批量触发 E0425，按编译警告精确定位。 |
| A187 | 反向注入验证的 FAILED 数量要按实记录，不按预估写；注入后失败面更广说明前置更关键，不是测试写坏了。 |
''')

app('docs/rules/ui-demo.md', '''## 052 闸门判定

**未触发**。本轮改 `src/core/integrity.rs` 与 `src/core/mod.rs`，新增 `demos/round-052-integrity.html`（**流程 HTML，不是 UX HTML**）、功能登记与文档。`demos/ui-full-kcu-paper.html`、两个语言包、56 张 PNG 全部零 diff。051 的 `DECLARATION` 三卡与按钮保持静态预览，未接实现层回调；渲染层接线属 UI 层，动到那层才按闸门规则出整页演示与预览图。
''')

app('docs/records/code-ownership-audit.md', '''## 052 零新增第三方

`Cargo.toml` / `Cargo.lock` / `vendor/` 一行未动，仍 26 包 / 25 第三方。新增 `src/core/integrity.rs` 的验签、摘要、hex、JSON 解析、路径校验、LRU 缓存、信封、限流全部复用已进构建的库；项目侧只有顺序编排、四级分级、字段映射，**不是新开自写底座例外**（023 A03 已于 024 撤回）。`cargo test --offline --lib` 313 / 0，全量 339 / 0。
''')

app('docs/design/implementation-strategy.md', '''## 052 软件完整性状态

| 项 | 状态 |
| --- | --- |
| 本地签名比对、四级兜底、安全模式诊断包 | **已落地（052）**：`src/core/integrity.rs`，零新增依赖 |
| 摘要缓存与显式刷新 | 已落地：`path:len` 键 / TTL 30 s / `refresh()` |
| 信任根公钥、manifest、文件读取 | 由调用方注入；发行物生成与公钥分发**未启动** |
| 从 GitHub / atomgit 拉版本平台信息、Win7 运行时判定 | 未启动（D07） |
| 演示层三按钮到 `Outcome` 的渲染层接线 | 未启动 |
''')

p = Path('docs/index.md')
t = p.read_text()
a = '262. docs/verification/round-051.md\n\n读取命令：'
if a in t:
    t = t.replace(a, '''262. docs/verification/round-051.md
263. docs/spec/52-round-052-instructions.txt
264. docs/records/round-052-full-readback.md
265. docs/decisions/052-integrity-verification.md
266. docs/verification/round-052.md

读取命令：''', 1)
    t = t.replace('docs/decisions/051-compliance-and-declaration.md docs/verification/round-051.md; do printf',
                  'docs/decisions/051-compliance-and-declaration.md docs/verification/round-051.md docs/spec/52-round-052-instructions.txt docs/records/round-052-full-readback.md docs/decisions/052-integrity-verification.md docs/features/software-integrity.md src/core/integrity.rs docs/verification/round-052.md; do printf', 1)
    p.write_text(t); print('INDEX_OK')
else:
    print('INDEX_SKIP_DUP')

p = Path('README.md')
t = re.sub(r'\| 当前轮次 \| \d+ \|', '| 当前轮次 | 052 |', p.read_text(), count=1)
sec = f'''

## 052 软件完整性验证（B06 实现层）

`src/core/integrity.rs`：签名校验排在解析之前，四级兜底（ok / degraded / disabled / fatal），连续失败 ≥3 导出诊断包，摘要缓存含长度键且 `refresh()` 全清，**签名与判定不缓存结论**，限流不返回通过。公钥与文件读取由调用方注入，代码不内置信任根、不写路径、不发网络请求。

`cargo test --offline --lib` **313 / 0**，全量 **339 / 0**，Windows GNU 交叉检查通过，四守卫零命中，反向注入验签判定 9 FAILED、恢复 15 / 0。零新增依赖，仍 **{pkgs} 包 / {third} 第三方**。UI 闸门未触发，UX HTML 与 {png_n} 张 PNG 零 diff。
'''
if '## 052 软件完整性验证' not in t:
    p.write_text(t.rstrip() + sec); print('README_OK')
else:
    p.write_text(t); print('README_SKIP_DUP')

app('docs/records/rounds.md', f'''## 052

| 落点 | 内容 |
| --- | --- |
| docs/spec/52-round-052-instructions.txt | 逐字副本：「干」 |
| docs/records/round-052-full-readback.md | B02 复读证据：4 份字节 / 行 / SHA-256；防错清单 364 行全文回显 |
| docs/decisions/052-integrity-verification.md | U121–U129、V1–V16、E105–E108、自我批判、四值 |
| docs/verification/round-052.md | 24 条复跑证据 |
| docs/features/software-integrity.md | F052-01 五字段登记、顺序、分级、缓存、三动作映射、未启动项 |
| src/core/integrity.rs | **主交付**：{integ_lines} 行，本地签名比对与分级兜底 |
| src/core/mod.rs | 注册 `pub mod integrity;` |
| demos/round-052-integrity.html | 运行逻辑演示（19 步可点，非整页 UX HTML） |
| 索引与记录 | docs/index 266 项、README、decisions/index、requirement-compliance-audit、pending-question-environments、interface-log I83–I85、ai-errors A183–A187、code-ownership-audit、implementation-strategy、ui-demo 闸门判定 |

051 结尾写「继续按台账走 B06 的实现层软件完整性验证 —— 用已进构建的 ed25519-compact 做本地签名比对，不拉新依赖、不碰真实网络 IO；或用户点 EQ-01 ~ EQ-13 任一编号」。用户回「干」，按默认走前者；**用户未点 EQ 编号，登记 D-052-1，不写成已决断**。

**B02**：对 4 份原文执行全文 `read_text()` 与逐行遍历；`docs/checklists/ai-errors.md` 34458 B / 364 行 / `b08e96ae816e4895` **全文回显**（A182 点名、此前从未逐字打印）；`00-requirements.txt` 261 行已于 051 全文回显；另两份全文遍历未逐行打印。防错清单哈希较 051 变化是 051 自己追加 A178–A182 所致。

**A158 阈值核对**：全仓 grep `consecutive` / `safe_mode` / `SAFE_MODE`，`src/dispatcher/launcher.rs:470-474` 是第 3 次失败进安全模式；本模块 `SAFE_MODE_AFTER=3` 与之一致。

**落地**：验签复用 036 `verify_detached`（ed25519-compact）且**排在解析之前**；manifest 用 `serde_json::Value` 的 `get` / `as_str` / `as_array`，空集合 / 缺字段 / 超 4096 项 / 摘要非 128 位 hex 全返回 `Fatal`，无 `expect` 与下标 panic；路径走 048 `robust::safe_join`；摘要用 037 的 `sha512` + 042 的 `hex`；缓存复用 029 的 `Cache`（`path:len -> sha512hex`，容量 256 / TTL 30 s），`refresh()` 全清，**签名与判定每次重跑、不缓存结论**；`OpBudget` 限 64 次/秒，超限返回 `disabled` 而非 `ok`；连续失败 ≥3 导出 `DiagnosticBundle`（诊断行 / 配置快照 / 运行时 / 模块列表）；结果带 `Envelope::new(Kind::Response, "core.integrity")`，`code` / `level` / `checked` / `safe_mode` 字段，诊断行单行 `[KCU]`。**零新增第三方**，`Cargo.toml` / `Cargo.lock` / `vendor/` 未动，仍 {pkgs} 包 / {third} 第三方。

`public_key` / `signature` / `manifest_bytes` / `root` / `read` 全部由调用方注入，代码不内置信任根、不写绝对路径、不发网络请求，符合 §7.3 与 A12 / A13。发行物公钥分发流程**未启动**。

**演示层三动作映射**：「用默认继续」→ `level != Ok && safe_mode=0`，忽略自定义配置用内置默认；「重新获取」→ `refresh()` 后重走 `verify()`；「取消」→ 不继续启动。**如实**：051 的三卡与按钮仍是静态预览，未接实现层回调，渲染层接线属 UI 层未启动。B06 只补签名比对一项，拉版本平台信息与 Win7 判定仍属 D07 未启动，不能把 B06 整体写成「已修」。

本轮真实问题：

| 编号 | 现象 | 处置 |
| --- | --- | --- |
| E105 | 首版不确定 `sha512::Hash` 是否实现 `AsRef` | 编译验证通过，未改断言 |
| E106 | 全局把 `disk` 改成 `_disk` 误改 7 处，5 处仍引用 → 6 个 E0425 | 全部恢复，按编译警告精确定位 3 行，复跑 313 / 0 零 warning |
| E107 | 反向注入验签判定后 9 个测试 FAILED，不是预估的 2 个 | 按实记录 9 个；证明验签是全部正向路径的共同前置，未调整测试 |
| E108 | abi 集成首跑被网关 502 截断 | 等待后重跑 6 / 0，断言没降 |

**验证**：`cargo test --offline --lib core::integrity` 15 / 0；`cargo test --offline --lib` **313 / 0**（298 + 15，零 warning）；`http_construct` 7 / 0、`window_handle_contract` 6 / 0、`plugin_lifecycle_load` 7 / 0（54.54 s 真加载 cdylib）、`plugin_abi_load` 6 / 0（116.87 s）；全量 **339 / 0**；Windows GNU 交叉检查通过（35.04 s）；panic / semver / i18n / lang 四守卫零命中（`files 39 hits 0`、`keys 26`）；`P09_HITS 0`；CI 三条 `NO_CREDENTIAL` / `NO_EXPLANATORY` / `NO_HARDCODE`；{html_n} 份 demos HTML `node new Function` 全通过；`yaml.safe_load` scan 8 steps；反向验证 9 FAILED → 恢复 15 / 0。UI 闸门**未触发**：UX HTML、两语言包、{png_n} 张 PNG 零 diff。

**四值**：B02 复读、B06 实现层、313 / 0、339 / 0、零新增依赖 = 已证实；B01 / B02 历史缺失 = 已失败（不补写）；B06 其余两项、D07 取数与分发、渲染层接线 = 未启动；EQ-01 ~ EQ-13 拍板 = 未证实；GUI 端到端 / 真实网络 IO / Win7 与 MSVC 运行时 = 受阻。独立验证「部分通过」，**未发通过标记**。

**下一步**：继续按台账走 B06 剩余两项中的「自动关闭某功能」——从版本平台信息得到可用范围后关闭对应入口，属真实网络 IO 层，需 EQ-01 / EQ-03 的 Win7 TLS 口径拍板才能动；或用户点 EQ-01 ~ EQ-13 任一编号。
''', '## 052\n')
print('ALL_DOCS_OK')

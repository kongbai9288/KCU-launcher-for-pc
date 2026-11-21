# 第 065 轮：AX11 设置导入导出与清理（数据层）

| 项 | 值 |
| --- | --- |
| 编号 | 065 |
| 状态 | AX11 `Planned` → `DataLayer`；零新增第三方；UI 闸门未触发 |
| 依据 | `docs/spec/65-round-065-instructions.txt`（逐字「干」）；064 功能池「按工程依赖逐轮落地」；`00:7` / `00:112` / `00:113` / `00:179` / `00:248`；`11:10`；`64-privacy-policy-v1.1.txt` 2.2；`docs/records/ax-feature-pool.md` |
| 前序 | 064：AX01–AX24 全量决断，22 项 `Planned` 排队，AX05 / AX23 已落地 |
| 本轮性质 | 实现轮；`src/` 新增 1 模块 + 3 处接线；`Cargo.toml` / `Cargo.lock` / `vendor/` 零 diff |

## 2. 时间戳

开工 `Sat Nov 21 19:08:52 CST 2026`；最终 `Sat Nov 21 19:38:18 CST 2026`。

## 3. 本轮目标与范围

只发「干」，未点 AX 编号、未回 EQ / Q-C。按 064 功能池「按工程依赖逐轮落地」继续，不另起新层。选 **AX11 settings_export**：它是 22 项 `Planned` 里依赖最浅、不碰 EQ-01 / EQ-13 / 真实网络 IO / UI 渲染的一项，直接衔接 035 的 `config.rs`、048 的 `robust.rs`、050 的端点配置化和 064 的 `consent.rs`。

不做的：AX04 回滚碰 EQ-13 条件数量未拍；AX06 下载历史依赖真实网络 IO；AX01/AX14/AX15/AX17/AX20 是重 UI，卡 EQ-01。按 048 批评的 C 类错误口径，不擅自定默认。

**只落数据层与编排**：导出差集、导入校验、清理回默认。设置页输入控件、文件选择器、进度条等 UI 渲染实现未启动。

## 4. 决定了什么

| 编号 | 决定 | 约束 |
| --- | --- | --- |
| D-065-1 | AX11 状态 `Planned` → `DataLayer` | `AX_SPECS` 状态分层改为 `Planned 21` / `DataLayer 2` / `GateOnly 1`；`ax_guard.py` 改为动态求和 + 显式 AX05/AX11 断言；064 历史行不重写，功能池 065 补记覆盖 |
| D-065-2 | 导出只含与内置默认不同的键 | 与 Axolotl v1.11.0「仅导出与默认设置不同的配置」一致；`os_class` 是环境派生值，列入 `DERIVED_KEYS` 不导出，避免把当前机器写进可移植配置（`00:112`） |
| D-065-3 | 导入逐键校验，未知键 / 坏类型 / 控制字符 / 超长 / 超限一律剔除并给 `[KCU]` DEGRADE 行 | 8 类坏输入不 panic、不静默吞；剩余合法键继续导入；端点值只查类型与长度，**不解析 URL**，与 050 的 8 类回退口径一致，避免误拒合法镜像名 |
| D-065-4 | 清理只回写内置默认，不删同目录状态文件 | 显式保护 `privacy-consent.json` / `boot-state.json` / `diagnostic-bundle.json` / `play-stats.json`；`reject_protected_removal()` 对外拒绝；原子写 `.tmp` + `fs::rename`，无残留 |
| D-065-5 | 零新增第三方，仍 26 包 / 25 第三方 | `serde_json` / `robust` / `diagnostics` / 已有状态常量全部复用；UI 闸门未触发，UX HTML、两语言包、56 张 PNG 零 diff |

## 5. 真发现：清理不能抹掉隐私同意（E192）

`consent.rs` 的 `privacy-consent.json` 与设置文件同目录。若把「清理设置」实现成 `remove_dir_all(root)` 或按目录清空，会一并删掉同意记录：下次启动重新弹同意，更严重的是可被当成「重置同意」绕过 `11:10` 的开启时同意闸门。

处置：`PROTECTED_FILES` 用四个常量名组表（不写死字面量），`cleanup` 只调 `atomic_write` 回写默认、不删任何文件，`is_protected` 表驱动，`reject_protected_removal` 显式拒绝；单测在四个文件里各写 `"keep"`，清理后逐项读回仍是 `"keep"`。政策 2.2「应用设置通常保存在设备本地」保持，导入导出不触发任何上传。

## 6. 关键落地

| 文件 | 行 | 内容 |
| --- | --- | --- |
| `src/core/settings_io.rs` | 247 | `export_diff` / `import` / `atomic_write` / `cleanup` / `is_protected` / `reject_protected_removal`；12 个单测 |
| `src/core/ax.rs` | 1 行 + 2 断言 | AX11 `DataLayer`，计数 21 / 2 / 1 |
| `src/core/boot.rs` | +1 | `LOADED_MODULES` 同步，诊断包模块列表不缺项 |
| `scripts/ax_guard.py` | 改 | 动态状态求和，显式 AX05 / AX11 |
| `scripts/settings_guard.py` | 新建 | 4 常量保护、无批量删除、原子写、派生键排除、AX11 状态；CI `scan` 第 14 步 |

## 7. 交付快照

本地 `19ba29f`（主快照）→ 065 补记，**1114 文件 DIRTY 0**。远端主快照 `b071edd50d894d0781eec0ca82cfac878d74b40b`（`force=false`），主快照阶段逐项 ALL_MATCH **True**（1114 / 1114，DIFF 0 / EXTRA 0 / truncated False）；065 补记以该 ref 为父。主包按 `git ls-files` 打包 1114 项、预览包 57 项，EXTRA 0 / MISSING 0。全仓零凭据、临时日志与注入备份已删。

推送登记：20-blob 精简增量 + `base_tree`（tree `0351a46`），RC=0；未走全量 `api_push.py`，未强推、未重写历史。

## 8. 验证

| 项 | 值 |
| --- | --- |
| `cargo test --offline --lib` | `**425 / 0**` |
| 全量 `cargo test --offline` | `**464 / 0**（8 段，拆三段执行）` |
| Windows GNU 交叉检查 | `**通过 / RC=0 / 29.72 s / 零 warning**` |
| 十三守卫 | `十三守卫 OK + `P09_HITS 0`` |
| CI 三 job / 演示脚本 / 必读项 | ``NO_EXPLANATORY` / `NO_HARDCODE` / `NO_CREDENTIAL`；52 份演示脚本 `BAD 0`；必读 342 项 `MISSING 0`` |
| 独立验证 | 部分通过，未发通过标记 |

## 9. 自我批判

| 编号 | 真问题 | 处置 |
| --- | --- | --- |
| E190 | `ImportReport` derive `Debug/Clone/PartialEq/Eq` 要求 `Config` 实现四个 trait，编译 E0277 / E0369 共 4 条 | 去掉该 derive，不给 `Config` 加无关 trait；425 / 0 |
| E191 | `settings_guard.py` 全文扫 `remove_dir_all`，把单测里清理临时目录的正常用法误判为批量删除 | 守卫只扫 `#[cfg(test)]` 之前的非测试段；与 048 `i18n_guard` 同形态 |
| E192 | 清理设置会抹掉 `privacy-consent.json`，绕过 `11:10` 同意闸门 | D-065-4 四文件表驱动保护 + 单测逐项读回 |
| E193 | `is_protected` 初版写 `name == SETTINGS_FILE && false`，恒假冗余 | 改成纯 `PROTECTED_FILES.contains(&name)`；另删未用的 `bad_type` 避免 dead_code |
| E194 | 导出差集若用 `Config::empty("windows")` 当基准会硬编码环境假设（`00:112`） | 基准由 `Config::empty(&config.os_class)` 生成并排除 `os_class`，零硬编码 |
| E195 | 端点值若走 `http::validate_authority` 会误拒 050 允许的合法镜像名 | 只查类型 / 长度 / 控制字符，URL 解析留给 `endpoints::plan` 的既有 8 类回退 |
| E196 | 改 AX11 状态后 `ax_guard.py` 写死 `planned != 22` 会误报 | 改动态求和 + 显式 AX05 / AX11 断言，不降断言 |
| E197 | 「干」容易被写成一轮做完 22 项 | 决策与功能池写明：按工程依赖逐轮，本轮 1 项，剩 21 项 |
| E198 | `settings_guard.py` 初版用全文子串核四个保护常量，`use` 行会让删掉 `CONSENT_FILE` 的注入仍假 OK | 改成解析 `PROTECTED_FILES` 常量表内容；注入 A 真触发 RC=1 |
| E199 | `export_diff` 实际只靠「基准用当前 `os_class`」天然排除派生键，`DERIVED_KEYS` 常量声明了却没被使用，与 D-065-2 文档不一致 | 加回显式 `DERIVED_KEYS` continue，代码与决策一致；425 / 0 不变 |
| E200 | 注入 C 删掉显式排除语句后，守卫 FAIL RC=1，但 `os_class_is_derived_not_exported` 单测仍通过 | 如实登记：该约束由 `settings_guard.py` 持有，行为测试无法区分两种实现；不改测试凑失败，按 `00:9.2` 测试锁定口径保留原断言 |

自评 9.3（8.8（只想按编号顺推 AX01） → 9.1（选依赖最浅项 + 发现同意文件风险） → 9.3（十三守卫 + 四组注入 + 显式派生键修正））。扣分：21 项仍 `Planned`；EQ-01 ~ EQ-13 与 4 条 Q-C 未拍；设置页 UI 渲染未启动；6 项低可信度转述未交叉印证。

## 10. 四值

| 类 | 值 |
| --- | --- |
| 已证实 | AX11 数据层 / 4 文件保护 / 差集导出 / 8 类坏输入 / 原子写 / `**425 / 0**` / `**464 / 0**（8 段，拆三段执行）` / 十三守卫 / 零新增依赖 / 远端逐项一致 |
| 已失败（不补写） | 035–047 历史格式缺失 |
| 未证实 | 21 项 `Planned`、6 项低可信度转述、逐版本归属、EQ-01 ~ EQ-13、4 条 Q-C |
| 未启动 | 21 项实现、设置页 UI 渲染、真实网络 IO、UI 宿主、崩溃分析、子进程隔离 |
| 受阻 | 无（远端 Git Data API 通道正常；21 项 `Planned` 属未启动，不计受阻） |

# 加载器注册与安装

| 项 | 值 |
| --- | --- |
| 编号 | F016-03 |
| 状态 | 已实现、已验证 |
| 轮次 | 016 |
| 框架 | lightweight.loaders / E03 |

## 怎么运作

`LoaderKind` 六种：Fabric / Forge / NeoForge / Quilt / LiteLoader / OptiFine。`LoaderRegistry` 用 `BTreeSet` 注册，重复注册返回 false 并写 2 级诊断；`codes()` 按序输出。`install(&mut self, kind, &CancelToken)` 返回 Installed / Skipped / Failed 三态，未注册或取消时跳过而不崩，每步写单行诊断。**`version_json_fields()` 恒空、`schema_patch()` 恒 None**：逐版本加载器 schema 未证实，不写死注入字段。信封明确 `schema_patch=none`。

## 开放了什么

| 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- |
| `LoaderKind::{code,all}` | 无 | &str / [LoaderKind;6] | 无 |
| `LoaderRegistry::{new,register,register_all,contains,len,codes,version_json_fields,schema_patch,install,envelope}` | LoaderKind / CancelToken | bool / usize / Vec / Option / InstallOutcome / Envelope | 不 panic |
| `InstallOutcome::code` | 无 | installed / skipped / failed | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | lightweight.loaders（B05；E03 loader） |
| 模块路径 | src/lightweight/loaders.rs |
| 依赖 | core.asynk / diagnostics / envelope |
| 约束 | 未证实字段不写进实现（005 C02）；不生成 version json patch |

## 用户使用逻辑

| 入口 | 动作 | 结果 |
| --- | --- | --- |
| 打开加载器页 | 列出 6 种 | 可逐个或全部安装 |
| 点安装 | 登记标识与结果 | 不写死版本字段，后续拿到一手 schema 再补 |
| 重复点 | 去重可见 | 不重复安装，不崩 |
| 取消 | CancelToken | 跳过，不残留 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | BTreeSet 最多 6 项 |
| 启动耗时 | 7 项测试含在全量 0.12s 内 |
| 常驻进程 | 无 |
| 退出条件 | install 返回 |
| 测量命令 | `cargo test --offline lightweight::loaders`（7 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `six_loaders_are_registered_once` | 6 / 6 | 已证实 |
| `duplicate_register_is_visible_and_not_fatal` | duplicate=true | 已证实 |
| `installed_loader_returns_record_without_schema_fields`、`envelope_declares_no_schema_patch` | 空字段 / none | 已证实 |
| `uninstalled_loader_install_is_skipped_not_crash`、`cancelled_install_skips` | Skipped | 已证实 |
| 逐版本 schema 一手原文 | 未取得 | 未证实 |

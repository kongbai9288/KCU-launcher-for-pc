# F038-01 插件 ABI 契约与库化动态加载

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | 插件导出 C ABI 三个符号（major / minor / init）；宿主用 `libloading::Library::new` 打开动态库、`get::<fn()>` 取符号、拷出数值后丢弃 `Symbol`；`compatible()` 按 major 严格相等、minor 不超宿主判 `Compatible` / `RejectMajor` / `RejectMinor`。Windows 分支由 `windows-link` 的 raw-dylib 链接宏提供 `LoadLibraryExW` / `GetProcAddress`。 |
| 开放了什么 | `src/plugins/abi.rs`：`ABI_MAJOR` / `ABI_MINOR` / 三个符号名 / `PluginAbi` / `AbiVerdict` / `open` / `read_abi` / `read_init` / `check` / `compatible`；`src/plugins/mod.rs` 导出。 |
| 登记框架 | 挂在 036 签名校验与 037 升级同意之后，作为第三条独立闸门；依赖 `libloading 0.8.9` + `cfg-if 1.0.5`（Unix）+ `windows-link 0.2.1`（Windows）。 |
| 用户使用逻辑 | 装插件前先看签名、再看是不是同一个插件的新版本、再看 ABI 对不对；三关任一不过就保留旧插件并给可见原因，不会把启动器拖崩。ABI 不匹配的插件可以禁用后继续尝试启动（037 的故障弹窗），也可以取消。 |
| 性能 | 一次动态库打开 + 两次符号查找 + 一次可选 init；无网络、无额外分配大头，O(1)。Windows GNU 目标已 `cargo check` 通过；MSVC / Win7 运行时未证实。 |

状态：业务层已实现；界面闸门未触发，无界面实现。

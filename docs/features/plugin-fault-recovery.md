# F037-02 插件故障报告与三动作

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | 加载失败生成 `PluginFault { plugin_id, reason }` → `fault_report()` 出标题/正文/两个动作 → `handle_fault()` 按 `DisableAndContinue` / `Cancel` 改 `StartupPlan`。 |
| 开放了什么 | `src/plugins/fault.rs::fault_report` / `handle_fault` / `StartupPlan::active_plugins` / `should_continue`；`PopupKind::PluginFault` 进 catalog。 |
| 登记框架 | 挂在启动流程的插件装载阶段；弹窗注册表 `src/core/popup.rs` 统一管理关闭路径。 |
| 用户使用逻辑 | 弹窗直接报告哪个插件出了什么问题；底部「禁用并继续尝试启动」只跳过这一个插件再试一次，「取消」中止启动，× / Esc 等同取消。禁用只影响本次启动，其他插件照常加载；全被禁用后不再空转。流程结束 0 残留。 |
| 性能 | BTreeSet 查删 O(log n)，无重试风暴；`retry_count` 单调递增可见。 |

状态：业务层已实现；界面层仅演示（51-plugin-fault.png），未进实现。

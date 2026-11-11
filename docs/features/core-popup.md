# 弹窗与关闭 Popup

| 项 | 值 |
| --- | --- |
| 编号 | F013-08 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 013 |

## 怎么运作

`Popup::new` 默认带关闭按钮、Esc、取消三条关闭路径；`close(action)` 按动作校验许可，特殊要求可 `with_special` 覆盖，`allow` 可关掉默认路径但仍须保留一条。`PopupRegistry` 用 BTreeMap 管全部弹窗，`missing_close_path()` 返回无关闭路径的 id，`force_close_all()` 兜底。`catalog()` 列出 11 类弹窗（隐私政策、声明页、EULA、重复模组、文件锁、访客密码、上线提醒、时长、错误、AI 确认、拓展包安装），每类都必须能关。重复 close 幂等。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `Popup::new` / `with_special` / `allow` / `close` / `has_close_path` | 函数 | id/kind/title/CloseAction | Self / bool | 无 |
| `PopupRegistry::{open,close,open_count,all_closed,missing_close_path,force_close_all}` | 函数 | Popup / id+action / 无 | bool / usize / Vec<String> | 无 |
| `catalog` | 函数 | 无 | Vec<Popup> | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | core.popup（B03、K08、013 H03） |
| 模块路径 | src/core/popup.rs |
| 扩展点 | 新增弹窗类型须进 catalog 并过关闭测试 |
| 依赖 | std only |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 任意弹窗出现 | 无 | 点 X / Esc / 取消 / 确认 / 超时 / 宿主 | 必有一条能关 |
| 特殊要求弹窗 | 用户设定 | `with_special` | 仍保留指定关闭动作 |
| 退出流程 | 任意 | `all_closed()` 校验 | 不留未关弹窗 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 11 个 catalog 项，未实测进程级数值 |
| 启动耗时 | 无 |
| 常驻进程 | 无 |
| 退出条件 | 全部 closed |
| 测量命令 | `cargo test --offline core::popup`（6 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `cargo test --offline core::popup` | 6 passed | 已证实 |
| `every_catalog_popup_can_be_closed_by_button` | 11/11 关闭、open_count=0 | 已证实 |
| `special_requirement_overrides_default` | Host 关闭成功 | 已证实 |

## 边界

013 H03 用户点名另一个项目「连弹窗的关闭都没有写」，本层把关闭路径做成构造默认 + 注册表可枚举校验；实际 UI 控件绑定未实现，标未证实。

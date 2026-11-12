# JSON 解析底座

| 项 | 值 |
| --- | --- |
| 编号 | F015-01 |
| 状态 | 已实现、已验证 |
| 版本 | 0.0.0 |
| 轮次 | 015 |

## 怎么运作

`parse(&str)` 用递归下降读取字节流：跳过 ASCII 空白 → 按首字节分派 object / array / string / number / true / false / null。object 与 array 进出时维护 depth，超过 64 报错；string 处理 `\" \\ \/ \b \f \n \r \t \uXXXX`，控制字符直接拒绝，UTF-8 分块按 `from_utf8` 校验；number 拒绝整数部分前导零，支持小数与指数。末尾检查无尾随内容。错误字符串带字节位置。`Json::Obj` 用 `BTreeMap`，键顺序稳定。

## 开放了什么

| 接口 | 类型 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| `parse` | 函数 | &str | Json | String，含字节位置 |
| `Json::{get,as_str,as_bool,as_u64,as_array,string_field}` | 函数 | 键名 / 无 | 引用或 Option | 无 |

## 登记框架

| 项 | 值 |
| --- | --- |
| 框架 | dispatcher.json（005-blueprint.md B04，015 D06 L03） |
| 模块路径 | src/dispatcher/json.rs |
| 扩展点 | 无 |
| 依赖 | std only；未引入 serde |

## 用户使用逻辑

| 入口 | 前置 | 动作 | 结果 |
| --- | --- | --- | --- |
| 任务文件 / config 文件 | 用户放置 json | 解析 | 结构化任务；坏文件给出字节位置报错 |
| 中文 mc 版本名 / 实例名 | 字符串含中文 | 按 UTF-8 读取 | 原样保留 |

## 性能

| 项 | 值 |
| --- | --- |
| 内存峰值 | 单次解析与输入同阶；深度上限 64，嵌套不无限增长 |
| 启动耗时 | 7 项测试合计含在全量 0.11s 内 |
| 常驻进程 | 无 |
| 退出条件 | 返回 Json 或 String 错误 |
| 测量命令 | `cargo test --offline dispatcher::json`（7 passed） |

## 验证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| `parses_object_with_nested_values`、`parses_escapes_and_unicode` | 通过 | 已证实 |
| `rejects_trailing_content`、`rejects_malformed_input`、`rejects_excessive_depth` | 通过 | 已证实 |
| `object_keys_are_ordered` | 键序 a、b | 已证实 |

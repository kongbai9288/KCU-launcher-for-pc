# 插件 ABI 契约（038）

| 项 | 值 |
| --- | --- |
| ABI 版本 | major=1 / minor=0 |
| 必需符号 | `kcu_plugin_abi_major() -> u32`、`kcu_plugin_abi_minor() -> u32` |
| 可选符号 | `kcu_plugin_init() -> i32`，缺失返回 None，不判失败 |
| 符号名 | 必须以 NUL 结尾传给 `libloading::Library::get`（常量已自带 `\0`） |
| major | 与宿主不等 → `RejectMajor`，优先于 minor 判定 |
| minor | 大于宿主 → `RejectMinor`；小于等于宿主 → `Compatible` |
| 句柄 | `Symbol` 不可存进长期结构体；取出数值后由 `Library` 自行 Drop |
| Windows | `Library::new` 默认 flags=0 → `LoadLibraryExW` 基础路径；不启用 `LOAD_LIBRARY_SEARCH_*` |
| Win7 | KB2533623 只在显式启用搜索目录标志时才相关；默认路径不依赖，运行时行为未证实 |
| 闸门顺序 | 签名校验（036）→ 身份哈希 / 升级同意（037）→ ABI 协商（038）→ 故障恢复（037） |
| 未启动 | 插件子进程隔离、卸载顺序、真实 `.dll` 加载、MSVC 目标验证 |

依赖与许可：`docs/decisions/038-plugin-abi-libloading.md`、`THIRD-PARTY-NOTICES.md` N32–N34。

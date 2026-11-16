# 破坏性输入与路径穿越一手资料（048）

| 锚点 | 内容 | 四值 |
| --- | --- | --- |
| https://owasp.org/www-community/attacks/Path_Traversal | 「By manipulating variables that reference files with "dot-dot-slash (../)" sequences and its variations or by using absolute file paths, it may be possible to access arbitrary files and directories」；「Validate the user's input by only accepting known good – do not sanitize the data」；「normalize the input before using in file io API's」 | 已证实 |
| https://owasp.org/www-community/attacks/Path_Traversal | 编码变体 `%2e%2e%2f` 代表 `../`；攻击别名 dot-dot-slash / directory traversal / backtracking | 已证实 |
| https://doc.rust-lang.org/std/path/enum.Component.html | `Prefix` / `RootDir` / `CurDir` / `ParentDir` / `Normal` 五种分量；分量由标准库解析，项目侧只做策略判定 | 已证实 |
| https://doc.rust-lang.org/std/sync/struct.PoisonError.html | `pub fn into_inner(self) -> T`；046 已用于锁中毒恢复 | 已证实 |
| https://doc.rust-lang.org/std/fs/fn.read_to_string.html | 读失败返回 `io::Result`，不 panic；048 的 `read_or_default` 据此回退 | 已证实 |
| `src/plugins/icon.rs`（044） | `MAX_SVG_BYTES = 16 KiB`，`s.is_empty() || s.len() > MAX_SVG_BYTES` 已在校验入口 | 已证实 |
| `src/core/cache.rs`（029 / 046） | `LruCache` 容量有界、锁中毒恢复 | 已证实 |

| 编号 | 结论 |
| --- | --- |
| R36 | OWASP 建议「只接受已知好值」而不是清洗输入，048 的 `safe_join` 因此逐分量拒绝，而不是把 `../` 字符串删掉。 |
| R37 | 绝对路径与 `..` 越界是两类独立入口，都要拒；Windows 保留设备名（CON/NUL/COM1…）在 Linux 上也要检查，因为目标平台是 Windows。 |
| R38 | 「删文件」不等于「崩溃」：可选文件回默认值、必需文件给明确错误，二者不能都静默回默认。 |
| R39 | 高频重复与并发洪泛用原子计数 + 滚动窗口限流；锁中毒时按 046 的口径恢复，不让防护模块自身成为崩溃点。 |

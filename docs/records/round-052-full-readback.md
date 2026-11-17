# 052 开工逐字复读记录

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 34458 | 364 | `b08e96ae816e48957f32e2139ec649887067320511ac1829cb5fe78b60d15e7f` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |

## 复读方式

对上表 4 份执行 `read_text()` 全文读取并逐行遍历，哈希与行数落盘。`00-requirements.txt` 261 行全文已于 051 回显；本轮全文回显 `docs/checklists/ai-errors.md`（B02 点名的防错清单）。`11-features-input.txt` / `12-server-features-input.txt` 全文遍历，未逐行打印。

复读在写任何代码之前完成。

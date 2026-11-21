# 064 开工逐字复读记录

| 文件 | 字节 | 行 | SHA-256 |
| --- | --- | --- | --- |
| `docs/spec/00-requirements.txt` | 16422 | 261 | `23ffbf3fe341ce4f7757e8c9ca8a6de81da3b312124aaab0802930c4d798f295` |
| `docs/checklists/ai-errors.md` | 44442 | 463 | `7e2542249d244ce36420363dd54e5e8273f81e1bb272f07986097e6edc62be5b` |
| `docs/spec/11-features-input.txt` | 17096 | 268 | `1c3ff1a282863dfb6a3255a2efbbe4c8cfe6f0247d0828bbb8b15dad3b15a33c` |
| `docs/spec/12-server-features-input.txt` | 4970 | 64 | `03a62d90a2325fdf5c71157b2026a359343e753676527d36b83cb845e14c3d88` |
| `docs/spec/63-round-063-instructions.txt` | 228 | 0 | `f92348ac3bc6802fb6d04f5dcbb398985404043cecb2160ab29410d6ac9da9f9` |
| `docs/spec/64-round-064-instructions.txt` | 4813 | 76 | `d20e36a1241c6feb35ed6e0ffbd21d0301448de8db90e47713d6be4a4b4364fc` |
| `docs/spec/64-privacy-policy-v1.1.txt` | 4638 | 77 | `de3b07c70f6747ae220db8e67c6168eed0b35e992c80334581b154cd80a3e8b8` |
| `docs/research/31-axolotl-launcher-features.md` | 13676 | 85 | `da59dd069c0220f5dba2ccfa31fd28c5d6af6a74841162280b7848ad12df5a01` |

复读在写任何代码 / 文档之前完成。真读 `00-requirements.txt` 全文、`11-features-input.txt` 55 条全文、`12-server-features-input.txt` 全文、防错清单 A194–A229 全文、063 调研副本 24 项候选、以及当轮隐私政策全文。

| 原文锚点 | 内容 |
| --- | --- |
| `64-round-064-instructions.txt:1` | `全部（不与我们的项目冲突的情况下），至于客户端的ai由于我为用户的安全性着想，所以说只留一个口子，但是不给用户操作页面。` |
| `64-privacy-policy-v1.1.txt:2` | `版本： v1.1` |
| `64-privacy-policy-v1.1.txt:3` | `生效日期： 2026年11月21日` |
| `64-privacy-policy-v1.1.txt:5` | `联系方式： kcustudios@outlook.com` |
| `64-privacy-policy-v1.1.txt:10` | `十、政策更新 ... 您继续使用本应用，即视为接受更新后的政策。` |
| `00-requirements.txt:44` | `功能与市面主流启动器保持同步：别人有的功能要有。` |
| `00-requirements.txt:133` | `需求必须逐字保存到仓库（如文档目录下的规格目录），不能只存链接或转述。` |
| `00-requirements.txt:248` | `用户当轮明确指令 > 本文件规则。` |
| `00-requirements.txt:73-94` | 仓库内容边界：禁止解释性内容进仓库；许可证、第三方声明、规则约束可进仓库 |
| `11-features-input.txt:217` | `10.软件开启时候需要同意隐私政策` |
| `11-features-input.txt:18` | `尽量不要把咱们的APi写成共有的API,防止被别人攻击，内部监听（只有服务器功能让ai用的api不受影响）` |
| `12-server-features-input.txt:4` | 开服器 AI 工具，不赋予删除权限 + 用户手动同意 |
| `31-axolotl-launcher-features.md` | AX01–AX24 共 24 项未列候选；AX23 与 `11:18` 冲突 |

政策全文逐字保存判定：`docs/spec/64-privacy-policy-v1.1.txt` 是用户给的原文，属 `00:133` 规格目录与 `13.1` 文档清单里的「许可证、第三方声明、规则约束」，不是模型写的解释性内容，按 `00:73-94` 允许进仓库。政策原文里含「为提供」「用于」「由于」等词，是被引用的原文，不作模型解释性输出处理。

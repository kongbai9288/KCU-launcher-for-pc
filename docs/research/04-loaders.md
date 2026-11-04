# 加载器

检索日期：2026-11-04

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| Fabric Loader | 平台无关模组加载器 | 已证实 | fabricmc.net |
| Fabric API | 放入 `mods` 文件夹 | 已证实 | fabricmc.net |
| Quilt Loader | 声明兼容已有 Fabric mod | 已证实 | quiltmc.org |
| NeoForge | 存在版本发布与 26.1 / 21.11 等构建线 | 已证实 | neoforged.net |
| Forge 服务端安装 | `java -jar <installer>.jar --installServer`，生成 `libraries/` 与 `run.sh` | 部分已证实 | 第三方部署文档 |
| Fabric 服务端安装 | `java -jar fabric-installer.jar server -mcversion <v> -downloadMinecraft` | 部分已证实 | 同上 |
| Java 版本线 | 1.20.1+ 用 Java 17，1.21+ 用 Java 21 | 部分已证实 | 第三方部署文档 |
| version json 注入 | `inheritsFrom`、`arguments`、`mainClass`、`libraries` 的逐加载器差异 | 未证实 | 官方 installer schema 未取得 |
| natives 处理差异 | 未核实 | 未证实 | 同上 |
| OptiFine 安装器格式 | 未核实 | 未证实 | 同上 |
| Forge/NeoForge installer schema | 未核实 | 未证实 | 同上 |
| 组合兼容上下界 | 由具体版本与构建号决定，未核实 | 未证实 | 同上 |

来源：
- https://fabricmc.net/
- https://quiltmc.org/en/
- https://neoforged.net/
- https://asiagb.com/content/minecraft-forge-fabric-mods-zh.html

约束：
- 未取得 schema 前不生成伪造的 version json patch。
- 五个加载器共用同一安装模块入口，参数差异走配置项。
- 商店显示加载器图标，图标来源与许可证单独登记。

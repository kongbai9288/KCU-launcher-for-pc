# 加载器

检索日期：2026-11-05
锚点格式：完整 URL、`path:line` 或 `cmd: <命令> → <输出>`；锚点逐行独立。

| 事实 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| Fabric Loader | 平台无关模组加载器 | 已证实 | https://fabricmc.net/ |
| Fabric API | 放入 mods 文件夹 | 已证实 | https://fabricmc.net/ |
| Quilt Loader | 声明兼容已有 Fabric mod | 已证实 | https://quiltmc.org/en/ |
| NeoForge | 存在版本发布与 26.1 / 21.11 构建线 | 已证实 | https://neoforged.net/ |
| Fabric Meta README | 544 行，blob SHA-1 3b33b9956e1e551c2fe65dbc29502b27c2f27937 | 已证实 | https://api.github.com/repos/FabricMC/fabric-meta/contents/README.md |
| profile/json 端点 | /v2/versions/loader/:game_version/:loader_version/profile/json 返回标准启动器 profile JSON | 已证实 | https://api.github.com/repos/FabricMC/fabric-meta/contents/README.md |
| profile/zip 端点 | 含 profile json 与 dummy jar，解压到 .minecraft/versions | 已证实 | https://api.github.com/repos/FabricMC/fabric-meta/contents/README.md |
| server/json 端点 | 返回 launcher JSON 格式，主类为服务端主类 | 已证实 | https://api.github.com/repos/FabricMC/fabric-meta/contents/README.md |
| launcherMeta | 含 libraries 与 mainClass.client / mainClass.server | 已证实 | https://api.github.com/repos/FabricMC/fabric-meta/contents/README.md |
| URL 编码 | game_version 与 loader_version 需 url encode | 已证实 | https://api.github.com/repos/FabricMC/fabric-meta/contents/README.md |
| Forge 服务端安装 | java -jar <installer>.jar --installServer，生成 libraries/ 与 run.sh | 未证实 | https://asiagb.com/content/minecraft-forge-fabric-mods-zh.html |
| Fabric 服务端安装 | java -jar fabric-installer.jar server -mcversion <v> -downloadMinecraft | 未证实 | https://asiagb.com/content/minecraft-forge-fabric-mods-zh.html |
| Java 版本线 | 1.20.1+ 用 Java 17，1.21+ 用 Java 21 | 未证实 | https://asiagb.com/content/minecraft-forge-fabric-mods-zh.html |
| version json 注入逐加载器差异 | inheritsFrom、arguments、mainClass、libraries 差异未取得 | 未证实 | 官方 installer schema 未取得 |
| natives 处理差异 | 未核实 | 未证实 | 官方 installer schema 未取得 |
| OptiFine 安装器格式 | 未核实 | 未证实 | 官方 schema 未取得 |
| Forge/NeoForge installer schema | 未核实 | 未证实 | 官方 schema 未取得 |
| Quilt / LiteLoader schema | 未核实 | 未证实 | 官方 schema 未取得 |
| 组合兼容上下界 | 由具体版本与构建号决定 | 未证实 | 官方 schema 未取得 |

## 上游版本状态

| 组件 | 值 | 四值 | 锚点 |
| --- | --- | --- | --- |
| fabric-loader 最新 release | 0.20.1，2026-10-19T19:02:45Z | 已证实 | https://api.github.com/repos/FabricMC/fabric-loader/releases/latest |
| quilt-loader 首个 tag | 0.31.0-beta.5 | 已证实 | https://api.github.com/repos/QuiltMC/quilt-loader/tags?per_page=1 |
| quilt-loader releases/latest | 404 Not Found | 已失败 | https://api.github.com/repos/QuiltMC/quilt-loader/releases/latest |
| NeoForge 首个 tag | v99.99，占位 tag，不作版本依据 | 已证实 | https://api.github.com/repos/neoforged/NeoForge/tags?per_page=1 |
| NeoForge releases/latest | 404 Not Found | 已失败 | https://api.github.com/repos/neoforged/NeoForge/releases/latest |
| meta.fabricmc.net 直连 | 403 policy_default_denied | 受阻 | cmd: curl https://meta.fabricmc.net/v2/versions/loader → 403 |
| meta.quiltmc.org 直连 | 403 policy_default_denied | 受阻 | cmd: curl https://meta.quiltmc.org/v3/versions/loader → 403 |
| maven.neoforged.net 直连 | 403 policy_default_denied | 受阻 | cmd: curl https://maven.neoforged.net/releases/net/neoforged/neoforge/maven-metadata.xml → 403 |

## 005 补证

| 命令 | 输出 | 四值 |
| --- | --- | --- |
| GET /repos/FabricMC/fabric-meta/contents/README.md | 200，544 行 | 已证实 |
| GET /repos/FabricMC/fabric-loader/releases/latest | 200，0.20.1 | 已证实 |

来源：
- https://fabricmc.net/
- https://quiltmc.org/en/
- https://neoforged.net/
- https://api.github.com/repos/FabricMC/fabric-meta/contents/README.md

约束：
- 未取得 schema 前不生成 version json patch。
- 五个加载器共用同一安装模块入口，参数差异走配置项。
- 商店显示加载器图标，图标来源与许可证单独登记。

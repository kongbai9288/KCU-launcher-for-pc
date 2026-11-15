# F037-03 插件侧栏 SVG 与问号兜底

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `PluginIcon::from_svg(Option<&str>)`：合法 SVG 原样保留；缺失/空/非 svg/超 16 KiB/含脚本或外链 → `Fallback`，`glyph()` 返回 `?`。 |
| 开放了什么 | `src/plugins/icon.rs::PluginIcon` / `FALLBACK_GLYPH` / `MAX_SVG_BYTES`。 |
| 登记框架 | 挂在插件清单解析到侧栏槽位注册之间；渲染层由 UI 宿主负责（本轮未实现）。 |
| 用户使用逻辑 | 插件自带图标就显示自己的；没给的显示虚线框问号，尺寸与 lucide 图标一致，深浅主题都清楚。SVG 里的 `href="#..."` 内部引用放行，外部引用退回问号。不做内容白名单，留高度自定义。 |
| 性能 | 单次线性扫描，上限 16 KiB；渲染走 `<img data:>` 隔离，脚本不进 DOM。 |

状态：业务层已实现；界面层仅演示（49-plugin-icons.png），未进实现。

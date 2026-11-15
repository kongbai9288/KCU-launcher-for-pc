# F044-01 插件侧栏 SVG 校验契约

| 字段 | 内容 |
| --- | --- |
| 怎么运作 | `PluginIcon::from_svg` 先做长度 / 根标签 / 空白的快速筛，再交给 `quick_xml::Reader::from_str` 遍历事件；词法、属性格式、重复属性检查、实体解码、well-formed 全由库完成。项目侧只判三件事：禁止元素清单、所有 `on*` 事件属性、`href` / `src` 只允许 `#` 内部片段；根不是 `svg`、出现 DOCTYPE、解析报错都退成 `Fallback`。 |
| 开放了什么 | `src/plugins/icon.rs` 的 `from_svg` / `glyph` / `is_fallback`；`FALLBACK_GLYPH`（`?`）与 `MAX_SVG_BYTES`（16 KB）两个常量不变；渲染层仍用 `<img data:>` 隔离，SVG 脚本不进 DOM。 |
| 登记框架 | `quick-xml 0.38.4`（MIT / MSRV 1.56 / 唯一非 optional 依赖 memchr，025 已在构建）；与 037 的插件图标兜底、038 的 ABI、039 的生命周期串联。 |
| 用户使用逻辑 | 插件自带 SVG 照常显示，没给就显示虚线框问号；插件作者用单引号、命名空间前缀、实体编码写的外链都不会悄悄生效；正常 SVG 里出现 `&lt;script&gt;` 这类文本也不会被误判成坏图标；内部片段引用仍可自定义。 |
| 性能 | 16 KB 上限内一次线性事件遍历，无分配大头、无 IO、无额外网络请求；校验失败立即返回，不继续遍历。 |

状态：已实现已验证；真实网络 IO 未启动。

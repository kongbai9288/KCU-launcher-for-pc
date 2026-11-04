# 启动器图标

| 项 | 值 |
| --- | --- |
| 编号 | 002 |
| 状态 | 已实现 |
| 版本 | 0.0.0 |
| 轮次 | 002 |

## 决定了什么

| 项 | 值 |
| --- | --- |
| 资产路径 | assets/icon/kcu-launcher.jpg |
| 来源 | 用户第 002 轮提供，/data/inputs/CMP_20261024210823292.png |
| 源文件扩展名 | .png |
| 实际格式 | JPEG，1440x1440，RGB，Exif orientation=upper-left |
| 字节数 | 175816 |
| SHA-1 | d453d3f5eb2b09913e6e19e85460f990f1e39076 |
| 落盘动作 | 复制原始字节，扩展名改为 .jpg |
| 视觉 | 白底浅色水印，青绿像素立方体，两面 KCU 字样 |

## 约束

| 编号 | 约束 |
| --- | --- |
| C01 | 字节未改动，落盘文件 SHA-1 与源文件一致 |
| C02 | 许可证未定，不进入构建，不生成 ICO，不生成资产派生图 |
| C03 | 白底与水印未裁切，窗口图标与任务栏图标使用前需单独确认 |
| C04 | 框架蓝图未确认前不绑定到 UI 模块 |
| C05 | 图标内文字为 KCU，语言范围中文与英文 |

## 验证条件

| 编号 | 命令 | 期望 |
| --- | --- | --- |
| V01 | `file assets/icon/kcu-launcher.jpg` | JPEG image data，1440x1440 |
| V02 | `sha1sum assets/icon/kcu-launcher.jpg /data/inputs/CMP_20261024210823292.png` | 两行哈希相同 |
| V03 | `! grep -rqE 'gh[p]_' .` | exit 0 |

from pathlib import Path
import re, html, json

p = Path('demos/ui-full-kcu-paper.html')
t = p.read_text()
cut = t.index('<script>')
body, script = t[:cut], t[cut:]

# 中文短语 -> 英文（演示层字典；实现层由 .ftl 全量提供）
EN_TEXT = {
    # 通用 / 导航
    '常规': 'General', '启动与实例': 'Startup & instances', '界面语言': 'Language', '主题': 'Theme',
    '数据目录': 'Data folder', '公告提示': 'Notices', '使用说明': 'How it works', 'EULA': 'EULA',
    '崩溃后': 'After a crash', '旧版 jar': 'Old jars', '用户指定': 'User pick', '设备连接范围': 'Connection budget',
    '双击进服': 'Double-click to join', '推荐与排序': 'Recommend & rank', '服务器状态': 'Server status',
    '自动连接': 'Auto connect', '排序规则': 'Sorting', '缓存与刷新': 'Cache & refresh', '下载与镜像': 'Downloads & mirrors',
    'AI 容器接口': 'AI container', '插件与更新': 'Plugins & updates', '崩溃反馈': 'Crash reports',
    '隐私与诊断': 'Privacy & diagnostics', '实验性': 'Labs', '已改 3 项': 'Changed 3', '恢复默认': 'Reset all',
    '扩展': 'Extensions', '我的插件': 'My plugins', '更新与状态': 'Updates & status', '设置': 'Settings',
    '关于': 'About', '收起侧栏': 'Collapse', '公告中心': 'Notices', '实例与版本': 'Instances',
    '服务器': 'Servers', '下载中心': 'Downloads', '模组管理': 'Mods', '账号登录': 'Accounts',
    '开服器': 'Server Host', '日志诊断': 'Logs', '首页': 'Home', '桌面端': 'Desktop',
    # 选项
    '简体中文': '简体中文', 'English': 'English', '纸质浅色（默认）': 'Paper light (default)', '深色纸质': 'Paper dark',
    '跟随系统': 'Follow system', '启动前写入': 'Write before launch', '按日志自动重启': 'Restart on crash log',
    '写 lockfile 禁用': 'Disable with lockfile', '永远排第一': 'Always first', '未读时铃铛提示': 'Bell for unread',
    '静默': 'Silent', '每次自动连几台': 'Servers per round', '同时连接': 'Concurrent', '轻量机器': 'Light machines',
    '新加的服务器': 'Newly added', '范围外的': 'Outside the round', '一定连，但占同一份额度': 'Always connect, inside the same budget',
    '保留上次结果，不主动连': 'Keep last result, no request', '4 台（推荐）': '4 (recommended)', '2 台': '2', '6 台': '6',
    '全部': 'All', '3 路': '3', '2 路': '2', '1 路': '1', '自动降到 2 台 / 2 路': 'Auto: 2 / 2',
    '与标准一致': 'Same as standard', '上次玩这个服用的实例': 'Last instance for this server',
    '上次用过的实例': 'Last used instance', '版本兼容范围': 'Compatible versions', '自动选定': 'Selected',
    '只读，不改游戏文件': 'Read only', 'SLP + 手动覆盖': 'SLP + manual override', '仅手动': 'Manual only',
    '插件提供': 'From plugin', '在线': 'Online', '维护中': 'Maintenance', '离线': 'Offline', '满员': 'Full',
    '私有': 'Private', '自定义': 'Custom', '超时标灰，回退缓存': 'Grey on timeout, fall back to cache',
    '协议被禁用时给可见提示': 'Visible notice when protocol is off', '不静默重试': 'No silent retry',
    # 通用标签
    '项目': 'Project', '版本 / 分组': 'Version / group', '许可证': 'License', '版权': 'Copyright',
    '用途': 'Use', '来源': 'Source', '说明': 'Notes', '状态': 'Status', '名称': 'Name', '地址': 'Address',
    '操作': 'Actions', '类型': 'Type', '时间': 'Time', '内容': 'Content', '数量': 'Count', '结果': 'Result',
    '已就绪': 'Ready', '待刷新': 'Pending', '就绪': 'Ready', '已保存': 'Saved', '未配置': 'Not set',
    '未发送': 'Not sent', '启用': 'Enabled', '正常': 'OK', '可更新': 'Update', '被锁': 'Locked',
    # 按钮
    '刷新': 'Refresh', '重新获取': 'Reload', '刷新清单': 'Refresh list', '重新扫描': 'Rescan',
    '新建实例': 'New instance', '列表': 'List', '网格': 'Grid', '取消': 'Cancel', '保存': 'Save',
    '稍后': 'Later', '知道了': 'Got it', '不再提示': 'Do not show again', '知道了 ': 'Got it',
    '看最近一次': 'View latest', '导出诊断包': 'Export diagnostics', '查看插件': 'View plugins',
    '模拟插件化更新': 'Simulate plugin update', '模拟回滚': 'Simulate rollback', '重新读取': 'Rescan',
    '停止本次同步': 'Stop', '切到轻量档': 'Lighter mode', '切回标准档': 'Standard mode',
    '上次更新': 'Updated', '刷新': 'Refresh', '仅清过期': 'Clear expired', '仅本地': 'Local only',
    # 面板标题（高频）
    '设置': 'Settings', '关于 KCU Launcher': 'About KCU Launcher', '第三方许可': 'Third-party licenses',
    '连接范围': 'Connection budget', '自动同步': 'Auto sync', '四层缓存': 'Four-layer cache',
    '刷新机制': 'Refresh triggers', '推荐位': 'Recommendations', '公告中心': 'Notices',
    '服务器列表': 'Server list', '推荐服务器': 'Recommended servers', '运行状态': 'Status',
    '已装插件与更新模拟': 'Installed plugins & update demo', '会记下什么': 'What is recorded',
    '崩溃反馈': 'Crash reports',
    # 表格 / 副标题常见
    '按许可证分组': 'Grouped by license', '离线可读': 'Readable offline', '改动立即生效': 'Applied instantly',
    '容量有界': 'Bounded', '单飞去重': 'Single-flight', '失败回退上次缓存': 'Fall back to last cache',
    '取消 0 副作用': 'Cancel has no side effects', '流程结束 0 残留': 'No dialogs left open',
}


def key_of(s):
    return s


def add_attr(m, tag_pat):
    whole = m.group(0)
    if 'data-i18n=' in whole:
        return whole
    text = m.group(3)
    if not re.search(r'[一-鿿]', text):
        return whole
    attr = ' data-i18n="' + html.escape(text, quote=True) + '"'
    head = m.group(1) + m.group(2)
    if head.startswith('<option') and 'value=' not in head:
        head = head.replace('<option', '<option value="' + html.escape(text, quote=True) + '"', 1)
    return head + attr + '>' + text + m.group(4)


PATTERNS = [
    r'(<span class="k")([^>]*)([^<]+)(</span>)',
    r'(<div class="hd")([^>]*)([^<]+)(</div>)',
    r'(<option)([^>]*)([^<]+)(</option>)',
    r'(<div class="panel-title")([^>]*)([^<]+)(</div>)',
    r'(<div class="panel-sub")([^>]*)([^<]+)(</div>)',
    r'(<th)([^>]*)([^<]+)(</th>)',
    r'(<span class="chip" id="[^"]+")([^>]*)([^<]+)(</span>)',
    r'(<div class="stack"[^>]*>\s*<div)(>)([^<]+)(</div>)',
    r'(<span class="lb")([^>]*)([^<]+)(</span>)',
]
for pat in PATTERNS:
    body, n = re.subn(pat, lambda m: add_attr(m, pat), body)
    print('PAT', pat[:38], 'n=', n)

# 追加 EN_TEXT 到脚本：插在 let LOCALE 前
anchor = "let LOCALE='zh-CN';"
assert anchor in script
insert = 'const EN_TEXT=' + json.dumps(EN_TEXT, ensure_ascii=False, separators=(',', ':')) + ';\n'
script = script.replace(anchor, insert + anchor, 1)

# tr 支持中文原文作 key
old = "function tr(k,fb){return LOCALE==='en-US'&&EN[k]?EN[k]:(fb!==undefined?fb:k);}"
new = "function tr(k,fb){if(LOCALE==='en-US'){if(EN[k])return EN[k];if(EN_TEXT[k])return EN_TEXT[k];}return fb!==undefined?fb:k;}"
assert old in script
script = script.replace(old, new, 1)

p.write_text(body + script)
print('I18N_COVER_OK', p.stat().st_size, 'dict', len(EN_TEXT))

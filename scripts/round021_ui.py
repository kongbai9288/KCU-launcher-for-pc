from pathlib import Path
import re

p = Path('demos/ui-full-kcu-paper.html')
t = p.read_text()


def I(n):
    return '<svg class="li" aria-hidden="true"><use href="#i-' + n + '"></use></svg>'


def repl(a, b, label):
    global t
    assert a in t, label
    t = t.replace(a, b, 1)
    print('OK', label)


# ---------- CSS ----------
css = '''
.srv-row{display:flex;align-items:center;gap:12px;padding:10px 12px;border-bottom:1px solid var(--line);cursor:pointer}
.srv-row:last-child{border-bottom:none}
.srv-row:hover{background:var(--sel)}
.srv-ico{width:48px;height:48px;flex-shrink:0;border-radius:var(--r-sm);border:1px solid var(--line);display:flex;align-items:center;justify-content:center;font-family:var(--serif);font-size:19px;font-weight:700;background:var(--card);color:var(--accent)}
.srv-ico.off{filter:grayscale(1);opacity:.55}
.srv-main{flex:1;min-width:0}
.srv-name{font-size:13px;font-weight:600;color:var(--ink);display:flex;align-items:center;gap:6px}
.srv-motd{font-size:11px;color:var(--ink-2);margin-top:3px;line-height:1.5;white-space:pre-line;overflow:hidden;max-height:34px}
.srv-meta{font-size:10px;color:var(--ink-3);margin-top:4px}
.srv-side{text-align:right;flex-shrink:0;min-width:92px}
.srv-count{font-size:12px;color:var(--ink-2)}
.srv-ping{display:inline-flex;gap:2px;align-items:flex-end;height:12px;margin-top:5px;justify-content:flex-end}
.srv-ping i{width:3px;background:var(--accent);border-radius:1px;display:block}
.srv-ping i:nth-child(1){height:4px}.srv-ping i:nth-child(2){height:6px}.srv-ping i:nth-child(3){height:8px}.srv-ping i:nth-child(4){height:10px}.srv-ping i:nth-child(5){height:12px}
.srv-ping.off i{background:var(--ink-3);opacity:.4}
.srv-ver{font-size:10px;color:var(--ink-3);margin-top:4px}
.lock-star{color:var(--accent);cursor:pointer}
.rank-tb{width:100%;border-collapse:collapse;font-size:11px}
.rank-tb td{padding:7px 8px;border-bottom:1px solid var(--line);color:var(--ink-2)}
.rank-tb td:first-child{width:26px;color:var(--accent);font-weight:700}
'''
t = t.replace('</style>\n', '\n' + css + '\n</style>\n', 1)

# ---------- 去工程叙事：设置 ID 小字、徽章、口径 ----------
t = re.sub(r'<span class="setid">[^<]*</span>', '', t)
print('OK setid removed', t.count('class="setid"'))
repl('9 个分组 · 每项有稳定 ID · 写后即时生效 · 可搜索 / @modified / 单项重置',
     '改动立即生效 · 可搜索 · 只看改过的项 · 一键恢复默认', 'settings subtitle')
repl('<span class="badge ok">slot:core.locked.settings</span><span class="badge up">' + I('lock-keyhole') + ' 插件不可覆盖</span>',
     '<span class="badge ok">已保存</span>', 'settings badges')
repl('<span class="chip" id="tabModified">@modified 3</span>', '<span class="chip" id="tabModified">已改 3 项</span>', 'modified chip')
repl('<div class="panel-title">设置项约定</div></div><div class="stack" style="font-size:11px;color:var(--ink-2)"><div>每项有稳定 ID、默认值、作用范围；写后即时生效，失败保留旧值并可见报错。</div><div><span class="badge up">@modified 3</span> 只看改过的项；齿轮可复制 ID / 重置单项。</div><div>插件可在设置内追加自己的分组，不能改写 <b>core.*</b> 项。</div></div>',
     '<div class="panel-title">使用说明</div></div><div class="stack" style="font-size:11px;color:var(--ink-2)"><div>改动立即生效；保存失败会保留原来的值并给出提示。</div><div>「已改 3 项」只看动过的地方，每项都能单独恢复默认。</div><div>插件可以加自己的设置分组，不会改动原有的设置。</div></div>', 'settings convention')

# ---------- 导航：去掉工程标签与内部证据入口 ----------
repl('<div class="slot-plugin"><div class="sh">' + I('puzzle') + ' 插件区 · slot:plugin.*</div>',
     '<div class="slot-plugin"><div class="sh">' + I('puzzle') + ' 扩展</div>', 'plugin area title')
repl('<button class="nav-item" data-v="slots"><span class="ic">' + I('layout-grid') + '</span><span class="lb">推荐插件</span><span class="cnt">2</span></button>',
     '<button class="nav-item" data-v="plugins"><span class="ic">' + I('puzzle') + '</span><span class="lb">我的插件</span><span class="cnt">2</span></button>', 'plugin entry')
t = t.replace('<span class="lb">状态面板</span></button>', '<span class="lb">状态面板</span></button>', 1)
repl('<div class="slot-core"><div class="sh">' + I('lock-keyhole') + ' 核心槽位 · 锁定 · 插件不可占用</div>',
     '<div class="slot-core"><div class="sh"> </div>', 'core slot title')
repl('<span class="lb">设置</span><span class="lock-b">locked</span>', '<span class="lb">设置</span>', 'settings lock badge')
repl('<span class="lb">关于</span><span class="lock-b">locked</span>', '<span class="lb">关于</span>', 'about lock badge')
# 内部证据入口从产品导航移除
for frag, label in [
    ('        <button class="nav-item" data-v="recommendations"><span class="ic">' + I('star') + '</span><span class="lb">推荐位总览</span></button>\n', 'rec catalog nav'),
    ('        <button class="nav-item" data-v="popups"><span class="ic">' + I('clipboard-list') + '</span><span class="lb">弹窗全集</span></button>\n', 'popups nav'),
    ('        <button class="nav-item" data-v="lightweight"><span class="ic">' + I('play') + '</span><span class="lb">轻量模式</span></button>\n', 'lightweight nav'),
]:
    assert frag in t, label
    t = t.replace(frag, '', 1)
    print('OK removed', label)
repl('<span class="lb">状态面板</span></button>', '<span class="lb">状态面板</span></button>', 'noop')
# 插件区第二项改指设置里的插件分组
t = t.replace('data-v="states"><span class="ic">' + I('activity') + '</span><span class="lb">状态面板</span>',
              'data-v="plugins"><span class="ic">' + I('activity') + '</span><span class="lb">更新与状态</span>', 1)
print('OK plugin second entry')

# ---------- 设置 tab 名与状态面板重做 ----------
repl('data-tab="status">服务器状态</span>', 'data-tab="status">服务器与连接</span>', 'status tab label')
status_start = '<div class="tabpane" data-pane="status">'
i = t.index(status_start)
j = t.index('<div class="tabpane" data-pane="ai">', i)
status_new = '''<div class="tabpane" data-pane="status"><div class="grid g2"><div class="set-card"><div class="hd">自动连接</div><div class="kv">
<span class="k">添加后</span><span><select class="sel"><option>自动尝试连接</option><option>等我手动刷新</option></select></span>
<span class="k">打开列表时</span><span><select class="sel"><option>自动同步一次</option><option>不自动同步</option></select></span>
<span class="k">同步间隔</span><span><select class="sel"><option>60 秒</option><option>5 分钟</option><option>仅手动</option></select></span>
<span class="k">连接结果</span><span><span class="badge ok">缓存为排序权重</span></span></div></div>
<div class="set-card"><div class="hd">排序</div><div class="kv">
<span class="k">锁定的服务器</span><span><select class="sel"><option>永远排最前，连不上也不动</option></select></span>
<span class="k">连不上的</span><span><select class="sel"><option>排到列表最后</option><option>保持原位</option></select></span>
<span class="k">其余顺序</span><span><select class="sel"><option>延迟 + 最近玩过 + 在线人数</option></select></span>
<span class="k">不感兴趣</span><span><select class="sel"><option>降权，不隐藏</option></select></span></div></div>
<div class="set-card"><div class="hd">读取游戏里的服务器</div><div class="kv">
<span class="k">自动读取</span><span><select class="sel"><option>开启 · 各实例目录的 servers.dat</option><option>关闭</option></select></span>
<span class="k">隐藏的服务器</span><span><select class="sel"><option>不导入</option><option>一起导入</option></select></span>
<span class="k">快速进入过的</span><span><select class="sel"><option>一起导入</option><option>不导入</option></select></span>
<span class="k">显示内容</span><span><span class="badge off">与游戏内一致</span></span></div></div>
<div class="set-card"><div class="hd">双击进服</div><div class="kv">
<span class="k">优先</span><span><select class="sel"><option>上次玩这个服用的实例</option></select></span>
<span class="k">其次</span><span><select class="sel"><option>上次用过的实例</option></select></span>
<span class="k">范围</span><span><select class="sel"><option>只选版本兼容的实例</option></select></span>
<span class="k">锁定实例</span><span><select class="sel"><option>按锁定的来</option></select></span></div></div></div>
<div class="panel" style="margin-top:12px"><div class="panel-head"><div class="panel-title">现在读到的</div><div class="panel-sub">来自游戏自己保存的服务器列表</div><div class="panel-tools"><button class="btn tiny" id="setSrvScan">重新读取</button><span class="badge ok" id="setSrvState">3 个实例目录 · 5 台服务器</span></div></div>
<div class="stack" style="font-size:12px;color:var(--ink-2)"><div>服务器名字、地址、图标都在游戏目录的 servers.dat 里；加过服务器或进过服以后游戏会自动生成。</div><div>列表分「可见」和「隐藏」两份，快速进入过的地址会进隐藏那份；这里只读、不改游戏的文件。</div></div></div></div>'''
t = t[:i] + status_new + t[j:]
print('OK status pane replaced')

# ---------- 其余 pane 的工程词收口 ----------
t = t.replace('data-v="recommendations">查看推荐位总览', 'data-v="servers">查看服务器排序', 1)
t = t.replace('data-v="recommendations">总览页', 'data-v="servers">看排序', 1)
t = t.replace('data-v="slots">查看槽位图', 'data-v="plugins">查看插件', 1)
t = t.replace('data-v="handoff">查看底层交接基线', 'data-v="about">查看关于', 1)
t = t.replace('只写 slot:plugin.*，core.* 拒绝', '插件只能加自己的位置', 1)
t = t.replace('摘要 + 签名 + ABI 主版本', '校验来源与版本', 1)
t = t.replace('高风险插件进程隔离', '插件单独运行，不影响启动器', 1)
t = t.replace('默认只升；回滚需显式比较器', '只更新到新版本，可回滚', 1)
t = t.replace('保留旧插件，核心不动', '失败保留原来的插件', 1)
t = t.replace('plugin.nav.recommend', '推荐位', 1)
t = t.replace('plugin.nav.status', '状态显示', 1)
t = t.replace('核心 0.0.0 未替换', '启动器本体未改动', 1)
t = t.replace('F012 方案待批准', '暂未启用', 1)
t = t.replace('Tier3 + build-std（待验证）', 'Win7 兼容（试验中）', 1)
t = t.replace('未证实，不写死', '暂未启用', 1)
t = t.replace('共用策略引擎', '统一记录', 1)
t = t.replace('KCU 不预设地址；其他应用带 AI 容器时由用户自行填写。设置内只放配置，不做业务入口。',
              '地址由你自己填；不填就不会连接。', 1)
t = t.replace('设置内只放配置，不做业务入口。', '', 1)
t = t.replace('未证实项只登记开关，不产生实现行为。', '试验中的功能默认关闭，改动只影响当前实例。', 1)
print('OK pane wording')

# ---------- 关于页：删工程卡片与候选表 ----------
about_anchor = '        <div class="grid g2" style="margin-top:12px">\n          <div class="panel"><div class="panel-head"><div class="panel-title">核心槽位 · 锁定</div>'
if about_anchor in t:
    k = t.index(about_anchor)
    # 到「开源致谢」面板前
    end = t.index('        <div class="panel" style="margin-top:12px"><div class="panel-head"><div class="panel-title">开源致谢</div>', k)
    t = t[:k] + t[end:]
    print('OK about engineering cards removed')
t = t.replace('<div class="panel-sub">版本与许可证</div><div class="panel-tools"><button class="btn primary tiny" data-v="licenses">' + I('scale') + ' 查看第三方许可</button></div>',
              '<div class="panel-sub">版本与开源许可</div><div class="panel-tools"><button class="btn primary tiny" data-v="licenses">' + I('scale') + ' 第三方许可</button></div>', 1)
t = t.replace('<span class="k">本项目许可证</span><span><span class="badge miss">LICENSE 未生成</span></span>',
              '<span class="k">开源许可</span><span>见「第三方许可」</span>', 1)
t = t.replace('<span class="k">纸质样板</span><span>仅质感参考，不复制代码与品牌</span>',
              '<span class="k">界面</span><span>纸质质感 · 深浅两套主题</span>', 1)
t = t.replace('<div class="panel-sub">文档层登记，未复制代码</div>', '<div class="panel-sub">感谢这些项目</div>', 1)
t = t.replace('<div class="panel-sub">16 组组件 · 按许可证分组 · 离线可读</div>', '<div class="panel-sub">按许可证分组 · 离线可读</div>', 1)
t = t.replace('<span class="badge up">演示层已使用 1 组</span><span class="badge off">进入 src/ 构建 0 项</span>',
              '<span class="badge up">按许可证分组</span>', 1)
print('OK about wording')

# ---------- 许可页构建状态列 ----------
t = t.replace('<th>构建状态</th>', '<th>说明</th>', 1)
print('OK license header')

# ---------- 首页推荐卡按钮 ----------
t = t.replace('data-v="sync">' + I('database') + ' 缓存与刷新', 'data-v="servers">' + I('server') + ' 服务器列表', 1)
print('OK home rec button')

# ---------- 服务器页整体替换 ----------
srv_start = t.index('<section class="view" data-view="servers">')
srv_end = t.index('</section>', srv_start) + len('</section>')
LB = ('<div class="logicbar" data-lb="servers"><span class="lb-t">' + I('refresh-cw') +
      ' 自动同步 · <b class="lb-age">12 秒前</b></span><span class="lb-t">' + I('activity') +
      ' <b class="lb-hit">4</b> 台连得上 / <b class="lb-miss">1</b> 台连不上</span><span class="lb-sp"></span>' +
      '<span class="badge ok lb-state">已同步</span><button class="btn lb-soft">' + I('refresh-cw') +
      ' 重新连接</button><button class="btn lb-hard">' + I('rotate-ccw') + ' 重读游戏列表</button></div>')
srv_new = '''<section class="view" data-view="servers">
        ''' + LB + '''
        <div class="grid" style="grid-template-columns:1.35fr 1fr">
          <div class="stack">
            <div class="panel"><div class="panel-head"><div class="panel-title">服务器</div><div class="panel-sub">和游戏里看到的一样 · 双击直接进服</div>
              <div class="panel-tools"><button class="btn tiny" id="srvRecRefresh">''' + I('refresh-cw') + ''' 重新连接</button><button class="btn primary tiny" id="srvAdd">''' + I('plus') + ''' 添加服务器</button><span class="badge up" id="srvRecTime">上次同步 12 秒前</span></div></div>
              <div id="recSrvList"></div></div>
            <div class="panel"><div class="panel-head"><div class="panel-title">全部服务器</div><div class="panel-sub">排序按连接结果自动更新 · 锁定的不会掉下去</div></div>
              <div id="srvAllBody"></div></div>
          </div>
          <div class="stack">
            <div class="panel"><div class="panel-head"><div class="panel-title">排序规则</div></div>
              <table class="rank-tb"><tbody>
                <tr><td>1</td><td>锁定的服务器，连不上也排最前</td></tr>
                <tr><td>2</td><td>连得上、延迟低、最近玩过</td></tr>
                <tr><td>3</td><td>在线人数与版本兼容度</td></tr>
                <tr><td>4</td><td>连不上的排到最后</td></tr>
              </tbody></table><div class="mut" style="font-size:11px;margin-top:9px">每次连接的结果会记下来，下次打开直接按这个顺序排；不感兴趣只降权，不会消失。</div></div>
            <div class="panel"><div class="panel-head"><div class="panel-title">自动同步</div><div class="panel-tools"><button class="btn tiny" id="srvScan">''' + I('database') + ''' 重新读取</button><span class="badge ok" id="srvScanState">3 个实例目录</span></div></div>
              <div class="stack" style="font-size:12px;color:var(--ink-2)">
                <div>添加完服务器就自动连一次，结果缓存下来作为排序依据。</div>
                <div>游戏自己会把服务器名单存在目录里的 servers.dat，启动器会自动读取；快速进入过的地址也能找到。</div>
                <div>显示的名字、图标、公告、人数和延迟都照游戏内的样子，不另做一套。</div>
              </div>
              <div class="attach" style="margin-top:9px" id="srvScanLog">[KCU] servers.dat 可见 4 · 隐藏 2 · 快速进入 1<br>[KCU] 连接 4 成功 / 1 失败 · 锁定 2 台保持靠前</div></div>
            <div class="panel"><div class="panel-head"><div class="panel-title">双击进服</div></div>
              <div class="stack" style="font-size:12px;color:var(--ink-2)">
                <div>先看「上次玩这个服用的实例」，再看「上次用过的实例」，只在版本兼容的范围里挑。</div>
                <div>你锁定过实例就按锁定的来；没有合适的实例会让你换一个，不会静默失败。</div>
              </div><div class="row" style="margin-top:9px"><button class="btn tiny" id="srvBindDemo">看一次实例选择</button></div></div>
            <div class="panel"><div class="panel-head"><div class="panel-title">连接前提示</div></div>
              <div class="notice" style="box-shadow:none;padding:9px"><div class="notice-ico">''' + I('shield-check') + '''</div><div class="notice-main"><div class="notice-body">连接外部服务器会外传 IP 与 UUID，首次连接会问一次；之后不再打断。</div></div></div></div>
          </div>
        </div>
      </section>'''
t = t[:srv_start] + srv_new + t[srv_end:]
print('OK servers view replaced')

# ---------- VIEW_META 收口 ----------
repl("settings:['设置','9 个分组 · 配置归拢 · slot:core.locked.settings 插件不可覆盖']",
     "settings:['设置','改动立即生效 · 可搜索 · 一键恢复默认']", 'meta settings')
repl("servers:['服务器','推荐位 · 状态设置入口 · 测速缓存 60s']",
     "servers:['服务器','自动连接 · 结果缓存为排序权重 · 双击直接进服']", 'meta servers')
repl("about:['关于','核心槽位锁定 · 第三方许可 · 交接基线']",
     "about:['关于','版本 · 开源许可 · 致谢']", 'meta about')
repl("licenses:['第三方许可','关于 → 第三方许可 · 16 组 · 离线可读']",
     "licenses:['第三方许可','按许可证分组 · 离线可读']", 'meta licenses')
repl("recommendations:['推荐位总览','10 处推荐 · 权重 / 覆盖 / 刷新']",
     "recommendations:['推荐位总览','内部设计证据 · 不进产品导航']", 'meta recommendations')
repl("handoff:['底层交接基线','新对话把本仓库当底层直接接续']",
     "handoff:['底层交接基线','内部设计证据 · 不进产品导航']", 'meta handoff')
repl("upperstack:['上层实现候选','12 组第三方库 · 许可证与复用边界']",
     "upperstack:['上层实现候选','内部设计证据 · 不进产品导航']", 'meta upperstack')
repl("slots:['插件槽位与锁定','core.locked.* 不可占用 · plugin.* 开放']",
     "slots:['插件槽位与锁定','内部设计证据 · 不进产品导航']", 'meta slots')

# ---------- 内部证据区块标注（产品导航已不可达） ----------
for v in ['slots', 'recommendations', 'handoff', 'upperstack']:
    t = t.replace('<section class="view" data-view="' + v + '">',
                  '<section class="view" data-internal="1" data-view="' + v + '">', 1)
print('OK internal sections marked')

p.write_text(t)
print('STEP_A_OK', p.stat().st_size, 'sections', t.count('<section class="view'))

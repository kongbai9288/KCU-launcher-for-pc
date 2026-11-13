from pathlib import Path
import re

p = Path('demos/ui-full-kcu-paper.html')
t = p.read_text()


def I(n):
    return '<svg class="li" aria-hidden="true"><use href="#i-' + n + '"></use></svg>'


css = '''
.set-tabs{display:flex;flex-wrap:wrap;gap:6px;margin-bottom:12px;padding-bottom:10px;border-bottom:1px solid var(--line)}
.set-tabs .chip{cursor:pointer;font-size:11px}
.set-tabs .chip.on{font-weight:600}
.tabpane{display:none}
.tabpane.on{display:block}
.setid{font-size:10px;color:var(--ink-3);display:block;margin-top:2px;letter-spacing:.2px}
.slot-core{background:var(--sel);border:1px dashed var(--accent);border-radius:var(--r-md);padding:8px 10px;margin:0 6px 6px}
.slot-core .sh{display:flex;align-items:center;gap:5px;font-size:10px;color:var(--accent);font-weight:600;letter-spacing:.3px;margin-bottom:5px}
.slot-core .nav-item{height:32px;font-size:12px}
.slot-plugin{margin:0 6px 6px;padding:7px 10px;border:1px solid var(--line);border-radius:var(--r-md)}
.slot-plugin .sh{font-size:10px;color:var(--ink-3);margin-bottom:5px;display:flex;align-items:center;gap:5px}
.slot-plugin .nav-item{height:30px;font-size:12px}
.lock-b{font-size:9px;border:1px solid var(--accent);color:var(--accent);border-radius:8px;padding:0 5px;margin-left:auto;white-space:nowrap}
.win.narrow .slot-core .sh,.win.narrow .slot-plugin .sh{font-size:0}
.win.narrow .lock-b{display:none}
.rec-tb{width:100%;border-collapse:collapse;font-size:11px}
.rec-tb th{text-align:left;color:var(--ink-3);font-weight:500;padding:7px 8px;border-bottom:1px solid var(--line);background:var(--card-2)}
.rec-tb td{padding:7px 8px;border-bottom:1px solid var(--line);color:var(--ink-2)}
.status-dot{width:9px;height:9px;border-radius:99px;display:inline-block;margin-right:6px;background:var(--ink-3)}
.status-dot.ok{background:#6E9E72}.status-dot.mt{background:#C79A4E}.status-dot.off{background:#9A968C}.status-dot.err{background:#B8543F}
.mini{font-size:10px;color:var(--ink-3)}
'''
t = t.replace('</style>\n', '\n' + css + '\n</style>\n', 1)

nav_new = '''    <nav class="nav" id="nav">
      <button class="nav-item active" data-v="home"><span class="ic">''' + I('house') + '''</span><span class="lb">首页</span></button>
      <button class="nav-item" data-v="notices"><span class="ic">''' + I('mail') + '''</span><span class="lb">公告中心</span><span class="cnt">3</span></button>
      <button class="nav-item" data-v="instances"><span class="ic">''' + I('layout-grid') + '''</span><span class="lb">实例与版本</span><span class="cnt">7</span></button>
      <button class="nav-item" data-v="servers"><span class="ic">''' + I('server') + '''</span><span class="lb">服务器</span></button>
      <button class="nav-item" data-v="download"><span class="ic">''' + I('download') + '''</span><span class="lb">下载中心</span></button>
      <button class="nav-item" data-v="mods"><span class="ic">''' + I('boxes') + '''</span><span class="lb">模组管理</span><span class="cnt">110</span></button>
      <button class="nav-item" data-v="login"><span class="ic">''' + I('user-round') + '''</span><span class="lb">账号登录</span></button>
      <button class="nav-item" data-v="serverhost"><span class="ic">''' + I('terminal') + '''</span><span class="lb">开服器</span></button>
      <button class="nav-item" data-v="logs"><span class="ic">''' + I('scroll-text') + '''</span><span class="lb">日志诊断</span></button>
      <div class="nav-sep"></div>
      <div class="slot-plugin"><div class="sh">''' + I('puzzle') + ''' 插件区 · slot:plugin.*</div>
        <button class="nav-item" data-v="slots"><span class="ic">''' + I('layout-grid') + '''</span><span class="lb">推荐插件</span><span class="cnt">2</span></button>
        <button class="nav-item" data-v="slots"><span class="ic">''' + I('activity') + '''</span><span class="lb">状态面板</span></button>
      </div>
      <div class="nav-foot">
        <div class="slot-core"><div class="sh">''' + I('lock-keyhole') + ''' 核心槽位 · 锁定 · 插件不可占用</div>
          <button class="nav-item" data-v="settings"><span class="ic">''' + I('settings') + '''</span><span class="lb">设置</span><span class="lock-b">locked</span></button>
          <button class="nav-item" data-v="about"><span class="ic">''' + I('info') + '''</span><span class="lb">关于</span><span class="lock-b">locked</span></button>
        </div>
        <button class="nav-item" data-v="recommendations"><span class="ic">''' + I('star') + '''</span><span class="lb">推荐位总览</span></button>
        <button class="nav-item" data-v="popups"><span class="ic">''' + I('clipboard-list') + '''</span><span class="lb">弹窗全集</span></button>
        <button class="nav-item" data-v="lightweight"><span class="ic">''' + I('play') + '''</span><span class="lb">轻量模式</span></button>
        <button class="nav-item" id="btnCollapse"><span class="ic">''' + I('chevrons-left') + '''</span><span class="lb">收起侧栏</span></button>
      </div>
    </nav>'''
t, n = re.subn(r'    <nav class="nav" id="nav">[\s\S]*?</nav>', lambda m: nav_new, t, count=1)
assert n == 1, 'nav'
print('NAV_OK')

LB = ('          <div class="logicbar" data-lb="settings"><span class="lb-t">' + I('database') +
      ' 已缓存 · <b class="lb-age">12 秒前</b></span><span class="lb-t">' + I('gauge') +
      ' 命中 <b class="lb-hit">8</b> / 未命中 <b class="lb-miss">1</b></span><span class="lb-sp"></span>' +
      '<span class="badge ok lb-state">就绪</span><button class="btn lb-soft">' + I('refresh-cw') +
      ' 刷新</button><button class="btn lb-hard">' + I('rotate-ccw') + ' 强制刷新</button></div>')
TABS = [('general', '常规'), ('download', '下载与镜像'), ('cache', '缓存与刷新'),
        ('recommend', '推荐与排序'), ('status', '服务器状态'), ('ai', 'AI 容器接口'),
        ('plugins', '插件与更新'), ('privacy', '隐私与诊断'), ('experimental', '实验性')]
tabbar = ('<div class="set-tabs">' + ''.join('<span class="chip' + (' on' if k == 'general' else '') +
          '" data-tab="' + k + '">' + v + '</span>' for k, v in TABS) +
          '<span class="chip" id="tabModified">@modified 3</span><span class="chip" id="tabReset">恢复默认</span></div>')


def card(title, rows):
    body = ''.join('<span class="k">' + a + '</span><span>' + b + '<span class="setid">' + c + '</span></span>' for a, b, c in rows)
    return '<div class="set-card"><div class="hd">' + title + '</div><div class="kv">' + body + '</div></div>'


panes = []
panes.append(('general', '<div class="grid g2">' +
    card('常规', [('界面语言', '<select class="sel"><option>简体中文</option><option>English</option></select>', 'core.ui.language'),
                  ('主题', '<select class="sel"><option>纸质浅色（默认）</option><option>深色纸质</option><option>跟随系统</option></select>', 'core.ui.theme'),
                  ('数据目录', '<input class="txt" value="C:\\KCU" readonly>', 'core.paths.data_dir'),
                  ('公告提示', '<select class="sel"><option>未读时铃铛提示</option><option>静默</option></select>', 'core.notices.badge')]) +
    card('启动与实例', [('EULA', '<select class="sel"><option>启动前写入</option></select>', 'core.server.eula_timing'),
                    ('崩溃后', '<select class="sel"><option>按日志自动重启</option></select>', 'core.server.crash_restart'),
                    ('旧版 jar', '<select class="sel"><option>写 lockfile 禁用</option></select>', 'core.instance.legacy_lock'),
                    ('用户指定', '<select class="sel"><option>永远排第一</option></select>', 'core.rank.user_first')]) +
    '<div class="panel"><div class="panel-head"><div class="panel-title">设置项约定</div></div><div class="stack" style="font-size:11px;color:var(--ink-2)">' +
    '<div>每项有稳定 ID、默认值、作用范围；写后即时生效，失败保留旧值并可见报错。</div>' +
    '<div><span class="badge up">@modified 3</span> 只看改过的项；齿轮可复制 ID / 重置单项。</div>' +
    '<div>插件可在设置内追加自己的分组，不能改写 <b>core.*</b> 项。</div></div></div></div>'))

panes.append(('download', '<div class="grid g2">' +
    card('下载与网络', [('每页条数', '<input class="txt" value="20" readonly>', 'core.net.page_size'),
                    ('批量请求', '<select class="sel"><option>一次带多个 id</option><option>逐条目单发（禁止）</option></select>', 'core.net.batch'),
                    ('并发上限', '<input class="txt" value="3" readonly>', 'core.net.concurrency'),
                    ('单飞去重', '<select class="sel"><option>开启</option></select>', 'core.net.single_flight')]) +
    card('镜像与地域', [('镜像测速', '<select class="sel"><option>开启</option><option>关闭</option></select>', 'core.net.mirror_speedtest'),
                    ('地域软策略', '<select class="sel"><option>区域设置 + 物理位置</option></select>', 'core.net.region_policy'),
                    ('强制境外', '<select class="sel"><option>允许用户自行指定</option></select>', 'core.net.region_override'),
                    ('用途边界', '<span class="badge off">仅下载选择，不复用为地区禁用</span>', 'core.net.region_scope')]) +
    '<div class="panel"><div class="panel-head"><div class="panel-title">自定义项</div></div><div class="stack" style="font-size:11px;color:var(--ink-2)">' +
    '<div>测速源列表、每页条数、超时、重试上限、失败后镜像顺序均可自定义。</div>' +
    '<div>下载域名白名单机制按既有决定先不启用，留高度自定义。</div>' +
    '<div><button class="btn tiny" data-v="recommendations">查看推荐位总览</button> <button class="btn tiny" data-v="refresh">查看刷新机制</button></div></div></div></div>'))

panes.append(('cache', '<div class="grid g2">' +
    card('四层缓存', [('C1 内存', '<input class="txt" value="32 条 / TTL 30s" readonly>', 'core.cache.memory'),
                    ('C2 磁盘', '<input class="txt" value="有界目录 / 24h" readonly>', 'core.cache.disk'),
                    ('C3 网络', '<input class="txt" value="按源 / 60s" readonly>', 'core.cache.network'),
                    ('C4 预取', '<input class="txt" value="8 条 / 会话内" readonly>', 'core.cache.prefetch')]) +
    card('刷新', [('普通刷新', '<select class="sel"><option>取增量，不清缓存</option></select>', 'core.refresh.soft'),
                 ('强制刷新', '<select class="sel"><option>清层重取全量</option></select>', 'core.refresh.hard'),
                 ('事件推送', '<select class="sel"><option>开启，不弹窗不抢焦点</option></select>', 'core.refresh.observer'),
                 ('失败回退', '<select class="sel"><option>保留上次缓存，不空白</option></select>', 'core.refresh.fallback')]) +
    '<div class="panel"><div class="panel-head"><div class="panel-title">操作</div><div class="panel-tools"><button class="btn tiny" data-v="sync">打开四层总控</button></div></div>' +
    '<div class="row"><button class="btn tiny" id="setCacheExpired">仅清过期</button><button class="btn tiny" id="setCacheAll">全清（二次确认）</button>' +
    '<span class="badge up">命中率 88%</span><span class="badge ok">inflight 0</span></div>' +
    '<div class="mut" style="font-size:11px;margin-top:9px">时间戳统一「N 秒前 / N 分钟前 / HH:MM」；取消后 0 副作用扩散。</div></div></div>'))

rec_rows = ''.join('<tr><td>' + a + '</td><td>' + b + '</td><td>' + c + '</td><td><span class="badge ok">开</span></td></tr>' for a, b, c in [
    ('首页启动卡', '上次实例 / 最近 3 个', '最近使用 > 推荐'),
    ('首页推荐服务器', '兼容 + 习惯', '用户指定 > 兼容度 > 延迟'),
    ('版本页', '稳定版', '稳定 > 快照'),
    ('下载页', '缺失依赖 / 可更新', '缺依赖优先'),
    ('模组页', '可更新 / 缺依赖', '缺失优先'),
    ('公告中心', '置顶', '置顶 > 时间'),
    ('加载器', '与实例兼容', '兼容度 > 热度'),
    ('Java', '稳定版本', '稳定 > 预览'),
    ('镜像源', '测速结果', '延迟 > 可用性'),
    ('插件', '已装且启用', '用户评分 > 更新日')])
panes.append(('recommend', '<div class="grid g2">' +
    card('推荐总控', [('推荐总开关', '<select class="sel"><option>开启</option><option>关闭</option></select>', 'core.rec.enabled'),
                     ('权重可自定义', '<select class="sel"><option>允许调数值与顺序</option></select>', 'core.rec.weights_editable'),
                     ('用户指定', '<select class="sel"><option>永远排第一</option></select>', 'core.rec.user_first'),
                     ('不感兴趣', '<select class="sel"><option>降权，不隐藏</option></select>', 'core.rec.dismiss')]) +
    card('来源与刷新', [('推荐来源', '<select class="sel"><option>本地 + 官方 + 插件</option></select>', 'core.rec.sources'),
                     ('刷新方式', '<select class="sel"><option>事件驱动 + 定时软刷新</option></select>', 'core.rec.refresh'),
                     ('缓存', '<input class="txt" value="5min / 容量有界" readonly>', 'core.rec.cache'),
                     ('排序口径', '<span class="badge up">10 个推荐位统一</span>', 'core.rec.rank_table')]) +
    '</div><div class="panel" style="margin-top:12px"><div class="panel-head"><div class="panel-title">10 个推荐位</div>' +
    '<div class="panel-sub">每个都可单独开关、调权重、看来源</div><div class="panel-tools"><button class="btn tiny" data-v="recommendations">总览页</button></div></div>' +
    '<table class="rec-tb"><thead><tr><th>位置</th><th>内容</th><th>默认权重</th><th>状态</th></tr></thead><tbody>' + rec_rows + '</tbody></table></div>'))

panes.append(('status', '<div class="grid g2">' +
    card('状态来源', [('探测方式', '<select class="sel"><option>SLP 状态查询 + 手动覆盖</option><option>仅手动</option><option>插件提供</option></select>', 'core.status.source'),
                    ('探测间隔', '<input class="txt" value="60s" readonly>', 'core.status.interval'),
                    ('超时', '<input class="txt" value="3s" readonly>', 'core.status.timeout'),
                    ('状态缓存', '<input class="txt" value="60s / 失败标灰" readonly>', 'core.status.cache')]) +
    card('状态类型', [('在线', '<span class="status-dot ok"></span><span class="mini">SLP 有响应</span>', 'core.status.online'),
                    ('维护中', '<span class="status-dot mt"></span><span class="mini">MOTD 可改</span>', 'core.status.maintenance'),
                    ('离线 / 满员 / 私有', '<span class="status-dot off"></span><span class="mini">可自定义文案</span>', 'core.status.custom'),
                    ('自定义', '<input class="txt" placeholder="自定义文案与颜色">', 'core.status.label')]) +
    '<div class="panel"><div class="panel-head"><div class="panel-title">显示位置与变更历史</div></div>' +
    '<div class="row"><span class="chip on">首页推荐卡</span><span class="chip on">服务器列表</span><span class="chip">状态栏</span><span class="chip">右键菜单</span></div>' +
    '<div class="attach" style="margin-top:9px">[KCU] status srv-01 OK detail=slp 42ms players=3/20<br>[KCU] status srv-02 DEGRADE detail=timeout fallback=last_60s<br>[KCU] status srv-01 OK detail=manual maintenance</div>' +
    '<div class="mut" style="font-size:11px;margin-top:8px">SLP 字段：version.name / protocol、players.max / online / sample、description（text component）、favicon（64×64 PNG base64）、enforcesSecureChat。协议可被禁用，1.7 前后不兼容。</div></div></div>'))

panes.append(('ai', '<div class="grid g2">' +
    card('AI 容器接口', [('接口地址', '<input class="txt" id="setAiAddr" placeholder="用户自填，留空未启用">', 'core.ai.endpoint'),
                      ('连接状态', '<span class="badge off" id="setAiState">未配置</span>', 'core.ai.state'),
                      ('确认粒度', '<select class="sel"><option>每次请求单独确认</option></select>', 'core.ai.confirm'),
                      ('删除权限', '<select class="sel"><option>不给</option></select>', 'core.ai.delete_scope')]) +
    card('边界', [('请求正文', '<span class="badge off">不缓存</span>', 'core.ai.body_cache'),
                 ('审计', '<span class="badge up">共用策略引擎</span>', 'core.ai.audit'),
                 ('关页', '<span class="badge ok">即停请求</span>', 'core.ai.stop_on_close'),
                 ('失败分类', '<span class="mini">地址 / 认证 / 网络 三类</span>', 'core.ai.errors')]) +
    '<div class="panel"><div class="panel-head"><div class="panel-title">测试</div><div class="panel-tools"><button class="btn tiny" data-v="ai">打开独立页</button></div></div>' +
    '<div class="row"><button class="btn primary tiny" id="setAiTest">' + I('zap') + ' 测试连接</button><span class="badge ok" id="setAiResult">待命</span></div>' +
    '<div class="mut" style="font-size:11px;margin-top:9px">KCU 不预设地址；其他应用带 AI 容器时由用户自行填写。设置内只放配置，不做业务入口。</div></div></div>'))

panes.append(('plugins', '<div class="grid g2">' +
    card('插件', [('插件目录', '<input class="txt" value="C:\\KCU\\plugins" readonly>', 'core.plugins.dir'),
                 ('槽位规则', '<select class="sel"><option>只写 slot:plugin.*，core.* 拒绝</option></select>', 'core.plugins.slot_rule'),
                 ('清单校验', '<select class="sel"><option>摘要 + 签名 + ABI 主版本</option></select>', 'core.plugins.verify'),
                 ('隔离', '<select class="sel"><option>高风险插件进程隔离</option></select>', 'core.plugins.isolation')]) +
    card('插件化更新', [('更新通道', '<select class="sel"><option>稳定 / 预览 / 插件化</option></select>', 'core.update.channel'),
                    ('签名校验', '<select class="sel"><option>不可禁用</option></select>', 'core.update.signature'),
                    ('版本比较', '<select class="sel"><option>默认只升；回滚需显式比较器</option></select>', 'core.update.comparator'),
                    ('失败降级', '<select class="sel"><option>保留旧插件，核心不动</option></select>', 'core.update.fallback')]) +
    '<div class="panel"><div class="panel-head"><div class="panel-title">已装插件与更新模拟</div><div class="panel-tools"><button class="btn tiny" data-v="slots">查看槽位图</button></div></div>' +
    '<table class="rec-tb"><thead><tr><th>插件</th><th>槽位</th><th>许可证</th><th>状态</th></tr></thead><tbody>' +
    '<tr><td>推荐插件</td><td>plugin.nav.recommend</td><td>MIT</td><td><span class="badge ok">启用</span></td></tr>' +
    '<tr><td>状态面板</td><td>plugin.nav.status</td><td>Apache-2.0</td><td><span class="badge ok">启用</span></td></tr></tbody></table>' +
    '<div class="row" style="margin-top:9px"><button class="btn tiny" id="plugUpdate">模拟插件化更新</button>' +
    '<button class="btn tiny" id="plugRollback">模拟回滚</button><span class="badge up" id="plugState">核心 0.0.0 未替换</span></div></div></div>'))

panes.append(('privacy', '<div class="grid g2">' +
    card('日志与外传', [('日志上传', '<select class="sel"><option>默认脱敏（可手动关）</option></select>', 'core.privacy.redact'),
                     ('保留期', '<input class="txt" value="30 天" readonly>', 'core.privacy.retention'),
                     ('外传确认', '<select class="sel"><option>每次二次确认</option></select>', 'core.privacy.upload_confirm'),
                     ('审计', '<select class="sel"><option>共用策略引擎</option></select>', 'core.privacy.audit')]) +
    card('文件与凭据', [('文件管理', '<span class="badge off">系统面板 + OS 级防护</span>', 'core.files.system_panel'),
                     ('锁定', '<span class="badge up">lockfile</span>', 'core.files.lockfile'),
                     ('凭据保护', '<span class="badge miss">F012 方案待批准</span>', 'core.credential.guard'),
                     ('诊断包', '<button class="btn tiny" data-v="logs">导出</button>', 'core.diagnostics.export')]) + '</div>'))

panes.append(('experimental', '<div class="grid g2">' +
    card('实验性开关', [('多操作入口', '<select class="sel"><option>关闭</option></select>', 'core.exp.multi_action'),
                      ('Win7 兼容', '<select class="sel"><option>Tier3 + build-std（待验证）</option></select>', 'core.exp.win7'),
                      ('插件化更新灰度', '<select class="sel"><option>关闭</option></select>', 'core.exp.plugin_update'),
                      ('加载器 schema', '<span class="badge miss">未证实，不写死</span>', 'core.exp.loader_schema')]) +
    '<div class="panel"><div class="panel-head"><div class="panel-title">开关约定</div></div><div class="stack" style="font-size:11px;color:var(--ink-2)">' +
    '<div>实验项默认关闭；改动只影响本实例，重启后读盘。</div>' +
    '<div>未证实项只登记开关，不产生实现行为。</div>' +
    '<div><button class="btn tiny" data-v="handoff">查看底层交接基线</button></div></div></div></div>'))

pane_html = ''.join('<div class="tabpane' + (' on' if k == 'general' else '') + '" data-pane="' + k + '">' + v + '</div>' for k, v in panes)
settings_new = ('<section class="view" data-view="settings">\n' + LB +
    '\n        <div class="panel" style="margin-bottom:12px"><div class="panel-head"><div class="panel-title">设置</div>' +
    '<div class="panel-sub">9 个分组 · 每项有稳定 ID · 写后即时生效 · 可搜索 / @modified / 单项重置</div>' +
    '<div class="panel-tools"><span class="badge ok">slot:core.locked.settings</span><span class="badge up">' +
    I('lock-keyhole') + ' 插件不可覆盖</span></div></div>' + tabbar + '</div>\n' + pane_html + '\n      </section>')
t, n = re.subn(r'<section class="view" data-view="settings">[\s\S]*?</section>', lambda m: settings_new, t, count=1)
assert n == 1, 'settings'
print('SETTINGS_OK panes', len(panes))

about_add = '''
        <div class="grid g2" style="margin-top:12px">
          <div class="panel"><div class="panel-head"><div class="panel-title">核心槽位 · 锁定</div><div class="panel-sub">slot:core.locked.*</div><div class="panel-tools"><button class="btn tiny" data-v="slots">槽位图</button></div></div>
            <div class="kv"><span class="k">设置</span><span>core.locked.settings · 固定位置</span>
              <span class="k">关于</span><span>core.locked.about · 固定位置</span>
              <span class="k">插件可写</span><span>仅 slot:plugin.*</span>
              <span class="k">冲突处置</span><span><span class="badge err">拒绝注册 + 诊断行</span></span></div>
            <div class="mut" style="font-size:11px;margin-top:9px">更新包与插件不能改写、隐藏、重排这两个槽位，否则下次更新会把设置与关于顶掉。</div></div>
          <div class="panel"><div class="panel-head"><div class="panel-title">底层交接基线</div><div class="panel-sub">新对话可把本仓库当底层直接接续</div><div class="panel-tools"><button class="btn tiny" data-v="handoff">打开交接页</button></div></div>
            <div class="stack" style="font-size:12px;color:var(--ink-2)">
              <div>基线：`kongbai9288/KCU-launcher-for-pc` / main / public，不含任何凭据与私有配置。</div>
              <div>必读顺序：docs/index.md 78 项；不可变边界写在 `docs/design/handoff.md`。</div>
              <div>已完成：L1 core、L2 dispatcher、L3 lightweight；UI 仍是演示层。</div>
              <div>更新：优先插件化更新，核心不随更新替换；失败保留旧插件。</div>
            </div></div>
        </div>
        <div class="panel" style="margin-top:12px"><div class="panel-head"><div class="panel-title">上层实现采用第三方代码</div><div class="panel-sub">候选清单 · 未进入 src/ 构建 · 逐项取得 LICENSE 全文后才允许复用</div><div class="panel-tools"><button class="btn tiny" data-v="licenses">许可清单</button></div></div>
          <table class="lic-table"><thead><tr><th>层</th><th>候选</th><th>许可证</th><th>用途</th><th>复制状态</th></tr></thead><tbody id="upperBody"></tbody></table></div>'''
anchor = '        <div class="panel" style="margin-top:12px"><div class="panel-head"><div class="panel-title">开源致谢</div>'
assert anchor in t, 'about anchor'
t = t.replace(anchor, about_add + '\n' + anchor, 1)
print('ABOUT_OK')
p.write_text(t)
print('STEP_A_OK', p.stat().st_size)

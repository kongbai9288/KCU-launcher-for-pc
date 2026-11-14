from pathlib import Path
import re, hashlib

p = Path('demos/ui-full-kcu-paper.html')
t = p.read_text()


def R(a, b, label, count=1, regex=False):
    global t
    if regex:
        t2, n = re.subn(a, b, t, count=count)
        assert n >= 1, ('REGEX_MISS', label)
        t = t2
    else:
        assert a in t, ('MISS', label, a[:90])
        t = t.replace(a, b, count)
    print('OK', label)


def Rall(a, b, label):
    global t
    assert a in t, ('MISS', label)
    n = t.count(a)
    t = t.replace(a, b)
    print('OK', label, 'x', n)


# ============ 1. CSS ============
css = '''
.srv-ms{font-size:10px;color:var(--ink-3);margin-top:2px;text-align:right;font-variant-numeric:tabular-nums}
.rename-btn{border:none;background:none;cursor:pointer;color:var(--ink-3);font-size:11px;padding:0 3px;margin-left:4px;vertical-align:1px}
.rename-btn:hover{color:var(--accent)}
.tb-lang{font-size:11px;letter-spacing:.3px}
.same-tag{display:inline-block;font-size:10px;color:var(--accent);border:1px solid var(--line-2);border-radius:3px;padding:0 5px;margin-left:6px}
'''
R('</style>\n', css + '</style>\n', 'css')

# ============ 2. 标题栏语言按钮 ============
R('<button class="tb-icon" id="btnTheme" title="切换主题">',
  '<button class="tb-icon tb-lang" id="btnLang" title="界面语言" data-i18n-title="lang.switch">中</button>\n    <button class="tb-icon" id="btnTheme" title="切换主题">',
  'lang button')
R('<div class="tb-name"><b>KCU Launcher</b> · 桌面端</div>',
  '<div class="tb-name"><b>KCU Launcher</b> · <span data-i18n="app.desktop">桌面端</span></div>',
  'tb name')
R('<input type="text" placeholder="搜索实例、模组、设置">',
  '<input type="text" placeholder="搜索实例、模组、设置" data-i18n-ph="search.hint">',
  'search ph')

# ============ 3. 导航项加 data-i18n ============
nav_a = t.index('<nav class="nav" id="nav">')
nav_b = t.index('</nav>', nav_a)
nav = t[nav_a:nav_b]
nav_new, n = re.subn(
    r'(<button class="nav-item[^"]*" data-v="([a-z-]+)"[^>]*>[\s\S]*?<span class="lb">)([^<]+)(</span>)',
    lambda m: m.group(1).replace('<span class="lb">', '<span class="lb" data-i18n="nav.' + m.group(2) + '">') + m.group(3) + m.group(4),
    nav)
assert n >= 9, ('NAV', n)
t = t[:nav_a] + nav_new + t[nav_b:]
print('OK nav i18n x', n)

# ============ 4. 逻辑条通用文案 ============
Rall(' 上次更新 · <b class="lb-age">',
     ' <span data-i18n="cache.updated">上次更新</span> · <b class="lb-age">',
     'logicbar updated')
R(r'(<button class="btn lb-soft">[\s\S]*?</svg>)\s*刷新(</button>)',
  r'\1 <span data-i18n="act.refresh">刷新</span>\2', 'logicbar soft', count=0, regex=True)
R(r'(<button class="btn lb-hard">[\s\S]*?</svg>)\s*重新获取(</button>)',
  r'\1 <span data-i18n="act.hard">重新获取</span>\2', 'logicbar hard', count=0, regex=True)
Rall('<span class="badge ok lb-state">就绪</span>',
     '<span class="badge ok lb-state" data-i18n="state.ready">就绪</span>',
     'logicbar state')
Rall('<span class="badge ok lb-state">已同步</span>',
     '<span class="badge ok lb-state" data-i18n="state.synced">已同步</span>',
     'logicbar synced')

# ============ 5. 设置 tabs / 面板 ============
R('<div class="panel-title">设置</div><div class="panel-sub">改动立即生效 · 可搜索 · 只看改过的项 · 一键恢复默认</div>',
  '<div class="panel-title" data-i18n="settings.title">设置</div><div class="panel-sub" data-i18n="settings.sub">改动立即生效 · 可搜索 · 只看改过的项 · 一键恢复默认</div>',
  'settings head')
R(r'(<span class="chip[^"]*" data-tab="([a-z-]+)"[^>]*)(>)([^<]+)(</span>)',
  r'\1 data-i18n="tab.\2"\3\4\5', 'settings tabs', count=0, regex=True)

# 崩溃反馈 tab（放在隐私与诊断前）
R('<span class="chip" data-tab="privacy" data-i18n="tab.privacy">隐私与诊断</span>',
  '<span class="chip" data-tab="crash">崩溃反馈</span><span class="chip" data-tab="privacy" data-i18n="tab.privacy">隐私与诊断</span>',
  'crash tab')
t = t.replace('<span class="chip" data-tab="crash">崩溃反馈</span>',
              '<span class="chip" data-tab="crash" data-i18n="tab.crash">崩溃反馈</span>', 1)

# 界面语言下拉绑定 id
R('<span class="k">界面语言</span><span><select class="sel"><option>简体中文</option><option>English</option></select></span>',
  '<span class="k" data-i18n="set.lang">界面语言</span><span><select class="sel" id="setLang"><option value="zh-CN">简体中文</option><option value="en-US">English</option></select></span>',
  'setLang select')

# ============ 6. 崩溃反馈 pane ============
crash_pane = '''<div class="tabpane" data-pane="crash"><div class="grid g2">
<div class="set-card"><div class="hd" data-i18n="crash.card">崩溃反馈</div><div class="kv">
<span class="k" data-i18n="crash.enable">出问题时记录</span><span><select class="sel" id="setCrashOn"><option value="off" data-i18n="crash.off">先问我，再发送</option><option value="local" data-i18n="crash.local">只留在本地</option><option value="off2" data-i18n="crash.never">不记录</option></select></span>
<span class="k" data-i18n="crash.addr">接收地址</span><span><input class="txt" id="setCrashAddr" placeholder="由用户自己填写，留空不外发" data-i18n-ph="crash.addrph"></span>
<span class="k" data-i18n="crash.mask">先抹掉私人信息</span><span><select class="sel" id="setCrashMask"><option data-i18n="crash.maskon">默认抹掉（可手动关）</option><option data-i18n="crash.maskoff">不抹掉</option></select></span>
<span class="k" data-i18n="crash.dir">诊断包位置</span><span><input class="txt" value="C:\\KCU\\diagnostics" readonly></span></div></div>
<div class="set-card"><div class="hd" data-i18n="crash.what">会记下什么</div><div class="stack" style="font-size:12px;color:var(--ink-2)">
<div data-i18n="crash.what1">出错时的窗口、版本、系统版本与出错前的操作步骤。</div>
<div data-i18n="crash.what2">服务器地址、聊天、玩家名与存档内容默认不进诊断包。</div>
<div data-i18n="crash.what3">发送前会弹一次确认，能看完整内容，也能直接取消。</div>
<div data-i18n="crash.what4">不填接收地址就只存本地，随时可以自己导出。</div></div>
<div class="row" style="margin-top:10px"><button class="btn tiny" id="crashView" data-i18n="crash.view">看最近一次</button><button class="btn tiny" id="crashExport" data-i18n="crash.export">导出诊断包</button><span class="badge ok" id="crashState" data-i18n="crash.state">未发送</span></div></div></div>
<div class="stack" style="font-size:12px;color:var(--ink-2)"><div data-i18n="crash.note">旧机器、多架构与不同系统版本的行为不完全一样；这一类记录交给专门的崩溃分析库处理，不在启动器里自己写一套。</div></div></div>
'''
R('<div class="tabpane" data-pane="privacy">', crash_pane + '<div class="tabpane" data-pane="privacy">', 'crash pane')

# ============ 7. 服务器页静态文案 i18n ============
R('<div class="panel-title" style="white-space:nowrap">连接范围</div><div class="panel-sub">按机器能力控制同时连几台，连不过来就排队</div>',
  '<div class="panel-title" style="white-space:nowrap" data-i18n="srv.budget">连接范围</div><div class="panel-sub" data-i18n="srv.budgetsub">按机器能力控制同时连几台，连不过来就排队</div>',
  'budget head')
R('<div class="panel-title">自动同步</div>', '<div class="panel-title" data-i18n="srv.autosync">自动同步</div>', 'autosync head')
R('<span>本次可连</span>', '<span data-i18n="srv.limit">本次可连</span>', 'budget limit')
R('<span>同时连接</span>', '<span data-i18n="srv.conc">同时连接</span>', 'budget conc')
R('<span>正在连 / 队列</span>', '<span data-i18n="srv.flight">正在连 / 队列</span>', 'budget flight')
R('<span>本次不连</span>', '<span data-i18n="srv.skip">本次不连</span>', 'budget skip')
R('id="budSwitch">切到轻量档</button><button class="btn tiny" id="budCancel">停止本次同步</button>',
  'id="budSwitch" data-i18n="srv.tier">切到轻量档</button><button class="btn tiny" id="budCancel" data-i18n="srv.stop">停止本次同步</button>',
  'budget buttons')
R('<div class="set-card"><div class="hd">设备连接范围</div>',
  '<div class="set-card"><div class="hd" data-i18n="srv.devcard">设备连接范围</div>', 'dev card')
R('<div>连不上也从没成功过的，按原来的权重留在列表里，不再反复占用连接；锁定过的始终排最前。</div>',
  '<div data-i18n="srv.note1">连不上也从没成功过的，按原来的权重留在列表里，不再反复占用连接；锁定过的始终排最前。</div><div data-i18n="srv.note2">名字可以重复、也可以随时改；同名服务器各归各，改一个不会动到另一个。</div>',
  'server settings note')

# ============ 8. SERVERS 加 sid + 同名演示项 ============
start = t.index('const SERVERS=[')
end = t.index('\n];', start) + 3
block = t[start:end]


def add_sid(m):
    line = m.group(0)
    ipm = re.search(r"ip:'([^']+)'", line)
    ip = ipm.group(1) if ipm else 'unknown'
    sid = 'sv-' + hashlib.sha1(ip.encode()).hexdigest()[:8]
    return line.replace("{id:'", "{sid:'" + sid + "',id:'", 1)


block2 = re.sub(r"\{id:'s\d+',[^\n]*", add_sid, block)
assert block2.count("sid:'sv-") >= 8, 'SID inject'
s9 = " {id:'s9',sid:'sv-taowa2b',name:'陶瓦联机 · 主服',ip:'mc.taowa2.example:25566',ver:'1.21.4',motd:'§a§l陶瓦联机 §7| §f备用入口\\n§7同一个名字，另一台机器',online:8,max:60,ping:96,ok:true,lock:false,ever:true,tried:true,last:'昨天',inst:'生存季',src:'servers.dat'},\n"
block2 = block2.rstrip()[:-2].rstrip() + ',\n' + s9 + '];\n'
t = t[:start] + block2 + t[end:]
print('OK servers sid + same-name')

# ============ 9. pingBars 延迟小字 + srvRow 走 sid / 改名按钮 / i18n ============
R("function pingBars(s){\n  if(!s.ok)return '<span class=\"mut\" style=\"font-size:10px\">连不上</span>';",
  "function pingBars(s){\n  if(!s.ok)return '<span class=\"mut\" style=\"font-size:10px\">'+tr('srv.offline','连不上')+'</span>';",
  'pingBars offline')
R("  return '<span class=\"srv-ping\">'+[1,2,3,4,5].map(i=>'<i style=\"'+(i>n?'opacity:.2':'')+'\"></i>').join('')+'</span>';\n}",
  "  return '<span class=\"srv-ping\">'+[1,2,3,4,5].map(i=>'<i style=\"'+(i>n?'opacity:.2':'')+'\"></i>').join('')+'</span><div class=\"srv-ms\">'+s.ping+' ms</div>';\n}",
  'pingBars ms')

# srvNote 走 tr
R("  if(s.lock)return '<span class=\"srv-note\">已锁定</span>';",
  "  if(s.lock)return '<span class=\"srv-note\">'+tr('srv.locked','已锁定')+'</span>';", 'note locked')
R("  if(s.isNew)return '<span class=\"srv-note\">新加 · 待连接</span>';",
  "  if(s.isNew)return '<span class=\"srv-note\">'+tr('srv.new','新加 · 待连接')+'</span>';", 'note new')
R("  if(s.probeSkip==='never')return '<span class=\"srv-note\">还没连上过 · 暂不重试</span>';",
  "  if(s.probeSkip==='never')return '<span class=\"srv-note\">'+tr('srv.never','还没连上过 · 暂不重试')+'</span>';", 'note never')
R("  if(s.probeSkip==='out')return '<span class=\"srv-note\">超出本次范围 · 用上次结果</span>';",
  "  if(s.probeSkip==='out')return '<span class=\"srv-note\">'+tr('srv.out','超出本次范围 · 用上次结果')+'</span>';", 'note out')
R("  if(!s.ok)return '<span class=\"srv-note\">连不上 · 排到最后</span>';",
  "  if(!s.ok)return '<span class=\"srv-note\">'+tr('srv.fail','连不上 · 排到最后')+'</span>';", 'note fail')

R("  const star='<span class=\"lock-star\" data-lock=\"'+s.id+'\" title=\"锁定/取消锁定\">'+(s.lock?'★':'☆')+'</span>';",
  "  const star='<span class=\"lock-star\" data-lock=\"'+s.sid+'\" title=\"'+tr('srv.locktip','锁定/取消锁定')+'\">'+(s.lock?'★':'☆')+'</span>';",
  'star sid')
R("'<div class=\"srv-motd\" style=\"color:var(--ink-3)\">'+(s.probeSkip==='never'?'还没有成功的连接记录':'无法连接到服务器')+'</div>'",
  "'<div class=\"srv-motd\" style=\"color:var(--ink-3)\">'+(s.probeSkip==='never'?tr('srv.norecord','还没有成功的连接记录'):tr('srv.unreachable','无法连接到服务器'))+'</div>'",
  'motd i18n')
R("  const meta='<div class=\"srv-meta\">'+esc(s.last)+' 玩过 · '+esc(s.inst)+srvNote(s)+'</div>';",
  "  const meta='<div class=\"srv-meta\">'+esc(s.last)+' '+tr('srv.played','玩过')+' · '+esc(s.inst)+srvNote(s)+'</div>';",
  'meta i18n')
R("  return '<div class=\"srv-row\" data-join=\"'+s.id+'\">'+ico+'<div class=\"srv-main\"><div class=\"srv-name\">'+star+esc(s.name)+'</div>'+motd+meta+'</div>'+side+'</div>';",
  "  const rn='<button class=\"rename-btn\" data-rename=\"'+s.sid+'\" title=\"'+tr('srv.rename','改名')+'\">✎</button>';\n  const same=SERVERS.filter(x=>x.name===s.name).length>1?'<span class=\"same-tag\" data-i18n=\"srv.same\">同名</span>':'';\n  return '<div class=\"srv-row\" data-join=\"'+s.sid+'\">'+ico+'<div class=\"srv-main\"><div class=\"srv-name\">'+star+esc(s.name)+same+rn+'</div>'+motd+meta+'</div>'+side+'</div>';",
  'srvRow sid/rename/same')

# renderSrv 事件用 sid
R("document.querySelectorAll('[data-lock]').forEach(x=>x.onclick=e=>{e.stopPropagation();const s=SERVERS.find(y=>y.id===x.dataset.lock);s.lock=!s.lock;renderSrv();log('ui','servers','lock','OK','detail='+s.id+' locked='+s.lock);});",
  "document.querySelectorAll('[data-lock]').forEach(x=>x.onclick=e=>{e.stopPropagation();const s=SERVERS.find(y=>y.sid===x.dataset.lock);s.lock=!s.lock;renderSrv();log('ui','servers','lock','OK','detail='+s.sid+' locked='+s.lock);});",
  'lock handler')
R("document.querySelectorAll('[data-join]').forEach(x=>x.ondblclick=()=>openJoin(SERVERS.find(y=>y.id===x.dataset.join)));",
  "document.querySelectorAll('[data-join]').forEach(x=>x.ondblclick=()=>openJoin(SERVERS.find(y=>y.sid===x.dataset.join)));",
  'join handler')
R("  const s=SERVERS.find(x=>x.id==='s2');", "  const s=SERVERS[1];", 'force offline by index')
R("  const s={id:'s'+(SERVERS.length+1),name:'新加的服务器',",
  "  const s={id:'s'+(SERVERS.length+1),sid:'sv-new'+SERVERS.length,name:'新加的服务器',", 'srvAdd sid')

# 改名弹窗 + 事件（插在 openJoin 前）
R('function openJoin(s){', '''function openRename(s){
  const body='<p style="font-size:13px;color:var(--ink);margin-bottom:10px">'+tr('srv.renameTitle','给服务器换个名字')+'</p>'+
   '<input class="txt" id="rnInput" value="'+esc(s.name)+'" style="width:100%;margin-bottom:9px">'+
   '<div class="attach" style="line-height:1.9">'+tr('srv.renameBody','名字可以重复，也可以随时改；改完只换显示名，之前的连接记录、排序与目录都留着。')+'</div>';
  openDlg(tr('srv.renameTitle','给服务器换个名字'),body,'rename_'+s.sid);
  $('mdActs').innerHTML='<button class="btn" id="rnCancel">'+tr('act.cancel','取消')+'</button><button class="btn primary" id="rnOk">'+tr('act.save','保存')+'</button>';
  $('rnCancel').onclick=()=>closeDlg('cancel');
  $('rnOk').onclick=()=>{
    const v=($('rnInput').value||'').trim();
    if(v){s.name=v;renderSrv();log('ui','servers','rename','OK','detail=sid='+s.sid+' unchanged=true');}
    closeDlg('confirm');
  };
  $('rnInput').onkeydown=e=>{if(e.key==='Enter')$('rnOk').click();};
}
function openJoin(s){''', 'openRename')

# renderSrv 里绑定改名按钮
R("  document.querySelectorAll('[data-join]').forEach(x=>x.onclick=e=>{if(e.detail===1)log('ui','servers','select','OK','detail='+x.dataset.join+' single_click');});",
  "  document.querySelectorAll('[data-join]').forEach(x=>x.onclick=e=>{if(e.detail===1)log('ui','servers','select','OK','detail='+x.dataset.join+' single_click');});\n  document.querySelectorAll('[data-rename]').forEach(x=>x.onclick=e=>{e.stopPropagation();const s=SERVERS.find(y=>y.sid===x.dataset.rename);if(s)openRename(s);});",
  'rename handler')

# openJoin 弹窗按钮 i18n
R("  openDlg('进入服务器',body,'join_'+s.id);", "  openDlg(tr('srv.join','进入服务器'),body,'join_'+s.sid);", 'openJoin title')
R("  $('mdActs').innerHTML='<button class=\"btn\" id=\"jnCancel\">取消</button><button class=\"btn\" id=\"jnOther\">换实例</button><button class=\"btn primary\" id=\"jnGo\">进入</button>';",
  "  $('mdActs').innerHTML='<button class=\"btn\" id=\"jnCancel\">'+tr('act.cancel','取消')+'</button><button class=\"btn\" id=\"jnOther\">'+tr('srv.other','换实例')+'</button><button class=\"btn primary\" id=\"jnGo\">'+tr('srv.enter','进入')+'</button>';",
  'join buttons')

# budget hint 走 tr
R("  const hint=$('budHint');if(hint)hint.textContent=PROBE.cancelled?'已停止，不再发出新的连接；已经拿到的结果保留。':PROBE.running?'正在后台连接，界面先显示上次结果；慢的会自动跳过，随时可以停。':'按权重取前几台自动连；范围外的保留上次结果，不发请求。新加的服务器一定连，但总数还是卡在这个范围里。';",
  "  const hint=$('budHint');if(hint)hint.textContent=PROBE.cancelled?tr('srv.hintStop','已停止，不再发出新的连接；已经拿到的结果保留。'):PROBE.running?tr('srv.hintRun','正在后台连接，界面先显示上次结果；慢的会自动跳过，随时可以停。'):tr('srv.hintIdle','按权重取前几台自动连；范围外的保留上次结果，不发请求。新加的服务器一定连，但总数还是卡在这个范围里。');",
  'budget hint')

# ============ 10. i18n 字典与 applyI18n（插在 <script> 开头附近） ============
i18n_js = r'''
/* 023 i18n：界面文案只走 key，中文是缺资源时的兜底；实现层改用 .ftl 后源码不保留文案 */
const EN={
 'app.desktop':'Desktop','search.hint':'Search instances, mods, settings','lang.switch':'Language',
 'nav.home':'Home','nav.notices':'Notices','nav.instances':'Instances','nav.servers':'Servers',
 'nav.download':'Downloads','nav.mods':'Mods','nav.login':'Accounts','nav.serverhost':'Server Host','nav.logs':'Logs',
 'cache.updated':'Updated','act.refresh':'Refresh','act.hard':'Reload','state.ready':'Ready','state.synced':'Synced',
 'settings.title':'Settings','settings.sub':'Applied instantly · searchable · changed only · reset all',
 'tab.general':'General','tab.download':'Downloads','tab.cache':'Cache','tab.recommend':'Recommend','tab.status':'Servers',
 'tab.ai':'AI','tab.crash':'Crash reports','tab.plugins':'Plugins','tab.privacy':'Privacy','tab.experimental':'Labs',
 'tab.modified':'Changed','tab.reset':'Reset','set.lang':'Language','set.theme':'Theme','set.dir':'Data folder',
 'srv.budget':'Connection budget','srv.budgetsub':'Limit how many connect at once based on this machine',
 'srv.limit':'This round','srv.conc':'At the same time','srv.flight':'Active / queued','srv.skip':'Not this round',
 'srv.tier':'Lighter mode','srv.stop':'Stop','srv.devcard':'Connection budget',
 'srv.note1':'Servers that never connected keep their old rank and are not retried; locked ones stay on top.',
 'srv.note2':'Names can repeat and can be changed anytime; each server keeps its own records.',
 'srv.autosync':'Auto sync','srv.offline':'Offline','srv.locked':'Locked','srv.new':'New · pending',
 'srv.never':'Never connected · skipped','srv.out':'Outside this round · last result','srv.fail':'Offline · moved down',
 'srv.norecord':'No successful connection yet','srv.unreachable':'Unable to connect','srv.played':'played',
 'srv.same':'Same name','srv.locktip':'Pin / unpin','srv.rename':'Rename',
 'srv.renameTitle':'Rename server','srv.renameBody':'Names may repeat and can change anytime. Only the label changes; history, ranking and folder stay.',
 'srv.join':'Join server','srv.other':'Pick instance','srv.enter':'Join','srv.hintStop':'Stopped. No new connections; results already received are kept.',
 'srv.hintRun':'Connecting in the background. Last results show first; slow ones are skipped and you can stop anytime.',
 'srv.hintIdle':'Connect the top few by rank; the rest keep their last result without a request. New servers always connect but stay inside the same budget.',
 'act.cancel':'Cancel','act.save':'Save','act.later':'Later','act.ok':'Got it','act.noprompt':'Do not show again',
 'crash.card':'Crash reports','crash.enable':'When something breaks','crash.off':'Ask me first','crash.local':'Keep locally only',
 'crash.never':'Do not record','crash.addr':'Destination','crash.addrph':'Filled in by you; leave empty to stay local',
 'crash.mask':'Remove private details','crash.maskon':'Masked by default (can turn off)','crash.maskoff':'Do not mask',
 'crash.dir':'Diagnostic folder','crash.what':'What is recorded','crash.what1':'Window, version, OS build and the steps before the error.',
 'crash.what2':'Server addresses, chat, player names and save contents are excluded by default.',
 'crash.what3':'You get one confirmation with the full contents before anything is sent, and can cancel.',
 'crash.what4':'Without a destination it stays local and you can export it yourself.',
 'crash.view':'View latest','crash.export':'Export diagnostics','crash.state':'Not sent',
 'crash.note':'Older machines, different architectures and OS builds behave differently; a dedicated crash library handles this instead of custom code here.',
 'view.home':'Home','view.notices':'Notices','view.instances':'Instances','view.servers':'Servers',
 'view.download':'Downloads','view.mods':'Mods','view.login':'Accounts','view.serverhost':'Server Host','view.logs':'Logs',
 'view.settings':'Settings','view.about':'About','view.licenses':'Third-party licenses','view.popups':'Dialogs',
 'lic.all':'All','lic.group':'Grouped by license','about.title':'About KCU Launcher','about.sub':'Version and licenses'
};
let LOCALE='zh-CN';
function tr(k,fb){return LOCALE==='en-US'&&EN[k]?EN[k]:(fb!==undefined?fb:k);}
function applyI18n(){
  document.querySelectorAll('[data-i18n]').forEach(el=>{
    if(el.dataset.i18nFb===undefined)el.dataset.i18nFb=el.textContent;
    el.textContent=tr(el.dataset.i18n,el.dataset.i18nFb);
  });
  document.querySelectorAll('[data-i18n-ph]').forEach(el=>{
    if(el.dataset.i18nPhFb===undefined)el.dataset.i18nPhFb=el.getAttribute('placeholder')||'';
    el.setAttribute('placeholder',tr(el.dataset.i18nPh,el.dataset.i18nPhFb));
  });
  document.querySelectorAll('[data-i18n-title]').forEach(el=>{
    if(el.dataset.i18nTFb===undefined)el.dataset.i18nTFb=el.getAttribute('title')||'';
    el.setAttribute('title',tr(el.dataset.i18nTitle,el.dataset.i18nTFb));
  });
  const cur=document.querySelector('.view.on');
  if(cur){const k='view.'+cur.dataset.view;$('vTitle').textContent=EN[k]&&LOCALE==='en-US'?EN[k]:(window.__vTitleFb||$('vTitle').textContent);}
  $('btnLang').textContent=LOCALE==='en-US'?'EN':'中';
}
function setLang(l){
  LOCALE=l;
  const sel=$('setLang');if(sel)sel.value=l;
  applyI18n();
  if(typeof renderSrv==='function')renderSrv();
  if(typeof updateBudget==='function')updateBudget();
  log('ui','i18n','switch','OK','detail='+LOCALE);
}
$('btnLang').onclick=()=>setLang(LOCALE==='zh-CN'?'en-US':'zh-CN');
if($('setLang'))$('setLang').onchange=e=>setLang(e.target.value);
'''
# 插在 esc 函数之前（脚本靠前位置）
anchor = 'function esc(s){'
assert anchor in t
t = t.replace(anchor, i18n_js + '\n' + anchor, 1)
print('OK i18n dict')

# show() 里视图标题走 tr，并新增场景别名
R("  const m=VIEW_META[v]||VIEW_META.home;$('vTitle').textContent=m[0];$('vCrumb').textContent=m[1];",
  "  const m=VIEW_META[v]||VIEW_META.home;window.__vTitleFb=m[0];$('vTitle').textContent=tr('view.'+v,m[0]);$('vCrumb').textContent=m[1];",
  'show title i18n')
R("  if(v==='servers-history'){show('servers');DEVICE_TIER='lightweight';const bs=$('budSwitch');if(bs)bs.textContent='切回标准档';buildPlan();renderSrv();updateBudget();setTimeout(()=>srvProbe(true),40);return;}",
  """  if(v==='servers-history'){show('servers');DEVICE_TIER='lightweight';const bs=$('budSwitch');if(bs)bs.textContent='切回标准档';buildPlan();renderSrv();updateBudget();setTimeout(()=>srvProbe(true),40);return;}
  if(v==='servers-rename'){show('servers');setTimeout(()=>openRename(SERVERS[0]),40);return;}
  if(v==='servers-samenames'){show('servers');setTimeout(()=>{if(typeof renderSrv==='function')renderSrv();},40);return;}
  if(v==='i18n-en'){setLang('en-US');show('settings');setTab('general');return;}""",
  'show aliases 023')

# openDlg 默认按钮走 tr
R("  $('mdActs').innerHTML='<button class=\"btn\" id=\"mdNo\">不再提示</button><button class=\"btn\" id=\"mdCancel\">稍后</button><button class=\"btn primary\" id=\"mdOk\">知道了</button>';",
  "  $('mdActs').innerHTML='<button class=\"btn\" id=\"mdNo\">'+tr('act.noprompt','不再提示')+'</button><button class=\"btn\" id=\"mdCancel\">'+tr('act.later','稍后')+'</button><button class=\"btn primary\" id=\"mdOk\">'+tr('act.ok','知道了')+'</button>';",
  'openDlg buttons')

# 崩溃反馈页按钮行为
R("renderSrv();buildPlan();renderSrv();updateBudget();", """renderSrv();buildPlan();renderSrv();updateBudget();applyI18n();
if($('crashView'))$('crashView').onclick=()=>openDlg(tr('crash.view','看最近一次'),'<div class="attach" style="line-height:1.9">'+tr('crash.what1','出错时的窗口、版本、系统版本与出错前的操作步骤。')+'<br>'+tr('crash.state','未发送')+'</div>','crash_latest');
if($('crashExport'))$('crashExport').onclick=()=>{$('crashState').textContent=tr('crash.local','只留在本地');log('ui','crash','export','OK','detail=local_only masked=true');};
if($('setCrashMask'))$('setCrashMask').onchange=e=>log('ui','crash','mask','OK','detail='+(e.target.selectedIndex===0?'on':'off'));""", 'crash handlers + applyI18n init')

# 关于页 / 许可页 i18n 标注
R('<div class="panel-title">关于 KCU Launcher</div><div class="panel-sub">版本与开源许可</div>',
  '<div class="panel-title" data-i18n="about.title">关于 KCU Launcher</div><div class="panel-sub" data-i18n="about.sub">版本与开源许可</div>', 'about head')
R('<div class="panel-title">第三方许可</div><div class="panel-sub">清单生成 2026-11-13 · 离线可读 · 按许可证分组</div>',
  '<div class="panel-title" data-i18n="view.licenses">第三方许可</div><div class="panel-sub">清单生成 2026-11-14 · 离线可读 · 按许可证分组</div>', 'lic head')
R('<span class="chip on" data-lic="all">全部 16</span>', '<span class="chip on" data-lic="all">全部 22</span>', 'lic count')
R('<span class="badge up">按许可证分组</span>', '<span class="badge up" data-i18n="lic.group">按许可证分组</span>', 'lic group')

# ============ 11. 许可表追加候选 6 组 ============
lic_new = """ ['fluent-rs','UI / 崩溃层候选','Apache-2.0 OR MIT','Mozilla & contributors','界面文案 .ftl 运行时选择','projectfluent.org','候选 · 未进构建','Apache-2.0'],
 ['i18n-embed','UI / 崩溃层候选','MIT','i18n-embed contributors','语言包嵌入与系统语言探测','lib.rs/crates/i18n-embed','候选 · 未进构建','MIT'],
 ['sentry-minidump','UI / 崩溃层候选','MIT','Sentry','独立进程捕获原生崩溃','lib.rs/crates/sentry-minidump','候选 · 未进构建','MIT'],
 ['rust-minidump','UI / 崩溃层候选','MIT','Mozilla & contributors','本地解析 minidump，不联网','lib.rs/crates/minidump','候选 · 未进构建','MIT'],
 ['Breakpad','UI / 崩溃层候选','BSD-3-Clause','Google','崩溃后端之一','chromium.googlesource.com/breakpad','候选 · 未进构建','Apache-2.0'],
 ['sentry-native','UI / 崩溃层候选','MIT','Sentry','Breakpad / Crashpad 后端封装','github.com/getsentry/sentry-native','候选 · 未进构建','MIT'],
"""
R(" ['KCU Launcher 本项目','0.0.0','未生成','—','本项目 LICENSE 待定','THIRD-PARTY-NOTICES.md','未生成','NOASSERTION'],\n];",
  " ['KCU Launcher 本项目','0.0.0','未生成','—','本项目 LICENSE 待定','THIRD-PARTY-NOTICES.md','未生成','NOASSERTION'],\n" + lic_new + "];",
  'license rows')

p.write_text(t)
print('UX_023_OK', p.stat().st_size)

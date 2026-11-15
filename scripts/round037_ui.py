from pathlib import Path

p = Path('demos/ui-full-kcu-paper.html')
t = p.read_text()

def rep(old, new, label):
    global t
    assert old in t, 'MISS ' + label
    t = t.replace(old, new, 1)
    print('OK', label)

# 1) CSS：插件自带 SVG 与问号兜底
rep('.slot-plugin .nav-item{height:30px;font-size:12px}',
    '''.slot-plugin .nav-item{height:30px;font-size:12px}
.plug-svg{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;flex-shrink:0}
.plug-svg svg{width:18px;height:18px;stroke:currentColor;fill:none;stroke-width:1.8;stroke-linecap:round;stroke-linejoin:round}
.plug-q{display:inline-flex;align-items:center;justify-content:center;width:18px;height:18px;flex-shrink:0;
  border:1px dashed var(--ink-3);border-radius:5px;font-family:var(--serif);font-weight:700;font-size:12px;color:var(--ink-3)}''',
    'css')

# 2) 侧栏插件区：2 个自带 SVG + 1 个问号兜底
old_side = '''      <div class="slot-plugin"><div class="sh"><svg class="li" aria-hidden="true"><use href="#i-puzzle"></use></svg> 扩展</div>
        <button class="nav-item" data-gotab="plugins"><span class="ic"><svg class="li" aria-hidden="true"><use href="#i-puzzle"></use></svg></span><span class="lb" data-i18n="我的插件">我的插件</span><span class="cnt">2</span></button>
        <button class="nav-item" data-gotab="plugins"><span class="ic"><svg class="li" aria-hidden="true"><use href="#i-activity"></use></svg></span><span class="lb" data-i18n="更新与状态">更新与状态</span></button>'''
new_side = '''      <div class="slot-plugin"><div class="sh"><svg class="li" aria-hidden="true"><use href="#i-puzzle"></use></svg> <span data-i18n="扩展">扩展</span></div>
        <button class="nav-item" data-gotab="plugins"><span class="ic"><svg class="li" aria-hidden="true"><use href="#i-puzzle"></use></svg></span><span class="lb" data-i18n="我的插件">我的插件</span><span class="cnt">3</span></button>
        <button class="nav-item" data-gotab="plugins" title="插件自带 SVG"><span class="ic plug-svg"><svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l2.6 5.4 5.9.8-4.3 4.1 1.1 5.9L12 16.4 6.7 19.2l1.1-5.9L3.5 9.2l5.9-.8z"/></svg></span><span class="lb" data-i18n="plugin.nav.recommend">推荐插件</span></button>
        <button class="nav-item" data-gotab="plugins" title="插件自带 SVG"><span class="ic plug-svg"><svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M8 14h3M8 17h6"/></svg></span><span class="lb" data-i18n="plugin.nav.status">状态面板</span></button>
        <button class="nav-item" data-gotab="plugins" title="未提供 SVG"><span class="ic plug-q">?</span><span class="lb" data-i18n="plugin.nav.legacy">旧版插件</span></button>
        <button class="nav-item" data-gotab="plugins"><span class="ic"><svg class="li" aria-hidden="true"><use href="#i-activity"></use></svg></span><span class="lb" data-i18n="更新与状态">更新与状态</span></button>'''
rep(old_side, new_side, 'sidebar')

# 3) 弹窗全集 11 -> 13
rep(" ['extension','扩展安装','扩展安装确认，可关闭。'],\n];",
    ''' ['extension','扩展安装','扩展安装确认，可关闭。'],
 ['plugin-upgrade','升级确认','身份哈希一致 → 比对版本 → 你手动同意才安装。'],
 ['plugin-fault','插件故障','报告问题，底部可禁用继续尝试启动 / 取消。'],
];''', 'popups')
rep(" 'ai.af.no.s','什么都不做也不自动重试'",
    " 'ai.af.no.s','什么都不做也不自动重试'", 'noop-check') if False else None

# 4) VIEW_META
rep(" upperstack:['上层实现候选','内部设计证据 · 不进产品导航']};",
    ''' upperstack:['上层实现候选','内部设计证据 · 不进产品导航'],
 pluginicons:['插件侧栏图标','插件自带 SVG · 没有就用问号'],
 pluginupgrade:['插件升级确认','身份哈希一致 · 比对版本 · 手动同意'],
 pluginfault:['插件故障报告','禁用并继续尝试启动 / 取消']};''', 'viewmeta')

# 5) show() 分支
rep("  if(v==='i18n-en'){setLang('en-US');show('settings');setTab('general');return;}",
    '''  if(v==='plugin-icons'){show('home');return;}
  if(v==='plugin-upgrade'){show('settings');setTab('plugins');setTimeout(openUpgradeDlg,40);return;}
  if(v==='plugin-fault'){show('home');setTimeout(openFaultDlg,40);return;}
  if(v==='i18n-en'){setLang('en-US');show('settings');setTab('general');return;}''', 'show-branches')

# 6) 两个弹窗函数，插在 closeDlg 之后
rep("function closeDlg(r){if(!dlgOpen)return;$('mask').classList.remove('on');dlgOpen=false;log('ui','popup','close','OK','detail='+r);}",
    '''function closeDlg(r){if(!dlgOpen)return;$('mask').classList.remove('on');dlgOpen=false;log('ui','popup','close','OK','detail='+r);}
function openUpgradeDlg(){
  const body='<p>'+tr('plugin.upgrade.p1','已装的「推荐插件」与候选包身份哈希一致，属于同一个插件。')+'</p>'+
   '<p>'+tr('plugin.upgrade.p2','版本 1.2.3 → 1.3.0，签名校验已通过。升级需要你手动同意；没同意就保留旧插件，不会自动安装。')+'</p>'+
   '<div class="attach">'+tr('plugin.upgrade.attach','身份哈希 a3f1…c9 · 签名通过 · 原插件可回滚')+'</div>';
  openDlg(tr('plugin.upgrade.title','确认升级插件'),body,'plugin_upgrade');
  $('mdActs').innerHTML='<button class="btn" id="mdCancel">'+tr('plugin.upgrade.later','暂不升级')+'</button><button class="btn primary" id="mdOk">'+tr('plugin.upgrade.ok','升级')+'</button>';
  $('mdCancel').onclick=()=>{closeDlg('keep_old');log('plugin','upgrade','keep','OK','detail=not_confirmed');};
  $('mdOk').onclick=()=>{closeDlg('user_confirmed_upgrade');log('plugin','upgrade','install','OK','detail=manual_consent');};
}
function openFaultDlg(){
  const body='<p>'+tr('plugin.fault.p1','插件「旧版插件」没能正常加载：入口符号缺失。')+'</p>'+
   '<p>'+tr('plugin.fault.p2','可以先禁用它再继续尝试启动；也可以取消本次启动。')+'</p>'+
   '<div class="attach">'+tr('plugin.fault.attach','诊断行已记录 · 禁用只影响本次启动 · 其他插件不受影响')+'</div>'+
   '<div class="mut" style="font-size:10.5px">'+tr('plugin.fault.hint','也可以点右上角 × 或按 Esc 取消。')+'</div>';
  openDlg(tr('plugin.fault.title','插件加载失败'),body,'plugin_fault');
  $('mdActs').innerHTML='<button class="btn" id="mdCancel">'+tr('plugin.fault.cancel','取消')+'</button><button class="btn primary" id="mdOk">'+tr('plugin.fault.retry','禁用并继续尝试启动')+'</button>';
  $('mdCancel').onclick=()=>{closeDlg('cancel_startup');log('plugin','fault','cancel','OK','detail=startup_aborted');};
  $('mdOk').onclick=()=>{closeDlg('disable_and_retry');log('plugin','fault','disable','OK','detail=retry_startup');};
}''', 'dialogs')

# 7) EN 语义 key
rep(" 'auto.risk.blacklist':'These stay locked unless you unlock them one by one, each with its own confirm.'\n};",
    ''' 'auto.risk.blacklist':'These stay locked unless you unlock them one by one, each with its own confirm.',
 'plugin.nav.recommend':'Recommended plugins','plugin.nav.status':'Status panel','plugin.nav.legacy':'Legacy plugin',
 'plugin.upgrade.title':'Confirm plugin upgrade','plugin.upgrade.p1':'The installed plugin and the candidate share the same identity hash, so they are the same plugin.',
 'plugin.upgrade.p2':'Version 1.2.3 to 1.3.0; signature verified. Upgrading needs your manual consent, otherwise the old plugin stays.',
 'plugin.upgrade.attach':'Identity a3f1…c9 · Signature OK · Old plugin can be restored',
 'plugin.upgrade.later':'Not now','plugin.upgrade.ok':'Upgrade',
 'plugin.fault.title':'Plugin failed to load','plugin.fault.p1':'Plugin "Legacy plugin" could not load: entry symbol missing.',
 'plugin.fault.p2':'You can disable it and retry startup, or cancel this startup.',
 'plugin.fault.attach':'Diagnostic line recorded · Disable affects this startup only · Other plugins are unaffected',
 'plugin.fault.hint':'You can also click the top-right × or press Esc to cancel.',
 'plugin.fault.cancel':'Cancel','plugin.fault.retry':'Disable and retry startup',
 'plugin.set.upgrade':'Upgrade','plugin.set.upgrade.v':'Manual consent required',
 'plugin.set.fault':'On plugin fault','plugin.set.fault.v':'Report, disable & retry, or cancel',
 'plugin.set.icon':'Sidebar icon','plugin.set.icon.v':'Plugin SVG, or ? if missing'
};''', 'en-keys')

# 8) 设置 → 插件与更新：三条口径
rep('<span class="k" data-i18n="失败降级">失败降级</span><span><select class="sel"><option value="失败保留原来的插件" data-i18n="失败保留原来的插件">失败保留原来的插件</option></select></span></div></div>',
    '''<span class="k" data-i18n="失败降级">失败降级</span><span><select class="sel"><option value="失败保留原来的插件" data-i18n="失败保留原来的插件">失败保留原来的插件</option></select></span>
<span class="k" data-i18n="plugin.set.upgrade">升级</span><span><select class="sel"><option value="手动同意才安装" data-i18n="plugin.set.upgrade.v">手动同意才安装</option></select></span>
<span class="k" data-i18n="plugin.set.fault">插件有问题时</span><span><select class="sel"><option value="报告 · 禁用继续 · 取消" data-i18n="plugin.set.fault.v">报告 · 禁用继续 · 取消</option></select></span>
<span class="k" data-i18n="plugin.set.icon">侧边栏图标</span><span><select class="sel"><option value="插件 SVG · 没有就用问号" data-i18n="plugin.set.icon.v">插件 SVG · 没有就用问号</option></select></span></div></div>''', 'settings')

# 9) 弹窗全集标题 11 -> 13
rep("popups:['弹窗全集','11 类 · 每类有关闭路径']", "popups:['弹窗全集','13 类 · 每类有关闭路径']", 'popups-meta')
rep("['弹窗全集','11 类 · 每类有关闭路径']", "['弹窗全集','13 类 · 每类有关闭路径']", 'popups-meta2') if "['弹窗全集','11 类" in t else None

p.write_text(t)
print('UI_WRITTEN', p.stat().st_size)

# 10) render_ui.py 新增 3 个场景
r = Path('scripts/render_ui.py')
s = r.read_text()
old = '    ("48-loose-actions", "loose-actions", "宽松档 · 动作逐项可勾"),\n]'
new = '''    ("48-loose-actions", "loose-actions", "宽松档 · 动作逐项可勾"),
    ("49-plugin-icons", "plugin-icons", "侧栏插件图标 · 自带 SVG / 问号兜底"),
    ("50-plugin-upgrade", "plugin-upgrade", "升级确认 · 身份哈希一致需手动同意"),
    ("51-plugin-fault", "plugin-fault", "插件故障 · 禁用继续 / 取消"),
]'''
assert old in s
r.write_text(s.replace(old, new, 1))
print('RENDER_SCENES_OK')

from pathlib import Path

p = Path('demos/ui-full-kcu-paper.html')
t = p.read_text()

# 1) CSS：档位卡片 / 锁定态
css_anchor = '.badge.r{color:var(--red);border-color:var(--red)}'
if '.tier-card{' not in t:
    t = t.replace(css_anchor, css_anchor + '''
.tier-card{border:1px solid var(--line);border-radius:8px;padding:9px 12px;text-align:left;min-width:196px;background:#fff;cursor:pointer}
.tier-card.on{border-color:var(--teal);box-shadow:inset 0 0 0 1px var(--teal)}
.tier-card b{display:block;font:600 12px Georgia,serif;margin-bottom:3px}
.tier-card span{font-size:10.5px;color:var(--ink-2);line-height:1.45;display:block}
.tier-locked{opacity:.45}
.chk{width:13px;height:13px;vertical-align:-2px;margin-right:5px}
.risk{font-size:10.5px;color:var(--red)}
''', 1)
    print('CSS_OK')

# 2) 031 分组里中文当 key 的 data-i18n 全部换语义 key
cn_keys = {
    '命中以后': 'auto.afterhit', '要不要问': 'auto.ask', '没确认': 'auto.unconfirmed',
    '等太久': 'auto.timeout', '刷屏时': 'auto.burst', '冷却': 'auto.cooldown',
    '能做的事': 'auto.actions', '记录与提醒': 'auto.a1', '游戏内广播': 'auto.a2',
    '服务器命令': 'auto.a3', '重启与备份': 'auto.a4', '日志外传': 'auto.a5',
    '哪些文字算数': 'auto.source', '只看': 'auto.source.only', '玩家聊天': 'auto.source.chat',
    '测试规则': 'auto.source.test', '插件': 'auto.source.plugin',
    '这样设置以后': 'auto.effect', '先说清楚，免得跟想的不一样': 'auto.effect.sub',
    '每次都先问过你': 'auto.v.ask', '什么都不做，也不自动重试': 'auto.v.none',
    '当作取消': 'auto.v.cancel', '只留一条待确认，其余记次数': 'auto.v.count',
    '允许 · 仍需每次确认': 'auto.v.c1', '不允许': 'auto.v.deny',
    '服务器自己输出的日志': 'auto.v.srvlog', '不参与匹配': 'auto.v.nochat',
    '只预览，不真的执行': 'auto.v.preview', '不能放宽这些限制': 'auto.v.noplugin',
    '自动命令': 'tab.auto',
}
for cn, key in cn_keys.items():
    t = t.replace('data-i18n="' + cn + '"', 'data-i18n="' + key + '"')
print('I18N_KEYS_REWRITTEN')

# 3) EN 字典追加语义 key
en_anchor = " 'lic.all':'All','lic.group':'Grouped by license','about.title':'About KCU Launcher','about.sub':'Version and licenses'\n};"
assert en_anchor in t
en_new = """ 'lic.all':'All','lic.group':'Grouped by license','about.title':'About KCU Launcher','about.sub':'Version and licenses',
 'tab.auto':'Auto commands',
 'auto.tier':'Strictness','auto.tier.sub':'Strict by default. Change this yourself if you want unattended handling.',
 'auto.tier.strict':'Strict (default)','auto.tier.strict.d':'Ask every time. Record only, no server changes.',
 'auto.tier.standard':'Standard','auto.tier.standard.d':'Records run without asking; other actions still ask. You pick what is allowed.',
 'auto.tier.loose':'Loose','auto.tier.loose.d':'Authorise a rule once, then it runs on its own. All actions can be enabled; the risk is yours.',
 'auto.tier.now':'Current','auto.tier.reset':'Back to strict',
 'auto.afterhit':'After a hit','auto.ask':'Ask first','auto.unconfirmed':'Not confirmed','auto.timeout':'Timeout',
 'auto.burst':'Rapid hits','auto.cooldown':'Cooldown','auto.actions':'Allowed actions',
 'auto.a1':'Records & notices','auto.a2':'In-game broadcast','auto.a3':'Server commands',
 'auto.a4':'Restart & backup','auto.a5':'Upload logs',
 'auto.source':'Which text counts','auto.source.only':'Only','auto.source.chat':'Player chat',
 'auto.source.test':'Rule test','auto.source.plugin':'Plugins','auto.effect':'What this means',
 'auto.effect.sub':'Spelled out so it matches what you expect','auto.actions.tip':'Tick only what you are comfortable with; each can be turned off again.',
 'auto.v.ask':'Ask every time','auto.v.none':'Do nothing, no auto retry','auto.v.cancel':'Treat as cancel',
 'auto.v.count':'One pending dialog, the rest counted','auto.v.c1':'Allowed, still asks','auto.v.deny':'Not allowed',
 'auto.v.srvlog':'Server output only','auto.v.nochat':'Not matched','auto.v.preview':'Preview only','auto.v.noplugin':'Cannot relax these',
 'auto.tier.switch':'Change strictness','auto.tier.cancel':'Keep current','auto.tier.ok':'Change',
 'auto.risk.c2':'Interrupts every player online','auto.risk.c3':'Changes server state and writes your world',
 'auto.risk.c4':'Touches files and the running instance','auto.risk.c5':'Sends logs outside; a separate confirm still applies',
 'auto.risk.blacklist':'These stay locked unless you unlock them one by one, each with its own confirm.'
};"""
if "'auto.tier'" not in t:
    t = t.replace(en_anchor, en_new, 1)
    print('EN_OK')

# 4) 档位卡片插到 auto pane 顶部
pane_anchor = '<div class="tabpane" data-pane="auto"><div class="grid g2">'
assert pane_anchor in t
tier_panel = '''<div class="tabpane" data-pane="auto"><div class="panel" style="margin-bottom:12px"><div class="panel-head"><div class="panel-title" data-i18n="auto.tier">宽严程度</div><div class="panel-sub" data-i18n="auto.tier.sub">默认是严格；想让夜里也能自动处理，自己在这里换</div><div class="panel-tools"><span class="badge ok" id="tierNow">当前：严格</span><button class="btn tiny" id="tierReset" data-i18n="auto.tier.reset">恢复严格</button></div></div>
<div class="row" id="tierCards" style="gap:9px;flex-wrap:wrap">
<button class="btn tier-card on" data-tier="strict"><b data-i18n="auto.tier.strict">严格（默认）</b><span data-i18n="auto.tier.strict.d">每次都先问 · 只记录不操作</span></button>
<button class="btn tier-card" data-tier="standard"><b data-i18n="auto.tier.standard">标准</b><span data-i18n="auto.tier.standard.d">记录免问，其他仍问 · 可自己勾选动作</span></button>
<button class="btn tier-card" data-tier="loose"><b data-i18n="auto.tier.loose">宽松</b><span data-i18n="auto.tier.loose.d">授权一次后自动 · 动作全可开，风险自己担</span></button>
</div></div>
<div class="grid g2">'''
if 'id="tierCards"' not in t:
    t = t.replace(pane_anchor, tier_panel, 1)
    print('TIER_PANEL_OK')

# 5) 把 031 静态「能做的事」卡片换成动态容器
old_actions = '''<div class="set-card"><div class="hd" data-i18n="auto.actions">能做的事</div><div class="kv">
<span class="k" data-i18n="auto.a1">记录与提醒</span><span><span class="badge ok">允许 · 仍需每次确认</span></span>
<span class="k" data-i18n="auto.a2">游戏内广播</span><span><span class="badge off">不允许</span></span>
<span class="k" data-i18n="auto.a3">服务器命令</span><span><span class="badge off">不允许</span></span>
<span class="k" data-i18n="auto.a4">重启与备份</span><span><span class="badge off">不允许</span></span>
<span class="k" data-i18n="auto.a5">日志外传</span><span><span class="badge off">不允许</span></span></div></div>'''
assert old_actions in t
new_actions = '''<div class="set-card"><div class="hd" data-i18n="auto.actions">能做的事</div><div class="kv" id="autoActionRows"></div><div class="mut" style="font-size:10.5px;margin-top:8px" id="autoActionTip"></div></div>'''
t = t.replace(old_actions, new_actions, 1)
print('ACTIONS_DYNAMIC_OK')

# 6) JS：档位状态机
js_anchor = "function closeDlg(r){if(!dlgOpen)return;$('mask').classList.remove('on');dlgOpen=false;log('ui','popup','close','OK','detail='+r);}"
assert js_anchor in t
tier_js = '''
let TIER='strict';
const TIER_LABEL={strict:'严格',standard:'标准',loose:'宽松'};
const TIER_EN={strict:'Strict',standard:'Standard',loose:'Loose'};
const AROWS=[
 ['c1','auto.a1','记录与提醒','Records & notices','只写记录与诊断行，不改存档、不碰服务器','Only records, no world or server changes',false],
 ['c2','auto.a2','游戏内广播','In-game broadcast','会打断所有在线玩家','Interrupts every player online',true],
 ['c3','auto.a3','服务器命令','Server commands','会改服务器状态，也会写存档','Changes server state and writes your world',true],
 ['c4','auto.a4','重启与备份','Restart & backup','会动文件和运行中的实例','Touches files and the running instance',true],
 ['c5','auto.a5','日志外传','Upload logs','会发到外面，发送前仍要单独确认','Sends logs outside; a separate confirm still applies',true],
];
let TIER_ALLOW={standard:{c1:true,c2:false,c3:false,c4:false,c5:false},loose:{c1:true,c2:false,c3:false,c4:false,c5:false}};
function renderTier(){
  document.querySelectorAll('.tier-card').forEach(b=>b.classList.toggle('on',b.dataset.tier===TIER));
  const now=$('tierNow');if(now)now.textContent=(LOCALE==='en-US'?'Current: ':'当前：')+(LOCALE==='en-US'?TIER_EN[TIER]:TIER_LABEL[TIER]);
  const rows=$('autoActionRows');if(!rows)return;
  rows.innerHTML=AROWS.map(r=>{
    const [id,key,cn,en,riskCn,riskEn,optional]=r;
    const label=LOCALE==='en-US'?en:cn, risk=LOCALE==='en-US'?riskEn:riskCn;
    if(TIER==='strict'){
      return '<span class="k" data-i18n="'+key+'">'+label+'</span><span>'+(id==='c1'?'<span class="badge ok">'+(LOCALE==='en-US'?'Allowed, still asks':'允许 · 仍需每次确认')+'</span>':'<span class="badge off">'+(LOCALE==='en-US'?'Not allowed':'不允许')+'</span>')+'</span>';
    }
    const on=TIER_ALLOW[TIER][id];
    const dis=id==='c1'?' disabled checked':'';
    return '<span class="k" data-i18n="'+key+'">'+label+'</span><span><label style="font-size:11.5px"><input class="chk" type="checkbox" data-act="'+id+'"'+(on?' checked':'')+dis+'>'+(LOCALE==='en-US'?'Allow':'允许')+'</label><span class="risk" style="margin-left:6px">'+risk+'</span></span>';
  }).join('');
  rows.querySelectorAll('input[data-act]').forEach(c=>c.onchange=e=>{
    const id=e.target.dataset.act;TIER_ALLOW[TIER][id]=e.target.checked;
    log('server','auto','action','OK','detail=tier='+TIER+' '+id+'='+e.target.checked);
  });
  const tip=$('autoActionTip');if(tip)tip.textContent=TIER==='strict'
    ? (LOCALE==='en-US'?'Only records are allowed. Switch strictness above to enable more.':'这一档只做记录。想放开别的，先在上面换宽严程度。')
    : tr('auto.actions.tip','只勾你能接受的那几项，随时能再关掉。')+' '+tr('auto.risk.blacklist','高风险命令默认锁着，要一条一条单独解开，每次都要再确认一遍。');
}
function setTier(t){
  if(!TIER_LABEL[t]||t===TIER)return;
  const from=TIER;TIER=t;renderTier();
  log('server','auto','tier','OK','detail=from='+from+' to='+t+' user_initiated=true audit=1');
}
function openTierConfirm(to){
  const cn=TIER_LABEL[to], en=TIER_EN[to];
  const name=LOCALE==='en-US'?en:cn;
  const body='<p style="margin:0 0 8px">'+(LOCALE==='en-US'?'You are changing from ':'你要从 ')+'<b>'+(LOCALE==='en-US'?TIER_EN[TIER]:TIER_LABEL[TIER])+'</b>'+(LOCALE==='en-US'?' to ':' 换到 ')+'<b>'+name+'</b>'+(LOCALE==='en-US'?'.':'。')+'</p>'
   +'<div class="attach" style="margin-bottom:8px">'+(LOCALE==='en-US'?'After the change: fewer confirmations, more actions available. Unattended handling becomes possible.':'换了以后：要问的次数变少、能做的事变多，夜里没人在电脑前也会自己处理。')+'</div>'
   +'<p style="margin:0;color:var(--ink-2)">'+(LOCALE==='en-US'?'Uploading logs still always needs its own confirm. Every hit is still recorded. You can come back here and switch back at any time.':'日志外传仍然每次单独确认；每次命中仍然会记下来；随时可以回到这一页换回去。')+'</p>';
  openDlg('切换宽严程度',body,'tier_switch');
  $('mdId').textContent='';
  $('mdActs').innerHTML='<button class="btn" id="mdCancel">保持当前</button><button class="btn primary" id="mdOk">确认切换</button>';
  $('mdCancel').onclick=()=>{closeDlg('cancel');log('server','auto','tier','DENY','detail=user_kept='+TIER);};
  $('mdOk').onclick=()=>{closeDlg('confirm');setTier(to);};
}
'''
if 'let TIER=' not in t:
    t = t.replace(js_anchor, js_anchor + tier_js, 1)
    print('TIER_JS_OK')

# 7) show() 分支
show_anchor = "  if(v==='auto-confirm'){show('serverhost');setTimeout(()=>openAutoConfirm(),40);return;}"
assert show_anchor in t
branches = """  if(v==='auto-confirm'){show('serverhost');setTimeout(()=>openAutoConfirm(),40);return;}
  if(v==='tier-switch'){show('settings');setTab('auto');setTimeout(()=>openTierConfirm('standard'),40);return;}
  if(v==='loose-actions'){show('settings');setTab('auto');setTimeout(()=>{setTier('loose');const rows=$('autoActionRows');if(rows)rows.querySelectorAll('input[data-act]').forEach(c=>{if(c.dataset.act!=='c1'){c.checked=true;TIER_ALLOW.loose[c.dataset.act]=true;}});renderTier();},40);return;}
"""
if "v==='tier-switch'" not in t:
    t = t.replace(show_anchor, branches, 1)
    print('SHOW_BRANCH_OK')

# 8) 初始绑定：renderTier + 卡片点击 + 恢复严格 + 语言切换重渲
init_anchor = "renderNotices();$('noticePreview').innerHTML="
assert init_anchor in t
init_js = """document.querySelectorAll('.tier-card').forEach(b=>b.onclick=()=>{if(b.dataset.tier!==TIER)openTierConfirm(b.dataset.tier);});
if($('tierReset'))$('tierReset').onclick=()=>{if(TIER!=='strict'){const from=TIER;TIER='strict';renderTier();log('server','auto','tier','OK','detail=from='+from+' to=strict reset=1');}};
renderTier();
"""
if "if($('tierReset'))$('tierReset').onclick" not in t:
    t = t.replace(init_anchor, init_js + init_anchor, 1)
    print('INIT_OK')

# 语言切换时重渲档位
lang_anchor = "  applyI18n();\n  log('ui','i18n','switch','OK','detail='+LOCALE);"
assert lang_anchor in t
if "applyI18n();\n  renderTier();" not in t:
    t = t.replace(lang_anchor, "  applyI18n();\n  renderTier();\n  log('ui','i18n','switch','OK','detail='+LOCALE);", 1)
    print('LANG_RERENDER_OK')

p.write_text(t)
print('HTML_OK bytes', len(t))

# 9) render_ui.py 三个新场景
r = Path('scripts/render_ui.py')
s = r.read_text()
a = '    ("45-auto-confirm", "auto-confirm", "命中确认 · 每次都先问过你"),\n]'
assert a in s
if '"46-settings-tiers"' not in s:
    s = s.replace(a, '    ("45-auto-confirm", "auto-confirm", "命中确认 · 每次都先问过你"),\n    ("46-settings-tiers", "settings&tab=auto", "设置 · 宽严程度默认严格"),\n    ("47-tier-switch", "tier-switch", "切换宽严程度 · 二次确认"),\n    ("48-loose-actions", "loose-actions", "宽松档 · 动作逐项可勾"),\n]', 1)
    r.write_text(s)
    print('RENDER_SCENES_OK')

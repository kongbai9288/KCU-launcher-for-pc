from pathlib import Path

p = Path('demos/ui-full-kcu-paper.html')
t = p.read_text()


def repl(a, b, label):
    global t
    assert a in t, label
    t = t.replace(a, b, 1)
    print('OK', label)


# ---------- CSS ----------
css = '''
.budget-kv{display:grid;grid-template-columns:repeat(4,1fr);gap:8px;margin-top:9px}
.budget-cell{background:var(--card);border:1px solid var(--line);border-radius:var(--r-sm);padding:8px 10px}
.budget-cell b{display:block;font-size:16px;color:var(--ink);font-weight:600;margin-top:3px}
.budget-cell span{font-size:10px;color:var(--ink-3)}
.budget-bar{height:5px;border-radius:3px;background:var(--line);margin-top:10px;overflow:hidden}
.budget-bar i{display:block;height:100%;background:var(--accent);width:0;transition:width .2s}
.srv-note{display:inline-block;font-size:10px;color:var(--ink-3);border:1px solid var(--line);border-radius:3px;padding:0 5px;margin-left:6px}
'''
t = t.replace('</style>\n', '\n' + css + '\n</style>\n', 1)
print('OK css')

# ---------- 服务器页加「设备连接范围」卡 ----------
anchor = '''            <div class="panel"><div class="panel-head"><div class="panel-title">自动同步</div>'''
card = '''            <div class="panel"><div class="panel-head"><div class="panel-title">设备连接范围</div><div class="panel-sub">按机器能力控制同时连几台，连不过来就排队</div>
              <div class="panel-tools"><span class="badge ok" id="budTier">标准模式</span><button class="btn tiny" id="budSwitch">切到轻量档</button><button class="btn tiny" id="budCancel">停止本次同步</button></div></div>
              <div class="budget-kv"><div class="budget-cell"><span>本次可连</span><b id="budLimit">4</b></div><div class="budget-cell"><span>同时连接</span><b id="budConc">3</b></div><div class="budget-cell"><span>正在连 / 队列</span><b id="budFlight">0 / 0</b></div><div class="budget-cell"><span>本次不连</span><b id="budSkip">0</b></div></div>
              <div class="budget-bar"><i id="budBar"></i></div>
              <div class="mut" style="font-size:11px;margin-top:8px" id="budHint">按权重取前几台自动连；范围外的保留上次结果，不发请求。新加的服务器一定连，但总数还是卡在这个范围里。</div></div>
            <div class="panel"><div class="panel-head"><div class="panel-title">自动同步</div>'''
repl(anchor, card, 'budget panel')

# ---------- 设置页加「设备连接范围」分组 ----------
anchor2 = '''<div class="set-card"><div class="hd">双击进服</div><div class="kv">'''
setcard = '''<div class="set-card"><div class="hd">设备连接范围</div><div class="kv">
<span class="k">每次自动连几台</span><span><select class="sel" id="setBudLimit"><option>4 台（推荐）</option><option>2 台</option><option>6 台</option><option>全部</option></select></span>
<span class="k">同时连接</span><span><select class="sel" id="setBudConc"><option>3 路</option><option>2 路</option><option>1 路</option></select></span>
<span class="k">轻量机器</span><span><select class="sel" id="setBudTier"><option>自动降到 2 台 / 2 路</option><option>与标准一致</option></select></span>
<span class="k">新加的服务器</span><span><select class="sel"><option>一定连，但占同一份额度</option></select></span>
<span class="k">范围外的</span><span><select class="sel"><option>保留上次结果，不主动连</option></select></span></div></div>
<div class="set-card"><div class="hd">双击进服</div><div class="kv">'''
repl(anchor2, setcard, 'settings budget card')

# ---------- 替换 021 服务器 JS 整段 ----------
start = t.index('/* 021 服务器：自动连接')
end = t.index("$('aiTest').onclick=", start)
JS = r'''/* 022 服务器：异步探测、设备连接范围、失败历史分类、双击进服 */
const SERVERS=[
 {id:'s1',name:'陶瓦联机 · 主服',ip:'mc.taowa.example',ver:'1.21.4',motd:'§a§l陶瓦联机 §7| §f生存季 S3\n§7每周六活动 · 欢迎回家',online:42,max:100,ping:42,ok:true,lock:true,ever:true,tried:true,last:'2 分钟前',inst:'生存季',src:'servers.dat'},
 {id:'s2',name:'朋友的小服',ip:'mc.friends.example:25566',ver:'1.21.1',motd:'§e小服 §7· §f别炸我家',online:6,max:20,ping:88,ok:true,lock:false,ever:true,tried:true,last:'昨天',inst:'测试服',src:'servers.dat'},
 {id:'s3',name:'快照体验服',ip:'snap.example',ver:'1.21.5',motd:'§6快照抢先玩\n§7内容随时会变',online:11,max:30,ping:120,ok:true,lock:false,ever:true,tried:true,last:'3 天前',inst:'快照服',src:'快速进入'},
 {id:'s4',name:'旧服（我锁过）',ip:'old.example',ver:'1.20.4',motd:'',online:0,max:0,ping:null,ok:false,lock:true,ever:true,tried:true,last:'上个月',inst:'怀旧服',src:'隐藏列表'},
 {id:'s5',name:'临时测试服',ip:'tmp.example',ver:'1.21.4',motd:'',online:0,max:0,ping:null,ok:false,lock:false,ever:false,tried:true,last:'两周前',inst:'测试服',src:'servers.dat'},
 {id:'s6',name:'朋友的 1.20 服',ip:'a.example',ver:'1.20.4',motd:'§fA Minecraft Server',online:3,max:20,ping:210,ok:true,lock:false,ever:true,tried:true,last:'两周前',inst:'怀旧服',src:'servers.dat'},
 {id:'s7',name:'公益小服',ip:'b.example',ver:'1.21.1',motd:'§7欢迎',online:2,max:10,ping:340,ok:true,lock:false,ever:true,tried:true,last:'上个月',inst:'测试服',src:'servers.dat'},
 {id:'s8',name:'没连上过的地址',ip:'c.example',ver:'1.21.4',motd:'',online:0,max:0,ping:null,ok:false,lock:false,ever:false,tried:true,last:'上个月',inst:'测试服',src:'快速进入'}
];
const DEVICE={normal:{limit:4,concurrency:3,label:'标准模式'},lightweight:{limit:2,concurrency:2,label:'轻量档'},headless:{limit:0,concurrency:0,label:'无界面'}};
let DEVICE_TIER='normal';
let SERVERS_SYNC='12 秒前';
let PROBE={running:false,cancelled:false,inflight:0,done:0,total:0,skipped:0,plan:null};

function neverSuccess(s){return s.tried && !s.ever && !s.isNew;}
function srvRank(s){
  if(s.lock)return 0;
  if(s.probeSkip==='never')return 500+srvCachedWeight(s);
  if(s.probeSkip==='out')return 400+srvCachedWeight(s);
  if(!s.ok)return 900+srvCachedWeight(s);
  const recent=({'刚刚':0,'2 分钟前':1,'昨天':2,'3 天前':3,'两周前':4,'上个月':5})[s.last]||6;
  return 100+s.ping*0.4+recent*25+(100-s.online)*0.1;
}
function srvCachedWeight(s){
  const recent=({'刚刚':0,'2 分钟前':1,'昨天':2,'3 天前':3,'两周前':4,'上个月':5})[s.last]||6;
  return recent*20+(s.ping!==null&&s.ping!==undefined?s.ping*0.1:0);
}
function srvSorted(){return SERVERS.slice().sort((a,b)=>srvRank(a)-srvRank(b));}
function pingBars(s){
  if(!s.ok)return '<span class="mut" style="font-size:10px">连不上</span>';
  const n=s.ping<150?5:s.ping<300?4:s.ping<600?3:s.ping<1000?2:1;
  return '<span class="srv-ping">'+[1,2,3,4,5].map(i=>'<i style="'+(i>n?'opacity:.2':'')+'"></i>').join('')+'</span>';
}
function srvNote(s){
  if(s.lock)return '<span class="srv-note">已锁定</span>';
  if(s.isNew)return '<span class="srv-note">新加 · 待连接</span>';
  if(s.probeSkip==='never')return '<span class="srv-note">还没连上过 · 暂不重试</span>';
  if(s.probeSkip==='out')return '<span class="srv-note">超出本次范围 · 用上次结果</span>';
  if(!s.ok)return '<span class="srv-note">连不上 · 排到最后</span>';
  return '';
}
function srvRow(s){
  const star='<span class="lock-star" data-lock="'+s.id+'" title="锁定/取消锁定">'+(s.lock?'★':'☆')+'</span>';
  const ico='<div class="srv-ico'+(s.ok?'':' off')+'">'+esc(s.name.charAt(0))+'</div>';
  const motd=(s.ok&&s.motd)?'<div class="srv-motd">'+esc(s.motd.replace(/§[0-9a-fklmnor]/g,''))+'</div>':'<div class="srv-motd" style="color:var(--ink-3)">'+(s.probeSkip==='never'?'还没有成功的连接记录':'无法连接到服务器')+'</div>';
  const side='<div class="srv-side"><div class="srv-count">'+(s.ok?s.online+' / '+s.max:'—')+'</div>'+pingBars(s)+'<div class="srv-ver">'+esc(s.ver)+(s.ok?' · '+s.ping+' ms':'')+'</div></div>';
  const meta='<div class="srv-meta">'+esc(s.last)+' 玩过 · '+esc(s.inst)+srvNote(s)+'</div>';
  return '<div class="srv-row" data-join="'+s.id+'">'+ico+'<div class="srv-main"><div class="srv-name">'+star+esc(s.name)+'</div>'+motd+meta+'</div>'+side+'</div>';
}
function renderSrv(){
  const list=srvSorted();
  $('recSrvList').innerHTML=list.map(s=>srvRow(s)).join('');
  $('srvAllBody').innerHTML='<div class="panel" style="padding:0">'+list.map(s=>srvRow(s)).join('')+'</div>';
  $('homeRecSrv').innerHTML=list.filter(s=>s.ok).slice(0,2).map(s=>'<div class="row" style="gap:8px"><span style="width:14px">'+ic('star')+'</span><div style="flex:1"><div style="font-size:12px;font-weight:600">'+esc(s.name)+'</div><div class="mut" style="font-size:10px">'+s.online+' 人在线 · '+s.ping+' ms</div></div></div>').join('');
  document.querySelectorAll('[data-lock]').forEach(x=>x.onclick=e=>{e.stopPropagation();const s=SERVERS.find(y=>y.id===x.dataset.lock);s.lock=!s.lock;renderSrv();log('ui','servers','lock','OK','detail='+s.id+' locked='+s.lock);});
  document.querySelectorAll('[data-join]').forEach(x=>x.ondblclick=()=>openJoin(SERVERS.find(y=>y.id===x.dataset.join)));
  document.querySelectorAll('[data-join]').forEach(x=>x.onclick=e=>{if(e.detail===1)log('ui','servers','select','OK','detail='+x.dataset.join+' single_click');});
}
function buildPlan(){
  const cfg=DEVICE[DEVICE_TIER];
  const list=srvSorted();
  const never=list.filter(neverSuccess);
  const active=list.filter(s=>!neverSuccess(s));
  const fresh=active.filter(s=>s.isNew);
  const rest=active.filter(s=>!s.isNew);
  const ordered=fresh.concat(rest);
  const probe=ordered.slice(0,cfg.limit);
  const out=ordered.slice(cfg.limit);
  list.forEach(s=>{s.probeSkip=null;});
  never.forEach(s=>{s.probeSkip='never';});
  out.forEach(s=>{s.probeSkip='out';});
  return {probe,out,never,cfg};
}
function updateBudget(){
  const cfg=DEVICE[DEVICE_TIER];
  const set=(id,v)=>{const e=$(id);if(e)e.textContent=v;};
  set('budTier',cfg.label);set('budLimit',cfg.limit);set('budConc',cfg.concurrency);
  set('budFlight',PROBE.inflight+' / '+Math.max(0,PROBE.total-PROBE.done-PROBE.inflight));
  set('budSkip',PROBE.skipped);
  const bar=$('budBar');if(bar)bar.style.width=(PROBE.total?Math.round(PROBE.done/PROBE.total*100):0)+'%';
  const hint=$('budHint');if(hint)hint.textContent=PROBE.cancelled?'已停止，不再发出新的连接；已经拿到的结果保留。':PROBE.running?'正在后台连接，界面先显示上次结果；慢的会自动跳过，随时可以停。':'按权重取前几台自动连；范围外的保留上次结果，不发请求。新加的服务器一定连，但总数还是卡在这个范围里。';
}
function applyResult(s,soft){
  s.isNew=false;s.tried=true;s.probeSkip=null;
  if(s.offlineMark){s.ok=false;s.ping=null;s.motd='';return;}
  s.ok=true;s.ever=true;
  if(s.ping===null||s.ping===undefined)s.ping=160;
  else s.ping=Math.max(20,s.ping+(soft?Math.round((Math.random()-.5)*16):-18));
  if(!s.motd)s.motd='§fA Minecraft Server';
  if(!s.max){s.max=20;s.online=1;}
}
function srvProbe(soft){
  if(PROBE.running)return;
  const plan=buildPlan();
  PROBE.plan=plan;PROBE.running=true;PROBE.cancelled=false;PROBE.inflight=0;PROBE.done=0;
  PROBE.total=plan.probe.length;PROBE.skipped=plan.out.length+plan.never.length;
  renderSrv();updateBudget();
  const cfg=plan.cfg;
  if(cfg.limit===0||plan.probe.length===0){
    PROBE.running=false;SERVERS_SYNC='刚刚';updateBudget();
    log('ui','servers','probe','SKIP','detail=budget=0 skipped='+PROBE.skipped);return;
  }
  let idx=0;
  const worker=()=>new Promise(res=>{
    const step=()=>{
      if(PROBE.cancelled||idx>=plan.probe.length){res();return;}
      const s=plan.probe[idx++];PROBE.inflight++;updateBudget();
      setTimeout(()=>{
        if(PROBE.cancelled){PROBE.inflight--;updateBudget();res();return;}
        applyResult(s,soft);PROBE.inflight--;PROBE.done++;
        renderSrv();updateBudget();step();
      },120+Math.round(Math.random()*150));
    };step();
  });
  const n=Math.min(cfg.concurrency,plan.probe.length);
  Promise.all(Array.from({length:n},worker)).then(()=>{
    PROBE.running=false;
    if(PROBE.cancelled){updateBudget();log('ui','servers','probe','CANCELLED','detail=inflight=0 no_new_request');return;}
    SERVERS_SYNC='刚刚';
    const lb=document.querySelector('[data-lb="servers"]');if(lb)lb.querySelector('.lb-age').textContent='刚刚';
    const t=$('srvRecTime');if(t)t.textContent='上次同步 刚刚';
    updateBudget();
    log('ui','servers','probe','OK','detail=async tier='+DEVICE_TIER+' limit='+cfg.limit+' conc='+cfg.concurrency+' done='+PROBE.done+' skipped='+PROBE.skipped);
  });
}
function srvCancel(){if(!PROBE.running)return;PROBE.cancelled=true;PROBE.inflight=0;updateBudget();}
function srvSwitchTier(){
  DEVICE_TIER=DEVICE_TIER==='normal'?'lightweight':'normal';
  const b=$('budSwitch');if(b)b.textContent=DEVICE_TIER==='normal'?'切到轻量档':'切回标准档';
  const plan=buildPlan();PROBE.skipped=plan.out.length+plan.never.length;PROBE.total=plan.probe.length;
  renderSrv();updateBudget();log('ui','servers','tier','OK','detail='+DEVICE_TIER+' limit='+plan.cfg.limit);
}
function srvScan(){
  $('srvScanState').textContent='3 个实例目录 · 8 台服务器';
  $('srvScanLog').innerHTML='[KCU] servers.dat 可见 6 · 隐藏 2 · 快速进入 1<br>[KCU] 异步预算 limit='+DEVICE[DEVICE_TIER].limit+' conc='+DEVICE[DEVICE_TIER].concurrency+'<br>[KCU] 范围外与没有成功记录的只按缓存权重排序，不发连接';
  if($('setSrvState'))$('setSrvState').textContent='3 个实例目录 · 8 台服务器';
  log('ui','servers','servers_dat','OK','detail=visible=6 hidden=2 quickplay=1 readonly=true');
}
function srvForceOffline(){
  const s=SERVERS.find(x=>x.id==='s2');s.ok=false;s.offlineMark=true;s.ping=null;s.motd='';renderSrv();
  $('srvScanLog').innerHTML='[KCU] 异步预算内 4 台 · 2 台范围外 · 2 台无成功记录<br>[KCU] 曾连上过但这轮连不上的排到最后，锁定的不动';
  log('ui','servers','offline','DEGRADE','detail=s2_timeout moved_to_bottom locked_unchanged');
}
function srvAdd(){
  const s={id:'s'+(SERVERS.length+1),name:'新加的服务器',ip:'new.example',ver:'1.21.4',motd:'',online:0,max:0,ping:null,ok:false,lock:false,ever:false,tried:false,isNew:true,last:'刚刚',inst:'1.21.4 Fabric',src:'servers.dat'};
  SERVERS.forEach(x=>{x.isNew=false;});SERVERS.push(s);
  renderSrv();srvScan();
  log('ui','servers','add','OK','detail=fresh_force_probe budget_unchanged');
  srvProbe(false);
}
function openJoin(s){
  const body='<p style="font-size:13px;color:var(--ink);margin-bottom:10px">准备进入 <b>'+esc(s.name)+'</b>（'+esc(s.ip)+'）</p>'+
   '<div class="attach" style="line-height:1.9">上次玩这个服用的实例：<b>'+esc(s.inst)+'</b>'+(s.lock?' · 已锁定':'')+'<br>'+
   '上次用过的实例：<b>1.21.4 Fabric</b><br>版本兼容范围：'+esc(s.ver)+' / 1.21.4 / 1.21.1<br>'+
   '自动选定：<b>'+esc(s.inst)+'</b>'+(s.ok?'':'<br><span style="color:var(--warn)">这台服务器现在连不上，仍可尝试进入</span>')+'</div>';
  openDlg('进入服务器',body,'join_'+s.id);
  $('mdActs').innerHTML='<button class="btn" id="jnCancel">取消</button><button class="btn" id="jnOther">换实例</button><button class="btn primary" id="jnGo">进入</button>';
  $('jnCancel').onclick=()=>closeDlg('cancel');
  $('jnOther').onclick=()=>{closeDlg('other');show('instances');};
  $('jnGo').onclick=()=>{closeDlg('confirm');log('dispatcher','server','join','OK','detail='+s.id+' instance='+s.inst+' weight=user_last');};
}
renderSrv();buildPlan();renderSrv();updateBudget();
$('srvRecRefresh').onclick=()=>srvProbe(true);
$('srvAdd').onclick=srvAdd;
$('srvScan').onclick=srvScan;
$('srvBindDemo').onclick=()=>openJoin(SERVERS[0]);
$('budSwitch').onclick=srvSwitchTier;
$('budCancel').onclick=srvCancel;
if($('setSrvScan'))$('setSrvScan').onclick=srvScan;
if($('setBudLimit'))$('setBudLimit').onchange=e=>{
  const v={'4 台（推荐）':4,'2 台':2,'6 台':6,'全部':SERVERS.length}[e.target.value]||4;
  DEVICE.normal.limit=v;buildPlan();renderSrv();updateBudget();log('ui','settings','budget','OK','detail=limit='+v);
};
if($('setBudConc'))$('setBudConc').onchange=e=>{
  const v={'3 路':3,'2 路':2,'1 路':1}[e.target.value]||3;
  DEVICE.normal.concurrency=v;updateBudget();log('ui','settings','budget','OK','detail=conc='+v);
};
if($('setBudTier'))$('setBudTier').onchange=e=>{
  const light=e.target.value.indexOf('自动')===0;
  DEVICE.lightweight.limit=light?2:DEVICE.normal.limit;
  DEVICE.lightweight.concurrency=light?2:DEVICE.normal.concurrency;
  buildPlan();renderSrv();updateBudget();log('ui','settings','budget','OK','detail=lightweight_auto='+light);
};
const srvLb=document.querySelector('[data-lb="servers"]');
if(srvLb){srvLb.querySelector('.lb-soft').onclick=()=>srvProbe(true);srvLb.querySelector('.lb-hard').onclick=()=>{srvScan();srvProbe(false);};}

'''
t = t[:start] + JS + t[end:]
print('OK js replaced')

# ---------- show 别名 ----------
a = "  if(v==='servers-locked'){show('servers');setTimeout(()=>srvForceOffline(),40);return;}"
b = a + "\n  if(v==='servers-budget'){show('servers');setTimeout(()=>srvProbe(true),40);return;}\n  if(v==='servers-history'){show('servers');DEVICE_TIER='lightweight';const bs=$('budSwitch');if(bs)bs.textContent='切回标准档';buildPlan();renderSrv();updateBudget();setTimeout(()=>srvProbe(true),40);return;}"
assert a in t, 'show alias'
t = t.replace(a, b, 1)
print('OK show aliases')

p.write_text(t)
print('STEP_OK', p.stat().st_size)

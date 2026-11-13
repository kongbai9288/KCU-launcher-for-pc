from pathlib import Path

p = Path('demos/ui-full-kcu-paper.html')
t = p.read_text()


def repl(a, b, label):
    global t
    assert a in t, label
    t = t.replace(a, b, 1)
    print('OK', label)


# 导航插件按钮改走设置分组
t = t.replace('<button class="nav-item" data-v="plugins">', '<button class="nav-item" data-gotab="plugins">')
t = t.replace('data-v="plugins">查看插件', 'data-gotab="plugins">查看插件', 1)
print('OK gotab entries')

# 关于页上层表已移除，避免空引用
a = "$('upperBody').innerHTML=UPPER.map(r=>'<tr><td>'+esc(r[0])+'</td><td><b>'+esc(r[1])+'</b></td><td>'+esc(r[2])+'</td><td>'+esc(r[3])+'</td><td><span class=\"badge off\">'+esc(r[4])+'</span></td></tr>').join('');"
b = "if($('upperBody'))$('upperBody').innerHTML=UPPER.map(r=>'<tr><td>'+esc(r[0])+'</td><td><b>'+esc(r[1])+'</b></td><td>'+esc(r[2])+'</td><td>'+esc(r[3])+'</td><td><span class=\"badge off\">'+esc(r[4])+'</span></td></tr>').join('');"
assert a in t, 'upperBody'
t = t.replace(a, b, 1)
t = t.replace("$('tabModified').onclick=()=>log('ui','settings','filter','OK','detail=@modified 3');",
              "$('tabModified').onclick=()=>log('ui','settings','filter','OK','detail=changed_only 3');", 1)
print('OK upperBody guard')

# ---------- 替换旧 REC_SRV 段 ----------
start = t.index("const REC_SRV=[")
end = t.index("$('aiTest').onclick=", start)
JS = r'''/* 021 服务器：自动连接、缓存权重、锁定置顶、失败沉底、双击进服 */
const SRV=[
 {id:'s1',name:'陶瓦联机 · 主服',ip:'mc.taowa.example',ver:'1.21.4',motd:'§a§l陶瓦联机 §7| §f生存季 S3\n§7每周六活动 · 欢迎回家',online:42,max:100,ping:42,ok:true,lock:true,last:'2 分钟前',inst:'生存季',src:'servers.dat'},
 {id:'s2',name:'朋友的小服',ip:'mc.friends.example:25566',ver:'1.21.1',motd:'§e小服 §7· §f别炸我家','online':6,max:20,ping:88,ok:true,lock:false,last:'昨天',inst:'测试服',src:'servers.dat'},
 {id:'s3',name:'快照体验服',ip:'snap.example',ver:'1.21.5',motd:'§6快照抢先玩\n§7内容随时会变',online:11,max:30,ping:120,ok:true,lock:false,last:'3 天前',inst:'快照服',src:'快速进入'},
 {id:'s4',name:'旧服（我锁过）',ip:'old.example',ver:'1.20.4',motd:'',online:0,max:0,ping:null,ok:false,lock:true,last:'上个月',inst:'怀旧服',src:'隐藏列表'},
 {id:'s5',name:'临时测试服',ip:'tmp.example',ver:'1.21.4',motd:'',online:0,max:0,ping:null,ok:false,lock:false,last:'两周前',inst:'测试服',src:'servers.dat'}
];
let SRV_SYNC='12 秒前';
function srvRank(s){
  if(s.lock)return 0;
  if(!s.ok)return 900;
  const recent=({'2 分钟前':0,'昨天':1,'3 天前':2,'两周前':3,'上个月':4})[s.last]||5;
  return 100+s.ping*0.4+recent*25+(100-s.online)*0.1;
}
function srvSorted(){return SRV.slice().sort((a,b)=>srvRank(a)-srvRank(b));}
function pingBars(s){
  if(!s.ok)return '<span class="mut" style="font-size:10px">连不上</span>';
  const n=s.ping<150?5:s.ping<300?4:s.ping<600?3:s.ping<1000?2:1;
  return '<span class="srv-ping">'+[1,2,3,4,5].map(i=>'<i style="'+(i>n?'opacity:.2':'')+'"></i>').join('')+'</span>';
}
function srvRow(s,compact){
  const star='<span class="lock-star" data-lock="'+s.id+'" title="锁定/取消锁定">'+(s.lock?'★':'☆')+'</span>';
  const ico='<div class="srv-ico'+(s.ok?'':' off')+'">'+esc(s.name.charAt(0))+'</div>';
  const motd=s.ok?'<div class="srv-motd">'+esc(s.motd.replace(/§[0-9a-fklmnor]/g,''))+'</div>':'<div class="srv-motd" style="color:var(--ink-3)">无法连接到服务器</div>';
  const side='<div class="srv-side"><div class="srv-count">'+(s.ok?s.online+' / '+s.max:'—')+'</div>'+pingBars(s)+'<div class="srv-ver">'+esc(s.ver)+(s.ok?' · '+s.ping+' ms':'')+'</div></div>';
  const meta='<div class="srv-meta">'+esc(s.last)+' 玩过 · '+esc(s.inst)+(s.lock?' · 已锁定':'')+'</div>';
  return '<div class="srv-row" data-join="'+s.id+'">'+ico+'<div class="srv-main"><div class="srv-name">'+star+esc(s.name)+'</div>'+motd+meta+'</div>'+side+'</div>';
}
function renderSrv(){
  const list=srvSorted();
  $('recSrvList').innerHTML=list.map(s=>srvRow(s)).join('');
  $('srvAllBody').innerHTML='<div class="panel" style="padding:0">'+list.map(s=>srvRow(s)).join('')+'</div>';
  $('homeRecSrv').innerHTML=list.slice(0,2).map(s=>'<div class="row" style="gap:8px"><span style="width:14px">'+ic('star')+'</span><div style="flex:1"><div style="font-size:12px;font-weight:600">'+esc(s.name)+'</div><div class="mut" style="font-size:10px">'+(s.ok?s.online+' 人在线 · '+s.ping+' ms':'连不上'+(s.lock?' · 已锁定':''))+'</div></div></div>').join('');
  document.querySelectorAll('[data-lock]').forEach(x=>x.onclick=e=>{e.stopPropagation();const s=SRV.find(y=>y.id===x.dataset.lock);s.lock=!s.lock;renderSrv();log('ui','servers','lock','OK','detail='+s.id+' locked='+s.lock);});
  document.querySelectorAll('[data-join]').forEach(x=>x.ondblclick=()=>openJoin(SRV.find(y=>y.id===x.dataset.join)));
  document.querySelectorAll('[data-join]').forEach(x=>x.onclick=e=>{if(e.detail===1)log('ui','servers','select','OK','detail='+x.dataset.join+' single_click');});
}
function openJoin(s){
  const body='<p style="font-size:13px;color:var(--ink);margin-bottom:10px">准备进入 <b>'+esc(s.name)+'</b>（'+esc(s.ip)+'）</p>'+
   '<div class="attach" style="line-height:1.9">上次玩这个服用的实例：<b>'+esc(s.inst)+'</b>'+(s.lock?' · 已锁定':'')+'<br>'+
   '上次用过的实例：<b>1.21.4 Fabric</b><br>版本兼容范围：'+esc(s.ver)+' / 1.21.4 / 1.21.1<br>'+
   '自动选定：<b>'+(s.lock?s.inst:esc(s.inst))+'</b>'+(s.ok?'':'<br><span style="color:var(--warn)">这台服务器现在连不上，仍可尝试进入</span>')+'</div>';
  openDlg('进入服务器',body,'join_'+s.id);
  $('mdActs').innerHTML='<button class="btn" id="jnCancel">取消</button><button class="btn" id="jnOther">换实例</button><button class="btn primary" id="jnGo">进入</button>';
  $('jnCancel').onclick=()=>closeDlg('cancel');
  $('jnOther').onclick=()=>{closeDlg('other');show('instances');};
  $('jnGo').onclick=()=>{closeDlg('confirm');log('dispatcher','server','join','OK','detail='+s.id+' instance='+s.inst+' weight=user_last');};
}
function srvSync(soft){
  SRV.forEach(s=>{if(s.ok&&!s.lock){s.ping=Math.max(20,s.ping+(soft?Math.round((Math.random()-.5)*16):-18));}});
  SRV_SYNC='刚刚';$('srvRecTime').textContent='上次同步 刚刚';
  const lb=document.querySelector('[data-lb="servers"]');if(lb){lb.querySelector('.lb-age').textContent='刚刚';}
  renderSrv();log('ui','servers','autoconnect','OK','detail=4_online 1_offline locked_pinned');
}
function srvScan(){
  $('srvScanState').textContent='3 个实例目录 · 5 台服务器';
  $('srvScanLog').innerHTML='[KCU] servers.dat 可见 4 · 隐藏 2 · 快速进入 1<br>[KCU] 连接 4 成功 / 1 失败 · 锁定 2 台保持靠前';
  if($('setSrvState'))$('setSrvState').textContent='3 个实例目录 · 5 台服务器';
  log('ui','servers','servers_dat','OK','detail=visible=4 hidden=2 quickplay=1 readonly=true');
}
function srvForceOffline(){
  const s=SRV.find(x=>x.id==='s2');s.ok=false;s.ping=null;s.motd='';renderSrv();
  $('srvScanLog').innerHTML='[KCU] 连接 3 成功 / 2 失败 · 锁定 2 台保持靠前<br>[KCU] 连不上的已排到列表最后';
  log('ui','servers','offline','DEGRADE','detail=s2_timeout moved_to_bottom locked_unchanged');
}
function srvAdd(){
  const s={id:'s6',name:'新加的服务器',ip:'new.example',ver:'1.21.4',motd:'§fA Minecraft Server',online:1,max:20,ping:66,ok:true,lock:false,last:'刚刚',inst:'1.21.4 Fabric',src:'servers.dat'};
  SRV.push(s);renderSrv();srvScan();
  log('ui','servers','add','OK','detail=auto_connect_immediately cached_as_weight');
}
renderSrv();
$('srvRecRefresh').onclick=()=>srvSync(true);
$('srvAdd').onclick=srvAdd;
$('srvScan').onclick=srvScan;
$('srvBindDemo').onclick=()=>openJoin(SRV[0]);
if($('setSrvScan'))$('setSrvScan').onclick=srvScan;
document.querySelectorAll('.logicbar [data-lb="servers"]').forEach(()=>{});
const srvLb=document.querySelector('[data-lb="servers"]');
if(srvLb){srvLb.querySelector('.lb-soft').onclick=()=>srvSync(true);srvLb.querySelector('.lb-hard').onclick=()=>{srvScan();srvSync(false);};}

'''
t = t[:start] + JS + t[end:]
print('OK srv js replaced')

# gotab 路由（在 [data-v] 绑定之后追加）
anchor = "document.querySelectorAll('[data-v]').forEach(b=>b.onclick=()=>show(b.dataset.v));"
assert anchor in t
t = t.replace(anchor, anchor + "\ndocument.querySelectorAll('[data-gotab]').forEach(b=>b.onclick=()=>{show('settings');setTab(b.dataset.gotab);log('ui','settings','tab','OK','detail='+b.dataset.gotab);});", 1)

# show 别名：双击进服弹窗 / 失败沉底
a = "  if(v==='update'){show('home');openDlg('发现新版本 0.0.1','<p>批量下载、公告中心、纸质界面与 18 张预览图已就绪。</p><div class=\"attach\">更新日志 14 项 · 可「稍后」或「立即更新」</div>','update');return;}"
b = a + "\n  if(v==='server-join'){show('servers');setTimeout(()=>openJoin(SRV[0]),40);return;}\n  if(v==='servers-locked'){show('servers');setTimeout(()=>srvForceOffline(),40);return;}"
assert a in t, 'show alias anchor'
t = t.replace(a, b, 1)
print('OK show aliases')

p.write_text(t)
print('STEP_B_OK', p.stat().st_size)

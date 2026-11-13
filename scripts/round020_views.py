from pathlib import Path

p = Path('demos/ui-full-kcu-paper.html')
t = p.read_text()


def I(n):
    return '<svg class="li" aria-hidden="true"><use href="#i-' + n + '"></use></svg>'


def LB(v):
    return ('<div class="logicbar" data-lb="' + v + '"><span class="lb-t">' + I('database') +
            ' 已缓存 · <b class="lb-age">12 秒前</b></span><span class="lb-t">' + I('gauge') +
            ' 命中 <b class="lb-hit">8</b> / 未命中 <b class="lb-miss">1</b></span><span class="lb-sp"></span>' +
            '<span class="badge ok lb-state">就绪</span><button class="btn lb-soft">' + I('refresh-cw') +
            ' 刷新</button><button class="btn lb-hard">' + I('rotate-ccw') + ' 强制刷新</button></div>')


S = []


def sec(v, body):
    S.append('      <section class="view" data-view="' + v + '">\n        ' + LB(v) + '\n' + body + '\n      </section>\n')


sec('slots', '''
        <div class="grid g2">
          <div class="panel"><div class="panel-head"><div class="panel-title">槽位注册表</div><div class="panel-sub">core.* 保留 · plugin.* 开放</div>
            <div class="panel-tools"><button class="btn primary tiny" id="slotConflict">模拟插件占用核心槽位</button><button class="btn tiny" id="slotReset">复位</button></div></div>
            <table class="lic-table"><thead><tr><th>槽位 ID</th><th>归属</th><th>可写方</th><th>位置</th><th>状态</th></tr></thead><tbody>
              <tr><td>core.locked.settings</td><td>核心</td><td>仅核心</td><td>导航底部固定区</td><td><span class="badge err">锁定</span></td></tr>
              <tr><td>core.locked.about</td><td>核心</td><td>仅核心</td><td>导航底部固定区</td><td><span class="badge err">锁定</span></td></tr>
              <tr><td>core.nav.home</td><td>核心</td><td>仅核心</td><td>主导航首位</td><td><span class="badge ok">固定</span></td></tr>
              <tr><td>core.nav.servers</td><td>核心</td><td>仅核心</td><td>主导航第 4 位</td><td><span class="badge ok">固定</span></td></tr>
              <tr><td>plugin.nav.*</td><td>插件区</td><td>插件</td><td>分隔线下独立容器</td><td><span class="badge up">开放</span></td></tr>
              <tr><td>plugin.settings.*</td><td>设置内插件分组</td><td>插件</td><td>设置页末尾</td><td><span class="badge up">开放</span></td></tr>
              <tr><td>plugin.about.credits</td><td>关于页追加区</td><td>插件</td><td>开源致谢之后</td><td><span class="badge up">开放</span></td></tr>
            </tbody></table>
            <div class="notice" id="slotDeny" style="margin-top:11px;display:none;border-color:var(--warn)"><div class="notice-ico" style="color:var(--warn)">''' + I('circle-x') + '''</div><div class="notice-main"><div class="notice-title" style="color:var(--warn)">注册被拒绝 · core.locked.settings 已占用</div><div class="notice-body">插件 `plugin.example` 试图占用核心槽位。注册表拒绝写入、保留原条目、写 [KCU] 诊断行；插件自身不崩溃，可改用 plugin.nav.*。</div></div><button class="btn tiny" id="slotDenyClose" style="align-self:center">知道了</button></div>
          </div>
          <div class="stack">
            <div class="panel"><div class="panel-head"><div class="panel-title">锁定规则</div></div>
              <div class="stack" style="font-size:12px;color:var(--ink-2)">
                <div class="notice" style="box-shadow:none;padding:9px"><div class="notice-ico">''' + I('lock-keyhole') + '''</div><div class="notice-main"><div class="notice-body">设置与关于固定在同一容器，位置、顺序、ID 三者都不可变更。</div></div></div>
                <div class="notice" style="box-shadow:none;padding:9px"><div class="notice-ico">''' + I('shield-check') + '''</div><div class="notice-main"><div class="notice-body">插件与更新包只能追加到 plugin.* 容器；core.* 冲突一律拒绝注册。</div></div></div>
                <div class="notice" style="box-shadow:none;padding:9px"><div class="notice-ico">''' + I('refresh-cw') + '''</div><div class="notice-main"><div class="notice-body">插件化更新不替换核心二进制，只替换插件包；失败保留旧插件并可回滚。</div></div></div>
                <div class="notice" style="box-shadow:none;padding:9px"><div class="notice-ico">''' + I('scale') + '''</div><div class="notice-main"><div class="notice-body">插件加载后在关于页追加插件名、许可证、作者、项目地址、修改后版本地址。</div></div></div>
              </div></div>
            <div class="panel"><div class="panel-head"><div class="panel-title">插件清单校验</div></div>
              <table class="grid"><thead><tr><th>项</th><th>口径</th></tr></thead><tbody>
                <tr><td>清单</td><td>manifest 只声明贡献，不执行代码</td></tr>
                <tr><td>边界</td><td>C ABI / 进程隔离，Rust ABI 不跨边界</td></tr>
                <tr><td>版本</td><td>ABI_MAJOR 不匹配拒绝加载</td></tr>
                <tr><td>校验</td><td>摘要 + 签名 + 路径遍历防护</td></tr>
                <tr><td>预算</td><td>耗时上限，超时可终止</td></tr>
              </tbody></table></div>
          </div>
        </div>''')

sec('recommendations', '''
        <div class="panel"><div class="panel-head"><div class="panel-title">推荐位总览 · 10 处</div><div class="panel-sub">每处都有内容、权重、用户覆盖、缓存与刷新设置</div>
          <div class="panel-tools"><button class="btn tiny" data-v="servers">服务器推荐位</button><button class="btn tiny" data-v="settings">推荐设置</button><span class="badge ok">10 / 10 已定义</span></div></div>
          <table class="lic-table"><thead><tr><th>位置</th><th>推荐内容</th><th>默认权重</th><th>用户覆盖</th><th>缓存 / 刷新</th><th>设置 ID</th></tr></thead><tbody id="recCatalog"></tbody></table>
        </div>
        <div class="grid g3" style="margin-top:12px">
          <div class="panel"><h3 class="sec">用户指定排第一</h3><div class="mut" style="font-size:12px">手动选过的实例、显式指定的服务器、固定的排序值，永远压过系统推荐。</div></div>
          <div class="panel"><h3 class="sec">不感兴趣只降权</h3><div class="mut" style="font-size:12px">降权不隐藏，避免用户失去找回入口；权重数值可在设置里改。</div></div>
          <div class="panel"><h3 class="sec">来源可插拔</h3><div class="mut" style="font-size:12px">本地 / 官方 / 插件三类来源可单独开关；插件来源走 plugin.rec.* 槽位，不改 core.rec.*。</div></div>
        </div>''')

sec('handoff', '''
        <div class="grid g2">
          <div class="panel"><div class="panel-head"><div class="panel-title">可交接底层基线</div><div class="panel-sub">新对话把本仓库当底层直接接续</div></div>
            <div class="kv"><span class="k">仓库</span><span>kongbai9288/KCU-launcher-for-pc / main / public</span>
              <span class="k">基线</span><span>020 轮提交，工作区干净，231+ 文件</span>
              <span class="k">必读</span><span>docs/index.md 78 项，按命令逐项复读</span>
              <span class="k">工具链</span><span>腾讯 rustup 镜像；CARGO_HOME / RUSTUP_HOME 在工作区</span>
              <span class="k">测试</span><span>CARGO_INCREMENTAL=0 cargo test --offline</span>
              <span class="k">本地 LICENSE</span><span><span class="badge miss">未生成</span></span></div></div>
          <div class="panel"><div class="panel-head"><div class="panel-title">已完成 / 未完成</div></div>
            <table class="grid"><thead><tr><th>层</th><th>状态</th></tr></thead><tbody>
              <tr><td>L1 core</td><td><span class="badge ok">已实现、已验证</span></td></tr>
              <tr><td>L2 dispatcher</td><td><span class="badge ok">已实现、已验证</span></td></tr>
              <tr><td>L3 lightweight</td><td><span class="badge ok">已实现、已验证</span></td></tr>
              <tr><td>UI / normal</td><td><span class="badge up">演示层 36 视图</span></td></tr>
              <tr><td>L4 headless 及以下 6 层</td><td><span class="badge off">未启动</span></td></tr>
            </tbody></table></div>
        </div>
        <div class="panel" style="margin-top:12px"><div class="panel-head"><div class="panel-title">新对话开工 6 步</div><div class="panel-sub">照此顺序就不会丢上下文</div></div>
          <div class="row"><span class="chip on">1 读 docs/index.md 78 项</span><span class="chip">2 读 docs/design/handoff.md</span><span class="chip">3 读 docs/records/rounds.md 末段</span><span class="chip">4 跑必读检查命令</span><span class="chip">5 跑 cargo test --offline</span><span class="chip">6 对照 docs/features/index.md 继续施工</span></div>
        </div>
        <div class="grid g2" style="margin-top:12px">
          <div class="panel"><div class="panel-head"><div class="panel-title">不可变边界</div></div>
            <div class="stack" style="font-size:12px;color:var(--ink-2)">
              <div>全仓零凭据字面量；后端仓只读；私有配置、诊断包、令牌不进公仓。</div>
              <div>core.locked.* 槽位不可被插件或更新包改写。</div>
              <div>未取得 LICENSE 全文前不复制上游代码、资源、商标、Client ID。</div>
              <div>未证实字段不写进实现；四值只用已证实 / 已失败 / 未证实 / 受阻。</div>
              <div>每实现一个功能写一份功能 md，维护 docs/index.md 与 docs/features/index.md。</div>
            </div></div>
          <div class="panel"><div class="panel-head"><div class="panel-title">上层实现口径</div></div>
            <div class="stack" style="font-size:12px;color:var(--ink-2)">
              <div>上层实现采用第三方库，候选清单见关于页与 docs/design/upper-layer-stack.md。</div>
              <div>每个候选标许可证、用途、来源、是否取得 LICENSE 全文、是否进入构建。</div>
              <div>插件化更新优先；核心不随更新替换；失败保留旧插件并可回滚。</div>
              <div>演示确认后才把 UI 写进实现；轻量模式不复用 normal.ui。</div>
            </div></div>
        </div>''')

block = '\n'.join(S)
anchor = '\n      </div>\n    </main>'
assert anchor in t, 'main end'
t = t.replace(anchor, '\n' + block + anchor, 1)
print('SECTIONS_OK', len(S))

# VIEW_META
vm_anchor = " states:['状态与降级','六态 · 缓存兜底 · 降级链']};"
vm_new = (" states:['状态与降级','六态 · 缓存兜底 · 降级链'],\n"
          " slots:['插件槽位与锁定','core.locked.* 不可占用 · plugin.* 开放'],\n"
          " recommendations:['推荐位总览','10 处推荐 · 权重 / 覆盖 / 刷新'],\n"
          " handoff:['底层交接基线','新对话把本仓库当底层直接接续']};")
assert vm_anchor in t, 'view_meta'
t = t.replace(vm_anchor, vm_new, 1)

# show() 支持 settings&tab
old = "  const m=VIEW_META[v]||VIEW_META.home;$('vTitle').textContent=m[0];$('vCrumb').textContent=m[1];\n  history.replaceState(null,'','#view='+v);"
new = ("  const tab=(location.hash.match(/tab=([a-z-]+)/)||[])[1]||'general';\n"
       "  if(v==='settings')setTab(tab);\n"
       "  const m=VIEW_META[v]||VIEW_META.home;$('vTitle').textContent=m[0];$('vCrumb').textContent=m[1];\n"
       "  history.replaceState(null,'',v==='settings'?'#view=settings&tab='+tab:'#view='+v);")
assert old in t, 'show replace'
t = t.replace(old, new, 1)

JS = r'''
/* 020 设置分组、槽位锁定、推荐目录、服务器状态与交接 */
function ic(n){return '<svg class="li" aria-hidden="true"><use href="#i-'+n+'"></use></svg>';}
function setTab(k){
  document.querySelectorAll('[data-pane]').forEach(x=>x.classList.toggle('on',x.dataset.pane===k));
  document.querySelectorAll('[data-tab]').forEach(x=>x.classList.toggle('on',x.dataset.tab===k));
}
document.querySelectorAll('[data-tab]').forEach(x=>x.onclick=()=>{setTab(x.dataset.tab);log('ui','settings','tab','OK','detail='+x.dataset.tab);});
$('tabModified').onclick=()=>log('ui','settings','filter','OK','detail=@modified 3');
$('tabReset').onclick=()=>openDlg('恢复默认','<p>将把本页已改动的 3 项恢复到默认值，需二次确认。</p><div class="attach">取消后 0 副作用；写盘失败保留旧值并可见报错。</div>','settings_reset');
$('setCacheExpired').onclick=()=>log('ui','cache','clean','OK','detail=expired_only');
$('setCacheAll').onclick=()=>openDlg('全清缓存','<p>四层缓存将被清空，含令牌缓存，需二次确认。</p>','settings_cache_all');
$('setAiTest').onclick=()=>{$('setAiState').innerHTML='<span class="badge ok">已连接</span>';$('setAiResult').textContent='连接成功';log('ui','ai','test','OK','detail=settings_scoped');};
$('plugUpdate').onclick=()=>{$('plugState').textContent='插件包已更新 · 核心 0.0.0 未替换';$('plugState').className='badge ok';log('update','plugin','install','OK','detail=signed core_untouched');};
$('plugRollback').onclick=()=>{$('plugState').textContent='已回滚到旧插件 · 核心 0.0.0 未替换';$('plugState').className='badge up';log('update','plugin','rollback','OK','detail=old_plugin_restored');};

const UPPER=[
 ['UI 窗口 / WebView','tao + wry','Apache-2.0 / MIT','桌面窗口与网页渲染','候选 · 未进构建'],
 ['UI 方案备选','slint','三许可（Royalty-free / GPLv3 / Commercial）','声明式界面','候选 · 未进构建'],
 ['UI 方案备选','egui / iced','Apache-2.0 / MIT','即时模式界面','候选 · 未进构建'],
 ['序列化','serde + serde_json','MIT OR Apache-2.0','配置 / 清单 / 统一信封','候选 · 未进构建'],
 ['网络','reqwest','MIT OR Apache-2.0','批量请求 / 单飞 / 竞速','候选 · 未进构建'],
 ['异步','tokio','MIT','任务调度与取消','候选 · 未进构建'],
 ['版本比较','semver','MIT OR Apache-2.0','插件化更新版本判定','候选 · 未进构建'],
 ['哈希 / 校验','sha2','MIT OR Apache-2.0','文件与插件摘要','候选 · 未进构建'],
 ['错误','anyhow + thiserror','MIT OR Apache-2.0','错误链','候选 · 未进构建'],
 ['插件加载','libloading','ISC','动态库加载（C ABI）','候选 · 未进构建'],
 ['更新','tauri-plugin-updater / self_update','Apache-2.0 / MIT','签名校验与回滚','候选 · 未进构建'],
 ['本地存储','rusqlite','MIT','索引与状态缓存','候选 · 未进构建'],
];
$('upperBody').innerHTML=UPPER.map(r=>'<tr><td>'+esc(r[0])+'</td><td><b>'+esc(r[1])+'</b></td><td>'+esc(r[2])+'</td><td>'+esc(r[3])+'</td><td><span class="badge off">'+esc(r[4])+'</span></td></tr>').join('');

const REC_CATALOG=[
 ['首页启动卡','上次实例 / 最近 3 个','最近使用 > 推荐','手动选过置顶','30s / 事件推送','core.rec.home_launch'],
 ['首页推荐服务器','兼容 + 习惯','用户指定 > 兼容度 > 延迟','指定实例排第一','60s / 测速刷新','core.rec.home_server'],
 ['版本页','稳定版','稳定 > 快照','用户指定排第一','24h / 强制刷新','core.rec.version'],
 ['下载页','缺失依赖 / 可更新','缺依赖优先','手动清单优先','30s / 完成事件','core.rec.download'],
 ['模组页','可更新 / 缺依赖','缺失优先','手动禁用保持','60s / 扫描事件','core.rec.mods'],
 ['公告中心','置顶','置顶 > 时间','不再提示降权','5min / 增量刷新','core.rec.notices'],
 ['加载器','与实例兼容','兼容度 > 热度','用户指定优先','24h / 强制刷新','core.rec.loader'],
 ['Java','稳定版本','稳定 > 预览','用户指定优先','24h / 手动刷新','core.rec.java'],
 ['镜像源','测速结果','延迟 > 可用性','用户强制指定','60s / 测速刷新','core.rec.mirror'],
 ['插件','已装且启用','用户评分 > 更新日','手动置顶','会话内 / 安装事件','core.rec.plugin'],
];
$('recCatalog').innerHTML=REC_CATALOG.map(r=>'<tr><td><b>'+esc(r[0])+'</b></td><td>'+esc(r[1])+'</td><td>'+esc(r[2])+'</td><td>'+esc(r[3])+'</td><td>'+esc(r[4])+'</td><td><span class="mini">'+esc(r[5])+'</span></td></tr>').join('');

$('slotConflict').onclick=()=>{$('slotDeny').style.display='flex';log('plugins','slot','register','DENY','detail=core.locked.settings already_occupied plugin=example');};
$('slotDenyClose').onclick=()=>{$('slotDeny').style.display='none';};
$('slotReset').onclick=()=>{$('slotDeny').style.display='none';log('plugins','slot','reset','OK','detail=registry_clean');};
'''
anchor2 = '/* 初始 */'
assert anchor2 in t, 'init anchor'
t = t.replace(anchor2, JS + '\n' + anchor2, 1)
p.write_text(t)
print('STEP_B_OK', p.stat().st_size, 'sections', t.count('<section class="view'), 'logicbars', t.count('class="logicbar"'))

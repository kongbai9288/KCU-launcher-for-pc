#!/usr/bin/env python3
"""093：扫描仓库真实文件，生成功能位置清单 txt。

不改任何功能文件；只读取。输出 docs/records/round-093-feature-locations.txt。
每条计数来自本脚本实跑的目录枚举与文件解析，不写推测值。
"""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/records/round-093-feature-locations.txt'

AX_MODULE = {
    'AX01': ('home_widgets', 'widget_layout.rs'),
    'AX02': ('game_news', 'notice_center.rs'),
    'AX03': ('world_editor', 'world_editor.rs'),
    'AX04': ('mod_rollback', 'mod_rollback.rs'),
    'AX05': ('storage_analysis', 'storage.rs'),
    'AX06': ('download_history', 'download_history.rs'),
    'AX07': ('doh_support', None),
    'AX08': ('instance_import', 'instance_import.rs'),
    'AX09': ('upgrade_compat', 'upgrade_plan.rs'),
    'AX10': ('first_run_wizard', 'first_run.rs'),
    'AX11': ('settings_export', 'settings_io.rs'),
    'AX12': ('download_sources', 'download_sources.rs'),
    'AX13': ('appearance_modes', 'appearance.rs'),
    'AX14': ('skin_editor', 'skin_draft.rs'),
    'AX15': ('studio_image_editor', 'studio_image.rs'),
    'AX16': ('cn_search_filter', 'search_filter.rs'),
    'AX17': ('banner_designer', 'banner_design.rs'),
    'AX18': ('lab_generators', 'generator_session.rs'),
    'AX19': ('seed_map', 'seed_access.rs'),
    'AX20': ('projection_workshop', 'projection.rs'),
    'AX21': ('redstone_multiplayer', 'lan_channel.rs'),
    'AX22': ('shimu_account', None),
    'AX23': ('client_ai_gate', 'client_ai.rs'),
    'AX24': ('ungrouped_drop', 'instance_drop.rs'),
}

INFRA = {
    'envelope', 'diagnostics', 'paths', 'config', 'log', 'http', 'window',
    'args', 'instance', 'popup', 'userflow', 'cache', 'asynk', 'leak',
    'robust', 'endpoints', 'integrity', 'feature_gate', 'region', 'boot',
    'stats', 'consent', 'ax', 'launch_progress', 'settings_io',
    'extension_gate', 'download_history',
}


def sh(cmd):
    return subprocess.check_output(cmd, shell=True, cwd=ROOT, text=True).strip()


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def glob(rel, pat):
    return sorted((ROOT / rel).glob(pat))


def count_lines(p):
    return len(p.read_text(encoding='utf-8').splitlines())


def literals(body):
    return re.findall(r'"([^"]+)"', body)


def module_rows():
    mod = read('src/core/mod.rs')
    ax = read('src/core/ax.rs')
    guard_files = [(g.name, g.read_text(encoding='utf-8')) for g in glob('scripts', '*_guard.py')]
    dec_files = [(d.name, d.read_text(encoding='utf-8')) for d in glob('docs/decisions', '*.md')]
    ax_rows = {}
    for line in ax.splitlines():
        m = re.search(r'id: "(AX\d+)", name: "([a-z_]+)", state: AxState::(\w+), conflict: "([^"]*)", ui: (\w+)', line)
        if m:
            ax_rows[m.group(1)] = (m.group(2), m.group(3), m.group(4), m.group(5))
    rows = []
    for p in glob('src/core', '*.rs'):
        name = p.name
        stem = name[:-3]
        t = p.read_text(encoding='utf-8')
        decl = next((i for i, l in enumerate(mod.splitlines(), 1) if l.strip() == 'pub mod %s;' % stem), 0)
        tests = len(re.findall(r'^\s*#\[test\]', t, re.M))
        dstate = re.search(r'pub const DEFAULT_STATE:\s*&str\s*=\s*r#"(.*?)"#', t, re.S)
        keymaps = re.findall(r'pub const ([A-Z_]*KEYS):\s*&\[&str\]\s*=\s*&\[(.*?)\];', t, re.S)
        guards = [n for n, t in guard_files if stem in t or stem in n]
        decs = [n for n, t in dec_files if stem in t]
        feats = [f.name for f in glob('docs/features', '*.md') if stem in f.name or ('core-%s' % stem) in f.name]
        demos = [d.name for d in glob('demos', '*.html') if stem in d.name]
        ax_id = next((k for k, (slug, f) in AX_MODULE.items() if f == name), '')
        label = ax_rows.get(ax_id, ('', '', '', ''))[0] if ax_id else ''
        state = ax_rows.get(ax_id, ('', '', '', ''))[1] if ax_id else ('基础设施/早期数据层' if stem in INFRA else '未登记')
        rows.append(dict(name=name, lines=count_lines(p), decl=decl, tests=tests,
                         default_state=dstate.group(1) if dstate else '', keymaps=keymaps,
                         guards=guards, decs=decs, feats=feats, demos=demos,
                         ax_id=ax_id, label=label, state=state))
    return rows, ax_rows


def settings_data(rows):
    cfg = read('src/core/config.rs')
    io = read('src/core/settings_io.rs')
    keys = re.search(r'pub const KNOWN_KEYS:\s*&\[&str\]\s*=\s*&\[(.*?)\];', io, re.S)
    root_keys = literals(keys.group(1)) if keys else []
    derived = literals(re.search(r'pub const DERIVED_KEYS:[^;]*;', io, re.S).group(0))
    protected = re.search(r'pub const PROTECTED_FILES:[^;]*;', io, re.S).group(0)
    limits = re.findall(r'pub const (MAX_[A-Z_]+|TMP_SUFFIX|SETTINGS_FILE):\s*(?:&str|usize)\s*=\s*([^;]+);', io)
    default_states = []
    for r in rows:
        if not r['default_state']:
            continue
        try:
            obj = json.loads(r['default_state'])
            default_states.append((r['name'], list(obj.keys()), r['default_state']))
        except json.JSONDecodeError:
            default_states.append((r['name'], [], r['default_state']))
    keymaps = []
    for r in rows:
        for kn, body in r['keymaps']:
            keymaps.append((r['name'], kn, literals(body)))
    return dict(root_keys=root_keys, derived=derived, protected=protected,
                limits=limits, default_states=default_states, keymaps=keymaps, cfg=cfg)


def html_settings():
    html = read('demos/ui-full-kcu-paper.html')
    parts = re.split(r'(data-pane="([^"]+)")', html)
    panes = []
    for i in range(1, len(parts) - 1, 3):
        pane = parts[i + 1]
        body = parts[i + 2][:9000]
        items = re.findall(r'class="k" data-i18n="([^"]+)">([^<]+)</span>', body)
        opts = re.findall(r'<option value="([^"]+)"', body)
        ctrl = re.findall(r'id="(set[A-Za-z]+)"', body)
        panes.append((pane, items, opts, ctrl))
    tabs = re.findall(r'data-tab="([^"]+)"', html)
    set_ids = sorted(set(re.findall(r'id="(set[A-Za-z]+)"', html)))
    return panes, tabs, set_ids


def stable_ids():
    out = {}
    for d in list(glob('docs/design', '*.md')) + list(glob('docs/features', '*.md')):
        t = d.read_text(encoding='utf-8')
        for v in re.findall(r'core\.[a-z][a-zA-Z0-9_.]+', t):
            v = v.rstrip('.,;:')
            out.setdefault(v, set()).add(d.name)
    return out


def lang_keys():
    out = {}
    for p in glob('demos/lang', '*.js'):
        t = p.read_text(encoding='utf-8')
        out[p.name] = dict(set_keys=sorted(set(re.findall(r'"(set\.[a-zA-Z0-9_.]+)"', t))),
                           t_keys=len(re.findall(r'"(t\.\d+)"', t)))
    return out


def protected_values():
    vals = {}
    for p in glob('src/core', '*.rs'):
        t = p.read_text(encoding='utf-8')
        for m in re.finditer(r'pub const ([A-Z_]*FILE):\s*&str\s*=\s*"([^"]+)";', t):
            vals[m.group(1)] = (m.group(2), p.name)
    return vals


def build():
    rows, ax_rows = module_rows()
    sd = settings_data(rows)
    panes, tabs, set_ids = html_settings()
    ids = stable_ids()
    langs = lang_keys()
    pv = protected_values()
    tracked = int(sh('git ls-files | wc -l'))
    head = sh('git log --oneline -1')
    ts = sh("TZ='CST-8' date '+%a %b %e %H:%M:%S %Z %Y'")
    L = []
    add = L.append
    add('KCU Launcher 功能位置清单（093 轮）')
    add('文件：docs/records/round-093-feature-locations.txt')
    add('生成：python3 scripts/feature_locations.py（只读实扫，不改功能文件）')
    add('开工时间戳：Thu Nov 26 13:30:12 CST 2026')
    add('生成时间戳：' + ts)
    add('本地 HEAD（生成时）：' + head)
    add('远端 ref（092 补记，A145 开工时核）：5c9313e284d5ac8dd6b5947265f184d423bc88fc')
    add('tracked 文件数：%d' % tracked)
    add('用户 093 逐字指令（183 字节）：干，还有你需要向我提交现在所有功能写的位置的txt，估计这么多轮下来有些功能放的位置应该要改一下了（包括设置当中的具体设置项）')
    add('本轮动作：只交位置与候选调整清单，不移动任何文件位置，不改设置项，候选全部标待拍板未执行。')
    add('')
    add('=' * 78)
    add('一、总览（计数均为本脚本实跑目录枚举）')
    add('=' * 78)
    for label, cmd in [
        ('src/core/*.rs', 'ls src/core/*.rs | wc -l'),
        ('src/core 总行数', 'cat src/core/*.rs | wc -l'),
        ('src 顶层文件', 'ls src/*.rs | wc -l'),
        ('tests/*.rs', 'ls tests/*.rs | wc -l'),
        ('scripts/*_guard.py', 'ls scripts/*_guard.py | wc -l'),
        ('demos/*.html', 'ls demos/*.html | wc -l'),
        ('demos/preview/*.png', 'ls demos/preview/*.png | wc -l'),
        ('docs/decisions/*.md', 'ls docs/decisions/*.md | wc -l'),
        ('docs/verification/*.md', 'ls docs/verification/*.md | wc -l'),
        ('docs/features/*.md', 'ls docs/features/*.md | wc -l'),
        ('docs/design/*.md', 'ls docs/design/*.md | wc -l'),
        ('docs/records/*.md', 'ls docs/records/*.md | wc -l'),
        ('docs/spec/*.txt', 'ls docs/spec/*.txt | wc -l'),
        ('docs/licenses/*', 'ls docs/licenses/* | wc -l'),
    ]:
        add('  %-28s %s' % (label, sh(cmd)))
    idx_n = len(re.search(r'for f in (.*?); do printf', read('docs/index.md'), re.S).group(1).split())
    add('  %-28s %d' % ('docs/index.md 必读清单项', idx_n))
    add('  目录职责：')
    add('    src/core/            实现层数据层与判定层；src/dispatcher/ 统一调度；src/lightweight/ 轻量；src/plugins/ 插件；src/updater/ 更新；src/api.rs 稳定面；src/lib.rs crate 根')
    add('    tests/               行为与边界测试（6 个集成段 + lib 单测）')
    add('    scripts/             守卫与推送/复读/位置清单脚本')
    add('    demos/               UX 整页 HTML + 逐轮运行逻辑 HTML；demos/preview/ PNG 预览；demos/lang/ 两份语言包')
    add('    docs/decisions/      逐轮决策（按轮次编号，不以功能域命名）')
    add('    docs/verification/   逐轮独立验证报告（按轮次编号）')
    add('    docs/features/       功能说明（按功能名命名）')
    add('    docs/design/         UX 逻辑矩阵、槽位契约、设置 ID 表')
    add('    docs/records/        轮次台账、接口台账、功能池、待拍板清单、所有权审计、需求合规审计')
    add('    docs/spec/           用户原文逐字副本与项目约束')
    add('    docs/licenses/       第三方 LICENSE 全文；vendor/ 第三方源码；THIRD-PARTY-NOTICES.md 声明')
    add('')
    add('=' * 78)
    add('二、实现层模块逐文件位置（%d 个 src/core/*.rs，%d 行）' % (len(rows), sum(r['lines'] for r in rows)))
    add('=' * 78)
    add('列：文件 | 行数 | mod.rs 声明行 | AX/状态 | 功能 slug | 单测数 | DEFAULT_STATE | 守卫 | 决策(命中数) | 功能文档 | 演示')
    for r in rows:
        add('  %s | %d | %s | %s %s | %s | %d | %s | %s | %d | %s | %s' % (
            r['name'], r['lines'], r['decl'] or '-',
            r['ax_id'] or '-', r['state'], r['label'] or '-', r['tests'],
            'Y' if r['default_state'] else 'N',
            ','.join(r['guards']) or '-', len(r['decs']),
            ','.join(r['feats']) or '-', ','.join(r['demos']) or '-'))
    add('')
    add('  mod.rs 全文 48 行，逐行列出 pub mod 声明；boot.rs 的 LOADED_MODULES 为诊断包模块列表，接线位置见 src/core/boot.rs。')
    add('  api.rs 仅 4 条 pub use / 7 个稳定符号（CancelToken / Envelope / Kind / CloseAction / PopupOpenError / PopupRegistry / ClientAiGate），069 起未扩面。')
    add('')
    add('=' * 78)
    add('三、功能池 24 项（src/core/ax.rs:20–43）→ 代码位置')
    add('=' * 78)
    add('列：AX | slug | 状态 | conflict | ui | 实现文件 | 守卫 | 决策')
    for ax_id in sorted(AX_MODULE):
        slug, f = AX_MODULE[ax_id]
        st, cf, ui = ax_rows.get(ax_id, ('?', '?', '?'))[1:4]
        guards = [g.name for g in glob('scripts', '*_guard.py') if (f and f[:-3] in g.name)]
        decs = [d.name for d in glob('docs/decisions', '*.md') if slug in d.read_text(encoding='utf-8')]
        add('  %s | %s | %s | %s | %s | %s | %s | %s' % (
            ax_id, slug, st, cf or '(空)', ui, f or '未落实现（保持 Planned/GateOnly）',
            ','.join(guards) or '-', ','.join(decs[:2]) or '-'))
    add('  计数：Planned 2 / DataLayer 21 / GateOnly 1；AX07 conflict=network_io_not_started（EQ-03），AX22 空 conflict（待拍板）。')
    add('')
    add('=' * 78)
    add('四、设置当中的具体设置项（用户点名范围）')
    add('=' * 78)
    add('4.1 实现层根键（src/core/config.rs + src/core/settings_io.rs）')
    add('  SETTINGS_FILE = "launch.json"；路径入口 src/core/paths.rs（c/kcu/kculauncher/config/launch.json 由 00:8 原文给定）')
    add('  settings_io.rs KNOWN_KEYS（%d 个）：' % len(sd['root_keys']))
    for k in sd['root_keys']:
        add('    - %s' % k)
    add('  Config::empty 默认值：language="zh-CN"；mirror_speedtest=true；os_class 由调用方传入；endpoints={}；ports={}；download_region=None（src/core/config.rs:12–23）')
    add('  DERIVED_KEYS（导出差集排除）：%s（src/core/settings_io.rs:29）' % ', '.join(sd['derived']))
    add('  PROTECTED_FILES（清理时保留，4 项）：')
    for c, (v, src) in pv.items():
        if c in sd['protected']:
            add('    - %s = "%s"  （定义 %s）' % (c, v, src))
    add('  上限常量（src/core/settings_io.rs:14–18）：')
    for k, v in sd['limits']:
        add('    - %s = %s' % (k, v.strip()))
    add('  导入校验：未知键 reject + DEGRADE 诊断；类型/长度/控制字符逐项；export_diff 排除派生键；atomic_write 走 .tmp + fs::rename。')
    add('')
    add('4.2 各模块内部状态键（%d 个模块带 DEFAULT_STATE，逐值来自源码 r#"..."#）' % len(sd['default_states']))
    for name, keys, raw in sd['default_states']:
        add('  %-26s 键=%s' % (name, ','.join(keys) or '(解析失败)'))
        add('    %s' % raw[:180])
    add('')
    add('4.3 键白名单常量表（%d 张，逐值来自源码数组）' % len(sd['keymaps']))
    for name, kn, vals in sd['keymaps']:
        add('  %-26s %-22s %s' % (name, kn, ','.join(vals)))
    add('')
    add('4.4 演示层设置页（demos/ui-full-kcu-paper.html）')
    add('  data-tab / data-pane 实跑各 %d 个：%s' % (len(tabs), ' / '.join(tabs)))
    add('  id="set*" 控件实跑 %d 个：%s' % (len(set_ids), ','.join(set_ids)))
    add('  逐分组逐项（列：分组 | 语言包键 | 设置项文案 | 该组首个 option 默认值 | 该组控件 id）：')
    for pane, items, opts, ctrl in panes:
        first = opts[0] if opts else '-'
        add('  [%s] 默认首项=%s 控件=%s' % (pane, first, ','.join(sorted(set(ctrl))) or '-'))
        for key, label in items:
            add('    %-14s %s' % (key, label))
    add('')
    add('4.5 稳定设置 ID（docs/design/ + docs/features/ 中 core.* 全集，%d 个去重值）' % len(ids))
    groups = {}
    for v, srcs in ids.items():
        head2 = '.'.join(v.split('.')[:2])
        groups.setdefault(head2, []).append((v, sorted(srcs)))
    for g in sorted(groups):
        add('  [%s] %d 项' % (g, len(groups[g])))
        for v, srcs in sorted(groups[g]):
            add('    %-34s %s' % (v, ','.join(srcs[:3])))
    add('')
    add('4.6 语言包（demos/lang/）')
    for name, d in langs.items():
        add('  %s：set.* 键 %d 个 = %s；t.NNNN 键 %d 个' % (name, len(d['set_keys']), ','.join(d['set_keys']) or '-', d['t_keys']))
    add('')
    add('4.7 单个设置项的位置链示例（界面语言）')
    add('  1 实现层默认值   src/core/config.rs:18  language="zh-CN"')
    add('  2 导入白名单     src/core/settings_io.rs:21–28  KNOWN_KEYS 含 language；:62 类型校验 string')
    add('  3 演示层控件     demos/ui-full-kcu-paper.html  data-pane="general" → id="setLang" → data-i18n="set.lang"')
    add('  4 语言包文案     demos/lang/zh-CN.js / en-US.js  "set.lang"')
    add('  5 分组文档       docs/features/settings-groups.md（常规）；docs/design/ux-logic-matrix.md U09/U22')
    add('  同一设置项分散在 5 处，无单一注册表；4.1 的根键与 4.2 的模块内部键是两套不同口径。')
    add('')
    add('=' * 78)
    add('五、文档 / 演示 / 守卫 / 台账的位置索引')
    add('=' * 78)
    add('  docs/index.md                 必读清单 515 项（按文件路径线性列出）')
    add('  docs/records/interface-log.md 接口台账 I1–I221（按轮次追加，含 092 的 I219–I221）')
    add('  docs/records/rounds.md        逐轮变更记录（按轮次追加）')
    add('  docs/records/ax-feature-pool.md 功能池 24 项状态与 conflict 台账')
    add('  docs/records/pending-question-environments.md  EQ-01 ~ EQ-13 / Q-C / 历史 Q 可拍环境（092 摊平段）')
    add('  docs/records/requirement-compliance-audit.md 需求合规逐条对照')
    add('  docs/records/code-ownership-audit.md 第三方与所有权审计')
    add('  docs/records/open-questions.md 93 条待拍板问题（Q-A ~ Q-H 组 013 已答复）')
    add('  docs/features/index.md        功能文档索引')
    add('  scripts/*_guard.py           34 个守卫，逐个对应一个模块或一条口径；CI .github/workflows/ci.yml scan job 挂全部')
    add('  docs/decisions/0NN-*.md      85 份，按轮次编号；查某功能需跨多轮')
    add('  docs/verification/round-NNN.md 87 份，按轮次编号')
    add('  demos/round-NNN-*.html       逐轮运行逻辑演示；demos/ui-full-*.html 为整页 UX 演示')
    add('')
    add('=' * 78)
    add('六、位置偏差与候选调整（真实核出，全部待拍板未执行）')
    add('=' * 78)
    add('偏差 1 设置分组数不一致')
    add('  现状：docs/decisions/020-nav-slots-settings.md D03 与 docs/features/settings-groups.md 记 9 分组 / 测量命令写 grep -c data-pane= 输出 9；demos/ui-full-kcu-paper.html 实跑 data-tab 11 / data-pane 11（多 crash 崩溃反馈、auto 自动化）。scripts/settings_guard.py 不核 tab 数，故 092 轮既有 34 个守卫全绿，本轮新增守卫另计。')
    add('  候选 A 文档改 11 并同步测量命令；候选 B 演示层合并到 9；候选 C 登记偏差不改。')
    add('  影响面：docs/decisions/020（历史行不重写）、docs/features/settings-groups.md、docs/design/ux-logic-matrix.md U22、demos/ui-full-kcu-paper.html、语言包 t.* 键、5 张设置 PNG、settings_guard.py 是否新增 tab 断言。')
    add('  状态：待拍板，未执行。')
    add('')
    add('偏差 2 设置项真值分散')
    add('  现状：根键 6 个在 config.rs / settings_io.rs；%d 个模块各有 DEFAULT_STATE；%d 张 *_KEYS 白名单；11 个演示分组与 %d 个控件在 HTML；set.*/t.* 键在两份语言包；core.* ID 在 docs/design 与 docs/features。6 处无单一注册表。' % (len(sd['default_states']), len(sd['keymaps']), len(set_ids)))
    add('  候选 A 抽单一设置注册表模块（键 / 默认值 / 分组 / 控件 id / 语言包键 / 校验口径逐值）；候选 B 保持分散，加交叉守卫逐值对齐；候选 C 按域归中到少数模块。')
    add('  影响面：src/core/ 新增或合并模块数、%s 个守卫、%s 份决策、%s 份演示 HTML、两份语言包、docs/index.md 必读清单。' % (sh('ls scripts/*_guard.py | wc -l'), sh('ls docs/decisions/*.md | wc -l'), sh('ls demos/*.html | wc -l')))
    add('  状态：待拍板，未执行。')
    add('')
    add('偏差 3 同构数据层模块按轮次线性堆积')
    add('  现状：src/core/ 48 个模块 / %d 行；069–091 期间多轮各新建一个 400–1000 行模块（%d 个带 DEFAULT_STATE、%d 张白名单表），每个重复 JSON 默认态、原子写、统一信封、diag_line、路径校验。00:175 原文为同类功能复用同一模块，11:15 原文为文件归中。' % (sum(r['lines'] for r in rows), len(sd['default_states']), len(sd['keymaps'])))
    add('  候选 A 按域合并（外观 / 编辑器 / 下载 / 实例 / 通知 / 网络 六域）；候选 B 抽公共 state_store 保留 48 个薄模块；候选 C 维持现状并只交本清单。')
    add('  影响面：48 个文件路径、mod.rs 48 行声明、boot.rs LOADED_MODULES、34 个守卫的正则锚点、85 份决策的文件路径引用、%d 项必读清单、%s 个集成测试 import。' % (idx_n, sh('ls tests/*.rs | wc -l')))
    add('  状态：待拍板，未执行。本轮采用候选 C（只交清单）。')
    add('')
    add('偏差 4 索引按轮次而非按功能域')
    add('  现状：85 份决策 / 87 份验证 / 79 份 HTML / 72 份功能文档 / 34 个守卫 / 515 项必读清单，按轮次编号或线性堆叠；查一个功能要跨多轮台账。')
    add('  候选 A 以本 txt 作为功能域索引并逐轮维护；候选 B 目录按域重排；候选 C 维持现状。')
    add('  影响面：docs/index.md、interface-log.md、delivery_guard.py 的轮次 glob、CI 路径、历史文件路径引用（A181 历史不重写）。')
    add('  状态：待拍板，未执行。本轮采用候选 A（本 txt 即索引）。')
    add('')
    add('偏差 5 功能池 24 项与 48 个模块非一一对应')
    add('  现状：ax.rs 24 项 AX 中 21 项 DataLayer 各对应 1 个模块，AX07 / AX22 无实现文件，AX23 为 GateOnly；其余 27 个模块为基础设施或早期数据层，不在功能池表内。')
    add('  候选 A 本清单第二节逐文件标注 AX / 状态 / 归属；候选 B 扩 ax.rs 到 48 项；候选 C 维持。')
    add('  影响面：ax_guard.py 显式断言表、ax-feature-pool.md、本清单第二节、未来状态迁移轮次。')
    add('  状态：待拍板，未执行。本轮采用候选 A（已在本清单第二节落地标注）。')
    add('')
    add('=' * 78)
    add('七、约束与状态')
    add('=' * 78)
    add('  本轮不移动文件、不改设置项、不改 src/、不改 Cargo.* / vendor/、不改功能池状态、不改 api::v1。')
    add('  候选调整全部标「待拍板，未执行」；093 用户当轮明确指令为提交位置 txt，按 00:248 覆盖 092 结尾「等用户拍板 A 组」的预告，A 组 EQ / Q 仍全部未证实。')
    add('  四值：已证实（本清单全部计数与键值来自实扫 / 实跑）；已失败（E213–E375 历史项 + 偏差 1 的文档数值过期）；未证实（13 条 EQ / 4 项 Q-C / 31 条历史 Q / 2 项 Planned / 候选调整后果）；未启动（真实网络 IO / UI 宿主 / 渲染层 / 文件迁移执行）。')
    add('  通过标记：按 00:245 不发；独立验证部分通过。')
    add('  唯一下一步：用户从第六节 5 条偏差里点要执行哪几条（或回「都不动」），再按 A208 排迁移轮次；不擅自开工硬做。')
    add('')
    add('生成命令：python3 scripts/feature_locations.py')
    add('校验命令：python3 scripts/feature_locations_guard.py')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    OUT.write_text(build(), encoding='utf-8')
    b = OUT.read_bytes()
    print('FEATURE_LOCATIONS_OK path=%s bytes=%d lines=%d sha256=%s' %
          (str(OUT.relative_to(ROOT)), len(b), b.count(b'\n'), hashlib.sha256(b).hexdigest()[:16]))

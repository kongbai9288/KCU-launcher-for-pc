#!/usr/bin/env python3
"""090：AX20 投影预览两格式槽位、顺序单条决策；零真实解析、不扩 v1。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(reason):
    print('PROJECTION_GUARD_FAIL reason=' + reason)
    sys.exit(1)


f = ROOT / 'src/core/projection.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]

# A258 / A220 / A117：禁用字面量分部件拼接
HTTP = 'ht' + 'tp://'
HTTPS = 'ht' + 'tps://'
LOOPBACK = '127' + '.0.0.1'
TOKEN = 'To' + 'ken'
for banned in ['TcpListener', 'TcpStream', 'bind(', LOOPBACK, '/mcp', TOKEN,
               'SystemTime', 'UNIX_EPOCH', 'std::process::Command', HTTP, HTTPS,
               'reqwest', 'remove_dir_all', 'fs::remove_file', 'x-api-key',
               'ZipArchive', 'zip::', 'flate2', 'tar::', 'litematica',
               'schematica', '.litematic', '.schem', 'nbt', 'vianbt',
               'minecraft:', 'give ', '\u00a7', '.jar']:
    if banned in prod:
        fail('forbidden_literal ' + repr(banned))
for banned in ['EDITOR_TABLE', 'FIELD_TABLE', 'LICENSE_TABLE', 'STEP_CATALOG',
               'url', 'uuid', 'texture', 'AIProvider', 'WikiEntries']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')

# A270：五张常量表用显式 EXPECTED 集合逐值比对
EXPECTED = {
    'ROOT_KEYS': {'schema', 'current', 'entries'},
    'ENTRY_KEYS': {'id', 'format', 'path', 'view', 'scale', 'state', 'decided'},
    'FORMATS': {'primary', 'secondary'},
    'VIEWS': {'fit', 'original', 'scaled'},
    'STATES': {'pending', 'previewed', 'closed'},
}
parsed = {}
for name, expected in EXPECTED.items():
    m = re.search(r'pub const ' + name + r':\s*&\[&str\]\s*=\s*&\[(.*?)\];', prod, re.S)
    if not m:
        fail(name + '_parse_failed')
    ks = re.findall(r'"([a-z_]+)"', m.group(1))
    if len(ks) != len(expected) or set(ks) != expected:
        fail(name + '_values=' + str(ks))
    parsed[name] = set(ks)

m = re.search(r'pub const PATH_KINDS:\s*&\[\(&str,\s*&str\)\]\s*=\s*&\[(.*?)\];', prod, re.S)
if not m:
    fail('PATH_KINDS_parse_failed')
pairs = re.findall(r'\("([a-z]+)",\s*"([a-z_]+)"\)', m.group(1))
PATH_EXPECTED = [('primary', 'primary'), ('secondary', 'secondary')]
if pairs != PATH_EXPECTED:
    fail('PATH_KINDS_values=' + str(pairs))
if any(code not in parsed['FORMATS'] for _, code in pairs):
    fail('PATH_KINDS_code_not_in_table')
if set(p for p, _ in pairs) != parsed['FORMATS']:
    fail('two_format_slots_not_both_registered')

if 'obj.keys().any(|k| !ROOT_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_root_key_not_rejected')
if 'io.keys().any(|k| !ENTRY_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_entry_key_not_rejected')
if 'current > arr.len()' not in prod:
    fail('current_out_of_range_not_rejected')

# A247：显式复用既有上限、路径模块与读取降级
for lit in ['use crate::core::robust;',
            'use crate::core::diagnostics::diag_line;',
            'use crate::core::envelope::{Envelope, Kind};']:
    if lit not in prod:
        fail('import_missing ' + lit)
for bound in ['robust::MAX_TEXT_BYTES', 'robust::MAX_PATH_BYTES',
              'robust::MAX_ID_BYTES', 'robust::MAX_REL_DEPTH']:
    if bound not in prod:
        fail('bound_not_reused ' + bound)
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'robust::read_or_default(&path, DEFAULT_STATE)' not in prod:
    fail('read_or_default_not_reused')

# A255：显式元素类型
for decl in ['let mut lines: Vec<String> = Vec::new();',
             'let mut parts: Vec<String> = Vec::new();',
             'let mut items: Vec<PreviewEntry> = Vec::new();',
             'let mut out: Vec<&str> = Vec::new();',
             'let entries: Vec<Value> = p.entries.iter()']:
    if decl not in prod:
        fail('explicit_vec_type_missing ' + repr(decl))

# A269：三个 impl 段里 code()/parse() 字面量与各自常量表逐值一致
for enum_name, table in [('ProjectionFormat', 'FORMATS'), ('ViewMode', 'VIEWS'),
                         ('PreviewState', 'STATES')]:
    m = re.search(r'impl ' + enum_name + r' \{(.*?)\n\}', prod, re.S)
    if not m:
        fail(enum_name + '_impl_parse_failed')
    impl = m.group(1)
    code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
    parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
    if code_vals != parsed[table] or parse_vals != parsed[table]:
        fail(enum_name + '_literals_mismatch code=%s parse=%s expected=%s'
             % (sorted(code_vals), sorted(parse_vals), sorted(parsed[table])))
    if 'pub fn parse(' not in impl:
        fail(enum_name + '_parse_missing')
for fn in ['ProjectionFormat::parse', 'ViewMode::parse', 'PreviewState::parse']:
    if fn not in prod:
        fail('enum_parse_not_explicit ' + fn)
for bound in ['and_then(ProjectionFormat::parse)', 'and_then(ViewMode::parse)',
              'and_then(PreviewState::parse)']:
    if bound not in prod:
        fail('parse_entry_missing ' + bound)

# A263：从 find(marker) 起逐行扫描到匹配缩进的 } 行
def body_after(marker, closer):
    start = prod.find(marker)
    if start < 0:
        return None
    lines = prod[start:].splitlines()
    out = [lines[0]]
    for ln in lines[1:]:
        out.append(ln)
        if ln == closer:
            break
    return '\n'.join(out)

# A50 / A165：路径校验用标准库 Component 逐分量，不做字符串清洗
vp = body_after('fn validate_entry_path(', '}')
if not vp or not vp.rstrip().endswith('}'):
    fail('validate_entry_path_body_parse_failed')
for lit in ['Component::Normal(part)',
            'Component::CurDir | Component::ParentDir | Component::RootDir | Component::Prefix(_)',
            'Path::new(s).components()',
            'robust::MAX_REL_DEPTH',
            'parts.is_empty()',
            'PATH_KINDS.iter().any(']:
    if lit not in vp:
        fail('component_check_missing ' + lit)
for banned in ['replace(', 'strip_prefix(', 'contains("..")', 'split("..")',
               'fs::', 'std::fs', '.unwrap()', '.expect(', 'unwrap_or']:
    if banned in vp:
        fail('path_cleaning_or_write_present ' + repr(banned))
if prod.count('validate_entry_path(path)') < 2:
    fail('validate_entry_path_not_called count=%d' % prod.count('validate_entry_path(path)'))
if '.and_then(validate_entry_path)' not in prod:
    fail('parse_path_validation_missing')

# classify_path 走显式表
cp = body_after('fn classify_path(', '}')
if not cp or not cp.rstrip().endswith('}'):
    fail('classify_path_body_parse_failed')
for lit in ['ProjectionFormat::parse(code)', 'path.split']:
    if lit not in cp:
        fail('classify_literal_missing ' + lit)
if not re.search(r'for \(prefix, code\) in PATH_KINDS \{', cp):
    fail('classify_table_literal_missing')

# E322 同形态：entry_consistent 函数体逐项核五条字面量
ic = body_after('fn entry_consistent(', '}')
if not ic or not ic.rstrip().endswith('}'):
    fail('entry_consistent_body_parse_failed')
for check in ['i.state == PreviewState::Closed && !i.decided',
              'i.decided && i.state == PreviewState::Pending',
              'i.view == ViewMode::Scaled && (i.scale < MIN_SCALE || i.scale > MAX_SCALE)',
              'i.view != ViewMode::Scaled && i.scale != DEFAULT_SCALE',
              'i.format != classify_path(&i.path)']:
    if not re.search(re.escape(check) + r'(?!\w)', ic):
        fail('entry_consistent_check_missing ' + check)
calls = prod.count('entry_consistent(&')
if calls != 9:
    fail('entry_consistent_calls=%d expected=9' % calls)

# A260：纯查询段不读文件、不写文件
for fn in ['pub fn page_count(', 'pub fn pending_count(', 'pub fn previewed_count(',
           'pub fn closed_count(', 'pub fn current_entry(', 'pub fn by_format(',
           'pub fn by_view(', 'pub fn summary(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('    }'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + '_writes_user_files')

# 坏输入标签（A361：边界用 (?!\w)，不用 \b）
for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'bad_current', 'entries_not_array', 'entries_too_many',
          'current_out_of_range', 'entry_not_object', 'entry_unknown_key',
          'id_too_large', 'bad_id', 'duplicate_id', 'path_escapes_root',
          'bad_format', 'bad_view', 'bad_scale', 'bad_state', 'bad_decided',
          'bad_entry_state', 'in_memory', 'path_rejected',
          'missing_or_unreadable', 'too_large', 'no_root']:
    if not re.search(r'\b' + re.escape(c) + r'(?!\w)', prod):
        fail('bad_input_missing ' + c)
for const in ['MAX_FILE_BYTES', 'MAX_ENTRIES', 'MIN_SCALE', 'MAX_SCALE',
              'DEFAULT_SCALE', 'DEFAULT_STATE', 'EVENT_TARGET',
              'PROJECTION_FILE', 'TMP_SUFFIX']:
    if not re.search(r'\b' + re.escape(const) + r'\b', prod):
        fail('bound_missing ' + const)

# 11:250 / 11:244 顺序单条决策，无批量
for fn in ['pub fn add_entry(', 'pub fn append_entry(', 'pub fn resolve_current(',
           'pub fn set_format(', 'pub fn set_view(', 'pub fn set_scale(',
           'pub fn set_state(', 'pub fn set_decided(', 'pub fn set_path(',
           'pub fn remove_entry(']:
    if fn not in prod:
        fail('single_mutation_missing ' + fn)
for banned in ['mark_all', 'accept_all', 'resolve_all', 'confirm_all', 'preview_all']:
    if banned in prod:
        fail('batch_mutation_present ' + banned)
if 'if self.pending_count() == 0 {' not in prod:
    fail('append_entry_pending_guard_missing')
if 'self.current += 1;' not in prod:
    fail('single_page_advance_missing')
if 'if state == PreviewState::Pending || self.current >= self.entries.len() {' not in prod:
    fail('resolve_current_bound_missing')

# 原子写与统一信封
for lit in ['fs::write(&tmp, body)?;', 'fs::rename(&tmp, &path)?;',
            'Envelope::new(Kind::Event, EVENT_TARGET)']:
    if lit not in prod:
        fail('atomic_write_or_envelope_missing ' + lit)
ce = body_after('pub fn change_event(', '    }')
if not ce or not ce.rstrip().endswith('    }'):
    fail('change_event_body_parse_failed')
payload_keys = re.findall(r'\.with\("([a-z_]+)",', ce)
PAYLOAD_EXPECTED = {'pages', 'current', 'pending', 'previewed', 'closed',
                    'primary', 'secondary', 'formats', 'views', 'states'}
if len(payload_keys) != 10 or set(payload_keys) != PAYLOAD_EXPECTED:
    fail('event_payload_keys=' + str(payload_keys))
for banned in ['.path', '.id', 'format!("{}", i.']:
    if banned in ce:
        fail('user_text_in_event_payload ' + repr(banned))

# A246：稳定面不扩
api = (ROOT / 'src/api.rs').read_text()
lines = [l.strip() for l in api.splitlines() if l.strip().startswith('pub use crate::')]
syms = set()
for l in lines:
    tail = l.split('::')[-1].rstrip(';').strip()
    if tail.startswith('{') and tail.endswith('}'):
        syms.update(x.strip() for x in tail[1:-1].split(','))
    else:
        syms.add(tail)
WHITELIST = {'CancelToken', 'Envelope', 'Kind', 'CloseAction',
             'PopupOpenError', 'PopupRegistry', 'ClientAiGate'}
if syms != WHITELIST:
    fail('v1_surface_changed got=' + ','.join(sorted(syms)))

# A234 / A256：模块登记与诊断包列表
mod = (ROOT / 'src/core/mod.rs').read_text()
if 'pub mod projection;' not in mod:
    fail('module_declaration_missing')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.projection",' not in boot:
    fail('boot_module_missing')
if boot.index('"core.projection",') > boot.index('"dispatcher.launcher",'):
    fail('boot_module_after_dispatcher')
ci = (ROOT / '.github/workflows/ci.yml').read_text()
if not re.search(r'^\s*- name: projection_guard\s*$', ci, re.M) or \
        'python3 scripts/projection_guard.py' not in ci:
    fail('ci_step_missing')

# A267 / A240 / A262：AX20 真实 slug 与状态，计数由 ax_guard 动态持有
ax = (ROOT / 'src/core/ax.rs').read_text()
ax_row = re.search(r'AxSpec \{ id: "AX20", name: "([a-z_]+)", state: AxState::(\w+), conflict: "([^"]*)"', ax)
if not ax_row:
    fail('ax20_row_missing')
if ax_row.group(1) != 'projection_workshop' or ax_row.group(2) != 'DataLayer' or ax_row.group(3) != '':
    fail('ax20_state_mismatch name=%s state=%s conflict=%s' % ax_row.groups())
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX20'" not in axg:
    fail('ax_guard_explicit_assert_missing')
if 'planned = sum(' not in axg or 'data = sum(' not in axg:
    fail('ax_guard_not_dynamic')
# A230：AX07 硬技术冲突保持，AX15 / AX22 仍 Planned，不擅自升级
for ax_id, state, conflict in [('AX07', 'Planned', 'network_io_not_started'),
                               ('AX15', 'Planned', ''),
                               ('AX22', 'Planned', '')]:
    row = re.search(r'AxSpec \{ id: "' + ax_id + r'", name: "([a-z_]+)", state: AxState::(\w+), conflict: "([^"]*)"', ax)
    if not row or row.group(2) != state or row.group(3) != conflict:
        fail('a230_conflict_not_recorded ' + ax_id)

# A100：UI 渲染层不落投影文件名
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'projection-preview.json' in p.read_text():
        fail('ui_surface ' + rel)

print('PROJECTION_GUARD_OK root_keys=3 entry_keys=7 formats=2 views=3 states=3 '
      'path_kinds=2 three_impl_literals_match component_path_check '
      'consistent_checks_five calls=%d pure_queries event_payload=%d '
      'v1_unchanged ax20=DataLayer a230_conflicts_recorded'
      % (calls, len(payload_keys)))

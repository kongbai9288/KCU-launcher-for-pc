#!/usr/bin/env python3
"""088：AX08 导入条目路径校验、格式与动作表、顺序单条决策；零真实解压、不扩 v1。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(reason):
    print('INSTANCE_IMPORT_GUARD_FAIL reason=' + reason)
    sys.exit(1)


f = ROOT / 'src/core/instance_import.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]

# A258 / A220 / A117：禁用字面量分部件拼接，保留运行时值，去掉连续串
HTTP = 'ht' + 'tp://'
HTTPS = 'ht' + 'tps://'
LOOPBACK = '127' + '.0.0.1'
TOKEN = 'To' + 'ken'
for banned in ['TcpListener', 'TcpStream', 'bind(', LOOPBACK, '/mcp', TOKEN,
               'SystemTime', 'UNIX_EPOCH', 'std::process::Command', HTTP, HTTPS,
               'reqwest', 'remove_dir_all', 'fs::remove_file', 'x-api-key',
               'ZipArchive', 'zip::', 'flate2', 'tar::']:
    if banned in prod:
        fail('forbidden_literal ' + repr(banned))
for banned in ['EDITOR_TABLE', 'FIELD_TABLE', 'LICENSE_TABLE', 'STEP_CATALOG',
               'url', 'uuid', 'texture', 'minecraft:', 'give ', '\u00a7', '.jar']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')

# A270：六张常量表用显式 EXPECTED 集合逐值比对
EXPECTED = {
    'ROOT_KEYS': {'schema', 'format', 'current', 'entries'},
    'ENTRY_KEYS': {'id', 'path', 'kind', 'action', 'state', 'bytes'},
    'FORMATS': {'mrpack', 'curseforge_zip', 'portable_instance', 'instance_template'},
    'KINDS': {'mod', 'plugin', 'config', 'world', 'other'},
    'ACTIONS': {'create', 'clone', 'overwrite_confirm', 'skip', 'auto_rename'},
    'STATES': {'pending', 'accepted', 'rejected'},
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
PATH_EXPECTED = [('mods', 'mod'), ('plugins', 'plugin'), ('config', 'config'), ('saves', 'world')]
if pairs != PATH_EXPECTED:
    fail('PATH_KINDS_values=' + str(pairs))
if any(kind not in parsed['KINDS'] for _, kind in pairs):
    fail('PATH_KINDS_kind_not_in_table')

if 'obj.keys().any(|k| !ROOT_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_root_key_not_rejected')
if 'io.keys().any(|k| !ENTRY_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_entry_key_not_rejected')
if 'current > arr.len()' not in prod:
    fail('current_out_of_range_not_rejected')

# A247：显式复用既有文本上限、路径模块与读取降级
if 'use crate::core::robust;' not in prod:
    fail('robust_import_missing')
if 'use crate::core::diagnostics::diag_line;' not in prod:
    fail('diag_line_import_missing')
if 'use crate::core::envelope::{Envelope, Kind};' not in prod:
    fail('envelope_import_missing')
if prod.count('robust::MAX_TEXT_BYTES') < 1 or prod.count('robust::MAX_PATH_BYTES') < 1:
    fail('text_bound_not_reused')
if prod.count('robust::MAX_ID_BYTES') < 1 or prod.count('robust::MAX_REL_DEPTH') < 1:
    fail('path_bound_not_reused')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'robust::read_or_default(&path, DEFAULT_STATE)' not in prod:
    fail('read_or_default_not_reused')

# A255：显式元素类型
for decl in ['let mut lines: Vec<String> = Vec::new();',
             'let mut parts: Vec<String> = Vec::new();',
             'let mut items: Vec<ImportEntry> = Vec::new();',
             'let entries: Vec<Value> = p.entries.iter()']:
    if decl not in prod:
        fail('explicit_vec_type_missing ' + repr(decl))

# A269：四个 impl 段里 code()/parse() 的字面量与各自常量表逐值一致
for enum_name, table in [('ImportFormat', 'FORMATS'), ('EntryKind', 'KINDS'),
                         ('ImportAction', 'ACTIONS'), ('EntryState', 'STATES')]:
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
for fn in ['ImportFormat::parse', 'EntryKind::parse',
           'ImportAction::parse', 'EntryState::parse']:
    if fn not in prod:
        fail('enum_parse_not_explicit ' + fn)
for bound in ['and_then(ImportFormat::parse)', 'and_then(EntryKind::parse)',
              'and_then(ImportAction::parse)', 'and_then(EntryState::parse)']:
    if bound not in prod:
        fail('parse_entry_missing ' + bound)

# A263：从 find(marker) 起逐行扫描到匹配缩进的 } 行，不用跨行非贪婪正则
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
            'parts.is_empty()']:
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

# classify_path 走显式表，不写硬编码分支
cp = body_after('fn classify_path(', '}')
if not cp or not cp.rstrip().endswith('}'):
    fail('classify_path_body_parse_failed')
for lit in ['for (prefix, code) in PATH_KINDS {', 'EntryKind::parse(code)', 'path.split']:
    if lit not in cp:
        fail('classify_literal_missing ' + lit)

# E322 同形态：entry_consistent 函数体逐项核五条字面量
ic = body_after('fn entry_consistent(', '}')
if not ic or not ic.rstrip().endswith('}'):
    fail('entry_consistent_body_parse_failed')
for check in ['i.state == EntryState::Accepted && i.action == ImportAction::Skip',
              'i.state == EntryState::Pending && i.action == ImportAction::Skip',
              'i.kind != classify_path(&i.path)',
              'i.bytes > MAX_ENTRY_BYTES',
              'i.action == ImportAction::Clone && i.kind == EntryKind::World']:
    if not re.search(re.escape(check) + r'(?!\w)', ic):
        fail('entry_consistent_check_missing ' + check)
calls = prod.count('entry_consistent(&')
if calls != 6:
    fail('entry_consistent_calls=%d expected=6' % calls)

# A260：纯查询段不读文件、不写文件
for fn in ['pub fn page_count(', 'pub fn pending_count(', 'pub fn accepted_count(',
           'pub fn rejected_count(', 'pub fn current_entry(', 'pub fn by_kind(',
           'pub fn by_action(', 'pub fn summary(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('    }'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + '_writes_user_files')

# 坏输入标签
for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'bad_format', 'entries_not_array', 'entries_too_many', 'bad_current',
          'current_out_of_range', 'entry_not_object', 'entry_unknown_key',
          'id_too_large', 'bad_id', 'duplicate_id', 'path_escapes_root',
          'bad_kind', 'bad_action', 'bad_state', 'bad_bytes',
          'kind_path_mismatch', 'bad_entry_state', 'in_memory',
          'path_rejected', 'missing_or_unreadable', 'too_large', 'no_root']:
    if not re.search(r'\b' + re.escape(c) + r'(?!\w)', prod):
        fail('bad_input_missing ' + c)
for const in ['MAX_FILE_BYTES', 'MAX_ENTRIES', 'MAX_ENTRY_BYTES',
              'DEFAULT_STATE', 'EVENT_TARGET', 'INSTANCE_IMPORT_FILE', 'TMP_SUFFIX']:
    if const not in prod:
        fail('bound_missing ' + const)

# 11:222 / 12:40 / 12:41 顺序单条决策，无批量
for fn in ['pub fn add_entry(', 'pub fn append_entry(', 'pub fn resolve_current(',
           'pub fn set_action(', 'pub fn set_state(', 'pub fn set_path(',
           'pub fn set_format(', 'pub fn remove_entry(']:
    if fn not in prod:
        fail('single_mutation_missing ' + fn)
for banned in ['mark_all', 'accept_all', 'resolve_all', 'confirm_all']:
    if banned in prod:
        fail('batch_mutation_present ' + banned)
if 'if self.pending_count() == 0 {' not in prod:
    fail('append_entry_pending_guard_missing')
if 'self.current += 1;' not in prod:
    fail('single_page_advance_missing')
if 'if state == EntryState::Pending || self.current >= self.entries.len() {' not in prod:
    fail('resolve_current_bound_missing')

# 原子写与统一信封
for lit in ['fs::write(&tmp, body)?;', 'fs::rename(&tmp, &path)?;',
            'Envelope::new(Kind::Event, EVENT_TARGET)']:
    if lit not in prod:
        fail('atomic_write_or_envelope_missing ' + lit)
ce = body_after('pub fn change_event(', '    }')
if not ce or not ce.rstrip().endswith('    }'):
    fail('change_event_body_parse_failed')
payload_count = ce.count('.with("')
if payload_count != 10:
    fail('event_payload_count=%d expected=10' % payload_count)
payload_keys = re.findall(r'\.with\("([a-z_]+)",', ce)
PAYLOAD_EXPECTED = {'pages', 'current', 'pending', 'accepted', 'rejected',
                    'create', 'clone', 'skip', 'formats', 'kinds'}
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
if 'pub mod instance_import;' not in mod:
    fail('module_declaration_missing')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.instance_import",' not in boot:
    fail('boot_module_missing')
if boot.index('"core.instance_import",') > boot.index('"dispatcher.launcher",'):
    fail('boot_module_after_dispatcher')
ci = (ROOT / '.github/workflows/ci.yml').read_text()
if not re.search(r'^\s*- name: instance_import_guard\s*$', ci, re.M) or \
        'python3 scripts/instance_import_guard.py' not in ci:
    fail('ci_step_missing')

# A267 / A240：AX08 真实 slug 与状态由本守卫独立核一次，不写死上一轮计数
ax = (ROOT / 'src/core/ax.rs').read_text()
ax_row = re.search(r'AxSpec \{ id: "AX08", name: "([a-z_]+)", state: AxState::(\w+), conflict: "([^"]*)"', ax)
if not ax_row:
    fail('ax08_row_missing')
if ax_row.group(1) != 'instance_import' or ax_row.group(2) != 'DataLayer' or ax_row.group(3) != '':
    fail('ax08_state_mismatch name=%s state=%s conflict=%s' % ax_row.groups())
ax_rows = [r for r in re.findall(r'AxSpec \{([^}]*)\}', ax) if 'id: "AX' in r]
ax_states = [re.search(r'state: AxState::(\w+)', r).group(1) for r in ax_rows]
ax_planned = ax_states.count('Planned')
ax_data = ax_states.count('DataLayer')
# A240 / A262 / E366：状态计数由 ax_guard 动态持有，本守卫只核行数与关键项断言
if len(ax_rows) != 24 or ax_states.count('GateOnly') != 1:
    fail('ax_table_shape rows=%d gate=%d' % (len(ax_rows), ax_states.count('GateOnly')))
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX08'" not in axg:
    fail('ax_guard_explicit_assert_missing AX08')
if 'planned = sum(' not in axg or 'data = sum(' not in axg:
    fail('ax_guard_not_dynamic')

print('INSTANCE_IMPORT_GUARD_OK root_keys=%d entry_keys=%d formats=%d kinds=%d actions=%d states=%d '
      'path_kinds=%d four_impl_literals_match component_path_check consistent_checks_five calls=%d '
      'pure_queries event_payload=%d v1_unchanged ax08=DataLayer planned=%d data=%d'
      % (len(parsed['ROOT_KEYS']), len(parsed['ENTRY_KEYS']), len(parsed['FORMATS']),
         len(parsed['KINDS']), len(parsed['ACTIONS']), len(parsed['STATES']),
         len(pairs), calls, payload_count, ax_planned, ax_data))

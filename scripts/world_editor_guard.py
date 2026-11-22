#!/usr/bin/env python3
"""082：AX03 存档编辑会话与开源组件许可证状态索引；零内容持有、不扩 v1。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('WORLD_EDITOR_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/world_editor.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

# A258 / A117 / 11:19：运行时值保留，字面量分部件拼接
HTTP = 'ht' + 'tp://'
HTTPS = 'ht' + 'tps://'
LOOPBACK = '127' + '.0.0.1'
TOKEN = 'To' + 'ken'
for banned in ['TcpListener', 'TcpStream', 'bind(', LOOPBACK, '/mcp', TOKEN,
               'SystemTime', 'UNIX_EPOCH', 'std::process::Command', HTTP, HTTPS,
               'reqwest', 'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['EDITOR_TABLE', 'FIELD_TABLE', 'LICENSE_TABLE', 'STEP_CATALOG',
               'cmp_precedence', 'semver', 'Version::parse', 'url', 'token', 'uuid',
               'texture', 'png', 'minecraft:', 'give ', 'regex', 'glob',
               'AIProvider', 'WikiEntries', '\u00a7']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 2:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
for decl in ['let mut lines: Vec<String> = Vec::new();',
             'let mut entries: Vec<EditorEntry> = Vec::new();',
             'let mut out: Vec<&str> = Vec::new();']:
    if decl not in prod:
        fail('explicit_vec_type_missing ' + decl)

# A270：七张常量表用显式 EXPECTED 集合逐值比对
EXPECTED = {
    'KNOWN_KEYS': {'schema', 'session', 'entries'},
    'ENTRY_KEYS': {'id', 'field', 'format', 'source', 'license', 'link_mode', 'verified', 'diff_checked', 'state'},
    'FIELDS': {'seed', 'world_type', 'chunks', 'dimension'},
    'FORMATS': {'int', 'bool', 'opaque'},
    'SOURCES': {'builtin', 'open_source'},
    'LINK_MODES': {'same_license', 'dynamic_link', 'separate_process'},
    'STATES': {'draft', 'verified', 'applied'},
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
if 'obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_root_key_not_rejected')
if 'eo.keys().any(|k| !ENTRY_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_entry_key_not_rejected')

# VERIFIED_LICENSE 单值
m = re.search(r'pub const VERIFIED_LICENSE:\s*&str\s*=\s*"([A-Za-z0-9\.\-]+)";', prod)
if not m or m.group(1) != 'MIT':
    fail('verified_license_value=' + (m.group(1) if m else 'missing'))

# A247：显式复用既有文本上限常量，删 import 行要真 FAIL
if 'use crate::core::robust;' not in prod:
    fail('robust_import_missing')
if prod.count('robust::MAX_TEXT_BYTES') < 2:
    fail('text_bound_not_reused count=%d' % prod.count('robust::MAX_TEXT_BYTES'))
if 'robust::read_or_default(&path, DEFAULT_STATE)' not in prod:
    fail('read_or_default_not_reused')

# A269：五个 impl 段里 code()/parse() 的字面量与各自常量表逐值一致
for enum_name, table in [('EditField', 'FIELDS'), ('ValueFormat', 'FORMATS'),
                         ('OssSource', 'SOURCES'), ('LinkMode', 'LINK_MODES'),
                         ('EditorState', 'STATES')]:
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
for fn in ['EditField::parse', 'ValueFormat::parse', 'OssSource::parse',
           'LinkMode::parse', 'EditorState::parse']:
    if fn not in prod:
        fail('enum_parse_not_explicit ' + fn)
for bound in ['FIELDS.contains(&field.code())',
              'FORMATS.contains(&format.code())',
              'SOURCES.contains(&source.code())',
              'LINK_MODES.contains(&link_mode.code())',
              'STATES.contains(&state.code())']:
    if bound not in prod:
        fail('set_bound_missing ' + bound)

# 坏输入标签
for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid', 'bad_session',
          'entries_not_array', 'entries_too_many', 'entry_not_object', 'entry_unknown_key',
          'id_too_large', 'bad_id', 'duplicate_id', 'bad_field', 'bad_format', 'bad_source',
          'license_too_large', 'bad_license', 'bad_link_mode', 'bad_verified',
          'bad_diff_checked', 'bad_state', 'bad_entry_state', 'in_memory',
          'path_rejected', 'missing_or_unreadable', 'too_large', 'no_root']:
    if c not in prod:
        fail('bad_input_missing ' + c)
for const in ['MAX_FILE_BYTES', 'MAX_ENTRIES', 'DEFAULT_STATE', 'EVENT_TARGET', 'VERIFIED_LICENSE']:
    if const not in prod:
        fail('bound_missing ' + const)

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

# 八个纯查询段不读文件
for fn in ['pub fn editable_count(', 'pub fn verified_count(', 'pub fn by_field(',
           'pub fn by_source(', 'pub fn by_link_mode(', 'pub fn license_for(',
           'pub fn applied_count(', 'pub fn summary(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('    }'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

# E322 教训：解析 entry_consistent 函数体逐项核五条字面量，不只核函数名与 DEGRADE 标签
ec = body_after('fn entry_consistent(', '}')
if not ec or not ec.rstrip().endswith('}'):
    fail('entry_consistent_body_parse_failed')
for check in ['OssSource::OpenSource && e.license.is_empty()',
              'e.state == EditorState::Applied && !e.verified',
              'e.state == EditorState::Applied && !e.diff_checked',
              'e.link_mode == LinkMode::SeparateProcess && e.source == OssSource::Builtin',
              '!e.license.is_empty() && e.source == OssSource::Builtin']:
    if check not in ec:
        fail('entry_consistent_check_missing ' + check)
calls = prod.count('entry_consistent(&')
if calls != 8:
    fail('entry_consistent_calls=%d expected=8' % calls)
for marker, expected in [('if !entry_consistent(&e) {', 2),
                         ('if !entry_consistent(&candidate) {', 6)]:
    if prod.count(marker) != expected:
        fail('entry_consistent_call_shape=%s count=%d expected=%d'
             % (marker, prod.count(marker), expected))

# 单条突变入口，无批量
for fn in ['pub fn add_entry(', 'pub fn set_field(', 'pub fn set_source(',
           'pub fn set_link_mode(', 'pub fn set_state(', 'pub fn set_verified(',
           'pub fn set_diff_checked(', 'pub fn remove_entry(']:
    if fn not in prod:
        fail('single_mutation_missing ' + fn)
if 'mark_all' in prod or 'confirm_all' in prod:
    fail('batch_mutation_present')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, EVENT_TARGET)' not in prod:
    fail('event_not_unified_envelope')

# E330 教训：解析 change_event 函数体核不进用户文本与载荷数
ev = body_after('pub fn change_event(', '    }')
if not ev or not ev.rstrip().endswith('    }'):
    fail('change_event_body_parse_failed')
for key in ['"id"', '"license"', '"title"', '"body"']:
    if '.with(%s,' % key in ev:
        fail('user_text_in_event_payload ' + key)
if ev.count('.with(') != 10:
    fail('event_payload_count=%d expected=10' % ev.count('.with('))
for key in ['id', 'license', 'title', 'body']:
    if 'e.field("%s"), None' % key not in tests:
        fail('user_text_assertion_missing ' + key)
if 'assert_eq!(e.payload.len(), 10);' not in tests:
    fail('event_payload_count_missing')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
for key in ['"schema": 1, "session": p.session.code(), "entries": items',
            '"id": e.id', '"field": e.field.code()', '"format": e.format.code()',
            '"source": e.source.code()', '"license": e.license',
            '"link_mode": e.link_mode.code()', '"verified": e.verified',
            '"diff_checked": e.diff_checked', '"state": e.state.code()']:
    if key not in prod:
        fail('serialize_key_missing ' + key)

api = (ROOT / 'src/api.rs').read_text()
if 'world_editor' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX03", name: "world_editor", state: AxState::(\w+), conflict: "([a-z_]*)"', ax)
if not m or m.group(1) != 'DataLayer' or m.group(2) != '':
    fail('ax03_state_or_conflict_changed')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX03'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.world_editor"' not in boot:
    fail('module_not_in_boot_diagnostics')
ci = (ROOT / '.github/workflows/ci.yml').read_text()
if 'name: world_editor_guard' not in ci:
    fail('ci_step_missing')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'world-editor.json' in p.read_text():
        fail('ui_surface ' + rel)

print('WORLD_EDITOR_GUARD_OK root_keys=3 entry_keys=9 fields=4 formats=3 '
      'sources=2 links=3 states=3 verified_license=MIT expected_tables '
      'five_impl_literals_match robust_reused consistent_checks_five calls=8 '
      'pure_queries event_payload=10 v1_unchanged ax03=DataLayer conflict_empty')

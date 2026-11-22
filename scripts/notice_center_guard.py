#!/usr/bin/env python3
"""081：AX02 公告中心状态索引；零内容持有、内置条目不可删、不扩 v1。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('NOTICE_CENTER_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/notice_center.rs'
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
for banned in ['NOTICE_TABLE', 'CATEGORY_TABLE', 'ACTION_TABLE', 'STEP_CATALOG',
               'cmp_precedence', 'semver', 'Version::parse', 'url', 'token', 'uuid',
               'texture', 'png', 'minecraft:', 'give ', 'regex', 'glob',
               'AIProvider', 'WikiEntries', '\u00a7']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 2:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'let mut lines: Vec<String> = Vec::new();' not in prod:
    fail('explicit_vec_type_missing')
if 'let mut entries: Vec<NoticeEntry> = Vec::new();' not in prod:
    fail('explicit_entry_vec_type_missing')
if 'let mut out: Vec<&str> = Vec::new();' not in prod:
    fail('explicit_str_vec_type_missing')

# A270：六张常量表用显式 EXPECTED 集合逐值比对
EXPECTED = {
    'KNOWN_KEYS': {'schema', 'entries'},
    'ENTRY_KEYS': {'id', 'category', 'read', 'action', 'closable', 'detail', 'builtin'},
    'CATEGORIES': {'update', 'maintenance', 'activity', 'declaration'},
    'READ_STATES': {'unread', 'read'},
    'ACTIONS': {'never', 'later', 'ack'},
    'CLOSE_PATHS': {'button', 'escape', 'cancel'},
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

# BUILTIN_ID 单值 + 内置条目保护
m = re.search(r'pub const BUILTIN_ID:\s*&str\s*=\s*"([a-z_]+)";', prod)
if not m or m.group(1) != 'declaration':
    fail('builtin_id_value=' + (m.group(1) if m else 'missing'))
if 'if self.is_builtin(id) {' not in prod or 'return false;' not in prod.split('pub fn remove_entry(')[1][:120]:
    fail('builtin_remove_not_protected')
if '!entries.iter().any(|e| e.builtin && e.id == BUILTIN_ID)' not in prod:
    fail('missing_builtin_not_rejected')
if 'entries.iter().filter(|e| e.builtin).count() != 1' not in prod:
    fail('duplicate_builtin_not_rejected')

# A247：显式复用既有文本上限常量，删 import 行要真 FAIL
if 'use crate::core::robust;' not in prod:
    fail('robust_import_missing')
if prod.count('robust::MAX_TEXT_BYTES') < 2:
    fail('text_bound_not_reused count=%d' % prod.count('robust::MAX_TEXT_BYTES'))
if 'robust::read_or_default(&path, DEFAULT_STATE)' not in prod:
    fail('read_or_default_not_reused')

# A269：四个 impl 段里 code()/parse() 的字面量与各自常量表逐值一致
for enum_name, table in [('NoticeCategory', 'CATEGORIES'), ('ReadState', 'READ_STATES'),
                         ('NoticeAction', 'ACTIONS'), ('ClosePath', 'CLOSE_PATHS')]:
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
for fn in ['NoticeCategory::parse', 'ReadState::parse', 'NoticeAction::parse']:
    if fn not in prod:
        fail('enum_parse_not_explicit ' + fn)
if 'ClosePath::parse' not in t:
    fail('close_path_parse_not_exercised')

# 坏输入标签
for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'entries_not_array', 'entries_too_many', 'entry_not_object',
          'entry_unknown_key', 'id_too_large', 'bad_id', 'duplicate_id',
          'bad_category', 'bad_read', 'bad_action', 'bad_closable', 'bad_detail',
          'bad_builtin', 'bad_entry_state', 'missing_builtin', 'duplicate_builtin',
          'in_memory', 'path_rejected', 'missing_or_unreadable', 'too_large', 'no_root']:
    if c not in prod:
        fail('bad_input_missing ' + c)
for const in ['MAX_FILE_BYTES', 'MAX_ENTRIES', 'DEFAULT_STATE', 'EVENT_TARGET']:
    if const not in prod:
        fail('bound_missing ' + const)
for bound in ['CATEGORIES.contains(&category.code())',
              'READ_STATES.contains(&read.code())',
              'ACTIONS.contains(&action.code())',
              'CLOSE_PATHS.contains(&path.code())']:
    if bound not in prod:
        fail('set_bound_missing ' + bound)

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
for fn in ['pub fn can_close(', 'pub fn visible_count(', 'pub fn unread_count(',
           'pub fn by_category(', 'pub fn action_for(', 'pub fn is_builtin(',
           'pub fn detail_available(', 'pub fn summary(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('    }'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

# E322 教训：解析 entry_consistent 函数体逐项核三处字面量，不只核函数名与 DEGRADE 标签
ec = body_after('fn entry_consistent(', '}')
if not ec or not ec.rstrip().endswith('}'):
    fail('entry_consistent_body_parse_failed')
for check in ['NoticeAction::Never && e.read == ReadState::Unread',
              '!e.closable && e.action == NoticeAction::Later',
              'e.builtin && e.id != BUILTIN_ID']:
    if check not in ec:
        fail('entry_consistent_check_missing ' + check)
calls = prod.count('entry_consistent(&')
if calls < 5:
    fail('entry_consistent_calls=%d expected>=5' % calls)
for marker in ['if !entry_consistent(&e) {', 'if !entry_consistent(&candidate) {']:
    if marker not in prod:
        fail('entry_consistent_call_missing ' + marker)

# 单条突变入口，无批量
for fn in ['pub fn add_entry(', 'pub fn set_read(', 'pub fn set_action(',
           'pub fn set_closable(', 'pub fn remove_entry(']:
    if fn not in prod:
        fail('single_mutation_missing ' + fn)
if 'mark_all' in prod or 'confirm_all' in prod:
    fail('batch_mutation_present')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, EVENT_TARGET)' not in prod:
    fail('event_not_unified_envelope')
ev = body_after('pub fn change_event(', '    }')
if not ev or not ev.rstrip().endswith('    }'):
    fail('change_event_body_parse_failed')
for key in ['"id"', '"title"', '"body"']:
    if '.with(%s,' % key in ev:
        fail('user_text_in_event_payload ' + key)
if ev.count('.with(') != 10:
    fail('event_payload_count=%d expected=10' % ev.count('.with('))
for key in ['id', 'title', 'body']:
    if 'e.field("%s"), None' % key not in tests:
        fail('user_text_assertion_missing ' + key)
if 'assert_eq!(e.payload.len(), 10);' not in tests:
    fail('event_payload_count_missing')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
for key in ['"schema": 1, "entries": items', '"id": e.id', '"category": e.category.code()',
            '"read": e.read.code()', '"action": e.action.code()', '"closable": e.closable',
            '"detail": e.detail', '"builtin": e.builtin']:
    if key not in prod:
        fail('serialize_key_missing ' + key)

api = (ROOT / 'src/api.rs').read_text()
if 'notice_center' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX02", name: "game_news", state: AxState::(\w+), conflict: "([a-z_]*)"', ax)
if not m or m.group(1) != 'DataLayer' or m.group(2) != '':
    fail('ax02_state_or_conflict_changed')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX02'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.notice_center"' not in boot:
    fail('module_not_in_boot_diagnostics')
ci = (ROOT / '.github/workflows/ci.yml').read_text()
if 'name: notice_center_guard' not in ci:
    fail('ci_step_missing')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'notice-center.json' in p.read_text():
        fail('ui_surface ' + rel)

print('NOTICE_CENTER_GUARD_OK root_keys=2 entry_keys=7 categories=4 reads=2 '
      'actions=3 closes=3 builtin=declaration expected_tables four_impl_literals_match '
      'robust_reused consistent_checks_three calls=%d pure_queries' % calls +
      ' v1_unchanged ax02=DataLayer conflict_empty')

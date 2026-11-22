#!/usr/bin/env python3
"""078：AX18 生成器会话元数据层；不扩 v1；不落生成算法与端点。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('GENERATOR_SESSION_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/generator_session.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'ht' + 'tp://', 'ht' + 'tps://',
               'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['SESSION_TABLE', 'GRADIENT_TABLE', 'AI_TABLE', 'CLIPBOARD_TABLE',
               'GEN_TABLE', 'COLOR_TABLE', 'PATTERN_CODES', 'cmp_precedence',
               'semver', 'Version::parse', 'url', 'Token', 'token', 'uuid',
               'minecraft:', 'give ', 'regex', 'glob', 'AIProvider', 'WikiEntries',
               'StepCatalog', 'dialog']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'let mut lines: Vec<String> = Vec::new();' not in prod:
    fail('explicit_vec_type_missing')

# A270：六张常量表用显式 EXPECTED 集合逐值比对
EXPECTED = {
    'KNOWN_KEYS': {'schema', 'format', 'sessions', 'translations', 'history'},
    'SESSION_KEYS': {'id', 'kind', 'format', 'input', 'result', 'state'},
    'TRANSLATION_KEYS': {'id', 'key', 'value', 'enabled'},
    'KINDS': {'recipe', 'gradient', 'mod_translation'},
    'FORMATS': {'legacy', 'json'},
    'STATES': {'draft', 'ready', 'archived'},
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
    fail('unknown_key_not_rejected')
if 'session_keys_ok(e)' not in prod:
    fail('session_keys_not_rejected')
if 'translation_keys_ok(e)' not in prod:
    fail('translation_keys_not_rejected')

# A247：显式复用既有文本上限常量，删 import 行要真 FAIL
if 'use crate::core::robust;' not in prod:
    fail('robust_import_missing')
if prod.count('robust::MAX_TEXT_BYTES') < 2:
    fail('text_bound_not_reused count=%d' % prod.count('robust::MAX_TEXT_BYTES'))
if 'robust::read_or_default(&path, DEFAULT_STATE)' not in prod:
    fail('read_or_default_not_reused')

# A269：三个 impl 段里 code()/parse() 的字面量与各自常量表逐值一致
for enum_name, table in [('GeneratorKind', 'KINDS'),
                         ('OutputFormat', 'FORMATS'),
                         ('SessionState', 'STATES')]:
    m = re.search(r'impl ' + enum_name + r' \{(.*?)\n\}', prod, re.S)
    if not m:
        fail(enum_name + '_impl_parse_failed')
    impl = m.group(1)
    code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
    parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
    if code_vals != parsed[table] or parse_vals != parsed[table]:
        fail(enum_name + '_literals_mismatch code=%s parse=%s expected=%s'
             % (sorted(code_vals), sorted(parse_vals), sorted(parsed[table])))
for fn in ['GeneratorKind::parse', 'OutputFormat::parse', 'SessionState::parse']:
    if fn not in prod:
        fail('enum_parse_not_explicit ' + fn)

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'format_invalid', 'sessions_not_array', 'translations_not_array',
          'history_not_array', 'too_large', 'bad_shape', 'bad_id', 'bad_kind',
          'bad_format', 'bad_input', 'bad_result', 'bad_state', 'bad_state_pair',
          'duplicate_id', 'bad_key', 'bad_value', 'bad_enabled', 'duplicate_key',
          'bad_text', 'duplicate', 'overflow', 'missing_or_unreadable',
          'path_rejected', 'in_memory']:
    if c not in prod:
        fail('bad_input_missing ' + c)

for const in ['MAX_SESSIONS', 'MAX_TRANSLATIONS', 'MAX_HISTORY',
              'MAX_FILE_BYTES', 'DEFAULT_STATE']:
    if const not in prod:
        fail('bound_missing ' + const)
if 'self.sessions.len() >= MAX_SESSIONS' not in prod:
    fail('session_add_bound_missing')
if 'self.translations.len() >= MAX_TRANSLATIONS' not in prod:
    fail('translation_add_bound_missing')
if 'FORMATS.contains(&format.code())' not in prod:
    fail('format_bidirectional_bound_missing')
if 'OutputFormat::parse' not in prod:
    fail('load_format_bound_missing')
if prod.count('state == SessionState::Ready && result.is_empty()') < 1:
    fail('parse_state_pair_missing')
if 'if state == SessionState::Ready && s.result.is_empty()' not in prod:
    fail('set_state_pair_missing')

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

for fn in ['pub fn add_session(', 'pub fn remove_session(',
           'pub fn set_session_input(', 'pub fn set_session_result(',
           'pub fn set_session_state(', 'pub fn set_session_format(',
           'pub fn set_session_kind(', 'pub fn add_translation(',
           'pub fn remove_translation(', 'pub fn set_translation_enabled(',
           'pub fn set_translation_value(', 'pub fn set_format(',
           'pub fn add_history(', 'pub fn remove_history(',
           'pub fn renderable(', 'pub fn active_translations(',
           'pub fn by_kind(', 'pub fn clipboard_candidates(',
           'pub fn change_event(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('}'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

sess_find = prod.count('self.sessions.iter_mut().find(|s| s.id == id)')
tr_find = prod.count('self.translations.iter_mut().find(|t| t.id == id)')
if sess_find < 5 or tr_find < 2:
    fail('single_item_mutation_count sess=%d tr=%d' % (sess_find, tr_find))
if 'self.sessions.iter().any(|s| s.id == id)' not in prod:
    fail('duplicate_session_id_not_rejected')
if 'self.translations.iter().any(|t| t.key == key)' not in prod:
    fail('duplicate_translation_key_not_rejected')

render_body = body_after('pub fn renderable(', '    }')
if not render_body or 's.state == SessionState::Ready && !s.result.is_empty()' not in render_body:
    fail('renderable_state_aware_missing')
clip_body = body_after('pub fn clipboard_candidates(', '    }')
if not clip_body or 's.format == format' not in clip_body:
    fail('clipboard_format_filter_missing')
kind_body = body_after('pub fn by_kind(', '    }')
if not kind_body or 'out[0] += 1' not in kind_body or 'out[2] += 1' not in kind_body:
    fail('by_kind_three_slots_missing')
active_body = body_after('pub fn active_translations(', '    }')
if not active_body or 't.enabled' not in active_body:
    fail('active_translations_filter_missing')
if 'for_all' in prod or 'confirm_all' in prod:
    fail('batch_mutation_present')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, EVENT_TARGET)' not in prod:
    fail('event_not_unified_envelope')
for key in ['ids', 'values', 'text', 'input', 'result']:
    if 'e.field("%s"), None' % key not in tests:
        fail('user_text_leaks_into_event ' + key)
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
if 'assert_eq!(e.payload.len(), 9);' not in tests:
    fail('event_payload_count_missing')

api = (ROOT / 'src/api.rs').read_text()
if 'generator_session' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX18", name: "lab_generators", state: AxState::(\w+), conflict: "([a-z_]+)"', ax)
if not m or m.group(1) != 'DataLayer' or m.group(2) != 'ai_provider_ui_excluded':
    fail('ax18_state_or_conflict_changed')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX18'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.generator_session"' not in boot:
    fail('module_not_in_boot_diagnostics')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'generator-session.json' in p.read_text():
        fail('ui_surface ' + rel)

print('GENERATOR_SESSION_GUARD_OK keys=5 session_keys=6 translation_keys=4 '
      'kinds=3 formats=2 states=3 bad_inputs=29 opaque_text expected_tables '
      'three_impl_literals_match robust_reused derived_queries '
      'v1_unchanged ax18=DataLayer conflict_kept')

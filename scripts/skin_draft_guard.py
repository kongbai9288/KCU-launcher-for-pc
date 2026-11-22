#!/usr/bin/env python3
"""075：AX14 皮肤草稿会话元数据层；草稿 id 不透明；不扩 v1。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('SKIN_DRAFT_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/skin_draft.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'ht' + 'tp://', 'ht' + 'tps://',
               'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['SKIN_TABLE', 'TEXTURE_TABLE', 'texture', 'uuid', 'png']:
    if banned in prod:
        fail('external_skin_asset ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'robust::MAX_ID_BYTES' not in prod:
    fail('id_bound_not_reused')

# A270：四张常量表用显式 EXPECTED 集合逐值比对，不只比数量与去重
EXPECTED = {
    'KNOWN_KEYS': {'schema', 'active', 'leave_warn', 'drafts'},
    'DRAFT_KEYS': {'id', 'kind', 'state', 'interval'},
    'KINDS': {'saved', 'original'},
    'DRAFT_STATES': {'clean', 'dirty'},
}
parsed = {}
for name, expected in EXPECTED.items():
    m = re.search(name + r':\s*&\[&str\]\s*=\s*&\[(.*?)\];', prod, re.S)
    if not m:
        fail(name + '_parse_failed')
    ks = re.findall(r'"([a-z_]+)"', m.group(1))
    if len(ks) != len(expected) or set(ks) != expected:
        fail(name + '_values=' + str(ks))
    parsed[name] = set(ks)
if 'obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_key_not_rejected')
if 'draft_keys_ok(e)' not in prod:
    fail('draft_keys_not_rejected')

# A269：两个 impl 段里 code()/parse() 的字面量必须与各自常量表逐值一致
for enum_name, table in [('SkinKind', 'KINDS'), ('DraftState', 'DRAFT_STATES')]:
    m = re.search(r'impl ' + enum_name + r' \{(.*?)\n\}', prod, re.S)
    if not m:
        fail(enum_name + '_impl_parse_failed')
    impl = m.group(1)
    code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
    parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
    if code_vals != parsed[table] or parse_vals != parsed[table]:
        fail(enum_name + '_literals_mismatch code=%s parse=%s expected=%s'
             % (sorted(code_vals), sorted(parse_vals), sorted(parsed[table])))
if 'SkinKind::parse' not in prod or 'DraftState::parse' not in prod:
    fail('enum_parse_not_explicit')

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'active_invalid', 'active_dangling', 'leave_warn_not_bool',
          'drafts_not_array', 'too_large', 'bad_shape', 'bad_id',
          'bad_kind', 'bad_state', 'bad_interval', 'duplicate_id', 'overflow']:
    if c not in prod:
        fail('bad_input_missing ' + c)

for const in ['MAX_DRAFTS', 'MAX_INTERVAL', 'MAX_FILE_BYTES', 'DEFAULT_STATE']:
    if const not in prod:
        fail('bound_missing ' + const)
if 'v <= MAX_INTERVAL' not in prod or 'secs > MAX_INTERVAL' not in prod:
    fail('interval_bound_not_applied')
if 'if self.active.as_deref() == Some(id)' not in prod:
    fail('active_cleanup_missing')

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

for fn in ['pub fn add_draft(', 'pub fn remove_draft(', 'pub fn set_active(',
           'pub fn clear_active(', 'pub fn mark_dirty(', 'pub fn mark_clean(',
           'pub fn set_kind(', 'pub fn set_interval(', 'pub fn set_leave_warn(',
           'pub fn drafts_by_kind(', 'pub fn dirty_count(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('}'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, SKIN_TARGET)' not in prod:
    fail('event_not_unified_envelope')
if 'e.field("ids"), None' not in tests:
    fail('draft_ids_leak_into_event')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')

api = (ROOT / 'src/api.rs').read_text()
if 'skin_draft' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX14", name: "skin_editor", state: AxState::(\w+)', ax)
if not m or m.group(1) != 'DataLayer':
    fail('ax14_not_data_layer')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX14'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.skin_draft"' not in boot:
    fail('module_not_in_boot_diagnostics')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'skin-draft.json' in p.read_text():
        fail('ui_surface ' + rel)

print('SKIN_DRAFT_GUARD_OK keys=4 draft_keys=4 kinds=2 states=2 bad_inputs=16 '
      'opaque_ids expected_tables two_impl_literals_match interval_bound v1_unchanged ax14=DataLayer')

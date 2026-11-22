#!/usr/bin/env python3
"""072：AX01 首页小组件布局数据层；组件 id 不透明；不扩 v1。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('WIDGET_LAYOUT_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/widget_layout.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'ht' + 'tp://', 'ht' + 'tps://',
               'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['calendar', 'greeting', 'recent_world', 'minecraft:', 'WIDGET_TYPES']:
    if banned in prod:
        fail('external_widget_type ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'robust::MAX_ID_BYTES' not in prod:
    fail('id_bound_not_reused')

for name, expected in [('KNOWN_KEYS', 3), ('SLOT_KEYS', 2), ('MODES', 2)]:
    m = re.search(name + r':\s*&\[&str\]\s*=\s*&\[(.*?)\];', prod, re.S)
    if not m:
        fail(name + '_parse_failed')
    ks = re.findall(r'"([a-z_]+)"', m.group(1))
    if len(ks) != expected or len(set(ks)) != expected:
        fail(name + '=' + str(ks))
if 'obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_key_not_rejected')
if 'slot_keys_ok(e)' not in prod:
    fail('slot_keys_not_rejected')
if 'LayoutMode::parse' not in prod:
    fail('mode_parse_not_explicit')
impl_m = re.search(r'impl LayoutMode \{(.*?)\n\}', prod, re.S)
if not impl_m:
    fail('layout_mode_impl_parse_failed')
impl = impl_m.group(1)
modes_expected = set(re.findall(r'"([a-z_]+)"', re.search(r'MODES:\s*&\[&str\]\s*=\s*&\[(.*?)\];', prod, re.S).group(1)))
code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
if code_vals != modes_expected or parse_vals != modes_expected:
    fail('mode_literals_mismatch code=%s parse=%s expected=%s' % (sorted(code_vals), sorted(parse_vals), sorted(modes_expected)))

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'mode_invalid', 'slots_not_array', 'too_large', 'bad_shape',
          'bad_id', 'bad_pinned', 'duplicate_id', 'overflow']:
    if c not in prod:
        fail('bad_input_missing ' + c)

for const in ['MAX_SLOTS', 'MAX_FILE_BYTES', 'DEFAULT_STATE']:
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

for fn in ['pub fn add(', 'pub fn remove(', 'pub fn move_to(',
           'pub fn toggle_pin(', 'pub fn set_mode(', 'pub fn pinned_count(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('}'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, WIDGET_TARGET)' not in prod:
    fail('event_not_unified_envelope')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')

api = (ROOT / 'src/api.rs').read_text()
if 'widget_layout' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX01", name: "home_widgets", state: AxState::(\w+)', ax)
if not m or m.group(1) != 'DataLayer':
    fail('ax01_not_data_layer')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX01'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.widget_layout"' not in boot:
    fail('module_not_in_boot_diagnostics')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'widget-layout.json' in p.read_text():
        fail('ui_surface ' + rel)

print('WIDGET_LAYOUT_GUARD_OK keys=3 slot_keys=2 modes=2 bad_inputs=12 opaque_ids v1_unchanged ax01=DataLayer')

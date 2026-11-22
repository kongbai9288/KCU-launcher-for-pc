#!/usr/bin/env python3
"""073：AX13 外观偏好数据层；色号不透明；模式显式 code；不扩 v1。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('APPEARANCE_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/appearance.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'ht' + 'tp://', 'ht' + 'tps://',
               'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['PRESET_COLORS', 'COLOR_TABLE', 'minecraft:', '#ffffff', '#000000']:
    if banned in prod:
        fail('external_color_table ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'robust::MAX_ID_BYTES' not in prod:
    fail('id_bound_not_reused')

EXPECTED = {
    'KNOWN_KEYS': {'schema', 'mode', 'accent', 'background', 'transparency', 'presets'},
    'PRESET_KEYS': {'id', 'accent'},
    'MODES': {'light', 'dark', 'oled', 'system'},
}
for name, expected in EXPECTED.items():
    m = re.search(name + r':\s*&\[&str\]\s*=\s*&\[(.*?)\];', prod, re.S)
    if not m:
        fail(name + '_parse_failed')
    ks = re.findall(r'"([a-z_]+)"', m.group(1))
    if len(ks) != len(expected) or set(ks) != expected:
        fail(name + '_values=' + str(ks))
if 'obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_key_not_rejected')
if 'preset_keys_ok(e)' not in prod:
    fail('preset_keys_not_rejected')
if 'AppearanceMode::parse' not in prod:
    fail('mode_parse_not_explicit')

# A269：impl 段里 code()/parse() 的字面量必须与 MODES 表逐值一致
impl_m = re.search(r'impl AppearanceMode \{(.*?)\n\}', prod, re.S)
if not impl_m:
    fail('appearance_mode_impl_parse_failed')
impl = impl_m.group(1)
modes_expected = set(re.findall(r'"([a-z_]+)"', re.search(r'MODES:\s*&\[&str\]\s*=\s*&\[(.*?)\];', prod, re.S).group(1)))
code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
if code_vals != modes_expected or parse_vals != modes_expected:
    fail('mode_literals_mismatch code=%s parse=%s expected=%s' % (sorted(code_vals), sorted(parse_vals), sorted(modes_expected)))

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'mode_invalid', 'accent_invalid', 'background_not_bool',
          'transparency_not_bool', 'presets_not_array', 'too_large',
          'bad_shape', 'bad_id', 'bad_accent', 'duplicate_id', 'overflow']:
    if c not in prod:
        fail('bad_input_missing ' + c)

for const in ['MAX_PRESETS', 'MAX_FILE_BYTES', 'DEFAULT_STATE']:
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

for fn in ['pub fn set_mode(', 'pub fn set_accent(', 'pub fn clear_accent(',
           'pub fn set_background(', 'pub fn set_transparency(',
           'pub fn add_preset(', 'pub fn remove_preset(', 'pub fn apply_preset(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('}'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, APPEARANCE_TARGET)' not in prod:
    fail('event_not_unified_envelope')
if 'e.field("accent"), None' not in tests:
    fail('user_accent_value_leaks_into_event')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')

api = (ROOT / 'src/api.rs').read_text()
if 'appearance' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX13", name: "appearance_modes", state: AxState::(\w+)', ax)
if not m or m.group(1) != 'DataLayer':
    fail('ax13_not_data_layer')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX13'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.appearance"' not in boot:
    fail('module_not_in_boot_diagnostics')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'appearance.json' in p.read_text():
        fail('ui_surface ' + rel)

print('APPEARANCE_GUARD_OK keys=6 preset_keys=2 modes=4 bad_inputs=15 opaque_colors impl_literals_match v1_unchanged ax13=DataLayer')

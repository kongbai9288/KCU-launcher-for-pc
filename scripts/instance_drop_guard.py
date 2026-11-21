#!/usr/bin/env python3
"""070：AX24 未分组与拖拽落点数据层；plan 只算路径不落用户文件；不扩 v1。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('INSTANCE_DROP_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/instance_drop.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'ht' + 'tp://', 'ht' + 'tps://',
               'fs::copy', 'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
if '.unwrap()' in prod or '.expect(' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))

km = re.search(r'KNOWN_KEYS:\s*&\[&str\]\s*=\s*&\[(.*?)\];', prod, re.S)
if not km:
    fail('known_keys_parse_failed')
ks = re.findall(r'"([a-z_]+)"', km.group(1))
if len(ks) != 3 or len(set(ks)) != 3:
    fail('known_keys=' + str(ks))
if 'obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_key_not_rejected')

cm = re.search(r'CATEGORY_DIRS:\s*&\[\(&str, &str\)\]\s*=\s*&\[(.*?)\];', prod, re.S)
if not cm:
    fail('category_table_parse_failed')
pairs = re.findall(r'\("([a-z_]+)",\s*"([a-z_]+)"\)', cm.group(1))
if len(pairs) != 3 or len({c for c, _ in pairs}) != 3 or len({d for _, d in pairs}) != 3:
    fail('category_dirs=' + str(pairs))
if 'category_dir(category)' not in prod:
    fail('category_lookup_missing')

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid', 'collapsed_invalid',
          'ungrouped_not_array', 'too_large', 'bad_id']:
    if c not in prod:
        fail('bad_input_missing ' + c)

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

plan = body_after('pub fn plan(', '    }')
if not plan or not plan.rstrip().endswith('}'):
    fail('plan_body_parse_failed')
if 'fs::' in plan or 'std::fs' in plan:
    fail('plan_writes_user_files')
if 'Envelope::new' in plan:
    fail('plan_emits_event_instead_of_path')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, DROP_TARGET)' not in prod:
    fail('event_not_unified_envelope')

if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
api = (ROOT / 'src/api.rs').read_text()
if 'instance_drop' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX24", name: "ungrouped_drop", state: AxState::(\w+)', ax)
if not m or m.group(1) != 'DataLayer':
    fail('ax24_not_data_layer')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX24'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.instance_drop"' not in boot:
    fail('module_not_in_boot_diagnostics')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'instance-drop.json' in p.read_text():
        fail('ui_surface ' + rel)

print('INSTANCE_DROP_GUARD_OK keys=3 categories=3 bad_inputs=8 plan_pure v1_unchanged ax24=DataLayer')

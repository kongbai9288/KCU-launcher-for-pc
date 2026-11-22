#!/usr/bin/env python3
"""074：AX10 首次启动向导步骤状态机数据层；步骤 id 不透明；不扩 v1。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('FIRST_RUN_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/first_run.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'ht' + 'tp://', 'ht' + 'tps://',
               'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['STEP_CATALOG', 'language', 'account', 'java', 'minecraft']:
    if banned in prod:
        fail('external_step_catalog ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'robust::MAX_ID_BYTES' not in prod:
    fail('id_bound_not_reused')

# A270：三张常量表用显式 EXPECTED 集合逐值比对，不只比数量与去重
EXPECTED = {
    'KNOWN_KEYS': {'schema', 'cursor', 'finished', 'steps'},
    'STEP_KEYS': {'id', 'required', 'state'},
    'STATES': {'pending', 'done', 'skipped'},
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
if 'step_keys_ok(e)' not in prod:
    fail('step_keys_not_rejected')
if 'StepState::parse' not in prod:
    fail('state_parse_not_explicit')

# A269：impl 段里 code()/parse() 的字面量必须与 STATES 表逐值一致
impl_m = re.search(r'impl StepState \{(.*?)\n\}', prod, re.S)
if not impl_m:
    fail('step_state_impl_parse_failed')
impl = impl_m.group(1)
code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
if code_vals != EXPECTED['STATES'] or parse_vals != EXPECTED['STATES']:
    fail('state_literals_mismatch code=%s parse=%s expected=%s'
         % (sorted(code_vals), sorted(parse_vals), sorted(EXPECTED['STATES'])))

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'cursor_not_u64', 'cursor_out_of_range', 'finished_not_bool',
          'steps_not_array', 'too_large', 'bad_shape', 'bad_id',
          'bad_required', 'bad_state', 'duplicate_id', 'overflow']:
    if c not in prod:
        fail('bad_input_missing ' + c)

for const in ['MAX_STEPS', 'MAX_FILE_BYTES', 'DEFAULT_STATE']:
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

for fn in ['pub fn add_step(', 'pub fn remove_step(', 'pub fn advance(',
           'pub fn back(', 'pub fn skip(', 'pub fn set_state(',
           'pub fn set_finished(', 'pub fn pending_required(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('}'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

skip_body = body_after('pub fn skip(', '    }')
if not skip_body or 'if s.required {' not in skip_body:
    fail('required_step_guard_missing')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, FIRST_RUN_TARGET)' not in prod:
    fail('event_not_unified_envelope')
if 'e.field("ids"), None' not in tests:
    fail('step_ids_leak_into_event')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')

api = (ROOT / 'src/api.rs').read_text()
if 'first_run' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX10", name: "first_run_wizard", state: AxState::(\w+)', ax)
if not m or m.group(1) != 'DataLayer':
    fail('ax10_not_data_layer')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX10'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.first_run"' not in boot:
    fail('module_not_in_boot_diagnostics')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'first-run.json' in p.read_text():
        fail('ui_surface ' + rel)

print('FIRST_RUN_GUARD_OK keys=4 step_keys=3 states=3 bad_inputs=15 opaque_ids '
      'expected_tables impl_literals_match required_guard v1_unchanged ax10=DataLayer')

#!/usr/bin/env python3
"""076：AX09 逐条升级决策持久化数据层；单条确认；不扩 v1；不重复实现版本判定。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('UPGRADE_PLAN_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/upgrade_plan.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'ht' + 'tp://', 'ht' + 'tps://',
               'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['COMPAT_TABLE', 'UPGRADE_TABLE', 'VERSION_TABLE', 'cmp_precedence',
               'semver', 'Version::parse', 'url', 'token', 'uuid', 'minecraft:']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'robust::MAX_ID_BYTES' not in prod:
    fail('id_bound_not_reused')
if 'let mut lines: Vec<String> = Vec::new();' not in prod:
    fail('explicit_vec_type_missing')

# A270：四张常量表用显式 EXPECTED 集合逐值比对，不只比数量与去重
EXPECTED = {
    'KNOWN_KEYS': {'schema', 'page_size', 'choices'},
    'CHOICE_KEYS': {'id', 'current', 'candidate', 'compat', 'mode', 'confirmed'},
    'COMPATS': {'compatible', 'conflict', 'unknown'},
    'MODES': {'defer', 'direct', 'clone'},
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
if 'choice_keys_ok(e)' not in prod:
    fail('choice_keys_not_rejected')

# A269：两个 impl 段里 code()/parse() 的字面量必须与各自常量表逐值一致
for enum_name, table in [('Compat', 'COMPATS'), ('UpgradeMode', 'MODES')]:
    m = re.search(r'impl ' + enum_name + r' \{(.*?)\n\}', prod, re.S)
    if not m:
        fail(enum_name + '_impl_parse_failed')
    impl = m.group(1)
    code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
    parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
    if code_vals != parsed[table] or parse_vals != parsed[table]:
        fail(enum_name + '_literals_mismatch code=%s parse=%s expected=%s'
             % (sorted(code_vals), sorted(parse_vals), sorted(parsed[table])))
if 'Compat::parse' not in prod or 'UpgradeMode::parse' not in prod:
    fail('enum_parse_not_explicit')

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'page_size_invalid', 'choices_not_array', 'too_large', 'bad_shape',
          'bad_id', 'bad_current', 'bad_candidate', 'bad_compat', 'bad_mode',
          'bad_confirmed', 'bad_state_pair', 'duplicate_id', 'overflow']:
    if c not in prod:
        fail('bad_input_missing ' + c)
if 'confirmed && mode == UpgradeMode::Defer' not in prod or 'confirmed && compat == Compat::Conflict' not in prod:
    fail('contradictory_pair_not_rejected')

for const in ['MAX_CHOICES', 'MAX_PAGE_SIZE', 'MIN_PAGE_SIZE', 'MAX_FILE_BYTES', 'DEFAULT_STATE']:
    if const not in prod:
        fail('bound_missing ' + const)
if 'v >= MIN_PAGE_SIZE as u64 && v <= MAX_PAGE_SIZE as u64' not in prod:
    fail('page_size_load_bound_missing')
if 'size < MIN_PAGE_SIZE || size > MAX_PAGE_SIZE' not in prod:
    fail('page_size_set_bound_missing')
if 'UpgradeMode::Defer' not in prod:
    fail('default_defer_missing')

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

for fn in ['pub fn add_choice(', 'pub fn remove_choice(', 'pub fn set_compat(',
           'pub fn set_mode(', 'pub fn confirm(', 'pub fn revoke(',
           'pub fn set_page_size(', 'pub fn page_count(', 'pub fn page_items(',
           'pub fn pending_count(', 'pub fn ready_count(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('}'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

find_count = prod.count('self.choices.iter_mut().find(|c| c.id == id)')
if find_count < 4:
    fail('single_item_mutation_count=%d' % find_count)
confirm_body = body_after('pub fn confirm(', '    }')
if not confirm_body or 'if c.mode == UpgradeMode::Defer' not in confirm_body or 'return false;' not in confirm_body:
    fail('defer_confirm_not_refused')
if 'for c in' in confirm_body:
    fail('batch_confirm_present')
compat_body = body_after('pub fn set_compat(', '    }')
if not compat_body or 'if c.compat == Compat::Conflict' not in compat_body or 'c.mode = UpgradeMode::Defer;' not in compat_body:
    fail('conflict_reset_missing')
if 'confirm_all' in prod or 'set_all_modes' in prod:
    fail('batch_confirm_api_present')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, UPGRADE_TARGET)' not in prod:
    fail('event_not_unified_envelope')
if 'e.field("ids"), None' not in tests or 'e.field("versions"), None' not in tests:
    fail('ids_or_versions_leak_into_event')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')

api = (ROOT / 'src/api.rs').read_text()
if 'upgrade_plan' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX09", name: "upgrade_compat", state: AxState::(\w+)', ax)
if not m or m.group(1) != 'DataLayer':
    fail('ax09_not_data_layer')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX09'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.upgrade_plan"' not in boot:
    fail('module_not_in_boot_diagnostics')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'upgrade-plan.json' in p.read_text():
        fail('ui_surface ' + rel)

print('UPGRADE_PLAN_GUARD_OK keys=3 choice_keys=6 compats=3 modes=3 bad_inputs=17 '
      'opaque_text expected_tables two_impl_literals_match single_item_confirm '
      'conflict_reset page_bounds v1_unchanged ax09=DataLayer')

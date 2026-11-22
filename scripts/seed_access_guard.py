#!/usr/bin/env python3
"""079：AX19 种子可见性与审计元数据层；不扩 v1；不落 NBT 与地形探索。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('SEED_ACCESS_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/seed_access.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'ht' + 'tp://', 'ht' + 'tps://',
               'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['SEED_TABLE', 'POLICY_TABLE', 'AUDIT_TABLE', 'VISIBILITY_TABLE',
               'DENY_TABLE', 'COLOR_TABLE', 'PATTERN_CODES', 'cmp_precedence',
               'semver', 'Version::parse', 'url', 'Token', 'token', 'uuid',
               'texture', 'png', 'minecraft:', 'give ', 'regex', 'glob',
               'AIProvider', 'WikiEntries', 'StepCatalog', 'dialog', '\u00a7']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'let mut lines: Vec<String> = Vec::new();' not in prod:
    fail('explicit_vec_type_missing')
if 'let mut records: Vec<SeedRecord> = Vec::new();' not in prod:
    fail('explicit_record_vec_type_missing')

# A270：五张常量表用显式 EXPECTED 集合逐值比对
EXPECTED = {
    'KNOWN_KEYS': {'schema', 'guest_mode', 'password_required', 'records', 'audit', 'locked_features', 'command_deny'},
    'SEED_KEYS': {'instance_id', 'value', 'policy', 'note'},
    'AUDIT_KEYS': {'id', 'action', 'target', 'scope'},
    'POLICIES': {'visible', 'hint', 'hidden'},
    'ACTIONS': {'view', 'policy_change', 'guest_toggle', 'hidden'},
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
if 'seed_keys_ok(e)' not in prod:
    fail('seed_keys_not_rejected')
if 'audit_keys_ok(e)' not in prod:
    fail('audit_keys_not_rejected')

# A247：显式复用既有文本上限常量，删 import 行要真 FAIL
if 'use crate::core::robust;' not in prod:
    fail('robust_import_missing')
if prod.count('robust::MAX_TEXT_BYTES') < 2:
    fail('text_bound_not_reused count=%d' % prod.count('robust::MAX_TEXT_BYTES'))
if 'robust::read_or_default(&path, DEFAULT_STATE)' not in prod:
    fail('read_or_default_not_reused')

# A269：两个 impl 段里 code()/parse() 的字面量与各自常量表逐值一致
for enum_name, table in [('SeedPolicy', 'POLICIES'), ('AuditAction', 'ACTIONS')]:
    m = re.search(r'impl ' + enum_name + r' \{(.*?)\n\}', prod, re.S)
    if not m:
        fail(enum_name + '_impl_parse_failed')
    impl = m.group(1)
    code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
    parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
    if code_vals != parsed[table] or parse_vals != parsed[table]:
        fail(enum_name + '_literals_mismatch code=%s parse=%s expected=%s'
             % (sorted(code_vals), sorted(parse_vals), sorted(parsed[table])))
for fn in ['SeedPolicy::parse', 'AuditAction::parse']:
    if fn not in prod:
        fail('enum_parse_not_explicit ' + fn)

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'guest_not_bool', 'password_not_bool', 'records_not_array',
          'audit_not_array', 'locked_not_array', 'deny_not_array', 'too_large',
          'missing_or_unreadable', 'path_rejected', 'in_memory',
          'bad_shape', 'bad_id', 'bad_value', 'bad_policy', 'bad_note',
          'bad_policy_note_pair', 'duplicate_id', 'bad_action', 'bad_target',
          'bad_scope', 'bad_text', 'duplicate', 'overflow']:
    if c not in prod:
        fail('bad_input_missing ' + c)

for const in ['MAX_RECORDS', 'MAX_AUDIT', 'MAX_LOCKED', 'MAX_DENY',
              'MAX_FILE_BYTES', 'DEFAULT_STATE']:
    if const not in prod:
        fail('bound_missing ' + const)
if 'self.records.len() >= MAX_RECORDS' not in prod:
    fail('record_add_bound_missing')
if 'self.audit.len() >= MAX_AUDIT' not in prod:
    fail('audit_add_bound_missing')
if 'self.locked_features.len() >= MAX_LOCKED' not in prod:
    fail('locked_add_bound_missing')
if 'self.command_deny.len() >= MAX_DENY' not in prod:
    fail('deny_add_bound_missing')
if 'POLICIES.contains(&policy.code())' not in prod:
    fail('policy_bidirectional_bound_missing')
if 'ACTIONS.contains(&action.code())' not in prod:
    fail('action_bidirectional_bound_missing')

# 矛盾态在 parse、set_policy、set_note 三处一致
if 'policy_note_pair_ok(policy, &note)' not in prod:
    fail('parse_pair_check_missing')
fn_set_policy = 'pub fn set_policy(&mut self, instance_id: &str, policy: SeedPolicy) -> bool {'
if fn_set_policy not in prod:
    fail('set_policy_signature_changed')
sp = prod[prod.find(fn_set_policy):]
sp = sp[:sp.find('\n    }') + 6]
if 'policy_note_pair_ok(policy, &r.note)' not in sp:
    fail('set_policy_pair_check_missing')
fn_set_note = 'pub fn set_note(&mut self, instance_id: &str, note: &str) -> bool {'
if fn_set_note not in prod:
    fail('set_note_signature_changed')
sn = prod[prod.find(fn_set_note):]
sn = sn[:sn.find('\n    }') + 6]
if 'policy_note_pair_ok(r.policy, note)' not in sn:
    fail('set_note_pair_check_missing')

# 3x2 可见性矩阵六格
matrix = prod[prod.find('pub fn classify('):]
matrix = matrix[:matrix.find('\n}') + 2]
for branch in ['(SeedPolicy::Visible, false) => SeedPolicy::Visible',
               '(SeedPolicy::Visible, true) => SeedPolicy::Hidden',
               '(SeedPolicy::Hint, false) => SeedPolicy::Hint',
               '(SeedPolicy::Hint, true) => SeedPolicy::Hidden',
               '(SeedPolicy::Hidden, false) => SeedPolicy::Hidden',
               '(SeedPolicy::Hidden, true) => SeedPolicy::Hidden']:
    if branch not in matrix:
        fail('matrix_branch_missing ' + branch)

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

for fn in ['pub fn add_record(', 'pub fn remove_record(', 'pub fn set_policy(',
           'pub fn set_note(', 'pub fn set_value(', 'pub fn add_audit(',
           'pub fn remove_audit(', 'pub fn set_audit_action(',
           'pub fn set_guest_mode(', 'pub fn set_password_required(',
           'pub fn add_locked(', 'pub fn remove_locked(', 'pub fn add_deny(',
           'pub fn remove_deny(', 'pub fn visible_records(',
           'pub fn hint_records(', 'pub fn hidden_records(',
           'pub fn policy_counts(', 'pub fn audit_by_action(',
           'pub fn guest_locked(', 'pub fn command_allowed(',
           'pub fn change_event(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('}'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

find_count = prod.count('iter_mut().find(')
if find_count < 4:
    fail('single_item_mutation_count=%d' % find_count)
if 'self.records.iter().any(|r| r.instance_id == instance_id)' not in prod:
    fail('duplicate_record_id_not_rejected')
if 'self.audit.iter().any(|a| a.id == id)' not in prod:
    fail('duplicate_audit_id_not_rejected')

vis_body = body_after('pub fn visible_records(', '    }')
if not vis_body or 'classify(r.policy, self.guest_mode) == SeedPolicy::Visible' not in vis_body:
    fail('visible_records_matrix_missing')
hint_body = body_after('pub fn hint_records(', '    }')
if not hint_body or 'classify(r.policy, self.guest_mode) == SeedPolicy::Hint' not in hint_body:
    fail('hint_records_matrix_missing')
hidden_body = body_after('pub fn hidden_records(', '    }')
if not hidden_body or 'classify(r.policy, self.guest_mode) == SeedPolicy::Hidden' not in hidden_body:
    fail('hidden_records_matrix_missing')
gl_body = body_after('pub fn guest_locked(', '    }')
if not gl_body or 'self.guest_mode &&' not in gl_body:
    fail('guest_locked_scope_missing')
ca_body = body_after('pub fn command_allowed(', '    }')
if not ca_body or '!self.command_deny.iter().any' not in ca_body:
    fail('command_deny_filter_missing')
if 'for_all' in prod or 'confirm_all' in prod:
    fail('batch_mutation_present')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, EVENT_TARGET)' not in prod:
    fail('event_not_unified_envelope')
if 'for key in ["value", "note", "instance_id", "target", "scope"]' not in tests:
    fail('user_text_assertion_loop_missing')
if 'assert_eq!(e.field(key), None);' not in tests:
    fail('user_text_leaks_into_event')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
if 'assert_eq!(e.payload.len(), 12);' not in tests:
    fail('event_payload_count_missing')

api = (ROOT / 'src/api.rs').read_text()
if 'seed_access' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX19", name: "seed_map", state: AxState::(\w+), conflict: "([a-z_]*)"', ax)
if not m or m.group(1) != 'DataLayer' or m.group(2) != '':
    fail('ax19_state_or_conflict_changed')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX19'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.seed_access"' not in boot:
    fail('module_not_in_boot_diagnostics')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'seed-access.json' in p.read_text():
        fail('ui_surface ' + rel)

print('SEED_ACCESS_GUARD_OK keys=7 seed_keys=4 audit_keys=4 '
      'policies=3 actions=4 bad_inputs=32 opaque_text expected_tables '
      'two_impl_literals_match robust_reused matrix_six_branches '
      'pair_checks_three pure_queries v1_unchanged ax19=DataLayer conflict_empty')

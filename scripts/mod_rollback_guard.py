#!/usr/bin/env python3
"""085：AX04 顺序决策队列与版本回滚计划；零内容执行、不扩 v1。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(reason):
    print('MOD_ROLLBACK_GUARD_FAIL reason=' + reason)
    sys.exit(1)


f = ROOT / 'src/core/mod_rollback.rs'
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
               'reqwest', 'remove_dir_all', 'fs::remove_file', 'x-api-key']:
    if banned in prod:
        fail('forbidden_literal ' + repr(banned))
for banned in ['EDITOR_TABLE', 'FIELD_TABLE', 'LICENSE_TABLE', 'STEP_CATALOG',
               'url', 'uuid', 'texture', 'png', 'minecraft:', 'give ', 'regex',
               'glob', 'AIProvider', 'WikiEntries', '\u00a7', '.jar']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 2:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
for decl in ['let mut lines: Vec<String> = Vec::new();',
             'let mut items: Vec<RollbackItem> = Vec::new();',
             'let mut out: Vec<&str> = Vec::new();',
             'let items: Vec<Value> = p.items.iter()']:
    if decl not in prod:
        fail('explicit_vec_type_missing ' + repr(decl))

# A270：六张常量表用显式 EXPECTED 集合逐值比对
EXPECTED = {
    'ROOT_KEYS': {'schema', 'scope', 'current', 'items'},
    'ITEM_KEYS': {'id', 'mod_id', 'installed', 'candidate', 'kind',
                  'disable_lower', 'choice', 'snapshot'},
    'SCOPES': {'instance'},
    'KINDS': {'same_version', 'higher_version', 'lower_version', 'other_issue'},
    'CHOICES': {'pending', 'keep', 'replace', 'rollback'},
    'SNAPSHOTS': {'server_properties', 'ops_json', 'mod_config', 'loader_version'},
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
if 'obj.keys().any(|k| !ROOT_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_root_key_not_rejected')
if 'io.keys().any(|k| !ITEM_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_item_key_not_rejected')
if 'current > arr.len()' not in prod:
    fail('current_out_of_range_not_rejected')

# A247：显式复用既有文本上限常量、路径模块与读取降级
if 'use crate::core::robust;' not in prod:
    fail('robust_import_missing')
if prod.count('robust::MAX_TEXT_BYTES') < 2:
    fail('text_bound_not_reused count=%d' % prod.count('robust::MAX_TEXT_BYTES'))
if 'robust::read_or_default(&path, DEFAULT_STATE)' not in prod:
    fail('read_or_default_not_reused')
if 'use semver::Version;' not in prod:
    fail('semver_import_missing')
if 'use std::cmp::Ordering;' not in prod:
    fail('ordering_import_missing')

# A94 / A160：版本判定走 cmp_precedence，不用 Version 的 ==
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


vo = body_after('fn version_order(', '}')
if not vo or not vo.rstrip().endswith('}'):
    fail('version_order_body_parse_failed')
if 'Some(b.cmp_precedence(&a))' not in vo:
    fail('version_order_not_using_cmp_precedence')
if 'installed == candidate' in vo or 'candidate == installed' in vo:
    fail('version_order_uses_equality')
cl = body_after('fn classify(', '}')
if not cl or 'Some(Ordering::Greater) => DecisionKind::HigherVersion' not in cl:
    fail('classify_body_parse_failed')
for lit in ['Some(Ordering::Equal) => DecisionKind::SameVersion',
            'Some(Ordering::Less) => DecisionKind::LowerVersion',
            'None => DecisionKind::OtherIssue']:
    if lit not in cl:
        fail('classify_literal_missing ' + lit)

# A269：四个 impl 段里 code()/parse() 的字面量与各自常量表逐值一致
for enum_name, table in [('RollbackScope', 'SCOPES'), ('DecisionKind', 'KINDS'),
                         ('UserChoice', 'CHOICES'), ('SnapshotTarget', 'SNAPSHOTS')]:
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
for fn in ['RollbackScope::parse', 'DecisionKind::parse',
           'UserChoice::parse', 'SnapshotTarget::parse']:
    if fn not in prod:
        fail('enum_parse_not_explicit ' + fn)
for bound in ['SCOPES.contains(&self.scope.code())',
              'SNAPSHOTS.contains(&snapshot.code())',
              'KINDS.contains(&kind.code())',
              'CHOICES.contains(&choice.code())']:
    if bound not in prod:
        fail('set_bound_missing ' + bound)

# 坏输入标签
for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'bad_scope', 'items_not_array', 'items_too_many', 'bad_current',
          'current_out_of_range', 'item_not_object', 'item_unknown_key',
          'id_too_large', 'bad_id', 'duplicate_id', 'mod_id_too_large',
          'bad_mod_id', 'installed_too_large', 'bad_installed',
          'candidate_too_large', 'bad_candidate', 'bad_kind',
          'bad_disable_lower', 'bad_choice', 'bad_snapshot', 'bad_item_state',
          'in_memory', 'path_rejected', 'missing_or_unreadable', 'too_large',
          'no_root']:
    if c not in prod:
        fail('bad_input_missing ' + c)
for const in ['MAX_FILE_BYTES', 'MAX_ITEMS', 'DEFAULT_STATE', 'EVENT_TARGET']:
    if const not in prod:
        fail('bound_missing ' + const)

# 八个纯查询段不读文件
for fn in ['pub fn page_count(', 'pub fn pending_count(', 'pub fn resolved_count(',
           'pub fn current_item(', 'pub fn disable_lower_count(',
           'pub fn by_kind(', 'pub fn by_snapshot(', 'pub fn summary(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('    }'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

# E322 教训：解析 item_consistent 函数体逐项核五条字面量
ic = body_after('fn item_consistent(', '}')
if not ic or not ic.rstrip().endswith('}'):
    fail('item_consistent_body_parse_failed')
for check in ['i.kind == DecisionKind::HigherVersion && !i.disable_lower',
              'i.kind == DecisionKind::SameVersion && i.disable_lower',
              'i.choice == UserChoice::Rollback',
              'i.choice != UserChoice::Pending',
              'i.snapshot == SnapshotTarget::LoaderVersion && i.choice == UserChoice::Keep']:
    if check not in ic:
        fail('item_consistent_check_missing ' + check)
calls = prod.count('item_consistent(&')
if calls != 9:
    fail('item_consistent_calls=%d expected=9' % calls)
for marker, expected in [('if !item_consistent(&i) {', 3),
                         ('if !item_consistent(&candidate) {', 2),
                         ('|| !item_consistent(&candidate) {', 3),
                         ('if !item_consistent(&next) {', 1)]:
    if prod.count(marker) != expected:
        fail('item_consistent_call_shape=%s count=%d expected=%d'
             % (marker, prod.count(marker), expected))

# 11:244 顺序页码与单条选择，无批量
for fn in ['pub fn add_item(', 'pub fn append_issue(', 'pub fn resolve_current(',
           'pub fn set_kind(', 'pub fn set_choice(', 'pub fn set_disable_lower(',
           'pub fn set_snapshot(', 'pub fn set_versions(', 'pub fn remove_item(']:
    if fn not in prod:
        fail('single_mutation_missing ' + fn)
if 'mark_all' in prod or 'confirm_all' in prod or 'resolve_all' in prod:
    fail('batch_mutation_present')
if 'if self.pending_count() == 0 {' not in prod:
    fail('append_issue_pending_guard_missing')
if 'self.current += 1;' not in prod:
    fail('single_page_advance_missing')
if 'if choice == UserChoice::Pending || self.current >= self.items.len() {' not in prod:
    fail('resolve_current_bound_missing')
if 'let kind = classify(installed, candidate);' not in prod:
    fail('classify_not_reused_in_add_item')
if 'let disable_lower = kind == DecisionKind::HigherVersion;' not in prod:
    fail('higher_version_disable_lower_missing')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, EVENT_TARGET)' not in prod:
    fail('event_not_unified_envelope')

# E330 教训：解析 change_event 函数体核不进用户文本与载荷数
ev = body_after('pub fn change_event(', '    }')
if not ev or not ev.rstrip().endswith('    }'):
    fail('change_event_body_parse_failed')
for key in ['"id"', '"mod_id"', '"installed"', '"candidate"', '"title"', '"body"']:
    if '.with(%s,' % key in ev:
        fail('user_text_in_event_payload ' + key)
if ev.count('.with(') != 10:
    fail('event_payload_count=%d expected=10' % ev.count('.with('))
for key in ['id', 'mod_id', 'installed', 'candidate', 'title', 'body']:
    if 'e.field("%s"), None' % key not in tests:
        fail('user_text_assertion_missing ' + key)
if 'assert_eq!(e.payload.len(), 10);' not in tests:
    fail('event_payload_count_missing')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
for key in ['"schema": 1,', '"scope": p.scope.code(),', '"current": p.current,',
            '"items": items', '"id": i.id', '"mod_id": i.mod_id',
            '"installed": i.installed', '"candidate": i.candidate',
            '"kind": i.kind.code()', '"disable_lower": i.disable_lower',
            '"choice": i.choice.code()', '"snapshot": i.snapshot.code()']:
    if key not in prod:
        fail('serialize_key_missing ' + repr(key))

api = (ROOT / 'src/api.rs').read_text()
if 'mod_rollback' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX04", name: "mod_rollback", state: AxState::(\w+), conflict: "([a-z_]*)"', ax)
if not m or m.group(1) != 'DataLayer' or m.group(2) != '':
    fail('ax04_state_or_conflict_changed')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX04'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.mod_rollback"' not in boot:
    fail('module_not_in_boot_diagnostics')
mod = (ROOT / 'src/core/mod.rs').read_text()
if 'pub mod mod_rollback;' not in mod:
    fail('mod_declaration_missing')
ci = (ROOT / '.github/workflows/ci.yml').read_text()
if 'name: mod_rollback_guard' not in ci:
    fail('ci_step_missing')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'mod-rollback.json' in p.read_text():
        fail('ui_surface ' + rel)

print('MOD_ROLLBACK_GUARD_OK root_keys=4 item_keys=8 scopes=1 kinds=4 '
      'choices=4 snapshots=4 expected_tables four_impl_literals_match '
      'cmp_precedence robust_reused consistent_checks_five calls=9 pure_queries '
      'event_payload=10 v1_unchanged ax04=DataLayer conflict_empty')

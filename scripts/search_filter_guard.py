#!/usr/bin/env python3
"""077：AX16 搜索筛选条件持久化数据层；不扩 v1；不重复实现遍历与快照解析。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('SEARCH_FILTER_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/search_filter.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'ht' + 'tp://', 'ht' + 'tps://',
               'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['CONDITION_TABLE', 'VALUE_TABLE', 'SORT_TABLE', 'OP_TABLE',
               'cmp_precedence', 'semver', 'Version::parse', 'url', 'token',
               'uuid', 'minecraft:', 'regex', 'glob', 'WikiEntries']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'robust::MAX_ID_BYTES' not in prod:
    fail('id_bound_not_reused')
if 'let mut lines: Vec<String> = Vec::new();' not in prod:
    fail('explicit_vec_type_missing')

# A270：六张常量表用显式 EXPECTED 集合逐值比对，不只比数量与去重
EXPECTED = {
    'KNOWN_KEYS': {'schema', 'scope', 'sort', 'conditions', 'excludes', 'saved', 'history'},
    'CONDITION_KEYS': {'id', 'dimension', 'op', 'value', 'enabled'},
    'SORT_KEYS': {'key', 'desc'},
    'SCOPES': {'current', 'recursive'},
    'DIMENSIONS': {'name', 'type', 'size', 'modified', 'path'},
    'OPS': {'contains', 'equals', 'prefix', 'suffix'},
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
if 'condition_keys_ok(e)' not in prod:
    fail('condition_keys_not_rejected')
if 'sort_keys_ok(o)' not in prod:
    fail('sort_keys_not_rejected')

# A247：排序维度复用同一张 DIMENSIONS 表，删别名行要真 FAIL
if 'pub const SORT_DIMENSIONS: &[&str] = DIMENSIONS;' not in prod:
    fail('sort_dimensions_alias_missing')
if 'SORT_DIMENSIONS.contains(&s)' not in prod or 'SORT_DIMENSIONS.contains(&key.code())' not in prod:
    fail('sort_dimensions_alias_not_used')

# A269：两个 impl 段里 code()/parse() 的字面量必须与各自常量表逐值一致
for enum_name, table in [('SearchDimension', 'DIMENSIONS'), ('SearchOp', 'OPS')]:
    m = re.search(r'impl ' + enum_name + r' \{(.*?)\n\}', prod, re.S)
    if not m:
        fail(enum_name + '_impl_parse_failed')
    impl = m.group(1)
    code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
    parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
    if code_vals != parsed[table] or parse_vals != parsed[table]:
        fail(enum_name + '_literals_mismatch code=%s parse=%s expected=%s'
             % (sorted(code_vals), sorted(parse_vals), sorted(parsed[table])))
if 'SearchDimension::parse' not in prod or 'SearchOp::parse' not in prod:
    fail('enum_parse_not_explicit')

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'scope_invalid', 'sort_invalid', 'conditions_not_array',
          'excludes_not_array', 'saved_not_array', 'history_not_array',
          'too_large', 'bad_shape', 'bad_id', 'bad_dimension', 'bad_op',
          'bad_value', 'bad_enabled', 'duplicate_id', 'bad_text',
          'duplicate', 'overflow']:
    if c not in prod:
        fail('bad_input_missing ' + c)

for const in ['MAX_CONDITIONS', 'MAX_EXCLUDES', 'MAX_SAVED', 'MAX_HISTORY',
              'MAX_FILE_BYTES', 'DEFAULT_STATE']:
    if const not in prod:
        fail('bound_missing ' + const)
if 'SCOPES.contains(&s)' not in prod or 'SCOPES.contains(&scope)' not in prod:
    fail('scope_bound_not_bidirectional')
if 'self.conditions.len() >= MAX_CONDITIONS' not in prod:
    fail('condition_add_bound_missing')
if 'self.excludes.len() >= MAX_EXCLUDES' not in prod:
    fail('exclude_add_bound_missing')

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

for fn in ['pub fn add_condition(', 'pub fn remove_condition(',
           'pub fn set_condition_enabled(', 'pub fn set_condition_op(',
           'pub fn set_condition_value(', 'pub fn add_exclude(',
           'pub fn remove_exclude(', 'pub fn add_saved(', 'pub fn remove_saved(',
           'pub fn add_history(', 'pub fn remove_history(', 'pub fn set_scope(',
           'pub fn set_sort(', 'pub fn active_count(', 'pub fn matches(',
           'pub fn apply(', 'pub fn field(', 'pub fn fields(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('}'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')

find_count = prod.count('self.conditions.iter_mut().find(|c| c.id == id)')
if find_count < 3:
    fail('single_item_mutation_count=%d' % find_count)
match_body = body_after('pub fn matches(', '    }')
if not match_body or 'self.conditions.iter().filter(|x| x.enabled)' not in match_body:
    fail('and_semantics_missing')
if 'for cond in self.conditions.iter() {' in match_body:
    fail('disabled_condition_not_skipped')
apply_body = body_after('pub fn apply(', '    }')
if not apply_body or 'idx.sort_by(' not in apply_body or 'self.matches(&items[i])' not in apply_body:
    fail('derived_sort_missing')
if 'for_all' in prod or 'confirm_all' in prod:
    fail('batch_mutation_present')
if 'self.conditions.iter().any(|c| c.id == id)' not in prod:
    fail('duplicate_id_not_rejected')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, FILTER_TARGET)' not in prod:
    fail('event_not_unified_envelope')
if 'e.field("ids"), None' not in tests or 'e.field("values"), None' not in tests or 'e.field("text"), None' not in tests:
    fail('user_text_leaks_into_event')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')

api = (ROOT / 'src/api.rs').read_text()
if 'search_filter' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX16", name: "cn_search_filter", state: AxState::(\w+)', ax)
if not m or m.group(1) != 'DataLayer':
    fail('ax16_not_data_layer')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX16'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.search_filter"' not in boot:
    fail('module_not_in_boot_diagnostics')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'search-filter.json' in p.read_text():
        fail('ui_surface ' + rel)

print('SEARCH_FILTER_GUARD_OK keys=7 condition_keys=5 sort_keys=2 scopes=2 '
      'dimensions=5 ops=4 bad_inputs=21 opaque_text expected_tables '
      'two_impl_literals_match alias_reused derived_filter_and_sort '
      'v1_unchanged ax16=DataLayer')

#!/usr/bin/env python3
"""080：AX21 局域网互传通道协议数据层；不建监听、不写端点、不扩 v1。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('LAN_CHANNEL_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/lan_channel.rs'
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
               'reqwest', 'remove_dir_all', 'fs::remove_file']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
for banned in ['CHANNEL_TABLE', 'TRANSITION_TABLE', 'FIELD_TABLE', 'STEP_CATALOG',
               'cmp_precedence', 'semver', 'Version::parse', 'url', 'token', 'uuid',
               'texture', 'png', 'minecraft:', 'give ', 'regex', 'glob',
               'AIProvider', 'WikiEntries', '\u00a7']:
    if banned in prod:
        fail('external_or_duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')
if prod.count('robust::safe_join') < 2:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'let mut lines: Vec<String> = Vec::new();' not in prod:
    fail('explicit_vec_type_missing')
if 'let mut out: Vec<\u0026\u0027static str> = Vec::new();' not in prod:
    fail('explicit_str_vec_type_missing')

# A270：五张常量表用显式 EXPECTED 集合逐值比对
EXPECTED = {
    'KNOWN_KEYS': {'schema', 'stage', 'method', 'direction', 'room_id', 'pair_code', 'channel_open'},
    'MESSAGE_KINDS': {'request', 'response', 'event'},
    'STAGES': {'discover', 'pair', 'transfer', 'close'},
    'METHODS': {'qr', 'link_code'},
    'DIRECTIONS': {'pc_to_phone', 'phone_to_pc'},
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

# TRANSITIONS 六对与 STAGE_FIELDS 四段逐值比对
tr = re.search(r'pub const TRANSITIONS:\s*&\[\(&str, &str\)\]\s*=\s*&\[(.*?)\];', prod, re.S)
if not tr:
    fail('TRANSITIONS_parse_failed')
pairs = re.findall(r'\("([a-z_]+)",\s*"([a-z_]+)"\)', tr.group(1))
EXPECTED_PAIRS = {('discover', 'pair'), ('pair', 'transfer'), ('transfer', 'close'),
                  ('pair', 'discover'), ('transfer', 'pair'), ('close', 'discover')}
if len(pairs) != 6 or set(pairs) != EXPECTED_PAIRS:
    fail('TRANSITIONS_values=' + str(pairs))
sf = re.search(r'pub const STAGE_FIELDS:\s*&\[\(&str, &\[&str\]\)\]\s*=\s*&\[(.*?)\n\];', prod, re.S)
if not sf:
    fail('STAGE_FIELDS_parse_failed')
segments = re.findall(r'\("([a-z_]+)",\s*&\[', sf.group(1))
if segments != ['discover', 'pair', 'transfer', 'close']:
    fail('STAGE_FIELDS_segments=' + str(segments))
for key in ['"pair_code", "room_id"', '"direction", "channel_open"', '"stage", "channel_open"']:
    if key not in sf.group(1):
        fail('STAGE_FIELDS_fields_missing ' + key)

# A247：显式复用既有文本上限常量，删 import 行要真 FAIL
if 'use crate::core::robust;' not in prod:
    fail('robust_import_missing')
if prod.count('robust::MAX_TEXT_BYTES') < 2:
    fail('text_bound_not_reused count=%d' % prod.count('robust::MAX_TEXT_BYTES'))
if 'robust::read_or_default(&path, DEFAULT_STATE)' not in prod:
    fail('read_or_default_not_reused')

# A269：四个 impl 段里 code()/parse() 的字面量与各自常量表逐值一致
for enum_name, table in [('MessageKind', 'MESSAGE_KINDS'), ('LinkStage', 'STAGES'),
                         ('PairMethod', 'METHODS'), ('TransferDirection', 'DIRECTIONS')]:
    m = re.search(r'impl ' + enum_name + r' \{(.*?)\n\}', prod, re.S)
    if not m:
        fail(enum_name + '_impl_parse_failed')
    impl = m.group(1)
    code_vals = set(re.findall(r'=> "([a-z_]+)"', impl))
    parse_vals = set(re.findall(r'"([a-z_]+)" =>', impl))
    if code_vals != parsed[table] or parse_vals != parsed[table]:
        fail(enum_name + '_literals_mismatch code=%s parse=%s expected=%s'
             % (sorted(code_vals), sorted(parse_vals), sorted(parsed[table])))
for fn in ['LinkStage::parse', 'PairMethod::parse', 'TransferDirection::parse']:
    if fn not in prod:
        fail('enum_parse_not_explicit ' + fn)
if 'MessageKind::parse' not in tests:
    fail('message_kind_parse_not_exercised')
if 'pub fn message_kind_for(' not in prod:
    fail('message_kind_producer_missing')

# 坏输入标签
for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'bad_stage', 'bad_method', 'direction_not_text', 'bad_direction',
          'bad_room_id', 'bad_pair_code', 'channel_not_bool', 'bad_stage_state_pair',
          'direction_too_large',
          'in_memory', 'path_rejected', 'missing_or_unreadable', 'too_large', 'no_root']:
    if c not in prod:
        fail('bad_input_missing ' + c)
for const in ['MAX_FILE_BYTES', 'DEFAULT_STATE', 'EVENT_TARGET']:
    if const not in prod:
        fail('bound_missing ' + const)
for bound in ['METHODS.contains(&method.code())',
              'DIRECTIONS.contains(&direction.code())',
              'can_transition(self.stage, to)']:
    if bound not in prod:
        fail('set_bound_missing ' + bound)

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

# 八个纯函数段不读文件
for fn in ['pub fn can_transition(', 'pub fn stage_fields(', 'pub fn next_stages(',
           'pub fn message_kind_for(', 'pub fn field_allowed(',
           'pub fn pair_ready(', 'pub fn channel_usable(', 'pub fn summary(']:
    body = body_after(fn, '}')
    if not body or not body.rstrip().endswith('}'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + 'writes_user_files')
state_body = body_after('fn state_consistent(', '}')
if not state_body or 'fs::' in state_body:
    fail('state_consistent_not_pure')
for check in ['pair_code.is_empty()', 'direction.is_none()', '!channel_open',
              'LinkStage::Close || stage == LinkStage::Discover']:
    if check not in state_body:
        fail('parse_pair_check_missing ' + check)

# 矛盾态三处
if 'fn state_consistent(' not in prod or 'bad_stage_state_pair' not in prod:
    fail('parse_pair_check_label_missing')
sp = body_after('pub fn set_stage(', '    }')
if not sp or '!self.pair_ready()' not in sp or 'self.direction.is_none()' not in sp:
    fail('set_stage_pair_check_missing')
co = body_after('pub fn set_channel_open(', '    }')
if not co or 'self.direction.is_none()' not in co or '!self.pair_ready()' not in co:
    fail('set_channel_open_pair_check_missing')
pc = body_after('pub fn set_pair_code(', '    }')
if not pc or 'code.is_empty()' not in pc:
    fail('set_pair_code_pair_check_missing')

# 六个单条突变入口，无批量
for fn in ['pub fn set_stage(', 'pub fn set_method(', 'pub fn set_direction(',
           'pub fn clear_direction(', 'pub fn set_room_id(', 'pub fn set_pair_code(',
           'pub fn set_channel_open(']:
    if fn not in prod:
        fail('single_mutation_missing ' + fn)
if 'for_all' in prod or 'confirm_all' in prod:
    fail('batch_mutation_present')
if 'TRANSITIONS.iter().any(' not in prod:
    fail('transition_table_not_queried')
if 'stage_fields(stage).contains(&field)' not in prod:
    fail('field_table_not_queried')

write_body = body_after('fn write(', '}')
if not write_body or 'fs::rename(&tmp, &path)' not in write_body:
    fail('atomic_write_missing')
if 'Envelope::new(Kind::Event, EVENT_TARGET)' not in prod:
    fail('event_not_unified_envelope')
for key in ['room_id', 'pair_code']:
    if 'e.field("%s"), None' % key not in tests and 'for key in ["room_id", "pair_code"]' not in tests:
        fail('user_text_leaks_into_event ' + key)
if 'assert_eq!(e.field(key), None);' not in tests:
    fail('user_text_assertion_loop_missing')
if 'assert_eq!(e.payload.len(), 10);' not in tests:
    fail('event_payload_count_missing')
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
for key in ['"schema": 1', '"stage": p.stage.code()', '"method": p.method.code()',
            '"direction": direction', '"room_id": p.room_id', '"pair_code": p.pair_code',
            '"channel_open": p.channel_open']:
    if key not in prod:
        fail('serialize_key_missing ' + key)

api = (ROOT / 'src/api.rs').read_text()
if 'lan_channel' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX21", name: "redstone_multiplayer", state: AxState::(\w+), conflict: "([a-z_]*)"', ax)
if not m or m.group(1) != 'DataLayer' or m.group(2) != '':
    fail('ax21_state_or_conflict_changed')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX21'" not in axg:
    fail('ax_guard_not_extended')
if 'planned = sum(' not in axg:
    fail('ax_guard_not_dynamic')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.lan_channel"' not in boot:
    fail('module_not_in_boot_diagnostics')
ci = (ROOT / '.github/workflows/ci.yml').read_text()
if 'name: lan_channel_guard' not in ci:
    fail('ci_step_missing')
for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'lan-channel.json' in p.read_text():
        fail('ui_surface ' + rel)

print('LAN_CHANNEL_GUARD_OK keys=7 kinds=3 stages=4 methods=2 directions=2 '
      'transitions=6 field_segments=4 bad_inputs=23 opaque_text expected_tables '
      'four_impl_literals_match robust_reused pair_checks_three pure_queries '
      'v1_unchanged ax21=DataLayer conflict_empty')

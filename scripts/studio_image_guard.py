#!/usr/bin/env python3
"""091：AX15 Studio 图片编辑会话、两目标槽位与像素区间；零字节持有、不扩 v1。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(reason):
    print('STUDIO_IMAGE_GUARD_FAIL reason=' + reason)
    sys.exit(1)


f = ROOT / 'src/core/studio_image.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

HTTP = 'ht' + 'tp://'
HTTPS = 'ht' + 'tps://'
LOOPBACK = '127' + '.0.0.1'
TOKEN = 'To' + 'ken'
for banned in ['TcpListener', 'TcpStream', 'bind(', LOOPBACK, '/mcp', TOKEN,
               'SystemTime', 'UNIX_EPOCH', 'std::process::Command', HTTP, HTTPS,
               'reqwest', 'remove_dir_all', 'fs::remove_file', 'x-api-key',
               'ZipArchive', 'zip::', 'flate2', 'nbt', 'vianbt',
               'minecraft:', 'give ', '\u00a7', '.jar', '.litematic', '.schem']:
    if banned in prod:
        fail('forbidden_literal ' + repr(banned))
for banned in ['image::', 'use image', 'resvg', 'usvg', 'png::', 'gif::', 'svg::',
               'include_bytes!', 'Vec<u8>', 'fs::read(', 'base64', 'libpng',
               'lodepng', 'jpeg', 'bmp', 'tiff', 'decode(']:
    if banned in prod:
        fail('image_bytes_or_library ' + repr(banned))
for banned in ['undo', 'redo', 'MAX_HISTORY', 'push_layer',
               'ViewMode', 'scaled', 'original', 'projection.preview',
               'EDITOR_TABLE', 'FIELD_TABLE', 'LICENSE_TABLE', 'STEP_CATALOG',
               'url', 'uuid', 'texture', 'AIProvider', 'WikiEntries']:
    if banned in prod:
        fail('duplicated_logic ' + repr(banned))
if '.unwrap()' in prod or '.expect(' in prod or 'unwrap_or' in prod:
    fail('unchecked_unwrap_present')

EXPECTED = {
    'ROOT_KEYS': {'schema', 'session', 'entries'},
    'ENTRY_KEYS': {'id', 'format', 'path', 'target_px', 'fit', 'state', 'decided'},
    'IMAGE_FORMATS': {'png', 'gif', 'svg', 'opaque'},
    'STATES': {'draft', 'adjusted', 'closed'},
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

m = re.search(r'pub const PATH_KINDS:\s*&\[\(&str,\s*&str\)\]\s*=\s*&\[(.*?)\];', prod, re.S)
if not m:
    fail('PATH_KINDS_parse_failed')
pairs = re.findall(r'\("([a-z]+)",\s*"([a-z_]+)"\)', m.group(1))
if pairs != [('logo', 'logo'), ('icon', 'icon')]:
    fail('PATH_KINDS_values=' + str(pairs))
if set(c for _, c in pairs) != {'logo', 'icon'}:
    fail('two_target_slots_not_both_registered')

if 'obj.keys().any(|k| !ROOT_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_root_key_not_rejected')
if 'io.keys().any(|k| !ENTRY_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_entry_key_not_rejected')

for lit in ['use crate::core::robust;',
            'use crate::core::diagnostics::diag_line;',
            'use crate::core::envelope::{Envelope, Kind};']:
    if lit not in prod:
        fail('import_missing ' + lit)
for bound in ['robust::MAX_TEXT_BYTES', 'robust::MAX_PATH_BYTES',
              'robust::MAX_ID_BYTES', 'robust::MAX_REL_DEPTH']:
    if bound not in prod:
        fail('bound_not_reused ' + bound)
if prod.count('robust::safe_join') < 3:
    fail('path_not_centralised count=%d' % prod.count('robust::safe_join'))
if 'robust::read_or_default(&path, DEFAULT_STATE)' not in prod:
    fail('read_or_default_not_reused')

for decl in ['let mut lines: Vec<String> = Vec::new();',
             'let mut parts: Vec<String> = Vec::new();',
             'let mut items: Vec<ImageEntry> = Vec::new();',
             'let mut out: Vec<&str> = Vec::new();',
             'let entries: Vec<Value> = p.entries.iter()']:
    if decl not in prod:
        fail('explicit_vec_type_missing ' + repr(decl))

for enum_name, table in [('ImageFormat', 'IMAGE_FORMATS'), ('EditState', 'STATES')]:
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
for fn in ['ImageFormat::parse', 'EditState::parse']:
    if fn not in prod:
        fail('enum_parse_not_explicit ' + fn)
for bound in ['and_then(ImageFormat::parse)', 'and_then(EditState::parse)']:
    if bound not in prod:
        fail('parse_entry_missing ' + bound)


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


vp = body_after('fn validate_entry_path(', '}')
if not vp or not vp.rstrip().endswith('}'):
    fail('validate_entry_path_body_parse_failed')
for lit in ['Component::Normal(part)',
            'Component::CurDir | Component::ParentDir | Component::RootDir | Component::Prefix(_)',
            'Path::new(s).components()', 'robust::MAX_REL_DEPTH',
            'parts.is_empty()', 'PATH_KINDS.iter().any(']:
    if lit not in vp:
        fail('component_check_missing ' + lit)
for banned in ['replace(', 'strip_prefix(', 'contains("..")', 'fs::', 'std::fs',
               '.unwrap()', '.expect(', 'unwrap_or']:
    if banned in vp:
        fail('path_cleaning_or_write_present ' + repr(banned))
if prod.count('validate_entry_path(path)') < 2:
    fail('validate_entry_path_not_called count=%d' % prod.count('validate_entry_path(path)'))
if '.and_then(validate_entry_path)' not in prod:
    fail('parse_path_validation_missing')

cp = body_after('fn classify_target(', '}')
if not cp or not cp.rstrip().endswith('}'):
    fail('classify_target_body_parse_failed')
for lit in ['path.split', 'for (prefix, code) in PATH_KINDS {']:
    if lit not in cp:
        fail('classify_literal_missing ' + lit)

ic = body_after('fn entry_consistent(', '}')
if not ic or not ic.rstrip().endswith('}'):
    fail('entry_consistent_body_parse_failed')
for check in ['i.state == EditState::Closed && !i.decided',
              'i.decided && i.state == EditState::Draft',
              'i.state == EditState::Adjusted && !i.fit',
              'i.format == ImageFormat::Opaque && i.fit',
              'i.target_px < MIN_PIXEL || i.target_px > MAX_PIXEL']:
    if not re.search(re.escape(check) + r'(?!\w)', ic):
        fail('entry_consistent_check_missing ' + check)
calls = prod.count('entry_consistent(&')
if calls != 8:
    fail('entry_consistent_calls=%d expected=8' % calls)

for fn in ['pub fn entry_count(', 'pub fn draft_count(', 'pub fn adjusted_count(',
           'pub fn closed_count(', 'pub fn by_format(', 'pub fn by_target(',
           'pub fn format_for(', 'pub fn summary(']:
    body = body_after(fn, '    }')
    if not body or not body.rstrip().endswith('    }'):
        fail(fn + '_body_parse_failed')
    if 'fs::' in body or 'std::fs' in body:
        fail(fn + '_writes_user_files')

for c in ['not_json', 'root_not_object', 'unknown_key', 'schema_invalid',
          'bad_session', 'entries_not_array', 'entries_too_many',
          'entry_not_object', 'entry_unknown_key', 'id_too_large', 'bad_id',
          'duplicate_id', 'bad_format', 'path_escapes_root', 'bad_target_px',
          'bad_fit', 'bad_state', 'bad_decided', 'bad_entry_state', 'in_memory',
          'path_rejected', 'missing_or_unreadable', 'too_large', 'no_root']:
    if not re.search(r'\b' + re.escape(c) + r'(?!\w)', prod):
        fail('bad_input_missing ' + c)
for const in ['MAX_FILE_BYTES', 'MAX_ENTRIES', 'MIN_PIXEL', 'MAX_PIXEL',
              'DEFAULT_PIXEL', 'DEFAULT_STATE', 'EVENT_TARGET',
              'STUDIO_IMAGE_FILE', 'TMP_SUFFIX']:
    if not re.search(r'\b' + re.escape(const) + r'\b', prod):
        fail('bound_missing ' + const)

for fn in ['pub fn add_entry(', 'pub fn set_format(', 'pub fn set_target_px(',
           'pub fn set_fit(', 'pub fn set_state(', 'pub fn set_decided(',
           'pub fn set_path(', 'pub fn remove_entry(']:
    if fn not in prod:
        fail('single_mutation_missing ' + fn)
for banned in ['mark_all', 'accept_all', 'resolve_all', 'confirm_all',
               'preview_all', 'undo_all', 'redo_all']:
    if banned in prod:
        fail('batch_mutation_present ' + banned)

for lit in ['fs::write(&tmp, body)?;', 'fs::rename(&tmp, &path)?;',
            'Envelope::new(Kind::Event, EVENT_TARGET)']:
    if lit not in prod:
        fail('atomic_write_or_envelope_missing ' + lit)
ce = body_after('pub fn change_event(', '    }')
if not ce or not ce.rstrip().endswith('    }'):
    fail('change_event_body_parse_failed')
payload_keys = re.findall(r'\.with\("([a-z_]+)",', ce)
PAYLOAD_EXPECTED = {'entries', 'session', 'draft', 'adjusted', 'closed',
                    'logo', 'icon', 'formats', 'targets', 'pixel_bounds'}
if len(payload_keys) != 10 or set(payload_keys) != PAYLOAD_EXPECTED:
    fail('event_payload_keys=' + str(payload_keys))
for banned in ['.path', '.id', 'i.id', 'i.path']:
    if banned in ce:
        fail('user_text_in_event_payload ' + repr(banned))

api = (ROOT / 'src/api.rs').read_text()
lines = [l.strip() for l in api.splitlines() if l.strip().startswith('pub use crate::')]
syms = set()
for l in lines:
    tail = l.split('::')[-1].rstrip(';').strip()
    if tail.startswith('{') and tail.endswith('}'):
        syms.update(x.strip() for x in tail[1:-1].split(','))
    else:
        syms.add(tail)
WHITELIST = {'CancelToken', 'Envelope', 'Kind', 'CloseAction',
             'PopupOpenError', 'PopupRegistry', 'ClientAiGate'}
if syms != WHITELIST:
    fail('v1_surface_changed got=' + ','.join(sorted(syms)))

mod = (ROOT / 'src/core/mod.rs').read_text()
if 'pub mod studio_image;' not in mod:
    fail('module_declaration_missing')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.studio_image",' not in boot:
    fail('boot_module_missing')
if boot.index('"core.studio_image",') > boot.index('"dispatcher.launcher",'):
    fail('boot_module_after_dispatcher')
ci = (ROOT / '.github/workflows/ci.yml').read_text()
if not re.search(r'^\s*- name: studio_image_guard\s*$', ci, re.M) or \
        'python3 scripts/studio_image_guard.py' not in ci:
    fail('ci_step_missing')

ax = (ROOT / 'src/core/ax.rs').read_text()
ax_row = re.search(r'AxSpec \{ id: "AX15", name: "([a-z_]+)", state: AxState::(\w+), conflict: "([^"]*)"', ax)
if not ax_row:
    fail('ax15_row_missing')
if ax_row.group(1) != 'studio_image_editor' or ax_row.group(2) != 'DataLayer' or ax_row.group(3) != '':
    fail('ax15_state_mismatch name=%s state=%s conflict=%s' % ax_row.groups())
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX15'" not in axg:
    fail('ax_guard_explicit_assert_missing')
if 'planned = sum(' not in axg or 'data = sum(' not in axg:
    fail('ax_guard_not_dynamic')
for ax_id, state, conflict in [('AX07', 'Planned', 'network_io_not_started'),
                               ('AX22', 'Planned', ''),
                               ('AX15', 'DataLayer', '')]:
    row = re.search(r'AxSpec \{ id: "' + ax_id + r'", name: "([a-z_]+)", state: AxState::(\w+), conflict: "([^"]*)"', ax)
    if not row or row.group(2) != state or row.group(3) != conflict:
        fail('a230_conflict_not_recorded ' + ax_id)

for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'studio-image.json' in p.read_text():
        fail('ui_surface ' + rel)

print('STUDIO_IMAGE_GUARD_OK root_keys=3 entry_keys=7 formats=4 states=3 '
      'path_kinds=2 two_impl_literals_match component_path_check '
      'consistent_checks_five calls=%d pure_queries event_payload=%d '
      'v1_unchanged ax15=DataLayer a230_conflicts_recorded'
      % (calls, len(payload_keys)))

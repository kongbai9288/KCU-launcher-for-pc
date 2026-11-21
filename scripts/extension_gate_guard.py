#!/usr/bin/env python3
"""067：扩展包安装门禁；锁位注册表单一源；两进程信封配对；无真实进程/端口/时钟。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('EXTENSION_GATE_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/extension_gate.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', '127.0.0.1', 'SystemTime', 'UNIX_EPOCH', 'std::process::Command', 'http://', 'https://']:
    if banned in prod:
        fail('real_ipc_or_clock_present ' + banned)
if 'remove_dir_all' in prod or 'fs::remove_file' in prod:
    fail('bulk_delete_present')
if '.unwrap()' in prod or '.expect(' in prod:
    fail('unchecked_unwrap_present')
if 'robust::safe_join' not in prod:
    fail('path_not_centralised')

slots = re.search(r'EXTENSION_SLOTS:\s*&\[ExtensionSlot\]\s*=\s*&\[(.*?)\n\];', prod, re.S)
if not slots:
    fail('slot_table_missing')
rows = [r for r in re.findall(r'ExtensionSlot \{([^}]*)\}', slots.group(1)) if 'slot_id:' in r]
if len(rows) != 5:
    fail('slot_count=' + str(len(rows)))
ids = re.findall(r'slot_id:\s*"([^"]+)"', slots.group(1))
exts = re.findall(r'extension_id:\s*"([^"]+)"', slots.group(1))
if len(set(ids)) != 5 or len(set(exts)) != 5:
    fail('slot_ids_not_unique')
if 'headless.kculf' not in ids:
    fail('kculf_slot_missing')
for r in rows:
    if 'LOCK_POPUP_ID' not in r:
        fail('slot_without_registered_popup')

if 'open_registered(' not in prod:
    fail('lock_click_not_using_registry')
if 'pub const LOCK_POPUP_ID: &str = "extension"' not in prod:
    fail('popup_id_mismatch')
pop = (ROOT / 'src/core/popup.rs').read_text()
if 'id: "extension"' not in pop:
    fail('extension_popup_not_registered')

checks = ['kind != Kind::Response', 'response.target != INSTALL_TARGET', '!response.ok()',
          'unknown_or_replayed_request_id', 'extension_id_mismatch', 'timeout', 'pending_full']
for c in checks:
    if c not in prod:
        fail('ipc_check_missing ' + c)
if 'self.pending.remove(&response.request_id)' not in prod:
    fail('replay_not_consumed')
if 'Envelope::new(Kind::Request, INSTALL_TARGET)' not in prod:
    fail('request_not_unified_envelope')

if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
api = (ROOT / 'src/api.rs').read_text()
if 'extension_gate' in api or 'launch_progress' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4 or sum(1 for l in lines if 'ClientAiGate' in l) != 1:
    fail('v1_port_count=' + str(len(lines)))

boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.extension_gate"' not in boot:
    fail('module_not_in_boot_diagnostics')

for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'EXTENSION_SLOTS' in p.read_text():
        fail('ui_surface ' + rel)

print('EXTENSION_GATE_GUARD_OK slots=5 popup=extension ipc_checks=8 v1_unchanged no_real_ipc')

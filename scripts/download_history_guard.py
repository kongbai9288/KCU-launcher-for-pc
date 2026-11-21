#!/usr/bin/env python3
"""066：AX06 下载历史为纯本地数据层；无网络、无 UI、不扩公共面、不删保护文件。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('DOWNLOAD_HISTORY_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/download_history.rs'
t = f.read_text().split('#[cfg(test)]')[0]

if 'remove_dir_all' in t:
    fail('bulk_delete_present')
if 'fs::remove_file' in t:
    fail('file_delete_present')
for banned in ['TcpStream', 'TcpListener', 'reqwest', 'http://', 'https://', 'SystemTime', 'UNIX_EPOCH']:
    if banned in t:
        fail('network_or_clock_present ' + banned)
if '.unwrap()' in t or '.expect(' in t:
    fail('unchecked_unwrap_present')
if 'robust::safe_join' not in t:
    fail('path_not_centralised')
if 'DEFAULT_HISTORY' not in t or 'fs::rename(&tmp, &path)' not in t:
    fail('atomic_write_missing')

kinds = re.search(r'KINDS:\s*&\[&str\]\s*=\s*&\[([^\]]*)\]', t)
results = re.search(r'RESULTS:\s*&\[&str\]\s*=\s*&\[([^\]]*)\]', t)
if not kinds or not results:
    fail('closed_tables_missing')
for k in ['game', 'mod', 'modpack', 'resourcepack', 'shaderpack', 'datapack']:
    if '"' + k + '"' not in kinds.group(1):
        fail('kind_missing ' + k)
for r in ['ok', 'failed', 'cancelled']:
    if '"' + r + '"' not in results.group(1):
        fail('result_missing ' + r)

tests = f.read_text().split('#[cfg(test)]')[1] if '#[cfg(test)]' in f.read_text() else ''
if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
api = (ROOT / 'src/api.rs').read_text()
if 'download_history' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4 or sum(1 for l in lines if 'ClientAiGate' in l) != 1:
    fail('v1_port_count=' + str(len(lines)))

boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.download_history"' not in boot:
    fail('module_not_in_boot_diagnostics')

ax = (ROOT / 'src/core/ax.rs').read_text()
row = [r for r in ax.splitlines() if 'id: "AX06"' in r]
if not row or 'AxState::DataLayer' not in row[0]:
    fail('ax06_not_data_layer')

for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'download_history' in p.read_text():
        fail('ui_surface ' + rel)

print('DOWNLOAD_HISTORY_GUARD_OK local_only no_network no_ui v1_unchanged ax06=DataLayer')

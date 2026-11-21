#!/usr/bin/env python3
"""069：AX12 下载来源策略数据层；密钥只留布尔；缺失降级镜像；严格白名单；不扩 v1。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('DOWNLOAD_SOURCES_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/download_sources.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]
tests = t.split('#[cfg(test)]')[1] if '#[cfg(test)]' in t else ''

for banned in ['TcpListener', 'TcpStream', 'bind(', '127.0.0.1', 'SystemTime', 'UNIX_EPOCH',
               'std::process::Command', 'http://', 'https://', 'CurseForge', 'ghp_', 'github_pat_',
               'x-api-key', 'mcim']:
    if banned in prod:
        fail('forbidden_literal ' + banned)
if 'remove_dir_all' in prod or 'fs::remove_file' in prod:
    fail('bulk_delete_present')
if '.unwrap()' in prod or '.expect(' in prod:
    fail('unchecked_unwrap_present')
if 'robust::safe_join' not in prod:
    fail('path_not_centralised')

if 'pub const KNOWN_KEYS' not in prod:
    fail('known_keys_table_missing')
keys = re.search(r'KNOWN_KEYS:\s*&\[&str\]\s*=\s*&\[(.*?)\];', prod, re.S)
if not keys:
    fail('known_keys_parse_failed')
ks = re.findall(r'"([a-z_]+)"', keys.group(1))
if len(ks) != 6 or len(set(ks)) != 6:
    fail('known_keys=' + str(ks))
if 'obj.keys().any(|k| !KNOWN_KEYS.contains(&k.as_str()))' not in prod:
    fail('unknown_key_not_rejected')

for c in ['not_json', 'root_not_object', 'schema_invalid', 'unknown_key', 'tier_invalid',
          'concurrent_invalid', 'flag_invalid', 'restricted_not_array', 'too_large']:
    if c not in prod:
        fail('bad_input_missing ' + c)
if 'key_absent_downgrade_mirror' not in prod:
    fail('key_downgrade_missing')
if 'SourceTier::AutoMirror' not in prod or 'SourceKind::Mirror' not in prod:
    fail('default_mirror_missing')
if 'key_present' not in prod or 'DEFAULT_SOURCES' not in prod:
    fail('key_state_missing')
if 'pub fn effective_plan(' not in prod:
    fail('plan_missing')
if 'Envelope::new(Kind::Event, SOURCES_TARGET)' not in prod:
    fail('event_not_unified_envelope')

if 'use crate::core::settings_io::PROTECTED_FILES;' not in tests:
    fail('protected_table_not_reused')
api = (ROOT / 'src/api.rs').read_text()
if 'download_sources' in api:
    fail('v1_surface_expanded')
lines = [l for l in api.splitlines() if l.strip().startswith('pub use crate::')]
if len(lines) != 4:
    fail('v1_port_count=' + str(len(lines)))

ax = (ROOT / 'src/core/ax.rs').read_text()
m = re.search(r'AxSpec \{ id: "AX12", name: "download_sources", state: AxState::(\w+)', ax)
if not m or m.group(1) != 'DataLayer':
    fail('ax12_not_data_layer')
if 'count_by_state(AxState::Planned), 19' not in ax:
    fail('ax_planned_count_not_updated')
axg = (ROOT / 'scripts/ax_guard.py').read_text()
if "'AX12'" not in axg:
    fail('ax_guard_not_extended')

boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.download_sources"' not in boot:
    fail('module_not_in_boot_diagnostics')

for rel in ['demos/ui-full-kcu-paper.html', 'demos/lang/zh-CN.js', 'demos/lang/en-US.js']:
    p = ROOT / rel
    if p.is_file() and 'download-sources.json' in p.read_text():
        fail('ui_surface ' + rel)

print('DOWNLOAD_SOURCES_GUARD_OK keys=6 bad_inputs=9 key_downgrade=1 v1_unchanged ax12=DataLayer')

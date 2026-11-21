#!/usr/bin/env python3
"""065：AX11 设置导入导出与清理；清理不得抹掉隐私同意与状态文件。"""
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('SETTINGS_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/settings_io.rs'
t = f.read_text().split('#[cfg(test)]')[0]

import re
table = re.search(r'PROTECTED_FILES:\s*&\[&str\]\s*=\s*&\[([^\]]*)\]', t)
if not table:
    fail('protected_table_missing')
for name in ['CONSENT_FILE', 'STATE_FILE', 'BUNDLE_FILE', 'STATS_FILE']:
    if name not in table.group(1):
        fail('protected_constant_missing ' + name)
if 'remove_dir_all' in t:
    fail('bulk_delete_present')
if 'pub fn is_protected(' not in t or 'pub fn reject_protected_removal(' not in t:
    fail('protection_api_missing')
if 'PROTECTED_FILES.contains(&name)' not in t:
    fail('is_protected_not_table_driven')
if 'fs::rename(&tmp, &path)' not in t:
    fail('atomic_write_missing')
if 'DERIVED_KEYS' not in t or 'if DERIVED_KEYS.contains(&key.as_str())' not in t:
    fail('derived_key_not_excluded_from_export')
if 'unknown_key' not in t or 'control_char' not in t:
    fail('bad_input_visible_missing')

cfg = (ROOT / 'src/core/config.rs').read_text()
if 'pub struct Config' not in cfg:
    fail('config_missing')

consent = (ROOT / 'src/core/consent.rs').read_text()
if 'privacy-consent.json' not in consent:
    fail('consent_filename_changed')

boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.settings_io"' not in boot:
    fail('module_not_in_boot_diagnostics')

ax = (ROOT / 'src/core/ax.rs').read_text()
row = [r for r in ax.splitlines() if 'id: "AX11"' in r]
if not row or 'AxState::DataLayer' not in row[0]:
    fail('ax11_not_data_layer')

print('SETTINGS_GUARD_OK protected=4 no_bulk_delete atomic_write derived_excluded ax11=DataLayer')

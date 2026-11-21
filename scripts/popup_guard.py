#!/usr/bin/env python3
"""062：弹窗唯一声明源与注册表行为。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(reason):
    print('POPUP_GUARD_FAIL reason=' + reason)
    sys.exit(1)


p = (ROOT / 'src/core/popup.rs').read_text()
rows = [r for r in re.findall(r'PopupSpec \{([^}]*)\}', p) if 'id: "' in r]
if len(rows) != 13:
    fail('spec_count=' + str(len(rows)))
ids = re.findall(r'id:\s*"([^"]+)"', p)
if len(ids) != 13 or len(set(ids)) != 13:
    fail('spec_ids_not_unique count=' + str(len(ids)) + ' unique=' + str(len(set(ids))))
for r in rows:
    if not re.search(r'button: true|escape: true|cancel: true|special: Some', r):
        fail('spec_without_close_path ' + r.strip()[:40])
if 'POPUP_SPECS.iter().map(Popup::from_spec)' not in p:
    fail('catalog_not_derived_from_specs')
if 'ok_or(PopupOpenError::UnknownId)' not in p:
    fail('unknown_id_not_rejected')
others = [
    str(x.relative_to(ROOT))
    for x in (ROOT / 'src').rglob('*.rs')
    if x.name != 'popup.rs' and 'PopupSpec' in x.read_text()
]
if others:
    fail('spec_table_duplicated ' + ','.join(others))

print('POPUP_GUARD_OK specs=13 ids_unique=13 close_path=all catalog_derived unknown_rejected')

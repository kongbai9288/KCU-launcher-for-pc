#!/usr/bin/env python3
"""062：crate 顶层不把内部类型平铺成共有 API；稳定面只走 api::v1；业务模块不散落构造弹窗。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(reason):
    print('API_GUARD_FAIL reason=' + reason)
    sys.exit(1)


lib = (ROOT / 'src/lib.rs').read_text()
flat = [l for l in lib.splitlines() if re.match(r'^pub use ', l)]
if flat:
    fail('top_level_pub_use=' + str(len(flat)))

api = (ROOT / 'src/api.rs').read_text()
lines = [l.strip() for l in api.splitlines() if l.strip().startswith('pub use crate::')]
syms = set()
for l in lines:
    tail = l.split('::')[-1].rstrip(';').strip()
    if tail.startswith('{') and tail.endswith('}'):
        syms.update(x.strip() for x in tail[1:-1].split(','))
    else:
        syms.add(tail)
WHITELIST = {'CancelToken', 'Envelope', 'Kind', 'CloseAction', 'PopupOpenError', 'PopupRegistry', 'ClientAiGate'}
if syms != WHITELIST:
    fail('v1_surface_changed got=' + ','.join(sorted(syms)))

FORBIDDEN = ('Popup::new(', 'PopupKind::', 'catalog()')
hits = []
for p in (ROOT / 'src').rglob('*.rs'):
    if p.name == 'popup.rs':
        continue
    for i, l in enumerate(p.read_text().splitlines(), 1):
        for k in FORBIDDEN:
            if k in l:
                hits.append(str(p.relative_to(ROOT)) + ':' + str(i) + ' ' + k)
if hits:
    fail('scattered_popup_construction ' + '; '.join(hits[:5]))

print('API_GUARD_OK flat_pub_use=0 v1_symbols=' + str(len(syms)) + ' scattered=0')

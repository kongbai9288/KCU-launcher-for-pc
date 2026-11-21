#!/usr/bin/env python3
"""064：AX01-AX24 单一声明源、冲突裁决与状态分层。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('AX_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/ax.rs'
t = f.read_text()
rows = [r for r in re.findall(r'AxSpec \{([^}]*)\}', t) if 'id: "AX' in r]
if len(rows) != 24:
    fail('spec_count=' + str(len(rows)))
ids = re.findall(r'id:\s*"(AX\d\d)"', t)
if len(ids) != 24 or len(set(ids)) != 24 or set(ids) != {f'AX{i:02d}' for i in range(1, 25)}:
    fail('spec_ids')

def field(i, key):
    m = re.search(key + r':\s*([^,]+)', [r for r in rows if f'id: "{i}"' in r][0])
    return m.group(1).strip() if m else ''

if field('AX23', 'state') != 'AxState::GateOnly' or field('AX23', 'ui') != 'false':
    fail('ax23_not_gate_only')
if 'no_ui' not in field('AX23', 'conflict'):
    fail('ax23_conflict_missing')
for ax in ('AX05', 'AX06', 'AX11', 'AX12', 'AX24'):
    if field(ax, 'state') != 'AxState::DataLayer':
        fail(ax + '_not_data_layer')
if 'ai_provider_ui_excluded' not in field('AX18', 'conflict'):
    fail('ax18_excluded_subitem_missing')
planned = sum(1 for r in rows if 'AxState::Planned' in r)
data = sum(1 for r in rows if 'AxState::DataLayer' in r)
gate = sum(1 for r in rows if 'AxState::GateOnly' in r)
if planned + data + gate != 24 or gate != 1 or data < 1:
    fail('state_sum planned=%d data=%d gate=%d' % (planned, data, gate))

for p in (ROOT / 'src').rglob('*.rs'):
    if p.name != 'ax.rs' and 'AxSpec {' in p.read_text():
        fail('spec_table_duplicated ' + str(p.relative_to(ROOT)))

doc = (ROOT / 'docs/research/31-axolotl-launcher-features.md').read_text()
for i in range(1, 25):
    if f'AX{i:02d}' not in doc:
        fail('doc_missing AX' + f'{i:02d}')

print('AX_GUARD_OK specs=24 gate_only=%d data_layer=%d planned=%d' % (gate, data, planned))

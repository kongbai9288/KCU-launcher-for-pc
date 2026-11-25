#!/usr/bin/env python3
"""092：拍板清单完整性、不代拍、功能池状态不变；零 src 改动、不扩 v1。"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def fail(reason):
    print('PENDING_DECISIONS_GUARD_FAIL reason=' + reason)
    sys.exit(1)


def has(code, text):
    return re.search(r'(?<![\w-])' + re.escape(code) + r'(?![\w-])', text) is not None


env = (ROOT / 'docs/records/pending-question-environments.md').read_text()
m = re.search(r'^## 092 摊平\s*$', env, re.M)
if not m:
    fail('092_section_missing')
sec = env[m.end():]
nxt = re.search(r'^## ', sec, re.M)
if nxt:
    sec = sec[:nxt.start()]

EXPECTED = {
    'eq': {('EQ-%02d' % i) for i in range(1, 14)},
    'q091': {'Q-091-01', 'Q-091-02', 'Q-091-03'},
    'qc': {'Q-C01', 'Q-C02', 'Q-C08', 'Q-037-01'},
    'ax': {'AX07', 'AX22'},
    'anchor': {'12:63', '11:18', '11:7'},
}
for group, codes in EXPECTED.items():
    for code in sorted(codes):
        if not has(code, sec):
            fail('missing_code ' + group + ' ' + code)
eq_rows = set(re.findall(r'^\| (EQ-\d\d) \|[^\n]*\| 未证实（待拍板） \|$', sec, re.M))
if eq_rows != EXPECTED['eq']:
    fail('eq_table_rows=' + ','.join(sorted(eq_rows)))
for code in ('EQ-14', 'EQ-15'):
    if not has(code, sec):
        fail('closed_eq_not_recorded ' + code)
if 'EQ-14（048 新增 / 049 按选项②关闭）、EQ-15（048 新增 / 050 按选项①关闭）已关闭' not in sec:
    fail('eq14_eq15_closure_missing')

for banned in ('已拍板', '用户已选', '选中 ①', '决断为', '代为拍板', '默认选 ①'):
    if banned in sec:
        fail('author_decided_instead_of_user ' + banned)
if '待拍板' not in sec or '未证实' not in sec:
    fail('pending_state_not_echoed')
for anchor in ('### 已决断', '### 未决断'):
    if not re.search(r'^' + re.escape(anchor) + r'\s*$', sec, re.M):
        fail('a164_split_missing ' + anchor)
if '| 项 | 环境 | 选项 | 后果 | 耦合 |' not in sec:
    fail('a73_header_missing')
for element in ('环境', '选项', '后果', '耦合'):
    if element not in sec:
        fail('a73_element_missing ' + element)

ax = (ROOT / 'src/core/ax.rs').read_text()
row07 = re.search(r'AxSpec \{ id: "AX07", name: "([a-z_]+)", state: AxState::(\w+), conflict: "([^"]*)"', ax)
row22 = re.search(r'AxSpec \{ id: "AX22", name: "([a-z_]+)", state: AxState::(\w+), conflict: "([^"]*)"', ax)
if not row07 or row07.group(1) != 'doh_support' or row07.group(2) != 'Planned' or row07.group(3) != 'network_io_not_started':
    fail('ax07_state_or_conflict_changed')
if not row22 or row22.group(1) != 'shimu_account' or row22.group(2) != 'Planned' or row22.group(3) != '':
    fail('ax22_state_or_conflict_changed')

api = (ROOT / 'src/api.rs').read_text()
syms = set()
for line in api.splitlines():
    line = line.strip()
    if not line.startswith('pub use crate::'):
        continue
    tail = line.split('::')[-1].rstrip(';').strip()
    if tail.startswith('{') and tail.endswith('}'):
        syms.update(x.strip() for x in tail[1:-1].split(','))
    else:
        syms.add(tail)
if syms != {'CancelToken', 'Envelope', 'Kind', 'CloseAction',
            'PopupOpenError', 'PopupRegistry', 'ClientAiGate'}:
    fail('v1_surface_changed got=' + ','.join(sorted(syms)))

ci = (ROOT / '.github/workflows/ci.yml').read_text()
if not re.search(r'^\s*- name: pending_decisions_guard\s*$', ci, re.M) or \
        'python3 scripts/pending_decisions_guard.py' not in ci:
    fail('ci_step_missing')

dec_path = ROOT / 'docs/decisions/092-pending-decisions.md'
if not dec_path.is_file():
    fail('decision_file_missing')
dec = dec_path.read_text()
if not has('D-092-1', dec) or not has('D-092-9', dec):
    fail('a203_default_echo_missing')

print('PENDING_DECISIONS_GUARD_OK eq=13 q091=3 qc=4 ax=2 anchors=3 '
      'a164_split a73_elements no_author_decision ax_states_unchanged '
      'v1_unchanged ci_step a203_echo')

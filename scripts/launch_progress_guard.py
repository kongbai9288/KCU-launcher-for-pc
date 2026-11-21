#!/usr/bin/env python3
"""067：统一调度器→全量启动器加载阶段单调状态机；取消 0 副作用；事件走统一信封。"""
from pathlib import Path
import re, sys

ROOT = Path(__file__).resolve().parents[1]

def fail(reason):
    print('LAUNCH_PROGRESS_GUARD_FAIL reason=' + reason)
    sys.exit(1)

f = ROOT / 'src/core/launch_progress.rs'
t = f.read_text()
prod = t.split('#[cfg(test)]')[0]

phases = re.search(r'PHASES:\s*&\[\(&str,\s*u8\)\]\s*=\s*&\[(.*?)\n\];', prod, re.S)
if not phases:
    fail('phase_table_missing')
pairs = re.findall(r'\("([a-z_]+)",\s*(\d+)\)', phases.group(1))
if len(pairs) != 5:
    fail('phase_count=' + str(len(pairs)))
vals = [int(v) for _, v in pairs]
if vals[0] != 0 or vals[-1] != 100 or any(vals[i] > vals[i + 1] for i in range(len(vals) - 1)):
    fail('phase_not_monotonic')
if pairs[0][0] != 'dispatcher_start' or pairs[-1][0] != 'ui_ready':
    fail('phase_endpoints_wrong')

for c in ['non_monotonic', 'frozen', 'timeout', 'unknown_phase', 'ProgressState::Cancelled', 'ProgressState::Failed']:
    if c not in prod:
        fail('state_guard_missing ' + c)
ev = re.search(r'pub fn event\(&self\) -> Envelope \{(.*?)\n    \}', prod, re.S)
if not ev or 'Kind::Event' not in ev.group(1) or 'PROGRESS_TARGET' not in ev.group(1):
    fail('event_not_unified_envelope')
if 'pub fn cancel(' not in prod or 'pub fn fail(' not in prod:
    fail('cancel_or_fail_missing')

for banned in ['SystemTime', 'UNIX_EPOCH', 'std::fs', 'TcpListener', 'http://', 'https://']:
    if banned in prod:
        fail('side_effect_or_clock_present ' + banned)
if '.unwrap()' in prod or '.expect(' in prod:
    fail('unchecked_unwrap_present')

api = (ROOT / 'src/api.rs').read_text()
if 'launch_progress' in api:
    fail('v1_surface_expanded')
boot = (ROOT / 'src/core/boot.rs').read_text()
if '"core.launch_progress"' not in boot:
    fail('module_not_in_boot_diagnostics')

print('LAUNCH_PROGRESS_GUARD_OK phases=5 monotonic cancel_freeze events=unified v1_unchanged')

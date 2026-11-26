#!/usr/bin/env python3
"""093：功能位置清单 txt 完整性与「未执行迁移」口径守护。"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TXT = ROOT / 'docs/records/round-093-feature-locations.txt'


def fail(reason):
    print('FEATURE_LOCATIONS_GUARD_FAIL reason=' + reason)
    sys.exit(1)


if not TXT.is_file():
    fail('txt_missing')
t = TXT.read_text(encoding='utf-8')
if len(t) < 8000:
    fail('txt_too_short bytes=' + str(len(t.encode('utf-8'))))

for p in sorted((ROOT / 'src/core').glob('*.rs')):
    if p.name not in t:
        fail('module_missing ' + p.name)
ax = (ROOT / 'src/core/ax.rs').read_text(encoding='utf-8')
ax_ids = re.findall(r'id: "(AX\d+)"', ax)
for a in ax_ids:
    if a not in t:
        fail('ax_missing ' + a)
if len(ax_ids) != 24:
    fail('ax_count=' + str(len(ax_ids)))

io = (ROOT / 'src/core/settings_io.rs').read_text(encoding='utf-8')
km = re.search(r'pub const KNOWN_KEYS:[^;]*;', io, re.S)
for k in re.findall(r'"([a-z_]+)"', km.group(0)):
    if k not in t:
        fail('root_key_missing ' + k)

html = (ROOT / 'demos/ui-full-kcu-paper.html').read_text(encoding='utf-8')
panes = re.findall(r'data-pane="([^"]+)"', html)
for p in panes:
    if p not in t:
        fail('pane_missing ' + p)
setids = sorted(set(re.findall(r'id="(set[A-Za-z]+)"', html)))
for s in setids:
    if s not in t:
        fail('setting_control_missing ' + s)
if len(panes) != 11 or len(setids) != 15:
    fail('html_counts_changed panes=%d setids=%d' % (len(panes), len(setids)))

for i in range(1, 6):
    if ('偏差 %d ' % i) not in t:
        fail('deviation_missing ' + str(i))
if t.count('状态：待拍板，未执行。') != 5:
    fail('pending_state_count=' + str(t.count('状态：待拍板，未执行。')))
for banned in ('已迁移', '已执行', '已决断', '已拍板', '用户已选'):
    if banned in t:
        fail('migration_marked_done ' + banned)
for needle in ('候选 A', '候选 B', '候选 C', '影响面', '4.7 单个设置项的位置链示例'):
    if needle not in t:
        fail('section_missing ' + needle)

gen = ROOT / 'scripts/feature_locations.py'
if not gen.is_file() or 'OUT.write_text(build()' not in gen.read_text(encoding='utf-8'):
    fail('generator_missing_or_not_reproducible')
for anchor in ('生成命令：python3 scripts/feature_locations.py',
               '校验命令：python3 scripts/feature_locations_guard.py'):
    if anchor not in t:
        fail('reproduce_anchor_missing ' + anchor)

dirty = subprocess.check_output(
    ['git', 'status', '--porcelain', '--', 'src/', 'Cargo.toml', 'Cargo.lock', 'vendor/'],
    cwd=ROOT, text=True).strip()
if dirty:
    fail('src_changed ' + dirty.splitlines()[0])

ci = (ROOT / '.github/workflows/ci.yml').read_text(encoding='utf-8')
if not re.search(r'^\s*- name: feature_locations_guard\s*$', ci, re.M) or \
        'python3 scripts/feature_locations_guard.py' not in ci:
    fail('ci_step_missing')

dec = ROOT / 'docs/decisions/093-feature-locations.md'
if not dec.is_file():
    fail('decision_missing')
d = dec.read_text(encoding='utf-8')
if 'D-093-1' not in d or 'D-093-9' not in d:
    fail('a203_default_echo_missing')

needle = 'gh' + 'p_'
r = subprocess.run(['git', 'grep', '-l', '-I', '-E', needle, '--', '.'],
                   cwd=ROOT, capture_output=True, text=True)
if r.returncode not in (0, 1):
    fail('credential_scan_failed rc=' + str(r.returncode))
if r.returncode == 0 and r.stdout.strip():
    fail('credential_literal ' + r.stdout.strip().splitlines()[0])

print('FEATURE_LOCATIONS_GUARD_OK modules=%d ax=%d panes=%d setids=%d deviations=5 '
      'src_zero_diff ci_step a203_echo no_credential' % (len(list((ROOT / 'src/core').glob('*.rs'))), len(ax_ids), len(panes), len(setids)))

#!/usr/bin/env python3
"""094：功能归类表完整性与「未执行迁移」口径守护。"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TXT = ROOT / 'docs/records/round-094-feature-regrouping.txt'


def fail(reason):
    print('FEATURE_REGROUPING_GUARD_FAIL reason=' + reason)
    sys.exit(1)


if not TXT.is_file():
    fail('txt_missing')
t = TXT.read_text(encoding='utf-8')
if len(t.encode('utf-8')) < 30000:
    fail('txt_too_short bytes=' + str(len(t.encode('utf-8'))))

# 20 域
for i in range(1, 21):
    did = 'D%02d' % i
    if ('【' + did + ' ') not in t:
        fail('domain_missing ' + did)

# 功能项六字段
items = re.findall(r'^  (D\d{2}-\d{2}) (.+)$', t, re.M)
if len(items) < 30:
    fail('item_count=' + str(len(items)))
blocks = re.split(r'(?=^  D\d{2}-\d{2} )', t, flags=re.M)[1:]
for b in blocks:
    for field in ('行为链路：', '当前落点：', '归位落点：', '依据锚点：', '边界：', '状态：'):
        if field not in b:
            fail('field_missing ' + b.splitlines()[0][:20] + ' ' + field)

# 用户点名：下载后台 → 下载页 → 进度条与百分比
for needle in ('下载会进入后台', '进度条', '百分比', '后台化', '默认队列视图', '每文件进度条'):
    if needle not in t:
        fail('download_demo_missing ' + needle)
steps = [int(x) for x in re.findall(r'^ {2,3}(\d{1,2}) \| ', t, re.M)]
if sorted(x for x in steps if 1 <= x <= 12) != list(range(1, 13)):
    fail('download_chain_steps=' + str(len(steps)) + ' ' + str(steps[:15]))

# 093 / 094 区别（回应用户「你交给我的是什么」）
for needle in ('与 093 的区别', '093 回答「文件在哪」', '094 回答'):
    if needle not in t:
        fail('round_diff_missing ' + needle)

# 依据锚点：11:n / 12:n 行号必须真实存在且非空
l11 = (ROOT / 'docs/spec/11-features-input.txt').read_text(encoding='utf-8').splitlines()
l12 = (ROOT / 'docs/spec/12-server-features-input.txt').read_text(encoding='utf-8').splitlines()
for a, b in re.findall(r'\b(11|12):(\d+)', t):
    n = int(b)
    lines = l11 if a == '11' else l12
    if n < 1 or n > len(lines) or not lines[n - 1].strip():
        fail('bad_anchor %s:%d' % (a, n))
for bad in ('11:37 多语言',):
    if bad in t:
        fail('known_bad_anchor_present ' + bad)

# 归类规则 R01–R08 与散落清单
for i in range(1, 9):
    if ('R%02d' % i) not in t:
        fail('rule_missing R%02d' % i)
if t.count('状态：待拍板，未执行。') < 1 and '归位方案全部待拍板未执行' not in t:
    fail('pending_state_missing')
for banned in ('已迁移', '已执行', '已决断', '已拍板', '用户已选'):
    if banned in t:
        fail('migration_marked_done ' + banned)
for sec in ('一、怎么读这份表', '二、功能域总表', '三、逐域逐功能详表',
            '四、下载域完整行为链路示范', '五、归类规则候选', '六、散落清单', '七、约束与状态'):
    if sec not in t:
        fail('section_missing ' + sec)

# 094 spec 逐字
spec = ROOT / 'docs/spec/94-round-094-instructions.txt'
if not spec.is_file() or len(spec.read_bytes()) != 357:
    fail('spec_missing_or_not_357')
if spec.read_text(encoding='utf-8') not in t:
    fail('spec_not_echoed_in_txt')

# 生成脚本可复现
gen = ROOT / 'scripts/feature_regrouping.py'
if not gen.is_file() or 'OUT.write_text(build()' not in gen.read_text(encoding='utf-8'):
    fail('generator_missing_or_not_reproducible')
for anchor in ('生成命令：python3 scripts/feature_regrouping.py',
               '校验命令：python3 scripts/feature_regrouping_guard.py'):
    if anchor not in t:
        fail('reproduce_anchor_missing ' + anchor)

# src 零 diff
dirty = subprocess.check_output(
    ['git', 'status', '--porcelain', '--', 'src/', 'Cargo.toml', 'Cargo.lock', 'vendor/'],
    cwd=ROOT, text=True).strip()
if dirty:
    fail('src_changed ' + dirty.splitlines()[0])

# CI step
ci = (ROOT / '.github/workflows/ci.yml').read_text(encoding='utf-8')
if not re.search(r'^\s*- name: feature_regrouping_guard\s*$', ci, re.M) or \
        'python3 scripts/feature_regrouping_guard.py' not in ci:
    fail('ci_step_missing')

# decision 默认回显
dec = ROOT / 'docs/decisions/094-feature-regrouping.md'
if not dec.is_file():
    fail('decision_missing')
d = dec.read_text(encoding='utf-8')
if 'D-094-1' not in d or 'D-094-9' not in d:
    fail('a203_default_echo_missing')

# 全仓凭据
needle = 'gh' + 'p_'
r = subprocess.run(['git', 'grep', '-l', '-I', '-E', needle, '--', '.'],
                   cwd=ROOT, capture_output=True, text=True)
if r.returncode not in (0, 1):
    fail('credential_scan_failed rc=' + str(r.returncode))
if r.returncode == 0 and r.stdout.strip():
    fail('credential_literal ' + r.stdout.strip().splitlines()[0])

print('FEATURE_REGROUPING_GUARD_OK domains=20 items=%d chain_steps=12 rules=8 '
      'anchors_verified src_zero_diff ci_step a203_echo no_credential' % len(items))

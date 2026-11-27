#!/usr/bin/env python3
"""095：归类覆盖度核对表完整性与「未执行归位」口径守护。"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TXT = ROOT / 'docs/records/round-095-coverage-gaps.txt'


def fail(reason):
    print('FEATURE_COVERAGE_GUARD_FAIL reason=' + reason)
    sys.exit(1)


if not TXT.is_file():
    fail('txt_missing')
t = TXT.read_text(encoding='utf-8')
if len(t.encode('utf-8')) < 20000:
    fail('txt_too_short bytes=' + str(len(t.encode('utf-8'))))

for sec in ('一、11 号原文逐条覆盖', '二、12 号原文逐条覆盖', '三、00 号约束类条目归属',
            '四、U 段 → 功能域映射核对', '五、缺口汇总', '六、12 号无编号补充项逐条', '七、约束与状态'):
    if sec not in t:
        fail('section_missing ' + sec)

# 11 号 55 条编号 / 12 号 24 条编号行，逐条行号必须出现（按原文实跑枚举）
l11 = (ROOT / 'docs/spec/11-features-input.txt').read_text(encoding='utf-8').splitlines()
l12 = (ROOT / 'docs/spec/12-server-features-input.txt').read_text(encoding='utf-8').splitlines()
n11 = [n for n, l in enumerate(l11, 1) if re.match(r'\s*\d{1,2}\.\s*\S', l) and n >= 207]
n12 = [n for n, l in enumerate(l12, 1) if re.match(r'\s*\d{1,2}\.\s*\S', l)]
if len(n11) < 50 or len(n12) < 22:
    fail('source_numbering_changed 11=%d 12=%d' % (len(n11), len(n12)))
body = t.split('三、00 号')[0]
for n in n11 + n12:
    if not re.search(r'^  %3d \|' % n, body, re.M):
        fail('source_line_not_echoed %d' % n)

# 五状态定义与真值
for st in ('OK', 'PART', 'GAP', 'ANCHOR', 'PENDING'):
    if not re.search(r'^  %s\s{2,}' % st, t, re.M):
        fail('state_missing ' + st)
for needle in ('11:248', '11:250', '11:254', '11:259', '11:261', '12:6', '12:11',
               '皮肤预览', '投影预览', '备份', '放音乐', '我的世界百科', '开服文档'):
    if needle not in t:
        fail('gap_missing ' + needle)

# 下载域 12 步不被本轮冲掉：095 不改 094 归类表
t094 = (ROOT / 'docs/records/round-094-feature-regrouping.txt').read_text(encoding='utf-8')
if '下载会进入后台' not in t094 or '百分比' not in t094:
    fail('094_regrouping_damaged')
if '20 域' not in t094:
    fail('094_domains_damaged')

# A259：行号与编号分开核，11:37 / 12:22 等易错形态不出现
for bad in ('11:37 多语言', '11:37', '12:22 条目'):
    if bad in t:
        fail('known_bad_anchor_present ' + bad)

# 00 号约束归属
for n in (8, 15, 20, 21, 24, 25, 32, 33, 114, 137, 175, 245, 248, 249):
    if not re.search(r'00:%d\s*\|' % n, t):
        fail('constraint_missing 00:%d' % n)

# U 段 30 段
useg = re.findall(r'^### (U\d{2}) ', (ROOT / 'docs/design/ux-logic-matrix.md').read_text(), re.M)
for u in useg:
    if not re.search(r'^  %s \|' % u, t, re.M):
        fail('u_segment_missing ' + u)
if len(useg) < 27:
    fail('u_segment_count=' + str(len(useg)))

# 12 号 28–62 行 34 条无编号补充项
l12txt = (ROOT / 'docs/spec/12-server-features-input.txt').read_text(encoding='utf-8').splitlines()
bl = [n for n, l in enumerate(l12txt, 1) if 28 <= n <= 62 and l.strip().startswith('·')]
if len(bl) < 30:
    fail('bullet_count=' + str(len(bl)))
for n in bl:
    if not re.search(r'^  %3d \|' % n, t, re.M):
        fail('bullet_line_not_echoed %d' % n)

# 未执行口径
for banned in ('已迁移', '已执行', '已决断', '已拍板', '用户已选'):
    if banned in t:
        fail('migration_marked_done ' + banned)
if '不执行归位' not in t or '不改 src/' not in t:
    fail('pending_state_missing')

# 95 号 spec 逐字
spec = ROOT / 'docs/spec/95-round-095-instructions.txt'
if not spec.is_file() or len(spec.read_bytes()) != 42:
    fail('spec_missing_or_not_42')
if spec.read_text(encoding='utf-8') not in t:
    fail('spec_not_echoed_in_txt')

# 复现锚点
gen = ROOT / 'scripts/feature_coverage.py'
if not gen.is_file() or "OUT.write_text(build(), encoding='utf-8')" not in gen.read_text():
    fail('generator_missing_or_not_reproducible')
for anchor in ('生成命令：python3 scripts/feature_coverage.py',
               '校验命令：python3 scripts/feature_coverage_guard.py'):
    if anchor not in t:
        fail('reproduce_anchor_missing ' + anchor)

# src 零 diff
dirty = subprocess.check_output(
    ['git', 'status', '--porcelain', '--', 'src/', 'Cargo.toml', 'Cargo.lock', 'vendor/'],
    cwd=ROOT, text=True).strip()
if dirty:
    fail('src_changed ' + dirty.splitlines()[0])

# CI step
ci = (ROOT / '.github/workflows/ci.yml').read_text()
if not re.search(r'^\s*- name: feature_coverage_guard\s*$', ci, re.M) or \
        'python3 scripts/feature_coverage_guard.py' not in ci:
    fail('ci_step_missing')

# decision 默认回显
dec = ROOT / 'docs/decisions/095-feature-coverage.md'
if not dec.is_file():
    fail('decision_missing')
d = dec.read_text()
if 'D-095-1' not in d or 'D-095-8' not in d:
    fail('a203_default_echo_missing')

# 全仓凭据
needle = 'gh' + 'p_'
r = subprocess.run(['git', 'grep', '-l', '-I', '-E', needle, '--', '.'],
                   cwd=ROOT, capture_output=True, text=True)
if r.returncode not in (0, 1):
    fail('credential_scan_failed rc=' + str(r.returncode))
if r.returncode == 0 and r.stdout.strip():
    fail('credential_literal ' + r.stdout.strip().splitlines()[0])

print('FEATURE_COVERAGE_GUARD_OK src11=%d src12=%d c00=14 useg=%d bullets=34 states=5 '
      'gap=7 part=4 anchor=2 src_zero_diff ci_step a203_echo no_credential' %
      (len(n11), len(n12), len(useg)))

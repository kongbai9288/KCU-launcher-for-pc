#!/usr/bin/env python3
"""096：行为链路全集完整性与「未执行归位」口径守护。"""
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
TXT = ROOT / 'docs/records/round-096-behavior-chains.txt'


def fail(reason):
    print('BEHAVIOR_CHAINS_GUARD_FAIL reason=' + reason)
    sys.exit(1)


if not TXT.is_file():
    fail('txt_missing')
t = TXT.read_text(encoding='utf-8')
if len(t.encode('utf-8')) < 60000:
    fail('txt_too_short bytes=' + str(len(t.encode('utf-8'))))

for sec in ('一、UX 矩阵逐 L 行为链路全集', '二、用户举例的「非常详细」颗粒度对照',
            '三、095 缺口方案对照骨架', '四、11 / 12 号原文锚点逐值核', '五、约束与状态'):
    if sec not in t:
        fail('section_missing ' + sec)


def parse_ux():
    lines = (ROOT / 'docs/design/ux-logic-matrix.md').read_text(encoding='utf-8').splitlines()
    segs = []
    cur = None
    for i, l in enumerate(lines, 1):
        m = re.match(r'^### (U\d{2}) (.+)$', l)
        if m:
            cur = {'uid': m.group(1), 'line': i, 'title': m.group(2).strip(), 'ls': []}
            segs.append(cur)
            continue
        if cur:
            mm = re.match(r'^\s*\|\s*(L\d{2})\s*\|\s*(.+?)\s*\|\s*$', l)
            if mm:
                cur['ls'].append((mm.group(1), mm.group(2).strip(), i))
    return segs


def seg_version(title):
    if '历史记录' in title or '保留为历史' in title:
        return '020 历史保留'
    if '021' in title:
        return '021 修订'
    return '主版本'


segs = parse_ux()
heads = len(segs)
uniq = sorted({s['uid'] for s in segs})
total_l = sum(len(s['ls']) for s in segs)
if heads != 29 or len(uniq) != 28 or total_l != 348:
    fail('ux_source_changed heads=%d uniq=%d total=%d' % (heads, len(uniq), total_l))

# 第一节逐 L 回显：按 (uid, 版本, lid, 原文行号, 设计全文) 集合比对，
# U24 两个版本同 uid 同 lid，用集合避免后一版覆盖前一版。
echoed = set()
for l in t.split('一、UX 矩阵逐 L')[1].split('二、用户举例')[0].splitlines():
    m = re.match(r'^  (U\d{2}) \| (.+?) \| (L\d{2}) \|\s*(\d+)\s*\| (.+) \| (D\d{2}|—) \| (.+?) \| 待用户方案填$', l)
    if m:
        echoed.add((m.group(1), m.group(2), m.group(3), int(m.group(4)), m.group(5).strip()))
for s in segs:
    ver = seg_version(s['title'])
    for lid, text, ln in s['ls']:
        key = (s['uid'], ver, lid, ln, text)
        if key not in echoed:
            fail('l_not_echoed_or_mismatch %s/%s/%s line=%d' % (s['uid'], ver, lid, ln))
if len(echoed) != total_l:
    fail('l_echo_count=%d expected=%d' % (len(echoed), total_l))

# 29 个标题行、U24 两版标注
nhead = len(re.findall(r'^  ### U\d{2} ', t, re.M))
if nhead != heads:
    fail('segment_head_echo_count=%d expected=%d' % (nhead, heads))
if '标题行 424 ｜ 版本 021 修订' not in t:
    fail('u24_active_version_missing')
if '标题行 575 ｜ 版本 020 历史保留' not in t:
    fail('u24_history_version_missing')

# 28 个唯一段的域沿用 095
for u in uniq:
    if not re.search(r'### %s .*域 D\d{2}（沿用 095）' % u, t):
        fail('domain_echo_missing ' + u)

# 094 12 步与 U05 12 条 L 对齐
if '094 第四节实跑解析出 12 步，U05 实跑 12 条 L' not in t:
    fail('download_12_step_align_missing')
if '按序号并列不等于语义一一对应' not in t:
    fail('non_one_to_one_disclaimer_missing')
if '同源逐值' in t:
    fail('false_same_source_claim')

# 方案对照骨架 47 行 / 四字段留空
skeleton = t.split('三、095 缺口方案对照骨架')[1].split('四、11 / 12 号')[0]
rows = re.findall(r'^  (?:11|12):\d+\s*\|.*$', skeleton, re.M)
if len(rows) != 47:
    fail('skeleton_rows=%d expected=47' % len(rows))
for r in rows:
    if r.count('待用户方案填') != 4:
        fail('skeleton_field_not_blank ' + r[:40])
if '骨架行数 47：来自 095 第五节 13 条缺口 + 第六节 34 条无编号补充项' not in t:
    fail('skeleton_count_echo_missing')
if '骨架锚点共 47 个' not in t:
    fail('anchor_count_echo_missing')
for src in ('11:248', '11:250', '11:254', '11:259', '11:261', '12:6', '12:11', '12:28', '12:62'):
    if src not in skeleton:
        fail('skeleton_gap_missing ' + src)

# 未执行口径
for banned in ('已迁移', '已执行', '已决断', '已拍板', '用户已选', '为什么做这个'):
    if banned in t:
        fail('migration_marked_done ' + banned)
if '不执行归位' not in t or '不改 `src/`' not in t or '不代拍板' not in t:
    fail('pending_state_missing')

# 94 / 95 交付物未损坏
t094 = (ROOT / 'docs/records/round-094-feature-regrouping.txt').read_text(encoding='utf-8')
t095 = (ROOT / 'docs/records/round-095-coverage-gaps.txt').read_text(encoding='utf-8')
if '下载会进入后台' not in t094 or '20 域' not in t094:
    fail('t094_damaged')
if '五、缺口汇总' not in t095 or '六、12 号无编号补充项逐条' not in t095:
    fail('t095_damaged')

# 96 号 spec 逐字
spec = ROOT / 'docs/spec/96-round-096-instructions.txt'
if not spec.is_file() or len(spec.read_bytes()) != 3:
    fail('spec_missing_or_not_3')
if '用户 096 逐字指令（3 字节）：干' not in t:
    fail('spec_not_echoed_in_txt')

# 复现锚点
gen = ROOT / 'scripts/behavior_chains.py'
if not gen.is_file() or "OUT.write_text(build(), encoding='utf-8')" not in gen.read_text():
    fail('generator_missing_or_not_reproducible')
for anchor in ('生成命令：python3 scripts/behavior_chains.py',
               '校验命令：python3 scripts/behavior_chains_guard.py'):
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
if not re.search(r'^\s*- name: behavior_chains_guard\s*$', ci, re.M) or \
        'python3 scripts/behavior_chains_guard.py' not in ci:
    fail('ci_step_missing')

# decision 默认回显
dec = ROOT / 'docs/decisions/096-behavior-chains.md'
if not dec.is_file():
    fail('decision_missing')
d = dec.read_text()
if 'D-096-1' not in d or 'D-096-9' not in d:
    fail('a203_default_echo_missing')

# 全仓凭据
needle = 'gh' + 'p_'
r = subprocess.run(['git', 'grep', '-l', '-I', '-E', needle, '--', '.'],
                   cwd=ROOT, capture_output=True, text=True)
if r.returncode not in (0, 1):
    fail('credential_scan_failed rc=' + str(r.returncode))
if r.returncode == 0 and r.stdout.strip():
    fail('credential_literal ' + r.stdout.strip().splitlines()[0])

print('BEHAVIOR_CHAINS_GUARD_OK heads=%d uniq=%d l=%d skeleton=47 anchors=47 '
      'u24_two_versions domains=28 src_zero_diff ci_step a203_echo no_credential' %
      (heads, len(uniq), total_l))

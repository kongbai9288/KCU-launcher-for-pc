#!/usr/bin/env python3
"""从 056 起守护 B01 交付格式与 B02 开工复读留痕。

不追溯 054 之前的历史轮次：035–047 的缺失按 048 台账口径「不补写」。
054 决策文件缺两项锚点，按 E128 登记、不补写；守卫只对 >= 056 生效。
失败打印 reason 并返回非零。
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
GUARD_FROM = 56


def read(rel):
    p = ROOT / rel
    if not p.is_file():
        fail(f'missing {rel}')
    return p.read_text()


def fail(reason):
    print(f'DELIVERY_GUARD_FAIL reason={reason}')
    sys.exit(1)


def need(text, needle, tag, rel):
    if needle not in text:
        fail(f'{tag} missing "{needle}" in {rel}')


# 找出所有 >= GUARD_FROM 的轮次编号
nums = set()
for p in (ROOT / 'docs/spec').glob('*-round-*-instructions.txt'):
    m = re.match(r'(\d+)-round-(\d+)-instructions', p.name)
    if m and int(m.group(2)) >= GUARD_FROM:
        nums.add(int(m.group(2)))
if GUARD_FROM not in nums:
    fail('G0 current_round_spec_missing')

for n in sorted(nums):
    tag = f'{n:03d}'

    # G1 逐字副本
    spec = f'docs/spec/{n:02d}-round-{n:03d}-instructions.txt'
    s = read(spec)
    if not s.strip():
        fail(f'G1 spec_empty {spec}')

    # G2 复读记录：5 份原文 + SHA-256 表
    rb = f'docs/records/round-{n:03d}-full-readback.md'
    t = read(rb)
    for f in ('00-requirements.txt', 'ai-errors.md', '11-features-input.txt',
              '12-server-features-input.txt'):
        need(t, f, 'G2', rb)
    need(t, 'SHA-256', 'G2', rb)

    # G3 决策文件四锚点
    decs = list((ROOT / 'docs/decisions').glob(f'{n:03d}-*.md'))
    if not decs:
        fail(f'G3 decision_missing {n}')
    d = decs[0].read_text()
    rel = str(decs[0].relative_to(ROOT))
    # 行首精确匹配：文档表格里会引用这些锚点字符串，子串 in 会被引用干扰
    for anchor in ('## 2. 时间戳', '## 9. 自我批判', '## 10. 四值'):
        if not re.search(r'^' + re.escape(anchor) + r'\s*$', d, re.M):
            fail(f'G3 heading_missing "{anchor}" in {rel}')
    need(d, '开工', 'G3', rel)

    # G4 验证报告：独立验证 + 四值/受阻
    v = read(f'docs/verification/round-{n:03d}.md')
    need(v, '独立验证', 'G4', f'verification/{tag}')
    if '已证实' not in v or ('受阻' not in v and '未证实' not in v):
        fail(f'G4 four_values_incomplete {n}')

    # G5 运行逻辑 HTML 存在
    demos = list((ROOT / 'demos').glob(f'round-{n:03d}-*.html'))
    if not demos:
        fail(f'G5 demo_missing {n}')

# G6 B 类台账 056 补记（E127 / E128 / E129）
b = read('docs/records/requirement-compliance-audit.md')
need(b, '## 056 补记', 'G6', 'compliance-audit')
for k in ('E127', 'E128', 'E129'):
    need(b, k, 'G6', 'compliance-audit')

# G7 055 与 056 决策都带交付状态段（远端受阻如实登记）
for n in (55, 56):
    ds = list((ROOT / 'docs/decisions').glob(f'{n:03d}-*.md'))
    ok = any(('交付快照' in p.read_text() or '交付补记' in p.read_text()) for p in ds)
    if not ok:
        fail(f'G7 delivery_snapshot_missing {n}')

# G8 CI 真的挂上本 step
ci = read('.github/workflows/ci.yml')
need(ci, 'name: delivery_guard', 'G8', 'ci.yml')

print(f'DELIVERY_GUARD_OK rounds={sorted(nums)} g1_spec g2_readback '
      'g3_four_anchors g4_four_values g5_demo g6_b_ledger g7_snapshot g8_ci_step')

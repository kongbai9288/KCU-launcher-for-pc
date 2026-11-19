#!/usr/bin/env python3
"""守护 031 / 032 / 033 自动命令档位口径与 055 C 类台账修正。

只检查文档事实，不改文件；失败时打印 reason 并返回非零。
历史行不重写，因此用「补记段是否存在」而不是「旧行是否消失」判定结案。
"""
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]


def read(rel):
    p = ROOT / rel
    if not p.is_file():
        fail(f'missing {rel}')
    return p.read_text()


def fail(reason):
    print(f'POLICY_GUARD_FAIL reason={reason}')
    sys.exit(1)


def need(text, needle, tag, rel):
    if needle not in text:
        fail(f'{tag} missing "{needle}" in {rel}')


# G1 033 结案证据
g1 = read('docs/decisions/033-answer-abbr-and-anyhow.md')
need(g1, 'Q-031-01 结案', 'G1', '033')
need(g1, 'A 是 answer 缩写', 'G1', '033')

# G2 031 / 032 都带 055 补记，覆盖其历史行里的「待确认 / 未证实」
for rel in ('docs/decisions/031-strict-policy-and-config.md',
            'docs/decisions/032-user-selectable-tiers.md'):
    t = read(rel)
    need(t, '## 055 补记', 'G2', rel)
    need(t, 'Q-031-01', 'G2', rel)

# G3 合规核对表补记了三处台账修正
g3 = read('docs/records/requirement-compliance-audit.md')
need(g3, '## 055 补记', 'G3', 'compliance-audit')
for k in ('C05 台账笔误', 'C06 台账滞后', 'C08 依据轮次错'):
    need(g3, k, 'G3', 'compliance-audit')

# G4 默认严格档、Q1-C / Q2-A、U01 回严格
g4 = read('docs/rules/auto-command-policy.md')
need(g4, '**严格档**（本文件上半部 P01–P07 全部适用）', 'G4', 'policy')
need(g4, 'Q1-C', 'G4', 'policy')
need(g4, 'Q2-A', 'G4', 'policy')
need(g4, '档位一律回到严格', 'G4', 'policy')

# G5 三档单调：严格 Q1-C/Q2-A → 标准 Q1-B/Q2-C → 宽松 Q1-A/Q2-D
rows = []
for line in g4.splitlines():
    if re.match(r'^\| (严格（默认）|标准|宽松) \|', line):
        q1 = re.search(r'Q1-[A-D]', line)
        q2 = re.search(r'Q2-[A-D]', line)
        if q1 and q2:
            rows.append((q1.group(), q2.group()))
expect = [('Q1-C', 'Q2-A'), ('Q1-B', 'Q2-C'), ('Q1-A', 'Q2-D')]
if rows != expect:
    fail(f'G5 tier_monotonicity got {rows} expect {expect}')

# G6 Q-031-01 在待拍板环境清单里标已结案
g6 = read('docs/records/pending-question-environments.md')
if 'Q-031-01 已答' not in g6 and 'Q-031-01 已结案' not in g6:
    fail('G6 q031_not_closed_in_environment_list')
need(g6, '**055 状态**', 'G6', 'pending-question-environments')

# G7 C 类复核表 10 条齐备
g7 = read('docs/records/c-class-default-recheck.md')
for i in range(1, 11):
    tag = f'C{i:02d}'
    need(g7, tag, 'G7', 'c-class-default-recheck')
need(g7, 'Q-037-01', 'G7', 'c-class-default-recheck')

# G8 054 结尾错述已撤回
g8 = read('docs/records/rounds.md')
need(g8, '## 054 结尾错述撤回', 'G8', 'rounds')

print('POLICY_GUARD_OK g1_033_closed g2_031_032_recheck g3_three_ledger_fixes '
      f'g4_default_strict g5_tiers={len(rows)} g6_env_closed g7_c10 g8_054_retracted')

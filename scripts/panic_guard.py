"""CI 守卫：非测试段不得出现会连锁崩溃的调用。

白名单只列构造函数里已由 assert 保证的不变量。
标准库恢复入口（PoisonError::into_inner）与返回 Result 的分支不受限。
"""
from pathlib import Path
import re
import sys

PATTERNS = [
    r'\.lock\(\)\.unwrap\(\)',
    r'\.expect\(',
    r'\bpanic!\(',
    r'\bunreachable!\(',
    r'\btodo!\(',
    r'\bunimplemented!\(',
]
ALLOW = {
    ('src/core/cache.rs', 'NonZeroUsize::new(capacity).expect("capacity > 0")'),
}

hits = []
for p in sorted(Path('src').rglob('*.rs')):
    in_test = False
    for i, line in enumerate(p.read_text().splitlines(), 1):
        s = line.strip()
        if s.startswith('#[cfg(test)]'):
            in_test = True
        if in_test or s.startswith('//') or s.startswith('///'):
            continue
        for pat in PATTERNS:
            if re.search(pat, line):
                if any(str(p) == f and a in s for f, a in ALLOW):
                    continue
                hits.append((str(p), i, pat, s[:100]))

if hits:
    for h in hits:
        print('PANIC_GUARD_HIT', *h, sep=' | ')
    print('PANIC_GUARD_FAIL', len(hits))
    sys.exit(1)
print('PANIC_GUARD_OK', 'files', len(list(Path('src').rglob('*.rs'))), 'hits 0')

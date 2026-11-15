"""CI 守卫：semver::Version 的相等判定必须走 cmp_precedence。

`Version` 的 `==` 包含 build 元数据（+hotfix.1），会破坏同优先级判定。
034 E28 已登记该坑；本脚本防止回滚 / 同版本分支里再次出现裸 `==`。
"""
from pathlib import Path
import sys

# 版本判定文件：含 Version::parse 或 cmp_precedence 的源文件
# 禁止形态：把 Version 值当普通值用 == / != 比较（b、a、v 为约定变量名）
BAD_FORMS = [
    "== b)", "== b,", "== b;", "== a)", "== a,", "== a;",
    "v == b", "b == v", "v == a", "a == v",
    "== candidate", "== installed", "candidate ==", "installed ==",
]

# 显式白名单：034 口径「精确串相等保留」，两侧均为 &str，不是 Version 值。
ALLOW = {
    ("src/core/instance.rs", "if supported == candidate {"),
}

hits = []
checked = []
for p in sorted(Path('src').rglob('*.rs')):
    text = p.read_text()
    if 'Version::parse' not in text and 'cmp_precedence' not in text:
        continue
    checked.append(str(p))
    in_test = False
    for i, line in enumerate(text.splitlines(), 1):
        s = line.strip()
        if s.startswith('#[cfg(test)]'):
            in_test = True
        if in_test or s.startswith('//') or s.startswith('///'):
            continue
        # `== Ordering::Equal` 是合法的比较结果判定，排除
        probe = s.replace('== Ordering::Equal', '')
        if (str(p), s) in ALLOW:
            continue
        for form in BAD_FORMS:
            if form in probe:
                hits.append((str(p), i, form, s[:110]))
                break

if hits:
    for h in hits:
        print('SEMVER_GUARD_HIT', *h, sep=' | ')
    print('SEMVER_GUARD_FAIL', len(hits))
    sys.exit(1)
print('SEMVER_GUARD_OK', 'version_files', len(checked), 'hits 0')

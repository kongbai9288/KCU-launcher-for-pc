"""CI 守卫：界面文案不得硬编码在产品代码或 DOM 属性里。

检查项：
1. src/**/*.rs 非测试段的字符串字面量不得含中文（诊断行、日志、key 除外由白名单列）。
2. demos/ui-full-*.html 的 DOM 段 data-i18n* 值不得含中文。
3. DOM 段纯文本节点含中文时，标签必须带 data-i18n（style/title/script 等排除）。

049 起演示数据源已抽到 demos/lang/*.js；script 段剩余中文是内联双语
fallback 与稳定状态字面量，只统计、不判失败。语言包结构由 lang_guard.py 判。
"""
from pathlib import Path
import re
import sys

CN = re.compile(r'[\u4e00-\u9fff]')


def cn(s):
    return bool(CN.search(s))


hits = []
rs_files = 0
for p in sorted(Path('src').rglob('*.rs')):
    rs_files += 1
    in_test = False
    for i, line in enumerate(p.read_text().splitlines(), 1):
        s = line.strip()
        if s.startswith('#[cfg(test)]'):
            in_test = True
        if in_test or s.startswith('//'):
            continue
        for m in re.finditer(r'"([^"\\]*(?:\\.[^"\\]*)*)"', line):
            if cn(m.group(1)):
                hits.append(('RS_LITERAL', str(p), i, m.group(1)[:80]))

SKIP_TAGS = {'style', 'script', 'title', 'svg', 'path', 'rect'}
NODE = re.compile(r'(<([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>)([^<>]*[\u4e00-\u9fff][^<>]*)(</\2>)')

# 当前有效的整页 UX 演示。其余为历史稿，018 已标记作废，不参与守卫。
ACTIVE = {'ui-full-kcu-paper.html'}
excluded = []
html_files = 0
script_cn = 0
for p in sorted(Path('demos').glob('ui-full-*.html')):
    if p.name not in ACTIVE:
        excluded.append(p.name)
        continue
    html_files += 1
    text = p.read_text()
    at = text.find('<script>')
    dom = text[:at] if at >= 0 else text
    for m in re.finditer(r'data-i18n(?:-[a-z]+)?="([^"]*)"', dom):
        if cn(m.group(1)):
            hits.append(('DOM_CN_KEY', str(p), 0, m.group(1)[:80]))
    for m in NODE.finditer(dom):
        tag, attrs, body = m.group(2), m.group(3), m.group(4)
        if tag.lower() in SKIP_TAGS or 'data-i18n' in attrs or not body.strip():
            continue
        hits.append(('DOM_BARE_CN', str(p), 0, body.strip()[:80]))
    if at >= 0:
        js = text[at:].split('</script>')[0]
        script_cn += sum(1 for l in js.splitlines() if cn(l))

if hits:
    for h in hits[:40]:
        print('I18N_GUARD_HIT', *h, sep=' | ')
    print('I18N_GUARD_FAIL', len(hits))
    sys.exit(1)
print('I18N_GUARD_OK', 'rs_files', rs_files, 'ux_html', html_files,
      'hits 0', 'inline_bilingual_cn_lines', script_cn,
      'excluded_history', ','.join(excluded))

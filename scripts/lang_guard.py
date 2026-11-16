"""CI 守卫：演示数据源语言包结构完整、离线可加载、切换时重建。

048 EQ-14 选项②落地后的约束。只判结构与稳定值，不判译文覆盖率
（英文包里未审校的中文字符串如实打印，不伪装成失败或成功）。
"""
from pathlib import Path
import json
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
LANGDIR = ROOT / 'demos/lang'
HTML = ROOT / 'demos/ui-full-kcu-paper.html'
CN = re.compile(r'[\u4e00-\u9fff]')


def load(name):
    p = LANGDIR / name
    if not p.is_file():
        raise RuntimeError('LANG_MISSING ' + name)
    t = p.read_text()
    assert t.startswith('window.KCU_LANG = window.KCU_LANG || {};'), name + ' bad header'
    m = re.search(r"window\.KCU_LANG\['([a-zA-Z-]+)'\] = (\{.*\});\s*$", t, re.S)
    if not m:
        raise RuntimeError('LANG_PARSE_FAIL ' + name)
    return m.group(1), json.loads(m.group(2))


def shape(v):
    if isinstance(v, list):
        return ('list', len(v), tuple(shape(x) for x in v[:3]))
    if isinstance(v, dict):
        return ('obj', tuple(sorted(v.keys())), tuple(shape(v[k]) for k in sorted(v)[:3]))
    return ('scalar',)


def strings(v, out):
    if isinstance(v, str):
        out.append(v)
    elif isinstance(v, list):
        for x in v:
            strings(x, out)
    elif isinstance(v, dict):
        for x in v.values():
            strings(x, out)


hits = []
zl, zh = load('zh-CN.js')
el, en = load('en-US.js')
if (zl, el) != ('zh-CN', 'en-US'):
    hits.append(('LANG_LOCALE', zl, el))
if set(zh) != set(en):
    hits.append(('LANG_KEYS_DIFF', sorted(set(zh) ^ set(en))[:8]))
for k in sorted(set(zh) & set(en)):
    if shape(zh[k]) != shape(en[k]):
        hits.append(('LANG_SHAPE_DIFF', k, shape(zh[k])[0], shape(en[k])[0]))

# 稳定状态值 / 用户数据不得随语言变化
for i, row in enumerate(zh['SRV']):
    if en['SRV'][i][3] != row[3]:
        hits.append(('SRV_STATUS_CHANGED', i, row[3], en['SRV'][i][3]))
for i, row in enumerate(zh['LICENSE_ROWS']):
    if en['LICENSE_ROWS'][i][6] != row[6]:
        hits.append(('LIC_STATUS_CHANGED', i, row[6], en['LICENSE_ROWS'][i][6]))
for i, row in enumerate(zh['INS']):
    if en['INS'][i][5] != row[5]:
        hits.append(('INS_CODE_CHANGED', i, row[5], en['INS'][i][5]))
USER_FIELDS = ('sid', 'id', 'name', 'ip', 'ver', 'motd', 'inst', 'last', 'src')
for i, s in enumerate(zh['SERVERS']):
    for f in USER_FIELDS:
        if en['SERVERS'][i].get(f) != s.get(f):
            hits.append(('USER_DATA_TRANSLATED', i, f))

t = HTML.read_text()
main = t.find('<script>\n')
for name in ('lang/zh-CN.js', 'lang/en-US.js'):
    pos = t.find('<script src="' + name + '"></script>')
    if pos < 0 or pos > main:
        hits.append(('LANG_SCRIPT_REF_MISSING_OR_LATE', name, pos, main))
if 'function loadData(l)' not in t or 'loadData(l);' not in t:
    hits.append(('REBUILD_MISSING',))
if 'mergeState(' not in t:
    hits.append(('STATE_MERGE_MISSING',))
if re.search(r"fetch\(\s*['\"](?:\./)?lang/|XMLHttpRequest", t):
    hits.append(('OFFLINE_BROKEN', 'fetch/XHR used for lang'))

zs, es = [], []
for k, v in zh.items():
    if k not in {'EN', 'ZH_TEXT', 'EN_TEXT', 'TIER_EN'}:
        strings(v, zs)
for k, v in en.items():
    if k not in {'EN', 'ZH_TEXT', 'EN_TEXT', 'TIER_EN'}:
        strings(v, es)
cn_zh = sum(1 for s in zs if CN.search(s))
cn_en = sum(1 for s in es if CN.search(s))

if hits:
    for h in hits[:30]:
        print('LANG_GUARD_HIT', *h, sep=' | ')
    print('LANG_GUARD_FAIL', len(hits))
    sys.exit(1)
print('LANG_GUARD_OK', 'locales', zl, el, 'keys', len(zh),
      'data_cn_zh', cn_zh, 'data_cn_en_known', cn_en,
      'stable_values_ok', 'offline_refs_ok')

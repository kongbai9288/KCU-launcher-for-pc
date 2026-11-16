"""把 UX 演示里的中文 key 与裸中文文本收敛到语义 key + 语言包字典。"""
from pathlib import Path
import json
import re

P = Path('demos/ui-full-kcu-paper.html')
t = P.read_text()
script_at = t.find('<script>')
dom, script = t[:script_at], t[script_at:]

# 现有 EN_TEXT：中文 -> 英文
m = re.search(r'const EN_TEXT=(\{.*?\});\n', script, re.S)
assert m, 'EN_TEXT not found'
en_cn = json.loads(m.group(1))
en_cn = {k.strip(): v for k, v in en_cn.items()}

zh2key = {}
key2zh = {}
key2en = {}
counter = [0]


def new_key(zh):
    k = zh.strip()
    if k in zh2key:
        return zh2key[k]
    counter[0] += 1
    key = 't.%04d' % counter[0]
    zh2key[k] = key
    key2zh[key] = k
    key2en[key] = en_cn.get(k, k)
    return key


def cn(s):
    return bool(re.search(r'[\u4e00-\u9fff]', s))


# 1) 属性值：data-i18n / -ph / -title 中的中文换成语义 key
attr_re = re.compile(r'(data-i18n(?:-[a-z]+)?)="([^"]*)"')


def attr_sub(mo):
    name, val = mo.group(1), mo.group(2)
    if not cn(val):
        return mo.group(0)
    return '%s="%s"' % (name, new_key(val))


dom = attr_re.sub(attr_sub, dom)

# 2) 纯文本节点：开标签注入 data-i18n，原文收进字典
SKIP = {'style', 'script', 'title', 'svg', 'path', 'rect'}
node_re = re.compile(
    r'(<([a-zA-Z][a-zA-Z0-9]*)\b([^>]*)>)([^<>]*[\u4e00-\u9fff][^<>]*)(</\2>)'
)


def node_sub(mo):
    open_tag, tag, attrs, text, close_tag = mo.groups()
    if tag.lower() in SKIP or 'data-i18n' in attrs:
        return mo.group(0)
    if not text.strip():
        return mo.group(0)
    key = new_key(text)
    # 在开标签的 > 前插入属性
    injected = open_tag[:-1].rstrip() + ' data-i18n="%s">' % key
    return injected + text + close_tag


dom = node_re.sub(node_sub, dom)

# 3) 重生成字典与 tr()
zh_json = json.dumps(key2zh, ensure_ascii=False, separators=(',', ':'))
en_json = json.dumps(key2en, ensure_ascii=False, separators=(',', ':'))
new_dict = 'const ZH_TEXT=%s;\nconst EN_TEXT=%s;' % (zh_json, en_json)
script = script[:m.start()] + new_dict + script[m.end() - 1:]

old_tr = "function tr(k,fb){if(LOCALE==='en-US'){if(EN[k])return EN[k];if(EN_TEXT[k])return EN_TEXT[k];}return fb!==undefined?fb:k;}"
new_tr = "function tr(k,fb){if(LOCALE==='en-US'){if(EN[k])return EN[k];if(EN_TEXT[k])return EN_TEXT[k];}if(ZH_TEXT[k])return ZH_TEXT[k];return fb!==undefined?fb:k;}"
assert old_tr in script
script = script.replace(old_tr, new_tr, 1)

P.write_text(dom + script)

# 自检
t2 = P.read_text()
dom2 = t2[:t2.find('<script>')]
attrs2 = re.findall(r'data-i18n(?:-[a-z]+)?="([^"]*)"', dom2)
cn_keys = [a for a in attrs2 if cn(a)]
bare = [
    h for h in node_re.findall(dom2)
    if h[1].lower() not in SKIP and 'data-i18n' not in h[2] and h[3].strip()
]
refs = set(re.findall(r'data-i18n(?:-[a-z]+)?="([^"]*)"', dom2))
defined = set(key2zh) | set(re.findall(r"'([a-zA-Z][a-zA-Z0-9_.-]*)'\s*:", script.split('const ZH_TEXT')[0]))
missing = refs - defined
print('CN_KEYS_LEFT', len(cn_keys))
print('BARE_CN_NODES_LEFT', len(bare))
print('KEYS_GENERATED', counter[0])
print('UNTRANSLATED_EN', sum(1 for k, v in key2en.items() if v == key2zh[k]))
print('MISSING_REFS', len(missing), sorted(missing)[:8])

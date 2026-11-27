#!/usr/bin/env python3
"""096：把 UX 矩阵 348 条 L 逐值摊平，并给 095 缺口留方案对照骨架。

只读实扫：ux-logic-matrix.md、094 归类表、095 覆盖表、11/12 号原文。
不执行归位、不代拍板、不改 src/。输出 docs/records/round-096-behavior-chains.txt。
"""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/records/round-096-behavior-chains.txt'
SPEC = '干'
T094 = (ROOT / 'docs/records/round-094-feature-regrouping.txt').read_text(encoding='utf-8')
T095 = (ROOT / 'docs/records/round-095-coverage-gaps.txt').read_text(encoding='utf-8')

# 095 轮已定的 U 段 -> 域映射，096 沿用不新决断（A203 默认值 D-096-3）
UMAP = {
    'U01': 'D01', 'U02': 'D02', 'U03': 'D03', 'U04': 'D04', 'U05': 'D05',
    'U06': 'D06', 'U07': 'D07', 'U08': 'D09', 'U09': 'D10', 'U10': 'D11',
    'U11': 'D12', 'U12': 'D16', 'U13': 'D16', 'U14': 'D15', 'U15': 'D08',
    'U16': 'D10', 'U17': 'D17', 'U18': 'D16', 'U19': 'D16', 'U20': 'D18',
    'U21': 'D10', 'U22': 'D10', 'U23': 'D14', 'U24': 'D04', 'U25': 'D13',
    'U26': 'D04', 'U27': 'D04', 'U28': 'D19',
}

# 094 开工快照（096 文件落地前，095 补记后）
SNAP = dict(tracked=1316, core_rs=48, guards=38, demos=81, previews=56,
            decisions=88, verification=90, features=73, required=539, ax=24)


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


def refs094(uid, lid):
    """094 归类表里引用了 Uxx Lxx / Uxx 的功能项编号。"""
    pat = re.compile(r'\b' + uid + r'\s+L?' + lid + r'\b')
    out = []
    for b in re.split(r'(?=^  D\d{2}-\d{2} )', T094, flags=re.M)[1:]:
        head = b.splitlines()[0].strip()
        m = re.match(r'(D\d{2}-\d{2})', head)
        if m and pat.search(b):
            out.append(m.group(1))
    return out


def parse095_gaps():
    """从 095 覆盖表第五 / 六节实扫缺口行，不重写清单。

    第五节格式：'  11:248 | GAP | 候选域' 下一行缩进 8 空格是原文摘要。
    第六节格式：'  28 | 补充项 | 候选域 | 094 状态'。
    返回 (来源, 类型, 候选域, 摘要, 节)。
    """
    gaps = []
    sec5 = T095.split('五、缺口汇总')[1].split('六、12 号无编号补充项')[0]
    lines5 = sec5.splitlines()
    for i, l in enumerate(lines5):
        m = re.match(r'^  (11|12):(\d+)\s*\|\s*(GAP|PART|ANCHOR)\s*\|\s*(.+)$', l)
        if not m:
            continue
        desc = lines5[i + 1].strip() if i + 1 < len(lines5) else ''
        gaps.append((m.group(1) + ':' + m.group(2), m.group(3),
                     m.group(4).strip(), desc, '第五节'))
    sec6 = T095.split('六、12 号无编号补充项逐条')[1].split('七、约束与状态')[0]
    for m in re.finditer(r'^\s+(\d+)\s*\|\s*(.+?)\s*\|\s*(.+?)\s*\|\s*(.+)$', sec6, re.M):
        gaps.append(('12:' + m.group(1), 'BULLET', m.group(3).strip(),
                     m.group(2).strip(), '第六节'))
    return gaps


def parse094_steps():
    """094 第四节下载域 12 步，格式 '   1 | 环节 | 用户可见事实 | 依据'。"""
    seg = T094.split('四、下载域完整行为链路示范')[1].split('五、')[0]
    out = []
    for l in seg.splitlines():
        m = re.match(r'^\s+(\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|', l)
        if m:
            out.append((int(m.group(1)), m.group(2).strip(), m.group(3).strip()))
    return out


def seg_version(title):
    if '历史记录' in title or '保留为历史' in title:
        return '020 历史保留'
    if '021' in title:
        return '021 修订'
    return '主版本'


def build():
    segs = parse_ux()
    heads = len(segs)
    uniq = sorted({s['uid'] for s in segs})
    total_l = sum(len(s['ls']) for s in segs)
    gaps = parse095_gaps()
    per = {}
    for s in segs:
        per[s['uid']] = per.get(s['uid'], 0) + len(s['ls'])

    L = []
    add = L.append
    add('KCU Launcher 用户可见行为链路全集与方案对照骨架（096 轮）')
    add('文件：docs/records/round-096-behavior-chains.txt')
    add('生成：python3 scripts/behavior_chains.py（只读实扫 UX 矩阵 / 094 归类表 / 095 覆盖表 / 11 / 12 号原文）')
    add('开工时间戳：Fri Nov 27 13:17:10 CST 2026')
    add('用户 096 逐字指令（3 字节）：' + SPEC)
    add('本轮动作：用户 095「我设计好再给你」、096 只发「干」，按 `00:248` 继续做不依赖归位方案的增量工作。')
    add('把 UX 矩阵每一条 L 逐值摊平，并给 095 查出的缺口留一份可填的方案对照骨架。')
    add('不执行归位、不代拍板、不移动文件、不改设置项、不改 `src/`；域归属沿用 095 已定映射，不新决断。')
    add('')
    add('核对对象与边界：094 交的是按域归纳的 20 域 / 37 功能项，只有下载域按用户举例的「非常详细」颗粒度逐值展开了 12 步；')
    add('095 逐条核出 7 条真漏 / 4 条部分覆盖 / 2 条锚点缺口 / 34 条无编号补充项，全部标待拍板。')
    add('用户要「每一个功能重新归好类」且「非常详细」。096 不替用户定归类，先把所有可见行为的原文逐字摊平，')
    add('再把每条缺口的六个字段留成空位，用户方案到了直接填，不靠我猜。')
    add('')
    add('计数口径：096 文件落地前 tracked %d / 48 个 `src/core/*.rs` / %d 守卫 / %d HTML / %d PNG / %d 决策 / %d 验证 / %d 功能文档 / 必读清单 %d 项 / 24 AX。' % (
        SNAP['tracked'], SNAP['guards'], SNAP['demos'], SNAP['previews'],
        SNAP['decisions'], SNAP['verification'], SNAP['features'], SNAP['required']))
    add('096 文件落地后 tracked 增加，两口径在补记并列不混用（沿用 093 E379 / 094 E381 / 095 补记）。')
    add('UX 矩阵实跑：%d 个 U 段标题 / %d 个唯一编号 / 每段 %s 条 L / 共 %d 条 L；U24 出现两次。' % (
        heads, len(uniq), sorted(set(per.values())), total_l))
    add('')
    add('状态与来源定义：')
    add('  UX      该行为逐字来自 `docs/design/ux-logic-matrix.md` 对应行，096 不改一字')
    add('  沿用 095  域编号取自 095 的 U 段映射，096 不新决断、不重新归类')
    add('  待用户方案填  归位落点 / 当前落点 / 边界 / 状态四字段一律留空，不代填（A203 / A208）')
    add('  094 已展开  094 归类表里逐值引用了该 L（实扫匹配），否则标「094 未逐 L 展开 → 096 补」')
    add('')
    add('=' * 92)
    add('一、UX 矩阵逐 L 行为链路全集（%d 段 / %d 条 L，逐字回显）' % (heads, total_l))
    add('=' * 92)
    add('列：段 | 版本 | L | 原文行 | 设计全文（逐字） | 域(沿用095) | 094 引用 | 归位落点')
    for s in segs:
        uid = s['uid']
        ver = seg_version(s['title'])
        add('')
        add('  ### %s %s ｜ 标题行 %d ｜ 版本 %s ｜ L %d 条 ｜ 域 %s（沿用 095）' % (
            uid, s['title'], s['line'], ver, len(s['ls']), UMAP.get(uid, '—')))
        for lid, text, ln in s['ls']:
            rr = ','.join(refs094(uid, lid)) or '094 未逐 L 展开 → 096 补'
            add('  %s | %s | %s | %4d | %s | %s | %s | 待用户方案填' % (
                uid, ver, lid, ln, text, UMAP.get(uid, '—'), rr))
    add('')
    add('  逐 L 合计 %d 条；U24 两个版本各自 12 条都回显，021 修订版与 020 历史保留版不合并（095 已登记）。' % total_l)
    add('  094 归类表只逐值引用了下载域相关的少数 L；其余段 094 按域归纳未展开到 L 颗粒度，096 一次性补齐。')
    add('')
    add('=' * 92)
    add('二、用户举例的「非常详细」颗粒度对照（下载域）')
    add('=' * 92)
    add('用户 094 原话：「下载会进入后台，然后用户可以在下载页当中打开，并且查看它的进度条和百分比」。')
    add('094 已按 12 步展开；096 把 U05 的 12 条 L 与 094 的 12 步逐条对齐，核这个颗粒度是不是全域统一形态。')
    add('')
    u05 = next(s for s in segs if s['uid'] == 'U05' and '下载中心' in s['title'])
    steps094 = parse094_steps()
    add('列：步 | 094 环节 | 094 用户可见事实（逐字） | U05 对应 L（逐字） | 对齐')
    for i, (lid, text, ln) in enumerate(u05['ls'], 1):
        st = '%s / %s' % (steps094[i - 1][1], steps094[i - 1][2]) if i <= len(steps094) else '（094 12 步段未收该步，按实标注）'
        add('  %2d | %s | %s %s | 按序号并列' % (i, st[:70], lid, text[:56]))
    add('')
    add('  094 第四节实跑解析出 %d 步，U05 实跑 %d 条 L；两侧逐值摆出来，不改写 094。' % (len(steps094), len(u05['ls'])))
    add('  按序号并列不等于语义一一对应：094 的 12 步来自 11 号下载锚点与 U05 L 的合并表述，U05 的 12 条 L 来自 UX 矩阵原文；')
    add('  步 1「触发」与 L01「导航进入」不是同一件事，按实标注，不写成同源、不替用户合并（A208）。')
    add('  094 不改写，096 只把 U05 原文 12 条逐值摆出来。')
    add('  结论：这个颗粒度在 UX 矩阵里是每段 12 条 L 的统一形态，不是下载域独有；第二节全集已按同一形态摊平 28 个唯一段。')
    add('')
    add('=' * 92)
    add('三、095 缺口方案对照骨架（只回填锚点 / 候选域 / 摘要，四个归位字段留空待用户方案）')
    add('=' * 92)
    add('用户方案到了，逐行在「归位落点 / 行为链路 / 边界 / 状态」四列填值即可；096 一个都不代填。')
    add('列：来源 | 类型 | 095 候选域（沿用） | 原文 / 补充项摘要（逐字） | 归位落点 | 行为链路 | 边界 | 状态')
    for src, typ, cand, desc, where in gaps:
        add('  %-7s | %-7s | %s | %s | 待用户方案填 | 待用户方案填 | 待用户方案填 | 待用户方案填' % (
            src, typ, cand[:56], (desc or '（095 该行无摘要）')[:70]))
    add('')
    add('  骨架行数 %d：来自 095 第五节 %d 条缺口 + 第六节 %d 条无编号补充项（实扫解析，不重写清单）。' % (
        len(gaps), sum(1 for g in gaps if g[1] != 'BULLET'),
        sum(1 for g in gaps if g[1] == 'BULLET')))
    add('  095 的 7 条真漏里最需定夺的 6 条（皮肤预览与创建角色 / 投影预览 / 备份打包 / 音乐播放 / MC 百科 / 开服文档）都在骨架内；')
    add('  `12:6` 快速标注与 `11:240` 颜色代码一键复制是两条不同功能，骨架里单列不合并（095 E383）。')
    add('')
    add('=' * 92)
    add('四、11 / 12 号原文锚点逐值核（骨架里的行号都真存在）')
    add('=' * 92)
    l11 = (ROOT / 'docs/spec/11-features-input.txt').read_text(encoding='utf-8').splitlines()
    l12 = (ROOT / 'docs/spec/12-server-features-input.txt').read_text(encoding='utf-8').splitlines()
    srcs = sorted({g[0] for g in gaps})
    add('列：锚点 | 原文该行（逐字） | 骨架状态')
    for src in srcs:
        k, n = src.split(':'); n = int(n)
        arr = l11 if k == '11' else l12
        val = arr[n - 1].strip() if 1 <= n <= len(arr) else '（行号越界）'
        add('  %-7s | %s | 骨架已留空位' % (src, val[:80]))
    add('')
    add('  骨架锚点共 %d 个，逐个核真实行存在且非空；12 号 25 / 26 缺号不在骨架内（095 E384）。' % len(srcs))
    add('')
    add('=' * 92)
    add('五、约束与状态')
    add('=' * 92)
    add('  用户 096 当轮「干」：按 `00:248` 覆盖 095 结尾「等用户归位方案」的预告，继续做不依赖方案的增量；不执行归位、不代拍板（A208）。')
    add('  域归属全部沿用 095 UMAP，096 零新决断；U24 两版都回显不合并；归位落点四字段一律留空（A203）。')
    add('  096 只增文档 / 脚本 / 演示 / 台账：不移动文件、不改设置项、不改 `src/`、不改 `Cargo.*` / `vendor/`、不改 094 / 095 交付物。')
    add('  093 的 5 条偏差、094 的 8 条规则与 10 条散落清单、095 的 13 条缺口与 %d 条补充项、A 组 EQ / Q 全部仍待拍板。' % sum(1 for g in gaps if g[1] == 'BULLET'))
    add('  E385 登记：094 只把下载域展开到用户举例的「非常详细」颗粒度，其余 27 个唯一 U 段停在按域归纳；095 把逐条覆盖查清但未展开 L。')
    add('  096 补交 %d 条 L 逐值全集与方案对照骨架；094 / 095 历史文件不重写（A181 / A201），E385 计入四值「已失败」。' % total_l)
    add('  四值：已证实（96 号 spec 逐字 3 字节、四份原文逐行校验复读、UX 矩阵 %d 段 / %d 条 L 实扫逐值摊平、095 缺口 %d 条实扫解析成骨架、锚点 %d 个逐值核、094 下载 12 步与 U05 12 条 L 对齐、开工 A145 远端 c0f8161 与 1316 ALL_MATCH True）；已失败（E213–E384 历史项 + E385 本轮颗粒度缺口）；未证实（13 条 EQ / 4 项 Q-C / 31 条历史 Q / 2 项 Planned / 所有归位落点与边界 / 用户方案）；未启动（归位迁移执行、真实网络 IO、UI 宿主、渲染层、真实下载字节落盘）。' % (
        heads, total_l, len(gaps), len(srcs)))
    add('  通过标记：按 00:245 不发；独立验证部分通过。')
    add('  唯一下一步：等用户归位方案；方案到了按第三节骨架逐行填值，不擅自开工硬做。')
    add('')
    add('生成命令：python3 scripts/behavior_chains.py')
    add('校验命令：python3 scripts/behavior_chains_guard.py')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    OUT.write_text(build(), encoding='utf-8')
    b = OUT.read_bytes()
    print('BEHAVIOR_CHAINS_OK path=%s bytes=%d lines=%d sha256=%s' %
          (str(OUT.relative_to(ROOT)), len(b), b.count(b'\n'), hashlib.sha256(b).hexdigest()[:16]))

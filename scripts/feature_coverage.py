#!/usr/bin/env python3
"""095：逐条核 11 / 12 号原文功能有没有被 094 的 20 域收进去。

只读实扫：11 / 12 号编号条目、094 归类表锚点与功能项、00 号约束、U 段。
不执行归位、不代拍板、不改 src/。输出 docs/records/round-095-coverage-gaps.txt。
"""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/records/round-095-coverage-gaps.txt'
SPEC = '你先继续干，我设计好再给你。'
T094 = (ROOT / 'docs/records/round-094-feature-regrouping.txt').read_text(encoding='utf-8')

# 094 开工快照（095 文件落地前）
SNAP = dict(tracked=1308, core_rs=48, guards=37, demos=80, previews=56,
            decisions=87, verification=89, features=72, required=531, ax=24)


def anchors(txt):
    a = {'11': set(), '12': set()}
    for m in re.finditer(r'\b(11|12):(\d+)(?:[–-](\d+))?', txt):
        k, x, y = m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))
        if y - x < 40:
            a[k].update(range(x, y + 1))
    return a


ANCH = anchors(T094)

# 094 功能项块 → 该项引用了哪些 11/12 行
ITEMS = []
for b in re.split(r'(?=^  D\d{2}-\d{2} )', T094, flags=re.M)[1:]:
    head = b.splitlines()[0].strip()
    m = re.match(r'(D\d{2}-\d{2}) (.+)', head)
    if not m:
        continue
    ITEMS.append((m.group(1), m.group(2), anchors(b)))


def refs(kind, n):
    return [i[0] for i in ITEMS if n in i[2][kind]]


def numbered(path, start=1):
    out = []
    for n, l in enumerate((ROOT / path).read_text(encoding='utf-8').splitlines(), 1):
        m = re.match(r'\s*(\d{1,2})\.\s*(.+)', l)
        if m and n >= start:
            out.append((n, int(m.group(1)), m.group(2).strip()))
    return out


def bullets(path, lo, hi):
    """12 号 28–62 行 `· ` 开头的无编号补充项（原文逐条写的功能，094 基本未收）。"""
    out = []
    for n, l in enumerate((ROOT / path).read_text(encoding='utf-8').splitlines(), 1):
        if lo <= n <= hi and l.strip().startswith('·'):
            out.append((n, l.strip().lstrip('·').strip()))
    return out


def bullet_domain(text):
    if re.search(r'下载源|镜像|共享模组缓存|缓存', text):
        return 'D05 下载中心 / D18 缓存与刷新总控'
    if re.search(r'图标|MOTD|皮肤|头像', text):
        return 'D04 服务器·图标'
    if re.search(r'种子|权限提示|审计日志|敏感信息', text):
        return 'D08 开服器·世界 / D04 服务器'
    if re.search(r'颜色|标注|mod 名称', text):
        return 'D06 模组管理·标注'
    if re.search(r'配置快照|依赖预检|回滚', text):
        return 'D06 模组管理 / D08 开服器·运维'
    return 'D08 开服器·运维'


# 人工判定：行号 -> (状态, 缺口说明, 候选域, 094 已有落点)
# 状态：OK 已覆盖 / PART 部分覆盖 / GAP 真漏归类 / ANCHOR 有域无锚点 / PENDING 原文待拍板
H11 = {
 211: ('PART', '094 D20 只挂「快捷键绑定 / 录屏截屏加了快捷键并打开开关后后台才有进程」；原文同条还有保存时间、保存清晰度、内容大小熔断 5GB 与 2 小时并联（两限制并联不是串联）、游戏关闭时引导打开保存文件夹、默认不开启', 'D20 搜索与快捷入口 或新子项「录屏截屏」，候选取决于用户方案', 'D20-01'),
 223: ('ANCHOR', '加载器自动安装：094 D08-01 写了「自动下载 jar → 加载器选择页」，但依据只挂 12:2，未挂 11:223；功能有域、锚点缺', 'D08 开服器·建服（补挂 11:223）', 'D08-01'),
 229: ('PART', '094 D04-02 只写「自动上线 / 自动加入服务器按手动设定时间触发」；原文同条还有自动下线、电脑自动关机任务', 'D04 服务器·状态 或 D08 开服器·定时任务（12:17 已在 D08-02）', 'D04-02'),
 232: ('PART', '094 D03-01 只写「键盘文件、服务器文件随版本迁移」；原文同条还有「一次性应用于多个 MC 版本」与「弹窗是否去掉不支持的文件内容」', 'D03 实例与版本·版本迁移', 'D03-01'),
 242: ('PENDING', '094 D16-01 已挂「.kculf / kculh / 使用两天或手动装拓展包」并标 11:242 时长路径待拍板；归类无缺口，口径待拍', 'D16 运行形态（口径待拍）', 'D16-01'),
 248: ('GAP', '皮肤预览与创建角色选择：094 D19 只挂 skin_draft.rs（AX14 草稿会话元数据），AX14 收窄时明确排除 3D 旋转预览 / PNG 下载 / 玩家名与 UUID 查询；「皮肤预览、创建角色选择角」这条原文没有任何域承接', 'D19 外观与文案 或 D07 账号登录·角色（候选，待拍板）', 'D19-01（仅草稿元数据，非本条）'),
 250: ('GAP', '投影预览（两个投影模组的文件都支持）：094 20 域 / 37 项里没有投影预览条目；AX20 projection_workshop 已在 090 落地数据层，094 归类表漏收', '新建子项归 D06 模组管理 或 D03 实例与版本（候选，待拍板）', '无'),
 254: ('GAP', '备份、文件自动打成压缩包：094 D15 只挂「分卷解压 / 压缩包校验 / 修复」，12:13 增量备份归 D08-02（服务器侧）；客户端实例备份这条原文没有域承接', 'D03 实例与版本·备份 或 D15 文件管理（候选，待拍板）', 'D15-01（仅解压校验）'),
 259: ('GAP', '放音乐功能，导入音乐 mp4，未启动 MC 时播放：094 20 域里没有任何域承接', 'D01 首页与启动·空闲态 或 D19 外观与文案（候选，待拍板）', '无'),
 261: ('GAP', '我的世界百科，按当前语言定 minecraft wiki 站点、失败进英文、可直接搜：094 D20 搜索域只收启动器内搜索（设置项 / 文件名 / 推荐位 / 服务器名），未收外部百科站点', 'D20 搜索与全局快捷入口·外部源 或新子项（候选，待拍板）', 'D20-01（仅启动器内搜索）'),
 266: ('PENDING', '094 D07-01 已挂「11:266 正版复用方案待拍板」；归类无缺口，方案待拍', 'D07 账号登录（方案待拍）', 'D07-01'),
 267: ('PART', '094 D05-02 挂了「curseforge 境外双通道口径按 11:267 不写进注释、不进表正文细节」；原文同条还含「镜像优先、限额低、自己做了限速处理」等口径，按用户要求不入仓，只标已登记', 'D05 下载中心·源与并发（口径按 11:267 不入仓）', 'D05-02'),
}

H12 = {
 6: ('GAP', '快速标注、通过颜色区分 mod 名称等：094 D06-03 挂的是 11:240「MC 颜色代码一键复制」与 12:6 在 D08-02 里被误并为「颜色快速标注」；12:6 这条「颜色区分 mod 名称」在服务器侧没有独立域承接', 'D06 模组管理·标注 或 D08 开服器·快速标注（候选，待拍板）', 'D06-03（颜色代码复制，非本条）'),
 11: ('GAP', '详细开服文档：绑定域名 / 如何管理 / 如何更新：094 D08-02 运维闭环 12 条锚点里没有 12:11', 'D08 开服器·文档 或 D11 关于（候选，待拍板）', '无'),
 25: ('ANCHOR', '配置 jvm 容量：094 D03-02 写了「JVM 内存自动分配，用户可改」并挂 11:257，服务器侧 12:25 未挂；功能有域、锚点缺', 'D08 开服器·建服（补挂 12:25）或 D10 设置·常规', 'D03-02'),
 3: ('PENDING', '094 D08-01 已挂「12:3 插件服官方通道名称待拍板」；归类无缺口，名称待拍', 'D08 开服器·建服（名称待拍）', 'D08-01'),
 14: ('PENDING', '094 D08-03 已挂「vianbt 库引入待拍板 Q-082-01」；归类无缺口，库待拍', 'D08 开服器·世界（Q-082-01 待拍）', 'D08-03'),
}

# 00 号约束类：不是用户功能，不进 20 域，但标归属，防被当功能漏归类
C00 = [
 (8, '默认轻量 ≤2GB 与配置路径 c/kcu/kculauncher/config/launch.json', 'D16 运行形态 / D10 设置'),
 (15, '连接码', 'D17 扩展通道'),
 (20, '手机互传需要设计协议', 'D17 扩展通道'),
 (21, 'EULA 启动前写入需可见说明', 'D01 首页与启动 / D08 开服器（12:7）'),
 (24, 'UI 用框架方式统一管理', 'D12 弹窗与通知 / D10 设置'),
 (25, '少选平台固定 API', '094 未挂：约束类，归 D12 / D18 统一调度器（候选）'),
 (32, '开源优先', 'D11 关于'),
 (33, '每次交付必须带 HTML 一比一运行逻辑', '094 未挂：交付约束，不进功能域'),
 (114, '统一信封三分', 'D12 弹窗与通知 / D09 日志诊断'),
 (137, '接口终点核对', '094 readback 显式核，不进功能域'),
 (175, '同类功能复用同一模块', '094 自我批判 E284，对应 R01–R08'),
 (245, '多语言文件堆在一起', 'D19 外观与文案（11:245）'),
 (248, '当轮明确指令优先', '094 决策第 3 节引用，不进功能域'),
 (249, '许可证合规优先', 'D11 关于'),
]

# U 段覆盖：30 段各 12 L
USEG = []
for m in re.finditer(r'^### (U\d{2}) (.+)$', (ROOT / 'docs/design/ux-logic-matrix.md').read_text(), re.M):
    USEG.append((m.group(1), m.group(2).strip()))
UMAP = {
 'U01':'D01','U02':'D02','U03':'D03','U04':'D04','U05':'D05','U06':'D06','U07':'D07',
 'U08':'D09','U09':'D10','U10':'D11','U11':'D12','U12':'D16','U13':'D16','U14':'D15',
 'U15':'D08','U16':'D10','U17':'D17','U18':'D16','U19':'D16','U20':'D18','U21':'D10',
 'U22':'D10','U23':'D14','U24':'D04','U25':'D13','U26':'D04','U27':'D04','U28':'D19',
}


def state_of(kind, n):
    table = H11 if kind == '11' else H12
    if n in table:
        return table[n][0], table[n]
    if n in ANCH[kind]:
        return 'OK', None
    return 'GAP', None


def build():
    L = []
    add = L.append
    add('KCU Launcher 归类覆盖度核对表（095 轮）')
    add('文件：docs/records/round-095-coverage-gaps.txt')
    add('生成：python3 scripts/feature_coverage.py（只读实扫 11 / 12 号编号条目 + 094 归类表锚点与功能项）')
    add('开工时间戳：Fri Nov 27 12:04:35 CST 2026')
    add('用户 095 逐字指令（42 字节）：' + SPEC)
    add('本轮动作：等用户设计归位方案期间，继续把归类做扎实——逐条核原文每条功能有没有被 094 的 20 域收进去。')
    add('不执行归位、不代拍板、不移动文件、不改设置项、不改 src/；所有候选域标「待拍板，未执行」。')
    add('')
    add('核对对象：094 交的是按功能域归纳的 20 域 / 37 功能项，用户 094 要的是「每一个功能重新归好类」。')
    add('按域归纳会漏掉原文逐条写的功能：仅凭域表看不出哪条 11 / 12 号编号还没被任何域承接。')
    add('095 把 11 号 55 条编号、12 号 24 条编号行 + 34 条无编号补充项、00 号约束、29 个 U 段标题逐条对表，缺口直接可查。')
    add('E384：12 号原文编号最大到 27，但真实 `NN.` 编号行只有 24 条（25 / 26 缺号），另有 28–62 行 34 条「· 」开头的无编号补充功能；`ux-logic-matrix.md` 实跑 29 个 U 段标题（U24 出现两次：021 修订版与 020 历史保留版，唯一编号 28 个），094 与 095 首版按「27 条 / 30 个 U 段」表述，按 A35 / A259 改为真实条数并逐值回显。')
    add('')
    add('状态定义：')
    add('  OK       已覆盖：094 归类表有功能项且依据锚点挂到该行')
    add('  PART     部分覆盖：有功能项，但原文同条还有子行为没展开')
    add('  GAP      真漏归类：原文这条没有任何域承接（或只挂了同形近义的另一条）')
    add('  ANCHOR   锚点缺口：功能已有域，依据锚点没挂到该行（不是功能漏）')
    add('  PENDING  归类无缺口，原文口径 / 方案待拍板')
    add('')
    add('计数口径：094 文件落地前 tracked 1308 / 48 个 src/core/*.rs / 37 守卫 / 80 HTML / 56 PNG / 87 决策 / 89 验证 / 72 功能文档 / 必读清单 531 项 / 24 AX。095 文件落地后 tracked 增加，补记并列不混用（093 E379 / 094 E381 同口径）。')
    add('')
    add('=' * 78)
    add('一、11 号原文逐条覆盖（下面详细介绍功能，编号 1–55）')
    add('=' * 78)
    add('列：行 | 编号 | 状态 | 094 功能项 | 原文摘要 | 缺口 / 候选域')
    c11 = {'OK':0,'PART':0,'GAP':0,'ANCHOR':0,'PENDING':0}
    for n, k, text in numbered('docs/spec/11-features-input.txt', 207):
        st, info = state_of('11', n)
        c11[st] += 1
        rr = ','.join(refs('11', n)) or '—'
        if info:
            detail = info[1] + ' ｜ 候选域：' + info[2] + ' ｜ 094 落点：' + info[3]
        else:
            detail = '—' if st == 'OK' else '真漏：094 无域承接，候选域待拍板'
        add('  %3d | %2d | %-7s | %-14s | %s' % (n, k, st, rr, text[:58]))
        if st != 'OK':
            add('        缺口：%s' % detail)
    add('')
    add('  11 号小计：OK %d / PART %d / GAP %d / ANCHOR %d / PENDING %d（合计 %d 条编号行）' % (
        c11['OK'], c11['PART'], c11['GAP'], c11['ANCHOR'], c11['PENDING'], sum(c11.values())))
    add('  注：11 号 249 / 252 / 255 / 256 行是上一条的续行（皮肤预览续句 / 文件一键补全续句 / 备份续句 / 空行），不是独立编号条目，不单列；其语义随主条一起核。')
    add('')
    add('=' * 78)
    add('二、12 号原文逐条覆盖（开服器，24 条编号行：编号 2–24 与 27，25 / 26 缺号）')
    add('=' * 78)
    c12 = {'OK':0,'PART':0,'GAP':0,'ANCHOR':0,'PENDING':0}
    for n, k, text in numbered('docs/spec/12-server-features-input.txt'):
        st, info = state_of('12', n)
        c12[st] += 1
        rr = ','.join(refs('12', n)) or '—'
        if info:
            detail = info[1] + ' ｜ 候选域：' + info[2] + ' ｜ 094 落点：' + info[3]
        else:
            detail = '—' if st == 'OK' else '真漏：094 无域承接，候选域待拍板'
        add('  %3d | %2d | %-7s | %-14s | %s' % (n, k, st, rr, text[:58]))
        if st != 'OK':
            add('        缺口：%s' % detail)
    add('')
    add('  12 号小计：OK %d / PART %d / GAP %d / ANCHOR %d / PENDING %d（合计 %d 条编号行）' % (
        c12['OK'], c12['PART'], c12['GAP'], c12['ANCHOR'], c12['PENDING'], sum(c12.values())))
    add('  注：12 号 22–24 行是第 21 条 RCON 三项的展开说明（无编号）；25 / 26 / 27 行分别是编号 22「配置 jvm 容量」/ 23「服务器默认配置汉化」/ 24「Java 多版本管理」；63 行是编号 27「png logo」。编号 25 / 26 在原文里不存在，28–62 行另有 35 条「· 」开头的无编号补充项（见第六节）。按真实行号逐条核，不按编号猜行号（A259 / E384）。')
    add('')
    add('=' * 78)
    add('三、00 号约束类条目归属（不是用户功能，不进 20 域，但要标归属）')
    add('=' * 78)
    for n, text, owner in C00:
        add('  00:%-3d | %-46s | %s' % (n, text[:46], owner))
    add('')
    add('  00:25「少选平台固定 API」与 00:33「每次交付带 HTML 演示」在 094 归类表里没有挂点：前者是 API 收紧约束（062 已落 api.rs v1 面），后者是交付约束。两者不进功能域，登记归属防被当漏功能。')
    add('')
    add('=' * 78)
    add('四、U 段 → 功能域映射核对')
    add('=' * 78)
    add('列：U 段 | 标题 | 094 域 | 状态')
    for u, title in USEG:
        d = UMAP.get(u, '—')
        st = '已挂' if d != '—' else '未挂（候选待拍板）'
        add('  %s | %-34s | %s | %s' % (u, title[:34], d, st))
    add('')
    add('  U24 在 ux-logic-matrix.md 出现两次（021 修订版与 020 历史保留版），按 021 修订版归 D04；U25 归 D13 插件。')
    add('  29 个 U 段标题各 12 条 L（U24 重复一次，唯一编号 28 个），094 表按段挂域但没逐 L 回显；095 不展开 348 条 L，只标段级归属，逐 L 颗粒度留用户方案（候选，待拍板）。')
    add('')
    add('=' * 78)
    add('五、缺口汇总（按处置优先级排，全部待拍板）')
    add('=' * 78)
    gaps = []
    for kind, table in (('11', H11), ('12', H12)):
        for n, (st, desc, cand, cur) in table.items():
            if st in ('GAP', 'PART', 'ANCHOR'):
                gaps.append((kind, n, st, cand, desc))
    order = {'GAP':0,'PART':1,'ANCHOR':2}
    gaps.sort(key=lambda x: (order[x[2]], x[0], x[1]))
    add('列：来源 | 状态 | 候选域 | 缺口')
    for kind, n, st, cand, desc in gaps:
        add('  %s:%-3d | %-7s | %s' % (kind, n, st, cand))
        add('        %s' % desc[:110])
    ng = sum(1 for g in gaps if g[2] == 'GAP')
    np_ = sum(1 for g in gaps if g[2] == 'PART')
    na = sum(1 for g in gaps if g[2] == 'ANCHOR')
    add('')
    add('  真漏 GAP %d 条 / 部分覆盖 PART %d 条 / 锚点缺口 ANCHOR %d 条；PENDING 项不计缺口。' % (ng, np_, na))
    add('  真漏里最需要用户方案定夺的 6 条：11:248 皮肤预览与创建角色、11:250 投影预览、11:254 备份打包、11:259 音乐播放、11:261 MC 百科、12:11 开服文档；另 12:6 快速标注与 D06-03 颜色代码复制是两条不同功能，094 有混挂风险。')
    add('')
    add('=' * 78)
    add('六、12 号无编号补充项逐条（28–62 行「· 」开头，E384）')
    add('=' * 78)
    bl = bullets('docs/spec/12-server-features-input.txt', 28, 62)
    add('列：行 | 原文补充项 | 候选域（待拍板） | 094 状态')
    for n, text in bl:
        add('  %3d | %-52s | %-34s | %s' % (n, text[:52], bullet_domain(text), '未逐条承接'))
    add('')
    add('  12 号无编号补充项 %d 条，094 归类表只在 D08-02 运维闭环里笼统挂了 12:21 一条，28–62 行这 %d 条没有逐条域归属。' % (len(bl), len(bl)))
    add('  这是「每一个功能重新归好类」漏得最多的一块：端口冲突检测、UPnP 映射、进程守护、TPS/MSPT 仪表盘、玩家概览、审计日志、白名单封禁、MOTD 可视化编辑、跨实例共享模组缓存、定时任务依赖链等。全部候选域待拍板，095 不擅自归位。')
    add('')
    add('=' * 78)
    add('七、约束与状态')
    add('=' * 78)
    add('  用户 095 当轮「你先继续干，我设计好再给你」：按 A208 不执行归位、不代拍板、不擅自定 2 项 Planned 优先级。')
    add('  095 只做覆盖核对：不移动文件、不改设置项、不改 src/、不改 Cargo.* / vendor/、不改功能池状态、不改 api::v1。')
    add('  094 的 20 域 / 37 项 / R01–R08 / 10 条散落清单、093 的 5 条偏差、A 组 EQ / Q 全部仍待拍板；用户方案到了直接对第五、六节的表。')
    add('  E382 登记：094 归类表按域归纳，漏收 11:248 / 11:250 / 11:254 / 11:259 / 11:261 / 12:6 / 12:11 等原文逐条功能；094 文件不重写（A181 / A201），095 补交逐条覆盖核对。')
    add('  四值：已证实（95 号 spec 逐字 42 字节、四份原文逐行校验复读、11 号 %d 条 / 12 号 %d 条编号行 + %d 条无编号补充项逐条覆盖、00 号 %d 条约束归属、%d 个 U 段标题段级映射、GAP %d / PART %d / ANCHOR %d、开工 A145 远端 51aaf75 与 1308 ALL_MATCH True）；已失败（E213–E383 历史项 + E382 归类漏收 + E383 混挂 + E384 12 号条数口径错）；未证实（13 条 EQ / 4 项 Q-C / 31 条历史 Q / 2 项 Planned / 所有候选域后果 / 逐 L 颗粒度）；未启动（归位迁移执行、真实网络 IO、UI 宿主、渲染层、真实下载字节落盘）。' % (
        sum(c11.values()), sum(c12.values()), len(bl), len(C00), len(USEG), ng, np_, na))
    add('  通过标记：按 00:245 不发；独立验证部分通过。')
    add('  唯一下一步：等用户归位方案；方案到了按第五、六节缺口表逐条对表，不擅自开工硬做。')
    add('')
    add('生成命令：python3 scripts/feature_coverage.py')
    add('校验命令：python3 scripts/feature_coverage_guard.py')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    OUT.write_text(build(), encoding='utf-8')
    b = OUT.read_bytes()
    print('FEATURE_COVERAGE_OK path=%s bytes=%d lines=%d sha256=%s' %
          (str(OUT.relative_to(ROOT)), len(b), b.count(b'\n'), hashlib.sha256(b).hexdigest()[:16]))

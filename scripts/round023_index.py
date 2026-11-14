from pathlib import Path

NEW = [
    'docs/spec/23-round-023-instructions.txt',
    'docs/decisions/023-architecture-answers.md',
    'docs/research/20-i18n-crash-identity.md',
    'docs/design/stable-identity.md',
    'docs/design/i18n-policy.md',
    'docs/design/crash-reporting.md',
    'docs/design/implementation-strategy.md',
    'docs/features/stable-identity-rename.md',
    'docs/features/i18n-crash-settings.md',
    'docs/verification/round-023.md',
    'scripts/round023_ux.py',
    'scripts/round023_i18n_cover.py',
    'scripts/round023_docs.py',
]


def upd(f, pairs):
    p = Path(f); t = p.read_text()
    for a, b in pairs:
        assert a in t, (f, a[:80])
        t = t.replace(a, b, 1)
    p.write_text(t); print('UPDATED', f)


# ---------- docs/index.md ----------
p = Path('docs/index.md'); t = p.read_text()
a = '109. scripts/round022_async.py\n\n读取命令：'
b = ('109. scripts/round022_async.py\n' +
     ''.join('%d. %s\n' % (110 + i, x) for i, x in enumerate(NEW)) +
     '\n读取命令：')
assert a in t; t = t.replace(a, b, 1)
t = t.replace('scripts/round022_async.py; do printf',
              'scripts/round022_async.py ' + ' '.join(NEW) + '; do printf', 1)
t = t.replace('必读顺序扩为 109 项', '必读顺序扩为 122 项', 1)
t = t.replace('37 张产品视图 PNG + 4 张内部证据图 + 00-overview.png 总览 + index.md',
              '43 张产品视图 PNG + 4 张内部证据图 + 00-overview.png 总览 + index.md', 1)
t = t.replace('022 轮 37 个产品视图缩略拼图', '023 轮 43 个产品视图缩略拼图', 1)
t = t.replace('`ls demos/preview/*.png \\| wc -l` = 42', '`ls demos/preview/*.png \\| wc -l` = 48', 1)
a2 = '| 022 异步与连接范围 | `grep -c \'budget-cell\'` = 4；`python3 scripts/p09_scan.py` = P09_HITS 0；`36-servers-budget.png` / `37-servers-history.png` 可见 |'
b2 = a2 + '\n| 023 标识 / i18n / 崩溃 | `grep -c "sid:\'sv-"` = 10；`41-i18n-en.png` / `39-servers-rename.png` / `42-settings-crash.png` 可见 |'
assert a2 in t; t = t.replace(a2, b2, 1)
a3 = '| 022 设计 | docs/design/ | async-probe-policy；取代 021 的同步遍历口径 |'
b3 = a3 + '\n| 023 设计 | docs/design/ | stable-identity、i18n-policy、crash-reporting、implementation-strategy |'
assert a3 in t; t = t.replace(a3, b3, 1)
t = t.replace('022 增 G22：异步预算与失败历史的用户可见口径', '023 增 G23：i18n 切换、改名、延迟小字、崩溃反馈的用户可见口径', 1)
t = t.replace('022 异步探测与设备连接范围、失败历史分类，37 张产品视图 + 4 张内部证据图；用户按手感调整后先改演示与截图、确认后才改实现。',
              '023 稳定标识、i18n、崩溃反馈、延迟小字、实现路线，43 张产品视图 + 4 张内部证据图；用户按手感调整后先改演示与截图、确认后才改实现。', 1)
p.write_text(t); print('INDEX_OK 122')

# ---------- README ----------
upd('README.md', [
    ('| 当前轮次 | 022 |', '| 当前轮次 | 023 |'),
    ('37 张产品视图 PNG', '43 张产品视图 PNG'),
    ('按设备能力限制同时连几台，范围外不连、无成功记录的不反复连 |',
     '按设备能力限制同时连几台，范围外不连、无成功记录的不反复连；稳定 ID 隔离同名、显示名可改 |'),
    ('| 使用逻辑矩阵 | docs/design/ux-logic-matrix.md，U01–U27 × L01–L12，022 新增 U27 |',
     '| 使用逻辑矩阵 | docs/design/ux-logic-matrix.md，U01–U28 × L01–L12，023 新增 U28 |'),
    ('022 增 G22（异步预算与失败历史口径），已交付 37 视图', '023 增 G23，已交付 43 视图'),
    ('F020-01..06、F021-01..04、F022-01..02 已实现、已验证 |',
     'F020-01..06、F021-01..04、F022-01..02、F023-01..02 已实现、已验证 |'),
    ('022 异步探测与连接范围，37 张产品视图；实现未进构建 |',
     '023 i18n / 崩溃反馈 / 稳定标识，43 张产品视图；实现未进构建 |'),
])

# ---------- 各类 index ----------
p = Path('docs/decisions/index.md'); t = p.read_text()
a = '| 022 | 异步探测、设备连接范围、失败历史分类、范围外与无成功记录排序 | 已批准 | 022-async-budget.md |'
assert a in t
p.write_text(t.replace(a, a + '\n| 023 | 六项质疑答复、稳定标识、i18n 选型、崩溃库分层、实现路线 | 已批准 | 023-architecture-answers.md |', 1))
print('DECISIONS_OK')

p = Path('docs/features/index.md'); t = p.read_text()
a = '| F022-02 | 失败历史分类与权重排序 | ui.demo / servers.rank | 已实现、已验证（演示层） | server-failure-history.md |'
assert a in t
t = t.replace(a, a + '\n| F023-01 | 稳定标识、同名与改名 | ui.demo / servers.identity | 已实现、已验证（演示层） | stable-identity-rename.md |\n| F023-02 | i18n 切换与崩溃反馈设置 | ui.demo / i18n + settings.crash | 已实现、已验证（演示层） | i18n-crash-settings.md |', 1)
a2 = '| G40 | 无成功案例且测过的不主动重连、按缓存权重排中段；曾成功但本轮失败沉底；锁定不受影响。 |'
assert a2 in t
t = t.replace(a2, a2 + '\n| G41 | 显示名不进路径；目录与缓存按稳定 ID；同名允许、改名不动 ID。 |\n| G42 | 界面文案走 key，日志与诊断行不本地化；语言包可插件追加。 |\n| G43 | 崩溃库默认不外发、脱敏默认开、发送前二次确认；Win7 降级本地 dump。 |', 1)
p.write_text(t); print('FEATURES_OK')

p = Path('docs/research/index.md'); t = p.read_text().replace('更新轮次：022', '更新轮次：023', 1)
t = t.rstrip() + '''

## 023 i18n / 崩溃 / 稳定标识 / 兼容性

| 项 | 文档 | 状态 |
| --- | --- | --- |
| 18 个完整 URL 锚点、J01-J07 结论、Q01-Q04 口径说明 | docs/research/20-i18n-crash-identity.md | 一手 15 组 + 公开资料 6 组 |
| Fluent / i18n-embed / Sentry SDK / minidump / Breakpad / Win7 Tier 3 / servers.dat 无 ID 字段 | 同上 | 已证实 |
'''
p.write_text(t); print('RESEARCH_OK')

p = Path('docs/rules/push-scope.md'); t = p.read_text().replace('轮次：022', '轮次：023', 1)
a = '| 022 调研与设计 | docs/research/19-async-probe-budget.md、docs/design/async-probe-policy.md |'
assert a in t
p.write_text(t.replace(a, a + '\n| 023 改造脚本 | scripts/round023_ux.py、scripts/round023_i18n_cover.py、scripts/round023_docs.py、scripts/round023_index.py |\n| 023 调研与设计 | docs/research/20-i18n-crash-identity.md、docs/design/ 四份策略文档 |', 1))
print('PUSHSCOPE_OK')

# ---------- 防错 / 闸门 ----------
p = Path('docs/checklists/ai-errors.md'); t = p.read_text()
a = '| A96 | 取消后仍写新结果（关联 022 A04） | `applyResult` 前检查 `PROBE.cancelled`；取消后 inflight 归零、队列清空 |'
assert a in t
t = t.replace(a, a + '''
| A97 | 用显示名拼目录 / 缓存键（关联 023 Q1） | SERVERS 每项带 `sid`；`data-lock` / `data-join` / `data-rename` 全用 sid；`C:\\KCU\\servers\\<sid>` 只含白名单字符 |
| A98 | 界面文案写死在渲染代码里（关联 023 Q2） | `grep -c 'data-i18n='` > 500；动态文本走 `tr()`；`41-i18n-en.png` 英文可见 |
| A99 | 崩溃信息默认外传（关联 023 Q5） | `setCrashOn` 默认不记录、`setCrashAddr` 可空、脱敏默认开、发送前确认 |
| A100 | 拿第三方库不登记许可证（关联 023 H02） | 关于页 22 组、`THIRD-PARTY-NOTICES.md` 新增 6 组候选均标「未进构建」 |''', 1)
p.write_text(t); print('AIERRORS_OK')

p = Path('docs/rules/ui-demo.md'); t = p.read_text().replace('轮次：022', '轮次：023', 1)
t = t.rstrip() + '''

## 023 增补

| 编号 | 项 | 值 |
| --- | --- | --- |
| G23 | i18n / 改名 / 延迟 / 崩溃反馈 | 动界面轮次必须给语言切换证据、改名弹窗、信号格具体延迟、崩溃反馈设置分组各一张截图 |

023 检查命令：

```
grep -c 'data-i18n=' demos/ui-full-kcu-paper.html
grep -c "sid:'sv-" demos/ui-full-kcu-paper.html
test -f demos/preview/41-i18n-en.png
test -f demos/preview/39-servers-rename.png
test -f demos/preview/42-settings-crash.png
python3 scripts/p09_scan.py
python3 scripts/render_ui.py
```

023 手感回路不变：先看图 → 提意见 → 先改演示与截图 → 确认后才改实现。本轮 `src/` 与 Cargo.lock 无变化。
'''
p.write_text(t); print('UIDEMO_OK')

# ---------- 矩阵 ----------
p = Path('docs/design/ux-logic-matrix.md'); t = p.read_text()
a = '## 022 自评迭代'
b = '''### U28 稳定标识 / i18n / 崩溃反馈（023）

| 编号 | 设计 |
| --- | --- |
| L01 | 标题栏语言按钮、设置常规语言项、服务器每行改名入口、设置崩溃反馈分组 |
| L02 | 同名允许、锁定与权重按 sid；默认语言跟随系统 |
| L03 | 缓存按 sid 分片；缺语言资源回退中文；dump 本地有界保留 |
| L04 | 切换语言即时生效；重新读取 servers.dat 不改 sid |
| L05 | 无 dump 给空态；无语言包回退中文不白屏 |
| L06 | 语言切换不重启；崩溃上报取消 0 外发 0 浮层 |
| L07 | 缺 key 显示兜底文案；崩溃发送失败保留本地 dump 并可见提示 |
| L08 | 改名弹窗 / 预览弹窗都支持按钮、ESC、×、宿主关闭，流程后 0 残留 |
| L09 | 崩溃发送前一次完整内容确认；脱敏默认开 |
| L10 | 中 / EN 按钮、同名标签、42 ms 延迟小字、诊断状态徽章 |
| L11 | 切换一次遍历、无网络；崩溃默认 0 常驻上报进程 |
| L12 | 服务器页、设置常规、设置崩溃反馈、关于页第三方许可 |

## 023 跨功能一致性检查

| 编号 | 检查 | 结果 |
| --- | --- | --- |
| C30 | 两台同名是否各自独立且带标签 | 已证实 |
| C31 | 改名后 sid 是否不变、排序与记录是否保留 | 已证实 |
| C32 | 英文界面导航 / 设置 / 按钮是否切换 | 已证实 |
| C33 | 信号格下是否显示具体毫秒 | 已证实 |
| C34 | 崩溃反馈默认是否不外发 | 已证实（演示层） |

## 023 自评迭代

| 轮次 | 自评 | 发现的不足 | 补入 |
| --- | --- | --- | --- |
| 迭代 1 | 7.0 | 只答了方案没改界面；目录键仍隐含名称；英文切换只覆盖导航 | sid 三分离、改名弹窗、i18n 字典初版 |
| 迭代 2 | 8.5 | 英文界面一半中文；自动标注脚本生成多余尖括号与 `&gt;` 转义；hash 正则吃掉场景名数字 | 扩到 550+ 标注点、修 HTML 形态、hash 正则支持数字 |
| 迭代 3 | 9.3 | 补齐 18 个一手锚点、43 张产品视图、崩溃分层与许可登记、实现路线映射表 | Q01-Q04、U28、C30-C34，收口 |

## 023 最终自评分项

| 维度 | 分 | 依据 |
| --- | --- | --- |
| 质疑逐条回应 | 9.6 | 六问全答，三处偏差承认并落改 |
| 架构路线清晰度 | 9.4 | 9 层映射 + 12 组库 + 7 条硬规则 |
| 一手调研 | 9.3 | 18 个完整 URL 锚点 |
| 界面证据 | 9.2 | 43 产品视图，英文 / 改名 / 延迟 / 崩溃各一张 |
| **综合** | **9.3** | 达 9 分线；扣分是真实运行时未实现与 Q01-Q04 待确认 |

## 022 自评迭代'''
assert a in t; t = t.replace(a, b, 1)
t = t.replace('021 修订 U24；022 新增 U27 与自评迭代', '021 修订 U24；022 新增 U27；023 新增 U28 与自评迭代', 1)
p.write_text(t); print('MATRIX_OK')

# ---------- preview index ----------
p = Path('demos/preview/index.md'); t = p.read_text()
t = t.replace('# 界面预览图索引（022 · 37 个产品视图）', '# 界面预览图索引（023 · 43 个产品视图）', 1)
t = t.replace('| 轮次 | 022 |', '| 轮次 | 023 |', 1)
t = t.replace('37 张产品截图 + 4 张内部证据图', '43 张产品截图 + 4 张内部证据图', 1)
t = t.replace('022 信息架构 | 一级导航 9 项；设置与关于固定在底部；扩展区独立；产品界面不出现工程叙事；服务器页加连接范围卡、范围外 / 暂不重试标签 |',
              '023 信息架构 | 一级导航 9 项；设置与关于固定在底部；扩展区独立；产品界面不出现工程叙事；标题栏语言切换、服务器改名、延迟小字、崩溃反馈分组 |', 1)
t = t.replace('只收 37 个产品视图，4 列 10 行，1462×2702', '只收 43 个产品视图，4 列 11 行，1462×2964', 1)
a = '| 37-servers-history.png | 轻量档与失败历史 | 2 台 / 2 路，无成功记录按权重排中段 |'
assert a in t
t = t.replace(a, a + '''
| 38-servers-latency.png | 信号格延迟 | 五格信号条下标 42 ms / 96 ms / 120 ms |
| 39-servers-rename.png | 改名弹窗 | 只改显示名，同名标签可见 |
| 40-servers-samenames.png | 同名服务器 | 两台同名不同地址，各自独立 |
| 41-i18n-en.png | English 界面 | 导航 / 设置 / 按钮 / 说明切换为英文 |
| 42-settings-crash.png | 崩溃反馈 | 默认不外发、脱敏开、可导出 |
| 43-licenses-updated.png | 第三方许可 | 新增 6 组候选库登记 |''', 1)
p.write_text(t); print('PREVIEW_OK')

# ---------- interface log ----------
p = Path('docs/records/interface-log.md'); t = p.read_text()
a = '## 版本弃用'
b = '''## 023 标识 / i18n / 崩溃反馈

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I67 | `tr(k, fb)` / `applyI18n()` / `setLang(l)` | key / locale | 本地化文本 | 缺 key 回退 fb |
| I68 | `openRename(s)` / `data-rename` | sid | 改名弹窗 | 空名不保存 |
| I69 | `setCrashOn` / `setCrashAddr` / `setCrashMask` | 值 | 崩溃策略 | 无 |
| I70 | `crashView` / `crashExport` | 无 | 预览 / 本地导出 | 无 dump 空态 |
| I71 | `servers-rename` / `servers-samenames` / `i18n-en` 路由别名 | 无 | 演示场景 | 无 |

| 编号 | 内容 |
| --- | --- |
| RO75 | 023 对后端仓 0 个写请求，约束延续 RO01-RO74。 |
| RO76 | spec 逐字副本 1 行 698 字节，SHA-1 `a473ce3dfc83cad84b35991e6053358ccfbd234a`。 |
| RO77 | `sid = UUIDv5(KCU_NAMESPACE, normalize(ip:port))`；目录与缓存只按 sid；显示名可重复可改。 |
| RO78 | 演示层 550+ 个 `data-i18n` 标注点；日志与 `[KCU]` 诊断行不进字典。 |
| RO79 | 崩溃库四层候选全部标「未进构建」；默认不记录、脱敏开、发送前确认、Win7 降级本地 dump。 |
| RO80 | 43 张产品截图 / 4 张内部证据图 / 1 张总览；26 区块、26 逻辑条、88 symbol、10 个设置 tab-pane。 |
| RO81 | Q01-Q04 为本轮自主拍板口径，待用户确认，只落 docs/，不写进产品界面。 |

## 版本弃用'''
assert a in t; p.write_text(t.replace(a, b, 1))
print('INTERFACE_OK')

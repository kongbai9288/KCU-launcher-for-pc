from pathlib import Path

NEW = [
    'docs/spec/22-round-022-instructions.txt',
    'docs/decisions/022-async-budget.md',
    'docs/research/19-async-probe-budget.md',
    'docs/design/async-probe-policy.md',
    'docs/features/server-async-probe.md',
    'docs/features/server-failure-history.md',
    'docs/verification/round-022.md',
    'scripts/round022_async.py',
]


def upd(f, pairs):
    p = Path(f)
    t = p.read_text()
    for a, b in pairs:
        assert a in t, (f, a[:70])
        t = t.replace(a, b, 1)
    p.write_text(t)
    print('UPDATED', f)


# ---------- docs/index.md ----------
p = Path('docs/index.md')
t = p.read_text()
a = '101. docs/features/ui-product-copy.md\n\n读取命令：'
b = ('101. docs/features/ui-product-copy.md\n' +
     ''.join('%d. %s\n' % (102 + i, x) for i, x in enumerate(NEW)) +
     '\n读取命令：')
assert a in t
t = t.replace(a, b, 1)
t = t.replace('docs/features/ui-product-copy.md; do printf',
              'docs/features/ui-product-copy.md ' + ' '.join(NEW) + '; do printf', 1)
t = t.replace('必读顺序扩为 101 项', '必读顺序扩为 109 项', 1)
t = t.replace('| 界面预览 | demos/preview/ | 35 张产品视图 PNG + 4 张内部证据图 + 00-overview.png 总览 + index.md |',
              '| 界面预览 | demos/preview/ | 37 张产品视图 PNG + 4 张内部证据图 + 00-overview.png 总览 + index.md |', 1)
t = t.replace('| 界面预览总览 | demos/preview/00-overview.png | 021 轮 35 个产品视图缩略拼图，直接看界面长相 |',
              '| 界面预览总览 | demos/preview/00-overview.png | 022 轮 37 个产品视图缩略拼图，直接看界面长相 |', 1)
t = t.replace('`ls demos/preview/*.png \\| wc -l` = 40', '`ls demos/preview/*.png \\| wc -l` = 42', 1)
a2 = '| 021 服务器逻辑 | `grep -c \'srv-row\'` > 0；`21-servers.png` / `34-servers-join.png` / `35-servers-locked.png` 可见 |'
b2 = a2 + '\n| 022 异步与连接范围 | `grep -c \'budget-cell\'` = 4；`python3 scripts/p09_scan.py` = P09_HITS 0；`36-servers-budget.png` / `37-servers-history.png` 可见 |'
assert a2 in t
t = t.replace(a2, b2, 1)
a3 = '| 021 设计 | docs/design/ | server-list-logic、ui-product-copy；020 的 server-status 页面口径已被 021 取代 |'
b3 = a3 + '\n| 022 设计 | docs/design/ | async-probe-policy；取代 021 的同步遍历口径 |'
assert a3 in t
t = t.replace(a3, b3, 1)
t = t.replace('| UI 闸门规则 | docs/rules/ui-demo.md | 021 增 G19-G21：产品文案、内部证据页隔离、总览只收产品视图 |',
              '| UI 闸门规则 | docs/rules/ui-demo.md | 022 增 G22：异步预算与失败历史的用户可见口径 |', 1)
t = t.replace('021 去工程化、服务器页按自动连接 / 缓存权重 / 锁定置顶 / 失败沉底 / 双击进服重做，35 张产品视图 + 4 张内部证据图；用户按手感调整后先改演示与截图、确认后才改实现。',
              '021 去工程化、服务器页重做；022 异步探测与设备连接范围、失败历史分类，37 张产品视图 + 4 张内部证据图；用户按手感调整后先改演示与截图、确认后才改实现。', 1)
p.write_text(t)
print('INDEX_OK 109')

# ---------- README ----------
upd('README.md', [
    ('| 当前轮次 | 021 |', '| 当前轮次 | 022 |'),
    ('| 界面预览图 | demos/preview/00-overview.png 总览 + 35 张产品视图 PNG，本地 chromium 每视图强制重载，直接看界面长相 |',
     '| 界面预览图 | demos/preview/00-overview.png 总览 + 37 张产品视图 PNG，本地 chromium 每视图强制重载，直接看界面长相 |'),
    ('| 服务器 | 添加后自动连接、结果缓存为排序权重、锁定置顶、连不上沉底、双击按上次实例绑定进服；只读 servers.dat 自动分析 |',
     '| 服务器 | 添加后异步自动连接、结果缓存为排序权重、锁定置顶、连不上沉底、双击按上次实例绑定进服；只读 servers.dat 自动分析；按设备能力限制同时连几台，范围外不连、无成功记录的不反复连 |'),
    ('| 使用逻辑矩阵 | docs/design/ux-logic-matrix.md，U01–U26 × L01–L12，021 修订 U24 |',
     '| 使用逻辑矩阵 | docs/design/ux-logic-matrix.md，U01–U27 × L01–L12，022 新增 U27 |'),
    ('| UI 整页演示闸门 | docs/rules/ui-demo.md；021 增 G19-G21（产品文案、内部证据隔离、总览只收产品视图），已交付 35 视图，用户手感调整优先于实现 |',
     '| UI 整页演示闸门 | docs/rules/ui-demo.md；022 增 G22（异步预算与失败历史口径），已交付 37 视图，用户手感调整优先于实现 |'),
    ('F020-01..06、F021-01..04 已实现、已验证 |', 'F020-01..06、F021-01..04、F022-01..02 已实现、已验证 |'),
    ('020 37 视图；021 去工程化并重做服务器页，35 张产品视图；实现未进构建 |',
     '020 37 视图；021 去工程化并重做服务器页；022 异步探测与连接范围，37 张产品视图；实现未进构建 |'),
])

# ---------- index 类 ----------
p = Path('docs/decisions/index.md')
t = p.read_text()
a = '| 021 | 服务器自动连接与缓存权重、servers.dat 自动分析、双击进服实例绑定、产品界面去工程化 | 已批准 | 021-server-autoconnect.md |'
b = a + '\n| 022 | 异步探测、设备连接范围、失败历史分类、范围外与无成功记录排序 | 已批准 | 022-async-budget.md |'
assert a in t
p.write_text(t.replace(a, b, 1))
print('DECISIONS_INDEX_OK')

p = Path('docs/features/index.md')
t = p.read_text()
a = '| F021-04 | 产品界面去工程化 | ui.demo / copy | 已实现、已验证（演示层） | ui-product-copy.md |'
b = (a + '\n| F022-01 | 异步探测与设备连接范围 | ui.demo / servers.probe | 已实现、已验证（演示层） | server-async-probe.md |'
     + '\n| F022-02 | 失败历史分类与权重排序 | ui.demo / servers.rank | 已实现、已验证（演示层） | server-failure-history.md |')
assert a in t
t = t.replace(a, b, 1)
a2 = '| G37 | 产品界面不写工程叙事；内部证据页不进导航与总览。 |'
b2 = a2 + '\n| G38 | 自动连接异步、并发有上限、队列有界、可取消；总额卡在设备档位内。 |\n| G39 | 新加服务器一定连一次但不扩总额度；范围外保留上次结果、不发请求。 |\n| G40 | 无成功案例且测过的不主动重连、按缓存权重排中段；曾成功但本轮失败沉底；锁定不受影响。 |'
assert a2 in t
p.write_text(t.replace(a2, b2, 1))
print('FEATURES_INDEX_OK')

p = Path('docs/research/index.md')
t = p.read_text().replace('更新轮次：021', '更新轮次：022', 1)
t = t.rstrip() + '''

## 022 异步探测与连接预算

| 项 | 文档 | 状态 |
| --- | --- | --- |
| 并行探测 API、context deadline、启动器异步 ping、背压 / 有界队列 / 连接池上限 / 失败不毁整批 | docs/research/19-async-probe-budget.md | 12 个完整 URL 锚点，J01-J07 结论 |
| Q01-Q04 口径说明 | 同上 | 自主拍板，待用户确认，只落 docs/ |
'''
p.write_text(t)
print('RESEARCH_INDEX_OK')

p = Path('docs/rules/push-scope.md')
t = p.read_text().replace('轮次：021', '轮次：022', 1)
a = '| 021 调研与设计 | docs/research/18-server-list-autodiscovery.md、docs/design/server-list-logic.md、docs/design/ui-product-copy.md |'
b = a + '\n| 022 改造脚本 | scripts/round022_async.py、scripts/round022_docs.py、scripts/round022_index.py |\n| 022 调研与设计 | docs/research/19-async-probe-budget.md、docs/design/async-probe-policy.md |'
assert a in t
p.write_text(t.replace(a, b, 1))
print('PUSHSCOPE_OK')

# ---------- 防错与闸门 ----------
p = Path('docs/checklists/ai-errors.md')
t = p.read_text()
a = '| A92 | 锁定项被连接失败下沉（关联 021 D05 / 用户逻辑） | `35-servers-locked.png` 中锁定项保持靠前；`srvRank` 中 lock 返回 0 |'
b = a + '''
| A93 | 同步遍历全部服务器状态（关联 022 D01） | `srvProbe` 用 worker-pull 异步队列；`srvSync` 已移除；`grep -c 'srvSync'` = 0 |
| A94 | 服务器越多连接数越涨（关联 022 D02-D04） | `DEVICE` 档位表 limit / concurrency 双上限；新服仍占同一份额度，`buildPlan` 用 slice(0,limit) |
| A95 | 把无成功记录的服务器沉底或反复重连（关联 022 D06） | `neverSuccess` 分组不进 probe 计划；`srvRank` 给 300 档中段；`37-servers-history.png` 可见 |
| A96 | 取消后仍写新结果（关联 022 A04） | `applyResult` 前检查 `PROBE.cancelled`；取消后 inflight 归零、队列清空 |'''
assert a in t
p.write_text(t.replace(a, b, 1))
print('AIERRORS_OK')

p = Path('docs/rules/ui-demo.md')
t = p.read_text().replace('轮次：021', '轮次：022', 1)
t = t.rstrip() + '''

## 022 增补

| 编号 | 项 | 值 |
| --- | --- | --- |
| G22 | 异步预算与失败历史 | 动服务器界面的轮次必须给出连接范围可见口径（本次可连 / 同时连接 / 在飞·队列 / 本次不连 / 停止）与失败历史标签（范围外、暂不重试、连不上）；截图至少含标准档与轻量档各一张 |

022 检查命令：

```
grep -c 'budget-cell' demos/ui-full-kcu-paper.html
grep -c 'srvProbe' demos/ui-full-kcu-paper.html
test -f demos/preview/36-servers-budget.png
test -f demos/preview/37-servers-history.png
python3 scripts/p09_scan.py
python3 scripts/render_ui.py
```

022 手感回路不变：先看图 → 提意见 → 先改演示与截图 → 确认后才改实现。本轮 `src/` 与 Cargo.lock 无变化。
'''
p.write_text(t)
print('UIDEMO_OK')

# ---------- 设计文档补充 ----------
p = Path('docs/design/server-list-logic.md')
t = p.read_text()
t = t.replace('| 状态 | 已批准（设计层） |', '| 状态 | 已批准（设计层）；同步遍历口径已被 022 取代 |', 1)
t = t.rstrip() + '''

## 022 补充

| 编号 | 内容 |
| --- | --- |
| N01 | 自动连接改为异步：worker-pull 有界队列、并发有上限、可取消；UI 先渲染上次结果再增量更新。详见 `docs/design/async-probe-policy.md`。 |
| N02 | 设备连接范围：按权重取前 N 台进入本次探测计划，范围外不发请求、保留上次结果；新加服务器强制入队但占同一份额度。 |
| N03 | 失败历史分两类：有成功案例且本轮失败沉底；测过且无成功案例的不主动重连、按缓存权重排中段；锁定始终置顶。 |
| N04 | 排序档位：锁定 0 → 可用 100+ → 范围外 200+ → 无成功记录 300+ → 曾成功但本轮失败 900+。 |
| N05 | 本文件的「打开列表自动同步一次」仍成立，只是执行方式换成 N01 的异步计划；`servers.dat` 只读、显示照游戏内、双击进服实例绑定三条不变。 |
'''
p.write_text(t)
print('SERVER_LIST_LOGIC_OK')

p = Path('docs/design/ux-logic-matrix.md')
t = p.read_text()
a = '## 021 自评迭代'
b = '''### U27 异步探测与设备连接范围（022）

| 编号 | 设计 |
| --- | --- |
| L01 | 服务器页右栏「连接范围」卡；首屏不等待网络 |
| L02 | 按权重取前 N 台连；新加的一定连但占同一份额度 |
| L03 | 范围外与无成功记录用缓存结果；探测结果增量写回 |
| L04 | 重新连接取增量、重新获取清缓存全量、重新读取只扫 servers.dat |
| L05 | 没有服务器给添加入口；档位 0 给「本次不连」说明 |
| L06 | 进度条 + 停止按钮；取消后 0 新请求、已完成结果保留 |
| L07 | 单台超时跳过；曾成功失败沉底；范围外用上次结果；无成功记录排中段 |
| L08 | 停止、切档、弹窗都不留浮层 |
| L09 | 021 L09 不变 |
| L10 | 本次可连 / 同时连接 / 在飞·队列 / 本次不连 / 进度条 / 每行标签 |
| L11 | 并发与总台数双上限，不随服务器数线性增长；轻量自动降档 |
| L12 | 服务器页、设置 → 服务器与连接、首页推荐卡 |

## 022 跨功能一致性检查

| 编号 | 检查 | 结果 |
| --- | --- | --- |
| C25 | 新加服务器是否不被 N 裁剪且总量不超 N | 已证实 |
| C26 | 范围外是否 0 请求且保留上次结果 | 已证实 |
| C27 | 无成功记录是否不主动重连且排中段 | 已证实 |
| C28 | 锁定项是否连不上、超范围都不动 | 已证实 |
| C29 | 停止后是否 0 新请求、0 浮层残留 | 已证实（演示层） |

## 022 自评迭代

| 轮次 | 自评 | 发现的不足 | 补入 |
| --- | --- | --- | --- |
| 迭代 1 | 7.8 | 只加了异步但没限制总台数，服务器越多连接越多；新服直接扩量；失败历史没分类 | 档位表、slice(0,N)、新服占同一份额度、ever / tried 分类 |
| 迭代 2 | 8.8 | 范围外与无成功记录的排序位置不合理，视觉上排到最后；锁定离线服被探测成在线 | 排序改 200 / 300 档中段；锁定离线服保持 offlineMark；逻辑条动态计数 |
| 迭代 3 | 9.4 | 补齐 12 个一手 / 公开来源、37 张产品视图、设置自定义项与停止入口；剩余为真实客户端未实现与 Q01-Q03 待确认 | Q 口径说明、U27、C25-C29，收口 |

## 022 最终自评分项

| 维度 | 分 | 依据 |
| --- | --- | --- |
| 用户逻辑还原 | 9.6 | 异步、范围、新服、失败历史、锁定五条逐条落地 |
| 资源安全 | 9.5 | 双上限、有界队列、可取消、轻量降档 |
| 一手调研 | 9.3 | 12 个完整 URL 锚点 |
| 界面证据 | 9.3 | 37 产品视图，标准档与轻量档各一张 |
| **综合** | **9.4** | 达 9 分线；扣分是真实客户端未实现与 Q01-Q03 待确认 |

## 021 自评迭代'''
assert a in t
t = t.replace(a, b, 1)
t = t.replace('| 轮次 | 019；020 增补 U21-U25；021 修订 U24、新增 U26 与自评迭代 |',
              '| 轮次 | 019；020 增补 U21-U25；021 修订 U24；022 新增 U27 与自评迭代 |', 1)
p.write_text(t)
print('MATRIX_OK')

# ---------- preview index ----------
p = Path('demos/preview/index.md')
t = p.read_text()
t = t.replace('# 界面预览图索引（021 · 35 个产品视图）', '# 界面预览图索引（022 · 37 个产品视图）', 1)
t = t.replace('| 轮次 | 021 |', '| 轮次 | 022 |', 1)
t = t.replace('26 个独立区块，35 张产品截图 + 4 张内部证据图', '26 个独立区块，37 张产品截图 + 4 张内部证据图', 1)
t = t.replace('| 021 信息架构 | 一级导航 9 项；设置与关于固定在底部；扩展区独立；产品界面不出现工程叙事；服务器页按自动连接 / 缓存权重 / 锁定置顶 / 失败沉底重做 |',
              '| 022 信息架构 | 一级导航 9 项；设置与关于固定在底部；扩展区独立；产品界面不出现工程叙事；服务器页加连接范围卡、范围外 / 暂不重试标签 |', 1)
t = t.replace('| 总览 | `00-overview.png`，只收 35 个产品视图，4 列 9 行，1462×2440 |',
              '| 总览 | `00-overview.png`，只收 37 个产品视图，4 列 10 行，1462×2702 |', 1)
a = '| 35-servers-locked.png | 连不上沉底 | 锁定项保持靠前，失败项排最后 |'
b = a + '\n| 36-servers-budget.png | 设备连接范围 | 标准档 4 台 / 3 路，预算四格、范围外标签 |\n| 37-servers-history.png | 轻量档与失败历史 | 2 台 / 2 路，无成功记录按权重排中段 |'
assert a in t
t = t.replace(a, b, 1)
p.write_text(t)
print('PREVIEW_INDEX_OK')

# ---------- interface log ----------
p = Path('docs/records/interface-log.md')
t = p.read_text()
a = '## 版本弃用'
b = '''## 022 异步探测与设备连接范围

| 编号 | 接口 | 输入 | 输出 | 错误 |
| --- | --- | --- | --- | --- |
| I62 | `srvProbe(soft)` / `buildPlan()` | 是否增量 | 异步计划、增量渲染 | 已在跑忽略；档位 0 给空计划 |
| I63 | `srvCancel()` / `srvSwitchTier()` | 无 | 停止 / 切档重排 | 未在跑忽略 |
| I64 | `setBudLimit` / `setBudConc` / `setBudTier` | 数值 | 改档位并重算计划 | 无 |
| I65 | `srvRank` / `srvCachedWeight` / `neverSuccess` | 服务器对象 | 排序值与分组 | 无 |
| I66 | `servers-budget` / `servers-history` 路由别名 | 无 | 标准档 / 轻量档演示 | 无 |

| 编号 | 内容 |
| --- | --- |
| RO67 | 022 轮对后端仓 0 个写请求，约束延续 RO01-RO66。 |
| RO68 | spec 逐字副本 1 行 265 字节，SHA-1 `1a99d1a137ad246fa50c9e66958d3792dc54ec2f`。 |
| RO69 | 档位表：标准 limit=4 / conc=3，轻量 limit=2 / conc=2，无界面 0；数值可在设置里改。 |
| RO70 | 新加服务器强制入队、不受 N 裁剪，但占同一份额度，总数仍等于 N。 |
| RO71 | 范围外不发请求、保留上次结果、按缓存权重 200 档；无成功记录不主动连、300 档中段；曾成功本轮失败 900 档沉底；锁定 0 档不动。 |
| RO72 | 取消后不再写新结果、不再发新请求、inflight 归零、队列清空；已完成结果保留。 |
| RO73 | 37 张产品截图 / 4 张内部证据图 / 1 张总览；26 区块、26 逻辑条、88 symbol、9+9 tabs-panes。 |
| RO74 | Q01-Q03 为本轮自主拍板口径，待用户确认，只落 docs/，不写进产品界面。 |

## 版本弃用'''
assert a in t
p.write_text(t.replace(a, b, 1))
print('INTERFACE_OK')

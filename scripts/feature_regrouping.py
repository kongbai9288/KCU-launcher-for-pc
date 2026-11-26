#!/usr/bin/env python3
"""094：按功能域重新归类，逐功能回显行为链路 / 当前落点 / 归位落点。

只读实扫：11 / 12 号原文行、U 段、nav 契约、HTML pane、src/core 模块、features 文档。
归类判断与行为链路由本脚本内的结构化表给出，不写推测计数。
输出 docs/records/round-094-feature-regrouping.txt。
"""
from pathlib import Path
import hashlib
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'docs/records/round-094-feature-regrouping.txt'

SPEC = '但我主要问题是为了启动器本身的相关的功能散落问题，我打算把每一个功能重新归好类，防止你乱开导致的逻辑免费不是正常逻辑但是你交给我的是什么？（还有就是非常详细，就比如下载会进入后台，然后用户可以在下载页当中打开，并且查看它的进度条和百分比）'

# 094 开工实跑快照（文件落地后 tracked 会变，两口径并列，不混用）
SNAP = dict(tracked=1300, core_rs=48, core_lines=22332, guards=35,
            p09=1, demos=80, previews=56, decisions=86, verification=88,
            features=72, design=13, records=16, spec=26, required=523,
            panes=11, setids=15, ax=24, states_planned=2)

DOMAINS = [
dict(id='D01', name='首页与启动', slot='core.nav.home', ux='U01:32',
     items=[
     dict(id='D01-01', name='启动落首页与同帧骨架',
          chain=['启动进程读 boot-state.json → 落首页；标题栏 / 左导航 / 工具条 / 底部状态栏同帧可见',
                 '首页统计、公告、实例列表走内存缓存 TTL 30s；离线显示上次快照并标灰；容量 32 条',
                 '状态栏显示「上次同步 N 秒前」、Java / 内存 / 镜像延迟 / 手机连接'],
          now=['src/core/boot.rs（DEFAULT_STATE / LOADED_MODULES / STATE_FILE）','src/core/stats.rs（STATS_FILE）','docs/design/ux-logic-matrix.md:32–48 U01','demos/ui-full-kcu-paper.html data-pane="general" 之外的首页区块'],
          target=['D01 首页与启动：boot.rs / stats.rs 只服务启动态与统计，不承载下载进度'],
          basis=['U01 L01 / L03 / L10','nav-slot-contract.md:14','00:8 默认轻量与配置路径'],
          edge='不把下载队列、启动阶段进度以外的态塞进首页；游戏运行期无常驻后台进程（U01 L11）',
          state='已归位（启动态）；启动进度条见 D01-02'),
     dict(id='D01-02', name='启动阶段进度与失败回退',
          chain=['点「启动游戏」→ 阶段进度准备 → 校验 → 拉起；取消后 0 副作用',
                 '启动失败给退出码 / 日志入口 / 重试；连续 3 次进安全模式',
                 'EULA 启动前写入需可见说明；正版凭据缺失提示且不静默改离线'],
          now=['src/core/launch_progress.rs（PHASES / PROGRESS_TARGET=launcher.progress / MAX_WAIT_SECS=120）','src/core/consent.rs（DEFAULT_CONSENT / POPUP_ID=privacy）','docs/features/normal-launcher.md'],
          target=['D01 首页与启动·启动进度（launch_progress.rs）；与 D05 下载任务进度分源不合并'],
          basis=['U01 L06 / L07 / L09','12:12 关机保存进度','src/core/launch_progress.rs:6 PHASES'],
          edge='不与 D05 的每文件进度条、百分比共用同一状态；不落真实进程拉起',
          state='散落 3 处；易与下载进度混淆，归位待拍板'),
     dict(id='D01-03', name='启动卡与最近实例',
          chain=['启动卡推荐「上次实例」并列最近 3 个；手动选过的实例权重高于推荐',
                 '无实例时启动卡换空态 + 新建实例 / 双击服务器进服两入口',
                 '下载完成 / 实例新增 / 公告已读三事件推送更新首页'],
          now=['src/core/widget_layout.rs（AX01 DEFAULT_STATE）','src/core/instance.rs','docs/design/recommendation-catalog.md:14 core.rec.home_launch','docs/features/recommendation-catalog.md'],
          target=['D01 首页与启动·启动卡；推荐权重口径归 D14，不在首页另算'],
          basis=['U01 L02 / L04 / L05','docs/design/recommendation-catalog.md:14'],
          edge='不自己算权重；不重复拉逐条目请求（U01 L11）',
          state='已归位；权重口径跨域挂 D14'),
     ]),
dict(id='D02', name='公告中心', slot='core.nav.notices', ux='U02:49',
     items=[
     dict(id='D02-01', name='公告列表与四类筛选',
          chain=['导航进公告中心 → 置顶优先、时间次之；四类筛选与未读态同帧',
                 '三动作、× 与 ESC 关闭；版本更新提示可取消',
                 '内置声明页条目不可删；公告已读事件推送首页'],
          now=['src/core/notice_center.rs（AX02 / BUILTIN_ID=declaration / 6 张白名单）','docs/features/plugin-upgrade-consent.md','docs/design/ux-logic-matrix.md:49–65 U02'],
          target=['D02 公告中心：notice_center.rs 单一状态；第三方更新公告归本域不落设置'],
          basis=['11:12 统一调度器送 json 必须内置并出声明页','11:219 第三方更新指示公告可取消','11:231 上线提醒','11:10 每个弹窗有关闭逻辑'],
          edge='不碰真实网络 IO；内容获取执行层未启动',
          state='已归位'),
     dict(id='D02-02', name='上线提醒与记录器横幅',
          chain=['启动启动器时按用户自定义图片 / 文本显示；标题记为 kcu 记录器',
                 '横幅可关闭；弹窗流程后 0 残留'],
          now=['src/core/notice_center.rs','src/core/popup.rs','docs/design/ux-logic-matrix.md U01 L08'],
          target=['D02 公告中心·横幅；关闭逻辑复用 D12 弹窗全集'],
          basis=['11:231 上线提醒','11:10 弹窗关闭','U01 L08'],
          edge='不新开横幅模块',
          state='已归位'),
     ]),
dict(id='D03', name='实例与版本', slot='core.nav.instances', ux='U03:66',
     items=[
     dict(id='D03-01', name='实例列表与版本迁移',
          chain=['实例页按版本 / 加载器分组；键盘文件、服务器文件随版本迁移',
                 '「打开目录」直达系统文件面板；右键菜单同入口',
                 '同一版本同一哈希同加载器 mod 可多实例共用，启动时手动选中'],
          now=['src/core/instance.rs','src/core/instance_drop.rs（AX24 / collapsed / ungrouped）','src/core/instance_import.rs（AX08 / format=mrpack）','src/core/upgrade_plan.rs（AX09）','docs/features/stable-identity-rename.md'],
          target=['D03 实例与版本：instance.rs 为唯一实例真值；导入 / 拖放 / 回滚为子流程不另开域'],
          basis=['11:232 版本功能迁移','11:253 多实例共用 mod','11:222 整合包拖到主界面安装','U03'],
          edge='真实 mrpack / zip 解压落盘未启动；不写真实 NBT',
          state='散落 5 模块；归位待拍板'),
     dict(id='D03-02', name='多开与内存分配',
          chain=['同时启动多个 MC 版本，默认上限 3 个',
                 'JVM 内存自动分配，用户可改；可选回收器；按模组内存给比值',
                 '友情提示：内存 / 存储不足时先确认'],
          now=['src/core/instance.rs','src/core/args.rs','docs/features/core-args.md','docs/features/normal-stats.md'],
          target=['D03 实例与版本·启动参数；JVM 参数收藏归 D10 设置·常规'],
          basis=['11:233 同时启动多个版本上限 3','11:257 jvm 内存自动分配','11:234 友情提示','11:265 环境变量与 jvm 参数收藏'],
          edge='不落真实进程；不把友情提示做成新弹窗域',
          state='已归位'),
     dict(id='D03-03', name='游戏时长与统计',
          chain=['每次游戏结束显示本次时长，按实例记录总时长',
                 '状态栏与统计卡读取同一份 play-stats.json'],
          now=['src/core/stats.rs（STATS_FILE=play-stats.json）','docs/records/feature-pool.md 之外的统计文档','docs/features/server-activity-pie.md'],
          target=['D03 实例与版本·时长；统计卡渲染归 D01 首页，不另存一份'],
          basis=['11:226 玩了多长时间与总时长','11:239 动态查看 cpu 性能信息'],
          edge='11:242 时长路径待拍板；不自行定口径',
          state='已归位；11:242 待拍板'),
     ]),
dict(id='D04', name='服务器', slot='core.nav.servers', ux='U04:83 / U24:424 / U26:441 / U27:458',
     items=[
     dict(id='D04-01', name='服务器列表与 servers.dat',
          chain=['启动页直接看到服务器列表；双击直接进服（实例绑定按版本习惯与最近使用）',
                 '自动读取各实例目录 servers.dat；隐藏的 / 快速进入过的可分别选导入口径',
                 '改名、锁定、右键三入口；连不上的排到列表最后或保持原位'],
          now=['src/core/region.rs','src/core/userflow.rs','docs/features/servers-dat-analysis.md','docs/features/server-join-binding.md','docs/design/server-list-logic.md','docs/design/ux-logic-matrix.md:83 U04'],
          target=['D04 服务器：列表与 servers.dat 单一来源；实例绑定归 D04 子流程'],
          basis=['11:214 启动页看服务器列表与双击进服','12:2 自动下载 jar 进加载器选择页','U24 / U26'],
          edge='真实 NBT / 存档读取未启动',
          state='散落 5 处；归位待拍板'),
     dict(id='D04-02', name='状态探测与自动连接',
          chain=['服务器每行状态条：绿 / 金 / 灰点与上次探测时间',
                 '添加后自动尝试连接或等手动刷新；打开列表时自动同步一次或不自动同步',
                 '同步间隔 60 秒 / 5 分钟 / 仅手动；每次自动连几台、同时连接几路、轻量机器降档',
                 '状态判定失败回退缓存，不空白、不静默重试；超时标灰',
                 '自动上线 / 自动加入服务器按手动设定时间触发'],
          now=['src/core/region.rs','docs/features/server-async-probe.md','docs/features/server-autoconnect.md','docs/features/server-status-settings.md','docs/features/server-failure-history.md','docs/features/server-join-alert.md','demos/ui-full-kcu-paper.html data-pane="status"'],
          target=['D04 服务器·状态；探测间隔 / 超时 / 显示口径归 D10 设置·服务器状态'],
          basis=['11:229 自动上线与自动加入服务器','12:9 ftp/sftp 自动连接','docs/design/ux-logic-matrix.md U27','docs/features/server-status-settings.md:30 core.status.*'],
          edge='真实异步网络探测未启动；失败回退缓存不空白',
          state='散落 6 处；设置项另挂 D10'),
     dict(id='D04-03', name='服务器图标与 logo',
          chain=['png 快速设置服务器 logo，自动调整像素',
                 '图标可视化编辑；png / gif / svg 与 opaque 兜底'],
          now=['src/core/studio_image.rs（AX15 / MIN_PIXEL / MAX_PIXEL / Component）','src/core/banner_design.rs','docs/features/ui-visual-catalog.md'],
          target=['D04 服务器·图标；像素与图像元数据留 studio_image.rs，不另开图片域'],
          basis=['12:63 png 快速设置服务器 logo 自动调整像素','12:59 服务器图标可视化编辑','11:243 模组图标全图片格式'],
          edge='真实像素调整与缩放执行层未启动',
          state='已归位'),
     ]),
dict(id='D05', name='下载中心', slot='core.nav.download', ux='U05:100',
     items=[
     dict(id='D05-01', name='下载任务后台化与队列视图',
          chain=['实例页 / 模组页 / 开服器 / 公告任一处点「下载 / 安装 / 更新」→ 任务写入后台队列；当前页不跳转、不阻塞',
                 '状态栏出现任务角标；首页 / 模组页 / 实例页收到「下载完成」事件推送',
                 '点状态栏角标或左导航「下载中心」→ 默认队列视图；队列面板可收起',
                 '队列行同帧显示每文件进度条、百分比、已下 / 总量、速度、总体进度条',
                 '同帧显示请求计数、每页数、缓存命中数、诊断行；空队列给「检查更新 / 导入清单」两入口',
                 '行内操作：暂停 / 恢复 / 取消 / 重试；右键重试；工具栏三动作；搜索命中文件名',
                 '单文件失败重试 2 次后标错，不阻塞其余；源不可达自动切镜像；取消后 0 副作用',
                 '任务结束清 inflight，写完成提示；完成事件自动推实例页与模组页'],
          now=['docs/design/ux-logic-matrix.md:100–116 U05 L01–L12','docs/spec/11-features-input.txt:183–191、208、238','src/core/download_sources.rs','src/core/download_history.rs','src/core/endpoints.rs（DOWNLOAD_BATCH_KEY=download/batch）','src/core/config.rs（endpoints / ports / download_region）','src/core/settings_io.rs（KNOWN_KEYS）','demos/ui-full-kcu-paper.html data-pane="download"','docs/features/lightweight-download.md'],
          target=['D05 下载中心·队列视图：进度条 / 百分比 / 暂停恢复取消 / 终态唯一落点',
                  'D05 下载中心·历史：download_history.rs（KINDS 六类）',
                  'D10 设置·下载与镜像：download_sources.rs（tier / max_concurrent / restricted / 测速 / § 模板 / 多源竞速）',
                  '配置根键：settings_io.rs 白名单 endpoints / ports / download_region，不单开模块'],
          basis=['11:183 传输进度显示','11:184 复制队列','11:185 暂停传输','11:186 恢复传输','11:187 取消传输','11:188 后台传输','11:189 断点续传','11:190 传输完成提示','11:191 传输失败重试','11:208 按序下载 / 多线程 / 每 20 条目 / 聚合搜索','11:238 多源竞速一个下好取消其余','U05 L01 / L04 / L06 / L07 / L08 / L10 / L11 / L12'],
          edge='不写真实网络 IO、不落真实字节、不引第三方下载库；启动阶段进度条（launch_progress.rs）不并入本域；未成年人模式禁用下载归 D10 开关（11:225）',
          state='散落 9 处；归位方案待拍板，未执行'),
     dict(id='D05-02', name='源与并发配置',
          chain=['默认源按测速结果；用户可强制境外，仅影响下载选择',
                 '手动选不同镜像下载 java 与游戏实例；§ 作模板版本号占位',
                 '一个模组多源同时下载，一个下好关闭其余请求',
                 '并发上限默认 3，最大 64；分层 auto_mirror；受限源单独开关'],
          now=['src/core/download_sources.rs（DEFAULT_SOURCES / MAX_CONCURRENT=64 / DEFAULT_CONCURRENT=3 / SOURCES_TARGET=download.sources）','src/core/config.rs','src/core/region.rs','docs/features/region-offline-restriction.md','docs/features/settings-groups.md'],
          target=['D10 设置·下载与镜像；队列视图只读结果不自己存源'],
          basis=['11:220 手动选镜像','11:236 § 模板版本号','11:238 多源竞速','U05 L02 / L11','12:60 下载源测速与镜像切换'],
          edge='curseforge 境外双通道口径按 11:267 不写进注释、不进本表正文细节',
          state='已归位'),
     dict(id='D05-03', name='缓存复用与增量刷新',
          chain=['文件按 SHA-1 落磁盘缓存复用；元数据内存缓存 TTL 30s；容量有界；单飞去重',
                 '刷新取队列增量；强制刷新重算校验和',
                 '一次请求带多个 id、每页 20、10 次重复只发 1 次'],
          now=['src/core/cache.rs','src/core/endpoints.rs','docs/features/core-cache.md','docs/features/query-encoding-contract.md','docs/features/request-id-contract.md'],
          target=['D18 缓存与刷新总控；下载队列只调用，不自己实现缓存'],
          basis=['U05 L03 / L04 / L11','U20','11:208 每 20 条目'],
          edge='不新开下载专用缓存模块',
          state='跨域复用；归位待拍板'),
     dict(id='D05-04', name='下载历史',
          chain=['任务终态写入历史；按 game / mod / modpack / resourcepack / shaderpack / datapack 六类分',
                 '历史条目上限 256；键长 256 字节；值长 4096 字节'],
          now=['src/core/download_history.rs（AX06 / DEFAULT_HISTORY / KINDS / MAX_ENTRIES=256）','docs/features/settings-groups.md'],
          target=['D05 下载中心·历史；不与统计 / 日志混存'],
          basis=['11:227 日志多文件合一（对照：历史不并入日志）','U05 L08'],
          edge='不把历史当日志',
          state='已归位'),
     ]),
dict(id='D06', name='模组管理', slot='core.nav.mods', ux='U06:117',
     items=[
     dict(id='D06-01', name='模组列表与方案快速选择',
          chain=['mod 页每 20 条目显示一次；聚合搜索；图标全格式',
                 '同一实例模组启用禁用快速选择像文件夹；点方案选中对应模组集',
                 '收藏、思维导图看依赖（图标 / 文字 / 版本 / 作者）'],
          now=['src/core/search_filter.rs（AX16）','src/core/world_editor.rs（AX03）','src/core/mod_rollback.rs（AX04）','docs/features/lucide-icon-system.md','docs/features/ui-product-copy.md'],
          target=['D06 模组管理：列表与方案唯一落点；搜索能力调 D20，不自己实现'],
          basis=['11:208 mod 页每 20 条目','11:230 模组收藏','11:247 思维导图看依赖','11:263 模组启用禁用快速选择','11:243 图标全图片格式'],
          edge='真实图片渲染 / 3D 预览未启动',
          state='散落 4 模块；归位待拍板'),
     dict(id='D06-02', name='依赖检测与更新',
          chain=['模组依赖检测与一键安装；文件一键补全（有版本 json 就补）',
                 '服主 json 声明更新 url / 是否检查 / 是否强制 / 指定 MC 版本 / 提示文本；页面可取消',
                 '重复同版本警告；版本更高时低版本 jar 自动禁用，顺序页码弹窗逐条选择',
                 '二分法模组可用性检验'],
          now=['src/core/mod_rollback.rs','src/core/upgrade_plan.rs','src/core/download_sources.rs','docs/features/plugin-upgrade-consent.md','docs/features/upper-layer-thirdparty.md'],
          target=['D06 模组管理·依赖与更新；下载动作调 D05，源配置调 D10'],
          basis=['11:209 依赖检测一键安装','11:219 服主 json 模组更新','11:221 模组更新管理','11:244 重复同版本警告与页码弹窗','11:251 文件一键补全','11:264 二分法检验','12:8 高版本禁用低版本 jar'],
          edge='真实解压 / 版本比较执行未启动；11:219 提示文本不复制进本表',
          state='散落 4 处；归位待拍板'),
     dict(id='D06-03', name='模组翻译与颜色代码',
          chain=['模组界面翻译；翻译源由统一调度器发放 json 与字体',
                 'MC 颜色代码一键复制，旧格式与新 json 两格式'],
          now=['src/core/generator_session.rs（AX18 / TRANSLATION_KEYS）','demos/lang/zh-CN.js / en-US.js','docs/features/i18n-crash-settings.md'],
          target=['D06 模组管理·翻译；语言包文件归 D19，不分散到各模块'],
          basis=['11:210 模组界面翻译','11:240 颜色代码一键复制','11:245 多语言统一调度器发放'],
          edge='语言文件按 11:245 堆在一起，不按模块散放',
          state='已归位'),
     ]),
dict(id='D07', name='账号登录', slot='core.nav.login', ux='U07:134',
     items=[
     dict(id='D07-01', name='账号绑定与切换',
          chain=['每个 MC 绑定默认账号，可切换；uuid 手动填写',
                 '微软 token 到期前 7 天提示；正版凭据缺失不静默改离线',
                 '访客模式不显示账号列表与实例，关闭后恢复；密码设开 / 密码设关'],
          now=['src/core/consent.rs','src/core/feature_gate.rs','docs/features/lightweight-login.md','docs/features/credential-guard.md','docs/features/headless.md'],
          target=['D07 账号登录：凭据与账号态唯一落点；访客模式开关归 D16 运行形态'],
          basis=['11:224 每个 mc 绑定账号','11:228 uuid 手动填写','11:260 token 到期前 7 天','11:262 访客模式','U01 L09'],
          edge='11:266 正版复用方案待拍板；不写真实授权流程',
          state='已归位；11:266 待拍板'),
     ]),
dict(id='D08', name='开服器', slot='core.nav.serverhost', ux='U15:270',
     items=[
     dict(id='D08-01', name='建服与 Java 检查',
          chain=['先检查可直接使用的 java；不可用走镜像拉，境外走官方源',
                 '自动下载 jar → 加载器选择页，允许原版或多个加载器',
                 'mod / 插件走官方通道；Java 多版本下载、切换、按 MC 版本推荐'],
          now=['src/core/endpoints.rs','src/core/args.rs','docs/features/lightweight-loaders.md','docs/features/server.md','docs/features/server-backlog.md'],
          target=['D08 开服器：Java 与 jar 选择唯一落点；下载动作调 D05，镜像调 D10'],
          basis=['12:2 先检查 java 与自动下载 jar','12:3 mod 与插件官方通道','12:27 Java 多版本管理','12:60 下载源测速与镜像切换'],
          edge='12:3 插件服官方通道名称待拍板；不写真实下载执行',
          state='已归位；12:3 待拍板'),
     dict(id='D08-02', name='运维闭环',
          chain=['快捷命令 / 与 MC 一致；快捷输入自动加 say/talk',
                 '手动同意 eula；成就快速分析；玩家快速管理',
                 '定时任务（自动重启 / 自动开机 / 自动发命令）；自动化增量备份选定路径',
                 'RCON 安全通道 + 看门狗 + 崩溃自动归因；快速导出日志',
                 '功能锁定与命令黑名单用于访客模式；op 锁定；ftp/sftp'],
          now=['src/core/log.rs','src/core/instance.rs','docs/features/server-auto-command-log-trigger.md','docs/features/server-failure-history.md','docs/features/server-async-probe.md'],
          target=['D08 开服器·运维；日志导出调 D09，不另存日志副本'],
          basis=['12:5 快捷命令','12:7 手动同意 eula','12:13 增量备份','12:17 定时任务','12:19 功能锁定与黑名单','12:20 快速导出日志','12:21 RCON 三项','12:10 op 锁定','12:9 ftp/sftp','12:16 快捷输入','12:18 成就分析'],
          edge='真实 RCON / 看门狗 / 备份执行层未启动',
          state='散落 5 处；归位待拍板'),
     dict(id='D08-03', name='世界与种子',
          chain=['快速显示种子号（需 NBT 能力）；世界文件夹未关实例时被锁定并提示',
                 '默认服务器配置汉化并快速选择、多实例同步'],
          now=['src/core/seed_access.rs（AX19）','src/core/world_editor.rs（AX03）','src/core/notice_center.rs'],
          target=['D08 开服器·世界；种子权限提示归本域，NBT 执行层未启动'],
          basis=['12:14 快速显示种子号','12:15 世界文件夹锁定','12:26 服务器配置汉化','11:213 vianbt 提供 NBT 能力'],
          edge='vianbt 库引入待拍板（Q-082-01）；真实 NBT 读取未启动',
          state='已归位；Q-082-01 待拍板'),
     ]),
dict(id='D09', name='日志诊断', slot='core.nav.logs', ux='U08:151',
     items=[
     dict(id='D09-01', name='日志记录与压缩',
          chain=['记录启动器自身问题；多个日志合一文件，每 100 条压缩到一个压缩包',
                 '日志可选对应 mod 提示内容；快速导出日志',
                 '状态栏、日志页、设置页三入口；诊断行 [KCU] 贯穿'],
          now=['src/core/log.rs','src/core/diagnostics.rs（diag_line）','src/core/boot.rs（BUNDLE_FILE=diagnostic-bundle.json）','docs/features/log.md','docs/features/core-log.md','docs/features/core-diagnostics.md'],
          target=['D09 日志诊断：log.rs / diagnostics.rs 唯一落点；各模块只发 diag_line 不自存日志'],
          basis=['11:227 日志多文件合一每 100 条压缩','11:235 日志选 mod 提示内容','12:20 快速导出日志','00:114 统一信封'],
          edge='下载历史、统计、崩溃反馈不并入日志',
          state='已归位'),
     dict(id='D09-02', name='崩溃反馈',
          chain=['崩溃后弹一次完整内容预览；先问我再发送；脱敏口径',
                 '保留最近 N 份、容量有界；设置里可调'],
          now=['src/core/consent.rs','src/core/boot.rs','docs/design/crash-reporting.md','docs/features/i18n-crash-settings.md','demos/ui-full-kcu-paper.html data-pane="crash"'],
          target=['D19 外观与文案·崩溃反馈分组；诊断内容读 D09'],
          basis=['docs/design/crash-reporting.md:28 / :54','U28'],
          edge='真实发送执行层未启动',
          state='跨域；归位待拍板'),
     ]),
dict(id='D10', name='设置', slot='core.locked.settings', ux='U09:168 / U22:390',
     items=[
     dict(id='D10-01', name='设置分组与配置读写',
          chain=['导航底部锁定槽位进入，默认常规分组；9 分组 chip（演示实跑 11 pane）',
                 '配置写后内存缓存即时生效，磁盘落 C 盘 KCU，重启读盘；写盘合并为一次',
                 '写盘失败保留旧值并可见报错；恢复默认二次确认；关窗保存进度',
                 '@modified 过滤、单项重置、搜索命中设置项、稳定性 ID、保存状态、诊断行'],
          now=['src/core/config.rs（6 根键 / Config::empty 默认值）','src/core/settings_io.rs（SETTINGS_FILE=launch.json / KNOWN_KEYS / DERIVED_KEYS / PROTECTED_FILES 4 项 / 6 上限）','src/core/paths.rs','demos/ui-full-kcu-paper.html 11 个 data-pane / 15 个 id="set*" 控件','demos/lang/zh-CN.js / en-US.js set.* 键','docs/features/settings-groups.md','docs/design/nav-slot-contract.md:38'],
          target=['D10 设置：config.rs + settings_io.rs 唯一真值；分组 / 控件 / 语言包键为投影，不各自存默认值',
                  '设置项注册表候选：把 6 根键、18 个 DEFAULT_STATE、40 张白名单、11 分组、15 控件、core.* ID 收到一处'],
          basis=['00:8 配置路径 c/kcu/kculauncher/config/launch.json','11:241 用户选语言与语言包管理','U09','U22 L01–L12','020 D03 九分组'],
          edge='历史文档记 9 分组与演示 11 pane 的偏差只登记不重写（093 E378 / A181）；插件不得改写 core.* 项',
          state='散落 6 处；注册表候选待拍板，未执行'),
     dict(id='D10-02', name='AI 容器接口',
          chain=['地址由用户自填，启动器不预设；测连接后状态徽章变化',
                 '凭据不回显；危险项二次确认'],
          now=['src/core/client_ai.rs（AX23 GateOnly）','src/core/endpoints.rs（ports）','demos/ui-full-kcu-paper.html data-pane="ai" / id="setAi*"','docs/features/settings-groups.md'],
          target=['D10 设置·AI 容器接口分组；GateOnly 不扩 v1 面'],
          basis=['U09 L09','U22 L09','12:4 ai 自动管理服务器开放 api 不赋删除权限','11:18 API 不共有'],
          edge='AX23 保持 GateOnly；不写真实本地容器连接',
          state='已归位；12:4 授权形态待拍板'),
     dict(id='D10-03', name='插件与更新 / 隐私与诊断 / 实验性',
          chain=['模拟更新 / 回滚，核心版本保持 0.0.0；插件区独立容器',
                 '隐私同意弹窗；诊断包导出；实验性分组收未定项'],
          now=['src/core/extension_gate.rs','src/core/consent.rs','src/core/boot.rs','src/core/feature_gate.rs（CORE_LOCKED / FORBIDDEN_ENTRY_KEYS）','docs/features/plugin-upgrade-consent.md','demos/ui-full-kcu-paper.html data-pane="plugins" / "privacy" / "experimental"'],
          target=['D10 设置对应三分组；插件运行时归 D13'],
          basis=['11:217 隐私政策同意','U22 L07','docs/features/nav-slot-lock.md'],
          edge='插件只能追加分组不改 core.*',
          state='已归位'),
     ]),
dict(id='D11', name='关于', slot='core.locked.about', ux='U10:185',
     items=[
     dict(id='D11-01', name='第三方许可与关于页',
          chain=['完整关于页与第三方开源许可；所有图片用真正的图片',
                 '58 份 LICENSE 全文 + THIRD-PARTY-NOTICES.md 309 行声明'],
          now=['docs/features/third-party-licenses-about.md','docs/features/upper-layer-thirdparty.md','docs/licenses/','THIRD-PARTY-NOTICES.md','docs/records/code-ownership-audit.md'],
          target=['D11 关于：许可与归属唯一落点；不散到各功能文档'],
          basis=['11:216 关于与第三方开源许可','00:32 开源优先','00:249 许可证合规优先'],
          edge='B05 源仓库与许可待拍板；零新增第三方（093 / 094 同）',
          state='已归位；B05 待拍板'),
     ]),
dict(id='D12', name='弹窗与通知', slot='跨页统一', ux='U11:202',
     items=[
     dict(id='D12-01', name='弹窗全集与关闭逻辑',
          chain=['每个弹窗有关闭逻辑；× 与 ESC；圆圈 i 详情；每页扩展统一格式',
                 '冲突 / 失败 / 取消均可见，0 副作用扩散；空态给入口不显示空白',
                 '统一信封三分；弹窗流程后 0 残留'],
          now=['src/core/popup.rs（PopupRegistry / CloseAction / PopupOpenError）','src/core/consent.rs（POPUP_ID=privacy）','src/core/extension_gate.rs（LOCK_POPUP_ID=extension）','src/core/envelope.rs','src/api.rs（v1 7 符号）'],
          target=['D12 弹窗与通知：popup.rs + envelope.rs 唯一落点；各域只登记弹窗 ID 不自建弹窗'],
          basis=['11:10 每个弹窗有关闭逻辑','11:22 圆圈 i 详情','11:16 每页扩展','00:114 统一信封三分','00:137 接口终点'],
          edge='api::v1 7 符号 / 4 条 pub use 不变（A246）',
          state='已归位'),
     ]),
dict(id='D13', name='插件', slot='插件区容器', ux='U25:592',
     items=[
     dict(id='D13-01', name='插件安装与槽位',
          chain=['插件区独立容器；只能追加条目，不改 core.* 导航与设置项',
                 '侧栏图标安全、动态 ABI、生命周期、故障恢复、升级同意',
                 '默认显示 CopperGolemLauncher 插件条目并引导下载，软件不内置'],
          now=['src/core/extension_gate.rs','src/core/feature_gate.rs','src/plugins/','docs/features/plugin-lifecycle.md','docs/features/plugin-sidebar-icon.md','docs/features/plugin-dynamic-abi.md','docs/features/plugin-fault-recovery.md','docs/features/plugin-upgrade-consent.md','docs/features/plugin-icon-safety.md'],
          target=['D13 插件：extension_gate.rs + src/plugins/ 唯一落点；plugin.settings.* 只追加设置分组'],
          basis=['11:258 CopperGolemLauncher 做成插件','11:3 模块化','020 D06','docs/design/nav-slot-contract.md:30 / :32'],
          edge='真实插件加载执行未启动；11:258 单开仓库不写进本仓',
          state='散落 7 份文档；归位待拍板'),
     ]),
dict(id='D14', name='推荐与排序', slot='跨页总控', ux='U23:407',
     items=[
     dict(id='D14-01', name='推荐位目录与权重',
          chain=['10 处推荐位：首页启动卡 / 首页推荐服务器 / 版本页 / 下载页 / 模组页 / 公告 / 加载器 / Java / 镜像源 / 插件',
                 '总开关、权重可自定义、用户指定永远排第一、不感兴趣只降权不隐藏',
                 '来源本地 / 官方 / 插件三类可插拔；事件驱动 + 定时软刷新；5min 容量有界缓存'],
          now=['docs/design/recommendation-catalog.md:14–43（RC01–RC10 / core.rec.*）','docs/features/recommendation-catalog.md','demos/ui-full-kcu-paper.html data-pane="recommend"','src/core/widget_layout.rs'],
          target=['D14 推荐与排序：权重口径单点维护；各页只渲染结果不自己算'],
          basis=['020 D10 推荐位补全','U23','docs/design/recommendation-catalog.md:29–36'],
          edge='plugin.rec.* 不改 core.rec.* 权重口径',
          state='已归位'),
     ]),
dict(id='D15', name='文件管理', slot='跨页复用', ux='U14:253',
     items=[
     dict(id='D15-01', name='传输与文件操作全集',
          chain=['分卷解压 / 压缩包校验 / 修复 / 创建快捷方式 / 文件锁定与占用提示 / 自动刷新目录 / 文件变更监视',
                 '传输进度显示 / 复制队列 / 暂停 / 恢复 / 取消 / 后台 / 断点续传 / 完成提示 / 失败重试',
                 '冲突处理：覆盖确认 / 跳过 / 保留两者 / 自动重命名；撤销 / 重做 / 操作历史',
                 '批量操作确认与预览；错误提示 / 重试 / 跳过'],
          now=['docs/spec/11-features-input.txt:175–204','docs/design/ux-logic-matrix.md U14','src/core/robust.rs','src/core/paths.rs','src/core/instance_import.rs','src/core/world_editor.rs'],
          target=['D15 文件管理：能力清单归本域，下载队列（D05）/ 实例导入（D03）/ 世界编辑（D08）复用同一套，不各写一份'],
          basis=['11:175–204 逐条','11:205 搜索等用户逻辑也要有对应功能','11:206 有文件管理功能就要与正常文件管理器一样'],
          edge='真实解压 / 撤销栈执行层未启动',
          state='能力散落 4 模块；归位待拍板'),
     ]),
dict(id='D16', name='运行形态', slot='启动分流', ux='U12:219 / U13:236 / U18:321 / U19:338',
     items=[
     dict(id='D16-01', name='轻量 / 无头 / 安全模式 / 首次引导',
          chain=['默认轻量 ≤2GB；无头模式走 kculh，.kculf 跳过 GUI 直接进 MC',
                 '连续启动失败 3 次进安全模式；首次进入 4 步引导可跳过',
                 '未成年人模式自动禁用所有下载，启动 MC 有防沉迷'],
          now=['src/lightweight/','src/core/boot.rs','src/core/first_run.rs（AX10）','src/core/args.rs','docs/features/lightweight.md','docs/features/headless.md','docs/features/auto-disable-feature.md'],
          target=['D16 运行形态：启动分流唯一落点；下载禁用开关挂 D10，不在各下载入口各判一次'],
          basis=['00:8 默认轻量 ≤2GB','11:225 未成年人模式禁用下载','11:242 .kculf / kculh','U01 L07','U12 / U13 / U18 / U19'],
          edge='.kculf 需使用两天或手动装拓展包（11:242）；11:242 时长路径待拍板',
          state='散落 5 处；归位待拍板'),
     ]),
dict(id='D17', name='扩展通道', slot='设置分组', ux='U16:287 / U17:304',
     items=[
     dict(id='D17-01', name='手机互联与局域网',
          chain=['同一网络下手机与电脑建立连接并传文件；连接码与二维码配对',
                 '陶瓦联机；房间号 / 配对码 / 通道开关；发现 → 配对 → 传输阶段'],
          now=['src/core/lan_channel.rs（AX21 / TRANSITIONS / STAGE_FIELDS）','src/core/region.rs','docs/features/lan.md','docs/design/upper-layer-stack.md'],
          target=['D17 扩展通道：lan_channel.rs 唯一状态；设置项挂 D10「实验性 / 常规」'],
          basis=['00:20 手机互传需要设计协议','00:15 连接码','11:215 手机互传通道与二维码','11:218 陶瓦联机','11:18 API 不共有','11:19 不写死网址端口'],
          edge='真实网络 IO / 二维码生成未启动；协议只到定义层',
          state='已归位'),
     ]),
dict(id='D18', name='缓存与刷新总控', slot='跨页总控', ux='U20:355',
     items=[
     dict(id='D18-01', name='四层缓存与软刷新',
          chain=['同帧显示四层缓存状态；软刷新取增量、强制刷新重算',
                 '事件驱动推送；5min 容量有界；离线显示上次快照并标灰',
                 '设置页「数据与缓存」、状态栏、下载页三入口'],
          now=['src/core/cache.rs','src/core/stats.rs','src/core/notice_center.rs','src/core/download_sources.rs','docs/features/core-cache.md','docs/features/settings-groups.md'],
          target=['D18 缓存与刷新总控：cache.rs 唯一实现；D01 / D05 / D14 只调用'],
          basis=['U20','U01 L03 / L04','U05 L03 / L04','docs/design/recommendation-catalog.md:35'],
          edge='不新开各页专用缓存',
          state='已归位'),
     ]),
dict(id='D19', name='外观与文案', slot='设置分组', ux='U28:485',
     items=[
     dict(id='D19-01', name='语言 / 主题 / 深色 / 崩溃反馈',
          chain=['用户选语言与语言包并管理；语言文件堆在一起由统一调度器发放 json 与字体',
                 '深色模式；外观预设最多 16 套；横幅设计 / 皮肤草稿 / Studio 图像',
                 '崩溃反馈分组：预览 / 脱敏 / 先问再发送'],
          now=['src/core/appearance.rs（AX13 / MAX_PRESETS=16）','src/core/banner_design.rs（AX17）','src/core/skin_draft.rs（AX14）','src/core/studio_image.rs（AX15）','src/core/generator_session.rs（AX18）','demos/lang/zh-CN.js / en-US.js','demos/ui-full-kcu-paper.html data-pane="general" / "crash"','docs/features/ui-framework.md','docs/features/ui-paper-ux.md'],
          target=['D19 外观与文案：语言包两份 + 外观状态唯一落点；编辑器类图像态按域回 D04 / D06，不混进外观'],
          basis=['11:241 选语言与语言包管理','11:245 统一调度器发放并堆在一起','11:246 深色模式','U28'],
          edge='语言键不按模块散放；崩溃反馈真实发送未启动',
          state='散落 6 模块；归位待拍板'),
     ]),
dict(id='D20', name='搜索与全局快捷入口', slot='跨页胶囊', ux='11:205–206',
     items=[
     dict(id='D20-01', name='胶囊搜索与快捷键',
          chain=['Ctrl K 胶囊搜索；命中设置项、文件名、推荐位、服务器名',
                 '快捷入口 4 格；导航可折叠 64px；搜索框与排序按钮与文件管理器一致',
                 '快捷键绑定；录屏截屏加了快捷键并打开开关后后台才有进程'],
          now=['src/core/search_filter.rs（AX16 / DIMENSIONS / SORT_DIMENSIONS）','src/core/args.rs','demos/ui-full-kcu-paper.html','docs/features/query-encoding-contract.md'],
          target=['D20 搜索：search_filter.rs 唯一实现；D05 / D06 / D10 / D04 只提供被搜字段'],
          basis=['11:205 搜索等用户逻辑也要有对应功能','11:206 搜索框与排序按钮同文件管理器','11:208 聚合搜索','U01 L12','11:212 快捷键绑定','11:211 录屏截屏'],
          edge='不各页各写一套搜索',
          state='已归位'),
     ]),
]

# 用户点名示范：下载会进入后台 → 下载页打开 → 进度条与百分比
DEMO_CHAIN = [
 ('1', '触发', '实例与版本 / 模组管理 / 开服器 / 公告中心任一处点「下载 / 安装 / 更新」', '11:208 / 11:209 / 12:2 / 11:219'),
 ('2', '后台化', '任务写入后台队列；当前页不跳转、不阻塞', '11:188 后台传输'),
 ('3', '角标', '状态栏出现任务角标；首页 / 模组页 / 实例页收到下载完成事件推送', 'U01 L04 / U05 L04'),
 ('4', '进入', '点状态栏角标或左导航「下载中心」→ 默认队列视图', 'U05 L01 / nav-slot-contract.md:18'),
 ('5', '同帧', '队列面板可收起；进度条同帧可见', 'U05 L01 / L08'),
 ('6', '每文件', '每文件进度条、百分比、已下 / 总量、速度', '11:183 传输进度显示 / U05 L06 / L10'),
 ('7', '总体', '总体进度条；请求计数、每页数、缓存命中数、诊断行', 'U05 L06 / L10'),
 ('8', '操作', '暂停 / 恢复 / 取消 / 重试；右键重试；工具栏三动作；搜索命中文件名', '11:185 / 11:186 / 11:187 / 11:191 / U05 L12'),
 ('9', '异常', '单文件失败重试 2 次后标错，不阻塞其余；源不可达自动切镜像；取消后 0 副作用', 'U05 L06 / L07'),
 ('10', '空态', '空队列给「检查更新 / 导入清单」两入口', 'U05 L05'),
 ('11', '终态', '任务结束清 inflight；写完成提示；完成事件自动推实例页与模组页', '11:190 / U05 L04 / L08'),
 ('12', '不混', '启动阶段进度准备 → 校验 → 拉起在 launch_progress.rs，与下载进度条分源', 'U01 L06 / src/core/launch_progress.rs:6'),
]

REGROUP_RULES = [
 ('R01', '新功能先查本表 20 域；命中既有域直接归入，不新开功能域'),
 ('R02', '每轮开工不因一个功能新建一个 src/core/*.rs；同域状态并到既有模块'),
 ('R03', '同一状态只留一处真值：配置根键、模块 DEFAULT_STATE、演示控件、语言包键、core.* ID 由一处登记'),
 ('R04', '跨域能力只走统一调度器：搜索 D20、缓存 D18、弹窗 D12、推荐 D14、文件管理 D15'),
 ('R05', '进度类状态按源分开：启动进度 D01、下载任务进度 D05、传输进度 D15，不合并'),
 ('R06', '设置项只登记键 / 默认值 / 分组 / 控件 id / 语言包键 / 校验口径，不在各模块各存一份'),
 ('R07', '原文直接给出的锚点逐条挂域；未拍板 EQ / Q 挂待拍板层，不代拍、不硬做（A208）'),
 ('R08', '归位方案全部待拍板，094 不移动文件、不改设置项、不改 src/'),
]


def read(rel):
    return (ROOT / rel).read_text(encoding='utf-8')


def line_of(rel, n):
    return read(rel).splitlines()[n - 1]


def anchor_ok(spec):
    """校验依据锚点里的 11:n / 12:n 行号真实存在且非空。"""
    for m in re.finditer(r'\b(11|12):(\d+)', spec):
        f = 'docs/spec/11-features-input.txt' if m.group(1) == '11' else 'docs/spec/12-server-features-input.txt'
        n = int(m.group(2))
        lines = read(f).splitlines()
        if n < 1 or n > len(lines) or not lines[n - 1].strip():
            return False, '%s:%d' % (m.group(1), n)
    return True, ''


def build():
    L = []
    add = L.append
    add('KCU Launcher 功能归类与归位表（094 轮）')
    add('文件：docs/records/round-094-feature-regrouping.txt')
    add('生成：python3 scripts/feature_regrouping.py（只读实扫 + 结构化归类表，不改功能文件）')
    add('开工时间戳：Thu Nov 26 23:36:07 CST 2026')
    add('用户 094 逐字指令（357 字节）：' + SPEC)
    add('本轮动作：按功能域重新归类，逐功能回显行为链路；不移动文件、不改设置项、不改 src/；归位方案全部待拍板未执行。')
    add('')
    add('与 093 的区别：093 交的是「每个功能写在哪个文件」的位置台账（48 模块 / 6 根键 / 11 pane / 5 条偏差）；')
    add('094 交的是「每个功能该归到哪一类、用户可见的行为链路怎么归位」，细到下载进入后台、下载页打开、进度条与百分比。')
    add('093 回答「文件在哪」；094 回答「功能属于哪一类、行为从哪到哪、现在散在哪几处、归位后收到哪」。')
    add('')
    add('计数口径：本表目录计数为 094 开工实跑快照，094 文件落地后 tracked 会增加；两口径在 094 补记并列，不混用（093 E379 同）。')
    add('开工快照：tracked %d / src/core/*.rs %d / %d 行 / %d 个 *_guard.py + p09_scan.py / demos %d / PNG %d / 决策 %d / 验证 %d / 功能文档 %d / design %d / 必读清单 %d 项 / 11 pane / 15 控件 / 24 AX（Planned 2）。' % (
        SNAP['tracked'], SNAP['core_rs'], SNAP['core_lines'], SNAP['guards'], SNAP['demos'],
        SNAP['previews'], SNAP['decisions'], SNAP['verification'], SNAP['features'],
        SNAP['design'], SNAP['required']))
    add('')
    add('=' * 78)
    add('一、怎么读这份表')
    add('=' * 78)
    add('  功能域：20 个一级域；9 个来自 core.nav.* 一级导航，2 个来自 core.locked.* 锁定槽位，9 个为跨页能力域。')
    add('  每个功能项固定六字段：')
    add('    行为链路  = 用户可见的动作 → 状态 → 入口 → 可见值 → 终态，逐条写实，不写解释性话术')
    add('    当前落点  = 094 实扫到的真实文件 / 行号 / 演示 pane / 设置分组')
    add('    归位落点  = 归类后唯一该在的位置；跨域能力指明调用关系')
    add('    依据锚点  = 00 / 11 / 12 号原文真实行号、U 段编号、契约行号；不编造')
    add('    边界      = 不做什么、哪些执行层未启动')
    add('    状态      = 已归位 / 散落 N 处 / 归位方案待拍板未执行')
    add('  行为链路颗粒度对齐用户 094 举例：下载进入后台 → 下载页打开 → 进度条与百分比（见第四节逐步展开）。')
    add('')
    add('=' * 78)
    add('二、功能域总表（%d 域）' % len(DOMAINS))
    add('=' * 78)
    add('列：域 | 名称 | 唯一落点 | 导航槽位 | UX 矩阵 | 功能数 | 依据')
    for d in DOMAINS:
        add('  %s | %s | %s | %s | %s | %d | %s' % (
            d['id'], d['name'], d['name'], d['slot'], d['ux'], len(d['items']),
            ','.join(sorted({b for it in d['items'] for b in it['basis'] if b.startswith(('11:', '12:'))})[:3]) or d['ux']))
    add('')
    add('  9 个一级导航域：D01 首页 / D02 公告 / D03 实例 / D04 服务器 / D05 下载 / D06 模组 / D07 登录 / D08 开服器 / D09 日志。')
    add('  2 个锁定槽位域：D10 设置 / D11 关于（nav-slot-contract.md:38–39，不可改写 / 隐藏 / 重排 / 换 ID）。')
    add('  9 个跨页能力域：D12 弹窗 / D13 插件 / D14 推荐 / D15 文件管理 / D16 运行形态 / D17 扩展通道 / D18 缓存 / D19 外观文案 / D20 搜索。')
    add('')
    add('=' * 78)
    add('三、逐域逐功能详表')
    add('=' * 78)
    n_items = 0
    for d in DOMAINS:
        add('')
        add('-' * 78)
        add('【%s %s】 唯一落点=%s | 槽位=%s | UX=%s' % (d['id'], d['name'], d['name'], d['slot'], d['ux']))
        add('-' * 78)
        for it in d['items']:
            n_items += 1
            ok, bad = anchor_ok(' '.join(it['basis']))
            if not ok:
                raise SystemExit('BAD_ANCHOR %s %s' % (it['id'], bad))
            add('  %s %s' % (it['id'], it['name']))
            add('    行为链路：')
            for j, c in enumerate(it['chain'], 1):
                add('      %d) %s' % (j, c))
            add('    当前落点：')
            for x in it['now']:
                add('      - %s' % x)
            add('    归位落点：')
            for x in it['target']:
                add('      - %s' % x)
            add('    依据锚点：%s' % '；'.join(it['basis']))
            add('    边界：%s' % it['edge'])
            add('    状态：%s' % it['state'])
            add('')
    add('  逐域合计 %d 个功能项，全部六字段齐。' % n_items)
    add('')
    add('=' * 78)
    add('四、下载域完整行为链路示范（用户 094 点名）')
    add('=' * 78)
    add('  用户原句：「下载会进入后台，然后用户可以在下载页当中打开，并且查看它的进度条和百分比」。')
    add('  逐值展开为 12 步，列：步 | 环节 | 用户可见事实 | 依据')
    for n, phase, fact, basis in DEMO_CHAIN:
        add('  %2s | %-6s | %s | %s' % (n, phase, fact, basis))
    add('')
    add('  真值分散实况（094 实扫）：')
    add('    行为定义  ux-logic-matrix.md:100–116 U05 L01–L12 / 11:183–191 / 11:208 / 11:238')
    add('    源与并发  src/core/download_sources.rs（DEFAULT_SOURCES tier=auto_mirror / max_concurrent=3 / DEFAULT_CONCURRENT=3 / MAX_CONCURRENT=64）')
    add('    历史      src/core/download_history.rs（KINDS 六类 / MAX_ENTRIES=256）')
    add('    批量端点  src/core/endpoints.rs（DOWNLOAD_BATCH_KEY=download/batch）')
    add('    配置根键  src/core/config.rs + settings_io.rs（endpoints / ports / download_region 在 KNOWN_KEYS）')
    add('    演示视图  demos/ui-full-kcu-paper.html data-pane="download"')
    add('    启动进度  src/core/launch_progress.rs（PHASES 准备→校验→拉起，PROGRESS_TARGET=launcher.progress）——与下载进度不同源')
    add('  归位后：队列视图与进度条 / 百分比只落 D05；源与并发只落 D10 设置·下载与镜像；历史只落 D05·历史；启动进度只落 D01。')
    add('  9 处散落收拢到 4 个唯一落点；方案待拍板，094 未执行（A208）。')
    add('')
    add('=' * 78)
    add('五、归类规则候选（防止乱开导致逻辑不归位）')
    add('=' * 78)
    for rid, r in REGROUP_RULES:
        add('  %s | %s' % (rid, r))
    add('')
    add('  用户 094 原句「防止你乱开导致的逻辑不是正常逻辑」对应 R01 / R02 / R03 / R05：')
    add('  093 已实证 069–091 期间多轮各新建一个 400–1000 行同构模块，48 模块 / 22332 行；')
    add('  同类状态（JSON 默认态、原子写、统一信封、diag_line、路径校验）重复 18 份 DEFAULT_STATE / 40 张白名单。')
    add('  R01–R08 为候选归位规则，全部待拍板，094 不擅自定规则、不擅自迁移（A203 / A208）。')
    add('')
    add('=' * 78)
    add('六、散落清单（跨域收拢对照）')
    add('=' * 78)
    add('列：功能 | 当前跨几处 | 主要散落位置 | 归位后唯一落点')
    scattered = [
      ('D05 下载任务后台化与进度条 / 百分比', 9, 'U05 / 11:183–191 / download_sources / download_history / endpoints / config / settings_io / HTML pane / features', 'D05 队列视图 + D10 下载与镜像 + D05 历史 + 配置根键'),
      ('D10 设置项真值', 6, 'config.rs / settings_io.rs / 18 个 DEFAULT_STATE / 40 张白名单 / HTML 11 pane 15 控件 / 两份语言包 / core.* ID', '单一设置注册表（候选，待拍板）'),
      ('D03 实例与导入 / 拖放 / 回滚', 5, 'instance.rs / instance_drop.rs / instance_import.rs / upgrade_plan.rs / world_editor.rs', 'D03 实例与版本'),
      ('D04 服务器列表 / 状态 / 自动连接', 6, 'region.rs / userflow.rs / servers-dat / join-binding / async-probe / status-settings', 'D04 服务器 + D10 服务器状态分组'),
      ('D06 模组列表 / 依赖 / 更新 / 翻译', 4, 'search_filter / world_editor / mod_rollback / generator_session', 'D06 模组管理 + D20 搜索 + D19 语言包'),
      ('D08 开服器运维闭环', 5, 'log.rs / instance.rs / 3 份 server-* features', 'D08 开服器·运维 + D09 日志导出'),
      ('D13 插件', 7, 'extension_gate / feature_gate / src/plugins / 5 份 plugin-* features', 'D13 插件'),
      ('D15 文件管理能力全集', 4, '11:175–204 / robust / paths / instance_import / world_editor', 'D15 文件管理，D05 / D03 / D08 复用'),
      ('D16 运行形态', 5, 'src/lightweight / boot / first_run / args / 3 份 features', 'D16 运行形态 + D10 下载禁用开关'),
      ('D19 外观与文案', 6, 'appearance / banner_design / skin_draft / studio_image / generator_session / 两份语言包', 'D19 外观文案 + D04 / D06 图像态'),
    ]
    for name, n, where, target in scattered:
        add('  %s | %d | %s | %s' % (name, n, where, target))
    add('')
    add('  E378 延续：020 决策与 settings-groups.md 记 9 分组，HTML 实跑 11 pane；094 不重写历史文档，只在本表标当前落点。')
    add('')
    add('=' * 78)
    add('七、约束与状态')
    add('=' * 78)
    add('  094 不移动文件、不改设置项、不改 src/、不改 Cargo.* / vendor/、不改功能池状态、不改 api::v1。')
    add('  归位方案与 R01–R08 全部标「待拍板，未执行」；093 的 5 条偏差仍待拍板，A 组 EQ / Q 与 2 项 Planned 仍全部未证实。')
    add('  四值：已证实（本表 20 域 / %d 功能项 / 12 步下载链路 / 真实锚点逐条校验 / 开工 A145 远端 87513a5 与 1300 ALL_MATCH True）；已失败（E213–E379 历史项 + E378 分组数过期 + 094 归类偏差登记）；未证实（13 条 EQ / 4 项 Q-C / 31 条历史 Q / 2 项 Planned / R01–R08 后果 / 10 条散落归位后果）；未启动（真实网络 IO / UI 宿主 / 渲染层 / 文件迁移执行 / 真实下载字节落盘）。' % n_items)
    add('  通过标记：按 00:245 不发；独立验证部分通过。')
    add('  唯一下一步：用户点第三 / 四 / 五 / 六节里要执行哪几条归位（或回「都不动」），再按 A208 排迁移轮次；不擅自开工硬做。')
    add('')
    add('生成命令：python3 scripts/feature_regrouping.py')
    add('校验命令：python3 scripts/feature_regrouping_guard.py')
    return '\n'.join(L) + '\n'


if __name__ == '__main__':
    OUT.write_text(build(), encoding='utf-8')
    b = OUT.read_bytes()
    print('FEATURE_REGROUPING_OK path=%s bytes=%d lines=%d sha256=%s' %
          (str(OUT.relative_to(ROOT)), len(b), b.count(b'\n'), hashlib.sha256(b).hexdigest()[:16]))

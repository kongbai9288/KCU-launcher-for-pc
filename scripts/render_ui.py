#!/usr/bin/env python3
"""把整页 UX 界面按视图渲染为 PNG 预览，并拼一张总览图。"""
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "demos" / "ui-full-kcu-paper.html"
OUT = ROOT / "demos" / "preview"
OUT.mkdir(parents=True, exist_ok=True)

SCENES = [
    ("01-home", "home", "首页 · 米纸质感"),
    ("02-home-dark", "home-dark", "深色纸质主题"),
    ("03-notices", "notices", "公告中心 · 四类标签"),
    ("04-notice-detail", "notice-detail", "公告详情弹窗"),
    ("05-update", "update", "版本更新提示"),
    ("06-onboarding", "onboarding", "首次启动 4 步引导"),
    ("07-instances", "instances", "实例列表 · 纸感表格"),
    ("08-cardgrid", "cardgrid", "网格视图"),
    ("09-download", "download", "下载队列与进度"),
    ("10-mods", "mods", "模组管理表格"),
    ("11-login", "login", "三种登录与回退链"),
    ("12-logs", "logs", "运行日志"),
    ("13-logs-drawer", "logs-drawer", "日志抽屉"),
    ("14-settings", "settings", "设置 · 纸感表单"),
    ("15-about", "about", "关于与外观"),
    ("16-popups", "popups", "弹窗全集 11 类"),
    ("17-lightweight", "lightweight", "轻量模式极简视图"),
    ("18-error", "error", "异常与边界六态"),
    ("19-narrow", "narrow", "侧栏收起态"),
    ("20-context", "context", "右键菜单"),
    ("21-servers", "servers", "服务器列表 · 自动连接与连接范围"),
    ("22-licenses", "licenses", "第三方许可七列表"),
    ("23-sync", "sync", "四层缓存与刷新总控"),
    ("24-refresh", "refresh", "R1-R5 刷新触发"),
    ("25-states", "states", "六态与缓存兜底"),
    ("26-ai", "ai", "AI 容器接口与权限"),
    ("27-serverhost", "serverhost", "开服器与控制台"),
    ("28-headless", "headless", "无头模式统一信封"),
    ("29-settings-recommend", "settings&tab=recommend", "设置 · 推荐与排序 10 位"),
    ("30-settings-status", "settings&tab=status", "设置 · 服务器与连接"),
    ("31-settings-plugins", "settings&tab=plugins", "设置 · 插件与插件化更新"),
    ("32-settings-cache", "settings&tab=cache", "设置 · 四层缓存与刷新"),
    ("33-settings-ai", "settings&tab=ai", "设置 · AI 容器接口"),
    ("34-servers-join", "server-join", "双击进服 · 实例绑定弹窗"),
    ("35-servers-locked", "servers-locked", "连不上沉底 · 锁定保持靠前"),
    ("36-servers-budget", "servers-budget", "设备连接范围 · 异步队列"),
    ("37-servers-history", "servers-history", "轻量档 · 无成功记录按权重排序"),
    ("38-servers-latency", "servers", "信号格下标注具体延迟"),
    ("39-servers-rename", "servers-rename", "服务器改名弹窗"),
    ("40-servers-samenames", "servers-samenames", "同名服务器各自独立"),
    ("41-i18n-en", "i18n-en", "界面语言切换 · English"),
    ("42-settings-crash", "settings&tab=crash", "设置 · 崩溃反馈"),
    ("43-licenses-updated", "licenses", "第三方许可 · 新增候选 6 组"),
]

W, H = 1440, 900
CHROME = os.environ.get("KCU_CHROME", "/usr/local/bin/chromium")


def font(size):
    for p in [
        "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
        "/nix/store/smgbvz9sqcikc18vf3i9ry2p5zlnb7h5-noto-fonts-cjk-sans-2.004/share/fonts/opentype/noto-cjk/NotoSansCJK-VF.otf.ttc",
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
    ]:
        if Path(p).exists():
            return ImageFont.truetype(p, size)
    return ImageFont.load_default()


INTERNAL = [
    ("34-slots", "slots"),
    ("35-recommendations", "recommendations"),
    ("36-handoff", "handoff"),
    ("37-upperstack", "upperstack"),
]


def shots():
    for _name, _scene, _title in SCENES:
        old = OUT / (_name + ".png")
        if old.exists():
            old.unlink()
    if (OUT / "00-overview.png").exists():
        (OUT / "00-overview.png").unlink()
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=CHROME,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        )
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for i, (name, scene, _title) in enumerate(SCENES):
            page.goto(HTML.as_uri() + "?r=" + str(i) + "#view=" + scene, wait_until="load")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(1200 if name in ("36-servers-budget", "37-servers-history") else 420)
            path = OUT / (name + ".png")
            page.screenshot(path=str(path))
            results.append((name, path))
            print("[KCU] shot", name, path.stat().st_size)
        for name, scene in INTERNAL:
            page.goto(HTML.as_uri() + "?r=i" + name + "#view=" + scene, wait_until="load")
            page.wait_for_timeout(220)
            page.screenshot(path=str(OUT / (name + ".png")))
            print("[KCU] internal", name)
        browser.close()
    return results


def overview(results):
    cols, cw, ch, pad, head = 4, 348, 218, 14, 68
    rows = (len(results) + cols - 1) // cols
    width = cols * cw + (cols + 1) * pad
    height = head + rows * (ch + 30 + pad) + pad
    canvas = Image.new("RGB", (width, height), (18, 21, 20))
    d = ImageDraw.Draw(canvas)
    f_title, f_sub, f_lab = font(28), font(15), font(15)
    d.text((pad + 4, 12), f"KCU Launcher · 桌面界面预览（{len(results)} 个视图）", fill=(127, 184, 175), font=f_title)
    d.text((pad + 4, 44), "米纸质感 · 设置归拢 · 核心槽位锁定 · 推荐位总览 · 离线渲染", fill=(189, 186, 176), font=f_sub)
    titles = dict((n, t) for n, _s, t in SCENES)
    for i, (name, path) in enumerate(results):
        r, c = divmod(i, cols)
        x = pad + c * (cw + pad)
        y = head + r * (ch + 30 + pad)
        im = Image.open(path).convert("RGB")
        im.thumbnail((cw, ch), Image.LANCZOS)
        d.rounded_rectangle([x - 2, y - 2, x + cw + 2, y + ch + 2], radius=6, outline=(90, 88, 80), width=1)
        canvas.paste(im, (x + (cw - im.width) // 2, y + (ch - im.height) // 2))
        d.text((x + 3, y + ch + 5), f"{name}  {titles[name]}", fill=(233, 231, 222), font=f_lab)
    out = OUT / "00-overview.png"
    canvas.save(out)
    print("[KCU] overview", out, out.stat().st_size, canvas.size)
    return out


def main():
    results = shots()
    overview(results)
    assert len(list(OUT.glob("[0-9][0-9]-*.png"))) == len(SCENES) + 1 + len(INTERNAL)
    print("[KCU] render_ui OK shots=" + str(len(SCENES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

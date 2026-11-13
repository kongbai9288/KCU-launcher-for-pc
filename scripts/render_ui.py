#!/usr/bin/env python3
"""把整页界面演示按场景渲染为 PNG 预览，并拼一张总览图。"""
import os
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
HTML = ROOT / "demos" / "ui-full-kcu-v2.html"
OUT = ROOT / "demos" / "preview"
OUT.mkdir(parents=True, exist_ok=True)

SCENES = [
    ("01-home", "home", "首页 · 启动与状态"),
    ("02-notices", "notices", "公告中心 · 分类与未读"),
    ("03-notice-detail", "notice-detail", "公告详情弹窗"),
    ("04-onboarding", "onboarding", "首次启动引导"),
    ("05-update", "update", "版本更新提示"),
    ("06-instances", "instances", "实例与服务器列表"),
    ("07-download", "download", "批量下载进度"),
    ("08-login", "login", "三种登录与回退链"),
    ("09-settings", "settings", "设置 · 快速配置中文"),
    ("10-logs", "logs", "日志与诊断包"),
    ("11-error", "error", "异常与边界状态"),
    ("12-about", "about", "关于与界面口径"),
    ("13-popups", "popups", "弹窗全集 11 类"),
    ("14-lightweight", "lightweight", "轻量模式极简视图"),
    ("15-home-light", "home-light", "浅色主题预览"),
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


def shots():
    results = []
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            executable_path=CHROME,
            args=["--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"],
        )
        page = browser.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
        for name, scene, _title in SCENES:
            page.goto(HTML.as_uri() + "#scene=" + scene, wait_until="load")
            page.evaluate("document.fonts.ready")
            page.wait_for_timeout(260)
            path = OUT / (name + ".png")
            page.screenshot(path=str(path))
            results.append((name, path))
            print("[KCU] shot", name, path.stat().st_size)
        browser.close()
    return results


def overview(results):
    cols, cw, ch, pad, head = 3, 460, 288, 16, 70
    rows = (len(results) + cols - 1) // cols
    width = cols * cw + (cols + 1) * pad
    height = head + rows * (ch + 34 + pad) + pad
    canvas = Image.new("RGB", (width, height), (9, 13, 20))
    d = ImageDraw.Draw(canvas)
    f_title, f_sub, f_lab = font(30), font(16), font(17)
    d.text((pad + 4, 14), "KCU Launcher · 界面总览（15 个场景）", fill=(94, 224, 180), font=f_title)
    d.text((pad + 4, 48), "布局重排 · 风格取自样板 · 公告等界面全部可见 · 离线渲染", fill=(148, 165, 191), font=f_sub)
    titles = dict((n, t) for n, _s, t in SCENES)
    for i, (name, path) in enumerate(results):
        r, c = divmod(i, cols)
        x = pad + c * (cw + pad)
        y = head + r * (ch + 34 + pad)
        im = Image.open(path).convert("RGB")
        im.thumbnail((cw, ch), Image.LANCZOS)
        d.rounded_rectangle([x - 2, y - 2, x + cw + 2, y + ch + 2], radius=8, outline=(51, 69, 97), width=1)
        canvas.paste(im, (x + (cw - im.width) // 2, y + (ch - im.height) // 2))
        d.text((x + 4, y + ch + 6), f"{name}  {titles[name]}", fill=(201, 214, 232), font=f_lab)
    out = OUT / "00-overview.png"
    canvas.save(out)
    print("[KCU] overview", out, out.stat().st_size, canvas.size)
    return out


def main():
    results = shots()
    overview(results)
    assert len(list(OUT.glob("[0-9][0-9]-*.png"))) == len(SCENES) + 1
    print("[KCU] render_ui OK shots=" + str(len(SCENES)))
    return 0


if __name__ == "__main__":
    sys.exit(main())

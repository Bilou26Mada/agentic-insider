# Uniform 16:10 cover per tool (brand glow look) for the site. python covers.py -> assets/cover-<slug>.jpg
from pathlib import Path
from playwright.sync_api import sync_playwright
import importlib.util

spec = importlib.util.spec_from_file_location("b", Path(__file__).with_name("build.py"))
src = Path(__file__).with_name("build.py").read_text(encoding="utf-8")
TOOLS = eval(src[src.index("TOOLS = [") + 8: src.index("\nREELS")])
logo = (Path(__file__).parent / "assets/logo.png").resolve().as_uri()
CSS = """* { margin: 0; box-sizing: border-box; } body { width: 1200px; height: 750px; overflow: hidden; background: #0B0B0D; font-family: Inter, sans-serif; color: #fff; position: relative; }
.orb { position: absolute; right: -160px; top: -200px; width: 820px; height: 820px; border-radius: 50%; background: radial-gradient(circle, #FFC86166, #F08A2B2e 38%, transparent 68%); }
.ring { position: absolute; right: 120px; top: 150px; width: 380px; height: 380px; border-radius: 50%; border: 2px solid #F2A65A88; box-shadow: 0 0 60px #F08A2B55, inset 0 0 60px #F08A2B33; }
.ring::after { content: ""; position: absolute; left: 50%; top: 50%; width: 90px; height: 90px; margin: -45px; border-radius: 50%; background: radial-gradient(circle, #FFF6DA, #FFC861 40%, #F08A2B 65%, transparent 72%); filter: drop-shadow(0 0 40px #FF8A1A); }
.by { position: absolute; left: 70px; top: 70px; font-size: 24px; font-weight: 700; letter-spacing: .16em; color: #ffffffa0; text-transform: uppercase; }
h1 { position: absolute; left: 70px; top: 200px; width: 700px; font-family: "Instrument Serif", serif; font-weight: 400; font-size: 120px; line-height: .95; letter-spacing: -0.02em; }
p { position: absolute; left: 70px; top: 470px; width: 640px; font-size: 34px; line-height: 1.25; color: #F3E9DD; }
.st { position: absolute; left: 70px; bottom: 60px; display: flex; gap: 14px; } .st span { padding: 10px 18px; border-radius: 30px; border: 1px solid #ffffff30; font-size: 22px; font-weight: 600; }
.st span:first-child { background: #F2A65A; color: #1a1208; border-color: #F2A65A; }
img { position: absolute; right: 60px; bottom: 55px; width: 64px; height: 64px; border-radius: 50%; }"""
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1200, "height": 750})
    for t in TOOLS:
        pg.set_content(f"""<html><head><link href="https://fonts.googleapis.com/css2?family=Inter:wght@600;700&family=Instrument+Serif&display=swap" rel="stylesheet">
<style>{CSS}</style></head><body><div class="orb"></div><div class="ring"></div><div class="by">{t['by']} · open source</div><h1>{t['name']}</h1>
<p>{t['hook']}</p><div class="st"><span>★ {t['stars']}K on GitHub</span><span>{t['license']}</span><span>Free</span></div><img src="{logo}"></body></html>""", wait_until="networkidle")
        pg.evaluate("document.fonts.ready")
        pg.screenshot(path=str(Path(__file__).parent / f"assets/cover-{t['slug']}.jpg"), type="jpeg", quality=85)
    b.close()
print("covers", len(TOOLS))

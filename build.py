# Static site for Agentic Insider (GitHub Pages). One page per tool from TOOLS, plus index, sitemap, robots.
# python build.py  -> index.html, tools/<slug>.html, sitemap.xml, robots.txt
import html
import json
from datetime import date
from pathlib import Path

BASE = "https://bilou26mada.github.io/agentic-insider"
IG = "https://www.instagram.com/agentic_insider/"
FB = "https://www.facebook.com/agenticinsider"
TOOLS = [
    dict(hook="An AI that uses an Android phone like a human", slug="google-artemis", name="ARTEMIS", by="Google", date="2026-10-26", img="artemis.jpg", stars="14.8K", license="Apache 2.0",
         repo="https://github.com/google/artemis",
         title="Google ARTEMIS: the open-source AI that uses an Android phone like a human",
         lead="You type a task in plain English. ARTEMIS reads the screen, taps, types and swipes on a real Android phone until the job is done.",
         facts=["About 3 to 5 seconds per step", "Over 99% of tasks finished on Google Research's AndroidWorld benchmark (100+ multi-step tasks)",
                "Connects to Claude Code, Cursor, Codex and Windsurf through MCP"],
         steps=["Plug in an Android phone with USB debugging on, or start an emulator.",
                "Clone the repo and run <code>./start.sh</code> (Mac/Linux) or <code>start.bat</code> (Windows).",
                "Let the script install what it needs: ADB, scrcpy, FFmpeg and Python.",
                "Describe the task in plain English and watch the phone do it."]),
    dict(hook="A free Office suite with an AI agent in every file", slug="genoffice", name="GenOffice", by="Genspark", date="2026-10-28", img="genoffice.jpg", stars="10.8K", license="Apache 2.0",
         repo="https://github.com/genspark-ai/genoffice",
         title="GenOffice: a free, open-source Office suite with an AI agent in every document",
         lead="It opens and saves real .docx, .xlsx and .pptx files, and the AI edits the file itself, showing every change as tracked changes you can undo.",
         facts=["Runs on Mac, Windows and Linux", "PDF to Word, Excel or PowerPoint conversion on your own computer",
                "Bring your own key for Claude, ChatGPT, Gemini, DeepSeek or a local model"],
         steps=["Download the installer for your system from the latest release.",
                "Open any Word, Excel or PowerPoint file.",
                "Ask the AI for a change and review it as tracked changes.",
                "Star a folder of documents and ask questions across them, with the source file for every answer."]),
    dict(hook="One photo in, a 3D model written in code out", slug="img2threejs", name="img2threejs", by="open source", date="2026-10-30", img="img2threejs.jpg", stars="19.2K", license="Apache 2.0",
         repo="https://github.com/img2threejs/img2threejs",
         title="img2threejs: turn one photo into a 3D model written entirely in code",
         lead="Give your AI coding agent one reference image and it rebuilds the object as a Three.js model from basic shapes and procedural textures, ready to animate.",
         facts=["No 3D scan and no downloaded models", "Moving parts come already separated, so you can animate right away",
                "Live gallery: a guitar, a cat on Mars, game characters, SpaceX's Starship"],
         steps=["Give your AI coding agent one reference image.",
                "It studies the shapes and proportions.",
                "It writes the model piece by piece and checks it against its own quality gates.",
                "You get a TypeScript file you can drop into any website or game."]),
]
TOOLS.sort(key=lambda t: t["date"], reverse=True)
e = html.escape

CSS = """
:root { --bg: #0B0D12; --card: #141821; --line: #ffffff1c; --text: #EDEFF3; --mute: #9AA4B2; --acc: #F2A65A; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--bg); color: var(--text); font-family: Inter, system-ui, sans-serif; line-height: 1.6; }
a { color: var(--acc); text-decoration: none; } a:hover { text-decoration: underline; }
.wrap { max-width: 860px; margin: 0 auto; padding: 0 20px; }
header.top { display: flex; align-items: center; gap: 14px; padding: 22px 0; border-bottom: 1px solid var(--line); }
header.top img { width: 44px; height: 44px; border-radius: 50%; }
header.top b { font-size: 19px; white-space: nowrap; }
@media (max-width: 520px) { header.top nav a:first-child { display: none; } header.top nav { gap: 12px; font-size: 14px; } } header.top nav { margin-left: auto; display: flex; gap: 18px; font-size: 15px; }
.hero { padding: 64px 0 40px; }
.hero h1 { font-family: "Instrument Serif", Georgia, serif; font-weight: 400; font-size: clamp(40px, 7vw, 68px); line-height: 1.04; letter-spacing: -0.01em; }
.hero h1 em { color: var(--acc); }
.hero p { margin-top: 18px; font-size: 19px; color: var(--mute); max-width: 620px; }
.btns { display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px; }
.btn { display: inline-block; padding: 13px 22px; border-radius: 40px; border: 1px solid var(--line); background: var(--card); color: var(--text); font-weight: 600; }
.btn.pri { background: var(--acc); color: #1a1208; border-color: var(--acc); }
h2.sec { font-size: 14px; letter-spacing: 0.16em; text-transform: uppercase; color: var(--mute); margin: 40px 0 16px; }
.grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 18px; padding-bottom: 60px; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 18px; overflow: hidden; color: var(--text); }
.card:hover { border-color: var(--acc); text-decoration: none; }
.card img { width: 100%; aspect-ratio: 4/5; object-fit: cover; display: block; }
.card div { padding: 16px; } .card small { color: var(--mute); } .card h3 { font-size: 18px; line-height: 1.3; margin-top: 4px; }
article { padding: 44px 0 70px; }
article .meta { color: var(--mute); font-size: 15px; }
article h1 { font-size: clamp(30px, 5vw, 44px); line-height: 1.15; margin: 10px 0 18px; letter-spacing: -0.015em; }
article .lead { font-size: 20px; }
article img.hero-img { width: 100%; max-width: 560px; border-radius: 18px; border: 1px solid var(--line); margin: 28px 0; display: block; }
article h2 { font-size: 24px; margin: 34px 0 12px; }
article ul, article ol { padding-left: 22px; } article li { margin: 8px 0; }
code { background: #ffffff14; padding: 2px 7px; border-radius: 6px; font-size: 0.92em; }
.chips { display: flex; flex-wrap: wrap; gap: 10px; margin-top: 14px; }
.chips span { padding: 7px 14px; border-radius: 30px; background: var(--card); border: 1px solid var(--line); font-size: 14px; font-weight: 600; }
footer { border-top: 1px solid var(--line); padding: 28px 0 40px; color: var(--mute); font-size: 14px; }
"""


def page(title, desc, path, body, ld=None, img="assets/logo.png"):
    url = f"{BASE}/{path}"
    rel = "../" if path.startswith("tools/") else ""
    ldj = f'<script type="application/ld+json">{json.dumps(ld)}</script>' if ld else ""
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url}">
<meta property="og:type" content="{'article' if ld and ld.get('@type') == 'Article' else 'website'}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url}"><meta property="og:image" content="{BASE}/{img}">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}assets/logo.png">
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;600;800&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>{CSS}</style>{ldj}
</head><body><div class="wrap">
<header class="top"><a href="{rel}index.html"><img src="{rel}assets/logo.png" alt="Agentic Insider logo"></a><b>Agentic Insider</b>
<nav><a href="{rel}index.html#tools">Tools</a><a href="{IG}" rel="me">Instagram</a><a href="{FB}" rel="me">Facebook</a></nav></header>
{body}
<footer>Agentic Insider · open-source AI tools and agents, explained in 60 seconds. Facts come from each project's official repository; check it before you install anything.</footer>
</div></body></html>"""


cards = "".join(f'<a class="card" href="tools/{t["slug"]}.html"><img src="assets/{t["img"]}" alt="{e(t["title"])}" loading="lazy">'
                f'<div><small>{t["by"]} · ★ {t["stars"]}</small><h3>{e(t["name"])}: {e(t["hook"])}</h3></div></a>' for t in TOOLS)
home = f"""<section class="hero"><h1>Open-source AI tools and agents, <em>explained in 60 seconds.</em></h1>
<p>Real tests, real repos, links included. A new tool every day on Reels, with the full how-to here.</p>
<div class="btns"><a class="btn pri" href="{IG}">Follow on Instagram</a><a class="btn" href="{FB}">Facebook</a><a class="btn" href="#tools">Latest tools</a></div></section>
<h2 class="sec" id="tools">Latest tools</h2><div class="grid">{cards}</div>"""
org = {"@context": "https://schema.org", "@type": "Organization", "name": "Agentic Insider", "url": BASE + "/",
       "logo": BASE + "/assets/logo.png", "sameAs": [IG, FB]}
Path("index.html").write_text(page("Agentic Insider: open-source AI tools and agents, explained",
                                   "Open-source AI tools and agents explained in 60 seconds: what they do, how to install them, and the official repo link.",
                                   "", home, org), encoding="utf-8")

for t in TOOLS:
    body = f"""<article><div class="meta">{t["by"]} · {t["date"]}</div><h1>{e(t["title"])}</h1>
<p class="lead">{e(t["lead"])}</p>
<div class="chips"><span>★ {t["stars"]} on GitHub</span><span>{t["license"]}</span><span>Free</span></div>
<img class="hero-img" src="../assets/{t["img"]}" alt="{e(t["title"])}">
<h2>Why it matters</h2><ul>{"".join(f"<li>{e(f)}</li>" for f in t["facts"])}</ul>
<h2>How to try it</h2><ol>{"".join(f"<li>{s}</li>" for s in t["steps"])}</ol>
<h2>Official link</h2><p><a href="{t["repo"]}" rel="nofollow">{t["repo"].replace("https://", "")}</a></p>
<div class="btns"><a class="btn pri" href="{IG}">Get one tool like this every day</a><a class="btn" href="../index.html#tools">More tools</a></div></article>"""
    ld = {"@context": "https://schema.org", "@type": "Article", "headline": t["title"], "datePublished": t["date"],
          "image": f"{BASE}/assets/{t['img']}", "author": {"@type": "Organization", "name": "Agentic Insider", "url": BASE + "/"},
          "publisher": {"@type": "Organization", "name": "Agentic Insider", "logo": {"@type": "ImageObject", "url": BASE + "/assets/logo.png"}}}
    Path(f"tools/{t['slug']}.html").write_text(page(t["title"], t["lead"], f"tools/{t['slug']}.html", body, ld, f"assets/{t['img']}"), encoding="utf-8")

urls = [BASE + "/"] + [f"{BASE}/tools/{t['slug']}.html" for t in TOOLS]
Path("sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                               + "".join(f"<url><loc>{u}</loc><lastmod>{date.today()}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
Path("robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
Path(".nojekyll").write_text("")
print("built", len(TOOLS), "tool pages")

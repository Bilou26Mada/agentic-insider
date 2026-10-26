# Agentic Insider static site (GitHub Pages). Layout modelled on the big AI media sites (The Rundown AI): dark hero
# with one promise + CTA, proof strip, then a light rounded panel with filterable "latest drops", a how-it-works row,
# a reels strip, FAQ (FAQPage schema) and a full footer. Brand = the amber glow series.
# python build.py -> index.html, tools/<slug>.html, sitemap.xml, robots.txt
import html
from _theme import THEMES, BASE_CSS, hero
import json
from datetime import date
from pathlib import Path

BASE = "https://bilou26mada.github.io/agentic-insider"
IG = "https://www.instagram.com/agentic_insider/"
FB = "https://www.facebook.com/agenticinsider"
TOOLS = [
    dict(seo="Google ARTEMIS: the AI that uses an Android phone", slug="google-artemis", name="ARTEMIS", by="Google", tag="Agents", date="2026-10-26", img="artemis.jpg", stars=14.8, license="Apache 2.0",
         repo="https://github.com/google/artemis", time="5 min setup",
         hook="Google's open-source AI uses an Android phone like a human",
         lead="You type a task in plain English. ARTEMIS reads the screen, taps, types and swipes on a real Android phone until the job is done.",
         facts=["About 3 to 5 seconds per step", "Over 99% of tasks finished on Google Research's AndroidWorld benchmark (100+ multi-step tasks)",
                "Connects to Claude Code, Cursor, Codex and Windsurf through MCP"],
         steps=["Plug in an Android phone with USB debugging on, or start an emulator.",
                "Clone the repo and run <code>./start.sh</code> (Mac/Linux) or <code>start.bat</code> (Windows).",
                "Let the script install what it needs: ADB, scrcpy, FFmpeg and Python.",
                "Describe the task in plain English and watch the phone do it."],
         good="Testing Android apps, automating repetitive phone tasks", needs="An Android phone or emulator, a computer"),
    dict(seo="GenOffice: free open-source Office suite with AI", slug="genoffice", name="GenOffice", by="Genspark", tag="Productivity", date="2026-10-26", img="genoffice.jpg", stars=10.8, license="Apache 2.0",
         repo="https://github.com/genspark-ai/genoffice", time="2 min install",
         hook="A free Office suite with an AI agent in every document",
         lead="It opens and saves real .docx, .xlsx and .pptx files, and the AI edits the file itself, showing every change as tracked changes you can undo.",
         facts=["Runs on Mac, Windows and Linux", "PDF to Word, Excel or PowerPoint conversion on your own computer",
                "Bring your own key for Claude, ChatGPT, Gemini, DeepSeek or a local model"],
         steps=["Download the installer for your system from the latest release.", "Open any Word, Excel or PowerPoint file.",
                "Ask the AI for a change and review it as tracked changes.",
                "Star a folder of documents and ask questions across them, with the source file for every answer."],
         good="Reports, spreadsheets and decks you edit with AI", needs="Mac, Windows or Linux"),
    dict(seo="img2threejs: turn one photo into a 3D model in code", slug="img2threejs", name="img2threejs", by="Open source", tag="3D & design", date="2026-10-26", img="img2threejs.jpg", stars=19.2,
         license="Apache 2.0", repo="https://github.com/img2threejs/img2threejs", time="Works inside your AI coding agent",
         hook="One photo in, a 3D model written entirely in code out",
         lead="Give your AI coding agent one reference image and it rebuilds the object as a Three.js model from basic shapes and procedural textures, ready to animate.",
         facts=["No 3D scan and no downloaded models", "Moving parts come already separated, so you can animate right away",
                "Live gallery: a guitar, a cat on Mars, game characters, SpaceX's Starship"],
         steps=["Give your AI coding agent one reference image.", "It studies the shapes and proportions.",
                "It writes the model piece by piece and checks it against its own quality gates.",
                "You get a TypeScript file you can drop into any website or game."],
         good="Web 3D, games, product showcases", needs="An AI coding agent (Claude Code, Codex, Cursor)"),
]
REELS = [("reel-glow3.jpg", "What your AI is doing while you wait", "https://www.instagram.com/reel/De7UCLhzZNC/"),
         ("reel-drift.jpg", "AI copied one photo 20 times", IG),
         ("reel-team.jpg", "My whole team is 7 Claude tabs", IG)]
FAQ = [("What is Agentic Insider?", "A daily media on open-source AI tools and AI agents. Every tool gets a 60-second video on Instagram and Facebook, and a page here with what it does, how to install it and the official link."),
       ("Are the tools free?", "Every tool we cover is open source with a free license (for example MIT or Apache 2.0). Some let you plug in a paid AI model if you want to."),
       ("Do you test the tools?", "We check every claim against the project's official repository and documentation, and we link to it so you can verify before installing anything."),
       ("How often is there something new?", "A new reel every day on Instagram, and a new tool page here several times a week.")]
TOOLS.sort(key=lambda t: t["slug"] != "google-artemis")  # featured first: the flagship post
for t in TOOLS:
    t["cover"] = f"cover-{t['slug']}.jpg"
e = html.escape
fmt_date = lambda d: date.fromisoformat(d).strftime("%b %d, %Y").replace(" 0", " ")

CSS = """
:root { --paper: #FBFAF7; --ink: #111111; --soft: #4A4A4A; --mute: #7A7670; --rule: #1111111f; --rule2: #111111; --acc: #C2410C; --tint: #F3EFE8; }
* { margin: 0; padding: 0; box-sizing: border-box; }
body { background: var(--paper); color: var(--ink); font-family: "Public Sans", system-ui, sans-serif; font-size: 17px; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
img { height: auto; max-width: 100%; }
.wrap { max-width: 1180px; margin: 0 auto; padding: 0 24px; }
.serif { font-family: "Newsreader", Georgia, serif; }
/* masthead */
.top { border-bottom: 1px solid var(--rule); font-size: 13px; color: var(--mute); }
.top .wrap { display: flex; justify-content: space-between; height: 38px; align-items: center; }
.top a:hover { color: var(--ink); }
.mast { text-align: center; padding: 30px 0 18px; }
.mast .name { font-family: "Newsreader", Georgia, serif; font-weight: 600; font-size: clamp(42px, 7vw, 76px); letter-spacing: -0.03em; line-height: 1; }
.mast .tag { margin-top: 8px; font-size: 15px; color: var(--soft); }
.sections { border-top: 2px solid var(--rule2); border-bottom: 1px solid var(--rule); }
.sections .wrap { display: flex; justify-content: center; gap: 28px; height: 46px; align-items: center; font-size: 14px; font-weight: 600; letter-spacing: .02em; }
.sections a:hover, .sections a.on { color: var(--acc); }
.slim { position: sticky; top: 0; z-index: 10; background: var(--paper); border-bottom: 1px solid var(--rule); }
.slim .wrap { display: flex; align-items: center; height: 58px; gap: 22px; }
.slim .logo { font-family: "Newsreader", serif; font-weight: 600; font-size: 24px; letter-spacing: -0.02em; }
.slim nav { margin-left: auto; display: flex; gap: 22px; font-size: 14px; font-weight: 600; }
.slim nav a:hover { color: var(--acc); }
/* labels, buttons */
.kick { font-size: 12px; font-weight: 700; letter-spacing: .12em; text-transform: uppercase; color: var(--acc); }
.meta { font-size: 13px; color: var(--mute); }
.btn { display: inline-block; padding: 11px 18px; font-weight: 600; font-size: 15px; border: 1px solid var(--ink); border-radius: 3px; }
.btn.pri { background: var(--ink); color: var(--paper); }
.btn:hover { background: var(--acc); border-color: var(--acc); color: #fff; }
/* front page */
.front { display: grid; grid-template-columns: minmax(0, 2fr) minmax(0, 1fr); gap: 0; padding: 34px 0 40px; border-bottom: 1px solid var(--rule); }
.lead-story { padding-right: 34px; border-right: 1px solid var(--rule); }
.lead-story img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; }
.lead-story h1 { font-family: "Newsreader", serif; font-weight: 600; font-size: clamp(32px, 4.2vw, 50px); line-height: 1.06; letter-spacing: -0.02em; margin: 16px 0 12px; }
.lead-story h1 a:hover, .item h3 a:hover, .list h3 a:hover { text-decoration: underline; text-decoration-thickness: 1px; text-underline-offset: 4px; }
.lead-story p { font-size: 19px; color: var(--soft); max-width: 720px; }
.rail { padding-left: 30px; }
.rail .item { padding: 0 0 22px; margin-bottom: 22px; border-bottom: 1px solid var(--rule); }
.rail .item:last-child { border-bottom: 0; margin-bottom: 0; }
.rail img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; margin-bottom: 12px; }
.item h3 { font-family: "Newsreader", serif; font-weight: 600; font-size: 23px; line-height: 1.18; letter-spacing: -0.01em; margin: 6px 0 6px; }
.block { padding: 40px 0; border-bottom: 1px solid var(--rule); }
.block > .head { display: flex; align-items: baseline; justify-content: space-between; border-top: 2px solid var(--rule2); padding-top: 10px; margin-bottom: 22px; }
.block > .head h2 { font-family: "Newsreader", serif; font-size: 26px; font-weight: 600; letter-spacing: -0.01em; }
.list { display: grid; grid-template-columns: repeat(3, 1fr); gap: 28px; }
.list article { border-top: 1px solid var(--rule); padding-top: 14px; }
.list .n { font-family: "Newsreader", serif; font-size: 34px; color: var(--acc); line-height: 1; }
.list h3 { font-family: "Newsreader", serif; font-size: 21px; line-height: 1.2; margin: 8px 0 6px; font-weight: 600; }
.reels { display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; max-width: 900px; }
.reels a { display: block; } .reels img { width: 100%; aspect-ratio: 9/16; object-fit: cover; display: block; }
.reels span { display: block; margin-top: 10px; font-family: "Newsreader", serif; font-weight: 600; font-size: 18px; line-height: 1.25; }
.reels a:hover span { color: var(--acc); }
.about { display: grid; grid-template-columns: 1fr 2fr; gap: 40px; }
.about p { font-size: 19px; color: var(--soft); margin-bottom: 14px; max-width: 700px; }
.about dl { font-size: 16px; } .about dt { font-weight: 700; margin-top: 16px; } .about dd { color: var(--soft); }
.follow { display: flex; align-items: center; justify-content: space-between; gap: 20px; padding: 30px; background: var(--tint); margin: 40px 0; }
.follow h2 { font-family: "Newsreader", serif; font-size: 28px; font-weight: 600; } .follow p { color: var(--soft); }
.follow .btns { display: flex; gap: 10px; flex-wrap: wrap; }
footer { border-top: 2px solid var(--rule2); padding: 26px 0 40px; font-size: 14px; color: var(--mute); }
footer .wrap { display: flex; flex-wrap: wrap; justify-content: space-between; gap: 16px; }
footer .logo { font-family: "Newsreader", serif; font-weight: 600; font-size: 22px; color: var(--ink); }
footer nav { display: flex; gap: 18px; } footer a:hover { color: var(--ink); }
/* article */
.panel { background: var(--paper); }
.crumbs { font-size: 13px; color: var(--mute); padding-top: 26px; } .crumbs a:hover { color: var(--ink); }
.art { display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 56px; align-items: start; padding-bottom: 20px; }
.art article { max-width: 700px; }
.art h2 { font-family: "Newsreader", serif; font-size: 28px; font-weight: 600; letter-spacing: -0.01em; margin: 38px 0 12px; }
.art ul, .art ol { padding-left: 22px; font-size: 18px; } .art li { margin: 10px 0; }
.art .byline { margin-top: 20px; padding: 14px 0; border-top: 1px solid var(--rule); border-bottom: 1px solid var(--rule); font-size: 14px; color: var(--mute); }
code { background: #1111110d; padding: 1px 6px; font-size: 0.88em; border-radius: 3px; }
.glance { position: sticky; top: 82px; border-top: 2px solid var(--rule2); padding-top: 12px; margin-top: 26px; }
.glance h4 { font-size: 12px; letter-spacing: .12em; text-transform: uppercase; margin-bottom: 8px; }
.glance dl { display: grid; grid-template-columns: auto 1fr; font-size: 15px; }
.glance dt, .glance dd { padding: 9px 0; border-bottom: 1px solid var(--rule); } .glance dt { color: var(--mute); padding-right: 14px; } .glance dd { font-weight: 600; }
.glance .btn { display: block; text-align: center; margin-top: 16px; }
.more { display: grid; grid-template-columns: repeat(2, 1fr); gap: 26px; }
.more img { width: 100%; aspect-ratio: 16/9; object-fit: cover; display: block; margin-bottom: 10px; }
.hero { text-align: center; padding: 90px 0; } .hero h1 { font-family: "Newsreader", serif; font-size: 54px; font-weight: 600; } .hero p { color: var(--soft); margin: 10px 0 24px; }
.hidden { display: none !important; }
@media (max-width: 860px) {
  .front, .about, .art { grid-template-columns: 1fr; } .lead-story { padding-right: 0; border-right: 0; } .rail { padding-left: 0; margin-top: 30px; }
  .list, .more { grid-template-columns: 1fr; } .reels { grid-template-columns: repeat(2, 1fr); } .sections .wrap { gap: 18px; overflow-x: auto; justify-content: flex-start; }
  .top .ed { display: none; } .follow { flex-direction: column; align-items: flex-start; } .glance { position: static; } .slim nav a.x { display: none; }
}
"""
JS = ""


def shell(title, desc, path, body, ld, img="assets/og-home.jpg", iw=1200, ih=630, extra_css="", font=""):
    rel = "../" if "/" in path else ""
    url = f"{BASE}/{path}"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    today = date.today().strftime("%A, %B %d, %Y").replace(" 0", " ")
    if rel:  # article pages: slim sticky bar
        header = (f'<header class="slim"><div class="wrap"><a class="logo" href="../index.html">Agentic Insider</a>'
                  f'<nav><a class="x" href="../index.html#latest">Latest</a><a class="x" href="../index.html#reels">Reels</a><a href="{IG}">Instagram</a></nav></div></header>')
    else:
        header = (f'<div class="top"><div class="wrap"><span class="ed">{today}</span><span><a href="{IG}">Instagram</a> · <a href="{FB}">Facebook</a> · <a href="feed.xml">RSS</a></span></div></div>'
                  f'<header class="mast"><div class="wrap"><a class="name" href="index.html">Agentic Insider</a>'
                  f'<div class="tag">The open-source AI tools worth your time, explained.</div></div></header>'
                  f'<nav class="sections"><div class="wrap"><a class="on" href="#latest">Latest</a><a href="#tools">All tools</a><a href="#reels">Reels</a><a href="#about">About</a></div></nav>')
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<link rel="alternate" type="application/rss+xml" title="Agentic Insider" href="{BASE}/feed.xml">
<meta name="theme-color" content="#FBFAF7">
<meta property="og:site_name" content="Agentic Insider"><meta property="og:type" content="{'article' if rel else 'website'}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/{img}"><meta property="og:image:width" content="{iw}"><meta property="og:image:height" content="{ih}">
<meta property="og:image:alt" content="{e(title)}"><meta property="og:locale" content="en_US"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}assets/logo-128.png"><link rel="apple-touch-icon" href="{rel}assets/logo-128.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,500;6..72,600&family=Public+Sans:wght@400;600;700&display=swap" rel="stylesheet">
{f'<link href="https://fonts.googleapis.com/css2?family={font}&display=swap" rel="stylesheet">' if font else ""}<style>{CSS}{extra_css}</style>{lds}
</head><body>
{header}
{body}
<footer><div class="wrap"><a class="logo" href="{rel}index.html">Agentic Insider</a>
<nav><a href="{rel}index.html#about">About</a><a href="{IG}" rel="me">Instagram</a><a href="{FB}" rel="me">Facebook</a><a href="{rel}feed.xml">RSS</a></nav>
<span>© {date.today().year} Agentic Insider. Facts checked against each project's official repository.</span></div></footer>
</body></html>"""


def tile(t, cls=""):  # used for "more tools" on article pages
    return (f'<a class="item" href="tools/{t["slug"]}.html"><img src="assets/{t["cover"]}" width="1600" height="900" alt="{e(t["name"])}" loading="lazy">'
            f'<div class="kick">{t["tag"]}</div><h3>{e(t["hook"])}</h3><div class="meta">{t["by"]} · {fmt_date(t["date"])}</div></a>')


lead, rest = TOOLS[0], TOOLS[1:]
home = f"""<main class="wrap">
<section class="front" id="latest">
<article class="lead-story"><a href="tools/{lead["slug"]}.html"><img src="assets/{lead["cover"]}" width="1600" height="900" alt="{e(lead["name"])}"></a>
<div class="kick" style="margin-top:16px">{lead["tag"]} · {lead["by"]}</div>
<h1><a href="tools/{lead["slug"]}.html">{e(lead["hook"])}</a></h1><p>{e(lead["lead"])}</p>
<div class="meta" style="margin-top:12px">{fmt_date(lead["date"])} · ★ {lead["stars"]}K on GitHub · {lead["license"]}</div></article>
<aside class="rail">{"".join(f'<article class="item"><a href="tools/{t["slug"]}.html"><img src="assets/{t["cover"]}" width="1600" height="900" alt="{e(t["name"])}" loading="lazy"></a>'
                             f'<div class="kick">{t["tag"]} · {t["by"]}</div><h3><a href="tools/{t["slug"]}.html">{e(t["hook"])}</a></h3>'
                             f'<div class="meta">{fmt_date(t["date"])} · ★ {t["stars"]}K</div></article>' for t in rest)}</aside>
</section>
<section class="block" id="tools"><div class="head"><h2>All tools</h2><span class="meta">{len(TOOLS)} covered so far</span></div><div class="list">
{"".join(f'<article><div class="n">{k + 1:02d}</div><h3><a href="tools/{t["slug"]}.html">{e(t["name"])}: {e(t["hook"])}</a></h3>'
         f'<div class="meta">{t["by"]} · {t["license"]} · ★ {t["stars"]}K</div></article>' for k, t in enumerate(TOOLS))}</div></section>
<section class="block" id="reels"><div class="head"><h2>Reels</h2><a class="meta" href="{IG}">More on Instagram →</a></div><div class="reels">
{"".join(f'<a href="{u}"><img src="assets/{i}" width="540" height="960" alt="{e(c)}" loading="lazy"><span>{e(c)}</span></a>' for i, c, u in REELS)}</div></section>
<section class="block" id="about"><div class="head"><h2>About</h2></div><div class="about">
<dl>{"".join(f"<dt>{e(q)}</dt><dd>{e(a)}</dd>" for q, a in FAQ[1:])}</dl>
<div><p>Agentic Insider covers the open-source AI tools and agents that do something genuinely new. Every pick gets a short video on Instagram and Facebook, and a page here that says what it does, who built it and how to install it.</p>
<p>Every number on this site comes from the project's own repository, and we link to it so you can check before you install anything.</p></div></div></section>
<section class="follow"><div><h2>A new tool, most days.</h2><p>Follow along wherever you scroll.</p></div>
<div class="btns"><a class="btn pri" href="{IG}">Instagram</a><a class="btn" href="{FB}">Facebook</a></div></section>
</main>"""
org = {"@context": "https://schema.org", "@type": "Organization", "name": "Agentic Insider", "url": BASE + "/", "logo": BASE + "/assets/logo.png", "sameAs": [IG, FB]}
site = {"@context": "https://schema.org", "@type": "WebSite", "name": "Agentic Insider", "url": BASE + "/"}
faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
Path("index.html").write_text(shell("Agentic Insider: Open-Source AI Tools, Explained",
                                    "The open-source AI tools and agents worth your time, checked against the source and explained in 60 seconds, with install steps and official links.",
                                    "", home, [org, site, faq]), encoding="utf-8")

for t in TOOLS:
    others = [o for o in TOOLS if o is not t]
    body = hero(t) + f"""<main class="panel"><div class="wrap"><div class="art"><article>
<div class="crumbs"><a href="../index.html">Agentic Insider</a> / <a href="../index.html#tools">Tools</a> / {e(t["name"])}</div>
<div class="byline">By the Agentic Insider desk · {fmt_date(t["date"])} · Sources: <a href="{t["repo"]}" rel="nofollow">{t["repo"].replace("https://github.com/", "")}</a></div>
<h2>Why it matters</h2><ul>{"".join(f"<li>{e(f)}</li>" for f in t["facts"])}</ul>
<h2>How to try it</h2><ol>{"".join(f"<li>{s}</li>" for s in t["steps"])}</ol>
<h2>Official link</h2><p style="font-size:18px"><a style="color:var(--acc);font-weight:600;text-decoration:underline" href="{t["repo"]}" rel="nofollow">{t["repo"].replace("https://", "")}</a></p>
<h2>More tools</h2><div class="more">{"".join(tile(o).replace('href="tools/', 'href="').replace('src="assets/', 'src="../assets/') for o in others[:2])}</div>
</article><aside class="glance"><h4>At a glance</h4><dl><dt>Tool</dt><dd>{e(t["name"])}</dd><dt>By</dt><dd>{e(t["by"])}</dd>
<dt>Stars</dt><dd>★ {t["stars"]}K</dd><dt>License</dt><dd>{t["license"]}</dd><dt>Price</dt><dd>Free</dd><dt>Setup</dt><dd>{e(t["time"])}</dd>
<dt>Good for</dt><dd>{e(t["good"])}</dd><dt>You need</dt><dd>{e(t["needs"])}</dd></dl>
<a class="btn pri" href="{t["repo"]}" rel="nofollow">Open on GitHub</a><a class="btn" href="{IG}">Follow on Instagram</a></aside></div>
<section class="follow"><div><h2>A new tool, most days.</h2><p>Follow along wherever you scroll.</p></div><div class="btns"><a class="btn pri" href="{IG}">Instagram</a><a class="btn" href="{FB}">Facebook</a></div></section>
</div></main>"""
    art = {"@context": "https://schema.org", "@type": "Article", "headline": t["hook"], "description": t["lead"], "datePublished": t["date"],
           "image": f"{BASE}/assets/{t['cover']}", "dateModified": t["date"], "mainEntityOfPage": f"{BASE}/tools/{t['slug']}.html",
           "author": {"@type": "Organization", "name": "Agentic Insider", "url": BASE + "/"},
           "publisher": {"@type": "Organization", "name": "Agentic Insider", "logo": {"@type": "ImageObject", "url": BASE + "/assets/logo.png"}},
           "about": {"@type": "SoftwareApplication", "name": t["name"], "applicationCategory": "DeveloperApplication", "offers": {"@type": "Offer", "price": "0"}, "url": t["repo"]}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": t["name"], "item": f"{BASE}/tools/{t['slug']}.html"}]}
    Path(f"tools/{t['slug']}.html").write_text(shell(t["seo"], t["lead"], f"tools/{t['slug']}.html", body,
                                                     [art, crumbs], f"assets/{t['cover']}", 1200, 750, BASE_CSS + THEMES[t['slug']]['css'], THEMES[t['slug']]['font']), encoding="utf-8")

urls = [(BASE + "/", max(t['date'] for t in TOOLS))] + [(f"{BASE}/tools/{t['slug']}.html", t['date']) for t in TOOLS]
Path("sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                               + "".join(f"<url><loc>{u}</loc><lastmod>{d}</lastmod></url>\n" for u, d in urls) + "</urlset>\n", encoding="utf-8")
Path("robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
Path(".nojekyll").write_text("")
# RSS feed (discovery by readers and search engines) + a branded 404
items = "".join(f"<item><title>{e(t['name'])}: {e(t['hook'])}</title><link>{BASE}/tools/{t['slug']}.html</link><guid>{BASE}/tools/{t['slug']}.html</guid>"
                f"<pubDate>{date.fromisoformat(t['date']).strftime('%a, %d %b %Y')} 12:00:00 +0000</pubDate><description>{e(t['lead'])}</description></item>" for t in TOOLS)
Path("feed.xml").write_text(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>Agentic Insider</title><link>{BASE}/</link>'
                            f'<description>Open-source AI tools and agents, explained in 60 seconds.</description><language>en</language>{items}</channel></rss>', encoding="utf-8")
nf = shell("Page not found | Agentic Insider", "This page does not exist.", "404.html",
           f'<section class="hero"><div class="wrap"><h1>Page not found</h1><p>The page you were looking for has moved or never existed.</p>'
           f'<div class="btns"><a class="btn pri" href="{BASE}/">Back to the tools</a></div></div></section>', [])
Path("404.html").write_text(nf.replace('content="index, follow', 'content="noindex, follow').replace('href="index.html', f'href="{BASE}/index.html').replace('src="assets/', f'src="{BASE}/assets/').replace('href="assets/', f'href="{BASE}/assets/'), encoding="utf-8")

print("built", len(TOOLS), "tool pages")

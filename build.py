# Agentic Insider static site (GitHub Pages). Layout modelled on the big AI media sites (The Rundown AI): dark hero
# with one promise + CTA, proof strip, then a light rounded panel with filterable "latest drops", a how-it-works row,
# a reels strip, FAQ (FAQPage schema) and a full footer. Brand = the amber glow series.
# python build.py -> index.html, tools/<slug>.html, sitemap.xml, robots.txt
import html
import json
from datetime import date
from pathlib import Path

BASE = "https://bilou26mada.github.io/agentic-insider"
IG = "https://www.instagram.com/agentic_insider/"
FB = "https://www.facebook.com/agenticinsider"
TOOLS = [
    dict(slug="google-artemis", name="ARTEMIS", by="Google", tag="Agents", date="2026-10-26", img="artemis.jpg", stars=14.8, license="Apache 2.0",
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
    dict(slug="genoffice", name="GenOffice", by="Genspark", tag="Productivity", date="2026-10-28", img="genoffice.jpg", stars=10.8, license="Apache 2.0",
         repo="https://github.com/genspark-ai/genoffice", time="2 min install",
         hook="A free Office suite with an AI agent in every document",
         lead="It opens and saves real .docx, .xlsx and .pptx files, and the AI edits the file itself, showing every change as tracked changes you can undo.",
         facts=["Runs on Mac, Windows and Linux", "PDF to Word, Excel or PowerPoint conversion on your own computer",
                "Bring your own key for Claude, ChatGPT, Gemini, DeepSeek or a local model"],
         steps=["Download the installer for your system from the latest release.", "Open any Word, Excel or PowerPoint file.",
                "Ask the AI for a change and review it as tracked changes.",
                "Star a folder of documents and ask questions across them, with the source file for every answer."],
         good="Reports, spreadsheets and decks you edit with AI", needs="Mac, Windows or Linux"),
    dict(slug="img2threejs", name="img2threejs", by="Open source", tag="3D & design", date="2026-10-30", img="img2threejs.jpg", stars=19.2,
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
         ("reel-glow1.jpg", "How an AI agent works, in 7 moves", IG),
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
:root { --ink: #0B0B0D; --ink2: #15151A; --paper: #FAF7F2; --card: #FFFFFF; --line: #ECE6DC; --text: #17120E; --mute: #6B6258;
  --light: #F3E9DD; --acc: #F2A65A; --acc2: #E2672C; --r: 22px; }
* { margin: 0; padding: 0; box-sizing: border-box; }
html { scroll-behavior: smooth; }
body { background: var(--ink); color: var(--light); font-family: Inter, system-ui, sans-serif; line-height: 1.6; -webkit-font-smoothing: antialiased; }
a { color: inherit; text-decoration: none; }
.wrap { max-width: 1160px; margin: 0 auto; padding: 0 22px; }
/* nav */
.nav { position: sticky; top: 0; z-index: 20; background: #0B0B0Dd9; backdrop-filter: blur(14px); border-bottom: 1px solid #ffffff12; }
.nav .wrap { display: flex; align-items: center; height: 68px; gap: 28px; }
.brand { display: flex; align-items: center; gap: 11px; font-weight: 700; font-size: 18px; white-space: nowrap; }
.brand img { width: 34px; height: 34px; border-radius: 50%; }
.links { display: flex; gap: 26px; font-size: 15px; color: #ffffffc0; }
.links a:hover { color: #fff; }
.nav .cta { margin-left: auto; }
.btn { display: inline-flex; align-items: center; gap: 8px; padding: 12px 22px; border-radius: 12px; font-weight: 600; font-size: 15px; border: 1px solid #ffffff24; transition: .2s; }
.btn:hover { transform: translateY(-1px); }
.btn.pri { background: var(--acc); color: #1a1208; border-color: var(--acc); box-shadow: 0 8px 30px #F2A65A40; }
.btn.light { background: #fff; color: var(--ink); border-color: #fff; }
.btn.ghost { color: var(--text); border-color: var(--line); background: var(--card); }
/* hero */
.hero { position: relative; text-align: center; padding: 110px 0 70px; overflow: hidden; }
.orb { position: absolute; left: 50%; top: -120px; width: 640px; height: 640px; transform: translateX(-50%); border-radius: 50%;
  background: radial-gradient(circle, #FFC86155 0%, #F08A2B26 35%, transparent 68%); filter: blur(10px); pointer-events: none; animation: breathe 7s ease-in-out infinite; }
@keyframes breathe { 50% { transform: translateX(-50%) scale(1.08); opacity: .8; } }
.eyebrow { display: inline-flex; align-items: center; gap: 10px; padding: 7px 14px; border: 1px solid #ffffff1f; border-radius: 30px; font-size: 13px; color: #ffffffb0; background: #ffffff08; }
.eyebrow i { width: 8px; height: 8px; border-radius: 50%; background: #34A853; box-shadow: 0 0 10px #34A853; }
.hero h1 { position: relative; margin: 26px auto 0; max-width: 900px; font-family: "Instrument Serif", Georgia, serif; font-weight: 400;
  font-size: clamp(46px, 8vw, 92px); line-height: 0.98; letter-spacing: -0.02em; color: #fff; }
.hero h1 em { background: linear-gradient(95deg, #FFD08A, #F2A65A 45%, #E8602C); -webkit-background-clip: text; background-clip: text; color: transparent; }
.hero p { position: relative; margin: 24px auto 0; max-width: 560px; font-size: 19px; color: #ffffffb8; }
.hero .btns { position: relative; display: flex; justify-content: center; flex-wrap: wrap; gap: 12px; margin-top: 34px; }
.proof { position: relative; display: flex; justify-content: center; flex-wrap: wrap; gap: 14px 46px; margin-top: 58px; color: #ffffff8c; font-size: 14px; }
.proof b { display: block; color: #fff; font-size: 26px; font-weight: 700; letter-spacing: -0.02em; }
/* light panel */
.panel { background: var(--paper); color: var(--text); border-radius: 34px 34px 0 0; margin: 0 14px; padding: 80px 0 30px; }
.panel h2 { font-size: clamp(30px, 4vw, 44px); letter-spacing: -0.025em; line-height: 1.1; text-align: center; }
.panel .sub { text-align: center; color: var(--mute); font-size: 18px; margin-top: 10px; }
.tabs { display: flex; justify-content: center; gap: 6px; margin: 28px auto 38px; padding: 5px; width: max-content; max-width: 100%; overflow-x: auto;
  background: var(--card); border: 1px solid var(--line); border-radius: 14px; }
.tabs button { border: 0; background: none; font: 600 15px Inter, sans-serif; padding: 9px 16px; border-radius: 10px; color: var(--mute); cursor: pointer; white-space: nowrap; }
.tabs button.on { background: var(--ink); color: #fff; }
.drops { display: grid; grid-template-columns: 1.4fr 1fr; gap: 28px; align-items: start; }
.drops .side { display: grid; gap: 22px; }
.tile { display: flex; flex-direction: column; background: var(--card); border: 1px solid var(--line); border-radius: var(--r); overflow: hidden; transition: .25s; }
.tile:hover { transform: translateY(-3px); box-shadow: 0 18px 40px #17120E14; }
.tile .im { position: relative; background: var(--ink); }
.tile img { width: 100%; height: 100%; object-fit: cover; display: block; }
.tile .im { aspect-ratio: 16/10; }
.badge { position: absolute; right: 12px; top: 12px; padding: 4px 10px; border-radius: 8px; background: #fff; color: var(--text); font-size: 12px; font-weight: 700; }
.tile .tx { padding: 20px 22px; }
.tile h3 { font-size: 20px; line-height: 1.25; letter-spacing: -0.01em; } .feat h3 { font-size: 30px; }
.tile .meta { margin-top: 10px; font-size: 13px; color: var(--mute); } .tile p { margin-top: 8px; color: var(--mute); }
.hidden { display: none !important; }
.how { display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; margin-top: 44px; }
.step { background: var(--card); border: 1px solid var(--line); border-radius: var(--r); padding: 28px; }
.step b { display: inline-grid; place-items: center; width: 40px; height: 40px; border-radius: 12px; background: #F2A65A26; color: var(--acc2); font-size: 18px; }
.step h3 { margin-top: 16px; font-size: 20px; } .step p { margin-top: 6px; color: var(--mute); }
.sec { padding-top: 90px; }
.reels { display: grid; grid-template-columns: repeat(4, 1fr); gap: 18px; margin-top: 40px; }
.reel { position: relative; border-radius: 18px; overflow: hidden; aspect-ratio: 9/16; background: var(--ink); }
.reel img { width: 100%; height: 100%; object-fit: cover; transition: .3s; } .reel:hover img { transform: scale(1.04); }
.reel span { position: absolute; left: 0; right: 0; bottom: 0; padding: 50px 16px 16px; color: #fff; font-weight: 600; font-size: 15px; line-height: 1.3;
  background: linear-gradient(transparent, #000d); }
.reel::after { content: "▶"; position: absolute; right: 12px; top: 12px; width: 34px; height: 34px; border-radius: 50%; background: #ffffffd9; color: var(--ink);
  display: grid; place-items: center; font-size: 12px; }
.faq { max-width: 760px; margin: 40px auto 0; }
.faq details { background: var(--card); border: 1px solid var(--line); border-radius: 16px; padding: 18px 22px; margin-bottom: 12px; }
.faq summary { font-weight: 600; font-size: 17px; cursor: pointer; list-style: none; display: flex; justify-content: space-between; }
.faq summary::after { content: "+"; color: var(--acc2); font-size: 22px; line-height: 1; } .faq details[open] summary::after { content: "–"; }
.faq p { margin-top: 10px; color: var(--mute); }
.band { margin: 90px 0 60px; padding: 56px 30px; border-radius: 28px; text-align: center; color: #fff;
  background: radial-gradient(ellipse at 50% 0%, #F08A2B55, transparent 60%), var(--ink); }
.band h2 { font-family: "Instrument Serif", serif; font-weight: 400; font-size: clamp(34px, 5vw, 54px); }
.band p { color: #ffffffb0; margin: 10px 0 26px; }
footer { background: var(--paper); color: var(--mute); margin: 0 14px; padding: 0 0 40px; font-size: 14px; }
footer .cols { display: grid; grid-template-columns: 2fr 1fr 1fr; gap: 30px; border-top: 1px solid var(--line); padding-top: 34px; }
footer b { color: var(--text); display: block; margin-bottom: 8px; } footer a { display: block; margin: 4px 0; } footer a:hover { color: var(--text); }
/* article */
.crumbs { font-size: 14px; color: var(--mute); } .crumbs a:hover { color: var(--text); }
.art { display: grid; grid-template-columns: minmax(0, 1fr) 320px; gap: 50px; align-items: start; }
.art h1 { font-size: clamp(32px, 4.6vw, 50px); line-height: 1.08; letter-spacing: -0.03em; margin: 14px 0 18px; }
.art .lead { font-size: 21px; color: #3a322b; }
.art img.cover { width: 100%; border-radius: var(--r); border: 1px solid var(--line); margin: 30px 0 10px; display: block; }
.art h2 { font-size: 26px; letter-spacing: -0.02em; margin: 40px 0 12px; text-align: left; }
.art ul, .art ol { padding-left: 22px; font-size: 18px; } .art li { margin: 10px 0; }
code { background: #17120E0f; padding: 2px 7px; border-radius: 6px; font-size: 0.9em; }
.glance { position: sticky; top: 96px; background: var(--card); border: 1px solid var(--line); border-radius: var(--r); padding: 24px; }
.glance h4 { font-size: 13px; letter-spacing: .14em; text-transform: uppercase; color: var(--mute); margin-bottom: 10px; }
.glance dl { display: grid; grid-template-columns: auto 1fr; gap: 10px 16px; font-size: 15px; } .glance dt { color: var(--mute); } .glance dd { font-weight: 600; }
.glance .btn { width: 100%; justify-content: center; margin-top: 18px; }
.more { display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; margin-top: 20px; }
@media (max-width: 900px) {
  .links { display: none; } .drops, .art { grid-template-columns: 1fr; } .how { grid-template-columns: 1fr; }
  .reels { grid-template-columns: repeat(2, 1fr); } footer .cols { grid-template-columns: 1fr; } .glance { position: static; }
  .more { grid-template-columns: 1fr; }
  .panel, footer { margin: 0; } .hero { padding-top: 80px; }
}
"""
JS = """<script>
document.querySelectorAll('.tabs button').forEach(b => b.onclick = () => {
  document.querySelectorAll('.tabs button').forEach(x => x.classList.toggle('on', x === b));
  document.querySelectorAll('[data-tag]').forEach(t => t.classList.toggle('hidden', b.dataset.f !== 'All' && t.dataset.tag !== b.dataset.f));
});
</script>"""


def shell(title, desc, path, body, ld, img="assets/logo.png"):
    rel = "../" if "/" in path else ""
    url = f"{BASE}/{path}"
    lds = "".join(f'<script type="application/ld+json">{json.dumps(x)}</script>' for x in ld)
    return f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}"><link rel="canonical" href="{url}">
<meta name="theme-color" content="#0B0B0D">
<meta property="og:site_name" content="Agentic Insider"><meta property="og:type" content="{'article' if rel else 'website'}">
<meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}"><meta property="og:url" content="{url}">
<meta property="og:image" content="{BASE}/{img}"><meta name="twitter:card" content="summary_large_image">
<link rel="icon" href="{rel}assets/logo.png"><link rel="apple-touch-icon" href="{rel}assets/logo.png">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Instrument+Serif:ital@0;1&display=swap" rel="stylesheet">
<style>{CSS}</style>{lds}
</head><body>
<header class="nav"><div class="wrap"><a class="brand" href="{rel}index.html"><img src="{rel}assets/logo.png" alt="Agentic Insider">Agentic Insider</a>
<nav class="links"><a href="{rel}index.html#drops">Tools</a><a href="{rel}index.html#how">How it works</a><a href="{rel}index.html#reels">Reels</a><a href="{rel}index.html#faq">FAQ</a></nav>
<a class="btn light cta" href="{IG}">Follow</a></div></header>
{body}
<footer><div class="wrap cols">
<div><b>Agentic Insider</b>Open-source AI tools and agents, explained in 60 seconds. Every fact is checked against the project's official repository.</div>
<div><b>Explore</b><a href="{rel}index.html#drops">Latest tools</a><a href="{rel}index.html#reels">Reels</a><a href="{rel}index.html#faq">FAQ</a></div>
<div><b>Follow</b><a href="{IG}" rel="me">Instagram</a><a href="{FB}" rel="me">Facebook</a></div>
</div><div class="wrap" style="margin-top:26px">© {date.today().year} Agentic Insider</div></footer>
{JS}</body></html>"""


def tile(t, cls=""):
    return (f'<a class="tile {cls}" data-tag="{t["tag"]}" href="tools/{t["slug"]}.html"><div class="im"><img src="assets/{t["cover"]}" alt="{e(t["hook"])}" loading="lazy">'
            f'<span class="badge">{t["tag"]}</span></div><div class="tx"><h3>{e(t["hook"])}</h3>'
            + (f'<p>{e(t["lead"])}</p>' if cls == "feat" else "")
            + f'<div class="meta">{t["name"]} · {t["by"]} · ★ {t["stars"]}K · {fmt_date(t["date"])}</div></div></a>')


tags = ["All"] + sorted({t["tag"] for t in TOOLS})
stars = sum(t["stars"] for t in TOOLS)
home = f"""<section class="hero"><div class="orb"></div><div class="wrap">
<span class="eyebrow"><i></i>New tool every day</span>
<h1>Open-source AI tools, <em>explained in 60 seconds.</em></h1>
<p>We find the AI tools and agents worth your time, check them against the source, and show you how to use them. Free, no hype.</p>
<div class="btns"><a class="btn pri" href="#drops">Browse the tools</a><a class="btn" href="{IG}">Watch on Instagram</a></div>
<div class="proof"><div><b>{len(TOOLS)}</b>tools explained</div><div><b>{stars:.1f}K</b>GitHub stars covered</div><div><b>100%</b>open source</div><div><b>60 s</b>per video</div></div>
</div></section>
<main class="panel"><div class="wrap">
<section id="drops"><h2>Latest drops</h2><p class="sub">Every open-source AI tool we covered, checked against the source.</p>
<div class="tabs">{"".join(f'<button class="{"on" if x == "All" else ""}" data-f="{x}">{x}</button>' for x in tags)}</div>
<div class="drops">{tile(TOOLS[0], "feat")}<div class="side">{"".join(tile(t) for t in TOOLS[1:])}</div></div></section>
<section class="sec" id="how"><h2>How it works</h2><p class="sub">Three steps, every day.</p><div class="how">
<div class="step"><b>1</b><h3>We find it</h3><p>We track GitHub and the big AI labs for tools that actually do something new.</p></div>
<div class="step"><b>2</b><h3>We check it</h3><p>Every number comes from the official repo: stars, license, benchmarks, install steps.</p></div>
<div class="step"><b>3</b><h3>You try it</h3><p>A 60-second reel to see it, and a page here with the steps and the official link.</p></div></div></section>
<section class="sec" id="reels"><h2>Watch the reels</h2><p class="sub">Short, visual and made entirely with code.</p><div class="reels">
{"".join(f'<a class="reel" href="{u}"><img src="assets/{i}" alt="{e(c)}" loading="lazy"><span>{e(c)}</span></a>' for i, c, u in REELS)}</div></section>
<section class="sec" id="faq"><h2>Questions</h2><div class="faq">{"".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q, a in FAQ)}</div></section>
<section class="band"><h2>One new AI tool a day.</h2><p>Follow Agentic Insider and never be the last to know.</p>
<div class="btns" style="display:flex;justify-content:center;gap:12px;flex-wrap:wrap"><a class="btn pri" href="{IG}">Follow on Instagram</a><a class="btn" href="{FB}">Follow on Facebook</a></div></section>
</div></main>"""
org = {"@context": "https://schema.org", "@type": "Organization", "name": "Agentic Insider", "url": BASE + "/", "logo": BASE + "/assets/logo.png", "sameAs": [IG, FB]}
site = {"@context": "https://schema.org", "@type": "WebSite", "name": "Agentic Insider", "url": BASE + "/"}
faq = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in FAQ]}
Path("index.html").write_text(shell("Agentic Insider: open-source AI tools and agents, explained in 60 seconds",
                                    "The open-source AI tools and agents worth your time, checked against the source and explained in 60 seconds, with install steps and official links.",
                                    "", home, [org, site, faq]), encoding="utf-8")

for t in TOOLS:
    others = [o for o in TOOLS if o is not t]
    body = f"""<main class="panel" style="margin-top:24px"><div class="wrap"><div class="art"><article>
<div class="crumbs"><a href="../index.html">Home</a> / <a href="../index.html#drops">Tools</a> / {e(t["name"])}</div>
<h1>{e(t["hook"])}</h1><p class="lead">{e(t["lead"])}</p>
<img class="cover" src="../assets/{t["img"]}" alt="{e(t["hook"])}">
<h2>Why it matters</h2><ul>{"".join(f"<li>{e(f)}</li>" for f in t["facts"])}</ul>
<h2>How to try it</h2><ol>{"".join(f"<li>{s}</li>" for s in t["steps"])}</ol>
<h2>Official link</h2><p style="font-size:18px"><a style="color:var(--acc2);font-weight:600" href="{t["repo"]}" rel="nofollow">{t["repo"].replace("https://", "")}</a></p>
<h2>More tools</h2><div class="more">{"".join(tile(o).replace('href="tools/', 'href="').replace('src="assets/', 'src="../assets/') for o in others[:2])}</div>
</article><aside class="glance"><h4>At a glance</h4><dl><dt>Tool</dt><dd>{e(t["name"])}</dd><dt>By</dt><dd>{e(t["by"])}</dd>
<dt>Stars</dt><dd>★ {t["stars"]}K</dd><dt>License</dt><dd>{t["license"]}</dd><dt>Price</dt><dd>Free</dd><dt>Setup</dt><dd>{e(t["time"])}</dd>
<dt>Good for</dt><dd>{e(t["good"])}</dd><dt>You need</dt><dd>{e(t["needs"])}</dd></dl>
<a class="btn pri" href="{t["repo"]}" rel="nofollow">Open on GitHub</a><a class="btn ghost" style="width:100%;justify-content:center;margin-top:10px" href="{IG}">Get one tool a day</a></aside></div>
<section class="band"><h2>One new AI tool a day.</h2><p>Follow Agentic Insider and never be the last to know.</p><a class="btn pri" href="{IG}">Follow on Instagram</a></section>
</div></main>"""
    art = {"@context": "https://schema.org", "@type": "Article", "headline": t["hook"], "description": t["lead"], "datePublished": t["date"],
           "image": f"{BASE}/assets/{t['cover']}", "author": {"@type": "Organization", "name": "Agentic Insider", "url": BASE + "/"},
           "publisher": {"@type": "Organization", "name": "Agentic Insider", "logo": {"@type": "ImageObject", "url": BASE + "/assets/logo.png"}},
           "about": {"@type": "SoftwareApplication", "name": t["name"], "applicationCategory": "DeveloperApplication", "offers": {"@type": "Offer", "price": "0"}, "url": t["repo"]}}
    crumbs = {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Home", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": t["name"], "item": f"{BASE}/tools/{t['slug']}.html"}]}
    Path(f"tools/{t['slug']}.html").write_text(shell(f"{t['name']}: {t['hook']} | Agentic Insider", t["lead"], f"tools/{t['slug']}.html", body,
                                                     [art, crumbs], f"assets/{t['cover']}"), encoding="utf-8")

urls = [BASE + "/"] + [f"{BASE}/tools/{t['slug']}.html" for t in TOOLS]
Path("sitemap.xml").write_text('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
                               + "".join(f"<url><loc>{u}</loc><lastmod>{date.today()}</lastmod></url>\n" for u in urls) + "</urlset>\n", encoding="utf-8")
Path("robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {BASE}/sitemap.xml\n", encoding="utf-8")
Path(".nojekyll").write_text("")
print("built", len(TOOLS), "tool pages")

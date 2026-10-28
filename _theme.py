# Per-publisher announcement heroes for tool pages: each one uses the publisher's own official images and visual
# language (colours, type) from its repository, plus a clear "not affiliated" credit line.
THEMES = {
    "google-artemis": dict(font="Outfit:wght@200;300;600", css="""
.th { background: radial-gradient(ellipse at 20% 30%, #1b2233, #05070b 70%); color: #fff; font-family: Outfit, sans-serif; }
.th .ey { color: #9aa0a6; } .th .ey b { background: conic-gradient(#4285F4 0 25%, #EA4335 0 50%, #FBBC05 0 75%, #34A853 0); }
.th h1 { font-weight: 300; letter-spacing: -0.01em; } .th h1 em { font-style: normal; font-weight: 600; color: #8AB4F8; }
.th .bar { height: 4px; width: 160px; margin: 26px auto 0; border-radius: 2px; background: linear-gradient(90deg, #4285F4 25%, #EA4335 25% 50%, #FBBC05 50% 75%, #34A853 75%); }
.th .shots { grid-template-columns: 1fr 1.6fr; } .th .chip { border-color: #ffffff2a; background: #ffffff0d; }""",
        eyebrow="Google · Open source", title="ARTEMIS: an AI that uses <em>an Android phone like a human</em>",
        banner="official/artemis-banner.png", shots=["official/artemis-demo.jpg", "official/artemis-ui.jpg"],
        chips=["★ 14.8K on GitHub", "99%+ on AndroidWorld", "Apache 2.0"],
        credit="Images: google/artemis repository. Agentic Insider is not affiliated with Google."),
    "genoffice": dict(font="Plus+Jakarta+Sans:wght@500;700;800", css="""
.th { background: linear-gradient(160deg, #f7f8fc, #eef0fb 55%, #f6eefb); color: #0b0b12; font-family: "Plus Jakarta Sans", sans-serif; }
.th .ey { color: #5b5f73; } .th .ey b { background: #0b0b12; border-radius: 4px; }
.th h1 { font-weight: 800; letter-spacing: -0.035em; }
.th h1 em { font-style: normal; background: linear-gradient(90deg, #4f46e5, #c026d3); -webkit-background-clip: text; background-clip: text; color: transparent; }
.th .apps { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-top: 22px; }
.th .apps span { padding: 8px 14px; border-radius: 12px; background: #fff; box-shadow: 0 2px 10px #0000000f; font-weight: 700; font-size: 15px; }
.th .apps i { display: inline-block; width: 22px; height: 22px; border-radius: 6px; margin-right: 8px; vertical-align: -5px; }
.th .shots { grid-template-columns: 1fr 1fr; } .th .shots img, .th .ban { box-shadow: 0 30px 60px #1b1b4a26; border: 0; }
.th .chip { background: #fff; border-color: #e3e5ef; color: #2b2d3a; }""",
        eyebrow="Genspark · Open source", title="GenOffice: the open-source <em>AI Office suite</em>",
        banner="official/genoffice-hero.jpg", shots=["official/genoffice-docs.jpg", "official/genoffice-sheets.jpg"],
        apps=[("Docs", "#2b6cb0"), ("Sheets", "#2f855a"), ("Slides", "#c53030"), ("PDF", "#e53e3e"), ("Markdown", "#6b46c1"), ("HTML", "#dd6b20")],
        chips=["★ 10.8K on GitHub", "macOS · Windows · Linux", "Apache 2.0"],
        credit="Images: genspark-ai/genoffice repository. Agentic Insider is not affiliated with Genspark."),
    "img2threejs": dict(font="Space+Grotesk:wght@400;600;700&family=JetBrains+Mono:wght@500", css="""
.th { background: radial-gradient(ellipse at 80% 10%, #2a1f5c, #07070d 60%); color: #fff; font-family: "Space Grotesk", sans-serif; }
.th .ey { color: #a3a8c3; font-family: "JetBrains Mono", monospace; } .th .ey b { background: linear-gradient(135deg, #8b5cff, #38e8ff); }
.th h1 { font-weight: 700; letter-spacing: -0.03em; }
.th h1 em { font-style: normal; background: linear-gradient(90deg, #8b5cff, #38e8ff); -webkit-background-clip: text; background-clip: text; color: transparent; }
.th .logo { width: 84px; display: block; margin: 0 auto 18px; filter: drop-shadow(0 0 30px #8b5cff88); }
.th .shots { grid-template-columns: 1.4fr 0.6fr 1fr; align-items: center; }
.th .chip { font-family: "JetBrains Mono", monospace; border-color: #8b5cff55; background: #8b5cff14; }""",
        eyebrow="img2threejs · Open source", title="One photo in. <em>A procedural 3D model out.</em>",
        logo="official/img2threejs-logo.svg", banner="official/img2threejs-og.jpg",
        shots=["official/img2threejs-guitar.jpg", "official/img2threejs-cat.jpg", "official/img2threejs-game.jpg"],
        chips=["★ 19.2K on GitHub", "Three.js", "Apache 2.0"],
        credit="Images: img2threejs repository and showcase. Agentic Insider is not affiliated with the project."),
    "top-5-claude-plugins": dict(font="Inter:wght@600;800&family=JetBrains+Mono:wght@500;700", css="""
.th { background: radial-gradient(ellipse at 85% 0%, #1f2a3a, #0D1117 60%); color: #fff; font-family: Inter, sans-serif; }
.th .ey { color: #3FB950; font-family: "JetBrains Mono", monospace; } .th .ey b { background: #3FB950; }
.th h1 { font-weight: 800; letter-spacing: -0.03em; } .th h1 em { font-style: normal; color: #E3B341; }
.th .shots { grid-template-columns: repeat(5, 1fr); } .th .chip { font-family: "JetBrains Mono", monospace; border-color: #30363d; background: #161b22; }""",
        eyebrow="Trending on GitHub · October 2026", title="5 free Claude plugins that <em>replace apps you pay for</em>",
        banner=None, shots=[], chips=["★ 21.4K stars combined", "All MIT licensed", "One command each"],
        credit="Screenshots: each project's GitHub page. Agentic Insider is not affiliated with these projects."),
}
BASE_CSS = """
.th { position: relative; padding: 70px 0 80px; text-align: center; overflow: hidden; }
.th .ey { display: inline-flex; align-items: center; gap: 10px; font-size: 14px; font-weight: 600; letter-spacing: .14em; text-transform: uppercase; }
.th .ey b { width: 12px; height: 12px; border-radius: 50%; display: inline-block; }
.th h1 { margin: 20px auto 0; max-width: 980px; font-size: clamp(38px, 6.2vw, 74px); line-height: 1.02; }
.th .lead { margin: 22px auto 0; max-width: 680px; font-size: 19px; opacity: .85; }
.th .chips { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; margin-top: 24px; }
.th .chip { padding: 8px 15px; border-radius: 30px; border: 1px solid; font-size: 14px; font-weight: 600; }
.th .ban { width: 100%; max-width: 1100px; display: block; margin: 44px auto 0; border-radius: 20px; }
.th .shots { display: grid; gap: 18px; max-width: 1100px; margin: 22px auto 0; }
.th .shots img { width: 100%; border-radius: 16px; border: 1px solid #ffffff1c; display: block; }
.th .credit { margin-top: 22px; font-size: 13px; opacity: .6; }
@media (max-width: 760px) { .th .shots { grid-template-columns: 1fr !important; } }
"""


def hero(t, rel="../"):
    th = THEMES[t["slug"]]
    logo = f'<img class="logo" src="{rel}assets/{th["logo"]}" alt="{t["name"]} logo">' if th.get("logo") else ""
    apps = ('<div class="apps">' + "".join(f'<span><i style="background:{c}"></i>{a}</span>' for a, c in th["apps"]) + "</div>") if th.get("apps") else ""
    bar = '<div class="bar"></div>' if t["slug"] == "google-artemis" else ""
    shots = "".join(f'<img src="{rel}assets/{s}" alt="{t["name"]} official screenshot" loading="lazy">' for s in th["shots"])
    chips = "".join(f'<span class="chip">{c}</span>' for c in th["chips"])
    return (f'<section class="th"><div class="wrap">{logo}<span class="ey"><b></b>{th["eyebrow"]}</span><h1>{th["title"]}</h1>{bar}'
            f'<p class="lead">{t["lead"]}</p>{apps}<div class="chips">{chips}</div>'
            + (f'<img class="ban" src="{rel}assets/{th["banner"]}" alt="{t["name"]} official banner">' if th["banner"] else "") + f'<div class="shots">{shots}</div>'
            f'<p class="credit">{th["credit"]}</p></div></section>')

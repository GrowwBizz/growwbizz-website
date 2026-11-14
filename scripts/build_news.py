#!/usr/bin/env python3
"""Build news.html from news.json for the GrowwBizz website.

Usage: python3 scripts/build_news.py   (run from the repo root)

news.json is the single source of truth. The Android app can read the same
file from https://www.growwbizz.in/news.json.
Every item must link to an official government source (source_url).
"""
import html, json, sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OFFICIAL = (".gov.in", ".nic.in", "icai.org", "rbi.org.in", "sebi.gov.in")
CATS = ["GST", "Income Tax", "MCA / ROC", "MSME & Startup", "Other"]
MAX_ITEMS = 60

def esc(s):
    return html.escape(str(s or ""), quote=True)

def nice(d):
    return date.fromisoformat(d).strftime("%d %b %Y")

def check(items):
    seen = set()
    for it in items:
        for k in ("id", "date", "cat", "title", "summary", "source_name", "source_url"):
            if not it.get(k):
                sys.exit(f"news.json: item {it.get('id')} is missing '{k}'")
        host = it["source_url"].split("/")[2].lower()
        if not any(host.endswith(o) for o in OFFICIAL):
            sys.exit(f"news.json: {it['id']} source is not an official site: {host}")
        if it["cat"] not in CATS:
            sys.exit(f"news.json: {it['id']} has unknown category {it['cat']}")
        if it["id"] in seen:
            sys.exit(f"news.json: duplicate id {it['id']}")
        seen.add(it["id"])
        date.fromisoformat(it["date"])
        if it.get("deadline"):
            date.fromisoformat(it["deadline"])

def card(it):
    dl = ""
    if it.get("deadline"):
        dl = f'<span class="due" data-due="{esc(it["deadline"])}">Due {esc(nice(it["deadline"]))}</span>'
    who = f'<p class="meta"><b>Who it affects:</b> {esc(it["who"])}</p>' if it.get("who") else ""
    act = f'<p class="meta"><b>What to do:</b> {esc(it["action"])}</p>' if it.get("action") else ""
    ref = f' · {esc(it["ref"])}' if it.get("ref") else ""
    return (f'<article class="n" id="{esc(it["id"])}" data-cat="{esc(it["cat"])}">'
            f'<div class="top"><span class="kick">{esc(it["cat"])}</span>'
            f'<time datetime="{esc(it["date"])}">{esc(nice(it["date"]))}</time>{dl}</div>'
            f'<h2>{esc(it["title"])}</h2><p>{esc(it["summary"])}</p>{who}{act}'
            f'<p class="src">Official source: <a href="{esc(it["source_url"])}" target="_blank" rel="noopener">'
            f'{esc(it["source_name"])}</a>{ref}</p></article>')

CSS = """:root{--bg:#f7f3ea;--card:#fffdf8;--ink:#09252e;--ink2:#33494f;--muted:#5d6f72;--em:#0d604c;--gold:#b98a2e;--hair:#e4dccb;--wa:#1f9d55;--red:#b3261e}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.65 Manrope,system-ui,-apple-system,Segoe UI,sans-serif}
a{color:var(--em)}img{max-width:100%;height:auto}
.wrap{max-width:860px;margin:0 auto;padding:0 16px}
header{background:var(--card);border-bottom:1px solid var(--hair);position:sticky;top:0;z-index:5}
header .wrap{display:flex;align-items:center;justify-content:space-between;height:64px;gap:12px;max-width:1080px}
header nav a{font-weight:700;text-decoration:none;font-size:15px}
.crumbs{font-size:13px;color:var(--muted);padding:18px 0 0}.crumbs a{color:var(--muted)}
h1,h2{font-family:Fraunces,Georgia,serif;line-height:1.2;color:var(--ink)}
h1{font-size:clamp(30px,5vw,44px);margin:6px 0 10px}
h2{font-size:21px;margin:8px 0 8px}
.kick{color:var(--gold);font-weight:800;letter-spacing:.08em;text-transform:uppercase;font-size:12px}
.lead{font-size:17px;color:var(--ink2);margin:0}
.chips{display:flex;flex-wrap:wrap;gap:8px;margin:20px 0 18px}
.chips button{font:700 14px Manrope,system-ui,sans-serif;border:1.5px solid var(--em);background:var(--card);color:var(--em);border-radius:99px;padding:7px 14px;cursor:pointer}
.chips button[aria-pressed=true]{background:var(--em);color:#fff}
.n{background:var(--card);border:1px solid var(--hair);border-radius:18px;padding:20px;margin:0 0 14px}
.n .top{display:flex;flex-wrap:wrap;align-items:center;gap:10px;font-size:13px;color:var(--muted)}
.n p{margin:0 0 8px;color:var(--ink2)}.n .meta{font-size:15px}.n .meta b{color:var(--ink)}
.n .src{font-size:13px;color:var(--muted);margin:10px 0 0;padding-top:10px;border-top:1px solid var(--hair)}
.due{background:#fdecea;color:var(--red);font-weight:800;border-radius:99px;padding:2px 10px}
.due.past{background:#eee;color:var(--muted)}
.empty{display:none;color:var(--muted)}
.note{font-size:13px;color:var(--muted);margin:20px 0}
.cta{background:var(--em);color:#d9efe6;border-radius:18px;padding:20px;margin:24px 0}
.cta b{color:#fff;font-size:18px;display:block}.cta a{display:inline-block;margin-top:10px;background:var(--wa);color:#fff;font-weight:800;text-decoration:none;border-radius:12px;padding:11px 16px}
footer{background:var(--ink);color:#d9e4e1;margin-top:30px;padding:28px 0 40px;font-size:14px}footer a{color:#fff}footer .wrap{max-width:1080px}"""

JS = """(function(){var b=document.querySelectorAll('.chips button'),n=document.querySelectorAll('.n'),e=document.querySelector('.empty');
function show(c){var k=0;n.forEach(function(x){var on=c==='All'||x.dataset.cat===c;x.style.display=on?'':'none';if(on)k++});
b.forEach(function(x){x.setAttribute('aria-pressed',x.dataset.c===c)});e.style.display=k?'none':'block'}
b.forEach(function(x){x.addEventListener('click',function(){show(x.dataset.c)})});
var t=new Date();t.setHours(0,0,0,0);document.querySelectorAll('.due').forEach(function(d){var p=d.dataset.due.split('-'),
x=new Date(+p[0],p[1]-1,+p[2]),days=Math.round((x-t)/864e5);if(days<0){d.classList.add('past');d.textContent+=' (passed)'}
else if(days===0){d.textContent+=' (today)'}else if(days<=30){d.textContent+=' ('+days+(days===1?' day':' days')+' left)'}})})();"""

def build():
    data = json.loads((ROOT / "news.json").read_text(encoding="utf-8"))
    items = sorted(data["items"], key=lambda i: (i["date"], i["id"]), reverse=True)
    check(items)
    items = items[:MAX_ITEMS]
    cats = [c for c in CATS if any(i["cat"] == c for i in items)]
    chips = '<button type="button" data-c="All" aria-pressed="true">All</button>' + "".join(
        f'<button type="button" data-c="{esc(c)}" aria-pressed="false">{esc(c)}</button>' for c in cats)
    title = "Latest GST, Income Tax &amp; MCA News and Updates | GrowwBizz"
    desc = ("Daily GST, Income Tax, TDS, MCA/ROC and MSME updates in simple words, "
            "each linked to the official government notification or circular.")
    ld = {"@context": "https://schema.org", "@type": "CollectionPage", "name": "GrowwBizz News",
          "url": "https://www.growwbizz.in/news.html", "dateModified": data.get("updated", ""),
          "hasPart": [{"@type": "NewsArticle", "headline": i["title"], "datePublished": i["date"],
                       "url": f"https://www.growwbizz.in/news.html#{i['id']}",
                       "publisher": {"@type": "Organization", "name": "GrowwBizz"},
                       "isBasedOn": i["source_url"]} for i in items[:20]]}
    upd = nice(data["updated"]) if data.get("updated") else ""
    page = f"""<!doctype html>
<html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title><meta name="description" content="{desc}"><link rel="canonical" href="https://www.growwbizz.in/news.html">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}"><meta property="og:url" content="https://www.growwbizz.in/news.html"><meta property="og:image" content="https://www.growwbizz.in/logo-light.png">
<link rel="icon" type="image/png" href="favicon.png"><link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Fraunces:wght@600;700&family=Manrope:wght@500;700;800&display=swap">
<style>{CSS}</style>
<script type="application/ld+json">{json.dumps(ld, ensure_ascii=False)}</script></head><body>
<header><div class="wrap"><a href="/" aria-label="GrowwBizz home"><img src="logo-dark.png" alt="GrowwBizz" width="145" height="35"></a><nav><a href="tel:+919203601998">Call 92036 01998</a></nav></div></header>
<main class="wrap"><div class="crumbs"><a href="/">Home</a> › News</div>
<div style="padding:22px 0 0"><div class="kick">Updated {esc(upd)} · Official sources only</div><h1>GrowwBizz News</h1>
<p class="lead">GST, Income Tax, MCA and MSME updates that matter to your business, in plain words. Every update links to the official notification, circular or press release.</p></div>
<div class="chips" role="group" aria-label="Filter by topic">{chips}</div>
{''.join(card(i) for i in items)}
<p class="empty">No updates in this topic yet.</p>
<div class="cta"><b>Not sure how an update affects you?</b>Ask us on WhatsApp. No 100% advance on any service.<br><a href="https://wa.me/919203601998?text=Hi%20GrowwBizz%2C%20I%20have%20a%20question%20about%20a%20news%20update">WhatsApp 92036 01998</a></div>
<p class="note">These summaries are for general information. The official notification, circular or press release linked with each update is the authoritative text. Recommendations of the GST Council apply only after the government notifies them.</p>
</main>
<footer><div class="wrap"><p><b>GrowwBizz</b> · Serving clients across India.</p>
<p>WhatsApp and Call <a href="tel:+919203601998">92036 01998</a> · <a href="mailto:hello.growwbizz@gmail.com">hello.growwbizz@gmail.com</a> · <a href="guides.html">Guides</a> · <a href="privacy.html">Privacy Policy</a></p></div></footer>
<script>{JS}</script>
</body></html>
"""
    (ROOT / "news.html").write_text(page, encoding="utf-8")
    print(f"news.html built with {len(items)} items")

if __name__ == "__main__":
    build()

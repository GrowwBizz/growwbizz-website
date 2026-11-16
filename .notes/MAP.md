# GrowwBizz website, bot, Orders/Refer apps: where things live

PURPOSE: save Claude usage. SEARCH, DON'T READ: `grep -n "<name>" file`, then read only about 40 lines around the hit.
NEVER read whole: tpl.html (229 KB), body.html (217 KB), worker.js (238 KB), hi.json (110 KB), Code.gs (110 KB),
deploy/ or repo index.html (300 KB, generated), *.apk, *.zip, *.raw, *.pdf, test/index.html. No secrets belong in this file.
Line numbers below were checked on 2026-11-16 and drift: use the NAME, then grep.

## Where things are
- Live site: www.growwbizz.in = GitHub Pages, repo growwbizz/growwbizz-website, files at repo root. Commit straight to main.
- Website SOURCE is NOT in the repo: /mnt/project-files/website/source/ . The repo's index.html and the SEO pages are build output; never edit them by hand.
- Bot source: /mnt/project-files/whatsapp-bot/source/ ; Orders app: /mnt/project-files/orders/app/source/ ; Refer app: /mnt/project-files/apps-autoupdate/refer/ ; Android app: repo growwbizz/growwbizz-app (its own MAP.md).

## website/source files (what to open for what)
- data.js (51 KB, 303 lines) = ALL services and prices. `var CATS` (categories), `var DSC_ROW`, `var S = [` with one object per service: id, cat, name, short, mrp (struck price), price (our fee), plus, card, sub, get, steps, breakup (fee table), docs etc.
  Service ids: private-limited, llp, opc, startup-india, gst-registration, gst-filing, gst-ecommerce, gst-amendment, lut, llp-compliance, company-compliance, inc-20a, dir-kyc, other-roc, itr, tds-return, msme, iec, dsc, trademark, project-report. Category ids: start, gst, roc, tax, reg, brand, fin.
  Edit one service: `grep -n 'id: "gst-filing"' data.js` then read that block.
- tpl.html (2204 lines) = page layout + all site JS. `/*DATA*/` is replaced by data.js, `/*AMEND*/` by amend.js, `WA_ICON` by an svg. Parts:
  - lines 7-821 `<style>` CSS; 824-1017 header, mega menu, hero, sections (ids: promise, services, prices, tools, calendar, compare, how, refer, faq); 1018 contact; 1053 footer; 1063 cart sheet; 1068-2204 script.
  - Constants: `var BOT_WA` (WhatsApp number for every site link), `var STATES` (state, stamp duty), `var OPC_FEE`, then the line `var PRO = 899, DSC = 2000, NAME = 1000, PANTAN = 143, LLP_GOVT = 900, PRO_MRP = 4999, DSC_MRP = 2500` (calculator constants: keep equal to data.js).
  - `function offerName()` and `saveBand()` = monthly offer label (big festivals + New Year only, never Muslim festivals; other months "Limited time offer").
  - Calculator: `renderCalc`. Guided assistant: `startFlow`, `answer`, `finish`, `general`, `typed`. Due dates: `gstDues`, `dueRow`.
  - Cart and quote: `var ORDERS_URL` (Orders app endpoint, `track()` sends to it), `lineCost` (state-wise costing per service), `lineRows`, `addToCart`, `orderNow`, `renderCart`, `cartSums`, `quoteText` (copy text), `quotePdf` (PDF, strikethrough MRP + "You save" band), `askWho` (name+mobile before PDF).
- amend.js (109 lines) = GST amendment checker list (`var AM = [`). Also used to generate the app's assistant.js.
- seo_pages.py = the focus service pages (list `PAGES`), footer links `FOOT_LINKS`, `build()`, writes sitemap.xml + robots.txt. seo_articles.py = guides/blog (`ARTICLES`, `META`, `hub()`), seo_states.py = 38 state cost pages + hub, seo_tools.py = GST calculator page. They read prices from data.js, so price edits flow in on rebuild.
- build_site.py = THE build: `python3 build_site.py` -> /mnt/project-files/website/deploy/ (index.html + all pages + sitemap/robots) and growwbizz-website-upload.zip. NOTE its hard-coded `<title>`, meta description and `document.title` strings contain the GST 499 / Pvt Ltd 899 prices: update them on a price change.
- body.html, build.py, mkdeploy.py are OLD (body.html is only read for the WhatsApp svg). Do not use or read them.
- deploy/refer.html and deploy/privacy.html, plus the zip, are edited directly in deploy/ (not generated).

## Routine change recipes
1. PRICE CHANGE (any service): edit data.js (price, mrp, breakup, plus text, steps text if it names the price); if it is Pvt Ltd/LLP/OPC/DSC also the `var PRO = ...` line in tpl.html; grep old price in build_site.py title/description. Then:
   a) `python3 build_site.py`  b) copy deploy/*.html, sitemap.xml, robots.txt into the repo root (never delete repo-only files: news.html, news.json, scripts/, app-data.json, app-privacy.html, staff-b3368.../ ) and push to main
   c) bot: `node /mnt/project-files/whatsapp-bot/source/build.js` (reads data.js + tpl.html) then deploy worker.js
   d) app: regenerate app-data.json with the Android app's tools/gen-data.js, push to BOTH repos (see app MAP.md)
   e) Refer app prices: separate list (`['INC-20A Filing', 499]` in refer/Code.gs and `var SERVICES` in refer/Index.html). Orders app has no price list.
2. QUOTE/CART/OFFER label: tpl.html functions above (`lineCost`, `quotePdf`, `offerName`). The app has its own copies (see app MAP.md), keep both in sync.
3. WhatsApp number on site: `BOT_WA` and the `wa.me/919203601998` links in tpl.html and seo_*.py (`WA`, `PHONE`). Rule: site links open 9203601998 only.
4. NEWS: only the daily news task edits news.html, news.json, scripts/build_news.py (in the repo). `python3 scripts/build_news.py` from the repo root builds news.html from news.json. The header/footer "News" links come from tpl.html and seo_*.py (FOOT_LINKS in seo_pages.py).
5. NEW SEO PAGE/ARTICLE: add to PAGES (seo_pages.py) or ARTICLES (seo_articles.py), rebuild, copy as in 1b.

## WhatsApp bot (/mnt/project-files/whatsapp-bot/)
- source/bot-core.js (70 KB, `var BOT = (function () {`) = replies/logic; source/hi.json = Hindi (English text -> Hindi; build.js prints missing translations); source/config.json = phone shown, call hours, links; source/build.js = `node build.js` builds ../worker.js and ../test/index.html using the website's data.js/tpl.html (STATES, OPC_FEE, ORDERS_URL, DOCSBY) so a price change needs a bot rebuild.
- worker.js is OUTPUT: never hand-edit. Deployed to Cloudflare by API (see project memory growwbizz-bot-golive: deploy code only so secrets and cron stay).

## Orders & Queries app (/mnt/project-files/orders/app/)
- source/Code.src.gs (server; sections: intake_, quote*, chat*, followups_, `app_` for the Android app, appOrders_/appUpload_/appPaid_, adminDeliver) + source/Index.html (team page) -> `python3 source/build.py` builds one-file ../Code.gs. Edit the source files, never Code.gs.
- Delivered to Apps Script by the Drive auto-update folder (see apps-autoupdate/ and memory). Only push updates when the user asks for a change. Settings (team password, keys) sit at the top of Code.src.gs: never copy them anywhere.

## Refer & Earn app (/mnt/project-files/apps-autoupdate/refer/): Code.gs + Index.html + appsscript.json, same auto-update route.

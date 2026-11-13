#!/usr/bin/env python3
"""Static site generator for Sparked Live Network.

Zero dependencies, stdlib only — emits a complete static site into dist/:
creator landing page, apply page, privacy policy, terms, 404, sitemap, robots.

Launch gating
-------------
NETWORK_STATUS controls the claims the site makes:

  prelaunch (default) — we are an applicant to TikTok's LIVE Backstage network
                        program. Copy uses founding-creator/waitlist framing and
                        carries an explicit "not affiliated with TikTok" notice.
  live                — onboarding approved and contract accepted. Copy switches
                        to operating-network language and the partner notice.

Never set NETWORK_STATUS=live before LIVE Backstage approval: claiming an
affiliation we do not yet have would be inaccurate (TikTok Terms 3.2(c), 2.3(d)).
That rule is enforced below, not merely documented here — live mode also requires
BACKSTAGE_APPROVAL naming the approval, and falls back to prelaunch without it.

Optional env: GA4_MEASUREMENT_ID, SITE_DOMAIN (writes CNAME), APPLY_LINK,
BASE_PATH (URL prefix when served from a subpath, e.g. GitHub project pages).
"""

import html
import os
import shutil
from pathlib import Path
from interest_content import COPY, MARKETS, PHONE, WHATSAPP, TIKTOK_PROFILE, wa, interest_form, market_cards, country_body, international_body, shop_body

STATUS = os.environ.get("NETWORK_STATUS", "prelaunch").strip().lower()

# Live mode drops the "not affiliated with TikTok" notice from every page footer
# and asserts an operating TikTok LIVE Creator Network partnership. That is a
# claim about a signed relationship, so one switch must not be able to make it:
# live also requires BACKSTAGE_APPROVAL naming the approval (date, who granted
# it). Missing approval degrades to prelaunch — the truthful state — rather than
# publishing a partnership we cannot evidence. NETWORK_STATUS=live sat in this
# repo for 26 days in 2026-08 while the contract was still unaccepted; a comment
# saying "never do this" did not stop it, so the check now runs at build time.
BACKSTAGE_APPROVAL = os.environ.get("BACKSTAGE_APPROVAL", "").strip()
LIVE = STATUS == "live" and bool(BACKSTAGE_APPROVAL)
CLAIM_BLOCKED = STATUS == "live" and not BACKSTAGE_APPROVAL
DOMAIN = os.environ.get("SITE_DOMAIN", "").strip()
BASE_URL = ("https://" + DOMAIN) if DOMAIN else ""
# Serving from a subpath (GitHub project pages) breaks root-absolute links, so
# every internal href is built through u(). Empty for a custom domain at apex.
BASE_PATH = "/" + os.environ.get("BASE_PATH", "").strip().strip("/") \
    if os.environ.get("BASE_PATH", "").strip().strip("/") else ""


def u(path):
    """Internal URL: u('/apply/') -> '<base>/apply/'."""
    return BASE_PATH + path
GA4 = os.environ.get("GA4_MEASUREMENT_ID", "").strip()
# TikTok's own application link, from LIVE Backstage -> Creators -> Scout
# creators -> "Share application info". A creator who applies through this
# lands in Scout creators -> Creators and needs NO invitation code.
#
# ⚠ The `agency_scout_source` parameter on the resolved URL is ATTRIBUTION.
# This short link is the QR-code variant (agency_scout_source=qr_code_leads),
# so web traffic through it is reported as QR scans. Backstage's "Copy link"
# button yields a differently-tagged link — use that one here once captured,
# and keep this one for printed/QR use, or the source column lies.
APPLY_LINK = os.environ.get("APPLY_LINK", "").strip() or "https://www.tiktok.com/t/ZTAynpxHM/"

COMPANY = "Derek Coleman & Associates Inc., trading as Sparked Live Network"
EMAIL = "tiktok@dcassociatesgroup.com"
ADDRESS = "1800 JFK Blvd, Suite 300, PMB 92814, Philadelphia, PA 19103"
UPDATED = "November 12, 2026"

OUT = Path(__file__).parent / "dist"

CSS = """
:root{--bg:#ffffff;--fg:#14181d;--muted:#5b6570;--card:#f6f8fa;--accent:#e8355a;
--accent2:#00c2c7;--border:#e1e6eb;--ok:#0f9d58}
@media(prefers-color-scheme:dark){:root{--bg:#0d1116;--fg:#e9eef4;--muted:#96a3b0;
--card:#161c23;--accent:#ff5c7c;--accent2:#2ee6ea;--border:#252d36}}
*{box-sizing:border-box}
body{margin:0;font:16px/1.65 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,
Helvetica,Arial,sans-serif;background:var(--bg);color:var(--fg);
-webkit-font-smoothing:antialiased}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{max-width:940px;margin:0 auto;padding:0 20px}
header.site{border-bottom:1px solid var(--border);padding:16px 0;position:sticky;
top:0;background:var(--bg);z-index:10}
header.site .wrap{display:flex;justify-content:space-between;align-items:center;
gap:12px;flex-wrap:wrap}
.brand{font-weight:800;color:var(--fg);font-size:1.05rem;letter-spacing:-.01em}
.brand span{color:var(--accent)}
nav a{margin-left:20px;color:var(--muted);font-size:.94rem}
.hero{padding:64px 0 44px;border-bottom:1px solid var(--border)}
.badge{display:inline-block;font-size:.78rem;font-weight:700;letter-spacing:.04em;
text-transform:uppercase;color:var(--accent2);border:1px solid var(--accent2);
border-radius:99px;padding:4px 12px;margin-bottom:18px}
h1{font-size:2.6rem;line-height:1.12;margin:0 0 18px;letter-spacing:-.025em}
@media(max-width:640px){h1{font-size:1.95rem}.hero{padding:40px 0 32px}}
h2{font-size:1.45rem;margin:2.2em 0 .6em;letter-spacing:-.015em}
h3{font-size:1.05rem;margin:1.6em 0 .35em}
p.lede{color:var(--muted);font-size:1.16rem;max-width:44em;margin:0 0 26px}
.btn{display:inline-block;background:var(--accent);color:#fff;font-weight:700;
padding:13px 26px;border-radius:8px;margin:6px 10px 6px 0}
.btn:hover{opacity:.9;text-decoration:none}
.btn.alt{background:transparent;color:var(--fg);border:1px solid var(--border)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(260px,1fr));
gap:16px;margin:26px 0}
.card{background:var(--card);border:1px solid var(--border);border-radius:11px;
padding:20px}
.card h3{margin:0 0 7px;font-size:1.02rem}
.card p{margin:0;color:var(--muted);font-size:.95rem}
.big{font-size:2.1rem;font-weight:800;color:var(--accent);line-height:1;
margin:0 0 6px;letter-spacing:-.02em}
ul.check{list-style:none;padding:0;margin:14px 0}
ul.check li{padding:9px 0 9px 30px;position:relative;border-bottom:1px solid var(--border)}
ul.check li:before{content:"\\2713";position:absolute;left:4px;color:var(--ok);font-weight:700}
ul.no{list-style:none;padding:0;margin:14px 0}
ul.no li{padding:9px 0 9px 30px;position:relative;border-bottom:1px solid var(--border)}
ul.no li:before{content:"\\00D7";position:absolute;left:6px;color:var(--muted);
font-weight:700;font-size:1.15rem}
details{border-bottom:1px solid var(--border);padding:13px 0}
summary{cursor:pointer;font-weight:600}
details p{color:var(--muted);margin:9px 0 0}
.note{background:var(--card);border-left:3px solid var(--accent2);padding:14px 18px;
border-radius:0 8px 8px 0;margin:26px 0;color:var(--muted);font-size:.94rem}
form.apply{margin:24px 0}
form.apply .f{margin-bottom:18px}
form.apply label{display:block;font-weight:600;margin-bottom:6px}
form.apply .hint{display:block;font-weight:400;color:var(--muted);font-size:.88rem;
margin-top:2px}
form.apply input[type=text],form.apply input[type=email],form.apply input[type=tel],
form.apply input[type=url],form.apply select,form.apply textarea{width:100%;
padding:11px 13px;font:inherit;color:var(--fg);background:var(--bg);
border:1px solid var(--border);border-radius:8px}
form.apply textarea{min-height:110px;resize:vertical}
form.apply input:focus,form.apply select:focus,form.apply textarea:focus{outline:none;
border-color:var(--accent2);box-shadow:0 0 0 3px rgba(0,194,199,.18)}
form.apply .consent{display:flex;gap:10px;align-items:flex-start;
background:var(--card);padding:14px 16px;border-radius:8px}
form.apply .consent input{margin-top:4px;flex:none}
form.apply .consent label{font-weight:400;font-size:.93rem;margin:0}
form.apply button{background:var(--accent);color:#fff;font:inherit;font-weight:700;
padding:13px 26px;border:0;border-radius:999px;cursor:pointer}
form.apply button:hover{opacity:.9}
form.apply .hp{position:absolute;left:-9999px}
.req{color:var(--accent)}
/* Vertical phone capture — constrain by HEIGHT or it swallows a desktop page. */
figure.howto{margin:26px 0;text-align:center}
figure.howto video{display:block;margin:0 auto;max-height:74vh;max-width:100%;
width:auto;height:auto;border-radius:16px;border:1px solid var(--border);
background:#000}
figure.howto figcaption{color:var(--muted);font-size:.9rem;margin-top:12px}
ol.steps{counter-reset:s;list-style:none;padding:0;margin:18px 0}
ol.steps li{counter-increment:s;position:relative;padding:11px 0 11px 46px;
border-bottom:1px solid var(--border)}
ol.steps li:before{content:counter(s);position:absolute;left:0;top:11px;
width:28px;height:28px;border-radius:50%;background:var(--accent);color:#fff;
font-size:.85rem;font-weight:700;display:flex;align-items:center;
justify-content:center}
footer.site{border-top:1px solid var(--border);margin-top:60px;padding:30px 0 50px;
color:var(--muted);font-size:.89rem}
footer.site a{color:var(--muted)}
footer.site .fnav{margin-bottom:14px}
footer.site .fnav a{margin-right:18px}
.legal h2{font-size:1.15rem}
.legal p,.legal li{color:var(--muted)}
/* A clearer application hierarchy, with comfortable mobile targets. */
:root{--accent:#b92447;--accent2:#087b80}
@media(prefers-color-scheme:dark){:root{--accent:#ff8199;--accent2:#55dbe0}}
.wrap{max-width:1100px}
.brand{font-size:1.25rem;line-height:1.2;white-space:nowrap}
.brand small{display:block;font-size:.58rem;letter-spacing:.18em;margin-top:5px}
nav{display:flex;align-items:center;flex-wrap:wrap;gap:8px 20px}
nav a{margin:0;padding:8px 0;font-size:.9rem}
.nav-contact{font-weight:700;color:var(--fg)}
.hero{padding:68px 0 46px}
h1{font-size:clamp(2.2rem,5.4vw,4.2rem);max-width:17ch;letter-spacing:-.045em;line-height:1.07}
.hero .lede{max-width:47em;margin-top:22px}
.home-hero{display:grid;grid-template-columns:1.2fr 1fr;gap:44px;align-items:center}
.home-hero h1{max-width:13ch}
.home-hero .lede{font-size:1.1rem}
.coaching-panel{background:var(--card);border:1px solid var(--border);border-top:4px solid var(--accent);border-radius:14px;padding:26px}
.coaching-panel h2{margin:12px 0 20px;font-size:1.6rem;line-height:1.3}
.coaching-panel .steps{margin:0}.coaching-panel .steps li:last-child{border:0}
.eyebrow{font-size:.73rem;font-weight:750;letter-spacing:.12em;text-transform:uppercase;color:var(--muted)}
.btn,form.apply button{background:#b92447;color:white;border:1px solid transparent;border-radius:9px;line-height:1.4;min-height:46px;text-align:center}
.btn.alt{background:transparent;color:var(--fg);border-color:var(--border)}
.btn.whatsapp{background:#126847}
.fine{font-size:.83rem;color:var(--muted);max-width:76em}
.value-strip{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;padding:18px 0;border-bottom:1px solid var(--border)}
.value-strip strong,.value-strip span{display:block}.value-strip span{font-size:.9rem;color:var(--muted)}
.value-strip strong{font-size:1.12rem}
.card{padding:25px;border-radius:14px}.card .eyebrow{display:block;margin-bottom:15px}
.card h2{font-size:1.2rem;margin:0 0 12px}
.text-link{display:inline-block;font-weight:650;margin-top:16px;padding:6px 0}
.founder{border-left:4px solid var(--accent);padding:8px 26px;margin:52px 0;max-width:800px}
.founder h2{margin-top:10px}.founder p{max-width:64ch}
.market-list{border-top:1px solid var(--border);margin:22px 0 38px}
.market-link{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:23px 5px;border-bottom:1px solid var(--border);color:var(--fg)}
.market-link strong{font-size:1.3rem}.market-link small{display:block;color:var(--muted);font-size:.87rem}
.market-link:hover{color:var(--accent);text-decoration:none;background:var(--card)}
.closing{padding:26px;margin:48px 0 0;background:var(--card);border-radius:14px}.closing h2{margin:0 0 14px}
.application-route{margin-top:36px;padding:28px;border:1px solid var(--border);border-radius:14px}.application-route h2{margin-top:10px}
.interest-panel{scroll-margin-top:110px;margin-top:46px;max-width:820px;padding:28px;background:var(--card);border:1px solid var(--border);border-radius:14px}
.interest-panel h2{margin-top:0}.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:0 24px}
.hint{font-size:.87rem;color:var(--muted);display:block}
.message-review{border:1px solid var(--accent2);padding:18px;border-radius:10px;margin-top:24px;background:var(--bg)}
.message-review h3{margin-top:0}.message-review textarea{font-size:.9rem}
.country-nav{margin-top:38px;font-size:.87rem}
footer.site .fnav{display:flex;flex-wrap:wrap;gap:8px 18px}
footer.site .fnav a{margin-right:0}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:3px solid var(--accent2);outline-offset:4px}
.skip-link{position:absolute;top:-100px;left:15px;padding:12px;background:var(--bg);z-index:30}.skip-link:focus{top:10px}
main{overflow-wrap:anywhere}section[id],h2[id]{scroll-margin-top:120px}
[hidden]{display:none!important}
@media(max-width:800px){.home-hero{grid-template-columns:1fr;gap:20px}.coaching-panel{max-width:580px}.hero{padding-top:36px}.home-hero h1{max-width:none}header.site{position:relative}header.site .wrap{align-items:flex-start}nav{gap:4px 16px}.badge{font-size:.7rem}.value-strip{gap:12px}.value-strip strong{font-size:1rem}}
@media(max-width:520px){.form-grid{grid-template-columns:1fr}.wrap{padding:0 18px}.grid{grid-template-columns:1fr}.interest-panel,.application-route,.coaching-panel{padding:20px}.btn{display:block;margin-right:0}.value-strip{grid-template-columns:1fr;gap:0}.value-strip p{margin:9px 0}.value-strip strong{display:inline}.value-strip span{display:inline;margin-left:7px}.founder{padding-left:18px}form.apply button{width:100%}h1{max-width:none}.country-nav{display:block}.country-nav a{display:inline-block}.fnav{line-height:2.4}}
"""


def ga_snippet():
    if not GA4:
        return ""
    return (
        '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>'
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push"
        "(arguments);}gtag('js',new Date());gtag('config','%s');</script>" % (GA4, GA4)
    )


def page(slug, title, description, body, legal=False, lang="en", territory=False):
    """Render a localized page, keeping market status explicit in its footer."""
    c = COPY[lang]
    contact_url = html.escape(wa(MARKETS[slug]["message"])) if slug in MARKETS else html.escape(wa())
    canonical = BASE_URL + u("/" + (slug + "/" if slug else "")) if BASE_URL else ""
    canon_tag = '<link rel="canonical" href="%s">' % html.escape(canonical) if canonical else ""
    footer_notice = c["territory_notice"] if territory else DISCLAIMER
    doc = f"""<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)}</title><meta name="description" content="{html.escape(description)}">
{canon_tag}<meta property="og:title" content="{html.escape(title)}">
<meta property="og:description" content="{html.escape(description)}"><meta property="og:type" content="website">
<meta property="og:url" content="{html.escape(canonical)}">
<style>{CSS}</style>{ga_snippet()}</head><body>
<a class="skip-link" href="#main">{c['skip']}</a>
<header class="site"><div class="wrap"><a class="brand" href="{u('/')}">Sparked <span>Live</span><small>CREATOR NETWORK</small></a>
<nav aria-label="{c['home']}"><a href="{u('/apply/')}">{c['apply']}</a><a href="{u('/shop/')}">Shop</a><a href="{u('/international/')}">{c['international']}</a><a href="{u('/managers/')}">{c['managers']}</a><a class="nav-contact" href="{contact_url}" target="_blank" rel="noopener noreferrer">WhatsApp ↗</a><a class="nav-contact" href="{TIKTOK_PROFILE}" target="_blank" rel="noopener noreferrer" aria-label="TikTok @sparkedlive">TikTok ↗</a></nav></div></header>
<main id="main" class="wrap{' legal' if legal else ''}">{body}</main>
<footer class="site"><div class="wrap"><div class="fnav"><a href="{u('/')}">{c['home']}</a><a href="{u('/apply/')}">{c['apply']}</a><a href="{u('/international/')}">{c['international']}</a><a href="{u('/managers/')}">{c['managers']}</a><a href="{u('/privacy/')}">{c['privacy']}</a><a href="{u('/terms/')}">{c['terms']}</a></div>
<p><a href="{contact_url}" target="_blank" rel="noopener noreferrer">WhatsApp {PHONE}</a> · <a href="{TIKTOK_PROFILE}" target="_blank" rel="noopener noreferrer">TikTok @sparkedlive</a> · <a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p>&copy; 2026 {html.escape(COMPANY)} · {html.escape(ADDRESS)}</p><p>{footer_notice}</p><p>{c['footer_status']}</p>
</div></footer></body></html>"""
    d = OUT / slug if slug else OUT
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(doc, encoding="utf-8")
    return slug


# The affiliation notice is the single most important compliance string on the
# site. Pre-launch we are an independent applicant; only after LIVE Backstage
# approval may we describe ourselves as a partner network.
DISCLAIMER = (
    "Sparked Live Network is an independent talent network and is not "
    "affiliated with, endorsed by, or sponsored by TikTok. TikTok is a trademark "
    "of its respective owner."
) if not LIVE else (
    "Sparked Live Network is operating as a TikTok LIVE Creator Network partner "
    "in the United States only. This does not establish Shop or international approval. "
    "TikTok is a trademark of its respective owner."
)

def index_body():
    badge = "US LIVE creator applications open" if LIVE else "US LIVE founding-creator interest"
    status = "" if LIVE else '<div class="note">Our TikTok LIVE Backstage network application is in review. We are gathering interest while approval is pending.</div>'
    return f"""<section class="hero home-hero"><div><span class="badge">{badge}</span>
<h1>Your LIVE.<br>Your next level.</h1><p class="lede">Build a stream people come back for. Sparked connects creators with practical coaching, streaming support and a person to talk to.</p>
<a class="btn" href="{u('/apply/')}">Apply to join</a><a class="btn alt" href="{html.escape(wa())}" target="_blank" rel="noopener noreferrer">Talk to us on WhatsApp</a>
<p class="fine">US LIVE applications · International expressions of interest</p></div>
<aside class="coaching-panel"><p class="eyebrow">Coaching in practice</p><h2>A stronger stream starts with a plan.</h2><ol class="steps"><li><strong>Make your opening count.</strong><br>Give new viewers a reason to stay.</li><li><strong>Build a repeatable format.</strong><br>Find a schedule and structure that fit you.</li><li><strong>Review and improve.</strong><br>Turn your stream experience into a next step.</li></ol></aside></section>
{status}
<div class="value-strip"><p><strong>0% network cut</strong><span>of your LIVE gifts</span></p><p><strong>Practical support</strong><span>for your setup and stream</span></p><p><strong>Real conversations</strong><span>with the Sparked team</span></p></div>
<p class="fine">Sparked does not take a cut of creators’ LIVE gifts. TikTok’s own rewards rules, conversion, deductions and payout conditions still apply. Earnings are not guaranteed. Shop collaborations have separate terms.</p>
<h2 id="what-you-get">Support for the work behind the LIVE</h2>
<div class="grid"><article class="card"><span class="eyebrow">01 / Your stream</span><h3>Get comfortable on camera</h3><p>Work on your opening, stream format, audience interaction and schedule. Build habits you can maintain.</p></article><article class="card"><span class="eyebrow">02 / Your setup</span><h3>Make your setup work for you</h3><p>Get guidance on OBS, sound, lighting, overlays and computer streaming. TikTok controls access to features and stream keys.</p></article><article class="card"><span class="eyebrow">03 / Your community</span><h3>Find your people</h3><p>Discuss creator collaborations, LIVE matches and how to respond when a stream or account needs attention. Platform outcomes cannot be guaranteed.</p></article></div>
<section class="founder"><p class="eyebrow">Meet the founder</p><h2>Built from the viewer’s side of LIVE.</h2><p>Derek Coleman founded Sparked after spending time on TikTok LIVE as a gifter. That perspective shapes our approach: understand why people stay, help creators find a repeatable format, and make support easy to reach.</p><a href="https://www.tiktok.com/@sparkedlive" target="_blank" rel="noopener noreferrer">Meet Sparked on TikTok ↗</a></section>
<h2>Choose your next step</h2><div class="grid"><article class="card"><h3>US LIVE creators</h3><p>See the application steps and continue to TikTok’s official flow.</p><a class="text-link" href="{u('/apply/')}">Explore LIVE →</a></article><article class="card"><h3>Shop creators and partners</h3><p>Tell us about your product content and affiliate interests. Shop development is separate from LIVE enrollment.</p><a class="text-link" href="{u('/shop/')}">Discuss Shop →</a></article><article class="card"><h3>Managers and recruiters</h3><p>Share your creator experience, availability and proposed scope.</p><a class="text-link" href="{u('/managers/')}">Work with Sparked →</a></article></div>
<h2>Help shape our international expansion</h2><p>UK, Brazil and Mexico: expressions of interest only while local operations and program approvals are assessed.</p>{market_cards(u)}
<h2>Before you apply</h2><details><summary>Who can apply for US LIVE?</summary><p>Adults based in the US can discuss eligibility with us. Tell us if you already belong to another network. We confirm current TikTok criteria and any streaming expectations before onboarding.</p></details><details><summary>Does Sparked take a cut of my LIVE gifts?</summary><p>Sparked’s network cut is zero. This is separate from TikTok’s platform rules and payout calculations. It is not an earnings guarantee or a statement about Shop commission terms.</p></details><details><summary>Does registering interest sign me up?</summary><p>No. A WhatsApp conversation does not enroll you. US LIVE network invitations are accepted inside TikTok. Any work or commercial arrangement needs its own agreed terms.</p></details><details><summary>Can I leave a network?</summary><p>Ask us about the current release process and any applicable agreement before joining. TikTok’s current rules and your agreement govern the process.</p></details>
<section class="closing"><h2>Let’s talk about what you want to build.</h2><a class="btn" href="{u('/apply/')}">Find your application path</a><a class="btn alt" href="{html.escape(wa())}" target="_blank" rel="noopener noreferrer">Message Sparked</a></section>"""


def apply_body():
    us_action = (f'<a class="btn" href="{html.escape(APPLY_LINK)}" target="_blank" rel="noopener noreferrer">Apply on TikTok — US LIVE</a>' if LIVE else f'<p>Our network application is in review. <a href="{html.escape(wa())}">Discuss US LIVE interest on WhatsApp</a>.</p>')
    return f"""<section class="hero"><span class="badge">Find your path</span><h1>Start with your country.<br>Choose what you create.</h1><p class="lede">LIVE streaming and Shop are different opportunities. Choose the route that fits you so your inquiry reaches us with the right context.</p></section>
<section class="application-route" id="us-live"><p class="eyebrow">United States / LIVE</p><h2>Apply to the US LIVE network</h2><p>For creators aged 18 or older who live in the US. TikTok determines eligibility; tell us if you are already in another network.</p>{us_action}<a class="btn alt" href="{html.escape(wa('Hi Sparked Live, I have a question about the US LIVE application.'))}" target="_blank" rel="noopener noreferrer">Ask a question on WhatsApp</a>
<ol class="steps"><li><strong>Open the TikTok application.</strong> Use the account you create with. The shared application link identifies Sparked; no invitation code is needed for this route.</li><li><strong>We review eligibility and fit.</strong> Discuss your content, schedule and support needs with us.</li><li><strong>Accept an invitation inside TikTok.</strong> Applying alone does not enroll you, and we never need your password.</li></ol><p>Need help with the app? <a href="{u('/invitation-code/')}">View our application walkthrough</a>.</p></section>
<section id="international"><h2>Outside the US?</h2><p>Register interest in your local market. These pages do not enroll creators into the US network or promise a local launch.</p>{market_cards(u)}</section>
<div class="grid"><article class="card"><h2>Interested in Shop?</h2><p>Product videos, affiliate content and LIVE shopping have their own eligibility and commercial terms.</p><a class="text-link" href="{u('/shop/')}">Register Shop interest →</a></article><article class="card"><h2>Manager or recruiter?</h2><p>Tell us about your market, experience and availability.</p><a class="text-link" href="{u('/managers/')}">Discuss working with us →</a></article></div>
<div class="note">We do not charge a joining fee for the Sparked LIVE network and never ask for your password or verification codes. If an invitation looks suspicious, <a href="{html.escape(wa())}" target="_blank" rel="noopener noreferrer">ask us directly</a>.</div>"""


def invitation_code_body():
    return """
<h1>US LIVE application walkthrough</h1>
<div class="note">This walkthrough is for US LIVE creators. For UK, Brazil or Mexico, use our <a href="%(uinternational)s">international interest pages</a>. Shop has a separate inquiry route.</div>
<p class="lede">The quickest way in is our TikTok application link. Tap it, send
your details, and we take it from there &mdash; <strong>no invitation code
needed</strong>.</p>

<p><a class="btn" href="%(applylink)s" rel="noopener">Open the application on TikTok</a></p>

<figure class="howto" style="margin-top:18px">
<img src="%(qr)s" alt="QR code linking to the Sparked Live Network application on TikTok"
     width="240" height="240"
     style="width:240px;height:auto;border-radius:12px;border:1px solid var(--border);background:#fff;padding:10px">
<figcaption>On a second device? Scan this with your phone camera or the TikTok app.</figcaption>
</figure>

<div class="note">Applying through this link means TikTok already knows which
network you are applying to, so <strong>you can skip the invitation code
entirely</strong>. The rest of this page is only for people who did not use it.</div>

<h2>If you are applying without our link</h2>
<p>TikTok will ask you for a 6-character invitation code. Here is where to find
it &mdash; it takes about thirty seconds.</p>

<figure class="howto">
<video controls playsinline preload="none"
       poster="%(poster)s"
       aria-label="Screen recording showing where to find the invitation code in the TikTok app">
<source src="%(video)s" type="video/mp4">
<p>Your browser cannot play this video.
<a href="%(video)s">Download it instead</a>, or follow the written steps below.</p>
</video>
<figcaption>Recorded in the TikTok app. The code in the video is blurred on purpose.</figcaption>
</figure>

<h2>The same steps, written down</h2>
<ol class="steps">
<li>Open <strong>TikTok Studio</strong> and tap the <strong>LIVE</strong> tab.</li>
<li>Scroll down to <strong>Tools and resources</strong>.</li>
<li>Tap <strong>Join Creator Network</strong>.</li>
<li>Tap <strong>View how to join</strong>.</li>
<li>Under step 2, <em>Apply to join</em>, tap the <strong>invitation code</strong> link.</li>
<li>Your code appears &mdash; six characters, letters and numbers.</li>
<li>Tap <strong>Copy code</strong> and send it to us.</li>
</ol>

<div class="note"><strong>Your code expires after 24 hours.</strong> The screen
shows the exact time it runs out. Follow the expiry shown in your app. If yours has
lapsed, open the same screen again to check the available options.</div>

<h2>What the code does, and what it doesn't</h2>
<ul class="check">
<li>It lets us send you a Creator Network invitation through TikTok's own system</li>
<li>It is tied to your handle and expires on its own</li>
</ul>
<ul class="no">
<li>It does not give anyone access to your account</li>
<li>It does not sign you up for anything &mdash; you still have to accept the
invitation inside the TikTok app, and you can decline it</li>
</ul>

<div class="note"><strong>Nobody should ever ask you for your password.</strong>
Not us, not TikTok, not anyone claiming to work with either. The invitation code
is the only thing we need from you, and Sparked does not charge a LIVE joining fee or take a network cut of your LIVE gifts.</div>

<p><a class="btn" href="%(applylink)s" rel="noopener">Open the application on TikTok</a>
<a class="btn alt" href="%(uapply)s">What we look for</a></p>
""" % {"video": u("/assets/invitation-code-howto.mp4"),
       "poster": u("/assets/invitation-code-howto-poster.jpg"),
       "qr": u("/assets/apply-qr.png"),
       "applylink": html.escape(APPLY_LINK),
       "uapply": u("/apply/"), "uinternational": u("/international/")}


def managers_body():
    return f"""<section class="hero"><span class="badge">Managers &amp; recruiters</span><h1>Know creators?<br>Let’s build together.</h1><p class="lede">Tell us about the market you know, the creators you support and the work you want to do. We welcome proposals for a defined scope, availability and compensation.</p><a class="btn" href="#interest">Introduce yourself</a></section>
<div class="note">US LIVE opportunities and international planning are different stages. UK, Brazil and Mexico inquiries are exploratory, and Shop is a separate program. This page is not a job offer or a promise of paid work.</div>
<div class="grid"><article class="card"><h2>Local managers</h2><p>Coach creators, support their stream setup, plan schedules and follow through on questions. Show us relevant work and how you communicate.</p></article><article class="card"><h2>Recruiters</h2><p>Build real relationships with suitable creators and explain the opportunity accurately. We want thoughtful introductions, not bulk unsolicited messages.</p></article></div>
<h2>What to include</h2><ul class="check"><li>Your country and working languages</li><li>Experience with LIVE, Shop or both, with examples you have permission to share</li><li>Hours available each week and your proposed scope</li><li>Your proposed hourly, monthly or project rate and any commission expectations</li></ul>
<h2>Agree the work before it starts</h2><p>Scope, payment, responsibilities and any performance incentives must be agreed in writing before work begins. Your proposal does not commit either side. We do not ask candidates to pay a joining fee.</p>
<p>Prefer a local-language introduction? <a href="{u('/brazil/')}">Brasil — Português</a> · <a href="{u('/mexico/')}">México — Español</a> · <a href="{u('/uk/')}">UK — English</a></p>
{interest_form(u, managers=True)}"""


def privacy_body():
    return """
<h1>Privacy Policy</h1>
<p class="lede">Last updated %(updated)s</p>

<p>%(company)s ("we", "us") operates this site and a talent network for TikTok LIVE
creators. This policy explains what we collect and why. We keep it short because our
practice is genuinely simple.</p>

<h2>What we collect</h2>
<p><strong>Applicants and creators.</strong> When you apply, you give us your TikTok
handle, contact details, and information about your streaming activity. If you join our
roster we also keep the records needed to manage the relationship &mdash; performance
statistics made available to us through TikTok's LIVE Backstage system, and our
correspondence with you.</p>
<p><strong>If you connect your TikTok account to a tool we operate.</strong> Some of our
creator tools ask you to authorize access through TikTok's official login. In that case
we receive only the information covered by the permissions you approve &mdash; typically
your public profile and your own content statistics. We use it to show you and your
manager your own numbers. We do not access data belonging to people who have not
authorized us, and you can disconnect at any time from your TikTok settings, which
immediately ends our access.</p>
<p><strong>Visitors.</strong> Our hosting provider processes technical request information to serve this website. If analytics are enabled, they may process device and browsing information. Do not include personal or sensitive information in page URLs.</p>

<p><strong>WhatsApp inquiries, including international interest.</strong> Our message builder asks for your name, country, preferred language, role, program and optional TikTok handle, experience and availability. It creates a draft in your browser without saving it in browser storage or sending it to our application server. When you open WhatsApp, the draft text is passed to WhatsApp in the link; WhatsApp processes it under its own privacy policy. Sparked receives the message and your WhatsApp account contact information when you send it. We use those details to respond to your inquiry. This is not consent to bulk marketing or automated text messages.</p>
<p>WhatsApp is operated by Meta; see <a href="https://www.whatsapp.com/legal/privacy-policy">WhatsApp’s privacy policy</a>. TikTok and WhatsApp are separate services. We operate from the United States, so information you send may be processed in the US and other countries where our service providers operate. Please do not send identity documents, payment details, passwords or verification codes in an initial inquiry.</p>

<p><strong>If you tap &ldquo;Apply now&rdquo; on one of our TikTok videos.</strong> That
opens a form inside the TikTok app. We ask only for your <strong>name and email
address</strong> &mdash; we do not collect your phone number there, and we do not send
automated text messages. TikTok operates that form and holds your answers on its own
systems before passing them to us; TikTok's handling of it is governed by
<a href="https://www.tiktok.com/legal/privacy-policy">TikTok's privacy policy</a>, not
this one. We use what you send only to reply to you about joining the network.</p>

<p>Tapping that button does <strong>not</strong> apply you to the Creator Network and does
not sign you up to anything. A real Creator Network invitation only ever arrives through
TikTok's own LIVE Backstage system, inside the TikTok app, and you accept it there.</p>

<h2>What we do with it</h2>
<p>We use your information to evaluate applications, manage our roster, provide coaching
and support, advocate for you with TikTok when you ask us to, and meet our own legal and
tax obligations. We do not sell personal information. We do not share it with advertisers.
We share it only with TikTok where the relationship requires it, with service providers
who help us operate, and where the law requires.</p>

<h2>How long we keep it</h2>
<p>We keep applicant information only as long as needed to make and record a decision,
and creator information for the duration of the relationship plus the period our legal
and tax obligations require. Ask us to delete your information and we will, except where
we are legally required to keep it.</p>

<h2>Your choices</h2>
<p>Message us on <a href="https://wa.me/13053179940">WhatsApp at +1 305-317-9940</a> or email <a href="mailto:%(email)s">%(email)s</a> to see, correct, or delete the
information we hold about you, or to withdraw a permission you previously granted.
Depending on where you live, applicable privacy law may provide rights to access, correction, deletion, objection or withdrawal of consent. Contact us to make a request; we will respond as required by applicable law.</p>

<h2>Children</h2>
<p>Our network is for adults. We do not knowingly work with, or collect information from,
anyone under 18. If you believe a minor has given us information, contact us and we will
delete it.</p>

<h2>Changes and contact</h2>
<p>If we change this policy we will update the date above. Questions or requests:
<a href="mailto:%(email)s">%(email)s</a>, or %(company)s, %(addr)s.</p>
""" % {"updated": UPDATED, "company": COMPANY, "email": EMAIL,
       "addr": html.escape(ADDRESS), "umanagers": u("/managers/")}


def terms_body():
    return """
<h1>Terms of Use</h1>
<p class="lede">Last updated %(updated)s</p>

<h2>This site</h2>
<p>This website is operated by %(company)s. By using it you agree
to these terms. The content here is provided for information about our talent network.</p>

<h2>What this site is not</h2>
<p>Nothing on this site is an offer of employment, a guarantee of earnings, or a promise
of any particular result on TikTok or any other platform. Creator earnings depend on
factors outside our control, and outcomes such as account reinstatements, stream-key
grants, and content distribution are decided by TikTok, not by us. Any working
relationship between you and us is governed by the separate agreement we sign with you,
which prevails over anything stated here. UK, Brazil and Mexico pages collect expressions of interest only. LIVE and Shop participation must be confirmed separately; inquiries do not guarantee launch, acceptance, work or earnings.</p>

<h2>Independence</h2>
<p>%(disclaimer)s</p>

<h2>Applications</h2>
<p>Submitting an application does not create a relationship between us, and we may decline
any application. Information you give us must be accurate; we rely on it. Invitations to
join our roster are issued only through TikTok's official LIVE Backstage system.</p>

<h2>Intellectual property</h2>
<p>The text, design, and marks on this site belong to us, except third-party marks, which
belong to their owners and are referred to here for identification only.</p>

<h2>Liability</h2>
<p>This site is provided "as is." To the fullest extent the law allows, we are not liable
for indirect or consequential losses arising from your use of it.</p>

<h2>Governing law and contact</h2>
<p>These terms are governed by the laws of the State of Delaware. Questions:
<a href="mailto:%(email)s">%(email)s</a>.</p>
""" % {"updated": UPDATED, "company": COMPANY, "email": EMAIL, "disclaimer": DISCLAIMER}


def main():
    slugs = [
        page("", "Sparked Live — Creator Support, LIVE & International Opportunities",
             "Explore Sparked LIVE creator support, US applications, Shop inquiries and "
             "UK, Brazil and Mexico interest. Connect directly on WhatsApp.",
             index_body()),
        page("apply", "Apply — Sparked Live Network",
             "Apply to join Sparked Live Network. Two minutes, and a person reads every "
             "application.", apply_body()),
        page("invitation-code", "Apply on TikTok — Sparked Live Network",
             "Apply to Sparked Live Network through TikTok's own application link "
             "— no invitation code needed. Plus a thirty-second walkthrough showing "
             "where the invitation code lives if you need one.",
             invitation_code_body()),
        page("managers", "Work With Us — Talent Managers and Recruiters",
             "Connect with Sparked about local creator management and recruiting. "
             "Share your country, experience, availability and proposed rates.",
             managers_body()),
        page("privacy", "Privacy Policy — Sparked Live Network",
             "How Sparked Live collects, uses, and protects your "
             "information.", privacy_body(), legal=True),
        page("terms", "Terms of Use — Sparked Live Network",
             "Terms governing use of the Sparked Live Network website.",
             terms_body(), legal=True),
    ]

    slugs.extend([
        page("international", "International Creator Opportunities — Sparked Live", "Explore UK, Brazil and Mexico LIVE and Shop interest with Sparked. Regional approvals are pending confirmation.", international_body(u), territory=True),
        page("shop", "Shop Creator & Partner Interest — Sparked Live", "Discuss product content, affiliate and LIVE shopping interests with Sparked. Shop approval and terms must be confirmed separately.", shop_body(u), territory=True),
    ])
    for slug, market in MARKETS.items():
        slugs.append(page(slug, market["name"] + " — Sparked Live", market["lede"], country_body(slug, u), lang=market["lang"], territory=True))

    # Static assets (the how-to video and its poster). Copied rather than
    # generated, so the build stays reproducible from a clean checkout.
    src_assets = Path(__file__).parent / "assets"
    if src_assets.is_dir():
        shutil.copytree(src_assets, OUT / "assets", dirs_exist_ok=True)

    (OUT / "404.html").write_text(
        "<!doctype html><html lang=en><head><meta charset=utf-8>"
        "<title>Not found — Sparked Live Network</title><style>%s</style></head>"
        "<body><main class=wrap><h1>That page doesn't exist</h1>"
        "<p class=lede>Try the <a href='%s'>home page</a> or "
        "<a href='%s'>apply to join</a>.</p></main></body></html>"
        % (CSS, u("/"), u("/apply/")),
        encoding="utf-8")

    if BASE_URL:
        urls = "".join(
            "<url><loc>%s%s</loc></url>" % (BASE_URL, u("/" + (s + "/" if s else "")))
            for s in slugs)
        (OUT / "sitemap.xml").write_text(
            '<?xml version="1.0" encoding="UTF-8"?>'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>'
            % urls, encoding="utf-8")
        (OUT / "robots.txt").write_text(
            "User-agent: *\nAllow: /\nSitemap: %s/sitemap.xml\n" % BASE_URL,
            encoding="utf-8")
    else:
        (OUT / "robots.txt").write_text("User-agent: *\nAllow: /\n", encoding="utf-8")

    if DOMAIN:
        (OUT / "CNAME").write_text(DOMAIN + "\n", encoding="utf-8")

    (OUT / ".nojekyll").write_text("", encoding="utf-8")

    print("Built %d pages into %s (status=%s, domain=%s)"
          % (len(slugs), OUT, STATUS, DOMAIN or "-"))
    if CLAIM_BLOCKED:
        # ::warning:: is a GitHub Actions annotation, so this surfaces on the run
        # summary instead of scrolling past in the log.
        print("::warning title=Live claim blocked::NETWORK_STATUS=live but "
              "BACKSTAGE_APPROVAL is empty — built in prelaunch mode. Set "
              "BACKSTAGE_APPROVAL to the approval reference once LIVE Backstage "
              "onboarding is approved and the contract is accepted.")
    if not LIVE:
        print("NOTE: prelaunch mode — 'not affiliated with TikTok' notice is active.")


if __name__ == "__main__":
    main()

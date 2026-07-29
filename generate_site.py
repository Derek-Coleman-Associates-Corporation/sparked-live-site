#!/usr/bin/env python3
"""Static site generator for Sparked Live Network Inc.

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

Optional env: GA4_MEASUREMENT_ID, SITE_DOMAIN (writes CNAME), DISCORD_INVITE,
BASE_PATH (URL prefix when served from a subpath, e.g. GitHub project pages).
"""

import html
import os
import shutil
from pathlib import Path

STATUS = os.environ.get("NETWORK_STATUS", "prelaunch").strip().lower()
LIVE = STATUS == "live"
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
DISCORD = os.environ.get("DISCORD_INVITE", "").strip()
# POST target for the talent-manager form. GitHub Pages serves static files and
# cannot process a form, so submission needs a third-party endpoint (Formspree,
# Basin, Formsubmit) or our own function. Set FORM_ENDPOINT as a repo Actions
# variable. Left empty the page degrades to a mailto link — never to a form that
# silently drops what someone typed.
FORM_ENDPOINT = os.environ.get("FORM_ENDPOINT", "").strip()

# TikTok's own application link, from LIVE Backstage -> Creators -> Scout
# creators -> "Share application info". A creator who applies through this
# lands in Scout creators -> Creators and needs NO invitation code.
#
# ⚠ The `agency_scout_source` parameter on the resolved URL is ATTRIBUTION.
# This short link is the QR-code variant (agency_scout_source=qr_code_leads),
# so web traffic through it is reported as QR scans. Backstage's "Copy link"
# button yields a differently-tagged link — use that one here once captured,
# and keep this one for printed/QR use, or the source column lies.
APPLY_LINK = os.environ.get(
    "APPLY_LINK", "https://www.tiktok.com/t/ZTAynpxHM/").strip()

COMPANY = "Sparked Live Network Inc."
EMAIL = "tiktok@dcassociatesgroup.com"
ADDRESS = "1800 JFK Blvd, Suite 300, PMB 92814, Philadelphia, PA 19103"
UPDATED = "July 24, 2026"

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
"""


def ga_snippet():
    if not GA4:
        return ""
    return (
        '<script async src="https://www.googletagmanager.com/gtag/js?id=%s"></script>'
        "<script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push"
        "(arguments);}gtag('js',new Date());gtag('config','%s');</script>" % (GA4, GA4)
    )


def page(slug, title, description, body, legal=False):
    """Render one page into dist/<slug>/index.html (slug '' = site root)."""
    canonical = ("%s/%s" % (BASE_URL, slug + "/" if slug else "")) if BASE_URL else ""
    canon_tag = '<link rel="canonical" href="%s">' % canonical if canonical else ""
    doc = """<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%(title)s</title>
<meta name="description" content="%(desc)s">
%(canon)s
<meta property="og:title" content="%(title)s">
<meta property="og:description" content="%(desc)s">
<meta property="og:type" content="website">
<style>%(css)s</style>%(ga)s</head>
<body>
<header class="site"><div class="wrap">
<a class="brand" href="%(root)s">Sparked <span>Live</span> Network</a>
<nav><a href="%(root)s">Home</a><a href="%(uapply)s">Apply</a>
<a href="%(umanagers)s">Work with us</a><a href="mailto:%(email)s">Contact</a></nav>
</div></header>
<main class="wrap%(legalcls)s">
%(body)s
</main>
<footer class="site"><div class="wrap">
<div class="fnav"><a href="%(root)s">Home</a><a href="%(uapply)s">Apply</a>
<a href="%(umanagers)s">Work with us</a>
<a href="%(uprivacy)s">Privacy</a><a href="%(uterms)s">Terms</a>
<a href="mailto:%(email)s">%(email)s</a></div>
<p>&copy; 2026 %(company)s &middot; A Delaware corporation &middot; %(addr)s</p>
<p>%(disclaimer)s</p>
</div></footer>
</body></html>
""" % {
        "title": html.escape(title),
        "desc": html.escape(description),
        "canon": canon_tag,
        "css": CSS,
        "ga": ga_snippet(),
        "body": body,
        "email": EMAIL,
        "company": COMPANY,
        "addr": html.escape(ADDRESS),
        "legalcls": " legal" if legal else "",
        "disclaimer": DISCLAIMER,
        "root": u("/"),
        "uapply": u("/apply/"),
        "umanagers": u("/managers/"),
        "uprivacy": u("/privacy/"),
        "uterms": u("/terms/"),
    }
    d = OUT / slug if slug else OUT
    d.mkdir(parents=True, exist_ok=True)
    (d / "index.html").write_text(doc, encoding="utf-8")
    return slug


# The affiliation notice is the single most important compliance string on the
# site. Pre-launch we are an independent applicant; only after LIVE Backstage
# approval may we describe ourselves as a partner network.
DISCLAIMER = (
    "Sparked Live Network Inc. is an independent talent network and is not "
    "affiliated with, endorsed by, or sponsored by TikTok. TikTok is a trademark "
    "of its respective owner."
) if not LIVE else (
    "Sparked Live Network Inc. is an independent company operating as a TikTok "
    "LIVE Creator Network partner. TikTok is a trademark of its respective owner."
)

APPLY_HREF = DISCORD if DISCORD else ("mailto:%s?subject=Creator%%20Application" % EMAIL)


def index_body():
    if LIVE:
        badge = "Now accepting creators"
        h1 = "You keep 100% of your diamonds."
        lede = ("Sparked Live Network is a U.S. TikTok LIVE creator network built by a "
                "Top Gifter &mdash; we spent years on the <em>sending</em> side of the gift "
                "bar, so we know exactly what turns a stream into diamonds. "
                "No cut, no catch, no exceptions.")
    else:
        badge = "Founding creators &mdash; applications open"
        h1 = "We're building a network where you keep 100%."
        lede = ("Sparked Live Network is a U.S. talent network for TikTok LIVE creators, "
                "founded by a Top Gifter who spent years on the <em>sending</em> side of "
                "the gift bar. We're onboarding our founding creators now &mdash; get in "
                "before the roster fills.")

    prelaunch_note = "" if LIVE else (
        '<div class="note"><strong>Straight with you:</strong> our TikTok LIVE Backstage '
        'network application is in review. We are opening founding-creator applications '
        'now so we can onboard our first cohort the day we are approved. We will tell you '
        'exactly where that stands when you apply &mdash; no one gets a surprise.</div>')

    return """
<section class="hero">
<span class="badge">%(badge)s</span>
<h1>%(h1)s</h1>
<p class="lede">%(lede)s</p>
<a class="btn" href="%(apply)s">Apply to join</a>
<a class="btn alt" href="#what-you-get">See what you get</a>
</section>

%(prenote)s

<h2>Why a gifter, not a manager</h2>
<p>Every network says it helps you grow. Here is what is actually different about us:
our founder built his side of TikTok LIVE as a <strong>Top Gifter</strong>. We have
watched thousands of hours of LIVE from the viewer's seat and know, concretely, what
makes someone open their wallet at minute forty of a stream &mdash; and what makes them
close the app. That is the knowledge we hand our creators.</p>

<div class="grid">
<div class="card"><p class="big">0%%</p><h3>Our cut of your gifts</h3>
<p>Not a reduced cut. Not a tiered cut. Zero.</p></div>
<div class="card"><p class="big">100%%</p><h3>Yours to keep</h3>
<p>Every diamond you earn stays yours.</p></div>
<div class="card"><p class="big">1:1</p><h3>A real manager</h3>
<p>A dedicated person, not a Discord role.</p></div>
</div>

<p>TikTok pays us directly from its own network incentive pool, based on how our roster
performs overall. Our income depends entirely on helping you earn more. That is the only
alignment that makes sense &mdash; and it is why we can afford to never touch your gifts.</p>

<h2 id="what-you-get">What you get</h2>
<ul class="check">
<li><strong>Zero-cut earnings.</strong> $0 deducted from your gifts, ever. Your diamonds
are yours.</li>
<li><strong>Account protection.</strong> When a false strike or ban hits, a real person
works your case through our agency support channel. We file, escalate, and keep you
updated. <em>(Outcomes are TikTok's call; the advocacy is ours.)</em></li>
<li><strong>Computer streaming setup (Windows or Mac).</strong> Going live from a
computer instead of your phone gets you sharper video, on-screen alerts, and graphics.
We request a <em>stream key</em> on your behalf through our partner channel &mdash; that
is the code that lets your computer broadcast to TikTok &mdash; then set you up end to
end in <strong>OBS Studio (Open Broadcaster Software)</strong>, the free streaming
program most creators use, including overlays, alerts, and gift-triggered effects that
measurably lift gifting.</li>
<li><strong>PK battles and matchmaking.</strong> A <strong>PK battle</strong>
(&ldquo;PK&rdquo; is short for <em>player knockout</em>) is a head-to-head LIVE match
where you and another creator appear side by side and viewers send gifts to pick the
winner. We organize matches against partners at your level &mdash; the fastest way to
put your stream in front of an audience that has never seen you.</li>
<li><strong>1-on-1 growth coaching.</strong> Stream structure, hook timing, gift-goal
design, schedule strategy, and a monthly walk through your numbers.</li>
</ul>

<h2>What we ask</h2>
<p>We are selective, and we will tell you why. Under TikTok's network rules, a creator
only counts toward the incentives that pay us &mdash; and fund what we give back &mdash;
by showing up consistently. To stay active on our roster:</p>
<ul class="check">
<li><strong>7+ valid LIVE days per month</strong> (a valid day is 60+ continuous minutes)</li>
<li><strong>15+ total LIVE hours per month</strong></li>
<li>18 years or older, based in the United States</li>
<li>Not currently signed to another TikTok LIVE network</li>
</ul>
<p>Already streaming near that? You will do well here. Just starting out? Tell us
&mdash; we would rather build a ramp with you than set you up to miss a target.</p>

<h2>What we won't do</h2>
<ul class="no">
<li><strong>We won't lock you in.</strong> Under TikTok's own rules every creator may
leave their network at any time, for any reason. We will not make that awkward.</li>
<li><strong>We won't promise unbans, reach, or feature placement.</strong> Those are
TikTok's decisions. Anyone promising them is selling you something they do not control.</li>
<li><strong>We won't ask you for money.</strong> No fees, no subscriptions, no
"starter packages." If a network asks you to pay, walk away.</li>
</ul>

<h2>Questions</h2>
<details><summary>Do you really take nothing from my gifts?</summary>
<p>Correct &mdash; zero. TikTok compensates networks separately, out of its own incentive
pool, based on overall roster performance. We are never paid out of your diamonds.</p></details>
<details><summary>Can I leave if it is not working out?</summary>
<p>Yes, any time. That is your right under TikTok's rules, not a favor we grant.</p></details>
<details><summary>Will you get my account unbanned?</summary>
<p>We will file and escalate your case through our agency support channel and stay on it.
We cannot promise an outcome, because that decision belongs to TikTok. Any network telling
you otherwise is overselling.</p></details>
<details><summary>Can you get me a stream key so I can go LIVE from my computer?</summary>
<p>A stream key is the code that lets a computer broadcast to TikTok instead of streaming
from your phone. We can request one on your behalf through our partner channel, and we
will do the whole OBS Studio (Open Broadcaster Software) setup with you once it is
granted. TikTok grants keys at its own discretion &mdash; but the request coming from a
network carries further than one from an individual.</p></details>
<details><summary>What if I stream in a language other than English?</summary>
<p>Apply anyway and tell us. We are a U.S.-based roster, but we care about what you make,
not what language you make it in.</p></details>

<h2>Words you'll hear (and what they actually mean)</h2>
<p>New to LIVE? Nobody explains this stuff, so here it is in plain English.</p>
<div class="grid">
<div class="card"><h3>Diamonds</h3><p>What the gifts your viewers send convert into.
Diamonds are what you cash out &mdash; and 100%% of yours stay yours.</p></div>
<div class="card"><h3>PK battle</h3><p>Short for <em>player knockout</em>. A head-to-head
LIVE match: you and another creator side by side, viewers gifting to pick a winner.</p></div>
<div class="card"><h3>Stream key</h3><p>A code from TikTok that lets you broadcast from a
computer instead of your phone. TikTok grants these case by case.</p></div>
<div class="card"><h3>OBS Studio</h3><p>Open Broadcaster Software &mdash; the free
program most creators use to stream from a computer, with overlays and alerts.</p></div>
<div class="card"><h3>Overlay</h3><p>Graphics layered on your stream: gift alerts, goal
bars, top-gifter lists. They make viewers want to gift.</p></div>
<div class="card"><h3>Valid LIVE day</h3><p>TikTok only counts a day toward network
requirements if you streamed <strong>60+ continuous minutes</strong>.</p></div>
</div>

<h2>Ready?</h2>
<p>Applications are reviewed by a person, and you will get a real reply &mdash; not a
template. Never streamed from a computer, never done a PK battle? That is fine &mdash;
that is precisely what we are here to teach you.</p>
<a class="btn" href="%(apply)s">Apply to join</a>
""" % {"badge": badge, "h1": h1, "lede": lede, "prenote": prelaunch_note,
       "apply": html.escape(APPLY_HREF)}


def apply_body():
    channel = ('<p><a class="btn" href="%s">Join our Discord to apply</a></p>' % html.escape(DISCORD)
               if DISCORD else
               '<p><a class="btn" href="mailto:%s?subject=Creator%%20Application">'
               'Email your application</a></p>' % EMAIL)
    return """
<h1>Apply to Sparked Live</h1>
<p class="lede">Two minutes. A person reads every one of these.</p>
<p><a class="btn" href="%(applylink)s" rel="noopener">Apply on TikTok</a>
<a class="btn alt" href="%(uinvite)s">See how it works</a></p>
<p style="color:var(--muted);font-size:.94rem;margin-top:-2px">Goes straight to TikTok's own application form for our network. No invitation code needed.</p>
%(channel)s

<h2>Tell us this much</h2>
<ul class="check">
<li>Your TikTok handle</li>
<li>Roughly how many days and hours you go LIVE in a normal month</li>
<li>What you stream &mdash; gaming, music, just chatting, PK battles (head-to-head
matches against another creator), something else</li>
<li>Whether you are currently signed with another TikTok LIVE network</li>
<li>That you are 18 or older and based in the United States</li>
<li>The single thing you most want help with right now</li>
</ul>

<div class="note"><strong>Applying from outside our official TikTok account?</strong>
TikTok will ask you for a 6-character invitation code. It lives in the app and takes
about thirty seconds to find &mdash; <a href="%(uinvite)s">here is a video showing
exactly where</a>. It expires after 24 hours, so grab it when you are ready to send.</div>

<h2>What happens next</h2>
<p>We review your handle and recent LIVE activity, then reply either way &mdash; usually
within a few days. If we are a fit, you get an invitation through TikTok's official LIVE
Backstage system, which is the only way a creator can legitimately join a network. You
accept it from inside the TikTok app. Nobody will ever ask you for a password.</p>

<div class="note"><strong>Safety note.</strong> A real network never asks for your TikTok
password, never charges a joining fee, and never takes a cut of your diamonds. If anyone
claiming to be us does any of those things, they are not us &mdash; email
<a href="mailto:%(email)s">%(email)s</a> and tell us.</div>
""" % {"channel": channel, "email": EMAIL, "uinvite": u("/invitation-code/"),
       "applylink": html.escape(APPLY_LINK)}


def manager_form():
    """The talent-manager form, or an honest mailto fallback when unconfigured."""
    if not FORM_ENDPOINT:
        return ("""
<div class="note"><strong>The form is not live yet.</strong> Until it is, email
<a href="mailto:%(email)s?subject=Talent%%20Manager%%20Application">%(email)s</a>
with the details below and we will reply either way.</div>
<ul class="check">
<li>Your name, email, and TikTok handle</li>
<li>Whether you have managed or recruited creators before, and where</li>
<li>Roughly how many hours a week you can commit</li>
<li>The country and state you live in</li>
</ul>""" % {"email": EMAIL})

    return """
<form class="apply" action="%(endpoint)s" method="POST">
<div class="f"><label for="name">Full name <span class="req">*</span></label>
<input id="name" name="name" type="text" autocomplete="name" required></div>

<div class="f"><label for="email">Email address <span class="req">*</span>
<span class="hint">Where we reply. Check your spam folder if you don't hear back.</span>
</label><input id="email" name="email" type="email" autocomplete="email" required></div>

<div class="f"><label for="handle">Your TikTok username <span class="req">*</span>
<span class="hint">The @handle, for example @sparkedlive</span></label>
<input id="handle" name="tiktok_handle" type="text" placeholder="@" required></div>

<div class="f"><label for="country">Where do you live? <span class="req">*</span>
<span class="hint">TikTok requires managers and creators to be located in the
network's region, so we have to ask.</span></label>
<select id="country" name="country" required>
<option value="">Select&hellip;</option>
<option>United States</option>
<option>Other</option>
</select></div>

<div class="f"><label for="role">What are you interested in? <span class="req">*</span>
</label><select id="role" name="role" required>
<option value="">Select&hellip;</option>
<option>Talent manager &mdash; coaching and looking after a roster</option>
<option>Recruiter &mdash; finding and signing new creators</option>
<option>Both</option>
</select></div>

<div class="f"><label for="experience">Have you managed or recruited creators before?
<span class="hint">Tell us where and roughly how many. &ldquo;No, but here's why I'd be
good at it&rdquo; is a real answer &mdash; we read these.</span></label>
<textarea id="experience" name="experience"></textarea></div>

<div class="f"><label for="hours">Hours a week you can commit</label>
<input id="hours" name="hours_per_week" type="text"
placeholder="e.g. 10&ndash;15"></div>

<div class="f"><label for="phone">Phone number <span class="hint">Optional. Only used
if you ask us to call &mdash; we do not run automated texts.</span></label>
<input id="phone" name="phone" type="tel" autocomplete="tel"></div>

<div class="f"><label for="referrer">Referred by someone? Their TikTok username
<span class="hint">Optional.</span></label>
<input id="referrer" name="referred_by" type="text" placeholder="@"></div>

<div class="f hp" aria-hidden="true">
<label for="company_website">Leave this field empty</label>
<input id="company_website" name="company_website" type="text" tabindex="-1"
autocomplete="off"></div>

<div class="f consent">
<input id="consent" name="consent" type="checkbox" value="yes" required>
<label for="consent">I am 18 or older, and I agree that %(company)s may store and use
these details to consider my application, as described in the
<a href="%(uprivacy)s">Privacy Policy</a>. <span class="req">*</span></label></div>

<p><button type="submit">Send my details</button></p>
</form>""" % {"endpoint": html.escape(FORM_ENDPOINT), "company": COMPANY,
              "uprivacy": u("/privacy/")}


def invitation_code_body():
    return """
<h1>Apply to Sparked Live</h1>
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
shows the exact time it runs out. If yours has lapsed, just open the same screen
again and generate a new one &mdash; there is no limit and it costs you nothing.</div>

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
is the only thing we need from you, and a real network never charges a joining
fee or takes a cut of your diamonds.</div>

<p><a class="btn" href="%(applylink)s" rel="noopener">Open the application on TikTok</a>
<a class="btn alt" href="%(uapply)s">What we look for</a></p>
""" % {"video": u("/assets/invitation-code-howto.mp4"),
       "poster": u("/assets/invitation-code-howto-poster.jpg"),
       "qr": u("/assets/apply-qr.png"),
       "applylink": html.escape(APPLY_LINK),
       "uapply": u("/apply/")}


def managers_body():
    return """
<h1>Work with us</h1>
<p class="lede">We are looking for talent managers and recruiters &mdash; freelance,
paid on results, working the roster you build.</p>

%(form)s

<h2>What the work actually is</h2>
<p><strong>Talent manager.</strong> You look after a group of creators: help them build
a schedule they can keep, get them set up to stream from a computer, pair them for
head-to-head battles, and escalate problems &mdash; false strikes, bans, payment
questions &mdash; on their behalf. The job is mostly consistency and follow-through, not
sales.</p>
<p><strong>Recruiter.</strong> You find creators who would be better off with support
than without it, start a real conversation, and bring them in through TikTok's official
invitation system. No cold-spam, no scraping, no bought lists &mdash; those break
TikTok's rules and we will not run that way.</p>

<h2>How you get paid</h2>
<p>TikTok pays networks a monthly bonus based on how the roster performs. Managers earn
a share of the bonus their own creators generate &mdash; so your pay tracks how well the
people you look after actually do. We will give you the exact terms in writing before
you start.</p>
<div class="note"><strong>Creators keep one hundred percent of their diamonds.</strong>
Your pay never comes out of a creator's earnings, and neither does ours. If you have
worked somewhere that took a cut of gifts, this is not that.</div>

<h2>The honest version</h2>
<ul class="check">
<li>This is freelance, contractor work &mdash; not employment, no salary, no benefits</li>
<li>Pay is performance-based. A roster that does not stream earns nothing</li>
<li>We are a new network, so you would be building from a small base</li>
<li>You keep your own hours; nobody is tracking your screen</li>
</ul>
<ul class="no">
<li>We will not ask you to pay anything to join &mdash; ever, for any reason</li>
<li>We will not ask for your TikTok password, and neither should anyone else</li>
<li>We will not promise you a number we cannot back up</li>
</ul>

<h2>What we need from you</h2>
<ul class="check">
<li>18 or older, and legally able to work as a contractor where you live</li>
<li>Located in the region our network covers &mdash; TikTok enforces this, not us</li>
<li>Reachable. Creators ask questions at odd hours and notice when nobody answers</li>
<li>Straight with people. You will be the reason someone trusts us or doesn't</li>
</ul>

<div class="note"><strong>How the hiring works.</strong> You send the form, we reply
either way, and if it looks like a fit we talk. Anyone who takes on creators signs a
written agreement first &mdash; scope, pay, confidentiality, and how either side ends
it. Nothing starts on a handshake.</div>
""" % {"form": manager_form()}


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
<p><strong>Visitors.</strong> This site collects no personal information from ordinary
browsing. If site analytics are enabled, they measure aggregate traffic only.</p>

<p><strong>Talent manager and recruiter applicants.</strong> If you submit the form on
our <a href="%(umanagers)s">Work with us</a> page we collect your name, email address,
TikTok username, the country you live in, the role you are interested in, and anything
you choose to tell us about your experience and availability. A phone number and a
referrer's username are optional; we ask for a phone number only so we can call if you
want us to, and <strong>we do not send automated text messages</strong>. That form is
delivered by a third-party form service, which handles the message in transit on our
behalf and does not use it for its own purposes.</p>

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
<p>Email <a href="mailto:%(email)s">%(email)s</a> to see, correct, or delete the
information we hold about you, or to withdraw a permission you previously granted.
Depending on where you live you may have additional rights under laws such as the
California Consumer Privacy Act; we honor those requests regardless of where you live.</p>

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
<p>This website is operated by %(company)s, a Delaware corporation. By using it you agree
to these terms. The content here is provided for information about our talent network.</p>

<h2>What this site is not</h2>
<p>Nothing on this site is an offer of employment, a guarantee of earnings, or a promise
of any particular result on TikTok or any other platform. Creator earnings depend on
factors outside our control, and outcomes such as account reinstatements, stream-key
grants, and content distribution are decided by TikTok, not by us. Any working
relationship between you and us is governed by the separate agreement we sign with you,
which prevails over anything stated here.</p>

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
        page("", "Sparked Live Network — Keep 100% of Your TikTok LIVE Diamonds",
             "A U.S. TikTok LIVE creator network that takes zero percent of your gifts. "
             "Account protection, computer streaming setup, head-to-head battles, and "
             "one-on-one growth coaching.",
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
             "Freelance talent manager and recruiter roles at Sparked Live Network. "
             "Paid on roster performance, never out of a creator's diamonds.",
             managers_body()),
        page("privacy", "Privacy Policy — Sparked Live Network",
             "How Sparked Live Network Inc. collects, uses, and protects your "
             "information.", privacy_body(), legal=True),
        page("terms", "Terms of Use — Sparked Live Network",
             "Terms governing use of the Sparked Live Network website.",
             terms_body(), legal=True),
    ]

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
            "<url><loc>%s/%s</loc></url>" % (BASE_URL, s + "/" if s else "")
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
    if not LIVE:
        print("NOTE: prelaunch mode — 'not affiliated with TikTok' notice is active.")


if __name__ == "__main__":
    main()

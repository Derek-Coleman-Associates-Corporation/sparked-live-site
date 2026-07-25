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
<a href="mailto:%(email)s">Contact</a></nav>
</div></header>
<main class="wrap%(legalcls)s">
%(body)s
</main>
<footer class="site"><div class="wrap">
<div class="fnav"><a href="%(root)s">Home</a><a href="%(uapply)s">Apply</a>
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
<li><strong>PC and OBS streaming setup.</strong> We request stream-key access on your
behalf through our partner channel, then set you up end to end &mdash; OBS, overlays,
alerts, and gift-triggered interactions that measurably lift gifting.</li>
<li><strong>PK battles and matchmaking.</strong> Organized matches against partners at
your level &mdash; the fastest way to put your stream in front of a new audience.</li>
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
<details><summary>Can you get me a stream key so I can go LIVE from my PC?</summary>
<p>We can request stream-key access on your behalf through our partner channel, and we
will do the whole OBS setup with you once it is granted. TikTok grants keys at its own
discretion &mdash; but the request coming from a network carries further than one from an
individual.</p></details>
<details><summary>What if I stream in a language other than English?</summary>
<p>Apply anyway and tell us. We are a U.S.-based roster, but we care about what you make,
not what language you make it in.</p></details>

<h2>Ready?</h2>
<p>Applications are reviewed by a person, and you will get a real reply &mdash; not a
template.</p>
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
%(channel)s

<h2>Tell us this much</h2>
<ul class="check">
<li>Your TikTok handle</li>
<li>Roughly how many days and hours you go LIVE in a normal month</li>
<li>What you stream &mdash; gaming, music, chat, PK battles, something else</li>
<li>Whether you are currently signed with another TikTok LIVE network</li>
<li>That you are 18 or older and based in the United States</li>
<li>The single thing you most want help with right now</li>
</ul>

<h2>What happens next</h2>
<p>We review your handle and recent LIVE activity, then reply either way &mdash; usually
within a few days. If we are a fit, you get an invitation through TikTok's official LIVE
Backstage system, which is the only way a creator can legitimately join a network. You
accept it from inside the TikTok app. Nobody will ever ask you for a password.</p>

<div class="note"><strong>Safety note.</strong> A real network never asks for your TikTok
password, never charges a joining fee, and never takes a cut of your diamonds. If anyone
claiming to be us does any of those things, they are not us &mdash; email
<a href="mailto:%(email)s">%(email)s</a> and tell us.</div>
""" % {"channel": channel, "email": EMAIL}


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
""" % {"updated": UPDATED, "company": COMPANY, "email": EMAIL, "addr": html.escape(ADDRESS)}


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
             "Account protection, PC/OBS setup, PK battles, and 1-on-1 coaching.",
             index_body()),
        page("apply", "Apply — Sparked Live Network",
             "Apply to join Sparked Live Network. Two minutes, and a person reads every "
             "application.", apply_body()),
        page("privacy", "Privacy Policy — Sparked Live Network",
             "How Sparked Live Network Inc. collects, uses, and protects your "
             "information.", privacy_body(), legal=True),
        page("terms", "Terms of Use — Sparked Live Network",
             "Terms governing use of the Sparked Live Network website.",
             terms_body(), legal=True),
    ]

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

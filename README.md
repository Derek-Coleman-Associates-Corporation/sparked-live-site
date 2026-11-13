# Sparked Live Network — creator site

Public marketing + creator-recruitment site for **Derek Coleman & Associates Inc.,
trading as Sparked Live Network** (operator confirmed November 12, 2026).
Static, zero dependencies, deployed to GitHub Pages.

This repo is **public by design** and contains only marketing copy and legal pages.
Business records, contracts, and the confidential TikTok Fee Policy live in the
private `sparked-live-network` repo — never copy them here.

## Pages

| Path | Purpose |
|---|---|
| `/` | Creator landing page — value props, requirements, FAQ |
| `/apply/` | How to apply and what happens next |
| `/international/` | UK, Brazil and Mexico interest hub |
| `/uk/` | UK LIVE/Shop interest, English |
| `/brazil/` | Brazil LIVE/Shop interest, Portuguese |
| `/mexico/` | Mexico LIVE/Shop interest, Spanish |
| `/shop/` | Separate Shop creator/partner inquiry |
| `/managers/` | Manager/recruiter proposals and WhatsApp draft |
| `/invitation-code/` | Existing US LIVE TikTok application walkthrough |
| `/privacy/` | Privacy policy — **also the policy URL required by the TikTok developer app review** |
| `/terms/` | Terms of use |

## Build

```bash
python3 generate_site.py     # → dist/
```

Stdlib only, no pip installs. Deploys on every push to `main` via
`.github/workflows/pages.yml`.

## ⚠ Launch gating — read before changing NETWORK_STATUS

`NETWORK_STATUS` controls what the site claims:

- **`prelaunch`** (default) — founding-creator/waitlist framing, and every page
  carries *"not affiliated with, endorsed by, or sponsored by TikTok."* This is
  the correct and truthful state while our LIVE Backstage network application is
  in review.
- **`live`** — operating-network language and the partner notice.

**Do not set `live` until LIVE Backstage onboarding is approved and the contract
is accepted.** Claiming an affiliation we do not yet have would be inaccurate, and
the TikTok Creator Network Terms require information we provide to be accurate
(§3.2(c)) and prohibit misrepresenting affiliation (§2.3(d)).

Flip it by setting the repo Actions **variable** `NETWORK_STATUS=live`, then
re-running the workflow — no code change needed.

## Optional Actions variables

| Variable | Effect |
|---|---|
| `NETWORK_STATUS` | `prelaunch` (default) or `live` — see above |
| `SITE_DOMAIN` | Custom domain, e.g. `sparkedlive.com` — writes `CNAME`, canonicals, sitemap, robots |
| `BASE_PATH` | URL prefix when served from a subpath. Currently `sparked-live-site` for the project-pages URL. **Clear it when a custom domain is set**, or links will double up |
| `APPLY_LINK` | Optional official US TikTok application link; blank uses the existing Backstage link |
| `GA4_MEASUREMENT_ID` | Enables Google Analytics |

Without `SITE_DOMAIN` the site still works on the default `*.github.io` URL —
that URL is usable immediately for the TikFinity agency-registry website field
and the TikTok developer app's privacy-policy URL.

## Copy source

The landing copy derives from `recruitment/tikfinity-registry-profile.md` in the
private repo. Keep the two consistent: same claims, same guardrails. In
particular, TikTok-controlled outcomes (unbans, stream keys, feature placement)
are always described as advocacy we perform, never as results we guarantee.

## Contact and international boundaries

The approved public WhatsApp Business number is **+1 305-317-9940**. `interest_content.py`
owns the number, local copy and form rendering. `assets/interest.js` prepares a message
for the visitor to review, then offers an explicit WhatsApp link. The visitor sends it
in WhatsApp. The site does not send messages, save browser drafts, or POST these forms.
The number is user-provided; delivery/account registration is not tested by sending.

The previous email-required manager form is replaced by this visitor-controlled flow.
The existing external lead API is unchanged and is no longer used by these pages;
`FORM_ENDPOINT` and `DISCORD_INVITE` repo variables no longer affect the site.
No email address is required for a website WhatsApp inquiry. TikTok's own application
may have different fields, controlled by TikTok.

US `NETWORK_STATUS` / `BACKSTAGE_APPROVAL` flags never activate foreign markets or Shop.
Country and Shop pages remain expressions of interest; no local approval or launch
date is asserted. Country forms ask for actual residence (including an Other option).
Manager inquiries invite rates; they do not promise employment or authorize work.

Run `python3 test_launch_gating.py`, `python3 test_interest_flow.py` and
`node --check assets/interest.js` before release. Deployment also runs these checks.
Browser QA should verify empty-form validation, localized message contents, the
WhatsApp recipient and stale draft invalidation after editing; never send QA messages.

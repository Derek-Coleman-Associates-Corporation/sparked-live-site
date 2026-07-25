# Sparked Live Network — creator site

Public marketing + creator-recruitment site for **Sparked Live Network Inc.**
(Delaware C-Corporation). Static, zero dependencies, deployed to GitHub Pages.

This repo is **public by design** and contains only marketing copy and legal pages.
Business records, contracts, and the confidential TikTok Fee Policy live in the
private `sparked-live-network` repo — never copy them here.

## Pages

| Path | Purpose |
|---|---|
| `/` | Creator landing page — value props, requirements, FAQ |
| `/apply/` | How to apply and what happens next |
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
| `DISCORD_INVITE` | Makes the Apply buttons point at Discord instead of email |
| `GA4_MEASUREMENT_ID` | Enables Google Analytics |

Without `SITE_DOMAIN` the site still works on the default `*.github.io` URL —
that URL is usable immediately for the TikFinity agency-registry website field
and the TikTok developer app's privacy-policy URL.

## Copy source

The landing copy derives from `recruitment/tikfinity-registry-profile.md` in the
private repo. Keep the two consistent: same claims, same guardrails. In
particular, TikTok-controlled outcomes (unbans, stream keys, feature placement)
are always described as advocacy we perform, never as results we guarantee.

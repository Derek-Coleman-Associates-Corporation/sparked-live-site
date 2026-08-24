#!/usr/bin/env python3
"""Launch-gating tests — the site must not claim a TikTok partnership it lacks.

Runs generate_site.py in a subprocess per case (module-level env reads mean the
settings are fixed at import, so a fresh process is the only honest way to test
them) and asserts on the rendered HTML rather than on internal flags.

    python3 test_launch_gating.py
"""

import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).parent
GEN = HERE / "generate_site.py"

# The exact sentence live mode puts in every footer, and the one it replaces.
PARTNER_CLAIM = "operating as a TikTok LIVE Creator Network partner"
DISCLAIMER = "not affiliated with, endorsed by, or sponsored by TikTok"
IN_REVIEW = "network application is in review"

PAGES = ["index.html", "apply/index.html", "managers/index.html",
         "privacy/index.html", "terms/index.html"]


def build(**env):
    """Build into a throwaway dist and return {page: html} plus stdout."""
    tmp = Path(tempfile.mkdtemp())
    work = tmp / "site"
    # Copy the sources the generator needs; it always emits to <script>/dist.
    work.mkdir()
    (work / "generate_site.py").write_bytes(GEN.read_bytes())
    if (HERE / "assets").is_dir():
        subprocess.run(["cp", "-R", str(HERE / "assets"), str(work / "assets")],
                       check=True)
    full = {"PATH": "/usr/bin:/bin", "SITE_DOMAIN": "sparkedlive.com"}
    full.update({k: v for k, v in env.items() if v is not None})
    proc = subprocess.run([sys.executable, "generate_site.py"], cwd=work,
                          env=full, capture_output=True, text=True)
    assert proc.returncode == 0, f"generator failed:\n{proc.stderr}"
    out = {}
    for page in PAGES:
        p = work / "dist" / page
        if p.exists():
            out[page] = p.read_text(encoding="utf-8")
    return out, proc.stdout


def check(name, cond, detail=""):
    print(f"  {'PASS' if cond else 'FAIL'}  {name}")
    if not cond:
        print(f"        {detail}")
    return cond


def main():
    ok = True

    print("\ndefault (no env) is prelaunch")
    pages, _ = build()
    for page, html in pages.items():
        ok &= check(f"{page}: carries the disclaimer", DISCLAIMER in html)
        ok &= check(f"{page}: no partnership claim", PARTNER_CLAIM not in html)
    ok &= check("index: discloses the application is in review",
                IN_REVIEW in pages["index.html"])

    print("\nNETWORK_STATUS=live WITHOUT approval degrades to prelaunch")
    pages, stdout = build(NETWORK_STATUS="live")
    for page, html in pages.items():
        ok &= check(f"{page}: partnership claim blocked", PARTNER_CLAIM not in html,
                    "live copy shipped without a named approval")
        ok &= check(f"{page}: disclaimer retained", DISCLAIMER in html)
    ok &= check("build annotates the blocked claim",
                "Live claim blocked" in stdout, stdout)

    print("\nNETWORK_STATUS=live WITH approval renders live copy")
    pages, _ = build(NETWORK_STATUS="live",
                     BACKSTAGE_APPROVAL="2026-09-01 Backstage onboarding approved")
    ok &= check("index: partnership claim present",
                PARTNER_CLAIM in pages["index.html"])
    ok &= check("index: disclaimer removed", DISCLAIMER not in pages["index.html"])

    print("\napproval alone (still prelaunch) does not go live")
    pages, _ = build(BACKSTAGE_APPROVAL="2026-09-01 approved")
    ok &= check("index: stays prelaunch", DISCLAIMER in pages["index.html"])

    print("\n" + ("All launch-gating tests passed." if ok else "FAILURES above."))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())

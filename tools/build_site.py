#!/usr/bin/env python3
"""build_site.py — rebuild the shared chrome on every artistso.com page.

The site is hand-written static HTML with no framework and no dependencies, so
the "build" is deliberately small and non-destructive. For each page it:

  1. writes the head metadata every page should have — canonical URL,
     Open Graph + Twitter card tags, theme-color, and a real favicon
     (replacing the empty `data:,` icon);
  2. writes the accessibility floor — a skip link as the first focusable
     element, and `id="main-content"` on the one <main>;
  3. writes the shared nav chain from tools/pages.py, with exactly one
     aria-current="page" that points at the current page or its section;
  4. writes that page's organic nav style block (#nav-organic-KEY).

It touches nothing inside the page body except the skip link, the <main> id and
the nav element. Copy, prose, verbatim texts and all other links are left byte
for byte alone. Every write is idempotent: running it twice changes nothing.

    python3 tools/build_site.py           # apply
    python3 tools/build_site.py --check   # report drift, change nothing
    python3 tools/build_site.py --list    # list motifs and pages
"""

from __future__ import annotations

import argparse
import html as htmllib
import os
import re
import sys
from urllib.parse import quote

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages as manifest  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# ---------------------------------------------------------------------------
# theme colours (light-mode accents; the strip is drawn once, in SVG)
# ---------------------------------------------------------------------------
C = {
    "pink": "#db2777", "pink2": "#f472b6", "green": "#16a34a",
    "blue": "#1d4ed8", "cyan": "#0e7490", "purple": "#7c3aed",
    "orange": "#ea580c", "red": "#b91c1c", "gold": "#a16207",
    "amber": "#b45309", "teal": "#0c6b5e",
}

# ---------------------------------------------------------------------------
# motifs: (svg body, link border-radius, section label)
# One 120 x 16 strip of inline SVG, repeated every 120px. Styling only.
# ---------------------------------------------------------------------------
def _svg(body: str) -> str:
    raw = (
        "<svg xmlns='http://www.w3.org/2000/svg' width='120' height='16' "
        "viewBox='0 0 120 16'>" + body + "</svg>"
    )
    return quote(raw, safe="='/.,:-")


MOTIFS = {
    # ---------------------------------------------------------- main sections
    "vine": (_svg(
        f"<path d='M0 10 C 30 2, 60 16, 120 7' fill='none' stroke='{C['pink']}' stroke-width='1.6'/>"
        f"<ellipse cx='30' cy='5' rx='5' ry='2.4' fill='{C['green']}' opacity='.75' transform='rotate(-24 30 5)'/>"
        f"<ellipse cx='74' cy='11' rx='5' ry='2.4' fill='{C['pink']}' opacity='.55' transform='rotate(20 74 11)'/>"
        f"<ellipse cx='102' cy='6' rx='4' ry='2' fill='{C['green']}' opacity='.6' transform='rotate(-18 102 6)'/>"
    ), "16px 5px 16px 5px", "home"),

    "wave": (_svg(
        f"<path d='M0 8 Q 15 0, 30 8 T 60 8 T 90 8 T 120 8' fill='none' stroke='{C['blue']}' stroke-width='1.6'/>"
        f"<path d='M0 11 Q 15 5, 30 11 T 60 11 T 90 11 T 120 11' fill='none' stroke='{C['cyan']}' stroke-width='1' opacity='.55'/>"
    ), "999px", "physics"),

    "circuit": (_svg(
        f"<path d='M0 4 H28 V12 H64 V4 H92 V12 H120' fill='none' stroke='{C['green']}' stroke-width='1.6'/>"
        f"<circle cx='28' cy='4' r='2.1' fill='{C['green']}'/><circle cx='64' cy='12' r='2.1' fill='{C['teal']}'/>"
        f"<circle cx='92' cy='4' r='2.1' fill='{C['green']}'/>"
    ), "3px 10px 3px 10px", "apps"),

    "ribbon": (_svg(
        f"<path d='M0 6 C 30 14, 60 0, 120 10' fill='none' stroke='{C['purple']}' stroke-width='2'/>"
        f"<path d='M0 11 C 30 17, 60 5, 120 14' fill='none' stroke='{C['pink']}' stroke-width='1' opacity='.6'/>"
    ), "4px 16px 4px 16px", "story"),

    "contour": (_svg(
        f"<path d='M0 12 C 20 3, 38 3, 58 10 C 78 16, 96 5, 120 8' fill='none' stroke='{C['orange']}' stroke-width='1.6'/>"
        f"<path d='M0 15 C 24 8, 44 8, 64 13 C 84 17, 100 10, 120 12' fill='none' stroke='{C['red']}' stroke-width='1' opacity='.5'/>"
    ), "12px 12px 3px 3px", "work"),

    "survey": (_svg(
        f"<path d='M0 5 H120 M0 11 H120' stroke='{C['gold']}' stroke-width='1.2'/>"
        f"<path d='M10 5 V11 M40 5 V11 M70 5 V11 M100 5 V11' stroke='{C['gold']}' stroke-width='1.2'/>"
        f"<circle cx='55' cy='8' r='1.8' fill='{C['amber']}'/>"
    ), "2px", "ledger"),

    "mile": (_svg(
        f"<path d='M0 13 H120' stroke='{C['teal']}' stroke-width='1.4' stroke-dasharray='6 5'/>"
        f"<path d='M18 13 V6 M58 13 V6 M98 13 V6' stroke='{C['teal']}' stroke-width='1.4'/>"
        f"<circle cx='58' cy='4' r='2.6' fill='{C['amber']}'/><circle cx='98' cy='4' r='2.2' fill='{C['teal']}'/>"
    ), "999px 4px 999px 4px", "principalia"),

    # -------------------------------------------------------------- showcase
    "map": (_svg(
        f"<path d='M0 9 C 22 2, 40 15, 62 8 C 84 1, 100 13, 120 7' fill='none' stroke='{C['pink']}' stroke-width='1.4' stroke-dasharray='5 4'/>"
        f"<circle cx='22' cy='4' r='2' fill='{C['pink']}'/><circle cx='62' cy='8' r='2' fill='{C['amber']}'/>"
        f"<circle cx='100' cy='10' r='2' fill='{C['pink']}'/>"
    ), "10px 10px 2px 10px", "projects"),

    "gallery": (_svg(
        f"<rect x='6' y='4' width='20' height='9' rx='1.5' fill='none' stroke='{C['pink']}' stroke-width='1.3'/>"
        f"<rect x='36' y='3' width='22' height='11' rx='1.5' fill='none' stroke='{C['pink2']}' stroke-width='1.3'/>"
        f"<rect x='68' y='5' width='18' height='8' rx='1.5' fill='none' stroke='{C['pink']}' stroke-width='1.3'/>"
        f"<rect x='96' y='3' width='20' height='11' rx='1.5' fill='none' stroke='{C['pink2']}' stroke-width='1.3'/>"
    ), "3px", "artwork"),

    "chapter": (_svg(
        f"<path d='M14 13 V4 H42 V13' fill='none' stroke='{C['pink']}' stroke-width='1.5'/>"
        f"<path d='M20 4 V13 M36 4 V13' fill='none' stroke='{C['pink']}' stroke-width='1' opacity='.55'/>"
        f"<path d='M56 13 H112' stroke='{C['pink2']}' stroke-width='1.3'/>"
        f"<path d='M96 10 L100 13 L96 16' fill='none' stroke='{C['pink2']}' stroke-width='1.3'/>"
    ), "2px 12px 2px 12px", "pie"),

    "seal": (_svg(
        f"<circle cx='24' cy='8' r='5' fill='none' stroke='{C['pink']}' stroke-width='1.5'/>"
        f"<circle cx='24' cy='8' r='1.6' fill='{C['pink']}'/>"
        f"<path d='M40 8 H120' stroke='{C['pink2']}' stroke-width='1.2' stroke-dasharray='3 4'/>"
    ), "2px 14px 14px 2px", "letter"),

    "shelf": (_svg(
        f"<path d='M0 12 H120' stroke='{C['pink']}' stroke-width='1.5'/>"
        f"<path d='M12 12 V6 M26 12 V4 M40 12 V7' stroke='{C['pink2']}' stroke-width='1.4'/>"
        f"<path d='M66 12 V5 M82 12 V5' stroke='{C['pink2']}' stroke-width='1.4'/>"
        f"<path d='M66 5 H82' stroke='{C['pink']}' stroke-width='1.4'/>"
        f"<circle cx='104' cy='8' r='2.4' fill='{C['pink']}'/>"
    ), "4px 4px 14px 14px", "shop"),

    # ---------------------------------------------------------------- social
    "gather": (_svg(
        f"<path d='M4 13 C 24 13, 36 4, 60 8' fill='none' stroke='{C['pink2']}' stroke-width='1.2'/>"
        f"<path d='M116 13 C 96 13, 84 4, 60 8' fill='none' stroke='{C['pink2']}' stroke-width='1.2'/>"
        f"<circle cx='60' cy='8' r='3' fill='{C['pink']}'/>"
        f"<circle cx='20' cy='10' r='2' fill='{C['pink']}' opacity='.7'/>"
        f"<circle cx='100' cy='10' r='2' fill='{C['pink']}' opacity='.7'/>"
    ), "999px", "social"),

    "gate": (_svg(
        f"<path d='M30 14 V5 H90 V14' fill='none' stroke='{C['pink']}' stroke-width='1.5'/>"
        f"<path d='M30 8 H90' stroke='{C['pink2']}' stroke-width='1' opacity='.7'/>"
        f"<path d='M0 14 H120' stroke='{C['pink2']}' stroke-width='1.2' opacity='.5'/>"
    ), "14px 14px 2px 2px", "gsite"),

    # ------------------------------------------------------------ utilities
    "cycle": (_svg(
        f"<path d='M6 13 H114' stroke='{C['pink2']}' stroke-width='1' stroke-dasharray='2 3'/>"
        f"<path d='M14 13 V9 M30 13 V9 M46 13 V9 M62 13 V9 M78 13 V9 M94 13 V9 M110 13 V9' stroke='{C['pink2']}' stroke-width='1.3'/>"
        f"<circle cx='62' cy='6' r='2.6' fill='{C['pink']}'/>"
    ), "3px 3px 3px 3px", "calendar"),

    "fork": (_svg(
        f"<path d='M12 13 V8 H50 V3' fill='none' stroke='{C['pink']}' stroke-width='1.5'/>"
        f"<path d='M12 8 H50 V13' fill='none' stroke='{C['pink2']}' stroke-width='1.3'/>"
        f"<circle cx='50' cy='3' r='2.2' fill='{C['pink']}'/><circle cx='50' cy='13' r='2.2' fill='{C['pink2']}'/>"
        f"<path d='M62 8 H116' stroke='{C['pink2']}' stroke-width='1.2' stroke-dasharray='4 4'/>"
    ), "3px 10px 3px 10px", "github"),

    "stack": (_svg(
        f"<rect x='10' y='4' width='34' height='9' rx='1' fill='none' stroke='{C['pink']}' stroke-width='1.3'/>"
        f"<rect x='16' y='7' width='34' height='9' rx='1' fill='none' stroke='{C['pink2']}' stroke-width='1.3'/>"
        f"<rect x='22' y='10' width='34' height='5' rx='1' fill='none' stroke='{C['pink']}' stroke-width='1.3'/>"
        f"<path d='M70 8 H116' stroke='{C['pink2']}' stroke-width='1.2' stroke-dasharray='3 4'/>"
    ), "2px 8px 8px 2px", "docs"),

    "lamp": (_svg(
        f"<circle cx='60' cy='9' r='3.4' fill='none' stroke='{C['pink']}' stroke-width='1.5'/>"
        f"<path d='M60 2 V0 M60 18 V16 M53 9 H51 M69 9 H67 M55 4 L54 3 M65 4 L66 3 M55 14 L54 15 M65 14 L66 15' stroke='{C['pink2']}' stroke-width='1.3'/>"
        f"<path d='M0 9 H44 M76 9 H120' stroke='{C['pink2']}' stroke-width='1' opacity='.35'/>"
    ), "999px 999px 4px 4px", "notebooks"),

    "reel": (_svg(
        f"<rect x='8' y='4' width='104' height='9' rx='1' fill='none' stroke='{C['pink']}' stroke-width='1.3'/>"
        f"<path d='M18 4 V13 M34 4 V13 M50 4 V13 M66 4 V13 M82 4 V13 M98 4 V13' stroke='{C['pink2']}' stroke-width='1' opacity='.6'/>"
        f"<path d='M8 8.5 H112' stroke='{C['pink2']}' stroke-width='1' opacity='.45'/>"
    ), "2px", "reviews"),

    "note": (_svg(
        f"<path d='M20 11 V4 C 26 3, 32 5, 34 7' fill='none' stroke='{C['pink']}' stroke-width='1.5'/>"
        f"<circle cx='17' cy='11' r='3' fill='{C['pink']}'/>"
        f"<path d='M48 6 H58 M48 10 H58' stroke='{C['pink2']}' stroke-width='1.2' opacity='.7'/>"
        f"<path d='M70 4 H112' stroke='{C['pink']}' stroke-width='1.4'/>"
        f"<path d='M70 9 H100' stroke='{C['pink2']}' stroke-width='1.2' opacity='.6'/>"
    ), "3px 12px 3px 12px", "muse-meta"),

    "index": (_svg(
        f"<rect x='8' y='3' width='24' height='11' rx='1.5' fill='none' stroke='{C['pink2']}' stroke-width='1.3'/>"
        f"<path d='M14 3 V1.5 M26 3 V1.5' stroke='{C['pink']}' stroke-width='1.4'/>"
        f"<path d='M40 5 H56 M40 9 H64' stroke='{C['pink2']}' stroke-width='1.1' opacity='.7'/>"
        f"<path d='M76 4 H116 M76 8 H108 M76 12 H96' stroke='{C['pink']}' stroke-width='1.1' opacity='.55'/>"
    ), "2px 2px 8px 2px", "wiki"),

    "thread": (_svg(
        f"<path d='M10 3 H46 V11 H26 L20 14 V11 H10 Z' fill='none' stroke='{C['pink']}' stroke-width='1.3' stroke-linejoin='round'/>"
        f"<path d='M18 7 H38' stroke='{C['pink2']}' stroke-width='1.1'/>"
        f"<path d='M66 5 H104 V12 H84 L78 15 V12 H66 Z' fill='none' stroke='{C['pink2']}' stroke-width='1.2' stroke-linejoin='round'/>"
    ), "8px 8px 8px 2px", "forum"),
}

# ---------------------------------------------------------------------------
# theme metadata
# ---------------------------------------------------------------------------
THEME_BG = {
    "pink": ("#fff5f8", "#170d12"), "blue": ("#f3f7ff", "#0c1220"),
    "green": ("#f2faf3", "#0b1610"), "yellow": ("#fffbeb", "#171106"),
    "purple": ("#f7f4ff", "#130d20"), "orange": ("#fff7ed", "#1a0f06"),
    "red": ("#fff5f5", "#1a0b0b"), "teal": ("#edf6f3", "#07120f"),
}

FAVICON_SVG = (
    "<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'>"
    "<rect width='64' height='64' rx='14' fill='#db2777'/>"
    "<circle cx='28' cy='32' r='13' fill='none' stroke='#fff' stroke-width='6'/>"
    "<circle cx='48' cy='42' r='5' fill='#fff'/>"
    "</svg>"
)
# the pink "o" of artistso + its dot, as a tiny vector favicon
FAVICON = "data:image/svg+xml," + quote(FAVICON_SVG, safe="='/.,:-")

SKIP_LINK = (
    '<a class="skip" href="#main-content">Skip to content</a>\n    '
)

CHROME_CSS = """<style id="chrome-a11y">
/* Skip link + focus ring. Written by tools/build_site.py — do not hand-edit. */
.skip{position:absolute;left:-9999px;top:0;z-index:100;background:var(--accent);color:#fff;padding:10px 16px;font-family:"IBM Plex Mono",ui-monospace,monospace;font-size:13px;border-radius:0 0 6px 0;text-decoration:none;}
.skip:focus{left:0;}
a:focus-visible,button:focus-visible,summary:focus-visible{outline:2px solid var(--accent);outline-offset:2px;}
@media (prefers-reduced-motion:reduce){html{scroll-behavior:auto;}}
</style>"""

# ---------------------------------------------------------------------------
# what the build owns. Each pattern matches a whole line (leading indentation
# included) so re-running the build changes nothing.
# ---------------------------------------------------------------------------
HEAD_START = "<!-- build:head — written by tools/build_site.py; do not hand-edit -->"
HEAD_END = "<!-- /build:head -->"
HEAD_BLOCK = re.compile(
    r"^[ \t]*" + re.escape(HEAD_START) + r".*?" + re.escape(HEAD_END) + r"[ \t]*\n?",
    re.M | re.S,
)
# legacy bits from before the build: the empty data: icon and a hand-written
# canonical / social block, if a page still carries them.
LEGACY_HEAD = re.compile(
    r'^[ \t]*<link rel="(?:icon|canonical)"[^>]*>[ \t]*\n'
    r'|^[ \t]*<meta (?:property="og:[^"]+"|name="twitter:[^"]+"|name="theme-color")[^>]*>[ \t]*\n',
    re.M,
)
LEGACY_STYLES = re.compile(
    r'^[ \t]*<style id="(?:nav-organic-[a-z-]+|chrome-a11y)">.*?</style>[ \t]*\n',
    re.M | re.S,
)
SKIP_RE = re.compile(r'^[ \t]*<a class="skip"[^>]*>Skip to content</a>[ \t]*\n', re.M)
NAV_RE = re.compile(r'^[ \t]*<nav class="pagenav".*?</nav>', re.M | re.S)


def esc(text: str) -> str:
    return htmllib.escape(text, quote=True)


def target_href(target: str, rel: str) -> str:
    """Render a nav target for this page's serving context."""
    if not target.startswith("/"):
        return target
    in_subdomain = "/" in rel
    if target == "/":
        return "https://artistso.com/"
    if in_subdomain:
        return "https://artistso.com" + target
    return target.lstrip("/")


def nav_html(rel: str, rec: dict) -> str:
    section_target = manifest.SECTIONS.get(rec["section"])
    current_url = manifest.url_for(rel)
    lines = ['    <nav class="pagenav" aria-label="Pages">', '      <div class="pagenav-inner">']
    for label, target in manifest.NAV:
        href = target_href(target, rel)
        # is this link the current page, or its section landing page?
        if target.startswith("/"):
            full = "https://artistso.com/" + target.lstrip("/")
        else:
            full = target
        is_current = full in (current_url, section_target)
        aria = ' aria-current="page"' if is_current else ""
        lines.append(f'        <a class="pnav" href="{href}"{aria}>{esc(label)}</a>')
    lines += ["      </div>", "    </nav>"]
    return "\n".join(lines)


def nav_style(rec: dict) -> str:
    body, radius, section = MOTIFS[rec["motif"]]
    return (
        f'<style id="nav-organic-{rec["motif"]}">\n'
        f'/* Organic nav upgrade 2026-11-26: {section} — {rec["motif"]}. '
        f'CSS only; links and breadcrumbs unchanged. */\n'
        f'.pagenav{{padding-bottom:15px;}}\n'
        f'.pagenav::after{{content:"";position:absolute;left:0;right:0;bottom:2px;height:14px;'
        f'background:url("{body}") repeat-x left center;background-size:120px 14px;pointer-events:none;}}\n'
        f'.pagenav{{position:sticky;}}\n'
        f'.pnav{{border-radius:{radius};transition:background .18s ease,color .18s ease;}}\n'
        f'.crumbs .sep{{color:var(--accent);font-weight:700;}}\n'
        f'</style>'
    )


# Subdomain landing pages that mirror a main-domain page get their own title,
# so no two pages share one in a search result.
SUBDOMAIN_TITLES = {
    "physics/index.html": "Physics &amp; maths — physics.artistso.com · Steven Owens",
    "apps/index.html": "Apps &amp; code — apps.artistso.com · Steven Owens",
    "story/index.html": "Story &amp; writing — story.artistso.com · Steven Owens",
    "work/index.html": "Work &amp; links — work.artistso.com · Steven Owens",
    "ledger/index.html": "Analytical Ledger — ledger.artistso.com · Steven Owens",
    "principalia/index.html": "Principalia — the Ultramile — principalia.artistso.com · Steven Owens",
}


def head_meta(rel: str, rec: dict, title: str, desc: str) -> list:
    url = manifest.url_for(rel)
    light, dark = THEME_BG.get(rec["theme"], THEME_BG["pink"])
    t = esc(htmllib.unescape(title))
    d = esc(desc)
    tags = [
        f'<link rel="icon" href="{FAVICON}" />',
        f'<link rel="canonical" href="{url}" />',
        f'<meta name="theme-color" content="{light}" media="(prefers-color-scheme: light)" />',
        f'<meta name="theme-color" content="{dark}" media="(prefers-color-scheme: dark)" />',
        '<meta property="og:type" content="website" />',
        '<meta property="og:site_name" content="artistso.com" />',
        f'<meta property="og:title" content="{t}" />',
        f'<meta property="og:description" content="{d}" />',
        f'<meta property="og:url" content="{url}" />',
        '<meta name="twitter:card" content="summary" />',
        f'<meta name="twitter:title" content="{t}" />',
        f'<meta name="twitter:description" content="{d}" />',
    ]
    if rec.get("noindex"):
        tags.append('<meta name="robots" content="noindex, follow" />')
    return tags


def build_page(rel: str, rec: dict, text: str) -> str:
    """Return the page with fresh, canonical chrome. Idempotent."""

    # --- remove what we own (first run also clears pre-build leftovers) ----
    text = HEAD_BLOCK.sub("", text)
    text = LEGACY_STYLES.sub("", text)
    text = LEGACY_HEAD.sub("", text)
    text = SKIP_RE.sub("", text)
    text = text.replace('<main id="main-content">', "<main>", 1)

    # --- title + description ----------------------------------------------
    if rel in SUBDOMAIN_TITLES:
        text = re.sub(r"<title>.*?</title>", f"<title>{SUBDOMAIN_TITLES[rel]}</title>", text, count=1, flags=re.S)
    tm = re.search(r"<title>(.*?)</title>", text, re.S)
    title = tm.group(1).strip() if tm else "artistso.com — Steven Owens"
    dm = re.search(r'^[ \t]*<meta name="description" content=".*?"[ \t]*/?>[ \t]*\n', text, re.M | re.S)
    desc_line = f'    <meta name="description" content="{esc(rec["desc"])}" />\n'
    if dm:
        text = text[:dm.start()] + desc_line + text[dm.end():]
    else:
        text = re.sub(r"(</title>[ \t]*\n)", r"\1" + desc_line.replace("\\", "\\\\"), text, count=1)

    # --- head: one managed block ------------------------------------------
    lines = ["    " + HEAD_START]
    styles = (CHROME_CSS,) if rec.get("noindex") else (nav_style(rec), CHROME_CSS)
    for chunk in styles:
        lines.extend("    " + ln for ln in chunk.splitlines())
    for line in head_meta(rel, rec, title, rec["desc"]):   # one tag per line
        lines.append("    " + line)
    lines.append("    " + HEAD_END)
    text = re.sub(
        r"[ \t\n]*</head>",
        "\n" + "\n".join(lines) + "\n  </head>",
        text, count=1,
    )

    # --- body: skip link, main id, shared nav -----------------------------
    text = text.replace("<body>", '<body>\n    <a class="skip" href="#main-content">Skip to content</a>', 1)
    text = text.replace('<main class="wrap">', '<main id="main-content" class="wrap">', 1)
    text = text.replace("<main>", '<main id="main-content">', 1)
    if not rec.get("noindex"):
        text = NAV_RE.sub(lambda _m: nav_html(rel, rec), text, count=1)
    return text


def targets():
    rels = [r for r in sorted(os.listdir(ROOT)) if r.endswith(".html")]
    for sub in manifest.SUBDOMAIN_DIRS:
        p = os.path.join(sub, "index.html")
        if os.path.exists(os.path.join(ROOT, p)):
            rels.append(f"{sub}/index.html")
    return rels


def main(argv=None):
    ap = argparse.ArgumentParser(description="Rebuild shared chrome on artistso.com pages.")
    ap.add_argument("--check", action="store_true", help="report drift only; write nothing")
    ap.add_argument("--list", action="store_true", help="list motifs and pages")
    args = ap.parse_args(argv)

    if args.list:
        print("motifs:")
        for key, (_, radius, section) in MOTIFS.items():
            print(f"  {key:9} radius {radius:22} section {section}")
        print("\nspecial pages:")
        for rel in manifest.SPECIAL:
            print(f"  {rel:26} special (no nav, noindex)")
        print("\npages:")
        for rel in targets():
            rec = manifest.PAGES.get(rel)
            print(f"  {rel:26} {rec['section'] if rec else 'UNMAPPED'}")
        return 0

    rels = targets()
    unmapped = [r for r in rels if r not in manifest.PAGES and r not in manifest.SPECIAL]
    if unmapped:
        print("pages missing from tools/pages.py: " + ", ".join(unmapped), file=sys.stderr)
        return 2

    changed = []
    for rel in rels:
        rec = manifest.PAGES.get(rel) or manifest.SPECIAL.get(rel)
        path = os.path.join(ROOT, rel)
        with open(path, encoding="utf-8") as fh:
            before = fh.read()
        after = build_page(rel, rec, before)
        if after != before:
            changed.append(rel)
            if not args.check:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(after)

    verb = "would change" if args.check else "updated"
    print(f"{len(rels)} pages · {len(changed)} {verb}")
    for rel in changed:
        print(f"  {rel}")
    return 1 if (args.check and changed) else 0


if __name__ == "__main__":
    sys.exit(main())

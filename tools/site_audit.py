#!/usr/bin/env python3
"""site_audit.py — integrity check for artistso.com.

Stdlib only, no dependencies, no network. Run from the repo root:

    python3 tools/site_audit.py            # human report, exit 1 on errors
    python3 tools/site_audit.py --quiet    # summary only
    python3 tools/site_audit.py --json     # machine-readable

What it checks
--------------
Structure
  * every local href/src/action target exists on disk
  * every file has exactly one <main>, one <h1>, one </html>
  * tags balance (unclosed / mismatched elements)
  * no duplicate element ids within a page
  * <html lang> and <html data-theme> present and a known theme
Head
  * unique <title> per page
  * <meta name="description"> present, unique, 60-200 chars
  * <link rel="canonical"> present, absolute, unique, matches the page
  * Open Graph + Twitter card tags present and consistent with the page
  * favicon declared (not an empty data: URI)
Chrome
  * .pagenav present, same link chain and order on every page
  * exactly one aria-current="page", pointing at the page itself
  * .crumbs present
  * organic nav style block present, with a known motif key
Accessibility floor
  * skip-to-content link as the first focusable element
  * <main id="main-content">
  * every <img> has a non-empty alt
House rules
  * no visitor-visible placeholder language (coming soon / TBD / lorem …)
  * no local asset referenced but missing (e.g. a deleted diagram)

Exit codes: 0 = clean, 1 = errors found.
"""

from __future__ import annotations

import argparse
import collections
import html
import json
import os
import re
import sys
from html.parser import HTMLParser

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages as manifest  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

THEMES = {"pink", "blue", "green", "yellow", "purple", "orange", "red", "teal"}
MOTIFS = {
    "vine", "wave", "circuit", "ribbon", "contour", "survey", "mile",
    "map", "gallery", "chapter", "seal", "shelf", "gather", "gate",
    "cycle", "fork", "stack", "lamp", "reel", "note", "index", "thread",
    "record", "bench", "note2",
}

# Subdomain folders: pages served from <sub>.artistso.com/
SUBDOMAINS = {
    "physics": "physics",
    "apps": "apps",
    "story": "story",
    "work": "work",
    "ledger": "ledger",
    "principalia": "principalia",
}

PLACEHOLDER_WORDS = re.compile(
    r"(coming soon|lorem ipsum|under construction|\bTBD\b|stay tuned|placeholder image)",
    re.I,
)

VOID = {
    "area", "base", "br", "col", "embed", "hr", "img", "input", "link",
    "meta", "param", "source", "track", "wbr",
}


class Page:
    def __init__(self, rel: str, text: str):
        self.rel = rel
        self.text = text

    @property
    def url(self) -> str:
        """Public URL this file is served at."""
        d = os.path.dirname(self.rel)
        if d in SUBDOMAINS:
            name = os.path.basename(d)
            return f"https://{name}.artistso.com/"
        return "https://artistso.com/" + (os.path.basename(self.rel) if self.rel != "index.html" else "")

    def find(self, pattern: str, flags: int = re.S):
        return re.search(pattern, self.text, flags)

    def all(self, pattern: str, flags: int = re.S):
        return re.findall(pattern, self.text, flags)

    def first(self, pattern: str, flags: int = re.S):
        """First capture group, or the whole match when there is no group."""
        m = re.search(pattern, self.text, flags)
        if not m:
            return None
        return m.group(1) if m.groups() else m.group(0)


class TagBalance(HTMLParser):
    """Reports unclosed / mismatched start and end tags."""

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.stack = []
        self.problems = []

    def handle_starttag(self, tag, attrs):
        if tag in VOID:
            return
        self.stack.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in VOID:
            return
        if not self.stack:
            self.problems.append(f"stray </{tag}> at line {self.getpos()[0]}")
            return
        if self.stack[-1][0] == tag:
            self.stack.pop()
            return
        # tolerate HTML's optional end tags
        optional = {"li", "p", "td", "th", "tr", "option", "dt", "dd"}
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                unclosed = [t for t, _ in self.stack[i + 1:] if t not in optional]
                if unclosed:
                    self.problems.append(
                        f"</{tag}> at line {self.getpos()[0]} closes over unclosed {unclosed}"
                    )
                del self.stack[i:]
                return
        self.problems.append(f"unmatched </{tag}> at line {self.getpos()[0]}")

    def close(self):
        super().close()
        for tag, pos in self.stack:
            optional = {"html", "body", "head", "li", "p", "td", "th", "tr", "option", "dt", "dd"}
            if tag not in optional:
                self.problems.append(f"unclosed <{tag}> opened at line {pos[0]}")
        return self.problems


def pages_on_disk():
    out = []
    for name in sorted(os.listdir(ROOT)):
        if name.endswith(".html"):
            out.append(name)
    for sub in sorted(SUBDOMAINS):
        p = os.path.join(sub, "index.html")
        if os.path.exists(os.path.join(ROOT, p)):
            out.append(f"{sub}/index.html")
    return out


def load(rel):
    with open(os.path.join(ROOT, rel), encoding="utf-8") as fh:
        return Page(rel, fh.read())


def normalise_href(href: str, page: Page) -> str:
    """Reduce a nav href to a site-wide comparable form.

    Root pages link with relative paths ("projects.html"), subdomain pages with
    absolute ones ("https://artistso.com/projects.html"); both mean the same
    file, so both normalise to "[/main]/projects.html".
    """
    h = html.unescape(href).strip()
    h = re.sub(r"^https://([a-z]+)\.artistso\.com/", r"[\1]/", h)
    h = re.sub(r"^https://artistso\.com/", "[/main]/", h)
    h = re.sub(r"^\[/main\]/$", "[/main]/index.html", h)
    if h.startswith("/"):
        h = "[/main]" + h
    elif h.startswith("index.html") or h == "":
        h = "[/main]/index.html"
    elif not h.startswith("[") and not h.startswith(("http", "#", "mailto")):
        h = "[/main]/" + h
    return h


def audit():
    errors, warnings = [], []
    rels = pages_on_disk()
    pages = {rel: load(rel) for rel in rels}

    titles = collections.defaultdict(list)
    descs = collections.defaultdict(list)
    canon = collections.defaultdict(list)
    navs = collections.defaultdict(list)

    for rel, page in pages.items():
        def err(msg):
            errors.append(f"{rel}: {msg}")

        def warn(msg):
            warnings.append(f"{rel}: {msg}")

        text = page.text

        # ---------- structural ----------
        if not text.lstrip().lower().startswith("<!doctype html>"):
            err("missing <!doctype html>")
        mains = page.all(r"<main\b")
        if len(mains) != 1:
            err("expected exactly 1 <main>, found " + str(len(mains)))
        h1s = page.all(r"<h1\b")
        if len(h1s) != 1:
            err("expected exactly 1 <h1>, found " + str(len(h1s)))
        if text.count("</html>") != 1:
            err(f"expected 1 </html>, found {text.count('</html>')}")

        m = re.search(r"<html\b([^>]*)>", text)
        attrs = m.group(1) if m else ""
        if 'lang="en"' not in attrs:
            err("<html lang> missing or not en")
        tm = re.search(r'data-theme="([^"]+)"', attrs)
        if not tm:
            err("<html data-theme> missing")
        elif tm.group(1) not in THEMES:
            err(f"unknown theme {tm.group(1)!r}")

        ids = page.all(r'\sid="([^"]+)"')
        dups = [k for k, v in collections.Counter(ids).items() if v > 1]
        if dups:
            err(f"duplicate ids: {dups}")

        tb = TagBalance()
        tb.feed(text)
        tb.close()
        for p in tb.problems[:4]:
            warn(f"tag balance: {p}")

        # ---------- links ----------
        for target in page.all(r'(?:href|src)="([^"]+)"'):
            t = html.unescape(target)
            if t.startswith(("http://", "https://", "#", "mailto:", "tel:", "data:", "javascript:")):
                continue
            path = t.split("#")[0].split("?")[0]
            if not path:
                continue
            local = os.path.normpath(os.path.join(os.path.dirname(rel), path))
            if not os.path.exists(os.path.join(ROOT, local)):
                err(f"broken local link: {target}")

        # ---------- head ----------
        title = page.first(r"<title>(.*?)</title>")
        if not title:
            err("missing <title>")
        else:
            titles[html.unescape(re.sub(r"<[^>]+>", "", title)).strip()].append(rel)

        desc = page.first(r'<meta name="description" content="(.*?)"')
        if not desc:
            err('missing <meta name="description">')
        else:
            d = html.unescape(desc).strip()
            descs[d].append(rel)
            if not 60 <= len(d) <= 200:
                warn(f"description is {len(d)} chars (aim 60-200)")

        c = page.first(r'<link rel="canonical" href="([^"]+)"')
        if not c:
            err('missing <link rel="canonical">')
        else:
            canon[c].append(rel)
            if c != page.url:
                err(f"canonical {c} != {page.url}")

        for prop in ("og:type", "og:site_name", "og:title", "og:description", "og:url"):
            if f'property="{prop}"' not in text:
                err(f'missing Open Graph tag {prop}')
            elif prop == "og:url":
                og = page.first(r'<meta property="og:url" content="([^"]+)"')
                if og and og != page.url:
                    err(f"og:url {og} != {page.url}")
        if 'name="twitter:card"' not in text:
            err("missing twitter:card")

        fav = page.first(r'<link rel="icon" href="([^"]*)"')
        if fav is None:
            err("no favicon declared")
        elif fav.strip() in ("", "data:,"):
            warn("favicon is an empty data: URI")

        for img in page.all(r"<img\b[^>]*>"):
            alt = re.search(r'alt="([^"]*)"', img)
            if not alt or not alt.group(1).strip():
                err(f"<img> without alt: {img[:70]}")

        # ---------- chrome ----------
        special = rel in manifest.SPECIAL
        if special:
            # utility pages (404) carry no page nav and are kept out of the index
            if '<meta name="robots" content="noindex' not in text:
                err("special page should carry a noindex robots tag")
            navm = None
        else:
            navm = re.search(r'<nav class="pagenav".*?</nav>', text, re.S)
        if navm is None and not special:
            err("missing .pagenav")
        elif navm is not None:
            navblock = navm.group(0)
            hrefs = re.findall(r'<a class="pnav"[^>]*href="([^"]+)"[^>]*>', navblock)
            if not hrefs:
                hrefs = re.findall(r'href="([^"]+)"', navblock)
            navs[tuple(normalise_href(h, page) for h in hrefs)].append(rel)

            currents = re.findall(r'<a class="pnav"[^>]*aria-current="page"[^>]*href="([^"]+)"', navblock)
            currents += re.findall(r'<a class="pnav"[^>]*href="([^"]+)"[^>]*aria-current="page"', navblock)
            currents = sorted(set(currents))
            if len(currents) != 1:
                err(f'expected exactly 1 aria-current="page" in nav, found {len(currents)}: {currents}')
            else:
                # A page may mark either itself or its section landing page:
                # /physics.html and physics.artistso.com/ are one section.
                own = normalise_href(page.url, page)
                hit = normalise_href(currents[0], page)
                # a page may mark itself, or its section landing page
                rec = manifest.PAGES.get(rel, {})
                landing = manifest.SECTIONS.get(rec.get("section"))
                section_ok = landing is not None and normalise_href(landing, page) == hit
                if hit != own and not section_ok:
                    err(f"aria-current points at {currents[0]}, page is {page.url}")

        if not special and 'class="crumbs"' not in text:
            err("missing .crumbs")

        if not special:
            motif = page.first(r'<style id="nav-organic-([a-z0-9-]+)">')
            if not motif:
                err("missing organic nav style block (#nav-organic-KEY)")
            elif motif not in MOTIFS:
                err(f"unknown organic nav motif {motif!r}")

        # ---------- accessibility floor ----------
        body = page.first(r"<body[^>]*>(.*?)</main>")
        if body is None:
            err("cannot find <body>…</main>")
        else:
            first_focusable = re.search(r'<(a|button|input|select|textarea)\b[^>]*>', body)
            if not first_focusable or 'class="skip"' not in first_focusable.group(0):
                err("first focusable element is not the skip link")
        if not re.search(r'<main[^>]*\bid="main-content"', text):
            err('<main> does not carry id="main-content"')
        if 'href="#main-content"' not in text:
            err("skip link does not target #main-content")

        # ---------- house rules ----------
        visible = re.sub(r"<(script|style)\b.*?</\1>", "", text, flags=re.S)
        visible = re.sub(r"<[^>]+>", " ", visible)
        hits = PLACEHOLDER_WORDS.findall(visible)
        if hits:
            err(f"visitor-visible placeholder language: {sorted(set(hits))}")

    # ---------- manifest ----------
    for rel in rels:
        if rel in manifest.SPECIAL:
            continue
        if rel not in manifest.PAGES:
            errors.append(f"{rel}: not in tools/pages.py (run build_site.py --list)")
        else:
            motif = manifest.PAGES[rel].get("motif")
            if motif not in MOTIFS:
                errors.append(f"{rel}: manifest motif {motif!r} is not a build motif")
    for rel in list(manifest.PAGES) + list(manifest.SPECIAL):
        if rel not in pages:
            errors.append(f"tools/pages.py maps {rel}, but that file does not exist")

    # ---------- cross-page ----------
    for t, rel in titles.items():
        if len(rel) > 1:
            errors.append(f"title reused by {len(rel)} pages: {t[:60]!r} → {rel}")
    for d, rel in descs.items():
        if len(rel) > 1:
            errors.append(f"description reused by {len(rel)} pages: {d[:60]!r} → {rel}")
    for c, rel in canon.items():
        if len(rel) > 1:
            errors.append(f"canonical reused by {len(rel)} pages: {c} → {rel}")

    if len(navs) > 1:
        base = max(navs, key=lambda k: len(navs[k]))
        for k, rel in navs.items():
            if k == base:
                continue
            extra = [h for h in k if h not in base]
            missing = [h for h in base if h not in k]
            errors.append(
                f"nav chain differs on {len(rel)} page(s) {rel[:4]}: "
                f"extra={extra} missing={missing}"
            )

    return errors, warnings, len(pages)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Audit artistso.com HTML.")
    ap.add_argument("--quiet", action="store_true", help="summary only")
    ap.add_argument("--json", action="store_true", help="machine-readable output")
    args = ap.parse_args(argv)

    errors, warnings, n = audit()

    if args.json:
        print(json.dumps(
            {"pages": n, "errors": errors, "warnings": warnings},
            indent=2,
        ))
    else:
        if not args.quiet:
            for e in errors:
                print(f"ERROR  {e}")
            for w in warnings:
                print(f"WARN   {w}")
        print(f"\n{n} pages checked · {len(errors)} errors · {len(warnings)} warnings")

    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())

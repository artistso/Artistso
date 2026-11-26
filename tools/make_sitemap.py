#!/usr/bin/env python3
"""make_sitemap.py — write sitemap.xml and robots.txt from tools/pages.py.

No dependencies, no network. Run after build_site.py:

    python3 tools/make_sitemap.py          # write both files
    python3 tools/make_sitemap.py --check  # exit 1 if the files are out of date

The sitemap covers every public page on the main domain and every subdomain
landing page — one <url> per canonical URL, at the site root, so the crawler
finds each subdomain from one file. 404.html is deliberately left out; it
carries noindex.
"""

from __future__ import annotations

import argparse
import os
import sys
import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pages as manifest  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ROBOTS = """# artistso.com — crawlers welcome.
User-agent: *
Allow: /

Sitemap: https://artistso.com/sitemap.xml
"""


def entries():
    """[(url, priority)] for every indexable page, main domain first."""
    out = []
    for rel, rec in manifest.PAGES.items():
        if rec.get("noindex"):
            continue
        url = manifest.url_for(rel)
        if "/" in rel:
            priority = "0.8"          # a subdomain landing page
        elif url == "https://artistso.com/":
            priority = "1.0"          # the home page
        elif rec["section"] in ("physics", "apps", "story", "ledger", "principalia", "work", "artwork"):
            priority = "0.9"          # a major section landing page
        else:
            priority = "0.6"
        out.append((url, priority))
    out.sort(key=lambda u: (u[1] != "1.0", u[0]))
    return out


def build_sitemap(today: str) -> str:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ]
    for url, priority in entries():
        lines += [
            "  <url>",
            f"    <loc>{url}</loc>",
            f"    <lastmod>{today}</lastmod>",
            "    <changefreq>weekly</changefreq>",
            f"    <priority>{priority}</priority>",
            "  </url>",
        ]
    lines.append("</urlset>")
    return "\n".join(lines) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Write sitemap.xml and robots.txt.")
    ap.add_argument("--check", action="store_true", help="report drift only; write nothing")
    ap.add_argument("--date", default=datetime.date.today().isoformat(),
                    help="lastmod date (default: today)")
    args = ap.parse_args(argv)

    wanted = {
        "sitemap.xml": build_sitemap(args.date),
        "robots.txt": ROBOTS,
    }
    stale = []
    for name, content in wanted.items():
        path = os.path.join(ROOT, name)
        current = open(path, encoding="utf-8").read() if os.path.exists(path) else None
        if current != content:
            stale.append(name)
            if not args.check:
                with open(path, "w", encoding="utf-8") as fh:
                    fh.write(content)

    urls = len(entries())
    if args.check:
        print(f"sitemap: {urls} urls · " + ("up to date" if not stale else "stale: " + ", ".join(stale)))
        return 1 if stale else 0
    print(f"sitemap: {urls} urls · wrote " + (", ".join(wanted) if stale else "nothing (already current)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())

> **Update, 2026-11-26.** The nav chrome is now generated, not hand-pasted.
> `tools/build_site.py` writes one `#nav-organic-KEY` block into every page from
> the motif table in that script, and `tools/pages.py` records which motif each
> page uses. All 39 pages now carry a motif — the main sections keep the ones
> specced below, and every other page has its own. See [BUILD.md](BUILD.md).
> The original spec below is kept as the record of the first pass.

# Organic nav upgrade — spec (2026-11-25)

Steven's brief: upgrade the toolbar/navigation — organic, fresh, original
for each subdomain and breadcrumb, so it stands out. Links and breadcrumb
chains stay consistent site-wide; only the chrome's styling differs per
section. Implemented CSS-only as one inline `<style id="nav-organic-KEY">`
block per page, inserted before `</head>`. No JS changes, no external
resources, no HTML/link/content changes (verified: href lists identical
before/after on every edited file).

## How it works
- `.pagenav` gains 15px bottom padding and an `::after` strip (14px tall,
  repeating every 120px) carrying the section's motif as an inline SVG
  data-URI in the section's theme colours.
- `.pnav` links get a section-specific asymmetric border-radius (organic,
  leaf/pill/ribbon shapes) with a soft hover transition.
- `.crumbs .sep` separators take the section accent colour and bold weight —
  same separator characters and chain as before, just coloured by section.

## Treatments
| Section | Theme | Key | Motif (toolbar strip) | Link radius |
|---|---|---|---|---|
| Home | tropical pink | `vine` | Flowing vine curve in pink with green leaf ellipses | 16px 5px 16px 5px (leaf) |
| Physics & maths | blue | `wave` | Sine wave in blue with a fainter cyan echo wave | 999px (pill) |
| Apps & code | green | `circuit` | Right-angled circuit path with node dots in greens | 3px 10px 3px 10px |
| Story & writing | purple | `ribbon` | Two flowing ribbon curves, purple over pink | 4px 16px 4px 16px |
| Work & links | orange | `contour` | Rolling contour/ridge lines, orange over red | 12px 12px 3px 3px |
| Analytical Ledger | yellow | `survey` | Double ruled survey line with tick marks and a marker dot, gold | 2px |

## Applied to
- Main site: index.html (vine), physics.html (wave), apps.html (circuit),
  story.html (ribbon), ledger.html (survey) — in both
  ~/workspace/artistso-multipage-v2/ and ~/workspace/artistso-repo/.
- Subdomains: physics, apps, story, work (contour), ledger — in
  ~/workspace/artistso-subdomains/<sub>/index.html,
  ~/workspace/deploy-subdomains/<sub>-index.html, and
  ~/workspace/artistso-repo/<sub>/index.html. All copies byte-identical.

## For future pages
Pick the section's key from the table, copy that page's
`nav-organic-KEY` style block verbatim into the new page's `<head>`, and
keep the standard `.pagenav` / `.pnav` / `.crumbs` markup and link set.
New sections get a new motif in the same pattern: one 120×16 SVG strip,
theme colours, one asymmetric radius.

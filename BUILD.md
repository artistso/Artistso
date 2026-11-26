# Build & check — artistso.com

The site is hand-written static HTML: no framework, no bundler, no npm, no
dependencies. Two small Python 3 scripts (stdlib only) keep the shared parts
consistent, and a GitHub Action runs them on every change.

```
tools/pages.py        the manifest: one record per page (description, section, motif, theme)
tools/build_site.py   writes the shared chrome — head metadata, skip link, page nav, motif styles
tools/site_audit.py   checks structure, links, head metadata, chrome, accessibility floor
tools/make_sitemap.py writes sitemap.xml and robots.txt from the manifest
```

## The routine

After editing any page — or adding one:

```bash
python3 tools/build_site.py       # rebuild shared chrome on every page
python3 tools/make_sitemap.py     # refresh sitemap.xml + robots.txt
python3 tools/site_audit.py       # must end: 0 errors
```

`build_site.py --check` and `make_sitemap.py --check` and
`site_audit.py` all exit non-zero when something drifts, which is exactly what
CI runs.

## Adding a page

1. Copy an existing page in the same section — it already carries the hero,
   nav and footer.
2. Add one record to `PAGES` in `tools/pages.py` (description, section, motif,
   theme). The description must be unique and 60–200 characters.
3. Run the three commands above. `build_site.py` will tell you if a page on
   disk has no manifest record.

## What the build owns

`build_site.py` only touches these, and nothing else in a page:

| Part | Where |
|---|---|
| `<link rel="icon">`, canonical, Open Graph, Twitter card, theme-color | the `build:head` block before `</head>` |
| Organic nav style block (`#nav-organic-KEY`) + skip-link/focus CSS | same block |
| The `<nav class="pagenav">` link chain | in the body |
| Skip link as the first focusable element | right after `<body>` |
| `id="main-content"` on the one `<main>` | in the body |

Everything else — prose, verbatim texts, embeds, scripts, breadcrumbs, the
footer, every other link — is left byte for byte alone. The build is
idempotent: running it twice changes nothing, so a clean `--check` is a
meaningful signal.

## Sections and motifs

Each section has its own motif on the nav strip and its own link shape:

| Section | Pages | Motif | Key |
|---|---|---|---|
| Home | index, 404 | flowing vine | `vine` |
| Physics & maths | physics.html, physics/ | sine wave | `wave` |
| Apps & code | apps.html, apps/ | circuit path | `circuit` |
| Projects | projects.html | dashed route | `map` |
| Story & writing | story.html, blog, friends, journey, statement, laws, training, story/ | ribbon | `ribbon` |
| Analytical Ledger | ledger.html, ledger/ | survey rule | `survey` |
| Principalia | principalia/ | milestone line | `mile` |
| Work & links | connect.html, work/ | contour lines | `contour` |
| Artwork | artwork.html | framed wall | `gallery` |
| It's a Pi-E Life | pie.html | book and arrow | `chapter` |
| The Letter | letter.html | seal and dotted rule | `seal` |
| Shop & free | shop.html | shelf | `shelf` |
| Social rooms | facebook, twitch, kick, reddit, youtube, xpage | gathering arcs | `gather` |
| Google Site | gsite.html | gate | `gate` |
| Calendar | calendar.html | month ticks | `cycle` |
| GitHub | github.html | fork | `fork` |
| Docs | docs.html | stacked pages | `stack` |
| NotebookLM | notebooks.html | lamp | `lamp` |
| Movie reviews | reviews.html | film reel | `reel` |
| Muse & Meta | muse-meta.html | note | `note` |
| Career & trades | career.html | ledger line | `record` |
| The bench | bench.html | workbench | `bench` |
| Working papers | partners.html | envelope | `note2` |
| Wiki | wiki.html | index card | `index` |
| Forum | forum.html | speech thread | `thread` |

To add a motif, add one entry to `MOTIFS` in `tools/build_site.py` (one
120×16 SVG strip, one asymmetric border-radius) and reference it from the
manifest.

## CI

`.github/workflows/check.yml` runs the audit on every push and pull request.
It fails on any error, so a broken link or a missing canonical can't land on
`main`. Deploying is still manual — merging to `main` does not auto-deploy.

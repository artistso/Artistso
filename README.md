# artistso.com

Source of Steven Owens' live personal site, [artistso.com](https://artistso.com) (hosted on DreamHost).

## Structure

- **Repo root** — the main-domain pages (35 HTML files: home, physics, apps, story, career, bench, connect, ledger, artwork, blog, statement, laws, journey, and the rest), plus `404.html`, `sitemap.xml` and `robots.txt`.
- **Subfolders** — one per subdomain, each holding that subdomain's `index.html`:
  - `physics/` → physics.artistso.com
  - `apps/` → apps.artistso.com
  - `story/` → story.artistso.com
  - `work/` → work.artistso.com
  - `ledger/` → ledger.artistso.com
  - `principalia/` → principalia.artistso.com
- **`tools/`** — the build and check scripts (Python 3, stdlib only). One manifest in `tools/pages.py` knows every page; `tools/build_site.py` writes the shared head metadata, skip link, page nav and per-section nav styling, and `tools/site_audit.py` checks the result.
- **`PARTNERS.md`** — the working papers between Atlas and Arena: what each changed and why, what is owed, and the decisions waiting on Steven. Mirrored on the site as [partners.html](https://artistso.com/partners.html).
- **blog.artistso.com** is WordPress and is **not** in this repo.
- The board at artistso.com/board/ is a separate PHP app and is **not** in this repo.

## Roles

- **Steven Owens** — owner / CEO. His word is final on everything.
- **Atlas** — Steven's main assistant. Atlas reviews, finalizes, and deploys.
- **Other AI agents and collaborators** — contribute via **pull requests only**. Nothing merges or deploys without Atlas's review, and Steven's approval where he asks for it.

## Deploy

Merging to `main` does **not** auto-deploy. Atlas deploys verified batches to DreamHost manually, at $0 cost.

## Check before you push

See [BUILD.md](BUILD.md) for the build and check routine:

```bash
python3 tools/build_site.py       # shared chrome on every page
python3 tools/make_sitemap.py     # sitemap.xml + robots.txt
python3 tools/site_audit.py       # must end: 0 errors
```

CI runs the same three checks on every push and pull request.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the house rules.

## Credits

- **Steven Owens** — owner, author, final word.
- **Atlas (Muse)** — assistant and collaborator: reviews, finalizes, builds and deploys alongside Steven.

Steven's words, Nov 25, 2026: "It's not just my website anymore. It's our website."

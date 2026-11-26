# artistso.com

Source of Steven Owens' live personal site, [artistso.com](https://artistso.com) (hosted on DreamHost).

## Structure

- **Repo root** — the main-domain pages (29 HTML files: home, physics, apps, story, connect, ledger, artwork, blog, statement, laws, journey, and the rest).
- **Subfolders** — one per subdomain, each holding that subdomain's `index.html`:
  - `physics/` → physics.artistso.com
  - `apps/` → apps.artistso.com
  - `story/` → story.artistso.com
  - `work/` → work.artistso.com
  - `ledger/` → ledger.artistso.com
- **blog.artistso.com** is WordPress and is **not** in this repo.
- The board at artistso.com/board/ is a separate PHP app and is **not** in this repo.

## Roles

- **Steven Owens** — owner / CEO. His word is final on everything.
- **Atlas** — Steven's main assistant. Atlas reviews, finalizes, and deploys.
- **Other AI agents and collaborators** — contribute via **pull requests only**. Nothing merges or deploys without Atlas's review, and Steven's approval where he asks for it.

## Deploy

Merging to `main` does **not** auto-deploy. Atlas deploys verified batches to DreamHost manually, at $0 cost.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the house rules before opening a PR.

## Credits

- **Steven Owens** — owner, author, final word.
- **Atlas (Muse)** — assistant and collaborator: reviews, finalizes, builds and deploys alongside Steven.

Steven's words, Nov 25, 2026: "It's not just my website anymore. It's our website."

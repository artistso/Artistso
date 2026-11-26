# Working papers — the partnership

Steven Owens owns the site and the final word on it. Two agents work on it with
him: **Atlas** (Muse) and **Arena** (this repo's build sessions). This file is
the shared notebook between them so each knows what the other did, why, and what
is still owed.

House rule for this file: **claims carry a status.** `done` means it is in the
repo and the audit passes. `proposed` means somebody wants it. `owed` means a
named agent has to do something before it is finished. Nothing here is aspirational
without saying so.

---

## Standing division of labour

| Who | Owns |
|---|---|
| **Steven** | Final word. Author of every verbatim text. Decides what ships. |
| **Atlas (Muse)** | Review, finalize, deploy to DreamHost. The Drive/Docs working channel. The referee role on research. |
| **Arena** | Code changes on this repo, the build/audit tooling, and pull requests for Atlas to review. |

Neither agent deploys. Atlas deploys, after Steven's word.

---

## Partner notes

### Arena → Atlas — 2026-11-26

**What I did, and why.** Three things, in one pull request, all of them
structural rather than editorial:

1. **The nav chain was never site-wide.** `Principalia` appeared in the nav only
   on its own page; `Muse & Meta` only on its own page. Every other page was
   missing both. I generated one nav chain from `tools/pages.py` and wrote it to
   all 41 pages — with exactly one `aria-current` per page, pointing at the page
   or its section landing page.
2. **The head was empty.** No canonical URLs, no Open Graph, no Twitter card, an
   empty `data:,` favicon, no sitemap, no 404 page. All of that is now generated
   per page from the same manifest.
3. **Nothing checked any of it.** `tools/site_audit.py` now checks structure,
   local links, head metadata, chrome, the accessibility floor, and the house
   no-placeholder rule. It ends at 0 errors. `.github/workflows/check.yml` runs
   it — plus the build check and the sitemap check — on every push and PR.

**What I deliberately did not do.** I did not move `physics.html`,
`apps.html`, `story.html`, `ledger.html` or `connect.html` into their matching
subfolders. The README maps each subfolder to a *different* page on a subdomain
(`physics/index.html` is not a copy of `physics.html` in intent), and
`NAV-UPGRADE.md` says the copies are byte-identical — so a move would delete the
page the nav points at. `connect.html` and `work/index.html` being identical is
the strongest evidence that the mapping is approximate: two different lots, one
file. **This needs your decision, not mine:** either the subdomain deploys from
the subfolder and the root page is the canonical one for the main domain, or
`work/` should be a copy of `connect.html` and the duplication is intended. Tell
me which and I will make the tree match it.

**Two content items for you:**
- `training.html` referenced `training-styles.jpg`, which was never in the repo.
  I drew a replacement, `training-styles.svg`, from the ratings table already on
  the page. If the original photograph exists, swap it back in.
- `laws.html` is live copy naming specific alleged offences. I have not touched it —
  it is protected verbatim text — but it is public and it is legal in nature. Flagging
  it, not changing it.

**What I added from Drive.**

- `career.html` — *Career & trades.* Twenty-two years that were nowhere on the
  site: Lucky Eagle and Gold Coast, PR and crisis communications, fine art and
  animation, and the trades. Built from the CV Doc and the Journey page, with
  `Steven stated` / `From my files` provenance labels on every block.
- `bench.html` — *The bench.* The seventeen apps from the working list in Drive,
  each row labelled `built`, `in progress`, or `spec`. Nothing on the page claims
  a build that does not exist.

Both pages are new prose in Steven's register, not found text. **Please read
them as the reviewer** — if a line reads as written-about-him rather than
written-as-him, it should be cut.

**Proposed, not done** (needs Steven's word before it is real):
- The Vroom product concept (modular electrostatic sweeper) is written up in a
  separate set of Docs from 25 Nov. It is a product idea, not a page yet, and it
  should not go on the site as a product page until Steven says what it is.
- The Drive folder `03 — Deployment & Muse` is empty; so is
  `02 — Site Assets & Content`. The Nov 7 review Docs in `01 — Review & Handoff`
  describe an *empty* repository, propose "creative community for independent
  artists" positioning, and use `hello@artistso.com` — none of which matches the
  live site or the site's voice. **They should not be used as a brief.** I have
  left all three folders alone.

**Owed by me:** nothing on this branch. It is ready for review.

### Atlas → Arena — (open)

*Atlas: add your note above this line. Status on the PR, any corrections to the
prose, and the deploy-mapping decision when Steven gives it.*

---

## The issue queue

Everything open is filed as a GitHub issue, so Atlas has a work queue rather
than a conversation to re-read. **Start at [#11 — the queue](https://github.com/artistso/Artistso/issues/11)**, which indexes the rest.

| # | Issue | Kind |
|---|---|---|
| [#2](https://github.com/artistso/Artistso/issues/2) | Main-domain / subdomain mapping — five byte-identical twins | needs a decision |
| [#3](https://github.com/artistso/Artistso/issues/3) | `training-styles.jpg` never existed — chart stands in | confirm or replace |
| [#4](https://github.com/artistso/Artistso/issues/4) | Muse letter 2 — publish or not, and where | needs a decision |
| [#5](https://github.com/artistso/Artistso/issues/5) | Drive: the Nov 7 review Docs are stale | needs a decision |
| [#6](https://github.com/artistso/Artistso/issues/6) | `laws.html` — public page naming alleged offences | needs a decision |
| [#7](https://github.com/artistso/Artistso/issues/7) | Nav: 30 links is too many — two-tier proposal | task, own PR |
| [#8](https://github.com/artistso/Artistso/issues/8) | Review the new pages' prose; homes for the faith material and Vroom | task |
| [#9](https://github.com/artistso/Artistso/issues/9) | Write the deploy runbook | task |
| [#10](https://github.com/artistso/Artistso/issues/10) | Home page: three different page counts, no lot numbers | needs a decision |

Labels in use: `needs-decision` (waiting on Steven), `atlas` (for Atlas),
`content`, `deploy`, `drive`.

**Rule:** a decision is not an edit. If an issue is labelled `needs-decision`,
the code change is usually small and the *choice* is the hard part — get the
choice, then make the change.

---

## The open decisions

1. **Subdomain mapping** — see above. Blocks making the tree honest.
2. **Verbatim texts** — Arena does not edit the Breadcrumb Trail, statement,
   laws, journey, Pi-E excerpts, the Letter, or blog entries. If a change is
   wanted there, Steven says it, Atlas applies it.
3. **Delivery channel** — the Muse letter is currently a Doc in Drive and a file
   in this repo, not a page. Publishing it as a subdomain page needs a "yes".
4. **Whether the bench goes in the nav.** It is in the nav now, twenty-nine links
   deep. If that is too long, the fix is a nav rebuild, not a one-page edit.

---

## How we keep from stepping on each other

- Every change that touches shared chrome is generated, not hand-edited. If you
  want a different nav, change `tools/pages.py` and run the build.
- `python3 tools/build_site.py --check` must say `0 would change` before any
  commit. If it does not, somebody hand-edited a generated block.
- `python3 tools/site_audit.py` must say `0 errors`.
- Deploy is still Atlas's. `main` is not production.

# Contributing — house rules

These rules apply to every agent and collaborator working on artistso.com. Steven Owens is the owner/CEO; Atlas reviews and finalizes all changes.

1. **Voice.** The site is written in first person in Steven's own verbiage. No AI verbiage, no third-person copy about him, no marketing polish.
2. **No visitor-visible placeholders.** No placeholder tiles or images, no "coming soon / pending / TBD" notices, no empty embed slots. If content isn't real yet, leave the section out entirely. (Backend state is for Steven and Atlas to see, not visitors.)
3. **Never edit Steven's verbatim texts** — the Breadcrumb Trail, the statement / laws / journey pages, the Pi-E excerpts, the Letter, and blog entries — except at his explicit instruction.
4. **Small changes, one PR per topic.** Describe what changed and what you verified.
5. **Embeds, links, scripts.** Do not alter existing embeds, URLs, or scripts unless the PR is specifically about them.
6. **Cost: $0.** No paid services, no new dependencies that cost money.
7. **Atlas finalizes.** PRs are reviewed by Atlas before anything merges or deploys. Steven is CEO — his word overrides any style rule.
8. **Run the checks.** `python3 tools/build_site.py && python3 tools/make_sitemap.py && python3 tools/site_audit.py` — the audit must end at 0 errors. CI (`.github/workflows/check.yml`) runs the same three checks and fails the PR if any of them is dirty.
9. **One manifest.** Add or change a page in `tools/pages.py` first, then run the build. The page nav, canonical URL, Open Graph tags and description are generated from that record — don't hand-write them into a page.

#!/usr/bin/env python3
"""pages.py — the manifest for artistso.com.

One record per HTML file in the repo. The build (tools/build_site.py) and the
audit (tools/site_audit.py) both read this, so there is one place that knows
what each page is, where it is served from, and which nav section it belongs to.

Fields
------
desc     <meta name="description"> — first person, plain, 60–200 characters.
section  nav section the page belongs to (drives aria-current and the motif).
motif    organic nav motif key (see MOTIFS in build_site.py).
theme    value for <html data-theme>.

Edit this file when a page is added, renamed, or re-described. Then run
`python3 tools/build_site.py` and `python3 tools/site_audit.py`.
"""

# ---------------------------------------------------------------- nav chain --
# The one nav chain every page carries: (label, target). "target" is either a
# URL (subdomain or main-domain page). Main-domain pages are written
# site-root-relative ("/projects.html") and rendered relative for root pages
# and absolute for subdomain pages, so both serving contexts work.
NAV = [
    ("Home", "/"),
    ("Physics & maths", "https://physics.artistso.com/"),
    ("Apps & code", "https://apps.artistso.com/"),
    ("Projects", "/projects.html"),
    ("Story & writing", "https://story.artistso.com/"),
    ("Career & trades", "/career.html"),
    ("The bench", "/bench.html"),
    ("Analytical Ledger", "https://ledger.artistso.com/"),
    ("Principalia", "https://principalia.artistso.com/"),
    ("Artwork", "/artwork.html"),
    ("It's a Pi-E Life", "/pie.html"),
    ("The Letter", "/letter.html"),
    ("Shop & free", "/shop.html"),
    ("Work & links", "https://work.artistso.com/"),
    ("Facebook", "/facebook.html"),
    ("Twitch", "/twitch.html"),
    ("Kick", "/kick.html"),
    ("Reddit", "/reddit.html"),
    ("YouTube", "/youtube.html"),
    ("X", "/xpage.html"),
    ("Google Site", "/gsite.html"),
    ("Calendar", "/calendar.html"),
    ("GitHub", "/github.html"),
    ("Docs", "/docs.html"),
    ("NotebookLM", "/notebooks.html"),
    ("Movie reviews", "/reviews.html"),
    ("Muse & Meta", "/muse-meta.html"),
    ("Working papers", "/partners.html"),
    ("Wiki", "/wiki.html"),
    ("Forum", "/forum.html"),
]

# Section key -> the NAV target that represents it.
SECTIONS = {
    "home": "/",
    "physics": "https://physics.artistso.com/",
    "apps": "https://apps.artistso.com/",
    "projects": "/projects.html",
    "story": "https://story.artistso.com/",
    "careers": "/career.html",
    "bench": "/bench.html",
    "ledger": "https://ledger.artistso.com/",
    "principalia": "https://principalia.artistso.com/",
    "artwork": "/artwork.html",
    "pie": "/pie.html",
    "letter": "/letter.html",
    "shop": "/shop.html",
    "work": "https://work.artistso.com/",
    "social": None,          # each social page is its own section
    "calendar": "/calendar.html",
    "code": "/github.html",
    "library": "/docs.html",
    "reviews": "/reviews.html",
    "meta": "/muse-meta.html",
    "partners": "/partners.html",
    "reference": "/wiki.html",
    "forum": "/forum.html",
}

# page file -> record.  desc is the human-facing summary; keep it unique.
PAGES = {
    # ---------------------------------------------------------------- home --
    "index.html": dict(
        section="home", motif="vine", theme="pink",
        desc="artistso.com: I'm Steven Owens — artist, animator, educator, developer. Drawing, pen-first Android apps, theoretical physics written referee-style, and long-form prose. Everything here runs at $0.",
    ),
    # ------------------------------------------------------------- physics --
    "physics.html": dict(
        section="physics", motif="wave", theme="blue",
        desc="My physics and mathematics, written referee-style: Quadrature Time, universe-line / zero-rings, K3,3, QCAV, and the Higgs-soup toy model — each claim labelled and stress-tested.",
    ),
    "physics/index.html": dict(
        section="physics", motif="wave", theme="blue",
        desc="physics.artistso.com — my physics and mathematics, written referee-style: Quadrature Time, universe-line / zero-rings, K3,3, QCAV, and the Higgs-soup toy model.",
    ),
    # ---------------------------------------------------------------- apps --
    "apps.html": dict(
        section="apps", motif="circuit", theme="green",
        desc="Drawing, animation, and notes apps I build for pen-first Android tablets — InkMind, Pluart, and the SoCreate line. On-device, no backend, build status stated plainly.",
    ),
    "apps/index.html": dict(
        section="apps", motif="circuit", theme="green",
        desc="apps.artistso.com — the pen-first Android apps: InkMind, Pluart, and the SoCreate line. On-device, no backend, no API keys, and the build status stated plainly.",
    ),
    # ------------------------------------------------------------ projects --
    "bench.html": dict(
        section="bench", motif="bench", theme="pink",
        desc="The bench: seventeen apps written down with the honest state of each one — what is built, what is typed, and what is still only a specification.",
    ),
    "projects.html": dict(
        section="projects", motif="map", theme="pink",
        desc="The full project index — socreate, quadrature-time, and the drawing, research, and games families, across several generations of each idea.",
    ),
    # --------------------------------------------------------------- story --
    "story.html": dict(
        section="story", motif="ribbon", theme="purple",
        desc="The Breadcrumb Trail — my life in crumbs, from a memory that goes back to age three through the 2018 break and everything rebuilt since.",
    ),
    "story/index.html": dict(
        section="story", motif="ribbon", theme="purple",
        desc="story.artistso.com — the Breadcrumb Trail: my life in crumbs, language and writing, from the memory that goes back to age three through everything rebuilt since.",
    ),
    "blog.html": dict(
        section="story", motif="ribbon", theme="purple",
        desc="My blog entries, newest first — notes from the walk back: what happened, what I remember, and what I'm building.",
    ),
    "friends.html": dict(
        section="story", motif="ribbon", theme="purple",
        desc="The friends and family I remember — the people I met in my amnesia state, the people outside it, and the people from before it.",
    ),
    "journey.html": dict(
        section="story", motif="ribbon", theme="purple",
        desc="My journey to Washington, year by year — his account, from Snohomish County in 1983 through Hanford, Las Vegas, Aberdeen, and Hoquiam.",
    ),
    "career.html": dict(
        section="careers", motif="record", theme="pink",
        desc="The record before the record: twenty-two years of casino floor leadership, PR and crisis communications, art and animation, and the trades — labelled by provenance.",
    ),
    "statement.html": dict(
        section="story", motif="ribbon", theme="purple",
        desc="Statement of record: my own account, in my own words, of what happened to me and what I am rebuilding from — with the record behind it.",
    ),
    "laws.html": dict(
        section="story", motif="ribbon", theme="purple",
        desc="Potential laws broken against Steven Owens — a structured list based strictly on the allegations in the report and the Washington State law it references. Not a legal determination.",
    ),
    "training.html": dict(
        section="story", motif="ribbon", theme="purple",
        desc="Martial arts and wrestling in my own account — what I learned first, before freestyle and Greco-Roman, with reference notes on each style.",
    ),
    # -------------------------------------------------------------- ledger --
    "ledger.html": dict(
        section="ledger", motif="survey", theme="yellow",
        desc="The Analytical Ledger — language as cartography. An analytical log, not a boast sheet: who I was against who I am now, every block carrying its provenance.",
    ),
    "ledger/index.html": dict(
        section="ledger", motif="survey", theme="yellow",
        desc="ledger.artistso.com — the Analytical Ledger: language as cartography, an analytical log with every block carrying its provenance. New, logged 2026-11-22.",
    ),
    # --------------------------------------------------------- principalia --
    "principalia/index.html": dict(
        section="principalia", motif="mile", theme="teal",
        desc="Principalia — the Ultramile: my principles and my walk of life. What I've done, what I do — the statements and philosophies others can take with them, and the demonstration of them.",
    ),
    # ------------------------------------------------------------- artwork --
    "artwork.html": dict(
        section="artwork", motif="gallery", theme="pink",
        desc="The gallery wall — my drawing and animation, posted first to Facebook, Google, and Reddit, gathered here on one page. Commissions open.",
    ),
    "pie.html": dict(
        section="pie", motif="chapter", theme="pink",
        desc="It's a Pi-E Life — a surreal science-fiction novella, book one of Found Me, free to read here: pages one to three in a demo reader.",
    ),
    "letter.html": dict(
        section="letter", motif="seal", theme="pink",
        desc="The thank-you letter to the Muse team, sent 6 November 2026, published as a page in its own right, with dated notes as Steven's review continues.",
    ),
    "shop.html": dict(
        section="shop", motif="shelf", theme="pink",
        desc="Shop and free — ebooks and apps I sell directly, and the lot I give away free alongside them. Sales start when a real compiled build exists.",
    ),
    # --------------------------------------------------------------- work ---
    "connect.html": dict(
        section="work", motif="contour", theme="orange",
        desc="Commissions and instruction: art and animation, online lessons in drawing and animation, and pen-first Android development. Message @soquarky on X.",
    ),
    "work/index.html": dict(
        section="work", motif="contour", theme="orange",
        desc="work.artistso.com — commissions and instruction: art and animation, lessons in drawing and animation, and pen-first Android development. Message @soquarky on X.",
    ),
    # -------------------------------------------------------------- social --
    "facebook.html": dict(
        section="social", motif="gather", theme="pink",
        desc="My Facebook room: new artwork as it posts, Substack announcements, stream notices, and the long threads that start here and end up in the Docs library.",
    ),
    "twitch.html": dict(
        section="social", motif="gather", theme="pink",
        desc="My Twitch room: live drawing, animation sessions, and build-alongs. Stream times post to the Calendar page and to X ahead of each session.",
    ),
    "kick.html": dict(
        section="social", motif="gather", theme="pink",
        desc="The Kick room — verified and open. Streams run as soquarkly: drawing, animation, and whatever the workbench holds that day.",
    ),
    "reddit.html": dict(
        section="social", motif="gather", theme="pink",
        desc="The Reddit room: posts and threads out in the subs — physics boards, artwork, and app progress, gathered back here so the conversation has one shelf.",
    ),
    "youtube.html": dict(
        section="social", motif="gather", theme="pink",
        desc="My video shelf: drawing sessions, animation tests, physics explainers, and songs — with written versions on the pages they belong to.",
    ),
    "xpage.html": dict(
        section="social", motif="gather", theme="pink",
        desc="X — @soquarky. Posts land here first and commissions start here: art and animation, instruction, pen-first software. Message with what you need.",
    ),
    "gsite.html": dict(
        section="social", motif="gate", theme="pink",
        desc="soquarky.click — the Google Sites edition of the house. Same name, Google-built rooms. The main house is artistso.com now; this address stays standing.",
    ),
    # ------------------------------------------------------------ calendar --
    "calendar.html": dict(
        section="calendar", motif="cycle", theme="pink",
        desc="My public schedule: streams, releases, and open commission slots, kept here on one page. Bookings run through X — message @soquarky.",
    ),
    # ---------------------------------------------------------------- code --
    "github.html": dict(
        section="code", motif="fork", theme="pink",
        desc="artistso on GitHub — 47 repositories: drawing and animation, research code, games and experiments, iterated in the open across several generations.",
    ),
    # ------------------------------------------------------------- library --
    "docs.html": dict(
        section="library", motif="stack", theme="pink",
        desc="The document library — 500+ Google Docs of physics, language, memoir, and code notes, with the public index of manuscripts and their test bundles.",
    ),
    "notebooks.html": dict(
        section="library", motif="lamp", theme="pink",
        desc="NotebookLM notebooks for each body of my work — ask the physics, ask the language, ask the memoir, and get answers cited back to the documents.",
    ),
    # ------------------------------------------------------------- reviews --
    "reviews.html": dict(
        section="reviews", motif="reel", theme="pink",
        desc="My movie reviews — the film, the verdict, the rating on a four-star scale, and the one scene I can't stop thinking about.",
    ),
    "muse-meta.html": dict(
        section="meta", motif="note", theme="pink",
        desc="My reviews of Muse and Meta — the current review and the constant reviews, for the usage of what we're consistently doing.",
    ),
    # ----------------------------------------------------------- reference --
    "partners.html": dict(
        section="partners", motif="note2", theme="pink",
        desc="The working papers between Atlas and Arena — what each did and why, what is still owed, and the decisions waiting on Steven.",
    ),
    "wiki.html": dict(
        section="reference", motif="index", theme="pink",
        desc="The shared reference for my whole body of work — the ALUMELA lexicon of all 206 forms, zero-rings, the apps, and the build records.",
    ),
    "forum.html": dict(
        section="forum", motif="thread", theme="pink",
        desc="Discussion for the work — vote a topic up or down and make your point in 250 characters or fewer. Runs in this browser session only.",
    ),
}

SUBDOMAIN_DIRS = ("apps", "ledger", "physics", "principalia", "story", "work")

# Pages that exist for browsers and crawlers rather than for the Directory.
# They get the shared head, the skip link and the accessibility floor, but not
# the page nav — and they are marked noindex and kept out of the sitemap.
SPECIAL = {
    "404.html": dict(
        section="home", motif="vine", theme="pink", noindex=True,
        desc="That address isn't on this site. Here are the doors that are — every page of artistso.com, in one list.",
    ),
}


def url_for(rel: str) -> str:
    """Public URL for a repo-relative HTML path."""
    if "/" in rel:
        sub = rel.split("/")[0]
        if sub in SUBDOMAIN_DIRS and rel.endswith("/index.html"):
            return f"https://{sub}.artistso.com/"
        return "https://artistso.com/" + rel
    if rel == "index.html":
        return "https://artistso.com/"
    return "https://artistso.com/" + rel

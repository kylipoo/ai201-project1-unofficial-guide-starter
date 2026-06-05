"""
Milestone 3 — Stage 1: Document Ingestion.

Fetches the 10 Minecraft Wiki articles listed in planning.md, strips them down to
the gameplay prose, and saves one cleaned, *structured* JSON file per article into
documents/.

"Structured" matters: instead of dumping a wall of text, each article is saved as a
list of sections that preserve the wiki's own header hierarchy (e.g. Behavior > Curing).
chunker.py relies on that structure to do header-aware splitting and to build the
"Article > Section:" prefix described in the Chunking Strategy section of planning.md.

Run:  python ingest.py
"""

import json
import time
from pathlib import Path

import requests
from bs4 import BeautifulSoup

API = "https://minecraft.wiki/api.php"
HEADERS = {"User-Agent": "ai201-project1/1.0 (student RAG project; contact via course)"}
OUT_DIR = Path("documents")

# The 10 sources from planning.md -> Documents.
# `page` is the exact wiki page name used by the API (spaces become underscores).
SOURCES = [
    {"title": "Villager",        "page": "Villager",        "url": "https://minecraft.wiki/w/Villager"},
    {"title": "Piglin",          "page": "Piglin",          "url": "https://minecraft.wiki/w/Piglin"},
    {"title": "Bartering",       "page": "Bartering",       "url": "https://minecraft.wiki/w/Bartering"},
    {"title": "Ender Dragon",    "page": "Ender_Dragon",    "url": "https://minecraft.wiki/w/Ender_Dragon"},
    {"title": "Illager",         "page": "Illager",         "url": "https://minecraft.wiki/w/Illager"},
    {"title": "Enchantment",     "page": "Enchantment",     "url": "https://minecraft.wiki/w/Enchantment"},
    {"title": "Slime",           "page": "Slime",           "url": "https://minecraft.wiki/w/Slime"},
    {"title": "The End",         "page": "The_End",         "url": "https://minecraft.wiki/w/The_End"},
    {"title": "The Nether",      "page": "The_Nether",      "url": "https://minecraft.wiki/w/The_Nether"},
    {"title": "Trial Chambers",  "page": "Trial_Chambers",  "url": "https://minecraft.wiki/w/Trial_Chambers"},
]

# Top-level (h2) sections to DROP. This is a blocklist, not a keep-list: a mob page
# (Spawning/Behavior/Trading) and a dimension page (Accessing/Environment) share almost
# no gameplay headers, but they ALL share this non-gameplay tail. Keeping everything
# except these survives the different article types. Names are matched case-insensitively
# against the cleaned heading text. (Derived by surveying all 10 articles' section lists.)
EXCLUDE_SECTIONS = {
    "history",          # version-by-version changelog — ~40% of each article, off-topic for "how to play"
    "issues",           # links to the bug tracker
    "gallery",          # images only
    "videos",           # embedded videos
    "references",       # citations
    "external links",   # outbound links
    "see also",         # outbound links
    "navigation",       # navbox of every related page
    "data values",      # NBT / numeric ID tables, not prose
    "technical information",  # ID/numeric-id tables + save-folder paths, not gameplay prose
    "sounds",           # tables of sound-event files
    "achievements",     # Bedrock achievement list
    "advancements",     # Java advancement list
    "trivia",           # off-topic factoids / version trivia
    "notes",            # footnotes
    "contents",         # the MediaWiki table-of-contents (an <h2>Contents</h2> in the .toc box)
}

# CSS selectors for page furniture to delete before reading text: infoboxes, navboxes,
# edit links, refs. NOTE: we no longer delete every <table> — content tables (class
# "wikitable") hold real data (loot, enchantment descriptions) and are flattened to text
# instead (see flatten_table). Layout/sprite tables that are not wikitables contribute
# nothing because the walk only reads wikitables.
JUNK_SELECTORS = [
    "style", "script",
    "sup.reference", ".mw-editsection", ".navbox", ".infobox",
    ".thumb", ".mw-empty-elt", ".reflist", ".noprint", ".hatnote",
    ".toc",             # table-of-contents box (otherwise captured as a "Contents" section)
]


def flatten_table(table):
    """Render a wiki content table as text: one row per line, cells joined by ' | '."""
    rows = []
    for tr in table.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["th", "td"], recursive=False)]
        cells = [c for c in cells if c]
        if cells:
            rows.append(" | ".join(cells))
    return "\n".join(rows)


def fetch_html(page: str) -> str:
    """Return the rendered HTML body of a wiki page via the MediaWiki parse API."""
    resp = requests.get(
        API,
        params={"action": "parse", "page": page, "prop": "text",
                "format": "json", "redirects": 1},
        headers=HEADERS,
        timeout=30,
    )
    resp.raise_for_status()
    return resp.json()["parse"]["text"]["*"]


def extract_sections(html: str):
    """
    Walk the article body in document order and group prose under its heading path.

    Returns a list of {"section": "Behavior > Curing", "text": "..."} dicts, with
    the non-gameplay sections (and all their subsections) removed.
    """
    soup = BeautifulSoup(html, "lxml")
    for selector in JUNK_SELECTORS:
        for tag in soup.select(selector):
            tag.decompose()

    body = soup.find("div", class_="mw-parser-output") or soup

    sections = []
    heads = {2: None, 3: None, 4: None}   # current heading at each level -> breadcrumb
    buf = []                              # text collected under the current heading
    skipping = False                      # True while inside an excluded h2

    def current_path():
        parts = [heads[lvl] for lvl in (2, 3, 4) if heads[lvl]]
        return " > ".join(parts)

    def flush():
        if buf and not skipping:
            text = "\n".join(buf).strip()
            if text:
                sections.append({"section": current_path() or "(introduction)", "text": text})

    # Walk every descendant in document order (not just direct children), so content and
    # tables nested inside wrapper <div>s are still reached and land under the right header.
    for el in body.descendants:
        name = getattr(el, "name", None)
        if name is None:
            continue

        if name in ("h2", "h3", "h4"):
            flush()
            buf = []
            level = int(name[1])
            heading_name = el.get_text(" ", strip=True)
            heads[level] = heading_name
            for deeper in range(level + 1, 5):   # entering a new section resets deeper crumbs
                heads[deeper] = None
            if level == 2:                       # only top sections toggle the skip switch
                skipping = heading_name.lower() in EXCLUDE_SECTIONS
            continue

        if skipping:
            continue

        # A wikitable is collected whole (flattened); its inner <p>/<li> are skipped below
        # so we don't also collect them twice. Nested lists are likewise handled by their
        # outer list, and list items by their <ul>/<ol>.
        if name == "table":
            if "wikitable" in (el.get("class") or []):
                flat = flatten_table(el)
                if flat:
                    buf.append(flat)
            continue

        if el.find_parent(["table", "li"]) is not None:
            continue   # already represented by its table / list item

        if name in ("p", "dl"):
            text = el.get_text(" ", strip=True)
            if text:
                buf.append(text)
        elif name in ("ul", "ol"):
            if el.find_parent(["ul", "ol"]) is not None:
                continue   # nested list — the outer list's get_text already includes it
            for li in el.find_all("li", recursive=False):
                item = li.get_text(" ", strip=True)
                if item:
                    buf.append(f"- {item}")

    flush()
    return sections


def main():
    OUT_DIR.mkdir(exist_ok=True)
    print(f"Ingesting {len(SOURCES)} articles into {OUT_DIR}/\n")

    for src in SOURCES:
        html = fetch_html(src["page"])
        sections = extract_sections(html)
        doc = {"title": src["title"], "url": src["url"], "sections": sections}

        slug = src["page"].lower().replace("/", "_")
        out_path = OUT_DIR / f"{slug}.json"
        out_path.write_text(json.dumps(doc, indent=2, ensure_ascii=False), encoding="utf-8")

        total_chars = sum(len(s["text"]) for s in sections)
        print(f"  {src['title']:<16} {len(sections):>3} sections  {total_chars:>6} chars  -> {out_path}")
        time.sleep(1)   # be polite to the wiki between requests

    print("\nDone. Inspect a file, e.g.:  python -m json.tool documents/the_nether.json | less")


if __name__ == "__main__":
    main()

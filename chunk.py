"""
Milestone 3 — Stage 2: Chunking.

Turns the cleaned documents/*.json files from ingest.py into retrieval-ready chunks,
following the Chunking Strategy section of planning.md:

  - Header-aware: split on the wiki's own section headers first; only sub-split a
    section when it is longer than the target size.
  - Target size ~250 tokens, measured with the *actual* all-MiniLM-L6-v2 tokenizer
    (the embedding model only encodes its first 256 tokens, so anything past that
    would never make it into the vector).
  - 40-50 token overlap, applied only when a long section is sub-split, so a fact
    isn't cut in half at a boundary.
  - Every chunk is prefixed with "Article > Section:" so it keeps its context even
    when the sentence itself doesn't name the article.
  - Every chunk carries {source, section, url} metadata for Milestone 4.

Run:  python chunk.py                 # chunk everything -> chunks.json
      python chunk.py --inspect "The Nether"   # print that article's chunks to eyeball
"""

import json
import random
import re
import sys
from pathlib import Path

from transformers import AutoTokenizer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
DOCS_DIR = Path("documents")
OUT_FILE = Path("chunks.json")

# all-MiniLM-L6-v2 truncates input at 256 tokens (its max_seq_length), and 2 of those
# are the special [CLS]/[SEP] tokens the model adds automatically. We target a bit under
# that so the prefix + body always fit inside the window that actually gets embedded.
MAX_TOKENS = 250
OVERLAP_TOKENS = 45

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def n_tokens(text: str) -> int:
    """Token count as the embedding model will see it (no special tokens added here)."""
    return len(tokenizer.encode(text, add_special_tokens=False))


def split_sentences(text: str):
    """
    Break a block into sentence-ish pieces. Splits on line breaks first (paragraphs and
    list items from ingest.py) and then on sentence-ending punctuation, so the chunker
    has small units to pack and never has to cut in the middle of a sentence.
    """
    pieces = []
    for line in text.split("\n"):
        line = line.strip()
        if not line:
            continue
        # split after . ! ? when followed by whitespace + a capital/quote/digit
        for sent in re.split(r"(?<=[.!?])\s+(?=[\"'A-Z0-9])", line):
            sent = sent.strip()
            if sent:
                pieces.append(sent)
    return pieces


def pack_with_overlap(sentences, budget):
    """
    Greedily pack sentences into windows of <= `budget` tokens. When a window fills,
    start the next one with the trailing ~OVERLAP_TOKENS of sentences so context carries
    across the boundary. Returns a list of body strings (no prefix yet).
    """
    windows = []
    current = []
    current_tokens = 0

    for sent in sentences:
        st = n_tokens(sent)
        # A single sentence longer than the budget can't be overlapped sensibly; emit it
        # on its own (the model will truncate it, which is unavoidable for one long sentence).
        if st >= budget:
            if current:
                windows.append(" ".join(current))
                current, current_tokens = [], 0
            windows.append(sent)
            continue

        if current_tokens + st > budget:
            windows.append(" ".join(current))
            # build the overlap tail from the end of the window just closed
            tail, tail_tokens = [], 0
            for prev in reversed(current):
                pt = n_tokens(prev)
                if tail_tokens + pt > OVERLAP_TOKENS:
                    break
                tail.insert(0, prev)
                tail_tokens += pt
            current = tail + [sent]
            current_tokens = tail_tokens + st
        else:
            current.append(sent)
            current_tokens += st

    if current:
        windows.append(" ".join(current))
    return windows


def chunk_text(text: str, prefix: str):
    """
    Turn one section's text into one or more prefixed chunks.

    `prefix` is the "Article > Section:" string. It is prepended to *every* chunk and
    counts against the token budget, so the body budget is MAX_TOKENS minus the prefix.
    """
    prefix_tokens = n_tokens(prefix + " ")

    if n_tokens(prefix + " " + text) <= MAX_TOKENS:
        return [f"{prefix} {text}".strip()]

    body_budget = MAX_TOKENS - prefix_tokens
    sentences = split_sentences(text)
    bodies = pack_with_overlap(sentences, body_budget)
    return [f"{prefix} {body}".strip() for body in bodies]


def chunk_document(doc):
    """Chunk every section of one loaded document into chunk dicts with metadata."""
    chunks = []
    title = doc["title"]
    for section in doc["sections"]:
        label = f"{title} > {section['section']}"
        prefix = f"{label}:"
        for body in chunk_text(section["text"], prefix):
            chunks.append({
                "text": body,
                "metadata": {
                    "source": title,
                    "section": section["section"],
                    "url": doc["url"],
                    "tokens": n_tokens(body),
                },
            })
    return chunks


def load_docs():
    files = sorted(DOCS_DIR.glob("*.json"))
    if not files:
        sys.exit("No documents found. Run `python ingest.py` first.")
    return [json.loads(f.read_text(encoding="utf-8")) for f in files]


def inspect(article_name):
    """Print every chunk for one article so you can eyeball size / prefix / metadata."""
    for doc in load_docs():
        if doc["title"].lower() == article_name.lower():
            for i, c in enumerate(chunk_document(doc)):
                print(f"\n--- chunk {i}  ({c['metadata']['tokens']} tokens) "
                      f"[section: {c['metadata']['section']}] ---")
                print(c["text"])
            return
    sys.exit(f"No article titled {article_name!r} in documents/.")


def sample(n=5):
    """
    Read chunks.json and print the total count, a health check, and a representative
    spread of chunks to eyeball. For each, ask yourself: does this make sense on its
    own? Could someone answer a question from this chunk alone?

    The spread is the smallest chunk, the largest chunk, and (n-2) evenly spaced across
    the corpus -- so you see the size extremes (where chunking usually goes wrong) plus
    typical cases from different articles.
    """
    if not OUT_FILE.exists():
        sys.exit("No chunks.json yet. Run `python chunk.py` first.")
    chunks = json.loads(OUT_FILE.read_text(encoding="utf-8"))
    sizes = [c["metadata"]["tokens"] for c in chunks]
    total = len(chunks)

    print(f"TOTAL CHUNKS: {total}  (healthy range for 10 docs: 50-2000)")
    if total < 50:
        print("  -> Below 50: chunks may be too LARGE (each covers too much to match precisely).")
    elif total > 2000:
        print("  -> Above 2000: chunks may be too SMALL (each carries too little meaning).")
    else:
        print("  -> In the healthy range.")
    print(f"Token size: min {min(sizes)}, max {max(sizes)}, avg {sum(sizes)//total}\n" + "=" * 70)

    smallest = min(range(total), key=lambda i: sizes[i])
    largest = max(range(total), key=lambda i: sizes[i])
    spread = max(1, total // (n - 1)) if n > 2 else total
    picks = [smallest, largest] + [i for i in range(0, total, spread)]
    seen, ordered = set(), []
    for i in picks:                       # dedupe, keep order, cap at n
        if i not in seen:
            seen.add(i)
            ordered.append(i)
    for i in ordered[:n]:
        c = chunks[i]
        tag = {smallest: "SMALLEST", largest: "LARGEST"}.get(i, "representative")
        print(f"\n### chunk {i} ({tag}) -- {c['metadata']['tokens']} tokens")
        print(f"    source={c['metadata']['source']!r}  section={c['metadata']['section']!r}")
        print(f"    {c['text']}\n" + "-" * 70)


def random_chunks(n=5, seed=None):
    """
    Read chunks.json and print n RANDOM chunks to eyeball. For each, ask: does this make
    sense on its own? Could someone answer a question from this chunk alone?

    Pass a seed to reproduce the same draw later (e.g. to cite exact chunks in a writeup):
        python chunk.py --random 5 42
    """
    if not OUT_FILE.exists():
        sys.exit("No chunks.json yet. Run `python chunk.py` first.")
    chunks = json.loads(OUT_FILE.read_text(encoding="utf-8"))

    rng = random.Random(seed)
    picks = rng.sample(range(len(chunks)), min(n, len(chunks)))

    print(f"TOTAL CHUNKS: {len(chunks)}   showing {len(picks)} random "
          f"(seed={seed})\n" + "=" * 70)
    for i in picks:
        c = chunks[i]
        print(f"\n### chunk {i} -- {c['metadata']['tokens']} tokens")
        print(f"    source={c['metadata']['source']!r}  section={c['metadata']['section']!r}")
        print(f"    {c['text']}\n" + "-" * 70)


def main():
    all_chunks = []
    for doc in load_docs():
        all_chunks.extend(chunk_document(doc))

    OUT_FILE.write_text(json.dumps(all_chunks, indent=2, ensure_ascii=False), encoding="utf-8")

    sizes = [c["metadata"]["tokens"] for c in all_chunks]
    over = sum(1 for s in sizes if s > MAX_TOKENS)
    print(f"Wrote {len(all_chunks)} chunks to {OUT_FILE}")
    print(f"Token size: min {min(sizes)}, max {max(sizes)}, "
          f"avg {sum(sizes) // len(sizes)}  (target <= {MAX_TOKENS})")
    print(f"Chunks over target (single long sentences): {over}")
    print('\nEyeball one article with:  python chunk.py --inspect "The Nether"')


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "--inspect":
        inspect(sys.argv[2])
    elif len(sys.argv) >= 2 and sys.argv[1] == "--sample":
        sample(int(sys.argv[2]) if len(sys.argv) >= 3 else 5)
    elif len(sys.argv) >= 2 and sys.argv[1] == "--random":
        n = int(sys.argv[2]) if len(sys.argv) >= 3 else 5
        seed = int(sys.argv[3]) if len(sys.argv) >= 4 else None
        random_chunks(n, seed)
    else:
        main()

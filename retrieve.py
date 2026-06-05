"""
Milestone 4 — Stage 4: Retrieval.

Defines retrieve(query, k=5): embed the query with the SAME model as the chunks, ask
ChromaDB for the k nearest chunks, and return them with their source metadata and cosine
distance (lower = more relevant).

Run:  python retrieve.py "How do I go to the Nether?"     # one query, top 5
      python retrieve.py --eval                           # all 5 planning.md eval questions
      python retrieve.py --eval 3                          # top 3 instead of 5
"""

import sys

from vectorstore import embed, get_collection

# Top-k from planning.md -> Retrieval Approach. 5 because many questions span multiple
# articles (e.g. "barter with piglins in the Nether" needs Piglin + Bartering + Nether).
DEFAULT_K = 5

# The 5 evaluation questions live in eval_questions.py (single source of truth).
from eval_questions import EVAL_QUESTIONS


def retrieve(query, k=DEFAULT_K):
    """Return the k chunks most relevant to `query`, nearest first."""
    collection = get_collection()
    result = collection.query(
        query_embeddings=embed([query]),
        n_results=k,
        include=["documents", "metadatas", "distances"],
    )
    hits = []
    for doc, meta, dist in zip(
        result["documents"][0], result["metadatas"][0], result["distances"][0]
    ):
        hits.append({
            "text": doc,
            "source": meta["source"],
            "section": meta["section"],
            "url": meta["url"],
            "distance": dist,
        })
    return hits


def print_hits(query, hits):
    print(f"\nQUERY: {query}")
    for rank, h in enumerate(hits, 1):
        flag = "" if h["distance"] < 0.5 else "  <-- weak (>0.5)"
        print(f"\n  {rank}. [{h['distance']:.3f}]{flag} {h['source']} > {h['section']}")
        print(f"     {h['text']}")           # full chunk text, so relevance is judgable


def main():
    args = sys.argv[1:]
    if args and args[0] == "--eval":
        k = int(args[1]) if len(args) > 1 else DEFAULT_K
        for q in EVAL_QUESTIONS:
            print_hits(q, retrieve(q, k))
        return
    if not args:
        sys.exit('Usage: python retrieve.py "your question"   (or --eval)')
    query = " ".join(args)
    print_hits(query, retrieve(query))


if __name__ == "__main__":
    main()

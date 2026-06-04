"""
Milestone 4 — Stage 3: Embedding + Vector Store.

Loads the chunks produced by chunker.py, embeds each one with all-MiniLM-L6-v2, and stores
the vectors in ChromaDB together with their metadata (source article, section, url, and
the chunk's position within its document). Run this once after chunking; re-run it whenever
chunks.json changes.

Run:  python embed.py
"""

import json
import sys
from pathlib import Path

from vectorstore import COLLECTION, DB_PATH, MODEL_NAME, embed, get_collection
import chromadb

CHUNKS_FILE = Path("chunks.json")


def load_chunks():
    if not CHUNKS_FILE.exists():
        sys.exit("No chunks.json. Run `python chunker.py` first.")
    return json.loads(CHUNKS_FILE.read_text(encoding="utf-8"))


def main():
    chunks = load_chunks()
    print(f"Embedding {len(chunks)} chunks with {MODEL_NAME}...")

    # Build the parallel lists ChromaDB wants. `position` is the chunk's index within its
    # own source article (0, 1, 2, ...), which we need later for source attribution.
    ids, documents, metadatas = [], [], []
    position_in_source = {}
    for i, c in enumerate(chunks):
        src = c["metadata"]["source"]
        pos = position_in_source.get(src, 0)
        position_in_source[src] = pos + 1

        ids.append(f"chunk-{i}")
        documents.append(c["text"])
        metadatas.append({
            "source": src,
            "section": c["metadata"]["section"],
            "url": c["metadata"]["url"],
            "position": pos,
        })

    embeddings = embed(documents)

    # Rebuild the collection from scratch so re-running never leaves stale chunks behind.
    client = chromadb.PersistentClient(path=DB_PATH)
    try:
        client.delete_collection(COLLECTION)
    except Exception:
        pass
    collection = get_collection()
    collection.add(ids=ids, embeddings=embeddings, documents=documents, metadatas=metadatas)

    print(f"Stored {collection.count()} vectors in ChromaDB at {DB_PATH}/ "
          f"(collection: {COLLECTION})")
    print('Test it with:  python retrieve.py "How do I go to the Nether?"')


if __name__ == "__main__":
    main()

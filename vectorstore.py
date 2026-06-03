"""
Milestone 4 — shared vector-store config.

Both embed.py (which stores chunks) and retrieve.py (which queries) import from here,
so the documents and the query are ALWAYS embedded with the exact same model. Embedding
the query with a different model than the chunks is the single most common retrieval bug,
and keeping the model in one place makes that mistake impossible.
"""

import chromadb
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"   # from planning.md -> Retrieval Approach
DB_PATH = "chroma_db"             # local, gitignored
COLLECTION = "minecraft_guide"

_model = None


def get_model():
    """Load the embedding model once and reuse it (loading is slow)."""
    global _model
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    return _model


def embed(texts):
    """Embed a list of strings into normalized vectors (as plain lists for ChromaDB)."""
    return get_model().encode(texts, normalize_embeddings=True).tolist()


def get_collection():
    """
    Open (or create) the ChromaDB collection.

    metadata={"hnsw:space": "cosine"} makes ChromaDB report COSINE distance, where
    0 = identical meaning and larger = less related. That is the scale the Milestone 4
    thresholds assume (good < 0.5, weak > 0.6-0.7).
    """
    client = chromadb.PersistentClient(path=DB_PATH)
    return client.get_or_create_collection(
        name=COLLECTION,
        metadata={"hnsw:space": "cosine"},
    )

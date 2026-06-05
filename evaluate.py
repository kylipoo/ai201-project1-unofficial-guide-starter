"""
Evaluation harness for the Minecraft RAG system. Runs the 5 eval questions through ask(),
scores each answer against its ground truth with answer-similarity (cosine of normalized
embeddings, so a dot product), and renders a Markdown report with blank manual-verdict fields.

Run:  python evaluate.py        # writes evaluation_report.md to the project root
"""

from eval_questions import EVAL_SET
from generate import ask
from retrieve import DEFAULT_K
from vectorstore import embed

REPORT_PATH = "evaluation_report.md"


def answer_similarity(answer, ground_truth):
    """Cosine similarity between answer and ground_truth.

    embed() returns L2-normalized vectors, so cosine similarity is the dot product.
    Higher = better (range ~0-1; normalized so the formula allows -1..1).
    Returns 0.0 if either argument is None or empty (no usable text to compare).
    """
    if not answer or not ground_truth:
        return 0.0
    vecs = embed([answer, ground_truth])
    a, b = vecs[0], vecs[1]
    return float(sum(x * y for x, y in zip(a, b)))

"""
Milestone 5 — Stage 5: Grounded Generation.

ask(question) retrieves the most relevant chunks, hands ONLY those chunks to the LLM as
context, and instructs it to answer from that context alone — or to refuse. The two
grounding guarantees this milestone cares about:

  1. Grounding is ENFORCED by the system prompt (answer only from context; refuse
     otherwise), and structurally by the fact that the model is given nothing but the
     retrieved chunks to work from.
  2. Source attribution is PROGRAMMATIC: the sources list is built in code from the
     retrieved chunks' metadata, never parsed out of (or trusted to) the LLM's answer.

Run:  python generate.py "How do I go to the Nether?"
"""

import os
import sys
from pathlib import Path

from dotenv import load_dotenv
from groq import Groq

from retrieve import DEFAULT_K, retrieve

load_dotenv(dotenv_path=Path(__file__).with_name(".env"))

# llama-3.3-70b-versatile (planning.md -> AI Tool Plan, M5). The smaller 8b-instant model
# made unstable grounding decisions on borderline questions — e.g. it refused "...without
# finding a village?" but answered the same question without the "?" — so we use the 70b
# model, which makes that judgment correctly and stably. (See generate.py debug, 2026-06.)
MODEL = "llama-3.3-70b-versatile"
# MODEL = "llama-3.1-8b-instant"   # faster/cheaper, but brittle on borderline grounding
REFUSAL = "I don't have enough information in my sources to answer that."

SYSTEM_PROMPT = f"""You are a helpful Minecraft guide. Answer the player's question using \
ONLY the information in the numbered context passages provided. Rules:
- Use only facts stated in the context. Do not add anything from your own knowledge,
  even if you are confident it is correct.
- Do not invent item names, block counts, timings, or steps that are not in the context.
- If the context does not contain enough information to answer, reply with exactly this
  sentence and nothing else: "{REFUSAL}"
- Be concise and practical, and write for a player who wants to know what to do."""

_client = None


def client():
    global _client
    if _client is None:
        _client = Groq(api_key=os.environ["GROQ_API_KEY"])
    return _client


def build_context(hits):
    """Format the retrieved chunks as a numbered context block for the prompt."""
    return "\n\n".join(
        f"[{i}] (from {h['source']} > {h['section']})\n{h['text']}"
        for i, h in enumerate(hits, 1)
    )


def sources_from(hits):
    """Unique source documents among the retrieved chunks, in retrieval order."""
    seen, out = set(), []
    for h in hits:
        if h["source"] not in seen:
            seen.add(h["source"])
            out.append(f"{h['source']} — {h['url']}")
    return out


def ask(question, k=DEFAULT_K):
    """Return {answer, sources, hits} for a question, grounded in retrieved chunks."""
    hits = retrieve(question, k)
    response = client().chat.completions.create(
        model=MODEL,
        temperature=0,   # deterministic; we want grounded recall, not creativity
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",
             "content": f"Context passages:\n\n{build_context(hits)}\n\nQuestion: {question}"},
        ],
    )
    answer = response.choices[0].message.content.strip()

    # Only attribute sources when the model actually answered. If it refused, listing
    # sources would falsely imply the documents covered the question.
    refused = REFUSAL.lower() in answer.lower() or answer.lower().startswith("i don't have")
    sources = [] if refused else sources_from(hits)

    return {"answer": answer, "sources": sources, "hits": hits}


def main():
    if len(sys.argv) < 2:
        sys.exit('Usage: python generate.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    print("\nANSWER:\n" + result["answer"])
    print("\nSOURCES:")
    for s in result["sources"]:
        print(f"  • {s}")
    if not result["sources"]:
        print("  (none — answered as 'not enough information')")


if __name__ == "__main__":
    main()

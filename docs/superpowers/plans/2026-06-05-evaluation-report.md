# Evaluation Report Feature Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a "Run Evaluation" capability to the Minecraft RAG app that runs the 5 test questions, shows the evidence on-screen, and exports a `evaluation_report.md` with blank manual-verdict fields.

**Architecture:** A single source-of-truth module (`eval_questions.py`) holds the 5 questions + ground-truth answers. `evaluate.py` runs each question through the existing `ask()` pipeline, computes an answer-similarity score via the existing `embed()` model, and renders a Markdown report. `app.py` gains an "Evaluation" tab that triggers the run, displays results, and writes the file. The existing Ask flow is untouched.

**Tech Stack:** Python, Gradio 4.44, sentence-transformers (all-MiniLM-L6-v2), ChromaDB, Groq, pytest (new dev dependency).

---

## File Structure

- **Create `eval_questions.py`** — `EVAL_SET` (5 dicts: id, question, ground_truth) and derived `EVAL_QUESTIONS`. Single source of truth.
- **Create `evaluate.py`** — `answer_similarity()`, `run_evaluation()`, `to_markdown()`, `main()`.
- **Modify `retrieve.py:21-28`** — import `EVAL_QUESTIONS` from `eval_questions` instead of the local copy.
- **Modify `app.py`** — wrap UI in `gr.Tabs`, add the "Evaluation" tab.
- **Modify `requirements.txt`** — add `pytest`.
- **Create `tests/test_evaluate.py`** — unit tests for the pure/near-pure functions.

---

## Task 1: Single source of truth — `eval_questions.py`

**Files:**
- Create: `eval_questions.py`
- Modify: `retrieve.py:21-28`
- Modify: `requirements.txt`
- Create: `tests/test_eval_questions.py`

- [ ] **Step 1: Add pytest to requirements and install**

Append to `requirements.txt`:

```text

# Testing (dev)
pytest>=8.0
```

Run: `.venv/bin/pip install pytest>=8.0`
Expected: pytest installs successfully.

- [ ] **Step 2: Write the failing test**

Create `tests/test_eval_questions.py`:

```python
from eval_questions import EVAL_SET, EVAL_QUESTIONS


def test_eval_set_has_five_complete_items():
    assert len(EVAL_SET) == 5
    for item in EVAL_SET:
        assert item["id"]
        assert item["question"].strip()
        assert item["ground_truth"].strip()


def test_eval_questions_derived_from_set():
    assert EVAL_QUESTIONS == [item["question"] for item in EVAL_SET]
    assert len(EVAL_QUESTIONS) == 5
```

- [ ] **Step 3: Run test to verify it fails**

Run: `.venv/bin/pytest tests/test_eval_questions.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'eval_questions'`

- [ ] **Step 4: Create `eval_questions.py`**

```python
"""
Single source of truth for the evaluation set: the 5 test questions and their ground-truth
answers (paraphrased from planning.md -> Evaluation Plan). retrieve.py and evaluate.py both
import from here so the questions are never duplicated.
"""

EVAL_SET = [
    {
        "id": 1,
        "question": "How do I go to the Nether in the first place?",
        "ground_truth": (
            "Build a nether portal from obsidian: a frame at least 4x5 (minimum 10 obsidian), "
            "then light the inside with a fire source like flint and steel. A purple portal "
            "appears; step into it and after a few seconds you arrive in the Nether."
        ),
    },
    {
        "id": 2,
        "question": "How do I get more villagers without finding a village?",
        "ground_truth": (
            "Two ways. Cure a zombie villager: trap one, splash it with a Potion of Weakness "
            "and feed it a golden apple, then wait for it to convert. Or breed existing "
            "villagers by giving them plenty of food (e.g. 12 carrots/potatoes/beetroot or "
            "3 bread) with unclaimed beds nearby so they enter breeding mode."
        ),
    },
    {
        "id": 3,
        "question": "How do I get ender pearls in the Nether? I can't find any Endermen.",
        "ground_truth": (
            "Two options. Find the warped forest (blue) biome where endermen spawn most often "
            "and kill them for pearls. Or barter with piglins: mine and craft gold ingots, "
            "then give/throw them to piglins, who sometimes return ender pearls in exchange."
        ),
    },
    {
        "id": 4,
        "question": "How do I get that cool pair of wings that lets me fly?",
        "ground_truth": (
            "The Elytra. Go to the End and defeat the Ender Dragon, take an exit portal on the "
            "outer edge to the End islands, explore until you find an End City with an End Ship, "
            "and grab the Elytra displayed in the ship."
        ),
    },
    {
        "id": 5,
        "question": "What is the enchantment that lets me automatically repair my items?",
        "ground_truth": (
            "Mending. It's a treasure enchantment (not available on the enchanting table) found "
            "via loot, fishing, or trading with a librarian villager for the enchanted book; "
            "it repairs the item using collected experience orbs."
        ),
    },
]

EVAL_QUESTIONS = [item["question"] for item in EVAL_SET]
```

- [ ] **Step 5: Refactor `retrieve.py` to import from the source of truth**

In `retrieve.py`, replace the local `EVAL_QUESTIONS` list (lines 21-28, the comment + the list literal) with:

```python
# The 5 evaluation questions live in eval_questions.py (single source of truth).
from eval_questions import EVAL_QUESTIONS
```

Keep `DEFAULT_K = 5` where it is. Place the import near the top with the other imports if preferred, but a local import here is acceptable to keep the diff minimal.

- [ ] **Step 6: Run tests + verify retrieve still works**

Run: `.venv/bin/pytest tests/test_eval_questions.py -v`
Expected: PASS (2 passed)

Run: `.venv/bin/python -c "from retrieve import EVAL_QUESTIONS; print(len(EVAL_QUESTIONS))"`
Expected: prints `5`

- [ ] **Step 7: Commit**

```bash
git add eval_questions.py retrieve.py requirements.txt tests/test_eval_questions.py
git commit -m "feat: add eval_questions.py as single source of truth for eval set"
```

---

## Task 2: Answer-similarity score — `evaluate.py`

**Files:**
- Create: `evaluate.py`
- Test: `tests/test_evaluate.py`

- [ ] **Step 1: Write the failing test**

Create `tests/test_evaluate.py`:

```python
from evaluate import answer_similarity


def test_identical_text_scores_near_one():
    s = answer_similarity("Build a nether portal from obsidian.",
                          "Build a nether portal from obsidian.")
    assert s > 0.99


def test_related_text_scores_higher_than_unrelated():
    gt = "Build a nether portal from obsidian and light it."
    related = answer_similarity("You make a portal out of obsidian and light it on fire.", gt)
    unrelated = answer_similarity("Breed villagers by giving them carrots.", gt)
    assert related > unrelated


def test_score_is_float_in_range():
    s = answer_similarity("anything", "something else")
    assert isinstance(s, float)
    assert -1.0 <= s <= 1.0
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/test_evaluate.py -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'evaluate'`

- [ ] **Step 3: Create `evaluate.py` with `answer_similarity`**

```python
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
    """
    vecs = embed([answer or "", ground_truth or ""])
    a, b = vecs[0], vecs[1]
    return float(sum(x * y for x, y in zip(a, b)))
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/test_evaluate.py -v`
Expected: PASS (3 passed). Note: first run loads the MiniLM model, so it may take a few seconds.

- [ ] **Step 5: Commit**

```bash
git add evaluate.py tests/test_evaluate.py
git commit -m "feat: add answer_similarity scoring in evaluate.py"
```

---

## Task 3: Markdown rendering — `to_markdown`

**Files:**
- Modify: `evaluate.py`
- Test: `tests/test_evaluate.py`

- [ ] **Step 1: Add the failing test**

Append to `tests/test_evaluate.py`:

```python
from evaluate import to_markdown


def _sample_results():
    return [{
        "id": 1,
        "question": "How do I go to the Nether?",
        "ground_truth": "Build an obsidian portal and light it.",
        "answer": "Make a portal from obsidian and light it with flint and steel.",
        "answer_similarity": 0.81,
        "hits": [
            {"text": "A nether portal is built as a frame of obsidian...",
             "source": "Nether", "section": "Creation",
             "url": "https://example.com/Nether", "distance": 0.21},
        ],
    }]


def test_markdown_contains_question_scores_and_verdicts():
    md = to_markdown(_sample_results())
    assert "How do I go to the Nether?" in md
    assert "Build an obsidian portal and light it." in md   # ground truth
    assert "0.81" in md                                     # answer-similarity
    assert "0.21" in md                                     # chunk distance
    assert "https://example.com/Nether" in md               # source url
    assert md.lower().count("verdict") >= 2                 # retrieval + response verdicts
    assert "higher = better" in md                          # similarity legend
    assert "lower = better" in md                           # distance legend
    assert "## Failure Case" in md                          # failure-case section
```

- [ ] **Step 2: Run test to verify it fails**

Run: `.venv/bin/pytest tests/test_evaluate.py::test_markdown_contains_question_scores_and_verdicts -v`
Expected: FAIL with `ImportError: cannot import name 'to_markdown'`

- [ ] **Step 3: Add `to_markdown` to `evaluate.py`**

```python
def _render_chunk(rank, hit):
    snippet = hit["text"].replace("\n", " ").strip()
    if len(snippet) > 200:
        snippet = snippet[:200] + "..."
    return (f'{rank}. [dist {hit["distance"]:.3f}] {hit["source"]} > {hit["section"]} '
            f'— "{snippet}" ({hit["url"]})')


def _render_result(r):
    chunks = "\n".join(_render_chunk(i, h) for i, h in enumerate(r["hits"], 1))
    return f"""### Q{r['id']} — {r['question']}

**Ground truth:** {r['ground_truth']}

**System answer:** {r['answer']}

**Answer-similarity:** {r['answer_similarity']:.2f}  (higher = better, range 0-1)

**Retrieved chunks** (distance: lower = better, <0.5 = strong):
{chunks}

**Retrieval verdict:** _[ accurate / partial / inaccurate ]_
**Response verdict:** _[ accurate / partial / inaccurate ]_
**Notes:** _____
"""


def to_markdown(results):
    """Render evaluation results as the submission report with blank manual-verdict fields."""
    header = (
        "# Evaluation Report — The Unofficial Minecraft Guide\n\n"
        "Generated by `evaluate.py`. Verdicts and the failure-case analysis are filled in "
        "manually.\n\n"
        "Scores legend:\n"
        "- Answer-similarity: higher = better (range 0-1).\n"
        "- Retrieval distance: lower = better (<0.5 = strong match).\n"
    )
    body = "\n---\n\n".join(_render_result(r) for r in results)
    failure = (
        "\n---\n\n## Failure Case\n\n"
        "_Pick the weakest result above and explain why it failed — e.g. vocabulary mismatch "
        "between the casual question and wiki jargon, a chunk boundary that split the answer, "
        "off-topic retrieval, or a low-similarity answer. Reference the scores as evidence._\n"
    )
    return f"{header}\n---\n\n{body}\n{failure}"
```

- [ ] **Step 4: Run test to verify it passes**

Run: `.venv/bin/pytest tests/test_evaluate.py -v`
Expected: PASS (4 passed)

- [ ] **Step 5: Commit**

```bash
git add evaluate.py tests/test_evaluate.py
git commit -m "feat: render evaluation results to markdown report"
```

---

## Task 4: Run the full evaluation — `run_evaluation` + CLI

**Files:**
- Modify: `evaluate.py`

- [ ] **Step 1: Add `run_evaluation` and `main` to `evaluate.py`**

```python
def run_evaluation(k=DEFAULT_K):
    """Run every eval question through ask() and score it. Returns a list of result dicts."""
    results = []
    for item in EVAL_SET:
        out = ask(item["question"], k)
        results.append({
            "id": item["id"],
            "question": item["question"],
            "ground_truth": item["ground_truth"],
            "answer": out["answer"],
            "answer_similarity": answer_similarity(out["answer"], item["ground_truth"]),
            "hits": out["hits"],
        })
    return results


def main():
    results = run_evaluation()
    report = to_markdown(results)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"Wrote {REPORT_PATH} ({len(results)} questions).")
    for r in results:
        print(f"  Q{r['id']}: answer-similarity {r['answer_similarity']:.2f}")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Integration smoke test (manual — needs GROQ_API_KEY + built chroma_db)**

Run: `.venv/bin/python evaluate.py`
Expected: prints `Wrote evaluation_report.md (5 questions).` followed by 5 similarity lines, and `evaluation_report.md` exists in the project root with all 5 questions, the score legends, two verdict placeholders per question, and the `## Failure Case` section.

Verify: `grep -c "verdict" evaluation_report.md` → expect `10` (2 per question). Open the file and confirm chunk URLs are present and clickable.

- [ ] **Step 3: Commit**

```bash
git add evaluate.py
git commit -m "feat: add run_evaluation pipeline and CLI entrypoint"
```

---

## Task 5: "Evaluation" tab in the Gradio app

**Files:**
- Modify: `app.py`

- [ ] **Step 1: Add the import and handler**

In `app.py`, add to the imports at the top:

```python
from evaluate import run_evaluation, to_markdown, REPORT_PATH
```

Add this handler function alongside `handle_query`:

```python
def handle_evaluation():
    try:
        results = run_evaluation()
    except Exception as e:  # API/key/collection errors — surface, don't write a half report
        return f"Evaluation failed: {e}"
    report = to_markdown(results)
    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        f.write(report)
    scores = "  ·  ".join(f"Q{r['id']} {r['answer_similarity']:.2f}" for r in results)
    return f"Wrote `{REPORT_PATH}`.  Answer-similarity (higher = better): {scores}\n\n{report}"
```

- [ ] **Step 2: Wrap the existing UI in tabs and add the Evaluation tab**

In `app.py`, restructure the `gr.Blocks` body so the current Ask UI lives in one tab and the new evaluation UI in a second. Replace the existing `with gr.Blocks(...) as demo:` body so it reads:

```python
with gr.Blocks(title="The Unofficial Minecraft Guide") as demo:
    with gr.Tabs():
        with gr.Tab("Ask"):
            gr.Markdown(
                "# The Unofficial Minecraft Guide\n"
                "Ask about mobs, dimensions, structures, and mechanics. "
                "Answers come **only** from the ingested Minecraft Wiki pages — if the guide "
                "doesn't cover it, the assistant says so instead of guessing."
            )
            inp = gr.Textbox(label="Your question", placeholder="How do I go to the Nether?")
            btn = gr.Button("Ask", variant="primary")
            answer = gr.Textbox(label="Answer", lines=8)
            sources = gr.Textbox(label="Retrieved from", lines=4)

            btn.click(handle_query, inputs=inp, outputs=[answer, sources])
            inp.submit(handle_query, inputs=inp, outputs=[answer, sources])

            gr.Examples(
                examples=[
                    "How do I go to the Nether in the first place?",
                    "How do I get more villagers without finding a village?",
                    "What is the enchantment that lets me automatically repair my items?",
                ],
                inputs=inp,
            )

        with gr.Tab("Evaluation"):
            gr.Markdown(
                "# Evaluation\n"
                "Runs all 5 test questions, scores each answer against its ground truth "
                "(**answer-similarity: higher = better**), and writes `evaluation_report.md` "
                "with blank verdict fields for manual judgment. Retrieval distances shown per "
                "chunk are **lower = better**."
            )
            eval_btn = gr.Button("Run Evaluation", variant="primary")
            eval_out = gr.Markdown()
            eval_btn.click(handle_evaluation, inputs=None, outputs=eval_out)
```

Leave the `if __name__ == "__main__": demo.launch()` block unchanged.

- [ ] **Step 3: Manual end-to-end test**

Run: `.venv/bin/python app.py`
Then open http://localhost:7860, click the **Evaluation** tab, click **Run Evaluation**.
Expected: after a few seconds the panel shows the confirmation line + the rendered report (5 questions, each with answer-similarity and retrieved chunks with URLs), and `evaluation_report.md` is written/updated on disk. Confirm the **Ask** tab still works as before.

- [ ] **Step 4: Commit**

```bash
git add app.py
git commit -m "feat: add Evaluation tab with Run Evaluation button"
```

---

## Self-Review Notes

- **Spec coverage:** ground-truth source of truth (Task 1) · answer-similarity score, higher=better labeling (Task 2) · per-chunk distance + URL, lower=better labeling, two verdict fields, failure-case section (Task 3) · run pipeline + file export (Task 4) · Evaluation tab + on-screen display + error handling for missing key/collection (Task 5). All spec sections mapped.
- **Naming consistency:** `run_evaluation`, `to_markdown`, `answer_similarity`, `REPORT_PATH`, `EVAL_SET`, `EVAL_QUESTIONS` used identically across tasks and imports.
- **Note on similarity bar:** the spec mentioned an optional on-screen similarity bar; the rendered Markdown shows the numeric score with its "higher = better" legend, which satisfies the directionality requirement without extra UI. Dropped the ASCII bar as YAGNI.

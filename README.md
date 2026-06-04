# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | | | |
| 2 | | | |
| 3 | | | |
| 4 | | | |
| 5 | | | |
| 6 | | | |
| 7 | | | |
| 8 | | | |
| 9 | | | |
| 10 | | | |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:**

**Overlap:**

**Why these choices fit your documents:**

**Final chunk count:**

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:**

**Production tradeoff reflection:**

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:**

**How source attribution is surfaced in the response:**

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

This failure was found during testing, diagnosed to a specific pipeline stage, fixed, and
re-verified. The "found → fixed → verified" trail is below.

**Question that failed:** "What is the enchantment that lets me automatically repair my
items?" (my evaluation question #5; the answer is Mending). I also hit the same wall asking
about specific enchantments from the "List of enchantments" — they returned *"I don't have
enough information in my sources to answer that."*

**What the system returned (before the fix):** A refusal. Searching the chunks showed why:
the only place "Mending" appeared in the whole Enchantment document was a conflict list
(*"Bow: Infinity and Mending"*) — the corpus said Mending *exists* but never what it *does*.
The same defect produced content-free "stub" chunks elsewhere, e.g. *"…each trial chambers
ominous vault contains items drawn from 3 pools, with the following distribution:"* and then
nothing. A corpus-wide scan found **19 of 233 chunks (~8%)** were these dangling stubs,
concentrated in **Trial Chambers (13)**.

**Root cause (tied to a specific pipeline stage):** Ingestion. `ingest.py` deleted every
`<table>` element to keep the text clean — but on minecraft.wiki the real loot and the
per-enchantment descriptions live *inside* those tables. The lead-in sentence (a normal
`<p>`) survived; the table it pointed to was deleted, leaving a reference to data that was
no longer there.

**The fix (and why the first approach was wrong):** Instead of deleting tables, flatten
each content table (`wikitable`) into `col | col | col` text rows so the data survives as
embeddable content. This also required rewriting the ingestion walk from a flat scan of the
page's *direct* children to a **recursive descent** of the whole document tree — many
tables (17 in Trial Chambers) are nested inside wrapper `<div>`s, so the flat walk never
reached them. (Note: the AI tool's first ingestion design deleted tables outright; the
recursive, table-preserving parse is the model I should have specified up front — see AI
Usage.)

**Verification (after the fix):** Dangling stubs dropped from **19/233 to 2/399** chunks,
and question #5 now answers correctly — *"The enchantment that lets you automatically repair
your items is Mending,"* sourced to the Enchantment page. Other List-of-enchantments
questions (Silk Touch, Smite, Frost Walker) now answer correctly too, and the previously
working questions (Nether access, villager breeding) did not regress.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

**One way your implementation diverged from the spec, and why:**

---

## AI Usage

<!-- Describe at least 2 specific instances where you used an AI tool during this project.
     For each: what did you give the AI as input, what did it produce, and what did you
     change, override, or direct differently?

     "I used Claude to help me code" is not sufficient.
     "I gave Claude my Chunking Strategy section from planning.md and asked it to implement
     chunk_text(). It returned a function using a fixed character split. I overrode the
     chunk size from 500 to 200 because my documents are short reviews, not long guides." -->

**Instance 1 — ingestion (and where the AI got it wrong)**

- *What I gave the AI:* my Documents list and Chunking Strategy from planning.md, plus
  stages 1–2 of the pipeline diagram, and asked it to write a script that fetches and
  cleans the 10 wiki articles into structured documents.
- *What it produced:* an `ingest.py` that pulls each page via the MediaWiki API, strips
  page furniture, and splits the article by its section headers. To "keep the text clean"
  it deleted every HTML `<table>`.
- *What I changed or overrode:* deleting tables was the wrong call, and it caused my
  Failure Case above — the enchantment descriptions and Trial Chambers loot live *inside*
  those tables, so questions about them returned "not enough information." In hindsight I
  should have specified the parsing model up front: the AI's flat parse only read the
  page's direct children, when what this wiki needs is a **recursive** parse that descends
  into nested wrappers and **flattens** content tables into text instead of discarding
  them. I directed that change; stubs fell from 19/233 to 2/399 and the failing
  enchantment questions started answering correctly.

**Instance 2 — grounded generation**

- *What I gave the AI:* my Retrieval Approach section and stage 5 of the diagram, with the
  requirement that answers come only from retrieved chunks and that sources are attributed.
- *What it produced:* a `generate.py` that passes the top-k chunks to Groq's
  llama-3.3-70b as context with a system prompt instructing it to answer only from that
  context and refuse otherwise.
- *What I changed or overrode:* I made source attribution **programmatic** — the source
  list is built in code from the retrieved chunks' metadata, not parsed out of the LLM's
  answer — so attribution can't be hallucinated. I verified grounding by asking a question
  my corpus doesn't cover ("how do I tame a horse?"); the system correctly refused instead
  of answering from the model's training knowledge.

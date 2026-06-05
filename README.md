# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section _after_ you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

<!-- What topic or category of knowledge does your system cover?
     Why is this knowledge valuable, and why is it hard to find through official channels?
     Example: "Student reviews of CS professors at [university] — useful because official
     course descriptions don't reflect teaching style, exam difficulty, or workload." -->

---

The domain that I chose is Minecraft information, hoping to be able to quickly answer questions about various content like the mobs, structures, dimensions and how to access them. This knowledge is particularly valuable because Minecraft is a game that's consistently being updated, each old feature is eventually given a use, and there aren't really any reliable official channels that can keep up (The wiki that I referred to has stated explicitly it's not actually sponsored by Mojang, it's a fandom project). From personal experience I did have some Minecraft guidebooks from over 10 years back, but that information is obviously outdated, and it would be a hassle for someone to rely on that for gameplay. In addition, the games themselves don't really have much of a tutorial after the basic opening inventory and getting a crafting table phase.

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| #   | Source | Type | URL or file path |
| --- | ------ | ---- | ---------------- |
| 1   |        |      |                  |
| 2   |        |      |                  |
| 3   |        |      |                  |
| 4   |        |      |                  |
| 5   |        |      |                  |
| 6   |        |      |                  |
| 7   |        |      |                  |
| 8   |        |      |                  |
| 9   |        |      |                  |
| 10  |        |      |                  |

---

1. Villagers
   1. Information on where do Minecraft villagers spawn, what use they have for a survival player (very good for trading and obtaining rare resources) and how to make more villagers.
   2. Website
   3. URL here: https://minecraft.wiki/w/Villager
2. Piglins
   1. Piglins are another important mob for gathering rare. resources, but they're distinct from villagers in that the players need a more specific set of requirements to find a Piglin
   2. Website
   3. https://minecraft.wiki/w/Piglin
3. Bartering
   1. Related to the previous URL on the piglins, bartering is a mechanic where the player throws a gold ingot at a Piglin and they will automatically pick it up, inspect it, and return a randomized item to the player.
   2. Website
   3. https://minecraft.wiki/w/Bartering
4. Ender Dragon
   1. The Ender Dragon is the final boss of Minecraft, it would be helpful for the player to know what its gameplay loop is, such as how it moves, what attacks to watch out for and what structures in the boss fight would be vital to look out for.
   2. Website
   3. https://minecraft.wiki/w/Ender_Dragon
5. Illagers
   1. Illagers are a type of hostile mob where after the player completes a certain set of conditions, they spawn in raids that occur in villages and should the player be successful in fending off the raid, they are rewarded with valuable resources.
   2. Website
   3. https://minecraft.wiki/w/Illager
6. Enchantments
   1. This game mechanic allows the player to enhance their equipment (weapons, tools, armor) to be more effective at their intended purpose. There are a wide range of possible enchantments, but the conditions to getting one are worthy of lots of analysis, plus there's cases in which enchantments are incompatible, yet Minecraft itself doesn't explicitly spell it out loud.
   2. Website
   3. https://minecraft.wiki/w/Enchantment
7. Slimes
   1. Slimes are a type of mob who drop slime balls upon death, a material that is useful in redstone, construction, brewing. Though from my own personal experience I've never been able to find a lot of slimes or figure out how to make the conditions right for them to spawn. I would hope for this project to help simplify the info by chunking.
   2. Website
   3. https://minecraft.wiki/w/Slime
8. The end
   1. The final boss dimension. The player needs to fight the Ender Dragon, then upon its defeat, unlock portals to go to end cities, which have an abundance of important resources.
   2. Website
   3. https://minecraft.wiki/w/The_End
9. The nether
   1. The precursor to the end. A hellish dimension filled with hostile mobs, new blocks and new structures. The player needs to go to this dimension to get some majorly important resources like blaze powder, netherrack blocks, quartz blocks, nether bricks, ender pearls.
   2. Website
   3. https://minecraft.wiki/w/The_Nether
10. Trial Chambers
    1. An uncommon underground structure where the player is given minigames that they need to pass to obtain very handy resources. I wasn't playing Minecraft at the time of these structures being added, so this is also a new learning experience for me.
    2. Website
    3. https://minecraft.wiki/w/Trial_Chambers

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

Chunk size: 250
Overlap tokens: 45.

Why these choices fit my document: The Minecraft wiki articles are a good fit for this size because they're already broken into clear sections with headers (e.g. "Accessing", "Traits", "Mobs", "Biomes"). Rather than cutting blindly every 250 tokens, I'll split on those headers first so each chunk stays about one topic, and only sub-split the longer sections (like Environment) down to the ~250 token target. I'll also prepend the article title and section name to each chunk (like "The Nether > Mobs:") so a chunk keeps its context even when the raw sentence doesn't mention the dimension by name.

The 40-50 token (1-2 sentence) overlap is mainly for those sub-splits inside long sections. It keeps a fact from getting cut in half right at a boundary. I'm keeping the overlap small because splitting on headers already gives clean topical breaks, so I don't need heavy overlap the way a wall-of-text FAQ would.

Final chunk count: 380 chunks written to chunks.json.

### Sample chunks

Five representative chunks from `chunks.json`, each labeled with its source document and section. Every chunk is prefixed with its "Article > Section:" breadcrumb so it stays self-contained even out of context:

1. **The Nether** — _Accessing_ (217 tokens)

   > The Nether > Accessing: To access the Nether, the player must construct a Nether portal in the Overworld (portals created in the End do not activate). To create the portal, the player must first build a rectangular obsidian frame, ranging in size from a minimum of 4 blocks × 5 blocks to a maximum of 23 blocks × 23 blocks. Once the frame is completed, it can then be activated by placing fire within the frame, using flint and steel, fire charge, dispensers, or any material that is capable of igniting fire…

2. **Enchantment** — _Obtaining_ (217 tokens)

   > Enchantment > Obtaining: … An enchanting table can be used to enchant unenchanted items, consuming lapis lazuli and experience levels in the process. The player can only choose one of three randomly generated enchantments to apply to the item…

3. **Bartering** — _Mechanics_ (199 tokens)

   > Bartering > Mechanics: If the game rule mobGriefing is false, piglins barter only when the player uses a gold ingot on them. In Java Edition, if a piglin is zombified into a zombified piglin before the bartering is complete, the newly-zombified piglin drops the gold ingot immediately…

4. **Villager** — _Spawning > Natural generation_ (104 tokens)

   > Villager > Spawning > Natural generation: … The zombie villager can [change profession] after being cured. … The zombie villager is unemployed immediately after being cured, so the player cannot lock in its profession.

5. **Trial Chambers** — _(introduction)_ (152 tokens)
   > Trial Chambers > (introduction): Trial chambers are uncommon underground structures that serve as a mid-game combat challenge. They consist mostly of copper blocks and tuff bricks, and are the only place where trial spawners and vaults naturally generate…

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2

**Production tradeoff reflection:**

---

**Model used:** all-MiniLM-L6-v2, as it is a fast, lightweight, well-established general-purpose embedding model that runs entirely on my machine with no need for an API key, rate limits or per-call cost, which suited the 10 document nature of this project. Its 256 token cap also helped to structure my pipeline.

**Production tradeoff reflection:**
Going to production, I'd weigh four tradeoffs against my current choice of all-MiniLM-L6-v2:

Domain accuracy is my biggest concern. MiniLM is a small general-purpose model and it failed on the colloquial-to-jargon mapping real players use — it couldn't connect "wings that let me fly" → Elytra, or "ender pearls in the Nether" → piglin bartering. A stronger model (OpenAI text-embedding-3-large, or BGE/E5-large locally) has richer semantic associations and would likely rank the right chunk higher; the ceiling option is fine-tuning on Minecraft text.

Context length — MiniLM only embeds the first 256 tokens, which forced my small chunks and means multi-step answers get fragmented across chunks (e.g. the gold-ore → ingot → barter → ender-pearl chain spans several chunks). A 512–8k-token model would let each chunk carry more of that process in one vector.

Latency and local-vs-API hosting — MiniLM's real strength is that it's tiny, local, free, and near-instant, with no network dependency and no user data leaving the machine. A hosted SOTA model gives the best accuracy but adds per-call cost, network latency, an external dependency, and a privacy consideration. For an interactive Q&A tool I'd benchmark this rather than assume bigger is better. Preferably for something on retrieving game information, I'd prefer a larger depth of explanation instead of instant retrieval.

Multilingual support — MiniLM-L6-v2 is English-only. Minecraft has a global playerbase, so for real users I'd switch to a multilingual model (multilingual-E5, paraphrase-multilingual-MiniLM) to handle non-English questions.

## Retrieval

I retrieve the **top-5** chunks per query, ranked by cosine distance (lower = more relevant), embedding the query with the same all-MiniLM-L6-v2 model that embedded the chunks. Three examples, showing the query and the chunks actually returned:

**Example 1 — "How do I go to the Nether?"**

| Rank | Distance | Source > Section            |
| ---- | -------- | --------------------------- |
| 1    | 0.446    | The Nether > Accessing      |
| 2    | 0.498    | The Nether > Environment    |
| 3    | 0.513    | The Nether > Accessing      |
| 4    | 0.527    | The Nether > Traits         |
| 5    | 0.555    | The Nether > (introduction) |

_Why these are relevant:_ all five chunks come from the correct article (The Nether), and the two strongest hits are the "Accessing" section — exactly the part that explains how to build and activate a portal. The answer-bearing section landed at rank #1 (0.446, a strong match), so the generator had the right context to work from.

**Example 2 — "What are ways I can enchant my equipment?"**

| Rank | Distance | Source > Section                                                     |
| ---- | -------- | -------------------------------------------------------------------- |
| 1    | 0.465    | Enchantment > List of enchantments > Summary of enchantments by item |
| 2    | 0.466    | Enchantment > Obtaining                                              |
| 3    | 0.466    | Enchantment > List of enchantments > Summary of enchantments by item |
| 4    | 0.486    | Enchantment > Obtaining                                              |
| 5    | 0.490    | Enchantment > List of enchantments > Summary of enchantments by item |

_Why these are relevant:_ every chunk is from the Enchantment article, and the "Obtaining" sections (ranks 2 and 4) directly list the ways to enchant — enchanting table, anvil, trading, fishing, loot. The distances are tightly clustered (0.465–0.490), which is what good retrieval on a well-covered question looks like.

**Example 3 — "How do I get more villagers without finding a village?"**

| Rank | Distance | Source > Section                             |
| ---- | -------- | -------------------------------------------- |
| 1    | 0.439    | Villager > (introduction)                    |
| 2    | 0.462    | Villager > Behavior > Breeding > Willingness |
| 3    | 0.469    | Villager > Schedules > Returning home        |
| 4    | 0.473    | Villager > Behavior > Breeding               |
| 5    | 0.479    | Villager > Trading > Economic trade          |

Retrieval pulled the right article and the breeding sections (ranks 2 and 4), which cover one valid answer (breeding). The _curing-a-zombie-villager_ path never surfaced in the top-5 — see the Evaluation Report (Q2) and Failure Case for why.

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

**System prompt grounding instruction:**
The model is given nothing but the previously-retrieved chunks to work from. The user message is built as "Context passages:\n\n{context}\n\nQuestion: {Question}", there is no other source of information in the call.

Also context is formatted as numbered, attributed passages. build_context() renders each chunk as [1] From Nether > Accessing\n<text>, so the model can see discrete, labeled sources rather than a blurb.

**How source attribution is surfaced in the response:**
Programmatic, not parsed from LLM answer, meaning that citation can never be hallucinated. After generation, I integrated a sources_from(hits) function which will build the source list in code directly from each retrieved chunk's metadata. The model is not permitted to name its own sources.

1. Here is an example when I asked about enchanting equipment, it has a clear source pointing to the minecraft wiki's article on enchanting.

![alt text](<Screenshot 2026-06-05 at 3.38.55 PM.jpg>)

2. Here is another example when I asked about getting more villagers.

![alt text](<Screenshot 2026-06-05 at 3.45.04 PM.jpg>)

3. Example of an out of scope query

![alt text](<Screenshot 2026-06-05 at 3.53.04 PM.jpg>)

## Query Interface

The interface is a minimal Gradio web app ([app.py](app.py), run with `python app.py`, served at `http://localhost:7860`).

**Input field:**

- _"Your question"_ — a single textbox where the user types a natural-language question. Submitting it (the **Ask** button, or pressing Enter) runs the full retrieve → generate pipeline. A row of clickable example questions is provided to try.

**Output fields:**

- _"Answer"_ — the grounded answer assembled from the retrieved chunks, or the refusal sentence (_"I don't have enough information in my sources to answer that."_) if the guide doesn't cover the question.
- _"Retrieved from"_ — the list of source documents the answer was drawn from (article name + wiki URL), built programmatically from the retrieved chunks' metadata. On a refusal this field is empty, so the interface never implies a source it didn't actually use.

**Sample interaction (a complete query → response):**

> **Your question:** How do I go to the Nether?
>
> **Answer:** To go to the Nether, you must construct a Nether portal in the Overworld by building a rectangular obsidian frame (minimum 4×5 blocks, maximum 23×23 blocks) and then activate it by placing fire within the frame. Stand in the portal for 4 seconds to enter the Nether.
>
> **Retrieved from:**
>
> - The Nether — https://minecraft.wiki/w/The_Nether

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| #   | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
| --- | -------- | --------------- | ---------------------------- | ----------------- | ----------------- |
| 1   |          |                 |                              |                   |                   |
| 2   |          |                 |                              |                   |                   |
| 3   |          |                 |                              |                   |                   |
| 4   |          |                 |                              |                   |                   |
| 5   |          |                 |                              |                   |                   |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

1. Question: "How do I go to the Nether?"
   1. My expected answer was that I would need to create a Nether Portal. Which do to so, would require at least 10 blocks of Obsidian, constructed in a square frame pattern, as well as a fire source (flint and steel, fire charge) which when lit in the center of the frame, would generate the portal.
   2. System response: "To enter the Nether, you must construct a Nether portal in the Overworld. To create the portal, build a rectangular obsidian frame (minimum 4 blocks × 5 blocks, maximum 23 blocks × 23 blocks) and then activate it by placing fire within the frame using flint and steel, fire charge, dispensers, or any material that can ignite fire. In Survival mode, stand in the portal for 4 seconds to enter the Nether."
   3. Relevant.My question was related to the Nether, the app says that the source it looked at was the Nether article.
   4. Response accuracy: Accurate. I can verify that as a veteran Minecraft player myself, that this is exactly how you build a Nether Portal.
2. Question: "How do I get more villagers without finding a village?"
   1. My expected answer: I can either breed a villager or cure a zombie villager. Breeding villagers would require 3 bread,12 carrots, 12 potatoes or 12 beetroots and an unclaimed bed for the baby villager's home, curing a zombie villager would need to throw weakness potion and use golden apple on them.
   2. System response: To get more villagers without finding a village, you need to breed them. Villagers must be willing to breed, which is determined by the amount of food items they have. You can make them willing by giving them 3 bread, 12 carrots, 12 potatoes, or 12 beetroots. They also need unclaimed beds with at least two empty blocks above their heads to spawn baby villagers.
   3. Retrieval quality: Relevant
   4. Response accuracy: Partially accurate. I suspect that the reason the zombie villager point isn't under the same labeling as breeding villagers. "Get more" is semantically a question of reproduction rather than finding.
3. Question: "How do I get that cool pair of wings that lets me fly?"
   1. Expected answer: The wings you're thinking of are the Elytra, which you will get through End ships, an uncommon structure found near End cities. In order to find End cities, you'll need to first beat the Ender Dragon and then you can go through the portals that are spawned. Build up to the End ship, kill the Shulkers, then break the item frame with the Elytra and you can now fly:
   2. System response: I don't have enough information.
   3. Retrieval quality: Relevant. Couldn't find a source which when considering how the sources are chunked, makes sense.
   4. Response accuracy: inaccurate. The system refused because of a vocabulary mismatch: The query named the item by its description (wings that let me fly) while the source uses the term Elytra and not the words wing or fly. I went back and tried a different query: "How do I get that cool pair of wings the Elytra that lets me fly?" and this time it correctly narrowed down the source to "The end" and gave me the steps to get to the End City.
4. Question: "How do I get ender pearls in the Nether? I can't find any Endermen."
   1. Expected answer: Piglin bartering with gold can give 2-4 ender pearls at a time.
   2. System response: I don't have enough information.
   3. Retrieval quality: Off-target
   4. Response accuracy: Inaccurate. My query is built from "ender pearls," "Nether," and "can't find any Endermen." But in Minecraft lore, "ender pearls" and "Endermen" co-occur most strongly with The End dimension — so the embedding pulls in four "The End / Ender Dragon" chunks, which are about where pearls normally come from, not how to get them another way. The real answer is indexed under a totally different vocabulary — "bartering" / "piglin" — words my query never contains.
5. Question: "What is the enchantment that lets you automatically repair equipment?"
   1. Expected answer: Mending. It uses experience to repair.
   2. System response: The enchantment that lets you automatically repair equipment is Mending.
   3. Retrieval quality: Relevant
   4. Response accuracy: Partially accurate. I don't see mention of experience, though that's moreso that's because I didn't specify how to repair the equipment.
6. Question: "What are ways I can enchant my equipment?"
   1. Expected answer: Enchantment table, anvil, enchanted books, fishing.
   2. System generated: You can enchant your equipment by:
      1. Using an enchanting table
      2. Using an anvil
      3. Trading with villagers
      4. Fishing for treasure loot
      5. Obtaining mob drops
      6. Bartering with Piglins
      7. Finding generated loot from various structures
      8. Using the /enchant or /give commands.
   3. Retrieval quality: Relevant
   4. Response accuracy: Accurate

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
about specific enchantments from the "List of enchantments" — they returned _"I don't have
enough information in my sources to answer that."_

**What the system returned (before the fix):** A refusal. Searching the chunks showed why:
the only place "Mending" appeared in the whole Enchantment document was a conflict list
(_"Bow: Infinity and Mending"_) — the corpus said Mending _exists_ but never what it _does_.
The same defect produced content-free "stub" chunks elsewhere, e.g. _"…each trial chambers
ominous vault contains items drawn from 3 pools, with the following distribution:"_ and then
nothing. A corpus-wide scan found **19 of 233 chunks (~8%)** were these dangling stubs,
concentrated in **Trial Chambers (13)**.

**Root cause (tied to a specific pipeline stage):** Ingestion. `ingest.py` deleted every
`<table>` element to keep the text clean — but on minecraft.wiki the real loot and the
per-enchantment descriptions live _inside_ those tables. The lead-in sentence (a normal
`<p>`) survived; the table it pointed to was deleted, leaving a reference to data that was
no longer there.

**The fix (and why the first approach was wrong):** Instead of deleting tables, flatten
each content table (`wikitable`) into `col | col | col` text rows so the data survives as
embeddable content. This also required rewriting the ingestion walk from a flat scan of the
page's _direct_ children to a **recursive descent** of the whole document tree — many
tables (17 in Trial Chambers) are nested inside wrapper `<div>`s, so the flat walk never
reached them. (Note: the AI tool's first ingestion design deleted tables outright; the
recursive, table-preserving parse is the model I should have specified up front — see AI
Usage.)

**Verification (after the fix):** Dangling stubs dropped from **19/233 to 2/399** chunks,
and question #5 now answers correctly — _"The enchantment that lets you automatically repair
your items is Mending,"_ sourced to the Enchantment page. Other List-of-enchantments
questions (Silk Touch, Smite, Frost Walker) now answer correctly too, and the previously
working questions (Nether access, villager breeding) did not regress.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:**

The Chunking Strategy section did the hard thinking before I wrote any code. Because I'd already worked out that all-MiniLM-L6-v2 only embeds the first 256 tokens, the spec fixed my chunk size at ~250 tokens with ~45-token overlap for a concrete reason rather than a guess — so when I wrote chunker.py, those numbers (MAX_TOKENS = 250, OVERLAP_TOKENS = 45) dropped straight in. The spec's decision to split on the wiki's own section headers first and prepend an "Article > Section:" prefix to every chunk also translated directly into the implementation, so I never had to stop and second-guess my chunking approach mid-build.

**One way your implementation diverged from the spec, and why:**
The spec's Chunking Strategy covered size, overlap, and header-aware splitting, but it never anticipated how much non-gameplay boilerplate the wiki pages carried. During implementation I had to add a cleaning step the spec didn't mention — a blocklist of sections to drop (history changelogs, the table of contents, and the "Technical information" ID tables) — because those fragments were polluting retrieval and stealing top-k slots. I only discovered the full extent of this while evaluating retrieval, which is why the cleaning rules in ingest.py grew well beyond anything in the original plan.

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

- _What I gave the AI:_ my Documents list and Chunking Strategy from planning.md, plus
  stages 1–2 of the pipeline diagram, and asked it to write a script that fetches and
  cleans the 10 wiki articles into structured documents.
- _What it produced:_ an `ingest.py` that pulls each page via the MediaWiki API, strips
  page furniture, and splits the article by its section headers. To "keep the text clean"
  it deleted every HTML `<table>`.
- _What I changed or overrode:_ deleting tables was the wrong call, and it caused my
  Failure Case above — the enchantment descriptions and Trial Chambers loot live _inside_
  those tables, so questions about them returned "not enough information." In hindsight I
  should have specified the parsing model up front: the AI's flat parse only read the
  page's direct children, when what this wiki needs is a **recursive** parse that descends
  into nested wrappers and **flattens** content tables into text instead of discarding
  them. I directed that change; stubs fell from 19/233 to 2/399 and the failing
  enchantment questions started answering correctly.

**Instance 2 — grounded generation**

- _What I gave the AI:_ my Retrieval Approach section and stage 5 of the diagram, with the
  requirement that answers come only from retrieved chunks and that sources are attributed.
- _What it produced:_ a `generate.py` that passes the top-k chunks to Groq's
  llama-3.3-70b as context with a system prompt instructing it to answer only from that
  context and refuse otherwise.
- _What I changed or overrode:_ I made source attribution **programmatic** — the source
  list is built in code from the retrieved chunks' metadata, not parsed out of the LLM's
  answer — so attribution can't be hallucinated. I verified grounding by asking a question
  my corpus doesn't cover ("how do I tame a horse?"); the system correctly refused instead
  of answering from the model's training knowledge.

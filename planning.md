# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->

The domain that I chose is Minecraft information, hoping to be able to quickly answer questions about various content like the mobs, structures, dimensions and how to access them. This knowledge is particularly valuable because Minecraft is a game that's consistently being updated, each old feature is eventually given a use, and there aren't really any reliable official channels that can keep up (The wiki that I referred to has stated explicitly it's not actually sponsored by Mojang, it's a fandom project). From personal experience I did have some Minecraft guidebooks from over 10 years back, but that information is obviously outdated, and it would be a hassle for someone to rely on that for gameplay. In addition, the games themselves don't really have much of a tutorial after the basic opening inventory and getting a crafting table phase.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| #   | Source | Description | URL or location |
| --- | ------ | ----------- | --------------- |
| 1   |        |             |                 |
| 2   |        |             |                 |
| 3   |        |             |                 |
| 4   |        |             |                 |
| 5   |        |             |                 |
| 6   |        |             |                 |
| 7   |        |             |                 |
| 8   |        |             |                 |
| 9   |        |             |                 |
| 10  |        |             |                 |

---

1. Villagers
   1. Information on where do Minecraft villagers spawn, what use they have for a survival player (very good for trading and obtaining rare resources) and how to make more villagers.
   2. URL here: https://minecraft.wiki/w/Villager
2. Piglins
   1. Piglins are another important mob for gathering rare. resources, but they're distinct from villagers in that the players need a more specific set of requirements to find a Piglin
   2. https://minecraft.wiki/w/Piglin
3. Bartering
   1. Related to the previous URL on the piglins, bartering is a mechanic where the player throws a gold ingot at a Piglin and they will automatically pick it up, inspect it, and return a randomized item to the player.
   2. https://minecraft.wiki/w/Bartering
4. Ender Dragon
   1. The Ender Dragon is the final boss of Minecraft, it would be helpful for the player to know what its gameplay loop is, such as how it moves, what attacks to watch out for and what structures in the boss fight would be vital to look out for.
   2. https://minecraft.wiki/w/Ender_Dragon
5. Illagers
   1. Illagers are a type of hostile mob where after the player completes a certain set of conditions, they spawn in raids that occur in villages and should the player be successful in fending off the raid, they are rewarded with valuable resources.
   2. https://minecraft.wiki/w/Illager
6. Enchantments
   1. This game mechanic allows the player to enhance their equipment (weapons, tools, armor) to be more effective at their intended purpose. There are a wide range of possible enchantments, but the conditions to getting one are worthy of lots of analysis, plus there's cases in which enchantments are incompatible, yet Minecraft itself doesn't explicitly spell it out loud.
   2. https://minecraft.wiki/w/Enchantment
7. Slimes
   1. Slimes are a type of mob who drop slime balls upon death, a material that is useful in redstone, construction, brewing. Though from my own personal experience I've never been able to find a lot of slimes or figure out how to make the conditions right for them to spawn. I would hope for this project to help simplify the info by chunking.
   2. https://minecraft.wiki/w/Slime
8. The end
   1. The final boss dimension. The player needs to fight the Ender Dragon, then upon its defeat, unlock portals to go to end cities, which have an abundance of important resources.
   2. https://minecraft.wiki/w/The_End
9. The nether
   1. The precursor to the end. A hellish dimension filled with hostile mobs, new blocks and new structures. The player needs to go to this dimension to get some majorly important resources like blaze powder, netherrack blocks, quartz blocks, nether bricks, ender pearls.
   2. https://minecraft.wiki/w/The_Nether
10. Trial Chambers
    1. An uncommon underground structure where the player is given minigames that they need to pass to obtain very handy resources. I wasn't playing Minecraft at the time of these structures being added, so this is also a new learning experience for me
    2. https://minecraft.wiki/w/Trial_Chambers

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

**Chunk size:**
I consulted with Claude based on these articles that I sent them, and the recommendation was about 250 token chunk sizes (~180 words).

**Overlap:**
40-50 tokens (that is, about 1-2 sentences)

**Reasoning:**

The 250 token size is tied directly to my embedding model. I'm using all-MiniLM-L6-v2, which only reads the first 256 tokens of any chunk and silently ignores everything past that. So there's no point making chunks bigger than ~250 tokens, since the extra text wouldn't even get embedded. Capping right under that limit means the whole chunk actually contributes to the vector.

The Minecraft wiki articles are also a good fit for this size because they're already broken into clear sections with headers (e.g. "Accessing", "Traits", "Mobs", "Biomes"). Rather than cutting blindly every 250 tokens, I'll split on those headers first so each chunk stays about one topic, and only sub-split the longer sections (like Environment) down to the ~250 token target. I'll also prepend the article title and section name to each chunk (like "The Nether > Mobs:") so a chunk keeps its context even when the raw sentence doesn't mention the dimension by name.

The 40-50 token (1-2 sentence) overlap is mainly for those sub-splits inside long sections. It keeps a fact from getting cut in half right at a boundary. I'm keeping the overlap small because splitting on headers already gives clean topical breaks, so I don't need heavy overlap the way a wall-of-text FAQ would.

One thing specific to this corpus: a huge portion of each article (roughly 40%) is version-by-version History, plus Advancements, Achievements, Gallery, and Videos sections. Since this guide is about how to actually play, I'll filter those sections out before chunking. They'd otherwise flood retrieval with off-topic changelog text (e.g. "1.16 added piglins") instead of the actual gameplay info.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

**Embedding model:**
all-MiniLM-L6-v2

**Top-k:**
Top 5 chunks per query.

I went with 5 chunks because a lot of my questions natrually span more than one section or even more than one article, like if I wanted to ask "How do I barter with piglins in the Nether?" that simple question would require pulling from multiple sources such as the Piglin, Bartering and Nether pages, and with ~250 token chunks, that information is spread across smaller chunks. Five would give the LLM sufficient surrounding conext to assemble a complete answer.

**Production tradeoff reflection:**

Given that I had chosen all-MiniLM-L6-v2, I can expect a small, fast, local-running service that is free, and ideal for this project. It works well on the short factual chunks that my questions might need.

- Domain accuracy — Minecraft text is full of game-specific jargon ("netherrack", "blaze powder", "bastion remnant") and MiniLM is a small general-purpose model. A stronger model like all-mpnet-base-v2 or a top retriever like BGE-large / E5-large would likely rank the right chunk higher on tricky queries. The ceiling option would be fine-tuning an embedding model on Minecraft text, which would capture the domain best but takes real effort and data.

- Context length — MiniLM only embeds the first 256 tokens, which is what forced my small chunk size. A model with a 512+ token window would let me use larger chunks and cut down on facts getting fragmented across chunk boundaries.
-
- Latency — MiniLM is one of the fastest models, so larger/heavier models or hosted API embeddings (e.g. OpenAI text-embedding-3-large, Voyage) would trade some response speed for accuracy. For an interactive Q&A tool I'd want to keep query-time embedding fast, so I'd benchmark this rather than just assume bigger is better.

- Multilingual support — my sources and users are English-only, so I don't need it now. But if I wanted non-English players to ask questions, I'd need to switch to something like multilingual-e5 or paraphrase-multilingual-MiniLM, accepting a slightly larger model for that reach.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| #   | Question | Expected answer |
| --- | -------- | --------------- |
| 1   |          |                 |
| 2   |          |                 |
| 3   |          |                 |
| 4   |          |                 |
| 5   |          |                 |

---

1. How do I go to the Nether in the first place?
   1. I expect an answer with the following idea: "You will need Obsidian and a fire source, have at least enough Obsidian to make a 4 x 5 pattern frame, then use your fire source in the center of the frame. If you see a purple outline, then go into it and after a few seconds, you will be in the Nether.
2. How do I get more villagers without finding a village?
   1. I expect an answer that sounds like: You can cure a zombie villager if they happen to spawn at night and then throw a weakness potion and use a golden Apple. Alternatively, you can breed villagers by giving them enough food (12 carrots, 12 potatoes, 3 bread or 12 beetroot) and make sure that there is a bed that hasn't been claimed by any other villagers or players.
3. How do I get ender pearls in the Nether? I can't find any Endermen.
   1. I expect that this one will give multiple options. Either: 1) Go to the blue biome, Endermen are most abundant there, then kill the Endermen for the pearls. Or 2) Mine the gold ore in the Nether, craft gold ingots, then throw the ingots to nearby Piglins. This will start a barter and there is a chance you may get Ender pearls.
4. How do I get that cool pair of wings that I see lots of Minecraft youtubers wearing that let me fly?
   1. 1. Go to the end 2) Beat the Ender Dragon 3) Go into one of the portals on the outer edges of the island 4) Keep exploring the end islands until you see an end city, some of them have end ships behind them. 5) Stack up, go into the ship, you will find your Elytra.
5. What is the enchantment that lets me automatically repair my items?
   1. Ah, the enchantment you're thinking of is Mending, which is a treasure enchantment that can only be found in certain structures or by trading with a Librarian villager (is RNG dependent) for the enchanted book.

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1.

2.

---

1. Vocabulary mismatch between casual questions and wiki jargon. Q4 and Q5 are literally this — users say "wings that let me fly" and "auto-repair," but the docs say "Elytra" and "Mending." A small general model like MiniLM can struggle to map slang/descriptions onto game terms it has little training signal for, so the right chunk may not land in the top-k. Mitigation: the title/section prefixes from your chunking help a bit; I could also test a higher top-k or a stronger embedding model on exactly these questions.
2. Version/edition conflicts inside a single article. This one is specific to your domain — you chose Minecraft because it keeps changing. The wiki encodes that change: History sections and Java-vs-Bedrock differences mean one article states different behavior for different versions. If a stale or wrong-edition chunk gets retrieved, the LLM may give version-incorrect advice (e.g. old spawn rules or changed barter loot). Mitigation: this is partly why you're filtering History before chunking; you could also prefer current-version sections.

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

---

![alt text](<Screenshot 2026-06-03 at 3.26.35 PM.jpg>)

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**

- Planning on using Claude as my tool.
- The inputs will be my documents list, chunking strategy section and stages 1-2 of the diagram.
- Ask it to produce: a script that fetches & cleans the 10 articles into documents/, and a chunk_text() that does header-aware splitting at ~250 tokens / 40–50 overlap, adds the "Article > Section:" prefix, and attaches {source, section, url} metadata
- Verify: run it on The Nether and eyeball the chunks — right size, prefixes present, metadata attached, no tables cut in half

**Milestone 4 — Embedding and retrieval:**
Tool: Claude
Input: my Retrieval Approach section + stages 3–4 of the diagram
Ask it to produce: code to embed all chunks with all-MiniLM-L6-v2, store them in ChromaDB with their metadata, and a retrieve(query, k=5) function
Verify: run my 5 eval questions and check the retrieved chunks come from the right articles (e.g. Q3 should pull both Nether and Bartering), and confirm the query is embedded with the same model as the chunks

**Milestone 5 — Generation and interface:**
Tool: Claude
Input: stage 5 of the diagram + my Evaluation Plan questions
Ask it to produce: a prompt template that answers only from the retrieved context and cites the source, the Groq API call (llama-3.3-70b), and a simple CLI question→answer loop
Verify: run all 5 questions end-to-end against my expected answers, and confirm it cites sources and says "not in my sources" when the context doesn't cover something

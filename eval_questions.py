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

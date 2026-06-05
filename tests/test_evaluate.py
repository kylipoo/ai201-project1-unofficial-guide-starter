from evaluate import answer_similarity, to_markdown


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


def test_empty_or_none_returns_zero():
    assert answer_similarity("", "Build a portal.") == 0.0
    assert answer_similarity("Build a portal.", "") == 0.0
    assert answer_similarity(None, "Build a portal.") == 0.0


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

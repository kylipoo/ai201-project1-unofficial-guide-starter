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

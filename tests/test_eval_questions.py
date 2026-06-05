from eval_questions import EVAL_SET, EVAL_QUESTIONS


def test_eval_set_has_five_complete_items():
    assert len(EVAL_SET) == 5
    for expected_id, item in enumerate(EVAL_SET, 1):
        assert item["id"] == expected_id
        assert item["question"].strip()
        assert item["ground_truth"].strip()


def test_eval_questions_derived_from_set():
    assert EVAL_QUESTIONS == [item["question"] for item in EVAL_SET]
    assert len(EVAL_QUESTIONS) == 5

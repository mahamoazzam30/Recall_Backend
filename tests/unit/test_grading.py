from app.db.models.question import Question, QuestionType
from app.services.grading import grade_deterministic


def _mcq_question() -> Question:
    return Question(
        type=QuestionType.mcq,
        prompt="What is 2+2?",
        choices=["3", "4", "5", "6"],
        answer_key="4",
    )


def test_deterministic_mcq_exact_match_is_correct():
    score, feedback = grade_deterministic(_mcq_question(), "4")
    assert score == 1.0
    assert feedback == "Correct."


def test_deterministic_mcq_wrong_choice_is_incorrect():
    score, feedback = grade_deterministic(_mcq_question(), "5")
    assert score == 0.0
    assert "Incorrect" in feedback


def test_deterministic_grading_normalizes_whitespace_and_case():
    question = Question(type=QuestionType.cloze, prompt="The sky is ____.", answer_key="Blue")
    score, _ = grade_deterministic(question, "  blue  ")
    assert score == 1.0

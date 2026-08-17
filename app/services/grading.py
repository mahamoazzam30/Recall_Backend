"""Grading skill.

Deterministic question types (MCQ/cloze) are graded in plain code — no model
call needed, per the code-vs-model design principle. Only short-answer goes
to the LLM (Claude), grounded explicitly in the source passage.
"""
import json
import re
from datetime import datetime, timezone

from app.db.models.attempt import Attempt
from app.db.models.chunk import Chunk
from app.db.models.question import Question, QuestionType
from app.llm.claude_client import ClaudeClient

SYSTEM_PROMPT = (
    "You are a strict but fair grader for a study app. Score the student's answer "
    "against the answer key, grounded explicitly in the provided passage. "
    "Give partial credit where reasonable. "
    'Return strict JSON: {"score": <float 0-1>, "feedback": "<short explanation of what was missed, '
    'citing the passage>"}.'
)


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip().lower())


def grade_deterministic(question: Question, student_answer: str) -> tuple[float, str]:
    """Grade MCQ/cloze via exact/normalized match. No model call."""
    correct = _normalize(question.answer_key) == _normalize(student_answer)
    score = 1.0 if correct else 0.0
    feedback = "Correct." if correct else f"Incorrect. The correct answer was: {question.answer_key}"
    return score, feedback


async def grade_short_answer(
    question: Question, chunk: Chunk, student_answer: str, client: ClaudeClient | None = None
) -> tuple[float, str]:
    client = client or ClaudeClient()

    user_prompt = (
        f"Passage:\n{chunk.content}\n\n"
        f"Question: {question.prompt}\n"
        f"Reference answer: {question.answer_key}\n"
        f"Student answer: {student_answer}\n\n"
        "Grade the student answer."
    )
    raw = await client.complete(SYSTEM_PROMPT, user_prompt, call_site="grading")

    try:
        payload = json.loads(raw)
        score = max(0.0, min(1.0, float(payload["score"])))
        feedback = str(payload["feedback"])
    except (json.JSONDecodeError, KeyError, ValueError, TypeError):
        # If the grader response is malformed, fail safe rather than silently
        # awarding credit — surface it as ungraded so the frontend can retry.
        raise ValueError(f"malformed grading response: {raw!r}")

    return score, feedback


async def grade_attempt(attempt: Attempt, question: Question, chunk: Chunk) -> Attempt:
    if question.type in (QuestionType.mcq, QuestionType.cloze):
        score, feedback = grade_deterministic(question, attempt.student_answer)
    else:
        score, feedback = await grade_short_answer(question, chunk, attempt.student_answer)

    attempt.score = score
    attempt.feedback = feedback
    attempt.graded_at = datetime.now(timezone.utc)
    return attempt

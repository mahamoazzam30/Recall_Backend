"""Question-generation skill.

Calls the fast/cheap model via OpenRouter with a strict system prompt to
generate a question grounded only in the given passage. Validates the
response and enforces the anti-drift guardrail: every question must trace
back to its source chunk_id, or it's rejected.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.db.models.concept import Concept
from app.db.models.question import Question, QuestionType
from app.llm.openrouter_client import OpenRouterClient

SYSTEM_PROMPT = (
    "You are a question-generation engine for a study app. Generate a question "
    "ONLY from the passage below. Do not introduce facts not present in the passage. "
    "Respond with ONLY a single JSON object and nothing else — no explanation, no markdown "
    "code fences, no text before or after the JSON. Your entire response must start with { "
    "and end with }.\n\n"
    'Return strict JSON of the form: {"type": "mcq|cloze|short_answer", "prompt": "...", '
    '"choices": ["..."] | null, "answer_key": "...", "concept_tag": "short concept name"}. '
    "For mcq, choices must contain 4 options and answer_key must be the exact correct choice text. "
    "For cloze, prompt must contain a blank marked with ____ and answer_key is the missing text. "
    "For short_answer, choices must be null and answer_key is the ideal answer.\n\n"
    'Example valid response: {"type": "mcq", "prompt": "What gas do plants release during '
    'photosynthesis?", "choices": ["Oxygen", "Nitrogen", "Hydrogen", "Helium"], '
    '"answer_key": "Oxygen", "concept_tag": "Photosynthesis"}'
)

_REQUIRED_KEYS = {"type", "prompt", "answer_key", "concept_tag"}


class GenerationError(Exception):
    pass


def _validate_payload(payload: dict) -> None:
    if not _REQUIRED_KEYS.issubset(payload.keys()):
        raise GenerationError(f"missing keys: {_REQUIRED_KEYS - payload.keys()}")
    if payload["type"] not in {t.value for t in QuestionType}:
        raise GenerationError(f"invalid type: {payload['type']}")
    if payload["type"] == "mcq":
        choices = payload.get("choices")
        if not choices or len(choices) != 4 or payload["answer_key"] not in choices:
            raise GenerationError("mcq requires 4 choices including the answer_key")


def _get_or_create_concept(db: Session, course_id: uuid.UUID, concept_tag: str) -> Concept:
    stmt = select(Concept).where(Concept.course_id == course_id, Concept.name == concept_tag)
    concept = db.execute(stmt).scalar_one_or_none()
    if concept is None:
        concept = Concept(course_id=course_id, name=concept_tag)
        db.add(concept)
        db.flush()
    return concept


async def generate_question(
    db: Session,
    chunk: Chunk,
    course_id: uuid.UUID,
    desired_type: QuestionType | None = None,
    concept_override: str | None = None,
    client: OpenRouterClient | None = None,
) -> Question:
    """Generate a question from `chunk`, retrying once on a bad/untraceable response.

    If `concept_override` is set, the question is tagged into that concept
    directly instead of whatever concept name the model guesses — used when
    the student has already picked a specific topic to be quizzed on.
    """
    client = client or OpenRouterClient()

    type_hint = f" The question type must be '{desired_type.value}'." if desired_type else ""
    user_prompt = f"Passage (chunk_id={chunk.id}):\n{chunk.content}\n\nGenerate one question from this passage.{type_hint}"

    last_error: Exception | None = None
    for _attempt in range(2):
        try:
            payload = await client.complete_json(SYSTEM_PROMPT, user_prompt, call_site="generation")
            _validate_payload(payload)
            break
        except Exception as exc:  # malformed JSON, validation failure, network error
            last_error = exc
            continue
    else:
        raise GenerationError(f"generation failed after retry: {last_error}")

    concept = _get_or_create_concept(db, course_id, concept_override or payload["concept_tag"])

    question = Question(
        chunk_id=chunk.id,
        concept_id=concept.id,
        type=QuestionType(payload["type"]),
        prompt=payload["prompt"],
        choices=payload.get("choices"),
        answer_key=payload["answer_key"],
    )
    db.add(question)
    db.commit()
    db.refresh(question)
    return question

"""Topic extraction: surfaces the topics covered in a course's materials so
a student can pick one before a quiz is generated, instead of only being
able to see topics after questions already happen to exist for them.

Extracted topics are persisted as Concepts (the same table question
generation tags questions into), so once a topic is picked, quiz generation
can reuse or build directly onto it rather than guessing a fresh, possibly
mismatched concept name.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.db.models.concept import Concept
from app.db.models.material import Material
from app.llm.openrouter_client import OpenRouterClient

SYSTEM_PROMPT = (
    "You are a curriculum analyst. Given excerpts from a student's course materials, extract the "
    "distinct topics they cover, ordered roughly as they appear in the material. Respond with ONLY "
    'a JSON object of the form {"topics": ["Topic name", ...]} — between 4 and 12 concise topic '
    "names (2-5 words each), with no duplicates or near-duplicates and no numbering. No "
    "explanation, no markdown fences — your entire response must start with { and end with }."
)

_MAX_CHARS = 12000


async def list_topics(
    db: Session, course_id: uuid.UUID, client: OpenRouterClient | None = None
) -> list[Concept]:
    """Return the course's topics, extracting and caching them as Concepts on first call."""
    existing = list(
        db.execute(
            select(Concept).where(Concept.course_id == course_id).order_by(Concept.created_at)
        ).scalars().all()
    )
    if existing:
        return existing

    chunk_texts = list(
        db.execute(
            select(Chunk.content)
            .join(Material, Chunk.material_id == Material.id)
            .where(Material.course_id == course_id)
            .order_by(Chunk.created_at)
        ).scalars().all()
    )
    if not chunk_texts:
        return []

    text = ""
    for content in chunk_texts:
        if len(text) + len(content) > _MAX_CHARS:
            break
        text += content + "\n\n"

    client = client or OpenRouterClient()
    payload = await client.complete_json(SYSTEM_PROMPT, text, call_site="topics")
    raw_names = [n.strip() for n in payload.get("topics", []) if isinstance(n, str) and n.strip()]

    seen: set[str] = set()
    concepts: list[Concept] = []
    for name in raw_names:
        key = name.lower()
        if key in seen:
            continue
        seen.add(key)
        concept = Concept(course_id=course_id, name=name)
        db.add(concept)
        concepts.append(concept)

    db.commit()
    for concept in concepts:
        db.refresh(concept)

    return concepts

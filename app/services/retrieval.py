"""'Search my notes' tool.

Exposed to the generation/grading skills as a callable tool — not just an
internal helper — so the agent primitive (retrieval) is real, not simulated.
"""
import uuid

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.db.models.material import Material
from app.llm.embeddings import embed_text


async def search(db: Session, query: str, course_id: uuid.UUID, top_k: int = 5) -> list[Chunk]:
    """Embed `query` and return the top-k nearest chunks (cosine distance) within a course."""
    query_vector = await embed_text(query)

    stmt = (
        select(Chunk)
        .join(Material, Chunk.material_id == Material.id)
        .where(Material.course_id == course_id)
        .order_by(Chunk.embedding.cosine_distance(query_vector))
        .limit(top_k)
    )
    return list(db.execute(stmt).scalars().all())

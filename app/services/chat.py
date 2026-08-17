"""Course chat: answers a student's question grounded only in that course's
ingested material, reusing the same retrieval pipeline as quiz generation.
"""
import uuid

from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.llm.claude_client import ClaudeClient
from app.services import retrieval

SYSTEM_PROMPT = (
    "You are a study assistant answering a student's question about their course notes. "
    "Answer ONLY using the passages below. If the passages don't contain the answer, say "
    "you don't have that information in the uploaded materials — never make things up. "
    "Keep answers concise and direct."
)


async def answer_question(
    db: Session, course_id: uuid.UUID, question: str, client: ClaudeClient | None = None
) -> tuple[str, list[Chunk]]:
    chunks = await retrieval.search(db, question, course_id, top_k=5)
    if not chunks:
        return "I don't have any materials for this course yet — upload some notes first.", []

    client = client or ClaudeClient()
    context = "\n\n".join(f"[Passage {i + 1}]\n{c.content}" for i, c in enumerate(chunks))
    user_prompt = f"Passages:\n{context}\n\nQuestion: {question}"
    answer = await client.complete(SYSTEM_PROMPT, user_prompt, call_site="chat")
    return answer, chunks

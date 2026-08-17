"""Upload & chunking pipeline.

1. Validate file type (PDF/MD/TXT).
2. Chunk text (target ~300-500 tokens, sentence-boundary aware, slight overlap).
3. Embed each chunk and bulk-insert into `chunks`.
4. Mark `materials.status = ready`.

Run as a FastAPI BackgroundTasks job for v1 (see proposal: swap for a queue
like arq/Celery only if upload volume justifies it).
"""
import re
import uuid

from sqlalchemy.orm import Session

from app.db.models.chunk import Chunk
from app.db.models.material import Material, MaterialStatus, SourceType
from app.llm.embeddings import embed_texts

_CHUNK_TARGET_TOKENS = 400
_CHUNK_OVERLAP_TOKENS = 50
_MIN_TEXT_CHARS_FOR_VALID_EXTRACTION = 200


def extract_text(raw_bytes: bytes, source_type: SourceType) -> str:
    if source_type == SourceType.pdf:
        return _extract_pdf_text(raw_bytes)
    return raw_bytes.decode("utf-8", errors="ignore")


def _extract_pdf_text(raw_bytes: bytes) -> str:
    import io

    import pdfplumber

    text_parts: list[str] = []
    with pdfplumber.open(io.BytesIO(raw_bytes)) as pdf:
        for page in pdf.pages:
            text_parts.append(page.extract_text() or "")
    return "\n\n".join(text_parts)


def chunk_text(text: str, target_tokens: int = _CHUNK_TARGET_TOKENS, overlap_tokens: int = _CHUNK_OVERLAP_TOKENS) -> list[str]:
    """Sentence-boundary-aware chunking with slight overlap.

    Approximates tokens as whitespace-split words (good enough for v1 chunk sizing).
    """
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks: list[str] = []
    current: list[str] = []
    current_len = 0

    for sentence in sentences:
        sentence_len = len(sentence.split())
        if current_len + sentence_len > target_tokens and current:
            chunks.append(" ".join(current))
            overlap_words = " ".join(current).split()[-overlap_tokens:]
            current = [" ".join(overlap_words)] if overlap_words else []
            current_len = len(overlap_words)
        current.append(sentence)
        current_len += sentence_len

    if current:
        chunks.append(" ".join(current))

    return [c.strip() for c in chunks if c.strip()]


async def ingest_material(db: Session, material_id: uuid.UUID, raw_bytes: bytes) -> None:
    material = db.get(Material, material_id)
    if material is None:
        return

    try:
        text = extract_text(raw_bytes, material.source_type)
    except Exception:
        material.status = MaterialStatus.failed
        db.commit()
        return

    if material.source_type == SourceType.pdf and len(text.strip()) < _MIN_TEXT_CHARS_FOR_VALID_EXTRACTION:
        # Handwritten/scanned PDFs are out of scope for v1 (per proposal risk mitigation).
        material.status = MaterialStatus.needs_review
        db.commit()
        return

    pieces = chunk_text(text)
    if not pieces:
        material.status = MaterialStatus.needs_review
        db.commit()
        return

    embeddings = await embed_texts(pieces)

    for i, (content, embedding) in enumerate(zip(pieces, embeddings)):
        db.add(
            Chunk(
                material_id=material.id,
                content=content,
                embedding=embedding,
                char_range=f"chunk-{i}",
            )
        )

    material.status = MaterialStatus.ready
    db.commit()

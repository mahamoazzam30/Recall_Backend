import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class QuestionType(str, enum.Enum):
    mcq = "mcq"
    cloze = "cloze"
    short_answer = "short_answer"


class Question(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "questions"

    chunk_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("chunks.id"), nullable=False)
    concept_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("concepts.id"), nullable=False)
    type: Mapped[QuestionType] = mapped_column(Enum(QuestionType, name="question_type"), nullable=False)
    prompt: Mapped[str] = mapped_column(Text, nullable=False)
    choices: Mapped[list | None] = mapped_column(JSONB, nullable=True)
    answer_key: Mapped[str] = mapped_column(Text, nullable=False)

    chunk: Mapped["Chunk"] = relationship(back_populates="questions")
    concept: Mapped["Concept"] = relationship(back_populates="questions")
    attempts: Mapped[list["Attempt"]] = relationship(back_populates="question", cascade="all, delete-orphan")

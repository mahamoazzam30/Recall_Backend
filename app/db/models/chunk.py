import uuid

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.config import get_settings
from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin

_settings = get_settings()


class Chunk(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "chunks"

    material_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("materials.id"), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    embedding: Mapped[list[float] | None] = mapped_column(Vector(_settings.embedding_dim), nullable=True)
    page_ref: Mapped[str | None] = mapped_column(String(64), nullable=True)
    char_range: Mapped[str | None] = mapped_column(String(64), nullable=True)

    material: Mapped["Material"] = relationship(back_populates="chunks")
    questions: Mapped[list["Question"]] = relationship(back_populates="chunk", cascade="all, delete-orphan")

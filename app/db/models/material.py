import enum
import uuid

from sqlalchemy import Enum, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class SourceType(str, enum.Enum):
    pdf = "pdf"
    md = "md"
    txt = "txt"


class MaterialStatus(str, enum.Enum):
    processing = "processing"
    ready = "ready"
    needs_review = "needs_review"
    failed = "failed"


class Material(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "materials"

    subject_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("subjects.id"), nullable=False)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    source_type: Mapped[SourceType] = mapped_column(Enum(SourceType, name="source_type"), nullable=False)
    status: Mapped[MaterialStatus] = mapped_column(
        Enum(MaterialStatus, name="material_status"), default=MaterialStatus.processing, nullable=False
    )

    subject: Mapped["Subject"] = relationship(back_populates="materials")
    chunks: Mapped[list["Chunk"]] = relationship(back_populates="material", cascade="all, delete-orphan")

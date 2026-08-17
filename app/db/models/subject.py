import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class Subject(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "subjects"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    user: Mapped["User"] = relationship(back_populates="subjects")
    materials: Mapped[list["Material"]] = relationship(back_populates="subject", cascade="all, delete-orphan")
    concepts: Mapped[list["Concept"]] = relationship(back_populates="subject", cascade="all, delete-orphan")

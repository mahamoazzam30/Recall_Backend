import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class Course(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "courses"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    color_tag: Mapped[str | None] = mapped_column(String(20), nullable=True)

    user: Mapped["User"] = relationship(back_populates="courses")
    modules: Mapped[list["Module"]] = relationship(back_populates="course", cascade="all, delete-orphan")
    materials: Mapped[list["Material"]] = relationship(back_populates="course", cascade="all, delete-orphan")
    concepts: Mapped[list["Concept"]] = relationship(back_populates="course", cascade="all, delete-orphan")

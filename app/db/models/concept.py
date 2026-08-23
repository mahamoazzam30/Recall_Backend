import uuid

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class Concept(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "concepts"

    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    course: Mapped["Course"] = relationship(back_populates="concepts")
    questions: Mapped[list["Question"]] = relationship(back_populates="concept")
    mastery_rows: Mapped[list["Mastery"]] = relationship(back_populates="concept")
    schedule_items: Mapped[list["ScheduleItem"]] = relationship(back_populates="concept")

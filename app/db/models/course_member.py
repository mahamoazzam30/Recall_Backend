import uuid

from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class CourseMember(UUIDPKMixin, TimestampMixin, Base):
    """A study-group member on a course the current user doesn't own."""

    __tablename__ = "course_members"
    __table_args__ = (UniqueConstraint("course_id", "user_id", name="uq_course_members_course_user"),)

    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    course: Mapped["Course"] = relationship(back_populates="members")
    user: Mapped["User"] = relationship()

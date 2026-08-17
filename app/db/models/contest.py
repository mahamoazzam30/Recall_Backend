import enum
import uuid

from sqlalchemy import Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class ContestStatus(str, enum.Enum):
    open = "open"
    resolved = "resolved"


class Contest(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "contests"

    attempt_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("attempts.id"), nullable=False)
    student_note: Mapped[str] = mapped_column(Text, nullable=False)
    status: Mapped[ContestStatus] = mapped_column(
        Enum(ContestStatus, name="contest_status"), default=ContestStatus.open, nullable=False
    )
    resolution_note: Mapped[str | None] = mapped_column(Text, nullable=True)

    attempt: Mapped["Attempt"] = relationship(back_populates="contests")

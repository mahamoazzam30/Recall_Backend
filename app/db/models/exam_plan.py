import enum
import uuid
from datetime import date as date_

from sqlalchemy import Boolean, Date, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base_class import Base
from app.db.models.mixins import TimestampMixin, UUIDPKMixin


class ExamPlanStatus(str, enum.Enum):
    active = "active"
    completed = "completed"
    cancelled = "cancelled"


class ExamPlan(UUIDPKMixin, TimestampMixin, Base):
    __tablename__ = "exam_plans"

    course_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("courses.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    exam_date: Mapped[date_] = mapped_column(Date, nullable=False)
    status: Mapped[ExamPlanStatus] = mapped_column(
        Enum(ExamPlanStatus, name="exam_plan_status"), default=ExamPlanStatus.active, nullable=False
    )

    days: Mapped[list["ExamPlanDay"]] = relationship(back_populates="exam_plan", cascade="all, delete-orphan")


class ExamPlanDay(UUIDPKMixin, Base):
    __tablename__ = "exam_plan_days"

    exam_plan_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("exam_plans.id"), nullable=False
    )
    date: Mapped[date_] = mapped_column(Date, nullable=False)
    target_concept_ids: Mapped[list[str]] = mapped_column(JSONB, nullable=False)
    completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    exam_plan: Mapped["ExamPlan"] = relationship(back_populates="days")

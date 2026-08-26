import uuid
from datetime import date

from pydantic import BaseModel

from app.db.models.exam_plan import ExamPlanStatus


class ExamPlanCreate(BaseModel):
    exam_date: date


class ExamPlanUpdate(BaseModel):
    exam_date: date | None = None
    status: ExamPlanStatus | None = None


class ExamPlanResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    exam_date: date
    status: ExamPlanStatus
    days_left: int
    readiness_pct: float
    today_target_concept_ids: list[uuid.UUID]

    model_config = {"from_attributes": True}

import uuid
from datetime import datetime

from pydantic import BaseModel

from app.schemas.material import MaterialResponse


class CourseCreate(BaseModel):
    name: str
    color_tag: str | None = None


class CourseResponse(BaseModel):
    id: uuid.UUID
    name: str
    color_tag: str | None
    created_at: datetime

    model_config = {"from_attributes": True}


class CourseListItem(CourseResponse):
    mastery_pct: float
    due_count: int


class ModuleCreate(BaseModel):
    name: str
    order_index: int = 0


class ModuleResponse(BaseModel):
    id: uuid.UUID
    course_id: uuid.UUID
    name: str
    order_index: int

    model_config = {"from_attributes": True}


class CourseDetailResponse(BaseModel):
    course: CourseResponse
    modules: list[ModuleResponse]
    materials: list[MaterialResponse]
    mastery_pct: float
    due_count: int


class CourseMasteryOut(BaseModel):
    concept_id: uuid.UUID
    concept_name: str
    accuracy_ema: float
    repetitions: int


class CourseDueTodayOut(BaseModel):
    concept_id: uuid.UUID
    concept_name: str
    due_at: datetime


class CourseDashboardResponse(BaseModel):
    mastery: list[CourseMasteryOut]
    due_today: list[CourseDueTodayOut]
    current_streak_days: int
    longest_streak_days: int

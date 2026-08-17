import uuid
from datetime import datetime

from pydantic import BaseModel


class MasteryOut(BaseModel):
    concept_id: uuid.UUID
    concept_name: str
    accuracy_ema: float
    repetitions: int


class DueTodayOut(BaseModel):
    concept_id: uuid.UUID
    concept_name: str
    due_at: datetime


class StreakOut(BaseModel):
    current_streak_days: int
    longest_streak_days: int


class HistoryPoint(BaseModel):
    date: datetime
    concept_id: uuid.UUID
    concept_name: str
    accuracy: float

import uuid
from datetime import datetime

from pydantic import BaseModel


class WeakSpotOut(BaseModel):
    concept_id: uuid.UUID
    concept_name: str
    mastery_pct: float
    error_note: str | None
    last_reviewed_at: datetime | None

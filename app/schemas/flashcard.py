import enum
import uuid

from pydantic import BaseModel

from app.db.models.question import QuestionType


class RecallRating(str, enum.Enum):
    forgot = "forgot"
    struggled = "struggled"
    knew_it = "knew_it"


RECALL_SCORE: dict[RecallRating, float] = {
    RecallRating.forgot: 0.0,
    RecallRating.struggled: 0.6,
    RecallRating.knew_it: 1.0,
}


class FlashcardOut(BaseModel):
    id: uuid.UUID
    type: QuestionType
    prompt: str
    answer_key: str
    concept_id: uuid.UUID

    model_config = {"from_attributes": True}


class FlashcardSessionResponse(BaseModel):
    cards: list[FlashcardOut]


class FlashcardReviewCreate(BaseModel):
    question_id: uuid.UUID
    recall: RecallRating


class FlashcardReviewResponse(BaseModel):
    question_id: uuid.UUID
    score: float
    mastery_pct: float
